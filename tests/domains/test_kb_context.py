# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for KB reference resolution and canonical artifact routing.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMON = ROOT / "skills" / "common"
if str(COMMON) not in sys.path:
    sys.path.insert(0, str(COMMON))

from kb_context import canonical_artifacts_dir
from kb_context import resolve_kb_reference


def test_resolve_kb_reference_prefers_front_matter_kb_id(tmp_path: Path) -> None:
    """
    Concept: Validates that resolve KB reference prefers front matter KB id.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    kb = tmp_path / "KB" / "sample-name.kb.md"
    kb.parent.mkdir(parents=True, exist_ok=True)
    kb.write_text(
        "\n".join(
            [
                "---",
                "kb_id: custom-kb-ref",
                "---",
                "",
                "# Canonical Statements",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    ctx = resolve_kb_reference(kb)
    assert ctx["kb_ref"] == "custom-kb-ref"
    assert ctx["kb_ref_from_filename"] == "sample-name"
    assert ctx["kb_ref_from_front_matter"] == "custom-kb-ref"


def test_resolve_kb_reference_rejects_mismatched_explicit_ref(tmp_path: Path) -> None:
    """
    Concept: Validates that resolve KB reference rejects mismatched explicit ref.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    kb = tmp_path / "KB" / "sample-name.kb.md"
    kb.parent.mkdir(parents=True, exist_ok=True)
    kb.write_text(
        "\n".join(
            [
                "---",
                "kb_id: canonical-kb",
                "---",
                "",
                "# Canonical Statements",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    try:
        resolve_kb_reference(kb, explicit_kb_ref="other-kb")
    except ValueError as exc:
        assert "does not match" in str(exc)
    else:
        raise AssertionError("Expected ValueError for mismatched explicit kb_ref")


def test_canonical_artifacts_dir_uses_kb_reference(tmp_path: Path) -> None:
    """
    Concept: Validates that canonical artifacts dir uses KB reference.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    resolved = canonical_artifacts_dir(tmp_path, "Graph_Theory KB")
    assert resolved == (tmp_path / "artifacts" / "graph-theory-kb").resolve()
