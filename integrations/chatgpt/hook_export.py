# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Export the original hook policies and their exact membership dependencies.

The bundle is a portable input to an explicitly wired native executor. It is not
a host hook registration or a complete Abducer workflow installation. Original
scripts and the existing dispatcher are copied byte for byte; the contract
explains where callers must enforce their decisions. The manifest detects drift,
while an independently trusted release digest must establish authenticity.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat

from integrations.chatgpt.native_hooks import EVENT_SCRIPTS, _source_files

PREFIX = Path("native-hook-runtime")
DISPATCHER = "integrations/chatgpt/native_hooks.py"
MAX_FILES = 128
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_BUNDLE_BYTES = 8 * 1024 * 1024
STOP_ARTIFACTS = [
    "agentic/state/current_target.json",
    "agentic/state/dependency_frontier.json",
    "agentic/reports/compliance/latest.md",
    "agentic/reports/drift/latest.md",
    "agentic/todos/looper_integration_todos.yaml",
]


class HookExportError(ValueError):
    """The bundle cannot preserve the bounded, declared native hook contract."""


def _encoded(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _source_digest(sources: dict[str, str]) -> str:
    """Match the existing dispatcher's release digest without changing its format."""
    return _digest(json.dumps(sources, sort_keys=True, allow_nan=False).encode())


def _path(root: Path, relative: str) -> Path:
    """Validate every path before reading; never follow a bundled symlink."""
    if (
        not isinstance(relative, str)
        or not relative
        or "\\" in relative
        or PurePosixPath(relative).is_absolute()
        or any(part in {"", ".", ".."} for part in relative.split("/"))
    ):
        raise HookExportError("Bundle paths must be canonical relative paths")
    path = root / relative
    for candidate in (path, *path.parents):
        if candidate == root:
            break
        if candidate.is_symlink():
            raise HookExportError("Bundle paths cannot contain symlinks")
    return path


def _read(root: Path, relative: str) -> bytes:
    """Bound reads and reject nonregular files before opening their contents."""
    path = _path(root, relative)
    try:
        metadata = path.stat()
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_FILE_BYTES:
            raise HookExportError("Bundle files must be bounded regular files")
        with path.open("rb") as stream:
            data = stream.read(MAX_FILE_BYTES + 1)
    except OSError as exc:
        raise HookExportError(f"Cannot read required bundle file: {relative}") from exc
    if len(data) > MAX_FILE_BYTES:
        raise HookExportError("Bundle file exceeds the size limit")
    return data


def _configuration(data: bytes) -> None:
    """Fail generation if canonical wiring changed without adapter support."""
    configuration = json.loads(data)
    expected = [
        {"event": event, "script": script} for event, script in EVENT_SCRIPTS.items()
    ]
    if configuration.get("version") != 1 or configuration.get("hooks") != expected:
        raise HookExportError(
            "Native hook configuration differs from the event contract"
        )


def _contract(sources: dict[str, str]) -> dict:
    """Describe native semantics, including warnings that must remain nonblocking."""
    behavior = {
        "UserPromptSubmit": {
            "payload_fields": ["prompt"],
            "decisions": ["accept", "warn"],
            "meaning": "Suggest controlled-goal enrichment for native prompt markers.",
        },
        "PreSkillUse": {
            "payload_fields": ["skill", "controlled"],
            "decisions": ["accept", "block"],
            "meaning": "Check skill membership in the union of visible native workflows; "
            "this does not validate workflow activation, step order or completion.",
        },
        "PostSkillUse": {
            "payload_fields": ["expected_artifacts"],
            "decisions": ["accept", "warn"],
            "meaning": "Warn when declared artifacts do not exist; no content validation.",
        },
        "PreToolUse": {
            "payload_fields": ["command", "path", "evidence"],
            "decisions": ["accept", "warn", "block"],
            "meaning": "Apply native destructive-command markers and protected-path "
            "evidence checks to caller-supplied fields; this is not a shell sandbox.",
        },
        "Stop": {
            "payload_fields": ["controlled"],
            "decisions": ["accept", "block"],
            "meaning": "Require the original five Looper artifact paths for controlled "
            "runs; existence does not certify scientific validity or fresh evidence.",
        },
    }
    return {
        "schema_version": 1,
        "kind": "abducer-native-hook-contract",
        "source_digest": _source_digest(sources),
        "configuration": "source/hooks/hooks.json",
        "events": [
            {"event": event, "script": script, **behavior[event]}
            for event, script in EVENT_SCRIPTS.items()
        ],
        "membership": {
            "namespace": "registry/tasks",
            "pattern": "registry/tasks/*/task_registry.json",
            "field": "visible_workflows[].composed_skills[]",
            "files": sorted(path for path in sources if path.startswith("registry/")),
        },
        "dispatcher": {
            "path": "runner/native_hooks.py",
            "class": "NativeHookDispatcher",
            "enforcing_method": "require(event, payload)",
            "inspection_method": "dispatch(event, payload)",
            "decision_semantics": {
                "accept": "Continue.",
                "warn": "Continue and retain the warning in the receipt.",
                "block": "require raises NativeHookBlocked even when the script exits 0.",
                "execution_error": "Raise NativeHookError; no successful decision.",
            },
        },
        "requirements": {
            "runtime": "Python 3.10+ on POSIX with fcntl; the dispatcher and five "
            "registered events use the standard library only",
            "trusted_source_root": "source/ verified against a trusted release digest",
            "writable_workspace": "A separate workspace with identical native hook and "
            "registry bytes, plus the workflow's own artifacts and dependencies.",
            "caller": "Explicitly invoke lifecycle events, supply trusted payload "
            "fields, and enforce require before gated actions or completion.",
            "controlled_default": True,
            "stop_artifacts": STOP_ARTIFACTS,
        },
        "trace_behavior": {
            "native": "agentic/traces/hook_runs/latest-<script-stem>.json",
            "receipts": "agentic/traces/hosted_native_hooks/events.jsonl",
            "location": "Writable workspace only; no prior traces are exported.",
        },
        "scope": {
            "host_hook_registration": False,
            "automatic_chatgpt_hooks": False,
            "workflow_engine_included": False,
            "all_workflow_execution_parity": False,
            "note": "PreSkillUse and PostSkillUse are Abducer executor events. "
            "The native list-form configuration is not a ChatGPT host hook manifest.",
            "host_payload_translation": "A future host adapter must map tool_input.command "
            "to command and native JSON decisions to the host's event-specific output. "
            "Passing host payloads directly does not preserve policy behavior.",
            "current_executor_limits": "The current hosted Marathon adapter supplies a "
            "synthesized intake prompt; errors and cancellation can skip finish-time "
            "PostSkillUse and Stop. Packaging does not repair lifecycle coverage.",
        },
        "unregistered_scripts": {
            "files": sorted(
                path
                for path in sources
                if path.startswith("hooks/scripts/")
                and path not in {*EVENT_SCRIPTS.values(), "hooks/scripts/hook_utils.py"}
            ),
            "status": "Preserved for exact dispatcher source parity; not registered or "
            "activated. COHERE helpers require PyYAML and external domain/workflow "
            "registries that this hook-only bundle does not include.",
        },
        "excluded": [
            "hooks/workflow_local/",
            "registry/optional-tasks/",
            "research state, reports, traces, private settings and credentials",
        ],
    }


def _readme() -> bytes:
    """Keep setup and limits with the export so extraction retains its meaning."""
    return b"""# Native Abducer hook bundle

This bundle preserves the original five registered lifecycle checks, their shared
helper, and the exact `registry/tasks` membership files. Scripts keep their bytes
and original workspace-relative paths. The existing dispatcher is included as
`runner/native_hooks.py`; `hook-contract.json` describes its decision semantics.
The manifest binds every included file and the native source digest.

## Use from an executor

1. Authenticate the package and its expected bundle digest through your release
   channel. In the Abducer checkout, call
   `integrations.chatgpt.hook_export.validate_bundle(bundle_root, expected_digest=...)`
   before importing the exported runner. A self-consistent manifest is not proof
   of who supplied the code.
2. Keep `source/` immutable. Create a separate writable research workspace containing
   identical hook/registry files and the original workflow's own dependencies and
   state. Python 3.10+ with POSIX `fcntl` is required for the dispatcher.
3. Import `NativeHookDispatcher` from the exported runner, construct it with
   `source_root=<bundle>/source` and `workspace=<research-workspace>`, and explicitly
   call `require(event, payload)` at the appropriate executor boundaries.

For example, `require("PreToolUse", {"command": "rm -rf scratch"})` raises
`NativeHookBlocked` even though the original script exits successfully. A missing
artifact in `require("PostSkillUse", {"expected_artifacts": ["missing.json"]})`
retains the original warning and permits continuation. `dispatch(...)` returns a
receipt for inspection; the caller must enforce it or use `require(...)`.

`PreSkillUse` checks the union of `visible_workflows[].composed_skills[]` from the
native task registry. It does not enforce step order or workflow activation.
Controlled `Stop` requires the five original Looper artifact paths documented in
the contract. Presence of those files is not scientific validation. The executor
owns trusted `controlled`, skill, command and artifact payload values.

Native latest traces and the append-only receipt journal are written only in the
writable workspace. No existing research state, credentials or traces are copied.
Optional `hooks/workflow_local` and `registry/optional-tasks` remain excluded.
Two unregistered COHERE scripts are preserved for native source-digest parity.
They are not activated: their PyYAML and external registry dependencies are not
part of this hook-only bundle.

## Host and workflow boundaries

This is not a ChatGPT host hook manifest or a complete workflow installation.
The native list-form `hooks.json` and its `PreSkillUse`/`PostSkillUse` events must
not be installed directly as host hooks. An explicit host adapter would need to
translate `tool_input.command` into native `command`, map native decisions to
event-specific host responses, and handle host availability and trust review.
There is no automatic personal online ChatGPT hook registration in this package.

The current hosted Marathon adapter supplies a synthesized intake prompt. Error
and cancellation exits can omit finish-time `PostSkillUse` and `Stop` calls. Source
preservation does not establish all-exit coverage or execution parity across all
workflows; use runtime capability evidence for the actual deployment.
"""


def outputs(root: Path) -> dict[Path, bytes]:
    """Return deterministic plugin-relative files, without mutating source or disk."""
    if root.is_symlink():
        raise HookExportError("Source root cannot be a symlink")
    root = root.resolve(strict=True)
    sources = _source_files(root)
    if len(sources) + 4 > MAX_FILES:
        raise HookExportError("Too many native hook bundle files")
    files = {
        f"source/{relative}": _read(root, relative) for relative in sorted(sources)
    }
    # A concurrent edit must not produce a manifest for different executable bytes.
    if any(_digest(files[f"source/{path}"]) != sha for path, sha in sources.items()):
        raise HookExportError("Native sources changed during export")
    _configuration(files["source/hooks/hooks.json"])
    files["runner/native_hooks.py"] = _read(root, DISPATCHER)
    files["hook-contract.json"] = _encoded(_contract(sources))
    files["README.md"] = _readme()
    if sum(len(data) for data in files.values()) > MAX_BUNDLE_BYTES:
        raise HookExportError("Native hook bundle exceeds the size limit")
    manifest = {
        "schema_version": 1,
        "kind": "abducer-native-hook-bundle",
        "source_digest": _source_digest(sources),
        "files": {
            path: {"sha256": _digest(data), "bytes": len(data)}
            for path, data in sorted(files.items())
        },
    }
    manifest["bundle_digest"] = _digest(_encoded(manifest))
    files["manifest.json"] = _encoded(manifest)
    return {PREFIX / path: data for path, data in sorted(files.items())}


def validate_bundle(bundle_root: Path, *, expected_digest: str | None = None) -> dict:
    """Verify an extracted bundle without importing or running its executable code.

    ``bundle_root`` is the exported ``native-hook-runtime`` directory. Pass the
    digest from an independently authenticated release to bind the check to that
    release; an internally consistent manifest alone does not authenticate code.
    """
    if bundle_root.is_symlink():
        raise HookExportError("Bundle root cannot be a symlink")
    root = bundle_root.resolve(strict=True)
    manifest = json.loads(_read(root, "manifest.json"))
    if (
        not isinstance(manifest, dict)
        or manifest.get("schema_version") != 1
        or manifest.get("kind") != "abducer-native-hook-bundle"
        or not isinstance(manifest.get("files"), dict)
        or not 1 <= len(manifest["files"]) < MAX_FILES
    ):
        raise HookExportError("Invalid native hook bundle manifest")
    digest = manifest.get("bundle_digest")
    body = {key: value for key, value in manifest.items() if key != "bundle_digest"}
    if digest != _digest(_encoded(body)) or (
        expected_digest is not None and digest != expected_digest
    ):
        raise HookExportError("Native hook bundle digest does not match the release")

    # Validate the complete tree, not only declared files: extra modules could
    # otherwise shadow imports, and extra research artifacts could leak state.
    found = set()
    directories = 0
    for parent, names, filenames in os.walk(root, followlinks=False):
        directories += len(names)
        if directories > MAX_FILES:
            raise HookExportError("Too many directories in native hook bundle")
        for name in [*names, *filenames]:
            _path(root, (Path(parent) / name).relative_to(root).as_posix())
        found.update(
            (Path(parent) / name).relative_to(root).as_posix() for name in filenames
        )
        if len(found) > MAX_FILES:
            raise HookExportError("Too many files in native hook bundle")
    if found != {*manifest["files"], "manifest.json"}:
        raise HookExportError("Native hook bundle inventory differs from its manifest")
    files = {}
    size = 0
    for relative, record in manifest["files"].items():
        data = _read(root, relative)
        size += len(data)
        if size > MAX_BUNDLE_BYTES:
            raise HookExportError("Native hook bundle exceeds the size limit")
        if record != {"sha256": _digest(data), "bytes": len(data)}:
            raise HookExportError(f"Native hook bundle file drifted: {relative}")
        files[relative] = data
    sources = _source_files(root / "source")
    expected = {f"source/{path}" for path in sources} | {
        "runner/native_hooks.py",
        "hook-contract.json",
        "README.md",
    }
    if set(files) != expected or manifest.get("source_digest") != _source_digest(
        sources
    ):
        raise HookExportError("Native hook source inventory or digest differs")
    _configuration(files["source/hooks/hooks.json"])
    if files["hook-contract.json"] != _encoded(_contract(sources)):
        raise HookExportError("Native hook contract differs from supported semantics")
    return manifest
