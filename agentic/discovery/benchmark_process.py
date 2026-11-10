# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Govern and attest JSON subprocesses used by the live benchmark.

Scientific evaluation remains in :mod:`agentic.discovery.benchmark`.  This
module owns the narrower operational trust chain: an output-row summary opens
an immutable full receipt, the receipt is a member of one immutable role index,
and those records bind the exact request, explicitly observed executable/script
bytes, attempt-local workspace, budget, measured accounting, and response bytes.
The chain records one trusted-parent local launch/exit correlation; it is not
transitive executable attestation and deliberately does *not* turn a local
verifier into external-human evidence or give an operational outcome epistemic
authority.
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence

from .benchmark import BenchmarkIntegrityError, RUNNER_EXECUTION_KEY, VERIFIER_EXECUTION_KEY
from .budgets import (
    BudgetExceeded,
    ResourceBudget,
    ResourceGovernor,
    complete_governed_process_environment,
    contained_path,
    minimal_replacement_environment,
    validate_job_id,
    validate_v2_process_event,
)
from .contracts import (
    bytes_digest,
    canonical_digest,
    canonical_json,
    file_digest,
    fsync_directory,
    stable_identifier,
    utc_now,
    validate_payload,
)


SUMMARY_SCHEMA = "benchmark_external_process_summary.schema.json"
RECEIPT_SCHEMA = "benchmark_external_process_receipt.schema.json"
INDEX_SCHEMA = "benchmark_external_process_index.schema.json"
EPistemic_NULL = "none_process_execution_has_no_epistemic_authority"


class ExternalBenchmarkProcessError(BenchmarkIntegrityError):
    """An operational/protocol failure with a persisted receipt summary."""

    def __init__(self, message: str, receipt: Mapping[str, Any]) -> None:
        self.receipt = dict(receipt)
        super().__init__(message)


class ExternalProcessValidationContext:
    """One evaluation's exact index and live-authority replay cache.

    The context starts empty and is never serialized or shared globally.  A
    cached index is identified by canonical path, declared content digest, and
    current file digest; its value retains every exact validated summary and
    full receipt.  Thus warm lookup can remove repeated transitive replay
    without turning a receipt ID or prior boolean result into authority.
    """

    def __init__(self) -> None:
        self._indices: dict[str, dict[str, Any]] = {}
        self._live_authorities: dict[str, dict[str, Any]] = {}
        self._file_snapshots: dict[str, dict[str, Any]] = {}
        self._finalized = False
        self._counts = {
            "index_replays": 0,
            "receipt_replays": 0,
            "authority_replays": 0,
            "index_cache_hits": 0,
            "receipt_cache_hits": 0,
            "final_index_checks": 0,
            "final_receipt_checks": 0,
            "final_authority_checks": 0,
        }

    @property
    def replay_counts(self) -> dict[str, int]:
        """Return a detached audit of cold replay, warm lookup, and final checks."""

        return dict(self._counts)

    @staticmethod
    def _stat_token(path: Path) -> tuple[int, int, int, int, int]:
        try:
            metadata = path.lstat()
        except OSError as exc:
            raise BenchmarkIntegrityError(
                f"benchmark authority became unavailable: {path}"
            ) from exc
        if path.is_symlink() or not stat.S_ISREG(metadata.st_mode):
            raise BenchmarkIntegrityError(
                f"benchmark authority is no longer a regular file: {path}"
            )
        return (
            int(metadata.st_dev),
            int(metadata.st_ino),
            int(metadata.st_size),
            int(metadata.st_mtime_ns),
            int(metadata.st_ctime_ns),
        )

    def _record_file(
        self, path: Path, *, kind: str, known_digest: str
    ) -> None:
        canonical = str(path.resolve(strict=True))
        snapshot = {
            "path": canonical,
            "kind": kind,
            "stat_token": self._stat_token(path),
            "sha256": known_digest,
        }
        prior = self._file_snapshots.get(canonical)
        if prior is not None and prior != snapshot:
            raise BenchmarkIntegrityError(
                f"benchmark authority changed while being recorded: {path}"
            )
        self._file_snapshots[canonical] = snapshot

    def _require_metadata_unchanged(self, path: Path) -> None:
        canonical = str(path.resolve(strict=True))
        snapshot = self._file_snapshots.get(canonical)
        if snapshot is None:
            raise BenchmarkIntegrityError(
                f"benchmark authority was not replayed in this context: {path}"
            )
        if self._stat_token(path) != snapshot["stat_token"]:
            raise BenchmarkIntegrityError(
                f"benchmark authority changed after replay: {path}"
            )

    def require_live_authority(self, authority: Mapping[str, Any]) -> None:
        authority_digest = str(authority.get("content_digest") or "")
        cached = self._live_authorities.get(authority_digest)
        if cached is not None:
            if cached != dict(authority):
                raise BenchmarkIntegrityError(
                    "one command authority digest names different authority objects"
                )
            return
        _require_live_command_authority(authority)
        self._live_authorities[authority_digest] = copy.deepcopy(dict(authority))
        self._counts["authority_replays"] += 1

    def _get_or_replay(
        self,
        index_path: Path,
        supplied_index: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        if self._finalized:
            raise BenchmarkIntegrityError("benchmark validation context is finalized")
        if index_path.is_symlink() or not index_path.is_file():
            raise BenchmarkIntegrityError(
                "external benchmark process index is unavailable or linked"
            )
        canonical_path = str(index_path.resolve(strict=True))
        cached = self._indices.get(canonical_path)
        if cached is not None:
            self._require_metadata_unchanged(index_path)
            if supplied_index is not None and dict(supplied_index) != cached["index"]:
                raise BenchmarkIntegrityError(
                    "supplied benchmark index differs from the replayed immutable index"
                )
            self._counts["index_cache_hits"] += 1
            return cached

        index = (
            copy.deepcopy(dict(supplied_index))
            if supplied_index is not None
            else _load_json_object(index_path)
        )
        before_digest = file_digest(index_path)
        if bytes_digest(canonical_json(index) + b"\n") != before_digest:
            raise BenchmarkIntegrityError(
                "external benchmark process index bytes are noncanonical or changed during load"
            )
        replay = _replay_index(index, index_path, validation_context=self)
        after_digest = file_digest(index_path)
        if after_digest != before_digest:
            raise BenchmarkIntegrityError(
                "external benchmark process index changed during replay"
            )
        self._record_file(index_path, kind="index", known_digest=after_digest)
        for record in replay["receipt_records"].values():
            summary = record["summary"]
            receipt_path = _contained_relative(
                Path(summary["run_directory"]), summary["receipt_ref"]
            )
            self._record_file(
                receipt_path,
                kind="receipt",
                known_digest=summary["receipt_file_sha256"],
            )
        cached = copy.deepcopy(replay)
        self._indices[canonical_path] = cached
        self._counts["index_replays"] += 1
        return cached

    def replay_index(
        self, index: Mapping[str, Any], index_path: Path
    ) -> dict[str, Any]:
        """Replay a supplied index while never exposing the mutable cache value."""

        return copy.deepcopy(self._get_or_replay(index_path, index))

    def replay_index_path(self, index_path: Path) -> dict[str, Any]:
        """Replay an index directly from disk, loading it only on the cold path."""

        return copy.deepcopy(self._get_or_replay(index_path))

    def receipt_for_summary(
        self, summary: Mapping[str, Any], index_path: Path
    ) -> dict[str, Any]:
        """Return one detached receipt after constant-time warm membership checks."""

        replay = self._get_or_replay(index_path)
        record = replay["receipt_records"].get(str(summary["receipt_id"]))
        if record is None or record["summary"] != dict(summary):
            raise BenchmarkIntegrityError(
                "external process summary lacks exact index membership"
            )
        receipt_path = _contained_relative(
            Path(summary["run_directory"]), str(summary["receipt_ref"])
        )
        self._require_metadata_unchanged(receipt_path)
        self._counts["receipt_cache_hits"] += 1
        return copy.deepcopy(record["receipt"])

    def assert_unchanged(self) -> None:
        """Perform one linear byte-exact drift sweep over all replayed authority.

        Warm membership checks intentionally avoid rehashing an O(n)-sized index
        for each of its n summaries.  This terminal sweep closes the resulting
        time-of-check window exactly once, keeping total validation O(n).
        """

        if self._finalized:
            return
        for canonical in sorted(self._file_snapshots):
            snapshot = self._file_snapshots[canonical]
            path = Path(canonical)
            self._require_metadata_unchanged(path)
            if file_digest(path) != snapshot["sha256"]:
                raise BenchmarkIntegrityError(
                    f"benchmark authority bytes changed after replay: {path}"
                )
            counter = (
                "final_index_checks"
                if snapshot["kind"] == "index"
                else "final_receipt_checks"
            )
            self._counts[counter] += 1
        for authority in self._live_authorities.values():
            _require_live_command_authority(authority)
            self._counts["final_authority_checks"] += 1
        self._finalized = True


def _write_immutable_bytes(path: Path, encoded: bytes) -> None:
    """Publish exact bytes with fsync + hard-link create-if-absent semantics.

    A crash can leave only an unreferenced temporary file; it cannot expose a
    partially written receipt or index at the authoritative name.  Repeating an
    exact invocation accepts byte-identical prior publication and rejects every
    conflicting byte sequence.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            if path.is_symlink() or not path.is_file() or path.read_bytes() != encoded:
                raise BenchmarkIntegrityError(
                    f"immutable benchmark process conflict: {path}"
                )
        else:
            fsync_directory(path.parent)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def _write_immutable_json(path: Path, payload: Mapping[str, Any]) -> None:
    _write_immutable_bytes(path, canonical_json(payload) + b"\n")


def _load_json_object(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise BenchmarkIntegrityError(f"benchmark authority is not a regular file: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BenchmarkIntegrityError(f"cannot read benchmark authority {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise BenchmarkIntegrityError(f"benchmark authority must be an object: {path}")
    return payload


def _contained_relative(root: Path, reference: str) -> Path:
    relative = Path(reference)
    if relative.is_absolute() or not relative.parts or any(
        part in {"", ".", ".."} for part in relative.parts
    ):
        raise BenchmarkIntegrityError(f"unsafe benchmark authority reference: {reference!r}")
    try:
        return contained_path(root, *relative.parts)
    except ValueError as exc:
        raise BenchmarkIntegrityError(str(exc)) from exc


def _descriptor(path: Path, *, source: str, argv_indexes: Sequence[int], executable: bool) -> dict[str, Any]:
    resolved = path.resolve(strict=True)
    if not resolved.is_file() or resolved.is_symlink():
        raise BenchmarkIntegrityError(f"command dependency is not a regular file: {path}")
    if executable and not os.access(resolved, os.X_OK):
        raise BenchmarkIntegrityError(f"command executable is not executable: {resolved}")
    return {
        "canonical_path": str(resolved),
        "sha256": file_digest(resolved),
        "byte_length": resolved.stat().st_size,
        "source": source,
        "argv_indexes": sorted(set(int(item) for item in argv_indexes)),
        "executable": executable,
    }


def _resolve_executable(raw: str) -> Path:
    candidate: str | None
    if Path(raw).is_absolute() or os.sep in raw or (os.altsep and os.altsep in raw):
        candidate = str(Path(raw).expanduser().resolve())
    else:
        candidate = shutil.which(raw)
    if not candidate:
        raise BenchmarkIntegrityError(f"external benchmark executable is unavailable: {raw!r}")
    return Path(candidate)


def _seal_command(
    command: Sequence[str], approved_dependency_paths: Sequence[Path | str]
) -> tuple[tuple[str, ...], dict[str, Any]]:
    """Resolve argv ambiguity and seal every explicit executable/script input.

    Existing regular-file argv entries are treated as semantic dependencies,
    including an interpreter's script.  Callers may add imported modules or
    other non-argv authority through ``approved_dependency_paths``.  This is a
    local byte pin, not an externally trusted identity or human attestation.
    """

    resolved_argv = list(command)
    executable = _resolve_executable(resolved_argv[0]).resolve(strict=True)
    resolved_argv[0] = str(executable)
    executable_descriptor = _descriptor(
        executable, source="executable", argv_indexes=[0], executable=True
    )

    dependencies: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(resolved_argv[1:], start=1):
        candidate = Path(raw).expanduser()
        if not candidate.is_absolute():
            candidate = Path.cwd() / candidate
        try:
            is_file = candidate.is_file()
        except OSError:
            is_file = False
        if not is_file:
            continue
        resolved = candidate.resolve(strict=True)
        resolved_argv[index] = str(resolved)
        dependencies[str(resolved)] = _descriptor(
            resolved, source="argv", argv_indexes=[index], executable=False
        )
    for raw in approved_dependency_paths:
        resolved = Path(raw).expanduser().resolve(strict=True)
        existing = dependencies.get(str(resolved))
        indexes = existing.get("argv_indexes", []) if existing else []
        dependencies[str(resolved)] = _descriptor(
            resolved,
            source="argv+approved" if existing else "approved",
            argv_indexes=indexes,
            executable=False,
        )
    authority: dict[str, Any] = {
        "schema_version": 1,
        "argv": resolved_argv,
        "argv_digest": canonical_digest(resolved_argv),
        "executable": executable_descriptor,
        "dependencies": [dependencies[key] for key in sorted(dependencies)],
        "trust_boundary": "local_exact_dependency_identity_not_external_human_authority",
    }
    authority["content_digest"] = canonical_digest(authority)
    return tuple(resolved_argv), authority


def _top_level_content_digest(payload: Mapping[str, Any]) -> str:
    """Hash an object without erasing nested authority digests."""

    return canonical_digest(
        {key: value for key, value in payload.items() if key != "content_digest"}
    )


def _validate_command_authority_structure(authority: Mapping[str, Any]) -> None:
    """Validate sealed metadata without consulting mutable live files."""

    if authority.get("content_digest") != _top_level_content_digest(authority):
        raise BenchmarkIntegrityError("command authority digest mismatch")
    argv = authority.get("argv")
    if not isinstance(argv, list) or authority.get("argv_digest") != canonical_digest(argv):
        raise BenchmarkIntegrityError("command authority argv digest mismatch")
    executable = authority.get("executable")
    dependencies = authority.get("dependencies")
    if not isinstance(executable, Mapping) or not isinstance(dependencies, list):
        raise BenchmarkIntegrityError("command authority dependency shape is invalid")
    if (
        executable.get("canonical_path") != argv[0]
        or executable.get("source") != "executable"
        or executable.get("argv_indexes") != [0]
        or executable.get("executable") is not True
    ):
        raise BenchmarkIntegrityError("command executable descriptor is not bound to argv[0]")
    seen: set[str] = set()
    for row in dependencies:
        if not isinstance(row, Mapping):
            raise BenchmarkIntegrityError("command authority dependency is malformed")
        path = str(row.get("canonical_path") or "")
        if not path or path in seen:
            raise BenchmarkIntegrityError("command authority dependency paths are not unique")
        seen.add(path)
        indexes = row.get("argv_indexes")
        if not isinstance(indexes, list) or any(
            index <= 0 or index >= len(argv) or argv[index] != path for index in indexes
        ):
            raise BenchmarkIntegrityError("command dependency argv binding is invalid")
        source = row.get("source")
        if (
            (indexes and source not in {"argv", "argv+approved"})
            or (not indexes and source != "approved")
            or row.get("executable") is not False
        ):
            raise BenchmarkIntegrityError("command dependency descriptor role is invalid")
    if [row["canonical_path"] for row in dependencies] != sorted(seen):
        raise BenchmarkIntegrityError("command authority dependencies are not canonically ordered")


def _observe_file_descriptor(descriptor: Mapping[str, Any]) -> dict[str, Any]:
    """Retain expected and observed bytes even when the command has mutated."""

    path = Path(str(descriptor["canonical_path"]))
    observed_path: str | None = None
    observed_sha256: str | None = None
    observed_byte_length: int | None = None
    observed_executable: bool | None = None
    status = "unavailable"
    try:
        if path.is_symlink():
            status = "symlink"
            try:
                observed_path = str(path.resolve(strict=True))
            except (OSError, RuntimeError):
                observed_path = None
        elif not path.exists():
            status = "missing"
        elif not path.is_file():
            status = "not_regular"
            observed_path = str(path.resolve(strict=True))
        else:
            resolved = path.resolve(strict=True)
            observed_path = str(resolved)
            observed_byte_length = resolved.stat().st_size
            observed_sha256 = file_digest(resolved)
            observed_executable = os.access(resolved, os.X_OK)
            if observed_path != str(path):
                status = "path_mismatch"
            elif (
                observed_byte_length != descriptor["byte_length"]
                or observed_sha256 != descriptor["sha256"]
            ):
                status = "bytes_mismatch"
            elif descriptor["executable"] is True and not observed_executable:
                status = "permission_mismatch"
            else:
                status = "matched"
    except (OSError, RuntimeError):
        status = "unavailable"
    return {
        "canonical_path": str(path),
        "expected_sha256": descriptor["sha256"],
        "expected_byte_length": descriptor["byte_length"],
        "expected_executable": descriptor["executable"],
        "observed_status": status,
        "observed_canonical_path": observed_path,
        "observed_sha256": observed_sha256,
        "observed_byte_length": observed_byte_length,
        "observed_executable": observed_executable,
    }


def _observe_command_authority(authority: Mapping[str, Any]) -> dict[str, Any]:
    _validate_command_authority_structure(authority)
    entries = [_observe_file_descriptor(authority["executable"])] + [
        _observe_file_descriptor(row) for row in authority["dependencies"]
    ]
    observation: dict[str, Any] = {
        "schema_version": 1,
        "status": (
            "exact_match"
            if all(row["observed_status"] == "matched" for row in entries)
            else "mismatch"
        ),
        "expected_authority_digest": authority["content_digest"],
        "entries": entries,
    }
    observation["content_digest"] = canonical_digest(observation)
    return observation


def _validate_command_authority_observation(
    authority: Mapping[str, Any], observation: Mapping[str, Any]
) -> None:
    if observation.get("content_digest") != _top_level_content_digest(observation):
        raise BenchmarkIntegrityError("command authority observation digest mismatch")
    if observation.get("expected_authority_digest") != authority["content_digest"]:
        raise BenchmarkIntegrityError("command authority observation targets another authority")
    descriptors = [authority["executable"], *authority["dependencies"]]
    entries = observation.get("entries")
    if not isinstance(entries, list) or len(entries) != len(descriptors):
        raise BenchmarkIntegrityError("command authority observation cardinality mismatch")
    for descriptor, entry in zip(descriptors, entries):
        expected = {
            "canonical_path": descriptor["canonical_path"],
            "expected_sha256": descriptor["sha256"],
            "expected_byte_length": descriptor["byte_length"],
            "expected_executable": descriptor["executable"],
        }
        if any(entry.get(key) != value for key, value in expected.items()):
            raise BenchmarkIntegrityError("command authority observation expected bytes drifted")
        if entry.get("observed_status") == "matched" and (
            entry.get("observed_canonical_path") != descriptor["canonical_path"]
            or entry.get("observed_sha256") != descriptor["sha256"]
            or entry.get("observed_byte_length") != descriptor["byte_length"]
            or (
                descriptor["executable"] is True
                and entry.get("observed_executable") is not True
            )
        ):
            raise BenchmarkIntegrityError("matched command observation is not exact")
    expected_status = (
        "exact_match"
        if all(entry.get("observed_status") == "matched" for entry in entries)
        else "mismatch"
    )
    if observation.get("status") != expected_status:
        raise BenchmarkIntegrityError("command authority observation status is inconsistent")


def _require_live_command_authority(authority: Mapping[str, Any]) -> dict[str, Any]:
    observation = _observe_command_authority(authority)
    if observation["status"] != "exact_match":
        changed = [
            row["canonical_path"]
            for row in observation["entries"]
            if row["observed_status"] != "matched"
        ]
        raise BenchmarkIntegrityError(
            "sealed command dependency differs from approved bytes: " + ", ".join(changed)
        )
    return observation


def _workspace_record(run_directory: Path, workspace_ref: str, invocation_id: str) -> dict[str, Any]:
    workspace = _contained_relative(run_directory, workspace_ref)
    record: dict[str, Any] = {
        "run_directory": str(run_directory),
        "workspace_ref": workspace_ref,
        "resolved_path": str(workspace),
        "invocation_id": invocation_id,
    }
    record["workspace_digest"] = canonical_digest(record)
    return record


def _failure(stage: str, error_type: str, message: str) -> dict[str, str]:
    return {
        "stage": stage,
        "error_type": error_type,
        "message": message,
        "message_digest": bytes_digest(message.encode("utf-8", errors="replace")),
    }


def _local_isolation_assurance() -> dict[str, Any]:
    """Describe local process supervision without pretending it is a sandbox."""

    assurance: dict[str, Any] = {
        "schema_version": 1,
        "status": "unisolated_protocol_only",
        "deny_by_construction": False,
        "external_efficacy_eligible": False,
        "channels": {
            "declared_input_only": "unavailable_process_can_read_host_inputs",
            "filesystem": "unavailable_no_mount_or_namespace_confinement",
            "environment": "exact_replacement_allowlist_plus_typed_budget_fields",
            "process": "unavailable_process_group_controls_lifecycle_not_access",
            "network": "unavailable_no_network_namespace_or_deny_policy",
            "symlink_and_absolute_path": "unavailable_no_kernel_path_confinement",
            "undeclared_access_audit": "unavailable_no_observed_access_trace",
        },
        "boundary": (
            "an exact replacement environment, working-directory controls, and process-group "
            "supervision provide operational containment only; they do not hide benchmark "
            "truth or establish external-human efficacy"
        ),
    }
    assurance["content_digest"] = canonical_digest(assurance)
    return assurance


def _pre_spawn_event(
    *,
    role: str,
    command: Sequence[str],
    request_bytes: bytes,
    input_limit_bytes: int,
    stdout_limit_bytes: int,
    stderr_limit_bytes: int,
    governor: ResourceGovernor,
    status: str,
    failure: Mapping[str, str],
) -> dict[str, Any]:
    empty_digest = bytes_digest(b"")
    now = utc_now()
    message = str(failure["message"])
    encoded_error = message.encode("utf-8", errors="replace")
    return {
        "event_schema_version": 2,
        "event": "process_terminal",
        "role": role,
        "command": list(command),
        "pid": None,
        "started_at": now,
        "completed_at": now,
        "elapsed_seconds": 0.0,
        "returncode": None,
        "status": status,
        "terminal_dimension": None,
        "terminal_used": None,
        "terminal_limit": None,
        "termination": "not_started",
        "stdin_bytes": len(request_bytes),
        "stdin_sha256": bytes_digest(request_bytes),
        "stdin_limit_bytes": input_limit_bytes,
        "stdin_written_bytes": 0,
        "stdin_write_incomplete": False,
        "stdin_write_error": None,
        "stdout": "",
        "stderr": message,
        "stdout_bytes": 0,
        "stderr_bytes": len(encoded_error),
        "stdout_retained_bytes": 0,
        "stderr_retained_bytes": len(encoded_error),
        "stdout_sha256": empty_digest,
        "stderr_sha256": bytes_digest(encoded_error),
        "stdout_utf8_valid": True,
        "stderr_utf8_valid": True,
        "stdout_truncated": False,
        "stderr_truncated": False,
        "stdout_drain_incomplete": False,
        "stderr_drain_incomplete": False,
        "stdout_limit_bytes": stdout_limit_bytes,
        "stderr_limit_bytes": stderr_limit_bytes,
        "descendant_leak_detected": False,
        "capture_limit_bytes": governor.capture_limit_bytes,
        "resource_measurement": governor.measurement_boundaries(),
        "supervision_attempt": None,
        "resource_limit_execution": None,
        "post_supervision_acceptance": {
            "status": "not_run",
            "disk_snapshot_bytes": governor.usage.disk_bytes,
            "disk_limit_bytes": governor.budget.disk_bytes,
            "disk_limit_exceeded": (
                governor.usage.disk_bytes > governor.budget.disk_bytes
            ),
            "continuous_disk_observation": False,
            "snapshot_error": None,
            "acceptance_deadline_overrun": False,
        },
        "epistemic_effect": "none_operational_outcome_only",
    }


def _summary_from_receipt(receipt: Mapping[str, Any], receipt_path: Path) -> dict[str, Any]:
    workspace = receipt["workspace"]
    return {
        "schema_version": 1,
        "receipt_id": receipt["receipt_id"],
        "receipt_ref": receipt["receipt_ref"],
        "receipt_digest": receipt["content_digest"],
        "receipt_file_sha256": file_digest(receipt_path),
        "receipt_byte_length": receipt_path.stat().st_size,
        "index_ref": receipt["index_ref"],
        "run_directory": workspace["run_directory"],
        "benchmark_id": receipt["benchmark_id"],
        "benchmark_run_id": receipt["benchmark_run_id"],
        "role": receipt["role"],
        "invocation_id": receipt["invocation_id"],
        "request_digest": receipt["request_digest"],
        "command_authority_digest": receipt["command_authority"]["content_digest"],
        "command_authority_status": receipt["command_authority_observation"]["status"],
        "command_authority_observation_digest": receipt["command_authority_observation"]["content_digest"],
        "isolation_assurance_digest": receipt["isolation_assurance"]["content_digest"],
        "isolation_status": receipt["isolation_assurance"]["status"],
        "external_efficacy_eligible": receipt["isolation_assurance"]["external_efficacy_eligible"],
        "workspace_ref": workspace["workspace_ref"],
        "workspace_digest": workspace["workspace_digest"],
        "budget_digest": receipt["budget_digest"],
        "resource_receipt_digest": receipt["resource_receipt_digest"],
        "response_digest": receipt["response_digest"],
        "process_status": receipt["process_status"],
        "protocol_status": receipt["protocol_status"],
        "outcome_status": receipt["outcome_status"],
        "epistemic_effect": receipt["epistemic_effect"],
    }


def _validate_receipt(
    receipt: Mapping[str, Any],
    receipt_path: Path,
    *,
    require_live_authority: bool = False,
    historical_decode_only: bool = False,
) -> dict[str, Any]:
    payload = copy.deepcopy(dict(receipt))
    if historical_decode_only:
        if payload.get("schema_version") != 1 or require_live_authority:
            raise BenchmarkIntegrityError(
                "historical benchmark decoding accepts only legacy v1 without live authority"
            )
    elif payload.get("schema_version") != 2:
        raise BenchmarkIntegrityError(
            "legacy benchmark process receipts are decode-only and cannot carry current authority"
        )
    validate_payload(payload, RECEIPT_SCHEMA)
    if payload["content_digest"] != _top_level_content_digest(payload):
        raise BenchmarkIntegrityError("external benchmark receipt content digest mismatch")
    expected_receipt_id = stable_identifier(
        "benchmark-process-receipt",
        payload["benchmark_id"],
        payload["benchmark_run_id"],
        payload["role"],
        payload["invocation_id"],
    )
    if payload["receipt_id"] != expected_receipt_id:
        raise BenchmarkIntegrityError("external benchmark receipt identity mismatch")
    workspace = payload["workspace"]
    run_directory = Path(workspace["run_directory"])
    if not run_directory.is_absolute() or run_directory.resolve() != run_directory:
        raise BenchmarkIntegrityError("external benchmark run directory is not canonical")
    expected_receipt_path = _contained_relative(run_directory, payload["receipt_ref"])
    if receipt_path.resolve() != expected_receipt_path or receipt_path.is_symlink():
        raise BenchmarkIntegrityError("external benchmark receipt path mismatch")
    expected_workspace = _workspace_record(
        run_directory, workspace["workspace_ref"], payload["invocation_id"]
    )
    if workspace != expected_workspace:
        raise BenchmarkIntegrityError("external benchmark workspace binding mismatch")
    workspace_path = Path(workspace["resolved_path"])
    if not workspace_path.is_dir() or workspace_path.is_symlink():
        raise BenchmarkIntegrityError("external benchmark workspace is unavailable")
    _validate_command_authority_structure(payload["command_authority"])
    _validate_command_authority_observation(
        payload["command_authority"], payload["command_authority_observation"]
    )
    if payload["isolation_assurance"] != _local_isolation_assurance():
        raise BenchmarkIntegrityError(
            "local benchmark receipt overstates process isolation"
        )
    if payload["outcome_status"] == "accepted":
        if payload["command_authority_observation"]["status"] != "exact_match":
            raise BenchmarkIntegrityError("accepted process has mismatched command authority")
        if require_live_authority:
            _require_live_command_authority(payload["command_authority"])
    elif (
        payload["protocol_status"] == "authority_mismatch"
        and payload["command_authority_observation"]["status"] != "mismatch"
    ):
        raise BenchmarkIntegrityError("authority-mismatch receipt lacks mismatch observation")
    if payload["budget_digest"] != canonical_digest(payload["resource_receipt"]["budget"]):
        raise BenchmarkIntegrityError("external benchmark budget digest mismatch")
    if payload["resource_receipt_digest"] != canonical_digest(payload["resource_receipt"]):
        raise BenchmarkIntegrityError("external benchmark resource receipt digest mismatch")
    measurement = payload["resource_receipt"]["resource_measurement"]["disk_bytes"]
    if measurement.get("accounting_root") != str(workspace_path):
        raise BenchmarkIntegrityError("external benchmark accounting root mismatch")
    event = payload["process_event"]
    if payload["schema_version"] == 2:
        expected_environment = None
        if event.get("supervision_attempt") is not None:
            base_environment = minimal_replacement_environment(
                workspace_path,
                create_temporary=False,
            )
            expected_environment = complete_governed_process_environment(
                base_environment,
                deadline=payload["resource_receipt"]["deadline"],
                budget=payload["resource_receipt"]["budget"],
            )
        try:
            validate_v2_process_event(
                event,
                accepted=payload["outcome_status"] == "accepted",
                expected_workspace=workspace_path,
                expected_replacement_environment=expected_environment,
                require_live_execution_authority=require_live_authority,
            )
        except ValueError as exc:
            raise BenchmarkIntegrityError(
                f"external benchmark v2 process evidence is invalid: {exc}"
            ) from exc
    if (
        event.get("command") != payload["command_authority"]["argv"]
        or event.get("stdin_sha256") != payload["request_digest"]
        or payload["resource_receipt"]["events"] != [event]
        or payload["resource_receipt"]["status"] != payload["process_status"]
    ):
        raise BenchmarkIntegrityError("external benchmark process/resource binding mismatch")
    response = payload["response_payload"]
    expected_response_digest = canonical_digest(response) if response is not None else None
    if payload["response_digest"] != expected_response_digest:
        raise BenchmarkIntegrityError("external benchmark response digest mismatch")
    if payload["outcome_status"] == "accepted" and not isinstance(response, dict):
        raise BenchmarkIntegrityError("accepted external process lacks a response object")
    if payload["outcome_status"] != "accepted" and response is not None:
        raise BenchmarkIntegrityError("failed external process cannot retain an accepted response")
    if (payload["failure"] is None) != (payload["outcome_status"] == "accepted"):
        raise BenchmarkIntegrityError("external process failure shape differs from outcome")
    if payload["failure"] is not None and payload["failure"]["message_digest"] != bytes_digest(
        payload["failure"]["message"].encode("utf-8", errors="replace")
    ):
        raise BenchmarkIntegrityError("external process failure message digest mismatch")
    return payload


def decode_historical_external_process_receipt(
    raw: Mapping[str, Any],
    *,
    receipt_path: Path | str,
) -> dict[str, Any]:
    """Decode one immutable v1 receipt without granting current authority.

    Current reuse, index membership, evaluation, and promotion call the strict
    v2 validator directly.  This separate function exists only for historical
    inspection and cannot request live executable authority.
    """

    return _validate_receipt(
        raw,
        Path(receipt_path),
        require_live_authority=False,
        historical_decode_only=True,
    )


def _aggregate(receipts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    usages = [row["resource_receipt"]["usage"] for row in receipts]
    return {
        "wall_time_seconds": sum(float(row["wall_time_seconds"]) for row in usages),
        "cpu_seconds": sum(float(row["cpu_seconds"]) for row in usages),
        "peak_memory_bytes": max((int(row["peak_memory_bytes"]) for row in usages), default=0),
        "disk_bytes": sum(int(row["disk_bytes"]) for row in usages),
        "network_bytes": sum(int(row["network_bytes"]) for row in usages),
        "token_count": sum(int(row["token_count"]) for row in usages),
        "request_count": sum(int(row["request_count"]) for row in usages),
        "cost_usd": sum(float(row["cost_usd"]) for row in usages),
    }


def _accounting_boundary() -> dict[str, str]:
    return {
        "workspace_policy": "one_attempt_local_accounting_root_per_invocation",
        "network": "unavailable_without_adapter_measurement",
        "cost_units": "benchmark_payload_units_not_relabelled_as_cost_usd",
        "cost_usd": "unavailable_without_adapter_measurement",
        "isolation": "local_subprocess_protocol_only_no_hiddenness_or_external_efficacy",
        "epistemic_effect": "none_operational_accounting_only",
    }


def _receipt_summaries(
    run_directory: Path,
    role: str,
    *,
    require_live_authority: bool = False,
    validation_context: ExternalProcessValidationContext | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    receipt_directory = _contained_relative(run_directory, f"receipts/{role}")
    if not receipt_directory.exists():
        return [], []
    if receipt_directory.is_symlink() or not receipt_directory.is_dir():
        raise BenchmarkIntegrityError("external benchmark receipt directory is invalid")
    summaries: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    seen_invocations: set[str] = set()
    for path in sorted(receipt_directory.glob("*.json")):
        # Replay every receipt structurally.  Live files are checked below once
        # per unique accepted authority, avoiding O(receipts * executable-size)
        # hashing without weakening any receipt/index membership check.
        receipt = _validate_receipt(_load_json_object(path), path)
        if receipt["role"] != role or receipt["invocation_id"] in seen_invocations:
            raise BenchmarkIntegrityError("external benchmark receipt set is not role/invocation unique")
        seen_invocations.add(receipt["invocation_id"])
        receipts.append(receipt)
        summaries.append(_summary_from_receipt(receipt, path))
    if require_live_authority:
        context = validation_context or ExternalProcessValidationContext()
        for receipt in receipts:
            if receipt["outcome_status"] != "accepted":
                continue
            authority = receipt["command_authority"]
            context.require_live_authority(authority)
    paired = sorted(zip(summaries, receipts), key=lambda pair: pair[0]["invocation_id"])
    return [pair[0] for pair in paired], [pair[1] for pair in paired]


def _replay_index(
    index: Mapping[str, Any],
    index_path: Path,
    *,
    validation_context: ExternalProcessValidationContext,
) -> dict[str, Any]:
    """Replay one immutable index and retain its exact summary/receipt map."""

    validate_payload(index, INDEX_SCHEMA)
    payload = dict(index)
    if payload["content_digest"] != _top_level_content_digest(payload):
        raise BenchmarkIntegrityError("external benchmark process index digest mismatch")
    run_directory = Path(payload["run_directory"])
    expected_path = _contained_relative(run_directory, f"indices/{payload['role']}.json")
    if not run_directory.is_absolute() or run_directory.resolve() != run_directory or index_path.resolve() != expected_path or index_path.is_symlink():
        raise BenchmarkIntegrityError("external benchmark process index path mismatch")
    summaries, receipts = _receipt_summaries(
        run_directory,
        payload["role"],
        require_live_authority=True,
        validation_context=validation_context,
    )
    validation_context._counts["receipt_replays"] += len(receipts)
    expected_id = stable_identifier(
        "benchmark-process-index",
        payload["benchmark_id"],
        payload["benchmark_run_id"],
        payload["role"],
        summaries,
    )
    if (
        payload["index_id"] != expected_id
        or payload["receipt_count"] != len(summaries)
        or payload["receipts"] != summaries
        or payload["aggregate_usage"] != _aggregate(receipts)
        or payload["accounting_boundary"] != _accounting_boundary()
    ):
        raise BenchmarkIntegrityError("external benchmark process index transitive binding mismatch")
    receipt_records: dict[str, dict[str, Any]] = {}
    for summary, receipt in zip(summaries, receipts):
        receipt_id = str(summary["receipt_id"])
        if receipt_id in receipt_records:
            raise BenchmarkIntegrityError(
                "external benchmark process index repeats a receipt identity"
            )
        receipt_records[receipt_id] = {
            "summary": summary,
            "receipt": receipt,
        }
    return {"index": payload, "receipt_records": receipt_records}


def _validate_index(index: Mapping[str, Any], index_path: Path) -> dict[str, Any]:
    context = ExternalProcessValidationContext()
    validated = context.replay_index(index, index_path)["index"]
    context.assert_unchanged()
    return validated


def validate_external_process_summary(
    raw: Mapping[str, Any],
    *,
    role: str,
    request_digest: str | None = None,
    require_index: bool = False,
    validation_context: ExternalProcessValidationContext | None = None,
) -> dict[str, Any]:
    """Reopen a summary's complete authority chain and return its full receipt."""

    validate_payload(raw, SUMMARY_SCHEMA)
    summary = dict(raw)
    if summary["role"] != role:
        raise BenchmarkIntegrityError("external process execution role mismatch")
    if request_digest is not None and summary["request_digest"] != request_digest:
        raise BenchmarkIntegrityError("external process request digest mismatch")
    run_directory = Path(summary["run_directory"])
    if not run_directory.is_absolute() or run_directory.resolve() != run_directory:
        raise BenchmarkIntegrityError("external process run directory is not canonical")
    if require_index:
        context = validation_context or ExternalProcessValidationContext()
        index_path = _contained_relative(run_directory, summary["index_ref"])
        receipt = context.receipt_for_summary(summary, index_path)
        if validation_context is None:
            context.assert_unchanged()
        return receipt
    receipt_path = _contained_relative(run_directory, summary["receipt_ref"])
    receipt = _validate_receipt(
        _load_json_object(receipt_path),
        receipt_path,
        require_live_authority=True,
    )
    if summary != _summary_from_receipt(receipt, receipt_path):
        raise BenchmarkIntegrityError(
            "external process summary is not the exact receipt projection"
        )
    return receipt


class ExternalBenchmarkProcessAdapter:
    """Run one external benchmark role with exact, idempotent attestation."""

    def __init__(
        self,
        *,
        command: Sequence[str],
        role: str,
        benchmark_id: str,
        benchmark_run_id: str,
        run_root: Path | str,
        approved_dependency_paths: Sequence[Path | str] = (),
        grace_period_seconds: float = 0.25,
        memory_bytes: int = 512 * 1024 * 1024,
        disk_bytes: int = 64 * 1024 * 1024,
        input_limit_bytes: int = 1024 * 1024,
        stdout_limit_bytes: int = 1024 * 1024,
        stderr_limit_bytes: int = 256 * 1024,
        verifier_wall_time_seconds: float = 10.0,
    ) -> None:
        if role not in {"benchmark_runner", "human_evidence_verifier"}:
            raise ValueError("external benchmark role is invalid")
        if not command or not all(isinstance(item, str) and item for item in command):
            raise ValueError("external benchmark command must be non-empty argv")
        if not isinstance(benchmark_id, str) or not benchmark_id:
            raise ValueError("benchmark_id is required")
        validate_job_id(benchmark_run_id)
        limits = {
            "grace_period_seconds": grace_period_seconds,
            "memory_bytes": memory_bytes,
            "disk_bytes": disk_bytes,
            "input_limit_bytes": input_limit_bytes,
            "stdout_limit_bytes": stdout_limit_bytes,
            "stderr_limit_bytes": stderr_limit_bytes,
            "verifier_wall_time_seconds": verifier_wall_time_seconds,
        }
        if any(isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0 for value in limits.values()):
            raise ValueError("all external benchmark process limits must be positive")
        self.role = role
        self.benchmark_id = benchmark_id
        self.benchmark_run_id = benchmark_run_id
        self.run_root = Path(run_root).resolve()
        self.run_directory = contained_path(self.run_root, benchmark_run_id)
        self.run_directory.mkdir(parents=True, exist_ok=True)
        self.command, self.command_authority = _seal_command(command, approved_dependency_paths)
        self.grace_period_seconds = float(grace_period_seconds)
        self.memory_bytes = int(memory_bytes)
        self.disk_bytes = int(disk_bytes)
        self.input_limit_bytes = int(input_limit_bytes)
        self.stdout_limit_bytes = int(stdout_limit_bytes)
        self.stderr_limit_bytes = int(stderr_limit_bytes)
        self.verifier_wall_time_seconds = float(verifier_wall_time_seconds)
        self.index_ref = f"indices/{role}.json"
        self.index_path = _contained_relative(self.run_directory, self.index_ref)
        summaries, receipts = _receipt_summaries(self.run_directory, role)
        for receipt in receipts:
            if receipt["benchmark_id"] != benchmark_id or receipt["benchmark_run_id"] != benchmark_run_id or receipt["command_authority"] != self.command_authority:
                raise BenchmarkIntegrityError("existing benchmark receipt belongs to a different authority")
        self._summaries = {row["invocation_id"]: row for row in summaries}
        self._finalized = self.index_path.exists()
        if self._finalized:
            index = _validate_index(_load_json_object(self.index_path), self.index_path)
            if index["benchmark_id"] != benchmark_id or index["benchmark_run_id"] != benchmark_run_id or index["role"] != role:
                raise BenchmarkIntegrityError("existing benchmark index identity mismatch")

    def _budget(self, wall_seconds: float, token_limit: int) -> ResourceBudget:
        return ResourceBudget.from_mapping({
            "budget_id": stable_identifier("benchmark-budget", self.benchmark_id, self.benchmark_run_id, self.role, wall_seconds, token_limit),
            "wall_time_seconds": wall_seconds,
            "grace_period_seconds": self.grace_period_seconds,
            "cpu_seconds": wall_seconds,
            "memory_bytes": self.memory_bytes,
            "disk_bytes": self.disk_bytes,
            "network_bytes": 0,
            "token_count": token_limit,
            "request_count": 1,
            "cost_usd": 0.0,
        })

    def _paths(self, invocation_id: str) -> tuple[str, Path, str, Path]:
        receipt_id = stable_identifier(
            "benchmark-process-receipt",
            self.benchmark_id,
            self.benchmark_run_id,
            self.role,
            invocation_id,
        )
        receipt_ref = f"receipts/{self.role}/{receipt_id}.json"
        receipt_path = _contained_relative(self.run_directory, receipt_ref)
        workspace_ref = f"workspaces/{self.role}/{invocation_id}"
        workspace = _contained_relative(self.run_directory, workspace_ref)
        return receipt_ref, receipt_path, workspace_ref, workspace

    def _persist(
        self,
        *,
        invocation_id: str,
        request_digest: str,
        receipt_ref: str,
        receipt_path: Path,
        workspace_record: Mapping[str, Any],
        governor: ResourceGovernor,
        event: Mapping[str, Any],
        process_status: str,
        protocol_status: str,
        outcome_status: str,
        response_payload: Mapping[str, Any] | None,
        failure: Mapping[str, str] | None,
        command_authority_observation: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not governor.events or governor.events[-1] != event:
            governor.events.append(dict(event))
        resource_receipt = governor.receipt(process_status)
        payload: dict[str, Any] = {
            "schema_version": 2 if event.get("event_schema_version") == 2 else 1,
            "receipt_id": stable_identifier("benchmark-process-receipt", self.benchmark_id, self.benchmark_run_id, self.role, invocation_id),
            "receipt_ref": receipt_ref,
            "index_ref": self.index_ref,
            "benchmark_id": self.benchmark_id,
            "benchmark_run_id": self.benchmark_run_id,
            "role": self.role,
            "invocation_id": invocation_id,
            "request_digest": request_digest,
            "command_authority": self.command_authority,
            "command_authority_observation": dict(command_authority_observation),
            "isolation_assurance": _local_isolation_assurance(),
            "workspace": dict(workspace_record),
            "budget_digest": canonical_digest(resource_receipt["budget"]),
            "process_status": process_status,
            "protocol_status": protocol_status,
            "outcome_status": outcome_status,
            "process_event": dict(event),
            "resource_receipt": resource_receipt,
            "resource_receipt_digest": canonical_digest(resource_receipt),
            "response_payload": dict(response_payload) if response_payload is not None else None,
            "response_digest": canonical_digest(response_payload) if response_payload is not None else None,
            "failure": dict(failure) if failure is not None else None,
            "epistemic_effect": EPistemic_NULL,
        }
        payload["content_digest"] = _top_level_content_digest(payload)
        validate_payload(payload, RECEIPT_SCHEMA)
        _write_immutable_json(receipt_path, payload)
        persisted = _validate_receipt(_load_json_object(receipt_path), receipt_path)
        summary = _summary_from_receipt(persisted, receipt_path)
        validate_payload(summary, SUMMARY_SCHEMA)
        previous = self._summaries.get(invocation_id)
        if previous is not None and previous != summary:
            raise BenchmarkIntegrityError("one invocation resolved to conflicting summaries")
        self._summaries[invocation_id] = summary
        return summary

    def _existing(self, invocation_id: str, receipt_path: Path) -> tuple[dict[str, Any], dict[str, Any]] | None:
        if not receipt_path.exists():
            return None
        receipt = _validate_receipt(
            _load_json_object(receipt_path),
            receipt_path,
            require_live_authority=True,
        )
        if receipt["command_authority"] != self.command_authority:
            raise BenchmarkIntegrityError("idempotent invocation command authority changed")
        summary = _summary_from_receipt(receipt, receipt_path)
        if receipt["outcome_status"] != "accepted":
            raise ExternalBenchmarkProcessError(
                f"{self.role} previously ended with {receipt['process_status']}/{receipt['protocol_status']}",
                summary,
            )
        return dict(receipt["response_payload"]), summary

    def _invoke(self, request: Mapping[str, Any], *, wall_seconds: float, token_limit: int, reserved_key: str) -> tuple[dict[str, Any], dict[str, Any]]:
        try:
            encoded = canonical_json(dict(request)) + b"\n"
        except Exception as exc:
            raise BenchmarkIntegrityError(f"external benchmark request is not canonical JSON: {exc}") from exc
        request_digest = bytes_digest(encoded)
        invocation_id = stable_identifier("benchmark-invocation", self.benchmark_id, self.benchmark_run_id, self.role, request_digest)
        receipt_ref, receipt_path, workspace_ref, workspace = self._paths(invocation_id)
        existing = self._existing(invocation_id, receipt_path)
        if existing is not None:
            return existing
        if self._finalized:
            raise BenchmarkIntegrityError("external benchmark role index is finalized; new invocations are forbidden")
        workspace.mkdir(parents=True, exist_ok=True)
        replacement_environment = minimal_replacement_environment(workspace)
        workspace_record = _workspace_record(self.run_directory, workspace_ref, invocation_id)
        try:
            budget = self._budget(wall_seconds, token_limit)
        except Exception as exc:
            raise BenchmarkIntegrityError(f"external benchmark invocation budget is invalid: {exc}") from exc
        governor = ResourceGovernor(
            budget,
            run_directory=workspace,
            allowed_working_directory=workspace,
            capture_limit_bytes=max(self.stdout_limit_bytes, self.stderr_limit_bytes),
            disk_sample_interval_seconds=0.01,
        )
        observation = _observe_command_authority(self.command_authority)
        if observation["status"] != "exact_match":
            failure = _failure(
                "command_authority",
                "CommandAuthorityMismatch",
                "sealed command dependency differs from approved bytes",
            )
            event = _pre_spawn_event(
                role=self.role,
                command=self.command,
                request_bytes=encoded,
                input_limit_bytes=self.input_limit_bytes,
                stdout_limit_bytes=self.stdout_limit_bytes,
                stderr_limit_bytes=self.stderr_limit_bytes,
                governor=governor,
                status="worker_failed",
                failure=failure,
            )
            summary = self._persist(
                invocation_id=invocation_id,
                request_digest=request_digest,
                receipt_ref=receipt_ref,
                receipt_path=receipt_path,
                workspace_record=workspace_record,
                governor=governor,
                event=event,
                process_status="worker_failed",
                protocol_status="authority_mismatch",
                outcome_status="operational_failure",
                response_payload=None,
                failure=failure,
                command_authority_observation=observation,
            )
            raise ExternalBenchmarkProcessError(
                f"{self.role} command authority changed before spawn", summary
            )
        try:
            event = governor.run_process(
                self.command,
                cwd=workspace,
                replacement_environment=replacement_environment,
                role=self.role,
                input_bytes=encoded,
                input_limit_bytes=self.input_limit_bytes,
                stdout_limit_bytes=self.stdout_limit_bytes,
                stderr_limit_bytes=self.stderr_limit_bytes,
            )
        except (OSError, ValueError, BudgetExceeded, subprocess.SubprocessError) as exc:
            status = exc.status if isinstance(exc, BudgetExceeded) else "worker_failed"
            failure = _failure("pre_spawn_or_launch", type(exc).__name__, str(exc))
            event = _pre_spawn_event(
                role=self.role,
                command=self.command,
                request_bytes=encoded,
                input_limit_bytes=self.input_limit_bytes,
                stdout_limit_bytes=self.stdout_limit_bytes,
                stderr_limit_bytes=self.stderr_limit_bytes,
                governor=governor,
                status=status,
                failure=failure,
            )
            summary = self._persist(
                invocation_id=invocation_id,
                request_digest=request_digest,
                receipt_ref=receipt_ref,
                receipt_path=receipt_path,
                workspace_record=workspace_record,
                governor=governor,
                event=event,
                process_status=status,
                protocol_status="authority_or_launch_failed",
                outcome_status="operational_failure",
                response_payload=None,
                failure=failure,
                command_authority_observation=observation,
            )
            raise ExternalBenchmarkProcessError(
                f"{self.role} ended before accepted process output", summary
            ) from exc

        post_observation = _observe_command_authority(self.command_authority)
        process_status = str(event.get("status") or "worker_failed")
        protocol_status = "accepted"
        outcome_status = "accepted"
        parsed: Any = None
        failure: dict[str, str] | None = None
        if post_observation["status"] != "exact_match":
            process_status, protocol_status, outcome_status = "worker_failed", "authority_mismatch", "operational_failure"
            failure = _failure(
                "command_authority",
                "CommandAuthorityMismatch",
                "sealed command dependency changed during process execution",
            )
        elif process_status != "succeeded":
            protocol_status = process_status if process_status in {"input_exhausted", "output_exhausted"} else "process_failed"
            outcome_status = "operational_failure"
            failure = _failure("process_execution", process_status, str(event.get("stderr") or process_status))
        elif event.get("stdout_utf8_valid") is not True:
            process_status, protocol_status, outcome_status = "worker_failed", "invalid_utf8", "protocol_failure"
            failure = _failure("response_decode", "UnicodeDecodeError", "stdout is not valid UTF-8")
        else:
            try:
                parsed = json.loads(str(event.get("stdout", "")))
            except json.JSONDecodeError as exc:
                process_status, protocol_status, outcome_status = "worker_failed", "invalid_json", "protocol_failure"
                failure = _failure("response_decode", type(exc).__name__, str(exc))
            if outcome_status == "accepted" and not isinstance(parsed, dict):
                process_status, protocol_status, outcome_status = "worker_failed", "non_object", "protocol_failure"
                failure = _failure("response_shape", "TypeError", "response is not a JSON object")
            if outcome_status == "accepted" and reserved_key in parsed:
                process_status, protocol_status, outcome_status = "worker_failed", "reserved_field_spoofed", "protocol_failure"
                failure = _failure("response_shape", "ReservedFieldSpoof", reserved_key)
            if outcome_status == "accepted":
                try:
                    governor.account(request_count=1)
                    if self.role == "benchmark_runner":
                        usage = parsed.get("resource_usage", {})
                        if not isinstance(usage, Mapping):
                            raise ValueError("resource_usage is not an object")
                        tokens = usage.get("tokens", 0)
                        if isinstance(tokens, bool):
                            raise ValueError("reported token usage cannot be boolean")
                        governor.account(token_count=int(tokens))
                except (BudgetExceeded, TypeError, ValueError) as exc:
                    process_status = exc.status if isinstance(exc, BudgetExceeded) else "worker_failed"
                    protocol_status, outcome_status = "reported_usage_exhausted", "operational_failure"
                    failure = _failure("reported_usage", type(exc).__name__, str(exc))

        accepted_response = parsed if outcome_status == "accepted" else None
        summary = self._persist(
            invocation_id=invocation_id,
            request_digest=request_digest,
            receipt_ref=receipt_ref,
            receipt_path=receipt_path,
            workspace_record=workspace_record,
            governor=governor,
            event=event,
            process_status=process_status,
            protocol_status=protocol_status,
            outcome_status=outcome_status,
            response_payload=accepted_response,
            failure=failure,
            command_authority_observation=post_observation,
        )
        if outcome_status != "accepted":
            raise ExternalBenchmarkProcessError(
                f"{self.role} ended with {process_status}/{protocol_status}", summary
            )
        return dict(parsed), summary

    def _persist_verifier_encoding_failure(
        self, raw: Any, descriptor: Any, exc: Exception
    ) -> dict[str, Any]:
        artifact_bytes = raw if isinstance(raw, bytes) else repr(raw).encode("utf-8", errors="replace")
        descriptor_repr = repr(descriptor)
        surrogate = canonical_json({
            "artifact_sha256": bytes_digest(artifact_bytes),
            "artifact_byte_length": len(artifact_bytes),
            "descriptor_repr_sha256": bytes_digest(descriptor_repr.encode("utf-8", errors="replace")),
            "request_encoding_status": "failed",
        }) + b"\n"
        request_digest = bytes_digest(surrogate)
        invocation_id = stable_identifier("benchmark-invocation", self.benchmark_id, self.benchmark_run_id, self.role, request_digest)
        receipt_ref, receipt_path, workspace_ref, workspace = self._paths(invocation_id)
        existing = self._existing(invocation_id, receipt_path)
        if existing is not None:
            return existing[1]
        if self._finalized:
            raise BenchmarkIntegrityError("external benchmark role index is finalized; new invocations are forbidden")
        workspace.mkdir(parents=True, exist_ok=True)
        governor = ResourceGovernor(
            self._budget(self.verifier_wall_time_seconds, 1),
            run_directory=workspace,
            allowed_working_directory=workspace,
            capture_limit_bytes=max(self.stdout_limit_bytes, self.stderr_limit_bytes),
            disk_sample_interval_seconds=0.01,
        )
        failure = _failure("verifier_request_encoding", type(exc).__name__, str(exc))
        event = _pre_spawn_event(
            role=self.role,
            command=self.command,
            request_bytes=surrogate,
            input_limit_bytes=self.input_limit_bytes,
            stdout_limit_bytes=self.stdout_limit_bytes,
            stderr_limit_bytes=self.stderr_limit_bytes,
            governor=governor,
            status="worker_failed",
            failure=failure,
        )
        observation = _observe_command_authority(self.command_authority)
        return self._persist(
            invocation_id=invocation_id,
            request_digest=request_digest,
            receipt_ref=receipt_ref,
            receipt_path=receipt_path,
            workspace_record=_workspace_record(self.run_directory, workspace_ref, invocation_id),
            governor=governor,
            event=event,
            process_status="worker_failed",
            protocol_status="request_encoding_failed",
            outcome_status="protocol_failure",
            response_payload=None,
            failure=failure,
            command_authority_observation=observation,
        )

    def hidden_runner(self, request: Mapping[str, Any]) -> dict[str, Any]:
        budget = request.get("resource_budget", {})
        if not isinstance(budget, Mapping):
            raise BenchmarkIntegrityError("hidden request budget is not an object")
        parsed, summary = self._invoke(
            request,
            wall_seconds=float(budget.get("wall_seconds", 0)),
            token_limit=int(budget.get("tokens", 0)),
            reserved_key=RUNNER_EXECUTION_KEY,
        )
        return {**parsed, RUNNER_EXECUTION_KEY: summary}

    def verifier(self, raw: bytes, descriptor: Mapping[str, Any]) -> dict[str, Any]:
        """Return every process/protocol failure as a persisted operational null."""

        try:
            if not isinstance(raw, bytes):
                raise TypeError("verifier artifact must be bytes")
            if not isinstance(descriptor, Mapping):
                raise TypeError("verifier descriptor must be an object")
            request = {
                "descriptor": dict(descriptor),
                "artifact_utf8": raw.decode("utf-8", errors="strict"),
            }
        except (TypeError, UnicodeDecodeError) as exc:
            try:
                summary = self._persist_verifier_encoding_failure(raw, descriptor, exc)
            except ExternalBenchmarkProcessError as prior:
                summary = prior.receipt
            self.finalize()
            return {VERIFIER_EXECUTION_KEY: summary}
        try:
            parsed, summary = self._invoke(
                request,
                wall_seconds=self.verifier_wall_time_seconds,
                token_limit=1,
                reserved_key=VERIFIER_EXECUTION_KEY,
            )
        except ExternalBenchmarkProcessError as exc:
            self.finalize()
            return {VERIFIER_EXECUTION_KEY: exc.receipt}
        self.finalize()
        return {**parsed, VERIFIER_EXECUTION_KEY: summary}

    def finalize(self) -> dict[str, Any]:
        if self._finalized:
            return _validate_index(_load_json_object(self.index_path), self.index_path)
        summaries, receipts = _receipt_summaries(self.run_directory, self.role)
        if summaries != sorted(self._summaries.values(), key=lambda row: row["invocation_id"]):
            raise BenchmarkIntegrityError("in-memory and immutable benchmark summaries differ")
        index: dict[str, Any] = {
            "schema_version": 1,
            "index_id": stable_identifier("benchmark-process-index", self.benchmark_id, self.benchmark_run_id, self.role, summaries),
            "benchmark_id": self.benchmark_id,
            "benchmark_run_id": self.benchmark_run_id,
            "role": self.role,
            "run_directory": str(self.run_directory),
            "receipt_count": len(summaries),
            "receipts": summaries,
            "aggregate_usage": _aggregate(receipts),
            "accounting_boundary": _accounting_boundary(),
        }
        index["content_digest"] = _top_level_content_digest(index)
        validate_payload(index, INDEX_SCHEMA)
        _write_immutable_json(self.index_path, index)
        self._finalized = True
        return _validate_index(_load_json_object(self.index_path), self.index_path)


__all__ = [
    "ExternalBenchmarkProcessAdapter",
    "ExternalBenchmarkProcessError",
    "ExternalProcessValidationContext",
    "validate_external_process_summary",
]
