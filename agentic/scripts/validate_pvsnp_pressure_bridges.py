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
"""Validate P vs NP pressure-to-bridge abstraction artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agentic_common import ROOT, fail, load_json_object, rel


REPORT = ROOT / "agentic/reports/pvsnp_pressure_bridges/latest.json"
REQUIRED_FIELDS = {
    "id",
    "title",
    "priority_score",
    "pressure_types",
    "difficulty_hypothesis",
    "bridge_abstraction",
    "source_object",
    "target_object",
    "controlled_interface",
    "preserved_invariant",
    "proof_obligation",
    "symbolic_probe",
    "falsifiers",
    "when_to_persist",
    "when_to_pivot",
    "validation_handoff",
    "paper_safe_narrative",
}
DOMAIN_TERMS = {
    "sat",
    "np",
    "p/poly",
    "circuit",
    "lower-bound",
    "mcsp",
    "mktp",
    "proof-complexity",
    "natural",
    "oracle",
    "algebr",
    "padding",
    "projection",
    "nonuniform",
    "polynomial-size",
    "prf",
    "pseudorandom",
    "truth-table",
    "beta",
    "exponent",
}
EXPECTED_SKILLS = {
    "pvsnp-symbolic-complexity-auditor",
    "pvsnp-impossibility-theorem-forger",
    "pvsnp-qualitative-complexity-reasoner",
    "contradiction-route-auditor",
}


def contains_domain_specific_language(row: dict[str, Any]) -> bool:
    text = " ".join(str(row.get(field, "")).lower() for field in REQUIRED_FIELDS)
    return sum(1 for term in DOMAIN_TERMS if term in text) >= 5


def main() -> int:
    if not REPORT.exists():
        fail(f"missing report: {rel(REPORT)}")
    payload = load_json_object(REPORT)
    if payload.get("target_id") != "p-vs-np-target":
        fail("pressure bridge report must target p-vs-np-target")
    candidates = payload.get("bridge_candidates")
    if not isinstance(candidates, list) or len(candidates) < 5:
        fail("expected at least five P vs NP bridge candidates")
    seen = set()
    all_handoffs = set()
    has_no_go = False
    has_symbolic = False
    for row in candidates:
        if not isinstance(row, dict):
            fail("bridge candidate rows must be objects")
        missing = sorted(REQUIRED_FIELDS - set(row))
        if missing:
            fail(f"{row.get('id', '<unknown>')} missing fields: {', '.join(missing)}")
        bridge_id = str(row["id"])
        if bridge_id in seen:
            fail(f"duplicate bridge id: {bridge_id}")
        seen.add(bridge_id)
        if not str(row["id"]).startswith("pvsnp-bridge-"):
            fail(f"bridge id must be P vs NP specific: {row['id']}")
        if not contains_domain_specific_language(row):
            fail(f"{bridge_id} lacks enough P vs NP domain-specific language")
        if not isinstance(row["falsifiers"], list) or len(row["falsifiers"]) < 2:
            fail(f"{bridge_id} needs at least two falsifiers")
        if not isinstance(row["validation_handoff"], list) or not row["validation_handoff"]:
            fail(f"{bridge_id} needs validation handoff skills")
        all_handoffs.update(str(skill) for skill in row["validation_handoff"])
        joined = " ".join(str(row.get(field, "")).lower() for field in ["title", "proof_obligation", "bridge_abstraction", "validation_handoff"])
        has_no_go = has_no_go or "no-go" in joined or "impossibility" in joined
        has_symbolic = has_symbolic or "symbolic" in joined or "audit_transfer" in joined or "beta" in joined
        if "persist" not in str(row["when_to_persist"]).lower():
            fail(f"{bridge_id} persist condition must be explicit")
        if not any(word in str(row["when_to_pivot"]).lower() for word in ["pivot", "backtrack", "quarantine", "reject"]):
            fail(f"{bridge_id} pivot condition must be explicit")
    missing_handoffs = sorted(EXPECTED_SKILLS - all_handoffs)
    if missing_handoffs:
        fail(f"missing expected handoff skills: {', '.join(missing_handoffs)}")
    if not has_no_go:
        fail("expected at least one no-go or impossibility bridge")
    if not has_symbolic:
        fail("expected at least one symbolic or beta/exponent audit bridge")
    rec = payload.get("recommended_next_move")
    if not isinstance(rec, dict) or not rec.get("payoff_criterion") or not rec.get("stop_condition"):
        fail("recommended_next_move must include payoff_criterion and stop_condition")
    print(f"validated {len(candidates)} P vs NP pressure bridge candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
