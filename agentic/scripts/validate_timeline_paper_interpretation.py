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
"""Validate the timeline-paper interpretation IR."""

from __future__ import annotations

from agentic_common import clean_text, fail, load_json_object, rel, repo_path
from timeline_paper_common import REPORT_FAMILIES
from build_timeline_paper_interpretation import OUT_JSON, OUT_MD


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    require(OUT_JSON.exists(), f"missing {rel(OUT_JSON)}")
    report = load_json_object(OUT_JSON)
    require(report.get("status") == "timeline_paper_interpretation_ready", "interpretation report is not ready")
    units = report.get("units", [])
    require(isinstance(units, list) and len(units) >= 40, "interpretation needs a substantive unit set")
    required_fields = {"unit_id", "family", "kind", "title", "content", "argument_role", "disposition", "source", "evidence_status"}
    valid_dispositions = {"main_body", "appendix", "future_work", "quarantine"}
    roles = set()
    for index, row in enumerate(units, start=1):
        require(isinstance(row, dict), f"unit {index} must be an object")
        missing = required_fields - set(row)
        require(not missing, f"unit {index} missing fields: {sorted(missing)}")
        for field in required_fields:
            require(clean_text(row.get(field)), f"unit {index} field {field} must not be empty")
        require(row["disposition"] in valid_dispositions, f"unit {index} invalid disposition {row['disposition']}")
        roles.add(row["argument_role"])
    for needed in ["motivation", "claim", "proof_step", "validation_boundary", "future_work"]:
        require(needed in roles, f"interpretation missing argument role {needed}")
    functions = report.get("required_argument_functions", {})
    for key in ["has_active_object", "has_contribution_candidate", "has_formal_derivation_material", "has_validation_boundary"]:
        require(functions.get(key) is True, f"interpretation required function failed: {key}")
    coverage = report.get("report_family_coverage", {}).get("families", {})
    for family in REPORT_FAMILIES:
        require(family in coverage, f"coverage missing family {family}")
        row = coverage[family]
        if row.get("present"):
            require(row.get("unit_count", 0) > 0, f"present report family {family} has no interpreted units")
            require(row.get("dispositions"), f"present report family {family} has no disposition accounting")
    require(not report.get("report_family_coverage", {}).get("missing_report_material"), "some report material lacks disposition")
    for key in ["json", "markdown"]:
        repo_path(str(report.get("artifacts", {}).get(key)), must_exist=True)
    require(OUT_MD.exists() and "Report Family Coverage" in OUT_MD.read_text(encoding="utf-8"), "markdown coverage summary missing")
    print(f"validated {rel(OUT_JSON)} with {len(units)} interpreted units")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
