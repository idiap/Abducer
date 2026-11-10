# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Dependency-aware, theory-first discovery information scheduler."""

from __future__ import annotations

import copy
import datetime as dt
import fcntl
import json
import os
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from agentic.discovery.conceptual_adjudication import (
    validate_sealed_preference_authority,
)
from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    canonical_digest,
    stable_identifier,
    utc_now,
    validate_identifier,
    validate_instance,
)
from agentic.discovery.ledger import build_event, reduce_from_state


ACTION_KINDS = {
    "refresh_literature",
    "assimilate",
    "rebase",
    "forge_high_risk",
    "reflect",
    "reframe",
    "differentiate",
    "parallel_mature",
    "cross_pollinate",
    "synthesize",
    "formalize",
    "derive",
    "compare",
    "read",
    "prove",
    "probe",
    "incubate",
    "retire",
}

_VIRTUES = (
    "essential_relevance",
    "root_tension_contact",
    "expected_understanding_gain",
    "expected_unification_gain",
    "conceptual_fertility",
    "programme_impact",
    "maturity",
    "cost_efficiency",
    "closure_safety",
)

# These actions consume material resources, change lifecycle state, or can be
# mistaken for conceptual promotion.  Structural Pareto position is diagnostic;
# only the complete sealed adjudication may authorize them for a candidate.
_PREFERENCE_SENSITIVE_ACTIONS = frozenset(
    {
        "parallel_mature",
        "cross_pollinate",
        "synthesize",
        "formalize",
        "derive",
        "compare",
        "read",
        "prove",
        "probe",
        "retire",
    }
)
_CALLER_PREFERENCE_FIELDS = frozenset(
    {
        "preferred_system_id",
        "preferred_system_ids",
        "preference_authority_evidence_id",
        "conceptual_adjudication_evidence_id",
        "conceptual_adjudication_evidence_digest",
    }
)
_PROGRAMME_SUPPORT_FIELDS = frozenset(
    {
        "disposition",
        "theory_programme_id",
        "theoretical_question_id",
        "conceptual_system_ids",
        "theoretical_question",
        "role",
        "why_theory_alone_is_currently_insufficient",
        "possible_theory_updates",
        "receipt_ids",
        "reflective_assimilation_event_ids",
    }
)
_FORMAL_CLAIM_BINDING_FIELDS = frozenset(
    {
        "schema_version",
        "binding_kind",
        "producer_operator_id",
        "producer_request_id",
        "producer_request_digest",
        "producer_receipt_id",
        "producer_receipt_digest",
        "producer_input_digest",
        "consumer_event_id",
        "consumer_event_hash",
        "semantic_row_id",
        "semantic_row_digest",
        "output_id",
        "output_digest",
        "source_theory_generation",
        "conjecture_id",
        "formal_claim_digest",
        "execution_plan_digest",
    }
)


def _conceptual_preference_authority(state: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and retain the sole set-valued conceptual authority.

    A detached ID/digest is deliberately unusable: replayable scheduling carries
    the complete sealed object and binds it to the exact ordered systems and
    reflection rounds that this scheduler consumed.
    """

    forbidden = sorted(_CALLER_PREFERENCE_FIELDS.intersection(state))
    if forbidden:
        raise ContractError(
            "scheduler rejects caller-authored or ID-only conceptual preference fields: "
            f"{forbidden}"
        )
    evidence = state.get("conceptual_adjudication_evidence")
    if evidence is None:
        return {
            "status": "absent_diagnostic_only",
            "evidence": None,
            "preference_set": None,
            "candidate_system_ids": [],
            "conceptual_systems_digest": None,
            "reflection_rounds_digest": None,
            "authority_boundary": (
                "No sealed blind adjudication was supplied. Structural priorities may "
                "route reflection but authorize no preference, promotion, lifecycle "
                "change, or active investment."
            ),
        }
    if not isinstance(evidence, Mapping):
        raise ContractError("conceptual_adjudication_evidence must be a complete object or null")
    run_id = state.get("run_id")
    systems_raw = state.get("conceptual_systems")
    rounds_raw = state.get("reflection_rounds")
    if not isinstance(run_id, str) or not run_id:
        raise ContractError("sealed conceptual preference scheduling requires run_id")
    if not isinstance(systems_raw, list) or not all(
        isinstance(row, Mapping) for row in systems_raw
    ):
        raise ContractError(
            "sealed conceptual preference scheduling requires the exact ordered conceptual_systems"
        )
    if not isinstance(rounds_raw, list) or not all(
        isinstance(row, Mapping) for row in rounds_raw
    ):
        raise ContractError(
            "sealed conceptual preference scheduling requires the exact ordered reflection_rounds"
        )
    systems = [copy.deepcopy(dict(row)) for row in systems_raw]
    rounds = [copy.deepcopy(dict(row)) for row in rounds_raw]
    system_ids = [str(row.get("system_id", "")) for row in systems]
    if not system_ids or any(not system_id for system_id in system_ids):
        raise ContractError("every scheduled conceptual system requires a system_id")
    preference = validate_sealed_preference_authority(
        evidence,
        target_id=str(state["target_id"]),
        run_id=run_id,
        state_version=int(state["state_version"]),
        system_ids=system_ids,
        systems=systems,
        reflection_rounds=rounds,
    )
    decision = str(preference["decision"])
    status = {
        "prefer_unique": "sealed_unique",
        "retain_plural_nondominated": "sealed_plural",
        "revise_all": "sealed_revise_all_diagnostic_only",
    }.get(decision)
    if status is None:
        raise ContractError(f"unsupported sealed conceptual preference decision: {decision}")
    return {
        "status": status,
        "evidence": copy.deepcopy(dict(evidence)),
        "preference_set": copy.deepcopy(preference),
        "candidate_system_ids": system_ids,
        "conceptual_systems_digest": canonical_digest(systems),
        "reflection_rounds_digest": canonical_digest(rounds),
        "authority_boundary": (
            "The embedded sealed blind adjudication is the sole internal conceptual "
            "preference authority. It grants no proof, empirical, external-validation, "
            "source-truth, theorem, mass-gap, or other physics-result authority."
        ),
    }


def _branch_conceptual_system_ids(branch: Mapping[str, Any]) -> list[str]:
    """Return the exact plural candidate binding for one scheduled branch."""

    forbidden = sorted(_CALLER_PREFERENCE_FIELDS.intersection(branch))
    if forbidden:
        raise ContractError(
            "scheduler branch rejects caller-authored conceptual preference fields: "
            f"{forbidden}"
        )
    if "conceptual_system_id" in branch:
        raise ContractError(
            "scheduler branch conceptual identity must use plural conceptual_system_ids"
        )
    raw = branch.get("conceptual_system_ids", [])
    if not isinstance(raw, list) or not all(isinstance(value, str) and value for value in raw):
        raise ContractError("branch conceptual_system_ids must be a list of non-empty strings")
    if len(raw) != len(set(raw)):
        raise ContractError("branch conceptual_system_ids must be unique")
    return sorted(raw)


def _score(value: Any) -> float:
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return max(0.0, min(1.0, float(value)))
    return 0.0


def priority_vector(branch: Mapping[str, Any]) -> dict[str, float]:
    """Build a transparent objective vector; no weighted scalar is produced."""

    virtues = branch.get("theory_virtues", {}) if isinstance(branch.get("theory_virtues"), Mapping) else {}
    cost = max(0.0, float(branch.get("estimated_cost", 0.0)))
    closure_risk = _score(branch.get("premature_closure_risk", 0.0))
    plateau = max(0, int(branch.get("equivalent_output_count", 0)))
    return {
        "essential_relevance": _score(virtues.get("essential_relevance", branch.get("essential_relevance"))),
        "root_tension_contact": _score(virtues.get("root_tension_contact")),
        "expected_understanding_gain": max(0.0, _score(virtues.get("expected_understanding_gain")) - min(0.5, 0.1 * plateau)),
        "expected_unification_gain": _score(virtues.get("expected_unification_gain")),
        "conceptual_fertility": max(0.0, _score(virtues.get("conceptual_fertility")) - min(0.4, 0.08 * plateau)),
        "programme_impact": _score(virtues.get("programme_impact")),
        "maturity": _score(virtues.get("maturity")),
        "cost_efficiency": 1.0 / (1.0 + cost),
        "closure_safety": 1.0 - closure_risk,
    }


def _dominates(left: Mapping[str, float], right: Mapping[str, float]) -> bool:
    return all(left[key] >= right[key] for key in _VIRTUES) and any(left[key] > right[key] for key in _VIRTUES)


def pareto_layers(branches: Sequence[Mapping[str, Any]]) -> list[list[Mapping[str, Any]]]:
    """Return deterministic non-dominated layers without collapsing objectives."""

    remaining = list(branches)
    layers: list[list[Mapping[str, Any]]] = []
    while remaining:
        front = [
            candidate
            for candidate in remaining
            if not any(
                other is not candidate and _dominates(priority_vector(other), priority_vector(candidate))
                for other in remaining
            )
        ]
        front.sort(key=lambda row: str(row.get("branch_id")))
        layers.append(front)
        front_ids = {id(row) for row in front}
        remaining = [row for row in remaining if id(row) not in front_ids]
    return layers


def _action(
    kind: str,
    *,
    state_version: int,
    target_id: str,
    branch_ids: Sequence[str] = (),
    depends_on: Sequence[str] = (),
    rationale: Sequence[str],
    priority_class: str,
    restrictions: Sequence[str] = (),
    payload: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if kind not in ACTION_KINDS:
        raise ContractError(f"unknown discovery action kind: {kind}")
    branch_ids = sorted(set(branch_ids))
    identity_material = {
        "kind": kind,
        "target_id": target_id,
        "state_version": state_version,
        "branch_ids": branch_ids,
        "depends_on": sorted(set(depends_on)),
        "payload": payload or {},
    }
    return {
        "action_id": stable_identifier("action", identity_material),
        "kind": kind,
        "target_id": target_id,
        "state_version": state_version,
        "branch_ids": branch_ids,
        "depends_on": sorted(set(depends_on)),
        "rationale": list(rationale),
        "priority_class": priority_class,
        "restrictions": list(restrictions),
        "payload": dict(payload or {}),
        "status": "pending",
        "consumed_at": None,
        "consumer_receipt_id": None,
    }


def _literature_lane(state: Mapping[str, Any]) -> tuple[list[dict[str, Any]], bool]:
    target_id = str(state.get("target_id", ""))
    version = int(state.get("state_version", 0))
    literature = state.get("literature", {}) if isinstance(state.get("literature"), Mapping) else {}
    status = literature.get("status", "missing")
    snapshot_id = literature.get("snapshot_id")
    assimilated = literature.get("assimilated_snapshot_id")
    actions: list[dict[str, Any]] = []
    blocked = status != "validated_current" or not snapshot_id or snapshot_id != assimilated
    previous_id = None
    if status != "validated_current" or not snapshot_id:
        refresh = _action(
            "refresh_literature",
            state_version=version,
            target_id=target_id,
            rationale=["active investment requires a current target-scoped validated search snapshot"],
            priority_class="hard_gate",
            payload={"claim_scope": literature.get("claim_scope"), "supersedes": snapshot_id},
        )
        actions.append(refresh)
        previous_id = refresh["action_id"]
    if not snapshot_id or snapshot_id != assimilated or status != "validated_current":
        assimilate = _action(
            "assimilate",
            state_version=version,
            target_id=target_id,
            depends_on=[previous_id] if previous_id else [],
            rationale=["source deltas must alter named concepts, hypotheses, genealogy, or actions before selection"],
            priority_class="hard_gate",
            payload={"snapshot_id": snapshot_id or "produced_by_refresh", "previous_assimilated_snapshot_id": assimilated},
        )
        actions.append(assimilate)
        rebase = _action(
            "rebase",
            state_version=version,
            target_id=target_id,
            branch_ids=[str(row.get("branch_id")) for row in state.get("branches", []) if isinstance(row, Mapping) and row.get("status") not in {"retired", "exhausted"}],
            depends_on=[assimilate["action_id"]],
            rationale=["every survivor must be rebased before synthesis, proof routing, investment, or novelty claims"],
            priority_class="hard_gate",
            payload={"allowed_branch_changes": ["spawn", "merge", "split", "reframe", "demote", "retire", "reprioritize"]},
        )
        actions.append(rebase)
    return actions, blocked


def _programme_support_action(
    state: Mapping[str, Any],
    conceptual_authority: Mapping[str, Any],
    *,
    literature_blocked: bool,
) -> dict[str, Any] | None:
    """Schedule one theory-derived support probe after sealed adjudication.

    This is deliberately programme-level rather than branch-selected.  A
    support experiment may discriminate a registered premise of the already
    preferred set, but it cannot choose that set, promote it, or bypass current
    literature and post-result reflection.
    """

    raw_support = state.get("programme_support_probe")
    if raw_support is None:
        return None
    if not isinstance(raw_support, Mapping) or set(raw_support) != set(
        _PROGRAMME_SUPPORT_FIELDS
    ):
        raise ContractError("programme support probe is not a closed reflective object")
    raw_programme = state.get("theory_programme")
    if not isinstance(raw_programme, Mapping):
        raise ContractError("programme support probe lacks its complete theory programme")
    support = copy.deepcopy(dict(raw_support))
    programme = copy.deepcopy(dict(raw_programme))
    preference = conceptual_authority.get("preference_set")
    preferred_ids = (
        list(preference.get("preferred_system_ids", []))
        if isinstance(preference, Mapping)
        else []
    )
    if literature_blocked:
        raise ContractError(
            "programme support probe cannot be scheduled before current literature assimilation"
        )
    if (
        conceptual_authority.get("status")
        not in {"sealed_unique", "sealed_plural"}
        or not preferred_ids
        or programme.get("authority_status") != conceptual_authority.get("status")
        or programme.get("investment_authorized") is not True
        or list(programme.get("conceptual_system_ids", [])) != preferred_ids
        or support.get("disposition") not in {"proposed", "commissioned"}
        or support.get("theory_programme_id") != programme.get("programme_id")
        or list(support.get("conceptual_system_ids", [])) != preferred_ids
        or support.get("role") == "none"
        or not isinstance(support.get("theoretical_question_id"), str)
        or not support["theoretical_question_id"].strip()
        or not isinstance(support.get("theoretical_question"), str)
        or not support["theoretical_question"].strip()
        or not isinstance(
            support.get("why_theory_alone_is_currently_insufficient"), str
        )
        or not support["why_theory_alone_is_currently_insufficient"].strip()
    ):
        raise ContractError(
            "programme support probe is not bound to the complete sealed preferred set"
        )
    return _action(
        "probe",
        state_version=int(state["state_version"]),
        target_id=str(state["target_id"]),
        rationale=[
            "the sealed preferred theory programme generated one mature discriminating support question",
            "the experiment is secondary and may request later reflective premise revision only",
        ],
        priority_class="theory_subordinate_support",
        restrictions=[
            "no_automatic_theory_selection",
            "no_direct_proof_authority",
            "no_direct_physics_result_authority",
            "requires_post_result_reflection",
        ],
        payload={
            "theory_programme_id": programme["programme_id"],
            "theory_programme_digest": canonical_digest(programme),
            "conceptual_system_ids": preferred_ids,
            "theoretical_question_id": support["theoretical_question_id"],
            "theoretical_question": support["theoretical_question"],
            "probe_role": support["role"],
            "why_theory_alone_is_currently_insufficient": support[
                "why_theory_alone_is_currently_insufficient"
            ],
            "possible_theory_updates": copy.deepcopy(
                support["possible_theory_updates"]
            ),
            "experiment_role": "secondary_theory_support_only",
            "permitted_direct_effect": "none",
        },
    )


def _branch_active(branch: Mapping[str, Any]) -> bool:
    status = branch.get("status", "incubating")
    if status in {"quarantined", "exhausted", "falsified", "retired", "complete"}:
        return bool(branch.get("reactivation_event_id"))
    return status not in {"operational_failure"}


def _dependencies_met(branch: Mapping[str, Any], by_id: Mapping[str, Mapping[str, Any]]) -> bool:
    for dependency in branch.get("depends_on", []):
        row = by_id.get(str(dependency))
        if row is None or row.get("status") not in {"validated", "proof_ready", "complete", "supported"}:
            return False
    return True


def _next_theory_action(branch: Mapping[str, Any], plateau_limit: int) -> tuple[str, list[str]]:
    repeats = int(branch.get("equivalent_output_count", 0))
    status = branch.get("status", "incubating")
    maturity = branch.get("maturity", "incubating")
    requested = branch.get("requested_action")
    probe_decision = branch.get("probe_decision", "commission")
    question_maturity = branch.get("theoretical_question_maturity", "immature")
    if repeats >= plateau_limit + 1:
        return "retire", ["semantic plateau exceeded the configured pivot allowance"]
    if repeats >= plateau_limit:
        return "reframe", ["materially equivalent outputs triggered a semantic pivot"]
    if status == "proof_ready" or maturity == "proof_ready":
        return "prove", ["formal obligations and provenance are ready for a proof continuation"]
    if requested == "probe":
        if probe_decision == "no_probe_needed":
            return "reflect", ["the theory has no support-probe need; continue conceptual work"]
        if question_maturity not in {"mature", "formalization_ready"}:
            return "formalize", ["the support question is not precise enough to test; formalize it first"]
        return "probe", ["a mature theory generated an exact discriminating support question"]
    if maturity == "formalization_ready":
        return "formalize", ["conceptual structure is ready to become typed definitions and obligations"]
    if maturity == "mature" and branch.get("synthesis_candidate"):
        return "synthesize", ["a mature branch exposes a conflict-preserving synthesis opportunity"]
    if branch.get("unresolved_dissent"):
        return "differentiate", ["unresolved dissent must be preserved and clarified before convergence"]
    if branch.get("needs_reading"):
        return "read", ["a named theoretical uncertainty calls for targeted reading"]
    return "reflect", ["reflection has the highest expected conceptual information gain at this maturity"]


def _independent(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    left_id, right_id = str(left.get("branch_id")), str(right.get("branch_id"))
    if right_id in left.get("depends_on", []) or left_id in right.get("depends_on", []):
        return False
    left_overlap = set(left.get("overlap_with", []))
    right_overlap = set(right.get("overlap_with", []))
    if right_id in left_overlap or left_id in right_overlap:
        return False
    return True


def propagate_evidence_priorities(state: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Emit an update for every route touched by newly validated evidence."""

    updates: list[dict[str, Any]] = []
    events = [row for row in state.get("new_evidence", []) if isinstance(row, Mapping) and row.get("validated")]
    for branch in state.get("branches", []):
        if not isinstance(branch, Mapping):
            continue
        dependencies = set(str(value) for value in branch.get("dependency_ids", []))
        for event in events:
            affected = dependencies.intersection(str(value) for value in event.get("affected_dependency_ids", []))
            if affected:
                updates.append(
                    {
                        "branch_id": str(branch.get("branch_id")),
                        "evidence_id": str(event.get("evidence_id")),
                        "affected_dependency_ids": sorted(affected),
                        "direction": event.get("direction", "reassess"),
                    }
                )
    return updates


def schedule_discovery_actions(state: Mapping[str, Any]) -> dict[str, Any]:
    """Create replayable theoretical action waves from durable epistemic state."""

    if not state.get("target_id"):
        raise ContractError("scheduler state requires target_id")
    version = state.get("state_version")
    if isinstance(version, bool) or not isinstance(version, int) or version < 0:
        raise ContractError("scheduler state requires a non-negative state_version")
    target_id = str(state["target_id"])
    conceptual_authority = _conceptual_preference_authority(state)
    preference_set = conceptual_authority.get("preference_set")
    preferred_system_ids = set(
        str(value)
        for value in (
            preference_set.get("preferred_system_ids", [])
            if isinstance(preference_set, Mapping)
            else []
        )
    )
    candidate_system_ids = set(conceptual_authority["candidate_system_ids"])
    branches = [dict(row) for row in state.get("branches", []) if isinstance(row, Mapping)]
    branch_ids = [str(row.get("branch_id", "")) for row in branches]
    if any(not branch_id for branch_id in branch_ids) or len(branch_ids) != len(
        set(branch_ids)
    ):
        raise ContractError("scheduler branches require unique non-empty branch_id values")
    by_id = {str(row.get("branch_id")): row for row in branches}
    conceptual_ids_by_branch: dict[str, list[str]] = {}
    for branch in branches:
        branch_id = str(branch["branch_id"])
        bound_ids = _branch_conceptual_system_ids(branch)
        if conceptual_authority["evidence"] is not None and not set(bound_ids).issubset(
            candidate_system_ids
        ):
            raise ContractError(
                f"branch {branch_id} references conceptual systems outside the sealed candidate set"
            )
        conceptual_ids_by_branch[branch_id] = bound_ids
    actions, literature_blocked = _literature_lane(state)

    programme_support = _programme_support_action(
        state,
        conceptual_authority,
        literature_blocked=literature_blocked,
    )
    if programme_support is not None:
        actions.append(programme_support)

    required_corners = set(str(value) for value in state.get("required_conceptual_corners", []))
    represented_corners = {str(row.get("conceptual_corner")) for row in branches if _branch_active(row)}
    missing_corners = sorted(required_corners - represented_corners)
    if missing_corners:
        forge = _action(
            "forge_high_risk",
            state_version=version,
            target_id=target_id,
            depends_on=[actions[-1]["action_id"]] if actions else [],
            rationale=["conceptual-corner coverage constraint protects high-upside routes from scalar plausibility pruning"],
            priority_class="portfolio_constraint",
            payload={"missing_conceptual_corners": missing_corners, "separate_truth_confidence_from_value_if_right": True},
        )
        actions.append(forge)

    active = [row for row in branches if _branch_active(row) and _dependencies_met(row, by_id)]
    active_ids = {str(row.get("branch_id")) for row in active}
    formal_bound = [
        row for row in branches if row.get("formal_claim_binding") is not None
    ]
    if len(formal_bound) > 1:
        raise ContractError(
            "scheduler v1 accepts at most one registered formal-claim binding"
        )
    for branch in formal_bound:
        branch_id = str(branch.get("branch_id"))
        if branch_id not in active_ids:
            raise ContractError(
                "registered formal-claim binding names an inactive or dependency-blocked branch"
            )
        if (
            branch.get("status") != "proof_ready"
            and branch.get("maturity") != "proof_ready"
        ):
            raise ContractError(
                "registered formal-claim binding requires a proof-ready branch"
            )
    layers = pareto_layers(active) if active else []
    selected = list(layers[0]) if layers else []
    # Preserve two wildcards when the active portfolio contains them.  This is
    # a cardinality constraint outside the Pareto order: one strong incumbent
    # must not be able to collapse both independent high-upside probes.
    protected = sorted(
        (row for row in active if row.get("protected_wildcard")),
        key=lambda row: str(row.get("branch_id")),
    )
    selected_ids = {str(row.get("branch_id")) for row in selected}
    protected_selected = sum(
        str(row.get("branch_id")) in selected_ids for row in protected
    )
    for wildcard in protected:
        if protected_selected >= min(2, len(protected)):
            break
        wildcard_id = str(wildcard.get("branch_id"))
        if wildcard_id not in selected_ids:
            selected.append(wildcard)
            selected_ids.add(wildcard_id)
            protected_selected += 1
    # A sealed ready formal claim is an already-authorized downstream
    # continuation, not another theory-virtue contender.  Pareto ranking may
    # order conceptual investment, but it cannot erase the exact proof action
    # authorized by the committed producer output.
    for branch in sorted(formal_bound, key=lambda row: str(row.get("branch_id"))):
        branch_id = str(branch.get("branch_id"))
        if branch_id not in selected_ids:
            selected.append(branch)
            selected_ids.add(branch_id)
    selected.sort(key=lambda row: str(row.get("branch_id")))
    plateau_limit = int(state.get("semantic_plateau_limit", 3))

    branch_actions: list[dict[str, Any]] = []
    prompt_digests: set[str] = set()
    gate_dependency = [actions[-1]["action_id"]] if literature_blocked and actions else []
    for branch in selected:
        branch_id = str(branch.get("branch_id"))
        if not branch_id:
            continue
        kind, reasons = _next_theory_action(branch, plateau_limit)
        requested_kind = kind
        prompt_digest = str(branch.get("semantic_prompt_digest") or canonical_digest(branch.get("question", branch_id)))
        formal_claim_binding = branch.get("formal_claim_binding")
        prompt_identity = (
            canonical_digest(
                {
                    "semantic_prompt_digest": prompt_digest,
                    "formal_claim_binding": formal_claim_binding,
                }
            )
            if formal_claim_binding is not None
            else prompt_digest
        )
        if prompt_identity in prompt_digests:
            continue
        prompt_digests.add(prompt_identity)
        vector = priority_vector(branch)
        bound_system_ids = conceptual_ids_by_branch[branch_id]
        authorized_system_ids = sorted(preferred_system_ids.intersection(bound_system_ids))
        restrictions: set[str] = set()
        preference_applied = False
        if conceptual_authority["status"] == "absent_diagnostic_only":
            restrictions.update(
                {"conceptual_preference_unsealed", "no_promotion", "no_active_investment"}
            )
        elif conceptual_authority["status"] == "sealed_revise_all_diagnostic_only":
            restrictions.update(
                {"sealed_revise_all", "no_promotion", "no_active_investment"}
            )

        if kind == "synthesize" and conceptual_authority["status"] == "sealed_plural":
            kind = "differentiate"
            reasons = [
                "the sealed plural nondominated set authorizes equal continuation, not an automatic synthesis or singular winner"
            ]
            restrictions.add("no_automatic_synthesis")
        elif kind in _PREFERENCE_SENSITIVE_ACTIONS:
            if not authorized_system_ids:
                kind = "incubate"
                if conceptual_authority["status"] == "absent_diagnostic_only":
                    reasons = [
                        "active investment and lifecycle change require the complete sealed blind conceptual adjudication"
                    ]
                elif conceptual_authority["status"] == "sealed_revise_all_diagnostic_only":
                    reasons = [
                        "the sealed adjudication requires revision of every candidate; it authorizes diagnosis but no active investment"
                    ]
                else:
                    reasons = [
                        "this branch has no candidate in the sealed set-valued conceptual preference"
                    ]
                restrictions.update({"no_promotion", "no_active_investment"})
            else:
                preference_applied = True

        if literature_blocked and kind not in {"reflect", "reframe", "differentiate", "incubate"}:
            kind = "incubate"
            reasons = ["active investment is blocked until target literature refresh, assimilation, and rebase complete"]
            preference_applied = False
        if literature_blocked:
            restrictions.update(
                {"literature_blind", "no_novelty_claim", "no_promotion", "no_active_investment"}
            )
        if formal_claim_binding is not None and kind != "prove":
            raise ContractError(
                "a registered ready formal claim was denied its exact prove action"
            )
        action_payload = {
            "priority_vector": vector,
            "conceptual_corner": branch.get("conceptual_corner"),
            "semantic_prompt_digest": prompt_digest,
            "requested_kind": requested_kind,
            "conceptual_system_ids": bound_system_ids,
            "sealed_preference_intersection": authorized_system_ids,
            "conceptual_preference_applied": preference_applied,
        }
        if kind == "prove":
            if (
                not isinstance(formal_claim_binding, Mapping)
                or set(formal_claim_binding) != _FORMAL_CLAIM_BINDING_FIELDS
                or any(
                    formal_claim_binding.get(field) in {None, ""}
                    for field in _FORMAL_CLAIM_BINDING_FIELDS
                )
            ):
                raise ContractError(
                    "prove action requires one exact registered formal-claim binding"
                )
            validate_instance(
                dict(formal_claim_binding),
                "discovery_formal_claim_schedule_binding_v1.schema.json",
            )
            action_payload["formal_claim_binding"] = copy.deepcopy(
                dict(formal_claim_binding)
            )
        action = _action(
            kind,
            state_version=version,
            target_id=target_id,
            branch_ids=[branch_id],
            depends_on=gate_dependency if kind not in {"incubate", "retire"} else [],
            rationale=reasons + ["selected on a non-dominated theory-virtue front; no scalar score was used"],
            priority_class=(
                "registered_formal_claim_continuation"
                if formal_claim_binding is not None
                else "protected_wildcard"
                if branch.get("protected_wildcard")
                else "pareto_front"
            ),
            restrictions=sorted(restrictions),
            payload=action_payload,
        )
        branch_actions.append(action)

    formal_action_branch_ids = [
        action["branch_ids"][0]
        for action in branch_actions
        if action["kind"] == "prove"
    ]
    expected_formal_branch_ids = sorted(
        str(branch["branch_id"]) for branch in formal_bound
    )
    if sorted(formal_action_branch_ids) != expected_formal_branch_ids:
        raise ContractError(
            "registered formal claims and scheduled prove actions are not bijective"
        )

    actions.extend(branch_actions)
    # Dependency-aware parallel waves: only mutually independent, uniquely
    # prompted actions appear in the same wave.
    waves: list[dict[str, Any]] = []
    hard_gate_ids = [row["action_id"] for row in actions if row["priority_class"] == "hard_gate"]
    for action_id in hard_gate_ids:
        waves.append({"wave_id": stable_identifier("wave", action_id), "mode": "serial_gate", "action_ids": [action_id]})
    pending = list(branch_actions)
    while pending:
        seed = pending.pop(0)
        wave = [seed]
        seed_branch = by_id.get(seed["branch_ids"][0], {})
        remainder = []
        for candidate in pending:
            candidate_branch = by_id.get(candidate["branch_ids"][0], {})
            if all(_independent(candidate_branch, by_id.get(member["branch_ids"][0], {})) for member in wave):
                wave.append(candidate)
            else:
                remainder.append(candidate)
        pending = remainder
        mode = "parallel" if len(wave) > 1 else "serial"
        waves.append({"wave_id": stable_identifier("wave", [row["action_id"] for row in wave]), "mode": mode, "action_ids": [row["action_id"] for row in wave]})
    nonbranch = [row for row in actions if row not in branch_actions and row["priority_class"] != "hard_gate"]
    for row in nonbranch:
        waves.append({"wave_id": stable_identifier("wave", row["action_id"]), "mode": "serial_constraint", "action_ids": [row["action_id"]]})

    schedule = {
        "scheduler_version": "discovery-information-scheduler/2.0.0",
        "target_id": target_id,
        "state_version": version,
        "input_digest": canonical_digest(state),
        "schedule_id": stable_identifier("schedule", target_id, version, canonical_digest(state)),
        "literature_investment_blocked": literature_blocked,
        "conceptual_preference_authority": conceptual_authority,
        "actions": actions,
        "waves": waves,
        "pareto_layers": [[str(row.get("branch_id")) for row in layer] for layer in layers],
        "priority_updates": propagate_evidence_priorities(state),
        "created_at": utc_now(),
        "consumption_log": [],
    }
    schedule["schedule_digest"] = canonical_digest(schedule, exclude_keys=("schedule_digest", "created_at", "consumption_log"))
    return schedule


def consume_action(schedule: Mapping[str, Any], action_id: str, *, expected_state_version: int, consumer_receipt_id: str) -> dict[str, Any]:
    """Consume a next-action record once under an explicit state-version CAS."""

    if schedule.get("state_version") != expected_state_version:
        raise ContractError("stale scheduler state version")
    updated = copy.deepcopy(dict(schedule))
    matches = [row for row in updated.get("actions", []) if row.get("action_id") == action_id]
    if len(matches) != 1:
        raise ContractError("action_id is missing or non-unique")
    action = matches[0]
    if action.get("status") != "pending":
        raise ContractError("action has already been consumed")
    completed = {row.get("action_id") for row in updated.get("actions", []) if row.get("status") == "consumed"}
    missing = set(action.get("depends_on", [])) - completed
    if missing:
        raise ContractError(f"action dependencies are not consumed: {sorted(missing)}")
    consumed_at = utc_now()
    action["status"] = "consumed"
    action["consumed_at"] = consumed_at
    action["consumer_receipt_id"] = consumer_receipt_id
    updated.setdefault("consumption_log", []).append(
        {"action_id": action_id, "consumer_receipt_id": consumer_receipt_id, "consumed_at": consumed_at, "state_version": expected_state_version}
    )
    # ``schedule_digest`` identifies the frozen pre-consumption schedule.  A
    # distinct digest is required after mutation so callers never mislabel the
    # source digest as the identity of the consumed queue.
    updated["consumed_schedule_digest"] = canonical_digest(
        updated,
        exclude_keys=("consumed_schedule_digest", "created_at"),
    )
    return updated


def consume_action_file(path: Path | str, action_id: str, *, expected_state_version: int, consumer_receipt_id: str) -> dict[str, Any]:
    """Durably consume an action in a standalone queue under a file CAS lock."""

    schedule_path = Path(path)
    lock_path = schedule_path.with_suffix(schedule_path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        current = json.loads(schedule_path.read_text(encoding="utf-8"))
        updated = consume_action(current, action_id, expected_state_version=expected_state_version, consumer_receipt_id=consumer_receipt_id)
        temporary = schedule_path.with_suffix(schedule_path.suffix + f".{os.getpid()}.tmp")
        with temporary.open("w", encoding="utf-8") as stream:
            stream.write(json.dumps(updated, indent=2, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, schedule_path)
        directory_fd = os.open(schedule_path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
        return updated


def consume_action_transaction(
    store: Any,
    schedule: Mapping[str, Any],
    action_id: str,
    *,
    expected_generation: int,
    consumer_receipt_id: str,
) -> tuple[dict[str, Any], Any]:
    """Commit one consumed action through ``DiscoveryTransactionStore``.

    The schedule remains bound to the frozen epistemic state from which it was
    derived; the enclosing canonical state advances by one transaction
    generation.  Reusing the same action/receipt pair is idempotent, while a
    competing generation fails the store's compare-and-swap.
    """

    from agentic.discovery.contracts import Namespace
    from agentic.state.discovery_transaction import CommitArtifact, DiscoveryTransactionStore

    if not isinstance(store, DiscoveryTransactionStore):
        raise ContractError("consume_action_transaction requires DiscoveryTransactionStore")
    current = store.read_state()
    if current is None:
        raise ContractError("cannot consume an action before canonical state initialization")
    schedule_version = int(schedule.get("state_version", -1))
    updated = consume_action(
        schedule,
        action_id,
        expected_state_version=schedule_version,
        consumer_receipt_id=consumer_receipt_id,
    )
    action = next(row for row in updated["actions"] if row["action_id"] == action_id)
    branch_ids = action.get("branch_ids", [])
    branch_id = str(branch_ids[0]) if len(branch_ids) == 1 else "control"
    next_state = copy.deepcopy(current)
    next_state["generation"] = expected_generation + 1
    next_state["next_action_schedule"] = updated
    next_state["last_consumed_action"] = {
        "action_id": action_id,
        "consumer_receipt_id": consumer_receipt_id,
        "source_state_version": schedule_version,
    }
    artifact_payload = json.dumps(updated, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n"
    request_digest = canonical_digest(
        {
            "action_id": action_id,
            "consumer_receipt_id": consumer_receipt_id,
            "schedule_digest": schedule.get("schedule_digest"),
            "expected_generation": expected_generation,
        }
    )
    result = store.commit(
        expected_generation=expected_generation,
        state=next_state,
        artifacts=(
            CommitArtifact(
                relative_path=f"branches/{branch_id}/scheduler/{action_id}.json",
                content=artifact_payload,
                namespace=Namespace(
                    target_id=store.target_id,
                    run_id=store.run_id,
                    branch_id=branch_id,
                    state_version=expected_generation,
                ),
            ),
        ),
        idempotency_key=stable_identifier("consume", action_id, consumer_receipt_id),
        request_digest=request_digest,
    )
    return updated, result


def reserve_actions_transaction(
    store: Any,
    schedule: Mapping[str, Any],
    action_ids: Sequence[str],
    *,
    expected_generation: int,
    consumer_receipt_id: str,
    source_cycle_id: str,
    source_commit_id: str,
    consume_before: str,
    allowed_action_kinds: Sequence[str],
    temporal_evaluation: Mapping[str, Any],
) -> tuple[dict[str, Any], Any, dict[str, Any]]:
    """Atomically reserve one exact compatibility action set in canonical state.

    Verification and use cannot share a long-running filesystem lock.  This
    short CAS transition closes that gap: every selected action is consumed in
    one updated schedule, and hash-chained reservation events advance the
    canonical epistemic state before any downstream investment begins. The
    caller supplies digest-bound local-process temporal evidence; this function
    never performs a second, potentially divergent wall-clock read. A competing
    consumer or superseding theory commit necessarily wins the same generation
    CAS and makes this reservation fail.
    """

    from agentic.state.discovery_transaction import CommitArtifact, DiscoveryTransactionStore

    if not isinstance(store, DiscoveryTransactionStore):
        raise ContractError("reserve_actions_transaction requires DiscoveryTransactionStore")
    if isinstance(expected_generation, bool) or not isinstance(expected_generation, int):
        raise ContractError("reservation expected_generation must be an integer")
    consumer_receipt_id = validate_identifier(consumer_receipt_id, "consumer_receipt_id")
    source_cycle_id = validate_identifier(source_cycle_id, "source_cycle_id")
    source_commit_id = validate_identifier(source_commit_id, "source_commit_id")
    normalized_action_ids = sorted(
        {validate_identifier(str(action_id), "action_id") for action_id in action_ids}
    )
    if not normalized_action_ids or len(normalized_action_ids) != len(action_ids):
        raise ContractError("reservation requires a non-empty unique action set")
    if not isinstance(temporal_evaluation, Mapping):
        raise ContractError("reservation requires governed local temporal evidence")
    clock_authority = temporal_evaluation.get("clock_authority")
    if not isinstance(clock_authority, Mapping):
        raise ContractError("reservation temporal evidence lacks clock authority")
    if (
        clock_authority.get("authority_digest")
        != canonical_digest(clock_authority, exclude_keys=("authority_digest",))
        or temporal_evaluation.get("clock_authority_digest")
        != clock_authority.get("authority_digest")
        or temporal_evaluation.get("authentication_status")
        != "governed_local_process_time_not_externally_authenticated"
    ):
        raise ContractError("reservation temporal authority evidence is invalid")
    try:
        deadline = dt.datetime.fromisoformat(str(consume_before).replace("Z", "+00:00"))
        evaluated_at = dt.datetime.fromisoformat(
            str(temporal_evaluation.get("evaluated_at")).replace("Z", "+00:00")
        )
    except (TypeError, ValueError) as exc:
        raise ContractError("reservation temporal evidence is not ISO date-time") from exc
    if deadline.tzinfo is None or evaluated_at.tzinfo is None:
        raise ContractError("reservation temporal evidence must be timezone-aware")
    if evaluated_at.astimezone(dt.timezone.utc) > deadline.astimezone(dt.timezone.utc):
        raise ContractError("canonical action authorization passed its consume-before deadline")

    current = store.read_state(expected_generation)
    if current is None:
        raise ContractError("cannot reserve actions before canonical state initialization")
    if store.current_generation() != expected_generation:
        raise ContractError("canonical state changed before action reservation")
    if schedule.get("state_version") != expected_generation - 1:
        raise ContractError("schedule is not bound to the source theory transition")
    if schedule.get("target_id") != store.target_id:
        raise ContractError("schedule target does not match reservation store")
    allowed = set(allowed_action_kinds)
    actions_by_id = {
        str(action.get("action_id")): action
        for action in schedule.get("actions", [])
        if isinstance(action, Mapping) and action.get("action_id")
    }
    selected_actions = []
    for action_id in normalized_action_ids:
        action = actions_by_id.get(action_id)
        if action is None:
            raise ContractError(f"reservation action is absent from the schedule: {action_id}")
        if action.get("kind") not in allowed:
            raise ContractError(
                f"reservation action kind is not authorized for this consumer: {action.get('kind')}"
            )
        if action.get("status") != "pending":
            raise ContractError(f"reservation action is not pending: {action_id}")
        selected_actions.append(dict(action))

    updated = copy.deepcopy(dict(schedule))
    pending_ids = set(normalized_action_ids)
    while pending_ids:
        progress = False
        for action_id in sorted(pending_ids):
            action = actions_by_id[action_id]
            dependencies = set(action.get("depends_on", []))
            already_consumed = {
                row.get("action_id")
                for row in updated.get("actions", [])
                if row.get("status") == "consumed"
            }
            if dependencies - already_consumed - (set(normalized_action_ids) - pending_ids):
                continue
            updated = consume_action(
                updated,
                action_id,
                expected_state_version=int(schedule["state_version"]),
                consumer_receipt_id=consumer_receipt_id,
            )
            pending_ids.remove(action_id)
            progress = True
            break
        if not progress:
            raise ContractError("reservation action dependencies are not jointly satisfiable")

    events: list[dict[str, Any]] = []
    previous_hash = str(current["last_event_hash"])
    for offset, action in enumerate(sorted(selected_actions, key=lambda row: row["action_id"]), 1):
        event = build_event(
            sequence=int(current["event_count"]) + offset,
            previous_event_hash=previous_hash,
            namespace=Namespace(
                store.target_id,
                store.run_id,
                "control",
                expected_generation,
            ),
            event_type="reflection_recorded",
            entity_type="reflection",
            entity_id=stable_identifier(
                "action-reservation", source_commit_id, action["action_id"], consumer_receipt_id
            ),
            payload={
                "kind": "canonical_action_reservation",
                "action_id": action["action_id"],
                "action_kind": action["kind"],
                "branch_ids": list(action.get("branch_ids", [])),
                "schedule_id": schedule["schedule_id"],
                "source_cycle_id": source_cycle_id,
                "source_commit_id": source_commit_id,
                "consumer_receipt_id": consumer_receipt_id,
                "consume_before": consume_before,
                "temporal_evaluation": copy.deepcopy(dict(temporal_evaluation)),
            },
            actor="canonical-compatibility-reservation",
            source_receipt_ids=[consumer_receipt_id],
        )
        events.append(event)
        previous_hash = event["event_hash"]
    next_state = reduce_from_state(current, events)
    reservation = {
        "schema_version": "1.0.0",
        "reservation_id": stable_identifier(
            "reservation", source_commit_id, normalized_action_ids, consumer_receipt_id
        ),
        "target_id": store.target_id,
        "run_id": store.run_id,
        "source_cycle_id": source_cycle_id,
        "source_commit_id": source_commit_id,
        "source_state_generation": expected_generation,
        "reserved_state_generation": expected_generation + 1,
        "schedule_id": schedule["schedule_id"],
        "schedule_digest": schedule["schedule_digest"],
        "consumed_schedule_digest": updated["consumed_schedule_digest"],
        "action_ids": normalized_action_ids,
        "actions": selected_actions,
        "consumer_receipt_id": consumer_receipt_id,
        "consume_before": consume_before,
        "temporal_evaluation": copy.deepcopy(dict(temporal_evaluation)),
        "status": "reserved_before_investment",
        "event_ids": [event["event_id"] for event in events],
    }
    reservation["reservation_digest"] = canonical_digest(reservation)
    request_digest = canonical_digest(
        {
            "reservation_id": reservation["reservation_id"],
            "source_commit_id": source_commit_id,
            "source_state_generation": expected_generation,
            "schedule_digest": schedule["schedule_digest"],
            "consumed_schedule_digest": updated["consumed_schedule_digest"],
            "action_ids": normalized_action_ids,
            "consumer_receipt_id": consumer_receipt_id,
            "consume_before": consume_before,
            "temporal_evaluation_digest": canonical_digest(temporal_evaluation),
        }
    )
    result = store.commit(
        expected_generation=expected_generation,
        state=next_state,
        artifacts=(
            CommitArtifact(
                relative_path=(
                    f"branches/control/reservations/{reservation['reservation_id']}/reservation.json"
                ),
                content=(json.dumps(reservation, indent=2, sort_keys=True) + "\n").encode(),
                namespace=Namespace(
                    store.target_id, store.run_id, "control", expected_generation
                ),
            ),
            CommitArtifact(
                relative_path=(
                    f"branches/control/reservations/{reservation['reservation_id']}/events.json"
                ),
                content=(json.dumps(events, indent=2, sort_keys=True) + "\n").encode(),
                namespace=Namespace(
                    store.target_id, store.run_id, "control", expected_generation
                ),
            ),
        ),
        idempotency_key=stable_identifier(
            "reserve", source_commit_id, normalized_action_ids, consumer_receipt_id
        ),
        request_digest=request_digest,
    )
    return updated, result, reservation
