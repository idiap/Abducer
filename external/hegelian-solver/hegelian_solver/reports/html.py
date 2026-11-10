# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""HTML report rendering from public reasoning logs.

The report has two audiences at once: a reader who wants the plain-language story of
what the solver did and why, and a reader who wants the formal record (predicates,
obligations, preservation maps, ranking gates) behind each step. Every step renders
both: a narrative line up top, a formal panel built from the step's structured
`machine_summary`, and the raw JSON underneath for full machine-readability.
"""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path
from typing import Any

from hegelian_solver.schemas import ReasoningLog

PASS_WORDS = {"passed", "pass", "accept", "validated", "true"}
WARN_WORDS = {"partial", "provisional", "accept_as_branch", "needs_evidence", "unknown", "planned", "defer", "underdetermined", "fragile"}
FAIL_WORDS = {"failed", "fail", "reject", "rejected", "collapsed", "false"}

def esc(value: Any) -> str:
    return escape(str(value))


def _pretty(value: Any) -> str:
    return escape(json.dumps(value, indent=2, sort_keys=True))


def json_details(summary: str, value: Any, *, class_name: str = "json-details") -> str:
    return f"""
    <details class="{esc(class_name)}">
      <summary>{esc(summary)}</summary>
      <pre>{_pretty(value)}</pre>
    </details>
    """


def _latex_text(value: Any, *, limit: int = 96) -> str:
    text = str(value)
    if len(text) > limit:
        text = text[: limit - 1] + "..."
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "_": r"\_",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "$": r"\$",
    }
    return "".join(replacements.get(char, char) for char in text)


def _latex_set(items: list[Any], *, limit: int = 6) -> str:
    if not items:
        return r"\varnothing"
    shown = [rf"\text{{{_latex_text(item)}}}" for item in items[:limit]]
    if len(items) > limit:
        shown.append(r"\ldots")
    return r"\{" + ", ".join(shown) + r"\}"


def _latex_math_set(items: list[str], *, limit: int = 6) -> str:
    if not items:
        return r"\varnothing"
    shown = items[:limit]
    if len(items) > limit:
        shown.append(r"\ldots")
    return r"\{" + ", ".join(shown) + r"\}"


def _latex_operator(value: Any) -> str:
    text = "".join(char if char.isalnum() else "_" for char in str(value)).strip("_")
    return text or "unknown"


def _status_class(status: Any) -> str:
    text = str(status).strip().lower()
    if text in PASS_WORDS:
        return "pass"
    if text in FAIL_WORDS:
        return "fail"
    if text in WARN_WORDS:
        return "warn"
    return "neutral"


def pill(label: Any, status: Any | None = None) -> str:
    klass = _status_class(status if status is not None else label)
    return f'<span class="pill {klass}">{esc(label)}</span>'


def chips(items: list[Any], empty: str = "none recorded") -> str:
    if not items:
        return f'<p class="muted">{esc(empty)}</p>'
    return '<div class="chips">' + "".join(f'<span class="chip">{esc(item)}</span>' for item in items) + "</div>"


def bullet_list(items: list[Any], empty: str = "None recorded.") -> str:
    if not items:
        return f'<p class="muted">{esc(empty)}</p>'
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def _split_summary(summary: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+(?=[A-Z])", summary.strip()) if part.strip()]


def _summary_points(summary: str) -> str:
    points = _split_summary(summary)
    if not points:
        return '<p class="summary">No run summary available.</p>'
    return '<ul class="summary-points">' + "".join(f"<li>{esc(point)}</li>" for point in points) + "</ul>"


def kv_grid(pairs: list[tuple[str, Any]]) -> str:
    rows = []
    for key, value in pairs:
        if isinstance(value, (list, tuple)):
            rendered = chips(list(value)) if value else '<p class="muted">none</p>'
        elif isinstance(value, dict):
            rendered = json_details(f"{key} JSON", value) if value else '<p class="muted">none</p>'
        else:
            rendered = esc(value) if value not in (None, "") else '<span class="muted">none</span>'
        rows.append(f"<div class='kv-row'><div class='kv-key'>{esc(key)}</div><div class='kv-val'>{rendered}</div></div>")
    return "<div class='kv-grid'>" + "".join(rows) + "</div>"


def table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return '<p class="muted">None recorded.</p>'
    head = "".join(f"<th>{esc(header)}</th>" for header in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def _checks(checks: list[dict[str, Any]]) -> str:
    if not checks:
        return '<p class="muted">No checks recorded.</p>'
    rows = []
    for check in checks:
        status = check.get("status")
        detail = {k: v for k, v in check.items() if k not in {"name", "status"}}
        rows.append([esc(check.get("name", "check")), pill(status), json_details("Check detail JSON", detail) if detail else ""])
    return table(["Check", "Status", "Detail"], rows)


# ---------------------------------------------------------------------------
# Stage-specific formal panels
# ---------------------------------------------------------------------------


def _formal_domain_profile(summary: dict[str, Any]) -> str:
    return kv_grid(
        [
            ("Domain", summary.get("domain")),
            ("Schema kind", summary.get("schema_kind")),
            ("Required fields", summary.get("required_fields", [])),
            ("Failure taxonomy", summary.get("failure_taxonomy", [])),
            ("Discovery taxonomy", summary.get("discovery_taxonomy", [])),
            ("Validation gates", summary.get("validation_gates", [])),
            ("Ranking features", summary.get("ranking_features", [])),
            ("Refs used", summary.get("refs_used", [])),
        ]
    )


def _formal_concept_formalization(summary: dict[str, Any]) -> str:
    counts = kv_grid(
        [
            ("Domain", summary.get("domain")),
            ("Tasks", summary.get("task_count")),
            ("Examples", summary.get("example_count")),
            ("Counterexamples", summary.get("counterexample_count")),
            ("Reported failures", summary.get("reported_failure_count")),
            ("Preservation constraints", summary.get("preservation_count")),
            ("Source refs", summary.get("source_refs", [])),
        ]
    )
    formal = summary.get("formal_analysis") or {}
    material = summary.get("material_analysis") or {}
    epistemic = summary.get("epistemic_profile") or {}
    triad = "".join(
        f"""<div class="triad-card">
              <h4>{title}</h4>
              {json_details(f"{title} JSON", block) if block else '<p class="muted">not provided</p>'}
            </div>"""
        for title, block in (("Formal analysis", formal), ("Material analysis", material), ("Epistemic profile", epistemic))
    )
    return counts + f'<div class="triad">{triad}</div>'


def _formal_task_evidence(summary: dict[str, Any]) -> str:
    return kv_grid(
        [
            ("Tasks curated", summary.get("task_count")),
            ("Evidence items", summary.get("evidence_count")),
            ("Missing evidence", summary.get("missing_evidence", [])),
        ]
    )


def _formal_failures(summary: dict[str, Any]) -> str:
    rows = []
    for failure in summary.get("failures", []):
        rows.append(
            [
                esc(failure.get("label")),
                esc(failure.get("failed_obligation")),
                pill(failure.get("severity")),
                esc(", ".join(failure.get("repair_target", []))) or '<span class="muted">none</span>',
                esc(failure.get("witness")),
            ]
        )
    return table(["Label", "Failed obligation", "Severity", "Repair target", "Witness"], rows)


def _formal_discovery(summary: dict[str, Any]) -> str:
    rows = []
    for signal in summary.get("signals", []):
        score = signal.get("score") or {}
        rows.append(
            [
                esc(signal.get("label")),
                esc(signal.get("candidate_move")),
                esc(signal.get("candidate_concept") or ""),
                esc(", ".join(f"{k}={v}" for k, v in score.items())) or '<span class="muted">n/a</span>',
            ]
        )
    return table(["Label", "Candidate move", "Candidate concept", "Score"], rows)


def _formal_candidates(summary: dict[str, Any]) -> str:
    cards = []
    for candidate in summary.get("candidates", []):
        target = candidate.get("target_concept") or {}
        cards.append(
            f"""
            <div class="card">
              <div class="card-head">
                <span class="card-title">{esc(candidate.get("operator"))}</span>
                <span class="card-sub">&rarr; {esc(target.get("name", target.get("id", "unnamed target")))}</span>
              </div>
              <p>{esc(candidate.get("resolution_mechanism"))}</p>
              <div class="kv-grid">
                <div class="kv-row"><div class="kv-key">Changed structure</div><div class="kv-val">{chips(candidate.get("changed_structure", []))}</div></div>
                <div class="kv-row"><div class="kv-key">Expected obligations</div><div class="kv-val">{chips(candidate.get("expected_obligations", []))}</div></div>
                <div class="kv-row"><div class="kv-key">Residual limits</div><div class="kv-val">{chips(candidate.get("residual_limits", []))}</div></div>
                <div class="kv-row"><div class="kv-key">Preservation map</div><div class="kv-val">{json_details("Preservation map JSON", candidate.get("preservation_map", {}))}</div></div>
              </div>
            </div>
            """
        )
    return "".join(cards) if cards else '<p class="muted">No candidates generated.</p>'


def _formal_validation(summary: dict[str, Any]) -> str:
    sections = []
    for packet in summary.get("validation_packets", []):
        rows = []
        for obligation in packet.get("obligations", []):
            rows.append(
                [
                    esc(obligation.get("kind")),
                    esc(obligation.get("statement")),
                    esc(obligation.get("method")),
                    pill(obligation.get("status")),
                    esc(obligation.get("blocker") or ""),
                ]
            )
        sections.append(
            f"""
            <div class="card">
              <div class="card-head">
                <span class="card-title">{esc(packet.get("candidate_id"))}</span>
                {pill(packet.get("summary"), "fail" if packet.get("hard_gate_failures") else "passed")}
              </div>
              {table(["Kind", "Statement", "Method", "Status", "Blocker"], rows)}
              {('<p class="warn-text">Hard gate failures: ' + esc("; ".join(packet.get("hard_gate_failures", []))) + '</p>') if packet.get("hard_gate_failures") else ""}
            </div>
            """
        )
    return "".join(sections) if sections else '<p class="muted">No validation packets.</p>'


def _formal_ranking(summary: dict[str, Any]) -> str:
    rows = []
    for decision in summary.get("decisions", []):
        scores = decision.get("scores") or {}
        rows.append(
            [
                esc(decision.get("candidate_id")),
                pill(decision.get("decision")),
                esc(f"{decision.get('score', 0):.3f}" if isinstance(decision.get("score"), (int, float)) else decision.get("score")),
                esc(", ".join(f"{k}={v:.2f}" if isinstance(v, (int, float)) else f"{k}={v}" for k, v in scores.items())),
                esc("; ".join(decision.get("reasons", []))),
            ]
        )
    return table(["Candidate", "Decision", "Score", "Score breakdown", "Reasons"], rows)


def _formal_refinement(summary: dict[str, Any]) -> str:
    header = kv_grid(
        [
            ("Max iterations", summary.get("max_iterations")),
            ("Iterations run", summary.get("iterations_run")),
            ("Stop reason", pill(summary.get("stop_reason"))),
        ]
    )
    rows = []
    for entry in summary.get("iterations", []):
        rows.append(
            [
                str(entry.get("iteration")),
                esc(entry.get("concept_id")),
                str(entry.get("trigger_count")),
                str(entry.get("candidate_count")),
                pill(entry.get("top_decision")),
                f"{entry.get('top_score', 0):.3f}" if isinstance(entry.get("top_score"), (int, float)) else esc(entry.get("top_score")),
            ]
        )
    return header + table(["Iteration", "Concept", "Triggers", "Candidates", "Top decision", "Top score"], rows)


def _formal_creativity(summary: dict[str, Any]) -> str:
    rows = []
    for analysis in summary.get("creativity_analyses", []):
        rows.append(
            [
                esc(analysis.get("operator")),
                pill(analysis.get("operation", "").replace("_", " "), "neutral"),
                pill(analysis.get("repair_vs_affordance")),
                esc(analysis.get("source_pressure", {}).get("label")),
                chips(analysis.get("new_affordance", []), empty="none (repair only)"),
            ]
        )
    return table(["Operator", "Operation", "Repair vs affordance", "Source pressure", "New affordance"], rows)


def _formal_graph(summary: dict[str, Any]) -> str:
    nodes = summary.get("nodes", {})
    edges = summary.get("edges", {})
    rejected = summary.get("rejected_candidates", [])
    counts = kv_grid([("Nodes", len(nodes)), ("Edges", len(edges)), ("Rejected candidates", len(rejected))])
    rows = []
    for edge in edges.values():
        rows.append(
            [
                esc(edge.get("source")),
                esc(edge.get("relation")),
                esc(edge.get("target")),
                pill(edge.get("status")),
                chips(edge.get("residual_limits", []), empty="none"),
            ]
        )
    return counts + table(["Source", "Relation", "Target", "Status", "Residual limits"], rows)


def _formal_explanation(summary: dict[str, Any]) -> str:
    text = summary.get("explanation", "")
    return f'<div class="explanation-box">{esc(text)}</div>' if text else '<p class="muted">No explanation text.</p>'


def _whole_reasoning_notation(log: ReasoningLog) -> str:
    """Render a compact LaTeX-style trace over the full reasoning log."""

    by_stage = {step.stage: step.machine_summary for step in log.steps}
    domain = _latex_text(log.domain)
    tasks = by_stage.get("concept_formalization", {}).get("task_count", 0)
    evidence = by_stage.get("task_evidence", {}).get("evidence_count", 0)
    failures = [
        f"f_{{{index}}}"
        for index, _failure in enumerate(by_stage.get("failure_classification", {}).get("failures", []), start=1)
    ]
    signals = [
        f"d_{{{index}}}"
        for index, _signal in enumerate(by_stage.get("discovery_mining", {}).get("signals", []), start=1)
    ]
    candidate_records = by_stage.get("candidate_generation", {}).get("candidates", [])
    candidates = [
        rf"\kappa_{{{index}}}"
        for index, _candidate in enumerate(candidate_records, start=1)
    ]
    validations = []
    for index, packet in enumerate(by_stage.get("validation", {}).get("validation_packets", []), start=1):
        obligations = packet.get("obligations", [])
        passed = sum(1 for obligation in obligations if str(obligation.get("status")).lower() in PASS_WORDS)
        validations.append(rf"v_{{{index}}}={passed}/{len(obligations)}")
    decisions = by_stage.get("ranking", {}).get("decisions", [])
    ranked = [
        rf"r_{{{index}}}: \kappa_{{{index}}} \mapsto \operatorname{{{_latex_operator(decision.get('decision', 'unknown'))}}}"
        for index, decision in enumerate(decisions, start=1)
    ]
    top_symbol = r"\varnothing"
    if decisions:
        top_id = decisions[0].get("candidate_id")
        for index, candidate in enumerate(candidate_records, start=1):
            if candidate.get("id") == top_id:
                top_symbol = rf"\kappa_{{{index}}}"
                break
        else:
            top_symbol = r"\kappa^\star"
    refinement = by_stage.get("reflective_refinement", {})
    graph = by_stage.get("graph_update", {})
    edge_count = len(graph.get("edges", {}))
    node_count = len(graph.get("nodes", {}))

    lines = [
        r"\begin{aligned}",
        rf"C_0 &\in \mathsf{{{domain}}} \\",
        rf"\mathcal{{T}} &= \{{t_i\}}_{{i=1}}^{{{tasks}}}, \qquad "
        rf"\mathcal{{E}} = \{{e_i\}}_{{i=1}}^{{{evidence}}} \\",
        rf"\mathcal{{F}}(C_0) &= {_latex_math_set(failures)} \\",
        rf"\mathcal{{D}}(C_0) &= {_latex_math_set(signals)} \\",
        rf"\mathcal{{K}} &= \operatorname{{Generate}}(C_0,\mathcal{{F}},\mathcal{{D}})"
        rf" = {_latex_math_set(candidates, limit=8)} \\",
        rf"\mathcal{{V}} &= \operatorname{{Validate}}(\mathcal{{K}}) = {_latex_math_set(validations, limit=8)} \\",
        rf"\mathcal{{R}} &= \operatorname{{Rank}}(\mathcal{{K}},\mathcal{{V}}) = {_latex_math_set(ranked, limit=8)} \\",
        rf"\kappa^\star &= {top_symbol}, \qquad "
        rf"\rho = \operatorname{{{_latex_operator(refinement.get('stop_reason', 'not_recorded'))}}}, \qquad "
        rf"n_\rho = {refinement.get('iterations_run', 0)} \\",
        rf"G_1 &= G_0 \cup N_{{{node_count}}} \cup E_{{{edge_count}}}, \qquad "
        rf"\sigma = \operatorname{{{_latex_operator(log.final_status)}}}",
        r"\end{aligned}",
    ]
    return "\n".join(lines)


def _whole_reasoning_legend(log: ReasoningLog) -> str:
    by_stage = {step.stage: step.machine_summary for step in log.steps}
    rows = [[r"\(C_0\)", esc(log.concept_name)]]
    for index, failure in enumerate(by_stage.get("failure_classification", {}).get("failures", []), start=1):
        rows.append(
            [
                rf"\(f_{{{index}}}\)",
                f"{esc(failure.get('label', 'failure'))}: {esc(failure.get('failed_obligation', ''))}",
            ]
        )
    for index, signal in enumerate(by_stage.get("discovery_mining", {}).get("signals", []), start=1):
        rows.append(
            [
                rf"\(d_{{{index}}}\)",
                f"{esc(signal.get('label', 'signal'))}: {esc(signal.get('candidate_move', ''))}",
            ]
        )
    for index, candidate in enumerate(by_stage.get("candidate_generation", {}).get("candidates", []), start=1):
        target = candidate.get("target_concept") or {}
        target_name = target.get("name") or target.get("id") or "target"
        rows.append(
            [
                rf"\(\kappa_{{{index}}}\)",
                f"{esc(candidate.get('operator', 'operator'))} -> {esc(target_name)}",
            ]
        )
    for index, decision in enumerate(by_stage.get("ranking", {}).get("decisions", []), start=1):
        rows.append(
            [
                rf"\(r_{{{index}}}\)",
                f"{esc(decision.get('candidate_id', 'candidate'))}: {esc(decision.get('decision', 'unknown'))}",
            ]
        )
    return table(["Symbol", "Meaning"], rows)


def _task_uses(concept: dict[str, Any]) -> list[str]:
    uses = []
    for task in concept.get("tasks", []):
        if isinstance(task, dict):
            name = task.get("name", "task")
            goal = task.get("goal", "")
            uses.append(f"{name}: {goal}" if goal else str(name))
        else:
            uses.append(str(task))
    return uses


def _phrase_list(items: list[Any], *, empty: str = "none recorded", limit: int = 4) -> str:
    if not items:
        return empty
    shown = [str(item) for item in items[:limit]]
    suffix = " and related cases" if len(items) > limit else ""
    return ", ".join(shown) + suffix


def _definition_text(concept: dict[str, Any], fallback_name: str) -> str:
    role = concept.get("role")
    if role:
        return str(role)
    uses = _task_uses(concept)
    if uses:
        return f"{fallback_name} is defined by its use in {uses[0]}"
    return f"{fallback_name} is the concept under dialectical transformation in this run."


def _render_concept_definition(concept: dict[str, Any], *, fallback_name: str) -> str:
    name = concept.get("name") or fallback_name
    formal = concept.get("formal_analysis", {})
    material = concept.get("material_analysis", {})
    epistemic = concept.get("epistemic_profile", {})
    tasks = _task_uses(concept)
    return f"""
      <h4>{esc(name)}</h4>
      <p><strong>Definition.</strong> {esc(_definition_text(concept, str(name)))}</p>
      <div class="kv-grid compact">
        <div class="kv-row"><div class="kv-key">Domain</div><div class="kv-val">{esc(concept.get("domain", "unknown"))}</div></div>
        <div class="kv-row"><div class="kv-key">Status</div><div class="kv-val">{pill(concept.get("status", "source"))}</div></div>
        <div class="kv-row"><div class="kv-key">Use</div><div class="kv-val">{bullet_list(tasks, empty="No explicit use/task recorded.")}</div></div>
        <div class="kv-row"><div class="kv-key">Examples</div><div class="kv-val">{chips(concept.get("examples", []), empty="none")}</div></div>
        <div class="kv-row"><div class="kv-key">Preservation constraints</div><div class="kv-val">{chips(concept.get("preservation", []), empty="none")}</div></div>
        <div class="kv-row"><div class="kv-key">Formal definition hooks</div><div class="kv-val">{chips(formal.get("obligations", []), empty="none")}</div></div>
        <div class="kv-row"><div class="kv-key">Material grounding</div><div class="kv-val">{esc(material.get("practice") or material.get("evidence") or material.get("phenomena") or "none recorded")}</div></div>
        <div class="kv-row"><div class="kv-key">Epistemic status</div><div class="kv-val">{esc(epistemic.get("uncertainty", "unknown"))}</div></div>
        <div class="kv-row"><div class="kv-key">Signature</div><div class="kv-val">{json_details("Signature JSON", concept.get("signature", {}))}</div></div>
      </div>
    """


def _concrete_concept_evolution(log: ReasoningLog) -> str:
    by_stage = {step.stage: step.machine_summary for step in log.steps}
    candidates = by_stage.get("candidate_generation", {}).get("candidates", [])
    if candidates:
        first_target = candidates[0].get("target_concept", {})
    else:
        first_target = {}
    source = {
        key: first_target.get(key)
        for key in (
            "domain",
            "role",
            "signature",
            "tasks",
            "examples",
            "preservation",
            "formal_analysis",
            "material_analysis",
            "epistemic_profile",
            "source_refs",
        )
    }
    source.update({"name": log.concept_name, "status": "source"})
    source_card = f"""
      <div class="evolution-card source">
        <div class="evolution-label">Source concept</div>
        {_render_concept_definition(source, fallback_name=log.concept_name)}
      </div>
    """
    successor_cards = []
    for index, candidate in enumerate(candidates, start=1):
        target = candidate.get("target_concept") or {}
        relation = candidate.get("preservation_map", {}).get("relation", "transforms")
        successor_cards.append(
            f"""
            <div class="evolution-card">
              <div class="evolution-label">Successor concept \\(\\kappa_{{{index}}}\\)</div>
              <p class="transition-line">
                \\(C_0 \\xrightarrow{{\\operatorname{{{_latex_operator(candidate.get("operator", "operator"))}}}}} \\kappa_{{{index}}}\\)
                <span>{esc(relation)} via {esc(candidate.get("resolution_mechanism", "candidate transformation"))}</span>
              </p>
              {_render_concept_definition(target, fallback_name=f"successor {index}")}
              <div class="kv-grid compact">
                <div class="kv-row"><div class="kv-key">Changed structure</div><div class="kv-val">{chips(candidate.get("changed_structure", []), empty="none")}</div></div>
                <div class="kv-row"><div class="kv-key">Expected obligations</div><div class="kv-val">{chips(candidate.get("expected_obligations", []), empty="none")}</div></div>
                <div class="kv-row"><div class="kv-key">Residual limits</div><div class="kv-val">{chips(candidate.get("residual_limits", []), empty="none")}</div></div>
              </div>
            </div>
            """
        )
    return f"""
      <section class="step">
        <h2>Concrete Concept Evolution</h2>
        <p class="muted">Definitions and uses for the concrete concepts before the compact formal trace.</p>
        <div class="evolution-flow">
          {source_card}
          {''.join(successor_cards) if successor_cards else '<p class="muted">No successor concepts generated.</p>'}
        </div>
      </section>
    """


def _source_concept_from_log(log: ReasoningLog) -> dict[str, Any]:
    by_stage = {step.stage: step.machine_summary for step in log.steps}
    candidates = by_stage.get("candidate_generation", {}).get("candidates", [])
    first_target = candidates[0].get("target_concept", {}) if candidates else {}
    source = {
        key: first_target.get(key)
        for key in (
            "domain",
            "role",
            "signature",
            "tasks",
            "examples",
            "preservation",
            "formal_analysis",
            "material_analysis",
            "epistemic_profile",
            "source_refs",
            "reported_failures",
        )
    }
    source.update({"name": log.concept_name, "status": "source"})
    return source


def _use_case_motivation(log: ReasoningLog) -> str:
    by_stage = {step.stage: step.machine_summary for step in log.steps}
    source = _source_concept_from_log(log)
    material = source.get("material_analysis", {}) or {}
    failures = by_stage.get("failure_classification", {}).get("failures", [])
    signals = by_stage.get("discovery_mining", {}).get("signals", [])
    tasks = _task_uses(source)
    examples = source.get("examples", [])
    stakes = material.get("stakes") or material.get("practice") or material.get("phenomena")
    failure_line = "; ".join(
        f"{failure.get('label')}: {failure.get('failed_obligation')}" for failure in failures
    )
    signal_line = "; ".join(
        f"{signal.get('label')} suggests {signal.get('candidate_move')}" for signal in signals
    )
    paragraphs = [
        (
            f"Big picture: this scenario asks how a concept changes when its intended use becomes "
            f"larger than its original structure. {source.get('name')} is not treated as a static label; "
            f"it is treated as a working concept whose role is: {_definition_text(source, log.concept_name)}"
        ),
        (
            f"The target use is {tasks[0] if tasks else 'the declared task set'}, and the examples "
            f"{_phrase_list(examples, empty='record the intended cases')} make the pressure visible in concrete terms. "
            "The point of the use case is to show why a successor concept is needed, not merely to rename the old one."
        ),
        (
            f"The stakes are {stakes}. If that pressure is ignored, the concept keeps being used for tasks "
            "that its own structure does not yet support." if stakes else
            "The stakes are to make the concept's intended use explicit enough to test instead of relying on an informal expectation."
        ),
        (
            f"The motivating failure is {failure_line}. This is the concrete reason the solver treats the case as a development problem rather than a description problem." if failure_line else
            "The motivating pressure comes from the solver's discovery and validation stages rather than a predeclared failure."
        ),
        (
            f"The discovery signal adds direction: {signal_line}. That signal keeps the proposed successor connected to a recognizable pattern instead of making the repair arbitrary." if signal_line else
            "No separate discovery signal was required to motivate the use case."
        ),
    ]
    return f"""
      <section class="step">
        <h2>Use Case Motivation</h2>
        <p class="muted">Generated by the `hegelian-use-case-motivation-writer` skill pattern from the use case role, tasks, examples, stakes, and trigger artifacts.</p>
        <div class="motivation-box">
          {''.join(f'<p>{esc(paragraph)}</p>' for paragraph in paragraphs)}
        </div>
      </section>
    """


def _selected_candidate_bundle(log: ReasoningLog) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    by_stage = {step.stage: step.machine_summary for step in log.steps}
    candidates = by_stage.get("candidate_generation", {}).get("candidates", [])
    packets = by_stage.get("validation", {}).get("validation_packets", [])
    decisions = by_stage.get("ranking", {}).get("decisions", [])
    if not candidates:
        return {}, {}, {}
    decision = decisions[0] if decisions else {}
    candidate_id = decision.get("candidate_id") or candidates[0].get("id")
    candidate = next((item for item in candidates if item.get("id") == candidate_id), candidates[0])
    packet = next((item for item in packets if item.get("candidate_id") == candidate.get("id")), {})
    return candidate, packet, decision


def _full_explanation(log: ReasoningLog) -> str:
    by_stage = {step.stage: step.machine_summary for step in log.steps}
    candidate, packet, decision = _selected_candidate_bundle(log)
    if not candidate:
        return f"""
        <section class="step">
          <h2>Full Explanation</h2>
          <p>No candidate successor was generated, so the report cannot expand the transition beyond the run summary.</p>
        </section>
        """
    target = candidate.get("target_concept") or {}
    source = _source_concept_from_log(log)
    material = source.get("material_analysis", {}) or {}
    examples = source.get("examples", [])
    tasks = _task_uses(source)
    failures = by_stage.get("failure_classification", {}).get("failures", [])
    signals = by_stage.get("discovery_mining", {}).get("signals", [])
    failure_text = "; ".join(
        f"{failure.get('label')}: {failure.get('failed_obligation')}" for failure in failures
    ) or "no typed failure was recorded"
    signal_text = "; ".join(
        f"{signal.get('label')}: {signal.get('candidate_move')}" for signal in signals
    ) or "no discovery signal was recorded"
    obligations = packet.get("obligations", [])
    passed = [item.get("kind") for item in obligations if item.get("status") == "passed"]
    open_items = [item.get("kind") for item in obligations if item.get("status") != "passed"]
    target_name = target.get("name") or candidate.get("id", "successor concept")
    relation = candidate.get("preservation_map", {}).get("relation", "transforms")
    preserved = candidate.get("preservation_map", {}).get("kind", "preservation map")
    preservation = target.get("preservation", [])
    residuals = candidate.get("residual_limits", [])
    stakes = material.get("stakes") or material.get("practice") or material.get("phenomena") or "the declared practice"
    score = decision.get("score", "n/a")
    decision_name = decision.get("decision", "not ranked")
    sections = [
        (
            "Big Picture",
            [
                (
                    f"The report is about concept growth under pressure. {log.concept_name} has a role "
                    f"before the solver touches it: {_definition_text(source, log.concept_name)}"
                ),
                (
                    f"In this use case, the concept is asked to support {tasks[0] if tasks else 'the declared task set'}. "
                    f"The examples {_phrase_list(examples, empty='provided by the use case')} show the intended family of cases, "
                    f"while the stakes are {stakes}."
                ),
            ],
        ),
        (
            "What Breaks",
            [
                (
                    f"The pressure is concrete: {failure_text}. This is why the run treats the source concept as incomplete "
                    "for its intended use, rather than merely poorly described."
                ),
                (
                    f"The discovery side adds: {signal_text}. That matters because it points to a patterned repair direction "
                    "instead of leaving the solver with an unconstrained list of possible changes."
                ),
            ],
        ),
        (
            "Why This Successor",
            [
                (
                    f"The selected successor is {target_name}. It is produced by {candidate.get('operator')} and recorded "
                    f"as a `{relation}` move in the graph."
                ),
                (
                    f"The intuitive claim is: {candidate.get('resolution_mechanism')}. In other words, the successor is meant "
                    "to add just enough structure for the motivating pressure to become tractable."
                ),
            ],
        ),
        (
            "What Is Preserved",
            [
                (
                    "A development is only useful if it does not erase what made the old concept work. "
                    f"Here preservation is mediated by {preserved}."
                ),
                (
                    f"The protected content is {_phrase_list(preservation, empty='the declared preservation constraints')}. "
                    "That is the report's non-collapse requirement: the successor should repair the limit without flattening the predecessor."
                ),
            ],
        ),
        (
            "How It Was Checked",
            [
                (
                    f"The validation packet checks {len(obligations)} obligations. Passed obligations: "
                    f"{_phrase_list(passed, empty='none')}."
                ),
                (
                    f"Open obligations: {_phrase_list(open_items, empty='none')}. These open items mark the remaining distance "
                    "between a plausible repair and a fully validated successor."
                ),
            ],
        ),
        (
            "How To Read The Result",
            [
                (
                    f"The ranking decision is {decision_name} with score {score}. Read this as a candidate repair that is strong "
                    "enough to keep in the graph, not as the final word on the concept."
                ),
                (
                    f"Residual limits remain: {_phrase_list(residuals, empty='none declared')}. The next work is to close the open "
                    "obligations with domain-specific proof, evidence, examples, or counterexamples."
                ),
            ],
        ),
    ]
    return f"""
      <section class="step">
        <h2>Full Explanation</h2>
        <div class="full-explanation">
          {''.join(f'<section class="explanation-part"><h3>{esc(title)}</h3>{"".join(f"<p>{esc(paragraph)}</p>" for paragraph in paragraphs)}</section>' for title, paragraphs in sections)}
        </div>
      </section>
    """


OPERATION_DISPLAY = {
    "closure_completion": "Closure completion",
    "abstraction_interface_discovery": "Abstraction / interface discovery",
    "invariance_reparameterization": "Invariance / reparameterization",
    "quotienting_redundancy_removal": "Quotienting / redundancy removal",
    "localization_regime_restriction": "Localization / regime restriction",
    "externalization_or_tooling": "Externalization / tooling",
    "bridge_mediation": "Bridge mediation",
    "latent_carrier_introduction": "Latent carrier introduction",
    "governance_safety_scaffold": "Governance / safety scaffold",
}


def _render_creativity_analysis(analysis: dict[str, Any]) -> str:
    source = analysis.get("source_pressure", {}) or {}
    operation = analysis.get("operation", "")
    residual_todos = analysis.get("residual_todos", [])
    return f"""
    <div class="card creativity-card">
      <div class="card-head">
        <span class="card-title">{esc(analysis.get("operator"))}</span>
        {pill(OPERATION_DISPLAY.get(operation, operation), "neutral")}
        {pill(analysis.get("repair_vs_affordance"))}
      </div>
      <p>{esc(analysis.get("why_creative_not_corrective"))}</p>
      <p class="muted">
        Triggered by {esc(source.get("label"))} ({esc(source.get("kind"))}): {esc(analysis.get("latent_tension"))}.
        The move {esc(analysis.get("creative_reframing"))}.
      </p>
      <details>
        <summary>Structured creativity payload</summary>
        <div class="kv-grid">
          <div class="kv-row"><div class="kv-key">New constructive resource</div><div class="kv-val">{esc(analysis.get("new_constructive_resource"))}</div></div>
          <div class="kv-row"><div class="kv-key">New affordance</div><div class="kv-val">{chips(analysis.get("new_affordance", []), empty="none (repair only)")}</div></div>
          <div class="kv-row"><div class="kv-key">Preservation under transformation</div><div class="kv-val">{chips(analysis.get("preservation_under_transformation", []))}</div></div>
          <div class="kv-row"><div class="kv-key">Generative payoff</div><div class="kv-val">{chips(analysis.get("generative_payoff", []))}</div></div>
          <div class="kv-row"><div class="kv-key">Creative risks</div><div class="kv-val">{chips(analysis.get("creative_risks", []))}</div></div>
          <div class="kv-row"><div class="kv-key">Downstream concept seeds</div><div class="kv-val">{chips(analysis.get("downstream_concept_seeds", []))}</div></div>
        </div>
        {f'<p class="warn-text"><strong>Residual TODOs:</strong> {esc("; ".join(residual_todos))}</p>' if residual_todos else ""}
      </details>
    </div>
    """


def _render_creativity_section(log: ReasoningLog) -> str:
    analyses = log.creativity_analyses
    if not analyses:
        return """
        <section class="step" id="creativity-analysis">
          <h2>Conceptual Creativity Analysis</h2>
          <p class="muted">No transformation candidates were available to analyze for this run.</p>
        </section>
        """
    repair_count = sum(1 for item in analyses if item.get("repair_vs_affordance") == "repair")
    affordance_count = sum(1 for item in analyses if item.get("repair_vs_affordance") == "affordance_creation")
    mixed_count = sum(1 for item in analyses if item.get("repair_vs_affordance") == "mixed")
    cards = "".join(_render_creativity_analysis(item) for item in analyses)
    return f"""
    <section class="step" id="creativity-analysis">
      <h2>Conceptual Creativity Analysis</h2>
      <p class="muted">
        Every candidate is classified before the concrete concept evolution and formal notation below:
        {affordance_count} introduce a new affordance, {mixed_count} are mixed repair-and-affordance moves,
        and {repair_count} are pure repairs with no new affordance claimed.
      </p>
      {cards}
    </section>
    """


STAGE_RENDERERS = {
    "domain_profile": _formal_domain_profile,
    "concept_formalization": _formal_concept_formalization,
    "task_evidence": _formal_task_evidence,
    "failure_classification": _formal_failures,
    "discovery_mining": _formal_discovery,
    "candidate_generation": _formal_candidates,
    "validation": _formal_validation,
    "ranking": _formal_ranking,
    "conceptual_creativity": _formal_creativity,
    "reflective_refinement": _formal_refinement,
    "graph_update": _formal_graph,
    "explanation": _formal_explanation,
}


def _formal_panel(stage: str, machine_summary: dict[str, Any]) -> str:
    renderer = STAGE_RENDERERS.get(stage)
    if renderer is None:
        return json_details("Machine summary JSON", machine_summary)
    try:
        return renderer(machine_summary)
    except Exception:  # pragma: no cover - defensive fallback for unexpected shapes
        return json_details("Machine summary JSON", machine_summary)


# ---------------------------------------------------------------------------
# Mechanism dossier rendering
# ---------------------------------------------------------------------------


def _render_abduction(packet: dict[str, Any]) -> str:
    shape = packet.get("required_mediation_shape", {})
    inference_rows = [
        [pill(item.get("role")), esc(item.get("claim")), esc(item.get("warrant"))]
        for item in shape.get("inference_commitments", [])
    ]
    hypothesis_cards = []
    for hyp in packet.get("mechanism_hypotheses", []):
        formal = hyp.get("formal_mediation", {})
        material = hyp.get("material_mediation", {})
        hypothesis_cards.append(
            f"""
            <div class="card">
              <div class="card-head">
                <span class="card-title">{esc(hyp.get("label"))}</span>
                {pill(hyp.get("hypothesis_type"), "neutral")}
              </div>
              <p>{esc(hyp.get("abductive_claim"))}</p>
              <p class="muted">If this existed: {esc(hyp.get("if_this_existed_then"))}</p>
              <div class="kv-grid">
                <div class="kv-row"><div class="kv-key">New predicates</div><div class="kv-val">{chips(formal.get("new_predicates", []))}</div></div>
                <div class="kv-row"><div class="kv-key">New maps</div><div class="kv-val">{chips(formal.get("new_maps", []))}</div></div>
                <div class="kv-row"><div class="kv-key">Constraints</div><div class="kv-val">{chips(formal.get("constraints", []))}</div></div>
                <div class="kv-row"><div class="kv-key">Actors</div><div class="kv-val">{chips(material.get("actors", []))}</div></div>
                <div class="kv-row"><div class="kv-key">Practices / infrastructure</div><div class="kv-val">{chips(material.get("practices_or_infrastructure", []))}</div></div>
                <div class="kv-row"><div class="kv-key">Explanatory gain</div><div class="kv-val">{chips(hyp.get("explanatory_gain", []))}</div></div>
                <div class="kv-row"><div class="kv-key">New risks</div><div class="kv-val">{chips(hyp.get("new_risks", []))}</div></div>
                <div class="kv-row"><div class="kv-key">Disconfirming observations</div><div class="kv-val">{chips(hyp.get("disconfirming_observations", []))}</div></div>
              </div>
            </div>
            """
        )
    rejected_rows = [
        [esc(item.get("label")), esc(item.get("reason"))] for item in packet.get("rejected_hypotheses", [])
    ]
    return f"""
      <h4>Required mediation shape</h4>
      <p>{esc(shape.get("incompatibility_to_mediate", ""))}</p>
      <div class="kv-grid">
        <div class="kv-row"><div class="kv-key">Commitments to preserve</div><div class="kv-val">{chips(shape.get("commitments_to_preserve", []))}</div></div>
        <div class="kv-row"><div class="kv-key">Missing relation / process</div><div class="kv-val">{chips(shape.get("missing_relation_or_process", []))}</div></div>
      </div>
      <h4>Inference commitments</h4>
      {table(["Role", "Claim", "Warrant"], inference_rows)}
      <h4>Mechanism hypotheses</h4>
      {''.join(hypothesis_cards) or '<p class="muted">None recorded.</p>'}
      <h4>Rejected hypotheses</h4>
      {table(["Label", "Reason"], rejected_rows)}
    """


def _render_requirements(packet: dict[str, Any]) -> str:
    requirement_rows = []
    for requirement in packet.get("requirements", []):
        requirement_rows.append(
            [
                esc(requirement.get("kind")),
                pill(requirement.get("necessity_status"), "neutral"),
                esc(requirement.get("statement")),
                esc(requirement.get("validation_method")),
                esc(requirement.get("failure_mode_if_missing")),
            ]
        )
    map_rows = [
        [esc(m.get("map_type")), esc(m.get("source_commitment")), esc(m.get("target_commitment")), esc(m.get("statement"))]
        for m in packet.get("mediation_maps", [])
    ]
    return f"""
      <p>{esc(packet.get("mechanism_role", ""))}</p>
      <h4>Requirements</h4>
      {table(["Kind", "Necessity", "Statement", "Validation method", "Failure mode if missing"], requirement_rows)}
      <h4>Mediation maps</h4>
      {table(["Type", "Source commitment", "Target commitment", "Statement"], map_rows)}
      <div class="kv-grid">
        <div class="kv-row"><div class="kv-key">Material preconditions</div><div class="kv-val">{chips(packet.get("material_preconditions", []))}</div></div>
        <div class="kv-row"><div class="kv-key">Implementation surfaces</div><div class="kv-val">{chips(packet.get("implementation_surfaces", []))}</div></div>
        <div class="kv-row"><div class="kv-key">Validation obligations</div><div class="kv-val">{chips(packet.get("validation_obligations", []))}</div></div>
        <div class="kv-row"><div class="kv-key">Residual limits</div><div class="kv-val">{chips(packet.get("residual_limits", []))}</div></div>
      </div>
    """


def _render_critique(packet: dict[str, Any]) -> str:
    test_rows = []
    for test in packet.get("counterfactual_tests", []):
        test_rows.append(
            [
                esc(test.get("test_type")),
                esc(test.get("scenario")),
                esc(test.get("failure_signal")),
                chips(test.get("affected_requirements", []), empty="none"),
                pill(test.get("result")),
            ]
        )
    return f"""
      <div class="kv-grid">
        <div class="kv-row"><div class="kv-key">Overall status</div><div class="kv-val">{pill(packet.get("overall_status"))}</div></div>
      </div>
      <h4>Counterfactual tests</h4>
      {table(["Test type", "Scenario", "Failure signal", "Affected requirements", "Result"], test_rows)}
      <div class="kv-grid">
        <div class="kv-row"><div class="kv-key">Hidden assumptions</div><div class="kv-val">{chips(packet.get("hidden_assumptions", []))}</div></div>
        <div class="kv-row"><div class="kv-key">Collapse risks</div><div class="kv-val">{chips(packet.get("collapse_risks", []))}</div></div>
        <div class="kv-row"><div class="kv-key">Alternative mechanisms still live</div><div class="kv-val">{chips(packet.get("alternative_mechanisms_still_live", []))}</div></div>
        <div class="kv-row"><div class="kv-key">Required revisions</div><div class="kv-val">{chips(packet.get("required_revisions", []))}</div></div>
      </div>
    """


def _render_todos(packet: dict[str, Any]) -> str:
    groups = []
    for group in packet.get("todo_groups", []):
        rows = []
        for todo in group.get("todos", []):
            rows.append(
                [
                    pill(todo.get("class", todo.get("class_")), "neutral"),
                    esc(todo.get("task")),
                    pill(todo.get("priority"), "neutral"),
                    "yes" if todo.get("blocks_candidate_acceptance") else "no",
                    esc(todo.get("acceptance_criterion")),
                ]
            )
        groups.append(
            f"""
            <details class="todo-group">
              <summary>{esc(group.get("group_id"))}</summary>
              <p>{esc(group.get("purpose"))}</p>
              {table(["Class", "Task", "Priority", "Blocks acceptance", "Acceptance criterion"], rows)}
            </details>
            """
        )
    return f"""
      {''.join(groups) or '<p class="muted">No TODO groups.</p>'}
      <div class="kv-grid">
        <div class="kv-row"><div class="kv-key">Immediate next actions</div><div class="kv-val">{chips(packet.get("immediate_next_actions", []))}</div></div>
        <div class="kv-row"><div class="kv-key">Stop conditions</div><div class="kv-val">{chips(packet.get("stop_conditions", []))}</div></div>
      </div>
    """


def _render_mechanism_dossier(dossier: dict[str, Any]) -> str:
    abduction = dossier.get("mechanism_abduction_packet")
    requirements = dossier.get("mechanism_requirements_packet")
    critique = dossier.get("mechanism_counterfactual_critique")
    todos = dossier.get("mechanism_todo_packet")
    sub_sections = []
    if abduction:
        sub_sections.append(("Abduction", _render_abduction(abduction)))
    if requirements:
        sub_sections.append(("Requirements", _render_requirements(requirements)))
    if critique:
        sub_sections.append(("Counterfactual critique", _render_critique(critique)))
    if todos:
        sub_sections.append(("TODO backlog", _render_todos(todos)))
    rendered = "".join(
        f"""
        <details class="mechanism-stage"{' open' if title != 'TODO backlog' else ''}>
          <summary>{esc(title)}</summary>
          {body}
        </details>
        """
        for title, body in sub_sections
    )
    return f"""
    <section class="step mechanism" id="mechanism-{esc(dossier.get('id'))}">
      <h2>{esc(dossier.get("mechanism_name"))}</h2>
      <p class="stage">{esc(dossier.get("field"))} &middot; crisis: {esc(dossier.get("source_tension_ref"))}</p>
      <p>{esc(dossier.get("scenario_summary", ""))}</p>
      {rendered}
    </section>
    """


# ---------------------------------------------------------------------------
# Top-level report
# ---------------------------------------------------------------------------


def _toc(log: ReasoningLog) -> str:
    items = "".join(f'<li><a href="#step-{step.index}">{step.index}. {esc(step.title)}</a></li>' for step in log.steps)
    mechanism_items = "".join(
        f'<li><a href="#mechanism-{esc(m.get("id"))}">{esc(m.get("mechanism_name"))}</a></li>' for m in log.mechanisms
    )
    return f"""
    <nav class="toc">
      <h3>Conceptual creativity</h3>
      <ol><li><a href="#creativity-analysis">Conceptual Creativity Analysis</a></li></ol>
      <h3>Reasoning steps</h3>
      <ol>{items}</ol>
      {f'<h3>Mechanism dossiers</h3><ol>{mechanism_items}</ol>' if mechanism_items else ""}
    </nav>
    """


def render_html_report(log: ReasoningLog) -> str:
    steps = []
    for step in log.steps:
        steps.append(
            f"""
            <section class="step" id="step-{step.index}">
              <div class="step-head">
                <h2>{step.index}. {esc(step.title)}</h2>
                <span class="stage-tag">{esc(step.stage)}</span>
              </div>
              <p class="narrative">{esc(step.human_summary)}</p>
              <p class="rationale">{esc(step.public_rationale)}</p>
              <div class="grid">
                <div><h3>Inputs</h3>{chips(step.inputs, empty="none")}</div>
                <div><h3>Outputs</h3>{chips(step.outputs, empty="none")}</div>
              </div>
              <h3>Checks</h3>
              {_checks(step.checks)}
              <h3>Formal record</h3>
              <div class="formal-panel">{_formal_panel(step.stage, step.machine_summary)}</div>
              {(f'<div class="epistemic-line"><strong>Assumptions:</strong> {", ".join(esc(a) for a in step.assumptions)}</div>') if step.assumptions else ""}
              {(f'<div class="epistemic-line warn-text"><strong>Unknowns:</strong> {", ".join(esc(u) for u in step.unknowns)}</div>') if step.unknowns else ""}
              {json_details("Raw machine summary JSON", step.machine_summary)}
            </section>
            """
        )
    mechanism_sections = "".join(_render_mechanism_dossier(m) for m in log.mechanisms)
    status_klass = _status_class(log.final_status)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hegelian Solver Report - {esc(log.concept_name)}</title>
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['\\\\(', '\\\\)']],
        displayMath: [['\\\\[', '\\\\]']]
      }},
      svg: {{ fontCache: 'global' }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
  <style>
    :root {{
      color-scheme: light;
      --ink: #15202b;
      --muted: #5f6b7a;
      --line: #dde3ec;
      --panel: #f7f9fc;
      --accent: #2b5fa8;
      --accent-soft: #eaf1fb;
      --pass: #15724a;
      --pass-bg: #e7f6ee;
      --warn: #9a6300;
      --warn-bg: #fdf3df;
      --fail: #b3261e;
      --fail-bg: #fbe9e7;
      --neutral: #475569;
      --neutral-bg: #eef1f5;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: #ffffff;
      line-height: 1.55;
    }}
    header {{
      padding: 36px max(24px, calc((100vw - 1180px) / 2));
      border-bottom: 1px solid var(--line);
      background: linear-gradient(180deg, #f3f8ff 0%, #ffffff 100%);
    }}
    header .badges {{ margin-top: 10px; }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 24px;
      display: grid;
      grid-template-columns: 240px 1fr;
      gap: 28px;
      align-items: start;
    }}
    .toc {{
      position: sticky;
      top: 24px;
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 16px;
      background: var(--panel);
      font-size: 0.88rem;
    }}
    .toc h3 {{ margin: 0 0 6px; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); }}
    .toc ol {{ margin: 0 0 14px; padding-left: 18px; }}
    .toc a {{ color: var(--accent); text-decoration: none; }}
    .toc a:hover {{ text-decoration: underline; }}
    .content {{ min-width: 0; }}
    h1 {{ margin: 0 0 8px; font-size: 2rem; }}
    h2 {{ margin: 0; font-size: 1.2rem; }}
    h3 {{ margin: 18px 0 8px; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); }}
    h4 {{ margin: 16px 0 6px; font-size: 0.95rem; }}
    .meta, .muted {{ color: var(--muted); }}
    .summary {{ max-width: 900px; font-size: 1.05rem; }}
    .summary-points {{
      max-width: 940px;
      margin: 16px 0 0;
      padding-left: 22px;
      font-size: 1.02rem;
    }}
    .summary-points li {{ margin: 6px 0; }}
    .step {{
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 22px;
      margin: 0 0 18px;
      background: #fff;
    }}
    .step-head {{ display: flex; align-items: baseline; justify-content: space-between; gap: 12px; }}
    .stage-tag {{ font-size: 0.78rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; }}
    .narrative {{ font-size: 1.02rem; margin: 10px 0 4px; }}
    .rationale {{ color: var(--muted); margin: 0 0 10px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }}
    .formal-panel {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 14px 16px; }}
    .evolution-flow {{ display: grid; gap: 14px; }}
    .evolution-card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      background: #fff;
    }}
    .evolution-card.source {{ background: #fbfcff; }}
    .evolution-label {{
      color: var(--muted);
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 8px;
      font-weight: 700;
    }}
    .transition-line {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      color: var(--muted);
      margin: 0 0 12px;
    }}
    .formal-notation {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcff;
      padding: 18px 20px;
      overflow-x: auto;
    }}
    .formal-notation mjx-container {{
      min-width: max-content;
    }}
    table {{ width: 100%; border-collapse: collapse; margin: 8px 0 14px; font-size: 0.9rem; }}
    th, td {{ text-align: left; border-bottom: 1px solid var(--line); padding: 8px; vertical-align: top; }}
    th {{ color: var(--muted); font-weight: 600; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.03em; }}
    pre {{ overflow: auto; border: 1px solid var(--line); border-radius: 6px; background: #fff; padding: 12px; font-size: 0.8rem; }}
    details {{ margin-top: 10px; }}
    details.mechanism-stage {{ border: 1px solid var(--line); border-radius: 8px; padding: 10px 14px; margin: 10px 0; background: var(--panel); }}
    details.todo-details,
    details.todo-group {{ border: 1px solid var(--line); border-radius: 8px; padding: 12px 14px; margin: 10px 0; background: var(--panel); }}
    details.todo-group {{ background: #fff; }}
    details.json-details,
    details.reasoning-log {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px 16px;
      background: var(--panel);
    }}
    details.json-details pre,
    details.reasoning-log pre {{ margin-bottom: 0; }}
    summary {{ cursor: pointer; color: var(--accent); font-weight: 600; }}
    .pill {{ display: inline-block; border-radius: 999px; padding: 2px 10px; font-size: 0.78rem; font-weight: 600; }}
    .pill.pass {{ color: var(--pass); background: var(--pass-bg); }}
    .pill.warn {{ color: var(--warn); background: var(--warn-bg); }}
    .pill.fail {{ color: var(--fail); background: var(--fail-bg); }}
    .pill.neutral {{ color: var(--neutral); background: var(--neutral-bg); }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    .chip {{ background: var(--accent-soft); color: var(--accent); border-radius: 6px; padding: 3px 9px; font-size: 0.82rem; }}
    .kv-grid {{ display: grid; gap: 10px; }}
    .kv-grid.compact {{ gap: 6px; }}
    .kv-row {{ display: grid; grid-template-columns: 220px 1fr; gap: 12px; align-items: start; }}
    .kv-key {{ color: var(--muted); font-size: 0.85rem; padding-top: 2px; }}
    .triad {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-top: 10px; }}
    .triad-card {{ border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; background: #fff; }}
    .card {{ border: 1px solid var(--line); border-radius: 8px; padding: 14px 16px; margin: 10px 0; background: #fff; }}
    .card-head {{ display: flex; align-items: center; justify-content: space-between; gap: 10px; flex-wrap: wrap; }}
    .card-title {{ font-weight: 700; }}
    .card-sub {{ color: var(--muted); }}
    .motivation-box {{ max-width: 900px; }}
    .motivation-box p {{ margin: 0 0 12px; }}
    .full-explanation {{ max-width: 900px; }}
    .explanation-part {{
      border-top: 1px solid var(--line);
      padding-top: 10px;
      margin-top: 12px;
    }}
    .explanation-part:first-child {{ border-top: 0; padding-top: 0; margin-top: 0; }}
    .full-explanation p {{ margin: 0 0 12px; }}
    .explanation-box {{ white-space: pre-wrap; background: var(--accent-soft); border-radius: 8px; padding: 14px 16px; }}
    .epistemic-line {{ margin-top: 8px; font-size: 0.9rem; }}
    .warn-text {{ color: var(--warn); }}
    section.mechanism h2 {{ color: var(--accent); }}
  </style>
</head>
<body>
  <header>
    <h1>Hegelian Solver Report</h1>
    <p class="meta">Run {esc(log.run_id)} &middot; {esc(log.domain)} &middot; concept {esc(log.concept_name)}</p>
    <div class="badges">{pill(log.final_status, status_klass)}</div>
    {_summary_points(log.summary)}
  </header>
  <main>
    {_toc(log)}
    <div class="content">
      {_use_case_motivation(log)}
      {_full_explanation(log)}
      {_render_creativity_section(log)}
      <section class="step">
        <h2>Machine Index</h2>
        <div class="formal-panel">{json_details("Machine index JSON", log.machine_index)}</div>
      </section>
      {_concrete_concept_evolution(log)}
      <section class="step">
        <h2>Formal Reasoning Notation</h2>
        <p class="muted">A compact LaTeX-style reconstruction of the complete solver trace.</p>
        <div class="formal-notation">\\[{esc(_whole_reasoning_notation(log))}\\]</div>
        <h3>Notation Legend</h3>
        {_whole_reasoning_legend(log)}
      </section>
      {''.join(steps)}
      {mechanism_sections}
      <section class="step">
        <details class="reasoning-log" id="reasoning-log-json">
          <summary>Reasoning Log</summary>
          <p class="muted">The JSON below is the same public reasoning log used to render this report.</p>
          <pre>{_pretty(log.model_dump(mode="json"))}</pre>
        </details>
      </section>
    </div>
  </main>
</body>
</html>
"""


def write_html_report(log: ReasoningLog, path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_html_report(log))
    return target
