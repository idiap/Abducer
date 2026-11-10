# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Domain detection and profile construction.

This is the first stage of every run: before a concept can be formalized, the solver must
decide whether it is a `mathematical_concept`, `physical_concept`, `language_model_concept`,
or fallback `generic_concept`, because that choice selects everything downstream — which
Pydantic schema applies (`formalizer.py`), which failure/discovery taxonomies are in play
(`failures.py`, `discovery.py`), which obligations are hard gates (`validators/core.py`),
and which ranking features matter (`ranker.py`/`operators/library.py`).

`detect_domain` prefers an explicit `domain` field, falls back to characteristic dict keys
(e.g. `observables` implies physics), and only then falls back to keyword search over the
flattened raw input. `domain_profile` turns the detected domain into a `DomainProfile`
carrying each domain's failure taxonomy, discovery taxonomy, validation gates, and ranking
feature names, plus the source refs that justify the routing.
"""

from __future__ import annotations

from typing import Any

from hegelian_solver.schemas import DomainProfile


MATH_FAILURES = [
    "NonClosure",
    "NonSolvability",
    "Incompleteness",
    "NonInvariance",
    "Rigidity",
    "Inconsistency",
    "Undecidability",
    "NonRepresentability",
    "AmbiguousEquivalence",
    "NonCompositionality",
    "CaseExplosion",
    "NoUniversalProperty",
    "PoorTransfer",
    "OverstrongAxiom",
    "MissingCoherence",
]

PHYSICS_FAILURES = [
    "EmpiricalAnomaly",
    "Overextension",
    "NonCovariance",
    "SymmetryMismatch",
    "ConservationViolation",
    "NonLocalConflict",
    "Singularity",
    "UVFailure",
    "IRFailure",
    "Instability",
    "RepresentationDependence",
    "ScaleMismatch",
    "ParameterAdHocness",
    "NonRenormalizability",
    "NoLimitingCase",
    "MeasurementGap",
    "ConceptualUnderdetermination",
]

LM_FAILURES = [
    "Hallucination",
    "NoProvenance",
    "ObjectiveInterfaceMismatch",
    "ArithmeticWeakness",
    "KnowledgeStaleness",
    "ContextOverflow",
    "PromptInjection",
    "OverRefusal",
    "SafetyViolation",
    "ToolMisuse",
    "ObservationMisuse",
    "PlanningMyopia",
    "RunawayLoop",
    "ComputeInefficiency",
    "EvaluationSaturation",
    "GovernanceGap",
]

GENERIC_DISCOVERY = [
    "SharedInterface",
    "InvariantPattern",
    "ProofCompression",
    "RepresentationRedundancy",
    "EquivalencePressure",
    "UniversalPattern",
    "FunctorialBehavior",
    "DualityPattern",
    "ParameterGeneralization",
    "AnomalyCluster",
]


def _flatten_text(raw: Any) -> str:
    if isinstance(raw, str):
        return raw.lower()
    if isinstance(raw, dict):
        return " ".join([str(key) + " " + _flatten_text(value) for key, value in raw.items()]).lower()
    if isinstance(raw, list):
        return " ".join(_flatten_text(item) for item in raw).lower()
    return str(raw).lower()


def detect_domain(raw: Any) -> str:
    """Pick a domain for `raw`, in order of decreasing confidence.

    1. an explicit `domain` field always wins;
    2. otherwise, characteristic dict keys (e.g. `observables` => physics) are checked,
       since structured input is more reliable than free text;
    3. otherwise, fall back to keyword search over the flattened raw payload.

    Step 3 is a known soft spot (see TODO.md Phase 19): it is first-match keyword search
    over the whole flattened input, so an unrelated mention of a marker word (e.g. "tool"
    in a math proof) can misroute a concept. Prefer an explicit `domain` field or one of the
    structural keys above whenever the input is authored by hand.
    """

    text = _flatten_text(raw)
    explicit = raw.get("domain") if isinstance(raw, dict) else None
    if explicit in {
        "mathematical_concept",
        "physical_concept",
        "language_model_concept",
        "generic_concept",
    }:
        return explicit
    if isinstance(raw, dict):
        keys = set(raw)
        if keys & {"observables", "measurement", "measurement_model", "dynamics", "regime"}:
            return "physical_concept"
        if keys & {"architecture", "interaction", "traces", "governance", "tools"}:
            return "language_model_concept"
        if keys & {"axioms", "axioms_or_constraints", "signature", "typed_signature"}:
            return "mathematical_concept"

    physics_markers = [
        "observable",
        "measurement",
        "regime",
        "symmetry",
        "dynamics",
        "newtonian",
        "relativity",
        "quantum",
        "field",
        "empirical",
        "units",
    ]
    lm_markers = [
        "language model",
        "assistant",
        "rag",
        "retrieval",
        "tool",
        "prompt",
        "hallucination",
        "governance",
        "deployment",
        "model output",
    ]
    math_markers = [
        "axiom",
        "signature",
        "theorem",
        "proof",
        "nat",
        "integer",
        "group",
        "topological",
        "closure",
        "isomorphism",
        "functor",
    ]

    if any(marker in text for marker in physics_markers):
        return "physical_concept"
    if any(marker in text for marker in lm_markers):
        return "language_model_concept"
    if any(marker in text for marker in math_markers):
        return "mathematical_concept"
    return "generic_concept"


def domain_profile(raw: Any) -> DomainProfile:
    domain = detect_domain(raw)
    if domain == "mathematical_concept":
        return DomainProfile(
            domain=domain,
            schema_kind="ConceptNode",
            required_fields=["signature", "axioms_or_constraints", "tasks", "preservation"],
            failure_taxonomy=MATH_FAILURES,
            discovery_taxonomy=GENERIC_DISCOVERY,
            validation_gates=["preservation", "resolution", "noncollapse", "residual_limit"],
            ranking_features=[
                "resolution",
                "preservation",
                "compression",
                "universality",
                "transfer",
                "invariance_gain",
                "complexity",
            ],
            refs_used=[
                "refs/hegelian_concept_solver_spec.md",
                "refs/dialectical_concept_solver_refined_with_discovery.md",
            ],
        )
    if domain == "physical_concept":
        return DomainProfile(
            domain=domain,
            schema_kind="PhysicalConcept",
            required_fields=[
                "state_space",
                "observables",
                "dynamics",
                "symmetries",
                "measurement_model",
                "regime",
            ],
            failure_taxonomy=PHYSICS_FAILURES,
            discovery_taxonomy=GENERIC_DISCOVERY
            + [
                "SymmetryPattern",
                "UnificationPressure",
                "LatentCarrier",
                "FieldPattern",
                "GeometricPattern",
                "QuantizationPressure",
                "OrderParameterPattern",
                "ScaleUniversality",
                "GaugeRedundancy",
            ],
            validation_gates=[
                "preservation",
                "resolution",
                "noncollapse",
                "regime",
                "measurement",
                "limiting_case",
                "anti_overfit",
            ],
            ranking_features=[
                "empirical_gain",
                "predecessor_recovery",
                "symmetry_gain",
                "predictive_novelty",
                "compression",
                "ad_hocness",
            ],
            refs_used=["refs/dialectical_concept_solver_physics_examples.md"],
        )
    if domain == "language_model_concept":
        return DomainProfile(
            domain=domain,
            schema_kind="LanguageModelConcept",
            required_fields=["representation", "architecture", "interaction", "tools", "evaluation"],
            failure_taxonomy=LM_FAILURES,
            discovery_taxonomy=GENERIC_DISCOVERY
            + [
                "ExternalEvidencePressure",
                "ToolAPIExtension",
                "ContextMemoryPressure",
                "GovernancePressure",
                "AgenticStatePressure",
            ],
            validation_gates=[
                "preservation",
                "resolution",
                "noncollapse",
                "risk",
                "governance",
                "efficiency",
            ],
            ranking_features=[
                "failure_resolution",
                "capability_preservation",
                "source_grounding",
                "tool_correctness",
                "safety",
                "monitorability",
                "latency_cost_fit",
            ],
            refs_used=["refs/dialectical_concept_solver_language_model_evolution.md"],
        )
    return DomainProfile(
        domain="generic_concept",
        schema_kind="ConceptNode",
        required_fields=["tasks", "preservation"],
        failure_taxonomy=MATH_FAILURES + PHYSICS_FAILURES + LM_FAILURES,
        discovery_taxonomy=GENERIC_DISCOVERY,
        validation_gates=["preservation", "resolution", "noncollapse", "residual_limit"],
        ranking_features=["resolution", "preservation", "compression", "complexity"],
        refs_used=["refs/source_index.md"],
        unknowns=["domain-specific validation gates"],
    )
