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

"""Validate the Hamiltonian spectral-gap derivation artifact."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


REPORT = ROOT / "agentic/reports/hamiltonian_gap_derivation/latest.json"
HTML = ROOT / "agentic/reports/hamiltonian_gap_derivation/latest.html"
CURRENT_TARGET = ROOT / "agentic/state/current_target.json"
YANG_MILLS_TARGET = "yang-mills-existence-and-mass-gap-target"
REQUIRED_SYMBOLS = ["H_YM", "Omega", "U(t)", "H", "P0", "Pperp", "E_H(B)", "Delta"]
REQUIRED_FORMULA_MARKERS = [
    "U(t)=e^{-itH}",
    "P_\\perp=I-P_0",
    "E_H((0,\\Delta))P_\\perp=0",
    "\\operatorname{spec}(H|_{P_\\perp\\mathcal H_{\\mathrm{YM}}})\\subset[\\Delta,\\infty)",
    "\\langle\\psi,H\\psi\\rangle",
    "\\ge\\Delta\\|\\psi\\|^2",
    "C_A(t)=",
    "e^{-\\Delta t}",
    "\\liminf_{a\\to0}\\Delta_a\\ge\\Delta>0",
]
REQUIRED_PROGRESS_WHY_MARKERS = [
    "Hamiltonian",
    "density",
    "cutoff",
    "continuum",
    "nontrivial",
    "interacting",
]


def flatten(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(flatten(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(flatten(item) for item in value)
    return clean_text(value)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_derivation(item: dict[str, Any], index: int) -> None:
    subject = f"derivation {index} ({item.get('candidate_id', 'unknown')})"
    for field in [
        "mathematical_subclaim",
        "symbols",
        "assumptions",
        "derivation_steps",
        "candidate_derivation",
        "what_would_count_as_progress",
        "what_does_not_count",
    ]:
        require(field in item, f"{rel(REPORT)} {subject} missing `{field}`")
    symbols = item["symbols"]
    require(isinstance(symbols, dict), f"{rel(REPORT)} {subject} symbols must be an object")
    for symbol in REQUIRED_SYMBOLS:
        require(symbol in symbols, f"{rel(REPORT)} {subject} missing symbol `{symbol}`")
    assumptions = item["assumptions"]
    require(isinstance(assumptions, list) and len(assumptions) >= 5, f"{rel(REPORT)} {subject} needs at least five assumptions")
    steps = item["derivation_steps"]
    require(isinstance(steps, list) and len(steps) >= 7, f"{rel(REPORT)} {subject} needs at least seven derivation steps")
    for step in steps:
        step_label = f"{subject} step {step.get('step', '?')}"
        context = step.get("equation_context")
        require(isinstance(context, dict), f"{rel(REPORT)} {step_label} missing equation context")
        definitions = context.get("definitions", [])
        assumptions_used = context.get("assumptions_used", [])
        valid_when = context.get("valid_when", [])
        require(isinstance(definitions, list) and len(definitions) >= 2, f"{rel(REPORT)} {step_label} needs equation definitions")
        require(isinstance(assumptions_used, list) and assumptions_used, f"{rel(REPORT)} {step_label} needs assumptions used")
        require(isinstance(valid_when, list) and len(valid_when) >= 2, f"{rel(REPORT)} {step_label} needs validity conditions")
        context_text = flatten(context).lower()
        require(
            any(marker in context_text for marker in ["reconstructed", "spectral", "vacuum", "cutoff", "observable"]),
            f"{rel(REPORT)} {step_label} equation context lacks mathematical grounding",
        )
    text = flatten(item)
    for marker in REQUIRED_FORMULA_MARKERS:
        require(marker in text, f"{rel(REPORT)} {subject} lacks formula marker `{marker}`")
    for marker in ["spectral theorem", "vacuum", "excitation", "continuum", "OS", "Wightman", "gauge-invariant"]:
        require(marker.lower() in text.lower(), f"{rel(REPORT)} {subject} lacks mathematical concept `{marker}`")
    require("does not prove yang-mills" not in item.get("candidate_derivation", "").lower(), f"{rel(REPORT)} {subject} confused derivation with proof disclaimer")
    progress_items = item["what_would_count_as_progress"]
    require(isinstance(progress_items, list) and len(progress_items) >= 4, f"{rel(REPORT)} {subject} needs progress criteria")
    progress_text = flatten(progress_items)
    for progress_index, progress in enumerate(progress_items, start=1):
        require(isinstance(progress, dict), f"{rel(REPORT)} {subject} progress item {progress_index} must have structured claim/why fields")
        require(clean_text(progress.get("claim")), f"{rel(REPORT)} {subject} progress item {progress_index} missing claim")
        why = clean_text(progress.get("why"))
        require(why, f"{rel(REPORT)} {subject} progress item {progress_index} missing why explanation")
        require(len(why.split()) >= 18, f"{rel(REPORT)} {subject} progress item {progress_index} why explanation is too thin")
    for marker in REQUIRED_PROGRESS_WHY_MARKERS:
        require(marker.lower() in progress_text.lower(), f"{rel(REPORT)} {subject} progress explanations lack `{marker}`")
    require(len(item["what_does_not_count"]) >= 4, f"{rel(REPORT)} {subject} needs rejection criteria")


def validate_html(report: dict[str, Any]) -> None:
    if not HTML.exists():
        fail(f"missing rendered derivation HTML: {rel(HTML)}")
    text = HTML.read_text(encoding="utf-8")
    lower = text.lower()
    forbidden = ["<script src=", "<link ", "http://", "https://", "@import", "<img "]
    found = [item for item in forbidden if item in lower]
    if found:
        fail(f"{rel(HTML)} contains external or non-embedded asset references: {found}")
    if text.count("<math") < 7:
        fail(f"{rel(HTML)} must render each derivation step with MathML `<math>` blocks")
    for marker in [
        "<annotation encoding=\"application/x-tex\">U(t)=e^{-itH}",
        "<annotation encoding=\"application/x-tex\">E_H((0,\\Delta))P_\\perp=0",
        "<annotation encoding=\"application/x-tex\">C_A(t)=",
        "<annotation encoding=\"application/x-tex\">\\inf\\sigma",
    ]:
        if marker not in text:
            fail(f"{rel(HTML)} missing TeX annotation marker `{marker}`")
    for visible in [
        "Hamiltonian Spectral-Gap Derivation",
        "Rendered Derivation",
        "Equation Context",
        "Definition:",
        "Assumptions used:",
        "Valid when:",
        "Open obligation",
        "Why:",
        report["target_id"],
    ]:
        if visible not in text:
            fail(f"{rel(HTML)} missing visible phrase `{visible}`")


def main() -> int:
    report = load_json_object(REPORT)
    current = load_json_object(CURRENT_TARGET)
    require(report.get("target_id") == current.get("target_id"), f"{rel(REPORT)} target does not match active target")
    require(report.get("target_id") == YANG_MILLS_TARGET, f"{rel(REPORT)} target is not Yang-Mills")
    require(report.get("report_mode") == "Hamiltonian spectral-gap mathematical derivation", f"{rel(REPORT)} has wrong report mode")
    derivations = report.get("derivations", [])
    require(isinstance(derivations, list) and derivations, f"{rel(REPORT)} must contain derivations")
    for index, item in enumerate(derivations, start=1):
        require(isinstance(item, dict), f"{rel(REPORT)} derivation {index} must be an object")
        validate_derivation(item, index)
    validate_html(report)
    print(f"validated Hamiltonian gap derivation for {report['target_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
