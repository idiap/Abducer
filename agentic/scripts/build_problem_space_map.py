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
"""Build a target-specific problem-space map from the result atlas."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, utc_now, write_json
from discovery_marathon_common import write_markdown
from target_profiles import target_profile


ATLAS = ROOT / "agentic/reports/result_subgoal_atlas/latest.json"
OUT_DIR = ROOT / "agentic/reports/problem_space_map"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"


PVSNP_NODES = [
    ("hardness_magnification", "Hardness Magnification And Threshold Transfer", "Compute exact beta/q/exponent transfer and determine whether all-exponent strength survives."),
    ("natural_property_barrier", "Natural-Property And Barrier Analysis", "Type naturalness, relativization, algebrization, oracle, and advice status for each lower-bound object."),
    ("mcsp_mktp_carrier", "MCSP/MKtP Carrier Transfer", "Find advice-free searchable certificates or falsify row-selection leakage."),
    ("proof_complexity_transfer", "Proof-Complexity Transfer", "Show whether proof lower bounds transfer to language/circuit lower bounds."),
    ("padding_projection", "Padding Projection And Sparse Valid-Length Debt", "Decide whether padding moves proof debt into target-equivalent sparse lengths."),
    ("all_exponent_uniformity", "All-Exponent Uniformity Lift", "Lift bounded-window evidence to cofinal all-exponent P/poly consequences."),
]

YM_NODES = [
    ("finite_os_obstruction", "Finite OS Obstruction", "Prove and apply finite Schur-Feshbach/OS positivity obstruction criteria."),
    ("wilson_collar_calculation", "Wilson Collar Calculation", "Compute concrete Wilson collar or hairpin terms that decide finite positivity gates."),
    ("same_theory_transfer", "Same-Theory Transfer", "Certify transfer from finite Wilson observables to the same continuum Yang-Mills theory."),
    ("constructive_continuum_control", "Constructive Continuum Control", "Control cutoff, volume, limits, and remainders for existence."),
    ("spectral_reconstruction", "Spectral Reconstruction", "Bridge Euclidean data to Hilbert-space vacuum and mass-gap claims."),
    ("nontriviality_witness", "Nontriviality Witness", "Show the constructed theory remains interacting and nontrivial."),
]


def node_status(results: list[dict[str, Any]]) -> str:
    statuses = {clean_text(row.get("achievement_status")) for row in results}
    if "handoff_ready" in statuses or "achieved" in statuses:
        return "achieved"
    if "partially_achieved" in statuses:
        return "partially_achieved"
    if "blocked" in statuses:
        return "blocked"
    if "quarantined" in statuses or "falsified" in statuses:
        return "quarantined"
    if "open" in statuses:
        return "open"
    return "not_started"


def target_safe_atlas(atlas: dict[str, Any] | None = None, target_id: str | None = None) -> dict[str, Any]:
    requested_target = clean_text(target_id)
    candidate = dict(atlas) if isinstance(atlas, dict) and atlas else load_optional_json(ATLAS)
    candidate_target = clean_text(candidate.get("target_id"))
    if requested_target and candidate_target != requested_target:
        from build_result_subgoal_atlas import build_atlas

        candidate = build_atlas(requested_target)
    return candidate


def build_map(atlas: dict[str, Any] | None = None, target_id: str | None = None) -> dict[str, Any]:
    atlas = target_safe_atlas(atlas, target_id)
    target_id = clean_text(target_id) or clean_text(atlas.get("target_id"))
    profile = target_profile(target_id)
    node_defs = PVSNP_NODES if target_id == "p-vs-np-target" else YM_NODES
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for result in atlas.get("results", []) if isinstance(atlas.get("results"), list) else []:
        family = clean_text(result.get("problem_space_coordinates", {}).get("route_family"))
        by_family[family].append(result)
    nodes = []
    for family, title, next_achievement in node_defs:
        rows = by_family.get(family, [])
        obligations = sorted({item for row in rows for item in row.get("open_obligations", []) if clean_text(item)})
        nodes.append(
            {
                "node_id": f"{target_id}.{family}",
                "target_id": target_id,
                "route_family": family,
                "title": title,
                "status": node_status(rows),
                "result_ids": [row.get("result_id") for row in rows],
                "achieved_summary": clean_text(rows[0].get("claim")) if rows else "No durable result has been archived for this route family yet.",
                "open_obligations": obligations[:8] or [next_achievement],
                "next_achievement": next_achievement,
                "why_it_matters": rows[0].get("problem_space_coordinates", {}).get("global_problem_role") if rows else next_achievement,
            }
        )
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": target_id,
        "target_display_name": profile.get("display_name", target_id),
        "source_atlas": rel(ATLAS),
        "summary": {
            "node_count": len(nodes),
            "achieved_or_partial": sum(1 for node in nodes if node["status"] in {"achieved", "partially_achieved"}),
            "open_or_not_started": sum(1 for node in nodes if node["status"] in {"open", "not_started"}),
            "blocked_or_quarantined": sum(1 for node in nodes if node["status"] in {"blocked", "quarantined"}),
        },
        "global_problem": {
            "target_id": target_id,
            "display_name": profile.get("display_name", target_id),
            "decisive_invariant": profile.get("decisive_target_invariant", ""),
        },
        "nodes": nodes,
        "validation_handoff": ["agentic/scripts/validate_problem_space_map.py"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Problem Space Map",
        "",
        f"- Target: `{report.get('target_id', '')}`",
        "",
    ]
    for node in report.get("nodes", []):
        lines.extend(
            [
                f"## {node.get('title')}",
                "",
                f"- Status: `{node.get('status')}`",
                f"- Why it matters: {node.get('why_it_matters')}",
                f"- Next achievement: {node.get('next_achievement')}",
                "- Open obligations:",
            ]
        )
        lines.extend(f"  - {item}" for item in node.get("open_obligations", [])[:6])
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    report = build_map()
    write_json(OUT_JSON, report)
    write_markdown(OUT_MD, render_markdown(report))
    print(f"wrote {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
