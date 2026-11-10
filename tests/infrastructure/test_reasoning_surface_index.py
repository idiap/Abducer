# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for surfaced reasoning-log indexing and filtering.

Concept: Captures the intended behavior of the human-facing reasoning-surface layer under deterministic test conditions.
Contribution: Keeps the new separation between internal audit traces and surfaced conceptual timelines stable across refactors.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORCH_SCRIPTS = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts"
if str(ORCH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ORCH_SCRIPTS))

from generate_reasoning_surface_index import _load_surfaces
from generate_reasoning_surface_index import _summarize
from generate_reasoning_surface_index import _timeline


def _write_surface(
    path: Path,
    agent: str,
    run_id: str,
    kb_ref: str,
    artifacts_dir: Path,
    focus: str,
    kind: str = "conceptual_move",
) -> None:
    """
    Concept: Creates a minimal surfaced reasoning fixture with the structure expected by the surface indexer.
    Contribution: Provides deterministic conceptual-movement inputs for run and KB filtering tests.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "agent": agent,
        "run_id": run_id,
        "started_utc": "2026-03-11T10:00:00+00:00",
        "ended_utc": "2026-03-11T10:00:02+00:00",
        "duration_s": 0.2,
        "status": "success",
        "summary": "surface ok",
        "internal_log_path": str(path.with_suffix(".md")),
        "surface_markdown_path": str(path.with_suffix(".surface.md")),
        "surface_json_path": str(path),
        "context": {
            "kb": f"KB/{kb_ref}.kb.md",
            "kb_ref": kb_ref,
            "artifacts_dir": str(artifacts_dir),
        },
        "outputs": [
            {
                "label": "report",
                "path": str(artifacts_dir / "report.md"),
            }
        ],
        "moments": [
            {
                "timestamp": "2026-03-11T10:00:01+00:00",
                "kind": kind,
                "title": f"{agent} move",
                "focus": focus,
                "significance": "tracks conceptual progress",
                "details": ["detail=a"],
                "tags": ["conceptual"],
                "stage": focus,
            }
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_reasoning_surface_index_filters_by_run_id_and_summarizes_moments(tmp_path: Path) -> None:
    """
    Concept: Validates that surfaced reasoning index filters by run id and summarizes conceptual movement.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the surfaced reasoning view.
    """

    surface_root = tmp_path / "reasoning-surfaces"
    artifacts_dir = tmp_path / "artifacts" / "alpha-kb"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    _write_surface(
        surface_root / "kb-orchestrator" / "a.json",
        "kb-orchestrator",
        "run-1",
        "alpha-kb",
        artifacts_dir,
        focus="bridge-plan",
        kind="stage_delegation",
    )
    _write_surface(
        surface_root / "kb-proof-sketcher" / "b.json",
        "kb-proof-sketcher",
        "run-1",
        "alpha-kb",
        artifacts_dir,
        focus="proof feasibility",
        kind="conceptual_move",
    )
    _write_surface(
        surface_root / "kb-proof-sketcher" / "c.json",
        "kb-proof-sketcher",
        "run-2",
        "alpha-kb",
        artifacts_dir,
        focus="other run",
        kind="conceptual_move",
    )

    surfaces = _load_surfaces(
        surface_root,
        repo_root=tmp_path,
        artifacts_dir=artifacts_dir,
        run_id="run-1",
    )
    assert len(surfaces) == 2
    assert {item["agent"] for item in surfaces} == {"kb-orchestrator", "kb-proof-sketcher"}

    summary = _summarize(surfaces, expected_agents=["kb-orchestrator", "kb-proof-sketcher", "kb-coherence-evaluator"])
    assert summary["surface_count"] == 2
    assert summary["total_moment_count"] == 2
    assert summary["missing_expected_agents"] == ["kb-coherence-evaluator"]
    assert summary["moment_kind_counts"]["stage_delegation"] == 1
    assert summary["moment_kind_counts"]["conceptual_move"] == 1

    timeline = _timeline(surfaces)
    assert len(timeline) == 2
    assert timeline[0]["focus"] == "bridge-plan"


def test_reasoning_surface_index_filters_by_kb_ref(tmp_path: Path) -> None:
    """
    Concept: Validates that surfaced reasoning index filters by KB ref.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken KB-scoped surfaced reporting.
    """

    surface_root = tmp_path / "reasoning-surfaces"
    artifacts_alpha = tmp_path / "artifacts" / "alpha-kb"
    artifacts_beta = tmp_path / "artifacts" / "beta-kb"
    artifacts_alpha.mkdir(parents=True, exist_ok=True)
    artifacts_beta.mkdir(parents=True, exist_ok=True)

    _write_surface(surface_root / "kb-orchestrator" / "alpha.json", "kb-orchestrator", "run-a", "alpha-kb", artifacts_alpha, "alpha-focus")
    _write_surface(surface_root / "kb-orchestrator" / "beta.json", "kb-orchestrator", "run-b", "beta-kb", artifacts_beta, "beta-focus")

    surfaces_alpha = _load_surfaces(
        surface_root,
        repo_root=tmp_path,
        artifacts_dir=artifacts_alpha,
        kb_ref_filter="alpha-kb",
    )
    surfaces_beta = _load_surfaces(
        surface_root,
        repo_root=tmp_path,
        artifacts_dir=artifacts_beta,
        kb_ref_filter="beta-kb",
    )

    assert len(surfaces_alpha) == 1
    assert len(surfaces_beta) == 1
    assert surfaces_alpha[0]["run_id"] == "run-a"
    assert surfaces_beta[0]["run_id"] == "run-b"
