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
"""Forward-evaluate the interpretive timeline-paper workflow on current artifacts."""

from __future__ import annotations

from agentic_common import ROOT, fail, load_json_object, rel, write_json


OUT_DIR = ROOT / "agentic/reports/timeline_paper_forward_eval"
OUT_JSON = OUT_DIR / "latest.json"
FIXTURE = ROOT / "agentic/evals/timeline_paper/current_yang_mills_fixture.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    interpretation = load_json_object(ROOT / "agentic/reports/timeline_paper_interpretation/latest.json")
    blueprint = load_json_object(ROOT / "agentic/reports/timeline_paper_blueprint/latest.json")
    sections = load_json_object(ROOT / "agentic/reports/timeline_paper_sections/latest.json")
    paper = load_json_object(ROOT / "agentic/reports/timeline_paper/latest.json")
    checks = {
        "uses_full_report_families": len(interpretation.get("report_family_coverage", {}).get("families", {})) >= 12,
        "has_bounded_paper_mode": blueprint.get("paper_mode") in {"obstruction_note", "worked_calculation_note", "theorem_note", "method_note"},
        "has_formal_core": any(row.get("section_id") == "formal_core" for row in sections.get("sections", [])),
        "has_claim_boundaries": bool(blueprint.get("non_claims")) and bool(sections.get("cross_section_reconciliation", {}).get("accepted_claims")),
        "paper_pdf_exists": (ROOT / paper.get("artifacts", {}).get("pdf", "")).exists(),
    }
    report = {
        "version": 1,
        "status": "timeline_paper_forward_eval_pass" if all(checks.values()) else "timeline_paper_forward_eval_fail",
        "fixture": rel(FIXTURE),
        "checks": checks,
        "repair_tasks": [
            key for key, value in checks.items() if not value
        ],
        "artifacts": {"json": rel(OUT_JSON)},
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_JSON, report)
    require(all(checks.values()), f"forward eval failed: {report['repair_tasks']}")
    print(f"validated forward eval {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
