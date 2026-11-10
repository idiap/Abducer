# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Regression coverage for the adapted project-support skill pack."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PACK = REPO / "proj_skills"


def run_script(relative: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PACK / relative), *args],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def test_project_support_pack_validator_passes() -> None:
    result = run_script("scripts/validate_proj_skills.py")
    assert result.returncode == 0, result.stderr
    catalog = json.loads((PACK / "catalog.yaml").read_text(encoding="utf-8"))
    assert f"validated {len(catalog['skills'])} catalogued project-support skills" in result.stdout


def test_readme_validator_matches_abducer_front_door(tmp_path: Path) -> None:
    output = tmp_path / "readme.json"
    result = run_script(
        "project-readme-orchestrator/scripts/validate_project_readme.py",
        "--repo",
        str(REPO),
        "--json-output",
        str(output),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["status"] == "pass"
    assert not report["errors"]


def test_report_generators_are_offline_and_emit_models(tmp_path: Path) -> None:
    cases = [
        ("workflow-health-audit-orchestrator/scripts/generate_workflow_health_audit.py", "health", []),
        ("project-evolution-timeline-reporter/scripts/generate_project_evolution_report.py", "evolution", ["--max-milestones", "4"]),
        ("project-workflow-graph-reporter/scripts/generate_workflow_graph_report.py", "graph", []),
    ]
    models: dict[str, object] = {}
    for script, stem, extra in cases:
        html = tmp_path / f"{stem}.html"
        model = tmp_path / f"{stem}.json"
        result = run_script(
            script,
            "--repo",
            str(REPO),
            "--output",
            str(html),
            "--json-output",
            str(model),
            *extra,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        rendered = html.read_text(encoding="utf-8")
        assert "<html" in rendered.lower()
        assert "cdn.jsdelivr" not in rendered.lower()
        models[stem] = json.loads(model.read_text(encoding="utf-8"))

    graph = models["graph"]
    assert isinstance(graph, dict)
    assert graph["summary"]["stacks"] >= 4
    assert graph["summary"]["unique_skills"] >= 20
