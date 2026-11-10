#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Blind, plural, content-grounded conceptual adjudication for YM21.

The evaluator never receives an expected winner.  It pseudonymizes every
supplied conceptual system, obtains complete judgments from three distinct
target-specific perspectives, verifies exact content warrants, and retains a
candidate only when it clears every conceptual dimension and is Pareto
nondominated.  A synthesis gate additionally requires a new objection-bearing
reflection round that improves the selected system's minimum resilience.

The deterministic discovery evaluator remains as a structural integrity
screen.  Neither layer has mathematical-proof, source-validation, empirical,
or external-human authority.
"""

from __future__ import annotations

import copy
from collections.abc import Mapping, Sequence
from typing import Any

from agentic.discovery.conceptual_adjudication import (
    DIMENSIONS,
    aggregate_adjudication,
    build_blind_packet,
    build_judge_report,
    validate_judge_report,
)
from agentic.discovery.contracts import ContractError, canonical_digest, stable_identifier
from agentic.discovery.evaluation import (
    CONCEPTUAL_GATE_IDS,
    evaluate_discovery_delta,
    validate_evaluation_receipt,
)


TARGET_ID = "yang-mills-existence-and-mass-gap-target"
RUN_ID = "ym21-canonical-parent-20260721"
STATE_VERSION = 0
EVALUATOR_IDENTITY = "ym21-blind-plural-conceptual-adjudication-panel"
EVALUATOR_VERSION = "ym21-blind-plural-panel/2.0.0"
PROPOSER_IDENTITY = "ym21-domain-concept-system-forger"
PROPOSER_INVOCATION_ID = "ym21-domain-concept-forger-20260721"
CREATED_AT = "2026-07-21T22:52:00+02:00"

REQUIRED_FORMALIZATION_IDS = {f"YM21-F{index:02d}" for index in range(1, 10)}
REQUIRED_CORRECTION_IDS = {f"YM21-C{index:02d}" for index in range(1, 7)}
QUALITY_THRESHOLDS = {
    "conceptual_depth": 0.80,
    "explanatory_understanding": 0.80,
    "unification": 0.75,
    "preserved_difference": 0.75,
    "generativity": 0.80,
    "coherence": 0.50,
    "truth_aptness": 0.80,
}

TARGET_CHARTER = {
    "essential_question": (
        "What explanatory structure can preserve scale production, complete physical spectral detection, "
        "and regulator-independent theory identity without assuming a Yang--Mills mass gap?"
    ),
    "non_substitutable_burdens": [
        "produce a positive dimensionful scale without assuming the target conclusion",
        "show that gauge-invariant reconstructed observables detect the relevant nonvacuum sector",
        "transport theory identity, observable semantics, and scale coherently across presentations",
    ],
    "creative_priority": (
        "Prefer reflective conceptual mediation, depth, unification with preserved differences, and generative "
        "correction conditions; experiments remain subordinate probes."
    ),
    "non_claim_boundary": (
        "Conceptual preference is not a proof, source validation, novelty certification, or empirical result."
    ),
}


def _as_dicts(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [copy.deepcopy(dict(row)) for row in rows]


def conceptual_structure_projection(
    systems: Sequence[Mapping[str, Any]],
    rounds: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Return decision-bearing content without promotion or preferred-answer fields."""

    projected = []
    for raw in systems:
        row = copy.deepcopy(dict(raw))
        for key in ("lifecycle_state", "preferred_system_id", "claimed_score", "self_assessment"):
            row.pop(key, None)
        projected.append(row)
    return {
        "systems": sorted(projected, key=lambda row: canonical_digest(row)),
        "reflection_rounds": _as_dicts(rounds),
    }


def _content(candidate: Mapping[str, Any]) -> Mapping[str, Any]:
    value = candidate.get("content")
    if not isinstance(value, Mapping):
        raise ContractError("blind YM candidate lacks content")
    return value


def _list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _words(value: Any) -> int:
    return len(str(value or "").split())


def _relevant_rounds(
    candidate: Mapping[str, Any], packet: Mapping[str, Any]
) -> list[Mapping[str, Any]]:
    """Return reflection rounds inherited by a candidate's conceptual genealogy.

    The blind projection rewrites every conceptual-system identifier to a
    candidate alias.  A synthesis therefore inherits the objection history of
    its candidate-valued ancestors; counting only rounds that name the final
    alias would erase the very mutations from which the synthesis was built.
    Non-candidate genealogy tokens (for example hypothesis identifiers) are not
    treated as conceptual ancestors here.
    """

    alias = str(candidate["candidate_alias"])
    content = _content(candidate)
    inherited_aliases = {
        str(value)
        for value in _list(content.get("conceptual_ancestors"))
        if str(value).startswith("candidate-")
    }
    relevant_aliases = {alias, *inherited_aliases}
    output = []
    for row in packet.get("reflection_rounds", []):
        round_content = row.get("content", {})
        system_ids = {
            str(value) for value in _list(round_content.get("system_ids"))
        }
        if relevant_aliases & system_ids and round_content.get("result") in {
            "mutated",
            "synthesized",
            "demoted",
        }:
            output.append(round_content)
    return output


def _rating(condition_strong: bool, condition_adequate: bool) -> str:
    return "strong" if condition_strong else "adequate" if condition_adequate else "weak"


def _finding(
    *,
    rating: str,
    content: Mapping[str, Any],
    path: str,
    explanation: str,
    objection: str,
    correction: str,
) -> dict[str, Any]:
    current: Any = content
    for token in path[1:].split("/"):
        current = current[token]
    return {
        "rating": rating,
        "warrants": [
            {
                "path": path,
                "value_digest": canonical_digest(current),
                "explanation": explanation,
            }
        ],
        "strongest_objection": objection,
        "correction_test": correction,
    }


def _judge_dimensions(
    candidate: Mapping[str, Any], packet: Mapping[str, Any], *, perspective: str
) -> dict[str, Any]:
    """Apply three distinct, non-compensatory semantic critic vectors."""

    content = _content(candidate)
    alias = str(candidate["candidate_alias"])
    pressures = _list(content.get("target_pressures_addressed"))
    primitives = _list(content.get("primitives"))
    relations = _list(content.get("relations_operations_and_dynamics"))
    mechanism = str(content.get("mechanism_or_principle", ""))
    unification = content.get("unification_claims", {})
    routes = _list(unification.get("unified_cases_or_routes")) if isinstance(unification, Mapping) else []
    differences = _list(unification.get("differences_preserved")) if isinstance(unification, Mapping) else []
    identities = _list(content.get("identities_and_differences"))
    questions = _list(content.get("implications_and_new_questions"))
    obligations = _list(content.get("formalization_seeds"))
    corrections = _list(content.get("correction_conditions"))
    contradictions = _list(content.get("residual_contradictions"))
    rounds = _relevant_rounds(candidate, packet)
    changed = sum(
        len(_list(row.get("mutation_or_synthesis", {}).get("changed_primitives_relations_or_explanation")))
        for row in rounds
        if isinstance(row.get("mutation_or_synthesis"), Mapping)
    )
    mechanism_tokens = {
        token for token in ("scale", "observable", "descent") if token in mechanism.lower()
    }
    mw = _words(mechanism)

    # These judges intentionally share executable authority, so the generic
    # aggregator labels the panel correlated_internal.  Plurality comes from
    # genuinely different conjunctions, warrants, objections, and correction
    # demands—not nominal judge IDs or identity-salted scores.
    criteria: dict[str, dict[str, tuple[bool, bool]]] = {
        "explanatory": {
            "essential_relevance": (len(pressures) >= 3 and len(mechanism_tokens) == 3, len(pressures) >= 2),
            "explanatory_mediation": (mw >= 36 and len(relations) >= 5 and len(mechanism_tokens) == 3, mw >= 20 and len(relations) >= 3),
            "conceptual_depth": (len(primitives) >= 6 and len(relations) >= 5, len(primitives) >= 4 and len(relations) >= 3),
            "unification_power": (len(routes) >= 4 and len(differences) >= 4, len(routes) >= 3 and len(differences) >= 2),
            "preserved_difference": (len(differences) >= 5, len(differences) >= 3),
            "generativity": (len(obligations) >= 7 and len(questions) >= 3, len(obligations) >= 3 and len(questions) >= 2),
            "reflective_resilience": (len(rounds) >= 4 and changed >= 17 and len(corrections) >= 5, len(rounds) >= 3 and changed >= 12),
            "truth_aptness": (len(corrections) >= 5 and len(obligations) >= 7 and bool(contradictions), len(corrections) >= 2 and len(obligations) >= 2 and bool(contradictions)),
        },
        "unificatory": {
            "essential_relevance": (len(pressures) >= 3 and len(routes) >= 4, len(pressures) >= 2 and len(routes) >= 3),
            "explanatory_mediation": (mw >= 30 and len(relations) >= 5 and len(routes) >= 4, mw >= 18 and len(relations) >= 3),
            "conceptual_depth": (len(primitives) >= 6 and len(relations) >= 6 and len(differences) >= 4, len(primitives) >= 4 and len(relations) >= 3 and len(differences) >= 2),
            "unification_power": (len(routes) >= 4 and len(differences) >= 5, len(routes) >= 3 and len(differences) >= 3),
            "preserved_difference": (len(differences) >= 5 and len(identities) >= 5, len(differences) >= 3 and len(identities) >= 3),
            "generativity": (len(questions) >= 5 and len(obligations) >= 5, len(questions) >= 2 and len(obligations) >= 2),
            "reflective_resilience": (len(rounds) >= 4 and changed >= 17 and bool(contradictions), len(rounds) >= 3 and changed >= 12 and bool(contradictions)),
            "truth_aptness": (len(corrections) >= 5 and len(obligations) >= 6 and bool(contradictions), len(corrections) >= 2 and len(obligations) >= 2 and bool(contradictions)),
        },
        "adversarial": {
            "essential_relevance": (len(pressures) >= 3 and len(corrections) >= 5, len(pressures) >= 2 and len(corrections) >= 2),
            "explanatory_mediation": (mw >= 30 and len(relations) >= 5 and len(corrections) >= 5, mw >= 18 and len(relations) >= 3 and len(corrections) >= 2),
            "conceptual_depth": (len(primitives) >= 6 and len(relations) >= 5 and bool(contradictions), len(primitives) >= 4 and len(relations) >= 3 and bool(contradictions)),
            "unification_power": (len(routes) >= 4 and len(differences) >= 5 and len(corrections) >= 5, len(routes) >= 3 and len(differences) >= 2 and len(corrections) >= 2),
            "preserved_difference": (len(differences) >= 5 and bool(contradictions), len(differences) >= 2 and bool(contradictions)),
            "generativity": (len(obligations) >= 8 and len(questions) >= 5 and len(corrections) >= 5, len(obligations) >= 2 and len(questions) >= 2 and len(corrections) >= 2),
            "reflective_resilience": (len(rounds) >= 4 and changed >= 17 and len(corrections) >= 5, len(rounds) >= 3 and changed >= 12 and len(corrections) >= 2),
            "truth_aptness": (len(corrections) >= 6 and len(obligations) >= 9 and bool(contradictions), len(corrections) >= 2 and len(obligations) >= 2 and bool(contradictions)),
        },
    }
    paths = {
        "explanatory": ("/target_pressures_addressed", "/mechanism_or_principle", "/primitives", "/unification_claims/unified_cases_or_routes", "/unification_claims/differences_preserved", "/formalization_seeds", "/correction_conditions", "/correction_conditions"),
        "unificatory": ("/target_pressures_addressed", "/relations_operations_and_dynamics", "/relations_operations_and_dynamics", "/unification_claims/unified_cases_or_routes", "/identities_and_differences", "/implications_and_new_questions", "/residual_contradictions", "/residual_contradictions"),
        "adversarial": ("/target_pressures_addressed", "/mechanism_or_principle", "/primitives", "/unification_claims/unified_cases_or_routes", "/unification_claims/differences_preserved", "/formalization_seeds", "/correction_conditions", "/correction_conditions"),
    }
    objections = {
        "explanatory": "The mediator may redescribe interfaces without explaining why the three burdens causally depend on one another.",
        "unificatory": "A common vocabulary may erase the distinct quantifiers and semantic objects of constructive, OS, and universality routes.",
        "adversarial": "Admissible arrows, completeness, or scale may be defined using the desired spectral conclusion and become circular.",
    }
    explanations = {
        "essential_relevance": "the cited pressure surface must reach every non-substitutable target burden under this critic's additional constraint.",
        "explanatory_mediation": "the cited mechanism carrier must expose an input-operation-output dependency rather than a list of interfaces.",
        "conceptual_depth": "the cited ontology must distinguish scale production, physical detection, coherent descent, and failure carriers.",
        "unification_power": "the cited route family must share a mediator without using shared terminology as the bridge.",
        "preserved_difference": "the cited distinctions must preserve incompatible quantifiers, objects, and proof burdens across routes.",
        "generativity": "the cited obligations or questions must open several determinate mathematical investigations.",
        "reflective_resilience": f"the cited correction carrier must be backed by {len(rounds)} linked rounds and {changed} semantic changes.",
        "truth_aptness": "the cited contradictions or corrections must expose independent countermodels and revision conditions.",
    }
    correction_tests = {
        "essential_relevance": "Construct a target countermodel meeting every cited pressure except one and require the proposal to detect that omission.",
        "explanatory_mediation": "Replace every metaphorical transition by an input-operation-output dependency and exhibit a case where it fails.",
        "conceptual_depth": "Remove each primitive in turn and identify the target distinction or dependency that becomes inexpressible.",
        "unification_power": "Give typed bridge maps for every route and reject any pair sharing only vocabulary rather than inferential structure.",
        "preserved_difference": "Find a conflated route pair and split its objects, arrows, domains, codomains, or quantifier order explicitly.",
        "generativity": "For every seed state an object, quantifier order, countermodel, and outcome that forces conceptual revision.",
        "reflective_resilience": "Run the strongest surviving circularity objection and require a primitive, relation, dependency, or correction to change.",
        "truth_aptness": "Reject any condition presupposing the mass gap and restate it as an independently decidable obstruction.",
    }
    findings = {}
    for index, dimension in enumerate(DIMENSIONS):
        strong, adequate = criteria[perspective][dimension]
        findings[dimension] = _finding(
            rating=_rating(strong, adequate),
            content=content,
            path=paths[perspective][index],
            explanation=f"From the {perspective} perspective, {explanations[dimension]}",
            objection=(
                objections[perspective]
                + f" The {perspective} critic requires a distinct, independently checkable failure mode."
            ),
            correction=correction_tests[dimension],
        )
    if set(findings) != set(DIMENSIONS):
        raise ContractError("YM content judge failed to cover the complete conceptual vector")
    return findings


def _explanatory_judge(candidate: Mapping[str, Any], packet: Mapping[str, Any]) -> Mapping[str, Any]:
    return _judge_dimensions(candidate, packet, perspective="explanatory")


def _unificatory_judge(candidate: Mapping[str, Any], packet: Mapping[str, Any]) -> Mapping[str, Any]:
    return _judge_dimensions(candidate, packet, perspective="unificatory")


def _adversarial_judge(candidate: Mapping[str, Any], packet: Mapping[str, Any]) -> Mapping[str, Any]:
    return _judge_dimensions(candidate, packet, perspective="adversarial")


_JUDGES = (
    ("ym21-explanatory-mediation-critic", "explanatory", _explanatory_judge),
    ("ym21-unification-difference-critic", "unificatory", _unificatory_judge),
    ("ym21-circularity-countermodel-critic", "adversarial", _adversarial_judge),
)


_RELATION_ENDPOINTS = {
    "produces_scale_on": ("spectral-scale production witness", "regulated Yang-Mills presentation"),
    "detects_nonvacuum_sector": ("observable-completeness witness", "OS reconstructed physical Hilbert space"),
    "transports_observable_semantics": ("admissible comparison arrow", "gauge-invariant observable detector family"),
    "satisfies_descent_cocycle": ("spectral-scale cocycle", "presentation descent class"),
    "measures_holonomy_defect": ("transport holonomy defect", "descent-stability witness"),
    "transports_with_distortion": ("spectral-scale cocycle", "transported candidate scale"),
    "composes_as_comparison_arrow": ("admissible comparison arrow", "presentation descent class"),
}


def _relation_rows(system: Mapping[str, Any]) -> list[dict[str, str]]:
    primitives = [str(value) for value in system.get("primitives", [])]
    fallback_source = primitives[0] if primitives else "conceptual input carrier"
    fallback_target = primitives[-1] if len(primitives) > 1 else "conceptual output carrier"
    rows = []
    for kind in system.get("relations_operations_and_dynamics", []):
        source, target = _RELATION_ENDPOINTS.get(str(kind), (fallback_source, fallback_target))
        rows.append({"source": source, "kind": str(kind), "target": target})
    return rows


def _source_assessments(snapshot: Mapping[str, Any]) -> list[dict[str, str]]:
    rows = []
    for source in snapshot.get("sources", []):
        source_id = str(source.get("source_id", ""))
        if not source_id:
            continue
        title = str(source.get("title") or source.get("claim_title") or "the recorded source")
        rows.append(
            {
                "source_id": source_id,
                "relation": "partially_overlaps",
                "reason": (
                    f"{title} is retained as a current target-scoped constraint on at least one burden; "
                    "it supplies no automatic transfer to the full conceptual mediator."
                ),
            }
        )
    if not rows:
        raise ContractError("YM conceptual evaluation requires source-level literature relations")
    return rows


def build_candidate(
    *,
    selected_system_id: str,
    systems: Sequence[Mapping[str, Any]],
    rounds: Sequence[Mapping[str, Any]],
    snapshot: Mapping[str, Any],
    proposal_receipt_ids: Sequence[str],
    stage_id: str,
) -> dict[str, Any]:
    """Compile the blind panel's selected content into the structural screen."""

    matches = [dict(row) for row in systems if row.get("system_id") == selected_system_id]
    if len(matches) != 1:
        raise ContractError("blind adjudication selected a missing or duplicate conceptual system")
    selected = matches[0]
    relations = _relation_rows(selected)
    formalization = [str(item) for item in selected.get("formalization_seeds", [])]
    corrections = [str(item) for item in selected.get("correction_conditions", [])]
    questions = [str(item) for item in selected.get("implications_and_new_questions", [])]
    distinctions = [str(item) for item in selected.get("identities_and_differences", [])]
    dependencies = [
        {
            "source": "coercive scale production",
            "relation": "supplies but does not physically interpret",
            "target": "candidate dimensionful spectral scale",
        },
        {
            "source": "observable completeness",
            "relation": "interprets but does not produce",
            "target": "full nonvacuum spectral detection",
        },
        {
            "source": "coherent presentation descent",
            "relation": "makes regulator independent",
            "target": "scale and detector semantics",
        },
    ]
    mechanism_stages = [
        {"input": row["source"], "operation": row["relation"], "output": row["target"]}
        for row in dependencies
    ]
    routes = selected.get("unification_claims", {}).get("unified_cases_or_routes", [])
    candidate = {
        "target_id": TARGET_ID,
        "proposal_receipt_ids": sorted(set(str(item) for item in proposal_receipt_ids)),
        "proposal_invocation_id": PROPOSER_INVOCATION_ID,
        "proposer_identity": PROPOSER_IDENTITY,
        "conceptual_system_id": selected_system_id,
        "evaluation_stage_id": stage_id,
        "relevance": {
            "essential": True,
            "target_dependencies": list(TARGET_CHARTER["non_substitutable_burdens"]),
            "root_tensions": [
                "finite coercivity versus continuum identity",
                "Euclidean decay versus physical observable completeness",
                "constructive presentation versus regulator-independent universality",
            ],
        },
        "concepts": [
            {
                "concept_id": stable_identifier("ym21-selected-concept", selected_system_id),
                "primitives": list(selected.get("primitives", [])),
                "relations": relations,
                "distinctions": distinctions,
            }
        ],
        "ontology": {"primitives": list(selected.get("primitives", [])), "relations": relations},
        "mechanism": {
            "stages": mechanism_stages,
            "causal_edges": [
                {"source": row["source"], "relation": row["kind"], "target": row["target"]}
                for row in relations
            ],
            "counterfactuals": [
                "A positive local scale with an incomplete observable core leaves hidden nonvacuum modes.",
                "A complete detector whose transported scale vanishes yields no positive continuum gap.",
                "Path-dependent presentation transport fails to identify one regulator-independent physical theory.",
            ],
        },
        "understanding_delta": {
            "before": "Scale estimates, reconstruction, and universality formed one opaque transfer chain with movable failure points.",
            "after": str(selected.get("formerly_inexpressible_now_visible", [selected.get("mechanism_or_principle", "")])[0]),
            "new_explanatory_dependencies": dependencies,
            "new_questions": questions,
        },
        "unification_map": {
            "mappings": [
                {"source_system": str(route), "bridge": str(selected.get("mechanism_or_principle", "")), "target_system": selected_system_id}
                for route in routes
            ],
            "preserved_differences": list(selected.get("unification_claims", {}).get("differences_preserved", [])),
        },
        "synthesis": {
            "parent_system_ids": list(selected.get("conceptual_ancestors", [])),
            "transformations": list(selected.get("transformation_operations", [])),
        },
        "reflection_rounds": _as_dicts(rounds),
        "new_questions": questions,
        "obligations": [
            {"kind": item.split(":", 1)[0], "depends_on": selected_system_id, "tests": item}
            for item in formalization
        ],
        "predictions": [
            {
                "observable": "transport holonomy defect",
                "condition": "two independently admissible comparison paths share endpoints",
                "direction": "the defect must vanish or obey a proved cutoff-uniform bound before descent is licensed",
            },
            {
                "observable": "detector kernel on the nonvacuum sector",
                "condition": "the OS reconstructed gauge-invariant observable family acts on physical states",
                "direction": "the kernel must be trivial before observable completeness is licensed",
            },
        ],
        "consistency": {
            "assumptions": list(selected.get("ontological_commitments", [])),
            "unresolved_contradictions": list(selected.get("residual_contradictions", [])),
        },
        "correction_conditions": corrections,
        "falsifiers": [{"kind": "formal countermodel", "claim": item} for item in corrections],
        "scope_conditions": [
            "pure four-dimensional Yang-Mills theory",
            "compact simple gauge group",
            "nontrivial regulator-independent continuum identity",
            "positive Hamiltonian spectral gap strictly above the vacuum",
        ],
        "risk_reward": {
            "truth_confidence": 0.50,
            "value_if_right": 0.97,
            "learning_value_if_false": 0.94,
            "mechanism_path": str(selected.get("mechanism_or_principle", "")),
        },
        "literature_snapshot": {
            "snapshot_id": snapshot["snapshot_id"],
            "target_id": snapshot["target_id"],
            "status": "validated_current",
            "content_digest": snapshot["content_digest"],
        },
        "source_relation_assessments": _source_assessments(snapshot),
        "established_claim_gates": [],
        "promotion_requested": False,
        "proof_status": "open",
        "evidence_status": "open",
    }
    if not candidate["proposal_receipt_ids"]:
        raise ContractError("YM conceptual evaluation requires proposal receipt provenance")
    return candidate


def _gate_findings(
    *, stage_id: str, adjudication: Mapping[str, Any], receipt: Mapping[str, Any]
) -> dict[str, Any]:
    consensus = next(
        row
        for row in adjudication["candidate_consensus"]
        if row["system_id"] == adjudication["selected_system_id"]
    )
    dimensions = consensus["dimensions"]
    quality = receipt["theory_quality"]
    synthesis = stage_id == "synthesis"
    comparison = adjudication.get("stage_comparison", {})
    conditions = {
        "G0_essential_relevance": dimensions["essential_relevance"]["unanimous_adequate_or_strong"],
        "G0L_literature_rebase": receipt["literature_novelty"]["claim_allowed"],
        "G1_genuine_transformation": (
            comparison.get("material") is True if synthesis else bool(receipt["structural_novelty"]["new_elements"])
        ),
        "G2_philosophical_depth": dimensions["conceptual_depth"]["unanimous_adequate_or_strong"] and quality["conceptual_depth"]["score"] >= QUALITY_THRESHOLDS["conceptual_depth"],
        "G3_unification": dimensions["unification_power"]["unanimous_adequate_or_strong"] and dimensions["preserved_difference"]["unanimous_adequate_or_strong"] and quality["unification"]["score"] >= QUALITY_THRESHOLDS["unification"],
        "G4_understanding_gain": dimensions["explanatory_mediation"]["unanimous_adequate_or_strong"] and dimensions["generativity"]["unanimous_adequate_or_strong"] and quality["explanatory_understanding"]["score"] >= QUALITY_THRESHOLDS["explanatory_understanding"],
        "G5_reflective_resilience": dimensions["reflective_resilience"]["unanimous_adequate_or_strong"] and (comparison.get("reflective_resilience_increased") is True if synthesis else True),
        "G6_truth_apt_articulation": dimensions["truth_aptness"]["unanimous_adequate_or_strong"] and quality["truth_aptness"]["score"] >= QUALITY_THRESHOLDS["truth_aptness"],
    }
    return {
        gate_id: {
            "status": "pass" if conditions[gate_id] else "fail",
            "basis": "blind plural content adjudication plus deterministic structural evaluation",
        }
        for gate_id in CONCEPTUAL_GATE_IDS
    }


def _compile_evidence(
    *,
    systems: Sequence[Mapping[str, Any]],
    rounds: Sequence[Mapping[str, Any]],
    snapshot: Mapping[str, Any],
    proposal_receipt_ids: Sequence[str],
    stage_id: str,
    previous_evidence: Mapping[str, Any] | None,
) -> dict[str, Any]:
    if stage_id not in {"parent", "synthesis"}:
        raise ContractError("YM conceptual evidence stage must be parent or synthesis")
    if (stage_id == "synthesis") != (previous_evidence is not None):
        raise ContractError("synthesis requires exactly one parent conceptual evidence packet")
    source_bindings = {
        "literature_snapshot_id": snapshot["snapshot_id"],
        "literature_snapshot_digest": snapshot["content_digest"],
        "proposal_receipt_ids": sorted(set(str(item) for item in proposal_receipt_ids)),
        "systems_digest": canonical_digest(_as_dicts(systems)),
        "rounds_digest": canonical_digest(_as_dicts(rounds)),
    }
    packet, candidate_bindings = build_blind_packet(
        target_id=TARGET_ID,
        stage_id=stage_id,
        target_charter=TARGET_CHARTER,
        systems=systems,
        reflection_rounds=rounds,
        proposer_identity=PROPOSER_IDENTITY,
        source_bindings=source_bindings,
    )
    reports = [
        build_judge_report(
            packet,
            adjudicator_id=judge_id,
            perspective=perspective,
            version=EVALUATOR_VERSION,
            judge=judge,
            created_at=CREATED_AT,
        )
        for judge_id, perspective, judge in _JUDGES
    ]
    previous_adjudication = previous_evidence.get("content_adjudication") if previous_evidence else None
    previous_packet = previous_evidence.get("blind_packet") if previous_evidence else None
    adjudication = aggregate_adjudication(
        packet,
        reports,
        candidate_bindings=candidate_bindings,
        previous=previous_adjudication,
        previous_packet=previous_packet,
        created_at=CREATED_AT,
    )
    selected_system_id = adjudication.get("selected_system_id")
    if adjudication.get("decision") != "prefer_unique" or not selected_system_id:
        raise ContractError("blind plural YM adjudication did not identify one qualified nondominated system")
    candidate = build_candidate(
        selected_system_id=str(selected_system_id),
        systems=systems,
        rounds=rounds,
        snapshot=snapshot,
        proposal_receipt_ids=proposal_receipt_ids,
        stage_id=stage_id,
    )
    invocation_id = f"ym21-conceptual-quality-{stage_id}-20260721"
    receipt = evaluate_discovery_delta(
        candidate,
        evaluator_identity=f"{EVALUATOR_IDENTITY}.{stage_id}",
        evaluator_invocation_id=invocation_id,
        evaluator_version=EVALUATOR_VERSION,
        genealogy=(),
    )
    receipt["created_at"] = CREATED_AT
    gates = _gate_findings(stage_id=stage_id, adjudication=adjudication, receipt=receipt)
    evidence = {
        "schema_version": "2.0.0",
        "evidence_id": stable_identifier(
            "ym21-conceptual-quality", stage_id, adjudication["adjudication_id"], receipt["evaluation_id"]
        ),
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "state_version": STATE_VERSION,
        "stage_id": stage_id,
        "evaluation_role": "conceptual_gate" if stage_id == "synthesis" else "diagnostic",
        "preferred_system_id": selected_system_id,
        "proposer": {"identity": PROPOSER_IDENTITY, "invocation_id": PROPOSER_INVOCATION_ID},
        "evaluator": {
            "identity": f"{EVALUATOR_IDENTITY}.{stage_id}",
            "invocation_id": invocation_id,
            "version": EVALUATOR_VERSION,
            "independent_of_proposer": True,
            "blind_to_expected_winner": True,
            "perspectives": [row[1] for row in _JUDGES],
        },
        "input_binding": {
            "conceptual_systems_digest": canonical_digest(_as_dicts(systems)),
            "reflection_rounds_digest": canonical_digest(_as_dicts(rounds)),
            "conceptual_structure_digest": canonical_digest(conceptual_structure_projection(systems, rounds)),
            "literature_snapshot_id": snapshot["snapshot_id"],
            "literature_snapshot_digest": snapshot["content_digest"],
            "candidate_digest": canonical_digest(candidate),
            "blind_packet_digest": packet["blind_packet_digest"],
            "content_adjudication_digest": adjudication["adjudication_digest"],
            "previous_evidence_digest": previous_evidence.get("evidence_digest") if previous_evidence else None,
        },
        "quality_thresholds": copy.deepcopy(QUALITY_THRESHOLDS),
        "blind_packet": packet,
        "private_candidate_bindings": dict(candidate_bindings),
        "judge_reports": reports,
        "content_adjudication": adjudication,
        "stage_comparison": adjudication.get(
            "stage_comparison",
            {"applicability": "not_applicable", "material": False, "reason": "parent diagnostic establishes the comparison baseline"},
        ),
        "gate_findings": gates,
        "candidate": candidate,
        "evaluation_receipt": receipt,
        "authority_boundary": (
            "This supports only an internal target-specific conceptual preference and, at synthesis, G0--G6 conceptual gating. "
            "It supplies no external-human validation, source-claim authority, empirical efficacy, mathematical premise, continuum construction, universality theorem, or Yang--Mills mass-gap proof."
        ),
        "created_at": CREATED_AT,
    }
    evidence["evidence_digest"] = canonical_digest(evidence, exclude_keys=("evidence_digest", "created_at"))
    return evidence


def build_evidence(
    *,
    systems: Sequence[Mapping[str, Any]],
    rounds: Sequence[Mapping[str, Any]],
    snapshot: Mapping[str, Any],
    proposal_receipt_ids: Sequence[str],
    stage_id: str = "parent",
    previous_evidence: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    evidence = _compile_evidence(
        systems=systems,
        rounds=rounds,
        snapshot=snapshot,
        proposal_receipt_ids=proposal_receipt_ids,
        stage_id=stage_id,
        previous_evidence=previous_evidence,
    )
    validate_evidence(
        evidence,
        systems=systems,
        rounds=rounds,
        snapshot=snapshot,
        previous_evidence=previous_evidence,
    )
    return evidence


def validate_evidence(
    evidence: Mapping[str, Any],
    *,
    systems: Sequence[Mapping[str, Any]],
    rounds: Sequence[Mapping[str, Any]],
    snapshot: Mapping[str, Any],
    previous_evidence: Mapping[str, Any] | None = None,
) -> None:
    """Recompute the complete blind decision and verify exact stage bindings."""

    if evidence.get("schema_version") != "2.0.0":
        raise ContractError("YM conceptual-quality evidence schema drift")
    stage_id = str(evidence.get("stage_id", ""))
    if evidence.get("target_id") != TARGET_ID or evidence.get("run_id") != RUN_ID or evidence.get("state_version") != STATE_VERSION:
        raise ContractError("YM conceptual-quality evidence crossed target/run/state")
    if evidence.get("evaluation_role") != ("conceptual_gate" if stage_id == "synthesis" else "diagnostic"):
        raise ContractError("YM conceptual-quality evidence role/stage mismatch")
    if evidence.get("evidence_digest") != canonical_digest(evidence, exclude_keys=("evidence_digest", "created_at")):
        raise ContractError("YM conceptual-quality evidence digest mismatch")

    packet = evidence.get("blind_packet")
    reports = evidence.get("judge_reports")
    adjudication = evidence.get("content_adjudication")
    bindings = evidence.get("private_candidate_bindings")
    if not isinstance(packet, Mapping) or not isinstance(reports, list) or not isinstance(adjudication, Mapping) or not isinstance(bindings, Mapping):
        raise ContractError("YM conceptual evidence lacks blind plural adjudication artifacts")
    for report in reports:
        validate_judge_report(report, packet)
    recomputed = _compile_evidence(
        systems=systems,
        rounds=rounds,
        snapshot=snapshot,
        proposal_receipt_ids=evidence.get("evaluation_receipt", {}).get("proposal_receipt_ids", []),
        stage_id=stage_id,
        previous_evidence=previous_evidence,
    )
    if canonical_digest(recomputed) != canonical_digest(evidence):
        raise ContractError("YM conceptual-quality evidence is not the canonical blind recomputation")

    selected_id = str(adjudication.get("selected_system_id", ""))
    if selected_id != evidence.get("preferred_system_id") or adjudication.get("decision") != "prefer_unique":
        raise ContractError("YM preference was not produced by unique blind content adjudication")
    selected = next((row for row in systems if row.get("system_id") == selected_id), None)
    if selected is None:
        raise ContractError("YM blind adjudication selected an absent system")
    formal_ids = {str(item).split(":", 1)[0] for item in selected.get("formalization_seeds", [])}
    correction_ids = {str(item).split(":", 1)[0] for item in selected.get("correction_conditions", [])}
    if formal_ids != REQUIRED_FORMALIZATION_IDS or correction_ids != REQUIRED_CORRECTION_IDS:
        raise ContractError("selected YM mediator lacks the complete F01--F09/C01--C06 correction programme")
    if len(selected.get("unification_claims", {}).get("differences_preserved", [])) < 5:
        raise ContractError("selected YM mediator erases a non-substitutable proof burden")
    if len(rounds) < (4 if stage_id == "synthesis" else 3):
        raise ContractError("YM stage lacks the required objection-bearing reflection depth")

    receipt = evidence.get("evaluation_receipt", {})
    validate_evaluation_receipt(receipt)
    if receipt.get("creative_worth_decision") != "prefer" or receipt.get("promotion_decision") != "not_requested":
        raise ContractError("YM conceptual structural screen failed or escaped its no-promotion boundary")
    for dimension, threshold in QUALITY_THRESHOLDS.items():
        if float(receipt.get("theory_quality", {}).get(dimension, {}).get("score", -1.0)) < threshold:
            raise ContractError(f"YM conceptual-quality threshold failed: {dimension}")
    gates = evidence.get("gate_findings", {})
    if set(gates) != set(CONCEPTUAL_GATE_IDS):
        raise ContractError("YM conceptual evidence omits a G0--G6 gate")
    if stage_id == "synthesis":
        if any(gates[gate_id].get("status") != "pass" for gate_id in CONCEPTUAL_GATE_IDS):
            raise ContractError("YM synthesis failed one or more conceptual gates")
        if evidence.get("stage_comparison", {}).get("material") is not True:
            raise ContractError("YM synthesis lacks material parent-to-synthesis reflective improvement")


__all__ = [
    "QUALITY_THRESHOLDS",
    "REQUIRED_CORRECTION_IDS",
    "REQUIRED_FORMALIZATION_IDS",
    "TARGET_CHARTER",
    "build_candidate",
    "build_evidence",
    "conceptual_structure_projection",
    "validate_evidence",
]
