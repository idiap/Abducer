# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Tests for frozen DAG fan-out, conflict preservation, rebase, and CAS."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

from agentic.discovery.contracts import ContractError, canonical_digest
from agentic.discovery.hypotheses import build_demo_high_risk_portfolio
from agentic.discovery.parallel import (
    build_parallel_manifest,
    run_parallel_hypothesis_portfolio,
    validate_parallel_portfolio,
)


ROOT = Path(__file__).resolve().parents[2]


def _portfolio() -> dict:
    """Return a complete high-risk seed portfolio."""

    return build_demo_high_risk_portfolio()


def _manifest(
    *,
    count: int = 4,
    dependencies: dict[str, list[str]] | None = None,
    seeds: list[dict] | None = None,
) -> dict:
    """Build a small bounded manifest while retaining the full source portfolio."""

    portfolio = _portfolio()
    chosen = (
        copy.deepcopy(seeds)
        if seeds is not None
        else copy.deepcopy(portfolio["parallel_branch_seeds"][:count])
    )
    return build_parallel_manifest(
        portfolio,
        base_theory_state_version=7,
        branch_seeds=chosen,
        dependencies=dependencies,
        resource_budget={
            "wall_seconds": 10,
            "max_workers": 4,
            "cost_units": 12,
            "storage_bytes": 100_000,
        },
    )


def _worker(request: dict) -> dict:
    """Produce a mechanism-specific delta from only the frozen branch request."""

    return {
        "theory_delta": {
            "delta_class": "conceptual_deepening",
            "mechanism_key": f"matured-{request['mechanism_key']}",
            "changed_question": (
                "Which explicit mediator makes the revised branch answer "
                f"{request['maturation_question']}"
            ),
            "new_explanatory_dependencies": [
                {
                    "source": request["mechanism_key"],
                    "relation": "is_reframed_through",
                    "target": request["unique_primitives"][0],
                }
            ],
            "new_distinctions": [
                {
                    "name": "carrier-vs-conclusion",
                    "left": "explanatory carrier",
                    "right": "target conclusion",
                    "preservation_condition": "carrier test does not assume conclusion",
                }
            ],
        },
        "claims": [
            {
                "proposition": "The target needs a new explanatory carrier.",
                "stance": "support",
            }
        ],
        "genealogy": [request["hypothesis_id"]],
        "conceptual_learning": True,
    }


def test_workers_share_frozen_basis_but_have_distinct_identity_and_namespace() -> None:
    manifest = _manifest()
    frozen = {
        (
            request["frozen_inputs"]["target_id"],
            request["frozen_inputs"]["theory_digest"],
            request["frozen_inputs"]["literature_digest"],
            request["frozen_inputs"]["portfolio_digest"],
        )
        for request in manifest["branch_requests"]
    }
    assert len(frozen) == 1
    assert len(
        {request["invocation_id"] for request in manifest["branch_requests"]}
    ) == len(manifest["branch_requests"])
    assert len(
        {
            request["artifact_namespace"]
            for request in manifest["branch_requests"]
        }
    ) == len(manifest["branch_requests"])
    assert len(
        {request["mechanism_key"] for request in manifest["branch_requests"]}
    ) == len(manifest["branch_requests"])
    assert all(
        "latest" in " ".join(request["forbidden_shared_reads"]).lower()
        for request in manifest["branch_requests"]
    )


def test_dependency_dag_places_children_after_parent_barrier() -> None:
    portfolio = _portfolio()
    seeds = copy.deepcopy(portfolio["parallel_branch_seeds"][:3])
    parent, child, grandchild = [seed["branch_id"] for seed in seeds]
    manifest = _manifest(
        seeds=seeds,
        dependencies={child: [parent], grandchild: [child]},
    )
    assert [wave["branch_ids"] for wave in manifest["waves"]] == [
        [parent],
        [child],
        [grandchild],
    ]
    packet = run_parallel_hypothesis_portfolio(manifest, _worker)
    validate_parallel_portfolio(packet)
    assert {
        receipt["status"] for receipt in packet["attempt_receipts"]
    } == {"completed"}


def test_correlated_seed_is_deduplicated_before_fanout() -> None:
    portfolio = _portfolio()
    seeds = copy.deepcopy(portfolio["parallel_branch_seeds"][:3])
    duplicate = copy.deepcopy(seeds[0])
    duplicate["branch_id"] = "theory-branch.correlated-paraphrase"
    duplicate["hypothesis_id"] = "hypothesis.correlated-paraphrase"
    duplicate["structural_signature"] = canonical_digest(
        {"forged": "different signature"}
    )
    duplicate["maturation_question"] = (
        seeds[0]["maturation_question"]  # Same structure, merely renamed.
    )
    seeds.append(duplicate)
    manifest = _manifest(seeds=seeds)
    assert len(manifest["branch_requests"]) == 3
    assert manifest["dependency_dag"]["duplicate_groups"]
    duplicate_ids = {
        branch_id
        for group in manifest["dependency_dag"]["duplicate_groups"]
        for branch_id in group
    }
    assert duplicate["branch_id"] in duplicate_ids


def test_conflict_preserving_merge_retains_genuine_dissenter() -> None:
    manifest = _manifest(count=4)
    dissent_id = manifest["branch_requests"][-1]["branch_id"]

    def worker(request: dict) -> dict:
        result = _worker(request)
        result["claims"][0]["stance"] = (
            "oppose" if request["branch_id"] == dissent_id else "support"
        )
        result["is_dissent"] = request["branch_id"] == dissent_id
        return result

    packet = run_parallel_hypothesis_portfolio(
        manifest, worker, cas_merge=lambda expected, proposal: expected + 1
    )
    assert packet["merge_proposal"]["contradiction_edges"]
    assert dissent_id in packet["merge_proposal"]["retained_dissent_ids"]
    expected_wildcards = {
        request["branch_id"]
        for request in manifest["branch_requests"]
        if request["is_wildcard"]
    }
    assert set(packet["merge_proposal"]["retained_wildcard_ids"]) == expected_wildcards
    assert packet["reducer_receipt"]["compare_and_swap_status"] == "committed"


def test_stale_compare_and_swap_generation_is_rejected() -> None:
    manifest = _manifest(count=2)
    packet = run_parallel_hypothesis_portfolio(
        manifest,
        _worker,
        cas_merge=lambda expected, proposal: expected + 2,
    )
    assert packet["reducer_receipt"]["compare_and_swap_status"] == "conflict"
    assert packet["reducer_receipt"]["committed_state_version"] is None


def test_new_literature_mid_wave_rebases_every_survivor_before_merge() -> None:
    manifest = _manifest(count=3)
    calls = {"resolver": 0, "cas": 0}
    newest = {
        "snapshot_id": "literature-snapshot.newer",
        "content_digest": canonical_digest({"new": "literature"}),
    }

    def resolver() -> dict:
        calls["resolver"] += 1
        if calls["resolver"] == 1:
            return {
                "snapshot_id": manifest["literature_snapshot_id"],
                "content_digest": manifest["literature_snapshot_digest"],
            }
        return newest

    def rebase(result: dict, snapshot: dict) -> dict:
        return {
            "literature_digest": snapshot["content_digest"],
            "theory_delta": {
                **result["theory_delta"],
                "literature_change": "Explicitly checked against the newer snapshot.",
            },
        }

    def cas(expected: int, proposal: dict) -> int:
        calls["cas"] += 1
        return expected + 1

    packet = run_parallel_hypothesis_portfolio(
        manifest,
        _worker,
        literature_resolver=resolver,
        rebase_worker=rebase,
        cas_merge=cas,
    )
    assert packet["literature_rebase"]["status"] == "rebased"
    assert set(packet["literature_rebase"]["required_branch_ids"]) == set(
        packet["literature_rebase"]["rebased_branch_ids"]
    )
    assert all(
        result["literature_status"] == "rebased"
        for result in packet["branch_results"]
    )
    assert all(result["pre_search_genealogy"] for result in packet["branch_results"])
    assert calls["cas"] == 1


def test_supersession_without_rebase_blocks_synthesis_and_cas() -> None:
    manifest = _manifest(count=2)
    calls = {"resolver": 0, "cas": 0}

    def resolver() -> dict:
        calls["resolver"] += 1
        return {
            "snapshot_id": (
                manifest["literature_snapshot_id"]
                if calls["resolver"] == 1
                else "literature-snapshot.newer"
            ),
            "content_digest": (
                manifest["literature_snapshot_digest"]
                if calls["resolver"] == 1
                else canonical_digest({"new": 2})
            ),
        }

    def cas(expected: int, proposal: dict) -> int:
        calls["cas"] += 1
        return expected + 1

    packet = run_parallel_hypothesis_portfolio(
        manifest,
        _worker,
        literature_resolver=resolver,
        cas_merge=cas,
    )
    assert packet["literature_rebase"]["status"] == "rebase_blocked"
    assert packet["literature_rebase"]["blocked_branch_ids"]
    assert packet["reducer_receipt"]["compare_and_swap_status"] == "blocked_rebase"
    assert calls["cas"] == 0


def test_worker_mutation_cannot_change_sibling_or_manifest_inputs() -> None:
    manifest = _manifest(count=3)
    before = copy.deepcopy(manifest)

    def mutating_worker(request: dict) -> dict:
        request["frozen_inputs"]["theory_digest"] = canonical_digest(
            {"malicious": True}
        )
        request["forbidden_shared_reads"].clear()
        return _worker(request)

    packet = run_parallel_hypothesis_portfolio(manifest, mutating_worker)
    assert manifest == before
    assert {
        request["frozen_inputs"]["theory_digest"]
        for request in packet["branch_requests"]
    } == {manifest["base_theory_digest"]}


def test_digest_invalid_manifest_is_rejected_before_any_worker_runs() -> None:
    manifest = _manifest(count=2)
    manifest["branch_requests"][0]["maturation_question"] = (
        "Tampered after the immutable input digest was issued."
    )
    calls: list[str] = []

    def worker(request: dict) -> dict:
        calls.append(request["branch_id"])
        return _worker(request)

    with pytest.raises(ContractError, match="immutable input digest mismatch"):
        run_parallel_hypothesis_portfolio(manifest, worker)
    assert calls == []


def test_matched_budget_progress_uses_corner_coverage_not_worker_count() -> None:
    def conservative_control(request: dict) -> dict:
        return {
            "theory_delta": {
                "delta_class": "conservative_local_continuation",
                "changed_question": "Which existing estimate can be tightened?",
            },
            "claims": [],
            "conceptual_learning": False,
        }

    packet = run_parallel_hypothesis_portfolio(
        _manifest(count=4),
        _worker,
        matched_budget_control_worker=conservative_control,
    )
    metrics = packet["portfolio_metrics"]
    assert metrics["worker_count_is_progress"] is False
    assert metrics["conceptual_corner_coverage"] >= 2
    assert metrics["matched_budget_comparison_authorized"] is True
    assert metrics["matched_budget_control"]["status"] == "completed"
    assert len(metrics["matched_budget_control"]["attempt_receipts"]) == 4
    assert metrics["matched_budget_improvement"] is True


def test_branch_cost_or_storage_overrun_is_invalid_not_theory_evidence() -> None:
    manifest = _manifest(count=3)
    overrun_id = manifest["branch_requests"][0]["branch_id"]

    def worker(request: dict) -> dict:
        result = _worker(request)
        if request["branch_id"] == overrun_id:
            result["resource_usage"] = {
                "cost_units": request["budget"]["cost_units"] + 1,
                "storage_bytes": request["budget"]["storage_bytes"] + 1,
            }
        return result

    packet = run_parallel_hypothesis_portfolio(manifest, worker)
    receipt = next(
        item
        for item in packet["attempt_receipts"]
        if item["branch_id"] == overrun_id
    )
    assert receipt["status"] == "invalid"
    assert receipt["failure_class"] == "output_contract_violation"
    assert overrun_id not in {
        result["branch_id"] for result in packet["branch_results"]
    }
    assert len(packet["partial_failure_ledger"]["preserved_branch_ids"]) == 2


def test_timeout_kills_worker_before_any_late_side_effect(tmp_path: Path) -> None:
    portfolio = _portfolio()
    seed = copy.deepcopy(portfolio["parallel_branch_seeds"][0])
    seed["budget"] = {"wall_seconds": 0.05, "cost_units": 1, "storage_bytes": 1000}
    manifest = _manifest(seeds=[seed])
    marker = tmp_path / "late-worker-side-effect.txt"

    def late_worker(request: dict) -> dict:
        subprocess.Popen(
            [
                sys.executable,
                "-c",
                (
                    "import pathlib,time; time.sleep(0.25); "
                    f"pathlib.Path({str(marker)!r}).write_text('descendant')"
                ),
            ]
        )
        time.sleep(1.0)
        return _worker(request)

    packet = run_parallel_hypothesis_portfolio(manifest, late_worker)
    assert packet["attempt_receipts"][0]["status"] == "timeout"
    time.sleep(0.30)
    assert not marker.exists(), "a timed-out worker continued after its receipt"


def test_prior_run_requires_full_validation_and_exact_current_input() -> None:
    manifest = _manifest(count=2)
    prior = run_parallel_hypothesis_portfolio(manifest, _worker)

    def sealed(payload: dict) -> tuple[dict, object]:
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        descriptor = {
            "artifact_ref": "agentic/runs/parallel/sealed/prior-run.json",
            "sha256": "sha256:" + hashlib.sha256(raw).hexdigest(),
            "byte_length": len(raw),
            "media_type": "application/json",
            "loader_id": "test-content-addressed-loader.v1",
        }
        return descriptor, lambda supplied: raw

    descriptor, loader = sealed(prior)

    def must_not_run(_request: dict) -> dict:
        raise AssertionError("sealed successful branch should have been reused")

    with pytest.raises(ContractError, match="sealed byte loader"):
        run_parallel_hypothesis_portfolio(manifest, must_not_run, prior_run=prior)
    replay = run_parallel_hypothesis_portfolio(
        manifest,
        must_not_run,
        prior_run=prior,
        prior_evidence_descriptor=descriptor,
        sealed_prior_loader=loader,
    )
    assert {item["status"] for item in replay["attempt_receipts"]} == {"reused"}

    tampered = copy.deepcopy(prior)
    tampered["branch_results"][0]["theory_delta"]["mechanism_key"] = "tampered"
    tampered["content_digest"] = canonical_digest(
        {key: value for key, value in tampered.items() if key != "content_digest"}
    )
    tampered_descriptor, tampered_loader = sealed(tampered)
    with pytest.raises(ContractError, match="prior_run failed full portfolio validation"):
        run_parallel_hypothesis_portfolio(
            manifest,
            must_not_run,
            prior_run=tampered,
            prior_evidence_descriptor=tampered_descriptor,
            sealed_prior_loader=tampered_loader,
        )

    changed_seeds = copy.deepcopy(_portfolio()["parallel_branch_seeds"][:2])
    changed_seeds[0]["maturation_question"] += " With a genuinely changed input?"
    changed_manifest = _manifest(seeds=changed_seeds)
    with pytest.raises(ContractError, match="exact current input"):
        run_parallel_hypothesis_portfolio(
            changed_manifest,
            must_not_run,
            prior_run=prior,
            prior_evidence_descriptor=descriptor,
            sealed_prior_loader=loader,
        )


def test_worker_learning_claim_is_advisory_and_semantic_delta_is_authoritative() -> None:
    manifest = _manifest(count=2)
    shallow_id = manifest["branch_requests"][0]["branch_id"]

    def worker(request: dict) -> dict:
        if request["branch_id"] == shallow_id:
            return {
                "theory_delta": {
                    "delta_class": "conceptual_deepening",
                    "mechanism_key": request["mechanism_key"],
                    "changed_question": request["expected_theory_delta"],
                },
                "claims": [],
                "conceptual_learning": True,
            }
        result = _worker(request)
        result["conceptual_learning"] = False
        return result

    packet = run_parallel_hypothesis_portfolio(manifest, worker)
    results = {item["branch_id"]: item for item in packet["branch_results"]}
    assert results[shallow_id]["worker_claimed_conceptual_learning"] is True
    assert results[shallow_id]["semantic_delta"]["material"] is False
    assert results[shallow_id]["conceptual_learning"] is False
    deep_id = next(branch_id for branch_id in results if branch_id != shallow_id)
    assert results[deep_id]["worker_claimed_conceptual_learning"] is False
    assert results[deep_id]["semantic_delta"]["material"] is True
    assert results[deep_id]["conceptual_learning"] is True
    assert packet["merge_proposal"]["pareto_frontier_ids"] == [deep_id]
    assert packet["portfolio_metrics"]["independent_learning_count"] == 1


def test_parallel_validator_cli_passes_partial_failure_self_check() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "agentic/scripts/validate_parallel_hypothesis_portfolio.py",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
