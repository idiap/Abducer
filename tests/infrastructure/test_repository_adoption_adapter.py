# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Exercise the real maintenance boundary and adversarial durable replay joins."""
from __future__ import annotations

import concurrent.futures
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "proj_skills/scripts/repository_adoption_adapter.py"
LEGACY = ROOT / "proj_skills/scripts/validate_proj_skills.py"
spec = importlib.util.spec_from_file_location("repository_adoption_adapter", SCRIPT)
adapter = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = adapter
spec.loader.exec_module(adapter)


@pytest.mark.parametrize("args", [[], ["--help"], ["--root"], ["--unexpected"], ["--root", "absent"], ["--root", "--unexpected"]])
def test_real_cli_preserves_bytes_and_exit_from_alternate_cwd(tmp_path, args):
    legacy = subprocess.run([sys.executable, str(LEGACY), *args], cwd=tmp_path, capture_output=True)
    candidate = subprocess.run([sys.executable, str(SCRIPT), adapter.OPERATION, "--", *args], cwd=tmp_path, capture_output=True)
    assert (candidate.stdout, candidate.stderr, candidate.returncode) == (legacy.stdout, legacy.stderr, legacy.returncode)
    assert list(tmp_path.iterdir()) == []


def context(attempt=1, invocation="call", run="run"):
    return adapter.InvocationContext(run, invocation, attempt)


def invoke(tmp_path, *, ctx=None, replay=False, args=None):
    return adapter.invoke(adapter.OPERATION, args or ["--help"], trace_root=tmp_path,
                          context=ctx or context(), replay=replay)


def directory(tmp_path):
    return tmp_path / "invocations/run/call/1"


def test_native_event_schema_terminal_digest_and_replay_no_respawn(tmp_path, monkeypatch):
    original = invoke(tmp_path)
    event = json.loads((tmp_path / "repository-adoption/runs/run/events.jsonl").read_text())
    jsonschema.validate(event, json.loads((ROOT / "agentic/spec/public_reasoning_event.schema.json").read_text()))
    terminal = event["control"]["terminal_result"]
    assert adapter._digest(Path(terminal["path"]).read_bytes()) == terminal["sha256"]
    assert event["claim_epistemic_status"] == "not_applicable"
    assert event["skill"] is None
    monkeypatch.setattr(adapter, "_execute", lambda *a, **k: pytest.fail("replay must not spawn"))
    repeated = invoke(tmp_path, replay=True)
    assert (repeated.returncode, repeated.stdout, repeated.stderr) == (original.returncode, original.stdout, original.stderr)
    assert len((tmp_path / "repository-adoption/runs/run/events.jsonl").read_text().splitlines()) == 1
    with pytest.raises(adapter.ReplayError, match="already used"):
        invoke(tmp_path)


@pytest.mark.parametrize("mutation", ["tamper", "cross-run", "type-substitution", "arguments", "missing", "incomplete"])
def test_replay_rejects_wrong_or_incomplete_join(tmp_path, monkeypatch, mutation):
    invoke(tmp_path)
    result_path = directory(tmp_path) / "result.json"
    if mutation == "tamper":
        result_path.write_bytes(result_path.read_bytes() + b" ")
    elif mutation in {"cross-run", "type-substitution"}:
        payload = json.loads(result_path.read_bytes())
        if mutation == "cross-run":
            payload["request"]["context"]["run_id"] = "another-run"
        else:
            payload["request"]["context"]["attempt"] = True
        data = adapter._bytes(payload)
        result_path.write_bytes(data)
        manifest_path = directory(tmp_path) / "invocation.json"
        manifest = json.loads(manifest_path.read_bytes())
        manifest["result_sha256"] = adapter._digest(data)
        manifest_path.write_bytes(adapter._bytes(manifest))
    elif mutation == "missing":
        result_path.unlink()
    elif mutation == "incomplete":
        manifest_path = directory(tmp_path) / "invocation.json"
        manifest = json.loads(manifest_path.read_bytes())
        manifest["status"] = "started"
        manifest_path.write_bytes(adapter._bytes(manifest))
    monkeypatch.setattr(adapter, "_execute", lambda *a, **k: pytest.fail("bad replay must not spawn"))
    with pytest.raises(adapter.ReplayError):
        invoke(tmp_path, replay=True, args=["--root", "absent"] if mutation == "arguments" else None)


def test_retry_and_independent_identical_inputs_have_distinct_identity(tmp_path):
    invoke(tmp_path)
    invoke(tmp_path, ctx=context(attempt=2))
    invoke(tmp_path, ctx=context(invocation="independent"))
    events = [json.loads(line) for line in (tmp_path / "repository-adoption/runs/run/events.jsonl").read_text().splitlines()]
    assert len({event["event_id"] for event in events}) == 3
    assert [event["attempt"] for event in events] == [1, 2, 1]


def test_default_host_invocations_are_distinct(tmp_path):
    for _ in range(2):
        adapter.invoke(adapter.OPERATION, ["--help"], trace_root=tmp_path)
    assert len(list((tmp_path / "invocations").iterdir())) == 2


def test_parallel_duplicate_executes_once(tmp_path, monkeypatch):
    calls = []
    original = adapter._execute
    def counted(*a, **kw):
        calls.append(a)
        return original(*a, **kw)
    monkeypatch.setattr(adapter, "_execute", counted)
    def run():
        try:
            return invoke(tmp_path).returncode
        except adapter.ReplayError:
            return "duplicate"
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: run(), range(2)))
    assert sorted(map(str, results)) == ["0", "duplicate"]
    assert len(calls) == 1


def test_parallel_independent_processes_native_store_is_consistent(tmp_path):
    def run(index):
        return subprocess.run([sys.executable, str(SCRIPT), adapter.OPERATION,
            "--trace-root", str(tmp_path), "--run-id", "parallel", "--invocation-id", str(index),
            "--", "--help"], capture_output=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, range(4)))
    assert all(result.returncode == 0 for result in results)
    events = [json.loads(line) for line in (tmp_path / "repository-adoption/runs/parallel/events.jsonl").read_text().splitlines()]
    assert [event["sequence"] for event in events] == [1, 2, 3, 4]
    assert len({event["event_id"] for event in events}) == 4


@pytest.mark.parametrize("exception", [OSError("spawn failed"), KeyboardInterrupt()])
def test_underlying_exception_or_cancellation_preserved_without_replay(tmp_path, monkeypatch, exception):
    def fail(*a, **k):
        raise exception
    monkeypatch.setattr(adapter, "_execute", fail)
    with pytest.raises(type(exception)) as caught:
        invoke(tmp_path)
    assert caught.value is exception
    with pytest.raises(adapter.ReplayError, match="completed receipt"):
        invoke(tmp_path, replay=True)


def test_process_crash_after_reservation_never_reexecutes(tmp_path):
    # A real process dies after durable reservation and before subprocess dispatch.
    code = f'''import importlib.util,sys,os
s=importlib.util.spec_from_file_location("adapter", {str(SCRIPT)!r})
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
m._execute=lambda *a,**k: os._exit(73)
m.invoke(m.OPERATION,["--help"],trace_root=m.Path({str(tmp_path)!r}),context=m.InvocationContext("run","call"))
'''
    result = subprocess.run([sys.executable, "-c", code], capture_output=True)
    assert result.returncode == 73
    with pytest.raises(adapter.ReplayError, match="completed receipt"):
        invoke(tmp_path, replay=True)


def test_optional_trace_and_storage_failure_preserve_owner_result(tmp_path, monkeypatch):
    expected = adapter.invoke(adapter.OPERATION, ["--root", "absent"])
    def fail(*a, **k):
        raise RuntimeError("sink and diagnostic unavailable")
    monkeypatch.setattr(adapter, "_emit", fail)
    result = invoke(tmp_path, args=["--root", "absent"])
    assert (result.returncode, result.stdout, result.stderr) == (expected.returncode, expected.stdout, expected.stderr)
    unavailable = tmp_path / "file"
    unavailable.write_text("not a directory")
    result = invoke(unavailable, args=["--root", "absent"])
    assert (result.returncode, result.stdout, result.stderr) == (expected.returncode, expected.stdout, expected.stderr)
    with pytest.raises(adapter.ReplayError):
        invoke(unavailable, replay=True)


def test_instruction_only_and_modified_binding_never_spawn(tmp_path, monkeypatch):
    monkeypatch.setattr(adapter, "_execute", lambda *a, **k: pytest.fail("unreviewed binding"))
    with pytest.raises(ValueError, match="no reviewed"):
        adapter.invoke("project-state-profiler", [])
    registry = json.loads(adapter.REGISTRY.read_text())
    registry["operations"][0]["implementation"] = "unreviewed.py"
    path = tmp_path / "registry.json"
    path.write_text(json.dumps(registry))
    monkeypatch.setattr(adapter, "REGISTRY", path)
    with pytest.raises(ValueError, match="no reviewed"):
        adapter.invoke(adapter.OPERATION, [])


def test_context_path_escape_and_replay_without_identity_rejected(tmp_path):
    for bad in (None, 42, "..", ".", "a/b", "", "space here"):
        with pytest.raises(ValueError):
            adapter.InvocationContext(bad, "valid")
    with pytest.raises(adapter.ReplayError):
        adapter.invoke(adapter.OPERATION, [], trace_root=tmp_path, replay=True)


@pytest.mark.parametrize("parent_only", [False, True])
def test_real_process_group_cancellation_leaves_unknown_receipt(tmp_path, parent_only):
    """Cancel a validator blocked on fixture input; replay cannot infer completion."""
    import os
    import signal
    import time
    fixture = tmp_path / "fixture"
    fixture.mkdir()
    (fixture / "catalog.yaml").write_text('{"skills": ["blocking"]}')
    (fixture / "blocking").mkdir()
    os.mkfifo(fixture / "blocking/SKILL.md")
    trace = tmp_path / "trace"
    args = ["--root", str(fixture)]
    process = subprocess.Popen([sys.executable, str(SCRIPT), adapter.OPERATION,
        "--trace-root", str(trace), "--run-id", "run", "--invocation-id", "call",
        "--", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        deadline = time.monotonic() + 5
        while not (directory(trace) / "invocation.json").exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert (directory(trace) / "invocation.json").is_file()
        children = []
        while not children and time.monotonic() < deadline:
            listing = subprocess.run(["ps", "-ax", "-o", "pid=,ppid="], capture_output=True, text=True, check=True)
            children = [int(fields[0]) for line in listing.stdout.splitlines()
                        if len(fields := line.split()) == 2 and int(fields[1]) == process.pid]
            if not children:
                time.sleep(0.01)
        assert children, "validator subprocess must have started before cancellation"
        if parent_only:
            process.terminate()
        else:
            os.killpg(process.pid, signal.SIGTERM)
        process.communicate(timeout=5)
        assert process.returncode == -signal.SIGTERM
        for child in children:
            with pytest.raises(ProcessLookupError):
                os.kill(child, 0)
        with pytest.raises(adapter.ReplayError, match="completed receipt"):
            invoke(trace, replay=True, args=args)
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate(timeout=5)


def test_underlying_unhandled_exception_cli_traceback_bytes_are_unchanged(tmp_path):
    fixture = tmp_path / "fixture"
    fixture.mkdir()
    (fixture / "catalog.yaml").write_bytes(b"\xff")
    legacy = subprocess.run([sys.executable, str(LEGACY), "--root", str(fixture)], capture_output=True)
    candidate = subprocess.run([sys.executable, str(SCRIPT), adapter.OPERATION,
        "--", "--root", str(fixture)], capture_output=True)
    assert b"UnicodeDecodeError" in legacy.stderr
    assert (candidate.returncode, candidate.stdout, candidate.stderr) == (legacy.returncode, legacy.stdout, legacy.stderr)



def native_store():
    """Use the actual scientific event owner for namespace-isolation regressions."""
    spec = importlib.util.spec_from_file_location("adoption_isolation_native_store", ROOT / "agentic/scripts/public_reasoning_trace_store.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scientific_event(step="scientific-step"):
    return {"run_id": "run", "workflow_id": "original-scientific-workflow",
            "workflow_version": "1", "target": "scientific-target", "phase": "reasoning",
            "event_family": "exit", "step_id": step, "skill": "original-skill",
            "claim_epistemic_status": "not_applicable"}


def test_same_run_id_preserves_original_scientific_stream_and_manifest(tmp_path):
    store = native_store()
    store.append_event(scientific_event(), store_root=tmp_path)
    original = {path.name: path.read_bytes() for path in (tmp_path / "runs/run").iterdir()}
    assert invoke(tmp_path).returncode == 0
    assert {path.name: path.read_bytes() for path in (tmp_path / "runs/run").iterdir()} == original
    event = json.loads((tmp_path / "repository-adoption/runs/run/events.jsonl").read_text())
    assert event["workflow_id"] == "repository-adoption-maintenance"
    assert event["run_id"] == "run"
    assert Path(event["control"]["terminal_result"]["path"]).parent == directory(tmp_path)


def test_concurrent_scientific_writer_and_maintenance_same_run_are_isolated(tmp_path):
    store = native_store()
    first = store.append_event(scientific_event(), store_root=tmp_path)
    def scientific_writer():
        for index in range(8):
            store.append_event(scientific_event(f"scientific-{index}"), store_root=tmp_path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        original = pool.submit(scientific_writer)
        maintenance = pool.submit(invoke, tmp_path)
        original.result()
        assert maintenance.result().returncode == 0
    events = store.read_events("run", store_root=tmp_path)
    assert len(events) == 9
    assert events[0] == first
    assert {row["workflow_id"] for row in events} == {"original-scientific-workflow"}
    assert [row["sequence"] for row in events] == list(range(1, 10))
    manifest = json.loads((tmp_path / "runs/run/manifest.json").read_text())
    assert manifest["event_count"] == 9
    assert manifest["latest_event_id"] == events[-1]["event_id"]
    assert len(store.read_events("run", store_root=tmp_path / "repository-adoption")) == 1


def test_pre_isolation_receipts_replay_without_moving_old_native_events(tmp_path, monkeypatch):
    original = invoke(tmp_path)
    # The pre-isolation event layout used runs/ directly. Receipts contain no
    # adapter-code digest or event namespace, so those durable bytes remain valid.
    (tmp_path / "repository-adoption/runs").rename(tmp_path / "runs")
    (tmp_path / "repository-adoption").rmdir()
    old_events = (tmp_path / "runs/run/events.jsonl").read_bytes()
    monkeypatch.setattr(adapter, "_execute", lambda *a, **k: pytest.fail("old receipt replay cannot spawn"))
    repeated = invoke(tmp_path, replay=True)
    assert (repeated.returncode, repeated.stdout, repeated.stderr) == (original.returncode, original.stdout, original.stderr)
    assert (tmp_path / "runs/run/events.jsonl").read_bytes() == old_events
    assert not (tmp_path / "repository-adoption").exists()


def test_namespace_symlink_cannot_redirect_into_scientific_store(tmp_path):
    store = native_store()
    store.append_event(scientific_event(), store_root=tmp_path)
    original = {path.name: path.read_bytes() for path in (tmp_path / "runs/run").iterdir()}
    (tmp_path / "repository-adoption").symlink_to(tmp_path, target_is_directory=True)
    # Optional event failure preserves legacy output without touching native runs.
    assert invoke(tmp_path).returncode == 0
    assert {path.name: path.read_bytes() for path in (tmp_path / "runs/run").iterdir()} == original
