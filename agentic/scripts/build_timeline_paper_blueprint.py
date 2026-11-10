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
"""Build a paper argument blueprint from the interpreted timeline report."""

from __future__ import annotations

from agentic_common import ROOT, clean_text, load_json_object, rel, stable_id, utc_now, write_json
from build_timeline_paper_interpretation import OUT_JSON as INTERPRETATION_JSON
from target_profiles import target_profile
from timeline_paper_common import tex_itemize


OUT_DIR = ROOT / "agentic/reports/timeline_paper_blueprint"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
SCHEMA = ROOT / "agentic/spec/timeline_paper_blueprint.schema.json"


def by_role(units: list[dict], *roles: str) -> list[dict]:
    return [row for row in units if row.get("argument_role") in roles]


def top_units(units: list[dict], *, disposition: str | None = None, limit: int = 8) -> list[dict]:
    rows = [row for row in units if disposition is None or row.get("disposition") == disposition]
    rows.sort(key=lambda row: (int(row.get("score", 0) or 0), row.get("cycle_id", "")), reverse=True)
    return rows[:limit]


def infer_paper_mode(units: list[dict]) -> str:
    text = " ".join(row.get("content", "") for row in units).lower()
    if "obstruction" in text or "falsifier" in text or "positivity" in text:
        return "obstruction_note"
    if "calculation" in text or "compute" in text:
        return "worked_calculation_note"
    if "theorem" in text or "proposition" in text:
        return "theorem_note"
    return "method_note"


def section(section_id: str, title: str, purpose: str, unit_ids: list[str], skill: str) -> dict:
    return {
        "section_id": section_id,
        "title": title,
        "purpose": purpose,
        "source_unit_ids": unit_ids,
        "responsible_skill": skill,
    }


def build_report() -> dict:
    interpretation = load_json_object(INTERPRETATION_JSON)
    profile = target_profile(interpretation.get("target_id"))
    units = interpretation.get("units", [])
    main_units = top_units(units, disposition="main_body", limit=40)
    appendix_units = top_units(units, disposition="appendix", limit=80)
    future_units = top_units(units, disposition="future_work", limit=24)
    claim_units = by_role(units, "claim")
    object_units = interpretation.get("active_mathematical_objects", [])[:12]
    validation_units = by_role(units, "validation_boundary")[:18]
    proof_units = by_role(units, "proof_step", "calculation_input", "calculation_result")[:30]
    contribution_claims = []
    for row in claim_units[:5]:
        contribution_claims.append(
            {
                "claim_id": stable_id("paper-claim", row["unit_id"]),
                "claim": row["content"],
                "source_unit_ids": [row["unit_id"]],
                "evidence_units": [row["unit_id"]] + [item["unit_id"] for item in proof_units[:4]],
                "novelty_boundary_units": [item["unit_id"] for item in by_role(units, "novelty_boundary")[:4]],
                "validation_burden_units": [item["unit_id"] for item in validation_units[:4]],
                "non_claim": "This is not a proof of the target theorem; it is a bounded paper-level contribution candidate.",
            }
        )
    if not contribution_claims and object_units:
        contribution_claims.append(
            {
                "claim_id": stable_id("paper-claim", object_units[0]["unit_id"]),
                "claim": "The timeline isolates a bounded mathematical object and validation handoff suitable for a scoped paper note.",
                "source_unit_ids": [object_units[0]["unit_id"]],
                "evidence_units": [item["unit_id"] for item in object_units[:3]],
                "novelty_boundary_units": [],
                "validation_burden_units": [item["unit_id"] for item in validation_units[:3]],
                "non_claim": "This does not solve the global target.",
            }
        )
    paper_mode = infer_paper_mode(units)
    if profile["target_id"] == "p-vs-np-target":
        title = "Route-Specific Transfer Obstructions and Certificate Gates in P vs NP Exploration"
        abstract_claim = (
            "The report-derived paper should claim a scoped complexity-theoretic bridge or no-go result, "
            "not a solution of P vs NP."
        )
        thesis = (
            "The timeline supports a bounded complexity-theory paper centered on target-preserving transfer control: "
            "state the source carrier and target class, derive the exact exponent or certificate gate, expose the "
            "uniformity/advice/barrier disqualifiers, and identify which route families are ruled out, repaired, or "
            "left as live proof obligations."
        )
        non_claims = [
            "The paper does not prove P != NP.",
            "The paper does not prove SAT is outside P/poly.",
            "A route-level transfer obstruction is not a target separation theorem.",
            "Artifact evidence documents the run state; external novelty still requires a prior-art boundary.",
        ]
        formal_skill = "pvsnp-proof-derivation-builder"
        worked_skill = "pvsnp-symbolic-complexity-auditor"
        mechanism_title = "Mechanism And Transfer Diagram"
        reference_roles = ["target_statement", "standard_complexity_reference", "closest_comparator", "artifact_evidence"]
        unresolved_reference_queue = [
            "closest comparator for the route-specific transfer-envelope obstruction and certificate-gate result"
        ]
    elif profile["target_id"] == "yang-mills-existence-and-mass-gap-target":
        title = "A Finite Reflection-Positivity Obstruction Program Extracted From a Discovery Timeline"
        abstract_claim = "The report-derived paper should claim a scoped finite obstruction or bridge criterion, not a solution of the main target."
        thesis = (
            "The timeline supports a bounded physics paper centered on a finite reflected-observable obstruction program: "
            "state the target pressure, define the active mathematical object, prove or package the local finite criterion, "
            "explain the worked calculation and failures, and state the same-theory validation debt."
        )
        non_claims = [
            "The paper does not claim Yang-Mills existence.",
            "The paper does not claim a mass gap.",
            "A finite reflected matrix obstruction is not automatically a continuum theorem.",
            "Artifact evidence documents the run state; it is not external literature.",
        ]
        formal_skill = "timeline-formal-physics-deriver"
        worked_skill = "endpoint-worked-calculation-packager"
        mechanism_title = "Mechanism And Organizing Diagram"
        reference_roles = ["target_statement", "standard_os_reconstruction", "closest_comparator", "artifact_evidence"]
        unresolved_reference_queue = ["closest comparator for the exact finite Wilson/OS obstruction packet"]
    else:
        title = f"A Target-Preserving Obstruction Program for {profile['display_name']}"
        abstract_claim = "The report-derived paper should claim a scoped bridge, obstruction, or method result, not a solution of the whole target."
        thesis = (
            "The timeline supports a bounded paper centered on a target-preserving mathematical object, a local proof or "
            "falsifier, and an explicit validation boundary."
        )
        non_claims = [
            "The paper does not claim the global target theorem.",
            "A route-level result is not automatically a target proof.",
            "Artifact evidence documents the run state; external novelty still requires a prior-art boundary.",
        ]
        formal_skill = "results-proof-packet-deriver"
        worked_skill = "results-finite-object-formalizer"
        mechanism_title = "Mechanism And Organizing Diagram"
        reference_roles = ["target_statement", "standard_reference", "closest_comparator", "artifact_evidence"]
        unresolved_reference_queue = ["closest comparator for the scoped target-preserving obstruction packet"]
    sections = [
        section("introduction", "Problem Pressure And Paper Claim", "Motivate the target and state the bounded claim.", [row["unit_id"] for row in by_role(units, "motivation", "claim")[:10]], "timeline-problem-space-narrator"),
        section("related_work", "Literature And Novelty Boundary", "Explain what is standard and where the paper contribution begins.", [row["unit_id"] for row in by_role(units, "novelty_boundary")[:12]], "timeline-reference-manager"),
        section("route_learning", "Route Narrowing And Scientific Learning", "Explain why earlier strategies narrowed into the active object.", [row["unit_id"] for row in by_role(units, "failure_learning")[:12]], "timeline-failed-route-interpreter"),
        section("formal_core", "Formal Object And Local Criterion", "State definitions, assumptions, proposition/calculation, and proof boundary.", [row["unit_id"] for row in proof_units[:14]], formal_skill),
        section("worked_example", "Worked Calculation And Falsifier Tests", "Expose the computable evidence and what would decide the branch.", [row["unit_id"] for row in proof_units[14:28] + validation_units[:8]], worked_skill),
        section("mechanism", mechanism_title, "Show how the problem, local criterion, and transfer obligations relate.", [row["unit_id"] for row in by_role(units, "mechanism")[:10] + object_units[:6]], "timeline-organizing-diagram-builder"),
        section("discussion", "Claim Boundary And Validation Handoff", "State implications, non-claims, future work, and stop/demotion conditions.", [row["unit_id"] for row in validation_units[:12] + future_units[:8]], "timeline-claim-boundary-auditor"),
    ]
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "schema": rel(SCHEMA),
        "status": "timeline_paper_blueprint_ready",
        "blueprint_id": stable_id("timeline-paper-blueprint", interpretation.get("interpretation_id"), paper_mode),
        "target_id": profile["target_id"],
        "target_display_name": profile["display_name"],
        "source_interpretation": rel(INTERPRETATION_JSON),
        "paper_mode": paper_mode,
        "title": title,
        "abstract_claim": abstract_claim,
        "main_thesis": thesis,
        "primary_mathematical_object": clean_text(object_units[0].get("title") if object_units else "active timeline mathematical object"),
        "active_object_unit_ids": [row["unit_id"] for row in object_units],
        "contribution_claims": contribution_claims,
        "sections": sections,
        "body_unit_ids": [row["unit_id"] for row in main_units],
        "appendix_unit_ids": [row["unit_id"] for row in appendix_units],
        "future_work_unit_ids": [row["unit_id"] for row in future_units],
        "quarantine_unit_ids": [row["unit_id"] for row in top_units(units, disposition="quarantine", limit=20)],
        "narrative_budget": {
            "max_main_cycles": 12,
            "max_failed_routes": 4,
            "max_core_equations": 10,
            "max_open_obligations": 8,
            "max_future_work_items": 6,
            "appendix_policy": "Preserve full report evidence by source unit and translated report packets, but keep the main body argumentative.",
        },
        "claim_reference_map": [
            {
                "claim_id": claim["claim_id"],
                "reference_roles": reference_roles,
                "unresolved_reference_queue": unresolved_reference_queue,
            }
            for claim in contribution_claims
        ],
        "non_claims": non_claims,
        "validation_handoff": "Run validate_timeline_paper_blueprint.py, then build sections, derivation, diagrams, TeX, and PDF.",
        "epistemic_status": "blueprint_ready_validation_needed",
        "artifacts": {"json": rel(OUT_JSON), "markdown": rel(OUT_MD)},
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Timeline Paper Blueprint",
        "",
        f"- Status: `{report['status']}`",
        f"- Mode: `{report['paper_mode']}`",
        f"- Primary object: {report['primary_mathematical_object']}",
        "",
        "## Main Thesis",
        "",
        report["main_thesis"],
        "",
        "## Contribution Claims",
        "",
    ]
    for claim in report["contribution_claims"]:
        lines.append(f"- `{claim['claim_id']}` {claim['claim']}")
    lines.extend(["", "## Section Responsibilities", ""])
    for row in report["sections"]:
        lines.append(f"- `{row['section_id']}` via `{row['responsible_skill']}`: {row['purpose']} ({len(row['source_unit_ids'])} units)")
    lines.extend(["", "## Non-Claims", "", tex_itemize(report["non_claims"])])
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
