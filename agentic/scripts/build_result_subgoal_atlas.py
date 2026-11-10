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
"""Build a target-scoped cumulative result and subgoal atlas."""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, stable_id, utc_now, write_json
from discovery_marathon_common import load_cycles, load_run_state, write_markdown
from target_profiles import target_profile


OUT_DIR = ROOT / "agentic/reports/result_subgoal_atlas"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"

CONTRIBUTION_MONITOR = ROOT / "agentic/reports/scientific_contribution_monitor/latest.json"
PVSNP_PRESSURE_BRIDGES = ROOT / "agentic/reports/pvsnp_pressure_bridges/latest.json"
PVSNP_NEGATIVE_TACTICS = ROOT / "agentic/reports/pvsnp_negative_tactics/latest.json"
FORMAL_DERIVATION = ROOT / "agentic/reports/timeline_formal_derivation/latest.json"
BIG_DEAL_ARCHIVE = ROOT / "agentic/reports/big_deal_goal_archive/latest.json"
DISCOVERY_REPORT = ROOT / "agentic/reports/discovery_marathon/latest.json"


STATUS_MAP = {
    "publishable_handoff_ready": "handoff_ready",
    "near_stepping_stone": "partially_achieved",
    "contribution_shaped": "partially_achieved",
    "active_bridge_candidate": "open",
    "theorem_candidate": "partially_achieved",
    "falsifier_candidate": "partially_achieved",
    "quarantined": "quarantined",
    "blocked": "blocked",
    "falsified": "falsified",
}


def active_target_id() -> str:
    _, run_state = load_run_state()
    return clean_text(run_state.get("target_id")) if run_state else ""


def target_matches(report: dict[str, Any], target_id: str) -> bool:
    declared = clean_text(report.get("target_id"))
    return not declared or declared == target_id


def route_family_for_text(text: str, target_id: str) -> str:
    lower = text.lower()
    if target_id == "p-vs-np-target":
        families = [
            ("hardness_magnification", ["magnification", "threshold", "beta", "exponent", "black-box", "black box"]),
            ("natural_property_barrier", ["natural", "barrier", "relativ", "algebr", "oracle"]),
            ("mcsp_mktp_carrier", ["mcsp", "mktp", "meta-complexity", "truth table", "certificate", "row"]),
            ("proof_complexity_transfer", ["proof complexity", "resolution", "frege", "tautology", "proof system"]),
            ("padding_projection", ["padding", "projection", "sparse valid", "valid length"]),
            ("all_exponent_uniformity", ["all-exponent", "cofinal", "uniformity", "p/poly", "advice"]),
        ]
    else:
        families = [
            ("finite_os_obstruction", ["finite", "os", "schur", "feshbach", "positivity", "quotient"]),
            ("wilson_collar_calculation", ["wilson", "collar", "hairpin", "endpoint", "kappa"]),
            ("same_theory_transfer", ["same-theory", "same theory", "transfer", "schwinger", "observable algebra"]),
            ("constructive_continuum_control", ["continuum", "cutoff", "constructive", "uniform", "remainder"]),
            ("spectral_reconstruction", ["spectral", "hamiltonian", "hilbert", "mass gap"]),
            ("nontriviality_witness", ["nontrivial", "interaction", "gauge"]),
        ]
    for family, markers in families:
        if any(marker in lower for marker in markers):
            return family
    return "unclassified_route"


def subgoal_id_for(kind: str, claim: str, target_id: str) -> str:
    family = route_family_for_text(f"{kind} {claim}", target_id)
    return f"{target_id.replace('-target', '')}.{family}"


def achievement_status(raw_status: str, fallback: str = "open") -> str:
    status = clean_text(raw_status)
    return STATUS_MAP.get(status, status if status in {"achieved", "partially_achieved", "open", "blocked", "falsified", "quarantined", "handoff_ready"} else fallback)


def entry(
    *,
    target_id: str,
    result_kind: str,
    claim: str,
    source_label: str,
    source_path: str,
    raw_status: str = "",
    branch_id: str = "",
    branch_title: str = "",
    route_family: str = "",
    dependencies: list[Any] | None = None,
    derivations: list[Any] | None = None,
    evidence_sources: list[Any] | None = None,
    validation_state: dict[str, Any] | None = None,
    open_obligations: list[Any] | None = None,
    promotion_criteria: list[Any] | None = None,
    demotion_criteria: list[Any] | None = None,
    paper_relevance: dict[str, Any] | None = None,
    non_claims: list[Any] | None = None,
    target_specific: dict[str, Any] | None = None,
) -> dict[str, Any]:
    clean_claim = clean_text(claim)
    clean_kind = clean_text(result_kind) or "result"
    family = clean_text(route_family) or route_family_for_text(clean_claim, target_id)
    subgoal_id = subgoal_id_for(family, clean_claim, target_id)
    evidence = [item for item in (evidence_sources or []) if clean_text(item)]
    evidence.append({"source": source_label, "path": source_path})
    return {
        "result_id": stable_id("result", target_id, clean_kind, clean_claim, branch_id or branch_title),
        "target_id": target_id,
        "subgoal_id": subgoal_id,
        "result_kind": clean_kind,
        "claim": clean_claim,
        "achievement_status": achievement_status(raw_status, "partially_achieved"),
        "problem_space_coordinates": {
            "route_family": family,
            "branch_id": clean_text(branch_id),
            "branch_title": clean_text(branch_title),
            "global_problem_role": global_problem_role(family, target_id),
        },
        "dependencies": [clean_text(item) for item in (dependencies or []) if clean_text(item)],
        "derivations": derivations or [],
        "evidence_sources": evidence,
        "validation_state": validation_state or {"status": "finite_check_queued", "validators": [], "last_checked": ""},
        "open_obligations": [clean_text(item) for item in (open_obligations or []) if clean_text(item)] or ["State a finite validation handoff before promotion."],
        "promotion_criteria": [clean_text(item) for item in (promotion_criteria or []) if clean_text(item)] or ["Promote only after evidence, validation state, and non-claim boundary are explicit."],
        "demotion_criteria": [clean_text(item) for item in (demotion_criteria or []) if clean_text(item)] or ["Demote if the result cannot name a target-preserving validation handoff."],
        "paper_relevance": paper_relevance or {"status": "not_assessed", "why_it_matters": global_problem_role(family, target_id)},
        "non_claims": [clean_text(item) for item in (non_claims or []) if clean_text(item)] or ["This entry does not prove the main target by itself."],
        "target_specific": target_specific or {},
    }


def global_problem_role(family: str, target_id: str) -> str:
    if target_id == "p-vs-np-target":
        mapping = {
            "hardness_magnification": "Tests whether weak lower-bound progress can transfer to P vs NP-level circuit lower bounds without losing all-exponent strength.",
            "natural_property_barrier": "Clarifies whether the proof object is blocked by naturalness, relativization, algebrization, oracle behavior, or advice leakage.",
            "mcsp_mktp_carrier": "Tests whether meta-complexity carriers can avoid nonuniform hard-row choice and produce target-relevant lower-bound evidence.",
            "proof_complexity_transfer": "Tests whether proof-system lower bounds can bridge to language or circuit lower bounds rather than staying inside proof complexity.",
            "padding_projection": "Checks whether padding or projection moves proof debt into sparse valid lengths or target-equivalent assumptions.",
            "all_exponent_uniformity": "Tracks the quantifier lift from bounded-window results to the all-exponent strength needed for NP not subset P/poly.",
        }
    else:
        mapping = {
            "finite_os_obstruction": "Tests finite reflection-positivity obstructions as controlled evidence for the constructive Yang-Mills route.",
            "wilson_collar_calculation": "Computes concrete Wilson observables that can decide whether finite OS obstruction terms have the needed sign or rank structure.",
            "same_theory_transfer": "Protects the bridge from finite or proxy calculations to the same continuum Yang-Mills theory.",
            "constructive_continuum_control": "Tracks cutoff, volume, and uniformity requirements needed for existence.",
            "spectral_reconstruction": "Connects Euclidean or Wilson data to Hilbert-space and mass-gap claims.",
            "nontriviality_witness": "Ensures the constructed theory is interacting rather than a trivial limit.",
        }
    return mapping.get(family, "Keeps the result linked to a named route family and explicit target commitments.")


def entries_from_contributions(target_id: str) -> list[dict[str, Any]]:
    monitor = load_optional_json(CONTRIBUTION_MONITOR)
    if not target_matches(monitor, target_id):
        return []
    rows = []
    for candidate in monitor.get("candidates", []) if isinstance(monitor.get("candidates"), list) else []:
        if not isinstance(candidate, dict):
            continue
        claim = clean_text(candidate.get("smallest_honest_claim"))
        if not claim:
            continue
        rows.append(
            entry(
                target_id=target_id,
                result_kind=clean_text(candidate.get("contribution_type")) or "contribution_candidate",
                claim=claim,
                source_label="scientific_contribution_monitor",
                source_path=rel(CONTRIBUTION_MONITOR),
                raw_status=clean_text(candidate.get("stepping_stone_maturity")),
                branch_title=clean_text(candidate.get("branch_title")),
                dependencies=candidate.get("validation_burden", []),
                derivations=[{"cycle_id": candidate.get("cycle_id", ""), "kind": "candidate_evidence"}],
                evidence_sources=candidate.get("evidence_basis", []),
                validation_state={"status": clean_text(candidate.get("status")) or "candidate", "validators": ["validate_scientific_contribution_monitor.py"], "last_checked": ""},
                open_obligations=candidate.get("missing_to_publishable", []) or candidate.get("validation_burden", []),
                promotion_criteria=candidate.get("good_enough_when", []),
                demotion_criteria=candidate.get("stop_when", []),
                paper_relevance=candidate.get("good_enough_paper_relevance", {}),
                non_claims=[candidate.get("overclaim_boundary", "")],
                target_specific={"candidate_id": candidate.get("candidate_id", ""), "scores": candidate.get("scores", {})},
            )
        )
    return rows


def entries_from_pvsnp_pressure(target_id: str) -> list[dict[str, Any]]:
    if target_id != "p-vs-np-target":
        return []
    report = load_optional_json(PVSNP_PRESSURE_BRIDGES)
    if not target_matches(report, target_id):
        return []
    rows = []
    for bridge in report.get("bridge_candidates", []) if isinstance(report.get("bridge_candidates"), list) else []:
        if not isinstance(bridge, dict):
            continue
        rows.append(
            entry(
                target_id=target_id,
                result_kind="pressure_bridge_candidate",
                claim=clean_text(bridge.get("paper_safe_narrative") or bridge.get("bridge_abstraction") or bridge.get("title")),
                source_label="pvsnp_pressure_bridges",
                source_path=rel(PVSNP_PRESSURE_BRIDGES),
                raw_status=clean_text(bridge.get("status")),
                branch_title=clean_text(bridge.get("title")),
                route_family=route_family_for_text(clean_text(bridge), target_id),
                dependencies=[bridge.get("source_object", ""), bridge.get("target_object", ""), bridge.get("controlled_interface", "")],
                evidence_sources=bridge.get("evidence_paths", []),
                open_obligations=[bridge.get("proof_obligation", "")],
                promotion_criteria=[bridge.get("when_to_persist", "")],
                demotion_criteria=[bridge.get("when_to_pivot", "")],
                non_claims=report.get("non_claims", []),
                target_specific={"bridge_id": bridge.get("id", ""), "priority_score": bridge.get("priority_score", 0)},
            )
        )
    return rows


def entries_from_pvsnp_negative_tactics(target_id: str) -> list[dict[str, Any]]:
    if target_id != "p-vs-np-target":
        return []
    report = load_optional_json(PVSNP_NEGATIVE_TACTICS)
    if not target_matches(report, target_id):
        return []
    rows = []
    for rec in report.get("recommendations", []) if isinstance(report.get("recommendations"), list) else []:
        if not isinstance(rec, dict):
            continue
        rows.append(
            entry(
                target_id=target_id,
                result_kind=f"negative_tactic_{clean_text(rec.get('tactic_mode'))}",
                claim=(
                    f"{clean_text(rec.get('branch_title'))}: {clean_text(rec.get('exact_negation_or_method_class'))} "
                    f"has carrier {clean_text(rec.get('contradiction_carrier_or_no_go_family'))} and conflict target {clean_text(rec.get('conflict_target'))}."
                ),
                source_label="pvsnp_negative_tactics",
                source_path=rel(PVSNP_NEGATIVE_TACTICS),
                raw_status="theorem_candidate" if rec.get("tactic_mode") in {"proof_by_contradiction", "impossibility_theorem"} else "falsifier_candidate",
                branch_id=clean_text(rec.get("branch_id")),
                branch_title=clean_text(rec.get("branch_title")),
                route_family=route_family_for_text(clean_text(rec), target_id),
                dependencies=rec.get("escape_conditions", []),
                evidence_sources=[{"source_cycle_ids": rec.get("source_cycle_ids", [])}],
                open_obligations=rec.get("proof_obligations", []),
                promotion_criteria=[rec.get("next_validation_handoff", "")],
                demotion_criteria=rec.get("escape_conditions", []),
                paper_relevance={"status": "candidate", "why_it_matters": rec.get("paper_contribution_potential", "")},
                non_claims=["This tactic scopes a method family; it does not settle P vs NP."],
                target_specific={"tactic_mode": rec.get("tactic_mode", ""), "recommendation_id": rec.get("recommendation_id", "")},
            )
        )
    return rows


def entries_from_formal_derivation(target_id: str) -> list[dict[str, Any]]:
    report = load_optional_json(FORMAL_DERIVATION)
    if not target_matches(report, target_id):
        return []
    text = clean_text(report)
    if not report or (target_id == "p-vs-np-target" and any(term in text.lower() for term in ["yang-mills", "wilson", "reflection positivity", "mass gap"])):
        return []
    rows = []
    for prop in report.get("propositions", []) if isinstance(report.get("propositions"), list) else []:
        if not isinstance(prop, dict):
            continue
        rows.append(
            entry(
                target_id=target_id,
                result_kind="formal_derivation_proposition",
                claim=clean_text(prop.get("statement") or prop.get("name")),
                source_label="timeline_formal_derivation",
                source_path=rel(FORMAL_DERIVATION),
                raw_status=clean_text(report.get("status")) or "partially_achieved",
                branch_title=clean_text(report.get("mathematical_object")),
                route_family=route_family_for_text(clean_text(prop), target_id),
                derivations=[{"derivation_id": report.get("derivation_id", ""), "proposition": prop.get("name", "")}],
                evidence_sources=prop.get("source_unit_ids", []),
                open_obligations=report.get("unresolved_obligations", []),
                promotion_criteria=[clean_text(report.get("validation_handoff", ""))],
                non_claims=report.get("non_claims", []),
            )
        )
    return rows


def entries_from_cycles(target_id: str) -> list[dict[str, Any]]:
    _, run_state = load_run_state(target_id=target_id)
    cycles = load_cycles(run_state) if run_state else []
    rows = []
    for cycle in cycles[-10:]:
        if clean_text(cycle.get("target_id")) != target_id:
            continue
        for output in cycle.get("branch_outputs", []):
            if not isinstance(output, dict):
                continue
            claim = clean_text(output.get("mathematical_learning"))
            if not claim:
                continue
            rows.append(
                entry(
                    target_id=target_id,
                    result_kind="cycle_learning",
                    claim=f"{clean_text(cycle.get('cycle_id'))}: {claim}",
                    source_label="discovery_cycle",
                    source_path=rel(ROOT / f"agentic/runs/discovery_marathons/{run_state['run_id']}/cycles/{cycle.get('cycle_id')}.json"),
                    raw_status="partially_achieved",
                    branch_id=clean_text(output.get("branch_id")),
                    branch_title=clean_text(output.get("branch_title")),
                    derivations=[{"cycle_id": cycle.get("cycle_id", ""), "derivation_id": output.get("attempted_derivation", {}).get("derivation_id", "")}],
                    evidence_sources=[f"cycle:{cycle.get('cycle_id')}"],
                    open_obligations=[output.get("next_experiment", ""), output.get("attempted_derivation", {}).get("blocking_gap", "")],
                    promotion_criteria=[output.get("control_decision", {}).get("promotion_test", "")],
                    demotion_criteria=[output.get("control_decision", {}).get("pivot_test", "")],
                    non_claims=[output.get("attempted_derivation", {}).get("why_not_yet_a_proof", "")],
                )
            )
    return rows


def dedupe_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: dict[str, dict[str, Any]] = {}
    for row in entries:
        key = stable_id(
            "result.key",
            row.get("target_id", ""),
            row.get("subgoal_id", ""),
            row.get("result_kind", ""),
            row.get("claim", "")[:220],
            row.get("problem_space_coordinates", {}).get("branch_id", ""),
        )
        existing = seen.get(key)
        if not existing:
            seen[key] = row
            continue
        existing["evidence_sources"].extend(row.get("evidence_sources", []))
        existing["open_obligations"] = sorted(set(existing.get("open_obligations", []) + row.get("open_obligations", [])))
        if row.get("achievement_status") == "handoff_ready":
            existing["achievement_status"] = "handoff_ready"
    return list(seen.values())


def build_atlas(target_id: str | None = None) -> dict[str, Any]:
    target_id = clean_text(target_id) or active_target_id()
    profile = target_profile(target_id)
    entries = []
    entries.extend(entries_from_contributions(target_id))
    entries.extend(entries_from_pvsnp_pressure(target_id))
    entries.extend(entries_from_pvsnp_negative_tactics(target_id))
    entries.extend(entries_from_formal_derivation(target_id))
    entries.extend(entries_from_cycles(target_id))
    results = dedupe_entries(entries)
    by_subgoal: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in results:
        by_subgoal[row["subgoal_id"]].append(row)
    subgoals = []
    for subgoal_id, rows in sorted(by_subgoal.items()):
        statuses = {row.get("achievement_status") for row in rows}
        subgoals.append(
            {
                "subgoal_id": subgoal_id,
                "title": subgoal_id.split(".", 1)[-1].replace("_", " ").title(),
                "target_id": target_id,
                "result_count": len(rows),
                "status": "handoff_ready" if "handoff_ready" in statuses else "partially_achieved" if "partially_achieved" in statuses else "open",
                "result_ids": [row["result_id"] for row in rows],
                "open_obligations": sorted({item for row in rows for item in row.get("open_obligations", []) if clean_text(item)})[:8],
            }
        )
    problem_index: dict[str, list[str]] = defaultdict(list)
    for row in results:
        problem_index[row["problem_space_coordinates"]["route_family"]].append(row["result_id"])
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": target_id,
        "target_display_name": profile.get("display_name", target_id),
        "source_artifacts": [
            rel(CONTRIBUTION_MONITOR),
            rel(PVSNP_PRESSURE_BRIDGES),
            rel(PVSNP_NEGATIVE_TACTICS),
            rel(FORMAL_DERIVATION),
            rel(BIG_DEAL_ARCHIVE),
            rel(DISCOVERY_REPORT),
        ],
        "summary": {
            "result_count": len(results),
            "subgoal_count": len(subgoals),
            "handoff_ready_count": sum(1 for row in results if row["achievement_status"] == "handoff_ready"),
            "partial_count": sum(1 for row in results if row["achievement_status"] == "partially_achieved"),
            "open_count": sum(1 for row in results if row["achievement_status"] == "open"),
            "purpose": "Durable target-scoped memory of achieved results, partial results, derivations, obligations, and problem-space coordinates.",
        },
        "subgoals": subgoals,
        "results": results,
        "problem_space_index": dict(sorted(problem_index.items())),
        "validation_handoff": [
            "agentic/scripts/validate_result_subgoal_atlas.py",
            "agentic/scripts/build_problem_space_map.py",
            "agentic/scripts/build_derivation_vault.py",
        ],
    }


def render_markdown(atlas: dict[str, Any]) -> str:
    lines = [
        "# Result Subgoal Atlas",
        "",
        f"- Target: `{atlas.get('target_id', '')}`",
        f"- Results: `{atlas.get('summary', {}).get('result_count', 0)}`",
        f"- Subgoals: `{atlas.get('summary', {}).get('subgoal_count', 0)}`",
        "",
        "## Subgoals",
        "",
    ]
    result_by_id = {row["result_id"]: row for row in atlas.get("results", [])}
    for subgoal in atlas.get("subgoals", []):
        lines.extend([f"### {subgoal.get('title')}", "", f"- Status: `{subgoal.get('status')}`", ""])
        for result_id in subgoal.get("result_ids", [])[:8]:
            row = result_by_id.get(result_id, {})
            lines.extend(
                [
                    f"- `{row.get('achievement_status', '')}` **{row.get('result_kind', '')}**: {row.get('claim', '')}",
                    f"  - Why it matters: {row.get('problem_space_coordinates', {}).get('global_problem_role', '')}",
                    f"  - Next obligation: {row.get('open_obligations', [''])[0] if row.get('open_obligations') else ''}",
                ]
            )
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    atlas = build_atlas()
    write_json(OUT_JSON, atlas)
    write_markdown(OUT_MD, render_markdown(atlas))
    print(f"wrote {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
