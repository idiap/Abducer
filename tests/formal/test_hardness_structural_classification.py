# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""
Regression tests for structural epistemic-hardness classification.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HARDNESS_SCRIPTS = ROOT / "skills" / "discovery" / "kb-epistemic-hardness" / "scripts"
if str(HARDNESS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(HARDNESS_SCRIPTS))

from articulate_hardness import _build_report


def test_hardness_uses_structural_signals_not_id_lexical_tokens() -> None:
    """
    Concept: Validates that hardness uses structural signals not id lexical tokens.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    statements = {
        "st.t.alpha": {
            "id": "st.t.alpha",
            "kind": "theorem",
            "is_barrier": True,
            "method_tags": ["barrier-analysis"],
            "used_symbols": [],
            "concept_roles": [],
            "latex": "A(x)",
            "depends_on": [],
        },
        "st.t.beta": {
            "id": "st.t.beta",
            "kind": "theorem",
            "method_tags": ["circuit-lower-bounds"],
            "used_symbols": ["Parity"],
            "concept_roles": [],
            "latex": "B(x)",
            "depends_on": [],
        },
        "st.t.gamma": {
            "id": "st.t.gamma",
            "kind": "theorem",
            "method_tags": [],
            "used_symbols": ["NP", "Pclass"],
            "concept_roles": [],
            "latex": r"\NP \subseteq \Pclass",
            "depends_on": [],
        },
    }

    analysis = {
        "connection_candidates": [],
        "top_interventions": [],
        "concept_graph": {
            "nodes": [
                {"id": "statement:st.t.alpha", "type": "statement", "statement_id": "st.t.alpha"},
                {"id": "statement:st.t.beta", "type": "statement", "statement_id": "st.t.beta"},
                {"id": "statement:st.t.gamma", "type": "statement", "statement_id": "st.t.gamma"},
                {"id": "barrier:st.t.alpha", "type": "barrier", "statement_id": "st.t.alpha"},
                {"id": "method:circuit-lower-bounds", "type": "method", "label": "circuit-lower-bounds"},
                {"id": "concept:np", "type": "concept", "label": "np"},
            ],
            "relations": [
                {"from": "statement:st.t.alpha", "to": "barrier:st.t.alpha", "relation": "defines", "weight": 0.9},
                {"from": "barrier:st.t.alpha", "to": "statement:st.t.gamma", "relation": "obstructs", "weight": 0.7},
                {"from": "statement:st.t.beta", "to": "method:circuit-lower-bounds", "relation": "uses", "weight": 0.7},
                {"from": "statement:st.t.gamma", "to": "concept:np", "relation": "uses", "weight": 0.7},
            ],
        },
    }
    entrypoints = {"ranked_entrypoints": []}
    pathways = {"pathways": []}
    phyp = {"hypotheses": []}

    report = _build_report(
        problem="P vs NP",
        statements=statements,
        phase_of={},
        analysis=analysis,
        entrypoints=entrypoints,
        pathways=pathways,
        phyp=phyp,
    )

    stats = report["kb_stats"]
    assert stats["barrier_family_count"] >= 1
    barrier_element = next(el for el in report["essential_elements"] if el["name"] == "Barrier Stack Constraints")
    asymmetry_element = next(el for el in report["essential_elements"] if el["name"] == "Asymmetric Lower-Bound Evidence")
    assert barrier_element["evidence"]["barrier_theorems"] >= 1
    assert asymmetry_element["evidence"]["restricted_lower_bounds"] >= 1
    assert asymmetry_element["evidence"]["grand_target_related_theorems"] >= 1
