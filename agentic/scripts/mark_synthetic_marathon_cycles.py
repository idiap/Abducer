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
"""Mark legacy fast marathon cycles as synthetic rather than research cycles."""

from __future__ import annotations

import argparse

from agentic_common import ROOT, rel, utc_now, write_json
from discovery_marathon_common import load_cycles, load_run_state, run_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id")
    parser.add_argument("--reason", default="legacy cycles generated before research-mode timing and Codex branch execution were enforced")
    args = parser.parse_args()
    _, run_state = load_run_state(args.run_id)
    if not run_state:
        print("No active discovery marathon to repair.")
        return 0
    changed = 0
    synthetic = 0
    research = 0
    for cycle in load_cycles(run_state):
        if cycle.get("execution_mode") == "research" and cycle.get("valid_as_research_cycle"):
            research += 1
            continue
        if not cycle.get("execution_mode"):
            cycle["execution_mode"] = "synthetic_legacy"
            cycle["synthetic_reason"] = args.reason
            cycle["valid_as_research_cycle"] = False
            cycle["research_seconds_target"] = 0
            cycle["research_seconds_elapsed"] = 0
            cycle["timing_validation"] = {
                "status": "not_research",
                "reason": args.reason,
            }
            cycle["semantic_repair_utc"] = utc_now()
            write_json(run_dir(run_state["run_id"]) / "cycles" / f"{cycle['cycle_id']}.json", cycle)
            changed += 1
        if cycle.get("execution_mode") != "research":
            synthetic += 1
    run_state["research_cycle_count"] = research
    run_state["synthetic_cycle_count"] = synthetic
    run_state["cycle_semantics"] = {
        "cycle_count": "Total persisted cycle packets, including synthetic smoke/legacy packets.",
        "research_cycle_count": "Cycles that satisfied research-mode elapsed-time and branch-engine requirements.",
        "synthetic_cycle_count": "Cycles retained for audit/smoke evidence but not counted as research progress.",
    }
    run_state["updated_utc"] = utc_now()
    write_json(run_dir(run_state["run_id"]) / "run_state.json", run_state)
    print(f"Marked {changed} legacy cycles as synthetic in {rel(run_dir(run_state['run_id']))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
