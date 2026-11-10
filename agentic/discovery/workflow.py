# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Theory-first orchestration for reflective conceptual discovery."""

from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

from agentic.discovery.conceptual_adjudication import (
    ConceptualAdjudicationError,
    validate_sealed_preference_authority,
)
from agentic.discovery.central_conceptual_reflection import (
    CentralConceptualReflectionError,
    build_central_conceptual_route_reflection_intake,
)
from agentic.discovery.contracts import canonical_digest, stable_identifier, utc_now, validate_payload
from agentic.discovery.reflection import (
    build_pareto_assessment,
    default_reflection_rounds,
    incumbent_system,
    system_from_hypothesis,
    validate_packet_invariants,
)


class DiscoveryWorkflowError(ValueError):
    """Raised when a requested conceptual cycle cannot satisfy its stage gates."""


def _parallel_reference(parallel_input: Mapping[str, Any]) -> dict[str, Any]:
    """Project the executable parallel packet into the reflective contract."""

    branch_requests = list(parallel_input.get("branch_requests", []))
    attempt_receipts = list(parallel_input.get("attempt_receipts", []))
    completed = [
        item for item in attempt_receipts if item.get("status") in {"completed", "reused"}
    ]
    failed = [item for item in attempt_receipts if item not in completed]
    merge = parallel_input.get("merge_proposal", {})
    rebase = parallel_input.get("literature_rebase", {})
    reducer = parallel_input.get("reducer_receipt", {})
    rebase_status = parallel_input.get("literature_rebase_status", rebase.get("status", "not_requested"))
    normalized_rebase = {
        "literature_superseded": "superseded",
        "rebase_blocked": "superseded",
    }.get(rebase_status, rebase_status)
    if not branch_requests:
        disposition = "not_needed"
    elif reducer.get("compare_and_swap_status") == "conflict":
        disposition = "merge_conflict"
    elif completed and failed:
        disposition = "partially_valid"
    elif completed and len(completed) == len(attempt_receipts):
        disposition = "rebased" if normalized_rebase == "rebased" else "validated"
    else:
        disposition = "running"
    explicit = parallel_input.get("disposition")
    if explicit is not None:
        disposition = explicit
    return {
        "disposition": disposition,
        "manifest_ref": parallel_input.get(
            "manifest_ref",
            f"portfolio:{parallel_input.get('portfolio_id')}" if branch_requests else None,
        ),
        "frozen_theory_digest": parallel_input.get("base_theory_digest"),
        "frozen_literature_digest": parallel_input.get("literature_snapshot_digest"),
        "branch_ids": list(parallel_input.get("branch_ids", []))
        or [str(item.get("branch_id")) for item in branch_requests],
        "valid_receipt_ids": list(parallel_input.get("valid_receipt_ids", []))
        or [str(item.get("receipt_id")) for item in completed],
        "failed_or_invalid_receipt_ids": list(
            parallel_input.get("failed_or_invalid_receipt_ids", [])
        )
        or [str(item.get("receipt_id")) for item in failed],
        "retained_dissent_ids": list(parallel_input.get("retained_dissent_ids", []))
        or list(merge.get("retained_dissent_ids", [])),
        "literature_rebase_status": normalized_rebase,
        "reducer_receipt_id": parallel_input.get("reducer_receipt_id")
        or reducer.get("reducer_id"),
    }


def _empty_portfolios() -> tuple[dict[str, Any], dict[str, Any]]:
    return (
        {"disposition": "not_requested", "portfolio_ref": None, "corner_families": [], "selected_hypothesis_ids": [], "protected_wildcard_ids": [], "control_hypothesis_ids": [], "literature_rebase_status": "not_requested"},
        {"disposition": "not_needed", "manifest_ref": None, "frozen_theory_digest": None, "frozen_literature_digest": None, "branch_ids": [], "valid_receipt_ids": [], "failed_or_invalid_receipt_ids": [], "retained_dissent_ids": [], "literature_rebase_status": "not_requested", "reducer_receipt_id": None},
    )


def _stable_union(rows: list[list[str]]) -> list[str]:
    """Return an order-preserving union without erasing set membership."""

    return list(dict.fromkeys(value for row in rows for value in row))


def _authority_systems(
    systems: list[dict[str, Any]], system_ids: list[str]
) -> list[dict[str, Any]]:
    """Resolve an ordered authority set without an index-zero convenience path."""

    by_id = {str(system["system_id"]): system for system in systems}
    if len(by_id) != len(systems):
        raise DiscoveryWorkflowError("conceptual system identities must be unique")
    missing = [system_id for system_id in system_ids if system_id not in by_id]
    if missing:
        raise DiscoveryWorkflowError(
            f"conceptual authority references missing systems: {missing}"
        )
    return [by_id[system_id] for system_id in system_ids]


def build_set_indexed_programme(
    *,
    programme_id: str,
    systems: list[dict[str, Any]],
    authority_status: str,
    literature_questions: list[str],
) -> dict[str, Any]:
    """Build one envelope containing an exact programme for every retained system."""

    investment_authorized = authority_status in {"sealed_unique", "sealed_plural"}
    components: list[dict[str, Any]] = []
    for system in systems:
        system_id = str(system["system_id"])
        if investment_authorized:
            next_actions = list(
                dict.fromkeys(
                    [
                        *system["formalization_seeds"],
                        *system["implications_and_new_questions"][:2],
                    ]
                )
            )
        elif authority_status == "sealed_revise_all_diagnostic_only":
            next_actions = [
                f"Revise {system_id}: {condition}"
                for condition in system["correction_conditions"]
            ]
        else:
            next_actions = [
                f"Incubate {system_id}: {condition}"
                for condition in system["correction_conditions"]
            ]
        components.append(
            {
                "component_programme_id": stable_identifier(
                    "programme-component", programme_id, system_id
                ),
                "conceptual_system_id": system_id,
                "investment_authorized": investment_authorized,
                "definitions_to_build": list(system["primitives"]),
                "relations_or_mechanisms_to_formalize": list(
                    system["relations_operations_and_dynamics"]
                ),
                "consequences_to_derive": list(
                    system["implications_and_new_questions"]
                ),
                "proof_or_model_obligations": (
                    list(system["formalization_seeds"])
                    if investment_authorized
                    else []
                ),
                "next_theory_actions": next_actions,
            }
        )
    return {
        "programme_id": programme_id,
        "authority_status": authority_status,
        "conceptual_system_ids": [
            str(component["conceptual_system_id"]) for component in components
        ],
        "investment_authorized": investment_authorized,
        "component_programmes": components,
        "definitions_to_build": _stable_union(
            [component["definitions_to_build"] for component in components]
        ),
        "relations_or_mechanisms_to_formalize": _stable_union(
            [
                component["relations_or_mechanisms_to_formalize"]
                for component in components
            ]
        ),
        "consequences_to_derive": _stable_union(
            [component["consequences_to_derive"] for component in components]
        ),
        "proof_or_model_obligations": _stable_union(
            [component["proof_or_model_obligations"] for component in components]
        ),
        "literature_questions": list(literature_questions),
        "next_theory_actions": _stable_union(
            [component["next_theory_actions"] for component in components]
        ),
    }


def build_set_indexed_understanding_delta(
    *,
    before: str,
    systems: list[dict[str, Any]],
    rounds: list[dict[str, Any]],
    authority_status: str,
) -> dict[str, Any]:
    """Describe internal structural change per system without certifying merit."""

    perspective_shifts = list(
        dict.fromkeys(
            str(row["mutation_or_synthesis"]["operation"]) for row in rounds
        )
    )
    system_deltas = [
        {
            "conceptual_system_id": str(system["system_id"]),
            "before": before,
            "after": str(system["formerly_inexpressible_now_visible"][0]),
            "perspective_shifts": perspective_shifts,
            "explanatory_compressions": [str(system["mechanism_or_principle"])],
            "new_distinctions": list(system["identities_and_differences"]),
            "productive_contradictions": list(system["residual_contradictions"]),
            "remaining_opacity": list(system["correction_conditions"]),
        }
        for system in systems
    ]
    if len(system_deltas) == 1:
        after = system_deltas[0]["after"]
    elif authority_status == "sealed_plural":
        after = "Plural alternatives remain non-reduced: " + " | ".join(
            f"{row['conceptual_system_id']}: {row['after']}" for row in system_deltas
        )
    elif authority_status == "sealed_revise_all_diagnostic_only":
        after = "No candidate earned preference; revision burdens were localized for: " + ", ".join(
            row["conceptual_system_id"] for row in system_deltas
        )
    else:
        after = "A diagnostic candidate localized an internal structural possibility without preference authority: " + " | ".join(
            row["after"] for row in system_deltas
        )
    return {
        "authority_status": authority_status,
        "conceptual_system_ids": [
            row["conceptual_system_id"] for row in system_deltas
        ],
        "authority_distinct_merit_evidence": False,
        "claim_boundary": "internal_correlated_structural_change_only",
        "system_deltas": system_deltas,
        "before": before,
        "after": after,
        "perspective_shifts": perspective_shifts,
        "explanatory_compressions": _stable_union(
            [row["explanatory_compressions"] for row in system_deltas]
        ),
        "new_distinctions": _stable_union(
            [row["new_distinctions"] for row in system_deltas]
        ),
        "productive_contradictions": _stable_union(
            [row["productive_contradictions"] for row in system_deltas]
        ),
        "remaining_opacity": _stable_union(
            [row["remaining_opacity"] for row in system_deltas]
        ),
    }


def default_set_action(
    systems: list[dict[str, Any]], authority_status: str
) -> dict[str, str]:
    """Choose an action for a set, never by silently selecting its first member."""

    system_ids = [str(system["system_id"]) for system in systems]
    if authority_status == "sealed_unique":
        return {
            "kind": "formalize",
            "question": str(systems[0]["implications_and_new_questions"][0]),
            "expected_conceptual_change": "Turn the uniquely retained mediation candidate into explicit definitions and correction-exposing consequences.",
        }
    if authority_status == "sealed_plural":
        return {
            "kind": "compare",
            "question": "Which predeclared discriminants separate the equally retained systems "
            + ", ".join(system_ids)
            + " without erasing their preserved differences?",
            "expected_conceptual_change": "Differentiate the plural nondominated set while preserving equal investment authority.",
        }
    if authority_status == "sealed_revise_all_diagnostic_only":
        return {
            "kind": "reframe",
            "question": "Which shared inadequacy requires every candidate to be revised before investment?",
            "expected_conceptual_change": "Produce materially revised candidates; no existing diagnostic system is promoted.",
        }
    return {
        "kind": "incubate",
        "question": "What correction would turn the diagnostic structural candidate into an adjudicable alternative?",
        "expected_conceptual_change": "Improve the diagnostic candidate without granting preference or investment authority.",
    }


def _not_conceptual_packet(request: Mapping[str, Any]) -> dict[str, Any]:
    charter = copy.deepcopy(request["discovery_charter"])
    high_risk, parallel = _empty_portfolios()
    action = str(request.get("ordinary_handoff", "derive"))
    if action not in {"derive", "prove", "read", "empirical"}:
        action = "derive"
    packet: dict[str, Any] = {
        "schema_version": "1.0.0", "packet_id": stable_identifier("discovery", request["target_id"], request["run_id"], request["state_version"], "not_conceptual"),
        "target_id": request["target_id"], "run_id": request["run_id"], "branch_id": request.get("branch_id", "root"), "state_version": request["state_version"],
        "prior_conceptual_state_ref": request.get("prior_conceptual_state_ref", f"state:{request['state_version']}"),
        "discovery_charter": charter, "conceptual_genealogy": copy.deepcopy(request["conceptual_genealogy"]),
        "literature_basis": copy.deepcopy(request.get("literature_basis", {"selected_snapshot_id": None, "snapshot_target_id": None, "selected_snapshot_digest": None, "search_completed_utc": None, "freshness_status": "refresh_required", "search_receipt_ids": [], "assimilation_packet_ref": None, "source_to_theory_delta_summary": [], "literature_generated_questions": [], "coverage_limitations": ["Conceptual workflow not entered."], "superseded_snapshot_ids": []})),
        "root_tensions": copy.deepcopy(request.get("root_tensions", [])), "conceptual_systems": [], "high_risk_hypothesis_portfolio": high_risk, "parallel_portfolio": parallel,
        "reflection_rounds": [], "provisional_synthesis": {"authority_status": "not_conceptual", "investment_authorized": False, "preferred_system_id": None, "preferred_system_ids": [], "diagnostic_synthesis_system_ids": [], "nondominated_system_ids": [], "preference_authority_evidence_id": None, "retained_challenger_ids": [], "stable_conceptual_core": [], "unresolved_dissent": [], "why_not_premature_convergence": "The bottleneck is not conceptual; no conceptual convergence was attempted."},
        "theory_quality_pareto": {"dimension_definitions": ["essential_relevance", "root_tension_contact", "conceptual_depth", "explanatory_understanding", "unification_power", "preservation_of_difference", "generativity", "coherence", "truth_aptness"], "system_assessments": [], "nondominated_system_ids": [], "dominated_or_demoted_systems": []},
        "understanding_delta": {"authority_status": "not_conceptual", "conceptual_system_ids": [], "authority_distinct_merit_evidence": False, "claim_boundary": "ordinary_bottleneck_localization_only", "system_deltas": [], "before": charter["conceptual_opacity"], "after": "The bottleneck was localized to ordinary work without inventing conceptual depth.", "perspective_shifts": ["Conceptual overreach was avoided."], "explanatory_compressions": [], "new_distinctions": ["conceptual formation versus ordinary completion"], "productive_contradictions": [], "remaining_opacity": [charter["conceptual_opacity"]]},
        "theoretical_programme": {"programme_id": stable_identifier("programme", request["target_id"], "ordinary"), "authority_status": "not_conceptual", "conceptual_system_ids": [], "investment_authorized": False, "component_programmes": [], "definitions_to_build": [], "relations_or_mechanisms_to_formalize": [], "consequences_to_derive": [], "proof_or_model_obligations": [], "literature_questions": [], "next_theory_actions": [f"Route to {action} work."]},
        "support_probe": {"disposition": "no_probe_needed", "theory_programme_id": None, "theoretical_question_id": None, "conceptual_system_ids": [], "theoretical_question": None, "role": "none", "why_theory_alone_is_currently_insufficient": None, "possible_theory_updates": [], "receipt_ids": [], "reflective_assimilation_event_ids": []},
        "stage_gates": {"G0_essential_relevance": "pass", "G0L_literature_rebase": "not_required", "G1_genuine_transformation": "open", "G2_philosophical_depth": "open", "G3_unification": "open", "G4_understanding_gain": "open", "G5_reflective_resilience": "open", "G6_truth_apt_articulation": "pass", "G7_claim_promotion": "not_requested"},
        "truth_convergence_status": {"conceptual_preference": "not_requested", "internal_coherence": "not_assessed", "formal_support": "open", "model_or_experimental_support": "not_requested", "proof_status": "open"},
        "plateau": {"materially_empty_rounds": 0, "equivalence_basis": "No conceptual rounds were run.", "action": "continue"},
        "next_reflective_action": {"kind": action, "question": f"What exact {action} step closes the localized bottleneck?", "expected_conceptual_change": "No conceptual change is required unless ordinary work exposes a new root tension."},
        "generation_mode": "not_applicable", "operator_receipt_ids": list(request.get("operator_receipt_ids", [])), "evaluation_receipt_ids": [], "conceptual_adjudication_evidence": None, "ledger_events": [{"event_type": "not_conceptual_diagnosis", "target_id": request["target_id"], "ordinary_handoff": action}], "explicit_unknowns": list(request.get("explicit_unknowns", [])), "created_utc": utc_now(),
    }
    packet["packet_digest"] = canonical_digest(packet)
    validate_payload(packet, "reflective_conceptual_discovery_packet.schema.json")
    validate_packet_invariants(packet)
    return packet


def build_reflective_discovery_packet(
    request: Mapping[str, Any],
    *,
    central_reflection_authority: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build and validate one feedback-effective reflective discovery cycle.

    The request may carry independently generated systems/reflection rounds.  If
    they are absent, the local structural operators compile literature-rebased
    high-risk seeds and execute two explicit reflection transformations.  A
    central-route source additionally requires a nonserializable live authority
    bundle; portable requests and caller-authored changed paths cannot reopen it.
    """

    required = {"target_id", "run_id", "state_version", "discovery_charter", "conceptual_genealogy"}
    missing = required - request.keys()
    if missing:
        raise DiscoveryWorkflowError(f"discovery request missing fields: {sorted(missing)}")
    central_request_present = (
        request.get("central_conceptual_reflection_request") is not None
    )
    if "central_conceptual_route_accounts" in request:
        raise DiscoveryWorkflowError(
            "caller-authored central route accounts and changed paths are forbidden"
        )
    if "central_reflection_authority" in request:
        raise DiscoveryWorkflowError(
            "live central reflection authority cannot be serialized into the request"
        )
    authority_present = central_reflection_authority is not None
    if central_request_present != authority_present:
        raise DiscoveryWorkflowError(
            "central conceptual reflection requires its exact live authority bundle"
        )
    authority_fields = {
        "store",
        "verified_commit",
        "bundle_root",
        "intake_claim",
        "producer_request",
        "producer_receipt",
        "producer_input",
        "producer_output",
    }
    if authority_present and (
        not isinstance(central_reflection_authority, Mapping)
        or set(central_reflection_authority) != authority_fields
    ):
        raise DiscoveryWorkflowError(
            "central reflection live authority bundle has an inexact capability shape"
        )
    charter = copy.deepcopy(request["discovery_charter"])
    if charter["bottleneck_diagnosis"] == "not_conceptual":
        if central_request_present:
            raise DiscoveryWorkflowError(
                "a central conceptual reflection request cannot be discarded "
                "through the not-conceptual fallback"
            )
        return _not_conceptual_packet(request)
    literature = copy.deepcopy(request.get("literature_basis") or {})
    if literature.get("freshness_status") != "current":
        raise DiscoveryWorkflowError("major active discovery requires the newest validated target-scoped literature basis")
    if not literature.get("search_receipt_ids") or not literature.get("assimilation_packet_ref"):
        raise DiscoveryWorkflowError("literature timestamp or bibliography cannot substitute for search and assimilation receipts")
    if literature.get("snapshot_target_id") != request["target_id"]:
        raise DiscoveryWorkflowError("target-scoped literature snapshot does not match the discovery target")
    portfolio = copy.deepcopy(request.get("high_risk_portfolio") or {})
    hypotheses = list(portfolio.get("hypotheses", []))
    canonical_selected = [
        item.get("hypothesis_id")
        for item in hypotheses
        if item.get("selection_status")
        in {"selected_pareto", "protected_wildcard", "control"}
    ]
    selected_ids = list(
        portfolio.get("selected_hypothesis_ids")
        or canonical_selected
        or [
            item.get("hypothesis_id")
            for item in hypotheses
            if item.get("concept_lifecycle_state") not in {"demoted", "retired"}
        ]
    )
    selected = [item for item in hypotheses if item.get("hypothesis_id") in selected_ids]
    if not selected:
        raise DiscoveryWorkflowError("conceptual cycle requires literature-rebased high-risk hypotheses")
    if any(item.get("concept_lifecycle_state") not in {"literature_rebased", "reflectively_supported", "incubating"} or item.get("literature_relation") in {None, "pending_rebase"} for item in selected):
        raise DiscoveryWorkflowError("every active seed must be literature-rebased before investment")
    portfolio_digest = portfolio.get("literature_snapshot_digest")
    if portfolio_digest and portfolio_digest != literature.get("selected_snapshot_digest"):
        raise DiscoveryWorkflowError(
            "high-risk portfolio and reflective cycle use different literature snapshots"
        )
    for item in selected:
        rebase = item.get("literature_rebase_receipt")
        if rebase:
            if (
                rebase.get("snapshot_digest") != literature.get("selected_snapshot_digest")
                or rebase.get("status") != "completed"
            ):
                raise DiscoveryWorkflowError(
                    "active high-risk seed lacks a completed rebase against the selected snapshot"
                )
    genealogy = copy.deepcopy(request["conceptual_genealogy"])
    supplied_systems = bool(request.get("conceptual_systems"))
    supplied_rounds = bool(request.get("reflection_rounds"))
    generation_mode = str(request.get("generation_mode") or "local_structural_fallback")
    if generation_mode not in {"local_structural_fallback", "operator_generated"}:
        raise DiscoveryWorkflowError(f"invalid generation_mode: {generation_mode}")
    if central_request_present and (
        generation_mode != "operator_generated"
        or not supplied_systems
        or not supplied_rounds
    ):
        raise DiscoveryWorkflowError(
            "central conceptual reflection intake requires operator_generated "
            "supplied conceptual systems and reflection rounds; default fallback "
            "is forbidden"
        )
    if request.get("preferred_system_id") is not None:
        raise DiscoveryWorkflowError(
            "caller-selected preferred_system_id is forbidden; preference comes only from sealed conceptual adjudication evidence"
        )
    if request.get("independent_evaluation_evidence"):
        raise DiscoveryWorkflowError(
            "legacy independent evaluation bundles cannot authorize conceptual preference"
        )
    evaluation_receipt_ids = list(request.get("evaluation_receipt_ids", []))
    adjudication_evidence = copy.deepcopy(
        request.get("conceptual_adjudication_evidence")
    )
    systems = copy.deepcopy(request.get("conceptual_systems") or [])
    if not systems:
        systems = [incumbent_system(charter, genealogy)] + [system_from_hypothesis(item, genealogy) for item in selected[:4]]
    rounds = copy.deepcopy(request.get("reflection_rounds") or [])
    if rounds:
        round_system_ids = [
            str(system_id)
            for round_row in reversed(rounds)
            for system_id in reversed(round_row.get("system_ids", []))
        ]
        synthesis = next(
            (
                item
                for system_id in round_system_ids
                for item in systems
                if item["system_id"] == system_id
            ),
            systems[-1],
        )
    else:
        rounds, synthesis = default_reflection_rounds(systems, charter)
    central_intake: dict[str, Any] | None = None
    if central_request_present:
        assert central_reflection_authority is not None
        try:
            central_intake = build_central_conceptual_route_reflection_intake(
                central_request=request[
                    "central_conceptual_reflection_request"
                ],
                intake_claim=central_reflection_authority["intake_claim"],
                producer_request=central_reflection_authority[
                    "producer_request"
                ],
                producer_receipt=central_reflection_authority[
                    "producer_receipt"
                ],
                producer_input=central_reflection_authority["producer_input"],
                producer_output=central_reflection_authority[
                    "producer_output"
                ],
                store=central_reflection_authority["store"],
                verified_commit=central_reflection_authority[
                    "verified_commit"
                ],
                bundle_root=central_reflection_authority["bundle_root"],
                target_id=str(request["target_id"]),
                run_id=str(request["run_id"]),
                state_version=int(request["state_version"]),
                conceptual_systems=systems,
                reflection_rounds=rounds,
            )
        except CentralConceptualReflectionError as exc:
            raise DiscoveryWorkflowError(
                f"central conceptual reflection intake is invalid: {exc}"
            ) from exc
    if adjudication_evidence is not None and (not supplied_systems or not supplied_rounds):
        raise DiscoveryWorkflowError(
            "sealed preference evidence must consume the exact supplied systems and reflection rounds"
        )
    preferred_ids: list[str] = []
    nondominated_ids: list[str] = []
    preference_decision: str | None = None
    if adjudication_evidence is not None:
        try:
            preference = validate_sealed_preference_authority(
                adjudication_evidence,
                target_id=str(request["target_id"]),
                run_id=str(request["run_id"]),
                state_version=int(request["state_version"]),
                system_ids=[str(item["system_id"]) for item in systems],
                systems=systems,
                reflection_rounds=rounds,
            )
        except ConceptualAdjudicationError as exc:
            raise DiscoveryWorkflowError(
                f"sealed conceptual adjudication evidence is invalid: {exc}"
            ) from exc
        preference_decision = str(preference["decision"])
        preferred_ids = list(preference["preferred_system_ids"])
        nondominated_ids = list(preference["nondominated_system_ids"])
    if preference_decision == "prefer_unique":
        authority_status = "sealed_unique"
        diagnostic_ids: list[str] = []
    elif preference_decision == "retain_plural_nondominated":
        authority_status = "sealed_plural"
        diagnostic_ids = []
    elif preference_decision == "revise_all":
        authority_status = "sealed_revise_all_diagnostic_only"
        diagnostic_ids = nondominated_ids or [str(item["system_id"]) for item in systems]
    else:
        authority_status = "absent_diagnostic_only"
        diagnostic_ids = [str(synthesis["system_id"])]
        nondominated_ids = list(diagnostic_ids)
    preference_authorized = bool(preferred_ids)
    authority_ids = preferred_ids or diagnostic_ids
    outcome_systems = _authority_systems(systems, authority_ids)
    challengers = [
        item["system_id"]
        for item in systems
        if item["system_id"] not in set(authority_ids)
        and item["relation"] != "incumbent"
    ]
    programme_id = stable_identifier(
        "programme",
        adjudication_evidence["evidence_id"]
        if adjudication_evidence is not None
        else canonical_digest(authority_ids),
        request["state_version"],
    )
    theoretical_programme = build_set_indexed_programme(
        programme_id=programme_id,
        systems=outcome_systems,
        authority_status=authority_status,
        literature_questions=list(literature["literature_generated_questions"]),
    )
    support = copy.deepcopy(
        request.get("support_probe")
        or {
            "disposition": "no_probe_needed",
            "theory_programme_id": programme_id if preference_authorized else None,
            "theoretical_question_id": None,
            "conceptual_system_ids": list(preferred_ids),
            "theoretical_question": None,
            "role": "none",
            "why_theory_alone_is_currently_insufficient": None,
            "possible_theory_updates": [],
            "receipt_ids": [],
            "reflective_assimilation_event_ids": [],
        }
    )
    if preference_authorized:
        if support.get("theory_programme_id") is None:
            support["theory_programme_id"] = programme_id
        if support.get("theory_programme_id") != programme_id:
            raise DiscoveryWorkflowError(
                "support probe must bind the exact set-indexed theory programme"
            )
        if list(support.get("conceptual_system_ids", [])) != preferred_ids:
            raise DiscoveryWorkflowError(
                "support probe must preserve the complete ordered sealed preference set"
            )
    elif (
        support.get("disposition") != "no_probe_needed"
        or support.get("theory_programme_id") is not None
        or support.get("conceptual_system_ids")
    ):
        raise DiscoveryWorkflowError(
            "diagnostic or revise-all outcomes cannot commission preference-sensitive support"
        )
    understanding_delta = build_set_indexed_understanding_delta(
        before=str(charter["conceptual_opacity"]),
        systems=outcome_systems,
        rounds=rounds,
        authority_status=authority_status,
    )
    next_action = copy.deepcopy(request.get("next_reflective_action"))
    if next_action is None:
        next_action = default_set_action(outcome_systems, authority_status)
    plural_probe_preserves_set = (
        next_action.get("kind") == "probe"
        and support.get("disposition") == "proposed"
        and list(support.get("conceptual_system_ids", [])) == preferred_ids
    )
    if (
        authority_status == "sealed_plural"
        and next_action.get("kind")
        not in {"compare", "differentiate", "reflect"}
        and not plural_probe_preserves_set
    ):
        raise DiscoveryWorkflowError(
            "plural nondominated outcomes require a set-preserving reflective or support action"
        )
    if authority_status == "sealed_revise_all_diagnostic_only" and next_action.get(
        "kind"
    ) not in {"reframe", "differentiate", "incubate", "reflect"}:
        raise DiscoveryWorkflowError(
            "revise_all permits revision or incubation actions only"
        )
    parallel_input = request.get("parallel_portfolio") or {}
    parallel_summary = _parallel_reference(parallel_input)
    high_risk_summary = {
        "disposition": "routed" if parallel_summary["disposition"] != "not_needed" else "literature_rebased",
        "portfolio_ref": request.get("high_risk_portfolio_ref", f"portfolio:{portfolio.get('portfolio_id', 'unknown')}"),
        "corner_families": sorted({str(item["corner_family"]) for item in hypotheses}),
        "selected_hypothesis_ids": selected_ids, "protected_wildcard_ids": list(portfolio.get("protected_wildcard_ids", [])),
        "control_hypothesis_ids": list(portfolio.get("control_hypothesis_ids", [])), "literature_rebase_status": "current",
    }
    central_intake_events = (
        [
            {
                "event_type": "central_conceptual_route_reflection_intake",
                "entity_id": central_intake["intake_id"],
                "source_request_id": central_intake["source_request_id"],
                "source_request_digest": central_intake[
                    "source_request_digest"
                ],
                "intake_claim_id": central_intake["intake_claim"]["claim_id"],
                "intake_claim_digest": central_intake["intake_claim"][
                    "claim_digest"
                ],
                "producer_request_id": central_intake[
                    "registered_producer_binding"
                ]["producer_request"]["request_id"],
                "producer_receipt_id": central_intake[
                    "registered_producer_binding"
                ]["producer_receipt"]["receipt_id"],
                "computed_patch_set_digest": central_intake[
                    "computed_patch_set"
                ]["patch_set_digest"],
                "central_source_commit_generation": central_intake[
                    "central_source_commit_generation"
                ],
                "cycle_input_head_generation": central_intake[
                    "cycle_input_head_generation"
                ],
                "descendant_effect_commit_generation": central_intake[
                    "descendant_effect_commit_generation"
                ],
                "source_selected_route_ids": central_intake[
                    "source_selected_route_ids"
                ],
                "changed_route_ids": central_intake["changed_route_ids"],
                "unresolved_route_ids": central_intake[
                    "unresolved_route_ids"
                ],
                "negative_knowledge_route_ids": central_intake[
                    "negative_knowledge_route_ids"
                ],
                "selection_is_set_valued_local_input": True,
                "direct_preference_authorized": False,
            }
        ]
        if central_intake is not None
        else []
    )
    packet: dict[str, Any] = {
        "schema_version": "1.0.0", "packet_id": stable_identifier("discovery", request["target_id"], request["run_id"], request["state_version"], authority_status, canonical_digest(authority_ids)),
        "target_id": request["target_id"], "run_id": request["run_id"], "branch_id": request.get("branch_id", "root"), "state_version": request["state_version"],
        "prior_conceptual_state_ref": request.get("prior_conceptual_state_ref", f"state:{request['state_version']}"),
        "discovery_charter": charter, "conceptual_genealogy": genealogy, "literature_basis": literature,
        "root_tensions": copy.deepcopy(request.get("root_tensions", [])), "conceptual_systems": systems,
        "high_risk_hypothesis_portfolio": high_risk_summary, "parallel_portfolio": parallel_summary, "reflection_rounds": rounds,
        "provisional_synthesis": {
            "authority_status": authority_status,
            "investment_authorized": preference_authorized,
            "preferred_system_id": preferred_ids[0] if len(preferred_ids) == 1 else None,
            "preferred_system_ids": preferred_ids,
            "diagnostic_synthesis_system_ids": diagnostic_ids,
            "nondominated_system_ids": nondominated_ids,
            "preference_authority_evidence_id": adjudication_evidence["evidence_id"] if adjudication_evidence is not None else None,
            "retained_challenger_ids": challengers,
            "stable_conceptual_core": list(dict.fromkeys(value for item in outcome_systems for value in [item["mechanism_or_principle"], *item["primitives"][:2]])),
            "unresolved_dissent": list(dict.fromkeys(value for item in outcome_systems for value in item["residual_contradictions"])),
            "why_not_premature_convergence": "The sealed adjudication retained every nondominated preferred system and leaves challengers and correction conditions live." if preferred_ids else "Structural synthesis is recorded only as a diagnostic incubation candidate; no preference is authorized without sealed adjudication evidence.",
        },
        "theory_quality_pareto": build_pareto_assessment(systems),
        "understanding_delta": understanding_delta,
        "theoretical_programme": theoretical_programme,
        "support_probe": support,
        "stage_gates": {"G0_essential_relevance": "pass", "G0L_literature_rebase": "pass", "G1_genuine_transformation": "pass" if preference_authorized else "open", "G2_philosophical_depth": "open", "G3_unification": "pass" if preference_authorized else "open", "G4_understanding_gain": "open", "G5_reflective_resilience": "pass" if preference_authorized else "open", "G6_truth_apt_articulation": "pass", "G7_claim_promotion": "not_requested"},
        "truth_convergence_status": {"conceptual_preference": f"sealed_preference_set:{','.join(preferred_ids)}" if preferred_ids else ("sealed_revise_all" if adjudication_evidence is not None else f"incubating_structural_set:{','.join(diagnostic_ids)}"), "internal_coherence": "sealed_internal_correlated_preference_open" if preference_authorized else ("sealed_revise_all_diagnostic_only" if adjudication_evidence is not None else "structurally_screened_diagnostic_only"), "formal_support": "formalization_needed" if preference_authorized else "not_authorized_for_investment", "model_or_experimental_support": "not_requested" if support["disposition"] == "no_probe_needed" else "see_support_receipts", "proof_status": "open"},
        "plateau": {"materially_empty_rounds": sum(item["result"] == "no_change" for item in rounds), "equivalence_basis": "Canonical primitives, relations, mechanisms, regimes, and generated questions.", "action": "reframe" if authority_status == "sealed_revise_all_diagnostic_only" or sum(item["result"] == "no_change" for item in rounds) >= 2 else ("incubate" if authority_status == "absent_diagnostic_only" else "continue")},
        "next_reflective_action": next_action,
        "generation_mode": generation_mode, "operator_receipt_ids": list(request.get("operator_receipt_ids", [])), "evaluation_receipt_ids": evaluation_receipt_ids,
        "conceptual_adjudication_evidence": adjudication_evidence,
        "ledger_events": [
            {"event_type": "conceptual_system_articulated", "entity_id": item["system_id"], "target_id": request["target_id"], "state_version": request["state_version"]}
            for item in systems
        ] + [{"event_type": "reflection_mutation", "entity_id": item["round_id"], "result": item["result"]} for item in rounds] + central_intake_events + ([{"event_type": "conceptual_preference_sealed", "entity_ids": preferred_ids, "evidence_id": adjudication_evidence["evidence_id"], "programme_id": programme_id}] if preferred_ids else [{"event_type": "diagnostic_theory_set_retained", "entity_ids": diagnostic_ids, "programme_id": programme_id, "authority_status": authority_status, "preference_authorized": False}]),
        "explicit_unknowns": list(request.get("explicit_unknowns", [])), "created_utc": utc_now(),
    }
    if central_intake is not None:
        packet["central_conceptual_route_reflection_intake"] = central_intake
    packet["packet_digest"] = canonical_digest(packet)
    validate_payload(packet, "reflective_conceptual_discovery_packet.schema.json")
    validate_packet_invariants(packet)
    return packet
