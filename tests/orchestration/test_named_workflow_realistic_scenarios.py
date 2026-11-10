# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Realistic control-plane integration scenarios for every named workflow.

These tests explicitly import the optional workflow-local policies, not the
registered native hooks. They execute the real registry implementations and do not
pretend to run the scientific skills themselves; fixture envelopes stand in for
their outputs so ordering, activation, artifact binding, exit gates, and typed
handoffs can be tested deterministically.
"""

from __future__ import annotations

import importlib
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

import jsonschema
import pytest


ROOT = Path(__file__).resolve().parents[2]

hook_utils = importlib.import_module("hooks.workflow_local.hook_utils")
post_skill = importlib.import_module("hooks.workflow_local.post_skill_use_review")
pre_skill = importlib.import_module("hooks.workflow_local.pre_skill_use_policy")
pre_tool = importlib.import_module("hooks.workflow_local.pre_tool_use_policy")
prompt_hook = importlib.import_module("hooks.workflow_local.user_prompt_submit_intake")
stop_hook = importlib.import_module("hooks.workflow_local.stop_artifact_check")

REGISTRY_PATH = ROOT / "agentic" / "registries" / "named_workflow_contracts.yaml"
LEGACY_REGISTRY_PATH = ROOT / "agentic" / "registries" / "workflow_contracts.yaml"
SCENARIO_PATH = ROOT / "tests" / "fixtures" / "named_workflow_scenarios.json"
ARTIFACT_SCHEMA_PATH = ROOT / "agentic" / "spec" / "named_workflow_artifacts.schema.json"

REGISTRY = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
CONTRACTS = {row["id"]: row for row in REGISTRY["workflows"]}
SCENARIOS = json.loads(SCENARIO_PATH.read_text(encoding="utf-8"))["scenarios"]
ARTIFACT_SCHEMA = json.loads(ARTIFACT_SCHEMA_PATH.read_text(encoding="utf-8"))


def _run_hook(module: object, payload: dict) -> dict:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        original_stdin = sys.stdin
        sys.stdin = io.StringIO(json.dumps(payload))
        try:
            assert module.main() == 0
        finally:
            sys.stdin = original_stdin
    return json.loads(stdout.getvalue().strip().splitlines()[-1])


def _profile(contract: dict, scenario: dict) -> dict | None:
    profile_id = scenario.get("profile_id")
    if not profile_id:
        return None
    return next(row for row in contract.get("profiles", []) if row["id"] == profile_id)


def _active_steps(contract: dict, scenario: dict) -> list[dict]:
    profile = _profile(contract, scenario)
    if profile is None:
        return list(contract["steps"])
    steps = list(profile["steps"])
    tail_id = profile["validation_tail_start"]
    tail_index = next(index for index, row in enumerate(contract["steps"]) if row["id"] == tail_id)
    steps.extend(contract["steps"][tail_index:])
    specialist = {
        "id": f"specialist:{scenario['specialist_skill']}",
        "skill": scenario["specialist_skill"],
        "mode": "profile_specialist",
        "consumes": ["RouteAOpenPointPlan"],
        "produces": [profile["specialist_output"]],
    }
    insert_after = profile["specialist_after"]
    insertion = next(index + 1 for index, row in enumerate(steps) if row["id"] == insert_after)
    steps.insert(insertion, specialist)
    return steps


def _base_context(contract: dict, scenario: dict, activation_receipt: dict) -> dict:
    context = {
        "controlled": True,
        "workflow_id": contract["id"],
        "workflow_version": contract["version"],
        "target": scenario["target"],
        "target_class": scenario["target_class"],
        "activation_receipt": activation_receipt,
    }
    profile = _profile(contract, scenario)
    if profile is not None:
        context.update(
            {
                "profile_id": profile["id"],
                "profile_version": profile["version"],
                "profile_activation_evidence": {
                    "activated": True,
                    "reason": "Explicit Route-A fixture activation",
                },
            }
        )
    return context


def _envelope(contract: dict, scenario: dict, step: dict, output_type: str) -> dict:
    return {
        "artifact_type": output_type,
        "workflow_id": contract["id"],
        "workflow_version": contract["version"],
        "target": scenario["target"],
        "epistemic_status": "validated",
        "provenance": [
            f"scenario:{scenario['id']}",
            f"step:{step['id']}",
            "fixture-evidence:reviewed-domain-case",
        ],
        "payload": {
            "claim": scenario["claim"],
            "scope": scenario["scope"],
            "evidence": scenario["evidence"],
            "falsifier": scenario["falsifier"],
            "stage": step["id"],
        },
    }


@pytest.fixture(autouse=True)
def _real_registry_without_traces(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr(hook_utils, "ROOT", tmp_path)
    monkeypatch.setattr(hook_utils, "WORKFLOW_REGISTRY", REGISTRY_PATH)
    monkeypatch.setattr(hook_utils, "NAMED_WORKFLOW_REGISTRY", REGISTRY_PATH)
    for module in (post_skill, pre_skill, pre_tool, prompt_hook, stop_hook):
        monkeypatch.setattr(module, "trace", lambda *_args: None)


@pytest.mark.parametrize("scenario", SCENARIOS, ids=[row["id"] for row in SCENARIOS])
def test_realistic_named_workflow_lifecycle(scenario: dict, tmp_path: Path) -> None:
    contract = CONTRACTS[scenario["workflow_id"]]

    recommendation = _run_hook(
        prompt_hook,
        {"prompt": scenario["claim"], "trigger_facts": scenario["trigger_facts"]},
    )
    recommendation_ids = {row["workflow_id"] for row in recommendation["workflow_recommendations"]}
    assert contract["id"] in recommendation_ids
    assert recommendation["activation_authorized"] is False

    prohibited_facts = dict(scenario["trigger_facts"])
    prohibited_facts[contract["trigger"]["none_of"][0]] = True
    prohibited = _run_hook(prompt_hook, {"prompt": scenario["claim"], "trigger_facts": prohibited_facts})
    assert contract["id"] not in {row["workflow_id"] for row in prohibited.get("workflow_recommendations", [])}

    activation = hook_utils.make_activation_receipt(
        workflow_id=contract["id"],
        workflow_version=contract["version"],
        target=scenario["target"],
        target_class=scenario["target_class"],
        trigger_facts=scenario["trigger_facts"],
        authorized_by="realistic-integration-fixture",
        evidence={"scenario": scenario["id"], "explicit_activation": True},
    )
    base = _base_context(contract, scenario, activation)
    steps = _active_steps(contract, scenario)

    first = steps[0]
    no_activation = {**base, "step_id": first["id"], "skill": first["skill"]}
    no_activation.pop("activation_receipt")
    assert _run_hook(pre_skill, no_activation)["decision"] == "block"

    premature = _run_hook(
        stop_hook,
        {
            **base,
            "completed_artifacts": [],
            "gate_status": scenario["gate_status"],
            "open_obligations": scenario["open_obligations"],
        },
    )
    assert premature["decision"] == "block"

    artifact_root = tmp_path / "scenario-artifacts" / scenario["id"]
    artifact_root.mkdir(parents=True)
    completed_steps: list[str] = []
    skipped_steps = [
        {"step_id": step["id"], "reason": "Scenario condition is false."}
        for step in steps
        if step.get("mode") == "conditional" and step["id"] not in scenario["conditional_steps"]
    ]
    receipts: list[dict] = []
    artifact_ledger = {contract["input_artifact"]["type"]}

    for step in steps:
        if step.get("mode") == "conditional" and step["id"] not in scenario["conditional_steps"]:
            continue

        missing_inputs = set(step.get("consumes", [])) - artifact_ledger
        if scenario.get("profile_id") and step["id"] == "certify_scope":
            adapter = _profile(contract, scenario)["validation_tail_adapter"]
            assert adapter["from"] in artifact_ledger
            artifact_ledger.add(adapter["to"])
            missing_inputs = set(step.get("consumes", [])) - artifact_ledger
        assert not missing_inputs, f"{scenario['id']}:{step['id']} missing {sorted(missing_inputs)}"

        context = {
            **base,
            "step_id": step["id"],
            "skill": step["skill"],
            "completed_steps": completed_steps,
            "skipped_steps": skipped_steps,
        }
        if step.get("mode") == "conditional":
            context["conditional_evidence"] = {
                "activated": True,
                "condition": step.get("when"),
                "scenario": scenario["id"],
            }
        authorization = _run_hook(pre_skill, context)
        assert authorization["decision"] == "accept", authorization

        output_type = step["produces"][0]
        relative_path = Path("scenario-artifacts") / scenario["id"] / f"{step['id']}.json"
        tool_result = _run_hook(
            pre_tool,
            {
                **context,
                "tool": "Write",
                "target_path": relative_path.as_posix(),
                "mutation_class": "create",
                "budget": {"approved": True, "max_writes": len(steps) + 2},
            },
        )
        assert tool_result["decision"] == "accept", tool_result

        envelope = _envelope(contract, scenario, step, output_type)
        jsonschema.Draft202012Validator(ARTIFACT_SCHEMA).validate(envelope)
        artifact_path = tmp_path / relative_path
        artifact_path.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
        completion = _run_hook(
            post_skill,
            {
                **context,
                "output_type": output_type,
                "epistemic_status": "validated",
                "expected_artifacts": [relative_path.as_posix()],
            },
        )
        assert completion["decision"] == "accept", completion
        receipt = completion["receipt"]
        assert hook_utils.valid_skill_receipt(receipt, workflow=contract, target=scenario["target"])
        receipts.append(receipt)
        completed_steps.append(step["id"])
        artifact_ledger.update(step["produces"])

    exit_result = _run_hook(
        stop_hook,
        {
            **base,
            "completed_artifacts": receipts,
            "gate_status": scenario["gate_status"],
            "open_obligations": scenario["open_obligations"],
        },
    )
    assert exit_result["decision"] == "accept", exit_result

    forged = [dict(receipt) for receipt in receipts]
    forged[0]["target"] = "borrowed-target"
    assert _run_hook(
        stop_hook,
        {
            **base,
            "completed_artifacts": forged,
            "gate_status": scenario["gate_status"],
            "open_obligations": scenario["open_obligations"],
        },
    )["decision"] == "block"

    handoff = scenario["handoff"]
    assert handoff in contract["handoffs"] or {
        key: value for key, value in handoff.items() if key != "adapter"
    } in contract["handoffs"]
    named_destination = CONTRACTS.get(handoff["workflow"])
    if named_destination is not None:
        compatible = named_destination["input_artifact"]["type"] == handoff["artifact_type"]
        assert compatible or handoff.get("adapter")
    else:
        legacy_ids = {
            row["id"]
            for row in json.loads(LEGACY_REGISTRY_PATH.read_text(encoding="utf-8"))["workflows"]
        }
        assert handoff["workflow"] in legacy_ids
        assert handoff.get("adapter")

    handoff_envelope = {
        "artifact_type": handoff["artifact_type"],
        "workflow_id": contract["id"],
        "workflow_version": contract["version"],
        "target": scenario["target"],
        "epistemic_status": "validated",
        "provenance": [receipts[-1]["id"], f"handoff:{handoff['when']}"],
        "payload": {
            "destination_workflow": handoff["workflow"],
            "claim": scenario["claim"],
            "scope": scenario["scope"],
            "adapter": handoff.get("adapter"),
        },
    }
    jsonschema.Draft202012Validator(ARTIFACT_SCHEMA).validate(handoff_envelope)


def test_deep_review_cannot_bypass_advisory_reviewers() -> None:
    scenario = next(row for row in SCENARIOS if row["workflow_id"] == "deep_review_and_reorientation")
    contract = CONTRACTS[scenario["workflow_id"]]
    activation = hook_utils.make_activation_receipt(
        workflow_id=contract["id"],
        workflow_version=contract["version"],
        target=scenario["target"],
        target_class=scenario["target_class"],
        trigger_facts=scenario["trigger_facts"],
        authorized_by="realistic-integration-fixture",
        evidence={"scenario": scenario["id"]},
    )
    context = _base_context(contract, scenario, activation)
    result = _run_hook(
        pre_skill,
        {
            **context,
            "step_id": "synthesize_meta_review",
            "skill": "meta",
            "completed_steps": ["formalize_framework_state"],
            "skipped_steps": [],
        },
    )
    assert result["decision"] == "block"
    assert set(result["missing"]) == {
        "review_discovery_science",
        "review_concept_logic",
        "review_epistemology",
        "review_fields",
        "review_radical_design",
    }


def test_route_a_specialist_requires_profile_planning() -> None:
    scenario = next(row for row in SCENARIOS if row.get("profile_id") == "route_a")
    contract = CONTRACTS[scenario["workflow_id"]]
    activation = hook_utils.make_activation_receipt(
        workflow_id=contract["id"],
        workflow_version=contract["version"],
        target=scenario["target"],
        target_class=scenario["target_class"],
        trigger_facts=scenario["trigger_facts"],
        authorized_by="realistic-integration-fixture",
        evidence={"scenario": scenario["id"]},
    )
    context = _base_context(contract, scenario, activation)
    specialist = scenario["specialist_skill"]
    result = _run_hook(
        pre_skill,
        {
            **context,
            "step_id": f"specialist:{specialist}",
            "skill": specialist,
            "completed_steps": [],
        },
    )
    assert result["decision"] == "block"
    assert result["missing"] == ["routea_attack", "routea_open_points"]


def test_named_pre_tool_policy_rejects_borrowed_context_and_unapproved_budget() -> None:
    scenario = SCENARIOS[0]
    contract = CONTRACTS[scenario["workflow_id"]]
    activation = hook_utils.make_activation_receipt(
        workflow_id=contract["id"],
        workflow_version=contract["version"],
        target=scenario["target"],
        target_class=scenario["target_class"],
        trigger_facts=scenario["trigger_facts"],
        authorized_by="realistic-integration-fixture",
        evidence={"scenario": scenario["id"]},
    )
    base = _base_context(contract, scenario, activation)
    valid = {
        **base,
        "step_id": "ingest",
        "tool": "Write",
        "target_path": "scenario-artifacts/intake.json",
        "mutation_class": "create",
        "budget": {"approved": True, "max_writes": 1},
    }
    assert _run_hook(pre_tool, {**valid, "workflow_version": "999.0.0"})["decision"] == "block"
    assert _run_hook(pre_tool, {**valid, "budget": {"approved": False}})["decision"] == "block"
    assert _run_hook(pre_tool, {**valid, "mutation_class": "delete"})["decision"] == "block"
