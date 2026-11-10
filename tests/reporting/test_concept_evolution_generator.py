# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for automatic concept-evolution generation for KB workflows.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from generate_concept_evolution import _build_markdown
from generate_concept_evolution import _phase_key


def test_phase_key_detects_yang_mills_specific_phases() -> None:
    """
    Concept: Validates that phase key detects yang mills specific phases.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    assert (
        _phase_key({"id": "st.def.os-euclidean-qft", "kind": "definition", "informal": "OS axioms and reflection positivity."})
        == "euclidean-os-framework"
    )
    assert (
        _phase_key({"id": "st.custom.bridge", "kind": "theorem", "statement_phase": "mass-gap-and-spectral-transfer", "informal": "Explicit metadata."})
        == "mass-gap-and-spectral-transfer"
    )
    assert (
        _phase_key({"id": "st.rem.continuum-limit-bottleneck", "kind": "remark", "informal": "Continuum-limit bottleneck remains open."})
        == "bottlenecks-and-open-gaps"
    )
    assert (
        _phase_key({"id": "st.thm.transfer-matrix-gap", "kind": "theorem", "informal": "Transfer-matrix gap implies exponential correlator decay and a mass gap."})
        == "mass-gap-and-spectral-transfer"
    )


def test_build_markdown_uses_domain_specific_bridge_agenda_title() -> None:
    """
    Concept: Validates that build markdown uses a domain-specific bridge agenda title.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    kb_path = Path("KB/yang-mills-existence-and-mass-gap.kb.md")
    markdown = _build_markdown(
        kb_path=kb_path,
        statements=[
            {"id": "st.prob.yang-mills", "kind": "problem", "informal": "Yang-Mills mass gap problem."},
            {"id": "st.def.os-euclidean-qft", "kind": "definition", "informal": "OS axioms and reflection positivity."},
            {"id": "st.thm.transfer-matrix-gap", "kind": "theorem", "informal": "Transfer-matrix gap yields correlator decay and a mass gap."},
        ],
        analysis={
            "top_interventions": [
                {"statement_id": "st.thm.transfer-matrix-gap", "rationale": "bridge into mass-gap route"}
            ]
        },
        phyp={
            "hypotheses": [
                {
                    "support_statement_id": "st.def.os-euclidean-qft",
                    "target_statement_id": "st.thm.transfer-matrix-gap",
                    "template_family": "transfer-matrix-to-gap-bridge",
                }
            ]
        },
    )

    assert "## Active Yang-Mills Bridge Agenda" in markdown
    assert "`st.thm.transfer-matrix-gap`" in markdown
    assert "`st.def.os-euclidean-qft` -> `st.thm.transfer-matrix-gap` via transfer-matrix-to-gap-bridge" in markdown


def test_build_markdown_uses_fixed_point_phase_titles() -> None:
    """
    Concept: Validates that build markdown uses theorem-specific phase narration for fixed-point KBs.
    Contribution: Documents the intended regression boundary so later changes do not silently flatten theorem-specific concept evolution into generic headings.
    """

    kb_path = Path("KB/markov-kakutani-fixed-point-theorem.kb.md")
    markdown = _build_markdown(
        kb_path=kb_path,
        statements=[
            {
                "id": "st.def.fixed-point-subset",
                "kind": "definition",
                "statement_phase": "fixed-point-subset-formation",
                "informal": "The fixed-point subset is the hidden bridge object.",
            },
            {
                "id": "st.lem.commuting-preserves-fixed-point-subset",
                "kind": "lemma",
                "statement_phase": "commuting-invariance",
                "informal": "Commuting maps preserve the fixed-point subset.",
            },
        ],
        analysis={"top_interventions": []},
        phyp={"hypotheses": []},
    )

    assert "## Fixed-Point Subset Formation" in markdown
    assert "## Commuting Invariance" in markdown
    assert "## Active Fixed-Point Bridge Agenda" in markdown
