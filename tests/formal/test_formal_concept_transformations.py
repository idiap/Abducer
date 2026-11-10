# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Focused constructive and adversarial tests for conceptual transformations v2."""

from __future__ import annotations

import copy

import pytest

from agentic.discovery.contracts import canonical_digest, validate_schema_file
from skills.common.formal_concept_transformations import (
    CONSTRUCTOR_IDS,
    FORMAL_CONCEPT_REPLAY_INVALID,
    FORMAL_CONCEPT_WITNESS_INVALID,
    FREE_COMPLETION_PROMOTION_INVALID,
    FormalConceptTransformationError,
    construct_descent_coherence,
    construct_equivalence_coherence,
    construct_functorial_transfer,
    construct_identity_transport,
    construct_mediator_factorization,
    construct_noncommutativity_localization,
    construct_path_independence,
    seal_conceptual_core,
    validate_conceptual_core,
    validate_semantic_delta,
)


CONSEQUENCE = {
    "explanatory_gain": (
        "The exact finite transformation separates a structural interface "
        "from the unchanged target burden."
    ),
    "new_question": (
        "Which additional domain witness would extend this finite relation "
        "without erasing a protected distinction?"
    ),
    "changed_burden": (
        "Prove the relation-specific construction and preserve every declared "
        "observable under its exact maps."
    ),
    "correction": (
        "Quarantine the route if a map collapses a protected distinction or "
        "if a required inhabitant is only freely adjoined."
    ),
    "falsifier": (
        "Exhibit one finite member where the replayed relation law or "
        "protected observable transport fails."
    ),
    "physics_next_action": (
        "Translate the changed burden into one carrier-specific definition, "
        "estimate, or counterexample while retaining all quantifiers."
    ),
}


def _primitive(primitive_id: str, prefix: str) -> dict:
    return {
        "primitive_id": primitive_id,
        "statement": f"Finite conceptual carrier {primitive_id}.",
        "member_ids": [f"{prefix}0", f"{prefix}1"],
    }


def _relation(
    relation_id: str,
    source: str,
    target: str,
    pairs: list[tuple[str, str]],
) -> dict:
    return {
        "relation_id": relation_id,
        "relation_type": "declared_finite_map",
        "statement": f"Declared finite map {relation_id}.",
        "source_primitive_id": source,
        "target_primitive_id": target,
        "action": [
            {"source_member_id": left, "target_member_id": right}
            for left, right in pairs
        ],
    }


def _observable(primitive_id: str, prefix: str) -> dict:
    return {
        "observable_id": f"observable.{primitive_id}",
        "carrier_primitive_id": primitive_id,
        "statement": f"Protected binary distinction on {primitive_id}.",
        "protected": True,
        "evaluations": [
            {"member_id": f"{prefix}0", "value": "red"},
            {"member_id": f"{prefix}1", "value": "blue"},
        ],
    }


def _path(
    path_id: str,
    ambient: str,
    source: str,
    target: str,
) -> dict:
    return {
        "inhabitant_id": path_id,
        "level": 1,
        "ambient_primitive_id": ambient,
        "source_boundary_id": source,
        "target_boundary_id": target,
        "derivation_rule": "declared_domain_constructor",
        "premise_inhabitant_ids": [],
        "evidence_refs": [f"evidence.{path_id}"],
    }


def _source_core() -> dict:
    primitives = [
        _primitive("A", "a"),
        _primitive("B", "b"),
        _primitive("C", "c"),
        _primitive("D", "d"),
        _primitive("U", "u"),
        _primitive("V", "v"),
        _primitive("O", "o"),
    ]
    relations = [
        _relation("map.f_ab", "A", "B", [("a0", "b0"), ("a1", "b1")]),
        _relation("map.g_bc", "B", "C", [("b0", "c0"), ("b1", "c1")]),
        _relation("map.h_ad", "A", "D", [("a0", "d0"), ("a1", "d1")]),
        _relation("map.k_dc", "D", "C", [("d0", "c1"), ("d1", "c0")]),
        _relation("map.direct_ac", "A", "C", [("a0", "c0"), ("a1", "c1")]),
        _relation("map.alt_ac", "A", "C", [("a0", "c0"), ("a1", "c1")]),
        _relation("map.collapse_ac", "A", "C", [("a0", "c0"), ("a1", "c0")]),
        _relation("map.id_a", "A", "A", [("a0", "a0"), ("a1", "a1")]),
        _relation("map.inverse_ba", "B", "A", [("b0", "a0"), ("b1", "a1")]),
        _relation("map.restrict_uo", "U", "O", [("u0", "o0"), ("u1", "o1")]),
        _relation("map.restrict_vo", "V", "O", [("v0", "o0"), ("v1", "o1")]),
    ]
    inhabitants = [
        _path("path.a0", "A", "a0", "a0"),
        _path("path.a0.alt", "A", "a0", "a0"),
        _path("path.a1", "A", "a1", "a1"),
        _path("path.b0", "B", "b0", "b0"),
        _path("path.b1", "B", "b1", "b1"),
        _path("path.c0", "C", "c0", "c0"),
        _path("path.c1", "C", "c1", "c1"),
        _path("path.o0", "O", "o0", "o0"),
        _path("path.o1", "O", "o1", "o1"),
        {
            "inhabitant_id": "cell.a0",
            "level": 2,
            "ambient_primitive_id": "A",
            "source_boundary_id": "path.a0",
            "target_boundary_id": "path.a0.alt",
            "derivation_rule": "declared_coherence_constructor",
            "premise_inhabitant_ids": ["path.a0", "path.a0.alt"],
            "evidence_refs": ["evidence.cell.a0"],
        },
    ]
    return seal_conceptual_core(
        {
            "schema_version": "2.0.0",
            "core_id": "core.formal.concept.v2",
            "target_id": "target.physics.formal.concept",
            "obligation_id": "obligation.physics.formal.concept",
            "physical_carrier": (
                "gauge-invariant observable content in one declared finite "
                "representation"
            ),
            "regime": (
                "finite structural calibration before continuum or theorem "
                "transport"
            ),
            "quantifiers": [
                {
                    "quantifier_id": "quantifier.every.declared.member",
                    "statement": "For every member of each declared finite carrier.",
                },
                {
                    "quantifier_id": "quantifier.every.protected.observable",
                    "statement": "For every explicitly protected observable.",
                },
            ],
            "primitives": primitives,
            "relations": relations,
            "observables": [
                _observable("A", "a"),
                _observable("B", "b"),
                _observable("C", "c"),
                _observable("D", "d"),
                _observable("U", "u"),
                _observable("V", "v"),
                _observable("O", "o"),
            ],
            "inhabitants": inhabitants,
            "burdens": [
                {
                    "burden_id": "burden.original",
                    "statement": (
                        "Relate the representations without changing the "
                        "physical target."
                    ),
                    "status": "open",
                }
            ],
        }
    )


def _hypothesis(kind: str, source: str, target: str) -> dict:
    return {
        "relation_id": f"hypothesis.{kind}",
        "relation_kind": kind,
        "statement": f"Typed task relation requiring {kind}.",
        "source_primitive_id": source,
        "target_primitive_id": target,
        "premise_ids": ["premise.theory", "premise.literature"],
    }


def _leg(
    relation_id: str,
    pairs: list[tuple[str, str]],
) -> dict:
    return {
        "relation_id": relation_id,
        "statement": f"Constructed leg {relation_id}.",
        "action": [
            {"source_member_id": left, "target_member_id": right}
            for left, right in pairs
        ],
    }


def _case(kind: str) -> tuple[dict, dict, object]:
    if kind == "noncommuting_composition":
        return (
            _hypothesis(kind, "A", "C"),
            {
                "witness_kind": "noncommutativity_localization",
                "left_path_relation_ids": ["map.f_ab", "map.g_bc"],
                "right_path_relation_ids": ["map.h_ad", "map.k_dc"],
            },
            construct_noncommutativity_localization,
        )
    if kind == "mediating_factorization":
        return (
            _hypothesis(kind, "A", "C"),
            {
                "witness_kind": "mediator_factorization",
                "direct_relation_id": "map.direct_ac",
                "mediator": {
                    "primitive_id": "M",
                    "statement": "Explicit finite mediator.",
                    "member_ids": ["m0", "m1"],
                },
                "first_leg": _leg(
                    "map.factor_first",
                    [("a0", "m0"), ("a1", "m1")],
                ),
                "second_leg": _leg(
                    "map.factor_second",
                    [("m0", "c0"), ("m1", "c1")],
                ),
            },
            construct_mediator_factorization,
        )
    if kind == "functorial_transfer":
        return (
            _hypothesis(kind, "A", "B"),
            {
                "witness_kind": "functorial_transfer",
                "source_relation_id": "map.f_ab",
                "transferred_source": {
                    "primitive_id": "A2",
                    "statement": "Transferred source representation.",
                    "member_ids": ["a20", "a21"],
                },
                "transferred_target": {
                    "primitive_id": "B2",
                    "statement": "Transferred target representation.",
                    "member_ids": ["b20", "b21"],
                },
                "source_component": _leg(
                    "map.source_component",
                    [("a0", "a20"), ("a1", "a21")],
                ),
                "target_component": _leg(
                    "map.target_component",
                    [("b0", "b20"), ("b1", "b21")],
                ),
                "transferred_relation": _leg(
                    "map.transferred",
                    [("a20", "b20"), ("a21", "b21")],
                ),
            },
            construct_functorial_transfer,
        )
    if kind == "identity_transport":
        return (
            _hypothesis(kind, "A", "A"),
            {
                "witness_kind": "identity_transport",
                "construction_origin": "derived_inhabitant",
                "transport_relation_id": "map.id_a",
                "path_inhabitant_ids": ["path.a0", "path.a1"],
                "adjoined_paths": [],
            },
            construct_identity_transport,
        )
    if kind == "equivalence_coherence":
        return (
            _hypothesis(kind, "A", "B"),
            {
                "witness_kind": "equivalence_coherence",
                "construction_origin": "derived_inhabitant",
                "forward_relation_id": "map.f_ab",
                "inverse_relation_id": "map.inverse_ba",
                "left_path_inhabitant_ids": [
                    "path.a0",
                    "path.a0.alt",
                    "path.a1",
                ],
                "right_path_inhabitant_ids": ["path.b0", "path.b1"],
                "coherence_cell_ids": ["cell.a0"],
                "adjoined_paths": [],
                "adjoined_cells": [],
            },
            construct_equivalence_coherence,
        )
    if kind == "path_independence":
        return (
            _hypothesis(kind, "A", "C"),
            {
                "witness_kind": "path_independence",
                "construction_origin": "derived_inhabitant",
                "left_path_relation_ids": ["map.alt_ac"],
                "right_path_relation_ids": ["map.f_ab", "map.g_bc"],
                "path_inhabitant_ids": ["path.c0", "path.c1"],
                "adjoined_paths": [],
            },
            construct_path_independence,
        )
    if kind == "descent_coherence":
        return (
            _hypothesis(kind, "U", "O"),
            {
                "witness_kind": "descent_coherence",
                "construction_origin": "derived_inhabitant",
                "left_restriction_relation_id": "map.restrict_uo",
                "right_restriction_relation_id": "map.restrict_vo",
                "compatible_pairs": [
                    {
                        "pair_id": "descent.pair.0",
                        "left_member_id": "u0",
                        "right_member_id": "v0",
                        "path_inhabitant_id": "path.o0",
                    },
                    {
                        "pair_id": "descent.pair.1",
                        "left_member_id": "u1",
                        "right_member_id": "v1",
                        "path_inhabitant_id": "path.o1",
                    },
                ],
                "adjoined_paths": [],
            },
            construct_descent_coherence,
        )
    raise AssertionError(kind)


@pytest.mark.parametrize("kind", tuple(CONSTRUCTOR_IDS))
def test_all_seven_relation_specific_constructors_replay(kind: str) -> None:
    relation, witness, constructor = _case(kind)
    packet = constructor(_source_core(), relation, witness, CONSEQUENCE)
    result = validate_semantic_delta(packet)

    assert result["status"] == "valid"
    assert result["constructor_id"] == CONSTRUCTOR_IDS[kind]
    assert packet["semantic_delta"]["added_primitive_ids"]
    assert packet["semantic_delta"]["added_relation_ids"]
    assert packet["semantic_delta"]["splits"]
    assert packet["semantic_delta"]["explanatory_gain"] == CONSEQUENCE["explanatory_gain"]
    assert packet["semantic_delta"]["correction"] == CONSEQUENCE["correction"]
    assert packet["semantic_delta"]["falsifier"] == CONSEQUENCE["falsifier"]
    assert packet["observable_preservation"]["status"] == "preserved"
    assert packet["physics_handback"]["physical_carrier"] == _source_core()["physical_carrier"]
    assert packet["physics_handback"]["quantifiers"] == _source_core()["quantifiers"]
    assert packet["physics_handback"]["experiment_role"] == (
        "secondary_theory_requested_falsifier_only"
    )
    assert not packet["physics_handback"]["physics_value_authorized"]
    assert not packet["physics_handback"]["theorem_authorized"]
    assert not packet["authority_boundary"]["experiment_selection_authorized"]

    expected_status = (
        "localized"
        if kind == "noncommuting_composition"
        else "constructively_removed"
    )
    assert packet["obstruction_transition"]["after_status"] == expected_status
    assert packet["obstruction_transition"]["decision_flip_authorized"] is (
        kind != "noncommuting_composition"
    )


def test_relation_kinds_have_distinct_constructors_and_structural_deltas() -> None:
    packets = {}
    for kind in CONSTRUCTOR_IDS:
        relation, witness, constructor = _case(kind)
        packets[kind] = constructor(_source_core(), relation, witness, CONSEQUENCE)

    assert {
        packet["construction"]["constructor_id"] for packet in packets.values()
    } == set(CONSTRUCTOR_IDS.values())
    assert len(
        {
            canonical_digest(
                {
                    "primitives": packet["semantic_delta"]["added_primitive_ids"],
                    "relations": packet["semantic_delta"]["added_relation_ids"],
                    "inhabitants": packet["semantic_delta"]["added_inhabitant_ids"],
                    "splits": packet["semantic_delta"]["splits"],
                }
            )
            for packet in packets.values()
        }
    ) == 7


def test_protected_observable_erasure_is_retained_and_quarantined() -> None:
    relation = _hypothesis("noncommuting_composition", "A", "C")
    witness = {
        "witness_kind": "noncommutativity_localization",
        "left_path_relation_ids": ["map.collapse_ac"],
        "right_path_relation_ids": ["map.direct_ac"],
    }
    packet = construct_noncommutativity_localization(
        _source_core(), relation, witness, CONSEQUENCE
    )

    assert packet["observable_preservation"]["protected_erasure_detected"]
    assert packet["observable_preservation"]["status"] == (
        "quarantined_protected_erasure"
    )
    assert packet["obstruction_transition"] == {
        "before_status": "open",
        "after_status": "quarantined_protected_erasure",
        "removal_authorized": False,
        "decision_flip_authorized": False,
        "reason_code": "protected_observable_erasure",
        "evidence_digest": packet["obstruction_transition"]["evidence_digest"],
    }
    assert any(
        row["reason_code"] == "protected_value_collision"
        for receipt in packet["observable_preservation"]["receipts"]
        for row in receipt["counterexamples"]
    )
    assert any(
        row["protected"] and row["disposition"] == "quarantined"
        for row in packet["semantic_delta"]["loss_ledger"]
    )
    assert validate_semantic_delta(packet)["protected_erasure_detected"]


def test_free_identity_completion_is_counterfactual_and_cannot_flip() -> None:
    relation = _hypothesis("identity_transport", "A", "A")
    witness = {
        "witness_kind": "identity_transport",
        "construction_origin": "free_completion_counterfactual",
        "transport_relation_id": "map.id_a",
        "path_inhabitant_ids": [],
        "adjoined_paths": [
            {
                "inhabitant_id": "free.path.a0",
                "ambient_primitive_id": "A",
                "source_boundary_id": "a0",
                "target_boundary_id": "a0",
            },
            {
                "inhabitant_id": "free.path.a1",
                "ambient_primitive_id": "A",
                "source_boundary_id": "a1",
                "target_boundary_id": "a1",
            },
        ],
    }
    packet = construct_identity_transport(
        _source_core(), relation, witness, CONSEQUENCE
    )

    assert packet["construction"]["construction_origin"] == (
        "free_completion_counterfactual"
    )
    assert packet["obstruction_transition"]["after_status"] == (
        "counterfactual_only"
    )
    assert not packet["obstruction_transition"]["removal_authorized"]
    assert not packet["obstruction_transition"]["decision_flip_authorized"]
    assert {"free.path.a0", "free.path.a1"} <= set(
        packet["semantic_delta"]["added_inhabitant_ids"]
    )
    assert validate_semantic_delta(packet)["after_status"] == "counterfactual_only"

    promoted = copy.deepcopy(packet)
    promoted["obstruction_transition"].update(
        {
            "after_status": "constructively_removed",
            "removal_authorized": True,
            "decision_flip_authorized": True,
            "reason_code": "exact_relation_specific_construction",
        }
    )
    promoted["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in promoted.items()
            if key != "content_digest"
        }
    )
    with pytest.raises(FormalConceptTransformationError) as exc:
        validate_semantic_delta(promoted)
    assert exc.value.reason_code == FORMAL_CONCEPT_REPLAY_INVALID


def test_frozen_source_rejects_free_inhabitants() -> None:
    core = copy.deepcopy(_source_core())
    core["inhabitants"].append(
        {
            "inhabitant_id": "forged.free.path",
            "level": 1,
            "ambient_primitive_id": "A",
            "source_boundary_id": "a0",
            "target_boundary_id": "a1",
            "derivation_rule": "free_adjoinment",
            "premise_inhabitant_ids": [],
            "evidence_refs": [],
        }
    )
    core["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in core.items()
            if key != "content_digest"
        }
    )
    with pytest.raises(FormalConceptTransformationError) as exc:
        validate_conceptual_core(core)
    assert exc.value.reason_code == FREE_COMPLETION_PROMOTION_INVALID


def test_rehashed_narrative_or_structural_tampering_fails_reconstruction() -> None:
    relation, witness, constructor = _case("mediating_factorization")
    packet = constructor(_source_core(), relation, witness, CONSEQUENCE)
    tampered = copy.deepcopy(packet)
    tampered["semantic_delta"]["changed_burden"] = (
        "A rehashed but non-derived burden."
    )
    tampered["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in tampered.items()
            if key != "content_digest"
        }
    )
    with pytest.raises(FormalConceptTransformationError) as exc:
        validate_semantic_delta(tampered)
    assert exc.value.reason_code == FORMAL_CONCEPT_REPLAY_INVALID


@pytest.mark.parametrize(
    ("kind", "mutation"),
    (
        ("noncommuting_composition", "erase_disagreement"),
        ("mediating_factorization", "break_factorization"),
        ("functorial_transfer", "break_naturality"),
    ),
)
def test_relation_specific_laws_reject_wrong_constructions(
    kind: str, mutation: str
) -> None:
    relation, witness, constructor = _case(kind)
    witness = copy.deepcopy(witness)
    if mutation == "erase_disagreement":
        witness["right_path_relation_ids"] = ["map.direct_ac"]
        witness["left_path_relation_ids"] = ["map.alt_ac"]
    elif mutation == "break_factorization":
        witness["second_leg"]["action"][0]["target_member_id"] = "c1"
    else:
        witness["transferred_relation"]["action"][0][
            "target_member_id"
        ] = "b21"
    with pytest.raises(FormalConceptTransformationError) as exc:
        constructor(_source_core(), relation, witness, CONSEQUENCE)
    assert exc.value.reason_code == FORMAL_CONCEPT_WITNESS_INVALID


def test_v2_schema_is_meta_valid() -> None:
    schema = validate_schema_file("formal_conceptual_delta_v2.schema.json")
    assert schema["$id"].endswith("formal_conceptual_delta_v2.schema.json")
