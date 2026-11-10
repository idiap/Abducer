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
"""Select discovery-marathon branches without letting the run drift."""

from __future__ import annotations

import argparse
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json
from artifact_or_stop_control import artifact_or_stop_hint_for_branch
from avenue_literature_gap import classify_branch_avenue, warrant_for_branch, warrant_summary
from discovery_marathon_common import dump_stdout, load_active_pointer, load_branches, load_run_state


PVSNP_PRESSURE_FAMILIES = [
    (
        "hardness_magnification_threshold",
        ["magnification", "barely", "weak lower bound", "threshold", "beta", "exponent", "window"],
    ),
    (
        "barrier_and_impossibility_control",
        ["barrier", "relativization", "natural", "algebrization", "oracle", "no-go", "impossibility"],
    ),
    (
        "meta_complexity_carrier",
        ["mcsp", "mktp", "meta-complexity", "carrier", "certificate", "explicitness"],
    ),
    (
        "proof_complexity_transfer",
        ["proof complexity", "resolution", "frege", "lower-bound", "lower bound", "pigeonhole", "tautology"],
    ),
    (
        "quantifier_uniformity_lift",
        ["all-exponent", "cofinal", "uniformity", "nonuniform", "p/poly", "advice", "padding"],
    ),
    (
        "gedanken_case_lab",
        ["gedanken", "toy", "case", "example", "concrete", "oracle substitution", "finite"],
    ),
]


PVSNP_FAMILY_CONTROL = {
    "hardness_magnification_threshold": {
        "novelty_signal": "Exact beta/q/a transfer calculus replaces broad magnification optimism with a computable threshold.",
        "high_reward_payoff": "A single calculation can show whether the route reaches all exponents or only a bounded SAT exponent window.",
        "pivot_criteria": "Pivot or convert to a no-go if beta>0 or q consumes the source margin for two named carriers.",
    },
    "barrier_and_impossibility_control": {
        "novelty_signal": "The branch identifies which formal barrier premise applies or fails for the actual proof object.",
        "high_reward_payoff": "A route-specific impossibility theorem can eliminate a method family while preserving escape conditions.",
        "pivot_criteria": "Backtrack if the branch only cites natural proofs, relativization, or algebrization without a new controlled interface.",
    },
    "meta_complexity_carrier": {
        "novelty_signal": "Searchable MCSP/MKtP certificates replace advice-selected hard truth tables as the carrier.",
        "high_reward_payoff": "Compact searchable certificates could produce uniform lower-bound evidence without nonuniform hard-string choice.",
        "pivot_criteria": "Backtrack if certificate existence is target-equivalent, unsearchable in the needed time, or advice-dependent.",
    },
    "proof_complexity_transfer": {
        "novelty_signal": "A proof-system object mediates between semantic lower bounds and verifiable evidence.",
        "high_reward_payoff": "The branch can become a proof-complexity bridge or a no-go showing the proof object merely renames the lower-bound target.",
        "pivot_criteria": "Pivot to impossibility if proof length, verifier overhead, or semantic soundness is already as hard as the target lower bound.",
    },
    "quantifier_uniformity_lift": {
        "novelty_signal": "A cofinal all-exponent family is separated from a single bounded-window magnification result.",
        "high_reward_payoff": "This decides whether a route can affect NP not subset P/poly rather than one fixed exponent.",
        "pivot_criteria": "Quarantine if the family repeats the same bounded window or changes advice/uniformity with the exponent.",
    },
    "gedanken_case_lab": {
        "novelty_signal": "A small complexity world isolates one mechanism such as oracle substitution, advice leakage, or naturalness.",
        "high_reward_payoff": "A concrete case can expose the next formal obstruction or bridge variable before spending API cycles.",
        "pivot_criteria": "Stop if the case has no transfer lesson, no falsifier, or no follow-up bridge calculation.",
    },
    "unclassified_pvsnp_pressure": {
        "novelty_signal": "The branch must first name its complexity-theoretic pressure family.",
        "high_reward_payoff": "Reward is unknown until the branch names a source model, target consequence, and transfer interface.",
        "pivot_criteria": "Backtrack if it cannot classify its pressure after one sharpening attempt.",
    },
}

CONTRIBUTION_MONITOR = ROOT / "agentic/reports/scientific_contribution_monitor/latest.json"
PVSNP_NEGATIVE_TACTICS = ROOT / "agentic/reports/pvsnp_negative_tactics/latest.json"
RESULT_SUBGOAL_ATLAS = ROOT / "agentic/reports/result_subgoal_atlas/latest.json"
PROBLEM_SPACE_MAP = ROOT / "agentic/reports/problem_space_map/latest.json"


def contribution_budget_hint(target_id: str) -> dict[str, str]:
    monitor = load_optional_json(CONTRIBUTION_MONITOR)
    if clean_text(monitor.get("target_id")) and clean_text(monitor.get("target_id")) != clean_text(target_id):
        return {}
    status = clean_text(monitor.get("contribution_aim_status"))
    if not status:
        return {}
    if status == "handoff_ready":
        return {
            "budget_posture": "pause_broad_exploration_for_publishable_handoff",
            "why_this_budget_now": clean_text(monitor.get("next_contribution_objective")),
        }
    if status == "near_stepping_stone_available":
        return {
            "budget_posture": "prioritize_bounded_stepping_stone_certification",
            "why_this_budget_now": clean_text(monitor.get("next_contribution_objective")),
        }
    if status == "active_candidate_available":
        return {
            "budget_posture": "continue_only_if_maturity_improves",
            "why_this_budget_now": clean_text(monitor.get("next_contribution_objective")),
        }
    return {
        "budget_posture": "contribution_search",
        "why_this_budget_now": clean_text(monitor.get("next_contribution_objective")),
    }


def negative_tactic_packet() -> dict[str, Any]:
    return load_optional_json(PVSNP_NEGATIVE_TACTICS)


def negative_tactic_hint(branch: dict[str, Any]) -> dict[str, Any]:
    if clean_text(branch.get("target_id")) != "p-vs-np-target":
        return {}
    branch_id = clean_text(branch.get("branch_id"))
    packet = negative_tactic_packet()
    for row in packet.get("recommendations", []) if isinstance(packet.get("recommendations"), list) else []:
        if isinstance(row, dict) and clean_text(row.get("branch_id")) == branch_id:
            return row
    return {}


def atlas_hint(branch: dict[str, Any]) -> dict[str, Any]:
    target_id = clean_text(branch.get("target_id"))
    atlas = load_optional_json(RESULT_SUBGOAL_ATLAS)
    problem_map = load_optional_json(PROBLEM_SPACE_MAP)
    if clean_text(atlas.get("target_id")) != target_id:
        return {}
    family = branch_pressure_family(branch)
    family_aliases = {
        "hardness_magnification_threshold": "hardness_magnification",
        "barrier_and_impossibility_control": "natural_property_barrier",
        "meta_complexity_carrier": "mcsp_mktp_carrier",
        "proof_complexity_transfer": "proof_complexity_transfer",
        "quantifier_uniformity_lift": "all_exponent_uniformity",
    }
    atlas_family = family_aliases.get(family, family)
    related = []
    for row in atlas.get("results", []) if isinstance(atlas.get("results"), list) else []:
        if clean_text(row.get("problem_space_coordinates", {}).get("route_family")) == atlas_family:
            related.append(row)
    node = {}
    if clean_text(problem_map.get("target_id")) == target_id:
        node = next(
            (
                item
                for item in problem_map.get("nodes", [])
                if isinstance(item, dict) and clean_text(item.get("route_family")) == atlas_family
            ),
            {},
        )
    return {
        "atlas_route_family": atlas_family,
        "related_result_count": len(related),
        "near_handoff_count": len([row for row in related if row.get("achievement_status") in {"handoff_ready", "partially_achieved"}]),
        "open_obligations": sorted({item for row in related for item in row.get("open_obligations", []) if clean_text(item)})[:5],
        "problem_node_status": node.get("status", ""),
        "next_achievement": node.get("next_achievement", ""),
    }


def branch_score(branch: dict[str, Any]) -> tuple[int, int, int, str]:
    status_bonus = 0 if branch.get("status") == "active" else 2
    priority = int(branch.get("priority", 999))
    hint = negative_tactic_hint(branch)
    tactic = clean_text(hint.get("tactic_mode"))
    if tactic in {"impossibility_theorem", "proof_by_contradiction", "falsifier_search"}:
        priority -= 2
    if tactic in {"quarantine", "stop"}:
        status_bonus += 2
    hint = atlas_hint(branch)
    if hint.get("open_obligations"):
        priority -= 1
    if hint.get("problem_node_status") in {"achieved"} and int(hint.get("related_result_count", 0)) > 2:
        priority += 1
    starvation = -int(branch.get("consecutive_low_learning_cycles", 0))
    attempts = int(branch.get("attempt_count", 0))
    return (status_bonus, priority, starvation, attempts, branch.get("branch_id", ""))


def branch_blocks_broad_api_reasoning(branch: dict[str, Any]) -> bool:
    """Return whether a target-specific gate forbids ordinary broad API search."""
    hint = artifact_or_stop_hint_for_branch(branch)
    return bool(hint and not hint.get("broad_api_reasoning_allowed", True))


def branch_pressure_family(branch: dict[str, Any]) -> str:
    """Classify P vs NP branches so parallel cycles do not duplicate one pressure."""
    if clean_text(branch.get("target_id")) != "p-vs-np-target":
        return "general_target_pressure"
    text = clean_text(
        {
            "title": branch.get("title", ""),
            "machinery_role": branch.get("machinery_role", ""),
            "controlled_interface": branch.get("controlled_interface", ""),
            "hypothesis": branch.get("hypothesis", ""),
            "mathematical_mechanism": branch.get("mathematical_mechanism", ""),
            "dependencies": branch.get("dependencies", []),
            "falsifiers": branch.get("falsifiers", []),
            "skill_requirements": branch.get("skill_requirements", []),
        }
    ).lower()
    for family, markers in PVSNP_PRESSURE_FAMILIES:
        if any(marker in text for marker in markers):
            return family
    return "unclassified_pvsnp_pressure"


def decision_for(branch: dict[str, Any]) -> dict[str, Any]:
    blockers = int(branch.get("consecutive_low_learning_cycles", 0))
    family = branch_pressure_family(branch)
    family_control = PVSNP_FAMILY_CONTROL.get(family, {}) if clean_text(branch.get("target_id")) == "p-vs-np-target" else {}
    tactic_hint = negative_tactic_hint(branch)
    result_hint = atlas_hint(branch)
    if blockers >= 2:
        move = "restrategize_with_backtrack_test"
        reason = (
            "The branch has repeated low-learning cycles, so the next pass must either sharpen the source/target objects "
            "or backtrack to the missing bridge premise."
        )
    elif branch.get("status") == "watch":
        move = "sample_for_diversity"
        reason = "The branch is sampled to prevent the marathon from overfitting to a single proof route."
    else:
        move = "persist_adapt"
        reason = "The branch remains target-linked and has not exhausted its certification tests."
    tactic = clean_text(tactic_hint.get("tactic_mode"))
    if tactic in {"impossibility_theorem", "proof_by_contradiction", "falsifier_search"}:
        move = clean_text(tactic_hint.get("branch_control_decision")) or move
        reason = clean_text(tactic_hint.get("reason_for_tactic")) or reason
    elif tactic in {"quarantine", "stop", "backtrack"}:
        move = clean_text(tactic_hint.get("branch_control_decision")) or tactic
        reason = clean_text(tactic_hint.get("reason_for_tactic")) or reason
    budget_hint = contribution_budget_hint(clean_text(branch.get("target_id")))
    avenue_id = classify_branch_avenue(branch)
    warrant = warrant_summary(warrant_for_branch(branch))
    warrant_decision = clean_text(warrant.get("investment_decision"))
    if warrant_decision in {"artifact_sprint_only", "reframe_gap_before_investment", "do_not_invest_prior_art_collision", "quarantine_low_relevance"}:
        reason = f"{reason} Literature-gap gate: {clean_text(warrant.get('effect'))}"
        if warrant_decision == "artifact_sprint_only" and move == "persist_adapt":
            move = "bounded_artifact_sprint"
        elif warrant_decision == "reframe_gap_before_investment" and move == "persist_adapt":
            move = "reframe_gap_before_investment"
        elif warrant_decision in {"do_not_invest_prior_art_collision", "quarantine_low_relevance"}:
            move = warrant_decision
    artifact_hint = artifact_or_stop_hint_for_branch(branch)
    if artifact_hint:
        move = clean_text(artifact_hint.get("recommended_move")) or "artifact_sprint_required"
        reason = f"{reason} Artifact-or-stop gate: {clean_text(artifact_hint.get('reason'))}"
    return {
        "branch_id": branch["branch_id"],
        "branch_title": branch["title"],
        "recommended_move": move,
        "reason": reason,
        **budget_hint,
        "avenue_id": avenue_id,
        "literature_gap_warrant": warrant,
        "warrant_decision": warrant_decision,
        "allowed_next_modes": artifact_hint.get("allowed_next_modes", []) if artifact_hint else warrant.get("allowed_next_modes", []),
        "warrant_required_before_broad_search": True,
        "warrant_effect": warrant.get("effect", ""),
        "artifact_or_stop": artifact_hint,
        "artifact_or_stop_mode": artifact_hint.get("control_decision", ""),
        "artifact_or_stop_required_artifact": artifact_hint.get("required_artifact", []),
        "artifact_or_stop_forbidden_next_modes": artifact_hint.get("forbidden_next_modes", []),
        "broad_api_reasoning_allowed": artifact_hint.get("broad_api_reasoning_allowed", True),
        "controlled_interface": branch.get("controlled_interface", ""),
        "pressure_family": family,
        "negative_tactic_mode": tactic,
        "negative_tactic_route_family": tactic_hint.get("route_family", ""),
        "negative_tactic_escape_conditions": tactic_hint.get("escape_conditions", []),
        "negative_tactic_validation_handoff": tactic_hint.get("next_validation_handoff", ""),
        "result_atlas_route_family": result_hint.get("atlas_route_family", ""),
        "result_atlas_related_result_count": result_hint.get("related_result_count", 0),
        "result_atlas_open_obligations": result_hint.get("open_obligations", []),
        "problem_map_node_status": result_hint.get("problem_node_status", ""),
        "problem_map_next_achievement": result_hint.get("next_achievement", ""),
        "novelty_signal": family_control.get("novelty_signal", ""),
        "high_reward_payoff": family_control.get("high_reward_payoff", ""),
        "step_back_or_pivot_criteria": family_control.get("pivot_criteria", ""),
    }


def select_branches(branches: list[dict[str, Any]], max_active: int = 3) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidates = [branch for branch in branches if branch.get("status") not in {"archived", "stopped"}]
    ranked_candidates = sorted(candidates, key=branch_score)
    broad_api_candidates = [branch for branch in ranked_candidates if not branch_blocks_broad_api_reasoning(branch)]
    ranked = broad_api_candidates or ranked_candidates
    selected: list[dict[str, Any]] = []
    seen_families: set[str] = set()
    limit = max(1, max_active)
    for branch in ranked:
        family = branch_pressure_family(branch)
        if family in seen_families and len(ranked) - len(selected) >= limit - len(selected):
            continue
        selected.append(branch)
        seen_families.add(family)
        if len(selected) >= limit:
            break
    if len(selected) < limit:
        selected_ids = {branch["branch_id"] for branch in selected}
        for branch in ranked:
            if branch["branch_id"] in selected_ids:
                continue
            selected.append(branch)
            if len(selected) >= limit:
                break
    return selected, [decision_for(branch) for branch in selected]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id")
    parser.add_argument("--max-active-branches", type=int, default=3)
    args = parser.parse_args()
    pointer = load_active_pointer()
    _, run_state = load_run_state(args.run_id or pointer.get("run_id"))
    branches = load_branches(run_state) if run_state else []
    candidates = [branch for branch in branches if branch.get("status") not in {"archived", "stopped"}]
    blocked_branch_ids = [
        branch["branch_id"]
        for branch in sorted(candidates, key=branch_score)
        if branch_blocks_broad_api_reasoning(branch)
    ]
    selected, decisions = select_branches(branches, args.max_active_branches)
    dump_stdout(
        {
            "selected_branch_ids": [branch["branch_id"] for branch in selected],
            "skipped_broad_api_blocked_branch_ids": [
                branch_id for branch_id in blocked_branch_ids if branch_id not in {branch["branch_id"] for branch in selected}
            ],
            "scheduler_decisions": decisions,
            "summary": clean_text(f"selected {len(selected)} branches from {len(branches)} available branches"),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
