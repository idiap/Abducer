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
"""Build an independent paper-style TeX/PDF from the discovery timeline report."""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, stable_id, utc_now, write_json
from discovery_marathon_common import LATEST_JSON, load_cycles, load_run_state
from target_profiles import target_profile


OUT_DIR = ROOT / "agentic/reports/timeline_paper"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
OUT_TEX = OUT_DIR / "latest.tex"
OUT_PDF = OUT_DIR / "latest.pdf"
TARGET_LITERATURE = ROOT / "agentic/reports/target_literature_evolution/latest.json"
MACRO_STRATEGY = ROOT / "agentic/reports/macro_strategy/latest.json"
CONTRIBUTION_MONITOR = ROOT / "agentic/reports/scientific_contribution_monitor/latest.json"
STRATEGY_JUDGE = ROOT / "agentic/reports/strategy_progression_judge/latest.json"
QUALITATIVE_GRAPH = ROOT / "agentic/state/qualitative_mechanistic_graphs/yang-mills-existence-and-mass-gap-target.json"
FINITE_ALGEBRA = ROOT / "agentic/reports/finite_algebra_interfaces/latest.json"
ANALYTIC_OBLIGATIONS = ROOT / "agentic/reports/analytic_estimate_obligations/latest.json"
ENDPOINT_INCIDENCE = ROOT / "agentic/reports/endpoint_incidence_certificate/latest.json"
TIMELINE_LATEX_SECTIONS = ROOT / "agentic/reports/timeline_latex_sections/latest.json"
TIMELINE_PAPER_INTERPRETATION = ROOT / "agentic/reports/timeline_paper_interpretation/latest.json"
TIMELINE_PAPER_BLUEPRINT = ROOT / "agentic/reports/timeline_paper_blueprint/latest.json"
TIMELINE_PAPER_SECTIONS = ROOT / "agentic/reports/timeline_paper_sections/latest.json"
TIMELINE_FORMAL_DERIVATION = ROOT / "agentic/reports/timeline_formal_derivation/latest.json"
TIMELINE_PAPER_DIAGRAMS = ROOT / "agentic/reports/timeline_paper_diagrams/latest.json"
PVSNP_PROOF_DELIVERY_QUEUE = ROOT / "agentic/reports/pvsnp_proof_delivery_queue/latest.json"
LATEST_STEP_COUNT = 40

PAPER_SKILLS = [
    "timeline-paper-workflow-orchestrator",
    "timeline-report-evidence-ingestor",
    "timeline-paper-argument-architect",
    "timeline-narrative-coherence-guard",
    "finite-theorem-section-packager",
    "endpoint-worked-calculation-packager",
    "prior-art-positioning-packager",
    "timeline-failed-route-interpreter",
    "timeline-claim-boundary-auditor",
    "timeline-paper-section-synthesizer",
    "timeline-paper-cross-section-reconciler",
    "timeline-report-latex-composer",
    "timeline-summary-latex-translator",
    "timeline-problem-literature-latex-translator",
    "timeline-story-latex-translator",
    "timeline-cycle-latex-translator",
    "timeline-problem-space-narrator",
    "timeline-contribution-stater",
    "timeline-contribution-explainer",
    "timeline-organizing-diagram-builder",
    "timeline-reference-manager",
    "timeline-formal-physics-deriver",
    "results-theorem-scope-certifier",
    "results-finite-object-formalizer",
    "results-proof-packet-deriver",
    "results-prior-art-disqualifier-auditor",
    "results-paper-readiness-gatekeeper",
]


def tex_escape(value: Any) -> str:
    text = clean_text(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    text = text.replace("–", "--").replace("—", "---").replace("’", "'").replace("“", '"').replace("”", '"')
    text = text.replace("≥", ">=").replace("≤", "<=").replace("→", "->").replace("Ω", "Omega")
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


_EXPLICIT_INLINE_MATH_RE = re.compile(r"\\\((.*?)\\\)", re.DOTALL)
_EXPLICIT_DISPLAY_MATH_RE = re.compile(r"\\\[(.*?)\\\]", re.DOTALL)
_MATH_PHRASE_PATTERNS = [
    (re.compile(r"\bP\s*!=\s*NP\b"), r"P \ne NP"),
    (re.compile(r"\bP\s+\\ne\s+NP\b"), r"P \ne NP"),
    (re.compile(r"\bSAT\s+notin\s+P/poly\b"), r"SAT\notin P/poly"),
    (re.compile(r"\bNP\s+not\s+subset\s+P/poly\b"), r"NP\not\subset P/poly"),
    (re.compile(r"\bSAT\s+in\s+SIZE\(([^)]*)\)"), r"SAT\in SIZE(\1)"),
]
_GREEK_WORDS = {
    "alpha",
    "beta",
    "delta",
    "epsilon",
    "eta",
    "gamma",
    "kappa",
    "lambda",
    "omega",
    "phi",
    "rho",
    "tau",
    "theta",
    "xi",
}
_FORMULA_WORDS = {
    "CNF",
    "DNNF",
    "DTSR",
    "EF",
    "EqSAT",
    "FormulaEval",
    "LB",
    "MCSP",
    "NP",
    "P",
    "Psys",
    "QCTSR",
    "ROBDD",
    "SAT",
    "SIZE",
    "TSR",
}


def group_repeated_subscripts(match: re.Match[str]) -> str:
    parts = match.group(0).split("_")
    return parts[0] + "_{" + ",".join(parts[1:]) + "}"


def normalize_inline_formula(fragment: str) -> str:
    formula = clean_text(fragment)
    formula = (
        formula.replace("≤", r"\le ")
        .replace("≥", r"\ge ")
        .replace("→", r"\to ")
        .replace("⊕", r"\oplus ")
        .replace("!=", r"\ne ")
        .replace("<=", r"\le ")
        .replace(">=", r"\ge ")
        .replace("->", r"\to ")
        .replace("=>", r"\Rightarrow ")
        .replace(" notin ", r"\notin ")
        .replace(" subset ", r"\subset ")
    )
    formula = re.sub(r"(?<!\\)\bpoly\b", r"\\mathrm{poly}", formula)
    formula = re.sub(r"(?<!\\)\bGamma(?=_|\b)", r"\\Gamma", formula)
    formula = re.sub(r"\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+){2,}", group_repeated_subscripts, formula)
    for word in sorted(_FORMULA_WORDS, key=len, reverse=True):
        formula = re.sub(rf"(?<![\\A-Za-z]){re.escape(word)}(?![A-Za-z])", rf"\\mathrm{{{word}}}", formula)
    for greek in sorted(_GREEK_WORDS, key=len, reverse=True):
        formula = re.sub(rf"(?<!\\)\b{greek}\b", rf"\\{greek}", formula)
    formula = re.sub(r"_(?!\{)([A-Za-z0-9]+|[+\-])", r"_{\1}", formula)
    formula = re.sub(r"\^(?!\{)([A-Za-z0-9]+|[+\-])", r"^{\1}", formula)
    formula = formula.replace("&", r"\&").replace("#", r"\#").replace("%", r"\%").replace("$", r"\$")
    return formula


def looks_like_inline_formula_token(token: str) -> bool:
    if not token:
        return False
    if not balanced_formula_token(token):
        return False
    if token.count("^") > 1:
        return False
    if re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)+", token):
        return False
    if re.fullmatch(r"[A-Za-z0-9_./-]+\.[A-Za-z0-9]+", token):
        return False
    if token in {"<", ">", "<=", ">=", "!=", "=", r"\ne", r"\le", r"\ge"}:
        return True
    if token in _GREEK_WORDS:
        return True
    if re.search(r"[_^=<>\\]|\\notin|\\subset|\\in\b", token):
        return True
    if any(token.startswith(prefix) for prefix in ("Gamma", "RealSAT", "TransparentRow", "LeastClosed", "ForcedRows")):
        return True
    if token in _FORMULA_WORDS and len(token) > 1:
        return False
    return False


def balanced_formula_token(token: str) -> bool:
    pairs = {"{": "}", "(": ")", "[": "]"}
    stack: list[str] = []
    escaped = False
    for char in token:
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char in pairs:
            stack.append(pairs[char])
        elif char in pairs.values():
            if not stack or stack[-1] != char:
                return False
            stack.pop()
    return not stack


def split_token_affixes(token: str) -> tuple[str, str, str]:
    leading = ""
    core = token
    while core and core[0] in "([\"'":
        leading += core[0]
        core = core[1:]
    trailing = ""
    while core and core[-1] in ".,;:)\"'":
        trailing = core[-1] + trailing
        core = core[:-1]
    return leading, core, trailing


def tex_inline_math(formula: str) -> str:
    return r"\(" + normalize_inline_formula(formula) + r"\)"


def expand_math_phrase(match: re.Match[str], formula: str) -> str:
    expanded = formula
    for index, group in enumerate(match.groups(), start=1):
        expanded = expanded.replace(rf"\{index}", group or "")
    return expanded


def tex_escape_mathish(value: Any) -> str:
    text = clean_text(value)
    if not text:
        return ""
    text = (
        text.replace("–", "--")
        .replace("—", "---")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
    )
    placeholders: dict[str, str] = {}

    def store_math(formula: str, *, display: bool = False) -> str:
        key = f"@@MATH{len(placeholders)}@@"
        normalized = normalize_inline_formula(formula)
        placeholders[key] = "\\[\n" + normalized + "\n\\]" if display else r"\(" + normalized + r"\)"
        return key

    text = _EXPLICIT_DISPLAY_MATH_RE.sub(lambda match: store_math(match.group(1), display=True), text)
    text = _EXPLICIT_INLINE_MATH_RE.sub(lambda match: store_math(match.group(1)), text)
    for pattern, formula in _MATH_PHRASE_PATTERNS:
        text = pattern.sub(lambda match, formula=formula: store_math(expand_math_phrase(match, formula)), text)

    rendered_parts: list[str] = []
    for segment in re.split(r"(@@MATH\d+@@)", text):
        if not segment:
            continue
        if segment in placeholders:
            rendered_parts.append(placeholders[segment])
            continue
        token_parts: list[str] = []
        for token in re.split(r"(\s+)", segment):
            if not token:
                continue
            if token.isspace():
                token_parts.append(token)
                continue
            leading, core, trailing = split_token_affixes(token)
            if core in placeholders:
                token_parts.append(tex_escape(leading) + placeholders[core] + tex_escape(trailing))
            elif looks_like_inline_formula_token(core):
                token_parts.append(tex_escape(leading) + tex_inline_math(core) + tex_escape(trailing))
            else:
                token_parts.append(tex_escape(token))
        rendered_parts.append("".join(token_parts))
    return "".join(rendered_parts)


def tex_key(value: Any, fallback: str) -> str:
    text = clean_text(value).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:48] or fallback


def itemize(items: list[Any]) -> str:
    rows = [clean_text(item) for item in items if clean_text(item)]
    if not rows:
        return r"\begin{itemize}\item None recorded.\end{itemize}"
    return "\\begin{itemize}\n" + "\n".join(f"\\item {tex_escape_mathish(row)}" for row in rows) + "\n\\end{itemize}"


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


def cycle_card(cycle: dict[str, Any]) -> dict[str, Any]:
    output = branch_output(cycle)
    lemma = first_lemma(output)
    return {
        "cycle_id": clean_text(cycle.get("cycle_id")),
        "cycle_number": cycle_number(cycle),
        "branch_title": clean_text(output.get("branch_title")),
        "learning": clean_text(output.get("mathematical_learning")),
        "blocking_gap": clean_text(output.get("attempted_derivation", {}).get("blocking_gap")),
        "next_experiment": clean_text(output.get("next_experiment")),
        "equation_count": len(lemma.get("equations", [])),
        "falsifier_count": len(output.get("falsifiers", [])),
        "equations": [
            {
                "label": clean_text(eq.get("label")),
                "latex": clean_text(eq.get("latex") or eq.get("latex_render")),
                "valid_when": clean_text(eq.get("valid_when")),
            }
            for eq in lemma.get("equations", [])
            if isinstance(eq, dict)
        ],
    }


def load_research_cycles(marathon: dict[str, Any]) -> list[dict[str, Any]]:
    _, run_state = load_run_state(clean_text(marathon.get("run_id")) or None)
    if not run_state:
        return []
    cycles = [cycle for cycle in load_cycles(run_state) if cycle.get("valid_as_research_cycle")]
    return sorted(cycles, key=cycle_number)


def select_timeline_window(cycles: list[dict[str, Any]], judge: dict[str, Any]) -> list[dict[str, Any]]:
    start = clean_text(judge.get("window", {}).get("start_cycle_id"))
    end = clean_text(judge.get("window", {}).get("end_cycle_id"))
    cards = [cycle_card(cycle) for cycle in cycles]
    if not start or not end:
        return cards[-10:]
    selected = [row for row in cards if start <= row["cycle_id"] <= end]
    return selected or cards[-10:]


def select_latest_steps(cycles: list[dict[str, Any]], limit: int = LATEST_STEP_COUNT) -> list[dict[str, Any]]:
    return [cycle_card(cycle) for cycle in cycles[-limit:]]


def build_references(literature: dict[str, Any], target_id: str = "") -> list[dict[str, str]]:
    refs = []
    for row in literature.get("references", []):
        if not isinstance(row, dict):
            continue
        key = tex_key(row.get("ref_id") or row.get("title"), f"ref{len(refs)+1}")
        refs.append(
            {
                "key": key,
                "kind": "literature",
                "label": clean_text(row.get("ref_id")),
                "authors": clean_text(row.get("authors")),
                "year": clean_text(row.get("year")),
                "title": clean_text(row.get("title")),
                "url": clean_text(row.get("url")),
                "supports": clean_text(row.get("supports")),
                "limitation": clean_text(row.get("limitation")),
            }
        )
    if target_id == "p-vs-np-target":
        artifact_refs = [
            ("timeline", "Accumulated P vs NP discovery marathon timeline", rel(LATEST_JSON)),
            ("judge", "P vs NP strategy progression judge", rel(STRATEGY_JUDGE)),
            ("contribution", "P vs NP scientific contribution monitor", rel(CONTRIBUTION_MONITOR)),
            ("macro", "P vs NP macro strategy report", rel(MACRO_STRATEGY)),
            ("proof-delivery-queue", "P vs NP proof-delivery queue and proof-object frontier", rel(PVSNP_PROOF_DELIVERY_QUEUE)),
            ("timeline-latex-sections", "P vs NP timeline report LaTeX section packet", rel(TIMELINE_LATEX_SECTIONS)),
            ("paper-interpretation", "P vs NP timeline paper interpretation packet", rel(TIMELINE_PAPER_INTERPRETATION)),
            ("formal-derivation", "P vs NP formal transfer derivation packet", rel(TIMELINE_FORMAL_DERIVATION)),
        ]
    else:
        artifact_refs = [
            ("timeline", "Accumulated discovery marathon timeline", rel(LATEST_JSON)),
            ("judge", "Strategy progression judge", rel(STRATEGY_JUDGE)),
            ("contribution", "Scientific contribution monitor", rel(CONTRIBUTION_MONITOR)),
            ("macro", "Macro strategy report", rel(MACRO_STRATEGY)),
            ("finite", "Finite algebra interface report", rel(FINITE_ALGEBRA)),
            ("analytic", "Analytic estimate obligations report", rel(ANALYTIC_OBLIGATIONS)),
            ("endpoint-incidence", "Endpoint kappa4 incidence certificate", rel(ENDPOINT_INCIDENCE)),
            ("timeline-latex-sections", "Timeline report LaTeX section packet", rel(TIMELINE_LATEX_SECTIONS)),
        ]
    for key, title, path in artifact_refs:
        refs.append(
            {
                "key": f"artifact-{key}",
                "kind": "artifact",
                "label": path,
                "authors": "Abducer timeline-paper workflow",
                "year": "2026",
                "title": title,
                "url": path,
                "supports": "Local evidence for the timeline-derived paper argument.",
                "limitation": "An artifact citation supports the state of the run, not an external theorem.",
            }
        )
    return refs


def target_matches(report: dict[str, Any], target_id: str) -> bool:
    declared = clean_text(report.get("target_id"))
    return not target_id or not declared or declared == target_id


def target_literature_for(target_id: str, current: dict[str, Any]) -> dict[str, Any]:
    if target_matches(current, target_id) and current:
        return current
    if target_id == "p-vs-np-target":
        from build_target_literature_evolution import build_pvsnp_report

        return build_pvsnp_report({"target_id": target_id, "raw_goal": "P vs NP", "source": "timeline paper builder"})
    if target_id == "yang-mills-existence-and-mass-gap-target":
        from build_target_literature_evolution import build_yang_mills_report

        return build_yang_mills_report({"target_id": target_id, "raw_goal": "Yang-Mills existence and mass gap", "source": "timeline paper builder"})
    return current if isinstance(current, dict) else {}


def contribution_monitor_for(target_id: str, current: dict[str, Any]) -> dict[str, Any]:
    if target_matches(current, target_id) and current:
        return current
    if not target_id:
        return {}
    from build_scientific_contribution_monitor import build_report as build_contribution_monitor

    return build_contribution_monitor(target_id)


def cite_by_role(refs: list[dict[str, str]], role_terms: list[str], fallback_count: int = 3) -> str:
    selected = []
    for ref in refs:
        hay = " ".join([ref.get("label", ""), ref.get("title", ""), ref.get("supports", "")]).lower()
        if any(term in hay for term in role_terms):
            selected.append(ref["key"])
    if not selected:
        selected = [ref["key"] for ref in refs[:fallback_count]]
    return ",".join(selected[:fallback_count])


def top_contributions(monitor: dict[str, Any], limit: int = 4) -> list[dict[str, Any]]:
    candidates = [row for row in monitor.get("candidates", []) if isinstance(row, dict)]
    candidates.sort(key=lambda row: int(row.get("score", 0)), reverse=True)
    return candidates[:limit]


def build_proof_objects(queue: dict[str, Any], limit: int = 8) -> list[dict[str, Any]]:
    """Project proof-delivery queue items into timeline-visible proof objects."""
    rows = []
    for item in queue.get("items", []) if isinstance(queue.get("items"), list) else []:
        if not isinstance(item, dict):
            continue
        outputs = [clean_text(row) for row in item.get("proof_outputs", []) if clean_text(row)]
        success = [clean_text(row) for row in item.get("success_criteria", []) if clean_text(row)]
        demotion = [clean_text(row) for row in item.get("demotion_criteria", []) if clean_text(row)]
        rows.append(
            {
                "proof_object_id": clean_text(item.get("queue_id")),
                "rank": int(item.get("rank", len(rows) + 1)),
                "title": clean_text(item.get("title")),
                "proof_status": clean_text(item.get("proof_status")),
                "source_anchor": clean_text(item.get("source_anchor")),
                "theorem_goal": clean_text(item.get("theorem_goal")),
                "source_object": clean_text(item.get("source_object")),
                "target_object": clean_text(item.get("target_object")),
                "next_analysis": clean_text(item.get("next_analysis")),
                "paper_handoff": clean_text(item.get("paper_handoff")),
                "proof_outputs": outputs[:8],
                "success_criteria": success[:6],
                "demotion_criteria": demotion[:6],
                "validation_handoff": item.get("validation_handoff", []),
            }
        )
    rows.sort(key=lambda row: row["rank"])
    return rows[:limit]


def render_proof_objects_tex(proof_objects: list[dict[str, Any]]) -> str:
    if not proof_objects:
        return ""
    rows = []
    for obj in proof_objects[:5]:
        rows.append(
            rf"""
\subsection*{{{tex_escape_mathish(obj.get("title"))}}}
\paragraph{{Timeline proof-object id.}} \texttt{{{tex_escape(obj.get("proof_object_id"))}}}; rank {tex_escape(obj.get("rank"))}; status \texttt{{{tex_escape(obj.get("proof_status"))}}}.
\paragraph{{Theorem goal.}} {tex_escape_mathish(obj.get("theorem_goal"))}
\paragraph{{Source object.}} {tex_escape_mathish(obj.get("source_object"))}
\paragraph{{Target object.}} {tex_escape_mathish(obj.get("target_object"))}
\paragraph{{Required proof outputs.}}
{itemize(obj.get("proof_outputs", [])[:5])}
\paragraph{{Success criteria.}}
{itemize(obj.get("success_criteria", [])[:4])}
\paragraph{{Demotion boundary.}}
{itemize(obj.get("demotion_criteria", [])[:4])}
"""
        )
    return "\n".join(
        [
            r"\section*{Timeline Proof Objects}",
            (
                "The following proof objects are copied from the proof-delivery queue into the timeline artifact so that "
                "the paper workflow tracks not only cycle evidence, but also the concrete proof packets needed before promotion."
            ),
            *rows,
        ]
    )


def render_latest_steps_tex(latest_steps: dict[str, Any]) -> str:
    rows = latest_steps.get("cycles", []) if isinstance(latest_steps, dict) else []
    if not rows:
        return ""
    items = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        parts = [
            clean_text(row.get("cycle_id")),
            clean_text(row.get("branch_title")),
            clean_text(row.get("learning")),
        ]
        next_experiment = clean_text(row.get("next_experiment"))
        blocking_gap = clean_text(row.get("blocking_gap"))
        if blocking_gap:
            parts.append(f"Gap: {blocking_gap}")
        if next_experiment:
            parts.append(f"Next: {next_experiment}")
        items.append(" -- ".join(part for part in parts if clean_text(part)))
    return "\n".join(
        [
            rf"\section*{{Latest {tex_escape(latest_steps.get('requested_count', len(rows)))} Timeline Steps}}",
            (
                "This terminal appendix records the most recent timeline steps included in the paper build, "
                "so the LaTeX artifact preserves the current end of the marathon rather than only the judged argument window."
            ),
            itemize(items),
        ]
    )


def build_paper_narrative_goal_lock(judge: dict[str, Any], monitor: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    progress = judge.get("progression_judgement", {})
    readiness = judge.get("paper_contribution_readiness", {})
    if profile["target_id"] == "p-vs-np-target":
        return {
            "lock_name": "pvsnp_transfer_obstruction_paper_goal",
            "status": "active",
            "subgoal_title": "Route-specific P vs NP transfer obstruction and certificate-gate note",
            "coherent_narrative_thesis": (
                "The coherent narrative is that the paper-level object is not the whole P vs NP discovery history. "
                "It is a bounded complexity-theory contribution candidate: formulate exact transfer envelopes for named "
                "bridge routes, prove where exponent loss, advice leakage, naturalness, or local-soundness failure blocks "
                "promotion, and isolate the finite proof obligation that would turn the route into a theorem."
            ),
            "anti_infinite_exploration_rule": (
                "Do not add more timeline detail unless it strengthens exactly one paper spine node: theorem scope, "
                "source carrier definition, transfer inequality, barrier/disqualifier boundary, proof packet, or prior-art boundary."
            ),
            "included_material_policy": [
                "Keep definitions of source carrier, target class, circuit model, length map, and uniformity/advice convention.",
                "Keep exact transfer inequalities of the form SIZE(H_N) <= N^{q+beta c+o(1)} and the source lower-bound threshold a>q+beta c.",
                "Keep certificate-gate material only when it states existence, searchability, soundness, density, and advice-freeness conditions.",
                "Keep falsifiers when they are theorem-shaped: bounded-window collapse, target-equivalent source assumptions, natural-property pressure, local-soundness failure, or row-selection leakage.",
                "Keep prior-art context only when it separates this route-specific obstruction from known hardness magnification, MCSP/MKtP, proof-complexity, natural-proofs, relativization, and algebrization results.",
            ],
            "excluded_detail_policy": [
                "Exclude cycle chronology that merely repeats that P vs NP is hard or that barriers exist.",
                "Exclude speculative carriers whose source object, target object, and transfer map are unnamed.",
                "Exclude broad novelty language until theorem scope, proof packet, and prior-art/disqualifier audit are explicit.",
                "Move exploratory strategy queues to appendices unless they decide a named branch by a finite calculation or proof obligation.",
            ],
            "narrative_spine": [
                "State the P vs NP/P-poly target commitment and why all-exponent nonuniform lower bounds are the relevant pressure.",
                "Explain why hardness magnification and meta-complexity routes live or die by exact transfer exponents and advice discipline.",
                "Define the source carrier H_N, target SAT_m or NP-complete target, circuit model, and transfer envelope q+beta c.",
                "Prove the bounded-window obstruction and the all-exponent lift gate.",
                "State the searchable-certificate bridge gate and its naturalness/advice disqualifiers.",
                "Package the direct-cluster soundness or odd-charge Tseitin falsifier as the current finite proof obligation.",
                "Close with the smallest honest claim: a route-specific transfer/no-go/certificate-gate note, not P != NP.",
            ],
            "detail_budget": {
                "paper_body": "Only details needed for theorem scope, source object, transfer formula, barrier boundary, proof packet, and prior-art boundary.",
                "appendix_or_future_work": "Exploratory branches, repeated pressure statements, and queue state useful for future runs.",
                "quarantine": "Details that do not name a source carrier, target class, transfer envelope, or falsifier.",
            },
            "decisive_next_work": [
                "Write the bounded-window transfer lemma with a,q,beta and prove the all-exponent obstruction.",
                "Instantiate one named carrier or proof system and compute q, beta, advice cost, and certificate-search exponent.",
                "Prove direct-cluster soundness or exhibit the odd-charge Tseitin parity ambiguity for that named system.",
                "Run prior-art and disqualifier audits against hardness magnification, MCSP/MKtP, natural proofs, relativization, algebrization, and proof-complexity transfer.",
            ],
            "stop_or_demote_when": [
                "Two successive paper passes add only route slogans without improving theorem scope, transfer inequality, carrier definition, or proof packet.",
                "The branch cannot name the source carrier, target class, circuit model, length map, or validation handoff.",
                "The proposed result is subsumed by known barriers or depends on a source lower bound equivalent to the target separation.",
            ],
            "do_not_stop_prematurely_if": [
                "The exact transfer formula is still becoming sharper through named q, beta, advice, or valid-length terms.",
                "A named proof system or carrier is close to yielding a finite falsifier or direct-soundness theorem.",
                "A failure identifies a precise method-class no-go that can become the paper's negative result.",
            ],
            "coherence_checks": [
                "Every section must say how it supports theorem scope, source-object formalization, transfer proof, disqualifier audit, or claim boundary.",
                "The introduction must promise only a scoped route-specific result, not P != NP.",
                "The conclusion must name what is locally established and what remains validation-needed.",
            ],
            "source_strategy_decision": clean_text(progress.get("decision")),
            "source_payoff_potential": clean_text(progress.get("payoff_potential")),
            "source_readiness": clean_text(readiness.get("readiness_class") or readiness.get("status")),
            "epistemic_status": "narrative_goal_locked_validation_needed",
        }
    return {
        "lock_name": "finite_wilson_os_obstruction_paper_goal",
        "status": "active",
        "subgoal_title": "Finite Wilson/OS Schur-Feshbach obstruction note",
        "coherent_narrative_thesis": (
            "The coherent narrative is that the paper-level object is not the whole "
            "Yang-Mills discovery history. It is a bounded scientific contribution: formulate and validate a finite "
            "reflected-Wilson Gram quotient test whose first-order PHP condition and "
            "second-order Schur-Feshbach correction expose a concrete OS-positivity "
            "obstruction or bridge obligation."
        ),
        "anti_infinite_exploration_rule": (
            "Do not add more timeline detail unless it strengthens exactly one of the paper spine nodes: "
            "finite theorem, first concrete H,K Wilson collar case, same-theory transfer certificate, "
            "prior-art boundary, or honest claim statement."
        ),
        "included_material_policy": [
            "Keep definitions, assumptions, and equations needed to prove the finite Schur-Feshbach tangent-cone theorem.",
            "Keep the first concrete H,K Wilson collar/hairpin calculation or the precise plan that directly computes it.",
            "Keep the post-H,K endpoint kappa_4 scalar certificate, including the heat-kernel source derivative, stencil error, incidence dominance functional, and tail/remainder obligations.",
            "Keep same-theory OS reconstruction and boundary-OPE transfer obligations that determine whether the finite result matters for the target problem.",
            "Keep literature context only when it explains why this finite obstruction program is a real contribution rather than a proxy calculation.",
            "Keep failures only when they explain a narrative decision: why Hamiltonian/global decay routes were narrowed into the finite Wilson/OS bridge.",
        ],
        "excluded_detail_policy": [
            "Exclude cycle-by-cycle operational chronology that does not change the theorem, example, transfer certificate, or claim boundary.",
            "Exclude new speculative branches until the finite theorem or first H,K collar case has been discharged or explicitly blocked.",
            "Exclude workflow mechanics, scoring traces, and queue administration from the paper body unless they justify evidence selection.",
            "Move useful but nonessential explorations to future work or appendices rather than letting them redefine the paper claim.",
        ],
        "narrative_spine": [
            "State the Clay-level obligation and why OS positivity plus same-theory reconstruction is the relevant bridge pressure.",
            "Explain the route narrowing: global Hamiltonian and correlator language became too under-typed, so the paper isolates a finite reflected Wilson Gram object.",
            "Define the normalized reflected Wilson quotient M_eta and the rank-one constant OS direction.",
            "Prove the finite first-order condition PHP positive semidefinite and the Schur-Feshbach second-order test on ker(PHP).",
            "Compute, extract, or sharply parameterize the first concrete H,K Wilson collar/hairpin case and run the finite positivity test.",
            "Package the post-H,K endpoint kappa_4 test as a worked calculation: scalar source derivatives of log Z_v, seven-point stencil certification, compact-group root-quartic coefficient, and endpoint incidence dominance D_v.",
            "State the transfer debt: same-theory boundary OPE, uniform collar/cutoff remainder, and OS reconstruction quotient legitimacy.",
            "Close with the smallest honest contribution claim and a decision rule for promotion, revision, or quarantine.",
        ],
        "detail_budget": {
            "paper_body": "Only details needed for the theorem, the first H,K example, transfer debt, and prior-art boundary.",
            "appendix_or_future_work": "Exploratory branches, failed analogies, and workflow diagnostics that are useful but not claim-bearing.",
            "quarantine": "Details that merely restate the obstruction ladder without proving the finite theorem or computing the concrete H,K case.",
        },
        "decisive_next_work": [
            "Prove the finite Schur-Feshbach tangent-cone theorem as a theorem independent of Yang-Mills.",
            "Compute or symbolically parameterize H and K for the smallest reflected Wilson collar/hairpin block.",
            "Compute the actual endpoint incidence table B_12,v, B_13,v, B_23,v and certify the kappa_4 source-derivative interval for M_G+R_end.",
            "Write the same-theory transfer certificate identifying exactly what boundary-OPE and remainder estimates would promote the finite result.",
        ],
        "stop_or_demote_when": [
            "Two successive paper passes add only chronology or variants without improving the finite theorem, the H,K example, or the transfer certificate.",
            "The branch cannot name the finite matrix object, the Wilson observable family, the quotient/null sector, or the validation handoff.",
            "A proposed detail has no role in the statement, proof, worked example, prior-art boundary, or honest contribution claim.",
        ],
        "do_not_stop_prematurely_if": [
            "The finite theorem is still becoming sharper through proof obligations that can be stated and checked.",
            "The first H,K Wilson collar case is not computed yet but the next step names the observable family and coefficient extraction method.",
            "The endpoint kappa_4 calculation is narrowing from abstract R to a concrete incidence table, source derivative, or remainder estimate.",
            "A failure identifies a precise same-theory transfer obstruction that can become the paper's negative result.",
        ],
        "coherence_checks": [
            "Every section must answer how it supports the finite theorem, H,K example, transfer certificate, prior-art boundary, or claim.",
            "The introduction must promise only the bounded paper subgoal, not a proof of Yang-Mills.",
            "The conclusion must name what has been established locally and what remains validation-needed.",
        ],
        "source_strategy_decision": clean_text(progress.get("decision")),
        "source_payoff_potential": clean_text(progress.get("payoff_potential")),
        "source_readiness": clean_text(readiness.get("readiness_class") or readiness.get("status")),
        "epistemic_status": "narrative_goal_locked_validation_needed",
    }


def build_diagram_tikz() -> str:
    return r"""
\begin{figure}[t]
\centering
\begin{tikzpicture}[
  node distance=1.2cm and 1.1cm,
  box/.style={draw, rounded corners, align=center, text width=3.0cm, minimum height=0.9cm},
  smallbox/.style={draw, rounded corners, align=center, text width=2.7cm, minimum height=0.8cm, font=\small},
  arrow/.style={-{Latex[length=2mm]}, thick},
  warn/.style={-{Latex[length=2mm]}, thick, dashed}
]
\node[box] (problem) {Clay target\\continuum YM + mass gap};
\node[box, right=of problem] (history) {Literature pressure\\construction, OS, spectrum};
\node[box, right=of history] (timeline) {Timeline evidence\\cycles 213--222};
\node[box, below=of history] (object) {Reflected Wilson\\Gram quotient};
\node[smallbox, below left=of object] (first) {First-order test\\$P H P \succeq 0$};
\node[smallbox, below right=of object] (second) {Second-order test\\$\Omega_2=P(K-n^{-2}H11^{*}HP)P$};
\node[box, right=of object] (contrib) {Paper-level subgoal\\finite OS obstruction};
\node[box, right=of contrib] (handoff) {Validation handoff\\OPE + uniform remainder};
\draw[arrow] (problem) -- (history);
\draw[arrow] (history) -- (timeline);
\draw[arrow] (timeline) -- (object);
\draw[arrow] (object) -- (first);
\draw[arrow] (object) -- (second);
\draw[arrow] (first) -- (contrib);
\draw[arrow] (second) -- (contrib);
\draw[arrow] (contrib) -- (handoff);
\draw[warn] (handoff) to[bend left=18] node[above,font=\scriptsize]{if transfer fails} (timeline);
\end{tikzpicture}
\caption{Organizing diagram for the timeline-derived paper. The argument runs from the Clay commitments and literature obligations into the current Wilson/OS finite obstruction candidate. Dashed feedback marks the demotion path: if the Wilson boundary OPE or uniform remainder cannot be certified in the same theory, the contribution remains a local obstruction program rather than a continuum result.}
\label{fig:organizing-diagram}
\end{figure}
"""


def build_formal_derivation() -> str:
    return r"""
\section{Formal Physics Derivation: The Wilson/OS Tangent-Cone Test}
\label{sec:formal-derivation}

This section states the local finite calculation isolated by the timeline. It is not a proof of the Yang--Mills mass gap. It is a candidate finite obstruction or bridge lemma that becomes physically relevant only when the reflected Wilson observable family and its boundary expansion are certified in the same continuum theory.

\paragraph{Definitions.}
Fix a finite family of gauge-invariant Wilson observables $W_1^{(\eta)},\ldots,W_n^{(\eta)}$ supported in a collar of width $\eta$ near a Euclidean reflection plane, with reflected partners $\Theta W_i^{(\eta)}$. Let
\[
  N_\eta(i,j)=\langle \Theta W_i^{(\eta)}, W_j^{(\eta)}\rangle
\]
denote the reflected Euclidean Gram matrix, under the assumption that the expectation is computed in the same regulated Yang--Mills measure whose continuum limit is being tested. Let $\widehat N_\eta$ and $\widehat B_\eta$ denote the normalized numerator and boundary/diagonal renormalization matrices, and set
\[
  M_\eta=\widehat N_\eta \oslash \widehat B_\eta .
\]
Let $\mathbf 1=(1,\ldots,1)^T$ and
\[
  P=I-\frac{\mathbf 1\mathbf 1^{*}}{n}
\]
be the projection onto $\mathbf 1^\perp$.

\paragraph{Assumptions.}
Assume that, after diagonal normalization, the reflected Wilson matrix has the expansion
\[
  M_\eta = \mathbf 1\mathbf 1^{*}+\eta H+\eta^2 K+O(\eta^3),
\]
where $H=H^*$ and $K=K^*$ are finite matrices extracted from the same reflected Wilson boundary operator-product expansion, and where the $O(\eta^3)$ remainder is uniform on the finite observable block. Assume also that the quotient by the rank-one constant direction is the correct finite shadow of the OS Hilbert-space null quotient.

\paragraph{First-order obstruction.}
For every $v\in\mathbf 1^\perp$,
\[
  v^{*}M_\eta v = \eta\,v^{*}H v+\eta^2 v^{*}K v+O(\eta^3).
\]
Thus reflection positivity on the quotient forces
\[
  P H P\succeq 0 .
\]
If there exists $v\in\mathbf 1^\perp$ with $v^{*}H v<0$, the finite reflected Wilson block is not OS-positive in the tested same-theory regime.

\paragraph{Second-order obstruction.}
When $P H P\succeq0$ but has a nontrivial null direction, the rank-one normalization direction contributes a Schur correction. The timeline isolates the second-order form
\[
  \Omega_2=P\left(K-n^{-2}H\mathbf 1\mathbf 1^{*}HP\right)P .
\]
The required second-order positivity condition is
\[
  w^{*}\Omega_2 w\ge 0\qquad\text{for all }w\in\ker(PHP)\cap\mathbf 1^\perp .
\]
Consequently, a vector $w$ in this null sector with $w^{*}\Omega_2w<0$ is a finite obstruction to the proposed Wilson/OS positivity bridge.

\paragraph{Physics meaning.}
The correction term subtracts the large constant OS direction and removes one-body diagonal renormalizations. A remaining negative value is therefore not a bookkeeping artifact of normalization; it is evidence for a mixed reflected Wilson boundary term that must be repaired, demoted, or turned into a publishable finite falsifier.

\paragraph{Endpoint \( \kappa_4 \) certificate.}
The latest marathon cycles sharpen the post-\(H,K\) remainder into a scalar endpoint calculation. In the one-dimensional null channel \(z=(1,1,-2)\), the connected endpoint contribution has the form
\[
  R_{\mathrm{end}}
  =C_{\mathrm{col}}\sum_v
  \left(2\kappa_{4,v}(b_{12,v})
        -4\kappa_{4,v}(b_{13,v})
        -4\kappa_{4,v}(b_{23,v})\right)
  +E_{\mathrm{tail}},
\]
where \(C_{\mathrm{col}}=\frac{g_a^4}{24}(T_F/N)^2\) in the current normalization, and
\[
  \kappa_{4,v}^{\mathrm{sing}}(b)
  =
  \left.\partial_s^4\log Z_v(s;b)\right|_{s=0}
  =
  \langle X_{v,b}^4\rangle_{c,v}
\]
is computed in the same heat-kernel endpoint-box regulator as the Wilson collar observables. This representation is valid only after disconnected Wick-square terms have been placed in the positive Gram margin and after straight \(C_Aff\) contacts cancel by the null-incidence identity.

For a small heat-kernel endpoint box, the compact-group volume density gives the leading local asymptotic
\[
  \kappa_{4,v}(B)
  =
  -\frac{t_v^4}{15}\operatorname{Tr}_{ad}(\operatorname{ad}_B^4)
  +O(t_v^5\|B\|^4+t_v^6\|B\|^6).
\]
Equivalently, for \(SU(N)\),
\[
  \sum_{\alpha>0}\alpha(B)^4
  =
  N\operatorname{tr}_F(B^4)+3(\operatorname{tr}_F B^2)^2 .
\]
Thus the endpoint term is not automatically dangerous: in the null scalar only the signed dominance
\[
  D_v=2B_{12,v}-4B_{13,v}-4B_{23,v}
\]
can lower the Schur-Feshbach scalar. A publishable worked example must therefore enumerate the actual endpoint incidence table and prove a bound of the form
\[
  S_{\mathrm{null}}
  \ge
  M_G-C_{\mathrm{col}}\sum_v\chi_v[D_v]_+
  -C_{\mathrm{col}}\sum_{v,ij}|w_{ij}|\,|\epsilon_{ij,v}|
  -|E_{\mathrm{tail}}|.
\]
Promotion requires the right-hand side to remain positive in the same regulator window; a certified negative interval is the finite endpoint falsifier.

\paragraph{Unresolved proof obligations.}
The local derivation becomes a Yang--Mills contribution only after the workflow supplies: (i) a controlled reflected Wilson boundary expansion for the chosen hairpin family, (ii) same-theory extraction of $H$ and $K$, (iii) a uniform collar/cutoff remainder, and (iv) a transfer certificate showing that the finite quotient is a legitimate OS reconstruction shadow.
"""


def render_bibliography(refs: list[dict[str, str]]) -> str:
    rows = []
    for ref in refs:
        title = tex_escape(ref["title"])
        authors = tex_escape(ref["authors"])
        year = tex_escape(ref["year"])
        url = tex_escape(ref["url"])
        supports = tex_escape(ref["supports"])
        limitation = tex_escape(ref["limitation"])
        rows.append(
            "\n".join(
                [
                    rf"\bibitem{{{ref['key']}}} {authors} ({year}). \emph{{{title}}}.",
                    rf"\newline \url{{{url}}}",
                    rf"\newline Supports: {supports}",
                    rf"\newline Limitation: {limitation}",
                ]
            )
        )
    return "\\begin{thebibliography}{99}\n" + "\n\n".join(rows) + "\n\\end{thebibliography}"


def render_contribution_table(contributions: list[dict[str, Any]]) -> str:
    lines = [
        r"\begin{longtable}{p{0.23\linewidth}p{0.35\linewidth}p{0.32\linewidth}}",
        r"\toprule",
        r"Contribution & Smallest honest claim & Validation boundary \\",
        r"\midrule",
    ]
    for row in contributions:
        lines.append(
            f"{tex_escape(row.get('contribution_type'))} & "
            f"{tex_escape(row.get('smallest_honest_claim'))} & "
            f"{tex_escape('; '.join(row.get('validation_burden', [])[:2]))} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{longtable}"])
    return "\n".join(lines)


def build_report() -> dict[str, Any]:
    marathon = load_optional_json(LATEST_JSON)
    literature = load_optional_json(TARGET_LITERATURE)
    macro = load_optional_json(MACRO_STRATEGY)
    monitor = load_optional_json(CONTRIBUTION_MONITOR)
    judge = load_optional_json(STRATEGY_JUDGE)
    qualitative = load_optional_json(QUALITATIVE_GRAPH)
    finite = load_optional_json(FINITE_ALGEBRA)
    analytic = load_optional_json(ANALYTIC_OBLIGATIONS)
    endpoint = load_optional_json(ENDPOINT_INCIDENCE)
    latex_sections = load_optional_json(TIMELINE_LATEX_SECTIONS)
    interpretation = load_optional_json(TIMELINE_PAPER_INTERPRETATION)
    blueprint = load_optional_json(TIMELINE_PAPER_BLUEPRINT)
    paper_sections = load_optional_json(TIMELINE_PAPER_SECTIONS)
    formal_derivation_artifact = load_optional_json(TIMELINE_FORMAL_DERIVATION)
    paper_diagrams = load_optional_json(TIMELINE_PAPER_DIAGRAMS)
    proof_delivery_queue = load_optional_json(PVSNP_PROOF_DELIVERY_QUEUE)
    cycles = load_research_cycles(marathon)
    target_id = clean_text(marathon.get("target_id") or literature.get("target_id") or "yang-mills-existence-and-mass-gap-target")
    profile = target_profile(target_id)
    literature = target_literature_for(profile["target_id"], literature)
    monitor = contribution_monitor_for(profile["target_id"], monitor)
    window = select_timeline_window(cycles, judge)
    latest_step_cards = select_latest_steps(cycles)
    refs = build_references(literature, profile["target_id"])
    contributions = top_contributions(monitor)
    proof_objects = build_proof_objects(proof_delivery_queue) if profile["target_id"] == "p-vs-np-target" else []
    top = contributions[0] if contributions else {}
    strategy = judge.get("current_strategy", {})
    progress = judge.get("progression_judgement", {})
    readiness = judge.get("paper_contribution_readiness", {})
    alignment = judge.get("main_problem_alignment", {})
    narrative_goal_lock = build_paper_narrative_goal_lock(judge, monitor, profile)
    if profile["target_id"] == "p-vs-np-target":
        title = "Route-Specific Transfer Obstructions and Certificate Gates in P vs NP Exploration"
        abstract = (
            "We turn the accumulated Abducer P vs NP timeline into a paper-style complexity-theory argument. "
            "The draft does not claim P != NP or SAT not in P/poly. Its contribution is to isolate exact transfer-envelope "
            "obstructions, certificate-gate conditions, and route-specific falsifiers that decide whether hardness-magnification, "
            "MCSP/MKtP, proof-complexity, or nonblackbox bridge routes have paper-level payoff."
        )
    elif profile["target_id"] == "yang-mills-existence-and-mass-gap-target":
        title = "A Timeline-Derived Wilson/OS Obstruction Program for Yang--Mills Mass Gap Exploration"
        abstract = (
            "We turn the accumulated Abducer discovery timeline into a paper-style scientific argument. "
            "The draft does not claim a proof of Yang--Mills existence or mass gap. "
            "Its contribution is to isolate a finite Wilson/OS tangent-cone obstruction candidate, explain how the route emerged from the timeline, and state the validation debt required before the result can be promoted from finite obstruction science to a continuum Yang--Mills bridge."
        )
    else:
        title = f"A Target-Preserving Obstruction Program for {profile['display_name']}"
        abstract = "We turn the accumulated Abducer discovery timeline into a bounded paper-style argument with explicit claim boundaries and validation debt."
    report = {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": profile["target_id"],
        "paper_id": stable_id("timeline-paper", marathon.get("run_id", ""), judge.get("judgement_id", "")),
        "title": title,
        "abstract": abstract,
        "independent_workflow": True,
        "invoked_skills": PAPER_SKILLS,
        "source_artifacts": [
            rel(LATEST_JSON),
            rel(TARGET_LITERATURE),
            rel(MACRO_STRATEGY),
            rel(CONTRIBUTION_MONITOR),
            rel(STRATEGY_JUDGE),
            rel(QUALITATIVE_GRAPH),
            rel(FINITE_ALGEBRA),
            rel(ANALYTIC_OBLIGATIONS),
            rel(ENDPOINT_INCIDENCE),
            rel(TIMELINE_LATEX_SECTIONS),
            rel(TIMELINE_PAPER_INTERPRETATION),
            rel(TIMELINE_PAPER_BLUEPRINT),
            rel(TIMELINE_PAPER_SECTIONS),
            rel(TIMELINE_FORMAL_DERIVATION),
            rel(TIMELINE_PAPER_DIAGRAMS),
            *([rel(PVSNP_PROOF_DELIVERY_QUEUE)] if profile["target_id"] == "p-vs-np-target" else []),
        ],
        "timeline_window": {
            "start_cycle_id": window[0]["cycle_id"] if window else "",
            "end_cycle_id": window[-1]["cycle_id"] if window else "",
            "cycle_count": len(window),
            "cycles": window,
        },
        "latest_steps": {
            "requested_count": LATEST_STEP_COUNT,
            "start_cycle_id": latest_step_cards[0]["cycle_id"] if latest_step_cards else "",
            "end_cycle_id": latest_step_cards[-1]["cycle_id"] if latest_step_cards else "",
            "cycle_count": len(latest_step_cards),
            "total_research_cycle_count": len(cycles),
            "cycles": latest_step_cards,
        },
        "paper_narrative_goal_lock": narrative_goal_lock,
        "problem_space": {
            "problem_name": literature.get("problem_name", ""),
            "formal_statement": literature.get("problem_statement", {}).get("formal_shape", ""),
            "why_it_matters": literature.get("why_it_matters", []),
            "literature_stages": literature.get("literature_stages", []),
            "macro_strategy_headline": macro.get("headline", ""),
            "primary_strategy": strategy.get("title", ""),
        },
        "contributions": contributions,
        "proof_delivery_queue": {
            "status": proof_delivery_queue.get("status", ""),
            "top_item_id": proof_delivery_queue.get("top_item_id", ""),
            "source_artifact": rel(PVSNP_PROOF_DELIVERY_QUEUE) if proof_delivery_queue else "",
            "item_count": len(proof_delivery_queue.get("items", [])) if isinstance(proof_delivery_queue.get("items"), list) else 0,
        },
        "proof_objects": proof_objects,
        "contribution_readiness": readiness,
        "strategy_judgement": {
            "decision": progress.get("decision", ""),
            "payoff_potential": progress.get("payoff_potential", ""),
            "next_decisive_test": progress.get("next_decisive_test", ""),
            "when_to_stop": progress.get("when_to_stop", ""),
            "alignment_class": alignment.get("alignment_class", ""),
            "target_commitments_touched": alignment.get("target_commitments_touched", []),
        },
        "diagram": {
            "kind": "tikz_route_diagram",
            "caption": (
                "Route diagram from P vs NP target commitments to transfer-envelope, certificate-gate, "
                "and disqualifier handoff."
                if profile["target_id"] == "p-vs-np-target"
                else "Route diagram from target commitments to finite Wilson/OS obstruction and validation handoff."
            ),
        },
        "formal_derivation": (
            {
                "object": "Target-preserving transfer envelope for P vs NP bridge routes.",
                "core_conditions": [
                    "named source carrier or language",
                    "fixed target class and circuit model",
                    "explicit length map and transfer envelope q+beta*c+o(1)",
                    "uniformity, advice, naturalness, and barrier status attached to the theorem",
                ],
                "local_result": "A source lower bound SIZE(H_N)>N^a contradicts SAT in SIZE(n^c) only when a>q+beta*c; fixed beta>0 yields a bounded exponent window rather than P/poly exclusion.",
                "remaining_obligations": [
                    "instantiate a named carrier or proof system",
                    "compute q, beta, advice cost, and certificate-search exponent",
                    "prove direct-cluster soundness or exhibit the parity-ambiguity falsifier",
                    "complete the prior-art/disqualifier audit before paper promotion",
                ],
            }
            if profile["target_id"] == "p-vs-np-target"
            else {
                "object": "Reflected Wilson Gram quotient near the OS reflection plane.",
                "core_conditions": [
                    "same-theory reflected Wilson observable family",
                    "diagonal normalization",
                    "uniform boundary OPE remainder",
                    "OS quotient by the constant rank-one direction",
                ],
                "local_result": "If PHP has a negative vector on 1^perp, or if the Schur-corrected Omega_2 is negative on ker(PHP), the finite block obstructs the proposed OS positivity bridge.",
                "remaining_obligations": [
                    "derive H and K for an actual reflected Wilson hairpin family",
                    "control the collar/cutoff remainder uniformly",
                    "certify same-theory transfer into continuum OS reconstruction",
                ],
            }
        ),
        "references": refs,
        "supporting_artifacts": {
            "qualitative_node_count": len(qualitative.get("nodes", [])) if isinstance(qualitative.get("nodes"), list) else 0,
            "finite_interface_status": finite.get("status", ""),
            "analytic_obligation_status": analytic.get("status", ""),
            "endpoint_incidence_status": endpoint.get("status", ""),
            "endpoint_incidence_certificate": endpoint.get("certificate_id", ""),
            "timeline_latex_sections_status": latex_sections.get("status", ""),
            "timeline_latex_sections_packet": latex_sections.get("packet_id", ""),
            "proof_delivery_queue_status": proof_delivery_queue.get("status", ""),
            "proof_object_count": len(proof_objects),
        },
        "timeline_latex_sections": {
            "target_id": latex_sections.get("target_id", ""),
            "target_display_name": latex_sections.get("target_display_name", ""),
            "status": latex_sections.get("status", ""),
            "packet_id": latex_sections.get("packet_id", ""),
            "source_artifact": latex_sections.get("source_artifact", ""),
            "report_document_contract": latex_sections.get("report_document_contract", {}),
            "sections": latex_sections.get("sections", []) if isinstance(latex_sections.get("sections"), list) else [],
            "artifacts": latex_sections.get("artifacts", {}),
        },
        "timeline_paper_interpretation": {
            "status": interpretation.get("status", ""),
            "interpretation_id": interpretation.get("interpretation_id", ""),
            "unit_count": len(interpretation.get("units", [])) if isinstance(interpretation.get("units"), list) else 0,
            "report_family_coverage": interpretation.get("report_family_coverage", {}),
            "required_argument_functions": interpretation.get("required_argument_functions", {}),
        },
        "timeline_paper_blueprint": blueprint,
        "timeline_paper_sections": paper_sections,
        "timeline_formal_derivation": formal_derivation_artifact,
        "timeline_paper_diagrams": paper_diagrams,
        "paper_build_manifest": {
            "mode": blueprint.get("paper_mode", "legacy_fallback"),
            "source_artifacts": [
                rel(TIMELINE_PAPER_INTERPRETATION),
                rel(TIMELINE_PAPER_BLUEPRINT),
                rel(TIMELINE_PAPER_SECTIONS),
                rel(TIMELINE_FORMAL_DERIVATION),
                rel(TIMELINE_PAPER_DIAGRAMS),
                rel(TIMELINE_LATEX_SECTIONS),
                *([rel(PVSNP_PROOF_DELIVERY_QUEUE)] if profile["target_id"] == "p-vs-np-target" else []),
            ],
            "section_order": [row.get("section_id") for row in paper_sections.get("sections", []) if isinstance(row, dict)],
            "validation_status": "interpretive_artifacts_consumed" if paper_sections.get("status") == "timeline_paper_sections_ready" else "legacy_fallback",
        },
        "artifacts": {
            "json": rel(OUT_JSON),
            "markdown": rel(OUT_MD),
            "tex": rel(OUT_TEX),
            "pdf": rel(OUT_PDF),
        },
        "epistemic_status": "paper_draft_validation_needed",
        "validation_handoff": "Run validate_timeline_paper.py and inspect the rendered PDF before treating the draft as a paper argument.",
    }
    return report


def render_full_report_translation(report: dict[str, Any]) -> str:
    packet = report.get("timeline_latex_sections", {}) if isinstance(report.get("timeline_latex_sections"), dict) else {}
    sections = packet.get("sections", []) if isinstance(packet.get("sections"), list) else []
    contract = packet.get("report_document_contract", {}) if isinstance(packet.get("report_document_contract"), dict) else {}
    tabs = contract.get("tab_sections", []) if isinstance(contract.get("tab_sections"), list) else []
    tab_map = itemize(
        [
            f"{tab.get('tab_label', '')} -> {tab.get('section_title', '')}"
            for tab in tabs
            if isinstance(tab, dict) and clean_text(tab.get("tab_label")) and clean_text(tab.get("section_title"))
        ]
    )
    section_tex = "\n\n".join(
        str(section.get("latex") or "").strip()
        for section in sections
        if isinstance(section, dict) and clean_text(section.get("latex"))
    )
    if not section_tex:
        section_tex = r"\paragraph{Missing packet.} The timeline LaTeX section packet was not available when the paper was built."
    return rf"""
\clearpage
\appendix
\section{{Full Timeline Report Translation: Orientation}}
\label{{app:full-timeline-report-translation}}
This appendix is intentionally expansive. The main paper body compresses the argument into a coherent scientific contribution candidate; this appendix preserves the translated report material that supports that compression: current summary, problem and literature context, accumulated story, and the full timeline evidence window. It is included so the paper draft does not hide the reasoning material behind artifact references.

\paragraph{{Tab-to-section contract.}} The standalone report translation artifact maps every visible report tab to one appendix section in the same order as the HTML report. The complete standalone LaTeX report is recorded at \texttt{{{tex_escape(packet.get("artifacts", {}).get("report_tex", "agentic/reports/timeline_latex_sections/latest_report.tex"))}}}.

{tab_map}

{section_tex}
"""


def render_markdown(report: dict[str, Any]) -> str:
    lock = report["paper_narrative_goal_lock"]
    lines = [
        "# Timeline Paper Draft",
        "",
        f"- Title: {report['title']}",
        f"- Target: `{report['target_id']}`",
        f"- Independent workflow: `{report['independent_workflow']}`",
        f"- TeX: `{report['artifacts']['tex']}`",
        f"- PDF: `{report['artifacts']['pdf']}`",
        "",
        "## Invoked Skills",
        "",
        itemize(report["invoked_skills"]).replace("\\begin{itemize}", "").replace("\\end{itemize}", ""),
        "",
        "## Timeline Window",
        "",
        f"- Start: `{report['timeline_window']['start_cycle_id']}`",
        f"- End: `{report['timeline_window']['end_cycle_id']}`",
        f"- Cycles: `{report['timeline_window']['cycle_count']}`",
        "",
        f"## Latest {report['latest_steps']['requested_count']} Timeline Steps",
        "",
        f"- Start: `{report['latest_steps']['start_cycle_id']}`",
        f"- End: `{report['latest_steps']['end_cycle_id']}`",
        f"- Cycles: `{report['latest_steps']['cycle_count']}`",
        "",
        *[
            f"- `{row['cycle_id']}` ({row['branch_title']}): {row['learning']} Next: {row['next_experiment']}"
            for row in report["latest_steps"]["cycles"]
        ],
        "",
        "## Paper Narrative Goal Lock",
        "",
        f"- Subgoal: {lock['subgoal_title']}",
        f"- Thesis: {lock['coherent_narrative_thesis']}",
        f"- Anti-infinite exploration rule: {lock['anti_infinite_exploration_rule']}",
        "",
        "### Narrative Spine",
        "",
        *[f"- {item}" for item in lock["narrative_spine"]],
        "",
        "### Demotion Boundary",
        "",
        *[f"- {item}" for item in lock["excluded_detail_policy"]],
        "",
        "## Strategy Judgement",
        "",
        f"- Decision: `{report['strategy_judgement']['decision']}`",
        f"- Payoff: `{report['strategy_judgement']['payoff_potential']}`",
        f"- Alignment: `{report['strategy_judgement']['alignment_class']}`",
        "",
        "## Timeline Proof Objects",
        "",
        *[
            f"- `{obj['proof_object_id']}` ({obj['proof_status']}): {obj['title']}. Goal: {obj['theorem_goal']}"
            for obj in report.get("proof_objects", [])
        ],
        "",
        "## Validation Handoff",
        "",
        report["validation_handoff"],
    ]
    return "\n".join(lines)


def render_interpretive_tex(report: dict[str, Any]) -> str:
    blueprint = report.get("timeline_paper_blueprint", {}) if isinstance(report.get("timeline_paper_blueprint"), dict) else {}
    sections_packet = report.get("timeline_paper_sections", {}) if isinstance(report.get("timeline_paper_sections"), dict) else {}
    refs = report["references"]
    sections = sections_packet.get("sections", []) if isinstance(sections_packet.get("sections"), list) else []
    appendices = sections_packet.get("appendix_sections", []) if isinstance(sections_packet.get("appendix_sections"), list) else []
    title = clean_text(blueprint.get("title")) or report["title"]
    abstract = clean_text(blueprint.get("abstract_claim")) or report["abstract"]
    main_tex = "\n\n".join(str(row.get("latex") or "").strip() for row in sections if isinstance(row, dict) and clean_text(row.get("latex")))
    appendix_tex = "\n\n".join(str(row.get("latex") or "").strip() for row in appendices if isinstance(row, dict) and clean_text(row.get("latex")))
    translated_report = render_full_report_translation(report)
    date = dt.datetime.now().strftime("%B %d, %Y")
    return rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{fontspec}}
\usepackage{{amsmath,amssymb,amsthm,mathtools}}
\usepackage{{booktabs,longtable,array}}
\usepackage{{enumitem}}
\usepackage{{tikz}}
\usetikzlibrary{{arrows.meta,positioning,shapes.geometric}}
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{{hyperref}}
\setlist[itemize]{{leftmargin=*,itemsep=0.25em,topsep=0.25em}}
\newtheorem{{proposition}}{{Proposition}}

\title{{{tex_escape(title)}}}
\author{{Abducer Interpretive Timeline Paper Workflow}}
\date{{{tex_escape(date)}}}

\begin{{document}}
\maketitle

\begin{{abstract}}
{tex_escape_mathish(abstract)}
\end{{abstract}}

\section*{{Paper Build Manifest}}
This paper is generated from an interpretation pipeline rather than a flat timeline dump. The build consumes a report interpretation, argument blueprint, synthesized paper sections, formal derivation artifact, generated diagram, and translated report appendix. The main body is bounded by the blueprint; broad report coverage is preserved in appendices and artifacts.

\paragraph{{Paper mode.}} {tex_escape(blueprint.get("paper_mode", "not recorded"))}
\paragraph{{Main thesis.}} {tex_escape_mathish(blueprint.get("main_thesis", ""))}
\paragraph{{Non-claims.}}
{itemize(blueprint.get("non_claims", []))}

{main_tex}

{render_proof_objects_tex(report.get("proof_objects", []))}

{appendix_tex}

{translated_report}

{render_latest_steps_tex(report.get("latest_steps", {}))}

{render_bibliography(refs)}

\end{{document}}
"""


def render_tex(report: dict[str, Any]) -> str:
    sections_packet = report.get("timeline_paper_sections", {}) if isinstance(report.get("timeline_paper_sections"), dict) else {}
    if sections_packet.get("status") == "timeline_paper_sections_ready":
        return render_interpretive_tex(report)
    refs = report["references"]
    lock = report["paper_narrative_goal_lock"]
    cite_problem = cite_by_role(refs, ["problem", "clay", "yang-mills"])
    cite_os = cite_by_role(refs, ["os", "reflection", "schwinger"])
    cite_rg = cite_by_role(refs, ["constructive", "rg", "balaban", "continuum"])
    cite_artifacts = "artifact-timeline,artifact-judge,artifact-contribution"
    stages = report["problem_space"]["literature_stages"]
    stage_items = [
        f"{clean_text(stage.get('period'))}: {clean_text(stage.get('title'))}. {clean_text(stage.get('core_shift'))}"
        for stage in stages
        if isinstance(stage, dict)
    ]
    contribution_table = render_contribution_table(report["contributions"])
    cycle_items = [
        f"{row['cycle_id']} ({row['branch_title']}): {row['learning']} Next: {row['next_experiment']}"
        for row in report["timeline_window"]["cycles"]
    ]
    narrative_spine_items = list(lock["narrative_spine"])
    included_policy_items = list(lock["included_material_policy"])
    excluded_policy_items = list(lock["excluded_detail_policy"])
    decisive_work_items = list(lock["decisive_next_work"])
    stop_or_demote_items = list(lock["stop_or_demote_when"])
    coherence_check_items = list(lock["coherence_checks"])
    contribution_items = [
        f"{clean_text(row.get('smallest_honest_claim'))} Evidence: {clean_text(row.get('cycle_id'))}. Boundary: {clean_text(row.get('overclaim_boundary'))}"
        for row in report["contributions"]
    ]
    date = dt.datetime.now().strftime("%B %d, %Y")
    return rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{fontspec}}
\usepackage{{amsmath,amssymb,amsthm,mathtools}}
\usepackage{{booktabs,longtable,array}}
\usepackage{{enumitem}}
\usepackage{{tikz}}
\usetikzlibrary{{arrows.meta,positioning,shapes.geometric}}
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{{hyperref}}
\setlist[itemize]{{leftmargin=*,itemsep=0.25em,topsep=0.25em}}
\newtheorem{{proposition}}{{Proposition}}

\title{{{tex_escape(report['title'])}}}
\author{{Abducer Timeline Paper Workflow}}
\date{{{tex_escape(date)}}}

\begin{{document}}
\maketitle

\begin{{abstract}}
{tex_escape(report['abstract'])}
\end{{abstract}}

\section{{Introduction and Problem Space}}
The target problem is {tex_escape(report['problem_space']['problem_name'])}. In the Clay formulation, the aim is not merely to write plausible gauge-theoretic formulas, but to construct a nontrivial quantum Yang--Mills theory and prove a positive mass gap in that same theory \cite{{{cite_problem}}}. The timeline analyzed here is therefore interpreted as a contribution to the proof architecture, not as a final proof.

The historical pressure is organized around three obligations. First, the construction must survive the continuum limit rather than remain fixed-regulator. Second, Euclidean positivity must support a reconstruction of the physical Hilbert space rather than be postulated after the fact \cite{{{cite_os}}}. Third, spectral language must be attached to reconstructed gauge-invariant excitations, not to a proxy Hamiltonian. The accumulated timeline connects these obligations to a finite Wilson/OS positivity test \cite{{{cite_artifacts}}}.

\subsection{{Related Work as Route Pressure}}
{itemize(stage_items)}

\section{{Timeline Evidence and Current Strategy}}
The judged timeline window runs from {tex_escape(report['timeline_window']['start_cycle_id'])} to {tex_escape(report['timeline_window']['end_cycle_id'])}. The strategy judge classifies the current route as {tex_escape(report['strategy_judgement']['alignment_class'])}, with decision {tex_escape(report['strategy_judgement']['decision'])} and payoff {tex_escape(report['strategy_judgement']['payoff_potential'])}.

The route is best read as a bridge program: extract a finite obstruction from reflected Wilson data, then ask whether the obstruction or positivity condition transfers to continuum OS reconstruction. This keeps the paper aligned with the main target while guarding against overclaiming fixed-collar or finite-matrix results \cite{{{cite_rg}}}.

\subsection{{Evidence Window}}
{itemize(cycle_items)}

\section{{Paper Narrative Goal Lock}}
The paper goal is deliberately narrower than the discovery loop. The active subgoal is {tex_escape(lock['subgoal_title'])}. Its coherent narrative thesis is: {tex_escape(lock['coherent_narrative_thesis'])}

\paragraph{{Anti-infinite exploration rule.}}
{tex_escape(lock['anti_infinite_exploration_rule'])}

\subsection{{Narrative Spine}}
{itemize(narrative_spine_items)}

\subsection{{What Belongs in the Paper Body}}
{itemize(included_policy_items)}

\subsection{{What Must Be Demoted Out of the Body}}
{itemize(excluded_policy_items)}

\subsection{{Decisive Next Work for This Paper Goal}}
{itemize(decisive_work_items)}

\subsection{{Stop or Demote Criteria}}
{itemize(stop_or_demote_items)}

\subsection{{Coherence Checks}}
{itemize(coherence_check_items)}

\section{{Specific Contributions}}
The draft makes scoped contribution claims. They are valuable only under the stated validation boundaries.

{contribution_table}

\subsection{{Contribution Statements}}
{itemize(contribution_items)}

\section{{Mechanism and Explanation}}
The central mechanism is a quotient calculation near the rank-one OS direction. Earlier formulations treated the Hamiltonian or decay route too globally. The timeline instead sharpened a local test: Wilson observables near a reflection plane define a finite reflected Gram matrix; after normalization and quotienting by constants, first- and second-order positivity constraints become computable. The gain is conceptual as well as technical: the analysis can now say what would count as a finite same-theory obstruction, what would count as a bridge lemma, and what would merely be a proxy artifact.

The negative result would also be informative. If the finite block violates the quotient positivity conditions in the same Wilson observable algebra, the route has discovered a falsifier for that proposed bridge. If it does not, the next burden is analytic: derive the Wilson boundary coefficients and prove uniform control of the collar remainder.

{build_diagram_tikz()}

{build_formal_derivation()}

\section{{Reference and Artifact Management}}
This paper draft uses two kinds of references. External literature references explain the target problem and route obligations. Local artifact references document what the discovery timeline actually produced. Artifact citations are evidence about the run state, not independent mathematical theorems.

\section{{Discussion: What This Paper Draft Does and Does Not Claim}}
The draft claims that the timeline has isolated a paper-level subgoal: a finite Wilson/OS tangent-cone obstruction program with explicit validation debt. It does not claim Yang--Mills existence, continuum nontriviality, or a mass gap. The strongest honest reading is that the current timeline has turned diffuse strategy pressure into a testable local object and a paper-note-ready contribution candidate.

\paragraph{{Next decisive test.}}
{tex_escape(report['strategy_judgement']['next_decisive_test'])}

\paragraph{{When to stop.}}
{tex_escape(report['strategy_judgement']['when_to_stop'])}

\paragraph{{Validation handoff.}}
{tex_escape(report['validation_handoff'])}

\section{{Conclusion}}
The timeline-paper workflow shows how a long-horizon discovery process can be converted into a scientific paper draft without pretending that the discovery loop has solved the target problem. The current paper-level object is the Wilson/OS finite obstruction program; its scientific value depends on whether the next derivation can compute the boundary OPE matrices $H$ and $K$ in the same theory and control the remainder uniformly.

{render_full_report_translation(report)}

{render_latest_steps_tex(report.get("latest_steps", {}))}

{render_bibliography(refs)}

\end{{document}}
"""


def find_latex_engine(preferred: str = "xelatex") -> list[str]:
    if preferred == "latexmk":
        found = shutil.which("latexmk")
        if found:
            return [found, "-pdf", "-xelatex"]
    candidates = [preferred, "xelatex", "pdflatex", "lualatex"]
    for name in dict.fromkeys(candidates):
        found = shutil.which(name)
        if found:
            return [found]
    raise FileNotFoundError("No LaTeX engine found.")


def sanitize_rendered_tex(tex: str) -> str:
    tex = tex.replace("∘", r"\circ ")
    tex = tex.replace(r"\left{", r"\left\{").replace(r"\right}", r"\right\}")

    def escape_text_body(match: re.Match[str]) -> str:
        body = match.group(1).replace("_", r"\_")
        return r"\text{" + body + "}"

    return re.sub(r"\\text\{([^{}]*)\}", escape_text_body, tex)


def compile_pdf(tex_path: Path, pdf_path: Path) -> dict[str, Any]:
    engine = find_latex_engine("latexmk")
    if Path(engine[0]).name == "latexmk":
        cmd = engine + ["-interaction=nonstopmode", "-halt-on-error", tex_path.name]
        passes = 1
    else:
        cmd = engine + ["-interaction=nonstopmode", "-halt-on-error", tex_path.name]
        passes = 2
    workdir = tex_path.parent
    stdout = ""
    stderr = ""
    for _ in range(passes):
        result = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, encoding="utf-8", errors="replace")
        stdout += result.stdout
        stderr += result.stderr
        if result.returncode != 0:
            raise RuntimeError(f"LaTeX failed with {' '.join(cmd)}\n{stdout}\n{stderr}")
    built_pdf = tex_path.with_suffix(".pdf")
    if built_pdf != pdf_path:
        pdf_path.write_bytes(built_pdf.read_bytes())
    for path in workdir.glob("latest.*"):
        if path.suffix in {".aux", ".fdb_latexmk", ".fls", ".log", ".out", ".toc"}:
            path.unlink()
    return {"engine": " ".join(cmd), "pdf": rel(pdf_path), "stdout_tail": stdout[-1200:], "stderr_tail": stderr[-1200:]}


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    write_json(OUT_JSON, report)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    OUT_TEX.write_text(sanitize_rendered_tex(render_tex(report)), encoding="utf-8")
    compile_info = compile_pdf(OUT_TEX, OUT_PDF)
    report["compile"] = compile_info
    report["artifacts"]["pdf"] = rel(OUT_PDF)
    write_json(OUT_JSON, report)
    print(f"wrote {rel(OUT_TEX)}")
    print(f"wrote {rel(OUT_PDF)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
