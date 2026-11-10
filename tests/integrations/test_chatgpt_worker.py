# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Hosted process/state/provider contracts with explicit controlled fixtures.

No test calls a model or asserts scientific success. The small fixture adapter
checks host plumbing, while existing native-adapter tests cover its real gates.
"""

import hashlib
import io
import json
import os
import subprocess
import sys
import threading
import time
import venv
from pathlib import Path
from types import SimpleNamespace

import pytest

from integrations.chatgpt import runtime
from integrations.chatgpt.provider import HostedServices, ProviderError
from integrations.chatgpt.store import Store
from integrations.chatgpt.worker import Worker, worker_environment

BUDGET = {"timeout_seconds": 60, "max_model_calls": 2, "max_output_tokens": 32000}


def seal(root):
    files = runtime.tree_manifest(root)
    manifest = {
        "version": 1,
        "revision": "fixture",
        "files": files,
        "content_sha256": hashlib.sha256(runtime.json_bytes(files)).hexdigest(),
    }
    (root / runtime.SOURCE_MANIFEST).write_bytes(runtime.json_bytes(manifest))
    return manifest


@pytest.fixture
def snapshot(tmp_path):
    root = tmp_path / "source"
    root.mkdir()
    (root / "example.py").write_text("# controlled fixture\n")
    seal(root)
    return root


def test_snapshot_rejects_changes_new_files_and_symlinks(snapshot):
    runtime.verify_snapshot(snapshot)
    (snapshot / "example.py").write_text("changed")
    with pytest.raises(ValueError, match="differs"):
        runtime.verify_snapshot(snapshot)
    (snapshot / "example.py").write_text("# controlled fixture\n")
    (snapshot / "new").write_text("extra")
    with pytest.raises(ValueError, match="differs"):
        runtime.verify_snapshot(snapshot)
    (snapshot / "new").unlink()
    (snapshot / "new").symlink_to(snapshot / "example.py")
    with pytest.raises(ValueError, match="symlink"):
        runtime.verify_snapshot(snapshot)


def test_snapshot_builder_uses_export_selection_and_never_copies_secrets(tmp_path):
    source = tmp_path / "repo"
    source.mkdir()
    for relative in (
        "README.md",
        "pyproject.toml",
        "uv.lock",
        "abducer-prism/workflows/manifest.json",
        "skills/test/example/SKILL.md",
        "docs/integrations/chatgpt-native-execution.md",
        "docs/integrations/chatgpt-hook-fidelity.md",
        "config/api_keys.json",
    ):
        path = source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture")
    (source / ".env").write_text("SECRET=never-copy")
    subprocess.run(["git", "init", "-q", str(source)], check=True)
    subprocess.run(["git", "-C", str(source), "add", "."], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(source),
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.test",
            "commit",
            "-qm",
            "fixture",
        ],
        check=True,
    )
    (source / "unrelated.txt").write_text("untracked")
    output = tmp_path / "snapshot"
    runtime.build_snapshot(source, output)
    runtime.verify_snapshot(output)
    assert (output / "skills/test/example/SKILL.md").is_file()
    assert (output / "docs/integrations/chatgpt-native-execution.md").is_file()
    assert (output / "docs/integrations/chatgpt-hook-fidelity.md").is_file()
    assert not (output / "config/api_keys.json").exists()
    assert not (output / ".env").exists()
    assert not (output / "unrelated.txt").exists()
    assert set(runtime.PYTHON_LAUNCHERS) <= set(
        runtime.verify_snapshot(output)["files"]
    )
    assert runtime.verify_snapshot(output)["python_launchers"] == list(
        runtime.PYTHON_LAUNCHERS
    )
    assert not (output / ".venv/pyvenv.cfg").exists()
    assert not (output / ".venv-pmp/pyvenv.cfg").exists()


@pytest.mark.skipif(os.name != "posix", reason="POSIX compatibility launchers")
def test_python_launchers_preserve_managed_interpreter_and_arguments(tmp_path):
    snapshot = tmp_path / "source"
    snapshot.mkdir()
    descriptors = runtime.install_python_launchers(snapshot)
    assert descriptors == runtime.tree_manifest(snapshot)
    managed = tmp_path / "managed runtime"
    # uv-managed macOS Python needs its original adjacent dynamic library.
    venv.EnvBuilder(with_pip=False, symlinks=True).create(managed)
    interpreter = managed / "bin/python"
    unrelated = tmp_path / "unrelated"
    unrelated.mkdir()
    environment = {
        "PATH": "/nonexistent",
        "PYTHON": str(interpreter),
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    for relative in runtime.PYTHON_LAUNCHERS:
        actual = json.loads(
            subprocess.check_output(
                [
                    str(snapshot / relative),
                    "-c",
                    "import json,sys; print(json.dumps([sys.prefix,sys.argv[1:]]))",
                    "two words",
                    "$(not a command)",
                ],
                cwd=unrelated,
                env=environment,
                text=True,
                timeout=10,
            )
        )
        assert actual == [str(managed), ["two words", "$(not a command)"]]


@pytest.mark.skipif(os.name != "posix", reason="POSIX compatibility launchers")
def test_python_launchers_refuse_missing_relative_and_recursive_interpreters(tmp_path):
    snapshot = tmp_path / "source"
    snapshot.mkdir()
    runtime.install_python_launchers(snapshot)
    launcher = snapshot / runtime.PYTHON_LAUNCHERS[0]
    nonexecutable = tmp_path / "not executable"
    nonexecutable.write_text("not an interpreter")
    for selected in (
        None,
        "python3",
        str(nonexecutable),
        str(launcher),
        str(snapshot / runtime.PYTHON_LAUNCHERS[-1]),
    ):
        environment = {"PATH": "/nonexistent"}
        if selected is not None:
            environment["PYTHON"] = selected
        result = subprocess.run(
            [str(launcher), "-c", "raise SystemExit(0)"],
            cwd=tmp_path,
            env=environment,
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 126
        assert "Abducer" in result.stderr


def test_python_launchers_refuse_collisions_before_writing(tmp_path):
    snapshot = tmp_path / "source"
    existing = snapshot / runtime.PYTHON_LAUNCHERS[-1]
    existing.parent.mkdir(parents=True)
    existing.write_bytes(b"authored interpreter entrypoint")
    before = runtime.tree_manifest(snapshot)
    with pytest.raises(ValueError, match="collides"):
        runtime.install_python_launchers(snapshot)
    assert runtime.tree_manifest(snapshot) == before


def test_python_launchers_refuse_symlinked_parents(tmp_path):
    snapshot = tmp_path / "source"
    snapshot.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (snapshot / ".venv-pmp").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="Symlinks"):
        runtime.install_python_launchers(snapshot)
    assert not (snapshot / ".venv").exists()
    assert not list(outside.iterdir())


def test_provider_preserves_native_schema_and_bounds_calls(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-secret")
    monkeypatch.setenv("ABDUCER_MODEL", "configured-model")
    calls = []

    def opened(request, timeout):
        calls.append((request, timeout))
        return io.BytesIO(
            json.dumps(
                {
                    "status": "completed",
                    "output": [
                        {
                            "content": [
                                {"type": "output_text", "text": '{"fixture":true}'}
                            ]
                        }
                    ],
                }
            ).encode()
        )

    service = HostedServices(
        {**BUDGET, "max_model_calls": 1},
        allow_public_network=False,
        opener=SimpleNamespace(open=opened),
    )
    schema = {
        "type": "object",
        "properties": {"fixture": {"type": "boolean"}},
        "required": ["fixture"],
        "additionalProperties": False,
    }
    args = {
        "messages": [{"role": "user", "content": "native prompt"}],
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "native", "schema": schema, "strict": True},
        },
        "max_tokens": 32000,
        "reasoning_effort": "high",
    }
    reply = service.completion(**args)
    payload = json.loads(calls[0][0].data)
    assert payload["input"] == args["messages"]
    assert payload["text"]["format"]["schema"] == schema
    assert payload["max_output_tokens"] == 32000 and payload["store"] is False
    assert reply["choices"][0]["finish_reason"] == "stop"
    with pytest.raises(ProviderError, match="budget exhausted"):
        service.completion(**args)
    assert len(calls) == 1


def test_provider_and_literature_fail_closed_before_network(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-secret")
    monkeypatch.setenv("ABDUCER_MODEL", "configured-model")
    service = HostedServices(
        BUDGET,
        allow_public_network=True,
        opener=SimpleNamespace(open=lambda *a, **k: pytest.fail("network")),
    )
    with pytest.raises(ProviderError, match="output token"):
        service.completion(
            messages=[], response_format={"type": "json_object"}, max_tokens=32001
        )
    for url in (
        "http://api.crossref.org/works",
        "https://api.crossref.org.evil.test/works",
        "https://localhost/works",
        "https://api.crossref.org/private",
        "https://user:pass@api.crossref.org/works",
    ):
        with pytest.raises(ProviderError, match="scope"):
            service.public_fetch(
                "open", url=url, resource_id="discovery-live-literature"
            )
    assert service.calls == 0 and service.fetches == 0


def test_worker_environment_does_not_inherit_service_secrets(monkeypatch):
    monkeypatch.setenv("ABDUCER_REPOSITORY_ROOT", "/operator/scientific-source")
    monkeypatch.setenv("OIDC_CLIENT_SECRET", "private")
    monkeypatch.setenv("ABDUCER_OIDC_JWKS_URL", "https://identity.example/jwks")
    monkeypatch.setenv("OPENAI_API_KEY", "worker-model-key")
    monkeypatch.setenv("PYTHONHOME", "/wrong/python-home")
    monkeypatch.setenv("VIRTUAL_ENV", "/wrong/environment")
    environment = worker_environment()
    assert environment["PYTHONPATH"].split(os.pathsep) == [
        str(Path(__file__).resolve().parents[2]),
        "/operator/scientific-source",
    ]
    assert "OIDC_CLIENT_SECRET" not in environment
    assert "ABDUCER_OIDC_JWKS_URL" not in environment
    assert environment["OPENAI_API_KEY"] == "worker-model-key"
    assert environment["PYTHONDONTWRITEBYTECODE"] == "1"
    assert "PYTHONHOME" not in environment
    assert environment["VIRTUAL_ENV"] == sys.prefix
    assert environment["PYTHON"] == sys.executable
    assert environment["PYTHONNOUSERSITE"] == "1"
    import shutil

    child = shutil.which("python", path=environment["PATH"])
    assert child and Path(child).parent == Path(sys.executable).absolute().parent
    # Exercise actual process resolution, rather than just comparing strings.
    result = subprocess.check_output(
        [
            child,
            "-c",
            "import json,sys; print(json.dumps([sys.prefix,sys.executable]))",
        ],
        env=environment,
        text=True,
    )
    assert json.loads(result)[0] == sys.prefix


def queued(store, *, budget=None, runtime_hash=None):
    store.provision_user("alice", "Alice")
    project = store.create_project("alice", "Controlled worker test")
    plan = store.prepare_plan(
        "alice",
        project["id"],
        workflow_id="discovery_marathon_loop",
        inputs={"target_id": "p-vs-np-target", "allow_public_network": True},
        budget=budget or BUDGET,
        release="fixture",
        runtime_source_sha256=runtime_hash,
    )
    job = store.start_job(
        "alice",
        plan["plan_id"],
        "test-key",
        release="fixture",
        runtime_source_sha256=runtime_hash,
    )
    return project, job


def test_real_subprocess_timeout_retains_parent_and_publishes_nothing(
    tmp_path, snapshot, monkeypatch
):
    from integrations.chatgpt import catalog

    monkeypatch.setattr(
        catalog, "Catalog", lambda root: SimpleNamespace(release="fixture")
    )
    store = Store(tmp_path / "service.sqlite3")
    project, job = queued(
        store,
        budget={**BUDGET, "timeout_seconds": 1},
        runtime_hash=runtime.verify_snapshot(snapshot)["content_sha256"],
    )
    worker = Worker(
        store,
        data_root=tmp_path / "data",
        source_root=snapshot,
        poll_seconds=0.05,
        command_factory=lambda *a: [
            sys.executable,
            "-c",
            "import time; time.sleep(60)",
        ],
    )
    assert worker.run_once()
    assert store.get_job("alice", job["id"])["status"] == "failed"
    assert "deadline" in store.get_job("alice", job["id"])["error"]
    assert store.project("alice", project["id"])["version"] == 0
    assert store.artifacts("alice", job["id"]) == []
    assert worker.run_once() is False


def test_real_subprocess_failed_native_run_does_not_release_old_artifacts(
    tmp_path, snapshot, monkeypatch
):
    from integrations.chatgpt import catalog

    monkeypatch.setattr(
        catalog, "Catalog", lambda root: SimpleNamespace(release="fixture")
    )
    store = Store(tmp_path / "service.sqlite3")
    project, job = queued(
        store, runtime_hash=runtime.verify_snapshot(snapshot)["content_sha256"]
    )
    worker = Worker(
        store,
        data_root=tmp_path / "data",
        source_root=snapshot,
        poll_seconds=0.05,
        command_factory=lambda *a: [sys.executable, "-c", "raise SystemExit(3)"],
    )
    worker.run_once()
    assert store.get_job("alice", job["id"])["status"] == "failed"
    assert store.project("alice", project["id"])["checkpoint"] is None


def test_checkpoint_rejects_cross_release_target_and_tamper(tmp_path):
    workspace = tmp_path / "jobs/one/output/workspace"
    workspace.mkdir(parents=True)
    (workspace / "state.json").write_text("{}")
    manifest = workspace.parent / "workspace-manifest.json"
    manifest.write_bytes(runtime.json_bytes(runtime.tree_manifest(workspace)))
    checkpoint = {
        "source_release": "release",
        "binding": {"target_id": "target"},
        "workspace_relative_path": "jobs/one/output/workspace",
        "workspace_manifest_path": "jobs/one/output/workspace-manifest.json",
        "workspace_manifest_sha256": runtime.digest_file(manifest),
    }
    assert (
        runtime.verify_checkpoint(
            tmp_path, checkpoint, release="release", target_id="target"
        )
        == workspace
    )
    with pytest.raises(ValueError, match="another release or target"):
        runtime.verify_checkpoint(
            tmp_path, checkpoint, release="other", target_id="target"
        )
    (workspace / "state.json").write_text('{"tampered":true}')
    with pytest.raises(ValueError, match="workspace changed"):
        runtime.verify_checkpoint(
            tmp_path, checkpoint, release="release", target_id="target"
        )


# This deliberately small adapter is only written inside a test-owned snapshot.
# It proves continuation and host artifact plumbing, not native science gates.
FIXTURE_ADAPTER = """
import json, hashlib, shutil
from pathlib import Path
def prepare(**args):
    source=Path(__file__).resolve().parents[2]
    binding=json.loads((source.parent/'marathon-binding.json').read_text())['runs'][0]
    if binding.get('initialize'):
        binding['run_id']='controlled-run'
        count=0
    else:
        count=json.loads((source/'run-state.json').read_text())['cycle_count']
    return {'state': {'source':str(source), 'run_root':str(args['run_root']), 'binding':binding, 'initial_cycle_count':count}}
def execute(*,state,services):
    workspace=Path(state['run_root'])/'workspace'
    shutil.copytree(state['source'],workspace)
    count=state['initial_cycle_count']+1
    (workspace/'run-state.json').write_text(json.dumps({'cycle_count':count}))
    return {'workspace':str(workspace),'cycle_count':count}
def verify(*,state,execution,services):
    p=Path(state['run_root'])/'latest.json'
    p.write_text(json.dumps({'cycle_count':execution['cycle_count']}))
    desc={'path':'latest.json','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'media_type':'application/json'}
    return {'result': {'structured_value': {'cycle_count':execution['cycle_count'], 'report_artifacts': {'latest.json':desc}}, 'report_verification': {'status':'passed','scientific_truth_verified':False}}}
"""


def test_native_adapter_boundary_continues_verified_workspace_not_original_export(
    tmp_path, monkeypatch
):
    # Suppress bytecode in the source snapshot just as the production supervisor does.
    monkeypatch.setattr(sys, "dont_write_bytecode", True)
    source = tmp_path / "source"
    adapter = source / "integrations/domain_package/marathon_runtime.py"
    adapter.parent.mkdir(parents=True)
    adapter.write_text(FIXTURE_ADAPTER)
    manifest = seal(source)
    data = tmp_path / "data"
    data.mkdir()
    job = {
        "id": "one",
        "workflow_id": "discovery_marathon_loop",
        "inputs": {"target_id": "p-vs-np-target", "allow_public_network": True},
        "release": "fixture",
        "budget": BUDGET,
        "parent_checkpoint": None,
        "runtime_source_sha256": manifest["content_sha256"],
    }
    request = {
        "job": job,
        "source_root": str(source),
        "data_root": str(data),
        "output_relative_path": "jobs/one/output",
    }
    services = SimpleNamespace(public_fetch=lambda *a, **k: None, calls=0)
    first = runtime.run_native(request, services=services)
    assert first["checkpoint"]["cycle_count"] == 1
    second = runtime.run_native(
        {
            **request,
            "job": {**job, "id": "two", "parent_checkpoint": first["checkpoint"]},
            "output_relative_path": "jobs/two/output",
        },
        services=services,
    )
    assert second["checkpoint"]["cycle_count"] == 2
    assert first["checkpoint"]["cycle_count"] == 1
    assert not (source / "run-state.json").exists()
    assert second["result"]["report_verification"]["scientific_truth_verified"] is False


def test_real_native_adapter_without_provider_fails_before_scientific_work(tmp_path):
    """Load the actual native adapter in a fresh process; never call a model."""
    source = tmp_path / "source"
    adapter = source / "integrations/domain_package/marathon_runtime.py"
    adapter.parent.mkdir(parents=True)
    original = (
        Path(__file__).resolve().parents[2]
        / "integrations/domain_package/marathon_runtime.py"
    )
    adapter.write_bytes(original.read_bytes())
    manifest = seal(source)
    data = tmp_path / "data"
    data.mkdir()
    request = tmp_path / "request.json"
    response = tmp_path / "response.json"
    request.write_bytes(
        runtime.json_bytes(
            {
                "source_root": str(source),
                "data_root": str(data),
                "output_relative_path": "jobs/native/output",
                "job": {
                    "id": "native",
                    "workflow_id": "discovery_marathon_loop",
                    "release": "fixture",
                    "runtime_source_sha256": manifest["content_sha256"],
                    "parent_checkpoint": None,
                    "budget": BUDGET,
                    "inputs": {
                        "target_id": "p-vs-np-target",
                        "allow_public_network": True,
                    },
                },
            }
        )
    )
    environment = worker_environment()
    environment.pop("OPENAI_API_KEY", None)
    environment.pop("ABDUCER_MODEL", None)
    result = subprocess.run(
        Worker._command(request, response),
        env=environment,
        capture_output=True,
        timeout=20,
    )
    assert result.returncode == 1
    failure = json.loads(response.read_bytes())
    assert failure["error_type"] == "ProviderError"
    assert "Configure ABDUCER_MODEL" in failure["error"]
    assert not (data / "jobs/native/output/workspace").exists()
    assert not (data / "jobs/native/output/latest.json").exists()


def test_real_subprocess_publication_and_continuation_are_durable(
    tmp_path, monkeypatch
):
    from integrations.chatgpt import catalog

    monkeypatch.setattr(
        catalog, "Catalog", lambda root: SimpleNamespace(release="fixture")
    )
    monkeypatch.setenv("OPENAI_API_KEY", "unused-controlled-key")
    monkeypatch.setenv("ABDUCER_MODEL", "controlled-no-model-calls")
    source = tmp_path / "source"
    adapter = source / "integrations/domain_package/marathon_runtime.py"
    adapter.parent.mkdir(parents=True)
    adapter.write_text(FIXTURE_ADAPTER)
    manifest = seal(source)
    store = Store(tmp_path / "service.sqlite3")
    project, job = queued(store, runtime_hash=manifest["content_sha256"])
    worker = Worker(
        store, data_root=tmp_path / "data", source_root=source, poll_seconds=0.05
    )
    worker.run_once()
    assert store.get_job("alice", job["id"])["status"] == "succeeded"
    assert store.project("alice", project["id"])["checkpoint"]["cycle_count"] == 1
    assert store.artifacts("alice", job["id"])
    # Reopen SQLite and construct a new supervisor, as after a host restart.
    reopened = Store(tmp_path / "service.sqlite3")
    plan = reopened.prepare_plan(
        "alice",
        project["id"],
        workflow_id="discovery_marathon_loop",
        inputs={"target_id": "p-vs-np-target", "allow_public_network": True},
        budget=BUDGET,
        release="fixture",
        runtime_source_sha256=manifest["content_sha256"],
    )
    next_job = reopened.start_job(
        "alice",
        plan["plan_id"],
        "continue",
        release="fixture",
        runtime_source_sha256=manifest["content_sha256"],
    )
    Worker(
        reopened, data_root=tmp_path / "data", source_root=source, poll_seconds=0.05
    ).run_once()
    assert reopened.get_job("alice", next_job["id"])["status"] == "succeeded"
    assert reopened.project("alice", project["id"])["checkpoint"]["cycle_count"] == 2
    assert (
        reopened.get_job("alice", job["id"])["result"]["structured_value"][
            "cycle_count"
        ]
        == 1
    )


def test_cancellation_terminates_active_process_before_publication(
    tmp_path, snapshot, monkeypatch
):
    from integrations.chatgpt import catalog

    monkeypatch.setattr(
        catalog, "Catalog", lambda root: SimpleNamespace(release="fixture")
    )
    store = Store(tmp_path / "service.sqlite3")
    project, job = queued(
        store, runtime_hash=runtime.verify_snapshot(snapshot)["content_sha256"]
    )
    started = tmp_path / "started"
    errors = []

    def cancel():
        deadline = time.monotonic() + 10
        while not started.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        if not started.exists():
            errors.append("Child never started")
        store.cancel_job("alice", job["id"])

    canceller = threading.Thread(target=cancel)
    canceller.start()
    script = (
        "import pathlib,time; pathlib.Path("
        + repr(str(started))
        + ").touch(); time.sleep(60)"
    )
    worker = Worker(
        store,
        data_root=tmp_path / "data",
        source_root=snapshot,
        poll_seconds=0.05,
        command_factory=lambda *a: [sys.executable, "-c", script],
    )
    worker.run_once()
    canceller.join(timeout=12)
    assert not errors
    assert store.get_job("alice", job["id"])["status"] == "cancelled"
    assert store.project("alice", project["id"])["version"] == 0
    assert store.artifacts("alice", job["id"]) == []


@pytest.mark.parametrize("expired_at", ["child_exit", "verification", "heartbeat"])
def test_deadline_after_child_exit_or_verification_cannot_publish(
    tmp_path, monkeypatch, expired_at
):
    """Advance only the supervisor clock across expensive final boundaries.

    The child is a real process using the controlled adapter. Deterministic
    clock advancement models slow child teardown, digest verification, or a
    contended final heartbeat without making the regression sleep for minutes.
    """
    from integrations.chatgpt import catalog, worker as worker_module

    monkeypatch.setattr(
        catalog, "Catalog", lambda root: SimpleNamespace(release="fixture")
    )
    monkeypatch.setenv("OPENAI_API_KEY", "unused-controlled-key")
    monkeypatch.setenv("ABDUCER_MODEL", "controlled-no-model-calls")
    source = tmp_path / "source"
    adapter = source / "integrations/domain_package/marathon_runtime.py"
    adapter.parent.mkdir(parents=True)
    adapter.write_text(FIXTURE_ADAPTER)
    manifest = seal(source)
    store = Store(tmp_path / "service.sqlite3")
    project, job = queued(store, runtime_hash=manifest["content_sha256"])
    worker = Worker(
        store, data_root=tmp_path / "data", source_root=source, poll_seconds=0.01
    )
    elapsed = [0.0]
    verified = [False]
    monkeypatch.setattr(
        worker_module,
        "time",
        SimpleNamespace(monotonic=lambda: elapsed[0], sleep=time.sleep),
    )
    original_terminate = worker_module.terminate_group
    original_verify = worker._verify_publication
    original_heartbeat = store.heartbeat

    def terminate(process, **kwargs):
        original_terminate(process, **kwargs)
        if expired_at == "child_exit":
            elapsed[0] = BUDGET["timeout_seconds"] + 1

    def verify(*args):
        original_verify(*args)
        verified[0] = True
        if expired_at == "verification":
            elapsed[0] = BUDGET["timeout_seconds"] + 1

    def heartbeat(*args, **kwargs):
        result = original_heartbeat(*args, **kwargs)
        if verified[0] and expired_at == "heartbeat":
            elapsed[0] = BUDGET["timeout_seconds"] + 1
        return result

    monkeypatch.setattr(worker_module, "terminate_group", terminate)
    monkeypatch.setattr(worker, "_verify_publication", verify)
    monkeypatch.setattr(store, "heartbeat", heartbeat)
    worker.run_once()
    recorded = store.get_job("alice", job["id"])
    assert recorded["status"] == "failed"
    assert "deadline exceeded" in recorded["error"]
    assert store.project("alice", project["id"])["version"] == 0
    assert store.project("alice", project["id"])["checkpoint"] is None
    assert store.artifacts("alice", job["id"]) == []
