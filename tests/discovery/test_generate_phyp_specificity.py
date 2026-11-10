# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""
Regression tests for proof-hypothesis specificity and domain-aware template generation.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONNECTOR_SCRIPTS = ROOT / "skills" / "discovery" / "kb-proof-connector" / "scripts"
if str(CONNECTOR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(CONNECTOR_SCRIPTS))

from generate_phyp import build_hypotheses


def test_build_hypotheses_includes_inferential_commitments() -> None:
    """
    Concept: Validates that build hypotheses includes inferential commitments.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    analysis = {
        "connection_candidates": [
            {
                "from_id": "st.thm.karp-lipton",
                "to_id": "st.thm.major-separation",
                "score": 0.82,
                "similarity": 0.71,
                "component_gain": 0.4,
                "relation": "potential-support",
                "evidence_terms": ["karp-lipton", "nonuniform", "hierarchy"],
                "specific_evidence": ["NP-in-P/poly-implies-PH-collapse", "PH-collapse-to-Sigma2"],
                "from_profile": {
                    "antecedent_signatures": ["NP-in-P/poly"],
                    "implication_signatures": ["NP-in-P/poly-implies-PH-collapse"],
                    "claim_signatures": ["PH-collapse"],
                    "model_signatures": ["nonuniform-circuits"],
                    "core_problems": ["P-vs-NP"],
                    "complexity_classes": ["NP", "PH"],
                    "barrier_signals": ["relativization"],
                },
                "to_profile": {
                    "consequence_signatures": ["PH-collapse-to-Sigma2"],
                    "claim_signatures": ["major-separation"],
                    "model_signatures": ["nonuniform-circuits"],
                    "core_problems": ["P-vs-NP"],
                    "complexity_classes": ["PH", "Sigma2"],
                    "barrier_signals": ["relativization"],
                },
            }
        ],
        "top_interventions": [],
    }
    statement_map = {
        "st.thm.karp-lipton": {
            "id": "st.thm.karp-lipton",
            "kind": "theorem",
            "informal": "If NP has polynomial-size circuits, the polynomial hierarchy collapses.",
            "latex": r"\NP \subseteq \Ppoly \Rightarrow \PH = \Sigma_2^p",
        },
        "st.thm.major-separation": {
            "id": "st.thm.major-separation",
            "kind": "theorem",
            "informal": "A major separation follows if the collapse route is established.",
            "latex": r"\PH = \Sigma_2^p",
        },
    }

    hypotheses = build_hypotheses(
        analysis=analysis,
        statement_map=statement_map,
        kb_slug="mini",
        top_links=1,
        top_interventions=0,
        top_conceptual=1,
    )

    bridge = next(item for item in hypotheses if item["kind"] == "bridge-link")
    assert bridge["support_antecedent_schema"] == "NP-in-P/poly"
    assert bridge["target_consequence_schema"] == "PH-collapse-to-Sigma2"
    assert "P-vs-NP complexity profile in nonuniform-circuits" == bridge["preserved_invariant"]
    assert bridge["barrier_scope"] == "relativization"

    conceptual = next(item for item in hypotheses if item["kind"] in {"intermediate-invariant", "barrier-escape-principle"})
    assert conceptual["preserved_invariant"] == bridge["preserved_invariant"]
    assert conceptual["barrier_scope"] == "relativization"


def test_build_hypotheses_prefers_specific_signatures_over_generic_labels() -> None:
    """
    Concept: Validates that build hypotheses prefers specific signatures over generic labels.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    analysis = {
        "connection_candidates": [
            {
                "from_id": "st.def.hm",
                "to_id": "st.thm.hm",
                "score": 0.8,
                "similarity": 0.7,
                "component_gain": 0.5,
                "relation": "definitional-expansion",
                "evidence_terms": ["MCSP", "magnification"],
                "specific_evidence": ["MCSP-near-threshold-nonuniform-circuit-lower-bound", "NP-vs-P/poly-separation"],
                "from_profile": {
                    "antecedent_signatures": ["mild-lower-bound", "MCSP-near-threshold-nonuniform-circuit-lower-bound"],
                    "claim_signatures": ["hardness-magnification"],
                    "model_signatures": ["nonuniform-circuits"],
                    "core_problems": ["MCSP"],
                    "complexity_classes": ["NP", "P/poly"],
                    "barrier_signals": [],
                },
                "to_profile": {
                    "consequence_signatures": ["major-separation", "NP-vs-P/poly-separation"],
                    "claim_signatures": ["NP-vs-P/poly-separation"],
                    "model_signatures": ["nonuniform-circuits"],
                    "core_problems": ["MCSP"],
                    "complexity_classes": ["NP", "P/poly"],
                    "barrier_signals": [],
                },
            }
        ],
        "top_interventions": [],
    }
    statement_map = {
        "st.def.hm": {"id": "st.def.hm", "kind": "definition", "informal": "Hardness magnification definition.", "latex": "HM"},
        "st.thm.hm": {"id": "st.thm.hm", "kind": "theorem", "informal": "Magnification theorem.", "latex": "THM"},
    }

    hypotheses = build_hypotheses(
        analysis=analysis,
        statement_map=statement_map,
        kb_slug="mini",
        top_links=1,
        top_interventions=0,
        top_conceptual=0,
    )

    bridge = hypotheses[0]
    assert bridge["support_antecedent_schema"] == "MCSP-near-threshold-nonuniform-circuit-lower-bound"
    assert bridge["target_consequence_schema"] == "NP-vs-P/poly-separation"


def test_build_hypotheses_uses_transfer_matrix_subfamily_metadata() -> None:
    """
    Concept: Validates that build hypotheses uses transfer matrix subfamily metadata.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    analysis = {
        "connection_candidates": [
            {
                "from_id": "st.thm.transfer-matrix",
                "to_id": "st.thm.mass-gap",
                "score": 0.77,
                "similarity": 0.66,
                "component_gain": 0.4,
                "relation": "definitional-expansion",
                "evidence_terms": ["transfer-matrix", "mass-gap"],
                "specific_evidence": ["reflection-positivity-and-transfer-matrix", "positive-mass-gap"],
                "from_profile": {
                    "ontology_profile": "mathematical-physics",
                    "statement_phase": "mass-gap-and-spectral-transfer",
                    "bridge_roles": ["transfer-matrix-to-gap-source"],
                    "antecedent_signatures": ["reflection-positivity-and-transfer-matrix"],
                    "claim_signatures": ["reflection-positivity-transfer"],
                    "model_signatures": ["reflection-positive-transfer-matrix"],
                    "core_problems": ["mass-gap"],
                    "complexity_classes": [],
                    "barrier_signals": ["continuum-limit"],
                },
                "to_profile": {
                    "ontology_profile": "mathematical-physics",
                    "statement_phase": "wightman-hamiltonian-framework",
                    "bridge_roles": ["transfer-matrix-to-gap-target"],
                    "consequence_signatures": ["positive-mass-gap"],
                    "claim_signatures": ["mass-gap"],
                    "model_signatures": ["Hamiltonian-mass-gap"],
                    "core_problems": ["mass-gap"],
                    "complexity_classes": [],
                    "barrier_signals": ["continuum-limit"],
                },
            }
        ],
        "top_interventions": [],
    }
    statement_map = {
        "st.thm.transfer-matrix": {"id": "st.thm.transfer-matrix", "kind": "theorem", "informal": "Transfer matrix theorem.", "latex": "TM"},
        "st.thm.mass-gap": {"id": "st.thm.mass-gap", "kind": "theorem", "informal": "Mass gap theorem.", "latex": "MG"},
    }

    hypotheses = build_hypotheses(
        analysis=analysis,
        statement_map=statement_map,
        kb_slug="yang-mills-test",
        top_links=1,
        top_interventions=0,
        top_conceptual=0,
    )

    bridge = hypotheses[0]
    assert bridge["template_family"] == "transfer-matrix-to-gap-bridge"
    assert bridge["preserved_invariant"] == "transfer-matrix spectral witness in Hamiltonian-mass-gap"
    assert "complexity profile" not in bridge["preserved_invariant"]
    assert "transfer-matrix-to-gap bridge" in bridge["informal"]


def test_build_hypotheses_emits_correlator_decay_subfamily() -> None:
    """
    Concept: Validates that build hypotheses emits correlator decay subfamily.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    analysis = {
        "connection_candidates": [
            {
                "from_id": "st.thm.decay",
                "to_id": "st.def.mass-gap",
                "score": 0.75,
                "similarity": 0.65,
                "component_gain": 0.38,
                "relation": "potential-support",
                "evidence_terms": ["correlator-decay", "mass-gap"],
                "specific_evidence": ["correlator-decay-signals-mass-gap", "positive-mass-gap"],
                "from_profile": {
                    "ontology_profile": "mathematical-physics",
                    "statement_phase": "mass-gap-and-spectral-transfer",
                    "bridge_roles": ["correlator-decay-to-gap-source"],
                    "antecedent_signatures": ["correlator-decay-signals-mass-gap"],
                    "claim_signatures": ["correlator-decay"],
                    "model_signatures": ["Schwinger-function-decay"],
                    "core_problems": ["mass-gap"],
                    "barrier_signals": ["continuum-limit"],
                },
                "to_profile": {
                    "ontology_profile": "mathematical-physics",
                    "statement_phase": "wightman-hamiltonian-framework",
                    "bridge_roles": ["correlator-decay-to-gap-target"],
                    "consequence_signatures": ["positive-mass-gap"],
                    "claim_signatures": ["mass-gap"],
                    "model_signatures": ["Hamiltonian-mass-gap"],
                    "core_problems": ["mass-gap"],
                    "barrier_signals": ["continuum-limit"],
                },
            }
        ],
        "top_interventions": [],
    }
    statement_map = {
        "st.thm.decay": {"id": "st.thm.decay", "kind": "theorem", "informal": "Decay theorem.", "latex": "DECAY"},
        "st.def.mass-gap": {"id": "st.def.mass-gap", "kind": "definition", "informal": "Mass gap definition.", "latex": "MG"},
    }

    hypotheses = build_hypotheses(
        analysis=analysis,
        statement_map=statement_map,
        kb_slug="yang-mills-test",
        top_links=1,
        top_interventions=0,
        top_conceptual=1,
    )

    bridge = next(item for item in hypotheses if item["kind"] == "bridge-link")
    assert bridge["template_family"] == "correlator-decay-to-gap-bridge"
    assert bridge["preserved_invariant"] == "correlator-decay mass-gap witness in Hamiltonian-mass-gap"


def test_build_hypotheses_emits_os_to_wightman_to_gap_subfamily() -> None:
    """
    Concept: Validates that build hypotheses emits os to wightman to gap subfamily.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    analysis = {
        "connection_candidates": [
            {
                "from_id": "st.thm.os-reconstruction",
                "to_id": "st.def.mass-gap",
                "score": 0.81,
                "similarity": 0.7,
                "component_gain": 0.42,
                "relation": "potential-support",
                "evidence_terms": ["OS-Euclidean-QFT", "Wightman-QFT", "mass-gap"],
                "specific_evidence": ["OS-axioms-imply-Wightman-QFT", "positive-mass-gap"],
                "from_profile": {
                    "ontology_profile": "mathematical-physics",
                    "statement_phase": "wightman-hamiltonian-framework",
                    "bridge_roles": ["os-to-wightman-to-gap-bridge"],
                    "antecedent_signatures": ["OS-axioms-and-reflection-positivity"],
                    "claim_signatures": ["OS-reconstruction"],
                    "model_signatures": ["OS-Euclidean-QFT"],
                    "core_problems": ["mass-gap", "Wightman-QFT"],
                    "barrier_signals": ["continuum-limit"],
                },
                "to_profile": {
                    "ontology_profile": "mathematical-physics",
                    "statement_phase": "wightman-hamiltonian-framework",
                    "bridge_roles": ["os-to-wightman-to-gap-target"],
                    "consequence_signatures": ["positive-mass-gap"],
                    "claim_signatures": ["mass-gap"],
                    "model_signatures": ["Wightman-QFT"],
                    "core_problems": ["mass-gap", "Wightman-QFT"],
                    "barrier_signals": ["continuum-limit"],
                },
            }
        ],
        "top_interventions": [],
    }
    statement_map = {
        "st.thm.os-reconstruction": {"id": "st.thm.os-reconstruction", "kind": "theorem", "informal": "OS reconstruction theorem.", "latex": "OS"},
        "st.def.mass-gap": {"id": "st.def.mass-gap", "kind": "definition", "informal": "Mass gap definition.", "latex": "MG"},
    }

    hypotheses = build_hypotheses(
        analysis=analysis,
        statement_map=statement_map,
        kb_slug="yang-mills-test",
        top_links=1,
        top_interventions=0,
        top_conceptual=1,
    )

    bridge = next(item for item in hypotheses if item["kind"] == "bridge-link")
    assert bridge["template_family"] == "os-to-wightman-to-gap-bridge"
    assert bridge["preserved_invariant"] == "OS-to-Wightman mass-gap transfer in Wightman-QFT"


def test_build_hypotheses_emits_os_reconstruction_template() -> None:
    """
    Concept: Validates that build hypotheses emits os reconstruction template.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    analysis = {
        "connection_candidates": [
            {
                "from_id": "st.def.os",
                "to_id": "st.thm.os-reconstruction",
                "score": 0.79,
                "similarity": 0.72,
                "component_gain": 0.41,
                "relation": "definitional-expansion",
                "evidence_terms": ["OS-Euclidean-QFT", "Wightman-QFT"],
                "specific_evidence": ["OS-axioms-imply-Wightman-QFT", "Wightman-QFT-realization"],
                "from_profile": {
                    "ontology_profile": "mathematical-physics",
                    "antecedent_signatures": ["OS-axioms-and-reflection-positivity"],
                    "claim_signatures": ["OS-reconstruction"],
                    "model_signatures": ["OS-Euclidean-QFT"],
                    "core_problems": ["OS-axioms", "Wightman-QFT"],
                    "barrier_signals": [],
                },
                "to_profile": {
                    "ontology_profile": "mathematical-physics",
                    "consequence_signatures": ["Wightman-QFT-realization"],
                    "claim_signatures": ["OS-reconstruction"],
                    "model_signatures": ["Wightman-QFT"],
                    "core_problems": ["OS-axioms", "Wightman-QFT"],
                    "barrier_signals": [],
                },
            }
        ],
        "top_interventions": [],
    }
    statement_map = {
        "st.def.os": {"id": "st.def.os", "kind": "definition", "informal": "OS axioms.", "latex": "OS"},
        "st.thm.os-reconstruction": {
            "id": "st.thm.os-reconstruction",
            "kind": "theorem",
            "informal": "OS reconstruction yields a Wightman theory.",
            "latex": "OS \\Rightarrow W",
        },
    }

    hypotheses = build_hypotheses(
        analysis=analysis,
        statement_map=statement_map,
        kb_slug="yang-mills-test",
        top_links=1,
        top_interventions=0,
        top_conceptual=1,
    )

    bridge = next(item for item in hypotheses if item["kind"] == "bridge-link")
    conceptual = next(item for item in hypotheses if item["kind"] == "representation-shift")

    assert bridge["template_family"] == "os-reconstruction-bridge"
    assert bridge["preserved_invariant"] == "OS reconstruction interface in Wightman-QFT"
    assert "OS-reconstruction bridge" in bridge["informal"]
    assert conceptual["template_family"] == "os-reconstruction-bridge"
