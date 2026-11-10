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
"""Build target-scoped proof strategy lock-in reports."""

from __future__ import annotations

import argparse
from typing import Any

from agentic_common import ROOT, clean_text, load_json_object, load_optional_json, rel, slugify, utc_now
from proof_depth_control import PROMOTION_DECISIONS, write_target_report
from target_profiles import TARGET_PROFILES


LEDGER_ROOT = ROOT / "agentic/reports/proof_learning/targets"
YM_TARGET_ID = "yang-mills-existence-and-mass-gap-target"
YM_DEMOTION_PACKET = ROOT / "agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/proof_objects/endpoint_route_demotion_packet.json"
DEFAULT_CONSOLIDATION_LIMIT = 4
DEFAULT_RECURSION_DEPTH_LIMIT = 1
DEFAULT_ALLOWED_CYCLE_TYPES = [
    "proof_completion",
    "counterexample_or_falsifier",
    "finite_computation_or_symbolic_parameterization",
    "prior_art_boundary",
    "manuscript_integration",
]
DEFAULT_STOP_CONDITIONS = [
    "publication_ready_subgoal",
    "precise_demotion",
    "blocked_named_lemma",
    "budget_exhausted_release_to_exploration",
]


def load_ledger(target_id: str) -> dict[str, Any]:
    path = LEDGER_ROOT / slugify(target_id) / "latest.json"
    return load_json_object(path) if path.exists() else {}


def live_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [event for event in events if clean_text(event.get("source_cycle_id")).startswith("cycle-")]


def decide_mode(events: list[dict[str, Any]]) -> str:
    if any(event.get("release_decision") in PROMOTION_DECISIONS and event.get("transfer_substance_verdict") != "blocked" for event in events):
        return "lock_in_ready"
    if any(event.get("epistemic_status") == "demoted_generalization" for event in events):
        return "forced_demote"
    return "exploration_continue"


def profile_for(target_id: str) -> dict[str, Any]:
    return TARGET_PROFILES.get(target_id, {})


def main_problem_balance(target_id: str, lead: dict[str, Any]) -> dict[str, Any]:
    profile = profile_for(target_id)
    configured = profile.get("main_problem_balance", {})
    if isinstance(configured, dict) and configured:
        return configured
    observed = clean_text(lead.get("observed_result")) or "current local subgoal"
    return {
        "local_subgoal_scope": observed,
        "larger_problem_boundary": "The main target remains open until the target theorem, transfer, and non-claim boundaries are proved in the original problem setting.",
        "allowed_claim": "Claim only the local theorem, obstruction, worked example, transfer boundary, or demotion supported by the live ledger.",
        "forbidden_claims": [
            "Do not advertise a local subgoal as the full target theorem.",
            "Do not replace a missing transfer theorem by narrative continuity.",
        ],
        "larger_problem_gate_map": ["construction", "transfer", "nontriviality", "target theorem"],
        "balance_test": "Every consolidation must state what larger-problem gate it changes and which gate remains untouched.",
    }


def publication_consolidation_control(mode: str, profile: dict[str, Any]) -> dict[str, Any]:
    configured = profile.get("publication_consolidation_policy", {})
    if not isinstance(configured, dict):
        configured = {}
    max_cycles = int(configured.get("max_completion_cycles", DEFAULT_CONSOLIDATION_LIMIT) or DEFAULT_CONSOLIDATION_LIMIT)
    max_depth = int(configured.get("max_recursion_depth", DEFAULT_RECURSION_DEPTH_LIMIT) or DEFAULT_RECURSION_DEPTH_LIMIT)
    allowed_cycle_types = configured.get("allowed_cycle_types", DEFAULT_ALLOWED_CYCLE_TYPES)
    stop_conditions = configured.get("stop_conditions", DEFAULT_STOP_CONDITIONS)
    if not isinstance(allowed_cycle_types, list) or not allowed_cycle_types:
        allowed_cycle_types = DEFAULT_ALLOWED_CYCLE_TYPES
    if not isinstance(stop_conditions, list) or not stop_conditions:
        stop_conditions = DEFAULT_STOP_CONDITIONS
    return {
        "status": "active_if_lock_in_ready" if mode == "lock_in_ready" else "inactive_until_lock_in_ready",
        "max_completion_cycles": min(max_cycles, DEFAULT_CONSOLIDATION_LIMIT),
        "max_recursion_depth": min(max_depth, DEFAULT_RECURSION_DEPTH_LIMIT),
        "current_recursion_depth": 0,
        "allowed_cycle_types": allowed_cycle_types,
        "stop_conditions": stop_conditions,
        "recursion_guard": clean_text(configured.get("recursion_guard"))
        or "No nested publication-consolidation loop is allowed; side work must fit the current budget or return to exploration.",
        "budget_exhaustion_action": "write a handoff, demote or block the subgoal, and return to conceptual exploration before any new publication consolidation",
        "reentry_condition": "only a new live learning event that changes a hard gate, supplies a missing object, or resolves a named blocker may start a fresh consolidation window",
    }


def build_report(target_id: str) -> dict[str, Any]:
    ledger = load_ledger(target_id)
    events = ledger.get("events", []) if isinstance(ledger.get("events"), list) else []
    live = live_events(events)
    decision_events = live
    mode = decide_mode(decision_events)
    lead = decision_events[-1] if decision_events else (events[-1] if events else {})
    transfer_verdict = clean_text(lead.get("transfer_substance_verdict")) or "no_transfer_subgoal_yet"
    profile = profile_for(target_id)
    balance = main_problem_balance(target_id, lead)
    consolidation = publication_consolidation_control(mode, profile)
    artifact_finalization = load_optional_json(YM_DEMOTION_PACKET) if target_id == YM_TARGET_ID else {}
    if artifact_finalization:
        mode = "released_to_exploration"
    return {
        "version": 1,
        "target_id": target_id,
        "generated_utc": utc_now(),
        "mode": mode,
        "frozen_subgoal": clean_text(lead.get("observed_result")) if mode == "lock_in_ready" else "",
        "conceptual_quality_basis": "Lock-in requires a sharp, novel, coherent result with explanatory or unification value.",
        "paper_relevance": (
            "support_only_or_appendix_note"
            if artifact_finalization
            else "publication_subgoal_candidate"
            if mode == "lock_in_ready"
            else "not_locked"
        ),
        "non_claims": [
            "Do not claim the main problem is solved from a subgoal.",
            "Do not promote a definition-built transfer theorem.",
            *[clean_text(item) for item in balance.get("forbidden_claims", []) if clean_text(item)],
        ],
        "main_problem_balance": balance,
        "publication_consolidation_control": consolidation,
        "cycle_budget": consolidation["max_completion_cycles"] if mode == "lock_in_ready" else 0,
        "completed_cycles": [artifact_finalization.get("completed_cycles")] if artifact_finalization else [],
        "stop_condition": ", ".join(consolidation["stop_conditions"]),
        "next_allowed_action": (
            "conceptual_exploration_after_release"
            if artifact_finalization
            else "proof-strategy-lockin-orchestrator"
            if mode == "lock_in_ready"
            else "proof-depth-pressure-formalizer"
        ),
        "transfer_substance_verdict": transfer_verdict,
        "definition_expansion_result": "must pass before transfer-theorem lock-in",
        "failure_case_status": "required for transfer-theorem lock-in",
        "consequence_delta": clean_text(lead.get("observed_result")),
        "prior_art_delta": "required before paper promotion",
        "ledger_path": rel(LEDGER_ROOT / slugify(target_id) / "latest.json"),
        "live_event_count": len(live),
        "reference_fixture_event_count": max(0, len(events) - len(live)),
        "learning_event_ids": [event.get("event_id") for event in events],
        "return_to_exploration_note": consolidation["budget_exhaustion_action"],
        "artifact_or_stop_finalization": artifact_finalization,
        "validation_handoff": "agentic/scripts/validate_proof_lockin_report.py",
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Proof Lock-In Report",
        "",
        f"Target: `{report['target_id']}`",
        f"Mode: `{report['mode']}`",
        f"Paper relevance: `{report['paper_relevance']}`",
        f"Transfer substance: `{report['transfer_substance_verdict']}`",
        f"Cycle budget: `{report['cycle_budget']}`",
        "",
        "## Subgoal",
        "",
        report.get("frozen_subgoal") or "No frozen subgoal is active.",
        "",
        "## Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in report.get("non_claims", []))
    balance = report.get("main_problem_balance", {})
    consolidation = report.get("publication_consolidation_control", {})
    lines.extend(
        [
            "",
            "## Main-Problem Balance",
            "",
            f"- Local scope: {balance.get('local_subgoal_scope', '')}",
            f"- Larger boundary: {balance.get('larger_problem_boundary', '')}",
            f"- Allowed claim: {balance.get('allowed_claim', '')}",
            f"- Balance test: {balance.get('balance_test', '')}",
            "",
            "## Publication Consolidation Limit",
            "",
            f"- Max completion cycles: `{consolidation.get('max_completion_cycles')}`",
            f"- Max recursion depth: `{consolidation.get('max_recursion_depth')}`",
            f"- Stop conditions: `{', '.join(consolidation.get('stop_conditions', []))}`",
            f"- Recursion guard: {consolidation.get('recursion_guard', '')}",
            f"- Re-entry condition: {consolidation.get('reentry_condition', '')}",
        ]
    )
    finalization = report.get("artifact_or_stop_finalization", {})
    if finalization:
        lines.extend(
            [
                "",
                "## Artifact-Or-Stop Finalization",
                "",
                f"- Completed cycles: `{finalization.get('completed_cycles')}`",
                f"- Blocked named artifact: {finalization.get('blocked_named_artifact', '')}",
                f"- No nested consolidation: `{finalization.get('no_nested_consolidation')}`",
                f"- Release to exploration: {finalization.get('release_to_exploration', '')}",
                f"- Demotion boundary: {finalization.get('demotion_boundary', '')}",
            ]
        )
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            f"`{report['next_allowed_action']}`",
            "",
            f"Return note: {report['return_to_exploration_note']}",
            "",
            f"Validation handoff: `{report['validation_handoff']}`",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def target_ids_from_args(raw: list[str]) -> list[str]:
    return raw or sorted(TARGET_PROFILES)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-id", action="append", default=[])
    args = parser.parse_args()
    for target_id in target_ids_from_args(args.target_id):
        report = build_report(target_id)
        json_path, md_path = write_target_report("proof_lockin", target_id, report, render_markdown(report))
        print(f"wrote {rel(json_path)} and {rel(md_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
