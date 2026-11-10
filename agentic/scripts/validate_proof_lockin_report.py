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
"""Validate target-scoped proof lock-in reports."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel, slugify


REPORT_ROOT = ROOT / "agentic/reports/proof_lockin/targets"
ALLOWED_MODES = {"exploratory", "exploration_continue", "lock_in_active", "lock_in_ready", "packaging", "released_to_exploration", "demoted", "forced_demote", "blocked"}


def require_nonempty(value: Any, source: Path, field: str) -> None:
    if not clean_text(value):
        fail(f"{rel(source)} missing {field}")


def require_dict(payload: dict[str, Any], source: Path, field: str) -> dict[str, Any]:
    value = payload.get(field)
    if not isinstance(value, dict):
        fail(f"{rel(source)} {field} must be an object")
    return value


def require_list(payload: dict[str, Any], source: Path, field: str) -> list[Any]:
    value = payload.get(field)
    if not isinstance(value, list) or not value:
        fail(f"{rel(source)} {field} must be a nonempty list")
    return value


def validate_main_problem_balance(payload: dict[str, Any], path: Path, target_id: str) -> None:
    balance = require_dict(payload, path, "main_problem_balance")
    for field in ["local_subgoal_scope", "larger_problem_boundary", "allowed_claim", "balance_test"]:
        require_nonempty(balance.get(field), path, f"main_problem_balance.{field}")
    forbidden = require_list(balance, path, "forbidden_claims")
    gate_map = require_list(balance, path, "larger_problem_gate_map")
    if target_id == "yang-mills-existence-and-mass-gap-target":
        boundary = clean_text(balance.get("larger_problem_boundary")).lower()
        if "mass gap" not in boundary or ("os" not in boundary and "wightman" not in boundary):
            fail(f"{rel(path)} YM balance must preserve OS/Wightman and mass gap as larger-problem boundaries")
        if not any("continuum" in clean_text(item).lower() for item in gate_map):
            fail(f"{rel(path)} YM balance gate map must include the continuum gate")
        if not any("mass gap" in clean_text(item).lower() for item in forbidden):
            fail(f"{rel(path)} YM forbidden claims must explicitly block local-to-mass-gap overclaiming")


def validate_publication_consolidation(payload: dict[str, Any], path: Path) -> None:
    control = require_dict(payload, path, "publication_consolidation_control")
    for field in [
        "status",
        "recursion_guard",
        "budget_exhaustion_action",
        "reentry_condition",
    ]:
        require_nonempty(control.get(field), path, f"publication_consolidation_control.{field}")
    allowed = require_list(control, path, "allowed_cycle_types")
    stops = require_list(control, path, "stop_conditions")
    try:
        max_cycles = int(control.get("max_completion_cycles"))
        max_depth = int(control.get("max_recursion_depth"))
        current_depth = int(control.get("current_recursion_depth"))
    except (TypeError, ValueError):
        fail(f"{rel(path)} publication consolidation limits must be integers")
    if max_cycles < 1 or max_cycles > 4:
        fail(f"{rel(path)} max_completion_cycles must be between 1 and 4")
    if max_depth < 0 or max_depth > 1:
        fail(f"{rel(path)} max_recursion_depth must be 0 or 1")
    if current_depth < 0 or current_depth > max_depth:
        fail(f"{rel(path)} current_recursion_depth exceeds max_recursion_depth")
    if "budget_exhausted_release_to_exploration" not in {clean_text(item) for item in stops}:
        fail(f"{rel(path)} consolidation stop conditions must include budget_exhausted_release_to_exploration")
    guard = clean_text(control.get("recursion_guard")).lower()
    if "nested" not in guard and "recursion" not in guard:
        fail(f"{rel(path)} recursion guard must explicitly block nested consolidation")
    if len(allowed) > max_cycles + 2:
        fail(f"{rel(path)} allowed cycle types are broader than the consolidation budget")


def validate_report(path: Path) -> None:
    payload = load_json_object(path)
    target_id = clean_text(payload.get("target_id"))
    require_nonempty(target_id, path, "target_id")
    if path.parent.name != slugify(target_id):
        fail(f"{rel(path)} path target slug does not match target_id {target_id}")
    mode = clean_text(payload.get("mode"))
    if mode not in ALLOWED_MODES:
        fail(f"{rel(path)} invalid mode {mode}")
    for field in [
        "conceptual_quality_basis",
        "paper_relevance",
        "next_allowed_action",
        "transfer_substance_verdict",
        "definition_expansion_result",
        "failure_case_status",
        "return_to_exploration_note",
        "validation_handoff",
    ]:
        require_nonempty(payload.get(field), path, field)
    if not isinstance(payload.get("non_claims"), list) or not payload["non_claims"]:
        fail(f"{rel(path)} non_claims must be a nonempty list")
    validate_main_problem_balance(payload, path, target_id)
    validate_publication_consolidation(payload, path)
    cycle_budget = int(payload.get("cycle_budget", 0) or 0)
    max_cycles = int(payload["publication_consolidation_control"]["max_completion_cycles"])
    if cycle_budget > max_cycles:
        fail(f"{rel(path)} cycle_budget exceeds max_completion_cycles")
    if mode == "lock_in_ready" and not clean_text(payload.get("frozen_subgoal")):
        fail(f"{rel(path)} lock_in_ready report must name frozen_subgoal")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    paths = [Path(raw) for raw in args.paths] if args.paths else sorted(REPORT_ROOT.glob("*/latest.json"))
    if not paths:
        fail("no proof lock-in reports found; run agentic/scripts/build_proof_lockin_report.py")
    for path in paths:
        validate_report(path)
    print(f"validated {len(paths)} proof lock-in report(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
