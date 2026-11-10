# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Execute and validate fresh, content-bound TODO acceptance evidence.

A receipt is an immutable snapshot, not an authority that can attest to its own
truth. Issuance records exact command, implementation, toolchain, and artifact
state. Final completion validation verifies that snapshot and then executes the
declared commands again. Every path is repository-relative and symlink-free so
an apparently local artifact cannot silently name bytes outside the workspace.
"""

from __future__ import annotations

import copy
import json
import shlex
import subprocess
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Callable

from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    file_digest,
    safe_relative_path,
    stable_identifier,
    utc_now,
    validate_payload,
)


class TodoAcceptanceError(ContractError):
    """Raised when evidence is failed, stale, malformed, or incomplete."""


# Acceptance must become stale when the implementation or a validator changes,
# even when that file is not repeated on every TODO's short required-artifact
# list.  Keep the surface narrow enough to exclude mutable reports/runs while
# covering the shared runtime, every validator, the tests, and the six central
# skill contracts.
IMPLEMENTATION_SURFACE: tuple[str, ...] = (
    "agentic/discovery",
    "agentic/experiments",
    "agentic/scripts",
    "agentic/spec",
    "agentic/state/discovery_transaction.py",
    "agentic/registries",
    "agentic/evals/ym_representational_dynamics_20260721",
    "agentic/external/yang_mills_representational_dynamics/2026-07-21/normalized",
    "agentic/external/yang_mills_representational_dynamics/2026-07-21/source_archives/full ym_representational_dynamics_complete_2026-07-21 (1).zip",
    "agentic/external/yang_mills_representational_dynamics/2026-07-21/immutable_source_manifest.json",
    "agentic/external/yang_mills_representational_dynamics/2026-07-21/checksum_report.json",
    "agentic/reports/ym_representational_dynamics_integration/2026-07-21/canonical_parent_cycle",
    "tests",
    ".github/workflows",
    "docs/plans-and-reviews/discovery-workflow-review-and-todos.md",
    "docs/operations/discovery-marathon-operations.md",
    "docs/operations/target-navigation-runbook.md",
    "docs/case-studies/yang-mills/ym-representational-dynamics-integration-todos.md",
    "docs/reference/skills.md",
    "registry/skill_projections",
    "skills/orchestration/reflective-conceptual-discovery",
    "skills/orchestration/parallel-hypothesis-portfolio",
    "skills/orchestration/work",
    "skills/orchestration/kb-orchestrator/scripts/simulate_theorem_discovery.py",
    "skills/reasoning/reflective-theory-synthesizer",
    "skills/reasoning/frontier-literature-assimilator",
    "skills/reasoning/high-risk-hypothesis-forger",
    "skills/reasoning/dynamic-symbolic-simulation-experimenter",
    "skills/yang_mills",
)


def todo_definition_digest(todo: Mapping[str, Any]) -> str:
    """Bind acceptance semantics while ignoring lifecycle/evidence bookkeeping."""

    semantic = {
        key: copy.deepcopy(value)
        for key, value in todo.items()
        if key not in {"status", "evidence", "review_date"}
    }
    return canonical_digest(semantic)


def resolve_safe_workspace_path(
    workspace: Path,
    raw_path: str,
    *,
    context: str,
    must_exist: bool = False,
    require_file: bool = False,
) -> Path:
    """Resolve a relative path without accepting any symlink component.

    ``Path.resolve`` alone is insufficient for a trust boundary because it
    follows a symlink and erases the evidence that a redirect existed. This
    helper inspects the lexical path first, then proves that the resolved result
    remains below the canonical workspace root.
    """

    try:
        relative = safe_relative_path(raw_path)
    except ContractError as exc:
        raise TodoAcceptanceError(f"unsafe {context} path: {raw_path!r}") from exc
    root = workspace.resolve()
    if not root.is_dir():
        raise TodoAcceptanceError(f"workspace is not a directory: {workspace}")
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise TodoAcceptanceError(
                f"{context} path contains a symlink: {relative.as_posix()}"
            )
    resolved = cursor.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise TodoAcceptanceError(
            f"{context} path escapes workspace: {raw_path!r}"
        ) from exc
    if must_exist and not resolved.exists():
        raise TodoAcceptanceError(
            f"{context} does not exist: {relative.as_posix()}"
        )
    if require_file and (not resolved.exists() or not resolved.is_file()):
        raise TodoAcceptanceError(
            f"{context} is not a regular file: {relative.as_posix()}"
        )
    return resolved


def _relative_workspace_file(
    workspace: Path, path: Path, *, context: str, must_exist: bool
) -> tuple[str, Path]:
    """Return the canonical relative name for an API-supplied workspace file."""

    root = workspace.resolve()
    candidate = path if path.is_absolute() else root / path
    try:
        relative = candidate.absolute().relative_to(root)
    except ValueError as exc:
        raise TodoAcceptanceError(f"{context} escapes workspace: {path}") from exc
    resolved = resolve_safe_workspace_path(
        root,
        relative.as_posix(),
        context=context,
        must_exist=must_exist,
        require_file=must_exist,
    )
    return relative.as_posix(), resolved


def _regular_descendants(path: Path, workspace: Path, *, context: str) -> list[Path]:
    """Enumerate regular descendants while rejecting redirects and special files."""

    root = workspace.resolve()
    pending = [path]
    files: list[Path] = []
    while pending:
        directory = pending.pop()
        for child in sorted(directory.iterdir(), key=lambda item: item.name):
            relative = child.relative_to(root).as_posix()
            if child.is_symlink():
                raise TodoAcceptanceError(
                    f"{context} contains a symlink: {relative}"
                )
            resolved = child.resolve()
            try:
                resolved.relative_to(root)
            except ValueError as exc:
                raise TodoAcceptanceError(
                    f"{context} descendant escapes workspace: {relative}"
                ) from exc
            if child.is_dir():
                pending.append(child)
            elif child.is_file():
                files.append(child)
            else:
                raise TodoAcceptanceError(
                    f"{context} contains a non-regular entry: {relative}"
                )
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def _directory_digest(path: Path, workspace: Path, *, context: str) -> tuple[str, int]:
    rows: list[dict[str, Any]] = []
    for child in _regular_descendants(path, workspace, context=context):
        if "__pycache__" in child.parts or child.suffix in {".pyc", ".pyo"}:
            continue
        rows.append(
            {
                "path": child.relative_to(path).as_posix(),
                "sha256": file_digest(child),
                "size_bytes": child.stat().st_size,
            }
        )
    return canonical_digest(rows), len(rows)


def artifact_result(workspace: Path, raw_path: str) -> dict[str, Any]:
    """Hash one explicit artifact, including large binary source archives."""

    relative = safe_relative_path(raw_path)
    path = resolve_safe_workspace_path(
        workspace, raw_path, context="required artifact"
    )
    if path.is_file():
        return {
            "path": relative.as_posix(), "kind": "file", "exists": True,
            "content_digest": file_digest(path), "file_count": 1,
        }
    if path.is_dir():
        digest, count = _directory_digest(
            path, workspace, context=f"required artifact {relative.as_posix()}"
        )
        return {
            "path": relative.as_posix(), "kind": "directory", "exists": True,
            "content_digest": digest, "file_count": count,
        }
    return {
        "path": relative.as_posix(), "kind": "missing", "exists": False,
        "content_digest": canonical_digest({"missing": relative.as_posix()}), "file_count": 0,
    }


def toolchain_digest(workspace: Path) -> str:
    rows = []
    for name in ("pyproject.toml", "uv.lock"):
        path = resolve_safe_workspace_path(
            workspace, name, context="toolchain file"
        )
        rows.append({"path": name, "sha256": file_digest(path) if path.is_file() else None})
    return canonical_digest(rows)


def implementation_surface_digest(workspace: Path) -> str:
    """Hash code, validators, tests, schemas, registries, and core skills.

    Missing optional roots are represented explicitly.  This keeps the helper
    usable in isolated unit-test workspaces while preventing a receipt from
    surviving a weakened validator or changed implementation in the real repo.
    """

    workspace = workspace.resolve()
    rows: list[dict[str, Any]] = []
    for raw in IMPLEMENTATION_SURFACE:
        relative = safe_relative_path(raw, forbid_latest=False)
        path = resolve_safe_workspace_path(
            workspace, raw, context="implementation surface"
        )
        if path.is_file():
            rows.append(
                {
                    "path": relative.as_posix(),
                    "kind": "file",
                    "sha256": file_digest(path),
                    "size_bytes": path.stat().st_size,
                }
            )
            continue
        if path.is_dir():
            for child in _regular_descendants(
                path, workspace, context=f"implementation surface {raw}"
            ):
                if "__pycache__" in child.parts or child.suffix in {".pyc", ".pyo"}:
                    continue
                rows.append(
                    {
                        "path": child.relative_to(workspace).as_posix(),
                        "kind": "file",
                        "sha256": file_digest(child),
                        "size_bytes": child.stat().st_size,
                    }
                )
            continue
        rows.append({"path": relative.as_posix(), "kind": "missing"})
    return canonical_digest(rows)


def command_argv(command: str) -> list[str]:
    """Parse an argv-only validation command and reject shell control syntax."""

    if any(token in command for token in (";", "&&", "||", "`", "$(", ">", "<", "|")):
        raise TodoAcceptanceError(f"shell control syntax is forbidden: {command}")
    argv = shlex.split(command)
    if not argv:
        raise TodoAcceptanceError("empty validation command")
    if argv[0] in {"python", "python3"}:
        argv[0] = sys.executable
    elif Path(argv[0]).resolve() != Path(sys.executable).resolve():
        raise TodoAcceptanceError(
            f"acceptance commands must use the locked Python entrypoint: {command}"
        )
    return argv


def _todo_contract(todo: Mapping[str, Any]) -> tuple[list[str], list[str]]:
    """Validate command and artifact lists before acceptance work begins."""

    commands = todo.get("validation_commands")
    artifacts = todo.get("required_artifact")
    todo_id = todo.get("id")
    if not isinstance(todo_id, str) or not todo_id.strip():
        raise TodoAcceptanceError("TODO has no valid id")
    if not isinstance(commands, list) or not commands:
        raise TodoAcceptanceError(f"TODO {todo_id} has no validation_commands")
    if not all(isinstance(command, str) and command.strip() for command in commands):
        raise TodoAcceptanceError(f"TODO {todo_id} has an invalid validation command")
    if len(commands) != len(set(commands)):
        raise TodoAcceptanceError(f"TODO {todo_id} repeats a validation command")
    if not isinstance(artifacts, list) or not artifacts:
        raise TodoAcceptanceError(f"TODO {todo_id} has no required artifacts")
    if not all(isinstance(path, str) and path.strip() for path in artifacts):
        raise TodoAcceptanceError(f"TODO {todo_id} has an invalid required artifact")
    if len(artifacts) != len(set(artifacts)):
        raise TodoAcceptanceError(f"TODO {todo_id} repeats a required artifact")
    return list(commands), list(artifacts)


def _execute_commands(
    commands: Sequence[str],
    *,
    workspace: Path,
    timeout_seconds: float,
    state_guard: Callable[[], None] | None = None,
) -> list[dict[str, Any]]:
    """Execute argv-only commands while guarding frozen authority inputs.

    The guard runs immediately before and after every subprocess.  Callers use
    it to prove that a validator did not rewrite its own TODO deck or another
    selected deck while the command result was being produced.
    """

    if timeout_seconds <= 0:
        raise TodoAcceptanceError("timeout_seconds must be positive")
    results: list[dict[str, Any]] = []
    for command in commands:
        if state_guard is not None:
            state_guard()
        argv = command_argv(command)
        try:
            try:
                completed = subprocess.run(
                    argv,
                    cwd=workspace,
                    text=True,
                    capture_output=True,
                    timeout=timeout_seconds,
                    check=False,
                )
                status = "passed" if completed.returncode == 0 else "failed"
                stdout, stderr, exit_code = (
                    completed.stdout,
                    completed.stderr,
                    completed.returncode,
                )
            except subprocess.TimeoutExpired as exc:
                status, exit_code = "timed_out", 124
                stdout = exc.stdout if isinstance(exc.stdout, str) else ""
                stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        finally:
            if state_guard is not None:
                state_guard()
        results.append(
            {
                "command": command,
                "argv": argv,
                "exit_code": exit_code,
                "status": status,
                "stdout_digest": canonical_digest(stdout),
                "stderr_digest": canonical_digest(stderr),
                "stdout_tail": stdout[-2000:],
                "stderr_tail": stderr[-2000:],
            }
        )
    return results


def _receipt_identifier(receipt: Mapping[str, Any]) -> str:
    """Derive the receipt ID from every field except its two self-hashes."""

    payload = {
        key: value
        for key, value in receipt.items()
        if key not in {"receipt_id", "receipt_digest"}
    }
    return stable_identifier("todo-acceptance", payload)


def _seal_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    """Add the independently recomputable receipt ID and full receipt digest."""

    receipt["receipt_id"] = _receipt_identifier(receipt)
    receipt["receipt_digest"] = canonical_digest(
        receipt, exclude_keys=("receipt_digest",)
    )
    return receipt


def receipt_annotation_path(todo: Mapping[str, Any], *, workspace: Path) -> Path:
    """Resolve the one immutable receipt annotation allowed on a TODO card."""

    evidence = todo.get("evidence")
    annotations = (
        [
            item
            for item in evidence
            if isinstance(item, str) and item.startswith("receipt:")
        ]
        if isinstance(evidence, list)
        else []
    )
    if len(annotations) != 1:
        raise TodoAcceptanceError(
            f"TODO {todo.get('id')} must have exactly one receipt annotation; "
            f"found {len(annotations)}"
        )
    raw_path = annotations[0].removeprefix("receipt:")
    if raw_path != raw_path.strip():
        raise TodoAcceptanceError(
            f"TODO {todo.get('id')} receipt path has surrounding whitespace"
        )
    return resolve_safe_workspace_path(
        workspace,
        raw_path,
        context=f"TODO {todo.get('id')} receipt",
        must_exist=True,
        require_file=True,
    )


def run_acceptance(
    todo: Mapping[str, Any], *, todo_file: Path, workspace: Path, timeout_seconds: float = 900
) -> dict[str, Any]:
    """Execute every declared command and freeze required-artifact digests."""

    commands, artifacts = _todo_contract(todo)
    relative_file, resolved_todo_file = _relative_workspace_file(
        workspace, todo_file, context="TODO file", must_exist=True
    )
    frozen_todo_bytes = resolved_todo_file.read_bytes()

    def todo_file_guard() -> None:
        _, current = _relative_workspace_file(
            workspace, resolved_todo_file, context="TODO file", must_exist=True
        )
        if current.read_bytes() != frozen_todo_bytes:
            raise TodoAcceptanceError(
                f"TODO deck changed during acceptance command: {relative_file}"
            )

    started = utc_now()
    results = _execute_commands(
        commands,
        workspace=workspace,
        timeout_seconds=timeout_seconds,
        state_guard=todo_file_guard,
    )
    artifact_results = [artifact_result(workspace, path) for path in artifacts]
    passed = all(row["status"] == "passed" for row in results) and all(
        row["exists"] for row in artifact_results
    )
    surface_digest = implementation_surface_digest(workspace)
    receipt: dict[str, Any] = {
        "schema_version": "1.0.0",
        "todo_id": todo["id"], "todo_file": relative_file,
        "todo_definition_digest": todo_definition_digest(todo),
        "toolchain_digest": toolchain_digest(workspace),
        "implementation_surface_digest": surface_digest,
        "started_at": started, "completed_at": utc_now(),
        "validation_results": results, "artifact_results": artifact_results,
        "overall_status": "passed" if passed else "failed",
    }
    _seal_receipt(receipt)
    validate_payload(receipt, "todo_acceptance_receipt.schema.json")
    return receipt


def validate_acceptance_receipt(
    receipt: Mapping[str, Any],
    todo: Mapping[str, Any],
    *,
    todo_file: Path,
    workspace: Path,
    reexecute_commands: bool = False,
    timeout_seconds: float = 900,
    state_guard: Callable[[], None] | None = None,
) -> None:
    """Reject stale evidence and optionally rerun commands as a fresh check.

    Final TODO completion sets ``reexecute_commands``. Stored result fields then
    remain useful provenance, but cannot authorize the card on their own.
    """

    commands, artifacts = _todo_contract(todo)
    expected_file, resolved_todo_file = _relative_workspace_file(
        workspace, todo_file, context="TODO file", must_exist=True
    )
    frozen_todo_bytes = resolved_todo_file.read_bytes()

    def guarded_todo_state() -> None:
        _, current = _relative_workspace_file(
            workspace, resolved_todo_file, context="TODO file", must_exist=True
        )
        if current.read_bytes() != frozen_todo_bytes:
            raise TodoAcceptanceError(
                f"TODO deck changed during fresh validation: {expected_file}"
            )
        if state_guard is not None:
            state_guard()

    guarded_todo_state()
    validate_payload(dict(receipt), "todo_acceptance_receipt.schema.json")
    if receipt["receipt_digest"] != canonical_digest(receipt, exclude_keys=("receipt_digest",)):
        raise TodoAcceptanceError("TODO acceptance receipt digest mismatch")
    if receipt["receipt_id"] != _receipt_identifier(receipt):
        raise TodoAcceptanceError("TODO acceptance receipt ID mismatch")
    if receipt["overall_status"] != "passed" or any(
        row["status"] != "passed" or row["exit_code"] != 0
        for row in receipt["validation_results"]
    ):
        raise TodoAcceptanceError("TODO acceptance commands did not all pass")
    if receipt["todo_id"] != todo.get("id") or receipt["todo_file"] != expected_file:
        raise TodoAcceptanceError("TODO acceptance identity mismatch")
    if receipt["todo_definition_digest"] != todo_definition_digest(todo):
        raise TodoAcceptanceError("TODO definition changed after acceptance")
    if receipt["toolchain_digest"] != toolchain_digest(workspace):
        raise TodoAcceptanceError("locked toolchain changed after acceptance")
    if receipt["implementation_surface_digest"] != implementation_surface_digest(workspace):
        raise TodoAcceptanceError("implementation or validator surface changed after acceptance")
    if [row["command"] for row in receipt["validation_results"]] != commands:
        raise TodoAcceptanceError("TODO validation command set changed after acceptance")
    if [row["argv"] for row in receipt["validation_results"]] != [
        command_argv(command) for command in commands
    ]:
        raise TodoAcceptanceError("TODO validation argv changed after acceptance")
    if any(
        not row["exists"] or row["kind"] == "missing"
        for row in receipt["artifact_results"]
    ):
        raise TodoAcceptanceError("TODO acceptance receipt has a missing required artifact")
    expected_artifacts = [artifact_result(workspace, path) for path in artifacts]
    if any(not row["exists"] or row["kind"] == "missing" for row in expected_artifacts):
        raise TodoAcceptanceError("required artifact does not exist")
    if receipt["artifact_results"] != expected_artifacts:
        raise TodoAcceptanceError("required artifact content changed after acceptance")
    if reexecute_commands:
        fresh_results = _execute_commands(
            commands,
            workspace=workspace,
            timeout_seconds=timeout_seconds,
            state_guard=guarded_todo_state,
        )
        failures = [
            f"{row['command']} ({row['status']}, exit {row['exit_code']})"
            for row in fresh_results
            if row["status"] != "passed" or row["exit_code"] != 0
        ]
        if failures:
            raise TodoAcceptanceError(
                "fresh TODO acceptance command failed: " + "; ".join(failures)
            )
        # Recheck after execution so a validator cannot change the evidence it
        # is judging and still leave a card in the resolved state.
        if receipt["toolchain_digest"] != toolchain_digest(workspace):
            raise TodoAcceptanceError("locked toolchain changed during fresh validation")
        if receipt["implementation_surface_digest"] != implementation_surface_digest(workspace):
            raise TodoAcceptanceError(
                "implementation or validator surface changed during fresh validation"
            )
        refreshed_artifacts = [artifact_result(workspace, path) for path in artifacts]
        if receipt["artifact_results"] != refreshed_artifacts:
            raise TodoAcceptanceError(
                "required artifact content changed during fresh validation"
            )


def self_check(workspace: Path) -> None:
    """Exercise definition and artifact staleness without running subprocesses."""

    sample = {
        "id": "DWF-SELF-CHECK", "title": "self check", "status": "open",
        "validation_commands": ["python -c pass"],
        "required_artifact": ["pyproject.toml"], "evidence": [],
    }
    artifact = artifact_result(workspace, "pyproject.toml")
    receipt: dict[str, Any] = {
        "schema_version": "1.0.0",
        "todo_id": sample["id"], "todo_file": "agentic/todos/self-check.yaml",
        "todo_definition_digest": todo_definition_digest(sample),
        "toolchain_digest": toolchain_digest(workspace),
        "implementation_surface_digest": implementation_surface_digest(workspace),
        "started_at": "2026-07-21T00:00:00Z", "completed_at": "2026-07-21T00:00:01Z",
        "validation_results": [{
            "command": "python -c pass", "argv": [sys.executable, "-c", "pass"],
            "exit_code": 0, "status": "passed", "stdout_digest": canonical_digest(""),
            "stderr_digest": canonical_digest(""), "stdout_tail": "", "stderr_tail": "",
        }],
        "artifact_results": [artifact], "overall_status": "passed",
    }
    _seal_receipt(receipt)
    validate_payload(receipt, "todo_acceptance_receipt.schema.json")
    stale = copy.deepcopy(sample)
    stale["acceptance_criteria"] = ["new requirement"]
    if receipt["todo_definition_digest"] == todo_definition_digest(stale):
        raise TodoAcceptanceError("self-check failed to detect definition drift")
