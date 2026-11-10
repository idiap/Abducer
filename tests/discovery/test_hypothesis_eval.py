# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""
Regression tests for hypothesis evaluation, coherence use, and inferential commitments.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMON = ROOT / "skills" / "common"
if str(COMMON) not in sys.path:
    sys.path.insert(0, str(COMMON))

from hypothesis_eval import evaluate_hypotheses
from hypothesis_eval import is_resolved_status


def test_force_resolution_keeps_provisional_status_unresolved() -> None:
    """
    Concept: Validates that force resolution keeps provisional status unresolved.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    statements = {
        "st.def.a": {
            "id": "st.def.a",
            "kind": "definition",
            "depends_on": [],
            "latex": "A",
            "informal": "A",
        },
        "st.thm.b": {
            "id": "st.thm.b",
            "kind": "theorem",
            "depends_on": [],
            "latex": "B",
            "informal": "B",
        },
    }
    hypotheses = [
        {
            "id": "phyp.test.001",
            "kind": "bridge-link",
            "status": "tentative",
            "priority": 0.5,
            "target_statement_id": "st.thm.b",
            "support_statement_id": "st.def.a",
            "evidence_terms": [],
        }
    ]

    report = evaluate_hypotheses(
        hypotheses=hypotheses,
        statements=statements,
        support_threshold=0.99,
        refute_threshold=0.99,
        margin=0.5,
        force_resolution=True,
    )

    assert report["metadata"]["hypothesis_count"] == 1
    result = report["results"][0]
    assert result["verdict"] in {"provisionally-supported", "provisionally-refuted"}
    assert result["next_status"] in {"provisionally-supported", "provisionally-refuted"}
    assert not is_resolved_status(result["next_status"])


def test_conceptual_hypothesis_uses_coherence_signals() -> None:
    """
    Concept: Validates that conceptual hypothesis uses coherence signals.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    statements = {
        "st.def.a": {
            "id": "st.def.a",
            "kind": "definition",
            "depends_on": [],
            "latex": "A(x)",
            "informal": "Definition A",
        },
        "st.thm.b": {
            "id": "st.thm.b",
            "kind": "theorem",
            "depends_on": ["st.def.a"],
            "latex": "B(x)",
            "informal": "Theorem B",
        },
    }
    hypotheses = [
        {
            "id": "phyp.test.100",
            "kind": "representation-shift",
            "status": "tentative",
            "priority": 0.7,
            "target_statement_id": "st.thm.b",
            "support_statement_id": "st.def.a",
            "provenance": {"analysis_score": 0.8},
        }
    ]

    report = evaluate_hypotheses(
        hypotheses=hypotheses,
        statements=statements,
        coherence_by_hypothesis={
            "phyp.test.100": {
                "explanatory_power_local": 0.75,
                "coherence_delta_global": 0.12,
                "global_coherence_if_accepted": 0.68,
            }
        },
        coherence_profile={"global_coherence": 0.52},
        support_threshold=0.5,
        refute_threshold=0.8,
    )

    assert report["metadata"]["coherence_signal_count"] == 1
    assert report["metadata"]["global_coherence"] == 0.52
    result = report["results"][0]
    assert result["kind"] == "representation-shift"
    assert result["signals"]["explanatory_power_local"] == 0.75
    assert result["signals"]["coherence_delta_global"] == 0.12
    assert "symbol_role_alignment" in result["signals"]
    assert "theorem_family_similarity" in result["signals"]
    assert result["signals"]["semantic_overlap"] >= 0.0
    assert result["support_score"] >= 0.5


def test_bridge_hypothesis_uses_inferential_commitments() -> None:
    """
    Concept: Validates that bridge hypothesis uses inferential commitments.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    statements = {
        "st.thm.karp-lipton": {
            "id": "st.thm.karp-lipton",
            "kind": "theorem",
            "depends_on": [],
            "latex": r"\NP \subseteq \Ppoly \Rightarrow \PH = \Sigma_2^p",
            "informal": "If NP has polynomial-size circuits then the polynomial hierarchy collapses.",
            "method_tags": ["circuit-complexity"],
            "notes": "nonuniform collapse theorem",
        },
        "st.thm.ph-collapse": {
            "id": "st.thm.ph-collapse",
            "kind": "theorem",
            "depends_on": [],
            "latex": r"\PH = \Sigma_2^p",
            "informal": "The polynomial hierarchy collapses to Sigma_2^p.",
            "method_tags": ["circuit-complexity"],
            "notes": "collapse consequence",
        },
    }
    hypotheses = [
        {
            "id": "phyp.test.200",
            "kind": "bridge-link",
            "status": "tentative",
            "priority": 0.7,
            "target_statement_id": "st.thm.ph-collapse",
            "support_statement_id": "st.thm.karp-lipton",
            "support_antecedent_schema": "NP-in-P/poly",
            "target_consequence_schema": "PH-collapse-to-Sigma2",
            "preserved_invariant": "P-vs-NP semantic object",
            "barrier_scope": "relativization",
            "provenance": {"analysis_score": 0.6},
        }
    ]

    report = evaluate_hypotheses(
        hypotheses=hypotheses,
        statements=statements,
        support_threshold=0.5,
        refute_threshold=0.8,
    )

    result = report["results"][0]
    assert result["signals"]["antecedent_alignment"] > 0.0
    assert result["signals"]["consequence_alignment"] > 0.0
    assert result["signals"]["commitment_support"] > 0.0
    assert result["inferential_commitment"]["target_consequence_schema"] == "PH-collapse-to-Sigma2"
    assert any("support antecedent schema grounded" in reason for reason in result["reasons"])


def test_bridge_hypothesis_can_support_novel_edge_without_authored_dependency() -> None:
    """
    Concept: Validates that structurally strong novel bridges can be supported even when the edge is not already authored in the KB.
    Contribution: Prevents discovery-mode evaluation from requiring explicit dependencies that are intentionally hidden under simulated ignorance.
    """

    statements = {
        "st.def.generator": {
            "id": "st.def.generator",
            "kind": "definition",
            "depends_on": [],
            "latex": r"For a C_0-semigroup, Ax := \lim_{h \downarrow 0} (T(h)x-x)/h.",
            "informal": "The generator is the right derivative at time zero of the semigroup orbit.",
            "used_symbols": ["sym.A", "sym.Tt"],
            "concept_roles": ["cnc.generator", "cnc.c0-semigroup"],
            "method_tags": ["laplace-transform"],
        },
        "st.thm.hille-yosida": {
            "id": "st.thm.hille-yosida",
            "kind": "theorem",
            "depends_on": [],
            "latex": r"A generates a C_0-semigroup iff A is closed, D(A) is dense, and the resolvent powers satisfy the Hille-Yosida bounds.",
            "informal": "Hille-Yosida characterizes generators of exponentially bounded C0 semigroups.",
            "used_symbols": ["sym.A", "sym.Tt", "sym.lambda"],
            "concept_roles": ["cnc.generator", "cnc.c0-semigroup", "cnc.resolvent-bounds"],
            "method_tags": ["resolvent-estimate", "laplace-transform"],
            "notes": "The proof uses Yosida approximations built from resolvents.",
        },
    }
    hypotheses = [
        {
            "id": "phyp.test.300",
            "kind": "bridge-link",
            "status": "tentative",
            "priority": 0.8,
            "target_statement_id": "st.thm.hille-yosida",
            "support_statement_id": "st.def.generator",
            "support_antecedent_schema": "c0-semigroup-definition",
            "target_consequence_schema": "generator-of-exponentially-bounded-c0-semigroup",
            "preserved_invariant": "Yosida approximation convergence in unbounded-generator-graph",
            "barrier_scope": "powers-of-resolvent-verification",
            "provenance": {"analysis_score": 0.62},
        }
    ]

    report = evaluate_hypotheses(
        hypotheses=hypotheses,
        statements=statements,
        support_threshold=0.6,
        refute_threshold=0.8,
    )

    result = report["results"][0]
    assert result["signals"]["direct_dependency"] == 0.0
    assert result["signals"]["novel_bridge_support"] > 0.0
    assert result["support_score"] > 0.5
    assert any("novel bridge is structurally well-supported" in reason for reason in result["reasons"])
