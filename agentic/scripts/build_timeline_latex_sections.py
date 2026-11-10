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
"""Translate the discovery marathon report into report-shaped LaTeX sections."""

from __future__ import annotations

import html as html_lib
import json
import re
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, stable_id, utc_now, write_json
from target_profiles import target_profile


FULL_TIMELINE_HTML = ROOT / "agentic/reports/discovery_marathon/full_timeline.html"
LATEST_JSON = ROOT / "agentic/reports/discovery_marathon/latest.json"
OUT_DIR = ROOT / "agentic/reports/timeline_latex_sections"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
OUT_TEX = OUT_DIR / "latest.tex"
OUT_REPORT_TEX = OUT_DIR / "latest_report.tex"

TRANSLATOR_SKILLS = [
    "timeline-report-latex-composer",
    "timeline-summary-latex-translator",
    "timeline-problem-literature-latex-translator",
    "timeline-story-latex-translator",
    "timeline-cycle-latex-translator",
]

BASE_REPORT_TAB_SECTIONS = [
    {
        "tab_id": "overview",
        "tab_label": "Summary",
        "section_id": "summary",
        "section_title": "Summary",
    },
    {
        "tab_id": "physics_math_strategy",
        "tab_label": "Physics & Maths Strategy",
        "section_id": "physics_math_strategy",
        "section_title": "Physics And Maths Strategy",
    },
    {
        "tab_id": "timeline",
        "tab_label": "Timeline From cycle window",
        "section_id": "timeline",
        "section_title": "Content-Specific Full Timeline",
    },
    {
        "tab_id": "ranked_queue",
        "tab_label": "Ranked Analyses",
        "section_id": "ranked_analyses",
        "section_title": "Current Ranked Next-Analysis Queue",
    },
    {
        "tab_id": "qualitative",
        "tab_label": "Qualitative Graph",
        "section_id": "qualitative_graph",
        "section_title": "Qualitative Mechanistic Graph",
    },
    {
        "tab_id": "gedanken",
        "tab_label": "Gedanken Experiments",
        "section_id": "gedanken",
        "section_title": "Gedanken Experiments",
    },
    {
        "tab_id": "parsimonious",
        "tab_label": "PMP Probes",
        "section_id": "parsimonious",
        "section_title": "Parsimonious Probe Control",
    },
    {
        "tab_id": "contributions",
        "tab_label": "Contributions",
        "section_id": "contributions",
        "section_title": "Scientific Contribution Monitor",
    },
    {
        "tab_id": "literature",
        "tab_label": "Problem & Literature",
        "section_id": "problem_literature",
        "section_title": "Target Problem And Literature Evolution",
    },
    {
        "tab_id": "macro_strategy",
        "tab_label": "Macro Strategies",
        "section_id": "macro_strategies",
        "section_title": "Macro Strategies",
    },
    {
        "tab_id": "strategy_judge",
        "tab_label": "Strategy Judge",
        "section_id": "strategy_judge",
        "section_title": "Strategy Progression Judge",
    },
    {
        "tab_id": "story",
        "tab_label": "Physics Story",
        "section_id": "physics_story",
        "section_title": "Accumulated Physics Story",
    },
]


ACTIVE_TARGET_ID = ""


def infer_target_id(payload: dict[str, Any]) -> str:
    embedded_target = clean_text(payload.get("target_id"))
    report_target = clean_text(payload.get("report", {}).get("target_id")) if isinstance(payload.get("report"), dict) else ""
    latest = load_optional_json(LATEST_JSON)
    latest_target = clean_text(latest.get("target_id")) if isinstance(latest, dict) else ""
    literature = load_optional_json(ROOT / "agentic/reports/target_literature_evolution/latest.json")
    literature_target = clean_text(literature.get("target_id")) if isinstance(literature, dict) else ""
    return embedded_target or report_target or latest_target or literature_target or "yang-mills-existence-and-mass-gap-target"


def report_tab_sections(target_id: str | None = None) -> list[dict[str, Any]]:
    profile = target_profile(target_id or ACTIVE_TARGET_ID)
    rows = [dict(row) for row in BASE_REPORT_TAB_SECTIONS]
    for row in rows:
        if row["section_id"] == "physics_math_strategy":
            if profile["target_id"] == "p-vs-np-target":
                row["tab_label"] = profile.get("strategy_tab_label", "Complexity Strategy")
                row["section_title"] = "Complexity Strategy"
            elif profile["target_id"] != "yang-mills-existence-and-mass-gap-target":
                row["tab_label"] = profile.get("strategy_tab_label", "Mathematical Strategy")
                row["section_title"] = profile.get("strategy_tab_label", "Mathematical Strategy")
        if row["section_id"] == "physics_story":
            if profile["target_id"] == "p-vs-np-target":
                row["tab_label"] = profile.get("story_tab_label", "Proof Strategy Story")
                row["section_title"] = "Accumulated Proof Strategy Story"
            elif profile["target_id"] != "yang-mills-existence-and-mass-gap-target":
                row["tab_label"] = profile.get("story_tab_label", "Proof Strategy Story")
                row["section_title"] = profile.get("story_tab_label", "Proof Strategy Story")
    return rows


REPORT_TAB_SECTIONS = report_tab_sections()


_INLINE_MATH_RE = re.compile(r"\\\((.*?)\\\)", re.DOTALL)
_DISPLAY_MATH_RE = re.compile(r"\\\[(.*?)\\\]", re.DOTALL)
_MATH_TOKEN_RE = re.compile(
    r"(?<![A-Za-z])"
    r"(?:[A-Za-z][A-Za-z0-9]{0,6})"
    r"(?:_(?:\{[A-Za-z0-9+\-]+\}|[A-Za-z0-9]+|[+\-])|\^(?:\{[A-Za-z0-9+\-]+\}|[0-9]+|[A-Za-z]+))"
    r"(?:_(?:\{[A-Za-z0-9+\-]+\}|[A-Za-z0-9]+|[+\-])|\^(?:\{[A-Za-z0-9+\-]+\}|[0-9]+|[A-Za-z]+))*"
)
_POWER_RATIO_RE = re.compile(r"(?<![A-Za-z])(?:[A-Za-z]\^\d+)(?:/[A-Za-z]\^\d+)+")
_FUNCTION_POWER_RE = re.compile(r"\b(?:alpha|omega|lambda|Lambda)\([A-Za-z0-9_,+\- ]+\)\^\d+")
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_MATH_PHRASE_PATTERNS = [
    (re.compile(r"\bP\s*!=\s*NP\b"), r"P \ne NP"),
    (re.compile(r"\bP\s+\\ne\s+NP\b"), r"P \ne NP"),
    (re.compile(r"\bSAT\s+notin\s+P/poly\b"), r"SAT\notin P/poly"),
    (re.compile(r"\bNP\s+not\s+subset\s+P/poly\b"), r"NP\not\subset P/poly"),
    (re.compile(r"\bSAT\s+in\s+SIZE\(([^)]*)\)"), r"SAT\in SIZE(\1)"),
    (re.compile(r"(?<![A-Za-z])\\?tilde\s*O\(([^)]*)\)"), r"\widetilde{O}(\1)"),
    (re.compile(r"(?<![A-Za-z])\\?tildeO\(([^)]*)\)"), r"\widetilde{O}(\1)"),
    (re.compile(r"(?<![A-Za-z])\\?widetilde\s*O\(([^)]*)\)"), r"\widetilde{O}(\1)"),
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
    "AC0",
    "CNF",
    "CTSR",
    "DNNF",
    "DTSR",
    "EF",
    "EqSAT",
    "FormulaEval",
    "LB",
    "MCSP",
    "MKtP",
    "NP",
    "P",
    "Psys",
    "QCTSR",
    "ROBDD",
    "SAT",
    "SIZE",
    "TSR",
}


def repair_legacy_controls(text: str) -> str:
    text = (
        text.replace("\x07amma", r"\Gamma")
        .replace("\x07delta", r"\delta")
        .replace("\x07lpha", r"\alpha")
        .replace("\x07eta", r"\eta")
    )
    return _CONTROL_RE.sub("", text)


def preferred_text(value: Any) -> str:
    if isinstance(value, dict):
        for key in ("text", "latex", "latex_render", "html", "title", "name", "description", "summary"):
            if clean_text(value.get(key)):
                return preferred_text(value.get(key))
        return "; ".join(f"{key}: {preferred_text(item)}" for key, item in value.items() if clean_text(item))
    if isinstance(value, list):
        return "; ".join(preferred_text(item) for item in value if clean_text(preferred_text(item)))
    text = html_lib.unescape(clean_text(value))
    text = _HTML_TAG_RE.sub("", text)
    return repair_legacy_controls(text)


def normalize_tex_formula(value: Any) -> str:
    formula = repair_legacy_controls(html_lib.unescape(clean_text(value)))
    formula = (
        formula.replace(r"\gt", ">")
        .replace(r"\lt", "<")
        .replace(r"\geqslant", r"\ge")
        .replace(r"\leqslant", r"\le")
        .replace(r"\Kappa", r"\kappa")
        .replace(r"\{", "{")
        .replace(r"\}", "}")
        .replace(r"\widetilde O", r"\widetilde{O}")
        .replace(r"\tilde O", r"\widetilde{O}")
        .replace("∘", r"\circ ")
        .replace("κ", r"\kappa")
    )
    formula = strip_math_delimiters(formula)
    return formula or r"\text{formula not recorded}"


def strip_math_delimiters(formula: str) -> str:
    """Return a bare formula fragment suitable for caller-chosen math delimiters."""
    formula = formula.strip()
    while True:
        inline = re.fullmatch(r"\\\((.*)\\\)", formula, flags=re.DOTALL)
        display = re.fullmatch(r"\\\[(.*)\\\]", formula, flags=re.DOTALL)
        dollars = re.fullmatch(r"\$\$(.*)\$\$", formula, flags=re.DOTALL)
        single_dollars = re.fullmatch(r"\$(.*)\$", formula, flags=re.DOTALL)
        match = inline or display or dollars or single_dollars
        if not match:
            return formula
        formula = match.group(1).strip()


def tex_escape_plain(value: Any) -> str:
    text = preferred_text(value)
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
    text = (
        text.replace("–", "--")
        .replace("—", "---")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("≥", ">=")
        .replace("≤", "<=")
        .replace("→", "->")
        .replace("∘", r"\(\circ\)")
        .replace("α", r"\(\alpha\)")
        .replace("β", r"\(\beta\)")
        .replace("γ", r"\(\gamma\)")
        .replace("δ", r"\(\delta\)")
        .replace("ε", r"\(\epsilon\)")
        .replace("η", r"\(\eta\)")
        .replace("θ", r"\(\theta\)")
        .replace("λ", r"\(\lambda\)")
        .replace("χ", r"\(\chi\)")
        .replace("Ω", r"\(\Omega\)")
        .replace("Φ", r"\(\Phi\)")
        .replace("Ξ", r"\(\Xi\)")
        .replace("⊕", r"\(\oplus\)")
        .replace("κ", "kappa")
    )
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def normalize_formula_fragment(fragment: str) -> str:
    formula = fragment.replace("κ", "kappa")
    formula = formula.replace(r"\Kappa", r"\kappa").replace("Kappa", r"\kappa").replace("kappa", r"\kappa")
    for name in ["epsilon", "lambda", "Lambda", "omega", "alpha", "delta", "tau", "xi", "eta", "rho", "phi", "Phi"]:
        formula = re.sub(rf"\b{name}(?=_|\()", rf"\\{name}", formula)
    formula = re.sub(r"_(?!\{)([A-Za-z0-9]+|[+\-])", r"_{\1}", formula)
    formula = re.sub(r"\^(?!\{)([0-9]+|[A-Za-z]+)", r"^{\1}", formula)
    for name in ["alpha", "delta", "epsilon", "eta", "lambda", "min", "omega", "phi", "Phi", "rho", "tau", "xi"]:
        command = "\\" + name if name != "min" else r"\min"
        formula = re.sub(rf"(?<=[{{,]){name}(?=[,}}>])", lambda _m, command=command: command, formula)
    return formula


def group_repeated_subscripts(match: re.Match[str]) -> str:
    parts = match.group(0).split("_")
    return parts[0] + "_{" + ",".join(parts[1:]) + "}"


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


def tex_inline_math(formula: str) -> str:
    return r"\(" + normalize_inline_formula(formula) + r"\)"


def expand_math_phrase(match: re.Match[str], formula: str) -> str:
    expanded = formula
    for index, group in enumerate(match.groups(), start=1):
        expanded = expanded.replace(rf"\{index}", group or "")
    return expanded


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
    if any(token.startswith(prefix) for prefix in ("AC0", "Gamma", "RealSAT", "TransparentRow", "LeastClosed", "ForcedRows")):
        return True
    if token in _FORMULA_WORDS and len(token) > 1:
        return False
    return False


def tex_escape_mathish(value: Any) -> str:
    text = preferred_text(value).replace("κ", "kappa")
    if not text:
        return ""
    placeholders: dict[str, str] = {}

    def store_math(formula: str, *, display: bool = False) -> str:
        key = f"@@MATH{len(placeholders)}@@"
        normalized = normalize_inline_formula(formula)
        placeholders[key] = "\\[\n" + normalized + "\n\\]" if display else r"\(" + normalized + r"\)"
        return key

    def protect_display(match: re.Match[str]) -> str:
        return store_math(match.group(1), display=True)

    def protect_inline(match: re.Match[str]) -> str:
        return store_math(match.group(1))

    text = _DISPLAY_MATH_RE.sub(protect_display, text)
    text = _INLINE_MATH_RE.sub(protect_inline, text)
    for pattern, formula in _MATH_PHRASE_PATTERNS:
        text = pattern.sub(lambda match, formula=formula: store_math(expand_math_phrase(match, formula)), text)
    text = text.replace("+/-", "@@PLUSMINUS@@")

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
                token_parts.append(tex_escape_plain(leading) + placeholders[core] + tex_escape_plain(trailing))
            elif looks_like_inline_formula_token(core):
                token_parts.append(tex_escape_plain(leading) + tex_inline_math(core) + tex_escape_plain(trailing))
            else:
                token_parts.append(tex_escape_plain(token))
        rendered_parts.append("".join(token_parts))
    escaped = "".join(rendered_parts).replace("@@PLUSMINUS@@", r"\(\pm\)")
    for key, formula in placeholders.items():
        escaped = escaped.replace(key, formula)
    return escaped


def latex_list(items: list[Any], *, limit: int | None = None) -> str:
    rows = [item for item in items if clean_text(preferred_text(item))]
    if limit is not None:
        rows = rows[:limit]
    if not rows:
        return "\\begin{itemize}\n\\item None recorded.\n\\end{itemize}"
    return "\\begin{itemize}\n" + "\n".join(f"\\item {tex_escape_mathish(row)}" for row in rows) + "\n\\end{itemize}"


def latex_ordered(items: list[Any], *, limit: int | None = None) -> str:
    rows = [item for item in items if clean_text(preferred_text(item))]
    if limit is not None:
        rows = rows[:limit]
    if not rows:
        return "\\begin{enumerate}\n\\item None recorded.\n\\end{enumerate}"
    return "\\begin{enumerate}\n" + "\n".join(f"\\item {tex_escape_mathish(row)}" for row in rows) + "\n\\end{enumerate}"


def latex_formula_block(value: Any, *, valid_when: Any = "") -> str:
    formula = normalize_tex_formula(value)
    valid = preferred_text(valid_when)
    suffix = f"\n\\emph{{Valid when:}} {tex_escape_mathish(valid)}" if valid else ""
    return "\\[\n" + formula + "\n\\]" + suffix


def section(label: str, title: str, body: str, source_fields: list[str], skill: str) -> dict[str, Any]:
    tab = next((row for row in report_tab_sections(ACTIVE_TARGET_ID) if row["section_id"] == label), {})
    return {
        "section_id": label,
        "source_tab_id": tab.get("tab_id", label),
        "source_tab_label": tab.get("tab_label", title),
        "title": title,
        "latex": clean_tex_lines(body),
        "source_fields": source_fields,
        "translator_skill": skill,
        "epistemic_status": "latex_translation_validation_needed",
    }


def clean_tex_lines(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.strip().splitlines()) + "\n"


def load_embedded_payload() -> dict[str, Any]:
    if not FULL_TIMELINE_HTML.exists():
        return {}
    text = FULL_TIMELINE_HTML.read_text(encoding="utf-8")
    marker = '<script id="marathon-data" type="application/json">'
    if marker not in text:
        return {}
    embedded = text.split(marker, 1)[1].split("</script>", 1)[0]
    payload = json.loads(html_lib.unescape(embedded))
    return payload if isinstance(payload, dict) else {}


def build_timeline_section(payload: dict[str, Any]) -> dict[str, Any]:
    cycles = payload.get("timeline_cycles", []) if isinstance(payload.get("timeline_cycles"), list) else []
    start = payload.get("timeline_start_cycle", "")
    blocks = [
        "\\section{Content-Specific Full Timeline}",
        "\\label{sec:report-timeline}",
        tex_escape_mathish(
            f"Visible timeline starts at cycle-{int(start):04d}, where the run shifted into content-specific mathematical work. "
            "Each cycle is rendered as a report card with learning, pressure, derivation, equations, falsifiers, and next analysis."
            if str(start).isdigit()
            else "Visible timeline starts at the report-selected content-specific window."
        ),
    ]
    for cycle in cycles:
        if not isinstance(cycle, dict):
            continue
        title = f"{preferred_text(cycle.get('cycle_id'))}: {preferred_text(cycle.get('branch_title'))}"
        blocks.append(f"\\subsection*{{{tex_escape_mathish(title)}}}")
        blocks.append(
            "\\paragraph{Execution.} "
            + tex_escape_mathish(
                f"{cycle.get('execution_mode', 'mode?')}; {cycle.get('engine', 'engine?')}; "
                f"attempt {cycle.get('api_attempt') or cycle.get('codex_attempt') or 'not recorded'}; "
                f"{cycle.get('research_seconds_elapsed', 0)} seconds; "
                f"{cycle.get('lemma_count', 0)} lemmas, {cycle.get('equation_count', 0)} equations, "
                f"{cycle.get('derivation_step_count', 0)} derivation steps, {cycle.get('falsifier_count', 0)} falsifiers."
            )
        )
        blocks.append("\\paragraph{Learning.} " + tex_escape_mathish(cycle.get("mathematical_learning")))
        blocks.append("\\paragraph{Pressure.} " + tex_escape_mathish(cycle.get("blocking_gap")))
        derivation_steps = cycle.get("derivation_steps", []) if isinstance(cycle.get("derivation_steps"), list) else []
        if derivation_steps:
            blocks.append("\\paragraph{Derivation steps.}\n" + latex_ordered(derivation_steps))
        equations = cycle.get("equations", []) if isinstance(cycle.get("equations"), list) else []
        if equations:
            eq_blocks = []
            for index, eq in enumerate(equations, start=1):
                if isinstance(eq, dict):
                    eq_blocks.append(
                        f"\\paragraph{{Equation {index}: {tex_escape_mathish(eq.get('label') or '')}.}}\n"
                        + latex_formula_block(eq.get("latex_render") or eq.get("latex"), valid_when=eq.get("valid_when"))
                    )
            blocks.extend(eq_blocks)
        blocks.append("\\paragraph{Next analysis.} " + tex_escape_mathish(cycle.get("next_experiment")))
        falsifiers = cycle.get("falsifiers", []) if isinstance(cycle.get("falsifiers"), list) else []
        if falsifiers:
            blocks.append("\\paragraph{Falsifiers.}\n" + latex_list(falsifiers))
    return section("timeline", "Content-Specific Full Timeline", "\n\n".join(blocks), ["timeline_cycles"], "timeline-cycle-latex-translator")


def build_ranked_analyses_section(payload: dict[str, Any]) -> dict[str, Any]:
    queue = payload.get("timeline_ranked_next_experiment_queue", []) if isinstance(payload.get("timeline_ranked_next_experiment_queue"), list) else []
    blocks = [
        "\\section{Current Ranked Next-Analysis Queue}",
        "\\label{sec:report-ranked-analyses}",
        tex_escape_mathish(
            "Ordered by target payoff, discriminating power, execution readiness, target integration, and anti-drift pressure. "
            "The score is a control signal for the next run, not a theorem-progress claim."
        ),
    ]
    for item in queue:
        if not isinstance(item, dict):
            continue
        heading = f"#{item.get('rank', '?')} {item.get('cycle_id', '')}: {item.get('branch_title', 'branch?')}"
        blocks.append(f"\\subsection*{{{tex_escape_mathish(heading)}}}")
        blocks.append("\\paragraph{Analysis.} " + tex_escape_mathish(item.get("next_experiment")))
        for label, key in [
            ("Why this is a good target", "why_target"),
            ("Risk", "risk"),
            ("Branch control", "branch_continuation_reason"),
            ("Premature-stop guard", "premature_stop_guard"),
            ("Source object", "source_object"),
            ("Target object", "target_object"),
            ("Transfer condition", "transfer_condition"),
        ]:
            if clean_text(item.get(key)):
                blocks.append(f"\\paragraph{{{label}.}} " + tex_escape_mathish(item.get(key)))
        for label, key in [
            ("Validation steps", "validation_steps"),
            ("Payoff criteria", "payoff_criteria"),
            ("Stop criteria", "stop_criteria"),
            ("Do not stop if", "do_not_stop_if"),
            ("Required skills", "required_skills"),
        ]:
            values = item.get(key, [])
            if isinstance(values, list) and values:
                blocks.append(f"\\paragraph{{{label}.}}\n" + latex_list(values))
    return section("ranked_analyses", "Current Ranked Next-Analysis Queue", "\n\n".join(blocks), ["timeline_ranked_next_experiment_queue"], "timeline-summary-latex-translator")


def build_qualitative_graph_section(payload: dict[str, Any]) -> dict[str, Any]:
    target_id = infer_target_id(payload)
    graph = payload.get("qualitative_mechanistic_graph", {}) if isinstance(payload.get("qualitative_mechanistic_graph"), dict) else {}
    nodes = graph.get("nodes", []) if isinstance(graph.get("nodes"), list) else []
    edges = graph.get("edges", []) if isinstance(graph.get("edges"), list) else []
    if target_id == "p-vs-np-target":
        mechanism_steps = [
            "A candidate bridge starts with a named source carrier, target class, circuit model, and length map.",
            "The transfer envelope computes how SAT circuits of size n^c induce source-carrier circuits, usually through an exponent term q+beta c.",
            "Positive beta or hidden advice can collapse all-exponent consequences into a bounded-window theorem.",
            "Barrier checks attach to the actual theorem shape: relativization, naturalness, algebrization, nonuniformity, and advice leakage are not generic slogans.",
            "A branch is promoted only when it yields an exact transfer theorem, a scoped no-go, or a finite certificate/soundness obligation that changes route priority.",
        ]
    else:
        mechanism_steps = [
            "Regulated reflection positivity gives finite Gram matrices at fixed cutoff and volume.",
            "Collar collapse can introduce boundary factors, quotient phases, determinant obstructions, and contact terms.",
            "Exact finite tests decide whether the finite family is eligible for analytic promotion.",
            "Analytic transfer turns finite algebra into Yang-Mills obligations: boundary OPE, contact control, nonzero denominators, modulus positivity, and same-theory realization.",
            "Euclidean decay can speak about a mass gap only after OS reconstruction and observable-density control.",
        ]
    blocks = [
        "\\section{Qualitative Mechanistic Graph}",
        "\\label{sec:report-qualitative-graph}",
        tex_escape_mathish(
            "The qualitative graph is a mechanism map, not a JSON registry. It states how variables, regimes, exact finite tests, and transfer obligations steer branch control."
        ),
        "\\subsection*{Mechanism in plain terms}",
        latex_ordered(mechanism_steps),
        "\\subsection*{Relations that matter now}",
    ]
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        title = f"{edge.get('source', '')} {edge.get('edge_type', 'relates to')} {edge.get('target', '')}"
        blocks.append(f"\\subsubsection*{{{tex_escape_mathish(title)}}}")
        blocks.append("\\paragraph{Behavior.} " + tex_escape_mathish(edge.get("qualitative_behavior") or edge.get("direction")))
        if edge.get("assumptions"):
            blocks.append("\\paragraph{Trust it when.}\n" + latex_list(edge.get("assumptions", []), limit=4))
        if edge.get("failure_modes"):
            blocks.append("\\paragraph{What would break it.}\n" + latex_list(edge.get("failure_modes", []), limit=4))
        if edge.get("originating_cycle_ids"):
            blocks.append("\\paragraph{Audit trail.} " + tex_escape_mathish(", ".join(edge.get("originating_cycle_ids", [])[-8:])))
    blocks.append("\\subsection*{Quantities and regimes}")
    for node in nodes:
        if isinstance(node, dict):
            blocks.append("\\paragraph{" + tex_escape_mathish(node.get("label") or node.get("id")) + ".} " + tex_escape_mathish(node.get("description")))
    return section("qualitative_graph", "Qualitative Mechanistic Graph", "\n\n".join(blocks), ["qualitative_mechanistic_graph"], "timeline-story-latex-translator")


def build_gedanken_section(payload: dict[str, Any]) -> dict[str, Any]:
    gedanken = payload.get("gedanken_experiments", {}) if isinstance(payload.get("gedanken_experiments"), dict) else {}
    packets = gedanken.get("packets", []) if isinstance(gedanken.get("packets"), list) else []
    blocks = [
        "\\section{Gedanken Experiments}",
        "\\label{sec:report-gedanken}",
        tex_escape_mathish(
            "Concrete imagined situations are used only when they isolate a mechanism, expose a hidden assumption, or create a follow-up task. They are conceptual probes, not proof progress."
        ),
    ]
    for packet in packets:
        if not isinstance(packet, dict):
            continue
        situation = packet.get("situation", {}) if isinstance(packet.get("situation"), dict) else {}
        title = situation.get("title") or packet.get("situation_title") or packet.get("packet_id")
        blocks.append(f"\\subsection*{{{tex_escape_mathish(title)}}}")
        for label, value in [
            ("Purpose", situation.get("purpose")),
            ("Minimal world", situation.get("minimal_world")),
            ("Carrier", situation.get("mathematical_carrier")),
            ("Why informative", situation.get("why_this_situation_is_informative")),
            ("Need decision", packet.get("need_decision")),
            ("Transfer verdict", packet.get("transfer_verdict")),
        ]:
            if clean_text(value):
                blocks.append(f"\\paragraph{{{label}.}} " + tex_escape_mathish(value))
        for label, key in [
            ("Trigger criteria", "trigger_criteria"),
            ("Interventions", "interventions"),
            ("Expected observations", "expected_observations"),
            ("Variants", "variants"),
            ("Follow-up tasks", "followup_cycle_tasks"),
            ("Failure modes", "failure_modes"),
        ]:
            values = packet.get(key, [])
            if isinstance(values, list) and values:
                blocks.append(f"\\paragraph{{{label}.}}\n" + latex_list(values))
    return section("gedanken", "Gedanken Experiments", "\n\n".join(blocks), ["gedanken_experiments"], "timeline-story-latex-translator")


def build_parsimonious_section(payload: dict[str, Any]) -> dict[str, Any]:
    target_id = infer_target_id(payload)
    layer = payload.get("parsimonious_probe_layer", {}) if isinstance(payload.get("parsimonious_probe_layer"), dict) else {}
    if target_id == "p-vs-np-target":
        layer_text = json.dumps(layer, ensure_ascii=False).lower()
        if any(term in layer_text for term in ["yang-mills", "wilson", "collar", "hairpin", "reflection positivity"]):
            layer = {}
    finite = layer.get("finite_algebra_interfaces", {}) if isinstance(layer.get("finite_algebra_interfaces"), dict) else {}
    symbolic = layer.get("symbolic_matrix_probe", {}) if isinstance(layer.get("symbolic_matrix_probe"), dict) else {}
    obligations = layer.get("analytic_estimate_obligations", {}) if isinstance(layer.get("analytic_estimate_obligations"), dict) else {}
    packets = finite.get("packets", []) if isinstance(finite.get("packets"), list) else []
    identities = symbolic.get("identities", []) if isinstance(symbolic.get("identities"), list) else []
    queue_items = obligations.get("next_experiment_queue_items", []) if isinstance(obligations.get("next_experiment_queue_items"), list) else []
    blocks = [
        "\\section{Parsimonious Probe Control}",
        "\\label{sec:report-pmp-probes}",
        tex_escape_mathish(
            "This section keeps symbolic-first computation separate from analytic obligations and rare bounded numeric probes."
        ),
    ]
    if target_id == "p-vs-np-target" and not layer:
        blocks.append(
            tex_escape_mathish(
                "No target-compatible parsimonious probe packet is active for this P vs NP report. "
                "A future packet should use symbolic complexity auditing: exact exponent envelopes, length maps, advice terms, certificate-search exponents, and barrier predicates."
            )
        )
    for packet in packets:
        if isinstance(packet, dict):
            carrier = packet.get("carrier", {}) if isinstance(packet.get("carrier"), dict) else {}
            blocks.append(f"\\subsection*{{Finite algebra interface: {tex_escape_mathish(carrier.get('name') or packet.get('packet_id'))}}}")
            blocks.append("\\paragraph{Boundary.} " + tex_escape_mathish(carrier.get("validity_boundary")))
            blocks.append("\\paragraph{Side conditions.}\n" + latex_list(packet.get("side_conditions", [])))
            blocks.append("\\paragraph{Falsifier shapes.}\n" + latex_list(packet.get("falsifier_templates", [])))
    if identities:
        blocks.append("\\subsection*{Exact symbolic interfaces}")
        for identity in identities:
            if isinstance(identity, dict):
                blocks.append(f"\\paragraph{{{tex_escape_mathish(identity.get('name') or identity.get('id'))}.}}")
                if clean_text(identity.get("latex")):
                    blocks.append(latex_formula_block(identity.get("latex"), valid_when=identity.get("valid_when")))
    if queue_items:
        blocks.append("\\subsection*{Formula-derived analytic obligations}")
        for item in queue_items:
            if isinstance(item, dict):
                blocks.append(f"\\paragraph{{{tex_escape_mathish(item.get('next_experiment') or item.get('source_obligation_id'))}.}}")
                blocks.append(latex_list(item.get("payoff_criteria", [])))
                blocks.append("\\emph{Required skills:} " + tex_escape_mathish(", ".join(item.get("required_skills", []))))
    return section("parsimonious", "Parsimonious Probe Control", "\n\n".join(blocks), ["parsimonious_probe_layer"], "timeline-summary-latex-translator")


def build_contributions_section(payload: dict[str, Any]) -> dict[str, Any]:
    target_id = infer_target_id(payload)
    monitor = payload.get("scientific_contribution_monitor", {}) if isinstance(payload.get("scientific_contribution_monitor"), dict) else {}
    if target_id and clean_text(monitor.get("target_id")) != target_id:
        from build_scientific_contribution_monitor import build_report as build_contribution_monitor

        monitor = build_contribution_monitor(target_id)
    candidates = monitor.get("candidates", []) if isinstance(monitor.get("candidates"), list) else []
    policy = monitor.get("loop_policy", {}) if isinstance(monitor.get("loop_policy"), dict) else {}
    blocks = [
        "\\section{Scientific Contribution Monitor}",
        "\\label{sec:report-contributions}",
        tex_escape_mathish(
            "This section keeps the marathon aimed at independently valuable subgoals and decides when a branch is good enough to hand off instead of continuing indefinitely."
        ),
        "\\subsection*{Standing objective}",
        tex_escape_mathish(policy.get("standing_objective")),
        "\\subsection*{Good enough definition}",
        tex_escape_mathish(policy.get("good_enough_definition")),
        "\\subsection*{Good enough paper relevance}",
        tex_escape_mathish(policy.get("good_enough_paper_relevance_definition")),
        "\\subsection*{Paper relevance marker criteria}",
        latex_list(
            [
                f"{key}: {value}"
                for key, value in (policy.get("paper_relevance_marker_criteria", {}) if isinstance(policy.get("paper_relevance_marker_criteria"), dict) else {}).items()
            ]
        ),
        "\\subsection*{Stepping-stone maturity levels}",
        latex_list(
            [
                f"{key}: {value}"
                for key, value in (policy.get("stepping_stone_maturity_levels", {}) if isinstance(policy.get("stepping_stone_maturity_levels"), dict) else {}).items()
            ]
        ),
        "\\subsection*{Anti-infinite progression rule}",
        tex_escape_mathish(policy.get("anti_infinite_progression_rule")),
    ]
    if clean_text(monitor.get("next_contribution_objective")):
        blocks.append("\\subsection*{Next contribution objective}\n" + tex_escape_mathish(monitor.get("next_contribution_objective")))
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        title = f"{candidate.get('cycle_id', '')}: {candidate.get('branch_title', candidate.get('candidate_id', 'candidate'))}"
        blocks.append(f"\\subsection*{{{tex_escape_mathish(title)}}}")
        for label, key in [
            ("Contribution type", "contribution_type"),
            ("Stepping-stone maturity", "stepping_stone_maturity"),
            ("Smallest honest claim", "smallest_honest_claim"),
            ("Why it could stand alone", "why_it_could_stand_alone"),
            ("Why this budget now", "why_this_budget_now"),
            ("Branch control", "branch_control_reason"),
            ("Overclaim boundary", "overclaim_boundary"),
        ]:
            blocks.append(f"\\paragraph{{{label}.}} " + tex_escape_mathish(candidate.get(key)))
        relevance = candidate.get("good_enough_paper_relevance", {}) if isinstance(candidate.get("good_enough_paper_relevance"), dict) else {}
        if relevance:
            blocks.append("\\paragraph{Good-enough paper relevance.} " + tex_escape_mathish(relevance.get("paper_relevance_decision")))
            blocks.append(
                "\\paragraph{Paper relevance status.} "
                + tex_escape_mathish(f"{relevance.get('status')} with average marker score {relevance.get('average_marker_score')}")
            )
        for label, key in [
            ("Good enough when", "good_enough_when"),
            ("Continue only if", "continue_only_if"),
            ("Stop when", "stop_when"),
            ("Validation burden", "validation_burden"),
            ("Evidence basis", "evidence_basis"),
            ("Missing to publishable", "missing_to_publishable"),
            ("Missing to good-enough paper", "missing_to_good_enough_paper"),
        ]:
            values = candidate.get(key, [])
            if isinstance(values, list) and values:
                blocks.append(f"\\paragraph{{{label}.}}\n" + latex_list(values))
        markers = candidate.get("paper_relevance_markers", []) if isinstance(candidate.get("paper_relevance_markers"), list) else []
        if markers:
            blocks.append(
                "\\paragraph{Paper relevance markers.}\n"
                + latex_list(
                    [
                        f"{marker.get('dimension')}: score={marker.get('score')}, status={marker.get('status')} - {marker.get('criterion')}"
                        for marker in markers
                        if isinstance(marker, dict)
                    ]
                )
            )
        gates = candidate.get("handoff_hard_gates", {}) if isinstance(candidate.get("handoff_hard_gates"), dict) else {}
        if gates:
            blocks.append(
                "\\paragraph{Hard gates.}\n"
                + latex_list(
                    [
                        f"{gate}: ready={packet.get('ready')}, finite_task={packet.get('finite_task')}"
                        for gate, packet in gates.items()
                        if isinstance(packet, dict)
                    ]
                )
            )
        disqualifiers = candidate.get("disqualifier_tests", []) if isinstance(candidate.get("disqualifier_tests"), list) else []
        if disqualifiers:
            blocks.append(
                "\\paragraph{Disqualifiers.}\n"
                + latex_list(
                    [
                        f"{row.get('name')}: {row.get('verdict')} - {row.get('evidence')}"
                        for row in disqualifiers
                        if isinstance(row, dict)
                    ]
                )
            )
        prior = candidate.get("prior_art_boundary", {}) if isinstance(candidate.get("prior_art_boundary"), dict) else {}
        if prior:
            blocks.append("\\paragraph{Prior-art boundary.} " + tex_escape_mathish(prior.get("novelty_status")))
            if isinstance(prior.get("citation_tasks"), list):
                blocks.append(latex_list(prior.get("citation_tasks")))
    return section("contributions", "Scientific Contribution Monitor", "\n\n".join(blocks), ["scientific_contribution_monitor"], "timeline-summary-latex-translator")


def build_problem_literature_section(payload: dict[str, Any]) -> dict[str, Any]:
    literature = payload.get("target_literature_evolution", {}) if isinstance(payload.get("target_literature_evolution"), dict) else {}
    problem = literature.get("problem_statement", {}) if isinstance(literature.get("problem_statement"), dict) else {}
    stages = literature.get("literature_stages", []) if isinstance(literature.get("literature_stages"), list) else []
    refs = literature.get("references", []) if isinstance(literature.get("references"), list) else []
    formal_shape = problem.get("formal_shape")
    blocks = [
        "\\section{Target Problem And Literature Evolution}",
        "\\label{sec:report-problem-literature}",
        f"\\subsection*{{{tex_escape_mathish(literature.get('problem_name') or 'Active target')}}}",
        tex_escape_mathish(problem.get("accessible")),
    ]
    if clean_text(formal_shape):
        blocks.append("\\[\n" + normalize_tex_formula(formal_shape) + "\n\\]")
    blocks.append("\\subsection*{Why this problem matters}\n" + latex_list(literature.get("why_it_matters", [])))
    blocks.append("\\subsection*{What would count as a solution}\n" + latex_list(literature.get("solution_criteria", [])))
    blocks.append("\\subsection*{How the literature evolved}")
    for stage in stages:
        if isinstance(stage, dict):
            blocks.append(f"\\subsubsection*{{{tex_escape_mathish(str(stage.get('period', '')) + ' -- ' + str(stage.get('title', '')))}}}")
            blocks.append("\\paragraph{Conceptual shift.} " + tex_escape_mathish(stage.get("core_shift")))
            blocks.append("\\paragraph{What became possible.} " + tex_escape_mathish(stage.get("what_became_possible")))
            blocks.append("\\paragraph{What remained open.} " + tex_escape_mathish(stage.get("what_remained_open")))
    blocks.append("\\subsection*{References preserved by the report}")
    for ref in refs:
        if isinstance(ref, dict):
            blocks.append(
                "\\paragraph{"
                + tex_escape_mathish(f"{ref.get('authors', '')} ({ref.get('year', '')})")
                + ".} "
                + tex_escape_mathish(f"{ref.get('title', '')}. Supports: {ref.get('supports', '')}. Limitation: {ref.get('limitation', '')}")
            )
    return section("problem_literature", "Target Problem And Literature Evolution", "\n\n".join(blocks), ["target_literature_evolution"], "timeline-problem-literature-latex-translator")


def build_macro_strategy_section(payload: dict[str, Any]) -> dict[str, Any]:
    report = payload.get("macro_strategy_report", {}) if isinstance(payload.get("macro_strategy_report"), dict) else {}
    strategies = report.get("macro_strategies", []) if isinstance(report.get("macro_strategies"), list) else []
    blocks = [
        "\\section{Macro Strategies}",
        "\\label{sec:report-macro-strategies}",
        tex_escape_mathish(report.get("headline")),
    ]
    for strategy in strategies:
        if isinstance(strategy, dict):
            blocks.append(f"\\subsection*{{{tex_escape_mathish(strategy.get('title') or strategy.get('strategy_id'))}}}")
            for label, key in [
                ("Physics picture", "physics_picture"),
                ("Mathematical object", "mathematical_object"),
                ("Why this route matters", "why_this_route_matters"),
                ("Current pressure", "current_pressure"),
                ("Next decisive move", "next_decisive_move"),
                ("Validation boundary", "validation_boundary"),
            ]:
                if clean_text(strategy.get(key)):
                    blocks.append(f"\\paragraph{{{label}.}} " + tex_escape_mathish(strategy.get(key)))
            if strategy.get("active_skills"):
                blocks.append("\\paragraph{Active skills.}\n" + latex_list(strategy.get("active_skills", [])))
            if strategy.get("evidence_from_story"):
                blocks.append("\\paragraph{Evidence from story.}\n" + latex_list(strategy.get("evidence_from_story", []), limit=8))
    return section("macro_strategies", "Macro Strategies", "\n\n".join(blocks), ["macro_strategy_report"], "timeline-story-latex-translator")


def build_complexity_strategy_section(payload: dict[str, Any]) -> dict[str, Any]:
    report = payload.get("macro_strategy_report", {}) if isinstance(payload.get("macro_strategy_report"), dict) else {}
    strategies = report.get("macro_strategies", []) if isinstance(report.get("macro_strategies"), list) else []
    judge = payload.get("strategy_progression_judge", {}) if isinstance(payload.get("strategy_progression_judge"), dict) else {}
    progress = judge.get("progression_judgement", {}) if isinstance(judge.get("progression_judgement"), dict) else {}
    blocks = [
        "\\section{Complexity Strategy}",
        "\\label{sec:report-complexity-strategy}",
        tex_escape_mathish(
            "This top-level section states the active proof strategy before the report moves into the full timeline. "
            "For P vs NP, strategy is controlled by source carrier, target class, reduction or transfer map, exact exponent debt, uniformity/advice discipline, and known barrier status."
        ),
    ]
    if clean_text(report.get("headline")):
        blocks.append("\\subsection*{Current macro reading}\n" + tex_escape_mathish(report.get("headline")))
    for label, key in [
        ("Contribution pivot invariant", "contribution_pivot_invariant"),
        ("Next decisive test", "next_decisive_test"),
        ("When to stop", "when_to_stop"),
    ]:
        if clean_text(progress.get(key)):
            blocks.append(f"\\paragraph{{{label}.}} " + tex_escape_mathish(progress.get(key)))
    for strategy in strategies:
        if not isinstance(strategy, dict):
            continue
        blocks.append(f"\\subsection*{{{tex_escape_mathish(strategy.get('title') or strategy.get('strategy_id'))}}}")
        for label, key in [
            ("Route family", "route_family"),
            ("Macro thesis", "macro_thesis"),
            ("Conceptual proof picture", "physics_picture"),
            ("Why this route matters now", "why_now"),
        ]:
            if clean_text(strategy.get(key)):
                blocks.append(f"\\paragraph{{{label}.}} " + tex_escape_mathish(strategy.get(key)))
        for label, key in [
            ("What to compute next", "what_to_compute_next"),
            ("Success condition", "success_condition"),
            ("Failure or pivot condition", "failure_or_pivot_condition"),
            ("Active skills", "active_skills"),
            ("Evidence from story", "evidence_from_story"),
        ]:
            values = strategy.get(key, [])
            if isinstance(values, list) and values:
                blocks.append(f"\\paragraph{{{label}.}}\n" + latex_list(values, limit=8))
    return section("physics_math_strategy", "Complexity Strategy", "\n\n".join(blocks), ["macro_strategy_report", "strategy_progression_judge"], "timeline-story-latex-translator")


def build_physics_math_strategy_section(payload: dict[str, Any]) -> dict[str, Any]:
    if infer_target_id(payload) == "p-vs-np-target":
        return build_complexity_strategy_section(payload)
    report = payload.get("physics_math_interpretation", {}) if isinstance(payload.get("physics_math_interpretation"), dict) else {}
    synthesis = report.get("cross_route_synthesis", {}) if isinstance(report.get("cross_route_synthesis"), dict) else {}
    routes = report.get("interpretations", []) if isinstance(report.get("interpretations"), list) else []
    blocks = [
        "\\section{Physics And Maths Strategy}",
        "\\label{sec:report-physics-maths-strategy}",
        tex_escape_mathish(
            "This top-level section states the active physics picture and the mathematical machinery before the report moves into the full timeline."
        ),
        "\\subsection*{Cross-route synthesis}",
        "\\paragraph{Constructive spine.} " + tex_escape_mathish(synthesis.get("constructive_spine")),
        "\\paragraph{Missing joint step.} " + tex_escape_mathish(synthesis.get("missing_joint_step")),
        "\\subsection*{Next mathematical-physics focus}",
        latex_list(synthesis.get("next_mathematical_physics_focus", []) if isinstance(synthesis.get("next_mathematical_physics_focus"), list) else []),
    ]
    for route in routes:
        if not isinstance(route, dict):
            continue
        blocks.append(f"\\subsection*{{{tex_escape_mathish(route.get('route_family') or route.get('candidate_id'))}}}")
        for label, key in [
            ("Route thesis", "route_thesis"),
            ("Physical meaning", "physical_meaning"),
            ("Load-bearing bridge", "load_bearing_bridge"),
            ("Conceptual bottleneck", "conceptual_bottleneck"),
            ("Why this is not a proof", "why_not_a_proof"),
        ]:
            if clean_text(route.get(key)):
                blocks.append(f"\\paragraph{{{label}.}} " + tex_escape_mathish(route.get(key)))
        blocks.append("\\paragraph{Mathematical objects.}\n" + latex_list(route.get("mathematical_objects", []) if isinstance(route.get("mathematical_objects"), list) else []))
        blocks.append("\\paragraph{Mechanism chain.}\n" + latex_ordered(route.get("mechanism_chain", []) if isinstance(route.get("mechanism_chain"), list) else []))
        blocks.append("\\paragraph{Next lemma questions.}\n" + latex_list(route.get("next_lemma_questions", []) if isinstance(route.get("next_lemma_questions"), list) else []))
        blocks.append("\\paragraph{False-positive controls.}\n" + latex_list(route.get("false_positive_controls", []) if isinstance(route.get("false_positive_controls"), list) else []))
    return section("physics_math_strategy", "Physics And Maths Strategy", "\n\n".join(blocks), ["physics_math_interpretation"], "timeline-story-latex-translator")


def build_strategy_judge_section(payload: dict[str, Any]) -> dict[str, Any]:
    judge = payload.get("strategy_progression_judge", {}) if isinstance(payload.get("strategy_progression_judge"), dict) else {}
    current = judge.get("current_strategy", {}) if isinstance(judge.get("current_strategy"), dict) else {}
    progress = judge.get("progression_judgement", {}) if isinstance(judge.get("progression_judgement"), dict) else {}
    readiness = judge.get("paper_contribution_readiness", {}) if isinstance(judge.get("paper_contribution_readiness"), dict) else {}
    alignment = judge.get("main_problem_alignment", {}) if isinstance(judge.get("main_problem_alignment"), dict) else {}
    payoff_rows = judge.get("strategy_payoff_table", []) if isinstance(judge.get("strategy_payoff_table"), list) else []
    blocks = [
        "\\section{Strategy Progression Judge}",
        "\\label{sec:report-strategy-judge}",
        tex_escape_mathish(
            "The 10-cycle payoff judge reads the target problem, literature evolution, latest analysis outputs, macro strategy, and contribution monitor."
        ),
        "\\subsection*{Current strategy}",
    ]
    for label, key in [
        ("Title", "title"),
        ("Route family", "route_family"),
        ("Active object", "active_object"),
        ("Macro thesis", "macro_thesis"),
    ]:
        blocks.append(f"\\paragraph{{{label}.}} " + tex_escape_mathish(current.get(key)))
    blocks.append("\\subsection*{Judgement summary}")
    for label, key in [
        ("Decision", "decision"),
        ("Payoff potential", "payoff_potential"),
        ("Contribution pivot invariant", "contribution_pivot_invariant"),
        ("Next decisive test", "next_decisive_test"),
        ("When to stop", "when_to_stop"),
    ]:
        blocks.append(f"\\paragraph{{{label}.}} " + tex_escape_mathish(progress.get(key)))
    blocks.append("\\subsection*{Paper-level contribution readiness}")
    for label, key in [
        ("Readiness", "readiness_class"),
        ("Closest contribution", "closest_contribution"),
        ("Missing for paper", "missing_for_paper"),
        ("Recommended paper move", "recommended_paper_move"),
    ]:
        blocks.append(f"\\paragraph{{{label}.}} " + tex_escape_mathish(readiness.get(key)))
    blocks.append("\\subsection*{Main problem alignment}")
    for label, key in [
        ("Alignment class", "alignment_class"),
        ("Alignment gain", "alignment_gain"),
        ("Alignment loss", "alignment_loss"),
        ("Proxy or transfer risk", "proxy_or_transfer_risk"),
        ("Repair action", "repair_action"),
    ]:
        blocks.append(f"\\paragraph{{{label}.}} " + tex_escape_mathish(alignment.get(key)))
    if payoff_rows:
        blocks.append("\\subsection*{Strategy payoff assessments}")
        for row in payoff_rows:
            if isinstance(row, dict):
                blocks.append(f"\\subsubsection*{{{tex_escape_mathish(row.get('strategy') or row.get('strategy_id'))}}}")
                blocks.append("\\paragraph{Payoff.} " + tex_escape_mathish(row.get("payoff")))
                blocks.append("\\paragraph{Risk.} " + tex_escape_mathish(row.get("risk")))
                blocks.append("\\paragraph{Decision.} " + tex_escape_mathish(row.get("decision")))
    return section("strategy_judge", "Strategy Progression Judge", "\n\n".join(blocks), ["strategy_progression_judge"], "timeline-summary-latex-translator")


def build_physics_story_section(payload: dict[str, Any]) -> dict[str, Any]:
    target_id = infer_target_id(payload)
    story_title = "Accumulated Proof Strategy Story" if target_id == "p-vs-np-target" else "Accumulated Physics Story"
    story = payload.get("timeline_storyline", {}) if isinstance(payload.get("timeline_storyline"), dict) else {}
    current = payload.get("current_story", {}) if isinstance(payload.get("current_story"), dict) else {}
    beats = story.get("beats", []) if isinstance(story.get("beats"), list) else []
    blocks = [
        f"\\section{{{story_title}}}",
        "\\label{sec:report-physics-story}",
        tex_escape_mathish(story.get("headline") or current.get("headline")),
        "\\paragraph{Latest learning.} " + tex_escape_mathish(current.get("latest_learning")),
        "\\paragraph{Current obstruction.} " + tex_escape_mathish(current.get("current_obstruction")),
        "\\paragraph{Current next analysis.} " + tex_escape_mathish(current.get("next_experiment")),
    ]
    for beat in beats:
        if not isinstance(beat, dict):
            continue
        heading = f"{beat.get('cycle_id', '')}: {beat.get('branch_title', '')}"
        blocks.append(f"\\subsection*{{{tex_escape_mathish(heading)}}}")
        blocks.append("\\paragraph{Learning.} " + tex_escape_mathish(beat.get("learning") or beat.get("mathematical_learning")))
        if clean_text(beat.get("blocking_gap")):
            blocks.append("\\paragraph{Pressure.} " + tex_escape_mathish(beat.get("blocking_gap")))
        if clean_text(beat.get("next_experiment")):
            blocks.append("\\paragraph{Next.} " + tex_escape_mathish(beat.get("next_experiment")))
        if clean_text(beat.get("when_to_stop")):
            blocks.append("\\paragraph{When to stop.} " + tex_escape_mathish(beat.get("when_to_stop")))
        if clean_text(beat.get("premature_stop_guard")):
            blocks.append("\\paragraph{Do not stop prematurely if.} " + tex_escape_mathish(beat.get("premature_stop_guard")))
        if clean_text(beat.get("global_problem_contribution")):
            blocks.append("\\paragraph{How it adds to the global problem.} " + tex_escape_mathish(beat.get("global_problem_contribution")))
    return section("physics_story", story_title, "\n\n".join(blocks), ["timeline_storyline", "current_story"], "timeline-story-latex-translator")


def build_summary_section(payload: dict[str, Any]) -> dict[str, Any]:
    report = payload.get("report", {}) if isinstance(payload.get("report"), dict) else {}
    control = payload.get("summary_analysis_control", {}) if isinstance(payload.get("summary_analysis_control"), dict) else {}
    blocks = [
        "\\section{Summary}",
        "\\label{sec:report-summary}",
        "\\subsection*{Current mathematical story}",
        tex_escape_mathish(report.get("current_mathematical_story")),
        "\\subsection*{What actually changed}",
        latex_list(report.get("what_actually_changed", []) if isinstance(report.get("what_actually_changed"), list) else []),
        "\\subsection*{How this adds to the global problem}",
        tex_escape_mathish(control.get("global_problem_contribution")),
        "\\subsection*{Payoff criteria}",
        latex_list(control.get("payoff_criteria", []) if isinstance(control.get("payoff_criteria"), list) else []),
        "\\subsection*{When to stop}",
        latex_list(control.get("stop_criteria", []) if isinstance(control.get("stop_criteria"), list) else []),
        "\\subsection*{Do not stop prematurely if}",
        latex_list(control.get("do_not_stop_if", []) if isinstance(control.get("do_not_stop_if"), list) else []),
    ]
    return section("summary", "Summary", "\n\n".join(blocks), ["report", "summary_analysis_control"], "timeline-summary-latex-translator")


def build_report() -> dict[str, Any]:
    global ACTIVE_TARGET_ID
    payload = load_embedded_payload()
    if not payload and LATEST_JSON.exists():
        payload = json.loads(LATEST_JSON.read_text(encoding="utf-8"))
    ACTIVE_TARGET_ID = infer_target_id(payload)
    profile = target_profile(ACTIVE_TARGET_ID)
    tab_sections = report_tab_sections(ACTIVE_TARGET_ID)
    builders = [
        build_summary_section,
        build_physics_math_strategy_section,
        build_timeline_section,
        build_ranked_analyses_section,
        build_qualitative_graph_section,
        build_gedanken_section,
        build_parsimonious_section,
        build_contributions_section,
        build_problem_literature_section,
        build_macro_strategy_section,
        build_strategy_judge_section,
        build_physics_story_section,
    ]
    sections = [builder(payload) for builder in builders]
    validation_preamble = (
        "\\section*{Report Translation Validation}\n"
        "These sections preserve the visible timeline report tabs as LaTeX sections. "
        "validation handoff: run \\texttt{python agentic/scripts/validate\\_timeline\\_latex\\_sections.py} "
        "before treating the translation as paper-ready."
    )
    tex = clean_tex_lines("\n\n".join([validation_preamble, *[item["latex"] for item in sections]]))
    section_ids = [section["section_id"] for section in sections]
    tab_contract = []
    for tab in tab_sections:
        tab_contract.append(
            {
                **tab,
                "present": tab["section_id"] in section_ids,
            }
        )
    return {
        "version": 2,
        "generated_utc": utc_now(),
        "target_id": ACTIVE_TARGET_ID,
        "target_display_name": profile.get("display_name", ACTIVE_TARGET_ID),
        "source_artifact": rel(FULL_TIMELINE_HTML if FULL_TIMELINE_HTML.exists() else LATEST_JSON),
        "packet_id": stable_id("timeline-latex", [section["section_id"] for section in sections], payload.get("generated_utc", "")),
        "status": "timeline_latex_sections_ready",
        "report_document_contract": {
            "source_report": "agentic/reports/discovery_marathon/full_timeline.html",
            "mapping_rule": "each visible timeline report tab is translated into one LaTeX section in the same tab order",
            "tab_count": len(tab_sections),
            "tab_sections": tab_contract,
        },
        "translator_skills": TRANSLATOR_SKILLS,
        "sections": sections,
        "artifacts": {"json": rel(OUT_JSON), "markdown": rel(OUT_MD), "tex": rel(OUT_TEX), "report_tex": rel(OUT_REPORT_TEX)},
        "epistemic_status": "latex_translation_validation_needed",
        "validation_handoff": "python agentic/scripts/validate_timeline_latex_sections.py",
        "latex": tex,
    }


def render_report_document(report: dict[str, Any]) -> str:
    contract = report.get("report_document_contract", {})
    tabs = contract.get("tab_sections", []) if isinstance(contract.get("tab_sections"), list) else []
    tab_lines = [
        f"\\item {tex_escape_mathish(tab.get('tab_label'))} $\\rightarrow$ {tex_escape_mathish(tab.get('section_title'))}"
        for tab in tabs
        if isinstance(tab, dict)
    ]
    tab_list = "\\begin{itemize}\n" + "\n".join(tab_lines) + "\n\\end{itemize}" if tab_lines else ""
    return rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{fontspec}}
\usepackage{{amsmath,amssymb,mathtools}}
\usepackage{{enumitem}}
\usepackage[colorlinks=true,linkcolor=blue,urlcolor=blue]{{hyperref}}
\setlist[itemize]{{leftmargin=*,itemsep=0.25em,topsep=0.25em}}

\title{{Timeline Report LaTeX Translation}}
\author{{Abducer Timeline Report LaTeX Workflow}}
\date{{{tex_escape_mathish(report.get("generated_utc"))}}}

\begin{{document}}
\maketitle
\tableofcontents
\clearpage

\section*{{Report Translation Contract}}
This document is the LaTeX version of the timeline HTML report. Each visible report tab is translated into a section, preserving the same tab order and internal report-card structure where applicable. The companion paper includes these same sections as an appendix.

{tab_list}

{report.get("latex", "")}

\end{{document}}
"""


def sanitize_rendered_tex(tex: str) -> str:
    tex = tex.replace("∘", r"\circ ")
    tex = tex.replace(r"\left{", r"\left\{").replace(r"\right}", r"\right\}")

    def escape_text_body(match: re.Match[str]) -> str:
        body = match.group(1)
        body = re.sub(r"(?<!\\)_", r"\\_", body)
        body = re.sub(r"(?<!\\)#", r"\\#", body)
        body = re.sub(r"(?<!\\)%", r"\\%", body)
        body = re.sub(r"(?<!\\)&", r"\\&", body)
        return r"\text{" + body + "}"

    return re.sub(r"\\text\{([^{}]*)\}", escape_text_body, tex)


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Timeline LaTeX Sections",
        "",
        f"- Status: `{report['status']}`",
        f"- Source: `{report['source_artifact']}`",
        f"- TeX: `{report['artifacts']['tex']}`",
        "",
        "## Translator Skills",
        "",
        *[f"- `{skill}`" for skill in report["translator_skills"]],
        "",
        "## Report-Shaped Sections",
        "",
    ]
    for item in report["sections"]:
        lines.append(f"- `{item['section_id']}` {item['title']} via `{item['translator_skill']}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    report = build_report()
    report["latex"] = sanitize_rendered_tex(report["latex"])
    report_document = sanitize_rendered_tex(render_report_document(report))
    write_json(OUT_JSON, {key: value for key, value in report.items() if key != "latex"})
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    OUT_TEX.write_text(report["latex"], encoding="utf-8")
    OUT_REPORT_TEX.write_text(report_document, encoding="utf-8")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    print(f"Wrote {OUT_TEX.relative_to(ROOT)}")
    print(f"Wrote {OUT_REPORT_TEX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
