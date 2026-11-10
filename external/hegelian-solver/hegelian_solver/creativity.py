# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Grounded conceptual creativity analysis.

This module answers a question the rest of the pipeline doesn't: *why* is a given
transformation candidate a creative move rather than a merely corrective one? Every field
of the resulting `ConceptualCreativityAnalysis` is derived from the candidate's own trace
artifacts (its trigger, preservation map, expected obligations, residual limits) rather than
asserted free-form — when an artifact doesn't supply enough to ground a field, that gap is
recorded in `residual_todos` instead of being papered over.

`OPERATOR_TO_OPERATION` is the conceptual-operation taxonomy from TODO.md Phase 21: every
operator name in `operators.library.ALL_OPERATOR_NAMES` is classified into exactly one of
nine operation kinds, which is what lets creativity be compared across cases (a
`closure_completion` in number theory and a `closure_completion` in an LM context are doing
the same *kind* of conceptual work even though nothing else about them matches).
"""

from __future__ import annotations

from hegelian_solver.ids import stable_id
from hegelian_solver.schemas import (
    ConceptualCreativityAnalysis,
    ConceptualOperationKind,
    DiscoverySignal,
    FailureCertificate,
    RankingDecision,
    SourcePressure,
    TransformationCandidate,
    ValidationPacket,
)

CORE_OBLIGATION_KINDS = {"preservation", "resolution", "noncollapse", "residual_limit"}

# Every name in operators.library.ALL_OPERATOR_NAMES classified into one conceptual
# operation. Kept here (not in operators/library.py) because the taxonomy is a lens over
# operators, not a property the operator templates need to know about themselves.
OPERATOR_TO_OPERATION: dict[str, ConceptualOperationKind] = {
    # closure_completion: adjoin a missing result instead of forbidding the case.
    "GroupCompletion": "closure_completion",
    "FieldOfFractions": "closure_completion",
    "Localization": "closure_completion",
    "Completion": "closure_completion",
    "AlgebraicAdjunction": "closure_completion",
    # abstraction_interface_discovery: name a reusable interface/structure.
    "AbstractInterface": "abstraction_interface_discovery",
    "WeakenAxioms": "abstraction_interface_discovery",
    "Categorify": "abstraction_interface_discovery",
    "Functorialize": "abstraction_interface_discovery",
    "FormalizeOperation": "abstraction_interface_discovery",
    "Mapify": "abstraction_interface_discovery",
    "MorphismLift": "abstraction_interface_discovery",
    "ModuleGeneralize": "abstraction_interface_discovery",
    "OpenSetAbstract": "abstraction_interface_discovery",
    "EpsilonDeltaRigorize": "abstraction_interface_discovery",
    "HomologyFunctor": "abstraction_interface_discovery",
    "RoleSpecialize": "abstraction_interface_discovery",
    "InstructionTune": "abstraction_interface_discovery",
    "Multimodalize": "abstraction_interface_discovery",
    "Distill": "abstraction_interface_discovery",
    # invariance_reparameterization: re-describe so a former distinction stops mattering.
    "Invariantize": "invariance_reparameterization",
    "WeakenEquivalence": "invariance_reparameterization",
    "InvariantizeKinematics": "invariance_reparameterization",
    "Tensorize": "invariance_reparameterization",
    "SelfAttend": "invariance_reparameterization",
    # quotienting_redundancy_removal: identify what shouldn't have been distinguished.
    "Quotient": "quotienting_redundancy_removal",
    "GaugeQuotient": "quotienting_redundancy_removal",
    "TypeStratify": "quotienting_redundancy_removal",
    # localization_regime_restriction: scope validity instead of claiming universality.
    "RestrictRegime": "localization_regime_restriction",
    "LocalizeSymmetry": "localization_regime_restriction",
    "CoarseGrain": "localization_regime_restriction",
    "Renormalize": "localization_regime_restriction",
    "ManifoldLocalize": "localization_regime_restriction",
    "ScaleInstrumentalize": "localization_regime_restriction",
    "Sparsify": "localization_regime_restriction",
    # externalization_or_tooling: move a capability outside the core object, on demand.
    "Retrieve": "externalization_or_tooling",
    "Toolify": "externalization_or_tooling",
    "Agentify": "externalization_or_tooling",
    "FewShotTransfer": "externalization_or_tooling",
    "ReasonAtInference": "externalization_or_tooling",
    # bridge_mediation: connect two previously separate descriptions or domains.
    "GeometrizeInteraction": "bridge_mediation",
    "FieldifyActionAtDistance": "bridge_mediation",
    "QuantizeObservableAlgebra": "bridge_mediation",
    "MeasurementModelEnrichment": "bridge_mediation",
    "Embed": "bridge_mediation",
    "Contextualize": "bridge_mediation",
    "PreferenceOptimize": "bridge_mediation",
    # latent_carrier_introduction: posit a new entity that carries an explanatory role.
    "IntroduceLatentCarrier": "latent_carrier_introduction",
    "IntroduceOrderParameter": "latent_carrier_introduction",
    "Pretrain": "latent_carrier_introduction",
    "AddState": "latent_carrier_introduction",
    # governance_safety_scaffold: add the accountability layer a capability now needs.
    "Verify": "governance_safety_scaffold",
    "Govern": "governance_safety_scaffold",
    "SecureRAG": "governance_safety_scaffold",
    "TaintTracking": "governance_safety_scaffold",
    "CalibrateSafetyPolicy": "governance_safety_scaffold",
    "EvaluateContinuously": "governance_safety_scaffold",
    "ReleaseGovernance": "governance_safety_scaffold",
}

OPERATION_REFRAMING = {
    "closure_completion": "treats the missing result as a new element to adjoin rather than a forbidden case",
    "abstraction_interface_discovery": "names the shared structure across cases as a reusable interface instead of leaving it implicit in each case separately",
    "invariance_reparameterization": "re-describes the object so a distinction that used to matter is reparameterized away",
    "quotienting_redundancy_removal": "identifies a distinction that was never load-bearing and collapses it",
    "localization_regime_restriction": "scopes the claim to where it actually holds instead of defending it as universal",
    "externalization_or_tooling": "moves a capability outside the core object and invokes it on demand instead of building it in",
    "bridge_mediation": "introduces an explicit relation connecting two previously separate descriptions",
    "latent_carrier_introduction": "posits a new entity to carry an explanatory role nothing in the current ontology can carry",
    "governance_safety_scaffold": "adds the accountability/control layer a capability needs once it is powerful enough to misfire",
}

OPERATION_GENERATIVE_PAYOFF = {
    "closure_completion": "the completed structure can now be reused as an ordinary object by every later construction, not handled as a special case",
    "abstraction_interface_discovery": "the new interface can be instantiated by other concepts, turning one fix into a reusable pattern",
    "invariance_reparameterization": "downstream work can now ignore the reparameterized-away distinction entirely",
    "quotienting_redundancy_removal": "the smaller quotient structure is easier to reason about and reduces redundant casework",
    "localization_regime_restriction": "the regime boundary becomes an explicit, testable object instead of a silent assumption",
    "externalization_or_tooling": "the externalized capability can be upgraded or swapped independently of the core object",
    "bridge_mediation": "the new relation enables transfer of results across the two domains it connects",
    "latent_carrier_introduction": "the new entity becomes independently testable/measurable, opening a new line of evidence",
    "governance_safety_scaffold": "the capability can now be deployed at higher stakes because its failure modes are bounded and observable",
}

OBLIGATION_KIND_TO_AFFORDANCE = {
    "universality": "satisfies a universal property other constructions can map into uniquely",
    "coverage": "covers more instances/examples than the predecessor could represent",
    "transfer": "supports transfer of results to representations the predecessor could not reach",
    "adequacy": "is adequate for cases the predecessor only handled by exception",
    "regime": "makes the regime of validity an explicit, checkable property",
    "measurement": "exposes a measurement interface the predecessor left implicit",
    "limiting_case": "recovers the predecessor as a provable limiting case rather than an informal analogy",
    "anti_overfit": "earns its new ontology with independent measurement consequences",
    "risk": "gates a newly powerful capability behind explicit safety checks",
    "governance": "exposes monitoring/governance hooks the predecessor lacked",
    "efficiency": "opens a latency/cost tradeoff space the predecessor didn't have to manage",
}


def _source_pressure(trigger: FailureCertificate | DiscoverySignal) -> SourcePressure:
    if isinstance(trigger, FailureCertificate):
        return SourcePressure(
            kind="failure", id=trigger.id, label=trigger.label, statement=trigger.failed_obligation
        )
    return SourcePressure(
        kind="discovery_signal",
        id=trigger.id,
        label=trigger.label,
        statement=trigger.candidate_move,
    )


def _latent_tension(trigger: FailureCertificate | DiscoverySignal) -> str:
    if isinstance(trigger, FailureCertificate):
        return f"{trigger.label}: {trigger.failed_obligation}"
    return f"{trigger.label} pressure observed across {len(trigger.evidence)} evidence item(s), suggesting {trigger.candidate_move}"


def _new_affordances(candidate: TransformationCandidate) -> list[str]:
    extra_kinds = [kind for kind in candidate.expected_obligations if kind not in CORE_OBLIGATION_KINDS]
    return [OBLIGATION_KIND_TO_AFFORDANCE.get(kind, f"takes on a new `{kind}` obligation") for kind in extra_kinds]


def _repair_vs_affordance(operation: ConceptualOperationKind, new_affordance: list[str]) -> str:
    if not new_affordance:
        return "repair"
    if operation in {"quotienting_redundancy_removal", "localization_regime_restriction", "governance_safety_scaffold"}:
        return "mixed"
    return "affordance_creation"


def _preservation(candidate: TransformationCandidate) -> list[str]:
    items = []
    kind = candidate.preservation_map.get("kind")
    relation = candidate.preservation_map.get("relation")
    if kind:
        items.append(f"preservation map kind: {kind}")
    if relation:
        items.append(f"graph relation: {relation}")
    return items


def _why_creative_not_corrective(
    repair_vs_affordance: str, operation: ConceptualOperationKind, trigger_label: str, new_affordance: list[str]
) -> str:
    if repair_vs_affordance == "repair":
        return (
            f"This move only restores the core obligations broken by {trigger_label}; "
            "no new affordance is claimed beyond fixing that obligation, so it is corrective rather than creative."
        )
    reframing = OPERATION_REFRAMING[operation]
    return (
        f"Beyond resolving {trigger_label}, this move {reframing}, which is new constructive "
        f"capability ({'; '.join(new_affordance)}) the predecessor concept did not have — that is "
        "what makes it a creative move rather than a merely corrective one."
    )


def analyze_creativity(
    candidate: TransformationCandidate,
    trigger: FailureCertificate | DiscoverySignal,
    packet: ValidationPacket | None = None,
) -> ConceptualCreativityAnalysis:
    """Build a grounded `ConceptualCreativityAnalysis` for one candidate.

    Every field is derived from `candidate`/`trigger`/`packet`; nothing here introduces a
    claim the trace artifacts don't already support. Where an artifact is too thin to ground
    a required field (see `REQUIRED_EXPLICIT_FIELDS`), the gap is recorded in
    `residual_todos` rather than left implicit.
    """

    operation = OPERATOR_TO_OPERATION.get(candidate.operator)
    residual_todos: list[str] = []
    if operation is None:
        operation = "abstraction_interface_discovery"
        residual_todos.append(
            f"operator `{candidate.operator}` has no conceptual-operation taxonomy entry; defaulted to "
            "abstraction_interface_discovery and should be classified explicitly"
        )

    new_affordance = _new_affordances(candidate)
    repair_vs_affordance = _repair_vs_affordance(operation, new_affordance)
    preservation = _preservation(candidate)
    if not preservation:
        residual_todos.append("no preservation map kind/relation found; preservation_under_transformation is unsupported")

    downstream_seeds = list(candidate.residual_limits)
    if not downstream_seeds:
        residual_todos.append("candidate declares no residual_limits; downstream_concept_seeds is unsupported")

    creative_risks = list(candidate.residual_limits) + list(candidate.unknowns)
    if packet is not None:
        creative_risks += [f"{o.kind}: {o.blocker}" for o in packet.obligations if o.blocker]

    analysis_payload = {
        "candidate_id": candidate.id,
        "operator": candidate.operator,
        "operation": operation,
        "repair_vs_affordance": repair_vs_affordance,
        "source_pressure": _source_pressure(trigger).model_dump(mode="json"),
        "latent_tension": _latent_tension(trigger),
        "creative_reframing": OPERATION_REFRAMING[operation],
        "new_constructive_resource": f"{candidate.target_concept.get('name', candidate.target_concept.get('id', 'successor concept'))} "
        f"via {candidate.operator} ({', '.join(candidate.changed_structure) or 'no structural delta declared'})",
        "new_affordance": new_affordance,
        "preservation_under_transformation": preservation,
        "generative_payoff": [OPERATION_GENERATIVE_PAYOFF[operation]],
        "creative_risks": creative_risks,
        "why_creative_not_corrective": _why_creative_not_corrective(
            repair_vs_affordance, operation, trigger.label, new_affordance
        ),
        "downstream_concept_seeds": downstream_seeds,
        "residual_todos": residual_todos,
    }
    analysis_payload["id"] = stable_id("creativity", {"candidate": candidate.id, "operator": candidate.operator})
    return ConceptualCreativityAnalysis.model_validate(analysis_payload)


def analyze_candidates(
    candidates: list[TransformationCandidate],
    triggers_by_id: dict[str, FailureCertificate | DiscoverySignal],
    packets_by_candidate_id: dict[str, ValidationPacket],
) -> list[ConceptualCreativityAnalysis]:
    """Analyze every candidate that has a resolvable trigger, in input order."""

    analyses = []
    for candidate in candidates:
        if not candidate.triggered_by:
            continue
        trigger = triggers_by_id.get(candidate.triggered_by[0])
        if trigger is None:
            continue
        analyses.append(analyze_creativity(candidate, trigger, packets_by_candidate_id.get(candidate.id)))
    return analyses


def order_by_decision(
    analyses: list[ConceptualCreativityAnalysis], decisions_by_candidate_id: dict[str, RankingDecision]
) -> list[ConceptualCreativityAnalysis]:
    """Sort analyses so accepted/branching/provisional candidates surface before rejected ones."""

    def sort_key(analysis: ConceptualCreativityAnalysis) -> tuple[bool, float, str]:
        decision = decisions_by_candidate_id.get(analysis.candidate_id)
        is_rejected = decision.decision in {"reject", "defer"} if decision else True
        score = -decision.score if decision else 0.0
        return (is_rejected, score, analysis.candidate_id)

    return sorted(analyses, key=sort_key)


REQUIRED_EXPLICIT_FIELDS = (
    "source_pressure",
    "operation",
    "new_affordance",
    "preservation_under_transformation",
    "creative_risks",
    "downstream_concept_seeds",
)


def validate_creativity_analysis(analysis: ConceptualCreativityAnalysis) -> list[str]:
    """Return validation-criteria violations: which required-explicit fields are empty.

    Per TODO.md Phase 21, source pressure, operation, new affordance, preserved invariant,
    risk/tradeoff, and downstream concept seeds must be explicit; this is the check that
    enforces it (the builder above already folds violations into `residual_todos`, so this
    is also usable standalone against a hand-authored or agent-authored analysis).
    """

    missing = []
    for field in REQUIRED_EXPLICIT_FIELDS:
        value = getattr(analysis, field)
        if not value:
            missing.append(f"missing or empty required field: {field}")
    return missing
