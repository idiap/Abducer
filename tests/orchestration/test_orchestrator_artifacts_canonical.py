# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for orchestrator artifact-path canonicalization.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORCHESTRATOR_SCRIPTS = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts"
if str(ORCHESTRATOR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ORCHESTRATOR_SCRIPTS))

from run_orchestrator import _resolve_phyp_doc_pattern


def test_run_orchestrator_rejects_noncanonical_artifacts_dir(tmp_path: Path) -> None:
    """
    Concept: Validates that run orchestrator rejects noncanonical artifacts dir.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    kb_dir = tmp_path / "KB"
    kb_dir.mkdir(parents=True, exist_ok=True)
    kb = kb_dir / "p-vs-np.kb.md"
    kb.write_text("# minimal\n", encoding="utf-8")

    script = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "run_orchestrator.py"
    cmd = [
        sys.executable,
        str(script),
        "--intent",
        "interpretation-reports",
        "--kb",
        str(kb),
        "--artifacts-dir",
        str(tmp_path / "artifacts" / "pvsnp"),
        "--no-export-phyp-docs",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    merged = (result.stdout or "") + (result.stderr or "")

    assert result.returncode != 0
    assert "artifacts are associated with the reference KB name" in merged
    assert "artifacts/p-vs-np" in merged


def test_resolve_phyp_doc_pattern_defaults_to_kb_ref_scope() -> None:
    """
    Concept: Validates that resolve phyp doc pattern defaults to KB ref scope.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    assert _resolve_phyp_doc_pattern("", "yang-mills-existence-and-mass-gap") == "yang-mills-existence-and-mass-gap*.md"
    assert _resolve_phyp_doc_pattern("custom*.md", "yang-mills-existence-and-mass-gap") == "custom*.md"
