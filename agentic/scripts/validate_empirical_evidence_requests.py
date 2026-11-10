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

"""Validate empirical evidence request packets."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


SCHEMA = ROOT / "agentic/spec/empirical_evidence_request.schema.json"
REPORT = ROOT / "agentic/reports/empirical_evidence_requests/latest.json"
MARKDOWN = ROOT / "agentic/reports/empirical_evidence_requests/latest.md"
TARGET_ID = "yang-mills-existence-and-mass-gap-target"


def flatten(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(flatten(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(flatten(item) for item in value)
    return clean_text(value)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_request(row: dict[str, Any], schema: dict[str, Any], index: int) -> None:
    subject = f"request {index} ({row.get('request_id', 'unknown')})"
    for field in schema["required_fields"]:
        require(field in row, f"{rel(REPORT)} {subject} missing `{field}`")
    for field in schema["list_fields"]:
        require(isinstance(row.get(field), list) and row[field], f"{rel(REPORT)} {subject} needs non-empty `{field}`")
    for field in schema["required_fields"]:
        if field not in schema["list_fields"]:
            require(clean_text(row.get(field)), f"{rel(REPORT)} {subject} has empty `{field}`")
    require(row["evidence_mode"] in schema["allowed_evidence_modes"], f"{rel(REPORT)} {subject} invalid evidence_mode")
    require(row["proximity_class"] in schema["allowed_proximity_classes"], f"{rel(REPORT)} {subject} invalid proximity_class")
    text = flatten(row).lower()
    marker_hits = [marker for marker in schema["required_yang_mills_markers"] if marker in text]
    require(len(marker_hits) >= 4, f"{rel(REPORT)} {subject} lacks Yang-Mills empirical markers")
    require("proof" in row["proof_boundary"].lower(), f"{rel(REPORT)} {subject} proof boundary must explicitly mention proof")
    require("theorem" in row["transfer_gap"].lower() or "proof" in row["transfer_gap"].lower(), f"{rel(REPORT)} {subject} transfer gap must name theorem/proof boundary")
    require("evidence-acquisition-planner" in row["skill_triggers"], f"{rel(REPORT)} {subject} must trigger evidence-acquisition-planner")
    for banned in ["proves the mass gap", "proves yang-mills", "certifies the theorem"]:
        require(banned not in text, f"{rel(REPORT)} {subject} overclaims empirical evidence: {banned}")


def main() -> int:
    schema = load_json_object(SCHEMA)
    report = load_json_object(REPORT)
    require(report.get("target_id") == TARGET_ID, f"{rel(REPORT)} target is not Yang-Mills")
    require(report.get("quality_gate") == "pass", f"{rel(REPORT)} quality gate is not pass")
    requests = report.get("requests", [])
    require(isinstance(requests, list) and len(requests) >= 4, f"{rel(REPORT)} needs at least four evidence requests")
    modes = {row.get("evidence_mode") for row in requests if isinstance(row, dict)}
    require({"empirical_probe", "negative_evidence", "source_import"} <= modes, f"{rel(REPORT)} missing required evidence modes")
    for index, row in enumerate(requests, start=1):
        require(isinstance(row, dict), f"{rel(REPORT)} request {index} must be an object")
        validate_request(row, schema, index)
    require(MARKDOWN.exists(), f"missing empirical evidence markdown: {rel(MARKDOWN)}")
    md = MARKDOWN.read_text(encoding="utf-8")
    for phrase in ["Empirical Evidence Requests", "Transfer gap", "Proof boundary", "Support Criteria", "Refutation Criteria"]:
        require(phrase in md, f"{rel(MARKDOWN)} missing visible phrase `{phrase}`")
    print(f"validated {len(requests)} empirical evidence requests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
