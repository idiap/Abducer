# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Theory-aware semantic learning and authoritative branch-state reduction.

This module distinguishes a change in conceptual structure from truth status,
elapsed time, polished prose, or mere activity.  ``LearningReducer`` is the only
public transition authority: it classifies mutation-bearing deltas, detects
semantic plateaus, handles validated falsifiers, preserves sibling outcomes, and
emits a digest-bound reducer receipt suitable for a transactional commit.
"""

from __future__ import annotations

import copy
import dataclasses
from typing import Any, Mapping, Sequence

from .contracts import ContractError, canonical_digest, stable_identifier, utc_now, validate_instance


MEANINGFUL_CLASSIFICATIONS = frozenset(
    {
        "perspective_shift",
        "conceptual_deepening",
        "theory_synthesis",
        "unification",
        "ontology_revision",
        "explanatory_compression",
        "productive_contradiction",
        "literature_absorption",
        "literature_contradiction",
        "source_generated_opportunity",
        "high_risk_maturation",
        "branch_convergence",
        "branch_conflict",
        "new_supported_claim",
        "new_falsifier",
        "assumption_repair",
        "region_narrowing",
    }
)
NON_LEARNING_CLASSIFICATIONS = frozenset({"duplicate", "rhetorical_rewrite", "operational_failure"})
TRANSITIONS = frozenset(
    {"promote", "persist", "pivot", "backtrack", "quarantine", "exhaust", "complete"}
)
TERMINAL_STATUSES = frozenset({"quarantined", "exhausted", "completed", "refuted"})


class StaleBranchState(ContractError):
    """Raised when a reducer caller presents an obsolete state generation."""


class InvalidLearningDelta(ContractError):
    """Raised when a claimed learning category lacks its semantic witness."""


@dataclasses.dataclass(frozen=True, slots=True)
class ReducerPolicy:
    """Explicit semantic plateau and stop policy for one discovery programme."""

    plateau_threshold: int = 3
    plateau_action: str = "pivot"

    def __post_init__(self) -> None:
        if self.plateau_threshold < 2:
            raise ContractError("plateau_threshold must be at least two")
        if self.plateau_action not in {"pivot", "backtrack", "exhaust"}:
            raise ContractError("plateau_action must be pivot, backtrack, or exhaust")


def initial_branch_state(
    *, target_id: str, run_id: str, branch_id: str, generation: int = 0
) -> dict[str, Any]:
    """Construct the state shape that all reducer transitions preserve."""

    if generation < 0:
        raise ContractError("branch generation cannot be negative")
    return {
        "schema_version": "1.0.0",
        "reducer_version": "1.0.0",
        "target_id": target_id,
        "run_id": run_id,
        "branch_id": branch_id,
        "generation": generation,
        "status": "incubating",
        "plateau_count": 0,
        "semantic_occurrences": {},
        "semantic_history": [],
        "learning_history": [],
        "operational_outcomes": [],
        "retired_hypothesis_ids": [],
        "active_hypothesis_ids": [],
        "last_transition": None,
        "stop_condition": None,
    }


def semantic_fingerprint(delta: Mapping[str, Any]) -> str:
    """Hash actual conceptual mutations while ignoring rhetoric and duration."""

    mutations = []
    for mutation in delta.get("semantic_mutations", []):
        mutations.append(
            {
                "mutation_kind": mutation.get("mutation_kind"),
                "entity_id": mutation.get("entity_id"),
                "before_digest": mutation.get("before_digest"),
                "after_digest": mutation.get("after_digest"),
            }
        )
    mutations.sort(key=lambda item: canonical_digest(item))
    evidence = delta.get("evidence", {})
    literature = delta.get("literature_effects", {})
    semantic = {
        "classification": delta.get("classification"),
        "mutations": mutations,
        "affected_hypothesis_ids": sorted(delta.get("affected_hypothesis_ids", [])),
        "evidence": {
            "status": evidence.get("status"),
            "relation": evidence.get("relation"),
            "falsified_premise": evidence.get("falsified_premise"),
            "claim_ids": sorted(evidence.get("claim_ids", [])),
        },
        "literature": {
            "snapshot_id": literature.get("snapshot_id"),
            "changed_concept_ids": sorted(literature.get("changed_concept_ids", [])),
            "changed_relation_ids": sorted(literature.get("changed_relation_ids", [])),
            "scheduled_action_ids": sorted(literature.get("scheduled_action_ids", [])),
        },
    }
    return canonical_digest(semantic)


def _validate_semantics(delta: Mapping[str, Any]) -> tuple[str, bool, str]:
    """Return normalized classification, learning flag, and semantic fingerprint."""

    validate_instance(delta, "discovery_learning_delta.schema.json")
    classification = delta["classification"]
    mutations = delta["semantic_mutations"]
    worker_status = delta["worker_status"]
    if worker_status in {"failed", "timed_out"}:
        if classification != "operational_failure":
            raise InvalidLearningDelta("failed/timed-out workers can only report operational_failure")
        if mutations:
            raise InvalidLearningDelta("operational failure cannot smuggle semantic mutations")
        return classification, False, semantic_fingerprint(delta)
    if classification in MEANINGFUL_CLASSIFICATIONS and not mutations:
        raise InvalidLearningDelta(f"{classification} requires at least one named semantic mutation")
    if classification in NON_LEARNING_CLASSIFICATIONS and mutations:
        raise InvalidLearningDelta(f"{classification} cannot carry semantic mutations")
    if classification.startswith("literature_") or classification == "source_generated_opportunity":
        effects = delta.get("literature_effects", {})
        named_changes = sum(
            len(effects.get(field, []))
            for field in ("changed_concept_ids", "changed_relation_ids", "scheduled_action_ids")
        )
        if named_changes == 0:
            raise InvalidLearningDelta("literature learning requires a named theory or scheduling change")
    if classification == "new_falsifier":
        evidence = delta["evidence"]
        if evidence["status"] != "validated" or evidence["relation"] != "contradicts":
            raise InvalidLearningDelta("a new falsifier needs validated contradictory evidence")
        if not evidence.get("falsified_premise"):
            raise InvalidLearningDelta("a falsifier must preserve the exact falsified premise")
    return classification, classification in MEANINGFUL_CLASSIFICATIONS, semantic_fingerprint(delta)


def _transition_status(action: str, current: str) -> str:
    """Map reducer actions to durable branch statuses."""

    return {
        "promote": "promoted",
        "persist": "active" if current == "incubating" else current,
        "pivot": "pivoted",
        "backtrack": "backtracked",
        "quarantine": "quarantined",
        "exhaust": "exhausted",
        "complete": "completed",
    }[action]


class LearningReducer:
    """Apply one semantic delta with CAS and emit a replayable reducer receipt."""

    def __init__(self, policy: ReducerPolicy | None = None) -> None:
        self.policy = policy or ReducerPolicy()

    def reduce(
        self,
        state: Mapping[str, Any],
        delta: Mapping[str, Any],
        *,
        expected_generation: int,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Reduce a delta; elapsed time is recorded but never establishes learning."""

        current_generation = state.get("generation")
        if current_generation != expected_generation:
            raise StaleBranchState(
                f"compare-and-swap failed: expected {expected_generation}, current {current_generation}"
            )
        for field in ("target_id", "run_id", "branch_id"):
            if state.get(field) != delta["identity"].get(field):
                raise InvalidLearningDelta(f"delta {field} does not match branch state")
        classification, is_learning, fingerprint = _validate_semantics(delta)
        next_state = copy.deepcopy(dict(state))
        occurrences = next_state.setdefault("semantic_occurrences", {})
        occurrences[fingerprint] = occurrences.get(fingerprint, 0) + 1
        occurrence_count = occurrences[fingerprint]
        duplicate = occurrence_count > 1 or classification == "duplicate"
        if duplicate:
            is_learning = False
            next_state["plateau_count"] = occurrence_count
        elif is_learning:
            next_state["plateau_count"] = 0
        else:
            next_state["plateau_count"] = max(1, next_state.get("plateau_count", 0) + 1)

        action = "persist"
        stop_condition = delta.get("stop_condition")
        if classification == "operational_failure":
            next_state.setdefault("operational_outcomes", []).append(
                {
                    "delta_id": delta["delta_id"],
                    "worker_status": delta["worker_status"],
                    "error": copy.deepcopy(delta.get("operational_error")),
                }
            )
        elif classification == "new_falsifier" and is_learning:
            retired = next_state.setdefault("retired_hypothesis_ids", [])
            for hypothesis_id in delta["affected_hypothesis_ids"]:
                if hypothesis_id not in retired:
                    retired.append(hypothesis_id)
                if hypothesis_id in next_state.setdefault("active_hypothesis_ids", []):
                    next_state["active_hypothesis_ids"].remove(hypothesis_id)
            action = delta.get("recommended_transition", "backtrack")
            if action not in {"backtrack", "quarantine", "exhaust"}:
                action = "backtrack"
        elif occurrence_count >= self.policy.plateau_threshold:
            action = self.policy.plateau_action
            stop_condition = stop_condition or "reflective_plateau"
        elif stop_condition in {"formalization_ready", "proof_ready", "decisive_falsification"}:
            action = "complete" if stop_condition != "decisive_falsification" else "quarantine"
        elif stop_condition in {"all_branches_terminal", "budget_exhaustion"}:
            action = "exhaust"
        elif stop_condition == "operational_failure":
            action = "persist"
        elif is_learning and delta.get("recommended_transition") in TRANSITIONS:
            action = delta["recommended_transition"]

        if next_state.get("status") in TERMINAL_STATUSES and action not in {"persist"}:
            raise InvalidLearningDelta("terminal branch cannot transition without a new branch identity")
        if action not in TRANSITIONS:
            raise InvalidLearningDelta(f"unsupported transition: {action}")

        history_record = {
            "delta_id": delta["delta_id"],
            "classification": classification,
            "semantic_fingerprint": fingerprint,
            "learning_recognized": is_learning,
            "truth_status": delta["truth_status"],
            "occurrence_count": occurrence_count,
            "transition": action,
            "source_event_ids": list(delta["source_event_ids"]),
            "operator_receipt_ids": list(delta["operator_receipt_ids"]),
            "duration_seconds": delta["duration_seconds"],
        }
        next_state.setdefault("semantic_history", []).append(fingerprint)
        next_state.setdefault("learning_history", []).append(history_record)
        next_state["generation"] = current_generation + 1
        next_state["status"] = _transition_status(action, next_state["status"])
        next_state["last_transition"] = action
        next_state["stop_condition"] = stop_condition
        receipt = {
            "schema_version": "1.0.0",
            "reducer_version": "1.0.0",
            "reducer_receipt_id": stable_identifier(
                "lreduce", delta["delta_id"], current_generation, canonical_digest(next_state)
            ),
            "delta_id": delta["delta_id"],
            "identity": copy.deepcopy(delta["identity"]),
            "expected_generation": current_generation,
            "committed_generation": current_generation + 1,
            "classification": classification,
            "semantic_fingerprint": fingerprint,
            "learning_recognized": is_learning,
            "truth_status": delta["truth_status"],
            "transition": action,
            "stop_condition": stop_condition,
            "prior_state_digest": canonical_digest(state),
            "next_state_digest": canonical_digest(next_state),
            "reduced_at": utc_now(),
        }
        return next_state, receipt

    def reduce_siblings(
        self,
        states: Mapping[str, Mapping[str, Any]],
        deltas: Sequence[Mapping[str, Any]],
    ) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
        """Reduce branch-local outcomes independently, preserving valid siblings."""

        next_states = {branch_id: copy.deepcopy(dict(state)) for branch_id, state in states.items()}
        receipts: list[dict[str, Any]] = []
        for delta in deltas:
            branch_id = delta["identity"]["branch_id"]
            if branch_id not in next_states:
                raise InvalidLearningDelta(f"unknown sibling branch: {branch_id}")
            next_state, receipt = self.reduce(
                next_states[branch_id], delta, expected_generation=next_states[branch_id]["generation"]
            )
            next_states[branch_id] = next_state
            receipts.append(receipt)
        return next_states, receipts
