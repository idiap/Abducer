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
"""Validate non-Lean finite algebra interface packets."""

from __future__ import annotations

import json

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


SCHEMA = ROOT / "agentic/spec/finite_algebra_interface_packet.schema.json"
REPORT = ROOT / "agentic/reports/finite_algebra_interfaces/latest.json"
FORBIDDEN_PROOF_PHRASES = [
    "lean checked",
    "theorem-prover output",
    "continuum yang-mills proof progress",
    "proves a mass gap",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_packet(packet: dict, source_label: str) -> None:
    schema = load_json_object(SCHEMA)
    for field in schema["required"]:
        require(field in packet and packet[field], f"{source_label} packet missing {field}")
    require(packet["epistemic_status"] == "equational_interface", f"{source_label} packet must be equational_interface")
    cycles = packet.get("source_cycle_ids", [])
    require(isinstance(cycles, list) and cycles, f"{source_label} packet needs source_cycle_ids")
    text = clean_text(packet).lower()
    for marker in ["det(q)", "rho", "phi", "holonomy", "rephasing", "side", "falsifier"]:
        require(marker in text, f"{source_label} packet lacks marker `{marker}`")
    for forbidden in FORBIDDEN_PROOF_PHRASES:
        if forbidden in text and f"not {forbidden}" not in text and f"not {forbidden.replace(' output', '')}" not in text:
            fail(f"{source_label} packet overclaims with `{forbidden}`")
    for identity in packet["exact_identities"]:
        for field in ["id", "name", "formula", "latex", "valid_when", "derivation_method", "symbolic_backend", "epistemic_status"]:
            require(clean_text(identity.get(field)), f"{source_label} identity missing {field}")
        require(identity["epistemic_status"] == "symbolic_formula", f"{source_label} identity {identity.get('id')} must be symbolic_formula")
    require(len(packet["side_conditions"]) >= 5, f"{source_label} needs at least five side conditions")
    for condition in packet["side_conditions"]:
        for field in ["id", "condition", "why_needed", "failure_effect"]:
            require(clean_text(condition.get(field)), f"{source_label} side condition missing {field}")
    require(len(packet["falsifier_templates"]) >= 4, f"{source_label} needs formula-derived falsifier templates")
    for falsifier in packet["falsifier_templates"]:
        for field in ["id", "epistemic_status", "preserved_assumptions", "changed_condition", "disconfirming_observation", "branch_control_effect", "numeric_search_allowed"]:
            require(falsifier.get(field), f"{source_label} falsifier missing {field}")
        require(falsifier["epistemic_status"] == "falsifier_shape", f"{source_label} falsifier {falsifier.get('id')} must be falsifier_shape")
    classes = {item.get("class") for item in packet["analytic_obligations"]}
    for required_class in {"boundary_ope_estimate", "contact_control", "phase_coboundary_control", "modulus_psd_control", "same_theory_realization"}:
        require(required_class in classes, f"{source_label} missing obligation class {required_class}")
    non_claims = clean_text(packet["non_claims"]).lower()
    for phrase in ["not lean checked", "not theorem-prover output", "not continuum yang-mills proof progress", "not a simulation", "does not prove a mass gap"]:
        require(phrase in non_claims, f"{source_label} non_claims missing `{phrase}`")


def main() -> int:
    json.loads(SCHEMA.read_text(encoding="utf-8"))
    if not REPORT.exists():
        fail(f"missing {rel(REPORT)}")
    report = load_json_object(REPORT)
    for field in ["version", "generated_utc", "status", "packets", "summary", "validation_handoff"]:
        require(report.get(field), f"{rel(REPORT)} missing {field}")
    packets = report["packets"]
    require(isinstance(packets, list) and packets, f"{rel(REPORT)} needs packets")
    for index, packet in enumerate(packets, start=1):
        validate_packet(packet, f"{rel(REPORT)} packet {index}")
    summary = report["summary"]
    require(summary.get("proof_safe") is True, f"{rel(REPORT)} summary proof_safe must be true")
    require(int(summary.get("identity_count", 0)) >= 3, f"{rel(REPORT)} summary needs identity count")
    require(int(summary.get("falsifier_template_count", 0)) >= 4, f"{rel(REPORT)} summary needs falsifier count")
    print(f"validated {rel(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
