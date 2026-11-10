# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Contract tests for aggressive but epistemically disciplined theory seeds."""

from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path

import pytest

from agentic.discovery.contracts import ContractError, canonical_digest
from agentic.discovery.hypotheses import (
    blind_articulation_digest,
    build_demo_high_risk_portfolio,
    forge_high_risk_portfolio,
    structural_signature,
    validate_high_risk_portfolio,
)
from agentic.discovery.literature import build_demo_literature_snapshot


ROOT = Path(__file__).resolve().parents[2]


def _charter(snapshot: dict) -> dict:
    """Provide exact target pressure, protected success, and drift boundaries."""

    return {
        "target_id": snapshot["target_id"],
        "target_statement": "Explain the target without replacing its quantifiers.",
        "theory_state_digest": snapshot["theory_state_digest"],
        "root_tensions": [
            "Local witness structure does not explain global behavior.",
            "Recurring barriers lack one mechanism.",
        ],
        "target_commitments": [
            "Preserve exact quantifiers, regime, and nontrivial target identity."
        ],
        "protected_successes": [
            "Recover the incumbent construction in its verified boundary regime."
        ],
        "forbidden_target_drift": "No average-case, finite-only, or lexical proxy.",
    }


def _rehash(portfolio: dict) -> None:
    """Rebind the envelope after an adversarial test mutation."""

    core = {
        key: value
        for key, value in portfolio.items()
        if key != "content_digest"
    }
    portfolio["content_digest"] = canonical_digest(core)


def _rebind_articulation(candidate: dict) -> None:
    """Update the blind/rebase binding after a deliberate semantic mutation."""

    digest = blind_articulation_digest(candidate)
    candidate["blind_articulation_digest"] = digest
    candidate["literature_rebase_receipt"][
        "blind_articulation_digest"
    ] = digest


def test_major_portfolio_has_ten_structural_corners_and_control() -> None:
    portfolio = build_demo_high_risk_portfolio()
    assert 8 <= len(portfolio["hypotheses"]) <= 12
    assert len(portfolio["corner_coverage"]) >= 6
    assert "ontology_inversion" in portfolio["corner_coverage"]
    assert "missing_mediator" in portfolio["corner_coverage"]
    assert "cross_field_transfer" in portfolio["corner_coverage"]
    assert "negative_theory" in portfolio["corner_coverage"]
    assert portfolio["control_hypothesis_ids"]
    controls = {
        item["hypothesis_id"]
        for item in portfolio["hypotheses"]
        if item["is_control"]
    }
    assert controls == set(portfolio["control_hypothesis_ids"])


def test_two_low_confidence_high_upside_nondominated_wildcards_survive() -> None:
    portfolio = build_demo_high_risk_portfolio()
    hypotheses = {
        item["hypothesis_id"]: item for item in portfolio["hypotheses"]
    }
    pareto = {
        item["hypothesis_id"]: item for item in portfolio["pareto_assessment"]
    }
    assert len(portfolio["protected_wildcard_ids"]) >= 2
    for hypothesis_id in portfolio["protected_wildcard_ids"]:
        candidate = hypotheses[hypothesis_id]
        assert candidate["risk_axes"]["probability_of_truth"] <= 0.35
        assert candidate["quality_axes"]["value_if_true"] >= 0.80
        assert candidate["selection_status"] == "protected_wildcard"
        assert pareto[hypothesis_id]["nondominated"] is True


def test_selected_seeds_have_mechanism_relevance_correction_and_boundary() -> None:
    portfolio = build_demo_high_risk_portfolio()
    hypotheses = {
        item["hypothesis_id"]: item for item in portfolio["hypotheses"]
    }
    for seed in portfolio["parallel_branch_seeds"]:
        candidate = hypotheses[seed["hypothesis_id"]]
        assert candidate["mechanism"].strip()
        assert candidate["target_pressures_addressed"]
        assert candidate["protected_successes"]
        assert candidate["assumptions_or_invariants_risked"]
        assert candidate["unification_upside"].strip()
        assert candidate["explanatory_upside"].strip()
        assert candidate["correction_conditions"]
        assert candidate["boundary_case"].strip()
        assert seed["first_theory_actions"]
        assert seed["forbidden_cross_branch_context"]


def test_local_literature_keeps_seeds_incubating_and_never_claims_novelty() -> None:
    portfolio = build_demo_high_risk_portfolio()
    assert all(not item["novelty_claim"] for item in portfolio["hypotheses"])
    assert all(
        item["concept_lifecycle_state"] == "incubating"
        for item in portfolio["hypotheses"]
    )
    assert all(
        item["literature_relation"] != "pending_rebase"
        for item in portfolio["hypotheses"]
    )
    assert all(
        "not evidence of novelty" in item["non_claim_boundary"]
        for item in portfolio["hypotheses"]
    )


def test_structural_paraphrase_is_deduplicated_by_mechanism_not_text() -> None:
    snapshot = build_demo_literature_snapshot(target_id="dedupe-target")
    baseline = forge_high_risk_portfolio(_charter(snapshot), snapshot)
    proposals = copy.deepcopy(baseline["hypotheses"])
    duplicate = copy.deepcopy(proposals[0])
    duplicate["hypothesis_id"] = "hypothesis.paraphrase"
    duplicate["intuitive_leap"] = (
        "Different wording for the exact same primitives and causal mechanism."
    )
    proposals[1] = duplicate
    portfolio = forge_high_risk_portfolio(
        _charter(snapshot), snapshot, proposals=proposals
    )
    assert portfolio["structural_duplicate_groups"]
    assert any(
        "hypothesis.paraphrase" in group
        for group in portfolio["structural_duplicate_groups"]
    )
    active_signatures = [
        item["structural_signature"]
        for item in portfolio["hypotheses"]
        if item["selection_status"]
        in {"selected_pareto", "protected_wildcard", "control"}
    ]
    assert len(active_signatures) == len(set(active_signatures))


def test_pairwise_overlap_is_complete_and_branch_seeds_are_selected_exactly() -> None:
    portfolio = build_demo_high_risk_portfolio()
    count = len(portfolio["hypotheses"])
    assert len(portfolio["pairwise_distinction_matrix"]) == count * (count - 1) // 2
    selected = {
        item["hypothesis_id"]
        for item in portfolio["hypotheses"]
        if item["selection_status"] in {"selected_pareto", "protected_wildcard"}
    }
    seeds = {
        item["hypothesis_id"] for item in portfolio["parallel_branch_seeds"]
    }
    assert seeds == selected


def test_mystical_or_target_free_candidate_is_rejected() -> None:
    mystical = build_demo_high_risk_portfolio()
    mystical["hypotheses"][0][
        "mechanism"
    ] = "A mystical vibration solves everything without an object or relation."
    _rebind_articulation(mystical["hypotheses"][0])
    _rehash(mystical)
    with pytest.raises(ContractError, match="mystical"):
        validate_high_risk_portfolio(mystical)

    target_free = build_demo_high_risk_portfolio()
    target_free["hypotheses"][0]["target_pressures_addressed"] = []
    _rebind_articulation(target_free["hypotheses"][0])
    _rehash(target_free)
    with pytest.raises(ContractError):
        validate_high_risk_portfolio(target_free)


def test_absent_match_cannot_be_laundered_into_novelty() -> None:
    portfolio = build_demo_high_risk_portfolio()
    portfolio["hypotheses"][0]["novelty_claim"] = True
    _rehash(portfolio)
    with pytest.raises(ContractError):
        validate_high_risk_portfolio(portfolio)


def test_wrong_target_literature_snapshot_rejects_generation() -> None:
    snapshot = build_demo_literature_snapshot(target_id="target-one")
    charter = _charter(snapshot)
    charter["target_id"] = "target-two"
    with pytest.raises(ContractError, match="one target"):
        forge_high_risk_portfolio(charter, snapshot)


def test_risk_reward_truth_and_cost_axes_remain_separate() -> None:
    portfolio = build_demo_high_risk_portfolio()
    for candidate in portfolio["hypotheses"]:
        assert set(candidate["risk_axes"]) == {
            "probability_of_truth",
            "failure_risk",
            "maturation_cost",
        }
        assert "value_if_true" in candidate["quality_axes"]
        assert "learning_if_false" in candidate["quality_axes"]
        assert candidate["truth_status"] == "not_assessed"
        assert structural_signature(candidate) == candidate["structural_signature"]


def test_target_grounded_exception_supports_fewer_corners_or_wildcards() -> None:
    """A narrow target may explain a real exception instead of filling quotas."""

    snapshot = build_demo_literature_snapshot(target_id="narrow-target")
    charter = _charter(snapshot)
    charter.update(
        {
            "target_supports_six_corners": False,
            "fewer_corners_reason": (
                "The target is a fixed representation theorem with no meaningful "
                "scale or cross-field transfer; five structural families remain."
            ),
            "wildcards_available": False,
            "fewer_wildcards_reason": (
                "Every low-confidence proposal below the relevance floor changes "
                "the fixed target statement, so none is viable."
            ),
        }
    )
    baseline = build_demo_high_risk_portfolio(snapshot)
    proposals = copy.deepcopy(baseline["hypotheses"])
    narrow_families = [
        "ontology_inversion",
        "missing_mediator",
        "relation_process_first",
        "negative_theory",
    ]
    for index, candidate in enumerate(proposals[:-1]):
        candidate["corner_family"] = narrow_families[
            index % len(narrow_families)
        ]
        candidate["is_wildcard"] = False
    proposals[-1]["corner_family"] = "conservative_control"
    proposals[-1]["is_wildcard"] = False
    portfolio = forge_high_risk_portfolio(
        charter, snapshot, proposals=proposals
    )
    assert len(portfolio["corner_coverage"]) == 5
    assert portfolio["protected_wildcard_ids"] == []
    assert portfolio["generation_policy"]["fewer_corners_reason"]
    assert portfolio["generation_policy"]["fewer_wildcards_reason"]


def test_high_risk_validator_cli_passes() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "agentic/scripts/validate_high_risk_hypothesis_portfolio.py",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
