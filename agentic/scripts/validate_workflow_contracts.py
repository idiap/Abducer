#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Validate legacy and named workflow contracts plus complete skill disposition."""

from __future__ import annotations

from agentic_common import ROOT, clean_text, fail, load_json_object, rel, repo_path, skill_dir_by_name


CONTRACTS = ROOT / "agentic" / "registries" / "workflow_contracts.yaml"


def _path_without_fragment(value: str) -> str:
    return value.split("#", 1)[0]


def _validate_named_workflows(payload: dict, legacy_ids: set[str]) -> tuple[set[str], set[str]]:
    named_path = repo_path(clean_text(payload.get("named_workflow_contracts")), must_exist=True)
    named = load_json_object(named_path)
    if named.get("version") != 2:
        fail(f"{rel(named_path)} must use version 2")
    repo_path(clean_text(named.get("contract_schema")), must_exist=True)
    repo_path(clean_text(named.get("artifact_schema")), must_exist=True)
    rows = named.get("workflows")
    if not isinstance(rows, list) or not rows:
        fail(f"{rel(named_path)} must declare at least one named workflow")
    all_ids = set(legacy_ids)
    named_ids: set[str] = set()
    assigned_skills: set[str] = set()
    allowed_modes = {"required", "conditional", "advisory", "validator_only"}
    hook_events = {"UserPromptSubmit", "PreSkillUse", "PostSkillUse", "PreToolUse", "Stop"}
    profile_ids: set[str] = set()
    for row in rows:
        workflow_id = clean_text(row.get("id")) if isinstance(row, dict) else ""
        if not workflow_id or workflow_id in all_ids:
            fail(f"{rel(named_path)} missing or duplicate workflow id: {workflow_id}")
        all_ids.add(workflow_id)
        named_ids.add(workflow_id)
        for field in ["version", "visible_name", "activation", "owner_skill", "cost_profile"]:
            if not clean_text(row.get(field)):
                fail(f"{rel(named_path)} workflow {workflow_id} needs {field}")
        aliases = row.get("aliases")
        if not isinstance(aliases, list) or not aliases or len(aliases) != len(set(aliases)):
            fail(f"{rel(named_path)} workflow {workflow_id} needs unique projection aliases")
        owner = clean_text(row.get("owner_skill"))
        if skill_dir_by_name(owner) is None:
            fail(f"{rel(named_path)} workflow {workflow_id} owner skill missing: {owner}")
        trigger = row.get("trigger")
        if not isinstance(trigger, dict) or set(trigger) != {"all_of", "any_of", "none_of"}:
            fail(f"{rel(named_path)} workflow {workflow_id} has invalid trigger")
        input_artifact = row.get("input_artifact")
        if not isinstance(input_artifact, dict) or not clean_text(input_artifact.get("type")):
            fail(f"{rel(named_path)} workflow {workflow_id} has invalid input artifact")
        repo_path(_path_without_fragment(clean_text(input_artifact.get("schema"))), must_exist=True)
        steps = row.get("steps")
        if not isinstance(steps, list) or not steps:
            fail(f"{rel(named_path)} workflow {workflow_id} needs steps")
        orders = [step.get("order") for step in steps if isinstance(step, dict)]
        if len(orders) != len(steps) or orders != sorted(orders) or len(orders) != len(set(orders)):
            fail(f"{rel(named_path)} workflow {workflow_id} step order must be unique and ascending")
        step_ids: set[str] = set()
        for step in steps:
            step_id = clean_text(step.get("id"))
            skill = clean_text(step.get("skill"))
            if not step_id or step_id in step_ids:
                fail(f"{rel(named_path)} workflow {workflow_id} has duplicate/missing step id")
            step_ids.add(step_id)
            if skill_dir_by_name(skill) is None:
                fail(f"{rel(named_path)} workflow {workflow_id} references unknown skill {skill}")
            assigned_skills.add(skill)
            if step.get("mode") not in allowed_modes:
                fail(f"{rel(named_path)} workflow {workflow_id} step {step_id} has invalid mode")
            for field in ["consumes", "produces"]:
                if not isinstance(step.get(field), list) or not step[field]:
                    fail(f"{rel(named_path)} workflow {workflow_id} step {step_id} needs {field}")
            if not clean_text(step.get("on_failure")):
                fail(f"{rel(named_path)} workflow {workflow_id} step {step_id} needs on_failure")
        hooks = row.get("hooks")
        if not isinstance(hooks, list) or {hook.get("event") for hook in hooks if isinstance(hook, dict)} != hook_events:
            fail(f"{rel(named_path)} workflow {workflow_id} must bind each shared hook event exactly once")
        for hook in hooks:
            for field in ["hook_id", "phase", "condition", "decision"]:
                if not clean_text(hook.get(field)):
                    fail(f"{rel(named_path)} workflow {workflow_id} hook needs {field}")
            if not isinstance(hook.get("required_inputs"), list):
                fail(f"{rel(named_path)} workflow {workflow_id} hook needs required_inputs")
        gate = row.get("exit_gate")
        if not isinstance(gate, dict):
            fail(f"{rel(named_path)} workflow {workflow_id} needs exit_gate")
        repo_path(clean_text(gate.get("validator")), must_exist=True)
        if not clean_text(gate.get("consumes")) or not isinstance(gate.get("allowed"), list) or not gate["allowed"]:
            fail(f"{rel(named_path)} workflow {workflow_id} has invalid exit gate")
        if not isinstance(gate.get("required_artifacts"), list) or not gate["required_artifacts"]:
            fail(f"{rel(named_path)} workflow {workflow_id} exit gate needs required artifacts")
        if gate.get("open_obligations_policy") not in {"forbid", "allow_declared", "archive_only"}:
            fail(f"{rel(named_path)} workflow {workflow_id} exit gate needs obligation policy")
        profiles = row.get("profiles", [])
        if not isinstance(profiles, list):
            fail(f"{rel(named_path)} workflow {workflow_id} profiles must be a list")
        for profile in profiles:
            profile_id = clean_text(profile.get("id"))
            if not profile_id or profile_id in profile_ids:
                fail(f"{rel(named_path)} duplicate/missing profile id {profile_id}")
            profile_ids.add(profile_id)
            profile_steps = profile.get("steps", [])
            if not isinstance(profile_steps, list) or not profile_steps:
                fail(f"{rel(named_path)} profile {profile_id} needs ordered steps")
            profile_orders = [step.get("order") for step in profile_steps if isinstance(step, dict)]
            if (
                len(profile_orders) != len(profile_steps)
                or profile_orders != sorted(profile_orders)
                or len(profile_orders) != len(set(profile_orders))
            ):
                fail(f"{rel(named_path)} profile {profile_id} step order must be unique and ascending")
            profile_step_ids = {clean_text(step.get("id")) for step in profile_steps if isinstance(step, dict)}
            for step in profile_steps:
                skill = clean_text(step.get("skill"))
                if skill_dir_by_name(skill) is None or step.get("mode") not in allowed_modes:
                    fail(f"{rel(named_path)} profile {profile_id} has invalid skill step {skill}")
                assigned_skills.add(skill)
            specialist_after = clean_text(profile.get("specialist_after"))
            if specialist_after not in profile_step_ids:
                fail(f"{rel(named_path)} profile {profile_id} has invalid specialist_after")
            tail_start = clean_text(profile.get("validation_tail_start"))
            base_tail_step = next((step for step in steps if clean_text(step.get("id")) == tail_start), None)
            if base_tail_step is None:
                fail(f"{rel(named_path)} profile {profile_id} has invalid validation_tail_start")
            tail_adapter = profile.get("validation_tail_adapter")
            if not isinstance(tail_adapter, dict):
                fail(f"{rel(named_path)} profile {profile_id} needs validation_tail_adapter")
            if clean_text(tail_adapter.get("from")) != clean_text(profile.get("specialist_output")):
                fail(f"{rel(named_path)} profile {profile_id} tail adapter must consume specialist_output")
            if clean_text(tail_adapter.get("to")) not in {
                clean_text(value) for value in base_tail_step.get("consumes", [])
            }:
                fail(f"{rel(named_path)} profile {profile_id} tail adapter does not feed validation tail")
            for skill in profile.get("specialist_skills", []):
                if skill_dir_by_name(clean_text(skill)) is None:
                    fail(f"{rel(named_path)} profile {profile_id} has unknown specialist {skill}")
                assigned_skills.add(clean_text(skill))
    if profile_ids != {"route_a"}:
        fail(f"{rel(named_path)} must declare exactly the Route-A profile")
    named_by_id = {row["id"]: row for row in rows}
    for row in rows:
        produced_types = {
            clean_text(value)
            for step in row.get("steps", [])
            for value in step.get("produces", [])
        }
        for handoff in row.get("handoffs", []):
            if handoff.get("workflow") not in all_ids:
                fail(f"{rel(named_path)} unknown handoff workflow {handoff.get('workflow')}")
            if not clean_text(handoff.get("when")) or not clean_text(handoff.get("artifact_type")):
                fail(f"{rel(named_path)} workflow {row['id']} has invalid typed handoff")
            destination = named_by_id.get(handoff.get("workflow"))
            destination_type = (
                clean_text(destination.get("input_artifact", {}).get("type")) if destination else ""
            )
            direct = handoff.get("artifact_type") in produced_types and destination_type == handoff.get("artifact_type")
            if not direct and not clean_text(handoff.get("adapter")):
                fail(f"{rel(named_path)} workflow {row['id']} non-direct handoff needs an adapter")
    return named_ids, assigned_skills


def _validate_dispositions(payload: dict, legacy_owners: set[str], named_skills: set[str]) -> int:
    disposition_path = repo_path(clean_text(payload.get("skill_dispositions")), must_exist=True)
    dispositions = load_json_object(disposition_path)
    skill_registry_path = repo_path(clean_text(dispositions.get("source_skill_registry")), must_exist=True)
    skill_registry = load_json_object(skill_registry_path)
    registered = {clean_text(row.get("name")) for row in skill_registry.get("skills", []) if isinstance(row, dict)}
    if not registered or "" in registered:
        fail(f"{rel(skill_registry_path)} must contain unique non-empty named skills")
    policy = dispositions.get("resolution_policy")
    if not isinstance(policy, dict) or not isinstance(policy.get("precedence"), list):
        fail(f"{rel(disposition_path)} needs an ordered resolution policy")
    expected_rules = {
        "named_workflow_step",
        "named_profile_step",
        "named_profile_specialist",
        "legacy_workflow_owner",
        "dispatch_required",
        "dispatch_conditional",
        "dispatch_advisory",
        "task_workflow_member",
        "standalone_default",
    }
    if set(policy["precedence"]) != expected_rules or len(policy["precedence"]) != len(expected_rules):
        fail(f"{rel(disposition_path)} disposition precedence must conserve each resolution rule exactly once")
    allowed = set(dispositions.get("allowed_dispositions", []))
    if allowed != {"required", "conditional", "advisory", "validator_only", "standalone", "quarantined"}:
        fail(f"{rel(disposition_path)} has invalid disposition vocabulary")
    for rule_name in expected_rules:
        rule = policy.get(rule_name)
        if not isinstance(rule, dict) or not clean_text(rule.get("rationale")):
            fail(f"{rel(disposition_path)} rule {rule_name} needs an explicit rationale")
    resolved = {skill: "standalone" for skill in registered}
    for skill in legacy_owners:
        resolved[skill] = "required"
    for skill in named_skills:
        resolved[skill] = "workflow_declared"
    if set(resolved) != registered or len(resolved) != len(registered):
        fail(
            f"{rel(disposition_path)} does not resolve all "
            f"{len(registered)} registered skills exactly once"
        )
    executable = dispositions.get("executable_policy")
    if not isinstance(executable, dict) or executable.get("default") is not False or not clean_text(executable.get("criterion")):
        fail(f"{rel(disposition_path)} must keep declaration distinct from executable status")
    return len(registered)


def main() -> int:
    payload = load_json_object(CONTRACTS)
    rows = payload.get("workflows")
    if not isinstance(rows, list) or not rows:
        fail(f"{rel(CONTRACTS)} needs non-empty workflows")
    seen: set[str] = set()
    legacy_owners: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            fail(f"{rel(CONTRACTS)} workflows entries must be objects")
        workflow_id = clean_text(row.get("id"))
        if not workflow_id or workflow_id in seen:
            fail(f"{rel(CONTRACTS)} missing or duplicate workflow id: {workflow_id}")
        seen.add(workflow_id)
        owner = clean_text(row.get("owner_skill"))
        if not owner or skill_dir_by_name(owner) is None:
            fail(f"{rel(CONTRACTS)} workflow {workflow_id} owner skill missing: {owner}")
        legacy_owners.add(owner)
        for field in ["required_artifacts", "reasoning_log_events", "validators", "handoff_to"]:
            values = row.get(field)
            if not isinstance(values, list) or not values:
                fail(f"{rel(CONTRACTS)} workflow {workflow_id} needs non-empty {field}")
        for raw in row["required_artifacts"]:
            repo_path(str(raw), must_exist=True)
        for raw in row["validators"]:
            repo_path(str(raw), must_exist=True)
        if "skill_application_start" not in row["reasoning_log_events"] or "skill_application_complete" not in row["reasoning_log_events"]:
            fail(f"{rel(CONTRACTS)} workflow {workflow_id} lacks required lifecycle events")
    unknown_handoffs = sorted({handoff for row in rows for handoff in row["handoff_to"] if handoff not in seen})
    if unknown_handoffs:
        fail(f"{rel(CONTRACTS)} unknown handoff workflow IDs: {', '.join(unknown_handoffs)}")
    named_ids, named_skills = _validate_named_workflows(payload, seen)
    registered_count = _validate_dispositions(payload, legacy_owners, named_skills)
    print(
        f"validated {len(rows)} legacy and {len(named_ids)} named workflow contracts; "
        f"resolved {registered_count} skill dispositions"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
