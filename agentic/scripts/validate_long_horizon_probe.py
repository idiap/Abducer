#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Validate the latest long-horizon Yang-Mills probe report."""

from __future__ import annotations

from agentic_common import ROOT, fail, load_json_object, rel
from abstraction_machinery_selection import validate_machinery_shape
from formal_subgoal_control import validate_control_shape


REPORT = ROOT / "agentic/reports/long_horizon/latest.json"
CURRENT_TARGET = ROOT / "agentic/state/current_target.json"
YANG_MILLS_TARGET = "yang-mills-existence-and-mass-gap-target"


def main() -> int:
    report = load_json_object(REPORT)
    current = load_json_object(CURRENT_TARGET)
    if report.get("target_id") != current.get("target_id"):
        fail(f"{rel(REPORT)} target {report.get('target_id')} does not match active target {current.get('target_id')}")
    if report.get("quality_gate") != "pass":
        fail(f"{rel(REPORT)} quality gate is {report.get('quality_gate')}")
    if report.get("critical_findings") != 0:
        fail(f"{rel(REPORT)} has critical findings")
    metrics = report.get("metrics", {})
    if metrics.get("proof_queue_count", 0) <= 0:
        fail(f"{rel(REPORT)} has no active proof-queue routes")
    if metrics.get("proof_queue_count", 0) > metrics.get("proof_queue_budget", 0):
        fail(f"{rel(REPORT)} exceeds proof queue budget")
    formal = report.get("formal_subgoal_control", {})
    summary = formal.get("summary", {})
    if not formal or not formal.get("active_controls"):
        fail(f"{rel(REPORT)} lacks formal subgoal control state")
    if summary.get("active_control_count", 0) != len(formal.get("active_controls", [])):
        fail(f"{rel(REPORT)} formal subgoal control count mismatch")
    if summary.get("stale_repeated_blockers"):
        fail(f"{rel(REPORT)} has stale repeated blockers without action")
    decisions = summary.get("decision_counts", {})
    if decisions.get("persist_adapt", 0) < metrics.get("proof_queue_count", 0):
        fail(f"{rel(REPORT)} active proof routes are not covered by persist_adapt controls")
    machinery = report.get("machinery_portfolio", {})
    if not isinstance(machinery, dict) or not machinery.get("active_selections"):
        fail(f"{rel(REPORT)} lacks machinery_portfolio active selections")
    machinery_summary = machinery.get("summary", {})
    if machinery_summary.get("selection_count", 0) < metrics.get("candidate_routes", 0):
        fail(f"{rel(REPORT)} machinery portfolio does not cover all routes")
    for marker in ["construction", "transfer", "witness", "validation"]:
        if marker not in str(machinery).lower():
            fail(f"{rel(REPORT)} machinery portfolio lacks `{marker}`")
    coverage = report.get("commitment_coverage", {})
    if coverage.get("missing"):
        fail(f"{rel(REPORT)} missing commitment coverage: {coverage['missing']}")
    skill_coherence = report.get("skill_ecosystem_coherence", {})
    if skill_coherence.get("status") != "pass":
        fail(f"{rel(REPORT)} skill ecosystem coherence is {skill_coherence.get('status')}")
    if skill_coherence.get("critical_findings") != 0:
        fail(f"{rel(REPORT)} skill ecosystem coherence has critical findings")
    metrics = skill_coherence.get("metrics", {})
    if metrics.get("projected_skill_count", 0) < metrics.get("direct_workflow_skill_count", 0):
        fail(f"{rel(REPORT)} skill coherence has more direct skills than projected skills")
    phase_coverage = skill_coherence.get("phase_coverage", [])
    phases = {phase.get("phase"): phase for phase in phase_coverage if isinstance(phase, dict)}
    for phase_name in ["target_navigation", "conceptual_refinement", "conditional_pools"]:
        if phase_name not in phases:
            fail(f"{rel(REPORT)} skill coherence missing phase {phase_name}")
    for phase_name in ["target_navigation", "conceptual_refinement"]:
        if phases[phase_name].get("status") != "role-complete":
            fail(f"{rel(REPORT)} skill coherence phase {phase_name} is not role-complete")
        if len(phases[phase_name].get("composed_skills", [])) < 5:
            fail(f"{rel(REPORT)} skill coherence phase {phase_name} has too few composed skills")
    conditional = phases["conditional_pools"]
    for pool in ["review_pool", "ingest_pool", "reporting_pool"]:
        if not conditional.get(pool):
            fail(f"{rel(REPORT)} skill coherence conditional pool {pool} is empty")
    policy = skill_coherence.get("policy", "").lower()
    for marker in ["phase-complete", "conditional", "control-plane", "discovery", "review"]:
        if marker not in policy:
            fail(f"{rel(REPORT)} skill coherence policy lacks {marker}")
    is_yang_mills = report.get("target_id") == YANG_MILLS_TARGET
    for route in report.get("active_proof_queue", []):
        text = route.get("transformation", "").lower()
        if "factor the opaque obligation" in text or "smaller lemmas, evidence tasks, or discovery branches" in text:
            fail(f"{rel(REPORT)} proof route {route.get('candidate_id')} uses generic strategy language")
        if route.get("target_relevance_score", 0) < 0.8:
            fail(f"{rel(REPORT)} proof route {route.get('candidate_id')} has weak target relevance")
        if is_yang_mills and len(route.get("domain_terms", [])) < 3:
            fail(f"{rel(REPORT)} proof route {route.get('candidate_id')} is not content-specific enough")
        route_physics = f"{route.get('physics_story', '')} {route.get('physical_failure_mode', '')}".lower()
        for marker in ["gauge", "continuum", "observable", "spectral"]:
            if is_yang_mills and marker not in route_physics:
                fail(f"{rel(REPORT)} proof route {route.get('candidate_id')} lacks physics-facing marker `{marker}`")
        if not route.get("obligations"):
            fail(f"{rel(REPORT)} proof route {route.get('candidate_id')} lacks obligations")
        ok, reason = validate_control_shape(route.get("subgoal_control"))
        if not ok:
            fail(f"{rel(REPORT)} proof route {route.get('candidate_id')} invalid subgoal_control: {reason}")
        if route["subgoal_control"]["decision"] != "persist_adapt":
            fail(f"{rel(REPORT)} proof route {route.get('candidate_id')} is active without persist_adapt control")
        for marker in ["learning", "next", "backtrack", "pivot", "quarantine", "stop"]:
            if marker not in str(route["subgoal_control"]).lower():
                fail(f"{rel(REPORT)} proof route {route.get('candidate_id')} subgoal control lacks {marker}")
        if any(obligation.startswith("Discharge `") for obligation in route.get("obligations", [])):
            fail(f"{rel(REPORT)} proof route {route.get('candidate_id')} has generic obligations")
        ok, reason = validate_machinery_shape(route.get("machinery_selection"))
        if not ok:
            fail(f"{rel(REPORT)} proof route {route.get('candidate_id')} invalid machinery_selection: {reason}")
        if route["machinery_selection"].get("machinery_role") == "obstruction":
            fail(f"{rel(REPORT)} proof route {route.get('candidate_id')} uses obstruction machinery")
        for marker in ["controlled_interface", "required_bridge_obligation", "invalid_use_modes"]:
            if marker not in route["machinery_selection"]:
                fail(f"{rel(REPORT)} proof route {route.get('candidate_id')} machinery_selection lacks {marker}")
    print(f"validated long-horizon probe for {report['target_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
