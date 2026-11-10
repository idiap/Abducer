# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for proof-knockout materialization in theorem discovery simulation.

Concept: Simulated ignorance should blank authored proof structure while leaving the theorem statements themselves available.
Contribution: Keeps discovery simulation aligned with the framework's intended partial-knowledge setting.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORCH_SCRIPTS = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts"
if str(ORCH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ORCH_SCRIPTS))

from simulate_theorem_discovery import _extract_statements
from simulate_theorem_discovery import _materialize_knockout_kb


def test_materialize_knockout_kb_blanks_proof_structure(tmp_path: Path) -> None:
    """
    Concept: Validates that proof-structure knockout removes dependency and proof metadata.
    Contribution: Documents the intended regression boundary so discovery simulation does not leak authored proof graphs to the agents.
    """

    kb_path = tmp_path / "mini-proof.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.def.base",
                "kind: definition",
                "status: accepted",
                "latex: Base definition.",
                "informal: Base definition.",
                "source_ids: []",
                "used_symbols: []",
                "depends_on: []",
                "bridge_roles: [foundation]",
                "proof_sketch: ''",
                "notes: ''",
                "```",
                "",
                "```yaml",
                "id: st.thm.target",
                "kind: theorem",
                "status: accepted",
                "latex: Target theorem.",
                "informal: Target theorem.",
                "source_ids: []",
                "used_symbols: []",
                "depends_on: [st.def.base]",
                "bridge_roles: [core-characterization]",
                "proof_sketch: Uses the base definition.",
                "notes: Authored proof route.",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    working_kb, summary = _materialize_knockout_kb(
        kb_path=kb_path,
        output_dir=tmp_path / "working",
        target_statement_id="st.thm.target",
        profile="proof-structure",
        knockout_statements=[],
        knockout_edges=[],
        knockout_fields=[],
        bridge_concept_ids=[],
        bridge_concept_terms=[],
    )

    statements = _extract_statements(working_kb)
    theorem = statements["st.thm.target"]
    definition = statements["st.def.base"]

    assert summary["profile"] == "proof-structure"
    assert theorem["depends_on"] == []
    assert theorem["proof_sketch"] == ""
    assert theorem["notes"] == ""
    assert theorem["bridge_roles"] == []
    assert definition["depends_on"] == []
    assert definition["bridge_roles"] == ["foundation"]


def test_materialize_knockout_kb_hides_bridge_concept(tmp_path: Path) -> None:
    """
    Concept: Validates that bridge-concept knockout removes the defining statement and redacts nearby mentions while preserving the target theorem.
    Contribution: Ensures discovery simulation can model ignorance about a central bridge object rather than only hiding proof edges.
    """

    kb_path = tmp_path / "stone-mini.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.def.generator",
                "kind: definition",
                "status: accepted",
                "latex: The infinitesimal generator is defined by a derivative at zero.",
                "informal: The infinitesimal generator is the hidden bridge concept.",
                "source_ids: []",
                "used_symbols: []",
                "depends_on: []",
                "concept_roles: [cnc.infinitesimal-generator]",
                "bridge_roles: [generator-bridge]",
                "proof_sketch: Recover the infinitesimal generator from the orbit.",
                "notes: Main bridge concept.",
                "```",
                "",
                "```yaml",
                "id: st.prop.use",
                "kind: proposition",
                "status: accepted",
                "latex: The infinitesimal generator is symmetric.",
                "informal: This proposition uses the infinitesimal generator.",
                "source_ids: []",
                "used_symbols: []",
                "depends_on: [st.def.generator]",
                "concept_roles: [cnc.infinitesimal-generator]",
                "bridge_roles: [self-adjointness-witness]",
                "proof_sketch: Uses the infinitesimal generator.",
                "notes: Generator-side route.",
                "```",
                "",
                "```yaml",
                "id: st.thm.target",
                "kind: theorem",
                "status: accepted",
                "latex: Target theorem still states the final correspondence.",
                "informal: The target theorem stays visible.",
                "source_ids: []",
                "used_symbols: []",
                "depends_on: [st.prop.use]",
                "concept_roles: [cnc.self-adjoint-operator]",
                "bridge_roles: [correspondence-bijection]",
                "proof_sketch: Final theorem.",
                "notes: Final target route.",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    working_kb, summary = _materialize_knockout_kb(
        kb_path=kb_path,
        output_dir=tmp_path / "working",
        target_statement_id="st.thm.target",
        profile="bridge-concept",
        knockout_statements=[],
        knockout_edges=[],
        knockout_fields=[],
        bridge_concept_ids=["cnc.infinitesimal-generator"],
        bridge_concept_terms=["infinitesimal generator"],
    )

    statements = _extract_statements(working_kb)

    assert summary["profile"] == "bridge-concept"
    assert "st.def.generator" not in statements
    assert summary["redacted_mentions_count"] > 0
    assert statements["st.prop.use"]["notes"] == ""
    assert statements["st.prop.use"]["proof_sketch"] == ""
    assert statements["st.prop.use"]["concept_roles"] == []
    assert "[hidden bridge concept]" in statements["st.prop.use"]["informal"].lower()
    assert statements["st.thm.target"]["informal"] == "The target theorem stays visible."
