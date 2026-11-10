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

from to_prism.schemas import load_schema, validate_document


def incident_taxonomy() -> dict:
    return {
        "artifact": "project-semantic-taxonomy",
        "schema_version": "1.0",
        "source_fingerprint": "sha256:" + "a" * 64,
        "review_status": "proposed",
        "objects": [
            {
                "id": "witness_statements",
                "nominal_type": "IncidentWitnessStatements",
                "epistemic_role": "statement",
                "description": "Attributed witness reports about one identified operational incident.",
                "fields": [
                    {
                        "name": "incident_reference",
                        "type": "String",
                        "description": "Stable identifier for the investigated operational incident.",
                    },
                    {
                        "name": "statements",
                        "type": "List[String]",
                        "description": "Attributed first-person reports made by incident witnesses.",
                    },
                ],
                "source_anchors": [
                    "skills/incident-intake/SKILL.md#required-witness-inputs"
                ],
                "provenance": "raw",
                "assurance_justification": "The reports retain source attribution but have not been corroborated.",
                "unresolved": [],
            },
            {
                "id": "corroborated_evidence",
                "nominal_type": "CorroboratedIncidentEvidence",
                "epistemic_role": "evidence",
                "description": "Incident claims assessed for independence, agreement, and relevance.",
                "fields": [
                    {
                        "name": "supported_claims",
                        "type": "List[String]",
                        "description": "Incident claims supported by mutually independent witness sources.",
                    },
                    {
                        "name": "contested_claims",
                        "type": "List[String]",
                        "description": "Material claims for which the available witness sources conflict.",
                    },
                ],
                "source_anchors": [
                    "skills/testimony-corroborator/SKILL.md#independence-policy"
                ],
                "provenance": "supported",
                "assurance_justification": "Support records the stated corroboration policy and preserves disagreement.",
                "unresolved": [],
            },
            {
                "id": "candidate_failure_hypothesis",
                "nominal_type": "CandidateFailureHypothesis",
                "epistemic_role": "hypothesis",
                "description": "One defeasible causal explanation proposed for the incident failure.",
                "fields": [
                    {
                        "name": "causal_explanation",
                        "type": "String",
                        "description": "Proposed mechanism connecting incident conditions to the failure.",
                    }
                ],
                "source_anchors": [
                    "skills/root-cause-ranker/SKILL.md#candidate-generation"
                ],
                "provenance": "generated",
                "assurance_justification": "Generation establishes candidacy only, not support, rank, or truth.",
                "unresolved": [],
            },
            {
                "id": "ranked_failure_hypotheses",
                "nominal_type": "RankedFailureHypotheses",
                "epistemic_role": "ranked_hypotheses",
                "description": "Causal incident hypotheses ordered by an explicit evidential criterion.",
                "fields": [
                    {
                        "name": "ordered_hypotheses",
                        "type": "List[CandidateFailureHypothesis]",
                        "description": "Candidate explanations ordered from strongest to weakest support.",
                    },
                    {
                        "name": "ranking_basis",
                        "type": "String",
                        "description": "Evidence aggregation and tie policy used to establish the order.",
                    },
                ],
                "source_anchors": [
                    "skills/root-cause-ranker/SKILL.md#ranking-contract"
                ],
                "provenance": "generated",
                "assurance_justification": "The rank is a defeasible model assessment under the named criterion.",
                "unresolved": [],
            },
        ],
        "operations": [
            {
                "id": "rank_incident_causes",
                "granularity_rationale": "Corroboration and ranking form one reviewed occurrence here because the source exposes only their joint ranked result.",
                "kind": "abduct",
                "input_types": [
                    "IncidentWitnessStatements",
                    "CorroboratedIncidentEvidence",
                    "CandidateFailureHypothesis",
                ],
                "output_type": "RankedFailureHypotheses",
                "semantic_role": "epistemic",
                "result_provenance": "generated",
                "skill_composition": [
                    {
                        "path": "skills/testimony-corroborator",
                        "role": "source independence assessor",
                        "contribution": "Distinguishes independent support from repeated or contested testimony.",
                    },
                    {
                        "path": "skills/root-cause-ranker",
                        "role": "abductive cause ranking analyst",
                        "contribution": "Compares candidate causal mechanisms under the documented evidence criterion.",
                    },
                ],
                "rationale": "The occurrence compares causal explanations rather than proving a single cause.",
                "source_anchors": [
                    "workflows/incident-analysis.md#corroborate-and-rank"
                ],
            }
        ],
        "unresolved": [],
    }


def test_specific_project_taxonomy_is_registered_and_valid() -> None:
    taxonomy = incident_taxonomy()

    assert load_schema("project-semantic-taxonomy")["$id"].endswith(
        "project-semantic-taxonomy.schema.json"
    )
    assert validate_document(taxonomy) == []
    assert len(taxonomy["operations"][0]["skill_composition"]) == 2


def test_taxonomy_accepts_example_driven_query_and_formalization_roles() -> None:
    taxonomy = incident_taxonomy()
    taxonomy["objects"][0]["epistemic_role"] = "query"
    taxonomy["objects"][1]["epistemic_role"] = "retrieval_result"
    taxonomy["objects"][2]["epistemic_role"] = "formal_representation"
    taxonomy["objects"][3]["epistemic_role"] = "mathematical_representation"
    taxonomy["operations"][0]["kind"] = "formalize"
    taxonomy["operations"][0]["inference_class"] = "representational"

    assert validate_document(taxonomy) == []


def test_taxonomy_requires_reasoning_granularity_rationale() -> None:
    taxonomy = incident_taxonomy()
    del taxonomy["operations"][0]["granularity_rationale"]

    issues = validate_document(taxonomy)

    assert any(
        "missing required property 'granularity_rationale'" in str(issue)
        for issue in issues
    )


def test_taxonomy_requires_generated_results_for_epistemic_occurrences() -> None:
    taxonomy = incident_taxonomy()
    taxonomy["operations"][0]["result_provenance"] = "computed"

    issues = validate_document(taxonomy)

    assert any(
        "epistemic occurrences in the to_prism conversion profile must be generated"
        in str(issue)
        for issue in issues
    )


def test_taxonomy_allows_one_skill_to_contribute_to_multiple_occurrences() -> None:
    taxonomy = incident_taxonomy()
    second = deepcopy(taxonomy["operations"][0])
    second.update(
        {
            "id": "calibrate_incident_ranking",
            "kind": "calibrate",
            "input_types": ["RankedFailureHypotheses"],
            "output_type": "RankedFailureHypotheses",
            "granularity_rationale": "Calibration is separately reviewed because downstream consumers inspect its revised uncertainty independently.",
            "rationale": "The occurrence revises ranking uncertainty while retaining every incident hypothesis.",
            "source_anchors": ["workflows/incident-analysis.md#ranking-review"],
            "skill_composition": [
                deepcopy(taxonomy["operations"][0]["skill_composition"][1])
            ],
        }
    )
    taxonomy["operations"].append(second)

    assert validate_document(taxonomy) == []


def test_taxonomy_validation_does_not_mutate_reviewed_evidence() -> None:
    taxonomy = incident_taxonomy()
    original = deepcopy(taxonomy)

    assert validate_document(taxonomy) == []
    assert taxonomy == original


def test_taxonomy_rejects_unknown_fields_and_epistemic_roles() -> None:
    taxonomy = incident_taxonomy()
    taxonomy["objects"][0]["future_guess"] = True
    taxonomy["objects"][1]["epistemic_role"] = "information"

    issues = validate_document(taxonomy)

    assert any("future_guess: unknown property" in str(issue) for issue in issues)
    assert any("must be one of" in str(issue) for issue in issues)


def test_taxonomy_requires_object_source_anchors() -> None:
    taxonomy = incident_taxonomy()
    taxonomy["objects"][0]["source_anchors"] = []

    issues = validate_document(taxonomy)

    assert any("must contain project-source evidence" in str(issue) for issue in issues)


def test_taxonomy_rejects_generic_nominal_objects_even_when_declared() -> None:
    taxonomy = incident_taxonomy()
    taxonomy["objects"][0]["nominal_type"] = "Input"
    taxonomy["operations"][0]["input_types"][0] = "Input"

    issues = validate_document(taxonomy)

    assert any(
        "must name a project-specific semantic object" in str(issue) for issue in issues
    )


def test_taxonomy_requires_typed_operation_boundaries() -> None:
    taxonomy = incident_taxonomy()
    taxonomy["operations"][0]["input_types"] = []

    issues = validate_document(taxonomy)

    assert any(
        "must name one or more nominal input types" in str(issue) for issue in issues
    )


def test_taxonomy_requires_attributed_skill_composition() -> None:
    taxonomy = incident_taxonomy()
    taxonomy["operations"][0]["skill_composition"] = []

    issues = validate_document(taxonomy)

    assert any(
        "must attribute one or more source skills" in str(issue) for issue in issues
    )


def test_taxonomy_operation_types_must_name_declared_objects() -> None:
    taxonomy = incident_taxonomy()
    taxonomy["operations"][0]["output_type"] = "GenericReasoningResult"

    issues = validate_document(taxonomy)

    assert any(
        "undeclared nominal type GenericReasoningResult" in str(issue)
        for issue in issues
    )


def test_taxonomy_skill_composition_has_exact_semantic_fields() -> None:
    taxonomy = incident_taxonomy()
    taxonomy["operations"][0]["skill_composition"][0]["prompt"] = "analyze"
    del taxonomy["operations"][0]["skill_composition"][1]["contribution"]

    issues = validate_document(taxonomy)

    assert any("prompt: unknown property" in str(issue) for issue in issues)
    assert any(
        "missing required property 'contribution'" in str(issue) for issue in issues
    )


def test_taxonomy_rejects_unjustified_assurance_and_unknown_provenance() -> None:
    taxonomy = incident_taxonomy()
    taxonomy["objects"][0]["assurance_justification"] = "not sure"
    taxonomy["objects"][1]["provenance"] = "trusted"

    issues = validate_document(taxonomy)

    assert any(
        "assurance_justification: string is too short" in str(issue) for issue in issues
    )
    assert any("provenance: must be one of" in str(issue) for issue in issues)
