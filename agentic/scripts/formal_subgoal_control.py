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

"""Universal control policy for formal subgoals in Abducer workflows."""

from __future__ import annotations

from typing import Any

from agentic_common import clean_text, stable_id


DECISIONS = ["persist_adapt", "backtrack", "pivot", "quarantine", "stop"]


DECISION_CRITERIA = {
    "persist_adapt": (
        "Continue by adaptation when the subgoal still names the same target object, preserves essential commitments, "
        "and the last obstruction taught a sharper mathematical premise, object, regime, or bridge to formulate."
    ),
    "backtrack": (
        "Move backward when the subgoal uses an object, theorem, representation, limit, or premise before the workflow has "
        "constructed or certified it."
    ),
    "pivot": (
        "Change route family when the same certified obstruction repeats after adaptation and no new target-relevant "
        "mathematical information is being produced."
    ),
    "quarantine": (
        "Hold the idea as visible evidence or analogy when it is illuminating but lacks target-object identity, transfer "
        "certification, source grounding, or essential-commitment preservation."
    ),
    "stop": (
        "Stop spending active-loop budget when the subgoal has no meaningful target-object link or fails to generate new "
        "learning after repeated attempts."
    ),
}


POLICY = {
    "title": "Formal Subgoal Control Policy",
    "purpose": (
        "Control whether a formula, lemma, route subclaim, or proof obligation should be adapted, backtracked, pivoted, "
        "quarantined, or stopped during long-horizon exploration."
    ),
    "decision_order": DECISIONS,
    "decision_criteria": DECISION_CRITERIA,
    "universal_invariants": [
        "The subgoal must remain linked to the active target object or explicitly leave the proof queue.",
        "Persistence is licensed by informative mathematical learning, not by fluency or difficulty alone.",
        "A hard proof debt can remain active when it sharpens premises, definitions, or bridges.",
        "Repeated identical blockers without new information force backtrack, pivot, quarantine, or stop.",
        "Evidence-only, analogy-only, empirical, or transfer-risk routes remain outside proof authority until certified.",
    ],
    "required_fields": [
        "control_id",
        "decision",
        "target_object_link",
        "essential_commitments_preserved",
        "current_blocker",
        "adaptation_history",
        "learning_from_failure",
        "next_action",
        "backtrack_trigger",
        "pivot_trigger",
        "quarantine_trigger",
        "stop_condition",
        "repeated_blocker_count",
        "decision_rationale",
    ],
}


def target_object_link(candidate: dict[str, Any]) -> str:
    blueprint = candidate.get("route_blueprint", {}) if isinstance(candidate.get("route_blueprint"), dict) else {}
    family = clean_text(blueprint.get("route_family"))
    affected = ", ".join(clean_text(item) for item in candidate.get("affected_nodes", []) if clean_text(item))
    if family:
        return f"{family} acting on {affected or candidate.get('candidate_id', 'active target')}"
    return affected or clean_text(candidate.get("candidate_id")) or "active target object"


def repeated_blocker_count(candidate: dict[str, Any], route_disposition: str, hard_gates: dict[str, str]) -> int:
    count = 0
    if route_disposition == "quarantine":
        count += 2
    if hard_gates.get("source_grounding") == "fail":
        count += 2
    if hard_gates.get("target_activation") == "warn":
        count += 1
    if hard_gates.get("proof_queue_readiness") == "warn":
        count += 1
    if any("repeated" in clean_text(item).lower() for item in candidate.get("disconfirming_observations", [])):
        count += 1
    return count


def decide_subgoal_control(candidate: dict[str, Any], route_disposition: str, hard_gates: dict[str, str]) -> str:
    warn_count = list(hard_gates.values()).count("warn")
    if route_disposition in {"reject", "stop"}:
        return "stop"
    if route_disposition == "quarantine" or "fail" in hard_gates.values():
        return "quarantine"
    blueprint = candidate.get("route_blueprint", {}) if isinstance(candidate.get("route_blueprint"), dict) else {}
    family = clean_text(blueprint.get("route_family")).lower()
    operation = clean_text(candidate.get("creative_operation"))
    profile = candidate.get("domain_specificity", {}) if isinstance(candidate.get("domain_specificity"), dict) else {}
    score = float(profile.get("score") or 0.0)
    if operation in {"theorem_weakening", "representation_shift", "negative_route_inversion"}:
        return "backtrack"
    if route_disposition == "evidence_task" or operation == "analogy_transport":
        return "quarantine"
    if route_disposition == "revision_loop":
        return "backtrack"
    if warn_count >= 2:
        return "backtrack"
    if score < 0.35 and not family:
        return "stop"
    return "persist_adapt"


def subgoal_control_for_candidate(
    candidate: dict[str, Any],
    route_disposition: str,
    hard_gates: dict[str, str],
    *,
    target_commitments: list[str] | None = None,
) -> dict[str, Any]:
    """Return a universal subgoal-control packet for a generated candidate."""

    blueprint = candidate.get("route_blueprint", {}) if isinstance(candidate.get("route_blueprint"), dict) else {}
    profile = candidate.get("domain_specificity", {}) if isinstance(candidate.get("domain_specificity"), dict) else {}
    commitments = [
        str(item)
        for item in profile.get("commitment_ids", [])
        if str(item).strip() and (not target_commitments or item in target_commitments)
    ]
    if not commitments and target_commitments:
        commitments = target_commitments[:2]
    family = clean_text(blueprint.get("route_family")) or "unclassified formal route"
    failure_tests = [clean_text(item) for item in blueprint.get("failure_tests", []) if clean_text(item)]
    blocker = "; ".join(
        f"{gate}={status}"
        for gate, status in hard_gates.items()
        if status in {"warn", "fail"}
    )
    if not blocker:
        blocker = (
            "The route remains a proof obligation: its source and target objects are named, but the next mathematical bridge "
            "or lemma still has to be supplied."
        )
    decision = decide_subgoal_control(candidate, route_disposition, hard_gates)
    repeated = repeated_blocker_count(candidate, route_disposition, hard_gates)
    next_action_by_decision = {
        "persist_adapt": (
            f"Adapt the {family} into the next typed lemma by naming assumptions, constructed objects, validity regime, "
            "and the certification artifact that would change the route state."
        ),
        "backtrack": (
            f"Move this {family} claim behind the premise it currently assumes, then restate the assumed object or theorem "
            "as a prerequisite obligation."
        ),
        "pivot": (
            f"Demote this {family} route and promote a branch that preserves the failed commitment with a different carrier "
            "or proof mechanism."
        ),
        "quarantine": (
            "Keep the idea visible as evidence or analogy, but block proof-queue authority until source grounding and transfer "
            "certification are supplied."
        ),
        "stop": (
            "Stop allocating active-loop budget unless a future target ledger or source artifact supplies a new target-object link."
        ),
    }
    learning_by_decision = {
        "persist_adapt": (
            "The current obstruction is informative because it identifies the next missing bridge rather than invalidating the "
            "route family."
        ),
        "backtrack": (
            "The attempt taught that the formula is downstream of an unbuilt premise, so progress requires moving backward in "
            "the dependency order."
        ),
        "pivot": (
            "The attempt taught that the route family is not producing new target-relevant information after certified failures."
        ),
        "quarantine": (
            "The attempt may still guide evidence search, but it has not earned same-target proof authority."
        ),
        "stop": (
            "The attempt does not currently teach enough about the active target to justify further loop budget."
        ),
    }
    return {
        "control_id": stable_id("subgoal-control", candidate.get("candidate_id", ""), route_disposition, decision),
        "decision": decision,
        "target_object_link": target_object_link(candidate),
        "essential_commitments_preserved": list(dict.fromkeys(commitments)),
        "current_blocker": blocker,
        "adaptation_history": [
            "Generated from active pressure packet and validation gates.",
            f"Initial route disposition: {route_disposition}.",
            f"Hard-gate state: {', '.join(f'{gate}={status}' for gate, status in hard_gates.items())}.",
        ],
        "learning_from_failure": learning_by_decision[decision],
        "next_action": next_action_by_decision[decision],
        "backtrack_trigger": (
            "Backtrack if the next step uses a mathematical object, model, limit, theorem, or representation before the "
            "workflow has constructed or certified it."
        ),
        "pivot_trigger": (
            "Pivot if the same blocker repeats after the next certified adaptation with no sharper premise, no new object, "
            "and no improved target-preserving bridge."
        ),
        "quarantine_trigger": (
            failure_tests[0]
            if failure_tests
            else "Quarantine if the route is analogy-only, evidence-only, source-ungrounded, or cannot preserve the active target commitments."
        ),
        "stop_condition": (
            "Stop if no target-object link and no new mathematical learning can be stated after repeated adaptation attempts."
        ),
        "repeated_blocker_count": repeated,
        "decision_rationale": DECISION_CRITERIA[decision],
        "failure_tests": failure_tests,
    }


def validate_control_shape(control: Any) -> tuple[bool, str]:
    if not isinstance(control, dict):
        return False, "subgoal_control must be an object"
    missing = [field for field in POLICY["required_fields"] if field not in control]
    if missing:
        return False, f"missing fields: {', '.join(missing)}"
    if control.get("decision") not in DECISIONS:
        return False, f"invalid decision: {control.get('decision')}"
    for field in [
        "target_object_link",
        "current_blocker",
        "learning_from_failure",
        "next_action",
        "backtrack_trigger",
        "pivot_trigger",
        "quarantine_trigger",
        "stop_condition",
        "decision_rationale",
    ]:
        if not clean_text(control.get(field)):
            return False, f"{field} must be non-empty"
    for field in ["essential_commitments_preserved", "adaptation_history"]:
        if not isinstance(control.get(field), list) or not control[field]:
            return False, f"{field} must be a non-empty list"
    if int(control.get("repeated_blocker_count", -1)) < 0:
        return False, "repeated_blocker_count must be non-negative"
    return True, ""


def summary_from_controls(controls: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {decision: 0 for decision in DECISIONS}
    stale = []
    for control in controls:
        decision = str(control.get("decision", ""))
        if decision in counts:
            counts[decision] += 1
        if control.get("decision") == "persist_adapt" and int(control.get("repeated_blocker_count", 0)) >= 2:
            stale.append(
                {
                    "control_id": control.get("control_id", ""),
                    "target_object_link": control.get("target_object_link", ""),
                    "current_blocker": control.get("current_blocker", ""),
                    "required_action": "attach a new adaptation rationale or emit backtrack, pivot, quarantine, or stop",
                }
            )
    return {
        "decision_counts": counts,
        "active_control_count": len(controls),
        "stale_repeated_blockers": stale,
        "has_stale_repeated_blockers": bool(stale),
    }
