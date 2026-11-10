# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""
Regression tests for incremental reasoning-log persistence.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def test_reasoning_logger_writes_incrementally(tmp_path: Path) -> None:
    """
    Concept: Validates that reasoning logger writes incrementally.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    root = Path(__file__).resolve().parents[2]
    module_path = root / "skills" / "common" / "reasoning_log.py"
    spec = importlib.util.spec_from_file_location("reasoning_log", module_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ReasoningLogger = mod.ReasoningLogger

    logger = ReasoningLogger("unit-test-agent", repo_root=tmp_path, run_id="run-abc")
    assert logger.log_path.exists()
    assert logger.surface_md_path.exists()
    assert logger.surface_json_path.exists()

    header = logger.log_path.read_text(encoding="utf-8")
    assert "- Run ID: run-abc" in header
    assert "Surface log (Markdown)" in header

    logger.step("first step", "detail=1")
    logger.surface(
        "Conceptual bridge candidate sharpened",
        "positive_route=constructive fixed-point subset\nnegative_route=obstruction via non-invariance",
        focus="bridge-object hypothesis",
        kind="conceptual_move",
    )
    content = logger.log_path.read_text(encoding="utf-8")
    assert "first step" in content
    assert "detail=1" in content

    logger.add_output("x", "artifacts/a.json")
    logger.finalize("success", summary="ok")
    done = logger.log_path.read_text(encoding="utf-8")
    assert "## Run Result" in done
    assert "- Status: success" in done
    assert "- x: artifacts/a.json" in done

    surface_md = logger.surface_md_path.read_text(encoding="utf-8")
    assert "Reasoning Surface: unit-test-agent" in surface_md
    assert "Conceptual bridge candidate sharpened" in surface_md
    assert "Declared output: x" in surface_md

    surface_json = json.loads(logger.surface_json_path.read_text(encoding="utf-8"))
    assert surface_json["run_id"] == "run-abc"
    assert surface_json["status"] == "success"
    assert any(moment.get("title") == "first step" for moment in surface_json.get("moments", []))
    assert any(moment.get("title") == "Conceptual bridge candidate sharpened" for moment in surface_json.get("moments", []))
