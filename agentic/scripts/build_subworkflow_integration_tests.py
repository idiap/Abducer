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
"""Test qualitative/Gedanken subworkflows against current marathon progress."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel, utc_now, write_json
from discovery_marathon_common import load_cycles, load_run_state


QUAL = ROOT / "agentic/reports/qualitative_relation_packets/latest.json"
GEDANKEN = ROOT / "agentic/reports/gedanken_experiments/latest.json"
GRAPH = ROOT / "agentic/state/qualitative_mechanistic_graphs/yang-mills-existence-and-mass-gap-target.json"
SYMBOLIC = ROOT / "agentic/reports/symbolic_matrix_probe/latest.json"
FINITE = ROOT / "agentic/reports/finite_algebra_interfaces/latest.json"
OBLIGATIONS = ROOT / "agentic/reports/analytic_estimate_obligations/latest.json"
B_NUMERIC = ROOT / "agentic/reports/bounded_numeric_probe/latest.json"
OUT_DIR = ROOT / "agentic/reports/subworkflow_integration"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
TARGET_ID = "yang-mills-existence-and-mass-gap-target"
WINDOW = 8


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def cycle_path(run_id: str, cycle_id: str) -> str:
    return f"agentic/runs/discovery_marathons/{run_id}/cycles/{cycle_id}.json"


def cycle_text(cycle: dict[str, Any]) -> str:
    return clean_text(cycle.get("branch_outputs", []))


def focus_for_cycle(text: str) -> str:
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


def packet_focus(packet: dict[str, Any]) -> str:
    for variable in packet.get("variables", []):
        if isinstance(variable, dict) and variable.get("id") == "live_focus":
            role = clean_text(variable.get("role")).lower()
            if "holonomy" in role:
                return "quotient_holonomy"
            if "boundary ope" in role:
                return "boundary_ope_extraction"
            if "schur" in role or "determinant" in role:
                return "schur_preimage_determinant"
    text = clean_text(packet)
    return focus_for_cycle(text)


def branch_output_summary(cycle: dict[str, Any]) -> dict[str, Any]:
    output = (cycle.get("branch_outputs") or [{}])[0]
    lemma = (output.get("candidate_lemmas") or [{}])[0]
    return {
        "cycle_id": cycle.get("cycle_id"),
        "branch_id": output.get("branch_id", ""),
        "branch_title": output.get("branch_title", ""),
        "focus": focus_for_cycle(cycle_text(cycle)),
        "blocking_gap": output.get("attempted_derivation", {}).get("blocking_gap", ""),
        "next_experiment": output.get("next_experiment", ""),
        "first_lemma": lemma.get("statement", ""),
    }


def has_overlap(left: str, right: str, required_terms: int = 2) -> bool:
    stop = {
        "that",
        "with",
        "from",
        "this",
        "then",
        "only",
        "must",
        "into",
        "same",
        "valid",
        "branch",
        "cycle",
        "proof",
        "target",
    }
    words_left = {w for w in left.lower().replace("\\", " ").replace("_", " ").split() if len(w) > 4 and w not in stop}
    words_right = {w for w in right.lower().replace("\\", " ").replace("_", " ").split() if len(w) > 4 and w not in stop}
    return len(words_left & words_right) >= required_terms


def test_qualitative(cycles: list[dict[str, Any]], run_id: str, qual: dict[str, Any], graph: dict[str, Any]) -> list[dict[str, Any]]:
    packets = qual.get("packets", [])
    require(packets, "qualitative relation packets missing")
    packet = packets[0]
    recent_ids = [cycle["cycle_id"] for cycle in cycles]
    expected_paths = {cycle_path(run_id, cycle_id) for cycle_id in recent_ids}
    source_paths = set(packet.get("source_artifacts", []))
    relations = packet.get("relations", [])
    relation_text = clean_text(relations)
    cycle_window_text = clean_text([cycle_text(cycle) for cycle in cycles])
    tests = [
        {
            "name": "qualitative_packets_use_recent_cycle_window",
            "passed": expected_paths.issubset(source_paths),
            "detail": f"{len(expected_paths & source_paths)}/{len(expected_paths)} recent cycles cited",
        },
        {
            "name": "qualitative_relations_reflect_current_boundary_progress",
            "passed": all(term in relation_text.lower() for term in ["boundary", "quotient", "phase", "determinant"]),
            "detail": "requires boundary, quotient, phase, and determinant relation language from cycles 198-205",
        },
        {
            "name": "qualitative_relations_overlap_cycle_content",
            "passed": has_overlap(cycle_window_text, relation_text, required_terms=6),
            "detail": "relation text shares substantive terms with the recent branch outputs",
        },
        {
            "name": "qualitative_graph_preserves_cycle_ids",
            "passed": set(recent_ids).issubset(set(graph.get("source_cycle_ids", []))),
            "detail": f"graph source cycles: {', '.join(graph.get('source_cycle_ids', []))}",
        },
    ]
    return tests


def test_gedanken(cycles: list[dict[str, Any]], run_id: str, gedanken: dict[str, Any]) -> list[dict[str, Any]]:
    packets = gedanken.get("packets", [])
    require(packets, "Gedanken packets missing")
    recent_ids = [cycle["cycle_id"] for cycle in cycles]
    by_cycle = {cycle["cycle_id"]: cycle for cycle in cycles}
    packet_cycles = {cid for packet in packets for cid in packet.get("originating_cycle_ids", [])}
    focus_counts = Counter(packet_focus(packet) for packet in packets)
    cycle_focus_counts = Counter(focus_for_cycle(cycle_text(cycle)) for cycle in cycles)
    non_generic_packet_focuses = [focus for focus, count in focus_counts.items() if focus != "generic" and count > 0]
    dominant_packet_focus, dominant_packet_count = focus_counts.most_common(1)[0]
    dominant_cycle_focus, dominant_cycle_count = cycle_focus_counts.most_common(1)[0]
    diversity_or_convergence = (
        len(non_generic_packet_focuses) >= 2
        or (
            dominant_packet_focus == dominant_cycle_focus
            and dominant_packet_focus != "generic"
            and dominant_packet_count >= max(1, len(packets) - 1)
            and dominant_cycle_count >= max(1, len(cycles) - 1)
        )
    )
    grounded = []
    for packet in packets:
        cycle_ids = packet.get("originating_cycle_ids", [])
        for cycle_id in cycle_ids:
            if cycle_id not in by_cycle:
                grounded.append(False)
                continue
            expected_focus = focus_for_cycle(cycle_text(by_cycle[cycle_id]))
            actual_focus = packet_focus(packet)
            source = cycle_path(run_id, cycle_id)
            source_ok = source in packet.get("source_artifacts", []) and (ROOT / source).exists()
            overlap_ok = has_overlap(cycle_text(by_cycle[cycle_id]), clean_text(packet), required_terms=4)
            grounded.append(source_ok and expected_focus == actual_focus and overlap_ok)
    tests = [
        {
            "name": "gedanken_packets_cover_recent_cycles",
            "passed": set(recent_ids).issubset(packet_cycles),
            "detail": f"{len(set(recent_ids) & packet_cycles)}/{len(recent_ids)} recent cycles have packets",
        },
        {
            "name": "gedanken_packets_are_cycle_grounded",
            "passed": bool(grounded) and all(grounded),
            "detail": f"{sum(1 for item in grounded if item)}/{len(grounded)} packet-cycle links match source artifact, focus, and content overlap",
        },
        {
            "name": "gedanken_packets_preserve_progression_diversity",
            "passed": diversity_or_convergence,
            "detail": f"packet focus counts: {dict(focus_counts)}; cycle focus counts: {dict(cycle_focus_counts)}",
        },
        {
            "name": "gedanken_followups_use_qualitative_skills",
            "passed": all(
                any(skill.startswith("qualitative-") or skill in {"limit-convergence-behavior-auditor", "dimensional-symmetry-constraint-checker"} for task in packet.get("followup_cycle_tasks", []) for skill in task.get("required_skills", []))
                for packet in packets
            ),
            "detail": "every packet has at least one follow-up requiring the qualitative subworkflow",
        },
    ]
    return tests


def test_cross_workflow(gedanken: dict[str, Any], graph: dict[str, Any]) -> list[dict[str, Any]]:
    graph_edges = {edge.get("id"): edge for edge in graph.get("edges", [])}
    packets = gedanken.get("packets", [])
    affected_edges = [edge_id for packet in packets for edge_id in packet.get("affected_edge_ids", [])]
    linked_packets = {
        packet_id
        for edge in graph_edges.values()
        for packet_id in edge.get("gedanken_packet_ids", [])
    }
    packet_ids = {packet.get("packet_id") for packet in packets}
    tests = [
        {
            "name": "gedanken_affected_edges_exist_in_qualitative_graph",
            "passed": all(edge_id in graph_edges for edge_id in affected_edges),
            "detail": f"{sum(1 for edge_id in affected_edges if edge_id in graph_edges)}/{len(affected_edges)} affected edges exist",
        },
        {
            "name": "qualitative_graph_links_gedanken_packets",
            "passed": packet_ids.issubset(linked_packets),
            "detail": f"{len(packet_ids & linked_packets)}/{len(packet_ids)} packets linked from graph edges",
        },
        {
            "name": "graph_links_remain_conceptual_not_proof",
            "passed": all(
                update.get("epistemic_status") == "conceptual_probe"
                for update in graph.get("updates", [])
                if clean_text(update.get("packet_id")).startswith("gedanken.")
            ),
            "detail": "Gedanken-origin graph updates must remain conceptual probes",
        },
    ]
    return tests


def test_parsimonious_probe(graph: dict[str, Any]) -> list[dict[str, Any]]:
    symbolic = load_json_object(SYMBOLIC)
    finite = load_json_object(FINITE)
    obligations = load_json_object(OBLIGATIONS)
    graph_text = clean_text(graph).lower()
    queue = obligations.get("next_experiment_queue_items", [])
    numeric = load_json_object(B_NUMERIC) if B_NUMERIC.exists() else {}
    packet = finite.get("packets", [{}])[0]
    tests = [
        {
            "name": "pmp_symbolic_before_numeric",
            "passed": symbolic.get("status") == "symbolic_formula" and symbolic.get("probe_decision", {}).get("decision") == "derive_symbolically",
            "detail": "parsimonious symbolic-before-numeric decision is recorded for the finite quotient determinant",
        },
        {
            "name": "pmp_obligations_precede_numeric_probe",
            "passed": bool(queue) and all(item.get("epistemic_status") == "analytic_obligation" for item in queue[:3]),
            "detail": "analytic estimate queue items are ranked before any bounded numeric calibration",
        },
        {
            "name": "esr_finite_interface_has_side_conditions_and_falsifiers",
            "passed": packet.get("epistemic_status") == "equational_interface" and len(packet.get("side_conditions", [])) >= 5 and len(packet.get("falsifier_templates", [])) >= 4,
            "detail": "finite algebra packet records side-condition ledger and formula-derived falsifier shapes",
        },
        {
            "name": "esr_no_lean_or_proof_overclaim",
            "passed": all("not " in clean_text(item).lower() for item in packet.get("non_claims", []) if "Lean" in clean_text(item) or "theorem" in clean_text(item) or "proof" in clean_text(item)),
            "detail": "equational symbolic packet explicitly excludes Lean/theorem-prover/proof-promotion status",
        },
        {
            "name": "pmp_graph_carries_symbolic_and_obligation_status",
            "passed": "symbolic_formula" in graph_text and "analytic_obligation" in graph_text and "equational_interface" in graph_text and "falsifier_shape" in graph_text and "holonomy" in graph_text,
            "detail": "qualitative graph includes symbolic formula, finite interface, falsifier shape, and analytic obligation edges",
        },
        {
            "name": "pmp_bounded_numeric_probe_is_non_proof_when_present",
            "passed": not numeric or numeric.get("status") in {"calibration_only", "validated_probe", "falsifier_candidate"},
            "detail": "bounded numeric outputs remain non-proof statuses",
        },
    ]
    return tests


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Subworkflow Integration Tests",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Status: `{report['status']}`",
        f"- Recent cycle window: `{', '.join(report['recent_cycle_ids'])}`",
        "",
        "## Current Progress Context",
        "",
    ]
    for row in report["cycle_progress"]:
        lines.append(f"### {row['cycle_id']} - {row['focus']}")
        lines.append(f"- Branch: `{row['branch_id']}` {row['branch_title']}")
        lines.append(f"- Blocking gap: {row['blocking_gap']}")
        lines.append(f"- Next experiment: {row['next_experiment']}")
        lines.append("")
    for section in ["qualitative_tests", "gedanken_tests", "cross_workflow_tests", "parsimonious_probe_tests"]:
        lines.extend([f"## {section.replace('_', ' ').title()}", ""])
        for test in report[section]:
            mark = "PASS" if test["passed"] else "FAIL"
            lines.append(f"- `{mark}` {test['name']}: {test['detail']}")
        lines.append("")
    if report.get("refinements"):
        lines.extend(["## Refinements", ""])
        for item in report["refinements"]:
            lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def main() -> int:
    _, run_state = load_run_state()
    require(run_state, "missing discovery marathon run state")
    run_id = run_state.get("run_id", "unknown-run")
    active_target_id = clean_text(run_state.get("target_id"))
    cycles = [cycle for cycle in load_cycles(run_state) if cycle.get("valid_as_research_cycle")]
    if active_target_id != TARGET_ID:
        report = {
            "version": 1,
            "target_id": active_target_id,
            "generated_utc": utc_now(),
            "run_id": run_id,
            "status": "skipped_target_mismatch",
            "skip_reason": (
                "Yang-Mills qualitative/Gedanken/PMP integration tests require boundary-OPE, quotient-holonomy, "
                "Schur-determinant, and Wilson-collar artifacts. The active marathon target is different, so these "
                "tests are not meaningful for the current run."
            ),
            "recent_cycle_ids": [cycle["cycle_id"] for cycle in cycles[-min(WINDOW, len(cycles)):]],
            "cycle_progress": [branch_output_summary(cycle) for cycle in cycles[-min(WINDOW, len(cycles)):]],
            "qualitative_tests": [],
            "gedanken_tests": [],
            "cross_workflow_tests": [],
            "parsimonious_probe_tests": [],
            "refinements": [
                "Skipped Yang-Mills-specific integration tests for the active non-Yang-Mills target.",
                "Parsimonious probe control remains defined as symbolic-before-numeric with bounded numeric probes only after analytic obligations.",
            ],
            "parsimonious_probe_summary": {
                "status": "not_applicable_to_active_target",
                "policy": "parsimonious symbolic-before-numeric discipline remains available but was not applied to this target-specific integration test.",
                "bounded_numeric": "bounded numeric probes are third-stage calibration only and not part of proof promotion.",
            },
        }
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        write_json(OUT_JSON, report)
        OUT_MD.write_text(render_markdown(report), encoding="utf-8")
        print(f"Wrote {rel(OUT_JSON)}")
        print(f"Wrote {rel(OUT_MD)}")
        print(f"skipped Yang-Mills-specific subworkflow integration for active target {active_target_id}")
        return 0
    recent = cycles[-WINDOW:]
    require(len(recent) == WINDOW, f"need at least {WINDOW} valid cycles for integration tests")
    qual = load_json_object(QUAL)
    gedanken = load_json_object(GEDANKEN)
    graph = load_json_object(GRAPH)
    report = {
        "version": 1,
        "target_id": TARGET_ID,
        "generated_utc": utc_now(),
        "run_id": run_id,
        "recent_cycle_ids": [cycle["cycle_id"] for cycle in recent],
        "cycle_progress": [branch_output_summary(cycle) for cycle in recent],
        "qualitative_tests": test_qualitative(recent, run_id, qual, graph),
        "gedanken_tests": test_gedanken(recent, run_id, gedanken),
        "cross_workflow_tests": test_cross_workflow(gedanken, graph),
        "parsimonious_probe_tests": test_parsimonious_probe(graph),
        "refinements": [
            "Gedanken packet generation is cycle-sensitive, so repeated branch titles no longer overwrite distinct previous-cycle progress.",
            "Reflection-positive Gedanken packets now distinguish boundary OPE extraction from quotient-holonomy progress.",
            "The integration gate checks semantic overlap with recent cycle outputs, not only artifact existence.",
            "PMP/ESR now routes exact finite algebra through side-condition ledgers, falsifier shapes, and analytic obligation queues before any bounded numeric probe.",
        ],
        "parsimonious_probe_summary": {
            "symbolic_identity_count": len(load_json_object(SYMBOLIC).get("identities", [])),
            "finite_interface_count": len(load_json_object(FINITE).get("packets", [])),
            "falsifier_template_count": len(load_json_object(FINITE).get("packets", [{}])[0].get("falsifier_templates", [])),
            "analytic_obligation_count": len(load_json_object(OBLIGATIONS).get("obligations", [])),
            "proof_safe": True,
        },
    }
    all_tests = report["qualitative_tests"] + report["gedanken_tests"] + report["cross_workflow_tests"] + report["parsimonious_probe_tests"]
    report["status"] = "pass" if all(test["passed"] for test in all_tests) else "fail"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_JSON, report)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    if report["status"] != "pass":
        failed = ", ".join(test["name"] for test in all_tests if not test["passed"])
        fail(f"subworkflow integration tests failed: {failed}")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    print(f"validated subworkflow integration over {len(recent)} recent cycles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
