# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""
Regression tests for connector status filtering and candidate inclusion policy.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONNECTOR_SCRIPTS = ROOT / "skills" / "discovery" / "kb-proof-connector" / "scripts"
if str(CONNECTOR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(CONNECTOR_SCRIPTS))

from analyze_kb_graph import analyze_kb


def test_analyze_kb_excludes_rejected_by_default_filter(tmp_path: Path) -> None:
    """
    Concept: Validates that analyze KB excludes rejected by default filter.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    kb_path = tmp_path / "mini.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.def.a",
                "kind: definition",
                "status: accepted",
                "latex: A",
                "informal: A",
                "source_ids: []",
                "used_symbols: []",
                "depends_on: []",
                "confidence: 0.9",
                "proof_sketch: ''",
                "notes: ''",
                "```",
                "",
                "```yaml",
                "id: st.thm.rej",
                "kind: theorem",
                "status: rejected",
                "latex: R",
                "informal: R",
                "source_ids: []",
                "used_symbols: []",
                "depends_on: [st.def.a]",
                "confidence: 0.1",
                "proof_sketch: ''",
                "notes: ''",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    accepted_report = analyze_kb(
        kb_path=kb_path,
        top_k=10,
        min_similarity=0.0,
        max_connections=10,
        loop_rounds=1,
        include_statuses={"accepted"},
    )
    assert accepted_report["stats"]["statement_count"] == 1
    assert accepted_report["stats"]["filtered_out_count"] == 1
    assert accepted_report["top_interventions"][0]["statement_id"] == "st.def.a"

    all_report = analyze_kb(
        kb_path=kb_path,
        top_k=10,
        min_similarity=0.0,
        max_connections=10,
        loop_rounds=1,
        include_statuses={"accepted", "rejected"},
    )
    assert all_report["stats"]["statement_count"] == 2
    assert "concept_graph" in all_report
    assert isinstance(all_report["concept_graph"].get("nodes"), list)
    assert isinstance(all_report["concept_graph"].get("relations"), list)
