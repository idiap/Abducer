# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Canonical theory-first discovery cycle and its single durable state transition.

This module is the composition boundary between independently executed discovery
operators and the authoritative epistemic ledger.  It consumes only
digest-verified operator artifacts, checks that every artifact names one target,
run, frozen state, theory digest, and literature snapshot, then reduces the
result into exactly one compare-and-swap transaction.  Symbolic experiments and
proof handoffs are optional children of a mature theory programme; neither may
select a theory or promote a truth claim.

The important distinction is between *operator success* and *epistemic effect*.
An output is not considered used merely because it exists.  Each successful
operator receipt receives a typed consumer event and a feedback edge inside the
same atomic commit.  This makes reachability replayable and prevents a generated
report from masquerading as learning.
"""

from __future__ import annotations

import copy
import datetime as dt
import json
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    bytes_digest,
    canonical_json,
    canonical_digest,
    resolve_workspace_path,
    stable_identifier,
    validate_identifier,
    validate_instance,
    validate_payload,
)
from agentic.discovery.conceptual_adjudication import (
    validate_material_system_transition,
    validate_sealed_preference_authority,
)
from agentic.discovery.committed_projection import (
    build_committed_cycle_projection_artifacts,
)
from agentic.discovery.evaluation import (
    CONCEPTUAL_GATE_IDS,
    conceptual_gate_vector,
    conceptual_gates_pass,
    evaluate_discovery_delta,
    semantic_delta_evidence,
    validate_evaluation_receipt,
)
from agentic.discovery.formal_claim_authority import (
    build_formal_claim_producer_output,
    formalization_seed_rows,
    validate_formal_claim_producer_input,
    validate_formal_claim_producer_output,
)
from agentic.discovery.hypotheses import validate_high_risk_portfolio
from agentic.discovery.ledger import (
    GENESIS_HASH,
    SYNTHESIS_AUTHORITY_NULLS,
    build_event,
    initial_state,
    reduce_from_state,
)
from agentic.discovery.literature import (
    LANE_TYPES,
    expected_snapshot_validator_receipt_id,
    resolve_present_literature_freshness,
    validate_assimilation,
    validate_snapshot,
)
from agentic.discovery.literature_acquisition import (
    derive_source_routing_semantic_warrants,
    validate_source_routing_pre_map_policy,
    validate_source_routing_realization,
)
from agentic.discovery.literature_production_commitment import (
    validate_portable_literature_production_input_bundle,
)
from agentic.discovery.parallel import validate_parallel_portfolio
from agentic.discovery.receipts import (
    assert_feedback_effective,
    ensure_evaluation_ready,
    semantic_output_rows,
)
from agentic.discovery.receipts import (
    validate_operator_receipt_identity,
    validate_operator_request_identity,
)
from agentic.discovery.reflection import validate_packet_invariants
from agentic.discovery.scheduler import schedule_discovery_actions
from agentic.discovery.workflow import (
    build_set_indexed_programme,
    build_set_indexed_understanding_delta,
    default_set_action,
)
from agentic.experiments import (
    build_experiment_reflection_receipt,
    validate_commissioned_experiment_spec,
    validate_experiment_receipt,
)
from agentic.experiments.world_matrix import (
    build_experiment_authority_projection,
    validate_experiment_authority_projection,
)
from agentic.state.discovery_transaction import CommitArtifact, DiscoveryTransactionStore


REQUIRED_ROLES = (
    "literature_snapshot",
    "literature_production_input_bundle",
    "literature_assimilation",
    "high_risk_portfolio",
    "parallel_portfolio",
    "reflective_packets",
)
EXTERNAL_ROLE_ARTIFACTS = frozenset(
    {"literature_snapshot", "literature_production_input_bundle"}
)
OPTIONAL_ROLES = (
    "source_routing_precommit",
    "source_routing_pre_map_policy",
    "source_routing_realization",
    "parent_conceptual_adjudication",
    "synthesis_conceptual_adjudication",
    "formal_claim_output",
)
CONCEPTUAL_ADJUDICATION_ROLES = (
    "parent_conceptual_adjudication",
    "synthesis_conceptual_adjudication",
)
SOURCE_AUTHORITY_PRODUCER_ROLES = {
    "source_routing_pre_map_policy": "source-routing-pre-map-policy-producer",
    "source_routing_realization": "source-routing-realization-producer",
}
DISCOVERY_OPERATOR_REGISTRY_PATH = (
    Path(__file__).resolve().parents[1]
    / "registries"
    / "discovery_operator_registry.yaml"
)
LITERATURE_FRESHNESS_SECONDS = 30 * 24 * 60 * 60
AUTHORITY_BOUNDARY = (
    "conceptual_worth_is_independent_of_truth_authority; experiments_and_proof_"
    "handoffs_are_theory_subordinate_and_require_reflective_assimilation; internal_"
    "correlated_rubric_results_are_not_external_depth_or_understanding_validation"
)
DECLARED_EXPERIMENT_WORLD_IDS = (
    "no_probe",
    "neutral_inconclusive",
    "misleading_toy_positive",
    "registered_premise_falsifier",
    "operational_failure",
)
EXPERIMENT_WORLD_MATRIX_SCOPE = (
    "declared_five_world_consistency_matrix_not_an_exhaustive_experiment_universe"
)
SYNTHESIS_AUTHORITY_BOUNDARY = (
    "sealed conceptual preference is internal-only; proof, empirical, external-validation, "
    "source-truth, theorem, mass-gap, and physics-result authority remain null"
)

_SEMANTIC_TRANSPORT_KEYS = frozenset(
    {
        "action_id",
        "candidate_digest",
        "consumption_log",
        "content_digest",
        "deduplication_key",
        "deduplication_keys",
        "event_count",
        "event_hash",
        "event_id",
        "evaluation_id",
        "feedback_edge_id",
        "input_digest",
        "last_event_hash",
        "last_event_id",
        "operator_receipt_ids",
        "output_digest",
        "packet_digest",
        "packet_id",
        "previous_event_hash",
        "producer_request_id",
        "receipt_digest",
        "receipt_id",
        "receipt_ids",
        "resource_usage",
        "row_digest",
        "schedule_digest",
        "schedule_id",
        "search_receipt_ids",
        "source_output_path",
        "wall_seconds",
        "wave_id",
    }
)
_SEMANTIC_TRANSPORT_SUFFIXES = (
    "_event_id",
    "_event_ids",
    "_evaluation_id",
    "_invocation_id",
    "_receipt_id",
    "_receipt_ids",
)
_SEMANTIC_TIME_KEYS = frozenset(
    {
        "completed_at",
        "consumed_at",
        "consume_before",
        "created_at",
        "created_utc",
        "evaluated_at",
        "occurred_at",
        "present_use_evaluated_at",
        "requested_at",
        "search_completed_at",
        "search_completed_utc",
        "search_started_at",
        "started_at",
    }
)
_NON_THEORY_EXPERIMENT_REFLECTION_KINDS = frozenset(
    {"operator_output_consumed", "post_result_reflective_assimilation"}
)


def _internal_panel_evidence_class(packet: Mapping[str, Any]) -> str:
    """Conservatively classify the evaluator evidence exposed by a cycle.

    Even authority-distinct local programs remain internal evidence. The public
    cycle projection therefore reports the panel's actual internal class but
    never turns it into external philosophical-depth or understanding authority.
    """

    evidence = packet.get("independent_evaluation_evidence", [])
    if not evidence:
        return "single_internal_structural_evaluator"
    classes = {
        str(
            item.get("content_adjudication", {})
            .get("authority", {})
            .get("panel_evidence_class", "internal_evaluator_authority_unresolved")
        )
        for item in evidence
        if isinstance(item, Mapping)
    }
    if len(classes) != 1:
        return "internal_evaluator_authority_unresolved"
    value = next(iter(classes))
    return (
        value
        if value
        in {"correlated_internal_critique", "independent_internal_judgment"}
        else "internal_evaluator_authority_unresolved"
    )


def _bound_conceptual_evaluation_authority(
    packet: Mapping[str, Any],
) -> tuple[list[Mapping[str, Any]], list[str], bool]:
    """Validate and derive authority from the packet's exact sealed receipts.

    A packet that binds independent evaluation evidence cannot fall back to a
    later structural evaluation for its public decision.  Receipt order is
    authority-bearing, every receipt ID must match the packet's declared list,
    and every receipt must be accompanied by a complete passing conceptual-gate
    adjudication with a material parent-to-synthesis comparison.
    """

    receipts: list[Mapping[str, Any]] = []
    conceptual_gate_evidence_count = 0
    for evidence in packet.get("independent_evaluation_evidence", []):
        receipt = evidence.get("evaluation_receipt") if isinstance(evidence, Mapping) else None
        if not isinstance(receipt, Mapping):
            raise ContractError("bound conceptual evaluation evidence lacks a receipt")
        validate_evaluation_receipt(receipt)
        receipts.append(receipt)
        if evidence.get("evaluation_role") != "conceptual_gate":
            continue
        findings = evidence.get("gate_findings", {})
        if not isinstance(findings, Mapping):
            raise ContractError("conceptual-gate evidence lacks typed G0--G6 findings")
        missing_findings = set(CONCEPTUAL_GATE_IDS) - set(findings)
        if missing_findings:
            raise ContractError(
                f"conceptual-gate evidence omits gates: {sorted(missing_findings)}"
            )
        if any(
            not isinstance(findings[gate_id], Mapping)
            or findings[gate_id].get("status") != "pass"
            for gate_id in CONCEPTUAL_GATE_IDS
        ):
            raise ContractError("conceptual-gate evidence has a non-passing G0--G6 gate")
        comparison = evidence.get("stage_comparison", {})
        if (
            not isinstance(comparison, Mapping)
            or comparison.get("applicability") != "applicable"
            or comparison.get("material") is not True
        ):
            raise ContractError(
                "conceptual-gate evidence lacks a material parent-to-synthesis delta"
            )
        conceptual_gate_evidence_count += 1
    if receipts and packet.get("evaluation_receipt_ids") != [
        receipt["evaluation_id"] for receipt in receipts
    ]:
        raise ContractError("bound conceptual evaluation IDs differ from their receipts")
    decisions = [str(receipt["creative_worth_decision"]) for receipt in receipts]
    preferred = bool(receipts) and all(
        receipt["creative_worth_decision"] == "prefer"
        and receipt["promotion_decision"] == "not_requested"
        for receipt in receipts
    ) and conceptual_gate_evidence_count == len(receipts)
    return receipts, decisions, preferred


def _ordered_packet_systems(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return one exact ordered candidate set with no identity collapse."""

    systems = [copy.deepcopy(dict(row)) for row in packet.get("conceptual_systems", [])]
    system_ids = [str(row.get("system_id", "")) for row in systems]
    if len(systems) < 2 or any(not system_id for system_id in system_ids):
        raise ContractError("conceptual adjudication requires at least two identified systems")
    if len(system_ids) != len(set(system_ids)):
        raise ContractError("conceptual adjudication candidate IDs must be unique")
    return systems


def _set_indexed_system_outcomes(
    packet: Mapping[str, Any],
    *,
    preferred_system_ids: Sequence[str],
    diagnostic_system_ids: Sequence[str],
    authority_status: str,
) -> list[dict[str, Any]]:
    """Project every authority member without selecting a representative member."""

    systems = {
        str(row["system_id"]): copy.deepcopy(dict(row))
        for row in packet.get("conceptual_systems", [])
    }
    support = copy.deepcopy(dict(packet.get("support_probe", {})))
    support_ids = set(str(value) for value in support.get("conceptual_system_ids", []))
    ordered_authority = [
        *(str(value) for value in preferred_system_ids),
        *(str(value) for value in diagnostic_system_ids),
    ]
    if len(ordered_authority) != len(set(ordered_authority)):
        raise ContractError("preferred and diagnostic conceptual authority must be disjoint sets")
    if not set(ordered_authority).issubset(systems):
        raise ContractError("conceptual authority escapes the synthesized candidate set")
    authority_systems = [systems[system_id] for system_id in ordered_authority]
    programme = build_set_indexed_programme(
        programme_id=stable_identifier(
            "canonical-authority-programme",
            packet["packet_id"],
            authority_status,
            ordered_authority,
        ),
        systems=authority_systems,
        authority_status=authority_status,
        literature_questions=list(
            packet.get("literature_basis", {}).get(
                "literature_generated_questions", []
            )
        ),
    )
    understanding = build_set_indexed_understanding_delta(
        before=str(packet["discovery_charter"]["conceptual_opacity"]),
        systems=authority_systems,
        rounds=list(packet.get("reflection_rounds", [])),
        authority_status=authority_status,
    )
    programme_components = {
        str(row["conceptual_system_id"]): copy.deepcopy(dict(row))
        for row in programme["component_programmes"]
    }
    understanding_deltas = {
        str(row["conceptual_system_id"]): copy.deepcopy(dict(row))
        for row in understanding["system_deltas"]
    }
    next_action = default_set_action(authority_systems, authority_status)

    preferred = set(str(value) for value in preferred_system_ids)
    rows: list[dict[str, Any]] = []
    for system_id in ordered_authority:
        system = systems[system_id]
        unification_map = copy.deepcopy(system.get("unification_claims", {}))
        rows.append(
            {
                "system_id": system_id,
                "disposition": (
                    "preferred"
                    if system_id in preferred
                    else "diagnostic_revision"
                    if diagnostic_system_ids
                    and authority_status
                    == "sealed_revise_all_diagnostic_only"
                    else "diagnostic_local"
                ),
                "unification_map": unification_map,
                "preserved_differences": copy.deepcopy(
                    unification_map.get(
                        "preserved_differences",
                        unification_map.get("differences_preserved", []),
                    )
                ),
                "component_programme": programme_components[system_id],
                "understanding_delta": understanding_deltas[system_id],
                "support_probe": support if system_id in support_ids else None,
                "next_reflective_action": copy.deepcopy(next_action),
            }
        )
    return rows


def derive_conceptual_authority(
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    literature_mode: str,
    parent_packet: Mapping[str, Any],
    synthesis_packet: Mapping[str, Any],
    parent_evidence: Mapping[str, Any] | None,
    synthesis_evidence: Mapping[str, Any] | None,
    proof_ready: bool = False,
) -> dict[str, Any]:
    """Replay the total conceptual-preference algebra from complete evidence.

    The reflective packets are proposal surfaces.  They cannot be their own
    preference authority inside the canonical role graph: parent generation is
    followed by a blind parent adjudication, synthesis consumes that complete
    evidence, and a second blind adjudication judges the exact final candidate
    bytes.  Local-only incubation has no adjudicator role and therefore retains
    every synthesized candidate as diagnostic-only.
    """

    parent_systems = _ordered_packet_systems(parent_packet)
    synthesis_systems = _ordered_packet_systems(synthesis_packet)
    parent_ids = [str(row["system_id"]) for row in parent_systems]
    synthesis_ids = [str(row["system_id"]) for row in synthesis_systems]
    if parent_packet.get("conceptual_adjudication_evidence") is not None:
        raise ContractError(
            "canonical parent proposal cannot self-embed conceptual preference authority"
        )
    synthesis_embedded_parent = synthesis_packet.get(
        "conceptual_adjudication_evidence"
    )
    prior_critique = synthesis_packet.get("parent_adjudication_evidence")
    if prior_critique is not None:
        if synthesis_embedded_parent is not None:
            raise ContractError("synthesis proposal ambiguously embeds prior critique as current preference")
        # A revised proposal consumes the old panel as critique. Its preference
        # remains absent until the separate synthesis adjudicator seals it.
        synthesis_embedded_parent = prior_critique

    if literature_mode == "local_only_incubation":
        if (
            parent_evidence is not None
            or synthesis_evidence is not None
            or synthesis_embedded_parent is not None
        ):
            raise ContractError("local-only incubation cannot carry conceptual adjudicator authority")
        parent_preference = None
        synthesis_preference = None
        preferred_ids: list[str] = []
        diagnostic_ids = [
            str(value)
            for value in synthesis_packet.get("provisional_synthesis", {}).get(
                "diagnostic_synthesis_system_ids", []
            )
        ]
        if not diagnostic_ids or not set(diagnostic_ids).issubset(synthesis_ids):
            raise ContractError(
                "local-only synthesis requires a nonempty diagnostic set inside its candidate set"
            )
        status = "absent_diagnostic_only"
        decision = "absent_local"
    else:
        if not isinstance(parent_evidence, Mapping) or not isinstance(
            synthesis_evidence, Mapping
        ):
            raise ContractError(
                "active-current discovery requires complete parent and synthesis adjudication evidence"
            )
        if synthesis_embedded_parent != parent_evidence:
            raise ContractError(
                "synthesis proposal did not consume the exact parent adjudication evidence"
            )
        parent_preference = validate_sealed_preference_authority(
            parent_evidence,
            target_id=target_id,
            run_id=run_id,
            state_version=state_version,
            system_ids=parent_ids,
            systems=parent_systems,
            reflection_rounds=parent_packet.get("reflection_rounds", []),
        )
        synthesis_preference = validate_sealed_preference_authority(
            synthesis_evidence,
            target_id=target_id,
            run_id=run_id,
            state_version=state_version,
            system_ids=synthesis_ids,
            systems=synthesis_systems,
            reflection_rounds=synthesis_packet.get("reflection_rounds", []),
        )
        if parent_evidence.get("stage_id") == synthesis_evidence.get("stage_id"):
            raise ContractError("parent and synthesis adjudications require distinct stage identities")
        if parent_evidence.get("input_binding", {}).get("previous_evidence_digest") is not None:
            raise ContractError("parent adjudication cannot claim prior conceptual authority")
        if synthesis_evidence.get("input_binding", {}).get(
            "previous_evidence_digest"
        ) != parent_evidence.get("evidence_digest"):
            raise ContractError(
                "synthesis adjudication does not bind the complete parent evidence digest"
            )
        if _parse_timestamp(str(synthesis_evidence.get("created_at")), "synthesis adjudication") < _parse_timestamp(
            str(parent_evidence.get("created_at")), "parent adjudication"
        ):
            raise ContractError("synthesis adjudication predates parent adjudication")
        decision = str(synthesis_preference["decision"])
        preferred_ids = [
            str(value) for value in synthesis_preference["preferred_system_ids"]
        ]
        if decision == "prefer_unique":
            if len(preferred_ids) != 1:
                raise ContractError("prefer_unique must authorize exactly one conceptual system")
            diagnostic_ids = []
            status = "sealed_unique"
        elif decision == "retain_plural_nondominated":
            if len(preferred_ids) < 2:
                raise ContractError(
                    "retain_plural_nondominated must preserve at least two preferred systems"
                )
            diagnostic_ids = []
            status = "sealed_plural"
        elif decision == "revise_all":
            if preferred_ids:
                raise ContractError("revise_all cannot authorize a preferred conceptual system")
            diagnostic_ids = [
                str(value)
                for value in synthesis_preference.get("nondominated_system_ids", [])
            ] or synthesis_ids
            status = "sealed_revise_all_diagnostic_only"
        else:  # pragma: no cover - closed by the evidence schema and validator.
            raise ContractError(f"unsupported conceptual preference decision: {decision}")

    preference_authorized = status in {"sealed_unique", "sealed_plural"}
    return {
        "status": status,
        "decision": decision,
        "candidate_system_ids": synthesis_ids,
        "preferred_system_ids": preferred_ids,
        "diagnostic_synthesis_system_ids": diagnostic_ids,
        "preference_authorized": preference_authorized,
        "parent_preference_set": copy.deepcopy(parent_preference),
        "synthesis_preference_set": copy.deepcopy(synthesis_preference),
        "parent_evidence": (
            copy.deepcopy(dict(parent_evidence))
            if isinstance(parent_evidence, Mapping)
            else None
        ),
        "synthesis_evidence": (
            copy.deepcopy(dict(synthesis_evidence))
            if isinstance(synthesis_evidence, Mapping)
            else None
        ),
        "system_outcomes": _set_indexed_system_outcomes(
            synthesis_packet,
            preferred_system_ids=preferred_ids,
            diagnostic_system_ids=diagnostic_ids,
            authority_status=status,
        ),
        "structural_screen": {
            "status": "diagnostic_only",
            "gate_vector": conceptual_gate_vector(synthesis_packet),
            "preference_authority": False,
            "proof_authority": False,
            "schedule_authority": False,
        },
        "internal_correlated_preference": preference_authorized,
        "philosophical_depth_authority": None,
        "understanding_gain_authority": None,
        "unification_power_authority": None,
        "creativity_authority": None,
        "relevance_authority": None,
        "external_depth_validation_status": "unavailable",
        "external_understanding_validation_status": "unavailable",
        "external_unification_validation_status": "unavailable",
        "external_creativity_validation_status": "unavailable",
        "external_relevance_validation_status": "unavailable",
        "proof_ready": bool(proof_ready and preference_authorized),
        "fallback_disposition": (
            "maturation_only" if status == "absent_diagnostic_only" else "not_applicable"
        ),
        "authority_nulls": copy.deepcopy(SYNTHESIS_AUTHORITY_NULLS),
        "authority_boundary": SYNTHESIS_AUTHORITY_BOUNDARY,
    }


_CANONICAL_PROJECTION_RECEIPT_PLAN: tuple[
    tuple[str, tuple[str, ...]], ...
] = (
    (
        "source_routing_pre_map_policy",
        ("source-routing-pre-map-policy-producer",),
    ),
    (
        "source_routing_realization",
        ("source-routing-realization-producer",),
    ),
    ("high_risk_portfolio", ("high-risk-hypothesis-forger",)),
    ("parallel_portfolio", ("parallel-hypothesis-portfolio",)),
    (
        "reflective_packets",
        (
            "reflective-conceptual-discovery",
            "reflective-theory-synthesizer",
        ),
    ),
    (
        "parent_conceptual_adjudication",
        ("blind-conceptual-preference-adjudicator",),
    ),
    (
        "synthesis_conceptual_adjudication",
        ("blind-conceptual-preference-adjudicator",),
    ),
)


def _canonical_projection_role_receipts(
    producers_by_role: Mapping[str, Sequence[Mapping[str, Any]]],
    *,
    target_id: str,
    run_id: str,
    state_version: int,
) -> dict[str, list[dict[str, Any]]]:
    """Validate the exact local producer lineage projected into a commission."""

    projected: dict[str, list[dict[str, Any]]] = {}
    receipt_ids: list[str] = []
    request_ids: list[str] = []
    invocation_ids: list[str] = []
    expected_namespace = (target_id, run_id, state_version)
    for role, expected_operators in _CANONICAL_PROJECTION_RECEIPT_PLAN:
        raw_rows = producers_by_role.get(role, ())
        if isinstance(raw_rows, (str, bytes)) or not isinstance(
            raw_rows, Sequence
        ):
            raise ContractError(
                f"canonical world projection producer role {role} is not a receipt sequence"
            )
        rows = [copy.deepcopy(dict(row)) for row in raw_rows]
        if len(rows) != len(expected_operators):
            raise ContractError(
                f"canonical world projection producer role {role} has the wrong cardinality"
            )
        observed_operators: list[str] = []
        for receipt in rows:
            validate_operator_receipt_identity(receipt)
            identity = receipt.get("identity", {})
            actual_namespace = (
                identity.get("target_id"),
                identity.get("run_id"),
                identity.get("state_version"),
            )
            if receipt.get("status") != "succeeded":
                raise ContractError(
                    f"canonical world projection role {role} includes a failed producer"
                )
            if actual_namespace != expected_namespace:
                raise ContractError(
                    f"canonical world projection role {role} crossed target/run/state"
                )
            observed_operators.append(
                str(receipt.get("operator", {}).get("operator_id", ""))
            )
            receipt_ids.append(str(receipt["receipt_id"]))
            request_ids.append(str(receipt["request_id"]))
            invocation_ids.append(str(receipt["invocation_id"]))
        if tuple(observed_operators) != expected_operators:
            raise ContractError(
                f"canonical world projection role {role} has the wrong ordered producers"
            )
        projected[role] = rows
    for values, label in (
        (receipt_ids, "receipt"),
        (request_ids, "request"),
        (invocation_ids, "invocation"),
    ):
        if len(values) != len(set(values)):
            raise ContractError(
                f"canonical world projection reuses a producer {label} identity"
            )
    return projected


def finalize_post_adjudication_reflection(
    *,
    synthesis_packet: Mapping[str, Any],
    conceptual_authority: Mapping[str, Any],
) -> dict[str, Any]:
    """Seal the final adjudication into a theory-produced synthesis packet.

    The final blind adjudication occurs after the synthesizer has emitted its
    packet.  This deterministic reducer replaces the earlier adjudication
    binding and rebuilds the set-indexed programme without inventing a support
    question.  A proposed probe survives only when the synthesizer already
    emitted it for the exact final preferred set; otherwise the finalized
    packet remains ``no_probe_needed``.
    """

    packet = copy.deepcopy(dict(synthesis_packet))
    validate_payload(packet, "reflective_conceptual_discovery_packet.schema.json")
    validate_packet_invariants(packet)
    if packet.get("packet_digest") != _digest_without(packet, "packet_digest"):
        raise ContractError("post-adjudication source packet self-digest is invalid")
    authority = copy.deepcopy(dict(conceptual_authority))
    if (
        authority.get("status") not in {"sealed_unique", "sealed_plural"}
        or authority.get("preference_authorized") is not True
        or authority.get("internal_correlated_preference") is not True
    ):
        raise ContractError(
            "post-adjudication finalization requires sealed conceptual preference"
        )
    evidence = authority.get("synthesis_evidence")
    if not isinstance(evidence, Mapping):
        raise ContractError(
            "post-adjudication finalization lacks final synthesis evidence"
        )
    evidence = copy.deepcopy(dict(evidence))
    validate_payload(evidence, "conceptual_adjudication_evidence.schema.json")
    preferred_ids = [str(value) for value in authority["preferred_system_ids"]]
    candidate_ids = [str(row["system_id"]) for row in packet["conceptual_systems"]]
    if (
        not preferred_ids
        or len(preferred_ids) != len(set(preferred_ids))
        or candidate_ids != list(authority.get("candidate_system_ids", []))
        or not set(preferred_ids).issubset(candidate_ids)
    ):
        raise ContractError(
            "post-adjudication finalization candidate/preferred sets drifted"
        )
    systems_by_id = {
        str(row["system_id"]): row for row in packet["conceptual_systems"]
    }
    preferred_systems = [systems_by_id[system_id] for system_id in preferred_ids]
    programme_id = stable_identifier(
        "programme", evidence["evidence_id"], packet["state_version"]
    )
    programme = build_set_indexed_programme(
        programme_id=programme_id,
        systems=preferred_systems,
        authority_status=str(authority["status"]),
        literature_questions=list(
            packet["literature_basis"]["literature_generated_questions"]
        ),
    )
    support = copy.deepcopy(dict(packet["support_probe"]))
    disposition = support.get("disposition")
    if disposition == "no_probe_needed":
        support = {
            "disposition": "no_probe_needed",
            "theory_programme_id": programme_id,
            "theoretical_question_id": None,
            "conceptual_system_ids": preferred_ids,
            "theoretical_question": None,
            "role": "none",
            "why_theory_alone_is_currently_insufficient": None,
            "possible_theory_updates": [],
            "receipt_ids": [],
            "reflective_assimilation_event_ids": [],
        }
    elif disposition == "proposed":
        source_programme_id = packet["theoretical_programme"]["programme_id"]
        if (
            support.get("theory_programme_id") != source_programme_id
            or list(support.get("conceptual_system_ids", [])) != preferred_ids
            or not isinstance(support.get("theoretical_question_id"), str)
            or not support["theoretical_question_id"].strip()
            or not isinstance(support.get("theoretical_question"), str)
            or not support["theoretical_question"].strip()
            or support.get("role") == "none"
            or support.get("receipt_ids") != []
            or support.get("reflective_assimilation_event_ids") != []
            or packet.get("next_reflective_action", {}).get("kind") != "probe"
        ):
            raise ContractError(
                "post-adjudication support was not emitted by theory for the exact preferred set"
            )
        support["theory_programme_id"] = programme_id
    else:
        raise ContractError(
            "post-adjudication pre-execution reflection permits only proposed or no-probe support"
        )

    packet["packet_id"] = stable_identifier(
        "discovery",
        packet["target_id"],
        packet["run_id"],
        packet["state_version"],
        authority["status"],
        canonical_digest(preferred_ids),
        evidence["evidence_digest"],
    )
    packet["provisional_synthesis"].update(
        {
            "authority_status": authority["status"],
            "investment_authorized": True,
            "preferred_system_id": (
                preferred_ids[0] if len(preferred_ids) == 1 else None
            ),
            "preferred_system_ids": preferred_ids,
            "diagnostic_synthesis_system_ids": [],
            "nondominated_system_ids": preferred_ids,
            "preference_authority_evidence_id": evidence["evidence_id"],
        }
    )
    packet["theoretical_programme"] = programme
    packet["understanding_delta"] = build_set_indexed_understanding_delta(
        before=packet["discovery_charter"]["conceptual_opacity"],
        systems=preferred_systems,
        rounds=packet["reflection_rounds"],
        authority_status=str(authority["status"]),
    )
    packet["support_probe"] = support
    packet["conceptual_adjudication_evidence"] = evidence
    packet["stage_gates"].update(
        {
            "G1_genuine_transformation": "pass",
            "G2_philosophical_depth": "open",
            "G3_unification": "pass",
            "G4_understanding_gain": "open",
            "G5_reflective_resilience": "pass",
        }
    )
    packet["truth_convergence_status"].update(
        {
            "conceptual_preference": (
                "sealed_preference_set:" + ",".join(preferred_ids)
            ),
            "internal_coherence": "sealed_internal_correlated_preference_open",
            "formal_support": "formalization_needed",
            "model_or_experimental_support": (
                "not_requested"
                if disposition == "no_probe_needed"
                else "proposed_theory_subordinate_probe"
            ),
            "proof_status": "open",
        }
    )
    packet["ledger_events"] = [
        copy.deepcopy(row)
        for row in packet["ledger_events"]
        if row.get("event_type")
        not in {"conceptual_preference_sealed", "diagnostic_theory_set_retained"}
    ]
    packet["ledger_events"].append(
        {
            "event_type": "conceptual_preference_sealed",
            "entity_ids": preferred_ids,
            "evidence_id": evidence["evidence_id"],
            "programme_id": programme_id,
        }
    )
    packet["packet_digest"] = canonical_digest(
        packet, exclude_keys=("packet_digest",)
    )
    validate_payload(packet, "reflective_conceptual_discovery_packet.schema.json")
    validate_packet_invariants(packet)
    return packet


def build_canonical_world_authority_projection(
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    prior_state: Mapping[str, Any],
    final_reflection: Mapping[str, Any],
    conceptual_authority: Mapping[str, Any],
    source_authority_pair: Mapping[str, Any],
    literature_production_input_bundle: Mapping[str, Any],
    producers_by_role: Mapping[str, Sequence[Mapping[str, Any]]],
    schedule: Mapping[str, Any],
) -> dict[str, Any]:
    """Derive the complete world authority base from actual canonical inputs.

    No expected component is accepted from a commission.  This function is the
    sole translation from the reopened canonical cycle state into the generic
    five-world projector; the paired replay function later requires literal
    equality with this derivation.
    """

    target_id = validate_identifier(target_id, "target_id")
    run_id = validate_identifier(run_id, "run_id")
    if (
        isinstance(state_version, bool)
        or not isinstance(state_version, int)
        or state_version < 0
    ):
        raise ContractError("canonical world projection state_version is invalid")
    state = copy.deepcopy(dict(prior_state))
    if (
        state.get("target_id"),
        state.get("run_id"),
        state.get("generation"),
    ) != (target_id, run_id, state_version):
        raise ContractError(
            "canonical world projection prior state crossed target/run/generation"
        )

    packet = copy.deepcopy(dict(final_reflection))
    validate_payload(packet, "reflective_conceptual_discovery_packet.schema.json")
    validate_packet_invariants(packet)
    if (
        packet.get("target_id"),
        packet.get("run_id"),
        packet.get("branch_id"),
        packet.get("state_version"),
    ) != (target_id, run_id, "root", state_version):
        raise ContractError(
            "canonical world projection reflection crossed the root target/run/state namespace"
        )
    if packet.get("packet_digest") != _digest_without(packet, "packet_digest"):
        raise ContractError(
            "canonical world projection reflection packet self-digest is invalid"
        )

    authority = copy.deepcopy(dict(conceptual_authority))
    if (
        authority.get("status") not in {"sealed_unique", "sealed_plural"}
        or authority.get("preference_authorized") is not True
        or authority.get("internal_correlated_preference") is not True
        or authority.get("authority_nulls") != SYNTHESIS_AUTHORITY_NULLS
    ):
        raise ContractError(
            "canonical world projection requires sealed conceptual preference authority"
        )
    preferred_ids = [str(value) for value in authority.get("preferred_system_ids", [])]
    if not preferred_ids or len(preferred_ids) != len(set(preferred_ids)):
        raise ContractError(
            "canonical world projection preferred system set is empty or duplicated"
        )
    merit_null_fields = (
        "philosophical_depth_authority",
        "understanding_gain_authority",
        "unification_power_authority",
        "creativity_authority",
        "relevance_authority",
    )
    merit_status_fields = (
        "external_depth_validation_status",
        "external_understanding_validation_status",
        "external_unification_validation_status",
        "external_creativity_validation_status",
        "external_relevance_validation_status",
    )
    if any(authority.get(field) is not None for field in merit_null_fields) or any(
        authority.get(field) != "unavailable" for field in merit_status_fields
    ):
        raise ContractError(
            "canonical world projection invented external conceptual-merit authority"
        )
    if [
        str(row.get("system_id", ""))
        for row in authority.get("system_outcomes", [])
    ] != preferred_ids:
        raise ContractError(
            "canonical world projection set-valued outcomes differ from the preferred set"
        )
    systems = [copy.deepcopy(dict(row)) for row in packet.get("conceptual_systems", [])]
    candidate_ids = [str(row.get("system_id", "")) for row in systems]
    if (
        not candidate_ids
        or len(candidate_ids) != len(set(candidate_ids))
        or candidate_ids != list(authority.get("candidate_system_ids", []))
        or not set(preferred_ids).issubset(candidate_ids)
    ):
        raise ContractError(
            "canonical world projection candidate systems differ from derived authority"
        )
    systems_by_id = {str(row["system_id"]): row for row in systems}

    programme = copy.deepcopy(dict(packet.get("theoretical_programme", {})))
    if (
        programme.get("authority_status") != authority["status"]
        or programme.get("investment_authorized") is not True
        or list(programme.get("conceptual_system_ids", [])) != preferred_ids
    ):
        raise ContractError(
            "canonical world projection programme differs from the preferred set"
        )
    synthesis = packet.get("provisional_synthesis", {})
    if (
        synthesis.get("authority_status") != authority["status"]
        or synthesis.get("investment_authorized") is not True
        or list(synthesis.get("preferred_system_ids", [])) != preferred_ids
    ):
        raise ContractError(
            "canonical world projection synthesis differs from conceptual authority"
        )
    support = copy.deepcopy(dict(packet.get("support_probe", {})))
    if (
        support.get("disposition") not in {"proposed", "commissioned"}
        or not isinstance(support.get("theoretical_question_id"), str)
        or not support["theoretical_question_id"].strip()
        or not isinstance(support.get("theoretical_question"), str)
        or not support["theoretical_question"].strip()
        or support.get("role") == "none"
        or support.get("theory_programme_id") != programme.get("programme_id")
        or list(support.get("conceptual_system_ids", [])) != preferred_ids
    ):
        raise ContractError(
            "canonical world projection support question is not a pre-execution preferred-set commission"
        )

    role_receipts = _canonical_projection_role_receipts(
        producers_by_role,
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
    )
    parent_evidence = authority.get("parent_evidence")
    synthesis_evidence = authority.get("synthesis_evidence")
    if not isinstance(parent_evidence, Mapping) or not isinstance(
        synthesis_evidence, Mapping
    ):
        raise ContractError(
            "canonical world projection lacks complete conceptual adjudication evidence"
        )
    parent_evidence = copy.deepcopy(dict(parent_evidence))
    synthesis_evidence = copy.deepcopy(dict(synthesis_evidence))
    validate_payload(parent_evidence, "conceptual_adjudication_evidence.schema.json")
    validate_payload(synthesis_evidence, "conceptual_adjudication_evidence.schema.json")
    if (
        parent_evidence.get("input_binding", {}).get("proposer_receipt_ids")
        != [role_receipts["reflective_packets"][0]["receipt_id"]]
        or synthesis_evidence.get("input_binding", {}).get("proposer_receipt_ids")
        != [role_receipts["reflective_packets"][1]["receipt_id"]]
        or parent_evidence.get("input_binding", {}).get("previous_evidence_digest")
        is not None
        or synthesis_evidence.get("input_binding", {}).get(
            "previous_evidence_digest"
        )
        != parent_evidence.get("evidence_digest")
    ):
        raise ContractError(
            "canonical world projection adjudication evidence crossed its proposal lineage"
        )
    if packet.get("conceptual_adjudication_evidence") != synthesis_evidence:
        raise ContractError(
            "canonical world projection final packet does not embed the exact final adjudication"
        )

    pair = copy.deepcopy(dict(source_authority_pair))
    if set(pair) != {"pre_map_policy", "realization"}:
        raise ContractError(
            "canonical world projection source authority pair is incomplete"
        )
    policy = pair["pre_map_policy"]
    realization = pair["realization"]
    if not isinstance(policy, Mapping) or not isinstance(realization, Mapping):
        raise ContractError(
            "canonical world projection source authority pair is not object-valued"
        )
    if (
        policy.get("policy_digest") != _digest_without(policy, "policy_digest")
        or realization.get("realization_digest")
        != _digest_without(realization, "realization_digest")
    ):
        raise ContractError(
            "canonical world projection source authority self-digest is invalid"
        )

    literature_bundle = validate_portable_literature_production_input_bundle(
        literature_production_input_bundle
    )
    literature_projection = literature_bundle["semantic_consumer_projection"]
    if (
        literature_bundle.get("target_id") != target_id
        or literature_bundle.get("state_version") != state_version
        or literature_projection.get("target_id") != target_id
        or literature_projection.get("state_version") != state_version
    ):
        raise ContractError(
            "canonical world projection literature input crossed target or generation"
        )

    schedule_value = copy.deepcopy(dict(schedule))
    if (
        schedule_value.get("target_id"),
        schedule_value.get("run_id"),
        schedule_value.get("state_version"),
    ) != (target_id, run_id, state_version):
        raise ContractError("canonical world projection schedule crossed target/run/state")
    schedule_preference = schedule_value.get("conceptual_preference_authority", {})
    if (
        schedule_preference.get("status") != authority["status"]
        or schedule_preference.get("evidence") != synthesis_evidence
        or schedule_value.get("source_routing_pre_map_policy_id")
        != policy.get("policy_id")
        or schedule_value.get("source_routing_pre_map_policy_digest")
        != policy.get("policy_digest")
        or schedule_value.get("source_routing_realization_id")
        != realization.get("realization_id")
        or schedule_value.get("source_routing_realization_digest")
        != realization.get("realization_digest")
        or schedule_value.get("authority_boundary") != AUTHORITY_BOUNDARY
        or not any(
            action.get("kind") == "probe"
            for action in schedule_value.get("actions", [])
            if isinstance(action, Mapping)
        )
        or schedule_value.get("schedule_digest")
        != canonical_digest(
            schedule_value,
            exclude_keys=("schedule_digest", "created_at", "consumption_log"),
        )
    ):
        raise ContractError(
            "canonical world projection schedule differs from canonical authority"
        )

    claim_core = {
        "claim_id": support["theoretical_question_id"],
        "claim_kind": "theory_premise",
        "target_relation": "necessary_not_sufficient",
        "statement": support["theoretical_question"],
        "theory_programme_id": programme["programme_id"],
        "source_theory_programme_digest": canonical_digest(programme),
        "source_reflection_packet_digest": packet["packet_digest"],
        "conceptual_system_ids": preferred_ids,
    }
    registered_claim = {
        **claim_core,
        "claim_digest": canonical_digest(claim_core),
    }
    preferred_systems = [systems_by_id[system_id] for system_id in preferred_ids]
    conceptual_system_projection = {
        "ordered_system_ids": preferred_ids,
        "systems": copy.deepcopy(preferred_systems),
        "candidate_system_ids": candidate_ids,
        "candidate_systems": copy.deepcopy(systems),
        "diagnostic_synthesis_system_ids": copy.deepcopy(
            authority.get("diagnostic_synthesis_system_ids", [])
        ),
        "system_outcomes": copy.deepcopy(authority.get("system_outcomes", [])),
        "conceptual_authority": authority,
        "authority_boundary": (
            "internal correlated conceptual preference only; external creativity, "
            "philosophical depth, understanding gain, unification power, truth, "
            "theorem, and physics-result authority remain null"
        ),
    }
    genealogy = {
        "packet_genealogy": copy.deepcopy(packet["conceptual_genealogy"]),
        "ordered_system_ids": preferred_ids,
        "system_genealogies": [
            {
                "system_id": system_id,
                "conceptual_ancestors": copy.deepcopy(
                    systems_by_id[system_id].get("conceptual_ancestors", [])
                ),
                "genealogy_ids": copy.deepcopy(
                    systems_by_id[system_id]
                    .get("structural_identity", {})
                    .get("genealogy_ids", [])
                ),
            }
            for system_id in preferred_ids
        ],
    }
    committed_ancestor = {
        "ancestor_kind": (
            "genesis" if state_version == 0 else "verified_local_committed_state"
        ),
        "generation": state_version,
        "state": state,
        "state_semantic_digest": canonical_digest(state),
        "authority_boundary": (
            "exact state reopened from the local committed transcript; no "
            "external-state or independence authority"
        ),
    }
    source_projection = {
        "pre_map_policy": copy.deepcopy(dict(policy)),
        "realization": copy.deepcopy(dict(realization)),
        "literature_production_input": {
            "bundle_id": literature_bundle["bundle_id"],
            "bundle_digest": literature_bundle["bundle_digest"],
            "production_manifest_descriptor": copy.deepcopy(
                literature_bundle["production_manifest_descriptor"]
            ),
            "commitment_receipt_id": literature_bundle[
                "commitment_receipt"
            ]["receipt_id"],
            "commitment_receipt_digest": literature_bundle[
                "commitment_receipt"
            ]["receipt_digest"],
            "semantic_consumer_projection": copy.deepcopy(
                literature_projection
            ),
            "semantic_projection_digest": literature_projection[
                "projection_digest"
            ],
        },
        "producer_receipts": [
            *copy.deepcopy(role_receipts["source_routing_pre_map_policy"]),
            *copy.deepcopy(role_receipts["source_routing_realization"]),
        ],
        "authority_boundary": (
            "locally executed source-routing lineage only; source truth, external "
            "independence, and conceptual merit are not established"
        ),
    }
    generator_receipts = [
        *copy.deepcopy(role_receipts["high_risk_portfolio"]),
        *copy.deepcopy(role_receipts["parallel_portfolio"]),
        *copy.deepcopy(role_receipts["reflective_packets"]),
    ]
    adjudicator_receipts = [
        *copy.deepcopy(role_receipts["parent_conceptual_adjudication"]),
        *copy.deepcopy(role_receipts["synthesis_conceptual_adjudication"]),
    ]
    generator_authority = {
        "stage_order": [
            "high_risk_generation",
            "parallel_maturation",
            "parent_reflective_proposal",
            "parent_conceptual_adjudication",
            "synthesis_reflective_proposal",
            "synthesis_conceptual_adjudication",
        ],
        "generator_receipts": generator_receipts,
        "adjudicator_receipts": adjudicator_receipts,
        "stage_receipts": [
            {
                "stage_id": "high_risk_generation",
                "semantic_role": "high_risk_portfolio",
                "producer_receipt": copy.deepcopy(
                    role_receipts["high_risk_portfolio"][0]
                ),
            },
            {
                "stage_id": "parallel_maturation",
                "semantic_role": "parallel_portfolio",
                "producer_receipt": copy.deepcopy(
                    role_receipts["parallel_portfolio"][0]
                ),
            },
            {
                "stage_id": "parent_reflective_proposal",
                "semantic_role": "reflective_packets",
                "producer_receipt": copy.deepcopy(
                    role_receipts["reflective_packets"][0]
                ),
            },
            {
                "stage_id": "parent_conceptual_adjudication",
                "semantic_role": "parent_conceptual_adjudication",
                "producer_receipt": copy.deepcopy(
                    role_receipts["parent_conceptual_adjudication"][0]
                ),
            },
            {
                "stage_id": "synthesis_reflective_proposal",
                "semantic_role": "reflective_packets",
                "producer_receipt": copy.deepcopy(
                    role_receipts["reflective_packets"][1]
                ),
            },
            {
                "stage_id": "synthesis_conceptual_adjudication",
                "semantic_role": "synthesis_conceptual_adjudication",
                "producer_receipt": copy.deepcopy(
                    role_receipts["synthesis_conceptual_adjudication"][0]
                ),
            },
        ],
        "authority_boundary": (
            "receipts establish local execution lineage, not cognitive independence, "
            "creative merit, philosophical depth, or physics value"
        ),
    }
    return build_experiment_authority_projection(
        target_id=target_id,
        run_id=run_id,
        prior_state_version=state_version,
        committed_ancestor=committed_ancestor,
        theory_programme=programme,
        reflection_packet=packet,
        conceptual_systems=conceptual_system_projection,
        genealogy=genealogy,
        source_authority=source_projection,
        registered_claim=registered_claim,
        generator_authority=generator_authority,
        adjudication_authority=synthesis_evidence,
        schedule=schedule_value,
    )


def replay_canonical_world_authority_projection(
    observed_projection: Mapping[str, Any],
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    prior_state: Mapping[str, Any],
    final_reflection: Mapping[str, Any],
    conceptual_authority: Mapping[str, Any],
    source_authority_pair: Mapping[str, Any],
    literature_production_input_bundle: Mapping[str, Any],
    producers_by_role: Mapping[str, Sequence[Mapping[str, Any]]],
    schedule: Mapping[str, Any],
) -> dict[str, Any]:
    """Reject a commission projection unless it equals the cycle derivation."""

    observed = validate_experiment_authority_projection(observed_projection)
    expected = build_canonical_world_authority_projection(
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        prior_state=prior_state,
        final_reflection=final_reflection,
        conceptual_authority=conceptual_authority,
        source_authority_pair=source_authority_pair,
        literature_production_input_bundle=literature_production_input_bundle,
        producers_by_role=producers_by_role,
        schedule=schedule,
    )
    if observed != expected:
        observed_components = {
            row["component_kind"]: row for row in observed["components"]
        }
        expected_components = {
            row["component_kind"]: row for row in expected["components"]
        }
        component_differences = sorted(
            key
            for key in set(observed_components) | set(expected_components)
            if observed_components.get(key) != expected_components.get(key)
        )
        top_level_differences = sorted(
            key
            for key in set(observed) | set(expected)
            if key != "components" and observed.get(key) != expected.get(key)
        )
        raise ContractError(
            "caller-supplied world authority projection differs from cycle-derived "
            f"state: components={component_differences}, top_level={top_level_differences}"
        )
    return expected


def _json_bytes(value: Any) -> bytes:
    """Render deterministic, readable bytes for immutable commit artifacts."""

    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n"


def _canonical_semantic_output_rows(
    operator_id: str, payload: Mapping[str, Any]
) -> list[dict[str, str]]:
    """Extend dispatcher row closure to canonical authority producers.

    Source policy and realization producers are part of the canonical receipt
    wave, not untyped side files.  Their one decision-bearing row is the full
    self-digested authority object.  All other operators retain the shared
    dispatcher projection unchanged.
    """

    if operator_id == "source-routing-pre-map-policy-producer":
        return [
            {
                "semantic_kind": "source_routing_pre_map_policy",
                "semantic_id": str(payload["policy_id"]),
                "row_digest": canonical_digest(payload),
            }
        ]
    if operator_id == "source-routing-realization-producer":
        return [
            {
                "semantic_kind": "source_routing_realization",
                "semantic_id": str(payload["realization_id"]),
                "row_digest": canonical_digest(payload),
            }
        ]
    return semantic_output_rows(operator_id, payload)


def _role_paths(artifact_roles: Mapping[str, Any]) -> dict[str, list[str]]:
    """Normalize the explicit semantic-role to receipt-artifact routing table."""

    unknown = set(artifact_roles) - set(REQUIRED_ROLES) - set(OPTIONAL_ROLES)
    if unknown:
        raise ContractError(f"unknown canonical-cycle artifact roles: {sorted(unknown)}")
    normalized: dict[str, list[str]] = {}
    for role, raw in artifact_roles.items():
        values = [raw] if isinstance(raw, str) else list(raw) if isinstance(raw, Sequence) else []
        if not values or not all(isinstance(item, str) and item for item in values):
            raise ContractError(f"artifact role {role!r} requires one or more paths")
        normalized[role] = values
    for role in REQUIRED_ROLES:
        if role not in normalized:
            raise ContractError(f"canonical cycle is missing artifact role {role!r}")
    if normalized.get("source_routing_precommit"):
        raise ContractError(
            "legacy post-assimilation source-routing precommit is quarantined; "
            "canonical authority requires the policy-realization pair"
        )
    if len(normalized["literature_snapshot"]) != 1:
        raise ContractError("canonical cycle requires exactly one literature snapshot")
    if len(normalized["literature_production_input_bundle"]) != 1:
        raise ContractError(
            "canonical cycle requires exactly one committed literature-production input bundle"
        )
    if len(normalized["literature_assimilation"]) != 1:
        raise ContractError("canonical cycle requires exactly one literature assimilation packet")
    if len(normalized["high_risk_portfolio"]) != 1:
        raise ContractError("canonical cycle requires exactly one high-risk portfolio")
    if len(normalized["parallel_portfolio"]) != 1:
        raise ContractError("canonical cycle requires exactly one parallel portfolio")
    if len(normalized.get("source_routing_precommit", [])) not in {0, 1}:
        raise ContractError(
            "canonical source-routing precommit role has cardinality greater than one"
        )
    source_phase_cardinality = (
        len(normalized.get("source_routing_pre_map_policy", [])),
        len(normalized.get("source_routing_realization", [])),
    )
    if source_phase_cardinality not in {(0, 0), (1, 1)}:
        raise ContractError(
            "canonical source authority requires one pre-map policy and one post-assimilation realization, or neither locally"
        )
    adjudication_cardinality = tuple(
        len(normalized.get(role, [])) for role in CONCEPTUAL_ADJUDICATION_ROLES
    )
    if adjudication_cardinality not in {(0, 0), (1, 1)}:
        raise ContractError(
            "canonical conceptual authority requires exactly one parent and one synthesis "
            "adjudication artifact, or neither for local-only incubation"
        )
    if len(normalized.get("formal_claim_output", [])) not in {0, 1}:
        raise ContractError(
            "canonical formal-claim output role has cardinality greater than one"
        )
    flattened = [path for paths in normalized.values() for path in paths]
    if len(flattened) != len(set(flattened)):
        raise ContractError("one artifact path cannot impersonate multiple semantic roles")
    return normalized


def _verify_and_load_artifacts(
    *,
    workspace: Path,
    target_id: str,
    run_id: str,
    state_version: int,
    operator_requests: Sequence[Mapping[str, Any]],
    operator_receipts: Sequence[Mapping[str, Any]],
    artifact_roles: Mapping[str, Any],
) -> tuple[
    dict[str, list[dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
    dict[str, list[str]],
    dict[str, list[str]],
    dict[str, bytes],
]:
    """Verify requests/receipts, then load only successful, role-bound outputs.

    The base readiness check enforces required operators.  A second per-success
    check also verifies successful optional operators, which the base contract
    intentionally ignores when they are absent or fail.
    """

    role_paths = _role_paths(artifact_roles)
    requests = [dict(item) for item in operator_requests]
    receipts = [dict(item) for item in operator_receipts]
    if not requests or not receipts:
        raise ContractError("canonical cycle requires operator requests and attempt receipts")
    request_by_id: dict[str, dict[str, Any]] = {}
    expected = (target_id, run_id, state_version)
    for request in requests:
        validate_operator_request_identity(request)
        identity = request["identity"]
        actual = (identity["target_id"], identity["run_id"], identity["state_version"])
        if actual != expected:
            raise ContractError(f"operator request crossed target/run/state: expected {expected}, got {actual}")
        if request["request_id"] in request_by_id:
            raise ContractError(f"duplicate operator request: {request['request_id']}")
        expected_input_digest = canonical_digest(
            {
                "identity": request["identity"],
                "operator": request["operator"],
                "parameters": request.get("parameters", {}),
                "input_artifacts": request.get("input_artifacts", []),
                "declared_outputs": request.get("declared_outputs", []),
            }
        )
        if request["input_digest"] != expected_input_digest:
            raise ContractError(f"operator request input digest is invalid: {request['request_id']}")
        request_by_id[request["request_id"]] = request
    receipt_ids: set[str] = set()
    for receipt in receipts:
        validate_operator_receipt_identity(receipt)
        if receipt["receipt_id"] in receipt_ids:
            raise ContractError(f"duplicate operator receipt: {receipt['receipt_id']}")
        receipt_ids.add(receipt["receipt_id"])
        identity = receipt["identity"]
        actual = (identity["target_id"], identity["run_id"], identity["state_version"])
        if actual != expected:
            raise ContractError(f"operator receipt crossed target/run/state: expected {expected}, got {actual}")
        if receipt["request_id"] not in request_by_id:
            raise ContractError(f"operator receipt has no supplied request: {receipt['receipt_id']}")
        request = request_by_id[receipt["request_id"]]
        validate_operator_receipt_identity(receipt, request)
        if any(
            receipt[field] != request[field]
            for field in ("invocation_id", "operator", "identity", "required", "input_digest")
        ):
            raise ContractError(
                f"operator receipt does not exactly bind its sealed request: {receipt['receipt_id']}"
            )
        output_digests = [descriptor["sha256"] for descriptor in receipt["output_history_artifacts"]]
        for validator_receipt in receipt["validator_receipts"]:
            if validator_receipt.get("artifact_digests") != output_digests:
                raise ContractError(
                    f"validator receipt does not bind the exact output set: {receipt['receipt_id']}"
                )
    missing_attempts = set(request_by_id) - {receipt["request_id"] for receipt in receipts}
    if missing_attempts:
        raise ContractError(
            f"operator requests lack terminal attempt receipts: {sorted(missing_attempts)}"
        )
    ensure_evaluation_ready(requests, receipts, workspace=workspace)

    successful = [receipt for receipt in receipts if receipt["status"] == "succeeded"]
    for receipt in successful:
        request = copy.deepcopy(request_by_id[receipt["request_id"]])
        request["required"] = True
        ensure_evaluation_ready([request], [receipt], workspace=workspace)

    producers_by_path: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for receipt in successful:
        for descriptor in receipt["output_artifacts"]:
            producers_by_path[descriptor["path"]].append(receipt)
    payloads: dict[str, list[dict[str, Any]]] = {}
    role_source_bytes: dict[str, bytes] = {}
    producers_by_role: dict[str, list[dict[str, Any]]] = {}
    receipt_roles: dict[str, list[str]] = defaultdict(list)
    for role, paths in role_paths.items():
        payloads[role] = []
        producers_by_role[role] = []
        for raw_path in paths:
            producers = producers_by_path.get(raw_path, [])
            if len(producers) > 1:
                raise ContractError(
                    f"artifact role {role!r} has ambiguous successful producers: {raw_path}"
                )
            if not producers and role not in EXTERNAL_ROLE_ARTIFACTS:
                raise ContractError(f"artifact role {role!r} is not backed by a successful receipt: {raw_path}")
            if producers:
                producer = producers[0]
                original_index = next(
                    index
                    for index, descriptor in enumerate(producer["output_artifacts"])
                    if descriptor["path"] == raw_path
                )
                source_descriptor = producer["output_history_artifacts"][original_index]
                path = resolve_workspace_path(
                    workspace, source_descriptor["path"], must_exist=True
                )
                data = path.read_bytes()
                if (
                    bytes_digest(data) != source_descriptor["sha256"]
                    or len(data) != source_descriptor["size_bytes"]
                ):
                    raise ContractError(f"immutable output history changed: {raw_path}")
            else:
                path = resolve_workspace_path(workspace, raw_path, must_exist=True)
                data = path.read_bytes()
            try:
                payload = json.loads(data)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ContractError(f"role artifact is not readable JSON: {raw_path}: {exc}") from exc
            if not isinstance(payload, dict):
                raise ContractError(f"role artifact must contain a JSON object: {raw_path}")
            payloads[role].append(payload)
            role_source_bytes[raw_path] = data
            producers_by_role[role].extend(producers)
            for producer in producers:
                receipt_roles[producer["receipt_id"]].append(role)
    # Role assignment is a bijection over successful output paths, not merely
    # over receipts.  A multi-output receipt cannot hide an unconsumed file
    # behind one role-bound sibling.  The literature snapshot is the one
    # permitted external decision artifacts.  The snapshot is validated as the
    # frozen assimilation input; the production bundle independently replays
    # its exact manifest descriptor, commitment receipt, and semantic values.
    successful_output_paths = {
        descriptor["path"]
        for receipt in successful
        for descriptor in receipt["output_artifacts"]
    }
    role_output_paths = {
        path
        for paths in role_paths.values()
        for path in paths
        if producers_by_path.get(path)
    }
    if successful_output_paths != role_output_paths:
        raise ContractError(
            "successful output/semantic-role bijection failed: "
            f"unassigned={sorted(successful_output_paths - role_output_paths)}, "
            f"nonoutput={sorted(role_output_paths - successful_output_paths)}"
        )
    unused = {receipt["receipt_id"] for receipt in successful} - set(receipt_roles)
    if unused:
        raise ContractError(f"successful operator outputs were not assigned a consumer role: {sorted(unused)}")
    return (
        payloads,
        producers_by_role,
        {key: sorted(set(value)) for key, value in receipt_roles.items()},
        role_paths,
        role_source_bytes,
    )


def _digest_without(payload: Mapping[str, Any], key: str) -> str:
    """Return the conventional self-digest for one top-level digest field."""

    return canonical_digest({name: value for name, value in payload.items() if name != key})


def _validate_reflective_packet(packet: Mapping[str, Any], *, active_literature: bool) -> None:
    """Validate a reflection packet under active or local-incubation authority."""

    validate_payload(dict(packet), "reflective_conceptual_discovery_packet.schema.json")
    if packet.get("packet_digest") != _digest_without(packet, "packet_digest"):
        raise ContractError("reflective packet content digest mismatch")
    if active_literature:
        validate_packet_invariants(packet)
        return
    # A local-only snapshot may feed structural incubation, never a self-certified
    # preference.  Search provenance overrides an upstream packet's freshness
    # label, so only its conservative structural content is admissible here.
    if packet.get("generation_mode") != "local_structural_fallback":
        raise ContractError("local-only reflection must use local_structural_fallback mode")
    gates = packet.get("stage_gates", {})
    preference = str(packet.get("truth_convergence_status", {}).get("conceptual_preference", ""))
    if gates.get("G2_philosophical_depth") == "pass" or gates.get("G4_understanding_gain") == "pass":
        raise ContractError("local-only reflection cannot self-certify depth or understanding")
    if preference.startswith("theoretically_preferred"):
        raise ContractError("local-only reflection cannot authorize theoretical preference")
    if packet.get("support_probe", {}).get("disposition") != "no_probe_needed":
        raise ContractError("local-only incubation cannot commission a support experiment")


def _validate_core_identity(
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    prior_state: Mapping[str, Any],
    payloads: Mapping[str, list[dict[str, Any]]],
    workspace: Path,
    present_use_at: dt.datetime,
) -> tuple[str, str, str]:
    """Validate core schemas and one cross-artifact theory/literature identity."""

    snapshot = payloads["literature_snapshot"][0]
    assimilation = payloads["literature_assimilation"][0]
    portfolio = payloads["high_risk_portfolio"][0]
    parallel = payloads["parallel_portfolio"][0]
    reflections = payloads["reflective_packets"]
    validate_snapshot(snapshot)
    validate_assimilation(assimilation, snapshot=snapshot)
    validate_high_risk_portfolio(portfolio)
    validate_parallel_portfolio(parallel)

    if any(item.get("target_id") != target_id for item in (snapshot, assimilation, portfolio, parallel)):
        raise ContractError("a core discovery artifact targets another problem")
    theory_digest = canonical_digest(prior_state)
    named_theory_digests = {
        snapshot.get("theory_state_digest"),
        assimilation.get("theory_state_digest"),
        portfolio.get("theory_state_digest"),
        parallel.get("base_theory_digest"),
    }
    if named_theory_digests != {theory_digest}:
        raise ContractError(
            "core artifacts are stale or cross-state: their theory digests do not bind the frozen canonical state"
        )
    if parallel.get("base_theory_state_version") != state_version:
        raise ContractError("parallel portfolio is bound to another state generation")

    literature_digest = snapshot["content_digest"]
    literature_id = snapshot["snapshot_id"]
    selected = assimilation.get("selected_snapshot", {})
    named_literature_digests = {
        literature_digest,
        selected.get("content_digest"),
        portfolio.get("literature_snapshot_digest"),
        parallel.get("literature_snapshot_digest"),
    }
    named_literature_ids = {
        literature_id,
        selected.get("snapshot_id"),
        portfolio.get("literature_snapshot_id"),
        parallel.get("literature_snapshot_id"),
    }
    if len(named_literature_digests) != 1 or len(named_literature_ids) != 1:
        raise ContractError("core discovery artifacts use stale or different literature snapshots")

    present_freshness = resolve_present_literature_freshness(
        assimilation, now=present_use_at
    )
    freshness = present_freshness["freshness_status"]
    investment_gate = present_freshness["active_investment_gate"]
    lane_receipts = snapshot.get("lane_receipts", [])
    snapshot_validators = snapshot.get("validator_receipts", [])
    source_ids_by_lane = {
        receipt["lane_id"]: sorted(
            source["source_id"]
            for source in snapshot.get("sources", [])
            if receipt["lane_id"] in source.get("lane_ids", [])
        )
        for receipt in lane_receipts
    }
    # Receipt identities are derived from the content they validate. A caller
    # cannot promote a snapshot merely by asserting ``execution_mode=live`` and
    # ``status=completed``: the complete lane record, its reduced source set,
    # the lane validator link, and the snapshot validator must be one
    # digest-bound structure. ``validate_snapshot`` above has already
    # recomputed every lane, source, and snapshot digest.
    lane_receipt_integrity = all(
        receipt.get("source_ids") == source_ids_by_lane.get(receipt.get("lane_id"), [])
        and receipt.get("validator_receipt_ids")
        == [
            stable_identifier(
                "validator",
                receipt.get("lane_id"),
                receipt.get("content_digest"),
            )
        ]
        for receipt in lane_receipts
    )
    snapshot_validator_integrity = all(
        row.get("receipt_id")
        == expected_snapshot_validator_receipt_id(
            snapshot, str(row.get("validator_id") or "")
        )
        for row in snapshot_validators
    )
    live_boundary_valid = (
        len(lane_receipts) == 6
        and {row.get("lane_type") for row in lane_receipts} == set(LANE_TYPES)
        and all(
            row.get("execution_mode") == "live"
            and row.get("status") == "completed"
            and row.get("provider")
            and row.get("index")
            and row.get("queries")
            and row.get("validator_receipt_ids")
            for row in lane_receipts
        )
        and lane_receipt_integrity
        and bool(snapshot_validators)
        and snapshot.get("validation_status") == "validated"
        and snapshot_validator_integrity
        and all(
            row.get("status") == "passed"
            and row.get("validated_digest") == snapshot.get("content_digest")
            and row.get("receipt_id")
            for row in snapshot_validators
        )
    )
    if (
        snapshot.get("provenance_mode") == "live"
        and freshness == "current"
        and investment_gate == "pass"
        and live_boundary_valid
    ):
        literature_mode = "active_current"
    elif (
        snapshot.get("provenance_mode") == "local_only"
        and freshness == "local_only"
        and investment_gate == "blocked_local_only"
    ):
        literature_mode = "local_only_incubation"
    else:
        raise ContractError("stale, invalid, or ambiguous literature cannot enter a canonical cycle")

    legacy_precommits = payloads.get("source_routing_precommit", [])
    source_phase_cardinality = (
        len(payloads.get("source_routing_pre_map_policy", [])),
        len(payloads.get("source_routing_realization", [])),
    )
    if literature_mode == "active_current":
        if legacy_precommits:
            raise ContractError(
                "legacy post-assimilation source-routing precommit is compatibility-only and cannot authorize canonical mapping"
            )
        if source_phase_cardinality != (1, 1):
            raise ContractError(
                "active-current canonical discovery requires a pre-map policy and post-assimilation realization"
            )
    elif legacy_precommits or source_phase_cardinality != (0, 0):
        raise ContractError(
            "local-only incubation cannot fabricate active two-phase source-routing authority"
        )

    reducer_status = parallel.get("reducer_receipt", {}).get("compare_and_swap_status")
    if reducer_status == "committed":
        raise ContractError("parallel workers cannot pre-commit the canonical state transition")
    rebase_status = parallel.get("literature_rebase", {}).get("status")
    if rebase_status == "rebase_blocked" and reflections:
        raise ContractError("reflection cannot consume branches whose literature basis is superseded")
    active = literature_mode == "active_current"
    adjudication_cardinality = tuple(
        len(payloads.get(role, [])) for role in CONCEPTUAL_ADJUDICATION_ROLES
    )
    if active and adjudication_cardinality != (1, 1):
        raise ContractError(
            "active-current canonical discovery requires ordered parent and synthesis adjudications"
        )
    if not active and adjudication_cardinality != (0, 0):
        raise ContractError(
            "local-only incubation requires absent conceptual adjudication roles"
        )
    for packet in reflections:
        if (
            packet.get("target_id") != target_id
            or packet.get("run_id") != run_id
            or packet.get("state_version") != state_version
        ):
            raise ContractError("reflective packet crossed target/run/state identity")
        basis = packet.get("literature_basis", {})
        if (
            basis.get("snapshot_target_id") != target_id
            or basis.get("selected_snapshot_id") != literature_id
            or basis.get("selected_snapshot_digest") != literature_digest
        ):
            raise ContractError("reflective packet uses another literature basis")
        selected_ids = set(packet.get("high_risk_hypothesis_portfolio", {}).get("selected_hypothesis_ids", []))
        portfolio_ids = {row["hypothesis_id"] for row in portfolio.get("hypotheses", [])}
        if not selected_ids.issubset(portfolio_ids):
            raise ContractError("reflective packet names hypotheses absent from the canonical portfolio")
        _validate_reflective_packet(packet, active_literature=active)

    if "experiment_spec" in payloads:
        if not active:
            raise ContractError("local-only incubation cannot commission or consume an experiment")
        spec = payloads["experiment_spec"][0]
        receipt = payloads["experiment_receipt"][0]
        validate_experiment_receipt(receipt, spec, work_directory=workspace)
        if (
            receipt.get("target_id") != target_id
            or receipt.get("run_id") != run_id
            or receipt.get("state_version") != state_version
        ):
            raise ContractError("experiment crossed target/run/state identity")
        programme_ids = {row["theoretical_programme"]["programme_id"] for row in reflections}
        system_ids = {
            system["system_id"]
            for row in reflections
            for system in row.get("conceptual_systems", [])
        }
        if receipt.get("theory_programme_id") not in programme_ids:
            raise ContractError("experiment is not bound to a consumed theory programme")
        if not set(receipt.get("conceptual_system_ids", [])).issubset(system_ids):
            raise ContractError("experiment is not bound to consumed conceptual systems")
        if not any(row.get("support_probe", {}).get("disposition") in {"commissioned", "assimilated"} for row in reflections):
            raise ContractError("an experiment cannot override a no_probe_needed theory decision")
    return literature_mode, literature_id, literature_digest


def validate_source_authority_pair_execution(
    *,
    active_required: bool,
    payloads: Mapping[str, list[dict[str, Any]]],
    producers_by_role: Mapping[str, list[dict[str, Any]]],
    operator_requests: Sequence[Mapping[str, Any]],
    operator_receipts: Sequence[Mapping[str, Any]],
    input_payloads: Mapping[str, list[dict[str, Any]]],
    require_artifact_producers: bool = False,
) -> dict[str, Any] | None:
    """Replay pre-map policy plus post-assimilation realization and dispatch use."""

    policy_values = payloads.get("source_routing_pre_map_policy", [])
    realization_values = payloads.get("source_routing_realization", [])
    if not active_required:
        if policy_values or realization_values:
            raise ContractError(
                "non-active literature cannot carry two-phase source-routing authority"
            )
        if any(
            envelope.get("source_routing_pre_map_policy") is not None
            or envelope.get("source_routing_realization") is not None
            for envelopes in input_payloads.values()
            for envelope in envelopes
        ):
            raise ContractError(
                "non-active operator envelope smuggles two-phase source-routing authority"
            )
        return None
    if len(policy_values) != 1 or len(realization_values) != 1:
        raise ContractError(
            "active source routing requires one exact pre-map policy and realization"
        )
    policy = policy_values[0]
    realization = realization_values[0]
    snapshot = payloads["literature_snapshot"][0]
    assimilation = payloads["literature_assimilation"][0]
    requests_by_id = {
        str(request["request_id"]): request for request in operator_requests
    }
    source_producers: dict[str, Mapping[str, Any]] = {}
    if require_artifact_producers:
        for role, expected_operator_id in SOURCE_AUTHORITY_PRODUCER_ROLES.items():
            producers = producers_by_role.get(role, [])
            if len(producers) != 1:
                raise ContractError(
                    f"active source authority role {role} requires exactly one successful producer"
                )
            producer = producers[0]
            request = requests_by_id.get(str(producer.get("request_id", "")))
            artifact = policy if role == "source_routing_pre_map_policy" else realization
            artifact_id = (
                artifact["policy_id"]
                if role == "source_routing_pre_map_policy"
                else artifact["realization_id"]
            )
            if (
                producer.get("status") != "succeeded"
                or producer.get("operator", {}).get("operator_id")
                != expected_operator_id
                or request is None
                or request.get("operator", {}).get("operator_id")
                != expected_operator_id
                or request.get("parameters", {}).get("producer_role") != role
                or request.get("parameters", {}).get("artifact_id") != artifact_id
                or request.get("parameters", {}).get("artifact_digest")
                != canonical_digest(artifact)
            ):
                raise ContractError(
                    f"active source authority role {role} crossed its exact producer request/receipt"
                )
            envelopes = input_payloads.get(str(request["request_id"]), [])
            if len(envelopes) != 1 or not _same_payload(
                envelopes[0].get("authority_artifact"), artifact
            ):
                raise ContractError(
                    f"active source authority role {role} producer did not consume its exact artifact"
                )
            outputs = producer.get("output_artifacts", [])
            histories = producer.get("output_history_artifacts", [])
            if (
                len(outputs) != 1
                or len(histories) != 1
                or outputs[0].get("path") not in request.get("declared_outputs", [])
                or outputs[0].get("sha256") != histories[0].get("sha256")
                or outputs[0].get("size_bytes") != histories[0].get("size_bytes")
                or outputs[0].get("namespace") != histories[0].get("namespace")
            ):
                raise ContractError(
                    f"active source authority role {role} lacks exact output/history evidence"
                )
            source_producers[role] = producer
    # Recompute the public deterministic warrant projection from the sealed
    # snapshot.  The realization still has to bind the exact stage receipts;
    # this replay merely avoids trusting caller-supplied semantic warrants.
    validated_warrants = derive_source_routing_semantic_warrants(snapshot)
    acquisition_completion = policy.get("acquisition_completion", {})
    validated_policy = validate_source_routing_pre_map_policy(
        policy,
        authority=policy["acquisition_authority"],
        snapshot=snapshot,
        acquisition_producer_receipt=acquisition_completion,
        algorithm_contracts=policy["algorithm_contracts"],
    )
    validated_realization = validate_source_routing_realization(
        realization,
        policy=validated_policy,
        authority=validated_policy["acquisition_authority"],
        snapshot=snapshot,
        acquisition_producer_receipt=acquisition_completion,
        algorithm_contracts=validated_policy["algorithm_contracts"],
        validated_warrants=validated_warrants,
        claim_mappings=assimilation["theory_mappings"],
        assimilation=assimilation,
        stage_receipts=realization["stage_receipts"],
    )
    policy_sealed_at = _parse_timestamp(
        str(validated_policy["sealed_at"]), "source-routing pre-map policy"
    )
    realization_completed_at = _parse_timestamp(
        str(validated_realization["completed_at"]), "source-routing realization"
    )
    if require_artifact_producers:
        policy_producer = source_producers["source_routing_pre_map_policy"]
        realization_producer = source_producers["source_routing_realization"]
        assimilation_producers = producers_by_role.get("literature_assimilation", [])
        if len(assimilation_producers) != 1:
            raise ContractError(
                "active source authority requires one exact assimilation producer"
            )
        assimilation_producer = assimilation_producers[0]
        if _parse_timestamp(
            str(policy_producer["completed_at"]), "source policy producer completion"
        ) > _parse_timestamp(
            str(assimilation_producer["started_at"]), "assimilation producer start"
        ):
            raise ContractError(
                "source-routing pre-map policy producer completed after assimilation began"
            )
        if _parse_timestamp(
            str(realization_producer["completed_at"]),
            "source realization producer completion",
        ) < realization_completed_at:
            raise ContractError(
                "source-routing realization claims completion after its producer receipt"
            )
    receipts_by_request: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for receipt in operator_receipts:
        receipts_by_request[str(receipt["request_id"])].append(receipt)
    required_operator_ids = set(
        validated_realization["downstream_consumption_contract"][
            "required_operator_ids"
        ]
    )
    present_required_counts: dict[str, int] = defaultdict(int)
    for request in operator_requests:
        operator_id = str(request["operator"]["operator_id"])
        request_id = str(request["request_id"])
        envelopes = input_payloads.get(request_id, [])
        if len(envelopes) != 1:
            raise ContractError(
                f"source-routing consumer {operator_id} lacks one sealed input envelope"
            )
        envelope = envelopes[0]
        if operator_id == "frontier-literature-assimilator":
            if not _same_payload(
                envelope.get("source_routing_pre_map_policy"), validated_policy
            ) or envelope.get("source_routing_realization") is not None:
                raise ContractError(
                    "assimilation must consume the exact pre-map policy before realization exists"
                )
            successful = [
                receipt
                for receipt in receipts_by_request.get(request_id, [])
                if receipt.get("status") == "succeeded"
            ]
            if len(successful) != 1 or _parse_timestamp(
                str(successful[0]["started_at"]), "assimilation start"
            ) < policy_sealed_at:
                raise ContractError("assimilation did not execute after the sealed pre-map policy")
            continue
        if operator_id not in required_operator_ids:
            continue
        present_required_counts[operator_id] += 1
        if not _same_payload(
            envelope.get("source_routing_pre_map_policy"), validated_policy
        ) or not _same_payload(
            envelope.get("source_routing_realization"), validated_realization
        ):
            raise ContractError(
                f"downstream operator {operator_id} did not consume the exact policy-realization pair"
            )
        successful = [
            receipt
            for receipt in receipts_by_request.get(request_id, [])
            if receipt.get("status") == "succeeded"
        ]
        if len(successful) != 1:
            raise ContractError(
                f"source-routing consumer {operator_id} lacks one successful attempt"
            )
        if _parse_timestamp(
            str(successful[0].get("started_at")),
            f"{operator_id} start",
        ) < realization_completed_at:
            raise ContractError(
                f"source-routing realization was created after {operator_id} dispatch"
            )
        if require_artifact_producers and _parse_timestamp(
            str(successful[0].get("started_at")),
            f"{operator_id} start",
        ) < _parse_timestamp(
            str(source_producers["source_routing_realization"]["completed_at"]),
            "source realization producer completion",
        ):
            raise ContractError(
                f"source-routing realization producer completed after {operator_id} dispatch"
            )
    mandatory_counts = {
        "high-risk-hypothesis-forger": 1,
        "parallel-hypothesis-portfolio": 1,
        "reflective-conceptual-discovery": 1,
        "reflective-theory-synthesizer": 1,
        "blind-conceptual-preference-adjudicator": 2,
    }
    if any(
        present_required_counts[operator_id] != count
        for operator_id, count in mandatory_counts.items()
    ):
        raise ContractError(
            "two-phase source authority lacks the exact mandatory downstream cardinalities"
        )
    return {
        "pre_map_policy": validated_policy,
        "realization": validated_realization,
    }


def _same_payload(left: Any, right: Any) -> bool:
    """Compare nested stage payloads by canonical meaning, not object identity."""

    return isinstance(left, Mapping) and canonical_digest(left) == canonical_digest(right)


def _validate_stage_causality(
    *,
    operator_requests: Sequence[Mapping[str, Any]],
    input_payloads: Mapping[str, list[dict[str, Any]]],
    payloads: Mapping[str, list[dict[str, Any]]],
    producers_by_role: Mapping[str, list[dict[str, Any]]],
    role_paths: Mapping[str, list[str]],
) -> None:
    """Prove that downstream operator inputs contain exact upstream outputs.

    Dispatcher receipts bind the input-envelope bytes.  This check completes the
    causal chain by comparing the nested domain packet at each stage with the
    exact object named by the upstream output descriptor.  A collection of
    independently valid but disconnected fixtures therefore cannot be committed.
    """

    snapshot = payloads["literature_snapshot"][0]
    literature_bundles = payloads.get("literature_production_input_bundle", [])
    if len(literature_bundles) != 1:
        raise ContractError(
            "theory causality requires one committed literature-production input bundle"
        )
    literature_bundle = validate_portable_literature_production_input_bundle(
        literature_bundles[0]
    )
    literature_projection = literature_bundle["semantic_consumer_projection"]
    assimilation = payloads["literature_assimilation"][0]
    portfolio = payloads["high_risk_portfolio"][0]
    parallel = payloads["parallel_portfolio"][0]
    reflections = payloads["reflective_packets"]
    by_operator: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for request in operator_requests:
        by_operator[str(request["operator"]["operator_id"])].append(request)

    if (
        literature_bundle.get("target_id") != snapshot.get("target_id")
        or literature_bundle.get("state_version")
        != parallel.get("base_theory_state_version")
        or literature_projection.get("target_id") != snapshot.get("target_id")
        or literature_projection.get("state_version")
        != parallel.get("base_theory_state_version")
    ):
        raise ContractError(
            "committed literature-production input crossed theory target or generation"
        )

    literature_projection_consumers = frozenset(
        {
            "high-risk-hypothesis-forger",
            "parallel-hypothesis-portfolio",
            "reflective-conceptual-discovery",
            "reflective-theory-synthesizer",
            "local-reflective-incubator",
            "local-reflective-synthesizer",
            "blind-conceptual-preference-adjudicator",
        }
    )
    projection_digest = literature_projection["projection_digest"]
    for operator_id in literature_projection_consumers:
        for request in by_operator.get(operator_id, []):
            values = input_payloads.get(str(request["request_id"]), [])
            if len(values) != 1 or not _same_payload(
                values[0].get("literature_production_projection"),
                literature_projection,
            ):
                raise ContractError(
                    f"conceptual operator {operator_id} did not consume the exact committed literature projection"
                )
            if request.get("parameters", {}).get(
                "literature_production_projection_digest"
            ) != projection_digest:
                raise ContractError(
                    f"conceptual operator {operator_id} did not bind the committed literature projection digest"
                )

    def envelopes(operator_id: str) -> list[dict[str, Any]]:
        output: list[dict[str, Any]] = []
        for request in by_operator.get(operator_id, []):
            values = input_payloads.get(str(request["request_id"]), [])
            if len(values) != 1:
                raise ContractError(f"operator {operator_id} must have one frozen causal envelope")
            value = values[0]
            if not isinstance(value, dict):
                raise ContractError(f"causal envelope for {operator_id} must be an object")
            output.append(value)
        return output

    for envelope in envelopes("frontier-literature-assimilator"):
        if not _same_payload(envelope.get("snapshot"), snapshot):
            raise ContractError("literature assimilation did not consume the exact frozen snapshot")
    for envelope in envelopes("high-risk-hypothesis-forger"):
        if not _same_payload(envelope.get("literature_snapshot"), snapshot):
            raise ContractError("high-risk generation did not consume the exact literature snapshot")
        if not _same_payload(envelope.get("assimilation_packet"), assimilation):
            raise ContractError("high-risk generation did not consume the exact assimilation packet")
    for envelope in envelopes("parallel-hypothesis-portfolio"):
        if not _same_payload(envelope.get("high_risk_portfolio"), portfolio):
            raise ContractError("parallel maturation did not consume the exact high-risk portfolio")
    for envelope in envelopes("reflective-conceptual-discovery"):
        if not _same_payload(envelope.get("high_risk_portfolio"), portfolio):
            raise ContractError("reflective parent did not consume the exact high-risk portfolio")
        if not _same_payload(envelope.get("parallel_portfolio"), parallel):
            raise ContractError("reflective parent did not consume the exact parallel portfolio")
        basis = envelope.get("literature_basis", {})
        if not isinstance(basis, Mapping) or basis.get("selected_snapshot_digest") != snapshot["content_digest"]:
            raise ContractError("reflective parent did not consume the exact literature digest")
    local_portfolio = copy.deepcopy(portfolio)
    for hypothesis in local_portfolio.get("hypotheses", []):
        hypothesis.pop("literature_rebase_receipt", None)
        hypothesis["concept_lifecycle_state"] = "incubating"
    for envelope in envelopes("local-reflective-incubator"):
        if not _same_payload(envelope.get("high_risk_portfolio"), local_portfolio):
            raise ContractError(
                "local reflective parent did not consume the exact deterministic incubation projection"
            )
        if not _same_payload(envelope.get("parallel_portfolio"), parallel):
            raise ContractError("local reflective parent did not consume the exact parallel portfolio")
        basis = envelope.get("literature_basis", {})
        if not isinstance(basis, Mapping) or basis.get("selected_snapshot_digest") != snapshot["content_digest"]:
            raise ContractError("local reflective parent did not consume the exact literature digest")
    synthesis_envelopes = [
        *envelopes("reflective-theory-synthesizer"),
        *envelopes("local-reflective-synthesizer"),
    ]
    if synthesis_envelopes:
        if len(reflections) < 2:
            raise ContractError("a synthesizer receipt requires parent and synthesized reflective packets")
        parent_packet = reflections[-2]
        for envelope in synthesis_envelopes:
            if not _same_payload(envelope.get("prior_reflective_packet"), parent_packet):
                raise ContractError("reflective synthesizer did not consume the exact parent packet")
            if not _same_payload(envelope.get("parallel_portfolio"), parallel):
                raise ContractError("reflective synthesizer did not consume the exact parallel branch results")
            if envelope in envelopes("local-reflective-synthesizer") and not _same_payload(
                envelope.get("high_risk_portfolio"), local_portfolio
            ):
                raise ContractError(
                    "local reflective synthesizer did not preserve the exact incubation projection"
                )

    adjudication_envelopes = envelopes("blind-conceptual-preference-adjudicator")
    parent_evidence_rows = payloads.get("parent_conceptual_adjudication", [])
    synthesis_evidence_rows = payloads.get("synthesis_conceptual_adjudication", [])
    if parent_evidence_rows or synthesis_evidence_rows:
        if (
            len(reflections) < 2
            or len(parent_evidence_rows) != 1
            or len(synthesis_evidence_rows) != 1
            or len(adjudication_envelopes) != 2
        ):
            raise ContractError(
                "active conceptual authority requires parent proposal -> adjudication -> "
                "synthesis -> adjudication exactly once"
            )
        parent_packet, synthesis_packet = reflections[-2], reflections[-1]
        parent_evidence = parent_evidence_rows[0]
        synthesis_evidence = synthesis_evidence_rows[0]

        def matching_adjudication_envelope(
            evidence: Mapping[str, Any], packet: Mapping[str, Any]
        ) -> dict[str, Any]:
            matching = [
                envelope
                for envelope in adjudication_envelopes
                if _same_payload(envelope.get("blind_packet"), evidence.get("blind_packet"))
                and _same_payload(
                    {"systems": envelope.get("systems")},
                    {"systems": packet.get("conceptual_systems")},
                )
                and _same_payload(
                    {"reflection_rounds": envelope.get("reflection_rounds")},
                    {"reflection_rounds": packet.get("reflection_rounds")},
                )
            ]
            if len(matching) != 1:
                raise ContractError(
                    f"conceptual adjudication stage {evidence.get('stage_id')} lacks one exact causal envelope"
                )
            return matching[0]

        parent_adjudication_envelope = matching_adjudication_envelope(
            parent_evidence, parent_packet
        )
        synthesis_adjudication_envelope = matching_adjudication_envelope(
            synthesis_evidence, synthesis_packet
        )
        if (
            parent_adjudication_envelope.get("previous_evidence") is not None
            or parent_adjudication_envelope.get("previous_evidence_digest") is not None
        ):
            raise ContractError("parent conceptual adjudication cannot consume prior authority")
        if not _same_payload(
            synthesis_adjudication_envelope.get("previous_evidence"), parent_evidence
        ):
            raise ContractError(
                "synthesis conceptual adjudication did not consume the complete parent evidence"
            )
        if synthesis_adjudication_envelope.get(
            "previous_evidence_digest"
        ) != parent_evidence.get("evidence_digest"):
            raise ContractError(
                "synthesis adjudication previous-evidence descriptor is not exact"
            )
        if len(synthesis_envelopes) != 1 or not _same_payload(
            synthesis_envelopes[0].get("previous_evidence"), parent_evidence
        ):
            raise ContractError(
                "reflective synthesizer did not consume the complete parent adjudication evidence"
            )

        parent_packet_path = role_paths["reflective_packets"][-2]
        synthesis_packet_path = role_paths["reflective_packets"][-1]
        parent_producers = [
            receipt
            for receipt in producers_by_role.get("reflective_packets", [])
            if any(
                descriptor.get("path") == parent_packet_path
                for descriptor in receipt.get("output_artifacts", [])
            )
        ]
        synthesis_producers = [
            receipt
            for receipt in producers_by_role.get("reflective_packets", [])
            if any(
                descriptor.get("path") == synthesis_packet_path
                for descriptor in receipt.get("output_artifacts", [])
            )
        ]
        parent_adjudication_producers = producers_by_role.get(
            "parent_conceptual_adjudication", []
        )
        synthesis_adjudication_producers = producers_by_role.get(
            "synthesis_conceptual_adjudication", []
        )
        if not (
            len(parent_producers) == 1
            and len(synthesis_producers) == 1
            and len(parent_adjudication_producers) == 1
            and len(synthesis_adjudication_producers) == 1
        ):
            raise ContractError("conceptual authority stage producers are ambiguous")
        if parent_evidence.get("input_binding", {}).get("proposer_receipt_ids") != [
            parent_producers[0]["receipt_id"]
        ]:
            raise ContractError("parent adjudication does not bind its exact proposal receipt")
        if synthesis_evidence.get("input_binding", {}).get("proposer_receipt_ids") != [
            synthesis_producers[0]["receipt_id"]
        ]:
            raise ContractError("synthesis adjudication does not bind its exact proposal receipt")
        stage_receipts = [
            parent_producers[0],
            parent_adjudication_producers[0],
            synthesis_producers[0],
            synthesis_adjudication_producers[0],
        ]
        for earlier, later in zip(stage_receipts, stage_receipts[1:]):
            if _parse_timestamp(
                str(earlier["completed_at"]), "conceptual authority completion"
            ) > _parse_timestamp(str(later["started_at"]), "conceptual authority start"):
                raise ContractError("conceptual authority operator stages are not causally ordered")
    elif adjudication_envelopes:
        raise ContractError(
            "conceptual adjudicator execution cannot exist without both canonical evidence roles"
        )
    for envelope in envelopes("dynamic-symbolic-simulation-experimenter"):
        if "experiment_receipt" not in payloads:
            raise ContractError("experiment operator succeeded without a consumed experiment receipt")
        triage = envelope.get("triage_request", {})
        programme_ids = {packet["theoretical_programme"]["programme_id"] for packet in reflections}
        if not isinstance(triage, Mapping) or triage.get("theory_programme_id") not in programme_ids:
            raise ContractError("experiment was not commissioned by the consumed theory programme")
        matching_packets = [
            packet
            for packet in reflections
            if packet["theoretical_programme"]["programme_id"]
            == triage.get("theory_programme_id")
            and packet["packet_digest"]
            == triage.get("source_reflection_packet_digest")
        ]
        if len(matching_packets) != 1:
            raise ContractError("experiment programme identity is missing or ambiguous")
        packet = matching_packets[0]
        if (
            triage.get("source_theory_programme_digest")
            != canonical_digest(packet["theoretical_programme"])
            or triage.get("source_reflection_packet_digest") != packet["packet_digest"]
        ):
            raise ContractError(
                "experiment commission does not bind the exact reflection/programme bytes"
            )
        experiment_receipt = payloads["experiment_receipt"][0]
        experiment_spec = payloads["experiment_spec"][0]
        sealed_envelope_spec = envelope.get("experiment_spec")
        if not isinstance(sealed_envelope_spec, Mapping) or not _same_payload(
            sealed_envelope_spec, experiment_spec
        ):
            raise ContractError(
                "experiment operator did not consume the exact presealed specification"
            )
        validate_commissioned_experiment_spec(
            triage,
            envelope.get("experiment_request", {}),
            experiment_spec,
        )
        if any(
            experiment_receipt.get(field) != triage.get(field)
            for field in (
                "theory_programme_id",
                "source_theory_programme_digest",
                "source_reflection_packet_digest",
                "conceptual_system_ids",
                "theoretical_question_id",
            )
        ):
            raise ContractError(
                "experiment receipt does not preserve the exact sealed commission identity"
            )
        support = packet.get("support_probe", {})
        claim = experiment_spec.get("tested_theory_claim", {})
        if (
            claim.get("claim_id") != support.get("theoretical_question_id")
            or claim.get("statement") != support.get("theoretical_question")
            or claim.get("theory_programme_id") != support.get("theory_programme_id")
            or claim.get("conceptual_system_ids")
            != sorted(support.get("conceptual_system_ids", []))
            or claim.get("source_theory_programme_digest")
            != canonical_digest(packet["theoretical_programme"])
            or claim.get("source_reflection_packet_digest") != packet["packet_digest"]
            or claim not in triage.get("registered_theory_claims", [])
        ):
            raise ContractError(
                "experiment tested claim is not the exact consumed reflective support question"
            )
        post_result_envelopes = [
            value
            for value in synthesis_envelopes
            if value.get("experiment_result") is not None
        ]
        if len(post_result_envelopes) != 1 or not _same_payload(
            post_result_envelopes[0].get("experiment_result"), experiment_receipt
        ):
            raise ContractError(
                "experiment result was not consumed exactly once by a post-result reflective synthesizer"
            )
        final_support = reflections[-1].get("support_probe", {})
        if (
            final_support.get("disposition") != "assimilated"
            or experiment_receipt["receipt_id"]
            not in set(final_support.get("receipt_ids", []))
        ):
            raise ContractError(
                "post-result reflective packet does not bind the exact experiment receipt"
            )


def _integrate_parallel_theory(
    packet: Mapping[str, Any],
    portfolio: Mapping[str, Any],
    parallel: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any] | None]:
    """Make validated branch learning and dissent materially change synthesis.

    Parallel metadata alone is not conceptual integration.  Each valid branch
    becomes a typed system revision whose mechanism and changed question are
    carried into a new synthesis.  Dissent is retained as a live contradiction,
    not averaged away.  The returned packet is an internal evaluator projection;
    the immutable upstream packet remains untouched.
    """

    projection = copy.deepcopy(dict(packet))
    systems = {row["system_id"]: copy.deepcopy(row) for row in packet.get("conceptual_systems", [])}
    preferred_id = packet.get("provisional_synthesis", {}).get("preferred_system_id")
    preferred = systems.get(preferred_id)
    if preferred is None:
        return projection, [], None
    hypotheses = {row["hypothesis_id"]: row for row in portfolio.get("hypotheses", [])}
    system_for_hypothesis: dict[str, dict[str, Any]] = {}
    for system in systems.values():
        for ancestor in system.get("conceptual_ancestors", []):
            if ancestor in hypotheses:
                system_for_hypothesis[str(ancestor)] = system
    request_by_branch = {row["branch_id"]: row for row in parallel.get("branch_requests", [])}
    valid = [
        row
        for row in parallel.get("branch_results", [])
        if row.get("literature_status") in {"current", "rebased"}
    ]
    branch_systems: list[dict[str, Any]] = []
    for result in valid:
        request = request_by_branch[result["branch_id"]]
        hypothesis = hypotheses[request["hypothesis_id"]]
        base = copy.deepcopy(system_for_hypothesis.get(request["hypothesis_id"], preferred))
        delta = result.get("theory_delta", {})
        mechanism_key = str(delta.get("mechanism_key") or hypothesis.get("mechanism_key") or result["branch_id"])
        changed_question = str(delta.get("changed_question") or hypothesis.get("maturation_question"))
        system_id = stable_identifier("system", "branch-delta", result["branch_id"], result["output_digest"])
        base.update(
            {
                "system_id": system_id,
                "relation": "rival",
                "lifecycle_state": "reflectively_revised",
                "conceptual_ancestors": [base["system_id"], request["hypothesis_id"]],
                "mechanism_or_principle": f"{base['mechanism_or_principle']} Branch maturation adds {mechanism_key}.",
                "transformation_operations": [
                    *base.get("transformation_operations", []),
                    f"validated branch delta:{delta.get('delta_class', 'conceptual_deepening')}",
                ],
                "primitives": sorted(set([*base.get("primitives", []), mechanism_key])),
                "relations_operations_and_dynamics": [
                    *base.get("relations_operations_and_dynamics", []),
                    mechanism_key,
                ],
                "formerly_inexpressible_now_visible": [
                    *base.get("formerly_inexpressible_now_visible", []),
                    changed_question,
                ],
                "implications_and_new_questions": sorted(
                    set([*base.get("implications_and_new_questions", []), changed_question])
                ),
                "residual_contradictions": [
                    *base.get("residual_contradictions", []),
                    *(
                        [f"Dissent from {result['branch_id']}: {row['proposition']}" for row in result.get("claims", [])]
                        if result.get("is_dissent")
                        else []
                    ),
                ],
            }
        )
        identity = copy.deepcopy(base["structural_identity"])
        identity["primitive_ids"] = sorted(
            set([*identity.get("primitive_ids", []), stable_identifier("primitive", system_id, mechanism_key)])
        )
        identity["relation_ids"] = sorted(
            set([*identity.get("relation_ids", []), stable_identifier("relation", system_id, "branch-delta")])
        )
        identity["mechanism_id"] = stable_identifier("mechanism", system_id, mechanism_key, changed_question)
        identity["maturation_question_id"] = stable_identifier("question", system_id, changed_question)
        identity["genealogy_ids"] = sorted(set([*identity.get("genealogy_ids", []), result["branch_id"]]))
        base["structural_identity"] = identity
        branch_systems.append(base)
    if not branch_systems:
        return projection, [], None

    dissent_ids = set(parallel.get("merge_proposal", {}).get("retained_dissent_ids", []))
    contradiction_edges = copy.deepcopy(parallel.get("merge_proposal", {}).get("contradiction_edges", []))
    integration_key = [
        {
            "branch_id": row["branch_id"],
            "semantic_digest": canonical_digest(
                {
                    "theory_delta": row.get("theory_delta"),
                    "claims": row.get("claims", []),
                    "genealogy": row.get("genealogy", []),
                    "mechanism_key": row.get("mechanism_key"),
                    "corner_family": row.get("corner_family"),
                    "is_dissent": row.get("is_dissent", False),
                    "synthesis_parent_ids": row.get("synthesis_parent_ids", []),
                }
            ),
        }
        for row in sorted(valid, key=lambda item: item["branch_id"])
    ]
    integrated = copy.deepcopy(preferred)
    integrated_id = stable_identifier("system", "parallel-synthesis", preferred_id, integration_key)
    branch_mechanisms = [row["mechanism_or_principle"] for row in branch_systems]
    integrated.update(
        {
            "system_id": integrated_id,
            "relation": "synthesis",
            "lifecycle_state": "synthesized",
            "conceptual_ancestors": [preferred_id, *[row["system_id"] for row in branch_systems]],
            "transformation_operations": [
                *integrated.get("transformation_operations", []),
                "conflict-preserving integration of validated parallel theory deltas",
            ],
            "primitives": sorted(set([*integrated.get("primitives", []), *[primitive for row in branch_systems for primitive in row.get("primitives", [])]])),
            "relations_operations_and_dynamics": [
                *integrated.get("relations_operations_and_dynamics", []),
                *branch_mechanisms,
            ],
            "mechanism_or_principle": (
                f"{integrated['mechanism_or_principle']} Validated branch mechanisms are retained as typed, regime-indexed constraints."
            ),
            "formerly_inexpressible_now_visible": [
                *integrated.get("formerly_inexpressible_now_visible", []),
                *[question for row in branch_systems for question in row.get("formerly_inexpressible_now_visible", [])[-1:]],
            ],
            "implications_and_new_questions": sorted(
                set([*integrated.get("implications_and_new_questions", []), *[question for row in branch_systems for question in row.get("implications_and_new_questions", [])]])
            ),
            "residual_contradictions": [
                *integrated.get("residual_contradictions", []),
                *[f"Retained dissenting branch: {branch_id}" for branch_id in sorted(dissent_ids)],
                *[f"Parallel contradiction remains typed: {canonical_digest(edge)}" for edge in contradiction_edges],
            ],
            "correction_conditions": [
                *integrated.get("correction_conditions", []),
                "Reject the integrated synthesis if a branch delta can be removed without changing any stated mechanism, distinction, or question.",
            ],
        }
    )
    identity = copy.deepcopy(integrated["structural_identity"])
    identity["primitive_ids"] = sorted(
        set([*identity.get("primitive_ids", []), *[item for row in branch_systems for item in row["structural_identity"].get("primitive_ids", [])]])
    )
    identity["relation_ids"] = sorted(
        set([*identity.get("relation_ids", []), *[item for row in branch_systems for item in row["structural_identity"].get("relation_ids", [])]])
    )
    identity["mechanism_id"] = stable_identifier("mechanism", integrated_id, integration_key)
    identity["maturation_question_id"] = stable_identifier("question", integrated_id, integrated["implications_and_new_questions"])
    identity["genealogy_ids"] = [preferred_id, *[row["system_id"] for row in branch_systems]]
    integrated["structural_identity"] = identity
    unification = copy.deepcopy(integrated.get("unification_claims", {}))
    unification["unified_cases_or_routes"] = sorted(
        set([*unification.get("unified_cases_or_routes", []), *[row["system_id"] for row in branch_systems]])
    )
    unification["differences_preserved"] = [
        *unification.get("differences_preserved", []),
        *[f"Branch-specific mechanism remains explicit: {row['mechanism_or_principle']}" for row in branch_systems],
        *[f"Dissent is retained rather than averaged: {branch_id}" for branch_id in sorted(dissent_ids)],
    ]
    integrated["unification_claims"] = unification
    projection["conceptual_systems"] = [*projection.get("conceptual_systems", []), *branch_systems, integrated]
    projection["provisional_synthesis"]["preferred_system_id"] = integrated_id
    projection["provisional_synthesis"]["retained_challenger_ids"] = sorted(
        set([*projection["provisional_synthesis"].get("retained_challenger_ids", []), *[row["system_id"] for row in branch_systems]])
    )
    projection["provisional_synthesis"]["unresolved_dissent"] = list(integrated["residual_contradictions"])
    projection["understanding_delta"]["after"] = integrated["formerly_inexpressible_now_visible"][-1]
    projection["theoretical_programme"]["next_theory_actions"] = list(integrated["implications_and_new_questions"])
    return projection, branch_systems, integrated


def _hypothesis_concept_ids(hypothesis: Mapping[str, Any]) -> list[str]:
    """Derive stable concept identities from typed ontology deltas, not prose labels."""

    ontology = hypothesis.get("ontology_delta", {})
    primitives = list(ontology.get("new_primitives", [])) if isinstance(ontology, Mapping) else []
    if not primitives:
        primitives = [hypothesis.get("mechanism_key") or hypothesis["hypothesis_id"]]
    return [stable_identifier("concept", hypothesis["hypothesis_id"], primitive) for primitive in primitives]


def _source_receipt_ids(producers_by_role: Mapping[str, list[dict[str, Any]]], *roles: str) -> list[str]:
    """Collect unique producer receipts for ledger provenance."""

    return sorted(
        {
            receipt["receipt_id"]
            for role in roles
            for receipt in producers_by_role.get(role, [])
        }
    )


def _event_builder(
    prior_state: Mapping[str, Any],
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    occurred_at: str,
):
    """Return a closure that extends the exact prior sequence/hash boundary."""

    events: list[dict[str, Any]] = []

    def append(
        *,
        branch_id: str,
        event_type: str,
        entity_type: str,
        entity_id: str,
        payload: Mapping[str, Any],
        source_receipt_ids: Sequence[str] = (),
        relations: Sequence[Mapping[str, Any]] = (),
        actor: str = "canonical-discovery-cycle",
    ) -> dict[str, Any]:
        previous = events[-1]["event_hash"] if events else prior_state.get("last_event_hash", GENESIS_HASH)
        event = build_event(
            sequence=int(prior_state.get("event_count", 0)) + len(events) + 1,
            previous_event_hash=previous,
            namespace=Namespace(target_id, run_id, branch_id, state_version),
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload,
            actor=actor,
            relations=relations,
            source_receipt_ids=source_receipt_ids,
            occurred_at=occurred_at,
        )
        events.append(event)
        return event

    return events, append


def _date_time(value: Any, fallback: str) -> str:
    """Normalize a date cutoff into the event schema's date-time vocabulary."""

    text = str(value or "")
    if len(text) == 10:
        text += "T23:59:59Z"
    try:
        dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
        return text
    except ValueError:
        return fallback


def _parse_timestamp(value: str, label: str) -> dt.datetime:
    """Parse one timezone-aware authority timestamp."""

    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError(f"{label} is not an ISO date-time") from exc
    if parsed.tzinfo is None:
        raise ContractError(f"{label} must be timezone-aware")
    return parsed.astimezone(dt.timezone.utc)


def _freshness_policy(
    snapshot: Mapping[str, Any],
    assimilation: Mapping[str, Any],
    present_freshness: Mapping[str, Any],
) -> dict[str, Any]:
    """Project the one assimilation-authorized window and its present-use clock.

    The canonical reducer does not invent a second recency policy.  It copies
    the validated immutable window from the assimilation packet and records the
    independently evaluated present-use instant that actually gated this
    transaction.
    """

    resolution = assimilation.get("resolution", {})
    required = {
        "freshness_policy",
        "max_age_seconds",
        "consume_before",
        "authority_scope",
    }
    if not required.issubset(resolution):
        raise ContractError("canonical literature use requires bounded temporal authority")
    return {
        "policy": resolution["freshness_policy"],
        "search_completed_at": str(snapshot["search_completed_at"]),
        "coverage_cutoff": _date_time(
            snapshot.get("coverage_cutoff"), str(snapshot["search_completed_at"])
        ),
        "max_age_seconds": resolution["max_age_seconds"],
        "consume_before": resolution["consume_before"],
        "present_use_evaluated_at": present_freshness["evaluated_at"],
        "present_use_reason": present_freshness["reason"],
        "authority_scope": resolution["authority_scope"],
    }


def _seal_operator_evidence(
    *,
    workspace: Path,
    cycle_id: str,
    cycle_directory: str,
    target_id: str,
    run_id: str,
    state_version: int,
    operator_requests: Sequence[Mapping[str, Any]],
    operator_receipts: Sequence[Mapping[str, Any]],
    role_paths: Mapping[str, Sequence[str]],
    namespace: Namespace,
    role_source_bytes: Mapping[str, bytes],
) -> tuple[
    dict[str, Any],
    list[CommitArtifact],
    dict[str, str],
    dict[str, list[dict[str, Any]]],
]:
    """Seal the complete execution wave and byte-exact role evidence.

    Requests and every terminal attempt receipt (including failed optional
    attempts and their validator receipts) live in one immutable index.  Every
    file named by any receipt is copied byte-for-byte into the same transaction.
    Successful outputs have exactly one semantic role; failed-attempt outputs
    remain auditable but never become decision inputs.
    """

    roles_by_original_path = {
        path: role
        for role, paths in role_paths.items()
        for path in paths
    }
    sealed_artifacts: list[CommitArtifact] = []
    artifact_roles: dict[str, str] = {}
    output_bindings: list[dict[str, Any]] = []
    input_bindings: list[dict[str, Any]] = []
    validator_authority_bindings: list[dict[str, Any]] = []
    input_payloads: dict[str, list[dict[str, Any]]] = {}
    receipt_by_id = {
        str(receipt["receipt_id"]): dict(receipt) for receipt in operator_receipts
    }

    for request in sorted(operator_requests, key=lambda row: row["request_id"]):
        request_id = str(request["request_id"])
        input_payloads[request_id] = []
        seen_input_paths: set[str] = set()
        for index, descriptor in enumerate(request.get("input_artifacts", [])):
            original_path = str(descriptor["path"])
            if original_path in seen_input_paths:
                raise ContractError(f"request {request_id} repeats input path {original_path}")
            seen_input_paths.add(original_path)
            source = resolve_workspace_path(workspace, original_path, must_exist=True)
            data = source.read_bytes()
            if bytes_digest(data) != descriptor["sha256"] or len(data) != descriptor["size_bytes"]:
                raise ContractError(f"operator input changed before canonical sealing: {original_path}")
            suffix = ".json" if source.suffix.lower() == ".json" else ".bin"
            sealed_name = stable_identifier(
                "sealed-input", request_id, index, original_path, descriptor["sha256"]
            ) + suffix
            sealed_path = f"{cycle_directory}/operator-evidence/inputs/{sealed_name}"
            commit_role = f"sealed_input.{request_id}.{index}"
            sealed_artifacts.append(CommitArtifact(sealed_path, data, namespace))
            artifact_roles[commit_role] = sealed_path
            input_bindings.append(
                {
                    "request_id": request_id,
                    "operator_id": request["operator"]["operator_id"],
                    "input_index": index,
                    "original_descriptor": copy.deepcopy(descriptor),
                    "sealed_path": sealed_path,
                    "sealed_sha256": bytes_digest(data),
                    "sealed_size_bytes": len(data),
                    "commit_artifact_role": commit_role,
                }
            )
            try:
                payload = json.loads(data)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ContractError(f"sealed operator input is not JSON: {original_path}: {exc}") from exc
            if not isinstance(payload, dict):
                raise ContractError(f"sealed operator input must be an object: {original_path}")
            input_payloads[request_id].append(payload)

    for receipt in sorted(operator_receipts, key=lambda row: (row["receipt_id"], row["attempt"])):
        receipt_namespace = Namespace.from_mapping(receipt["identity"])
        if (
            receipt_namespace.target_id != namespace.target_id
            or receipt_namespace.run_id != namespace.run_id
            or receipt_namespace.state_version != namespace.state_version
        ):
            raise ContractError("sealed operator output crossed target/run/state identity")
        for index, (descriptor, history_descriptor) in enumerate(
            zip(
                receipt["output_artifacts"],
                receipt["output_history_artifacts"],
                strict=True,
            )
        ):
            original_path = str(descriptor["path"])
            source = resolve_workspace_path(
                workspace, history_descriptor["path"], must_exist=True
            )
            data = (
                role_source_bytes[original_path]
                if receipt["status"] == "succeeded" and original_path in role_source_bytes
                else source.read_bytes()
            )
            if (
                bytes_digest(data) != descriptor["sha256"]
                or len(data) != descriptor["size_bytes"]
                or descriptor["sha256"] != history_descriptor["sha256"]
                or descriptor["size_bytes"] != history_descriptor["size_bytes"]
            ):
                raise ContractError(
                    f"operator output history changed before canonical sealing: {original_path}"
                )
            suffix = ".json" if source.suffix.lower() == ".json" else ".bin"
            sealed_name = stable_identifier(
                "sealed-output", receipt["receipt_id"], index, original_path, descriptor["sha256"]
            ) + suffix
            sealed_path = f"{cycle_directory}/operator-evidence/outputs/{sealed_name}"
            sealed_artifacts.append(CommitArtifact(sealed_path, data, namespace))
            semantic_role = (
                roles_by_original_path.get(original_path)
                if receipt["status"] == "succeeded"
                else None
            )
            projection_role = (
                f"sealed_role.{semantic_role}.{list(role_paths[semantic_role]).index(original_path)}"
                if semantic_role
                else f"sealed_attempt_output.{receipt['receipt_id']}.{index}"
            )
            if projection_role in artifact_roles:
                raise ContractError(f"duplicate sealed artifact role: {projection_role}")
            artifact_roles[projection_role] = sealed_path
            output_bindings.append(
                {
                    "receipt_id": receipt["receipt_id"],
                    "request_id": receipt["request_id"],
                    "operator_id": receipt["operator"]["operator_id"],
                    "attempt": receipt["attempt"],
                    "status": receipt["status"],
                    "original_descriptor": copy.deepcopy(descriptor),
                    "history_descriptor": copy.deepcopy(history_descriptor),
                    "sealed_path": sealed_path,
                    "sealed_sha256": bytes_digest(data),
                    "sealed_size_bytes": len(data),
                    "semantic_role": semantic_role,
                    "commit_artifact_role": projection_role,
                }
            )
        for validator in receipt["validator_receipts"]:
            authority = validator["validator_authority"]
            for file_index, authority_file in enumerate(authority["files"]):
                descriptor = authority_file["snapshot_descriptor"]
                source = resolve_workspace_path(workspace, descriptor["path"], must_exist=True)
                data = source.read_bytes()
                if (
                    bytes_digest(data) != descriptor["sha256"]
                    or len(data) != descriptor["size_bytes"]
                    or descriptor["sha256"] != authority_file["sha256"]
                    or descriptor["size_bytes"] != authority_file["size_bytes"]
                ):
                    raise ContractError("validator authority snapshot changed before sealing")
                sealed_name = stable_identifier(
                    "sealed-validator",
                    receipt["receipt_id"],
                    validator["receipt_digest"],
                    file_index,
                    descriptor["sha256"],
                ) + (Path(str(authority_file["runtime_path"])).suffix or ".bin")
                sealed_path = f"{cycle_directory}/operator-evidence/validators/{sealed_name}"
                commit_role = (
                    f"sealed_validator.{receipt['receipt_id']}."
                    f"{validator['validator_id']}.{file_index}"
                )
                sealed_artifacts.append(CommitArtifact(sealed_path, data, namespace))
                artifact_roles[commit_role] = sealed_path
                validator_authority_bindings.append(
                    {
                        "receipt_id": receipt["receipt_id"],
                        "validator_receipt_digest": validator["receipt_digest"],
                        "validator_id": validator["validator_id"],
                        "authority_digest": authority["authority_digest"],
                        "file_index": file_index,
                        "authority_file": copy.deepcopy(authority_file),
                        "sealed_path": sealed_path,
                        "sealed_sha256": bytes_digest(data),
                        "sealed_size_bytes": len(data),
                        "commit_artifact_role": commit_role,
                    }
                )

    role_bindings: list[dict[str, Any]] = []
    for role, paths in sorted(role_paths.items()):
        for index, original_path in enumerate(paths):
            producer = next(
                (
                    binding
                    for binding in output_bindings
                    if binding["original_descriptor"]["path"] == original_path
                    and binding["status"] == "succeeded"
                    and binding["semantic_role"] == role
                ),
                None,
            )
            if producer is None:
                data = role_source_bytes[original_path]
                source = resolve_workspace_path(workspace, original_path, must_exist=True)
                sealed_name = stable_identifier(
                    "sealed-role-source", role, index, original_path, bytes_digest(data)
                ) + (".json" if source.suffix.lower() == ".json" else ".bin")
                sealed_path = f"{cycle_directory}/operator-evidence/role-sources/{sealed_name}"
                sealed_artifacts.append(CommitArtifact(sealed_path, data, namespace))
                projection_role = f"sealed_role.{role}.{index}"
                artifact_roles[projection_role] = sealed_path
            else:
                sealed_path = str(producer["sealed_path"])
                data = role_source_bytes[original_path]
                projection_role = str(producer["commit_artifact_role"])
            role_bindings.append(
                {
                    "role": role,
                    "role_index": index,
                    "original_path": original_path,
                    "sealed_path": sealed_path,
                    "sha256": bytes_digest(data),
                    "size_bytes": len(data),
                    "source_kind": "operator_output" if producer else "external_role_artifact",
                    "producer_receipt_id": producer["receipt_id"] if producer else None,
                    "producer_request_id": producer["request_id"] if producer else None,
                    "producer_operator_id": producer["operator_id"] if producer else None,
                    "commit_artifact_role": projection_role,
                }
            )

    evidence = {
        "schema_version": "1.0.0",
        "cycle_id": cycle_id,
        "target_id": target_id,
        "run_id": run_id,
        "prior_state_version": state_version,
        "operator_requests": sorted(
            [copy.deepcopy(dict(row)) for row in operator_requests],
            key=lambda row: row["request_id"],
        ),
        "operator_receipts": sorted(
            [copy.deepcopy(dict(row)) for row in operator_receipts],
            key=lambda row: (row["receipt_id"], row["attempt"]),
        ),
        "successful_receipt_ids": sorted(
            receipt_id
            for receipt_id, receipt in receipt_by_id.items()
            if receipt["status"] == "succeeded"
        ),
        "input_bindings": input_bindings,
        "role_bindings": role_bindings,
        "output_bindings": output_bindings,
        "validator_authority_bindings": validator_authority_bindings,
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    evidence["evidence_digest"] = canonical_digest(evidence)
    evidence_path = f"{cycle_directory}/operator-evidence.json"
    sealed_artifacts.append(CommitArtifact(evidence_path, _json_bytes(evidence), namespace))
    artifact_roles["operator_evidence"] = evidence_path
    return evidence, sealed_artifacts, artifact_roles, input_payloads


def _system_hypotheses(
    system_id: str,
    systems: Mapping[str, Mapping[str, Any]],
    hypothesis_ids: set[str],
    *,
    seen: set[str] | None = None,
) -> list[str]:
    """Trace a synthesis back to stable hypothesis IDs without rewriting genealogy."""

    visited = set() if seen is None else set(seen)
    if system_id in visited:
        return []
    visited.add(system_id)
    system = systems.get(system_id, {})
    output: list[str] = []
    for ancestor in system.get("conceptual_ancestors", []):
        if ancestor in hypothesis_ids:
            output.append(str(ancestor))
        elif ancestor in systems:
            output.extend(_system_hypotheses(str(ancestor), systems, hypothesis_ids, seen=visited))
    return sorted(set(output))


def _evaluation_candidate(
    packet: Mapping[str, Any],
    portfolio: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    *,
    proposal_receipt: Mapping[str, Any],
    literature_mode: str,
    concept_ids_by_hypothesis: Mapping[str, list[str]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Compile a reflective synthesis into the independent evaluator vocabulary."""

    systems = {row["system_id"]: row for row in packet.get("conceptual_systems", [])}
    preferred_id = packet.get("provisional_synthesis", {}).get("preferred_system_id")
    preferred = systems.get(preferred_id)
    if preferred is None:
        raise ContractError("reflective packet lacks a resolvable preferred system")
    hypotheses = {row["hypothesis_id"]: row for row in portfolio.get("hypotheses", [])}
    ancestry = _system_hypotheses(str(preferred_id), systems, set(hypotheses))
    ancestor = hypotheses.get(ancestry[0], {}) if ancestry else {}
    concept_ids = sorted({value for hypothesis_id in ancestry for value in concept_ids_by_hypothesis.get(hypothesis_id, [])})
    primitives = list(preferred.get("primitives", []))
    relation_texts = list(preferred.get("relations_operations_and_dynamics", []))
    pressures = list(preferred.get("target_pressures_addressed", []))
    relations = [
        {
            "source": primitives[index % len(primitives)] if primitives else str(preferred_id),
            "kind": "mediates",
            "target": pressures[index % len(pressures)] if pressures else "target-pressure",
        }
        for index, _ in enumerate(relation_texts or ["mediates"])
    ]
    stages = [
        {
            "input": relation["source"],
            "operation": relation_texts[index] if index < len(relation_texts) else "mediate",
            "output": relation["target"],
        }
        for index, relation in enumerate(relations)
    ]
    unified = list(preferred.get("unification_claims", {}).get("unified_cases_or_routes", []))
    mappings = []
    for left, right in zip(unified, unified[1:]):
        mappings.append(
            {
                "source_system": str(left),
                "bridge": str(preferred.get("mechanism_or_principle", "mediation")),
                "target_system": str(right),
            }
        )
    source_assessments = []
    for source_id in ancestor.get("literature_source_ids", [])[:3]:
        relation = ancestor.get("literature_relation", "partially_overlaps")
        allowed = {"anticipates", "contradicts", "sharpens", "independent", "partially_overlaps"}
        source_assessments.append(
            {
                "source_id": source_id,
                "relation": relation if relation in allowed else "partially_overlaps",
                "reason": "The source relation was inherited from the claim-level literature rebase.",
            }
        )
    if not source_assessments and snapshot.get("sources"):
        source_assessments = [
            {
                "source_id": snapshot["sources"][0]["source_id"],
                "relation": "partially_overlaps",
                "reason": "The synthesis consumes this mapped source without inferring novelty from absence.",
            }
        ]
    risk = ancestor.get("risk_axes", {})
    quality = ancestor.get("quality_axes", {})
    candidate = {
        "target_id": packet["target_id"],
        "proposal_receipt_ids": [proposal_receipt["receipt_id"]],
        "proposal_invocation_id": proposal_receipt["invocation_id"],
        "proposer_identity": proposal_receipt["operator"]["operator_id"],
        "concept_ids": concept_ids,
        "hypothesis_ids": ancestry,
        "conceptual_system_id": preferred_id,
        "relevance": {
            "essential": bool(pressures),
            "target_dependencies": pressures,
            "root_tensions": [
                str(row.get("minimal_incompatibility_or_missing_mediation") or row.get("tension_id"))
                for row in packet.get("root_tensions", [])
            ]
            or [packet["discovery_charter"]["essential_question"]],
        },
        "concepts": [
            {
                "concept_id": concept_ids[0] if concept_ids else stable_identifier("concept", preferred_id),
                "primitives": primitives,
                "relations": relations,
                "distinctions": list(preferred.get("identities_and_differences", [])),
            }
        ],
        "ontology": {"primitives": primitives, "relations": relations},
        "mechanism": {
            "stages": stages,
            "causal_edges": [
                {"source": row["source"], "relation": row["kind"], "target": row["target"]}
                for row in relations
            ],
            "counterfactuals": list(preferred.get("correction_conditions", [])),
        },
        "understanding_delta": {
            **copy.deepcopy(packet.get("understanding_delta", {})),
            "new_explanatory_dependencies": [
                {"source": row["source"], "relation": row["kind"], "target": row["target"]}
                for row in relations
            ],
            "new_questions": list(preferred.get("implications_and_new_questions", [])),
        },
        "unification_map": {
            "mappings": mappings,
            "preserved_differences": list(preferred.get("unification_claims", {}).get("differences_preserved", [])),
        },
        "synthesis": {
            "parent_system_ids": list(preferred.get("conceptual_ancestors", [])),
            "transformations": [
                str(round_row.get("mutation_or_synthesis", {}).get("operation", ""))
                for round_row in packet.get("reflection_rounds", [])
                if str(round_row.get("mutation_or_synthesis", {}).get("operation", "")).strip()
            ],
        },
        "reflection_rounds": copy.deepcopy(packet.get("reflection_rounds", [])),
        "new_questions": list(preferred.get("implications_and_new_questions", [])),
        "obligations": [
            {"kind": "formalize", "depends_on": str(preferred_id), "tests": str(item)}
            for item in packet.get("theoretical_programme", {}).get("proof_or_model_obligations", [])
        ],
        "predictions": [],
        "consistency": {
            "assumptions": list(preferred.get("ontological_commitments", [])),
            "unresolved_contradictions": list(preferred.get("residual_contradictions", [])),
        },
        "correction_conditions": list(preferred.get("correction_conditions", [])),
        "falsifiers": [
            {"kind": "declared correction condition", "claim": str(item)}
            for item in preferred.get("correction_conditions", [])
        ],
        "scope_conditions": list(packet.get("discovery_charter", {}).get("target_commitments", [])),
        "risk_reward": {
            "truth_confidence": float(risk.get("probability_of_truth", 0.25)),
            "value_if_right": float(quality.get("value_if_true", 0.75)),
            "learning_value_if_false": float(quality.get("learning_if_false", 0.6)),
            "mechanism_path": str(preferred.get("mechanism_or_principle", "")),
        },
        "literature_snapshot": {
            "snapshot_id": snapshot["snapshot_id"],
            "target_id": snapshot["target_id"],
            "status": "validated_current" if literature_mode == "active_current" else "local_only",
            "content_digest": snapshot["content_digest"],
        },
        "source_relation_assessments": source_assessments,
        "established_claim_gates": [],
        "promotion_requested": False,
        "proof_status": "open",
        "evidence_status": "open",
    }
    identity = {
        "conceptual_system_id": preferred_id,
        "hypothesis_ids": ancestry,
        "concept_ids": concept_ids,
    }
    return candidate, identity


def _formal_claim_schedule_binding(
    *,
    formal_claim_output: Mapping[str, Any] | None,
    formal_claim_request: Mapping[str, Any] | None,
    formal_claim_receipt: Mapping[str, Any] | None,
    formal_claim_input: Mapping[str, Any] | None,
    formal_claim_event: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    """Derive the sole schedule binding from exact sealed producer evidence."""

    components = (
        formal_claim_request,
        formal_claim_receipt,
        formal_claim_input,
        formal_claim_event,
    )
    if formal_claim_output is None:
        if any(component is not None for component in components):
            raise ContractError(
                "formal-claim scheduler evidence exists without a producer output"
            )
        return None
    if any(not isinstance(component, Mapping) for component in components):
        raise ContractError(
            "formal-claim scheduler binding requires exact request, receipt, input, and event evidence"
        )
    request = dict(formal_claim_request or {})
    receipt = dict(formal_claim_receipt or {})
    producer_input = dict(formal_claim_input or {})
    event = dict(formal_claim_event or {})
    output = validate_formal_claim_producer_output(formal_claim_output)
    semantic_rows = semantic_output_rows("formal-claim-producer", output)
    if len(semantic_rows) != 1:
        raise ContractError(
            "formal-claim scheduler binding lacks one semantic producer row"
        )
    semantic_row = semantic_rows[0]
    event_payload = event.get("payload", {})
    semantic_projection = (
        event_payload.get("semantic_projection", {})
        if isinstance(event_payload, Mapping)
        else {}
    )
    if (
        request.get("operator", {}).get("operator_id")
        != "formal-claim-producer"
        or receipt.get("operator", {}).get("operator_id")
        != "formal-claim-producer"
        or receipt.get("status") != "succeeded"
        or receipt.get("request_id") != request.get("request_id")
        or receipt.get("request_digest") != request.get("request_digest")
        or receipt.get("input_digest") != request.get("input_digest")
        or receipt.get("identity") != request.get("identity")
        or request.get("identity", {}).get("target_id") != output["target_id"]
        or request.get("identity", {}).get("run_id") != output["run_id"]
        or request.get("identity", {}).get("branch_id") != output["branch_id"]
        or request.get("identity", {}).get("state_version")
        != output["source_prior_state_version"]
        or producer_input.get("conjecture_id") != output["conjecture_id"]
        or producer_input.get("branch_id") != output["branch_id"]
        or producer_input.get("hypothesis_id") != output["hypothesis_id"]
        or event.get("event_type") != "reflection_recorded"
        or event.get("entity_type") != "reflection"
        or event.get("entity_id") != semantic_row["semantic_id"]
        or event.get("source_receipt_ids") != [receipt.get("receipt_id")]
        or event_payload.get("kind") != "formal_claim_production"
        or event_payload.get("output_id") != output["output_id"]
        or event_payload.get("output_digest") != output["content_digest"]
        or event_payload.get("status") != output["status"]
        or event_payload.get("formal_claim_output") != output
        or semantic_projection.get("semantic_kind")
        != semantic_row["semantic_kind"]
        or semantic_projection.get("semantic_id") != semantic_row["semantic_id"]
        or semantic_projection.get("row_digest") != semantic_row["row_digest"]
    ):
        raise ContractError(
            "formal-claim scheduler evidence does not form one exact producer-to-event join"
        )
    if output["status"] == "not_ready":
        return None
    return {
        "schema_version": 1,
        "binding_kind": "registered_formal_claim_prove_action",
        "producer_operator_id": "formal-claim-producer",
        "producer_request_id": request["request_id"],
        "producer_request_digest": request["request_digest"],
        "producer_receipt_id": receipt["receipt_id"],
        "producer_receipt_digest": receipt["receipt_digest"],
        "producer_input_digest": canonical_digest(producer_input),
        "consumer_event_id": event["event_id"],
        "consumer_event_hash": event["event_hash"],
        "semantic_row_id": semantic_row["semantic_id"],
        "semantic_row_digest": semantic_row["row_digest"],
        "output_id": output["output_id"],
        "output_digest": output["content_digest"],
        "source_theory_generation": output["source_theory_generation"],
        "conjecture_id": output["conjecture_id"],
        "formal_claim_digest": output["formal_claim_digest"],
        "execution_plan_digest": output["execution_plan_digest"],
    }


def _scheduler_projection(
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    literature_mode: str,
    snapshot_id: str,
    portfolio: Mapping[str, Any],
    parallel: Mapping[str, Any],
    final_reflection: Mapping[str, Any],
    concept_ids_by_hypothesis: Mapping[str, list[str]],
    system_ids_by_hypothesis: Mapping[str, list[str]],
    proof_handoff: Mapping[str, Any] | None,
    experiment_receipt: Mapping[str, Any] | None,
    source_routing_precommit: Mapping[str, Any] | None,
    conceptual_authority: Mapping[str, Any],
    formal_claim_output: Mapping[str, Any] | None = None,
    formal_claim_request: Mapping[str, Any] | None = None,
    formal_claim_receipt: Mapping[str, Any] | None = None,
    formal_claim_input: Mapping[str, Any] | None = None,
    formal_claim_event: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Project canonical identities into the existing theory-first scheduler."""

    hypotheses = {row["hypothesis_id"]: row for row in portfolio.get("hypotheses", [])}
    results = {row["branch_id"]: row for row in parallel.get("branch_results", [])}
    support = final_reflection.get("support_probe", {})
    branches: list[dict[str, Any]] = []
    identity_bindings: list[dict[str, Any]] = []
    expected_formal_binding = _formal_claim_schedule_binding(
        formal_claim_output=formal_claim_output,
        formal_claim_request=formal_claim_request,
        formal_claim_receipt=formal_claim_receipt,
        formal_claim_input=formal_claim_input,
        formal_claim_event=formal_claim_event,
    )
    bound_formal_branch_count = 0
    for request in parallel.get("branch_requests", []):
        branch_id = request["branch_id"]
        hypothesis_id = request["hypothesis_id"]
        hypothesis = hypotheses[hypothesis_id]
        result = results.get(branch_id)
        quality = hypothesis.get("quality_axes", {})
        ready_formal_claim = bool(
            expected_formal_binding is not None
            and formal_claim_output is not None
            and formal_claim_output.get("branch_id") == branch_id
            and formal_claim_output.get("hypothesis_id") == hypothesis_id
        )
        if ready_formal_claim:
            bound_formal_branch_count += 1
        formal_claim_binding = (
            copy.deepcopy(expected_formal_binding)
            if ready_formal_claim
            else None
        )
        branch = {
            "branch_id": branch_id,
            "status": "incubating" if result else "operational_failure",
            "maturity": (
                "proof_ready"
                if ready_formal_claim
                or (proof_handoff and proof_handoff["branch_id"] == branch_id)
                else "incubating"
            ),
            "formal_claim_binding": formal_claim_binding,
            "conceptual_system_ids": copy.deepcopy(
                system_ids_by_hypothesis[hypothesis_id]
            ),
            "conceptual_corner": hypothesis["corner_family"],
            "semantic_prompt_digest": request["input_digest"],
            "depends_on": list(request.get("depends_on_branch_ids", [])),
            "dependency_ids": [hypothesis_id],
            "theory_virtues": {
                "essential_relevance": float(quality.get("essential_relevance", 0.0)),
                "root_tension_contact": float(quality.get("essential_relevance", 0.0)),
                "expected_understanding_gain": float(quality.get("explanatory_upside", 0.0)),
                "expected_unification_gain": float(quality.get("unification_potential", 0.0)),
                "conceptual_fertility": float(quality.get("generativity", 0.0)),
                "programme_impact": float(quality.get("value_if_true", 0.0)),
                "maturity": 0.6 if result else 0.0,
            },
            "estimated_cost": float(hypothesis.get("risk_axes", {}).get("maturation_cost", 1.0)),
            "premature_closure_risk": float(hypothesis.get("risk_axes", {}).get("failure_risk", 0.5)),
            "protected_wildcard": hypothesis_id in set(portfolio.get("protected_wildcard_ids", [])),
            "requested_action": (
                "probe"
                if support.get("disposition") in {"proposed", "commissioned"}
                else "reflect"
            ),
            "probe_decision": (
                "commission"
                if support.get("disposition") in {"proposed", "commissioned"}
                else str(support.get("disposition") or "no_probe_needed")
            ),
            "theoretical_question_maturity": "mature",
        }
        branches.append(branch)
        identity_bindings.append(
            {
                "branch_id": branch_id,
                "hypothesis_id": hypothesis_id,
                "concept_ids": concept_ids_by_hypothesis[hypothesis_id],
                "conceptual_system_ids": system_ids_by_hypothesis[hypothesis_id],
            }
        )
    if expected_formal_binding is not None and bound_formal_branch_count != 1:
        raise ContractError(
            "ready formal-claim output does not bind exactly one canonical branch"
        )
    scheduler_state = {
        "target_id": target_id,
        "run_id": run_id,
        "state_version": state_version,
        "conceptual_systems": copy.deepcopy(
            final_reflection.get("conceptual_systems", [])
        ),
        "reflection_rounds": copy.deepcopy(
            final_reflection.get("reflection_rounds", [])
        ),
        "theory_programme": copy.deepcopy(
            final_reflection.get("theoretical_programme", {})
        ),
        "programme_support_probe": (
            copy.deepcopy(support)
            if support.get("disposition") in {"proposed", "commissioned"}
            else None
        ),
        "conceptual_adjudication_evidence": copy.deepcopy(
            conceptual_authority.get("synthesis_evidence")
        ),
        "literature": {
            "status": "validated_current" if literature_mode == "active_current" else "local_only",
            "snapshot_id": snapshot_id,
            "assimilated_snapshot_id": snapshot_id,
        },
        "branches": branches,
        "semantic_plateau_limit": 3,
        "required_conceptual_corners": sorted(portfolio.get("corner_coverage", [])),
        # A falsifier may request reflective review, but it cannot silently
        # reprioritize or select ordinary theory work. The exact pending delta
        # is carried beside the invariant schedule by experiment-world
        # semantics and must be accepted by a later reflective cycle.
        "new_evidence": [],
    }
    schedule = schedule_discovery_actions(scheduler_state)
    schedule["run_id"] = run_id
    formal_actions = [
        action
        for action in schedule.get("actions", [])
        if action.get("kind") == "prove"
    ]
    if expected_formal_binding is not None:
        if (
            len(formal_actions) != 1
            or formal_actions[0].get("branch_ids")
            != [formal_claim_output["branch_id"]]
            or formal_actions[0].get("payload", {}).get(
                "formal_claim_binding"
            )
            != expected_formal_binding
        ):
            raise ContractError(
                "ready formal-claim output does not schedule exactly one bound prove action"
            )
    elif formal_actions:
        raise ContractError(
            "not-ready or absent formal-claim output scheduled a prove action"
        )
    if schedule.get("conceptual_preference_authority", {}).get(
        "status"
    ) != conceptual_authority.get("status"):
        raise ContractError(
            "scheduler conceptual authority differs from canonical evidence replay"
        )
    if final_reflection.get("generation_mode") == "local_structural_fallback":
        fallback_restrictions = {
            "structural_fallback",
            "no_philosophical_depth_claim",
            "no_understanding_gain_claim",
            "no_proof",
            "no_promotion",
        }
        for action in schedule["actions"]:
            if not action.get("branch_ids"):
                continue
            if action.get("kind") in {"prove", "probe"}:
                raise ContractError(
                    "local structural fallback cannot schedule proof or experiment authority"
                )
            action["restrictions"] = sorted(
                {*action.get("restrictions", []), *fallback_restrictions}
            )
    schedule["identity_bindings"] = identity_bindings
    source_policy = (
        source_routing_precommit.get("pre_map_policy")
        if source_routing_precommit is not None
        else None
    )
    source_realization = (
        source_routing_precommit.get("realization")
        if source_routing_precommit is not None
        else None
    )
    schedule["source_routing_pre_map_policy_id"] = (
        source_policy["policy_id"] if source_policy is not None else None
    )
    schedule["source_routing_pre_map_policy_digest"] = (
        source_policy["policy_digest"] if source_policy is not None else None
    )
    schedule["source_routing_realization_id"] = (
        source_realization["realization_id"]
        if source_realization is not None
        else None
    )
    schedule["source_routing_realization_digest"] = (
        source_realization["realization_digest"]
        if source_realization is not None
        else None
    )
    schedule["authority_boundary"] = AUTHORITY_BOUNDARY
    schedule["schedule_digest"] = canonical_digest(
        schedule,
        exclude_keys=("schedule_digest", "created_at", "consumption_log"),
    )
    return schedule


def _semantic_projection_value(
    value: Any,
    *,
    preserve_digest_keys: frozenset[str] = frozenset(),
) -> Any:
    """Remove transport/integrity bookkeeping while preserving complete meaning.

    Integrity digests are omitted only where the complete underlying semantic
    object is present in the same projection. Historical revision records keep
    their full semantic `record` values while dropping event-chain addresses.
    """

    if isinstance(value, Mapping):
        projected: dict[str, Any] = {}
        for raw_key, item in sorted(value.items(), key=lambda pair: str(pair[0])):
            key = str(raw_key)
            if key == "revisions":
                projected[key] = [
                    _semantic_projection_value(
                        revision.get("record", revision)
                        if isinstance(revision, Mapping)
                        else revision,
                        preserve_digest_keys=preserve_digest_keys,
                    )
                    for revision in item
                ]
                continue
            if (
                key in _SEMANTIC_TRANSPORT_KEYS
                or key in _SEMANTIC_TIME_KEYS
                or key.endswith(_SEMANTIC_TRANSPORT_SUFFIXES)
                or (key.endswith("_digest") and key not in preserve_digest_keys)
            ):
                continue
            projected[key] = _semantic_projection_value(
                item,
                preserve_digest_keys=preserve_digest_keys,
            )
        return projected
    if isinstance(value, list):
        return [
            _semantic_projection_value(
                item,
                preserve_digest_keys=preserve_digest_keys,
            )
            for item in value
        ]
    return copy.deepcopy(value)


def _state_theory_semantics(state: Mapping[str, Any]) -> dict[str, Any]:
    """Project every theory-bearing reducer table without chain transport data."""

    table_names = (
        "conceptual_systems",
        "concepts",
        "hypotheses",
        "evidence",
        "literature_snapshots",
        "branch_attempts",
        "branches",
        "transformations",
        "syntheses",
        "understanding_deltas",
        "relations",
        "retired_routes",
    )
    projection = {
        name: _semantic_projection_value(state.get(name, {}))
        for name in table_names
    }
    projection.update(
        {
            "active_theory_constellation": _semantic_projection_value(
                state.get("active_theory_constellation", [])
            ),
            "current_literature_snapshot_id": state.get(
                "current_literature_snapshot_id"
            ),
            "stale_branches": _semantic_projection_value(
                state.get("stale_branches", [])
            ),
            "rebase_history": _semantic_projection_value(
                state.get("rebase_history", [])
            ),
        }
    )
    reflection_rows = [
        _semantic_projection_value(row)
        for row in state.get("reflections", {}).values()
        if isinstance(row, Mapping)
        and row.get("kind") not in _NON_THEORY_EXPERIMENT_REFLECTION_KINDS
    ]
    projection["reflections"] = sorted(
        reflection_rows,
        key=canonical_digest,
    )
    return projection


def _reflective_theory_semantics(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Keep all reflective theory content while separating the probe interface."""

    fields = (
        "discovery_charter",
        "conceptual_genealogy",
        "root_tensions",
        "conceptual_systems",
        "reflection_rounds",
        "provisional_synthesis",
        "theoretical_programme",
        "understanding_delta",
        "truth_convergence_status",
        "stage_gates",
        "theory_quality_pareto",
        "next_reflective_action",
        "plateau",
        "explicit_unknowns",
    )
    projection = {
        field: copy.deepcopy(packet.get(field))
        for field in fields
    }
    convergence = projection.get("truth_convergence_status")
    if isinstance(convergence, dict):
        # This one field reports the optional child-probe lane; it is not a
        # constituent of theory identity and is represented separately below.
        convergence.pop("model_or_experimental_support", None)
    return _semantic_projection_value(projection)


def _schedule_theory_semantics(schedule: Mapping[str, Any]) -> dict[str, Any]:
    """Project the complete action/dependency/priority schedule semantics."""

    return _semantic_projection_value(
        schedule,
        preserve_digest_keys=frozenset({"semantic_prompt_digest"}),
    )


def _experiment_world_id(
    experiment_receipt: Mapping[str, Any] | None,
) -> str:
    if experiment_receipt is None:
        return "no_probe"
    effect_kind = experiment_receipt.get("theory_effect", {}).get("effect_kind")
    return {
        "no_theory_effect_inconclusive": "neutral_inconclusive",
        "bounded_consistency_signal_only": "misleading_toy_positive",
        "registered_premise_revision_requested": "registered_premise_falsifier",
        "no_theory_effect_operational": "operational_failure",
    }.get(str(effect_kind), "outside_declared_five_world_matrix")


def _tested_claim_binding(
    experiment_spec: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    if experiment_spec is None:
        return None
    claim = copy.deepcopy(dict(experiment_spec["tested_theory_claim"]))
    expected = canonical_digest(claim, exclude_keys=("claim_digest",))
    if claim.get("claim_digest") != expected:
        raise ContractError("experiment-world tested claim digest is invalid")
    return claim


def _pending_review_delta(
    experiment_reflection_receipt: Mapping[str, Any] | None,
    tested_claim: Mapping[str, Any] | None,
) -> dict[str, Any]:
    pending = bool(
        experiment_reflection_receipt
        and experiment_reflection_receipt.get("decision")
        == "pending_registered_premise_review"
    )
    if pending:
        if tested_claim is None:
            raise ContractError("pending premise review lacks its exact tested claim")
        delta = copy.deepcopy(experiment_reflection_receipt["typed_delta"])
        if (
            delta.get("tested_claim_id") != tested_claim["claim_id"]
            or delta.get("tested_claim_digest") != tested_claim["claim_digest"]
        ):
            raise ContractError("executed reflection delta crossed its tested premise")
    else:
        delta = {
            "status": "none",
            "kind": "none",
            "tested_claim_id": None,
            "tested_claim_digest": None,
            "theory_programme_id": None,
            "source_theory_programme_digest": None,
            "source_reflection_packet_digest": None,
            "conceptual_system_ids": [],
            "requested_followup_kind": None,
            "review_reason": None,
            "theory_identity_changed": False,
            "ontology_mutation_authorized": False,
            "selection_authorized": False,
            "proof_authorized": False,
            "automatic_evidence_relation_authorized": False,
            "schedule_mutation_authorized": False,
        }
    expected_digest = canonical_digest(delta, exclude_keys=("delta_digest",))
    if "delta_digest" in delta and delta["delta_digest"] != expected_digest:
        raise ContractError("executed reflection typed-delta digest is invalid")
    delta["delta_digest"] = expected_digest
    return delta


def _experiment_direct_mutation_audit(
    events: Sequence[Mapping[str, Any]],
    experiment_operator_receipt_ids: Sequence[str],
) -> dict[str, Any]:
    receipt_ids = sorted(set(str(value) for value in experiment_operator_receipt_ids))
    related = [
        event
        for event in events
        if set(event.get("source_receipt_ids", [])).intersection(receipt_ids)
    ]
    mutations = [
        event
        for event in related
        if event.get("event_type") != "reflection_recorded"
        or event.get("payload", {}).get("kind")
        not in _NON_THEORY_EXPERIMENT_REFLECTION_KINDS
    ]
    evidence_relations = [
        event
        for event in mutations
        if event.get("event_type") in {"evidence_recorded", "relation_recorded"}
    ]
    proof_events = [
        event
        for event in mutations
        if event.get("event_type") == "proof_obligation_recorded"
    ]
    selection_events = [
        event
        for event in mutations
        if event.get("event_type")
        in {
            "entity_upsert",
            "perspective_shift",
            "ontology_revision",
            "conceptual_transformation",
            "synthesis_recorded",
            "route_retired",
        }
    ]
    return {
        "experiment_operator_receipt_ids": receipt_ids,
        "theory_mutation_event_ids": [event["event_id"] for event in mutations],
        "automatic_evidence_relation_event_ids": [
            event["event_id"] for event in evidence_relations
        ],
        "proof_authorization_event_ids": [event["event_id"] for event in proof_events],
        "selection_event_ids": [event["event_id"] for event in selection_events],
        "theory_identity_changed": bool(mutations),
        "automatic_evidence_relation_recorded": bool(evidence_relations),
        "proof_authorized": bool(proof_events),
        "theory_selected": bool(selection_events),
    }


def _build_experiment_world_semantics(
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    prior_state: Mapping[str, Any],
    next_state: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    assimilation: Mapping[str, Any],
    portfolio: Mapping[str, Any],
    parallel: Mapping[str, Any],
    reflections: Sequence[Mapping[str, Any]],
    final_reflection: Mapping[str, Any],
    identity_map: Mapping[str, Any],
    evaluations: Sequence[Mapping[str, Any]],
    evaluation_identities: Sequence[Mapping[str, Any]],
    conceptual_authority: Mapping[str, Any],
    proof_handoff: Mapping[str, Any] | None,
    schedule: Mapping[str, Any],
    experiment_spec: Mapping[str, Any] | None,
    experiment_receipt: Mapping[str, Any] | None,
    experiment_reflection_receipt: Mapping[str, Any] | None,
    direct_mutation_audit: Mapping[str, Any],
    source_routing_precommit: Mapping[str, Any] | None,
) -> dict[str, Any]:
    tested_claim = _tested_claim_binding(experiment_spec)
    theory_projection = {
        "prior_state": _state_theory_semantics(prior_state),
        "committed_state": _state_theory_semantics(next_state),
        "literature_snapshot": _semantic_projection_value(snapshot),
        "literature_assimilation": _semantic_projection_value(assimilation),
        "source_routing_precommit": _semantic_projection_value(
            source_routing_precommit
        ),
        "high_risk_portfolio": _semantic_projection_value(portfolio),
        "parallel_portfolio": _semantic_projection_value(parallel),
        "parent_reflective_theory": _reflective_theory_semantics(reflections[0]),
        "synthesis_reflective_theory": _reflective_theory_semantics(reflections[-1]),
        "integrated_reflective_theory": _reflective_theory_semantics(final_reflection),
        "identity_map": _semantic_projection_value(identity_map),
        "evaluation_receipts": _semantic_projection_value(evaluations),
        "evaluation_identity_bindings": _semantic_projection_value(
            evaluation_identities
        ),
        "conceptual_authority": _semantic_projection_value(conceptual_authority),
        "proof_handoff": _semantic_projection_value(proof_handoff),
    }
    schedule_projection = _schedule_theory_semantics(schedule)
    ancestor_projection = {
        "prior_state": theory_projection["prior_state"],
        "literature_snapshot": theory_projection["literature_snapshot"],
        "literature_assimilation": theory_projection["literature_assimilation"],
        "source_routing_precommit": theory_projection[
            "source_routing_precommit"
        ],
        "high_risk_portfolio": theory_projection["high_risk_portfolio"],
        "parallel_portfolio": theory_projection["parallel_portfolio"],
        "parent_reflective_theory": theory_projection["parent_reflective_theory"],
    }
    ancestor_bytes = _json_bytes(ancestor_projection)
    committed_ancestor = {
        "encoding": "sorted_indented_json_utf8_with_terminal_newline_v1",
        "projection": ancestor_projection,
        "byte_size": len(ancestor_bytes),
        "byte_digest": bytes_digest(ancestor_bytes),
    }
    parent = theory_projection["parent_reflective_theory"]
    programme = parent["theoretical_programme"]
    generator_digest = canonical_digest(
        {
            "high_risk_portfolio": theory_projection["high_risk_portfolio"],
            "parallel_portfolio": theory_projection["parallel_portfolio"],
        }
    )
    obligations = programme.get("proof_or_model_obligations", [])
    if not obligations:
        raise ContractError("five-world precommitment lacks a theory-generated premise")
    precommitment: dict[str, Any] = {
        "schema_version": "1.0.0",
        "premise_id": stable_identifier(
            "five-world-premise", programme["programme_id"], obligations[0]
        ),
        "premise_statement": str(obligations[0]),
        "theory_programme_id": programme["programme_id"],
        "source_theory_programme_digest": canonical_digest(programme),
        "conceptual_system_ids": sorted(
            row["system_id"] for row in parent.get("conceptual_systems", [])
        ),
        "generator_projection_digest": generator_digest,
        "schedule_projection_digest": canonical_digest(schedule_projection),
        "registered_world_ids": list(DECLARED_EXPERIMENT_WORLD_IDS),
        "theory_identity_locked": True,
        "direct_selection_authorized": False,
        "direct_proof_authorized": False,
        "direct_evidence_relation_authorized": False,
    }
    precommitment["precommitment_digest"] = canonical_digest(precommitment)
    executed_spec_binding = (
        {
            "spec_id": experiment_spec["spec_id"],
            "execution_id": experiment_spec["execution_id"],
            "precommitted_receipt_id": experiment_spec["precommitted_receipt_id"],
            "spec_digest": experiment_spec["spec_digest"],
            "tested_claim_digest": experiment_spec["tested_theory_claim"]["claim_digest"],
        }
        if experiment_spec is not None
        else None
    )
    reflection_binding = (
        {
            "reflection_receipt_id": experiment_reflection_receipt[
                "reflection_receipt_id"
            ],
            "reflection_digest": experiment_reflection_receipt["reflection_digest"],
            "experiment_receipt_id": experiment_reflection_receipt[
                "experiment_binding"
            ]["receipt_id"],
            "epistemic_outcome": experiment_reflection_receipt["epistemic_outcome"],
            "decision": experiment_reflection_receipt["decision"],
            "typed_delta": copy.deepcopy(experiment_reflection_receipt["typed_delta"]),
        }
        if experiment_reflection_receipt is not None
        else None
    )
    semantics: dict[str, Any] = {
        "schema_version": "1.0.0",
        "world_id": _experiment_world_id(experiment_receipt),
        "matrix_scope": EXPERIMENT_WORLD_MATRIX_SCOPE,
        "target_id": target_id,
        "run_id": run_id,
        "prior_state_version": state_version,
        "committed_ancestor": committed_ancestor,
        "matrix_precommitment": precommitment,
        "theory_state_projection": theory_projection,
        "theory_state_projection_digest": canonical_digest(theory_projection),
        "schedule_projection": schedule_projection,
        "schedule_projection_digest": canonical_digest(schedule_projection),
        "tested_claim_binding": tested_claim,
        "executed_spec_binding": executed_spec_binding,
        "post_result_reflection_binding": reflection_binding,
        "permitted_pending_review_delta": _pending_review_delta(
            experiment_reflection_receipt,
            tested_claim,
        ),
        "direct_mutation_audit": copy.deepcopy(dict(direct_mutation_audit)),
    }
    semantics["semantics_digest"] = canonical_digest(semantics)
    return semantics


def validate_five_experiment_world_semantics(
    worlds: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Validate exact consistency across the declared five-world matrix.

    The result is deliberately finite: it proves equality for these five
    declared interventions and no more. Every nested projection is compared in
    addition to its digest so a fully rehashed one-world forgery still fails.
    """

    semantics_rows: list[dict[str, Any]] = []
    for row in worlds:
        value = row.get("experiment_world_semantics", row)
        if not isinstance(value, Mapping):
            raise ContractError("five-world matrix row is not a semantic record")
        semantics_rows.append(dict(value))
    if len(semantics_rows) != len(DECLARED_EXPERIMENT_WORLD_IDS):
        raise ContractError("five-world matrix requires exactly five world records")
    by_world: dict[str, dict[str, Any]] = {}
    for semantics in semantics_rows:
        # The comparator is also a public adversarial boundary.  Validate the
        # standalone record schema before comparing values so omission and
        # fully rehashed shape attacks cannot bypass the canonical cycle schema.
        validate_payload(semantics, "experiment_world_semantics.schema.json")
        world_id = str(semantics.get("world_id", ""))
        if world_id in by_world:
            raise ContractError(f"five-world matrix duplicates world {world_id}")
        if world_id not in DECLARED_EXPERIMENT_WORLD_IDS:
            raise ContractError(f"five-world matrix has unknown world {world_id}")
        if semantics.get("matrix_scope") != EXPERIMENT_WORLD_MATRIX_SCOPE:
            raise ContractError("five-world matrix scope changed")
        ancestor = semantics.get("committed_ancestor", {})
        ancestor_bytes = _json_bytes(ancestor.get("projection"))
        if (
            ancestor.get("encoding")
            != "sorted_indented_json_utf8_with_terminal_newline_v1"
            or ancestor.get("byte_size") != len(ancestor_bytes)
            or ancestor.get("byte_digest") != bytes_digest(ancestor_bytes)
        ):
            raise ContractError(f"world {world_id} committed ancestor bytes are invalid")
        precommitment = semantics.get("matrix_precommitment", {})
        if precommitment.get("precommitment_digest") != canonical_digest(
            precommitment, exclude_keys=("precommitment_digest",)
        ):
            raise ContractError(f"world {world_id} matrix precommitment is invalid")
        if semantics.get("theory_state_projection_digest") != canonical_digest(
            semantics.get("theory_state_projection")
        ):
            raise ContractError(f"world {world_id} theory projection digest is invalid")
        if semantics.get("schedule_projection_digest") != canonical_digest(
            semantics.get("schedule_projection")
        ):
            raise ContractError(f"world {world_id} schedule projection digest is invalid")
        delta = semantics.get("permitted_pending_review_delta", {})
        if not isinstance(delta, Mapping) or delta.get("delta_digest") != canonical_digest(
            delta,
            exclude_keys=("delta_digest",),
        ):
            raise ContractError(f"world {world_id} pending-review delta digest is invalid")
        if semantics.get("semantics_digest") != canonical_digest(
            semantics,
            exclude_keys=("semantics_digest",),
        ):
            raise ContractError(f"world {world_id} semantic record digest is invalid")
        audit = semantics.get("direct_mutation_audit", {})
        if any(
            audit.get(field) is not False
            for field in (
                "theory_identity_changed",
                "automatic_evidence_relation_recorded",
                "proof_authorized",
                "theory_selected",
            )
        ):
            raise ContractError(f"world {world_id} contains direct experiment theory authority")
        expected_receipt_count = 0 if world_id == "no_probe" else 1
        if len(audit.get("experiment_operator_receipt_ids", [])) != expected_receipt_count:
            raise ContractError(
                f"world {world_id} has the wrong experiment receipt cardinality"
            )
        if any(
            audit.get(field)
            for field in (
                "theory_mutation_event_ids",
                "automatic_evidence_relation_event_ids",
                "proof_authorization_event_ids",
                "selection_event_ids",
            )
        ):
            raise ContractError(
                f"world {world_id} contains a direct experiment mutation event"
            )
        by_world[world_id] = semantics
    if set(by_world) != set(DECLARED_EXPERIMENT_WORLD_IDS):
        raise ContractError("five-world matrix is missing a declared world")
    identities = {
        (
            row.get("target_id"),
            row.get("run_id"),
            row.get("prior_state_version"),
        )
        for row in by_world.values()
    }
    if len(identities) != 1:
        raise ContractError("five-world matrix crosses target, run, or prior state")
    baseline = by_world["no_probe"]
    if baseline.get("tested_claim_binding") is not None:
        raise ContractError("no-probe world cannot carry a tested claim binding")
    if (
        baseline.get("executed_spec_binding") is not None
        or baseline.get("post_result_reflection_binding") is not None
    ):
        raise ContractError("no-probe world cannot carry execution or reflection bindings")
    for world_id in DECLARED_EXPERIMENT_WORLD_IDS[1:]:
        binding = by_world[world_id].get("tested_claim_binding")
        if not isinstance(binding, Mapping):
            raise ContractError(f"world {world_id} lacks its tested claim binding")
        if binding.get("claim_digest") != canonical_digest(
            binding,
            exclude_keys=("claim_digest",),
        ):
            raise ContractError(f"world {world_id} tested claim digest is invalid")
        execution = by_world[world_id].get("executed_spec_binding")
        reflection = by_world[world_id].get("post_result_reflection_binding")
        if not isinstance(execution, Mapping) or not isinstance(reflection, Mapping):
            raise ContractError(f"world {world_id} lacks executed spec/reflection binding")
        if (
            execution.get("precommitted_receipt_id")
            != reflection.get("experiment_receipt_id")
            or execution.get("tested_claim_digest") != binding.get("claim_digest")
            or reflection.get("typed_delta", {}).get("delta_digest")
            != canonical_digest(
                reflection.get("typed_delta", {}),
                exclude_keys=("delta_digest",),
            )
        ):
            raise ContractError(
                f"world {world_id} crossed its precommitted spec/reflection chain"
            )
        parent = by_world[world_id]["theory_state_projection"][
            "parent_reflective_theory"
        ]
        programme = parent["theoretical_programme"]
        if (
            binding.get("theory_programme_id") != programme.get("programme_id")
            or binding.get("source_theory_programme_digest")
            != canonical_digest(programme)
        ):
            raise ContractError(
                f"world {world_id} tested claim is not bound to its parent programme"
            )
        parent_system_ids = {
            row.get("system_id") for row in parent.get("conceptual_systems", [])
        }
        if not set(binding.get("conceptual_system_ids", [])).issubset(
            parent_system_ids
        ):
            raise ContractError(
                f"world {world_id} tested claim crosses its parent conceptual systems"
            )
    for world_id, semantics in by_world.items():
        if semantics["committed_ancestor"] != baseline["committed_ancestor"]:
            raise ContractError(f"world {world_id} changed committed ancestor bytes")
        if semantics["matrix_precommitment"] != baseline["matrix_precommitment"]:
            raise ContractError(f"world {world_id} changed the precommitted premise/spec")
        if semantics["theory_state_projection"] != baseline["theory_state_projection"]:
            raise ContractError(f"world {world_id} changed complete semantic theory state")
        if semantics["schedule_projection"] != baseline["schedule_projection"]:
            raise ContractError(f"world {world_id} changed complete semantic schedule")
        delta = semantics["permitted_pending_review_delta"]
        reflection = semantics.get("post_result_reflection_binding")
        if reflection is not None and delta != reflection.get("typed_delta"):
            raise ContractError(f"world {world_id} delta is not issued by executed reflection")
        if world_id == "registered_premise_falsifier":
            binding = semantics.get("tested_claim_binding")
            if not isinstance(binding, Mapping):
                raise ContractError("registered-premise world lacks its tested claim binding")
            expected = {
                "status": "pending",
                "kind": "registered_premise_review",
                "tested_claim_id": binding["claim_id"],
                "tested_claim_digest": binding["claim_digest"],
                "theory_programme_id": binding["theory_programme_id"],
                "source_theory_programme_digest": binding[
                    "source_theory_programme_digest"
                ],
                "source_reflection_packet_digest": binding[
                    "source_reflection_packet_digest"
                ],
                "conceptual_system_ids": list(binding["conceptual_system_ids"]),
                "requested_followup_kind": "reflect",
                "review_reason": "registered_premise_falsified_within_declared_scope",
                "theory_identity_changed": False,
                "ontology_mutation_authorized": False,
                "selection_authorized": False,
                "proof_authorized": False,
                "automatic_evidence_relation_authorized": False,
                "schedule_mutation_authorized": False,
            }
            if {key: delta.get(key) for key in expected} != expected:
                raise ContractError("registered-premise pending review is bound to the wrong claim")
            if (
                binding.get("claim_kind") != "theory_premise"
                or reflection.get("epistemic_outcome") != "falsifies_claim"
                or reflection.get("decision")
                != "pending_registered_premise_review"
            ):
                raise ContractError("pending review was not issued by a registered-premise falsifier")
        elif any(
            (
                delta.get("status") != "none",
                delta.get("kind") != "none",
                delta.get("tested_claim_id") is not None,
                bool(delta.get("conceptual_system_ids")),
            )
        ):
            raise ContractError(f"world {world_id} carries an unauthorized pending review")
    certificate = {
        "schema_version": "1.0.0",
        "matrix_scope": EXPERIMENT_WORLD_MATRIX_SCOPE,
        "world_ids": list(DECLARED_EXPERIMENT_WORLD_IDS),
        "target_id": baseline["target_id"],
        "run_id": baseline["run_id"],
        "prior_state_version": baseline["prior_state_version"],
        "theory_state_projection_digest": baseline[
            "theory_state_projection_digest"
        ],
        "schedule_projection_digest": baseline["schedule_projection_digest"],
        "committed_ancestor_byte_digest": baseline["committed_ancestor"]["byte_digest"],
        "matrix_precommitment_digest": baseline["matrix_precommitment"][
            "precommitment_digest"
        ],
        "theory_identity_changed": False,
        "theory_selected": False,
        "proof_authorized": False,
        "automatic_evidence_relation_recorded": False,
        "only_permitted_delta": "registered_premise_review_pending",
    }
    certificate["certificate_digest"] = canonical_digest(certificate)
    return certificate


def run_canonical_discovery_cycle(
    *,
    workspace: Path | str,
    state_root: Path | str,
    target_id: str,
    run_id: str,
    state_version: int,
    operator_requests: Sequence[Mapping[str, Any]],
    operator_receipts: Sequence[Mapping[str, Any]],
    artifact_roles: Mapping[str, Any],
    evaluator_identity: str,
    evaluator_version: str = "canonical-independent-evaluator/1.0.0",
    proof_request: Mapping[str, Any] | None = None,
    idempotency_key: str | None = None,
    literature_freshness_seconds: int | None = None,
    present_use_at: str | dt.datetime | None = None,
) -> dict[str, Any]:
    """Consume one complete operator wave and atomically commit its theory effect.

    Caller-authored proof requests are rejected.  A cycle may seal at most one
    registered formal-claim producer output; claim authority and any proof
    action are derived only after this transaction commits.  A cycle may
    validly contain no experiment and may schedule ``no_probe_needed`` as
    continued reflection.
    """

    workspace_path = Path(workspace).resolve()
    state_root_path = Path(state_root).resolve()
    target_id = validate_identifier(target_id, "target_id")
    run_id = validate_identifier(run_id, "run_id")
    validate_identifier(evaluator_identity, "evaluator_identity")
    if isinstance(state_version, bool) or not isinstance(state_version, int) or state_version < 0:
        raise ContractError("state_version must be a non-negative integer")
    if literature_freshness_seconds is not None and (
        isinstance(literature_freshness_seconds, bool)
        or not isinstance(literature_freshness_seconds, int)
        or literature_freshness_seconds <= 0
    ):
        raise ContractError("literature_freshness_seconds must be a positive integer or null")
    if proof_request is not None:
        raise ContractError(
            "caller-authored proof_request is disabled; use the registered "
            "formal-claim producer and post-commit proof authorization"
        )
    if present_use_at is None:
        present_use_time = dt.datetime.now(dt.timezone.utc)
    elif isinstance(present_use_at, dt.datetime):
        if present_use_at.tzinfo is None:
            raise ContractError("present_use_at must be timezone-aware")
        present_use_time = present_use_at.astimezone(dt.timezone.utc)
    else:
        present_use_time = _parse_timestamp(str(present_use_at), "present_use_at")
    present_use_text = present_use_time.isoformat().replace("+00:00", "Z")

    store = DiscoveryTransactionStore(
        state_root_path, target_id=target_id, run_id=run_id
    )
    prior_state = store.read_state(state_version)
    if prior_state is None:
        if state_version != 0:
            raise ContractError(f"canonical state generation {state_version} does not exist")
        prior_state = initial_state(target_id, run_id)
    forbidden_theory_transaction_roles = sorted(
        role
        for role in (
            "experiment_spec",
            "experiment_receipt",
            "experiment_reflection_receipt",
            "experiment_world_semantics",
        )
        if isinstance(artifact_roles, Mapping) and role in artifact_roles
    )
    if forbidden_theory_transaction_roles:
        raise ContractError(
            "same-generation experiment artifacts are forbidden in the "
            "canonical theory transaction; persist terminal observations and "
            "request reflection through the registered descendant support lane "
            f"instead: {forbidden_theory_transaction_roles}"
        )
    payloads, producers_by_role, receipt_roles, role_paths, role_source_bytes = _verify_and_load_artifacts(
        workspace=workspace_path,
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        operator_requests=operator_requests,
        operator_receipts=operator_receipts,
        artifact_roles=artifact_roles,
    )
    successful_receipts = [dict(row) for row in operator_receipts if row.get("status") == "succeeded"]
    registry_bytes = DISCOVERY_OPERATOR_REGISTRY_PATH.read_bytes()
    try:
        registry_snapshot = json.loads(registry_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError("discovery operator registry is not canonical JSON") from exc
    if (
        not isinstance(registry_snapshot, dict)
        or registry_snapshot.get("registry_id")
        != "reflective-discovery-operators"
    ):
        raise ContractError("discovery operator registry identity is invalid")
    cycle_authority_time = max(
        _parse_timestamp(str(row["completed_at"]), "operator completion")
        for row in operator_receipts
    ).isoformat().replace("+00:00", "Z")
    assimilation_resolution = payloads["literature_assimilation"][0].get("resolution", {})
    authorized_max_age = assimilation_resolution.get("max_age_seconds")
    if literature_freshness_seconds is not None and literature_freshness_seconds != authorized_max_age:
        raise ContractError(
            "canonical literature freshness cannot override the assimilation-authorized policy"
        )
    role_descriptor_digests = {
        role: [canonical_digest(payload) for payload in role_payloads]
        for role, role_payloads in payloads.items()
    }
    request_digest = canonical_digest(
        {
            "target_id": target_id,
            "run_id": run_id,
            "state_version": state_version,
            "receipt_ids": sorted(row["receipt_id"] for row in successful_receipts),
            "operator_requests_digest": canonical_digest(
                sorted([dict(row) for row in operator_requests], key=lambda row: row["request_id"])
            ),
            "operator_receipts_digest": canonical_digest(
                sorted(
                    [dict(row) for row in operator_receipts],
                    key=lambda row: (row["receipt_id"], row["attempt"]),
                )
            ),
            "role_artifact_digests": role_descriptor_digests,
            "role_artifact_byte_digests": {
                role: [
                    bytes_digest(
                        resolve_workspace_path(workspace_path, path, must_exist=True).read_bytes()
                    )
                    for path in paths
                ]
                for role, paths in role_paths.items()
            },
            "operator_registry_file_digest": bytes_digest(registry_bytes),
            "evaluator_identity": evaluator_identity,
            "evaluator_version": evaluator_version,
            "proof_request": dict(proof_request) if proof_request else None,
            "literature_freshness_seconds": authorized_max_age,
            "present_use_at": present_use_text,
        }
    )
    cycle_id = stable_identifier("cycle", target_id, run_id, state_version, request_digest)
    commit_key = idempotency_key or stable_identifier("cycle-commit", cycle_id)
    validate_identifier(commit_key, "idempotency_key")
    cycle_directory = f"branches/root/cycles/{cycle_id}"
    artifact_namespace = Namespace(target_id, run_id, "root", state_version)
    (
        operator_evidence,
        sealed_evidence_artifacts,
        sealed_artifact_roles,
        sealed_input_payloads,
    ) = _seal_operator_evidence(
        workspace=workspace_path,
        cycle_id=cycle_id,
        cycle_directory=cycle_directory,
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        operator_requests=operator_requests,
        operator_receipts=operator_receipts,
        role_paths=role_paths,
        namespace=artifact_namespace,
        role_source_bytes=role_source_bytes,
    )
    literature_mode, literature_id, literature_digest = _validate_core_identity(
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        prior_state=prior_state,
        payloads=payloads,
        workspace=workspace_path,
        present_use_at=present_use_time,
    )
    _validate_stage_causality(
        operator_requests=operator_requests,
        input_payloads=sealed_input_payloads,
        payloads=payloads,
        producers_by_role=producers_by_role,
        role_paths=role_paths,
    )
    source_authority_pair = validate_source_authority_pair_execution(
        active_required=literature_mode == "active_current",
        payloads=payloads,
        producers_by_role=producers_by_role,
        operator_requests=operator_requests,
        operator_receipts=operator_receipts,
        input_payloads=sealed_input_payloads,
        require_artifact_producers=True,
    )
    snapshot = payloads["literature_snapshot"][0]
    literature_input_bundle = validate_portable_literature_production_input_bundle(
        payloads["literature_production_input_bundle"][0]
    )
    literature_input_projection = literature_input_bundle[
        "semantic_consumer_projection"
    ]
    assimilation = payloads["literature_assimilation"][0]
    freshness = _freshness_policy(
        snapshot,
        assimilation,
        resolve_present_literature_freshness(assimilation, now=present_use_time),
    )
    portfolio = payloads["high_risk_portfolio"][0]
    parallel = payloads["parallel_portfolio"][0]
    reflections = payloads["reflective_packets"]
    if len(reflections) != 2:
        raise ContractError(
            "canonical conceptual discovery requires exactly one parent and one synthesis packet"
        )
    final_reflection = reflections[-1]
    parent_adjudication_evidence = payloads.get(
        "parent_conceptual_adjudication", [None]
    )[0]
    synthesis_adjudication_evidence = payloads.get(
        "synthesis_conceptual_adjudication", [None]
    )[0]
    conceptual_authority = derive_conceptual_authority(
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        literature_mode=literature_mode,
        parent_packet=reflections[0],
        synthesis_packet=final_reflection,
        parent_evidence=parent_adjudication_evidence,
        synthesis_evidence=synthesis_adjudication_evidence,
    )
    if conceptual_authority.get("status") in {"sealed_unique", "sealed_plural"}:
        final_reflection = finalize_post_adjudication_reflection(
            synthesis_packet=final_reflection,
            conceptual_authority=conceptual_authority,
        )
    experiment_spec = payloads.get("experiment_spec", [None])[0]
    experiment_receipt = payloads.get("experiment_receipt", [None])[0]

    events, append_event = _event_builder(
        prior_state,
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        occurred_at=cycle_authority_time,
    )
    literature_operator_receipts = _source_receipt_ids(
        producers_by_role, "literature_snapshot", "literature_assimilation"
    )
    search_lane_receipts = sorted(
        {
            identifier
            for receipt in snapshot.get("lane_receipts", [])
            for identifier in [receipt.get("lane_id"), *receipt.get("validator_receipt_ids", [])]
            if identifier
        }
    )
    snapshot_validator_receipts = sorted(
        receipt["receipt_id"] for receipt in snapshot.get("validator_receipts", [])
    )
    literature_receipts = sorted(
        set([*literature_operator_receipts, *search_lane_receipts, *snapshot_validator_receipts])
    )
    valid_results = {
        row["branch_id"]: row
        for row in parallel.get("branch_results", [])
        if row.get("literature_status") in {"current", "rebased"}
    }
    branch_rebases = [
        {
            "branch_id": branch_id,
            "disposition": "survives",
            "theory_delta": {
                "literature_status": result["literature_status"],
                "literature_digest": result["literature_digest"],
            },
        }
        for branch_id, result in sorted(valid_results.items())
    ]
    append_event(
        branch_id="root",
        event_type="literature_snapshot_recorded",
        entity_type="literature_snapshot",
        entity_id=literature_id,
        payload={
            "completed_at": snapshot["search_completed_at"],
            "coverage_cutoff": _date_time(snapshot.get("coverage_cutoff"), snapshot["search_completed_at"]),
            "content_digest": literature_digest,
            "source_claim_mappings": copy.deepcopy(assimilation.get("theory_mappings", [])),
            "source_theory_deltas": copy.deepcopy(assimilation.get("ledger_events", [])),
            "affected_branch_ids": sorted(valid_results),
            "survivor_branch_ids": sorted(valid_results),
            "branch_rebases": branch_rebases,
            "provenance_mode": snapshot["provenance_mode"],
            "investment_gate": literature_mode,
            "search_lane_receipt_ids": search_lane_receipts,
            "snapshot_validator_receipt_ids": snapshot_validator_receipts,
            "assimilation_operator_receipt_ids": literature_operator_receipts,
            "assimilation_packet_id": assimilation["packet_id"],
            "assimilation_content_digest": assimilation["content_digest"],
            "source_routing_pre_map_policy_id": (
                source_authority_pair["pre_map_policy"]["policy_id"]
                if source_authority_pair is not None
                else None
            ),
            "source_routing_pre_map_policy_digest": (
                source_authority_pair["pre_map_policy"]["policy_digest"]
                if source_authority_pair is not None
                else None
            ),
            "source_routing_realization_id": (
                source_authority_pair["realization"]["realization_id"]
                if source_authority_pair is not None
                else None
            ),
            "source_routing_realization_digest": (
                source_authority_pair["realization"]["realization_digest"]
                if source_authority_pair is not None
                else None
            ),
        },
        source_receipt_ids=literature_receipts,
    )
    if source_authority_pair is not None:
        for role, artifact_key, artifact_id_key, artifact_digest_key in (
            (
                "source_routing_pre_map_policy",
                "pre_map_policy",
                "policy_id",
                "policy_digest",
            ),
            (
                "source_routing_realization",
                "realization",
                "realization_id",
                "realization_digest",
            ),
        ):
            artifact = source_authority_pair[artifact_key]
            producer = producers_by_role[role][0]
            semantic_row = _canonical_semantic_output_rows(
                producer["operator"]["operator_id"], artifact
            )[0]
            append_event(
                branch_id="root",
                event_type="reflection_recorded",
                entity_type="reflection",
                entity_id=semantic_row["semantic_id"],
                payload={
                    "kind": role,
                    "source_authority_artifact_id": artifact[artifact_id_key],
                    "source_authority_artifact_digest": artifact[
                        artifact_digest_key
                    ],
                    "source_authority_artifact": copy.deepcopy(artifact),
                    "semantic_projection": {
                        **semantic_row,
                        "source_output_path": role_paths[role][0],
                    },
                    "authority_boundary": AUTHORITY_BOUNDARY,
                },
                source_receipt_ids=[producer["receipt_id"]],
            )
    assimilation_path = role_paths["literature_assimilation"][0]
    assimilation_receipt_id = producers_by_role["literature_assimilation"][0]["receipt_id"]
    for row in semantic_output_rows("frontier-literature-assimilator", assimilation):
        append_event(
            branch_id="root",
            event_type="reflection_recorded",
            entity_type="reflection",
            entity_id=row["semantic_id"],
            payload={
                "kind": "literature_assimilation_mapping",
                "semantic_projection": {**row, "source_output_path": assimilation_path},
                "assimilation_packet_id": assimilation["packet_id"],
                "assimilation_content_digest": assimilation["content_digest"],
                "mapping": next(
                    item for item in assimilation["theory_mappings"]
                    if item["mapping_id"] == row["semantic_id"]
                ),
            },
            source_receipt_ids=[assimilation_receipt_id],
        )

    portfolio_receipts = _source_receipt_ids(producers_by_role, "high_risk_portfolio")
    hypotheses = {row["hypothesis_id"]: row for row in portfolio["hypotheses"]}
    concept_ids_by_hypothesis: dict[str, list[str]] = {}
    for hypothesis_id, hypothesis in sorted(hypotheses.items()):
        concept_ids = _hypothesis_concept_ids(hypothesis)
        concept_ids_by_hypothesis[hypothesis_id] = concept_ids
        ontology = hypothesis.get("ontology_delta", {})
        primitives = list(ontology.get("new_primitives", [])) or [hypothesis.get("mechanism_key", hypothesis_id)]
        for concept_id, primitive in zip(concept_ids, primitives, strict=True):
            append_event(
                branch_id="root",
                event_type="entity_upsert",
                entity_type="concept",
                entity_id=concept_id,
                payload={
                    "record": {
                        "concept_id": concept_id,
                        "primitive": primitive,
                        "hypothesis_ids": [hypothesis_id],
                        "literature_snapshot_digest": literature_digest,
                        "lifecycle_state": "literature_rebased" if literature_mode == "active_current" else "incubating_local_only",
                    }
                },
                source_receipt_ids=portfolio_receipts,
            )
        record = copy.deepcopy(hypothesis)
        record["concept_ids"] = concept_ids
        record["literature_snapshot_digest"] = literature_digest
        record["source_portfolio_id"] = portfolio["portfolio_id"]
        record["source_portfolio_digest"] = portfolio["content_digest"]
        if literature_mode != "active_current":
            record["concept_lifecycle_state"] = "incubating"
            record["novelty_claim"] = False
            record["canonical_restrictions"] = ["local_only", "no_novelty_claim", "no_active_investment", "no_promotion"]
        hypothesis_row = next(
            row
            for row in semantic_output_rows("high-risk-hypothesis-forger", portfolio)
            if row["semantic_id"] == hypothesis_id
        )
        append_event(
            branch_id="root",
            event_type="entity_upsert",
            entity_type="hypothesis",
            entity_id=hypothesis_id,
            payload={
                "record": record,
                "semantic_projection": {
                    **hypothesis_row,
                    "source_output_path": role_paths["high_risk_portfolio"][0],
                },
            },
            source_receipt_ids=portfolio_receipts,
        )

    parallel_receipts = _source_receipt_ids(producers_by_role, "parallel_portfolio")
    branch_by_hypothesis: dict[str, str] = {}
    for request in parallel.get("branch_requests", []):
        branch_id = request["branch_id"]
        hypothesis_id = request["hypothesis_id"]
        branch_by_hypothesis[hypothesis_id] = branch_id
        result = valid_results.get(branch_id)
        append_event(
            branch_id=branch_id,
            event_type="entity_upsert",
            entity_type="branch",
            entity_id=branch_id,
            payload={
                "record": {
                    "branch_id": branch_id,
                    "hypothesis_id": hypothesis_id,
                    "concept_ids": concept_ids_by_hypothesis[hypothesis_id],
                    "status": "validated" if result else "operational_failure",
                    "maturity": "incubating",
                    "literature_snapshot_id": literature_id,
                    "literature_snapshot_digest": literature_digest,
                    "pre_search_genealogy": list(request.get("pre_search_genealogy", [])),
                }
            },
            source_receipt_ids=parallel_receipts,
        )
    results_by_branch = {row["branch_id"]: row for row in parallel.get("branch_results", [])}
    contradiction_edges = parallel.get("merge_proposal", {}).get("contradiction_edges", [])
    for attempt in parallel.get("attempt_receipts", []):
        branch_id = attempt["branch_id"]
        status = attempt["status"]
        outcome = "validated" if status in {"completed", "reused"} else "timed_out" if status == "timeout" else "failed"
        result = results_by_branch.get(branch_id)
        attempt_row = next(
            row
            for row in semantic_output_rows("parallel-hypothesis-portfolio", parallel)
            if row["semantic_id"] == attempt["receipt_id"]
        )
        append_event(
            branch_id=branch_id,
            event_type="branch_attempt_recorded",
            entity_type="branch_attempt",
            entity_id=attempt["receipt_id"],
            payload={
                "branch_id": branch_id,
                "outcome": outcome,
                "parent_branch_ids": list(
                    next(
                        (row.get("depends_on_branch_ids", []) for row in parallel["branch_requests"] if row["branch_id"] == branch_id),
                        [],
                    )
                ),
                "conflicts": [
                    edge
                    for edge in contradiction_edges
                    if branch_id in {edge.get("left_branch_id"), edge.get("right_branch_id"), edge.get("source_branch_id"), edge.get("target_branch_id")}
                ],
                "artifact_digests": [result["output_digest"]] if result and result.get("output_digest") else [],
                "operational_status": status,
                "failure_class": attempt.get("failure_class"),
                "parallel_portfolio_id": parallel["portfolio_id"],
                "parallel_portfolio_digest": parallel["content_digest"],
                "semantic_projection": {
                    **attempt_row,
                    "source_output_path": role_paths["parallel_portfolio"][0],
                },
            },
            source_receipt_ids=parallel_receipts,
        )

    reflection_receipts = _source_receipt_ids(producers_by_role, "reflective_packets")
    all_systems: dict[str, dict[str, Any]] = {}
    all_system_concepts: dict[str, list[str]] = {}
    seen_concepts = {
        concept_id
        for concept_ids in concept_ids_by_hypothesis.values()
        for concept_id in concept_ids
    }
    seen_system_records: dict[str, str] = {}
    seen_understanding: set[str] = set()
    for packet_index, packet in enumerate(reflections):
        packet_path = role_paths["reflective_packets"][packet_index]
        packet_producer = next(
            receipt
            for receipt in producers_by_role["reflective_packets"]
            if any(item["path"] == packet_path for item in receipt["output_artifacts"])
        )
        packet_receipts = [packet_producer["receipt_id"]]
        packet_rows = semantic_output_rows(
            packet_producer["operator"]["operator_id"], packet
        )
        material_rows = {
            row["row_digest"]: row
            for row in packet_rows
            if row["semantic_kind"] in {"material_reflection_round", "reflection_plateau_round"}
        }
        packet_systems = {row["system_id"]: row for row in packet.get("conceptual_systems", [])}
        all_systems.update(copy.deepcopy(packet_systems))
        for system_id, system in sorted(packet_systems.items()):
            ancestry = _system_hypotheses(system_id, packet_systems, set(hypotheses))
            system_concepts = sorted(
                {value for hypothesis_id in ancestry for value in concept_ids_by_hypothesis.get(hypothesis_id, [])}
            )
            if not system_concepts:
                system_concepts = [stable_identifier("concept", system_id, primitive) for primitive in system.get("primitives", [])[:2]]
                for concept_id, primitive in zip(system_concepts, system.get("primitives", [])[:2], strict=True):
                    if (
                        concept_id not in prior_state.get("concepts", {})
                        and concept_id not in seen_concepts
                    ):
                        append_event(
                            branch_id="root",
                            event_type="entity_upsert",
                            entity_type="concept",
                            entity_id=concept_id,
                            payload={"record": {"concept_id": concept_id, "primitive": primitive, "system_ids": [system_id]}},
                            source_receipt_ids=reflection_receipts,
                        )
                    seen_concepts.add(concept_id)
            all_system_concepts[system_id] = system_concepts
            system_record = copy.deepcopy(system)
            system_record["concept_ids"] = system_concepts
            system_record["hypothesis_ids"] = ancestry
            if literature_mode != "active_current":
                # The packet lifecycle is part of the sealed candidate bytes
                # consumed by synthesis. Local incubation is an orthogonal
                # canonical disposition and must never rewrite that evidence.
                system_record["canonical_lifecycle_state"] = "incubating_local_only"
                system_record["canonical_restrictions"] = ["local_only", "no_theoretical_preference", "no_active_investment"]
            system_digest = canonical_digest(system_record)
            prior_system_digest = seen_system_records.get(system_id)
            should_upsert = prior_system_digest is None
            if prior_system_digest is not None and prior_system_digest != system_digest:
                raise ContractError(
                    f"synthesizer changed stable conceptual system {system_id}; material integration "
                    "must be emitted as a new candidate identity before final adjudication"
                )
            if should_upsert:
                seen_system_records[system_id] = system_digest
                append_event(
                    branch_id="root",
                    event_type="entity_upsert",
                    entity_type="conceptual_system",
                    entity_id=system_id,
                    payload={"record": system_record},
                    source_receipt_ids=reflection_receipts,
                )
        for round_row in packet.get("reflection_rounds", []):
            semantic_row = material_rows.get(canonical_digest(round_row))
            if semantic_row is None:
                continue
            append_event(
                branch_id="root",
                event_type="reflection_recorded",
                entity_type="reflection",
                entity_id=semantic_row["semantic_id"],
                payload={
                    **copy.deepcopy(round_row),
                    "literature_mode": literature_mode,
                    "packet_id": packet["packet_id"],
                    "packet_digest": packet["packet_digest"],
                    "semantic_projection": {
                        **semantic_row,
                        "source_output_path": packet_path,
                    },
                },
                source_receipt_ids=packet_receipts,
            )
        programme = packet["theoretical_programme"]
        consequence_rows = [
            row for row in packet_rows if row["semantic_kind"] == "synthesis_consequence"
        ]
        for semantic_row, consequence in zip(
            consequence_rows, programme["consequences_to_derive"], strict=True
        ):
            append_event(
                branch_id="root",
                event_type="reflection_recorded",
                entity_type="reflection",
                entity_id=semantic_row["semantic_id"],
                payload={
                    "kind": "synthesis_consequence",
                    "packet_id": packet["packet_id"],
                    "packet_digest": packet["packet_digest"],
                    "programme_id": programme["programme_id"],
                    "programme_digest": canonical_digest(programme),
                    "consequence": consequence,
                    "semantic_projection": {
                        **semantic_row,
                        "source_output_path": packet_path,
                    },
                },
                source_receipt_ids=packet_receipts,
            )
        delta_id = stable_identifier("understanding", packet["packet_id"], packet["understanding_delta"])
        if delta_id not in seen_understanding:
            seen_understanding.add(delta_id)
            append_event(
                branch_id="root",
                event_type="understanding_delta_recorded",
                entity_type="understanding_delta",
                entity_id=delta_id,
                payload={
                    **copy.deepcopy(packet["understanding_delta"]),
                    "packet_id": packet["packet_id"],
                    "authority": "independent_evaluation_required_for_conceptual_preference",
                },
                source_receipt_ids=reflection_receipts,
            )

    # The synthesizer's distinct epistemic contribution is the material use of
    # branch deltas and dissent.  It is recorded after immutable upstream packet
    # ingestion, so the original operator outputs remain auditable.
    synthesis_receipts = sorted(
        {
            receipt["receipt_id"]
            for receipt in producers_by_role["reflective_packets"]
            if receipt["operator"]["operator_id"] == "reflective-theory-synthesizer"
        }
    ) or reflection_receipts
    synthesis_operator_records = [
        receipt
        for receipt in producers_by_role["reflective_packets"]
        if receipt["operator"]["operator_id"]
        in {"reflective-theory-synthesizer", "local-reflective-synthesizer"}
    ]
    experiment_reflection_receipt: dict[str, Any] | None = None
    if experiment_receipt is not None:
        if len(synthesis_operator_records) != 1 or len(reflections) < 2:
            raise ContractError(
                "an experiment requires exactly one executed post-result synthesizer"
            )
        experiment_reflection_receipt = build_experiment_reflection_receipt(
            experiment_spec,
            experiment_receipt,
            reflections[-2],
            reflections[-1],
            synthesis_operator_records[0],
            work_directory=workspace_path,
        )
    for role, evidence in (
        ("parent_conceptual_adjudication", parent_adjudication_evidence),
        ("synthesis_conceptual_adjudication", synthesis_adjudication_evidence),
    ):
        if evidence is None:
            continue
        evidence_path = role_paths[role][0]
        evidence_receipt = producers_by_role[role][0]
        for semantic_row in semantic_output_rows(
            "blind-conceptual-preference-adjudicator", evidence
        ):
            append_event(
                branch_id="root",
                event_type="reflection_recorded",
                entity_type="reflection",
                entity_id=semantic_row["semantic_id"],
                payload={
                    "kind": semantic_row["semantic_kind"],
                    "stage_id": evidence["stage_id"],
                    "evidence_id": evidence["evidence_id"],
                    "evidence_digest": evidence["evidence_digest"],
                    "preference_set": copy.deepcopy(evidence["preference_set"]),
                    "conceptual_adjudication_evidence": copy.deepcopy(evidence),
                    "semantic_projection": {
                        **semantic_row,
                        "source_output_path": evidence_path,
                    },
                },
                source_receipt_ids=[evidence_receipt["receipt_id"]],
            )

    def append_strict_synthesis(
        stage_name: str,
        packet: Mapping[str, Any],
        evidence: Mapping[str, Any] | None,
    ) -> None:
        systems = _ordered_packet_systems(packet)
        system_ids = [str(row["system_id"]) for row in systems]
        if evidence is None:
            preferred_ids: list[str] = []
            diagnostic_ids = [
                str(value)
                for value in packet.get("provisional_synthesis", {}).get(
                    "diagnostic_synthesis_system_ids", []
                )
            ]
            if not diagnostic_ids or not set(diagnostic_ids).issubset(system_ids):
                raise ContractError(
                    "local-only synthesis requires a nonempty diagnostic set inside its candidate set"
                )
            preference_authorized = False
        else:
            preference = validate_sealed_preference_authority(
                evidence,
                target_id=target_id,
                run_id=run_id,
                state_version=state_version,
                system_ids=system_ids,
                systems=systems,
                reflection_rounds=packet.get("reflection_rounds", []),
            )
            preferred_ids = [str(value) for value in preference["preferred_system_ids"]]
            if preference["decision"] == "revise_all":
                diagnostic_ids = [
                    str(value) for value in preference.get("nondominated_system_ids", [])
                ] or system_ids
                preference_authorized = False
            else:
                diagnostic_ids = []
                preference_authorized = True
        authority_ids = [*preferred_ids, *diagnostic_ids]
        systems_by_id = {str(row["system_id"]): row for row in systems}
        packet_path = role_paths["reflective_packets"][
            0 if stage_name == "parent" else -1
        ]
        source_ids = [
            receipt["receipt_id"]
            for receipt in producers_by_role["reflective_packets"]
            if any(
                descriptor["path"] == packet_path
                for descriptor in receipt["output_artifacts"]
            )
        ]
        if evidence is not None:
            evidence_role = f"{stage_name}_conceptual_adjudication"
            source_ids.extend(
                receipt["receipt_id"] for receipt in producers_by_role[evidence_role]
            )
        append_event(
            branch_id="root",
            event_type="synthesis_recorded",
            entity_type="synthesis",
            entity_id=stable_identifier(
                "synthesis", stage_name, packet["packet_id"], authority_ids
            ),
            payload={
                "component_system_ids": system_ids,
                "unification_maps": [
                    {
                        "system_id": system_id,
                        "unification_map": copy.deepcopy(
                            systems_by_id[system_id]["unification_claims"]
                        ),
                        "preserved_differences": copy.deepcopy(
                            systems_by_id[system_id]["unification_claims"].get(
                                "preserved_differences",
                                systems_by_id[system_id]["unification_claims"].get(
                                    "differences_preserved", []
                                ),
                            )
                        ),
                    }
                    for system_id in authority_ids
                ],
                "conceptual_systems": systems,
                "reflection_rounds": copy.deepcopy(
                    packet.get("reflection_rounds", [])
                ),
                "conceptual_adjudication_evidence": (
                    copy.deepcopy(dict(evidence))
                    if isinstance(evidence, Mapping)
                    else None
                ),
                "preferred_system_ids": preferred_ids,
                "diagnostic_synthesis_system_ids": diagnostic_ids,
                "preference_authorized": preference_authorized,
                "authority_boundary": SYNTHESIS_AUTHORITY_BOUNDARY,
                "authority_nulls": copy.deepcopy(SYNTHESIS_AUTHORITY_NULLS),
            },
            source_receipt_ids=sorted(set(source_ids)),
        )

    append_strict_synthesis(
        "parent", reflections[0], parent_adjudication_evidence
    )
    append_strict_synthesis(
        "synthesis", final_reflection, synthesis_adjudication_evidence
    )

    # Structural evaluation is retained nowhere in the preference path. The
    # complete blind adjudication artifacts above are the sole authority.
    evaluations: list[dict[str, Any]] = []
    evaluation_identities: list[dict[str, Any]] = []

    system_ids_by_hypothesis: dict[str, list[str]] = {
        hypothesis_id: sorted(
            system_id
            for system_id in all_systems
            if hypothesis_id
            in _system_hypotheses(system_id, all_systems, set(hypotheses))
        )
        for hypothesis_id in hypotheses
    }
    formal_claim_output = payloads.get("formal_claim_output", [None])[0]
    formal_claim_receipt: dict[str, Any] | None = None
    formal_claim_request: dict[str, Any] | None = None
    formal_claim_input: dict[str, Any] | None = None
    formal_claim_event: dict[str, Any] | None = None
    if formal_claim_output is not None:
        if (
            literature_mode != "active_current"
            or source_authority_pair is None
            or experiment_spec is not None
            or experiment_receipt is not None
        ):
            raise ContractError(
                "registered formal-claim production requires active-current literature "
                "authority and forbids same-cycle experiment ancestry"
            )
        formal_claim_output = validate_formal_claim_producer_output(
            formal_claim_output
        )
        formal_producers = producers_by_role.get("formal_claim_output", [])
        if (
            len(formal_producers) != 1
            or formal_producers[0]["operator"]["operator_id"]
            != "formal-claim-producer"
        ):
            raise ContractError(
                "formal-claim output lacks one registered producer receipt"
            )
        formal_claim_receipt = formal_producers[0]
        requests_by_id = {
            str(row["request_id"]): dict(row) for row in operator_requests
        }
        formal_claim_request = requests_by_id[formal_claim_receipt["request_id"]]
        formal_inputs = sealed_input_payloads.get(formal_claim_request["request_id"], [])
        if len(formal_inputs) != 1:
            raise ContractError(
                "formal-claim producer requires one exact sealed input envelope"
            )
        formal_claim_input = validate_formal_claim_producer_input(
            formal_inputs[0], workspace=workspace_path
        )
        if build_formal_claim_producer_output(
            formal_claim_input, workspace=workspace_path
        ) != formal_claim_output:
            raise ContractError(
                "formal-claim output differs from canonical independent replay"
            )

        synthesis_path = role_paths["reflective_packets"][-1]
        synthesis_receipts = [
            receipt
            for receipt in producers_by_role["reflective_packets"]
            if any(
                descriptor["path"] == synthesis_path
                for descriptor in receipt["output_artifacts"]
            )
        ]
        if len(synthesis_receipts) != 1:
            raise ContractError(
                "formal-claim ancestry lacks one synthesis producer receipt"
            )
        synthesis_receipt = synthesis_receipts[0]
        synthesis_request = requests_by_id[synthesis_receipt["request_id"]]
        parent_evidence = conceptual_authority.get("parent_evidence")
        synthesis_evidence = conceptual_authority.get("synthesis_evidence")
        if not isinstance(parent_evidence, Mapping) or not isinstance(
            synthesis_evidence, Mapping
        ):
            raise ContractError(
                "formal-claim ancestry lacks sealed conceptual adjudication evidence"
            )
        expected_literature_authority = {
            "authority_kind": "validated_target_scoped_literature_snapshot",
            "snapshot_id": literature_id,
            "snapshot_digest": literature_digest,
            "literature_production_projection_digest": literature_input_projection[
                "projection_digest"
            ],
            "source_routing_pre_map_policy_digest": source_authority_pair[
                "pre_map_policy"
            ]["policy_digest"],
            "source_routing_realization_digest": source_authority_pair[
                "realization"
            ]["realization_digest"],
            "basis_status": "current",
            "consume_before": freshness["consume_before"],
            "present_use_evaluated_at": freshness["present_use_evaluated_at"],
            "present_use_reason": freshness["present_use_reason"],
        }
        expected_theory_ancestry = {
            "conceptual_authority_digest": canonical_digest(
                conceptual_authority
            ),
            "parent_adjudication_evidence_digest": parent_evidence[
                "evidence_digest"
            ],
            "synthesis_adjudication_evidence_digest": synthesis_evidence[
                "evidence_digest"
            ],
            "preferred_system_ids": copy.deepcopy(
                conceptual_authority["preferred_system_ids"]
            ),
        }
        hypothesis_id = formal_claim_input["hypothesis_id"]
        branch_id = branch_by_hypothesis.get(hypothesis_id)
        formal_request_namespace = Namespace.from_mapping(
            formal_claim_request["identity"]
        )
        authorized_system_ids = [
            system_id
            for system_id in conceptual_authority["preferred_system_ids"]
            if system_id in system_ids_by_hypothesis.get(hypothesis_id, [])
        ]
        source_seed_rows = [
            row
            for row in formalization_seed_rows(final_reflection)
            if row["semantic_id"] == formal_claim_input["source_semantic_row_id"]
        ]
        source_system_ids = (
            [source_seed_rows[0]["row"]["system_id"]]
            if len(source_seed_rows) == 1
            else []
        )
        expected_conjecture_id = stable_identifier(
            "formal-conjecture-v2",
            target_id,
            run_id,
            state_version + 1,
            branch_id,
            hypothesis_id,
            formal_claim_input["concept_id"],
            source_system_ids,
            formal_claim_input["source_semantic_row_id"],
        )
        if (
            branch_id is None
            or formal_request_namespace.target_id != target_id
            or formal_request_namespace.run_id != run_id
            or formal_request_namespace.branch_id != branch_id
            or formal_request_namespace.state_version != state_version
            or formal_claim_input["branch_id"] != branch_id
            or formal_claim_input["concept_id"]
            not in concept_ids_by_hypothesis.get(hypothesis_id, [])
            or formal_claim_input["conceptual_system_ids"] != source_system_ids
            or formal_claim_input["conjecture_id"] != expected_conjecture_id
            or len(source_seed_rows) != 1
            or not set(source_system_ids).issubset(authorized_system_ids)
            or formal_claim_input["source_producer_request"] != synthesis_request
            or formal_claim_input["source_producer_receipt"] != synthesis_receipt
            or formal_claim_input["finalized_reflection"] != final_reflection
            or formal_claim_input["finalized_reflection_digest"]
            != final_reflection["packet_digest"]
            or formal_claim_input["conceptual_authority"] != conceptual_authority
            or formal_claim_input["conceptual_authority_digest"]
            != canonical_digest(conceptual_authority)
            or formal_claim_input["literature_authority"]
            != expected_literature_authority
            or formal_claim_input["theory_ancestry"] != expected_theory_ancestry
            or formal_claim_input["source_prior_state_version"] != state_version
            or formal_claim_input["source_theory_generation"] != state_version + 1
            or formal_claim_output["source_semantic_row_digest"]
            != source_seed_rows[0]["row_digest"]
        ):
            raise ContractError(
                "formal-claim producer input differs from the canonical cycle ancestry"
            )
        formal_semantic_row = semantic_output_rows(
            "formal-claim-producer", formal_claim_output
        )[0]
        formal_claim_event = append_event(
            branch_id=branch_id,
            event_type="reflection_recorded",
            entity_type="reflection",
            entity_id=formal_semantic_row["semantic_id"],
            payload={
                "kind": "formal_claim_production",
                "output_id": formal_claim_output["output_id"],
                "output_digest": formal_claim_output["content_digest"],
                "status": formal_claim_output["status"],
                "formal_claim_output": copy.deepcopy(formal_claim_output),
                "semantic_projection": {
                    **formal_semantic_row,
                    "source_output_path": role_paths[
                        "formal_claim_output"
                    ][0],
                },
                "authority_boundary": AUTHORITY_BOUNDARY,
            },
            source_receipt_ids=[formal_claim_receipt["receipt_id"]],
        )
    proof_handoff: dict[str, Any] | None = None

    experiment_theory_effect = (
        copy.deepcopy(experiment_receipt["theory_effect"])
        if experiment_receipt is not None
        else None
    )
    experiment_assimilation = {
        "present": experiment_receipt is not None,
        "receipt_id": experiment_receipt.get("receipt_id") if experiment_receipt else None,
        "epistemic_outcome": experiment_receipt.get("epistemic_outcome") if experiment_receipt else "not_requested",
        "theory_effect": experiment_theory_effect,
        "premise_revision_requested": bool(
            experiment_reflection_receipt
            and experiment_reflection_receipt["typed_delta"]["status"] == "pending"
        ),
        "post_result_reflection_receipt_ids": (
            [experiment_reflection_receipt["reflection_receipt_id"]]
            if experiment_reflection_receipt is not None
            else []
        ),
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    experiment_operator_receipt_ids: list[str] = []
    if experiment_receipt is not None:
        experiment_operator_receipt_ids = _source_receipt_ids(
            producers_by_role, "experiment_spec", "experiment_receipt"
        )
        append_event(
            branch_id=experiment_receipt["branch_id"],
            event_type="reflection_recorded",
            entity_type="reflection",
            entity_id=stable_identifier("reflection", experiment_receipt["receipt_id"], "assimilation"),
            payload={
                "kind": "post_result_reflective_assimilation",
                "experiment_receipt_id": experiment_receipt["receipt_id"],
                "theory_effect": experiment_theory_effect,
                "automatic_evidence_relation_recorded": False,
                "requires_reflective_review": experiment_assimilation[
                    "premise_revision_requested"
                ],
                "recommendations": copy.deepcopy(experiment_receipt["reflective_assimilation"]),
                "post_result_reflection_receipt_ids": [
                    experiment_reflection_receipt["reflection_receipt_id"]
                ],
                "post_result_reflection_digest": experiment_reflection_receipt[
                    "reflection_digest"
                ],
                "typed_delta": copy.deepcopy(
                    experiment_reflection_receipt["typed_delta"]
                ),
                "authority_boundary": AUTHORITY_BOUNDARY,
                "semantic_projection": {
                    **semantic_output_rows(
                        "dynamic-symbolic-simulation-experimenter",
                        experiment_receipt,
                    )[0],
                    "source_output_path": role_paths["experiment_receipt"][0],
                },
            },
            source_receipt_ids=sorted(
                set([*experiment_operator_receipt_ids, *synthesis_receipts])
            ),
        )

    conceptual_authority["proof_ready"] = proof_handoff is not None
    schedule = _scheduler_projection(
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        literature_mode=literature_mode,
        snapshot_id=literature_id,
        portfolio=portfolio,
        parallel=parallel,
        final_reflection=final_reflection,
        concept_ids_by_hypothesis=concept_ids_by_hypothesis,
        system_ids_by_hypothesis=system_ids_by_hypothesis,
        proof_handoff=proof_handoff,
        experiment_receipt=experiment_receipt,
        source_routing_precommit=source_authority_pair,
        conceptual_authority=conceptual_authority,
        formal_claim_output=formal_claim_output,
        formal_claim_request=formal_claim_request,
        formal_claim_receipt=formal_claim_receipt,
        formal_claim_input=formal_claim_input,
        formal_claim_event=formal_claim_event,
    )
    schedule["created_at"] = cycle_authority_time

    receipt_consumer_events: dict[str, str] = {}
    payload_by_role_path = {
        path: payloads[role][index]
        for role, paths in role_paths.items()
        for index, path in enumerate(paths)
    }
    for receipt in sorted(successful_receipts, key=lambda row: row["receipt_id"]):
        operator_id = receipt["operator"]["operator_id"]
        receipt_payloads = [
            payload_by_role_path[descriptor["path"]]
            for descriptor in receipt["output_artifacts"]
            if descriptor["path"] in payload_by_role_path
        ]
        if len(receipt_payloads) != len(receipt["output_artifacts"]):
            raise ContractError(
                f"successful operator {operator_id} has output outside the exact role map"
            )
        primary_payload = receipt_payloads[0]
        candidates = [
            event
            for event in events
            if receipt["receipt_id"] in event.get("source_receipt_ids", [])
            and event.get("payload", {}).get("kind") != "operator_output_consumed"
        ]
        role_selectors = {
            "source-routing-pre-map-policy-producer": [
                event
                for event in candidates
                if event["event_type"] == "reflection_recorded"
                and event.get("payload", {}).get("kind")
                == "source_routing_pre_map_policy"
                and event.get("payload", {}).get(
                    "source_authority_artifact_digest"
                )
                == primary_payload.get("policy_digest")
            ],
            "source-routing-realization-producer": [
                event
                for event in candidates
                if event["event_type"] == "reflection_recorded"
                and event.get("payload", {}).get("kind")
                == "source_routing_realization"
                and event.get("payload", {}).get(
                    "source_authority_artifact_digest"
                )
                == primary_payload.get("realization_digest")
            ],
            "frontier-literature-assimilator": [
                event
                for event in candidates
                if event["event_type"] == "literature_snapshot_recorded"
                and event["entity_id"] == primary_payload.get("selected_snapshot", {}).get("snapshot_id")
                and event.get("payload", {}).get("assimilation_content_digest")
                == primary_payload.get("content_digest")
            ],
            "high-risk-hypothesis-forger": [
                event
                for event in candidates
                if event["event_type"] == "entity_upsert" and event["entity_type"] == "hypothesis"
                and event.get("payload", {}).get("record", {}).get("source_portfolio_digest")
                == primary_payload.get("content_digest")
            ],
            "parallel-hypothesis-portfolio": [
                event
                for event in candidates
                if event["event_type"] == "branch_attempt_recorded"
                and event.get("payload", {}).get("parallel_portfolio_digest")
                == primary_payload.get("content_digest")
            ],
            "reflective-conceptual-discovery": [
                event
                for event in candidates
                if event["event_type"] == "reflection_recorded"
                and event.get("payload", {}).get("packet_id") == primary_payload.get("packet_id")
                and event.get("payload", {}).get("packet_digest") == primary_payload.get("packet_digest")
            ],
            "reflective-theory-synthesizer": [
                event
                for event in candidates
                if event["event_type"] == "synthesis_recorded"
                and event.get("payload", {}).get("conceptual_systems")
                == primary_payload.get("conceptual_systems")
                and event.get("payload", {}).get("reflection_rounds")
                == primary_payload.get("reflection_rounds")
            ],
            "blind-conceptual-preference-adjudicator": [
                event
                for event in candidates
                if event.get("payload", {}).get("kind")
                == "conceptual_adjudication_evidence"
                and event.get("payload", {}).get("evidence_id")
                == primary_payload.get("evidence_id")
                and event.get("payload", {}).get("evidence_digest")
                == primary_payload.get("evidence_digest")
            ],
            "dynamic-symbolic-simulation-experimenter": [
                event
                for event in candidates
                if event.get("payload", {}).get("kind")
                == "post_result_reflective_assimilation"
                and event.get("payload", {}).get("experiment_receipt_id")
                == primary_payload.get("receipt_id")
            ],
            "formal-claim-producer": [
                event
                for event in candidates
                if event["event_type"] == "reflection_recorded"
                and event.get("payload", {}).get("kind")
                == "formal_claim_production"
                and event.get("payload", {}).get("output_id")
                == primary_payload.get("output_id")
                and event.get("payload", {}).get("output_digest")
                == primary_payload.get("content_digest")
            ],
            "local-reflective-incubator": [
                event
                for event in candidates
                if event["event_type"] == "reflection_recorded"
                and event.get("payload", {}).get("packet_id") == primary_payload.get("packet_id")
                and event.get("payload", {}).get("packet_digest") == primary_payload.get("packet_digest")
            ],
            "local-reflective-synthesizer": [
                event
                for event in candidates
                if event["event_type"] == "synthesis_recorded"
                and event.get("payload", {}).get("conceptual_systems")
                == primary_payload.get("conceptual_systems")
                and event.get("payload", {}).get("reflection_rounds")
                == primary_payload.get("reflection_rounds")
            ],
        }
        if operator_id not in role_selectors:
            raise ContractError(f"successful operator has no closed semantic role: {operator_id}")
        semantic = role_selectors[operator_id]
        if not semantic:
            raise ContractError(
                f"successful operator {operator_id} has no role-specific semantic consumer event"
            )
        receipt_consumer_events[receipt["receipt_id"]] = semantic[0]["event_id"]
        append_event(
            branch_id=receipt["identity"]["branch_id"],
            event_type="reflection_recorded",
            entity_type="reflection",
            entity_id=stable_identifier("consumption", cycle_id, receipt["receipt_id"]),
            payload={
                "kind": "operator_output_consumed",
                "producer_receipt_id": receipt["receipt_id"],
                "artifact_roles": receipt_roles[receipt["receipt_id"]],
                "output_artifact_digests": [row["sha256"] for row in receipt["output_artifacts"]],
                "cycle_id": cycle_id,
            },
            source_receipt_ids=[receipt["receipt_id"]],
        )
    receipts_by_id = {row["receipt_id"]: row for row in successful_receipts}
    events_by_id = {row["event_id"]: row for row in events}
    feedback_edges = []
    for receipt_id, event_id in sorted(receipt_consumer_events.items()):
        receipt = receipts_by_id[receipt_id]
        event = events_by_id[event_id]
        semantic_projections: list[dict[str, Any]] = []
        for descriptor in receipt["output_artifacts"]:
            output_path = descriptor["path"]
            output_payload = payload_by_role_path[output_path]
            for row in _canonical_semantic_output_rows(
                receipt["operator"]["operator_id"], output_payload
            ):
                marker = {**row, "source_output_path": output_path}
                matching_events = [
                    candidate
                    for candidate in events
                    if candidate.get("payload", {}).get("semantic_projection") == marker
                    and receipt_id in candidate.get("source_receipt_ids", [])
                ]
                if len(matching_events) != 1:
                    raise ContractError(
                        f"semantic output row has {len(matching_events)} committed events: {marker}"
                    )
                semantic_event = matching_events[0]
                semantic_projections.append(
                    {
                        "output_path": output_path,
                        **row,
                        "consumer_event_id": semantic_event["event_id"],
                        "consumer_event_hash": semantic_event["event_hash"],
                    }
                )
        if not semantic_projections:
            raise ContractError(
                f"successful operator {receipt['operator']['operator_id']} has no semantic row projection"
            )
        edge = {
            "schema_version": "1.0.0",
            "feedback_edge_id": stable_identifier("feedback", receipt_id, event_id, cycle_id),
            "target_id": target_id,
            "run_id": run_id,
            "prior_state_version": state_version,
            "committed_state_generation": state_version + 1,
            "producer_receipt_id": receipt_id,
            "producer_request_id": receipt["request_id"],
            "producer_operator_id": receipt["operator"]["operator_id"],
            "producer_output_artifacts": [
                {
                    "path": descriptor["path"],
                    "sha256": descriptor["sha256"],
                    "size_bytes": descriptor["size_bytes"],
                }
                for descriptor in receipt["output_artifacts"]
            ],
            "consumer_event_id": event_id,
            "consumer_event_hash": event["event_hash"],
            "artifact_roles": receipt_roles[receipt_id],
            "semantic_event_projections": sorted(
                semantic_projections,
                key=lambda row: (
                    row["output_path"], row["semantic_kind"], row["semantic_id"]
                ),
            ),
            "consumed": True,
            "state_edge_committed": True,
            "authority_boundary": AUTHORITY_BOUNDARY,
        }
        validate_payload(edge, "discovery_feedback_edge.schema.json")
        feedback_edges.append(edge)
    assert_feedback_effective(successful_receipts, feedback_edges)

    direct_mutation_audit = _experiment_direct_mutation_audit(
        events,
        experiment_operator_receipt_ids,
    )
    experiment_assimilation.update(
        {
            "automatic_evidence_relation_recorded": direct_mutation_audit[
                "automatic_evidence_relation_recorded"
            ],
            "theory_identity_changed": direct_mutation_audit[
                "theory_identity_changed"
            ],
            "theory_selected": direct_mutation_audit["theory_selected"],
            "proof_authorized": direct_mutation_audit["proof_authorized"],
        }
    )

    next_state = reduce_from_state(prior_state, events)
    concept_ids = sorted(
        concept_id
        for hypothesis_concept_ids in concept_ids_by_hypothesis.values()
        for concept_id in hypothesis_concept_ids
    )
    identity_map = {
        "concept_ids": concept_ids,
        "hypothesis_ids": sorted(hypotheses),
        "branch_ids": sorted(row["branch_id"] for row in parallel.get("branch_requests", [])),
        "conceptual_system_ids": sorted(all_systems),
        "proof_obligation_ids": [proof_handoff["obligation_id"]] if proof_handoff else [],
        "branch_bindings": [
            {
                "branch_id": branch_id,
                "hypothesis_id": hypothesis_id,
                "concept_ids": concept_ids_by_hypothesis[hypothesis_id],
                "conceptual_system_ids": system_ids_by_hypothesis[hypothesis_id],
            }
            for hypothesis_id, branch_id in sorted(branch_by_hypothesis.items())
        ],
    }
    failure_attempts = [
        row["receipt_id"]
        for row in parallel.get("attempt_receipts", [])
        if row["status"] not in {"completed", "reused"}
    ]
    # The theory transaction never consumes an experiment or world result.
    # Optional support begins only after this commit, using the exact committed
    # projection as its immutable N -> N+7 base.  The retained v1 diagnostic
    # slot is permanently null on the canonical route.
    experiment_world_semantics = None
    cycle_core = {
        "schema_version": "1.0.0",
        "cycle_id": cycle_id,
        "target_id": target_id,
        "run_id": run_id,
        "prior_state_version": state_version,
        "next_state_version": state_version + 1,
        "literature_basis": {
            "snapshot_id": literature_id,
            "snapshot_digest": literature_digest,
            "mode": literature_mode,
            "active_investment_allowed": literature_mode == "active_current",
            "source_routing_pre_map_policy_id": (
                source_authority_pair["pre_map_policy"]["policy_id"]
                if source_authority_pair is not None
                else None
            ),
            "source_routing_pre_map_policy_digest": (
                source_authority_pair["pre_map_policy"]["policy_digest"]
                if source_authority_pair is not None
                else None
            ),
            "source_routing_realization_id": (
                source_authority_pair["realization"]["realization_id"]
                if source_authority_pair is not None
                else None
            ),
            "source_routing_realization_digest": (
                source_authority_pair["realization"]["realization_digest"]
                if source_authority_pair is not None
                else None
            ),
            **freshness,
            "restrictions": []
            if literature_mode == "active_current"
            else ["local_only", "no_novelty_claim", "no_active_investment", "no_experiment", "no_proof", "no_promotion"],
        },
        "literature_production_input": {
            "bundle_id": literature_input_bundle["bundle_id"],
            "bundle_digest": literature_input_bundle["bundle_digest"],
            "producer_run_id": literature_input_bundle["producer_run_id"],
            "state_version": literature_input_bundle["state_version"],
            "production_manifest_descriptor": copy.deepcopy(
                literature_input_bundle["production_manifest_descriptor"]
            ),
            "commitment_receipt_id": literature_input_bundle[
                "commitment_receipt"
            ]["receipt_id"],
            "commitment_receipt_digest": literature_input_bundle[
                "commitment_receipt"
            ]["receipt_digest"],
            "semantic_projection_digest": literature_input_projection[
                "projection_digest"
            ],
            "authority_nulls": copy.deepcopy(
                literature_input_projection["authority_nulls"]
            ),
            "authority_boundary": literature_input_projection[
                "authority_boundary"
            ],
        },
        "literature_production_projection_digest": literature_input_projection[
            "projection_digest"
        ],
        "input_receipt_ids": sorted(row["receipt_id"] for row in successful_receipts),
        "source_routing_pre_map_policy": copy.deepcopy(
            source_authority_pair.get("pre_map_policy")
            if source_authority_pair is not None
            else None
        ),
        "source_routing_pre_map_policy_digest": (
            source_authority_pair["pre_map_policy"]["policy_digest"]
            if source_authority_pair is not None
            else None
        ),
        "source_routing_realization": copy.deepcopy(
            source_authority_pair.get("realization")
            if source_authority_pair is not None
            else None
        ),
        "source_routing_realization_digest": (
            source_authority_pair["realization"]["realization_digest"]
            if source_authority_pair is not None
            else None
        ),
        "identity_map": identity_map,
        "parallel_outcome": {
            "valid_branch_ids": sorted(valid_results),
            "failed_or_invalid_attempt_ids": sorted(failure_attempts),
            "retained_dissent_ids": sorted(parallel.get("merge_proposal", {}).get("retained_dissent_ids", [])),
            "canonical_cas_commits": 1,
            "integration_authority": "synthesizer_candidate_set_before_final_adjudication",
            "preferred_system_ids": copy.deepcopy(
                conceptual_authority["preferred_system_ids"]
            ),
            "diagnostic_synthesis_system_ids": copy.deepcopy(
                conceptual_authority["diagnostic_synthesis_system_ids"]
            ),
        },
        "evaluation_ids": [row["evaluation_id"] for row in evaluations],
        "schedule_id": schedule["schedule_id"],
        "proof_handoff_id": proof_handoff["handoff_id"] if proof_handoff else None,
        "experiment_assimilation": experiment_assimilation,
        "experiment_reflection_receipt": experiment_reflection_receipt,
        "experiment_world_semantics": experiment_world_semantics,
        "conceptual_authority": conceptual_authority,
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    validate_payload(operator_evidence, "canonical_operator_evidence.schema.json")
    cycle_core["operator_evidence_digest"] = operator_evidence["evidence_digest"]
    artifact_payloads: dict[str, Any] = {
        "events.json": events,
        "evaluations.json": {
            "cycle_id": cycle_id,
            "candidate_identity_bindings": evaluation_identities,
            "receipts": evaluations,
            "authority_boundary": AUTHORITY_BOUNDARY,
        },
        # The synthesizer output is finalized only after blind adjudication.
        # Persist that exact reducer result rather than asking a later world
        # commission to recreate or accept it from a caller.
        "finalized-reflection.json": final_reflection,
        "schedule.json": schedule,
        "feedback-edges.json": feedback_edges,
        "cycle.json": cycle_core,
    }
    if proof_handoff:
        artifact_payloads["proof-handoff.json"] = proof_handoff
    if experiment_reflection_receipt is not None:
        artifact_payloads["experiment-reflection-receipt.json"] = (
            experiment_reflection_receipt
        )
    core_artifact_roles = {
        name.removesuffix(".json").replace("-", "_"): f"{cycle_directory}/{name}"
        for name in artifact_payloads
    }
    operator_registry_path = f"{cycle_directory}/operator-registry.json"
    core_artifact_roles["operator_registry"] = operator_registry_path
    projection_source_artifacts, projection_source_roles = (
        build_committed_cycle_projection_artifacts(
            target_id=target_id,
            run_id=run_id,
            source_cycle_prior_state_version=state_version,
            cycle_id=cycle_id,
            canonical_cycle=cycle_core,
            finalized_reflection=final_reflection,
            schedule=schedule,
            operator_evidence=operator_evidence,
            sealed_artifacts=sealed_evidence_artifacts,
            namespace=artifact_namespace,
        )
    )
    commit_artifact_roles = {
        **core_artifact_roles,
        **sealed_artifact_roles,
        **projection_source_roles,
    }
    if len(commit_artifact_roles) != len(set(commit_artifact_roles.values())):
        raise ContractError("canonical commit artifact roles are not a path bijection")
    commit_artifacts = [
        CommitArtifact(
            relative_path=f"{cycle_directory}/{name}",
            content=_json_bytes(payload),
            namespace=artifact_namespace,
        )
        for name, payload in artifact_payloads.items()
    ] + [
        CommitArtifact(
            relative_path=operator_registry_path,
            content=registry_bytes,
            namespace=artifact_namespace,
        )
    ] + sealed_evidence_artifacts + projection_source_artifacts
    result = store.commit(
        expected_generation=state_version,
        state=next_state,
        artifacts=commit_artifacts,
        idempotency_key=commit_key,
        request_digest=request_digest,
    )

    # Always return the bytes that actually won the CAS.  On an idempotent retry
    # this discards newly generated timestamps and exposes the first commit.
    committed_artifact_root = result.commit_path / "artifacts" / cycle_directory
    committed_core = json.loads((committed_artifact_root / "cycle.json").read_text(encoding="utf-8"))
    committed_events = json.loads((committed_artifact_root / "events.json").read_text(encoding="utf-8"))
    committed_evaluations = json.loads((committed_artifact_root / "evaluations.json").read_text(encoding="utf-8"))
    committed_schedule = json.loads((committed_artifact_root / "schedule.json").read_text(encoding="utf-8"))
    committed_feedback = json.loads((committed_artifact_root / "feedback-edges.json").read_text(encoding="utf-8"))
    committed_operator_evidence = json.loads(
        (committed_artifact_root / "operator-evidence.json").read_text(encoding="utf-8")
    )
    committed_proof = (
        json.loads((committed_artifact_root / "proof-handoff.json").read_text(encoding="utf-8"))
        if (committed_artifact_root / "proof-handoff.json").is_file()
        else None
    )
    assert_feedback_effective(successful_receipts, committed_feedback)
    committed_state = store.read_state(result.generation)
    if committed_state is None:
        raise ContractError("canonical transaction committed no readable state")
    manifest = json.loads((result.commit_path / "manifest.json").read_text(encoding="utf-8"))
    descriptors_by_path = {row["path"]: row for row in manifest["artifacts"]}
    if set(commit_artifact_roles.values()) != set(descriptors_by_path):
        raise ContractError("committed manifest does not exactly cover canonical artifact roles")
    descriptor_digests = {
        role: descriptors_by_path[path]["sha256"]
        for role, path in commit_artifact_roles.items()
    }
    output = {
        **committed_core,
        "committed_state_version": result.generation,
        "commit_id": result.commit_id,
        "manifest_digest": result.manifest_digest,
        "transaction_root": str(Path(state_root).resolve()),
        "commit_path": str(result.commit_path.resolve()),
        "manifest_path": str((result.commit_path / "manifest.json").resolve()),
        "idempotent": result.idempotent,
        "state_digest": canonical_digest(committed_state),
        "events": committed_events,
        "evaluation_receipts": committed_evaluations["receipts"],
        "evaluation_identity_bindings": committed_evaluations["candidate_identity_bindings"],
        "schedule": committed_schedule,
        "feedback_edges": committed_feedback,
        "operator_evidence": committed_operator_evidence,
        "proof_handoff": committed_proof,
        "artifact_paths": commit_artifact_roles,
        "artifact_digests": descriptor_digests,
    }
    validate_payload(output, "canonical_discovery_cycle.schema.json")
    return output


__all__ = [
    "AUTHORITY_BOUNDARY",
    "build_canonical_world_authority_projection",
    "derive_conceptual_authority",
    "replay_canonical_world_authority_projection",
    "run_canonical_discovery_cycle",
    "validate_source_authority_pair_execution",
]
