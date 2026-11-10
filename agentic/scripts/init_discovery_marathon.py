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
"""Initialize a durable long-horizon discovery marathon."""

from __future__ import annotations

import argparse
from typing import Any

from agentic_common import ROOT, rel, stable_id, utc_now, write_json
from discovery_marathon_common import (
    MARATHON_ROOT,
    branch_path,
    default_branch,
    dump_stdout,
    run_dir,
    write_active_run_pointers,
    stretch_programs,
    write_markdown,
)
from target_profiles import DEFAULT_TARGET_ID, target_profile


def build_initial_state(target_id: str, hours: float, cycle_minutes: int, max_active_branches: int, run_id: str | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    profile = target_profile(target_id)
    selected_run_id = run_id or stable_id("marathon.run", target_id, utc_now())
    programs = stretch_programs(target_id)
    branches = [default_branch(program, selected_run_id, target_id, index + 1) for index, program in enumerate(programs)]
    if profile["target_id"] == "p-vs-np-target":
        checkpoint_policy = {
            "cycle_budget_is_metadata": True,
            "persist_condition": "A branch may continue only when it sharpens source model, target class, reduction, threshold, barrier status, or bridge obligation.",
            "backtrack_condition": "Backtrack when a branch imports a wrong source model, wrong target class, nonuniform leakage, barrier mismatch, or collapsed quantitative threshold.",
            "pivot_condition": "Pivot after repeated certified failure if another branch protects more target commitments with clearer complexity-theoretic machinery.",
            "review_every_cycles": 3,
        }
        artifact_lineage = [
            "agentic/examples/targets/p-vs-np-target.json",
            "agentic/state/dependency_graphs/p-vs-np.json",
            "artifacts/p-vs-np/proof-strategies.json",
            "agentic/registries/discovery_marathon_skill_dispatch.yaml",
            "agentic/spec/discovery_marathon_run.schema.json",
        ]
    else:
        checkpoint_policy = {
            "cycle_budget_is_metadata": True,
            "persist_condition": "A branch may continue only when failures sharpen definitions, assumptions, equations, or bridge obligations.",
            "backtrack_condition": "Backtrack when a branch imports a wrong object, wrong cutoff, wrong reconstruction stage, or wrong observable family.",
            "pivot_condition": "Pivot after repeated certified failure if another branch protects more target commitments with clearer machinery.",
            "review_every_cycles": 3,
        }
        artifact_lineage = [
            "agentic/reports/discovery_stretch/latest.json",
            "agentic/registries/discovery_marathon_skill_dispatch.yaml",
            "agentic/spec/discovery_marathon_run.schema.json",
        ]
    state = {
        "version": 1,
        "run_id": selected_run_id,
        "target_id": target_id,
        "target_profile": {
            "slug": profile["slug"],
            "display_name": profile["display_name"],
            "domain": profile["domain"],
            "strategy_tab_label": profile["strategy_tab_label"],
            "story_tab_label": profile["story_tab_label"],
        },
        "status": "initialized",
        "created_utc": utc_now(),
        "updated_utc": utc_now(),
        "wall_clock_budget_minutes": int(hours * 60),
        "cycle_minutes": cycle_minutes,
        "max_active_branches": max_active_branches,
        "cycle_count": 0,
        "branch_registry": [
            {
                "branch_id": branch["branch_id"],
                "title": branch["title"],
                "status": branch["status"],
                "priority": branch["priority"],
                "local_memory_path": branch["local_memory_path"],
            }
            for branch in branches
        ],
        "active_branch_ids": [branch["branch_id"] for branch in branches if branch["status"] == "active"][:max_active_branches],
        "checkpoint_policy": checkpoint_policy,
        "artifact_lineage": artifact_lineage,
        "validator_history": [],
    }
    return state, branches


def persist_run(state: dict[str, Any], branches: list[dict[str, Any]]) -> None:
    root = run_dir(state["run_id"])
    write_json(root / "run_state.json", state)
    for branch in branches:
        write_json(branch_path(state["run_id"], branch["branch_id"]), branch)
        write_markdown(
            branch_path(state["run_id"], branch["branch_id"]).with_suffix(".md"),
            f"# {branch['title']}\n\nControlled interface: `{branch['controlled_interface']}`\n\n{branch['hypothesis']}\n",
        )
    write_active_run_pointers(state)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=DEFAULT_TARGET_ID)
    parser.add_argument("--hours", type=float, default=6)
    parser.add_argument("--cycle-minutes", type=int, default=30)
    parser.add_argument("--max-active-branches", type=int, default=3)
    parser.add_argument("--run-id")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    MARATHON_ROOT.mkdir(parents=True, exist_ok=True)
    state, branches = build_initial_state(args.target, args.hours, args.cycle_minutes, args.max_active_branches, args.run_id)
    if args.dry_run:
        dump_stdout({"run_state": state, "branches": branches})
        return 0
    persist_run(state, branches)
    print(f"Wrote {rel(ROOT / state['branch_registry'][0]['local_memory_path'])} and {rel(run_dir(state['run_id']) / 'run_state.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
