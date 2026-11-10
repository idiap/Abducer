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
"""Validate the cumulative result/subgoal atlas."""

from __future__ import annotations

import argparse
import contextlib
import io
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel
from target_profiles import target_profile


ATLAS = ROOT / "agentic/reports/result_subgoal_atlas/latest.json"
FIXTURE_DIR = ROOT / "tests/fixtures/result_subgoal_atlas"
ALLOWED_STATUS = {"achieved", "partially_achieved", "open", "blocked", "falsified", "quarantined", "handoff_ready"}
REQUIRED_ENTRY_FIELDS = [
    "result_id",
    "target_id",
    "subgoal_id",
    "result_kind",
    "claim",
    "achievement_status",
    "problem_space_coordinates",
    "dependencies",
    "derivations",
    "evidence_sources",
    "validation_state",
    "open_obligations",
    "promotion_criteria",
    "demotion_criteria",
    "paper_relevance",
    "non_claims",
]


def validate_entry(entry: dict[str, Any], source: Path, index: int, target_id: str) -> None:
    for field in REQUIRED_ENTRY_FIELDS:
        if field not in entry or (field not in {"dependencies", "derivations"} and not entry.get(field)):
            fail(f"{rel(source)} result {index} missing {field}")
    if entry.get("target_id") != target_id:
        fail(f"{rel(source)} result {index} target_id mismatch")
    if entry.get("achievement_status") not in ALLOWED_STATUS:
        fail(f"{rel(source)} result {index} invalid achievement_status {entry.get('achievement_status')}")
    coords = entry.get("problem_space_coordinates", {})
    for field in ["route_family", "global_problem_role"]:
        if not clean_text(coords.get(field)):
            fail(f"{rel(source)} result {index} missing problem_space_coordinates.{field}")
    for list_field in ["evidence_sources", "open_obligations", "promotion_criteria", "demotion_criteria", "non_claims"]:
        if not isinstance(entry.get(list_field), list) or not entry.get(list_field):
            fail(f"{rel(source)} result {index} needs nonempty {list_field}")
    validation = entry.get("validation_state", {})
    if not isinstance(validation, dict) or not clean_text(validation.get("status")):
        fail(f"{rel(source)} result {index} needs validation_state.status")
    if entry.get("achievement_status") in {"achieved", "handoff_ready"} and validation.get("status") in {"", "not_assessed", "candidate"}:
        fail(f"{rel(source)} result {index} cannot be {entry.get('achievement_status')} without validation state")
    text = clean_text(entry).lower()
    forbidden = [term for term in target_profile(target_id).get("forbidden_cross_target_terms", []) if term in text]
    if forbidden:
        fail(f"{rel(source)} result {index} contains cross-target terms: {sorted(set(forbidden))}")


def validate_atlas(payload: dict[str, Any], source: Path) -> None:
    for field in ["version", "generated_utc", "target_id", "source_artifacts", "summary", "subgoals", "results", "problem_space_index", "validation_handoff"]:
        if not payload.get(field):
            fail(f"{rel(source)} missing {field}")
    target_id = clean_text(payload.get("target_id"))
    results = payload.get("results", [])
    subgoals = payload.get("subgoals", [])
    if not isinstance(results, list) or len(results) < 3:
        fail(f"{rel(source)} needs at least three durable result entries")
    if not isinstance(subgoals, list) or not subgoals:
        fail(f"{rel(source)} needs subgoals")
    result_ids = set()
    for index, row in enumerate(results, start=1):
        if not isinstance(row, dict):
            fail(f"{rel(source)} result {index} must be an object")
        validate_entry(row, source, index, target_id)
        result_id = clean_text(row.get("result_id"))
        if result_id in result_ids:
            fail(f"{rel(source)} duplicate result_id {result_id}")
        result_ids.add(result_id)
    for index, subgoal in enumerate(subgoals, start=1):
        for field in ["subgoal_id", "title", "target_id", "result_count", "status", "result_ids", "open_obligations"]:
            if not subgoal.get(field):
                fail(f"{rel(source)} subgoal {index} missing {field}")
        unknown = [item for item in subgoal.get("result_ids", []) if item not in result_ids]
        if unknown:
            fail(f"{rel(source)} subgoal {index} cites unknown results: {unknown}")
    index = payload.get("problem_space_index", {})
    if not isinstance(index, dict) or not index:
        fail(f"{rel(source)} needs problem_space_index")
    joined = clean_text(payload).lower()
    if target_id == "p-vs-np-target":
        for marker in ["sat", "circuit", "p/poly", "mcsp", "lower bound"]:
            if marker not in joined:
                fail(f"{rel(source)} P vs NP atlas lacks `{marker}`")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    paths = [Path(path) for path in args.paths] if args.paths else [ATLAS]
    checked = 0
    for path in paths:
        validate_atlas(load_json_object(path), path)
        checked += 1
    if not args.paths:
        valid = FIXTURE_DIR / "valid_pvsnp_atlas.json"
        if valid.exists():
            validate_atlas(load_json_object(valid), valid)
            checked += 1
        invalid = FIXTURE_DIR / "invalid_cross_target_atlas.json"
        if invalid.exists():
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    validate_atlas(load_json_object(invalid), invalid)
            except SystemExit:
                pass
            else:
                fail(f"{rel(invalid)} should fail validation")
    print(f"validated {checked} result subgoal atlas file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
