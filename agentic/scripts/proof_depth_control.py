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
"""Shared proof-depth control helpers for discovery marathons and reports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, rel, slugify, stable_id, utc_now, write_json


QUALITY_DIMS = [
    "conceptual_depth",
    "explanatory_power",
    "unification_power",
    "mechanism_specificity",
    "compression",
    "generativity",
    "transfer_reach",
    "falsifiability",
    "boundary_sharpness",
    "literature_displacement",
]

PROMOTION_DECISIONS = {"promote", "lock_in_candidate", "proof_delivery"}
TRANSFER_TERMS = ["transfer", "bridge", "normalization", "carrier", "reduction", "same-theory", "same theory"]
DEFINITIONAL_TERMS = [
    "by definition",
    "definition-built",
    "defined as the image",
    "defined to be the image",
    "target predicate is defined",
    "follows from the definition",
    "unfolding the definition",
]
PRIOR_ART_MARKERS = [
    "prior art",
    "literature",
    "known result",
    "standard",
    "classical",
    "unlike",
    "differs from",
    "extends",
    "sharpens",
    "not covered",
    "novel",
    "new contribution",
]


def first_matching_text(items: list[str], *markers: str) -> str:
    for item in items:
        text = clean_text(item)
        lowered = text.lower()
        if any(marker in lowered for marker in markers):
            return text
    return ""


def first_lemma(output: dict[str, Any]) -> dict[str, Any]:
    lemmas = output.get("candidate_lemmas", [])
    return lemmas[0] if lemmas and isinstance(lemmas[0], dict) else {}


def text_has_any(value: Any, markers: list[str]) -> bool:
    lowered = clean_text(value).lower()
    return any(marker in lowered for marker in markers)


def infer_prior_art_delta(output: dict[str, Any]) -> str:
    candidates: list[str] = []
    for item in output.get("dependency_updates", []) if isinstance(output.get("dependency_updates"), list) else []:
        candidates.append(clean_text(item))
    candidates.extend(
        [
            clean_text(output.get("mathematical_learning")),
            clean_text(output.get("next_experiment")),
            clean_text(output.get("attempted_derivation", {}).get("blocking_gap") if isinstance(output.get("attempted_derivation"), dict) else ""),
        ]
    )
    for lemma in output.get("candidate_lemmas", []) if isinstance(output.get("candidate_lemmas"), list) else []:
        if not isinstance(lemma, dict):
            continue
        candidates.extend(
            [
                clean_text(lemma.get("statement")),
                clean_text(lemma.get("proof_role")),
                clean_text(lemma.get("failure_test")),
            ]
        )
    for candidate in candidates:
        lowered = candidate.lower()
        if any(marker in lowered for marker in PRIOR_ART_MARKERS):
            return f"Branch states a prior-art delta requiring citation check: {candidate[:280]}"
    return "pending prior-art comparison; cannot claim literature displacement without it"


def infer_pressure_kind(output: dict[str, Any], target_id: str) -> str:
    text = clean_text(output).lower()
    if text_has_any(text, DEFINITIONAL_TERMS):
        return "definitional_collapse"
    if any(term in text for term in ["normalization", "same-theory", "same theory"]):
        return "hidden_normalization"
    if "transfer" in text or "bridge" in text or "reduction" in text:
        return "transfer_failure"
    if any(term in text for term in ["carrier", "construct", "realize", "realisation", "realization"]):
        return "missing_construction"
    if target_id == "p-vs-np-target" and any(term in text for term in ["barrier", "natural", "relativ", "algebr"]):
        return "barrier_mismatch"
    return "weak_invariant"


def infer_hard_gate(branch: dict[str, Any], output: dict[str, Any]) -> str:
    text = clean_text({"branch": branch, "output": output}).lower()
    target_id = clean_text(branch.get("target_id"))
    if target_id == "yang-mills-existence-and-mass-gap-target":
        if "collar" in text or "hairpin" in text:
            return "geometric_collar_realization"
        if "normalization" in text or "same-theory" in text or "same theory" in text:
            return "same_theory_normalization"
        if "coefficient" in text or "kappa" in text or "endpoint" in text:
            return "geometric_coefficient_or_endpoint_estimate"
        return "same_regulator_reflection_positivity_gate"
    if target_id == "p-vs-np-target":
        if "uniform" in text or "advice" in text:
            return "all_exponent_uniformity_and_advice_gate"
        if "barrier" in text or "natural" in text or "relativ" in text or "algebr" in text:
            return "barrier_specificity_gate"
        if "carrier" in text or "mcsp" in text or "mktp" in text:
            return "carrier_transparency_gate"
        if "reduction" in text or "transfer" in text:
            return "reduction_preservation_gate"
        return "proof_complexity_transfer_gate"
    return clean_text(branch.get("controlled_interface")) or "target_preserving_bridge_gate"


def concept_quality_vector(output: dict[str, Any], hard_gate: str, transfer_verdict: str) -> dict[str, Any]:
    text = clean_text(output).lower()
    has_falsifier = bool(output.get("falsifiers"))
    has_mechanism = any(term in text for term in ["because", "mechanism", "invariant", "preserve", "obstruction"])
    transfer_cap = transfer_verdict in {"definitional_restatement", "notation_translation", "conservative_unpacking", "blocked"}
    vector: dict[str, Any] = {}
    for dim in QUALITY_DIMS:
        score = 3
        evidence = f"Hard gate `{hard_gate}` is explicitly attached to the branch output."
        missing = "Needs reviewer-confirmed proof or literature comparison before publication promotion."
        if dim == "conceptual_depth":
            score = 4 if has_mechanism else 3
            evidence = "Cycle names the hard gate and attempts to explain the route pressure."
        elif dim == "explanatory_power":
            score = 4 if has_mechanism else 2
            evidence = "Explanatory value depends on the named mechanism and blocking gap."
        elif dim == "unification_power":
            score = 2
            evidence = "Unification is tentative unless two distinct regimes or failures are explicitly connected."
        elif dim == "mechanism_specificity":
            score = 4 if has_mechanism else 2
            evidence = "Mechanism specificity is measured by named mediator, invariant, and defeater."
        elif dim == "compression":
            score = 2
            evidence = "Compression requires a theorem or schema that reduces local cases."
        elif dim == "generativity":
            score = 4 if clean_text(output.get("next_experiment")) else 2
            evidence = "The next experiment creates follow-up proof obligations or falsifiers."
        elif dim == "transfer_reach":
            score = 1 if transfer_cap else 3
            evidence = f"Transfer reach is governed by transfer-substance verdict `{transfer_verdict}`."
        elif dim == "falsifiability":
            score = 4 if has_falsifier else 2
            evidence = "Falsifiability depends on concrete falsifiers, edge cases, or failure regimes."
        elif dim == "boundary_sharpness":
            score = 3 if "not" in text or "only" in text or "quarantine" in text else 2
            evidence = "Boundary sharpness depends on explicit non-claims and demotion triggers."
        elif dim == "literature_displacement":
            score = 1
            evidence = "Literature displacement remains low until prior-art delta is supplied."
        vector[dim] = {
            "score": score,
            "evidence": evidence,
            "missing_evidence": missing,
            "scope": "target-scoped discovery control, not standalone proof authority",
            "demotion_trigger": "Demote if the cycle does not change understanding, hard-gate status, or future routing.",
        }
    return vector


def transfer_substance_audit(output: dict[str, Any], source_object: str, target_object: str) -> dict[str, Any]:
    text = clean_text(output).lower()
    transfer_shaped = text_has_any(text, TRANSFER_TERMS)
    definition_built = text_has_any(text, DEFINITIONAL_TERMS)
    has_falsifier = bool(output.get("falsifiers"))
    if not transfer_shaped:
        verdict = "not_transfer"
    elif definition_built:
        verdict = "definitional_restatement"
    elif source_object and target_object and has_falsifier:
        verdict = "substantive_transfer"
    else:
        verdict = "blocked"
    return {
        "definition_expansion_test": "fails if the conclusion follows only by unfolding bridge definitions" if definition_built else "passes unless later audit shows the conclusion is definition-built",
        "independent_source_object_test": source_object or "missing independent source object",
        "independent_target_property_test": target_object or "missing independent target property",
        "nontrivial_hypothesis_test": "uses branch assumptions and validity conditions" if first_lemma(output).get("assumptions") else "missing explicit nontrivial hypothesis",
        "source_variation_test": "requires an admissible source variation or records the absence as a limitation",
        "stress_case_test": "uses falsifier or boundary regime when available" if has_falsifier else "missing stress case",
        "failure_case_test": clean_text(output.get("falsifiers", [""])[0]) if has_falsifier else "missing failure case",
        "consequence_delta": clean_text(output.get("mathematical_learning")) or "missing consequence delta",
        "prior_art_delta": infer_prior_art_delta(output),
        "verdict": verdict,
        "repair_certificate": "supply independent target semantics, stress/failure case, and prior-art delta" if verdict != "substantive_transfer" else "preservation work is visible; still requires proof-quality review",
        "evidence": ["branch output", "candidate lemma definitions", "falsifiers"],
        "validation_handoff": "agentic/scripts/validate_proof_depth_control.py",
    }


def same_domain_transfer_audit(output: dict[str, Any], source_object: str, target_object: str, target_id: str) -> dict[str, Any]:
    text = clean_text(output).lower()
    same_domain_marker = "same-theory" in text or "same theory" in text or "target-preserving" in text or "same-framework" in text
    return {
        "source_object": source_object,
        "target_object": target_object,
        "source_domain": "Yang-Mills regulated Wilson/OS setting" if "yang-mills" in target_id else "target-local source domain",
        "target_domain": "same target theorem regime" if same_domain_marker else "target domain requires explicit certification",
        "preserved_structure": "same-domain marker present" if same_domain_marker else "preservation not yet certified",
        "changed_structure": "no silent change detected by deterministic markers" if same_domain_marker else "possible representation, regulator, model, or quantifier drift",
        "transfer_theorem": "branch-level transfer or bridge claim" if text_has_any(text, TRANSFER_TERMS) else "not a transfer theorem",
        "missing_certificate": "" if same_domain_marker else "same-domain transfer certificate",
        "same_domain_status": "certified_by_branch_markers" if same_domain_marker else "certificate_needed",
        "stress_or_failure_case": clean_text(output.get("falsifiers", [""])[-1]) if output.get("falsifiers") else "missing stress or failure case",
        "evidence": ["branch output", "definitions", "assumptions"],
        "validation_handoff": "proof-same-domain-transfer-certifier",
    }


def release_decision_from(output: dict[str, Any], transfer_audit: dict[str, Any]) -> tuple[str, str]:
    decision = clean_text(output.get("control_decision", {}).get("decision")).lower()
    transfer_verdict = clean_text(transfer_audit.get("verdict"))
    if transfer_verdict in {"definitional_restatement", "notation_translation", "conservative_unpacking", "blocked"}:
        return "support_only", "Principal transfer substance is not yet enough for promotion."
    if transfer_verdict == "substantive_transfer":
        prior_art_delta = clean_text(transfer_audit.get("prior_art_delta")).lower()
        if prior_art_delta.startswith("missing") or prior_art_delta.startswith("pending"):
            return "support_only", "Substantive transfer remains support-only until the branch states a prior-art delta."
    if any(marker in decision for marker in ["promote", "proof_delivery", "proof delivery", "lock_in", "lock-in"]):
        return "promote", "Branch decision and proof-depth packet support promotion subject to proof-quality review."
    if "persist" in decision:
        return "support_only", "Persist/adapt keeps the branch live but is not proof-depth promotion."
    if "quarantine" in decision:
        return "quarantine", "Branch control decision quarantines the output."
    if "pivot" in decision or "backtrack" in decision:
        return "pivot", "Branch control decision sends the route to a pivot or backtrack."
    return "support_only", "No hard-gate promotion decision was available."


def build_proof_depth_packet(output: dict[str, Any], branch: dict[str, Any], cycle_index: int) -> dict[str, Any]:
    target_id = clean_text(branch.get("target_id"))
    lemma = first_lemma(output)
    definitions = [clean_text(item) for item in lemma.get("definitions", [])]
    source_object = first_matching_text(definitions, "source object") or clean_text(branch.get("controlled_interface"))
    target_object = first_matching_text(definitions, "target object") or clean_text(lemma.get("statement"))
    hard_gate = infer_hard_gate(branch, output)
    transfer_audit = transfer_substance_audit(output, source_object, target_object)
    quality = concept_quality_vector(output, hard_gate, clean_text(transfer_audit.get("verdict")))
    release_decision, demotion_trigger = release_decision_from(output, transfer_audit)
    event_id = stable_id("proof-learning", target_id, branch.get("branch_id"), cycle_index, output.get("mathematical_learning"))
    return {
        "version": 1,
        "packet_id": stable_id("proof-depth", target_id, branch.get("branch_id"), cycle_index, lemma.get("lemma_id")),
        "target_id": target_id,
        "branch_id": clean_text(branch.get("branch_id")),
        "cycle_id": f"cycle-{cycle_index:04d}",
        "pressure_kind": infer_pressure_kind(output, target_id),
        "hard_gate": hard_gate,
        "proof_object": clean_text(lemma.get("statement")) or clean_text(output.get("branch_title")),
        "target_commitment": target_object,
        "proposed_move": clean_text(output.get("next_experiment")),
        "depth_delta": "hard_gate_moved" if release_decision in PROMOTION_DECISIONS else "support_only_or_demoted",
        "conceptual_quality_vector": quality,
        "transfer_substance_audit": transfer_audit,
        "same_domain_transfer_audit": same_domain_transfer_audit(output, source_object, target_object, target_id),
        "transfer_status": clean_text(transfer_audit.get("verdict")),
        "nontriviality_status": "load_bearing" if release_decision in PROMOTION_DECISIONS else "support_only",
        "declarative_learning_event": {
            "event_id": event_id,
            "target_id": target_id,
            "source_cycle_id": f"cycle-{cycle_index:04d}",
            "premises_used": lemma.get("assumptions", []),
            "attempted_inference": clean_text(lemma.get("proof_role")) or clean_text(output.get("next_experiment")),
            "observed_result": clean_text(output.get("mathematical_learning")),
            "learned_constraint": clean_text(output.get("attempted_derivation", {}).get("blocking_gap")) or demotion_trigger,
            "scope_condition": "valid only under the lemma definitions, assumptions, and target-specific hard gate",
            "invalidated_generalization": "do not promote definition-built transfer or hard-gate-free local work",
            "future_routing_effect": clean_text(output.get("next_experiment")) or "route to proof-depth release gate",
            "epistemic_status": "learned_rule" if release_decision in PROMOTION_DECISIONS else "branch_routing_rule",
            "evidence": ["branch output", "proof_depth_control packet"],
            "validation_handoff": "agentic/scripts/validate_proof_learning_ledger.py",
        },
        "demotion_trigger": demotion_trigger,
        "release_decision": release_decision,
        "evidence": [
            "candidate lemma definitions",
            "candidate lemma assumptions",
            "attempted derivation blocking gap",
            "branch falsifiers",
            "control decision",
        ],
        "validation_handoff": "agentic/scripts/validate_proof_depth_control.py",
    }


def attach_proof_depth_control_packet(output: dict[str, Any], branch: dict[str, Any], cycle_index: int) -> dict[str, Any]:
    output["proof_depth_control"] = build_proof_depth_packet(output, branch, cycle_index)
    return output


def discover_proof_depth_packets(value: Any) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    if isinstance(value, dict):
        direct = value.get("proof_depth_control")
        if isinstance(direct, dict):
            packets.append(direct)
        nested = value.get("proof_depth_packets")
        if isinstance(nested, list):
            packets.extend(item for item in nested if isinstance(item, dict))
        if "packet_id" in value and "release_decision" in value and "conceptual_quality_vector" in value:
            packets.append(value)
        for nested_value in value.values():
            if isinstance(nested_value, (dict, list)):
                packets.extend(discover_proof_depth_packets(nested_value))
    elif isinstance(value, list):
        for item in value:
            packets.extend(discover_proof_depth_packets(item))
    seen: set[str] = set()
    unique = []
    for packet in packets:
        packet_id = clean_text(packet.get("packet_id"))
        if packet_id and packet_id not in seen:
            seen.add(packet_id)
            unique.append(packet)
    return unique


def proof_report_dir(root_name: str, target_id: str) -> Path:
    return ROOT / "agentic" / "reports" / root_name / "targets" / slugify(target_id)


def write_target_report(root_name: str, target_id: str, report: dict[str, Any], markdown: str) -> tuple[Path, Path]:
    out_dir = proof_report_dir(root_name, target_id)
    json_path = out_dir / "latest.json"
    md_path = out_dir / "latest.md"
    write_json(json_path, report)
    md_path.write_text(markdown, encoding="utf-8")
    return json_path, md_path
