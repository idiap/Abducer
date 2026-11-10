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
"""Judge strategy progression, payoff, paper readiness, and target alignment."""

from __future__ import annotations

import json
from statistics import mean
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, stable_id, utc_now, write_json
from discovery_marathon_common import LATEST_JSON, load_cycles, load_run_state, markdown_list, write_markdown


OUT_DIR = ROOT / "agentic/reports/strategy_progression_judge"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
WINDOW_SIZE = 10
JUDGE_SKILLS = [
    "progression-payoff-judge",
    "paper-contribution-readiness-judge",
    "main-problem-alignment-auditor",
]
CONTRIBUTION_MONITOR = ROOT / "agentic/reports/scientific_contribution_monitor/latest.json"
TARGET_LITERATURE = ROOT / "agentic/reports/target_literature_evolution/latest.json"
MACRO_STRATEGY = ROOT / "agentic/reports/macro_strategy/latest.json"
PVSNP_PRESSURE_BRIDGES = ROOT / "agentic/reports/pvsnp_pressure_bridges/latest.json"


def target_matches(report: dict[str, Any], target_id: str) -> bool:
    declared = clean_text(report.get("target_id"))
    return not declared or declared == target_id


def contains_any(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return any(term in lower for term in terms)


def cycle_number(cycle: dict[str, Any]) -> int:
    raw = clean_text(cycle.get("cycle_id"))
    try:
        return int(raw.split("-")[-1])
    except ValueError:
        return 0


def branch_output(cycle: dict[str, Any]) -> dict[str, Any]:
    outputs = cycle.get("branch_outputs", [])
    return outputs[0] if outputs and isinstance(outputs[0], dict) else {}


def first_lemma(output: dict[str, Any]) -> dict[str, Any]:
    lemmas = output.get("candidate_lemmas", [])
    return lemmas[0] if lemmas and isinstance(lemmas[0], dict) else {}


def cycle_summary(cycle: dict[str, Any]) -> dict[str, Any]:
    output = branch_output(cycle)
    lemma = first_lemma(output)
    return {
        "cycle_id": clean_text(cycle.get("cycle_id")),
        "cycle_number": cycle_number(cycle),
        "branch_title": clean_text(output.get("branch_title")),
        "mathematical_learning": clean_text(output.get("mathematical_learning")),
        "blocking_gap": clean_text(output.get("attempted_derivation", {}).get("blocking_gap")),
        "next_experiment": clean_text(output.get("next_experiment")),
        "definition_count": len(lemma.get("definitions", [])),
        "assumption_count": len(lemma.get("assumptions", [])),
        "equation_count": len(lemma.get("equations", [])),
        "derivation_step_count": len(output.get("attempted_derivation", {}).get("steps", [])),
        "falsifier_count": len(output.get("falsifiers", [])),
        "dependency_update_count": len(output.get("dependency_updates", [])),
        "text": clean_text(
            " ".join(
                [
                    output.get("branch_title", ""),
                    output.get("mathematical_learning", ""),
                    output.get("attempted_derivation", {}).get("blocking_gap", ""),
                    output.get("next_experiment", ""),
                    json.dumps(lemma.get("equations", []), ensure_ascii=False),
                    " ".join(output.get("falsifiers", [])),
                ]
            )
        ),
    }


def score_terms(text: str, terms: list[str], *, floor: int = 1) -> int:
    hits = sum(1 for term in terms if term.lower() in text.lower())
    return max(0, min(5, floor + hits))


def average_int(values: list[int]) -> int:
    return round(mean(values)) if values else 0


def latest_window(cycles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid = sorted([cycle for cycle in cycles if cycle.get("valid_as_research_cycle")], key=cycle_number)
    return valid[-WINDOW_SIZE:]


def load_research_cycles() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    marathon = load_optional_json(LATEST_JSON)
    _, run_state = load_run_state(clean_text(marathon.get("run_id")) or None)
    if not run_state:
        return marathon, []
    cycles = [cycle for cycle in load_cycles(run_state) if cycle.get("valid_as_research_cycle")]
    return marathon, sorted(cycles, key=cycle_number)


def active_strategy(macro: dict[str, Any], window_rows: list[dict[str, Any]], target_id: str) -> dict[str, Any]:
    strategies = macro.get("macro_strategies", [])
    top = strategies[0] if strategies else {}
    joined = " ".join(row["text"] for row in window_rows)
    if target_id == "p-vs-np-target":
        if contains_any(joined, ["beta", "black-box", "projection", "demagnification", "threshold"]):
            route = "quantitative transfer obstruction for hardness magnification"
            active_object = "source exponent a, overhead q, target-query exponent beta, and the target SAT exponent c"
        elif contains_any(joined, ["mcsp", "mktp", "certificate", "meta-complexity"]):
            route = "searchable meta-complexity certificate bridge"
            active_object = "verifier, decoder, certificate length, search schedule, gap coverage, and soundness threshold"
        elif contains_any(joined, ["natural", "relativization", "algebrization", "oracle", "barrier"]):
            route = "barrier-aware no-go and escape-condition audit"
            active_object = "method-class premises, barrier signature, escape feature, and target-preserving transfer"
        elif contains_any(joined, ["all-exponent", "cofinal", "p/poly", "advice", "uniform"]):
            route = "all-exponent quantifier-lift and uniformity control"
            active_object = "cofinal source obligation family, valid-length coverage, uniform indexing, and advice accounting"
        else:
            route = "P vs NP bridge-abstraction search"
            active_object = "complexity-theoretic source object, target lower-bound consequence, controlled transfer interface, and falsifier"
    elif contains_any(joined, ["wilson", "reflection", "os", "hairpin", "collar", "schur", "psd"]):
        route = "OS reflection-positivity bridge through Wilson collar quotient tests"
        active_object = "finite reflected Wilson Gram quotient and its tangent-cone / Schur-complement obstruction"
    elif contains_any(joined, ["spectral", "hamiltonian", "mass gap", "hilbert"]):
        route = "spectral-gap witness after reconstruction"
        active_object = "reconstructed Hilbert space, vacuum, Hamiltonian, and non-vacuum excitation sector"
    elif contains_any(joined, ["rg", "continuum", "cutoff", "uniform"]):
        route = "RG continuum-construction discipline"
        active_object = "cutoff-uniform continuum limit obligation"
    else:
        route = clean_text(top.get("title")) or "active discovery route"
        active_object = "current branch object extracted from the latest cycle window"
    return {
        "strategy_id": clean_text(top.get("strategy_id")) or stable_id("strategy", route),
        "route_family": clean_text(top.get("route_family")) or "unknown route family",
        "title": route,
        "active_object": active_object,
        "macro_thesis": clean_text(top.get("macro_thesis")),
        "source_macro_strategy": clean_text(top.get("title")),
    }


def progression_scores(window_rows: list[dict[str, Any]], target_id: str) -> dict[str, int]:
    joined = " ".join(row["text"] for row in window_rows)
    if target_id == "p-vs-np-target":
        mechanics = score_terms(joined, ["because", "mechanism", "beta", "threshold", "certificate", "oracle", "advice", "natural", "uniform"])
        alignment = score_terms(joined, ["p vs np", "sat", "circuit", "lower bound", "p/poly", "np", "mcsp", "complexity", "uniform"], floor=0)
        payoff = score_terms(joined, ["compute", "test", "audit", "prove", "falsifier", "obstruction", "no-go", "certificate", "exponent"], floor=1)
        anti_drift = score_terms(joined, ["stop", "quarantine", "pivot", "backtrack", "target-preserving", "source object", "target object", "advice", "barrier"], floor=1)
    else:
        mechanics = score_terms(joined, ["because", "mechanism", "tangent cone", "schur", "kernel", "holonomy", "ope"])
        alignment = score_terms(joined, ["yang-mills", "wilson", "gauge", "os", "reflection positivity", "continuum", "hilbert", "spectral"], floor=0)
        payoff = score_terms(joined, ["compute", "test", "evaluate", "falsifier", "obstruction", "paper", "handoff", "prior-art"], floor=1)
        anti_drift = score_terms(joined, ["stop", "quarantine", "pivot", "backtrack", "same-theory", "source object", "target object"], floor=1)
    specificity = min(
        5,
        1
        + min(1, average_int([row["definition_count"] for row in window_rows]))
        + min(1, average_int([row["assumption_count"] for row in window_rows]))
        + min(1, average_int([row["equation_count"] for row in window_rows]))
        + min(1, average_int([row["falsifier_count"] for row in window_rows])),
    )
    learning = min(5, 1 + len({row["branch_title"] for row in window_rows if row["branch_title"]}) // 2 + min(2, len(window_rows) // 5))
    return {
        "mechanistic_gain": mechanics,
        "technical_specificity": specificity,
        "problem_alignment": alignment,
        "payoff_potential": payoff,
        "anti_drift_control": anti_drift,
        "window_learning": learning,
    }


def payoff_label(score: int) -> str:
    if score >= 82:
        return "high"
    if score >= 66:
        return "medium_high"
    if score >= 52:
        return "watch"
    return "low"


def weighted_progression(scores: dict[str, int]) -> int:
    weights = {
        "mechanistic_gain": 0.20,
        "technical_specificity": 0.20,
        "problem_alignment": 0.20,
        "payoff_potential": 0.18,
        "anti_drift_control": 0.12,
        "window_learning": 0.10,
    }
    return round(sum((scores[key] / 5) * 100 * weight for key, weight in weights.items()))


def top_contribution(contribution: dict[str, Any]) -> dict[str, Any]:
    top = contribution.get("top_candidate")
    if isinstance(top, dict) and top:
        return top
    candidates = contribution.get("candidates", [])
    return candidates[0] if candidates and isinstance(candidates[0], dict) else {}


def readiness_from_candidate(candidate: dict[str, Any], alignment_score: int) -> dict[str, Any]:
    candidate_scores = candidate.get("scores", {}) if isinstance(candidate.get("scores"), dict) else {}
    dimensions = {
        "conceptual_novelty": int(candidate_scores.get("conceptual_novelty", 0)),
        "technical_depth": max(
            int(candidate_scores.get("certification_readiness", 0)),
            int(candidate_scores.get("implications", 0)),
        ),
        "explanatory_power": int(candidate_scores.get("explanatory_power", 0)),
        "target_alignment": max(alignment_score, int(candidate_scores.get("target_relevance", 0))),
        "validation_readiness": int(candidate_scores.get("certification_readiness", 0)),
        "paper_packaging_readiness": 3 if candidate.get("status") in {"near_certification", "good_enough_to_handoff"} else 2,
    }
    composite = round(mean(dimensions.values()) * 20) if dimensions else 0
    if candidate.get("status") == "good_enough_to_handoff" and dimensions["validation_readiness"] >= 4:
        level = "paper_note_ready"
    elif composite >= 76:
        level = "near_paper_note"
    elif composite >= 58:
        level = "developing"
    else:
        level = "not_ready"
    return {
        "candidate_id": clean_text(candidate.get("candidate_id")),
        "candidate_title": clean_text(candidate.get("branch_title") or candidate.get("candidate_id") or "current contribution candidate"),
        "smallest_honest_claim": clean_text(candidate.get("smallest_honest_claim"))
        or "A contribution-shaped claim has not yet been stabilized; the next bounded step must name the source object, target object, validation burden, and overclaim boundary.",
        "paper_contribution_type": clean_text(candidate.get("contribution_type")) or "contribution_search",
        "readiness_level": level,
        "readiness_score": composite,
        "dimension_scores": dimensions,
        "novelty_argument": clean_text(candidate.get("why_it_could_stand_alone"))
        or "Novelty must be established against the target literature before paper claims are made.",
        "explanatory_power": (
            "The candidate is valuable if it explains why a route succeeds or fails through a named mechanism, not merely because it extends the workflow."
        ),
        "main_problem_implication": clean_text(candidate.get("implication_map", {}).get("paper_level"))
        or "The candidate must state how it changes the main target's route priority, validation burden, or obstruction map.",
        "validation_burden": candidate.get("validation_burden", [])
        or ["Run a bounded validation and prior-art comparison before any paper-level claim."],
        "overclaim_boundary": clean_text(candidate.get("overclaim_boundary"))
        or "This can be a scoped scientific contribution without proving the main theorem.",
        "paper_skeleton": {
            "title": "A scoped obstruction or bridge note for the active discovery route",
            "abstract_claim": clean_text(candidate.get("smallest_honest_claim"))
            or "A contribution-shaped claim has not yet been stabilized.",
            "core_sections": [
                "Target bottleneck and historical positioning",
                "Definitions, assumptions, and validity regime",
                "Main finite criterion, bridge lemma, or obstruction",
                "Validation, falsifiers, and overclaim boundary",
                "Implications for the main problem and next analyses",
            ],
            "decisive_artifacts": [
                "evidence table from the judged 10-cycle window",
                "prior-art boundary",
                "bounded falsifier or validation calculation",
            ],
        },
    }


def alignment_audit(strategy: dict[str, Any], window_rows: list[dict[str, Any]], literature: dict[str, Any], target_id: str) -> dict[str, Any]:
    joined = " ".join(row["text"] for row in window_rows)
    commitments = []
    if target_id == "p-vs-np-target":
        commitment_terms = {
            "target lower-bound consequence": ["p vs np", "sat", "circuit lower", "lower bound", "np", "p/poly"],
            "uniformity and advice control": ["uniform", "advice", "nonuniform", "search", "deterministic"],
            "quantitative exponent transfer": ["beta", "q", "threshold", "exponent", "window", "margin"],
            "barrier compatibility": ["natural", "relativization", "algebrization", "oracle", "barrier"],
            "meta-complexity carrier": ["mcsp", "mktp", "meta-complexity", "certificate"],
            "route-specific no-go discipline": ["no-go", "impossibility", "falsifier", "quarantine", "demote"],
        }
        for commitment, terms in commitment_terms.items():
            if contains_any(joined, terms):
                commitments.append(commitment)
        if {"target lower-bound consequence", "quantitative exponent transfer"} & set(commitments):
            alignment_class = "bridge_aligned"
        elif "route-specific no-go discipline" in commitments:
            alignment_class = "negative_result_aligned"
        elif "meta-complexity carrier" in commitments:
            alignment_class = "carrier_aligned_with_validation_requirement"
        else:
            alignment_class = "method_aligned_or_drifting"
        return {
            "alignment_class": alignment_class,
            "target_commitments_touched": commitments or literature.get("solution_criteria", [])[:3],
            "source_to_target_handoff": "Source: latest cycle window and bridge candidates. Target: P != NP or an explicitly scoped lower-bound/nonuniform separation consequence.",
            "proxy_or_transfer_risk": "The branch remains aligned only if its carrier, barrier escape, or transfer formula preserves uniformity, valid lengths, and the all-exponent target rather than proving a proxy statement.",
            "alignment_gain": "The window is valuable when it replaces slogans about hardness magnification or barriers with exact source objects, target objects, thresholds, and falsifiers.",
            "alignment_loss": "The main danger is proving a bounded-window, advised, natural, relativizing, or target-equivalent proxy that cannot affect P vs NP route priority.",
            "repair_action": "Every next analysis must name the complexity class target, source model, transfer formula or certificate object, and the falsifier that would force pivot.",
            "decision_effect": "Alignment supports continuation only toward a bounded calculation, no-go theorem, certificate audit, or paper-contribution handoff.",
        }
    commitment_terms = {
        "same-theory continuum construction": ["same-theory", "continuum", "cutoff", "limit"],
        "gauge-invariant observable algebra": ["wilson", "gauge", "observable"],
        "reflection positivity / OS reconstruction": ["os", "reflection positivity", "reflected", "schwinger"],
        "nontriviality": ["nontrivial", "interacting"],
        "Hamiltonian and spectral-gap witness": ["hamiltonian", "spectral", "mass gap", "hilbert", "vacuum"],
        "finite obstruction discipline": ["falsifier", "obstruction", "negative", "schur", "kernel", "psd"],
    }
    for commitment, terms in commitment_terms.items():
        if contains_any(joined, terms):
            commitments.append(commitment)
    if {"same-theory continuum construction", "gauge-invariant observable algebra", "reflection positivity / OS reconstruction"} & set(commitments):
        alignment_class = "bridge_aligned"
    elif "Hamiltonian and spectral-gap witness" in commitments:
        alignment_class = "directly_aligned"
    elif "finite obstruction discipline" in commitments:
        alignment_class = "proxy_aligned_with_transfer_requirement"
    else:
        alignment_class = "method_aligned_or_drifting"
    risk = (
        "The finite Wilson quotient work remains aligned only if each quotient, collar, and boundary-OPE calculation carries a same-theory transfer certificate into OS-positive continuum Schwinger data."
        if "finite obstruction discipline" in commitments or "reflection positivity / OS reconstruction" in commitments
        else "The branch must restate its source object, target object, and validation handoff before receiving long-run budget."
    )
    return {
        "alignment_class": alignment_class,
        "target_commitments_touched": commitments or literature.get("solution_criteria", [])[:3],
        "source_to_target_handoff": (
            "Source: latest cycle window and finite/local route objects. Target: the main problem's construction, reconstruction, obstruction, or spectral witness obligation."
        ),
        "proxy_or_transfer_risk": risk,
        "alignment_gain": "The window keeps the current object tied to a named bridge or obstruction rather than only expanding a hypothesis queue.",
        "alignment_loss": "The remaining danger is proving a finite or boundary statement whose constants, observable algebra, or positivity do not survive the target limit.",
        "repair_action": "Every next analysis must name the target-preserving object, validity regime, and validation handoff before it can be promoted.",
        "decision_effect": "Alignment supports continuation with adaptation, but only toward a bounded validation or paper-contribution handoff.",
    }


def window_progress(window_rows: list[dict[str, Any]]) -> dict[str, Any]:
    progressed = []
    not_progressed = []
    for row in window_rows[-5:]:
        if row["equation_count"] or row["falsifier_count"] or contains_any(row["text"], ["compute", "kernel", "schur", "ope", "falsifier"]):
            progressed.append(
                {
                    "cycle_id": row["cycle_id"],
                    "change": row["mathematical_learning"]
                    or f"{row['branch_title']} introduced a content-specific object or test.",
                    "next_analysis": row["next_experiment"],
                }
            )
        else:
            not_progressed.append(
                {
                    "cycle_id": row["cycle_id"],
                    "block": row["blocking_gap"] or "No concrete mathematical change was detected in this cycle.",
                }
            )
    if not progressed:
        progressed.append(
            {
                "cycle_id": window_rows[-1]["cycle_id"] if window_rows else "",
                "change": "The judged window did not expose a strong content-specific progression signal.",
                "next_analysis": "Backtrack to target commitments and force a bounded validation test.",
            }
        )
    if not not_progressed:
        latest_gap = window_rows[-1]["blocking_gap"] if window_rows else ""
        not_progressed.append(
            {
                "cycle_id": window_rows[-1]["cycle_id"] if window_rows else "",
                "block": latest_gap
                or "The main unresolved issue is not absence of ideas but certification: the strongest claim still needs a bounded validation or transfer proof.",
            }
        )
    return {"what_progressed": progressed, "what_did_not_progress": not_progressed}


def build_high_reward_avenues(target_id: str, contribution: dict[str, Any]) -> list[dict[str, Any]]:
    if target_id != "p-vs-np-target":
        return []
    pressure = load_optional_json(PVSNP_PRESSURE_BRIDGES)
    bridges = pressure.get("bridge_candidates", []) if isinstance(pressure.get("bridge_candidates"), list) else []
    rows: list[dict[str, Any]] = []
    for bridge in sorted(bridges, key=lambda row: -int(row.get("priority_score", 0)))[:5]:
        rows.append(
            {
                "avenue_id": clean_text(bridge.get("id")),
                "title": clean_text(bridge.get("title")),
                "novelty_signal": clean_text(bridge.get("bridge_abstraction")),
                "reward_condition": clean_text(bridge.get("proof_obligation")),
                "step_back_or_pivot_condition": clean_text(bridge.get("when_to_pivot")),
                "why_it_matters": clean_text(bridge.get("paper_safe_narrative") or bridge.get("difficulty_hypothesis")),
            }
        )
    candidate = top_contribution(contribution)
    if candidate:
        rows.insert(
            0,
            {
                "avenue_id": clean_text(candidate.get("candidate_id")),
                "title": clean_text(candidate.get("branch_title") or "current contribution candidate"),
                "novelty_signal": clean_text(candidate.get("smallest_honest_claim")),
                "reward_condition": clean_text(candidate.get("validation_burden", [""])[0] if candidate.get("validation_burden") else ""),
                "step_back_or_pivot_condition": "; ".join(candidate.get("stop_when", [])[:2]),
                "why_it_matters": clean_text(candidate.get("why_it_could_stand_alone")),
            },
        )
    return rows


def make_judgement(
    *,
    cycles: list[dict[str, Any]],
    marathon: dict[str, Any],
    contribution: dict[str, Any],
    literature: dict[str, Any],
    macro: dict[str, Any],
) -> dict[str, Any]:
    window_cycles = latest_window(cycles)
    window_rows = [cycle_summary(cycle) for cycle in window_cycles]
    target_id = clean_text(marathon.get("target_id")) or clean_text(literature.get("target_id"))
    scores = progression_scores(window_rows, target_id)
    progression_score = weighted_progression(scores)
    strategy = active_strategy(macro, window_rows, target_id)
    alignment = alignment_audit(strategy, window_rows, literature, target_id)
    readiness = readiness_from_candidate(top_contribution(contribution), scores["problem_alignment"])
    progress = window_progress(window_rows)
    if readiness["readiness_level"] in {"paper_note_ready", "paper_argument_ready"}:
        decision = "handoff_after_bounded_validation"
    elif progression_score >= 70 and scores["problem_alignment"] >= 3:
        decision = "continue_with_targeted_adaptation"
    elif progression_score >= 55:
        decision = "backtrack_to_validation_handoff"
    else:
        decision = "quarantine_unless_alignment_is_repaired"
    if target_id == "p-vs-np-target":
        next_test = (
            "Compute the next named transfer or certificate parameter: a,q,beta for the active carrier, certificate length/searchability for MCSP/MKtP, or the exact barrier premise that triggers a route-specific no-go."
        )
        summary = (
            "The current P vs NP route is valuable only when it produces exact complexity-theoretic control: quantitative transfer inequalities, searchable certificate conditions, barrier-premise audits, or no-go theorems. "
            "Its payoff is not another broad route story; it is a bridge or obstruction that changes which lower-bound avenues deserve further work."
        )
        pivot_invariant = (
            "If the next work only restates hardness magnification, MCSP promise, or barrier folklore, the branch is looping. If it computes a concrete transfer parameter, proves a route-specific no-go, or certifies a searchable certificate carrier with no advice leakage, it is moving toward a real scientific contribution."
        )
        when_to_stop = (
            "Stop, backtrack, or quarantine when two sharpened attempts still yield only a bounded exponent window, advised hard strings, a natural/relativizing/algebrizing proof object, or a certificate-existence condition equivalent to the target lower bound."
        )
        do_not_stop = (
            "Do not stop while a named carrier still has an untested exact audit: beta=0 or N^{o(1)} query dependence, compact searchable certificates, sparse non-natural property escape, proof-system overhead, or cofinal all-exponent lift."
        )
    else:
        next_test = (
            "Compute the next finite obstruction or bridge validation named by the latest cycle, then test whether it preserves the source object, target object, and same-theory handoff."
        )
        summary = (
            "The current route is strongest when it converts the Wilson/OS bridge pressure into a finite, same-theory obstruction or validation calculation. "
            "Its value is not that it solves the main problem now, but that it can isolate a publishable bridge or falsifier that changes how the main problem should be attacked."
        )
        pivot_invariant = (
            "If the next work only restates the obstruction ladder, the branch is looping. If it computes the first concrete H,K Wilson collar case "
            "or proves the finite theorem rigorously, it is moving toward a real scientific contribution."
        )
        when_to_stop = (
            "Stop or quarantine this branch only if the next bounded obstruction/bridge calculation cannot state a source object, target object, transfer condition, and validation handoff, or if two sharpened attempts leave the finite result unable to affect the main target's route priority."
        )
        do_not_stop = (
            "Do not stop while the branch still has a concrete calculation that can decide positivity, kernel structure, Schur-complement obstruction, uniform-transfer debt, or paper-level obstruction value in the same target architecture."
        )
    if window_rows and window_rows[-1]["next_experiment"]:
        next_test = window_rows[-1]["next_experiment"]
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": target_id,
        "judgement_id": stable_id(
            "strategy-judge",
            marathon.get("run_id", ""),
            window_rows[0]["cycle_id"] if window_rows else "",
            window_rows[-1]["cycle_id"] if window_rows else "",
        ),
        "judgement_cadence": {
            "policy": "Run after each completed 10 valid research cycles; between boundaries, judge the rolling latest 10-cycle window.",
            "window_size": WINDOW_SIZE,
            "total_valid_research_cycles": len(cycles),
            "completed_ten_cycle_windows": len(cycles) // WINDOW_SIZE,
            "judgement_due": len(cycles) >= WINDOW_SIZE,
            "next_boundary_cycle_count": ((len(cycles) // WINDOW_SIZE) + 1) * WINDOW_SIZE,
        },
        "window": {
            "cycle_ids": [row["cycle_id"] for row in window_rows],
            "window_research_cycle_count": len(window_rows),
            "start_cycle_id": window_rows[0]["cycle_id"] if window_rows else "",
            "end_cycle_id": window_rows[-1]["cycle_id"] if window_rows else "",
        },
        "generated_by_skills": JUDGE_SKILLS,
        "evidence_sources": [
            rel(LATEST_JSON),
            rel(CONTRIBUTION_MONITOR),
            rel(TARGET_LITERATURE),
            rel(MACRO_STRATEGY),
            *(f"cycle:{row['cycle_id']}" for row in window_rows),
        ],
        "current_strategy": strategy,
        "progression_judgement": {
            "decision": decision,
            "payoff_potential": payoff_label(progression_score),
            "progression_score": progression_score,
            "dimension_scores": scores,
            "summary": summary,
            "contribution_pivot_invariant": pivot_invariant,
            **progress,
            "next_decisive_test": next_test,
            "when_to_stop": when_to_stop,
            "do_not_stop_prematurely_if": do_not_stop,
        },
        "paper_contribution_readiness": readiness,
        "main_problem_alignment": alignment,
        "strategy_payoff_table": [
            {
                "strategy_id": clean_text(strategy_row.get("strategy_id")),
                "title": clean_text(strategy_row.get("title")),
                "priority_score": strategy_row.get("priority_score", 0),
                "payoff_read": (
                    "High if its next computation produces a bounded bridge lemma, obstruction, or validation handoff; low if it only restates route ambition."
                ),
            "paper_contribution_path": clean_text(strategy_row.get("what_to_compute_next", [""])[0])
            if strategy_row.get("what_to_compute_next")
            else "",
            }
            for strategy_row in macro.get("macro_strategies", [])
        ],
        "novelty_high_reward_avenues": build_high_reward_avenues(target_id, contribution),
        "validation_handoff": [
            "Run validate_strategy_progression_judge.py after the builder.",
            "Render the Strategy Judge report tab in generate_discovery_marathon_html.py.",
            "Re-run this judge whenever the valid research-cycle count reaches another 10-cycle boundary.",
        ],
        "source_artifacts": {
            "marathon_report": rel(LATEST_JSON),
            "contribution_monitor": rel(CONTRIBUTION_MONITOR),
            "target_literature": rel(TARGET_LITERATURE),
            "macro_strategy": rel(MACRO_STRATEGY),
        },
        "epistemic_status": "interpretive_judgement_from_accumulated_artifacts",
    }


def render_markdown(report: dict[str, Any]) -> str:
    progression = report["progression_judgement"]
    readiness = report["paper_contribution_readiness"]
    alignment = report["main_problem_alignment"]
    lines = [
        "# Strategy Progression Judge",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Window: `{report['window']['start_cycle_id']}` to `{report['window']['end_cycle_id']}`",
        f"- Decision: `{progression['decision']}`",
        f"- Payoff potential: `{progression['payoff_potential']}`",
        f"- Paper readiness: `{readiness['readiness_level']}`",
        f"- Alignment: `{alignment['alignment_class']}`",
        "",
        "## Current Strategy",
        "",
        f"- Route: {report['current_strategy']['title']}",
        f"- Active object: {report['current_strategy']['active_object']}",
        "",
        "## What Progressed",
        "",
    ]
    for row in progression["what_progressed"]:
        lines.append(f"- `{row['cycle_id']}` {row['change']}")
    lines.extend(["", "## What Did Not Progress", ""])
    for row in progression["what_did_not_progress"]:
        lines.append(f"- `{row['cycle_id']}` {row['block']}")
    if report.get("novelty_high_reward_avenues"):
        lines.extend(["", "## Novelty And High-Reward Avenues", ""])
        for avenue in report["novelty_high_reward_avenues"]:
            lines.extend(
                [
                    f"### {avenue['avenue_id']}",
                    "",
                    f"- Avenue: {avenue['title']}",
                    f"- Novelty signal: {avenue['novelty_signal']}",
                    f"- Reward condition: {avenue['reward_condition']}",
                    f"- Step-back/pivot condition: {avenue['step_back_or_pivot_condition']}",
                    f"- Why it matters: {avenue['why_it_matters']}",
                    "",
                ]
            )
    lines.extend(
        [
            "",
            "## Paper Contribution Readiness",
            "",
            f"- Smallest honest claim: {readiness['smallest_honest_claim']}",
            f"- Novelty argument: {readiness['novelty_argument']}",
            f"- Main problem implication: {readiness['main_problem_implication']}",
            "",
            "## Alignment",
            "",
            f"- Handoff: {alignment['source_to_target_handoff']}",
            f"- Transfer risk: {alignment['proxy_or_transfer_risk']}",
            "",
            "## Next Decisive Test",
            "",
            progression["next_decisive_test"],
            "",
            "## Contribution Pivot Invariant",
            "",
            progression["contribution_pivot_invariant"],
            "",
            "## When To Stop",
            "",
            progression["when_to_stop"],
            "",
            "## Do Not Stop Prematurely If",
            "",
            progression["do_not_stop_prematurely_if"],
            "",
            "## Validation Handoff",
            "",
            markdown_list(report["validation_handoff"]),
        ]
    )
    return "\n".join(lines)


def main() -> int:
    marathon, cycles = load_research_cycles()
    target_id = clean_text(marathon.get("target_id"))
    contribution = load_optional_json(CONTRIBUTION_MONITOR)
    if not target_matches(contribution, target_id):
        contribution = {}
    literature = load_optional_json(TARGET_LITERATURE)
    if not target_matches(literature, target_id):
        literature = {}
    macro = load_optional_json(MACRO_STRATEGY)
    if not target_matches(macro, target_id):
        macro = {}
    report = make_judgement(
        cycles=cycles,
        marathon=marathon,
        contribution=contribution,
        literature=literature,
        macro=macro,
    )
    write_json(OUT_JSON, report)
    write_markdown(OUT_MD, render_markdown(report))
    print(f"wrote {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
