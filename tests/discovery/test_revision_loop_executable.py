# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for executable ontology revision operators.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REV_SCRIPTS = ROOT / "skills" / "evaluation" / "kb-revision-loop" / "scripts"
if str(REV_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(REV_SCRIPTS))

from revise_ontology import _apply_revision_actions


def test_revision_loop_applies_executable_operators(tmp_path: Path) -> None:
    """
    Concept: Validates that revision loop applies executable operators.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    kb_path = tmp_path / "KB" / "demo.kb.md"
    kb_path.parent.mkdir(parents=True, exist_ok=True)
    kb_path.write_text(
        "\n".join(
            [
                "# Demo KB",
                "",
                "```yaml",
                "id: st.a",
                "kind: theorem",
                "status: tentative",
                "depends_on: [st.missing.x]",
                "informal: Statement A",
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )

    statements = {
        "st.a": {
            "id": "st.a",
            "kind": "theorem",
            "depends_on": ["st.missing.x"],
            "informal": "Statement A",
        }
    }
    phyp = {
        "hypotheses": [
            {
                "id": "h.low",
                "kind": "bridge-link",
                "status": "tentative",
                "priority": 0.8,
                "target_statement_id": "st.a",
                "support_statement_id": "st.b",
            },
            {
                "id": "h.concept",
                "kind": "representation-shift",
                "status": "tentative",
                "priority": 0.6,
                "target_statement_id": "st.a",
                "support_statement_id": "st.b",
            },
        ]
    }
    report = {
        "revision_actions": [
            {"revision_id": "rev.001", "revision_type": "definition-repair", "target_hypothesis_ids": ["h.low"]},
            {"revision_id": "rev.002", "revision_type": "representation-rotation", "target_hypothesis_ids": ["h.concept"]},
            {"revision_id": "rev.003", "revision_type": "concept-splitting", "target_statement_ids": ["st.a"]},
            {"revision_id": "rev.004", "revision_type": "kb-reencoding"},
        ]
    }

    patched_kb, patched_phyp, executable = _apply_revision_actions(
        kb_path=kb_path,
        statements=statements,
        phyp=phyp,
        report=report,
    )

    assert executable["applied"] is True
    assert executable["operator_counts"]["definition_repair_touches"] >= 1
    assert executable["operator_counts"]["representation_rotations_generated"] >= 1
    assert executable["operator_counts"]["generated_statements"] >= 1
    assert "## Auto-Generated Revision Patch" in patched_kb
    assert "h.concept.rot1" in {h.get("id", "") for h in patched_phyp.get("hypotheses", [])}
    low = next(h for h in patched_phyp["hypotheses"] if h.get("id") == "h.low")
    assert low.get("status") == "needs-testing"
