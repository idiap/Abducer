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
"""Switch the active discovery marathon pointer without mixing target runs."""

from __future__ import annotations

import argparse

from agentic_common import ROOT, fail, load_optional_json, rel
from discovery_marathon_common import load_run_state, target_active_pointer_path, write_active_run_pointers
from init_discovery_marathon import build_initial_state, persist_run
from target_profiles import DEFAULT_TARGET_ID, target_profile


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=DEFAULT_TARGET_ID)
    parser.add_argument("--run-id", help="Optional explicit run id to activate for the target.")
    parser.add_argument("--init-if-missing", action="store_true", help="Initialize a new target-specific run if no pointer exists.")
    parser.add_argument("--hours", type=float, default=6)
    parser.add_argument("--cycle-minutes", type=int, default=30)
    parser.add_argument("--max-active-branches", type=int, default=3)
    args = parser.parse_args()

    profile = target_profile(args.target)
    if args.run_id:
        path, run_state = load_run_state(args.run_id)
        if not run_state:
            fail(f"run id {args.run_id} does not resolve to a run state")
        if run_state.get("target_id") != args.target:
            fail(f"run {args.run_id} belongs to {run_state.get('target_id')}, not {args.target}")
    else:
        pointer = load_optional_json(target_active_pointer_path(args.target))
        if not pointer and args.init_if_missing:
            run_state, branches = build_initial_state(
                args.target,
                args.hours,
                args.cycle_minutes,
                args.max_active_branches,
                run_id=f"{profile['slug']}-marathon",
            )
            persist_run(run_state, branches)
            pointer = load_optional_json(target_active_pointer_path(args.target))
        if not pointer:
            fail(f"no run pointer exists for {args.target}; rerun with --init-if-missing")
        path, run_state = load_run_state(pointer.get("run_id"))
        if not run_state:
            fail(f"{rel(target_active_pointer_path(args.target))} points to a missing run")
        if run_state.get("target_id") != args.target:
            fail(f"{rel(path)} target_id is {run_state.get('target_id')}, expected {args.target}")

    write_active_run_pointers(run_state)
    print(
        f"Active discovery target: {profile['display_name']} "
        f"({run_state['target_id']}) via {run_state['run_id']} at {rel(ROOT / run_state['branch_registry'][0]['local_memory_path'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
