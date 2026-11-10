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

"""Build visible reasoning-progress logs from active Abducer artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, kb_ref_from_path, load_json_object, load_optional_json, repo_path, stable_id, utc_now, write_json


TRACE_DIR = ROOT / "agentic/traces/reasoning_events"
REPORT_JSON = ROOT / "agentic/reports/reasoning_progress/latest.json"
REPORT_MD = ROOT / "agentic/reports/reasoning_progress/latest.md"


def existing_paths(paths: list[str]) -> list[str]:
    return [path for path in paths if (ROOT / path).exists()]


def visual(lane: str, salience: str, color: str, glyph: str, detail: str = "summary") -> dict[str, str]:
    return {
        "lane": lane,
        "salience": salience,
        "color_token": color,
        "glyph": glyph,
        "detail_level": detail,
    }


def event(
    *,
    run_id: str,
    target_id: str,
    workflow_id: str,
    phase: str,
    event_type: str,
    title: str,
    narrative_summary: str,
    mathematical_objects: list[str],
    conceptual_move: str,
    target_commitments: list[str],
    evidence_paths: list[str],
    epistemic_status: str,
    uncertainty: str,
    proof_obligations: list[str],
    visual_encoding: dict[str, str],
) -> dict[str, Any]:
    return {
        "event_id": stable_id("reasoning-event", run_id, target_id, phase, event_type, title),
        "run_id": run_id,
        "target_id": target_id,
        "workflow_id": workflow_id,
        "timestamp_utc": utc_now(),
        "phase": phase,
        "event_type": event_type,
        "title": title,
        "narrative_summary": narrative_summary,
        "mathematical_objects": mathematical_objects,
        "conceptual_move": conceptual_move,
        "target_commitments": target_commitments,
        "evidence_paths": evidence_paths,
        "epistemic_status": epistemic_status,
        "uncertainty": uncertainty,
        "proof_obligations": proof_obligations,
        "visual_encoding": visual_encoding,
    }


def top_frontier_labels(graph: dict[str, Any], limit: int = 6) -> list[str]:
    rows = []
    node_by_id = {row["id"]: row for row in graph.get("nodes", [])}
    for frontier in graph.get("frontier", [])[:limit]:
        node = node_by_id.get(frontier["id"], {})
        label = clean_text(node.get("label") or frontier.get("next_action") or frontier.get("blocker") or frontier.get("id"))
        rows.append(label[:180])
    return rows


def route_physics_summary(route: dict[str, Any], ranking: dict[str, Any]) -> str:
    family = clean_text(route.get("route_blueprint", {}).get("route_family", "")).lower()
    disposition = clean_text(ranking.get("route_disposition", "unknown"))
    if "balaban" in family or "rg" in family:
        body = (
            "This candidate treats multiscale Yang-Mills control as a construction question: can regulated non-Abelian "
            "gauge-field measures be controlled through ultraviolet cutoff removal so that a non-Gaussian, reflection-positive "
            "continuum vacuum sector remains?"
        )
    elif "correlator" in family or "spectral-gap" in family:
        body = (
            "This candidate treats Euclidean decay as a spectral question: can gauge-invariant time correlations in the same "
            "continuum vacuum have spectral measures with support bounded away from zero, and can that exclusion survive OS "
            "reconstruction into the Hamiltonian spectrum?"
        )
    elif "hamiltonian" in family:
        body = (
            "This candidate sharpens the endpoint: the reconstructed Yang-Mills Hilbert space must have a vacuum sector and a "
            "positive Hamiltonian whose vacuum-orthogonal spectrum has no arbitrarily soft excitations."
        )
    elif "os" in family or "wightman" in family:
        body = (
            "This candidate asks whether Euclidean Schwinger functions can be carried through reflection positivity into a "
            "positive-norm quantum Hilbert space before any spectral-gap claim is made."
        )
    else:
        body = clean_text(route.get("proposed_transformation")) or "This candidate needs a physics-facing mechanism statement."
    return (
        f"{body} Operationally it is marked `{disposition}` only to control sequencing; the substantive question is whether "
        "the named objects, observables, limiting regime, and transfer theorem can be made same-theory."
    )


def build_events(run_id: str) -> list[dict[str, Any]]:
    target = load_json_object(ROOT / "agentic/state/current_target.json")
    target_id = target["target_id"]
    kb_ref = kb_ref_from_path(repo_path(target["kb_path"], must_exist=True))
    workflow_id = f"{kb_ref}-reasoning-monitor"
    graph = load_json_object(ROOT / "agentic/state/dependency_graphs" / f"{kb_ref}.json")
    hypothesis = load_json_object(ROOT / "artifacts/hegelian/hypothesis_exploration_map.json")
    stale_report = load_json_object(ROOT / "agentic/reports/stale_workflows/latest.json")
    ledger_path = ROOT / "agentic/state/essential_target_ledgers" / f"{kb_ref}.json"
    ledger = load_json_object(ledger_path) if ledger_path.exists() else {}
    commitments = [row["id"] for row in ledger.get("essential_commitments", []) if isinstance(row, dict) and row.get("id")]
    if not commitments:
        commitments = [claim for claim in target.get("main_claim_ids", [])]
    events = [
        event(
            run_id=run_id,
            target_id=target_id,
            workflow_id=workflow_id,
            phase="target-spine",
            event_type="target_spine",
            title="Yang-Mills target spine is active",
            narrative_summary=(
                "The active analysis is anchored to the Clay Yang-Mills target: construct a nontrivial four-dimensional "
                "compact-gauge quantum field theory and prove a positive mass gap in that same theory. Every later claim "
                "must preserve the gauge-field object, OS/Wightman adequacy, continuum limit, nontriviality, and spectral gap."
            ),
            mathematical_objects=["quantum Yang-Mills theory on R^4", "compact simple gauge group", "positive mass gap"],
            conceptual_move="Make the physical target object explicit before considering construction or spectral mechanisms.",
            target_commitments=commitments,
            evidence_paths=existing_paths([target["kb_path"], f"agentic/state/essential_target_ledgers/{kb_ref}.json", "agentic/state/current_target.json"]),
            epistemic_status="evidence-backed",
            uncertainty="The target spine is controlled, but no mathematical proof route is promoted by this event.",
            proof_obligations=["Preserve existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap in every active route."],
            visual_encoding=visual("target", "critical", "target-gold", "compass", "summary"),
        ),
        event(
            run_id=run_id,
            target_id=target_id,
            workflow_id=workflow_id,
            phase="dependency-frontier",
            event_type="dependency_frontier",
            title="Dependency frontier exposes unresolved mathematical interfaces",
            narrative_summary=(
                f"The active dependency graph exposes {graph['summary']['frontier_count']} unresolved mathematical interfaces "
                f"among {graph['summary']['node_count']} tracked objects: definitions of the gauge theory, OS reconstruction, "
                "continuum passage, nontriviality witnesses, and spectral-gap transfer. These are not administrative tasks; "
                "they are the places where the physics mechanism can fail."
            ),
            mathematical_objects=top_frontier_labels(graph),
            conceptual_move="Expose which mathematical interfaces must be supplied before a Yang-Mills gap claim has physical meaning.",
            target_commitments=commitments,
            evidence_paths=existing_paths([f"agentic/state/dependency_graphs/{kb_ref}.json", f"agentic/reports/dependency_closure/{kb_ref}.md"]),
            epistemic_status="proof-obligation",
            uncertainty="Frontier nodes are route obligations, not proof dependencies, until later validation discharges them.",
            proof_obligations=[f"Resolve or demote {graph['summary']['frontier_count']} open frontier nodes."],
            visual_encoding=visual("dependency", "high", "frontier-cyan", "graph", "expandable"),
        ),
    ]
    summary = hypothesis.get("summary", {})
    events.append(
        event(
            run_id=run_id,
            target_id=target_id,
            workflow_id=workflow_id,
            phase="conceptual-pressure",
            event_type="conceptual_pressure",
            title="Conceptual pressure has been extracted from the frontier",
            narrative_summary=(
                f"The exploration layer isolated {summary.get('pressure_count', 0)} tensions and {summary.get('candidate_count', 0)} "
                "candidate mechanisms in the Yang-Mills space. The useful tensions are physical ones: ultraviolet construction "
                "versus infrared mass generation, Euclidean positivity versus Hamiltonian reconstruction, and lattice evidence "
                "versus continuum same-theory transfer."
            ),
            mathematical_objects=["ultraviolet scale control", "gauge-invariant observables", "spectral support near zero"],
            conceptual_move="Turn unresolved physics interfaces into explicit mechanism candidates with failure conditions.",
            target_commitments=commitments,
            evidence_paths=existing_paths(["artifacts/hegelian/hypothesis_exploration_map.json", "artifacts/hegelian/failure_signal_cartography.json"]),
            epistemic_status="conjectural",
            uncertainty="Creative pressure can widen the search space but must be filtered by target relevance and validation gates.",
            proof_obligations=["Attach each generated route to target commitments and disconfirming observations before continuation."],
            visual_encoding=visual("conceptual", "high", "pressure-magenta", "spark", "summary"),
        )
    )
    rankings = hypothesis.get("candidate_rankings", [])
    candidates = {row["candidate_id"]: row for row in hypothesis.get("mediation_candidates", [])}
    validations = {row["candidate_id"]: row for row in hypothesis.get("validation_packets", [])}
    for index, ranking in enumerate(rankings[:4], start=1):
        candidate = candidates.get(ranking["candidate_id"], {})
        validation = validations.get(ranking["candidate_id"], {})
        subgoal_control = ranking.get("subgoal_control") or candidate.get("subgoal_control") or validation.get("subgoal_control", {})
        disposition = ranking.get("route_disposition", "unknown")
        event_type = "route_ranking" if index <= 2 else "validation_gate"
        status = "proof-obligation" if disposition == "proof_queue" else "conjectural"
        events.append(
            event(
                run_id=run_id,
                target_id=target_id,
                workflow_id=workflow_id,
                phase=f"candidate-{index:02d}",
                event_type=event_type,
                title=f"Route candidate {index}: {candidate.get('creative_operation', 'unknown')} -> {disposition}",
                narrative_summary=route_physics_summary(candidate, ranking),
                mathematical_objects=[
                    clean_text(candidate.get("proposed_transformation"))[:220] or ranking["candidate_id"],
                    candidate.get("creative_operation", "creative_operation"),
                ],
                conceptual_move="Translate a route candidate into a same-theory mechanism question about construction, observables, limits, and spectrum.",
                target_commitments=ranking.get("cited_commitment_ids", commitments),
                evidence_paths=existing_paths(["artifacts/hegelian/candidate_rankings.json", "artifacts/hegelian/mediation_candidates.json", "artifacts/hegelian/validation_packets.json"]),
                epistemic_status=status,
                uncertainty="The ranking is only a sequencing device; physical progress requires the bridge assumptions and failure tests to be discharged.",
                proof_obligations=[row.get("requirement", "") for row in validation.get("obligations", [])[:4] if isinstance(row, dict)],
                visual_encoding=visual("candidate" if event_type == "route_ranking" else "validation", "high" if disposition == "proof_queue" else "medium", "route-green" if disposition == "proof_queue" else "route-blue", "route", "expandable"),
            )
        )
    control_items = [
        ranking.get("subgoal_control")
        for ranking in rankings
        if isinstance(ranking.get("subgoal_control"), dict)
    ]
    if control_items:
        active_controls = [
            control
            for control in control_items
            if control.get("decision") in {"persist_adapt", "backtrack", "pivot", "quarantine", "stop"}
        ][:6]
        events.append(
            event(
                run_id=run_id,
                target_id=target_id,
                workflow_id=workflow_id,
                phase="formal-subgoal-control",
                event_type="subgoal_control_decision",
                title="Formal subgoals are under explicit continuation control",
                narrative_summary=(
                    "Every active route now carries a control decision: persist by adaptation only while failure teaches a sharper "
                    "premise, object, regime, or bridge; backtrack when a formula assumes an unbuilt premise; pivot after repeated "
                    "certified failure; quarantine evidence or analogy routes; and stop subgoals that no longer teach the target loop."
                ),
                mathematical_objects=[control.get("target_object_link", "") for control in active_controls],
                conceptual_move=(
                    "Turn formula persistence into a public work-loop decision with blocker, learning-from-failure, next action, "
                    "and demotion triggers."
                ),
                target_commitments=commitments,
                evidence_paths=existing_paths(
                    [
                        "agentic/spec/formal_subgoal_control.schema.json",
                        "docs/research-methods/formal-subgoal-control-policy.md",
                        "artifacts/hegelian/formal_subgoal_controls.json",
                        "artifacts/hegelian/candidate_rankings.json",
                    ]
                ),
                epistemic_status="proof-obligation",
                uncertainty=(
                    "The control packet governs route continuation; it does not prove the mathematical subgoal. Generative review "
                    "still has to judge whether the rationale is mathematically substantive."
                ),
                proof_obligations=[
                    f"{control.get('decision')}: {control.get('next_action')}"
                    for control in active_controls[:5]
                ],
                visual_encoding=visual("reflection", "high", "pressure-magenta", "control", "expandable"),
            )
        )
    events.append(
        event(
            run_id=run_id,
            target_id=target_id,
            workflow_id=workflow_id,
            phase="stale-workflow-guard",
            event_type="drift_guard",
            title="Previous workflow artifacts are isolated as historical",
            narrative_summary=(
                f"The stale-workflow preflight found {stale_report.get('historical_artifact_count', 0)} historical artifacts but "
                f"{stale_report.get('critical_findings', 0)} critical active-state mismatches."
            ),
            mathematical_objects=["active target state", "historical artifacts", "latest report surfaces"],
            conceptual_move="Keep old runs available as evidence without letting them masquerade as the current mathematical route.",
            target_commitments=commitments,
            evidence_paths=existing_paths(["agentic/reports/stale_workflows/latest.json", "agentic/reports/stale_workflows/latest.md"]),
            epistemic_status="evidence-backed",
            uncertainty="Historical artifacts remain in the repository and must stay visually separated from active Yang-Mills reasoning.",
            proof_obligations=["Continue blocking report generation if active target IDs diverge."],
            visual_encoding=visual("drift", "medium", "guard-amber", "shield", "summary"),
        )
    )
    bridge = load_optional_json(ROOT / "agentic/reports/yang_mills_bridge_lemma_packets/latest.json")
    contradiction_branches = []
    for packet in bridge.get("packets", []) if isinstance(bridge.get("packets"), list) else []:
        if not isinstance(packet, dict):
            continue
        for branch in packet.get("contradiction_branches", []):
            if isinstance(branch, dict):
                contradiction_branches.append((packet, branch))
    if contradiction_branches:
        branch_titles = [branch.get("strategy", branch.get("branch_id", "contradiction branch")) for _, branch in contradiction_branches]
        events.append(
            event(
                run_id=run_id,
                target_id=target_id,
                workflow_id=workflow_id,
                phase="proof-by-contradiction",
                event_type="contradiction_route",
                title="Proof-by-contradiction branches expose route pressure",
                narrative_summary=(
                    "The reductio branches now have physical carriers: a negative reflection form would block Hilbert-space "
                    "reconstruction, triviality collapse would kill connected gauge-invariant cumulants, and no-gap would place "
                    "spectral weight arbitrarily close to zero in the vacuum-orthogonal sector. Each branch asks whether those "
                    "worlds are incompatible with one same continuum Yang-Mills object."
                ),
                mathematical_objects=branch_titles,
                conceptual_move=(
                    "Use contradiction as a controlled discovery instrument: exact negation, same-theory carrier, "
                    "conflict target, proof obligations, and auditor handoff."
                ),
                target_commitments=commitments,
                evidence_paths=existing_paths(
                    [
                        "agentic/reports/yang_mills_bridge_lemma_packets/latest.json",
                        "agentic/reports/yang_mills_bridge_lemma_packets/latest.md",
                        "agentic/reports/proof_by_contradiction_validation/latest.json",
                        "skills/reasoning/kb-contradiction-strategist/SKILL.md",
                        "skills/evaluation/contradiction-route-auditor/SKILL.md",
                    ]
                ),
                epistemic_status="proof-obligation",
                uncertainty=(
                    "These branches are not proofs. They are high-value pressure tests whose success depends on density, "
                    "closedness, nontriviality, and cutoff-uniform transfer obligations."
                ),
                proof_obligations=[
                    "Audit each reductio branch before proof-queue promotion.",
                    "Reject branches that change cutoff, Hilbert space, observable algebra, or limiting object.",
                    "Record whether failed branches point to missing density, closedness, nontriviality, or uniform-decay input.",
                ],
                visual_encoding=visual("reflection", "high", "pressure-magenta", "contradiction", "expandable"),
            )
        )
    empirical_report = load_optional_json(ROOT / "agentic/reports/empirical_evidence_requests/latest.json")
    empirical_requests = empirical_report.get("requests", []) if isinstance(empirical_report.get("requests"), list) else []
    if empirical_requests:
        events.append(
            event(
                run_id=run_id,
                target_id=target_id,
                workflow_id=workflow_id,
                phase="empirical-evidence-requests",
                event_type="evidence_request",
                title="Theoretical obligations spawned closely related empirical evidence requests",
                narrative_summary=(
                    "Empirical and numerical evidence is requested only when it is tied to a named Yang-Mills object: Wilson-loop "
                    "or string-tension data for nontriviality, glueball correlators for spectral scale, reflection-positive lattice "
                    "actions for OS transfer, or negative extrapolation evidence for cutoff leakage."
                ),
                mathematical_objects=[request.get("observable_or_quantity", request.get("request_id", "")) for request in empirical_requests[:6]],
                conceptual_move=(
                    "Use empirical evidence to guide witness selection, calibrate plausibility, find negative evidence, "
                    "or trigger demotion while preserving the theorem/proof boundary."
                ),
                target_commitments=commitments,
                evidence_paths=existing_paths(
                    [
                        "agentic/reports/empirical_evidence_requests/latest.json",
                        "agentic/reports/empirical_evidence_requests/latest.md",
                        "skills/ingest/evidence-acquisition-planner/SKILL.md",
                    ]
                ),
                epistemic_status="evidence-backed",
                uncertainty=(
                    "Empirical evidence can guide observable choice and stress-test transfer assumptions, but continuum Yang-Mills proof obligations remain live "
                    "until same-theory transfer theorems are supplied."
                ),
                proof_obligations=[
                    "Keep empirical evidence behind explicit transfer-gap and proof-boundary fields.",
                    "Demote fixed-cutoff, finite-volume, non-gauge-invariant, or analogy-only evidence.",
                    "Use supportive empirical evidence to prioritize witness and uniformity obligations, not to mark proof success.",
                ],
                visual_encoding=visual("validation", "high", "route-blue", "evidence", "expandable"),
            )
        )
    events.append(
        event(
            run_id=run_id,
            target_id=target_id,
            workflow_id=workflow_id,
            phase="reasoning-monitor-gate",
            event_type="validation_gate",
            title="Reasoning monitor generation is controlled by packet and HTML gates",
            narrative_summary=(
                "The Yang-Mills monitor is generated from a stable packet contract and then validated as a self-contained HTML artifact. "
                "This keeps the visible dashboard tied to the active target, evidence ledger, physics-facing route interpretations, stale-workflow preflight, and open mathematical obligations."
            ),
            mathematical_objects=["reasoning monitor packet", "self-contained HTML report", "active target guard"],
            conceptual_move="Treat the report as a controlled observability surface rather than an informal rendering of hidden state.",
            target_commitments=commitments,
            evidence_paths=existing_paths(
                [
                    "agentic/spec/reasoning_monitor_packet.schema.json",
                    "agentic/scripts/build_reasoning_monitor_packet.py",
                    "agentic/scripts/generate_reasoning_monitor_html.py",
                    "agentic/scripts/validate_reasoning_monitor.py",
                    "agentic/reports/reasoning_monitor/latest.json",
                    "agentic/reports/reasoning_monitor/latest.html",
                    "tests/reporting/test_reasoning_monitor_html.py",
                    "tests/generative/test_reasoning_monitor_visual_quality.md",
                    "docs/reference/reasoning-monitor-visual-grammar.md",
                    "docs/operations/reasoning-monitor-runbook.md",
                ]
            ),
            epistemic_status="evidence-backed",
            uncertainty="The monitor can show controlled progress and open mathematical obligations, but it must never be read as theorem completion.",
            proof_obligations=["Regenerate and validate the monitor whenever the active reasoning loop advances."],
            visual_encoding=visual("validation", "high", "route-blue", "monitor", "summary"),
        )
    )
    return events


def render_markdown(events: list[dict[str, Any]]) -> str:
    lines = [
        "# Reasoning Progress Log",
        "",
        f"- Target: `{events[0]['target_id'] if events else 'unknown'}`",
        f"- Events: {len(events)}",
        "",
        "## Progression",
        "",
    ]
    for row in events:
        lines.append(f"### {row['title']}")
        lines.append("")
        lines.append(row["narrative_summary"])
        lines.append("")
        lines.append(f"- Phase: `{row['phase']}`")
        lines.append(f"- Type: `{row['event_type']}`")
        lines.append(f"- Epistemic status: `{row['epistemic_status']}`")
        lines.append(f"- Conceptual move: {row['conceptual_move']}")
        lines.append(f"- Target commitments: `{', '.join(row['target_commitments'])}`")
        lines.append(f"- Evidence: `{', '.join(row['evidence_paths']) or 'explicit-unknown'}`")
        if row["proof_obligations"]:
            lines.append("- Proof obligations:")
            for obligation in row["proof_obligations"][:6]:
                lines.append(f"  - {obligation}")
        lines.append(f"- Uncertainty: {row['uncertainty']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default="ITER-0001")
    args = parser.parse_args()
    events = build_events(args.run_id)
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    trace_path = TRACE_DIR / f"{args.run_id}.jsonl"
    trace_path.write_text("\n".join(json.dumps(row, sort_keys=True, ensure_ascii=False) for row in events) + "\n", encoding="utf-8")
    write_json(
        REPORT_JSON,
        {
            "version": 1,
            "run_id": args.run_id,
            "target_id": events[0]["target_id"] if events else "",
            "event_count": len(events),
            "events": events,
        },
    )
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text(render_markdown(events), encoding="utf-8")
    print(f"Wrote {trace_path} with {len(events)} reasoning events")
    print(REPORT_JSON)
    print(REPORT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
