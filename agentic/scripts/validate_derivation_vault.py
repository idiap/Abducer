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
"""Validate the derivation vault."""

from __future__ import annotations

from agentic_common import ROOT, clean_text, fail, load_json_object, rel
from target_profiles import target_profile


REPORT = ROOT / "agentic/reports/derivation_vault/latest.json"


def main() -> int:
    if not REPORT.exists():
        fail(f"missing {rel(REPORT)}")
    report = load_json_object(REPORT)
    for field in ["version", "generated_utc", "target_id", "source_atlas", "summary", "derivations", "validation_handoff"]:
        if not report.get(field):
            fail(f"{rel(REPORT)} missing {field}")
    target_id = clean_text(report.get("target_id"))
    derivations = report.get("derivations", [])
    if not isinstance(derivations, list) or len(derivations) < 3:
        fail(f"{rel(REPORT)} needs at least three derivations")
    for index, row in enumerate(derivations, start=1):
        for field in [
            "derivation_id",
            "target_id",
            "kind",
            "title",
            "claim",
            "definitions",
            "assumptions",
            "equations",
            "proof_steps",
            "proof_status",
            "unresolved_obligations",
            "non_claims",
            "linked_result_ids",
            "source_artifact",
        ]:
            if field not in row or (field not in {"linked_result_ids"} and not row.get(field)):
                fail(f"{rel(REPORT)} derivation {index} missing {field}")
        if row.get("target_id") != target_id:
            fail(f"{rel(REPORT)} derivation {index} target mismatch")
        if not row.get("linked_result_ids") and not clean_text(row.get("orphan_reason")):
            fail(f"{rel(REPORT)} derivation {index} must link to a result or state orphan_reason")
        if row.get("proof_status") in {"proof", "proved"} and row.get("unresolved_obligations"):
            fail(f"{rel(REPORT)} derivation {index} claims proof while obligations remain")
    text = clean_text(report).lower()
    forbidden = [term for term in target_profile(target_id).get("forbidden_cross_target_terms", []) if term in text]
    if forbidden:
        fail(f"{rel(REPORT)} contains cross-target terms: {sorted(set(forbidden))}")
    print(f"validated {rel(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
