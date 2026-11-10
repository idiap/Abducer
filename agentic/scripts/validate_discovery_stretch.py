#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Validate the large-stretch Yang-Mills discovery exploration report."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


REPORT = ROOT / "agentic/reports/discovery_stretch/latest.json"
TARGET_ID = "yang-mills-existence-and-mass-gap-target"
REQUIRED_MARKERS = [
    "yang-mills",
    "gauge",
    "schwinger",
    "os",
    "hamiltonian",
    "spectral",
    "continuum",
    "observable",
]
FORBIDDEN_GENERIC = [
    "factor the opaque obligation",
    "smaller lemmas, evidence tasks, or discovery branches",
    "use advanced mathematics",
]


def require_fields(row: dict[str, Any], fields: list[str], subject: str) -> None:
    for field in fields:
        if field not in row:
            fail(f"{rel(REPORT)} {subject} missing `{field}`")


def main() -> int:
    report = load_json_object(REPORT)
    require_fields(
        report,
        [
            "version",
            "generated_utc",
            "target_id",
            "quality_gate",
            "source_artifacts",
            "stretch_thesis",
            "programs",
            "role_counts",
            "synthesis",
            "next_run_queue",
        ],
        "report",
    )
    if report["target_id"] != TARGET_ID:
        fail(f"{rel(REPORT)} target_id must be {TARGET_ID}")
    if report["quality_gate"] != "pass":
        fail(f"{rel(REPORT)} quality_gate must be pass")
    if report.get("long_horizon_quality") != "pass":
        fail(f"{rel(REPORT)} must be built on a passing long-horizon report")
    programs = report.get("programs", [])
    if not isinstance(programs, list) or len(programs) < 6:
        fail(f"{rel(REPORT)} requires at least six discovery programs")
    role_counts = report.get("role_counts", {})
    for role in ["invariant_preservation", "transfer", "witness", "validation", "obstruction"]:
        if role_counts.get(role, 0) < 1:
            fail(f"{rel(REPORT)} missing discovery role coverage: {role}")
    full_text = clean_text(report).lower()
    for marker in REQUIRED_MARKERS:
        if marker not in full_text:
            fail(f"{rel(REPORT)} lacks domain marker `{marker}`")
    for phrase in FORBIDDEN_GENERIC:
        if phrase in full_text:
            fail(f"{rel(REPORT)} contains generic stale phrase `{phrase}`")
    seen_ids = set()
    for index, item in enumerate(programs, start=1):
        if not isinstance(item, dict):
            fail(f"{rel(REPORT)} program {index} must be an object")
        require_fields(
            item,
            [
                "program_id",
                "title",
                "machinery_role",
                "hypothesis",
                "mathematical_mechanism",
                "controlled_interface",
                "equations",
                "dependencies",
                "falsifiers",
                "next_experiments",
                "expected_learning",
                "promotion_signal",
                "pivot_signal",
                "status",
            ],
            f"program {index}",
        )
        if item["program_id"] in seen_ids:
            fail(f"{rel(REPORT)} duplicate program_id {item['program_id']}")
        seen_ids.add(item["program_id"])
        if "->" not in item["controlled_interface"]:
            fail(f"{rel(REPORT)} program {index} controlled_interface must contain an arrow")
        for field in ["hypothesis", "mathematical_mechanism", "expected_learning", "promotion_signal", "pivot_signal"]:
            if len(clean_text(item[field]).split()) < 8:
                fail(f"{rel(REPORT)} program {index} field `{field}` is too shallow")
        for field in ["dependencies", "falsifiers", "next_experiments"]:
            if not isinstance(item[field], list) or len(item[field]) < 3:
                fail(f"{rel(REPORT)} program {index} needs at least three `{field}`")
        equations = item["equations"]
        if not isinstance(equations, list) or len(equations) < 2:
            fail(f"{rel(REPORT)} program {index} needs at least two equations")
        for equation in equations:
            if not isinstance(equation, dict):
                fail(f"{rel(REPORT)} program {index} equation must be an object")
            for field in ["label", "latex", "valid_when"]:
                if not clean_text(equation.get(field)):
                    fail(f"{rel(REPORT)} program {index} equation missing `{field}`")
            if len(clean_text(equation["valid_when"]).split()) < 8:
                fail(f"{rel(REPORT)} program {index} equation validity condition is too shallow")
    if len(report.get("next_run_queue", [])) < 3:
        fail(f"{rel(REPORT)} next_run_queue needs at least three actions")
    print(f"validated discovery stretch with {len(programs)} programs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
