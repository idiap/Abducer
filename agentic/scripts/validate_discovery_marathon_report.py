#!/usr/bin/env python3
"""Validate discovery marathon report artifacts."""

from __future__ import annotations

import json
import re
import html as html_lib

from agentic_common import clean_text, fail, load_json_object, rel
from discovery_marathon_common import LATEST_HTML, LATEST_JSON, LATEST_MD, LATEST_TIMELINE_HTML


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
INLINE_TEX_RE = re.compile(r"\\\((.*?)\\\)")
INLINE_MATH_SPAN_RE = re.compile(r"<span class=\"inline-math\">\\\(.*?\\\)</span>")
CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
MISSING_SCRIPT_ARG_RE = re.compile(r"(?<!\\)(?:_|\^)(?=\s|$|[),.;:])")
MATH_COMMAND_MISSING_ARG_RE = re.compile(r"\\(?:mathbb|mathcal|mathrm|mathbf)\s*(?:$|[),.;:])")
MATH_ACCENT_UNBRACED_RE = re.compile(r"\\(?:widehat|overline)(?!\{)")
SCRIPT_SRC_RE = re.compile(r"<script\b[^>]*\bsrc\s*=", re.IGNORECASE)
STYLESHEET_LINK_RE = re.compile(r"<link\b(?=[^>]*\brel\s*=\s*['\"]?stylesheet)[^>]*\bhref\s*=", re.IGNORECASE)
CSS_IMPORT_RE = re.compile(r"@import\s+(?:url\()?['\"]?https?://", re.IGNORECASE)
TAB_BUTTON_RE = re.compile(r'<button\b(?=[^>]*\bclass="tab(?: active)?")(?=[^>]*\bdata-tab="([^"]+)")[^>]*>([^<]+)</button>')


def validate_self_contained_html(document: str, context: str) -> None:
    if SCRIPT_SRC_RE.search(document):
        fail(f"{context} must embed scripts directly; found a script src dependency")
    if STYLESHEET_LINK_RE.search(document):
        fail(f"{context} must embed styles directly; found a stylesheet link dependency")
    if CSS_IMPORT_RE.search(document):
        fail(f"{context} must not import remote CSS")
    if "cdn.jsdelivr.net/npm/mathjax" in document:
        fail(f"{context} still references CDN MathJax")
    if 'data-embedded-dependency="mathjax-tex-svg"' not in document:
        fail(f"{context} must embed the MathJax tex-svg dependency")


def validate_top_tab_order(document: str, context: str, *, timeline: bool = False) -> None:
    nav_match = re.search(r'<nav class="tabs" aria-label="(?:marathon|timeline) sections">(.*?)</nav>', document, re.DOTALL)
    if not nav_match:
        fail(f"{context} missing visible tab navigation")
    buttons = [(tab_id, html_lib.unescape(label)) for tab_id, label in TAB_BUTTON_RE.findall(nav_match.group(1))]
    if len(buttons) < 3:
        fail(f"{context} needs at least three visible report tabs")
    expected_first = [("overview", "Summary"), ("physics_math_strategy", "Physics & Maths Strategy")]
    if buttons[:2] != expected_first:
        fail(f"{context} must put Summary first and Physics & Maths Strategy second; found {buttons[:2]}")
    first_button_markup = TAB_BUTTON_RE.search(nav_match.group(1))
    if not first_button_markup or 'class="tab active"' not in first_button_markup.group(0):
        fail(f"{context} must make Summary the active default tab")
    if timeline and buttons[2][0] != "timeline":
        fail(f"{context} timeline report must put the content-specific timeline immediately after the top strategy tabs")
    panel_ids = set(re.findall(r'data-panel="([^"]+)"', document))
    if panel_ids:
        button_ids = {tab_id for tab_id, _ in buttons}
        missing_panels = sorted(button_ids - panel_ids)
        if missing_panels:
            fail(f"{context} has tab buttons without matching data-panel sections: {missing_panels}")
        if "document.addEventListener('click'" not in document and 'document.addEventListener("click"' not in document:
            fail(f"{context} has data-panel tabs but no click handler")


def has_unsafe_ampersand(value: str) -> bool:
    text = clean_text(value)
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
            index = match.end()
            continue
        if text[index] == "&" and (index == 0 or text[index - 1] != "\\") and not alignment_stack:
            return True
        index += 1
    return False


def validate_renderable_equations(payload: dict, source_label: str) -> None:
    for cycle in payload.get("all_cycles", []) + payload.get("research_cycles", []) + payload.get("timeline_cycles", []):
        cycle_id = clean_text(cycle.get("cycle_id")) or "unknown-cycle"
        for equation_index, equation in enumerate(cycle.get("equations", []), start=1):
            if not isinstance(equation, dict):
                continue
            render_latex = clean_text(equation.get("latex_render"))
            if not render_latex:
                fail(f"{source_label} {cycle_id} equation {equation_index} missing latex_render")
            if has_unsafe_ampersand(render_latex):
                fail(f"{source_label} {cycle_id} equation {equation_index} has a bare ampersand outside a TeX alignment environment")


def validate_tex_fragment(latex: str, context: str, kind: str) -> None:
    if CONTROL_CHAR_RE.search(latex):
        fail(f"{context} has a raw control character inside a {kind} TeX fragment")
    if re.search(r"\\mathbb(?!\{)", latex):
        fail(f"{context} has an unbraced \\mathbb command inside a {kind} TeX fragment")
    accent_match = MATH_ACCENT_UNBRACED_RE.search(latex)
    if accent_match:
        fail(f"{context} has an unbraced {accent_match.group(0)} command inside a {kind} TeX fragment")
    if MISSING_SCRIPT_ARG_RE.search(latex):
        fail(f"{context} has a missing superscript or subscript argument inside a {kind} TeX fragment")
    if MATH_COMMAND_MISSING_ARG_RE.search(latex):
        fail(f"{context} has a math font command without an argument inside a {kind} TeX fragment")
    if any(entity in latex for entity in ["&lt;", "&gt;", "&amp;lt;", "&amp;gt;", "&amp;"]):
        fail(f"{context} has an HTML comparison entity inside a {kind} TeX fragment")
    if has_unsafe_ampersand(html_lib.unescape(latex)):
        fail(f"{context} has a bare ampersand inside a {kind} TeX fragment")
    if "∘" in latex:
        fail(f"{context} has unicode composition inside a {kind} TeX fragment; use \\circ")


def validate_inline_math_html(value: str, context: str) -> None:
    text = clean_text(value)
    if CONTROL_CHAR_RE.search(value):
        fail(f"{context} contains a raw control character that can break MathJax")
    if '&lt;span class="inline-math"' in text or "&lt;span class='inline-math'" in text:
        fail(f"{context} contains escaped inline-math markup")
    if '<span class="inline-math"></span>' in text or '<span class="inline-math"> </span>' in text:
        fail(f"{context} contains an empty inline-math span")
    for broken in ["log(<span", "</span>\\oslash", "</span>∘"]:
        if broken in text:
            fail(f"{context} contains a split inline formula fragment `{broken}`")
    outside_math = INLINE_TEX_RE.sub("", INLINE_MATH_SPAN_RE.sub("", text))
    for broken in ["∘q_", "∘Q_"]:
        if broken in outside_math:
            fail(f"{context} contains a split inline formula fragment `{broken}`")
    for broken in [r"C^\(", r"\(\mathbb\)", r"\(C^\)", r"\(^"]:
        if broken in text:
            fail(f"{context} contains a split or argumentless inline TeX fragment `{broken}`")
    for latex in INLINE_TEX_RE.findall(clean_text(value)):
        if any(entity in latex for entity in ["&lt;", "&gt;", "&amp;lt;", "&amp;gt;", "&amp;"]):
            fail(f"{context} has an HTML comparison entity inside an inline TeX fragment")
        if has_unsafe_ampersand(html_lib.unescape(latex)):
            fail(f"{context} has a bare ampersand inside an inline TeX fragment")
        if "∘" in latex:
            fail(f"{context} has unicode composition inside an inline TeX fragment; use \\circ")
        validate_tex_fragment(latex, context, "inline")


def validate_renderable_cycle_prose(payload: dict, source_label: str) -> None:
    for cycle in payload.get("all_cycles", []) + payload.get("research_cycles", []) + payload.get("timeline_cycles", []):
        cycle_id = clean_text(cycle.get("cycle_id")) or "unknown-cycle"
        for field in ["mathematical_learning", "blocking_gap", "next_experiment"]:
            raw = clean_text(cycle.get(field))
            rendered = clean_text(cycle.get(f"{field}_html"))
            if raw and not rendered:
                fail(f"{source_label} {cycle_id} missing {field}_html")
            validate_inline_math_html(rendered, f"{source_label} {cycle_id} {field}_html")
        for raw_field, html_field in [("derivation_steps", "derivation_steps_html"), ("falsifiers", "falsifiers_html")]:
            raw_items = cycle.get(raw_field, [])
            html_items = cycle.get(html_field, [])
            if len(raw_items) != len(html_items):
                fail(f"{source_label} {cycle_id} {html_field} length does not match {raw_field}")
            for item_index, rendered in enumerate(html_items, start=1):
                if clean_text(raw_items[item_index - 1]) and not clean_text(rendered):
                    fail(f"{source_label} {cycle_id} {html_field} item {item_index} is empty")
                validate_inline_math_html(rendered, f"{source_label} {cycle_id} {html_field} item {item_index}")
        for raw_field, html_field in [("definitions", "definitions_html"), ("assumptions", "assumptions_html")]:
            raw_items = cycle.get(raw_field, [])
            html_items = cycle.get(html_field, [])
            if raw_items and len(raw_items) != len(html_items):
                fail(f"{source_label} {cycle_id} {html_field} length does not match {raw_field}")
            for item_index, rendered in enumerate(html_items, start=1):
                raw_value = raw_items[item_index - 1] if item_index - 1 < len(raw_items) else ""
                if clean_text(raw_value) and not clean_text(rendered):
                    fail(f"{source_label} {cycle_id} {html_field} item {item_index} is empty")
                validate_inline_math_html(rendered, f"{source_label} {cycle_id} {html_field} item {item_index}")
        if cycle.get("equation_count", 0) or cycle.get("derivation_step_count", 0):
            if not cycle.get("definitions") or not cycle.get("assumptions"):
                fail(f"{source_label} {cycle_id} equations/derivation steps must expose definitions and assumptions")
            validate_inline_math_html(
                clean_text(cycle.get("definition_assumption_elicitation_note_html")),
                f"{source_label} {cycle_id} definition_assumption_elicitation_note_html",
            )


def validate_storyline(payload: dict, source_label: str, timeline: bool = False) -> None:
    key = "timeline_storyline" if timeline else "research_storyline"
    storyline = payload.get(key, {})
    if not isinstance(storyline, dict):
        fail(f"{source_label} missing {key}")
    beats = storyline.get("beats", [])
    if not isinstance(beats, list) or not beats:
        fail(f"{source_label} {key} needs accumulated story beats")
    expected_cycles = payload.get("timeline_cycles" if timeline else "research_cycles", [])
    if timeline:
        expected_cycles = [cycle for cycle in expected_cycles if cycle.get("valid_as_research_cycle")]
        if int(storyline.get("start_cycle", 0)) != 174:
            fail(f"{source_label} timeline_storyline must start at cycle-0174")
        first_cycle = clean_text(beats[0].get("cycle_id"))
        if first_cycle != "cycle-0174":
            fail(f"{source_label} timeline_storyline starts at {first_cycle}, expected cycle-0174")
    if len(beats) != len(expected_cycles):
        fail(f"{source_label} {key} has {len(beats)} beats, expected {len(expected_cycles)}")
    for index, beat in enumerate(beats, start=1):
        for field in [
            "cycle_id",
            "branch_title",
            "learning",
            "learning_html",
            "next_experiment",
            "next_experiment_html",
            "when_to_stop",
            "global_problem_contribution",
            "global_problem_contribution_html",
            "premature_stop_guard",
            "required_skills",
        ]:
            if not clean_text(beat.get(field)):
                fail(f"{source_label} {key} beat {index} missing {field}")
        validate_inline_math_html(clean_text(beat.get("learning_html")), f"{source_label} {key} beat {index} learning_html")
        validate_inline_math_html(clean_text(beat.get("next_experiment_html")), f"{source_label} {key} beat {index} next_experiment_html")
        validate_inline_math_html(clean_text(beat.get("global_problem_contribution_html")), f"{source_label} {key} beat {index} global_problem_contribution_html")
        if "Stop or quarantine" not in clean_text(beat.get("when_to_stop")):
            fail(f"{source_label} {key} beat {index} when_to_stop lacks an explicit stop/quarantine condition")
        if "global problem" not in clean_text(beat.get("global_problem_contribution")).lower():
            fail(f"{source_label} {key} beat {index} global contribution is not framed as global problem value")


def validate_summary_analysis_control(payload: dict, source_label: str) -> None:
    control = payload.get("summary_analysis_control", {})
    if not isinstance(control, dict) or not control:
        fail(f"{source_label} missing summary_analysis_control")
    for field in [
        "next_experiment_html",
        "when_to_stop",
        "global_problem_contribution",
        "global_problem_contribution_html",
        "premature_stop_guard",
        "required_skills",
        "payoff_criteria",
    ]:
        if not control.get(field):
            fail(f"{source_label} summary_analysis_control missing {field}")
    validate_inline_math_html(clean_text(control.get("next_experiment_html")), f"{source_label} summary next_experiment_html")
    validate_inline_math_html(clean_text(control.get("global_problem_contribution_html")), f"{source_label} summary global_problem_contribution_html")


def validate_ranked_queue(payload: dict, source_label: str, timeline: bool = False) -> None:
    queue_key = "timeline_ranked_next_experiment_queue" if timeline else "ranked_next_experiment_queue"
    base_key = "timeline_next_experiment_queue" if timeline else "next_experiment_queue"
    ranked = payload.get(queue_key, [])
    base = payload.get(base_key, [])
    if not isinstance(ranked, list) or not ranked:
        fail(f"{source_label} {queue_key} must not be empty")
    if not isinstance(base, list) or not base:
        fail(f"{source_label} {base_key} must not be empty")
    if len(ranked) != len(base):
        fail(f"{source_label} {queue_key} length {len(ranked)} does not match {base_key} length {len(base)}")
    for index, item in enumerate(base, start=1):
        if not clean_text(item.get("next_experiment")):
            fail(f"{source_label} {base_key} item {index} missing next_experiment")
        validate_inline_math_html(clean_text(item.get("next_experiment_html")), f"{source_label} {base_key} item {index} next_experiment_html")
    previous_score = 10**9
    seen_ranks = []
    for index, item in enumerate(ranked, start=1):
        for field in [
            "rank",
            "priority_score",
            "priority_band",
            "why_target",
            "risk",
            "payoff_criteria",
            "required_skills",
            "next_experiment_html",
            "branch_continuation_decision",
            "branch_continuation_reason",
            "premature_stop_guard",
            "do_not_stop_if",
            "stop_criteria",
        ]:
            if field not in item or (field != "priority_score" and not item.get(field)):
                fail(f"{source_label} {queue_key} item {index} missing {field}")
        score = int(item["priority_score"])
        if score > previous_score:
            fail(f"{source_label} {queue_key} is not sorted by descending priority_score")
        previous_score = score
        seen_ranks.append(int(item["rank"]))
        criteria = item.get("payoff_criteria", [])
        if not isinstance(criteria, list) or not criteria:
            fail(f"{source_label} {queue_key} item {index} needs payoff criteria")
        for criterion_index, criterion in enumerate(criteria, start=1):
            if not clean_text(criterion.get("text")) or not clean_text(criterion.get("html")):
                fail(f"{source_label} {queue_key} item {index} payoff criterion {criterion_index} is incomplete")
            validate_inline_math_html(clean_text(criterion.get("html")), f"{source_label} {queue_key} item {index} payoff criterion {criterion_index}")
        if "next-experiment-queue-ranker" not in item.get("required_skills", []):
            fail(f"{source_label} {queue_key} item {index} must require next-experiment-queue-ranker")
        if item.get("queue_source") == "gedanken":
            for field in ["packet_id", "situation_title", "transfer_verdict", "success_criterion", "failure_or_demotion_criterion"]:
                if not clean_text(item.get(field)):
                    fail(f"{source_label} {queue_key} Gedanken item {index} missing {field}")
            if "gedanken-followup-planner" not in item.get("required_skills", []):
                fail(f"{source_label} {queue_key} Gedanken item {index} must require gedanken-followup-planner")
        decision = clean_text(item.get("branch_continuation_decision"))
        allowed_decisions = {
            "continue_run_next",
            "adapt_then_run",
            "backtrack_to_sharpen",
            "watch_archive_until_sharpened",
            "quarantine_candidate",
            "stop_candidate_after_repeat_low_payoff",
            "paper_packaging_priority",
        }
        if decision not in allowed_decisions:
            fail(f"{source_label} {queue_key} item {index} has invalid branch_continuation_decision {decision}")
        if decision == "stop_candidate_after_repeat_low_payoff" and "repeat" not in clean_text(item.get("premature_stop_guard")).lower():
            fail(f"{source_label} {queue_key} item {index} stop candidate lacks repeat-evidence guard")
        if len(item.get("do_not_stop_if", [])) < 3:
            fail(f"{source_label} {queue_key} item {index} needs do_not_stop_if guards")
        if len(item.get("stop_criteria", [])) < 3:
            fail(f"{source_label} {queue_key} item {index} needs stop criteria")
    if seen_ranks != list(range(1, len(ranked) + 1)):
        fail(f"{source_label} {queue_key} ranks must be consecutive")
    if timeline and ranked and min(int(item.get("cycle_number", 0)) for item in ranked) < 174:
        fail(f"{source_label} timeline ranked queue must not include pre-cycle-0174 items")


def validate_decisive_next_move_queue(payload: dict, source_label: str, timeline: bool = False) -> None:
    ranked_key = "timeline_ranked_next_experiment_queue" if timeline else "ranked_next_experiment_queue"
    base_key = "timeline_next_experiment_queue" if timeline else "next_experiment_queue"
    ranked = payload.get(ranked_key, [])
    base = payload.get(base_key, [])
    ranked_items = [item for item in ranked if item.get("queue_source") == "decisive_next_move"]
    base_items = [item for item in base if item.get("queue_source") == "decisive_next_move"]
    if len(ranked_items) != 1:
        fail(f"{source_label} {ranked_key} must contain exactly one decisive_next_move item")
    if len(base_items) != 1:
        fail(f"{source_label} {base_key} must contain exactly one decisive_next_move item")
    item = ranked_items[0]
    if int(item.get("rank", 0)) < 1:
        fail(f"{source_label} decisive_next_move item must be ranked")
    for field in [
        "source_object",
        "source_object_html",
        "target_object",
        "target_object_html",
        "transfer_condition",
        "transfer_condition_html",
        "next_experiment",
        "next_experiment_html",
        "smallest_honest_claim",
        "smallest_honest_claim_html",
    ]:
        if not clean_text(item.get(field)):
            fail(f"{source_label} decisive_next_move item missing {field}")
    for field in ["source_object_html", "target_object_html", "transfer_condition_html", "next_experiment_html", "smallest_honest_claim_html"]:
        validate_inline_math_html(clean_text(item.get(field)), f"{source_label} decisive_next_move {field}")
    steps = item.get("validation_steps", [])
    steps_html = item.get("validation_steps_html", [])
    if not isinstance(steps, list) or len(steps) < 7:
        fail(f"{source_label} decisive_next_move needs at least seven self-contained validation steps")
    if len(steps_html) != len(steps):
        fail(f"{source_label} decisive_next_move validation_steps_html length mismatch")
    required_step_terms = [
        "finite theorem",
        "Prove",
        "source object",
        "Compute",
        "finite positivity test",
        "same-theory transfer certificate",
        "prior art",
    ]
    combined_steps = " ".join(clean_text(step) for step in steps)
    for term in required_step_terms:
        if term.lower() not in combined_steps.lower():
            fail(f"{source_label} decisive_next_move validation steps missing `{term}`")
    for index, rendered in enumerate(steps_html, start=1):
        validate_inline_math_html(clean_text(rendered), f"{source_label} decisive_next_move validation step {index}")
    for field in ["payoff_criteria", "do_not_stop_if", "stop_criteria", "required_skills"]:
        values = item.get(field, [])
        if not isinstance(values, list) or len(values) < 4:
            fail(f"{source_label} decisive_next_move needs at least four {field}")
    expected_skills = {
        "next-experiment-queue-ranker",
        "paper-contribution-readiness-judge",
        "main-problem-alignment-auditor",
        "progression-payoff-judge",
        "finite-algebra-interface-builder",
        "symbolic-matrix-probe",
        "analytic-estimate-obligation-builder",
        "prior-art-importer",
    }
    missing = expected_skills.difference(set(item.get("required_skills", [])))
    if missing:
        fail(f"{source_label} decisive_next_move missing required skills: {sorted(missing)}")
    if "Wilson" not in clean_text(item.get("source_object")) or "OS-positive continuum" not in clean_text(item.get("target_object")):
        fail(f"{source_label} decisive_next_move source/target objects are not self-contained enough")
    if "uniform" not in clean_text(item.get("transfer_condition")).lower():
        fail(f"{source_label} decisive_next_move transfer condition must state the uniformity requirement")


def validate_paper_argument_priority_queue(payload: dict, source_label: str, timeline: bool = False) -> None:
    ranked_key = "timeline_ranked_next_experiment_queue" if timeline else "ranked_next_experiment_queue"
    base_key = "timeline_next_experiment_queue" if timeline else "next_experiment_queue"
    ranked = payload.get(ranked_key, [])
    base = payload.get(base_key, [])
    ranked_items = [item for item in ranked if item.get("queue_source") == "paper_argument_priority"]
    base_items = [item for item in base if item.get("queue_source") == "paper_argument_priority"]
    expected = {"finite_theorem_section", "endpoint_worked_calculation", "prior_art_positioning"}
    if {item.get("paper_task_subtype") for item in ranked_items} != expected:
        fail(f"{source_label} {ranked_key} must contain the three paper argument priority items")
    if {item.get("paper_task_subtype") for item in base_items} != expected:
        fail(f"{source_label} {base_key} must contain the three paper argument priority items")
    ranks = sorted(int(item.get("rank", 0)) for item in ranked_items)
    if ranks != [1, 2, 3]:
        fail(f"{source_label} paper argument priority items must occupy ranks 1-3")
    expected_skills = {
        "finite_theorem_section": "finite-theorem-section-packager",
        "endpoint_worked_calculation": "endpoint-worked-calculation-packager",
        "prior_art_positioning": "prior-art-positioning-packager",
    }
    for item in ranked_items:
        subtype = item.get("paper_task_subtype")
        for field in ["source_object", "target_object", "transfer_condition", "next_experiment", "validation_steps", "payoff_criteria", "required_skills"]:
            if not item.get(field):
                fail(f"{source_label} paper argument priority {subtype} missing {field}")
        if expected_skills[subtype] not in set(item.get("required_skills", [])):
            fail(f"{source_label} paper argument priority {subtype} missing skill {expected_skills[subtype]}")
        if int(item.get("priority_score", 0)) < 101:
            fail(f"{source_label} paper argument priority {subtype} must outrank ordinary queue items")
        for field in ["source_object_html", "target_object_html", "transfer_condition_html", "next_experiment_html"]:
            validate_inline_math_html(clean_text(item.get(field)), f"{source_label} paper argument priority {subtype} {field}")


def validate_qualitative_graph(payload: dict, source_label: str) -> None:
    graph = payload.get("qualitative_mechanistic_graph", {})
    if not isinstance(graph, dict) or not graph:
        fail(f"{source_label} missing qualitative_mechanistic_graph")
    summary = graph.get("summary", {})
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    if int(summary.get("node_count", len(nodes))) < 5:
        fail(f"{source_label} qualitative_mechanistic_graph needs at least five nodes")
    if int(summary.get("edge_count", len(edges))) < 4:
        fail(f"{source_label} qualitative_mechanistic_graph needs at least four edges")
    if int(summary.get("relation_packet_count", 0)) < 1:
        fail(f"{source_label} qualitative_mechanistic_graph needs relation packets")
    for index, edge in enumerate(edges, start=1):
        for field in ["source", "target", "edge_type", "direction", "validity_regime", "assumptions", "failure_modes", "evidence_paths", "epistemic_status"]:
            if not edge.get(field):
                fail(f"{source_label} qualitative edge {index} missing {field}")
        validate_inline_math_html(clean_text(edge.get("qualitative_behavior_html")), f"{source_label} qualitative edge {index}")


def validate_gedanken_experiments(payload: dict, source_label: str) -> None:
    report = payload.get("gedanken_experiments", {})
    if not isinstance(report, dict) or not report:
        fail(f"{source_label} missing gedanken_experiments")
    packets = report.get("packets", [])
    if not isinstance(packets, list) or not packets:
        fail(f"{source_label} gedanken_experiments needs packets")
    for index, packet in enumerate(packets, start=1):
        for field in ["packet_id", "need_decision", "need_assessment", "situation", "transfer_scope", "followup_cycle_tasks", "epistemic_status", "originating_cycle_ids", "originating_branch_ids"]:
            if not packet.get(field):
                fail(f"{source_label} Gedanken packet {index} missing {field}")
        need = packet.get("need_assessment", {})
        if need.get("decision") != packet.get("need_decision"):
            fail(f"{source_label} Gedanken packet {index} need_assessment decision mismatch")
        if packet.get("need_decision") == "design_now" and len(need.get("criteria_met", [])) < 2:
            fail(f"{source_label} Gedanken packet {index} design_now lacks criteria")
        situation = packet.get("situation", {})
        for field in ["purpose", "minimal_world", "mathematical_carrier", "controlled_contrast", "why_this_situation_is_informative", "non_claims"]:
            if not situation.get(field):
                fail(f"{source_label} Gedanken packet {index} situation missing {field}")
        transfer = packet.get("transfer_scope", {})
        for field in ["transfer_verdict", "transfers", "does_not_transfer", "transfer_certificate_needed"]:
            if not clean_text(transfer.get(field)):
                fail(f"{source_label} Gedanken packet {index} transfer_scope missing {field}")
        if packet.get("graph_update_action") != "none" and not packet.get("proposed_graph_updates"):
            fail(f"{source_label} Gedanken packet {index} graph update lacks proposed_graph_updates")
        tasks = packet.get("followup_cycle_tasks", [])
        if not isinstance(tasks, list) or not tasks:
            fail(f"{source_label} Gedanken packet {index} needs followup_cycle_tasks")
        for task_index, task in enumerate(tasks, start=1):
            for field in ["packet_id", "situation_title", "transfer_verdict", "success_criterion", "failure_or_demotion_criterion", "required_skills"]:
                if not task.get(field):
                    fail(f"{source_label} Gedanken packet {index} task {task_index} missing {field}")
            if task.get("packet_id") != packet.get("packet_id"):
                fail(f"{source_label} Gedanken packet {index} task {task_index} packet mismatch")
        if "proves the theorem" in clean_text(packet).lower():
            fail(f"{source_label} Gedanken packet {index} overclaims proof status")


def validate_scientific_contribution_monitor(payload: dict, source_label: str) -> None:
    monitor = payload.get("scientific_contribution_monitor", {})
    if not isinstance(monitor, dict) or not monitor:
        fail(f"{source_label} missing scientific_contribution_monitor")
    for field in ["loop_policy", "contribution_aim_status", "next_contribution_objective", "metrics", "validation_gap", "candidates"]:
        if not monitor.get(field):
            fail(f"{source_label} scientific_contribution_monitor missing {field}")
    policy = clean_text(monitor.get("loop_policy", {})).lower().replace("_", " ")
    for phrase in ["standing objective", "good enough", "anti infinite progression", "stepping stone maturity"]:
        if phrase not in policy:
            fail(f"{source_label} contribution monitor loop_policy missing `{phrase}`")
    metrics = monitor.get("metrics", {})
    for field in [
        "active_candidate_count",
        "certification_ready_count",
        "good_enough_count",
        "contribution_shaped_count",
        "near_stepping_stone_count",
        "publishable_handoff_count",
        "average_contribution_score",
        "average_publishable_subgoal_score",
        "infinite_progression_risk_count",
    ]:
        if field not in metrics:
            fail(f"{source_label} contribution monitor metrics missing {field}")
    candidates = monitor.get("candidates", [])
    if not isinstance(candidates, list) or len(candidates) < 3:
        fail(f"{source_label} contribution monitor needs at least three candidates")
    if int(metrics.get("active_candidate_count", 0)) < 1:
        fail(f"{source_label} contribution monitor needs at least one active candidate")
    required_skills = {
        "scientific-contribution-detector",
        "contribution-value-assessor",
        "contribution-oriented-subgoal-manager",
        "scientific-contribution-paper-handoff",
    }
    for index, candidate in enumerate(candidates, start=1):
        for field in [
            "candidate_id",
            "stepping_stone_maturity",
            "smallest_honest_claim",
            "why_it_could_stand_alone",
            "scores",
            "exploration_payoff_score",
            "publishable_subgoal_score",
            "paper_relevance_markers",
            "good_enough_paper_relevance",
            "missing_to_good_enough_paper",
            "handoff_hard_gates",
            "prior_art_boundary",
            "disqualifier_tests",
            "missing_to_publishable",
            "paper_note_shape",
            "why_this_budget_now",
            "good_enough_when",
            "continue_only_if",
            "stop_when",
            "infinite_progression_risk",
            "branch_control_decision",
        ]:
            if not candidate.get(field):
                fail(f"{source_label} contribution candidate {index} missing {field}")
        if candidate.get("stepping_stone_maturity") not in {"contribution_shaped", "near_stepping_stone", "publishable_handoff_ready"}:
            fail(f"{source_label} contribution candidate {index} invalid stepping_stone_maturity")
        if candidate.get("status") == "good_enough_to_handoff" and candidate.get("stepping_stone_maturity") != "publishable_handoff_ready":
            fail(f"{source_label} contribution candidate {index} overpromoted by status")
        if int(candidate.get("publishable_subgoal_score", 0)) > int(candidate.get("exploration_payoff_score", 0)):
            fail(f"{source_label} contribution candidate {index} publishable score exceeds exploration score")
        markers = candidate.get("paper_relevance_markers", [])
        expected_dims = {"conceptual_depth", "conceptual_novelty", "unblocking_power", "applicability", "understanding_gain"}
        marker_dims = {marker.get("dimension") for marker in markers if isinstance(marker, dict)}
        if marker_dims != expected_dims:
            fail(f"{source_label} contribution candidate {index} needs exact paper relevance markers")
        for marker in markers:
            if marker.get("status") not in {"absent", "weak", "adequate", "strong", "paper_ready"}:
                fail(f"{source_label} contribution candidate {index} invalid paper relevance marker status")
            if not isinstance(marker.get("score"), int) or not 0 <= marker.get("score") <= 5:
                fail(f"{source_label} contribution candidate {index} invalid paper relevance marker score")
            if not marker.get("criterion") or not marker.get("evidence"):
                fail(f"{source_label} contribution candidate {index} malformed paper relevance marker")
        relevance = candidate.get("good_enough_paper_relevance", {})
        for field in ["status", "average_marker_score", "paper_relevance_decision", "missing_for_good_enough_paper"]:
            if field not in relevance:
                fail(f"{source_label} contribution candidate {index} good_enough_paper_relevance missing {field}")
        if relevance.get("status") == "paper_relevance_ready" and candidate.get("stepping_stone_maturity") != "publishable_handoff_ready":
            fail(f"{source_label} contribution candidate {index} paper relevance ready without handoff maturity")
        gates = candidate.get("handoff_hard_gates", {})
        for gate in ["claim_statement_ready", "evidence_ready", "novelty_boundary_ready", "validation_ready", "overclaim_boundary_ready"]:
            packet = gates.get(gate)
            if not isinstance(packet, dict) or "ready" not in packet or "finite_task" not in packet or not clean_text(packet.get("evidence")):
                fail(f"{source_label} contribution candidate {index} malformed hard gate {gate}")
        if candidate.get("stepping_stone_maturity") == "publishable_handoff_ready" and not all(packet.get("ready") for packet in gates.values()):
            fail(f"{source_label} contribution candidate {index} publishable without all hard gates")
        prior = candidate.get("prior_art_boundary", {})
        for field in ["closest_known_results", "what_is_reused", "what_is_new_if_true", "rediscovery_risk", "citation_tasks", "novelty_status"]:
            if not prior.get(field):
                fail(f"{source_label} contribution candidate {index} prior_art_boundary missing {field}")
        if candidate.get("stepping_stone_maturity") == "publishable_handoff_ready" and prior.get("novelty_status") != "checked":
            fail(f"{source_label} contribution candidate {index} publishable without checked prior art")
        if len(candidate.get("disqualifier_tests", [])) < 5:
            fail(f"{source_label} contribution candidate {index} needs disqualifier tests")
        shape = candidate.get("paper_note_shape", {})
        for field in ["title", "abstract_claim", "theorem_or_result_statement", "definitions_needed", "proof_plan", "relation_to_main_problem", "limitations", "next_validation_artifacts"]:
            if not shape.get(field):
                fail(f"{source_label} contribution candidate {index} paper_note_shape missing {field}")
        if len(candidate.get("good_enough_when", [])) < 4:
            fail(f"{source_label} contribution candidate {index} needs good-enough criteria")
        if len(candidate.get("continue_only_if", [])) < 3:
            fail(f"{source_label} contribution candidate {index} needs continue-only-if criteria")
        if len(candidate.get("stop_when", [])) < 3:
            fail(f"{source_label} contribution candidate {index} needs stop criteria")
        if not required_skills.issubset(set(candidate.get("required_skills", []))):
            fail(f"{source_label} contribution candidate {index} missing contribution skills")


def validate_target_literature_evolution(payload: dict, source_label: str) -> None:
    report = payload.get("target_literature_evolution", {})
    if not isinstance(report, dict) or not report:
        fail(f"{source_label} missing target_literature_evolution")
    for field in ["problem_name", "problem_statement", "literature_stages", "workflow_implications", "open_obligations", "references", "required_skills"]:
        if not report.get(field):
            fail(f"{source_label} target_literature_evolution missing {field}")
    refs = report.get("references", [])
    if len(refs) < 8:
        fail(f"{source_label} target_literature_evolution needs at least eight references")
    ref_ids = {ref.get("ref_id") for ref in refs if isinstance(ref, dict)}
    roles = {clean_text(ref.get("role")) for ref in refs if isinstance(ref, dict)}
    for role in ["problem_statement", "origin", "axiomatic_bridge", "physics_motivation", "constructive_program", "route_obstruction"]:
        if role not in roles:
            fail(f"{source_label} target literature references missing role {role}")
    for index, ref in enumerate(refs, start=1):
        for field in ["ref_id", "year", "authors", "title", "url", "role", "supports", "limitation"]:
            if not ref.get(field):
                fail(f"{source_label} target literature reference {index} missing {field}")
    stages = report.get("literature_stages", [])
    if len(stages) < 5:
        fail(f"{source_label} target_literature_evolution needs at least five stages")
    for index, stage in enumerate(stages, start=1):
        for field in ["period", "title", "core_shift", "what_became_possible", "what_remained_open", "refs"]:
            if not stage.get(field):
                fail(f"{source_label} target literature stage {index} missing {field}")
        for ref_id in stage.get("refs", []):
            if ref_id not in ref_ids:
                fail(f"{source_label} target literature stage {index} cites unknown {ref_id}")
    text = clean_text(report).lower()
    for phrase in ["same-theory", "continuum", "reflection positivity", "mass gap", "nontrivial"]:
        if phrase not in text:
            fail(f"{source_label} target literature narrative missing `{phrase}`")
    if not {"target-literature-source-curator", "target-literature-evolution-narrator"}.issubset(set(report.get("required_skills", []))):
        fail(f"{source_label} target literature report missing required skills")


def validate_macro_strategy_report(payload: dict, source_label: str) -> None:
    report = payload.get("macro_strategy_report", {})
    if not isinstance(report, dict) or not report:
        fail(f"{source_label} missing macro_strategy_report")
    for field in ["headline", "strategy_status", "physics_language_standard", "story_basis", "macro_strategies", "recommended_next_posture"]:
        if not report.get(field):
            fail(f"{source_label} macro_strategy_report missing {field}")
    strategies = report.get("macro_strategies", [])
    if not isinstance(strategies, list) or len(strategies) < 4:
        fail(f"{source_label} macro_strategy_report needs at least four strategies")
    text = clean_text(report).lower()
    for phrase in ["yang-mills", "wilson", "schwinger", "reflection positivity", "continuum", "hilbert", "spectral gap"]:
        if phrase not in text:
            fail(f"{source_label} macro strategy report lacks physics phrase `{phrase}`")
    previous = 101
    for index, strategy in enumerate(strategies, start=1):
        for field in [
            "strategy_id",
            "title",
            "route_family",
            "priority_score",
            "macro_thesis",
            "physics_picture",
            "why_now",
            "evidence_from_story",
            "what_to_compute_next",
            "success_condition",
            "failure_or_pivot_condition",
            "linked_literature_refs",
            "active_skills",
            "epistemic_status",
        ]:
            if not strategy.get(field):
                fail(f"{source_label} macro strategy {index} missing {field}")
        score = int(strategy.get("priority_score", 0))
        if score > previous:
            fail(f"{source_label} macro strategies must be sorted by descending priority")
        previous = score
        for list_field in ["what_to_compute_next", "success_condition", "failure_or_pivot_condition", "linked_literature_refs", "active_skills"]:
            if len(strategy.get(list_field, [])) < 3:
                fail(f"{source_label} macro strategy {index} needs at least three {list_field}")
        if len(strategy.get("evidence_from_story", [])) < 1:
            fail(f"{source_label} macro strategy {index} needs cycle evidence")


def validate_physics_math_interpretation(payload: dict, source_label: str) -> None:
    report = payload.get("physics_math_interpretation", {})
    if not isinstance(report, dict) or not report:
        fail(f"{source_label} missing physics_math_interpretation")
    for field in ["interpretation_mode", "scope_boundary", "cross_route_synthesis", "interpretations"]:
        if not report.get(field):
            fail(f"{source_label} physics_math_interpretation missing {field}")
    synthesis = report.get("cross_route_synthesis", {})
    for field in ["constructive_spine", "missing_joint_step", "next_mathematical_physics_focus"]:
        if not synthesis.get(field):
            fail(f"{source_label} physics_math_interpretation cross_route_synthesis missing {field}")
    focus = synthesis.get("next_mathematical_physics_focus", [])
    if not isinstance(focus, list) or len(focus) < 3:
        fail(f"{source_label} physics_math_interpretation needs at least three next mathematical-physics focus items")
    routes = report.get("interpretations", [])
    if not isinstance(routes, list) or len(routes) < 2:
        fail(f"{source_label} physics_math_interpretation needs multiple route interpretations")
    if int(report.get("active_route_count", len(routes))) != len(routes):
        fail(f"{source_label} physics_math_interpretation must interpret every active route")
    for index, route in enumerate(routes, start=1):
        for field in [
            "route_family",
            "route_thesis",
            "physical_meaning",
            "load_bearing_bridge",
            "conceptual_bottleneck",
            "why_not_a_proof",
            "mathematical_objects",
            "mechanism_chain",
            "next_lemma_questions",
            "false_positive_controls",
        ]:
            if not route.get(field):
                fail(f"{source_label} physics/math route {index} missing {field}")
        for list_field in ["mathematical_objects", "mechanism_chain", "next_lemma_questions", "false_positive_controls"]:
            if len(route.get(list_field, [])) < 2:
                fail(f"{source_label} physics/math route {index} needs at least two {list_field}")
    joined = clean_text(report).lower()
    for phrase in ["physics", "mathematical", "bridge", "proof", "gauge", "reflection"]:
        if phrase not in joined:
            fail(f"{source_label} physics_math_interpretation lacks `{phrase}`")


def validate_strategy_progression_judge(payload: dict, source_label: str) -> None:
    judge = payload.get("strategy_progression_judge", {})
    if not isinstance(judge, dict) or not judge:
        fail(f"{source_label} missing strategy_progression_judge")
    for field in [
        "judgement_cadence",
        "window",
        "generated_by_skills",
        "evidence_sources",
        "current_strategy",
        "progression_judgement",
        "paper_contribution_readiness",
        "main_problem_alignment",
        "strategy_payoff_table",
        "validation_handoff",
        "epistemic_status",
    ]:
        if not judge.get(field):
            fail(f"{source_label} strategy_progression_judge missing {field}")
    required_skills = {
        "progression-payoff-judge",
        "paper-contribution-readiness-judge",
        "main-problem-alignment-auditor",
    }
    if not required_skills.issubset(set(judge.get("generated_by_skills", []))):
        fail(f"{source_label} strategy_progression_judge missing required judge skills")
    cadence = judge.get("judgement_cadence", {})
    if int(cadence.get("total_valid_research_cycles", 0)) >= 10 and not cadence.get("judgement_due"):
        fail(f"{source_label} strategy judge must run after 10 valid cycles are complete")
    window = judge.get("window", {})
    if int(window.get("window_research_cycle_count", 0)) != min(10, int(cadence.get("total_valid_research_cycles", 0))):
        fail(f"{source_label} strategy judge must cover the rolling latest 10-cycle window")
    progress = judge.get("progression_judgement", {})
    for field in [
        "decision",
        "payoff_potential",
        "progression_score",
        "dimension_scores",
        "summary",
        "contribution_pivot_invariant",
        "what_progressed",
        "what_did_not_progress",
        "next_decisive_test",
        "when_to_stop",
        "do_not_stop_prematurely_if",
    ]:
        if not progress.get(field) and field != "progression_score":
            fail(f"{source_label} strategy progression_judgement missing {field}")
    for field in ["summary_html", "contribution_pivot_invariant_html", "next_decisive_test_html", "when_to_stop_html", "do_not_stop_prematurely_if_html"]:
        validate_inline_math_html(clean_text(progress.get(field)), f"{source_label} strategy judge {field}")
    pivot = clean_text(progress.get("contribution_pivot_invariant", "")).lower()
    for phrase in ["obstruction ladder", "h,k wilson collar", "finite theorem", "scientific contribution"]:
        if phrase not in pivot:
            fail(f"{source_label} strategy judge contribution pivot invariant missing `{phrase}`")
    readiness = judge.get("paper_contribution_readiness", {})
    for field in [
        "candidate_title",
        "smallest_honest_claim",
        "readiness_level",
        "dimension_scores",
        "novelty_argument",
        "main_problem_implication",
        "validation_burden",
        "overclaim_boundary",
        "paper_skeleton",
    ]:
        if not readiness.get(field):
            fail(f"{source_label} paper_contribution_readiness missing {field}")
    alignment = judge.get("main_problem_alignment", {})
    for field in [
        "alignment_class",
        "target_commitments_touched",
        "source_to_target_handoff",
        "proxy_or_transfer_risk",
        "alignment_gain",
        "alignment_loss",
        "repair_action",
        "decision_effect",
    ]:
        if not alignment.get(field):
            fail(f"{source_label} main_problem_alignment missing {field}")
    joined = clean_text(judge).lower()
    for phrase in ["paper", "contribution", "payoff", "alignment", "source object", "target object", "validation"]:
        if phrase not in joined:
            fail(f"{source_label} strategy judge lacks `{phrase}`")


def validate_timeline_paper_lock(payload: dict, source_label: str) -> None:
    paper = payload.get("timeline_paper_report", {})
    if not isinstance(paper, dict) or not paper:
        fail(f"{source_label} missing timeline_paper_report")
    lock = paper.get("paper_narrative_goal_lock", {})
    if not isinstance(lock, dict) or not lock:
        fail(f"{source_label} missing paper_narrative_goal_lock")
    for field in [
        "subgoal_title",
        "coherent_narrative_thesis",
        "anti_infinite_exploration_rule",
        "narrative_spine",
        "included_material_policy",
        "excluded_detail_policy",
        "decisive_next_work",
        "stop_or_demote_when",
        "do_not_stop_prematurely_if",
        "coherence_checks",
    ]:
        if not lock.get(field):
            fail(f"{source_label} paper_narrative_goal_lock missing {field}")
    joined = clean_text(lock).lower()
    for phrase in ["finite", "coherent narrative", "do not add more timeline detail", "schur-feshbach", "h,k wilson collar"]:
        if phrase not in joined:
            fail(f"{source_label} paper_narrative_goal_lock lacks `{phrase}`")


def validate_all_rendered_math_fields(payload: dict, source_label: str) -> None:
    def walk(value: object, path: list[str]) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                walk(child, [*path, str(key)])
            return
        if isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, [*path, str(index)])
            return
        if not isinstance(value, str):
            return
        last = path[-1] if path else ""
        if not (last.endswith("_html") or last in {"latex", "latex_render", "formal_shape"}):
            return
        context = f"{source_label} rendered math field {'.'.join(path)}"
        validate_inline_math_html(value, context)
        for latex in re.findall(r"\\\[(.*?)\\\]", clean_text(value), flags=re.DOTALL):
            validate_tex_fragment(latex, context, "display")

    walk(payload, ["payload"])


def validate_visual_conceptualization_summary(payload: dict, source_label: str) -> None:
    summary = payload.get("visual_conceptualization_summary", {})
    if not isinstance(summary, dict) or not summary:
        fail(f"{source_label} missing visual_conceptualization_summary")
    for field in ["concept_count", "hypothesis_output_count", "route_consequences", "latest_json", "latest_md", "validator"]:
        if not clean_text(summary.get(field)):
            fail(f"{source_label} visual_conceptualization_summary missing {field}")
    if int(summary.get("concept_count", 0)) <= 0:
        fail(f"{source_label} visual_conceptualization_summary must include at least one concept")
    if int(summary.get("hypothesis_output_count", 0)) <= 0:
        fail(f"{source_label} visual_conceptualization_summary must include at least one route output")
    if summary.get("validator") != "agentic/scripts/validate_visual_conceptualization_packet.py":
        fail(f"{source_label} visual_conceptualization_summary points to the wrong validator")


def validate_physical_relevance_impact_summary(payload: dict, source_label: str) -> None:
    summary = payload.get("physical_relevance_impact_summary", {})
    if not isinstance(summary, dict):
        fail(f"{source_label} physical_relevance_impact_summary must be an object")
    for field in [
        "packet_count",
        "persisted_packet_count",
        "legacy_derived_assessment_count",
        "relevance_decision_counts",
        "major_publication_investment_counts",
        "physical_carrier_counts",
        "target_commitment_counts",
        "unification_power_score_counts",
        "active_skills",
        "cycle_gate",
        "validator",
    ]:
        if field not in summary:
            fail(f"{source_label} physical_relevance_impact_summary missing {field}")
    if not isinstance(summary.get("unification_power_score_counts"), dict):
        fail(f"{source_label} physical_relevance_impact_summary unification_power_score_counts must be an object")
    if int(summary.get("packet_count", 0)) and not summary.get("unification_power_score_counts"):
        fail(f"{source_label} physical_relevance_impact_summary must count unification-power scores when packets exist")
    gate_text = clean_text(summary.get("cycle_gate")).lower()
    if "unification power" not in gate_text:
        fail(f"{source_label} physical_relevance_impact_summary cycle_gate must name unification power")
    for cycle in payload.get("all_cycles", []) + payload.get("research_cycles", []) + payload.get("timeline_cycles", []):
        physical = cycle.get("physical_relevance_impact", {})
        if not isinstance(physical, dict) or not clean_text(physical.get("relevance_decision")):
            continue
        if "unification_power_score" not in physical:
            fail(f"{source_label} {cycle.get('cycle_id', 'unknown-cycle')} physical_relevance_impact missing unification_power_score")
        try:
            score = int(physical.get("unification_power_score"))
        except (TypeError, ValueError):
            fail(f"{source_label} {cycle.get('cycle_id', 'unknown-cycle')} unification_power_score must be an integer")
        if score < 0 or score > 5:
            fail(f"{source_label} {cycle.get('cycle_id', 'unknown-cycle')} unification_power_score must be between 0 and 5")


def validate_avenue_literature_gap_summary(payload: dict, source_label: str) -> None:
    summary = payload.get("avenue_literature_gap_summary", {})
    if not isinstance(summary, dict) or not summary:
        fail(f"{source_label} missing avenue_literature_gap_summary")
    for field in [
        "warrant_count",
        "investment_decision_counts",
        "allowed_next_mode_counts",
        "warrants",
        "latest_json",
        "latest_md",
        "active_skill",
        "validator",
        "gate_rule",
    ]:
        if field not in summary:
            fail(f"{source_label} avenue_literature_gap_summary missing {field}")
    if summary.get("active_skill") != "literature-gap-relevance-auditor":
        fail(f"{source_label} avenue_literature_gap_summary active_skill must be literature-gap-relevance-auditor")
    if summary.get("validator") != "agentic/scripts/validate_avenue_literature_gap_warrant.py":
        fail(f"{source_label} avenue_literature_gap_summary points to the wrong validator")
    if int(summary.get("warrant_count", 0)) != len(summary.get("warrants", [])):
        fail(f"{source_label} avenue_literature_gap_summary warrant_count mismatch")
    if int(summary.get("warrant_count", 0)) <= 0:
        fail(f"{source_label} avenue_literature_gap_summary needs at least one warrant")
    gate_rule = clean_text(summary.get("gate_rule")).lower()
    for phrase in ["literature gap", "novelty boundary", "unification power", "route-decision power"]:
        if phrase not in gate_rule:
            fail(f"{source_label} avenue_literature_gap_summary gate_rule missing `{phrase}`")
    for index, warrant in enumerate(summary.get("warrants", []), start=1):
        for field in [
            "avenue_id",
            "avenue_title",
            "investment_decision",
            "allowed_next_modes",
            "smallest_honest_claim",
            "gap_statement",
            "relevance_score",
            "field_impact_score",
            "unification_score",
            "route_decision_score",
            "next_decisive_test",
        ]:
            if field not in warrant or (field not in {"relevance_score", "field_impact_score", "unification_score", "route_decision_score"} and not warrant.get(field)):
                fail(f"{source_label} avenue_literature_gap_summary warrant {index} missing {field}")
        if warrant.get("investment_decision") == "invest_in_avenue" and int(warrant.get("relevance_score", 0)) < 4:
            fail(f"{source_label} avenue_literature_gap_summary warrant {index} invests below relevance threshold")


def visible_report_markup(document: str) -> str:
    main_start = document.find('<main class="shell">')
    mathjax_start = document.find('<script data-embedded-dependency="mathjax-tex-svg"')
    if main_start < 0:
        return document
    if mathjax_start < 0:
        return document[main_start:]
    return document[main_start:mathjax_start]


def validate_visible_math_rendering(document: str, source_label: str, *, require_display_equations: bool = False) -> None:
    visible = visible_report_markup(document)
    if "&lt;=" in visible or "&gt;=" in visible or "&amp;lt;" in visible or "&amp;gt;" in visible:
        fail(f"{source_label} visible report markup contains escaped comparison operators in mathematical prose")
    for code_match in re.finditer(r"<code>(.*?)</code>", visible, flags=re.DOTALL):
        code_text = html_lib.unescape(clean_text(code_match.group(1)))
        if any(marker in code_text for marker in [r"\(", r"\[", "C(", "SIZE(", "N^"]) or re.search(r"_[A-Za-z0-9]", code_text):
            fail(f"{source_label} visible report markup renders mathematical formulae inside code tags")
    if require_display_equations and 'class="equation"' not in visible:
        fail(f"{source_label} visible report markup must render recorded equations as MathJax display blocks")


def main() -> int:
    if not LATEST_JSON.exists():
        print("No discovery marathon report yet; report validator is idle.")
        return 0
    report = load_json_object(LATEST_JSON)
    for field in ["version", "generated_utc", "status", "cycle_count", "research_cycle_count", "synthetic_cycle_count", "branch_summaries", "proof_depth_control_summary", "avenue_literature_gap_summary", "cycle_summaries", "what_actually_changed", "next_queue", "breakthrough_status"]:
        if field not in report:
            fail(f"{rel(LATEST_JSON)} missing {field}")
    if report.get("status") != "no_active_run":
        if not report.get("run_id") or not report.get("target_id"):
            fail(f"{rel(LATEST_JSON)} active report needs run_id and target_id")
        if not isinstance(report.get("branch_summaries"), list) or not report["branch_summaries"]:
            fail(f"{rel(LATEST_JSON)} active report needs branch summaries")
        report_text = clean_text(report).lower()
        for marker in ["controlled interface", "latest learning", "next experiment", "research cycle", "synthetic", "no_breakthrough_claimed"]:
            if marker not in report_text:
                fail(f"{rel(LATEST_JSON)} report lacks `{marker}`")
        proof_depth = report.get("proof_depth_control_summary", {})
        if not isinstance(proof_depth, dict):
            fail(f"{rel(LATEST_JSON)} proof_depth_control_summary must be an object")
        for field in ["packet_count", "release_decision_counts", "transfer_substance_counts", "pressure_kind_counts", "proof_gate"]:
            if field not in proof_depth:
                fail(f"{rel(LATEST_JSON)} proof_depth_control_summary missing {field}")
        if proof_depth.get("packet_count") and "agentic/scripts/validate_proof_depth_control.py" not in clean_text(proof_depth.get("proof_gate")):
            fail(f"{rel(LATEST_JSON)} proof_depth_control_summary points to the wrong validator")
        validate_avenue_literature_gap_summary(report, rel(LATEST_JSON))
    if not LATEST_MD.exists():
        fail(f"missing markdown report {rel(LATEST_MD)}")
    text = LATEST_MD.read_text(encoding="utf-8")
    for phrase in ["Discovery Marathon Report", "What Actually Changed", "Research cycles", "Synthetic smoke/legacy packets", "Proof Depth Control", "Literature Gap Preinvestment Gate", "Branch Learning", "Cycle Learning", "Deep Reviews"]:
        if phrase not in text:
            fail(f"{rel(LATEST_MD)} missing `{phrase}`")
    if not LATEST_HTML.exists():
        fail(f"missing HTML report {rel(LATEST_HTML)}")
    html = LATEST_HTML.read_text(encoding="utf-8")
    validate_self_contained_html(html, rel(LATEST_HTML))
    validate_top_tab_order(html, rel(LATEST_HTML), timeline=False)
    is_yang_mills_report = report.get("target_id") == "yang-mills-existence-and-mass-gap-target"
    if not is_yang_mills_report:
        for phrase in [
            "Discovery Marathon Report",
            "marathon-data",
            "Physics & Maths Strategy",
            "Current Mathematical Story",
            "Research Cycles",
            "Ranked Analyses",
            "Skill Use",
            "Visual Conceptualization",
            "Scientific Contribution Candidates",
            "Result Atlas And Problem Map",
            "Problem Space Map",
            "Derivation Vault",
            "Target Problem And Literature Evolution",
            "General Macro Strategies",
            "Strategy Progression Judge",
            "Accumulated Strategy Story",
            "Branches",
            "Deep Reviews",
            "Job Health",
            "MathJax",
        ]:
            if phrase not in html:
                fail(f"{rel(LATEST_HTML)} missing `{phrase}`")
        try:
            embedded = html.split('<script id="marathon-data" type="application/json">', 1)[1].split("</script>", 1)[0]
            payload = json.loads(html_lib.unescape(embedded))
        except Exception as exc:
            fail(f"{rel(LATEST_HTML)} has invalid embedded marathon-data JSON: {exc}")
        if payload.get("report", {}).get("target_id") != report.get("target_id"):
            fail(f"{rel(LATEST_HTML)} embedded payload target does not match latest JSON target")
        if not payload.get("research_cycles"):
            fail(f"{rel(LATEST_HTML)} embedded payload needs research_cycles")
        if not payload.get("jobs"):
            fail(f"{rel(LATEST_HTML)} embedded payload needs target job summaries")
        skill_summary = payload.get("skill_dispatch_summary", {})
        if not isinstance(skill_summary, dict) or int(skill_summary.get("phase_count", 0)) < 5:
            fail(f"{rel(LATEST_HTML)} embedded payload needs a rich skill_dispatch_summary")
        if int(skill_summary.get("invoked_skill_count", 0)) < 10:
            fail(f"{rel(LATEST_HTML)} must expose substantial skill usage in skill_dispatch_summary")
        if skill_summary.get("missing_required_skills"):
            fail(f"{rel(LATEST_HTML)} reports missing required skills in the discovery loop")
        validate_avenue_literature_gap_summary(payload, rel(LATEST_HTML))
        validate_physical_relevance_impact_summary(payload, rel(LATEST_HTML))
        validate_visual_conceptualization_summary(payload, rel(LATEST_HTML))
        atlas = payload.get("result_subgoal_atlas", {})
        problem_map = payload.get("problem_space_map", {})
        derivation_vault = payload.get("derivation_vault", {})
        if not isinstance(atlas, dict) or not atlas.get("results") or not atlas.get("subgoals"):
            fail(f"{rel(LATEST_HTML)} embedded payload missing result_subgoal_atlas results/subgoals")
        if not isinstance(problem_map, dict) or not problem_map.get("nodes"):
            fail(f"{rel(LATEST_HTML)} embedded payload missing problem_space_map nodes")
        if not isinstance(derivation_vault, dict) or not derivation_vault.get("derivations"):
            fail(f"{rel(LATEST_HTML)} embedded payload missing derivation_vault derivations")
        if clean_text(atlas.get("target_id")) != report.get("target_id"):
            fail(f"{rel(LATEST_HTML)} result_subgoal_atlas target does not match latest JSON target")
        if clean_text(problem_map.get("target_id")) != report.get("target_id"):
            fail(f"{rel(LATEST_HTML)} problem_space_map target does not match latest JSON target")
        if clean_text(derivation_vault.get("target_id")) != report.get("target_id"):
            fail(f"{rel(LATEST_HTML)} derivation_vault target does not match latest JSON target")
        visible = visible_report_markup(html)
        for stale_term in ["Yang-Mills", "Wilson", "OS positivity", "mass gap", "Schwinger"]:
            if report.get("target_id") != "yang-mills-existence-and-mass-gap-target" and stale_term in visible:
                fail(f"{rel(LATEST_HTML)} visible target-neutral report leaked stale term `{stale_term}`")
        for generic_payoff in [
            "A computed obstruction, sign, determinant, or counterexample decides whether the branch must persist",
            "The calculation names the regulator or limiting regime",
            "cutoff-uniform estimates",
            "Euclidean construction/reconstruction bridge",
        ]:
            if report.get("target_id") == "p-vs-np-target" and generic_payoff in visible:
                fail(f"{rel(LATEST_HTML)} P vs NP report contains non-content-specific payoff/control phrase `{generic_payoff}`")
        if report.get("target_id") == "p-vs-np-target":
            for required_skill in [
                "pvsnp-conceptual-pressure-localizer",
                "pvsnp-qualitative-complexity-reasoner",
                "pvsnp-impossibility-theorem-forger",
                "pvsnp-symbolic-complexity-auditor",
                "pvsnp-negative-tactic-selector",
                "pvsnp-inference-quality-controller",
                "pvsnp-reduction-consistency-reviewer",
                "pvsnp-quantifier-uniformity-reviewer",
                "pvsnp-barrier-specificity-reviewer",
            ]:
                if required_skill not in visible:
                    fail(f"{rel(LATEST_HTML)} P vs NP report does not expose required skill `{required_skill}`")
            negative_tactics = payload.get("pvsnp_negative_tactics", {})
            if not isinstance(negative_tactics, dict) or not negative_tactics.get("recommendations"):
                fail(f"{rel(LATEST_HTML)} P vs NP report missing embedded pvsnp_negative_tactics")
            if "Negative Tactic Control" not in visible:
                fail(f"{rel(LATEST_HTML)} P vs NP report missing visible Negative Tactic Control panel")
            inference_quality = payload.get("pvsnp_inference_quality", {})
            if not isinstance(inference_quality, dict) or not inference_quality.get("summary"):
                fail(f"{rel(LATEST_HTML)} P vs NP report missing embedded pvsnp_inference_quality")
            if "Inference Quality Control" not in visible:
                fail(f"{rel(LATEST_HTML)} P vs NP report missing visible Inference Quality Control panel")
        validate_renderable_equations(payload, rel(LATEST_HTML))
        validate_renderable_cycle_prose(payload, rel(LATEST_HTML))
        validate_all_rendered_math_fields(payload, rel(LATEST_HTML))
        validate_visible_math_rendering(html, rel(LATEST_HTML), require_display_equations=True)
        if not LATEST_TIMELINE_HTML.exists():
            fail(f"missing timeline HTML report {rel(LATEST_TIMELINE_HTML)}")
        timeline_html = LATEST_TIMELINE_HTML.read_text(encoding="utf-8")
        validate_self_contained_html(timeline_html, rel(LATEST_TIMELINE_HTML))
        validate_top_tab_order(timeline_html, rel(LATEST_TIMELINE_HTML), timeline=True)
        validate_visible_math_rendering(timeline_html, rel(LATEST_TIMELINE_HTML))
        for phrase in ["Discovery Marathon Full Timeline", "marathon-data", "Timeline", "Job Health"]:
            if phrase not in timeline_html:
                fail(f"{rel(LATEST_TIMELINE_HTML)} missing `{phrase}`")
        try:
            timeline_embedded = timeline_html.split('<script id="marathon-data" type="application/json">', 1)[1].split("</script>", 1)[0]
            timeline_payload = json.loads(html_lib.unescape(timeline_embedded))
        except Exception as exc:
            fail(f"{rel(LATEST_TIMELINE_HTML)} has invalid embedded marathon-data JSON: {exc}")
        if not timeline_payload.get("timeline_mode"):
            fail(f"{rel(LATEST_TIMELINE_HTML)} embedded payload must mark timeline_mode")
        if not timeline_payload.get("timeline_cycles"):
            fail(f"{rel(LATEST_TIMELINE_HTML)} embedded payload must include visible timeline cycles")
        timeline_skill_summary = timeline_payload.get("skill_dispatch_summary", {})
        if int(timeline_skill_summary.get("invoked_skill_count", 0)) < 10:
            fail(f"{rel(LATEST_TIMELINE_HTML)} must expose substantial skill usage in skill_dispatch_summary")
        validate_avenue_literature_gap_summary(timeline_payload, rel(LATEST_TIMELINE_HTML))
        validate_physical_relevance_impact_summary(timeline_payload, rel(LATEST_TIMELINE_HTML))
        validate_visual_conceptualization_summary(timeline_payload, rel(LATEST_TIMELINE_HTML))
        for field in ["result_subgoal_atlas", "problem_space_map", "derivation_vault"]:
            value = timeline_payload.get(field, {})
            if not isinstance(value, dict) or not value:
                fail(f"{rel(LATEST_TIMELINE_HTML)} embedded payload missing {field}")
        for phrase in ["Result Atlas And Problem Map", "Problem Space Map", "Derivation Vault"]:
            if phrase not in timeline_html:
                fail(f"{rel(LATEST_TIMELINE_HTML)} missing `{phrase}`")
        timeline_visible = visible_report_markup(timeline_html)
        for stale_term in ["Yang-Mills", "Wilson", "OS positivity", "mass gap", "Schwinger"]:
            if report.get("target_id") != "yang-mills-existence-and-mass-gap-target" and stale_term in timeline_visible:
                fail(f"{rel(LATEST_TIMELINE_HTML)} visible target-neutral report leaked stale term `{stale_term}`")
        for generic_payoff in [
            "A computed obstruction, sign, determinant, or counterexample decides whether the branch must persist",
            "The calculation names the regulator or limiting regime",
            "cutoff-uniform estimates",
            "Euclidean construction/reconstruction bridge",
        ]:
            if report.get("target_id") == "p-vs-np-target" and generic_payoff in timeline_visible:
                fail(f"{rel(LATEST_TIMELINE_HTML)} P vs NP report contains non-content-specific payoff/control phrase `{generic_payoff}`")
        if report.get("target_id") == "p-vs-np-target":
            for required_skill in [
                "pvsnp-conceptual-pressure-localizer",
                "pvsnp-qualitative-complexity-reasoner",
                "pvsnp-impossibility-theorem-forger",
                "pvsnp-symbolic-complexity-auditor",
                "pvsnp-negative-tactic-selector",
                "pvsnp-inference-quality-controller",
                "pvsnp-reduction-consistency-reviewer",
                "pvsnp-quantifier-uniformity-reviewer",
                "pvsnp-barrier-specificity-reviewer",
            ]:
                if required_skill not in timeline_visible:
                    fail(f"{rel(LATEST_TIMELINE_HTML)} P vs NP timeline does not expose required skill `{required_skill}`")
            negative_tactics = timeline_payload.get("pvsnp_negative_tactics", {})
            if not isinstance(negative_tactics, dict) or not negative_tactics.get("recommendations"):
                fail(f"{rel(LATEST_TIMELINE_HTML)} P vs NP timeline missing embedded pvsnp_negative_tactics")
            if "Negative Tactic Control" not in timeline_visible:
                fail(f"{rel(LATEST_TIMELINE_HTML)} P vs NP timeline missing visible Negative Tactic Control panel")
            inference_quality = timeline_payload.get("pvsnp_inference_quality", {})
            if not isinstance(inference_quality, dict) or not inference_quality.get("summary"):
                fail(f"{rel(LATEST_TIMELINE_HTML)} P vs NP timeline missing embedded pvsnp_inference_quality")
            if "Inference Quality Control" not in timeline_visible:
                fail(f"{rel(LATEST_TIMELINE_HTML)} P vs NP timeline missing visible Inference Quality Control panel")
        first_visible_cycle = clean_text(timeline_payload.get("timeline_cycles", [{}])[0].get("cycle_id"))
        if report.get("target_id") != "yang-mills-existence-and-mass-gap-target" and first_visible_cycle != "cycle-0001":
            fail(f"{rel(LATEST_TIMELINE_HTML)} target-neutral timeline should start at first persisted research cycle, found {first_visible_cycle}")
        print(
            f"validated discovery marathon report for {report.get('target_id')} "
            f"with {len(payload.get('research_cycles', []))} research cycles"
        )
        return 0
    for phrase in [
        "Discovery Marathon Report",
        "marathon-data",
        "Physics & Maths Strategy",
        "Cross-Route Synthesis",
        "Next Mathematical-Physics Focus",
        "Latest Valid Cycles",
        "All Marathon Jobs",
        "Research Cycle Timeline",
        "Current Ranked Next-Analysis Queue",
        "Qualitative Mechanistic Graph",
        "What This Graph Is Saying",
        "Mechanism In Plain Terms",
        "Relations That Matter Now",
        "What The User Should Watch",
        "Gedanken Experiments",
        "PMP Probes",
        "Scientific Contribution Monitor",
        "Good Enough",
        "Anti-Infinite Progression Rule",
        "Target Problem And Literature Evolution",
        "How The Literature Evolved",
        "References",
        "General Macro Strategies",
        "Current Strategy Families",
        "Strategy Progression Judge",
        "Paper Narrative Goal Lock",
        "Anti-infinite exploration rule",
        "Paper-Level Contribution Readiness",
        "Main Problem Alignment",
        "Accumulated Physics Story",
        "When To Stop",
        "How This Adds To The Global Problem",
        "How does it add to the global problem",
        "Literature Gap Gate",
        "Visual Conceptualization",
        "MathJax",
    ]:
        if phrase not in html:
            fail(f"{rel(LATEST_HTML)} missing `{phrase}`")
    try:
        embedded = html.split('<script id="marathon-data" type="application/json">', 1)[1].split("</script>", 1)[0]
        payload = json.loads(html_lib.unescape(embedded))
    except Exception as exc:
        fail(f"{rel(LATEST_HTML)} has invalid embedded marathon-data JSON: {exc}")
    if not payload.get("research_cycles"):
        fail(f"{rel(LATEST_HTML)} embedded payload needs research_cycles")
    if not payload.get("jobs"):
        fail(f"{rel(LATEST_HTML)} embedded payload needs accumulated jobs")
    if not payload.get("quality", {}).get("all_markers_ok"):
        fail(f"{rel(LATEST_HTML)} embedded quality must preserve marker checks")
    validate_renderable_equations(payload, rel(LATEST_HTML))
    validate_renderable_cycle_prose(payload, rel(LATEST_HTML))
    validate_storyline(payload, rel(LATEST_HTML), timeline=False)
    validate_summary_analysis_control(payload, rel(LATEST_HTML))
    validate_ranked_queue(payload, rel(LATEST_HTML), timeline=False)
    validate_paper_argument_priority_queue(payload, rel(LATEST_HTML), timeline=False)
    validate_decisive_next_move_queue(payload, rel(LATEST_HTML), timeline=False)
    validate_qualitative_graph(payload, rel(LATEST_HTML))
    validate_gedanken_experiments(payload, rel(LATEST_HTML))
    validate_scientific_contribution_monitor(payload, rel(LATEST_HTML))
    validate_target_literature_evolution(payload, rel(LATEST_HTML))
    validate_physics_math_interpretation(payload, rel(LATEST_HTML))
    validate_macro_strategy_report(payload, rel(LATEST_HTML))
    validate_strategy_progression_judge(payload, rel(LATEST_HTML))
    validate_timeline_paper_lock(payload, rel(LATEST_HTML))
    validate_avenue_literature_gap_summary(payload, rel(LATEST_HTML))
    validate_physical_relevance_impact_summary(payload, rel(LATEST_HTML))
    validate_visual_conceptualization_summary(payload, rel(LATEST_HTML))
    validate_all_rendered_math_fields(payload, rel(LATEST_HTML))
    pmp = payload.get("parsimonious_probe_layer", {})
    if not isinstance(pmp, dict) or not pmp.get("symbolic_matrix_probe") or not pmp.get("analytic_estimate_obligations"):
        fail(f"{rel(LATEST_HTML)} missing parsimonious_probe_layer symbolic and analytic artifacts")
    if not pmp.get("finite_algebra_interfaces"):
        fail(f"{rel(LATEST_HTML)} missing finite algebra interfaces in parsimonious_probe_layer")
    if not pmp.get("proof_safe"):
        fail(f"{rel(LATEST_HTML)} parsimonious_probe_layer is not proof-safe")
    if not LATEST_TIMELINE_HTML.exists():
        fail(f"missing timeline HTML report {rel(LATEST_TIMELINE_HTML)}")
    timeline_html = LATEST_TIMELINE_HTML.read_text(encoding="utf-8")
    validate_self_contained_html(timeline_html, rel(LATEST_TIMELINE_HTML))
    validate_top_tab_order(timeline_html, rel(LATEST_TIMELINE_HTML), timeline=True)
    for phrase in [
        "Discovery Marathon Full Timeline",
        "Physics & Maths Strategy",
        "Cross-Route Synthesis",
        "Next Mathematical-Physics Focus",
        "Content-Specific Full Timeline",
        "marathon-data",
        "timeline_mode",
        "Timeline From cycle-0174",
        "Integrated Reasoning Operations",
        "Next Analyses Queue",
        "How does it add to the global problem",
        "Literature Gap Gate",
        "Current Ranked Next-Analysis Queue",
        "Qualitative Mechanistic Graph",
        "What This Graph Is Saying",
        "Mechanism In Plain Terms",
        "Relations That Matter Now",
        "What The User Should Watch",
        "Gedanken Experiments",
        "PMP Probes",
        "Scientific Contribution Monitor",
        "Good Enough",
        "Anti-Infinite Progression Rule",
        "Target Problem And Literature Evolution",
        "How The Literature Evolved",
        "References",
        "General Macro Strategies",
        "Current Strategy Families",
        "Strategy Progression Judge",
        "Paper Narrative Goal Lock",
        "Anti-infinite exploration rule",
        "Paper-Level Contribution Readiness",
        "Main Problem Alignment",
        "Visual Conceptualization",
        "next_experiment_queue",
        "MathJax",
    ]:
        if phrase not in timeline_html:
            fail(f"{rel(LATEST_TIMELINE_HTML)} missing `{phrase}`")
    try:
        timeline_embedded = timeline_html.split('<script id="marathon-data" type="application/json">', 1)[1].split("</script>", 1)[0]
        timeline_payload = json.loads(html_lib.unescape(timeline_embedded))
    except Exception as exc:
        fail(f"{rel(LATEST_TIMELINE_HTML)} has invalid embedded marathon-data JSON: {exc}")
    if not timeline_payload.get("timeline_mode"):
        fail(f"{rel(LATEST_TIMELINE_HTML)} embedded payload must mark timeline_mode")
    if int(timeline_payload.get("timeline_start_cycle", 0)) != 174:
        fail(f"{rel(LATEST_TIMELINE_HTML)} visible timeline must start at cycle-0174")
    if len(timeline_payload.get("all_cycles", [])) < int(report.get("cycle_count", 0)):
        fail(f"{rel(LATEST_TIMELINE_HTML)} all_cycles must accumulate every persisted cycle")
    if len(timeline_payload.get("all_cycles", [])) <= len(timeline_payload.get("research_cycles", [])):
        fail(f"{rel(LATEST_TIMELINE_HTML)} full timeline must include more than research cycles")
    timeline_cycles = timeline_payload.get("timeline_cycles", [])
    if not timeline_cycles:
        fail(f"{rel(LATEST_TIMELINE_HTML)} timeline_cycles must not be empty")
    first_cycle_id = clean_text(timeline_cycles[0].get("cycle_id"))
    if first_cycle_id != "cycle-0174":
        fail(f"{rel(LATEST_TIMELINE_HTML)} visible timeline starts at {first_cycle_id}, expected cycle-0174")
    if len(timeline_cycles) >= len(timeline_payload.get("all_cycles", [])):
        fail(f"{rel(LATEST_TIMELINE_HTML)} visible timeline should exclude pre-cycle-0174 setup packets")
    queue = timeline_payload.get("timeline_next_experiment_queue", [])
    if not isinstance(queue, list) or len(queue) < len(timeline_payload.get("research_cycles", [])) // 2:
        fail(f"{rel(LATEST_TIMELINE_HTML)} next_experiment_queue must accumulate next experiment bullets")
    if not all(clean_text(item.get("next_experiment")) for item in queue if isinstance(item, dict)):
        fail(f"{rel(LATEST_TIMELINE_HTML)} next_experiment_queue contains empty next_experiment")
    if queue and clean_text(queue[0].get("cycle_id")) != "cycle-0174":
        fail(f"{rel(LATEST_TIMELINE_HTML)} visible next_experiment_queue should start at cycle-0174")
    validate_renderable_equations(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_renderable_cycle_prose(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_storyline(timeline_payload, rel(LATEST_TIMELINE_HTML), timeline=True)
    validate_summary_analysis_control(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_ranked_queue(timeline_payload, rel(LATEST_TIMELINE_HTML), timeline=True)
    validate_paper_argument_priority_queue(timeline_payload, rel(LATEST_TIMELINE_HTML), timeline=True)
    validate_decisive_next_move_queue(timeline_payload, rel(LATEST_TIMELINE_HTML), timeline=True)
    validate_qualitative_graph(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_gedanken_experiments(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_scientific_contribution_monitor(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_target_literature_evolution(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_physics_math_interpretation(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_macro_strategy_report(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_strategy_progression_judge(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_timeline_paper_lock(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_avenue_literature_gap_summary(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_physical_relevance_impact_summary(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_visual_conceptualization_summary(timeline_payload, rel(LATEST_TIMELINE_HTML))
    validate_all_rendered_math_fields(timeline_payload, rel(LATEST_TIMELINE_HTML))
    timeline_pmp = timeline_payload.get("parsimonious_probe_layer", {})
    if not isinstance(timeline_pmp, dict) or not timeline_pmp.get("symbolic_matrix_probe") or not timeline_pmp.get("analytic_estimate_obligations"):
        fail(f"{rel(LATEST_TIMELINE_HTML)} missing parsimonious_probe_layer symbolic and analytic artifacts")
    if not timeline_pmp.get("finite_algebra_interfaces"):
        fail(f"{rel(LATEST_TIMELINE_HTML)} missing finite algebra interfaces in parsimonious_probe_layer")
    if not timeline_pmp.get("proof_safe"):
        fail(f"{rel(LATEST_TIMELINE_HTML)} parsimonious_probe_layer is not proof-safe")
    print(f"validated {rel(LATEST_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
