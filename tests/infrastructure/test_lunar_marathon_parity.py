# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Transport, source dispatch and report fidelity; not scientific acceptance.

Boundary fakes exercise host plumbing. The real research gate and branch
validator are exercised separately and are never replaced in exported code.
"""
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import sys

import pytest

from integrations.domain_package import marathon_runtime as adapter
from integrations.domain_package.runtime_registration import registration

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))
import run_discovery_marathon as marathon


def test_registration_selects_native_runner_not_seven_effect_demo():
    contract = registration()
    assert contract["execute_hook"] == "abducer-execute"
    assert contract["input_schema"]["additionalProperties"] is False
    assert "context_summary" not in contract["input_schema"]["properties"]
    assert "html_report" in contract["output_schema"]["properties"]["structured_value"]["required"]


def test_missing_binding_is_actionable_and_never_replays_history(tmp_path):
    source = tmp_path / "repository/runtime"
    source.mkdir(parents=True)
    (source.parent / "marathon-binding.json").write_text(json.dumps({"target_id": adapter.TARGET}))
    with pytest.raises(ValueError, match="no committed canonical theory cycle"):
        adapter.read_binding(source)
    assert not (tmp_path / "full_timeline.html").exists()


def test_new_run_requires_public_channel_before_any_writes_and_gets_unique_identity(monkeypatch, tmp_path):
    source = tmp_path / "repository/runtime"
    module = source / "integrations/domain_package/marathon_runtime.py"
    module.parent.mkdir(parents=True)
    monkeypatch.setattr(adapter, "__file__", str(module))
    catalog = {"version": 2, "runs": [{"target_id": "p-vs-np-target", "run_id": "new", "initialize": True,
        "cycle_count": 0, "canonical_theory_cycle": None, "canonical_theory_state_root": None}]}
    (source.parent / "marathon-binding.json").write_text(json.dumps(catalog))
    arguments = dict(workflow_id="discovery_marathon_loop", inputs={"target_id": "p-vs-np-target", "run_id": "new"},
                     mode="live", run_id="host-run-1", run_root=tmp_path / "output", on_reasoning=lambda **k: None)
    for enabled, channel in ((False, lambda **k: None), (True, None)):
        with pytest.raises(ValueError, match="public literature reads"):
            adapter.prepare(**arguments, network_authority=enabled, public_fetch=channel)
    assert not arguments["run_root"].exists()
    first = adapter.prepare(**arguments, network_authority=True, public_fetch=lambda **k: None)
    second = adapter.prepare(**{**arguments, "run_id": "host-run-2"}, network_authority=True, public_fetch=lambda **k: None)
    identity = first["state"]["binding"]["run_id"]
    assert identity != second["state"]["binding"]["run_id"]
    assert identity.startswith("lunar-marathon-") and "." not in identity
    assert first["state"]["initial_cycle_count"] == 0


@pytest.mark.parametrize("path", ["../outside", "/absolute", "a/../b", "a\\b", "./file"])
def test_state_paths_cannot_escape(tmp_path, path):
    with pytest.raises(ValueError):
        adapter.confined(tmp_path, path)


def test_real_branch_transport_preserves_prompt_schema_and_validation(monkeypatch):
    branch = json.loads((ROOT / "tests/fixtures/discovery_marathon/yang_mills_branch_fixture.json").read_text())
    calls = []
    monkeypatch.setattr(marathon, "environment_with_api_keys", lambda *a, **k: pytest.fail("credentials read"))
    monkeypatch.setattr(marathon.urllib.request, "urlopen", lambda *a, **k: pytest.fail("direct network"))
    def provider(**kwargs):
        calls.append(kwargs)
        return {"choices": [{"message": {"content": "{}"}}]}
    with marathon.bind_host_model(provider, "owned-model"):
        with pytest.raises(marathon.BranchExecutionError):
            marathon.build_api_branch_output(branch, 1, 60)
    assert len(calls) == 2
    for call, compact in zip(calls, (False, True)):
        assert call["messages"] == [{"role": "user", "content": marathon.branch_prompt(branch, 1, 60, compact=compact)}]
        assert call["response_format"]["json_schema"]["schema"] == json.loads(marathon.CODEX_BRANCH_SCHEMA.read_text())
    assert marathon._HOST_MODEL.get() is None


def test_real_research_gate_precedes_model_and_scheduler(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(marathon, "marathon_transaction_store", lambda _: SimpleNamespace(root=tmp_path, current_generation=lambda: 0))
    monkeypatch.setattr(marathon, "load_branches", lambda _: calls.append("branches"))
    with marathon.bind_host_model(lambda **k: calls.append("model"), "owned-model"):
        with pytest.raises(SystemExit):
            marathon.run_one_cycle({"target_id": adapter.TARGET, "run_id": adapter.RUN_ID})
    assert calls == []


def test_controlled_valid_branch_passes_existing_source_validators():
    """A synthetic test response checks transport success, not live research."""
    branch = json.loads((ROOT / "tests/fixtures/discovery_marathon/yang_mills_branch_fixture.json").read_text())
    packet = marathon.attach_negative_tactic_decision(marathon.build_branch_output(branch, 1), branch)
    calls = []
    def provider(**arguments):
        calls.append(arguments)
        return {"choices": [{"message": {"content": json.dumps(packet)}}]}
    with marathon.bind_host_model(provider, "controlled-test"):
        output, record = marathon.build_api_branch_output(branch, 1, 60)
    assert record["status"] == "complete" and record["engine"] == "host_model_channel"
    assert len(calls) == 1
    assert output["branch_id"] == branch["branch_id"]


def test_host_failure_uses_source_compact_retry():
    branch = json.loads((ROOT / "tests/fixtures/discovery_marathon/yang_mills_branch_fixture.json").read_text())
    packet = marathon.attach_negative_tactic_decision(marathon.build_branch_output(branch, 1), branch)
    calls = []
    def provider(**arguments):
        calls.append(arguments)
        if len(calls) == 1:
            raise RuntimeError("Controlled transient provider failure")
        return {"choices": [{"message": {"content": json.dumps(packet)}}]}
    with marathon.bind_host_model(provider, "controlled-test"):
        _, record = marathon.build_api_branch_output(branch, 1, 60)
    assert record["api_attempt"] == "compact_retry"
    assert len(calls) == 2
    assert calls[1]["messages"][0]["content"] == marathon.branch_prompt(branch, 1, 60, compact=True)


def test_adapter_invokes_source_cli_and_rejects_failed_exit(monkeypatch, tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    output = tmp_path / "output"
    output.mkdir()
    copied = output / "workspace"
    recorded = []
    @contextmanager
    def bind(completion, model_id):
        recorded.append(model_id)
        yield
    def main():
        recorded.append(sys.argv[:])
        raise SystemExit(2)
    fake = SimpleNamespace(__file__=str(copied / "agentic/scripts/run_discovery_marathon.py"), bind_host_model=bind, main=main)
    monkeypatch.setattr(adapter.importlib, "import_module", lambda _: fake)
    services = SimpleNamespace(completion=lambda **k: None, model=SimpleNamespace(model_id="owned-model"), event=lambda *a: None)
    state = {"source": str(source), "run_root": str(output), "binding": {"target_id": adapter.TARGET, "run_id": adapter.RUN_ID,
             "canonical_theory_cycle": "cycle.json", "canonical_theory_state_root": "state"}}
    before = Path.cwd()
    with pytest.raises(ValueError, match="Source marathon stopped"):
        adapter.execute(state=state, services=services)
    argv = recorded[1]
    assert argv[argv.index("--execution-mode") + 1] == "research"
    assert argv[argv.index("--run-id") + 1] == adapter.RUN_ID
    assert "--skip-report-rebuild" not in argv and "--dry-run" not in argv
    assert Path.cwd() == before
    assert not (output / "full_timeline.html").exists()


def test_report_projection_preserves_original_html_bytes(tmp_path):
    workspace = tmp_path / "workspace"
    reports = workspace / adapter.REPORT_ROOT
    reports.mkdir(parents=True)
    historical = ROOT / adapter.REPORT_ROOT
    for name in ("latest.html", "full_timeline.html", "latest.json", "latest.md"):
        (reports / name).write_bytes((historical / name).read_bytes())
    source_report = json.loads((reports / "latest.json").read_text())
    identity = source_report["run_id"]
    result = adapter.verify(state={"run_root": str(tmp_path), "binding": {"target_id": adapter.TARGET, "run_id": identity}},
        execution={"workspace": str(workspace), "cycle_count": source_report["cycle_count"], "runner_sha256": "a" * 64}, services=None)["result"]
    original = (historical / "full_timeline.html").read_bytes()
    assert (tmp_path / "full_timeline.html").read_bytes() == original
    assert result["structured_value"]["html_report"]["sha256"] == hashlib.sha256(original).hexdigest()
    assert result["report_verification"]["scientific_truth_verified"] is False


def test_parallel_transport_is_explicitly_rejected():
    with marathon.bind_host_model(lambda **k: None, "owned-model"):
        with pytest.raises(ValueError, match="serial"):
            marathon.resolve_api_parallel_config(2, requested_workers=2, parallel_branches=True,
                api_key_config=None, requested_spacing_seconds=None)


@pytest.mark.parametrize("packet", [{"packet_id": "invalid"}, {}, None])
def test_report_rebuild_accepts_pre_packet_history_without_skipping_recorded_packets(monkeypatch, tmp_path, packet):
    """Historical absence is displayable; malformed recorded evidence still fails."""
    cycles = tmp_path / "cycles"
    cycles.mkdir()
    historical = cycles / "cycle-0001.json"
    historical.write_text(json.dumps({"branch_outputs": []}))
    modern = cycles / "cycle-0002.json"
    modern.write_text(json.dumps({"branch_outputs": [{"proof_depth_control": packet}]}))
    monkeypatch.setattr(marathon, "run_dir", lambda _: tmp_path)
    commands = marathon.report_rebuild_commands(adapter.RUN_ID, adapter.TARGET)
    command = next(row for row in commands if "agentic/scripts/validate_proof_depth_control.py" in row)
    assert str(historical) not in command
    assert str(modern) in command
    import subprocess
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode != 0


def test_catalog_selects_exact_pairs_and_schema_rejects_cross_target(tmp_path):
    from integrations.domain_package.export import marathon_catalog
    from jsonschema import Draft202012Validator, ValidationError
    for target, identity in (("target-a", "run-a"), ("target-b", "run-b")):
        path = tmp_path / f"agentic/runs/discovery_marathons/{identity}/run_state.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({"target_id": target, "run_id": identity, "cycle_count": 4}))
    catalog, directories, additions = marathon_catalog(tmp_path, None, None, "state")
    assert len(catalog["runs"]) == 4 and not additions
    historical = [run for run in catalog["runs"] if not run.get("initialize")]
    assert all(run["readiness"]["status"] == "blocked" for run in historical)
    schema = Draft202012Validator(registration(catalog["runs"])["input_schema"])
    schema.validate({"target_id": "target-b", "run_id": "run-b"})
    for inputs in ({}, {"target_id": "target-a", "run_id": "run-b"},
                   {"target_id": "target-a", "run_id": "run-a", "path": "cycle.json"}):
        with pytest.raises(ValidationError):
            schema.validate(inputs)
    source = tmp_path / "repository/runtime"
    source.mkdir(parents=True)
    (source.parent / "marathon-binding.json").write_text(json.dumps(catalog))
    with pytest.raises(ValueError, match="no committed canonical theory cycle"):
        adapter.read_binding(source, {"target_id": "target-b", "run_id": "run-b"})
    with pytest.raises(ValueError, match="not available"):
        adapter.read_binding(source, {"target_id": "target-a", "run_id": "run-b"})
    new_run = {"target_id": "p-vs-np-target", "run_id": "new"}
    schema.validate(new_run)
    assert adapter.read_binding(source, new_run)["initialize"] is True


def test_catalog_binding_keeps_source_identity_and_never_asserts_currentness(tmp_path):
    from integrations.domain_package.export import marathon_catalog
    from integrations.domain_package.exporter import ExportError
    path = tmp_path / "agentic/runs/discovery_marathons/run-a/run_state.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"target_id": "target-a", "run_id": "run-a", "cycle_count": 1}))
    cycle = tmp_path / "cycle.json"
    cycle.write_text(json.dumps({"target_id": "target-b", "run_id": "run-a"}))
    (tmp_path / "state").mkdir()
    with pytest.raises(ExportError, match="does not belong"):
        marathon_catalog(tmp_path, "run-a", "cycle.json", "state")
    cycle.write_text(json.dumps({"target_id": "target-a", "run_id": "run-a"}))
    catalog, _, _ = marathon_catalog(tmp_path, "run-a", "cycle.json", "state")
    assert catalog["runs"][0]["readiness"]["status"] == "requires_validation"
    catalog, _, _ = marathon_catalog(tmp_path, None, None, "state", {
        "run-a": {"canonical_theory_cycle": "cycle.json", "canonical_theory_state_root": "state"}})
    assert catalog["runs"][0]["canonical_theory_cycle"] == "cycle.json"
    with pytest.raises(ExportError, match="outside the selected catalog"):
        marathon_catalog(tmp_path, None, None, "state", {"unknown": {}})


def test_catalog_rejects_symlink_run_before_reading(tmp_path):
    from integrations.domain_package.export import marathon_catalog
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "run_state.json").write_text("not JSON and must not be read")
    runs = tmp_path / "agentic/runs/discovery_marathons"
    runs.mkdir(parents=True)
    (runs / "run-a").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="symlinks"):
        marathon_catalog(tmp_path, None, None, "state")


@pytest.mark.parametrize("target", [adapter.TARGET, "p-vs-np-target"])
def test_source_markdown_retains_target_specific_report_sections(target):
    import re
    from build_discovery_marathon_report import render_markdown
    directory = ROOT / "agentic/reports/discovery_marathon/targets" / target
    report = json.loads((directory / "latest.json").read_text())
    expected = re.findall(r"^## (.+)$", (directory / "latest.md").read_text(), re.M)
    assert re.findall(r"^## (.+)$", render_markdown(report), re.M) == expected
