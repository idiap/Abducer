# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for the proof-discovery language specification."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMON_DIR = ROOT / "skills" / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from proof_discovery_language import build_language_spec
from proof_discovery_language import render_latex
from proof_discovery_language import render_markdown
from proof_discovery_language import serialize_discovery_branch_as_pdl
from proof_discovery_language import serialize_proof_attempt_as_pdl
from proof_discovery_language import serialize_queue_entry_as_pdl


def test_proof_discovery_language_covers_coherence_nexus_and_material_inference() -> None:
    spec = build_language_spec()

    primitive_ids = {row["id"] for row in spec["primitives"]}
    relation_ids = {row["id"] for row in spec["relations"]}
    judgment_forms = {row["form"] for row in spec["judgments"]}
    operation_ids = {row["id"] for row in spec["material_inference_operations"]}
    operational_judgment_forms = {row["form"] for row in spec["operational_judgments"]}

    assert spec["metadata"]["short_name"] == "PDL"
    assert "coherence" in spec["metadata"]["thesis"].lower()
    assert "material inference" in spec["metadata"]["thesis"].lower()
    assert {"anchor", "tension", "nexus", "bridge_object", "obstruction", "discovery_program", "proof_debt", "decision_gate"} <= primitive_ids
    assert {"extract", "focus", "concretize", "transport", "factor", "compose", "obstruct", "revise", "aggregate", "persist", "route"} <= operation_ids
    assert {"grounds", "coheres", "bridges", "obstructs", "persists", "loops"} <= relation_ids
    assert "K ; M |- A : grounded" in judgment_forms
    assert "A, X => N : coherent" in judgment_forms
    assert "P ; O |- impossibility(T)" in judgment_forms
    assert "A ; T |-m X" in operational_judgment_forms
    assert "B ; I ; s->t |-m tr_I(B)" in operational_judgment_forms

    markdown = render_markdown(spec)
    assert "# Proof Discovery Language" in markdown
    assert "coherent conceptual nexus" in markdown.lower()
    assert "material inference" in markdown.lower()
    assert "Material-Inference Operations" in markdown
    assert "Notation Layers" in markdown
    assert "Operational Judgments" in markdown
    assert "Well-Formed Discovery Program" in markdown

    latex = render_latex(spec)
    assert "\\section{Core Claim}" in latex
    assert "Proof Discovery Language" in latex
    assert "\\section{Material-Inference Operations}" in latex
    assert "\\section{Operational Judgments}" in latex
    assert "Well-Formed Discovery Program" in latex


def test_runtime_artifacts_can_serialize_as_pdl_programs() -> None:
    queue_program = serialize_queue_entry_as_pdl(
        {
            "queue_id": "proofq.demo.001",
            "kb_ref": "demo",
            "title": "Witness family route",
            "conjecture_statement": "There exists an admissible witness family yielding the target theorem.",
            "source_statement_id": "st.src",
            "target_statement_id": "st.tgt",
            "source_excerpt": "Source theorem body.",
            "target_excerpt": "Target theorem body.",
            "candidate_object": "Witness family",
            "carrier_kind": "family of hard instances",
            "preserved_invariant": "witness complexity profile",
            "route_synopsis": "Transport a source lower bound to the target theorem.",
            "missing_route_lemma": "Prove the witness family preserves the invariant.",
            "proof_strategy_family": "invariant-lift-through-intermediate-object",
            "proof_obligations": ["Realize the witness family."],
            "negative_reasoning_program": {
                "negative_mode": "non-realization",
                "negated_claim": "Assume no admissible witness family exists.",
                "contradiction_target": "Show realization fails.",
                "forbidden_outcome": "The bridge object is only topical overlap.",
                "impossibility_claim_template": "No admissible witness family currently forces the target theorem.",
            },
        }
    )
    assert queue_program["metadata"]["kind"] == "queue-entry"
    assert queue_program["bridge_object"]["label"] == "Witness family"

    branch_program = serialize_discovery_branch_as_pdl(
        {
            "branch_id": "disclayer.demo.family.realization",
            "kb_ref": "demo",
            "layer_kind": "breakthrough-family",
            "target_id": "realization",
            "target_label": "Carrier realization",
            "linked_queue_ids": ["proofq.demo.001"],
            "linked_breakthrough_families": ["realization"],
            "linked_obstruction_classes": ["carrier-realization"],
            "required_move": "Realize an explicit carrier.",
            "abstraction_required": "A witness family with admissibility conditions.",
            "minimal_theorem_shape": "If S then construct C forcing T.",
            "spawn_reason": "Blocked routes concentrate on carrier realization.",
            "rationale": "This branch searches for the missing carrier theorem.",
            "required_questions": ["What explicit carrier can absorb the source theorem?"],
            "expected_deliverables": ["A theorem-shaped realization claim."],
            "stop_criteria": ["Stop if the branch only renames the carrier."],
            "anti_patterns": ["Renaming the carrier."],
            "external_framework_search": {"recommended": False, "mode": "local-first"},
        }
    )
    assert branch_program["metadata"]["kind"] == "discovery-branch"
    assert branch_program["target"]["target_id"] == "realization"

    attempt_program = serialize_proof_attempt_as_pdl(
        {
            "metadata": {"attempt_id": "attempt.demo.001", "kb_ref": "demo", "queue_id": "proofq.demo.001"},
            "target": {
                "title": "Witness family route",
                "bridge_id": "bridge.001",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
                "carrier_kind": "family of hard instances",
                "preserved_invariant": "witness complexity profile",
                "route_synopsis": "Transport the source theorem to the target theorem.",
                "proof_obligations": ["Realize the witness family."],
                "candidate_lemmas": ["The witness family preserves the invariant."],
            },
            "local_context": {
                "source_excerpt": "Source theorem body.",
                "target_excerpt": "Target theorem body.",
                "mathlib_hits": [{"result_id": "mathlib.demo.001", "title": "Auxiliary lemma", "summary": "Helps realize the witness family."}],
            },
            "proof_attempt": {
                "theorem_statement": "There exists an admissible witness family yielding the target theorem.",
                "route_lemma_under_test": "Prove the witness family preserves the invariant.",
                "strategy": "invariant-lift-through-intermediate-object",
                "assumptions": ["Assume the witness family is admissible."],
                "stepwise_argument": [{"claim": "The source theorem induces the witness family."}],
                "contradiction_frame": {"negative_mode": "non-realization", "negated_claim": "Assume no witness family exists."},
                "negative_argument": {"impossibility_claim": "No admissible witness family currently forces the target theorem."},
                "negative_route_heuristic": {"decision": "parallel", "decision_rule": "Run constructive and negative routes in parallel."},
            },
            "web_search_gate": {"decision": "not-evaluated", "rationale": "Stay local first."},
            "final_assessment": {"outcome": "in_progress", "summary": "Proof scaffold only."},
        }
    )
    assert attempt_program["metadata"]["kind"] == "proof-attempt"
    assert attempt_program["positive_route"]["route_lemma"] == "Prove the witness family preserves the invariant."
