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
"""Validate visual conceptualization packets."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from agentic_common import clean_text, fail, load_json_object, rel


REQUIRED_TOP_LEVEL = [
    "schema",
    "generated_utc",
    "generated_by_skills",
    "target_id",
    "run_id",
    "source_context",
    "summary",
    "visual_conceptualizations",
    "workflow_caps",
    "evidence_paths",
    "validation_handoff",
]
PROPERTY_CATEGORIES = {
    "invariant",
    "symmetry",
    "locality_globality",
    "order_monotonicity",
    "positivity_sign",
    "limiting_behavior",
    "physical_carrier",
    "proof_obligation",
}
ALLOWED_VERDICTS = {"preserved", "partially_preserved", "distorted", "absent"}
ALLOWED_AUDIT_VERDICTS = {
    "usable_for_explanation",
    "usable_for_hypothesis_generation",
    "needs_revision",
    "quarantine",
    "reject",
}
ROUTE_ACTIONS = {
    "artifact_sprint",
    "falsifier_sprint",
    "reframe",
    "quarantine",
    "representation_requirement",
    "same-theory carrier certificate",
    "reflection-positivity interval certificate",
    "endpoint source table plus positivity interval",
    "uniform tail bound ledger",
    "OS reconstruction obligation ledger",
    "order-of-limits spectral falsifier",
    "property-preservation ledger",
}


def require_list(value: Any, label: str, source: Path, min_items: int = 1) -> list[Any]:
    if not isinstance(value, list) or len([item for item in value if clean_text(item)]) < min_items:
        fail(f"{rel(source)} {label} must contain at least {min_items} item(s)")
    return value


def require_dict(value: Any, label: str, source: Path) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{rel(source)} {label} must be an object")
    return value


def validate_hypothesis(item: dict[str, Any], source: Path, row_label: str) -> None:
    for field in ["kind", "hypothesis", "route_consequence", "required_artifact", "falsifier", "expected_physics_reward"]:
        if not clean_text(item.get(field)):
            fail(f"{rel(source)} {row_label} hypothesis_inspiration missing {field}")
    route_text = clean_text(item.get("route_consequence"))
    artifact = clean_text(item.get("required_artifact"))
    if not route_text or not artifact:
        fail(f"{rel(source)} {row_label} inspired hypothesis needs route_consequence and required_artifact")


def validate_concept(row: dict[str, Any], source: Path, *, ym: bool) -> str:
    label = clean_text(row.get("concept_id")) or "visual_conceptualization"
    if not clean_text(row.get("concept_id")):
        fail(f"{rel(source)} visual_conceptualization missing concept_id")
    focus = require_dict(row.get("formal_focus"), f"{label}.formal_focus", source)
    for field in ["type", "name", "statement", "proof_pressure", "physical_carrier"]:
        if not clean_text(focus.get(field)):
            fail(f"{rel(source)} {label}.formal_focus missing {field}")
    if ym and clean_text(focus.get("physical_carrier")).lower() in {"", "not_applicable_or_not_named", "missing"}:
        fail(f"{rel(source)} {label} must name a YM physical carrier")
    require_list(row.get("main_concepts"), f"{label}.main_concepts", source, min_items=3)
    require_list(row.get("key_properties"), f"{label}.key_properties", source, min_items=4)
    metaphor = require_dict(row.get("visual_metaphor"), f"{label}.visual_metaphor", source)
    for field in ["family", "title", "description", "why_selected"]:
        if not clean_text(metaphor.get(field)):
            fail(f"{rel(source)} {label}.visual_metaphor missing {field}")
    table = require_list(row.get("property_preservation_table"), f"{label}.property_preservation_table", source, min_items=6)
    categories = set()
    distorted = False
    for index, prop in enumerate(table):
        if not isinstance(prop, dict):
            fail(f"{rel(source)} {label}.property_preservation_table[{index}] must be object")
        for field in ["category", "formal_property", "visual_counterpart", "preservation_verdict", "rationale"]:
            if not clean_text(prop.get(field)):
                fail(f"{rel(source)} {label}.property_preservation_table[{index}] missing {field}")
        category = clean_text(prop.get("category"))
        if category not in PROPERTY_CATEGORIES:
            fail(f"{rel(source)} {label}.property_preservation_table[{index}] invalid category {category}")
        verdict = clean_text(prop.get("preservation_verdict"))
        if verdict not in ALLOWED_VERDICTS:
            fail(f"{rel(source)} {label}.property_preservation_table[{index}] invalid preservation_verdict {verdict}")
        categories.add(category)
        distorted = distorted or verdict in {"distorted", "absent"}
    missing_categories = PROPERTY_CATEGORIES - categories
    if missing_categories:
        fail(f"{rel(source)} {label} missing preservation categories: {sorted(missing_categories)}")
    require_list(row.get("distortion_ledger"), f"{label}.distortion_ledger", source, min_items=2)
    ledger_text = clean_text(row.get("distortion_ledger")).lower()
    if not distorted and not any(marker in ledger_text for marker in ["distort", "hide", "overstate", "understate", "suggest", "not justify"]):
        fail(f"{rel(source)} {label} needs an explicit distortion, hidden-danger, or absent-property record")
    hypotheses = require_list(row.get("hypothesis_inspiration"), f"{label}.hypothesis_inspiration", source)
    for hypothesis in hypotheses:
        if not isinstance(hypothesis, dict):
            fail(f"{rel(source)} {label}.hypothesis_inspiration entries must be objects")
        validate_hypothesis(hypothesis, source, label)
    if not clean_text(row.get("non_claim_boundary")):
        fail(f"{rel(source)} {label} missing non_claim_boundary")
    audit = require_dict(row.get("audit"), f"{label}.audit", source)
    verdict = clean_text(audit.get("audit_verdict"))
    if verdict not in ALLOWED_AUDIT_VERDICTS:
        fail(f"{rel(source)} {label}.audit invalid verdict {verdict}")
    for field in ["physical_relevance_verdict", "proof_search_value", "allowed_route_consequence"]:
        if not clean_text(audit.get(field)):
            fail(f"{rel(source)} {label}.audit missing {field}")
    if verdict in {"usable_for_hypothesis_generation", "needs_revision", "quarantine"}:
        consequence = clean_text(audit.get("allowed_route_consequence"))
        if consequence not in ROUTE_ACTIONS and not any(token in consequence for token in ["artifact", "falsifier", "ledger", "certificate", "interval", "table"]):
            fail(f"{rel(source)} {label}.audit allowed_route_consequence is not concrete: {consequence}")
    return verdict


def validate_packet(packet: dict[str, Any], source: Path) -> None:
    for field in REQUIRED_TOP_LEVEL:
        if not clean_text(packet.get(field)):
            fail(f"{rel(source)} missing {field}")
    if packet.get("schema") != "abducer.visual_conceptualization_packet.v1":
        fail(f"{rel(source)} invalid schema {packet.get('schema')}")
    skills = packet.get("generated_by_skills", [])
    for skill in ["visual-theorem-conceptualizer", "visual-analogy-preservation-auditor"]:
        if skill not in skills:
            fail(f"{rel(source)} must cite {skill}")
    source_context = require_dict(packet.get("source_context"), "source_context", source)
    require_list(source_context.get("cycle_ids"), "source_context.cycle_ids", source)
    if clean_text(source_context.get("trigger")) != "deep_reflection_visual_conceptualization":
        fail(f"{rel(source)} invalid source_context.trigger")
    summary = require_dict(packet.get("summary"), "summary", source)
    for field in ["concept_count", "hypothesis_output_count", "quarantined_or_rejected_count"]:
        if field not in summary or not isinstance(summary.get(field), int):
            fail(f"{rel(source)} summary missing numeric {field}")
    for field in ["route_consequences", "core_diagnosis"]:
        if field not in summary or not clean_text(summary.get(field)):
            fail(f"{rel(source)} summary missing {field}")
    if int(summary.get("hypothesis_output_count", 0)) <= 0:
        fail(f"{rel(source)} must emit at least one hypothesis output")
    require_list(summary.get("route_consequences"), "summary.route_consequences", source)
    rows = require_list(packet.get("visual_conceptualizations"), "visual_conceptualizations", source)
    ym = clean_text(packet.get("target_id")) == "yang-mills-existence-and-mass-gap-target"
    verdicts = [validate_concept(row, source, ym=ym) for row in rows if isinstance(row, dict)]
    if len(verdicts) != len(rows):
        fail(f"{rel(source)} visual_conceptualizations entries must be objects")
    if ym and not any(verdict in {"quarantine", "reject"} for verdict in verdicts):
        fail(f"{rel(source)} YM visual packet must quarantine or reject at least one analogy")
    workflow_caps = require_dict(packet.get("workflow_caps"), "workflow_caps", source)
    for field in ["max_reflection_passes_per_failed_major_cycle_set", "promotion_requires", "no_investment_verdict"]:
        if not clean_text(workflow_caps.get(field)):
            fail(f"{rel(source)} workflow_caps missing {field}")
    if int(workflow_caps.get("max_reflection_passes_per_failed_major_cycle_set", 0)) > 1:
        fail(f"{rel(source)} visual reflection pass cap must be 1 unless explicitly revised")
    require_list(packet.get("evidence_paths"), "evidence_paths", source)
    if packet.get("validation_handoff") != "agentic/scripts/validate_visual_conceptualization_packet.py":
        fail(f"{rel(source)} invalid validation_handoff")
    packet_text = clean_text(packet).lower()
    forbidden_secret_terms = ["api_key", "azure_openai_api_key", "openai_api_key", "authorization"]
    if any(term in packet_text for term in forbidden_secret_terms):
        fail(f"{rel(source)} appears to contain secret/config material")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    for raw in args.paths:
        path = Path(raw)
        validate_packet(load_json_object(path), path)
    print(f"validated {len(args.paths)} visual conceptualization packet(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
