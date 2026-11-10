# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Closed operational supervision for one trusted local protocol process.

This module is deliberately below discovery, experiment, and scientific
semantics.  It binds one exact request, transports bounded protocol bytes,
observes a POSIX process group, and returns a strictly validated attempt
record.  It does not establish hard containment, truth, novelty, experiment
value, or physics authority.

The direct child is deliberately left unreaped until every operation on its
numeric process-group identifier is finished.  Its unreaped PID is therefore
the identity anchor that prevents a fast-exit/PID-reuse race.  Required group
sampling is performed only by a fixed, separately supervised ``ps`` sidecar;
callers cannot inject an unbounded Python sampler callback.

The monotonic deadline covers parent-observed operational work through stream
evidence sealing.  Python cannot pre-empt a kernel-blocked spawn, close,
signal, or wait operation.  Any overrun visible after such an operation
returns is recorded and makes success impossible.  JSON serialization after
the evidence seal is outside that operational deadline.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import platform
import re
import selectors
import signal
import subprocess
import time
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Literal, Mapping, Sequence


PROCESS_ATTEMPT_SCHEMA_VERSION = "2.0.0"
PROCESS_ATTEMPT_KIND = "trusted_local_protocol_process_attempt"
CONTAINMENT_MODE = "trusted_worker_posix_anchored_process_group_observation"
AUTHORITY_BOUNDARY = (
    "operational_process_evidence_only_no_semantic_scientific_truth_proof_"
    "experiment_value_or_physics_authority"
)

_READ_CHUNK_BYTES = 64 * 1024
_SELECT_QUANTUM_NS = 20_000_000
_FAILURE_MESSAGE_BYTES = 4096
_PS_EXECUTABLE_CANDIDATES = ("/bin/ps", "/usr/bin/ps")
_SHA256_PREFIX = "sha256:"
_MAX_FAILURE_EVENTS = 128
_MAX_DIAGNOSTIC_EVENTS = 128
_EVENT_TOKEN_RE = re.compile(r"^[a-z][a-z0-9_]{0,126}$")
_FAILURE_CATEGORIES = {"cleanup", "operational", "policy", "worker"}
_DIAGNOSTIC_CATEGORIES = {"diagnostic"}
_FAILURE_STAGES = {
    "descriptor_cleanup",
    "evidence_seal",
    "execution",
    "host_control_cleanup",
    "launch",
    "launch_setup",
    "prelaunch",
    "process_cleanup",
    "process_exit",
    "process_wait",
    "resource_observation",
    "sampling",
    "selector",
    "supervisor",
    "transport",
}
_FAILURE_REASON_CODES = {
    "cleanup_host_exception_suppressed",
    "diagnostic_ledger_capacity_exhausted",
    "direct_child_not_reaped",
    "direct_child_not_reaped_before_cleanup_deadline",
    "direct_child_wait_failed",
    "execution_deadline_exhausted",
    "execution_ended_without_both_output_eofs",
    "failure_ledger_capacity_exhausted",
    "final_group_no_signalable_member",
    "fresh_session_observation_mismatch",
    "input_limit_exceeded",
    "launch_consumed_execution_deadline",
    "leader_ownership_lost",
    "leader_reap_before_group_actions_finalized_blocked",
    "observed_wait4_cpu_threshold_exceeded",
    "observed_wait4_normalized_maxrss_threshold_exceeded",
    "original_group_signal_failed",
    "pipe_creation_failed",
    "post_reap_original_group_operation_blocked",
    "post_reap_original_group_sampling_blocked",
    "process_launch_failed",
    "request_preparation_consumed_execution_deadline",
    "required_sampling_observation_missing",
    "sampled_original_group_member_threshold_exceeded",
    "sampled_original_group_rss_threshold_exceeded",
    "sampler_budget_unavailable",
    "sampler_cleanup_select_failed",
    "sampler_cleanup_wait_failed",
    "sampler_deadline_exhausted",
    "sampler_descriptor_close_failed",
    "sampler_exit_nonzero",
    "sampler_launch_failed",
    "sampler_not_reaped",
    "sampler_not_reaped_before_deadline",
    "sampler_process_reap_count_mismatch",
    "sampler_read_failed",
    "sampler_result_missing",
    "sampler_select_failed",
    "sampler_selector_close_failed",
    "sampler_sigkill_failed",
    "sampler_wait_failed",
    "sampling_executable_unavailable",
    "selector_close_failed",
    "selector_map_failed",
    "selector_select_failed",
    "selector_setup_failed",
    "session_observation_failed",
    "session_observation_unavailable",
    "stderr_close_failed",
    "stderr_close_unverified",
    "stderr_limit_exceeded",
    "stderr_read_failed",
    "stderr_selector_unregister_failed",
    "stdin_close_failed",
    "stdin_close_unverified",
    "stdin_incomplete",
    "stdin_selector_unregister_failed",
    "stdin_write_failed",
    "stdout_close_failed",
    "stdout_close_unverified",
    "stdout_limit_exceeded",
    "stdout_read_failed",
    "stdout_selector_unregister_failed",
    "supervisor_internal_exception",
    "total_deadline_overrun_detected",
    "unsupported_platform",
    "worker_exit_nonzero",
}
_SAMPLER_RESULT_REASON_CODES = {
    "sampler_cleanup_select_failed",
    "sampler_cleanup_wait_failed",
    "sampler_deadline_exhausted",
    "sampler_descriptor_close_failed",
    "sampler_exit_nonzero",
    "sampler_launch_failed",
    "sampler_not_reaped_before_deadline",
    "sampler_read_failed",
    "sampler_select_failed",
    "sampler_selector_close_failed",
    "sampler_sigkill_failed",
    "sampler_wait_failed",
}
_FAILURE_VARIANTS = frozenset(
    {
        ("cleanup", "descriptor_cleanup", "selector_close_failed"),
        ("cleanup", "descriptor_cleanup", "selector_map_failed"),
        ("cleanup", "host_control_cleanup", "cleanup_host_exception_suppressed"),
        (
            "cleanup",
            "process_cleanup",
            "post_reap_original_group_operation_blocked",
        ),
        ("cleanup", "process_cleanup", "original_group_signal_failed"),
        (
            "cleanup",
            "process_wait",
            "direct_child_not_reaped_before_cleanup_deadline",
        ),
        ("cleanup", "process_wait", "direct_child_wait_failed"),
        ("cleanup", "process_wait", "leader_ownership_lost"),
        (
            "cleanup",
            "process_wait",
            "leader_reap_before_group_actions_finalized_blocked",
        ),
        ("cleanup", "sampling", "post_reap_original_group_sampling_blocked"),
        ("cleanup", "sampling", "sampler_not_reaped"),
        ("cleanup", "sampling", "sampler_process_reap_count_mismatch"),
        ("diagnostic", "process_cleanup", "final_group_no_signalable_member"),
        ("diagnostic", "sampling", "sampler_budget_unavailable"),
        ("diagnostic", "supervisor", "diagnostic_ledger_capacity_exhausted"),
        ("operational", "evidence_seal", "total_deadline_overrun_detected"),
        ("operational", "execution", "execution_deadline_exhausted"),
        (
            "operational",
            "execution",
            "execution_ended_without_both_output_eofs",
        ),
        ("operational", "launch", "launch_consumed_execution_deadline"),
        ("operational", "launch", "pipe_creation_failed"),
        ("operational", "launch", "process_launch_failed"),
        ("operational", "launch_setup", "fresh_session_observation_mismatch"),
        ("operational", "launch_setup", "selector_setup_failed"),
        ("operational", "launch_setup", "session_observation_failed"),
        ("operational", "launch_setup", "session_observation_unavailable"),
        ("operational", "prelaunch", "request_preparation_consumed_execution_deadline"),
        ("operational", "prelaunch", "sampling_executable_unavailable"),
        ("operational", "prelaunch", "unsupported_platform"),
        ("operational", "process_wait", "direct_child_not_reaped"),
        ("operational", "sampling", "required_sampling_observation_missing"),
        ("operational", "sampling", "sampler_budget_unavailable"),
        ("operational", "sampling", "sampler_result_missing"),
        ("operational", "selector", "selector_map_failed"),
        ("operational", "selector", "selector_select_failed"),
        ("operational", "supervisor", "failure_ledger_capacity_exhausted"),
        ("operational", "supervisor", "supervisor_internal_exception"),
        ("operational", "transport", "stdin_incomplete"),
        ("operational", "transport", "stdin_write_failed"),
        ("policy", "prelaunch", "input_limit_exceeded"),
        (
            "policy",
            "resource_observation",
            "observed_wait4_cpu_threshold_exceeded",
        ),
        (
            "policy",
            "resource_observation",
            "observed_wait4_normalized_maxrss_threshold_exceeded",
        ),
        (
            "policy",
            "sampling",
            "sampled_original_group_member_threshold_exceeded",
        ),
        (
            "policy",
            "sampling",
            "sampled_original_group_rss_threshold_exceeded",
        ),
        ("worker", "process_exit", "worker_exit_nonzero"),
    }
    | {
        ("cleanup", "descriptor_cleanup", f"{label}_{suffix}")
        for label in ("stdin", "stdout", "stderr")
        for suffix in (
            "close_failed",
            "close_unverified",
            "selector_unregister_failed",
        )
    }
    | {
        ("operational", "transport", f"{label}_read_failed")
        for label in ("stdout", "stderr")
    }
    | {
        ("policy", "transport", f"{label}_limit_exceeded")
        for label in ("stdout", "stderr")
    }
    | {
        (category, "sampling", reason)
        for category in ("operational", "diagnostic")
        for reason in _SAMPLER_RESULT_REASON_CODES
    }
)
_SUCCESS_FINAL_GROUP_DISPOSITIONS = {
    "final_group_quiescence_sigkill_sent",
    "final_group_quiescence_sigkill_sent_no_signalable_member",
}
_TERMINATION_DISPOSITIONS = {
    "not_started",
    "running_anchored",
    "final_group_quiescence_sigkill_sent",
    "final_group_quiescence_sigkill_sent_no_signalable_member",
    "sigterm_sent",
    "sigterm_sent_no_signalable_member",
    "sigkill_sent",
    "sigkill_sent_no_signalable_member",
}


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _bytes_digest(value: bytes) -> str:
    return _SHA256_PREFIX + hashlib.sha256(value).hexdigest()


def _value_digest(value: Any) -> str:
    return _bytes_digest(_canonical_json(value))


def _is_sha256(value: object) -> bool:
    if not isinstance(value, str) or not value.startswith(_SHA256_PREFIX):
        return False
    suffix = value[len(_SHA256_PREFIX) :]
    return len(suffix) == 64 and all(character in "0123456789abcdef" for character in suffix)


def _require_exact_keys(raw: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(raw)
    if actual != expected:
        raise ValueError(
            f"{label} keys differ: missing={sorted(expected - actual)!r}, "
            f"extra={sorted(actual - expected)!r}"
        )


def _positive_int(value: object, label: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{label} must be a positive integer")
    return value


def _optional_positive_int(value: object, label: str) -> int | None:
    if value is None:
        return None
    return _positive_int(value, label)


@dataclass(frozen=True, slots=True)
class ProcessGroupSamplingPolicy:
    """Fixed sampling policy; ``posix_ps`` is the only executable sampler."""

    mode: Literal["disabled", "posix_ps"]
    required: bool
    interval_ns: int
    attempt_timeout_ns: int
    cleanup_reserve_ns: int
    stdout_limit_bytes: int
    stderr_limit_bytes: int
    maximum_attempts: int = 64
    reject_if_observed_members_above: int | None = None
    reject_if_observed_rss_bytes_above: int | None = None

    def __post_init__(self) -> None:
        if self.mode not in {"disabled", "posix_ps"}:
            raise ValueError("sampling mode must be disabled or posix_ps")
        if type(self.required) is not bool:
            raise ValueError("sampling required must be boolean")
        for name in (
            "interval_ns",
            "attempt_timeout_ns",
            "cleanup_reserve_ns",
            "stdout_limit_bytes",
            "stderr_limit_bytes",
            "maximum_attempts",
        ):
            _positive_int(getattr(self, name), f"sampling.{name}")
        if self.cleanup_reserve_ns >= self.attempt_timeout_ns:
            raise ValueError("sampling cleanup reserve must be below its attempt timeout")
        for name in (
            "reject_if_observed_members_above",
            "reject_if_observed_rss_bytes_above",
        ):
            _optional_positive_int(getattr(self, name), f"sampling.{name}")
        if self.mode == "disabled" and self.required:
            raise ValueError("disabled sampling cannot be required")
        if self.mode == "disabled" and (
            self.reject_if_observed_members_above is not None
            or self.reject_if_observed_rss_bytes_above is not None
        ):
            raise ValueError("disabled sampling cannot carry observation thresholds")

    def as_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "required": self.required,
            "interval_ns": self.interval_ns,
            "attempt_timeout_ns": self.attempt_timeout_ns,
            "cleanup_reserve_ns": self.cleanup_reserve_ns,
            "stdout_limit_bytes": self.stdout_limit_bytes,
            "stderr_limit_bytes": self.stderr_limit_bytes,
            "maximum_attempts": self.maximum_attempts,
            "reject_if_observed_members_above": self.reject_if_observed_members_above,
            "reject_if_observed_rss_bytes_above": self.reject_if_observed_rss_bytes_above,
        }

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "ProcessGroupSamplingPolicy":
        if not isinstance(raw, Mapping):
            raise ValueError("sampling policy must be a mapping")
        _require_exact_keys(raw, {field.name for field in fields(cls)}, "sampling policy")
        return cls(**dict(raw))


@dataclass(frozen=True, slots=True)
class SupervisionLimits:
    """Fixed transport, deadline, observation, and acceptance thresholds."""

    total_deadline_ns: int
    cleanup_reserve_ns: int
    termination_grace_ns: int
    evidence_seal_reserve_ns: int
    stdin_limit_bytes: int
    stdout_limit_bytes: int | None
    stderr_limit_bytes: int | None
    stdout_retained_tail_bytes: int
    stderr_retained_tail_bytes: int
    sampling: ProcessGroupSamplingPolicy
    reject_if_observed_wait4_cpu_ns_above: int | None = None
    reject_if_observed_wait4_normalized_maxrss_bytes_above: int | None = None

    def __post_init__(self) -> None:
        for name in (
            "total_deadline_ns",
            "cleanup_reserve_ns",
            "evidence_seal_reserve_ns",
            "stdin_limit_bytes",
            "stdout_retained_tail_bytes",
            "stderr_retained_tail_bytes",
        ):
            _positive_int(getattr(self, name), name)
        if type(self.termination_grace_ns) is not int or self.termination_grace_ns < 0:
            raise ValueError("termination_grace_ns must be a non-negative integer")
        for name in ("stdout_limit_bytes", "stderr_limit_bytes"):
            _optional_positive_int(getattr(self, name), name)
        if not isinstance(self.sampling, ProcessGroupSamplingPolicy):
            raise ValueError("sampling must be ProcessGroupSamplingPolicy")
        if self.cleanup_reserve_ns >= self.total_deadline_ns:
            raise ValueError("cleanup reserve must be below total deadline")
        if (
            self.termination_grace_ns + self.evidence_seal_reserve_ns
            >= self.cleanup_reserve_ns
        ):
            raise ValueError(
                "cleanup reserve must strictly exceed termination grace plus evidence seal reserve"
            )
        if (
            self.stdout_limit_bytes is not None
            and self.stdout_retained_tail_bytes > self.stdout_limit_bytes
        ):
            raise ValueError("stdout retained tail cannot exceed its ceiling")
        if (
            self.stderr_limit_bytes is not None
            and self.stderr_retained_tail_bytes > self.stderr_limit_bytes
        ):
            raise ValueError("stderr retained tail cannot exceed its ceiling")
        for name in (
            "reject_if_observed_wait4_cpu_ns_above",
            "reject_if_observed_wait4_normalized_maxrss_bytes_above",
        ):
            _optional_positive_int(getattr(self, name), name)
        if (
            self.reject_if_observed_wait4_normalized_maxrss_bytes_above is not None
            and platform.system() not in {"Darwin", "Linux"}
        ):
            raise ValueError("normalized wait4 maxrss threshold is unsupported on this host")

    def as_dict(self) -> dict[str, Any]:
        return {
            "total_deadline_ns": self.total_deadline_ns,
            "cleanup_reserve_ns": self.cleanup_reserve_ns,
            "termination_grace_ns": self.termination_grace_ns,
            "evidence_seal_reserve_ns": self.evidence_seal_reserve_ns,
            "stdin_limit_bytes": self.stdin_limit_bytes,
            "stdout_limit_bytes": self.stdout_limit_bytes,
            "stderr_limit_bytes": self.stderr_limit_bytes,
            "stdout_retained_tail_bytes": self.stdout_retained_tail_bytes,
            "stderr_retained_tail_bytes": self.stderr_retained_tail_bytes,
            "sampling": self.sampling.as_dict(),
            "reject_if_observed_wait4_cpu_ns_above": (
                self.reject_if_observed_wait4_cpu_ns_above
            ),
            "reject_if_observed_wait4_normalized_maxrss_bytes_above": (
                self.reject_if_observed_wait4_normalized_maxrss_bytes_above
            ),
        }

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "SupervisionLimits":
        if not isinstance(raw, Mapping):
            raise ValueError("limits must be a mapping")
        expected = {field.name for field in fields(cls)}
        _require_exact_keys(raw, expected, "supervision limits")
        values = dict(raw)
        values["sampling"] = ProcessGroupSamplingPolicy.from_mapping(values["sampling"])
        return cls(**values)


@dataclass(frozen=True, slots=True)
class ProcessRequestBinding:
    """Secret-safe, deterministic identity of an exact process request."""

    argv: tuple[str, ...]
    argv_digest: str
    cwd: str
    environment_bindings: tuple[tuple[str, str], ...]
    environment_digest: str
    stdin_bytes: int
    stdin_sha256: str
    limits_digest: str
    sampling_executable: str | None
    request_digest: str

    @property
    def environment_keys(self) -> tuple[str, ...]:
        return tuple(name for name, _digest in self.environment_bindings)

    def as_dict(self) -> dict[str, Any]:
        return {
            "argv": list(self.argv),
            "argv_digest": self.argv_digest,
            "cwd": self.cwd,
            "environment_bindings": [
                {"name": name, "value_sha256": digest}
                for name, digest in self.environment_bindings
            ],
            "environment_digest": self.environment_digest,
            "stdin_bytes": self.stdin_bytes,
            "stdin_sha256": self.stdin_sha256,
            "limits_digest": self.limits_digest,
            "sampling_executable": self.sampling_executable,
            "request_digest": self.request_digest,
        }

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "ProcessRequestBinding":
        if not isinstance(raw, Mapping):
            raise ValueError("request binding must be a mapping")
        _require_exact_keys(
            raw,
            {
                "argv",
                "argv_digest",
                "cwd",
                "environment_bindings",
                "environment_digest",
                "stdin_bytes",
                "stdin_sha256",
                "limits_digest",
                "sampling_executable",
                "request_digest",
            },
            "request binding",
        )
        argv_raw = raw["argv"]
        if not isinstance(argv_raw, list):
            raise ValueError("request argv must be a canonical JSON list")
        bindings_raw = raw["environment_bindings"]
        if not isinstance(bindings_raw, list):
            raise ValueError("environment_bindings must be a list")
        bindings: list[tuple[str, str]] = []
        for index, row in enumerate(bindings_raw):
            if not isinstance(row, Mapping):
                raise ValueError(f"environment binding {index} must be a mapping")
            _require_exact_keys(row, {"name", "value_sha256"}, "environment binding")
            bindings.append((row["name"], row["value_sha256"]))
        instance = cls(
            argv=tuple(argv_raw),
            argv_digest=raw["argv_digest"],
            cwd=raw["cwd"],
            environment_bindings=tuple(bindings),
            environment_digest=raw["environment_digest"],
            stdin_bytes=raw["stdin_bytes"],
            stdin_sha256=raw["stdin_sha256"],
            limits_digest=raw["limits_digest"],
            sampling_executable=raw["sampling_executable"],
            request_digest=raw["request_digest"],
        )
        _validate_request_binding(instance)
        return instance


def _validated_invocation(
    argv: Sequence[str],
    cwd: Path | str,
    environment: Mapping[str, str],
    input_bytes: bytes,
) -> tuple[tuple[str, ...], str, dict[str, str], bytes]:
    if (
        not isinstance(argv, Sequence)
        or isinstance(argv, (str, bytes))
        or not argv
        or any(
            not isinstance(part, str) or not part or "\x00" in part
            for part in argv
        )
    ):
        raise ValueError("argv must be a non-empty sequence of non-NUL strings")
    raw_cwd = Path(cwd)
    if not raw_cwd.is_absolute():
        raise ValueError("cwd must be an absolute canonical directory")
    resolved_cwd = raw_cwd.resolve(strict=True)
    if raw_cwd != resolved_cwd or raw_cwd.is_symlink() or not resolved_cwd.is_dir():
        raise ValueError("cwd must be an absolute non-symlink canonical directory")
    if not isinstance(environment, Mapping):
        raise ValueError("environment must be a string mapping")
    clean_environment: dict[str, str] = {}
    for name, value in environment.items():
        if (
            not isinstance(name, str)
            or not name
            or "=" in name
            or "\x00" in name
            or not isinstance(value, str)
            or "\x00" in value
        ):
            raise ValueError("environment names and values must be exact strings")
        clean_environment[name] = value
    if not isinstance(input_bytes, bytes):
        raise ValueError("input_bytes must be bytes")
    return tuple(argv), str(resolved_cwd), clean_environment, input_bytes


def _resolve_ps_executable() -> str:
    for candidate in _PS_EXECUTABLE_CANDIDATES:
        path = Path(candidate)
        if path.is_file() and not path.is_symlink() and os.access(path, os.X_OK):
            return str(path.resolve(strict=True))
    raise FileNotFoundError("no fixed /bin/ps or /usr/bin/ps sampler is available")


def build_process_request_binding(
    argv: Sequence[str],
    *,
    cwd: Path | str,
    environment: Mapping[str, str],
    input_bytes: bytes,
    limits: SupervisionLimits,
) -> ProcessRequestBinding:
    exact_argv, exact_cwd, exact_environment, exact_input = _validated_invocation(
        argv, cwd, environment, input_bytes
    )
    if not isinstance(limits, SupervisionLimits):
        raise ValueError("limits must be SupervisionLimits")
    bindings = tuple(
        (name, _bytes_digest(value.encode("utf-8")))
        for name, value in sorted(exact_environment.items())
    )
    binding_rows = [
        {"name": name, "value_sha256": digest} for name, digest in bindings
    ]
    material = {
        "argv": list(exact_argv),
        "argv_digest": _value_digest(list(exact_argv)),
        "cwd": exact_cwd,
        "environment_bindings": binding_rows,
        "environment_digest": _value_digest(binding_rows),
        "stdin_bytes": len(exact_input),
        "stdin_sha256": _bytes_digest(exact_input),
        "limits_digest": _value_digest(limits.as_dict()),
        "sampling_executable": (
            _resolve_ps_executable() if limits.sampling.mode == "posix_ps" else None
        ),
    }
    request = ProcessRequestBinding(
        argv=exact_argv,
        argv_digest=material["argv_digest"],
        cwd=exact_cwd,
        environment_bindings=bindings,
        environment_digest=material["environment_digest"],
        stdin_bytes=len(exact_input),
        stdin_sha256=material["stdin_sha256"],
        limits_digest=material["limits_digest"],
        sampling_executable=material["sampling_executable"],
        request_digest=_value_digest(material),
    )
    _validate_request_binding(request)
    return request


def _validate_request_binding(request: ProcessRequestBinding) -> None:
    if not request.argv or any(
        not isinstance(row, str) or not row or "\x00" in row for row in request.argv
    ):
        raise ValueError("request argv is invalid")
    if request.argv_digest != _value_digest(list(request.argv)):
        raise ValueError("request argv digest mismatch")
    cwd = Path(request.cwd)
    if not cwd.is_absolute():
        raise ValueError("request cwd is not absolute")
    try:
        resolved_cwd = cwd.resolve(strict=True)
    except OSError as exc:
        raise ValueError("request cwd is not a live canonical directory") from exc
    if cwd != resolved_cwd or cwd.is_symlink() or not cwd.is_dir():
        raise ValueError("request cwd is not a live canonical non-symlink directory")
    if tuple(sorted(request.environment_bindings)) != request.environment_bindings:
        raise ValueError("environment bindings are not canonical")
    names = [name for name, _digest in request.environment_bindings]
    if len(names) != len(set(names)) or any(
        not name or "=" in name or "\x00" in name for name in names
    ):
        raise ValueError("environment bindings contain duplicate or empty names")
    if any(not _is_sha256(digest) for _name, digest in request.environment_bindings):
        raise ValueError("environment binding digest is invalid")
    rows = [
        {"name": name, "value_sha256": digest}
        for name, digest in request.environment_bindings
    ]
    if request.environment_digest != _value_digest(rows):
        raise ValueError("environment digest mismatch")
    if type(request.stdin_bytes) is not int or request.stdin_bytes < 0:
        raise ValueError("request stdin byte count is invalid")
    if not _is_sha256(request.stdin_sha256) or not _is_sha256(request.limits_digest):
        raise ValueError("request digest syntax is invalid")
    if request.sampling_executable is not None:
        sampler = Path(request.sampling_executable)
        try:
            resolved_sampler = sampler.resolve(strict=True)
        except OSError as exc:
            raise ValueError("sampling executable is unavailable") from exc
        if (
            not sampler.is_absolute()
            or sampler != resolved_sampler
            or sampler.is_symlink()
            or not sampler.is_file()
            or not os.access(sampler, os.X_OK)
        ):
            raise ValueError("sampling executable is not canonical and executable")
    material = request.as_dict()
    material.pop("request_digest")
    if request.request_digest != _value_digest(material):
        raise ValueError("request digest mismatch")


@dataclass(frozen=True, slots=True)
class _FailureEvent:
    ordinal: int
    category: str
    stage: str
    reason_code: str
    message: str
    message_sha256: str
    message_truncated: bool

    @classmethod
    def build(
        cls,
        ordinal: int,
        category: str,
        stage: str,
        reason_code: str,
        message: str,
    ) -> "_FailureEvent":
        raw = (str(message) or reason_code).encode("utf-8", errors="replace")
        retained = raw[:_FAILURE_MESSAGE_BYTES]
        return cls(
            ordinal=ordinal,
            category=category,
            stage=stage,
            reason_code=reason_code,
            message=retained.decode("utf-8", errors="replace"),
            message_sha256=_bytes_digest(raw),
            message_truncated=len(raw) > len(retained),
        )

    def __post_init__(self) -> None:
        if type(self.ordinal) is not int or self.ordinal < 0:
            raise ValueError("failure ordinal must be non-negative")
        if any(not isinstance(value, str) or not value for value in (
            self.category, self.stage, self.reason_code, self.message
        )):
            raise ValueError("failure text fields must be non-empty")
        if self.category not in _FAILURE_CATEGORIES | _DIAGNOSTIC_CATEGORIES:
            raise ValueError("failure category is outside the closed union")
        if self.stage not in _FAILURE_STAGES:
            raise ValueError("failure stage is outside the closed union")
        if _EVENT_TOKEN_RE.fullmatch(self.reason_code) is None:
            raise ValueError("failure reason code is not a canonical token")
        if self.reason_code not in _FAILURE_REASON_CODES or (
            self.category,
            self.stage,
            self.reason_code,
        ) not in _FAILURE_VARIANTS:
            raise ValueError("failure event is outside the closed discriminated union")
        if not _is_sha256(self.message_sha256) or type(self.message_truncated) is not bool:
            raise ValueError("failure digest/truncation fields are invalid")
        if len(self.message.encode("utf-8")) > _FAILURE_MESSAGE_BYTES:
            raise ValueError("failure message exceeds its retained bound")
        if not self.message_truncated and self.message_sha256 != _bytes_digest(
            self.message.encode("utf-8")
        ):
            raise ValueError("untruncated failure message digest mismatch")

    def as_dict(self) -> dict[str, Any]:
        return {
            "ordinal": self.ordinal,
            "category": self.category,
            "stage": self.stage,
            "reason_code": self.reason_code,
            "message": self.message,
            "message_sha256": self.message_sha256,
            "message_truncated": self.message_truncated,
        }

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "_FailureEvent":
        if not isinstance(raw, Mapping):
            raise ValueError("failure event must be a mapping")
        _require_exact_keys(raw, {field.name for field in fields(cls)}, "failure event")
        return cls(**dict(raw))


@dataclass(frozen=True, slots=True)
class _StreamEvidence:
    captured_bytes: int
    captured_sha256: str
    retained_tail: bytes
    retained_limit_bytes: int
    ceiling_bytes: int | None
    ceiling_exceeded: bool
    utf8_valid_retained_tail: bool
    eof_observed: bool
    capture_complete: bool
    capture_disposition: str
    parent_descriptor_existed: bool
    parent_close_attempted: bool
    parent_descriptor_closed: bool
    read_failed: bool

    def __post_init__(self) -> None:
        if type(self.captured_bytes) is not int or self.captured_bytes < 0:
            raise ValueError("captured byte count is invalid")
        if not _is_sha256(self.captured_sha256):
            raise ValueError("captured stream digest is invalid")
        if not isinstance(self.retained_tail, bytes):
            raise ValueError("retained stream tail must be bytes")
        _positive_int(self.retained_limit_bytes, "retained stream limit")
        _optional_positive_int(self.ceiling_bytes, "stream ceiling")
        if len(self.retained_tail) > self.retained_limit_bytes:
            raise ValueError("retained stream tail exceeds its limit")
        if len(self.retained_tail) > self.captured_bytes:
            raise ValueError("retained stream tail exceeds captured bytes")
        for name in (
            "ceiling_exceeded",
            "utf8_valid_retained_tail",
            "eof_observed",
            "capture_complete",
            "parent_descriptor_existed",
            "parent_close_attempted",
            "parent_descriptor_closed",
            "read_failed",
        ):
            if type(getattr(self, name)) is not bool:
                raise ValueError(f"{name} must be boolean")
        expected_ceiling = (
            self.ceiling_bytes is not None and self.captured_bytes > self.ceiling_bytes
        )
        if self.ceiling_exceeded != expected_ceiling:
            raise ValueError("stream ceiling relation is inconsistent")
        expected_complete = self.eof_observed and not self.read_failed
        if self.capture_complete != expected_complete:
            raise ValueError("stream capture completeness is inconsistent")
        if not self.parent_descriptor_existed:
            if self.parent_close_attempted:
                raise ValueError("a nonexistent descriptor cannot have a close attempt")
            if not self.parent_descriptor_closed:
                raise ValueError(
                    "a not-started stream must assert that no parent descriptor remains open"
                )
            if (
                self.captured_bytes != 0
                or self.retained_tail
                or self.eof_observed
                or self.read_failed
                or self.captured_sha256 != _bytes_digest(b"")
            ):
                raise ValueError("a not-started stream carries capture evidence")
        elif self.parent_descriptor_closed and not self.parent_close_attempted:
            raise ValueError("a closed parent descriptor lacks a close attempt")
        if self.capture_disposition not in {
            "not_started",
            "complete_eof",
            "forced_close_without_eof",
            "read_failed",
        }:
            raise ValueError("unknown stream capture disposition")
        expected_disposition = (
            "not_started"
            if not self.parent_descriptor_existed
            else "read_failed"
            if self.read_failed
            else "complete_eof"
            if self.eof_observed
            else "forced_close_without_eof"
        )
        if self.capture_disposition != expected_disposition:
            raise ValueError("stream capture disposition is inconsistent")

    @property
    def total_bytes(self) -> int:
        return self.captured_bytes

    @property
    def sha256(self) -> str:
        return self.captured_sha256

    def as_dict(self) -> dict[str, Any]:
        return {
            "captured_bytes": self.captured_bytes,
            "captured_sha256": self.captured_sha256,
            "retained_tail_base64": base64.b64encode(self.retained_tail).decode("ascii"),
            "retained_bytes": len(self.retained_tail),
            "retained_limit_bytes": self.retained_limit_bytes,
            "ceiling_bytes": self.ceiling_bytes,
            "ceiling_exceeded": self.ceiling_exceeded,
            "utf8_valid_retained_tail": self.utf8_valid_retained_tail,
            "eof_observed": self.eof_observed,
            "capture_complete": self.capture_complete,
            "capture_disposition": self.capture_disposition,
            "parent_descriptor_existed": self.parent_descriptor_existed,
            "parent_close_attempted": self.parent_close_attempted,
            "parent_descriptor_closed": self.parent_descriptor_closed,
            "read_failed": self.read_failed,
        }

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "_StreamEvidence":
        if not isinstance(raw, Mapping):
            raise ValueError("stream evidence must be a mapping")
        expected = {
            "captured_bytes",
            "captured_sha256",
            "retained_tail_base64",
            "retained_bytes",
            "retained_limit_bytes",
            "ceiling_bytes",
            "ceiling_exceeded",
            "utf8_valid_retained_tail",
            "eof_observed",
            "capture_complete",
            "capture_disposition",
            "parent_descriptor_existed",
            "parent_close_attempted",
            "parent_descriptor_closed",
            "read_failed",
        }
        _require_exact_keys(raw, expected, "stream evidence")
        encoded = raw["retained_tail_base64"]
        if not isinstance(encoded, str):
            raise ValueError("retained stream tail must use canonical base64 text")
        try:
            retained = base64.b64decode(encoded.encode("ascii"), validate=True)
        except (UnicodeEncodeError, ValueError) as exc:
            raise ValueError("retained stream tail base64 is invalid") from exc
        if base64.b64encode(retained).decode("ascii") != encoded:
            raise ValueError("retained stream tail base64 is noncanonical")
        if raw["retained_bytes"] != len(retained):
            raise ValueError("retained stream byte count mismatch")
        values = dict(raw)
        values.pop("retained_tail_base64")
        values.pop("retained_bytes")
        values["retained_tail"] = retained
        return cls(**values)


class _StreamCapture:
    def __init__(self, *, ceiling_bytes: int | None, retained_bytes: int) -> None:
        self.ceiling_bytes = ceiling_bytes
        self.retained_bytes = retained_bytes
        self.captured_bytes = 0
        self.tail = bytearray()
        self.digest = hashlib.sha256()
        self.eof_observed = False
        self.read_failed = False

    def add(self, data: bytes) -> None:
        self.captured_bytes += len(data)
        self.digest.update(data)
        self.tail.extend(data)
        excess = len(self.tail) - self.retained_bytes
        if excess > 0:
            del self.tail[:excess]

    def freeze(
        self,
        *,
        descriptor_existed: bool,
        close_attempted: bool,
        descriptor_closed: bool,
    ) -> _StreamEvidence:
        retained = bytes(self.tail)
        try:
            retained.decode("utf-8", errors="strict")
            utf8_valid = True
        except UnicodeDecodeError:
            utf8_valid = False
        disposition = (
            "not_started"
            if not descriptor_existed
            else "read_failed"
            if self.read_failed
            else "complete_eof"
            if self.eof_observed
            else "forced_close_without_eof"
        )
        return _StreamEvidence(
            captured_bytes=self.captured_bytes,
            captured_sha256=_SHA256_PREFIX + self.digest.hexdigest(),
            retained_tail=retained,
            retained_limit_bytes=self.retained_bytes,
            ceiling_bytes=self.ceiling_bytes,
            ceiling_exceeded=(
                self.ceiling_bytes is not None
                and self.captured_bytes > self.ceiling_bytes
            ),
            utf8_valid_retained_tail=utf8_valid,
            eof_observed=self.eof_observed,
            capture_complete=self.eof_observed and not self.read_failed,
            capture_disposition=disposition,
            parent_descriptor_existed=descriptor_existed,
            parent_close_attempted=close_attempted,
            parent_descriptor_closed=descriptor_closed,
            read_failed=self.read_failed,
        )


@dataclass(frozen=True, slots=True)
class _Wait4Evidence:
    returncode: int
    user_cpu_ns: int
    system_cpu_ns: int
    maxrss_raw: int
    maxrss_unit: str
    normalized_maxrss_bytes: int | None
    reaped_ns: int


def _normalize_maxrss(raw: int) -> tuple[str, int | None]:
    system = platform.system()
    if system == "Darwin":
        return "bytes", max(0, raw)
    if system == "Linux":
        return "kibibytes", max(0, raw) * 1024
    return "unknown", None


def _wait4_nohang(pid: int) -> _Wait4Evidence | None:
    waited_pid, status, usage = os.wait4(pid, os.WNOHANG)
    if waited_pid == 0:
        return None
    if waited_pid != pid:
        raise ChildProcessError("wait4 returned a PID other than the requested child")
    raw = max(0, int(usage.ru_maxrss))
    unit, normalized = _normalize_maxrss(raw)
    return _Wait4Evidence(
        returncode=os.waitstatus_to_exitcode(status),
        user_cpu_ns=int(max(0.0, usage.ru_utime) * 1_000_000_000),
        system_cpu_ns=int(max(0.0, usage.ru_stime) * 1_000_000_000),
        maxrss_raw=raw,
        maxrss_unit=unit,
        normalized_maxrss_bytes=normalized,
        reaped_ns=time.monotonic_ns(),
    )


@dataclass(frozen=True, slots=True)
class _ProcessGroupSample:
    members: int
    zombie_members: int
    rss_bytes: int


@dataclass(frozen=True, slots=True)
class _SamplerAttempt:
    sample: _ProcessGroupSample | None
    started: bool
    reaped: bool
    failure_reason: str | None
    failure_message: str | None


def _read_one_nonblocking(stream: Any, limit: int, buffer: bytearray) -> bool:
    """Read at most one chunk; return True only when EOF was observed."""

    chunk = os.read(stream.fileno(), min(_READ_CHUNK_BYTES, limit - len(buffer) + 1))
    if not chunk:
        return True
    buffer.extend(chunk)
    if len(buffer) > limit:
        raise OverflowError("sampler output exceeded its fixed byte ceiling")
    return False


def _run_ps_sampler(
    process_group_id: int,
    *,
    executable: str,
    policy: ProcessGroupSamplingPolicy,
    parent_execution_deadline_ns: int,
) -> _SamplerAttempt:
    """Run one fixed ps sidecar with its own absolute deadline and cleanup."""

    started_ns = time.monotonic_ns()
    hard_deadline_ns = min(
        parent_execution_deadline_ns,
        started_ns + policy.attempt_timeout_ns,
    )
    io_deadline_ns = hard_deadline_ns - policy.cleanup_reserve_ns
    if io_deadline_ns <= started_ns:
        return _SamplerAttempt(
            sample=None,
            started=False,
            reaped=False,
            failure_reason="sampler_budget_unavailable",
            failure_message="insufficient absolute budget for one sampler attempt",
        )

    process: subprocess.Popen[bytes] | None = None
    selector: selectors.BaseSelector | None = None
    stdout = bytearray()
    stderr = bytearray()
    stdout_eof = False
    stderr_eof = False
    reaped = False
    returncode: int | None = None
    failure_reason: str | None = None
    failure_message: str | None = None

    def remember(reason: str, message: str) -> None:
        nonlocal failure_reason, failure_message
        if failure_reason is None:
            failure_reason = reason
            failure_message = message

    preserving_host_exception = False

    def close_all(*, suppress_base_exception: bool = False) -> None:
        nonlocal selector
        for stream in (
            process.stdout if process is not None else None,
            process.stderr if process is not None else None,
        ):
            if stream is None:
                continue
            try:
                if selector is not None:
                    selector.unregister(stream)
            except Exception:
                pass
            except BaseException as exc:
                if not suppress_base_exception:
                    raise
                remember("sampler_descriptor_close_failed", f"{type(exc).__name__}: {exc}")
            try:
                stream.close()
            except Exception as exc:
                remember("sampler_descriptor_close_failed", f"{type(exc).__name__}: {exc}")
            except BaseException as exc:
                if not suppress_base_exception:
                    raise
                remember("sampler_descriptor_close_failed", f"{type(exc).__name__}: {exc}")
        if selector is not None:
            try:
                selector.close()
            except Exception as exc:
                remember("sampler_selector_close_failed", f"{type(exc).__name__}: {exc}")
            except BaseException as exc:
                if not suppress_base_exception:
                    raise
                remember("sampler_selector_close_failed", f"{type(exc).__name__}: {exc}")

    def kill_before_reap(*, suppress_base_exception: bool = False) -> None:
        if process is None or reaped:
            return
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except Exception as exc:
            remember("sampler_sigkill_failed", f"{type(exc).__name__}: {exc}")
        except BaseException as exc:
            if not suppress_base_exception:
                raise
            remember("sampler_sigkill_failed", f"{type(exc).__name__}: {exc}")

    def retain_reap(evidence: _Wait4Evidence) -> None:
        nonlocal reaped, returncode
        reaped = True
        returncode = evidence.returncode
        if process is not None:
            process.returncode = evidence.returncode

    try:
        try:
            process = subprocess.Popen(
                [executable, "-axo", "pid=,pgid=,rss=,state="],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={"LANG": "C", "LC_ALL": "C", "PATH": "/usr/bin:/bin"},
                text=False,
                start_new_session=True,
                close_fds=True,
            )
            if process.stdout is None or process.stderr is None:
                raise RuntimeError("sampler pipes are unavailable")
            selector = selectors.DefaultSelector()
            for stream, label in ((process.stdout, "stdout"), (process.stderr, "stderr")):
                os.set_blocking(stream.fileno(), False)
                selector.register(stream, selectors.EVENT_READ, data=label)
        except Exception as exc:
            remember("sampler_launch_failed", f"{type(exc).__name__}: {exc}")

        while process is not None and failure_reason is None:
            now_ns = time.monotonic_ns()
            if now_ns >= io_deadline_ns:
                remember("sampler_deadline_exhausted", "sampler IO deadline was exhausted")
                break
            timeout_ns = min(_SELECT_QUANTUM_NS, io_deadline_ns - now_ns)
            try:
                events = selector.select(timeout=timeout_ns / 1_000_000_000) if selector else []
            except Exception as exc:
                remember("sampler_select_failed", f"{type(exc).__name__}: {exc}")
                break
            for key, _mask in events:
                try:
                    if key.data == "stdout":
                        stdout_eof = _read_one_nonblocking(
                            key.fileobj, policy.stdout_limit_bytes, stdout
                        )
                    else:
                        stderr_eof = _read_one_nonblocking(
                            key.fileobj, policy.stderr_limit_bytes, stderr
                        )
                except BlockingIOError:
                    continue
                except Exception as exc:
                    remember("sampler_read_failed", f"{type(exc).__name__}: {exc}")
                    break
            if failure_reason is not None:
                break
            if stdout_eof and stderr_eof:
                try:
                    evidence = _wait4_nohang(process.pid)
                except Exception as exc:
                    remember("sampler_wait_failed", f"{type(exc).__name__}: {exc}")
                    break
                if evidence is not None:
                    retain_reap(evidence)
                    break

        if process is not None and not reaped:
            kill_before_reap()
            while time.monotonic_ns() < hard_deadline_ns and not reaped:
                if selector is not None:
                    try:
                        events = selector.select(
                            timeout=min(
                                _SELECT_QUANTUM_NS,
                                max(0, hard_deadline_ns - time.monotonic_ns()),
                            )
                            / 1_000_000_000
                        )
                    except Exception as exc:
                        remember("sampler_cleanup_select_failed", f"{type(exc).__name__}: {exc}")
                        events = []
                    for key, _mask in events:
                        try:
                            if key.data == "stdout" and not stdout_eof:
                                stdout_eof = _read_one_nonblocking(
                                    key.fileobj, policy.stdout_limit_bytes, stdout
                                )
                            elif key.data == "stderr" and not stderr_eof:
                                stderr_eof = _read_one_nonblocking(
                                    key.fileobj, policy.stderr_limit_bytes, stderr
                                )
                        except (BlockingIOError, OverflowError, OSError):
                            pass
                try:
                    evidence = _wait4_nohang(process.pid)
                except Exception as exc:
                    remember("sampler_cleanup_wait_failed", f"{type(exc).__name__}: {exc}")
                    break
                if evidence is not None:
                    retain_reap(evidence)
                    break
        if process is not None and not reaped:
            remember(
                "sampler_not_reaped_before_deadline",
                "the sampler child did not reach a wait4 terminal state",
            )
    except BaseException:
        preserving_host_exception = True
        kill_before_reap(suppress_base_exception=True)
        host_cleanup_deadline_ns = time.monotonic_ns() + policy.cleanup_reserve_ns
        while process is not None and not reaped and time.monotonic_ns() < host_cleanup_deadline_ns:
            try:
                evidence = _wait4_nohang(process.pid)
            except BaseException:
                evidence = None
            if evidence is not None:
                retain_reap(evidence)
                break
            remaining_ns = host_cleanup_deadline_ns - time.monotonic_ns()
            if remaining_ns > 0:
                time.sleep(min(0.001, remaining_ns / 1_000_000_000))
        close_all(suppress_base_exception=True)
        raise
    finally:
        close_all(suppress_base_exception=preserving_host_exception)

    if failure_reason is None and returncode != 0:
        remember("sampler_exit_nonzero", f"ps sampler exited with return code {returncode}")
    sample: _ProcessGroupSample | None = None
    if failure_reason is None:
        members = 0
        zombies = 0
        rss_kib = 0
        for raw_line in bytes(stdout).splitlines():
            columns = raw_line.split()
            if len(columns) != 4:
                continue
            try:
                _pid, group_id, row_rss = map(int, columns[:3])
            except ValueError:
                continue
            if group_id != process_group_id:
                continue
            members += 1
            rss_kib += max(0, row_rss)
            state = columns[3].decode("ascii", errors="ignore")
            if state.startswith("Z"):
                zombies += 1
        sample = _ProcessGroupSample(
            members=members,
            zombie_members=zombies,
            rss_bytes=rss_kib * 1024,
        )
    return _SamplerAttempt(
        sample=sample,
        started=process is not None,
        reaped=reaped,
        failure_reason=failure_reason,
        failure_message=failure_message,
    )


@dataclass(frozen=True, slots=True, init=False)
class SupervisedProcessAttempt:
    """A sealed attempt; direct construction is intentionally unavailable."""

    attempt_id: str
    status: str
    request: ProcessRequestBinding
    process_started: bool
    stdin_enqueued_bytes: int
    stdin_parent_descriptor_closed: bool
    stdout: _StreamEvidence
    stderr: _StreamEvidence
    pid: int | None
    intended_process_group_id: int | None
    observed_process_group_id: int | None
    observed_session_id: int | None
    returncode: int | None
    leader_reaped: bool
    termination_disposition: str
    original_group_action_disposition: str
    call_started_monotonic_ns: int
    spawn_started_monotonic_ns: int | None
    spawn_completed_monotonic_ns: int | None
    execution_deadline_monotonic_ns: int
    cleanup_io_deadline_monotonic_ns: int
    total_deadline_monotonic_ns: int
    evidence_sealed_monotonic_ns: int
    leader_reaped_monotonic_ns: int | None
    last_original_group_operation_ns: int | None
    wait4_accounted_user_cpu_ns: int | None
    wait4_accounted_system_cpu_ns: int | None
    wait4_ru_maxrss_raw: int | None
    wait4_ru_maxrss_unit: str | None
    wait4_ru_maxrss_normalized_bytes: int | None
    group_sample_count: int
    peak_observed_sampled_original_group_members: int | None
    peak_observed_sampled_original_group_zombie_members: int | None
    peak_observed_sampled_original_group_rss_bytes: int | None
    sampler_processes_started: int
    sampler_processes_reaped: int
    failure_events: tuple[_FailureEvent, ...]
    cleanup_failures: tuple[_FailureEvent, ...]
    nonfatal_diagnostics: tuple[_FailureEvent, ...]
    limits: SupervisionLimits

    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        raise TypeError(
            "SupervisedProcessAttempt is sealed; use run_ or load_supervised_process_attempt"
        )

    @classmethod
    def _seal(cls, **values: Any) -> "SupervisedProcessAttempt":
        expected = {field.name for field in fields(cls)}
        if set(values) != expected:
            raise ValueError("internal attempt seal received an incomplete field set")
        self = object.__new__(cls)
        for field in fields(cls):
            object.__setattr__(self, field.name, values[field.name])
        validate_supervised_process_attempt(self)
        return self

    @property
    def argv(self) -> tuple[str, ...]:
        return self.request.argv

    @property
    def cwd(self) -> str:
        return self.request.cwd

    @property
    def environment_keys(self) -> tuple[str, ...]:
        return self.request.environment_keys

    @property
    def stdin_bytes(self) -> int:
        return self.request.stdin_bytes

    @property
    def stdin_sha256(self) -> str:
        return self.request.stdin_sha256

    @property
    def stdin_fully_enqueued(self) -> bool:
        return self.stdin_enqueued_bytes == self.request.stdin_bytes

    @property
    def leader_identity_anchor_released(self) -> bool:
        return self.leader_reaped or any(
            event.reason_code == "leader_ownership_lost" for event in self.failure_events
        )

    @property
    def primary_failure(self) -> _FailureEvent | None:
        return self.failure_events[0] if self.failure_events else None

    @property
    def total_elapsed_ns(self) -> int:
        return max(0, self.evidence_sealed_monotonic_ns - self.call_started_monotonic_ns)

    @property
    def deadline_overrun_ns(self) -> int:
        return max(0, self.evidence_sealed_monotonic_ns - self.total_deadline_monotonic_ns)

    @property
    def containment(self) -> dict[str, Any]:
        return {
            "mode": CONTAINMENT_MODE,
            "trusted_worker_required": True,
            "fresh_posix_session_requested": True,
            "unreaped_leader_is_numeric_pgid_identity_anchor": True,
            "all_original_group_operations_must_precede_leader_reap": True,
            "original_process_group_cleanup_scope": True,
            "hard_descendant_containment": False,
            "escaped_descendants_unobservable": True,
            "short_lived_descendants_between_samples_unobservable": True,
            "filesystem_isolation": "unavailable",
            "network_isolation": "unavailable",
            "uid_isolation": "unavailable",
            "cryptographic_authenticity": False,
        }

    @property
    def authority_boundaries(self) -> dict[str, Any]:
        return {
            "semantic_authority": False,
            "scientific_authority": False,
            "truth_authority": False,
            "proof_authority": False,
            "experiment_value_authority": False,
            "physics_authority": False,
            "cryptographic_authenticity": False,
            "authority_boundary": AUTHORITY_BOUNDARY,
        }

    def invariant_projection(self) -> dict[str, Any]:
        projection: dict[str, Any] = {
            "schema_version": PROCESS_ATTEMPT_SCHEMA_VERSION,
            "attempt_kind": PROCESS_ATTEMPT_KIND,
            "request": self.request.as_dict(),
            "outcome": {
                "status": self.status,
                "process_started": self.process_started,
                "returncode": self.returncode,
                "stdin_fully_enqueued": self.stdin_fully_enqueued,
                "stdout_captured_bytes": self.stdout.captured_bytes,
                "stdout_captured_sha256": self.stdout.captured_sha256,
                "stdout_eof_observed": self.stdout.eof_observed,
                "stderr_captured_bytes": self.stderr.captured_bytes,
                "stderr_captured_sha256": self.stderr.captured_sha256,
                "stderr_eof_observed": self.stderr.eof_observed,
                "failure_reason_codes": [
                    event.reason_code for event in self.failure_events
                ],
                "cleanup_reason_codes": [
                    event.reason_code for event in self.cleanup_failures
                ],
            },
            "containment": self.containment,
            "authority_boundaries": self.authority_boundaries,
        }
        projection["projection_digest"] = _value_digest(projection)
        return projection

    def as_dict(self) -> dict[str, Any]:
        validate_supervised_process_attempt(self)
        payload: dict[str, Any] = {
            "schema_version": PROCESS_ATTEMPT_SCHEMA_VERSION,
            "attempt_kind": PROCESS_ATTEMPT_KIND,
            "attempt_id": self.attempt_id,
            "status": self.status,
            "request": self.request.as_dict(),
            "streams": {"stdout": self.stdout.as_dict(), "stderr": self.stderr.as_dict()},
            "process": {
                "process_started": self.process_started,
                "pid": self.pid,
                "intended_process_group_id": self.intended_process_group_id,
                "observed_process_group_id": self.observed_process_group_id,
                "observed_session_id": self.observed_session_id,
                "returncode": self.returncode,
                "leader_reaped": self.leader_reaped,
                "leader_identity_anchor_released": self.leader_identity_anchor_released,
                "termination_disposition": self.termination_disposition,
                "original_group_action_disposition": self.original_group_action_disposition,
                "stdin_enqueued_bytes": self.stdin_enqueued_bytes,
                "stdin_fully_enqueued": self.stdin_fully_enqueued,
                "stdin_parent_descriptor_closed": self.stdin_parent_descriptor_closed,
            },
            "timing": {
                "clock": "time.monotonic_ns",
                "deadline_scope": (
                    "parent_observed_operational_work_through_stream_evidence_seal"
                ),
                "hard_kernel_preemption": False,
                "overrun_detected_after_blocking_call_returns": True,
                "record_serialization_after_evidence_seal_excluded": True,
                "call_started_ns": self.call_started_monotonic_ns,
                "spawn_started_ns": self.spawn_started_monotonic_ns,
                "spawn_completed_ns": self.spawn_completed_monotonic_ns,
                "execution_deadline_ns": self.execution_deadline_monotonic_ns,
                "cleanup_io_deadline_ns": self.cleanup_io_deadline_monotonic_ns,
                "total_deadline_ns": self.total_deadline_monotonic_ns,
                "evidence_sealed_ns": self.evidence_sealed_monotonic_ns,
                "leader_reaped_ns": self.leader_reaped_monotonic_ns,
                "last_original_group_operation_ns": self.last_original_group_operation_ns,
                "total_elapsed_ns": self.total_elapsed_ns,
                "deadline_overrun_ns": self.deadline_overrun_ns,
            },
            "resource_observation": {
                "wait4_accounted_user_cpu_ns": self.wait4_accounted_user_cpu_ns,
                "wait4_accounted_system_cpu_ns": self.wait4_accounted_system_cpu_ns,
                "wait4_ru_maxrss_raw": self.wait4_ru_maxrss_raw,
                "wait4_ru_maxrss_unit": self.wait4_ru_maxrss_unit,
                "wait4_ru_maxrss_normalized_bytes": self.wait4_ru_maxrss_normalized_bytes,
                "wait4_accounting_scope": (
                    "target_pid_wait4_accounting_platform_defined_may_include_descendant_accrual"
                ),
                "wait4_threshold_semantics": (
                    "post_exit_acceptance_only_not_runtime_enforcement"
                ),
                "group_threshold_semantics": (
                    "sample_triggered_best_effort_termination_not_hard_ceiling"
                ),
            },
            "sampling": {
                "policy": self.limits.sampling.as_dict(),
                "group_sample_count": self.group_sample_count,
                "peak_observed_sampled_original_group_members": (
                    self.peak_observed_sampled_original_group_members
                ),
                "peak_observed_sampled_original_group_zombie_members": (
                    self.peak_observed_sampled_original_group_zombie_members
                ),
                "peak_observed_sampled_original_group_rss_bytes": (
                    self.peak_observed_sampled_original_group_rss_bytes
                ),
                "sampler_processes_started": self.sampler_processes_started,
                "sampler_processes_reaped": self.sampler_processes_reaped,
                "measurement_scope": (
                    "sampled_original_process_group_not_hard_supremum"
                ),
            },
            "failure_events": [event.as_dict() for event in self.failure_events],
            "primary_failure": (
                self.primary_failure.as_dict() if self.primary_failure is not None else None
            ),
            "cleanup_failures": [event.as_dict() for event in self.cleanup_failures],
            "nonfatal_diagnostics": [
                event.as_dict() for event in self.nonfatal_diagnostics
            ],
            "limits": self.limits.as_dict(),
            "containment": self.containment,
            "authority_boundaries": self.authority_boundaries,
            "invariant_projection": self.invariant_projection(),
        }
        payload["attempt_digest"] = _value_digest(payload)
        return payload


def _derived_status(failures: tuple[_FailureEvent, ...]) -> str:
    if not failures:
        return "succeeded"
    first = failures[0]
    reason = first.reason_code
    if reason == "input_limit_exceeded":
        return "input_exhausted"
    if reason == "unsupported_platform":
        return "unsupported_platform"
    if first.stage in {"prelaunch", "launch", "launch_setup"}:
        return "launch_failed"
    if reason in {
        "stdout_limit_exceeded",
        "stderr_limit_exceeded",
        "sampled_original_group_member_threshold_exceeded",
        "sampled_original_group_rss_threshold_exceeded",
        "observed_wait4_cpu_threshold_exceeded",
        "observed_wait4_normalized_maxrss_threshold_exceeded",
    }:
        return "resource_or_output_exhausted"
    if "deadline" in reason or "overrun" in reason:
        return "deadline_exhausted"
    if first.stage in {"transport", "process_exit"}:
        return "worker_failed"
    return "operational_failure"


def validate_supervised_process_attempt(
    attempt: SupervisedProcessAttempt,
    *,
    expected_request: ProcessRequestBinding | None = None,
) -> None:
    if not isinstance(attempt, SupervisedProcessAttempt):
        raise ValueError("attempt must be SupervisedProcessAttempt")
    _validate_request_binding(attempt.request)
    if expected_request is not None and attempt.request != expected_request:
        raise ValueError("attempt request does not match expected request binding")
    if attempt.request.limits_digest != _value_digest(attempt.limits.as_dict()):
        raise ValueError("attempt limits do not match request binding")
    expected_attempt_id = "process-attempt." + hashlib.sha256(
        _canonical_json(
            {
                "request_digest": attempt.request.request_digest,
                "call_started_monotonic_ns": attempt.call_started_monotonic_ns,
            }
        )
    ).hexdigest()[:32]
    if attempt.attempt_id != expected_attempt_id:
        raise ValueError("attempt identifier mismatch")
    if attempt.status != _derived_status(attempt.failure_events):
        raise ValueError("attempt status is not derived from its failure ledger")
    if tuple(event.ordinal for event in attempt.failure_events) != tuple(
        range(len(attempt.failure_events))
    ):
        raise ValueError("fatal failure ordinals are not contiguous")
    if len(attempt.failure_events) > _MAX_FAILURE_EVENTS:
        raise ValueError("fatal failure ledger exceeds its cardinality ceiling")
    if tuple(event.ordinal for event in attempt.nonfatal_diagnostics) != tuple(
        range(len(attempt.nonfatal_diagnostics))
    ):
        raise ValueError("diagnostic ordinals are not contiguous")
    if len(attempt.nonfatal_diagnostics) > _MAX_DIAGNOSTIC_EVENTS:
        raise ValueError("diagnostic ledger exceeds its cardinality ceiling")
    if any(event.category == "diagnostic" for event in attempt.failure_events):
        raise ValueError("fatal ledger contains a diagnostic event")
    if any(event.category != "diagnostic" for event in attempt.nonfatal_diagnostics):
        raise ValueError("diagnostic ledger contains a fatal event")
    fatal_by_ordinal = {event.ordinal: event for event in attempt.failure_events}
    if any(fatal_by_ordinal.get(event.ordinal) != event for event in attempt.cleanup_failures):
        raise ValueError("cleanup failures must be members of the fatal ledger")
    if tuple(event for event in attempt.failure_events if event.category == "cleanup") != (
        attempt.cleanup_failures
    ):
        raise ValueError("fatal cleanup events and cleanup ledger differ")
    if attempt.termination_disposition not in _TERMINATION_DISPOSITIONS:
        raise ValueError("termination disposition is outside the closed union")
    if attempt.original_group_action_disposition not in _TERMINATION_DISPOSITIONS:
        raise ValueError("original-group disposition is outside the closed union")
    if type(attempt.process_started) is not bool:
        raise ValueError("process_started must be boolean")
    if attempt.process_started:
        if type(attempt.pid) is not int or attempt.pid <= 0:
            raise ValueError("started attempt requires a positive PID")
        if attempt.intended_process_group_id != attempt.pid:
            raise ValueError("intended process group must equal anchored PID")
        if (
            attempt.spawn_started_monotonic_ns is None
            or attempt.spawn_completed_monotonic_ns is None
        ):
            raise ValueError("started attempt lacks complete spawn timing")
        if attempt.observed_process_group_id is not None and (
            type(attempt.observed_process_group_id) is not int
            or attempt.observed_process_group_id <= 0
        ):
            raise ValueError("observed process group is invalid")
        if attempt.observed_session_id is not None and (
            type(attempt.observed_session_id) is not int
            or attempt.observed_session_id <= 0
        ):
            raise ValueError("observed session is invalid")
    elif any(
        value is not None
        for value in (
            attempt.pid,
            attempt.intended_process_group_id,
            attempt.observed_process_group_id,
            attempt.observed_session_id,
            attempt.returncode,
            attempt.leader_reaped_monotonic_ns,
        )
    ) or attempt.leader_reaped:
        raise ValueError("unstarted attempt carries process evidence")
    if attempt.leader_reaped != (attempt.leader_reaped_monotonic_ns is not None):
        raise ValueError("leader reaping fields are inconsistent")
    if attempt.leader_reaped != (attempt.returncode is not None):
        raise ValueError("return code presence must match leader reaping")
    if attempt.returncode is not None and type(attempt.returncode) is not int:
        raise ValueError("return code must be an integer")
    if (
        attempt.leader_reaped_monotonic_ns is not None
        and attempt.last_original_group_operation_ns is not None
        and attempt.last_original_group_operation_ns
        > attempt.leader_reaped_monotonic_ns
    ):
        raise ValueError("an original-group operation occurred after leader reap")
    if type(attempt.stdin_enqueued_bytes) is not int or not (
        0 <= attempt.stdin_enqueued_bytes <= attempt.request.stdin_bytes
    ):
        raise ValueError("stdin enqueued byte count is invalid")
    if type(attempt.stdin_parent_descriptor_closed) is not bool:
        raise ValueError("stdin descriptor closure flag is invalid")
    if attempt.stdout.ceiling_bytes != attempt.limits.stdout_limit_bytes:
        raise ValueError("stdout evidence ceiling does not match limits")
    if attempt.stderr.ceiling_bytes != attempt.limits.stderr_limit_bytes:
        raise ValueError("stderr evidence ceiling does not match limits")
    if attempt.stdout.retained_limit_bytes != attempt.limits.stdout_retained_tail_bytes:
        raise ValueError("stdout retained limit mismatch")
    if attempt.stderr.retained_limit_bytes != attempt.limits.stderr_retained_tail_bytes:
        raise ValueError("stderr retained limit mismatch")
    if attempt.execution_deadline_monotonic_ns != (
        attempt.total_deadline_monotonic_ns - attempt.limits.cleanup_reserve_ns
    ):
        raise ValueError("execution deadline derivation mismatch")
    if attempt.cleanup_io_deadline_monotonic_ns != (
        attempt.total_deadline_monotonic_ns - attempt.limits.evidence_seal_reserve_ns
    ):
        raise ValueError("cleanup IO deadline derivation mismatch")
    if attempt.total_deadline_monotonic_ns != (
        attempt.call_started_monotonic_ns + attempt.limits.total_deadline_ns
    ):
        raise ValueError("total deadline derivation mismatch")
    if not (
        attempt.call_started_monotonic_ns
        <= attempt.execution_deadline_monotonic_ns
        < attempt.cleanup_io_deadline_monotonic_ns
        < attempt.total_deadline_monotonic_ns
    ):
        raise ValueError("attempt timing order is invalid")
    if attempt.spawn_started_monotonic_ns is not None and (
        attempt.spawn_started_monotonic_ns < attempt.call_started_monotonic_ns
    ):
        raise ValueError("spawn start precedes call start")
    if attempt.spawn_completed_monotonic_ns is not None and (
        attempt.spawn_started_monotonic_ns is None
        or attempt.spawn_completed_monotonic_ns < attempt.spawn_started_monotonic_ns
    ):
        raise ValueError("spawn completion timing is invalid")
    if (
        attempt.spawn_completed_monotonic_ns is not None
        and attempt.spawn_completed_monotonic_ns > attempt.evidence_sealed_monotonic_ns
    ):
        raise ValueError("spawn completion follows evidence sealing")
    if attempt.evidence_sealed_monotonic_ns < attempt.call_started_monotonic_ns:
        raise ValueError("evidence seal precedes call start")
    if attempt.leader_reaped_monotonic_ns is not None and (
        type(attempt.leader_reaped_monotonic_ns) is not int
        or attempt.leader_reaped_monotonic_ns < attempt.call_started_monotonic_ns
        or attempt.leader_reaped_monotonic_ns > attempt.evidence_sealed_monotonic_ns
    ):
        raise ValueError("leader reap timing is outside the sealed attempt interval")
    if attempt.last_original_group_operation_ns is not None and (
        type(attempt.last_original_group_operation_ns) is not int
        or attempt.last_original_group_operation_ns < attempt.call_started_monotonic_ns
        or attempt.last_original_group_operation_ns > attempt.evidence_sealed_monotonic_ns
        or (
            attempt.spawn_completed_monotonic_ns is not None
            and attempt.last_original_group_operation_ns
            < attempt.spawn_completed_monotonic_ns
        )
    ):
        raise ValueError("original-group operation timing is outside the valid interval")
    if any(
        type(value) is not int or value < 0
        for value in (
            attempt.group_sample_count,
            attempt.sampler_processes_started,
            attempt.sampler_processes_reaped,
        )
    ):
        raise ValueError("sampling counters must be non-negative integers")
    if attempt.sampler_processes_reaped > attempt.sampler_processes_started:
        raise ValueError("reaped sampler count exceeds started sampler count")
    if attempt.sampler_processes_started > attempt.limits.sampling.maximum_attempts:
        raise ValueError("started sampler count exceeds the policy cardinality cap")
    if attempt.group_sample_count > attempt.sampler_processes_reaped:
        raise ValueError("valid sample count exceeds reaped sampler attempts")
    peaks = (
        attempt.peak_observed_sampled_original_group_members,
        attempt.peak_observed_sampled_original_group_zombie_members,
        attempt.peak_observed_sampled_original_group_rss_bytes,
    )
    if attempt.group_sample_count == 0 and any(value is not None for value in peaks):
        raise ValueError("zero samples cannot carry peak observations")
    if attempt.group_sample_count > 0 and any(
        type(value) is not int or value < 0 for value in peaks
    ):
        raise ValueError("positive sample count requires non-negative peaks")
    if (
        attempt.peak_observed_sampled_original_group_zombie_members is not None
        and attempt.peak_observed_sampled_original_group_members is not None
        and attempt.peak_observed_sampled_original_group_zombie_members
        > attempt.peak_observed_sampled_original_group_members
    ):
        raise ValueError("sampled zombie peak exceeds member peak")
    if attempt.limits.sampling.mode == "disabled":
        if (
            attempt.request.sampling_executable is not None
            or attempt.group_sample_count != 0
            or attempt.sampler_processes_started != 0
            or attempt.sampler_processes_reaped != 0
            or any(value is not None for value in peaks)
        ):
            raise ValueError("disabled sampling carries sampler authority or evidence")
    elif attempt.request.sampling_executable is None and not any(
        event.reason_code == "sampling_executable_unavailable"
        for event in attempt.failure_events
    ):
        raise ValueError("enabled sampling lacks a bound canonical executable")
    wait_fields = (
        attempt.wait4_accounted_user_cpu_ns,
        attempt.wait4_accounted_system_cpu_ns,
        attempt.wait4_ru_maxrss_raw,
        attempt.wait4_ru_maxrss_unit,
    )
    if attempt.leader_reaped and any(value is None for value in wait_fields):
        raise ValueError("reaped leader lacks wait4 accounting")
    if not attempt.leader_reaped and any(value is not None for value in wait_fields) or (
        not attempt.leader_reaped
        and attempt.wait4_ru_maxrss_normalized_bytes is not None
    ):
        raise ValueError("unreaped leader carries wait4 accounting")
    if attempt.wait4_ru_maxrss_unit == "bytes":
        if attempt.wait4_ru_maxrss_normalized_bytes != attempt.wait4_ru_maxrss_raw:
            raise ValueError("Darwin maxrss normalization mismatch")
    elif attempt.wait4_ru_maxrss_unit == "kibibytes":
        if attempt.wait4_ru_maxrss_normalized_bytes != attempt.wait4_ru_maxrss_raw * 1024:
            raise ValueError("Linux maxrss normalization mismatch")
    elif attempt.wait4_ru_maxrss_unit == "unknown":
        if attempt.wait4_ru_maxrss_normalized_bytes is not None:
            raise ValueError("unknown maxrss units cannot be normalized")
    elif attempt.wait4_ru_maxrss_unit is not None:
        raise ValueError("unknown wait4 maxrss unit")
    for label, value in (
        ("wait4 user CPU", attempt.wait4_accounted_user_cpu_ns),
        ("wait4 system CPU", attempt.wait4_accounted_system_cpu_ns),
        ("wait4 raw maxrss", attempt.wait4_ru_maxrss_raw),
        ("wait4 normalized maxrss", attempt.wait4_ru_maxrss_normalized_bytes),
    ):
        if value is not None and (type(value) is not int or value < 0):
            raise ValueError(f"{label} must be a non-negative integer")

    failure_reasons = {event.reason_code for event in attempt.failure_events}
    input_exceeded = attempt.request.stdin_bytes > attempt.limits.stdin_limit_bytes
    if ("input_limit_exceeded" in failure_reasons) != input_exceeded:
        raise ValueError("stdin limit evidence and failure ledger differ")
    if input_exceeded and attempt.process_started:
        raise ValueError("an over-limit stdin request must fail before launch")
    for label, stream in (("stdout", attempt.stdout), ("stderr", attempt.stderr)):
        if (f"{label}_limit_exceeded" in failure_reasons) != stream.ceiling_exceeded:
            raise ValueError(f"{label} ceiling evidence and failure ledger differ")
    observed_cpu_ns = (
        None
        if attempt.wait4_accounted_user_cpu_ns is None
        or attempt.wait4_accounted_system_cpu_ns is None
        else attempt.wait4_accounted_user_cpu_ns
        + attempt.wait4_accounted_system_cpu_ns
    )
    cpu_threshold_exceeded = (
        attempt.limits.reject_if_observed_wait4_cpu_ns_above is not None
        and observed_cpu_ns is not None
        and observed_cpu_ns > attempt.limits.reject_if_observed_wait4_cpu_ns_above
    )
    if (
        "observed_wait4_cpu_threshold_exceeded" in failure_reasons
    ) != cpu_threshold_exceeded:
        raise ValueError("wait4 CPU threshold evidence and failure ledger differ")
    maxrss_threshold_exceeded = (
        attempt.limits.reject_if_observed_wait4_normalized_maxrss_bytes_above is not None
        and attempt.wait4_ru_maxrss_normalized_bytes is not None
        and attempt.wait4_ru_maxrss_normalized_bytes
        > attempt.limits.reject_if_observed_wait4_normalized_maxrss_bytes_above
    )
    if (
        "observed_wait4_normalized_maxrss_threshold_exceeded" in failure_reasons
    ) != maxrss_threshold_exceeded:
        raise ValueError("wait4 maxrss threshold evidence and failure ledger differ")
    member_threshold_exceeded = (
        attempt.limits.sampling.reject_if_observed_members_above is not None
        and attempt.peak_observed_sampled_original_group_members is not None
        and attempt.peak_observed_sampled_original_group_members
        > attempt.limits.sampling.reject_if_observed_members_above
    )
    if (
        "sampled_original_group_member_threshold_exceeded" in failure_reasons
    ) != member_threshold_exceeded:
        raise ValueError("sampled member threshold evidence and failure ledger differ")
    rss_threshold_exceeded = (
        attempt.limits.sampling.reject_if_observed_rss_bytes_above is not None
        and attempt.peak_observed_sampled_original_group_rss_bytes is not None
        and attempt.peak_observed_sampled_original_group_rss_bytes
        > attempt.limits.sampling.reject_if_observed_rss_bytes_above
    )
    if (
        "sampled_original_group_rss_threshold_exceeded" in failure_reasons
    ) != rss_threshold_exceeded:
        raise ValueError("sampled RSS threshold evidence and failure ledger differ")
    if attempt.status == "succeeded":
        success_conditions = (
            attempt.process_started,
            attempt.spawn_started_monotonic_ns is not None,
            attempt.spawn_completed_monotonic_ns is not None,
            attempt.returncode == 0,
            attempt.stdin_fully_enqueued,
            attempt.stdin_parent_descriptor_closed,
            attempt.stdout.capture_complete,
            attempt.stderr.capture_complete,
            attempt.stdout.parent_close_attempted,
            attempt.stderr.parent_close_attempted,
            attempt.stdout.parent_descriptor_closed,
            attempt.stderr.parent_descriptor_closed,
            not attempt.stdout.ceiling_exceeded,
            not attempt.stderr.ceiling_exceeded,
            attempt.leader_reaped,
            attempt.sampler_processes_started == attempt.sampler_processes_reaped,
            not attempt.cleanup_failures,
            not attempt.failure_events,
            attempt.evidence_sealed_monotonic_ns <= attempt.total_deadline_monotonic_ns,
            (
                not attempt.limits.sampling.required
                or attempt.group_sample_count > 0
            ),
            attempt.observed_process_group_id == attempt.pid,
            attempt.observed_session_id == attempt.pid,
            attempt.termination_disposition in _SUCCESS_FINAL_GROUP_DISPOSITIONS,
            attempt.original_group_action_disposition
            == attempt.termination_disposition,
            attempt.last_original_group_operation_ns is not None,
            attempt.leader_reaped_monotonic_ns is not None,
        )
        if not all(success_conditions):
            raise ValueError("successful attempt violates closure invariants")


def _load_failure_list(raw: Any, label: str) -> tuple[_FailureEvent, ...]:
    if not isinstance(raw, list):
        raise ValueError(f"{label} must be a list")
    return tuple(_FailureEvent.from_mapping(row) for row in raw)


def load_supervised_process_attempt(
    payload: Mapping[str, Any],
    *,
    expected_request: ProcessRequestBinding | None = None,
) -> SupervisedProcessAttempt:
    """Strictly reopen a durable v2 attempt, rejecting any structural drift."""

    if not isinstance(payload, Mapping):
        raise ValueError("attempt payload must be a mapping")
    try:
        detached = json.loads(_canonical_json(payload))
    except (TypeError, ValueError) as exc:
        raise ValueError("attempt payload is not canonical JSON data") from exc
    expected_top = {
        "schema_version",
        "attempt_kind",
        "attempt_id",
        "status",
        "request",
        "streams",
        "process",
        "timing",
        "resource_observation",
        "sampling",
        "failure_events",
        "primary_failure",
        "cleanup_failures",
        "nonfatal_diagnostics",
        "limits",
        "containment",
        "authority_boundaries",
        "invariant_projection",
        "attempt_digest",
    }
    _require_exact_keys(detached, expected_top, "attempt payload")
    digest = detached.pop("attempt_digest")
    if not _is_sha256(digest) or digest != _value_digest(detached):
        raise ValueError("attempt digest mismatch")
    if detached["schema_version"] != PROCESS_ATTEMPT_SCHEMA_VERSION:
        raise ValueError("attempt schema version mismatch")
    if detached["attempt_kind"] != PROCESS_ATTEMPT_KIND:
        raise ValueError("attempt kind mismatch")
    request = ProcessRequestBinding.from_mapping(detached["request"])
    limits = SupervisionLimits.from_mapping(detached["limits"])
    streams = detached["streams"]
    _require_exact_keys(streams, {"stdout", "stderr"}, "attempt streams")
    stdout = _StreamEvidence.from_mapping(streams["stdout"])
    stderr = _StreamEvidence.from_mapping(streams["stderr"])
    process = detached["process"]
    _require_exact_keys(
        process,
        {
            "process_started",
            "pid",
            "intended_process_group_id",
            "observed_process_group_id",
            "observed_session_id",
            "returncode",
            "leader_reaped",
            "leader_identity_anchor_released",
            "termination_disposition",
            "original_group_action_disposition",
            "stdin_enqueued_bytes",
            "stdin_fully_enqueued",
            "stdin_parent_descriptor_closed",
        },
        "attempt process",
    )
    timing = detached["timing"]
    _require_exact_keys(
        timing,
        {
            "clock",
            "deadline_scope",
            "hard_kernel_preemption",
            "overrun_detected_after_blocking_call_returns",
            "record_serialization_after_evidence_seal_excluded",
            "call_started_ns",
            "spawn_started_ns",
            "spawn_completed_ns",
            "execution_deadline_ns",
            "cleanup_io_deadline_ns",
            "total_deadline_ns",
            "evidence_sealed_ns",
            "leader_reaped_ns",
            "last_original_group_operation_ns",
            "total_elapsed_ns",
            "deadline_overrun_ns",
        },
        "attempt timing",
    )
    resources = detached["resource_observation"]
    _require_exact_keys(
        resources,
        {
            "wait4_accounted_user_cpu_ns",
            "wait4_accounted_system_cpu_ns",
            "wait4_ru_maxrss_raw",
            "wait4_ru_maxrss_unit",
            "wait4_ru_maxrss_normalized_bytes",
            "wait4_accounting_scope",
            "wait4_threshold_semantics",
            "group_threshold_semantics",
        },
        "resource observation",
    )
    sampling = detached["sampling"]
    _require_exact_keys(
        sampling,
        {
            "policy",
            "group_sample_count",
            "peak_observed_sampled_original_group_members",
            "peak_observed_sampled_original_group_zombie_members",
            "peak_observed_sampled_original_group_rss_bytes",
            "sampler_processes_started",
            "sampler_processes_reaped",
            "measurement_scope",
        },
        "sampling evidence",
    )
    failures = _load_failure_list(detached["failure_events"], "failure_events")
    cleanup = _load_failure_list(detached["cleanup_failures"], "cleanup_failures")
    diagnostics = _load_failure_list(
        detached["nonfatal_diagnostics"], "nonfatal_diagnostics"
    )
    primary = detached["primary_failure"]
    if primary != (failures[0].as_dict() if failures else None):
        raise ValueError("primary failure is not the first fatal event")
    attempt = SupervisedProcessAttempt._seal(
        attempt_id=detached["attempt_id"],
        status=detached["status"],
        request=request,
        process_started=process["process_started"],
        stdin_enqueued_bytes=process["stdin_enqueued_bytes"],
        stdin_parent_descriptor_closed=process["stdin_parent_descriptor_closed"],
        stdout=stdout,
        stderr=stderr,
        pid=process["pid"],
        intended_process_group_id=process["intended_process_group_id"],
        observed_process_group_id=process["observed_process_group_id"],
        observed_session_id=process["observed_session_id"],
        returncode=process["returncode"],
        leader_reaped=process["leader_reaped"],
        termination_disposition=process["termination_disposition"],
        original_group_action_disposition=process["original_group_action_disposition"],
        call_started_monotonic_ns=timing["call_started_ns"],
        spawn_started_monotonic_ns=timing["spawn_started_ns"],
        spawn_completed_monotonic_ns=timing["spawn_completed_ns"],
        execution_deadline_monotonic_ns=timing["execution_deadline_ns"],
        cleanup_io_deadline_monotonic_ns=timing["cleanup_io_deadline_ns"],
        total_deadline_monotonic_ns=timing["total_deadline_ns"],
        evidence_sealed_monotonic_ns=timing["evidence_sealed_ns"],
        leader_reaped_monotonic_ns=timing["leader_reaped_ns"],
        last_original_group_operation_ns=timing["last_original_group_operation_ns"],
        wait4_accounted_user_cpu_ns=resources["wait4_accounted_user_cpu_ns"],
        wait4_accounted_system_cpu_ns=resources["wait4_accounted_system_cpu_ns"],
        wait4_ru_maxrss_raw=resources["wait4_ru_maxrss_raw"],
        wait4_ru_maxrss_unit=resources["wait4_ru_maxrss_unit"],
        wait4_ru_maxrss_normalized_bytes=resources["wait4_ru_maxrss_normalized_bytes"],
        group_sample_count=sampling["group_sample_count"],
        peak_observed_sampled_original_group_members=(
            sampling["peak_observed_sampled_original_group_members"]
        ),
        peak_observed_sampled_original_group_zombie_members=(
            sampling["peak_observed_sampled_original_group_zombie_members"]
        ),
        peak_observed_sampled_original_group_rss_bytes=(
            sampling["peak_observed_sampled_original_group_rss_bytes"]
        ),
        sampler_processes_started=sampling["sampler_processes_started"],
        sampler_processes_reaped=sampling["sampler_processes_reaped"],
        failure_events=failures,
        cleanup_failures=cleanup,
        nonfatal_diagnostics=diagnostics,
        limits=limits,
    )
    if process["leader_identity_anchor_released"] != attempt.leader_identity_anchor_released:
        raise ValueError("leader identity release projection mismatch")
    if process["stdin_fully_enqueued"] != attempt.stdin_fully_enqueued:
        raise ValueError("stdin completion projection mismatch")
    if timing["total_elapsed_ns"] != attempt.total_elapsed_ns:
        raise ValueError("total elapsed projection mismatch")
    if timing["deadline_overrun_ns"] != attempt.deadline_overrun_ns:
        raise ValueError("deadline overrun projection mismatch")
    if sampling["policy"] != limits.sampling.as_dict():
        raise ValueError("sampling policy projection mismatch")
    if detached["containment"] != attempt.containment:
        raise ValueError("containment constant mismatch")
    if detached["authority_boundaries"] != attempt.authority_boundaries:
        raise ValueError("authority boundary mismatch")
    if detached["invariant_projection"] != attempt.invariant_projection():
        raise ValueError("invariant projection mismatch")
    regenerated = attempt.as_dict()
    if regenerated != {**detached, "attempt_digest": digest}:
        raise ValueError("attempt payload is not the canonical sealed representation")
    validate_supervised_process_attempt(attempt, expected_request=expected_request)
    return attempt


def run_supervised_process(
    argv: Sequence[str],
    *,
    cwd: Path | str,
    environment: Mapping[str, str],
    input_bytes: bytes,
    limits: SupervisionLimits,
) -> SupervisedProcessAttempt:
    """Run one trusted local process and return closed operational evidence."""

    call_started_ns = time.monotonic_ns()
    if not isinstance(limits, SupervisionLimits):
        raise ValueError("limits must be SupervisionLimits")
    exact_argv, exact_cwd, exact_environment, supplied_input = _validated_invocation(
        argv, cwd, environment, input_bytes
    )
    request: ProcessRequestBinding
    request_failure: tuple[str, str] | None = None
    try:
        request = build_process_request_binding(
            exact_argv,
            cwd=exact_cwd,
            environment=exact_environment,
            input_bytes=supplied_input,
            limits=limits,
        )
    except FileNotFoundError as exc:
        request_failure = ("sampling_executable_unavailable", str(exc))
        disabled_limits = SupervisionLimits(
            total_deadline_ns=limits.total_deadline_ns,
            cleanup_reserve_ns=limits.cleanup_reserve_ns,
            termination_grace_ns=limits.termination_grace_ns,
            evidence_seal_reserve_ns=limits.evidence_seal_reserve_ns,
            stdin_limit_bytes=limits.stdin_limit_bytes,
            stdout_limit_bytes=limits.stdout_limit_bytes,
            stderr_limit_bytes=limits.stderr_limit_bytes,
            stdout_retained_tail_bytes=limits.stdout_retained_tail_bytes,
            stderr_retained_tail_bytes=limits.stderr_retained_tail_bytes,
            sampling=ProcessGroupSamplingPolicy(
                mode="disabled",
                required=False,
                interval_ns=limits.sampling.interval_ns,
                attempt_timeout_ns=limits.sampling.attempt_timeout_ns,
                cleanup_reserve_ns=limits.sampling.cleanup_reserve_ns,
                stdout_limit_bytes=limits.sampling.stdout_limit_bytes,
                stderr_limit_bytes=limits.sampling.stderr_limit_bytes,
            ),
            reject_if_observed_wait4_cpu_ns_above=(
                limits.reject_if_observed_wait4_cpu_ns_above
            ),
            reject_if_observed_wait4_normalized_maxrss_bytes_above=(
                limits.reject_if_observed_wait4_normalized_maxrss_bytes_above
            ),
        )
        request = build_process_request_binding(
            exact_argv,
            cwd=exact_cwd,
            environment=exact_environment,
            input_bytes=supplied_input,
            limits=disabled_limits,
        )
        # Preserve the requested limits digest even though no sampler path exists.
        object.__setattr__(request, "limits_digest", _value_digest(limits.as_dict()))
        material = request.as_dict()
        material.pop("request_digest")
        object.__setattr__(request, "request_digest", _value_digest(material))

    total_deadline_ns = call_started_ns + limits.total_deadline_ns
    execution_deadline_ns = total_deadline_ns - limits.cleanup_reserve_ns
    cleanup_io_deadline_ns = total_deadline_ns - limits.evidence_seal_reserve_ns
    attempt_id = "process-attempt." + hashlib.sha256(
        _canonical_json(
            {
                "request_digest": request.request_digest,
                "call_started_monotonic_ns": call_started_ns,
            }
        )
    ).hexdigest()[:32]

    process: subprocess.Popen[bytes] | None = None
    selector: selectors.BaseSelector | None = None
    stdout_capture = _StreamCapture(
        ceiling_bytes=limits.stdout_limit_bytes,
        retained_bytes=limits.stdout_retained_tail_bytes,
    )
    stderr_capture = _StreamCapture(
        ceiling_bytes=limits.stderr_limit_bytes,
        retained_bytes=limits.stderr_retained_tail_bytes,
    )
    descriptor_existed = {"stdin": False, "stdout": False, "stderr": False}
    close_attempted = {"stdin": False, "stdout": False, "stderr": False}
    descriptor_closed = {"stdin": True, "stdout": True, "stderr": True}
    stdin_enqueued = 0
    spawn_started_ns: int | None = None
    spawn_completed_ns: int | None = None
    observed_pgid: int | None = None
    observed_sid: int | None = None
    wait4_evidence: _Wait4Evidence | None = None
    leader_ownership_lost = False
    group_actions_finalized = False
    last_group_operation_ns: int | None = None
    termination = "not_started"
    group_action_disposition = "not_started"
    fatal: list[_FailureEvent] = []
    cleanup_failures: list[_FailureEvent] = []
    diagnostics: list[_FailureEvent] = []
    group_sample_count = 0
    peak_members: int | None = None
    peak_zombies: int | None = None
    peak_group_rss: int | None = None
    sampler_started = 0
    sampler_reaped = 0
    next_sample_ns = call_started_ns
    sampling_terminal = False
    selector_usable = True

    def add_fatal(category: str, stage: str, reason: str, message: str) -> None:
        identity = (category, stage, reason)
        if any((row.category, row.stage, row.reason_code) == identity for row in fatal):
            return
        if len(fatal) >= _MAX_FAILURE_EVENTS:
            return
        if len(fatal) == _MAX_FAILURE_EVENTS - 1 and reason != "failure_ledger_capacity_exhausted":
            fatal.append(
                _FailureEvent.build(
                    len(fatal),
                    "operational",
                    "supervisor",
                    "failure_ledger_capacity_exhausted",
                    "additional distinct failures were suppressed at the fixed ledger ceiling",
                )
            )
            return
        fatal.append(_FailureEvent.build(len(fatal), category, stage, reason, message))

    def add_cleanup(stage: str, reason: str, message: str) -> None:
        if any(row.stage == stage and row.reason_code == reason for row in cleanup_failures):
            return
        before = len(fatal)
        add_fatal("cleanup", stage, reason, message)
        if len(fatal) > before and fatal[-1].category == "cleanup":
            cleanup_failures.append(fatal[-1])

    def add_diagnostic(stage: str, reason: str, message: str) -> None:
        if any(row.stage == stage and row.reason_code == reason for row in diagnostics):
            return
        if len(diagnostics) >= _MAX_DIAGNOSTIC_EVENTS:
            return
        if (
            len(diagnostics) == _MAX_DIAGNOSTIC_EVENTS - 1
            and reason != "diagnostic_ledger_capacity_exhausted"
        ):
            diagnostics.append(
                _FailureEvent.build(
                    len(diagnostics),
                    "diagnostic",
                    "supervisor",
                    "diagnostic_ledger_capacity_exhausted",
                    "additional distinct diagnostics were suppressed at the fixed ledger ceiling",
                )
            )
            return
        diagnostics.append(
            _FailureEvent.build(len(diagnostics), "diagnostic", stage, reason, message)
        )

    def close_stream(stream: Any, label: str) -> None:
        if stream is None:
            return
        close_attempted[label] = True
        if selector is not None:
            try:
                selector.unregister(stream)
            except (KeyError, ValueError):
                pass
            except Exception as exc:
                add_cleanup(
                    "descriptor_cleanup",
                    f"{label}_selector_unregister_failed",
                    f"{type(exc).__name__}: {exc}",
                )
            except BaseException as exc:
                if pending_host_exception is None:
                    raise
                add_cleanup(
                    "host_control_cleanup",
                    "cleanup_host_exception_suppressed",
                    f"selector unregister: {type(exc).__name__}: {exc}",
                )
        try:
            stream.close()
        except Exception as exc:
            add_cleanup(
                "descriptor_cleanup",
                f"{label}_close_failed",
                f"{type(exc).__name__}: {exc}",
            )
        except BaseException as exc:
            if pending_host_exception is None:
                raise
            add_cleanup(
                "host_control_cleanup",
                "cleanup_host_exception_suppressed",
                f"stream close: {type(exc).__name__}: {exc}",
            )
        try:
            descriptor_closed[label] = bool(getattr(stream, "closed", False))
        except BaseException as exc:
            if pending_host_exception is None:
                raise
            descriptor_closed[label] = False
            add_cleanup(
                "host_control_cleanup",
                "cleanup_host_exception_suppressed",
                f"stream closure observation: {type(exc).__name__}: {exc}",
            )
        if not descriptor_closed[label] and not any(
            event.reason_code == f"{label}_close_failed" for event in cleanup_failures
        ):
            add_cleanup(
                "descriptor_cleanup",
                f"{label}_close_unverified",
                "the parent descriptor did not report a closed state",
            )

    def read_ready(stream: Any, label: str) -> None:
        capture = stdout_capture if label == "stdout" else stderr_capture
        try:
            chunk = os.read(stream.fileno(), _READ_CHUNK_BYTES)
        except BlockingIOError:
            return
        except Exception as exc:
            capture.read_failed = True
            add_fatal(
                "operational",
                "transport",
                f"{label}_read_failed",
                f"{type(exc).__name__}: {exc}",
            )
            close_stream(stream, label)
            return
        except BaseException as exc:
            if pending_host_exception is None:
                raise
            capture.read_failed = True
            add_cleanup(
                "host_control_cleanup",
                "cleanup_host_exception_suppressed",
                f"stream read: {type(exc).__name__}: {exc}",
            )
            close_stream(stream, label)
            return
        if not chunk:
            capture.eof_observed = True
            close_stream(stream, label)
            return
        capture.add(chunk)
        if capture.ceiling_bytes is not None and capture.captured_bytes > capture.ceiling_bytes:
            add_fatal(
                "policy",
                "transport",
                f"{label}_limit_exceeded",
                f"{label} exceeded its fixed byte ceiling",
            )

    def pump_io(deadline_ns: int, *, allow_stdin: bool) -> None:
        nonlocal stdin_enqueued, selector_usable
        now_ns = time.monotonic_ns()
        if now_ns >= deadline_ns or selector is None or not selector_usable:
            return
        try:
            selector_map = selector.get_map()
        except Exception as exc:
            selector_usable = False
            add_fatal(
                "operational",
                "selector",
                "selector_map_failed",
                f"{type(exc).__name__}: {exc}",
            )
            return
        except BaseException as exc:
            if pending_host_exception is None:
                raise
            selector_usable = False
            add_cleanup(
                "host_control_cleanup",
                "cleanup_host_exception_suppressed",
                f"{type(exc).__name__}: {exc}",
            )
            return
        if not selector_map:
            return
        timeout_ns = min(_SELECT_QUANTUM_NS, deadline_ns - now_ns)
        try:
            events = selector.select(timeout=timeout_ns / 1_000_000_000)
        except Exception as exc:
            selector_usable = False
            add_fatal(
                "operational",
                "selector",
                "selector_select_failed",
                f"{type(exc).__name__}: {exc}",
            )
            return
        except BaseException as exc:
            if pending_host_exception is None:
                raise
            selector_usable = False
            add_cleanup(
                "host_control_cleanup",
                "cleanup_host_exception_suppressed",
                f"{type(exc).__name__}: {exc}",
            )
            return
        for key, _mask in events:
            label = str(key.data)
            stream = key.fileobj
            if label == "stdin":
                if not allow_stdin:
                    close_stream(stream, "stdin")
                    continue
                try:
                    written = os.write(
                        stream.fileno(),
                        supplied_input[stdin_enqueued : stdin_enqueued + _READ_CHUNK_BYTES],
                    )
                except BlockingIOError:
                    continue
                except Exception as exc:
                    add_fatal(
                        "operational",
                        "transport",
                        "stdin_write_failed",
                        f"{type(exc).__name__}: {exc}",
                    )
                    close_stream(stream, "stdin")
                    continue
                except BaseException as exc:
                    if pending_host_exception is None:
                        raise
                    add_cleanup(
                        "host_control_cleanup",
                        "cleanup_host_exception_suppressed",
                        f"stdin write: {type(exc).__name__}: {exc}",
                    )
                    close_stream(stream, "stdin")
                    continue
                if written <= 0:
                    add_fatal(
                        "operational",
                        "transport",
                        "stdin_write_failed",
                        "stdin accepted no bytes",
                    )
                    close_stream(stream, "stdin")
                    continue
                stdin_enqueued += written
                if stdin_enqueued == len(supplied_input):
                    close_stream(stream, "stdin")
            else:
                read_ready(stream, label)
            if fatal:
                return

    def signal_original_group(
        requested_signal: int,
        disposition: str,
        *,
        eof_terminal_boundary: bool = False,
    ) -> None:
        nonlocal last_group_operation_ns, termination, group_action_disposition
        if process is None or wait4_evidence is not None or leader_ownership_lost:
            add_cleanup(
                "process_cleanup",
                "post_reap_original_group_operation_blocked",
                "an original-group signal was refused after the PID anchor was released",
            )
            return
        last_group_operation_ns = time.monotonic_ns()
        try:
            # start_new_session=True is performed in the child before exec and
            # Popen does not return a successful child until that setup passes.
            # The unreaped PID therefore anchors the intended same-valued PGID
            # even when a very fast child is already a zombie before getpgid.
            os.killpg(process.pid, requested_signal)
            termination = disposition
            group_action_disposition = disposition
        except ProcessLookupError:
            group_action_disposition = f"{disposition}_no_signalable_member"
            termination = group_action_disposition
        except PermissionError as exc:
            if eof_terminal_boundary:
                # Darwin may report EPERM for a zombie-only process group.  The
                # unreaped same-UID leader is still the numeric identity anchor;
                # this is absence of a signalable member, not containment proof.
                group_action_disposition = f"{disposition}_no_signalable_member"
                termination = group_action_disposition
                add_diagnostic(
                    "process_cleanup",
                    "final_group_no_signalable_member",
                    f"{type(exc).__name__}: {exc}",
                )
            else:
                add_cleanup(
                    "process_cleanup",
                    "original_group_signal_failed",
                    f"{disposition}: {type(exc).__name__}: {exc}",
                )
        except Exception as exc:
            add_cleanup(
                "process_cleanup",
                "original_group_signal_failed",
                f"{disposition}: {type(exc).__name__}: {exc}",
            )
        except BaseException as exc:
            if pending_host_exception is None:
                raise
            add_cleanup(
                "host_control_cleanup",
                "cleanup_host_exception_suppressed",
                f"group signal {disposition}: {type(exc).__name__}: {exc}",
            )

    def reap_after_group_actions() -> None:
        nonlocal wait4_evidence, leader_ownership_lost
        if process is None or wait4_evidence is not None or leader_ownership_lost:
            return
        if not group_actions_finalized:
            add_cleanup(
                "process_wait",
                "leader_reap_before_group_actions_finalized_blocked",
                "wait4 was refused before final original-group action",
            )
            return
        try:
            evidence = _wait4_nohang(process.pid)
        except ChildProcessError as exc:
            leader_ownership_lost = True
            add_cleanup("process_wait", "leader_ownership_lost", str(exc))
            return
        except Exception as exc:
            add_cleanup(
                "process_wait",
                "direct_child_wait_failed",
                f"{type(exc).__name__}: {exc}",
            )
            return
        except BaseException as exc:
            if pending_host_exception is None:
                raise
            add_cleanup(
                "host_control_cleanup",
                "cleanup_host_exception_suppressed",
                f"wait4 cleanup: {type(exc).__name__}: {exc}",
            )
            return
        if evidence is not None:
            wait4_evidence = evidence
            process.returncode = evidence.returncode

    def perform_sample() -> None:
        nonlocal last_group_operation_ns, sampler_started, sampler_reaped
        nonlocal group_sample_count, peak_members, peak_zombies, peak_group_rss
        nonlocal sampling_terminal
        if process is None or limits.sampling.mode == "disabled":
            return
        if sampler_started >= limits.sampling.maximum_attempts:
            sampling_terminal = True
            return
        if wait4_evidence is not None or leader_ownership_lost:
            add_cleanup(
                "sampling",
                "post_reap_original_group_sampling_blocked",
                "sampling was refused after the PID anchor was released",
            )
            return
        remaining_ns = execution_deadline_ns - time.monotonic_ns()
        if remaining_ns < limits.sampling.attempt_timeout_ns:
            message = "insufficient execution budget remained for a full sampler attempt"
            if limits.sampling.required:
                add_fatal("operational", "sampling", "sampler_budget_unavailable", message)
            else:
                add_diagnostic("sampling", "sampler_budget_unavailable", message)
            return
        last_group_operation_ns = time.monotonic_ns()
        result = _run_ps_sampler(
            process.pid,
            executable=request.sampling_executable or "",
            policy=limits.sampling,
            parent_execution_deadline_ns=execution_deadline_ns,
        )
        sampler_started += int(result.started)
        sampler_reaped += int(result.reaped)
        if sampler_started >= limits.sampling.maximum_attempts:
            sampling_terminal = True
        if result.started and not result.reaped:
            add_cleanup(
                "sampling",
                "sampler_not_reaped",
                result.failure_message or "sampler process was not reaped",
            )
        if result.failure_reason is not None:
            if limits.sampling.required:
                add_fatal(
                    "operational",
                    "sampling",
                    result.failure_reason,
                    result.failure_message or result.failure_reason,
                )
            else:
                add_diagnostic(
                    "sampling",
                    result.failure_reason,
                    result.failure_message or result.failure_reason,
                )
            return
        if result.sample is None:
            add_fatal(
                "operational", "sampling", "sampler_result_missing", "sampler returned no observation"
            )
            return
        group_sample_count += 1
        peak_members = max(peak_members or 0, result.sample.members)
        peak_zombies = max(peak_zombies or 0, result.sample.zombie_members)
        peak_group_rss = max(peak_group_rss or 0, result.sample.rss_bytes)
        if (
            limits.sampling.reject_if_observed_members_above is not None
            and result.sample.members
            > limits.sampling.reject_if_observed_members_above
        ):
            add_fatal(
                "policy",
                "sampling",
                "sampled_original_group_member_threshold_exceeded",
                "one sampled original-group observation exceeded its member threshold",
            )
        if (
            limits.sampling.reject_if_observed_rss_bytes_above is not None
            and result.sample.rss_bytes
            > limits.sampling.reject_if_observed_rss_bytes_above
        ):
            add_fatal(
                "policy",
                "sampling",
                "sampled_original_group_rss_threshold_exceeded",
                "one sampled original-group observation exceeded its RSS threshold",
            )

    pending_host_exception: BaseException | None = None
    pending_host_traceback: Any = None
    try:
        if len(supplied_input) > limits.stdin_limit_bytes:
            add_fatal(
                "policy",
                "prelaunch",
                "input_limit_exceeded",
                "stdin bytes exceed the fixed prelaunch ceiling",
            )
        elif request_failure is not None:
            add_fatal("operational", "prelaunch", request_failure[0], request_failure[1])
        elif (
            os.name != "posix"
            or not hasattr(os, "wait4")
            or not hasattr(os, "killpg")
            or not hasattr(os, "setsid")
        ):
            add_fatal(
                "operational",
                "prelaunch",
                "unsupported_platform",
                "supervision requires POSIX wait4, sessions, and process groups",
            )
        elif time.monotonic_ns() >= execution_deadline_ns:
            add_fatal(
                "operational",
                "prelaunch",
                "request_preparation_consumed_execution_deadline",
                "request validation and identity binding exhausted execution time",
            )
        else:
            try:
                spawn_started_ns = time.monotonic_ns()
                process = subprocess.Popen(
                    list(exact_argv),
                    cwd=exact_cwd,
                    env=exact_environment,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=False,
                    start_new_session=True,
                    close_fds=True,
                )
                spawn_completed_ns = time.monotonic_ns()
                termination = "running_anchored"
                if process.stdin is None or process.stdout is None or process.stderr is None:
                    add_fatal(
                        "operational", "launch", "pipe_creation_failed", "protocol pipes are unavailable"
                    )
                else:
                    for label in descriptor_existed:
                        descriptor_existed[label] = True
                        descriptor_closed[label] = False
                    try:
                        observed_pgid = os.getpgid(process.pid)
                        observed_sid = os.getsid(process.pid)
                    except ProcessLookupError:
                        observed_pgid = None
                        observed_sid = None
                        add_fatal(
                            "operational",
                            "launch_setup",
                            "session_observation_unavailable",
                            (
                                "the child became unobservable before its intended fresh "
                                "session and process group could be independently observed"
                            ),
                        )
                    except Exception as exc:
                        add_fatal(
                            "operational",
                            "launch_setup",
                            "session_observation_failed",
                            f"{type(exc).__name__}: {exc}",
                        )
                    if observed_pgid not in {None, process.pid} or observed_sid not in {
                        None,
                        process.pid,
                    }:
                        add_fatal(
                            "operational",
                            "launch_setup",
                            "fresh_session_observation_mismatch",
                            "child was observed outside its intended fresh session",
                        )
                    try:
                        selector = selectors.DefaultSelector()
                        for stream, events, label in (
                            (process.stdin, selectors.EVENT_WRITE, "stdin"),
                            (process.stdout, selectors.EVENT_READ, "stdout"),
                            (process.stderr, selectors.EVENT_READ, "stderr"),
                        ):
                            os.set_blocking(stream.fileno(), False)
                            selector.register(stream, events, data=label)
                    except Exception as exc:
                        add_fatal(
                            "operational",
                            "launch_setup",
                            "selector_setup_failed",
                            f"{type(exc).__name__}: {exc}",
                        )
                    if not supplied_input and process.stdin is not None:
                        close_stream(process.stdin, "stdin")
                    if spawn_completed_ns >= execution_deadline_ns:
                        add_fatal(
                            "operational",
                            "launch",
                            "launch_consumed_execution_deadline",
                            "process launch returned after the cleanup-reserved deadline",
                        )
            except Exception as exc:
                spawn_completed_ns = time.monotonic_ns()
                add_fatal(
                    "operational",
                    "launch",
                    "process_launch_failed",
                    f"{type(exc).__name__}: {exc}",
                )

        while process is not None and not fatal:
            now_ns = time.monotonic_ns()
            if now_ns >= execution_deadline_ns:
                add_fatal(
                    "operational",
                    "execution",
                    "execution_deadline_exhausted",
                    "execution reached the cleanup-reserved monotonic deadline",
                )
                break
            if (
                limits.sampling.mode == "posix_ps"
                and not sampling_terminal
                and now_ns >= next_sample_ns
            ):
                perform_sample()
                next_sample_ns = time.monotonic_ns() + limits.sampling.interval_ns
                if fatal:
                    break
            pump_io(execution_deadline_ns, allow_stdin=True)
            if stdout_capture.eof_observed and stderr_capture.eof_observed:
                break
        if (
            process is not None
            and not fatal
            and stdout_capture.eof_observed
            and stderr_capture.eof_observed
            and limits.sampling.mode == "posix_ps"
            and not sampling_terminal
        ):
            # Observe the original group again at the terminal stream boundary.
            # An earlier sample can precede a late descendant spawn, while EOF
            # can arrive after that descendant deliberately closes inherited
            # descriptors.  The unreaped leader still anchors the exact PGID.
            perform_sample()
        if process is not None and not fatal and (
            not stdout_capture.eof_observed or not stderr_capture.eof_observed
        ):
            add_fatal(
                "operational",
                "execution",
                "execution_ended_without_both_output_eofs",
                "execution loop ended without complete output terminal signals",
            )
    except Exception as exc:
        add_fatal(
            "operational",
            "supervisor",
            "supervisor_internal_exception",
            f"{type(exc).__name__}: {exc}",
        )
    except BaseException as exc:
        pending_host_exception = exc
        pending_host_traceback = exc.__traceback__
    finally:
        if process is not None and process.stdin is not None and not descriptor_closed["stdin"]:
            close_stream(process.stdin, "stdin")

        if process is not None and wait4_evidence is None and not leader_ownership_lost:
            ordinary_eof = stdout_capture.eof_observed and stderr_capture.eof_observed and not fatal
            if ordinary_eof:
                signal_original_group(
                    signal.SIGKILL,
                    "final_group_quiescence_sigkill_sent",
                    eof_terminal_boundary=True,
                )
            else:
                signal_original_group(signal.SIGTERM, "sigterm_sent")
                grace_deadline_ns = min(
                    cleanup_io_deadline_ns,
                    time.monotonic_ns() + limits.termination_grace_ns,
                )
                while time.monotonic_ns() < grace_deadline_ns:
                    pump_io(grace_deadline_ns, allow_stdin=False)
                    remaining_ns = grace_deadline_ns - time.monotonic_ns()
                    if remaining_ns > 0:
                        try:
                            time.sleep(min(0.002, remaining_ns / 1_000_000_000))
                        except BaseException as exc:
                            if pending_host_exception is None:
                                raise
                            add_cleanup(
                                "host_control_cleanup",
                                "cleanup_host_exception_suppressed",
                                f"termination grace sleep: {type(exc).__name__}: {exc}",
                            )
                signal_original_group(
                    signal.SIGKILL,
                    "sigkill_sent",
                    eof_terminal_boundary=(
                        stdout_capture.eof_observed and stderr_capture.eof_observed
                    ),
                )
            group_actions_finalized = True

            while time.monotonic_ns() < cleanup_io_deadline_ns and wait4_evidence is None and not leader_ownership_lost:
                pump_io(cleanup_io_deadline_ns, allow_stdin=False)
                reap_after_group_actions()
                if wait4_evidence is None and not leader_ownership_lost:
                    remaining = cleanup_io_deadline_ns - time.monotonic_ns()
                    if remaining > 0:
                        try:
                            time.sleep(min(0.002, remaining / 1_000_000_000))
                        except BaseException as exc:
                            if pending_host_exception is None:
                                raise
                            add_cleanup(
                                "host_control_cleanup",
                                "cleanup_host_exception_suppressed",
                                f"reap polling sleep: {type(exc).__name__}: {exc}",
                            )
            if wait4_evidence is None and not leader_ownership_lost:
                add_cleanup(
                    "process_wait",
                    "direct_child_not_reaped_before_cleanup_deadline",
                    "the direct child did not reach a wait4 terminal state before evidence sealing",
                )

        while (
            process is not None
            and time.monotonic_ns() < cleanup_io_deadline_ns
            and (not stdout_capture.eof_observed or not stderr_capture.eof_observed)
        ):
            pump_io(cleanup_io_deadline_ns, allow_stdin=False)
            if selector is None or not selector_usable:
                break
            try:
                if not selector.get_map():
                    break
            except Exception as exc:
                selector_usable = False
                add_cleanup(
                    "descriptor_cleanup",
                    "selector_map_failed",
                    f"{type(exc).__name__}: {exc}",
                )
                break
            except BaseException as exc:
                if pending_host_exception is None:
                    raise
                selector_usable = False
                add_cleanup(
                    "host_control_cleanup",
                    "cleanup_host_exception_suppressed",
                    f"final selector map: {type(exc).__name__}: {exc}",
                )
                break

        if process is not None:
            close_stream(process.stdin, "stdin")
            close_stream(process.stdout, "stdout")
            close_stream(process.stderr, "stderr")
        if selector is not None:
            try:
                selector.close()
            except Exception as exc:
                add_cleanup(
                    "descriptor_cleanup",
                    "selector_close_failed",
                    f"{type(exc).__name__}: {exc}",
                )
            except BaseException as exc:
                if pending_host_exception is None:
                    raise
                add_cleanup(
                    "host_control_cleanup",
                    "cleanup_host_exception_suppressed",
                    f"selector close: {type(exc).__name__}: {exc}",
                )

    if wait4_evidence is not None:
        if wait4_evidence.returncode != 0:
            add_fatal(
                "worker",
                "process_exit",
                "worker_exit_nonzero",
                f"direct child exited with return code {wait4_evidence.returncode}",
            )
        observed_cpu = wait4_evidence.user_cpu_ns + wait4_evidence.system_cpu_ns
        if (
            limits.reject_if_observed_wait4_cpu_ns_above is not None
            and observed_cpu > limits.reject_if_observed_wait4_cpu_ns_above
        ):
            add_fatal(
                "policy",
                "resource_observation",
                "observed_wait4_cpu_threshold_exceeded",
                "wait4 CPU observation exceeded its post-exit acceptance threshold",
            )
        if (
            limits.reject_if_observed_wait4_normalized_maxrss_bytes_above is not None
            and wait4_evidence.normalized_maxrss_bytes is not None
            and wait4_evidence.normalized_maxrss_bytes
            > limits.reject_if_observed_wait4_normalized_maxrss_bytes_above
        ):
            add_fatal(
                "policy",
                "resource_observation",
                "observed_wait4_normalized_maxrss_threshold_exceeded",
                "wait4 maxrss observation exceeded its post-exit acceptance threshold",
            )
    if process is not None and wait4_evidence is None and not any(
        event.reason_code in {"leader_ownership_lost", "direct_child_not_reaped_before_cleanup_deadline"}
        for event in fatal
    ):
        add_fatal(
            "operational",
            "process_wait",
            "direct_child_not_reaped",
            "the direct child lacks a terminal wait4 observation",
        )
    if process is not None and stdin_enqueued != len(supplied_input):
        add_fatal(
            "operational",
            "transport",
            "stdin_incomplete",
            "the exact input was not completely enqueued to the child pipe",
        )
    if limits.sampling.required and process is not None and group_sample_count == 0:
        add_fatal(
            "operational",
            "sampling",
            "required_sampling_observation_missing",
            "required sampling produced no valid original-group observation",
        )
    if sampler_started != sampler_reaped:
        add_cleanup(
            "sampling",
            "sampler_process_reap_count_mismatch",
            "not every started sampler process was reaped",
        )

    stdout_evidence = stdout_capture.freeze(
        descriptor_existed=descriptor_existed["stdout"],
        close_attempted=close_attempted["stdout"],
        descriptor_closed=descriptor_closed["stdout"],
    )
    stderr_evidence = stderr_capture.freeze(
        descriptor_existed=descriptor_existed["stderr"],
        close_attempted=close_attempted["stderr"],
        descriptor_closed=descriptor_closed["stderr"],
    )
    evidence_sealed_ns = time.monotonic_ns()
    if evidence_sealed_ns > total_deadline_ns:
        add_fatal(
            "operational",
            "evidence_seal",
            "total_deadline_overrun_detected",
            "stream evidence sealing completed after the total monotonic deadline",
        )
    if pending_host_exception is not None:
        raise pending_host_exception.with_traceback(pending_host_traceback)

    failure_tuple = tuple(fatal)
    status = _derived_status(failure_tuple)
    return SupervisedProcessAttempt._seal(
        attempt_id=attempt_id,
        status=status,
        request=request,
        process_started=process is not None,
        stdin_enqueued_bytes=stdin_enqueued,
        stdin_parent_descriptor_closed=descriptor_closed["stdin"],
        stdout=stdout_evidence,
        stderr=stderr_evidence,
        pid=process.pid if process is not None else None,
        intended_process_group_id=process.pid if process is not None else None,
        observed_process_group_id=observed_pgid,
        observed_session_id=observed_sid,
        returncode=wait4_evidence.returncode if wait4_evidence is not None else None,
        leader_reaped=wait4_evidence is not None,
        termination_disposition=termination,
        original_group_action_disposition=group_action_disposition,
        call_started_monotonic_ns=call_started_ns,
        spawn_started_monotonic_ns=spawn_started_ns,
        spawn_completed_monotonic_ns=spawn_completed_ns,
        execution_deadline_monotonic_ns=execution_deadline_ns,
        cleanup_io_deadline_monotonic_ns=cleanup_io_deadline_ns,
        total_deadline_monotonic_ns=total_deadline_ns,
        evidence_sealed_monotonic_ns=evidence_sealed_ns,
        leader_reaped_monotonic_ns=(
            wait4_evidence.reaped_ns if wait4_evidence is not None else None
        ),
        last_original_group_operation_ns=last_group_operation_ns,
        wait4_accounted_user_cpu_ns=(
            wait4_evidence.user_cpu_ns if wait4_evidence is not None else None
        ),
        wait4_accounted_system_cpu_ns=(
            wait4_evidence.system_cpu_ns if wait4_evidence is not None else None
        ),
        wait4_ru_maxrss_raw=(
            wait4_evidence.maxrss_raw if wait4_evidence is not None else None
        ),
        wait4_ru_maxrss_unit=(
            wait4_evidence.maxrss_unit if wait4_evidence is not None else None
        ),
        wait4_ru_maxrss_normalized_bytes=(
            wait4_evidence.normalized_maxrss_bytes
            if wait4_evidence is not None
            else None
        ),
        group_sample_count=group_sample_count,
        peak_observed_sampled_original_group_members=peak_members,
        peak_observed_sampled_original_group_zombie_members=peak_zombies,
        peak_observed_sampled_original_group_rss_bytes=peak_group_rss,
        sampler_processes_started=sampler_started,
        sampler_processes_reaped=sampler_reaped,
        failure_events=failure_tuple,
        cleanup_failures=tuple(cleanup_failures),
        nonfatal_diagnostics=tuple(diagnostics),
        limits=limits,
    )


__all__ = [
    "AUTHORITY_BOUNDARY",
    "CONTAINMENT_MODE",
    "PROCESS_ATTEMPT_KIND",
    "PROCESS_ATTEMPT_SCHEMA_VERSION",
    "ProcessGroupSamplingPolicy",
    "ProcessRequestBinding",
    "SupervisedProcessAttempt",
    "SupervisionLimits",
    "build_process_request_binding",
    "load_supervised_process_attempt",
    "run_supervised_process",
    "validate_supervised_process_attempt",
]
