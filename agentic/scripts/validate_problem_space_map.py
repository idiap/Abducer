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
"""Validate the target-specific problem-space map."""

from __future__ import annotations

from agentic_common import ROOT, clean_text, fail, load_json_object, rel
from target_profiles import target_profile


REPORT = ROOT / "agentic/reports/problem_space_map/latest.json"
ALLOWED_STATUS = {"achieved", "partially_achieved", "open", "blocked", "quarantined", "not_started"}


def main() -> int:
    if not REPORT.exists():
        fail(f"missing {rel(REPORT)}")
    report = load_json_object(REPORT)
    for field in ["version", "generated_utc", "target_id", "source_atlas", "summary", "global_problem", "nodes", "validation_handoff"]:
        if not report.get(field):
            fail(f"{rel(REPORT)} missing {field}")
    target_id = clean_text(report.get("target_id"))
    nodes = report.get("nodes", [])
    if not isinstance(nodes, list) or len(nodes) < 5:
        fail(f"{rel(REPORT)} needs at least five problem-space nodes")
    for index, node in enumerate(nodes, start=1):
        for field in ["node_id", "target_id", "route_family", "title", "status", "result_ids", "achieved_summary", "open_obligations", "next_achievement", "why_it_matters"]:
            if field not in node or (field != "result_ids" and not node.get(field)):
                fail(f"{rel(REPORT)} node {index} missing {field}")
        if node.get("target_id") != target_id:
            fail(f"{rel(REPORT)} node {index} target mismatch")
        if node.get("status") not in ALLOWED_STATUS:
            fail(f"{rel(REPORT)} node {index} invalid status {node.get('status')}")
        if node.get("status") in {"achieved", "partially_achieved"} and not node.get("result_ids"):
            fail(f"{rel(REPORT)} node {index} has achieved/partial status without result links")
    text = clean_text(report).lower()
    forbidden = [term for term in target_profile(target_id).get("forbidden_cross_target_terms", []) if term in text]
    if forbidden:
        fail(f"{rel(REPORT)} contains cross-target terms: {sorted(set(forbidden))}")
    if target_id == "p-vs-np-target":
        for phrase in ["hardness", "mcsp", "proof-complexity", "padding", "all-exponent"]:
            if phrase not in text:
                fail(f"{rel(REPORT)} P vs NP map lacks `{phrase}`")
    print(f"validated {rel(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
