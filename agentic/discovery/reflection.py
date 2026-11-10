# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Structural reflection and plural-theory invariants.

This module does not pretend that a deterministic template is philosophical
creativity.  It validates generative operator output and supplies explicit
fallback transformations over typed primitives, relations, mechanisms, and
genealogy when a local/offline cycle is requested.  Every fallback is visible
as an operator receipt and may remain conjectural.
"""

from __future__ import annotations

import copy
import json
import re
from collections.abc import Iterable, Mapping
from typing import Any

from agentic.discovery.conceptual_adjudication import (
    ConceptualAdjudicationError,
    validate_sealed_preference_authority,
)
from agentic.discovery.contracts import canonical_digest, stable_identifier


PARETO_DIMENSIONS = (
    "essential_relevance", "root_tension_contact", "conceptual_depth",
    "explanatory_understanding", "unification_power", "preservation_of_difference",
    "generativity", "coherence", "truth_aptness",
)
MATERIAL_RESULTS = {"mutated", "synthesized", "demoted"}


class ReflectionInvariantError(ValueError):
    """Raised when reflection is rhetorical rather than structurally effective."""


def _normalized_terms(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        values = [value]
    elif isinstance(value, Iterable):
        values = [str(item) for item in value]
    else:
        values = [str(value)]
    return tuple(sorted({re.sub(r"\s+", " ", item.strip().lower()) for item in values if item.strip()}))


def structural_signature(system: Mapping[str, Any]) -> str:
    """Hash typed structural IDs, never wording or display labels.

    Producers must preserve these IDs across paraphrase and reorder operations.
    A conceptually new system must change a primitive, relation, mechanism,
    maturation question, or genealogy identity rather than merely its prose.
    """

    identity = system.get("structural_identity")
    if not isinstance(identity, Mapping):
        raise ReflectionInvariantError("conceptual system lacks typed structural_identity")
    projection = {
        "primitive_ids": sorted(identity.get("primitive_ids", [])),
        "relation_ids": sorted(identity.get("relation_ids", [])),
        "mechanism_id": identity.get("mechanism_id"),
        "maturation_question_id": identity.get("maturation_question_id"),
        "genealogy_ids": sorted(identity.get("genealogy_ids", [])),
    }
    return canonical_digest(projection)


def systems_are_structurally_distinct(systems: list[Mapping[str, Any]]) -> bool:
    """Return true only when every system has a different structural signature."""

    signatures = [structural_signature(system) for system in systems]
    return len(signatures) == len(set(signatures))


def system_from_hypothesis(hypothesis: Mapping[str, Any], genealogy: Mapping[str, Any], *, relation: str = "rival") -> dict[str, Any]:
    """Compile either supported high-risk contract version into one rival.

    The reflective kernel originally predated the executable high-risk
    portfolio and used a flatter seed shape.  Keeping the adapter here makes
    the newer typed ontology/mechanism packet the canonical input while still
    accepting preserved fixtures and older ledger events.
    """

    hypothesis_id = str(hypothesis["hypothesis_id"])
    independence = hypothesis.get("branch_independence_signature", {})
    ontology_delta = hypothesis.get("ontology_delta", {})
    mechanism = str(
        hypothesis.get("mechanism")
        or independence.get("unique_mechanism")
        or hypothesis.get("mechanism_key")
        or "explicitly unknown mechanism"
    )
    legacy_elements = hypothesis.get("new_primitives_relations_or_mechanisms")
    primitives = [
        str(item)
        for item in (
            legacy_elements or ontology_delta.get("new_primitives", [])
        )
    ]
    typed_relations = [str(item) for item in ontology_delta.get("new_relations", [])]
    protected = [str(item) for item in hypothesis["protected_successes"]]
    pressures = [str(item) for item in hypothesis["target_pressures_addressed"]]
    boundary = str(hypothesis["boundary_case"])
    correction = [str(item) for item in hypothesis["correction_conditions"]]
    corner = str(hypothesis["corner_family"])
    system_id = stable_identifier("system", hypothesis_id, primitives, mechanism)
    primitive_ids = [stable_identifier("primitive", hypothesis_id, item) for item in primitives]
    relation_ids = [
        stable_identifier("relation", hypothesis_id, item)
        for item in (typed_relations or [mechanism])
    ]
    return {
        "system_id": system_id,
        "relation": relation,
        "lifecycle_state": "articulated",
        "structural_identity": {
            "primitive_ids": primitive_ids or [stable_identifier("primitive", hypothesis_id, "explicit-unknown")],
            "relation_ids": relation_ids,
            "mechanism_id": stable_identifier("mechanism", hypothesis_id, mechanism),
            "maturation_question_id": stable_identifier("question", hypothesis_id, hypothesis["maturation_question"]),
            "genealogy_ids": [hypothesis_id],
        },
        "conceptual_ancestors": [hypothesis_id],
        "transformation_operations": [corner],
        "primitives": primitives,
        "ontological_commitments": [f"Treat {corner} as a load-bearing organization of the target objects."],
        "identities_and_differences": [f"Identity is mediated by {item}." for item in primitives[:2]] or ["Identity conditions remain an explicit unknown."],
        "relations_operations_and_dynamics": [*typed_relations, mechanism],
        "explanatory_ideal": "mixed",
        "mechanism_or_principle": mechanism,
        "protected_successes": protected,
        "target_pressures_addressed": pressures,
        "formerly_inexpressible_now_visible": [str(hypothesis["explanatory_upside"])],
        "unification_claims": {
            "unified_cases_or_routes": pressures,
            "common_principle": str(hypothesis["unification_upside"]),
            "differences_preserved": [f"The distinct boundary behavior remains explicit: {boundary}"],
            "erasure_risks": [boundary],
        },
        "implications_and_new_questions": [
            str(hypothesis["maturation_question"]),
            str(
                hypothesis.get("learning_value_if_wrong")
                or hypothesis.get("learning_value_if_false")
                or "Determine which load-bearing assumption fails if the mechanism is wrong."
            ),
        ],
        "formalization_seeds": [f"Formalize the carrier and action of {mechanism}."],
        "correction_conditions": correction,
        "residual_contradictions": [boundary],
        "non_claims": [str(hypothesis["non_claim_boundary"])],
    }


def incumbent_system(charter: Mapping[str, Any], genealogy: Mapping[str, Any]) -> dict[str, Any]:
    """Reconstruct an incumbent system without falsely presenting it as a rival."""

    inherited = list(genealogy.get("inherited_concepts", [])) or [str(charter["incumbent_framework"])]
    assumptions = list(genealogy.get("hidden_assumptions", [])) or ["The inherited representation remains adequate."]
    system_id = stable_identifier("system", "incumbent", inherited, assumptions)
    return {
        "system_id": system_id, "relation": "incumbent", "lifecycle_state": "articulated",
        "structural_identity": {
            "primitive_ids": [stable_identifier("primitive", "incumbent", item) for item in inherited],
            "relation_ids": [stable_identifier("relation", "incumbent", charter["incumbent_framework"])],
            "mechanism_id": stable_identifier("mechanism", "incumbent", charter["incumbent_framework"]),
            "maturation_question_id": stable_identifier("question", "incumbent", charter["conceptual_opacity"]),
            "genealogy_ids": [],
        },
        "conceptual_ancestors": [], "transformation_operations": ["genealogical reconstruction"],
        "primitives": inherited, "ontological_commitments": assumptions,
        "identities_and_differences": ["Preserve the incumbent identity and regime distinctions until explicitly revised."],
        "relations_operations_and_dynamics": [str(charter["incumbent_framework"])],
        "explanatory_ideal": "mixed", "mechanism_or_principle": str(charter["incumbent_framework"]),
        "protected_successes": list(genealogy.get("protected_successes", [])),
        "target_pressures_addressed": [str(charter["essential_question"])],
        "formerly_inexpressible_now_visible": ["No new expressive resource is claimed by the incumbent reconstruction."],
        "unification_claims": {"unified_cases_or_routes": ["incumbent successes"], "common_principle": str(charter["incumbent_framework"]), "differences_preserved": ["Known regimes and boundary cases"], "erasure_risks": ["Incumbent opacity remains"]},
        "implications_and_new_questions": [str(charter["conceptual_opacity"])],
        "formalization_seeds": ["State the incumbent assumptions and quantifier order explicitly."],
        "correction_conditions": ["Revise when a rival preserves the successes while explaining the root opacity."],
        "residual_contradictions": list(genealogy.get("hidden_assumptions", [])),
        "non_claims": [str(charter["non_claim_boundary"])],
    }


def synthesize_systems(left: Mapping[str, Any], right: Mapping[str, Any], charter: Mapping[str, Any]) -> dict[str, Any]:
    """Build a dialectical synthesis that keeps parental differences visible."""

    system_id = stable_identifier("system", "synthesis", left["system_id"], right["system_id"])
    left_mechanism = str(left["mechanism_or_principle"])
    right_mechanism = str(right["mechanism_or_principle"])
    common = f"A regime-indexed mediation lets {left_mechanism} and {right_mechanism} constrain different explanatory levels without identifying them."
    return {
        "system_id": system_id, "relation": "synthesis", "lifecycle_state": "synthesized",
        "structural_identity": {
            "primitive_ids": sorted(set([*left["structural_identity"]["primitive_ids"], *right["structural_identity"]["primitive_ids"], stable_identifier("primitive", system_id, "regime-mediated")])),
            "relation_ids": sorted(set([*left["structural_identity"]["relation_ids"], *right["structural_identity"]["relation_ids"], stable_identifier("relation", system_id, "mediation")])),
            "mechanism_id": stable_identifier("mechanism", system_id, common),
            "maturation_question_id": stable_identifier("question", system_id, "transition-invariant"),
            "genealogy_ids": [str(left["system_id"]), str(right["system_id"])],
        },
        "conceptual_ancestors": [str(left["system_id"]), str(right["system_id"])],
        "transformation_operations": ["dialectical mediation", "regime stratification", "unification with preserved difference"],
        "primitives": sorted(set([*left.get("primitives", []), *right.get("primitives", []), "regime-indexed mediation"])),
        "ontological_commitments": ["The opposed mechanisms are level- or regime-relative, not interchangeable."],
        "identities_and_differences": [f"Preserve {left['system_id']} and {right['system_id']} as non-reducible limiting descriptions."],
        "relations_operations_and_dynamics": [left_mechanism, right_mechanism, common],
        "explanatory_ideal": "unification", "mechanism_or_principle": common,
        "protected_successes": sorted(set([*left.get("protected_successes", []), *right.get("protected_successes", [])])),
        "target_pressures_addressed": sorted(set([*left.get("target_pressures_addressed", []), *right.get("target_pressures_addressed", [])])),
        "formerly_inexpressible_now_visible": ["The opposition can be treated as a typed relation among regimes rather than a forced exclusive choice."],
        "unification_claims": {
            "unified_cases_or_routes": [str(left["system_id"]), str(right["system_id"])],
            "common_principle": common,
            "differences_preserved": [left_mechanism, right_mechanism],
            "erasure_risks": ["The regime index must not be chosen post hoc to absorb counterexamples."],
        },
        "implications_and_new_questions": [f"Which invariant determines the transition between {left['system_id']} and {right['system_id']}?", str(charter["essential_question"])],
        "formalization_seeds": ["Define the regime index, mediation maps, and compatibility laws."],
        "correction_conditions": ["Reject if the mediation has no independent definition or silently weakens the target."],
        "residual_contradictions": ["Whether one mechanism is genuinely fundamental remains unresolved."],
        "non_claims": [str(charter["non_claim_boundary"])],
    }


def default_reflection_rounds(systems: list[dict[str, Any]], charter: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Apply ontological and dialectical/unificatory rounds with concrete effects."""

    rivals = [item for item in systems if item["relation"] != "incumbent"]
    if len(rivals) < 2:
        raise ReflectionInvariantError("major reflection requires at least two rival systems")
    first = rivals[0]
    first["lifecycle_state"] = "reflectively_revised"
    exposed = f"The object-first identity in {first['system_id']} may be an unearned assumption."
    relational = f"relational realization of {first['primitives'][0]}"
    if relational not in first["primitives"]:
        first["primitives"].append(relational)
    first["structural_identity"]["primitive_ids"].append(stable_identifier("primitive", first["system_id"], "relational-realization"))
    first["transformation_operations"].append("ontological relation-first reconstruction")
    round_one = {
        "round_id": stable_identifier("reflection", "ontological", first["system_id"]),
        "system_ids": [first["system_id"]],
        "lenses_used": ["ontological", "epistemological", "representational"],
        "strongest_objections": [exposed],
        "blind_spots": ["The new relational carrier may merely rename the old object."],
        "mutation_or_synthesis": {"operation": "replace one object-first primitive with an explicit relational realization", "changed_primitives_relations_or_explanation": [relational], "preserved_content": list(first["protected_successes"]), "lost_content": ["Unqualified primitive identity"]},
        "result": "mutated", "no_change_reason": None,
    }
    synthesis = synthesize_systems(rivals[0], rivals[1], charter)
    systems.append(synthesis)
    round_two = {
        "round_id": stable_identifier("reflection", "dialectical", synthesis["system_id"]),
        "system_ids": [rivals[0]["system_id"], rivals[1]["system_id"], synthesis["system_id"]],
        "lenses_used": ["dialectical", "unificatory", "explanatory"],
        "strongest_objections": ["A synthesis may hide incompatibility behind an unconstrained regime index."],
        "blind_spots": ["The mediation laws are not yet formalized."],
        "mutation_or_synthesis": {"operation": "regime-indexed mediation with explicit non-reducible parental mechanisms", "changed_primitives_relations_or_explanation": ["regime-indexed mediation", synthesis["mechanism_or_principle"]], "preserved_content": synthesis["protected_successes"], "lost_content": ["The assumption that exactly one parent must be globally fundamental"]},
        "result": "synthesized", "no_change_reason": None,
    }
    return [round_one, round_two], synthesis


def validate_synthesis_revision(request: Mapping[str, Any]) -> None:
    """Bind a revision to its sealed parent without transferring old preference.

    This boundary permits genuine synthesis changes after adjudication. The old
    evidence remains complete and validated against the old systems; new rounds
    retain that history and must receive a new adjudication before investment.
    """
    from .conceptual_adjudication import validate_sealed_preference_authority
    from .contracts import ContractError, canonical_digest, validate_payload
    parent, evidence = request.get("prior_reflective_packet"), request.get("previous_evidence")
    if not isinstance(parent, Mapping) or not isinstance(evidence, Mapping):
        raise ContractError("synthesis revision requires its complete parent packet and adjudication")
    validate_payload(dict(parent), "reflective_conceptual_discovery_packet.schema.json")
    if parent.get("packet_digest") != canonical_digest({k: v for k, v in parent.items() if k != "packet_digest"}):
        raise ContractError("synthesis revision parent packet digest mismatch")
    validate_packet_invariants(parent)
    for key in ("target_id", "run_id", "state_version"):
        if request.get(key) != parent.get(key):
            raise ContractError("synthesis revision crossed its parent identity")
    validate_sealed_preference_authority(evidence, target_id=parent["target_id"],
        run_id=parent["run_id"], state_version=parent["state_version"],
        system_ids=[row["system_id"] for row in parent["conceptual_systems"]],
        systems=parent["conceptual_systems"], reflection_rounds=parent["reflection_rounds"])
    rounds = request.get("reflection_rounds", [])
    prior_rounds = parent["reflection_rounds"]
    if len(rounds) <= len(prior_rounds) or rounds[:len(prior_rounds)] != prior_rounds:
        raise ContractError("synthesis revision must preserve its full parent history and append a real round")
    if request.get("generation_mode") != "operator_generated":
        raise ContractError("synthesis revision requires explicitly authored content")


def validate_reflection_round(item: Mapping[str, Any]) -> None:
    """Validate a round before it becomes immutable history for later authors."""
    result = item.get("result")
    mutation = item.get("mutation_or_synthesis", {})
    changed = mutation.get("changed_primitives_relations_or_explanation", [])
    if result in MATERIAL_RESULTS and not changed:
        raise ReflectionInvariantError(f"round {item.get('round_id')} claims {result} without structural change")
    if result == "no_change" and not str(item.get("no_change_reason") or "").strip():
        raise ReflectionInvariantError("no_change reflection requires an explicit reason")
    corrections = item.get("correction_tests", [])
    links = item.get("semantic_patch_links", [])
    if links and not corrections:
        raise ReflectionInvariantError(
            "semantic patch links require explicit round-level correction tests"
        )
    for link in links:
        if link.get("candidate_ref") not in item.get("system_ids", []):
            raise ReflectionInvariantError(
                "semantic patch link candidate must participate in its reflection round"
            )
        if link.get("objection") not in item.get("strongest_objections", []):
            raise ReflectionInvariantError(
                "semantic patch link must cite an exact objection from its reflection round"
            )
        if link.get("correction_test") not in corrections:
            raise ReflectionInvariantError(
                "semantic patch link must cite an exact correction test from its reflection round"
            )


def validate_reflection_rounds(rounds: list[Mapping[str, Any]], plateau: Mapping[str, Any]) -> None:
    """Require two effective rounds or an explicit two-round plateau/reframe."""

    if len(rounds) < 2:
        raise ReflectionInvariantError("conceptual discovery requires at least two reflection rounds")
    for item in rounds:
        validate_reflection_round(item)
    empty = sum(item.get("result") == "no_change" for item in rounds)
    if empty >= 2 and (plateau.get("materially_empty_rounds", 0) < 2 or plateau.get("action") != "reframe"):
        raise ReflectionInvariantError("two empty rounds must declare a reflective plateau and reframe")


def validate_unification(system: Mapping[str, Any]) -> None:
    """Reject unification that has no plurality or preserved difference."""

    unification = system.get("unification_claims", {})
    unified_cases = unification.get("source_case_ids") or unification.get(
        "unified_cases_or_routes", []
    )
    preserved_differences = unification.get("preserved_differences") or unification.get(
        "differences_preserved", []
    )
    if len(unified_cases) < 2:
        raise ReflectionInvariantError("preferred synthesis must unify at least two cases or routes")
    if not preserved_differences:
        raise ReflectionInvariantError("unification by erasure is forbidden")


def _dominates(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    """Return whether ``left`` Pareto-dominates ``right``."""

    return all(a >= b for a, b in zip(left, right, strict=True)) and any(
        a > b for a, b in zip(left, right, strict=True)
    )


def _structural_quality_vector(system: Mapping[str, Any]) -> tuple[int, ...]:
    """Return bounded, inspectable structural obligations—not a truth score.

    Strict adjudication systems expose source cases and typed preserved-difference
    witnesses, while historical/local fallback systems retain the compact field
    names.  Both are diagnostic inputs to this vector; neither can authorize a
    conceptual preference without the complete sealed adjudication object.
    """

    identity = system["structural_identity"]
    unification = system.get("unification_claims", {})
    unified_cases = unification.get("source_case_ids") or unification.get(
        "unified_cases_or_routes", []
    )
    preserved_differences = unification.get("preserved_differences") or unification.get(
        "differences_preserved", []
    )
    return (
        min(3, len(system.get("target_pressures_addressed", []))),
        min(3, len(system.get("transformation_operations", []))),
        min(3, len(identity.get("primitive_ids", [])) + len(identity.get("relation_ids", []))),
        min(3, len(system.get("formerly_inexpressible_now_visible", []))),
        min(3, len(unified_cases)),
        min(3, len(preserved_differences)),
        min(3, len(system.get("implications_and_new_questions", []))),
        min(3, len(system.get("protected_successes", [])) + int(bool(system.get("residual_contradictions")))),
        min(3, len(system.get("correction_conditions", [])) + len(system.get("formalization_seeds", []))),
    )


def build_pareto_assessment(systems: list[Mapping[str, Any]]) -> dict[str, Any]:
    """Compute a real partial order over explicit structural obligations.

    The vector is a deterministic screening surface, not a philosophical-quality
    oracle. Independent evaluation receipts remain necessary for conceptual
    preference.
    """

    assessments = []
    vectors = {str(system["system_id"]): _structural_quality_vector(system) for system in systems}
    nondominated = [
        system_id for system_id, vector in vectors.items()
        if not any(other_id != system_id and _dominates(other_vector, vector) for other_id, other_vector in vectors.items())
    ]
    dominated = []
    for system in systems:
        relevance = "pass" if system.get("target_pressures_addressed") else "fail"
        dimensions = {
            dimension: {
                "judgment": "strong" if dimension in {"essential_relevance", "root_tension_contact"} and relevance == "pass" else "open",
                "evidence": [
                    str(system.get("mechanism_or_principle", "")),
                    *(str(item) for item in system.get("target_pressures_addressed", [])[:2]),
                ],
            }
            for dimension in PARETO_DIMENSIONS
        }
        assessments.append({"system_id": system["system_id"], "relevance_floor": relevance, "dimensions": dimensions, "dominance_vector": dict(zip(PARETO_DIMENSIONS, vectors[str(system["system_id"])], strict=True)), "assessment_boundary": "Structural obligation coverage only; conceptual worth requires an independent evaluator receipt.", "decisive_strengths": list(system.get("formerly_inexpressible_now_visible", [])), "decisive_weaknesses": list(system.get("residual_contradictions", [])), "explicit_tradeoffs": list(system.get("correction_conditions", []))})
        if system["system_id"] not in nondominated or relevance == "fail" or system.get("lifecycle_state") in {"retired", "refuted"}:
            dominators = [other_id for other_id, other_vector in vectors.items() if other_id != system["system_id"] and _dominates(other_vector, vectors[str(system["system_id"])] )]
            dominated.append({"system_id": system["system_id"], "reason": "failed relevance/terminal or structurally Pareto-dominated", "dominated_by": dominators})
    nondominated = [system_id for system_id in nondominated if next(item for item in systems if item["system_id"] == system_id).get("target_pressures_addressed")]
    return {"dimension_definitions": list(PARETO_DIMENSIONS), "system_assessments": assessments, "nondominated_system_ids": nondominated, "dominated_or_demoted_systems": dominated}


def _ordered_union(rows: Iterable[Iterable[str]]) -> list[str]:
    return list(dict.fromkeys(value for row in rows for value in row))


def _validate_set_indexed_surfaces(
    packet: Mapping[str, Any],
    *,
    authority_ids: list[str],
    authority_status: str,
    investment_authorized: bool,
) -> None:
    """Reject hidden index-zero semantics in programmes and understanding deltas."""

    systems_by_id = {
        str(system["system_id"]): system for system in packet["conceptual_systems"]
    }
    retained = [systems_by_id[system_id] for system_id in authority_ids]
    programme = packet["theoretical_programme"]
    if (
        programme.get("authority_status") != authority_status
        or list(programme.get("conceptual_system_ids", [])) != authority_ids
        or programme.get("investment_authorized") is not investment_authorized
    ):
        raise ReflectionInvariantError(
            "theory programme does not preserve the complete authority set"
        )
    components = list(programme.get("component_programmes", []))
    if [row.get("conceptual_system_id") for row in components] != authority_ids:
        raise ReflectionInvariantError(
            "theory programme components are not an ordered bijection over the authority set"
        )
    programme_id = str(programme["programme_id"])
    for component, system in zip(components, retained, strict=True):
        system_id = str(system["system_id"])
        if component.get("component_programme_id") != stable_identifier(
            "programme-component", programme_id, system_id
        ):
            raise ReflectionInvariantError(
                "component programme identity does not bind its retained system"
            )
        expected_obligations = (
            list(system["formalization_seeds"]) if investment_authorized else []
        )
        if investment_authorized:
            expected_actions = list(
                dict.fromkeys(
                    [
                        *system["formalization_seeds"],
                        *system["implications_and_new_questions"][:2],
                    ]
                )
            )
        elif authority_status == "sealed_revise_all_diagnostic_only":
            expected_actions = [
                f"Revise {system_id}: {condition}"
                for condition in system["correction_conditions"]
            ]
        else:
            expected_actions = [
                f"Incubate {system_id}: {condition}"
                for condition in system["correction_conditions"]
            ]
        exact_fields = {
            "investment_authorized": investment_authorized,
            "definitions_to_build": list(system["primitives"]),
            "relations_or_mechanisms_to_formalize": list(
                system["relations_operations_and_dynamics"]
            ),
            "consequences_to_derive": list(system["implications_and_new_questions"]),
            "proof_or_model_obligations": expected_obligations,
            "next_theory_actions": expected_actions,
        }
        if any(component.get(key) != value for key, value in exact_fields.items()):
            raise ReflectionInvariantError(
                f"component programme for {system_id} differs from its exact system obligations"
            )
    aggregate_fields = (
        "definitions_to_build",
        "relations_or_mechanisms_to_formalize",
        "consequences_to_derive",
        "proof_or_model_obligations",
        "next_theory_actions",
    )
    for field in aggregate_fields:
        if programme.get(field) != _ordered_union(
            component[field] for component in components
        ):
            raise ReflectionInvariantError(
                f"aggregate theory programme {field} does not preserve all components"
            )
    if programme.get("literature_questions") != packet["literature_basis"].get(
        "literature_generated_questions", []
    ):
        raise ReflectionInvariantError(
            "set-indexed programme changed its exact literature questions"
        )

    delta = packet["understanding_delta"]
    if (
        delta.get("authority_status") != authority_status
        or list(delta.get("conceptual_system_ids", [])) != authority_ids
        or delta.get("authority_distinct_merit_evidence") is not False
        or delta.get("claim_boundary")
        != "internal_correlated_structural_change_only"
    ):
        raise ReflectionInvariantError(
            "understanding delta overstates or loses its set-valued internal boundary"
        )
    system_deltas = list(delta.get("system_deltas", []))
    if [row.get("conceptual_system_id") for row in system_deltas] != authority_ids:
        raise ReflectionInvariantError(
            "understanding deltas are not an ordered bijection over the authority set"
        )
    perspective_shifts = list(
        dict.fromkeys(
            str(row["mutation_or_synthesis"]["operation"])
            for row in packet["reflection_rounds"]
        )
    )
    for row, system in zip(system_deltas, retained, strict=True):
        expected = {
            "before": packet["discovery_charter"]["conceptual_opacity"],
            "after": system["formerly_inexpressible_now_visible"][0],
            "perspective_shifts": perspective_shifts,
            "explanatory_compressions": [system["mechanism_or_principle"]],
            "new_distinctions": list(system["identities_and_differences"]),
            "productive_contradictions": list(system["residual_contradictions"]),
            "remaining_opacity": list(system["correction_conditions"]),
        }
        if any(row.get(key) != value for key, value in expected.items()):
            raise ReflectionInvariantError(
                f"understanding delta for {system['system_id']} is not exact"
            )
    for field in (
        "perspective_shifts",
        "explanatory_compressions",
        "new_distinctions",
        "productive_contradictions",
        "remaining_opacity",
    ):
        if delta.get(field) != _ordered_union(row[field] for row in system_deltas):
            raise ReflectionInvariantError(
                f"aggregate understanding {field} loses a retained system"
            )


def validate_packet_invariants(packet: Mapping[str, Any]) -> None:
    """Validate theory-first, literature, diversity, reflection, and support invariants."""

    charter = packet["discovery_charter"]
    if charter["bottleneck_diagnosis"] == "not_conceptual":
        if packet["conceptual_systems"] or packet["reflection_rounds"]:
            raise ReflectionInvariantError("not_conceptual control must not invent rival systems or reflection")
        if packet["next_reflective_action"]["kind"] not in {"derive", "prove", "read", "empirical"}:
            raise ReflectionInvariantError("not_conceptual control must route to ordinary work")
        if packet.get("conceptual_adjudication_evidence") is not None or packet[
            "provisional_synthesis"
        ].get("preferred_system_ids"):
            raise ReflectionInvariantError(
                "not_conceptual control cannot carry conceptual preference authority"
            )
        if (
            packet["provisional_synthesis"].get("authority_status") != "not_conceptual"
            or packet["provisional_synthesis"].get("investment_authorized") is not False
            or packet["theoretical_programme"].get("authority_status") != "not_conceptual"
            or packet["theoretical_programme"].get("conceptual_system_ids") != []
            or packet["theoretical_programme"].get("component_programmes") != []
            or packet["understanding_delta"].get("authority_status") != "not_conceptual"
            or packet["understanding_delta"].get("conceptual_system_ids") != []
            or packet["understanding_delta"].get("system_deltas") != []
            or packet["understanding_delta"].get("authority_distinct_merit_evidence")
            is not False
        ):
            raise ReflectionInvariantError(
                "not_conceptual control must keep all conceptual authority surfaces empty"
            )
        return
    systems = packet["conceptual_systems"]
    if len(systems) < 3 or not systems_are_structurally_distinct(systems):
        raise ReflectionInvariantError("major conceptual cycle needs at least three structurally different systems")
    literature = packet["literature_basis"]
    if literature.get("snapshot_target_id") != packet["target_id"]:
        raise ReflectionInvariantError("literature snapshot target does not match the discovery target")
    high_risk = packet["high_risk_hypothesis_portfolio"]
    synthesis_contract = packet["provisional_synthesis"]
    preferred_ids = list(synthesis_contract.get("preferred_system_ids", []))
    diagnostic_ids = list(synthesis_contract.get("diagnostic_synthesis_system_ids", []))
    evidence = packet.get("conceptual_adjudication_evidence")
    system_ids = [str(item["system_id"]) for item in systems]
    sealed_preference: Mapping[str, Any] | None = None
    if evidence is None:
        if preferred_ids or synthesis_contract.get("preferred_system_id") is not None:
            raise ReflectionInvariantError(
                "conceptual preference requires sealed conceptual adjudication evidence"
            )
        if synthesis_contract.get("preference_authority_evidence_id") is not None:
            raise ReflectionInvariantError(
                "preference authority ID cannot exist without its sealed evidence object"
            )
    else:
        try:
            sealed_preference = validate_sealed_preference_authority(
                evidence,
                target_id=str(packet["target_id"]),
                run_id=str(packet["run_id"]),
                state_version=int(packet["state_version"]),
                system_ids=system_ids,
                systems=systems,
                reflection_rounds=packet["reflection_rounds"],
            )
        except ConceptualAdjudicationError as exc:
            raise ReflectionInvariantError(
                f"invalid sealed conceptual preference authority: {exc}"
            ) from exc
        if preferred_ids != list(sealed_preference["preferred_system_ids"]):
            raise ReflectionInvariantError(
                "packet preference set differs from sealed conceptual adjudication evidence"
            )
        if synthesis_contract.get("preference_authority_evidence_id") != evidence.get(
            "evidence_id"
        ):
            raise ReflectionInvariantError(
                "packet preference authority ID is not exactly bound to sealed evidence"
            )
    if sealed_preference is None:
        expected_status = "absent_diagnostic_only"
        expected_nondominated = diagnostic_ids
    elif sealed_preference["decision"] == "prefer_unique":
        expected_status = "sealed_unique"
        expected_nondominated = list(sealed_preference["nondominated_system_ids"])
        if diagnostic_ids:
            raise ReflectionInvariantError(
                "a unique sealed preference cannot retain diagnostic synthesis authority"
            )
    elif sealed_preference["decision"] == "retain_plural_nondominated":
        expected_status = "sealed_plural"
        expected_nondominated = list(sealed_preference["nondominated_system_ids"])
        if diagnostic_ids:
            raise ReflectionInvariantError(
                "a plural sealed preference cannot retain diagnostic synthesis authority"
            )
    else:
        expected_status = "sealed_revise_all_diagnostic_only"
        expected_nondominated = list(sealed_preference["nondominated_system_ids"])
        expected_diagnostics = expected_nondominated or system_ids
        if diagnostic_ids != expected_diagnostics:
            raise ReflectionInvariantError(
                "revise_all must retain the complete nondominated diagnostic set"
            )
    if (
        synthesis_contract.get("authority_status") != expected_status
        or synthesis_contract.get("investment_authorized") is not bool(preferred_ids)
        or list(synthesis_contract.get("nondominated_system_ids", []))
        != expected_nondominated
    ):
        raise ReflectionInvariantError(
            "synthesis authority status does not equal the sealed preference algebra"
        )
    expected_singular = preferred_ids[0] if len(preferred_ids) == 1 else None
    if synthesis_contract.get("preferred_system_id") != expected_singular:
        raise ReflectionInvariantError(
            "singular preferred_system_id is permitted only for a unique sealed preference"
        )
    if set(preferred_ids) & set(diagnostic_ids):
        raise ReflectionInvariantError(
            "a system cannot be both sealed-preferred and diagnostic-only"
        )
    if not set(preferred_ids + diagnostic_ids).issubset(set(system_ids)):
        raise ReflectionInvariantError(
            "preferred or diagnostic synthesis does not resolve to a conceptual system"
        )
    if not preferred_ids and not diagnostic_ids:
        raise ReflectionInvariantError(
            "conceptual packet must retain at least one diagnostic incubation candidate"
        )
    active_synthesis = bool(preferred_ids)
    authority_ids = preferred_ids or diagnostic_ids
    _validate_set_indexed_surfaces(
        packet,
        authority_ids=authority_ids,
        authority_status=expected_status,
        investment_authorized=active_synthesis,
    )
    if active_synthesis:
        if literature["freshness_status"] != "current" or not literature["search_receipt_ids"] or not literature["assimilation_packet_ref"]:
            raise ReflectionInvariantError("active synthesis requires current receipt-backed target literature")
        if high_risk["literature_rebase_status"] != "current":
            raise ReflectionInvariantError("active portfolio must be literature-rebased")
    if high_risk["disposition"] != "not_requested":
        if len(set(high_risk["corner_families"])) < 6:
            raise ReflectionInvariantError("major high-risk portfolio requires six genuine corner families")
        if len(high_risk["protected_wildcard_ids"]) < 2:
            raise ReflectionInvariantError("major high-risk portfolio must preserve two wildcards when available")
    validate_reflection_rounds(packet["reflection_rounds"], packet["plateau"])
    retained_outcomes = [
        item for item in systems if item["system_id"] in set(preferred_ids or diagnostic_ids)
    ]
    for retained in retained_outcomes:
        validate_unification(retained)
        if not retained.get("correction_conditions") or not retained.get("non_claims"):
            raise ReflectionInvariantError(
                "retained synthesis must expose correction conditions and non-claims"
            )
    delta = packet["understanding_delta"]
    if delta["before"].strip() == delta["after"].strip() or not (delta["perspective_shifts"] or delta["new_distinctions"]):
        raise ReflectionInvariantError("understanding delta must state a material before/after change")
    if not packet["theoretical_programme"]["next_theory_actions"]:
        raise ReflectionInvariantError("preferred programme must generate consequential next actions")
    support = packet["support_probe"]
    if active_synthesis:
        if support.get("theory_programme_id") != packet["theoretical_programme"].get(
            "programme_id"
        ) or list(support.get("conceptual_system_ids", [])) != preferred_ids:
            raise ReflectionInvariantError(
                "support must bind the complete ordered sealed preference set"
            )
    elif (
        support.get("disposition") != "no_probe_needed"
        or support.get("theory_programme_id") is not None
        or support.get("conceptual_system_ids")
    ):
        raise ReflectionInvariantError(
            "diagnostic and revise-all outcomes cannot authorize a support probe"
        )
    if support["disposition"] in {"commissioned", "assimilated"}:
        required = (support.get("theory_programme_id"), support.get("theoretical_question_id"), support.get("theoretical_question"), support.get("receipt_ids"))
        if not all(required):
            raise ReflectionInvariantError("commissioned support must cite programme, question, and receipts")
        if support["disposition"] == "assimilated" and not support["reflective_assimilation_event_ids"]:
            raise ReflectionInvariantError("support result must return through reflective assimilation")
    elif support["disposition"] == "no_probe_needed" and support["receipt_ids"]:
        raise ReflectionInvariantError("no_probe_needed cannot fabricate experiment receipts")
    if (
        packet["stage_gates"]["G2_philosophical_depth"] == "pass"
        or packet["stage_gates"]["G4_understanding_gain"] == "pass"
    ):
        raise ReflectionInvariantError(
            "internal correlated preference cannot certify philosophical depth or understanding"
        )
    mode = packet.get("generation_mode")
    if mode == "local_structural_fallback":
        if preferred_ids or packet["truth_convergence_status"]["conceptual_preference"].startswith(("theoretically_preferred", "sealed_preference_set")):
            raise ReflectionInvariantError("local structural fallback must remain incubating")
    if packet.get("independent_evaluation_evidence"):
        raise ReflectionInvariantError(
            "legacy evaluation bundles are diagnostic only and cannot enter the preference contract"
        )
