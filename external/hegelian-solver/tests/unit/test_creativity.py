# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

from pathlib import Path

from hegelian_solver.creativity import (
    OPERATOR_TO_OPERATION,
    analyze_candidates,
    analyze_creativity,
    order_by_decision,
    validate_creativity_analysis,
)
from hegelian_solver.formalizer import formalize_concept
from hegelian_solver.io import read_structured
from hegelian_solver.operators import propose_candidates
from hegelian_solver.operators.library import ALL_OPERATOR_NAMES
from hegelian_solver.ranker import rank_candidates
from hegelian_solver.schemas import ConceptualOperationKind, FailureCertificate, TransformationCandidate
from hegelian_solver.validators import validate_candidates

ROOT = Path(__file__).resolve().parents[2]
VALID_OPERATIONS = set(ConceptualOperationKind.__args__)


def _naturals():
    return formalize_concept(read_structured(ROOT / "hegelian_solver/examples/naturals.yaml"))


def test_every_operator_has_a_taxonomy_entry_with_a_valid_kind():
    missing = [op for op in ALL_OPERATOR_NAMES if op not in OPERATOR_TO_OPERATION]
    assert missing == []

    invalid_kinds = {kind for kind in OPERATOR_TO_OPERATION.values() if kind not in VALID_OPERATIONS}
    assert invalid_kinds == set()


def test_pure_obligation_repair_is_classified_as_repair_not_creative():
    concept = _naturals()
    trigger = FailureCertificate(
        id="f1",
        label="NonInvariance",
        concept=concept.id,
        witness={"value": "representation dependence"},
        failed_obligation="representation dependence",
        repair_target=[],
    )
    candidate = propose_candidates(concept, [trigger])[0]
    assert candidate.operator == "Invariantize"

    analysis = analyze_creativity(candidate, trigger)

    assert analysis.repair_vs_affordance == "repair"
    assert analysis.new_affordance == []
    assert "corrective" in analysis.why_creative_not_corrective
    assert analysis.source_pressure.id == trigger.id
    assert analysis.source_pressure.kind == "failure"


def test_operator_adding_extra_obligations_is_classified_as_affordance_creation():
    concept = _naturals()
    trigger = FailureCertificate(
        id="f2",
        label="NonClosure",
        concept=concept.id,
        witness={"value": "3 - 5 not in Nat"},
        failed_obligation="closed subtraction",
        repair_target=["GroupCompletion"],
    )
    candidate = propose_candidates(concept, [trigger])[0]
    assert candidate.operator == "GroupCompletion"

    analysis = analyze_creativity(candidate, trigger)

    assert analysis.operation == "closure_completion"
    assert analysis.repair_vs_affordance == "affordance_creation"
    assert analysis.new_affordance
    assert analysis.preservation_under_transformation
    assert analysis.downstream_concept_seeds
    assert "creative" in analysis.why_creative_not_corrective
    assert validate_creativity_analysis(analysis) == []


def test_validate_creativity_analysis_flags_missing_required_fields():
    concept = _naturals()
    trigger = FailureCertificate(
        id="f3",
        label="NonClosure",
        concept=concept.id,
        witness={"value": "x"},
        failed_obligation="closure",
        repair_target=["GroupCompletion"],
    )
    candidate = propose_candidates(concept, [trigger])[0]
    analysis = analyze_creativity(candidate, trigger)

    thin = analysis.model_copy(
        update={"preservation_under_transformation": [], "creative_risks": [], "downstream_concept_seeds": []}
    )

    violations = validate_creativity_analysis(thin)

    assert any("preservation_under_transformation" in v for v in violations)
    assert any("creative_risks" in v for v in violations)
    assert any("downstream_concept_seeds" in v for v in violations)


def test_analyze_candidates_skips_candidates_with_unresolved_triggers():
    concept = _naturals()
    trigger = FailureCertificate(
        id="f4",
        label="NonClosure",
        concept=concept.id,
        witness={"value": "x"},
        failed_obligation="closure",
        repair_target=["GroupCompletion"],
    )
    candidates = propose_candidates(concept, [trigger])

    analyses = analyze_candidates(candidates, triggers_by_id={}, packets_by_candidate_id={})

    assert analyses == []


def test_order_by_decision_puts_rejected_after_accepted_or_provisional():
    concept = _naturals()
    good_trigger = FailureCertificate(
        id="f5", label="NonClosure", concept=concept.id, witness={"value": "x"}, failed_obligation="closure", repair_target=[]
    )
    good_candidate = propose_candidates(concept, [good_trigger])[0]

    bad_trigger = FailureCertificate(
        id="f6", label="NonRepresentability", concept=concept.id, witness={"value": "y"}, failed_obligation="bad", repair_target=[]
    )
    bad_candidate = TransformationCandidate(
        id="candidate_bad",
        operator="AbstractInterface",
        source_concepts=[concept.id],
        target_concept=concept.model_dump(mode="json"),
        triggered_by=[bad_trigger.id],
        preservation_map={},
        resolution_mechanism="",
        expected_obligations=["preservation", "resolution", "noncollapse", "residual_limit"],
        residual_limits=[],
    )

    candidates = [good_candidate, bad_candidate]
    packets = validate_candidates(concept, candidates)
    decisions = rank_candidates(candidates, packets)
    assert decisions[-1].decision == "reject"

    triggers_by_id = {good_trigger.id: good_trigger, bad_trigger.id: bad_trigger}
    packets_by_id = {p.candidate_id: p for p in packets}
    decisions_by_id = {d.candidate_id: d for d in decisions}
    analyses = analyze_candidates(candidates, triggers_by_id, packets_by_id)
    ordered = order_by_decision(analyses, decisions_by_id)

    assert ordered[0].candidate_id == good_candidate.id
    assert ordered[-1].candidate_id == bad_candidate.id
