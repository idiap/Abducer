# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for proof-sketch generation and paper-style argument rendering.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skills" / "discovery" / "kb-proof-sketcher" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from generate_proof_sketches import _build
from generate_proof_sketches import _paper_style_argument
from generate_proof_sketches import _statement_body


def test_proof_sketch_mode_builds_invariant_lift_outline() -> None:
    """
    Concept: Validates that proof sketch mode builds invariant lift outline.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    conjectures = {
        "gap_clusters": [{"bridge_id": "bridge.001"}],
        "abstraction_conjectures": [
            {
                "conjecture_id": "conj.001",
                "bridge_id": "bridge.001",
                "abstraction_type": "intermediate-complexity-measure",
                "abstraction_label": "threshold-sensitive MCSP witness family",
                "mathematical_object_role": "A typed witness family recording near-threshold MCSP hardness data strongly enough to support magnification.",
                "carrier_kind": "family of instances equipped with a monotone witness measure",
                "typing_status": "typed",
                "priority": 0.82,
                "gap_target": "missing-intermediate-abstraction",
                "support_antecedent_schema": "MCSP-near-threshold-nonuniform-circuit-lower-bound",
                "target_consequence_schema": "NP-not-in-P/poly",
                "preserved_invariant": "MCSP complexity profile",
                "statement_delta": {
                    "source_claim_focus": "MCSP-near-threshold-nonuniform-circuit-lower-bound",
                    "target_claim_focus": "NP-not-in-P/poly",
                    "model_shift": "nonuniform-circuits -> P/poly",
                    "threshold_shift": "near-threshold lower bound -> major separation consequence",
                    "consequence_shift": "upgrade `MCSP-near-threshold-nonuniform-circuit-lower-bound` into `NP-not-in-P/poly`",
                    "missing_witness_or_transport": "Show that a threshold-sensitive MCSP witness family survives the move from nonuniform circuits to P/poly without losing the MCSP hardness profile.",
                },
                "definitional_completeness": 0.76,
                "counterfactual_sharpness": 0.71,
                "definitional_profile": {
                    "necessary_attributes": [
                        {
                            "attribute": "admits source-side witness data for `MCSP-near-threshold-nonuniform-circuit-lower-bound`",
                            "kind": "antecedent-realization",
                            "why_it_matters": "The bridge object must absorb the actual source-side hardness theorem rather than merely rename it.",
                        },
                        {
                            "attribute": "preserves the route invariant `MCSP complexity profile`",
                            "kind": "invariant-preservation",
                            "why_it_matters": "The object must remain sensitive to the source hardness profile.",
                        },
                        {
                            "attribute": "forces the target-side payoff `NP-not-in-P/poly`",
                            "kind": "consequence-forcing",
                            "why_it_matters": "The bridge only matters if it yields the intended separation payoff.",
                        },
                        {
                            "attribute": "specifies a typed carrier (family of instances equipped with a monotone witness measure) rather than a role-description only",
                            "kind": "explicit-object-witness",
                            "why_it_matters": "An expert needs to inspect an actual mathematical carrier, not a slogan.",
                        },
                    ],
                    "sufficient_attribute_sets": [
                        {
                            "label": "core set",
                            "attributes": [
                                "admits source-side witness data for `MCSP-near-threshold-nonuniform-circuit-lower-bound`",
                                "preserves the route invariant `MCSP complexity profile`",
                                "forces the target-side payoff `NP-not-in-P/poly`",
                            ],
                        }
                    ],
                },
                "counterfactual_probes": [
                    {
                        "intervention": "Permit the route from `MCSP-near-threshold-nonuniform-circuit-lower-bound` to `NP-not-in-P/poly` to proceed without preserving `MCSP complexity profile`.",
                        "expected_bridge_effect": "bridge-degrades-or-fails",
                        "diagnostic_value": "Separates a genuine MCSP witness family from a generic topical analogy.",
                    }
                ],
            }
        ],
    }
    strategies = {
        "strategies": [
            {
                "strategy_id": "strat.001",
                "name": "Magnification Route around st.def.mcsp",
                "phase": "Meta-Complexity",
                "anchor_statement_id": "st.def.mcsp",
                "strategy_score": 0.79,
                "bridge_ids": ["bridge.001"],
                "hypothesis_ids": ["phyp.001"],
                "anchor_concepts": ["MCSP", "hardness magnification"],
                "bridge_concepts": ["MCSP", "NP-not-in-P/poly"],
                "abstraction_concepts": ["threshold-sensitive MCSP witness family"],
                "definitional_focus": ["preserves the route invariant `MCSP complexity profile`"],
            }
        ]
    }
    bridges = {
        "bridge_programs": [
            {
                "bridge_id": "bridge.001",
                "from_id": "st.def.mcsp",
                "to_id": "st.thm.sep",
                "bridge_type": "magnification bridge",
                "statement_delta": {
                    "source_claim_focus": "MCSP-near-threshold-nonuniform-circuit-lower-bound",
                    "target_claim_focus": "NP-not-in-P/poly",
                    "model_shift": "nonuniform-circuits -> P/poly",
                    "threshold_shift": "near-threshold lower bound -> major separation consequence",
                    "consequence_shift": "upgrade `MCSP-near-threshold-nonuniform-circuit-lower-bound` into `NP-not-in-P/poly`",
                    "missing_witness_or_transport": "Show that a threshold-sensitive MCSP witness family survives the move from nonuniform circuits to P/poly without losing the MCSP hardness profile.",
                },
                "inferential_commitment": {
                    "support_antecedent_schema": "MCSP-near-threshold-nonuniform-circuit-lower-bound",
                    "target_consequence_schema": "NP-not-in-P/poly",
                    "preserved_invariant": "MCSP complexity profile",
                    "barrier_scope": "none",
                },
            }
        ]
    }
    phyp = {
        "hypotheses": [
            {
                "id": "phyp.001",
                "support_statement_id": "st.def.mcsp",
                "target_statement_id": "st.thm.sep",
                "kind": "intermediate-invariant",
            }
        ]
    }
    coherence = {
        "coherence_profile": {"global_coherence": 0.64},
        "hypothesis_coherence": [
            {
                "hypothesis_id": "phyp.001",
                "coherence_delta_global": 0.08,
                "explanatory_power_local": 0.57,
            }
        ],
    }

    report = _build(
        conjectures=conjectures,
        strategies=strategies,
        bridges=bridges,
        phyp=phyp,
        analysis={},
        coherence=coherence,
        hardness={},
        top_k=3,
    )

    assert report["recommended_execution_order"] == ["psk.001"]
    sketch = report["proof_sketches"][0]
    assert sketch["proof_strategy_family"] == "invariant-lift-through-intermediate-object"
    assert sketch["counterfactual_test"]["expected_bridge_effect"] == "bridge-degrades-or-fails"
    assert sketch["carrier_kind"] == "family of instances equipped with a monotone witness measure"
    assert sketch["statement_delta"]["model_shift"] == "nonuniform-circuits -> P/poly"
    assert "Show that a threshold-sensitive MCSP witness family survives the move" in sketch["statement_delta"]["missing_witness_or_transport"]
    assert any("preserves `MCSP complexity profile`" in row["requirement"] for row in sketch["proof_obligations"])
    assert any("route-specific lemma" in row["requirement"] for row in sketch["proof_obligations"])
    assert any("Payoff lemma" in row["statement"] for row in sketch["candidate_lemmas"])
    assert "If these assumptions hold" in sketch["mathematical_argument"]["proposition"]
    assert "candidate bridge object" not in sketch["mathematical_argument"]["bridge_definition"]
    assert sketch["negative_reasoning_program"]["negative_mode"] == "non-realization"
    assert sketch["negative_reasoning_program"]["heuristic"]["decision"] == "parallel"
    assert "No admissible carrier realizing" in sketch["negative_reasoning_program"]["impossibility_claim_template"]
    assert any("force `NP-not-in-P/poly`" in row["objective"] or "force `NP-not-in-P/poly`" in row["expected_output"] for row in sketch["proof_outline_steps"])


def test_proof_sketch_mode_builds_barrier_escape_outline() -> None:
    """
    Concept: Validates that proof sketch mode builds barrier escape outline.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    conjectures = {
        "gap_clusters": [{"bridge_id": "bridge.002"}],
        "abstraction_conjectures": [
            {
                "conjecture_id": "conj.002",
                "bridge_id": "bridge.002",
                "abstraction_type": "barrier-escaping-representation",
                "abstraction_label": "natural-proof-resistant PIT certificate",
                "priority": 0.74,
                "gap_target": "barrier-pressure",
                "target_consequence_schema": "Permanent-superpolynomial-lower-bound",
                "preserved_invariant": "PIT certificate soundness",
                "definitional_profile": {"necessary_attributes": []},
                "counterfactual_probes": [
                    {
                        "intervention": "Encode the certificate in the standard natural-proof representation.",
                        "expected_bridge_effect": "bridge-blocked-by-known-barrier",
                    }
                ],
                "barrier_scope": "natural-proofs",
            }
        ],
    }
    strategies = {
        "strategies": [
            {
                "strategy_id": "strat.002",
                "name": "Barrier-Aware Escape around st.def.pit",
                "phase": "Barrier Analysis",
                "anchor_statement_id": "st.def.pit",
                "strategy_score": 0.72,
                "bridge_ids": ["bridge.002"],
                "hypothesis_ids": [],
                "anchor_concepts": ["PIT", "natural-proofs"],
                "bridge_concepts": ["Permanent", "natural-proofs"],
                "abstraction_concepts": ["natural-proof-resistant PIT certificate"],
            }
        ]
    }
    bridges = {
        "bridge_programs": [
            {
                "bridge_id": "bridge.002",
                "from_id": "st.def.pit",
                "to_id": "st.thm.perm",
                "bridge_type": "barrier-aware transfer bridge",
                "inferential_commitment": {
                    "support_antecedent_schema": "PIT-in-P",
                    "target_consequence_schema": "Permanent-superpolynomial-lower-bound",
                    "preserved_invariant": "PIT certificate soundness",
                    "barrier_scope": "natural-proofs",
                },
            }
        ]
    }
    hardness = {
        "anti_barrier_programs": [
            {
                "barrier_family": "natural-proofs",
                "minimal_conceptual_changes": [
                    "replace largeness with certificate-local structure",
                    "encode the argument through PIT-style algebraic witnesses",
                ],
            }
        ]
    }

    report = _build(
        conjectures=conjectures,
        strategies=strategies,
        bridges=bridges,
        phyp={"hypotheses": []},
        analysis={},
        coherence={},
        hardness=hardness,
        top_k=3,
    )

    sketch = report["proof_sketches"][0]
    assert sketch["proof_strategy_family"] == "barrier-escape-reencoding"
    assert sketch["barrier_scope"] == "natural-proofs"
    assert sketch["negative_reasoning_program"]["negative_mode"] == "barrier-impossibility"
    assert sketch["negative_reasoning_program"]["heuristic"]["decision"] == "negative-first"
    assert "blocked by barrier `natural-proofs`" in sketch["negative_reasoning_program"]["impossibility_claim_template"]
    assert any("natural-proofs" in row["condition"] for row in sketch["barrier_checkpoints"])
    assert any("natural-proofs" in row for row in sketch["abort_conditions"])


def test_paper_style_argument_renders_top_route_as_conditional_proof() -> None:
    """
    Concept: Validates that paper style argument renders top route as conditional proof.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    report = _build(
        conjectures={
            "abstraction_conjectures": [
                {
                    "conjecture_id": "conj.001",
                    "bridge_id": "bridge.001",
                    "abstraction_type": "intermediate-complexity-measure",
                    "abstraction_label": "threshold-sensitive MCSP witness family",
                    "mathematical_object_role": "A typed witness family recording near-threshold MCSP hardness data strongly enough to support magnification.",
                    "carrier_kind": "family of instances equipped with a monotone witness measure",
                    "typing_status": "typed",
                    "priority": 0.82,
                    "gap_target": "missing-intermediate-abstraction",
                    "support_antecedent_schema": "MCSP-near-threshold-nonuniform-circuit-lower-bound",
                    "target_consequence_schema": "NP-not-in-P/poly",
                    "preserved_invariant": "MCSP complexity profile",
                    "statement_delta": {
                        "source_claim_focus": "MCSP-near-threshold-nonuniform-circuit-lower-bound",
                        "target_claim_focus": "NP-not-in-P/poly",
                        "model_shift": "nonuniform-circuits -> P/poly",
                        "threshold_shift": "near-threshold lower bound -> major separation consequence",
                        "consequence_shift": "upgrade `MCSP-near-threshold-nonuniform-circuit-lower-bound` into `NP-not-in-P/poly`",
                        "missing_witness_or_transport": "Show that a threshold-sensitive MCSP witness family survives the move from nonuniform circuits to P/poly without losing the MCSP hardness profile.",
                    },
                    "definitional_completeness": 0.76,
                    "counterfactual_sharpness": 0.71,
                    "definitional_profile": {
                        "necessary_attributes": [
                            {
                                "attribute": "admits source-side witness data for `MCSP-near-threshold-nonuniform-circuit-lower-bound`",
                                "kind": "antecedent-realization",
                                "why_it_matters": "The bridge object must absorb the actual source-side hardness theorem rather than merely rename it.",
                            },
                            {
                                "attribute": "preserves the route invariant `MCSP complexity profile`",
                                "kind": "invariant-preservation",
                                "why_it_matters": "The bridge object must preserve the magnification profile that carries the argument.",
                            },
                            {
                                "attribute": "forces the target-side payoff `NP-not-in-P/poly`",
                                "kind": "consequence-forcing",
                                "why_it_matters": "The bridge only matters if it yields the intended separation payoff.",
                            },
                        ],
                        "sufficient_attribute_sets": [
                            {
                                "label": "transport set",
                                "attributes": [
                                    "admits source-side witness data for `MCSP-near-threshold-nonuniform-circuit-lower-bound`",
                                    "preserves the route invariant `MCSP complexity profile`",
                                    "forces the target-side payoff `NP-not-in-P/poly`",
                                ],
                            }
                        ],
                    },
                    "counterfactual_probes": [
                        {
                            "intervention": "Allow `threshold-sensitive MCSP witness family` to ignore the source-side content `MCSP-near-threshold-nonuniform-circuit-lower-bound` and only preserve topical overlap.",
                            "expected_bridge_effect": "bridge-degrades-or-fails",
                            "diagnostic_value": "Checks whether the theorem-pair-specific source content is genuinely needed.",
                        }
                    ],
                }
            ]
        },
        strategies={
            "strategies": [
                {
                    "strategy_id": "strat.001",
                    "name": "Magnification Route",
                    "phase": "Meta-Complexity",
                    "anchor_statement_id": "st.def.magnify",
                    "strategy_score": 0.79,
                    "bridge_ids": ["bridge.001"],
                    "hypothesis_ids": [],
                }
            ]
        },
        bridges={
            "bridge_programs": [
                {
                    "bridge_id": "bridge.001",
                    "from_id": "st.def.magnify",
                    "to_id": "st.thm.magnify",
                    "statement_delta": {
                        "source_claim_focus": "MCSP-near-threshold-nonuniform-circuit-lower-bound",
                        "target_claim_focus": "NP-not-in-P/poly",
                        "model_shift": "nonuniform-circuits -> P/poly",
                        "threshold_shift": "near-threshold lower bound -> major separation consequence",
                        "consequence_shift": "upgrade `MCSP-near-threshold-nonuniform-circuit-lower-bound` into `NP-not-in-P/poly`",
                        "missing_witness_or_transport": "Show that a threshold-sensitive MCSP witness family survives the move from nonuniform circuits to P/poly without losing the MCSP hardness profile.",
                    },
                    "inferential_commitment": {
                        "support_antecedent_schema": "MCSP-near-threshold-nonuniform-circuit-lower-bound",
                        "target_consequence_schema": "NP-not-in-P/poly",
                        "preserved_invariant": "MCSP complexity profile",
                        "barrier_scope": "none",
                    },
                }
            ]
        },
        phyp={"hypotheses": []},
        analysis={},
        coherence={},
        hardness={},
        top_k=1,
    )

    text = _paper_style_argument(
        report,
        kb_statements={
            "st.def.magnify": {
                "id": "st.def.magnify",
                "latex": "A hardness magnification theorem turns barely nontrivial lower bounds for Gap-MCSP into major consequences such as $\\NP\\not\\subseteq\\Ppoly$.",
            },
            "st.thm.magnify": {
                "id": "st.thm.magnify",
                "latex": "In refined regimes, suitable Gap-MCSP lower bounds imply $\\NP\\not\\subseteq\\Ppoly$.",
            },
        },
    )

    assert "# Paper-Style Argument" in text
    assert "## Mathematical Delta" in text
    assert "## Candidate Bridge Object" in text
    assert "## Admissibility Conditions" in text
    assert "## Proposition" in text
    assert "## Proof" in text
    assert "## Failure Diagnosis" in text
    assert "NP-not-in-P/poly" in text
    assert "MCSP complexity profile" in text
    assert "Lemma 1" in text
    assert "Source theorem (`st.def.magnify`)" in text
    assert "Target theorem (`st.thm.magnify`)" in text
    assert "Minimal admissibility conditions" in text
    assert "realizes antecedent schema" not in text
    assert "near-threshold `MCSP` regime" not in text


def test_statement_body_normalizes_noisy_theorem_text() -> None:
    """
    Concept: Validates that proof-sketch theorem excerpts use the shared normalized statement rendering.
    Contribution: Prevents paper-style outputs from leaking raw LaTeX or source-text encoding noise.
    """

    text = _statement_body(
        {
            "latex": r"\MCSP requires circuits of size 2^{\alpha n} \Rightarrow \NP \not\subseteq \Ppoly.",
            "informal": "MCSP Qtext requires circuits of size 2^{alpha n} Rightarrow NP not in P/poly.",
        }
    )

    assert text == "MCSP requires circuits of size 2^ alpha n implies NP not in P/poly."
