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
"""Validate exact symbolic matrix probe artifacts."""

from __future__ import annotations

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


REPORT = ROOT / "agentic/reports/symbolic_matrix_probe/latest.json"


def main() -> int:
    if not REPORT.exists():
        fail(f"missing {rel(REPORT)}")
    report = load_json_object(REPORT)
    for field in ["version", "target_id", "generated_utc", "status", "symbolic_backend", "probe_decision", "identities", "falsifier_templates", "analytic_obligation_seeds", "non_claims"]:
        if not report.get(field):
            fail(f"{rel(REPORT)} missing {field}")
    if report["status"] != "symbolic_formula":
        fail(f"{rel(REPORT)} status must be symbolic_formula")
    text = clean_text(report).lower()
    for marker in ["det(q)", "rho12", "cos(phi)", "holonomy", "pairwise", "same-theory", "not a simulation"]:
        if marker not in text:
            fail(f"{rel(REPORT)} lacks `{marker}`")
    if "proof_obligation_discharged" in text or "proves a spectral gap" in text:
        fail(f"{rel(REPORT)} overclaims proof status")
    decision = report["probe_decision"]
    if decision.get("decision") != "derive_symbolically":
        fail(f"{rel(REPORT)} probe decision must be derive_symbolically")
    numeric = decision.get("numeric_probe_if_needed", {})
    if numeric.get("allowed"):
        fail(f"{rel(REPORT)} must not allow numeric search for exact determinant derivation")
    identities = report.get("identities", [])
    if len(identities) < 3:
        fail(f"{rel(REPORT)} needs determinant, minor, and holonomy identities")
    for index, identity in enumerate(identities, start=1):
        for field in ["id", "name", "latex", "formula", "valid_when", "epistemic_status"]:
            if not clean_text(identity.get(field)):
                fail(f"{rel(REPORT)} identity {index} missing {field}")
        if identity.get("epistemic_status") != "symbolic_formula":
            fail(f"{rel(REPORT)} identity {index} must remain symbolic_formula")
    print(f"validated {rel(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
