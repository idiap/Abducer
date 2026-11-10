# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""
Regression tests for reasoning-log marker capture from orchestrated command output.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _load_module(path: Path, name: str):
    """
    Concept: Loads a script module directly from disk for log-marker extraction tests.
    Contribution: Keeps the tests focused on script behavior without requiring package installation side effects.
    """
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_orchestrator_extract_log_paths_matches_plain_log_marker() -> None:
    """
    Concept: Validates that orchestrator extract log paths matches plain log marker.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    module = _load_module(
        ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "run_orchestrator.py",
        "run_orchestrator",
    )
    payload = "line a\n[LOG] /tmp/a.md\nline b\n[LOG] relative/b.md\n"
    parsed = module._extract_log_paths(payload)
    assert [str(p) for p in parsed] == ["/tmp/a.md", "relative/b.md"]


def test_integrated_runner_extract_log_paths_matches_plain_log_marker() -> None:
    """
    Concept: Validates that integrated runner extract log paths matches plain log marker.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    module = _load_module(
        ROOT / "skills" / "discovery" / "kb-novel-proof-strategist" / "scripts" / "run_integrated_pvsnp.py",
        "run_integrated_pvsnp",
    )
    payload = "[LOG] /tmp/x.md\n"
    parsed = module._extract_log_paths(payload)
    assert [str(p) for p in parsed] == ["/tmp/x.md"]
