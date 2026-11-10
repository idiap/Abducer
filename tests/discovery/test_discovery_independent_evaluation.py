# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Tests for structural creative-worth and established-claim evaluation."""

from __future__ import annotations

import copy

import pytest

from agentic.discovery.contracts import ContractError
from agentic.discovery.evaluation import (
    evaluate_discovery_delta,
    semantic_delta_evidence,
    validate_evaluation_receipt,
)


def rich_candidate() -> dict:
    return {
        "target_id": "target-pvsnp",
        "proposal_receipt_ids": ["proposal-receipt-1"],
        "proposal_invocation_id": "proposal-invocation-1",
        "proposer_identity": "creative-agent-a",
        "relevance": {
            "essential": True,
            "target_dependencies": ["dependency-circuit-lower-bound"],
            "root_tensions": ["local regularity versus global hardness"],
        },
        "concepts": [
            {
                "concept_id": "concept-obstruction-flow",
                "primitives": ["obstruction flow", "boundary witness"],
                "relations": [{"source": "obstruction flow", "kind": "accumulates-at", "target": "boundary witness"}],
                "distinctions": ["local compressibility differs from global composability"],
            }
        ],
        "ontology": {
            "primitives": ["obstruction flow", "boundary witness"],
            "relations": [{"source": "boundary witness", "kind": "certifies", "target": "composition failure"}],
        },
        "mechanism": {
            "stages": [
                {"input": "local simplification", "operation": "transport", "output": "boundary load"},
                {"input": "boundary load", "operation": "accumulate", "output": "global obstruction"},
            ],
            "causal_edges": [{"source": "boundary load", "relation": "forces", "target": "global obstruction"}],
            "counterfactuals": ["if transport preserves no load, the proposed obstruction disappears"],
        },
        "understanding_delta": {
            "before": "hardness was an undifferentiated lack of algorithm",
            "after": "hardness is traced to accumulation of boundary load under composition",
            "new_explanatory_dependencies": [
                {"source": "transport", "relation": "creates", "target": "boundary load"},
                {"source": "boundary load", "relation": "explains", "target": "composition failure"},
            ],
            "new_questions": ["which reductions preserve boundary load?"],
        },
        "unification_map": {
            "mappings": [
                {"source_system": "communication", "bridge": "boundary load", "target_system": "circuits"},
                {"source_system": "proof complexity", "bridge": "boundary load", "target_system": "circuits"},
            ],
            "preserved_differences": ["communication partitions remain protocol-relative", "proof lines retain syntactic locality"],
        },
        "new_questions": ["can boundary load be amplified without naturalness?"],
        "obligations": [{"kind": "formalize", "depends_on": "boundary load", "tests": "composition law"}],
        "predictions": [{"observable": "load", "condition": "two-stage composition", "direction": "nondecreasing"}],
        "consistency": {"assumptions": ["finite encodings", "typed reductions", "fixed composition"], "unresolved_contradictions": []},
        "correction_conditions": ["retire if load is not representation invariant", "split if reductions reverse load"],
        "falsifiers": [{"kind": "exact counterexample", "claim": "composition can erase all load"}],
        "scope_conditions": ["finite Boolean circuits", "declared reduction class"],
        "risk_reward": {
            "truth_confidence": 0.62,
            "value_if_right": 0.94,
            "learning_value_if_false": 0.8,
            "mechanism_path": "derive load transport, test composition, then formalize the obstruction",
        },
        "literature_snapshot": {
            "snapshot_id": "snapshot-pvsnp-20260721",
            "target_id": "target-pvsnp",
            "status": "validated_current",
            "content_digest": "sha256:" + "a" * 64,
        },
        "source_relation_assessments": [
            {"source_id": "source-1", "relation": "partially_overlaps", "reason": "the source has a local measure but not the transport mechanism"}
        ],
        "established_claim_gates": [],
        "promotion_requested": False,
        "proof_status": "open",
        "evidence_status": "open",
    }


def evaluate(candidate: dict, genealogy: list[dict] | None = None, **overrides: object) -> dict:
    kwargs = {
        "evaluator_identity": "independent-evaluator-b",
        "evaluator_invocation_id": "evaluation-invocation-2",
        "evaluator_version": "structural-evaluator/1.0.0",
        "genealogy": genealogy or [],
    }
    kwargs.update(overrides)
    return evaluate_discovery_delta(candidate, **kwargs)


def test_conceptual_preference_does_not_claim_proof_or_evidence() -> None:
    receipt = evaluate(rich_candidate())
    assert receipt["creative_worth_decision"] == "prefer"
    assert receipt["proof_status"] == "open"
    assert receipt["evidence_status"] == "open"
    assert receipt["promotion_decision"] == "not_requested"
    assert receipt["literature_novelty"]["claim_allowed"] is True
    validate_evaluation_receipt(receipt)


def test_rephrasing_without_structural_change_is_duplicate() -> None:
    prior = rich_candidate()
    candidate = copy.deepcopy(prior)
    candidate["understanding_delta"]["before"] = "an algorithmic absence was not differentiated"
    candidate["understanding_delta"]["after"] = "the compositional boundary bears an accumulating obstruction"
    receipt = evaluate(candidate, [prior])
    assert receipt["structural_novelty"]["classification"] == "duplicate"
    assert receipt["creative_worth_decision"] == "duplicate"


def test_marker_rich_shallow_synthesis_is_rejected_structurally() -> None:
    candidate = rich_candidate()
    for field in ("concepts", "ontology", "mechanism", "unification_map", "obligations", "predictions"):
        candidate.pop(field, None)
    candidate["self_assessment"] = "deep radical ontology synthesis unified explanatory breakthrough"
    receipt = evaluate(candidate)
    assert receipt["structural_novelty"]["classification"] == "undetermined"
    assert receipt["creative_worth_decision"] == "demote"


def test_high_reward_low_confidence_wildcard_remains_incubating() -> None:
    candidate = rich_candidate()
    candidate["risk_reward"]["truth_confidence"] = 0.12
    receipt = evaluate(candidate)
    assert receipt["risk_reward"]["portfolio_status"] == "protected_wildcard"
    assert receipt["creative_worth_decision"] == "incubate"


def test_random_counterconsensus_claim_without_mechanism_is_demoted() -> None:
    candidate = rich_candidate()
    candidate["risk_reward"]["mechanism_path"] = ""
    receipt = evaluate(candidate)
    assert receipt["creative_worth_decision"] == "demote"


def test_equal_count_placeholder_packet_cannot_purchase_semantic_quality() -> None:
    candidate = rich_candidate()
    candidate["ontology"]["primitives"] = ["x", "x"]
    candidate["concepts"][0]["primitives"] = ["x", "x"]
    candidate["concepts"][0]["relations"] = [
        {"source": "x", "kind": "x", "target": "x"}
    ]
    candidate["ontology"]["relations"] = [
        {"source": "x", "kind": "x", "target": "x"}
    ]
    candidate["mechanism"]["stages"] = [
        {"input": "x", "operation": "x", "output": "x"},
        {"input": "x", "operation": "x", "output": "x"},
    ]
    receipt = evaluate(candidate)
    assert receipt["creative_worth_decision"] == "demote"
    assert receipt["theory_quality"]["conceptual_depth"]["score"] == 0.0


def test_terminology_rename_preserves_quality_but_mediator_deletion_does_not() -> None:
    original = rich_candidate()
    renamed = copy.deepcopy(original)
    replacements = {
        "obstruction flow": "constraint current",
        "boundary witness": "interface detector",
        "boundary load": "junction pressure",
        "global obstruction": "aggregate barrier",
    }

    def rename(value: object) -> object:
        if isinstance(value, str):
            for old, new in replacements.items():
                value = value.replace(old, new)
            return value
        if isinstance(value, list):
            return [rename(item) for item in value]
        if isinstance(value, dict):
            return {key: rename(item) for key, item in value.items()}
        return value

    renamed = rename(renamed)
    assert isinstance(renamed, dict)
    original_receipt = evaluate(original)
    renamed_receipt = evaluate(renamed)
    assert renamed_receipt["pareto_vector"] == original_receipt["pareto_vector"]
    assert renamed_receipt["creative_worth_decision"] == original_receipt["creative_worth_decision"]

    deleted = copy.deepcopy(original)
    deleted["mechanism"]["stages"].pop()
    deleted_receipt = evaluate(deleted)
    assert deleted_receipt["pareto_vector"] != original_receipt["pareto_vector"]
    assert deleted_receipt["creative_worth_decision"] == "revise"


def test_pairwise_materiality_ignores_rename_and_isolated_padding() -> None:
    original = rich_candidate()
    renamed = copy.deepcopy(original)
    renamed["ontology"]["primitives"] = ["constraint current", "interface detector"]
    renamed["concepts"][0]["primitives"] = ["constraint current", "interface detector"]
    for relation in [
        *renamed["ontology"]["relations"],
        *renamed["concepts"][0]["relations"],
    ]:
        relation["source"] = relation["source"].replace("obstruction flow", "constraint current").replace("boundary witness", "interface detector")
        relation["target"] = relation["target"].replace("boundary witness", "interface detector")
    assert semantic_delta_evidence(original, renamed)["material"] is False

    padded = copy.deepcopy(original)
    padded["ontology"]["primitives"].append("fluent but disconnected ornamental carrier")
    assert semantic_delta_evidence(original, padded)["material"] is False


def test_equal_count_mediation_replacement_with_explanatory_consequences_is_material() -> None:
    before = rich_candidate()
    after = copy.deepcopy(before)
    after["mechanism"]["stages"] = [
        {"input": "local simplification", "operation": "expose", "output": "interface torsion"},
        {"input": "interface torsion", "operation": "propagate", "output": "global obstruction"},
    ]
    after["mechanism"]["causal_edges"] = [
        {"source": "interface torsion", "relation": "propagates", "target": "global obstruction"}
    ]
    after["mechanism"]["counterfactuals"] = [
        "if interface torsion cancels under composition, the proposed obstruction disappears"
    ]
    after["understanding_delta"]["new_explanatory_dependencies"] = [
        {"source": "transport", "relation": "creates", "target": "interface torsion"},
        {"source": "interface torsion", "relation": "explains", "target": "composition failure"},
    ]
    after["reflection_rounds"] = [
        {
            "round_id": "round-equal-count-mediation-replacement",
            "result": "mutated",
            "strongest_objections": [
                "Boundary load cannot distinguish reversible transport from path-dependent interface torsion."
            ],
            "mutation_or_synthesis": {
                "changed_primitives_relations_or_explanation": [
                    "Replace boundary load by interface torsion and revise both the counterfactual and explanatory dependency."
                ]
            },
        }
    ]
    delta = semantic_delta_evidence(before, after)
    assert delta["anonymous_topology_changed"] is False
    assert {"mechanism", "explanation"}.issubset(delta["changed_semantic_facets"])
    assert delta["new_material_reflection_rounds"] == 1
    assert delta["material"] is True


def test_new_objection_bearing_reflection_round_is_material_without_count_padding() -> None:
    before = rich_candidate()
    after = copy.deepcopy(before)
    after["reflection_rounds"] = [
        {
            "round_id": "round-interface-torsion",
            "result": "mutated",
            "strongest_objections": [
                "The original carrier cannot distinguish cancellation from accumulation across interfaces."
            ],
            "mutation_or_synthesis": {
                "changed_primitives_relations_or_explanation": [
                    "Introduce interface torsion and make its cancellation law explicit."
                ]
            },
        }
    ]
    delta = semantic_delta_evidence(before, after)
    assert delta["new_material_reflection_rounds"] == 1
    assert delta["material"] is True


@pytest.mark.parametrize("status,target", [("superseded", "target-pvsnp"), ("validated_current", "target-yang-mills"), ("missing", "target-pvsnp")])
def test_stale_wrong_target_or_missing_search_cannot_support_novelty(status: str, target: str) -> None:
    candidate = rich_candidate()
    candidate["literature_snapshot"].update(status=status, target_id=target)
    receipt = evaluate(candidate)
    assert receipt["literature_novelty"]["claim_allowed"] is False


def test_proposer_cannot_independently_evaluate_same_invocation() -> None:
    candidate = rich_candidate()
    with pytest.raises(ContractError, match="must not share"):
        evaluate(
            candidate,
            evaluator_identity=candidate["proposer_identity"],
            evaluator_invocation_id=candidate["proposal_invocation_id"],
        )


def test_deterministic_validator_may_validate_same_artifact() -> None:
    candidate = rich_candidate()
    receipt = evaluate(
        candidate,
        evaluator_identity=candidate["proposer_identity"],
        evaluator_invocation_id=candidate["proposal_invocation_id"],
        deterministic_validator=True,
    )
    assert receipt["deterministic_validator"] is True


def test_unknown_hard_gate_blocks_established_claim_promotion() -> None:
    candidate = rich_candidate()
    candidate.update(
        promotion_requested=True,
        proof_status="proved",
        established_claim_gates=[{"gate_id": "transfer", "applicability": "unknown", "status": "unknown", "reason": "transfer scope is unresolved"}],
    )
    receipt = evaluate(candidate)
    assert receipt["promotion_decision"] == "blocked"


def test_not_applicable_gate_requires_reasoned_waiver() -> None:
    candidate = rich_candidate()
    candidate.update(
        promotion_requested=True,
        established_claim_gates=[{"gate_id": "empirical", "applicability": "not_applicable", "status": "waived", "reason": "n/a"}],
    )
    with pytest.raises(ContractError, match="reasoned waiver"):
        evaluate(candidate)
