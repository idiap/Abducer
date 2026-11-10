# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for coherence-aware entrypoint ranking.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT_SCRIPTS = ROOT / "skills" / "discovery" / "kb-entrypoint-finder" / "scripts"
if str(ENTRYPOINT_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ENTRYPOINT_SCRIPTS))

from recommend_entrypoints import _build_recommendations


def test_coherence_salience_preserves_magnitude_across_statements() -> None:
    """
    Concept: Validates that coherence salience preserves magnitude across statements.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    statements = {
        "st.a": {"id": "st.a", "kind": "theorem", "notes": "", "informal": "A", "latex": "A"},
        "st.b": {"id": "st.b", "kind": "definition", "notes": "", "informal": "B", "latex": "B"},
        "st.c": {"id": "st.c", "kind": "theorem", "notes": "", "informal": "C", "latex": "C"},
        "st.d": {"id": "st.d", "kind": "definition", "notes": "", "informal": "D", "latex": "D"},
    }
    concept_map = {}
    analysis = {"top_interventions": [], "connection_candidates": [], "concept_graph": {"relations": []}}
    phyp = {
        "hypotheses": [
            {
                "id": "h.low",
                "kind": "bridge-link",
                "target_statement_id": "st.a",
                "support_statement_id": "st.b",
                "priority": 0.6,
            },
            {
                "id": "h.high",
                "kind": "bridge-link",
                "target_statement_id": "st.c",
                "support_statement_id": "st.d",
                "priority": 0.6,
            },
        ]
    }
    coherence = {
        "hypothesis_coherence_index": {
            "h.low": {"explanatory_power_local": 0.25, "coherence_delta_global": 0.05},
            "h.high": {"explanatory_power_local": 0.85, "coherence_delta_global": 0.30},
        }
    }

    report = _build_recommendations(
        statements=statements,
        concept_map=concept_map,
        analysis=analysis,
        phyp=phyp,
        coherence=coherence,
        top_k=10,
    )

    by_id = {row["statement_id"]: row for row in report["ranked_entrypoints"]}
    low = float(by_id["st.a"]["evidence"]["coherence_salience"])
    high = float(by_id["st.c"]["evidence"]["coherence_salience"])
    assert low > 0.0
    assert high > low
    # Regression guard: single-value normalization bug collapsed all positives to 1.0.
    assert not (low == 1.0 and high == 1.0)
