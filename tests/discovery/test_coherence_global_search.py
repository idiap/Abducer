# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for set-level coherentist search in the coherence evaluator.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COH_SCRIPTS = ROOT / "skills" / "discovery" / "kb-coherence-evaluator" / "scripts"
if str(COH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(COH_SCRIPTS))

from evaluate_coherence import _global_theory_search


def test_global_theory_search_prefers_positive_core_subset() -> None:
    """
    Concept: Validates that global theory search prefers positive core subset.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    nodes = {
        "statement:st.a": {"id": "statement:st.a", "type": "statement"},
        "statement:st.b": {"id": "statement:st.b", "type": "statement"},
        "statement:st.c": {"id": "statement:st.c", "type": "statement"},
        "hypothesis:h.good": {"id": "hypothesis:h.good", "type": "hypothesis"},
        "hypothesis:h.bad": {"id": "hypothesis:h.bad", "type": "hypothesis"},
    }
    base_edges = []
    hypothesis_edges = [
        {
            "from": "statement:st.a",
            "to": "statement:st.b",
            "relation": "supports",
            "weight": 0.9,
            "hypothesis_id": "h.good",
        },
        {
            "from": "statement:st.c",
            "to": "statement:st.b",
            "relation": "attacks",
            "weight": 0.9,
            "hypothesis_id": "h.bad",
        },
    ]
    hypothesis_rows = [
        {
            "hypothesis_id": "h.good",
            "explanatory_power_local": 0.72,
            "coherence_delta_global": 0.18,
            "priority": 0.8,
            "target_statement_id": "st.b",
            "support_statement_id": "st.a",
        },
        {
            "hypothesis_id": "h.bad",
            "explanatory_power_local": 0.30,
            "coherence_delta_global": -0.22,
            "priority": 0.7,
            "target_statement_id": "st.b",
            "support_statement_id": "st.c",
        },
    ]

    search = _global_theory_search(
        nodes=nodes,
        base_edges=base_edges,
        hypothesis_edges=hypothesis_edges,
        hypothesis_rows=hypothesis_rows,
        statement_count=3,
        beam_width=8,
        max_depth=3,
    )

    best = search["best_subset"]
    best_ids = set(best.get("hypothesis_ids", []))
    assert "h.good" in best_ids
    assert "h.bad" not in best_ids
    assert best.get("objective_score", 0.0) > 0.0
