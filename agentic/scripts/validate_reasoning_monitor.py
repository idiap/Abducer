#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Validate the reasoning monitor packet and self-contained HTML report."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel
from abstraction_machinery_selection import validate_machinery_shape
from formal_subgoal_control import DECISIONS as CONTROL_DECISIONS
from formal_subgoal_control import validate_control_shape


SCHEMA = ROOT / "agentic/spec/reasoning_monitor_packet.schema.json"
PACKET = ROOT / "agentic/reports/reasoning_monitor/latest.json"
HTML = ROOT / "agentic/reports/reasoning_monitor/latest.html"
CURRENT_TARGET = ROOT / "agentic/state/current_target.json"
SECTION_TABS = ["overview", "timeline", "frontier", "candidates", "strategy", "milestones", "reorientation", "subgoals", "machinery", "stretch", "marathon", "qualitative", "debt", "evidence", "drift"]
YANG_MILLS_TARGET = "yang-mills-existence-and-mass-gap-target"
GENERIC_STRATEGY_PHRASES = [
    "factor the opaque obligation",
    "smaller lemmas, evidence tasks, or discovery branches",
]
YANG_MILLS_ROUTE_MARKERS = [
    "yang-mills",
    "yang mills",
    "balaban",
    "renormalisation",
    "renormalization",
    "schwinger",
    "wightman",
    "reflection positivity",
    "transfer matrix",
    "mass-gap",
    "mass gap",
    "spectral",
    "hamiltonian",
    "continuum",
    "gauge",
    "correlator",
]
STORY_REQUIRED_MARKERS = [
    "first we tried",
    "did not pay off",
    "then we moved",
    "hamiltonian",
    "os/wightman",
    "schwinger",
    "gauge-invariant",
    "cutoff",
    "continuum",
    "spectral",
    "balaban",
    "correlator",
    "learned",
    "learning",
    "contradiction",
    "negated",
    "gauge-field",
    "observable algebra",
    "spectral measure",
    "continuum limit",
    "same-theory transfer",
]
PHYSICS_EXPLANATION_MARKERS = [
    "dynamical object",
    "scale story",
    "observables",
    "kinematics",
    "spectral meaning",
    "failure physically",
]


def require_fields(payload: dict[str, Any], fields: list[str], subject: str, path: Path) -> None:
    for field in fields:
        if field not in payload:
            fail(f"{rel(path)} {subject} missing `{field}`")


def validate_packet() -> dict[str, Any]:
    schema = load_json_object(SCHEMA)
    packet = load_json_object(PACKET)
    require_fields(packet, schema["required_fields"], "packet", PACKET)
    target = packet["target"]
    if not isinstance(target, dict):
        fail(f"{rel(PACKET)} target must be an object")
    require_fields(target, schema["target_required_fields"], "target", PACKET)
    current = load_json_object(CURRENT_TARGET)
    if target["target_id"] != current.get("target_id"):
        fail(f"{rel(PACKET)} target_id {target['target_id']} does not match current target {current.get('target_id')}")
    if not packet.get("validation", {}).get("active_target_match"):
        fail(f"{rel(PACKET)} validation.active_target_match is false")
    if packet.get("stale_workflow", {}).get("critical_findings") != 0:
        fail(f"{rel(PACKET)} stale workflow critical findings must be zero")
    if not packet.get("reasoning_events", {}).get("events"):
        fail(f"{rel(PACKET)} requires reasoning events")
    if not packet.get("candidate_routes"):
        fail(f"{rel(PACKET)} requires candidate routes")
    if packet.get("frontier", {}).get("total", 0) <= 0:
        fail(f"{rel(PACKET)} frontier total must be positive for active Yang-Mills monitoring")
    story = packet.get("interpretative_strategy_story", {})
    if not isinstance(story, dict):
        fail(f"{rel(PACKET)} interpretative_strategy_story must be an object")
    beats = story.get("story_beats", [])
    if not isinstance(beats, list) or len(beats) < 4:
        fail(f"{rel(PACKET)} interpretative_strategy_story needs at least four story beats")
    story_text = clean_text(story).lower()
    for marker in STORY_REQUIRED_MARKERS:
        if marker not in story_text:
            fail(f"{rel(PACKET)} interpretative strategy story lacks `{marker}`")
    contract = story.get("physics_explanation_contract", [])
    if not isinstance(contract, list) or len(contract) < 6:
        fail(f"{rel(PACKET)} interpretative strategy story needs a physics_explanation_contract")
    contract_text = clean_text(contract).lower()
    for marker in PHYSICS_EXPLANATION_MARKERS:
        if marker not in contract_text:
            fail(f"{rel(PACKET)} physics explanation contract lacks `{marker}`")
    if story_text.count(".md") > 2 and "not route-index prose" not in story_text:
        fail(f"{rel(PACKET)} interpretative strategy story appears to be artifact references rather than physics narrative")
    for index, beat in enumerate(beats, start=1):
        if not isinstance(beat, dict):
            fail(f"{rel(PACKET)} story beat {index} must be an object")
        for field in ["phase", "headline", "tried", "physics_story", "decision", "moved_to"]:
            if not clean_text(beat.get(field)):
                fail(f"{rel(PACKET)} story beat {index} missing `{field}`")
        equations = beat.get("equations", [])
        if not isinstance(equations, list) or not equations:
            fail(f"{rel(PACKET)} story beat {index} needs rendered equation checkpoints")
        for equation in equations:
            if not isinstance(equation, dict) or not clean_text(equation.get("label")) or not clean_text(equation.get("display")):
                fail(f"{rel(PACKET)} story beat {index} has malformed equation checkpoint")
            if beat.get("phase") == "proof_by_contradiction_branching" and not clean_text(equation.get("valid_when")):
                fail(f"{rel(PACKET)} contradiction story beat equation {index} must state validity conditions")
        learning = beat.get("what_we_learned", [])
        if not isinstance(learning, list) or len(learning) < 2:
            fail(f"{rel(PACKET)} story beat {index} needs explicit learning notes")
        if not any("learn" in clean_text(item).lower() or "taught" in clean_text(item).lower() or "shifted" in clean_text(item).lower() for item in learning):
            fail(f"{rel(PACKET)} story beat {index} learning notes must explain what changed")
        if not beat.get("why_it_did_not_pay_off") and not beat.get("remaining_blockers") and not beat.get("why_this_is_the_next_goal"):
            fail(f"{rel(PACKET)} story beat {index} must explain non-payoff, blockers, or why the next move follows")
    if len(story.get("anti_drift_rules", [])) < 3:
        fail(f"{rel(PACKET)} interpretative strategy story needs anti-drift rules")
    milestones = packet.get("success_milestones", {})
    if not isinstance(milestones, dict):
        fail(f"{rel(PACKET)} success_milestones must be an object")
    milestone_items = milestones.get("items", [])
    if not isinstance(milestone_items, list) or len(milestone_items) < 5:
        fail(f"{rel(PACKET)} success_milestones needs at least five milestone items")
    milestone_text = clean_text(milestones).lower()
    for marker in ["big-deal", "potential breakthrough", "potentially achieved", "success signal", "certification", "disqualifier", "next action"]:
        if marker not in milestone_text:
            fail(f"{rel(PACKET)} success milestones lack `{marker}`")
    for index, milestone in enumerate(milestone_items, start=1):
        if not isinstance(milestone, dict):
            fail(f"{rel(PACKET)} success milestone {index} must be an object")
        for field in ["milestone_id", "label", "current_status", "why_big_deal", "potentially_achieved_when", "success_signal", "next_action"]:
            if not clean_text(milestone.get(field)):
                fail(f"{rel(PACKET)} success milestone {index} missing `{field}`")
        if len(milestone.get("certification_evidence", [])) < 2:
            fail(f"{rel(PACKET)} success milestone {index} needs certification evidence")
        if len(milestone.get("disqualifiers", [])) < 2:
            fail(f"{rel(PACKET)} success milestone {index} needs disqualifiers")
        if len(milestone.get("linked_commitments", [])) < 1:
            fail(f"{rel(PACKET)} success milestone {index} must link target commitments")
        equations = milestone.get("equations", [])
        if not isinstance(equations, list) or not equations:
            fail(f"{rel(PACKET)} success milestone {index} needs an equation checkpoint")
    machinery = packet.get("machinery_selection", {})
    if not isinstance(machinery, dict):
        fail(f"{rel(PACKET)} machinery_selection must be an object")
    machinery_text = clean_text(machinery).lower()
    for marker in ["machinery selection", "controlled interface", "invalid", "abstraction chain", "yang-mills", "construction", "transfer", "witness", "validation"]:
        if marker not in machinery_text:
            fail(f"{rel(PACKET)} machinery_selection lacks `{marker}`")
    items = machinery.get("items", [])
    if not isinstance(items, list) or not items:
        fail(f"{rel(PACKET)} machinery_selection needs active route items")
    for index, item in enumerate(items, start=1):
        ok, reason = validate_machinery_shape(item)
        if not ok:
            fail(f"{rel(PACKET)} machinery_selection item {index} invalid: {reason}")
        if "->" not in item.get("controlled_interface", ""):
            fail(f"{rel(PACKET)} machinery_selection item {index} needs a controlled-interface arrow")
    chain = machinery.get("abstraction_chain", {})
    if not isinstance(chain, dict):
        fail(f"{rel(PACKET)} machinery_selection.abstraction_chain must be an object")
    if len(chain.get("nodes", [])) < 6 or len(chain.get("bridge_obligations", [])) < 5:
        fail(f"{rel(PACKET)} abstraction chain needs ordered nodes and bridge obligations")
    for edge in chain.get("bridge_obligations", []):
        if not isinstance(edge, dict):
            fail(f"{rel(PACKET)} abstraction chain bridge obligations must be objects")
        for field in ["from", "to", "bridge_obligation", "assumptions", "output", "failure_mode", "validator_handoff"]:
            if not edge.get(field):
                fail(f"{rel(PACKET)} abstraction chain edge missing `{field}`")
    policy = packet.get("formal_subgoal_control_policy", {})
    if not isinstance(policy, dict):
        fail(f"{rel(PACKET)} formal_subgoal_control_policy must be an object")
    policy_text = clean_text(policy).lower()
    for marker in ["formal subgoal", "persist", "backtrack", "pivot", "quarantine", "stop", "repeated identical blockers"]:
        if marker not in policy_text:
            fail(f"{rel(PACKET)} formal subgoal control policy lacks `{marker}`")
    policy_raw = str(policy).lower()
    for decision in CONTROL_DECISIONS:
        if decision not in policy_raw and decision.replace("_", " ") not in policy_text:
            fail(f"{rel(PACKET)} formal subgoal control policy lacks decision `{decision}`")
    reorientation = packet.get("reorientation_control", {})
    if not isinstance(reorientation, dict):
        fail(f"{rel(PACKET)} reorientation_control must be an object")
    reorientation_text = clean_text(reorientation).lower()
    for marker in [
        "restrategize",
        "backtrack",
        "pivot",
        "quarantine",
        "current diagnosis",
        "current recommendation",
        "bounded reflection",
        "route-level",
        "forbidden shortcut",
        "same-theory",
        "yang-mills",
    ]:
        if marker not in reorientation_text:
            fail(f"{rel(PACKET)} reorientation control lacks `{marker}`")
    recommendation = reorientation.get("current_recommendation", {})
    if not isinstance(recommendation, dict):
        fail(f"{rel(PACKET)} reorientation_control.current_recommendation must be an object")
    for field in ["decision", "rationale", "backtrack_guard", "pivot_guard", "quarantine_guard"]:
        if not clean_text(recommendation.get(field)):
            fail(f"{rel(PACKET)} reorientation current recommendation missing `{field}`")
    contract = reorientation.get("bounded_reflection_contract", {})
    if not isinstance(contract, dict):
        fail(f"{rel(PACKET)} reorientation bounded_reflection_contract must be an object")
    if int(contract.get("max_reflection_passes_before_action", 0)) <= 0:
        fail(f"{rel(PACKET)} reorientation contract needs positive max_reflection_passes_before_action")
    if len(contract.get("required_output_per_pass", [])) < 2:
        fail(f"{rel(PACKET)} reorientation contract needs required outputs")
    if len(contract.get("stop_reflecting_when", [])) < 2:
        fail(f"{rel(PACKET)} reorientation contract needs stop conditions")
    modes = reorientation.get("reorientation_modes", [])
    if not isinstance(modes, list) or len(modes) < 4:
        fail(f"{rel(PACKET)} reorientation_control needs at least four reorientation modes")
    for index, mode in enumerate(modes, start=1):
        if not isinstance(mode, dict):
            fail(f"{rel(PACKET)} reorientation mode {index} must be an object")
        for field in ["mode", "deep_meaning", "yang_mills_use", "trigger", "allowed_action", "forbidden_shortcut"]:
            if not clean_text(mode.get(field)):
                fail(f"{rel(PACKET)} reorientation mode {index} missing `{field}`")
    decision_points = reorientation.get("decision_points", [])
    if not isinstance(decision_points, list) or len(decision_points) < 3:
        fail(f"{rel(PACKET)} reorientation_control needs decision checkpoints")
    for index, point in enumerate(decision_points, start=1):
        if not isinstance(point, dict):
            fail(f"{rel(PACKET)} reorientation decision point {index} must be an object")
        for field in ["checkpoint", "if_progress", "if_stalls", "backtrack_if", "pivot_if", "next_experiment"]:
            if not clean_text(point.get(field)):
                fail(f"{rel(PACKET)} reorientation decision point {index} missing `{field}`")
    route_assessments = reorientation.get("route_assessments", [])
    if not isinstance(route_assessments, list) or not route_assessments:
        fail(f"{rel(PACKET)} reorientation_control needs route-level assessments")
    for index, assessment in enumerate(route_assessments, start=1):
        if not isinstance(assessment, dict):
            fail(f"{rel(PACKET)} route-level assessment {index} must be an object")
        for field in ["candidate_id", "route_family", "recommended_move", "obstruction_type", "current_read", "backtrack_trigger", "pivot_trigger", "next_probe"]:
            if not clean_text(assessment.get(field)):
                fail(f"{rel(PACKET)} route-level assessment {index} missing `{field}`")
        ok, reason = validate_control_shape(assessment.get("subgoal_control"))
        if not ok:
            fail(f"{rel(PACKET)} route-level assessment {index} invalid subgoal_control: {reason}")
        if not clean_text(assessment.get("formal_control_decision")):
            fail(f"{rel(PACKET)} route-level assessment {index} missing formal_control_decision")
        if len(assessment.get("protected_commitments", [])) < 1:
            fail(f"{rel(PACKET)} route-level assessment {index} must protect commitments")
    pivot_watchlist = reorientation.get("pivot_watchlist", [])
    if not isinstance(pivot_watchlist, list):
        fail(f"{rel(PACKET)} reorientation_control pivot_watchlist must be a list")
    for index, candidate in enumerate(pivot_watchlist, start=1):
        if not isinstance(candidate, dict):
            fail(f"{rel(PACKET)} pivot watchlist entry {index} must be an object")
        for field in ["candidate_id", "why_not_proof_queue_now", "promotion_condition"]:
            if not clean_text(candidate.get(field)):
                fail(f"{rel(PACKET)} pivot watchlist entry {index} missing `{field}`")
    queue = reorientation.get("active_reorientation_queue", [])
    if not isinstance(queue, list) or len(queue) < 3:
        fail(f"{rel(PACKET)} reorientation_control needs an active reorientation queue")
    for index, action in enumerate(queue, start=1):
        if not isinstance(action, dict):
            fail(f"{rel(PACKET)} reorientation action {index} must be an object")
        for field in ["action_id", "mode", "priority", "action", "why_now", "success_condition"]:
            if not clean_text(action.get(field)):
                fail(f"{rel(PACKET)} reorientation action {index} missing `{field}`")
    contradiction = packet.get("contradiction_routes", {})
    if not isinstance(contradiction, dict):
        fail(f"{rel(PACKET)} contradiction_routes must be an object")
    branches = contradiction.get("items", [])
    if not isinstance(branches, list) or len(branches) < 3:
        fail(f"{rel(PACKET)} contradiction_routes needs at least three active branches")
    contradiction_text = clean_text(contradiction).lower()
    for marker in ["proof-by-contradiction", "exact", "negation", "no-gap", "os", "triviality", "spectral", "reflection", "cumulant", "same-theory"]:
        if marker not in contradiction_text:
            fail(f"{rel(PACKET)} contradiction_routes lacks `{marker}`")
    for index, branch in enumerate(branches, start=1):
        if not isinstance(branch, dict):
            fail(f"{rel(PACKET)} contradiction branch {index} must be an object")
        for field in [
            "branch_id",
            "strategy",
            "exact_negation",
            "contradiction_carrier",
            "derived_consequence",
            "conflict_target",
            "computed_verdict",
            "mathematical_learning",
            "same_theory_invariant",
        ]:
            if not clean_text(branch.get(field)):
                fail(f"{rel(PACKET)} contradiction branch {index} missing `{field}`")
        for field in ["preserved_commitments", "proof_obligations", "failure_modes", "equation_checkpoints"]:
            if not isinstance(branch.get(field), list) or not branch[field]:
                fail(f"{rel(PACKET)} contradiction branch {index} needs non-empty `{field}`")
        for equation in branch["equation_checkpoints"]:
            if not isinstance(equation, dict) or not clean_text(equation.get("valid_when")):
                fail(f"{rel(PACKET)} contradiction branch {index} equation checkpoints need validity conditions")
    validation_summary = contradiction.get("validation_summary", {})
    if int(validation_summary.get("active_promotable_routes", 0)) < 3:
        fail(f"{rel(PACKET)} contradiction validation summary should show active promotable routes")
    empirical = packet.get("empirical_evidence_requests", {})
    if not isinstance(empirical, dict):
        fail(f"{rel(PACKET)} empirical_evidence_requests must be an object")
    empirical_items = empirical.get("items", [])
    if not isinstance(empirical_items, list) or len(empirical_items) < 4:
        fail(f"{rel(PACKET)} empirical_evidence_requests needs at least four evidence requests")
    empirical_text = clean_text(empirical).lower()
    for marker in ["empirical", "lattice", "numerical", "simulation", "theoretical", "transfer gap", "proof boundary", "gauge", "continuum"]:
        if marker not in empirical_text:
            fail(f"{rel(PACKET)} empirical evidence requests lack `{marker}`")
    for index, item in enumerate(empirical_items, start=1):
        if not isinstance(item, dict):
            fail(f"{rel(PACKET)} empirical evidence request {index} must be an object")
        for field in ["request_id", "linked_theoretical_step", "evidence_mode", "empirical_question", "observable_or_quantity", "proximity_class", "transfer_gap", "proof_boundary", "integration_action"]:
            if not clean_text(item.get(field)):
                fail(f"{rel(PACKET)} empirical evidence request {index} missing `{field}`")
        for field in ["search_plan", "support_criteria", "refutation_criteria", "demotion_triggers", "skill_triggers"]:
            if not isinstance(item.get(field), list) or not item[field]:
                fail(f"{rel(PACKET)} empirical evidence request {index} needs non-empty `{field}`")
        if "proof" not in item["proof_boundary"].lower():
            fail(f"{rel(PACKET)} empirical evidence request {index} must state proof boundary")
    stretch = packet.get("discovery_stretch", {})
    if not isinstance(stretch, dict):
        fail(f"{rel(PACKET)} discovery_stretch must be an object")
    if stretch.get("quality_gate") != "pass":
        fail(f"{rel(PACKET)} discovery_stretch quality gate must be pass")
    stretch_text = clean_text(stretch).lower()
    for marker in ["large-stretch", "discovery", "controlled interface", "falsifiers", "promotion signal", "pivot signal", "yang-mills", "spectral", "observable"]:
        if marker not in stretch_text:
            fail(f"{rel(PACKET)} discovery_stretch lacks `{marker}`")
    programs = stretch.get("programs", [])
    if not isinstance(programs, list) or len(programs) < 6:
        fail(f"{rel(PACKET)} discovery_stretch needs at least six programs")
    for index, program in enumerate(programs, start=1):
        if not isinstance(program, dict):
            fail(f"{rel(PACKET)} discovery stretch program {index} must be an object")
        for field in ["program_id", "title", "machinery_role", "hypothesis", "mathematical_mechanism", "controlled_interface", "equations", "falsifiers", "next_experiments", "promotion_signal", "pivot_signal"]:
            if not program.get(field):
                fail(f"{rel(PACKET)} discovery stretch program {index} missing `{field}`")
        if "->" not in program["controlled_interface"]:
            fail(f"{rel(PACKET)} discovery stretch program {index} needs controlled-interface arrow")
        if len(program.get("equations", [])) < 2:
            fail(f"{rel(PACKET)} discovery stretch program {index} needs equations")
        if len(program.get("falsifiers", [])) < 3:
            fail(f"{rel(PACKET)} discovery stretch program {index} needs falsifiers")
    marathon = packet.get("discovery_marathon", {})
    if not isinstance(marathon, dict):
        fail(f"{rel(PACKET)} discovery_marathon must be an object")
    marathon_text = clean_text(marathon).lower()
    for marker in ["discovery marathon", "long-horizon", "branch memory", "skill-dispatch", "what actually changed"]:
        if marker not in marathon_text:
            fail(f"{rel(PACKET)} discovery_marathon lacks `{marker}`")
    if marathon.get("status") != "no_active_run":
        if int(marathon.get("cycle_count", 0)) < 1:
            fail(f"{rel(PACKET)} active discovery_marathon must have at least one persisted cycle packet")
        if "research_cycle_count" not in marathon or "synthetic_cycle_count" not in marathon:
            fail(f"{rel(PACKET)} discovery_marathon must distinguish research and synthetic cycle counts")
        if not marathon.get("branch_summaries"):
            fail(f"{rel(PACKET)} active discovery_marathon needs branch_summaries")
        if not marathon.get("cycle_summaries"):
            fail(f"{rel(PACKET)} active discovery_marathon needs cycle_summaries")
        for index, branch in enumerate(marathon.get("branch_summaries", []), start=1):
            for field in ["branch_id", "title", "controlled_interface", "latest_learning", "next_experiment"]:
                if not clean_text(branch.get(field)):
                    fail(f"{rel(PACKET)} discovery_marathon branch {index} missing `{field}`")
        if "no_breakthrough_claimed" not in marathon_text:
            fail(f"{rel(PACKET)} discovery_marathon must avoid unsupported breakthrough claims")
    qualitative = packet.get("qualitative_mechanistic_graph", {})
    if not isinstance(qualitative, dict):
        fail(f"{rel(PACKET)} qualitative_mechanistic_graph must be an object")
    qualitative_text = clean_text(qualitative).lower()
    for marker in ["qualitative", "mechanistic", "relation", "epistemic_status"]:
        if marker not in qualitative_text:
            fail(f"{rel(PACKET)} qualitative_mechanistic_graph lacks `{marker}`")
    summary = qualitative.get("summary", {})
    if int(summary.get("node_count", 0)) < 5:
        fail(f"{rel(PACKET)} qualitative_mechanistic_graph needs at least five nodes")
    if int(summary.get("edge_count", 0)) < 4:
        fail(f"{rel(PACKET)} qualitative_mechanistic_graph needs at least four relation edges")
    for index, edge in enumerate(qualitative.get("edges", []), start=1):
        for field in ["source", "target", "edge_type", "direction", "validity_regime", "assumptions", "failure_modes", "evidence_paths", "epistemic_status"]:
            if not edge.get(field):
                fail(f"{rel(PACKET)} qualitative edge {index} missing `{field}`")
    is_yang_mills = target["target_id"] == YANG_MILLS_TARGET
    for index, route in enumerate(packet["candidate_routes"], start=1):
        if not isinstance(route, dict):
            fail(f"{rel(PACKET)} candidate route {index} must be an object")
        require_fields(route, schema["candidate_required_fields"], f"candidate route {index}", PACKET)
        ok, reason = validate_control_shape(route.get("subgoal_control"))
        if not ok:
            fail(f"{rel(PACKET)} candidate route {index} invalid subgoal_control: {reason}")
        ok, reason = validate_machinery_shape(route.get("machinery_selection"))
        if not ok:
            fail(f"{rel(PACKET)} candidate route {index} invalid machinery_selection: {reason}")
        if route["route_disposition"] == "proof_queue" and route["subgoal_control"]["decision"] != "persist_adapt":
            fail(f"{rel(PACKET)} proof-queue route {index} must have persist_adapt subgoal control")
        route_text = clean_text(route.get("proposed_transformation", "")).lower()
        if any(phrase in route_text for phrase in GENERIC_STRATEGY_PHRASES):
            fail(f"{rel(PACKET)} candidate route {index} uses stale generic strategy language")
        if any(str(obligation.get("requirement", "")).startswith("Discharge `") for obligation in route.get("obligations", [])):
            fail(f"{rel(PACKET)} candidate route {index} has generic obligations")
        if is_yang_mills:
            family = route.get("route_blueprint", {}).get("route_family")
            if not family:
                fail(f"{rel(PACKET)} Yang-Mills candidate route {index} lacks a route family")
            if not any(marker in route_text for marker in YANG_MILLS_ROUTE_MARKERS):
                fail(f"{rel(PACKET)} Yang-Mills candidate route {index} lacks domain-specific strategy language")
    for index, item in enumerate(packet.get("frontier", {}).get("items", []), start=1):
        if not isinstance(item, dict):
            fail(f"{rel(PACKET)} frontier item {index} must be an object")
        require_fields(item, schema["frontier_required_fields"], f"frontier item {index}", PACKET)
    missing = packet.get("evidence_ledger", {}).get("missing", [])
    if missing:
        fail(f"{rel(PACKET)} has missing evidence ledger entries: {missing[:3]}")
    return packet


def embedded_packet(text: str) -> dict[str, Any]:
    match = re.search(r'<script id="monitor-data" type="application/json">(.*?)</script>', text, re.DOTALL)
    if not match:
        fail(f"{rel(HTML)} missing embedded monitor-data JSON")
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        fail(f"{rel(HTML)} embedded monitor-data is invalid JSON: {exc}")


def validate_html(packet: dict[str, Any]) -> None:
    if not HTML.exists():
        fail(f"missing HTML report: {rel(HTML)}")
    text = HTML.read_text(encoding="utf-8")
    lower = text.lower()
    forbidden = ["<script src=", "<link ", "http://", "https://", "@import", "<img "]
    found = [item for item in forbidden if item in lower]
    if found:
        fail(f"{rel(HTML)} contains external or non-embedded asset references: {found}")
    embedded = embedded_packet(text)
    if embedded.get("target", {}).get("target_id") != packet["target"]["target_id"]:
        fail(f"{rel(HTML)} embedded target does not match packet target")
    if embedded.get("reasoning_events", {}).get("event_count") != packet.get("reasoning_events", {}).get("event_count"):
        fail(f"{rel(HTML)} embedded event count does not match packet")
    for tab in SECTION_TABS:
        if f'data-tab="{tab}"' not in text:
            fail(f"{rel(HTML)} missing tab control `{tab}`")
    for required_id in ["targetId", "goal", "metrics", "query", "laneFilter", "statusFilter", "commitmentFilter", "evidenceFilter", "view"]:
        if f'id="{required_id}"' not in text:
            fail(f"{rel(HTML)} missing DOM id `{required_id}`")
    for phrase in [
        "Proof Debt",
        "Evidence",
        "Drift",
        "Target Spine",
        "Strategy Story",
        "What Counts As A Physics Explanation",
        "Underlying mathematics",
        "Physics mechanism",
        "Anti-Drift Rules",
        "Success Milestones",
        "Potentially Achieved When",
        "Certification Evidence",
        "Disqualifiers",
        "Reorientation Control",
        "Formal Subgoal Control",
        "Machinery Selection",
        "Large-Stretch Discovery Exploration",
        "Discovery Marathon",
        "What Actually Changed",
        "Branch Learning",
        "Cycle Learning",
        "Deep Reviews",
        "Discovery Programs",
        "Falsifiers",
        "Promotion Signal",
        "Pivot Signal",
        "Universal Machinery Roles",
        "Controlled Interface",
        "Invalid Use Modes",
        "Yang-Mills Example Alignment",
        "Abstraction Chain",
        "Persist Or Adapt",
        "Learning From Failure",
        "Backtrack Trigger",
        "Pivot Trigger",
        "Quarantine Trigger",
        "Stop Condition",
        "Current Diagnosis",
        "Current Recommendation",
        "Bounded Reflection Contract",
        "Route-Level Diagnosis",
        "Decision Checkpoints",
        "Forbidden Shortcut",
        "Proof By Contradiction Branches",
        "Exact negation",
        "Contradiction carrier",
        "What failure would teach",
        "Same-theory invariant",
        "Closely Related Empirical Evidence",
        "Linked Theoretical Step",
        "Empirical Question",
        "Transfer Gap",
        "Proof Boundary",
    ]:
        if phrase not in text:
            fail(f"{rel(HTML)} missing visible section phrase `{phrase}`")
    if len(clean_text(text)) < 5000:
        fail(f"{rel(HTML)} appears too small to be the full dynamic report")


def main() -> int:
    packet = validate_packet()
    validate_html(packet)
    print(f"validated reasoning monitor for {packet['target']['target_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
