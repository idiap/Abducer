# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Execute original native operations on disposable sources and authored fixtures.

Synthetic packets here test composition and rejection boundaries. They are never
represented as scientific evidence or a live model-generated investigation.
"""

import json
from pathlib import Path
import shutil

import pytest

from integrations.chatgpt.native_hooks import NativeHookBlocked
from integrations.chatgpt.native_steps import (
    prepare_cohere_fast,
    run_cohere_fast,
    validate_hypothesis_map,
)

ROOT = Path(__file__).resolve().parents[2]
STOP_FILES = (
    "agentic/state/current_target.json",
    "agentic/state/dependency_frontier.json",
    "agentic/reports/compliance/latest.md",
    "agentic/reports/drift/latest.md",
    "agentic/todos/looper_integration_todos.yaml",
)


@pytest.fixture
def isolated(tmp_path):
    source = tmp_path / "source"
    for directory in ("hooks/scripts", "registry/tasks"):
        shutil.copytree(ROOT / directory, source / directory)
    files = [
        "hooks/hooks.json",
        "agentic/orchestration/cohere_fast_runner.py",
        "agentic/registries/domain_skill_bundles.yaml",
        "agentic/registries/cohere_fast_workflow_contracts.yaml",
        "agentic/registries/cohere_fast_subworkflows.yaml",
        "agentic/spec/cohere_fast_artifacts.schema.json",
        "agentic/scripts/validate_hypothesis_exploration.py",
        "agentic/scripts/agentic_common.py",
        "agentic/scripts/abstraction_machinery_selection.py",
        "agentic/scripts/formal_subgoal_control.py",
        "agentic/spec/hypothesis_exploration_map.schema.json",
        "agentic/spec/formal_subgoal_control.schema.json",
        "agentic/spec/conceptual_pressure_packet.schema.json",
        "agentic/spec/abducer_validation_packet.schema.json",
    ]
    for relative in files:
        destination = source / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, destination)
    workspace = tmp_path / "workspace"
    shutil.copytree(source, workspace)
    for relative in STOP_FILES:
        destination = workspace / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("controlled test artifact\n")
    return {"source_root": source, "workspace": workspace}


def prepare(isolated):
    return prepare_cohere_fast(
        **isolated, command="cohere-fast ym", target="Explicit test target"
    )


def authored_step(child, packet):
    output = {
        "artifact_type": "CohereFastStagePacket",
        "schema_version": "1.0",
        "workflow_id": "cohere_fast",
        "domain_id": packet["domain_id"],
        "run_id": packet["run_id"],
        "stage_id": child["id"],
        "input_digests": ["sha256:" + "1" * 64],
        "output_digest": "sha256:" + "2" * 64,
        "disposition": "accepted",
    }
    if child["id"] == "independent-audit":
        output["audit_status"] = "accepted"
    return {
        "state": "accepted",
        "packet": output,
        "artifacts": {
            "steps/" + child["id"] + ".txt": "Explicit authored test fixture"
        },
    }


def test_cohere_preserves_disabled_domain_and_exact_activation(isolated, monkeypatch):
    monkeypatch.delenv("ABDUCER_ENABLE_COHERE_FAST", raising=False)
    with pytest.raises(ValueError, match="disabled domain"):
        prepare(isolated)
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "true")
    with pytest.raises(ValueError, match="explicit"):
        prepare_cohere_fast(
            **isolated, command="please run cohere-fast ym", target="Test"
        )
    assert not (isolated["workspace"] / "artifacts").exists()


def test_cohere_calls_original_children_and_writes_real_receipts(isolated, monkeypatch):
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "true")
    prepared = prepare(isolated)
    seen = []

    def execute(child, packet):
        seen.append(child["id"])
        return authored_step(child, packet)

    result = run_cohere_fast(
        **isolated,
        command="cohere-fast ym",
        target="Explicit test target",
        request=prepared["request"],
        executor=execute,
    )
    assert seen == [
        "scope-and-ground",
        "adaptive-frontier",
        "derivation-and-proof",
        "independent-audit",
        "manuscript-release",
    ]
    assert result["result"]["state"] == "accepted"
    assert {receipt["event"] for receipt in result["hook_receipts"]} == {
        "UserPromptSubmit",
        "PreSkillUse",
        "PostSkillUse",
        "PreToolUse",
        "Stop",
    }
    assert all(
        receipt["result"]["decision"] == "accept" for receipt in result["hook_receipts"]
    )
    run_root = Path(result["result"]["run_root"])
    for receipt in result["result"]["steps"]:
        assert (
            json.loads(
                (run_root / "receipts" / (receipt["step_id"] + ".json")).read_text()
            )
            == receipt
        )
        assert receipt["artifact_digests"]
    assert not result["scientific_truth_verified"]
    with pytest.raises(ValueError, match="already exists"):
        run_cohere_fast(
            **isolated,
            command="cohere-fast ym",
            target="Explicit test target",
            request=prepared["request"],
            executor=execute,
        )


def test_native_retry_budget_and_quarantine_survive_adapter(isolated, monkeypatch):
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "true")
    prepared = prepare(isolated)
    seen = []

    def execute(child, packet):
        seen.append(child["id"])
        result = authored_step(child, packet)
        if child["id"] == "adaptive-frontier":
            result["state"] = "failed"
            result["packet"]["disposition"] = "rejected"
        return result

    result = run_cohere_fast(
        **isolated,
        command="cohere-fast ym",
        target="Explicit test target",
        request=prepared["request"],
        executor=execute,
    )
    assert seen == [
        "scope-and-ground",
        "adaptive-frontier",
        "adaptive-frontier",
        "adaptive-frontier",
    ]
    assert result["result"]["state"] == "quarantined"
    assert result["result"]["steps"][-1]["attempt"] == 3


def test_manuscript_requires_accepted_independent_audit(isolated, monkeypatch):
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "true")
    prepared = prepare(isolated)
    seen = []

    def execute(child, packet):
        seen.append(child["id"])
        result = authored_step(child, packet)
        result["packet"].pop("audit_status", None)
        return result

    with pytest.raises(ValueError, match="independent-audit"):
        run_cohere_fast(
            **isolated,
            command="cohere-fast ym",
            target="Explicit test target",
            request=prepared["request"],
            executor=execute,
        )
    assert "manuscript-release" not in seen


@pytest.mark.parametrize("attack", ["wrong_run", "path_escape", "wrong_disposition"])
def test_authored_packet_cannot_cross_binding_or_output_boundary(
    isolated, monkeypatch, attack
):
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "true")
    prepared = prepare(isolated)

    def execute(child, packet):
        result = authored_step(child, packet)
        if attack == "wrong_run":
            result["packet"]["run_id"] = "cf-" + "f" * 24
        elif attack == "path_escape":
            result["artifacts"] = {"../../escape.txt": "must never write"}
        else:
            result["packet"]["disposition"] = "rejected"
        return result

    with pytest.raises(ValueError):
        run_cohere_fast(
            **isolated,
            command="cohere-fast ym",
            target="Explicit test target",
            request=prepared["request"],
            executor=execute,
        )
    assert not list((isolated["workspace"] / "artifacts").rglob("*.txt"))


def test_native_stop_block_is_not_reported_as_success(isolated, monkeypatch):
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "true")
    prepared = prepare(isolated)
    (isolated["workspace"] / STOP_FILES[-1]).unlink()
    with pytest.raises(NativeHookBlocked, match="Stop"):
        run_cohere_fast(
            **isolated,
            command="cohere-fast ym",
            target="Explicit test target",
            request=prepared["request"],
            executor=authored_step,
        )
    trace = json.loads(
        (
            isolated["workspace"]
            / "agentic/traces/hook_runs/latest-stop_artifact_check.json"
        ).read_text()
    )
    assert trace["result"]["decision"] == "block"


def test_conceptual_validator_executes_original_rejection(isolated):
    destination = isolated["workspace"] / "artifacts/research/map.json"
    destination.parent.mkdir(parents=True)
    destination.write_text('{"target_id":"fixture"}')
    result = validate_hypothesis_map(**isolated, map_path="artifacts/research/map.json")
    assert result["status"] == "failed" and result["exit_code"] != 0
    assert "missing required field" in result["stderr"]
    assert result["hook_receipt"]["event"] == "PreToolUse"
    assert not result["native_workflow_executed"]


def test_conceptual_validator_preserves_valid_native_fixture(isolated):
    payload = json.loads(
        (
            ROOT / "agentic/fixtures/hegelian/hypothesis_exploration_map.example.json"
        ).read_text()
    )
    workspace = isolated["workspace"]
    for key in ("kb_path", "source_graph"):
        destination = workspace / payload[key]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("fixture input exists\n")
    destination = workspace / "artifacts/research/map.json"
    destination.parent.mkdir(parents=True)
    destination.write_text(json.dumps(payload))
    result = validate_hypothesis_map(**isolated, map_path="artifacts/research/map.json")
    assert result["status"] == "passed", result["stderr"]
    assert "validated hypothesis exploration map" in result["stdout"]
    assert not result["scientific_truth_verified"]


def test_native_operation_rejects_modified_code_and_symlink_inputs(isolated):
    path = isolated["workspace"] / "agentic/scripts/validate_hypothesis_exploration.py"
    original = path.read_bytes()
    path.write_text("raise RuntimeError('modified validator')")
    with pytest.raises(ValueError, match="source drift"):
        validate_hypothesis_map(**isolated, map_path="map.json")
    path.write_bytes(original)
    (isolated["workspace"] / "map.json").symlink_to(
        isolated["source_root"] / "hooks/hooks.json"
    )
    with pytest.raises(ValueError, match="symlink"):
        validate_hypothesis_map(**isolated, map_path="map.json")
