# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

from copy import deepcopy

import pytest
from to_prism.semantic_types import (
    SemanticContract,
    SemanticTypeError,
    validate_reasoning_projection,
    validate_semantic_contract,
)

from to_prism.schemas import load_schema, validate_document


def incident_hypothesis_plan() -> dict:
    """A specific epistemic workflow, not a generic text transformation."""
    return {
        "artifact": "generation-plan",
        "schema_version": "1.0",
        "type_definitions": [
            {
                "name": "IncidentWitnessStatements",
                "description": "Witness statements and stable identity for one investigated incident.",
                "kind": "record",
                "fields": [
                    {
                        "name": "incident_reference",
                        "type": "String",
                        "description": "Stable identifier of the operational incident under investigation.",
                    },
                    {
                        "name": "statements",
                        "type": "List[String]",
                        "description": "First-person observations supplied by identified incident witnesses.",
                    },
                ],
            },
            {
                "name": "CorroboratedIncidentEvidence",
                "description": "Witness claims separated by corroboration and relevance to the incident.",
                "kind": "record",
                "fields": [
                    {
                        "name": "corroborated_claims",
                        "type": "List[String]",
                        "description": "Claims supported by mutually independent incident observations.",
                    },
                    {
                        "name": "contested_claims",
                        "type": "List[String]",
                        "description": "Material incident claims whose sources conflict or lack support.",
                    },
                ],
            },
            {
                "name": "FailureHypothesis",
                "description": "One causal explanation considered for the investigated incident failure.",
                "kind": "record",
                "fields": [
                    {
                        "name": "causal_explanation",
                        "type": "String",
                        "description": "Proposed causal mechanism connecting evidence to the observed failure.",
                    },
                    {
                        "name": "supporting_claims",
                        "type": "List[String]",
                        "description": "Corroborated incident claims that support this causal explanation.",
                    },
                ],
            },
            {
                "name": "RankedFailureHypotheses",
                "description": "Ordered causal hypotheses with an explicit evidence-based ranking basis.",
                "kind": "record",
                "fields": [
                    {
                        "name": "hypotheses",
                        "type": "List[FailureHypothesis]",
                        "description": "Candidate failure explanations ordered from strongest to weakest support.",
                    },
                    {
                        "name": "ranking_basis",
                        "type": "String",
                        "description": "Comparative evidential basis used to order the causal hypotheses.",
                    },
                ],
            },
        ],
        "workflows": [
            {
                "id": "rank_incident_failure_hypotheses",
                "review_status": "approved",
                "semantic_mode": "epistemic",
                "description": "Derive and rank causal incident hypotheses from witness testimony.",
                "input": {
                    "name": "witness_statements",
                    "type": "IncidentWitnessStatements",
                    "fixture": {
                        "incident_reference": "INC-2041",
                        "statements": [
                            "The deployment alarm preceded the service restart.",
                            "Database saturation began after the deployment alarm.",
                        ],
                    },
                },
                "output": {
                    "type": "RankedFailureHypotheses",
                    "provenance": "generated",
                },
                "epistemic_contract": {
                    "subject": "The causal mechanism of operational incident INC-2041.",
                    "question": "Which failure hypotheses best explain the reported incident evidence?",
                    "observations": [
                        "Witness statements are reports rather than direct system measurements."
                    ],
                    "defeaters": [
                        "Shared information sources may make apparently independent reports correlated."
                    ],
                    "defeater_rationale": "The listed defeater bounds how testimonial corroboration is interpreted.",
                    "output_meaning": "A defeasible ordering of causal hypotheses by evidential support.",
                    "assurance": "generated",
                    "assurance_justification": "The ranked hypotheses are model inferences and not material facts.",
                    "unresolved": [],
                },
                "steps": [
                    {
                        "id": "corroborate_testimony",
                        "description": "Assess independence, agreement, and relevance across witness statements.",
                        "input_type": "IncidentWitnessStatements",
                        "output_type": "CorroboratedIncidentEvidence",
                        "semantic_role": "epistemic",
                        "granularity_rationale": "Corroboration is independently consumed and reviewed before any causal hypotheses are ranked.",
                        "reasoning_type": "TestimonialReliabilityAssessment",
                        "reasoning_rationale": "Corroboration must discount shared sources and preserve contested claims.",
                        "output_provenance": "generated",
                        "failure_type": "ModelFailure",
                        "effects": ["AI.Generate", "Context.Disclose"],
                        "skills": [
                            {
                                "path": "skills/source-independence-assessor",
                                "role": "source independence assessor",
                                "contribution": "Identifies shared information sources before claims are treated as corroboration.",
                                "resource_dispositions": {},
                            },
                            {
                                "path": "skills/testimony-corroborator",
                                "role": "testimony corroboration analyst",
                                "contribution": "Separates independently supported incident claims from materially contested claims.",
                                "resource_dispositions": {},
                            },
                        ],
                    },
                    {
                        "id": "rank_failure_hypotheses",
                        "description": "Compare causal explanations against corroborated and contested evidence.",
                        "input_type": "CorroboratedIncidentEvidence",
                        "output_type": "RankedFailureHypotheses",
                        "semantic_role": "epistemic",
                        "granularity_rationale": "Ranking makes a new comparative commitment over the corroborated evidence and has its own typed result.",
                        "reasoning_type": "AbductiveFailureHypothesisRanking",
                        "reasoning_rationale": "Abductive comparison ranks explanations while retaining defeasibility.",
                        "output_provenance": "generated",
                        "failure_type": "ModelFailure",
                        "effects": ["AI.Generate", "Context.Disclose"],
                        "skills": [
                            {
                                "path": "skills/abductive-hypothesis-ranker",
                                "role": "causal hypothesis ranker",
                                "contribution": "Orders causal failure hypotheses by their comparative support in corroborated evidence.",
                                "resource_dispositions": {},
                            },
                            {
                                "path": "skills/testimony-corroborator",
                                "role": "contested testimony boundary keeper",
                                "contribution": "Carries corroboration and disagreement limits into the comparative hypothesis ranking.",
                                "resource_dispositions": {},
                            }
                        ],
                    },
                ],
            }
        ],
    }


def validate_contract(plan: dict):
    workflow = plan["workflows"][0]
    return validate_semantic_contract(plan, workflow, workflow["steps"])


def test_specific_epistemic_plan_is_schema_valid_and_semantically_typed() -> None:
    plan = incident_hypothesis_plan()

    assert load_schema("generation-plan")["$id"].endswith("generation-plan.schema.json")
    assert validate_document(plan) == []
    contract = validate_contract(plan)

    assert contract.input_type == "IncidentWitnessStatements"
    assert contract.output_type == "RankedFailureHypotheses"
    assert set(contract.types) == {
        "IncidentWitnessStatements",
        "CorroboratedIncidentEvidence",
        "FailureHypothesis",
        "RankedFailureHypotheses",
    }
    assert len(plan["workflows"][0]["steps"][0]["skills"]) == 2


def test_step_can_compose_multiple_skills_with_distinct_contributions() -> None:
    plan = incident_hypothesis_plan()
    skills = plan["workflows"][0]["steps"][0]["skills"]

    assert validate_document(plan) == []
    assert [skill["role"] for skill in skills] == [
        "source independence assessor",
        "testimony corroboration analyst",
    ]


def test_skill_can_contribute_to_multiple_reasoning_occurrences() -> None:
    plan = incident_hypothesis_plan()
    steps = plan["workflows"][0]["steps"]

    assert validate_document(plan) == []
    assert "skills/testimony-corroborator" in {
        skill["path"] for skill in steps[0]["skills"]
    }
    assert "skills/testimony-corroborator" in {
        skill["path"] for skill in steps[1]["skills"]
    }


def test_reasoning_occurrence_requires_reviewed_granularity() -> None:
    plan = incident_hypothesis_plan()
    del plan["workflows"][0]["steps"][0]["granularity_rationale"]

    issues = validate_document(plan)

    assert any(
        "missing required property 'granularity_rationale'" in str(issue)
        for issue in issues
    )
    with pytest.raises(SemanticTypeError, match="granularity_rationale"):
        validate_contract(plan)


@pytest.mark.parametrize(
    "generic_name", ["ConversionTask", "Task", "Input", "Output", "Data", "Any"]
)
def test_generic_nominal_types_are_rejected(generic_name: str) -> None:
    plan = incident_hypothesis_plan()
    plan["type_definitions"][0]["name"] = generic_name
    plan["workflows"][0]["input"]["type"] = generic_name
    plan["workflows"][0]["steps"][0]["input_type"] = generic_name

    with pytest.raises(SemanticTypeError, match="generic and forbidden"):
        validate_contract(plan)


def test_any_is_rejected_inside_an_otherwise_specific_type() -> None:
    plan = incident_hypothesis_plan()
    plan["type_definitions"][0]["fields"][1]["type"] = "List[Any]"

    with pytest.raises(SemanticTypeError, match="cannot use Any"):
        validate_contract(plan)


def test_one_field_text_envelope_is_rejected() -> None:
    plan = incident_hypothesis_plan()
    plan["type_definitions"][0]["fields"] = [
        {
            "name": "text",
            "type": "String",
            "description": "Unstructured text with no declared incident-domain interpretation.",
        }
    ]
    plan["workflows"][0]["input"]["fixture"] = {"text": "some statement"}

    with pytest.raises(SemanticTypeError, match="uninformative one-field"):
        validate_contract(plan)


def test_unresolved_semantic_questions_block_generation() -> None:
    plan = incident_hypothesis_plan()
    plan["workflows"][0]["epistemic_contract"]["unresolved"] = [
        "Whether two witnesses relied on the same monitoring dashboard."
    ]

    with pytest.raises(SemanticTypeError, match="blocked by unresolved"):
        validate_contract(plan)


def test_broken_nominal_chain_is_rejected() -> None:
    plan = incident_hypothesis_plan()
    plan["workflows"][0]["steps"][1]["input_type"] = "IncidentWitnessStatements"

    with pytest.raises(SemanticTypeError, match="predecessor produces"):
        validate_contract(plan)


def test_epistemic_step_without_reasoning_rationale_is_rejected() -> None:
    plan = incident_hypothesis_plan()
    del plan["workflows"][0]["steps"][0]["reasoning_rationale"]

    with pytest.raises(SemanticTypeError, match="reasoning_rationale"):
        validate_contract(plan)


def test_schema_requires_explicit_defeater_rationale_and_exact_step_fields() -> None:
    plan = incident_hypothesis_plan()
    del plan["workflows"][0]["epistemic_contract"]["defeater_rationale"]
    plan["workflows"][0]["steps"][0]["generic_prompt"] = "summarize this"

    issues = validate_document(plan)

    assert any(
        "missing required property 'defeater_rationale'" in str(i) for i in issues
    )
    assert any("generic_prompt: unknown property" in str(i) for i in issues)


def test_schema_requires_each_disclosed_effect_exactly_once() -> None:
    plan = incident_hypothesis_plan()
    plan["workflows"][0]["steps"][0]["effects"] = [
        "AI.Generate",
        "AI.Generate",
        "Context.Disclose",
    ]

    issues = validate_document(plan)

    assert any(
        "must contain AI.Generate and Context.Disclose exactly once" in str(i)
        for i in issues
    )


def test_computed_step_cannot_claim_computed_materialization_without_constructor_contract() -> None:
    plan = incident_hypothesis_plan()
    workflow = plan["workflows"][0]
    workflow["semantic_mode"] = "mixed"
    step = workflow["steps"][0]
    step["semantic_role"] = "operational"
    step["material_kind"] = "computed"
    step["adapter_operation"] = "incident.corroborate"
    step["procedure"] = "incident-corroboration-v1"
    step["effects"] = ["Python.Call"]
    step["failure_type"] = "PythonError"
    del step["reasoning_type"]
    del step["reasoning_rationale"]

    with pytest.raises(
        SemanticTypeError, match="output_provenance must be computed"
    ):
        validate_contract(plan)


def test_schema_rejects_missing_skill_composition() -> None:
    plan = incident_hypothesis_plan()
    del plan["workflows"][0]["steps"][0]["skills"]

    issues = validate_document(plan)

    assert any("missing required property 'skills'" in str(i) for i in issues)


def test_schema_rejects_empty_skill_composition() -> None:
    plan = incident_hypothesis_plan()
    plan["workflows"][0]["steps"][0]["skills"] = []

    issues = validate_document(plan)

    assert any(
        "must compose one or more explicitly attributed skills" in str(i)
        for i in issues
    )


def test_schema_rejects_generic_skill_contribution() -> None:
    plan = incident_hypothesis_plan()
    plan["workflows"][0]["steps"][0]["skills"][0]["contribution"] = (
        "Transform the input into the output."
    )

    issues = validate_document(plan)

    assert any(
        "must identify a domain-specific skill contribution" in str(i) for i in issues
    )


def test_schema_rejects_generic_skill_role() -> None:
    plan = incident_hypothesis_plan()
    plan["workflows"][0]["steps"][0]["skills"][0]["role"] = (
        "generic task handler worker"
    )

    issues = validate_document(plan)

    assert any("must identify a domain-specific skill role" in str(i) for i in issues)


def test_generation_plan_validation_does_not_mutate_reviewed_steps() -> None:
    plan = incident_hypothesis_plan()
    original = deepcopy(plan)

    assert validate_document(plan) == []
    assert plan == original


def test_validation_rejects_orphaned_epistemic_steps_in_reasoning_projection() -> None:
    plan = incident_hypothesis_plan()
    workflow = plan["workflows"][0]
    workflow["semantic_mode"] = "mixed"
    workflow["reasoning_projection"] = {
        "name": "AssessIncidentEvidence",
        "description": "Expose the reviewed human-scale incident reasoning topology.",
        "input_name": "witness_statements",
        "input_type": "IncidentWitnessStatements",
        "output_occurrence": "corroborated_evidence",
        "output_type": "CorroboratedIncidentEvidence",
        "occurrences": [
            {
                "id": "corroborated_evidence",
                "method": "CorroborateTestimony",
                "input_type": "IncidentWitnessStatements",
                "output_type": "CorroboratedIncidentEvidence",
                "rationale": "Expose corroboration as a distinct evidential commitment.",
                "arguments": [{"source": "witness_statements"}],
                "material_steps": ["corroborate_testimony"],
            }
        ],
        "topology": ["corroborated_evidence"],
    }

    issues = validate_document(plan)

    assert any("orphaned" in str(issue) for issue in issues)


def test_reviewed_projection_can_interpret_operational_material_workflow() -> None:
    semantic = SemanticContract(
        types={"ControlSnapshot": object(), "ControlDisposition": object()},
        mode="operational",
        workflow_name="ValidateControlSurface",
        workflow_description="Validate the declared Mathformer control surface.",
        input_name="control_snapshot",
        input_type="ControlSnapshot",
        output_type="ControlDisposition",
        output_provenance="computed",
        fixture={},
        assurance="computed",
    )
    steps = [{"id": "validate_contract", "semantic_role": "operational"}]
    projection = {
        "name": "AssessControlIntegrity",
        "description": "Interpret deterministic control evidence as a scoped disposition.",
        "input_name": "control_snapshot",
        "input_type": "ControlSnapshot",
        "output_occurrence": "control_disposition",
        "output_type": "ControlDisposition",
        "occurrences": [
            {
                "id": "control_disposition",
                "method": "CalibrateControlIntegrity",
                "input_type": "ControlSnapshot",
                "output_type": "ControlDisposition",
                "rationale": "Calibrate the control status from the reviewed deterministic checks.",
                "arguments": [{"source": "control_snapshot"}],
                "material_steps": ["validate_contract"],
            }
        ],
        "topology": ["control_disposition"],
    }

    validate_reasoning_projection(projection, semantic, steps)
