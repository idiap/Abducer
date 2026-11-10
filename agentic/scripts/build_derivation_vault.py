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
"""Persist reusable derivation objects linked to result-atlas entries."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, stable_id, utc_now, write_json
from discovery_marathon_common import load_cycles, load_run_state, write_markdown


ATLAS = ROOT / "agentic/reports/result_subgoal_atlas/latest.json"
FORMAL_DERIVATION = ROOT / "agentic/reports/timeline_formal_derivation/latest.json"
OUT_DIR = ROOT / "agentic/reports/derivation_vault"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"


def target_matches(report: dict[str, Any], target_id: str) -> bool:
    declared = clean_text(report.get("target_id"))
    return not declared or declared == target_id


def linked_results_for_text(atlas: dict[str, Any], text: str) -> list[str]:
    lower = text.lower()
    hits = []
    for row in atlas.get("results", []) if isinstance(atlas.get("results"), list) else []:
        claim = clean_text(row.get("claim")).lower()
        branch = clean_text(row.get("problem_space_coordinates", {}).get("branch_title")).lower()
        if (branch and branch in lower) or any(token and token in lower for token in claim.split()[:8]):
            hits.append(row.get("result_id"))
        if len(hits) >= 3:
            break
    return [hit for hit in hits if clean_text(hit)]


def derivations_from_formal(atlas: dict[str, Any], target_id: str) -> list[dict[str, Any]]:
    report = load_optional_json(FORMAL_DERIVATION)
    if not target_matches(report, target_id):
        return []
    text = clean_text(report)
    if target_id == "p-vs-np-target" and any(term in text.lower() for term in ["yang-mills", "wilson", "reflection positivity", "mass gap"]):
        return []
    rows = []
    for prop in report.get("propositions", []) if isinstance(report.get("propositions"), list) else []:
        if not isinstance(prop, dict):
            continue
        body = clean_text(prop)
        linked = linked_results_for_text(atlas, body)
        rows.append(
            {
                "derivation_id": stable_id("derivation", report.get("derivation_id", ""), prop.get("name", "")),
                "target_id": target_id,
                "kind": "formal_derivation",
                "title": clean_text(prop.get("name")),
                "claim": clean_text(prop.get("statement")),
                "definitions": report.get("definitions", []),
                "assumptions": report.get("assumptions", []),
                "equations": [{"latex": prop.get("latex", ""), "valid_when": prop.get("valid_when", "")}],
                "proof_steps": prop.get("proof_steps", []),
                "validity_regime": clean_text(prop.get("valid_when")),
                "proof_status": clean_text(report.get("status")) or "formal_fragment",
                "unresolved_obligations": report.get("unresolved_obligations", []),
                "non_claims": report.get("non_claims", []),
                "linked_result_ids": linked,
                "orphan_reason": "" if linked else "No target-matching atlas result currently cites this formal derivation.",
                "source_artifact": rel(FORMAL_DERIVATION),
            }
        )
    return rows


def derivations_from_cycles(atlas: dict[str, Any], target_id: str) -> list[dict[str, Any]]:
    _, run_state = load_run_state(target_id=target_id)
    cycles = load_cycles(run_state) if run_state else []
    rows = []
    for cycle in cycles[-20:]:
        if clean_text(cycle.get("target_id")) != target_id:
            continue
        for output in cycle.get("branch_outputs", []):
            if not isinstance(output, dict):
                continue
            derivation = output.get("attempted_derivation", {}) if isinstance(output.get("attempted_derivation"), dict) else {}
            lemmas = output.get("candidate_lemmas", []) if isinstance(output.get("candidate_lemmas"), list) else []
            title = f"{clean_text(cycle.get('cycle_id'))} · {clean_text(output.get('branch_title'))}"
            body = clean_text({"output": output, "derivation": derivation})
            linked = linked_results_for_text(atlas, body)
            definitions = []
            assumptions = []
            equations = []
            for lemma in lemmas[:2]:
                if not isinstance(lemma, dict):
                    continue
                definitions.extend(lemma.get("definitions", []))
                assumptions.extend(lemma.get("assumptions", []))
                equations.extend(lemma.get("equations", []))
            rows.append(
                {
                    "derivation_id": stable_id("derivation", cycle.get("cycle_id", ""), output.get("branch_id", ""), derivation.get("derivation_id", "")),
                    "target_id": target_id,
                    "kind": "branch_derivation_sketch",
                    "title": title,
                    "claim": clean_text(output.get("mathematical_learning")),
                    "definitions": definitions[:8],
                    "assumptions": assumptions[:8],
                    "equations": equations[:8],
                    "proof_steps": derivation.get("steps", []),
                    "validity_regime": clean_text(lemmas[0].get("equations", [{}])[0].get("valid_when", "")) if lemmas and isinstance(lemmas[0], dict) and lemmas[0].get("equations") else "",
                    "proof_status": "sketch_with_blocking_gap",
                    "unresolved_obligations": [derivation.get("blocking_gap", ""), output.get("next_experiment", "")],
                    "non_claims": [derivation.get("why_not_yet_a_proof", "")],
                    "linked_result_ids": linked,
                    "orphan_reason": "" if linked else "Branch derivation has not yet been promoted into a stable atlas result.",
                    "source_artifact": rel(ROOT / f"agentic/runs/discovery_marathons/{run_state['run_id']}/cycles/{cycle.get('cycle_id')}.json"),
                }
            )
    return rows


def target_safe_atlas(atlas: dict[str, Any] | None = None, target_id: str | None = None) -> dict[str, Any]:
    requested_target = clean_text(target_id)
    candidate = dict(atlas) if isinstance(atlas, dict) and atlas else load_optional_json(ATLAS)
    candidate_target = clean_text(candidate.get("target_id"))
    if requested_target and candidate_target != requested_target:
        from build_result_subgoal_atlas import build_atlas

        candidate = build_atlas(requested_target)
    return candidate


def build_vault(atlas: dict[str, Any] | None = None, target_id: str | None = None) -> dict[str, Any]:
    atlas = target_safe_atlas(atlas, target_id)
    target_id = clean_text(target_id) or clean_text(atlas.get("target_id"))
    rows = []
    rows.extend(derivations_from_formal(atlas, target_id))
    rows.extend(derivations_from_cycles(atlas, target_id))
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": target_id,
        "source_atlas": rel(ATLAS),
        "summary": {
            "derivation_count": len(rows),
            "linked_count": sum(1 for row in rows if row.get("linked_result_ids")),
            "orphan_count": sum(1 for row in rows if not row.get("linked_result_ids")),
        },
        "derivations": rows,
        "validation_handoff": ["agentic/scripts/validate_derivation_vault.py"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Derivation Vault", "", f"- Target: `{report.get('target_id', '')}`", ""]
    for row in report.get("derivations", [])[:40]:
        lines.extend(
            [
                f"## {row.get('title')}",
                "",
                f"- Kind: `{row.get('kind')}`",
                f"- Proof status: `{row.get('proof_status')}`",
                f"- Claim: {row.get('claim')}",
                f"- Linked results: {', '.join(row.get('linked_result_ids', [])) or row.get('orphan_reason', '')}",
                f"- Next obligation: {row.get('unresolved_obligations', [''])[0] if row.get('unresolved_obligations') else ''}",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    report = build_vault()
    write_json(OUT_JSON, report)
    write_markdown(OUT_MD, render_markdown(report))
    print(f"wrote {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
