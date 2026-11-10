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
"""Build markdown and JSON reports for the active discovery marathon."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, utc_now, write_json
from artifact_or_stop_control import BLOCKER_REPORT, YM_TARGET_ID as ARTIFACT_YM_TARGET_ID
from avenue_literature_gap import load_target_warrant_package, package_warrants, target_warrant_latest_json, target_warrant_latest_md
from cycle_failure_archaeology import (
    build_failure_archaeology_report,
    summary_for_discovery_report as failure_summary_for_discovery_report,
    write_failure_archaeology_report,
)
from discovery_marathon_common import (
    LATEST_JSON,
    LATEST_MD,
    SMOKE_MD,
    generic_report_path_writable,
    load_branches,
    load_cycles,
    load_run_state,
    load_reviews,
    markdown_list,
    target_latest_json,
    target_latest_md,
    write_markdown,
)
from physical_relevance_impact import YM_TARGET_ID, build_physical_relevance_impact_packet, discover_physical_relevance_packets
from proof_depth_control import discover_proof_depth_packets
from target_profiles import target_profile
from visual_conceptualization import (
    build_visual_conceptualization_report,
    summary_for_discovery_report as visual_summary_for_discovery_report,
    write_visual_conceptualization_report,
)

RESULT_SUBGOAL_ATLAS = ROOT / "agentic/reports/result_subgoal_atlas/latest.json"
PVSNP_PROOF_DELIVERY_QUEUE = ROOT / "agentic/reports/pvsnp_proof_delivery_queue/latest.json"


def summarize_artifact_or_stop(target_id: str) -> dict[str, Any]:
    if clean_text(target_id) != ARTIFACT_YM_TARGET_ID:
        return {}
    report = load_optional_json(BLOCKER_REPORT)
    if clean_text(report.get("target_id")) != ARTIFACT_YM_TARGET_ID:
        return {
            "target_id": ARTIFACT_YM_TARGET_ID,
            "status": "not_generated",
            "latest_json": "",
            "gate_rule": "Run agentic/scripts/build_blocker_signature_report.py before the next YM endpoint marathon.",
        }
    control = report.get("artifact_or_stop_control", {}) if isinstance(report.get("artifact_or_stop_control"), dict) else {}
    endpoint = next(
        (
            row
            for row in report.get("signatures", [])
            if isinstance(row, dict) and clean_text(row.get("blocker_signature")) == "ym.endpoint_source_table_ttail_gate"
        ),
        {},
    )
    return {
        "target_id": ARTIFACT_YM_TARGET_ID,
        "status": "active" if control.get("endpoint_blocked") else "inactive",
        "endpoint_repetition_count": int(endpoint.get("repetition_count", 0) or 0),
        "endpoint_mode": clean_text(control.get("next_endpoint_mode") or endpoint.get("proposed_mode_switch")),
        "broad_api_marathon_blocked": bool(control.get("broad_api_marathon_blocked")),
        "missing_artifacts": endpoint.get("missing_artifacts", []),
        "branch_ids": endpoint.get("branch_ids", []),
        "latest_json": rel(BLOCKER_REPORT),
        "latest_html": rel(BLOCKER_REPORT.with_suffix(".html")),
        "endpoint_contract": clean_text(control.get("endpoint_contract")),
        "endpoint_pilot": clean_text(control.get("endpoint_pilot")),
        "demotion_packet": clean_text(control.get("demotion_packet")),
        "validator": clean_text(control.get("validator")) or "agentic/scripts/validate_artifact_or_stop_control.py",
        "gate_rule": (
            "The endpoint branch should not receive another broad API marathon until the endpoint artifact-or-stop gate emits "
            "the endpoint source table, a finite falsifier, or a quarantine/demotion packet."
        ),
    }


def summarize_branch(branch: dict[str, Any], cycles: list[dict[str, Any]]) -> dict[str, Any]:
    outputs = [
        output
        for cycle in cycles
        for output in cycle.get("branch_outputs", [])
        if output.get("branch_id") == branch.get("branch_id")
    ]
    latest = outputs[-1] if outputs else {}
    return {
        "branch_id": branch.get("branch_id"),
        "title": branch.get("title"),
        "status": branch.get("status"),
        "priority": branch.get("priority"),
        "attempt_count": branch.get("attempt_count", 0),
        "controlled_interface": branch.get("controlled_interface"),
        "latest_learning": latest.get("mathematical_learning", "No cycle output yet."),
        "latest_control_decision": latest.get("control_decision", {}),
        "next_experiment": latest.get("next_experiment") or branch.get("hypothesis"),
    }


def cycle_int(cycle: dict[str, Any]) -> int:
    raw = clean_text(cycle.get("cycle_id"))
    try:
        return int(raw.split("-")[-1])
    except ValueError:
        return 0


def first_branch_output(cycle: dict[str, Any]) -> dict[str, Any]:
    outputs = cycle.get("branch_outputs", [])
    return outputs[0] if outputs and isinstance(outputs[0], dict) else {}


def first_lemma(output: dict[str, Any]) -> dict[str, Any]:
    lemmas = output.get("candidate_lemmas", [])
    return lemmas[0] if lemmas and isinstance(lemmas[0], dict) else {}


def cycle_quality_summary(cycle: dict[str, Any]) -> dict[str, Any]:
    output = first_branch_output(cycle)
    lemma = first_lemma(output)
    record = (cycle.get("branch_execution_records") or [{}])[0]
    text = json.dumps(output, ensure_ascii=False).lower()
    physical_packet = physical_relevance_packet_for_output(cycle, output)
    return {
        "cycle_id": cycle.get("cycle_id"),
        "execution_mode": cycle.get("execution_mode", "synthetic_legacy"),
        "valid_as_research_cycle": bool(cycle.get("valid_as_research_cycle")),
        "research_seconds_elapsed": cycle.get("research_seconds_elapsed", 0),
        "branch_title": output.get("branch_title", ""),
        "engine": record.get("engine", ""),
        "api_attempt": record.get("api_attempt", ""),
        "model": record.get("model", ""),
        "reasoning_effort": record.get("reasoning_effort", ""),
        "max_output_tokens": record.get("max_output_tokens", 0),
        "lemma_count": len(output.get("candidate_lemmas", [])),
        "definition_count": len(lemma.get("definitions", [])),
        "assumption_count": len(lemma.get("assumptions", [])),
        "equation_count": len(lemma.get("equations", [])),
        "derivation_step_count": len(output.get("attempted_derivation", {}).get("steps", [])),
        "falsifier_count": len(output.get("falsifiers", [])),
        "dependency_update_count": len(output.get("dependency_updates", [])),
        "markers_ok": all(
            [
                "source object" in text,
                "target object" in text,
                "same-theory" in text or "same theory" in text,
                all(eq.get("valid_when") for eq in lemma.get("equations", [])),
            ]
        ),
        "mathematical_learning": output.get("mathematical_learning", cycle.get("cycle_learning", "")),
        "blocking_gap": output.get("attempted_derivation", {}).get("blocking_gap", ""),
        "next_experiment": output.get("next_experiment", ""),
        "control_decision": output.get("control_decision", {}),
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
            "major_publication_gate": physical_packet.get("major_publication_gate", {}),
            "general_impact_claim": clean_text(physical_packet.get("general_impact_claim")),
            "incremental_math_drift_risk": clean_text(physical_packet.get("incremental_math_drift_risk")),
            "next_physical_relevance_test": clean_text(physical_packet.get("next_physical_relevance_test")),
            "legacy_derived_assessment": bool(physical_packet.get("legacy_derived_assessment")),
        },
    }


def summarize_quality(research_cycles: list[dict[str, Any]]) -> dict[str, Any]:
    rows = [cycle_quality_summary(cycle) for cycle in research_cycles]
    if not rows:
        return {
            "research_cycles": 0,
            "engine_counts": {},
            "api_attempt_counts": {},
            "average_elapsed_seconds": 0,
            "minimum_quality": {},
            "all_markers_ok": False,
        }
    engine_counts: dict[str, int] = {}
    attempt_counts: dict[str, int] = {}
    for row in rows:
        engine_counts[row["engine"]] = engine_counts.get(row["engine"], 0) + 1
        attempt = row.get("api_attempt") or "not_api"
        attempt_counts[attempt] = attempt_counts.get(attempt, 0) + 1
    return {
        "research_cycles": len(rows),
        "engine_counts": engine_counts,
        "api_attempt_counts": attempt_counts,
        "average_elapsed_seconds": round(mean(float(row.get("research_seconds_elapsed", 0)) for row in rows), 3),
        "minimum_quality": {
            "lemmas": min(row["lemma_count"] for row in rows),
            "definitions": min(row["definition_count"] for row in rows),
            "assumptions": min(row["assumption_count"] for row in rows),
            "equations": min(row["equation_count"] for row in rows),
            "derivation_steps": min(row["derivation_step_count"] for row in rows),
            "falsifiers": min(row["falsifier_count"] for row in rows),
            "dependency_updates": min(row["dependency_update_count"] for row in rows),
        },
        "all_markers_ok": all(row["markers_ok"] for row in rows),
        "recent_research_cycles": rows[-12:],
    }


def summarize_proof_depth(cycles: list[dict[str, Any]]) -> dict[str, Any]:
    packets = []
    for cycle in cycles:
        packets.extend(discover_proof_depth_packets(cycle))
    release_counts: dict[str, int] = {}
    transfer_counts: dict[str, int] = {}
    pressure_counts: dict[str, int] = {}
    for packet in packets:
        release = clean_text(packet.get("release_decision")) or "missing"
        transfer = clean_text(packet.get("transfer_substance_audit", {}).get("verdict")) or "missing"
        pressure = clean_text(packet.get("pressure_kind")) or "missing"
        release_counts[release] = release_counts.get(release, 0) + 1
        transfer_counts[transfer] = transfer_counts.get(transfer, 0) + 1
        pressure_counts[pressure] = pressure_counts.get(pressure, 0) + 1
    return {
        "packet_count": len(packets),
        "release_decision_counts": release_counts,
        "transfer_substance_counts": transfer_counts,
        "pressure_kind_counts": pressure_counts,
        "active_skills": [
            "proof-depth-pressure-formalizer",
            "proof-hard-gate-selector",
            "proof-nontriviality-auditor",
            "proof-conceptual-quality-heuristic-rater",
            "proof-transfer-substance-auditor",
            "proof-same-domain-transfer-certifier",
            "proof-inference-learning-extractor",
            "proof-depth-release-gate",
        ],
        "proof_gate": "agentic/scripts/validate_proof_depth_control.py",
        "ledger_builder": "agentic/scripts/build_proof_learning_ledger.py",
        "lockin_report_builder": "agentic/scripts/build_proof_lockin_report.py",
    }


def physical_relevance_packet_for_output(cycle: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    existing = output.get("physical_relevance_impact")
    if isinstance(existing, dict):
        return existing
    if clean_text(cycle.get("target_id")) != YM_TARGET_ID:
        return {}
    try:
        index = cycle_int(cycle)
        packet = build_physical_relevance_impact_packet(
            output,
            {
                "target_id": cycle.get("target_id"),
                "branch_id": output.get("branch_id"),
                "controlled_interface": "",
            },
            index,
        )
    except Exception:
        return {}
    packet["legacy_derived_assessment"] = True
    return packet


def summarize_physical_relevance(cycles: list[dict[str, Any]]) -> dict[str, Any]:
    packets = []
    legacy_assessment_count = 0
    for cycle in cycles:
        direct = discover_physical_relevance_packets(cycle)
        if direct:
            packets.extend(direct)
            continue
        if clean_text(cycle.get("target_id")) != YM_TARGET_ID:
            continue
        for output in cycle.get("branch_outputs", []) if isinstance(cycle.get("branch_outputs"), list) else []:
            if not isinstance(output, dict):
                continue
            packet = physical_relevance_packet_for_output(cycle, output)
            if packet:
                packets.append(packet)
                legacy_assessment_count += 1
    decision_counts: dict[str, int] = {}
    investment_counts: dict[str, int] = {}
    carrier_counts: dict[str, int] = {}
    commitment_counts: dict[str, int] = {}
    unification_score_counts: dict[str, int] = {}
    for packet in packets:
        decision = clean_text(packet.get("relevance_decision")) or "missing"
        investment = clean_text(packet.get("major_publication_gate", {}).get("investment_decision")) or "missing"
        carrier = clean_text(packet.get("physical_carrier")) or "missing"
        unification_score = clean_text(
            packet.get("general_impact_vector", {})
            .get("unification_power", {})
            .get("score", "missing")
        )
        decision_counts[decision] = decision_counts.get(decision, 0) + 1
        investment_counts[investment] = investment_counts.get(investment, 0) + 1
        carrier_counts[carrier] = carrier_counts.get(carrier, 0) + 1
        unification_score_counts[unification_score] = unification_score_counts.get(unification_score, 0) + 1
        for commitment in packet.get("target_commitments_touched", []) if isinstance(packet.get("target_commitments_touched"), list) else []:
            item = clean_text(commitment) or "missing"
            commitment_counts[item] = commitment_counts.get(item, 0) + 1
    return {
        "packet_count": len(packets),
        "persisted_packet_count": len(packets) - legacy_assessment_count,
        "legacy_derived_assessment_count": legacy_assessment_count,
        "relevance_decision_counts": decision_counts,
        "major_publication_investment_counts": investment_counts,
        "physical_carrier_counts": carrier_counts,
        "target_commitment_counts": commitment_counts,
        "unification_power_score_counts": unification_score_counts,
        "active_skills": [
            "physical-relevance-impact-auditor",
            "main-problem-alignment-auditor",
            "paper-contribution-readiness-judge",
        ],
        "cycle_gate": "YM cycle-0352+ branch packets must expose physical carrier, target gate, unification power, general impact, and a major-publication investment decision before promotion.",
        "validator": "agentic/scripts/validate_discovery_marathon_cycle.py",
    }


def summarize_avenue_literature_gap(target_id: str) -> dict[str, Any]:
    package = load_target_warrant_package(target_id)
    warrants = package_warrants(package)
    decision_counts: dict[str, int] = {}
    mode_counts: dict[str, int] = {}
    top_warrants = []
    for warrant in warrants:
        decision = clean_text(warrant.get("investment_decision")) or "missing"
        decision_counts[decision] = decision_counts.get(decision, 0) + 1
        for mode in warrant.get("allowed_next_modes", []) if isinstance(warrant.get("allowed_next_modes"), list) else []:
            item = clean_text(mode)
            mode_counts[item] = mode_counts.get(item, 0) + 1
        top_warrants.append(
            {
                "avenue_id": clean_text(warrant.get("avenue_id")),
                "avenue_title": clean_text(warrant.get("avenue_title")),
                "investment_decision": decision,
                "allowed_next_modes": warrant.get("allowed_next_modes", []),
                "smallest_honest_claim": clean_text(warrant.get("smallest_honest_claim")),
                "gap_statement": clean_text(warrant.get("gap_statement")),
                "relevance_score": warrant.get("relevance_threshold", {}).get("score"),
                "field_impact_score": warrant.get("physics_or_field_impact", {}).get("score"),
                "unification_score": warrant.get("unification_power", {}).get("score"),
                "route_decision_score": warrant.get("route_decision_power", {}).get("score"),
                "next_decisive_test": clean_text(warrant.get("route_decision_power", {}).get("next_decisive_test")),
            }
        )
    return {
        "status": clean_text(package.get("status")) or ("missing" if not warrants else "available"),
        "target_id": clean_text(target_id),
        "warrant_count": len(warrants),
        "investment_decision_counts": decision_counts,
        "allowed_next_mode_counts": mode_counts,
        "warrants": top_warrants,
        "latest_json": rel(target_warrant_latest_json(target_id)),
        "latest_md": rel(target_warrant_latest_md(target_id)),
        "active_skill": "literature-gap-relevance-auditor",
        "validator": "agentic/scripts/validate_avenue_literature_gap_warrant.py",
        "gate_rule": (
            "Broad branch exploration is allowed only after a validated warrant states a precise literature gap, novelty boundary, "
            "field impact, unification power, route-decision power, and major-publication reward."
        ),
    }


def infer_job_run_id(events: list[dict[str, Any]]) -> str:
    for event in events:
        tail = clean_text(event.get("output_tail", ""))
        if "Ran " not in tail or " for " not in tail:
            continue
        after_for = tail.rsplit(" for ", 1)[-1]
        run_id = after_for.split(":", 1)[0].strip()
        if run_id:
            return run_id
    return ""


def load_job_summaries(run_id: str | None = None, limit: int = 5) -> list[dict[str, Any]]:
    job_dir = ROOT / "agentic/logs/discovery_marathon_jobs"
    if not job_dir.exists():
        return []
    manifests = sorted(job_dir.glob("*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    summaries: list[dict[str, Any]] = []
    expected_run_id = clean_text(run_id)
    for manifest_path in manifests:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        raw_log_path = clean_text(manifest.get("log_path", ""))
        log_path = ROOT / raw_log_path if raw_log_path else Path()
        events: list[dict[str, Any]] = []
        if raw_log_path and log_path.is_file():
            for raw in log_path.read_text(encoding="utf-8").splitlines():
                try:
                    event = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if isinstance(event, dict):
                    events.append(event)
        inferred_run_id = infer_job_run_id(events)
        if expected_run_id and inferred_run_id and inferred_run_id != expected_run_id:
            continue
        if expected_run_id and not inferred_run_id and expected_run_id not in manifest_path.stem:
            continue
        summaries.append(
            {
                "job_id": manifest.get("job_id", manifest_path.stem),
                "run_id": inferred_run_id,
                "status": manifest.get("status", ""),
                "completed_cycles": manifest.get("completed_cycles", 0),
                "failed_cycle_attempts": manifest.get("failed_cycle_attempts", 0),
                "duration_seconds": manifest.get("duration_seconds", 0),
                "updated_utc": manifest.get("updated_utc", ""),
                "log_path": raw_log_path,
                "event_count": len(events),
                "failure_events": [event for event in events if event.get("event") == "cycle_attempt_failed"],
                "last_event": events[-1] if events else {},
            }
        )
        if len(summaries) >= limit:
            break
    return summaries


def story_headline_for_target(target_id: str | None) -> str:
    profile = target_profile(target_id)
    if profile.get("target_id") == "p-vs-np-target":
        return (
            "The active discovery route is now concentrated on target-preserving complexity-theoretic bridges: "
            "turning weak lower-bound, meta-complexity, proof-complexity, or derandomization interfaces into explicit "
            "threshold transfers without importing nonuniform leakage or barrier-evading slogans."
        )
    if profile.get("target_id") == "yang-mills-existence-and-mass-gap-target":
        return (
            "The active discovery route is now concentrated on a same-theory reflection-positivity bridge: "
            "turning controlled collar/RG positivity into continuum OS positivity without smuggling in a boundary sector."
        )
    return (
        f"The active discovery route is concentrated on {clean_text(profile.get('display_name', 'the target'))}: "
        "turning target-preserving bridge lemmas, calculations, falsifiers, and backtrack decisions into controlled progress."
    )


def build_current_story(research_cycles: list[dict[str, Any]], target_id: str | None = None) -> dict[str, Any]:
    rows = [cycle_quality_summary(cycle) for cycle in research_cycles]
    if not rows:
        return {
            "headline": "No real research cycle has completed yet.",
            "current_obstruction": "",
            "latest_learning": "",
            "next_experiment": "",
            "recent_storyline": [],
        }
    latest = rows[-1]
    recent = rows[-5:]
    return {
        "headline": story_headline_for_target(target_id),
        "current_obstruction": latest.get("blocking_gap", ""),
        "latest_learning": latest.get("mathematical_learning", ""),
        "next_experiment": latest.get("next_experiment", ""),
        "recent_storyline": [
            {
                "cycle_id": row["cycle_id"],
                "branch_title": row["branch_title"],
                "learning": row["mathematical_learning"],
                "next_experiment": row["next_experiment"],
            }
            for row in recent
        ],
    }


def build_completed_subgoal_enablement_analysis(
    target_id: str,
    research_cycles: list[dict[str, Any]],
) -> dict[str, Any]:
    """Summarize how completed or near-completed subgoals enable the larger target."""
    if clean_text(target_id) != "p-vs-np-target":
        return {}
    atlas = load_optional_json(RESULT_SUBGOAL_ATLAS)
    if clean_text(atlas.get("target_id")) != "p-vs-np-target":
        atlas = {}
    proof_queue = load_optional_json(PVSNP_PROOF_DELIVERY_QUEUE)
    if clean_text(proof_queue.get("target_id")) and clean_text(proof_queue.get("target_id")) != "p-vs-np-target":
        proof_queue = {}
    latest_cycle = cycle_quality_summary(research_cycles[-1]) if research_cycles else {}
    results = atlas.get("results", []) if isinstance(atlas.get("results"), list) else []
    status_counts: dict[str, int] = {}
    for result in results:
        if not isinstance(result, dict):
            continue
        status = clean_text(result.get("achievement_status")) or "unknown"
        status_counts[status] = status_counts.get(status, 0) + 1
    proof_items = proof_queue.get("items", []) if isinstance(proof_queue.get("items"), list) else []
    top_items = [
        {
            "proof_object_id": clean_text(item.get("queue_id")),
            "title": clean_text(item.get("title")),
            "proof_status": clean_text(item.get("proof_status")),
            "source_anchor": clean_text(item.get("source_anchor")),
            "theorem_goal": clean_text(item.get("theorem_goal")),
            "source_object": clean_text(item.get("source_object")),
            "target_object": clean_text(item.get("target_object")),
            "next_analysis": clean_text(item.get("next_analysis")),
        }
        for item in proof_items[:5]
        if isinstance(item, dict)
    ]
    completed_subgoals = [
        {
            "subgoal_id": "pvsnp.enablement.transparent-row-support",
            "completed_subgoal": "TransparentRowSupport_N parser/falsifier abstraction over FormulaEval selector cases",
            "achievement_status": "proof_delivery_ready",
            "enablement_class": "paper_handoff_enabled",
            "bigger_problem_gate": "Replace selector-case accumulation with one transparent-support theorem and one hidden-support countermodel before any larger P vs NP claim can be evaluated.",
            "before_gate": "The marathon was still adding FormulaEval selector variants whose relation to the larger target was easy to overstate.",
            "after_gate": "The route now has a named theorem/countermodel pair and can move from exploration into proof delivery and paper-module packaging.",
            "enablement_mechanism": "The completed abstraction lets future work ask whether a rule has visible, charged, influence-closed support or must be quarantined behind a private-row/unread-enable-bit countermodel.",
            "residual_blockers": [
                "Write the referee-checkable proof packet.",
                "Resolve or quarantine RealSATInfluenceRealizer_N for concrete semantic FormulaEval rules.",
                "Do not infer P != NP or SAT notin P/poly from the parser/falsifier theorem.",
            ],
            "evidence_sources": [
                "agentic/reports/pvsnp_proof_delivery_queue/latest.json",
                "agentic/reports/timeline_paper/latest.json",
                "cycles 103-120",
            ],
            "next_consumer": "proof-delivery-workflow-orchestrator and subgoal-enablement-handoff-packager",
        },
        {
            "subgoal_id": "pvsnp.enablement.qctsr-ranked-verifier",
            "completed_subgoal": "Ranked QCTSR same-theory verifier/minimality packet",
            "achievement_status": "route_decision_ready",
            "enablement_class": "route_decision_enabled",
            "bigger_problem_gate": "Decide whether quotient compression is a legitimate same-theory proof step or a semantic row-deletion overclaim.",
            "before_gate": "Quotient compression could be described as if EqSAT-equivalent counterfactual children were freely mergeable.",
            "after_gate": "Cycle 145 states the allowed condition: compression is valid only when proof-carrying certificates are ranked, dependency-closed, and charged before use.",
            "enablement_mechanism": "The first rejected quotient merge becomes a private-row falsifier, so the branch can test a toy QCTSR proof instead of repeating the quotient slogan.",
            "residual_blockers": [
                "Instantiate the finite verifier on a two-child EqSAT/CTSR example.",
                "Delete one certificate edge and write the two-world private-row falsifier.",
                "Keep arbitrary semantic FormulaEval quarantined unless RealSATInfluenceRealizer_N^{arb} is supplied.",
            ],
            "evidence_sources": [
                "cycle-0145",
                "agentic/runs/discovery_marathons/p-vs-np-marathon/cycles/cycle-0145.json",
            ],
            "next_consumer": "completed-subgoal-enablement-auditor and next-experiment-queue-ranker",
        },
        {
            "subgoal_id": "pvsnp.enablement.l120-paper-module",
            "completed_subgoal": "L120 least-closed support theorem/countermodel module",
            "achievement_status": "paper_module_ready_for_validation",
            "enablement_class": "validation_enabled",
            "bigger_problem_gate": "Determine which parser/falsifier claims can be promoted into the P vs NP paper without leaking semantic advice or hiding transfer assumptions.",
            "before_gate": "The L120 material was visible in the timeline but not forced through a source/target/validity promotion gate.",
            "after_gate": "The proof-delivery queue names the L120 theorem/countermodel package, inference-quality gate, and proof-audit packet as concrete next consumers.",
            "enablement_mechanism": "The report can now separate theorem-shaped proof objects from broad exploration and attach promotion/demotion tests to each proof packet.",
            "residual_blockers": [
                "Close L120 inference-quality marker gaps.",
                "Run prior-art and disqualifier checks before external paper claims.",
                "Maintain the non-claim boundary: this is a route-specific parser/falsifier contribution, not P != NP.",
            ],
            "evidence_sources": [
                "agentic/reports/pvsnp_proof_delivery_queue/latest.json",
                "agentic/reports/pvsnp_inference_quality/latest.json",
            ],
            "next_consumer": "proof-quality-gatekeeper and subgoal-enablement-handoff-packager",
        },
    ]
    return {
        "status": "completed_subgoal_enablement_analysis_ready",
        "generated_by_skills": [
            "completed-subgoal-enablement-auditor",
            "subgoal-enablement-handoff-packager",
        ],
        "target_id": "p-vs-np-target",
        "atlas_status_counts": status_counts,
        "proof_delivery_queue_status": clean_text(proof_queue.get("status")),
        "top_proof_objects": top_items,
        "latest_cycle_id": clean_text(latest_cycle.get("cycle_id")),
        "summary": (
            "The completed or near-completed subgoals currently enable proof delivery, route decisions, validation, "
            "and paper-module packaging. They do not enable a claim that P != NP is proved. Their value is that the "
            "larger problem now has sharper gates: transparent support versus hidden semantic support, ranked same-theory "
            "quotient compression versus private-row falsifier, and L120 promotion versus quarantine."
        ),
        "completed_subgoals": completed_subgoals,
        "overclaim_boundary": (
            "No completed subgoal in this report proves P != NP, SAT notin P/poly, or an all-exponent lower bound. "
            "The enabled work is a route-specific proof-delivery and paper-boundary program."
        ),
        "validation_handoff": (
            "Use completed-subgoal-enablement-auditor before marking any atlas entry handoff-ready, then use "
            "subgoal-enablement-handoff-packager to add the enablement relation to the atlas, timeline, proof queue, or paper text."
        ),
    }


def build_report(run_state: dict[str, Any]) -> dict[str, Any]:
    target_id = clean_text(run_state.get("target_id", ""))
    branches = load_branches(run_state)
    cycles = load_cycles(run_state)
    reviews = load_reviews(run_state)
    research_cycles = [cycle for cycle in cycles if cycle.get("valid_as_research_cycle")]
    synthetic_cycles = [cycle for cycle in cycles if not cycle.get("valid_as_research_cycle")]
    branch_summaries = [summarize_branch(branch, cycles) for branch in branches]
    quality_summary = summarize_quality(research_cycles)
    job_summaries = load_job_summaries(run_state.get("run_id", ""))
    failure_archaeology = build_failure_archaeology_report(run_state, cycles)
    visual_conceptualization = build_visual_conceptualization_report(run_state, cycles)
    artifact_or_stop_summary = summarize_artifact_or_stop(target_id)
    impact_control_bullet = (
        "Physical relevance and general impact are now explicit for Yang-Mills: local mathematics is support-only unless it names a physical carrier, target gate, unification-power payoff, and demotion-ready impact test."
        if target_id == "yang-mills-existence-and-mass-gap-target"
        else "Field relevance and general impact are now explicit: local route work is support-only unless it names a target carrier, target gate, unification-power payoff, and demotion-ready impact test."
    )
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "purpose": "Discovery Marathon report with controlled interface summaries, latest learning per branch, branch memory, cycle learning, skill-dispatch validation, real research cycle counts, synthetic smoke or legacy counts, and what actually changed.",
        "run_id": run_state.get("run_id", ""),
        "target_id": target_id,
        "status": run_state.get("status", "no_active_run"),
        "canonical_initialization": run_state.get("canonical_initialization"),
        "cycle_count": run_state.get("cycle_count", 0),
        "research_cycle_count": len(research_cycles),
        "synthetic_cycle_count": len(synthetic_cycles),
        "wall_clock_budget_minutes": run_state.get("wall_clock_budget_minutes", 0),
        "cycle_minutes": run_state.get("cycle_minutes", 0),
        "branch_summaries": branch_summaries,
        "research_quality_summary": quality_summary,
        "proof_depth_control_summary": summarize_proof_depth(research_cycles),
        "avenue_literature_gap_summary": summarize_avenue_literature_gap(target_id),
        "physical_relevance_impact_summary": summarize_physical_relevance(research_cycles),
        "failure_archaeology": failure_archaeology,
        "failure_archaeology_summary": failure_summary_for_discovery_report(failure_archaeology),
        "visual_conceptualization": visual_conceptualization,
        "visual_conceptualization_summary": visual_summary_for_discovery_report(visual_conceptualization),
        "artifact_or_stop_summary": artifact_or_stop_summary,
        "current_mathematical_story": build_current_story(research_cycles, target_id),
        "completed_subgoal_enablement_analysis": build_completed_subgoal_enablement_analysis(
            target_id,
            research_cycles,
        ),
        "latest_job_summaries": job_summaries,
        "cycle_summaries": [
            cycle_quality_summary(cycle)
            for cycle in cycles
        ],
        "deep_reviews": [
            {
                "review_id": review.get("review_id"),
                "summary": review.get("summary", ""),
                "recommendation": review.get("recommendation", ""),
            }
            for review in reviews
        ],
        "what_actually_changed": [
            "The marathon created durable branch-local mathematical memory.",
            "Each cycle produced theorem-shaped branch outputs with equations, assumptions, falsifiers, and next experiments.",
            "Skill dispatch is now explicit and validated rather than implicit in a workflow name.",
            "Completed subgoal enablement is now explicit: completed or near-completed subgoals are interpreted by the gate they open for the larger target, not by completion alone.",
            "Literature-gap preinvestment is now explicit: broad branch exploration needs a validated avenue warrant with closest-known-result accounting, novelty boundary, field impact, unification power, and route-decision power.",
            impact_control_bullet,
            (
                "Artifact-or-stop control is active for the YM endpoint branch: repeated source-table/T_tail blockers now require an artifact sprint, falsifier sprint, publication demotion, or quarantine before another broad endpoint API marathon."
                if artifact_or_stop_summary.get("status") == "active"
                else "Artifact-or-stop control is available but no repeated YM endpoint artifact blocker is currently active."
            ),
            "Visual conceptualization is now controlled: metaphors must preserve named theorem properties, expose distortions, and generate an audited route consequence before affecting proof search.",
            f"Research cycle count is {len(research_cycles)}; synthetic smoke/legacy packet count is {len(synthetic_cycles)}.",
        ]
        if cycles
        else [run_state.get("canonical_initialization", {}).get("summary")
              or "The marathon is initialized but has not yet run an exploration cycle."],
        "next_queue": run_state.get("active_branch_ids", []),
        "breakthrough_status": "no_breakthrough_claimed",
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Discovery Marathon Report",
        "",
        f"Run: `{report['run_id']}`",
        f"Target: `{report['target_id']}`",
        f"Status: `{report['status']}`",
        f"Persisted cycle packets: {report['cycle_count']}",
        f"Research cycles: {report.get('research_cycle_count', 0)}",
        f"Synthetic smoke/legacy packets: {report.get('synthetic_cycle_count', 0)}",
        "",
        "## What Actually Changed",
        "",
        markdown_list(report["what_actually_changed"]),
        "## Latest Job Health",
        "",
    ]
    jobs = report.get("latest_job_summaries", [])
    if jobs:
        for job in jobs[:3]:
            lines.extend(
                [
                    f"### {job.get('job_id')}",
                    "",
                    f"Status: `{job.get('status')}`",
                    f"Completed cycles: `{job.get('completed_cycles', 0)}`",
                    f"Failed operational attempts: `{job.get('failed_cycle_attempts', 0)}`",
                    f"Updated UTC: `{job.get('updated_utc')}`",
                    f"Log: `{job.get('log_path')}`",
                    "",
                ]
            )
            failures = job.get("failure_events", [])
            if failures:
                lines.append("Operational failures, not counted as research:")
                lines.append("")
                for failure in failures[-3:]:
                    lines.append(f"- Cycle attempt `{failure.get('cycle_number_in_job')}`: {clean_text(failure.get('output_tail'))[:500]}")
                lines.append("")
    else:
        lines.extend(["No marathon job logs found.", ""])
    quality = report.get("research_quality_summary", {})
    proof_depth = report.get("proof_depth_control_summary", {})
    literature_gap = report.get("avenue_literature_gap_summary", {})
    physical = report.get("physical_relevance_impact_summary", {})
    artifact_or_stop = report.get("artifact_or_stop_summary", {})
    failure_archaeology = report.get("failure_archaeology_summary", {})
    visual_summary = report.get("visual_conceptualization_summary", {})
    lines.extend(
        [
            "## Research Quality",
            "",
            f"Real research cycles: `{quality.get('research_cycles', 0)}`",
            f"Engine counts: `{quality.get('engine_counts', {})}`",
            f"API attempt counts: `{quality.get('api_attempt_counts', {})}`",
            f"Average elapsed seconds: `{quality.get('average_elapsed_seconds', 0)}`",
            f"All source/target/same-theory/validity markers present: `{quality.get('all_markers_ok', False)}`",
            f"Minimum quality counts: `{quality.get('minimum_quality', {})}`",
            "",
            "## Proof Depth Control",
            "",
            f"Proof-depth packets: `{proof_depth.get('packet_count', 0)}`",
            f"Release decisions: `{proof_depth.get('release_decision_counts', {})}`",
            f"Transfer-substance verdicts: `{proof_depth.get('transfer_substance_counts', {})}`",
            f"Pressure kinds: `{proof_depth.get('pressure_kind_counts', {})}`",
            f"Validator: `{proof_depth.get('proof_gate', 'agentic/scripts/validate_proof_depth_control.py')}`",
            "",
            "## Literature Gap Preinvestment Gate",
            "",
            f"Warrants: `{literature_gap.get('warrant_count', 0)}`",
            f"Investment decisions: `{literature_gap.get('investment_decision_counts', {})}`",
            f"Allowed next modes: `{literature_gap.get('allowed_next_mode_counts', {})}`",
            f"Full packet JSON: `{literature_gap.get('latest_json', '')}`",
            f"Full packet Markdown: `{literature_gap.get('latest_md', '')}`",
            f"Validator: `{literature_gap.get('validator', 'agentic/scripts/validate_avenue_literature_gap_warrant.py')}`",
            "",
            clean_text(literature_gap.get("gate_rule", "")),
            "",
            "## Physical Relevance And General Impact",
            "",
            f"Physical-impact assessments: `{physical.get('packet_count', 0)}`",
            f"Persisted packets: `{physical.get('persisted_packet_count', 0)}`",
            f"Legacy derived assessments: `{physical.get('legacy_derived_assessment_count', 0)}`",
            f"Relevance decisions: `{physical.get('relevance_decision_counts', {})}`",
            f"Major-publication investment decisions: `{physical.get('major_publication_investment_counts', {})}`",
            f"Physical carriers: `{physical.get('physical_carrier_counts', {})}`",
            f"Target commitments: `{physical.get('target_commitment_counts', {})}`",
            f"Unification-power scores: `{physical.get('unification_power_score_counts', {})}`",
            f"Validator: `{physical.get('validator', 'agentic/scripts/validate_discovery_marathon_cycle.py')}`",
            "",
            # This control belongs to Yang–Mills. Rendering it for another
            # target would turn absent evidence into a misleading clear gate.
            *([
            "## Artifact-Or-Stop Anti-Incrementality Gate",
            "",
            f"Status: `{artifact_or_stop.get('status', 'not_generated')}`",
            f"Endpoint repetition count: `{artifact_or_stop.get('endpoint_repetition_count', 0)}`",
            f"Endpoint mode: `{artifact_or_stop.get('endpoint_mode', '')}`",
            f"Broad API endpoint marathon blocked: `{artifact_or_stop.get('broad_api_marathon_blocked', False)}`",
            f"Missing artifacts: `{artifact_or_stop.get('missing_artifacts', [])}`",
            f"Branch ids: `{artifact_or_stop.get('branch_ids', [])}`",
            f"Full blocker JSON: `{artifact_or_stop.get('latest_json', '')}`",
            f"Full blocker HTML: `{artifact_or_stop.get('latest_html', '')}`",
            f"Endpoint contract: `{artifact_or_stop.get('endpoint_contract', '')}`",
            f"Endpoint pilot: `{artifact_or_stop.get('endpoint_pilot', '')}`",
            f"Demotion packet: `{artifact_or_stop.get('demotion_packet', '')}`",
            f"Validator: `{artifact_or_stop.get('validator', 'agentic/scripts/validate_artifact_or_stop_control.py')}`",
            "",
            clean_text(artifact_or_stop.get("gate_rule", "")),
            "",
            ] if clean_text(report.get("target_id")) == ARTIFACT_YM_TARGET_ID else []),
            "## Failure Archaeology And Failed-Hypothesis Premortem",
            "",
            f"Failure detected in latest major cycle set: `{failure_archaeology.get('failure_detected', False)}`",
            f"Cycle set: `{failure_archaeology.get('cycle_set_id', '')}`",
            f"Disposition: `{failure_archaeology.get('route_disposition', '')}`",
            f"Detected heuristics: `{failure_archaeology.get('detected_heuristics', [])}`",
            f"Full packet JSON: `{failure_archaeology.get('latest_json', '')}`",
            f"Full packet Markdown: `{failure_archaeology.get('latest_md', '')}`",
            "",
            clean_text(failure_archaeology.get("failure_summary", "")),
            "",
            "## Visual Conceptualization Reflection",
            "",
            f"Conceptualizations: `{visual_summary.get('concept_count', 0)}`",
            f"Hypothesis outputs: `{visual_summary.get('hypothesis_output_count', 0)}`",
            f"Quarantined or rejected analogies: `{visual_summary.get('quarantined_or_rejected_count', 0)}`",
            f"Headline metaphor: `{visual_summary.get('headline_metaphor', '')}`",
            f"Route consequences: `{visual_summary.get('route_consequences', [])}`",
            f"Full packet JSON: `{visual_summary.get('latest_json', '')}`",
            f"Full packet Markdown: `{visual_summary.get('latest_md', '')}`",
            f"Validator: `{visual_summary.get('validator', 'agentic/scripts/validate_visual_conceptualization_packet.py')}`",
            "",
            "Visual analogies in this report are reflection artifacts only unless the preservation audit promotes a concrete route mutation, missing artifact, falsifier, counterfactual variant, or representation requirement.",
            "",
        ]
    )
    for warrant in literature_gap.get("warrants", []):
        lines.extend(
            [
                f"### {clean_text(warrant.get('avenue_title'))}",
                "",
                f"- Avenue: `{clean_text(warrant.get('avenue_id'))}`",
                f"- Decision: `{clean_text(warrant.get('investment_decision'))}`",
                f"- Scores: relevance `{warrant.get('relevance_score')}`, field impact `{warrant.get('field_impact_score')}`, unification `{warrant.get('unification_score')}`, route decision `{warrant.get('route_decision_score')}`",
                f"- Next decisive test: {clean_text(warrant.get('next_decisive_test'))}",
                "",
            ]
        )
    lines.extend(
        [
            "## Current Mathematical Story",
            "",
        ]
    )
    story = report.get("current_mathematical_story", {})
    lines.extend(
        [
            clean_text(story.get("headline", "")),
            "",
            f"Latest learning: {clean_text(story.get('latest_learning', ''))}",
            "",
            f"Current obstruction: {clean_text(story.get('current_obstruction', ''))}",
            "",
            f"Next experiment: {clean_text(story.get('next_experiment', ''))}",
            "",
            "### Recent Storyline",
            "",
        ]
    )
    for row in story.get("recent_storyline", []):
        lines.extend(
            [
                f"- `{row.get('cycle_id')}` {clean_text(row.get('learning'))}",
                "",
            ]
        )
    enablement = report.get("completed_subgoal_enablement_analysis", {})
    if enablement:
        lines.extend(
            [
                "## Completed Subgoal Enablement Analysis",
                "",
                clean_text(enablement.get("summary")),
                "",
                f"Generated by skills: `{', '.join(enablement.get('generated_by_skills', []))}`",
                "",
                f"Overclaim boundary: {clean_text(enablement.get('overclaim_boundary'))}",
                "",
            ]
        )
        for row in enablement.get("completed_subgoals", []):
            lines.extend(
                [
                    f"### {clean_text(row.get('completed_subgoal'))}",
                    "",
                    f"- Enablement class: `{clean_text(row.get('enablement_class'))}`",
                    f"- Bigger-problem gate: {clean_text(row.get('bigger_problem_gate'))}",
                    f"- Before gate: {clean_text(row.get('before_gate'))}",
                    f"- After gate: {clean_text(row.get('after_gate'))}",
                    f"- Mechanism: {clean_text(row.get('enablement_mechanism'))}",
                    f"- Next consumer: `{clean_text(row.get('next_consumer'))}`",
                    "",
                    "Residual blockers:",
                    "",
                    markdown_list(row.get("residual_blockers", [])),
                    "",
                ]
            )
        lines.extend(
            [
                f"Validation handoff: {clean_text(enablement.get('validation_handoff'))}",
                "",
            ]
        )
    lines.extend(
        [
            "## Recent Research Cycles",
            "",
        ]
    )
    for cycle in quality.get("recent_research_cycles", []):
        lines.extend(
            [
                f"### {cycle.get('cycle_id')}",
                "",
                f"Branch: {cycle.get('branch_title')}",
                f"Engine: `{cycle.get('engine')}` / attempt `{cycle.get('api_attempt') or 'not_api'}`",
                f"Elapsed research seconds: `{cycle.get('research_seconds_elapsed', 0)}`",
                f"Quality counts: lemmas `{cycle.get('lemma_count')}`, equations `{cycle.get('equation_count')}`, steps `{cycle.get('derivation_step_count')}`, falsifiers `{cycle.get('falsifier_count')}`, dependencies `{cycle.get('dependency_update_count')}`",
                f"Proof depth: `{cycle.get('proof_depth_control', {})}`",
                f"Physical relevance: `{cycle.get('physical_relevance_impact', {})}`",
                "",
                f"Learning: {clean_text(cycle.get('mathematical_learning'))}",
                "",
                f"Next experiment: {clean_text(cycle.get('next_experiment'))}",
                "",
            ]
        )
    lines.extend(
        [
        "## Branch Learning",
        "",
        ]
    )
    for branch in report.get("branch_summaries", []):
        lines.extend(
            [
                f"### {branch['title']}",
                "",
                f"Controlled interface: `{branch['controlled_interface']}`",
                "",
                f"Latest learning: {branch['latest_learning']}",
                "",
                f"Control: `{branch.get('latest_control_decision', {}).get('decision', 'pending')}`",
                "",
                f"Next experiment: {branch['next_experiment']}",
                "",
            ]
        )
    lines.extend(["## Cycle Learning", ""])
    lines.append("Showing the latest persisted cycles here; older synthetic legacy cycles remain in the JSON report but are not foregrounded.")
    lines.append("")
    for cycle in report.get("cycle_summaries", [])[-20:]:
        lines.extend(
            [
                f"### {cycle['cycle_id']}",
                "",
                f"Execution mode: `{cycle.get('execution_mode', 'synthetic_legacy')}`",
                f"Valid as research cycle: `{cycle.get('valid_as_research_cycle', False)}`",
                f"Elapsed research seconds: `{cycle.get('research_seconds_elapsed', 0)}`",
                "",
                clean_text(cycle.get("mathematical_learning")),
                "",
            ]
        )
    lines.extend(["## Deep Reviews", ""])
    if report.get("deep_reviews"):
        for review in report["deep_reviews"]:
            lines.extend([f"### {review['review_id']}", "", review.get("summary", ""), "", f"Recommendation: `{review.get('recommendation')}`", ""])
    else:
        lines.append("No deep review has been recorded yet.")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id")
    parser.add_argument("--target-id")
    args = parser.parse_args()
    _, run_state = load_run_state(args.run_id, args.target_id)
    if not run_state:
        report = {
            "version": 1,
            "generated_utc": utc_now(),
            "run_id": "",
            "target_id": "",
            "status": "no_active_run",
            "cycle_count": 0,
            "research_cycle_count": 0,
            "synthetic_cycle_count": 0,
            "branch_summaries": [],
            "proof_depth_control_summary": summarize_proof_depth([]),
            "avenue_literature_gap_summary": {},
            "failure_archaeology": {},
            "failure_archaeology_summary": {},
            "visual_conceptualization": {},
            "visual_conceptualization_summary": {},
            "cycle_summaries": [],
            "deep_reviews": [],
            "what_actually_changed": ["No active discovery marathon is present."],
            "next_queue": [],
            "breakthrough_status": "no_breakthrough_claimed",
        }
    else:
        report = build_report(run_state)
    markdown = render_markdown(report)
    if report.get("failure_archaeology"):
        paths = write_failure_archaeology_report(report["failure_archaeology"])
        print(f"Wrote failure archaeology {rel(paths['latest_json'])} and {rel(paths['latest_md'])}")
    if report.get("visual_conceptualization"):
        visual_paths = write_visual_conceptualization_report(report["visual_conceptualization"])
        print(f"Wrote visual conceptualization {rel(visual_paths['latest_json'])} and {rel(visual_paths['latest_md'])}")
    target_id = clean_text(report.get("target_id"))
    if target_id:
        scoped_json = target_latest_json(target_id)
        scoped_md = target_latest_md(target_id)
        write_json(scoped_json, report)
        write_markdown(scoped_md, markdown)
        print(f"Wrote target-scoped {rel(scoped_json)} and {rel(scoped_md)}")
    if generic_report_path_writable(LATEST_JSON, target_id) and generic_report_path_writable(LATEST_MD, target_id):
        write_json(LATEST_JSON, report)
        write_markdown(LATEST_MD, markdown)
        print(f"Wrote compatibility {rel(LATEST_JSON)} and {rel(LATEST_MD)}")
    else:
        print(
            "Skipped compatibility discovery marathon latest files because they are scoped to a different target; "
            f"use {rel(target_latest_json(target_id))} and {rel(target_latest_md(target_id))}."
        )
    if "yang-mills" in report.get("target_id", ""):
        write_markdown(SMOKE_MD, markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
