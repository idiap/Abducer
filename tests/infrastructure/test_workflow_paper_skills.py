# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""End-to-end contract tests for the workflow-to-paper skill stack."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
RUNNER = REPO / "proj_skills/framework-paper-orchestrator/scripts/run_framework_paper.py"
FIXTURE = REPO / "tests/fixtures/workflow_paper/observed/repo"


def invoke(output: Path, *extra: str, repo: Path = FIXTURE) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUNNER), "--repo", str(repo), "--output-root", str(output),
         "--slug", "fixture", "--run-id", "run", *extra],
        cwd=REPO, text=True, capture_output=True, check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def test_full_repository_only_run_is_evidence_qualified_and_resumable(tmp_path: Path) -> None:
    first = invoke(tmp_path)
    assert first.returncode == 0, first.stdout + first.stderr
    run = tmp_path / "fixture/run"
    manifest = json.loads((run / "run-manifest.json").read_text())
    validation = json.loads((run / "bundle/validation.json").read_text())
    assert manifest["status"] == validation["status"] == "pass"
    assert manifest["promotion_status"] == "not_promoted"
    tex = (run / "bundle/main.tex").read_text()
    assert "No provenance-valid literature snapshot" in tex
    assert "No authorized result packet" in tex
    receipt = run / "receipts/01-evidence-index.json"
    before = receipt.stat().st_mtime_ns
    resumed = invoke(tmp_path, "--resume")
    assert resumed.returncode == 0, resumed.stdout + resumed.stderr
    assert receipt.stat().st_mtime_ns == before


def test_existing_run_requires_explicit_resume(tmp_path: Path) -> None:
    assert invoke(tmp_path).returncode == 0
    rejected = invoke(tmp_path)
    assert rejected.returncode != 0
    assert "--resume" in rejected.stderr


def test_every_stage_has_a_passing_receipt(tmp_path: Path) -> None:
    assert invoke(tmp_path).returncode == 0
    receipts = sorted((tmp_path / "fixture/run/receipts").glob("*.json"))
    assert len(receipts) == 20
    assert all(json.loads(path.read_text())["status"] == "pass" for path in receipts)


def test_resume_reindexes_when_frozen_source_changes(tmp_path: Path) -> None:
    snapshot = tmp_path / "snapshot"
    shutil.copytree(FIXTURE, snapshot)
    output = tmp_path / "out"
    assert invoke(output, repo=snapshot).returncode == 0
    evidence = output / "fixture/run/models/evidence-index.json"
    before = json.loads(evidence.read_text())["index_digest"]
    (snapshot / "README.md").write_text("new frozen-snapshot evidence\n")
    assert invoke(output, "--resume", repo=snapshot).returncode == 0
    after = json.loads(evidence.read_text())["index_digest"]
    assert after != before


def test_missing_optional_authority_is_rejected_in_preflight(tmp_path: Path) -> None:
    result = invoke(tmp_path, "--literature", str(tmp_path / "missing.json"))
    assert result.returncode != 0
    assert "must be an existing file" in result.stderr
