# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Exercise the actual HTTP/MCP boundary with signed named-user credentials.

The issuer's key fetch is injected; token signing/verification, HTTP transport,
MCP dispatch, project isolation and durable job admission use production code.
No model call is made: the queued job is cancelled before any worker claims it.
"""

from contextlib import contextmanager
from pathlib import Path
import socket
import threading
import time
from types import SimpleNamespace

import pytest

# Optional dependencies gate this integration suite before production imports.
# ruff: noqa: E402
pytest.importorskip("mcp")
jwt = pytest.importorskip("jwt")
httpx = pytest.importorskip("httpx")
uvicorn = pytest.importorskip("uvicorn")
from cryptography.hazmat.primitives.asymmetric import rsa

from integrations.chatgpt.auth import JWTVerifier
from integrations.chatgpt.config import Config
from integrations.chatgpt.server import create_app
from integrations.chatgpt.store import Store
from integrations.chatgpt.runtime import build_snapshot

ROOT = Path(__file__).resolve().parents[2]


@contextmanager
def running_server(app):
    """Bind an ephemeral loopback socket before starting the ASGI server."""
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level="error", access_log=False))
    thread = threading.Thread(target=lambda: server.run(sockets=[sock]), daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 10
        while not server.started and thread.is_alive() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert server.started, "HTTP server failed to start"
        yield f"http://127.0.0.1:{port}"
    finally:
        server.should_exit = True
        thread.join(timeout=10)
        sock.close()
        assert not thread.is_alive(), "HTTP server failed to stop"


def test_signed_http_mcp_project_plan_retry_and_cancel(tmp_path):
    source = tmp_path / "source"
    build_snapshot(ROOT, source)
    config = Config(
        repository_root=source,
        data_root=tmp_path / "data",
        public_url="https://research.example.org",
        issuer="https://identity.example.org/",
        jwks_url="https://identity.example.org/keys",
        audience="https://research.example.org/mcp",
        worker_enabled=True,
    )
    store = Store(config.database)
    for subject in ("alice", "bob"):
        store.provision_user(subject, subject.title())
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    keys = SimpleNamespace(
        get_signing_key_from_jwt=lambda token: SimpleNamespace(key=key.public_key())
    )
    verifier = JWTVerifier(config, store, key_client=keys)

    def token(subject, **override):
        claims = dict(
            sub=subject,
            iss=config.issuer,
            aud=config.audience,
            iat=int(time.time()),
            exp=int(time.time()) + 300,
            scope="abducer",
        )
        claims.update(override)
        return jwt.encode(claims, key, algorithm="RS256", headers={"kid": "test"})

    with (
        running_server(create_app(config, store, verifier)) as base,
        httpx.Client(base_url=base, timeout=15) as client,
    ):
        assert client.get("/healthz").status_code == 200
        response = client.post(
            "/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
        )
        assert response.status_code == 401
        assert "resource_metadata" in response.headers["www-authenticate"]
        metadata = client.get("/.well-known/oauth-protected-resource/mcp")
        assert metadata.status_code == 200
        assert metadata.json()["resource"] == config.audience
        counter = 0

        def rpc(method, params=None, subject="alice", bearer=None):
            nonlocal counter
            counter += 1
            headers = {
                "Accept": "application/json, text/event-stream",
                "Authorization": "Bearer " + (bearer or token(subject)),
            }
            response = client.post(
                "/mcp",
                headers=headers,
                json={
                    "jsonrpc": "2.0",
                    "id": counter,
                    "method": method,
                    "params": params or {},
                },
            )
            assert response.status_code == 200, response.text
            payload = response.json()
            assert "error" not in payload, payload
            return payload["result"]

        initialized = rpc(
            "initialize",
            {
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "abducer-http-test", "version": "1"},
            },
        )
        assert initialized["serverInfo"]["name"] == "Abducer"
        names = {item["name"] for item in rpc("tools/list")["tools"]}
        assert {
            "open_explorer",
            "prepare_research_run",
            "start_research_run",
            "get_report",
        } <= names

        def call(name, arguments=None, subject="alice"):
            result = rpc(
                "tools/call", {"name": name, "arguments": arguments or {}}, subject
            )
            assert not result.get("isError"), result
            return result["structuredContent"]

        assert call("get_profile")["name"] == "Alice"
        project = call("create_project", {"name": "HTTP end-to-end project"})
        assert call("list_projects", subject="bob")["projects"] == []
        rejected = rpc(
            "tools/call",
            {"name": "list_runs", "arguments": {"project_id": project["id"]}},
            "bob",
        )
        assert rejected.get("isError") is True
        plan = call(
            "prepare_research_run",
            {
                "project_id": project["id"],
                "workflow_id": "discovery_marathon_workflow",
                "inputs": {"target_id": "p-vs-np-target", "allow_public_network": True},
                "max_output_tokens": 32000,
            },
        )
        job = call(
            "start_research_run",
            {"plan_id": plan["plan_id"], "idempotency_key": "http-e2e"},
        )
        replay = call(
            "start_research_run",
            {"plan_id": plan["plan_id"], "idempotency_key": "http-e2e"},
        )
        assert job["job_id"] == replay["job_id"]
        assert job["status"] == "queued"
        opened = call(
            "open_explorer", {"project_id": project["id"], "job_id": job["job_id"]}
        )
        assert opened["selection"]["job_id"] == job["job_id"]
        ui = rpc("resources/read", {"uri": "ui://abducer/explorer/v1.html"})
        assert ui["contents"][0]["mimeType"] == "text/html;profile=mcp-app"
        assert "ui/initialize" in ui["contents"][0]["text"]
        assert "globalThis.AbducerReports" in ui["contents"][0]["text"]
        assert "<!-- ABDUCER_REPORT_VIEWER -->" not in ui["contents"][0]["text"]
        assert call("cancel_run", {"job_id": job["job_id"]})["status"] == "cancelled"
        assert call("list_run_artifacts", {"job_id": job["job_id"]})["artifacts"] == []

        for bearer in (
            token("alice", aud="https://another.example/mcp"),
            token("unprovisioned"),
            token("alice", scope="other"),
        ):
            denied = client.post(
                "/mcp",
                headers={"Authorization": "Bearer " + bearer},
                json={"jsonrpc": "2.0", "id": 99, "method": "tools/list"},
            )
            assert denied.status_code in {401, 403}
        store.provision_user("alice", "Alice", active=False)
        denied = client.post(
            "/mcp",
            headers={"Authorization": "Bearer " + token("alice")},
            json={"jsonrpc": "2.0", "id": 100, "method": "tools/list"},
        )
        assert denied.status_code in {401, 403}
