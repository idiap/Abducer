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
"""Validate cycle failure archaeology packets."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from agentic_common import clean_text, fail, load_json_object, rel


REQUIRED_TOP_LEVEL = [
    "schema",
    "generated_utc",
    "generated_by_skills",
    "cycle_set",
    "failure_detected",
    "failure_summary",
    "smallest_honest_failed_hypothesis",
    "hard_problem_diagnosis",
    "why_failed",
    "why_not_anticipated",
    "anticipation_heuristics",
    "learning_for_future_cycles",
    "required_workflow_change",
    "route_disposition",
    "evidence_paths",
    "validation_handoff",
]

ALLOWED_DISPOSITIONS = {
    "persist_with_new_artifact_gate",
    "reframe_before_investment",
    "demote_to_support_only",
    "falsifier_or_negative_result",
    "quarantine_until_new_evidence",
    "stop",
    "persist_with_explicit_premortem",
}


def require_list(packet: dict[str, Any], field: str, source: Path, min_items: int = 1) -> list[Any]:
    value = packet.get(field)
    if not isinstance(value, list) or len([item for item in value if clean_text(item)]) < min_items:
        fail(f"{rel(source)} {field} must contain at least {min_items} item(s)")
    return value


def validate_packet(packet: dict[str, Any], source: Path) -> None:
    for field in REQUIRED_TOP_LEVEL:
        if field == "failure_detected":
            if not isinstance(packet.get(field), bool):
                fail(f"{rel(source)} failure_detected must be boolean")
        elif not clean_text(packet.get(field)):
            fail(f"{rel(source)} missing {field}")
    if packet.get("schema") != "abducer.cycle_failure_archaeology.v1":
        fail(f"{rel(source)} invalid schema {packet.get('schema')}")
    cycle_set = packet.get("cycle_set")
    if not isinstance(cycle_set, dict):
        fail(f"{rel(source)} cycle_set must be an object")
    for field in ["cycle_set_id", "target_id", "run_id", "cycle_ids", "branch_ids", "window_policy"]:
        if not clean_text(cycle_set.get(field)):
            fail(f"{rel(source)} cycle_set missing {field}")
    if not isinstance(cycle_set.get("cycle_ids"), list) or not cycle_set.get("cycle_ids"):
        fail(f"{rel(source)} cycle_set.cycle_ids must be a non-empty list")
    hypothesis = packet.get("smallest_honest_failed_hypothesis")
    if not isinstance(hypothesis, dict):
        fail(f"{rel(source)} smallest_honest_failed_hypothesis must be an object")
    for field in ["claim", "source_object", "target_object"]:
        if not clean_text(hypothesis.get(field)):
            fail(f"{rel(source)} smallest_honest_failed_hypothesis missing {field}")
    diagnosis = packet.get("hard_problem_diagnosis")
    if not isinstance(diagnosis, dict):
        fail(f"{rel(source)} hard_problem_diagnosis must be an object")
    for field in ["physics_hardness", "mathematical_hardness", "representation_hardness"]:
        require_list(diagnosis, field, source)
    require_list(packet, "why_failed", source)
    require_list(packet, "why_not_anticipated", source, min_items=2)
    require_list(packet, "learning_for_future_cycles", source)
    require_list(packet, "required_workflow_change", source)
    if packet.get("route_disposition") not in ALLOWED_DISPOSITIONS:
        fail(f"{rel(source)} invalid route_disposition {packet.get('route_disposition')}")
    heuristics = packet.get("anticipation_heuristics")
    if not isinstance(heuristics, list) or len(heuristics) < 4:
        fail(f"{rel(source)} anticipation_heuristics must contain at least four heuristics")
    detected_count = 0
    for index, row in enumerate(heuristics):
        if not isinstance(row, dict):
            fail(f"{rel(source)} anticipation_heuristics[{index}] must be an object")
        for field in ["signature", "detected", "why_it_matters", "prompt_heuristic", "pre_cycle_gate"]:
            if field == "detected":
                if not isinstance(row.get(field), bool):
                    fail(f"{rel(source)} anticipation_heuristics[{index}].detected must be boolean")
            elif not clean_text(row.get(field)):
                fail(f"{rel(source)} anticipation_heuristics[{index}] missing {field}")
        detected_count += int(bool(row.get("detected")))
    if packet.get("failure_detected") and detected_count == 0:
        fail(f"{rel(source)} failure_detected requires at least one detected heuristic")
    if "failure-archaeology-explainer" not in packet.get("generated_by_skills", []):
        fail(f"{rel(source)} must cite failure-archaeology-explainer")
    if "failed-hypothesis-anticipator" not in packet.get("generated_by_skills", []):
        fail(f"{rel(source)} must cite failed-hypothesis-anticipator")
    if packet.get("validation_handoff") != "agentic/scripts/validate_cycle_failure_archaeology.py":
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
    print(f"validated {len(args.paths)} cycle failure archaeology packet(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
