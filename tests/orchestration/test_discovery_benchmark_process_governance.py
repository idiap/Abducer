# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial tests for benchmark subprocess isolation and epistemic nulls."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

import agentic.discovery.benchmark as benchmark_module
from agentic.discovery.benchmark import VERIFIER_EXECUTION_KEY, build_human_evidence_trust_anchor
from agentic.discovery.benchmark_process import (
    ExternalBenchmarkProcessAdapter,
    ExternalBenchmarkProcessError,
    ExternalProcessValidationContext,
    validate_external_process_summary,
)
from agentic.discovery.budgets import (
    ResourceBudget,
    ResourceGovernor,
    complete_governed_process_environment,
    minimal_replacement_environment,
    validate_v2_process_event,
)
from agentic.discovery.contracts import (
    SchemaValidationError,
    canonical_digest,
    canonical_json,
    validate_payload,
)


def _budget(wall: float = 1.0) -> ResourceBudget:
    return ResourceBudget.from_mapping({"budget_id": "test", "wall_time_seconds": wall, "grace_period_seconds": 0.05, "cpu_seconds": max(1.0, wall), "memory_bytes": 256 * 1024 * 1024, "disk_bytes": 1024 * 1024, "network_bytes": 0, "token_count": 10, "request_count": 1, "cost_usd": 0.0})


def _request() -> dict:
    return {"benchmark_id": "bench", "case_id": "case", "domain": "domain", "condition": "full_discovery", "repetition": 1, "task_packet": {"question": "q"}, "task_packet_digest": "sha256:" + "a" * 64, "resource_budget": {"tokens": 10, "wall_seconds": 1.0, "cost_units": 1.0}, "forbidden_generation_input_classes": []}


def _adapter(tmp_path: Path, code: str, *, role: str = "benchmark_runner", **limits: object) -> ExternalBenchmarkProcessAdapter:
    return ExternalBenchmarkProcessAdapter(command=[sys.executable, "-c", code], role=role, benchmark_id="bench", benchmark_run_id=f"run-{role}", run_root=tmp_path, **limits)


def test_governor_delivers_bounded_stdin_with_exact_digest(tmp_path: Path) -> None:
    payload = b'{"hello":"world"}\n'
    governor = ResourceGovernor(_budget(), run_directory=tmp_path)
    result = governor.run_process([sys.executable, "-c", "import sys; d=sys.stdin.buffer.read(); print(len(d))"], cwd=tmp_path, input_bytes=payload, input_limit_bytes=len(payload), stdout_limit_bytes=100, stderr_limit_bytes=100)
    assert result["status"] == "succeeded"
    assert result["stdin_written_bytes"] == len(payload)
    assert result["stdin_sha256"].startswith("sha256:")
    assert result["stdout_utf8_valid"] is True
    assert result["stdout"].strip() == str(len(payload))


def test_governor_rejects_oversize_input_before_spawn(tmp_path: Path) -> None:
    marker = tmp_path / "must-not-exist"
    governor = ResourceGovernor(_budget(), run_directory=tmp_path)
    result = governor.run_process([sys.executable, "-c", f"open({str(marker)!r},'w').write('bad')"], cwd=tmp_path, input_bytes=b"x" * 100, input_limit_bytes=10)
    assert result["status"] == "input_exhausted"
    assert result["pid"] is None
    assert result["epistemic_effect"] == "none_operational_outcome_only"
    assert not marker.exists()


@pytest.mark.skipif(os.name != "posix", reason="full process-group assertion is POSIX-specific")
def test_hard_output_cap_kills_descendants_before_side_effect(tmp_path: Path) -> None:
    marker = tmp_path / "late-marker"
    descendant = f"import time; time.sleep(.4); open({str(marker)!r},'w').write('bad')"
    code = f"import subprocess,sys,time; subprocess.Popen([sys.executable,'-c',{descendant!r}]); sys.stdout.write('x'*200000); sys.stdout.flush(); time.sleep(5)"
    governor = ResourceGovernor(_budget(2.0), run_directory=tmp_path, capture_limit_bytes=128)
    result = governor.run_process([sys.executable, "-c", code], cwd=tmp_path, stdout_limit_bytes=128, stderr_limit_bytes=128)
    assert result["status"] == "output_exhausted"
    assert result["terminal_dimension"] == "stdout_bytes"
    assert result["stdout_bytes"] > 128
    assert result["stdout_retained_bytes"] <= 128
    time.sleep(0.5)
    assert not marker.exists()


def test_invalid_utf8_is_reported_without_corrupting_byte_digest(tmp_path: Path) -> None:
    governor = ResourceGovernor(_budget(), run_directory=tmp_path)
    result = governor.run_process([sys.executable, "-c", "import os; os.write(1,b'\\xff')"], cwd=tmp_path)
    assert result["status"] == "succeeded"
    assert result["stdout_utf8_valid"] is False
    assert result["stdout_bytes"] == 1
    assert result["stdout_sha256"].startswith("sha256:")


def test_adapter_uses_exact_workspace_and_seals_receipt_index(tmp_path: Path) -> None:
    code = "import json,os,sys; from pathlib import Path; r=json.load(sys.stdin); p=Path('spawn-count'); n=int(p.read_text())+1 if p.exists() else 1; p.write_text(str(n)); open('local.bin','wb').write(b'x'*32); print(json.dumps({'candidate_output':{'cwd':os.getcwd(),'spawn_count':n},'resource_usage':{'tokens':2,'wall_seconds':.1,'cost_units':.5},'generation_input_refs':['tasks/case.json']}))"
    adapter = _adapter(tmp_path, code)
    result = adapter.hidden_runner(_request())
    summary = result["__abducer_runner_execution__"]
    assert summary["outcome_status"] == "accepted"
    assert Path(result["candidate_output"]["cwd"]).resolve() == (adapter.run_directory / summary["workspace_ref"]).resolve()
    receipt_path = next((adapter.run_directory / "receipts/benchmark_runner").glob("*.json"))
    receipt_mtime = receipt_path.stat().st_mtime_ns
    retried = adapter.hidden_runner(_request())
    assert retried == result
    assert retried["candidate_output"]["spawn_count"] == 1
    assert (adapter.run_directory / summary["workspace_ref"] / "spawn-count").read_text() == "1"
    assert receipt_path.stat().st_mtime_ns == receipt_mtime
    assert len(list((adapter.run_directory / "workspaces/benchmark_runner").iterdir())) == 1
    index = adapter.finalize()
    assert index["receipt_count"] == 1
    assert index["accounting_boundary"]["cost_units"] == "benchmark_payload_units_not_relabelled_as_cost_usd"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    validate_payload(receipt, "benchmark_external_process_receipt.schema.json")
    assert receipt["command_authority_observation"]["status"] == "exact_match"
    assert summary["command_authority_observation_digest"] == receipt["command_authority_observation"]["content_digest"]
    assert receipt["resource_receipt"]["resource_measurement"]["disk_bytes"]["accounting_root"] == str((adapter.run_directory / summary["workspace_ref"]).resolve())


@pytest.mark.parametrize("code,protocol", [("print('not-json')", "invalid_json"), ("import os; os.write(1,b'\\xff')", "invalid_utf8"), ("import sys; sys.stdout.write('x'*10000)", "output_exhausted")])
def test_adapter_rejects_protocol_and_cap_failures(tmp_path: Path, code: str, protocol: str) -> None:
    adapter = _adapter(tmp_path / protocol, code, stdout_limit_bytes=128)
    with pytest.raises(ExternalBenchmarkProcessError) as raised:
        adapter.hidden_runner(_request())
    assert raised.value.receipt["protocol_status"] == protocol
    assert raised.value.receipt["epistemic_effect"] == "none_process_execution_has_no_epistemic_authority"
    adapter.finalize()


@pytest.mark.skipif(os.name != "posix", reason="full process-group assertion is POSIX-specific")
def test_adapter_timeout_kills_late_descendant(tmp_path: Path) -> None:
    marker = tmp_path / "late"
    descendant = f"import time; time.sleep(.4); open({str(marker)!r},'w').write('bad')"
    code = f"import subprocess,sys,time; subprocess.Popen([sys.executable,'-c',{descendant!r}]); time.sleep(5)"
    request = _request()
    # Keep this below the supervisor's optional-sampling threshold so this
    # case exercises deadline exhaustion rather than the distinct sampled-
    # descendant rejection lane.
    request["resource_budget"]["wall_seconds"] = 0.08
    adapter = _adapter(tmp_path / "timeout", code)
    with pytest.raises(ExternalBenchmarkProcessError) as raised:
        adapter.hidden_runner(request)
    assert raised.value.receipt["process_status"] == "deadline_exhausted"
    time.sleep(0.5)
    assert not marker.exists()


def test_verifier_operational_failure_is_not_authentication_rejection(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    adapter = _adapter(tmp_path, "raise SystemExit(3)", role="human_evidence_verifier")
    outcome = adapter.verifier(b"{}", {"authority_id": "authority"})
    execution = outcome[VERIFIER_EXECUTION_KEY]
    assert execution["outcome_status"] == "operational_failure"

    monkeypatch.setattr(benchmark_module, "_validate_live_manifest", lambda manifest: ([{"case_id": "c"}], ["d"], ("full_discovery",), 5, {"tokens": 1, "wall_seconds": 1.0, "cost_units": 1.0}))
    monkeypatch.setattr(benchmark_module, "_validate_capture", lambda *args, **kwargs: ({"content_digest": "sha256:" + "b" * 64}, {}))
    monkeypatch.setattr(benchmark_module, "_automatic_live_metrics", lambda *args: {})
    monkeypatch.setattr(benchmark_module, "_load_descriptor_bytes", lambda *args: b"{}")
    manifest = {"benchmark_id": "bench", "human_evidence": {"authority_id": "authority"}}
    anchor = build_human_evidence_trust_anchor(
        trust_anchor_id="test-anchor",
        authority_id="authority",
        benchmark_id="bench",
        verifier_command_authority_digest=adapter.command_authority["content_digest"],
    )
    report = benchmark_module._evaluate_live_manifest(
        tmp_path / "manifest.json", manifest, lambda raw, descriptor: outcome, anchor
    )
    assert report["human_evidence"]["status"] == "verifier_operational_failure"
    assert report["human_evidence"]["epistemic_effect"] == "none_operational_outcome_only"
    assert report["efficacy_authorized"] is False
    assert report["replicated"] is False

    rejecting = _adapter(
        tmp_path / "rejecting",
        "import json,sys; json.load(sys.stdin); print(json.dumps({'authenticated':False,'blinding_verified':False,'independent_raters_verified':False,'ratings_immutable':False,'artifact_sha256':'sha256:'+'0'*64,'authority_id':'authority'}))",
        role="human_evidence_verifier",
    )
    rejection_anchor = build_human_evidence_trust_anchor(
        trust_anchor_id="rejecting-anchor",
        authority_id="authority",
        benchmark_id="bench",
        verifier_command_authority_digest=rejecting.command_authority["content_digest"],
    )
    rejection = benchmark_module._evaluate_live_manifest(
        tmp_path / "manifest.json", manifest, rejecting.verifier, rejection_anchor
    )
    assert rejection["human_evidence"]["status"] == "authentication_rejected"
    adapter.finalize()


def test_dependency_mutation_persists_expected_observed_null_and_never_spawns(
    tmp_path: Path,
) -> None:
    marker = tmp_path / "must-not-spawn"
    script = tmp_path / "runner.py"
    script.write_text(
        "import json,sys\n"
        f"open({str(marker)!r},'w').write('spawned')\n"
        "json.load(sys.stdin)\n"
        "print(json.dumps({'candidate_output':{'x':1},'resource_usage':{'tokens':1,'wall_seconds':.1,'cost_units':.1},'generation_input_refs':['tasks/case.json']}))\n",
        encoding="utf-8",
    )
    adapter = ExternalBenchmarkProcessAdapter(
        command=[sys.executable, str(script)],
        role="benchmark_runner",
        benchmark_id="bench",
        benchmark_run_id="run-mutation",
        run_root=tmp_path / "runs",
    )
    script.write_text(script.read_text(encoding="utf-8") + "# mutated\n", encoding="utf-8")
    with pytest.raises(ExternalBenchmarkProcessError) as first:
        adapter.hidden_runner(_request())
    with pytest.raises(ExternalBenchmarkProcessError) as retried:
        adapter.hidden_runner(_request())
    assert first.value.receipt == retried.value.receipt
    assert first.value.receipt["protocol_status"] == "authority_mismatch"
    assert first.value.receipt["command_authority_status"] == "mismatch"
    assert not marker.exists()
    receipt_path = next((adapter.run_directory / "receipts/benchmark_runner").glob("*.json"))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    changed = [
        row
        for row in receipt["command_authority_observation"]["entries"]
        if row["observed_status"] != "matched"
    ]
    assert len(changed) == 1
    assert changed[0]["expected_sha256"] != changed[0]["observed_sha256"]
    assert changed[0]["observed_status"] == "bytes_mismatch"
    assert receipt["process_event"]["pid"] is None
    assert adapter.finalize()["receipt_count"] == 1


def test_invalid_utf8_verifier_request_is_immutable_idempotent_and_indexed(
    tmp_path: Path,
) -> None:
    adapter = _adapter(
        tmp_path,
        "raise SystemExit('must not spawn')",
        role="human_evidence_verifier",
    )
    first = adapter.verifier(b"\xff", {"authority_id": "authority"})
    second = adapter.verifier(b"\xff", {"authority_id": "authority"})
    assert first == second
    summary = first[VERIFIER_EXECUTION_KEY]
    assert summary["protocol_status"] == "request_encoding_failed"
    assert summary["outcome_status"] == "protocol_failure"
    assert adapter.index_path.is_file()
    index = adapter.finalize()
    assert index["receipt_count"] == 1
    receipt_path = adapter.run_directory / summary["receipt_ref"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["process_event"]["pid"] is None
    assert receipt["resource_receipt"]["events"] == [receipt["process_event"]]


def test_validation_context_is_deeply_detached_linear_and_finally_replayed(
    tmp_path: Path,
) -> None:
    adapter = _adapter(
        tmp_path,
        "import json,sys; r=json.load(sys.stdin); print(json.dumps({'candidate_output':{'repetition':r['repetition']},'resource_usage':{'tokens':1,'wall_seconds':.1,'cost_units':.1},'generation_input_refs':['tasks/case.json']}))",
    )
    summaries = []
    for repetition in (1, 2):
        request = _request()
        request["repetition"] = repetition
        summaries.append(adapter.hidden_runner(request)["__abducer_runner_execution__"])
    adapter.finalize()

    context = ExternalProcessValidationContext()
    first = validate_external_process_summary(
        summaries[0],
        role="benchmark_runner",
        require_index=True,
        validation_context=context,
    )
    validate_external_process_summary(
        summaries[1],
        role="benchmark_runner",
        require_index=True,
        validation_context=context,
    )
    # A consumer receives a deep copy. Mutating it cannot alter cached authority.
    first["workspace"]["resolved_path"] = "caller-cache-poison"
    reopened = validate_external_process_summary(
        summaries[0],
        role="benchmark_runner",
        require_index=True,
        validation_context=context,
    )
    assert reopened["workspace"]["resolved_path"] != "caller-cache-poison"
    assert context.replay_counts == {
        "index_replays": 1,
        "receipt_replays": 2,
        "authority_replays": 1,
        "index_cache_hits": 2,
        "receipt_cache_hits": 3,
        "final_index_checks": 0,
        "final_receipt_checks": 0,
        "final_authority_checks": 0,
    }
    context.assert_unchanged()
    assert context.replay_counts["final_index_checks"] == 1
    assert context.replay_counts["final_receipt_checks"] == 2
    assert context.replay_counts["final_authority_checks"] == 1


@pytest.mark.parametrize("target", ["receipt", "index"])
def test_warm_validation_context_rejects_disk_tamper(
    tmp_path: Path, target: str
) -> None:
    adapter = _adapter(
        tmp_path / target,
        "import json,sys; json.load(sys.stdin); print(json.dumps({'candidate_output':{'x':1},'resource_usage':{'tokens':1,'wall_seconds':.1,'cost_units':.1},'generation_input_refs':['tasks/case.json']}))",
    )
    summary = adapter.hidden_runner(_request())["__abducer_runner_execution__"]
    adapter.finalize()
    context = ExternalProcessValidationContext()
    validate_external_process_summary(
        summary,
        role="benchmark_runner",
        require_index=True,
        validation_context=context,
    )
    path = adapter.run_directory / summary[
        "receipt_ref" if target == "receipt" else "index_ref"
    ]
    payload = json.loads(path.read_text(encoding="utf-8"))
    if target == "receipt":
        payload["workspace"]["resolved_path"] = str(tmp_path / "forged")
    else:
        payload["receipt_count"] = 0
    payload["content_digest"] = canonical_digest(
        {key: value for key, value in payload.items() if key != "content_digest"}
    )
    _rewrite_json(path, payload)
    with pytest.raises(benchmark_module.BenchmarkIntegrityError, match="changed after replay"):
        validate_external_process_summary(
            summary,
            role="benchmark_runner",
            require_index=True,
            validation_context=context,
        )


def test_final_validation_context_rechecks_live_dependency_bytes(tmp_path: Path) -> None:
    script = tmp_path / "runner.py"
    script.write_text(
        "import json,sys\n"
        "json.load(sys.stdin)\n"
        "print(json.dumps({'candidate_output':{'x':1},'resource_usage':{'tokens':1,'wall_seconds':.1,'cost_units':.1},'generation_input_refs':['tasks/case.json']}))\n",
        encoding="utf-8",
    )
    adapter = ExternalBenchmarkProcessAdapter(
        command=[sys.executable, str(script)],
        role="benchmark_runner",
        benchmark_id="bench",
        benchmark_run_id="run-final-drift",
        run_root=tmp_path / "runs",
    )
    summary = adapter.hidden_runner(_request())["__abducer_runner_execution__"]
    adapter.finalize()
    context = ExternalProcessValidationContext()
    validate_external_process_summary(
        summary,
        role="benchmark_runner",
        require_index=True,
        validation_context=context,
    )
    script.write_text(script.read_text(encoding="utf-8") + "# drift\n", encoding="utf-8")
    with pytest.raises(benchmark_module.BenchmarkIntegrityError, match="approved bytes"):
        context.assert_unchanged()


def test_local_process_exfiltration_canaries_are_typed_protocol_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    withheld = tmp_path / "run-benchmark_runner" / "withheld-truth.txt"
    monkeypatch.setenv("ABDUCER_BENCHMARK_CANARY", "environment-readable")
    code = (
        "import json,os,socket,subprocess,sys; from pathlib import Path; json.load(sys.stdin); "
        f"absolute=Path({str(withheld)!r}); "
        "relative=Path('../../../withheld-truth.txt'); link=Path('truth-link'); "
        "link.symlink_to(absolute); child=subprocess.check_output([sys.executable,'-c','print(\"child\")'],text=True).strip(); "
        "sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM); socket_created=sock.fileno()>=0; sock.close(); "
        "print(json.dumps({'candidate_output':{'traversal':relative.read_text(),'absolute':absolute.read_text(),"
        "'symlink':link.read_text(),'environment':os.environ.get('ABDUCER_BENCHMARK_CANARY'),"
        "'process':child,'network_socket_created':socket_created},'resource_usage':{'tokens':1,'wall_seconds':.1,'cost_units':.1},"
        "'generation_input_refs':['tasks/case.json']}))"
    )
    adapter = _adapter(tmp_path, code)
    withheld.write_text("withheld-readable", encoding="utf-8")
    result = adapter.hidden_runner(_request())
    candidate = result["candidate_output"]
    assert candidate == {
        "traversal": "withheld-readable",
        "absolute": "withheld-readable",
        "symlink": "withheld-readable",
        "environment": None,
        "process": "child",
        "network_socket_created": True,
    }
    summary = result["__abducer_runner_execution__"]
    assert summary["isolation_status"] == "unisolated_protocol_only"
    assert summary["external_efficacy_eligible"] is False
    receipt = json.loads(
        (adapter.run_directory / summary["receipt_ref"]).read_text(encoding="utf-8")
    )
    assurance = receipt["isolation_assurance"]
    assert assurance["deny_by_construction"] is False
    assert assurance["external_efficacy_eligible"] is False
    event = receipt["process_event"]
    execution = event["resource_limit_execution"]
    assert execution["replacement_environment_used"] is True
    workspace = Path(receipt["workspace"]["resolved_path"])
    expected_environment = complete_governed_process_environment(
        minimal_replacement_environment(workspace, create_temporary=False),
        deadline=receipt["resource_receipt"]["deadline"],
        budget=receipt["resource_receipt"]["budget"],
    )
    observed_names = [
        row["name"]
        for row in event["supervision_attempt"]["request"]["environment_bindings"]
    ]
    assert observed_names == sorted(expected_environment)
    assert "ABDUCER_BENCHMARK_CANARY" not in observed_names
    wrong_policy = dict(expected_environment)
    wrong_policy["LANG"] = "not-the-launched-policy"
    with pytest.raises(ValueError, match="exact replacement-environment policy"):
        validate_v2_process_event(
            event,
            accepted=True,
            expected_workspace=workspace,
            expected_replacement_environment=wrong_policy,
        )

    forged_false_flag = copy.deepcopy(receipt)
    forged_false_flag["process_event"]["resource_limit_execution"][
        "replacement_environment_used"
    ] = False
    forged_false_flag["resource_receipt"]["events"] = [
        copy.deepcopy(forged_false_flag["process_event"])
    ]
    with pytest.raises(SchemaValidationError):
        validate_payload(
            forged_false_flag,
            "benchmark_external_process_receipt.schema.json",
        )
    assert set(assurance["channels"]) == {
        "declared_input_only",
        "filesystem",
        "environment",
        "process",
        "network",
        "symlink_and_absolute_path",
        "undeclared_access_audit",
    }
    adapter.finalize()


def _rewrite_json(path: Path, payload: dict) -> None:
    path.write_bytes(canonical_json(payload) + b"\n")


@pytest.mark.parametrize(
    "mutation",
    ["summary", "nested_authority", "workspace", "accounting", "index"],
)
def test_summary_receipt_index_workspace_and_accounting_tamper_fail_closed(
    tmp_path: Path, mutation: str
) -> None:
    adapter = _adapter(
        tmp_path / mutation,
        "import json,sys; json.load(sys.stdin); print(json.dumps({'candidate_output':{'x':1},'resource_usage':{'tokens':1,'wall_seconds':.1,'cost_units':.1},'generation_input_refs':['tasks/case.json']}))",
    )
    output = adapter.hidden_runner(_request())
    summary = copy.deepcopy(output["__abducer_runner_execution__"])
    adapter.finalize()
    receipt_path = adapter.run_directory / summary["receipt_ref"]
    index_path = adapter.run_directory / summary["index_ref"]
    if mutation == "summary":
        summary["workspace_digest"] = "sha256:" + "f" * 64
    elif mutation == "index":
        index = json.loads(index_path.read_text(encoding="utf-8"))
        index["receipt_count"] = 0
        index["receipts"] = []
        index["content_digest"] = canonical_digest(
            {key: value for key, value in index.items() if key != "content_digest"}
        )
        _rewrite_json(index_path, index)
    else:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if mutation == "nested_authority":
            receipt["command_authority"]["argv_digest"] = "sha256:" + "e" * 64
        elif mutation == "workspace":
            receipt["workspace"]["resolved_path"] = str(tmp_path / "wrong-workspace")
            receipt["workspace"]["workspace_digest"] = canonical_digest(
                {
                    key: value
                    for key, value in receipt["workspace"].items()
                    if key != "workspace_digest"
                }
            )
        else:
            receipt["resource_receipt"]["resource_measurement"]["disk_bytes"]["accounting_root"] = str(tmp_path / "wrong-accounting")
            receipt["resource_receipt_digest"] = canonical_digest(receipt["resource_receipt"])
        receipt["content_digest"] = canonical_digest(
            {key: value for key, value in receipt.items() if key != "content_digest"}
        )
        _rewrite_json(receipt_path, receipt)
    with pytest.raises(benchmark_module.BenchmarkIntegrityError):
        validate_external_process_summary(
            summary, role="benchmark_runner", require_index=True
        )


def test_legacy_launch_error_is_present_in_resource_accounting(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    script = (
        Path(__file__).resolve().parents[2]
        / "skills/orchestration/kb-orchestrator/scripts/simulate_theorem_discovery.py"
    )
    spec = importlib.util.spec_from_file_location("benchmark_legacy_simulator", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    def fail_launch(*_args: object, **_kwargs: object) -> dict:
        raise OSError("launch unavailable")

    monkeypatch.setattr(ResourceGovernor, "run_process", fail_launch)

    class Logger:
        def step(self, *_args: object, **_kwargs: object) -> None:
            return None

    code, output, receipt = module._run_command(
        ["missing-python", "stage.py"], Logger(), "stage", tmp_path, tmp_path
    )
    assert code == 1
    assert "launch unavailable" in output
    assert receipt["status"] == "worker_failed"
    assert len(receipt["events"]) == 1
    event = receipt["events"][0]
    assert event["pid"] is None
    assert event["termination"] == "not_started"
    assert event["epistemic_effect"] == "none_operational_outcome_only"


@pytest.mark.parametrize(
    "case,extra_args,expected",
    [
        ("missing", [], "benchmark_manifest_load_failed"),
        ("malformed", [], "benchmark_manifest_load_failed"),
        (
            "bad-command",
            ["--benchmark-capture-output", "capture.json", "--benchmark-runner-command", "[", "--benchmark-run-id", "run-bad-command"],
            "benchmark_runner_command_manifest_invalid",
        ),
        (
            "missing-anchor",
            ["--human-evidence-verifier-command", "[\"python\",\"-c\",\"print(1)\"]", "--benchmark-run-id", "run-missing-anchor"],
            "separately configured trust anchor",
        ),
    ],
)
def test_benchmark_cli_missing_and_malformed_inputs_are_typed(
    tmp_path: Path, case: str, extra_args: list[str], expected: str
) -> None:
    simulator = (
        Path(__file__).resolve().parents[2]
        / "skills/orchestration/kb-orchestrator/scripts/simulate_theorem_discovery.py"
    )
    manifest = tmp_path / "manifest.json"
    if case == "malformed":
        manifest.write_text("{", encoding="utf-8")
    elif case != "missing":
        manifest.write_text(json.dumps({"benchmark_id": "bench"}), encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(simulator), "--benchmark-manifest", str(manifest), *extra_args],
        cwd=Path(__file__).resolve().parents[2],
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 2
    error = json.loads(completed.stderr.strip().splitlines()[-1])
    assert error["status"] == "benchmark_integrity_error"
    assert expected in error["message"]
    assert error["epistemic_effect"] == "none_operational_outcome_only"
