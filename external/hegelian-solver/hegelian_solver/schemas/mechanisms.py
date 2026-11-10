# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Pydantic models for abductive mechanism reasoning artifacts.

These mirror the YAML shapes produced by the `hegelian-abductive-mechanism-hypothesizer`,
`hegelian-mechanism-requirements-formalizer`, `hegelian-mechanism-counterfactual-critic`, and
`hegelian-mechanism-todo-elicitor` skills. Mechanism packets remain provisional artifacts: they
are hypothesis and requirement objects, not accepted repair edges in the concept graph.
"""

from __future__ import annotations

from typing import Literal

from pydantic import ConfigDict, Field

from hegelian_solver.schemas.models import StrictModel


class InferenceCommitment(StrictModel):
    role: Literal[
        "necessary_mediator",
        "enabling_condition",
        "jointly_sufficient_set",
        "diagnostic_observation",
        "defeater",
        "impossibility_boundary",
    ]
    claim: str
    warrant: str


class RequiredMediationShape(StrictModel):
    commitments_to_preserve: list[str] = Field(default_factory=list)
    incompatibility_to_mediate: str
    missing_relation_or_process: list[str] = Field(default_factory=list)
    inference_commitments: list[InferenceCommitment] = Field(default_factory=list)


class FormalMediation(StrictModel):
    new_predicates: list[str] = Field(default_factory=list)
    new_maps: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    preserved_obligations: list[str] = Field(default_factory=list)


class MaterialMediation(StrictModel):
    actors: list[str] = Field(default_factory=list)
    practices_or_infrastructure: list[str] = Field(default_factory=list)
    resources_needed: list[str] = Field(default_factory=list)
    incentive_or_governance_changes: list[str] = Field(default_factory=list)


class MechanismHypothesis(StrictModel):
    id: str
    label: str
    hypothesis_type: Literal["conservative", "expressive", "institutional", "hybrid", "experimental"]
    abductive_claim: str
    if_this_existed_then: str
    formal_mediation: FormalMediation = Field(default_factory=FormalMediation)
    material_mediation: MaterialMediation = Field(default_factory=MaterialMediation)
    explanatory_gain: list[str] = Field(default_factory=list)
    new_risks: list[str] = Field(default_factory=list)
    disconfirming_observations: list[str] = Field(default_factory=list)
    evidence_needed: list[str] = Field(default_factory=list)


class RejectedHypothesis(StrictModel):
    id: str
    label: str
    reason: str


class MechanismAbductionPacket(StrictModel):
    crisis_ref: str
    crisis_restated: str
    required_mediation_shape: RequiredMediationShape
    mechanism_hypotheses: list[MechanismHypothesis] = Field(default_factory=list)
    rejected_hypotheses: list[RejectedHypothesis] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)


class MechanismRequirement(StrictModel):
    id: str
    kind: Literal[
        "formal_capacity",
        "material_capacity",
        "interface_capacity",
        "epistemic_capacity",
        "safety_or_noncollapse_capacity",
        "regime_capacity",
    ]
    necessity_status: Literal["necessary", "jointly_sufficient", "exploratory", "regime_specific"]
    statement: str
    formalization: str | None = None
    material_anchor: str | None = None
    verifies_commitments: list[str] = Field(default_factory=list)
    validation_method: Literal[
        "proof",
        "simulation",
        "benchmark",
        "audit",
        "field_study",
        "policy_review",
        "experiment",
        "trace_replay",
        "human_review",
    ]
    evidence_needed: list[str] = Field(default_factory=list)
    failure_mode_if_missing: str


class MediationMap(StrictModel):
    id: str
    source_commitment: str
    target_commitment: str
    map_type: Literal[
        "transport",
        "calibration",
        "authorization",
        "accountability",
        "limiting",
        "embedding",
        "refinement",
        "feedback",
        "governance",
    ]
    statement: str
    required_properties: list[str] = Field(default_factory=list)


class MechanismRequirementsPacket(StrictModel):
    crisis_ref: str
    selected_hypothesis_refs: list[str] = Field(default_factory=list)
    mechanism_name: str
    mechanism_role: str
    requirements: list[MechanismRequirement] = Field(default_factory=list)
    mediation_maps: list[MediationMap] = Field(default_factory=list)
    material_preconditions: list[str] = Field(default_factory=list)
    implementation_surfaces: list[str] = Field(default_factory=list)
    validation_obligations: list[str] = Field(default_factory=list)
    residual_limits: list[str] = Field(default_factory=list)
    open_todos: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)


class CounterfactualTest(StrictModel):
    id: str
    test_type: Literal[
        "remove_requirement",
        "invert_incentive",
        "shift_regime",
        "proxy_capture",
        "authority_gap",
        "evidence_shift",
        "material_bottleneck",
        "noncollapse_probe",
    ]
    scenario: str
    expected_if_mechanism_valid: str
    failure_signal: str
    affected_requirements: list[str] = Field(default_factory=list)
    result: Literal["pass", "fail", "unknown", "needs_evidence"]


class MechanismCounterfactualCritique(StrictModel):
    requirements_ref: str
    overall_status: Literal["plausible", "underdetermined", "fragile", "collapsed", "rejected"]
    counterfactual_tests: list[CounterfactualTest] = Field(default_factory=list)
    hidden_assumptions: list[str] = Field(default_factory=list)
    collapse_risks: list[str] = Field(default_factory=list)
    alternative_mechanisms_still_live: list[str] = Field(default_factory=list)
    required_revisions: list[str] = Field(default_factory=list)
    evidence_or_experiment_priorities: list[str] = Field(default_factory=list)


class MechanismTodo(StrictModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    class_: Literal[
        "formal_work",
        "evidence_work",
        "simulation_or_benchmark",
        "material_design",
        "implementation",
        "validation",
        "decision",
    ] = Field(alias="class")
    task: str
    why_needed: str
    depends_on: list[str] = Field(default_factory=list)
    artifact_expected: str
    acceptance_criterion: str
    priority: Literal["low", "medium", "high", "critical"]
    blocks_candidate_acceptance: bool


class MechanismTodoGroup(StrictModel):
    group_id: str
    purpose: str
    todos: list[MechanismTodo] = Field(default_factory=list)


class MechanismTodoPacket(StrictModel):
    requirements_ref: str
    critique_ref: str | None = None
    todo_groups: list[MechanismTodoGroup] = Field(default_factory=list)
    immediate_next_actions: list[str] = Field(default_factory=list)
    deferred_questions: list[str] = Field(default_factory=list)
    stop_conditions: list[str] = Field(default_factory=list)


class MechanismDossier(StrictModel):
    """Bundles one mechanism's full abduction -> requirements -> critique -> TODO chain."""

    id: str
    source_tension_ref: str
    field: str
    mechanism_name: str
    scenario_summary: str = ""
    mechanism_abduction_packet: MechanismAbductionPacket | None = None
    mechanism_requirements_packet: MechanismRequirementsPacket | None = None
    mechanism_counterfactual_critique: MechanismCounterfactualCritique | None = None
    mechanism_todo_packet: MechanismTodoPacket | None = None


def all_mechanism_schema_models() -> list[type[StrictModel]]:
    return [
        InferenceCommitment,
        RequiredMediationShape,
        FormalMediation,
        MaterialMediation,
        MechanismHypothesis,
        RejectedHypothesis,
        MechanismAbductionPacket,
        MechanismRequirement,
        MediationMap,
        MechanismRequirementsPacket,
        CounterfactualTest,
        MechanismCounterfactualCritique,
        MechanismTodo,
        MechanismTodoGroup,
        MechanismTodoPacket,
        MechanismDossier,
    ]
