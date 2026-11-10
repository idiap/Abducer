# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Admission requires a recent compatible native worker, not a configured URL."""

from pathlib import Path
import time

from integrations.chatgpt.bridge import BridgeRuntimeConfig
from integrations.chatgpt.server import Service

ROOT = Path(__file__).resolve().parents[2]


def test_native_admission_tracks_source_provider_hooks_and_liveness(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(
        "integrations.chatgpt.server.verify_snapshot",
        lambda root: {"content_sha256": "release-a"},
    )
    service = Service(
        BridgeRuntimeConfig(
            ROOT, tmp_path, worker_enabled=True, require_online_worker=True
        )
    )
    assert not service.executable
    for source, ready, hooks in [
        ("release-b", True, True),
        ("release-a", False, True),
        ("release-a", True, False),
    ]:
        service.store.record_worker(
            "worker", source, "chatgpt", provider_ready=ready, hooks_enabled=hooks
        )
        assert not service.executable
    service.store.record_worker(
        "worker", "release-a", "chatgpt", provider_ready=True, hooks_enabled=True
    )
    caps = service.capabilities()
    assert service.executable
    assert caps["executable_workflows"] == ["discovery_marathon_workflow"]
    assert caps["model_providers"] == ["chatgpt"]
    assert caps["native_hooks_enabled"] is True
    service.store.provision_user("owner", "Owner")
    project = service.store.create_project("owner", "Provider-bound research")
    plan = service.prepare(
        "owner",
        project["id"],
        "discovery_marathon_workflow",
        {"target_id": "p-vs-np-target", "allow_public_network": True},
    )
    assert plan["inputs"]["model_provider"] == "chatgpt"
    assert plan["inputs"]["native_hooks_required"] is True
    job = service.start("owner", plan["plan_id"], "native-provider-test")
    assert service.store.claim_job("unconfigured") is None
    profile = {
        "source_sha256": "release-a",
        "provider": "chatgpt",
        "provider_ready": True,
        "hooks_enabled": True,
    }
    for key, value in [
        ("source_sha256", "release-b"),
        ("provider", "api"),
        ("provider_ready", False),
        ("hooks_enabled", False),
    ]:
        assert (
            service.store.claim_job(
                "wrong-profile", capabilities={**profile, key: value}
            )
            is None
        )
        assert service.store.get_job("owner", job["job_id"])["status"] == "queued"
    assert (
        service.store.claim_job("matching", capabilities=profile)["id"] == job["job_id"]
    )
    with service.store.connection(write=True) as db:
        db.execute("UPDATE worker_presence SET seen=?", (time.time() - 46,))
    assert not service.executable
    assert "No recent worker" in service.capabilities()["execution_reason"]


def test_dependency_pages_require_identity_and_retain_manifest(tmp_path):
    service = Service(BridgeRuntimeConfig(ROOT, tmp_path))
    service.store.provision_user("owner", "Owner")
    first = service.dependencies("owner", "discovery_marathon_workflow", limit=2)
    second = service.dependencies(
        "owner", "discovery_marathon_workflow", offset=2, limit=2
    )
    assert first["total"] > 2
    assert first["next_offset"] == 2
    assert first["entries"] != second["entries"]
    assert first["manifest_sha256"] == second["manifest_sha256"]
    assert first["runtime_closure_verified"] is False
