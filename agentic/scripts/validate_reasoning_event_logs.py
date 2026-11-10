#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Validate visible reasoning-progress logs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


SCHEMA = ROOT / "agentic/spec/reasoning_event_log_schema.json"
LOGS = ROOT / "agentic/traces/reasoning_events"
REPORT = ROOT / "agentic/reports/reasoning_progress/latest.json"


def require_list(row: dict[str, Any], field: str, path: Path, line_no: int) -> list[Any]:
    value = row.get(field)
    if not isinstance(value, list):
        fail(f"{rel(path)}:{line_no} {field} must be a list")
    return value


def validate_row(row: dict[str, Any], schema: dict[str, Any], path: Path, line_no: int) -> None:
    missing = set(schema["required_fields"]) - set(row)
    if missing:
        fail(f"{rel(path)}:{line_no} missing fields: {', '.join(sorted(missing))}")
    if row["event_type"] not in schema["allowed_event_types"]:
        fail(f"{rel(path)}:{line_no} unknown event_type: {row['event_type']}")
    if row["epistemic_status"] not in schema["allowed_epistemic_status"]:
        fail(f"{rel(path)}:{line_no} unknown epistemic_status: {row['epistemic_status']}")
    for field in ["title", "narrative_summary", "conceptual_move", "uncertainty"]:
        if not clean_text(row.get(field)):
            fail(f"{rel(path)}:{line_no} {field} must be non-empty")
    for field in ["mathematical_objects", "target_commitments", "evidence_paths", "proof_obligations"]:
        require_list(row, field, path, line_no)
    if not row["mathematical_objects"]:
        fail(f"{rel(path)}:{line_no} needs at least one mathematical object")
    if not row["target_commitments"]:
        fail(f"{rel(path)}:{line_no} needs at least one target commitment")
    for evidence in row["evidence_paths"]:
        if not isinstance(evidence, str) or not evidence.strip():
            fail(f"{rel(path)}:{line_no} evidence paths must be non-empty strings")
        if evidence != "explicit-unknown" and not (ROOT / evidence).exists():
            fail(f"{rel(path)}:{line_no} evidence path does not exist: {evidence}")
    visual = row.get("visual_encoding")
    if not isinstance(visual, dict):
        fail(f"{rel(path)}:{line_no} visual_encoding must be an object")
    for field in schema["visual_encoding_required_fields"]:
        if not clean_text(visual.get(field)):
            fail(f"{rel(path)}:{line_no} visual_encoding missing {field}")
    if visual["lane"] not in schema["allowed_lanes"]:
        fail(f"{rel(path)}:{line_no} unknown visual lane: {visual['lane']}")
    if visual["salience"] not in schema["allowed_salience"]:
        fail(f"{rel(path)}:{line_no} unknown visual salience: {visual['salience']}")


def validate_log(path: Path, schema: dict[str, Any]) -> int:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"{rel(path)}:{line_no} invalid JSON: {exc}")
        if not isinstance(row, dict):
            fail(f"{rel(path)}:{line_no} row must be an object")
        validate_row(row, schema, path, line_no)
        rows.append(row)
    if not rows:
        fail(f"{rel(path)} is empty")
    event_types = {row["event_type"] for row in rows}
    required_types = {"target_spine", "dependency_frontier", "conceptual_pressure", "route_ranking", "drift_guard", "subgoal_control_decision"}
    missing = required_types - event_types
    if missing:
        fail(f"{rel(path)} missing required communication event types: {', '.join(sorted(missing))}")
    if any(row.get("target_id") == "yang-mills-existence-and-mass-gap-target" for row in rows):
        text = clean_text(rows).lower()
        for marker in ["gauge-field", "spectral", "observable", "continuum", "same-theory"]:
            if marker not in text:
                fail(f"{rel(path)} Yang-Mills reasoning log lacks physics-facing marker `{marker}`")
    for row in rows:
        if row["event_type"] != "subgoal_control_decision":
            continue
        text = clean_text(row).lower()
        for marker in ["persist", "backtrack", "pivot", "quarantine", "stop", "learning", "next action"]:
            if marker not in text:
                fail(f"{rel(path)}:{row.get('event_id')} subgoal control event lacks `{marker}`")
    return len(rows)


def main() -> int:
    schema = load_json_object(SCHEMA)
    paths = sorted(LOGS.glob("*.jsonl"))
    if not paths:
        fail("no reasoning event logs found")
    total = sum(validate_log(path, schema) for path in paths)
    report = load_json_object(REPORT)
    if report.get("event_count") != total and len(paths) == 1:
        fail(f"{rel(REPORT)} event_count does not match log rows")
    print(f"validated {total} reasoning events across {len(paths)} log files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
