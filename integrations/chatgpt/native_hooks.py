# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Execute the original native hooks inside a source-bound research workspace.

This adapter does not install ChatGPT-wide hooks or substitute workflow_local
policies. The caller supplies a trusted release and a separate writable clone.
Native JSON decisions and latest traces remain unchanged; hosted receipts are
written separately so a warning is never silently strengthened into a block.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict, dataclass
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile

EVENT_SCRIPTS = {
    "UserPromptSubmit": "hooks/scripts/user_prompt_submit_intake.py",
    "PreSkillUse": "hooks/scripts/pre_skill_use_policy.py",
    "PostSkillUse": "hooks/scripts/post_skill_use_review.py",
    "PreToolUse": "hooks/scripts/pre_tool_use_policy.py",
    "Stop": "hooks/scripts/stop_artifact_check.py",
}
JOURNAL = "agentic/traces/hosted_native_hooks/events.jsonl"
MAX_PAYLOAD_BYTES = 64 * 1024


class NativeHookError(ValueError):
    """The adapter could not establish a valid native hook decision."""


class NativeHookBlocked(NativeHookError):
    """A successfully executed native policy rejected the proposed action."""

    def __init__(self, receipt: "HookReceipt"):
        self.receipt = receipt
        super().__init__(f"{receipt.event}: {receipt.result['reason']}")


@dataclass(frozen=True)
class HookReceipt:
    """Bind one exact input and native result to its source and latest trace."""

    event: str
    script: str
    source_digest: str
    payload_sha256: str
    result: dict
    native_trace: str
    native_trace_sha256: str

    @property
    def allowed(self) -> bool:
        return self.result["decision"] != "block"

    def as_dict(self) -> dict:
        return asdict(self)


def _json_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, allow_nan=False).encode("utf-8")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _confined(root: Path, relative: str) -> Path:
    """Reject traversal and links before native code reads or writes a path."""
    if (
        not isinstance(relative, str)
        or not relative
        or "\\" in relative
        or PurePosixPath(relative).is_absolute()
        or any(part in {"", ".", ".."} for part in relative.split("/"))
    ):
        raise NativeHookError("Hook paths must be canonical workspace-relative paths")
    candidate = root / relative
    for part in (candidate, *candidate.parents):
        if part == root:
            break
        if part.is_symlink():
            raise NativeHookError("Hook paths cannot contain symlinks")
    candidate.resolve().relative_to(root)
    return candidate


def _source_files(root: Path) -> dict[str, str]:
    """Pin executable hook bytes and the native membership registry namespace."""
    scripts = _confined(root, "hooks/scripts")
    registry = _confined(root, "registry/tasks")
    if registry.exists():
        for entry in registry.iterdir():
            _confined(root, entry.relative_to(root).as_posix())
    paths = [root / "hooks/hooks.json", *scripts.glob("*.py")]
    paths.extend(registry.glob("*/task_registry.json"))
    result = {}
    for path in paths:
        relative = path.relative_to(root).as_posix()
        checked = _confined(root, relative)
        if not checked.is_file():
            raise NativeHookError("A required native hook source is missing")
        result[relative] = _digest(checked.read_bytes())
    required = {
        "hooks/hooks.json",
        "hooks/scripts/hook_utils.py",
        *EVENT_SCRIPTS.values(),
    }
    if not required.issubset(result):
        raise NativeHookError(
            "The release does not contain the complete native hook set"
        )
    # A sourceless module could otherwise shadow a standard-library import.
    if list(scripts.glob("*.pyc")) or list(scripts.glob("*.so")):
        raise NativeHookError(
            "Unexpected executable files in the native hook directory"
        )
    return result


class NativeHookDispatcher:
    """Dispatch fixed lifecycle events while retaining original policy semantics.

    The source_root must already be authenticated by the caller's release
    mechanism. This class pins its relevant bytes and detects subsequent drift;
    accepting a caller-controlled source directory would not authenticate code.
    The caller also owns the trust decision for payload fields such as controlled.
    """

    def __init__(self, *, source_root: Path, workspace: Path, timeout_seconds=10):
        if source_root.is_symlink() or workspace.is_symlink():
            raise NativeHookError("Native hook roots cannot be symlinks")
        self.source_root = source_root.resolve(strict=True)
        self.workspace = workspace.resolve(strict=True)
        if self.workspace == self.source_root:
            raise NativeHookError("Native hooks require a separate writable workspace")
        if not 0 < timeout_seconds <= 30:
            raise NativeHookError("Hook timeout must be in (0, 30] seconds")
        self.timeout_seconds = timeout_seconds
        self._sources = _source_files(self.source_root)
        self.source_digest = _digest(_json_bytes(self._sources))
        configuration = json.loads((self.source_root / "hooks/hooks.json").read_text())
        expected = [
            {"event": event, "script": script}
            for event, script in EVENT_SCRIPTS.items()
        ]
        if configuration.get("version") != 1 or configuration.get("hooks") != expected:
            raise NativeHookError(
                "Native hook configuration differs from the supported event contract"
            )
        self._validate_sources()

    def _validate_sources(self):
        if (
            _source_files(self.source_root) != self._sources
            or _source_files(self.workspace) != self._sources
        ):
            raise NativeHookError(
                "Native hook sources or membership registry drifted from the release"
            )

    @contextmanager
    def _journal(self):
        """Serialize same-workspace hook calls without altering native trace rules."""
        path = _confined(self.workspace, JOURNAL)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and (not path.is_file() or path.stat().st_nlink != 1):
            raise NativeHookError("Hook journal must be an unlinked regular file")
        descriptor = os.open(
            path, os.O_CREAT | os.O_APPEND | os.O_WRONLY | os.O_NOFOLLOW, 0o600
        )
        with os.fdopen(descriptor, "ab") as stream:
            if (
                not stat.S_ISREG(os.fstat(stream.fileno()).st_mode)
                or os.fstat(stream.fileno()).st_nlink != 1
            ):
                raise NativeHookError("Invalid hook journal file")
            fcntl.flock(stream, fcntl.LOCK_EX)
            try:
                yield stream
            finally:
                fcntl.flock(stream, fcntl.LOCK_UN)

    def dispatch(self, event: str, payload: dict) -> HookReceipt:
        """Execute the original handler and return its exact accept/warn/block."""
        if event not in EVENT_SCRIPTS or not isinstance(payload, dict):
            raise NativeHookError(
                "Expected a supported native event and object payload"
            )
        try:
            encoded = _json_bytes(payload)
            frozen = json.loads(encoded)
        except (TypeError, ValueError) as exc:
            raise NativeHookError("Hook payload must be finite JSON") from exc
        if len(encoded) > MAX_PAYLOAD_BYTES:
            raise NativeHookError("Hook payload exceeds the bounded input size")
        paths = frozen.get("expected_artifacts", [])
        if not isinstance(paths, list) or not all(
            isinstance(path, str) for path in paths
        ):
            raise NativeHookError("expected_artifacts must be a list of relative paths")
        for path in paths:
            _confined(self.workspace, path)
        if frozen.get("path"):
            _confined(self.workspace, frozen["path"])
        script = EVENT_SCRIPTS[event]
        trace = f"agentic/traces/hook_runs/latest-{Path(script).stem}.json"
        with self._journal() as journal:
            self._validate_sources()
            trace_path = _confined(self.workspace, trace)
            if trace_path.exists() and (
                not trace_path.is_file() or trace_path.stat().st_nlink != 1
            ):
                raise NativeHookError("Native trace must be an unlinked regular file")
            # An empty cache prefix prevents stale workspace pyc files from
            # overriding the hashed source. -B also prevents new bytecode writes.
            with tempfile.TemporaryDirectory(prefix="abducer-hook-cache-") as cache:
                try:
                    completed = subprocess.run(
                        [
                            sys.executable,
                            "-B",
                            "-S",
                            "-E",
                            "-X",
                            f"pycache_prefix={cache}",
                            str(self.workspace / script),
                        ],
                        input=encoded,
                        capture_output=True,
                        cwd=self.workspace,
                        env={"PATH": os.defpath, "LANG": "C.UTF-8"},
                        timeout=self.timeout_seconds,
                        check=False,
                    )
                except (OSError, subprocess.TimeoutExpired) as exc:
                    raise NativeHookError(
                        "Native hook execution failed or timed out"
                    ) from exc
            if completed.returncode != 0 or len(completed.stdout) > MAX_PAYLOAD_BYTES:
                raise NativeHookError(
                    "Native hook exited unsuccessfully or returned oversized output"
                )
            try:
                result = json.loads(completed.stdout)
            except (ValueError, UnicodeDecodeError) as exc:
                raise NativeHookError(
                    "Native hook did not return a JSON decision"
                ) from exc
            if (
                not isinstance(result, dict)
                or result.get("decision") not in {"accept", "warn", "block"}
                or not isinstance(result.get("reason"), str)
                or not result["reason"]
            ):
                raise NativeHookError("Native hook returned an invalid decision")
            self._validate_sources()
            trace_path = _confined(self.workspace, trace)
            try:
                trace_bytes = trace_path.read_bytes()
                expected_trace = {
                    "hook": Path(script).stem,
                    "payload": frozen,
                    "result": result,
                }
                if (
                    len(trace_bytes) > MAX_PAYLOAD_BYTES * 3
                    or json.loads(trace_bytes) != expected_trace
                ):
                    raise NativeHookError(
                        "Native hook trace differs from its invocation"
                    )
            except OSError as exc:
                raise NativeHookError(
                    "Native hook did not produce its original trace"
                ) from exc
            receipt = HookReceipt(
                event,
                script,
                self.source_digest,
                _digest(encoded),
                result,
                trace,
                _digest(trace_bytes),
            )
            journal.write(
                _json_bytes({"schema_version": 1, **receipt.as_dict()}) + b"\n"
            )
            journal.flush()
            os.fsync(journal.fileno())
            return receipt

    def require(self, event: str, payload: dict) -> HookReceipt:
        """Allow warnings, and stop the caller before an action rejected by policy."""
        receipt = self.dispatch(event, payload)
        if not receipt.allowed:
            raise NativeHookBlocked(receipt)
        return receipt
