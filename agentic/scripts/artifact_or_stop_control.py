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
"""Artifact-or-stop control helpers for YM anti-incrementality gates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel


YM_TARGET_ID = "yang-mills-existence-and-mass-gap-target"
BLOCKER_ID = "ym.endpoint_source_table_ttail_gate"
BLOCKER_REPORT = ROOT / "agentic/reports/blocker_signatures/targets/yang-mills-existence-and-mass-gap-target/latest.json"
PROOF_OBJECT_DIR = ROOT / "agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/proof_objects"
ENDPOINT_CONTRACT_JSON = PROOF_OBJECT_DIR / "endpoint_source_table_contract.json"
ENDPOINT_CONTRACT_MD = PROOF_OBJECT_DIR / "endpoint_source_table_contract.md"
ENDPOINT_PILOT_JSON = PROOF_OBJECT_DIR / "endpoint_source_table_pilot.json"
ENDPOINT_PILOT_MD = PROOF_OBJECT_DIR / "endpoint_source_table_pilot.md"
DEMOTION_PACKET_JSON = PROOF_OBJECT_DIR / "endpoint_route_demotion_packet.json"
DEMOTION_PACKET_MD = ROOT / "agentic/reports/results_ellaboration/yang_mills_routea_endpoint_artifact_blocked_demotion.md"

ALLOWED_NEXT_MODES = [
    "artifact_sprint",
    "falsifier_sprint",
    "publication_demotion",
    "quarantine",
    "conceptual_exploration_after_release",
]
FORBIDDEN_AFTER_REPETITION = [
    "broad_api_reasoning",
    "ordinary_proof_search",
    "unbounded_publication_consolidation",
]
REQUIRED_ENDPOINT_ARTIFACTS = [
    "endpoint_source_table_contract",
    "endpoint_source_table",
    "T_tail",
    "endpoint_route_demotion_packet",
]


def endpoint_blocker_signature() -> dict[str, Any]:
    return {
        "version": 1,
        "target_id": YM_TARGET_ID,
        "blocker_signature": BLOCKER_ID,
        "canonical_statement": (
            "Missing positive-D endpoint source intervals and cutoff-uniform T_tail for the heat-kernel "
            "SU(N) three-hairpin post-H,K endpoint gate; without these, I_gate cannot be signed."
        ),
        "required_artifact": REQUIRED_ENDPOINT_ARTIFACTS,
        "allowed_next_modes": ALLOWED_NEXT_MODES,
        "forbidden_next_modes": FORBIDDEN_AFTER_REPETITION,
        "promotion_condition": (
            "Attach an endpoint source table whose I_gate lower interval is nonnegative and whose "
            "T_tail is cutoff-uniform for the fixed regulated geometry."
        ),
        "demotion_condition": (
            "If the table gives a negative upper interval or the current artifacts cannot instantiate "
            "a row, emit a finite Route A falsifier or publication-demotion packet."
        ),
        "quarantine_condition": (
            "If the endpoint source table remains underspecified, or I_gate overlaps zero, quarantine "
            "the Route A endpoint branch before returning to conceptual exploration."
        ),
        "clay_progress_boundary": (
            "This is a finite same-regulator endpoint gate only. It does not prove continuum existence, "
            "OS/Wightman reconstruction, nontriviality, or the Yang-Mills mass gap."
        ),
        "control_decision": "artifact_sprint_required",
    }


def classify_blocker_text(text: Any) -> dict[str, Any]:
    lowered = clean_text(text).lower()
    endpoint_markers = [
        "endpoint source",
        "source table",
        "positive-d",
        "positive d",
        "i_gate",
        "t_tail",
        "tail bound",
        "seven log z",
        "seven-point",
        "heat-kernel",
        "three-hairpin",
    ]
    if sum(1 for marker in endpoint_markers if marker in lowered) >= 2 and (
        "endpoint" in lowered or "hairpin" in lowered or "wilson" in lowered
    ):
        signature = endpoint_blocker_signature()
        signature["blocker_kind"] = "artifact-blocked"
        return signature
    if "literature" in lowered and ("gap" in lowered or "prior art" in lowered):
        return {
            "blocker_signature": "literature_gap_boundary",
            "blocker_kind": "literature-blocked",
            "canonical_statement": "A literature-gap or prior-art boundary must be sharpened before further investment.",
        }
    if "physical carrier" in lowered or "physical relevance" in lowered or "same-theory" in lowered:
        return {
            "blocker_signature": "physical_handoff_boundary",
            "blocker_kind": "physical-handoff-blocked",
            "canonical_statement": "A physical carrier and same-theory handoff must be named before promotion.",
        }
    if "representation" in lowered or "abstraction" in lowered:
        return {
            "blocker_signature": "conceptual_representation_boundary",
            "blocker_kind": "conceptual-representation-blocked",
            "canonical_statement": "The current representation is too weak or mismatched for the route obligation.",
        }
    return {
        "blocker_signature": "proof_obligation_boundary",
        "blocker_kind": "proof-blocked",
        "canonical_statement": clean_text(text)[:280],
    }


def blocker_report() -> dict[str, Any]:
    report = load_optional_json(BLOCKER_REPORT)
    if clean_text(report.get("target_id")) == YM_TARGET_ID:
        return report
    return {}


def endpoint_signature_from_report() -> dict[str, Any]:
    report = blocker_report()
    for signature in report.get("signatures", []) if isinstance(report.get("signatures"), list) else []:
        if clean_text(signature.get("blocker_signature")) == BLOCKER_ID:
            return signature
    return {}


def branch_is_endpoint_route(branch: dict[str, Any]) -> bool:
    text = clean_text(branch).lower()
    return any(marker in text for marker in ["endpoint", "hairpin", "wilson", "collar", "schur", "feshbach"])


def artifact_or_stop_hint_for_branch(branch: dict[str, Any]) -> dict[str, Any]:
    if clean_text(branch.get("target_id")) != YM_TARGET_ID:
        return {}
    signature = endpoint_signature_from_report()
    repetition_count = int(signature.get("repetition_count", 0) or 0)
    if repetition_count < 3 or not branch_is_endpoint_route(branch):
        return {}
    branch_id = clean_text(branch.get("branch_id"))
    branch_ids = {clean_text(item) for item in signature.get("branch_ids", []) if clean_text(item)}
    if branch_ids and branch_id not in branch_ids and not branch_is_endpoint_route(branch):
        return {}
    return {
        "target_id": YM_TARGET_ID,
        "blocker_signature": BLOCKER_ID,
        "blocker_kind": signature.get("blocker_kind", "artifact-blocked"),
        "repetition_count": repetition_count,
        "required_artifact": signature.get("missing_artifacts") or REQUIRED_ENDPOINT_ARTIFACTS,
        "allowed_next_modes": ALLOWED_NEXT_MODES,
        "forbidden_next_modes": FORBIDDEN_AFTER_REPETITION,
        "recommended_move": "artifact_sprint_required",
        "control_decision": "artifact_sprint_required",
        "broad_api_reasoning_allowed": False,
        "reason": (
            "The Route A endpoint branch has repeated the same endpoint source table and T_tail debt at least "
            "three times. The next packet must attach the artifact, a falsifier, a demotion packet, or quarantine."
        ),
        "blocker_report": rel(BLOCKER_REPORT),
        "endpoint_contract": rel(ENDPOINT_CONTRACT_JSON),
        "endpoint_pilot": rel(ENDPOINT_PILOT_JSON),
        "demotion_packet": rel(DEMOTION_PACKET_JSON),
    }


def artifact_or_stop_preflight(decisions: list[dict[str, Any]], target_id: str) -> dict[str, Any]:
    if clean_text(target_id) != YM_TARGET_ID:
        return {
            "target_id": clean_text(target_id),
            "enabled": False,
            "broad_api_reasoning_allowed": True,
            "branch_controls": [],
            "preflight_decision": "target_not_gated",
        }
    controls = [
        decision.get("artifact_or_stop")
        for decision in decisions
        if isinstance(decision.get("artifact_or_stop"), dict) and decision.get("artifact_or_stop")
    ]
    all_blocked = bool(decisions) and len(controls) == len(decisions)
    return {
        "target_id": YM_TARGET_ID,
        "enabled": True,
        "threshold": 3,
        "branch_controls": controls,
        "selected_branch_count": len(decisions),
        "artifact_blocked_branch_count": len(controls),
        "all_selected_branches_artifact_blocked": all_blocked,
        "broad_api_reasoning_allowed": not all_blocked,
        "preflight_decision": "block_broad_api_marathon" if all_blocked else "allow_with_branch_controls",
        "mode_rule": (
            "Any branch with a repeated named artifact debt may not receive broad_api_reasoning; if every selected "
            "YM branch is artifact-blocked, the marathon preflight fails until an artifact sprint, falsifier sprint, "
            "publication demotion, or quarantine packet is configured."
        ),
        "required_artifacts": sorted({item for control in controls for item in control.get("required_artifact", []) if clean_text(item)}),
        "blocker_report": rel(BLOCKER_REPORT) if BLOCKER_REPORT.exists() else "",
        "validator": "agentic/scripts/validate_artifact_or_stop_control.py",
    }


def evaluate_artifact_or_stop_packet(packet: dict[str, Any]) -> dict[str, Any]:
    target_id = clean_text(packet.get("target_id"))
    if target_id and target_id != YM_TARGET_ID:
        return {
            "valid": True,
            "verdict": "target_not_gated",
            "reason": "Artifact-or-stop control is scoped to the Yang-Mills target.",
        }
    blocker = clean_text(packet.get("blocker_signature")) or BLOCKER_ID
    repetition_count = int(packet.get("repetition_count", 0) or 0)
    requested_mode = clean_text(packet.get("requested_next_mode") or packet.get("next_mode") or packet.get("control_decision"))
    attached = {
        clean_text(item)
        for item in packet.get("attached_artifacts", [])
        if clean_text(item)
    }
    if blocker == BLOCKER_ID and repetition_count >= 3:
        if requested_mode in FORBIDDEN_AFTER_REPETITION:
            return {
                "valid": False,
                "verdict": "reject_repeated_artifact_free_request",
                "reason": "The endpoint source table/T_tail blocker repeated past threshold; broad API reasoning is forbidden.",
            }
        if requested_mode not in ALLOWED_NEXT_MODES:
            return {
                "valid": False,
                "verdict": "reject_unknown_next_mode",
                "reason": f"Mode `{requested_mode}` is not allowed after an artifact-blocked repetition.",
            }
        decisive = attached.intersection(REQUIRED_ENDPOINT_ARTIFACTS)
        if requested_mode == "artifact_sprint" and "endpoint_source_table_contract" in attached:
            return {
                "valid": True,
                "verdict": "accept_artifact_sprint_contract",
                "reason": "The next cycle is bounded to the endpoint table contract; no proof promotion is granted.",
            }
        if requested_mode == "artifact_sprint" and decisive:
            return {
                "valid": True,
                "verdict": "accept_artifact_sprint",
                "reason": "The packet attaches a named endpoint artifact and remains bounded to artifact production.",
            }
        if requested_mode == "falsifier_sprint" and decisive:
            return {
                "valid": True,
                "verdict": "accept_finite_falsifier",
                "reason": "The packet attaches a finite falsifier or endpoint data that can demote the route.",
            }
        if requested_mode in {"publication_demotion", "quarantine"} and (
            "endpoint_route_demotion_packet" in attached or "quarantine_packet" in attached
        ):
            return {
                "valid": True,
                "verdict": "accept_quarantine_or_demotion",
                "reason": "The branch is stopped or demoted instead of recursing into another completion cycle.",
            }
        if requested_mode == "conceptual_exploration_after_release" and (
            "endpoint_route_demotion_packet" in attached or "quarantine_packet" in attached
        ):
            return {
                "valid": True,
                "verdict": "accept_release_to_conceptual_exploration",
                "reason": "Conceptual exploration resumes only after the artifact-blocked route is released or quarantined.",
            }
        return {
            "valid": False,
            "verdict": "reject_missing_decisive_artifact",
            "reason": "The repeated endpoint blocker requires a table, falsifier, demotion packet, or quarantine packet.",
        }
    return {
        "valid": True,
        "verdict": "reasoning_allowed",
        "reason": "The blocker has not crossed the artifact-or-stop repetition threshold.",
    }


def validate_cycle_artifact_or_stop(cycle: dict[str, Any], *, future_threshold_cycle: int = 352) -> list[str]:
    target_id = clean_text(cycle.get("target_id"))
    if target_id != YM_TARGET_ID:
        return []
    try:
        cycle_number = int(clean_text(cycle.get("cycle_id")).split("-")[-1])
    except ValueError:
        cycle_number = int(cycle.get("cycle_index", 0) or 0)
    control = cycle.get("artifact_or_stop_control")
    if cycle_number >= future_threshold_cycle and not isinstance(control, dict):
        return ["future YM cycles must persist artifact_or_stop_control"]
    if not isinstance(control, dict):
        return []
    errors: list[str] = []
    for field in [
        "enabled",
        "branch_controls",
        "preflight_decision",
        "broad_api_reasoning_allowed",
        "mode_rule",
    ]:
        if field not in control:
            errors.append(f"artifact_or_stop_control missing {field}")
    for branch_control in control.get("branch_controls", []):
        if not isinstance(branch_control, dict):
            errors.append("artifact_or_stop_control.branch_controls entries must be objects")
            continue
        for field in ["blocker_signature", "repetition_count", "required_artifact", "control_decision"]:
            if not branch_control.get(field):
                errors.append(f"artifact_or_stop branch control missing {field}")
        if branch_control.get("control_decision") == "artifact_sprint_required" and branch_control.get("broad_api_reasoning_allowed") is not False:
            errors.append("artifact_sprint_required branches must block broad_api_reasoning")
    return errors
