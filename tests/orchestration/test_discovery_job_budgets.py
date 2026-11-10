# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Regression tests for hard discovery resource and path governance."""

from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import pytest

import agentic.process_supervision as process_supervision
from agentic.discovery.budgets import (
    BudgetExceeded,
    PortfolioBudget,
    ResourceBudget,
    ResourceGovernor,
    branch_run_directory,
    contained_path,
    partial_result_partition,
    selective_retry_schedule,
    validate_job_id,
)
from agentic.discovery.contracts import validate_payload


def _budget(**overrides: object) -> dict:
    raw = {
        "schema_version": 1,
        "budget_id": "portfolio-budget",
        "wall_time_seconds": 1.0,
        "grace_period_seconds": 0.1,
        "cpu_seconds": 2.0,
        "memory_bytes": 512 * 1024 * 1024,
        "disk_bytes": 20 * 1024 * 1024,
        "network_bytes": 1000,
        "token_count": 1000,
        "request_count": 10,
        "cost_usd": 10.0,
        "portfolio_reserve_fraction": 0.2,
        "per_branch": {},
    }
    raw.update(overrides)
    return raw


def _branch_budget(**overrides: object) -> dict:
    raw = {
        "wall_time_seconds": 0.4,
        "cpu_seconds": 0.5,
        "memory_bytes": 128 * 1024 * 1024,
        "disk_bytes": 1024,
        "network_bytes": 100,
        "token_count": 100,
        "request_count": 1,
        "cost_usd": 1.0,
    }
    raw.update(overrides)
    return raw


def test_resource_budget_schema_is_real_json_schema() -> None:
    validate_payload(_budget(), "discovery_resource_budget.schema.json")


@pytest.mark.parametrize("malicious", ["../escape", "a/b", "a\\b", ".hidden", "a..b", "", "x\x00y"])
def test_job_ids_cannot_escape_run_directory(malicious: str, tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        validate_job_id(malicious)
    with pytest.raises(ValueError):
        branch_run_directory(tmp_path, malicious)


def test_contained_path_rejects_traversal(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="escapes"):
        contained_path(tmp_path, "..", "outside")


def test_absolute_deadline_terminates_entire_process_group_within_grace(tmp_path: Path) -> None:
    budget = ResourceBudget.from_mapping(
        {
            # Below the declared short-job sampling floor, so this lane tests
            # deadline-triggered group cleanup rather than earlier positive
            # descendant detection.
            **_budget(wall_time_seconds=0.08, grace_period_seconds=0.05),
            "per_branch": {},
        }
    )
    governor = ResourceGovernor(budget, run_directory=tmp_path)
    code = "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); time.sleep(30)"
    started = time.monotonic()
    result = governor.run_process([sys.executable, "-c", code], cwd=tmp_path)
    elapsed = time.monotonic() - started
    assert result["status"] == "deadline_exhausted"
    assert result["termination"] in {"terminated", "killed"}
    assert elapsed < 1.0


def test_terminal_parent_cannot_leave_inherited_pipe_or_descendant_alive(
    tmp_path: Path,
) -> None:
    budget = ResourceBudget.from_mapping(
        {
            **_budget(wall_time_seconds=0.4, grace_period_seconds=0.05),
            "per_branch": {},
        }
    )
    governor = ResourceGovernor(
        budget,
        run_directory=tmp_path,
        capture_limit_bytes=256,
        disk_sample_interval_seconds=0.01,
    )
    code = (
        "import subprocess,sys; "
        "subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); "
        "print('leader-exited', flush=True)"
    )
    started = time.monotonic()
    result = governor.run_process([sys.executable, "-c", code], cwd=tmp_path)
    assert time.monotonic() - started < 1.0
    assert result["status"] == "worker_failed"
    assert result["descendant_leak_detected"] is True
    assert result["termination"] in {"terminated", "killed"}
    assert result["stdout_drain_incomplete"] is False
    assert "leader-exited" in result["stdout"]


def test_noisy_worker_output_is_drained_but_retained_tail_is_bounded(
    tmp_path: Path,
) -> None:
    governor = ResourceGovernor(
        ResourceBudget.from_mapping(_budget(wall_time_seconds=2.0)),
        run_directory=tmp_path,
        capture_limit_bytes=128,
    )
    code = "import sys; sys.stdout.write('o'*200000); sys.stderr.write('e'*200000)"
    result = governor.run_process([sys.executable, "-c", code], cwd=tmp_path)
    assert result["status"] == "succeeded"
    assert result["stdout_bytes"] == result["stderr_bytes"] == 200000
    assert result["stdout_truncated"] is result["stderr_truncated"] is True
    assert len(result["stdout"].encode()) <= 128
    assert len(result["stderr"].encode()) <= 128


def test_five_parallel_governors_retain_required_sampler_headroom(
    tmp_path: Path,
) -> None:
    """Matched arms must not inherit the retired fixed 100 ms ps deadline."""

    def invoke(ordinal: int) -> dict:
        run_directory = tmp_path / f"parallel-arm-{ordinal}"
        run_directory.mkdir()
        governor = ResourceGovernor(
            ResourceBudget.from_mapping(
                _budget(
                    budget_id=f"parallel-arm-budget-{ordinal}",
                    wall_time_seconds=30.0,
                    cpu_seconds=30.0,
                )
            ),
            run_directory=run_directory,
        )
        return governor.run_process(
            [sys.executable, "-c", "import time; time.sleep(0.3)"],
            cwd=run_directory,
        )

    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(invoke, range(5)))

    assert all(result["status"] == "succeeded" for result in results)
    assert len({result["pid"] for result in results}) == 5
    assert all(
        result["supervision_attempt"]["limits"]["sampling"][
            "attempt_timeout_ns"
        ]
        >= 2_000_000_000
        for result in results
    )
    assert all(
        result["supervision_attempt"]["limits"]["sampling"]["required"]
        is True
        for result in results
    )


def _install_fake_ps(tmp_path: Path, body: str) -> str:
    """Install one canonical executable used only as the fixed sampler seam."""

    fake_ps = tmp_path / "fake-ps"
    fake_ps.write_text("#!/bin/sh\n" + body, encoding="utf-8")
    fake_ps.chmod(0o755)
    return str(fake_ps.resolve(strict=True))


@pytest.mark.skipif(
    os.name != "posix" or not hasattr(os, "wait4"),
    reason="sampler supervision requires POSIX wait4",
)
def test_slow_required_sampler_finishes_inside_fractional_headroom(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A slow but bounded ps scan remains required and fully reaped."""

    real_ps = shutil.which("ps")
    if real_ps is None:
        pytest.skip("the fixed ps sampler is unavailable")
    fake_ps = _install_fake_ps(
        tmp_path,
        f"/bin/sleep 0.05\nexec {Path(real_ps).resolve(strict=True)} \"$@\"\n",
    )
    monkeypatch.setattr(
        process_supervision,
        "_PS_EXECUTABLE_CANDIDATES",
        (fake_ps,),
    )
    governor = ResourceGovernor(
        ResourceBudget.from_mapping(
            _budget(wall_time_seconds=6.0, cpu_seconds=6.0)
        ),
        run_directory=tmp_path,
    )
    result = governor.run_process(
        [sys.executable, "-c", "import time; time.sleep(0.2)"],
        cwd=tmp_path,
    )
    attempt = result["supervision_attempt"]

    assert result["status"] == "succeeded"
    assert attempt["limits"]["sampling"]["required"] is True
    assert attempt["sampling"]["group_sample_count"] >= 1
    assert (
        attempt["sampling"]["sampler_processes_started"]
        == attempt["sampling"]["sampler_processes_reaped"]
    )
    assert attempt["timing"]["deadline_overrun_ns"] == 0


@pytest.mark.skipif(
    os.name != "posix" or not hasattr(os, "wait4"),
    reason="sampler supervision requires POSIX wait4",
)
def test_hung_sampler_is_killed_reaped_and_bounded_by_absolute_deadline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A stuck ps sidecar cannot consume the worker deadline or leave a child."""

    fake_ps = _install_fake_ps(tmp_path, "exec /bin/sleep 30\n")
    real_popen = process_supervision.subprocess.Popen
    sampler_pids: list[int] = []

    def observed_popen(*args: Any, **kwargs: Any) -> Any:
        process = real_popen(*args, **kwargs)
        raw_argv = args[0] if args else kwargs.get("args")
        if raw_argv and str(raw_argv[0]) == fake_ps:
            sampler_pids.append(process.pid)
        return process

    monkeypatch.setattr(process_supervision.subprocess, "Popen", observed_popen)
    monkeypatch.setattr(
        process_supervision,
        "_PS_EXECUTABLE_CANDIDATES",
        (fake_ps,),
    )
    absolute_deadline = dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=1.0)
    governor = ResourceGovernor(
        ResourceBudget.from_mapping(
            _budget(
                wall_time_seconds=5.0,
                grace_period_seconds=0.05,
                cpu_seconds=5.0,
                absolute_deadline=absolute_deadline.isoformat(),
            )
        ),
        run_directory=tmp_path,
    )
    started = time.monotonic()
    result = governor.run_process(
        [sys.executable, "-c", "import time; time.sleep(30)"],
        cwd=tmp_path,
    )
    elapsed = time.monotonic() - started
    attempt = result["supervision_attempt"]
    reasons = {
        row["reason_code"] for row in attempt["failure_events"]
    }

    assert result["status"] == "deadline_exhausted"
    assert "sampler_deadline_exhausted" in reasons
    assert attempt["sampling"]["sampler_processes_started"] == 1
    assert attempt["sampling"]["sampler_processes_reaped"] == 1
    assert attempt["timing"]["deadline_overrun_ns"] == 0
    assert elapsed < 1.0
    assert len(sampler_pids) == 1
    with pytest.raises(ChildProcessError):
        os.waitpid(sampler_pids[0], os.WNOHANG)


@pytest.mark.skipif(
    os.name != "posix" or not hasattr(os, "wait4"),
    reason="sampler supervision requires POSIX wait4",
)
def test_short_absolute_budget_disables_sampler_without_skipping_cleanup(
    tmp_path: Path,
) -> None:
    """Sub-100 ms execution authority never starts an underfunded ps sidecar."""

    absolute_deadline = dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=0.09)
    governor = ResourceGovernor(
        ResourceBudget.from_mapping(
            _budget(
                wall_time_seconds=5.0,
                grace_period_seconds=0.02,
                cpu_seconds=5.0,
                absolute_deadline=absolute_deadline.isoformat(),
            )
        ),
        run_directory=tmp_path,
    )
    started = time.monotonic()
    result = governor.run_process(
        [sys.executable, "-c", "import time; time.sleep(30)"],
        cwd=tmp_path,
    )
    elapsed = time.monotonic() - started
    attempt = result["supervision_attempt"]

    assert result["status"] == "deadline_exhausted"
    assert attempt["limits"]["sampling"]["mode"] == "disabled"
    assert attempt["sampling"]["sampler_processes_started"] == 0
    assert attempt["sampling"]["sampler_processes_reaped"] == 0
    assert attempt["process"]["leader_reaped"] is True
    assert attempt["timing"]["deadline_overrun_ns"] == 0
    assert elapsed < 0.6


def test_disk_growth_and_aggregate_local_dimensions_are_hard_limits(
    tmp_path: Path,
) -> None:
    governor = ResourceGovernor(
        ResourceBudget.from_mapping(_budget(wall_time_seconds=2.0, disk_bytes=1024)),
        run_directory=tmp_path,
        disk_sample_interval_seconds=0.01,
    )
    result = governor.run_process(
        [sys.executable, "-c", "open('large.bin','wb').write(b'x'*1000000)"],
        cwd=tmp_path,
    )
    # Python converts the per-file RLIMIT_FSIZE event into an ordinary OSError
    # and exits nonzero.  Without a kernel signal or an aggregate snapshot over
    # the limit, the projection must not guess that this was disk exhaustion.
    assert result["status"] == "worker_failed"
    assert result["resource_measurement"]["disk_bytes"]["enforced"] is True
    assert (
        result["resource_measurement"]["disk_bytes"]["kernel_limit"]
        == "inherited_per_file_rlimit_fsize"
    )

    cpu_governor = ResourceGovernor(
        ResourceBudget.from_mapping(_budget(cpu_seconds=0.1)), run_directory=tmp_path
    )
    cpu_governor.usage.cpu_seconds = 0.1001
    with pytest.raises(BudgetExceeded, match="cpu_seconds") as cpu_error:
        cpu_governor.checkpoint()
    assert cpu_error.value.status == "cpu_exhausted"

    memory_governor = ResourceGovernor(
        ResourceBudget.from_mapping(_budget(memory_bytes=1024)), run_directory=tmp_path
    )
    memory_governor.usage.peak_memory_bytes = 1025
    with pytest.raises(BudgetExceeded, match="peak_memory_bytes") as memory_error:
        memory_governor.checkpoint()
    assert memory_error.value.status == "out_of_memory"


def test_unobservable_remote_dimensions_are_labelled_until_adapter_reports(
    tmp_path: Path,
) -> None:
    governor = ResourceGovernor(ResourceBudget.from_mapping(_budget()), run_directory=tmp_path)
    assert governor.measurement_boundaries()["token_count"] == {
        "status": "unavailable",
        "enforced": False,
        "reason": "generic subprocess governance cannot observe this dimension",
    }
    governor.account(token_count=1)
    assert governor.measurement_boundaries()["token_count"]["status"] == "externally_reported"


def test_deadline_is_exported_to_subprocess(tmp_path: Path) -> None:
    governor = ResourceGovernor(ResourceBudget.from_mapping(_budget()), run_directory=tmp_path)
    result = governor.run_process([sys.executable, "-c", "import os; print(os.environ['ABDUCER_ABSOLUTE_DEADLINE'])"], cwd=tmp_path)
    assert result["status"] == "succeeded"
    assert "+00:00" in result["stdout"]


def test_spend_tokens_requests_and_network_are_hard_limits(tmp_path: Path) -> None:
    dimensions = [
        ({"cost_usd": 10.01}, "spend_exhausted"),
        ({"token_count": 1001}, "token_exhausted"),
        ({"request_count": 11}, "request_exhausted"),
        ({"network_bytes": 1001}, "network_exhausted"),
    ]
    for increment, expected in dimensions:
        governor = ResourceGovernor(ResourceBudget.from_mapping(_budget()), run_directory=tmp_path)
        with pytest.raises(BudgetExceeded) as raised:
            governor.account(**increment)
        assert raised.value.status == expected


def test_report_builder_failure_is_not_success(tmp_path: Path) -> None:
    governor = ResourceGovernor(ResourceBudget.from_mapping(_budget()), run_directory=tmp_path)
    result = governor.run_process([sys.executable, "-c", "raise SystemExit(3)"], cwd=tmp_path, role="report_builder")
    assert result["status"] == "report_failed"


def test_portfolio_protects_reserve_and_independent_branch_budgets(tmp_path: Path) -> None:
    raw = _budget(per_branch={"branch-a": _branch_budget(), "branch-b": _branch_budget()})
    portfolio = PortfolioBudget(raw, tmp_path)
    assert portfolio.governor_for("branch-a") is not portfolio.governor_for("branch-b")
    oversubscribed = _budget(per_branch={"branch-a": _branch_budget(cost_usd=5.0), "branch-b": _branch_budget(cost_usd=4.0)})
    with pytest.raises(ValueError, match="reserve"):
        PortfolioBudget(oversubscribed, tmp_path)


def test_partial_success_is_retained_and_retry_is_selective() -> None:
    results = [
        {"branch_id": "a", "status": "succeeded", "validated": True, "literature_current": True, "artifact": "a.json"},
        {"branch_id": "b", "status": "worker_failed", "validated": False, "literature_current": True},
        {"branch_id": "c", "status": "succeeded", "validated": True, "literature_current": False},
    ]
    partition = partial_result_partition(results)
    assert [row["branch_id"] for row in partition["retained_successes"]] == ["a"]
    assert {row["branch_id"] for row in partition["retry_schedule"]} == {"b", "c"}
    retry = selective_retry_schedule(results, dependency_invalidations={"b": ["a"]})
    assert {row["branch_id"] for row in retry} == {"a", "b", "c"}
    assert next(row for row in retry if row["branch_id"] == "a")["reason"] == "dependency_invalidated:b"
