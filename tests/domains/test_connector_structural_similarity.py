# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""
Regression tests for structural similarity, ontology routing, and evidence cleanup in the proof connector.

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

from analyze_kb_graph import _clean_evidence_terms
from analyze_kb_graph import analyze_kb


def test_connector_uses_structural_similarity_without_lexical_overlap(tmp_path: Path) -> None:
    """
    Concept: Validates that connector uses structural similarity without lexical overlap.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    kb_path = tmp_path / "structural-only.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.thm.alpha",
                "kind: theorem",
                "status: accepted",
                "latex: A_1(x) \\Rightarrow B_1(x)",
                "informal: unique_alpha_phrase_only",
                "source_ids: []",
                "used_symbols: [SharedConcept]",
                "method_tags: [communication]",
                "depends_on: []",
                "confidence: 0.9",
                "proof_sketch: ''",
                "notes: ''",
                "```",
                "",
                "```yaml",
                "id: st.thm.beta",
                "kind: theorem",
                "status: accepted",
                "latex: C_2(y) \\Rightarrow D_2(y)",
                "informal: unique_beta_phrase_only",
                "source_ids: []",
                "used_symbols: [SharedConcept]",
                "method_tags: [communication]",
                "depends_on: []",
                "confidence: 0.9",
                "proof_sketch: ''",
                "notes: ''",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = analyze_kb(
        kb_path=kb_path,
        top_k=5,
        min_similarity=0.10,
        max_connections=10,
        loop_rounds=1,
        include_statuses={"accepted"},
    )

    assert report["connection_candidates"], "Expected structural candidate despite lexical mismatch."
    top = report["connection_candidates"][0]
    assert top["similarity"] >= 0.10
    assert top["lexical_support_overlap"] <= 0.20


def test_connector_extracts_specific_implication_signatures(tmp_path: Path) -> None:
    """
    Concept: Validates that connector extracts specific implication signatures.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    kb_path = tmp_path / "specific-signatures.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.thm.karp-lipton-test",
                "kind: theorem",
                "status: accepted",
                "latex: If \\\\NP\\\\subseteq \\\\Ppoly, then \\\\PH collapses to \\\\Sigma_2^p.",
                "informal: If NP has polynomial-size circuits then the polynomial hierarchy collapses.",
                "source_ids: []",
                "used_symbols: []",
                "method_tags: [circuit-complexity]",
                "depends_on: []",
                "confidence: 0.9",
                "proof_sketch: ''",
                "notes: 'classic nonuniform consequence'",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = analyze_kb(
        kb_path=kb_path,
        top_k=5,
        min_similarity=0.0,
        max_connections=10,
        loop_rounds=1,
        include_statuses={"accepted"},
    )

    intervention = next(item for item in report["top_interventions"] if item["statement_id"] == "st.thm.karp-lipton-test")
    profile = intervention["concept_profile"]

    assert "PH-collapse" in profile["claim_signatures"]
    assert "NP-in-P/poly-implies-PH-collapse" in profile["implication_signatures"]
    assert "nonuniform-circuits" in profile["model_signatures"]
    assert any(
        node.get("type") == "implication-signature" and node.get("label") == "NP-in-P/poly-implies-PH-collapse"
        for node in report["concept_graph"]["nodes"]
    )


def test_connector_extracts_markov_kakutani_fixed_point_signatures(tmp_path: Path) -> None:
    """
    Concept: Validates that connector extracts fixed-point-theorem signatures for the Markov-Kakutani regime.
    Contribution: Prevents convex fixed-point KBs from collapsing into generic mathematical routing.
    """

    kb_path = tmp_path / "markov-kakutani-mini.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "---",
                "kb_id: markov-kakutani-mini",
                "title: Markov-Kakutani Mini",
                "domain: mathematics",
                "subdomain: functional-analysis-convex-fixed-point",
                "---",
                "",
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.thm.mk",
                "kind: theorem",
                "status: accepted",
                "latex: Every commuting family of continuous affine self-maps on a nonempty compact convex set has a common fixed point.",
                "informal: The Markov-Kakutani theorem lifts single-map fixed-point subsets to a common fixed point for a commuting family.",
                "source_ids: []",
                "used_symbols: []",
                "method_tags: [fixed-point-analysis, commuting-family-analysis]",
                "depends_on: []",
                "confidence: 0.9",
                "proof_sketch: ''",
                "notes: 'finite intersection and invariant fixed-point subset route'",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = analyze_kb(
        kb_path=kb_path,
        top_k=5,
        min_similarity=0.0,
        max_connections=10,
        loop_rounds=1,
        include_statuses={"accepted"},
    )

    intervention = next(item for item in report["top_interventions"] if item["statement_id"] == "st.thm.mk")
    profile = intervention["concept_profile"]

    assert "markov-kakutani-common-fixed-point" in profile["claim_signatures"]
    assert "finite-intersection-property-implies-common-fixed-point" in profile["implication_signatures"]
    assert "common-fixed-point-for-commuting-family" in profile["consequence_signatures"]
    assert "commuting-affine-self-map-family" in profile["model_signatures"]


def test_connector_prefers_specific_lower_bound_consequences(tmp_path: Path) -> None:
    """
    Concept: Validates that connector prefers specific lower bound consequences.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    kb_path = tmp_path / "specific-lower-bounds.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.thm.acc0-lb",
                "kind: theorem",
                "status: accepted",
                "latex: Any ACC^0 circuit for parity requires exponential size.",
                "informal: Parity has exponential-size lower bounds against ACC0 circuits.",
                "source_ids: []",
                "used_symbols: []",
                "method_tags: [circuit-complexity]",
                "depends_on: []",
                "confidence: 0.9",
                "proof_sketch: ''",
                "notes: 'restricted model lower bound'",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = analyze_kb(
        kb_path=kb_path,
        top_k=5,
        min_similarity=0.0,
        max_connections=10,
        loop_rounds=1,
        include_statuses={"accepted"},
    )

    intervention = next(item for item in report["top_interventions"] if item["statement_id"] == "st.thm.acc0-lb")
    profile = intervention["concept_profile"]

    assert "ACC0-lower-bound" in profile["claim_signatures"]
    assert any("ACC0" in item or "PARITY-ACC0-circuits-lower-bound" == item for item in profile["consequence_signatures"])
    assert "restricted-model-lower-bound" not in profile["consequence_signatures"]


def test_connector_preserves_statement_local_phase_and_bridge_roles(tmp_path: Path) -> None:
    """
    Concept: Validates that connector preserves statement local phase and bridge roles.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    kb_path = tmp_path / "yang-mills-metadata.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "---",
                "kb_id: ym-mini",
                "title: Yang-Mills Mini",
                "domain: mathematics",
                "subdomain: mathematical-physics",
                "---",
                "",
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.thm.transfer",
                "kind: theorem",
                "status: accepted",
                "latex: Reflection positivity yields a transfer matrix.",
                "informal: Transfer matrix route toward a mass gap.",
                "source_ids: []",
                "used_symbols: []",
                "depends_on: []",
                "concept_roles: []",
                "statement_phase: mass-gap-and-spectral-transfer",
                "bridge_roles: [transfer-matrix-to-gap-source]",
                "method_tags: []",
                "barrier_family: ''",
                "confidence: 0.9",
                "proof_sketch: ''",
                "notes: ''",
                "```",
                "",
                "```yaml",
                "id: st.def.mass-gap",
                "kind: definition",
                "status: accepted",
                "latex: Positive Hamiltonian mass gap.",
                "informal: Hamiltonian mass gap target.",
                "source_ids: []",
                "used_symbols: []",
                "depends_on: []",
                "concept_roles: []",
                "statement_phase: wightman-hamiltonian-framework",
                "bridge_roles: [transfer-matrix-to-gap-target]",
                "method_tags: []",
                "barrier_family: ''",
                "confidence: 0.9",
                "proof_sketch: ''",
                "notes: ''",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = analyze_kb(
        kb_path=kb_path,
        top_k=5,
        min_similarity=0.05,
        max_connections=10,
        loop_rounds=1,
        include_statuses={"accepted"},
    )

    candidate = report["connection_candidates"][0]
    profiles = {
        candidate["from_id"]: candidate["from_profile"],
        candidate["to_id"]: candidate["to_profile"],
    }
    assert profiles["st.thm.transfer"]["statement_phase"] == "mass-gap-and-spectral-transfer"
    assert "transfer-matrix-to-gap-source" in profiles["st.thm.transfer"]["bridge_roles"]
    assert profiles["st.def.mass-gap"]["statement_phase"] == "wightman-hamiltonian-framework"
    assert "transfer-matrix-to-gap-target" in profiles["st.def.mass-gap"]["bridge_roles"]


def test_connector_uses_mathematical_physics_ontology_without_complexity_leakage(tmp_path: Path) -> None:
    """
    Concept: Validates that connector uses mathematical physics ontology without complexity leakage.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    kb_path = tmp_path / "yang-mills.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "---",
                "kb_id: yang-mills-test",
                "title: Yang-Mills Test",
                "domain: mathematics",
                "subdomain: mathematical-physics",
                "---",
                "",
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.thm.os-gap",
                "kind: theorem",
                "status: accepted",
                "latex: Reflection positivity and the OS axioms yield a Wightman quantum field theory with a positive mass gap when Schwinger functions decay exponentially.",
                "informal: Reflection positivity, OS reconstruction, and exponential correlator decay supply the mass-gap route for constructive Yang-Mills.",
                "source_ids: []",
                "used_symbols: [mass-gap, reflection-positivity]",
                "method_tags: []",
                "depends_on: []",
                "confidence: 0.9",
                "proof_sketch: ''",
                "notes: 'continuum limit remains open'",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = analyze_kb(
        kb_path=kb_path,
        top_k=5,
        min_similarity=0.0,
        max_connections=10,
        loop_rounds=1,
        include_statuses={"accepted"},
    )

    assert report["stats"]["ontology_profile"] == "mathematical-physics"
    intervention = next(item for item in report["top_interventions"] if item["statement_id"] == "st.thm.os-gap")
    profile = intervention["concept_profile"]

    assert profile["complexity_classes"] == []
    assert "OS-reconstruction" in profile["claim_signatures"]
    assert "mass-gap" in profile["claim_signatures"]
    assert "OS-Euclidean-QFT" in profile["model_signatures"]
    assert "Wightman-QFT-realization" in profile["consequence_signatures"]
    assert "continuum-limit" in profile["barrier_signals"]
    assert "E" not in intervention["concept_focus"]
    assert "lower-bound" not in profile["claim_signatures"]


def test_connector_extracts_semigroup_generation_signatures(tmp_path: Path) -> None:
    """
    Concept: Validates that functional-analysis KBs route through a semigroup-specific ontology.
    Contribution: Prevents Hille-Yosida style content from collapsing back into generic mathematical structure labels.
    """

    kb_path = tmp_path / "hille-yosida-mini.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "---",
                "kb_id: hy-mini",
                "title: Hille-Yosida Mini",
                "domain: mathematics",
                "subdomain: functional-analysis-semigroup-theory",
                "---",
                "",
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.thm.hille-yosida-mini",
                "kind: theorem",
                "status: accepted",
                "latex: Let A be a linear operator on a Banach space X. Then A generates a C_0-semigroup iff A is closed, D(A) is dense, and ||(\\\\lambda I-A)^{-n}|| <= M/(\\\\lambda-\\\\omega)^n for all n.",
                "informal: Hille-Yosida characterizes generators of exponentially bounded C0 semigroups by closure, density, and resolvent power bounds.",
                "source_ids: []",
                "used_symbols: [sym.A, sym.lambda, sym.X]",
                "depends_on: []",
                "concept_roles: [cnc.c0-semigroup, cnc.generator, cnc.resolvent-bounds]",
                "statement_phase: core-generation-theorem",
                "bridge_roles: [core-characterization]",
                "method_tags: [resolvent-estimate, laplace-transform]",
                "barrier_family: powers-of-resolvent-verification",
                "confidence: 0.95",
                "proof_sketch: The proof uses Yosida approximations built from resolvents.",
                "notes: Resolvent powers are the hard part to verify directly.",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = analyze_kb(
        kb_path=kb_path,
        top_k=5,
        min_similarity=0.0,
        max_connections=10,
        loop_rounds=1,
        include_statuses={"accepted"},
    )

    intervention = next(item for item in report["top_interventions"] if item["statement_id"] == "st.thm.hille-yosida-mini")
    profile = intervention["concept_profile"]

    assert report["stats"]["ontology_profile"] == "functional-analysis-semigroup"
    assert "semigroup-generation-characterization" in profile["claim_signatures"]
    assert "closed-dense-plus-resolvent-powers-imply-c0-generation" in profile["implication_signatures"]
    assert "closed-dense-operator-with-resolvent-power-bounds" in profile["antecedent_signatures"]
    assert "generator-of-exponentially-bounded-c0-semigroup" in profile["consequence_signatures"]
    assert "resolvent-generation-criterion" in profile["model_signatures"]


def test_connector_orients_profiles_with_candidate_direction(tmp_path: Path) -> None:
    """
    Concept: Validates that oriented connector edges carry the matching source and target profiles.
    Contribution: Prevents later bridge generation from using reversed mathematical commitments.
    """

    kb_path = tmp_path / "hille-yosida-orientation.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "---",
                "kb_id: hy-orientation",
                "title: Hille-Yosida Orientation",
                "domain: mathematics",
                "subdomain: functional-analysis-semigroup-theory",
                "---",
                "",
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.prop.regularity",
                "kind: proposition",
                "status: accepted",
                "latex: If A is the generator of a C_0-semigroup then A is closed and D(A) is dense.",
                "informal: Generator regularity gives closure and density.",
                "source_ids: []",
                "used_symbols: [sym.A]",
                "depends_on: []",
                "concept_roles: [cnc.generator]",
                "statement_phase: foundational-regularity",
                "bridge_roles: []",
                "method_tags: [laplace-transform]",
                "barrier_family: domain-closure-density",
                "confidence: 0.95",
                "proof_sketch: ''",
                "notes: ''",
                "```",
                "",
                "```yaml",
                "id: st.thm.general",
                "kind: theorem",
                "status: accepted",
                "latex: A generates a C_0-semigroup iff A is closed, D(A) is dense, and the resolvent powers satisfy the Hille-Yosida bounds.",
                "informal: The general Hille-Yosida theorem characterizes semigroup generators via closure, density, and resolvent powers.",
                "source_ids: []",
                "used_symbols: [sym.A]",
                "depends_on: []",
                "concept_roles: [cnc.c0-semigroup, cnc.generator, cnc.resolvent-bounds]",
                "statement_phase: core-generation-theorem",
                "bridge_roles: []",
                "method_tags: [resolvent-estimate, laplace-transform]",
                "barrier_family: powers-of-resolvent-verification",
                "confidence: 0.95",
                "proof_sketch: ''",
                "notes: ''",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = analyze_kb(
        kb_path=kb_path,
        top_k=5,
        min_similarity=0.0,
        max_connections=10,
        loop_rounds=1,
        include_statuses={"accepted"},
    )

    candidate = report["connection_candidates"][0]
    if candidate["from_id"] == "st.thm.general":
        assert "resolvent-generation-criterion" in candidate["from_profile"]["model_signatures"]
        assert "generator-closed-dense" in candidate["to_profile"]["claim_signatures"]
    else:
        assert candidate["from_id"] == "st.prop.regularity"
        assert "generator-closed-dense" in candidate["from_profile"]["claim_signatures"]
        assert "resolvent-generation-criterion" in candidate["to_profile"]["model_signatures"]


def test_connector_keeps_strong_intra_component_bridges_when_cross_component_candidates_exist(tmp_path: Path) -> None:
    """
    Concept: Validates that connector retains strong intra-component bridges even when cross-component candidates are available.
    Contribution: Prevents core definitional proof moves from disappearing merely because the KB also contains disconnected regions.
    """

    kb_path = tmp_path / "hybrid-candidates.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "---",
                "kb_id: hybrid-candidates",
                "title: Hybrid Candidates",
                "domain: mathematics",
                "subdomain: functional-analysis-semigroup-theory",
                "---",
                "",
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.def.c0",
                "kind: definition",
                "status: accepted",
                "latex: A C_0-semigroup is strongly continuous.",
                "informal: Strongly continuous semigroup on a Banach space.",
                "source_ids: []",
                "used_symbols: [sym.Tt]",
                "depends_on: []",
                "concept_roles: [cnc.c0-semigroup]",
                "statement_phase: foundational-definitions",
                "bridge_roles: [semigroup-foundation]",
                "method_tags: [laplace-transform]",
                "barrier_family: ''",
                "confidence: 0.95",
                "proof_sketch: ''",
                "notes: ''",
                "```",
                "",
                "```yaml",
                "id: st.def.gen",
                "kind: definition",
                "status: accepted",
                "latex: The generator is the derivative at time zero of a C_0-semigroup orbit.",
                "informal: Generator of a C0 semigroup.",
                "source_ids: []",
                "used_symbols: [sym.A, sym.Tt]",
                "depends_on: [st.def.c0]",
                "concept_roles: [cnc.generator, cnc.c0-semigroup]",
                "statement_phase: foundational-definitions",
                "bridge_roles: [generator-foundation]",
                "method_tags: [laplace-transform]",
                "barrier_family: ''",
                "confidence: 0.95",
                "proof_sketch: ''",
                "notes: ''",
                "```",
                "",
                "```yaml",
                "id: st.thm.other",
                "kind: theorem",
                "status: accepted",
                "latex: A disconnected theorem about an abstract Cauchy problem.",
                "informal: A separate theorem producing cross-component opportunities.",
                "source_ids: []",
                "used_symbols: [sym.CP]",
                "depends_on: []",
                "concept_roles: [cnc.abstract-cauchy-problem]",
                "statement_phase: problem-semantics",
                "bridge_roles: [evolution-equivalence]",
                "method_tags: [laplace-transform]",
                "barrier_family: ''",
                "confidence: 0.95",
                "proof_sketch: ''",
                "notes: ''",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = analyze_kb(
        kb_path=kb_path,
        top_k=5,
        min_similarity=0.0,
        max_connections=10,
        loop_rounds=1,
        include_statuses={"accepted"},
    )

    assert report["stats"]["candidate_generation_mode"] == "hybrid"
    assert any(
        {item["from_id"], item["to_id"]} == {"st.def.c0", "st.def.gen"}
        for item in report["connection_candidates"]
    )


def test_connector_extracts_stone_operator_theory_signatures(tmp_path: Path) -> None:
    """
    Concept: Validates that Stone-style unitary-group content is routed through the operator-theoretic semigroup ontology.
    Contribution: Prevents the bridge concept `generator` from being misread as a complexity-theoretic object.
    """

    kb_path = tmp_path / "stone-mini.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "---",
                "kb_id: stone-mini",
                "title: Stone Mini",
                "domain: mathematics",
                "subdomain: functional-analysis-semigroup-theory",
                "---",
                "",
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.thm.stone-mini",
                "kind: theorem",
                "status: accepted",
                "latex: A strongly continuous one-parameter unitary group U_t on a Hilbert space H is of the form U_t = e^{itA} for a unique self-adjoint operator A.",
                "informal: Stone's theorem identifies strongly continuous one-parameter unitary groups with unique self-adjoint generators via spectral calculus.",
                "source_ids: []",
                "used_symbols: [sym.Ut, sym.A, sym.H]",
                "depends_on: []",
                "concept_roles: [cnc.unitary-group, cnc.infinitesimal-generator, cnc.self-adjoint-operator]",
                "statement_phase: stone-correspondence",
                "bridge_roles: [correspondence-bijection]",
                "method_tags: [generator-analysis, spectral-analysis, functional-calculus]",
                "barrier_family: orbit-differentiability-control",
                "confidence: 0.95",
                "proof_sketch: Recover the generator from unitary orbits and use functional calculus for the converse.",
                "notes: The hidden bridge concept is the infinitesimal generator.",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = analyze_kb(
        kb_path=kb_path,
        top_k=5,
        min_similarity=0.0,
        max_connections=10,
        loop_rounds=1,
        include_statuses={"accepted"},
    )

    intervention = next(item for item in report["top_interventions"] if item["statement_id"] == "st.thm.stone-mini")
    profile = intervention["concept_profile"]

    assert report["stats"]["ontology_profile"] == "functional-analysis-semigroup"
    assert "stone-unitary-group-correspondence" in profile["claim_signatures"]
    assert any(
        item in profile["implication_signatures"]
        for item in ("unitary-group-implies-self-adjoint-generator", "unitary-group-implies-unique-self-adjoint-generator")
    )
    assert "strongly-continuous-unitary-group" in profile["antecedent_signatures"]
    assert "unique-self-adjoint-generator" in profile["consequence_signatures"]
    assert "strongly-continuous-unitary-group" in profile["model_signatures"]
    assert "self-adjoint-spectral-calculus" in profile["model_signatures"]
    assert profile["complexity_classes"] == []


def test_connector_extracts_riesz_measure_representation_signatures(tmp_path: Path) -> None:
    """
    Concept: Validates that Riesz-Markov-Kakutani content is routed through the measure-representation ontology.
    Contribution: Prevents the bridge concept `measure` from collapsing into generic probability or lexical similarity only.
    """

    kb_path = tmp_path / "riesz-mini.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "---",
                "kb_id: riesz-mini",
                "title: Riesz Mini",
                "domain: mathematics",
                "subdomain: functional-analysis-measure-representation",
                "---",
                "",
                "# Canonical Statements",
                "",
                "```yaml",
                "id: st.thm.riesz-mini",
                "kind: theorem",
                "status: accepted",
                "latex: Every positive linear functional on C_c(X) is represented by integration against a unique regular Borel measure on a locally compact Hausdorff space X.",
                "informal: The Riesz-Markov-Kakutani theorem identifies positive linear functionals with unique regular Borel measures.",
                "source_ids: []",
                "used_symbols: [sym.X, sym.phi, sym.mu, sym.CcX]",
                "depends_on: []",
                "concept_roles: [cnc.positive-functional, cnc.regular-borel-measure, cnc.integration-pairing]",
                "statement_phase: riesz-markov-kakutani-correspondence",
                "bridge_roles: [representation-bijection]",
                "method_tags: [measure-representation, compact-open-approximation, integration-representation]",
                "barrier_family: topological-regularity-reconstruction",
                "confidence: 0.95",
                "proof_sketch: Recover the hidden regular Borel measure from positivity and compact-open approximation.",
                "notes: The hidden bridge concept is the regular Borel measure.",
                "```",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = analyze_kb(
        kb_path=kb_path,
        top_k=5,
        min_similarity=0.0,
        max_connections=10,
        loop_rounds=1,
        include_statuses={"accepted"},
    )

    intervention = next(item for item in report["top_interventions"] if item["statement_id"] == "st.thm.riesz-mini")
    profile = intervention["concept_profile"]

    assert report["stats"]["ontology_profile"] == "functional-analysis-measure-representation"
    assert "riesz-markov-kakutani-correspondence" in profile["claim_signatures"]
    assert "positive-functional-implies-regular-measure" in profile["implication_signatures"]
    assert "positive-linear-functional-on-cc-space" in profile["antecedent_signatures"]
    assert "regular-borel-measure-representation" in profile["consequence_signatures"]
    assert "regular-Borel-measure-model" in profile["model_signatures"]
    assert "locally-compact-Hausdorff-space" in profile["model_signatures"]
    assert profile["complexity_classes"] == []


def test_clean_evidence_terms_filters_symbol_debris_but_keeps_compact_math_labels() -> None:
    """
    Concept: Validates that clean evidence terms filters symbol debris but keeps compact math labels.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    cleaned = _clean_evidence_terms({"OS", "AC0", "c", "f", "g", "mass-gap", "Wightman-QFT", "b"})

    assert "c" not in cleaned
    assert "f" not in cleaned
    assert "g" not in cleaned
    assert "b" not in cleaned
    assert "OS" in cleaned
    assert "AC0" in cleaned
    assert "mass-gap" in cleaned
