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
"""Validate the P vs NP proof-delivery priority queue."""

from __future__ import annotations

from agentic_common import clean_text, fail, load_json_object, rel, repo_path
from build_pvsnp_proof_delivery_queue import (
    OUT_JSON,
    OUT_MD,
    PROOF_DELIVERY_SKILLS,
    PVSNP_DISCOVERY_SKILLS,
    PVSNP_REVIEW_SKILLS,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def text_contains(row: dict, *terms: str) -> bool:
    text = clean_text(row).lower()
    return all(term.lower() in text for term in terms)


def main() -> int:
    require(OUT_JSON.exists(), f"missing {rel(OUT_JSON)}")
    report = load_json_object(OUT_JSON)
    require(report.get("status") == "pvsnp_proof_delivery_queue_ready", "queue status is not ready")
    require(report.get("target_id") == "p-vs-np-target", "queue must be scoped to P vs NP")
    require(
        report.get("top_item_id") == "pvsnp.paper.bit-explicit-parser-formulaeval-boundary",
        "TransparentRowSupport_N / FormulaEval boundary theorem pair must be top item",
    )
    extracted = report.get("extracted_from_draft", {})
    require(extracted.get("source"), "queue must record the source draft")
    require(len(extracted.get("proof_assets", [])) >= 5, "queue must extract proof assets from the draft")
    require(len(extracted.get("open_directions", [])) >= 5, "queue must extract open directions from the draft")
    items = report.get("items", [])
    require(isinstance(items, list) and len(items) >= 7, "expected at least seven draft-extracted proof-delivery items")
    top = items[0]
    require(top.get("queue_id") == report.get("top_item_id"), "first item must match top_item_id")
    require(int(top.get("priority_score", 0)) >= 9990, "top proof item must outrank normal queue items")
    require(
        text_contains(top, "TransparentRowSupport_N", "Gamma_trans", "FormulaEval"),
        "top proof item must be the TransparentRowSupport_N theorem-pair task",
    )
    require(
        text_contains(top, "cycle", "inference", "paper"),
        "top proof item must include cycle evidence, inference, and paper handoffs",
    )
    require(text_contains(top, "support-density", "q-trichotomy"), "top proof item must include the support-density q-trichotomy")
    require(text_contains(top, "private-row", "countermodel"), "top proof item must include the hidden-support countermodel")

    required = set(PROOF_DELIVERY_SKILLS + PVSNP_REVIEW_SKILLS + PVSNP_DISCOVERY_SKILLS)
    top_skills = set(top.get("required_skills", []))
    missing = sorted(required.difference(top_skills))
    require(not missing, f"top proof item missing required skills: {', '.join(missing)}")

    for index, row in enumerate(items, start=1):
        require(row.get("queue_source") == "proof_delivery_priority", f"item {index} must use proof_delivery_priority source")
        for field in [
            "queue_id",
            "title",
            "next_analysis",
            "theorem_goal",
            "source_object",
            "source_anchor",
            "proof_status",
            "target_object",
            "proof_outputs",
            "validation_steps",
            "success_criteria",
            "demotion_criteria",
            "required_skills",
            "paper_handoff",
        ]:
            require(row.get(field), f"item {index} missing {field}")
        require(any("proof" in clean_text(step).lower() for step in row.get("validation_steps", [])), f"item {index} validation steps must include proof work")
        require(any("demot" in clean_text(step).lower() or "fails" in clean_text(step).lower() or "cannot" in clean_text(step).lower() for step in row.get("demotion_criteria", [])), f"item {index} needs demotion criteria")
        require("explore" not in clean_text(row.get("next_analysis")).lower(), f"item {index} must not be broad exploration")
        require(row.get("required_skills"), f"item {index} has no required skills")
        for skill in row.get("required_skills", []):
            candidate_paths = [
                f"skills/proof_delivery/{skill}/SKILL.md",
                f"skills/orchestration/{skill}/SKILL.md",
                f"skills/reasoning/{skill}/SKILL.md",
                f"skills/evaluation/{skill}/SKILL.md",
                f"skills/reporting/{skill}/SKILL.md",
                f"skills/results_ellaboration/{skill}/SKILL.md",
            ]
            require(any(repo_path(path).exists() for path in candidate_paths), f"item {index} references missing skill {skill}")

    require(OUT_MD.exists(), f"missing {rel(OUT_MD)}")
    md = OUT_MD.read_text(encoding="utf-8")
    for phrase in [
        "P vs NP Proof Delivery Queue",
        "TransparentRowSupport",
        "FormulaEval",
        "Extracted Proof Assets",
        "Extracted Open Directions",
        "Required skills",
    ]:
        require(phrase in md, f"{rel(OUT_MD)} missing {phrase}")
    print(f"validated {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
