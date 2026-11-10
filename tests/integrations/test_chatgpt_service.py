# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Hosted boundary regressions: identity, durable admission and publication.

Optional HTTP dependencies are installed with ``uv sync --group chatgpt``.
Default local-plugin installations retain their original dependency footprint.
"""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
import hashlib
from pathlib import Path
import time
from types import SimpleNamespace

import pytest

# Optional integration dependencies intentionally gate the imports below.
# ruff: noqa: E402

pytest.importorskip("mcp")
jwt = pytest.importorskip("jwt")
from cryptography.hazmat.primitives.asymmetric import rsa
from starlette.testclient import TestClient

from integrations.chatgpt.auth import JWTVerifier
from integrations.chatgpt.config import Config
from integrations.chatgpt.store import Store, AccessDenied
from integrations.chatgpt.catalog import Catalog, CONTRACT_ID
from integrations.chatgpt.server import Service, create_app, create_server

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def store(tmp_path):
    result = Store(tmp_path / "service.sqlite3")
    result.provision_user("alice", "Alice")
    result.provision_user("bob", "Bob")
    return result


@pytest.fixture
def config(tmp_path):
    return Config(
        ROOT,
        tmp_path,
        "https://abducer.example",
        "https://identity.example/",
        "https://identity.example/jwks",
        "https://abducer.example/mcp",
        worker_enabled=True,
    )


def plan(store, subject="alice", project=None):
    project = project or store.create_project(subject, "Research")["id"]
    return store.prepare_plan(
        subject,
        project,
        workflow_id="discovery_marathon_loop",
        inputs={"target_id": "p-vs-np-target", "allow_public_network": True},
        budget={
            "timeout_seconds": 7200,
            "max_model_calls": 50,
            "max_output_tokens": 32000,
        },
        release="r1",
    )


def test_named_accounts_and_project_membership_are_required(store):
    with pytest.raises(AccessDenied):
        store.create_project("unprovisioned", "Research")
    project = store.create_project("alice", "Private")
    assert store.list_projects("bob") == []
    with pytest.raises(AccessDenied):
        store.project("bob", project["id"])
    store.grant_project("bob", project["id"], "viewer")
    assert store.project("bob", project["id"])["role"] == "viewer"
    with pytest.raises(AccessDenied):
        plan(store, "bob", project["id"])
    store.provision_user("alice", "Alice", active=False)
    with pytest.raises(AccessDenied):
        store.project("alice", project["id"])


def test_start_is_atomic_idempotent_and_project_exclusive(store):
    prepared = plan(store)
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(
            pool.map(
                lambda _: store.start_job(
                    "alice", prepared["plan_id"], "same-key", release="r1"
                ),
                range(8),
            )
        )
    assert len({row["job_id"] for row in results}) == 1
    other = plan(store, project=prepared["project_id"])
    with pytest.raises(ValueError, match="another plan"):
        store.start_job("alice", other["plan_id"], "same-key", release="r1")
    with pytest.raises(ValueError, match="active research"):
        store.start_job("alice", other["plan_id"], "new-key", release="r1")
    with pytest.raises(AccessDenied):
        store.get_job("bob", results[0]["job_id"])


def test_expired_or_release_stale_plans_do_not_enqueue(store):
    prepared = plan(store)
    with pytest.raises(ValueError, match="stale"):
        store.start_job("alice", prepared["plan_id"], "key", release="r2")
    with store.connection(write=True) as db:
        db.execute("UPDATE plans SET expires=0")
    with pytest.raises(ValueError, match="expired"):
        store.start_job("alice", prepared["plan_id"], "key", release="r1")
    assert store.claim_job("worker") is None


def test_only_lease_owner_can_publish_and_old_plans_become_stale(store):
    prepared = plan(store)
    stale = plan(store, project=prepared["project_id"])
    job = store.start_job("alice", prepared["plan_id"], "key", release="r1")
    assert store.claim_job("worker")["id"] == job["id"]
    with pytest.raises(ValueError, match="lease"):
        store.finish_job(job["id"], "other", {}, [], {})
    checkpoint = {
        "binding": {"target_id": "p-vs-np-target"},
        "workspace_relative_path": "jobs/checkpoint",
    }
    store.finish_job(
        job["id"], "worker", {"scientific_truth_verified": False}, [], checkpoint
    )
    assert store.project("alice", prepared["project_id"])["version"] == 1
    assert (
        plan(store, project=prepared["project_id"])["parent_checkpoint"] == checkpoint
    )
    with pytest.raises(ValueError, match="stale"):
        store.start_job("alice", stale["plan_id"], "stale", release="r1")


@pytest.mark.parametrize("clock", [(101.0,), (99.0, 101.0)])
def test_deadline_expiry_inside_publication_transaction_rolls_back(
    store, monkeypatch, clock
):
    prepared = plan(store)
    job = store.start_job("alice", prepared["plan_id"], "deadline", release="r1")
    store.claim_job("worker")
    ticks = iter(clock)
    monkeypatch.setattr(
        "integrations.chatgpt.store.time.monotonic", lambda: next(ticks)
    )
    with pytest.raises(TimeoutError, match="deadline"):
        store.finish_job(
            job["id"],
            "worker",
            {},
            [{"id": "candidate"}],
            {"candidate": True},
            deadline_monotonic=100,
        )
    assert store.project("alice", prepared["project_id"])["version"] == 0
    assert store.artifacts("alice", job["id"]) == []
    assert store.get_job("alice", job["id"])["status"] == "running"


def test_cancel_does_not_publish_or_advance_checkpoint(store):
    prepared = plan(store)
    job = store.start_job("alice", prepared["plan_id"], "key", release="r1")
    store.claim_job("worker")
    assert store.cancel_job("alice", job["id"])["status"] == "running"
    assert not store.heartbeat(job["id"], "worker")
    store.finish_job(
        job["id"], "worker", {"bad": "result"}, [{"id": "bad"}], {"bad": "checkpoint"}
    )
    assert store.get_job("alice", job["id"])["status"] == "cancelled"
    assert store.project("alice", prepared["project_id"])["version"] == 0
    assert store.artifacts("alice", job["id"]) == []


def test_crash_expiration_does_not_respawn_model_work(store):
    prepared = plan(store)
    job = store.start_job("alice", prepared["plan_id"], "key", release="r1")
    store.claim_job("worker", lease_seconds=-1)
    assert store.claim_job("replacement") is None
    assert store.get_job("alice", job["id"])["status"] == "failed"
    with pytest.raises(ValueError):
        store.finish_job(job["id"], "worker", {}, [], {})


def test_revoked_account_cannot_continue_worker_or_publish(store):
    prepared = plan(store)
    job = store.start_job("alice", prepared["plan_id"], "key", release="r1")
    store.claim_job("worker")
    store.provision_user("alice", "Alice", active=False)
    assert not store.heartbeat(job["id"], "worker")
    assert store.cancellation_requested(job["id"], "worker")
    store.fail_job(job["id"], "worker", "cancelled")
    with store.connection() as db:
        assert db.execute("SELECT status FROM jobs").fetchone()[0] == "cancelled"


def test_job_budget_limit_survives_store_reopen(store):
    first, second = plan(store), plan(store)
    store.start_job("alice", first["plan_id"], "first", release="r1", max_active_jobs=1)
    reopened = Store(store.path)
    with pytest.raises(ValueError, match="limit"):
        reopened.start_job(
            "alice", second["plan_id"], "second", release="r1", max_active_jobs=1
        )


@pytest.fixture
def signer():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return key


def token(signer, **overrides):
    claims = {
        "sub": "alice",
        "iss": "https://identity.example/",
        "aud": "https://abducer.example/mcp",
        "iat": int(time.time()),
        "exp": int(time.time()) + 300,
        "scope": "abducer",
        **overrides,
    }
    return jwt.encode(claims, signer, algorithm="RS256", headers={"kid": "test"})


def test_jwt_verifier_checks_signature_issuer_audience_scope_and_provisioning(
    config, store, signer
):
    keys = SimpleNamespace(
        get_signing_key_from_jwt=lambda _: SimpleNamespace(key=signer.public_key())
    )
    verifier = JWTVerifier(config, store, keys)
    verified = asyncio.run(verifier.verify_token(token(signer)))
    assert verified.subject == "alice" and verified.resource == config.audience
    for changes in (
        {"aud": "other"},
        {"iss": "other"},
        {"scope": "other"},
        {"sub": "unknown"},
        {"exp": 1},
    ):
        assert asyncio.run(verifier.verify_token(token(signer, **changes))) is None
    attacker = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    assert asyncio.run(verifier.verify_token(token(attacker))) is None
    assert (
        asyncio.run(
            verifier.verify_token(
                jwt.encode(
                    {"sub": "alice"},
                    "a-test-key-that-is-long-enough-32-chars",
                    algorithm="HS256",
                )
            )
        )
        is None
    )
    store.provision_user("alice", "Alice", active=False)
    assert asyncio.run(verifier.verify_token(token(signer))) is None


def test_config_fails_closed_and_enforces_resource_audience(config):
    from dataclasses import replace

    with pytest.raises(ValueError, match="HTTPS"):
        replace(config, issuer="http://identity.example")
    with pytest.raises(ValueError, match="audience"):
        replace(config, audience="https://other.example")


def test_every_tool_declares_structured_output_for_explorer(config, store):
    server = create_server(config, store)
    tools = asyncio.run(server.list_tools())
    assert len(tools) >= 16
    assert all(
        tool.outputSchema and tool.outputSchema["type"] == "object" for tool in tools
    )


def test_catalog_reuses_all_canonical_inventories_without_claiming_execution():
    catalog = Catalog(ROOT)
    assert len(catalog.skills) == 221
    assert len(catalog.native.rows) == 34
    assert len(catalog.viewers) == 19
    assert all(
        row["execution_status"] == "inspectable"
        for row in catalog.list_workflows()["workflows"]
    )
    source = catalog.get_skill("kb-orchestrator")
    assert (
        hashlib.sha256(source["instructions"].encode()).hexdigest() == source["sha256"]
    )
    assert (
        catalog.get_workflow(CONTRACT_ID)["viewer"]["id"] == "discovery_marathon_loop"
    )


def test_http_requires_identity_and_advertises_oauth_resource_metadata(
    config, store, signer
):
    keys = SimpleNamespace(
        get_signing_key_from_jwt=lambda _: SimpleNamespace(key=signer.public_key())
    )
    app = create_app(config, store, JWTVerifier(config, store, keys))
    with TestClient(app, base_url=config.public_url) as client:
        denied = client.post(
            "/mcp",
            json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        )
        assert denied.status_code == 401
        assert "resource_metadata=" in denied.headers["www-authenticate"]
        metadata = client.get("/.well-known/oauth-protected-resource/mcp").json()
        assert metadata["resource"] == config.audience
        assert metadata["authorization_servers"] == [config.issuer]
        assert client.get("/healthz").status_code == 200
        headers = {
            "Authorization": "Bearer " + token(signer),
            "Accept": "application/json, text/event-stream",
        }
        initialized = client.post(
            "/mcp",
            headers=headers,
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-11-25",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "1"},
                },
            },
        )
        assert initialized.status_code == 200
        assert initialized.json()["result"]["serverInfo"]["name"] == "Abducer"


@pytest.mark.parametrize("report_bytes", [13, 40 * 1024 * 1024])
def test_service_preserves_budgets_and_authorized_report_digests(
    config, store, monkeypatch, report_bytes
):
    monkeypatch.setattr(
        "integrations.chatgpt.server.verify_snapshot",
        lambda root: {"content_sha256": "fixture-runtime"},
    )
    service = Service(config, store)
    project = store.create_project("alice", "Research")["id"]
    with pytest.raises(ValueError, match="32000"):
        service.prepare(
            "alice",
            project,
            CONTRACT_ID,
            {"target_id": "p-vs-np-target", "allow_public_network": True},
            max_output_tokens=100,
        )
    prepared = service.prepare(
        "alice",
        project,
        CONTRACT_ID,
        {"target_id": "p-vs-np-target", "allow_public_network": True},
    )
    job = service.start("alice", prepared["plan_id"], "once")
    assert "parent_checkpoint" not in prepared
    store.claim_job("worker")
    path = config.data_root / "report.md"
    path.write_text("actual report" + " " * (report_bytes - 13))
    artifact = {
        "id": "report",
        "name": "report.md",
        "media_type": "text/markdown",
        "relative_path": "report.md",
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "size": path.stat().st_size,
    }
    store.finish_job(
        job["job_id"], "worker", {"scientific_truth_verified": False}, [artifact]
    )
    first = service.report("alice", job["job_id"], "report")
    assert first["text"].rstrip() == "actual report"
    assert first["total_characters"] == report_bytes
    assert first["next_offset"] == (20000 if report_bytes > 20000 else None)
    with pytest.raises(AccessDenied):
        service.report("bob", job["job_id"], "report")
    assert (
        "relative_path" not in service.artifacts("alice", job["job_id"])["artifacts"][0]
    )
    path.write_text("changed")
    with pytest.raises(ValueError, match="digest"):
        service.report("alice", job["job_id"], "report")
    # A larger sparse file must be refused before any unbounded read occurs.
    with path.open("wb") as handle:
        handle.truncate(64 * 1024 * 1024 + 1)
    with pytest.raises(ValueError, match="bounded report"):
        service.report("alice", job["job_id"], "report")
