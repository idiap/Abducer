#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Validate and apply the shared Looper gate policy."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentic_common import ROOT, clean_text, fail, load_json_object, rel
from abstraction_machinery_selection import validate_machinery_shape
from formal_subgoal_control import validate_control_shape


POLICY = ROOT / "agentic" / "registries" / "gate_policy.yaml"
HYPOTHESIS_MAP = ROOT / "artifacts/hegelian/hypothesis_exploration_map.json"
MARATHON_POINTER = ROOT / "agentic/runs/discovery_marathons/active_run.json"
MARATHON_REPORT = ROOT / "agentic/reports/discovery_marathon/latest.json"


DISPOSITION_DECISION_COMPATIBILITY = {
    "proof_queue": {"persist_adapt"},
    "discovery_branch": {"persist_adapt"},
    "revision_loop": {"backtrack", "persist_adapt"},
    "evidence_task": {"quarantine", "persist_adapt"},
    "quarantine": {"quarantine"},
    "reject": {"stop", "quarantine"},
    "stop": {"stop"},
}


def load_policy() -> dict[str, dict]:
    payload = load_json_object(POLICY)
    decisions = payload.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        fail(f"{rel(POLICY)} needs non-empty decisions")
    rows: dict[str, dict] = {}
    for decision in decisions:
        if not isinstance(decision, dict) or not clean_text(decision.get("id")):
            fail(f"{rel(POLICY)} decision entries need id")
        rows[decision["id"]] = decision
    for required in ["pass", "warn", "fail", "block", "quarantine", "promote"]:
        if required not in rows:
            fail(f"{rel(POLICY)} missing decision {required}")
    return rows


def validate_subgoal_control_gate() -> None:
    if not HYPOTHESIS_MAP.exists():
        return
    payload = load_json_object(HYPOTHESIS_MAP)
    for row in payload.get("candidate_rankings", []):
        if not isinstance(row, dict):
            continue
        control = row.get("subgoal_control")
        ok, reason = validate_control_shape(control)
        if not ok:
            fail(f"{rel(HYPOTHESIS_MAP)} {row.get('candidate_id')} gate missing valid subgoal_control: {reason}")
        disposition = row.get("route_disposition")
        decision = control.get("decision")
        if decision not in DISPOSITION_DECISION_COMPATIBILITY.get(disposition, set()):
            fail(f"{rel(HYPOTHESIS_MAP)} {row.get('candidate_id')} incompatible gate state: {disposition} vs {decision}")
        if disposition == "proof_queue" and decision != "persist_adapt":
            fail(f"{rel(HYPOTHESIS_MAP)} {row.get('candidate_id')} proof_queue route lacks persist_adapt control")
        if decision == "persist_adapt" and int(control.get("repeated_blocker_count", 0)) >= 2:
            fail(f"{rel(HYPOTHESIS_MAP)} {row.get('candidate_id')} persists despite repeated blockers")
        machinery = row.get("machinery_selection")
        ok, reason = validate_machinery_shape(machinery)
        if not ok:
            fail(f"{rel(HYPOTHESIS_MAP)} {row.get('candidate_id')} gate missing valid machinery_selection: {reason}")
        if disposition == "proof_queue" and machinery.get("machinery_role") == "obstruction":
            fail(f"{rel(HYPOTHESIS_MAP)} {row.get('candidate_id')} proof_queue route cannot use obstruction machinery")
        if disposition == "proof_queue" and "->" not in machinery.get("controlled_interface", ""):
            fail(f"{rel(HYPOTHESIS_MAP)} {row.get('candidate_id')} proof_queue route lacks controlled-interface arrow")


def validate_marathon_gate() -> None:
    if not MARATHON_POINTER.exists():
        return
    pointer = load_json_object(MARATHON_POINTER)
    if pointer.get("status") == "failed":
        fail(f"{rel(MARATHON_POINTER)} points to failed marathon run")
    if not MARATHON_REPORT.exists():
        fail(f"active discovery marathon requires {rel(MARATHON_REPORT)}")
    report = load_json_object(MARATHON_REPORT)
    if report.get("status") == "failed":
        fail(f"{rel(MARATHON_REPORT)} has failed status")
    if report.get("breakthrough_status") not in {"no_breakthrough_claimed", "potential_breakthrough_signal"}:
        fail(f"{rel(MARATHON_REPORT)} has unknown breakthrough_status")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decision-json", help="Optional JSON file containing decision, reason, and evidence.")
    args = parser.parse_args()
    policy = load_policy()
    if args.decision_json:
        decision_packet = load_json_object(Path(args.decision_json))
        decision_id = clean_text(decision_packet.get("decision"))
        if decision_id not in policy:
            fail(f"unknown gate decision: {decision_id}")
        rule = policy[decision_id]
        if rule.get("requires_reason") and not clean_text(decision_packet.get("reason")):
            fail(f"decision {decision_id} requires reason")
        if rule.get("requires_evidence") and not decision_packet.get("evidence"):
            fail(f"decision {decision_id} requires evidence")
        print(json.dumps({"decision": decision_id, "blocks": bool(rule.get("blocks"))}, sort_keys=True))
    else:
        validate_subgoal_control_gate()
        validate_marathon_gate()
        print(f"validated gate policy with {len(policy)} decisions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
