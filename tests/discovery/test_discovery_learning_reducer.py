# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Semantic-learning and branch-control tests independent of elapsed time."""

from __future__ import annotations

import copy

import pytest

from agentic.discovery.contracts import canonical_digest
from agentic.discovery.learning import (
    InvalidLearningDelta,
    LearningReducer,
    ReducerPolicy,
    StaleBranchState,
    initial_branch_state,
)


def _mutation(entity: str = "concept-a", after: str = "revised") -> dict:
    return {
        "mutation_kind": "ontology_edge_changed",
        "entity_id": entity,
        "before_digest": canonical_digest("prior"),
        "after_digest": canonical_digest(after),
        "description": "Changed explanatory dependence from representation to mechanism.",
    }


def _delta(
    delta_id: str,
    *,
    branch: str = "branch-a",
    classification: str = "perspective_shift",
    mutations: list[dict] | None = None,
    worker_status: str = "succeeded",
    truth_status: str = "unknown",
    evidence: dict | None = None,
    literature_effects: dict | None = None,
    duration: float = 0.01,
    **extra,
) -> dict:
    return {
        "schema_version": "1.0.0",
        "delta_id": delta_id,
        "identity": {"target_id": "target-a", "run_id": "run-a", "branch_id": branch, "state_version": 0},
        "classification": classification,
        "truth_status": truth_status,
        "worker_status": worker_status,
        "duration_seconds": duration,
        "semantic_mutations": [_mutation()] if mutations is None else mutations,
        "affected_hypothesis_ids": [],
        "evidence": evidence or {"status": "none", "relation": "none", "claim_ids": [], "falsified_premise": None},
        "literature_effects": literature_effects or {"snapshot_id": None, "changed_concept_ids": [], "changed_relation_ids": [], "scheduled_action_ids": []},
        "source_event_ids": ["devent.1"],
        "operator_receipt_ids": ["opreceipt.1"],
        "summary": "A structural delta with truth status kept separate.",
        **extra,
    }


def _state(branch: str = "branch-a") -> dict:
    return initial_branch_state(target_id="target-a", run_id="run-a", branch_id=branch)


def test_perspective_shift_counts_as_learning_without_experiment_or_truth_claim() -> None:
    next_state, receipt = LearningReducer().reduce(_state(), _delta("delta-1"), expected_generation=0)
    assert receipt["learning_recognized"] is True
    assert receipt["truth_status"] == "unknown"
    assert receipt["transition"] == "persist"
    assert next_state["generation"] == 1
    assert next_state["learning_history"][0]["duration_seconds"] == 0.01


def test_idle_time_never_turns_canned_rhetoric_into_learning() -> None:
    delta = _delta(
        "delta-rhetoric",
        classification="rhetorical_rewrite",
        mutations=[],
        duration=100000.0,
        summary="A long-lived but mutation-free paraphrase.",
    )
    next_state, receipt = LearningReducer().reduce(_state(), delta, expected_generation=0)
    assert receipt["learning_recognized"] is False
    assert next_state["plateau_count"] == 1


def test_three_materially_equivalent_outputs_trigger_configured_plateau_action() -> None:
    reducer = LearningReducer(ReducerPolicy(plateau_threshold=3, plateau_action="pivot"))
    state = _state()
    receipts = []
    for index in range(1, 4):
        state, receipt = reducer.reduce(state, _delta(f"delta-{index}"), expected_generation=index - 1)
        receipts.append(receipt)
    assert receipts[0]["learning_recognized"] is True
    assert receipts[1]["learning_recognized"] is False
    assert receipts[2]["transition"] == "pivot"
    assert receipts[2]["stop_condition"] == "reflective_plateau"
    assert state["plateau_count"] == 3
    assert state["status"] == "pivoted"


def test_validated_falsifier_retires_hypothesis_but_failed_execution_does_not() -> None:
    state = _state()
    state["active_hypothesis_ids"] = ["hyp-a"]
    falsifier = _delta(
        "delta-falsifier",
        classification="new_falsifier",
        mutations=[{**_mutation("hyp-a"), "mutation_kind": "status_changed"}],
        truth_status="refuted",
        evidence={
            "status": "validated",
            "relation": "contradicts",
            "claim_ids": ["claim-falsifier"],
            "falsified_premise": "the map preserves all hard instances",
        },
        affected_hypothesis_ids=["hyp-a"],
    )
    retired, receipt = LearningReducer().reduce(state, falsifier, expected_generation=0)
    assert receipt["transition"] == "backtrack"
    assert retired["retired_hypothesis_ids"] == ["hyp-a"]
    assert retired["active_hypothesis_ids"] == []

    failed_state = _state()
    failed_state["active_hypothesis_ids"] = ["hyp-a"]
    failed = _delta(
        "delta-failed",
        classification="operational_failure",
        mutations=[],
        worker_status="failed",
        evidence={"status": "failed_execution", "relation": "none", "claim_ids": [], "falsified_premise": None},
        affected_hypothesis_ids=["hyp-a"],
        operational_error={"type": "RuntimeError", "message": "CAS process unavailable"},
        stop_condition="operational_failure",
    )
    unchanged, failed_receipt = LearningReducer().reduce(failed_state, failed, expected_generation=0)
    assert failed_receipt["learning_recognized"] is False
    assert unchanged["active_hypothesis_ids"] == ["hyp-a"]
    assert unchanged["retired_hypothesis_ids"] == []


def test_literature_delta_requires_named_theory_or_schedule_change() -> None:
    empty = _delta(
        "delta-bibliography",
        classification="literature_absorption",
        literature_effects={"snapshot_id": "snapshot-1", "changed_concept_ids": [], "changed_relation_ids": [], "scheduled_action_ids": []},
    )
    with pytest.raises(InvalidLearningDelta, match="named theory"):
        LearningReducer().reduce(_state(), empty, expected_generation=0)
    changed = _delta(
        "delta-literature",
        classification="literature_contradiction",
        literature_effects={"snapshot_id": "snapshot-2", "changed_concept_ids": ["concept-a"], "changed_relation_ids": [], "scheduled_action_ids": ["action-rebase"]},
    )
    _, receipt = LearningReducer().reduce(_state(), changed, expected_generation=0)
    assert receipt["learning_recognized"] is True


def test_failed_parallel_worker_is_operational_while_valid_sibling_remains_learning() -> None:
    states = {"branch-a": _state("branch-a"), "branch-b": _state("branch-b")}
    good = _delta("delta-good", branch="branch-a", classification="theory_synthesis")
    failed = _delta(
        "delta-bad", branch="branch-b", classification="operational_failure", mutations=[], worker_status="timed_out",
        evidence={"status": "failed_execution", "relation": "none", "claim_ids": [], "falsified_premise": None},
        operational_error={"type": "TimeoutExpired", "message": "deadline"},
    )
    next_states, receipts = LearningReducer().reduce_siblings(states, [failed, good])
    by_branch = {receipt["identity"]["branch_id"]: receipt for receipt in receipts}
    assert by_branch["branch-a"]["learning_recognized"] is True
    assert by_branch["branch-b"]["learning_recognized"] is False
    assert next_states["branch-a"]["generation"] == 1
    assert next_states["branch-b"]["operational_outcomes"][0]["worker_status"] == "timed_out"


def test_only_matching_generation_and_identity_can_transition() -> None:
    with pytest.raises(StaleBranchState, match="compare-and-swap"):
        LearningReducer().reduce(_state(), _delta("delta-stale"), expected_generation=4)
    wrong = _delta("delta-wrong", branch="branch-b")
    with pytest.raises(InvalidLearningDelta, match="branch_id"):
        LearningReducer().reduce(_state("branch-a"), wrong, expected_generation=0)


def test_meaningful_label_without_mutation_is_rejected_as_self_attestation() -> None:
    vapour = _delta("delta-vapour", classification="conceptual_deepening", mutations=[])
    with pytest.raises(InvalidLearningDelta, match="requires at least one"):
        LearningReducer().reduce(_state(), vapour, expected_generation=0)


def test_formalization_and_proof_ready_are_semantic_completion_conditions() -> None:
    state, receipt = LearningReducer().reduce(
        _state(), _delta("delta-proof", stop_condition="proof_ready"), expected_generation=0
    )
    assert receipt["transition"] == "complete"
    assert state["status"] == "completed"
    assert receipt["next_state_digest"] == canonical_digest(state)


def test_reducer_does_not_mutate_its_inputs() -> None:
    state, delta = _state(), _delta("delta-immutable")
    prior_state, prior_delta = copy.deepcopy(state), copy.deepcopy(delta)
    LearningReducer().reduce(state, delta, expected_generation=0)
    assert state == prior_state
    assert delta == prior_delta
