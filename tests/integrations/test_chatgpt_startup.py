# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Startup must preload real sources without running scientific workflows."""

import importlib.metadata
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from integrations.chatgpt.execution_registry import ExecutionRegistry
from integrations.chatgpt import startup
from integrations.chatgpt.startup import preload, preload_packages
from integrations.chatgpt.setup_runtime import install
from integrations.chatgpt.generate_plugin import outputs

ROOT = Path(__file__).resolve().parents[2]


def test_cold_start_loads_all_canonical_sources_and_warm_reads_use_cache(monkeypatch):
    registry = ExecutionRegistry(ROOT)
    result = preload(registry)
    assert result["status"] == "ready"
    assert (result["skills"], result["workflows"], result["graphs"]) == (221, 34, 19)
    assert result["source_files"] >= 1200
    assert result["packages"]["loaded"] == 12
    assert result["packages"]["complete_closure_verified"]
    assert result["packages"]["verified_count"] >= 51
    assert not result["scientific_execution_started"]
    assert not result["all_workflows_executable"]
    assert set(registry._manifests) == set(registry.catalog.native.by_id)

    def unexpected(*args, **kwargs):
        raise AssertionError("Warm source lookup attempted a filesystem read")

    monkeypatch.setattr(Path, "read_bytes", unexpected)
    monkeypatch.setattr(Path, "read_text", unexpected)
    for row in registry.catalog.native.rows:
        assert registry.dependency_manifest(row["id"])["declared_sources_complete"]


def test_missing_or_unlocked_package_is_explicit(monkeypatch):
    version = importlib.metadata.version

    def missing(name):
        if name == "scipy":
            raise importlib.metadata.PackageNotFoundError(name)
        return version(name)

    monkeypatch.setattr(importlib.metadata, "version", missing)
    result = preload_packages(ROOT)
    assert result["status"] == "blocked"
    assert result["issues"] == [
        {"dependency": "scipy", "reason": "PackageNotFoundError"}
    ]
    monkeypatch.setattr(
        importlib.metadata,
        "version",
        lambda name: "999.0" if name == "scipy" else version(name),
    )
    assert preload_packages(ROOT)["issues"] == [
        {"dependency": "scipy", "reason": "ValueError"}
    ]


@pytest.fixture
def dependency_environment(tmp_path, monkeypatch):
    """A package graph with optional features and platform/Python partitions."""
    root = tmp_path / "source"
    root.mkdir()
    (root / "pyproject.toml").write_text(
        '[project]\nrequires-python = ">=3.11"\n'
        'dependencies = ["app-lib[feature]>=1"]\n'
        "[dependency-groups]\nchatgpt = []\n"
    )
    (root / "uv.lock").write_text(
        '[[package]]\nname="app-lib"\nversion="1.0"\n'
        '[[package]]\nname="common"\nversion="1.0"\n'
        "resolution-markers=[\"python_version >= '3.12'\"]\n"
        '[[package]]\nname="common"\nversion="2.0"\n'
        "resolution-markers=[\"python_version < '3.12'\"]\n"
        '[[package]]\nname="feature-dep"\nversion="2.0"\n'
        '[[package]]\nname="baseline"\nversion="1.0"\n'
        '[[package]]\nname="late-extra"\nversion="1.0"\n'
    )

    def distribution(name, version, requires):
        return SimpleNamespace(
            version=version,
            requires=requires,
            metadata={"Name": name, "Requires-Python": ">=3.11"},
        )

    installed = {
        "app-lib": distribution(
            "app-lib",
            "1.0",
            [
                "common>=1",
                "feature-dep>=2; extra == 'feature'",
                "baseline; extra != 'feature'",
                "windows-only>=1; sys_platform == 'win32'",
                "future>=1; python_version >= '3.14'",
                "backport>=1; python_version < '3.12'",
            ],
        ),
        "common": distribution("common", "1.0", ["late-extra; extra == 'addon'"]),
        "feature-dep": distribution("feature-dep", "2.0", ["common[addon]<2"]),
        "baseline": distribution("baseline", "1.0", []),
        "late-extra": distribution("late-extra", "1.0", []),
    }

    def lookup(name):
        try:
            return installed[startup.canonicalize_name(name)]
        except KeyError:
            raise importlib.metadata.PackageNotFoundError(name) from None

    marker_environment = startup.default_environment()
    monkeypatch.setattr(
        startup,
        "default_environment",
        lambda: {
            **marker_environment,
            "sys_platform": "linux",
            "python_full_version": "3.13.13",
            "python_version": "3.13",
        },
    )
    monkeypatch.setattr(startup.platform, "python_version", lambda: "3.13.13")
    monkeypatch.setattr(importlib.metadata, "distribution", lookup)
    monkeypatch.setattr(
        importlib.metadata, "version", lambda name: lookup(name).version
    )
    monkeypatch.setattr(
        importlib.metadata, "distributions", lambda: iter(installed.values())
    )
    monkeypatch.setitem(startup.MODULES, "app-lib", "fixture_app")
    original_import = importlib.import_module
    monkeypatch.setattr(
        importlib,
        "import_module",
        lambda name: (
            SimpleNamespace() if name == "fixture_app" else original_import(name)
        ),
    )
    receipt = tmp_path / "abducer-setup.json"
    monkeypatch.setattr(startup, "_receipt_path", lambda: receipt)
    return root, installed, receipt


def test_closure_selects_extras_platform_and_python_markers(dependency_environment):
    root, installed, _ = dependency_environment
    result = preload_packages(root)
    assert result["status"] == "ready"
    assert result["complete_closure_verified"]
    assert result["verified_count"] == 5
    assert result["loaded"] == 1
    assert {p["name"] for p in result["runtime_packages"]} == set(installed)
    # Activating features never removes a base dependency, and a later request
    # for another package's extra must expand that package again.
    assert {"baseline", "late-extra"} <= {p["name"] for p in result["runtime_packages"]}
    assert result["receipt"]["status"] == "absent"


def test_missing_transitive_package_blocks_ready_direct_import(dependency_environment):
    root, installed, _ = dependency_environment
    installed.pop("common")
    result = preload_packages(root)
    assert result["loaded"] == 1
    assert result["status"] == "blocked"
    assert not result["complete_closure_verified"]
    assert result["issues"] == [
        {"dependency": "common", "reason": "PackageNotFoundError"}
    ]


def test_wrong_platform_lock_version_and_unsatisfied_requires_dist(
    dependency_environment,
):
    root, installed, _ = dependency_environment
    installed["common"].version = "2.0"
    result = preload_packages(root)
    assert result["status"] == "blocked"
    assert result["issues"] == [{"dependency": "common", "reason": "ValueError"}]
    # A version may be locked for this platform but violate a parent's minimum.
    installed["common"].version = "1.0"
    installed["feature-dep"].requires = ["common>=2"]
    assert preload_packages(root)["issues"] == [
        {"dependency": "common", "reason": "ValueError"}
    ]


def test_receipt_attests_actual_inventory_and_rejects_stale_lock(
    dependency_environment,
):
    root, installed, path = dependency_environment
    result = preload_packages(root)
    receipt = {
        "schema_version": 2,
        "status": "installed",
        "lock_sha256": result["lock_sha256"],
        "pyproject_sha256": hashlib.sha256(
            (root / "pyproject.toml").read_bytes()
        ).hexdigest(),
        "groups": ["project", "chatgpt"],
        "python_version": result["python"]["version"],
        "python_implementation": result["python"]["implementation"],
        "python_requires": result["python"]["requires"],
        "isolated": True,
        "installed_distributions": [
            {"name": n, "version": d.version} for n, d in installed.items()
        ],
    }
    path.write_text(json.dumps(receipt))
    assert preload_packages(root)["receipt"]["status"] == "verified"
    receipt["lock_sha256"] = "stale"
    path.write_text(json.dumps(receipt))
    assert preload_packages(root)["status"] == "blocked"
    receipt["lock_sha256"] = result["lock_sha256"]
    receipt["installed_distributions"].pop()
    path.write_text(json.dumps(receipt))
    assert preload_packages(root)["issues"] == [
        {"dependency": "installation-receipt", "reason": "StaleInstallationReceipt"}
    ]


def test_markdown_dependency_paths_preserve_real_links_and_legacy_provenance():
    registry = ExecutionRegistry(ROOT)
    result = registry.dependency_manifest("kb_orchestration_workflow")
    assert result["declared_sources_complete"]
    assert any(
        r["to"]
        == "skills/orchestration/kb-orchestrator/scripts/generate_reasoning_dynamics.py"
        and r["authority"] == "canonical_skill_scripts"
        for r in result["resolved_references"]
    )
    assert (
        registry._source_path(
            "integrations/README.md", "docs/README.md", markdown_link=True
        )
        == "docs/integrations/README.md"
    )
    assert not registry._markdown_references(
        "abducer-prism/references/test.md",
        '```prism\nreturn python_call[Finding]("reviews.inspect", access)\n```',
    )
    assert (
        registry._source_path(
            "conversion/project-semantic-taxonomy.json",
            "abducer-prism/skills/to-prism-derive-types/SKILL.md",
        )
        is None
    )


def test_setup_export_is_complete_and_installer_rejects_unsafe_destinations(tmp_path):
    package = outputs()
    for name in ("pyproject.toml", "uv.lock"):
        assert package[Path("runtime-setup") / name] == (ROOT / name).read_bytes()
    assert (
        package[Path("runtime-setup/setup_runtime.py")]
        == (ROOT / "integrations/chatgpt/setup_runtime.py").read_bytes()
    )
    assert (
        json.loads(package[Path("release.json")])["dependency_setup"]["starts_research"]
        is False
    )
    with pytest.raises(ValueError, match="outside"):
        install(ROOT, ROOT / "plugin-test-environment")
    foreign = tmp_path / "foreign"
    foreign.mkdir()
    (foreign / "important.txt").write_text("preserve me")
    with pytest.raises(ValueError, match="not created"):
        install(ROOT, foreign)
    assert (foreign / "important.txt").read_text() == "preserve me"
