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
"""Validate the P vs NP result-refinement packet."""

from __future__ import annotations

from agentic_common import ROOT, clean_text, fail, load_json_object, rel, repo_path
from build_pvsnp_result_refinement_packet import OUT_JSON, OUT_MD, PAPER_PROJECT_ID, SKILLS


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    require(OUT_JSON.exists(), f"missing {rel(OUT_JSON)}")
    report = load_json_object(OUT_JSON)
    require(report.get("target_id") == "p-vs-np-target", "packet target must be P vs NP")
    require(report.get("paper_project_id") == PAPER_PROJECT_ID, "packet must remain scoped to the P vs NP paper project")
    require(report.get("status") == "pvsnp_result_refinement_ready", "packet must be ready")
    require(set(SKILLS).issubset(set(report.get("invoked_skills", []))), "missing recurring result-elaboration skills")
    for key in [
        "theorem_scope",
        "finite_object",
        "proof_packet",
        "transparent_row_support_packet",
        "prior_art_disqualifier_audit",
        "readiness_gate",
        "narrative_integration",
    ]:
        require(isinstance(report.get(key), dict) and report[key], f"missing {key}")

    scope = report["theorem_scope"]
    require("P != NP" in " ".join(scope.get("non_claims", [])), "scope must explicitly avoid P != NP overclaim")
    require("SAT notin P/poly" in " ".join(scope.get("excluded_domain", [])) or "SAT is outside P/poly" in " ".join(scope.get("excluded_domain", [])), "scope must exclude SAT/P-poly separation claims")
    require("a>q+beta c" in scope.get("smallest_honest_claim", ""), "scope must expose exact transfer threshold")

    obj = report["finite_object"]
    for symbol in ["H_N", "SAT_m", "a", "q", "beta", "A"]:
        require(symbol in obj.get("notation_table", {}), f"finite object missing notation {symbol}")
    require("advice" in clean_text(obj.get("validity_regime")).lower(), "finite object must track advice")

    proof = report["proof_packet"]
    require(proof.get("proof_status") in {"conditional_theorem", "proof_obligation_localized"}, "proof packet has unsupported proof status")
    require(len(proof.get("proof_steps", [])) >= 5, "proof packet needs stepwise derivation")
    require(any("q+\\beta c" in eq or "q+beta c" in eq for eq in proof.get("equations", [])), "proof packet missing transfer equation")

    transparent = report["transparent_row_support_packet"]
    require(transparent.get("name") == "TransparentRowSupport_N", "transparent support packet must name the consolidation object")
    require(transparent.get("status") == "consolidation_target", "transparent support packet must be the active consolidation target")
    definition_text = clean_text(transparent.get("definition_fields")).lower()
    for term in ["visible", "enumeration", "influence", "row_expansion", "same_theory", "advice"]:
        require(term.replace("_", " ") in definition_text or term in definition_text, f"transparent support definition missing {term}")
    positive = transparent.get("generic_positive_theorem", {})
    countermodel = transparent.get("generic_countermodel_theorem", {})
    require("Gamma" in clean_text(positive.get("statement")), "positive theorem must name Gamma charge")
    require("private-row" in clean_text(countermodel.get("statement")) or "unread-enable" in clean_text(countermodel.get("statement")), "countermodel theorem must name private-row/unread-enable obstruction")
    require(len(transparent.get("examples_subsumed") or positive.get("examples_subsumed", [])) >= 0, "transparent support packet malformed")
    require("Do not add more selector classes" in clean_text(transparent.get("stop_rule")), "transparent support packet must include anti-loop stop rule")
    for cycle in ["cycle-0103", "cycle-0104", "cycle-0105", "cycle-0106", "cycle-0107"]:
        require(cycle in transparent.get("evidence_cycles", []), f"transparent support evidence missing {cycle}")

    audit = report["prior_art_disqualifier_audit"]
    require(audit.get("claimability_decision") == "claimable_after_repair", "audit must not over-promote claimability")
    require(len(audit.get("disqualifier_matrix", [])) >= 4, "audit needs disqualifier matrix")
    audit_text = clean_text(audit)
    for term in ["target-equivalent", "advice", "beta", "prior-art"]:
        require(term in audit_text.lower(), f"audit missing {term}")

    readiness = report["readiness_gate"]
    require(readiness.get("readiness_decision") in {"scoped_note_ready_needs_prior_art_repair", "paper_scaffold_ready_for_theorem_consolidation"}, "readiness decision must remain scoped")
    require(readiness.get("gate_table", {}).get("prior_art_boundary_ready") is False, "prior-art boundary should remain explicitly open")
    require(readiness.get("missing_blockers"), "readiness gate must name finite blockers")
    forbidden = " ".join(readiness.get("forbidden_language", []))
    require("P != NP" in forbidden and "SAT outside P/poly" in forbidden, "forbidden language must include main overclaims")

    for raw in report.get("source_artifacts", []):
        if clean_text(raw):
            repo_path(str(raw), must_exist=True)
    manifest = clean_text(report.get("paper_project_manifest"))
    if manifest:
        manifest_path = repo_path(manifest, must_exist=True)
        manifest_payload = load_json_object(ROOT / manifest)
        require(manifest_path.is_file(), "paper project manifest path must be a file")
        require(manifest_payload.get("paper_project_id") == PAPER_PROJECT_ID, "paper project manifest id mismatch")
        require(manifest_payload.get("target_id") == "p-vs-np-target", "paper project manifest target mismatch")
    require(OUT_MD.exists(), f"missing {rel(OUT_MD)}")
    md = OUT_MD.read_text(encoding="utf-8")
    for phrase in ["Smallest Honest Claim", "Current Consolidation Target", "Theorem Pair", "Stop Rule", "Readiness", "Missing Blockers", "Next Paper Actions"]:
        require(phrase in md, f"{rel(OUT_MD)} missing {phrase}")
    print(f"validated {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
