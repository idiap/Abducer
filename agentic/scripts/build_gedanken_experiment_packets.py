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
"""Build live-aware Gedanken experiment packets for follow-up discovery cycles."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, load_json_object, stable_id, utc_now, write_json
from discovery_marathon_common import load_cycles, load_run_state, run_dir


OUT = ROOT / "agentic/reports/gedanken_experiments/latest.json"
MD = ROOT / "agentic/reports/gedanken_experiments/latest.md"


def cycle_sources(cycles: list[dict[str, Any]], run_id: str) -> list[str]:
    recent = cycles[-6:]
    if not recent:
        return ["agentic/reports/discovery_marathon/latest.json"]
    return [
        f"agentic/runs/discovery_marathons/{run_id}/cycles/{cycle.get('cycle_id', 'unknown')}.json"
        for cycle in recent
    ]


def need_assessment(decision: str, met: list[str], missing: list[str], rejected: list[str], why: str) -> dict[str, Any]:
    return {
        "decision": decision,
        "criteria_met": met,
        "criteria_missing": missing,
        "rejected_alternatives": rejected,
        "why_not_direct_derivation_or_probe": why,
    }


def followup(packet_id: str, title: str, transfer_verdict: str, action: str, description: str, success: str, failure: str, skills: list[str]) -> dict[str, Any]:
    return {
        "action": action,
        "description": description,
        "success_criterion": success,
        "failure_or_demotion_criterion": failure,
        "required_skills": skills,
        "packet_id": packet_id,
        "situation_title": title,
        "transfer_verdict": transfer_verdict,
    }


def domain_from_text(text: str) -> str:
    lower = text.lower()
    if "determinant" in lower or "phase" in lower or "positivity" in lower or "reflection" in lower:
        return "reflection_positive_gram"
    if "spectral" in lower or "decay" in lower or "correlator" in lower or "measure" in lower:
        return "spectral_leakage"
    if "limit" in lower or "cutoff" in lower or "volume" in lower or "uniform" in lower:
        return "limit_switchboard"
    return "generic_mechanism"


def focus_for_text(text: str) -> str:
    lower = text.lower()
    if "boundary ope" in lower or "b_{ij}" in lower or "n_{ij}" in lower or "additive contact" in lower:
        return "boundary_ope_extraction"
    if "leading quotient kernel" in lower or "boundary quotient" in lower:
        return "boundary_ope_extraction"
    if "holonomy" in lower or "coboundary" in lower or "phase removal" in lower:
        return "quotient_holonomy"
    if "schur" in lower or "determinant" in lower or "pairwise" in lower:
        return "schur_preimage_determinant"
    if "spectral" in lower or "correlator" in lower:
        return "spectral_leakage"
    if "limit" in lower or "uniform" in lower or "cutoff" in lower:
        return "limit_switchboard"
    return "generic"


def reflection_focus_from_text(text: str) -> dict[str, str]:
    lower = text.lower()
    if "boundary ope" in lower or "b_{ij}" in lower or "n_{ij}" in lower or "additive contact" in lower or "leading quotient kernel" in lower or "boundary quotient" in lower:
        return {
            "focus_id": "boundary_ope_extraction",
            "title": "Boundary OPE extraction bench for reflected Wilson hairpins",
            "purpose": "Make visible exactly which boundary data must be computed before the finite quotient criterion can touch Yang-Mills.",
            "minimal_world": "Imagine three reflected Wilson hairpins with a shared reflection-plane footprint and separate the collar matrix N, multiplicative boundary anomaly B, and additive contact C.",
            "carrier": "A finite boundary OPE bookkeeping model N = B circ M + C, followed by diagonal normalization and Hadamard quotient Q = Nhat oslash Bhat.",
            "contrast": "Compare additive-contact failure against multiplicative boundary-anomaly failure after diagonal trace continuity.",
            "why": "It follows the previous cycles' progress: the linear algebra bridge is typed, so the live blocker is the analytic boundary OPE data B, N, and C for actual reflected Wilson hairpins.",
            "varied": "boundary OPE decomposition",
            "observation": "whether C vanishes and whether B yields a well-defined quotient Q on the realized finite family",
            "expected": "If additive contacts vanish, the obstruction moves to multiplicative quotient positivity; if they do not, the branch must backtrack to contact control.",
            "disconfirm": "If a same-theory estimate proves zero additive contact and quotient positivity for the tested finite family.",
            "task": "Derive or compute the leading boundary OPE for the simplest reflected Wilson hairpin triple and extract B, N, C, and Q.",
            "success": "The branch obtains typed boundary data that can feed the quotient determinant or holonomy test.",
            "failure": "If B, N, or C cannot be defined in the same observable algebra, quarantine the finite-matrix criterion as a proxy.",
        }
    if "holonomy" in lower or "coboundary" in lower or "phase removal" in lower:
        return {
            "focus_id": "quotient_holonomy",
            "title": "Quotient holonomy switch for reflected Wilson triples",
            "purpose": "Make visible whether a boundary quotient phase is a removable coboundary or a genuine finite-family obstruction.",
            "minimal_world": "Imagine a support graph of reflected Wilson triples with quotient phases theta_ij and ask whether every cycle holonomy vanishes before testing the real modulus quotient.",
            "carrier": "A normalized Hermitian quotient matrix Q on a finite support graph, with cycle holonomies H_C=sum theta_ij mod 2pi and real modulus matrix |Q| after possible diagonal rephasing.",
            "contrast": "Compare removable diagonal phase coboundaries against nonzero cycle holonomy that must be tested by principal minors.",
            "why": "It follows the latest branch progress: the finite matrix criterion is no longer merely pairwise positivity; the live issue is whether quotient phase can be gauged away before modulus positivity is checked.",
            "varied": "quotient cycle holonomy",
            "observation": "cycle holonomy and determinant of the corresponding principal quotient minor",
            "expected": "Zero holonomy permits a real-modulus quotient test, while nonzero holonomy localizes the first phase-sensitive determinant falsifier.",
            "disconfirm": "If all realized quotient phases are coboundaries and the real modulus quotient is positive on the same finite family.",
            "task": "Compute quotient phases on the smallest realized support graph, test the coboundary condition, then evaluate the corresponding principal determinant.",
            "success": "The calculation distinguishes removable phase from an actual holonomy obstruction and identifies the next same-theory premise.",
            "failure": "If phase is removable in all tested families, demote holonomy and shift to modulus quotient or boundary OPE estimates.",
        }
    return {
        "focus_id": "schur_preimage_determinant",
        "title": "Schur-preimage determinant falsifier for reflected Wilson triples",
        "purpose": "Make visible how pairwise damping can coexist with a negative finite-family determinant.",
        "minimal_world": "Imagine three gauge-invariant reflected probes whose pairwise overlaps remain positive while a normalized Schur quotient accumulates a determinant obstruction.",
        "carrier": "A finite Hermitian Gram matrix N(delta) with positive diagonal, pairwise positive minors, and a phase- or modulus-sensitive 3-by-3 quotient determinant.",
        "contrast": "Compare pairwise reflection positivity against full finite-family reflection positivity as the collar width delta tends to zero.",
        "why": "It follows the earlier live-cycle progress: pairwise damping inequalities are necessary but not sufficient for same-theory OS positivity.",
        "varied": "Schur-preimage quotient determinant",
        "observation": "sign of det(Bhat^{-1} circ Nhat) and pairwise minor status",
        "expected": "Pairwise tests remain positive while the triple determinant is the first possible obstruction.",
        "disconfirm": "If every realized triple with positive pairwise minors also has positive quotient determinant under the same assumptions.",
        "task": "Build the smallest finite Hermitian quotient family with positive pairwise minors and test determinant sign under the branch's boundary anomaly.",
        "success": "A determinant calculation identifies whether finite-family positivity is the necessary bridge premise.",
        "failure": "If no sign-sensitive obstruction exists, demote the determinant story and search for topology or observable-density failures.",
    }


def common_packet(
    *,
    packet_id: str,
    target_id: str,
    title: str,
    cycle_ids: list[str],
    branch_ids: list[str],
    sources: list[str],
    need: dict[str, Any],
    situation: dict[str, Any],
    variables: list[dict[str, Any]],
    interventions: list[dict[str, Any]],
    observations: list[dict[str, Any]],
    variants: list[dict[str, Any]],
    insights: list[str],
    transfer_scope: dict[str, Any],
    affected_nodes: list[str],
    affected_edges: list[str],
    graph_action: str,
    graph_updates: list[dict[str, Any]],
    tasks: list[dict[str, Any]],
    failures: list[str],
) -> dict[str, Any]:
    return {
        "packet_id": packet_id,
        "target_id": target_id,
        "created_utc": utc_now(),
        "source_artifacts": sources,
        "originating_cycle_ids": cycle_ids or ["seed"],
        "originating_branch_ids": branch_ids or ["seed"],
        "need_decision": need["decision"],
        "need_assessment": need,
        "trigger_criteria": need["criteria_met"],
        "situation": situation,
        "variables": variables,
        "interventions": interventions,
        "expected_observations": observations,
        "variants": variants,
        "insight_hypotheses": insights,
        "transfer_scope": transfer_scope,
        "affected_node_ids": affected_nodes,
        "affected_edge_ids": affected_edges,
        "graph_update_action": graph_action,
        "proposed_graph_updates": graph_updates,
        "followup_cycle_tasks": tasks,
        "failure_modes": failures,
        "epistemic_status": "conceptual_probe",
        "validation_handoff": "python agentic/scripts/validate_gedanken_experiment_packets.py",
    }


def reflection_packet(target_id: str, sources: list[str], cycle_ids: list[str], branch_ids: list[str], branch_title: str = "Reflection positivity branch", focus: dict[str, str] | None = None) -> dict[str, Any]:
    focus = focus or reflection_focus_from_text(branch_title)
    title = focus["title"]
    packet_id = stable_id("gedanken.packet", target_id, branch_title, focus["focus_id"], cycle_ids)
    transfer_verdict = "needs_certificate"
    situation = {
        "title": title,
        "purpose": focus["purpose"],
        "minimal_world": focus["minimal_world"],
        "mathematical_carrier": focus["carrier"],
        "controlled_contrast": focus["contrast"],
        "why_this_situation_is_informative": focus["why"],
        "non_claims": [
            "This does not prove a Yang-Mills obstruction.",
            "This does not replace continuum reflection positivity.",
            "This only designs the situation that a later concrete probe or derivation must compute."
        ],
    }
    need = need_assessment(
        "design_now",
        [
            "The branch has a positivity-transfer pressure but the decisive obstruction may be finite-family rather than pairwise.",
            f"A controlled contrast can separate the live-cycle focus `{focus['focus_id']}` from nearby positivity stories.",
        ],
        ["A same-theory finite observable family still has to be certified."],
        ["run_concrete_probe_first", "not_needed"],
        "A direct derivation would hide the conceptual distinction between pairwise positivity and full finite-family positivity; the imagined carrier isolates that distinction before computation.",
    )
    tasks = [
        followup(
            packet_id,
            title,
            transfer_verdict,
            "compute",
            focus["task"],
            focus["success"],
            focus["failure"],
            ["qualitative-toy-model-builder", "dimensional-symmetry-constraint-checker", "qualitative-physics-falsifier"],
        ),
        followup(
            packet_id,
            title,
            transfer_verdict,
            "update_graph",
            "Revise the qualitative graph edge from quotient phase to reflection Gram positivity as a needs-probe edge.",
            "The edge gains packet provenance, a concrete failure mode, and a validation handoff.",
            "If the carrier is a proxy with no same-theory map, quarantine as analogy.",
            ["gedanken-transfer-guard", "qualitative-physics-falsifier"],
        ),
    ]
    return common_packet(
        packet_id=packet_id,
        target_id=target_id,
        title=title,
        cycle_ids=cycle_ids,
        branch_ids=branch_ids,
        sources=sources,
        need=need,
        situation=situation,
        variables=[
            {"id": "delta", "role": "collar width", "control_status": "varied", "held_fixed_or_varied": "varied toward zero", "validity_regime": "finite reflected family before continuum transfer"},
            {"id": "live_focus", "role": focus["varied"], "control_status": "varied", "held_fixed_or_varied": "varied according to the originating cycle blocker", "validity_regime": "same finite reflected Wilson family named by the live branch"},
            {"id": "phi", "role": "quotient holonomy phase", "control_status": "dependent", "held_fixed_or_varied": "observed as delta varies", "validity_regime": "normalized finite-family quotient"},
            {"id": "detN", "role": "Gram determinant", "control_status": "dependent", "held_fixed_or_varied": "observed", "validity_regime": "finite matrix positivity test"},
        ],
        interventions=[
            {
                "id": "shrink-collar",
                "operation": "Let delta decrease while keeping the reflected observable labels fixed.",
                "varied_variable": focus["varied"],
                "held_fixed": ["observable family", "pairwise normalization", "reflection operation"],
                "predicted_direction": focus["expected"],
                "decision_value": "If the live focus creates a same-family obstruction, the branch must backtrack from generic positivity transfer to the exact finite-family bridge premise."
            }
        ],
        observations=[
            {
                "id": "phase-vs-determinant",
                "observable": focus["observation"],
                "expected_pattern": focus["expected"],
                "what_it_would_teach": "A bridge lemma must control the whole reflected family, not only pairwise overlap damping.",
                "what_would_disconfirm_it": focus["disconfirm"]
            }
        ],
        variants=[
            {"id": "force-zero-phase", "changed_condition": "Impose a real positive quotient with phi identically zero.", "predicted_change": "The determinant obstruction should disappear or move to an amplitude inequality.", "reason_for_variant": "Separates phase obstruction from amplitude failure."}
        ],
        insights=[
            f"The live-cycle focus is `{focus['focus_id']}`, so the next subgoal must preserve that exact distinction.",
            "The right positivity subgoal should be finite-family closed-cone control, not pairwise positivity.",
            "A useful falsifier is a same-algebra family with positive pairwise minors but negative determinant."
        ],
        transfer_scope={
            "transfer_verdict": transfer_verdict,
            "transfers": "Conceptual structure of the obstruction and the determinant falsifier shape.",
            "does_not_transfer": "Numerical sign, continuum existence, or proof of Yang-Mills nontriviality.",
            "transfer_certificate_needed": "The finite family must be realized by the same reflected observable algebra used by the target route."
        },
        affected_nodes=["var.quotient_phase_phi", "var.reflection_gram_N"],
        affected_edges=["rel-phase-falsifies-gram-transfer"],
        graph_action="needs_probe",
        graph_updates=[
            {
                "edge_id": "rel-phase-falsifies-gram-transfer",
                "action": "needs_probe",
                "epistemic_status": "conceptual_probe",
                "rationale": "Thought experiment identifies determinant/phase obstruction as a probe target, not an established relation."
            }
        ],
        tasks=tasks,
        failures=[
            "The imagined situation is too remote from the target observable algebra.",
            "The determinant failure is a toy artifact with no same-theory transfer certificate.",
            "The branch mistakes conceptual illumination for theorem progress."
        ],
    )


def spectral_packet(target_id: str, sources: list[str], cycle_ids: list[str], branch_ids: list[str], branch_title: str = "Spectral decay branch") -> dict[str, Any]:
    title = "A positive spectral measure with hidden low-energy leakage"
    packet_id = stable_id("gedanken.packet", target_id, branch_title, "spectral-leakage-decay", cycle_ids)
    transfer_verdict = "needs_certificate"
    need = need_assessment(
        "design_now",
        [
            "The branch interprets Euclidean decay as spectral-gap evidence.",
            "A controlled contrast can separate finite-window decay from support bounded away from zero.",
        ],
        ["Observable-density and large-time uniformity remain open."],
        ["not_needed", "quarantine_as_analogy"],
        "A direct proof attempt would likely restate the support condition; the imagined leakage situation makes the missing condition visible.",
    )
    tasks = [
        followup(
            packet_id,
            title,
            transfer_verdict,
            "derive",
            "Derive the exact condition under which Laplace decay bounds imply a spectral support gap for a family of observables.",
            "The condition names the observable family, measure support, and large-time uniformity requirement.",
            "If the condition only holds for one observable, demote to evidence task.",
            ["kb-deduce", "limit-convergence-behavior-auditor", "entailment-gap-auditor"],
        )
    ]
    return common_packet(
        packet_id=packet_id,
        target_id=target_id,
        title=title,
        cycle_ids=cycle_ids,
        branch_ids=branch_ids,
        sources=sources,
        need=need,
        situation={
            "title": title,
            "purpose": "Elicit the difference between decay of one correlator and a gap in the full excitation sector.",
            "minimal_world": "Imagine a positive measure dmu_O(lambda) with most mass above m but a tunable tiny tail near zero.",
            "mathematical_carrier": "Laplace transform C(t)=int exp(-t lambda) dmu_O(lambda) with a small low-energy tail.",
            "controlled_contrast": "Compare apparent finite-window exponential decay against true large-t spectral support.",
            "why_this_situation_is_informative": "It shows why observable density and uniform long-time control are needed before a correlator estimate becomes a mass-gap witness.",
            "non_claims": [
                "This does not assert that Yang-Mills has low-energy leakage.",
                "This does not produce a spectral theorem proof.",
                "This only isolates the failure mode of finite-window or restricted-observable decay."
            ],
        },
        variables=[
            {"id": "epsilon", "role": "low-energy tail mass", "control_status": "varied", "held_fixed_or_varied": "varied toward zero", "validity_regime": "positive spectral representation"},
            {"id": "t", "role": "Euclidean time", "control_status": "varied", "held_fixed_or_varied": "varied to large values", "validity_regime": "OS-reconstructed spectral readout"},
            {"id": "C", "role": "connected correlator", "control_status": "dependent", "held_fixed_or_varied": "observed", "validity_regime": "vacuum-subtracted observable sector"},
        ],
        interventions=[
            {"id": "hide-low-tail", "operation": "Make epsilon small enough that finite t windows look exponentially gapped.", "varied_variable": "epsilon", "held_fixed": ["high-energy mass scale", "observable norm", "positivity of the measure"], "predicted_direction": "C(t) appears to decay with rate m on bounded windows but is eventually dominated by the low-energy tail.", "decision_value": "Forces the next cycle to ask for uniform asymptotic decay and observable-density control."}
        ],
        observations=[
            {"id": "late-time-tail", "observable": "effective decay rate -d/dt log C(t)", "expected_pattern": "The effective rate initially tracks m and then bends toward the low-energy support.", "what_it_would_teach": "Finite-window decay is not enough; the route needs a lower spectral support statement for all non-vacuum excitations.", "what_would_disconfirm_it": "If the branch can prove the spectral measure has no support below m for a dense observable sector."}
        ],
        variants=[
            {"id": "dense-observable-sector", "changed_condition": "Require the observable algebra to approximate every non-vacuum excitation.", "predicted_change": "Decay of a sufficiently rich family can become a spectral witness.", "reason_for_variant": "Separates one-observable decay from sector-wide mass gap evidence."}
        ],
        insights=[
            "A correlator route must formulate a no-low-energy-tail lemma, not only a decay estimate.",
            "Observable density is a decisive bridge premise for turning Euclidean behavior into Hamiltonian spectrum."
        ],
        transfer_scope={
            "transfer_verdict": transfer_verdict,
            "transfers": "The conceptual failure mode of finite-window decay and restricted observable support.",
            "does_not_transfer": "Any actual spectral support claim about the target theory.",
            "transfer_certificate_needed": "OS reconstruction plus a dense gauge-invariant observable sector."
        },
        affected_nodes=["var.euclidean_time_t", "var.correlation_C", "var.spectral_gap_m"],
        affected_edges=["rel.euclidean-decay-to-gap", "rel.spectral-gap-controls-correlator"],
        graph_action="annotate_edge",
        graph_updates=[
            {"edge_id": "rel.euclidean-decay-to-gap", "action": "annotate_edge", "epistemic_status": "conceptual_probe", "rationale": "Thought experiment identifies low-energy leakage as a required falsifier for decay-to-gap transfer."}
        ],
        tasks=tasks,
        failures=[
            "The situation is used to argue by analogy instead of localizing a missing lemma.",
            "The branch ignores that tiny tails can dominate late-time behavior.",
            "The follow-up cycle fails to state which observable sector is being tested."
        ],
    )


def limit_packet(target_id: str, sources: list[str], cycle_ids: list[str], branch_ids: list[str], branch_title: str = "Continuum transfer branch") -> dict[str, Any]:
    title = "A limit-order switchboard for cutoff, volume, and long-time behavior"
    packet_id = stable_id("gedanken.packet", target_id, branch_title, "noncommuting-limit-switchboard", cycle_ids)
    transfer_verdict = "conceptual_only"
    need = need_assessment(
        "design_now",
        [
            "The branch moves from fixed regulator statements to continuum or infinite-volume commitments.",
            "Changing limit order can decide whether the qualitative claim is target-relevant or a regulated artifact.",
        ],
        ["The topology or observable sense of convergence still has to be named."],
        ["not_needed", "run_concrete_probe_first"],
        "A direct fixed-regulator derivation would not reveal whether the conclusion commutes with the target limit order.",
    )
    tasks = [
        followup(
            packet_id,
            title,
            transfer_verdict,
            "falsify",
            "Try to construct a simple F(a,L,t) where fixed-regulator decay fails to commute with continuum transfer.",
            "A counterexample class explains why the active branch needs uniform control.",
            "If no such class is possible under the branch assumptions, promote the uniformity premise as plausible but still unproved.",
            ["limit-convergence-behavior-auditor", "gedanken-counterfactual-variant-builder", "qualitative-physics-falsifier"],
        )
    ]
    return common_packet(
        packet_id=packet_id,
        target_id=target_id,
        title=title,
        cycle_ids=cycle_ids,
        branch_ids=branch_ids,
        sources=sources,
        need=need,
        situation={
            "title": title,
            "purpose": "Make noncommuting limits visible as a branch-control issue.",
            "minimal_world": "Imagine three knobs a, L, and t where each pairwise route looks controlled, but the conclusion changes when t tends to infinity before a tends to zero or L tends to infinity.",
            "mathematical_carrier": "A family F(a,L,t) with fixed-regulator decay, finite-volume spectral discreteness, and a continuum-transfer question.",
            "controlled_contrast": "Compare lim_{t to infinity} lim_{a to 0,L to infinity} F with lim_{a to 0,L to infinity} lim_{t to infinity} F.",
            "why_this_situation_is_informative": "It exposes whether a claimed qualitative relation is a real target property or only a path-dependent regulated artifact.",
            "non_claims": [
                "This does not assert which order is correct for the target.",
                "This does not replace a uniform estimate.",
                "This only identifies what uniformity a later proof attempt must supply."
            ],
        },
        variables=[
            {"id": "a", "role": "cutoff scale", "control_status": "varied", "held_fixed_or_varied": "varied toward zero", "validity_regime": "regulated construction"},
            {"id": "L", "role": "volume", "control_status": "varied", "held_fixed_or_varied": "varied toward infinity", "validity_regime": "finite-to-infinite volume transfer"},
            {"id": "t", "role": "Euclidean time", "control_status": "varied", "held_fixed_or_varied": "varied toward infinity", "validity_regime": "spectral readout"},
        ],
        interventions=[
            {"id": "swap-limit-order", "operation": "Exchange the long-time limit with cutoff and volume limits.", "varied_variable": "limit_order", "held_fixed": ["observable definition", "target branch commitment"], "predicted_direction": "A fixed-regulator spectral gap may disappear or fail to transfer if estimates are not uniform.", "decision_value": "If the conclusion changes under limit order, the branch must backtrack to a uniformity lemma."}
        ],
        observations=[
            {"id": "path-dependent-conclusion", "observable": "whether the qualitative gap or decay statement survives the target limit order", "expected_pattern": "One limit path gives an attractive relation while another leaves an explicit unknown or failure.", "what_it_would_teach": "The next experiment should test uniformity, not generate another fixed-regulator derivation.", "what_would_disconfirm_it": "A cutoff- and volume-uniform estimate that commutes with the spectral readout."}
        ],
        variants=[
            {"id": "add-uniform-bound", "changed_condition": "Assume a bound independent of a and L over the required t range.", "predicted_change": "The limit-order obstruction should weaken or disappear.", "reason_for_variant": "Identifies the exact kind of estimate that would rescue the branch."}
        ],
        insights=[
            "The branch should rank uniformity experiments above additional fixed-regulator calculations.",
            "Noncommuting limits are stop/backtrack criteria only after the uniformity rescue attempt fails."
        ],
        transfer_scope={
            "transfer_verdict": transfer_verdict,
            "transfers": "A branch-control diagnostic: whether the next cycle should ask for a uniformity lemma.",
            "does_not_transfer": "Any final conclusion about the target limit.",
            "transfer_certificate_needed": "A named topology or observable sense in which the limits are taken."
        },
        affected_nodes=["var.cutoff_a", "var.volume_L", "var.euclidean_time_t"],
        affected_edges=["rel.cutoff-to-gram-positivity"],
        graph_action="challenge_edge",
        graph_updates=[
            {"edge_id": "rel.cutoff-to-gram-positivity", "action": "challenge_edge", "epistemic_status": "conceptual_probe", "rationale": "Thought experiment challenges transfer unless cutoff, volume, and long-time limits commute in the stated topology."}
        ],
        tasks=tasks,
        failures=[
            "The thought experiment remains too abstract and never names F(a,L,t).",
            "The follow-up treats a limit-order warning as a proof of failure.",
            "Uniformity requirements are not attached to a topology or observable sense."
        ],
    )


def packet_for_branch(target_id: str, cycle: dict[str, Any], output: dict[str, Any], run_id: str) -> dict[str, Any]:
    cycle_id = clean_text(cycle.get("cycle_id")) or "cycle-unknown"
    branch_id = clean_text(output.get("branch_id")) or "branch-unknown"
    branch_title = clean_text(output.get("branch_title")) or branch_id
    source = f"agentic/runs/discovery_marathons/{run_id}/cycles/{cycle_id}.json"
    branch_text = clean_text([branch_title, output.get("attempted_derivation", {}).get("blocking_gap", ""), output.get("mathematical_learning", ""), output.get("falsifiers", []), output.get("next_experiment", "")])
    cycle_text = clean_text(cycle.get("branch_outputs", []))
    focus = focus_for_text(cycle_text)
    if focus in {"boundary_ope_extraction", "quotient_holonomy", "schur_preimage_determinant"}:
        return reflection_packet(target_id, [source], [cycle_id], [branch_id], branch_title, reflection_focus_from_text(cycle_text))
    domain = domain_from_text(branch_text)
    if focus == "spectral_leakage" or domain == "spectral_leakage":
        return spectral_packet(target_id, [source], [cycle_id], [branch_id], branch_title)
    return limit_packet(target_id, [source], [cycle_id], [branch_id], branch_title)


def generated_packet_paths(run_id: str) -> list[Path]:
    root = run_dir(run_id) / "gedanken"
    if not root.exists():
        return []
    return sorted(root.glob("*.json"))


def load_live_packets(run_id: str) -> list[dict[str, Any]]:
    packets = []
    for path in generated_packet_paths(run_id):
        payload = load_json_object(path)
        if isinstance(payload, dict) and payload.get("packet_id"):
            packets.append(payload)
    return packets


def persist_live_packets(target_id: str, cycles: list[dict[str, Any]], run_id: str) -> list[dict[str, Any]]:
    root = run_dir(run_id) / "gedanken"
    root.mkdir(parents=True, exist_ok=True)
    packets: dict[str, dict[str, Any]] = {}
    for cycle in cycles[-8:]:
        for output in cycle.get("branch_outputs", [])[:2]:
            if not isinstance(output, dict):
                continue
            packet = packet_for_branch(target_id, cycle, output, run_id)
            packets[packet["packet_id"]] = packet
    for packet in packets.values():
        write_json(root / f"{packet['packet_id']}.json", packet)
    return sorted(packets.values(), key=lambda row: (row["originating_cycle_ids"], row["packet_id"]))


def seed_packets(target_id: str, sources: list[str]) -> list[dict[str, Any]]:
    return [
        reflection_packet(target_id, sources, ["seed"], ["seed"]),
        spectral_packet(target_id, sources, ["seed"], ["seed"]),
        limit_packet(target_id, sources, ["seed"], ["seed"]),
    ]


def build_packets(target_id: str, cycles: list[dict[str, Any]], run_id: str) -> tuple[list[dict[str, Any]], str]:
    if target_id == "p-vs-np-target":
        module_path = ROOT / "skills/reasoning/pvsnp-gedanken-complexity-lab/scripts/build_pvsnp_gedanken_packets.py"
        spec = importlib.util.spec_from_file_location("build_pvsnp_gedanken_packets", module_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {module_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        payload = module.build_payload()
        return payload["packets"], payload["generation_mode"]
    live = persist_live_packets(target_id, cycles, run_id) if cycles and run_id != "unknown-run" else []
    live = live or load_live_packets(run_id)
    if live:
        return live, "live_cycle_context"
    return seed_packets(target_id, cycle_sources(cycles, run_id)), "static_seed_fallback"


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Gedanken Experiment Packets",
        "",
        f"- Target: `{payload['target_id']}`",
        f"- Packets: `{len(payload['packets'])}`",
        f"- Generation mode: `{payload['generation_mode']}`",
        "",
    ]
    for packet in payload["packets"]:
        lines.append(f"## {packet['situation']['title']}")
        lines.append("")
        lines.append(f"- Packet: `{packet['packet_id']}`")
        lines.append(f"- Need decision: `{packet['need_decision']}`")
        lines.append(f"- Epistemic status: `{packet['epistemic_status']}`")
        lines.append(f"- Origin cycles: `{', '.join(packet['originating_cycle_ids'])}`")
        lines.append(f"- Origin branches: `{', '.join(packet['originating_branch_ids'])}`")
        lines.append(f"- Purpose: {packet['situation']['purpose']}")
        lines.append(f"- Transfer verdict: `{packet['transfer_scope'].get('transfer_verdict', 'unknown')}`")
        lines.append(f"- Informative because: {packet['situation']['why_this_situation_is_informative']}")
        lines.append("- Follow-up tasks:")
        for task in packet["followup_cycle_tasks"]:
            lines.append(f"  - `{task['action']}` {task['description']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="auto")
    args = parser.parse_args()
    _, run_state = load_run_state()
    target_id = args.target
    if target_id == "auto":
        target_id = clean_text(run_state.get("target_id")) or "yang-mills-existence-and-mass-gap-target"
    cycles = [cycle for cycle in load_cycles(run_state) if cycle.get("valid_as_research_cycle")] if run_state else []
    run_id = run_state.get("run_id", "unknown-run") if run_state else "unknown-run"
    packets, mode = build_packets(target_id, cycles, run_id)
    payload = {
        "version": 1,
        "target_id": target_id,
        "generated_utc": utc_now(),
        "generation_mode": mode,
        "live_packet_count": sum(1 for packet in packets if packet.get("originating_cycle_ids") != ["seed"]),
        "quarantine_count": sum(1 for packet in packets if packet.get("need_decision") == "quarantine_as_analogy" or packet.get("graph_update_action") == "quarantine"),
        "queue_handoff_count": sum(len(packet.get("followup_cycle_tasks", [])) for packet in packets),
        "packets": packets,
    }
    write_json(OUT, payload)
    MD.parent.mkdir(parents=True, exist_ok=True)
    MD.write_text(render_markdown(payload), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"Wrote {MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
