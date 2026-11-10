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
"""Generate an accumulated HTML report for discovery marathon runs."""

from __future__ import annotations

import html
import argparse
import json
import re
from pathlib import Path
from statistics import mean
from typing import Any

from agentic_common import ROOT, clean_text, load_json_object, load_optional_json, rel
from discovery_marathon_common import (
    LATEST_HTML,
    LATEST_JSON,
    LATEST_TIMELINE_HTML,
    generic_report_path_writable,
    load_cycles,
    load_run_state,
    target_latest_html,
    target_latest_json,
    target_timeline_html,
)
from physical_relevance_impact import build_physical_relevance_impact_packet


JOB_DIR = ROOT / "agentic/logs/discovery_marathon_jobs"
QUALITATIVE_GRAPH_DIR = ROOT / "agentic/state/qualitative_mechanistic_graphs"
GEDANKEN_REPORT = ROOT / "agentic/reports/gedanken_experiments/latest.json"
SYMBOLIC_MATRIX_PROBE = ROOT / "agentic/reports/symbolic_matrix_probe/latest.json"
ANALYTIC_OBLIGATIONS = ROOT / "agentic/reports/analytic_estimate_obligations/latest.json"
BOUNDED_NUMERIC_PROBE = ROOT / "agentic/reports/bounded_numeric_probe/latest.json"
FINITE_ALGEBRA_INTERFACES = ROOT / "agentic/reports/finite_algebra_interfaces/latest.json"
SCIENTIFIC_CONTRIBUTION_MONITOR = ROOT / "agentic/reports/scientific_contribution_monitor/latest.json"
TARGET_LITERATURE_EVOLUTION = ROOT / "agentic/reports/target_literature_evolution/latest.json"
MACRO_STRATEGY_REPORT = ROOT / "agentic/reports/macro_strategy/latest.json"
STRATEGY_PROGRESSION_JUDGE = ROOT / "agentic/reports/strategy_progression_judge/latest.json"
PHYSICS_MATH_INTERPRETATION = ROOT / "agentic/reports/physics_math_interpretation/latest.json"
TIMELINE_PAPER_REPORT = ROOT / "agentic/reports/timeline_paper/latest.json"
PVSNP_NEGATIVE_TACTICS = ROOT / "agentic/reports/pvsnp_negative_tactics/latest.json"
PVSNP_INFERENCE_QUALITY = ROOT / "agentic/reports/pvsnp_inference_quality/latest.json"
PVSNP_PROOF_DELIVERY_QUEUE = ROOT / "agentic/reports/pvsnp_proof_delivery_queue/latest.json"
PVSNP_FF_TOP_PAPER_CRITERIA = ROOT / "agentic/reports/pvsnp_formula_footprints_referee_closure/top_paper_criteria.json"
PVSNP_FF_CLOSURE_LATEST = ROOT / "agentic/reports/pvsnp_formula_footprints_referee_closure/latest.json"
RESULT_SUBGOAL_ATLAS = ROOT / "agentic/reports/result_subgoal_atlas/latest.json"
PROBLEM_SPACE_MAP = ROOT / "agentic/reports/problem_space_map/latest.json"
DERIVATION_VAULT = ROOT / "agentic/reports/derivation_vault/latest.json"
YM_BLOCKER_SIGNATURE_REPORT = ROOT / "agentic/reports/blocker_signatures/targets/yang-mills-existence-and-mass-gap-target/latest.json"
MATHJAX_TEX_SVG_ASSET = ROOT / "agentic/assets/mathjax/tex-svg.js"
TIMELINE_START_CYCLE = 174
TEX_ALIGNMENT_ENVS = {
    "align",
    "alignat",
    "aligned",
    "alignedat",
    "array",
    "bmatrix",
    "cases",
    "gathered",
    "matrix",
    "pmatrix",
    "smallmatrix",
    "split",
    "vmatrix",
    "Vmatrix",
}
TEX_ENV_RE = re.compile(r"\\(begin|end)\{([^}]+)\}")
BACKTICK_RE = re.compile(r"`([^`]+)`")
EXPLICIT_INLINE_MATH_RE = re.compile(r"\\\((.*?)\\\)")
TOKEN_RE = re.compile(r"(\s+)")
INLINE_MATH_HINT_RE = re.compile(
    r"(\\[A-Za-z]+|[_^]\{?|\[[^\]]+\]|[<>]=?|!=|=|/|\||\b(?:det|ker|rank|dim|spec|Tr|tr|inf|liminf|limsup)\()"
)
MATH_TOKEN_RE = re.compile(r"^[A-Za-z0-9\\{}_^()[\]|.,+*/:=<>\-]+$")
SPECIAL_FORMULA_RE = re.compile(
    r"(?<![A-Za-z0-9_\\])("
    r"\\mathbb\{C\}\^[A-Za-z0-9]+\s*=\s*\\mathbb\{C\}\s*[A-Za-z]\s*\\oplus\s*1\^\\perp"
    r"|C\^[A-Za-z0-9]+\s*=\s*(?:C1|span\{[^}]+\}\\oplus1\^\\perp)"
    r"|[A-Za-z]_\{\\?[A-Za-z]+\}\s*=\s*\\widehat\{[A-Za-z]_\{\\?[A-Za-z]+\}\}\s*\\oslash\s*\\widehat\{[A-Za-z]_\{\\?[A-Za-z]+\}\}"
    r"|"
    r"(?:\\mathbb\{C\}|C)\^[A-Za-z0-9{}\\]+(?:\s*=\s*(?:\\mathbb\{C\}\s*)?(?:span\{[^}]+\}|[A-Za-z0-9{}\\]+)(?:\s*(?:\\oplus|\\oslash|[+\-*/=<>])\s*(?:span\{[^}]+\}|[A-Za-z0-9{}_^\\]+))*)?"
    r"|"
    r"[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?\s*=\s*"
    r"(?:widehat\s+[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?|overline\s+[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?|[A-Za-z0-9{}_^()[\]|.+*/:-]+)"
    r"(?:\s*(?:oslash|circ|\\(?:circ|oslash|le|ge|ne)|[+\-*/=<>]|∘)\s*"
    r"(?:widehat\s+[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?|overline\s+[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?|[A-Za-z0-9{}_^()[\]|.+*/:-]+))*"
    r"|"
    r"\\(?:widehat|overline)\s+[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?\s*(?:=|<=|>=|<|>)\s*"
    r"(?:\\(?:widehat|overline)\s+[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?|[A-Za-z0-9{}_^()[\]|.+*/:-]+)"
    r"(?:\s*(?:\\(?:circ|oslash|le|ge|ne)|[+\-*/=<>]|∘)\s*"
    r"(?:\\(?:widehat|overline)\s+[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?|[A-Za-z0-9{}_^()[\]|.+*/:-]+))*"
    r"(?:\s*:=\s*[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?)?"
    r"|\\(?:widehat|overline)\s+[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?\s*(?:<|>|<=|>=|\\le|\\ge)\s*0"
    r"|"
    r"[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?\([^)]*\)\s*=\s*(?:log|det|ker)\([^;,.]+\)"
    r"|"
    r"[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?\s*=\s*\\arg\\prod[^;,.]+"
    r"|[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?\s*=\s*(?:log|det|ker)\([^;,.]+\)"
    r"|[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?\s*=\s*"
    r"(?:\\[A-Za-z]+(?:\s*[A-Za-z0-9{}_^]+)?|[A-Za-z0-9{}_^()[\]|.+*/:-]+)"
    r"(?:\s*(?:\\(?:circ|oslash|le|ge|ne)|[+\-*/=<>]|∘)\s*"
    r"(?:\\[A-Za-z]+(?:\s*[A-Za-z0-9{}_^]+)?|[A-Za-z0-9{}_^()[\]|.+*/:-]+))*"
    r"|[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?\s*=\s*[A-Za-z0-9\\{}_^()[\]|.+*/:-]+\s*\\(?:circ|oslash)\s*[A-Za-z0-9\\{}_^()[\]|.+*/:-]+(?:\s*\+\s*[A-Za-z0-9\\{}_^()[\]|.+*/:-]+)?"
    r"|det\([^;,.]+\)(?:\s*(?:<|>|<=|>=|\\le|\\ge)\s*0)?"
    r"|\\(?:widehat|overline)\s+[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?"
    r")"
)
OS_FUNCTION_START_RE = re.compile(r"(?<![A-Za-z0-9_\\])S(?:_\{[^}]+\}|_[A-Za-z0-9]+)?\(")
OS_FUNCTION_TAIL_RE = re.compile(r"\s*(?:\\(?:ge|le|gt|lt|ne)|>=|<=|>|<|=)\s*0\b")


def normalize_generated_latex_text(value: Any) -> str:
    text = html.unescape(clean_text(value))
    text = text.replace("\x08igcup", r"\bigcup")
    text = text.replace("\x08dots", r"\dots")
    text = text.replace("\x08", "\\")
    text = text.replace("\x07epsilon", r"\epsilon")
    text = text.replace("\x07", "\\")
    text = text.replace("\x0b", "")
    text = text.replace("\x00", "")
    text = re.sub(r"\\mathbb\s+([A-Za-z])", r"\\mathbb{\1}", text)
    text = re.sub(r"\\mathbb(?!\{)([A-Za-z])", r"\\mathbb{\1}", text)
    for command in ["mathcal", "mathbf", "mathrm"]:
        text = re.sub(rf"\\{command}\s+([A-Za-z])", rf"\\{command}{{\1}}", text)
        text = re.sub(rf"\\{command}(?!\{{)([A-Za-z])", rf"\\{command}{{\1}}", text)
    for greek in ["alpha", "beta", "gamma", "delta", "eta", "lambda", "mu", "nu", "theta", "sigma", "tau", "omega"]:
        text = re.sub(rf"_({greek})(?![A-Za-z])", rf"_{{\\{greek}}}", text)
    text = re.sub(r"(?<!\\)\bOmega(?=_|\b)", r"\\Omega", text)
    text = re.sub(r"(?<!\\)\bDelta(?=_|\b)", r"\\Delta", text)
    text = re.sub(r"(?<!\\)\bTheta(?=_|\b)", r"\\Theta", text)
    text = re.sub(r"(?<!\\)\bperp\b", r"\\perp", text)
    text = re.sub(r"(?<!\\)\boslash\b", r"\\oslash", text)
    accent_arg = r"(\\[A-Za-z]+|[A-Za-z])(?:_\{[^}]+\}|_[A-Za-z0-9]+)?(?:\^\{[^}]+\}|\^[A-Za-z0-9]+)?"
    for command in ["widehat", "overline"]:
        text = re.sub(rf"(?<!\\)\b{command}\s+({accent_arg})", rf"\\{command}{{\1}}", text)
        text = re.sub(rf"\\{command}(?!\{{)\s+({accent_arg})", rf"\\{command}{{\1}}", text)
        text = re.sub(rf"\\{command}(?!\{{)(\\[A-Za-z]+(?:_\{{[^}}]+\}}|_[A-Za-z0-9]+)?)", rf"\\{command}{{\1}}", text)
        text = re.sub(rf"\\{command}\{{([A-Za-z])_([A-Za-z]+)\}}", rf"\\{command}{{\1_{{\2}}}}", text)
    return text


def sanitize_latex_for_mathjax(value: Any) -> str:
    """Escape bare ampersands while preserving TeX alignment separators."""
    text = normalize_generated_latex_text(value)
    replacements = [
        ("<=", r"\le "),
        (">=", r"\ge "),
        ("!=", r"\ne "),
        ("->", r"\to "),
        ("∘", r"\circ "),
        ("<", r"\lt "),
        (">", r"\gt "),
    ]
    for source, target in replacements:
        text = text.replace(source, target)
    output: list[str] = []
    alignment_stack: list[str] = []
    index = 0
    while index < len(text):
        match = TEX_ENV_RE.match(text, index)
        if match:
            command, env_name = match.groups()
            if env_name in TEX_ALIGNMENT_ENVS:
                if command == "begin":
                    alignment_stack.append(env_name)
                elif alignment_stack and alignment_stack[-1] == env_name:
                    alignment_stack.pop()
                elif env_name in alignment_stack:
                    alignment_stack.remove(env_name)
            output.append(match.group(0))
            index = match.end()
            continue
        char = text[index]
        escaped = index > 0 and text[index - 1] == "\\"
        if char == "&" and not escaped and not alignment_stack:
            output.append(r"\&")
        else:
            output.append(char)
        index += 1
    return "".join(output)


def looks_like_inline_math(value: str) -> bool:
    text = clean_text(value)
    if "/" in text and not re.search(r"(\\|[_^=<>]|\d|\b(?:det|ker|rank|dim|spec|Tr|tr|inf|liminf|limsup)\()", text):
        return False
    return bool(text and INLINE_MATH_HINT_RE.search(text))


def normalize_inline_latex(value: str) -> str:
    text = sanitize_latex_for_mathjax(value)
    for greek in ["alpha", "beta", "gamma", "delta", "epsilon", "eta", "lambda", "mu", "nu", "theta", "sigma", "tau", "omega"]:
        text = re.sub(rf"(?<!\\)\b{greek}\b", rf"\\{greek}", text)
    return text


def inline_math_html(value: str) -> str:
    latex = normalize_inline_latex(value)
    return rf'\({latex}\)'


def balanced_latex_fragment(value: str) -> bool:
    pairs = {"{": "}", "(": ")", "[": "]"}
    stack: list[str] = []
    escaped = False
    for char in value:
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


def render_auto_math_token(token: str) -> str:
    leading = ""
    trailing = ""
    core = token
    while core and core[0] in "":
        leading += core[0]
        core = core[1:]
    while core and core[-1] in ".,;:":
        trailing = core[-1] + trailing
        core = core[:-1]
    if core in {"<", ">", "<=", ">=", "!=", "="}:
        return html.escape(leading, quote=False) + inline_math_html(core) + html.escape(trailing, quote=False)
    if (
        len(core) >= 2
        and looks_like_inline_math(core)
        and MATH_TOKEN_RE.match(core)
        and balanced_latex_fragment(core)
        and not core.startswith("\\begin")
        and not core.startswith("\\end")
        and not core.startswith(("^", "_"))
        and core not in {r"\widehat", r"\overline"}
        and not core.endswith((r"\circ", r"\oslash", "=", "+", "-", "/", "*", "<", ">", "^", "_"))
    ):
        return html.escape(leading, quote=False) + inline_math_html(core) + html.escape(trailing, quote=False)
    return html.escape(token, quote=False)


def render_auto_math_segment(value: str) -> str:
    return "".join(
        part if part.isspace() else render_auto_math_token(part)
        for part in TOKEN_RE.split(value)
        if part != ""
    )


def find_balanced_parenthesis_end(value: str, open_index: int) -> int | None:
    depth = 0
    escaped = False
    for index in range(open_index, len(value)):
        char = value[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index + 1
            if depth < 0:
                return None
    return None


def looks_like_os_function_call(fragment: str) -> bool:
    return bool(re.search(r"(?:\\Theta|\bTheta\b|W\(|T_\{?\\?delta\}?|C_i|D_j|F_i|F_j)", fragment))


def extend_os_function_tail(value: str, end: int) -> int:
    match = OS_FUNCTION_TAIL_RE.match(value, end)
    if match:
        return match.end()
    return end


def render_special_formula_segment(value: str) -> str:
    output: list[str] = []
    index = 0
    for match in SPECIAL_FORMULA_RE.finditer(value):
        fragment = clean_text(match.group(1))
        trailing = ""
        while fragment and fragment[-1] in ".,;":
            trailing = fragment[-1] + trailing
            fragment = fragment[:-1]
        if not balanced_latex_fragment(fragment):
            continue
        output.append(render_auto_math_segment(value[index : match.start()]))
        output.append(inline_math_html(fragment))
        output.append(html.escape(trailing, quote=False))
        index = match.end()
    output.append(render_auto_math_segment(value[index:]))
    return "".join(output)


def render_special_math_segment(value: str) -> str:
    output: list[str] = []
    index = 0
    while index < len(value):
        match = OS_FUNCTION_START_RE.search(value, index)
        if not match:
            break
        end = find_balanced_parenthesis_end(value, match.end() - 1)
        if end is None:
            output.append(render_special_formula_segment(value[index : match.end()]))
            index = match.end()
            continue
        end = extend_os_function_tail(value, end)
        fragment = clean_text(value[match.start() : end])
        if not looks_like_os_function_call(fragment) or not balanced_latex_fragment(fragment):
            output.append(render_special_formula_segment(value[index:end]))
            index = end
            continue
        output.append(render_special_formula_segment(value[index : match.start()]))
        output.append(inline_math_html(fragment))
        index = end
    output.append(render_special_formula_segment(value[index:]))
    return "".join(output)


def render_plain_math_prose_html(value: str) -> str:
    value = normalize_generated_latex_text(value)
    for source, target in [
        ("<=", r" \le "),
        (">=", r" \ge "),
        ("!=", r" \ne "),
        ("->", r" \to "),
        ("=>", r" \Rightarrow "),
        ("<", r" \lt "),
        (">", r" \gt "),
    ]:
        value = value.replace(source, target)
    output: list[str] = []
    index = 0
    for match in EXPLICIT_INLINE_MATH_RE.finditer(value):
        output.append(render_special_math_segment(value[index : match.start()]))
        output.append(inline_math_html(match.group(1)))
        index = match.end()
    output.append(render_special_math_segment(value[index:]))
    return "".join(output)


def render_math_prose_html(value: Any) -> str:
    text = clean_text(value)
    output: list[str] = []
    index = 0
    for match in BACKTICK_RE.finditer(text):
        output.append(render_plain_math_prose_html(text[index : match.start()]))
        fragment = clean_text(match.group(1))
        if looks_like_inline_math(fragment):
            output.append(inline_math_html(fragment))
        else:
            output.append(f'<code>{html.escape(fragment)}</code>')
        index = match.end()
    output.append(render_plain_math_prose_html(text[index:]))
    return "".join(output)


def enrich_equations(equations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched = []
    for equation in equations:
        item = dict(equation)
        item["latex"] = normalize_generated_latex_text(item.get("latex", ""))
        item["latex_render"] = sanitize_latex_for_mathjax(item.get("latex", ""))
        enriched.append(item)
    return enriched


EMBEDDED_ACCENT_ARG_RE = r"(?:\\[A-Za-z]+|[A-Za-z])(?:_\{[^}]+\}|_[A-Za-z0-9]+)?(?:\^\{[^}]+\}|\^[A-Za-z0-9]+)?"


def normalize_embedded_tex_accents(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: normalize_embedded_tex_accents(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_embedded_tex_accents(item) for item in value]
    if not isinstance(value, str):
        return value
    text = value
    text = text.replace("\x08igcup", r"\bigcup")
    text = text.replace("\x08dots", r"\dots")
    text = text.replace("\x08", "\\")
    text = text.replace("\x07epsilon", r"\epsilon")
    text = text.replace("\x07", "\\")
    text = text.replace("\x0b", "")
    text = text.replace("\x00", "")
    for command in ["widehat", "overline"]:
        pattern = re.compile(rf"\\{command}(?!\{{)\s*({EMBEDDED_ACCENT_ARG_RE})")
        text = pattern.sub(lambda match, command=command: f"\\{command}{{{match.group(1)}}}", text)
    return text


def json_for_script(payload: dict[str, Any]) -> str:
    """Embed JSON in a script tag without HTML entities inside math fragments."""
    data = json.dumps(normalize_embedded_tex_accents(payload), ensure_ascii=False, sort_keys=True)
    return (
        data.replace("&", r"\u0026")
        .replace("<", r"\u003c")
        .replace(">", r"\u003e")
        .replace("\u2028", r"\u2028")
        .replace("\u2029", r"\u2029")
    )


def trim_trailing_whitespace(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"


CSS = r"""
:root {
  color-scheme: dark;
  --bg: #070b10;
  --surface: #101820;
  --surface-2: #15212c;
  --surface-3: #1b2a37;
  --line: #293845;
  --text: #edf6fb;
  --muted: #a7b6c3;
  --gold: #f0c95b;
  --cyan: #59d6f4;
  --green: #63d489;
  --red: #ff6b7a;
  --blue: #8aabff;
  --violet: #c991ff;
  --orange: #ffb15c;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font: 14px/1.48 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
button, input, select { font: inherit; }
.shell { min-height: 100vh; }
.hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 20px;
  padding: 24px clamp(16px, 4vw, 44px);
  border-bottom: 1px solid var(--line);
  background:
    linear-gradient(180deg, rgba(16,24,32,.96), rgba(7,11,16,.98)),
    radial-gradient(circle at 15% 0%, rgba(89,214,244,.14), transparent 34%);
}
.eyebrow {
  margin: 0 0 6px;
  color: var(--gold);
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: .08em;
}
h1 {
  margin: 0;
  font-size: clamp(26px, 3vw, 42px);
  line-height: 1.05;
  letter-spacing: 0;
}
.subtitle {
  max-width: 1000px;
  margin: 10px 0 0;
  color: var(--muted);
}
.metric-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(120px, 1fr));
  gap: 8px;
  align-self: start;
}
.metric {
  border: 1px solid var(--line);
  background: var(--surface);
  border-radius: 8px;
  padding: 10px 12px;
  min-width: 0;
}
.metric strong { display: block; font-size: 22px; line-height: 1.1; }
.metric span { color: var(--muted); font-size: 12px; }
.controls {
  display: grid;
  grid-template-columns: minmax(220px, 1fr) repeat(3, minmax(150px, 200px));
  gap: 10px;
  padding: 12px clamp(16px, 4vw, 44px);
  border-bottom: 1px solid var(--line);
  background: #0b1118;
}
.control {
  width: 100%;
  min-height: 38px;
  color: var(--text);
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 7px;
  padding: 8px 10px;
}
.tabs {
  display: flex;
  gap: 8px;
  padding: 14px clamp(16px, 4vw, 44px) 0;
  overflow-x: auto;
}
.tab {
  border: 1px solid var(--line);
  background: var(--surface);
  color: var(--muted);
  border-radius: 7px;
  padding: 8px 12px;
  min-height: 36px;
  cursor: pointer;
  white-space: nowrap;
}
.tab.active {
  color: var(--text);
  border-color: var(--cyan);
  background: #102637;
}
.content { padding: 16px clamp(16px, 4vw, 44px) 40px; }
.section { display: none; }
.section.active { display: block; }
.grid {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(320px, .8fr);
  gap: 14px;
}
.panel, .card {
  border: 1px solid var(--line);
  background: var(--surface);
  border-radius: 8px;
  padding: 14px;
  min-width: 0;
}
.panel h2, .card h3, .card h4 { margin: 0 0 10px; letter-spacing: 0; }
.panel h2 { font-size: 18px; }
.card { margin-bottom: 10px; background: var(--surface-2); }
.card.primary { border-left: 4px solid var(--cyan); }
.card.codex { border-left: 4px solid var(--blue); }
.card.api { border-left: 4px solid var(--green); }
.card.fail { border-left: 4px solid var(--red); }
.card.story { border-left: 4px solid var(--violet); }
.card.review { border-left: 4px solid var(--orange); }
.row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.pill {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 2px 8px;
  color: var(--text);
  background: #0c131b;
  font-size: 12px;
}
.pill.good { color: var(--green); border-color: var(--green); }
.pill.warn { color: var(--orange); border-color: var(--orange); }
.pill.fail { color: var(--red); border-color: var(--red); }
.pill.info { color: var(--cyan); border-color: var(--cyan); }
.muted { color: var(--muted); }
.code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 12px;
  overflow-wrap: anywhere;
}
.timeline {
  position: relative;
  padding-left: 18px;
}
.timeline::before {
  content: "";
  position: absolute;
  left: 5px;
  top: 4px;
  bottom: 8px;
  width: 2px;
  background: var(--line);
}
.timeline .card { position: relative; }
.timeline .card::before {
  content: "";
  position: absolute;
  left: -18px;
  top: 16px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--cyan);
}
.quality {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 8px;
}
.bar {
  height: 8px;
  width: 100%;
  border: 1px solid var(--line);
  background: #0b1118;
  border-radius: 999px;
  overflow: hidden;
  margin-top: 8px;
}
.bar > span {
  display: block;
  height: 100%;
  background: var(--green);
}
.equation {
  margin: 10px 0;
  padding: 10px;
  background: #0b1118;
  border: 1px solid var(--line);
  border-radius: 8px;
  overflow-x: auto;
}
.definition-assumption-block {
  margin: 10px 0;
  padding: 12px;
  border: 1px solid rgba(136, 165, 191, .28);
  border-left: 4px solid var(--gold);
  border-radius: 8px;
  background: rgba(255, 209, 102, .06);
}
.definition-assumption-block h4 {
  margin: 0 0 8px;
  font-size: 14px;
  color: var(--gold);
}
.inline-math {
  display: inline-block;
  max-width: 100%;
  overflow-x: auto;
  vertical-align: middle;
}
details {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid var(--line);
}
summary { cursor: pointer; color: var(--cyan); }
.empty {
  border: 1px dashed var(--line);
  border-radius: 8px;
  padding: 18px;
  color: var(--muted);
}
.runtime-diagnostic {
  margin: 12px clamp(16px, 4vw, 44px) 0;
  padding: 12px 14px;
  border: 1px solid rgba(255, 176, 32, .5);
  border-left: 4px solid var(--orange);
  border-radius: 8px;
  background: rgba(255, 176, 32, .08);
  color: var(--text);
  display: none;
}
.runtime-diagnostic strong { color: var(--orange); }
.runtime-diagnostic code {
  color: var(--cyan);
  white-space: pre-wrap;
}
.queue-list {
  margin: 0;
  padding-left: 20px;
}
.queue-list li {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface-2);
}
.queue-meta {
  display: block;
  margin-bottom: 4px;
  color: var(--cyan);
  font-size: 12px;
}
.rank-score {
  display: grid;
  grid-template-columns: auto minmax(120px, 1fr);
  gap: 8px;
  align-items: center;
  margin: 8px 0;
}
.rank-score strong {
  color: var(--gold);
  font-size: 20px;
}
.payoff-list {
  margin: 8px 0 0;
  padding-left: 20px;
}
.payoff-list li { margin: 6px 0; }
.graph-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 10px;
}
.graph-node { border-left: 4px solid var(--cyan); }
.graph-edge { border-left: 4px solid var(--gold); }
.graph-brief {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(280px, .85fr);
  gap: 14px;
  margin-bottom: 14px;
}
.graph-hero {
  border: 1px solid var(--line);
  background: var(--surface-2);
  border-radius: 8px;
  padding: 16px;
}
.graph-hero p { margin: 8px 0 0; }
.mechanism-flow {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 10px;
  margin: 14px 0;
}
.mechanism-step {
  position: relative;
  border: 1px solid var(--line);
  background: #0b1118;
  border-radius: 8px;
  padding: 12px;
  min-height: 118px;
}
.mechanism-step strong {
  display: block;
  color: var(--gold);
  margin-bottom: 6px;
}
.relation-board {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 12px;
  margin-top: 10px;
}
.relation-card {
  border: 1px solid var(--line);
  border-left: 4px solid var(--gold);
  background: var(--surface-2);
  border-radius: 8px;
  padding: 14px;
}
.relation-card.falsifies { border-left-color: var(--red); }
.relation-card.decreases { border-left-color: var(--blue); }
.relation-card.constrains { border-left-color: var(--orange); }
.relation-card.enables, .relation-card.induces { border-left-color: var(--green); }
.relation-title {
  display: block;
  color: var(--text);
  font-weight: 700;
  margin-bottom: 6px;
}
.relation-label {
  color: var(--cyan);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: .04em;
}
.relation-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 10px;
}
.relation-list .card { margin-bottom: 0; }
.compact-list {
  margin: 8px 0 0;
  padding-left: 18px;
}
.compact-list li { margin: 5px 0; }
.operation-flow {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 10px;
  margin: 14px 0;
}
.operation-flow .card { margin-bottom: 0; }
.edge-arrow {
  display: block;
  margin: 6px 0;
  color: var(--gold);
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  overflow-wrap: anywhere;
}
@media (max-width: 900px) {
  .hero, .grid, .controls, .graph-brief { grid-template-columns: 1fr; }
  .metric-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
"""


JS = r"""
let DATA = {};
try {
  DATA = JSON.parse(document.getElementById('marathon-data').textContent);
} catch (error) {
  DATA = { report: { target_id: 'discovery-marathon' }, parse_error: String(error) };
}
const TIMELINE_MODE = Boolean(DATA.timeline_mode);
const state = { tab: 'overview', query: '', engine: 'all', attempt: 'all', job: 'all' };

const $ = (id) => document.getElementById(id);
const esc = (v) => String(v ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
const tex = (v) => String(v ?? '').replace(/[<>"']/g, ch => ({'<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
const clean = (v) => String(v ?? '').replace(/\s+/g, ' ').trim();
const lower = (v) => clean(v).toLowerCase();
const pct = (num, den) => den ? Math.max(4, Math.round((num / den) * 100)) : 0;
const rich = (htmlValue, fallback='') => htmlValue || esc(fallback);

function pill(text, cls='') { return `<span class="pill ${cls}">${esc(text)}</span>`; }
function metric(value, label) { return `<div class="metric"><strong>${esc(value)}</strong><span>${esc(label)}</span></div>`; }
function qualityChip(label, value) { return `<div class="metric"><strong>${esc(value)}</strong><span>${esc(label)}</span></div>`; }
function listRich(items) { return (items || []).length ? `<ul>${items.map(item => `<li>${rich(item.html, item.text || item)}</li>`).join('')}</ul>` : ''; }
function listEsc(items) { return (items || []).length ? `<ul>${items.map(item => `<li>${esc(item.text || item)}</li>`).join('')}</ul>` : ''; }
function listMaybeRich(items, htmlItems) { return (items || []).length ? `<ul class="compact-list">${items.map((item, idx) => `<li>${rich((htmlItems || [])[idx], item)}</li>`).join('')}</ul>` : ''; }
function runtimeDiagnostic(message, detail='') {
  const box = $('runtimeDiagnostic');
  if (!box) return;
  box.style.display = 'block';
  box.innerHTML = `<strong>${esc(message)}</strong>${detail ? `<br><code>${esc(detail).slice(0, 1200)}</code>` : ''}`;
}
function safeTypeset() {
  try {
    if (window.MathJax?.typesetClear) window.MathJax.typesetClear([$('view')]);
    if (window.MathJax?.typesetPromise) {
      window.MathJax.typesetPromise([$('view')]).catch(error => {
        runtimeDiagnostic('Mathematical rendering reported a recoverable problem; navigation remains available.', String(error));
      });
    }
  } catch (error) {
    runtimeDiagnostic('Mathematical rendering reported a recoverable problem; navigation remains available.', String(error));
  }
}

function matchesFilters(cycle) {
  const q = state.query;
  const engine = cycle.engine || '';
  const attempt = cycle.api_attempt || cycle.codex_attempt || 'not_recorded';
  const job = cycle.job_id || '';
  const text = lower(JSON.stringify(cycle));
  return (!q || text.includes(q)) &&
    (state.engine === 'all' || engine === state.engine) &&
    (state.attempt === 'all' || attempt === state.attempt) &&
    (state.job === 'all' || job === state.job);
}

function cycles() { return TIMELINE_MODE ? (DATA.timeline_cycles || DATA.all_cycles || []) : (DATA.research_cycles || []); }
function filteredCycles() { return cycles().filter(matchesFilters); }

function renderOverview() {
  const q = DATA.quality || {};
  const proofDepth = DATA.proof_depth_control_summary || DATA.report?.proof_depth_control_summary || {};
  const literatureGap = DATA.avenue_literature_gap_summary || DATA.report?.avenue_literature_gap_summary || {};
  const physical = DATA.physical_relevance_impact_summary || DATA.report?.physical_relevance_impact_summary || {};
  const artifactStop = DATA.artifact_or_stop_control || {};
  const artifactStopSummary = DATA.artifact_or_stop_summary || DATA.report?.artifact_or_stop_summary || {};
  const failureArch = DATA.failure_archaeology_summary || DATA.report?.failure_archaeology_summary || {};
  const visualConcept = DATA.visual_conceptualization_summary || DATA.report?.visual_conceptualization_summary || {};
  const story = DATA.current_story || {};
  const summaryControl = DATA.summary_analysis_control || {};
  const contribution = DATA.scientific_contribution_monitor || {};
  const contributionMetrics = contribution.metrics || {};
  const recent = cycles().slice(-8);
  return `
    <section class="section active">
      <div class="grid">
        <div class="panel">
          <h2>Current Mathematical Story</h2>
          <p>${rich(story.headline_html, story.headline)}</p>
          <div class="card story">
            <h3>Latest Learning</h3>
            <p>${rich(story.latest_learning_html, story.latest_learning)}</p>
            <h3>Current Obstruction</h3>
            <p>${rich(story.current_obstruction_html, story.current_obstruction)}</p>
            <h3>Next Analysis</h3>
            <p>${rich(summaryControl.next_experiment_html, story.next_experiment)}</p>
            ${summaryControl.when_to_stop ? `<h3>When To Stop</h3><p>${rich(summaryControl.when_to_stop_html, summaryControl.when_to_stop)}</p>` : ''}
            ${summaryControl.global_problem_contribution_html ? `<h3>How This Adds To The Global Problem</h3><p>${rich(summaryControl.global_problem_contribution_html, summaryControl.global_problem_contribution)}</p>` : ''}
            ${summaryControl.payoff_criteria?.length ? `<h3>Payoff Criteria</h3>${listRich(summaryControl.payoff_criteria)}` : ''}
            ${summaryControl.required_skills?.length ? `<h3>Skills To Apply</h3><p>${summaryControl.required_skills.map(skill => pill(skill, 'info')).join('')}</p>` : ''}
          </div>
          <h2>Latest Valid Cycles</h2>
          ${recent.map(renderCycleCard).join('') || '<div class="empty">No research cycles yet.</div>'}
        </div>
        <aside class="panel">
          <h2>Accumulated Quality</h2>
          <div class="quality">
            ${qualityChip('Real cycles', q.valid_research_cycles || 0)}
            ${qualityChip('Average seconds', q.average_elapsed_seconds || 0)}
            ${qualityChip('Minimum equations', q.minimum_quality?.equations || 0)}
            ${qualityChip('Minimum steps', q.minimum_quality?.derivation_steps || 0)}
            ${qualityChip('Minimum falsifiers', q.minimum_quality?.falsifiers || 0)}
            ${qualityChip('Markers ok', q.all_markers_ok ? 'yes' : 'no')}
          </div>
          <h2>Engine Mix</h2>
          ${renderCounts(q.engine_counts || {})}
          <h2>Attempt Mix</h2>
          ${renderCounts(q.attempt_counts || {})}
          <h2>Proof Depth Control</h2>
          <div class="card story">
            <div class="row">
              ${pill(`${proofDepth.packet_count || 0} packets`, proofDepth.packet_count ? 'good' : 'warn')}
              ${pill(proofDepth.proof_gate || 'proof-depth validator', 'info')}
            </div>
            <p><strong>Release decisions:</strong> ${esc(JSON.stringify(proofDepth.release_decision_counts || {}))}</p>
            <p><strong>Transfer substance:</strong> ${esc(JSON.stringify(proofDepth.transfer_substance_counts || {}))}</p>
          </div>
          <h2>Literature Gap Gate</h2>
          <div class="card story">
            <div class="row">
              ${pill(`${literatureGap.warrant_count || 0} literature warrants`, literatureGap.warrant_count ? 'good' : 'warn')}
              ${pill(literatureGap.validator || 'literature-gap validator', 'info')}
            </div>
            <p><strong>Investment decisions:</strong> ${esc(JSON.stringify(literatureGap.investment_decision_counts || {}))}</p>
            <p><strong>Allowed next modes:</strong> ${esc(JSON.stringify(literatureGap.allowed_next_mode_counts || {}))}</p>
            <p><strong>Gate:</strong> ${esc(literatureGap.gate_rule || '')}</p>
            <p><strong>Full packet:</strong> <code>${esc(literatureGap.latest_json || '')}</code></p>
          </div>
          <h2>Physical Relevance</h2>
          <div class="card story">
            <div class="row">
              ${pill(`${physical.packet_count || 0} assessments`, physical.packet_count ? 'good' : 'warn')}
              ${pill(`${physical.persisted_packet_count || 0} persisted`, physical.persisted_packet_count ? 'good' : 'warn')}
              ${pill(`${physical.legacy_derived_assessment_count || 0} legacy`, physical.legacy_derived_assessment_count ? 'info' : 'warn')}
              ${pill(physical.validator || 'physical-impact validator', 'info')}
            </div>
            <p><strong>Decisions:</strong> ${esc(JSON.stringify(physical.relevance_decision_counts || {}))}</p>
            <p><strong>Target gates:</strong> ${esc(JSON.stringify(physical.target_commitment_counts || {}))}</p>
            <p><strong>Unification power scores:</strong> ${esc(JSON.stringify(physical.unification_power_score_counts || {}))}</p>
          </div>
          <h2>Artifact-Or-Stop</h2>
          <div class="card story ${artifactStopSummary.broad_api_marathon_blocked ? 'fail' : ''}">
            <div class="row">
              ${pill(artifactStopSummary.endpoint_mode || artifactStop.artifact_or_stop_control?.next_endpoint_mode || 'not generated', artifactStopSummary.broad_api_marathon_blocked ? 'fail' : 'info')}
              ${pill(`${artifactStopSummary.endpoint_repetition_count || 0} repeats`, artifactStopSummary.endpoint_repetition_count ? 'warn' : 'info')}
              ${pill(artifactStopSummary.validator || artifactStop.artifact_or_stop_control?.validator || 'artifact-or-stop validator', 'info')}
            </div>
            <p><strong>Broad endpoint API marathon blocked:</strong> ${esc(String(artifactStopSummary.broad_api_marathon_blocked || artifactStop.artifact_or_stop_control?.broad_api_marathon_blocked || false))}</p>
            <p><strong>Missing artifacts:</strong> ${esc(JSON.stringify(artifactStopSummary.missing_artifacts || []))}</p>
            <p><strong>Gate:</strong> ${esc(artifactStopSummary.gate_rule || artifactStop.signature_policy || '')}</p>
            <p><strong>Full packet:</strong> <code>${esc(artifactStopSummary.latest_json || artifactStop.latest_json || '')}</code></p>
          </div>
          <h2>Failure Archaeology</h2>
          <div class="card story ${failureArch.failure_detected ? 'fail' : ''}">
            <div class="row">
              ${pill(failureArch.failure_detected ? 'failure detected' : 'no failure detected', failureArch.failure_detected ? 'fail' : 'good')}
              ${pill(failureArch.route_disposition || 'pending disposition', 'info')}
            </div>
            <p><strong>Cycle set:</strong> ${esc(failureArch.cycle_set_id || '')}</p>
            <p>${esc(failureArch.failure_summary || '')}</p>
            <p><strong>Detected heuristics:</strong> ${esc(JSON.stringify(failureArch.detected_heuristics || []))}</p>
            <p><strong>Full packet:</strong> <code>${esc(failureArch.latest_json || '')}</code></p>
          </div>
          <h2>Visual Conceptualization</h2>
          <div class="card story">
            <div class="row">
              ${pill(`${visualConcept.concept_count || 0} metaphors`, visualConcept.concept_count ? 'good' : 'warn')}
              ${pill(`${visualConcept.hypothesis_output_count || 0} route outputs`, visualConcept.hypothesis_output_count ? 'good' : 'warn')}
              ${pill(`${visualConcept.quarantined_or_rejected_count || 0} quarantined/rejected`, visualConcept.quarantined_or_rejected_count ? 'warn' : 'info')}
            </div>
            <p><strong>Headline metaphor:</strong> ${esc(visualConcept.headline_metaphor || '')}</p>
            <p><strong>Route consequences:</strong> ${esc(JSON.stringify(visualConcept.route_consequences || []))}</p>
            <p class="muted">Reflection artifact only unless a preservation audit promotes a concrete artifact, falsifier, route mutation, or representation requirement.</p>
            <p><strong>Full packet:</strong> <code>${esc(visualConcept.latest_json || '')}</code></p>
          </div>
          <h2>Scientific Contribution Monitor</h2>
          <div class="card story">
            <div class="row">${pill(contribution.contribution_aim_status || 'not generated', contribution.contribution_aim_status === 'handoff_ready' ? 'good' : contribution.contribution_aim_status === 'near_stepping_stone_available' ? 'info' : 'warn')}${pill(`${contributionMetrics.active_candidate_count || 0} active`, 'info')}${pill(`${contributionMetrics.near_stepping_stone_count || 0} near`, 'info')}${pill(`${contributionMetrics.publishable_handoff_count || 0} publishable`, contributionMetrics.publishable_handoff_count ? 'good' : 'warn')}</div>
            <p>${esc(contribution.next_contribution_objective || '')}</p>
            <p><strong>Anti-infinite progression:</strong> ${esc(contribution.loop_policy?.anti_infinite_progression_rule || '')}</p>
          </div>
        </aside>
      </div>
    </section>`;
}

function renderCounts(obj) {
  const total = Object.values(obj).reduce((a,b) => a + Number(b || 0), 0);
  return Object.entries(obj).map(([key, value]) => `
    <div class="card">
      <div class="row"><strong>${esc(key)}</strong>${pill(value, 'info')}</div>
      <div class="bar"><span style="width:${pct(value,total)}%"></span></div>
    </div>
  `).join('') || '<div class="empty">No counts.</div>';
}

function renderJobs() {
  return `<section class="section active">
    <div class="panel">
      <h2>All Marathon Jobs</h2>
      ${(DATA.jobs || []).map(job => `
        <div class="card ${job.status === 'completed' ? 'api' : job.status === 'completed_with_failures' ? 'fail' : ''}">
          <div class="row">
            <h3>${esc(job.job_id)}</h3>
            ${pill(job.status, job.status === 'completed' ? 'good' : job.status === 'interrupted' ? 'warn' : 'fail')}
            ${pill(`${job.completed_cycles || 0} cycles`, 'info')}
            ${pill(`${job.failed_cycle_attempts || 0} failures`, job.failed_cycle_attempts ? 'fail' : 'good')}
          </div>
          <p class="muted code">${esc(job.log_path)}</p>
          <p>Updated: ${esc(job.updated_utc || '')}</p>
          ${job.failure_events?.length ? `<details open><summary>Operational failures</summary>${job.failure_events.map(f => `<div class="card fail"><strong>Attempt ${esc(f.cycle_number_in_job)}</strong><p>${esc(clean(f.output_tail)).slice(0, 900)}</p></div>`).join('')}</details>` : ''}
        </div>`).join('') || '<div class="empty">No job logs found.</div>'}
    </div>
  </section>`;
}

function renderTimeline() {
  const rows = filteredCycles();
  const title = TIMELINE_MODE ? 'Content-Specific Full Timeline' : 'Research Cycle Timeline';
  const start = DATA.timeline_start_cycle || '';
  return `<section class="section active">
    <div class="panel">
      <h2>${title}</h2>
      ${TIMELINE_MODE ? `<p class="muted">Visible timeline starts at cycle-${String(start).padStart(4, '0')}, where the run shifted into content-specific mathematical work. Earlier persisted cycles remain embedded for audit completeness.</p>` : ''}
      <p class="muted">${rows.length} cycles match the current filters.</p>
      <div class="timeline">${rows.map(renderCycleCard).join('') || '<div class="empty">No matching cycles.</div>'}</div>
      ${TIMELINE_MODE ? renderIntegratedReasoningOperations() : ''}
      ${TIMELINE_MODE ? renderNextQueueBlock('Next Analyses Queue') : ''}
    </div>
  </section>`;
}

function renderIntegratedReasoningOperations() {
  const graph = DATA.qualitative_mechanistic_graph || {};
  const layer = DATA.parsimonious_probe_layer || {};
  const finite = layer.finite_algebra_interfaces || {};
  const finitePacket = (finite.packets || [])[0] || {};
  const edges = (graph.edges || []).slice(0, 5);
  const gedanken = (DATA.gedanken_experiments?.packets || []).slice(0, 4);
  const queue = (DATA.timeline_ranked_next_experiment_queue || DATA.ranked_next_experiment_queue || []).slice(0, 6);
  return `<div class="panel">
    <h2>Integrated Reasoning Operations</h2>
    <p class="muted">This is the same expert-facing timeline flow, enriched with the current control operations that steer the next cycles: finite algebra interfaces, graph constraints, thought-experiment probes, and ranked next analyses.</p>
    <div class="operation-flow">
      <div class="card story">
        <div class="row"><h3>Equational Control</h3>${pill(finitePacket.epistemic_status || 'not generated','info')}</div>
        <p><strong>Carrier:</strong> ${esc(finitePacket.carrier?.name || '')}</p>
        <p><strong>Side-condition count:</strong> ${esc((finitePacket.side_conditions || []).length)} · <strong>Falsifier shapes:</strong> ${esc((finitePacket.falsifier_templates || []).length)}</p>
        <ul>${(finitePacket.exact_identities || []).map(identity => `<li>${esc(identity.name || identity.id)} \\(${tex(identity.latex || '')}\\)</li>`).join('')}</ul>
      </div>
      <div class="card">
        <div class="row"><h3>Graph Control</h3>${pill(`${edges.length} active edges`,'info')}</div>
        <ul>${edges.map(edge => `<li><strong>${esc(edge.id)}</strong>: ${rich(edge.qualitative_behavior_html, edge.qualitative_behavior || edge.direction || '')}</li>`).join('')}</ul>
      </div>
      <div class="card story">
        <div class="row"><h3>Gedanken Follow-Ups</h3>${pill(`${gedanken.length} probes`,'info')}</div>
        <ul>${gedanken.map(packet => `<li><strong>${esc(packet.packet_id)}</strong>: ${esc(packet.situation?.purpose || packet.need_decision || '')}</li>`).join('')}</ul>
      </div>
      <div class="card review">
        <div class="row"><h3>Next Analysis Control</h3>${pill(`${queue.length} ranked targets`,'good')}</div>
        <ol>${queue.map(item => `<li>${rich(item.next_experiment_html, item.next_experiment || '')}<br><span class="muted">payoff: ${esc((item.payoff_criteria || []).map(c => c.text || c).slice(0, 1).join(''))}</span></li>`).join('')}</ol>
      </div>
    </div>
  </div>`;
}

function renderCycleCard(cycle) {
  const attempt = cycle.api_attempt || cycle.codex_attempt || 'not_recorded';
  const cls = cycle.engine === 'codex_exec' ? 'codex' : cycle.engine === 'azure_responses_api' ? 'api' : 'primary';
  const equations = cycle.equations || [];
  const valid = Boolean(cycle.valid_as_research_cycle);
  const depth = cycle.proof_depth_control || {};
  const physical = cycle.physical_relevance_impact || {};
  return `<article class="card ${cls}" data-engine="${esc(cycle.engine)}">
    <div class="row">
      <h3>${esc(cycle.cycle_id)}</h3>
      ${pill(cycle.execution_mode || 'mode?', valid ? 'good' : 'warn')}
      ${pill(cycle.engine || 'no engine', cycle.engine ? 'info' : 'warn')}
      ${pill(attempt, attempt === 'compact_retry' ? 'warn' : valid ? 'good' : 'warn')}
      ${pill(`${cycle.research_seconds_elapsed || 0}s`)}
    </div>
    <p><strong>${esc(cycle.branch_title)}</strong></p>
    <div class="row">
      ${pill(`${cycle.lemma_count} lemmas`)}
      ${pill(`${cycle.equation_count} equations`)}
      ${pill(`${cycle.derivation_step_count} steps`)}
      ${pill(`${cycle.falsifier_count} falsifiers`)}
      ${pill(`${cycle.dependency_update_count} deps`)}
      ${pill(cycle.markers_ok ? 'markers ok' : 'marker issue', cycle.markers_ok ? 'good' : 'fail')}
    </div>
    ${depth.release_decision ? `<div class="row">
      ${pill(`depth: ${depth.release_decision}`, depth.release_decision === 'promote' || depth.release_decision === 'proof_delivery' ? 'good' : depth.release_decision === 'support_only' ? 'warn' : 'fail')}
      ${pill(`gate: ${depth.hard_gate || 'missing'}`, depth.hard_gate ? 'info' : 'fail')}
      ${pill(`transfer: ${depth.transfer_substance_verdict || 'missing'}`, depth.transfer_substance_verdict === 'substantive_transfer' || depth.transfer_substance_verdict === 'not_transfer' ? 'good' : 'warn')}
      ${pill(`pressure: ${depth.pressure_kind || 'missing'}`, 'info')}
    </div>` : ''}
    ${physical.relevance_decision ? `<div class="row">
      ${pill(`physics: ${physical.relevance_decision}`, physical.relevance_decision === 'physically_relevant_candidate' ? 'good' : physical.relevance_decision === 'math_support_only_pending_physical_handoff' ? 'warn' : 'fail')}
      ${pill(`carrier: ${physical.physical_carrier || 'missing'}`, physical.physical_carrier && physical.physical_carrier !== 'missing physical carrier' ? 'info' : 'fail')}
      ${pill(`unification: ${physical.unification_power_score ?? 0}`, Number(physical.unification_power_score || 0) >= 3 ? 'good' : 'warn')}
    </div>` : ''}
    <p>${rich(cycle.mathematical_learning_html, cycle.mathematical_learning)}</p>
    <details ${TIMELINE_MODE ? 'open' : ''}>
      <summary>Reasoning operations: derivation, equations, falsifiers, and next experiment</summary>
      <p><strong>Blocking gap:</strong> ${rich(cycle.blocking_gap_html, cycle.blocking_gap)}</p>
      ${(cycle.definitions || []).length || (cycle.assumptions || []).length ? `
        <section class="definition-assumption-block">
          <h4>Definitions And Assumptions</h4>
          ${cycle.definition_assumption_elicitation_note ? `<p class="muted">${rich(cycle.definition_assumption_elicitation_note_html, cycle.definition_assumption_elicitation_note)}</p>` : ''}
          ${(cycle.definitions || []).length ? `<p><strong>Definitions:</strong></p><ul class="compact-list">${cycle.definitions.map((item, idx) => `<li>${rich((cycle.definitions_html || [])[idx], item)}</li>`).join('')}</ul>` : ''}
          ${(cycle.assumptions || []).length ? `<p><strong>Assumptions:</strong></p><ul class="compact-list">${cycle.assumptions.map((item, idx) => `<li>${rich((cycle.assumptions_html || [])[idx], item)}</li>`).join('')}</ul>` : ''}
        </section>` : ''}
      ${(cycle.derivation_steps || []).map((step, idx) => `<p><strong>Step ${idx + 1}.</strong> ${rich((cycle.derivation_steps_html || [])[idx], step)}</p>`).join('')}
      ${equations.map(eq => `<div class="equation"><div>\\[${tex(eq.latex_render || eq.latex || '')}\\]</div><p><strong>Valid when:</strong> ${esc(eq.valid_when || '')}</p></div>`).join('')}
      ${depth.release_decision ? `<p><strong>Proof-depth demotion trigger:</strong> ${esc(depth.demotion_trigger || '')}</p>` : ''}
      ${physical.relevance_decision ? `<section class="definition-assumption-block">
        <h4>Physical Relevance And General Impact</h4>
        <p><strong>Decision:</strong> ${esc(physical.relevance_decision || '')}</p>
        <p><strong>Carrier:</strong> ${esc(physical.physical_carrier || '')}</p>
        <p><strong>Target gates:</strong> ${esc((physical.target_commitments_touched || []).join(', '))}</p>
        <p><strong>Unification power:</strong> ${esc(physical.unification_power_score ?? 0)}</p>
        <p><strong>Impact:</strong> ${rich(physical.general_impact_claim_html, physical.general_impact_claim || '')}</p>
        <p><strong>Drift risk:</strong> ${esc(physical.incremental_math_drift_risk || '')}</p>
        <p><strong>Next physical test:</strong> ${rich(physical.next_physical_relevance_test_html, physical.next_physical_relevance_test || '')}</p>
      </section>` : ''}
      <p><strong>Next experiment:</strong> ${rich(cycle.next_experiment_html, cycle.next_experiment)}</p>
      ${(cycle.falsifiers || []).length ? `<p><strong>Falsifiers:</strong></p><ul>${cycle.falsifiers.map((f, idx) => `<li>${rich((cycle.falsifiers_html || [])[idx], f)}</li>`).join('')}</ul>` : ''}
    </details>
  </article>`;
}

function renderStory() {
  const story = TIMELINE_MODE ? (DATA.timeline_storyline || {}) : (DATA.research_storyline || DATA.timeline_storyline || {});
  const beats = story.beats || DATA.current_story?.recent_storyline || [];
  const start = story.start_cycle || DATA.timeline_start_cycle || '';
  return `<section class="section active">
    <div class="panel">
      <h2>Accumulated Physics Story</h2>
      <p>${esc(story.headline || DATA.current_story?.headline || '')}</p>
      ${TIMELINE_MODE ? `<p class="muted">Cumulative story starts at cycle-${String(start).padStart(4, '0')} and follows ${beats.length} content-specific research beats. It uses the same start point as the visible timeline.</p>` : ''}
      ${beats.map(beat => `<div class="card story">
        <div class="row"><h3>${esc(beat.cycle_id)} · ${esc(beat.branch_title)}</h3>${pill(beat.engine || 'engine?', 'info')}${pill(beat.attempt || 'attempt?')}</div>
        <p>${rich(beat.learning_html, beat.learning)}</p>
        ${beat.blocking_gap ? `<p><strong>Pressure:</strong> ${rich(beat.blocking_gap_html, beat.blocking_gap)}</p>` : ''}
        <p><strong>Next:</strong> ${rich(beat.next_experiment_html, beat.next_experiment)}</p>
        ${beat.when_to_stop ? `<p><strong>When to stop:</strong> ${rich(beat.when_to_stop_html, beat.when_to_stop)}</p>` : ''}
        ${beat.premature_stop_guard ? `<p><strong>Do not stop prematurely if:</strong> ${rich(beat.premature_stop_guard_html, beat.premature_stop_guard)}</p>` : ''}
        ${beat.global_problem_contribution_html ? `<p><strong>How does it add to the global problem:</strong> ${rich(beat.global_problem_contribution_html, beat.global_problem_contribution)}</p>` : ''}
        ${beat.required_skills?.length ? `<p><strong>Skills to apply:</strong> ${beat.required_skills.map(skill => pill(skill, 'info')).join('')}</p>` : ''}
      </div>`).join('') || '<div class="empty">No story beats.</div>'}
    </div>
  </section>`;
}

function renderNextQueueBlock(title='Next Analyses Queue') {
  const queue = TIMELINE_MODE ? (DATA.timeline_next_experiment_queue || []) : (DATA.next_experiment_queue || []);
  return `<div class="panel">
    <h2>${esc(title)}</h2>
    <p class="muted">Accumulated from each visible valid research cycle's next analysis field, in cycle order. This queue keeps growing as new marathon cycles are persisted.</p>
    <ul class="queue-list">
      ${queue.map(item => `<li>
        <span class="queue-meta">${esc(item.cycle_id)} · ${esc(item.engine || 'engine?')} · ${esc(item.attempt || 'attempt?')}${item.queue_source === 'gedanken' ? ` · ${esc(item.packet_id || '')}` : ''}${item.queue_source === 'decisive_next_move' ? ' · decisive validation packet' : ''}${item.queue_source === 'paper_argument_priority' ? ` · paper argument task · ${esc(item.paper_task_subtype || '')}` : ''}${item.queue_source === 'proof_delivery_priority' ? ` · proof delivery · ${esc(item.queue_id || '')}` : ''}</span>
        ${item.queue_source === 'proof_delivery_priority' && item.branch_title ? `<strong>${esc(item.branch_title)}</strong><br>` : ''}
        ${item.queue_source === 'proof_delivery_priority' && item.source_anchor ? `<span class="queue-meta">Source: ${esc(item.source_anchor)}${item.proof_status ? ` · ${esc(item.proof_status)}` : ''}</span>` : ''}
        ${rich(item.next_experiment_html, item.next_experiment)}
        ${item.validation_steps?.length ? `<ol class="compact-list">${item.validation_steps.map((step, idx) => `<li>${rich((item.validation_steps_html || [])[idx], step)}</li>`).join('')}</ol>` : ''}
      </li>`).join('')}
    </ul>
  </div>`;
}

function renderNextQueue() {
  return `<section class="section active">${renderNextQueueBlock()}</section>`;
}

function renderRankedQueue() {
  const queue = TIMELINE_MODE ? (DATA.timeline_ranked_next_experiment_queue || []) : (DATA.ranked_next_experiment_queue || []);
  return `<section class="section active">
    <div class="panel">
      <h2>Current Ranked Next-Analysis Queue</h2>
      <p class="muted">Ordered by target payoff, discriminating power, execution readiness, target integration, and anti-drift pressure. The score is a control signal for the next run, not a theorem-progress claim.</p>
      ${queue.map(item => `<div class="card story">
        <div class="row">
          <h3>#${esc(item.rank)} · ${esc(item.cycle_id)} · ${esc(item.branch_title || 'branch?')}</h3>
          ${pill(item.priority_band || 'priority?', item.priority_band === 'high' ? 'good' : item.priority_band === 'medium' ? 'info' : 'warn')}
          ${pill(item.engine || 'engine?', 'info')}
          ${pill(item.attempt || 'attempt?')}
        </div>
        <div class="rank-score"><strong>${esc(item.priority_score)}</strong><div class="bar"><span style="width:${Math.max(4, Math.min(100, Number(item.priority_score || 0)))}%"></span></div></div>
        <p><strong>Analysis:</strong> ${rich(item.next_experiment_html, item.next_experiment)}</p>
        ${item.queue_source === 'proof_delivery_priority' ? `<p><strong>Source anchor:</strong> ${esc(item.source_anchor || '')}</p><p><strong>Proof status:</strong> ${esc(item.proof_status || '')}</p>` : ''}
        ${(item.queue_source === 'decisive_next_move' || item.queue_source === 'paper_argument_priority' || item.queue_source === 'proof_delivery_priority') ? `<p><strong>Source object:</strong> ${rich(item.source_object_html, item.source_object || '')}</p><p><strong>Target object:</strong> ${rich(item.target_object_html, item.target_object || '')}</p><p><strong>Transfer condition:</strong> ${rich(item.transfer_condition_html, item.transfer_condition || '')}</p>` : ''}
        ${item.queue_source === 'proof_delivery_priority' && item.theorem_goal ? `<p><strong>Theorem goal:</strong> ${rich(item.theorem_goal_html, item.theorem_goal || '')}</p>` : ''}
        ${item.queue_source === 'gedanken' ? `<p><strong>Gedanken packet:</strong> ${esc(item.packet_id || '')} · ${esc(item.situation_title || '')} · transfer: ${esc(item.transfer_verdict || '')}</p><p><strong>Success:</strong> ${esc(item.success_criterion || '')}</p><p><strong>Demotion:</strong> ${esc(item.failure_or_demotion_criterion || '')}</p>` : ''}
        ${item.validation_steps?.length ? `<p><strong>Decisive validation steps:</strong></p><ol class="payoff-list">${item.validation_steps.map((step, idx) => `<li>${rich((item.validation_steps_html || [])[idx], step)}</li>`).join('')}</ol>` : ''}
        <p><strong>Why this is a good target:</strong> ${esc(item.why_target)}</p>
        <p><strong>Risk:</strong> ${esc(item.risk)}</p>
        <p><strong>Branch control:</strong> ${pill(item.branch_continuation_decision || 'decision?', item.branch_continuation_decision === 'continue_run_next' ? 'good' : item.branch_continuation_decision === 'stop_candidate_after_repeat_low_payoff' ? 'fail' : 'warn')} ${esc(item.branch_continuation_reason || '')}</p>
        <p><strong>Premature-stop guard:</strong> ${rich(item.premature_stop_guard_html, item.premature_stop_guard || '')}</p>
        <p><strong>Do not stop if:</strong></p>
        <ul class="payoff-list">${(item.do_not_stop_if || []).map((rule, idx) => `<li>${rich((item.do_not_stop_if_html || [])[idx], rule)}</li>`).join('')}</ul>
        <p><strong>Payoff criteria:</strong></p>
        <ul class="payoff-list">${(item.payoff_criteria || []).map(criterion => `<li>${rich(criterion.html, criterion.text)}</li>`).join('')}</ul>
        <p><strong>Stop criteria:</strong></p>
        <ul class="payoff-list">${(item.stop_criteria || []).map((criterion, idx) => `<li>${rich((item.stop_criteria_html || [])[idx], criterion)}</li>`).join('')}</ul>
        <p><strong>Required skills:</strong> ${(item.required_skills || []).map(skill => pill(skill, 'info')).join('')}</p>
      </div>`).join('') || '<div class="empty">No ranked next analyses.</div>'}
    </div>
  </section>`;
}

function nodeMap(nodes) {
  return Object.fromEntries((nodes || []).map(node => [node.id, node]));
}

function nodeName(nodesById, id) {
  const node = nodesById[id] || {};
  return node.label || String(id || '').replace(/^(var|reg)\./, '').replace(/[_-]/g, ' ');
}

function regimeNames(nodesById, ids) {
  return (ids || []).map(id => nodeName(nodesById, id)).filter(Boolean);
}

function relationTitle(edge, nodesById) {
  const source = nodeName(nodesById, edge.source);
  const target = nodeName(nodesById, edge.target);
  const verb = {
    enables: 'enables',
    constrains: 'constrains',
    falsifies: 'can falsify',
    induces: 'induces',
    decreases: 'decreases',
  }[edge.edge_type] || 'relates to';
  return `${source} ${verb} ${target}`;
}

function whyRelationMatters(edge) {
  const type = edge.edge_type || '';
  const text = lower(`${edge.direction || ''} ${edge.qualitative_behavior || ''}`);
  if (type === 'falsifies') return 'This is a branch-control relation: if the condition appears in the same theory, the route must backtrack or be quarantined.';
  if (type === 'constrains') return 'This is a discipline relation: it says which side conditions must hold before a formula can be trusted.';
  if (type === 'induces') return 'This turns finite algebra into analytic work: formulas become concrete estimates or transfer obligations.';
  if (type === 'decreases' && text.includes('spectral')) return 'This connects observable decay to the spectral story, so it matters only after reconstruction and density are controlled.';
  if (type === 'decreases') return 'This is a qualitative response relation: increasing one quantity suppresses the other in the stated regime.';
  if (type === 'enables') return 'This is a mechanism-opening relation: it names a variable that can reveal whether the proposed bridge is real or fragile.';
  return 'This relation is kept because it changes what the next analysis should test.';
}

function renderMechanismStep(title, body, status='') {
  return `<div class="mechanism-step"><strong>${esc(title)}</strong><p>${body}</p>${status ? `<p class="muted">${esc(status)}</p>` : ''}</div>`;
}

function renderFriendlyNode(node) {
  return `<div class="card graph-node">
    <div class="row"><h3>${esc(node.label || node.id)}</h3>${pill(node.node_type || 'node', 'info')}${pill(node.epistemic_status || 'status?')}</div>
    <p>${esc(node.description || '')}</p>
  </div>`;
}

function renderFriendlyRelation(edge, nodesById) {
  const regimes = regimeNames(nodesById, edge.validity_regime);
  const failureModes = (edge.failure_modes || []).slice(0, 2);
  const assumptions = (edge.assumptions || []).slice(0, 2);
  return `<article class="relation-card ${esc(edge.edge_type || '')}">
    <span class="relation-label">${esc(edge.edge_type || 'relation')}</span>
    <span class="relation-title">${esc(relationTitle(edge, nodesById))}</span>
    <p>${rich(edge.qualitative_behavior_html, edge.qualitative_behavior || edge.direction || '')}</p>
    <p><strong>Why it matters:</strong> ${esc(whyRelationMatters(edge))}</p>
    ${regimes.length ? `<p><strong>Valid in:</strong> ${regimes.map(item => pill(item, 'info')).join('')}</p>` : ''}
    ${assumptions.length ? `<p><strong>Trust it when:</strong></p><ul class="compact-list">${assumptions.map(item => `<li>${esc(item)}</li>`).join('')}</ul>` : ''}
    ${failureModes.length ? `<p><strong>What would break it:</strong></p><ul class="compact-list">${failureModes.map(item => `<li>${esc(item)}</li>`).join('')}</ul>` : ''}
    ${(edge.originating_cycle_ids || []).length ? `<details><summary>Audit trail</summary><p class="muted">Learned or reinforced across ${(edge.originating_cycle_ids || []).length} cycle(s): ${(edge.originating_cycle_ids || []).slice(-4).map(id => pill(id, 'info')).join('')}</p></details>` : ''}
  </article>`;
}

function renderQualitative() {
  const graph = DATA.qualitative_mechanistic_graph || {};
  const nodes = graph.nodes || [];
  const edges = graph.edges || [];
  const summary = graph.summary || {};
  const nodesById = nodeMap(nodes);
  const regimes = nodes.filter(node => node.node_type === 'regime');
  const quantities = nodes.filter(node => node.node_type !== 'regime');
  const falsifiers = edges.filter(edge => edge.edge_type === 'falsifies');
  const controls = edges.filter(edge => ['constrains', 'induces', 'enables'].includes(edge.edge_type));
  const responses = edges.filter(edge => edge.edge_type === 'decreases');
  return `<section class="section active">
    <div class="panel">
      <h2>Qualitative Mechanistic Graph</h2>
      <div class="graph-brief">
        <div class="graph-hero">
          <h3>What This Graph Is Saying</h3>
          <p>The current qualitative picture is not a directory of variables. It says where the Yang-Mills route can genuinely move: finite reflected Wilson data must survive collar collapse, obey exact quotient side conditions, avoid phase or determinant obstructions, and then become uniform continuum estimates before it can support the spectral story.</p>
          <p>The useful question is therefore simple: which relation changes the next mathematical action?</p>
        </div>
        <div class="quality">
          ${qualityChip('Active relations', summary.edge_count || edges.length)}
          ${qualityChip('Quantities and regimes', summary.node_count || nodes.length)}
          ${qualityChip('Falsifier relations', falsifiers.length)}
          ${qualityChip('Source cycles', (graph.source_cycle_ids || []).length)}
        </div>
      </div>
      <h2>Mechanism In Plain Terms</h2>
      <div class="mechanism-flow">
        ${renderMechanismStep('1. Regulated positivity', 'At fixed cutoff and volume, reflection positivity gives finite Gram matrices. This is useful only if the limiting topology preserves positivity.')}
        ${renderMechanismStep('2. Collar collapse', 'When Wilson collars approach the reflection plane, boundary factors can introduce quotient phases and determinant obstructions. Pairwise positivity is not enough.')}
        ${renderMechanismStep('3. Exact finite tests', 'The quotient matrix, holonomy, minors, and side-condition ledger tell us whether the finite family is even eligible for analytic promotion.')}
        ${renderMechanismStep('4. Analytic transfer', 'Finite formulas become Yang-Mills obligations: boundary OPE control, contact terms, nonzero denominators, modulus positivity, and same-theory realization.')}
        ${renderMechanismStep('5. Spectral readout', 'Euclidean decay can speak about a mass gap only after OS reconstruction and observable-density control.')}
      </div>
      <h2>Relations That Matter Now</h2>
      <div class="relation-board">
        ${controls.map(edge => renderFriendlyRelation(edge, nodesById)).join('')}
        ${falsifiers.map(edge => renderFriendlyRelation(edge, nodesById)).join('')}
        ${responses.map(edge => renderFriendlyRelation(edge, nodesById)).join('')}
      </div>
      <h2>What The User Should Watch</h2>
      <div class="relation-list">
        <div class="card story">
          <h3>Control Knobs</h3>
          <p>These are the quantities we can vary or compute to learn something real.</p>
          <ul class="compact-list">${quantities.filter(node => ['scale', 'variable', 'observable', 'symbolic_carrier'].includes(node.node_type)).slice(0, 8).map(node => `<li><strong>${esc(node.label || node.id)}:</strong> ${esc(node.description || '')}</li>`).join('')}</ul>
        </div>
        <div class="card story">
          <h3>Regime Boundaries</h3>
          <p>These are the places where a true statement can become a false proof if transferred too casually.</p>
          <ul class="compact-list">${regimes.map(node => `<li><strong>${esc(node.label || node.id)}:</strong> ${esc(node.description || '')}</li>`).join('')}</ul>
        </div>
        <div class="card story">
          <h3>Current Decision Use</h3>
          <p>The graph should decide branch control. A determinant, phase holonomy, contact term, or non-uniform limit is not metadata; it tells us whether to continue, backtrack, or quarantine the route.</p>
        </div>
      </div>
    </div>
  </section>`;
}

function renderGedanken() {
  const packets = DATA.gedanken_experiments?.packets || [];
  return `<section class="section active">
    <div class="panel">
      <h2>Gedanken Experiments</h2>
      <p class="muted">Concrete imagined situations used only when they can isolate a mechanism, expose a hidden assumption, or create a follow-up task. These packets are conceptual probes, not proof progress.</p>
      ${packets.map(packet => `<div class="card story">
        <div class="row">
          <h3>${esc(packet.situation?.title || packet.packet_id)}</h3>
          ${pill(packet.need_decision || 'decision?', 'info')}
          ${pill(packet.epistemic_status || 'status?')}
        </div>
        <p><strong>Purpose:</strong> ${esc(packet.situation?.purpose || '')}</p>
        <p><strong>Minimal world:</strong> ${esc(packet.situation?.minimal_world || '')}</p>
        <p><strong>Carrier:</strong> ${esc(packet.situation?.mathematical_carrier || '')}</p>
        <p><strong>Why informative:</strong> ${esc(packet.situation?.why_this_situation_is_informative || '')}</p>
        <p><strong>Transfer scope:</strong> ${esc(packet.transfer_scope?.transfers || '')}</p>
        <p><strong>Does not transfer:</strong> ${esc(packet.transfer_scope?.does_not_transfer || '')}</p>
        <details>
          <summary>Interventions, observations, variants, and follow-up</summary>
          <p><strong>Trigger criteria:</strong></p>
          <ul>${(packet.trigger_criteria || []).map(item => `<li>${esc(item)}</li>`).join('')}</ul>
          <p><strong>Expected observations:</strong></p>
          <ul>${(packet.expected_observations || []).map(obs => `<li><strong>${esc(obs.observable || obs.id)}:</strong> ${esc(obs.expected_pattern || '')} ${esc(obs.what_it_would_teach || '')}</li>`).join('')}</ul>
          <p><strong>Variants:</strong></p>
          <ul>${(packet.variants || []).map(v => `<li><strong>${esc(v.id)}:</strong> ${esc(v.changed_condition)} -> ${esc(v.predicted_change)}</li>`).join('')}</ul>
          <p><strong>Follow-up tasks:</strong></p>
          <ul>${(packet.followup_cycle_tasks || []).map(task => `<li><strong>${esc(task.action)}:</strong> ${esc(task.description)} ${(task.required_skills || []).map(skill => pill(skill, 'info')).join('')}</li>`).join('')}</ul>
        </details>
      </div>`).join('') || '<div class="empty">No Gedanken experiment packets generated yet.</div>'}
    </div>
  </section>`;
}

function renderParsimoniousProbes() {
  const layer = DATA.parsimonious_probe_layer || {};
  const symbolic = layer.symbolic_matrix_probe || {};
  const finite = layer.finite_algebra_interfaces || {};
  const packet = (finite.packets || [])[0] || {};
  const obligations = layer.analytic_estimate_obligations || {};
  const numeric = layer.bounded_numeric_probe || {};
  return `<section class="section active">
    <div class="panel">
      <h2>Parsimonious Probe Control</h2>
      <p class="muted">Symbolic-first computation control for qualitative physics reasoning. This tab separates exact finite algebra, analytic estimate obligations, and rare bounded numeric calibration.</p>
      <div class="quality">
        ${qualityChip('Symbolic formulas', symbolic.identities?.length || 0)}
        ${qualityChip('Finite interfaces', finite.summary?.packet_count || 0)}
        ${qualityChip('Falsifier shapes', finite.summary?.falsifier_template_count || 0)}
        ${qualityChip('Analytic obligations', obligations.obligations?.length || 0)}
        ${qualityChip('Bounded numeric status', numeric.status || 'not run')}
        ${qualityChip('Proof-safe', layer.proof_safe ? 'yes' : 'no')}
      </div>
      <h2>Finite Algebra Interface Packet</h2>
      ${packet.packet_id ? `<div class="card">
        <div class="row"><h3>${esc(packet.carrier?.name || packet.packet_id)}</h3>${pill(packet.epistemic_status || 'equational_interface','info')}</div>
        <p><strong>Boundary:</strong> ${esc(packet.carrier?.validity_boundary || '')}</p>
        <p><strong>Side conditions:</strong></p>
        <ul>${(packet.side_conditions || []).map(item => `<li><strong>${esc(item.id)}:</strong> ${esc(item.condition)} · ${esc(item.why_needed)}</li>`).join('')}</ul>
        <p><strong>Falsifier shapes:</strong></p>
        <ul>${(packet.falsifier_templates || []).map(item => `<li><strong>${esc(item.id)}:</strong> ${esc(item.disconfirming_observation)} -> ${esc(item.branch_control_effect)}</li>`).join('')}</ul>
      </div>` : '<div class="empty">No finite algebra interface packet generated.</div>'}
      <h2>Exact Symbolic Interfaces</h2>
      ${(symbolic.identities || []).map(identity => `<div class="card">
        <div class="row"><h3>${esc(identity.name || identity.id)}</h3>${pill(identity.epistemic_status || 'symbolic_formula','info')}${pill(symbolic.symbolic_backend || 'backend?')}</div>
        <div class="equation">\\[${tex(identity.latex || '')}\\]</div>
        <p><strong>Valid when:</strong> ${esc(identity.valid_when || '')}</p>
      </div>`).join('') || '<div class="empty">No symbolic matrix probe generated.</div>'}
      <h2>Formula-Derived Analytic Obligations</h2>
      ${(obligations.next_experiment_queue_items || []).map(item => `<div class="card story">
        <div class="row"><h3>${esc(item.next_experiment || item.source_obligation_id)}</h3>${pill(item.epistemic_status || 'analytic_obligation','info')}${pill(`priority ${item.priority_score || '?'}`,'good')}</div>
        <p><strong>Payoff criteria:</strong></p>
        <ul>${(item.payoff_criteria || []).map(criterion => `<li>${esc(criterion)}</li>`).join('')}</ul>
        <p><strong>Skills:</strong> ${(item.required_skills || []).map(skill => pill(skill, 'info')).join('')}</p>
      </div>`).join('') || '<div class="empty">No analytic obligations generated.</div>'}
      <h2>Bounded Numeric Probe</h2>
      ${numeric.probe ? `<div class="card ${numeric.status === 'falsifier_candidate' ? 'fail' : 'review'}">
        <div class="row"><h3>${esc(numeric.probe.probe_kind || 'bounded probe')}</h3>${pill(numeric.status || 'status?', numeric.status === 'falsifier_candidate' ? 'warn' : 'info')}</div>
        <p><strong>Domain:</strong> ${esc((numeric.probe.bounded_domain || []).join('; '))}</p>
        <p><strong>Stopping:</strong> ${esc(numeric.probe.stopping_condition || '')}</p>
        <p><strong>Lesson:</strong> ${esc(numeric.probe.result?.qualitative_lesson || '')}</p>
        <p><strong>Boundary:</strong> ${esc(numeric.transfer_boundary || '')}</p>
      </div>` : '<div class="empty">No bounded numeric probe has been run; this is acceptable when symbolic and analytic routes suffice.</div>'}
    </div>
  </section>`;
}

function scoreMetric(label, value) {
  return `<div class="metric"><strong>${esc(value)}</strong><span>${esc(label)}</span></div>`;
}

function renderContributionCandidate(candidate) {
  const scores = candidate.scores || {};
  const gates = candidate.handoff_hard_gates || {};
  const prior = candidate.prior_art_boundary || {};
  const relevance = candidate.good_enough_paper_relevance || {};
  const relevanceMarkers = candidate.paper_relevance_markers || [];
  return `<article class="card story">
    <div class="row">
      <h3>${esc(candidate.candidate_id || candidate.branch_title || 'candidate')}</h3>
      ${pill(candidate.stepping_stone_maturity || candidate.status || 'maturity?', candidate.stepping_stone_maturity === 'publishable_handoff_ready' ? 'good' : candidate.stepping_stone_maturity === 'near_stepping_stone' ? 'info' : 'warn')}
      ${pill(candidate.contribution_type || 'type?','info')}
      ${pill(`explore ${candidate.exploration_payoff_score || candidate.score || 0}`, (candidate.exploration_payoff_score || candidate.score || 0) >= 74 ? 'good' : 'info')}
      ${pill(`publishable ${candidate.publishable_subgoal_score || 0}`, candidate.publishable_subgoal_score >= 80 ? 'good' : candidate.publishable_subgoal_score >= 55 ? 'info' : 'warn')}
      ${pill(relevance.status || 'paper relevance?', relevance.status === 'paper_relevance_ready' ? 'good' : relevance.status === 'strong_relevance_certification_pending' ? 'info' : 'warn')}
    </div>
    <p><strong>${esc(candidate.cycle_id || '')} · ${esc(candidate.branch_title || '')}</strong></p>
    <p><strong>Smallest honest claim:</strong> ${rich(candidate.smallest_honest_claim_html, candidate.smallest_honest_claim || '')}</p>
    <p><strong>Why it can stand alone:</strong> ${rich(candidate.why_it_could_stand_alone_html, candidate.why_it_could_stand_alone || '')}</p>
    <div class="quality">
      ${scoreMetric('Conceptual novelty', scores.conceptual_novelty || 0)}
      ${scoreMetric('Explanatory power', scores.explanatory_power || 0)}
      ${scoreMetric('Implications', scores.implications || 0)}
      ${scoreMetric('Certification readiness', scores.certification_readiness || 0)}
      ${scoreMetric('Target relevance', scores.target_relevance || 0)}
      ${scoreMetric('Paper relevance avg', relevance.average_marker_score || 0)}
      ${scoreMetric('Infinite progression risk', candidate.infinite_progression_risk || 'unknown')}
    </div>
    <p><strong>Good enough paper relevance:</strong> ${esc(relevance.paper_relevance_decision || '')}</p>
    <p><strong>Missing to good-enough paper:</strong></p>
    ${listMaybeRich(candidate.missing_to_good_enough_paper || [])}
    <div class="quality">
      ${relevanceMarkers.map(marker => scoreMetric((marker.dimension || '').replaceAll('_', ' '), `${marker.score || 0} · ${marker.status || 'unknown'}`)).join('')}
    </div>
    <p><strong>Why this budget now:</strong> ${esc(candidate.why_this_budget_now || '')}</p>
    <p><strong>Missing to publishable:</strong></p>
    ${listMaybeRich(candidate.missing_to_publishable || [])}
    <div class="quality">
      ${Object.entries(gates).map(([gate, packet]) => scoreMetric(gate.replaceAll('_', ' '), packet.ready ? 'ready' : packet.finite_task ? 'finite task' : 'missing')).join('')}
    </div>
    <p><strong>Branch control:</strong> ${pill(candidate.branch_control_decision || 'decision?', candidate.branch_control_decision === 'handoff' ? 'good' : candidate.branch_control_decision?.includes('stop') ? 'fail' : 'info')} ${rich(candidate.branch_control_reason_html, candidate.branch_control_reason || '')}</p>
    <p><strong>Good enough when:</strong></p>
    ${listMaybeRich(candidate.good_enough_when || [], candidate.good_enough_when_html || [])}
    <p><strong>Continue only if:</strong></p>
    ${listMaybeRich(candidate.continue_only_if || [], candidate.continue_only_if_html || [])}
    <p><strong>Stop when:</strong></p>
    ${listMaybeRich(candidate.stop_when || [], candidate.stop_when_html || [])}
    <details>
      <summary>Evidence, validation burden, and paper implication</summary>
      <p><strong>Evidence basis:</strong> ${(candidate.evidence_basis || []).map(item => pill(item, 'info')).join('')}</p>
      <p><strong>Validation burden:</strong></p>
      ${listMaybeRich(candidate.validation_burden || [], candidate.validation_burden_html || [])}
      <p><strong>Disqualifiers:</strong></p>
      <ul class="payoff-list">${(candidate.disqualifier_tests || []).map(row => `<li><strong>${esc(row.name || '')}:</strong> ${pill(row.verdict || 'unknown', row.verdict === 'pass' ? 'good' : row.verdict === 'fail' ? 'fail' : 'warn')} ${esc(row.evidence || '')}</li>`).join('')}</ul>
      <p><strong>Paper relevance markers:</strong></p>
      <ul class="payoff-list">${relevanceMarkers.map(marker => `<li><strong>${esc((marker.dimension || '').replaceAll('_', ' '))}:</strong> ${pill(`${marker.score || 0} · ${marker.status || 'unknown'}`, marker.status === 'paper_ready' || marker.status === 'strong' ? 'good' : marker.status === 'adequate' ? 'info' : 'warn')} ${esc(marker.criterion || '')}${marker.missing_for_good_enough ? `<br><span class="muted">Missing: ${esc(marker.missing_for_good_enough)}</span>` : ''}</li>`).join('')}</ul>
      <p><strong>Prior-art boundary:</strong> ${pill(prior.novelty_status || 'unknown', prior.novelty_status === 'checked' ? 'good' : 'warn')}</p>
      <ul class="payoff-list">${(prior.citation_tasks || []).map(item => `<li>${esc(item)}</li>`).join('')}</ul>
      <p><strong>Paper note shape:</strong> ${esc(candidate.paper_note_shape?.title || '')}</p>
      <p>${rich(candidate.paper_note_shape?.abstract_claim_html, candidate.paper_note_shape?.abstract_claim || '')}</p>
      <p><strong>Immediate next analysis:</strong> ${rich(candidate.implication_map?.immediate_next_analysis_html, candidate.implication_map?.immediate_next_analysis || '')}</p>
      <p><strong>Route-level implication:</strong> ${rich(candidate.implication_map?.route_level_html, candidate.implication_map?.route_level || '')}</p>
      <p><strong>Paper-level implication:</strong> ${rich(candidate.implication_map?.paper_level_html, candidate.implication_map?.paper_level || '')}</p>
      <p><strong>Overclaim boundary:</strong> ${rich(candidate.overclaim_boundary_html, candidate.overclaim_boundary || '')}</p>
      <p><strong>Required skills:</strong> ${(candidate.required_skills || []).map(skill => pill(skill, 'info')).join('')}</p>
    </details>
  </article>`;
}

function renderContributions() {
  const monitor = DATA.scientific_contribution_monitor || {};
  const metrics = monitor.metrics || {};
  const candidates = monitor.candidates || [];
  const top = monitor.top_candidate || {};
  return `<section class="section active">
    <div class="panel">
      <h2>Scientific Contribution Monitor</h2>
      <p class="muted">This tab keeps the marathon aimed at independently valuable subgoals. It asks whether a branch is producing a publishable bridge, obstruction, probe, method, reframing, or evidence packet, and it also decides when the branch is good enough to hand off instead of continuing indefinitely.</p>
      <div class="quality">
        ${scoreMetric('Aim status', monitor.contribution_aim_status || 'not generated')}
        ${scoreMetric('Active candidates', metrics.active_candidate_count || 0)}
        ${scoreMetric('Contribution-shaped', metrics.contribution_shaped_count || 0)}
        ${scoreMetric('Near stepping stone', metrics.near_stepping_stone_count || 0)}
        ${scoreMetric('Publishable handoff', metrics.publishable_handoff_count || 0)}
        ${scoreMetric('Average exploration score', metrics.average_contribution_score || 0)}
        ${scoreMetric('Average publishable score', metrics.average_publishable_subgoal_score || 0)}
        ${scoreMetric('Average paper relevance', metrics.average_paper_relevance_marker_score || 0)}
        ${scoreMetric('Strong paper relevance', metrics.strong_paper_relevance_candidate_count || 0)}
        ${scoreMetric('Paper relevance ready', metrics.paper_relevance_ready_count || 0)}
        ${scoreMetric('Infinite-risk branches', metrics.infinite_progression_risk_count || 0)}
      </div>
      <div class="card story">
        <h3>Standing Objective</h3>
        <p>${esc(monitor.loop_policy?.standing_objective || '')}</p>
        <h3>Good Enough</h3>
        <p>${esc(monitor.loop_policy?.good_enough_definition || '')}</p>
        <h3>Good Enough Paper Relevance</h3>
        <p>${esc(monitor.loop_policy?.good_enough_paper_relevance_definition || '')}</p>
        <h3>Paper Relevance Markers</h3>
        <ul class="payoff-list">${Object.entries(monitor.loop_policy?.paper_relevance_marker_criteria || {}).map(([key, value]) => `<li><strong>${esc(key.replaceAll('_', ' '))}:</strong> ${esc(value)}</li>`).join('')}</ul>
        <h3>Maturity Levels</h3>
        <ul class="payoff-list">${Object.entries(monitor.loop_policy?.stepping_stone_maturity_levels || {}).map(([key, value]) => `<li><strong>${esc(key)}:</strong> ${esc(value)}</li>`).join('')}</ul>
        <h3>Anti-Infinite Progression Rule</h3>
        <p>${esc(monitor.loop_policy?.anti_infinite_progression_rule || '')}</p>
        <h3>Next Contribution Objective</h3>
        <p>${esc(monitor.next_contribution_objective || '')}</p>
        <h3>Validation Gap</h3>
        <p>${esc(monitor.validation_gap || '')}</p>
      </div>
      ${top.candidate_id ? `<h2>Best Current Candidate</h2>${renderContributionCandidate(top)}` : ''}
      <h2>Contribution Candidate Queue</h2>
      ${candidates.map(renderContributionCandidate).join('') || '<div class="empty">No contribution monitor generated yet.</div>'}
    </div>
  </section>`;
}

function refById(report) {
  return Object.fromEntries((report.references || []).map(ref => [ref.ref_id, ref]));
}

function refLink(ref) {
  if (!ref) return '';
  return `<a href="${esc(ref.url || '#')}" target="_blank" rel="noreferrer">${esc(ref.ref_id || ref.title || 'ref')}</a>`;
}

function renderProblemLiterature() {
  const report = DATA.target_literature_evolution || {};
  const refs = refById(report);
  const statement = report.problem_statement || {};
  return `<section class="section active">
    <div class="panel">
      <h2>Target Problem And Literature Evolution</h2>
      <div class="graph-brief">
        <div class="graph-hero">
          <h3>${esc(report.problem_name || 'Active target')}</h3>
          <p>${esc(statement.accessible || '')}</p>
          ${statement.formal_shape ? `<div class="equation">\\[${tex(statement.formal_shape)}\\]</div>` : ''}
          ${statement.source_ref_id ? `<p class="muted">Canonical statement: ${refLink(refs[statement.source_ref_id])}</p>` : ''}
        </div>
        <div class="quality">
          ${qualityChip('Literature stages', (report.literature_stages || []).length)}
          ${qualityChip('Cited references', (report.references || []).length)}
          ${qualityChip('Open obligations', (report.open_obligations || []).length)}
          ${qualityChip('Required skills', (report.required_skills || []).length)}
        </div>
      </div>
      <h2>Why This Problem Matters</h2>
      <div class="relation-list">
        ${(report.why_it_matters || []).map(item => `<div class="card story"><p>${esc(item)}</p></div>`).join('')}
      </div>
      ${report.why_difficult ? `<h2>Why This Is Difficult</h2>
      <div class="card story">
        <p>${esc(report.why_difficult.overview || '')}</p>
        ${report.why_difficult.core_tension ? `<p><strong>Core tension:</strong> ${esc(report.why_difficult.core_tension)}</p>` : ''}
      </div>
      <div class="relation-board">
        ${(report.why_difficult.facets || []).map(facet => `<article class="relation-card">
          <span class="relation-label">${esc(facet.lens || 'difficulty lens')}</span>
          <span class="relation-title">${esc(facet.claim || '')}</span>
          <p><strong>Pressure:</strong> ${esc(facet.pressure || '')}</p>
          <p><strong>Workflow consequence:</strong> ${esc(facet.workflow_consequence || '')}</p>
        </article>`).join('')}
      </div>
      ${(report.why_difficult.common_false_shortcuts || []).length ? `<h3>False Shortcuts To Avoid</h3>
      <ul class="payoff-list">${(report.why_difficult.common_false_shortcuts || []).map(item => `<li>${esc(item)}</li>`).join('')}</ul>` : ''}` : ''}
      <h2>What Would Count As A Solution</h2>
      <ul class="payoff-list">${(report.solution_criteria || []).map(item => `<li>${esc(item)}</li>`).join('')}</ul>
      <h2>How The Literature Evolved</h2>
      <div class="timeline">
        ${(report.literature_stages || []).map(stage => `<article class="card story">
          <div class="row"><h3>${esc(stage.period)} · ${esc(stage.title)}</h3>${(stage.refs || []).map(refId => refLink(refs[refId])).join('')}</div>
          <p><strong>Conceptual shift:</strong> ${esc(stage.core_shift || '')}</p>
          <p><strong>What became possible:</strong> ${esc(stage.what_became_possible || '')}</p>
          <p><strong>What remained open:</strong> ${esc(stage.what_remained_open || '')}</p>
        </article>`).join('')}
      </div>
      <h2>What The Literature Teaches The Workflow</h2>
      ${(report.workflow_implications || []).map(item => `<div class="card review">
        <p><strong>Lesson:</strong> ${esc(item.lesson || '')}</p>
        <p><strong>Workflow effect:</strong> ${esc(item.active_workflow_effect || '')}</p>
        <p><strong>Refs:</strong> ${(item.refs || []).map(refId => refLink(refs[refId])).join('')}</p>
      </div>`).join('')}
      <h2>Open Obligations Still Alive</h2>
      <ul class="payoff-list">${(report.open_obligations || []).map(item => `<li>${esc(item)}</li>`).join('')}</ul>
      <h2>References</h2>
      <div class="relation-board">
        ${(report.references || []).map(ref => `<article class="relation-card">
          <span class="relation-label">${esc(ref.role || '')} · ${esc(ref.status || '')}</span>
          <span class="relation-title">${esc(ref.authors || '')} (${esc(ref.year || '')})</span>
          <p><a href="${esc(ref.url || '#')}" target="_blank" rel="noreferrer">${esc(ref.title || '')}</a></p>
          <p><strong>Supports:</strong> ${esc(ref.supports || '')}</p>
          <p><strong>Limit:</strong> ${esc(ref.limitation || '')}</p>
        </article>`).join('')}
      </div>
      <h2>Skills To Apply</h2>
      <p>${(report.required_skills || []).map(skill => pill(skill, 'info')).join('')}</p>
    </div>
  </section>`;
}

function renderMacroStrategyCard(strategy) {
  return `<article class="card story">
    <div class="row">
      <h3>${esc(strategy.rank || '')}. ${esc(strategy.title || '')}</h3>
      ${pill(strategy.route_family || 'route family?', 'info')}
      ${pill(`score ${strategy.priority_score || 0}`, strategy.priority_score >= 75 ? 'good' : 'info')}
      ${pill(strategy.epistemic_status || 'status?')}
    </div>
    <p><strong>Macro thesis:</strong> ${esc(strategy.macro_thesis || '')}</p>
    <p><strong>Physics picture:</strong> ${esc(strategy.physics_picture || '')}</p>
    <p><strong>Why now:</strong> ${esc(strategy.why_now || '')}</p>
    <details open>
      <summary>Computation, success, and pivot criteria</summary>
      <p><strong>What to compute next:</strong></p>
      <ul class="payoff-list">${(strategy.what_to_compute_next || []).map(item => `<li>${esc(item)}</li>`).join('')}</ul>
      <p><strong>Success condition:</strong></p>
      <ul class="payoff-list">${(strategy.success_condition || []).map(item => `<li>${esc(item)}</li>`).join('')}</ul>
      <p><strong>Failure or pivot condition:</strong></p>
      <ul class="payoff-list">${(strategy.failure_or_pivot_condition || []).map(item => `<li>${esc(item)}</li>`).join('')}</ul>
    </details>
    <details>
      <summary>Story evidence and skills</summary>
      ${(strategy.evidence_from_story || []).map(row => `<div class="card">
        <div class="row">${pill(row.cycle_id || 'cycle?', 'info')}<strong>${esc(row.branch_title || '')}</strong></div>
        <p>${esc(row.learning || '')}</p>
        <p><strong>Next:</strong> ${esc(row.next_experiment || '')}</p>
      </div>`).join('')}
      <p><strong>Literature refs:</strong> ${(strategy.linked_literature_refs || []).map(ref => pill(ref, 'info')).join('')}</p>
      <p><strong>Active skills:</strong> ${(strategy.active_skills || []).map(skill => pill(skill, 'info')).join('')}</p>
    </details>
  </article>`;
}

function renderPhysicsMathStrategy() {
  const report = DATA.physics_math_interpretation || {};
  const synthesis = report.cross_route_synthesis || {};
  const routes = report.interpretations || [];
  return `<section class="section active">
    <div class="panel">
      <h2>Physics & Maths Strategy</h2>
      <p class="muted">Top-level interpretation of the active routes in physics and mathematical terms. This is the strategic lens before the detailed timeline: what the physics picture is, which mathematical objects carry it, and what bridge must be proved next.</p>
      <div class="graph-brief">
        <div class="graph-hero">
          <h3>Cross-Route Synthesis</h3>
          <p><strong>Constructive spine:</strong> ${esc(synthesis.constructive_spine || '')}</p>
          <p><strong>Missing joint step:</strong> ${esc(synthesis.missing_joint_step || '')}</p>
        </div>
        <div class="quality">
          ${qualityChip('Active routes', report.active_route_count || routes.length || 0)}
          ${qualityChip('Mode', report.interpretation_mode || 'not generated')}
          ${qualityChip('Scope', report.scope_boundary || 'strategy interpretation')}
        </div>
      </div>
      <h2>Next Mathematical-Physics Focus</h2>
      <ul class="payoff-list">${(synthesis.next_mathematical_physics_focus || []).map(item => `<li>${esc(item)}</li>`).join('')}</ul>
      <h2>Route Interpretations</h2>
      ${routes.map(route => `<article class="card story">
        <div class="row">
          <h3>${esc(route.route_family || route.candidate_id || 'route')}</h3>
          ${pill(route.route_disposition || 'disposition?', 'info')}
          ${pill(route.content_verdict || 'verdict?')}
        </div>
        <p><strong>Route thesis:</strong> ${esc(route.route_thesis || '')}</p>
        <p><strong>Physical meaning:</strong> ${esc(route.physical_meaning || '')}</p>
        <p><strong>Load-bearing bridge:</strong> ${esc(route.load_bearing_bridge || '')}</p>
        <p><strong>Conceptual bottleneck:</strong> ${esc(route.conceptual_bottleneck || '')}</p>
        <details open>
          <summary>Mathematical objects and mechanism chain</summary>
          <p><strong>Mathematical objects:</strong></p>
          <ul class="payoff-list">${(route.mathematical_objects || []).map(item => `<li>${esc(item)}</li>`).join('')}</ul>
          <p><strong>Mechanism chain:</strong></p>
          <ul class="payoff-list">${(route.mechanism_chain || []).map(item => `<li>${esc(item)}</li>`).join('')}</ul>
          <p><strong>Next lemma questions:</strong></p>
          <ul class="payoff-list">${(route.next_lemma_questions || []).map(item => `<li>${esc(item)}</li>`).join('')}</ul>
        </details>
        <details>
          <summary>False-positive controls and why this is not yet a proof</summary>
          <ul class="payoff-list">${(route.false_positive_controls || []).map(item => `<li>${esc(item)}</li>`).join('')}</ul>
          <p>${esc(route.why_not_a_proof || '')}</p>
        </details>
      </article>`).join('') || '<div class="empty">No physics/math strategy interpretation generated yet.</div>'}
    </div>
  </section>`;
}

function renderMacroStrategies() {
  const report = DATA.macro_strategy_report || {};
  const basis = report.story_basis || {};
  const posture = report.recommended_next_posture || {};
  return `<section class="section active">
    <div class="panel">
      <h2>General Macro Strategies</h2>
      <p class="muted">This tab synthesizes the accumulated physics story into route families. It is not a proof-progress claim; it is the current strategic map for how the problem should be attacked without drifting away from Yang-Mills.</p>
      <div class="graph-brief">
        <div class="graph-hero">
          <h3>${esc(report.headline || '')}</h3>
          <p>${esc(report.physics_language_standard || '')}</p>
        </div>
        <div class="quality">
          ${qualityChip('Research cycles read', basis.research_cycle_count || 0)}
          ${qualityChip('Latest cycle', basis.latest_cycle_id || '')}
          ${qualityChip('Macro strategies', (report.macro_strategies || []).length)}
          ${qualityChip('Good-enough contributions', basis.good_enough_contributions || 0)}
        </div>
      </div>
      <h2>Recommended Posture</h2>
      <div class="relation-board">
        <article class="relation-card enables"><span class="relation-label">Primary</span><p>${esc(posture.primary || '')}</p></article>
        <article class="relation-card constrains"><span class="relation-label">Secondary</span><p>${esc(posture.secondary || '')}</p></article>
        <article class="relation-card induces"><span class="relation-label">Handoff</span><p>${esc(posture.handoff || '')}</p></article>
        <article class="relation-card falsifies"><span class="relation-label">Avoid</span><p>${esc(posture.avoid || '')}</p></article>
      </div>
      <h2>Current Strategy Families</h2>
      ${(report.macro_strategies || []).map(renderMacroStrategyCard).join('') || '<div class="empty">No macro strategy report generated yet.</div>'}
    </div>
  </section>`;
}

function renderJudgeProgressRow(row) {
  return `<article class="relation-card">
    <span class="relation-label">${esc(row.cycle_id || '')}</span>
    <p>${rich(row.change_html, row.change || row.block || '')}</p>
    ${row.next_analysis ? `<p><strong>Next:</strong> ${rich(row.next_analysis_html, row.next_analysis)}</p>` : ''}
  </article>`;
}

function renderStrategyProgressionJudge() {
  const judge = DATA.strategy_progression_judge || {};
  const cadence = judge.judgement_cadence || {};
  const window = judge.window || {};
  const strategy = judge.current_strategy || {};
  const progress = judge.progression_judgement || {};
  const readiness = judge.paper_contribution_readiness || {};
  const alignment = judge.main_problem_alignment || {};
  const paper = DATA.timeline_paper_report || {};
  const lock = paper.paper_narrative_goal_lock || {};
  return `<section class="section active">
    <div class="panel">
      <h2>Strategy Progression Judge</h2>
      <p class="muted">This tab is the 10-cycle payoff judge. It reads the target problem, literature evolution, latest analysis outputs, macro strategy, and contribution monitor, then asks whether the current route is close to a paper-level scientific subgoal and still aligned with the main problem.</p>
      <div class="graph-brief">
        <div class="graph-hero">
          <h3>${esc(strategy.title || 'No strategy judge generated yet')}</h3>
          <p><strong>Active object:</strong> ${rich(strategy.active_object_html, strategy.active_object || '')}</p>
          <p><strong>Decision:</strong> ${pill(progress.decision || 'not generated', progress.decision?.includes('handoff') ? 'good' : progress.decision?.includes('quarantine') ? 'fail' : 'info')} ${pill(progress.payoff_potential || 'payoff?', progress.payoff_potential?.includes('high') ? 'good' : progress.payoff_potential === 'low' ? 'fail' : 'info')}</p>
        </div>
        <div class="quality">
          ${qualityChip('Judged cycles', window.window_research_cycle_count || 0)}
          ${qualityChip('Start', window.start_cycle_id || '')}
          ${qualityChip('End', window.end_cycle_id || '')}
          ${qualityChip('Completed 10-cycle windows', cadence.completed_ten_cycle_windows || 0)}
          ${qualityChip('Progression score', progress.progression_score || 0)}
          ${qualityChip('Paper readiness', readiness.readiness_level || '')}
        </div>
      </div>
      <div class="card story">
        <h3>Judgement Summary</h3>
        <p>${rich(progress.summary_html, progress.summary || '')}</p>
        <p><strong>Contribution pivot invariant:</strong> ${rich(progress.contribution_pivot_invariant_html, progress.contribution_pivot_invariant || '')}</p>
        <p><strong>Next decisive test:</strong> ${rich(progress.next_decisive_test_html, progress.next_decisive_test || '')}</p>
        <p><strong>When to stop:</strong> ${rich(progress.when_to_stop_html, progress.when_to_stop || '')}</p>
        <p><strong>Do not stop prematurely if:</strong> ${rich(progress.do_not_stop_prematurely_if_html, progress.do_not_stop_prematurely_if || '')}</p>
      </div>
      <div class="card story">
        <h3>Paper Narrative Goal Lock</h3>
        <p><strong>Subgoal:</strong> ${rich(lock.subgoal_title_html, lock.subgoal_title || 'No paper lock generated yet.')}</p>
        <p><strong>Coherent thesis:</strong> ${rich(lock.coherent_narrative_thesis_html, lock.coherent_narrative_thesis || '')}</p>
        <p><strong>Anti-infinite exploration rule:</strong> ${rich(lock.anti_infinite_exploration_rule_html, lock.anti_infinite_exploration_rule || '')}</p>
        <p><strong>Decisive next work:</strong></p>
        ${listMaybeRich(lock.decisive_next_work || [], lock.decisive_next_work_html || [])}
        <p><strong>Stop or demote when:</strong></p>
        ${listMaybeRich(lock.stop_or_demote_when || [], lock.stop_or_demote_when_html || [])}
        <p><strong>Do not stop prematurely if:</strong></p>
        ${listMaybeRich(lock.do_not_stop_prematurely_if || [], lock.do_not_stop_prematurely_if_html || [])}
        <p><strong>Coherence checks:</strong></p>
        ${listMaybeRich(lock.coherence_checks || [], lock.coherence_checks_html || [])}
        ${(paper.artifacts && paper.artifacts.pdf) ? `<p><strong>Paper draft:</strong> <span class="code">${esc(paper.artifacts.pdf)}</span></p>` : ''}
      </div>
      <h2>Progress In The Judged Window</h2>
      <div class="relation-board">${(progress.what_progressed || []).map(renderJudgeProgressRow).join('') || '<div class="empty">No progress rows.</div>'}</div>
      <h2>What Still Did Not Progress</h2>
      <div class="relation-board">${(progress.what_did_not_progress || []).map(renderJudgeProgressRow).join('') || '<div class="empty">No blocked rows.</div>'}</div>
      <h2>Paper-Level Contribution Readiness</h2>
      <article class="card story">
        <div class="row">
          <h3>${esc(readiness.candidate_title || '')}</h3>
          ${pill(readiness.readiness_level || 'readiness?', readiness.readiness_level?.includes('ready') ? 'good' : readiness.readiness_level === 'developing' ? 'info' : 'warn')}
          ${pill(`score ${readiness.readiness_score || 0}`, readiness.readiness_score >= 75 ? 'good' : readiness.readiness_score >= 55 ? 'info' : 'warn')}
          ${pill(readiness.paper_contribution_type || 'type?', 'info')}
        </div>
        <p><strong>Smallest honest claim:</strong> ${rich(readiness.smallest_honest_claim_html, readiness.smallest_honest_claim || '')}</p>
        <p><strong>Novelty argument:</strong> ${rich(readiness.novelty_argument_html, readiness.novelty_argument || '')}</p>
        <p><strong>Main problem implication:</strong> ${rich(readiness.main_problem_implication_html, readiness.main_problem_implication || '')}</p>
        <p><strong>Validation burden:</strong></p>
        ${listMaybeRich(readiness.validation_burden || [], readiness.validation_burden_html || [])}
        <p><strong>Overclaim boundary:</strong> ${rich(readiness.overclaim_boundary_html, readiness.overclaim_boundary || '')}</p>
      </article>
      <h2>Main Problem Alignment</h2>
      <article class="card story">
        <div class="row">${pill(alignment.alignment_class || 'alignment?', alignment.alignment_class?.includes('aligned') ? 'good' : 'warn')}</div>
        <p><strong>Target commitments touched:</strong> ${(alignment.target_commitments_touched || []).map(item => pill(item, 'info')).join('')}</p>
        <p><strong>Source-to-target handoff:</strong> ${rich(alignment.source_to_target_handoff_html, alignment.source_to_target_handoff || '')}</p>
        <p><strong>Transfer risk:</strong> ${rich(alignment.proxy_or_transfer_risk_html, alignment.proxy_or_transfer_risk || '')}</p>
        <p><strong>Alignment gain:</strong> ${rich(alignment.alignment_gain_html, alignment.alignment_gain || '')}</p>
        <p><strong>Alignment loss:</strong> ${rich(alignment.alignment_loss_html, alignment.alignment_loss || '')}</p>
        <p><strong>Repair action:</strong> ${rich(alignment.repair_action_html, alignment.repair_action || '')}</p>
      </article>
      <h2>Strategy Payoff Table</h2>
      ${(judge.strategy_payoff_table || []).map(row => `<article class="card review">
        <div class="row"><h3>${esc(row.title || '')}</h3>${pill(`priority ${row.priority_score || 0}`, row.priority_score >= 75 ? 'good' : 'info')}</div>
        <p><strong>Payoff read:</strong> ${rich(row.payoff_read_html, row.payoff_read || '')}</p>
        <p><strong>Paper path:</strong> ${rich(row.paper_contribution_path_html, row.paper_contribution_path || '')}</p>
      </article>`).join('') || '<div class="empty">No strategy payoff table generated yet.</div>'}
      <h2>Evidence Sources</h2>
      <p>${(judge.evidence_sources || []).map(source => pill(source, 'info')).join('')}</p>
      <p><strong>Skills:</strong> ${(judge.generated_by_skills || []).map(skill => pill(skill, 'info')).join('')}</p>
    </div>
  </section>`;
}

function renderBranches() {
  return `<section class="section active">
    <div class="panel">
      <h2>Branch Memory</h2>
      ${(DATA.branch_summaries || []).map(branch => `<div class="card">
        <h3>${esc(branch.title)}</h3>
        <p>${pill(branch.status || 'status?')} ${pill(`priority ${branch.priority}`)}</p>
        <p><strong>Controlled interface:</strong> <span class="code">${esc(branch.controlled_interface)}</span></p>
        <p><strong>Latest learning:</strong> ${rich(branch.latest_learning_html, branch.latest_learning)}</p>
        <p><strong>Next experiment:</strong> ${rich(branch.next_experiment_html, branch.next_experiment)}</p>
      </div>`).join('') || '<div class="empty">No branches.</div>'}
    </div>
  </section>`;
}

function renderReviews() {
  return `<section class="section active">
    <div class="panel">
      <h2>Deep Reviews</h2>
      ${(DATA.deep_reviews || []).map(review => `<div class="card review"><h3>${esc(review.review_id)}</h3><p>${esc(review.summary)}</p><p>${pill(review.recommendation || 'recommendation?','info')}</p></div>`).join('') || '<div class="empty">No reviews.</div>'}
    </div>
  </section>`;
}

function renderArtifactOrStop() {
  const report = DATA.artifact_or_stop_control || {};
  const summary = DATA.artifact_or_stop_summary || {};
  const control = report.artifact_or_stop_control || {};
  const signatures = report.signatures || [];
  if (!report.target_id && !summary.status) {
    return `<section class="section active"><div class="panel"><h2>Artifact-Or-Stop</h2><div class="empty">No artifact-or-stop control is active for this target.</div></div></section>`;
  }
  return `<section class="section active">
    <div class="panel">
      <h2>Artifact-Or-Stop Anti-Incrementality Gate</h2>
      <div class="card story ${summary.broad_api_marathon_blocked || control.broad_api_marathon_blocked ? 'fail' : ''}">
        <div class="row">
          ${pill(summary.endpoint_mode || control.next_endpoint_mode || 'artifact_sprint_required', 'fail')}
          ${pill(`${summary.endpoint_repetition_count || 0} endpoint repeats`, 'warn')}
          ${pill(control.validator || summary.validator || 'agentic/scripts/validate_artifact_or_stop_control.py', 'info')}
        </div>
        <p><strong>Policy:</strong> ${esc(report.signature_policy || summary.gate_rule || '')}</p>
        <p><strong>Broad endpoint API marathon blocked:</strong> ${esc(String(summary.broad_api_marathon_blocked || control.broad_api_marathon_blocked || false))}</p>
        <p><strong>Endpoint contract:</strong> <code>${esc(summary.endpoint_contract || control.endpoint_contract || '')}</code></p>
        <p><strong>Endpoint pilot:</strong> <code>${esc(summary.endpoint_pilot || control.endpoint_pilot || '')}</code></p>
        <p><strong>Demotion packet:</strong> <code>${esc(summary.demotion_packet || control.demotion_packet || '')}</code></p>
        <p><strong>Blocker report:</strong> <code>${esc(summary.latest_json || report.latest_json || '')}</code></p>
      </div>
      ${signatures.map(row => `
        <article class="card story">
          <div class="row">
            <h3>${esc(row.blocker_signature || '')}</h3>
            ${pill(row.blocker_kind || '', row.blocker_kind === 'artifact-blocked' ? 'fail' : 'info')}
            ${pill(`${row.repetition_count || 0} repeats`, row.repetition_count >= 3 ? 'warn' : 'info')}
            ${pill(row.proposed_mode_switch || row.control_decision || '', row.proposed_mode_switch === 'artifact_sprint_required' ? 'fail' : 'info')}
          </div>
          <p>${esc(row.canonical_statement || '')}</p>
          <p><strong>Branches:</strong> ${esc(JSON.stringify(row.branch_ids || []))}</p>
          <p><strong>Missing artifacts:</strong> ${esc(JSON.stringify(row.missing_artifacts || []))}</p>
          <p><strong>Recent evidence:</strong></p>
          <ul>${(row.recent_evidence || []).map(ev => `<li><code>${esc(ev.cycle_id || '')}</code> ${esc(ev.blocking_gap || '')}</li>`).join('')}</ul>
        </article>
      `).join('') || '<div class="empty">No blocker signatures generated yet.</div>'}
    </div>
  </section>`;
}

function renderFailures() {
  const failures = (DATA.jobs || []).flatMap(job => (job.failure_events || []).map(f => ({...f, job_id: job.job_id})));
  return `<section class="section active">
    <div class="panel">
      <h2>Operational Failures Excluded From Research</h2>
      ${failures.map(f => `<div class="card fail"><div class="row"><h3>${esc(f.job_id)}</h3>${pill(`attempt ${f.cycle_number_in_job}`, 'fail')}</div><p>${esc(clean(f.output_tail))}</p></div>`).join('') || '<div class="empty">No operational failures recorded.</div>'}
    </div>
  </section>`;
}

function render() {
  try {
    document.querySelectorAll('.tab').forEach(btn => btn.classList.toggle('active', btn.dataset.tab === state.tab));
    const views = {
      overview: renderOverview,
      physics_math_strategy: renderPhysicsMathStrategy,
      jobs: renderJobs,
      timeline: renderTimeline,
      story: renderStory,
      next_queue: renderNextQueue,
      ranked_queue: renderRankedQueue,
      qualitative: renderQualitative,
      gedanken: renderGedanken,
      parsimonious: renderParsimoniousProbes,
      contributions: renderContributions,
      literature: renderProblemLiterature,
      macro_strategy: renderMacroStrategies,
      strategy_judge: renderStrategyProgressionJudge,
      artifact_or_stop: renderArtifactOrStop,
      branches: renderBranches,
      reviews: renderReviews,
      failures: renderFailures,
    };
    $('view').innerHTML = (views[state.tab] || renderOverview)();
    safeTypeset();
  } catch (error) {
    runtimeDiagnostic('The report app hit a recoverable rendering problem.', String(error));
    $('view').innerHTML = `<section class="section active"><div class="panel"><h2>Report Recovery View</h2><p>The embedded data is present, but this browser stopped while rendering the selected tab. Try another tab, or open this file in a standard desktop browser.</p><p><strong>Selected tab:</strong> ${esc(state.tab)}</p></div></section>`;
  }
}

function populateFilters() {
  const engines = [...new Set(cycles().map(c => c.engine).filter(Boolean))].sort();
  const attempts = [...new Set(cycles().map(c => c.api_attempt || c.codex_attempt || 'not_recorded'))].sort();
  const jobs = [...new Set((DATA.jobs || []).map(j => j.job_id).filter(Boolean))].sort();
  $('engineFilter').innerHTML = '<option value="all">All engines</option>' + engines.map(v => `<option value="${esc(v)}">${esc(v)}</option>`).join('');
  $('attemptFilter').innerHTML = '<option value="all">All attempts</option>' + attempts.map(v => `<option value="${esc(v)}">${esc(v)}</option>`).join('');
  $('jobFilter').innerHTML = '<option value="all">All jobs</option>' + jobs.map(v => `<option value="${esc(v)}">${esc(v)}</option>`).join('');
}

function init() {
  try {
    if (DATA.parse_error) runtimeDiagnostic('The embedded report data could not be parsed.', DATA.parse_error);
    $('metrics').innerHTML = [
      metric(DATA.quality?.valid_research_cycles || 0, 'valid research cycles'),
      metric(TIMELINE_MODE ? (DATA.timeline_cycles?.length || 0) : (DATA.research_cycles?.length || 0), TIMELINE_MODE ? 'visible timeline cycles' : 'shown cycles'),
      metric(DATA.jobs?.length || 0, 'marathon jobs'),
      metric(DATA.quality?.average_elapsed_seconds || 0, 'avg seconds'),
      metric(DATA.report?.research_cycle_count || 0, 'reported research cycles'),
      metric(DATA.quality?.failed_attempts || 0, 'operational failures'),
      metric(DATA.scientific_contribution_monitor?.metrics?.active_candidate_count || 0, 'contribution candidates'),
      metric(DATA.target_literature_evolution?.references?.length || 0, 'cited refs'),
      metric(DATA.macro_strategy_report?.macro_strategies?.length || 0, 'macro strategies'),
      metric(DATA.strategy_progression_judge?.progression_judgement?.payoff_potential || 'n/a', 'strategy payoff'),
      metric(DATA.quality?.all_markers_ok ? 'yes' : 'no', 'markers ok'),
    ].join('');
    populateFilters();
    document.addEventListener('click', event => {
      const btn = event.target.closest('.tab[data-tab]');
      if (!btn) return;
      state.tab = btn.dataset.tab;
      render();
    });
    $('query').addEventListener('input', e => { state.query = lower(e.target.value); render(); });
    $('engineFilter').addEventListener('change', e => { state.engine = e.target.value; render(); });
    $('attemptFilter').addEventListener('change', e => { state.attempt = e.target.value; render(); });
    $('jobFilter').addEventListener('change', e => { state.job = e.target.value; render(); });
    render();
  } catch (error) {
    runtimeDiagnostic('The report app could not finish initialization.', String(error));
  }
}

document.addEventListener('DOMContentLoaded', init);
"""


def load_job_summaries(run_id: str = "") -> list[dict[str, Any]]:
    """Load job health for one run, without borrowing unrelated failures."""
    if not JOB_DIR.exists():
        return []
    jobs: list[dict[str, Any]] = []
    for path in sorted(JOB_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        log_path = ROOT / clean_text(manifest.get("log_path", ""))
        events: list[dict[str, Any]] = []
        if log_path.is_file():
            for line in log_path.read_text(encoding="utf-8").splitlines():
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(event, dict):
                    events.append(event)
        if run_id:
            from build_discovery_marathon_report import infer_job_run_id
            declared_run = clean_text(manifest.get("run_id")) or infer_job_run_id(events)
            if declared_run and declared_run != run_id:
                continue
            if not declared_run and run_id not in path.stem:
                continue
        failure_events = [event for event in events if event.get("event") == "cycle_attempt_failed"]
        jobs.append(
            {
                "job_id": manifest.get("job_id", path.stem),
                "status": manifest.get("status", ""),
                "duration_seconds": manifest.get("duration_seconds", 0),
                "completed_cycles": manifest.get("completed_cycles", 0),
                "failed_cycle_attempts": manifest.get("failed_cycle_attempts", 0),
                "updated_utc": manifest.get("updated_utc", ""),
                "log_path": manifest.get("log_path", ""),
                "event_count": len(events),
                "failure_events": failure_events,
                "last_event": events[-1] if events else {},
            }
        )
    return jobs


def cycle_job_index(jobs: list[dict[str, Any]]) -> dict[str, str]:
    index: dict[str, str] = {}
    for job in jobs:
        log_path = ROOT / clean_text(job.get("log_path", ""))
        if not log_path.is_file():
            continue
        for line in log_path.read_text(encoding="utf-8").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            tail = clean_text(event.get("output_tail", ""))
            marker = "cycle-"
            pos = tail.rfind(marker)
            if event.get("event") == "cycle_completed" and pos >= 0:
                cycle_id = tail[pos : pos + len("cycle-0000")]
                index[cycle_id] = clean_text(job.get("job_id"))
    return index


def enrich_cycle(raw: dict[str, Any], job_by_cycle: dict[str, str]) -> dict[str, Any]:
    output = raw.get("branch_outputs", [{}])[0] if raw.get("branch_outputs") else {}
    lemma = output.get("candidate_lemmas", [{}])[0] if output.get("candidate_lemmas") else {}
    record = raw.get("branch_execution_records", [{}])[0] if raw.get("branch_execution_records") else {}
    text = json.dumps(output, ensure_ascii=False).lower()
    is_research = bool(raw.get("valid_as_research_cycle"))
    mathematical_learning = output.get("mathematical_learning", raw.get("cycle_learning", ""))
    blocking_gap = output.get("attempted_derivation", {}).get("blocking_gap", "")
    derivation_steps = output.get("attempted_derivation", {}).get("steps", [])
    falsifiers = output.get("falsifiers", [])
    next_experiment = output.get("next_experiment", "")
    physical_packet = output.get("physical_relevance_impact", {})
    if not isinstance(physical_packet, dict):
        physical_packet = {}
    if not physical_packet and clean_text(raw.get("target_id")) == "yang-mills-existence-and-mass-gap-target":
        try:
            physical_packet = build_physical_relevance_impact_packet(
                output,
                {
                    "target_id": raw.get("target_id"),
                    "branch_id": output.get("branch_id"),
                    "controlled_interface": "",
                },
                cycle_number(raw),
            )
            physical_packet["legacy_derived_assessment"] = True
        except Exception:
            physical_packet = {}
    definitions = [clean_text(item) for item in lemma.get("definitions", []) if clean_text(item)]
    assumptions = [clean_text(item) for item in lemma.get("assumptions", []) if clean_text(item)]
    elicitation_note = ""
    if definitions or assumptions:
        elicitation_note = (
            "Definitions and assumptions are shown because this timeline entry contains "
            "equations or derivation steps whose validity depends on local objects and regimes."
        )
    return {
        "cycle_id": raw.get("cycle_id", ""),
        "job_id": job_by_cycle.get(raw.get("cycle_id", ""), ""),
        "execution_mode": raw.get("execution_mode", ""),
        "valid_as_research_cycle": bool(raw.get("valid_as_research_cycle")),
        "research_seconds_elapsed": raw.get("research_seconds_elapsed", 0),
        "branch_title": output.get("branch_title", ""),
        "engine": record.get("engine", ""),
        "api_attempt": record.get("api_attempt", ""),
        "codex_attempt": record.get("codex_attempt", ""),
        "model": record.get("model", ""),
        "reasoning_effort": record.get("reasoning_effort", ""),
        "lemma_count": len(output.get("candidate_lemmas", [])),
        "definition_count": len(definitions),
        "assumption_count": len(assumptions),
        "equation_count": len(lemma.get("equations", [])),
        "derivation_step_count": len(output.get("attempted_derivation", {}).get("steps", [])),
        "falsifier_count": len(output.get("falsifiers", [])),
        "dependency_update_count": len(output.get("dependency_updates", [])),
        "markers_ok": (
            all(
                [
                    "source object" in text,
                    "target object" in text,
                    "same-theory" in text or "same theory" in text,
                    all(eq.get("valid_when") for eq in lemma.get("equations", [])),
                ]
            )
            if is_research
            else False
        ),
        "mathematical_learning": mathematical_learning,
        "mathematical_learning_html": render_math_prose_html(mathematical_learning),
        "blocking_gap": blocking_gap,
        "blocking_gap_html": render_math_prose_html(blocking_gap),
        "derivation_steps": derivation_steps,
        "derivation_steps_html": [render_math_prose_html(step) for step in derivation_steps],
        "definitions": definitions,
        "definitions_html": [render_math_prose_html(definition) for definition in definitions],
        "assumptions": assumptions,
        "assumptions_html": [render_math_prose_html(assumption) for assumption in assumptions],
        "definition_assumption_elicitation_note": elicitation_note,
        "definition_assumption_elicitation_note_html": render_math_prose_html(elicitation_note),
        "equations": enrich_equations(lemma.get("equations", [])),
        "falsifiers": falsifiers,
        "falsifiers_html": [render_math_prose_html(falsifier) for falsifier in falsifiers],
        "next_experiment": next_experiment,
        "next_experiment_html": render_math_prose_html(next_experiment),
        "proof_depth_control": {
            "pressure_kind": clean_text(output.get("proof_depth_control", {}).get("pressure_kind")),
            "hard_gate": clean_text(output.get("proof_depth_control", {}).get("hard_gate")),
            "release_decision": clean_text(output.get("proof_depth_control", {}).get("release_decision")),
            "transfer_substance_verdict": clean_text(output.get("proof_depth_control", {}).get("transfer_substance_audit", {}).get("verdict")),
            "nontriviality_status": clean_text(output.get("proof_depth_control", {}).get("nontriviality_status")),
            "demotion_trigger": clean_text(output.get("proof_depth_control", {}).get("demotion_trigger")),
        },
        "physical_relevance_impact": {
            "relevance_decision": clean_text(physical_packet.get("relevance_decision")),
            "physical_carrier": clean_text(physical_packet.get("physical_carrier")),
            "target_commitments_touched": physical_packet.get("target_commitments_touched", []),
            "unification_power_score": int(
                physical_packet.get("general_impact_vector", {})
                .get("unification_power", {})
                .get("score", 0)
                or 0
            ),
            "general_impact_claim": clean_text(physical_packet.get("general_impact_claim")),
            "general_impact_claim_html": render_math_prose_html(physical_packet.get("general_impact_claim", "")),
            "incremental_math_drift_risk": clean_text(physical_packet.get("incremental_math_drift_risk")),
            "next_physical_relevance_test": clean_text(physical_packet.get("next_physical_relevance_test")),
            "next_physical_relevance_test_html": render_math_prose_html(physical_packet.get("next_physical_relevance_test", "")),
            "legacy_derived_assessment": bool(physical_packet.get("legacy_derived_assessment")),
        },
        "skill_dispatch_trace": raw.get("skill_dispatch_trace", []),
        "next_cycle_queue": raw.get("next_cycle_queue", []),
        "selected_branch_ids": raw.get("selected_branch_ids", []),
        "scheduler_decisions": raw.get("scheduler_decisions", []),
        "validation_handoff": raw.get("validation_handoff", {}),
    }


def quality_summary(cycles: list[dict[str, Any]], jobs: list[dict[str, Any]]) -> dict[str, Any]:
    if not cycles:
        return {
            "valid_research_cycles": 0,
            "average_elapsed_seconds": 0,
            "engine_counts": {},
            "attempt_counts": {},
            "minimum_quality": {},
            "all_markers_ok": False,
            "failed_attempts": sum(int(job.get("failed_cycle_attempts", 0)) for job in jobs),
        }
    engine_counts: dict[str, int] = {}
    attempt_counts: dict[str, int] = {}
    for cycle in cycles:
        engine_counts[cycle["engine"]] = engine_counts.get(cycle["engine"], 0) + 1
        attempt = cycle.get("api_attempt") or cycle.get("codex_attempt") or "not_recorded"
        attempt_counts[attempt] = attempt_counts.get(attempt, 0) + 1
    return {
        "valid_research_cycles": len(cycles),
        "average_elapsed_seconds": round(mean(float(cycle.get("research_seconds_elapsed", 0)) for cycle in cycles), 3),
        "engine_counts": engine_counts,
        "attempt_counts": attempt_counts,
        "minimum_quality": {
            "lemmas": min(cycle["lemma_count"] for cycle in cycles),
            "definitions": min(cycle["definition_count"] for cycle in cycles),
            "assumptions": min(cycle["assumption_count"] for cycle in cycles),
            "equations": min(cycle["equation_count"] for cycle in cycles),
            "derivation_steps": min(cycle["derivation_step_count"] for cycle in cycles),
            "falsifiers": min(cycle["falsifier_count"] for cycle in cycles),
            "dependency_updates": min(cycle["dependency_update_count"] for cycle in cycles),
        },
        "all_markers_ok": all(cycle["markers_ok"] for cycle in cycles),
        "failed_attempts": sum(int(job.get("failed_cycle_attempts", 0)) for job in jobs),
    }


def build_skill_dispatch_summary(cycles: list[dict[str, Any]]) -> dict[str, Any]:
    phases: dict[str, dict[str, Any]] = {}
    skill_counts: dict[str, int] = {}
    missing: list[dict[str, Any]] = []
    conditional: list[dict[str, Any]] = []
    handoffs: list[dict[str, Any]] = []
    for cycle in cycles:
        for trace in cycle.get("skill_dispatch_trace", []) or []:
            if not isinstance(trace, dict):
                continue
            phase = clean_text(trace.get("phase")) or "unknown_phase"
            phase_row = phases.setdefault(
                phase,
                {
                    "phase": phase,
                    "cycle_count": 0,
                    "skills": {},
                    "latest_validation_handoff": "",
                    "latest_cycle_id": "",
                },
            )
            phase_row["cycle_count"] += 1
            phase_row["latest_cycle_id"] = clean_text(trace.get("cycle_id") or cycle.get("cycle_id"))
            phase_row["latest_validation_handoff"] = clean_text(trace.get("validation_handoff"))
            for skill in trace.get("invoked_skills", []) or []:
                skill = clean_text(skill)
                if not skill:
                    continue
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
                phase_row["skills"][skill] = int(phase_row["skills"].get(skill, 0)) + 1
            for skill in trace.get("missing_required_skills", []) or []:
                missing.append({"cycle_id": cycle.get("cycle_id", ""), "phase": phase, "skill": skill})
            for item in trace.get("queued_conditional_skills", []) or []:
                if isinstance(item, dict):
                    conditional.append(
                        {
                            "cycle_id": cycle.get("cycle_id", ""),
                            "phase": phase,
                            "skill": clean_text(item.get("skill")),
                            "reason": clean_text(item.get("reason")),
                        }
                    )
            if trace.get("validation_handoff"):
                handoffs.append(
                    {
                        "cycle_id": cycle.get("cycle_id", ""),
                        "phase": phase,
                        "validation_handoff": clean_text(trace.get("validation_handoff")),
                    }
                )
    top_skills = [
        {"skill": skill, "count": count}
        for skill, count in sorted(skill_counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    phase_rows = []
    for phase in sorted(phases):
        row = phases[phase]
        row = dict(row)
        row["skills"] = [
            {"skill": skill, "count": count}
            for skill, count in sorted(row["skills"].items(), key=lambda item: (-item[1], item[0]))
        ]
        phase_rows.append(row)
    return {
        "cycle_count": len(cycles),
        "phase_count": len(phase_rows),
        "invoked_skill_count": len(skill_counts),
        "total_skill_invocations": sum(skill_counts.values()),
        "top_skills": top_skills,
        "phases": phase_rows,
        "missing_required_skills": missing,
        "queued_conditional_skills": conditional,
        "latest_validation_handoffs": handoffs[-20:],
    }


def gedanken_cycle_number(packet: dict[str, Any]) -> int:
    numbers = []
    for raw in packet.get("originating_cycle_ids", []):
        try:
            numbers.append(int(clean_text(raw).split("-")[-1]))
        except ValueError:
            continue
    return max(numbers) if numbers else 0


def gedanken_queue_items(gedanken_report: dict[str, Any], *, minimum_cycle: int = 0) -> list[dict[str, Any]]:
    rows = []
    for packet in gedanken_report.get("packets", []) if isinstance(gedanken_report, dict) else []:
        if not isinstance(packet, dict):
            continue
        cycle_num = gedanken_cycle_number(packet)
        if minimum_cycle and cycle_num < minimum_cycle:
            continue
        if packet.get("need_decision") == "quarantine_as_analogy":
            continue
        transfer = packet.get("transfer_scope", {}) if isinstance(packet.get("transfer_scope"), dict) else {}
        for index, task in enumerate(packet.get("followup_cycle_tasks", []), start=1):
            if not isinstance(task, dict):
                continue
            experiment = clean_text(task.get("description"))
            if not experiment:
                continue
            rows.append(
                {
                    "cycle_id": (packet.get("originating_cycle_ids") or ["gedanken"])[0],
                    "cycle_number": cycle_num,
                    "engine": "gedanken_experiment",
                    "attempt": packet.get("epistemic_status", "conceptual_probe"),
                    "job_id": "",
                    "queue_source": "gedanken",
                    "packet_id": packet.get("packet_id", ""),
                    "situation_title": packet.get("situation", {}).get("title", ""),
                    "transfer_verdict": transfer.get("transfer_verdict", task.get("transfer_verdict", "")),
                    "branch_title": packet.get("situation", {}).get("title", ""),
                    "next_experiment": experiment,
                    "next_experiment_html": render_math_prose_html(experiment),
                    "success_criterion": task.get("success_criterion", ""),
                    "failure_or_demotion_criterion": task.get("failure_or_demotion_criterion", ""),
                    "required_skills_from_packet": task.get("required_skills", []),
                    "original_queue_index": index,
                }
            )
    return rows


def proof_delivery_queue_items(proof_queue: dict[str, Any] | None, *, minimum_cycle: int = 0) -> list[dict[str, Any]]:
    if not isinstance(proof_queue, dict) or clean_text(proof_queue.get("target_id")) != "p-vs-np-target":
        return []
    rows = []
    for index, item in enumerate(proof_queue.get("items", []) if isinstance(proof_queue.get("items"), list) else [], start=1):
        if not isinstance(item, dict):
            continue
        next_experiment = clean_text(item.get("next_analysis") or item.get("next_experiment"))
        if not next_experiment:
            continue
        rows.append(
            {
                "cycle_id": item.get("queue_id", "proof-delivery"),
                "cycle_number": 10_000 - index,
                "engine": "proof_delivery",
                "attempt": "proof_packet",
                "job_id": "",
                "queue_source": "proof_delivery_priority",
                "queue_id": item.get("queue_id", ""),
                "branch_title": item.get("title", ""),
                "source_anchor": item.get("source_anchor", ""),
                "proof_status": item.get("proof_status", ""),
                "next_experiment": next_experiment,
                "next_experiment_html": render_math_prose_html(next_experiment),
                "source_object": item.get("source_object", ""),
                "source_object_html": render_math_prose_html(item.get("source_object", "")),
                "target_object": item.get("target_object", ""),
                "target_object_html": render_math_prose_html(item.get("target_object", "")),
                "transfer_condition": item.get("transfer_condition", ""),
                "transfer_condition_html": render_math_prose_html(item.get("transfer_condition", "")),
                "theorem_goal": item.get("theorem_goal", ""),
                "theorem_goal_html": render_math_prose_html(item.get("theorem_goal", "")),
                "validation_steps": item.get("validation_steps", []),
                "validation_steps_html": [render_math_prose_html(step) for step in item.get("validation_steps", [])],
                "payoff_criteria": [{"text": text, "html": render_math_prose_html(text)} for text in item.get("success_criteria", [])],
                "stop_criteria": item.get("demotion_criteria", []),
                "stop_criteria_html": [render_math_prose_html(text) for text in item.get("demotion_criteria", [])],
                "do_not_stop_if": item.get("do_not_stop_if", []),
                "do_not_stop_if_html": [render_math_prose_html(text) for text in item.get("do_not_stop_if", [])],
                "required_skills": item.get("required_skills", []),
                "branch_continuation_decision": item.get("branch_control", "run_before_broad_exploration"),
                "branch_continuation_reason": "This proof-delivery item must be discharged before broad exploration because it targets the current theorem-shaped blocker.",
                "why_target": item.get("theorem_goal", ""),
                "risk": "Main risk: the item becomes new exploration instead of emitting a proof packet or blocked-lemma disposition.",
                "priority_score": item.get("priority_score", 9999 - index),
                "priority_band": item.get("priority_band", "proof-delivery-highest"),
                "original_queue_index": -1000 + index,
                "paper_handoff": item.get("paper_handoff", ""),
            }
        )
    return rows


def build_next_experiment_queue(
    cycles: list[dict[str, Any]],
    gedanken_report: dict[str, Any] | None = None,
    *,
    minimum_cycle: int = 0,
    strategy_judge: dict[str, Any] | None = None,
    target_id: str = "",
    proof_delivery_queue: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    queue = []
    if target_id == "p-vs-np-target":
        queue.extend(proof_delivery_queue_items(proof_delivery_queue or {}, minimum_cycle=minimum_cycle))
    for cycle in cycles:
        if minimum_cycle and cycle_number(cycle) < minimum_cycle:
            continue
        next_experiment = clean_text(cycle.get("next_experiment", ""))
        if not next_experiment:
            continue
        queue.append(
            {
                "cycle_id": cycle.get("cycle_id", ""),
                "engine": cycle.get("engine", ""),
                "attempt": cycle.get("api_attempt") or cycle.get("codex_attempt") or "not_recorded",
                "job_id": cycle.get("job_id", ""),
                "queue_source": "cycle",
                "next_experiment": next_experiment,
                "next_experiment_html": render_math_prose_html(next_experiment),
            }
        )
    if gedanken_report:
        queue.extend(gedanken_queue_items(gedanken_report, minimum_cycle=minimum_cycle))
    if target_id == "yang-mills-existence-and-mass-gap-target":
        queue.extend(build_paper_argument_priority_items(cycles, strategy_judge or {}, minimum_cycle=minimum_cycle))
        decisive_item = build_decisive_next_move_item(cycles, strategy_judge or {}, minimum_cycle=minimum_cycle)
        if decisive_item:
            queue.append(decisive_item)
    return queue


def finite_theorem_packaging_steps() -> list[str]:
    return [
        "State the finite theorem cleanly: assume a normalized reflected Wilson quotient q_tau=J+tau H+tau^2 K+O(tau^3), with J=11^*/n or the equivalent normalized vacuum rank-one matrix, Hermitian H,K, and a specified collar-remainder norm.",
        "Prove the theorem independently of Yang-Mills: remove the vacuum direction by Schur complement, project with P=I-11^*/n, and show that OS positivity forces PHP>=0 and, on ker(PHP), the Schur-corrected form P(K-n^{-1}Hee^*H)P>=0.",
        "Separate theorem proof from physical transfer: mark the finite theorem as a matrix/quotient result whose hypotheses must later be instantiated by Wilson observable data.",
        "Package the theorem as a paper section with definitions, hypotheses, proposition/theorem statement, proof skeleton, non-claims, and validation checklist.",
    ]


def endpoint_calculation_packaging_steps() -> list[str]:
    return [
        "Instantiate the source object: choose the smallest locked reflected Wilson collar family, preferably three hairpins with common reflection-plane footprint, and define the reflected Gram block N_delta, same-theory boundary factor B_delta, and quotient q_delta=widehat N_delta oslash widehat B_delta.",
        "Compute or symbolically parameterize the leading H and corrected K boundary-OPE coefficients for that three-hairpin block, keeping diagonal normalization, gauge-invariant Wilson observable algebra, cutoff/collar regime, and reflection map explicit.",
        "Run the finite positivity test: evaluate PHP on 1^perp and, if PHP has a null sector, evaluate P(K-n^{-1}Hee^*H)P on ker(PHP), recording the zero-sum vectors, determinant/minor tests, and any negative reduced coefficient.",
        "Compute the endpoint-box Kappa_{4,v}^{sing,epsilon} worked example: enumerate plaquette-sheet four-flux cumulants, color contractions, endpoint incidence signs sigma_{i,v}, negative eigenvalue bounds, and tail estimates.",
        "Package the calculation as a reproducible worked example with finite tables, formulas, sign/eigenvalue test, and explicit validation decision.",
    ]


def prior_art_packaging_steps() -> list[str]:
    return [
        "State the same-theory transfer certificate: identify the uniform collar-remainder estimate and observable-density or reconstruction handoff needed before the finite Wilson quotient can count as OS-positive continuum Yang-Mills evidence.",
        "Package the validation result: compare against prior art on OS reflection positivity, Schur complements, Feshbach reductions, Wilson loop/OPE expansions, and constructive Yang-Mills routes; then decide paper-note promotion, observable-family repair, backtrack, or quarantine.",
        "Separate standard machinery from the candidate contribution: Schur complements and OS positivity are standard, while the specific reflected-Wilson endpoint obstruction packet must be positioned conditionally.",
        "Build the reference-acquisition queue for closest comparators before claiming novelty.",
    ]


def build_paper_argument_priority_items(cycles: list[dict[str, Any]], strategy_judge: dict[str, Any], *, minimum_cycle: int = 0) -> list[dict[str, Any]]:
    if not cycles:
        return []
    latest = cycles[-1]
    if minimum_cycle and cycle_number(latest) < minimum_cycle:
        return []
    progress = strategy_judge.get("progression_judgement", {}) if isinstance(strategy_judge, dict) else {}
    readiness = strategy_judge.get("paper_contribution_readiness", {}) if isinstance(strategy_judge, dict) else {}
    source_object = (
        "The finite reflected Wilson collar Gram quotient and endpoint-box cumulant packet extracted from the latest Yang-Mills marathon cycles."
    )
    target_object = (
        "A scoped paper-note argument: finite theorem, worked endpoint calculation, and prior-art boundary for a Wilson/OS obstruction criterion."
    )
    transfer_condition = (
        "The paper may claim only the finite theorem and worked reduction unless the same-theory Wilson boundary OPE, endpoint tails, and uniform cutoff/collar remainder are validated."
    )
    common = {
        "cycle_id": latest.get("cycle_id", ""),
        "cycle_number": cycle_number(latest),
        "branch_title": latest.get("branch_title", ""),
        "engine": latest.get("engine", ""),
        "attempt": latest.get("api_attempt") or latest.get("codex_attempt") or "not_recorded",
        "job_id": latest.get("job_id", ""),
        "queue_source": "paper_argument_priority",
        "source_object": source_object,
        "source_object_html": render_math_prose_html(source_object),
        "target_object": target_object,
        "target_object_html": render_math_prose_html(target_object),
        "transfer_condition": transfer_condition,
        "transfer_condition_html": render_math_prose_html(transfer_condition),
        "smallest_honest_claim": clean_text(readiness.get("smallest_honest_claim"))
        or "A finite reflected-Wilson obstruction criterion can be packaged as a bounded paper note without claiming Yang-Mills mass gap.",
        "smallest_honest_claim_html": render_math_prose_html(
            clean_text(readiness.get("smallest_honest_claim"))
            or "A finite reflected-Wilson obstruction criterion can be packaged as a bounded paper note without claiming Yang-Mills mass gap."
        ),
        "branch_continuation_decision": "paper_packaging_priority",
        "branch_continuation_reason": "These are argument-structuring tasks required before the current contribution can become a credible paper draft.",
        "premature_stop_guard": "Do not resume broad discovery until these paper-argument tasks have produced a theorem section, worked example, and prior-art boundary.",
        "premature_stop_guard_html": render_math_prose_html("Do not resume broad discovery until these paper-argument tasks have produced a theorem section, worked example, and prior-art boundary."),
        "when_to_stop": clean_text(progress.get("when_to_stop"))
        or "Stop the paper-packaging pass only when theorem, worked calculation, and prior-art positioning sections each have a validation handoff.",
        "when_to_stop_html": render_math_prose_html(
            clean_text(progress.get("when_to_stop"))
            or "Stop the paper-packaging pass only when theorem, worked calculation, and prior-art positioning sections each have a validation handoff."
        ),
    }
    specs = [
        {
            "subtype": "finite_theorem_section",
            "original_queue_index": -30,
            "priority_score": 103,
            "priority_band": "paper-highest",
            "next_experiment": "Paper task 1: package the finite Schur-Feshbach tangent-cone criterion as a self-contained theorem section with definitions, hypotheses, proof skeleton, local conclusion, and non-claims.",
            "steps": finite_theorem_packaging_steps(),
            "required_skills": ["finite-theorem-section-packager", "timeline-formal-physics-deriver", "paper-contribution-readiness-judge", "main-problem-alignment-auditor", "next-experiment-queue-ranker"],
            "payoff_criteria": [
                "The paper has a theorem statement independent of Yang-Mills with every hypothesis named.",
                "The proof skeleton shows where Schur complement, quotient projection, and null-sector positivity enter.",
                "The section states what remains a Wilson/OPE transfer obligation.",
                "A reader can verify the finite theorem without reading marathon logs.",
            ],
        },
        {
            "subtype": "endpoint_worked_calculation",
            "original_queue_index": -20,
            "priority_score": 102,
            "priority_band": "paper-highest",
            "next_experiment": "Paper task 2: package the endpoint-box Kappa_{4,v}^{sing,epsilon} calculation as a worked example with incidence table, color/geometric factors, eigenvalue or sign bound, and reproducibility notes.",
            "steps": endpoint_calculation_packaging_steps(),
            "required_skills": ["endpoint-worked-calculation-packager", "symbolic-matrix-probe", "finite-algebra-interface-builder", "analytic-estimate-obligation-builder", "next-experiment-queue-ranker"],
            "payoff_criteria": [
                "The worked example contains the actual finite endpoint inputs rather than another route summary.",
                "The incidence/sign table and color factors are explicit enough to reproduce.",
                "The sign/eigenvalue condition is stated against the Schur-Feshbach margin.",
                "Failure or success changes whether the paper claims a validation example, obstruction, or open estimate.",
            ],
        },
        {
            "subtype": "prior_art_positioning",
            "original_queue_index": -10,
            "priority_score": 101,
            "priority_band": "paper-highest",
            "next_experiment": "Paper task 3: build the prior-art positioning section for the finite Wilson/OS obstruction note, separating standard OS/Schur/Feshbach machinery from the candidate reflected-Wilson endpoint obstruction contribution.",
            "steps": prior_art_packaging_steps(),
            "required_skills": ["prior-art-positioning-packager", "timeline-reference-manager", "prior-art-importer", "paper-contribution-readiness-judge", "next-experiment-queue-ranker"],
            "payoff_criteria": [
                "Closest prior-art families are named before novelty is claimed.",
                "The paper distinguishes reused machinery from its candidate contribution.",
                "The novelty claim is conditional and bounded by explicit non-claims.",
                "Missing references become a concrete acquisition queue.",
            ],
        },
    ]
    items = []
    for spec in specs:
        item = dict(common)
        steps = spec["steps"]
        payoff = spec["payoff_criteria"]
        item.update(
            {
                "paper_task_subtype": spec["subtype"],
                "next_experiment": spec["next_experiment"],
                "next_experiment_html": render_math_prose_html(spec["next_experiment"]),
                "validation_steps": steps,
                "validation_steps_html": [render_math_prose_html(step) for step in steps],
                "original_queue_index": spec["original_queue_index"],
                "priority_score": spec["priority_score"],
                "priority_band": spec["priority_band"],
                "why_target": "This is a non-discovery paper-argument task required to turn the current contribution candidate into a coherent manuscript section.",
                "risk": "Main risk: the task becomes another discovery branch instead of producing a bounded paper section with validation handoff.",
                "payoff_criteria": [{"text": criterion, "html": render_math_prose_html(criterion)} for criterion in payoff],
                "required_skills": sorted(set(spec["required_skills"])),
                "do_not_stop_if": [
                    "The section has a clear missing lemma, table, bound, or citation that can be supplied locally.",
                    "The task is reducing manuscript ambiguity even if it does not solve a new mathematical problem.",
                    "The result clarifies a non-claim or validation boundary needed for honest publication.",
                    "The work converts marathon evidence into a reader-checkable argument artifact.",
                ],
                "do_not_stop_if_html": [
                    render_math_prose_html(item)
                    for item in [
                        "The section has a clear missing lemma, table, bound, or citation that can be supplied locally.",
                        "The task is reducing manuscript ambiguity even if it does not solve a new mathematical problem.",
                        "The result clarifies a non-claim or validation boundary needed for honest publication.",
                        "The work converts marathon evidence into a reader-checkable argument artifact.",
                    ]
                ],
                "stop_criteria": [
                    "The task cannot name the paper section it would improve.",
                    "The task requires a new broad discovery run rather than argument structuring.",
                    "The task cannot produce a validation handoff, reproducible calculation, theorem statement, or citation queue.",
                    "The task would overstate the finite result as a Yang-Mills proof.",
                ],
                "stop_criteria_html": [
                    render_math_prose_html(item)
                    for item in [
                        "The task cannot name the paper section it would improve.",
                        "The task requires a new broad discovery run rather than argument structuring.",
                        "The task cannot produce a validation handoff, reproducible calculation, theorem statement, or citation queue.",
                        "The task would overstate the finite result as a Yang-Mills proof.",
                    ]
                ],
            }
        )
        items.append(item)
    return items


def decisive_next_move_steps() -> list[str]:
    return [
        *finite_theorem_packaging_steps()[:2],
        *endpoint_calculation_packaging_steps()[:3],
        *prior_art_packaging_steps()[:2],
    ]


def build_decisive_next_move_item(cycles: list[dict[str, Any]], strategy_judge: dict[str, Any], *, minimum_cycle: int = 0) -> dict[str, Any] | None:
    if not cycles:
        return None
    latest = cycles[-1]
    if minimum_cycle and cycle_number(latest) < minimum_cycle:
        return None
    progress = strategy_judge.get("progression_judgement", {}) if isinstance(strategy_judge, dict) else {}
    readiness = strategy_judge.get("paper_contribution_readiness", {}) if isinstance(strategy_judge, dict) else {}
    next_test = clean_text(progress.get("next_decisive_test")) or clean_text(latest.get("next_experiment"))
    if not next_test:
        return None
    steps = decisive_next_move_steps()
    source_object = (
        "A finite reflected Wilson collar Gram quotient q_delta=widehat N_delta oslash widehat B_delta built from a locked "
        "gauge-invariant Wilson hairpin family with common reflection-plane footprint."
    )
    target_object = (
        "A same-theory OS-positive continuum Schwinger-function bridge for four-dimensional Yang-Mills, sufficient to inform "
        "reconstruction and later spectral-gap obligations without claiming the Clay theorem."
    )
    transfer_condition = (
        "The finite quotient is relevant only if H,K arise from the same Wilson observable algebra and the O(delta^3) or o(tau^2) "
        "collar remainder is uniform in the cutoff/volume topology used for the continuum handoff."
    )
    next_experiment = (
        "Decisive validation packet for the current contribution candidate: prove the finite Wilson/OS Schur-Feshbach obstruction "
        "criterion, instantiate it on the minimal three-hairpin reflected Wilson collar block, compute or parameterize H and corrected K, "
        "and decide whether the result supports paper-note promotion, observable-family repair, backtracking, or quarantine."
    )
    smallest_honest_claim = clean_text(readiness.get("smallest_honest_claim")) or (
        "A finite Wilson/OS Schur-Feshbach obstruction criterion can be stated and tested on a minimal three-hairpin collar block, "
        "yielding either a bounded paper-note contribution, a same-theory transfer obligation, or a precise falsifier/repair gate without "
        "claiming the Yang-Mills mass gap."
    )
    payoff_criteria = [
        "Promotion: the finite theorem is proved with explicit hypotheses and the three-hairpin calculation yields a nontrivial positivity gate, obstruction, or validation handoff.",
        "Repair: H,K are definable but the first tested family is degenerate, forcing a named change of Wilson hairpin geometry while preserving the same observable algebra.",
        "Backtrack: the finite theorem is correct but the boundary quotient B_delta or collar expansion cannot be made same-theory without an additional bridge lemma.",
        "Quarantine: after two sharpened attempts, no locked Wilson collar family supplies H,K with controlled remainders or any finite test that changes route priority.",
    ]
    do_not_stop_if = [
        "The finite Schur-Feshbach theorem is proved but the first Wilson hairpin family has not yet been instantiated.",
        "The three-hairpin H,K coefficients are only parameterized, but their sign structure still gives a concrete PHP or corrected-K test.",
        "The obstruction fails only because a named collar-remainder or boundary-OPE estimate is missing and can be isolated as a smaller analytic obligation.",
        "The result could still become a scoped paper note about a finite OS obstruction criterion even without proving the Yang-Mills mass gap.",
    ]
    stop_criteria = [
        "The finite theorem cannot be stated without vacuous positivity, unstable normalization, or undefined quotient data.",
        "The three-hairpin calculation cannot keep the source object inside the gauge-invariant Wilson observable algebra after one named repair.",
        "The required uniform collar-remainder estimate cannot be localized and remains a broad continuum assumption.",
        "The analysis repeats the Schur/Feshbach ladder without producing a theorem statement, H,K computation, transfer certificate, or prior-art boundary.",
    ]
    required_skills = sorted(
        {
            "next-experiment-queue-ranker",
            "paper-contribution-readiness-judge",
            "main-problem-alignment-auditor",
            "progression-payoff-judge",
            "finite-algebra-interface-builder",
            "symbolic-matrix-probe",
            "analytic-estimate-obligation-builder",
            "prior-art-importer",
            "timeline-formal-physics-deriver",
        }
    )
    return {
        "cycle_id": latest.get("cycle_id", ""),
        "cycle_number": cycle_number(latest),
        "branch_title": latest.get("branch_title", ""),
        "engine": latest.get("engine", ""),
        "attempt": latest.get("api_attempt") or latest.get("codex_attempt") or "not_recorded",
        "job_id": latest.get("job_id", ""),
        "queue_source": "decisive_next_move",
        "source_object": source_object,
        "source_object_html": render_math_prose_html(source_object),
        "target_object": target_object,
        "target_object_html": render_math_prose_html(target_object),
        "transfer_condition": transfer_condition,
        "transfer_condition_html": render_math_prose_html(transfer_condition),
        "next_experiment": next_experiment,
        "next_experiment_html": render_math_prose_html(next_experiment),
        "validation_steps": steps,
        "validation_steps_html": [render_math_prose_html(step) for step in steps],
        "original_queue_index": 0,
        "priority_score": 100,
        "priority_band": "high",
        "why_target": (
            "This is the decisive next move because it converts the current high-payoff Wilson/OS obstruction candidate from repeated route "
            "sharpening into a bounded theorem-plus-worked-example validation packet."
        ),
        "risk": "Main risk: the finite obstruction remains mathematically valid but fails to acquire a same-theory Wilson/OPE transfer certificate.",
        "payoff_criteria": [{"text": criterion, "html": render_math_prose_html(criterion)} for criterion in payoff_criteria],
        "required_skills": required_skills,
        "branch_continuation_decision": "continue_run_next",
        "branch_continuation_reason": (
            "Run this before any further broad marathon because the strategy judge marked the route as handoff-after-bounded-validation "
            "and paper-note-ready only if the bounded validation packet is produced."
        ),
        "premature_stop_guard": clean_text(progress.get("do_not_stop_prematurely_if"))
        or "Do not stop while the finite theorem, concrete Wilson H,K calculation, or same-theory transfer certificate remains untested.",
        "premature_stop_guard_html": render_math_prose_html(
            clean_text(progress.get("do_not_stop_prematurely_if"))
            or "Do not stop while the finite theorem, concrete Wilson H,K calculation, or same-theory transfer certificate remains untested."
        ),
        "do_not_stop_if": do_not_stop_if,
        "do_not_stop_if_html": [render_math_prose_html(item) for item in do_not_stop_if],
        "stop_criteria": stop_criteria,
        "stop_criteria_html": [render_math_prose_html(item) for item in stop_criteria],
        "when_to_stop": clean_text(progress.get("when_to_stop"))
        or "Stop only when the bounded validation packet fails to produce a theorem, worked Wilson example, transfer certificate, or paper-note boundary.",
        "when_to_stop_html": render_math_prose_html(
            clean_text(progress.get("when_to_stop"))
            or "Stop only when the bounded validation packet fails to produce a theorem, worked Wilson example, transfer certificate, or paper-note boundary."
        ),
        "smallest_honest_claim": smallest_honest_claim,
        "smallest_honest_claim_html": render_math_prose_html(smallest_honest_claim),
    }


def contains_any(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return any(term in lower for term in terms)


def pvsnp_branch_controls(combined: str, experiment: str = "") -> dict[str, Any]:
    lower = clean_text(f"{combined} {experiment}").lower()
    if contains_any(lower, ["black-box", "oracle-interface", "substitution", "beta", "target-query", "query length"]):
        when_to_stop = (
            "Stop or quarantine this black-box substitution branch only after the source carrier, SAT-query length exponent beta, "
            "interface size exponent q, source-threshold exponent, and target class have been explicitly computed; quarantine if every sharpened "
            "interface still has positive beta and therefore only excludes a bounded range of SAT circuit exponents rather than NP subset P/poly."
        )
        guard = (
            "Do not stop before deriving the transfer inequality from SAT in SIZE(n^c) to the carrier upper bound, identifying whether beta=0, "
            "beta>0, or the argument is genuinely nonblackbox, and recording the barrier status of the proposed escape."
        )
        do_not_stop_if = [
            "The branch has not yet computed beta, q, and the induced source upper-bound exponent under SAT in SIZE(n^c).",
            "A subpolynomial-query or nonblackbox carrier remains available and has not been audited.",
            "The latest failure sharpened the threshold-collapse lemma into a formal no-go statement.",
            "The route can still isolate advice leakage, nonuniformity, naturalness, or algebrization as the exact obstruction.",
        ]
        stop_criteria = [
            "Every named carrier in the branch has beta>0 and yields only a bounded target-exponent exclusion.",
            "The branch cannot state a source lower-bound model, target class, and transfer inequality in the same notation.",
            "The proposed escape is only a black-box substitution restatement with no new carrier or nonblackbox mechanism.",
            "The barrier audit shows the needed source lower bound is just as hard as the original P vs NP/P/poly target.",
        ]
    elif contains_any(lower, ["mcsp", "mktp", "meta-complexity", "truth table", "gapmcsp"]):
        when_to_stop = (
            "Stop or quarantine this meta-complexity carrier branch only after MCSP/MKtP parameters, truth-table length N, size threshold s, "
            "verifier overhead, target SAT-circuit use, and natural-proof or advice-leakage status have been computed; quarantine if the transfer "
            "still produces only a finite exponent window or relies on a dense natural property without an escape certificate."
        )
        guard = (
            "Do not stop before naming the carrier variant, deriving its verifier/reduction overhead, and checking whether a SAT in SIZE(n^c) "
            "assumption gives carrier circuits below the claimed source lower-bound threshold."
        )
        do_not_stop_if = [
            "The MCSP/MKtP parameter regime has not yet been fixed.",
            "The truth-table length N and underlying input length n have not been related in the transfer inequality.",
            "The natural-proof largeness/constructivity issue has not yet been audited.",
            "A nonblackbox use of the target circuit could still avoid the multiplicative c factor.",
        ]
        stop_criteria = [
            "The induced carrier upper bound under SAT in SIZE(n^c) remains N^{q+beta c+o(1)} with beta>0 for all tested parameter choices.",
            "The source lower bound required for MCSP/MKtP is as strong as the target separation or becomes a natural property without an escape.",
            "The route cannot prevent advice leakage or model mismatch between the carrier lower bound and P/poly target.",
        ]
    elif contains_any(lower, ["padding", "projection", "pad_", "growth padding", "sparse", "valid length"]):
        when_to_stop = (
            "Stop or quarantine this padding/projection branch only after the length map N(n), projection overhead, source lower-bound quantifier "
            "and target exponent window are calculated; quarantine if the route merely moves the P vs NP difficulty into sparse valid-length lower bounds."
        )
        guard = (
            "Do not stop before deriving the exponent transfer c -> c/k or its growth-padding analogue, and before stating whether the result excludes "
            "all polynomial SAT exponents or only a bounded exponent interval."
        )
        do_not_stop_if = [
            "The quantifier pattern has not been repaired between fixed-k, unbounded-k, and single growth-padding carriers.",
            "The projection-sandwich inequality has not yet been written as an explicit circuit-size transfer.",
            "The sparse valid-length lower-bound obligation has not been isolated as the real source debt.",
        ]
        stop_criteria = [
            "The branch only proves a finite target-exponent lower bound and cannot scale to NP not subset P/poly.",
            "The route requires sparse valid-length lower bounds that are not weaker than the original target problem.",
            "The projection carrier has no nonprojection mechanism and no subpolynomial embedding repair.",
        ]
    else:
        when_to_stop = (
            "Stop or quarantine this P vs NP branch only after it states the source object, target class, complexity model, transfer inequality, "
            "quantifier strength, and barrier status; quarantine if two sharpened attempts still cannot say whether the route implies SAT notin P/poly, "
            "NP not subset P/poly, or only a weaker/proxy lower bound."
        )
        guard = (
            "Do not stop before the branch has produced a concrete source-to-target transfer theorem, an explicit obstruction lemma, or a barrier-aware "
            "reason why the route cannot reach the P vs NP/P/poly target."
        )
        do_not_stop_if = [
            "A transfer exponent, quantifier repair, or barrier status remains uncomputed.",
            "The branch can still name a target-preserving carrier and a falsifiable lower-bound threshold.",
            "The failure can become a formal no-go lemma for a route family.",
        ]
        stop_criteria = [
            "The branch cannot identify a source language/carrier and target complexity class in the same model.",
            "The route repeatedly proves only a proxy lower bound with no target-preserving transfer.",
            "The remaining work is a slogan about hardness magnification rather than a computable transfer or obstruction.",
        ]
    return {
        "when_to_stop": when_to_stop,
        "premature_stop_guard": guard,
        "do_not_stop_if": do_not_stop_if,
        "stop_criteria": stop_criteria,
    }


def dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        cleaned = clean_text(item)
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(cleaned)
    return result


def pvsnp_branch_specific_payoff_criteria(combined: str) -> list[str]:
    """Return decisive, branch-level P vs NP payoff tests before generic gates."""

    lower = combined.lower()
    criteria: list[str] = []
    if contains_any(lower, ["cap profile", "one-sided semantic", "sep_n", "semantic separator", "planted-slice"]):
        criteria.extend(
            [
                "For the one-sided semantic-separator branch, compute the cap profile A_N(s) for the named generator and predicate class; promotion requires a bound strong enough to force Sep_N^{1s}(E)>N^{1+epsilon-o(1)}.",
                "Exhibit or refute a subthreshold semantic planted-slice predicate; this decides whether the generated-OR carrier needs range-closure repair, stronger pseudorandomness, or quarantine.",
            ]
        )
    if contains_any(lower, ["sound local certificate", "slc cover", "partial certificate", "term cover", "backdoor"]):
        criteria.extend(
            [
                "For the certificate-cover branch, compute K,E,L and the induced circuit upper bound C(H_N)<=C(G_N)+O(K(s+L^{O(1)})+EN); promotion requires every sound local cover to stay above the N^{1+epsilon-o(1)} source threshold.",
                "Falsify the branch if Horn, 2-SAT, bounded-width CNF, or bounded-backdoor emitted formulas give subthreshold satisfying-term or sound-local-certificate covers.",
            ]
        )
    if contains_any(lower, ["generated-or", "high-q", "witness projection", "assignment hitting", "unary residual"]):
        criteria.extend(
            [
                "For the high-q generated-OR carrier, compute the exact leakage exponent of the remaining witness-cover or unary-residual mechanism and compare it with 1+epsilon-q.",
                "Promotion requires q+a>1+epsilon after every projection, padding, and witness-cover leakage term is accounted for; otherwise the branch becomes a bounded-window or no-go result.",
            ]
        )
    if contains_any(lower, ["low-anf", "anf degree", "determinant", "permanent", "global invariant", "accepted-image entropy"]):
        criteria.extend(
            [
                "For the MCSP invariant branch, compute ANF degree, accepted-image entropy D, verifier cap alpha_V, and ranked-access leakage for the proposed invariant; promotion requires no accepted sparse or low-circuit truth table below 2^{epsilon m}.",
                "Quarantine a low-degree invariant if it accepts a sparse table with circuit size O(degree times m); only a nonlinear high-degree certificate with row-hard no-side soundness can stay active.",
            ]
        )
    if contains_any(lower, ["mcsp", "mktp", "direct row", "ranked decoder", "row certificate", "aggregate row"]):
        criteria.extend(
            [
                "For the MCSP/MKtP row branch, decide whether the certificate proves direct row hardness or only aggregate/rank-index hardness; record q_extract=epsilon/(1+D) and q_force=(D+epsilon)/(1+D) in the same parameter regime.",
                "Promotion requires an advice-free row-hard certificate; backtrack if the ranked decoder, canonical unranking, or aggregate proof selects a hard row nonuniformly.",
            ]
        )
    if contains_any(lower, ["degree target", "polynomial-degree", "exact degree", "approximate degree", "sign degree", "fourier sparsity", "spectral norm"]):
        criteria.extend(
            [
                "For the polynomial-measure branch, compute the unrestricted-circuit envelope B_{mu,T}(m,k); promotion requires SAT to exceed this envelope, not merely to exceed a restricted proof or representation measure.",
                "Quarantine degree-only transfers when easy P functions such as AND or PARITY already attain the claimed maximal degree, sign-degree, approximate-degree, or spectral threshold.",
            ]
        )
    if contains_any(lower, ["ac0", "formula-size", "nc1", "obdd", "branching-program", "streaming-space", "read-k", "query complexity", "bit-query"]):
        criteria.extend(
            [
                "For the restricted-model branch, compute the compiler envelope from unrestricted SIZE(m^k) or P-time algorithms into the named model; promotion requires a bound above that envelope on the same SAT slice.",
                "Falsify direct transfer if a P function already has the same restricted-model lower bound, such as PARITY for AC0, HWB for OBDD, or XOR/Tseitin for proof-system degree.",
            ]
        )
    if contains_any(lower, ["resolution", "sos", "sherali", "polynomial calculus", "nullstellensatz", "tseitin", "xor"]):
        criteria.extend(
            [
                "For the proof-complexity branch, separate fixed-family proof hardness from language hardness by naming the proof system, shortcut algorithm, and semantic lower-bound target.",
                "Promotion requires a proof-system lower bound that survives the Gaussian-elimination or recognition shortcut; otherwise the result is a restricted-proof-system separation only.",
            ]
        )
    if contains_any(lower, ["natural", "relativ", "algebr", "oracle", "advice", "nonuniform"]):
        criteria.append(
            "For this route, state the exact barrier premise it uses or escapes: relativizing, natural, algebrizing, nonuniform, or advice-leaking; promotion requires the escape to be attached to the specific transfer theorem."
        )
    if not criteria:
        criteria.append(
            "For this P vs NP branch, state the branch-local mathematical object and the exact decision test that would promote, repair, backtrack, or quarantine it."
        )
    return criteria


def pvsnp_universal_control_criteria(combined: str) -> list[str]:
    """Secondary admissibility gates shared across P vs NP branches."""

    criteria = [
        "Control gate: name the source carrier or language, target class, and circuit or resource model before claiming progress.",
        "Control gate: derive the exact transfer inequality from SAT in SIZE(n^c), NP subset P/poly, or the stated target assumption to the source-carrier upper bound.",
    ]
    lower = combined.lower()
    if contains_any(lower, ["beta", "query", "black-box", "substitution"]):
        criteria.append(
            "Control gate: compute beta and q exactly, distinguishing all-exponent consequences from bounded target-exponent windows."
        )
    if contains_any(lower, ["natural", "relativ", "algebr", "advice", "nonuniform", "p/poly"]):
        criteria.append(
            "Control gate: record relativization, natural-proofs, algebrization, nonuniformity, and advice-leakage status for the specific theorem."
        )
    return criteria


def pvsnp_queue_payoff_profile(cycle: dict[str, Any], target_id: str = "") -> dict[str, Any]:
    experiment = clean_text(cycle.get("next_experiment", ""))
    combined = clean_text(
        " ".join(
            [
                experiment,
                cycle.get("branch_title", ""),
                cycle.get("mathematical_learning", ""),
                cycle.get("blocking_gap", ""),
                " ".join(cycle.get("falsifiers", [])),
            ]
        )
    )
    lower = combined.lower()
    score = 30
    reasons: list[str] = []
    skills = [
        "long-horizon-route-portfolio-manager",
        "next-experiment-queue-ranker",
        "entailment-gap-auditor",
        "main-problem-alignment-auditor",
        "pvsnp-conceptual-pressure-localizer",
        "pvsnp-qualitative-complexity-reasoner",
        "pvsnp-symbolic-complexity-auditor",
        "pvsnp-inference-quality-controller",
    ]
    criteria: list[str] = pvsnp_branch_specific_payoff_criteria(combined)
    if contains_any(lower, ["black-box", "substitution", "oracle-interface", "beta", "query"]):
        score += 25
        reasons.append("It directly tests the current black-box substitution cap by computing beta, q, and the induced target-exponent window.")
        skills.extend(["kb-deduce", "contradiction-route-auditor", "kb-hypothesis-refutation-loop", "pvsnp-impossibility-theorem-forger", "pvsnp-symbolic-complexity-auditor", "pvsnp-reduction-consistency-reviewer", "pvsnp-proof-derivation-builder"])
        criteria.append("Compute beta and q exactly; promotion requires beta=0, subpolynomial target queries, or a genuinely nonblackbox use of the SAT circuit.")
    if contains_any(lower, ["mcsp", "mktp", "gapmcsp", "meta-complexity", "truth table"]):
        score += 20
        reasons.append("It audits a meta-complexity carrier where the decisive questions are verifier overhead, density/naturalness, and advice leakage.")
        skills.extend(["kb-abduce", "kb-concept-bridge-planner", "counterexample-hunter", "pvsnp-conceptual-pressure-localizer", "pvsnp-symbolic-complexity-auditor", "pvsnp-meta-complexity-carrier-reviewer", "pvsnp-quantifier-uniformity-reviewer"])
        criteria.append("For MCSP/MKtP, state N, n, s, verifier overhead, lower-bound model, and whether the property is natural or non-natural.")
    if contains_any(lower, ["padding", "projection", "sparse", "valid length", "growth"]):
        score += 14
        reasons.append("It checks whether padding/projection transfers really magnify hardness or merely move the proof debt into sparse lower bounds.")
        skills.extend(["kb-induce", "abducer-failure-signal-cartographer", "pvsnp-impossibility-theorem-forger", "pvsnp-symbolic-complexity-auditor", "pvsnp-reduction-consistency-reviewer", "pvsnp-quantifier-uniformity-reviewer"])
        criteria.append("State whether the transfer excludes every polynomial SAT exponent or only a bounded interval c<c0.")
    if contains_any(lower, ["nonblackbox", "non-blackbox", "succinct", "local-consistency", "proof-complexity"]):
        score += 18
        reasons.append("It points toward the only unquarantined escape: a subpolynomial-query, nonprojection, or nonblackbox carrier.")
        skills.extend(["kb-gap-abstraction-conjecturer", "kb-proof-connector", "abducer-refinement-route-ranker", "pvsnp-qualitative-complexity-reasoner", "pvsnp-symbolic-complexity-auditor", "pvsnp-proof-derivation-builder"])
        criteria.append("Promotion requires a target-preserving nonblackbox/subpolynomial mechanism, not another black-box Cook-Levin substitution.")
    if contains_any(lower, ["natural", "relativ", "algebr", "advice", "nonuniform", "p/poly"]):
        score += 12
        reasons.append("It keeps the barrier and model-boundary audit attached to the mathematical transfer rather than as after-the-fact commentary.")
        skills.extend(["kb-end-to-end-proof-critic", "paper-contribution-readiness-judge", "pvsnp-conceptual-pressure-localizer", "pvsnp-impossibility-theorem-forger", "pvsnp-symbolic-complexity-auditor", "pvsnp-barrier-specificity-reviewer", "pvsnp-quantifier-uniformity-reviewer"])
        criteria.append("Record relativization, natural-proofs, algebrization, nonuniformity, and advice-leakage status for the specific transfer theorem.")
    if contains_any(lower, ["compute", "derive", "test", "audit", "instantiate", "formalize"]):
        score += 10
        reasons.append("It is executable as a bounded complexity calculation, CAS-backed exponent audit, or formal transfer check.")
        skills.append("pvsnp-symbolic-complexity-auditor")
    if not reasons:
        reasons.append("It remains in the queue only if sharpened into a concrete transfer theorem or obstruction lemma.")
        criteria.append("Before running, rewrite the task into a source object, target object, reduction overhead, and falsifier.")
        score -= 10
    criteria.extend(pvsnp_universal_control_criteria(combined))
    if len(experiment.split()) < 16:
        score -= 8
        reasons.append("The experiment is short and should be expanded into a formal transfer-audit checklist before receiving long-run budget.")
    score = max(0, min(100, score))
    band = "high" if score >= 75 else "medium" if score >= 55 else "watch"
    risk = (
        "Low drift risk: the item is framed as an explicit P vs NP transfer audit."
        if score >= 75
        else "Moderate risk: run only if source/target/model/barrier fields are explicit."
        if score >= 55
        else "High drift risk unless rewritten into a concrete complexity-theoretic transfer test."
    )
    branch_control = branch_continuation_profile(score, combined, reasons, experiment, target_id=target_id)
    return {
        "priority_score": score,
        "priority_band": band,
        "why_target": " ".join(reasons),
        "risk": risk,
        "payoff_criteria": [{"text": criterion, "html": render_math_prose_html(criterion)} for criterion in dedupe_preserve_order(criteria)[:6]],
        "required_skills": sorted(set(skills)),
        **branch_control,
    }


def queue_payoff_profile(cycle: dict[str, Any], target_id: str = "") -> dict[str, Any]:
    if target_id == "p-vs-np-target":
        return pvsnp_queue_payoff_profile(cycle, target_id=target_id)
    experiment = clean_text(cycle.get("next_experiment", ""))
    combined = clean_text(
        " ".join(
            [
                experiment,
                cycle.get("branch_title", ""),
                cycle.get("mathematical_learning", ""),
                cycle.get("blocking_gap", ""),
                " ".join(cycle.get("falsifiers", [])),
            ]
        )
    )
    score = 20
    reasons: list[str] = []
    skills = ["long-horizon-route-portfolio-manager", "next-experiment-queue-ranker"]
    criteria: list[str] = []
    if contains_any(combined, ["det(", "determinant", "minor", "negative", "counterexample", "falsifier", "holonomy"]):
        score += 22
        reasons.append("It can force a sharp branch decision through a sign, determinant, holonomy, or counterexample calculation.")
        skills.extend(["kb-contradiction-strategist", "contradiction-route-auditor", "kb-hypothesis-refutation-loop"])
        criteria.append("A computed obstruction, sign, determinant, or counterexample decides whether the branch must persist, backtrack, or be quarantined.")
    if contains_any(combined, ["compute", "extract", "evaluate", "construct", "parameterize", "test", "form "]):
        score += 18
        reasons.append("It is operationally executable as a bounded calculation rather than an open-ended request for more prose.")
        criteria.append("The run returns named objects, explicit formulas, and a reproducible calculation or estimate rather than a narrative restatement.")
    if contains_any(combined, ["os positivity", "os-positive", "reflection positivity", "reflection-positive", "schwinger", "same-theory", "same theory"]):
        score += 16
        reasons.append("It touches the construction/reconstruction bridge where local progress can affect the target commitments.")
        skills.extend(["abducer-obligation-gatekeeper", "entailment-gap-auditor", "kb-end-to-end-proof-critic"])
        criteria.append("The result states whether the object remains inside the same reconstructed theory, with no hidden proxy shift.")
    if contains_any(combined, ["continuum", "cutoff", "limit", "uniform", "rg", "boundary ope", "collar"]):
        score += 14
        reasons.append("It tests a transfer regime where cutoff, boundary, or limiting assumptions often decide whether progress is real.")
        skills.extend(["kb-induce", "evidence-acquisition-planner", "prior-art-importer"])
        criteria.append("The calculation names the regulator or limiting regime and identifies which estimate would need to be uniform.")
    if contains_any(combined, ["spectral", "mass gap", "hamiltonian", "decay", "measure"]):
        score += 12
        reasons.append("It links local observable work to a spectral or mass-gap witness.")
        skills.extend(["kb-deduce", "kb-proof-sketcher"])
        criteria.append("The result identifies the spectral witness, its validity assumptions, and the exact missing bridge if the gap is not proven.")
    if contains_any(combined, ["variable", "regime", "monotone", "monotonicity", "sensitivity", "converge", "convergence", "limit", "order of limits", "scale", "asymptotic", "toy model", "concrete probe", "graph edge"]):
        score += 13
        reasons.append("It can sharpen the qualitative mechanistic graph by typing variables, regimes, directional behavior, limits, or concrete-probe falsifiers.")
        skills.extend(
            [
                "qualitative-variable-isolator",
                "physics-regime-map-builder",
                "monotonicity-sensitivity-prober",
                "limit-convergence-behavior-auditor",
                "qualitative-toy-model-builder",
                "qualitative-physics-falsifier",
            ]
        )
        criteria.append("The run emits or revises a typed qualitative relation packet with variables, held-fixed conditions, validity regime, graph edge, and falsifier.")
    if contains_any(combined, ["gedanken", "thought experiment", "counterfactual", "imagined situation", "controlled contrast", "transfer guard", "variant"]):
        score += 12
        reasons.append("It can use a Gedanken experiment to isolate a mechanism before spending proof-search budget on an underspecified branch.")
        skills.extend(
            [
                "gedanken-need-assessor",
                "gedanken-situation-designer",
                "gedanken-counterfactual-variant-builder",
                "gedanken-transfer-guard",
                "gedanken-followup-planner",
            ]
        )
        criteria.append("The run produces a validated Gedanken packet with need decision, controlled situation, predicted observation, transfer scope, and follow-up cycle task.")
    if contains_any(combined, ["observable", "wilson", "gauge", "hairpin", "cumulant"]):
        score += 10
        reasons.append("It is stated in the domain objects of the theory rather than in generic workflow language.")
        criteria.append("The output keeps the source object, observable algebra, and target object typed throughout the derivation.")
    if contains_any(combined, ["certify the weakest condition", "weakest condition"]):
        score -= 8
        reasons.append("It is valuable but less directly executable unless rewritten into a concrete calculation or named lemma test.")
        criteria.append("The next run must replace the broad certification request with a smallest named premise and a falsifiable test.")
    if not reasons:
        reasons.append("It remains in the queue, but its payoff is unclear until the target object, decision test, and validation handoff are sharpened.")
        criteria.append("The next run must identify a source object, target object, falsifier, and promotion or demotion condition.")
    if len(experiment.split()) < 16:
        score -= 10
        reasons.append("The experiment statement is short; it needs expansion before receiving a long-horizon budget.")
    if "analog" in combined or "analogy" in combined:
        score -= 10
        reasons.append("Analogy-driven payoff is demoted until a same-theory transfer certificate is stated.")
    score = max(0, min(100, score))
    band = "high" if score >= 75 else "medium" if score >= 55 else "watch"
    risk = "Low drift risk" if score >= 75 else "Moderate risk: run only with explicit payoff checks" if score >= 55 else "High drift risk unless the experiment is sharpened first"
    branch_control = branch_continuation_profile(score, combined, reasons, experiment, target_id=target_id)
    return {
        "priority_score": score,
        "priority_band": band,
        "why_target": " ".join(reasons),
        "risk": risk,
        "payoff_criteria": [{"text": criterion, "html": render_math_prose_html(criterion)} for criterion in criteria[:4]],
        "required_skills": sorted(set(skills)),
        **branch_control,
    }


def gedanken_payoff_profile(item: dict[str, Any]) -> dict[str, Any]:
    transfer_verdict = clean_text(item.get("transfer_verdict")) or "unknown"
    score = 68
    reasons = [
        "This follow-up comes from a validated Gedanken packet, so it has a controlled situation, expected observation, transfer scope, and demotion criterion."
    ]
    if transfer_verdict in {"needs_certificate", "transfer_ready"}:
        score += 12
        reasons.append("The transfer guard leaves a concrete certificate path rather than analogy-only drift.")
    if transfer_verdict in {"conceptual_only", "quarantine"}:
        score -= 18
        reasons.append("The transfer verdict limits active budget; use it to sharpen or quarantine rather than to claim progress.")
    if item.get("success_criterion") and item.get("failure_or_demotion_criterion"):
        score += 8
        reasons.append("The task has explicit success and demotion criteria.")
    skills = sorted(set(["next-experiment-queue-ranker", "gedanken-followup-planner", *item.get("required_skills_from_packet", [])]))
    criteria = [
        f"Success: {item.get('success_criterion', '')}",
        f"Demotion: {item.get('failure_or_demotion_criterion', '')}",
        f"Transfer verdict: {transfer_verdict}; packet: {item.get('packet_id', '')}",
    ]
    score = max(0, min(100, score))
    branch_control = branch_continuation_profile(score, clean_text(item), reasons, clean_text(item.get("next_experiment", "")))
    return {
        "priority_score": score,
        "priority_band": "high" if score >= 75 else "medium" if score >= 55 else "watch",
        "why_target": " ".join(reasons),
        "risk": "Moderate risk: conceptual-probe follow-up must keep transfer limits visible",
        "payoff_criteria": [{"text": criterion, "html": render_math_prose_html(criterion)} for criterion in criteria],
        "required_skills": skills,
        **branch_control,
    }


def domain_specific_branch_controls(combined: str, experiment: str = "", target_id: str = "") -> dict[str, Any]:
    if target_id == "p-vs-np-target":
        return pvsnp_branch_controls(combined, experiment)
    text = clean_text(f"{combined} {experiment}")
    lower = text.lower()
    if contains_any(lower, ["wilson", "hairpin", "reflection positivity", "reflection-positive", "os positivity", "os-positive", "schur", "boundary ope"]):
        if contains_any(lower, ["schur", "h and k", "h,k", "php", "1^perp", "11^*", "rank-one"]):
            when_to_stop = (
                "Stop or quarantine this Wilson/OS tangent-cone branch only after the locked reflected-hairpin boundary OPE "
                "calculation has been attempted for the minimal three- or four-observable block, with diagonal normalization, "
                "the quotient projection P=I-11^*/n, and the Schur-corrected form \\Omega_2=P(K-n^{-2}H11^*HP)P explicitly evaluated; "
                "quarantine if H,K cannot be defined as same-theory Wilson OPE data with controlled collar remainders, or if PHP and \\Omega_2 "
                "are nonnegative on every stated zero-sum/null-vector test so the proposed finite obstruction disappears."
            )
            guard = (
                "Do not stop before deriving the concrete H and K tensors for the shared-footprint Wilson hairpins, applying the "
                "P=I-11^*/n quotient normalization, testing the zero-sum vector and triangle/null-space vectors, and recording whether the "
                "result promotes a finite OS-positivity falsifier, forces an OPE repair, backtracks the observable family, or quarantines the branch."
            )
            do_not_stop_if = [
                "The three-hairpin or four-hairpin boundary OPE coefficients H and K have not yet been computed in the same Wilson observable algebra.",
                "The rank-one normalization correction n^{-2}PH11^*HP has not yet been applied before testing the second-order form.",
                "Only diagonal or one-body Wilson renormalizations have been removed, but the mixed boundary coefficient has not yet been tested.",
                "No zero-sum, triangle, or ker(PHP) vector has been evaluated against PHP and \\Omega_2.",
                "The remaining blocker is a named collar-remainder or reflection-plane footprint estimate rather than a loss of target relevance.",
                "A negative Schur-corrected value would still decide the branch by producing a same-theory finite OS-positivity obstruction.",
            ]
            stop_criteria = [
                "The locked reflected-hairpin OPE calculation gives same-theory H,K with controlled remainders and all tested quotient vectors make PHP and \\Omega_2 nonnegative.",
                "After diagonal normalization and quotient projection, the candidate negative direction is shown to be a one-body renormalization artifact rather than a mixed Wilson boundary term.",
                "H,K cannot be extracted from gauge-invariant reflected Wilson observables with a common reflection-plane footprint after a named repair of the observable family.",
                "The required collar-remainder estimate cannot be localized into a smaller boundary OPE obligation and instead becomes an untyped continuum assumption.",
                "The finite matrix test no longer bears on OS positivity of the reconstructed same-theory Hilbert space.",
            ]
        else:
            when_to_stop = (
                "Stop or quarantine this Wilson/reflection-positivity branch only after the named Wilson observable family, reflected Gram block, "
                "quotient space, and finite positivity test have all been specified and the calculation either becomes nonnegative in the same theory "
                "or loses its controlled Wilson-source object."
            )
            guard = (
                "Do not stop before the Wilson observable block, reflection map, quotient projection, and sign/positivity test have been written down "
                "as concrete mathematical objects with a same-theory validation handoff."
            )
            do_not_stop_if = [
                "The reflected Wilson Gram block has not yet been defined.",
                "The quotient or null direction has not yet been identified.",
                "A concrete sign, determinant, or positivity test remains unrun.",
                "The branch still touches OS reconstruction through gauge-invariant observables.",
            ]
            stop_criteria = [
                "The reflected Wilson block is fully specified and all quotient positivity tests are nonnegative under the stated assumptions.",
                "The branch cannot keep the source object inside the gauge-invariant Wilson algebra.",
                "The proposed finite test is shown not to bear on OS positivity or reconstruction.",
            ]
        return {
            "when_to_stop": when_to_stop,
            "premature_stop_guard": guard,
            "do_not_stop_if": do_not_stop_if,
            "stop_criteria": stop_criteria,
        }
    if contains_any(lower, ["hamiltonian", "spectral", "mass gap", "hilbert", "vacuum"]):
        return {
            "when_to_stop": (
                "Stop or quarantine this spectral-gap branch only after the physical Hilbert space, vacuum vector, Hamiltonian generator, "
                "gauge-invariant excitation sector, and lower-bound witness have been typed; quarantine if the route assumes the Hilbert space or "
                "gap it was supposed to reconstruct, or if no dense excitation sector can be connected to the target theory."
            ),
            "premature_stop_guard": (
                "Do not stop before checking whether the missing step is specifically OS reconstruction, excitation-density, self-adjoint generator control, "
                "or a lower spectral-bound estimate, because each failure points to a different repair."
            ),
            "do_not_stop_if": [
                "The blocker is a named reconstruction premise rather than a false spectral claim.",
                "Gauge-invariant observables may still generate a dense non-vacuum sector.",
                "A Euclidean decay estimate can still be translated into a Hamiltonian spectral statement.",
            ],
            "stop_criteria": [
                "The route postulates the physical Hilbert space, vacuum, or spectral gap instead of deriving it.",
                "No gauge-invariant observable sector can be connected to the alleged excitation witness.",
                "The lower-bound estimate applies only at fixed cutoff or finite volume with no uniform bridge obligation.",
            ],
        }
    if contains_any(lower, ["balaban", "rg", "renormalization", "continuum", "cutoff"]):
        return {
            "when_to_stop": (
                "Stop or quarantine this RG/continuum branch only after the scale variables, cutoff-uniform estimates, observable transfer map, "
                "and reconstruction handoff are explicit; quarantine if the construction pressure never yields a same-theory observable or spectral witness."
            ),
            "premature_stop_guard": (
                "Do not stop before separating the scale-local estimate, its cutoff-uniform version, and the observable/reconstruction transfer it is meant to support."
            ),
            "do_not_stop_if": [
                "The route still localizes a cutoff-uniform estimate needed by a bridge lemma.",
                "The observable transfer from regulated to continuum theory has a named repair.",
                "The RG step changes a concrete construction premise rather than only restating route optimism.",
            ],
            "stop_criteria": [
                "The available estimates remain fixed-cutoff or finite-volume with no uniform upgrade path.",
                "No same-theory observable or reconstruction witness is produced by the RG construction.",
                "The branch can no longer name which continuum premise it changes.",
            ],
        }
    fallback_target = clean_text(experiment) or "the named next analysis"
    return {
        "when_to_stop": (
            f"Stop or quarantine this branch only after {fallback_target} has been rewritten as a named source object, target object, "
            "mathematical test, and validation handoff, and that concrete test either fails to change any target commitment or is shown to solve a proxy problem."
        ),
        "premature_stop_guard": (
            f"Do not stop before {fallback_target} has produced a concrete equation, obstruction, transfer certificate, or backtrack reason tied to the active target."
        ),
        "do_not_stop_if": [
            "A named equation, falsifier, or transfer certificate remains untested.",
            "The latest failure sharpened a specific assumption, regime, source object, or target object.",
            "A smaller same-target calculation can still decide promotion, repair, backtrack, or quarantine.",
        ],
        "stop_criteria": [
            "The concrete test fails to change a target commitment after a named sharpening attempt.",
            "The branch cannot name a same-target source object and target object.",
            "The remaining work is only a restatement or background search with no decision payoff.",
        ],
    }


def branch_continuation_profile(score: int, combined: str, reasons: list[str], experiment: str = "", target_id: str = "") -> dict[str, Any]:
    concrete_decision_test = contains_any(combined, ["det(", "determinant", "minor", "negative", "counterexample", "falsifier", "holonomy", "test", "compute", "construct", "extract", "evaluate"])
    target_bridge = contains_any(combined, ["same-theory", "same theory", "os positivity", "os-positive", "reflection positivity", "reflection-positive", "schwinger", "hilbert", "spectral", "mass gap", "continuum", "gauge", "wilson", "observable"])
    broad_or_vague = contains_any(combined, ["certify the weakest condition", "weakest condition", "analogy", "analog"])
    controls = domain_specific_branch_controls(combined, experiment, target_id=target_id)
    if score >= 75:
        decision = "continue_run_next"
        reason = "The item has high payoff and a concrete decision test; stopping now would be premature."
    elif score >= 55:
        decision = "adapt_then_run"
        reason = "The item remains target-linked but needs tighter payoff criteria before consuming a long run."
    elif concrete_decision_test or target_bridge:
        decision = "backtrack_to_sharpen"
        reason = "The branch still touches a relevant object, but the next experiment must be narrowed before continuation."
    elif ("analog" in combined or "analogy" in combined) and not target_bridge:
        decision = "quarantine_candidate"
        reason = "The item appears analogy-driven without a same-theory target bridge; keep it out of active budget unless transfer is certified."
    elif broad_or_vague:
        decision = "watch_archive_until_sharpened"
        reason = "The queue item is too broad or analogy-like for active budget, but it may be rescued by a sharper formulation."
    else:
        decision = "stop_candidate_after_repeat_low_payoff"
        reason = "The item has low visible payoff and no concrete decision test; stop only after repeated low-payoff evaluations."
    if not reasons:
        reason += " Its current justification is also under-specified."
    return {
        "branch_continuation_decision": decision,
        "branch_continuation_reason": reason,
        "premature_stop_guard": controls["premature_stop_guard"],
        "premature_stop_guard_html": render_math_prose_html(controls["premature_stop_guard"]),
        "do_not_stop_if": controls["do_not_stop_if"],
        "do_not_stop_if_html": [render_math_prose_html(item) for item in controls["do_not_stop_if"]],
        "stop_criteria": controls["stop_criteria"],
        "stop_criteria_html": [render_math_prose_html(item) for item in controls["stop_criteria"]],
        "when_to_stop": controls["when_to_stop"],
        "when_to_stop_html": render_math_prose_html(controls["when_to_stop"]),
    }


def global_problem_contribution(cycle: dict[str, Any], profile: dict[str, Any], target_id: str = "") -> str:
    text = clean_text(
        " ".join(
            [
                cycle.get("branch_title", ""),
                cycle.get("mathematical_learning", ""),
                cycle.get("blocking_gap", ""),
                cycle.get("next_experiment", ""),
                " ".join(cycle.get("falsifiers", [])),
            ]
        )
    )
    lower_text = text.lower()
    if target_id == "p-vs-np-target":
        contributions: list[str] = []
        if contains_any(lower_text, ["beta", "black-box", "substitution", "query"]):
            contributions.append("it identifies whether the transfer loses all-exponent strength through a positive target-query exponent beta")
        if contains_any(lower_text, ["mcsp", "mktp", "meta-complexity", "truth table"]):
            contributions.append("it tests whether a meta-complexity carrier gives a weaker source obligation than the original P vs NP/P-poly target")
        if contains_any(lower_text, ["padding", "projection", "sparse", "valid length"]):
            contributions.append("it separates true hardness magnification from projection or padding arguments that only move proof debt")
        if contains_any(lower_text, ["natural", "relativ", "algebr", "advice", "nonuniform", "p/poly"]):
            contributions.append("it keeps barrier status and nonuniform/advice leakage attached to the actual transfer theorem")
        if contains_any(lower_text, ["nonblackbox", "subpolynomial", "succinct", "proof-complexity", "local-consistency"]):
            contributions.append("it searches the remaining plausible escape route: nonblackbox or subpolynomial-interface carriers")
        if not contributions:
            contributions.append("it must earn its place by giving a source carrier, target class, transfer inequality, and falsifier")
        decision = clean_text(profile.get("branch_continuation_decision", ""))
        payoff = select_decisive_payoff_criterion(profile)
        suffix = f" The current branch-control decision is {decision}."
        if payoff:
            suffix += f" Payoff criterion: {payoff}"
        return "This move adds to the P vs NP problem because " + "; ".join(contributions[:4]) + "." + suffix
    contributions: list[str] = []
    if contains_any(lower_text, ["os positivity", "os-positive", "reflection positivity", "reflection-positive", "schwinger", "hilbert"]):
        contributions.append("it tests whether the Euclidean construction/reconstruction bridge is genuinely preserved")
    if contains_any(lower_text, ["continuum", "cutoff", "limit", "uniform", "rg", "collar", "boundary ope"]):
        contributions.append("it localizes which cutoff, collar, or boundary-OPE estimate must be uniform before a local calculation can count as continuum progress")
    if contains_any(lower_text, ["wilson", "gauge", "observable", "hairpin", "cumulant"]):
        contributions.append("it keeps the analysis inside the gauge-invariant Wilson observable algebra rather than drifting to a proxy problem")
    if contains_any(lower_text, ["det(", "determinant", "minor", "negative", "falsifier", "counterexample", "holonomy", "kernel", "schur"]):
        contributions.append("it supplies a finite obstruction test whose sign can force continuation, backtracking, or quarantine")
    if contains_any(lower_text, ["spectral", "mass gap", "hamiltonian", "decay"]):
        contributions.append("it ties the local construction work back to the spectral or mass-gap witness required by the target")
    if contains_any(lower_text, ["variable", "regime", "monotone", "convergence", "scale", "graph edge", "toy model"]):
        contributions.append("it can update the qualitative mechanistic graph with a typed relation, validity regime, or falsifier")
    if contains_any(lower_text, ["gedanken", "thought experiment", "counterfactual", "variant", "transfer guard"]):
        contributions.append("it can isolate a mechanism or transfer boundary before spending long-run proof budget")
    if not contributions:
        contributions.append("it must earn its place by naming the source object, target object, validation handoff, and falsifier it changes")
    decision = clean_text(profile.get("branch_continuation_decision", ""))
    payoff = select_decisive_payoff_criterion(profile)
    suffix = f" The current branch-control decision is {decision}."
    if payoff:
        suffix += f" Payoff criterion: {payoff}"
    return "This move adds to the global problem because " + "; ".join(contributions[:4]) + "." + suffix


def select_decisive_payoff_criterion(profile: dict[str, Any]) -> str:
    criteria = profile.get("payoff_criteria", [])
    if not isinstance(criteria, list):
        return ""
    fallback = ""
    for criterion in criteria:
        text = clean_text(criterion.get("text", "") if isinstance(criterion, dict) else criterion)
        if not text:
            continue
        if not fallback:
            fallback = text
        lowered = text.lower()
        if lowered.startswith("control gate:"):
            continue
        if "before claiming progress" in lowered:
            continue
        return text
    return fallback


def story_control_fields(cycle: dict[str, Any], target_id: str = "") -> dict[str, Any]:
    profile = queue_payoff_profile(cycle, target_id=target_id)
    stop_criteria = [clean_text(item).rstrip(".") for item in profile.get("stop_criteria", []) if clean_text(item)]
    do_not_stop_if = [clean_text(item) for item in profile.get("do_not_stop_if", []) if clean_text(item)]
    when_to_stop = clean_text(profile.get("when_to_stop")) or (
        "Stop or quarantine this branch only when "
        + (stop_criteria[0][0].lower() + stop_criteria[0][1:] if stop_criteria else "a named same-target calculation fails to change any target commitment")
    )
    contribution = global_problem_contribution(cycle, profile, target_id=target_id)
    return {
        "when_to_stop": when_to_stop,
        "when_to_stop_html": render_math_prose_html(when_to_stop),
        "global_problem_contribution": contribution,
        "global_problem_contribution_html": render_math_prose_html(contribution),
        "premature_stop_guard": profile.get("premature_stop_guard", ""),
        "premature_stop_guard_html": profile.get("premature_stop_guard_html", ""),
        "do_not_stop_if": do_not_stop_if[:3],
        "do_not_stop_if_html": profile.get("do_not_stop_if_html", [])[:3],
        "stop_criteria": stop_criteria[:3],
        "stop_criteria_html": profile.get("stop_criteria_html", [])[:3],
        "payoff_criteria": profile.get("payoff_criteria", []),
        "required_skills": profile.get("required_skills", []),
        "branch_continuation_decision": profile.get("branch_continuation_decision", ""),
        "branch_continuation_reason": profile.get("branch_continuation_reason", ""),
        "priority_score": profile.get("priority_score", 0),
        "priority_band": profile.get("priority_band", ""),
    }


def build_ranked_next_experiment_queue(
    cycles: list[dict[str, Any]],
    gedanken_report: dict[str, Any] | None = None,
    *,
    minimum_cycle: int = 0,
    strategy_judge: dict[str, Any] | None = None,
    target_id: str = "",
    proof_delivery_queue: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    ranked = []
    if target_id == "p-vs-np-target":
        ranked.extend(proof_delivery_queue_items(proof_delivery_queue or {}, minimum_cycle=minimum_cycle))
    if target_id == "yang-mills-existence-and-mass-gap-target":
        ranked.extend(build_paper_argument_priority_items(cycles, strategy_judge or {}, minimum_cycle=minimum_cycle))
        decisive_item = build_decisive_next_move_item(cycles, strategy_judge or {}, minimum_cycle=minimum_cycle)
        if decisive_item:
            ranked.append(decisive_item)
    for index, cycle in enumerate(cycles):
        if minimum_cycle and cycle_number(cycle) < minimum_cycle:
            continue
        next_experiment = clean_text(cycle.get("next_experiment", ""))
        if not next_experiment:
            continue
        profile = queue_payoff_profile(cycle, target_id=target_id)
        ranked.append(
            {
                "cycle_id": cycle.get("cycle_id", ""),
                "cycle_number": cycle_number(cycle),
                "branch_title": cycle.get("branch_title", ""),
                "engine": cycle.get("engine", ""),
                "attempt": cycle.get("api_attempt") or cycle.get("codex_attempt") or "not_recorded",
                "job_id": cycle.get("job_id", ""),
                "queue_source": "cycle",
                "next_experiment": next_experiment,
                "next_experiment_html": render_math_prose_html(next_experiment),
                "original_queue_index": index + 1,
                **profile,
            }
        )
    if gedanken_report:
        base_index = len(ranked)
        for offset, item in enumerate(gedanken_queue_items(gedanken_report, minimum_cycle=minimum_cycle), start=1):
            profile = gedanken_payoff_profile(item)
            ranked.append(
                {
                    "cycle_id": item.get("cycle_id", ""),
                    "cycle_number": item.get("cycle_number", 0),
                    "branch_title": item.get("branch_title", ""),
                    "engine": item.get("engine", "gedanken_experiment"),
                    "attempt": item.get("attempt", "conceptual_probe"),
                    "job_id": item.get("job_id", ""),
                    "queue_source": "gedanken",
                    "packet_id": item.get("packet_id", ""),
                    "situation_title": item.get("situation_title", ""),
                    "transfer_verdict": item.get("transfer_verdict", ""),
                    "success_criterion": item.get("success_criterion", ""),
                    "failure_or_demotion_criterion": item.get("failure_or_demotion_criterion", ""),
                    "next_experiment": item.get("next_experiment", ""),
                    "next_experiment_html": item.get("next_experiment_html", ""),
                    "original_queue_index": base_index + offset,
                    **profile,
                }
            )
    ranked.sort(key=lambda item: (-int(item["priority_score"]), -int(item["cycle_number"]), item["original_queue_index"]))
    for rank, item in enumerate(ranked, start=1):
        item["rank"] = rank
    return ranked


def build_storyline(cycles: list[dict[str, Any]], start_cycle: int | None = None, target_id: str = "") -> dict[str, Any]:
    beats = []
    for cycle in cycles:
        beats.append(
            {
                "cycle_id": cycle.get("cycle_id", ""),
                "branch_title": cycle.get("branch_title", ""),
                "engine": cycle.get("engine", ""),
                "attempt": cycle.get("api_attempt") or cycle.get("codex_attempt") or "not_recorded",
                "job_id": cycle.get("job_id", ""),
                "learning": cycle.get("mathematical_learning", ""),
                "learning_html": cycle.get("mathematical_learning_html", ""),
                "blocking_gap": cycle.get("blocking_gap", ""),
                "blocking_gap_html": cycle.get("blocking_gap_html", ""),
                "next_experiment": cycle.get("next_experiment", ""),
                "next_experiment_html": cycle.get("next_experiment_html", ""),
                **story_control_fields(cycle, target_id=target_id),
            }
        )
    first = beats[0]["cycle_id"] if beats else ""
    last = beats[-1]["cycle_id"] if beats else ""
    if start_cycle:
        headline = f"Content-specific physics story from cycle-{start_cycle:04d} through {last or 'the latest cycle'}."
    else:
        headline = f"Accumulated physics story across {len(beats)} valid research cycles."
    return {
        "start_cycle": start_cycle,
        "first_cycle_id": first,
        "last_cycle_id": last,
        "beat_count": len(beats),
        "headline": headline,
        "beats": beats,
    }


def load_qualitative_graph(target_id: str) -> dict[str, Any]:
    graph = load_optional_json(QUALITATIVE_GRAPH_DIR / f"{target_id}.json")
    if not graph:
        return {}
    output = dict(graph)
    edges = []
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        item = dict(edge)
        item["qualitative_behavior_html"] = render_math_prose_html(item.get("qualitative_behavior", ""))
        edges.append(item)
    output["edges"] = edges
    return output


def build_yang_mills_gedanken_experiments(cycles: list[dict[str, Any]]) -> dict[str, Any]:
    latest = cycles[-1] if cycles else {}
    cycle_id = clean_text(latest.get("cycle_id")) or "cycle-0000"
    branch_id = clean_text(latest.get("branch_id")) or clean_text(latest.get("branch_title")) or "yang-mills-wilson-os-route"
    packet_id = "gedanken.packet.ym-wilson-os-three-hairpin"
    situation_title = "Three-hairpin Wilson collar microscope"
    transfer_verdict = "needs_certificate"
    return {
        "target_id": "yang-mills-existence-and-mass-gap-target",
        "status": "fallback_target_specific_packet",
        "packets": [
            {
                "packet_id": packet_id,
                "created_utc": "",
                "need_decision": "design_now",
                "need_assessment": {
                    "decision": "design_now",
                    "criteria_met": [
                        "The active route has a concrete finite carrier: a reflected Wilson collar quotient with H,K coefficients.",
                        "The route has a sharp falsifier: failure of finite Schur-Feshbach positivity or failure of same-theory transfer.",
                    ],
                    "reason": "The thought experiment compresses the current Wilson/OS route into a minimal world where the decisive variables are visible.",
                },
                "situation": {
                    "title": situation_title,
                    "purpose": "Separate finite Schur-Feshbach obstruction content from broad continuum Yang-Mills rhetoric.",
                    "minimal_world": "Three reflected Wilson hairpin loops with a common reflection-plane footprint, fixed collar thickness, and a finite normalized OS quotient q_delta.",
                    "mathematical_carrier": "The finite matrices H and corrected K obtained from q_delta=J+delta H+delta^2 K+O(delta^3) after removing the vacuum direction.",
                    "controlled_contrast": "Hold the Wilson observable algebra and regulator fixed, then vary only the hairpin incidence geometry and endpoint-box contribution.",
                    "why_this_situation_is_informative": "It tests whether the route has a nontrivial finite positivity gate before any continuum or mass-gap claim is allowed.",
                    "non_claims": [
                        "It does not establish Yang-Mills existence.",
                        "It does not establish a spectral mass gap.",
                        "It does not replace the required uniform continuum transfer estimates.",
                    ],
                },
                "transfer_scope": {
                    "transfer_verdict": transfer_verdict,
                    "transfers": "A positive or negative finite Schur-Feshbach certificate transfers only to the local Wilson/OS route-control decision.",
                    "does_not_transfer": "It does not transfer directly to a continuum Schwinger-function construction or to the Clay mass-gap statement.",
                    "transfer_certificate_needed": "A same-theory certificate must show that H,K and the collar remainder come from the same regulated Wilson observable family uniformly in cutoff and volume.",
                },
                "followup_cycle_tasks": [
                    {
                        "action": "compute",
                        "description": "Instantiate the three-hairpin source object, compute or parameterize H and corrected K, and evaluate the finite Schur-Feshbach positivity gate.",
                        "packet_id": packet_id,
                        "situation_title": situation_title,
                        "transfer_verdict": transfer_verdict,
                        "success_criterion": "The cycle records an explicit finite matrix test with source object, target object, validity regime, and falsifier.",
                        "failure_or_demotion_criterion": "If H,K cannot be tied to the same Wilson regulator after one named repair, demote the route to a transfer-gap task.",
                        "required_skills": [
                            "finite-algebra-interface-builder",
                            "symbolic-matrix-probe",
                            "analytic-estimate-obligation-builder",
                        ],
                    },
                    {
                        "action": "rank_next_experiment",
                        "description": "Use the three-hairpin outcome to decide paper-note promotion, observable-family repair, backtracking, or quarantine.",
                        "packet_id": packet_id,
                        "situation_title": situation_title,
                        "transfer_verdict": transfer_verdict,
                        "success_criterion": "The ranked queue names the smallest honest claim, required transfer certificate, and stop condition.",
                        "failure_or_demotion_criterion": "If the queue repeats the Wilson/OS ladder without a new finite certificate or transfer obligation, quarantine as looping.",
                        "required_skills": [
                            "next-experiment-queue-ranker",
                            "paper-contribution-readiness-judge",
                            "main-problem-alignment-auditor",
                        ],
                    },
                ],
                "epistemic_status": "conceptual_probe",
                "originating_cycle_ids": [cycle_id],
                "originating_branch_ids": [branch_id],
                "graph_update_action": "none",
            }
        ],
    }


def load_gedanken_experiments(target_id: str = "", cycles: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    report = load_optional_json(GEDANKEN_REPORT)
    report_target = clean_text(report.get("target_id")) if isinstance(report, dict) else ""
    if report and (not report_target or report_target == target_id):
        return report
    if target_id == "yang-mills-existence-and-mass-gap-target":
        return build_yang_mills_gedanken_experiments(cycles or [])
    return {}


def load_parsimonious_probe_layer(target_id: str = "") -> dict[str, Any]:
    symbolic = load_optional_json(SYMBOLIC_MATRIX_PROBE)
    finite = load_optional_json(FINITE_ALGEBRA_INTERFACES)
    obligations = load_optional_json(ANALYTIC_OBLIGATIONS)
    numeric = load_optional_json(BOUNDED_NUMERIC_PROBE)
    for name, packet in [
        ("symbolic", symbolic),
        ("finite", finite),
        ("obligations", obligations),
        ("numeric", numeric),
    ]:
        packet_target = clean_text(packet.get("target_id")) if isinstance(packet, dict) else ""
        if packet_target and packet_target != target_id:
            if name == "symbolic":
                symbolic = {}
            elif name == "finite":
                finite = {}
            elif name == "obligations":
                obligations = {}
            elif name == "numeric":
                numeric = {}
    if target_id == "p-vs-np-target":
        finite_text = json.dumps(finite, ensure_ascii=False).lower() if finite else ""
        if any(term in finite_text for term in ["yang-mills", "wilson", "reflection positivity", "collar", "hairpin"]):
            finite = {}
    if not any([symbolic, finite, obligations, numeric]):
        return {}
    proof_safe = True
    if numeric:
        proof_safe = numeric.get("status") in {"calibration_only", "validated_probe", "falsifier_candidate"}
    return {
        "symbolic_matrix_probe": symbolic,
        "finite_algebra_interfaces": finite,
        "analytic_estimate_obligations": obligations,
        "bounded_numeric_probe": numeric,
        "proof_safe": proof_safe,
        "policy_path": "docs/research-methods/parsimonious-probe-policy.md",
        "equational_symbolic_policy_path": "docs/research-methods/equational-symbolic-reasoning.md",
    }


def load_scientific_contribution_monitor(target_id: str = "") -> dict[str, Any]:
    monitor = load_optional_json(SCIENTIFIC_CONTRIBUTION_MONITOR)
    if target_id and clean_text(monitor.get("target_id")) != target_id:
        from build_scientific_contribution_monitor import build_report as build_contribution_monitor

        monitor = build_contribution_monitor(target_id)
    if not monitor:
        return {}
    output = dict(monitor)
    candidates = []
    for candidate in monitor.get("candidates", []):
        if not isinstance(candidate, dict):
            continue
        item = dict(candidate)
        for field in [
            "smallest_honest_claim",
            "why_it_could_stand_alone",
            "branch_control_reason",
            "overclaim_boundary",
        ]:
            item[f"{field}_html"] = render_math_prose_html(item.get(field, ""))
        for field in ["good_enough_when", "continue_only_if", "stop_when", "validation_burden"]:
            item[f"{field}_html"] = [render_math_prose_html(row) for row in item.get(field, [])]
        implication = dict(item.get("implication_map", {}))
        for field in ["immediate_next_analysis", "route_level", "paper_level"]:
            implication[f"{field}_html"] = render_math_prose_html(implication.get(field, ""))
        item["implication_map"] = implication
        candidates.append(item)
    output["candidates"] = candidates
    if isinstance(monitor.get("top_candidate"), dict):
        top_id = monitor["top_candidate"].get("candidate_id")
        output["top_candidate"] = next((row for row in candidates if row.get("candidate_id") == top_id), candidates[0] if candidates else {})
    return output


def load_artifact_or_stop_control(target_id: str = "") -> dict[str, Any]:
    if clean_text(target_id) != "yang-mills-existence-and-mass-gap-target":
        return {}
    report = load_optional_json(YM_BLOCKER_SIGNATURE_REPORT)
    if clean_text(report.get("target_id")) != clean_text(target_id):
        return {}
    output = dict(report)
    output["latest_json"] = rel(YM_BLOCKER_SIGNATURE_REPORT)
    output["latest_html"] = rel(YM_BLOCKER_SIGNATURE_REPORT.with_suffix(".html"))
    return output


def load_target_literature_evolution(target_id: str = "") -> dict[str, Any]:
    scoped = TARGET_LITERATURE_EVOLUTION.parent / "targets" / target_id / "latest.json"
    report = load_optional_json(scoped) if target_id else {}
    report = report or load_optional_json(TARGET_LITERATURE_EVOLUTION)
    report_target = clean_text(report.get("target_id")) if isinstance(report, dict) else ""
    if target_id == "p-vs-np-target" and (not report or (report_target and report_target != target_id)):
        from build_target_literature_evolution import build_pvsnp_report

        report = build_pvsnp_report(
            {
                "target_id": target_id,
                "raw_goal": "P vs NP",
                "source": "target-scoped discovery marathon report",
            }
        )
    elif target_id == "yang-mills-existence-and-mass-gap-target" and (not report or (report_target and report_target != target_id)):
        from build_target_literature_evolution import build_yang_mills_report

        report = build_yang_mills_report(
            {
                "target_id": target_id,
                "raw_goal": "Yang-Mills existence and mass gap",
                "source": "target-scoped discovery marathon report",
            }
        )
    elif target_id and report_target and report_target != target_id:
        return {}
    if isinstance(report.get("problem_statement"), dict):
        statement = dict(report["problem_statement"])
        if statement.get("formal_shape"):
            statement["formal_shape"] = sanitize_latex_for_mathjax(statement["formal_shape"])
        report["problem_statement"] = statement
    return report


def latest_cycle_evidence(cycles: list[dict[str, Any]], limit: int = 3) -> list[dict[str, str]]:
    rows = []
    for cycle in cycles[-limit:]:
        rows.append(
            {
                "cycle_id": clean_text(cycle.get("cycle_id")),
                "branch_title": clean_text(cycle.get("branch_title")),
                "learning": clean_text(cycle.get("mathematical_learning")),
                "next_experiment": clean_text(cycle.get("next_experiment")),
            }
        )
    if rows:
        return rows
    return [
        {
            "cycle_id": "target-scoped-fallback",
            "branch_title": "YM Wilson/OS route",
            "learning": "Use finite Wilson/OS obstruction tests only as bounded evidence until same-theory continuum transfer is certified.",
            "next_experiment": "State the finite theorem, instantiate the three-hairpin Wilson collar block, and audit the transfer certificate.",
        }
    ]


def build_yang_mills_macro_strategy_fallback(cycles: list[dict[str, Any]]) -> dict[str, Any]:
    evidence = latest_cycle_evidence(cycles)
    strategies = [
        {
            "strategy_id": "macro.ym-wilson-os-finite-bridge",
            "title": "Wilson/OS finite bridge before continuum claims",
            "route_family": "Euclidean reconstruction / reflection positivity",
            "priority_score": 96,
            "macro_thesis": "Treat the Yang-Mills route as a same-theory Wilson observable bridge from finite reflected quotients to OS-positive Schwinger data.",
            "physics_picture": "Wilson hairpin observables near the reflection plane test whether reflection positivity can survive collar collapse before a Hilbert space is reconstructed.",
            "why_now": "The latest cycles have concentrated on H,K collar coefficients and Schur-Feshbach positivity gates.",
            "evidence_from_story": evidence,
            "what_to_compute_next": [
                "State the finite Schur-Feshbach theorem with explicit source object, target object, and validity regime.",
                "Compute or parameterize the three-hairpin Wilson collar H and corrected K matrices.",
                "Record whether the finite quotient gives a positive gate, a falsifier, or a same-theory transfer obligation.",
            ],
            "success_condition": [
                "The finite quotient criterion is exact under stated Wilson/OS assumptions.",
                "The source object remains inside the gauge-invariant Wilson observable algebra.",
                "The output is usable as a bounded paper-note contribution or route-control certificate.",
            ],
            "failure_or_pivot_condition": [
                "The H,K data cannot be tied to one regulated Wilson family.",
                "The Schur-Feshbach gate is vacuous or purely definitional.",
                "The collar remainder cannot be localized as a finite analytic obligation.",
            ],
            "linked_literature_refs": ["ref.os-1973-1975", "ref.wilson-1974", "ref.jaffe-witten-clay"],
            "active_skills": ["finite-algebra-interface-builder", "symbolic-matrix-probe", "analytic-estimate-obligation-builder"],
            "epistemic_status": "target_scoped_fallback_strategy",
        },
        {
            "strategy_id": "macro.ym-continuum-transfer-discipline",
            "title": "Continuum transfer discipline",
            "route_family": "Constructive QFT / regulator removal",
            "priority_score": 91,
            "macro_thesis": "Every finite Wilson result must declare the cutoff, volume, collar parameter, and uniform estimate needed for the continuum Yang-Mills handoff.",
            "physics_picture": "Asymptotic freedom and lattice regularization motivate the UV side, but the continuum Schwinger functions must keep gauge invariance, reflection positivity, and nontriviality.",
            "why_now": "Repeated cycles have isolated uniform collar and endpoint-box estimates as the bottleneck.",
            "evidence_from_story": evidence,
            "what_to_compute_next": [
                "Name the exact cutoff/volume topology for each finite quotient claim.",
                "Separate fixed-regulator statements from uniform continuum-transfer statements.",
                "Attach analytic estimate obligations to every promoted finite theorem.",
            ],
            "success_condition": [
                "The finite result states what remains bounded as the regulator is removed.",
                "The same Wilson observable family carries the source and target objects.",
                "The continuum handoff avoids changing the theory or collapsing to a trivial limit.",
            ],
            "failure_or_pivot_condition": [
                "Constants degenerate in the cutoff or infinite-volume limit.",
                "The source object becomes a proxy outside Yang-Mills observables.",
                "The argument relies on an unstated continuum compactness assumption.",
            ],
            "linked_literature_refs": ["ref.gross-wilczek-1973", "ref.politzer-1973", "ref.balaban-1985"],
            "active_skills": ["target-literature-evolution-narrator", "prior-art-importer", "abducer-obligation-gatekeeper"],
            "epistemic_status": "target_scoped_fallback_strategy",
        },
        {
            "strategy_id": "macro.ym-reconstruction-before-gap",
            "title": "Reconstruction before spectral gap",
            "route_family": "OS reconstruction / Hamiltonian witness",
            "priority_score": 86,
            "macro_thesis": "A spectral gap claim is meaningful only after Schwinger functions reconstruct a Hilbert space, vacuum, Hamiltonian, and gauge-invariant excitation sector.",
            "physics_picture": "The mass gap is a Hilbert-space spectral statement; Euclidean decay can support it only through a valid OS reconstruction bridge.",
            "why_now": "The marathon has generated finite positivity gates, but the reconstructed Hilbert-space object remains downstream.",
            "evidence_from_story": evidence,
            "what_to_compute_next": [
                "Maintain a premise ledger for Hilbert space, vacuum, Hamiltonian, and non-vacuum observable density.",
                "Translate any Euclidean decay estimate into a spectral statement only after reconstruction premises are explicit.",
                "Reject gap language that does not name the reconstructed same-theory object.",
            ],
            "success_condition": [
                "The Schwinger-function construction satisfies OS reconstruction hypotheses.",
                "Gauge-invariant observables generate the relevant non-vacuum sector.",
                "A positive spectral gap witness is stated in the reconstructed theory.",
            ],
            "failure_or_pivot_condition": [
                "The Hamiltonian is postulated rather than reconstructed.",
                "The decay estimate applies only to a non-determining observable family.",
                "The claimed gap belongs to a regulator model rather than continuum Yang-Mills.",
            ],
            "linked_literature_refs": ["ref.streater-wightman-1964", "ref.os-1973-1975", "ref.jaffe-witten-clay"],
            "active_skills": ["kb-proof-sketcher", "hamiltonian-gap-derivation", "entailment-gap-auditor"],
            "epistemic_status": "target_scoped_fallback_strategy",
        },
        {
            "strategy_id": "macro.ym-publishable-finite-obstruction",
            "title": "Publishable finite obstruction science",
            "route_family": "Finite algebra / falsifier-driven discovery",
            "priority_score": 82,
            "macro_thesis": "A sharp finite Wilson/OS obstruction can have publication value if it changes route understanding without pretending to solve the full problem.",
            "physics_picture": "A finite reflected Wilson matrix acts as a diagnostic shadow of the OS inner product; its determinant, tangent cone, and Schur complement expose real route tension.",
            "why_now": "The contribution-control workflow asks for bounded publication consolidation once a local subgoal reaches critical mass.",
            "evidence_from_story": evidence,
            "what_to_compute_next": [
                "Write the smallest honest theorem statement for the finite obstruction.",
                "Compare it against reflection positivity, Wilson-loop, and constructive-QFT prior art.",
                "Package assumptions, falsifiers, limitations, and next transfer obligations as a scoped note.",
            ],
            "success_condition": [
                "The result is non-definitional and mathematically exact under explicit assumptions.",
                "The novelty boundary is checked against nearby literature.",
                "The paper note explains how the result changes understanding of the YM route.",
            ],
            "failure_or_pivot_condition": [
                "The criterion is already standard prior art.",
                "The finite carrier cannot be connected to Yang-Mills observables even diagnostically.",
                "The result remains a fragmented report artifact rather than a reusable theorem object.",
            ],
            "linked_literature_refs": ["ref.os-1973-1975", "ref.wilson-1974", "ref.douglas-2004"],
            "active_skills": ["scientific-contribution-detector", "contribution-value-assessor", "scientific-contribution-paper-handoff"],
            "epistemic_status": "target_scoped_fallback_strategy",
        },
    ]
    for index, strategy in enumerate(strategies, start=1):
        strategy["rank"] = index
    return {
        "version": 1,
        "generated_utc": "",
        "target_id": "yang-mills-existence-and-mass-gap-target",
        "headline": "Current macro strategy: certify or falsify the Wilson/OS bridge before making spectral-gap claims.",
        "strategy_status": "target_scoped_macro_strategy_synthesis",
        "physics_language_standard": "Strategies must speak in terms of Yang-Mills, Wilson observables, Schwinger functions, reflection positivity, continuum limits, reconstructed Hilbert space, and spectral gap witnesses.",
        "story_basis": {
            "research_cycle_count": len(cycles),
            "latest_cycle_id": clean_text(cycles[-1].get("cycle_id")) if cycles else "",
            "dominant_branch": clean_text(cycles[-1].get("branch_title")) if cycles else "",
        },
        "macro_strategies": strategies,
        "recommended_next_posture": {
            "primary": "Run the finite Wilson/OS bridge until it yields a theorem, worked example, transfer obligation, or falsifier.",
            "secondary": "Keep continuum transfer as the discipline on every finite result.",
            "handoff": "Package only bounded finite contributions whose novelty and same-theory boundary are explicit.",
            "avoid": "Do not promote spectral-gap language before reconstruction and observable-density premises are declared.",
        },
    }


def load_macro_strategy_report(target_id: str = "", cycles: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    scoped = MACRO_STRATEGY_REPORT.parent / "targets" / target_id / "latest.json"
    report = load_optional_json(scoped) if target_id else {}
    report = report or load_optional_json(MACRO_STRATEGY_REPORT)
    report_target = clean_text(report.get("target_id")) if isinstance(report, dict) else ""
    if target_id == "yang-mills-existence-and-mass-gap-target" and report_target and report_target != target_id:
        return build_yang_mills_macro_strategy_fallback(cycles or [])
    if target_id and report_target and report_target != target_id:
        return {}
    return report


def load_physics_math_interpretation(target_id: str = "") -> dict[str, Any]:
    report = load_optional_json(PHYSICS_MATH_INTERPRETATION)
    report_target = clean_text(report.get("target_id")) if isinstance(report, dict) else ""
    report_text = json.dumps(report, ensure_ascii=False).lower() if isinstance(report, dict) else ""
    if target_id == "p-vs-np-target" and (
        (report_target and report_target != target_id)
        or any(term in report_text for term in ["yang-mills", "wilson", "mass gap", "schwinger", "gauge-invariant"])
    ):
        return {}
    if report_target and report_target != target_id:
        return {}
    return report


def build_yang_mills_strategy_progression_judge(cycles: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(cycles)
    window_cycles = cycles[-10:]
    cycle_ids = [clean_text(cycle.get("cycle_id")) for cycle in window_cycles]
    latest_cycle = cycle_ids[-1] if cycle_ids else ""
    return {
        "version": 1,
        "target_id": "yang-mills-existence-and-mass-gap-target",
        "judgement_id": "strategy-judge.ym-target-scoped-fallback",
        "judgement_cadence": {
            "policy": "Run after each completed 10 valid research cycles; use fallback when the global judge is scoped to another target.",
            "total_valid_research_cycles": total,
            "window_size": 10,
            "completed_ten_cycle_windows": total // 10,
            "next_boundary_cycle_count": ((total // 10) + 1) * 10,
            "judgement_due": total >= 10,
        },
        "window": {
            "window_research_cycle_count": min(10, total),
            "cycle_ids": cycle_ids,
            "latest_cycle_id": latest_cycle,
        },
        "generated_by_skills": [
            "progression-payoff-judge",
            "paper-contribution-readiness-judge",
            "main-problem-alignment-auditor",
        ],
        "evidence_sources": [
            "agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/latest.json",
            *[f"cycle:{cycle_id}" for cycle_id in cycle_ids],
        ],
        "current_strategy": {
            "strategy_id": "macro.ym-wilson-os-finite-bridge",
            "title": "finite Wilson/OS Schur-Feshbach bridge",
            "route_family": "Euclidean reconstruction / reflection positivity",
            "active_object": "source object: finite reflected Wilson collar quotient with H,K data; target object: OS-positive same-theory Schwinger bridge.",
            "macro_thesis": "Lock onto a bounded finite theorem plus worked three-hairpin Wilson collar calculation before reopening broad conceptual exploration.",
        },
        "progression_judgement": {
            "decision": "lock_in_for_bounded_validation",
            "payoff_potential": "high_if_nondefinitional",
            "progression_score": 84,
            "dimension_scores": {
                "conceptual_depth": 4,
                "explanatory_power": 4,
                "unification_power": 3,
                "publication_readiness": 3,
                "main_problem_alignment": 4,
            },
            "summary": "The latest YM window has enough exploratory critical mass to justify a bounded consolidation cycle around the finite Wilson/OS obstruction.",
            "contribution_pivot_invariant": "If the work only repeats the obstruction ladder, it is looping; continue only for a finite theorem, an H,K Wilson collar computation, or a same-theory transfer certificate that could become a scientific contribution.",
            "what_progressed": [
                {
                    "change": "The source object is now finite and explicit: a reflected Wilson collar quotient with H,K expansion data.",
                    "next_analysis": "State the finite theorem independently of the continuum theory.",
                },
                {
                    "change": "The target object is no longer generic positivity; it is a same-theory OS-positive Schwinger bridge.",
                    "next_analysis": "Name the transfer certificate and the uniform collar-remainder requirement.",
                },
            ],
            "what_did_not_progress": [
                {
                    "block": "The continuum mass-gap implication is still downstream of reconstruction, nontriviality, and spectral witness obligations.",
                    "next_analysis": "Do not claim spectral gap progress until the reconstructed Hilbert-space premises are explicit.",
                },
                {
                    "block": "The finite obstruction can still collapse into a definitional Schur complement unless the worked Wilson block changes route decisions.",
                    "next_analysis": "Require a nontrivial determinant, tangent-cone, or corrected-K gate.",
                },
            ],
            "next_decisive_test": "Produce the finite theorem plus three-hairpin H,K Wilson collar worked example, then decide promotion, repair, backtrack, or quarantine.",
            "when_to_stop": "Stop or demote after one bounded theorem pass and one worked-example repair if no finite certificate, transfer obligation, or falsifier emerges.",
            "do_not_stop_prematurely_if": "Do not stop while the source object, target object, and validation burden are explicit but the H,K Wilson collar computation remains unrun.",
        },
        "paper_contribution_readiness": {
            "candidate_title": "Finite Wilson/OS Schur-Feshbach obstruction criterion",
            "smallest_honest_claim": "A finite same-theory Wilson/OS quotient admits a Schur-Feshbach positivity gate whose three-hairpin instantiation can certify, falsify, or demote a proposed reflection-positivity bridge.",
            "readiness_level": "bounded_validation_needed",
            "dimension_scores": {
                "novelty": 3,
                "sharpness": 4,
                "coherent_narrative": 4,
                "proof_completeness": 2,
                "literature_positioning": 3,
            },
            "novelty_argument": "The value is not another positivity definition; it is the explicit use of finite Wilson H,K data to decide whether a reflected collar route has substance.",
            "main_problem_implication": "It changes understanding of the Yang-Mills route by identifying the exact local gate needed before continuum OS reconstruction and spectral gap work can matter.",
            "validation_burden": [
                "Prove the finite theorem with source object, target object, and validity regime.",
                "Compute or parameterize the minimal three-hairpin H,K matrices.",
                "Check prior art around reflection positivity, Wilson-loop Gram matrices, and Schur complement positivity.",
            ],
            "overclaim_boundary": "This is a bounded finite obstruction or route-control contribution, not a proof of Yang-Mills existence or mass gap.",
            "paper_skeleton": {
                "thesis": "A sharp finite positivity gate separates substantive Wilson/OS bridge work from definitional Schur-complement restatement.",
                "sections": ["finite theorem", "worked Wilson collar block", "same-theory transfer obligations", "limitations"],
            },
        },
        "main_problem_alignment": {
            "alignment_class": "bridge_aligned_but_not_solution",
            "target_commitments_touched": [
                "same-theory Euclidean Schwinger data",
                "reflection positivity",
                "continuum transfer",
                "nontriviality",
                "spectral gap only after reconstruction",
            ],
            "source_to_target_handoff": "Source object: finite reflected Wilson quotient with H,K data. Target object: same-theory OS-positive continuum Schwinger bridge.",
            "proxy_or_transfer_risk": "The finite theorem is aligned only if the Wilson observable algebra, regulator, and transfer estimates are not changed between source and target.",
            "alignment_gain": "The validation packet makes the main obstruction concrete enough to compute, falsify, or package.",
            "alignment_loss": "The packet does not by itself build the continuum Yang-Mills measure, Hilbert space, or spectral gap.",
            "repair_action": "If the first hairpin family degenerates, repair the observable geometry once while preserving the same regulator and transfer target.",
            "decision_effect": "Proceed with bounded publication consolidation, then return to conceptual exploration only after promotion, repair, backtrack, or quarantine is recorded.",
        },
        "strategy_payoff_table": [
            {
                "dimension": "conceptual_depth",
                "score": 4,
                "evidence": "The route localizes the tension between finite OS positivity and continuum transfer.",
            },
            {
                "dimension": "publication_readiness",
                "score": 3,
                "evidence": "The story has a coherent theorem-plus-example shape but still needs the actual H,K calculation.",
            },
            {
                "dimension": "alignment",
                "score": 4,
                "evidence": "The source object and target object are YM-specific and same-theory constrained.",
            },
        ],
        "validation_handoff": {
            "next_validator": "validate_discovery_marathon_report",
            "acceptance": "The report must expose source object, target object, payoff, alignment, contribution boundary, and validation burden.",
        },
        "epistemic_status": "target_scoped_fallback_judgement",
    }


def load_strategy_progression_judge(target_id: str = "", cycles: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    judge = load_optional_json(STRATEGY_PROGRESSION_JUDGE)
    judge_target = clean_text(judge.get("target_id")) if isinstance(judge, dict) else ""
    if target_id == "yang-mills-existence-and-mass-gap-target" and judge_target and judge_target != target_id:
        judge = build_yang_mills_strategy_progression_judge(cycles or [])
    elif target_id and judge_target and judge_target != target_id:
        return {}
    if not judge:
        return {}
    output = dict(judge)
    strategy = dict(output.get("current_strategy", {}))
    for field in ["active_object", "macro_thesis"]:
        strategy[f"{field}_html"] = render_math_prose_html(strategy.get(field, ""))
    output["current_strategy"] = strategy

    progress = dict(output.get("progression_judgement", {}))
    for field in ["summary", "contribution_pivot_invariant", "next_decisive_test", "when_to_stop", "do_not_stop_prematurely_if"]:
        progress[f"{field}_html"] = render_math_prose_html(progress.get(field, ""))
    for field in ["what_progressed", "what_did_not_progress"]:
        rows = []
        for row in progress.get(field, []):
            item = dict(row)
            for text_field in ["change", "block", "next_analysis"]:
                item[f"{text_field}_html"] = render_math_prose_html(item.get(text_field, ""))
            rows.append(item)
        progress[field] = rows
    output["progression_judgement"] = progress

    readiness = dict(output.get("paper_contribution_readiness", {}))
    for field in [
        "smallest_honest_claim",
        "novelty_argument",
        "explanatory_power",
        "main_problem_implication",
        "overclaim_boundary",
    ]:
        readiness[f"{field}_html"] = render_math_prose_html(readiness.get(field, ""))
    readiness["validation_burden_html"] = [render_math_prose_html(row) for row in readiness.get("validation_burden", [])]
    output["paper_contribution_readiness"] = readiness

    alignment = dict(output.get("main_problem_alignment", {}))
    for field in [
        "source_to_target_handoff",
        "proxy_or_transfer_risk",
        "alignment_gain",
        "alignment_loss",
        "repair_action",
        "decision_effect",
    ]:
        alignment[f"{field}_html"] = render_math_prose_html(alignment.get(field, ""))
    output["main_problem_alignment"] = alignment

    payoff_rows = []
    for row in output.get("strategy_payoff_table", []):
        item = dict(row)
        for field in ["payoff_read", "paper_contribution_path"]:
            item[f"{field}_html"] = render_math_prose_html(item.get(field, ""))
        payoff_rows.append(item)
    output["strategy_payoff_table"] = payoff_rows
    return output


def load_pvsnp_negative_tactics() -> dict[str, Any]:
    report = load_optional_json(PVSNP_NEGATIVE_TACTICS)
    if clean_text(report.get("target_id")) and clean_text(report.get("target_id")) != "p-vs-np-target":
        return {}
    output = dict(report)
    rows = []
    for row in report.get("recommendations", []) if isinstance(report.get("recommendations"), list) else []:
        if not isinstance(row, dict):
            continue
        item = dict(row)
        for field in [
            "reason_for_tactic",
            "exact_negation_or_method_class",
            "contradiction_carrier_or_no_go_family",
            "conflict_target",
            "next_validation_handoff",
            "paper_contribution_potential",
        ]:
            item[f"{field}_html"] = render_math_prose_html(item.get(field, ""))
        item["escape_conditions_html"] = [render_math_prose_html(value) for value in item.get("escape_conditions", [])]
        item["proof_obligations_html"] = [render_math_prose_html(value) for value in item.get("proof_obligations", [])]
        rows.append(item)
    output["recommendations"] = rows
    return output


def load_pvsnp_inference_quality() -> dict[str, Any]:
    report = load_optional_json(PVSNP_INFERENCE_QUALITY)
    if clean_text(report.get("target_id")) and clean_text(report.get("target_id")) != "p-vs-np-target":
        return {}
    output = dict(report)
    rows = []
    packets = report.get("packets", []) if isinstance(report.get("packets"), list) else []
    if not packets and isinstance(report.get("exemplar_packet"), dict):
        packets = [report["exemplar_packet"]]
    for row in packets:
        if not isinstance(row, dict):
            continue
        item = dict(row)
        for field in ["source_statement", "target_statement", "blocked_obligation"]:
            item[f"{field}_html"] = render_math_prose_html(item.get(field, ""))
        rows.append(item)
    output["packets"] = rows
    obligation = dict(report.get("current_packet_obligation", {})) if isinstance(report.get("current_packet_obligation"), dict) else {}
    obligation["required_packet_html"] = render_math_prose_html(obligation.get("required_packet", ""))
    obligation["minimum_fields_html"] = [render_math_prose_html(value) for value in obligation.get("minimum_fields", [])]
    output["current_packet_obligation"] = obligation
    return output


def load_pvsnp_proof_delivery_queue() -> dict[str, Any]:
    report = load_optional_json(PVSNP_PROOF_DELIVERY_QUEUE)
    if clean_text(report.get("target_id")) and clean_text(report.get("target_id")) != "p-vs-np-target":
        return {}
    return report


def load_pvsnp_formula_footprints_top_paper_criteria() -> dict[str, Any]:
    report = load_optional_json(PVSNP_FF_TOP_PAPER_CRITERIA)
    if not report:
        return {}
    output = {
        "status": clean_text(report.get("status")),
        "target_level": clean_text(report.get("target_level")),
        "decision_rule": report.get("decision_rule", {}),
        "optimization_order": report.get("optimization_order", []),
        "criteria": [],
    }
    for criterion in report.get("criteria", []) if isinstance(report.get("criteria"), list) else []:
        if not isinstance(criterion, dict):
            continue
        item = {
            "id": clean_text(criterion.get("id")),
            "name": clean_text(criterion.get("name")),
            "criterion_role": clean_text(criterion.get("criterion_role")),
            "critical": bool(criterion.get("critical")),
            "pass_evidence": criterion.get("pass_evidence", []),
            "fail_evidence": criterion.get("fail_evidence", []),
            "admission_rule": criterion.get("admission_rule", []),
        }
        for field in ["pass_evidence", "fail_evidence", "admission_rule"]:
            item[f"{field}_html"] = [render_math_prose_html(value) for value in item[field] if clean_text(value)]
        output["criteria"].append(item)
    return output


def load_pvsnp_formula_footprints_closure_gate() -> dict[str, Any]:
    report = load_optional_json(PVSNP_FF_CLOSURE_LATEST)
    if not report:
        return {}
    gate = report.get("top_paper_gate", {}) if isinstance(report.get("top_paper_gate"), dict) else {}
    final_claim_state = report.get("final_claim_state", {}) if isinstance(report.get("final_claim_state"), dict) else {}
    routes = report.get("remaining_upgrade_routes", [])
    if not isinstance(routes, list):
        routes = []
    criterion_status = clean_text(final_claim_state.get("carrier_independent_audit_upgrade_criterion"))
    self_auditing_status = clean_text(final_claim_state.get("self_auditing_rup_cdcl_instantiation"))
    append_only_status = clean_text(final_claim_state.get("append_only_self_auditing_rup_cdcl"))
    prefix_typed_status = clean_text(final_claim_state.get("prefix_typed_append_only_rup_cdcl"))
    prefix_witness_status = clean_text(final_claim_state.get("prefix_typed_rup_support_witness_necessity"))
    return {
        "result": clean_text(gate.get("result")),
        "narrative_weight_gate": clean_text(gate.get("narrative_weight_gate")),
        "coherence_pass_mode": clean_text(gate.get("coherence_pass_mode")),
        "coherence_fail_mode": clean_text(gate.get("coherence_fail_mode")),
        "carrier_independent_audit_upgrade_criterion": clean_text(
            gate.get("carrier_independent_audit_upgrade_criterion") or criterion_status
        ),
        "self_auditing_rup_cdcl_instantiation": clean_text(
            gate.get("self_auditing_rup_cdcl_instantiation") or self_auditing_status
        ),
        "append_only_self_auditing_rup_cdcl": clean_text(
            gate.get("append_only_self_auditing_rup_cdcl") or append_only_status
        ),
        "prefix_typed_append_only_rup_cdcl": clean_text(
            gate.get("prefix_typed_append_only_rup_cdcl") or prefix_typed_status
        ),
        "prefix_typed_rup_support_witness_necessity": clean_text(
            gate.get("prefix_typed_rup_support_witness_necessity") or prefix_witness_status
        ),
        "remaining_upgrade_routes": [clean_text(route) for route in routes if clean_text(route)],
        "revised_tex": clean_text(gate.get("revised_tex")),
        "revised_pdf": clean_text(gate.get("revised_pdf")),
        "novelty_delta_accounting": clean_text(
            gate.get("novelty_delta_accounting_artifact") or gate.get("novelty_delta_accounting")
        ),
    }


def load_result_subgoal_atlas(target_id: str) -> dict[str, Any]:
    atlas = load_optional_json(RESULT_SUBGOAL_ATLAS)
    if clean_text(atlas.get("target_id")) != target_id:
        from build_result_subgoal_atlas import build_atlas

        atlas = build_atlas(target_id)
    output = dict(atlas)
    results = []
    for result in atlas.get("results", []) if isinstance(atlas.get("results"), list) else []:
        if not isinstance(result, dict):
            continue
        item = dict(result)
        item["claim_html"] = render_math_prose_html(item.get("claim", ""))
        item["open_obligations_html"] = [render_math_prose_html(value) for value in item.get("open_obligations", [])]
        item["promotion_criteria_html"] = [render_math_prose_html(value) for value in item.get("promotion_criteria", [])]
        item["demotion_criteria_html"] = [render_math_prose_html(value) for value in item.get("demotion_criteria", [])]
        item["non_claims_html"] = [render_math_prose_html(value) for value in item.get("non_claims", [])]
        coords = dict(item.get("problem_space_coordinates", {}))
        coords["global_problem_role_html"] = render_math_prose_html(coords.get("global_problem_role", ""))
        item["problem_space_coordinates"] = coords
        results.append(item)
    output["results"] = results
    subgoals = []
    for subgoal in atlas.get("subgoals", []) if isinstance(atlas.get("subgoals"), list) else []:
        if not isinstance(subgoal, dict):
            continue
        item = dict(subgoal)
        item["open_obligations_html"] = [render_math_prose_html(value) for value in item.get("open_obligations", [])]
        subgoals.append(item)
    output["subgoals"] = subgoals
    return output


def load_problem_space_map(target_id: str) -> dict[str, Any]:
    report = load_optional_json(PROBLEM_SPACE_MAP)
    if clean_text(report.get("target_id")) != target_id:
        from build_problem_space_map import build_map
        from build_result_subgoal_atlas import build_atlas

        report = build_map(build_atlas(target_id), target_id)
    output = dict(report)
    nodes = []
    for node in report.get("nodes", []) if isinstance(report.get("nodes"), list) else []:
        if not isinstance(node, dict):
            continue
        item = dict(node)
        for field in ["achieved_summary", "next_achievement", "why_it_matters"]:
            item[f"{field}_html"] = render_math_prose_html(item.get(field, ""))
        item["open_obligations_html"] = [render_math_prose_html(value) for value in item.get("open_obligations", [])]
        nodes.append(item)
    output["nodes"] = nodes
    return output


def load_derivation_vault(target_id: str) -> dict[str, Any]:
    report = load_optional_json(DERIVATION_VAULT)
    if clean_text(report.get("target_id")) != target_id:
        from build_derivation_vault import build_vault
        from build_result_subgoal_atlas import build_atlas

        report = build_vault(build_atlas(target_id), target_id)
    output = dict(report)
    derivations = []
    for derivation in report.get("derivations", []) if isinstance(report.get("derivations"), list) else []:
        if not isinstance(derivation, dict):
            continue
        item = dict(derivation)
        item["claim_html"] = render_math_prose_html(item.get("claim", ""))
        item["definitions_html"] = [render_math_prose_html(value) for value in item.get("definitions", [])]
        item["assumptions_html"] = [render_math_prose_html(value) for value in item.get("assumptions", [])]
        item["proof_steps_html"] = [render_math_prose_html(value) for value in item.get("proof_steps", [])]
        item["unresolved_obligations_html"] = [render_math_prose_html(value) for value in item.get("unresolved_obligations", [])]
        item["non_claims_html"] = [render_math_prose_html(value) for value in item.get("non_claims", [])]
        equations = []
        for equation in item.get("equations", []) if isinstance(item.get("equations"), list) else []:
            if not isinstance(equation, dict):
                continue
            equations.append(
                {
                    **equation,
                    "latex_render": sanitize_latex_for_mathjax(equation.get("latex_render") or equation.get("latex", "")),
                    "valid_when_html": render_math_prose_html(equation.get("valid_when", "")),
                }
            )
        item["equations"] = equations
        derivations.append(item)
    output["derivations"] = derivations
    return output


def build_yang_mills_timeline_paper_fallback() -> dict[str, Any]:
    return {
        "paper_id": "ym-finite-wilson-os-schur-feshbach-note",
        "title": "Finite Wilson/OS Schur-Feshbach Obstruction Note",
        "artifacts": {
            "source_report": "agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/full_timeline.html"
        },
        "epistemic_status": "target_scoped_narrative_lock",
        "paper_narrative_goal_lock": {
            "lock_name": "ym_finite_wilson_os_schur_feshbach_goal",
            "status": "locked_for_bounded_validation",
            "subgoal_title": "Finite Wilson/OS Schur-Feshbach obstruction note",
            "coherent_narrative_thesis": "The coherent narrative is a finite, sharp Schur-Feshbach result: show how a reflected Wilson collar quotient exposes a nontrivial OS-positivity gate before any continuum Yang-Mills or spectral-gap claim is made.",
            "anti_infinite_exploration_rule": "Do not add more timeline detail unless it strengthens exactly one paper spine node: finite theorem, H,K Wilson collar worked example, same-theory transfer certificate, prior-art boundary, or limitation.",
            "narrative_spine": [
                "State the finite Wilson/OS quotient theorem with source object, target object, and validity regime.",
                "Prove the Schur-Feshbach tangent-cone and corrected-K positivity gate independently of Yang-Mills.",
                "Instantiate the H,K Wilson collar block for the minimal three-hairpin geometry.",
                "Explain what the finite result changes about the reflection-positivity route and what it does not prove.",
            ],
            "included_material_policy": [
                "Keep definitions, assumptions, equations, and proof steps needed for the finite theorem.",
                "Keep the H,K Wilson collar calculation and endpoint-box validity regime.",
                "Keep prior-art positioning for OS reflection positivity, Wilson loops, Schur complements, and constructive Yang-Mills.",
                "Keep explicit non-claims about continuum construction and spectral gap.",
            ],
            "excluded_detail_policy": [
                "Exclude chronological cycle detail that does not serve the coherent narrative.",
                "Exclude broad conceptual exploration unless it changes the theorem, calculation, transfer certificate, or limitation.",
                "Exclude any language implying a Yang-Mills mass-gap proof.",
            ],
            "decisive_next_work": [
                "Write the finite Schur-Feshbach theorem statement and proof skeleton.",
                "Compute or parameterize the minimal H,K Wilson collar matrices.",
                "Run the same-theory transfer and prior-art audits.",
            ],
            "stop_or_demote_when": [
                "Stop when the theorem is vacuous or only definitional after one repair.",
                "Demote when the H,K Wilson collar source object cannot be kept in the same regulated Wilson algebra.",
                "Quarantine when no finite certificate, falsifier, or transfer obligation appears after the bounded validation pass.",
            ],
            "do_not_stop_prematurely_if": [
                "The finite theorem is sharp but the H,K Wilson collar example is not yet evaluated.",
                "The worked example identifies a specific endpoint-box or collar-remainder obligation.",
                "The prior-art audit has not yet determined whether the finite obstruction is new.",
            ],
            "coherence_checks": [
                "Every section must support the finite Schur-Feshbach theorem, H,K Wilson collar computation, transfer certificate, or limitation.",
                "The paper must say how the result changes understanding of the YM route without claiming the full theorem.",
                "The conclusion must separate local finite contribution from continuum reconstruction and spectral-gap obligations.",
            ],
            "source_strategy_decision": "lock_in_for_bounded_validation",
            "source_payoff_potential": "high_if_nondefinitional",
            "source_readiness": "bounded_validation_needed",
            "epistemic_status": "narrative_goal_locked_validation_needed",
        },
    }


def load_timeline_paper_report(target_id: str = "") -> dict[str, Any]:
    paper = load_optional_json(TIMELINE_PAPER_REPORT)
    paper_target = clean_text(paper.get("target_id")) if isinstance(paper, dict) else ""
    if target_id == "yang-mills-existence-and-mass-gap-target" and paper_target and paper_target != target_id:
        paper = build_yang_mills_timeline_paper_fallback()
    elif target_id and paper_target and paper_target != target_id:
        return {}
    if not paper:
        return {}
    output = {
        "paper_id": clean_text(paper.get("paper_id")),
        "title": clean_text(paper.get("title")),
        "artifacts": paper.get("artifacts", {}),
        "epistemic_status": clean_text(paper.get("epistemic_status")),
        "paper_narrative_goal_lock": dict(paper.get("paper_narrative_goal_lock", {})),
    }
    lock = output["paper_narrative_goal_lock"]
    for field in [
        "subgoal_title",
        "coherent_narrative_thesis",
        "anti_infinite_exploration_rule",
        "source_strategy_decision",
        "source_payoff_potential",
        "source_readiness",
        "epistemic_status",
    ]:
        lock[f"{field}_html"] = render_math_prose_html(lock.get(field, ""))
    for field in [
        "narrative_spine",
        "included_material_policy",
        "excluded_detail_policy",
        "decisive_next_work",
        "stop_or_demote_when",
        "do_not_stop_prematurely_if",
        "coherence_checks",
    ]:
        lock[f"{field}_html"] = [render_math_prose_html(row) for row in lock.get(field, [])]
    output["paper_narrative_goal_lock"] = lock
    return output


def enrich_current_story(story: dict[str, Any]) -> dict[str, Any]:
    output = dict(story)
    for field in ["headline", "current_obstruction", "latest_learning", "next_experiment"]:
        output[f"{field}_html"] = render_math_prose_html(output.get(field, ""))
    return output


def enrich_branch_summaries(branches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for branch in branches:
        item = dict(branch)
        for field in ["controlled_interface", "latest_learning", "next_experiment"]:
            item[f"{field}_html"] = render_math_prose_html(item.get(field, ""))
        rows.append(item)
    return rows


def cycle_number(cycle: dict[str, Any]) -> int:
    raw = clean_text(cycle.get("cycle_id", ""))
    try:
        return int(raw.split("-")[-1])
    except ValueError:
        return 0


def timeline_start_cycle_for_target(target_id: str, cycles: list[dict[str, Any]], all_cycles: list[dict[str, Any]]) -> int:
    if target_id == "yang-mills-existence-and-mass-gap-target":
        return TIMELINE_START_CYCLE
    numbered_cycles = [cycle_number(cycle) for cycle in cycles if cycle_number(cycle) > 0]
    if not numbered_cycles:
        numbered_cycles = [cycle_number(cycle) for cycle in all_cycles if cycle_number(cycle) > 0]
    return min(numbered_cycles) if numbered_cycles else 1


def build_payload(report: dict[str, Any]) -> dict[str, Any]:
    jobs = load_job_summaries(clean_text(report.get("run_id")))
    job_by_cycle = cycle_job_index(jobs)
    _, run_state = load_run_state(report.get("run_id") or None)
    raw_cycles = load_cycles(run_state) if run_state else []
    cycles = [
        enrich_cycle(cycle, job_by_cycle)
        for cycle in raw_cycles
        if cycle.get("valid_as_research_cycle")
    ]
    all_cycles = [enrich_cycle(cycle, job_by_cycle) for cycle in raw_cycles]
    target_id = clean_text(report.get("target_id") or "yang-mills-existence-and-mass-gap-target")
    timeline_start_cycle = timeline_start_cycle_for_target(target_id, cycles, all_cycles)
    timeline_cycles = [cycle for cycle in all_cycles if cycle_number(cycle) >= timeline_start_cycle]
    timeline_research_cycles = [cycle for cycle in cycles if cycle_number(cycle) >= timeline_start_cycle]
    gedanken = load_gedanken_experiments(target_id, cycles)
    strategy_progression_judge = load_strategy_progression_judge(target_id, cycles)
    pvsnp_proof_delivery_queue = load_pvsnp_proof_delivery_queue() if target_id == "p-vs-np-target" else {}
    summary_analysis_control = story_control_fields(cycles[-1], target_id=target_id) if cycles else {}
    current_story = enrich_current_story(report.get("current_mathematical_story", {}))
    branch_summaries = enrich_branch_summaries(report.get("branch_summaries", []))
    return {
        "generated_utc": report.get("generated_utc", ""),
        "report": report,
        "jobs": jobs,
        "research_cycles": cycles,
        "all_cycles": all_cycles,
        "timeline_start_cycle": timeline_start_cycle,
        "timeline_cycles": timeline_cycles,
        "next_experiment_queue": build_next_experiment_queue(cycles, gedanken, strategy_judge=strategy_progression_judge, target_id=target_id, proof_delivery_queue=pvsnp_proof_delivery_queue),
        "timeline_next_experiment_queue": build_next_experiment_queue(cycles, gedanken, minimum_cycle=timeline_start_cycle, strategy_judge=strategy_progression_judge, target_id=target_id, proof_delivery_queue=pvsnp_proof_delivery_queue),
        "ranked_next_experiment_queue": build_ranked_next_experiment_queue(cycles, gedanken, strategy_judge=strategy_progression_judge, target_id=target_id, proof_delivery_queue=pvsnp_proof_delivery_queue),
        "timeline_ranked_next_experiment_queue": build_ranked_next_experiment_queue(cycles, gedanken, minimum_cycle=timeline_start_cycle, strategy_judge=strategy_progression_judge, target_id=target_id, proof_delivery_queue=pvsnp_proof_delivery_queue),
        "research_storyline": build_storyline(cycles, target_id=target_id),
        "timeline_storyline": build_storyline(timeline_research_cycles, timeline_start_cycle, target_id=target_id),
        "skill_dispatch_summary": build_skill_dispatch_summary(cycles),
        "qualitative_mechanistic_graph": load_qualitative_graph(target_id),
        "gedanken_experiments": gedanken,
        "parsimonious_probe_layer": load_parsimonious_probe_layer(target_id),
        "scientific_contribution_monitor": load_scientific_contribution_monitor(target_id),
        "target_literature_evolution": load_target_literature_evolution(target_id),
        "physics_math_interpretation": load_physics_math_interpretation(target_id),
        "macro_strategy_report": load_macro_strategy_report(target_id, cycles),
        "strategy_progression_judge": strategy_progression_judge,
        "pvsnp_negative_tactics": load_pvsnp_negative_tactics() if target_id == "p-vs-np-target" else {},
        "pvsnp_inference_quality": load_pvsnp_inference_quality() if target_id == "p-vs-np-target" else {},
        "pvsnp_proof_delivery_queue": pvsnp_proof_delivery_queue,
        "pvsnp_formula_footprints_top_paper_criteria": load_pvsnp_formula_footprints_top_paper_criteria() if target_id == "p-vs-np-target" else {},
        "pvsnp_formula_footprints_closure_gate": load_pvsnp_formula_footprints_closure_gate() if target_id == "p-vs-np-target" else {},
        "result_subgoal_atlas": load_result_subgoal_atlas(target_id),
        "problem_space_map": load_problem_space_map(target_id),
        "derivation_vault": load_derivation_vault(target_id),
        "timeline_paper_report": load_timeline_paper_report(target_id),
        "quality": quality_summary(cycles, jobs),
        "proof_depth_control_summary": report.get("proof_depth_control_summary", {}),
        "avenue_literature_gap_summary": report.get("avenue_literature_gap_summary", {}),
        "physical_relevance_impact_summary": report.get("physical_relevance_impact_summary", {}),
        "artifact_or_stop_control": load_artifact_or_stop_control(target_id),
        "artifact_or_stop_summary": report.get("artifact_or_stop_summary", {}),
        "failure_archaeology_summary": report.get("failure_archaeology_summary", {}),
        "visual_conceptualization_summary": report.get("visual_conceptualization_summary", {}),
        "current_story": current_story,
        "summary_analysis_control": {
            **summary_analysis_control,
            "next_experiment_html": cycles[-1].get("next_experiment_html", "") if cycles else "",
        },
        "branch_summaries": branch_summaries,
        "deep_reviews": report.get("deep_reviews", []),
    }


def embedded_mathjax() -> str:
    """Return the vendored MathJax component escaped for inline script use."""
    if not MATHJAX_TEX_SVG_ASSET.exists():
        raise SystemExit(f"missing vendored MathJax asset: {rel(MATHJAX_TEX_SVG_ASSET)}")
    return MATHJAX_TEX_SVG_ASSET.read_text(encoding="utf-8").replace("</script", "<\\/script")


def initialization_notice(payload: dict[str, Any]) -> str:
    """Keep the canonical initialization outcome visible above every report tab."""
    initialization = payload.get("report", {}).get("canonical_initialization") or {}
    if not initialization:
        return ""
    return '<p class="subtitle" role="status">' + html.escape(clean_text(initialization.get("summary"))) + '</p>'


def render_generic_target_html(payload: dict[str, Any], *, timeline_mode: bool = False) -> str:
    """Render a target-neutral report without Yang-Mills-specific tabs or source strings."""
    report = payload.get("report", {})
    target = html.escape(clean_text(report.get("target_id", "discovery-marathon")))
    generated = html.escape(clean_text(payload.get("generated_utc", "")))
    cycles = payload.get("timeline_cycles" if timeline_mode else "research_cycles", [])
    if not timeline_mode and not cycles:
        cycles = payload.get("research_cycles", [])
    quality = payload.get("quality", {})
    story = payload.get("current_story", {})
    branches = payload.get("branch_summaries", [])
    reviews = payload.get("deep_reviews", [])
    all_jobs = payload.get("jobs", [])
    target_id = clean_text(report.get("target_id", ""))
    from target_profiles import target_profile
    profile = target_profile(target_id)
    display_name = html.escape(profile["display_name"])
    strategy_label = html.escape(profile["strategy_tab_label"])
    target_job_tokens = {
        clean_text(report.get("run_id", "")),
        target_id.replace("-target", ""),
        target_id.replace("-", ""),
    }
    jobs = [
        job
        for job in all_jobs
        if any(token and token in clean_text(job.get("job_id", "")) for token in target_job_tokens)
    ]
    title = "Discovery Marathon Full Timeline" if timeline_mode else "Discovery Marathon Report"
    mathjax = embedded_mathjax()
    safe_report = {
        key: report.get(key)
        for key in [
            "version",
            "generated_utc",
            "purpose",
            "run_id",
            "target_id",
            "status",
            "cycle_count",
            "research_cycle_count",
            "synthetic_cycle_count",
            "wall_clock_budget_minutes",
            "cycle_minutes",
            "research_quality_summary",
            "avenue_literature_gap_summary",
            "physical_relevance_impact_summary",
            "failure_archaeology_summary",
            "visual_conceptualization_summary",
            "current_mathematical_story",
            "branch_summaries",
            "deep_reviews",
            "what_actually_changed",
            "canonical_initialization",
        ]
        if key in report
    }
    embedded_payload = json_for_script(
        {
            "generated_utc": payload.get("generated_utc", ""),
            "timeline_mode": timeline_mode,
            "timeline_start_cycle": payload.get("timeline_start_cycle", 1),
            "report": safe_report,
            "jobs": jobs,
            "research_cycles": payload.get("research_cycles", []),
            "all_cycles": payload.get("all_cycles", []),
            "timeline_cycles": payload.get("timeline_cycles", []),
            "next_experiment_queue": payload.get("next_experiment_queue", []),
            "timeline_next_experiment_queue": payload.get("timeline_next_experiment_queue", []),
            "ranked_next_experiment_queue": payload.get("ranked_next_experiment_queue", []),
            "timeline_ranked_next_experiment_queue": payload.get("timeline_ranked_next_experiment_queue", []),
            "research_storyline": payload.get("research_storyline", {}),
            "timeline_storyline": payload.get("timeline_storyline", {}),
            "skill_dispatch_summary": payload.get("skill_dispatch_summary", {}),
            "qualitative_mechanistic_graph": payload.get("qualitative_mechanistic_graph", {}),
            "gedanken_experiments": payload.get("gedanken_experiments", {}),
            "parsimonious_probe_layer": payload.get("parsimonious_probe_layer", {}),
            "scientific_contribution_monitor": payload.get("scientific_contribution_monitor", {}),
            "target_literature_evolution": payload.get("target_literature_evolution", {}),
            "physics_math_interpretation": payload.get("physics_math_interpretation", {}),
            "macro_strategy_report": payload.get("macro_strategy_report", {}),
            "strategy_progression_judge": payload.get("strategy_progression_judge", {}),
            "pvsnp_negative_tactics": payload.get("pvsnp_negative_tactics", {}),
            "pvsnp_inference_quality": payload.get("pvsnp_inference_quality", {}),
            "pvsnp_proof_delivery_queue": payload.get("pvsnp_proof_delivery_queue", {}),
            "pvsnp_formula_footprints_top_paper_criteria": payload.get("pvsnp_formula_footprints_top_paper_criteria", {}),
            "pvsnp_formula_footprints_closure_gate": payload.get("pvsnp_formula_footprints_closure_gate", {}),
            "result_subgoal_atlas": payload.get("result_subgoal_atlas", {}),
            "problem_space_map": payload.get("problem_space_map", {}),
            "derivation_vault": payload.get("derivation_vault", {}),
            "timeline_paper_report": payload.get("timeline_paper_report", {}),
            "artifact_or_stop_control": payload.get("artifact_or_stop_control", {}),
            "artifact_or_stop_summary": payload.get("artifact_or_stop_summary", {}),
            "summary_analysis_control": payload.get("summary_analysis_control", {}),
            "quality": quality,
            "proof_depth_control_summary": payload.get("proof_depth_control_summary", {}),
            "avenue_literature_gap_summary": payload.get("avenue_literature_gap_summary", {}),
            "physical_relevance_impact_summary": payload.get("physical_relevance_impact_summary", {}),
            "failure_archaeology_summary": payload.get("failure_archaeology_summary", {}),
            "visual_conceptualization_summary": payload.get("visual_conceptualization_summary", {}),
            "current_story": story,
            "branch_summaries": branches,
            "deep_reviews": reviews,
        }
    )

    def esc_text(value: Any) -> str:
        return html.escape(clean_text(value))

    def math_text(html_value: Any, fallback: Any = "") -> str:
        rendered = clean_text(html_value)
        if rendered:
            return rendered
        return render_math_prose_html(fallback)

    def chip(label: str, value: Any) -> str:
        return f'<div class="metric"><strong>{esc_text(value)}</strong><span>{esc_text(label)}</span></div>'

    def equations(cycle: dict[str, Any]) -> str:
        rows = []
        for eq in cycle.get("equations", [])[:5]:
            latex = sanitize_latex_for_mathjax(eq.get("latex_render") or eq.get("latex", ""))
            rows.append(
                "<li>"
                f"<strong>{esc_text(eq.get('label', 'equation'))}</strong>: "
                f"<div class=\"equation\">\\[{html.escape(latex, quote=False)}\\]</div>"
                f"<span class=\"muted\">Valid when: {render_math_prose_html(eq.get('valid_when', ''))}</span>"
                "</li>"
            )
        return "<ul>" + "".join(rows) + "</ul>" if rows else '<p class="muted">No equations recorded.</p>'

    def definitions_assumptions(cycle: dict[str, Any]) -> str:
        definitions = cycle.get("definitions", []) if isinstance(cycle.get("definitions"), list) else []
        assumptions = cycle.get("assumptions", []) if isinstance(cycle.get("assumptions"), list) else []
        if not definitions and not assumptions:
            return ""
        note = math_text(cycle.get("definition_assumption_elicitation_note_html"), cycle.get("definition_assumption_elicitation_note"))
        definition_items = "".join(
            f'<li>{math_text((cycle.get("definitions_html") or [])[idx] if idx < len(cycle.get("definitions_html") or []) else "", item)}</li>'
            for idx, item in enumerate(definitions[:6])
        )
        assumption_items = "".join(
            f'<li>{math_text((cycle.get("assumptions_html") or [])[idx] if idx < len(cycle.get("assumptions_html") or []) else "", item)}</li>'
            for idx, item in enumerate(assumptions[:6])
        )
        definition_block = f'<p><strong>Definitions:</strong></p><ul class="compact-list">{definition_items}</ul>' if definition_items else ""
        assumption_block = f'<p><strong>Assumptions:</strong></p><ul class="compact-list">{assumption_items}</ul>' if assumption_items else ""
        note_block = f'<p class="muted">{note}</p>' if note else ""
        return f"""
        <section class="definition-assumption-block">
          <h4>Definitions And Assumptions</h4>
          {note_block}
          {definition_block}
          {assumption_block}
        </section>
        """

    def cycle_card(cycle: dict[str, Any]) -> str:
        return f"""
        <article class="card api">
          <div class="row">
            <h3>{esc_text(cycle.get('cycle_id'))}</h3>
            <span class="pill good">{esc_text(cycle.get('engine') or 'engine?')}</span>
            <span class="pill info">{esc_text(cycle.get('research_seconds_elapsed'))}s</span>
          </div>
          <p><strong>Branch:</strong> {esc_text(cycle.get('branch_title'))}</p>
          <p><strong>Learning:</strong> {math_text(cycle.get('mathematical_learning_html'), cycle.get('mathematical_learning'))}</p>
          <p><strong>Blocking Gap:</strong> {math_text(cycle.get('blocking_gap_html'), cycle.get('blocking_gap'))}</p>
          <p><strong>Next Analysis:</strong> {math_text(cycle.get('next_experiment_html'), cycle.get('next_experiment'))}</p>
          <details>
            <summary>Equations And Falsifiers</summary>
            {definitions_assumptions(cycle)}
            {equations(cycle)}
            <ul>{''.join(f'<li>{math_text((cycle.get("falsifiers_html") or [])[idx] if idx < len(cycle.get("falsifiers_html") or []) else "", item)}</li>' for idx, item in enumerate(cycle.get('falsifiers', [])[:6]))}</ul>
          </details>
        </article>
        """

    branch_html = "".join(
        f"""
        <article class="card story">
          <div class="row"><h3>{esc_text(branch.get('title'))}</h3><span class="pill info">{esc_text(branch.get('status'))}</span></div>
          <p><strong>Controlled Interface:</strong> {esc_text(branch.get('controlled_interface'))}</p>
          <p><strong>Latest Learning:</strong> {render_math_prose_html(branch.get('latest_learning'))}</p>
          <p><strong>Next Analysis:</strong> {render_math_prose_html(branch.get('next_experiment'))}</p>
        </article>
        """
        for branch in branches
    )
    review_html = "".join(
        f"""
        <article class="card review">
          <h3>{esc_text(review.get('review_id'))}</h3>
          <p>{esc_text(review.get('summary'))}</p>
          <p><strong>Recommendation:</strong> {esc_text(review.get('recommendation'))}</p>
        </article>
        """
        for review in reviews
    )
    job_html = "".join(
        f"""
        <article class="card {'fail' if int(job.get('failed_cycle_attempts') or 0) else 'api'}">
          <div class="row"><h3>{esc_text(job.get('job_id'))}</h3><span class="pill info">{esc_text(job.get('status'))}</span></div>
          <p>{esc_text(job.get('completed_cycles'))} completed cycles; {esc_text(job.get('failed_cycle_attempts'))} operational failures.</p>
          <p class="muted">{esc_text(job.get('log_path'))}</p>
        </article>
        """
        for job in jobs[:8]
    )
    active_queue = payload.get("timeline_next_experiment_queue" if timeline_mode else "next_experiment_queue", [])
    ranked_queue = payload.get("timeline_ranked_next_experiment_queue" if timeline_mode else "ranked_next_experiment_queue", [])
    story_payload = payload.get("timeline_storyline" if timeline_mode else "research_storyline", {})
    story_beats = story_payload.get("beats", [])
    skill_summary = payload.get("skill_dispatch_summary", {})
    visual_summary = payload.get("visual_conceptualization_summary", {}) if isinstance(payload.get("visual_conceptualization_summary"), dict) else {}
    literature_summary = payload.get("avenue_literature_gap_summary", {}) if isinstance(payload.get("avenue_literature_gap_summary"), dict) else {}
    artifact_stop_report = payload.get("artifact_or_stop_control", {}) if isinstance(payload.get("artifact_or_stop_control"), dict) else {}
    artifact_stop_summary = payload.get("artifact_or_stop_summary", {}) if isinstance(payload.get("artifact_or_stop_summary"), dict) else {}

    def skill_pills(skills: list[Any], limit: int = 12) -> str:
        return " ".join(f'<span class="pill info">{esc_text(skill)}</span>' for skill in skills[:limit])

    def ranked_queue_html() -> str:
        rows = []
        for item in ranked_queue:
            criteria = item.get("payoff_criteria", [])
            rows.append(
                f"""
                <article class="card story">
                  <div class="row">
                    <h3>#{esc_text(item.get('rank'))} · {esc_text(item.get('cycle_id'))}</h3>
                    <span class="pill {'good' if item.get('priority_band') == 'high' else 'info'}">{esc_text(item.get('priority_band'))}</span>
                    <span class="pill info">{esc_text(item.get('engine'))}</span>
                  </div>
                  <p><strong>Analysis:</strong> {math_text(item.get('next_experiment_html'), item.get('next_experiment'))}</p>
                  <p><strong>Why target:</strong> {esc_text(item.get('why_target'))}</p>
                  <p><strong>Risk:</strong> {esc_text(item.get('risk'))}</p>
                  <p><strong>Branch control:</strong> {esc_text(item.get('branch_continuation_decision'))} · {esc_text(item.get('branch_continuation_reason'))}</p>
                  <p><strong>Payoff:</strong></p>
                  <ul>{''.join(f'<li>{math_text(c.get("html"), c.get("text"))}</li>' for c in criteria[:4] if isinstance(c, dict))}</ul>
                  <p><strong>Skills:</strong> {skill_pills(item.get('required_skills', []), 18)}</p>
                </article>
                """
            )
        return "".join(rows) or '<div class="empty">No ranked analyses are available for this target.</div>'

    def skill_dispatch_html() -> str:
        phases = skill_summary.get("phases", [])
        top_skills = skill_summary.get("top_skills", [])
        missing = skill_summary.get("missing_required_skills", [])
        conditional = skill_summary.get("queued_conditional_skills", [])
        handoffs = skill_summary.get("latest_validation_handoffs", [])
        return f"""
        <div class="quality">
          {chip('dispatch phases', skill_summary.get('phase_count', 0))}
          {chip('unique skills', skill_summary.get('invoked_skill_count', 0))}
          {chip('skill invocations', skill_summary.get('total_skill_invocations', 0))}
          {chip('missing required', len(missing))}
        </div>
        <h2>Most Used Skills</h2>
        <p>{' '.join(f'<span class="pill info">{esc_text(row.get("skill"))} · {esc_text(row.get("count"))}</span>' for row in top_skills[:28])}</p>
        <h2>Dispatch Phases</h2>
        {''.join(f'''
        <article class="card story">
          <div class="row"><h3>{esc_text(row.get("phase"))}</h3><span class="pill info">{esc_text(row.get("cycle_count"))} cycles</span><span class="pill info">{esc_text(row.get("latest_cycle_id"))}</span></div>
          <p>{esc_text(row.get("latest_validation_handoff"))}</p>
          <p>{' '.join(f'<span class="pill info">{esc_text(skill.get("skill"))} · {esc_text(skill.get("count"))}</span>' for skill in row.get("skills", [])[:18])}</p>
        </article>
        ''' for row in phases)}
        <h2>Conditional Skills Queued</h2>
        <ul>{''.join(f'<li><strong>{esc_text(item.get("cycle_id"))} · {esc_text(item.get("phase"))}</strong>: {esc_text(item.get("skill"))} — {esc_text(item.get("reason"))}</li>' for item in conditional[-24:])}</ul>
        <h2>Latest Validation Handoffs</h2>
        <ul>{''.join(f'<li><strong>{esc_text(item.get("cycle_id"))} · {esc_text(item.get("phase"))}</strong>: {esc_text(item.get("validation_handoff"))}</li>' for item in handoffs[-16:])}</ul>
        """

    def artifact_or_stop_html() -> str:
        control = artifact_stop_report.get("artifact_or_stop_control", {}) if isinstance(artifact_stop_report.get("artifact_or_stop_control"), dict) else {}
        signatures = artifact_stop_report.get("signatures", []) if isinstance(artifact_stop_report.get("signatures"), list) else []
        if not artifact_stop_report and not artifact_stop_summary:
            return '<div class="empty">No artifact-or-stop control is active for this target.</div>'
        signature_cards = []
        for row in signatures:
            evidence = "".join(
                f"<li><span class=\"muted\">{esc_text(item.get('cycle_id'))}</span> {esc_text(item.get('blocking_gap'))}</li>"
                for item in row.get("recent_evidence", [])
                if isinstance(item, dict)
            )
            signature_cards.append(
                f"""
                <article class="card story">
                  <div class="row">
                    <h3>{esc_text(row.get('blocker_signature'))}</h3>
                    <span class="pill {'fail' if row.get('blocker_kind') == 'artifact-blocked' else 'info'}">{esc_text(row.get('blocker_kind'))}</span>
                    <span class="pill warn">{esc_text(row.get('repetition_count', 0))} repeats</span>
                    <span class="pill info">{esc_text(row.get('proposed_mode_switch'))}</span>
                  </div>
                  <p>{esc_text(row.get('canonical_statement'))}</p>
                  <p><strong>Branches:</strong> {esc_text(row.get('branch_ids', []))}</p>
                  <p><strong>Missing artifacts:</strong> {esc_text(row.get('missing_artifacts', []))}</p>
                  <ul>{evidence}</ul>
                </article>
                """
            )
        return f"""
        <article class="card story {'fail' if artifact_stop_summary.get('broad_api_marathon_blocked') or control.get('broad_api_marathon_blocked') else ''}">
          <div class="row">
            <span class="pill fail">{esc_text(artifact_stop_summary.get('endpoint_mode') or control.get('next_endpoint_mode') or 'artifact_sprint_required')}</span>
            <span class="pill warn">{esc_text(artifact_stop_summary.get('endpoint_repetition_count', 0))} endpoint repeats</span>
            <span class="pill info">{esc_text(artifact_stop_summary.get('validator') or control.get('validator') or 'agentic/scripts/validate_artifact_or_stop_control.py')}</span>
          </div>
          <p><strong>Policy:</strong> {esc_text(artifact_stop_report.get('signature_policy') or artifact_stop_summary.get('gate_rule'))}</p>
          <p><strong>Broad endpoint API marathon blocked:</strong> {esc_text(artifact_stop_summary.get('broad_api_marathon_blocked') or control.get('broad_api_marathon_blocked') or False)}</p>
          <p><strong>Endpoint contract:</strong> <span class="muted">{esc_text(artifact_stop_summary.get('endpoint_contract') or control.get('endpoint_contract'))}</span></p>
          <p><strong>Endpoint pilot:</strong> <span class="muted">{esc_text(artifact_stop_summary.get('endpoint_pilot') or control.get('endpoint_pilot'))}</span></p>
          <p><strong>Demotion packet:</strong> <span class="muted">{esc_text(artifact_stop_summary.get('demotion_packet') or control.get('demotion_packet'))}</span></p>
          <p><strong>Blocker report:</strong> <span class="muted">{esc_text(artifact_stop_summary.get('latest_json') or artifact_stop_report.get('latest_json'))}</span></p>
        </article>
        {''.join(signature_cards)}
        """

    def contribution_html() -> str:
        if target_id != "p-vs-np-target":
            candidates = payload.get("scientific_contribution_monitor", {}).get("candidates", [])
            if not candidates:
                return '<div class="card story">No independently novel contribution is established for this run. Known-theorem reconstruction and worked checks are reported in the mathematical story and timeline.</div>'
            return "".join(
                f'<article class="card story"><h3>{esc_text(c.get("title") or c.get("candidate_id"))}</h3>'
                f'<p>{render_math_prose_html(c.get("smallest_honest_claim"))}</p>'
                f'<p><strong>Claim boundary:</strong> {render_math_prose_html(c.get("overclaim_boundary"))}</p></article>'
                for c in candidates if isinstance(c, dict)
            )
        candidates = [
            {
                "title": "Black-box substitution cap for barely-superlinear carrier lower bounds",
                "cycle": "cycle-0007",
                "claim": "Positive target-query length exponent beta collapses all-exponent transfer; surviving routes must be subpolynomial-query or nonblackbox.",
                "payoff": "This can be a bounded obstruction lemma if formalized independently of the marathon prose.",
            },
            {
                "title": "Projection-carrier demagnification dichotomy",
                "cycle": "cycle-0005",
                "claim": "Projection-style carriers preserve only a bounded target-exponent window unless their embedding length is subpolynomial.",
                "payoff": "This explains why padding-style magnification is not a weak-source path to P vs NP without stronger source lower bounds.",
            },
            {
                "title": "Growth-padding quantifier repair",
                "cycle": "cycle-0003",
                "claim": "A single growth-padding carrier can conditionally exclude every SAT exponent, but only by moving the hard work into sparse valid-length lower bounds.",
                "payoff": "This is useful as a diagnostic theorem for separating real progress from moved proof debt.",
            },
        ]
        return "".join(
            f"""
            <article class="card story">
              <div class="row"><h3>{esc_text(c['title'])}</h3><span class="pill info">{esc_text(c['cycle'])}</span></div>
              <p><strong>Candidate claim:</strong> {render_math_prose_html(c['claim'])}</p>
              <p><strong>Contribution payoff:</strong> {render_math_prose_html(c['payoff'])}</p>
              <p><strong>Good enough when:</strong> the lemma has definitions, proof, limits, barrier notes, and a precise non-claim boundary.</p>
            </article>
            """
            for c in candidates
        )

    def result_atlas_html() -> str:
        atlas = payload.get("result_subgoal_atlas", {}) if isinstance(payload.get("result_subgoal_atlas"), dict) else {}
        problem_map = payload.get("problem_space_map", {}) if isinstance(payload.get("problem_space_map"), dict) else {}
        vault = payload.get("derivation_vault", {}) if isinstance(payload.get("derivation_vault"), dict) else {}
        enablement = payload.get("report", {}).get("completed_subgoal_enablement_analysis", {}) if isinstance(payload.get("report"), dict) else {}
        results = atlas.get("results", []) if isinstance(atlas.get("results"), list) else []
        subgoals = atlas.get("subgoals", []) if isinstance(atlas.get("subgoals"), list) else []
        nodes = problem_map.get("nodes", []) if isinstance(problem_map.get("nodes"), list) else []
        derivations = vault.get("derivations", []) if isinstance(vault.get("derivations"), list) else []
        result_by_id = {clean_text(row.get("result_id")): row for row in results if isinstance(row, dict)}
        enablement_html = ""
        if enablement:
            enablement_cards = "".join(
                f"""
                <article class="card review">
                  <div class="row">
                    <h4>{esc_text(row.get('completed_subgoal'))}</h4>
                    <span class="pill good">{esc_text(row.get('enablement_class'))}</span>
                    <span class="pill info">{esc_text(row.get('achievement_status'))}</span>
                  </div>
                  <p><strong>Bigger-problem gate:</strong> {render_math_prose_html(row.get('bigger_problem_gate'))}</p>
                  <p><strong>Before:</strong> {render_math_prose_html(row.get('before_gate'))}</p>
                  <p><strong>After:</strong> {render_math_prose_html(row.get('after_gate'))}</p>
                  <p><strong>Enablement mechanism:</strong> {render_math_prose_html(row.get('enablement_mechanism'))}</p>
                  <p><strong>Residual blockers:</strong></p>
                  <ul class="compact-list">{''.join(f'<li>{render_math_prose_html(blocker)}</li>' for blocker in row.get('residual_blockers', []) if clean_text(blocker))}</ul>
                  <p><strong>Next consumer:</strong> {esc_text(row.get('next_consumer'))}</p>
                </article>
                """
                for row in enablement.get("completed_subgoals", [])
                if isinstance(row, dict)
            )
            enablement_html = f"""
            <h2>Completed Subgoal Enablement Analysis</h2>
            <section class="card story">
              <div class="row">
                <h3>How Completed Subgoals Enable The Bigger Problem</h3>
                <span class="pill good">{esc_text(enablement.get('status'))}</span>
              </div>
              <p>{render_math_prose_html(enablement.get('summary'))}</p>
              <p><strong>Generated by skills:</strong> {skill_pills(enablement.get('generated_by_skills', []), 4)}</p>
              <p><strong>Overclaim boundary:</strong> {render_math_prose_html(enablement.get('overclaim_boundary'))}</p>
              <p><strong>Validation handoff:</strong> {render_math_prose_html(enablement.get('validation_handoff'))}</p>
            </section>
            <div class="grid cards">{enablement_cards}</div>
            """
        node_html = "".join(
            f"""
            <article class="relation-card">
              <span class="relation-label">{esc_text(node.get('route_family'))} · {esc_text(node.get('status'))}</span>
              <span class="relation-title">{esc_text(node.get('title'))}</span>
              <p><strong>Why it matters:</strong> {math_text(node.get('why_it_matters_html'), node.get('why_it_matters'))}</p>
              <p><strong>Next achievement:</strong> {math_text(node.get('next_achievement_html'), node.get('next_achievement'))}</p>
              <p><strong>Open pressure:</strong> {math_text((node.get('open_obligations_html') or [''])[0], (node.get('open_obligations') or [''])[0] if node.get('open_obligations') else '')}</p>
            </article>
            """
            for node in nodes
            if isinstance(node, dict)
        )
        subgoal_html = []
        for subgoal in subgoals:
            if not isinstance(subgoal, dict):
                continue
            linked_results = [result_by_id.get(clean_text(result_id)) for result_id in subgoal.get("result_ids", [])]
            linked_results = [row for row in linked_results if isinstance(row, dict)]
            result_cards = "".join(
                f"""
                <article class="card review">
                  <div class="row">
                    <h4>{esc_text(result.get('result_kind'))}</h4>
                    <span class="pill {'good' if result.get('achievement_status') in {'achieved', 'handoff_ready'} else 'info'}">{esc_text(result.get('achievement_status'))}</span>
                  </div>
                  <p>{math_text(result.get('claim_html'), result.get('claim'))}</p>
                  <p><strong>Global role:</strong> {math_text(result.get('problem_space_coordinates', {}).get('global_problem_role_html'), result.get('problem_space_coordinates', {}).get('global_problem_role'))}</p>
                  <p><strong>Open obligation:</strong> {math_text((result.get('open_obligations_html') or [''])[0], (result.get('open_obligations') or [''])[0] if result.get('open_obligations') else '')}</p>
                  <p><strong>Non-claim:</strong> {math_text((result.get('non_claims_html') or [''])[0], (result.get('non_claims') or [''])[0] if result.get('non_claims') else '')}</p>
                </article>
                """
                for result in linked_results[:4]
            )
            subgoal_html.append(
                f"""
                <section class="card story">
                  <div class="row">
                    <h3>{esc_text(subgoal.get('title') or subgoal.get('subgoal_id'))}</h3>
                    <span class="pill info">{esc_text(subgoal.get('status'))}</span>
                    <span class="pill info">{esc_text(subgoal.get('result_count'))} results</span>
                  </div>
                  <p><strong>Main open obligation:</strong> {math_text((subgoal.get('open_obligations_html') or [''])[0], (subgoal.get('open_obligations') or [''])[0] if subgoal.get('open_obligations') else '')}</p>
                  {result_cards or '<p class="muted">No result entries linked to this subgoal yet.</p>'}
                </section>
                """
            )
        derivation_html = "".join(
            f"""
            <article class="card api">
              <div class="row">
                <h3>{esc_text(derivation.get('title'))}</h3>
                <span class="pill info">{esc_text(derivation.get('proof_status'))}</span>
              </div>
              <p>{math_text(derivation.get('claim_html'), derivation.get('claim'))}</p>
              <p><strong>Linked results:</strong> {esc_text(', '.join(derivation.get('linked_result_ids', [])[:3]) or derivation.get('orphan_reason'))}</p>
              <p><strong>Open proof obligation:</strong> {math_text((derivation.get('unresolved_obligations_html') or [''])[0], (derivation.get('unresolved_obligations') or [''])[0] if derivation.get('unresolved_obligations') else '')}</p>
              {''.join(f'<div class="equation">\\[{html.escape(eq.get("latex_render", ""), quote=False)}\\]</div>' for eq in derivation.get('equations', [])[:1] if isinstance(eq, dict) and clean_text(eq.get('latex_render')))}
            </article>
            """
            for derivation in derivations[:8]
            if isinstance(derivation, dict)
        )
        if not atlas:
            return '<div class="empty">No cumulative result atlas has been built for this target yet.</div>'
        summary = atlas.get("summary", {}) if isinstance(atlas.get("summary"), dict) else {}
        map_summary = problem_map.get("summary", {}) if isinstance(problem_map.get("summary"), dict) else {}
        vault_summary = vault.get("summary", {}) if isinstance(vault.get("summary"), dict) else {}
        return f"""
        <div class="quality">
          {chip('durable results', summary.get('result_count', len(results)))}
          {chip('subgoals', summary.get('subgoal_count', len(subgoals)))}
          {chip('problem nodes', map_summary.get('node_count', len(nodes)))}
          {chip('derivations', vault_summary.get('derivation_count', len(derivations)))}
        </div>
        <article class="card story">
          <h3>How To Read This Atlas</h3>
          <p>The atlas is the cumulative result memory for this target. It separates durable mathematical content from queued intentions: a result entry records what was learned, which subgoal it belongs to, which validation remains open, and why it matters for the global problem.</p>
          <p><strong>Authoritative control rule:</strong> future cycles should close open obligations or strengthen derivations attached to these entries; repeating an archived claim without a new proof step, calculation, or validation result should be demoted.</p>
          <p><strong>Active skills:</strong> {skill_pills(['result-atlas-maintainer','contribution-oriented-subgoal-manager','main-problem-alignment-auditor','paper-contribution-readiness-judge','next-experiment-queue-ranker'], 8)}</p>
        </article>
        {enablement_html}
        <h2>Problem Space Map</h2>
        <div class="relation-board">{node_html or '<div class="empty">No problem-space nodes available.</div>'}</div>
        <h2>Subgoal Result Atlas</h2>
        {''.join(subgoal_html) or '<div class="empty">No subgoal groups available.</div>'}
        <h2>Derivation Vault</h2>
        <p class="muted">Reusable derivations, sketches, symbolic audits, and unresolved proof obligations linked back to result entries.</p>
        {derivation_html or '<div class="empty">No derivations available.</div>'}
        """

    def literature_html() -> str:
        literature = payload.get("target_literature_evolution", {})
        statement = literature.get("problem_statement", {}) if isinstance(literature.get("problem_statement"), dict) else {}
        difficulty = literature.get("why_difficult", {}) if isinstance(literature.get("why_difficult"), dict) else {}
        stages = literature.get("literature_stages", []) if isinstance(literature.get("literature_stages"), list) else []
        refs = literature.get("references", []) if isinstance(literature.get("references"), list) else []
        criteria = literature.get("solution_criteria", []) if isinstance(literature.get("solution_criteria"), list) else []
        implications = literature.get("workflow_implications", []) if isinstance(literature.get("workflow_implications"), list) else []
        open_obligations = literature.get("open_obligations", []) if isinstance(literature.get("open_obligations"), list) else []
        required = literature.get("required_skills", []) if isinstance(literature.get("required_skills"), list) else []
        if not stages:
            stages = [
                {
                    "period": "current",
                    "title": "Target-specific literature profile not generated",
                    "core_shift": "Use the target-literature skill before claiming historical positioning.",
                    "what_became_possible": "",
                    "what_remained_open": "",
                }
            ]
        if not criteria:
            criteria = ["Name source object, target object, proof model, transfer theorem, and validation handoff."]
        problem_header = f"""
        <div class="card story">
          <h3>{esc_text(literature.get('problem_name') or target_id)}</h3>
          <p>{render_math_prose_html(statement.get('accessible', ''))}</p>
          <p class="muted">{esc_text(literature.get('authorship', ''))}</p>
          {f'<div class="equation">\\[{html.escape(sanitize_latex_for_mathjax(statement.get("formal_shape", "")), quote=False)}\\]</div>' if statement.get('formal_shape') else ''}
        </div>
        """
        why_matters = literature.get("why_it_matters", []) if isinstance(literature.get("why_it_matters"), list) else []
        why_matters_html = ""
        if why_matters:
            why_matters_html = "<h2>Why This Problem Matters</h2>" + "".join(
                f'<article class="card story"><p>{render_math_prose_html(item)}</p></article>' for item in why_matters
            )
        difficulty_html = ""
        if difficulty:
            difficulty_html = f"""
            <h2>Why This Is Difficult</h2>
            <article class="card story">
              <p>{render_math_prose_html(difficulty.get('overview', ''))}</p>
              {f"<p><strong>Core tension:</strong> {render_math_prose_html(difficulty.get('core_tension', ''))}</p>" if difficulty.get('core_tension') else ''}
            </article>
            <div class="relation-board">
              {''.join(f'''
              <article class="relation-card">
                <span class="relation-label">{esc_text(facet.get('lens', 'difficulty lens'))}</span>
                <span class="relation-title">{render_math_prose_html(facet.get('claim', ''))}</span>
                <p><strong>Pressure:</strong> {render_math_prose_html(facet.get('pressure', ''))}</p>
                <p><strong>Workflow consequence:</strong> {render_math_prose_html(facet.get('workflow_consequence', ''))}</p>
              </article>
              ''' for facet in difficulty.get('facets', []) if isinstance(facet, dict))}
            </div>
            {f"<h3>False Shortcuts To Avoid</h3><ul>{''.join(f'<li>{render_math_prose_html(item)}</li>' for item in difficulty.get('common_false_shortcuts', []))}</ul>" if difficulty.get('common_false_shortcuts') else ''}
            """
        return f"""
        {problem_header}
        {why_matters_html}
        {difficulty_html}
        <h2>Problem Evolution</h2>
        {''.join(f'''
        <article class="card story">
          <div class="row"><h3>{esc_text(stage.get('period'))} · {esc_text(stage.get('title'))}</h3></div>
          <p><strong>Conceptual shift:</strong> {render_math_prose_html(stage.get('core_shift', ''))}</p>
          <p><strong>What became possible:</strong> {render_math_prose_html(stage.get('what_became_possible', ''))}</p>
          <p><strong>What remained open:</strong> {render_math_prose_html(stage.get('what_remained_open', ''))}</p>
        </article>
        ''' for stage in stages if isinstance(stage, dict))}
        <h2>What Would Count As Progress</h2>
        <ul>{''.join(f'<li>{render_math_prose_html(item)}</li>' for item in criteria)}</ul>
        <h2>What The Literature Teaches The Workflow</h2>
        {''.join(f'''
        <article class="card review">
          <p><strong>Lesson:</strong> {render_math_prose_html(item.get('lesson', ''))}</p>
          <p><strong>Workflow effect:</strong> {render_math_prose_html(item.get('active_workflow_effect', ''))}</p>
        </article>
        ''' for item in implications if isinstance(item, dict))}
        <h2>Open Obligations Still Alive</h2>
        <ul>{''.join(f'<li>{render_math_prose_html(item)}</li>' for item in open_obligations)}</ul>
        <h2>Reference Anchors</h2>
        <div class="relation-board">
        {''.join(f'''
        <article class="relation-card">
          <span class="relation-label">{esc_text(ref.get('role', 'reference'))} · {esc_text(ref.get('status', ''))}</span>
          <span class="relation-title">{esc_text(ref.get('authors', ''))} ({esc_text(ref.get('year', ''))})</span>
          <p><a href="{html.escape(clean_text(ref.get('url', '#')), quote=True)}" target="_blank" rel="noreferrer">{esc_text(ref.get('title', ''))}</a></p>
          <p><strong>Supports:</strong> {render_math_prose_html(ref.get('supports', ''))}</p>
          <p><strong>Limit:</strong> {render_math_prose_html(ref.get('limitation', ''))}</p>
        </article>
        ''' for ref in refs if isinstance(ref, dict))}
        </div>
        <h2>Skills To Keep Active</h2>
        <p>{skill_pills(required or ['target-literature-source-curator','kb-prior-art-pass','kb-deduce','counterexample-hunter','main-problem-alignment-auditor','next-experiment-queue-ranker'], 12)}</p>
        """

    def macro_strategy_html() -> str:
        if target_id != "p-vs-np-target":
            rows = payload.get("macro_strategy_report", {}).get("strategies", [])
            if not rows:
                return '<div class="empty">No separate macro-strategy assessment is recorded. See the actual branch learning and next-analysis queue.</div>'
            return f'<p class="muted">{esc_text(payload.get("macro_strategy_report", {}).get("status", ""))}</p>' + "".join(
                f'<article class="card story"><h3>{esc_text(row.get("title"))}</h3>'
                f'<p>{render_math_prose_html(row.get("macro_thesis"))}</p>'
                f'<p><strong>Validation:</strong> {render_math_prose_html(row.get("validation"))}</p></article>'
                for row in rows if isinstance(row, dict)
            )
        strategies = [
            ("Quantitative transfer audit", "Compute exact exponent transfer from source lower bound to target class; demote routes whose overhead leaves only a bounded exponent window.", ["pvsnp-symbolic-complexity-auditor", "pvsnp-qualitative-complexity-reasoner", "kb-deduce", "entailment-gap-auditor", "progression-payoff-judge"]),
            ("Conceptual pressure localization", "Start each branch by naming why the route is hard: transfer debt, quantifier strength, model switch, barrier pressure, or proof-debt relocation.", ["pvsnp-conceptual-pressure-localizer", "main-problem-alignment-auditor", "next-experiment-queue-ranker"]),
            ("Meta-complexity carrier route", "Use MCSP/MKtP-style carriers only when the route states non-naturalness, density, advice, and verifier overhead explicitly.", ["pvsnp-conceptual-pressure-localizer", "pvsnp-symbolic-complexity-auditor", "kb-abduce", "kb-concept-bridge-planner", "counterexample-hunter"]),
            ("Nonblackbox/subpolynomial interface route", "Search for carriers where target-query length is subpolynomial or where the SAT circuit is used in a genuinely nonblackbox way.", ["pvsnp-qualitative-complexity-reasoner", "kb-gap-abstraction-conjecturer", "abducer-refinement-route-ranker", "kb-proof-connector"]),
            ("Barrier-aware no-go production", "Turn failed routes into publishable obstruction lemmas when they clarify why a class of magnification strategies cannot reach P vs NP.", ["pvsnp-symbolic-complexity-auditor", "pvsnp-impossibility-theorem-forger", "contradiction-route-auditor", "scientific-contribution-detector", "paper-contribution-readiness-judge"]),
        ]
        return "".join(
            f"""
            <article class="card story">
              <h3>{esc_text(title)}</h3>
              <p>{render_math_prose_html(thesis)}</p>
              <p><strong>Active skills:</strong> {skill_pills(skills, 8)}</p>
            </article>
            """
            for title, thesis, skills in strategies
        )

    def strategy_judge_html() -> str:
        latest = cycles[-1] if cycles else {}
        if target_id != "p-vs-np-target":
            return f'''<article class="card story">
              <h3>Current Diagnosis</h3>
              <p>{render_math_prose_html(story.get('latest_learning') or latest.get('mathematical_learning'))}</p>
              <p><strong>Current obstruction:</strong> {render_math_prose_html(story.get('current_obstruction') or latest.get('blocking_gap'))}</p>
              <p><strong>Next analysis:</strong> {render_math_prose_html(latest.get('next_experiment') or story.get('next_experiment'))}</p>
              <p><strong>Decision rule:</strong> complete the named derivation or counterexample and inspect its assumptions before continuing. Stop when the requested obligations have a checked disposition; retain unresolved gaps explicitly.</p>
              <p><strong>Scope:</strong> this is a summary of recorded learning, not an additional independent adjudication.</p>
            </article>{ranked_queue_html()}'''
        negative_tactics = payload.get("pvsnp_negative_tactics", {}) if target_id == "p-vs-np-target" else {}
        tactic_rows = negative_tactics.get("recommendations", []) if isinstance(negative_tactics.get("recommendations"), list) else []
        inference_quality = payload.get("pvsnp_inference_quality", {}) if target_id == "p-vs-np-target" else {}
        inference_packets = inference_quality.get("packets", []) if isinstance(inference_quality.get("packets"), list) else []
        inference_summary = inference_quality.get("summary", {}) if isinstance(inference_quality.get("summary"), dict) else {}
        packet_obligation = inference_quality.get("current_packet_obligation", {}) if isinstance(inference_quality.get("current_packet_obligation"), dict) else {}
        reviewer_stack = inference_quality.get("consistency_reviewer_stack", []) if isinstance(inference_quality.get("consistency_reviewer_stack"), list) else []
        top_paper_criteria = payload.get("pvsnp_formula_footprints_top_paper_criteria", {}) if target_id == "p-vs-np-target" else {}
        criteria_rows = top_paper_criteria.get("criteria", []) if isinstance(top_paper_criteria.get("criteria"), list) else []
        cohered_rows = [row for row in criteria_rows if isinstance(row, dict) and row.get("id") == "C11"]
        closure_gate = payload.get("pvsnp_formula_footprints_closure_gate", {}) if target_id == "p-vs-np-target" else {}
        tactic_html = ""
        if tactic_rows:
            tactic_html = f"""
            <h2>Negative Tactic Control</h2>
            {''.join(f'''
            <article class="card story">
              <div class="row">
                <h3>{esc_text(row.get('branch_title') or row.get('branch_id'))}</h3>
                <span class="pill good">{esc_text(row.get('tactic_mode'))}</span>
                <span class="pill info">{esc_text(row.get('route_family'))}</span>
              </div>
              <p><strong>Why this tactic:</strong> {row.get('reason_for_tactic_html') or render_math_prose_html(row.get('reason_for_tactic', ''))}</p>
              <p><strong>Method class / negation:</strong> {row.get('exact_negation_or_method_class_html') or render_math_prose_html(row.get('exact_negation_or_method_class', ''))}</p>
              <p><strong>Carrier:</strong> {row.get('contradiction_carrier_or_no_go_family_html') or render_math_prose_html(row.get('contradiction_carrier_or_no_go_family', ''))}</p>
              <p><strong>Conflict target:</strong> {row.get('conflict_target_html') or render_math_prose_html(row.get('conflict_target', ''))}</p>
              <p><strong>Escape conditions:</strong></p>
              <ul>{''.join(f'<li>{item}</li>' for item in row.get('escape_conditions_html', []))}</ul>
              <p><strong>Proof obligations:</strong></p>
              <ul>{''.join(f'<li>{item}</li>' for item in row.get('proof_obligations_html', []))}</ul>
              <p><strong>Handoff:</strong> {row.get('next_validation_handoff_html') or render_math_prose_html(row.get('next_validation_handoff', ''))}</p>
              <p><strong>Paper contribution potential:</strong> {row.get('paper_contribution_potential_html') or render_math_prose_html(row.get('paper_contribution_potential', ''))}</p>
            </article>
            ''' for row in tactic_rows)}
            """
        inference_html = ""
        if inference_quality:
            packet_cards = "".join(
                f"""
                <article class="card review">
                  <div class="row">
                    <h3>{esc_text(packet.get('packet_id'))}</h3>
                    <span class="pill {'good' if packet.get('decision') in {'accept_for_derivation', 'review_only'} else 'info'}">{esc_text(packet.get('decision'))}</span>
                    <span class="pill info">{esc_text(packet.get('inference_rule'))}</span>
                  </div>
                  <p><strong>Source:</strong> {packet.get('source_statement_html') or render_math_prose_html(packet.get('source_statement', ''))}</p>
                  <p><strong>Target:</strong> {packet.get('target_statement_html') or render_math_prose_html(packet.get('target_statement', ''))}</p>
                  <p><strong>Model:</strong> {render_math_prose_html(packet.get('source_carrier', ''))} &rarr; {render_math_prose_html(packet.get('target_class', ''))}; reduction {esc_text(packet.get('reduction_type'))}.</p>
                  <p><strong>Quantifiers:</strong> {esc_text(packet.get('length_regime'))}, {esc_text(packet.get('exponent_regime'))}, {esc_text(packet.get('uniformity'))}, {esc_text(packet.get('advice_status'))}.</p>
                  <p><strong>Derivation:</strong> {esc_text(packet.get('derivation_status'))}. {packet.get('blocked_obligation_html') or render_math_prose_html(packet.get('blocked_obligation', ''))}</p>
                </article>
                """
                for packet in inference_packets[:6]
                if isinstance(packet, dict)
            )
            inference_html = f"""
            <h2>Inference Quality Control</h2>
            <article class="card story">
              <div class="quality">
                {chip('live packets', inference_summary.get('live_packet_count', 0))}
                {chip('gate status', inference_summary.get('quality_gate_status', 'active'))}
                {chip('validator', inference_summary.get('proof_gate', 'validate_pvsnp_inference_quality.py'))}
              </div>
              <p>{packet_obligation.get('required_packet_html') or render_math_prose_html(packet_obligation.get('required_packet', ''))}</p>
              <p><strong>Minimum packet fields:</strong></p>
              <ul>{''.join(f'<li>{item}</li>' for item in packet_obligation.get('minimum_fields_html', []))}</ul>
              <p><strong>Consistency reviewers:</strong> {skill_pills([row.get('skill') for row in reviewer_stack if isinstance(row, dict)], 10)}</p>
            </article>
            {packet_cards}
            """
        top_paper_html = ""
        if cohered_rows:
            c11 = cohered_rows[0]
            top_paper_html = f"""
            <h2>Top Paper Criteria</h2>
            <article class="card story">
              <div class="row">
                <h3>C11 · Cohered Results</h3>
                <span class="pill {'good' if top_paper_criteria.get('status') == 'implemented' else 'info'}">{esc_text(top_paper_criteria.get('status') or 'active')}</span>
                <span class="pill info">{esc_text(top_paper_criteria.get('target_level') or 'publication gate')}</span>
              </div>
              <p>The paper must be one sharp, novel, weighty result package with a clear before/after understanding shift, not a fragmented ensemble of results or disconnected payoffs.</p>
              <p><strong>Pass evidence:</strong></p>
              <ul>{''.join(f'<li>{item}</li>' for item in c11.get('pass_evidence_html', [])[:5])}</ul>
              <p><strong>Fail evidence:</strong></p>
              <ul>{''.join(f'<li>{item}</li>' for item in c11.get('fail_evidence_html', [])[:5])}</ul>
              <p><strong>Admission rule:</strong></p>
              <ul>{''.join(f'<li>{item}</li>' for item in c11.get('admission_rule_html', [])[:4])}</ul>
            </article>
            """
        closure_gate_html = ""
        if closure_gate:
            route_items = "".join(
                f"<li>{render_math_prose_html(route)}</li>"
                for route in closure_gate.get("remaining_upgrade_routes", [])
                if clean_text(route)
            )
            artifact_links = ""
            if closure_gate.get("revised_tex") or closure_gate.get("revised_pdf") or closure_gate.get("novelty_delta_accounting"):
                tex_path = f'<span class="muted">{esc_text(closure_gate.get("revised_tex"))}</span>' if closure_gate.get("revised_tex") else ""
                pdf_path = f'<span class="muted">{esc_text(closure_gate.get("revised_pdf"))}</span>' if closure_gate.get("revised_pdf") else ""
                novelty_path = f'<span class="muted">{esc_text(closure_gate.get("novelty_delta_accounting"))}</span>' if closure_gate.get("novelty_delta_accounting") else ""
                artifact_links = f"""
                <p><strong>Artifacts:</strong>
                  {tex_path}
                  {pdf_path}
                  {novelty_path}
                </p>
                """
            closure_gate_html = f"""
            <h2>Formula Footprints Closure Gate</h2>
            <article class="card story">
              <div class="row">
                <h3>Carrier-independent audit upgrade criterion</h3>
                <span class="pill {'good' if closure_gate.get('carrier_independent_audit_upgrade_criterion') else 'info'}">{esc_text(closure_gate.get('carrier_independent_audit_upgrade_criterion') or 'criterion pending')}</span>
                <span class="pill {'good' if closure_gate.get('self_auditing_rup_cdcl_instantiation') else 'info'}">{esc_text(closure_gate.get('self_auditing_rup_cdcl_instantiation') or 'self-auditing RUP-CDCL pending')}</span>
                <span class="pill {'good' if closure_gate.get('append_only_self_auditing_rup_cdcl') else 'info'}">{esc_text(closure_gate.get('append_only_self_auditing_rup_cdcl') or 'append-only RUP-CDCL pending')}</span>
                <span class="pill {'good' if closure_gate.get('prefix_typed_append_only_rup_cdcl') else 'info'}">{esc_text(closure_gate.get('prefix_typed_append_only_rup_cdcl') or 'prefix-typed RUP-CDCL pending')}</span>
                <span class="pill {'good' if closure_gate.get('prefix_typed_rup_support_witness_necessity') else 'info'}">{esc_text(closure_gate.get('prefix_typed_rup_support_witness_necessity') or 'support-witness boundary pending')}</span>
                <span class="pill info">{esc_text(closure_gate.get('result') or 'gate active')}</span>
              </div>
              <p>{render_math_prose_html(closure_gate.get('narrative_weight_gate', ''))}</p>
              <p><strong>Coherence pass mode:</strong> {render_math_prose_html(closure_gate.get('coherence_pass_mode', ''))}</p>
              <p><strong>Coherence fail mode:</strong> {render_math_prose_html(closure_gate.get('coherence_fail_mode', ''))}</p>
              <p><strong>Remaining upgrade routes:</strong></p>
              <ul>{route_items}</ul>
              {artifact_links}
            </article>
            """
        return f"""
        <article class="card story">
          <h3>Current Diagnosis</h3>
          <p>{render_math_prose_html(story.get('latest_learning') or latest.get('mathematical_learning'))}</p>
          <p><strong>Current obstruction:</strong> {render_math_prose_html(story.get('current_obstruction') or latest.get('blocking_gap'))}</p>
          <p><strong>Recommendation:</strong> continue only with concrete carrier calculations or formal no-go lemmas; do not spend cycles restating hardness magnification.</p>
          <p><strong>When to stop:</strong> stop a branch when two sharpened attempts cannot name source lower bound, target class, reduction overhead, quantifier transfer, and barrier status.</p>
          <p><strong>Do not stop prematurely if:</strong> the branch can still compute an exponent transfer, isolate advice leakage, or formulate a formal obstruction lemma.</p>
          <p><strong>Skills:</strong> {skill_pills(['pvsnp-conceptual-pressure-localizer','pvsnp-qualitative-complexity-reasoner','pvsnp-symbolic-complexity-auditor','pvsnp-negative-tactic-selector','pvsnp-impossibility-theorem-forger','paper-contribution-readiness-judge','progression-payoff-judge','main-problem-alignment-auditor','contradiction-route-auditor','next-experiment-queue-ranker'], 12)}</p>
        </article>
        {inference_html}
        {tactic_html}
        {top_paper_html}
        {closure_gate_html}
        {ranked_queue_html()}
        """

    def story_html() -> str:
        return "".join(
            f"""
            <article class="card story">
              <div class="row"><h3>{esc_text(beat.get('cycle_id'))} · {esc_text(beat.get('branch_title'))}</h3><span class="pill info">{esc_text(beat.get('engine'))}</span></div>
              <p>{math_text(beat.get('learning_html'), beat.get('learning'))}</p>
              <p><strong>Next:</strong> {math_text(beat.get('next_experiment_html'), beat.get('next_experiment'))}</p>
              <p><strong>When to stop:</strong> {math_text(beat.get('when_to_stop_html'), beat.get('when_to_stop'))}</p>
              <p><strong>Global problem contribution:</strong> {math_text(beat.get('global_problem_contribution_html'), beat.get('global_problem_contribution'))}</p>
              <p><strong>Skills:</strong> {skill_pills(beat.get('required_skills', []), 14)}</p>
            </article>
            """
            for beat in story_beats
        ) or '<div class="empty">No accumulated story beats are available.</div>'

    generic_tab_script = """
  <script>
    (function () {
      function activateTab(tabName) {
        var selected = tabName || 'overview';
        document.querySelectorAll('.tab[data-tab]').forEach(function (button) {
          var active = button.getAttribute('data-tab') === selected;
          button.classList.toggle('active', active);
          button.setAttribute('aria-selected', active ? 'true' : 'false');
        });
        document.querySelectorAll('[data-panel]').forEach(function (panel) {
          panel.hidden = panel.getAttribute('data-panel') !== selected;
        });
        if (window.MathJax && window.MathJax.typesetPromise) {
          window.MathJax.typesetPromise().catch(function () {});
        }
      }
      document.addEventListener('click', function (event) {
        var button = event.target.closest('.tab[data-tab]');
        if (!button) return;
        event.preventDefault();
        activateTab(button.getAttribute('data-tab'));
      });
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { activateTab('overview'); });
      } else {
        activateTab('overview');
      }
    })();
  </script>
"""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="abducer-target-id" content="{target}">
  <title>{html.escape(title)}</title>
  <style>{CSS}</style>
</head>
<body>
  <script id="marathon-data" type="application/json">{embedded_payload}</script>
  <main class="shell">
    <header class="hero">
      <div>
        <p class="eyebrow">Abducer Discovery Marathon · generated {generated}</p>
        <h1>{display_name}</h1>
        <p class="subtitle">Target-specific marathon report with accumulated research cycles, branch learning, operational job health, and review checkpoints.</p>
        {initialization_notice(payload)}
      </div>
      <div class="metric-grid">
        {chip('research cycles', quality.get('valid_research_cycles', len(cycles)))}
        {chip('average seconds', quality.get('average_elapsed_seconds', 0))}
        {chip('minimum equations', (quality.get('minimum_quality') or {}).get('equations', 0))}
        {chip('unique skills', skill_summary.get('invoked_skill_count', 0))}
      </div>
    </header>
    <nav class="tabs" aria-label="{'timeline' if timeline_mode else 'marathon'} sections">
      <button class="tab active" data-tab="overview" aria-selected="true">Summary</button>
      <button class="tab" data-tab="physics_math_strategy" aria-selected="false">{strategy_label}</button>
      <button class="tab" data-tab="timeline" aria-selected="false">Timeline</button>
      <button class="tab" data-tab="ranked_queue" aria-selected="false">Ranked Analyses</button>
      <button class="tab" data-tab="skills" aria-selected="false">Skill Use</button>
      <button class="tab" data-tab="contributions" aria-selected="false">Contributions</button>
      <button class="tab" data-tab="result_atlas" aria-selected="false">Result Atlas</button>
      <button class="tab" data-tab="literature" aria-selected="false">Problem & Literature</button>
      <button class="tab" data-tab="macro_strategy" aria-selected="false">Macro Strategies</button>
      <button class="tab" data-tab="strategy_judge" aria-selected="false">Strategy Judge</button>
      <button class="tab" data-tab="artifact_or_stop" aria-selected="false">Artifact-Or-Stop</button>
      <button class="tab" data-tab="story" aria-selected="false">Story</button>
      <button class="tab" data-tab="branches" aria-selected="false">Branches</button>
      <button class="tab" data-tab="reviews" aria-selected="false">Deep Reviews</button>
    </nav>
    <section class="content">
      <div class="panel" data-panel="overview">
        <h2>Current Mathematical Story</h2>
        <div class="card story">
          <p>{render_math_prose_html(story.get('headline'))}</p>
          <p><strong>Latest Learning:</strong> {render_math_prose_html(story.get('latest_learning'))}</p>
          <p><strong>Current Obstruction:</strong> {render_math_prose_html(story.get('current_obstruction'))}</p>
          <p><strong>Next Analysis:</strong> {render_math_prose_html(story.get('next_experiment'))}</p>
        </div>
        <h2>Literature Gap Gate</h2>
        <div class="card story">
          <div class="row">
            <span class="pill {'good' if literature_summary.get('warrant_count') else 'warn'}">{esc_text(literature_summary.get('warrant_count', 0))} warrants</span>
            <span class="pill info">{esc_text(literature_summary.get('validator') or 'agentic/scripts/validate_avenue_literature_gap_warrant.py')}</span>
          </div>
          <p><strong>Investment decisions:</strong> {esc_text(literature_summary.get('investment_decision_counts', {}))}</p>
          <p><strong>Allowed next modes:</strong> {esc_text(literature_summary.get('allowed_next_mode_counts', {}))}</p>
          <p>{render_math_prose_html(literature_summary.get('gate_rule', 'Broad exploration needs a validated literature-gap warrant.'))}</p>
          <p><strong>Full packet:</strong> <span class="muted">{esc_text(literature_summary.get('latest_json'))}</span></p>
        </div>
        <h2>Next Analyses Queue</h2>
        <ul class="queue-list">
          {''.join(f'<li><span class="queue-meta">{esc_text(item.get("cycle_id"))} · {esc_text(item.get("engine"))}</span>{math_text(item.get("next_experiment_html"), item.get("next_experiment"))}</li>' for item in active_queue[:10])}
        </ul>
        <h2>Visual Conceptualization</h2>
        <div class="card story">
          <div class="row">
            <span class="pill good">{esc_text(visual_summary.get('concept_count', 0))} metaphors</span>
            <span class="pill info">{esc_text(visual_summary.get('hypothesis_output_count', 0))} route outputs</span>
            <span class="pill warn">{esc_text(visual_summary.get('quarantined_or_rejected_count', 0))} quarantined/rejected</span>
          </div>
          <p><strong>Headline metaphor:</strong> {esc_text(visual_summary.get('headline_metaphor'))}</p>
          <p><strong>Route consequences:</strong> {esc_text(visual_summary.get('route_consequences'))}</p>
          <p class="muted">Reflection artifact only unless a preservation audit promotes a concrete artifact, falsifier, route mutation, or representation requirement.</p>
          <p><strong>Full packet:</strong> <span class="muted">{esc_text(visual_summary.get('latest_json'))}</span></p>
        </div>
        <h2>Job Health</h2>
        {job_html or '<div class="empty">No job manifests found.</div>'}
      </div>
      <div class="panel" data-panel="physics_math_strategy" hidden>
        <h2>{strategy_label}</h2>
        <div class="card story">
          <h3>Cross-Route Synthesis</h3>
          <p>This view compares proof routes by their objects, assumptions, derivations, counterexamples and unresolved obligations.</p>
          <p><strong>Mathematical focus:</strong> {esc_text(profile['decisive_target_invariant'])}</p>
        </div>
        {macro_strategy_html()}
      </div>
      <div class="panel" data-panel="timeline" hidden>
        <h2>{'Timeline' if timeline_mode else 'Research Cycles'}</h2>
        {''.join(cycle_card(cycle) for cycle in cycles) or '<div class="empty">No research cycles found.</div>'}
      </div>
      <div class="panel" data-panel="ranked_queue" hidden>
        <h2>Current Ranked Next-Analysis Queue</h2>
        <p class="muted">Ordered by target payoff, discriminating power, execution readiness, target integration, and anti-drift pressure.</p>
        {ranked_queue_html()}
      </div>
      <div class="panel" data-panel="skills" hidden>
        <h2>Skill Use</h2>
        <p class="muted">Skill-dispatch trace accumulated from this run's recorded marathon cycles.</p>
        {skill_dispatch_html()}
      </div>
      <div class="panel" data-panel="contributions" hidden>
        <h2>Scientific Contribution Candidates</h2>
        <p class="muted">Candidate subgoals that may be paper-level contributions if converted into theorem statements, worked examples, or rigorous obstruction lemmas.</p>
        {contribution_html()}
      </div>
      <div class="panel" data-panel="result_atlas" hidden>
        <h2>Result Atlas And Problem Map</h2>
        <p class="muted">Cumulative state of achieved, partially achieved, blocked, and handoff-ready subgoals, with derivations attached to stable result objects.</p>
        {result_atlas_html()}
      </div>
      <div class="panel" data-panel="literature" hidden>
        <h2>Target Problem And Literature Evolution</h2>
        {literature_html()}
      </div>
      <div class="panel" data-panel="macro_strategy" hidden>
        <h2>General Macro Strategies</h2>
        {macro_strategy_html()}
      </div>
      <div class="panel" data-panel="strategy_judge" hidden>
        <h2>Strategy Progression Judge</h2>
        {strategy_judge_html()}
      </div>
      <div class="panel" data-panel="artifact_or_stop" hidden>
        <h2>Artifact-Or-Stop Anti-Incrementality Gate</h2>
        {artifact_or_stop_html()}
      </div>
      <div class="panel" data-panel="story" hidden>
        <h2>Accumulated Strategy Story</h2>
        {story_html()}
      </div>
      <div class="panel" data-panel="branches" hidden>
        <h2>Branches</h2>
        {branch_html or '<div class="empty">No branch summaries found.</div>'}
      </div>
      <div class="panel" data-panel="reviews" hidden>
        <h2>Deep Reviews</h2>
        {review_html or '<div class="empty">No deep reviews found.</div>'}
      </div>
    </section>
  </main>
  <script>
    window.MathJax = {{ tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['\\\\[', '\\\\]']] }}, svg: {{ fontCache: 'global' }} }};
  </script>
  <script data-embedded-dependency="mathjax-tex-svg">{mathjax}</script>
  {generic_tab_script}
</body>
</html>
"""


def render_html(payload: dict[str, Any]) -> str:
    if clean_text(payload.get("report", {}).get("target_id")) != "yang-mills-existence-and-mass-gap-target":
        return render_generic_target_html(payload, timeline_mode=False)
    data = json_for_script(payload)
    target = html.escape(clean_text(payload.get("report", {}).get("target_id", "discovery-marathon")))
    generated = html.escape(clean_text(payload.get("generated_utc", "")))
    mathjax = embedded_mathjax()
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="abducer-target-id" content="{target}">
  <title>Discovery Marathon Report</title>
  <style>{CSS}</style>
</head>
<body>
  <script id="marathon-data" type="application/json">{data}</script>
  <main class="shell">
    <header class="hero">
      <div>
        <p class="eyebrow">Abducer Discovery Marathon · generated {generated}</p>
        <h1>{target}</h1>
        <p class="subtitle">Accumulated marathon report across API and Codex-exec runs, with job health, research-cycle quality, operational failures, and the evolving mathematical story.</p>
        {initialization_notice(payload)}
      </div>
      <div id="metrics" class="metric-grid" aria-label="marathon metrics"></div>
    </header>
    <section class="controls" aria-label="cycle filters">
      <input id="query" class="control" type="search" placeholder="Filter cycles, equations, story, failures">
      <select id="engineFilter" class="control" aria-label="engine filter"></select>
      <select id="attemptFilter" class="control" aria-label="attempt filter"></select>
      <select id="jobFilter" class="control" aria-label="job filter"></select>
    </section>
    <nav class="tabs" aria-label="marathon sections">
      <button class="tab active" data-tab="overview">Summary</button>
      <button class="tab" data-tab="physics_math_strategy">Physics & Maths Strategy</button>
      <button class="tab" data-tab="timeline">Timeline</button>
      <button class="tab" data-tab="ranked_queue">Ranked Analyses</button>
      <button class="tab" data-tab="qualitative">Qualitative Graph</button>
      <button class="tab" data-tab="gedanken">Gedanken Experiments</button>
      <button class="tab" data-tab="parsimonious">PMP Probes</button>
      <button class="tab" data-tab="contributions">Contributions</button>
      <button class="tab" data-tab="literature">Problem & Literature</button>
      <button class="tab" data-tab="macro_strategy">Macro Strategies</button>
      <button class="tab" data-tab="strategy_judge">Strategy Judge</button>
      <button class="tab" data-tab="artifact_or_stop">Artifact-Or-Stop</button>
      <button class="tab" data-tab="story">Physics Story</button>
      <button class="tab" data-tab="branches">Branches</button>
      <button class="tab" data-tab="reviews">Deep Reviews</button>
    </nav>
    <div id="runtimeDiagnostic" class="runtime-diagnostic" role="status"></div>
    <section id="view" class="content" aria-live="polite"></section>
  </main>
  <script>{JS}</script>
  <script>
    window.MathJax = {{ tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['\\\\[', '\\\\]']] }}, svg: {{ fontCache: 'global' }} }};
  </script>
  <script data-embedded-dependency="mathjax-tex-svg">{mathjax}</script>
</body>
</html>
"""


def render_timeline_html(payload: dict[str, Any]) -> str:
    if clean_text(payload.get("report", {}).get("target_id")) != "yang-mills-existence-and-mass-gap-target":
        return render_generic_target_html(payload, timeline_mode=True)
    timeline_payload = dict(payload)
    timeline_payload["timeline_mode"] = True
    data = json_for_script(timeline_payload)
    target = html.escape(clean_text(payload.get("report", {}).get("target_id", "discovery-marathon")))
    generated = html.escape(clean_text(payload.get("generated_utc", "")))
    total_cycles = len(payload.get("timeline_cycles", []))
    start_cycle = TIMELINE_START_CYCLE
    mathjax = embedded_mathjax()
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="abducer-target-id" content="{target}">
  <title>Discovery Marathon Full Timeline</title>
  <style>{CSS}</style>
</head>
<body>
  <script id="marathon-data" type="application/json">{data}</script>
  <main class="shell">
    <header class="hero">
      <div>
        <p class="eyebrow">Abducer Discovery Marathon Timeline · generated {generated}</p>
        <h1>{target}</h1>
        <p class="subtitle">Content-specific accumulated timeline using the same card shape as the marathon report. It starts at cycle-{start_cycle:04d}, while the embedded payload still retains every persisted cycle packet for audit completeness.</p>
        {initialization_notice(payload)}
      </div>
      <div id="metrics" class="metric-grid" aria-label="timeline metrics"></div>
    </header>
    <section class="controls" aria-label="timeline filters">
      <input id="query" class="control" type="search" placeholder="Filter full timeline, engines, equations, failures">
      <select id="engineFilter" class="control" aria-label="engine filter"></select>
      <select id="attemptFilter" class="control" aria-label="attempt filter"></select>
      <select id="jobFilter" class="control" aria-label="job filter"></select>
    </section>
    <nav class="tabs" aria-label="timeline sections">
      <button class="tab active" data-tab="overview">Summary</button>
      <button class="tab" data-tab="physics_math_strategy">Physics & Maths Strategy</button>
      <button class="tab" data-tab="timeline">Timeline From cycle-{start_cycle:04d} ({total_cycles})</button>
      <button class="tab" data-tab="ranked_queue">Ranked Analyses</button>
      <button class="tab" data-tab="qualitative">Qualitative Graph</button>
      <button class="tab" data-tab="gedanken">Gedanken Experiments</button>
      <button class="tab" data-tab="parsimonious">PMP Probes</button>
      <button class="tab" data-tab="contributions">Contributions</button>
      <button class="tab" data-tab="literature">Problem & Literature</button>
      <button class="tab" data-tab="macro_strategy">Macro Strategies</button>
      <button class="tab" data-tab="strategy_judge">Strategy Judge</button>
      <button class="tab" data-tab="artifact_or_stop">Artifact-Or-Stop</button>
      <button class="tab" data-tab="story">Physics Story</button>
    </nav>
    <div id="runtimeDiagnostic" class="runtime-diagnostic" role="status"></div>
    <section id="view" class="content" aria-live="polite"></section>
  </main>
  <script>{JS}</script>
  <script>
    window.MathJax = {{ tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['\\\\[', '\\\\]']] }}, svg: {{ fontCache: 'global' }} }};
  </script>
  <script data-embedded-dependency="mathjax-tex-svg">{mathjax}</script>
</body>
</html>
"""


def select_report_path(run_id: str | None = None, target_id: str | None = None) -> Path:
    if target_id:
        scoped = target_latest_json(target_id)
        if scoped.exists():
            return scoped
    if run_id:
        _, run_state = load_run_state(run_id)
        run_target_id = clean_text(run_state.get("target_id"))
        if run_target_id:
            scoped = target_latest_json(run_target_id)
            if scoped.exists():
                return scoped
    return LATEST_JSON


def write_html(path: Path, document: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(trim_trailing_whitespace(document), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id")
    parser.add_argument("--target-id")
    args = parser.parse_args()
    report_path = select_report_path(args.run_id, args.target_id)
    report = load_json_object(report_path)
    payload = build_payload(report)
    latest_document = render_html(payload)
    timeline_document = render_timeline_html(payload)
    target_id = clean_text(report.get("target_id"))
    if target_id:
        scoped_latest = target_latest_html(target_id)
        scoped_timeline = target_timeline_html(target_id)
        write_html(scoped_latest, latest_document)
        write_html(scoped_timeline, timeline_document)
        print(f"Wrote target-scoped {rel(scoped_latest)}")
        print(f"Wrote target-scoped {rel(scoped_timeline)}")
    if generic_report_path_writable(LATEST_HTML, target_id) and generic_report_path_writable(LATEST_TIMELINE_HTML, target_id):
        write_html(LATEST_HTML, latest_document)
        write_html(LATEST_TIMELINE_HTML, timeline_document)
        print(f"Wrote compatibility {rel(LATEST_HTML)}")
        print(f"Wrote compatibility {rel(LATEST_TIMELINE_HTML)}")
    else:
        print(
            "Skipped compatibility discovery marathon HTML files because they are scoped to a different target; "
            f"use {rel(target_latest_html(target_id))} and {rel(target_timeline_html(target_id))}."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
