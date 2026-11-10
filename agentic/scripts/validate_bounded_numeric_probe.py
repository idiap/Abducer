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
"""Validate guarded PMP bounded numeric probe artifacts."""

from __future__ import annotations

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


REPORT = ROOT / "agentic/reports/bounded_numeric_probe/latest.json"


def main() -> int:
    if not REPORT.exists():
        print(f"No {rel(REPORT)} yet; bounded numeric probe validator is idle.")
        return 0
    report = load_json_object(REPORT)
    for field in ["version", "target_id", "status", "decision_packet", "probe", "deterministic_reproducibility", "transfer_boundary"]:
        if not report.get(field):
            fail(f"{rel(REPORT)} missing {field}")
    if report["status"] not in {"calibration_only", "validated_probe", "falsifier_candidate"}:
        fail(f"{rel(REPORT)} has invalid numeric status {report['status']}")
    decision = report["decision_packet"]
    if decision.get("decision") != "run_bounded_numeric_probe":
        fail(f"{rel(REPORT)} decision packet must be run_bounded_numeric_probe")
    if "cannot prove" not in clean_text(decision.get("non_proof_boundary")).lower():
        fail(f"{rel(REPORT)} must state non-proof boundary")
    probe = report["probe"]
    if not probe.get("bounded_domain") or not probe.get("stopping_condition"):
        fail(f"{rel(REPORT)} probe needs bounded_domain and stopping_condition")
    if "unbounded" in clean_text(report).lower() or "proves yang-mills" in clean_text(report).lower():
        fail(f"{rel(REPORT)} overclaims or permits unbounded search")
    print(f"validated {rel(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
