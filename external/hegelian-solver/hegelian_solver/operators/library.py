# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Deterministic transformation candidate templates.

This is the solver's `Aufhebung` proposal stage: given a concept and a list of triggers
(failures or discovery signals), `propose_candidates` produces one `TransformationCandidate`
per (trigger, operator) pair, where the operator comes from `operator_for_trigger` (an
explicit `repair_target`/`candidate_move` on the trigger if it names a real operator,
otherwise the `FAILURE_TO_OPERATORS`/`SIGNAL_TO_OPERATORS` lookup below). Every candidate's
`target_concept` is a *renamed, re-tagged copy* of the source concept (see `_target_payload`)
rather than a structurally new theory — this keeps the pipeline's shape demonstrable without
a real proof/derivation engine behind it, at the cost of representational depth (tracked in
TODO.md Phase 19). `ALL_OPERATOR_NAMES` is intentionally larger than the names that appear
in `FAILURE_TO_OPERATORS`/`SIGNAL_TO_OPERATORS`: operators like `Pretrain`, `Embed`,
`SelfAttend`, etc. are only reachable when a fixture's `repair_target` names them explicitly
(see the LM evolution chain fixtures), not via automatic label routing.

NOTE: `FAILURE_TO_OPERATORS` here and `failures.REPAIR_TARGETS` are two separately
maintained copies of the same label -> operator mapping and have already drifted for a
couple of labels — this file's table is authoritative for which operator actually gets
proposed (see TODO.md Phase 19 for the planned unification).
"""

from __future__ import annotations

from typing import Any

from hegelian_solver.ids import stable_id
from hegelian_solver.schemas import ConceptNode, DiscoverySignal, FailureCertificate, TransformationCandidate


FAILURE_TO_OPERATORS = {
    "NonClosure": ["GroupCompletion"],
    "NonSolvability": ["AlgebraicAdjunction"],
    "Incompleteness": ["Completion"],
    "NonInvariance": ["Invariantize", "Quotient"],
    "Rigidity": ["WeakenEquivalence"],
    "Inconsistency": ["TypeStratify"],
    "NonRepresentability": ["AbstractInterface"],
    "PoorTransfer": ["AbstractInterface"],
    "CaseExplosion": ["WeakenAxioms"],
    "NoUniversalProperty": ["Categorify"],
    "MissingCoherence": ["Functorialize"],
    "EmpiricalAnomaly": ["IntroduceLatentCarrier"],
    "Overextension": ["RestrictRegime"],
    "NonCovariance": ["InvariantizeKinematics"],
    "RepresentationDependence": ["GaugeQuotient"],
    "ScaleMismatch": ["CoarseGrain", "Renormalize"],
    "MeasurementGap": ["MeasurementModelEnrichment"],
    "NoLimitingCase": ["RestrictRegime"],
    "Hallucination": ["Retrieve", "Verify"],
    "NoProvenance": ["Retrieve", "Verify"],
    "PromptInjection": ["SecureRAG", "TaintTracking"],
    "ToolMisuse": ["Toolify", "Verify"],
    "OverRefusal": ["CalibrateSafetyPolicy"],
    "PlanningMyopia": ["Agentify", "AddState"],
    "GovernanceGap": ["Govern"],
}

SIGNAL_TO_OPERATORS = {
    "SharedInterface": ["AbstractInterface"],
    "InvariantPattern": ["Invariantize"],
    "ProofCompression": ["WeakenAxioms"],
    "RepresentationRedundancy": ["Quotient"],
    "EquivalencePressure": ["WeakenEquivalence"],
    "UniversalPattern": ["Categorify"],
    "FunctorialBehavior": ["Functorialize"],
    "DualityPattern": ["Categorify"],
    "ParameterGeneralization": ["AbstractInterface"],
    "AnomalyCluster": ["AbstractInterface"],
    "SymmetryPattern": ["InvariantizeKinematics"],
    "UnificationPressure": ["LocalizeSymmetry"],
    "LatentCarrier": ["IntroduceLatentCarrier"],
    "FieldPattern": ["FieldifyActionAtDistance"],
    "GeometricPattern": ["GeometrizeInteraction"],
    "QuantizationPressure": ["QuantizeObservableAlgebra"],
    "OrderParameterPattern": ["IntroduceOrderParameter"],
    "ScaleUniversality": ["Renormalize"],
    "GaugeRedundancy": ["GaugeQuotient"],
    "ToolAPIExtension": ["Toolify"],
    "ExternalEvidencePressure": ["Retrieve"],
    "ContextMemoryPressure": ["AddState"],
    "GovernancePressure": ["Govern"],
    "AgenticStatePressure": ["Agentify"],
}

ALL_OPERATOR_NAMES = sorted(
    {
        "GroupCompletion",
        "FieldOfFractions",
        "Localization",
        "Completion",
        "AlgebraicAdjunction",
        "Invariantize",
        "Quotient",
        "WeakenEquivalence",
        "AbstractInterface",
        "WeakenAxioms",
        "TypeStratify",
        "Categorify",
        "Functorialize",
        "RestrictRegime",
        "InvariantizeKinematics",
        "GeometrizeInteraction",
        "FieldifyActionAtDistance",
        "QuantizeObservableAlgebra",
        "IntroduceLatentCarrier",
        "GaugeQuotient",
        "LocalizeSymmetry",
        "CoarseGrain",
        "Renormalize",
        "IntroduceOrderParameter",
        "MeasurementModelEnrichment",
        "FormalizeOperation",
        "Mapify",
        "MorphismLift",
        "Functorialize",
        "ManifoldLocalize",
        "Tensorize",
        "ModuleGeneralize",
        "OpenSetAbstract",
        "EpsilonDeltaRigorize",
        "HomologyFunctor",
        "Pretrain",
        "Embed",
        "Contextualize",
        "SelfAttend",
        "RoleSpecialize",
        "FewShotTransfer",
        "ScaleInstrumentalize",
        "InstructionTune",
        "PreferenceOptimize",
        "Retrieve",
        "Verify",
        "Toolify",
        "Agentify",
        "Multimodalize",
        "ReasonAtInference",
        "Sparsify",
        "Distill",
        "Govern",
        "SecureRAG",
        "TaintTracking",
        "CalibrateSafetyPolicy",
        "AddState",
        "EvaluateContinuously",
        "ReleaseGovernance",
    }
)


def operator_for_trigger(trigger: FailureCertificate | DiscoverySignal) -> list[str]:
    """Pick the operator(s) to try for one trigger: explicit repair hint first, then the
    label-keyed lookup table, then a generic fallback (`AbstractInterface` for failures,
    the signal's own `candidate_move` for discovery signals)."""

    label = trigger.label
    if isinstance(trigger, FailureCertificate):
        explicit = [target for target in trigger.repair_target if target in ALL_OPERATOR_NAMES]
        if explicit:
            return explicit
        return FAILURE_TO_OPERATORS.get(label, trigger.repair_target or ["AbstractInterface"])
    return SIGNAL_TO_OPERATORS.get(label, [trigger.candidate_move])


def _relation_for_operator(operator: str) -> str:
    """Map an operator name to the `ConceptGraphEdge.relation` it produces (e.g.
    `GroupCompletion` -> `completes`, `Invariantize` -> `abstracts`)."""

    mapping = {
        "GroupCompletion": "completes",
        "FieldOfFractions": "completes",
        "Completion": "completes",
        "AlgebraicAdjunction": "extends",
        "Invariantize": "abstracts",
        "Quotient": "quotients",
        "WeakenEquivalence": "weakens",
        "AbstractInterface": "abstracts",
        "WeakenAxioms": "weakens",
        "TypeStratify": "stratifies",
        "Categorify": "abstracts",
        "Functorialize": "abstracts",
        "FormalizeOperation": "extends",
        "Mapify": "extends",
        "MorphismLift": "abstracts",
        "ManifoldLocalize": "localizes",
        "Tensorize": "abstracts",
        "ModuleGeneralize": "abstracts",
        "OpenSetAbstract": "abstracts",
        "EpsilonDeltaRigorize": "stratifies",
        "HomologyFunctor": "abstracts",
        "RestrictRegime": "effective_of",
        "InvariantizeKinematics": "limits_to",
        "GeometrizeInteraction": "geometrizes",
        "FieldifyActionAtDistance": "extends",
        "QuantizeObservableAlgebra": "quantizes",
        "IntroduceLatentCarrier": "extends",
        "GaugeQuotient": "gauge_quotients",
        "LocalizeSymmetry": "unifies",
        "CoarseGrain": "coarse_grains_to",
        "Renormalize": "renormalizes_to",
        "Retrieve": "retrieves",
        "Pretrain": "extends",
        "Embed": "extends",
        "Contextualize": "extends",
        "SelfAttend": "extends",
        "RoleSpecialize": "abstracts",
        "FewShotTransfer": "extends",
        "ScaleInstrumentalize": "extends",
        "Verify": "extends",
        "Toolify": "toolifies",
        "Agentify": "agentifies",
        "Govern": "governs",
        "EvaluateContinuously": "governs",
        "ReleaseGovernance": "governs",
    }
    return mapping.get(operator, "extends")


def _target_name(concept: ConceptNode, operator: str) -> str:
    """Render the successor concept's display name, e.g. `Naturals` + `GroupCompletion`
    -> `CompletedNaturals`."""

    prefixes = {
        "GroupCompletion": "Completed",
        "FieldOfFractions": "FractionField",
        "Completion": "Complete",
        "AlgebraicAdjunction": "Adjoined",
        "Invariantize": "Invariant",
        "Quotient": "Quotient",
        "WeakenEquivalence": "EquivalenceAware",
        "AbstractInterface": "Abstract",
        "WeakenAxioms": "Minimal",
        "TypeStratify": "Stratified",
        "Categorify": "Categorical",
        "Functorialize": "Functorial",
        "FormalizeOperation": "Operational",
        "Mapify": "Mapping",
        "MorphismLift": "Morphism",
        "ManifoldLocalize": "Manifold",
        "Tensorize": "Tensorial",
        "ModuleGeneralize": "Module",
        "OpenSetAbstract": "Topological",
        "EpsilonDeltaRigorize": "Rigorous",
        "HomologyFunctor": "Homological",
        "RestrictRegime": "Effective",
        "InvariantizeKinematics": "Covariant",
        "GeometrizeInteraction": "Geometric",
        "FieldifyActionAtDistance": "Field",
        "QuantizeObservableAlgebra": "Quantum",
        "IntroduceLatentCarrier": "CarrierAugmented",
        "GaugeQuotient": "GaugeInvariant",
        "LocalizeSymmetry": "Gauge",
        "CoarseGrain": "CoarseGrained",
        "Renormalize": "Renormalized",
        "Retrieve": "Grounded",
        "Pretrain": "Pretrained",
        "Embed": "Embedded",
        "Contextualize": "Contextual",
        "SelfAttend": "Transformer",
        "RoleSpecialize": "RoleSpecialized",
        "FewShotTransfer": "FewShot",
        "ScaleInstrumentalize": "Scaled",
        "Verify": "Verified",
        "Toolify": "ToolUsing",
        "Agentify": "Agentic",
        "Govern": "Governed",
        "EvaluateContinuously": "ContinuouslyEvaluated",
        "ReleaseGovernance": "Released",
    }
    return f"{prefixes.get(operator, operator)}{concept.name}"


def _target_payload(concept: ConceptNode, operator: str, trigger: Any) -> dict[str, Any]:
    """Build the successor concept dict: a copy of `concept` with a new id/name/history
    entry, plus domain-specific scaffolding the validator will later check for (physics:
    `regime`/`measurement_model`/`limiting_cases`; LM: `governance`, and `tools`/`safety`
    for `Retrieve`/`Verify`/`Toolify`/`Agentify`)."""

    target = concept.model_dump(mode="json")
    target["name"] = _target_name(concept, operator)
    target["id"] = stable_id("concept", {"source": concept.id, "operator": operator, "trigger": trigger.id})
    target["history"] = list(target.get("history", [])) + [
        {"from": concept.id, "operator": operator, "trigger": trigger.id}
    ]
    target["status"] = "provisional"
    target["allowed_operators"] = sorted(set(target.get("allowed_operators", []) + ALL_OPERATOR_NAMES))

    if concept.domain == "physical_concept":
        target.setdefault("regime", {})
        target["regime"].setdefault("valid_when", ["declared by candidate validation"])
        target.setdefault("measurement_model", {})
        target["measurement_model"].setdefault("maps", ["to be specified by validation"])
        target.setdefault("limiting_cases", [])
        target["limiting_cases"].append({"predecessor": concept.id, "operator": operator})

    if concept.domain == "language_model_concept":
        target.setdefault("governance", {})
        target["governance"].setdefault("monitoring", ["required"])
        if operator in {"Retrieve", "Verify"}:
            target.setdefault("tools", [])
            target["tools"].append({"name": "evidence_store", "role": "source grounding"})
        if operator in {"Toolify", "Agentify"}:
            target.setdefault("safety", {})
            target["safety"].setdefault("approval_gates", ["side-effecting actions"])

    return target


def _expected_obligations(operator: str, concept: ConceptNode) -> list[str]:
    """List the obligation kinds `validators/core.py` must check for this candidate: the
    four core ones every move owes (preservation/resolution/noncollapse/residual_limit),
    plus operator-specific ones (universality; coverage/transfer/adequacy for interface-
    style operators) and domain-specific ones (physics/LM extras)."""

    base = ["preservation", "resolution", "noncollapse", "residual_limit"]
    if operator in {"GroupCompletion", "FieldOfFractions", "Completion", "Categorify", "OpenSetAbstract", "HomologyFunctor"}:
        base.append("universality")
    if operator in {
        "AbstractInterface",
        "WeakenAxioms",
        "Functorialize",
        "MorphismLift",
        "ModuleGeneralize",
        "RoleSpecialize",
    }:
        base.extend(["coverage", "transfer", "adequacy"])
    if concept.domain == "physical_concept":
        base.extend(["regime", "measurement", "limiting_case", "anti_overfit"])
    if concept.domain == "language_model_concept":
        base.extend(["risk", "governance", "efficiency"])
    return list(dict.fromkeys(base))


def _ranking_features(operator: str, concept: ConceptNode) -> dict[str, float]:
    """Seed `TransformationCandidate.ranking_features` for `ranker.score_candidate`.

    NOTE: these are fixed per (operator, domain) constants, not derived from how strong the
    concept's own evidence is — two candidates with the same operator in the same domain
    always get identical feature values today. See TODO.md Phase 19 for making this
    evidence-sensitive.
    """

    if concept.domain == "physical_concept":
        return {
            "empirical_gain": 0.6,
            "predecessor_recovery": 0.7,
            "symmetry_gain": 0.7 if "Invariant" in operator or "Gauge" in operator else 0.4,
            "predictive_novelty": 0.5,
            "compression": 0.5,
            "ad_hocness": 0.2 if operator != "IntroduceLatentCarrier" else 0.45,
            "complexity": 0.35,
        }
    if concept.domain == "language_model_concept":
        return {
            "failure_resolution": 0.65,
            "capability_preservation": 0.65,
            "source_grounding": 0.8 if operator in {"Retrieve", "Verify"} else 0.4,
            "tool_correctness": 0.75 if operator == "Toolify" else 0.4,
            "safety": 0.7 if operator in {"Govern", "SecureRAG", "TaintTracking"} else 0.5,
            "monitorability": 0.7 if operator == "Govern" else 0.4,
            "latency_cost_fit": 0.5,
            "new_risk": 0.25 if operator not in {"Agentify", "Toolify"} else 0.45,
        }
    return {
        "resolution": 0.7,
        "preservation": 0.7,
        "compression": 0.6,
        "universality": 0.7 if operator in {"GroupCompletion", "Categorify", "AbstractInterface"} else 0.4,
        "transfer": 0.6,
        "invariance_gain": 0.7 if operator in {"Invariantize", "Quotient"} else 0.3,
        "complexity": 0.3,
    }


def _candidate(concept: ConceptNode, trigger: FailureCertificate | DiscoverySignal, operator: str) -> TransformationCandidate:
    """Assemble one full `TransformationCandidate` for a (concept, trigger, operator)
    triple: target concept, preservation map, resolution mechanism, expected obligations,
    and ranking features."""

    target = _target_payload(concept, operator, trigger)
    payload = {
        "operator": operator,
        "source_concepts": [concept.id],
        "target_concept": target,
        "triggered_by": [trigger.id],
        "preservation_map": {
            "kind": "embedding_or_interpretation",
            "source": concept.id,
            "target": target["id"],
            "relation": _relation_for_operator(operator),
        },
        "resolution_mechanism": f"{operator} addresses {trigger.label}",
        "changed_structure": [operator],
        "expected_obligations": _expected_obligations(operator, concept),
        "residual_limits": [
            f"{target['name']} remains provisional until domain-specific validation is complete"
        ],
        "rejected_alternatives": [],
        "ranking_features": _ranking_features(operator, concept),
        "assumptions": ["candidate generated by deterministic template"],
        "unknowns": [],
    }
    payload["id"] = stable_id("candidate", payload)
    return TransformationCandidate.model_validate(payload)


def propose_candidates(
    concept: ConceptNode, triggers: list[FailureCertificate | DiscoverySignal]
) -> list[TransformationCandidate]:
    """Entry point: generate one candidate per (trigger, operator) pair across all
    triggers, deduplicated by candidate id. Multiple operators per trigger (e.g.
    `ScaleMismatch` -> `CoarseGrain` and `Renormalize`) means a single pass already tries
    several repair strategies side by side, which is what lets `ranker.rank_candidates`
    branch instead of forcing one winner."""

    candidates: list[TransformationCandidate] = []
    seen: set[str] = set()
    for trigger in triggers:
        operators = operator_for_trigger(trigger)
        for operator in operators:
            candidate = _candidate(concept, trigger, operator)
            if candidate.id not in seen:
                candidates.append(candidate)
                seen.add(candidate.id)
    return candidates
