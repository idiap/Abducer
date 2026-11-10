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
"""Validate the parallel API branch-execution contract for marathon cycles."""

from __future__ import annotations

import argparse
import contextlib
import io
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


def validate_parallel_cycle_packet(cycle: dict[str, Any], source: Path) -> None:
    parallel = cycle.get("parallel_execution")
    synthesis = cycle.get("parallel_synthesis")
    if not isinstance(parallel, dict):
        fail(f"{rel(source)} missing parallel_execution object")
    if not isinstance(synthesis, dict):
        fail(f"{rel(source)} missing parallel_synthesis object")
    if not parallel.get("enabled"):
        fail(f"{rel(source)} must exercise enabled parallel execution")
    if int(parallel.get("max_workers", 0)) < 2:
        fail(f"{rel(source)} enabled parallel execution needs max_workers >= 2")
    if parallel.get("merge_policy") != "scheduler_order_single_writer":
        fail(f"{rel(source)} must declare scheduler_order_single_writer merge policy")
    if "serialized" not in clean_text(parallel.get("state_mutation_policy")).lower():
        fail(f"{rel(source)} state mutation policy must be serialized")
    selected = cycle.get("selected_branch_ids", [])
    outputs = cycle.get("branch_outputs", [])
    records = cycle.get("branch_execution_records", [])
    if not selected or len(outputs) != len(selected) or len(records) != len(selected):
        fail(f"{rel(source)} selected branches, outputs, and records must have matching nonzero lengths")
    if [output.get("branch_id") for output in outputs] != selected:
        fail(f"{rel(source)} branch_outputs must stay in selected scheduler order")
    if synthesis.get("cited_branch_ids") != selected:
        fail(f"{rel(source)} synthesis cited_branch_ids must match selected scheduler order")
    for index, record in enumerate(records):
        if record.get("status") != "complete":
            fail(f"{rel(source)} branch_execution_records[{index}] is not complete")
        if record.get("engine") != "azure_responses_api":
            fail(f"{rel(source)} branch_execution_records[{index}] must use azure_responses_api")
        if int(record.get("parallel_worker_index", -1)) != index:
            fail(f"{rel(source)} branch_execution_records[{index}] worker index must match scheduler order")
        if int(record.get("parallel_max_workers", 0)) < 2:
            fail(f"{rel(source)} branch_execution_records[{index}] missing max worker metadata")
    for field in ["common_proof_obligations", "cross_branch_conflicts", "no_go_opportunities", "queue_promotions"]:
        if field not in synthesis:
            fail(f"{rel(source)} parallel_synthesis missing {field}")
    if not synthesis["common_proof_obligations"]:
        fail(f"{rel(source)} parallel_synthesis needs common proof obligations")
    promotions = synthesis.get("queue_promotions", [])
    if not isinstance(promotions, list) or not promotions:
        fail(f"{rel(source)} parallel_synthesis needs queue promotions")
    for item in promotions:
        if not isinstance(item, dict):
            fail(f"{rel(source)} queue promotion must be an object")
        for field in [
            "pressure_family",
            "cited_branch_ids",
            "next_analysis",
            "promotion_test",
            "novelty_signal",
            "high_reward_payoff",
            "step_back_or_pivot_criterion",
        ]:
            if not clean_text(item.get(field)):
                fail(f"{rel(source)} queue promotion missing {field}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    paths = [Path(path) for path in args.paths]
    if not paths:
        paths = [ROOT / "tests/fixtures/discovery_marathon/parallel_api_cycle.valid.json"]
        invalid = ROOT / "tests/fixtures/discovery_marathon/parallel_api_cycle.invalid.json"
        if invalid.exists():
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    validate_parallel_cycle_packet(load_json_object(invalid), invalid)
            except SystemExit:
                pass
            else:
                fail(f"{rel(invalid)} should fail parallel API validation")
    for path in paths:
        validate_parallel_cycle_packet(load_json_object(path), path)
    print(f"validated {len(paths)} parallel API marathon packet(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
