# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Owned real-process validation, quota admission, timeout and source integrity."""

import hashlib
import json
from pathlib import Path
import shutil
from types import SimpleNamespace

import pytest

from integrations.chatgpt import validation_service
from integrations.chatgpt.native_steps import CONCEPTUAL_VALIDATOR_SOURCES
from integrations.chatgpt.runtime import SOURCE_MANIFEST, json_bytes, tree_manifest
from integrations.chatgpt.store import AccessDenied, Store

ROOT = Path(__file__).resolve().parents[2]


def seal(source):
    files = tree_manifest(source, exclude_manifest=True)
    payload = {
        "version": 1,
        "revision": "explicit-validation-fixture",
        "files": files,
        "content_sha256": hashlib.sha256(json_bytes(files)).hexdigest(),
    }
    (source / SOURCE_MANIFEST).write_bytes(json_bytes(payload))
    return payload["content_sha256"]


@pytest.fixture
def service(tmp_path):
    source = tmp_path / "source"
    shutil.copytree(
        ROOT / "hooks/scripts",
        source / "hooks/scripts",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    shutil.copytree(ROOT / "registry/tasks", source / "registry/tasks")
    for relative in ["hooks/hooks.json", *CONCEPTUAL_VALIDATOR_SOURCES]:
        destination = source / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, destination)
    for relative in ("KB/test.kb.md", "agentic/state/dependency_graphs/test.json"):
        destination = source / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("Explicit immutable fixture input\n")
    data = tmp_path / "data"
    store = Store(data / "store.sqlite3")
    store.provision_user("alice", "Alice")
    store.provision_user("bob", "Bob")
    return SimpleNamespace(
        config=SimpleNamespace(repository_root=source, data_root=data),
        store=store,
        catalog=SimpleNamespace(release="fixture-catalog-release"),
        runtime_source_sha256=seal(source),
    )


def compact_recorded_map():
    """Crop recorded fixture rows without making scientific claims in tests."""
    payload = json.loads(
        (
            ROOT / "agentic/fixtures/hegelian/hypothesis_exploration_map.example.json"
        ).read_text()
    )
    schema = json.loads(
        (ROOT / "agentic/spec/hypothesis_exploration_map.schema.json").read_text()
    )
    pressure_schema = json.loads(
        (ROOT / "agentic/spec/conceptual_pressure_packet.schema.json").read_text()
    )
    candidates = []
    operations = set()
    for row in payload["mediation_candidates"]:
        if row["creative_operation"] not in operations:
            candidates.append(row)
            operations.add(row["creative_operation"])
        if len(candidates) == 4:
            break
    identities = {row["candidate_id"] for row in candidates}
    pressure_ids = {
        identity for row in candidates for identity in row["source_pressure_ids"]
    }
    payload["mediation_candidates"] = [
        {key: row[key] for key in schema["required_candidate_fields"]}
        for row in candidates
    ]
    payload["pressure_packets"] = [
        {key: row[key] for key in pressure_schema["required_fields"]}
        for row in payload["pressure_packets"]
        if row["pressure_id"] in pressure_ids
    ]
    for key, fields in (
        ("validation_packets", "required_validation_fields"),
        ("candidate_rankings", "required_ranking_fields"),
    ):
        payload[key] = [
            {name: row[name] for name in schema[fields]}
            for row in payload[key]
            if row["candidate_id"] in identities
        ]
    payload["creative_operations"] = [
        {"id": row["id"]} for row in payload["creative_operations"]
    ]
    payload["refinement_trace"] = {"cycles": ["Explicit recorded-fixture crop"]}
    payload["summary"] = {"candidate_count": 4, "route_changing_candidates": 4}
    payload["kb_path"] = "KB/test.kb.md"
    payload["source_graph"] = "agentic/state/dependency_graphs/test.json"
    payload["discovery_signals"] = []
    payload["abstraction_machinery_policy"] = {}
    payload["formal_subgoal_control_policy"] = {}
    payload = {
        key: value
        for key, value in payload.items()
        if key in schema["required_fields"]
        or key in {"kb_path", "source_graph", "refinement_trace", "summary"}
    }

    # Retain the recorded first obligation/reference in nested fields. The
    # operation tests structural validation, not the fixture's scientific case.
    def crop_nested_lists(value):
        if isinstance(value, dict):
            return {key: crop_nested_lists(item) for key, item in value.items()}
        if isinstance(value, list):
            return [crop_nested_lists(item) for item in value[:1]]
        return value

    for collection in (
        "candidate_rankings",
        "mediation_candidates",
        "validation_packets",
    ):
        for row in payload[collection]:
            for field in ("subgoal_control", "machinery_selection", "obligations"):
                if field in row:
                    row[field] = crop_nested_lists(row[field])

    def shorten_fixture(value):
        if isinstance(value, dict):
            return {key: shorten_fixture(item) for key, item in value.items()}
        if isinstance(value, list):
            return [shorten_fixture(item) for item in value]
        if isinstance(value, str) and len(value) > 50:
            if "->" in value:
                left, right = value.split("->", 1)
                return left[:20] + " -> " + right[:20]
            return value[:50]
        return value

    return json.dumps(shorten_fixture(payload), separators=(",", ":"))


def test_owned_validation_runs_original_failure_without_advancing_checkpoint(service):
    project = service.store.create_project("alice", "Validation")
    receipt = validation_service.validate_conceptual(
        service, "alice", project["id"], '{"target_id":"test"}'
    )
    assert receipt["status"] == "failed", receipt
    assert receipt["source_snapshot_sha256"] == service.runtime_source_sha256
    assert receipt["hook_receipt"]["event"] == "PreToolUse"
    assert "missing required field" in receipt["stderr"]
    assert (
        not receipt["native_workflow_executed"]
        and not receipt["scientific_truth_verified"]
    )
    assert (
        validation_service.get_validation(
            service, "alice", project["id"], receipt["receipt_id"]
        )
        == receipt
    )
    current = service.store.project("alice", project["id"])
    assert current["version"] == 0 and current["checkpoint"] is None
    directory = (
        service.config.data_root / "conceptual-validations" / receipt["receipt_id"]
    )
    assert {path.name for path in directory.iterdir()} == {"input.json", "receipt.json"}
    assert "source_root" not in json.dumps(receipt)
    assert str(service.config.data_root) not in json.dumps(receipt)


def test_valid_recorded_map_uses_only_existing_immutable_dependencies(service):
    content = compact_recorded_map()
    assert len(content) <= 48000
    project = service.store.create_project("alice", "Validation")
    receipt = validation_service.validate_conceptual(
        service, "alice", project["id"], content
    )
    assert receipt["status"] == "passed", receipt
    paths = {entry["path"] for entry in receipt["source_dependencies"]}
    assert (
        "KB/test.kb.md" in paths
        and "agentic/state/dependency_graphs/test.json" in paths
    )
    assert not any("example" in path for path in paths)


def test_no_cross_user_or_viewer_validation_or_receipt_read(service):
    project = service.store.create_project("alice", "Private validation")
    with pytest.raises(AccessDenied):
        validation_service.validate_conceptual(service, "bob", project["id"], "{}")
    service.store.grant_project("bob", project["id"], "viewer")
    with pytest.raises(AccessDenied):
        validation_service.validate_conceptual(service, "bob", project["id"], "{}")
    receipt = validation_service.validate_conceptual(
        service, "alice", project["id"], "{}"
    )
    with pytest.raises(AccessDenied):
        validation_service.get_validation(
            service, "bob", project["id"], receipt["receipt_id"]
        )


@pytest.mark.parametrize(
    "content", ["[]", '{"a":NaN}', '{"a":1,"a":2}', "x" * 48001, "{broken"]
)
def test_invalid_input_rejected_before_any_operation(service, content):
    project = service.store.create_project("alice", "Validation")
    with pytest.raises(ValueError):
        validation_service.validate_conceptual(service, "alice", project["id"], content)
    assert not (service.config.data_root / "conceptual-validations").exists()


def test_storage_and_concurrent_admission_quotas_are_enforced(service, monkeypatch):
    project = service.store.create_project("alice", "Validation")
    validation_service._reserve(service, "alice", project["id"], "1" * 32, "a" * 64)
    with pytest.raises(ValueError, match="already active"):
        validation_service.validate_conceptual(service, "alice", project["id"], "{}")
    with service.store.connection(write=True) as db:
        db.execute("UPDATE conceptual_validations SET status='failed'")
    monkeypatch.setattr(validation_service, "MAX_PROJECT_OPERATIONS", 1)
    with pytest.raises(ValueError, match="quota"):
        validation_service.validate_conceptual(service, "alice", project["id"], "{}")


def test_missing_research_reference_is_not_fabricated(service):
    project = service.store.create_project("alice", "Validation")
    receipt = validation_service.validate_conceptual(
        service, "alice", project["id"], '{"kb_path":"KB/missing.md"}'
    )
    assert receipt["status"] == "error"
    assert "absent from the verified source" in receipt["error"]
    assert not (service.config.repository_root / "KB/missing.md").exists()


def test_snapshot_drift_and_path_escape_fail_before_validator(service):
    project = service.store.create_project("alice", "Validation")
    receipt = validation_service.validate_conceptual(
        service, "alice", project["id"], '{"kb_path":"../../private"}'
    )
    assert receipt["status"] == "error"
    changed = (
        service.config.repository_root
        / "agentic/scripts/validate_hypothesis_exploration.py"
    )
    changed.write_text("raise RuntimeError('changed')")
    receipt = validation_service.validate_conceptual(
        service, "alice", project["id"], "{}"
    )
    assert receipt["status"] == "error"
    assert "source snapshot differs" in receipt["error"]


def test_process_deadline_terminates_validator_without_checkpoint(service, monkeypatch):
    project = service.store.create_project("alice", "Validation")
    # Explicit process fixture: the trusted test release deliberately sleeps.
    script = (
        service.config.repository_root
        / "agentic/scripts/validate_hypothesis_exploration.py"
    )
    script.write_text("import time\ntime.sleep(60)\n")
    service.runtime_source_sha256 = seal(service.config.repository_root)
    monkeypatch.setattr(validation_service, "OPERATION_DEADLINE_SECONDS", 2)
    receipt = validation_service.validate_conceptual(
        service, "alice", project["id"], "{}"
    )
    assert receipt["status"] == "timed_out"
    assert receipt["elapsed_seconds"] < 3
    assert service.store.project("alice", project["id"])["checkpoint"] is None


def test_child_environment_has_no_account_or_model_credentials(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-pass")
    monkeypatch.setenv("ABDUCER_NATIVE_BRIDGE_KEY", "must-not-pass")
    monkeypatch.setenv("HOME", "/private/test-home")
    environment = validation_service._environment()
    assert "OPENAI_API_KEY" not in environment
    assert "ABDUCER_NATIVE_BRIDGE_KEY" not in environment
    assert "HOME" not in environment
