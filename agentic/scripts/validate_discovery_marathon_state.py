#!/usr/bin/env python3
"""Validate active discovery-marathon state."""

from __future__ import annotations

from agentic_common import ROOT, clean_text, fail, load_json_object, rel
from discovery_marathon_common import ACTIVE_POINTER, TARGET_ACTIVE_DIR, branch_path, load_branches, load_cycles, load_run_state, target_active_pointer_path
from validate_discovery_marathon_cycle import validate_cycle


def main() -> int:
    if not ACTIVE_POINTER.exists():
        print("No active discovery marathon pointer; state validator is idle.")
        return 0
    pointer = load_json_object(ACTIVE_POINTER)
    path, run_state = load_run_state(pointer.get("run_id"))
    if not run_state:
        fail(f"{rel(ACTIVE_POINTER)} points to missing run state")
    for field in ["run_id", "target_id", "status", "created_utc", "updated_utc", "wall_clock_budget_minutes", "cycle_minutes", "branch_registry", "active_branch_ids", "checkpoint_policy", "artifact_lineage", "validator_history"]:
        if field not in run_state:
            fail(f"{rel(path)} missing {field}")
    if run_state["status"] not in {"initialized", "running", "paused", "completed", "failed"}:
        fail(f"{rel(path)} has invalid status {run_state['status']}")
    target_pointer = target_active_pointer_path(run_state["target_id"])
    if not target_pointer.exists():
        fail(f"{rel(path)} missing per-target active pointer {rel(target_pointer)}")
    target_pointer_payload = load_json_object(target_pointer)
    if target_pointer_payload.get("run_id") != run_state["run_id"]:
        fail(f"{rel(target_pointer)} does not point at active run {run_state['run_id']}")
    if TARGET_ACTIVE_DIR.exists():
        for pointer_path in sorted(TARGET_ACTIVE_DIR.glob("*.json")):
            target_payload = load_json_object(pointer_path)
            pointer_run_id = clean_text(target_payload.get("run_id"))
            pointer_target_id = clean_text(target_payload.get("target_id"))
            if not pointer_run_id or not pointer_target_id:
                fail(f"{rel(pointer_path)} must include run_id and target_id")
            target_run_path, target_run_state = load_run_state(pointer_run_id)
            if not target_run_state:
                fail(f"{rel(pointer_path)} points to missing run state")
            if target_run_state.get("target_id") != pointer_target_id:
                fail(f"{rel(pointer_path)} target_id does not match pointed run state")
    branch_ids = set()
    for branch in load_branches(run_state):
        branch_ids.add(branch["branch_id"])
        for field in ["branch_id", "title", "status", "priority", "target_profile", "machinery_role", "controlled_interface", "hypothesis", "mathematical_mechanism", "attempt_count", "consecutive_low_learning_cycles", "skill_requirements", "promotion_signal", "pivot_signal", "local_memory"]:
            if field not in branch:
                fail(f"{rel(ROOT / branch.get('local_memory_path', 'missing'))} missing {field}")
        if "->" not in branch.get("controlled_interface", ""):
            fail(f"{rel(ROOT / branch['local_memory_path'])} controlled_interface needs an arrow")
    missing_active = [branch_id for branch_id in run_state.get("active_branch_ids", []) if branch_id not in branch_ids]
    if missing_active:
        fail(f"{rel(path)} active_branch_ids missing branch files: {missing_active}")
    for cycle in load_cycles(run_state):
        validate_cycle(cycle, ROOT / f"agentic/runs/discovery_marathons/{run_state['run_id']}/cycles/{cycle['cycle_id']}.json")
    print(f"validated discovery marathon state {run_state['run_id']} with {len(branch_ids)} branches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
