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
"""Validate PMP analytic estimate obligation artifacts."""

from __future__ import annotations

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


REPORT = ROOT / "agentic/reports/analytic_estimate_obligations/latest.json"
FINITE_INTERFACES = ROOT / "agentic/reports/finite_algebra_interfaces/latest.json"


def main() -> int:
    if not REPORT.exists():
        fail(f"missing {rel(REPORT)}")
    if not FINITE_INTERFACES.exists():
        fail(f"missing {rel(FINITE_INTERFACES)}")
    report = load_json_object(REPORT)
    for field in ["version", "target_id", "status", "obligations", "next_experiment_queue_items", "proof_safety"]:
        if not report.get(field):
            fail(f"{rel(REPORT)} missing {field}")
    obligations = report["obligations"]
    if len(obligations) < 6:
        fail(f"{rel(REPORT)} needs at least six analytic obligations including observable density")
    text = clean_text(report).lower()
    for marker in ["boundary ope", "additive contact", "phase", "modulus", "same-theory", "finite algebra", "observable density"]:
        if marker not in text:
            fail(f"{rel(REPORT)} lacks `{marker}`")
    if not report.get("finite_interface_artifacts") or int(report.get("finite_interface_packet_count", 0)) < 1:
        fail(f"{rel(REPORT)} must cite finite algebra interface packets")
    required_classes = {"boundary_ope_estimate", "contact_control", "phase_coboundary_control", "modulus_psd_control", "same_theory_realization", "observable_density"}
    classes = {item.get("obligation_class") for item in obligations}
    missing = sorted(required_classes - classes)
    if missing:
        fail(f"{rel(REPORT)} missing obligation classes: {', '.join(missing)}")
    for index, item in enumerate(obligations, start=1):
        for field in ["id", "title", "mathematical_object", "validity_regime", "source_formula_id", "what_would_certify_it", "what_would_falsify_it", "epistemic_status", "transfer_boundary", "obligation_class", "finite_interface_dependency", "source_side_conditions"]:
            if not clean_text(item.get(field)):
                fail(f"{rel(REPORT)} obligation {index} missing {field}")
        if item["epistemic_status"] != "analytic_obligation":
            fail(f"{rel(REPORT)} obligation {index} must remain analytic_obligation")
        if clean_text(item.get("what_would_certify_it")).lower() == clean_text(item.get("mathematical_object")).lower():
            fail(f"{rel(REPORT)} obligation {index} merely restates the formula/object")
    queue = report["next_experiment_queue_items"]
    if len(queue) != len(obligations):
        fail(f"{rel(REPORT)} queue count must match obligation count")
    if [item["priority_score"] for item in queue] != sorted([item["priority_score"] for item in queue], reverse=True):
        fail(f"{rel(REPORT)} queue must be sorted by priority")
    if report["proof_safety"].get("numeric_results_promote_proof") or report["proof_safety"].get("finite_matrix_algebra_is_proof"):
        fail(f"{rel(REPORT)} proof safety overclaims symbolic or numeric result")
    print(f"validated {rel(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
