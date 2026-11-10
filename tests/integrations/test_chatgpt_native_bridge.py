# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Exercise bridge authentication with the real native Store and Service.

No model work is executed. Real plans and jobs are admitted using a verified
source snapshot, then cancelled. Cross-language signing is checked against the
production JS client so a shared Python-only signing mistake cannot pass.
"""

from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
import hashlib
import hmac
import json
from pathlib import Path
import socket
import subprocess
import threading
import time
import uuid

import pytest

# Optional hosted dependencies are checked before production imports.
# ruff: noqa: E402
pytest.importorskip("mcp")
httpx = pytest.importorskip("httpx")
uvicorn = pytest.importorskip("uvicorn")
from starlette.testclient import TestClient

from integrations.chatgpt.bridge import (
    BRIDGE_PATH,
    BridgeConfig,
    BridgeRuntimeConfig,
    create_bridge_app,
    signing_message,
)
from integrations.chatgpt.runtime import build_snapshot
from integrations.chatgpt.server import Service
from integrations.chatgpt.chatgpt_model import ChatGPTServices

ROOT = Path(__file__).resolve().parents[2]
KEY = "12" * 32
AUDIENCE = "site-test-audience"


@pytest.fixture(scope="module")
def source(tmp_path_factory):
    destination = tmp_path_factory.mktemp("bridge-source") / "runtime"
    build_snapshot(ROOT, destination)
    return destination


@pytest.fixture
def runtime(source, tmp_path):
    service = Service(BridgeRuntimeConfig(source, tmp_path, worker_enabled=True))
    service.store.provision_user("native-alice", "Alice")
    service.store.provision_user("native-bob", "Bob")
    config = BridgeConfig(
        AUDIENCE, KEY, {"sites-alice": "native-alice", "sites-bob": "native-bob"}
    )
    return service, config


def signed(
    operation,
    arguments=None,
    *,
    principal="sites-alice",
    audience=AUDIENCE,
    key=KEY,
    timestamp=None,
    nonce=None,
):
    body = json.dumps(
        {
            "version": 1,
            "audience": audience,
            "principal": principal,
            "operation": operation,
            "arguments": arguments or {},
        },
        separators=(",", ":"),
    ).encode()
    stamp, nonce = (
        str(int(time.time()) if timestamp is None else timestamp),
        nonce or uuid.uuid4().hex,
    )
    signature = hmac.new(
        bytes.fromhex(key),
        signing_message(body, audience, stamp, nonce),
        hashlib.sha256,
    ).hexdigest()
    return body, {
        "content-type": "application/json",
        "x-abducer-timestamp": stamp,
        "x-abducer-nonce": nonce,
        "x-abducer-signature": signature,
    }


def call(client, operation, arguments=None, **kwargs):
    body, headers = signed(operation, arguments, **kwargs)
    return client.post(BRIDGE_PATH, content=body, headers=headers)


def test_signature_freshness_body_binding_and_durable_replay(runtime):
    service, config = runtime
    with TestClient(create_bridge_app(service, config)) as client:
        assert client.post(BRIDGE_PATH, json={}).status_code == 401
        for override in (
            {"key": "34" * 32},
            {"timestamp": int(time.time()) - 120},
            {"audience": "another-site"},
        ):
            assert (
                call(client, "get_execution_capabilities", **override).status_code
                == 401
            )
        body, headers = signed("get_execution_capabilities")
        assert (
            client.post(BRIDGE_PATH, content=body + b" ", headers=headers).status_code
            == 401
        )
        good = client.post(BRIDGE_PATH, content=body, headers=headers)
        assert good.status_code == 200
        assert good.json()["result"]["bridge_authenticated"] is True
    # A new ASGI instance shares the durable replay ledger, not process memory.
    with TestClient(create_bridge_app(service, config)) as restarted:
        replay = restarted.post(BRIDGE_PATH, content=body, headers=headers)
        assert replay.status_code == 409
        assert replay.json()["error"]["code"] == "replayed_request"


def test_provisioned_identity_and_project_binding_isolation(runtime):
    service, config = runtime
    with TestClient(create_bridge_app(service, config)) as client:
        assert (
            call(client, "get_execution_capabilities", principal="unknown").status_code
            == 403
        )
        forged = call(
            client,
            "bind_project",
            {
                "project_id": "same-sites-id",
                "title": "Research",
                "subject": "native-bob",
            },
        )
        assert forged.status_code == 400
        args = {"project_id": "same-sites-id", "title": "Research"}
        alice = call(client, "bind_project", args).json()["result"]["native_project_id"]
        retry = call(client, "bind_project", args).json()["result"]["native_project_id"]
        bob = call(client, "bind_project", args, principal="sites-bob").json()[
            "result"
        ]["native_project_id"]
        assert alice == retry and alice != bob
        assert len(service.store.list_projects("native-alice")) == 1
        assert len(service.store.list_projects("native-bob")) == 1
        service.store.provision_user("native-alice", "Alice", active=False)
        assert call(client, "get_execution_capabilities").status_code == 403


def test_real_plan_start_idempotency_access_and_cancel(runtime):
    service, config = runtime
    with TestClient(create_bridge_app(service, config)) as client:
        prepared = call(
            client,
            "prepare_research_run",
            {
                "project_id": "sites-project-1",
                "title": "Bounded research",
                "workflow_id": "discovery_marathon_workflow",
                "inputs": {"target_id": "p-vs-np-target", "allow_public_network": True},
            },
        )
        assert prepared.status_code == 200, prepared.text
        plan = prepared.json()["result"]
        assert "parent_checkpoint" not in plan
        assert (
            call(
                client,
                "start_research_run",
                {"plan_id": plan["plan_id"], "idempotency_key": "same-start"},
                principal="sites-bob",
            ).status_code
            == 403
        )
        args = {"plan_id": plan["plan_id"], "idempotency_key": "same-start"}
        started = call(client, "start_research_run", args)
        assert started.status_code == 200, started.text
        job = started.json()["result"]
        again = call(client, "start_research_run", args).json()["result"]
        assert again["job_id"] == job["job_id"]
        for operation in ("get_run_status", "list_run_artifacts", "cancel_run"):
            assert (
                call(
                    client, operation, {"job_id": job["job_id"]}, principal="sites-bob"
                ).status_code
                == 403
            )
        assert (
            call(client, "cancel_run", {"job_id": job["job_id"]}).json()["result"][
                "status"
            ]
            == "cancelled"
        )
        listing = call(
            client,
            "list_runs",
            {"project_id": "sites-project-1", "title": "Bounded research"},
        ).json()["result"]["runs"]
        assert len(listing) == 1 and listing[0]["job_id"] == job["job_id"]
        assert "payload" not in listing[0] and "parent_checkpoint" not in listing[0]


def test_bounds_and_browser_requests_fail_before_dispatch(runtime):
    service, config = runtime
    with TestClient(create_bridge_app(service, config)) as client:
        raw, headers = signed("get_execution_capabilities")
        headers["origin"] = "https://abducer.example"
        assert client.post(BRIDGE_PATH, content=raw, headers=headers).status_code == 403
        assert (
            client.post(
                BRIDGE_PATH,
                content=b"x" * (1024 * 1024 + 1),
                headers={"content-type": "application/json"},
            ).status_code
            == 413
        )
        assert call(client, "__dict__").status_code == 400
        assert (
            call(
                client, "get_execution_capabilities", {"subject": "native-bob"}
            ).status_code
            == 400
        )
        service.capabilities = lambda: {"oversized": "x" * 524288}
        assert call(client, "get_execution_capabilities").status_code == 502


def test_disabled_worker_remains_unavailable(source, tmp_path):
    service = Service(BridgeRuntimeConfig(source, tmp_path, worker_enabled=False))
    service.store.provision_user("alice", "Alice")
    with TestClient(
        create_bridge_app(
            service, BridgeConfig(AUDIENCE, KEY, {"sites-alice": "alice"})
        )
    ) as client:
        capabilities = call(client, "get_execution_capabilities").json()["result"]
        assert capabilities["executable_workflows"] == []
        assert capabilities["bridge_authenticated"] is True


def test_dependency_sources_from_real_runtime_snapshot(runtime):
    service, config = runtime
    with TestClient(create_bridge_app(service, config)) as client:
        workflow = "conceptual_hypothesis_exploration_workflow"
        dependencies = call(
            client, "get_workflow_dependencies", {"workflow_id": workflow, "limit": 1}
        )
        assert dependencies.status_code == 200, dependencies.text
        entry = dependencies.json()["result"]["entries"][0]
        source = call(
            client,
            "get_workflow_dependency_source",
            {"workflow_id": workflow, "path": entry["path"], "limit": 17},
        )
        assert source.status_code == 200, source.text
        assert (
            call(
                client,
                "get_workflow_dependency_source",
                {"workflow_id": workflow, "path": ".env"},
            ).status_code
            == 400
        )


def test_real_conceptual_validator_bridge(runtime):
    service, config = runtime
    with TestClient(create_bridge_app(service, config)) as client:
        receipt = call(
            client,
            "validate_hypothesis_map",
            {
                "project_id": "conceptual-sites-project",
                "title": "Conceptual validation",
                "content": '{"target_id":"test"}',
            },
        )
        assert receipt.status_code == 200, receipt.text
        result = receipt.json()["result"]
        assert result["status"] == "failed"
        assert result["hook_receipt"]["event"] == "PreToolUse"
        assert result["native_workflow_executed"] is False
        assert result["scientific_truth_verified"] is False
        assert service.store.list_projects("native-alice")[0]["version"] == 0
        arguments = {
            "project_id": "conceptual-sites-project",
            "title": "Conceptual validation",
            "receipt_id": result["receipt_id"],
        }
        recovered = call(client, "get_validation_receipt", arguments)
        assert recovered.status_code == 200, recovered.text
        assert recovered.json()["result"] == result
        listing_arguments = {
            "project_id": "conceptual-sites-project",
            "title": "Conceptual validation",
        }
        listing = call(client, "list_validation_receipts", listing_arguments)
        assert listing.status_code == 200, listing.text
        summaries = listing.json()["result"]["receipts"]
        assert len(summaries) == 1
        assert set(summaries[0]) == {
            "receipt_id",
            "status",
            "created",
            "artifact_sha256",
        }
        assert summaries[0]["receipt_id"] == result["receipt_id"]
        assert summaries[0]["artifact_sha256"] == result["artifact_sha256"]
        assert (
            call(
                client,
                "list_validation_receipts",
                listing_arguments,
                principal="sites-bob",
            ).json()["result"]["receipts"]
            == []
        )
        for invalid_limit in (0, 51, True):
            assert (
                call(
                    client,
                    "list_validation_receipts",
                    {**listing_arguments, "limit": invalid_limit},
                ).status_code
                == 400
            )
        assert (
            call(
                client,
                "get_validation_receipt",
                arguments,
                principal="sites-bob",
            ).status_code
            == 403
        )
        assert (
            call(
                client,
                "get_validation_receipt",
                {**arguments, "project_id": "different-project"},
            ).status_code
            == 403
        )


def test_model_rendezvous_through_signed_bridge_and_large_response(runtime):
    service, config = runtime
    project = service.store.create_project("native-alice", "Rendezvous")
    plan = service.store.prepare_plan(
        "native-alice",
        project["id"],
        workflow_id="test-native",
        inputs={},
        budget={
            "timeout_seconds": 30,
            "max_model_calls": 1,
            "max_output_tokens": 32000,
        },
        release="fixture",
        runtime_source_sha256="fixture",
    )
    started = service.store.start_job(
        "native-alice",
        plan["plan_id"],
        "rendezvous",
        release="fixture",
        runtime_source_sha256="fixture",
    )
    job = service.store.claim_job("model-worker")
    assert started["id"] == job["id"]
    provider = ChatGPTServices(
        job["budget"],
        store=service.store,
        job_id=job["id"],
        worker_id="model-worker",
        poll_seconds=0.01,
    )
    schema = {
        "type": "json_schema",
        "json_schema": {
            "schema": {
                "type": "object",
                "properties": {"answer": {"type": "string"}},
                "required": ["answer"],
                "additionalProperties": False,
            }
        },
    }
    with (
        TestClient(create_bridge_app(service, config)) as client,
        ThreadPoolExecutor(max_workers=1) as executor,
    ):
        future = executor.submit(
            provider.completion,
            messages=[{"role": "user", "content": "A controlled prompt."}],
            response_format=schema,
            max_tokens=32000,
        )
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            status = call(client, "get_run_status", {"job_id": job["id"]}).json()[
                "result"
            ]
            if status["model_handoff_waiting"]:
                break
            time.sleep(0.01)
        assert status["model_handoff_waiting"] is True
        request = call(
            client, "get_pending_model_request", {"job_id": job["id"]}
        ).json()["result"]
        assert (
            request["pending"]
            and json.loads(request["content"])["response_format"] == schema
        )
        assert (
            call(
                client,
                "get_pending_model_request",
                {"job_id": job["id"]},
                principal="sites-bob",
            ).status_code
            == 403
        )
        args = {
            "job_id": job["id"],
            "request_id": request["request_id"],
            "content": '{"answer":7}',
        }
        assert call(client, "submit_model_response", args).status_code == 400
        args["content"] = json.dumps({"answer": "x" * 70000})
        accepted = call(client, "submit_model_response", args)
        assert accepted.status_code == 200, accepted.text
        assert accepted.json()["result"]["token_usage_observed"] is False
        assert (
            future.result(timeout=3)["choices"][0]["message"]["content"]
            == args["content"]
        )
        oversized = call(
            client, "get_execution_capabilities", {"unexpected": "x" * 70000}
        )
        assert oversized.status_code == 413


@contextmanager
def serving(app):
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    server = uvicorn.Server(uvicorn.Config(app, log_level="error", access_log=False))
    thread = threading.Thread(target=lambda: server.run(sockets=[sock]), daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 10
        while not server.started and thread.is_alive() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert server.started
        yield f"http://127.0.0.1:{sock.getsockname()[1]}"
    finally:
        server.should_exit = True
        thread.join(timeout=10)
        sock.close()
        assert not thread.is_alive()


def test_actual_javascript_signer_calls_real_python_service(runtime):
    service, config = runtime
    with serving(create_bridge_app(service, config)) as url:
        result = subprocess.run(
            ["node", str(ROOT / "tests/infrastructure/chatgpt_native_bridge.mjs"), url],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=40,
        )
    assert result.returncode == 0, result.stdout + result.stderr
    assert '"python_bridge":true' in result.stdout
