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
"""Build a live P vs NP inference-quality report from packets and current run state."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, load_json_object, rel, stable_id, utc_now, write_json
from discovery_marathon_common import load_cycles, load_run_state, write_markdown


TARGET_ID = "p-vs-np-target"
OUT_DIR = ROOT / "agentic/reports/pvsnp_inference_quality"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
FIXTURE = ROOT / "agentic/fixtures/pvsnp_inference_quality/valid_transfer_packet.json"


def discover_packets(value: Any) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    if isinstance(value, dict):
        candidate = value.get("pvsnp_inference_quality")
        if isinstance(candidate, dict):
            packets.append(candidate)
        elif isinstance(candidate, list):
            packets.extend(item for item in candidate if isinstance(item, dict))
        for key in ["inference_quality_packets", "packets"]:
            nested = value.get(key)
            if isinstance(nested, list):
                packets.extend(item for item in nested if isinstance(item, dict))
        for nested in value.values():
            if isinstance(nested, (dict, list)):
                packets.extend(discover_packets(nested))
    elif isinstance(value, list):
        for item in value:
            packets.extend(discover_packets(item))
    return packets


def packet_summary(packet: dict[str, Any], *, live: bool = True) -> dict[str, Any]:
    model = packet.get("model_context", {}) if isinstance(packet.get("model_context"), dict) else {}
    quant = packet.get("quantifier_context", {}) if isinstance(packet.get("quantifier_context"), dict) else {}
    derivation = packet.get("derivation_status", {}) if isinstance(packet.get("derivation_status"), dict) else {}
    barrier = packet.get("barrier_status", {}) if isinstance(packet.get("barrier_status"), dict) else {}
    findings = packet.get("reviewer_findings", []) if isinstance(packet.get("reviewer_findings"), list) else []
    return {
        "packet_id": clean_text(packet.get("packet_id")),
        "branch_id": clean_text(packet.get("branch_id")),
        "inference_rule": clean_text(packet.get("inference_rule")),
        "source_statement": clean_text(packet.get("source_statement")),
        "target_statement": clean_text(packet.get("target_statement")),
        "source_carrier": clean_text(model.get("source_carrier")),
        "target_class": clean_text(model.get("target_class")),
        "reduction_type": clean_text(model.get("reduction_type")),
        "length_regime": clean_text(quant.get("length_regime")),
        "exponent_regime": clean_text(quant.get("exponent_regime")),
        "uniformity": clean_text(quant.get("uniformity")),
        "advice_status": clean_text(quant.get("advice_status")),
        "barrier_families": barrier.get("barrier_families", []) if isinstance(barrier.get("barrier_families"), list) else [],
        "derivation_status": clean_text(derivation.get("status")),
        "blocked_obligation": clean_text(derivation.get("blocked_obligation")),
        "decision": clean_text(packet.get("decision")),
        "reviewer_findings": findings,
        "validation_handoff": packet.get("validation_handoff", {}),
        "live_packet": live,
    }


def current_packet_obligation(cycles: list[dict[str, Any]]) -> dict[str, Any]:
    latest = cycles[-1] if cycles else {}
    text = clean_text(latest).lower()
    trigger = "current branch"
    if "mcsp" in text or "mktp" in text:
        trigger = "meta-complexity carrier branch"
    elif "proof complexity" in text or "tautolog" in text:
        trigger = "proof-complexity branch"
    elif "natural" in text:
        trigger = "natural-property branch"
    elif "beta" in text or "magnification" in text or "black-box" in text:
        trigger = "hardness-magnification branch"
    return {
        "obligation_id": stable_id("pvsnp-iq-obligation", trigger, latest.get("cycle_id", "")),
        "trigger": trigger,
        "required_packet": "The next theorem-shaped, transfer-shaped, or barrier-shaped claim must emit a pvsnp_inference_quality packet before promotion.",
        "minimum_fields": [
            "source_statement and target_statement",
            "model_context with source carrier, target class, circuit/proof model, and reduction type",
            "quantifier_context with length regime, exponent regime, uniformity, and advice status",
            "derivation_status with blocked obligation if incomplete",
            "reviewer findings from the appropriate consistency reviewers",
        ],
        "reviewer_stack": [
            "pvsnp-inference-quality-controller",
            "pvsnp-reduction-consistency-reviewer",
            "pvsnp-quantifier-uniformity-reviewer",
            "pvsnp-barrier-specificity-reviewer",
            "pvsnp-proof-derivation-builder",
        ],
    }


def build_report() -> dict[str, Any]:
    _, run_state = load_run_state()
    cycles = load_cycles(run_state) if run_state and run_state.get("target_id") == TARGET_ID else []
    live_packets = []
    for cycle in cycles:
        live_packets.extend(discover_packets(cycle))
    packets = [packet_summary(packet, live=True) for packet in live_packets]
    exemplar = packet_summary(load_json_object(FIXTURE), live=False) if FIXTURE.exists() else {}
    return {
        "version": 1,
        "target_id": TARGET_ID,
        "generated_utc": utc_now(),
        "source_run_id": run_state.get("run_id") if run_state else "",
        "summary": {
            "live_packet_count": len(packets),
            "exemplar_available": bool(exemplar),
            "quality_gate_status": "active_with_live_packets" if packets else "active_waiting_for_first_live_packet",
            "proof_gate": "agentic/scripts/validate_pvsnp_inference_quality.py",
        },
        "packets": packets,
        "exemplar_packet": exemplar,
        "current_packet_obligation": current_packet_obligation(cycles),
        "consistency_reviewer_stack": [
            {
                "skill": "pvsnp-reduction-consistency-reviewer",
                "checks": "reduction direction, transfer inequality, length map, and target preservation",
            },
            {
                "skill": "pvsnp-quantifier-uniformity-reviewer",
                "checks": "all lengths, all exponents, uniformity, and advice discipline",
            },
            {
                "skill": "pvsnp-barrier-specificity-reviewer",
                "checks": "route-specific relativization, algebrization, natural-proofs, and black-box status",
            },
            {
                "skill": "pvsnp-proof-complexity-transfer-reviewer",
                "checks": "proof-system lower bound versus semantic language/circuit transfer",
            },
            {
                "skill": "pvsnp-meta-complexity-carrier-reviewer",
                "checks": "MCSP/MKtP carrier, row selection, density, verifier overhead, and advice-free transfer",
            },
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# P vs NP Inference Quality",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Status: `{report['summary']['quality_gate_status']}`",
        f"- Live packets: `{report['summary']['live_packet_count']}`",
        f"- Validator: `{report['summary']['proof_gate']}`",
        "",
        "## Current Packet Obligation",
        "",
        report["current_packet_obligation"]["required_packet"],
        "",
        "## Reviewer Stack",
        "",
    ]
    for row in report["consistency_reviewer_stack"]:
        lines.append(f"- `{row['skill']}`: {row['checks']}")
    packets = report.get("packets") or ([report["exemplar_packet"]] if report.get("exemplar_packet") else [])
    lines.extend(["", "## Packet Summaries", ""])
    for packet in packets:
        lines.append(f"### {packet.get('packet_id')}")
        lines.append(f"- Decision: `{packet.get('decision')}`")
        lines.append(f"- Source: {packet.get('source_statement')}")
        lines.append(f"- Target: {packet.get('target_statement')}")
        lines.append(f"- Derivation: `{packet.get('derivation_status')}`")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    report = build_report()
    write_json(OUT_JSON, report)
    write_markdown(OUT_MD, render_markdown(report))
    print(f"wrote {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
