# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Regression tests for partial failure and selective retry semantics."""

from __future__ import annotations

import copy
import hashlib
import json
import time
from pathlib import Path

from agentic.discovery.hypotheses import build_demo_high_risk_portfolio
from agentic.discovery.parallel import (
    build_parallel_manifest,
    run_parallel_hypothesis_portfolio,
)


ROOT = Path(__file__).resolve().parents[2]
PARTIAL_FAILURE_PLAN = json.loads(
    (
        ROOT
        / "tests/fixtures/parallel_hypothesis_portfolio/partial_failure_plan.json"
    ).read_text(encoding="utf-8")
)


def _manifest(*, count: int = 3, seeds: list[dict] | None = None) -> dict:
    """Build a compact frozen portfolio for failure injection."""

    portfolio = build_demo_high_risk_portfolio()
    return build_parallel_manifest(
        portfolio,
        base_theory_state_version=4,
        branch_seeds=(
            copy.deepcopy(seeds)
            if seeds is not None
            else copy.deepcopy(portfolio["parallel_branch_seeds"][:count])
        ),
        resource_budget={
            "wall_seconds": 5,
            "max_workers": 3,
            "cost_units": 9,
            "storage_bytes": 100_000,
        },
    )


def _success(request: dict) -> dict:
    """Return one independently consumable conceptual delta."""

    return {
        "theory_delta": {
            "delta_class": "productive_contradiction",
            "mechanism": request["mechanism_key"],
        },
        "claims": [
            {
                "proposition": f"Mechanism {request['mechanism_key']} is worth maturing.",
                "stance": "support",
            }
        ],
        "genealogy": [request["hypothesis_id"]],
        "conceptual_learning": True,
    }


def test_one_worker_failure_does_not_erase_valid_sibling_packets() -> None:
    manifest = _manifest()
    failed_id = manifest["branch_requests"][
        PARTIAL_FAILURE_PLAN["failure_request_index"]
    ]["branch_id"]

    def worker(request: dict) -> dict:
        if request["branch_id"] == failed_id:
            raise RuntimeError(PARTIAL_FAILURE_PLAN["failure_message"])
        return _success(request)

    packet = run_parallel_hypothesis_portfolio(manifest, worker)
    assert failed_id in packet["partial_failure_ledger"]["retry_branch_ids"]
    assert len(packet["attempt_receipts"]) == PARTIAL_FAILURE_PLAN[
        "expected_attempt_count"
    ]
    assert len(packet["partial_failure_ledger"]["preserved_branch_ids"]) == (
        PARTIAL_FAILURE_PLAN["expected_preserved_success_count"]
    )
    assert len(packet["branch_results"]) == PARTIAL_FAILURE_PLAN[
        "expected_preserved_success_count"
    ]
    assert len(packet["partial_failure_ledger"]["retry_branch_ids"]) == (
        PARTIAL_FAILURE_PLAN["expected_retry_count"]
    )
    receipts = {
        receipt["branch_id"]: receipt for receipt in packet["attempt_receipts"]
    }
    assert receipts[failed_id]["status"] == "failed"
    assert receipts[failed_id]["failure_class"] == "RuntimeError"
    assert all(
        receipts[branch_id]["status"] == "completed"
        for branch_id in packet["partial_failure_ledger"]["preserved_branch_ids"]
    )


def test_invalid_output_is_operational_not_hypothesis_refutation() -> None:
    manifest = _manifest()
    invalid_id = manifest["branch_requests"][0]["branch_id"]

    def worker(request: dict) -> dict:
        if request["branch_id"] == invalid_id:
            return {"claims": []}  # Deliberately lacks a typed theory delta.
        return _success(request)

    packet = run_parallel_hypothesis_portfolio(manifest, worker)
    receipt = next(
        item
        for item in packet["attempt_receipts"]
        if item["branch_id"] == invalid_id
    )
    assert receipt["status"] == "invalid"
    assert receipt["failure_class"] == "output_contract_violation"
    assert invalid_id in packet["partial_failure_ledger"]["retry_branch_ids"]
    assert all(
        event["event_type"] != "hypothesis_refuted"
        for event in packet["merge_proposal"]["proposed_ledger_events"]
    )


def test_timeout_receipt_preserves_fast_siblings() -> None:
    portfolio = build_demo_high_risk_portfolio()
    seeds = copy.deepcopy(portfolio["parallel_branch_seeds"][:3])
    seeds[0]["budget"] = {
        "wall_seconds": 0.001,
        "cost_units": 1,
        "storage_bytes": 1000,
    }
    manifest = _manifest(seeds=seeds)
    # Manifest rendering is deterministic by branch ID, not input-list order.
    # Resolve the branch by its bound budget so the fixture exercises the
    # deadline invariant rather than scheduler ordering.
    slow_id = next(
        request["branch_id"]
        for request in manifest["branch_requests"]
        if request["budget"]["wall_seconds"] == 0.001
    )

    def worker(request: dict) -> dict:
        if request["branch_id"] == slow_id:
            time.sleep(0.02)
        return _success(request)

    packet = run_parallel_hypothesis_portfolio(manifest, worker)
    receipt = next(
        item
        for item in packet["attempt_receipts"]
        if item["branch_id"] == slow_id
    )
    assert receipt["status"] == "timeout"
    assert len(packet["partial_failure_ledger"]["preserved_branch_ids"]) == 2
    assert slow_id in packet["partial_failure_ledger"]["retry_branch_ids"]


def test_selective_retry_reuses_success_and_only_repurchases_failure() -> None:
    manifest = _manifest()
    failed_id = manifest["branch_requests"][0]["branch_id"]

    def first_worker(request: dict) -> dict:
        if request["branch_id"] == failed_id:
            raise RuntimeError("transient failure")
        return _success(request)

    first = run_parallel_hypothesis_portfolio(manifest, first_worker)
    assert {item["branch_id"] for item in first["attempt_receipts"]} == {
        request["branch_id"] for request in manifest["branch_requests"]
    }

    def retry_worker(request: dict) -> dict:
        return _success(request)

    raw = json.dumps(first, sort_keys=True, separators=(",", ":")).encode("utf-8")
    descriptor = {
        "artifact_ref": "agentic/runs/parallel/sealed/partial-failure.json",
        "sha256": "sha256:" + hashlib.sha256(raw).hexdigest(),
        "byte_length": len(raw),
        "media_type": "application/json",
        "loader_id": "partial-failure-content-addressed-loader.v1",
    }

    second = run_parallel_hypothesis_portfolio(
        manifest,
        retry_worker,
        prior_run=first,
        prior_evidence_descriptor=descriptor,
        sealed_prior_loader=lambda supplied: raw,
        cas_merge=lambda expected, proposal: expected + 1,
    )
    statuses = {
        receipt["branch_id"]: receipt["status"]
        for receipt in second["attempt_receipts"]
    }
    assert statuses[failed_id] == "completed"
    assert next(
        receipt["attempt"]
        for receipt in second["attempt_receipts"]
        if receipt["branch_id"] == failed_id
    ) == 2
    assert all(
        status == "reused"
        for branch_id, status in statuses.items()
        if branch_id != failed_id
    )
    assert second["partial_failure_ledger"]["retry_branch_ids"] == []
    assert second["reducer_receipt"]["compare_and_swap_status"] == "committed"


def test_failed_parent_blocks_child_without_erasing_independent_branch() -> None:
    portfolio = build_demo_high_risk_portfolio()
    seeds = copy.deepcopy(portfolio["parallel_branch_seeds"][:3])
    parent, independent, child = [seed["branch_id"] for seed in seeds]
    manifest = build_parallel_manifest(
        portfolio,
        base_theory_state_version=4,
        branch_seeds=seeds,
        dependencies={child: [parent]},
        resource_budget={
            "wall_seconds": 5,
            "max_workers": 3,
            "cost_units": 9,
            "storage_bytes": 100_000,
        },
    )

    def worker(request: dict) -> dict:
        if request["branch_id"] == parent:
            raise RuntimeError("parent failed")
        return _success(request)

    packet = run_parallel_hypothesis_portfolio(manifest, worker)
    receipts = {
        item["branch_id"]: item["status"] for item in packet["attempt_receipts"]
    }
    assert receipts[parent] == "failed"
    assert receipts[independent] == "completed"
    assert receipts[child] == "dependency_blocked"
    assert independent in packet["partial_failure_ledger"]["preserved_branch_ids"]
