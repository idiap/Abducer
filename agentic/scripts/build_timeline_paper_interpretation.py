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
"""Build a structured interpretation IR from the full timeline report."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, rel, stable_id, utc_now, write_json
from target_profiles import target_profile
from timeline_paper_common import FULL_TIMELINE_HTML, coverage_from_units, load_source_bundle, unit


OUT_DIR = ROOT / "agentic/reports/timeline_paper_interpretation"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
SCHEMA = ROOT / "agentic/spec/timeline_paper_interpretation.schema.json"


def add_if(units: list[dict[str, Any]], **kwargs: Any) -> None:
    if clean_text(kwargs.get("content")):
        units.append(unit(**kwargs))


def interpret_problem_literature(bundle: dict[str, Any], units: list[dict[str, Any]]) -> None:
    lit = bundle["target_literature"]
    problem = lit.get("problem_statement", {}) if isinstance(lit.get("problem_statement"), dict) else {}
    add_if(
        units,
        family="target_literature_evolution",
        kind="problem_context",
        title=lit.get("problem_name") or "Target problem",
        content=problem.get("accessible") or problem.get("formal_shape"),
        argument_role="motivation",
        disposition="main_body",
        source="agentic/reports/target_literature_evolution/latest.json:problem_statement",
    )
    for stage in lit.get("literature_stages", []) if isinstance(lit.get("literature_stages"), list) else []:
        if isinstance(stage, dict):
            add_if(
                units,
                family="target_literature_evolution",
                kind="literature_claim",
                title=f"{stage.get('period', '')}: {stage.get('title', '')}",
                content=f"{stage.get('core_shift', '')} What remained open: {stage.get('what_remained_open', '')}",
                argument_role="novelty_boundary",
                disposition="main_body",
                source="agentic/reports/target_literature_evolution/latest.json:literature_stages",
                evidence_status="literature_backed",
            )
    for ref in lit.get("references", []) if isinstance(lit.get("references"), list) else []:
        if isinstance(ref, dict):
            add_if(
                units,
                family="target_literature_evolution",
                kind="reference_role",
                title=ref.get("ref_id") or ref.get("title"),
                content=f"{ref.get('title', '')}. Supports: {ref.get('supports', '')}. Limitation: {ref.get('limitation', '')}",
                argument_role="novelty_boundary",
                disposition="appendix",
                source="agentic/reports/target_literature_evolution/latest.json:references",
                evidence_status="literature_backed",
                extra={"reference_id": clean_text(ref.get("ref_id")), "url": clean_text(ref.get("url"))},
            )


def interpret_timeline_cycles(bundle: dict[str, Any], units: list[dict[str, Any]]) -> None:
    cycles = bundle["payload"].get("timeline_cycles", [])
    if not isinstance(cycles, list):
        return
    for cycle in cycles:
        if not isinstance(cycle, dict):
            continue
        cycle_id = clean_text(cycle.get("cycle_id"))
        branch = clean_text(cycle.get("branch_title")) or cycle_id
        add_if(
            units,
            family="timeline_cycles",
            kind="strategy_shift",
            title=branch,
            content=cycle.get("mathematical_learning"),
            argument_role="failure_learning" if "not" in clean_text(cycle.get("mathematical_learning")).lower() else "proof_step",
            disposition="appendix" if int(cycle_id.split("-")[-1] or 0) < 220 else "main_body",
            source=f"agentic/reports/discovery_marathon/full_timeline.html:timeline_cycles:{cycle_id}",
            cycle_id=cycle_id,
        )
        add_if(
            units,
            family="timeline_cycles",
            kind="transfer_obligation",
            title=f"{branch} pressure",
            content=cycle.get("blocking_gap"),
            argument_role="validation_boundary",
            disposition="main_body",
            source=f"agentic/reports/discovery_marathon/full_timeline.html:timeline_cycles:{cycle_id}:blocking_gap",
            cycle_id=cycle_id,
            evidence_status="proof_obligation",
        )
        add_if(
            units,
            family="timeline_cycles",
            kind="future_work",
            title=f"{branch} next analysis",
            content=cycle.get("next_experiment"),
            argument_role="future_work",
            disposition="future_work",
            source=f"agentic/reports/discovery_marathon/full_timeline.html:timeline_cycles:{cycle_id}:next_experiment",
            cycle_id=cycle_id,
            evidence_status="validation_needed",
        )
        for eq in cycle.get("equations", []) if isinstance(cycle.get("equations"), list) else []:
            if isinstance(eq, dict):
                add_if(
                    units,
                    family="timeline_cycles",
                    kind="equation",
                    title=eq.get("label") or f"{cycle_id} equation",
                    content=eq.get("latex_render") or eq.get("latex"),
                    argument_role="proof_step",
                    disposition="appendix",
                    source=f"agentic/reports/discovery_marathon/full_timeline.html:timeline_cycles:{cycle_id}:equations",
                    cycle_id=cycle_id,
                    evidence_status="formula_with_conditions" if clean_text(eq.get("valid_when")) else "formula_needs_conditions",
                    extra={"valid_when": clean_text(eq.get("valid_when"))},
                )
        for falsifier in cycle.get("falsifiers", []) if isinstance(cycle.get("falsifiers"), list) else []:
            add_if(
                units,
                family="timeline_cycles",
                kind="falsifier",
                title=f"{cycle_id} falsifier",
                content=falsifier,
                argument_role="validation_boundary",
                disposition="appendix",
                source=f"agentic/reports/discovery_marathon/full_timeline.html:timeline_cycles:{cycle_id}:falsifiers",
                cycle_id=cycle_id,
                evidence_status="disconfirmation_probe",
            )


def interpret_strategy_and_contributions(bundle: dict[str, Any], units: list[dict[str, Any]]) -> None:
    monitor = bundle["contribution_monitor"]
    policy = monitor.get("loop_policy", {}) if isinstance(monitor.get("loop_policy"), dict) else {}
    add_if(
        units,
        family="scientific_contribution_monitor",
        kind="contribution_policy",
        title="Good enough contribution policy",
        content=f"{policy.get('standing_objective', '')} {policy.get('good_enough_definition', '')}",
        argument_role="novelty_boundary",
        disposition="main_body",
        source="agentic/reports/scientific_contribution_monitor/latest.json:loop_policy",
    )
    for candidate in monitor.get("candidates", []) if isinstance(monitor.get("candidates"), list) else []:
        if isinstance(candidate, dict):
            add_if(
                units,
                family="scientific_contribution_monitor",
                kind="contribution_candidate",
                title=candidate.get("branch_title") or candidate.get("candidate_id"),
                content=f"{candidate.get('smallest_honest_claim', '')} Boundary: {candidate.get('overclaim_boundary', '')}",
                argument_role="claim",
                disposition="main_body" if candidate.get("status") == "good_enough_to_handoff" else "appendix",
                source="agentic/reports/scientific_contribution_monitor/latest.json:candidates",
                cycle_id=clean_text(candidate.get("cycle_id")),
                evidence_status="paper_candidate",
                extra={
                    "candidate_id": clean_text(candidate.get("candidate_id")),
                    "score": int(candidate.get("score", 0) or 0),
                    "validation_burden": candidate.get("validation_burden", []),
                },
            )
    judge = bundle["strategy_judge"]
    for family_key, row in [
        ("current_strategy", judge.get("current_strategy", {})),
        ("progression_judgement", judge.get("progression_judgement", {})),
        ("paper_contribution_readiness", judge.get("paper_contribution_readiness", {})),
        ("main_problem_alignment", judge.get("main_problem_alignment", {})),
    ]:
        if isinstance(row, dict):
            add_if(
                units,
                family="strategy_progression_judge",
                kind=family_key,
                title=row.get("title") or family_key,
                content="; ".join(clean_text(row.get(key)) for key in row if not isinstance(row.get(key), (dict, list))),
                argument_role="validation_boundary" if "alignment" in family_key else "claim",
                disposition="main_body",
                source=f"agentic/reports/strategy_progression_judge/latest.json:{family_key}",
                evidence_status="judge_interpretation",
            )


def interpret_other_tabs(bundle: dict[str, Any], units: list[dict[str, Any]]) -> None:
    payload = bundle["payload"]
    story = payload.get("timeline_storyline", {}) if isinstance(payload.get("timeline_storyline"), dict) else {}
    for beat in story.get("beats", []) if isinstance(story.get("beats"), list) else []:
        if isinstance(beat, dict):
            add_if(
                units,
                family="timeline_storyline",
                kind="physics_story_beat",
                title=f"{beat.get('cycle_id', '')}: {beat.get('branch_title', '')}",
                content=f"{beat.get('learning', '')} Next: {beat.get('next_experiment', '')}",
                argument_role="failure_learning",
                disposition="appendix",
                source="agentic/reports/discovery_marathon/full_timeline.html:timeline_storyline",
                cycle_id=clean_text(beat.get("cycle_id")),
            )
    graph = payload.get("qualitative_mechanistic_graph", {}) if isinstance(payload.get("qualitative_mechanistic_graph"), dict) else {}
    for edge in graph.get("edges", []) if isinstance(graph.get("edges"), list) else []:
        if isinstance(edge, dict):
            add_if(
                units,
                family="qualitative_mechanistic_graph",
                kind="qualitative_mechanism",
                title=f"{edge.get('source', '')} -> {edge.get('target', '')}",
                content=edge.get("qualitative_behavior") or edge.get("direction"),
                argument_role="mechanism",
                disposition="appendix",
                source="agentic/state/qualitative_mechanistic_graphs",
            )
    gedanken = payload.get("gedanken_experiments", {}) if isinstance(payload.get("gedanken_experiments"), dict) else {}
    for packet in gedanken.get("packets", []) if isinstance(gedanken.get("packets"), list) else []:
        if isinstance(packet, dict):
            situation = packet.get("situation", {}) if isinstance(packet.get("situation"), dict) else {}
            add_if(
                units,
                family="gedanken_experiments",
                kind="gedanken_probe",
                title=situation.get("title") or packet.get("packet_id"),
                content=situation.get("why_this_situation_is_informative") or situation.get("purpose"),
                argument_role="future_work",
                disposition="future_work",
                source="agentic/reports/gedanken_experiments/latest.json",
                evidence_status="conceptual_probe",
            )
    layer = payload.get("parsimonious_probe_layer", {}) if isinstance(payload.get("parsimonious_probe_layer"), dict) else {}
    for key in ["symbolic_matrix_probe", "analytic_estimate_obligations", "finite_algebra_interfaces"]:
        item = layer.get(key, {}) if isinstance(layer.get(key), dict) else {}
        add_if(
            units,
            family="parsimonious_probe_layer",
            kind=key,
            title=key.replace("_", " "),
            content=item.get("headline") or item.get("status") or item.get("summary"),
            argument_role="calculation_input",
            disposition="appendix",
            source=f"agentic/reports/{key}/latest.json",
        )
    macro = bundle["macro_strategy"]
    for strategy in macro.get("macro_strategies", []) if isinstance(macro.get("macro_strategies"), list) else []:
        if isinstance(strategy, dict):
            add_if(
                units,
                family="macro_strategy_report",
                kind="macro_strategy",
                title=strategy.get("title") or strategy.get("strategy_id"),
                content=f"{strategy.get('physics_picture', '')} {strategy.get('current_pressure', '')}",
                argument_role="motivation",
                disposition="main_body",
                source="agentic/reports/macro_strategy/latest.json:macro_strategies",
            )
    control = payload.get("summary_analysis_control", {}) if isinstance(payload.get("summary_analysis_control"), dict) else {}
    add_if(
        units,
        family="summary_analysis_control",
        kind="summary_control",
        title="Current summary control",
        content=f"{control.get('global_problem_contribution', '')} {control.get('when_to_stop', '')}",
        argument_role="validation_boundary",
        disposition="main_body",
        source="agentic/reports/discovery_marathon/full_timeline.html:summary_analysis_control",
    )
    for family in ["timeline_ranked_next_experiment_queue", "branch_summaries", "deep_reviews"]:
        value = payload.get(family, [])
        rows = value if isinstance(value, list) else []
        if rows:
            add_if(
                units,
                family=family,
                kind="queue_or_review_summary",
                title=family.replace("_", " "),
                content=f"{len(rows)} items preserved for audit and follow-up control.",
                argument_role="appendix_evidence",
                disposition="appendix",
                source=f"agentic/reports/discovery_marathon/full_timeline.html:{family}",
            )
    paper_report = payload.get("timeline_paper_report") or bundle["timeline_latex_sections"]
    if isinstance(paper_report, dict):
        add_if(
            units,
            family="timeline_paper_report",
            kind="paper_status",
            title="Prior paper artifact status",
            content=paper_report.get("status") or paper_report.get("epistemic_status"),
            argument_role="appendix_evidence",
            disposition="appendix",
            source="agentic/reports/timeline_paper/latest.json",
        )


def build_report(source: Path = FULL_TIMELINE_HTML) -> dict[str, Any]:
    bundle = load_source_bundle(source)
    target_id = clean_text(bundle["payload"].get("report", {}).get("target_id") or bundle["payload"].get("target_id"))
    profile = target_profile(target_id)
    units: list[dict[str, Any]] = []
    interpret_problem_literature(bundle, units)
    interpret_timeline_cycles(bundle, units)
    interpret_strategy_and_contributions(bundle, units)
    interpret_other_tabs(bundle, units)
    coverage = coverage_from_units(bundle, units)
    if profile["target_id"] == "p-vs-np-target":
        object_terms = [
            "hardness",
            "magnification",
            "mcsp",
            "mktp",
            "proof-complexity",
            "proof complexity",
            "sat",
            "circuit",
            "p/poly",
            "transfer",
            "natural",
            "certificate",
            "beta",
            "query",
            "exponent",
            "uniformity",
            "advice",
        ]
    elif profile["target_id"] == "yang-mills-existence-and-mass-gap-target":
        object_terms = ["wilson", "schur", "gram", "reflection", "os ", "o.s.", "kappa", "quotient", "hairpin", "collar"]
    else:
        object_terms = ["bridge", "obstruction", "certificate", "transfer", "theorem", "proof"]
    active_objects = [
        row
        for row in units
        if any(token in row["content"].lower() for token in object_terms)
        and row["argument_role"] in {"proof_step", "calculation_input", "claim", "validation_boundary"}
    ][:12]
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "schema": rel(SCHEMA),
        "status": "timeline_paper_interpretation_ready",
        "source_report": bundle["source_report"],
        "target_id": profile["target_id"],
        "target_display_name": profile["display_name"],
        "interpretation_id": stable_id("timeline-paper-interpretation", bundle["source_report"], len(units)),
        "units": units,
        "active_mathematical_objects": active_objects,
        "report_family_coverage": coverage,
        "required_argument_functions": {
            "has_active_object": bool(active_objects),
            "has_contribution_candidate": any(row["kind"] == "contribution_candidate" for row in units),
            "has_formal_derivation_material": any(row["kind"] in {"equation", "symbolic_matrix_probe", "finite_algebra_interfaces"} for row in units),
            "has_validation_boundary": any(row["argument_role"] == "validation_boundary" for row in units),
        },
        "artifacts": {"json": rel(OUT_JSON), "markdown": rel(OUT_MD)},
        "epistemic_status": "interpretation_ready_validation_needed",
        "validation_handoff": "python agentic/scripts/validate_timeline_paper_interpretation.py",
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Timeline Paper Interpretation",
        "",
        f"- Status: `{report['status']}`",
        f"- Source report: `{report['source_report']}`",
        f"- Units: `{len(report['units'])}`",
        "",
        "## Required Argument Functions",
        "",
    ]
    for key, value in report["required_argument_functions"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Report Family Coverage", ""])
    for family, row in report["report_family_coverage"]["families"].items():
        lines.append(f"- `{family}`: present `{row['present']}`, units `{row['unit_count']}`, dispositions `{row['dispositions']}`")
    lines.extend(["", "## Main-Body Units", ""])
    for row in [unit for unit in report["units"] if unit["disposition"] == "main_body"][:80]:
        cite = f" `{row['cycle_id']}`" if row.get("cycle_id") else ""
        lines.append(f"- `{row['kind']}`{cite}: {row['title']} -> `{row['argument_role']}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(FULL_TIMELINE_HTML), help="Timeline HTML report with embedded marathon-data.")
    args = parser.parse_args()
    report = build_report(Path(args.source))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_JSON, report)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
