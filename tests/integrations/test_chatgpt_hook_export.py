# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Verify portable native decisions and reject altered or escaping hook bundles.

The extraction test imports only the exported dispatcher in an isolated Python
process. Its policy outcomes are independent expectations, not exporter-derived
answers, so byte preservation is accompanied by behavioral evidence.
"""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from integrations.chatgpt import hook_export
from integrations.chatgpt.native_hooks import _source_files

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def bundle(tmp_path):
    plugin = tmp_path / "plugin"
    for relative, data in hook_export.outputs(ROOT).items():
        path = plugin / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return plugin / hook_export.PREFIX


def test_export_preserves_original_bytes_and_native_membership_only(bundle):
    before = _source_files(ROOT)
    generated = hook_export.outputs(ROOT)
    assert generated == hook_export.outputs(ROOT)
    for relative in before:
        assert (bundle / "source" / relative).read_bytes() == (
            ROOT / relative
        ).read_bytes()
    assert (bundle / "runner/native_hooks.py").read_bytes() == (
        ROOT / hook_export.DISPATCHER
    ).read_bytes()
    assert not any("workflow_local" in str(path) for path in generated)
    assert not any("optional-tasks" in str(path) for path in generated)
    assert not any("agentic/traces" in str(path) for path in generated)
    manifest = hook_export.validate_bundle(bundle)
    assert (
        hook_export.validate_bundle(bundle, expected_digest=manifest["bundle_digest"])
        == manifest
    )
    assert _source_files(ROOT) == before


def test_contract_distinguishes_native_execution_from_host_installation(bundle):
    contract = json.loads((bundle / "hook-contract.json").read_text())
    events = {event["event"]: event for event in contract["events"]}
    assert events["PostSkillUse"]["decisions"] == ["accept", "warn"]
    assert events["Stop"]["decisions"] == ["accept", "block"]
    assert contract["requirements"]["stop_artifacts"] == hook_export.STOP_ARTIFACTS
    assert contract["scope"]["host_hook_registration"] is False
    assert contract["scope"]["all_workflow_execution_parity"] is False
    assert contract["unregistered_scripts"]["files"] == [
        "hooks/scripts/cohere_fast_intake.py",
        "hooks/scripts/cohere_fast_policy.py",
    ]


def test_extracted_dispatcher_runs_real_accept_warn_block_without_checkout(
    bundle, tmp_path
):
    workspace = tmp_path / "workspace"
    shutil.copytree(bundle / "source", workspace)
    # -I removes repository/user Python paths; -B keeps the immutable bundle free
    # of import caches. The runner itself uses the copied native hook scripts.
    script = r"""
import importlib.util, json, pathlib, sys
bundle, workspace = map(pathlib.Path, sys.argv[1:])
spec = importlib.util.spec_from_file_location("exported_hooks", bundle / "runner/native_hooks.py")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
hooks = module.NativeHookDispatcher(source_root=bundle / "source", workspace=workspace)
declared = set()
for registry in (workspace / "registry/tasks").glob("*/task_registry.json"):
    for workflow in json.loads(registry.read_text()).get("visible_workflows", []):
        declared.update(workflow.get("composed_skills", []))
assert declared
cases = [
    ("UserPromptSubmit", {"prompt": "hello"}, "accept"),
    ("UserPromptSubmit", {"prompt": "keep working"}, "warn"),
    ("PreSkillUse", {"skill": sorted(declared)[0]}, "accept"),
    ("PreSkillUse", {"skill": "not-a-native-declared-skill"}, "block"),
    ("PreToolUse", {"command": "rm -rf scratch"}, "block"),
    ("PreToolUse", {"path": "registry/fixture.json"}, "warn"),
    ("PreToolUse", {"command": "python --version"}, "accept"),
    ("PostSkillUse", {"expected_artifacts": ["missing.json"]}, "warn"),
    ("PostSkillUse", {"expected_artifacts": []}, "accept"),
    ("Stop", {"controlled": True}, "block"),
    ("Stop", {"controlled": False}, "accept"),
]
for event, payload, expected in cases:
    try:
        receipt = hooks.require(event, payload)
        assert expected != "block"
    except module.NativeHookBlocked as error:
        receipt = error.receipt
        assert expected == "block"
    assert receipt.result["decision"] == expected
    trace = json.loads((workspace / receipt.native_trace).read_text())
    assert trace["payload"] == payload and trace["result"] == receipt.result
contract = json.loads((bundle / "hook-contract.json").read_text())
for relative in contract["requirements"]["stop_artifacts"]:
    path = workspace / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("fixture artifact")
assert hooks.require("Stop", {"controlled": True}).result["decision"] == "accept"
assert len((workspace / module.JOURNAL).read_text().splitlines()) == len(cases) + 1
print(json.dumps({"cases": len(cases) + 1, "source_digest": hooks.source_digest}))
"""
    completed = subprocess.run(
        [sys.executable, "-I", "-B", "-c", script, str(bundle), str(workspace)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert completed.returncode == 0, completed.stderr
    result = json.loads(completed.stdout)
    assert result["cases"] == 12
    assert (
        result["source_digest"] == hook_export.validate_bundle(bundle)["source_digest"]
    )
    assert not (bundle / "source/agentic").exists()


@pytest.mark.parametrize(
    "relative",
    [
        "source/hooks/scripts/hook_utils.py",
        "source/hooks/scripts/pre_skill_use_policy.py",
        "source/registry/tasks/cohere-fast/task_registry.json",
        "runner/native_hooks.py",
        "hook-contract.json",
    ],
)
def test_validation_rejects_changed_code_membership_or_contract(bundle, relative):
    path = bundle / relative
    path.write_bytes(path.read_bytes() + b"\n")
    with pytest.raises(hook_export.HookExportError, match="drifted"):
        hook_export.validate_bundle(bundle)


@pytest.mark.parametrize("change", ["missing", "extra", "symlink", "large"])
def test_validation_rejects_incomplete_or_unsafe_tree(bundle, tmp_path, change):
    script = bundle / "source/hooks/scripts/hook_utils.py"
    if change == "missing":
        script.unlink()
    elif change == "extra":
        (bundle / "source/hooks/scripts/shadow.py").write_text("private data")
    elif change == "symlink":
        outside = tmp_path / "outside.py"
        script.rename(outside)
        script.symlink_to(outside)
    else:
        with script.open("wb") as stream:
            stream.truncate(hook_export.MAX_FILE_BYTES + 1)
    with pytest.raises(hook_export.HookExportError):
        hook_export.validate_bundle(bundle)


def test_release_pin_rejects_rehashed_modified_bundle(bundle):
    manifest_path = bundle / "manifest.json"
    original = json.loads(manifest_path.read_text())
    manifest = json.loads(manifest_path.read_text())
    path = bundle / "runner/native_hooks.py"
    path.write_bytes(path.read_bytes() + b"\n# altered release\n")
    manifest["files"]["runner/native_hooks.py"] = {
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
    }
    del manifest["bundle_digest"]
    manifest["bundle_digest"] = hashlib.sha256(
        hook_export._encoded(manifest)
    ).hexdigest()
    manifest_path.write_bytes(hook_export._encoded(manifest))
    with pytest.raises(hook_export.HookExportError, match="release"):
        hook_export.validate_bundle(bundle, expected_digest=original["bundle_digest"])


@pytest.mark.parametrize("path", ["../outside", "/outside", "a\\b", "a/./b"])
def test_manifest_paths_cannot_escape_bundle(bundle, path):
    manifest_path = bundle / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["files"][path] = {"sha256": "0" * 64, "bytes": 0}
    del manifest["bundle_digest"]
    manifest["bundle_digest"] = hashlib.sha256(
        hook_export._encoded(manifest)
    ).hexdigest()
    manifest_path.write_bytes(hook_export._encoded(manifest))
    with pytest.raises(hook_export.HookExportError):
        hook_export.validate_bundle(bundle)


def test_export_rejects_altered_event_wiring(tmp_path):
    for relative in [*_source_files(ROOT), hook_export.DISPATCHER]:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((ROOT / relative).read_bytes())
    config_path = tmp_path / "hooks/hooks.json"
    config = json.loads(config_path.read_text())
    config["hooks"][0]["script"] = "hooks/workflow_local/user_prompt_submit_intake.py"
    config_path.write_text(json.dumps(config))
    with pytest.raises(hook_export.HookExportError, match="event contract"):
        hook_export.outputs(tmp_path)
