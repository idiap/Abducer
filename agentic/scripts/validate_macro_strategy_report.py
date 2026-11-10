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
"""Validate macro strategy synthesis and report integration data."""

from __future__ import annotations

from agentic_common import clean_text, fail, load_json_object, rel
from build_macro_strategy_report import OUT_JSON, OUT_MD


REQUIRED_STRATEGY_FIELDS = {
    "strategy_id",
    "title",
    "route_family",
    "priority_score",
    "macro_thesis",
    "physics_picture",
    "why_now",
    "evidence_from_story",
    "what_to_compute_next",
    "success_condition",
    "failure_or_pivot_condition",
    "linked_literature_refs",
    "active_skills",
    "epistemic_status",
}


def main() -> int:
    if not OUT_JSON.exists():
        fail(f"missing {rel(OUT_JSON)}")
    report = load_json_object(OUT_JSON)
    for field in ["headline", "strategy_status", "physics_language_standard", "story_basis", "macro_strategies", "recommended_next_posture"]:
        if not report.get(field):
            fail(f"{rel(OUT_JSON)} missing {field}")
    strategies = report.get("macro_strategies", [])
    if not isinstance(strategies, list) or len(strategies) < 4:
        fail(f"{rel(OUT_JSON)} needs at least four macro strategies")
    previous = 101
    joined = clean_text(report).lower()
    target_id = clean_text(report.get("target_id"))
    if target_id == "p-vs-np-target":
        required_phrases = ["p vs np", "sat", "circuit", "p/poly", "transfer", "carrier", "beta", "nonuniform", "barrier"]
        required_skills = {
            "pvsnp-conceptual-pressure-localizer",
            "pvsnp-qualitative-complexity-reasoner",
            "pvsnp-impossibility-theorem-forger",
            "pvsnp-symbolic-complexity-auditor",
        }
    else:
        required_phrases = ["yang-mills", "wilson", "schwinger", "reflection positivity", "continuum", "hilbert", "spectral gap"]
        required_skills = set()
    for phrase in required_phrases:
        if phrase not in joined:
            fail(f"{rel(OUT_JSON)} lacks target strategy language `{phrase}`")
    if required_skills and not required_skills.issubset({skill for strategy in strategies for skill in strategy.get("active_skills", [])}):
        fail(f"{rel(OUT_JSON)} P vs NP macro strategies do not expose required skills {sorted(required_skills)}")
    for index, strategy in enumerate(strategies, start=1):
        missing = REQUIRED_STRATEGY_FIELDS.difference(strategy)
        if missing:
            fail(f"strategy {index} missing fields {sorted(missing)}")
        if int(strategy["priority_score"]) > previous:
            fail("macro strategies must be sorted by descending priority_score")
        previous = int(strategy["priority_score"])
        for list_field in ["what_to_compute_next", "success_condition", "failure_or_pivot_condition", "linked_literature_refs", "active_skills"]:
            if len(strategy.get(list_field, [])) < 3:
                fail(f"strategy {index} needs at least three {list_field}")
        if len(strategy.get("evidence_from_story", [])) < 1:
            fail(f"strategy {index} needs evidence_from_story from the accumulated cycles")
        text = clean_text(strategy).lower()
        domain_words = ["sat", "circuit", "carrier", "p/poly", "beta", "nonuniform"] if target_id == "p-vs-np-target" else ["wilson", "schwinger", "gauge", "hilbert", "spectral", "continuum"]
        if "workflow" in text and not any(word in text for word in domain_words):
            fail(f"strategy {index} is workflow-heavy without target-domain language")
    posture = report.get("recommended_next_posture", {})
    for field in ["primary", "secondary", "handoff", "avoid"]:
        if not clean_text(posture.get(field)):
            fail(f"recommended_next_posture missing {field}")
    if not OUT_MD.exists():
        fail(f"missing {rel(OUT_MD)}")
    md = OUT_MD.read_text(encoding="utf-8")
    for phrase in ["Macro Strategy Report", "Recommended Next Posture", "Macro Strategies", "Physics picture"]:
        if phrase not in md:
            fail(f"{rel(OUT_MD)} missing `{phrase}`")
    print(f"validated {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
