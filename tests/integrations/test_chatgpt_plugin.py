# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Hosted client packaging keeps source identity and local-plugin isolation."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

import pytest

from integrations.chatgpt.generate_plugin import (
    ROOT,
    PROFILE,
    checked_endpoint,
    outputs,
    write_archive,
)
from integrations.chatgpt.catalog import Catalog


def test_hosted_package_accounts_for_canonical_sources_without_local_resolution():
    generated = outputs()
    inventory = json.loads(generated[Path("source-inventory.json")])
    source = json.loads((ROOT / "plugins/abducer/source-skills.json").read_text())
    contracts = json.loads((ROOT / "plugins/abducer/workflows.json").read_text())
    assert {x["name"]: x["sha256"] for x in inventory["skills"]} == {
        x["name"]: x["sha256"] for x in source["skills"]
    }
    assert {x["id"] for x in inventory["workflows"]} == {
        x["id"] for x in contracts["workflows"]
    }
    assert len(inventory["viewer_mappings"]) == 19
    assert all(x["status"] == "inspectable" for x in inventory["skills"])
    entries = [p for p in generated if p.name == "SKILL.md"]
    assert len(entries) == 5
    for path in entries:
        text = generated[path].decode()
        assert "resolve_checkout.py" not in text
        assert "ABDUCER_ROOT" not in text
        assert "get_capabilities" in text
        reference = json.loads(generated[path.parent / "references/canonical.json"])
        for skill in reference["skills"]:
            assert (
                hashlib.sha256((ROOT / skill["source"]).read_bytes()).hexdigest()
                == skill["sha256"]
            )
    assert (
        json.loads(generated[Path("release.json")])["source_release"]
        == Catalog(ROOT).release
    )


def test_source_profile_has_no_invented_endpoint_and_release_requires_https():
    generated = outputs()
    assert json.loads(generated[Path("mcp.json")])["mcpServers"] == {}
    assert not json.loads(generated[Path("release.json")])["configured"]
    endpoint = "https://research.idiap.ch/mcp"
    release = outputs(endpoint=endpoint)
    server = json.loads(release[Path("mcp.json")])["mcpServers"]["abducer"]
    assert server["type"] == "streamable-http"
    assert server["url"] == endpoint
    assert server["extensions"]["com.openai"]["auth"]["type"] == "oauth"
    assert json.loads(release[Path("release.json")])["configured"]


@pytest.mark.parametrize(
    "endpoint",
    [
        "http://research.idiap.ch/mcp",
        "https://example.com/mcp",
        "https://localhost/mcp",
        "https://127.0.0.1/mcp",
        "https://user:password@research.idiap.ch/mcp",
        "https://research.idiap.ch/mcp?token=secret",
        "https://research.idiap.ch/mcp#secret",
        "https://research.idiap.ch/not-mcp",
        "https://deployment.invalid/mcp",
        "https://YOUR_HOST/mcp",
        "https://abducer/mcp",
        "https://10.0.0.2/mcp",
        "https://research.idiap.ch:bad/mcp",
    ],
)
def test_invalid_release_endpoints_rejected(endpoint):
    with pytest.raises(ValueError):
        checked_endpoint(endpoint)


def test_generation_and_check_detect_drift_without_touching_local_plugin(tmp_path):
    original = {
        p.relative_to(ROOT / "plugins/abducer"): hashlib.sha256(
            p.read_bytes()
        ).hexdigest()
        for p in (ROOT / "plugins/abducer").rglob("*")
        if p.is_file()
    }
    command = [
        sys.executable,
        "-m",
        "integrations.chatgpt.generate_plugin",
        "--output",
        str(tmp_path / "release"),
    ]
    subprocess.run(command, cwd=ROOT, check=True, capture_output=True)
    subprocess.run(command + ["--check"], cwd=ROOT, check=True, capture_output=True)
    skill = tmp_path / "release/skills/abducer-plan/SKILL.md"
    skill.write_text(skill.read_text() + "\nDrift\n")
    assert (
        subprocess.run(command + ["--check"], cwd=ROOT, capture_output=True).returncode
        == 1
    )
    after = {
        p.relative_to(ROOT / "plugins/abducer"): hashlib.sha256(
            p.read_bytes()
        ).hexdigest()
        for p in (ROOT / "plugins/abducer").rglob("*")
        if p.is_file()
    }
    assert original == after


def test_checked_in_hosted_profile_is_reproducible():
    for path, content in outputs().items():
        assert (ROOT / PROFILE / path).read_bytes() == content, path


def test_export_binds_hook_contract_and_preserves_original_event_names():
    generated = outputs()
    release = json.loads(generated[Path("release.json")])
    hook = release["native_hooks"]
    assert (
        hashlib.sha256(generated[Path(hook["contract"])]).hexdigest()
        == hook["contract_sha256"]
    )
    assert hook["host_hooks_registered"] is False
    assert hook["execution_authority"] == "native-runtime"
    assert Path("hooks/hooks.json") not in generated
    native = Path("native-hook-runtime/source/hooks/hooks.json")
    assert generated[native] == (ROOT / "hooks/hooks.json").read_bytes()
    assert {row["event"] for row in json.loads(generated[native])["hooks"]} == {
        "UserPromptSubmit",
        "PreSkillUse",
        "PreToolUse",
        "PostSkillUse",
        "Stop",
    }
    assert (
        "hooks"
        not in json.loads(generated[Path("plugin.json")])["extensions"]["com.openai"]
    )


def test_archive_is_reproducible_and_contains_only_generated_sources(tmp_path):
    generated = outputs()
    first, second = tmp_path / "first.zip", tmp_path / "second.zip"
    (tmp_path / "unrelated-secret.txt").write_text("not part of this package")
    write_archive(first, generated)
    write_archive(second, generated)
    assert first.read_bytes() == second.read_bytes()
    with zipfile.ZipFile(first) as archive:
        assert set(archive.namelist()) == {path.as_posix() for path in generated}
        for path, content in generated.items():
            assert archive.read(path.as_posix()) == content


def test_archive_rejects_paths_outside_plugin_without_replacing_destination(tmp_path):
    target = tmp_path / "plugin.zip"
    target.write_bytes(b"existing export")
    with pytest.raises(ValueError, match="Noncanonical"):
        write_archive(target, {Path("../outside"): b"untrusted"})
    assert target.read_bytes() == b"existing export"


@pytest.mark.parametrize("extra", [["--check"], ["--inside-output"]])
def test_archive_cli_refuses_check_mode_or_output_contamination(tmp_path, extra):
    output = tmp_path / "client"
    archive = (output if extra == ["--inside-output"] else tmp_path) / "client.zip"
    command = [
        sys.executable,
        "-m",
        "integrations.chatgpt.generate_plugin",
        "--output",
        str(output),
        "--archive",
        str(archive),
    ]
    if extra == ["--check"]:
        command += extra
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 2
    assert "--archive requires generation" in result.stderr
    assert not output.exists()
    assert not archive.exists()


def test_browser_bridge_and_research_interactions():
    node = shutil.which("node")
    if not node:
        pytest.skip("Node is required for the browser bridge harness")
    subprocess.run(
        [node, "tests/infrastructure/chatgpt_explorer_frontend.mjs"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        timeout=30,
    )
