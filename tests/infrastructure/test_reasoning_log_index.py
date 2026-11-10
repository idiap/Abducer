# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""
Regression tests for reasoning-log indexing, filtering, and stage coverage.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORCH_SCRIPTS = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts"
if str(ORCH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ORCH_SCRIPTS))

from generate_reasoning_log_index import _load_logs
from generate_reasoning_log_index import _summarize


def _write_log(
    path: Path,
    agent: str,
    run_id: str,
    status: str,
    summary: str,
    step_lines: list[str] | None = None,
) -> None:
    """
    Concept: Creates a minimal reasoning-log fixture with the structure expected by the indexer.
    Contribution: Provides deterministic test inputs for run filtering, coverage checks, and stage accounting.
    """
    lines = step_lines or ["- Parsed args"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                f"# Reasoning Log: {agent}",
                "",
                "- Started (UTC): 2026-03-11T10:00:00+00:00",
                f"- Run ID: {run_id}",
                f"- Log file: {path}",
                "",
                "## Step @ 2026-03-11T10:00:01+00:00",
                "",
                *lines,
                "",
                "## Run Result",
                "",
                f"- Status: {status}",
                "- Ended (UTC): 2026-03-11T10:00:02+00:00",
                "- Duration (s): 0.100",
                f"- Summary: {summary}",
                "",
                "## Declared Outputs",
                "",
                "- output_a: artifacts/example.json",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_reasoning_log_index_filters_by_run_id_and_detects_missing_agents(tmp_path: Path) -> None:
    """
    Concept: Validates that reasoning log index filters by run id and detects missing agents.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    log_root = tmp_path / "reasoning-logs"
    artifacts_dir = tmp_path / "artifacts"
    _write_log(log_root / "kb-orchestrator" / "a.md", "kb-orchestrator", "run-1", "success", "ok")
    _write_log(log_root / "kb-proof-connector" / "b.md", "kb-proof-connector", "run-1", "success", "ok")
    _write_log(log_root / "kb-proof-connector" / "c.md", "kb-proof-connector", "run-2", "success", "other")

    logs = _load_logs(
        log_root,
        repo_root=tmp_path,
        artifacts_dir=artifacts_dir,
        run_id="run-1",
    )
    assert len(logs) == 2
    assert {item["agent"] for item in logs} == {"kb-orchestrator", "kb-proof-connector"}

    summary = _summarize(logs, expected_agents=["kb-orchestrator", "kb-proof-connector", "kb-coherence-evaluator"])
    assert summary["log_count"] == 2
    assert summary["missing_expected_agents"] == ["kb-coherence-evaluator"]


def test_reasoning_log_index_tracks_stage_level_completeness(tmp_path: Path) -> None:
    """
    Concept: Validates that reasoning log index tracks stage level completeness.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    log_root = tmp_path / "reasoning-logs"
    artifacts_dir = tmp_path / "artifacts"
    _write_log(
        log_root / "kb-orchestrator" / "a.md",
        "kb-orchestrator",
        "run-1",
        "success",
        "ok",
        step_lines=["- Running stage: connect.analyze"],
    )

    logs = _load_logs(
        log_root,
        repo_root=tmp_path,
        artifacts_dir=artifacts_dir,
        run_id="run-1",
    )
    summary = _summarize(
        logs,
        expected_agents=["kb-orchestrator"],
        expected_stages=["connect.analyze"],
    )
    assert summary["missing_expected_stages"] == []
    assert summary["incomplete_expected_stages"] == ["connect.analyze"]
    assert summary["stage_coverage_complete"] is False


def test_reasoning_log_index_filters_by_kb_ref(tmp_path: Path) -> None:
    """
    Concept: Validates that reasoning log index filters by KB ref.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    log_root = tmp_path / "reasoning-logs"
    artifacts_alpha = tmp_path / "artifacts" / "alpha-kb"
    artifacts_beta = tmp_path / "artifacts" / "beta-kb"

    _write_log(
        log_root / "kb-orchestrator" / "alpha.md",
        "kb-orchestrator",
        "run-a",
        "success",
        "ok",
        step_lines=[
            "- Parsed args",
            "- kb=KB/alpha-kb.kb.md",
            "- kb_ref=alpha-kb",
            "- artifacts_dir=artifacts/alpha-kb",
        ],
    )
    _write_log(
        log_root / "kb-orchestrator" / "beta.md",
        "kb-orchestrator",
        "run-b",
        "success",
        "ok",
        step_lines=[
            "- Parsed args",
            "- kb=KB/beta-kb.kb.md",
            "- kb_ref=beta-kb",
            "- artifacts_dir=artifacts/beta-kb",
        ],
    )

    logs_alpha = _load_logs(
        log_root,
        repo_root=tmp_path,
        artifacts_dir=artifacts_alpha,
        kb_ref_filter="alpha-kb",
    )
    logs_beta = _load_logs(
        log_root,
        repo_root=tmp_path,
        artifacts_dir=artifacts_beta,
        kb_ref_filter="beta-kb",
    )
    assert len(logs_alpha) == 1
    assert len(logs_beta) == 1
    assert logs_alpha[0]["run_id"] == "run-a"
    assert logs_beta[0]["run_id"] == "run-b"
