# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Contract tests for the generated named-workflow task projection."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _contract_skills(contract: dict) -> list[str]:
    names = [contract["owner_skill"]]
    names.extend(step["skill"] for step in contract["steps"])
    for profile in contract.get("profiles", []):
        names.extend(step["skill"] for step in profile.get("steps", []))
        names.extend(profile.get("specialist_skills", []))
    return list(dict.fromkeys(names))


def test_named_workflow_projection_is_current() -> None:
    result = subprocess.run(
        [sys.executable, "agentic/scripts/generate_named_workflow_task_registry.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_projection_preserves_contract_order_membership_and_hooks() -> None:
    contracts = _read("agentic/registries/named_workflow_contracts.yaml")["workflows"]
    manifest = _read("registry/optional-tasks/named-skill-workflows/task_registry.json")
    projection = manifest["visible_workflows"]
    for hook in manifest["reference_hooks"]:
        assert hook["path"].startswith("hooks/workflow_local/")
        assert (ROOT / hook["path"]).is_file()
    by_id = {row["workflow_id"]: row for row in projection}
    assert set(by_id) == {row["id"] for row in contracts}
    for contract in contracts:
        row = by_id[contract["id"]]
        assert row["name"] == contract["id"]
        assert row["workflow_version"] == contract["version"]
        assert row["activation"] == contract["activation"]
        assert row["composed_skills"] == _contract_skills(contract)
        assert row["deterministic_hooks"] == [hook["hook_id"] for hook in contract["hooks"]]


def test_default_workflow_manifests_are_not_rewritten_as_named_workflows() -> None:
    task = _read("registry/tasks/target-navigation/task_registry.json")
    assert [row["name"] for row in task["visible_workflows"]] == [
        "target-navigation-control-plane"
    ]
