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
"""Synthesize paper sections from the timeline-paper blueprint and interpretation."""

from __future__ import annotations

from agentic_common import ROOT, clean_text, load_json_object, rel, stable_id, utc_now, write_json
from build_timeline_paper_blueprint import OUT_JSON as BLUEPRINT_JSON
from build_timeline_paper_diagrams import OUT_JSON as DIAGRAM_JSON
from build_timeline_formal_derivation import OUT_JSON as DERIVATION_JSON, OUT_TEX as DERIVATION_TEX
from build_timeline_paper_interpretation import OUT_JSON as INTERPRETATION_JSON
from timeline_paper_common import latex_escape, safe_tex_math, tex_itemize


OUT_DIR = ROOT / "agentic/reports/timeline_paper_sections"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
SCHEMA = ROOT / "agentic/spec/timeline_paper_sections.schema.json"


def unit_map(units: list[dict]) -> dict[str, dict]:
    return {row["unit_id"]: row for row in units}


def summarize_units(ids: list[str], mapping: dict[str, dict], *, limit: int = 6) -> list[str]:
    rows = []
    for unit_id in ids[:limit]:
        row = mapping.get(unit_id)
        if row:
            prefix = f"{row.get('cycle_id')}: " if row.get("cycle_id") else ""
            rows.append(f"{prefix}{row.get('title')}: {row.get('content')}")
    return rows


def render_unit_items(ids: list[str], mapping: dict[str, dict], *, limit: int = 6) -> str:
    rows = []
    for unit_id in ids[:limit]:
        row = mapping.get(unit_id)
        if not row:
            continue
        prefix = f"{row.get('cycle_id')}: " if row.get("cycle_id") else ""
        title = latex_escape(f"{prefix}{row.get('title')}")
        content = row.get("content", "")
        if row.get("kind") == "equation":
            rows.append(
                "\\item "
                + title
                + "\n\\[\n"
                + safe_tex_math(content)
                + "\n\\]"
            )
        else:
            rows.append("\\item " + latex_escape(content if not title else f"{prefix}{row.get('title')}: {content}"))
    if not rows:
        return "\\begin{itemize}\n\\item None recorded.\n\\end{itemize}"
    return "\\begin{itemize}\n" + "\n".join(rows) + "\n\\end{itemize}"


def section_payload(section: dict, mapping: dict[str, dict], body: str, latex: str) -> dict:
    return {
        "section_id": section["section_id"],
        "title": section["title"],
        "purpose": section["purpose"],
        "responsible_skill": section["responsible_skill"],
        "source_unit_ids": section.get("source_unit_ids", []),
        "body": body,
        "latex": latex,
        "epistemic_status": "section_synthesis_validation_needed",
        "accepted_claims": [unit_id for unit_id in section.get("source_unit_ids", []) if mapping.get(unit_id, {}).get("argument_role") == "claim"],
        "demoted_claims": [],
        "unresolved_obligations": [unit_id for unit_id in section.get("source_unit_ids", []) if mapping.get(unit_id, {}).get("argument_role") == "validation_boundary"],
    }


def build_intro(section: dict, mapping: dict[str, dict], blueprint: dict) -> dict:
    items = summarize_units(section.get("source_unit_ids", []), mapping, limit=5)
    body = (
        f"This paper draft is organized around a bounded claim: {blueprint['abstract_claim']} "
        "The report evidence is treated as a source of mathematical objects, route pressure, and validation obligations, not as a proof by accumulation."
    )
    latex = "\\section{" + latex_escape(section["title"]) + "}\n" + latex_escape(body) + "\n" + render_unit_items(section.get("source_unit_ids", []), mapping, limit=5)
    return section_payload(section, mapping, body, latex)


def build_related(section: dict, mapping: dict[str, dict]) -> dict:
    items = summarize_units(section.get("source_unit_ids", []), mapping, limit=8)
    body = "The related-work function is to separate target formulation, standard machinery, closest comparators, and novelty boundaries."
    latex = "\\section{" + latex_escape(section["title"]) + "}\n" + latex_escape(body) + "\n" + render_unit_items(section.get("source_unit_ids", []), mapping, limit=8)
    return section_payload(section, mapping, body, latex)


def build_route_learning(section: dict, mapping: dict[str, dict]) -> dict:
    items = summarize_units(section.get("source_unit_ids", []), mapping, limit=8)
    body = "The route history is included only where it explains why the paper object became narrower and more testable."
    latex = "\\section{" + latex_escape(section["title"]) + "}\n" + latex_escape(body) + "\n" + render_unit_items(section.get("source_unit_ids", []), mapping, limit=8)
    return section_payload(section, mapping, body, latex)


def build_formal_core(section: dict, mapping: dict[str, dict]) -> dict:
    derivation_tex = DERIVATION_TEX.read_text(encoding="utf-8") if DERIVATION_TEX.exists() else "\\section{Formal Physics Derivation}\nMissing derivation artifact."
    body = "The formal core is imported from the structured derivation artifact, preserving definitions, assumptions, propositions, validity conditions, and unresolved obligations."
    payload = section_payload(section, mapping, body, derivation_tex)
    payload["unresolved_obligations"].extend(["timeline_formal_derivation"])
    return payload


def build_worked(section: dict, mapping: dict[str, dict]) -> dict:
    items = summarize_units(section.get("source_unit_ids", []), mapping, limit=10)
    body = "The worked-calculation section records what is computable now and what exact transfer, threshold, falsifier, or remainder test would decide promotion or demotion."
    latex = "\\section{" + latex_escape(section["title"]) + "}\n" + latex_escape(body) + "\n" + render_unit_items(section.get("source_unit_ids", []), mapping, limit=10)
    return section_payload(section, mapping, body, latex)


def build_mechanism(section: dict, mapping: dict[str, dict], diagrams: dict) -> dict:
    items = summarize_units(section.get("source_unit_ids", []), mapping, limit=6)
    tikz = diagrams.get("diagrams", [{}])[0].get("tikz", "") if diagrams.get("diagrams") else ""
    body = "The mechanism section uses the generated diagram as an explanatory map from target commitments to local criterion and validation handoff."
    latex = "\\section{" + latex_escape(section["title"]) + "}\n" + latex_escape(body) + "\n" + render_unit_items(section.get("source_unit_ids", []), mapping, limit=6) + "\n" + tikz
    return section_payload(section, mapping, body, latex)


def build_discussion(section: dict, mapping: dict[str, dict], blueprint: dict) -> dict:
    items = summarize_units(section.get("source_unit_ids", []), mapping, limit=8)
    body = "The discussion states what has been learned, what is not claimed, and what validation handoff remains before any stronger result could be asserted."
    latex = (
        "\\section{" + latex_escape(section["title"]) + "}\n"
        + latex_escape(body)
        + "\n\\subsection*{Non-claims}\n"
        + tex_itemize(blueprint.get("non_claims", []))
        + "\n\\subsection*{Validation and Future Work}\n"
        + render_unit_items(section.get("source_unit_ids", []), mapping, limit=8)
    )
    return section_payload(section, mapping, body, latex)


def build_report() -> dict:
    interpretation = load_json_object(INTERPRETATION_JSON)
    blueprint = load_json_object(BLUEPRINT_JSON)
    derivation = load_json_object(DERIVATION_JSON)
    diagrams = load_json_object(DIAGRAM_JSON)
    mapping = unit_map(interpretation["units"])
    builders = {
        "introduction": lambda section: build_intro(section, mapping, blueprint),
        "related_work": lambda section: build_related(section, mapping),
        "route_learning": lambda section: build_route_learning(section, mapping),
        "formal_core": lambda section: build_formal_core(section, mapping),
        "worked_example": lambda section: build_worked(section, mapping),
        "mechanism": lambda section: build_mechanism(section, mapping, diagrams),
        "discussion": lambda section: build_discussion(section, mapping, blueprint),
    }
    sections = [builders.get(row["section_id"], lambda section: build_related(section, mapping))(row) for row in blueprint["sections"]]
    appendix_sections = [
        {
            "section_id": "appendix_evidence_map",
            "title": "Appendix Evidence Map",
            "source_unit_ids": blueprint.get("appendix_unit_ids", [])[:80],
            "latex": "\\appendix\n\\section{Appendix Evidence Map}\n"
            + "The appendix preserves interpreted report evidence without letting chronology control the main paper argument.\n"
            + render_unit_items(blueprint.get("appendix_unit_ids", []), mapping, limit=40),
        }
    ]
    accepted = [claim["claim_id"] for claim in blueprint.get("contribution_claims", [])]
    report = {
        "version": 1,
        "generated_utc": utc_now(),
        "schema": rel(SCHEMA),
        "target_id": clean_text(blueprint.get("target_id") or interpretation.get("target_id")),
        "status": "timeline_paper_sections_ready",
        "sections_id": stable_id("timeline-paper-sections", blueprint.get("blueprint_id"), len(sections)),
        "source_blueprint": rel(BLUEPRINT_JSON),
        "source_interpretation": rel(INTERPRETATION_JSON),
        "source_formal_derivation": rel(DERIVATION_JSON),
        "source_diagrams": rel(DIAGRAM_JSON),
        "sections": sections,
        "appendix_sections": appendix_sections,
        "cross_section_reconciliation": {
            "accepted_claims": accepted,
            "demoted_claims": [],
            "duplicate_definitions": [],
            "dangling_references": [],
            "unresolved_obligations": derivation.get("unresolved_obligations", []),
        },
        "artifacts": {"json": rel(OUT_JSON), "markdown": rel(OUT_MD)},
        "epistemic_status": "paper_sections_validation_needed",
        "validation_handoff": "python agentic/scripts/validate_timeline_paper_sections.py",
    }
    return report


def render_markdown(report: dict) -> str:
    lines = ["# Timeline Paper Sections", "", f"- Status: `{report['status']}`", "", "## Sections", ""]
    for row in report["sections"]:
        lines.append(f"- `{row['section_id']}` {row['title']} via `{row['responsible_skill']}` using {len(row['source_unit_ids'])} units")
    lines.extend(["", "## Reconciliation", "", f"- Accepted claims: `{len(report['cross_section_reconciliation']['accepted_claims'])}`", f"- Unresolved obligations: `{len(report['cross_section_reconciliation']['unresolved_obligations'])}`"])
    return "\n".join(lines) + "\n"


def main() -> int:
    report = build_report()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_JSON, report)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
