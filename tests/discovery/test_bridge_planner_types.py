# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for domain-specific bridge typing in the concept bridge planner.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skills" / "discovery" / "kb-concept-bridge-planner" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from plan_bridges import _build
from plan_bridges import _bridge_type


def test_bridge_type_prefers_yang_mills_domain_specific_families() -> None:
    """
    Concept: Validates that bridge type prefers yang mills domain specific families.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    assert (
        _bridge_type(
            "st.def.os-euclidean-qft",
            "st.def.mass-gap",
            "OS axioms and reflection positivity",
            "Wightman/Hamiltonian mass-gap",
            ["os-to-wightman-to-gap-source"],
            ["os-to-wightman-to-gap-target"],
        )
        == "OS-to-Wightman-to-gap bridge"
    )
    assert (
        _bridge_type(
            "st.thm.transfer-matrix-gap",
            "st.thm.mass-gap",
            "transfer-matrix route",
            "Hamiltonian mass-gap",
            ["transfer-matrix-to-gap-source"],
            ["transfer-matrix-to-gap-target"],
        )
        == "transfer-matrix-to-gap bridge"
    )
    assert (
        _bridge_type(
            "st.thm.correlator-decay",
            "st.def.mass-gap",
            "Euclidean correlator decay",
            "Hamiltonian mass-gap",
            ["correlator-decay-to-gap-source"],
            ["correlator-decay-to-gap-target"],
        )
        == "correlator-decay-to-gap bridge"
    )
    assert (
        _bridge_type(
            "st.rem.continuum-limit-bottleneck",
            "st.thm.constructive-qft",
            "lattice renormalization group",
            "continuum-limit candidate",
            ["continuum-limit-barrier"],
            ["continuum-limit-source"],
        )
        == "continuum-limit bridge"
    )


def test_bridge_plan_emits_mathematical_program_summary() -> None:
    """
    Concept: Validates that bridge plan exposes theorem-shaped mathematical program summaries.
    Contribution: Prevents bridge planning from regressing into execution-only protocol text.
    """

    analysis = {
        "top_interventions": [],
        "connection_candidates": [
            {
                "from_id": "st.def.magnify",
                "to_id": "st.thm.sep",
                "score": 0.72,
                "semantic_score": 0.66,
                "concept_alignment": 0.61,
                "evidence_terms": ["MCSP", "NP-not-in-P/poly"],
                "concept_evidence": ["hardness-magnification", "threshold-gap"],
                "from_profile": {
                    "statement_phase": "Meta-Complexity",
                    "core_problems": ["MCSP"],
                    "model_signatures": ["nonuniform-circuits"],
                    "claim_signatures": ["MCSP-near-threshold-nonuniform-circuit-lower-bound"],
                },
                "to_profile": {
                    "statement_phase": "Lower Bounds",
                    "core_problems": ["P-vs-NP"],
                    "model_signatures": ["P/poly"],
                    "claim_signatures": ["NP-not-in-P/poly"],
                    "consequence_signatures": ["NP-not-in-P/poly"],
                },
            }
        ],
    }
    entrypoints = {"ranked_entrypoints": [{"statement_id": "st.def.magnify", "entry_score": 0.7}]}
    pathways = {"pathways": [{"entry_statement_id": "st.def.magnify", "pathway_score": 0.65}]}
    phyp = {
        "hypotheses": [
            {
                "id": "phyp.001",
                "support_statement_id": "st.def.magnify",
                "target_statement_id": "st.thm.sep",
                "kind": "intermediate-invariant",
                "priority": 0.8,
                "support_antecedent_schema": "MCSP-near-threshold-nonuniform-circuit-lower-bound",
                "target_consequence_schema": "NP-not-in-P/poly",
                "preserved_invariant": "MCSP complexity profile",
                "invariant_basis": ["MCSP", "threshold-gap"],
            }
        ]
    }
    coherence = {
        "coherence_profile": {},
        "hypothesis_coherence": [
            {
                "hypothesis_id": "phyp.001",
                "coherence_delta_global": 0.04,
                "explanatory_power_local": 0.58,
            }
        ],
    }

    report = _build(
        analysis=analysis,
        entrypoints=entrypoints,
        pathways=pathways,
        phyp=phyp,
        coherence=coherence,
        phase_of={"st.def.magnify": "Meta-Complexity", "st.thm.sep": "Lower Bounds"},
        top_k=3,
    )

    top = report["bridge_programs"][0]
    mathematical_program = top["mathematical_program"]
    statement_delta = top["statement_delta"]
    assert "MCSP-near-threshold-nonuniform-circuit-lower-bound" in mathematical_program["source_assumption"]
    assert "NP-not-in-P/poly" in mathematical_program["target_payoff"]
    assert "preserves `MCSP complexity profile`" in mathematical_program["invariant_transport"]
    assert "If one constructs" in mathematical_program["theorem_template"]
    assert statement_delta["source_model"] == "nonuniform-circuits"
    assert statement_delta["target_model"] == "P/poly"
    assert "MCSP" in statement_delta["typed_object_expectation"]
    assert "preserves `MCSP complexity profile`" in statement_delta["missing_witness_or_transport"]
    assert "st.def.magnify" in statement_delta["route_synopsis"]
    assert "st.thm.sep" in statement_delta["route_synopsis"]


def test_bridge_plan_prefers_theorem_body_focus_and_normalized_excerpts() -> None:
    """
    Concept: Validates that bridge planning grounds source and target focus in theorem bodies when KB statements are available.
    Contribution: Prevents route labels and excerpts from regressing to profile-signature placeholders or noisy raw source text.
    """

    analysis = {
        "top_interventions": [],
        "connection_candidates": [
            {
                "from_id": "st.def.magnify",
                "to_id": "st.thm.sep",
                "score": 0.72,
                "semantic_score": 0.66,
                "concept_alignment": 0.61,
                "evidence_terms": ["MCSP", "NP-not-in-P/poly"],
                "concept_evidence": ["hardness-magnification", "threshold-gap"],
                "from_profile": {
                    "statement_phase": "Meta-Complexity",
                    "core_problems": ["MCSP"],
                    "model_signatures": ["nonuniform-circuits"],
                    "claim_signatures": ["MCSP-nonuniform-circuits-lower-bound"],
                },
                "to_profile": {
                    "statement_phase": "Lower Bounds",
                    "core_problems": ["P-vs-NP"],
                    "model_signatures": ["P/poly"],
                    "claim_signatures": ["NP-vs-P/poly-separation"],
                    "consequence_signatures": ["NP-not-in-P/poly"],
                },
            }
        ],
    }
    entrypoints = {"ranked_entrypoints": [{"statement_id": "st.def.magnify", "entry_score": 0.7}]}
    pathways = {"pathways": [{"entry_statement_id": "st.def.magnify", "pathway_score": 0.65}]}
    phyp = {
        "hypotheses": [
            {
                "id": "phyp.001",
                "support_statement_id": "st.def.magnify",
                "target_statement_id": "st.thm.sep",
                "kind": "intermediate-invariant",
                "priority": 0.8,
                "support_antecedent_schema": "MCSP-nonuniform-circuits-lower-bound",
                "target_consequence_schema": "NP-not-in-P/poly",
                "preserved_invariant": "MCSP complexity profile",
                "invariant_basis": ["MCSP", "threshold-gap"],
            }
        ]
    }
    coherence = {
        "coherence_profile": {},
        "hypothesis_coherence": [
            {
                "hypothesis_id": "phyp.001",
                "coherence_delta_global": 0.04,
                "explanatory_power_local": 0.58,
            }
        ],
    }
    kb_statements = {
        "st.def.magnify": {
            "id": "st.def.magnify",
            "latex": r"\MCSP requires circuits of size 2^{\alpha n} \Rightarrow \NP \not\subseteq \Ppoly.",
            "informal": "MCSP Qtext requires circuits of size 2^{alpha n} Rightarrow NP not in P/poly.",
        },
        "st.thm.sep": {
            "id": "st.thm.sep",
            "latex": r"\MCSP requires circuits of size n^{1+\epsilon} \Rightarrow \NP \not\subseteq \Ppoly.",
        },
    }

    report = _build(
        analysis=analysis,
        entrypoints=entrypoints,
        pathways=pathways,
        phyp=phyp,
        coherence=coherence,
        phase_of={"st.def.magnify": "Meta-Complexity", "st.thm.sep": "Lower Bounds"},
        top_k=3,
        kb_statements=kb_statements,
    )

    statement_delta = report["bridge_programs"][0]["statement_delta"]
    assert statement_delta["source_claim_focus"] != "MCSP-nonuniform-circuits-lower-bound"
    assert "MCSP requires circuits of size 2^ alpha n" in statement_delta["source_claim_focus"]
    assert statement_delta["target_claim_focus"] == "NP not in P/poly"
    assert "implies" in statement_delta["source_theorem_excerpt"]
    assert "\\" not in statement_delta["source_theorem_excerpt"]
    assert "Qtext" not in statement_delta["source_theorem_excerpt"]


def test_bridge_plan_deprioritizes_stale_search_space_routes() -> None:
    """
    Concept: Validates that bridge planning reads persisted search-space history and downranks stale exact repeats.
    Contribution: Prevents reruns from repeatedly prioritizing identical stalled routes over unexplored ones.
    """

    analysis = {
        "top_interventions": [],
        "connection_candidates": [
            {
                "from_id": "st.def.magnify",
                "to_id": "st.thm.sep",
                "score": 0.72,
                "semantic_score": 0.66,
                "concept_alignment": 0.61,
                "evidence_terms": ["MCSP", "NP-not-in-P/poly"],
                "concept_evidence": ["hardness-magnification", "threshold-gap"],
                "from_profile": {
                    "statement_phase": "Meta-Complexity",
                    "core_problems": ["MCSP"],
                    "model_signatures": ["nonuniform-circuits"],
                    "claim_signatures": ["MCSP-nonuniform-circuits-lower-bound"],
                },
                "to_profile": {
                    "statement_phase": "Lower Bounds",
                    "core_problems": ["P-vs-NP"],
                    "model_signatures": ["P/poly"],
                    "claim_signatures": ["NP-vs-P/poly-separation"],
                    "consequence_signatures": ["NP-not-in-P/poly"],
                },
            }
        ],
    }
    entrypoints = {"ranked_entrypoints": [{"statement_id": "st.def.magnify", "entry_score": 0.7}]}
    pathways = {"pathways": [{"entry_statement_id": "st.def.magnify", "pathway_score": 0.65}]}
    phyp = {
        "hypotheses": [
            {
                "id": "phyp.001",
                "support_statement_id": "st.def.magnify",
                "target_statement_id": "st.thm.sep",
                "kind": "intermediate-invariant",
                "priority": 0.8,
                "support_antecedent_schema": "MCSP-nonuniform-circuits-lower-bound",
                "target_consequence_schema": "NP-not-in-P/poly",
                "preserved_invariant": "MCSP complexity profile",
                "invariant_basis": ["MCSP", "threshold-gap"],
            }
        ]
    }
    coherence = {
        "coherence_profile": {},
        "hypothesis_coherence": [{"hypothesis_id": "phyp.001", "coherence_delta_global": 0.04, "explanatory_power_local": 0.58}],
    }
    kb_statements = {
        "st.def.magnify": {
            "id": "st.def.magnify",
            "informal": "MCSP requires circuits of size 2^{alpha n} implies NP not in P/poly.",
        },
        "st.thm.sep": {
            "id": "st.thm.sep",
            "informal": "MCSP requires circuits of size n^{1+epsilon} implies NP not in P/poly.",
        },
    }

    baseline = _build(
        analysis=analysis,
        entrypoints=entrypoints,
        pathways=pathways,
        phyp=phyp,
        coherence=coherence,
        phase_of={"st.def.magnify": "Meta-Complexity", "st.thm.sep": "Lower Bounds"},
        top_k=3,
        kb_statements=kb_statements,
    )
    bridge = baseline["bridge_programs"][0]
    state = {
        "metadata": {"kb_ref": "mini"},
        "branches": {
            bridge["search_space_state"]["route_signature"]: {
                "content_fingerprint": bridge["search_space_state"]["content_fingerprint"],
                "latest_outcome": "stalled",
                "visit_count": 3,
                "last_seen_run_id": "old-run",
            }
        },
    }

    revisited = _build(
        analysis=analysis,
        entrypoints=entrypoints,
        pathways=pathways,
        phyp=phyp,
        coherence=coherence,
        phase_of={"st.def.magnify": "Meta-Complexity", "st.thm.sep": "Lower Bounds"},
        top_k=3,
        kb_statements=kb_statements,
        search_space_state=state,
    )

    top = revisited["bridge_programs"][0]
    assert top["effective_bridge_score"] < top["bridge_score"]
    assert top["search_space_state"]["revisit_status"] == "revisited-stalled"
    assert top["signals"]["novelty_signal"] < 1.0
