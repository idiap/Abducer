# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Exercise real native policies through the hosted dispatcher in disposable trees.

Expected decisions below are native behavior, not assertions computed from the
adapter. No research tree, model provider or network service is used.
"""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from types import ModuleType
from types import SimpleNamespace

import pytest

from integrations.chatgpt import native_hooks
from integrations.chatgpt.native_hooks import (
    NativeHookBlocked,
    NativeHookDispatcher,
    NativeHookError,
)
from integrations.chatgpt.hooked_marathon import MODULE_SOURCES, OWNER_SKILL, run_hooked

ROOT = Path(__file__).resolve().parents[2]
STOP_ARTIFACTS = (
    "agentic/state/current_target.json",
    "agentic/state/dependency_frontier.json",
    "agentic/reports/compliance/latest.md",
    "agentic/reports/drift/latest.md",
    "agentic/todos/looper_integration_todos.yaml",
)


@pytest.fixture
def trees(tmp_path):
    source = tmp_path / "source"
    (source / "hooks/scripts").mkdir(parents=True)
    for file in (ROOT / "hooks/scripts").glob("*.py"):
        shutil.copyfile(file, source / "hooks/scripts" / file.name)
    shutil.copyfile(ROOT / "hooks/hooks.json", source / "hooks/hooks.json")
    registry = source / "registry/tasks/example/task_registry.json"
    registry.parent.mkdir(parents=True)
    registry.write_text(
        json.dumps(
            {
                "visible_workflows": [
                    {"composed_skills": ["baseline-skill", OWNER_SKILL]}
                ]
            }
        )
    )
    workspace = tmp_path / "workspace"
    shutil.copytree(source, workspace)
    return source, workspace


@pytest.mark.parametrize(
    "event,payload,decision",
    [
        ("UserPromptSubmit", {"prompt": "keep working"}, "warn"),
        (
            "UserPromptSubmit",
            {
                "prompt": "hello",
                "trigger_facts": {"external_mathematical_source": True},
            },
            "accept",
        ),
        ("PreSkillUse", {"skill": "baseline-skill"}, "accept"),
        ("PreSkillUse", {"skill": "unknown"}, "block"),
        ("PreSkillUse", {"skill": "unknown", "controlled": False}, "accept"),
        (
            "PreSkillUse",
            {"skill": "baseline-skill", "workflow_id": "other", "completed_steps": []},
            "accept",
        ),
        ("PreToolUse", {"command": "rm -rf /tmp/example"}, "block"),
        ("PreToolUse", {"path": "registry/example.json"}, "warn"),
        (
            "PreToolUse",
            {"path": "registry/example.json", "evidence": "TODO-1"},
            "accept",
        ),
        ("PreToolUse", {"path": "docs/integrations/looper-control-plane.md"}, "warn"),
        ("PostSkillUse", {"expected_artifacts": ["missing.json"]}, "warn"),
        ("PostSkillUse", {"expected_artifacts": []}, "accept"),
        ("Stop", {"controlled": False}, "accept"),
        ("Stop", {"controlled": True}, "block"),
    ],
)
def test_original_decisions_and_traces_are_preserved(trees, event, payload, decision):
    source, workspace = trees
    dispatcher = NativeHookDispatcher(source_root=source, workspace=workspace)
    receipt = dispatcher.dispatch(event, payload)
    assert receipt.result["decision"] == decision
    assert receipt.allowed is (decision != "block")
    trace = workspace / receipt.native_trace
    assert json.loads(trace.read_text()) == {
        "hook": Path(receipt.script).stem,
        "payload": payload,
        "result": receipt.result,
    }
    assert hashlib.sha256(trace.read_bytes()).hexdigest() == receipt.native_trace_sha256
    assert (
        json.loads((workspace / native_hooks.JOURNAL).read_text())["result"]
        == receipt.result
    )
    assert not (source / "agentic/traces").exists()
    assert not (workspace / "agentic/traces/public_reasoning").exists()


def test_require_raises_on_json_block_despite_successful_exit_and_keeps_warn(trees):
    source, workspace = trees
    hooks = NativeHookDispatcher(source_root=source, workspace=workspace)
    with pytest.raises(NativeHookBlocked) as blocked:
        hooks.require("PreSkillUse", {"skill": "unknown"})
    assert blocked.value.receipt.result["decision"] == "block"
    assert hooks.require("PostSkillUse", {"expected_artifacts": ["absent"]}).allowed
    assert len((workspace / native_hooks.JOURNAL).read_text().splitlines()) == 2


def test_stop_uses_original_five_artifacts_and_latest_trace_behavior(trees):
    source, workspace = trees
    hooks = NativeHookDispatcher(source_root=source, workspace=workspace)
    for relative in STOP_ARTIFACTS:
        path = workspace / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture")
    accepted = hooks.require("Stop", {"controlled": True})
    assert accepted.result == {
        "decision": "accept",
        "reason": "Required stop-time artifacts are present.",
    }
    (workspace / STOP_ARTIFACTS[-1]).unlink()
    with pytest.raises(NativeHookBlocked) as error:
        hooks.require("Stop", {"controlled": True})
    assert error.value.receipt.result["missing"] == [STOP_ARTIFACTS[-1]]
    assert (
        json.loads((workspace / accepted.native_trace).read_text())["result"]
        == error.value.receipt.result
    )
    assert len((workspace / native_hooks.JOURNAL).read_text().splitlines()) == 2


@pytest.mark.parametrize(
    "relative",
    [
        "hooks/scripts/hook_utils.py",
        "hooks/scripts/pre_skill_use_policy.py",
        "registry/tasks/example/task_registry.json",
        "registry/tasks/added/task_registry.json",
    ],
)
def test_source_or_membership_drift_rejects_before_policy_execution(trees, relative):
    source, workspace = trees
    hooks = NativeHookDispatcher(source_root=source, workspace=workspace)
    changed = workspace / relative
    changed.parent.mkdir(parents=True, exist_ok=True)
    changed.write_text("{}")
    with pytest.raises(NativeHookError, match="drifted"):
        hooks.dispatch("PreSkillUse", {"skill": "unknown"})
    assert not (workspace / "agentic/traces/hook_runs").exists()


def test_source_root_cannot_be_used_as_writable_workspace(trees):
    source, _ = trees
    with pytest.raises(NativeHookError, match="separate"):
        NativeHookDispatcher(source_root=source, workspace=source)


def test_optional_workflow_local_configuration_is_not_accepted(trees):
    source, workspace = trees
    config = json.loads((source / "hooks/hooks.json").read_text())
    config["hooks"][0]["script"] = "hooks/workflow_local/user_prompt_submit_intake.py"
    for root in (source, workspace):
        (root / "hooks/hooks.json").write_text(json.dumps(config))
    with pytest.raises(NativeHookError, match="supported event contract"):
        NativeHookDispatcher(source_root=source, workspace=workspace)


@pytest.mark.parametrize(
    "payload",
    [
        {"expected_artifacts": ["../outside"]},
        {"expected_artifacts": ["/tmp/outside"]},
        {"expected_artifacts": "not-a-list"},
        {"path": "hooks/../outside"},
    ],
)
def test_path_inputs_are_confined_before_native_reads(trees, payload):
    source, workspace = trees
    hooks = NativeHookDispatcher(source_root=source, workspace=workspace)
    with pytest.raises(NativeHookError):
        hooks.dispatch("PostSkillUse", payload)
    assert not (workspace / "agentic/traces").exists()


@pytest.mark.parametrize(
    "relative",
    ["hooks/scripts/hook_utils.py", "agentic/traces", "registry/tasks/example"],
)
def test_symlink_escapes_are_rejected(trees, tmp_path, relative):
    source, workspace = trees
    hooks = NativeHookDispatcher(source_root=source, workspace=workspace)
    path = workspace / relative
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()
    path.parent.mkdir(parents=True, exist_ok=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    path.symlink_to(outside)
    with pytest.raises(NativeHookError, match="symlink"):
        hooks.dispatch("PreSkillUse", {"skill": "baseline-skill"})
    assert list(outside.iterdir()) == []


def test_hardlinked_trace_cannot_write_outside_the_workspace(trees, tmp_path):
    source, workspace = trees
    hooks = NativeHookDispatcher(source_root=source, workspace=workspace)
    outside = tmp_path / "outside"
    outside.write_text("untouched")
    trace = workspace / "agentic/traces/hook_runs/latest-pre_skill_use_policy.json"
    trace.parent.mkdir(parents=True)
    trace.hardlink_to(outside)
    with pytest.raises(NativeHookError, match="unlinked regular"):
        hooks.dispatch("PreSkillUse", {"skill": "baseline-skill"})
    assert outside.read_text() == "untouched"


@pytest.mark.parametrize(
    "output",
    [b"not-json", b'{"decision":"allow","reason":"bad"}', b'{"decision":"accept"}'],
)
def test_invalid_subprocess_outputs_fail_closed(trees, monkeypatch, output):
    source, workspace = trees
    hooks = NativeHookDispatcher(source_root=source, workspace=workspace)
    monkeypatch.setattr(
        native_hooks.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=0, stdout=output),
    )
    with pytest.raises(NativeHookError):
        hooks.require("PreSkillUse", {"skill": "baseline-skill"})


def test_timeout_is_not_an_accept_decision(trees, monkeypatch):
    source, workspace = trees
    hooks = NativeHookDispatcher(source_root=source, workspace=workspace)

    def timed_out(*args, **kwargs):
        raise subprocess.TimeoutExpired("hook", 10)

    monkeypatch.setattr(native_hooks.subprocess, "run", timed_out)
    with pytest.raises(NativeHookError, match="timed out"):
        hooks.require("PreSkillUse", {"skill": "baseline-skill"})


def test_optional_task_registry_cannot_expand_native_membership(trees):
    source, workspace = trees
    extra = workspace / "registry/optional-tasks/test/task_registry.json"
    extra.parent.mkdir(parents=True)
    extra.write_text(
        json.dumps({"visible_workflows": [{"composed_skills": ["optional-skill"]}]})
    )
    hooks = NativeHookDispatcher(source_root=source, workspace=workspace)
    with pytest.raises(NativeHookBlocked):
        hooks.require("PreSkillUse", {"skill": "optional-skill"})


@pytest.fixture
def marathon_fixture(trees, tmp_path, monkeypatch):
    """A source-bound adapter fixture tests real hooks without simulating science."""
    source, _ = trees
    code = """import subprocess
class DiscoveryOperatorDispatcher:
    def __init__(self, workspace): self.workspace = workspace
    def _invoke_operator(self, binding, request): return binding.function(request)
    def _run_validator(self, binding, request, *args, **kwargs): return binding.function(request)
"""
    for name, relative in MODULE_SOURCES.items():
        path = source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(code)
        monkeypatch.delitem(sys.modules, name, raising=False)
    output = tmp_path / "run"
    output.mkdir()
    state = {
        "run_root": str(output),
        "binding": {"target_id": "fixture-target", "run_id": "fixture-run"},
    }
    calls = []
    service = SimpleNamespace(
        model=SimpleNamespace(model_id="fixture-no-model"),
        event=lambda *args: calls.append(("event", args)),
        completion=lambda *a, **k: calls.append(("completion", k)) or {"fixture": True},
        public_fetch=lambda *a, **k: calls.append(("fetch", a)) or b"fixture",
    )
    options = {"stop_artifacts": True, "command": [sys.executable, "-c", "pass"]}
    modules = {}

    def execute(*, state, services):
        workspace = output / "workspace"
        shutil.copytree(source, workspace)
        services.event("stage", {"stage_id": "workspace", "status": "completed"})
        for name, relative in MODULE_SOURCES.items():
            module = ModuleType(name)
            module.__file__ = str(workspace / relative)
            exec(compile(code, module.__file__, "exec"), module.__dict__)
            monkeypatch.setitem(sys.modules, name, module)
            modules[name] = module
        services.event("stage", {"stage_id": "marathon", "status": "running"})
        services.completion(messages=[{"role": "user", "content": "unchanged fixture"}])
        services.public_fetch("https://example.test/fixture")
        dispatcher = modules["agentic.discovery.receipts"].DiscoveryOperatorDispatcher(
            workspace
        )
        binding = SimpleNamespace(
            operator_id="internal-operator-not-a-native-skill",
            function=lambda request: calls.append(("operator", request))
            or {"value": 1},
        )
        assert dispatcher._invoke_operator(
            binding, {"declared_outputs": ["result.json"]}
        ) == {"value": 1}
        validator = SimpleNamespace(
            validator_id="fixture-validator", function=lambda request: True
        )
        assert dispatcher._run_validator(validator, {}) is True
        modules["run_discovery_marathon"].subprocess.run(options["command"], check=True)
        if options["stop_artifacts"]:
            for relative in STOP_ARTIFACTS:
                path = workspace / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture")
        # Missing expected research reports intentionally exercise native warn;
        # this fixture does not invoke the separate native report verifier.
        return {
            "workspace": str(workspace),
            "cycle_count": 1,
            "unchanged": {"value": 7},
        }

    return SimpleNamespace(
        source=source,
        state=state,
        services=service,
        adapter=SimpleNamespace(execute=execute),
        calls=calls,
        options=options,
        modules=modules,
    )


def test_marathon_owner_and_effect_hooks_preserve_native_return_values(
    marathon_fixture,
):
    fixture = marathon_fixture
    result = run_hooked(
        fixture.adapter,
        state=fixture.state,
        services=fixture.services,
        source_root=fixture.source,
        prompt="keep working",
    )
    assert result["unchanged"] == {"value": 7}
    coverage = result["native_hook_coverage"]
    assert coverage["events"] == sorted(native_hooks.EVENT_SCRIPTS)
    assert coverage["warnings"] == 2  # intake and missing fixture reports
    assert coverage["tool_boundaries_observed"] == [
        "host_model_completion",
        "host_public_fetch",
        "native_operator",
        "native_subprocess",
        "native_validator",
    ]
    assert coverage["internal_operators_are_separate_skill_invocations"] is False
    journal = Path(result["workspace"]) / coverage["journal"]
    receipts = [json.loads(line) for line in journal.read_text().splitlines()]
    assert [row["event"] for row in receipts].count("PreSkillUse") == 1
    assert any(row[0] == "operator" for row in fixture.calls)
    assert fixture.modules["run_discovery_marathon"].subprocess is subprocess
    assert not hasattr(
        fixture.modules[
            "agentic.discovery.receipts"
        ].DiscoveryOperatorDispatcher._invoke_operator,
        "__wrapped__",
    )


def test_marathon_blocked_owner_prevents_every_model_and_operator_effect(
    marathon_fixture,
):
    fixture = marathon_fixture
    registry = fixture.source / "registry/tasks/example/task_registry.json"
    registry.write_text(json.dumps({"visible_workflows": []}))
    with pytest.raises(NativeHookBlocked, match="not declared"):
        run_hooked(
            fixture.adapter,
            state=fixture.state,
            services=fixture.services,
            source_root=fixture.source,
        )
    assert fixture.calls == []


def test_marathon_missing_native_stop_artifacts_blocks_completion(marathon_fixture):
    fixture = marathon_fixture
    fixture.options["stop_artifacts"] = False
    with pytest.raises(
        NativeHookBlocked, match="Missing controlled-iteration stop artifacts"
    ):
        run_hooked(
            fixture.adapter,
            state=fixture.state,
            services=fixture.services,
            source_root=fixture.source,
        )
    assert fixture.modules["run_discovery_marathon"].subprocess is subprocess


def test_marathon_destructive_subprocess_is_blocked_before_launch(
    marathon_fixture, tmp_path
):
    fixture = marathon_fixture
    victim = tmp_path / "victim"
    victim.mkdir()
    fixture.options["command"] = ["rm", "-rf", str(victim)]
    with pytest.raises(NativeHookBlocked, match="Destructive"):
        run_hooked(
            fixture.adapter,
            state=fixture.state,
            services=fixture.services,
            source_root=fixture.source,
        )
    assert victim.exists()
    assert fixture.modules["run_discovery_marathon"].subprocess is subprocess


def test_marathon_without_native_workspace_callback_cannot_succeed(marathon_fixture):
    fixture = marathon_fixture
    fixture.adapter.execute = lambda **kwargs: {
        "workspace": str(Path(fixture.state["run_root"]) / "workspace")
    }
    with pytest.raises(NativeHookError, match="activated workspace"):
        run_hooked(
            fixture.adapter,
            state=fixture.state,
            services=fixture.services,
            source_root=fixture.source,
        )
