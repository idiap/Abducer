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
"""Validate synthesized timeline-paper sections."""

from __future__ import annotations

from agentic_common import clean_text, fail, load_json_object, rel, repo_path
from build_timeline_paper_sections import OUT_JSON, OUT_MD


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    require(OUT_JSON.exists(), f"missing {rel(OUT_JSON)}")
    report = load_json_object(OUT_JSON)
    require(report.get("status") == "timeline_paper_sections_ready", "paper sections not ready")
    sections = report.get("sections", [])
    require(isinstance(sections, list) and len(sections) >= 6, "paper needs synthesized main sections")
    for row in sections:
        for field in ["section_id", "title", "purpose", "responsible_skill", "source_unit_ids", "body", "latex", "epistemic_status"]:
            require(row.get(field), f"section {row.get('section_id')} missing {field}")
        require("section" in row["latex"].lower(), f"section {row['section_id']} TeX lacks section marker")
    recon = report.get("cross_section_reconciliation", {})
    require(recon.get("accepted_claims"), "reconciliation needs accepted claims")
    require("duplicate_definitions" in recon and "dangling_references" in recon, "reconciliation missing duplicate/dangling checks")
    require(report.get("appendix_sections"), "paper sections need bounded appendix section")
    repo_path(str(report.get("artifacts", {}).get("markdown")), must_exist=True)
    require("Reconciliation" in OUT_MD.read_text(encoding="utf-8"), "sections markdown missing reconciliation")
    all_tex = "\n".join(row["latex"] for row in sections)
    for phrase in ["Problem Pressure", "Claim Boundary"]:
        require(phrase in all_tex, f"main sections missing {phrase}")
    require("Formal " in all_tex and " Derivation" in all_tex, "main sections missing formal derivation")
    print(f"validated {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
