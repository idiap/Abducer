# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Typed resource governance for discovery jobs and branch portfolios.

The governor deliberately separates operational outcomes from epistemic ones.
Deadlines, process crashes, memory pressure, and spend limits can stop a job,
but none of them are evidence for or against a hypothesis.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import os
import platform
import re
import resource
import signal
import stat
import subprocess
import sys
import threading
import time
from collections import deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, BinaryIO, Mapping, Sequence

from agentic.process_resource_exec import ResourceExecPlan, digest_value
from agentic.process_supervision import (
    ProcessGroupSamplingPolicy,
    SupervisedProcessAttempt,
    SupervisionLimits,
    load_supervised_process_attempt,
    run_supervised_process,
)


TERMINAL_STATUSES = {
    "succeeded",
    "deadline_exhausted",
    "cpu_exhausted",
    "out_of_memory",
    "disk_exhausted",
    "network_exhausted",
    "token_exhausted",
    "request_exhausted",
    "spend_exhausted",
    "input_exhausted",
    "output_exhausted",
    "worker_failed",
    "report_failed",
    "cancelled",
}

RETRYABLE_STATUSES = {
    "deadline_exhausted",
    "cpu_exhausted",
    "out_of_memory",
    "disk_exhausted",
    "network_exhausted",
    "token_exhausted",
    "request_exhausted",
    "spend_exhausted",
    "input_exhausted",
    "output_exhausted",
    "worker_failed",
    "report_failed",
    "invalid",
    "literature_superseded",
}

_JOB_ID_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]{0,126}[A-Za-z0-9])?$")


class BudgetExceeded(RuntimeError):
    """Raised when a hard resource dimension is exhausted."""

    def __init__(self, status: str, dimension: str, used: float, limit: float) -> None:
        if status not in TERMINAL_STATUSES:
            raise ValueError(f"unknown terminal status: {status}")
        self.status = status
        self.dimension = dimension
        self.used = used
        self.limit = limit
        super().__init__(f"{dimension} budget exhausted: used={used!r}, limit={limit!r}")


def validate_job_id(job_id: str) -> str:
    """Return a validated filesystem-safe job identifier.

    Dot segments, separators, hidden names, and ambiguous trailing punctuation
    are rejected even on platforms where they would otherwise resolve.
    """

    if not isinstance(job_id, str) or not _JOB_ID_RE.fullmatch(job_id):
        raise ValueError("job_id must contain only bounded alphanumerics, '.', '_' or '-'")
    if job_id in {".", ".."} or job_id.startswith(".") or ".." in job_id:
        raise ValueError("job_id cannot contain dot path segments")
    if "/" in job_id or "\\" in job_id or "\x00" in job_id:
        raise ValueError("job_id cannot contain a path separator or NUL")
    return job_id


def contained_path(run_directory: Path | str, *parts: str) -> Path:
    """Resolve a path and prove it remains inside ``run_directory``."""

    root = Path(run_directory).resolve()
    candidate = root.joinpath(*parts).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"output path escapes run directory: {candidate}") from exc
    return candidate


def minimal_replacement_environment(
    workspace: Path | str,
    *,
    create_temporary: bool = True,
) -> dict[str, str]:
    """Build the shared deterministic base replacement environment.

    The governor adds only its typed ``ABDUCER_*`` operational budget fields.
    Receipt-producing adapters use this mapping as a replacement environment,
    never as an overlay on ambient host state.  This helper contains no secret
    values; later value digests omit plaintext but provide no confidentiality
    guarantee.
    """

    root = Path(workspace).resolve(strict=True)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("replacement-environment workspace must be a canonical directory")
    temporary = contained_path(root, "tmp")
    if create_temporary:
        temporary.mkdir(parents=True, exist_ok=True)
    elif temporary.is_symlink() or not temporary.is_dir():
        raise ValueError("replacement-environment temporary directory is unavailable")
    environment = {
        "HOME": str(root),
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONUTF8": "1",
        "TMPDIR": str(temporary),
    }
    if platform.system() == "Darwin":
        environment["__CF_USER_TEXT_ENCODING"] = f"0x{os.getuid():X}:0x0:0x0"
    return environment


def branch_run_directory(run_root: Path | str, job_id: str, branch_id: str | None = None) -> Path:
    """Construct (without creating) a contained run or branch directory."""

    safe_job = validate_job_id(job_id)
    path = contained_path(run_root, safe_job)
    if branch_id is not None:
        path = contained_path(path, "branches", validate_job_id(branch_id))
    return path


def _positive_number(value: Any, name: str, *, allow_zero: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    result = float(value)
    if result < 0 or (not allow_zero and result == 0):
        relation = "non-negative" if allow_zero else "positive"
        raise ValueError(f"{name} must be {relation}")
    return result


@dataclass(frozen=True)
class ResourceBudget:
    """Declared thresholds with dimension-specific enforcement semantics."""

    budget_id: str
    wall_time_seconds: float
    grace_period_seconds: float
    cpu_seconds: float
    memory_bytes: int
    disk_bytes: int
    network_bytes: int
    token_count: int
    request_count: int
    cost_usd: float
    absolute_deadline: str | None = None

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any], *, budget_id: str | None = None) -> "ResourceBudget":
        """Parse and strictly validate a budget mapping."""

        identifier = str(budget_id or raw.get("budget_id") or "budget")
        wall = _positive_number(raw.get("wall_time_seconds"), "wall_time_seconds")
        grace = _positive_number(raw.get("grace_period_seconds", 1.0), "grace_period_seconds", allow_zero=True)
        if grace > 30:
            raise ValueError("grace_period_seconds cannot exceed 30")
        cpu = _positive_number(raw.get("cpu_seconds", wall), "cpu_seconds")
        memory = int(_positive_number(raw.get("memory_bytes", 512 * 1024 * 1024), "memory_bytes"))
        disk = int(_positive_number(raw.get("disk_bytes", 64 * 1024 * 1024), "disk_bytes", allow_zero=True))
        network = int(_positive_number(raw.get("network_bytes", 0), "network_bytes", allow_zero=True))
        tokens = int(_positive_number(raw.get("token_count", 0), "token_count", allow_zero=True))
        requests = int(_positive_number(raw.get("request_count", 0), "request_count", allow_zero=True))
        cost = _positive_number(raw.get("cost_usd", 0.0), "cost_usd", allow_zero=True)
        absolute = raw.get("absolute_deadline")
        if absolute is not None:
            _parse_deadline(str(absolute))
        return cls(
            budget_id=identifier,
            wall_time_seconds=wall,
            grace_period_seconds=grace,
            cpu_seconds=cpu,
            memory_bytes=memory,
            disk_bytes=disk,
            network_bytes=network,
            token_count=tokens,
            request_count=requests,
            cost_usd=cost,
            absolute_deadline=str(absolute) if absolute is not None else None,
        )


@dataclass
class ResourceUsage:
    """Observed accountable resource use."""

    wall_time_seconds: float = 0.0
    cpu_seconds: float = 0.0
    peak_memory_bytes: int = 0
    disk_bytes: int = 0
    network_bytes: int = 0
    token_count: int = 0
    request_count: int = 0
    cost_usd: float = 0.0

    def add(self, other: "ResourceUsage") -> None:
        self.wall_time_seconds += other.wall_time_seconds
        self.cpu_seconds += other.cpu_seconds
        self.peak_memory_bytes = max(self.peak_memory_bytes, other.peak_memory_bytes)
        self.disk_bytes += other.disk_bytes
        self.network_bytes += other.network_bytes
        self.token_count += other.token_count
        self.request_count += other.request_count
        self.cost_usd += other.cost_usd


def _parse_deadline(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("absolute_deadline must include a timezone")
    return parsed.astimezone(dt.timezone.utc)


def _utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


_TYPED_GOVERNOR_ENVIRONMENT_FIELDS = {
    "ABDUCER_ABSOLUTE_DEADLINE",
    "ABDUCER_BUDGET_ID",
    "ABDUCER_COST_LIMIT_USD",
    "ABDUCER_NETWORK_LIMIT_BYTES",
    "ABDUCER_TOKEN_LIMIT",
    "ABDUCER_REQUEST_LIMIT",
}


def complete_governed_process_environment(
    base_environment: Mapping[str, str],
    *,
    deadline: dt.datetime | str,
    budget: ResourceBudget | Mapping[str, Any],
) -> dict[str, str]:
    """Return the exact child environment from a base map and typed budget.

    The result is suitable both for launch and for independent receipt replay.
    It does not inherit host state and its value hashes are identity evidence,
    not a confidentiality mechanism.
    """

    environment = dict(base_environment)
    for name, value in environment.items():
        if (
            not isinstance(name, str)
            or not name
            or "=" in name
            or "\x00" in name
            or not isinstance(value, str)
            or "\x00" in value
        ):
            raise ValueError("child environment must contain exact NUL-free strings")
    if _TYPED_GOVERNOR_ENVIRONMENT_FIELDS & set(environment):
        raise ValueError("base environment cannot predeclare governor-owned fields")
    if platform.system() == "Darwin":
        environment.setdefault(
            "__CF_USER_TEXT_ENCODING", f"0x{os.getuid():X}:0x0:0x0"
        )

    if isinstance(budget, ResourceBudget):
        budget_values: Mapping[str, Any] = asdict(budget)
    elif isinstance(budget, Mapping):
        budget_values = budget
    else:
        raise ValueError("budget must be ResourceBudget or a mapping")
    required_budget_fields = {
        "budget_id",
        "cost_usd",
        "network_bytes",
        "token_count",
        "request_count",
    }
    if not required_budget_fields.issubset(budget_values):
        raise ValueError("budget lacks governed environment fields")
    budget_id = budget_values["budget_id"]
    if not isinstance(budget_id, str) or not budget_id:
        raise ValueError("budget_id must be a non-empty string")
    deadline_text = deadline.isoformat() if isinstance(deadline, dt.datetime) else str(deadline)
    _parse_deadline(deadline_text)
    environment.update(
        {
            "ABDUCER_ABSOLUTE_DEADLINE": deadline_text,
            "ABDUCER_BUDGET_ID": budget_id,
            "ABDUCER_COST_LIMIT_USD": str(budget_values["cost_usd"]),
            "ABDUCER_NETWORK_LIMIT_BYTES": str(budget_values["network_bytes"]),
            "ABDUCER_TOKEN_LIMIT": str(budget_values["token_count"]),
            "ABDUCER_REQUEST_LIMIT": str(budget_values["request_count"]),
        }
    )
    return environment


def directory_file_sizes(path: Path | str) -> dict[str, int]:
    """Return stable relative paths and sizes for regular files below a root."""

    root = Path(path)
    if not root.exists():
        return {}
    sizes: dict[str, int] = {}
    for candidate in root.rglob("*"):
        try:
            if candidate.is_file() and not candidate.is_symlink():
                sizes[candidate.relative_to(root).as_posix()] = candidate.stat().st_size
        except (FileNotFoundError, PermissionError, OSError):
            continue
    return sizes


def directory_size(path: Path | str) -> int:
    """Return the total byte size of regular files below a contained path."""

    return sum(directory_file_sizes(path).values())


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _observe_sealed_local_file(
    path: Path | str,
    *,
    require_executable: bool,
) -> dict[str, Any]:
    """Observe one canonical local file without claiming authenticity."""

    candidate = Path(path)
    resolved = candidate.resolve(strict=True)
    if candidate != resolved or candidate.is_symlink():
        raise ValueError("sealed execution file must be a canonical non-symlink path")
    before = candidate.stat()
    if not stat.S_ISREG(before.st_mode):
        raise ValueError("sealed execution authority must identify a regular file")
    if require_executable and not os.access(candidate, os.X_OK):
        raise ValueError("sealed execution authority is not executable")
    raw = candidate.read_bytes()
    after = candidate.stat()
    stable_fields = (
        "st_dev",
        "st_ino",
        "st_mode",
        "st_size",
        "st_mtime_ns",
        "st_ctime_ns",
    )
    if any(getattr(before, name) != getattr(after, name) for name in stable_fields):
        raise ValueError("sealed execution file changed while it was observed")
    if len(raw) != after.st_size:
        raise ValueError("sealed execution file length changed while it was read")
    return {
        "path": str(resolved),
        "sha256": _sha256_bytes(raw),
        "size_bytes": len(raw),
        "device": int(after.st_dev),
        "inode": int(after.st_ino),
        "mode": int(after.st_mode),
        "mtime_ns": int(after.st_mtime_ns),
        "ctime_ns": int(after.st_ctime_ns),
        "executable_required": require_executable,
        "executable_observed": bool(os.access(candidate, os.X_OK)),
    }


def _resource_exec_authority_observation(
    *,
    python_executable: Path,
    launcher: Path,
) -> dict[str, Any]:
    return {
        "python_executable": _observe_sealed_local_file(
            python_executable,
            require_executable=True,
        ),
        "resource_exec_launcher": _observe_sealed_local_file(
            launcher,
            require_executable=False,
        ),
    }


_RESOURCE_LIMIT_EXECUTION_SCHEMA_VERSION = "2.0.0"
_RESOURCE_LIMIT_AUTHORITY_BOUNDARY = (
    "exact_local_bytes_and_request_binding_only_no_semantic_scientific_"
    "truth_experiment_value_or_physics_authority"
)
_RESOURCE_LIMIT_EXECUTION_KEYS = {
    "schema_version",
    "authority_kind",
    "logical_argv_digest",
    "transport_argv_digest",
    "supervised_request_digest",
    "supervised_transport_exact",
    "replacement_environment_used",
    "environment_digest",
    "capture_limit_bytes",
    "resource_exec_plan",
    "resource_exec_plan_digest",
    "pre_execution_observation",
    "post_execution_observation",
    "observation_status",
    "observation_error",
    "cryptographic_authenticity",
    "authority_boundary",
}


def _v2_termination_projection(attempt: SupervisedProcessAttempt) -> str | None:
    disposition = attempt.termination_disposition
    if disposition.startswith("sigterm_sent"):
        return "terminated"
    if disposition.startswith("sigkill_sent"):
        return "killed"
    return None


def _v2_governor_outcome_projection(
    attempt: SupervisedProcessAttempt,
    *,
    role: str,
    plan: ResourceExecPlan,
    post_acceptance: Mapping[str, Any],
    authority_exact: bool,
) -> dict[str, Any]:
    """Derive the only accepted governor status and terminal projection."""

    reasons = {failure.reason_code for failure in attempt.failure_events}
    deadline_reasons = {
        "execution_deadline_exhausted",
        "launch_consumed_execution_deadline",
        "request_preparation_consumed_execution_deadline",
        "sampler_deadline_exhausted",
        "total_deadline_overrun_detected",
    }
    output_reasons = {"stdout_limit_exceeded", "stderr_limit_exceeded"}
    memory_reasons = {
        "sampled_original_group_rss_threshold_exceeded",
        "observed_wait4_normalized_maxrss_threshold_exceeded",
    }
    disk_limit_exceeded = post_acceptance.get("disk_limit_exceeded") is True
    if "input_limit_exceeded" in reasons:
        status = "input_exhausted"
    elif reasons & deadline_reasons:
        status = "deadline_exhausted"
    elif reasons & output_reasons:
        status = "output_exhausted"
    elif reasons & memory_reasons:
        status = "out_of_memory"
    elif "observed_wait4_cpu_threshold_exceeded" in reasons:
        status = "cpu_exhausted"
    elif disk_limit_exceeded:
        status = "disk_exhausted"
    elif attempt.returncode == -signal.SIGXCPU:
        status = "cpu_exhausted"
    elif (
        attempt.returncode is not None
        and hasattr(signal, "SIGXFSZ")
        and attempt.returncode == -signal.SIGXFSZ
    ):
        status = "disk_exhausted"
    elif (
        not authority_exact
        or post_acceptance.get("snapshot_error") is not None
        or post_acceptance.get("acceptance_deadline_overrun") is True
    ):
        status = "report_failed" if role == "report_builder" else "worker_failed"
    elif attempt.status == "succeeded":
        status = "succeeded"
    elif role == "report_builder":
        status = "report_failed"
    else:
        status = "worker_failed"

    terminal_dimension: str | None = None
    terminal_used: float | int | None = None
    terminal_limit: float | int | None = None
    if status == "input_exhausted":
        terminal_dimension = "stdin_bytes"
        terminal_used = attempt.request.stdin_bytes
        terminal_limit = attempt.limits.stdin_limit_bytes
    elif status == "output_exhausted":
        stream_name = "stdout" if "stdout_limit_exceeded" in reasons else "stderr"
        stream = attempt.stdout if stream_name == "stdout" else attempt.stderr
        terminal_dimension = f"{stream_name}_bytes"
        terminal_used = stream.captured_bytes
        terminal_limit = stream.ceiling_bytes
    elif status == "out_of_memory":
        terminal_dimension = "peak_memory_bytes"
        terminal_used = max(
            attempt.wait4_ru_maxrss_normalized_bytes or 0,
            attempt.peak_observed_sampled_original_group_rss_bytes or 0,
        )
        terminal_limit = plan.process_memory_bytes
    elif status == "cpu_exhausted":
        terminal_dimension = "cpu_seconds"
        terminal_used = (
            (attempt.wait4_accounted_user_cpu_ns or 0)
            + (attempt.wait4_accounted_system_cpu_ns or 0)
        ) / 1_000_000_000
        terminal_limit = plan.remaining_cpu_ns / 1_000_000_000
    elif status == "disk_exhausted":
        terminal_dimension = "disk_bytes"
        terminal_used = post_acceptance["disk_snapshot_bytes"]
        terminal_limit = plan.workspace_disk_bytes
    elif status == "deadline_exhausted":
        terminal_dimension = "wall_time_seconds"
        terminal_used = attempt.total_elapsed_ns / 1_000_000_000
        terminal_limit = (
            attempt.limits.total_deadline_ns - attempt.limits.cleanup_reserve_ns
        ) / 1_000_000_000

    stdin_failure = next(
        (
            failure.message
            for failure in attempt.failure_events
            if failure.reason_code == "stdin_write_failed"
        ),
        None,
    )
    descendant = bool(
        attempt.peak_observed_sampled_original_group_members is not None
        and attempt.peak_observed_sampled_original_group_members > 1
    )
    return {
        "status": status,
        "terminal_dimension": terminal_dimension,
        "terminal_used": terminal_used,
        "terminal_limit": terminal_limit,
        "termination": _v2_termination_projection(attempt),
        "stdin_write_error": stdin_failure,
        "descendant_leak_detected": descendant,
        "epistemic_effect": (
            "awaiting_output_validation"
            if status == "succeeded"
            else "none_operational_outcome_only"
        ),
    }


def validate_v2_process_event(
    event: Mapping[str, Any],
    *,
    accepted: bool,
    expected_workspace: Path | str | None = None,
    expected_replacement_environment: Mapping[str, str] | None = None,
    require_live_execution_authority: bool = False,
) -> SupervisedProcessAttempt | None:
    """Reopen and correlate one v2 governor event across every authority layer."""

    if not isinstance(event, Mapping) or event.get("event_schema_version") != 2:
        raise ValueError("v2 process event marker is missing")
    measurement = event.get("resource_measurement")
    if not isinstance(measurement, Mapping) or measurement.get(
        "measurement_schema_version"
    ) != 2:
        raise ValueError("v2 process event lacks v2 measurement boundaries")
    post = event.get("post_supervision_acceptance")
    if not isinstance(post, Mapping):
        raise ValueError("v2 process event lacks post-supervision acceptance evidence")
    post_expected_status = (
        "snapshot_failed"
        if post.get("snapshot_error") is not None
        else "deadline_overrun"
        if post.get("acceptance_deadline_overrun") is True
        else "rejected"
        if post.get("disk_limit_exceeded") is True
        else "accepted"
    )
    if post.get("status") != "not_run" and post.get("status") != post_expected_status:
        raise ValueError("post-supervision acceptance status is not derived")
    if post.get("continuous_disk_observation") is not False:
        raise ValueError("disk observation overstates continuous coverage")
    if (
        type(post.get("disk_snapshot_bytes")) is not int
        or type(post.get("disk_limit_bytes")) is not int
        or post["disk_snapshot_bytes"] < 0
        or post["disk_limit_bytes"] < 0
        or post.get("disk_limit_exceeded")
        is not (post["disk_snapshot_bytes"] > post["disk_limit_bytes"])
    ):
        raise ValueError("post-supervision disk relation is inconsistent")

    attempt_payload = event.get("supervision_attempt")
    execution = event.get("resource_limit_execution")
    if attempt_payload is None:
        if (
            execution is not None
            or event.get("pid") is not None
            or event.get("returncode") is not None
            or post.get("status") != "not_run"
            or accepted
            or event.get("status") == "succeeded"
        ):
            raise ValueError("prelaunch v2 event carries launched or accepted evidence")
        empty_digest = _sha256_bytes(b"")
        stderr_text = event.get("stderr")
        if not isinstance(stderr_text, str):
            raise ValueError("prelaunch v2 stderr is not text")
        stderr_bytes = stderr_text.encode("utf-8", errors="replace")
        if (
            event.get("termination") != "not_started"
            or event.get("stdin_written_bytes") != 0
            or event.get("stdin_write_incomplete") is not False
            or event.get("stdin_write_error") is not None
            or event.get("stdout") != ""
            or event.get("stderr_bytes", 0) < 0
            or event.get("stdout_bytes") != 0
            or event.get("stdout_retained_bytes") != 0
            or event.get("stdout_sha256") != empty_digest
            or event.get("stdout_utf8_valid") is not True
            or event.get("stderr_bytes") != len(stderr_bytes)
            or event.get("stderr_retained_bytes") != len(stderr_bytes)
            or event.get("stderr_sha256") != _sha256_bytes(stderr_bytes)
            or event.get("stderr_utf8_valid") is not True
            or event.get("stdout_truncated") is not False
            or event.get("stdout_drain_incomplete") is not False
            or event.get("stderr_truncated") is not False
            or event.get("stderr_drain_incomplete") is not False
            or event.get("descendant_leak_detected") is not False
            or event.get("epistemic_effect") != "none_operational_outcome_only"
        ):
            raise ValueError("prelaunch v2 event carries impossible process evidence")
        if event.get("status") == "input_exhausted" and (
            event.get("terminal_dimension") != "stdin_bytes"
            or event.get("terminal_used") != event.get("stdin_bytes")
            or event.get("terminal_limit") != event.get("stdin_limit_bytes")
        ):
            raise ValueError("prelaunch input exhaustion projection differs")
        return None
    if not isinstance(attempt_payload, Mapping) or not isinstance(execution, Mapping):
        raise ValueError("launched v2 event lacks attempt or execution authority")
    if post.get("status") == "not_run":
        raise ValueError("launched v2 event lacks post-supervision acceptance evidence")
    if set(execution) != _RESOURCE_LIMIT_EXECUTION_KEYS:
        raise ValueError("resource execution authority keys differ from the closed contract")
    if (
        execution.get("schema_version") != _RESOURCE_LIMIT_EXECUTION_SCHEMA_VERSION
        or execution.get("authority_kind")
        != "trusted_local_resource_limit_execution"
        or type(execution.get("supervised_transport_exact")) is not bool
        or type(execution.get("replacement_environment_used")) is not bool
        or type(execution.get("capture_limit_bytes")) is not int
        or execution["capture_limit_bytes"] <= 0
        or execution.get("cryptographic_authenticity") is not False
        or execution.get("authority_boundary")
        != _RESOURCE_LIMIT_AUTHORITY_BOUNDARY
    ):
        raise ValueError("resource execution authority constants are invalid")
    attempt = load_supervised_process_attempt(attempt_payload)
    plan_raw = execution.get("resource_exec_plan")
    if not isinstance(plan_raw, Mapping):
        raise ValueError("resource execution plan is missing")
    plan = ResourceExecPlan.from_mapping(plan_raw)
    if plan.digest() != execution.get("resource_exec_plan_digest"):
        raise ValueError("resource execution plan digest mismatch")
    if plan.platform_system != platform.system():
        raise ValueError("resource execution plan platform differs from replay host")
    logical_argv = event.get("command")
    if not isinstance(logical_argv, list) or not logical_argv:
        raise ValueError("v2 logical command is invalid")
    if (
        digest_value(logical_argv) != execution.get("logical_argv_digest")
        or plan.logical_argv_digest != execution.get("logical_argv_digest")
    ):
        raise ValueError("logical command and resource plan digests differ")
    if plan.cwd != attempt.request.cwd:
        raise ValueError("resource plan and supervised cwd differ")
    if expected_workspace is not None and Path(plan.cwd) != Path(
        expected_workspace
    ).resolve(strict=True):
        raise ValueError("resource execution cwd differs from the receipt workspace")
    if execution.get("environment_digest") != plan.environment_digest:
        raise ValueError("resource execution environment digest differs from its plan")
    if plan.supervision_environment_digest != attempt.request.environment_digest:
        raise ValueError("resource plan and supervised environment identities differ")
    if expected_replacement_environment is not None:
        expected_environment = dict(expected_replacement_environment)
        expected_bindings = tuple(
            (name, _sha256_bytes(value.encode("utf-8")))
            for name, value in sorted(expected_environment.items())
        )
        if (
            execution.get("replacement_environment_used") is not True
            or plan.environment_digest != digest_value(expected_environment)
            or attempt.request.environment_bindings != expected_bindings
        ):
            raise ValueError(
                "resource execution differs from the exact replacement-environment policy"
            )
    if (
        post.get("disk_limit_bytes") != plan.workspace_disk_bytes
        or attempt.limits.reject_if_observed_wait4_cpu_ns_above
        != plan.remaining_cpu_ns
        or attempt.limits.reject_if_observed_wait4_normalized_maxrss_bytes_above
        != plan.process_memory_bytes
        or attempt.limits.termination_grace_ns != plan.cpu_grace_ns
    ):
        raise ValueError("resource plan and supervision limits differ")

    pre = execution.get("pre_execution_observation")
    observed_post = execution.get("post_execution_observation")
    if not isinstance(pre, Mapping):
        raise ValueError("resource execution lacks its pre-observation")
    python_row = pre.get("python_executable")
    launcher_row = pre.get("resource_exec_launcher")
    if not isinstance(python_row, Mapping) or not isinstance(launcher_row, Mapping):
        raise ValueError("resource execution file observations are incomplete")
    expected_transport = [
        python_row.get("path"),
        "-I",
        "-B",
        launcher_row.get("path"),
        "--resource-plan-base64",
        plan.base64_token(),
        "--",
        *logical_argv,
    ]
    transport_exact = attempt.request.argv == tuple(expected_transport)
    if (
        execution.get("transport_argv_digest") != digest_value(expected_transport)
        or execution.get("supervised_request_digest")
        != attempt.request.request_digest
        or execution.get("supervised_transport_exact") is not transport_exact
    ):
        raise ValueError("resource execution transport/request binding differs")
    authority_exact = (
        observed_post == pre
        and observed_post is not None
        and execution.get("observation_error") is None
    )
    if observed_post is None and execution.get("observation_error") is None:
        raise ValueError("missing post-execution observation lacks an error")
    expected_observation_status = "exact_match" if authority_exact else "mismatch"
    if execution.get("observation_status") != expected_observation_status:
        raise ValueError("resource execution observation status is not derived")
    if require_live_execution_authority and authority_exact:
        live = _resource_exec_authority_observation(
            python_executable=Path(str(python_row["path"])),
            launcher=Path(str(launcher_row["path"])),
        )
        if live != pre:
            raise ValueError("live resource execution authority changed after receipt")

    if event.get("pid") != attempt.pid or event.get("returncode") != attempt.returncode:
        raise ValueError("v2 process projection differs from wait4 evidence")
    if (
        event.get("stdin_bytes") != attempt.request.stdin_bytes
        or event.get("stdin_sha256") != attempt.request.stdin_sha256
        or event.get("stdin_limit_bytes") != attempt.limits.stdin_limit_bytes
        or event.get("stdin_written_bytes") != attempt.stdin_enqueued_bytes
        or event.get("stdin_write_incomplete") is attempt.stdin_fully_enqueued
    ):
        raise ValueError("v2 stdin projection differs from supervised evidence")
    for label, stream in (("stdout", attempt.stdout), ("stderr", attempt.stderr)):
        retained_text = stream.retained_tail.decode("utf-8", errors="replace")
        if (
            event.get(label) != retained_text
            or event.get(f"{label}_bytes") != stream.captured_bytes
            or event.get(f"{label}_retained_bytes") != len(stream.retained_tail)
            or event.get(f"{label}_sha256") != stream.captured_sha256
            or event.get(f"{label}_utf8_valid")
            is not stream.utf8_valid_retained_tail
            or event.get(f"{label}_truncated")
            is not (stream.captured_bytes > len(stream.retained_tail))
            or event.get(f"{label}_drain_incomplete") is stream.capture_complete
            or event.get(f"{label}_limit_bytes") != stream.ceiling_bytes
        ):
            raise ValueError(f"v2 {label} projection differs from supervised evidence")
    capture_limit = execution["capture_limit_bytes"]
    if event.get("capture_limit_bytes") != capture_limit:
        raise ValueError("v2 capture-limit projection differs from execution authority")
    for label, stream in (("stdout", attempt.stdout), ("stderr", attempt.stderr)):
        expected_retained_limit = (
            capture_limit
            if stream.ceiling_bytes is None
            else min(capture_limit, stream.ceiling_bytes)
        )
        if stream.retained_limit_bytes != expected_retained_limit:
            raise ValueError(f"v2 {label} retained limit differs from capture authority")
    projection = _v2_governor_outcome_projection(
        attempt,
        role=str(event.get("role")),
        plan=plan,
        post_acceptance=post,
        authority_exact=authority_exact,
    )
    for field, expected in projection.items():
        if event.get(field) != expected:
            raise ValueError(f"v2 {field} projection differs from supervised evidence")
    if accepted and (
        event.get("status") != "succeeded"
        or attempt.status != "succeeded"
        or attempt.returncode != 0
        or not transport_exact
        or not authority_exact
        or post.get("status") != "accepted"
        or post.get("disk_limit_exceeded") is not False
        or post.get("snapshot_error") is not None
        or post.get("acceptance_deadline_overrun") is not False
    ):
        raise ValueError("accepted v2 event lacks complete operational closure")
    return attempt


class _BoundedOutputCollector:
    """Drain one subprocess pipe while retaining only a fixed-size byte tail.

    ``communicate()`` retains the complete child output and can move an
    otherwise bounded worker's memory pressure into the ungoverned parent.
    Dedicated drain threads prevent pipe deadlock while the deque keeps parent
    memory independent of how noisy the child is.
    """

    def __init__(self, stream: BinaryIO, limit_bytes: int) -> None:
        self.stream = stream
        self.limit_bytes = limit_bytes
        self.total_bytes = 0
        self.retained_bytes = 0
        self.chunks: deque[bytes] = deque()
        self.error: OSError | None = None
        self._digest = hashlib.sha256()
        self._lock = threading.Lock()
        self.thread = threading.Thread(target=self._drain, daemon=True)

    def start(self) -> None:
        self.thread.start()

    def _drain(self) -> None:
        try:
            while True:
                chunk = self.stream.read(64 * 1024)
                if not chunk:
                    break
                with self._lock:
                    self.total_bytes += len(chunk)
                    self._digest.update(chunk)
                    self.chunks.append(chunk)
                    self.retained_bytes += len(chunk)
                    while self.retained_bytes > self.limit_bytes and self.chunks:
                        excess = self.retained_bytes - self.limit_bytes
                        oldest = self.chunks[0]
                        if len(oldest) <= excess:
                            self.chunks.popleft()
                            self.retained_bytes -= len(oldest)
                        else:
                            self.chunks[0] = oldest[excess:]
                            self.retained_bytes -= excess
        except OSError as exc:
            self.error = exc
        finally:
            try:
                self.stream.close()
            except OSError:
                pass

    def total(self) -> int:
        """Return the exact byte count observed so far."""

        with self._lock:
            return self.total_bytes

    def finish(
        self, *, deadline_monotonic: float
    ) -> tuple[str, int, bool, bool, str, bool, int]:
        """Return bounded text plus exact stream metadata by an absolute deadline.

        The digest covers every drained byte, not merely the retained tail.
        UTF-8 validity remains separate from replacement-decoded diagnostic text
        so protocol callers can fail closed without breaking legacy log readers.
        """

        self.thread.join(timeout=max(0.0, deadline_monotonic - time.monotonic()))
        incomplete = self.thread.is_alive()
        if self.error is not None and not incomplete:
            raise self.error
        with self._lock:
            encoded = b"".join(self.chunks)
            total_bytes = self.total_bytes
            stream_digest = "sha256:" + self._digest.hexdigest()
        try:
            decoded = encoded.decode("utf-8", errors="strict")
            utf8_valid = True
        except UnicodeDecodeError:
            decoded = encoded.decode("utf-8", errors="replace")
            utf8_valid = False
        return (
            decoded,
            total_bytes,
            total_bytes > self.limit_bytes,
            incomplete,
            stream_digest,
            utf8_valid,
            len(encoded),
        )


class _BoundedInputWriter:
    """Write pre-bounded stdin without letting a non-reader stall the parent."""

    def __init__(self, stream: BinaryIO, payload: bytes) -> None:
        self.stream = stream
        self.payload = payload
        self.written_bytes = 0
        self.error: str | None = None
        self.thread = threading.Thread(target=self._write, daemon=True)

    def start(self) -> None:
        self.thread.start()

    def _write(self) -> None:
        try:
            view = memoryview(self.payload)
            while view:
                written = self.stream.write(view[: 64 * 1024])
                if written is None or written <= 0:
                    raise BrokenPipeError("subprocess stdin accepted no further bytes")
                self.written_bytes += written
                view = view[written:]
            self.stream.flush()
        except (BrokenPipeError, OSError, ValueError) as exc:
            self.error = f"{type(exc).__name__}: {exc}"
        finally:
            try:
                self.stream.close()
            except OSError:
                pass

    def finish(self, *, deadline_monotonic: float) -> tuple[int, bool, str | None]:
        self.thread.join(timeout=max(0.0, deadline_monotonic - time.monotonic()))
        return self.written_bytes, self.thread.is_alive(), self.error


class ResourceGovernor:
    """Enforce measured limits and expose every unavailable accounting edge.

    Wall time, CPU, process-group RSS, captured output, and run-directory disk
    growth are measured by this process.  Network, token, request, and monetary
    cost require an adapter to call :meth:`account`; until that happens the
    receipt calls them unavailable rather than pretending environment hints are
    enforcement.
    """

    def __init__(
        self,
        budget: ResourceBudget,
        *,
        run_directory: Path | str | None = None,
        allowed_working_directory: Path | str | None = None,
        capture_limit_bytes: int = 1024 * 1024,
        disk_sample_interval_seconds: float = 0.5,
    ) -> None:
        if capture_limit_bytes <= 0:
            raise ValueError("capture_limit_bytes must be positive")
        if disk_sample_interval_seconds <= 0:
            raise ValueError("disk_sample_interval_seconds must be positive")
        self.budget = budget
        self.run_directory = Path(run_directory).resolve() if run_directory is not None else None
        self.allowed_working_directory = (
            Path(allowed_working_directory).resolve()
            if allowed_working_directory is not None
            else self.run_directory
        )
        self.capture_limit_bytes = int(capture_limit_bytes)
        self.disk_sample_interval_seconds = float(disk_sample_interval_seconds)
        self.started_monotonic = time.monotonic()
        self.started_at = _utc_now()
        relative = self.started_at + dt.timedelta(seconds=budget.wall_time_seconds)
        absolute = _parse_deadline(budget.absolute_deadline) if budget.absolute_deadline else relative
        self.deadline = min(relative, absolute)
        self.deadline_monotonic = self.started_monotonic + max(
            0.0, (self.deadline - self.started_at).total_seconds()
        )
        self.usage = ResourceUsage()
        self.events: list[dict[str, Any]] = []
        self._externally_reported_dimensions: set[str] = set()
        self._disk_baseline_sizes = (
            directory_file_sizes(self.run_directory)
            if self.run_directory is not None
            else {}
        )
        self._last_disk_sample_monotonic = self.started_monotonic

    @classmethod
    def from_mapping(
        cls,
        raw: Mapping[str, Any],
        *,
        run_directory: Path | str | None = None,
        branch_id: str | None = None,
    ) -> "ResourceGovernor":
        """Create a governor, applying a named per-branch override if present."""

        effective = dict(raw)
        if branch_id is not None:
            per_branch = raw.get("per_branch", {})
            if not isinstance(per_branch, Mapping) or branch_id not in per_branch:
                raise ValueError(f"missing independent budget for branch {branch_id!r}")
            branch_raw = per_branch[branch_id]
            if not isinstance(branch_raw, Mapping):
                raise ValueError(f"invalid budget for branch {branch_id!r}")
            for key, value in branch_raw.items():
                effective[key] = value
            effective["budget_id"] = f"{raw.get('budget_id', 'portfolio')}:{branch_id}"
        return cls(ResourceBudget.from_mapping(effective), run_directory=run_directory)

    def remaining_seconds(self) -> float:
        return max(0.0, (self.deadline - _utc_now()).total_seconds())

    def account(
        self,
        *,
        network_bytes: int | None = None,
        token_count: int | None = None,
        request_count: int | None = None,
        cost_usd: float | None = None,
        disk_bytes: int | None = None,
    ) -> None:
        """Atomically account externally observed resources and enforce maxima."""

        increments = tuple(
            value
            for value in (network_bytes, token_count, request_count, cost_usd)
            if value is not None
        )
        if any(value < 0 for value in increments):
            raise ValueError("resource increments cannot be negative")
        for dimension, value in (
            ("network_bytes", network_bytes),
            ("token_count", token_count),
            ("request_count", request_count),
            ("cost_usd", cost_usd),
        ):
            if value is None:
                continue
            self._externally_reported_dimensions.add(dimension)
            setattr(
                self.usage,
                dimension,
                getattr(self.usage, dimension) + (float(value) if dimension == "cost_usd" else int(value)),
            )
        if disk_bytes is not None:
            if disk_bytes < 0:
                raise ValueError("disk_bytes cannot be negative")
            self.usage.disk_bytes = int(disk_bytes)
        else:
            self._sample_disk_usage(force=True)
        self.checkpoint()

    def measurement_boundaries(self) -> dict[str, Any]:
        """Describe which resource dimensions are truly measured or reported."""

        boundaries = {
            "measurement_schema_version": 2,
            "wall_time_seconds": {
                "status": "parent_monotonic_deadline",
                "enforced": True,
                "scope": "execution_deadline_plus_bounded_cleanup_and_acceptance",
                "hard_kernel_preemption": False,
                "blocking_call_overrun_detected_after_return": True,
            },
            "cpu_seconds": {
                "status": "target_pid_wait4_accounting",
                "enforced": True,
                "kernel_limit": "inherited_per_process_integer_second_rlimit_cpu",
                "post_exit_acceptance": "exact_nanosecond_wait4_threshold",
                "full_process_group_coverage": False,
            },
            "peak_memory_bytes": {
                "status": "wait4_maxrss_plus_sampled_original_group_rss",
                "enforced": True,
                "kernel_limit": (
                    "linux_inherited_per_process_virtual_address_space_rlimit"
                    if platform.system() == "Linux"
                    else "unavailable_on_darwin"
                ),
                "hard_group_rss_limit": False,
                "sampling_misses_between_observations": True,
            },
            "disk_bytes": {
                "status": (
                    "post_exit_positive_growth_high_water"
                    if self.run_directory is not None
                    else "unavailable"
                ),
                "enforced": self.run_directory is not None,
                "kernel_limit": (
                    "inherited_per_file_rlimit_fsize"
                    if self.run_directory is not None
                    else "unavailable"
                ),
                "hard_aggregate_workspace_quota": False,
                "accounting_root": str(self.run_directory) if self.run_directory is not None else None,
                "sample_interval_seconds": (
                    self.disk_sample_interval_seconds
                    if self.run_directory is not None
                    else None
                ),
                "limitation": (
                    "positive per-file growth observed at sampling boundaries; "
                    "the final snapshot is acceptance evidence but ephemeral create-delete "
                    "bursts between observations are unavailable"
                    if self.run_directory is not None
                    else "no accounting root was supplied"
                ),
            },
        }
        for dimension in ("network_bytes", "token_count", "request_count", "cost_usd"):
            reported = dimension in self._externally_reported_dimensions
            boundaries[dimension] = {
                "status": "externally_reported" if reported else "unavailable",
                "enforced": reported,
                "reason": (
                    "adapter supplied cumulative usage"
                    if reported
                    else "generic subprocess governance cannot observe this dimension"
                ),
            }
        return boundaries

    def _sample_disk_usage(self, *, force: bool = False) -> int:
        """Measure high-water positive growth below the accounting root."""

        if self.run_directory is None:
            return self.usage.disk_bytes
        now = time.monotonic()
        if (
            not force
            and now - self._last_disk_sample_monotonic
            < self.disk_sample_interval_seconds
        ):
            return self.usage.disk_bytes
        current = directory_file_sizes(self.run_directory)
        growth = sum(
            max(0, size - self._disk_baseline_sizes.get(relative, 0))
            for relative, size in current.items()
        )
        self.usage.disk_bytes = max(self.usage.disk_bytes, growth)
        self._last_disk_sample_monotonic = now
        return self.usage.disk_bytes

    def checkpoint(self) -> None:
        """Enforce all observable resource dimensions immediately."""

        elapsed = time.monotonic() - self.started_monotonic
        self.usage.wall_time_seconds = max(self.usage.wall_time_seconds, elapsed)
        self._sample_disk_usage()
        if _utc_now() >= self.deadline or elapsed >= self.budget.wall_time_seconds:
            raise BudgetExceeded("deadline_exhausted", "wall_time_seconds", elapsed, self.budget.wall_time_seconds)
        checks = (
            ("cpu_exhausted", "cpu_seconds", self.usage.cpu_seconds, self.budget.cpu_seconds),
            ("out_of_memory", "peak_memory_bytes", self.usage.peak_memory_bytes, self.budget.memory_bytes),
            ("network_exhausted", "network_bytes", self.usage.network_bytes, self.budget.network_bytes),
            ("token_exhausted", "token_count", self.usage.token_count, self.budget.token_count),
            ("request_exhausted", "request_count", self.usage.request_count, self.budget.request_count),
            ("spend_exhausted", "cost_usd", self.usage.cost_usd, self.budget.cost_usd),
            ("disk_exhausted", "disk_bytes", self.usage.disk_bytes, self.budget.disk_bytes),
        )
        for status, dimension, used, limit in checks:
            # A zero allowance means the dimension is unavailable, not unbounded.
            if used > limit:
                raise BudgetExceeded(status, dimension, float(used), float(limit))

    def _build_exact_child_environment(
        self,
        *,
        env: Mapping[str, str] | None,
        replacement_environment: Mapping[str, str] | None,
    ) -> tuple[dict[str, str], bool]:
        if env is not None and replacement_environment is not None:
            raise ValueError("env overlay and replacement_environment are mutually exclusive")
        child_environment = (
            dict(replacement_environment)
            if replacement_environment is not None
            else os.environ.copy()
        )
        if env is not None:
            child_environment.update(env)
        child_environment = complete_governed_process_environment(
            child_environment,
            deadline=self.deadline,
            budget=self.budget,
        )
        return child_environment, replacement_environment is not None

    def _build_supervision_limits(
        self,
        *,
        execution_remaining_ns: int,
        remaining_cpu_ns: int,
        input_limit_bytes: int,
        stdout_limit_bytes: int | None,
        stderr_limit_bytes: int | None,
    ) -> SupervisionLimits:
        evidence_reserve_ns = 50_000_000
        termination_grace_ns = int(self.budget.grace_period_seconds * 1_000_000_000)
        cleanup_reserve_ns = termination_grace_ns + evidence_reserve_ns + 200_000_001
        if execution_remaining_ns >= 500_000_000:
            sampling_mode = "posix_ps"
            sampling_required = True
            # ``ps -axo`` scans the host process table, so its latency is not
            # proportional to the governed worker and concurrent matched arms
            # can legitimately contend here.  Reserve a bounded fraction of
            # the *arm's own* remaining deadline instead of imposing the old
            # fixed 100 ms sidecar deadline.  This preserves required,
            # fail-closed process-group observation while keeping both the
            # sampler and its cleanup inside the parent's absolute deadline.
            attempt_timeout_ns = min(
                3_000_000_000,
                max(100_000_000, execution_remaining_ns // 12),
            )
            sampling_cleanup_ns = min(
                250_000_000,
                max(25_000_000, attempt_timeout_ns // 10),
            )
        elif execution_remaining_ns >= 100_000_000:
            sampling_mode = "posix_ps"
            sampling_required = False
            attempt_timeout_ns = 30_000_000
            sampling_cleanup_ns = 10_000_000
        else:
            sampling_mode = "disabled"
            sampling_required = False
            attempt_timeout_ns = 30_000_000
            sampling_cleanup_ns = 10_000_000
        sampling_interval_ns = max(
            50_000_000,
            math.ceil(execution_remaining_ns / 63),
        )
        sampling = ProcessGroupSamplingPolicy(
            mode=sampling_mode,
            required=sampling_required,
            interval_ns=sampling_interval_ns,
            attempt_timeout_ns=attempt_timeout_ns,
            cleanup_reserve_ns=sampling_cleanup_ns,
            stdout_limit_bytes=64 * 1024,
            stderr_limit_bytes=16 * 1024,
            maximum_attempts=64,
            reject_if_observed_members_above=(
                1 if sampling_mode == "posix_ps" else None
            ),
            reject_if_observed_rss_bytes_above=(
                self.budget.memory_bytes if sampling_mode == "posix_ps" else None
            ),
        )
        return SupervisionLimits(
            total_deadline_ns=execution_remaining_ns + cleanup_reserve_ns,
            cleanup_reserve_ns=cleanup_reserve_ns,
            termination_grace_ns=termination_grace_ns,
            evidence_seal_reserve_ns=evidence_reserve_ns,
            stdin_limit_bytes=input_limit_bytes,
            stdout_limit_bytes=stdout_limit_bytes,
            stderr_limit_bytes=stderr_limit_bytes,
            stdout_retained_tail_bytes=(
                min(self.capture_limit_bytes, stdout_limit_bytes)
                if stdout_limit_bytes is not None
                else self.capture_limit_bytes
            ),
            stderr_retained_tail_bytes=(
                min(self.capture_limit_bytes, stderr_limit_bytes)
                if stderr_limit_bytes is not None
                else self.capture_limit_bytes
            ),
            sampling=sampling,
            reject_if_observed_wait4_cpu_ns_above=remaining_cpu_ns,
            reject_if_observed_wait4_normalized_maxrss_bytes_above=(
                self.budget.memory_bytes
            ),
        )

    def _strict_post_exit_disk_snapshot(self) -> int:
        if self.run_directory is None:
            return self.usage.disk_bytes
        root = self.run_directory.resolve(strict=True)
        if not root.is_dir() or root.is_symlink():
            raise OSError("disk accounting root is not a canonical directory")
        current: dict[str, int] = {}
        for candidate in root.rglob("*"):
            metadata = candidate.lstat()
            if stat.S_ISLNK(metadata.st_mode):
                continue
            if stat.S_ISREG(metadata.st_mode):
                current[candidate.relative_to(root).as_posix()] = metadata.st_size
        growth = sum(
            max(0, size - self._disk_baseline_sizes.get(relative, 0))
            for relative, size in current.items()
        )
        self.usage.disk_bytes = max(self.usage.disk_bytes, growth)
        self._last_disk_sample_monotonic = time.monotonic()
        return self.usage.disk_bytes

    @staticmethod
    def _termination_projection(attempt: SupervisedProcessAttempt) -> str | None:
        disposition = attempt.termination_disposition
        if disposition.startswith("sigterm_sent"):
            return "terminated"
        if disposition.startswith("sigkill_sent"):
            return "killed"
        return None

    @staticmethod
    def _retained_text(attempt_stream: Any) -> str:
        return attempt_stream.retained_tail.decode("utf-8", errors="replace")

    def _prelaunch_process_event(
        self,
        *,
        role: str,
        command: Sequence[str],
        started: dt.datetime,
        started_mono: float,
        supplied_input: bytes,
        input_limit_bytes: int,
        stdout_limit_bytes: int | None,
        stderr_limit_bytes: int | None,
        status: str,
        terminal_dimension: str | None,
        terminal_used: float | None,
        terminal_limit: float | None,
    ) -> dict[str, Any]:
        empty_digest = _sha256_bytes(b"")
        event = {
            "event_schema_version": 2,
            "event": "process_terminal",
            "role": role,
            "command": list(command),
            "pid": None,
            "started_at": started.isoformat(),
            "completed_at": _utc_now().isoformat(),
            "elapsed_seconds": time.monotonic() - started_mono,
            "returncode": None,
            "status": status,
            "terminal_dimension": terminal_dimension,
            "terminal_used": terminal_used,
            "terminal_limit": terminal_limit,
            "termination": "not_started",
            "stdin_bytes": len(supplied_input),
            "stdin_sha256": _sha256_bytes(supplied_input),
            "stdin_limit_bytes": input_limit_bytes,
            "stdin_written_bytes": 0,
            "stdin_write_incomplete": False,
            "stdin_write_error": None,
            "stdout": "",
            "stderr": "",
            "stdout_bytes": 0,
            "stderr_bytes": 0,
            "stdout_retained_bytes": 0,
            "stderr_retained_bytes": 0,
            "stdout_sha256": empty_digest,
            "stderr_sha256": empty_digest,
            "stdout_utf8_valid": True,
            "stderr_utf8_valid": True,
            "stdout_truncated": False,
            "stderr_truncated": False,
            "stdout_drain_incomplete": False,
            "stderr_drain_incomplete": False,
            "stdout_limit_bytes": stdout_limit_bytes,
            "stderr_limit_bytes": stderr_limit_bytes,
            "descendant_leak_detected": False,
            "capture_limit_bytes": self.capture_limit_bytes,
            "resource_measurement": self.measurement_boundaries(),
            "supervision_attempt": None,
            "resource_limit_execution": None,
            "post_supervision_acceptance": {
                "status": "not_run",
                "disk_snapshot_bytes": self.usage.disk_bytes,
                "disk_limit_bytes": self.budget.disk_bytes,
                "disk_limit_exceeded": self.usage.disk_bytes > self.budget.disk_bytes,
                "continuous_disk_observation": False,
                "snapshot_error": None,
                "acceptance_deadline_overrun": False,
            },
            "epistemic_effect": "none_operational_outcome_only",
        }
        self.events.append(event)
        return event

    def _run_process_v1_retired(
        self,
        command: Sequence[str],
        *,
        cwd: Path | str | None = None,
        env: Mapping[str, str] | None = None,
        role: str = "worker",
        input_bytes: bytes | None = None,
        input_limit_bytes: int | None = None,
        stdout_limit_bytes: int | None = None,
        stderr_limit_bytes: int | None = None,
    ) -> dict[str, Any]:
        """Run a command in an isolated process group under the hard deadline.

        Existing callers retain bounded diagnostic tails without treating total
        output as failure. Protocol callers can opt into bounded stdin and hard
        stdout/stderr byte ceilings. Exhaustion is always operational, never
        evidence about the requested scientific claim.
        """

        if not command or not all(isinstance(part, str) and part for part in command):
            raise ValueError("command must be a non-empty sequence of strings")
        allowed_roles = {
            "worker",
            "solver",
            "report_builder",
            "benchmark_runner",
            "human_evidence_verifier",
        }
        if role not in allowed_roles:
            raise ValueError(f"role must be one of {sorted(allowed_roles)}")
        if input_bytes is not None and not isinstance(input_bytes, bytes):
            raise ValueError("input_bytes must be bytes when supplied")
        effective_input_limit = (
            self.capture_limit_bytes if input_limit_bytes is None else input_limit_bytes
        )
        for name, value in (
            ("input_limit_bytes", effective_input_limit),
            ("stdout_limit_bytes", stdout_limit_bytes),
            ("stderr_limit_bytes", stderr_limit_bytes),
        ):
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int) or value <= 0
            ):
                raise ValueError(f"{name} must be a positive integer")
        self.checkpoint()
        workdir = Path(cwd).resolve() if cwd is not None else self.run_directory
        if self.allowed_working_directory is not None and workdir is not None:
            try:
                workdir.relative_to(self.allowed_working_directory)
            except ValueError as exc:
                raise ValueError("subprocess cwd must be inside the allowed working directory") from exc
        if workdir is not None:
            workdir.mkdir(parents=True, exist_ok=True)
        started = _utc_now()
        started_mono = time.monotonic()
        supplied_input = input_bytes or b""
        input_digest = "sha256:" + hashlib.sha256(supplied_input).hexdigest()
        if input_bytes is not None and len(input_bytes) > effective_input_limit:
            empty_digest = "sha256:" + hashlib.sha256(b"").hexdigest()
            event = {
                "event": "process_terminal",
                "role": role,
                "command": list(command),
                "pid": None,
                "started_at": started.isoformat(),
                "completed_at": _utc_now().isoformat(),
                "elapsed_seconds": time.monotonic() - started_mono,
                "returncode": None,
                "status": "input_exhausted",
                "terminal_dimension": "stdin_bytes",
                "terminal_used": len(input_bytes),
                "terminal_limit": effective_input_limit,
                "termination": "not_started",
                "stdin_bytes": len(input_bytes),
                "stdin_sha256": input_digest,
                "stdin_limit_bytes": effective_input_limit,
                "stdin_written_bytes": 0,
                "stdin_write_incomplete": False,
                "stdin_write_error": None,
                "stdout": "",
                "stderr": "",
                "stdout_bytes": 0,
                "stderr_bytes": 0,
                "stdout_retained_bytes": 0,
                "stderr_retained_bytes": 0,
                "stdout_sha256": empty_digest,
                "stderr_sha256": empty_digest,
                "stdout_utf8_valid": True,
                "stderr_utf8_valid": True,
                "stdout_truncated": False,
                "stderr_truncated": False,
                "stdout_drain_incomplete": False,
                "stderr_drain_incomplete": False,
                "stdout_limit_bytes": stdout_limit_bytes,
                "stderr_limit_bytes": stderr_limit_bytes,
                "descendant_leak_detected": False,
                "capture_limit_bytes": self.capture_limit_bytes,
                "resource_measurement": self.measurement_boundaries(),
                "epistemic_effect": "none_operational_outcome_only",
            }
            self.events.append(event)
            return event
        before = resource.getrusage(resource.RUSAGE_CHILDREN)
        child_environment = os.environ.copy()
        if env is not None:
            child_environment.update(env)
        child_environment.update(
            {
                "ABDUCER_ABSOLUTE_DEADLINE": self.deadline.isoformat(),
                "ABDUCER_BUDGET_ID": self.budget.budget_id,
                "ABDUCER_COST_LIMIT_USD": str(self.budget.cost_usd),
                "ABDUCER_NETWORK_LIMIT_BYTES": str(self.budget.network_bytes),
                "ABDUCER_TOKEN_LIMIT": str(self.budget.token_count),
                "ABDUCER_REQUEST_LIMIT": str(self.budget.request_count),
            }
        )
        process = subprocess.Popen(
            list(command),
            cwd=str(workdir) if workdir is not None else None,
            env=child_environment,
            stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            start_new_session=True,
            preexec_fn=self._preexec_limits if os.name == "posix" else None,
        )
        if process.stdout is None or process.stderr is None:
            raise RuntimeError("subprocess output pipes were not created")
        stdout_collector = _BoundedOutputCollector(process.stdout, self.capture_limit_bytes)
        stderr_collector = _BoundedOutputCollector(process.stderr, self.capture_limit_bytes)
        stdout_collector.start()
        stderr_collector.start()
        input_writer: _BoundedInputWriter | None = None
        if input_bytes is not None:
            if process.stdin is None:
                raise RuntimeError("subprocess stdin pipe was not created")
            input_writer = _BoundedInputWriter(process.stdin, input_bytes)
            input_writer.start()
        termination = None
        timed_out = False
        memory_exhausted = False
        disk_exhausted = False
        descendant_leak = False
        output_limit_hit: tuple[str, int, int] | None = None
        observed_peak_rss = 0
        while True:
            remaining = self.remaining_seconds()
            if remaining <= 0:
                timed_out = True
                termination = self._terminate_group(process, self.budget.grace_period_seconds)
                break
            try:
                process.wait(timeout=min(0.05, remaining))
                break
            except subprocess.TimeoutExpired:
                observed_rss = self._process_group_rss_bytes(process.pid)
                observed_peak_rss = max(observed_peak_rss, observed_rss)
                self.usage.peak_memory_bytes = max(self.usage.peak_memory_bytes, observed_rss)
                if observed_rss > self.budget.memory_bytes:
                    memory_exhausted = True
                    termination = self._terminate_group(process, self.budget.grace_period_seconds)
                    break
                if self._sample_disk_usage() > self.budget.disk_bytes:
                    disk_exhausted = True
                    termination = self._terminate_group(process, self.budget.grace_period_seconds)
                    break
                for dimension, collector, limit in (
                    ("stdout_bytes", stdout_collector, stdout_limit_bytes),
                    ("stderr_bytes", stderr_collector, stderr_limit_bytes),
                ):
                    if limit is not None and collector.total() > limit:
                        output_limit_hit = (dimension, collector.total(), limit)
                        termination = self._terminate_group(
                            process, self.budget.grace_period_seconds
                        )
                        break
                if output_limit_hit is not None:
                    break
        if self._process_group_exists(process.pid):
            descendant_leak = process.poll() is not None
            termination = self._terminate_group(process, self.budget.grace_period_seconds)
        # Pipe drainage never gains a fresh relative timeout.  In particular,
        # an inherited descriptor cannot extend the absolute job deadline.
        drain_deadline = self.deadline_monotonic
        (
            stdout,
            stdout_bytes,
            stdout_truncated,
            stdout_drain_incomplete,
            stdout_digest,
            stdout_utf8_valid,
            stdout_retained_bytes,
        ) = stdout_collector.finish(deadline_monotonic=drain_deadline)
        (
            stderr,
            stderr_bytes,
            stderr_truncated,
            stderr_drain_incomplete,
            stderr_digest,
            stderr_utf8_valid,
            stderr_retained_bytes,
        ) = stderr_collector.finish(deadline_monotonic=drain_deadline)
        stdin_written_bytes = 0
        stdin_write_incomplete = False
        stdin_write_error = None
        if input_writer is not None:
            stdin_written_bytes, stdin_write_incomplete, stdin_write_error = input_writer.finish(
                deadline_monotonic=drain_deadline
            )
        if output_limit_hit is None:
            if stdout_limit_bytes is not None and stdout_bytes > stdout_limit_bytes:
                output_limit_hit = ("stdout_bytes", stdout_bytes, stdout_limit_bytes)
            elif stderr_limit_bytes is not None and stderr_bytes > stderr_limit_bytes:
                output_limit_hit = ("stderr_bytes", stderr_bytes, stderr_limit_bytes)
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        elapsed = time.monotonic() - started_mono
        cpu = max(0.0, (after.ru_utime + after.ru_stime) - (before.ru_utime + before.ru_stime))
        maxrss = max(0, after.ru_maxrss) if after.ru_maxrss > before.ru_maxrss else 0
        peak_bytes = int(maxrss if platform.system() == "Darwin" else maxrss * 1024)
        self.usage.wall_time_seconds = max(self.usage.wall_time_seconds, time.monotonic() - self.started_monotonic)
        self.usage.cpu_seconds += cpu
        self.usage.peak_memory_bytes = max(
            self.usage.peak_memory_bytes, observed_peak_rss, peak_bytes
        )
        self._sample_disk_usage(force=True)

        returncode = process.returncode
        lower_error = stderr.lower()
        if timed_out:
            status = "deadline_exhausted"
        elif memory_exhausted:
            status = "out_of_memory"
        elif disk_exhausted:
            status = "disk_exhausted"
        elif output_limit_hit is not None:
            status = "output_exhausted"
        elif "memoryerror" in lower_error or "cannot allocate memory" in lower_error:
            status = "out_of_memory"
        elif returncode is not None and returncode < 0 and -returncode in {signal.SIGXCPU, signal.SIGKILL}:
            status = "cpu_exhausted" if -returncode == signal.SIGXCPU else "out_of_memory"
        elif (
            returncode is not None
            and returncode < 0
            and hasattr(signal, "SIGXFSZ")
            and -returncode == signal.SIGXFSZ
        ):
            status = "disk_exhausted"
        elif self.usage.disk_bytes > self.budget.disk_bytes or "file too large" in lower_error:
            status = "disk_exhausted"
        elif self.usage.peak_memory_bytes > self.budget.memory_bytes:
            status = "out_of_memory"
        elif self.usage.cpu_seconds > self.budget.cpu_seconds:
            status = "cpu_exhausted"
        elif input_writer is not None and (
            stdin_write_incomplete
            or stdin_write_error is not None
            or stdin_written_bytes != len(supplied_input)
        ):
            status = "worker_failed"
        elif descendant_leak or stdout_drain_incomplete or stderr_drain_incomplete:
            status = "report_failed" if role == "report_builder" else "worker_failed"
        elif returncode == 0:
            status = "succeeded"
        elif role == "report_builder":
            status = "report_failed"
        else:
            status = "worker_failed"
        event = {
            "event": "process_terminal",
            "role": role,
            "command": list(command),
            "pid": process.pid,
            "started_at": started.isoformat(),
            "completed_at": _utc_now().isoformat(),
            "elapsed_seconds": elapsed,
            "returncode": returncode,
            "status": status,
            "terminal_dimension": output_limit_hit[0] if output_limit_hit else None,
            "terminal_used": output_limit_hit[1] if output_limit_hit else None,
            "terminal_limit": output_limit_hit[2] if output_limit_hit else None,
            "termination": termination,
            "stdin_bytes": len(supplied_input),
            "stdin_sha256": input_digest,
            "stdin_limit_bytes": effective_input_limit if input_bytes is not None else None,
            "stdin_written_bytes": stdin_written_bytes,
            "stdin_write_incomplete": stdin_write_incomplete,
            "stdin_write_error": stdin_write_error,
            "stdout": stdout,
            "stderr": stderr,
            "stdout_bytes": stdout_bytes,
            "stderr_bytes": stderr_bytes,
            "stdout_retained_bytes": stdout_retained_bytes,
            "stderr_retained_bytes": stderr_retained_bytes,
            "stdout_sha256": stdout_digest,
            "stderr_sha256": stderr_digest,
            "stdout_utf8_valid": stdout_utf8_valid,
            "stderr_utf8_valid": stderr_utf8_valid,
            "stdout_truncated": stdout_truncated,
            "stderr_truncated": stderr_truncated,
            "stdout_drain_incomplete": stdout_drain_incomplete,
            "stderr_drain_incomplete": stderr_drain_incomplete,
            "stdout_limit_bytes": stdout_limit_bytes,
            "stderr_limit_bytes": stderr_limit_bytes,
            "descendant_leak_detected": descendant_leak,
            "capture_limit_bytes": self.capture_limit_bytes,
            "resource_measurement": self.measurement_boundaries(),
            "epistemic_effect": "none_operational_outcome_only" if status != "succeeded" else "awaiting_output_validation",
        }
        self.events.append(event)
        return event

    def run_process(
        self,
        command: Sequence[str],
        *,
        cwd: Path | str | None = None,
        env: Mapping[str, str] | None = None,
        replacement_environment: Mapping[str, str] | None = None,
        role: str = "worker",
        input_bytes: bytes | None = None,
        input_limit_bytes: int | None = None,
        stdout_limit_bytes: int | None = None,
        stderr_limit_bytes: int | None = None,
    ) -> dict[str, Any]:
        """Run a logical worker through sealed v2 supervision and projection.

        ``command`` remains the logical worker authority.  A distinct, sealed
        Python trampoline is the actual transport argv; it applies accurately
        scoped inherited kernel limits and then ``exec`` replaces itself with
        the logical worker.  Operational evidence has no scientific or
        epistemic authority.
        """

        if (
            not isinstance(command, Sequence)
            or isinstance(command, (str, bytes))
            or not command
            or any(
                not isinstance(part, str) or not part or "\x00" in part
                for part in command
            )
        ):
            raise ValueError("command must be a non-empty sequence of NUL-free strings")
        allowed_roles = {
            "worker",
            "solver",
            "report_builder",
            "benchmark_runner",
            "human_evidence_verifier",
        }
        if role not in allowed_roles:
            raise ValueError(f"role must be one of {sorted(allowed_roles)}")
        if input_bytes is not None and not isinstance(input_bytes, bytes):
            raise ValueError("input_bytes must be bytes when supplied")
        supplied_input = input_bytes or b""
        effective_input_limit = (
            self.capture_limit_bytes if input_limit_bytes is None else input_limit_bytes
        )
        for name, value in (
            ("input_limit_bytes", effective_input_limit),
            ("stdout_limit_bytes", stdout_limit_bytes),
            ("stderr_limit_bytes", stderr_limit_bytes),
        ):
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int) or value <= 0
            ):
                raise ValueError(f"{name} must be a positive integer")

        started = _utc_now()
        started_mono = time.monotonic()
        try:
            self.checkpoint()
        except BudgetExceeded as exc:
            return self._prelaunch_process_event(
                role=role,
                command=command,
                started=started,
                started_mono=started_mono,
                supplied_input=supplied_input,
                input_limit_bytes=effective_input_limit,
                stdout_limit_bytes=stdout_limit_bytes,
                stderr_limit_bytes=stderr_limit_bytes,
                status=exc.status,
                terminal_dimension=exc.dimension,
                terminal_used=exc.used,
                terminal_limit=exc.limit,
            )

        workdir = Path(cwd) if cwd is not None else self.run_directory or Path.cwd()
        if not workdir.is_absolute():
            workdir = (Path.cwd() / workdir).resolve()
        workdir.mkdir(parents=True, exist_ok=True)
        workdir = workdir.resolve(strict=True)
        if not workdir.is_dir() or workdir.is_symlink():
            raise ValueError("subprocess cwd must be a canonical non-symlink directory")
        if self.allowed_working_directory is not None:
            try:
                workdir.relative_to(self.allowed_working_directory)
            except ValueError as exc:
                raise ValueError(
                    "subprocess cwd must be inside the allowed working directory"
                ) from exc

        if len(supplied_input) > effective_input_limit:
            return self._prelaunch_process_event(
                role=role,
                command=command,
                started=started,
                started_mono=started_mono,
                supplied_input=supplied_input,
                input_limit_bytes=effective_input_limit,
                stdout_limit_bytes=stdout_limit_bytes,
                stderr_limit_bytes=stderr_limit_bytes,
                status="input_exhausted",
                terminal_dimension="stdin_bytes",
                terminal_used=len(supplied_input),
                terminal_limit=effective_input_limit,
            )

        execution_remaining_ns = int(
            max(0.0, self.deadline_monotonic - time.monotonic()) * 1_000_000_000
        )
        remaining_cpu_ns = int(
            max(0.0, self.budget.cpu_seconds - self.usage.cpu_seconds)
            * 1_000_000_000
        )
        if execution_remaining_ns <= 0:
            return self._prelaunch_process_event(
                role=role,
                command=command,
                started=started,
                started_mono=started_mono,
                supplied_input=supplied_input,
                input_limit_bytes=effective_input_limit,
                stdout_limit_bytes=stdout_limit_bytes,
                stderr_limit_bytes=stderr_limit_bytes,
                status="deadline_exhausted",
                terminal_dimension="wall_time_seconds",
                terminal_used=time.monotonic() - self.started_monotonic,
                terminal_limit=self.budget.wall_time_seconds,
            )
        if remaining_cpu_ns <= 0:
            return self._prelaunch_process_event(
                role=role,
                command=command,
                started=started,
                started_mono=started_mono,
                supplied_input=supplied_input,
                input_limit_bytes=effective_input_limit,
                stdout_limit_bytes=stdout_limit_bytes,
                stderr_limit_bytes=stderr_limit_bytes,
                status="cpu_exhausted",
                terminal_dimension="cpu_seconds",
                terminal_used=self.usage.cpu_seconds,
                terminal_limit=self.budget.cpu_seconds,
            )

        child_environment, used_replacement_environment = (
            self._build_exact_child_environment(
                env=env,
                replacement_environment=replacement_environment,
            )
        )
        python_executable = Path(sys.executable).resolve(strict=True)
        resource_exec_launcher = (
            Path(__file__).resolve(strict=True).parents[1]
            / "process_resource_exec.py"
        ).resolve(strict=True)
        pre_authority = _resource_exec_authority_observation(
            python_executable=python_executable,
            launcher=resource_exec_launcher,
        )
        plan = ResourceExecPlan.build(
            logical_argv=command,
            cwd=workdir,
            environment=child_environment,
            remaining_cpu_ns=remaining_cpu_ns,
            cpu_grace_ns=int(self.budget.grace_period_seconds * 1_000_000_000),
            workspace_disk_bytes=self.budget.disk_bytes,
            process_memory_bytes=self.budget.memory_bytes,
        )
        transport_argv = [
            str(python_executable),
            "-I",
            "-B",
            str(resource_exec_launcher),
            "--resource-plan-base64",
            plan.base64_token(),
            "--",
            *command,
        ]
        limits = self._build_supervision_limits(
            execution_remaining_ns=execution_remaining_ns,
            remaining_cpu_ns=remaining_cpu_ns,
            input_limit_bytes=effective_input_limit,
            stdout_limit_bytes=stdout_limit_bytes,
            stderr_limit_bytes=stderr_limit_bytes,
        )
        post_acceptance_deadline_ns = (
            time.monotonic_ns() + limits.total_deadline_ns + 250_000_000
        )
        attempt = run_supervised_process(
            transport_argv,
            cwd=workdir,
            environment=child_environment,
            input_bytes=supplied_input,
            limits=limits,
        )

        authority_error: str | None = None
        post_authority: dict[str, Any] | None
        try:
            post_authority = _resource_exec_authority_observation(
                python_executable=python_executable,
                launcher=resource_exec_launcher,
            )
        except (OSError, ValueError) as exc:
            post_authority = None
            authority_error = f"{type(exc).__name__}: {exc}"
        authority_exact = post_authority == pre_authority and authority_error is None
        request_transport_exact = attempt.request.argv == tuple(transport_argv)
        if not request_transport_exact:
            authority_exact = False
            authority_error = "supervised request transport argv differs from sealed transport"
        resource_limit_execution = {
            "schema_version": _RESOURCE_LIMIT_EXECUTION_SCHEMA_VERSION,
            "authority_kind": "trusted_local_resource_limit_execution",
            "logical_argv_digest": digest_value(list(command)),
            "transport_argv_digest": digest_value(transport_argv),
            "supervised_request_digest": attempt.request.request_digest,
            "supervised_transport_exact": request_transport_exact,
            "replacement_environment_used": used_replacement_environment,
            "environment_digest": plan.environment_digest,
            "capture_limit_bytes": self.capture_limit_bytes,
            "resource_exec_plan": plan.as_dict(),
            "resource_exec_plan_digest": plan.digest(),
            "pre_execution_observation": pre_authority,
            "post_execution_observation": post_authority,
            "observation_status": "exact_match" if authority_exact else "mismatch",
            "observation_error": authority_error,
            "cryptographic_authenticity": False,
            "authority_boundary": _RESOURCE_LIMIT_AUTHORITY_BOUNDARY,
        }

        cpu_ns = (attempt.wait4_accounted_user_cpu_ns or 0) + (
            attempt.wait4_accounted_system_cpu_ns or 0
        )
        self.usage.cpu_seconds += cpu_ns / 1_000_000_000
        self.usage.peak_memory_bytes = max(
            self.usage.peak_memory_bytes,
            attempt.wait4_ru_maxrss_normalized_bytes or 0,
            attempt.peak_observed_sampled_original_group_rss_bytes or 0,
        )
        self.usage.wall_time_seconds = max(
            self.usage.wall_time_seconds,
            time.monotonic() - self.started_monotonic,
        )

        disk_snapshot_error: str | None = None
        try:
            disk_snapshot_bytes = self._strict_post_exit_disk_snapshot()
        except OSError as exc:
            disk_snapshot_bytes = self.usage.disk_bytes
            disk_snapshot_error = f"{type(exc).__name__}: {exc}"
        acceptance_deadline_overrun = time.monotonic_ns() > post_acceptance_deadline_ns
        disk_limit_exceeded = disk_snapshot_bytes > self.budget.disk_bytes
        post_acceptance = {
            "status": (
                "snapshot_failed"
                if disk_snapshot_error is not None
                else "deadline_overrun"
                if acceptance_deadline_overrun
                else "rejected"
                if disk_limit_exceeded
                else "accepted"
            ),
            "disk_snapshot_bytes": disk_snapshot_bytes,
            "disk_limit_bytes": self.budget.disk_bytes,
            "disk_limit_exceeded": disk_limit_exceeded,
            "continuous_disk_observation": False,
            "snapshot_error": disk_snapshot_error,
            "acceptance_deadline_overrun": acceptance_deadline_overrun,
        }

        projection = _v2_governor_outcome_projection(
            attempt,
            role=role,
            plan=plan,
            post_acceptance=post_acceptance,
            authority_exact=authority_exact,
        )
        status = str(projection["status"])
        event = {
            "event_schema_version": 2,
            "event": "process_terminal",
            "role": role,
            "command": list(command),
            "pid": attempt.pid,
            "started_at": started.isoformat(),
            "completed_at": _utc_now().isoformat(),
            "elapsed_seconds": time.monotonic() - started_mono,
            "returncode": attempt.returncode,
            "status": status,
            "terminal_dimension": projection["terminal_dimension"],
            "terminal_used": projection["terminal_used"],
            "terminal_limit": projection["terminal_limit"],
            "termination": projection["termination"],
            "stdin_bytes": len(supplied_input),
            "stdin_sha256": _sha256_bytes(supplied_input),
            "stdin_limit_bytes": effective_input_limit,
            "stdin_written_bytes": attempt.stdin_enqueued_bytes,
            "stdin_write_incomplete": not attempt.stdin_fully_enqueued,
            "stdin_write_error": projection["stdin_write_error"],
            "stdout": self._retained_text(attempt.stdout),
            "stderr": self._retained_text(attempt.stderr),
            "stdout_bytes": attempt.stdout.captured_bytes,
            "stderr_bytes": attempt.stderr.captured_bytes,
            "stdout_retained_bytes": len(attempt.stdout.retained_tail),
            "stderr_retained_bytes": len(attempt.stderr.retained_tail),
            "stdout_sha256": attempt.stdout.captured_sha256,
            "stderr_sha256": attempt.stderr.captured_sha256,
            "stdout_utf8_valid": attempt.stdout.utf8_valid_retained_tail,
            "stderr_utf8_valid": attempt.stderr.utf8_valid_retained_tail,
            "stdout_truncated": (
                attempt.stdout.captured_bytes > len(attempt.stdout.retained_tail)
            ),
            "stderr_truncated": (
                attempt.stderr.captured_bytes > len(attempt.stderr.retained_tail)
            ),
            "stdout_drain_incomplete": not attempt.stdout.capture_complete,
            "stderr_drain_incomplete": not attempt.stderr.capture_complete,
            "stdout_limit_bytes": stdout_limit_bytes,
            "stderr_limit_bytes": stderr_limit_bytes,
            "descendant_leak_detected": projection["descendant_leak_detected"],
            "capture_limit_bytes": self.capture_limit_bytes,
            "resource_measurement": self.measurement_boundaries(),
            "supervision_attempt": attempt.as_dict(),
            "resource_limit_execution": resource_limit_execution,
            "post_supervision_acceptance": post_acceptance,
            "epistemic_effect": projection["epistemic_effect"],
        }
        self.events.append(event)
        return event

    def receipt(self, status: str) -> dict[str, Any]:
        if status not in TERMINAL_STATUSES:
            raise ValueError(f"invalid terminal status: {status}")
        return {
            "budget": asdict(self.budget),
            "usage": asdict(self.usage),
            "status": status,
            "events": list(self.events),
            "deadline": self.deadline.isoformat(),
            "resource_measurement": self.measurement_boundaries(),
        }


@dataclass
class PortfolioBudget:
    """Independent branch governors plus a protected unallocated reserve."""

    raw: Mapping[str, Any]
    run_directory: Path
    governors: dict[str, ResourceGovernor] = field(default_factory=dict)

    def __post_init__(self) -> None:
        reserve = _positive_number(self.raw.get("portfolio_reserve_fraction", 0.0), "portfolio_reserve_fraction", allow_zero=True)
        if reserve >= 1:
            raise ValueError("portfolio_reserve_fraction must be below one")
        per_branch = self.raw.get("per_branch")
        if not isinstance(per_branch, Mapping) or not per_branch:
            raise ValueError("portfolio budget requires explicit per_branch budgets")
        additive_dimensions = ("cpu_seconds", "disk_bytes", "network_bytes", "token_count", "request_count", "cost_usd")
        for dimension in additive_dimensions:
            total = float(self.raw.get(dimension, 0.0))
            allocated = sum(float(row.get(dimension, 0.0)) for row in per_branch.values() if isinstance(row, Mapping))
            spendable = total * (1.0 - reserve)
            if allocated > spendable + 1e-12:
                raise ValueError(f"branch {dimension} allocations consume the protected portfolio reserve")
        # Concurrent workers can overlap wall time, but each branch must still
        # fit the portfolio's wall and peak-memory envelopes individually.
        for branch_id, row in per_branch.items():
            if float(row.get("wall_time_seconds", 0.0)) > float(self.raw.get("wall_time_seconds", 0.0)):
                raise ValueError(f"branch {branch_id!r} wall budget exceeds portfolio wall budget")
            if float(row.get("memory_bytes", 0.0)) > float(self.raw.get("memory_bytes", 0.0)):
                raise ValueError(f"branch {branch_id!r} memory budget exceeds portfolio memory budget")

    def governor_for(self, branch_id: str) -> ResourceGovernor:
        branch_id = validate_job_id(branch_id)
        if branch_id not in self.governors:
            branch_dir = contained_path(self.run_directory, "branches", branch_id)
            branch_dir.mkdir(parents=True, exist_ok=True)
            self.governors[branch_id] = ResourceGovernor.from_mapping(
                self.raw,
                run_directory=branch_dir,
                branch_id=branch_id,
            )
        return self.governors[branch_id]

    def aggregate_usage(self) -> ResourceUsage:
        total = ResourceUsage()
        for governor in self.governors.values():
            total.add(governor.usage)
        return total


def selective_retry_schedule(
    branch_results: Sequence[Mapping[str, Any]],
    *,
    dependency_invalidations: Mapping[str, Sequence[str]] | None = None,
) -> list[dict[str, Any]]:
    """Schedule only failed/invalid/stale branches or explicitly invalidated dependants."""

    invalidations = dependency_invalidations or {}
    by_id = {str(row.get("branch_id")): row for row in branch_results}
    retry: dict[str, dict[str, Any]] = {}
    failed_ids: set[str] = set()
    for branch_id, row in by_id.items():
        status = str(row.get("status"))
        validated = bool(row.get("validated", False))
        literature_current = bool(row.get("literature_current", True))
        if status in RETRYABLE_STATUSES or not validated or not literature_current:
            reason = status if status in RETRYABLE_STATUSES else ("invalid" if not validated else "literature_superseded")
            retry[branch_id] = {"branch_id": branch_id, "reason": reason, "preserve_successful_siblings": True}
            failed_ids.add(branch_id)
    for failed_id in sorted(failed_ids):
        for dependant in invalidations.get(failed_id, ()):
            if dependant in by_id:
                retry.setdefault(
                    dependant,
                    {
                        "branch_id": dependant,
                        "reason": f"dependency_invalidated:{failed_id}",
                        "preserve_successful_siblings": True,
                    },
                )
    return [retry[key] for key in sorted(retry)]


def partial_result_partition(branch_results: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Retain validated successes independently from retryable failures."""

    retained = [
        dict(row)
        for row in branch_results
        if row.get("status") == "succeeded" and row.get("validated") is True and row.get("literature_current", True) is True
    ]
    return {
        "retained_successes": retained,
        "retry_schedule": selective_retry_schedule(branch_results),
        "partial_failure": bool(retained) and len(retained) != len(branch_results),
    }


def write_structured_job_log(path: Path | str, payload: Mapping[str, Any]) -> None:
    """Persist the full structured log without accepting an escaping path."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    target.write_text(encoded, encoding="utf-8")
