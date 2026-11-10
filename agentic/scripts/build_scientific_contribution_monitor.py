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
"""Build a standing monitor for standalone scientific contribution candidates."""

from __future__ import annotations

import json
from statistics import mean
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, stable_id, utc_now, write_json
from discovery_marathon_common import load_cycles, load_run_state, write_markdown
from target_profiles import target_profile


OUT_DIR = ROOT / "agentic/reports/scientific_contribution_monitor"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
TIMELINE_START_CYCLE = 174
PVSNP_PRESSURE_BRIDGES = ROOT / "agentic/reports/pvsnp_pressure_bridges/latest.json"
PVSNP_NEGATIVE_TACTICS = ROOT / "agentic/reports/pvsnp_negative_tactics/latest.json"

CONTRIBUTION_SKILLS = [
    "scientific-contribution-detector",
    "contribution-value-assessor",
    "paper-contribution-readiness-judge",
    "contribution-oriented-subgoal-manager",
    "scientific-contribution-paper-handoff",
]

STEPPING_STONE_MATURITIES = {
    "contribution_shaped",
    "near_stepping_stone",
    "publishable_handoff_ready",
}


def contains_any(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return any(term in lower for term in terms)


def cycle_number(cycle_id: Any) -> int:
    try:
        return int(clean_text(cycle_id).split("-")[-1])
    except ValueError:
        return 0


def branch_output(cycle: dict[str, Any]) -> dict[str, Any]:
    outputs = cycle.get("branch_outputs", [])
    return outputs[0] if outputs and isinstance(outputs[0], dict) else {}


def first_lemma(output: dict[str, Any]) -> dict[str, Any]:
    lemmas = output.get("candidate_lemmas", [])
    return lemmas[0] if lemmas and isinstance(lemmas[0], dict) else {}


def text_for_cycle(cycle: dict[str, Any]) -> str:
    output = branch_output(cycle)
    lemma = first_lemma(output)
    pieces = [
        cycle.get("cycle_id", ""),
        output.get("branch_title", ""),
        output.get("mathematical_learning", ""),
        output.get("next_experiment", ""),
        output.get("attempted_derivation", {}).get("blocking_gap", ""),
        " ".join(output.get("falsifiers", [])),
        json.dumps(lemma.get("equations", []), ensure_ascii=False),
    ]
    return clean_text(" ".join(str(piece) for piece in pieces))


def infer_contribution_type(text: str) -> str:
    lower = text.lower()
    if contains_any(lower, ["beta", "threshold collapse", "bounded exponent window", "black-box", "projection", "demagnification"]):
        return "quantitative_transfer_obstruction"
    if contains_any(lower, ["mcsp", "mktp", "meta-complexity", "searchable certificate", "succinct certificate"]):
        return "meta_complexity_certificate_bridge"
    if contains_any(lower, ["natural proof", "relativization", "algebrization", "oracle", "barrier", "no-go", "impossibility"]):
        return "route_specific_no_go"
    if contains_any(lower, ["all-exponent", "cofinal", "for every fixed c", "p/poly", "nonuniform", "advice"]):
        return "quantifier_uniformity_lift"
    if contains_any(lower, ["proof-complexity", "proof complexity", "frege", "resolution", "tautology"]):
        return "proof_complexity_certificate_bridge"
    if contains_any(lower, ["falsifier", "counterexample", "determinant", "holonomy", "negative minor", "obstruction"]):
        return "obstruction_or_falsifier"
    if contains_any(lower, ["bridge", "same-theory", "same theory", "os reconstruction", "reflection positivity", "schwinger"]):
        return "bridge_lemma"
    if contains_any(lower, ["quotient", "tangent cone", "schur", "conceptual", "mechanism", "regime", "graph"]):
        return "conceptual_reframing"
    if contains_any(lower, ["finite", "symbolic", "matrix", "probe", "compute", "benchmark"]):
        return "benchmark_or_probe"
    if contains_any(lower, ["skill", "workflow", "monitor", "queue", "validator"]):
        return "method_or_workflow"
    if contains_any(lower, ["evidence", "empirical", "source", "prior art"]):
        return "evidence_synthesis"
    return "contribution_search"


def target_terms(target_id: str) -> dict[str, list[str]]:
    if target_id == "p-vs-np-target":
        return {
            "novelty": [
                "beta",
                "threshold collapse",
                "black-box substitution cap",
                "projection-demagnification",
                "mcsp",
                "mktp",
                "searchable certificate",
                "natural-proof",
                "natural proof",
                "relativization",
                "algebrization",
                "all-exponent",
                "cofinal",
                "proof-complexity",
                "route-specific no-go",
            ],
            "explanation": [
                "because",
                "mechanism",
                "explains",
                "pressure",
                "blocking gap",
                "why",
                "falsifier",
                "barrier",
                "advice",
                "uniform",
                "threshold",
            ],
            "implications": [
                "compute",
                "test",
                "audit",
                "prove",
                "demote",
                "quarantine",
                "certificate",
                "no-go",
                "lower bound",
                "exponent",
            ],
            "relevance": [
                "p vs np",
                "p != np",
                "np",
                "sat",
                "circuit",
                "lower bound",
                "p/poly",
                "e",
                "mcsp",
                "mktp",
                "complexity",
                "uniformity",
                "advice",
            ],
        }
    return {
        "novelty": ["quotient", "tangent cone", "schur", "holonomy", "boundary ope", "same-theory", "obstruction", "finite falsifier"],
        "explanation": ["because", "mechanism", "explains", "pressure", "blocking gap", "why", "falsifier", "regime"],
        "implications": ["next experiment", "compute", "test", "evaluate", "construct", "branch", "quarantine", "handoff"],
        "relevance": ["yang-mills", "wilson", "gauge", "os", "reflection positivity", "spectral", "mass gap", "continuum", "schwinger"],
    }


def dimension_score(text: str, terms: list[str], base: int = 1) -> int:
    score = base
    lower = text.lower()
    for term in terms:
        if term in lower:
            score += 1
    return max(0, min(5, score))


def candidate_scores(text: str, output: dict[str, Any], lemma: dict[str, Any], target_id: str) -> dict[str, int]:
    equation_count = len(lemma.get("equations", []))
    falsifier_count = len(output.get("falsifiers", []))
    step_count = len(output.get("attempted_derivation", {}).get("steps", []))
    terms = target_terms(target_id)
    novelty = dimension_score(text, terms["novelty"])
    explanation = dimension_score(text, terms["explanation"])
    implications = dimension_score(text, terms["implications"])
    validation = min(5, 1 + min(2, equation_count) + min(1, falsifier_count) + min(1, step_count // 3))
    relevance = dimension_score(text, terms["relevance"])
    return {
        "conceptual_novelty": novelty,
        "explanatory_power": explanation,
        "implications": implications,
        "certification_readiness": validation,
        "target_relevance": relevance,
    }


def composite_score(scores: dict[str, int]) -> int:
    weights = {
        "conceptual_novelty": 0.24,
        "explanatory_power": 0.18,
        "implications": 0.20,
        "certification_readiness": 0.22,
        "target_relevance": 0.16,
    }
    return round(sum((scores[key] / 5) * 100 * weight for key, weight in weights.items()))


def status_for(score: int, scores: dict[str, int]) -> str:
    if score >= 82 and scores["certification_readiness"] >= 4:
        return "good_enough_to_handoff"
    if score >= 74 and scores["certification_readiness"] >= 3:
        return "near_certification"
    if score >= 62:
        return "active_candidate"
    if score >= 48:
        return "develop"
    return "watch"


def target_forms(target_id: str) -> list[dict[str, Any]]:
    forms = target_profile(target_id).get("stepping_stone_forms", [])
    return [row for row in forms if isinstance(row, dict)]


def contribution_form(kind: str, target_id: str) -> dict[str, Any]:
    forms = target_forms(target_id)
    aliases = {
        "meta_complexity_certificate_bridge": "searchable_certificate_bridge",
        "proof_complexity_certificate_bridge": "searchable_certificate_bridge",
        "barrier_and_impossibility_control": "route_specific_no_go",
    }
    wanted = aliases.get(kind, kind)
    for form in forms:
        if clean_text(form.get("form")) == wanted:
            return form
    if forms:
        return forms[0]
    return {
        "form": kind,
        "object": "target-preserving contribution candidate",
        "audience": "domain experts",
        "novelty_axis": "bounded scientific value",
        "decisive_validation": "finite validation handoff",
        "disqualifiers": ["proxy problem", "unbounded validation"],
    }


def prior_art_boundary(kind: str, target_id: str) -> dict[str, Any]:
    if target_id == "p-vs-np-target":
        closest = {
            "quantitative_transfer_obstruction": [
                "hardness magnification threshold theorems",
                "natural proofs and algebrization barriers",
                "padding/projection lower-bound transfer arguments",
            ],
            "meta_complexity_certificate_bridge": [
                "MCSP and MKtP hardness/derandomization literature",
                "minimum circuit size and truth-table hardness results",
                "proofs avoiding nonuniform hard-row choice",
            ],
            "proof_complexity_certificate_bridge": [
                "Cook-Reckhow proof systems",
                "resolution/Frege/IPS lower-bound transfer work",
                "proof complexity versus circuit lower-bound connections",
            ],
            "route_specific_no_go": [
                "relativization, natural proofs, and algebrization",
                "restricted-model lower-bound counterexamples",
                "method-specific impossibility theorems",
            ],
            "quantifier_uniformity_lift": [
                "P/poly lower-bound quantifier structure",
                "all-exponent hardness magnification requirements",
                "valid-length and sparse-language transfer issues",
            ],
        }.get(kind, ["complexity lower-bound and barrier literature"])
    else:
        closest = {
            "bridge_lemma": ["Osterwalder-Schrader reconstruction", "constructive QFT bridge lemmas"],
            "obstruction_or_falsifier": ["finite positivity and Schur-complement obstruction criteria"],
            "conceptual_reframing": ["constructive Yang-Mills strategy literature"],
        }.get(kind, ["target-domain literature"])
    return {
        "closest_known_results": closest,
        "what_is_reused": "Existing terminology, known barriers, and standard target commitments must be cited before novelty is claimed.",
        "what_is_new_if_true": "The candidate would be new only insofar as its exact object, obstruction, or bridge is not already present in those result families.",
        "rediscovery_risk": "medium",
        "citation_tasks": [f"Run prior-art pass for {item}." for item in closest[:3]],
        "novelty_status": "finite_check_queued",
    }


def disqualifier_tests(kind: str, text: str, target_id: str, scores: dict[str, int]) -> list[dict[str, str]]:
    tests = [
        {
            "name": "already_known",
            "verdict": "finite_check_queued",
            "evidence": "Prior-art boundary is queued before publishable handoff.",
        },
        {
            "name": "evidence_gap",
            "verdict": "pass" if scores.get("certification_readiness", 0) >= 4 else "finite_check_queued",
            "evidence": "Certification readiness is derived from equations, derivation steps, and falsifiers.",
        },
        {
            "name": "overclaim_risk",
            "verdict": "pass",
            "evidence": "Overclaim boundary explicitly states that the candidate does not prove the main target.",
        },
        {
            "name": "validation_unbounded",
            "verdict": "pass" if contains_any(text, ["compute", "prove", "audit", "test", "derive", "formalize", "falsifier"]) else "finite_check_queued",
            "evidence": "The next action is checked for bounded proof, calculation, audit, or falsifier language.",
        },
        {
            "name": "narrow_bookkeeping",
            "verdict": "pass" if kind != "method_or_workflow" else "finite_check_queued",
            "evidence": "The candidate is treated as scientific only if it has external mathematical content.",
        },
    ]
    if target_id == "p-vs-np-target":
        tests.extend(
            [
                {
                    "name": "target_equivalent_assumption",
                    "verdict": "finite_check_queued",
                    "evidence": "P vs NP candidates must show that the source obligation is not already the desired lower bound.",
                },
                {
                    "name": "advice_leakage",
                    "verdict": "finite_check_queued" if contains_any(text, ["advice", "nonuniform", "hard row", "mcsp", "mktp"]) else "pass",
                    "evidence": "Advice and nonuniform hard-row selection are explicit P vs NP disqualifiers.",
                },
                {
                    "name": "barrier_status",
                    "verdict": "finite_check_queued" if contains_any(text, ["natural", "relativ", "algebr", "barrier"]) else "pass",
                    "evidence": "Barrier status must be attached to the specific transfer theorem.",
                },
                {
                    "name": "restricted_model_proxy_drift",
                    "verdict": "finite_check_queued" if contains_any(text, ["ac0", "obdd", "resolution", "sos", "degree", "streaming", "restricted"]) else "pass",
                    "evidence": "Restricted-model results need a compiler envelope or explicit proxy boundary.",
                },
            ]
        )
    else:
        tests.extend(
            [
                {
                    "name": "proxy_problem",
                    "verdict": "finite_check_queued" if contains_any(text, ["finite", "toy", "proxy", "cutoff"]) else "pass",
                    "evidence": "Finite or proxy objects need a same-theory transfer certificate.",
                },
                {
                    "name": "same_theory_boundary",
                    "verdict": "pass" if contains_any(text, ["same-theory", "wilson", "os", "schwinger"]) else "finite_check_queued",
                    "evidence": "Yang-Mills candidates must keep observable algebra and target theory fixed.",
                },
            ]
        )
    return tests


def handoff_hard_gates(candidate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    scores = candidate.get("scores", {})
    prior = candidate.get("prior_art_boundary", {})
    disqualifiers = candidate.get("disqualifier_tests", [])
    disq_ok = all(row.get("verdict") == "pass" for row in disqualifiers)
    disq_finite = all(row.get("verdict") in {"pass", "finite_check_queued"} for row in disqualifiers)
    return {
        "claim_statement_ready": {
            "ready": bool(clean_text(candidate.get("smallest_honest_claim"))) and candidate.get("contribution_type") != "contribution_search",
            "finite_task": False,
            "evidence": candidate.get("smallest_honest_claim", ""),
        },
        "evidence_ready": {
            "ready": int(scores.get("certification_readiness", 0)) >= 4,
            "finite_task": int(scores.get("certification_readiness", 0)) >= 3,
            "evidence": "; ".join(candidate.get("evidence_basis", [])),
        },
        "novelty_boundary_ready": {
            "ready": prior.get("novelty_status") == "checked",
            "finite_task": bool(prior.get("citation_tasks")),
            "evidence": "; ".join(prior.get("closest_known_results", [])),
        },
        "validation_ready": {
            "ready": disq_ok and int(scores.get("certification_readiness", 0)) >= 4,
            "finite_task": disq_finite,
            "evidence": "; ".join(f"{row.get('name')}={row.get('verdict')}" for row in disqualifiers),
        },
        "overclaim_boundary_ready": {
            "ready": "does not prove the main target" in clean_text(candidate.get("overclaim_boundary")).lower(),
            "finite_task": False,
            "evidence": candidate.get("overclaim_boundary", ""),
        },
    }


def maturity_from_gates(gates: dict[str, dict[str, Any]]) -> str:
    if all(gate.get("ready") for gate in gates.values()):
        return "publishable_handoff_ready"
    if gates["claim_statement_ready"]["ready"] and gates["evidence_ready"].get("finite_task") and gates["novelty_boundary_ready"].get("finite_task"):
        return "near_stepping_stone"
    if gates["claim_statement_ready"]["ready"]:
        return "contribution_shaped"
    return "contribution_shaped"


def status_from_maturity(maturity: str, score: int) -> str:
    if maturity == "publishable_handoff_ready":
        return "good_enough_to_handoff"
    if maturity == "near_stepping_stone":
        return "near_certification"
    if score >= 62:
        return "active_candidate"
    if score >= 48:
        return "develop"
    return "watch"


def missing_to_publishable(gates: dict[str, dict[str, Any]]) -> list[str]:
    labels = {
        "claim_statement_ready": "Write the smallest honest theorem/result claim in paper style.",
        "evidence_ready": "Add or cite a bounded derivation, computation, falsifier, or source-backed evidence table.",
        "novelty_boundary_ready": "Run the finite prior-art boundary check and record closest known results.",
        "validation_ready": "Resolve disqualifier tests or convert unknowns into finite validation tasks.",
        "overclaim_boundary_ready": "State what the result does not prove about the main target.",
    }
    missing = []
    for key, gate in gates.items():
        if gate.get("ready"):
            continue
        missing.append(labels[key])
    return missing


def paper_note_shape(candidate: dict[str, Any], form: dict[str, Any]) -> dict[str, Any]:
    claim = clean_text(candidate.get("smallest_honest_claim"))
    title = clean_text(candidate.get("branch_title")) or clean_text(candidate.get("candidate_id"))
    return {
        "title": f"Stepping-stone note: {title}",
        "abstract_claim": claim,
        "theorem_or_result_statement": claim,
        "definitions_needed": [
            clean_text(form.get("object")),
            "source object and target object",
            "validity regime and model assumptions",
        ],
        "proof_plan": [
            "State the contribution object and assumptions.",
            "Present the derivation, calculation, falsifier, or source-backed evidence.",
            "Check disqualifiers and prior-art boundary.",
            "State implications and non-claims.",
        ],
        "figures_or_tables": [
            "claim-to-evidence table",
            "disqualifier and prior-art boundary table",
            "route implication diagram",
        ],
        "relation_to_main_problem": clean_text(candidate.get("implication_map", {}).get("route_level")),
        "limitations": [candidate.get("overclaim_boundary", "")],
        "next_validation_artifacts": candidate.get("validation_burden", []),
    }


def publishable_subgoal_score(scores: dict[str, int], gates: dict[str, dict[str, Any]]) -> int:
    base = composite_score(scores)
    ready_bonus = sum(8 for gate in gates.values() if gate.get("ready"))
    finite_bonus = sum(3 for gate in gates.values() if not gate.get("ready") and gate.get("finite_task"))
    unknown_penalty = sum(8 for gate in gates.values() if not gate.get("ready") and not gate.get("finite_task"))
    return max(0, min(100, round(base * 0.55 + ready_bonus + finite_bonus - unknown_penalty)))


def paper_relevance_criteria(target_id: str) -> list[dict[str, Any]]:
    criteria = target_profile(target_id).get("paper_relevance_criteria", [])
    return [row for row in criteria if isinstance(row, dict)]


def marker_status(score: int, *, hard_gate_ready: bool = False) -> str:
    if score >= 5 and hard_gate_ready:
        return "paper_ready"
    if score >= 4:
        return "strong"
    if score >= 3:
        return "adequate"
    if score >= 2:
        return "weak"
    return "absent"


def bounded_term_hits(text: str, terms: list[str], limit: int = 2) -> int:
    lower = text.lower()
    return min(limit, sum(1 for term in terms if term.lower() in lower))


def marker_score(
    dimension: str,
    text: str,
    scores: dict[str, int],
    gates: dict[str, dict[str, Any]],
    prior: dict[str, Any],
    disqualifiers: list[dict[str, str]],
    form: dict[str, Any],
    terms: list[str],
) -> int:
    hits = bounded_term_hits(text, terms, 2)
    finite_disqualifiers = all(row.get("verdict") in {"pass", "finite_check_queued"} for row in disqualifiers)
    if dimension == "conceptual_depth":
        return min(5, 1 + hits + int(scores.get("certification_readiness", 0) >= 4) + int(scores.get("target_relevance", 0) >= 4))
    if dimension == "conceptual_novelty":
        novelty_cap = 5 if prior.get("novelty_status") == "checked" else 4
        return min(novelty_cap, 1 + hits + int(scores.get("conceptual_novelty", 0) >= 4) + int(bool(clean_text(form.get("novelty_axis")))))
    if dimension == "unblocking_power":
        return min(5, 1 + hits + int(scores.get("implications", 0) >= 4) + int(finite_disqualifiers) + int(gates.get("validation_ready", {}).get("finite_task")))
    if dimension == "applicability":
        return min(5, 1 + hits + int(scores.get("target_relevance", 0) >= 4) + int(bool(clean_text(form.get("audience")))) + int(bool(clean_text(form.get("decisive_validation")))))
    if dimension == "understanding_gain":
        return min(5, 1 + hits + int(scores.get("explanatory_power", 0) >= 4) + int(scores.get("implications", 0) >= 4))
    return min(5, 1 + hits)


def paper_relevance_markers(
    *,
    target_id: str,
    text: str,
    scores: dict[str, int],
    gates: dict[str, dict[str, Any]],
    prior: dict[str, Any],
    disqualifiers: list[dict[str, str]],
    form: dict[str, Any],
) -> list[dict[str, Any]]:
    markers = []
    gate_ready = all(packet.get("ready") for packet in gates.values())
    for criterion in paper_relevance_criteria(target_id):
        dimension = clean_text(criterion.get("dimension"))
        terms = [clean_text(term) for term in criterion.get("strong_signals", []) if clean_text(term)]
        score = marker_score(dimension, text, scores, gates, prior, disqualifiers, form, terms)
        markers.append(
            {
                "dimension": dimension,
                "score": score,
                "status": marker_status(score, hard_gate_ready=gate_ready),
                "criterion": clean_text(criterion.get("good_enough")),
                "problem_space_specificity": "P vs NP complexity-theory relevance marker" if target_id == "p-vs-np-target" else "target-specific paper relevance marker",
                "evidence": {
                    "strong_signal_hits": [term for term in terms if term.lower() in text.lower()],
                    "score_basis": f"dimension={dimension}; marker_score={score}; novelty_status={prior.get('novelty_status', '')}; form={form.get('form', '')}",
                },
                "missing_for_good_enough": "" if score >= 4 else clean_text(criterion.get("missing_if_weak")),
            }
        )
    return markers


def good_enough_paper_relevance(markers: list[dict[str, Any]], gates: dict[str, dict[str, Any]]) -> dict[str, Any]:
    scores = [int(marker.get("score", 0)) for marker in markers]
    average = round(mean(scores), 1) if scores else 0
    by_dimension = {marker.get("dimension"): int(marker.get("score", 0)) for marker in markers}
    all_gates_ready = all(packet.get("ready") for packet in gates.values())
    decisive_dimensions = ["conceptual_depth", "unblocking_power", "understanding_gain"]
    decisive_strong = all(by_dimension.get(name, 0) >= 4 for name in decisive_dimensions)
    all_adequate = all(score >= 3 for score in scores) if scores else False
    if all_gates_ready and all_adequate and average >= 4:
        status = "paper_relevance_ready"
    elif all_adequate and average >= 4 and decisive_strong:
        status = "strong_relevance_certification_pending"
    elif all_adequate:
        status = "moderate_relevance_needs_sharpening"
    else:
        status = "weak_relevance"
    missing = [marker.get("missing_for_good_enough") for marker in markers if clean_text(marker.get("missing_for_good_enough"))]
    if not all_gates_ready:
        missing.append("Close the publishable handoff hard gates before calling the candidate paper-ready.")
    return {
        "status": status,
        "average_marker_score": average,
        "decisive_dimensions_strong": decisive_strong,
        "all_dimensions_adequate": all_adequate,
        "all_hard_gates_ready": all_gates_ready,
        "missing_for_good_enough_paper": missing,
        "paper_relevance_decision": (
            "The candidate is scientifically relevant enough to shape a paper, but certification/prior-art gates still control handoff."
            if status == "strong_relevance_certification_pending"
            else "The candidate is paper-relevance ready; move to validation and manuscript packaging."
            if status == "paper_relevance_ready"
            else "Sharpen the paper relevance markers before treating this as a good-enough paper subgoal."
        ),
    }


def smallest_honest_claim(kind: str, output: dict[str, Any], target_id: str) -> str:
    branch = clean_text(output.get("branch_title")) or "the active branch"
    if target_id == "p-vs-np-target":
        mapping = {
            "quantitative_transfer_obstruction": f"A route-specific quantitative obstruction can be isolated for {branch}: the transfer formula names the source exponent, overhead, target-query exponent, and exact threshold where magnification collapses.",
            "meta_complexity_certificate_bridge": f"A searchable meta-complexity certificate bridge can be stated for {branch}, with verifier, decoder, certificate length, search time, gap coverage, and advice-free soundness as the claim boundary.",
            "route_specific_no_go": f"A bounded no-go theorem can be formulated for {branch}, identifying the method-class assumptions under which relativization, naturalness, algebrization, advice leakage, or threshold collapse blocks the route.",
            "quantifier_uniformity_lift": f"A quantifier-lift obligation can be isolated for {branch}: a fixed exponent-window result is not enough unless a cofinal all-exponent family preserves uniformity and valid lengths.",
            "proof_complexity_certificate_bridge": f"A proof-complexity certificate bridge can be scoped for {branch}, separating proof-system evidence, semantic lower-bound soundness, verifier overhead, and target-class transfer.",
        }
        if kind in mapping:
            return mapping[kind]
    if kind == "obstruction_or_falsifier":
        return f"A bounded obstruction criterion can be isolated for {branch}, sufficient to decide continuation, backtracking, or quarantine without claiming the main theorem."
    if kind == "bridge_lemma":
        return f"A same-theory bridge lemma for {branch} can be stated with explicit source object, target object, assumptions, and validation burden."
    if kind == "conceptual_reframing":
        return f"The branch reframes the hypothesis space around a sharper mechanism that changes which subclaims, variables, or regimes should be tested next."
    if kind == "benchmark_or_probe":
        return f"A reusable finite or symbolic probe can test a proof-relevant mechanism under named assumptions and falsifier conditions."
    if kind == "method_or_workflow":
        return f"A reusable discovery-control method can keep long-horizon exploration tied to contribution candidates, stop criteria, and validation handoffs."
    if kind == "evidence_synthesis":
        return f"A source-backed evidence packet can change the plausibility or priority of a target-preserving route."
    return "A contribution-shaped subgoal has not yet been named; the next move must search for a bridge, obstruction, probe, reframing, or evidence packet."


def why_standalone(kind: str) -> str:
    mapping = {
        "quantitative_transfer_obstruction": "A quantitative transfer obstruction is independently useful because it replaces barrier folklore with an exact parameter condition showing when a proof route loses the target exponent.",
        "meta_complexity_certificate_bridge": "A searchable certificate bridge is independently useful because it identifies the precise carrier that could avoid advice-selected hard strings while still producing lower-bound evidence.",
        "route_specific_no_go": "A route-specific no-go theorem is independently useful because it tells researchers which method class cannot deliver P vs NP-level consequences and which escape conditions remain live.",
        "quantifier_uniformity_lift": "A quantifier-lift criterion is independently useful because it distinguishes bounded-window magnification from the all-exponent separation needed for nonuniform lower bounds.",
        "proof_complexity_certificate_bridge": "A proof-complexity bridge is independently useful when it turns semantic hardness evidence into verifiable objects without merely renaming the target lower bound.",
        "obstruction_or_falsifier": "A negative criterion is independently useful because it prevents wasted proof effort and gives other researchers a finite test for route failure.",
        "bridge_lemma": "A bridge lemma is independently useful because it exposes the exact transfer obligation between two mathematical regimes.",
        "conceptual_reframing": "A conceptual reframing is independently useful when it reorganizes the search space and explains why prior route families stalled.",
        "benchmark_or_probe": "A controlled probe is independently useful because it gives a reusable diagnostic object with explicit validity limits.",
        "method_or_workflow": "A workflow contribution is independently useful only when it demonstrably improves exploration control, validation, and anti-drift behavior.",
        "evidence_synthesis": "An evidence packet is independently useful when it changes route plausibility under explicit source and transport limits.",
        "contribution_search": "It is not yet standalone; usefulness depends on whether the next cycle can name a concrete contribution object.",
    }
    return mapping[kind]


def branch_control(status: str, score: int, scores: dict[str, int]) -> dict[str, Any]:
    if status == "good_enough_to_handoff":
        decision = "handoff"
        reason = "The smallest honest contribution claim is clear enough that more exploration risks churn; move to validation, prior-art, or paper packaging."
    elif status == "near_certification":
        decision = "continue_for_bounded_certification"
        reason = "The candidate is strong but still needs bounded validation or disqualifier checks before handoff."
    elif status == "active_candidate":
        decision = "continue_or_adapt"
        reason = "The candidate is live and contribution-shaped; keep it active only if the next cycle improves a monitored dimension."
    elif status == "develop":
        decision = "adapt"
        reason = "The candidate has value pressure but needs sharper mathematical object, evidence, or implications before long-run budget."
    else:
        decision = "stop_or_quarantine_after_repeat_low_payoff"
        reason = "The branch is not yet contribution-shaped; stop after repeated failed sharpening unless it touches an essential target commitment."
    return {
        "branch_control_decision": decision,
        "branch_control_reason": reason,
        "good_enough_when": [
            "Smallest honest claim can be stated without proving the main target.",
            "Mathematical object, assumptions, scope, and evidence basis are explicit.",
            "At least one disqualifier or falsifier has been checked or bounded.",
            "Remaining validation is finite enough for a paper note, obstruction note, benchmark, method note, or lemma packet.",
        ],
        "continue_only_if": [
            "The next cycle can improve novelty, explanation, implications, validation readiness, target relevance, or disqualifier resolution.",
            "The branch still touches a core target commitment or a reusable scientific object.",
            "The next action is a bounded calculation, derivation, source check, or falsifier test rather than generic elaboration.",
        ],
        "stop_when": [
            "Two explicit adaptation or backtracking attempts fail to improve any contribution metric.",
            "The branch cannot name a contribution candidate, contribution-disqualifying test, or target-preserving validation handoff.",
            "The candidate is already good enough for handoff and further exploration would only inflate proof debt.",
        ],
        "infinite_progression_risk": (
            "high" if score < 50 else "medium" if scores["certification_readiness"] <= 2 else "low"
        ),
    }


def target_pivot_control_policy(target_id: str) -> dict[str, Any]:
    if target_id == "p-vs-np-target":
        return {
            "novelty_signal_definition": "Novelty is signalled by a new controlled complexity object or exact obstruction: beta/q/a transfer calculus, searchable MCSP/MKtP certificates, sparse non-natural properties, proof-system carriers, or all-exponent quantifier lifts.",
            "high_reward_definition": "High reward means the next analysis could either produce a paper-level bridge/no-go lemma or eliminate an entire method family with a precise parameter condition.",
            "persist_if": [
                "A named source object, target object, and controlled interface are present.",
                "The next step computes a parameter, certificate condition, proof-system overhead, or barrier premise rather than restating route ambition.",
                "The branch can still alter route priority for P vs NP, NP not subset P/poly, or an explicitly scoped lower-bound consequence.",
            ],
            "backtrack_if": [
                "The branch imports advice, nonuniform hard strings, sparse valid lengths, or an unproved carrier before stating a transfer certificate.",
                "The source lower bound is already as hard as the target lower bound.",
                "A barrier is named but the exact premise that applies or fails is not typed.",
            ],
            "pivot_or_quarantine_if": [
                "Two sharpened attempts leave only a bounded exponent window when the target needs all exponents.",
                "The certificate existence condition is equivalent to the desired lower bound.",
                "The route remains natural, relativizing, or algebrizing under its own stated proof object.",
                "The next action cannot name a validation handoff, falsifier, or paper-level obstruction value.",
            ],
        }
    return {
        "novelty_signal_definition": "Novelty is signalled by a new target-preserving bridge, obstruction, calculation, or validation handoff.",
        "high_reward_definition": "High reward means the next analysis can produce a paper-level lemma, obstruction, worked calculation, or demotion of a route family.",
        "persist_if": ["A named source object, target object, and controlled interface are present."],
        "backtrack_if": ["A premise is imported before it is constructed or certified."],
        "pivot_or_quarantine_if": ["Repeated sharpening does not improve target alignment, validation readiness, or contribution value."],
    }


def high_reward_signals(target_id: str, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if target_id != "p-vs-np-target":
        return []
    pressure = load_optional_json(PVSNP_PRESSURE_BRIDGES)
    bridges = pressure.get("bridge_candidates", []) if isinstance(pressure.get("bridge_candidates"), list) else []
    rows = []
    for bridge in sorted(bridges, key=lambda row: -int(row.get("priority_score", 0)))[:4]:
        rows.append(
            {
                "signal_id": clean_text(bridge.get("id")),
                "avenue": clean_text(bridge.get("title")),
                "novelty_signal": clean_text(bridge.get("bridge_abstraction")),
                "why_high_reward": clean_text(bridge.get("paper_safe_narrative") or bridge.get("difficulty_hypothesis")),
                "payoff_criterion": clean_text(bridge.get("proof_obligation")),
                "pivot_or_backtrack_criterion": clean_text(bridge.get("when_to_pivot")),
                "validation_handoff": bridge.get("validation_handoff", []),
            }
        )
    for candidate in candidates[:2]:
        rows.append(
            {
                "signal_id": clean_text(candidate.get("candidate_id")),
                "avenue": clean_text(candidate.get("branch_title")),
                "novelty_signal": clean_text(candidate.get("smallest_honest_claim")),
                "why_high_reward": clean_text(candidate.get("why_it_could_stand_alone")),
                "payoff_criterion": clean_text(candidate.get("validation_burden", [""])[0] if candidate.get("validation_burden") else ""),
                "pivot_or_backtrack_criterion": "; ".join(candidate.get("stop_when", [])[:2]),
                "validation_handoff": candidate.get("required_skills", []),
            }
        )
    tactics = load_optional_json(PVSNP_NEGATIVE_TACTICS)
    for row in tactics.get("recommendations", []) if isinstance(tactics.get("recommendations"), list) else []:
        if not isinstance(row, dict):
            continue
        if row.get("tactic_mode") not in {"impossibility_theorem", "proof_by_contradiction", "falsifier_search"}:
            continue
        rows.append(
            {
                "signal_id": clean_text(row.get("recommendation_id")),
                "avenue": clean_text(row.get("branch_title") or row.get("route_family")),
                "novelty_signal": clean_text(row.get("exact_negation_or_method_class")),
                "why_high_reward": clean_text(row.get("paper_contribution_potential")),
                "payoff_criterion": "; ".join(row.get("proof_obligations", [])[:2]),
                "pivot_or_backtrack_criterion": "; ".join(row.get("escape_conditions", [])[:2]),
                "validation_handoff": [clean_text(row.get("next_validation_handoff"))],
            }
        )
    return rows


def negative_tactic_candidate(row: dict[str, Any]) -> dict[str, Any]:
    kind = "route_specific_no_go" if row.get("tactic_mode") == "impossibility_theorem" else "obstruction_or_falsifier"
    if row.get("tactic_mode") == "proof_by_contradiction":
        kind = "quantitative_transfer_obstruction"
    text = clean_text(row)
    scores = {
        "conceptual_novelty": 4 if row.get("tactic_mode") == "impossibility_theorem" else 3,
        "explanatory_power": 4,
        "implications": 4,
        "certification_readiness": 3,
        "target_relevance": 5,
    }
    score = composite_score(scores)
    form = contribution_form(kind, "p-vs-np-target")
    prior = prior_art_boundary(kind, "p-vs-np-target")
    disqualifiers = disqualifier_tests(kind, text, "p-vs-np-target", scores)
    title = clean_text(row.get("branch_title") or row.get("route_family"))
    claim = (
        f"A scoped {row.get('tactic_mode')} contribution can be formulated for {title}: "
        f"{clean_text(row.get('exact_negation_or_method_class'))} has carrier "
        f"{clean_text(row.get('contradiction_carrier_or_no_go_family'))} and conflict target "
        f"{clean_text(row.get('conflict_target'))}."
    )
    base_candidate = {
        "candidate_id": stable_id("contribution.neg", row.get("recommendation_id", ""), title, row.get("tactic_mode", "")),
        "cycle_id": clean_text(row.get("source_cycle_ids", ["negative-tactic"])[-1] if row.get("source_cycle_ids") else "negative-tactic"),
        "cycle_number": 0,
        "branch_title": title,
        "contribution_type": kind,
        "score": score,
        "scores": scores,
        "smallest_honest_claim": claim,
        "why_it_could_stand_alone": why_standalone(kind),
        "evidence_basis": [
            f"route_family:{clean_text(row.get('route_family'))}",
            f"tactic_mode:{clean_text(row.get('tactic_mode'))}",
            f"escape_conditions:{len(row.get('escape_conditions', []))}",
            f"proof_obligations:{len(row.get('proof_obligations', []))}",
        ],
        "validation_burden": row.get("proof_obligations", []) or ["State the theorem and run a bounded disqualifier check."],
        "overclaim_boundary": "This candidate is a scoped contribution candidate; it does not prove the main target unless all target commitments are discharged in the same theory.",
        "implication_map": {
            "immediate_next_analysis": clean_text(row.get("next_validation_handoff")),
            "route_level": clean_text(row.get("reason_for_tactic")),
            "paper_level": clean_text(row.get("paper_contribution_potential")),
        },
        "required_skills": CONTRIBUTION_SKILLS + [
            "pvsnp-negative-tactic-selector",
            "pvsnp-impossibility-theorem-forger",
            "contradiction-route-auditor",
        ],
    }
    gates = handoff_hard_gates({**base_candidate, "prior_art_boundary": prior, "disqualifier_tests": disqualifiers})
    maturity = maturity_from_gates(gates)
    publishable_score = min(score, publishable_subgoal_score(scores, gates))
    status = status_from_maturity(maturity, score)
    control = branch_control(status, score, scores)
    relevance_markers = paper_relevance_markers(
        target_id="p-vs-np-target",
        text=text,
        scores=scores,
        gates=gates,
        prior=prior,
        disqualifiers=disqualifiers,
        form=form,
    )
    paper_relevance = good_enough_paper_relevance(relevance_markers, gates)
    candidate = {
        **base_candidate,
        "status": status,
        "stepping_stone_maturity": maturity,
        "exploration_payoff_score": score,
        "publishable_subgoal_score": publishable_score,
        "paper_relevance_markers": relevance_markers,
        "good_enough_paper_relevance": paper_relevance,
        "missing_to_good_enough_paper": paper_relevance.get("missing_for_good_enough_paper", []),
        "target_specific_form": form,
        "prior_art_boundary": prior,
        "disqualifier_tests": disqualifiers,
        "handoff_hard_gates": gates,
        "missing_to_publishable": missing_to_publishable(gates),
        "certification_blockers": [
            item for item in missing_to_publishable(gates) if "prior-art" in item.lower() or "disqualifier" in item.lower() or "validation" in item.lower()
        ],
        **control,
    }
    candidate["paper_note_shape"] = paper_note_shape(candidate, form)
    candidate["why_this_budget_now"] = "Run bounded theorem/counterexample certification before another broad exploration cycle."
    return candidate


def negative_tactic_candidates(target_id: str) -> list[dict[str, Any]]:
    if target_id != "p-vs-np-target":
        return []
    packet = load_optional_json(PVSNP_NEGATIVE_TACTICS)
    rows = []
    for row in packet.get("recommendations", []) if isinstance(packet.get("recommendations"), list) else []:
        if isinstance(row, dict) and row.get("tactic_mode") in {"impossibility_theorem", "proof_by_contradiction", "falsifier_search"}:
            rows.append(negative_tactic_candidate(row))
    return rows


def build_candidate(cycle: dict[str, Any], target_id: str) -> dict[str, Any] | None:
    if not cycle.get("valid_as_research_cycle"):
        return None
    output = branch_output(cycle)
    if not output:
        return None
    lemma = first_lemma(output)
    text = text_for_cycle(cycle)
    if not text:
        return None
    kind = infer_contribution_type(text)
    scores = candidate_scores(text, output, lemma, target_id)
    score = composite_score(scores)
    cycle_id = clean_text(cycle.get("cycle_id"))
    evidence = [
        f"cycle:{cycle_id}",
        f"branch:{clean_text(output.get('branch_title'))}",
        f"equations:{len(lemma.get('equations', []))}",
        f"derivation_steps:{len(output.get('attempted_derivation', {}).get('steps', []))}",
        f"falsifiers:{len(output.get('falsifiers', []))}",
    ]
    form = contribution_form(kind, target_id)
    prior = prior_art_boundary(kind, target_id)
    disqualifiers = disqualifier_tests(kind, text, target_id, scores)
    validation_burden = []
    if scores["certification_readiness"] < 4:
        validation_burden.append("Add a bounded validation or disqualifier check before certification.")
    if scores["conceptual_novelty"] >= 4:
        validation_burden.append("Run prior-art comparison before claiming novelty.")
    if scores["target_relevance"] < 4:
        validation_burden.append(
            "Re-state the target-preserving complexity-class relation to avoid proxy drift."
            if target_id == "p-vs-np-target"
            else "Re-state the same-theory target relation to avoid proxy drift."
        )
    if not validation_burden:
        validation_burden.append("Package the evidence table and prior-art boundary for handoff.")
    base_candidate = {
        "candidate_id": stable_id("contribution", cycle_id, output.get("branch_title", ""), kind),
        "cycle_id": cycle_id,
        "cycle_number": cycle_number(cycle_id),
        "branch_title": output.get("branch_title", ""),
        "contribution_type": kind,
        "score": score,
        "scores": scores,
        "smallest_honest_claim": smallest_honest_claim(kind, output, target_id),
        "why_it_could_stand_alone": why_standalone(kind),
        "evidence_basis": evidence,
        "validation_burden": validation_burden,
        "overclaim_boundary": "This candidate is a scoped contribution candidate; it does not prove the main target unless all target commitments are discharged in the same theory.",
        "implication_map": {
            "immediate_next_analysis": output.get("next_experiment", ""),
            "route_level": "Use the candidate to decide whether to continue, adapt, backtrack, quarantine, stop, or hand off the branch.",
            "paper_level": "If certification succeeds, draft a scoped note around the smallest honest claim and evidence table.",
        },
        "required_skills": CONTRIBUTION_SKILLS,
    }
    gates = handoff_hard_gates({**base_candidate, "prior_art_boundary": prior, "disqualifier_tests": disqualifiers})
    maturity = maturity_from_gates(gates)
    publishable_score = publishable_subgoal_score(scores, gates)
    status = status_from_maturity(maturity, score)
    control = branch_control(status, score, scores)
    relevance_markers = paper_relevance_markers(
        target_id=target_id,
        text=text,
        scores=scores,
        gates=gates,
        prior=prior,
        disqualifiers=disqualifiers,
        form=form,
    )
    paper_relevance = good_enough_paper_relevance(relevance_markers, gates)
    candidate = {
        **base_candidate,
        "status": status,
        "stepping_stone_maturity": maturity,
        "exploration_payoff_score": score,
        "publishable_subgoal_score": publishable_score,
        "paper_relevance_markers": relevance_markers,
        "good_enough_paper_relevance": paper_relevance,
        "missing_to_good_enough_paper": paper_relevance.get("missing_for_good_enough_paper", []),
        "target_specific_form": form,
        "prior_art_boundary": prior,
        "disqualifier_tests": disqualifiers,
        "handoff_hard_gates": gates,
        "missing_to_publishable": missing_to_publishable(gates),
        "certification_blockers": [
            item for item in missing_to_publishable(gates) if "prior-art" in item.lower() or "disqualifier" in item.lower() or "validation" in item.lower()
        ],
        **control,
    }
    candidate["paper_note_shape"] = paper_note_shape(candidate, form)
    candidate["why_this_budget_now"] = (
        "Switch to validation or paper packaging; broad exploration risks churn."
        if maturity == "publishable_handoff_ready"
        else "Run the next bounded certification or prior-art gate before another broad marathon branch."
        if maturity == "near_stepping_stone"
        else "Continue exploration only if it sharpens the contribution object or a disqualifier."
    )
    return candidate


def build_report(target_id: str | None = None) -> dict[str, Any]:
    requested_target = clean_text(target_id)
    _, run_state = load_run_state(target_id=requested_target or None)
    if requested_target:
        target_id = requested_target
    else:
        target_id = clean_text(run_state.get("target_id")) if run_state else ""
    raw_cycles = load_cycles(run_state) if run_state else []
    candidates = [candidate for cycle in raw_cycles if (candidate := build_candidate(cycle, target_id))]
    candidates.extend(negative_tactic_candidates(target_id))
    candidates.sort(key=lambda row: (-int(row["score"]), -int(row["cycle_number"])))
    active = [row for row in candidates if row["status"] in {"active_candidate", "near_certification", "good_enough_to_handoff"}]
    contribution_shaped = [row for row in candidates if row.get("stepping_stone_maturity") == "contribution_shaped"]
    near = [row for row in candidates if row.get("stepping_stone_maturity") == "near_stepping_stone"]
    good_enough = [row for row in candidates if row.get("stepping_stone_maturity") == "publishable_handoff_ready"]
    latest_cycle = max([row["cycle_number"] for row in candidates], default=0)
    latest_improved = max([row["cycle_number"] for row in active], default=0)
    avg_score = round(mean(row["score"] for row in candidates), 1) if candidates else 0
    top = candidates[0] if candidates else {}
    metrics = {
        "active_candidate_count": len(active),
        "certification_ready_count": len(near) + len(good_enough),
        "good_enough_count": len(good_enough),
        "contribution_shaped_count": len(contribution_shaped),
        "near_stepping_stone_count": len(near),
        "publishable_handoff_count": len(good_enough),
        "average_contribution_score": avg_score,
        "average_publishable_subgoal_score": round(mean(row.get("publishable_subgoal_score", 0) for row in candidates), 1) if candidates else 0,
        "average_paper_relevance_marker_score": round(mean(row.get("good_enough_paper_relevance", {}).get("average_marker_score", 0) for row in candidates), 1) if candidates else 0,
        "strong_paper_relevance_candidate_count": len(
            [row for row in candidates if row.get("good_enough_paper_relevance", {}).get("status") == "strong_relevance_certification_pending"]
        ),
        "paper_relevance_ready_count": len([row for row in candidates if row.get("good_enough_paper_relevance", {}).get("status") == "paper_relevance_ready"]),
        "novelty_pressure": max([row["scores"]["conceptual_novelty"] for row in candidates], default=0),
        "explanatory_gain": max([row["scores"]["explanatory_power"] for row in candidates], default=0),
        "implication_payoff": max([row["scores"]["implications"] for row in candidates], default=0),
        "staleness": max(0, latest_cycle - latest_improved),
        "infinite_progression_risk_count": len([row for row in candidates if row["infinite_progression_risk"] == "high"]),
    }
    if good_enough:
        aim_status = "handoff_ready"
        objective = "Stop exploratory cycling on the strongest good-enough candidate and produce validation, prior-art, and paper handoff artifacts."
    elif near:
        aim_status = "near_stepping_stone_available"
        objective = "Run the best near-stepping-stone candidate through prior-art, disqualifier, or paper-shape certification before broad exploration."
    elif active:
        aim_status = "active_candidate_available"
        objective = "Run the best active candidate through a bounded sharpening, validation, or disqualifier step."
    else:
        aim_status = "contribution_search_needed"
        objective = "Force the next cycle to search for a bridge lemma, obstruction, reusable probe, conceptual reframing, method contribution, or evidence packet."
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": target_id,
        "source_artifacts": [
            "agentic/runs/discovery_marathons/active_run.json",
            "agentic/reports/discovery_marathon/latest.json",
            "agentic/reports/discovery_marathon/full_timeline.html",
        ],
        "timeline_start_cycle": TIMELINE_START_CYCLE,
        "loop_policy": {
            "standing_objective": "Every long-horizon branch must aim at a standalone scientific contribution candidate, a contribution-search move, or an explicit demotion test.",
            "good_enough_definition": "A candidate is good enough only when its claim, evidence, novelty boundary, validation/disqualifier checks, and overclaim boundary are explicit enough for publishable handoff.",
            "good_enough_paper_relevance_definition": (
                "A paper subgoal is good enough only when conceptual depth, conceptual novelty, unblocking power, applicability, "
                "and understanding gain are at least adequate, the decisive dimensions are strong, and hard gates prevent overclaiming."
            ),
            "paper_relevance_marker_criteria": {
                row.get("dimension"): row.get("good_enough")
                for row in paper_relevance_criteria(target_id)
                if clean_text(row.get("dimension"))
            },
            "stepping_stone_maturity_levels": {
                "contribution_shaped": "The branch has an independently meaningful object or obstruction, but it is not yet a publishable stepping stone.",
                "near_stepping_stone": "One or two bounded prior-art, disqualifier, proof-shape, or validation tasks could make the candidate paper-note ready.",
                "publishable_handoff_ready": "Broad exploration should pause; the candidate should move to validation, prior-art, and manuscript packaging.",
            },
            "anti_infinite_progression_rule": "A branch may continue only while the next cycle can improve a contribution metric or resolve a disqualifier; otherwise adapt, backtrack, quarantine, stop, or hand off.",
            "target_pivot_control": target_pivot_control_policy(target_id),
        },
        "novelty_high_reward_signals": high_reward_signals(target_id, candidates),
        "contribution_aim_status": aim_status,
        "next_contribution_objective": objective,
        "metrics": metrics,
        "validation_gap": top.get("validation_burden", ["No candidate available."])[0] if top else "No candidate available.",
        "top_candidate": top,
        "candidates": candidates[:12],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Scientific Contribution Monitor",
        "",
        f"- Target: `{report.get('target_id', '')}`",
        f"- Status: `{report['contribution_aim_status']}`",
        f"- Next contribution objective: {report['next_contribution_objective']}",
        f"- Good-enough definition: {report['loop_policy']['good_enough_definition']}",
        f"- Good-enough paper relevance definition: {report['loop_policy']['good_enough_paper_relevance_definition']}",
        f"- Anti-infinite progression rule: {report['loop_policy']['anti_infinite_progression_rule']}",
        "",
        "## Paper Relevance Marker Criteria",
        "",
    ]
    for key, value in report["loop_policy"].get("paper_relevance_marker_criteria", {}).items():
        lines.append(f"- `{key}`: {value}")
    lines.extend([
        "",
        "## Stepping-Stone Maturity Levels",
        "",
    ])
    for key, value in report["loop_policy"].get("stepping_stone_maturity_levels", {}).items():
        lines.append(f"- `{key}`: {value}")
    lines.extend([
        "## Metrics",
        "",
    ])
    for key, value in report["metrics"].items():
        lines.append(f"- `{key}`: `{value}`")
    if report.get("novelty_high_reward_signals"):
        lines.extend(["", "## Novelty And High-Reward Signals", ""])
        for signal in report["novelty_high_reward_signals"]:
            lines.extend(
                [
                    f"### {signal['signal_id']}",
                    "",
                    f"- Avenue: {signal['avenue']}",
                    f"- Novelty signal: {signal['novelty_signal']}",
                    f"- Why high reward: {signal['why_high_reward']}",
                    f"- Payoff criterion: {signal['payoff_criterion']}",
                    f"- Pivot/backtrack criterion: {signal['pivot_or_backtrack_criterion']}",
                    "",
                ]
            )
    control = report.get("loop_policy", {}).get("target_pivot_control", {})
    if control:
        lines.extend(
            [
                "",
                "## Target-Specific Pivot Control",
                "",
                f"- Novelty signal definition: {control.get('novelty_signal_definition', '')}",
                f"- High-reward definition: {control.get('high_reward_definition', '')}",
                "- Persist if:",
            ]
        )
        lines.extend(f"  - {item}" for item in control.get("persist_if", []))
        lines.append("- Backtrack if:")
        lines.extend(f"  - {item}" for item in control.get("backtrack_if", []))
        lines.append("- Pivot or quarantine if:")
        lines.extend(f"  - {item}" for item in control.get("pivot_or_quarantine_if", []))
    lines.extend(["", "## Candidate Queue", ""])
    for candidate in report["candidates"]:
        lines.extend(
            [
                f"### {candidate['candidate_id']}",
                "",
                f"- Cycle: `{candidate['cycle_id']}`",
                f"- Branch: {candidate['branch_title']}",
                f"- Type: `{candidate['contribution_type']}`",
                f"- Status: `{candidate['status']}`",
                f"- Stepping-stone maturity: `{candidate['stepping_stone_maturity']}`",
                f"- Exploration payoff score: `{candidate['exploration_payoff_score']}`",
                f"- Publishable subgoal score: `{candidate['publishable_subgoal_score']}`",
                f"- Good-enough paper relevance: `{candidate['good_enough_paper_relevance']['status']}`",
                f"- Average paper relevance marker score: `{candidate['good_enough_paper_relevance']['average_marker_score']}`",
                f"- Smallest honest claim: {candidate['smallest_honest_claim']}",
                f"- Why standalone: {candidate['why_it_could_stand_alone']}",
                f"- Branch control: `{candidate['branch_control_decision']}` - {candidate['branch_control_reason']}",
                f"- Infinite progression risk: `{candidate['infinite_progression_risk']}`",
                f"- Why this budget now: {candidate['why_this_budget_now']}",
                "",
                "#### Missing To Publishable",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in candidate.get("missing_to_publishable", []))
        lines.extend(["", "#### Missing To Good-Enough Paper", ""])
        lines.extend(f"- {item}" for item in candidate.get("missing_to_good_enough_paper", []))
        lines.extend(["", "#### Paper Relevance Markers", ""])
        for marker in candidate.get("paper_relevance_markers", []):
            lines.append(f"- `{marker.get('dimension')}`: score=`{marker.get('score')}`, status=`{marker.get('status')}` - {marker.get('criterion')}")
            if marker.get("missing_for_good_enough"):
                lines.append(f"  - Missing: {marker.get('missing_for_good_enough')}")
        lines.extend(["", "#### Hard Gates", ""])
        for gate, packet in candidate.get("handoff_hard_gates", {}).items():
            lines.append(f"- `{gate}`: ready=`{packet.get('ready')}`, finite_task=`{packet.get('finite_task')}`")
        lines.extend(["", "#### Disqualifiers", ""])
        for row in candidate.get("disqualifier_tests", []):
            lines.append(f"- `{row.get('name')}`: `{row.get('verdict')}` - {row.get('evidence')}")
        prior = candidate.get("prior_art_boundary", {})
        lines.extend(["", "#### Prior-Art Boundary", ""])
        lines.append(f"- Novelty status: `{prior.get('novelty_status', '')}`")
        for task in prior.get("citation_tasks", []):
            lines.append(f"- {task}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    report = build_report()
    write_json(OUT_JSON, report)
    write_markdown(OUT_MD, render_markdown(report))
    print(f"wrote {rel(OUT_JSON)}")
    print(f"wrote {rel(OUT_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
