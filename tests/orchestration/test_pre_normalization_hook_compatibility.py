# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Pin native composition and hook behavior to the user's f90f0c6f baseline.

The fixture contains historical hashes and workflow rows, not regenerated
expectations from the current implementation. Subprocess probes use disposable
repositories so original latest-file trace writes never touch research state.
Optional workflow-local policies are tested separately and cannot substitute
for these native behavior checks.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
BASELINE = json.loads(
    (ROOT / "tests/fixtures/pre_normalization_workflows.json").read_text()
)
RELOCATION_ALIAS = (
    '    # Preserve the original docs/looper-* protection after thematic relocation.\n'
    '    if str(raw).startswith("docs/integrations/looper-"):\n'
    '        raw = str(raw).replace("docs/integrations/", "docs/", 1)\n'
)
DISCOVERY_METADATA = {
    "key_function", "problem_domain_types", "reasoning_types", "task_context_types"
}
STOP_ARTIFACTS = (
    "agentic/state/current_target.json",
    "agentic/state/dependency_frontier.json",
    "agentic/reports/compliance/latest.md",
    "agentic/reports/drift/latest.md",
    "agentic/todos/looper_integration_todos.yaml",
)


def test_native_sources_and_workflow_contracts_match_historical_bytes() -> None:
    for relative, expected in BASELINE["files"].items():
        content = (ROOT / relative).read_bytes()
        if relative == "hooks/scripts/hook_utils.py":
            # Only the documented relocation alias may differ from baseline.
            assert content.decode().count(RELOCATION_ALIAS) == 1
            content = content.replace(RELOCATION_ALIAS.encode(), b"")
        assert hashlib.sha256(content).hexdigest() == expected, relative


def test_native_task_scan_preserves_composition_and_allowed_skills() -> None:
    actual = {
        path.relative_to(ROOT).as_posix(): [
            {key: value for key, value in row.items() if key not in DISCOVERY_METADATA}
            for row in json.loads(path.read_text())["visible_workflows"]
        ]
        for path in (ROOT / "registry/tasks").glob("*/task_registry.json")
    }
    # Exact rows preserve identity, ordering, conditional modes, children and
    # hook names. Exact file keys also reject an extra auto-discovered catalog.
    # The uv migration changes dependency artifact paths only; keep the original
    # fixture intact so composition and hook behavior retain their baseline.
    expected = json.loads(json.dumps(BASELINE["task_workflows"]))
    for rows in expected.values():
        for row in rows:
            if "requirements-pmp.txt" in row.get("artifacts", []):
                artifacts = row["artifacts"]
                index = artifacts.index("requirements-pmp.txt")
                artifacts[index:index + 1] = ["pyproject.toml", "uv.lock"]
    assert actual == expected
    configured = json.loads((ROOT / "hooks/hooks.json").read_text())
    assert "workflow_local" not in json.dumps(configured)
    assert "workflow_local" not in (ROOT / ".codex/hooks.json").read_text()


@pytest.mark.parametrize(
    "script,payload,expected",
    [
        ("pre_skill_use_policy", {"skill": "baseline-skill"}, "accept"),
        ("pre_skill_use_policy", {"skill": "unknown"}, "block"),
        ("pre_skill_use_policy", {"skill": "unknown", "controlled": False}, "accept"),
        ("pre_skill_use_policy", {}, "accept"),
        ("pre_skill_use_policy", {"skill": "baseline-skill", "workflow_id": "other", "completed_steps": []}, "accept"),
        ("pre_tool_use_policy", {"command": "rm -rf /tmp/example"}, "block"),
        ("pre_tool_use_policy", {"path": "registry/example.json"}, "warn"),
        ("pre_tool_use_policy", {"path": "registry/example.json", "evidence": "TODO-1"}, "accept"),
        ("pre_tool_use_policy", {"path": "docs/looper-control-plane.md"}, "warn"),
        ("pre_tool_use_policy", {"path": "docs/integrations/looper-control-plane.md"}, "warn"),
        ("pre_tool_use_policy", {"path": "tests/example.py", "workflow_id": "other", "controlled": True}, "accept"),
        ("post_skill_use_review", {"expected_artifacts": ["missing.json"]}, "warn"),
        ("post_skill_use_review", {"expected_artifacts": []}, "accept"),
        ("stop_artifact_check", {"controlled": False}, "accept"),
        ("stop_artifact_check", {"controlled": True}, "block"),
        ("user_prompt_submit_intake", {"prompt": "keep working"}, "warn"),
        ("user_prompt_submit_intake", {"prompt": "hello", "trigger_facts": {"external_mathematical_source": True}}, "accept"),
    ],
)
def test_original_native_hook_decisions(
    tmp_path: Path, script: str, payload: dict, expected: str
) -> None:
    _prepare_repository(tmp_path)
    result = _invoke(tmp_path, script, payload)
    assert result["decision"] == expected
    trace = tmp_path / f"agentic/traces/hook_runs/latest-{script}.json"
    assert json.loads(trace.read_text()) == {
        "hook": script, "payload": payload, "result": result
    }
    assert not (tmp_path / "agentic/traces/public_reasoning").exists()


def _prepare_repository(root: Path) -> None:
    """Supply only baseline-style task discovery and the real restored hooks."""
    shutil.copytree(ROOT / "hooks/scripts", root / "hooks/scripts")
    registry = root / "registry/tasks/example/task_registry.json"
    registry.parent.mkdir(parents=True)
    registry.write_text(json.dumps({
        "visible_workflows": [{"composed_skills": ["baseline-skill"]}]
    }))


def _invoke(root: Path, script: str, payload: dict) -> dict:
    result = subprocess.run(
        [sys.executable, str(root / f"hooks/scripts/{script}.py")],
        input=json.dumps(payload), text=True, capture_output=True,
        cwd=root, timeout=10, check=True,
    )
    return json.loads(result.stdout)


def test_original_stop_requires_every_baseline_artifact(tmp_path: Path) -> None:
    _prepare_repository(tmp_path)
    for relative in STOP_ARTIFACTS:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture")
    assert _invoke(tmp_path, "stop_artifact_check", {"controlled": True}) == {
        "decision": "accept", "reason": "Required stop-time artifacts are present."
    }
    (tmp_path / STOP_ARTIFACTS[-1]).unlink()
    rejected = _invoke(tmp_path, "stop_artifact_check", {"controlled": True})
    assert rejected["decision"] == "block"
    assert rejected["missing"] == [STOP_ARTIFACTS[-1]]
