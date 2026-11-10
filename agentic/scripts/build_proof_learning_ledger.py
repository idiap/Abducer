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
"""Build target-scoped proof learning ledgers from proof-depth packets."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, load_json_object, rel, stable_id, utc_now
from discovery_marathon_common import load_cycles, load_run_state, write_markdown
from proof_depth_control import discover_proof_depth_packets, write_target_report
from target_profiles import DEFAULT_TARGET_ID, TARGET_PROFILES


FIXTURE_DIR = ROOT / "tests/fixtures/proof_depth"
VALID_FIXTURES = [
    FIXTURE_DIR / "substantive_transfer_theorem_accept.json",
    FIXTURE_DIR / "yang_mills_routea_geometric_gate.json",
    FIXTURE_DIR / "pvsnp_carrier_uniformity_gate.json",
]


def event_from_packet(packet: dict[str, Any], source: str) -> dict[str, Any]:
    event = packet.get("declarative_learning_event", {})
    if not isinstance(event, dict):
        event = {}
    event_id = clean_text(event.get("event_id")) or stable_id(
        "proof-learning",
        packet.get("target_id"),
        packet.get("packet_id"),
        packet.get("release_decision"),
    )
    return {
        "event_id": event_id,
        "target_id": clean_text(packet.get("target_id")),
        "packet_id": clean_text(packet.get("packet_id")),
        "source_cycle_id": clean_text(event.get("source_cycle_id") or packet.get("cycle_id")),
        "premises_used": event.get("premises_used", []) if isinstance(event.get("premises_used"), list) else [],
        "attempted_inference": clean_text(event.get("attempted_inference") or packet.get("proposed_move")),
        "observed_result": clean_text(event.get("observed_result") or packet.get("proof_object")),
        "learned_constraint": clean_text(event.get("learned_constraint") or packet.get("demotion_trigger")),
        "scope_condition": clean_text(event.get("scope_condition") or "target-scoped proof-depth packet"),
        "invalidated_generalization": clean_text(event.get("invalidated_generalization")),
        "future_routing_effect": clean_text(event.get("future_routing_effect") or packet.get("proposed_move")),
        "epistemic_status": clean_text(event.get("epistemic_status") or "branch_routing_rule"),
        "transfer_substance_verdict": clean_text(packet.get("transfer_substance_audit", {}).get("verdict")),
        "release_decision": clean_text(packet.get("release_decision")),
        "evidence": list(dict.fromkeys([source, *[clean_text(item) for item in event.get("evidence", []) if clean_text(item)]])),
        "validation_handoff": clean_text(event.get("validation_handoff") or "agentic/scripts/validate_proof_learning_ledger.py"),
    }


def load_fixture_packets() -> list[tuple[dict[str, Any], str]]:
    packets: list[tuple[dict[str, Any], str]] = []
    for path in VALID_FIXTURES:
        if path.exists():
            packets.append((load_json_object(path), rel(path)))
    return packets


def live_packets_for_target(target_id: str, run_id: str | None = None) -> list[tuple[dict[str, Any], str]]:
    _, run_state = load_run_state(run_id, target_id)
    if not run_state:
        return []
    packets: list[tuple[dict[str, Any], str]] = []
    for cycle in load_cycles(run_state):
        for packet in discover_proof_depth_packets(cycle):
            if clean_text(packet.get("target_id")) == target_id:
                packets.append((packet, f"cycle:{clean_text(cycle.get('cycle_id'))}"))
    return packets


def build_target_ledger(target_id: str, run_id: str | None = None) -> dict[str, Any]:
    packet_rows = live_packets_for_target(target_id, run_id)
    packet_rows.extend((packet, source) for packet, source in load_fixture_packets() if clean_text(packet.get("target_id")) == target_id)
    events_by_id: dict[str, dict[str, Any]] = {}
    duplicates = 0
    for packet, source in packet_rows:
        event = event_from_packet(packet, source)
        if event["event_id"] in events_by_id:
            duplicates += 1
            continue
        events_by_id[event["event_id"]] = event
    events = sorted(events_by_id.values(), key=event_sort_key)
    transfer_rules = [
        event
        for event in events
        if event.get("transfer_substance_verdict") in {"definitional_restatement", "notation_translation", "conservative_unpacking", "blocked", "substantive_transfer"}
    ]
    return {
        "version": 1,
        "target_id": target_id,
        "generated_utc": utc_now(),
        "status": "active" if events else "waiting_for_live_events",
        "summary": {
            "event_count": len(events),
            "deduplicated_events": duplicates,
            "transfer_substance_rule_count": len(transfer_rules),
            "release_decisions": sorted({event["release_decision"] for event in events if event.get("release_decision")}),
        },
        "events": events,
        "transfer_substance_rules": transfer_rules,
        "branch_routing_rules": [event for event in events if event.get("epistemic_status") == "branch_routing_rule"],
        "required_certificates": [event for event in events if event.get("epistemic_status") == "required_certificate"],
        "demoted_generalizations": [event for event in events if event.get("epistemic_status") == "demoted_generalization"],
        "validation_handoff": "agentic/scripts/validate_proof_learning_ledger.py",
    }


def event_sort_key(row: dict[str, Any]) -> tuple[int, int, str, str]:
    source = clean_text(row.get("source_cycle_id"))
    if source.startswith("cycle-"):
        try:
            cycle_index = int(source.split("-", 1)[1])
        except ValueError:
            cycle_index = 0
        return (1, cycle_index, source, clean_text(row.get("event_id")))
    return (0, 0, source, clean_text(row.get("event_id")))


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Proof Learning Ledger",
        "",
        f"Target: `{report['target_id']}`",
        f"Status: `{report['status']}`",
        f"Events: `{report['summary']['event_count']}`",
        f"Transfer-substance rules: `{report['summary']['transfer_substance_rule_count']}`",
        "",
        "## Declarative Learning Events",
        "",
    ]
    for event in report.get("events", []):
        lines.extend(
            [
                f"### {event['event_id']}",
                "",
                f"- Cycle: `{event.get('source_cycle_id')}`",
                f"- Status: `{event.get('epistemic_status')}`",
                f"- Release: `{event.get('release_decision')}`",
                f"- Transfer substance: `{event.get('transfer_substance_verdict')}`",
                f"- Learned constraint: {event.get('learned_constraint')}",
                f"- Future routing: {event.get('future_routing_effect')}",
                "",
            ]
        )
    lines.append(f"Validation handoff: `{report['validation_handoff']}`")
    return "\n".join(lines).rstrip() + "\n"


def target_ids_from_args(raw: list[str]) -> list[str]:
    if raw:
        return raw
    return sorted(TARGET_PROFILES) or [DEFAULT_TARGET_ID]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-id", action="append", default=[])
    parser.add_argument("--run-id")
    args = parser.parse_args()
    written = []
    for target_id in target_ids_from_args(args.target_id):
        report = build_target_ledger(target_id, args.run_id)
        json_path, md_path = write_target_report("proof_learning", target_id, report, render_markdown(report))
        written.append(rel(json_path))
        print(f"wrote {rel(json_path)} and {rel(md_path)}")
    print(f"built proof learning ledgers for {len(written)} target(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
