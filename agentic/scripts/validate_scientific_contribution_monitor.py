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
"""Validate the scientific contribution monitor and anti-infinite-branch controls."""

from __future__ import annotations

from agentic_common import clean_text, fail, load_json_object, rel

from build_scientific_contribution_monitor import CONTRIBUTION_SKILLS, OUT_JSON, OUT_MD


REQUIRED_METRICS = {
    "active_candidate_count",
    "certification_ready_count",
    "good_enough_count",
    "contribution_shaped_count",
    "near_stepping_stone_count",
    "publishable_handoff_count",
    "average_contribution_score",
    "average_publishable_subgoal_score",
    "average_paper_relevance_marker_score",
    "strong_paper_relevance_candidate_count",
    "paper_relevance_ready_count",
    "novelty_pressure",
    "explanatory_gain",
    "implication_payoff",
    "staleness",
    "infinite_progression_risk_count",
}


def require_text(row: dict, field: str, context: str) -> None:
    if not clean_text(row.get(field)):
        fail(f"{context} missing {field}")


def main() -> int:
    if not OUT_JSON.exists():
        fail(f"missing {rel(OUT_JSON)}")
    report = load_json_object(OUT_JSON)
    for field in [
        "version",
        "generated_utc",
        "loop_policy",
        "contribution_aim_status",
        "next_contribution_objective",
        "metrics",
        "validation_gap",
        "target_id",
        "novelty_high_reward_signals",
        "candidates",
    ]:
        if field not in report:
            fail(f"{rel(OUT_JSON)} missing {field}")
    policy_text = clean_text(report.get("loop_policy", {})).lower().replace("_", " ")
    for phrase in ["standing objective", "good enough", "anti infinite progression", "stepping stone maturity"]:
        if phrase not in policy_text:
            fail(f"{rel(OUT_JSON)} loop_policy missing `{phrase}`")
    criteria = report.get("loop_policy", {}).get("paper_relevance_marker_criteria", {})
    baseline_dims = {"conceptual_depth", "conceptual_novelty", "unblocking_power", "applicability", "understanding_gain"}
    for dimension in ["conceptual_depth", "conceptual_novelty", "unblocking_power", "applicability", "understanding_gain"]:
        if dimension not in criteria:
            fail(f"{rel(OUT_JSON)} loop_policy missing paper relevance criterion {dimension}")
    expected_dims = set(criteria)
    if not baseline_dims.issubset(expected_dims):
        fail(f"{rel(OUT_JSON)} loop_policy paper relevance criteria must include baseline dimensions")
    metrics = report.get("metrics", {})
    missing = REQUIRED_METRICS.difference(metrics)
    if missing:
        fail(f"{rel(OUT_JSON)} metrics missing {sorted(missing)}")
    candidates = report.get("candidates", [])
    if not isinstance(candidates, list) or len(candidates) < 3:
        fail(f"{rel(OUT_JSON)} needs at least three contribution candidates")
    if int(metrics.get("active_candidate_count", 0)) < 1:
        fail(f"{rel(OUT_JSON)} must keep at least one active contribution candidate or report contribution_search_needed")
    for index, candidate in enumerate(candidates, start=1):
        context = f"candidate {index}"
        for field in [
            "candidate_id",
            "cycle_id",
            "branch_title",
            "contribution_type",
            "status",
            "stepping_stone_maturity",
            "score",
            "exploration_payoff_score",
            "publishable_subgoal_score",
            "paper_relevance_markers",
            "good_enough_paper_relevance",
            "missing_to_good_enough_paper",
            "scores",
            "smallest_honest_claim",
            "why_it_could_stand_alone",
            "evidence_basis",
            "validation_burden",
            "overclaim_boundary",
            "implication_map",
            "required_skills",
            "branch_control_decision",
            "branch_control_reason",
            "good_enough_when",
            "continue_only_if",
            "stop_when",
            "infinite_progression_risk",
            "handoff_hard_gates",
            "prior_art_boundary",
            "disqualifier_tests",
            "missing_to_publishable",
            "paper_note_shape",
            "why_this_budget_now",
        ]:
            if field not in candidate or (field not in {"score", "scores"} and not candidate.get(field)):
                fail(f"{context} missing {field}")
        if candidate["stepping_stone_maturity"] not in {"contribution_shaped", "near_stepping_stone", "publishable_handoff_ready"}:
            fail(f"{context} invalid stepping_stone_maturity")
        if candidate.get("status") == "good_enough_to_handoff" and candidate.get("stepping_stone_maturity") != "publishable_handoff_ready":
            fail(f"{context} uses good_enough_to_handoff without publishable maturity")
        if int(candidate.get("publishable_subgoal_score", 0)) > int(candidate.get("exploration_payoff_score", 0)):
            fail(f"{context} publishable_subgoal_score cannot exceed exploration_payoff_score")
        markers = candidate.get("paper_relevance_markers", [])
        marker_dims = {marker.get("dimension") for marker in markers if isinstance(marker, dict)}
        if marker_dims != expected_dims:
            fail(f"{context} needs exact paper relevance marker dimensions")
        for marker in markers:
            if marker.get("status") not in {"absent", "weak", "adequate", "strong", "paper_ready"}:
                fail(f"{context} marker {marker.get('dimension')} has invalid status")
            if not isinstance(marker.get("score"), int) or not 0 <= marker.get("score") <= 5:
                fail(f"{context} marker {marker.get('dimension')} has invalid score")
            for field in ["criterion", "problem_space_specificity", "evidence"]:
                if not marker.get(field):
                    fail(f"{context} marker {marker.get('dimension')} missing {field}")
        relevance = candidate.get("good_enough_paper_relevance", {})
        for field in [
            "status",
            "average_marker_score",
            "decisive_dimensions_strong",
            "all_dimensions_adequate",
            "all_hard_gates_ready",
            "missing_for_good_enough_paper",
            "paper_relevance_decision",
        ]:
            if field not in relevance:
                fail(f"{context} good_enough_paper_relevance missing {field}")
        if relevance.get("status") not in {
            "paper_relevance_ready",
            "strong_relevance_certification_pending",
            "moderate_relevance_needs_sharpening",
            "weak_relevance",
        }:
            fail(f"{context} invalid paper relevance status")
        if relevance.get("status") == "paper_relevance_ready" and candidate.get("stepping_stone_maturity") != "publishable_handoff_ready":
            fail(f"{context} paper relevance ready requires publishable handoff maturity")
        for dimension in [
            "conceptual_novelty",
            "explanatory_power",
            "implications",
            "certification_readiness",
            "target_relevance",
        ]:
            if dimension not in candidate["scores"]:
                fail(f"{context} missing score dimension {dimension}")
        if not set(CONTRIBUTION_SKILLS).issubset(set(candidate.get("required_skills", []))):
            fail(f"{context} must require all contribution skills")
        gates = candidate.get("handoff_hard_gates", {})
        for gate in ["claim_statement_ready", "evidence_ready", "novelty_boundary_ready", "validation_ready", "overclaim_boundary_ready"]:
            if gate not in gates:
                fail(f"{context} missing hard gate {gate}")
            packet = gates[gate]
            if not isinstance(packet, dict) or "ready" not in packet or "finite_task" not in packet or not clean_text(packet.get("evidence")):
                fail(f"{context} hard gate {gate} lacks ready/finite_task/evidence")
        if candidate["stepping_stone_maturity"] == "publishable_handoff_ready" and not all(packet.get("ready") for packet in gates.values()):
            fail(f"{context} publishable maturity requires all hard gates ready")
        prior = candidate.get("prior_art_boundary", {})
        for field in ["closest_known_results", "what_is_reused", "what_is_new_if_true", "rediscovery_risk", "citation_tasks", "novelty_status"]:
            if not prior.get(field):
                fail(f"{context} prior_art_boundary missing {field}")
        if candidate["stepping_stone_maturity"] == "publishable_handoff_ready" and prior.get("novelty_status") != "checked":
            fail(f"{context} publishable maturity requires checked prior art")
        disqualifiers = candidate.get("disqualifier_tests", [])
        if not isinstance(disqualifiers, list) or len(disqualifiers) < 5:
            fail(f"{context} needs disqualifier tests")
        for row in disqualifiers:
            if row.get("verdict") not in {"pass", "fail", "unknown", "finite_check_queued"} or not row.get("name") or not row.get("evidence"):
                fail(f"{context} malformed disqualifier test")
        shape = candidate.get("paper_note_shape", {})
        for field in ["title", "abstract_claim", "theorem_or_result_statement", "definitions_needed", "proof_plan", "relation_to_main_problem", "limitations", "next_validation_artifacts"]:
            if not shape.get(field):
                fail(f"{context} paper_note_shape missing {field}")
        if "pipeline" in clean_text(shape).lower() or "marathon" in clean_text(shape).lower():
            fail(f"{context} paper_note_shape leaks pipeline language")
        if len(candidate.get("good_enough_when", [])) < 4:
            fail(f"{context} needs explicit good-enough criteria")
        if len(candidate.get("continue_only_if", [])) < 3:
            fail(f"{context} needs continue-only-if criteria")
        if len(candidate.get("stop_when", [])) < 3:
            fail(f"{context} needs stop criteria")
        if "does not prove the main target" not in clean_text(candidate.get("overclaim_boundary")).lower():
            fail(f"{context} overclaim boundary must protect the main target")
        implication = candidate.get("implication_map", {})
        for field in ["immediate_next_analysis", "route_level", "paper_level"]:
            require_text(implication, field, f"{context} implication_map")
        if not OUT_MD.exists():
            fail(f"missing {rel(OUT_MD)}")
    text = OUT_MD.read_text(encoding="utf-8")
    for phrase in [
        "Scientific Contribution Monitor",
        "Good-enough definition",
        "Anti-infinite progression rule",
        "Stepping-Stone Maturity Levels",
        "Hard Gates",
        "Disqualifiers",
        "Prior-Art Boundary",
        "Paper Relevance Markers",
        "Candidate Queue",
    ]:
        if phrase not in text:
            fail(f"{rel(OUT_MD)} missing `{phrase}`")
    if report.get("target_id") == "p-vs-np-target":
        signals = report.get("novelty_high_reward_signals", [])
        if not isinstance(signals, list) or len(signals) < 3:
            fail(f"{rel(OUT_JSON)} P vs NP monitor needs novelty/high-reward signals")
        joined = clean_text(report).lower()
        for phrase in ["mcsp", "certificate", "lower bound", "advice", "pivot", "conceptual_depth", "unblocking_power"]:
            if phrase not in joined:
                fail(f"{rel(OUT_JSON)} P vs NP monitor lacks `{phrase}`")
        for forbidden in ["wilson", "yang-mills", "reflection positivity", "mass gap"]:
            if forbidden in joined:
                fail(f"{rel(OUT_JSON)} P vs NP monitor contains cross-target term `{forbidden}`")
    print(f"validated {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
