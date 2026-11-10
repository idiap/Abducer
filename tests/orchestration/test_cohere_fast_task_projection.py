# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_projection_is_current_and_exposes_parent_children_domain() -> None:
    result = subprocess.run([sys.executable, "agentic/scripts/generate_cohere_fast_task_registry.py", "--check"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads((ROOT / "registry/tasks/cohere-fast/task_registry.json").read_text())
    assert data["status"] == "disabled"
    assert data["visible_workflows"][0]["name"] == "cohere_fast"
    assert {row.get("subworkflow_id") for row in data["visible_workflows"][1:]} == {"scope-and-ground", "adaptive-frontier", "derivation-and-proof", "independent-audit", "manuscript-release"}
    assert all(row["domain_id"] == "ym" for row in data["visible_workflows"])
