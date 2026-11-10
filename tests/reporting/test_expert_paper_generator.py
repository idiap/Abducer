# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for expert paper synthesis and hypothesis recommendation scoring.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills" / "reporting" / "kb-expert-paper-generator" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_expert_paper import _build_report
from generate_expert_paper import _statement_preview


def test_expert_paper_prioritizes_high_signal_hypothesis() -> None:
    """
    Concept: Validates that expert paper scoring prioritizes high support/coherence/leverage hypotheses.
    Contribution: Documents the expected recommendation ordering for controlled signal contrasts.
    """

    phyp = {
        "hypotheses": [
            {
                "id": "phyp.demo.001",
                "kind": "bridge-link",
                "priority": 0.82,
                "status": "tentative",
                "target_statement_id": "st.thm.target-strong",
                "support_statement_id": "st.def.source-strong",
                "informal": "Strong route.",
                "validation_protocol": ["test-1", "test-2"],
                "falsifier": "fails under contradiction probe",
            },
            {
                "id": "phyp.demo.002",
                "kind": "bridge-link",
                "priority": 0.40,
                "status": "tentative",
                "target_statement_id": "st.thm.target-weak",
                "support_statement_id": "st.def.source-weak",
                "informal": "Weak route.",
                "validation_protocol": [],
                "falsifier": "",
            },
        ]
    }
    hypothesis_eval = {
        "results": [
            {
                "hypothesis_id": "phyp.demo.001",
                "target_statement_id": "st.thm.target-strong",
                "support_statement_id": "st.def.source-strong",
                "support_score": 0.82,
                "refute_score": 0.05,
                "confidence": 0.78,
                "verdict": "supported",
                "recommended_action": "promote",
            },
            {
                "hypothesis_id": "phyp.demo.002",
                "target_statement_id": "st.thm.target-weak",
                "support_statement_id": "st.def.source-weak",
                "support_score": 0.35,
                "refute_score": 0.46,
                "confidence": 0.44,
                "verdict": "inconclusive",
                "recommended_action": "retest",
            },
        ]
    }
    coherence = {
        "hypothesis_coherence": [
            {
                "hypothesis_id": "phyp.demo.001",
                "coherence_delta_global": 0.045,
                "explanatory_power_local": 0.55,
            },
            {
                "hypothesis_id": "phyp.demo.002",
                "coherence_delta_global": -0.03,
                "explanatory_power_local": 0.20,
            },
        ]
    }
    analysis = {
        "top_interventions": [
            {"statement_id": "st.thm.target-strong", "score": 0.71},
            {"statement_id": "st.thm.target-weak", "score": 0.29},
        ]
    }
    entrypoints = {
        "ranked_entrypoints": [
            {"statement_id": "st.thm.target-strong", "entry_score": 0.77},
            {"statement_id": "st.thm.target-weak", "entry_score": 0.32},
        ]
    }
    pathways = {
        "pathways": [
            {
                "pathway_score": 0.73,
                "entry_statement_id": "st.thm.target-strong",
                "supporting_hypotheses": [{"id": "phyp.demo.001"}],
                "supporting_links": [
                    {"from_id": "st.def.source-strong", "to_id": "st.thm.target-strong"}
                ],
            },
            {
                "pathway_score": 0.31,
                "entry_statement_id": "st.thm.target-weak",
                "supporting_hypotheses": [{"id": "phyp.demo.002"}],
                "supporting_links": [
                    {"from_id": "st.def.source-weak", "to_id": "st.thm.target-weak"}
                ],
            },
        ]
    }
    bridges = {
        "bridge_programs": [
            {
                "bridge_id": "bridge.001",
                "from_id": "st.def.source-strong",
                "to_id": "st.thm.target-strong",
                "bridge_type": "measure-representation",
                "bridge_score": 0.81,
                "statement_delta": {
                    "source_claim_focus": "positive-functional",
                    "target_claim_focus": "representation-theorem",
                    "model_shift": "function-space duality -> measure representation",
                    "threshold_shift": "bounded positive functional -> representing measure theorem",
                    "consequence_shift": "upgrade `positive-functional` into `representation-theorem`",
                    "missing_witness_or_transport": "Show that positivity determines a countably additive representing measure without losing the functional action.",
                    "route_synopsis": "Move from a positive functional statement to a representing-measure theorem through a typed measure object.",
                },
                "inferential_commitment": {
                    "hypothesis_id": "phyp.demo.001",
                    "support_antecedent_schema": "positive-functional",
                    "target_consequence_schema": "representation-theorem",
                    "preserved_invariant": "positivity",
                    "barrier_scope": "none",
                },
            }
        ]
    }
    conjectures = {
        "gap_clusters": [],
        "abstraction_conjectures": [
            {
                "conjecture_id": "conj.001",
                "bridge_id": "bridge.001",
                "abstraction_type": "measure-representation",
                "abstraction_label": "representing measure",
                "mathematical_object_role": "measure object",
                "carrier_kind": "regular Borel measure on the target compact space",
                "typing_status": "typed",
                "gap_target": "missing-intermediate-abstraction, implication-lift",
                "support_antecedent_schema": "positive-functional",
                "target_consequence_schema": "representation-theorem",
                "preserved_invariant": "positivity",
                "priority": 0.83,
                "mathematical_specification": {
                    "definition_template": "A representing measure object that transports positivity into a representation theorem.",
                    "conditional_claim": "If the representing measure exists and preserves positivity, then the representation theorem follows.",
                    "assumptions": ["`positive-functional` holds in the source regime."],
                    "carrier_kind": "regular Borel measure on the target compact space",
                    "statement_delta": {
                        "source_claim_focus": "positive-functional",
                        "target_claim_focus": "representation-theorem",
                        "model_shift": "function-space duality -> measure representation",
                        "threshold_shift": "bounded positive functional -> representing measure theorem",
                        "consequence_shift": "upgrade `positive-functional` into `representation-theorem`",
                        "missing_witness_or_transport": "Show that positivity determines a countably additive representing measure without losing the functional action.",
                    },
                    "obstruction_template": "Failure mode: the supposed representing measure is only formal and never becomes a countably additive measure carrying the original functional.",
                },
            }
        ],
    }
    hardness = {
        "anti_barrier_programs": [{"barrier_family": "continuum-limit"}],
        "essential_elements": [
            {"name": "Barrier Stack Constraints", "severity": "high", "score": 0.8}
        ],
    }
    revision = {
        "priority_program": [
            {"target_statement_ids": ["st.thm.target-strong"], "revision_id": "rev.001"}
        ],
        "revision_actions": [],
    }
    strategies = {
        "strategies": [
            {
                "strategy_id": "strat.001",
                "strategy_score": 0.76,
                "concept_fertility": 0.61,
                "hypothesis_ids": ["phyp.demo.001"],
            },
            {
                "strategy_id": "strat.002",
                "strategy_score": 0.31,
                "concept_fertility": 0.29,
                "hypothesis_ids": ["phyp.demo.002"],
            },
        ]
    }
    proof_sketches = {
        "metadata": {},
        "proof_sketches": [
            {
                "bridge_id": "bridge.001",
                "conjecture_id": "conj.001",
                "strategy_id": "strat.001",
                "proof_strategy_family": "measure-construction-from-positive-functional",
                "family_rationale": "recover a measure object from positivity and then force the representation theorem",
                "sketch_score": 0.88,
                "support_antecedent_schema": "positive-functional",
                "target_consequence_schema": "representation-theorem",
                "preserved_invariant": "positivity",
                "carrier_kind": "regular Borel measure on the target compact space",
                "typing_status": "typed",
                "statement_delta": {
                    "source_claim_focus": "positive-functional",
                    "target_claim_focus": "representation-theorem",
                    "model_shift": "function-space duality -> measure representation",
                    "threshold_shift": "bounded positive functional -> representing measure theorem",
                    "consequence_shift": "upgrade `positive-functional` into `representation-theorem`",
                    "missing_witness_or_transport": "Show that positivity determines a countably additive representing measure without losing the functional action.",
                },
                "hypothesis_ids": ["phyp.demo.001"],
                "proof_obligations": [{"requirement": "show the representing object is well-defined"}],
                "candidate_lemmas": [{"statement": "Source-to-object lemma: positivity yields a representing measure with the correct functional action."}],
                "proof_outline_steps": [{"objective": "construct the representing measure"}],
                "mathematical_argument": {
                    "bridge_definition": "Treat `representing measure` as the measure object attached to the source-target route.",
                    "proposition": "If the representing measure exists and preserves positivity, then the representation theorem follows.",
                    "assumptions": ["`positive-functional` holds in the source regime.", "The measure preserves positivity."],
                    "carrier_kind": "regular Borel measure on the target compact space",
                    "typing_status": "typed",
                    "statement_delta": {
                        "source_claim_focus": "positive-functional",
                        "target_claim_focus": "representation-theorem",
                        "model_shift": "function-space duality -> measure representation",
                        "threshold_shift": "bounded positive functional -> representing measure theorem",
                        "consequence_shift": "upgrade `positive-functional` into `representation-theorem`",
                        "missing_witness_or_transport": "Show that positivity determines a countably additive representing measure without losing the functional action.",
                    },
                    "failure_mode": "Failure occurs if the representing measure never becomes a countably additive measure carrying the original functional.",
                },
                "counterfactual_test": {
                    "intervention": "remove positivity",
                    "expected_bridge_effect": "bridge-degrades-or-fails",
                    "diagnostic_value": "shows the bridge is not merely topical",
                },
                "abort_conditions": ["abort if the object collapses to a restatement of the theorem"],
            }
        ],
        "recommended_execution_order": [],
    }
    statement_index = {
        "st.thm.target-strong": {"informal": "Strong target theorem."},
        "st.def.source-strong": {"informal": "Strong source definition."},
        "st.thm.target-weak": {"informal": "Weak target theorem."},
        "st.def.source-weak": {"informal": "Weak source definition."},
    }

    report = _build_report(
        kb_ref="demo",
        phyp=phyp,
        hypothesis_eval=hypothesis_eval,
        coherence=coherence,
        analysis=analysis,
        entrypoints=entrypoints,
        pathways=pathways,
        bridges=bridges,
        conjectures=conjectures,
        hardness=hardness,
        revision=revision,
        strategies=strategies,
        proof_sketches=proof_sketches,
        statement_index=statement_index,
        top_k=2,
        min_score=0.30,
        warnings=[],
    )

    recommended = report.get("recommended_hypotheses", [])
    all_rows = report.get("hypothesis_scores", [])
    assert len(recommended) >= 1
    assert len(all_rows) == 2
    assert all_rows[0]["hypothesis_id"] == "phyp.demo.001"
    assert all_rows[0]["scores"]["final"] > all_rows[1]["scores"]["final"]
    assert report.get("recommended_bridges", [])[0]["bridge_id"] == "bridge.001"
    assert "representation theorem follows" in report.get("recommended_bridges", [])[0]["conditional_proposition"]
    assert report.get("generative_function", {}).get("name") == "expert_hypothesis_potential_function"
    assert report.get("bridge_selection_function", {}).get("name") == "expert_bridge_priority_function"
    assert "M_b" in report.get("bridge_selection_function", {}).get("formula", "")
    bridge_signals = report.get("recommended_bridges", [])[0].get("signals", {})
    assert "mathematical_specificity" in bridge_signals
    assert "evidence_signal" in bridge_signals
    assert "sketch_operationalization" in bridge_signals
    assert bridge_signals.get("proof_readiness") == bridge_signals.get("sketch_operationalization")
    assert "## 2. Generative Recommendation Function" in report.get("paper_markdown", "")
    assert "## 3. Main Conceptual Bridges" in report.get("paper_markdown", "")
    assert "mathematical specificity" in report.get("paper_markdown", "")
    assert "Conditional proposition" in report.get("paper_markdown", "")
    assert "Candidate bridge object" in report.get("paper_markdown", "")
    assert "Failure diagnosis" in report.get("paper_markdown", "")
    assert "\\paragraph{Source Theorem}" in report.get("paper_tex", "")
    assert "\\paragraph{Failure Diagnosis}" in report.get("paper_tex", "")
    assert "realizes antecedent schema" not in report.get("paper_markdown", "")
    assert "realizes antecedent schema" not in report.get("paper_tex", "")


def test_statement_preview_normalizes_theorem_excerpt() -> None:
    """
    Concept: Validates that expert-paper statement previews use normalized theorem text.
    Contribution: Prevents the final paper from surfacing raw LaTeX control sequences or encoding noise in theorem excerpts.
    """

    preview = _statement_preview(
        {
            "st.demo": {
                "latex": r"\MCSP requires circuits of size 2^{\alpha n} \Rightarrow \NP \not\subseteq \Ppoly.",
                "informal": "MCSP Qtext requires circuits of size 2^{alpha n} Rightarrow NP not in P/poly.",
            }
        },
        "st.demo",
        limit=220,
    )

    assert preview == "MCSP requires circuits of size 2^ alpha n implies NP not in P/poly."
