# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[2]


def _load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_named_workflows_are_complete_typed_and_opt_in() -> None:
    payload = _load("agentic/registries/named_workflow_contracts.yaml")
    schema = _load("agentic/spec/named_workflow_contract.schema.json")
    artifact_schema = _load("agentic/spec/named_workflow_artifacts.schema.json")
    schema["properties"]["input_artifact"] = artifact_schema["$defs"]["artifactReference"]
    rows = payload["workflows"]
    for row in rows:
        jsonschema.Draft202012Validator(schema).validate(row)
    assert {row["id"] for row in rows} == {
        "evidence_to_proof_route_onramp",
        "conceptual_frontier_deepening",
        "theorem_proof_delivery",
        "scientific_contribution_cultivation",
        "manuscript_result_elaboration",
        "deep_review_and_reorientation",
    }
    assert all(row["activation"] != "default" for row in rows)
    assert all(row["steps"] and row["trigger"] and row["exit_gate"] for row in rows)
    assert all({hook["event"] for hook in row["hooks"]} == {"UserPromptSubmit", "PreSkillUse", "PostSkillUse", "PreToolUse", "Stop"} for row in rows)


def test_three_genuine_orphans_have_normative_positions() -> None:
    rows = _load("agentic/registries/named_workflow_contracts.yaml")["workflows"]
    positions = {step["skill"]: (row["id"], step["order"], step["mode"]) for row in rows for step in row["steps"]}
    assert positions["theorem-body-normalizer"] == ("evidence_to_proof_route_onramp", 30, "required")
    assert positions["hub-bias-auditor"] == ("evidence_to_proof_route_onramp", 70, "required")
    assert positions["regime-shift-auditor"] == ("evidence_to_proof_route_onramp", 100, "conditional")


def test_all_original_task_dispatch_gap_skills_are_declared() -> None:
    rows = _load("agentic/registries/named_workflow_contracts.yaml")["workflows"]
    declared = {step["skill"] for row in rows for step in row["steps"]}
    assert "conceptual-frontier-deepening" in declared
    assert "target-literature-evolution-narrator" in declared


def test_route_a_is_a_profile_with_common_specialist_output() -> None:
    manuscript = next(row for row in _load("agentic/registries/named_workflow_contracts.yaml")["workflows"] if row["id"] == "manuscript_result_elaboration")
    assert len(manuscript["profiles"]) == 1
    route_a = manuscript["profiles"][0]
    assert route_a["id"] == "route_a"
    assert route_a["specialist_output"] == "ResultCandidatePacket"
    assert route_a["specialist_after"] == "routea_open_points"
    assert route_a["validation_tail_start"] == "certify_scope"
    assert route_a["validation_tail_adapter"] == {
        "from": "ResultCandidatePacket",
        "to": "RefinedResultCandidates",
    }


def test_legacy_contracts_are_preserved_and_validator_passes() -> None:
    root = _load("agentic/registries/workflow_contracts.yaml")
    assert [row["id"] for row in root["workflows"]] == [
        "target_navigation_loop",
        "discovery_marathon_loop",
        "abducer_work_loop",
        "conceptual_hypothesis_exploration_loop",
        "release_promotion_loop",
    ]
    result = subprocess.run(
        [sys.executable, "agentic/scripts/validate_workflow_contracts.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    skill_count = len(_load("agentic/registries/skill_registry.yaml")["skills"])
    assert f"resolved {skill_count} skill dispositions" in result.stdout
