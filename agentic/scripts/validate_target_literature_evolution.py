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
"""Validate the target problem and literature-evolution report."""

from __future__ import annotations

from agentic_common import clean_text, fail, load_json_object, rel
from build_target_literature_evolution import OUT_JSON, OUT_MD


REQUIRED_REF_ROLES = {
    "problem_statement",
    "origin",
    "axiomatic_bridge",
    "physics_motivation",
    "constructive_program",
    "route_obstruction",
}


def main() -> int:
    if not OUT_JSON.exists():
        fail(f"missing {rel(OUT_JSON)}")
    report = load_json_object(OUT_JSON)
    for field in [
        "target_id",
        "problem_name",
        "problem_statement",
        "why_it_matters",
        "solution_criteria",
        "literature_stages",
        "workflow_implications",
        "open_obligations",
        "references",
        "required_skills",
    ]:
        if field not in report:
            fail(f"{rel(OUT_JSON)} missing {field}")
    if "yang-mills" in clean_text(report.get("target_id")).lower():
        refs = report.get("references", [])
        if len(refs) < 8:
            fail(f"{rel(OUT_JSON)} needs at least eight references for Yang-Mills context")
        roles = {clean_text(row.get("role")) for row in refs if isinstance(row, dict)}
        missing_roles = REQUIRED_REF_ROLES.difference(roles)
        if missing_roles:
            fail(f"{rel(OUT_JSON)} references missing roles {sorted(missing_roles)}")
        ref_ids = {row.get("ref_id") for row in refs}
        for index, ref in enumerate(refs, start=1):
            for field in ["ref_id", "year", "authors", "title", "url", "role", "supports", "limitation", "status"]:
                if not ref.get(field):
                    fail(f"reference {index} missing {field}")
            if not clean_text(ref.get("url")).startswith(("https://", "http://")):
                fail(f"reference {index} has invalid URL")
        stages = report.get("literature_stages", [])
        if len(stages) < 5:
            fail(f"{rel(OUT_JSON)} needs at least five literature stages")
        for index, stage in enumerate(stages, start=1):
            for field in ["stage_id", "period", "title", "core_shift", "what_became_possible", "what_remained_open", "refs", "citations"]:
                if not stage.get(field):
                    fail(f"stage {index} missing {field}")
            for ref_id in stage.get("refs", []):
                if ref_id not in ref_ids:
                    fail(f"stage {index} cites unknown reference {ref_id}")
        text = clean_text(report).lower()
        for phrase in ["same-theory", "continuum", "reflection positivity", "mass gap", "nontrivial"]:
            if phrase not in text:
                fail(f"{rel(OUT_JSON)} missing conceptual phrase `{phrase}`")
    if "p-vs-np" in clean_text(report.get("target_id")).lower():
        refs = report.get("references", [])
        if len(refs) < 8:
            fail(f"{rel(OUT_JSON)} needs at least eight references for P vs NP context")
        ref_ids = {row.get("ref_id") for row in refs if isinstance(row, dict)}
        for index, ref in enumerate(refs, start=1):
            for field in ["ref_id", "year", "authors", "title", "url", "role", "supports", "limitation", "status"]:
                if not ref.get(field):
                    fail(f"reference {index} missing {field}")
            if not clean_text(ref.get("url")).startswith(("https://", "http://")):
                fail(f"reference {index} has invalid URL")
        stages = report.get("literature_stages", [])
        if len(stages) < 5:
            fail(f"{rel(OUT_JSON)} needs at least five literature stages")
        for index, stage in enumerate(stages, start=1):
            for field in ["stage_id", "period", "title", "core_shift", "what_became_possible", "what_remained_open", "refs", "citations"]:
                if not stage.get(field):
                    fail(f"stage {index} missing {field}")
            for ref_id in stage.get("refs", []):
                if ref_id not in ref_ids:
                    fail(f"stage {index} cites unknown reference {ref_id}")
        difficulty = report.get("why_difficult")
        if not isinstance(difficulty, dict):
            fail(f"{rel(OUT_JSON)} missing P vs NP difficulty narrative")
        if len(difficulty.get("facets", [])) < 5:
            fail(f"{rel(OUT_JSON)} P vs NP difficulty narrative needs at least five facets")
        text = clean_text(report).lower()
        for phrase in [
            "verification",
            "search",
            "relativization",
            "natural proofs",
            "algebrization",
            "advice",
            "target-preserving",
            "exponent",
        ]:
            if phrase not in text:
                fail(f"{rel(OUT_JSON)} missing P vs NP conceptual phrase `{phrase}`")
    if not set(["target-literature-source-curator", "target-literature-evolution-narrator"]).issubset(set(report.get("required_skills", []))):
        fail(f"{rel(OUT_JSON)} missing required literature skills")
    if not OUT_MD.exists():
        fail(f"missing {rel(OUT_MD)}")
    md = OUT_MD.read_text(encoding="utf-8")
    for phrase in ["Target Problem And Literature Evolution", "Literature Evolution", "Workflow Implications", "References"]:
        if phrase not in md:
            fail(f"{rel(OUT_MD)} missing `{phrase}`")
    print(f"validated {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
