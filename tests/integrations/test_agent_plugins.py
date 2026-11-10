# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Test plugin routing and source identity without executing a research workflow."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
import yaml

from integrations.agent_plugins.generate import (
    PLUGIN,
    ROOT,
    expected_files,
    public_skills,
    synchronize,
    workflow_catalog,
)


@pytest.fixture
def checkout(tmp_path: Path) -> Path:
    """Use an actual canonical skill in a space-containing minimal checkout."""
    root = tmp_path / "research checkout"
    source = Path("skills/orchestration/work/SKILL.md")
    (root / source).parent.mkdir(parents=True)
    shutil.copyfile(ROOT / source, root / source)
    shutil.copyfile(ROOT / "pyproject.toml", root / "pyproject.toml")
    return root


@pytest.fixture
def resolver(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("ABDUCER_ROOT", raising=False)
    path = ROOT / PLUGIN / "scripts/resolve_checkout.py"
    spec = importlib.util.spec_from_file_location("abducer_checkout", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.resolve


def test_every_public_skill_has_one_matching_entry():
    rows = public_skills(ROOT)
    assert len(rows) == len(list((ROOT / "skills").glob("*/*/SKILL.md")))
    assert len({row["name"] for row in rows}) == len(rows)
    assert synchronize(ROOT, check=True) == []
    private = (ROOT / "skills/domain_specific").rglob("SKILL.md")
    assert all(
        str(path.relative_to(ROOT)) not in {r["source"] for r in rows}
        for path in private
    )
    for row in rows:
        text = (ROOT / PLUGIN / "skills" / row["name"] / "SKILL.md").read_text()
        frontmatter = yaml.safe_load(text.split("---", 2)[1])
        assert frontmatter == {"name": row["name"], "description": row["description"]}


def test_catalogs_resolve_same_contained_package():
    metadata = json.loads(
        (ROOT / "integrations/agent_plugins/metadata.json").read_text()
    )
    codex = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    claude = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    paths = [codex["plugins"][0]["source"]["path"], claude["plugins"][0]["source"]]
    assert paths == ["./plugins/abducer"] * 2
    for name in (
        "plugin.json",
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
    ):
        manifest = json.loads((ROOT / PLUGIN / name).read_text())
        assert manifest["name"] == "abducer"
        assert manifest["version"] == metadata["version"]
        assert "hooks" not in manifest
        if name == ".codex-plugin/plugin.json":
            assert manifest["mcpServers"] == "./.codex-mcp.json"
    assert not (ROOT / PLUGIN / "hooks").exists()
    assert not any(path.is_symlink() for path in (ROOT / PLUGIN).rglob("*"))


def test_resolve_from_nested_checkout(checkout, monkeypatch, resolver):
    monkeypatch.chdir(checkout / "skills/orchestration/work")
    result = resolver("work")
    assert result["root"] == str(checkout.resolve())
    assert result["skill_file"] == str(
        (checkout / "skills/orchestration/work/SKILL.md").resolve()
    )


def test_explicit_root_wins_and_paths_with_spaces_work(checkout, monkeypatch, resolver):
    monkeypatch.setenv("ABDUCER_ROOT", str(checkout))
    assert resolver("work")["root"] == str(checkout.resolve())
    monkeypatch.setenv("ABDUCER_ROOT", str(checkout / "not a checkout"))
    with pytest.raises(ValueError, match="No Abducer checkout"):
        resolver("work")
    assert resolver("work", str(checkout))["root"] == str(checkout.resolve())


def test_missing_checkout_does_not_resolve_plugin_cache(
    tmp_path, monkeypatch, resolver
):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match="No Abducer checkout"):
        resolver("work")
    monkeypatch.chdir(ROOT / PLUGIN)
    # Development loading may find the outer source repository; an installed
    # package in an unrelated directory cannot manufacture that ancestor.
    assert resolver("work")["root"] == str(ROOT.resolve())


@pytest.mark.parametrize("skill", ["../../work", "absent-skill"])
def test_unknown_skills_cannot_escape_inventory(skill, resolver):
    with pytest.raises(ValueError, match="Unknown public"):
        resolver(skill)


def test_source_drift_and_missing_source_fail(checkout, resolver):
    source = checkout / "skills/orchestration/work/SKILL.md"
    source.write_text(source.read_text() + "\nchanged\n")
    with pytest.raises(ValueError, match="versions differ"):
        resolver("work", str(checkout))
    source.unlink()
    with pytest.raises(ValueError, match="Missing or escaped"):
        resolver("work", str(checkout))


def test_canonical_source_cannot_escape_checkout(checkout, tmp_path, resolver):
    source = checkout / "skills/orchestration/work/SKILL.md"
    other = tmp_path / "outside.md"
    source.rename(other)
    source.symlink_to(other)
    with pytest.raises(ValueError, match="escaped"):
        resolver("work", str(checkout))


def test_resolver_cli_from_unrelated_directory(checkout, tmp_path, monkeypatch):
    monkeypatch.delenv("ABDUCER_ROOT", raising=False)
    script = ROOT / PLUGIN / "scripts/resolve_checkout.py"
    command = [sys.executable, str(script), "--skill", "work"]
    success = subprocess.run(
        command + ["--root", str(checkout)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert success.returncode == 0, success.stderr
    assert json.loads(success.stdout)["root"] == str(checkout.resolve())
    failure = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    assert failure.returncode == 1
    assert "Abducer setup required" in failure.stderr


def test_generation_detects_drift_additions_and_removals(tmp_path):
    source = Path("skills/orchestration/work/SKILL.md")
    (tmp_path / source).parent.mkdir(parents=True)
    shutil.copyfile(ROOT / source, tmp_path / source)
    metadata = Path("integrations/agent_plugins/metadata.json")
    (tmp_path / metadata).parent.mkdir(parents=True)
    shutil.copyfile(ROOT / metadata, tmp_path / metadata)
    (tmp_path / "LICENSES").mkdir()
    shutil.copyfile(ROOT / "LICENSES/MIT.txt", tmp_path / "LICENSES/MIT.txt")
    # Keep a real normalized contract in this minimal source checkout.
    workflow = next(
        r for r in workflow_catalog(ROOT) if r["id"] == "abducer_work_workflow"
    )
    index = Path("agentic/reasoning_flows/workflow_skill_v1/index.yaml")
    (tmp_path / index).parent.mkdir(parents=True)
    (tmp_path / index).write_text(
        yaml.safe_dump(
            {
                "workflows": [
                    {
                        k: workflow[k]
                        for k in (
                            "namespace",
                            "id",
                            "version",
                            "aliases",
                            "owner",
                            "descriptor",
                        )
                    }
                ]
            }
        )
    )
    descriptor = tmp_path / workflow["descriptor"]
    descriptor.parent.mkdir(parents=True)
    shutil.copyfile(ROOT / workflow["descriptor"], descriptor)
    server = Path("integrations/workflow_mcp/server.py")
    (tmp_path / server).parent.mkdir(parents=True)
    shutil.copyfile(ROOT / server, tmp_path / server)
    helper = server.with_name("agent_assets.py")
    shutil.copyfile(ROOT / helper, tmp_path / helper)
    assert synchronize(tmp_path, check=False)
    assert synchronize(tmp_path, check=True) == []
    assert synchronize(tmp_path, check=False) == []
    generated = tmp_path / PLUGIN / "skills/work/SKILL.md"
    generated.write_text("drift")
    orphan = tmp_path / PLUGIN / "skills/removed/SKILL.md"
    orphan.parent.mkdir()
    orphan.write_text("old")
    untouched = orphan.parent / "manual.txt"
    untouched.write_text("keep")
    assert str(generated.relative_to(tmp_path)) in synchronize(tmp_path, check=True)
    synchronize(tmp_path, check=False)
    assert not orphan.exists() and untouched.read_text() == "keep"
    new = tmp_path / "skills/orchestration/new-entry/SKILL.md"
    new.parent.mkdir()
    new.write_text(
        "---\nname: new-entry\ndescription: New public skill.\n---\nProcedure\n"
    )
    assert PLUGIN / "skills/new-entry/SKILL.md" in expected_files(tmp_path)
    duplicate = tmp_path / "skills/another/work/SKILL.md"
    duplicate.parent.mkdir(parents=True)
    shutil.copyfile(tmp_path / source, duplicate)
    with pytest.raises(ValueError, match="duplicate"):
        public_skills(tmp_path)


@pytest.mark.parametrize(
    "name", ["work", "cohere-fast-orchestrator", "ym-run-clay-program"]
)
def test_entry_instructions_preserve_checkout_and_activation_gates(name):
    text = (ROOT / PLUGIN / "skills" / name / "SKILL.md").read_text()
    assert "Read the returned `skill_file` in full" in text
    assert "never in the installed plugin cache" in text
    assert "stop this route" in text
    assert "generic domain prose does not authorize an opt-in workflow" in text
