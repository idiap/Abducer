#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Run a bounded discovery job under one absolute resource deadline.

The job wrapper governs process groups rather than trusting child timeouts.  It
also keeps worker, deadline, and report-builder failures distinct, and treats
elapsed time purely as resource usage.  Research validity is decided inside the
semantic reducer, never by filling a requested duration.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from agentic.discovery.budgets import (
    BudgetExceeded,
    ResourceBudget,
    ResourceGovernor,
    contained_path,
    validate_job_id,
)
from agentic.discovery.contracts import ContractError, validate_identifier
from agentic.discovery.theory_gate import (
    DEFAULT_CANONICAL_THEORY_STATE_ROOT,
    verify_canonical_theory_cycle,
)
from agentic_common import ROOT, rel, utc_now, write_json
from discovery_marathon_common import load_run_state
from run_discovery_marathon import report_rebuild_commands


class JobConfigurationError(ValueError):
    """Raised before any job artifact is written for an unsafe binding."""


@dataclass(frozen=True)
class ResearchJobBinding:
    """Exact canonical authority forwarded unchanged to the worker."""

    target_id: str
    run_id: str
    canonical_theory_cycle: str
    canonical_theory_state_root: str
    authorization_basis_digest: str
    source_present_decision_digest: str
    schedule_id: str
    canonical_cycle_id: str
    canonical_commit_id: str


def resolve_research_binding(args: argparse.Namespace) -> ResearchJobBinding:
    """Replay the canonical gate before creating logs or launching a worker."""

    try:
        target_id = validate_identifier(str(args.target or ""), "target")
        run_id = validate_identifier(str(args.run_id or ""), "run_id")
    except ContractError as exc:
        raise JobConfigurationError(str(exc)) from exc
    cycle_path = Path(args.canonical_theory_cycle).resolve()
    state_root = Path(args.canonical_theory_state_root).resolve()
    _, run_state = load_run_state(run_id)
    if not run_state:
        raise JobConfigurationError(f"run does not exist: {run_id}")
    if run_state.get("target_id") != target_id or run_state.get("run_id") != run_id:
        raise JobConfigurationError("run state target/run identity mismatch")
    try:
        authorization = verify_canonical_theory_cycle(
            cycle_path,
            target_id=target_id,
            run_id=run_id,
            state_root=state_root,
            previous_lineage=run_state.get("canonical_theory_lineage"),
        )
    except ContractError as exc:
        raise JobConfigurationError(str(exc)) from exc
    return ResearchJobBinding(
        target_id=target_id,
        run_id=run_id,
        canonical_theory_cycle=str(cycle_path),
        canonical_theory_state_root=str(state_root),
        authorization_basis_digest=str(authorization["authorization_basis_digest"]),
        source_present_decision_digest=str(
            authorization["present_investment_decision_digest"]
        ),
        schedule_id=str(authorization["schedule_id"]),
        canonical_cycle_id=str(authorization["cycle_id"]),
        canonical_commit_id=str(authorization["commit_id"]),
    )


def build_cycle_command(
    args: argparse.Namespace, binding: ResearchJobBinding
) -> list[str]:
    """Build one fully bound research invocation; no active pointer is consulted."""

    command = [
        sys.executable,
        "agentic/scripts/run_discovery_marathon.py",
        "--resume",
        "--run-id",
        binding.run_id,
        "--target",
        binding.target_id,
        "--canonical-theory-cycle",
        binding.canonical_theory_cycle,
        "--canonical-theory-state-root",
        binding.canonical_theory_state_root,
        "--canonical-authorization-basis-digest",
        binding.authorization_basis_digest,
        "--canonical-source-present-decision-digest",
        binding.source_present_decision_digest,
        "--canonical-schedule-id",
        binding.schedule_id,
        "--max-cycles",
        "1",
        "--max-active-branches",
        str(args.max_active_branches),
        "--execution-mode",
        "research",
        "--branch-engine",
        args.branch_engine,
        "--min-cycle-seconds",
        str(args.min_cycle_seconds),
        "--skip-report-rebuild",
    ]
    if args.api_key_config:
        command.extend(["--api-key-config", args.api_key_config])
    if args.parallel_branches:
        command.append("--parallel-branches")
    if args.api_max_workers is not None:
        command.extend(["--api-max-workers", str(args.api_max_workers)])
    if args.api_request_spacing_seconds is not None:
        command.extend(
            ["--api-request-spacing-seconds", str(args.api_request_spacing_seconds)]
        )
    return command


def validate_remote_budget_contract(args: argparse.Namespace) -> None:
    """Reject numeric promises the generic subprocess adapter cannot measure."""

    requested = {
        "network_bytes": args.network_bytes,
        "token_count": args.token_count,
        "request_count": args.request_count,
        "cost_usd": args.cost_usd,
    }
    positive = {name: value for name, value in requested.items() if value > 0}
    if positive:
        raise JobConfigurationError(
            "generic marathon workers do not report remote usage; positive remote "
            f"limits cannot be enforced honestly: {positive}"
        )


def _auto_job_id() -> str:
    """Return a bounded UTC identifier accepted by the shared path policy."""

    return dt.datetime.now(dt.timezone.utc).strftime("job-%Y%m%dT%H%M%SZ")


def _budget_from_args(args: argparse.Namespace) -> ResourceBudget:
    """Compile CLI limits into the same hard budget used by other discovery jobs."""

    deadline = dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=args.duration_seconds)
    return ResourceBudget.from_mapping(
        {
            "budget_id": f"marathon-{args.job_id}",
            "wall_time_seconds": args.duration_seconds,
            "grace_period_seconds": args.grace_period_seconds,
            "cpu_seconds": args.cpu_seconds or max(1, args.duration_seconds * 2),
            "memory_bytes": args.memory_bytes,
            "disk_bytes": args.disk_bytes,
            "network_bytes": args.network_bytes,
            "token_count": args.token_count,
            "request_count": args.request_count,
            "cost_usd": args.cost_usd,
            "absolute_deadline": deadline.isoformat(),
        }
    )


def classify_job_outcome(
    *,
    completed: int,
    failed: int,
    terminal_worker_statuses: list[str],
    report_results: list[dict[str, Any]],
) -> tuple[str, int]:
    """Return a stable terminal taxonomy and process exit code."""

    report_failed = any(row["status"] != "succeeded" for row in report_results)
    resource_failure = next(
        (
            item
            for item in terminal_worker_statuses
            if item
            in {
                "deadline_exhausted",
                "cpu_exhausted",
                "out_of_memory",
                "disk_exhausted",
                "network_exhausted",
                "token_exhausted",
                "request_exhausted",
                "spend_exhausted",
            }
        ),
        None,
    )
    if resource_failure:
        return resource_failure, 3
    if report_failed:
        return "completed_with_report_failures", 2
    if failed:
        return ("completed_with_worker_failures", 0) if completed else ("worker_failed", 1)
    if completed:
        return "completed", 0
    return "no_cycle_completed", 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration-seconds", type=int, default=3600)
    parser.add_argument("--branch-engine", choices=["api", "codex"], default="api")
    parser.add_argument(
        "--min-cycle-seconds",
        type=int,
        default=60,
        help="Legacy per-cycle budget hint; it no longer establishes research validity.",
    )
    parser.add_argument("--max-active-branches", type=int, default=1)
    parser.add_argument("--target", required=True, help="Exact target id; active pointers are forbidden.")
    parser.add_argument("--run-id", required=True, help="Exact existing legacy marathon run id.")
    parser.add_argument("--canonical-theory-cycle", type=Path, required=True)
    parser.add_argument(
        "--canonical-theory-state-root",
        type=Path,
        default=DEFAULT_CANONICAL_THEORY_STATE_ROOT,
    )
    parser.add_argument("--api-key-config")
    parser.add_argument("--parallel-branches", action="store_true", help="Pass through concurrent Azure/API branch execution.")
    parser.add_argument("--api-max-workers", type=int, help="Maximum concurrent API branch agents for each cycle.")
    parser.add_argument("--api-request-spacing-seconds", type=float, help="Deterministic launch spacing between API branch agents.")
    parser.add_argument("--job-id")
    parser.add_argument("--grace-period-seconds", type=float, default=2.0)
    parser.add_argument("--report-reserve-seconds", type=float, default=30.0)
    parser.add_argument("--cpu-seconds", type=float)
    parser.add_argument("--memory-bytes", type=int, default=2 * 1024 * 1024 * 1024)
    parser.add_argument("--disk-bytes", type=int, default=2 * 1024 * 1024 * 1024)
    parser.add_argument("--network-bytes", type=int, default=0)
    parser.add_argument("--token-count", type=int, default=0)
    parser.add_argument("--request-count", type=int, default=0)
    parser.add_argument("--cost-usd", type=float, default=0.0)
    parser.add_argument("--output-capture-bytes", type=int, default=1024 * 1024)
    args = parser.parse_args()

    if args.duration_seconds <= 0:
        parser.error("--duration-seconds must be positive")
    if args.report_reserve_seconds < 0 or args.report_reserve_seconds >= args.duration_seconds:
        parser.error("--report-reserve-seconds must be non-negative and below the total duration")
    try:
        args.job_id = validate_job_id(args.job_id or _auto_job_id())
        if args.output_capture_bytes <= 0:
            raise JobConfigurationError("--output-capture-bytes must be positive")
        validate_remote_budget_contract(args)
        binding = resolve_research_binding(args)
        budget = _budget_from_args(args)
    except ValueError as exc:
        parser.error(str(exc))
    governor = ResourceGovernor(
        budget,
        run_directory=ROOT / "agentic",
        allowed_working_directory=ROOT,
        capture_limit_bytes=args.output_capture_bytes,
        disk_sample_interval_seconds=0.05,
    )

    job_dir = ROOT / "agentic/logs/discovery_marathon_jobs"
    job_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = contained_path(job_dir, f"{args.job_id}.json")
    log_path = contained_path(job_dir, f"{args.job_id}.jsonl")
    completed = 0
    failed = 0
    status = "running"
    report_results: list[dict[str, Any]] = []
    terminal_worker_statuses: list[str] = []

    def manifest() -> dict[str, Any]:
        return {
            "job_id": args.job_id,
            "status": status,
            "duration_seconds": args.duration_seconds,
            "absolute_deadline": governor.deadline.isoformat(),
            "completed_cycles": completed,
            "failed_cycle_attempts": failed,
            "terminal_worker_statuses": terminal_worker_statuses,
            "report_results": report_results,
            "log_path": rel(log_path),
            "branch_engine": args.branch_engine,
            "max_active_branches": args.max_active_branches,
            "parallel_branches": args.parallel_branches,
            "api_max_workers": args.api_max_workers or 1,
            "api_request_spacing_seconds": args.api_request_spacing_seconds or 0.0,
            "target": args.target or "",
            "research_binding": asdict(binding),
            "budget": {
                "budget_id": budget.budget_id,
                "wall_time_seconds": budget.wall_time_seconds,
                "grace_period_seconds": budget.grace_period_seconds,
                "cpu_seconds": budget.cpu_seconds,
                "memory_bytes": budget.memory_bytes,
                "disk_bytes": budget.disk_bytes,
                "network_bytes": budget.network_bytes,
                "token_count": budget.token_count,
                "request_count": budget.request_count,
                "cost_usd": budget.cost_usd,
            },
            "usage": {
                "wall_time_seconds": governor.usage.wall_time_seconds,
                "cpu_seconds": governor.usage.cpu_seconds,
                "peak_memory_bytes": governor.usage.peak_memory_bytes,
                "disk_bytes": governor.usage.disk_bytes,
                "network_bytes": governor.usage.network_bytes,
                "token_count": governor.usage.token_count,
                "request_count": governor.usage.request_count,
                "cost_usd": governor.usage.cost_usd,
            },
            "resource_measurement": governor.measurement_boundaries(),
            "output_capture_bytes": args.output_capture_bytes,
            "updated_utc": utc_now(),
        }

    def emit(event: dict[str, Any]) -> None:
        payload = {"created_utc": utc_now(), **event}
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, sort_keys=True) + "\n")
        print(json.dumps(payload, sort_keys=True), flush=True)
        write_json(manifest_path, manifest())

    emit(
        {
            "event": "marathon_job_started",
            "absolute_deadline": governor.deadline.isoformat(),
            "duration_seconds": args.duration_seconds,
            "branch_engine": args.branch_engine,
            "cycle_budget_hint_seconds": args.min_cycle_seconds,
            "validity_policy": "semantic_receipts_not_elapsed_time",
        }
    )
    try:
        if governor.remaining_seconds() > max(
            args.report_reserve_seconds + 1.0,
            min(float(args.min_cycle_seconds), 120.0),
        ):
            command = build_cycle_command(args, binding)
            emit(
                {
                    "event": "cycle_launch",
                    "cycle_number_in_job": completed + failed + 1,
                    "remaining_seconds": governor.remaining_seconds(),
                }
            )
            result = governor.run_process(command, cwd=ROOT, role="worker")
            terminal_worker_statuses.append(result["status"])
            tail = (result.get("stdout", "") + "\n" + result.get("stderr", ""))[-4000:]
            if result["status"] == "succeeded":
                completed += 1
                emit(
                    {
                        "event": "cycle_completed",
                        "cycle_number_in_job": completed + failed,
                        "worker_status": result["status"],
                        "output_tail": tail,
                    }
                )
            else:
                failed += 1
                emit(
                    {
                        "event": "cycle_attempt_failed",
                        "cycle_number_in_job": completed + failed,
                        "returncode": result.get("returncode"),
                        "worker_status": result["status"],
                        "termination": result.get("termination"),
                        "descendant_leak_detected": result.get("descendant_leak_detected"),
                        "stdout_truncated": result.get("stdout_truncated"),
                        "stderr_truncated": result.get("stderr_truncated"),
                        "output_tail": tail,
                        "epistemic_effect": "none_operational_outcome_only",
                    }
                )
        report_commands = report_rebuild_commands(binding.run_id, binding.target_id)
        for command in report_commands:
            if governor.remaining_seconds() <= 0:
                report_results.append(
                    {"command": command, "status": "deadline_exhausted", "returncode": None}
                )
                continue
            result = governor.run_process(command, cwd=ROOT, role="report_builder")
            report_results.append(
                {
                    "command": command,
                    "status": result["status"],
                    "returncode": result.get("returncode"),
                    "stderr_tail": result.get("stderr", "")[-2000:],
                    "stdout_truncated": result.get("stdout_truncated"),
                    "stderr_truncated": result.get("stderr_truncated"),
                    "descendant_leak_detected": result.get("descendant_leak_detected"),
                }
            )
            emit(
                {
                    "event": "report_builder_terminal",
                    "command": command,
                    "report_status": result["status"],
                    "returncode": result.get("returncode"),
                }
            )
    except BudgetExceeded as exc:
        terminal_worker_statuses.append(exc.status)
        status = exc.status
        try:
            write_json(manifest_path, manifest())
        except OSError:
            pass
        return 3
    except KeyboardInterrupt:
        status = "cancelled"
        emit(
            {
                "event": "marathon_job_interrupted",
                "status": status,
                "completed_cycles": completed,
                "failed_cycle_attempts": failed,
            }
        )
        return 130

    status, exit_code = classify_job_outcome(
        completed=completed,
        failed=failed,
        terminal_worker_statuses=terminal_worker_statuses,
        report_results=report_results,
    )
    emit(
        {
            "event": "marathon_job_finished",
            "status": status,
            "completed_cycles": completed,
            "failed_cycle_attempts": failed,
            "report_failure_count": sum(row["status"] != "succeeded" for row in report_results),
        }
    )
    try:
        governor.account()
        write_json(manifest_path, manifest())
    except BudgetExceeded as exc:
        status = exc.status
        terminal_worker_statuses.append(exc.status)
        try:
            write_json(manifest_path, manifest())
        except OSError:
            pass
        return 3
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
