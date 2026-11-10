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
"""Validate the timeline-paper argument blueprint."""

from __future__ import annotations

from agentic_common import clean_text, fail, load_json_object, rel, repo_path
from build_timeline_paper_blueprint import OUT_JSON, OUT_MD


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    require(OUT_JSON.exists(), f"missing {rel(OUT_JSON)}")
    report = load_json_object(OUT_JSON)
    require(report.get("status") == "timeline_paper_blueprint_ready", "blueprint not ready")
    require(report.get("paper_mode") in {"theorem_note", "worked_calculation_note", "obstruction_note", "method_note", "negative_result_note", "survey_positioning_note"}, "invalid paper mode")
    for field in ["title", "abstract_claim", "main_thesis", "primary_mathematical_object"]:
        require(clean_text(report.get(field)), f"blueprint missing {field}")
    claims = report.get("contribution_claims", [])
    require(isinstance(claims, list) and claims, "blueprint needs contribution claims")
    for claim in claims:
        for field in ["claim_id", "claim", "evidence_units", "validation_burden_units", "non_claim"]:
            require(claim.get(field), f"claim missing {field}")
    sections = report.get("sections", [])
    require(isinstance(sections, list) and len(sections) >= 6, "blueprint needs a complete section plan")
    for section in sections:
        for field in ["section_id", "title", "purpose", "source_unit_ids", "responsible_skill"]:
            require(section.get(field), f"section missing {field}")
    budget = report.get("narrative_budget", {})
    for field in ["max_main_cycles", "max_failed_routes", "max_core_equations", "max_open_obligations", "max_future_work_items", "appendix_policy"]:
        require(budget.get(field), f"narrative budget missing {field}")
    require(report.get("body_unit_ids"), "blueprint needs body unit partition")
    require(report.get("appendix_unit_ids"), "blueprint needs appendix unit partition")
    require(report.get("future_work_unit_ids"), "blueprint needs future-work unit partition")
    require(len(report.get("non_claims", [])) >= 3, "blueprint needs explicit non-claims")
    require(report.get("claim_reference_map"), "blueprint needs claim-reference map")
    repo_path(str(report.get("artifacts", {}).get("markdown")), must_exist=True)
    require("Section Responsibilities" in OUT_MD.read_text(encoding="utf-8"), "blueprint markdown missing section responsibilities")
    print(f"validated {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
