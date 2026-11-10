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
"""Shared physical-relevance and impact helpers for discovery marathons."""

from __future__ import annotations

from typing import Any

from agentic_common import clean_text, stable_id


YM_TARGET_ID = "yang-mills-existence-and-mass-gap-target"

PHYSICAL_IMPACT_DIMS = [
    "physical_carrier_integrity",
    "same_theory_physical_transfer",
    "continuum_and_scale_relevance",
    "spectral_gap_interface",
    "nontriviality_and_observable_content",
    "field_understanding_impact",
    "unification_power",
    "route_decision_power",
]

PHYSICAL_RELEVANCE_DECISIONS = {
    "physically_relevant_candidate",
    "math_support_only_pending_physical_handoff",
    "incremental_math_drift_risk",
    "quarantine_proxy_or_artifact",
}

PHYSICS_PUBLICATION_INVESTMENT_DECISIONS = {
    "invest_high_physics_reward",
    "reframe_before_investment",
    "do_not_invest_support_only",
    "quarantine_low_physics_reward",
}

PHYSICAL_MARKERS = [
    "gauge-invariant",
    "gauge invariant",
    "wilson",
    "schwinger",
    "os hilbert",
    "reflection positivity",
    "os positivity",
    "observable",
    "hamiltonian",
    "spectral",
    "mass gap",
    "vacuum",
    "yang-mills",
]

TARGET_GATE_MARKERS = [
    ("same_theory_continuum_construction", ["same-theory", "same theory", "continuum", "cutoff", "regulator"]),
    ("os_wightman_reconstruction", ["os hilbert", "os positivity", "reflection positivity", "wightman", "reconstruction"]),
    ("gauge_invariant_observable_algebra", ["gauge-invariant", "gauge invariant", "wilson", "observable algebra", "schwinger"]),
    ("nontriviality_of_the_field", ["nontrivial", "connected cumulant", "non-gaussian", "vacuum-orthogonal", "cumulant"]),
    ("positive_spectral_mass_gap", ["spectral", "hamiltonian", "mass gap", "p_perp", "vacuum"]),
]


def first_lemma(output: dict[str, Any]) -> dict[str, Any]:
    lemmas = output.get("candidate_lemmas", [])
    return lemmas[0] if lemmas and isinstance(lemmas[0], dict) else {}


def first_matching_text(items: list[str], *markers: str) -> str:
    for item in items:
        text = clean_text(item)
        lowered = text.lower()
        if any(marker in lowered for marker in markers):
            return text
    return ""


def contains_any(text: str, markers: list[str]) -> bool:
    return any(marker in text for marker in markers)


def infer_physical_carrier(output: dict[str, Any]) -> str:
    text = clean_text(output).lower()
    if "wilson" in text:
        return "gauge-invariant Wilson observable family"
    if "schwinger" in text:
        return "continuum Schwinger-function family"
    if "os hilbert" in text or "hamiltonian" in text or "spectral" in text:
        return "OS Hilbert-space spectral object"
    if "observable" in text:
        return "gauge-invariant observable algebra"
    if "connected cumulant" in text or "non-gaussian" in text:
        return "nontrivial connected-cumulant witness"
    return ""


def target_commitments_touched(output: dict[str, Any]) -> list[str]:
    text = clean_text(output).lower()
    commitments = [name for name, markers in TARGET_GATE_MARKERS if contains_any(text, markers)]
    return commitments or ["physical_target_commitment_not_yet_identified"]


def score_item(score: int, evidence: str, missing: str) -> dict[str, Any]:
    return {
        "score": max(0, min(5, score)),
        "evidence": evidence,
        "missing_evidence": missing,
        "demotion_trigger": "Demote if the next result remains a local lemma with no named physical carrier, target gate, unification gain, or field-facing consequence.",
    }


def general_impact_vector(output: dict[str, Any], physical_carrier: str, commitments: list[str]) -> dict[str, Any]:
    text = clean_text(output).lower()
    next_experiment = clean_text(output.get("next_experiment")).lower()
    has_falsifier = bool(output.get("falsifiers"))
    has_explicit_impact_claim = contains_any(
        text,
        ["physical carrier", "physical relevance", "general impact", "field-facing", "mathematical physicist", "constructive-qft"],
    )
    has_unification_language = contains_any(
        text,
        [
            "unification",
            "unifies",
            "unifying",
            "unified",
            "combines",
            "compresses",
            "single mechanism",
            "common carrier",
            "same-theory connected",
            "one witness",
            "one inequality",
            "one ledger",
        ],
    )
    unifies_distinct_constraints = sum(
        int(contains_any(text, markers))
        for markers in [
            ["positivity", "os positivity", "reflection positivity"],
            ["nontrivial", "connected cumulant", "non-gaussian"],
            ["spectral", "mass gap", "hamiltonian", "vacuum"],
            ["continuum", "cutoff", "uniform", "regulator", "volume"],
            ["wilson", "schwinger", "observable", "gauge-invariant", "gauge invariant"],
            ["schur", "feshbach", "endpoint", "tail", "ope"],
        ]
    )
    has_route_decision = contains_any(
        clean_text(output.get("control_decision", {})).lower() + " " + next_experiment,
        ["prove", "compute", "bound", "falsify", "quarantine", "backtrack", "pivot", "handoff", "validate", "certify"],
    )
    vector = {
        "physical_carrier_integrity": score_item(
            4 if physical_carrier else 1,
            physical_carrier or "No physical carrier was identified by deterministic markers.",
            "Name the gauge-invariant observable, Schwinger family, OS Hilbert object, Hamiltonian/spectral object, or nontriviality witness.",
        ),
        "same_theory_physical_transfer": score_item(
            4 if contains_any(text, ["same-theory", "same theory"]) else 2,
            "Same-theory markers are present." if contains_any(text, ["same-theory", "same theory"]) else "Same-theory transfer remains implicit.",
            "State the source theory, target theory, topology/regulator, and transfer map that preserve the physical object.",
        ),
        "continuum_and_scale_relevance": score_item(
            4 if contains_any(text, ["continuum", "cutoff", "regulator", "rg", "volume", "scale", "uniform"]) else 1,
            "Continuum, regulator, RG, volume, or uniformity language is present." if contains_any(text, ["continuum", "cutoff", "regulator", "rg", "volume", "scale", "uniform"]) else "No continuum or scale gate was identified.",
            "Explain how the local result survives or fails under cutoff removal, volume limit, or RG/regulator comparison.",
        ),
        "spectral_gap_interface": score_item(
            4 if contains_any(text, ["spectral", "hamiltonian", "mass gap", "os hilbert", "p_perp", "vacuum"]) else 1,
            "Spectral/Hamiltonian/OS-Hilbert vocabulary is present." if contains_any(text, ["spectral", "hamiltonian", "mass gap", "os hilbert", "p_perp", "vacuum"]) else "No spectral-gap interface was identified.",
            "Name how the object would enter the OS Hilbert space, vacuum-orthogonal sector, Hamiltonian, or spectral measure.",
        ),
        "nontriviality_and_observable_content": score_item(
            4 if contains_any(text, ["nontrivial", "connected cumulant", "non-gaussian", "observable density", "vacuum-orthogonal"]) else 2,
            "Observable-content or nontriviality markers are present." if contains_any(text, ["nontrivial", "connected cumulant", "non-gaussian", "observable density", "vacuum-orthogonal"]) else "Nontrivial physical content is not yet separated from formal consistency.",
            "State the witness that prevents the construction from collapsing to a Gaussian, trivial, or empty observable theory.",
        ),
        "field_understanding_impact": score_item(
            4 if has_explicit_impact_claim else 2,
            "The branch explicitly names physical relevance or general field-facing impact." if has_explicit_impact_claim else "Field-facing impact remains underexplained.",
            "Say what a mathematical physicist would understand differently if the branch succeeds, relative to OS, Wilson-loop, constructive-QFT, or RG literature.",
        ),
        "unification_power": score_item(
            4 if has_unification_language and unifies_distinct_constraints >= 3 else 2 if has_unification_language or unifies_distinct_constraints >= 2 else 1,
            (
                "The branch names a unifying mechanism that connects multiple target constraints or carriers."
                if has_unification_language and unifies_distinct_constraints >= 3
                else "Unification is only implicit or local; the branch has not shown that one mechanism explains several target pressures."
            ),
            "State which formerly separate constraints, carriers, estimates, or routes are unified, and what new hypothesis or proof obligation this compression makes visible.",
        ),
        "route_decision_power": score_item(
            4 if has_route_decision and has_falsifier else 2,
            "The branch has a next action and falsifiers that can change route priority." if has_route_decision and has_falsifier else "The route decision is not yet falsifier-backed.",
            "State a physical-relevance test whose pass/fail result promotes, demotes, pivots, or quarantines the branch.",
        ),
    }
    if commitments == ["physical_target_commitment_not_yet_identified"]:
        vector["physical_carrier_integrity"]["score"] = min(1, vector["physical_carrier_integrity"]["score"])
    return vector


def relevance_decision(vector: dict[str, Any], physical_carrier: str, commitments: list[str], output: dict[str, Any]) -> str:
    scores = {key: int(value.get("score", 0)) for key, value in vector.items()}
    text = clean_text(output).lower()
    has_explicit_impact_claim = contains_any(
        text,
        ["physical carrier", "physical relevance", "general impact", "field-facing", "mathematical physicist", "constructive-qft"],
    )
    if not physical_carrier or commitments == ["physical_target_commitment_not_yet_identified"]:
        return "incremental_math_drift_risk"
    if not has_explicit_impact_claim:
        return "math_support_only_pending_physical_handoff"
    if scores["same_theory_physical_transfer"] < 3 or scores["continuum_and_scale_relevance"] < 3:
        return "math_support_only_pending_physical_handoff"
    if scores["physical_carrier_integrity"] >= 3 and scores["route_decision_power"] >= 3:
        return "physically_relevant_candidate"
    if "quarantine" in clean_text(output.get("control_decision", {})).lower():
        return "quarantine_proxy_or_artifact"
    return "math_support_only_pending_physical_handoff"


def build_major_publication_gate(
    output: dict[str, Any],
    vector: dict[str, Any],
    physical_carrier: str,
    commitments: list[str],
    relevance: str,
) -> dict[str, Any]:
    """Decide whether the branch is worth future YM investment."""
    scores = {key: int(value.get("score", 0)) for key, value in vector.items()}
    text = clean_text(output).lower()
    has_publication_language = contains_any(
        text,
        [
            "major publication",
            "publication weight",
            "publishable",
            "field-facing impact",
            "mathematical physicist",
            "constructive-qft",
            "changes understanding",
            "understand differently",
            "unifies",
            "explains",
            "conceptual reward",
            "conceptual payoff",
        ],
    )
    has_target_commitment = commitments != ["physical_target_commitment_not_yet_identified"]
    has_high_reward_vector = (
        scores.get("physical_carrier_integrity", 0) >= 3
        and scores.get("field_understanding_impact", 0) >= 3
        and scores.get("unification_power", 0) >= 3
        and scores.get("route_decision_power", 0) >= 3
        and max(
            scores.get("same_theory_physical_transfer", 0),
            scores.get("continuum_and_scale_relevance", 0),
            scores.get("spectral_gap_interface", 0),
            scores.get("nontriviality_and_observable_content", 0),
        )
        >= 3
    )
    if not physical_carrier or not has_target_commitment:
        investment = "quarantine_low_physics_reward"
        reward = "low"
        reason = "The branch lacks a concrete Yang-Mills physical carrier or target gate, so it should not receive another research cycle."
    elif relevance != "physically_relevant_candidate":
        investment = "do_not_invest_support_only"
        reward = "support_only"
        reason = "The branch is mathematically usable only as support material until it supplies a physical handoff."
    elif not has_publication_language or not has_high_reward_vector:
        investment = "reframe_before_investment"
        reward = "uncertain"
        reason = "The branch has some physical markers but has not yet stated a major publication payoff, unification gain, or route-changing physics consequence."
    else:
        investment = "invest_high_physics_reward"
        reward = "high"
        reason = "The branch names a physical carrier, target gate, unification gain, field-facing understanding change, and falsifier-backed route decision."
    return {
        "investment_decision": investment,
        "major_publication_potential": investment == "invest_high_physics_reward",
        "physics_conceptual_reward": reward,
        "publication_claim_candidate": (
            "A route-changing Yang-Mills subgoal contribution is possible only if the next artifact changes the status of a named "
            "physical carrier at a continuum, OS/Wightman, nontriviality, observable-density, or spectral-gap gate."
        ),
        "must_change_understanding": (
            "State what a constructive-QFT or mathematical-physics reader would understand differently about the YM gap route, "
            "including which standard obstruction, bridge, or physical carrier has moved."
        ),
        "unification_power_requirement": (
            "Name which previously separate physics or proof pressures are unified by one mechanism, carrier, estimate, or representation; "
            "without this compression, the result is support-only even if locally correct."
        ),
        "investment_rationale": reason,
        "non_investment_trigger": (
            "If the next step is only a finite lemma, local estimate, endpoint calculation, or symbolic identity with no major "
            "publication path, demote, reframe, pivot, or quarantine instead of continuing the branch."
        ),
        "required_next_artifact": (
            clean_text(output.get("next_experiment"))
            or "Produce a physics-load-bearing artifact or a demotion/quarantine packet before another YM marathon cycle."
        ),
        "validation_rule": (
            "Future YM discovery cycles may invest only in invest_high_physics_reward branches; every other decision must "
            "demote, reframe, pivot, stop, or quarantine the pathway."
        ),
    }


def build_physical_relevance_impact_packet(output: dict[str, Any], branch: dict[str, Any], cycle_index: int) -> dict[str, Any]:
    target_id = clean_text(branch.get("target_id"))
    lemma = first_lemma(output)
    definitions = [clean_text(item) for item in lemma.get("definitions", [])]
    source_object = first_matching_text(definitions, "source object") or clean_text(branch.get("controlled_interface"))
    target_object = first_matching_text(definitions, "target object") or clean_text(lemma.get("statement"))
    carrier = infer_physical_carrier(output)
    commitments = target_commitments_touched(output)
    vector = general_impact_vector(output, carrier, commitments)
    decision = relevance_decision(vector, carrier, commitments, output)
    publication_gate = build_major_publication_gate(output, vector, carrier, commitments, decision)
    return {
        "version": 1,
        "packet_id": stable_id("physical-impact", target_id, branch.get("branch_id"), cycle_index, lemma.get("lemma_id")),
        "target_id": target_id,
        "branch_id": clean_text(branch.get("branch_id")),
        "cycle_id": f"cycle-{cycle_index:04d}",
        "source_object": source_object,
        "target_object": target_object,
        "physical_carrier": carrier or "missing physical carrier",
        "target_commitments_touched": commitments,
        "general_impact_vector": vector,
        "relevance_decision": decision,
        "major_publication_gate": publication_gate,
        "general_impact_claim": (
            "Support-only until the branch shows how its mathematical object changes a gauge-invariant observable, "
            "continuum/OS reconstruction gate, nontriviality witness, or spectral-gap interface."
            if decision != "physically_relevant_candidate"
            else "The branch names a physical carrier and a target gate whose pass/fail test can change the YM route."
        ),
        "incremental_math_drift_risk": (
            "High: the packet lacks a physical carrier or target commitment."
            if decision == "incremental_math_drift_risk"
            else "Controlled: local mathematics is kept support-only until the physical handoff is validated."
        ),
        "next_physical_relevance_test": (
            clean_text(output.get("next_experiment"))
            or "Run physical-relevance-impact-auditor before promoting the mathematical subgoal."
        ),
        "evidence": [
            "candidate lemma definitions",
            "candidate lemma assumptions",
            "attempted derivation blocking gap",
            "branch falsifiers",
            "control decision",
            "next experiment",
        ],
        "generated_by_skills": [
            "physical-relevance-impact-auditor",
            "main-problem-alignment-auditor",
            "paper-contribution-readiness-judge",
        ],
        "validation_handoff": "agentic/scripts/validate_discovery_marathon_cycle.py",
    }


def attach_physical_relevance_impact_packet(output: dict[str, Any], branch: dict[str, Any], cycle_index: int) -> dict[str, Any]:
    if clean_text(branch.get("target_id")) == YM_TARGET_ID:
        output["physical_relevance_impact"] = build_physical_relevance_impact_packet(output, branch, cycle_index)
    return output


def discover_physical_relevance_packets(value: Any) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    if isinstance(value, dict):
        direct = value.get("physical_relevance_impact")
        if isinstance(direct, dict):
            packets.append(direct)
        if "packet_id" in value and "general_impact_vector" in value and "relevance_decision" in value:
            packets.append(value)
        for nested_value in value.values():
            if isinstance(nested_value, (dict, list)):
                packets.extend(discover_physical_relevance_packets(nested_value))
    elif isinstance(value, list):
        for item in value:
            packets.extend(discover_physical_relevance_packets(item))
    seen: set[str] = set()
    unique = []
    for packet in packets:
        packet_id = clean_text(packet.get("packet_id"))
        if packet_id and packet_id not in seen:
            seen.add(packet_id)
            unique.append(packet)
    return unique
