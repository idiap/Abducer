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
"""Validate P vs NP Gedanken experiments and extracted conclusions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agentic_common import ROOT, fail, load_json_object, rel


REPORT = ROOT / "agentic/reports/pvsnp_gedanken_experiments/latest.json"
REQUIRED_CONCLUSIONS = {
    "decisive_intuition",
    "formal_lesson",
    "route_control_consequence",
    "next_action",
}
DOMAIN_TERMS = {
    "sat",
    "oracle",
    "beta",
    "exponent",
    "mcsp",
    "mktp",
    "truth table",
    "certificate",
    "natural",
    "proof",
    "circuit",
    "p/poly",
    "padding",
    "projection",
    "advice",
    "uniform",
}
EXPECTED_PRESSURES = {
    "black_box_substitution_cap",
    "meta_complexity_carrier_debt",
    "naturalness_density_pressure",
    "all_exponent_quantifier_gap",
    "proof_complexity_transfer_gap",
}


def domain_score(packet: dict[str, Any]) -> int:
    text = str(packet).lower().replace("-", " ")
    return sum(1 for term in DOMAIN_TERMS if term in text)


def main() -> int:
    if not REPORT.exists():
        fail(f"missing P vs NP Gedanken report: {rel(REPORT)}")
    payload = load_json_object(REPORT)
    if payload.get("target_id") != "p-vs-np-target":
        fail("P vs NP Gedanken report must target p-vs-np-target")
    packets = payload.get("packets")
    if not isinstance(packets, list) or len(packets) < 5:
        fail("expected at least five P vs NP Gedanken packets")
    pressures = set()
    for packet in packets:
        if not isinstance(packet, dict):
            fail("packet entries must be objects")
        packet_id = str(packet.get("packet_id", "unknown"))
        if domain_score(packet) < 6:
            fail(f"{packet_id} lacks P vs NP domain-specific content")
        conclusions = packet.get("essential_conclusions")
        if not isinstance(conclusions, dict):
            fail(f"{packet_id} missing essential_conclusions")
        missing = sorted(REQUIRED_CONCLUSIONS - set(conclusions))
        if missing:
            fail(f"{packet_id} missing conclusions: {', '.join(missing)}")
        for key in REQUIRED_CONCLUSIONS:
            words = str(conclusions.get(key, "")).split()
            if len(words) < 8:
                fail(f"{packet_id} conclusion {key} is too thin")
        if not any(action in str(conclusions.get("next_action", "")).lower() for action in ["audit", "theorem", "ledger", "quarantine", "formalize", "instantiate"]):
            fail(f"{packet_id} next_action is not operational")
        trigger = packet.get("trigger_criteria", [])
        if isinstance(trigger, list) and trigger:
            pressures.add(str(trigger[0]))
        if not isinstance(packet.get("variants"), list) or not packet["variants"]:
            fail(f"{packet_id} needs a diagnostic variant")
        if not isinstance(packet.get("followup_cycle_tasks"), list) or len(packet["followup_cycle_tasks"]) < 2:
            fail(f"{packet_id} needs at least two follow-up tasks")
        task_text = str(packet.get("followup_cycle_tasks", [])).lower()
        if "pvsnp" not in task_text and "next-experiment" not in task_text:
            fail(f"{packet_id} follow-up tasks do not use P vs NP skills")
        transfer = packet.get("transfer_scope", {})
        if not isinstance(transfer, dict) or transfer.get("transfer_verdict") != "needs_certificate":
            fail(f"{packet_id} must keep thought-experiment transfer at needs_certificate")
    missing_pressures = sorted(EXPECTED_PRESSURES - pressures)
    if missing_pressures:
        fail(f"missing expected P vs NP pressures: {', '.join(missing_pressures)}")
    summary = payload.get("essential_conclusions_summary")
    if not isinstance(summary, list) or len(summary) != len(packets):
        fail("essential_conclusions_summary must mirror packet count")
    print(f"validated {len(packets)} P vs NP Gedanken packets with essential conclusions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
