# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Closed-contract tests for the v2 trusted local process supervisor.

The suite deliberately keeps scientific and semantic authority outside this
module.  It tests only exact request identity, bounded local process handling,
PID/PGID lifetime ordering, capture completeness, honest resource scopes, and
strict receipt validation.

Most tests disable operating-system sampling so failures are deterministic.
The small sampling lane uses either the real absolute ``ps`` executable or a
private executable-resolution seam; no arbitrary Python sampler is admitted by
the public API.
"""

from __future__ import annotations

import base64
import copy
import errno
import hashlib
import inspect
import json
import os
import platform
import selectors
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable, Mapping

import pytest

import agentic.process_supervision as supervision
from agentic.process_supervision import (
    AUTHORITY_BOUNDARY,
    CONTAINMENT_MODE,
    PROCESS_ATTEMPT_KIND,
    PROCESS_ATTEMPT_SCHEMA_VERSION,
    ProcessGroupSamplingPolicy,
    ProcessRequestBinding,
    SupervisedProcessAttempt,
    SupervisionLimits,
    build_process_request_binding,
    load_supervised_process_attempt,
    run_supervised_process,
    validate_supervised_process_attempt,
)


pytestmark = pytest.mark.skipif(
    os.name != "posix" or not hasattr(os, "wait4"),
    reason="the supervised process contract is explicitly POSIX/wait4-only",
)

_ROOT = Path.cwd().resolve()
_PYTHON = str(Path(sys.executable).resolve(strict=True))
_REAL_SELECTOR_FACTORY = selectors.DefaultSelector


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(value)).hexdigest()


def _rehash_payload(payload: dict[str, Any]) -> dict[str, Any]:
    payload.pop("attempt_digest", None)
    payload["attempt_digest"] = _digest(payload)
    return payload


def _reseal_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Recompute every public derived binding around an adversarial mutation."""

    request = payload["request"]
    request["limits_digest"] = _digest(payload["limits"])
    request_material = copy.deepcopy(request)
    request_material.pop("request_digest", None)
    request["request_digest"] = _digest(request_material)
    payload["attempt_id"] = "process-attempt." + hashlib.sha256(
        _canonical_json(
            {
                "request_digest": request["request_digest"],
                "call_started_monotonic_ns": payload["timing"]["call_started_ns"],
            }
        )
    ).hexdigest()[:32]

    process = payload["process"]
    process["stdin_fully_enqueued"] = (
        process["stdin_enqueued_bytes"] == request["stdin_bytes"]
    )
    process["leader_identity_anchor_released"] = bool(
        process["leader_reaped"]
        or any(
            row["reason_code"] == "leader_ownership_lost"
            for row in payload["failure_events"]
        )
    )
    timing = payload["timing"]
    timing["total_elapsed_ns"] = max(
        0,
        timing["evidence_sealed_ns"] - timing["call_started_ns"],
    )
    timing["deadline_overrun_ns"] = max(
        0,
        timing["evidence_sealed_ns"] - timing["total_deadline_ns"],
    )
    payload["sampling"]["policy"] = copy.deepcopy(payload["limits"]["sampling"])
    payload["primary_failure"] = (
        copy.deepcopy(payload["failure_events"][0])
        if payload["failure_events"]
        else None
    )

    projection = payload["invariant_projection"]
    projection["request"] = copy.deepcopy(request)
    outcome = projection["outcome"]
    outcome.update(
        {
            "status": payload["status"],
            "process_started": process["process_started"],
            "returncode": process["returncode"],
            "stdin_fully_enqueued": process["stdin_fully_enqueued"],
            "stdout_captured_bytes": payload["streams"]["stdout"]["captured_bytes"],
            "stdout_captured_sha256": payload["streams"]["stdout"]["captured_sha256"],
            "stdout_eof_observed": payload["streams"]["stdout"]["eof_observed"],
            "stderr_captured_bytes": payload["streams"]["stderr"]["captured_bytes"],
            "stderr_captured_sha256": payload["streams"]["stderr"]["captured_sha256"],
            "stderr_eof_observed": payload["streams"]["stderr"]["eof_observed"],
            "failure_reason_codes": [
                row["reason_code"] for row in payload["failure_events"]
            ],
            "cleanup_reason_codes": [
                row["reason_code"] for row in payload["cleanup_failures"]
            ],
        }
    )
    projection.pop("projection_digest", None)
    projection["projection_digest"] = _digest(projection)
    return _rehash_payload(payload)


def _environment(**extra: str) -> dict[str, str]:
    return {
        "LANG": "C",
        "LC_ALL": "C",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONUTF8": "1",
        **extra,
    }


def _sampling(**overrides: Any) -> ProcessGroupSamplingPolicy:
    values: dict[str, Any] = {
        "mode": "disabled",
        "required": False,
        "interval_ns": 50_000_000,
        "attempt_timeout_ns": 250_000_000,
        "cleanup_reserve_ns": 75_000_000,
        "stdout_limit_bytes": 2 * 1024 * 1024,
        "stderr_limit_bytes": 64 * 1024,
        "reject_if_observed_members_above": None,
        "reject_if_observed_rss_bytes_above": None,
    }
    values.update(overrides)
    return ProcessGroupSamplingPolicy(**values)


def _limits(**overrides: Any) -> SupervisionLimits:
    values: dict[str, Any] = {
        "total_deadline_ns": 3_000_000_000,
        "cleanup_reserve_ns": 500_000_000,
        "termination_grace_ns": 100_000_000,
        "evidence_seal_reserve_ns": 50_000_000,
        "stdin_limit_bytes": 512 * 1024,
        "stdout_limit_bytes": 512 * 1024,
        "stderr_limit_bytes": 512 * 1024,
        "stdout_retained_tail_bytes": 512 * 1024,
        "stderr_retained_tail_bytes": 512 * 1024,
        "sampling": _sampling(),
        "reject_if_observed_wait4_cpu_ns_above": None,
        "reject_if_observed_wait4_normalized_maxrss_bytes_above": None,
    }
    values.update(overrides)
    return SupervisionLimits(**values)


def _invoke(
    code: str,
    *,
    input_bytes: bytes = b"",
    limits: SupervisionLimits | None = None,
    environment: Mapping[str, str] | None = None,
    cwd: Path = _ROOT,
) -> SupervisedProcessAttempt:
    return run_supervised_process(
        [_PYTHON, "-B", "-c", code],
        cwd=cwd,
        environment=dict(environment or _environment()),
        input_bytes=input_bytes,
        limits=limits or _limits(),
    )


def _request(
    code: str,
    *,
    input_bytes: bytes = b"",
    limits: SupervisionLimits | None = None,
    environment: Mapping[str, str] | None = None,
    cwd: Path = _ROOT,
) -> Any:
    return build_process_request_binding(
        [_PYTHON, "-B", "-c", code],
        cwd=cwd,
        environment=dict(environment or _environment()),
        input_bytes=input_bytes,
        limits=limits or _limits(),
    )


def _assert_all_parent_descriptors_closed(
    attempt: SupervisedProcessAttempt,
) -> None:
    assert attempt.stdin_parent_descriptor_closed is True
    assert attempt.stdout.parent_descriptor_closed is True
    assert attempt.stderr.parent_descriptor_closed is True


def _assert_complete_stream(stream: Any) -> None:
    assert stream.eof_observed is True
    assert stream.capture_complete is True
    assert stream.capture_disposition == "complete_eof"
    assert stream.parent_descriptor_closed is True


def _assert_pid_gone(pid: int, *, timeout: float = 1.0) -> None:
    deadline = time.monotonic() + timeout
    while True:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return
        if time.monotonic() >= deadline:
            pytest.fail(f"process {pid} remained observable")
        time.sleep(0.01)


def _reap_or_kill_external_pid(pid: int) -> None:
    """Best-effort cleanup for an intentionally escaped test grandchild."""

    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        return
    deadline = time.monotonic() + 1.0
    while time.monotonic() < deadline:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return
        time.sleep(0.01)


def test_public_v2_surface_is_closed_and_has_no_arbitrary_callbacks() -> None:
    signature = inspect.signature(run_supervised_process)
    assert "sampler" not in signature.parameters
    assert "monotonic_ns" not in signature.parameters
    assert PROCESS_ATTEMPT_SCHEMA_VERSION == "2.0.0"
    assert {
        "ProcessGroupSamplingPolicy",
        "SupervisedProcessAttempt",
        "SupervisionLimits",
        "build_process_request_binding",
        "load_supervised_process_attempt",
        "run_supervised_process",
        "validate_supervised_process_attempt",
    }.issubset(set(supervision.__all__))
    assert {
        "ProcessFailure",
        "ProcessGroupSample",
        "ProcessGroupSampler",
        "StreamEvidence",
        "sample_original_process_group",
    }.isdisjoint(set(supervision.__all__))
    with pytest.raises(TypeError):
        SupervisedProcessAttempt()


def test_success_receipt_projection_digest_and_round_trip_are_closed() -> None:
    code = "print('projection')"
    limits = _limits()
    attempt = _invoke(code, limits=limits)
    assert attempt.status == "succeeded"
    assert attempt.returncode == 0
    assert attempt.stdout.retained_tail == b"projection\n"
    assert attempt.stdin_fully_enqueued is True
    _assert_complete_stream(attempt.stdout)
    _assert_complete_stream(attempt.stderr)
    _assert_all_parent_descriptors_closed(attempt)

    payload = attempt.as_dict()
    payload_without_digest = copy.deepcopy(payload)
    digest = payload_without_digest.pop("attempt_digest")
    assert digest == _digest(payload_without_digest)
    assert payload["schema_version"] == PROCESS_ATTEMPT_SCHEMA_VERSION
    assert payload["attempt_kind"] == PROCESS_ATTEMPT_KIND
    assert payload["containment"]["mode"] == CONTAINMENT_MODE
    assert payload["authority_boundaries"]["authority_boundary"] == AUTHORITY_BOUNDARY
    assert payload["authority_boundaries"]["cryptographic_authenticity"] is False

    projection = attempt.invariant_projection()
    projection_without_digest = copy.deepcopy(projection)
    projection_digest = projection_without_digest.pop("projection_digest")
    assert projection_digest == _digest(projection_without_digest)

    expected = _request(code, limits=limits)
    assert validate_supervised_process_attempt(
        attempt,
        expected_request=expected,
    ) is None
    loaded = load_supervised_process_attempt(
        payload,
        expected_request=expected,
    )
    assert loaded.as_dict() == payload
    assert loaded.invariant_projection() == attempt.invariant_projection()


def test_exact_replacement_environment_and_request_binding_hide_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    executable = shutil.which("env")
    if executable is None:
        pytest.skip("env executable is unavailable")
    monkeypatch.setenv("PROCESS_SUPERVISION_PARENT_SECRET", "must-not-cross")
    exact_environment = {
        "LANG": "C",
        "LC_ALL": "C",
        "SUPERVISION_ONLY": "exact",
    }
    limits = _limits()
    argv = [str(Path(executable).resolve(strict=True))]
    attempt = run_supervised_process(
        argv,
        cwd=_ROOT,
        environment=exact_environment,
        input_bytes=b"",
        limits=limits,
    )
    assert attempt.status == "succeeded"
    observed = {
        line.decode("utf-8").split("=", 1)[0]: line.decode("utf-8").split(
            "=", 1
        )[1]
        for line in attempt.stdout.retained_tail.splitlines()
    }
    assert observed == exact_environment
    assert "PROCESS_SUPERVISION_PARENT_SECRET" not in observed
    serialized_request = attempt.as_dict()["request"]
    assert "must-not-cross" not in json.dumps(serialized_request)
    assert "exact" not in json.dumps(serialized_request)
    expected = build_process_request_binding(
        argv,
        cwd=_ROOT,
        environment=exact_environment,
        input_bytes=b"",
        limits=limits,
    )
    validate_supervised_process_attempt(attempt, expected_request=expected)


def test_simultaneous_large_stdin_stdout_and_stderr_are_complete() -> None:
    payload = bytes(range(256)) * 768
    attempt = _invoke(
        (
            "import sys; "
            "data=sys.stdin.buffer.read(); "
            "sys.stdout.buffer.write(data); sys.stdout.buffer.flush(); "
            "sys.stderr.buffer.write(data); sys.stderr.buffer.flush()"
        ),
        input_bytes=payload,
    )
    assert attempt.status == "succeeded"
    assert attempt.stdin_enqueued_bytes == len(payload)
    assert attempt.stdout.captured_bytes == len(payload)
    assert attempt.stderr.captured_bytes == len(payload)
    assert attempt.stdout.retained_tail == payload
    assert attempt.stderr.retained_tail == payload
    assert attempt.stdout.captured_sha256 == attempt.stderr.captured_sha256
    _assert_complete_stream(attempt.stdout)
    _assert_complete_stream(attempt.stderr)


def test_pipe_capacity_nonreader_has_one_total_deadline() -> None:
    limits = _limits(
        total_deadline_ns=750_000_000,
        cleanup_reserve_ns=300_000_000,
        termination_grace_ns=75_000_000,
        evidence_seal_reserve_ns=50_000_000,
    )
    started = time.monotonic_ns()
    attempt = _invoke(
        "import time; time.sleep(30)",
        input_bytes=b"x" * (256 * 1024),
        limits=limits,
    )
    observed_elapsed = time.monotonic_ns() - started
    assert attempt.status == "deadline_exhausted"
    assert attempt.primary_failure is not None
    assert attempt.primary_failure.reason_code == "execution_deadline_exhausted"
    assert attempt.stdin_enqueued_bytes < attempt.stdin_bytes
    assert attempt.leader_reaped is True
    assert attempt.evidence_sealed_monotonic_ns <= (
        attempt.total_deadline_monotonic_ns
    )
    assert attempt.deadline_overrun_ns == 0
    assert observed_elapsed < 1_500_000_000
    _assert_all_parent_descriptors_closed(attempt)


def test_input_limit_plus_one_is_a_closed_prelaunch_attempt() -> None:
    limits = _limits(stdin_limit_bytes=8)
    attempt = _invoke(
        "raise AssertionError('must not spawn')",
        input_bytes=b"x" * 9,
        limits=limits,
    )
    assert attempt.status == "input_exhausted"
    assert attempt.process_started is False
    assert attempt.pid is None
    assert attempt.returncode is None
    assert attempt.leader_reaped is False
    assert attempt.stdin_enqueued_bytes == 0
    assert attempt.primary_failure is not None
    assert attempt.primary_failure.reason_code == "input_limit_exceeded"
    assert attempt.stdout.capture_disposition == "not_started"
    assert attempt.stderr.capture_disposition == "not_started"
    assert attempt.stdout.eof_observed is False
    assert attempt.stderr.eof_observed is False
    _assert_all_parent_descriptors_closed(attempt)


@pytest.mark.parametrize(
    ("descriptor", "stream_name", "reason_code"),
    (
        (1, "stdout", "stdout_limit_exceeded"),
        (2, "stderr", "stderr_limit_exceeded"),
    ),
)
def test_output_limit_plus_one_fails_but_drains_to_eof(
    descriptor: int,
    stream_name: str,
    reason_code: str,
) -> None:
    limits = _limits(
        stdout_limit_bytes=64,
        stderr_limit_bytes=64,
        stdout_retained_tail_bytes=64,
        stderr_retained_tail_bytes=64,
    )
    attempt = _invoke(
        f"import os; os.write({descriptor}, b'x' * 65)",
        limits=limits,
    )
    evidence = getattr(attempt, stream_name)
    assert attempt.status == "resource_or_output_exhausted"
    assert attempt.primary_failure is not None
    assert attempt.primary_failure.reason_code == reason_code
    assert evidence.captured_bytes == 65
    assert evidence.ceiling_exceeded is True
    assert evidence.retained_tail == b"x" * 64
    _assert_complete_stream(evidence)
    assert attempt.leader_reaped is True


def test_same_group_pipe_holder_is_killed_and_capture_reaches_eof() -> None:
    limits = _limits(
        total_deadline_ns=800_000_000,
        cleanup_reserve_ns=300_000_000,
        termination_grace_ns=75_000_000,
        evidence_seal_reserve_ns=50_000_000,
    )
    attempt = _invoke(
        (
            "import subprocess, sys; "
            "child=subprocess.Popen([sys.executable,'-B','-c',"
            "'import time; time.sleep(30)']); "
            "print(child.pid, flush=True)"
        ),
        limits=limits,
    )
    assert attempt.status == "deadline_exhausted"
    assert attempt.stdout.retained_tail.strip().isdigit()
    assert attempt.leader_reaped is True
    _assert_complete_stream(attempt.stdout)
    _assert_complete_stream(attempt.stderr)
    _assert_all_parent_descriptors_closed(attempt)


def test_escaped_pipe_holder_is_bounded_and_capture_is_explicitly_incomplete() -> None:
    limits = _limits(
        total_deadline_ns=650_000_000,
        cleanup_reserve_ns=250_000_000,
        termination_grace_ns=50_000_000,
        evidence_seal_reserve_ns=50_000_000,
    )
    attempt = _invoke(
        (
            "import subprocess, sys; "
            "child=subprocess.Popen([sys.executable,'-B','-c',"
            "\"import os,time; os.setsid(); time.sleep(30)\"]); "
            "print(child.pid, flush=True)"
        ),
        limits=limits,
    )
    escaped_pid = int(attempt.stdout.retained_tail.strip().splitlines()[0])
    try:
        assert attempt.status != "succeeded"
        assert attempt.deadline_overrun_ns == 0
        assert attempt.stdout.eof_observed is False
        assert attempt.stdout.capture_complete is False
        assert attempt.stdout.capture_disposition == "forced_close_without_eof"
        assert attempt.containment["escaped_descendants_unobservable"] is True
    finally:
        _reap_or_kill_external_pid(escaped_pid)


def test_fast_exit_never_uses_original_pgid_after_wait4_reap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_wait4 = supervision.os.wait4
    real_killpg = supervision.os.killpg
    reaped_pids: set[int] = set()
    terminal_waits: list[int] = []
    group_operations: list[int] = []

    def observed_wait4(pid: int, options: int) -> Any:
        result = real_wait4(pid, options)
        if result[0] == pid:
            reaped_pids.add(pid)
            terminal_waits.append(pid)
        return result

    def guarded_killpg(process_group_id: int, requested_signal: int) -> None:
        assert process_group_id not in reaped_pids
        group_operations.append(process_group_id)
        real_killpg(process_group_id, requested_signal)

    monkeypatch.setattr(supervision.os, "wait4", observed_wait4)
    monkeypatch.setattr(supervision.os, "killpg", guarded_killpg)
    for _ in range(8):
        attempt = _invoke("pass")
        assert attempt.status == "succeeded"
        assert attempt.pid in terminal_waits
        assert attempt.last_original_group_operation_ns is not None
        assert attempt.leader_reaped_monotonic_ns is not None
        assert (
            attempt.last_original_group_operation_ns
            <= attempt.leader_reaped_monotonic_ns
        )
    assert group_operations


def test_fast_exit_with_real_required_sampling_never_samples_reused_pgid() -> None:
    sampling = _sampling(
        mode="posix_ps",
        required=True,
        interval_ns=100_000_000,
        attempt_timeout_ns=750_000_000,
        cleanup_reserve_ns=100_000_000,
        reject_if_observed_members_above=4,
        reject_if_observed_rss_bytes_above=512 * 1024 * 1024,
    )
    for _ in range(3):
        attempt = _invoke("pass", limits=_limits(sampling=sampling))
        assert attempt.status == "succeeded"
        assert attempt.sampler_processes_started >= 1
        assert (
            attempt.sampler_processes_started
            == attempt.sampler_processes_reaped
        )
        assert not any(
            row.reason_code == "process_group_sample_failed"
            for row in attempt.failure_events
        )


def test_sampler_overrun_is_killed_reaped_and_cannot_leak(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fake_ps = tmp_path / "fake-ps"
    fake_ps.write_text(
        "#!/bin/sh\n"
        "exec /bin/sleep 30\n",
        encoding="utf-8",
    )
    fake_ps.chmod(0o755)
    exact_fake_ps = str(fake_ps.resolve(strict=True))
    real_popen = supervision.subprocess.Popen
    sampler_pids: list[int] = []

    def observed_popen(*args: Any, **kwargs: Any) -> Any:
        process = real_popen(*args, **kwargs)
        raw_argv = args[0] if args else kwargs.get("args")
        if raw_argv and str(raw_argv[0]) == exact_fake_ps:
            sampler_pids.append(process.pid)
        return process

    monkeypatch.setattr(supervision.subprocess, "Popen", observed_popen)
    monkeypatch.setattr(
        supervision,
        "_PS_EXECUTABLE_CANDIDATES",
        (exact_fake_ps,),
    )
    sampling = _sampling(
        mode="posix_ps",
        required=True,
        interval_ns=10_000_000,
        attempt_timeout_ns=250_000_000,
        cleanup_reserve_ns=50_000_000,
    )
    limits = _limits(
        total_deadline_ns=900_000_000,
        cleanup_reserve_ns=350_000_000,
        termination_grace_ns=75_000_000,
        evidence_seal_reserve_ns=50_000_000,
        sampling=sampling,
    )
    attempt = _invoke("import time; time.sleep(30)", limits=limits)
    assert attempt.status != "succeeded"
    assert attempt.sampler_processes_started == 1
    assert attempt.sampler_processes_reaped == 1
    assert any(
        row.reason_code == "sampler_deadline_exhausted"
        for row in attempt.failure_events
    )
    assert len(sampler_pids) == 1
    with pytest.raises(ChildProcessError):
        os.waitpid(sampler_pids[0], os.WNOHANG)
    _assert_pid_gone(sampler_pids[0])
    _assert_all_parent_descriptors_closed(attempt)


def test_sampler_timeout_has_no_one_millisecond_floor() -> None:
    source = inspect.getsource(supervision)
    assert "max(0.001" not in source
    policy = _sampling(
        mode="posix_ps",
        required=True,
        attempt_timeout_ns=250_000,
        cleanup_reserve_ns=100_000,
    )
    assert policy.attempt_timeout_ns == 250_000


class _FaultingSelector:
    def __init__(self, stage: str) -> None:
        self._delegate = _REAL_SELECTOR_FACTORY()
        self._stage = stage
        self._raised = False

    def _maybe_raise(self, stage: str) -> None:
        if self._stage == stage and not self._raised:
            self._raised = True
            raise RuntimeError(f"injected selector {stage} failure")

    def register(self, *args: Any, **kwargs: Any) -> Any:
        if self._stage == "register" and not self._raised:
            self._maybe_raise("register")
        return self._delegate.register(*args, **kwargs)

    def unregister(self, *args: Any, **kwargs: Any) -> Any:
        result = self._delegate.unregister(*args, **kwargs)
        self._maybe_raise("unregister")
        return result

    def select(self, *args: Any, **kwargs: Any) -> Any:
        self._maybe_raise("select")
        return self._delegate.select(*args, **kwargs)

    def get_map(self) -> Any:
        return self._delegate.get_map()

    def close(self) -> None:
        self._delegate.close()
        self._maybe_raise("close")


@pytest.mark.parametrize("stage", ("register", "select", "unregister", "close"))
def test_selector_exceptions_are_total_and_never_escape(
    monkeypatch: pytest.MonkeyPatch,
    stage: str,
) -> None:
    real_factory = selectors.DefaultSelector
    monkeypatch.setattr(
        supervision.selectors,
        "DefaultSelector",
        lambda: _FaultingSelector(stage),
    )
    try:
        attempt = _invoke("print('selector')")
    finally:
        monkeypatch.setattr(
            supervision.selectors,
            "DefaultSelector",
            real_factory,
        )
    assert attempt.status != "succeeded"
    assert attempt.leader_reaped is True
    assert any(
        "selector" in row.reason_code
        or "selector" in row.message.lower()
        for row in (*attempt.failure_events, *attempt.cleanup_failures)
    )


def test_wait4_exception_is_recorded_and_retry_reaps_exact_child(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_wait4 = supervision.os.wait4
    injected = False

    def fail_once(pid: int, options: int) -> Any:
        nonlocal injected
        if not injected:
            injected = True
            raise OSError(errno.EIO, "injected wait4 failure")
        return real_wait4(pid, options)

    monkeypatch.setattr(supervision.os, "wait4", fail_once)
    attempt = _invoke("print('wait4')")
    assert injected is True
    assert attempt.status != "succeeded"
    assert attempt.leader_reaped is True
    assert any(
        row.reason_code == "direct_child_wait_failed"
        for row in attempt.failure_events
    )
    _assert_all_parent_descriptors_closed(attempt)


def test_group_cleanup_exception_is_recorded_without_losing_reap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_killpg = supervision.os.killpg
    injected = False

    def fail_once(process_group_id: int, requested_signal: int) -> None:
        nonlocal injected
        if not injected:
            injected = True
            raise RuntimeError("injected killpg failure")
        real_killpg(process_group_id, requested_signal)

    monkeypatch.setattr(supervision.os, "killpg", fail_once)
    attempt = _invoke("print('group-cleanup')")
    assert injected is True
    assert attempt.status != "succeeded"
    assert attempt.leader_reaped is True
    assert any(
        row.reason_code == "original_group_signal_failed"
        for row in (*attempt.failure_events, *attempt.cleanup_failures)
    )


def test_first_failure_is_preserved_when_launch_setup_also_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_getpgid = supervision.os.getpgid

    def mismatched_getpgid(pid: int) -> int:
        observed = real_getpgid(pid)
        return observed + 1

    class RegisterFaultSelector(_FaultingSelector):
        def __init__(self) -> None:
            super().__init__("register")

    monkeypatch.setattr(supervision.os, "getpgid", mismatched_getpgid)
    monkeypatch.setattr(
        supervision.selectors,
        "DefaultSelector",
        RegisterFaultSelector,
    )
    attempt = _invoke("import time; time.sleep(30)")
    assert attempt.status != "succeeded"
    assert attempt.primary_failure is not None
    assert (
        attempt.primary_failure.reason_code
        == "fresh_session_observation_mismatch"
    )
    assert len(attempt.failure_events) >= 2
    assert attempt.failure_events[0] == attempt.primary_failure
    assert any(
        "selector" in row.reason_code
        or "selector" in row.message.lower()
        for row in attempt.failure_events[1:]
    )
    assert tuple(row.ordinal for row in attempt.failure_events) == tuple(
        range(len(attempt.failure_events))
    )


@pytest.mark.parametrize(
    "host_exception",
    (KeyboardInterrupt("host interrupt"), SystemExit(17)),
)
def test_host_control_flow_is_reraised_only_after_cleanup(
    monkeypatch: pytest.MonkeyPatch,
    host_exception: BaseException,
) -> None:
    real_popen = supervision.subprocess.Popen
    real_selector = selectors.DefaultSelector
    processes: list[subprocess.Popen[bytes]] = []

    def observed_popen(*args: Any, **kwargs: Any) -> subprocess.Popen[bytes]:
        process = real_popen(*args, **kwargs)
        processes.append(process)
        return process

    class InterruptSelector:
        def __init__(self) -> None:
            self._delegate = real_selector()
            self._raised = False

        def register(self, *args: Any, **kwargs: Any) -> Any:
            return self._delegate.register(*args, **kwargs)

        def unregister(self, *args: Any, **kwargs: Any) -> Any:
            return self._delegate.unregister(*args, **kwargs)

        def get_map(self) -> Any:
            return self._delegate.get_map()

        def select(self, *args: Any, **kwargs: Any) -> Any:
            if not self._raised:
                self._raised = True
                raise host_exception
            return self._delegate.select(*args, **kwargs)

        def close(self) -> None:
            self._delegate.close()

    monkeypatch.setattr(supervision.subprocess, "Popen", observed_popen)
    monkeypatch.setattr(
        supervision.selectors,
        "DefaultSelector",
        InterruptSelector,
    )
    with pytest.raises(type(host_exception)) as raised:
        _invoke("import time; time.sleep(30)")
    if isinstance(host_exception, SystemExit):
        assert raised.value.code == 17
    else:
        assert str(raised.value) == "host interrupt"
    assert len(processes) == 1
    process = processes[0]
    assert process.stdin is not None and process.stdin.closed
    assert process.stdout is not None and process.stdout.closed
    assert process.stderr is not None and process.stderr.closed
    with pytest.raises(ChildProcessError):
        os.waitpid(process.pid, os.WNOHANG)


class _CloseFaultProxy:
    def __init__(self, delegate: Any) -> None:
        self._delegate = delegate

    @property
    def closed(self) -> bool:
        return False

    def fileno(self) -> int:
        return self._delegate.fileno()

    def close(self) -> None:
        raise OSError(errno.EIO, "injected stream close failure")


def test_close_failure_does_not_forge_parent_descriptor_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_popen = supervision.subprocess.Popen
    underlying_streams: list[Any] = []

    def close_fault_popen(*args: Any, **kwargs: Any) -> Any:
        process = real_popen(*args, **kwargs)
        assert process.stdout is not None
        underlying_streams.append(process.stdout)
        process.stdout = _CloseFaultProxy(process.stdout)
        return process

    monkeypatch.setattr(supervision.subprocess, "Popen", close_fault_popen)
    try:
        attempt = _invoke("print('close-fault')")
        assert attempt.status != "succeeded"
        assert attempt.stdout.parent_descriptor_closed is False
        assert any(
            row.reason_code == "stdout_close_failed"
            for row in (*attempt.failure_events, *attempt.cleanup_failures)
        )
    finally:
        for stream in underlying_streams:
            stream.close()


def test_evidence_seal_occurs_after_freeze_and_overrun_cannot_succeed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_freeze = supervision._StreamCapture.freeze
    freezes = 0

    def delayed_freeze(*args: Any, **kwargs: Any) -> Any:
        nonlocal freezes
        freezes += 1
        time.sleep(0.07)
        return real_freeze(*args, **kwargs)

    monkeypatch.setattr(supervision._StreamCapture, "freeze", delayed_freeze)
    limits = _limits(
        total_deadline_ns=120_000_000,
        cleanup_reserve_ns=70_000_000,
        termination_grace_ns=10_000_000,
        evidence_seal_reserve_ns=20_000_000,
    )
    attempt = _invoke("pass", limits=limits)
    assert freezes == 2
    assert attempt.status != "succeeded"
    assert attempt.evidence_sealed_monotonic_ns > (
        attempt.total_deadline_monotonic_ns
    )
    assert attempt.deadline_overrun_ns > 0
    assert any(
        row.reason_code == "total_deadline_overrun_detected"
        for row in attempt.failure_events
    )


@pytest.mark.parametrize(
    ("cleanup_ns", "grace_ns", "seal_ns"),
    (
        (100_000_000, 100_000_000, 10_000_000),
        (100_000_000, 90_000_000, 10_000_000),
        (100_000_000, 80_000_000, 20_000_000),
    ),
)
def test_cleanup_reserve_strictly_exceeds_grace_plus_seal(
    cleanup_ns: int,
    grace_ns: int,
    seal_ns: int,
) -> None:
    with pytest.raises(ValueError):
        _limits(
            cleanup_reserve_ns=cleanup_ns,
            termination_grace_ns=grace_ns,
            evidence_seal_reserve_ns=seal_ns,
        )


def test_wait4_resource_scope_and_host_maxrss_units_are_honest() -> None:
    attempt = _invoke("value = sum(range(10000))")
    resource_record = attempt.as_dict()["resource_observation"]
    assert resource_record["wait4_accounting_scope"] == (
        "target_pid_wait4_accounting_platform_defined_"
        "may_include_descendant_accrual"
    )
    assert resource_record["wait4_threshold_semantics"] == (
        "post_exit_acceptance_only_not_runtime_enforcement"
    )
    assert resource_record["wait4_ru_maxrss_raw"] >= 0
    if platform.system() == "Darwin":
        assert resource_record["wait4_ru_maxrss_unit"] == "bytes"
        assert (
            resource_record["wait4_ru_maxrss_normalized_bytes"]
            == resource_record["wait4_ru_maxrss_raw"]
        )
    elif platform.system() == "Linux":
        assert resource_record["wait4_ru_maxrss_unit"] == "kibibytes"
        assert (
            resource_record["wait4_ru_maxrss_normalized_bytes"]
            == resource_record["wait4_ru_maxrss_raw"] * 1024
        )


def test_unknown_maxrss_unit_is_never_guessed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(supervision.platform, "system", lambda: "UnknownPOSIX")
    attempt = _invoke("pass")
    resource_record = attempt.as_dict()["resource_observation"]
    assert resource_record["wait4_ru_maxrss_unit"] == "unknown"
    assert resource_record["wait4_ru_maxrss_normalized_bytes"] is None


def test_wait4_threshold_is_post_exit_rejection_not_hard_enforcement() -> None:
    limits = _limits(reject_if_observed_wait4_cpu_ns_above=1)
    attempt = _invoke("value = sum(range(100000))", limits=limits)
    assert attempt.status == "resource_or_output_exhausted"
    assert attempt.leader_reaped is True
    assert attempt.returncode == 0
    assert attempt.primary_failure is not None
    assert (
        attempt.primary_failure.reason_code
        == "observed_wait4_cpu_threshold_exceeded"
    )
    assert (
        attempt.as_dict()["resource_observation"]["wait4_threshold_semantics"]
        == "post_exit_acceptance_only_not_runtime_enforcement"
    )


def test_optional_sampling_failure_is_diagnostic_not_fatal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    false_executable = shutil.which("false")
    if false_executable is None:
        pytest.skip("the false executable is unavailable")
    monkeypatch.setattr(
        supervision,
        "_PS_EXECUTABLE_CANDIDATES",
        (str(Path(false_executable).resolve(strict=True)),),
    )
    sampling = _sampling(
        mode="posix_ps",
        required=False,
        interval_ns=100_000_000,
    )
    attempt = _invoke(
        "import time; time.sleep(0.08)",
        limits=_limits(sampling=sampling),
    )
    assert attempt.status == "succeeded"
    assert attempt.primary_failure is None
    assert any(
        row.reason_code == "sampler_exit_nonzero"
        for row in attempt.nonfatal_diagnostics
    )
    assert attempt.sampler_processes_started == attempt.sampler_processes_reaped


def test_cleanup_failure_cannot_coexist_with_success_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_selector = selectors.DefaultSelector

    class CloseFaultSelector(_FaultingSelector):
        def __init__(self) -> None:
            super().__init__("close")

    monkeypatch.setattr(
        supervision.selectors,
        "DefaultSelector",
        CloseFaultSelector,
    )
    try:
        attempt = _invoke("print('cleanup-fault')")
    finally:
        monkeypatch.setattr(
            supervision.selectors,
            "DefaultSelector",
            real_selector,
        )
    assert attempt.status != "succeeded"
    assert attempt.cleanup_failures
    assert attempt.primary_failure is not None


def test_repeated_runs_share_only_the_deterministic_projection() -> None:
    first = _invoke("import sys; sys.stdout.write('stable')")
    second = _invoke("import sys; sys.stdout.write('stable')")
    assert first.attempt_id != second.attempt_id
    assert first.pid != second.pid
    assert first.invariant_projection() == second.invariant_projection()


def test_loader_rejects_stale_digest() -> None:
    payload = _invoke("print('digest')").as_dict()
    payload["status"] = "operational_failure"
    with pytest.raises(ValueError):
        load_supervised_process_attempt(payload)


def _mutate_extra_key(payload: dict[str, Any]) -> None:
    payload["unexpected"] = True


def _mutate_false_eof_completeness(payload: dict[str, Any]) -> None:
    payload["streams"]["stdout"]["eof_observed"] = False
    payload["streams"]["stdout"]["capture_complete"] = True


def _mutate_ceiling_relation(payload: dict[str, Any]) -> None:
    payload["streams"]["stdout"]["ceiling_exceeded"] = True
    payload["streams"]["stdout"]["captured_bytes"] = 0


def _mutate_environment_order(payload: dict[str, Any]) -> None:
    payload["request"]["environment_bindings"].reverse()


def _mutate_pgid(payload: dict[str, Any]) -> None:
    payload["process"]["intended_process_group_id"] = payload["process"]["pid"] + 1


def _mutate_post_reap_group_operation(payload: dict[str, Any]) -> None:
    payload["timing"]["last_original_group_operation_ns"] = (
        payload["timing"]["leader_reaped_ns"] + 1
    )


def _mutate_sampling_counts(payload: dict[str, Any]) -> None:
    payload["sampling"]["sampler_processes_started"] = 1
    payload["sampling"]["sampler_processes_reaped"] = 2


def _mutate_wait4_evidence(payload: dict[str, Any]) -> None:
    payload["resource_observation"].pop("wait4_ru_maxrss_raw")


def _mutate_success_overrun(payload: dict[str, Any]) -> None:
    payload["timing"]["evidence_sealed_ns"] = (
        payload["timing"]["total_deadline_ns"] + 1
    )


def _mutate_noncanonical_base64(payload: dict[str, Any]) -> None:
    payload["streams"]["stdout"]["retained_tail_base64"] = "!!!"


def _mutate_missing_observed_session_identity(payload: dict[str, Any]) -> None:
    payload["process"]["observed_process_group_id"] = None
    payload["process"]["observed_session_id"] = None


def _mutate_missing_final_group_action(payload: dict[str, Any]) -> None:
    payload["process"]["termination_disposition"] = "running_anchored"
    payload["process"]["original_group_action_disposition"] = "running_anchored"
    payload["timing"]["last_original_group_operation_ns"] = None


def _mutate_negative_wait4_cpu(payload: dict[str, Any]) -> None:
    payload["resource_observation"]["wait4_accounted_user_cpu_ns"] = -1


def _mutate_reap_after_evidence_seal(payload: dict[str, Any]) -> None:
    payload["timing"]["leader_reaped_ns"] = (
        payload["timing"]["evidence_sealed_ns"] + 1
    )


def _mutate_closed_stream_without_close_attempt(payload: dict[str, Any]) -> None:
    payload["streams"]["stdout"]["parent_close_attempted"] = False


def _mutate_disabled_sampling_with_unsourced_sample(payload: dict[str, Any]) -> None:
    payload["sampling"]["group_sample_count"] = 1
    payload["sampling"]["peak_observed_sampled_original_group_members"] = 1
    payload["sampling"]["peak_observed_sampled_original_group_zombie_members"] = 0
    payload["sampling"]["peak_observed_sampled_original_group_rss_bytes"] = 4096


def _mutate_disabled_sampling_with_executable(payload: dict[str, Any]) -> None:
    payload["request"]["sampling_executable"] = _PYTHON


@pytest.mark.parametrize(
    "mutator",
    (
        _mutate_extra_key,
        _mutate_false_eof_completeness,
        _mutate_ceiling_relation,
        _mutate_environment_order,
        _mutate_pgid,
        _mutate_post_reap_group_operation,
        _mutate_sampling_counts,
        _mutate_wait4_evidence,
        _mutate_success_overrun,
        _mutate_noncanonical_base64,
        _mutate_missing_observed_session_identity,
        _mutate_missing_final_group_action,
        _mutate_negative_wait4_cpu,
        _mutate_reap_after_evidence_seal,
        _mutate_closed_stream_without_close_attempt,
        _mutate_disabled_sampling_with_unsourced_sample,
        _mutate_disabled_sampling_with_executable,
    ),
)
def test_loader_rejects_rehashed_relational_forgeries(
    mutator: Callable[[dict[str, Any]], None],
) -> None:
    payload = _invoke("print('validator')").as_dict()
    mutator(payload)
    _reseal_payload(payload)
    with pytest.raises(ValueError):
        load_supervised_process_attempt(payload)


def test_loader_rejects_resealed_success_over_stream_ceiling() -> None:
    limits = _limits(stdout_limit_bytes=2, stdout_retained_tail_bytes=2)
    payload = _invoke("import sys; sys.stdout.write('xy')", limits=limits).as_dict()
    assert payload["status"] == "succeeded"
    payload["streams"]["stdout"]["captured_bytes"] = 3
    payload["streams"]["stdout"]["ceiling_exceeded"] = True
    _reseal_payload(payload)
    with pytest.raises(ValueError):
        load_supervised_process_attempt(payload)


def test_loader_rejects_resealed_success_with_stdin_over_configured_limit() -> None:
    limits = _limits(stdin_limit_bytes=2)
    payload = _invoke("import sys; sys.stdin.buffer.read()", input_bytes=b"xy", limits=limits).as_dict()
    assert payload["status"] == "succeeded"
    payload["limits"]["stdin_limit_bytes"] = 1
    _reseal_payload(payload)
    with pytest.raises(ValueError):
        load_supervised_process_attempt(payload)


def test_loader_rejects_resealed_success_above_wait4_cpu_threshold() -> None:
    threshold_ns = 10**12
    limits = _limits(reject_if_observed_wait4_cpu_ns_above=threshold_ns)
    payload = _invoke("pass", limits=limits).as_dict()
    assert payload["status"] == "succeeded"
    payload["resource_observation"]["wait4_accounted_user_cpu_ns"] = threshold_ns + 1
    payload["resource_observation"]["wait4_accounted_system_cpu_ns"] = 0
    _reseal_payload(payload)
    with pytest.raises(ValueError):
        load_supervised_process_attempt(payload)


def test_loader_rejects_resealed_open_failure_variant() -> None:
    payload = _invoke("raise SystemExit(3)").as_dict()
    assert payload["status"] == "worker_failed"
    payload["failure_events"][0]["category"] = "operational"
    _reseal_payload(payload)
    with pytest.raises(ValueError):
        load_supervised_process_attempt(payload)


def test_loader_rejects_forged_success_with_cleanup_failure() -> None:
    real_selector = selectors.DefaultSelector

    class CloseFaultSelector(_FaultingSelector):
        def __init__(self) -> None:
            super().__init__("close")

    supervision.selectors.DefaultSelector = CloseFaultSelector
    try:
        payload = _invoke("print('failure-source')").as_dict()
    finally:
        supervision.selectors.DefaultSelector = real_selector
    assert payload["cleanup_failures"]
    payload["status"] = "succeeded"
    payload["invariant_projection"]["outcome"]["status"] = "succeeded"
    projection = payload["invariant_projection"]
    projection.pop("projection_digest", None)
    projection["projection_digest"] = _digest(projection)
    _rehash_payload(payload)
    with pytest.raises(ValueError):
        load_supervised_process_attempt(payload)


@pytest.mark.parametrize(
    "variant",
    ("argv", "cwd", "environment", "stdin", "limits"),
)
def test_expected_request_binding_rejects_every_identity_mismatch(
    tmp_path: Path,
    variant: str,
) -> None:
    code = "print('binding')"
    limits = _limits()
    environment = _environment()
    attempt = _invoke(code, limits=limits, environment=environment)
    argv = [_PYTHON, "-B", "-c", code]
    cwd = _ROOT
    input_bytes = b""
    if variant == "argv":
        argv[-1] = "print('different')"
    elif variant == "cwd":
        cwd = tmp_path.resolve()
    elif variant == "environment":
        environment = _environment(EXTRA="different")
    elif variant == "stdin":
        input_bytes = b"different"
    else:
        limits = _limits(
            stdout_limit_bytes=511 * 1024,
            stdout_retained_tail_bytes=511 * 1024,
        )
    mismatched = build_process_request_binding(
        argv,
        cwd=cwd,
        environment=environment,
        input_bytes=input_bytes,
        limits=limits,
    )
    with pytest.raises(ValueError):
        validate_supervised_process_attempt(
            attempt,
            expected_request=mismatched,
        )
    with pytest.raises(ValueError):
        load_supervised_process_attempt(
            attempt.as_dict(),
            expected_request=mismatched,
        )


def test_success_invariant_is_machine_checkable() -> None:
    attempt = _invoke("print('success-invariant')")
    assert attempt.status == "succeeded"
    assert attempt.process_started is True
    assert attempt.returncode == 0
    assert attempt.stdin_fully_enqueued is True
    assert attempt.stdout.capture_complete is True
    assert attempt.stderr.capture_complete is True
    assert attempt.leader_reaped is True
    assert attempt.sampler_processes_started == attempt.sampler_processes_reaped
    assert attempt.stdin_parent_descriptor_closed is True
    assert attempt.stdout.parent_descriptor_closed is True
    assert attempt.stderr.parent_descriptor_closed is True
    assert attempt.failure_events == ()
    assert attempt.cleanup_failures == ()
    assert (
        attempt.evidence_sealed_monotonic_ns
        <= attempt.total_deadline_monotonic_ns
    )
    validate_supervised_process_attempt(attempt)


def test_unobserved_fast_leader_cannot_hide_same_group_descendant_or_reap_first(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    descendant_pid_path = tmp_path / "same-group-descendant.pid"
    descendant_code = (
        "import os,time; "
        "\nfor descriptor in (0,1,2):"
        "\n try: os.close(descriptor)"
        "\n except OSError: pass"
        "\ntime.sleep(30)"
    )
    leader_code = (
        "import pathlib,subprocess,sys; "
        f"child=subprocess.Popen([sys.executable,'-B','-c',{descendant_code!r}]); "
        f"pathlib.Path({str(descendant_pid_path)!r}).write_text("
        "str(child.pid), encoding='utf-8')"
    )
    real_wait4 = supervision.os.wait4
    real_killpg = supervision.os.killpg
    reaped_pids: set[int] = set()
    operation_order: list[tuple[str, int]] = []

    def unavailable_session_observation(_pid: int) -> int:
        # Establish the same-group descendant before injecting lookup loss so
        # fail-closed launch cleanup, rather than fixture scheduling, is under
        # test.  The leader exits immediately after publishing this witness.
        publish_deadline = time.monotonic() + 2.0
        while not descendant_pid_path.is_file() and time.monotonic() < publish_deadline:
            time.sleep(0.001)
        raise ProcessLookupError(errno.ESRCH, "injected fast-leader lookup loss")

    def observed_wait4(pid: int, options: int) -> Any:
        result = real_wait4(pid, options)
        if result[0] == pid:
            reaped_pids.add(pid)
            operation_order.append(("wait4_terminal", pid))
        return result

    def guarded_killpg(process_group_id: int, requested_signal: int) -> None:
        assert process_group_id not in reaped_pids
        operation_order.append(("killpg", process_group_id))
        real_killpg(process_group_id, requested_signal)

    monkeypatch.setattr(supervision.os, "getpgid", unavailable_session_observation)
    monkeypatch.setattr(supervision.os, "getsid", unavailable_session_observation)
    monkeypatch.setattr(supervision.os, "wait4", observed_wait4)
    monkeypatch.setattr(supervision.os, "killpg", guarded_killpg)

    attempt = _invoke(leader_code)
    assert descendant_pid_path.is_file()
    descendant_pid = int(descendant_pid_path.read_text(encoding="utf-8"))
    try:
        _assert_pid_gone(descendant_pid)
        leader_group_operations = [
            index
            for index, row in enumerate(operation_order)
            if row == ("killpg", attempt.pid)
        ]
        leader_terminal_waits = [
            index
            for index, row in enumerate(operation_order)
            if row == ("wait4_terminal", attempt.pid)
        ]
        assert leader_group_operations
        assert len(leader_terminal_waits) == 1
        assert max(leader_group_operations) < leader_terminal_waits[0]
        assert attempt.observed_process_group_id is None
        assert attempt.observed_session_id is None
        assert attempt.leader_reaped is True
        assert attempt.status != "succeeded"
        assert any(
            row.reason_code == "session_observation_unavailable"
            for row in attempt.failure_events
        )
    finally:
        _reap_or_kill_external_pid(descendant_pid)


@pytest.mark.parametrize(
    ("fault_method", "reason_code"),
    (
        ("get_map", "selector_map_failed"),
        ("select", "selector_select_failed"),
    ),
)
def test_persistent_selector_fault_is_bounded_without_ledger_or_spin_explosion(
    monkeypatch: pytest.MonkeyPatch,
    fault_method: str,
    reason_code: str,
) -> None:
    calls = {"get_map": 0, "select": 0}

    class PersistentFaultSelector:
        def __init__(self) -> None:
            self._delegate = _REAL_SELECTOR_FACTORY()

        def register(self, *args: Any, **kwargs: Any) -> Any:
            return self._delegate.register(*args, **kwargs)

        def unregister(self, *args: Any, **kwargs: Any) -> Any:
            return self._delegate.unregister(*args, **kwargs)

        def get_map(self) -> Any:
            calls["get_map"] += 1
            if fault_method == "get_map":
                raise RuntimeError("persistent injected selector get_map failure")
            return self._delegate.get_map()

        def select(self, *args: Any, **kwargs: Any) -> Any:
            calls["select"] += 1
            if fault_method == "select":
                raise RuntimeError("persistent injected selector select failure")
            return self._delegate.select(*args, **kwargs)

        def close(self) -> None:
            self._delegate.close()

    monkeypatch.setattr(
        supervision.selectors,
        "DefaultSelector",
        PersistentFaultSelector,
    )
    limits = _limits(
        total_deadline_ns=600_000_000,
        cleanup_reserve_ns=250_000_000,
        termination_grace_ns=25_000_000,
        evidence_seal_reserve_ns=50_000_000,
    )
    started_ns = time.monotonic_ns()
    attempt = _invoke("import time; time.sleep(30)", limits=limits)
    wall_elapsed_ns = time.monotonic_ns() - started_ns
    assert attempt.status != "succeeded"
    assert attempt.leader_reaped is True
    assert any(
        row.reason_code == reason_code for row in attempt.failure_events
    )
    assert len(attempt.failure_events) <= 128
    assert len(attempt.cleanup_failures) <= 128
    assert len(attempt.nonfatal_diagnostics) <= 128
    assert calls[fault_method] <= 4
    assert wall_elapsed_ns < 1_200_000_000
    assert attempt.deadline_overrun_ns == 0
    _assert_all_parent_descriptors_closed(attempt)


def test_sampling_maximum_attempts_is_bound_serialized_and_strictly_loaded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    false_executable = shutil.which("false")
    if false_executable is None:
        pytest.skip("the false executable is unavailable")
    exact_false = str(Path(false_executable).resolve(strict=True))
    real_popen = supervision.subprocess.Popen
    sampler_pids: list[int] = []

    def observed_popen(*args: Any, **kwargs: Any) -> Any:
        process = real_popen(*args, **kwargs)
        raw_argv = args[0] if args else kwargs.get("args")
        if raw_argv and str(raw_argv[0]) == exact_false:
            sampler_pids.append(process.pid)
        return process

    monkeypatch.setattr(supervision.subprocess, "Popen", observed_popen)
    monkeypatch.setattr(
        supervision,
        "_PS_EXECUTABLE_CANDIDATES",
        (exact_false,),
    )
    sampling = _sampling(
        mode="posix_ps",
        required=False,
        interval_ns=1_000_000,
        attempt_timeout_ns=100_000_000,
        cleanup_reserve_ns=20_000_000,
        maximum_attempts=3,
    )
    limits = _limits(sampling=sampling)
    code = "import time; time.sleep(0.15)"
    attempt = _invoke(code, limits=limits)
    assert attempt.status == "succeeded"
    assert attempt.sampler_processes_started == 3
    assert attempt.sampler_processes_reaped == 3
    assert len(sampler_pids) == 3
    assert any(
        row.reason_code == "sampler_exit_nonzero"
        for row in attempt.nonfatal_diagnostics
    )
    for sampler_pid in sampler_pids:
        with pytest.raises(ChildProcessError):
            os.waitpid(sampler_pid, os.WNOHANG)

    payload = attempt.as_dict()
    assert payload["limits"]["sampling"]["maximum_attempts"] == 3
    assert payload["sampling"]["policy"]["maximum_attempts"] == 3
    expected = _request(code, limits=limits)
    loaded = load_supervised_process_attempt(
        payload,
        expected_request=expected,
    )
    assert loaded.limits.sampling.maximum_attempts == 3
    validate_supervised_process_attempt(loaded, expected_request=expected)

    missing_maximum = sampling.as_dict()
    missing_maximum.pop("maximum_attempts")
    with pytest.raises(ValueError):
        ProcessGroupSamplingPolicy.from_mapping(missing_maximum)
    invalid_maximum = sampling.as_dict()
    invalid_maximum["maximum_attempts"] = 0
    with pytest.raises(ValueError):
        ProcessGroupSamplingPolicy.from_mapping(invalid_maximum)
    inconsistent_payload = copy.deepcopy(payload)
    inconsistent_payload["sampling"]["policy"]["maximum_attempts"] = 4
    _rehash_payload(inconsistent_payload)
    with pytest.raises(ValueError):
        load_supervised_process_attempt(inconsistent_payload)


@pytest.mark.parametrize(
    "invalid_field",
    (
        "tuple_argv",
        "nul_argv",
        "nul_environment_name",
        "noncanonical_cwd",
        "missing_cwd",
        "invalid_executable",
    ),
)
def test_request_binding_from_mapping_rejects_noncanonical_external_values(
    tmp_path: Path,
    invalid_field: str,
) -> None:
    raw = _request("pass").as_dict()
    if invalid_field == "tuple_argv":
        raw["argv"] = tuple(raw["argv"])
    elif invalid_field == "nul_argv":
        raw["argv"][0] = raw["argv"][0] + "\x00"
    elif invalid_field == "nul_environment_name":
        raw["environment_bindings"][0]["name"] += "\x00"
    elif invalid_field == "noncanonical_cwd":
        linked_cwd = tmp_path / "cwd-link"
        linked_cwd.symlink_to(_ROOT, target_is_directory=True)
        raw["cwd"] = str(linked_cwd)
    elif invalid_field == "missing_cwd":
        raw["cwd"] = str((tmp_path / "missing-cwd").resolve())
    else:
        raw["sampling_executable"] = str(
            (tmp_path / "missing-sampler-executable").resolve()
        )
    with pytest.raises(ValueError):
        ProcessRequestBinding.from_mapping(raw)


def test_sampler_popen_returncode_matches_exact_wait4_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    false_executable = shutil.which("false")
    if false_executable is None:
        pytest.skip("the false executable is unavailable")
    exact_false = str(Path(false_executable).resolve(strict=True))
    real_popen = supervision.subprocess.Popen
    real_wait4 = supervision.os.wait4
    sampler_processes: list[subprocess.Popen[bytes]] = []
    terminal_wait4_returncodes: dict[int, int] = {}

    def observed_popen(*args: Any, **kwargs: Any) -> Any:
        process = real_popen(*args, **kwargs)
        raw_argv = args[0] if args else kwargs.get("args")
        if raw_argv and str(raw_argv[0]) == exact_false:
            sampler_processes.append(process)
        return process

    def observed_wait4(pid: int, options: int) -> Any:
        result = real_wait4(pid, options)
        if result[0] == pid:
            terminal_wait4_returncodes[pid] = os.waitstatus_to_exitcode(result[1])
        return result

    monkeypatch.setattr(supervision.subprocess, "Popen", observed_popen)
    monkeypatch.setattr(supervision.os, "wait4", observed_wait4)
    monkeypatch.setattr(
        supervision,
        "_PS_EXECUTABLE_CANDIDATES",
        (exact_false,),
    )
    sampling = _sampling(
        mode="posix_ps",
        required=False,
        interval_ns=100_000_000,
        attempt_timeout_ns=100_000_000,
        cleanup_reserve_ns=20_000_000,
        maximum_attempts=1,
    )
    attempt = _invoke(
        "import time; time.sleep(0.08)",
        limits=_limits(sampling=sampling),
    )
    assert attempt.status == "succeeded"
    assert attempt.sampler_processes_started == 1
    assert attempt.sampler_processes_reaped == 1
    assert len(sampler_processes) == 1
    sampler = sampler_processes[0]
    assert sampler.pid in terminal_wait4_returncodes
    assert sampler.returncode == terminal_wait4_returncodes[sampler.pid] == 1
    with pytest.raises(ChildProcessError):
        os.waitpid(sampler.pid, os.WNOHANG)


def test_pending_keyboard_interrupt_survives_cleanup_base_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    primary_interrupt = KeyboardInterrupt("primary host interrupt")
    cleanup_collision = SystemExit(91)
    real_popen = supervision.subprocess.Popen
    worker_processes: list[subprocess.Popen[bytes]] = []
    selector_instances: list[Any] = []

    def observed_popen(*args: Any, **kwargs: Any) -> Any:
        process = real_popen(*args, **kwargs)
        worker_processes.append(process)
        return process

    class HostCollisionSelector:
        def __init__(self) -> None:
            self._delegate = _REAL_SELECTOR_FACTORY()
            self.get_map_calls = 0
            self.select_calls = 0
            selector_instances.append(self)

        def register(self, *args: Any, **kwargs: Any) -> Any:
            return self._delegate.register(*args, **kwargs)

        def unregister(self, *args: Any, **kwargs: Any) -> Any:
            return self._delegate.unregister(*args, **kwargs)

        def get_map(self) -> Any:
            self.get_map_calls += 1
            if self.get_map_calls >= 2:
                raise cleanup_collision
            return self._delegate.get_map()

        def select(self, *args: Any, **kwargs: Any) -> Any:
            self.select_calls += 1
            if self.select_calls == 1:
                raise primary_interrupt
            return self._delegate.select(*args, **kwargs)

        def close(self) -> None:
            self._delegate.close()

    monkeypatch.setattr(supervision.subprocess, "Popen", observed_popen)
    monkeypatch.setattr(
        supervision.selectors,
        "DefaultSelector",
        HostCollisionSelector,
    )
    with pytest.raises(KeyboardInterrupt) as raised:
        _invoke(
            "import time; time.sleep(30)",
            limits=_limits(
                total_deadline_ns=900_000_000,
                cleanup_reserve_ns=350_000_000,
                termination_grace_ns=50_000_000,
                evidence_seal_reserve_ns=50_000_000,
            ),
        )
    assert raised.value is primary_interrupt
    assert len(selector_instances) == 1
    assert selector_instances[0].get_map_calls >= 2
    assert len(worker_processes) == 1
    worker = worker_processes[0]
    assert worker.stdin is not None and worker.stdin.closed
    assert worker.stdout is not None and worker.stdout.closed
    assert worker.stderr is not None and worker.stderr.closed
    with pytest.raises(ChildProcessError):
        os.waitpid(worker.pid, os.WNOHANG)
