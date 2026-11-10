# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for conjecture-mode abstraction generation and definitional reasoning.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skills" / "discovery" / "kb-gap-abstraction-conjecturer" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from conjecture_gap_abstractions import _build


def test_conjecture_mode_recovers_magnification_abstractions() -> None:
    """
    Concept: Validates that conjecture mode recovers magnification abstractions.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    analysis = {
        "top_interventions": [],
        "connection_candidates": [
            {
                "from_id": "st.def.magnify",
                "to_id": "st.thm.sep",
                "from_profile": {
                    "core_problems": ["MCSP"],
                    "model_signatures": ["nonuniform-circuits"],
                    "antecedent_signatures": ["nonuniform-circuit-exponential-lower-bound"],
                    "claim_signatures": ["MCSP-nonuniform-circuits-lower-bound"],
                    "consequence_signatures": ["restricted-model-lower-bound"],
                },
                "to_profile": {
                    "core_problems": ["MCSP"],
                    "model_signatures": ["P/poly"],
                    "claim_signatures": ["NP-vs-P/poly-separation"],
                    "consequence_signatures": ["NP-not-in-P/poly"],
                },
            }
        ],
    }
    entrypoints = {"ranked_entrypoints": []}
    pathways = {
        "pathways": [
            {
                "supporting_links": [{"from_id": "st.def.magnify", "to_id": "st.thm.sep"}],
            }
        ]
    }
    bridges = {
        "bridge_programs": [
            {
                "bridge_id": "bridge.001",
                "from_id": "st.def.magnify",
                "to_id": "st.thm.sep",
                "bridge_type": "magnification bridge",
                "bridge_score": 0.74,
                "concept_evidence": ["MCSP", "hardness-magnification"],
                "evidence_terms": ["MCSP", "NP-not-in-P/poly"],
                "statement_delta": {
                    "source_claim_focus": "nonuniform-circuit-exponential-lower-bound",
                    "target_claim_focus": "NP-not-in-P/poly",
                    "model_shift": "nonuniform-circuits -> P/poly",
                    "threshold_shift": "exponential lower bound -> major separation consequence",
                    "consequence_shift": "upgrade `nonuniform-circuit-exponential-lower-bound` into `NP-not-in-P/poly`",
                    "missing_witness_or_transport": "Show that an MCSP witness family survives the move from nonuniform circuits to P/poly without losing the MCSP complexity profile.",
                },
                "inferential_commitment": {
                    "support_antecedent_schema": "nonuniform-circuit-exponential-lower-bound",
                    "target_consequence_schema": "NP-not-in-P/poly",
                    "preserved_invariant": "MCSP complexity profile in nonuniform-circuits",
                    "invariant_basis": ["MCSP", "nonuniform-circuits"],
                    "barrier_scope": "none",
                },
            }
        ]
    }
    phyp = {
        "hypotheses": [
            {
                "support_statement_id": "st.def.magnify",
                "target_statement_id": "st.thm.sep",
                "kind": "intermediate-invariant",
            }
        ]
    }

    report = _build(
        analysis=analysis,
        entrypoints=entrypoints,
        pathways=pathways,
        bridges=bridges,
        phyp=phyp,
        hardness={},
        top_bridges=4,
        max_conjectures_per_bridge=3,
    )

    gap_axes = [row["axis"] for row in report["gap_clusters"][0]["gap_axes"]]
    abstraction_types = {row["abstraction_type"] for row in report["abstraction_conjectures"]}
    top_row = report["abstraction_conjectures"][0]
    definitional = top_row["definitional_profile"]
    mathematical_spec = top_row["mathematical_specification"]
    necessary_kinds = {row["kind"] for row in definitional["necessary_attributes"]}
    counterfactual = top_row["counterfactual_probes"][0]

    assert "model-mismatch" in gap_axes
    assert "implication-lift" in gap_axes
    assert "intermediate-complexity-measure" in abstraction_types
    assert "surrogate-promise-problem" in abstraction_types
    assert "invariant-preservation" in necessary_kinds
    assert "consequence-forcing" in necessary_kinds
    assert top_row["carrier_kind"]
    assert top_row["typing_status"] == "typed"
    assert "complexity potential" not in top_row["abstraction_label"].lower()
    assert top_row["statement_delta"]["model_shift"] == "nonuniform-circuits -> P/poly"
    assert top_row["counterfactual_probes"][0]["expected_bridge_effect"] == "bridge-degrades-or-fails"
    assert counterfactual["diagnostic_value"]
    assert "If such a" in mathematical_spec["conditional_claim"]
    assert mathematical_spec["carrier_kind"] == top_row["carrier_kind"]
    assert mathematical_spec["statement_delta"]["model_shift"] == "nonuniform-circuits -> P/poly"
    assert any("Source-to-object claim" in row for row in mathematical_spec["proof_obligation_templates"])



def test_conjecture_mode_emits_barrier_escape_abstraction() -> None:
    """
    Concept: Validates that conjecture mode emits barrier escape abstraction.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    analysis = {
        "top_interventions": [],
        "connection_candidates": [
            {
                "from_id": "st.def.bridge",
                "to_id": "st.thm.target",
                "from_profile": {
                    "core_problems": ["PIT"],
                    "model_signatures": ["arithmetic-circuits"],
                    "antecedent_signatures": ["PIT-in-P"],
                    "claim_signatures": ["derandomization"],
                    "barrier_signals": ["natural-proofs"],
                },
                "to_profile": {
                    "core_problems": ["Permanent"],
                    "model_signatures": ["arithmetic-circuits"],
                    "claim_signatures": ["Permanent-lower-bound"],
                    "consequence_signatures": ["Permanent-superpolynomial-lower-bound"],
                    "barrier_signals": ["natural-proofs"],
                },
            }
        ],
    }
    bridges = {
        "bridge_programs": [
            {
                "bridge_id": "bridge.002",
                "from_id": "st.def.bridge",
                "to_id": "st.thm.target",
                "bridge_type": "barrier-aware transfer bridge",
                "bridge_score": 0.61,
                "concept_evidence": ["PIT", "Permanent", "natural-proofs"],
                "inferential_commitment": {
                    "support_antecedent_schema": "PIT-in-P",
                    "target_consequence_schema": "Permanent-superpolynomial-lower-bound",
                    "preserved_invariant": "support interface",
                    "invariant_basis": ["PIT"],
                    "barrier_scope": "natural-proofs",
                },
            }
        ]
    }
    report = _build(
        analysis=analysis,
        entrypoints={"ranked_entrypoints": []},
        pathways={"pathways": []},
        bridges=bridges,
        phyp={"hypotheses": []},
        hardness={},
        top_bridges=4,
        max_conjectures_per_bridge=3,
    )

    abstraction_types = {row["abstraction_type"] for row in report["abstraction_conjectures"]}
    barrier_rows = [row for row in report["abstraction_conjectures"] if row["abstraction_type"] == "barrier-escaping-representation"]

    assert "barrier-escaping-representation" in abstraction_types
    assert barrier_rows
    necessary = barrier_rows[0]["definitional_profile"]["necessary_attributes"]
    assert any(row["kind"] == "barrier-evasion" for row in necessary)
    assert any(probe["expected_bridge_effect"] == "bridge-blocked-by-known-barrier" for probe in barrier_rows[0]["counterfactual_probes"])


def test_fixed_point_preferred_abstraction_outranks_generic_barrier_escape() -> None:
    """
    Concept: Validates that fixed-point domains prioritize the invariant-subset bridge abstraction over generic barrier escape.
    Contribution: Documents the intended regression boundary so the conjecture layer prefers the mathematically native hidden object when the KB already identifies it.
    """

    analysis = {
        "top_interventions": [],
        "connection_candidates": [
            {
                "from_id": "st.def.fixed-point-subset",
                "to_id": "st.thm.markov-kakutani",
                "from_profile": {
                    "core_problems": ["common-fixed-point"],
                    "model_signatures": ["compact-convex-set", "commuting-affine-family"],
                    "claim_signatures": ["single-map-fixed-point-implies-invariant-fixed-point-subset"],
                    "consequence_signatures": ["nonempty-compact-convex-fixed-point-subset"],
                    "barrier_signals": ["invariant-subset-propagation"],
                },
                "to_profile": {
                    "core_problems": ["common-fixed-point"],
                    "model_signatures": ["compact-convex-set", "commuting-affine-family"],
                    "claim_signatures": ["common-fixed-point-for-commuting-family"],
                    "consequence_signatures": ["common-fixed-point-for-commuting-family"],
                    "barrier_signals": ["invariant-subset-propagation"],
                },
            }
        ],
    }
    bridges = {
        "bridge_programs": [
            {
                "bridge_id": "bridge.fp.001",
                "from_id": "st.def.fixed-point-subset",
                "to_id": "st.thm.markov-kakutani",
                "bridge_type": "structural support bridge",
                "bridge_score": 0.68,
                "concept_evidence": ["invariant-fixed-point-subset", "compact-convex-set", "commuting-family"],
                "evidence_terms": ["common-fixed-point-for-commuting-family", "finite-intersection-property"],
                "inferential_commitment": {
                    "support_antecedent_schema": "single-map-fixed-point-implies-invariant-fixed-point-subset",
                    "target_consequence_schema": "common-fixed-point-for-commuting-family",
                    "preserved_invariant": "support-target interface",
                    "invariant_basis": ["fixed-point subset", "compact convex subset"],
                    "barrier_scope": "invariant-subset-propagation",
                },
            }
        ]
    }
    phyp = {
        "hypotheses": [
            {
                "support_statement_id": "st.def.fixed-point-subset",
                "target_statement_id": "st.thm.markov-kakutani",
                "kind": "barrier-escape-principle",
            }
        ]
    }

    report = _build(
        analysis=analysis,
        entrypoints={"ranked_entrypoints": []},
        pathways={"pathways": []},
        bridges=bridges,
        phyp=phyp,
        hardness={},
        top_bridges=4,
        max_conjectures_per_bridge=3,
    )

    top_row = report["abstraction_conjectures"][0]
    abstraction_types = [row["abstraction_type"] for row in report["abstraction_conjectures"]]

    assert "barrier-escaping-representation" in abstraction_types
    assert top_row["abstraction_type"] == "invariant-fixed-point-core"


def test_conjecture_mode_emits_yang_mills_specific_abstraction_families() -> None:
    """
    Concept: Validates that conjecture mode emits yang mills specific abstraction families.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    analysis = {
        "top_interventions": [],
        "connection_candidates": [
            {
                "from_id": "st.def.os-euclidean-qft",
                "to_id": "st.thm.mass-gap-route",
                "from_profile": {
                    "core_problems": ["OS-axioms", "mass-gap"],
                    "model_signatures": ["OS-Euclidean-QFT", "continuum-limit"],
                    "antecedent_signatures": ["OS-axioms-and-reflection-positivity"],
                    "claim_signatures": ["OS-reconstruction", "reflection-positivity-transfer"],
                    "barrier_signals": ["continuum-limit"],
                },
                "to_profile": {
                    "core_problems": ["Wightman-QFT", "mass-gap"],
                    "model_signatures": ["Wightman-QFT", "Hamiltonian-mass-gap"],
                    "claim_signatures": ["mass-gap"],
                    "consequence_signatures": ["positive-mass-gap", "Wightman-QFT-realization"],
                    "barrier_signals": ["continuum-limit"],
                },
            }
        ],
    }
    bridges = {
        "bridge_programs": [
            {
                "bridge_id": "bridge.ym.001",
                "from_id": "st.def.os-euclidean-qft",
                "to_id": "st.thm.mass-gap-route",
                "bridge_type": "OS-reconstruction bridge",
                "bridge_score": 0.72,
                "concept_evidence": ["OS-Euclidean-QFT", "reflection-positivity", "Wightman-QFT"],
                "evidence_terms": ["mass-gap", "continuum-limit", "transfer-matrix"],
                "inferential_commitment": {
                    "support_antecedent_schema": "OS-axioms-and-reflection-positivity",
                    "target_consequence_schema": "positive-mass-gap",
                    "preserved_invariant": "OS reconstruction interface in Wightman-QFT",
                    "invariant_basis": ["OS-axioms", "Wightman-QFT", "reflection-positivity"],
                    "barrier_scope": "continuum-limit",
                },
            },
            {
                "bridge_id": "bridge.ym.002",
                "from_id": "st.thm.transfer-matrix-gap",
                "to_id": "st.thm.mass-gap-route",
                "bridge_type": "mass-gap transfer bridge",
                "bridge_score": 0.74,
                "concept_evidence": ["transfer-matrix", "mass-gap", "correlator-decay"],
                "evidence_terms": ["positive-mass-gap", "Hamiltonian-mass-gap"],
                "inferential_commitment": {
                    "support_antecedent_schema": "reflection-positivity-and-transfer-matrix",
                    "target_consequence_schema": "positive-mass-gap",
                    "preserved_invariant": "mass-gap witness transfer in Hamiltonian-mass-gap",
                    "invariant_basis": ["mass-gap", "transfer-matrix", "Hamiltonian-mass-gap"],
                    "barrier_scope": "continuum-limit",
                },
            },
            {
                "bridge_id": "bridge.ym.003",
                "from_id": "st.rem.continuum-limit-bottleneck",
                "to_id": "st.thm.mass-gap-route",
                "bridge_type": "continuum-limit bridge",
                "bridge_score": 0.76,
                "concept_evidence": ["continuum-limit", "renormalization-group", "lattice"],
                "evidence_terms": ["cutoff-removal", "mass-gap"],
                "inferential_commitment": {
                    "support_antecedent_schema": "multiscale-renormalization-control",
                    "target_consequence_schema": "rigorous-Yang-Mills-construction",
                    "preserved_invariant": "continuum-limit control in continuum-limit",
                    "invariant_basis": ["continuum-limit", "lattice", "renormalization-group"],
                    "barrier_scope": "continuum-limit",
                },
            },
        ]
    }
    phyp = {
        "hypotheses": [
            {"support_statement_id": "st.def.os-euclidean-qft", "target_statement_id": "st.thm.mass-gap-route", "kind": "representation-shift"},
            {"support_statement_id": "st.thm.transfer-matrix-gap", "target_statement_id": "st.thm.mass-gap-route", "kind": "intermediate-invariant"},
            {"support_statement_id": "st.rem.continuum-limit-bottleneck", "target_statement_id": "st.thm.mass-gap-route", "kind": "barrier-escape-principle"},
        ]
    }

    report = _build(
        analysis=analysis,
        entrypoints={"ranked_entrypoints": []},
        pathways={"pathways": []},
        bridges=bridges,
        phyp=phyp,
        hardness={},
        top_bridges=6,
        max_conjectures_per_bridge=3,
    )

    abstraction_types = {row["abstraction_type"] for row in report["abstraction_conjectures"]}

    assert "os-reconstruction-interface" in abstraction_types
    assert "mass-gap-witness-transfer" in abstraction_types
    assert "continuum-limit-construction" in abstraction_types
    os_row = next(row for row in report["abstraction_conjectures"] if row["abstraction_type"] == "os-reconstruction-interface")
    assert any(attr["kind"] == "reconstruction-law" for attr in os_row["definitional_profile"]["necessary_attributes"])
