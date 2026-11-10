# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Native admission never follows catalog visibility or untrusted asset paths."""

import hashlib
from pathlib import Path

import pytest

from integrations.chatgpt.execution_registry import ExecutionRegistry

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def registry():
    return ExecutionRegistry(ROOT)


def test_every_contract_is_visible_but_only_explicit_adapter_is_admitted(registry):
    rows = registry.list()["workflows"]
    assert len(rows) == 34
    assert {row["workflow_id"] for row in rows} == set(registry.catalog.native.by_id)
    assert not any(row["native_execution"] for row in rows)
    enabled = registry.list(runtime_enabled=True)["workflows"]
    assert [row["workflow_id"] for row in enabled if row["native_execution"]] == [
        "discovery_marathon_workflow"
    ]
    assert (
        registry.require_native("discovery_marathon_loop")["adapter_module"]
        == "integrations/domain_package/marathon_runtime.py"
    )
    for identity in (
        "cohere-fast",
        "conceptual_hypothesis_exploration_loop",
        "kb-orchestrator",
    ):
        with pytest.raises(ValueError, match="no qualified native adapter"):
            registry.require_native(identity)
    with pytest.raises(ValueError, match="Unknown canonical workflow"):
        registry.require_native("../../arbitrary-command")


def test_known_agent_driven_workflows_name_real_entrypoints(registry):
    conceptual = registry.get("conceptual_hypothesis_exploration_loop")
    cohere = registry.get("cohere-fast")
    assert (
        conceptual["execution_status"] == cohere["execution_status"] == "agent-driven"
    )
    assert "validate_hypothesis_map" in conceptual["bounded_operations"]
    assert "run_cohere_fast_authored_packets" in cohere["bounded_operations"]
    for descriptor in (conceptual, cohere):
        for entrypoint in descriptor["entrypoints"]:
            assert (ROOT / entrypoint["path"]).is_file()
    assert not cohere["adapter_available"]


def test_dependency_manifest_retains_templates_hooks_and_static_imports(registry):
    manifest = registry.dependency_manifest("discovery_marathon_loop")
    entries = {entry["path"]: entry for entry in manifest["entries"]}
    for path in (
        "skills/reasoning/kb-abduce/references/prompt-template.md",
        "hooks/hooks.json",
        "hooks/scripts/hook_utils.py",
        "hooks/scripts/pre_skill_use_policy.py",
        "integrations/domain_package/marathon_runtime.py",
        "registry/tasks/discovery-marathon/task_registry.json",
    ):
        assert path in entries
        assert (
            entries[path]["sha256"]
            == hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        )
    assert manifest["declared_sources_complete"]
    assert not manifest["runtime_closure_verified"]
    assert not any(
        entry.startswith(("agentic/runs/", "artifacts/", ".env")) for entry in entries
    )


def test_relocated_skill_references_are_explicit_not_silently_dropped(registry):
    manifest = registry.dependency_manifest("conceptual_hypothesis_exploration_loop")
    resolution = next(
        value
        for value in manifest["resolved_references"]
        if value["from"] == "skills/orchestration/kb-discovery-cycle/SKILL.md"
    )
    assert resolution == {
        "from": "skills/orchestration/kb-discovery-cycle/SKILL.md",
        "to": "skills/discovery/kb-discovery-cycle/SKILL.md",
        "authority": "canonical_skill_registry",
    }
    assert manifest["declared_sources_complete"]


def test_asset_pages_reconstruct_exact_source_and_reject_unlisted_files(registry):
    path = "hooks/scripts/pre_skill_use_policy.py"
    offset, parts = 0, []
    while True:
        page = registry.read_dependency(
            "discovery_marathon_loop", path, offset=offset, limit=29
        )
        parts.append(page["content"])
        if page["next_offset"] is None:
            break
        offset = page["next_offset"]
    assert "".join(parts) == (ROOT / path).read_text()
    for forbidden in (
        ".env",
        "hooks/scripts/../../../../secret",
        str(ROOT / path),
        "agentic/runs/private.json",
    ):
        with pytest.raises(ValueError, match="not declared"):
            registry.read_dependency("discovery_marathon_loop", forbidden)
    with pytest.raises(ValueError, match="page"):
        registry.read_dependency("discovery_marathon_loop", path, offset=True)
    with pytest.raises(ValueError, match="exceeds"):
        registry.read_dependency("discovery_marathon_loop", path, offset=10**9)


def test_manifest_result_is_not_a_mutable_admission_backdoor(registry):
    returned = registry.dependency_manifest("cohere-fast")
    digest = returned["manifest_sha256"]
    returned["entries"].append({"path": "private.json"})
    assert registry.dependency_manifest("cohere-fast")["manifest_sha256"] == digest
    with pytest.raises(ValueError, match="not declared"):
        registry.read_dependency("cohere-fast", "private.json")


def test_reference_escape_is_rejected(registry):
    with pytest.raises(ValueError, match="escapes"):
        registry._source_path("../../../../outside.py", "skills/example/SKILL.md")
