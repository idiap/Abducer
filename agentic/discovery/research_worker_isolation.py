# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Strongest-available isolation and exact receipts for research workers.

The discovery runtime needs two truths at once.  A worker should be kept behind
the strongest local boundary that the host can actually enforce, while a local
process must never be relabelled as a cognitively independent evaluator.  This
module therefore combines four existing repository primitives:

* :class:`~agentic.discovery.budgets.ResourceGovernor` for deadlines, rlimits,
  bounded pipes, disk accounting, and whole-process-group termination;
* benchmark command sealing for exact executable and semantic dependency bytes;
* canonical discovery identities and schema validation; and
* immutable create-if-absent receipt publication.

On macOS it uses ``sandbox-exec`` with workspace-only writes, network denial,
and an explicitly disclosed host-read limitation.  On Linux it uses a probed Bubblewrap namespace when
available.  Otherwise it records process-group supervision as the strongest
available boundary and explicitly marks filesystem/network isolation
unavailable.  Every mode scrubs the inherited environment through ``env -i``.

Even a kernel-sandboxed success retains explicit nulls for hidden-input,
cognitive, and semantic independence: operating-system denial cannot prove
training-data independence, task authorship independence, or scientific value.
"""

from __future__ import annotations

import copy
import functools
import json
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Mapping, Sequence

from .benchmark_process import (
    BenchmarkIntegrityError,
    _load_json_object,
    _observe_command_authority,
    _pre_spawn_event,
    _require_live_command_authority,
    _seal_command,
    _top_level_content_digest,
    _validate_command_authority_observation,
    _validate_command_authority_structure,
    _write_immutable_json,
)
from .budgets import (
    BudgetExceeded,
    ResourceBudget,
    ResourceGovernor,
    complete_governed_process_environment,
    contained_path,
    minimal_replacement_environment,
    validate_v2_process_event,
)
from .contracts import (
    bytes_digest,
    canonical_digest,
    canonical_json,
    file_digest,
    stable_identifier,
    validate_identifier,
    validate_instance,
)


RECEIPT_SCHEMA = "research_worker_execution_receipt.schema.json"
ROLES = {"candidate", "high_risk", "formal_lens", "judge"}
OPERATIONS = {
    "candidate_generation",
    "high_risk_generation",
    "parallel_maturation",
    "formal_lens",
    "reflection",
    "blind_judgment",
    "convergence",
    "isolation_probe",
}
ROLE_OPERATIONS = {
    "candidate": {"candidate_generation", "parallel_maturation", "reflection", "isolation_probe"},
    "high_risk": {"high_risk_generation", "parallel_maturation", "isolation_probe"},
    "formal_lens": {"formal_lens", "isolation_probe"},
    "judge": {"blind_judgment", "convergence", "isolation_probe"},
}
EPistemic_NULL = "none_operational_execution_and_internal_calibration_only"
ISOLATION_REQUIREMENT_VERSION = 1
ISOLATION_BACKENDS = {
    "macos_sandbox_exec",
    "linux_bubblewrap",
    "process_group_only",
}


class ResearchWorkerIntegrityError(BenchmarkIntegrityError):
    """Raised when a worker request, receipt, or live authority fails closed."""


def _file_authority(path: Path | str) -> dict[str, Any]:
    resolved = Path(path).resolve(strict=True)
    if resolved.is_symlink() or not resolved.is_file():
        raise ResearchWorkerIntegrityError(f"worker authority is not a regular file: {path}")
    return {
        "canonical_path": str(resolved),
        "sha256": file_digest(resolved),
        "byte_length": resolved.stat().st_size,
    }


def _failure(stage: str, error_type: str, message: str) -> dict[str, str]:
    text = str(message) or error_type
    return {
        "stage": stage,
        "error_type": error_type,
        "message": text,
        "message_digest": bytes_digest(text.encode("utf-8", errors="replace")),
    }


def _quote_sandbox_path(path: Path | str) -> str:
    """Render an absolute path as one sandbox-profile string literal."""

    return json.dumps(str(Path(path).resolve()), ensure_ascii=True)


def _macos_profile(
    *,
    workspace: Path,
    run_directory: Path,
    python_executable: Path,
    worker_script: Path,
) -> str:
    """Return the strongest Seatbelt profile that executes the sealed CPython.

    The macOS dynamic loader and this standalone CPython abort under a portable
    content-read allowlist: runtime paths vary across Apple/uv installations and
    denied loader reads are not surfaced on stderr.  The executable profile
    therefore kernel-denies network and all writes outside the exact workspace,
    while leaving host reads open and typing hidden-input independence false.
    This is stronger and more truthful than claiming a non-executable allowlist.
    """
    workspace_filter = f"(subpath {_quote_sandbox_path(workspace)})"
    run_directory_filter = f"(subpath {_quote_sandbox_path(run_directory)})"
    return "\n".join(
        [
            "(version 1)",
            "(deny default)",
            "(allow process*)",
            "(allow signal (target self))",
            "(allow mach*)",
            "(allow ipc*)",
            "(allow sysctl*)",
            "(allow file-read*)",
            f"(deny file-read* {run_directory_filter})",
            f"(allow file-read* {workspace_filter})",
            f"(allow file-write* {workspace_filter} (literal \"/dev/null\"))",
            "(deny network*)",
        ]
    )


@functools.lru_cache(maxsize=1)
def _probe_macos_sandbox() -> tuple[Path | None, str, str | None]:
    candidate = Path("/usr/bin/sandbox-exec")
    if platform.system() != "Darwin" or not candidate.is_file() or not os.access(candidate, os.X_OK):
        return None, "unavailable", "sandbox-exec is not an executable on this host"
    try:
        probe = subprocess.run(
            [
                str(candidate),
                "-p",
                "(version 1) (allow default) (deny network*)",
                "/usr/bin/true",
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2.0,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return None, "failed", f"sandbox-exec probe failed: {type(exc).__name__}: {exc}"
    if probe.returncode != 0:
        detail = probe.stderr.decode("utf-8", errors="replace").strip() or f"exit {probe.returncode}"
        return None, "failed", f"sandbox-exec probe rejected execution: {detail}"
    return candidate.resolve(strict=True), "passed", None


@functools.lru_cache(maxsize=1)
def _probe_bubblewrap() -> tuple[Path | None, str, str | None]:
    if platform.system() != "Linux":
        return None, "unavailable", "Bubblewrap route applies only on Linux"
    resolved = shutil.which("bwrap")
    if not resolved:
        return None, "unavailable", "bwrap is not installed"
    candidate = Path(resolved).resolve(strict=True)
    try:
        probe = subprocess.run(
            [
                str(candidate),
                "--die-with-parent",
                "--new-session",
                "--unshare-all",
                "--ro-bind",
                "/",
                "/",
                "--dev-bind",
                "/dev",
                "/dev",
                "--proc",
                "/proc",
                "--",
                "/bin/true",
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=3.0,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return None, "failed", f"Bubblewrap probe failed: {type(exc).__name__}: {exc}"
    if probe.returncode != 0:
        detail = probe.stderr.decode("utf-8", errors="replace").strip() or f"exit {probe.returncode}"
        return None, "failed", f"Bubblewrap namespace unavailable: {detail}"
    return candidate, "passed", None


def strongest_available_isolation() -> dict[str, Any]:
    """Describe the strongest successfully probed local isolation backend."""

    sandbox, sandbox_status, sandbox_reason = _probe_macos_sandbox()
    if sandbox is not None:
        return {
            "backend": "macos_sandbox_exec",
            "executable": sandbox,
            "probe_status": sandbox_status,
            "fallback_reason": None,
        }
    bubblewrap, bubble_status, bubble_reason = _probe_bubblewrap()
    if bubblewrap is not None:
        return {
            "backend": "linux_bubblewrap",
            "executable": bubblewrap,
            "probe_status": bubble_status,
            "fallback_reason": None,
        }
    reasons = [
        reason
        for reason in (sandbox_reason, bubble_reason)
        if isinstance(reason, str) and reason
    ]
    statuses = {sandbox_status, bubble_status}
    return {
        "backend": "process_group_only",
        "executable": None,
        "probe_status": "failed" if "failed" in statuses else "unavailable",
        "fallback_reason": "; ".join(reasons) or "no kernel sandbox backend was detected",
    }


def build_isolation_requirement(
    backend: Mapping[str, Any], *, require_kernel_isolation: bool
) -> dict[str, Any]:
    """Bind the requested isolation floor and selected backend into identity."""

    selected_backend = backend.get("backend")
    probe_status = backend.get("probe_status")
    if selected_backend not in ISOLATION_BACKENDS:
        raise ResearchWorkerIntegrityError("unknown selected isolation backend")
    if probe_status not in {"passed", "unavailable", "failed"}:
        raise ResearchWorkerIntegrityError("unknown isolation backend probe status")
    core = {
        "schema_version": ISOLATION_REQUIREMENT_VERSION,
        "kernel_isolation_required": bool(require_kernel_isolation),
        "minimum_accepted_status": (
            "kernel_policy_enforced"
            if require_kernel_isolation
            else "strongest_available"
        ),
        "selected_backend": selected_backend,
        "selected_backend_probe_status": probe_status,
    }
    return {**core, "content_digest": canonical_digest(core)}


def validate_isolation_requirement(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Replay the closed execution-eligibility requirement in a worker request."""

    record = copy.deepcopy(dict(raw))
    required = {
        "schema_version",
        "kernel_isolation_required",
        "minimum_accepted_status",
        "selected_backend",
        "selected_backend_probe_status",
        "content_digest",
    }
    if set(record) != required:
        raise ResearchWorkerIntegrityError("worker isolation requirement is not closed")
    if (
        record["schema_version"] != ISOLATION_REQUIREMENT_VERSION
        or not isinstance(record["kernel_isolation_required"], bool)
        or record["selected_backend"] not in ISOLATION_BACKENDS
        or record["selected_backend_probe_status"]
        not in {"passed", "unavailable", "failed"}
        or record["minimum_accepted_status"]
        != (
            "kernel_policy_enforced"
            if record["kernel_isolation_required"]
            else "strongest_available"
        )
        or record["content_digest"]
        != canonical_digest(
            {key: value for key, value in record.items() if key != "content_digest"}
        )
    ):
        raise ResearchWorkerIntegrityError("worker isolation requirement is invalid")
    return record


def _clean_environment(workspace: Path) -> dict[str, str]:
    return minimal_replacement_environment(workspace)


def _environment_authority(
    *,
    launcher: Path,
    python_executable: Path,
    clean_environment: Mapping[str, str],
    observed_environment: Mapping[str, Any] | None,
) -> dict[str, Any]:
    observed_names: list[str] = []
    observed_digest: str | None = None
    observation_status = "not_observed"
    if observed_environment is not None:
        raw_names = observed_environment.get("names")
        raw_digest = observed_environment.get("values_digest")
        if isinstance(raw_names, list) and all(isinstance(item, str) for item in raw_names):
            observed_names = list(raw_names)
        if isinstance(raw_digest, str):
            observed_digest = raw_digest
        expected_digest = canonical_digest(dict(sorted(clean_environment.items())))
        observation_status = (
            "matched"
            if observed_names == sorted(clean_environment) and observed_digest == expected_digest
            else "mismatch"
        )
    core: dict[str, Any] = {
        "schema_version": 1,
        "launcher": _file_authority(launcher),
        "clear_environment": True,
        "allowed_names": sorted(clean_environment),
        "bindings": [
            {
                "name": name,
                "value_sha256": bytes_digest(value.encode("utf-8")),
                "plaintext_omitted_from_binding_row": True,
            }
            for name, value in sorted(clean_environment.items())
        ],
        "observation_status": observation_status,
        "observed_names": observed_names,
        "observed_values_digest": observed_digest,
        "secret_environment_inheritance": "denied_by_env_i_allowlist",
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine() or "unknown-machine",
        },
        "python": {
            "version": platform.python_version(),
            "executable": _file_authority(python_executable),
        },
    }
    return {**core, "content_digest": canonical_digest(core)}


def _isolation_command(
    *,
    backend: Mapping[str, Any],
    workspace: Path,
    run_directory: Path,
    python_executable: Path,
    worker_script: Path,
    launcher: Path,
    clean_environment: Mapping[str, str],
) -> tuple[list[str], str | None]:
    command = [str(launcher), "-i"]
    command.extend(f"{name}={value}" for name, value in sorted(clean_environment.items()))
    policy: str | None = None
    if backend["backend"] == "macos_sandbox_exec":
        policy = _macos_profile(
            workspace=workspace,
            run_directory=run_directory,
            python_executable=python_executable,
            worker_script=worker_script,
        )
        command.extend([str(backend["executable"]), "-p", policy])
    elif backend["backend"] == "linux_bubblewrap":
        policy = canonical_json(
            {
                "namespace": "unshare_all_including_network",
                "root": "read_only_host_root",
                "workspace": "read_write_exact_attempt_root",
                "process": "die_with_parent_new_session",
            }
        ).decode("utf-8")
        command.extend(
            [
                str(backend["executable"]),
                "--die-with-parent",
                "--new-session",
                "--unshare-all",
                "--ro-bind",
                "/",
                "/",
                "--dev-bind",
                "/dev",
                "/dev",
                "--proc",
                "/proc",
                "--bind",
                str(workspace),
                str(workspace),
                "--chdir",
                str(workspace),
                "--",
            ]
        )
    command.extend([str(python_executable), "-I", "-B", str(worker_script)])
    return command, policy


def _isolation_assurance(
    *, backend: Mapping[str, Any], policy: str | None
) -> dict[str, Any]:
    kernel = backend["backend"] != "process_group_only"
    sibling_read_denied = backend["backend"] == "macos_sandbox_exec"
    executable = (
        _file_authority(backend["executable"])
        if backend.get("executable") is not None
        else None
    )
    mechanism = {
        "backend": backend["backend"],
        "executable": executable,
        "probe_status": backend["probe_status"],
        "policy_text": policy,
        "policy_digest": bytes_digest(policy.encode("utf-8")) if policy is not None else None,
        "fallback_reason": backend.get("fallback_reason"),
    }
    core: dict[str, Any] = {
        "schema_version": 1,
        "status": "kernel_policy_enforced" if kernel else "process_only_strongest_available",
        "mechanism": mechanism,
        "deny_by_construction": kernel,
        "channels": {
            "filesystem_read": (
                "kernel_sibling_run_data_denied_host_read_scope_unrestricted"
                if sibling_read_denied
                else "host_read_scope_unrestricted"
            ),
            "filesystem_write": "kernel_workspace_only" if kernel else "protocol_workspace_only",
            "network": "kernel_denied" if kernel else "unavailable_no_kernel_network_policy",
            "environment": "env_i_allowlist_enforced",
            "process_lifecycle": "isolated_session_process_group_supervised",
            "undeclared_access_audit": "unavailable_no_complete_syscall_trace",
        },
        "hidden_input_independence_authorized": False,
        "cognitive_independence_authorized": False,
        "semantic_independence_authorized": False,
        "external_efficacy_eligible": False,
        "limitation": (
            "Kernel policy constrains network and writes; the macOS route also denies reads from "
            "sibling run data while unrelated host reads remain open. Task authorship, training "
            "exposure, semantic independence, and complete syscall provenance are not established."
            if kernel
            else "Only environment scrubbing, cwd containment, rlimits, and process-group lifecycle "
            "supervision are available; host reads and network access are not kernel denied."
        ),
    }
    return {**core, "content_digest": canonical_digest(core)}


def _workspace_record(
    run_directory: Path, workspace_ref: str, invocation_id: str
) -> dict[str, Any]:
    workspace = contained_path(run_directory, *Path(workspace_ref).parts)
    core = {
        "run_directory": str(run_directory),
        "workspace_ref": workspace_ref,
        "resolved_path": str(workspace),
        "invocation_id": invocation_id,
    }
    return {**core, "workspace_digest": canonical_digest(core)}


def _authority_boundaries() -> dict[str, Any]:
    return {
        "epistemic_effect": EPistemic_NULL,
        "publication_authorized": False,
        "advantage_inference_authorized": False,
        "creativity_authorized": False,
        "conceptual_depth_authorized": False,
        "unification_power_authorized": False,
        "physics_value_authorized": False,
        "truth_authorized": False,
        "theorem_authorized": False,
        "continuum_authorized": False,
        "hidden_input_independence_authorized": False,
        "cognitive_independence_authorized": False,
        "semantic_independence_authorized": False,
        "external_human_authority_status": "unavailable",
    }


def _validate_worker_output(operation: str, output: Any) -> None:
    if not isinstance(output, Mapping) or output.get("output_kind") != operation:
        raise ResearchWorkerIntegrityError("worker output kind differs from the invoked operation")
    if operation == "formal_lens":
        execution = output.get("formal_execution")
        records = output.get("records")
        if not isinstance(execution, Mapping) or not isinstance(records, list) or not records:
            raise ResearchWorkerIntegrityError("formal-lens output lacks executable finite evidence")
        if any(
            execution.get(field) is not False
            for field in (
                "theorem_authorized",
                "continuum_authorized",
                "physics_value_authorized",
                "conceptual_advantage_authorized",
            )
        ):
            raise ResearchWorkerIntegrityError("formal-lens worker overstates its finite authority")
        model_projection = [
            {
                "task_id": row.get("task_id"),
                "category": row.get("category_check"),
                "hott": row.get("hott_check"),
            }
            for row in records
        ]
        witness_projection = [
            {
                "task_id": row.get("task_id"),
                "category_mismatches": (
                    row["category_check"].get("mismatch_elements", [])
                    if isinstance(row.get("category_check"), Mapping)
                    else []
                ),
                "hott_round_trip": (
                    row["hott_check"].get("round_trip_holds")
                    if isinstance(row.get("hott_check"), Mapping)
                    else None
                ),
            }
            for row in records
        ]
        if (
            execution.get("model_digest") != canonical_digest(model_projection)
            or execution.get("witness_digest") != canonical_digest(witness_projection)
        ):
            raise ResearchWorkerIntegrityError("formal-lens model or witness digest mismatch")
    if operation == "blind_judgment":
        authority = output.get("judge_authority")
        if not isinstance(authority, Mapping) or authority.get("authority_distinct_status") != "unavailable":
            raise ResearchWorkerIntegrityError("local blind judge invented authority-distinct evidence")
        if authority.get("cognitive_independence_authorized") is not False:
            raise ResearchWorkerIntegrityError("local blind judge invented cognitive independence")
    if operation == "convergence":
        for row in output.get("records", []):
            if row.get("promotion_authorized") is not False or row.get("truth_authorized") is not False:
                raise ResearchWorkerIntegrityError("internal convergence attempted promotion")


def _descriptor_is_member(authority: Mapping[str, Any], descriptor: Mapping[str, Any]) -> bool:
    path = descriptor.get("canonical_path")
    digest = descriptor.get("sha256")
    length = descriptor.get("byte_length")
    rows = [authority.get("executable"), *authority.get("dependencies", [])]
    return any(
        isinstance(row, Mapping)
        and row.get("canonical_path") == path
        and row.get("sha256") == digest
        and row.get("byte_length") == length
        for row in rows
    )


def _validate_research_worker_receipt(
    raw: Mapping[str, Any],
    *,
    receipt_path: Path | str | None = None,
    require_live_authority: bool = True,
    required_kernel_isolation: bool | None = None,
    historical_decode_only: bool = False,
) -> dict[str, Any]:
    """Replay one receipt, including exact bytes and live executable authority."""

    receipt = copy.deepcopy(dict(raw))
    if historical_decode_only:
        if receipt.get("schema_version") != 1 or require_live_authority:
            raise ResearchWorkerIntegrityError(
                "historical research decoding accepts only legacy v1 without live authority"
            )
    elif receipt.get("schema_version") != 2:
        raise ResearchWorkerIntegrityError(
            "legacy research worker receipts are decode-only and cannot carry current authority"
        )
    validate_instance(receipt, RECEIPT_SCHEMA, cache_json_structure=True)
    if receipt["content_digest"] != _top_level_content_digest(receipt):
        raise ResearchWorkerIntegrityError("research worker receipt content digest mismatch")
    expected_invocation = stable_identifier(
        "research-worker-invocation",
        receipt["study_id"],
        receipt["role"],
        receipt["operation"],
        receipt["request_sha256"],
    )
    expected_receipt = stable_identifier(
        "research-worker-receipt",
        receipt["study_id"],
        receipt["role"],
        expected_invocation,
    )
    if receipt["invocation_id"] != expected_invocation or receipt["receipt_id"] != expected_receipt:
        raise ResearchWorkerIntegrityError("research worker receipt identity mismatch")
    if receipt["operation"] not in ROLE_OPERATIONS[receipt["role"]]:
        raise ResearchWorkerIntegrityError("research worker role/operation mismatch")

    request_bytes = canonical_json(receipt["request_payload"]) + b"\n"
    if (
        receipt["request_byte_length"] != len(request_bytes)
        or receipt["request_sha256"] != bytes_digest(request_bytes)
        or receipt["request_payload"]["payload_digest"]
        != canonical_digest(receipt["request_payload"]["payload"])
    ):
        raise ResearchWorkerIntegrityError("research worker request bytes are not exact")
    request = receipt["request_payload"]
    if (
        request["study_id"] != receipt["study_id"]
        or request["role"] != receipt["role"]
        or request["operation"] != receipt["operation"]
    ):
        raise ResearchWorkerIntegrityError("research worker request envelope differs from receipt")
    requirement_raw = request.get("isolation_requirement")
    requirement = (
        validate_isolation_requirement(requirement_raw)
        if isinstance(requirement_raw, Mapping)
        else None
    )
    if receipt["schema_version"] == 2 and requirement is None:
        raise ResearchWorkerIntegrityError(
            "current research worker request lacks its isolation requirement"
        )
    if requirement is not None:
        expected_request_nonce = stable_identifier(
            "research-worker-request",
            receipt["study_id"],
            receipt["role"],
            receipt["operation"],
            request["invocation_context"],
            request["payload"],
            requirement,
            request["fault_mode"],
        )
        if request["request_nonce"] != expected_request_nonce:
            raise ResearchWorkerIntegrityError(
                "research worker request nonce is not derived from its exact inputs"
            )
    if required_kernel_isolation is not None and (
        requirement is None
        or requirement["kernel_isolation_required"]
        is not bool(required_kernel_isolation)
    ):
        raise ResearchWorkerIntegrityError(
            "research worker receipt does not satisfy the required isolation identity"
        )

    workspace = receipt["workspace"]
    run_directory = Path(workspace["run_directory"])
    if not run_directory.is_absolute() or run_directory.resolve() != run_directory:
        raise ResearchWorkerIntegrityError("research worker run directory is not canonical")
    expected_workspace_ref = f"workspaces/{receipt['role']}/{receipt['invocation_id']}"
    expected_workspace = _workspace_record(
        run_directory, expected_workspace_ref, receipt["invocation_id"]
    )
    if workspace != expected_workspace:
        raise ResearchWorkerIntegrityError("research worker workspace binding mismatch")
    workspace_path = Path(workspace["resolved_path"])
    if not workspace_path.is_dir() or workspace_path.is_symlink():
        raise ResearchWorkerIntegrityError("research worker workspace is unavailable")
    expected_ref = f"receipts/{receipt['role']}/{receipt['receipt_id']}.json"
    if receipt["receipt_ref"] != expected_ref:
        raise ResearchWorkerIntegrityError("research worker receipt reference mismatch")
    if receipt_path is not None:
        expected_path = contained_path(run_directory, *Path(expected_ref).parts)
        actual_path = Path(receipt_path)
        if actual_path.resolve() != expected_path or actual_path.is_symlink():
            raise ResearchWorkerIntegrityError("research worker receipt path mismatch")

    _validate_command_authority_structure(receipt["command_authority"])
    _validate_command_authority_observation(
        receipt["command_authority"], receipt["command_authority_observation"]
    )
    if receipt["outcome_status"] == "accepted":
        if receipt["command_authority_observation"]["status"] != "exact_match":
            raise ResearchWorkerIntegrityError("accepted worker lacks exact command authority")
        if require_live_authority:
            _require_live_command_authority(receipt["command_authority"])

    environment = receipt["environment_authority"]
    if environment["content_digest"] != canonical_digest(
        {key: value for key, value in environment.items() if key != "content_digest"}
    ):
        raise ResearchWorkerIntegrityError("research worker environment authority digest mismatch")
    if not _descriptor_is_member(receipt["command_authority"], environment["launcher"]):
        raise ResearchWorkerIntegrityError("environment launcher is not command-bound")
    if not _descriptor_is_member(
        receipt["command_authority"], environment["python"]["executable"]
    ):
        raise ResearchWorkerIntegrityError("Python executable is not command-bound")
    binding_names = [row["name"] for row in environment["bindings"]]
    if binding_names != sorted(environment["allowed_names"]):
        raise ResearchWorkerIntegrityError("environment bindings are not exact or ordered")
    expected_clean_environment = minimal_replacement_environment(
        workspace_path,
        create_temporary=False,
    )
    expected_environment_bindings = [
        {
            "name": name,
            "value_sha256": bytes_digest(value.encode("utf-8")),
            "plaintext_omitted_from_binding_row": True,
        }
        for name, value in sorted(expected_clean_environment.items())
    ]
    if (
        environment["allowed_names"] != sorted(expected_clean_environment)
        or environment["bindings"] != expected_environment_bindings
        or environment["clear_environment"] is not True
    ):
        raise ResearchWorkerIntegrityError(
            "research worker environment authority differs from the exact replacement policy"
        )
    if (
        environment["platform"]
        != {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine() or "unknown-machine",
        }
        or environment["python"]["version"] != platform.python_version()
    ):
        raise ResearchWorkerIntegrityError(
            "research worker environment platform observation differs from the replay host"
        )

    isolation = receipt["isolation_assurance"]
    if isolation["content_digest"] != canonical_digest(
        {key: value for key, value in isolation.items() if key != "content_digest"}
    ):
        raise ResearchWorkerIntegrityError("isolation assurance digest mismatch")
    mechanism = isolation["mechanism"]
    if mechanism["policy_text"] is None:
        if mechanism["policy_digest"] is not None or mechanism["backend"] != "process_group_only":
            raise ResearchWorkerIntegrityError("isolation policy absence is inconsistent")
    elif mechanism["policy_digest"] != bytes_digest(
        mechanism["policy_text"].encode("utf-8")
    ):
        raise ResearchWorkerIntegrityError("isolation policy digest mismatch")
    if mechanism["executable"] is not None and not _descriptor_is_member(
        receipt["command_authority"], mechanism["executable"]
    ):
        raise ResearchWorkerIntegrityError("isolation executable is not command-bound")
    backend_name = mechanism["backend"]
    kernel = backend_name != "process_group_only"
    if kernel:
        expected_system = "Darwin" if backend_name == "macos_sandbox_exec" else "Linux"
        if (
            backend_name not in {"macos_sandbox_exec", "linux_bubblewrap"}
            or platform.system() != expected_system
            or mechanism["probe_status"] != "passed"
            or mechanism["executable"] is None
            or mechanism["policy_text"] is None
            or mechanism["fallback_reason"] is not None
        ):
            raise ResearchWorkerIntegrityError(
                "kernel isolation mechanism discriminants are inconsistent"
            )
    elif (
        mechanism["executable"] is not None
        or mechanism["policy_text"] is not None
        or mechanism["probe_status"] not in {"unavailable", "failed"}
        or not isinstance(mechanism["fallback_reason"], str)
        or not mechanism["fallback_reason"]
    ):
        raise ResearchWorkerIntegrityError(
            "process-only isolation mechanism discriminants are inconsistent"
        )
    if (
        isolation["deny_by_construction"] is not kernel
        or (isolation["status"] == "kernel_policy_enforced") is not kernel
        or isolation["channels"]["filesystem_read"]
        != (
            "kernel_sibling_run_data_denied_host_read_scope_unrestricted"
            if mechanism["backend"] == "macos_sandbox_exec"
            else "host_read_scope_unrestricted"
        )
        or isolation["channels"]["network"]
        != ("kernel_denied" if kernel else "unavailable_no_kernel_network_policy")
    ):
        raise ResearchWorkerIntegrityError("isolation assurance overstates its mechanism")
    if requirement is not None:
        if (
            requirement["selected_backend"] != mechanism["backend"]
            or requirement["selected_backend_probe_status"]
            != mechanism["probe_status"]
        ):
            raise ResearchWorkerIntegrityError(
                "isolation assurance differs from the request identity"
            )
        if requirement["kernel_isolation_required"] and not kernel:
            if (
                receipt["outcome_status"] == "accepted"
                or receipt["protocol_status"] != "isolation_unavailable"
            ):
                raise ResearchWorkerIntegrityError(
                    "kernel-required request was accepted without kernel isolation"
                )

    command_argv = receipt["command_authority"]["argv"]
    python_path = environment["python"]["executable"]["canonical_path"]
    if len(command_argv) < 4 or command_argv[-4:-1] != [python_path, "-I", "-B"]:
        raise ResearchWorkerIntegrityError(
            "research worker command lacks the exact isolated Python tail"
        )
    worker_script_path = command_argv[-1]
    authority_rows = [
        receipt["command_authority"]["executable"],
        *receipt["command_authority"]["dependencies"],
    ]
    if not any(
        row.get("canonical_path") == worker_script_path for row in authority_rows
    ):
        raise ResearchWorkerIntegrityError(
            "research worker script is not command-authority bound"
        )
    backend_for_replay = {
        "backend": backend_name,
        "executable": (
            Path(mechanism["executable"]["canonical_path"])
            if mechanism["executable"] is not None
            else None
        ),
        "probe_status": mechanism["probe_status"],
        "fallback_reason": mechanism["fallback_reason"],
    }
    expected_command, expected_policy = _isolation_command(
        backend=backend_for_replay,
        workspace=workspace_path,
        run_directory=run_directory,
        python_executable=Path(python_path),
        worker_script=Path(worker_script_path),
        launcher=Path(environment["launcher"]["canonical_path"]),
        clean_environment=expected_clean_environment,
    )
    if command_argv != expected_command or mechanism["policy_text"] != expected_policy:
        raise ResearchWorkerIntegrityError(
            "research worker command differs from the exact env-i/backend policy"
        )

    event = receipt["process_event"]
    resource_receipt = receipt["resource_receipt"]
    if receipt["schema_version"] == 2:
        expected_process_environment = complete_governed_process_environment(
            expected_clean_environment,
            deadline=resource_receipt["deadline"],
            budget=resource_receipt["budget"],
        )
        try:
            validate_v2_process_event(
                event,
                accepted=receipt["outcome_status"] == "accepted",
                expected_workspace=workspace_path,
                expected_replacement_environment=expected_process_environment,
                require_live_execution_authority=require_live_authority,
            )
        except ValueError as exc:
            raise ResearchWorkerIntegrityError(
                f"research worker v2 process evidence is invalid: {exc}"
            ) from exc
    if (
        event["command"] != receipt["command_authority"]["argv"]
        or event["stdin_bytes"] != receipt["request_byte_length"]
        or event["stdin_sha256"] != receipt["request_sha256"]
        or resource_receipt["events"] != [event]
        or resource_receipt["status"] != receipt["process_status"]
        or receipt["budget_digest"] != canonical_digest(resource_receipt["budget"])
        or receipt["resource_receipt_digest"] != canonical_digest(resource_receipt)
    ):
        raise ResearchWorkerIntegrityError("research worker process/resource binding mismatch")
    if receipt["outcome_status"] == "accepted" and (
        receipt["process_status"] != "succeeded"
        or receipt["protocol_status"] != "accepted"
        or event["status"] != "succeeded"
        or event["returncode"] != 0
        or event["termination"] is not None
        or event["descendant_leak_detected"] is not False
    ):
        raise ResearchWorkerIntegrityError(
            "accepted research worker is not a normally exited terminal process group"
        )
    if resource_receipt["resource_measurement"]["disk_bytes"].get("accounting_root") != str(
        workspace_path
    ):
        raise ResearchWorkerIntegrityError("research worker accounting root mismatch")

    response = receipt["response_payload"]
    if receipt["outcome_status"] == "accepted":
        if not isinstance(response, Mapping) or receipt["failure"] is not None:
            raise ResearchWorkerIntegrityError("accepted worker response/failure shape is invalid")
        response_bytes = canonical_json(response) + b"\n"
        if (
            receipt["response_byte_length"] != len(response_bytes)
            or receipt["response_sha256"] != bytes_digest(response_bytes)
            or event["stdout_bytes"] != len(response_bytes)
            or event["stdout_sha256"] != bytes_digest(response_bytes)
            or event["stdout"] != response_bytes.decode("utf-8")
        ):
            raise ResearchWorkerIntegrityError("research worker response bytes are not exact")
        if (
            response["role"] != receipt["role"]
            or response["operation"] != receipt["operation"]
            or response["request_nonce"] != request["request_nonce"]
        ):
            raise ResearchWorkerIntegrityError("research worker response envelope mismatch")
        observation = response["environment_observation"]
        expected_observed_values_digest = canonical_digest(
            dict(sorted(expected_clean_environment.items()))
        )
        if (
            environment["observation_status"] != "matched"
            or environment["observed_names"] != observation["names"]
            or environment["observed_values_digest"] != observation["values_digest"]
            or observation["names"] != sorted(expected_clean_environment)
            or observation["values_digest"] != expected_observed_values_digest
            or observation["working_directory"] != str(workspace_path)
        ):
            raise ResearchWorkerIntegrityError("research worker environment observation mismatch")
        _validate_worker_output(receipt["operation"], response["output"])
    else:
        if any(
            receipt[field] is not None
            for field in ("response_payload", "response_byte_length", "response_sha256")
        ) or receipt["failure"] is None:
            raise ResearchWorkerIntegrityError("failed worker retained accepted response bytes")
        failure = receipt["failure"]
        if failure["message_digest"] != bytes_digest(
            failure["message"].encode("utf-8", errors="replace")
        ):
            raise ResearchWorkerIntegrityError("research worker failure digest mismatch")
    if receipt["authority_boundaries"] != _authority_boundaries():
        raise ResearchWorkerIntegrityError("research worker receipt overstates epistemic authority")
    return receipt


def validate_research_worker_receipt(
    raw: Mapping[str, Any],
    *,
    receipt_path: Path | str | None = None,
    require_live_authority: bool = True,
    required_kernel_isolation: bool | None = None,
) -> dict[str, Any]:
    """Validate one current v2 research receipt for authority-bearing reuse."""

    return _validate_research_worker_receipt(
        raw,
        receipt_path=receipt_path,
        require_live_authority=require_live_authority,
        required_kernel_isolation=required_kernel_isolation,
        historical_decode_only=False,
    )


def decode_historical_research_worker_receipt(
    raw: Mapping[str, Any],
    *,
    receipt_path: Path | str | None = None,
) -> dict[str, Any]:
    """Decode one immutable v1 receipt without granting current authority."""

    return _validate_research_worker_receipt(
        raw,
        receipt_path=receipt_path,
        require_live_authority=False,
        required_kernel_isolation=None,
        historical_decode_only=True,
    )


class ResearchWorkerAdapter:
    """Execute immutable worker attempts and return receipts for every outcome."""

    def __init__(
        self,
        *,
        study_id: str,
        run_root: Path | str,
        worker_script: Path | str | None = None,
        approved_dependency_paths: Sequence[Path | str] = (),
        require_kernel_isolation: bool = False,
        input_limit_bytes: int = 2 * 1024 * 1024,
        stdout_limit_bytes: int = 4 * 1024 * 1024,
        stderr_limit_bytes: int = 256 * 1024,
    ) -> None:
        validate_identifier(study_id, "study_id")
        self.study_id = study_id
        self.run_root = Path(run_root).resolve()
        self.run_directory = contained_path(self.run_root, study_id)
        self.run_directory.mkdir(parents=True, exist_ok=True)
        root = Path(__file__).resolve().parents[2]
        self.worker_script = (
            Path(worker_script).resolve(strict=True)
            if worker_script is not None
            else (root / "agentic/scripts/run_matched_discovery_worker.py").resolve(strict=True)
        )
        self.python_executable = Path(sys.executable).resolve(strict=True)
        launcher_raw = shutil.which("env") or "/usr/bin/env"
        self.launcher = Path(launcher_raw).resolve(strict=True)
        self.backend = strongest_available_isolation()
        self.require_kernel_isolation = bool(require_kernel_isolation)
        self.input_limit_bytes = int(input_limit_bytes)
        self.stdout_limit_bytes = int(stdout_limit_bytes)
        self.stderr_limit_bytes = int(stderr_limit_bytes)
        if min(self.input_limit_bytes, self.stdout_limit_bytes, self.stderr_limit_bytes) <= 0:
            raise ValueError("worker byte limits must be positive")
        local_dependencies = [
            Path(__file__).resolve(),
            root / "agentic/discovery/budgets.py",
            root / "agentic/discovery/contracts.py",
            root / "agentic/discovery/benchmark_process.py",
            root / "agentic/spec/research_worker_execution_receipt.schema.json",
            *[Path(path) for path in approved_dependency_paths],
        ]
        self.approved_dependency_paths = tuple(path.resolve(strict=True) for path in local_dependencies)

    @staticmethod
    def default_budget() -> dict[str, Any]:
        """Return one exact budget profile used by all matched study arms."""

        return {
            "budget_id": "matched-research-worker-budget.v1",
            "wall_time_seconds": 5.0,
            "grace_period_seconds": 0.2,
            "cpu_seconds": 5.0,
            "memory_bytes": 256 * 1024 * 1024,
            "disk_bytes": 8 * 1024 * 1024,
            "network_bytes": 0,
            "token_count": 0,
            "request_count": 0,
            "cost_usd": 0.0,
            "absolute_deadline": None,
        }

    def _paths(self, role: str, invocation_id: str) -> tuple[str, Path, str, Path]:
        receipt_id = stable_identifier(
            "research-worker-receipt", self.study_id, role, invocation_id
        )
        receipt_ref = f"receipts/{role}/{receipt_id}.json"
        receipt_path = contained_path(self.run_directory, *Path(receipt_ref).parts)
        workspace_ref = f"workspaces/{role}/{invocation_id}"
        workspace = contained_path(self.run_directory, *Path(workspace_ref).parts)
        return receipt_ref, receipt_path, workspace_ref, workspace

    def _persist(
        self,
        *,
        role: str,
        operation: str,
        invocation_id: str,
        request: Mapping[str, Any],
        request_bytes: bytes,
        receipt_ref: str,
        receipt_path: Path,
        workspace_record: Mapping[str, Any],
        command_authority: Mapping[str, Any],
        command_observation: Mapping[str, Any],
        environment_authority: Mapping[str, Any],
        isolation_assurance: Mapping[str, Any],
        governor: ResourceGovernor,
        event: Mapping[str, Any],
        process_status: str,
        protocol_status: str,
        outcome_status: str,
        response: Mapping[str, Any] | None,
        failure: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        if not governor.events or governor.events[-1] != event:
            governor.events.append(dict(event))
        resource_receipt = governor.receipt(process_status)
        response_bytes = canonical_json(response) + b"\n" if response is not None else None
        core: dict[str, Any] = {
            "schema_version": 2 if event.get("event_schema_version") == 2 else 1,
            "receipt_id": stable_identifier(
                "research-worker-receipt", self.study_id, role, invocation_id
            ),
            "receipt_ref": receipt_ref,
            "study_id": self.study_id,
            "role": role,
            "operation": operation,
            "invocation_id": invocation_id,
            "request_payload": copy.deepcopy(dict(request)),
            "request_byte_length": len(request_bytes),
            "request_sha256": bytes_digest(request_bytes),
            "response_payload": copy.deepcopy(dict(response)) if response is not None else None,
            "response_byte_length": len(response_bytes) if response_bytes is not None else None,
            "response_sha256": bytes_digest(response_bytes) if response_bytes is not None else None,
            "command_authority": copy.deepcopy(dict(command_authority)),
            "command_authority_observation": copy.deepcopy(dict(command_observation)),
            "environment_authority": copy.deepcopy(dict(environment_authority)),
            "isolation_assurance": copy.deepcopy(dict(isolation_assurance)),
            "workspace": copy.deepcopy(dict(workspace_record)),
            "budget_digest": canonical_digest(resource_receipt["budget"]),
            "process_status": process_status,
            "protocol_status": protocol_status,
            "outcome_status": outcome_status,
            "process_event": copy.deepcopy(dict(event)),
            "resource_receipt": resource_receipt,
            "resource_receipt_digest": canonical_digest(resource_receipt),
            "failure": copy.deepcopy(dict(failure)) if failure is not None else None,
            "authority_boundaries": _authority_boundaries(),
        }
        receipt = {**core, "content_digest": canonical_digest(core)}
        validate_instance(receipt, RECEIPT_SCHEMA, cache_json_structure=True)
        _write_immutable_json(receipt_path, receipt)
        return validate_research_worker_receipt(
            _load_json_object(receipt_path),
            receipt_path=receipt_path,
            require_live_authority=outcome_status == "accepted",
            required_kernel_isolation=bool(
                request["isolation_requirement"]["kernel_isolation_required"]
            ),
        )

    def invoke(
        self,
        *,
        role: str,
        operation: str,
        invocation_context: Mapping[str, Any],
        payload: Mapping[str, Any],
        budget: Mapping[str, Any] | None = None,
        fault_mode: str | None = None,
    ) -> dict[str, Any]:
        """Run one worker and return an immutable success or failure receipt."""

        if role not in ROLES or operation not in ROLE_OPERATIONS.get(role, set()):
            raise ResearchWorkerIntegrityError("invalid research worker role/operation")
        if not isinstance(invocation_context, Mapping) or not isinstance(payload, Mapping):
            raise ResearchWorkerIntegrityError("worker context and payload must be objects")
        if fault_mode not in {None, "exit_nonzero", "invalid_json", "hang"}:
            raise ResearchWorkerIntegrityError("unknown worker fault mode")
        isolation_requirement = build_isolation_requirement(
            self.backend,
            require_kernel_isolation=self.require_kernel_isolation,
        )
        request_nonce = stable_identifier(
            "research-worker-request",
            self.study_id,
            role,
            operation,
            dict(invocation_context),
            dict(payload),
            isolation_requirement,
            fault_mode,
        )
        request = {
            "schema_version": 1,
            "study_id": self.study_id,
            "role": role,
            "operation": operation,
            "request_nonce": request_nonce,
            "invocation_context": copy.deepcopy(dict(invocation_context)),
            "payload": copy.deepcopy(dict(payload)),
            "payload_digest": canonical_digest(payload),
            "isolation_requirement": isolation_requirement,
            "fault_mode": fault_mode,
        }
        request_bytes = canonical_json(request) + b"\n"
        request_sha256 = bytes_digest(request_bytes)
        invocation_id = stable_identifier(
            "research-worker-invocation",
            self.study_id,
            role,
            operation,
            request_sha256,
        )
        receipt_ref, receipt_path, workspace_ref, workspace = self._paths(role, invocation_id)
        if receipt_path.exists():
            existing = validate_research_worker_receipt(
                _load_json_object(receipt_path),
                receipt_path=receipt_path,
                required_kernel_isolation=self.require_kernel_isolation,
            )
            if existing["request_payload"] != request:
                raise ResearchWorkerIntegrityError("idempotent worker invocation request changed")
            return existing

        workspace.mkdir(parents=True, exist_ok=True)
        clean_environment = _clean_environment(workspace)
        command, policy = _isolation_command(
            backend=self.backend,
            workspace=workspace,
            run_directory=self.run_directory,
            python_executable=self.python_executable,
            worker_script=self.worker_script,
            launcher=self.launcher,
            clean_environment=clean_environment,
        )
        command, command_authority = _seal_command(command, self.approved_dependency_paths)
        isolation_assurance = _isolation_assurance(backend=self.backend, policy=policy)
        workspace_record = _workspace_record(self.run_directory, workspace_ref, invocation_id)
        effective_budget = ResourceBudget.from_mapping(budget or self.default_budget())
        governor = ResourceGovernor(
            effective_budget,
            run_directory=workspace,
            allowed_working_directory=workspace,
            capture_limit_bytes=max(self.stdout_limit_bytes, self.stderr_limit_bytes),
            disk_sample_interval_seconds=0.01,
        )
        pre_observation = _observe_command_authority(command_authority)
        expected_environment = _environment_authority(
            launcher=self.launcher,
            python_executable=self.python_executable,
            clean_environment=clean_environment,
            observed_environment=None,
        )

        pre_failure: dict[str, Any] | None = None
        pre_protocol: str | None = None
        if pre_observation["status"] != "exact_match":
            pre_failure = _failure(
                "command_authority",
                "CommandAuthorityMismatch",
                "sealed worker executable or dependency differs before spawn",
            )
            pre_protocol = "authority_mismatch"
        elif self.require_kernel_isolation and self.backend["backend"] == "process_group_only":
            pre_failure = _failure(
                "isolation_selection",
                "KernelIsolationUnavailable",
                str(self.backend["fallback_reason"]),
            )
            pre_protocol = "isolation_unavailable"
        if pre_failure is not None:
            event = _pre_spawn_event(
                role="worker",
                command=command,
                request_bytes=request_bytes,
                input_limit_bytes=self.input_limit_bytes,
                stdout_limit_bytes=self.stdout_limit_bytes,
                stderr_limit_bytes=self.stderr_limit_bytes,
                governor=governor,
                status="worker_failed",
                failure=pre_failure,
            )
            return self._persist(
                role=role,
                operation=operation,
                invocation_id=invocation_id,
                request=request,
                request_bytes=request_bytes,
                receipt_ref=receipt_ref,
                receipt_path=receipt_path,
                workspace_record=workspace_record,
                command_authority=command_authority,
                command_observation=pre_observation,
                environment_authority=expected_environment,
                isolation_assurance=isolation_assurance,
                governor=governor,
                event=event,
                process_status="worker_failed",
                protocol_status=str(pre_protocol),
                outcome_status="operational_failure",
                response=None,
                failure=pre_failure,
            )

        try:
            event = governor.run_process(
                command,
                cwd=workspace,
                replacement_environment=clean_environment,
                role="worker",
                input_bytes=request_bytes,
                input_limit_bytes=self.input_limit_bytes,
                stdout_limit_bytes=self.stdout_limit_bytes,
                stderr_limit_bytes=self.stderr_limit_bytes,
            )
        except (OSError, ValueError, BudgetExceeded, subprocess.SubprocessError) as exc:
            status = exc.status if isinstance(exc, BudgetExceeded) else "worker_failed"
            failure = _failure("pre_spawn_or_launch", type(exc).__name__, str(exc))
            event = _pre_spawn_event(
                role="worker",
                command=command,
                request_bytes=request_bytes,
                input_limit_bytes=self.input_limit_bytes,
                stdout_limit_bytes=self.stdout_limit_bytes,
                stderr_limit_bytes=self.stderr_limit_bytes,
                governor=governor,
                status=status,
                failure=failure,
            )
            return self._persist(
                role=role,
                operation=operation,
                invocation_id=invocation_id,
                request=request,
                request_bytes=request_bytes,
                receipt_ref=receipt_ref,
                receipt_path=receipt_path,
                workspace_record=workspace_record,
                command_authority=command_authority,
                command_observation=pre_observation,
                environment_authority=expected_environment,
                isolation_assurance=isolation_assurance,
                governor=governor,
                event=event,
                process_status=status,
                protocol_status="authority_or_launch_failed",
                outcome_status="operational_failure",
                response=None,
                failure=failure,
            )

        post_observation = _observe_command_authority(command_authority)
        process_status = str(event.get("status") or "worker_failed")
        protocol_status = "accepted"
        outcome_status = "accepted"
        response: Mapping[str, Any] | None = None
        failure: Mapping[str, Any] | None = None
        observed_environment: Mapping[str, Any] | None = None
        if post_observation["status"] != "exact_match":
            process_status = "worker_failed"
            protocol_status = "authority_mismatch"
            outcome_status = "operational_failure"
            failure = _failure(
                "command_authority",
                "CommandAuthorityMismatch",
                "sealed worker authority changed during execution",
            )
        elif process_status != "succeeded":
            protocol_status = (
                process_status
                if process_status in {"input_exhausted", "output_exhausted"}
                else "process_failed"
            )
            outcome_status = "operational_failure"
            failure = _failure(
                "process_execution", process_status, str(event.get("stderr") or process_status)
            )
        elif event.get("stdout_utf8_valid") is not True:
            process_status = "worker_failed"
            protocol_status = "invalid_utf8"
            outcome_status = "protocol_failure"
            failure = _failure("response_decode", "UnicodeDecodeError", "stdout is not valid UTF-8")
        else:
            try:
                parsed = json.loads(str(event.get("stdout", "")))
            except json.JSONDecodeError as exc:
                process_status = "worker_failed"
                protocol_status = "invalid_json"
                outcome_status = "protocol_failure"
                failure = _failure("response_decode", type(exc).__name__, str(exc))
            else:
                if not isinstance(parsed, Mapping):
                    process_status = "worker_failed"
                    protocol_status = "non_object"
                    outcome_status = "protocol_failure"
                    failure = _failure("response_shape", "TypeError", "response is not an object")
                else:
                    response = dict(parsed)
                    expected_keys = {
                        "schema_version",
                        "role",
                        "operation",
                        "request_nonce",
                        "environment_observation",
                        "output",
                    }
                    if (
                        set(response) != expected_keys
                        or response.get("schema_version") != 1
                        or response.get("role") != role
                        or response.get("operation") != operation
                        or response.get("request_nonce") != request_nonce
                    ):
                        process_status = "worker_failed"
                        protocol_status = "response_envelope_mismatch"
                        outcome_status = "protocol_failure"
                        failure = _failure(
                            "response_shape",
                            "ResponseEnvelopeMismatch",
                            "worker response does not match its sealed request",
                        )
                        response = None
                    else:
                        observed_environment = response.get("environment_observation")
                        try:
                            _validate_worker_output(operation, response.get("output"))
                        except ResearchWorkerIntegrityError as exc:
                            process_status = "worker_failed"
                            protocol_status = "response_envelope_mismatch"
                            outcome_status = "protocol_failure"
                            failure = _failure("response_semantics", type(exc).__name__, str(exc))
                            response = None

        environment_authority = _environment_authority(
            launcher=self.launcher,
            python_executable=self.python_executable,
            clean_environment=clean_environment,
            observed_environment=observed_environment,
        )
        if outcome_status == "accepted" and environment_authority["observation_status"] != "matched":
            process_status = "worker_failed"
            protocol_status = "environment_mismatch"
            outcome_status = "protocol_failure"
            failure = _failure(
                "environment_observation",
                "EnvironmentMismatch",
                "worker observed names or values outside the env-i allowlist",
            )
            response = None
            environment_authority = _environment_authority(
                launcher=self.launcher,
                python_executable=self.python_executable,
                clean_environment=clean_environment,
                observed_environment=observed_environment,
            )
        return self._persist(
            role=role,
            operation=operation,
            invocation_id=invocation_id,
            request=request,
            request_bytes=request_bytes,
            receipt_ref=receipt_ref,
            receipt_path=receipt_path,
            workspace_record=workspace_record,
            command_authority=command_authority,
            command_observation=post_observation,
            environment_authority=environment_authority,
            isolation_assurance=isolation_assurance,
            governor=governor,
            event=event,
            process_status=process_status,
            protocol_status=protocol_status,
            outcome_status=outcome_status,
            response=response if outcome_status == "accepted" else None,
            failure=failure,
        )


def receipt_summary(
    receipt: Mapping[str, Any], *, receipt_path: Path | str | None = None
) -> dict[str, Any]:
    """Reopen and bind the immutable receipt used by a study manifest.

    A content digest inside a caller-supplied mapping is not transitive file
    authority.  The study therefore resolves the receipt through its sealed
    run directory and relative reference, replays the exact on-disk object,
    and records the file byte hash and length as well as the receipt's internal
    digest.  This makes later study validation detect both semantic mutation
    and substitution of a different serialization at the same path.
    """

    run_directory = Path(str(receipt["workspace"]["run_directory"]))
    expected_path = contained_path(
        run_directory, *Path(str(receipt["receipt_ref"])).parts
    )
    resolved_path = expected_path if receipt_path is None else Path(receipt_path)
    if (
        resolved_path.resolve() != expected_path
        or resolved_path.is_symlink()
        or not resolved_path.is_file()
    ):
        raise ResearchWorkerIntegrityError("research worker summary receipt path mismatch")
    disk_receipt = validate_research_worker_receipt(
        _load_json_object(resolved_path),
        receipt_path=resolved_path,
        require_live_authority=receipt["outcome_status"] == "accepted",
    )
    if disk_receipt != dict(receipt):
        raise ResearchWorkerIntegrityError(
            "research worker summary differs from its immutable receipt"
        )
    receipt_bytes = resolved_path.read_bytes()
    if receipt_bytes != canonical_json(disk_receipt) + b"\n":
        raise ResearchWorkerIntegrityError(
            "research worker receipt file is not canonical JSON bytes"
        )

    return {
        "receipt_id": receipt["receipt_id"],
        "receipt_ref": receipt["receipt_ref"],
        "receipt_digest": receipt["content_digest"],
        "receipt_file_sha256": bytes_digest(receipt_bytes),
        "receipt_byte_length": len(receipt_bytes),
        "role": receipt["role"],
        "operation": receipt["operation"],
        "invocation_id": receipt["invocation_id"],
        "request_sha256": receipt["request_sha256"],
        "response_sha256": receipt["response_sha256"],
        "process_status": receipt["process_status"],
        "protocol_status": receipt["protocol_status"],
        "outcome_status": receipt["outcome_status"],
        "isolation_status": receipt["isolation_assurance"]["status"],
        "isolation_backend": receipt["isolation_assurance"]["mechanism"]["backend"],
        "hidden_input_independence_authorized": False,
        "cognitive_independence_authorized": False,
        "semantic_independence_authorized": False,
    }


__all__ = [
    "ResearchWorkerAdapter",
    "ResearchWorkerIntegrityError",
    "receipt_summary",
    "strongest_available_isolation",
    "validate_research_worker_receipt",
]
