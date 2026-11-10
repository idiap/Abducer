# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Focused tests for exact finite conceptual-transformation sequences."""

from __future__ import annotations

import copy

import pytest

from agentic.discovery.contracts import canonical_digest, validate_schema_file
from skills.common.formal_concept_sequence_algebra import (
    FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID,
    FormalConceptSequenceError,
    _outcome_and_handback,
    build_conditioned_formal_transformation_sequence,
    build_formal_transformation_sequence,
    compare_conceptual_cores,
    validate_conditioned_formal_transformation_sequence,
    validate_formal_transformation_sequence,
)
from skills.common.formal_concept_transformations import (
    construct_categorical_transformation,
    construct_hott_transformation,
    seal_conceptual_core,
)


CONSEQUENCE = {
    "explanatory_gain": (
        "The finite transformation separates a structural interface from the "
        "unchanged target burden."
    ),
    "new_question": (
        "Which domain witness extends this relation without erasing a "
        "protected distinction?"
    ),
    "changed_burden": (
        "Prove the relation-specific construction while preserving every "
        "declared observable."
    ),
    "correction": (
        "Quarantine any route that collapses a protected distinction or "
        "freely adjoins a required inhabitant."
    ),
    "falsifier": (
        "Exhibit a finite member where the relation law or observable "
        "transport fails."
    ),
    "physics_next_action": (
        "Translate the burden into one carrier-specific counterexample while "
        "retaining all quantifiers."
    ),
}


def _primitive(identifier: str, prefix: str) -> dict:
    return {
        "primitive_id": identifier,
        "statement": f"Finite conceptual carrier {identifier}.",
        "member_ids": [f"{prefix}0", f"{prefix}1"],
    }


def _relation(
    identifier: str,
    source: str,
    target: str,
    pairs: list[tuple[str, str]],
) -> dict:
    return {
        "relation_id": identifier,
        "relation_type": "declared_finite_map",
        "statement": f"Declared finite map {identifier}.",
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
    identifier: str,
    ambient: str,
    source: str,
    target: str,
) -> dict:
    return {
        "inhabitant_id": identifier,
        "level": 1,
        "ambient_primitive_id": ambient,
        "source_boundary_id": source,
        "target_boundary_id": target,
        "derivation_rule": "declared_domain_constructor",
        "premise_inhabitant_ids": [],
        "evidence_refs": [f"evidence.{identifier}"],
    }


def _source_core() -> dict:
    primitive_specs = (
        ("A", "a"),
        ("B", "b"),
        ("C", "c"),
        ("D", "d"),
        ("U", "u"),
        ("V", "v"),
        ("O", "o"),
    )
    return seal_conceptual_core(
        {
            "schema_version": "2.0.0",
            "core_id": "core.sequence.source",
            "target_id": "target.physics.sequence",
            "obligation_id": "obligation.physics.sequence",
            "physical_carrier": (
                "gauge-invariant observable content in one finite "
                "representation"
            ),
            "regime": (
                "finite structural calibration before continuum or theorem "
                "transport"
            ),
            "quantifiers": [
                {
                    "quantifier_id": "quantifier.every.member",
                    "statement": "For every member of each finite carrier.",
                },
                {
                    "quantifier_id": "quantifier.every.observable",
                    "statement": "For every protected observable.",
                },
            ],
            "primitives": [
                _primitive(identifier, prefix)
                for identifier, prefix in primitive_specs
            ],
            "relations": [
                _relation(
                    "map.f_ab",
                    "A",
                    "B",
                    [("a0", "b0"), ("a1", "b1")],
                ),
                _relation(
                    "map.g_bc",
                    "B",
                    "C",
                    [("b0", "c0"), ("b1", "c1")],
                ),
                _relation(
                    "map.h_ad",
                    "A",
                    "D",
                    [("a0", "d0"), ("a1", "d1")],
                ),
                _relation(
                    "map.k_dc",
                    "D",
                    "C",
                    [("d0", "c1"), ("d1", "c0")],
                ),
                _relation(
                    "map.direct_ac",
                    "A",
                    "C",
                    [("a0", "c0"), ("a1", "c1")],
                ),
                _relation(
                    "map.alt_ac",
                    "A",
                    "C",
                    [("a0", "c0"), ("a1", "c1")],
                ),
                _relation(
                    "map.collapse_ac",
                    "A",
                    "C",
                    [("a0", "c0"), ("a1", "c0")],
                ),
                _relation(
                    "map.id_a",
                    "A",
                    "A",
                    [("a0", "a0"), ("a1", "a1")],
                ),
                _relation(
                    "map.inverse_ba",
                    "B",
                    "A",
                    [("b0", "a0"), ("b1", "a1")],
                ),
                _relation(
                    "map.restrict_uo",
                    "U",
                    "O",
                    [("u0", "o0"), ("u1", "o1")],
                ),
                _relation(
                    "map.restrict_vo",
                    "V",
                    "O",
                    [("v0", "o0"), ("v1", "o1")],
                ),
            ],
            "observables": [
                _observable(identifier, prefix)
                for identifier, prefix in primitive_specs
            ],
            "inhabitants": [
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
            ],
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


def _leg(identifier: str, pairs: list[tuple[str, str]]) -> dict:
    return {
        "relation_id": identifier,
        "statement": f"Constructed leg {identifier}.",
        "action": [
            {"source_member_id": left, "target_member_id": right}
            for left, right in pairs
        ],
    }


def _plan(kind: str, identifier: str) -> dict:
    if kind == "mediating_factorization":
        relation = _hypothesis(kind, "A", "C")
        witness = {
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
        }
    elif kind == "functorial_transfer":
        relation = _hypothesis(kind, "A", "B")
        witness = {
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
        }
    elif kind == "identity_transport":
        relation = _hypothesis(kind, "A", "A")
        witness = {
            "witness_kind": "identity_transport",
            "construction_origin": "derived_inhabitant",
            "transport_relation_id": "map.id_a",
            "path_inhabitant_ids": ["path.a0", "path.a1"],
            "adjoined_paths": [],
        }
    elif kind == "descent_coherence":
        relation = _hypothesis(kind, "U", "O")
        witness = {
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
        }
    else:
        raise AssertionError(kind)
    return {
        "transformation_id": identifier,
        "relation_hypothesis": relation,
        "witness": witness,
        "consequence_contract": copy.deepcopy(CONSEQUENCE),
    }


def _protected_erasure_plan() -> dict:
    return {
        "transformation_id": "sequence.protected.erasure",
        "relation_hypothesis": _hypothesis(
            "noncommuting_composition", "A", "C"
        ),
        "witness": {
            "witness_kind": "noncommutativity_localization",
            "left_path_relation_ids": ["map.collapse_ac"],
            "right_path_relation_ids": ["map.direct_ac"],
        },
        "consequence_contract": copy.deepcopy(CONSEQUENCE),
    }


def _free_completion_plan() -> dict:
    return {
        "transformation_id": "sequence.free.completion",
        "relation_hypothesis": _hypothesis(
            "identity_transport", "A", "A"
        ),
        "witness": {
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
        },
        "consequence_contract": copy.deepcopy(CONSEQUENCE),
    }


def _asymmetric_protected_packet() -> dict:
    """Build a coenabled pair for which only mediator-first erases a value."""

    core = copy.deepcopy(_source_core())
    core["core_id"] = "core.sequence.asymmetric"
    core["primitives"].extend(
        [
            {
                "primitive_id": "X",
                "statement": "Three-member source carrier.",
                "member_ids": ["x0", "x1", "x2"],
            },
            {
                "primitive_id": "S",
                "statement": "Four-member order-sensitive carrier.",
                "member_ids": ["s0", "s1", "s2", "s3"],
            },
            {
                "primitive_id": "T",
                "statement": "Three-member comparison carrier.",
                "member_ids": ["t0", "t1", "t2"],
            },
        ]
    )
    core["relations"].extend(
        [
            _relation(
                "map.direct_xs",
                "X",
                "S",
                [("x0", "s0"), ("x1", "s2"), ("x2", "s3")],
            ),
            _relation(
                "map.left_st",
                "S",
                "T",
                [
                    ("s0", "t0"),
                    ("s1", "t0"),
                    ("s2", "t1"),
                    ("s3", "t2"),
                ],
            ),
            _relation(
                "map.right_st",
                "S",
                "T",
                [
                    ("s0", "t0"),
                    ("s1", "t1"),
                    ("s2", "t2"),
                    ("s3", "t2"),
                ],
            ),
        ]
    )
    core["observables"].extend(
        [
            {
                "observable_id": "observable.X",
                "carrier_primitive_id": "X",
                "statement": "Protected colors on X.",
                "protected": True,
                "evaluations": [
                    {"member_id": "x0", "value": "red"},
                    {"member_id": "x1", "value": "blue"},
                    {"member_id": "x2", "value": "blue"},
                ],
            },
            {
                "observable_id": "observable.S",
                "carrier_primitive_id": "S",
                "statement": "Protected colors on S.",
                "protected": True,
                "evaluations": [
                    {"member_id": "s0", "value": "red"},
                    {"member_id": "s1", "value": "red"},
                    {"member_id": "s2", "value": "blue"},
                    {"member_id": "s3", "value": "blue"},
                ],
            },
            {
                "observable_id": "observable.T",
                "carrier_primitive_id": "T",
                "statement": "Protected colors on T.",
                "protected": True,
                "evaluations": [
                    {"member_id": "t0", "value": "red"},
                    {"member_id": "t1", "value": "red"},
                    {"member_id": "t2", "value": "blue"},
                ],
            },
        ]
    )
    core.pop("content_digest")
    core = seal_conceptual_core(core)

    mediator = {
        "transformation_id": "sequence.asymmetric.mediator",
        "relation_hypothesis": _hypothesis(
            "mediating_factorization", "X", "S"
        ),
        "witness": {
            "witness_kind": "mediator_factorization",
            "direct_relation_id": "map.direct_xs",
            "mediator": {
                "primitive_id": "M.asymmetric",
                "statement": "Explicit asymmetric mediator.",
                "member_ids": ["ma0", "ma1", "ma2"],
            },
            "first_leg": _leg(
                "map.asymmetric_xm",
                [("x0", "ma0"), ("x1", "ma1"), ("x2", "ma2")],
            ),
            "second_leg": _leg(
                "map.asymmetric_ms",
                [("ma0", "s0"), ("ma1", "s2"), ("ma2", "s3")],
            ),
        },
        "consequence_contract": copy.deepcopy(CONSEQUENCE),
    }
    noncommuting = {
        "transformation_id": "sequence.asymmetric.noncommuting",
        "relation_hypothesis": _hypothesis(
            "noncommuting_composition", "S", "T"
        ),
        "witness": {
            "witness_kind": "noncommutativity_localization",
            "left_path_relation_ids": ["map.left_st"],
            "right_path_relation_ids": ["map.right_st"],
        },
        "consequence_contract": copy.deepcopy(CONSEQUENCE),
    }
    return build_formal_transformation_sequence(
        core,
        mediator,
        noncommuting,
    )


def _relabel_core(raw: dict) -> dict:
    core = copy.deepcopy(raw)
    primitive_ids = {
        row["primitive_id"]: f"relabel.primitive.{index}"
        for index, row in enumerate(core["primitives"])
    }
    member_ids = {
        member_id: f"relabel.member.{index}"
        for index, member_id in enumerate(
            member
            for row in core["primitives"]
            for member in row["member_ids"]
        )
    }
    relation_ids = {
        row["relation_id"]: f"relabel.relation.{index}"
        for index, row in enumerate(core["relations"])
    }
    observable_ids = {
        row["observable_id"]: f"relabel.observable.{index}"
        for index, row in enumerate(core["observables"])
    }
    inhabitant_ids = {
        row["inhabitant_id"]: f"relabel.inhabitant.{index}"
        for index, row in enumerate(core["inhabitants"])
    }
    evidence_ids = {
        evidence: f"relabel.evidence.{index}"
        for index, evidence in enumerate(
            dict.fromkeys(
                evidence
                for row in core["inhabitants"]
                for evidence in row["evidence_refs"]
            )
        )
    }
    burden_ids = {
        row["burden_id"]: f"relabel.burden.{index}"
        for index, row in enumerate(core["burdens"])
    }
    core["core_id"] = "core.sequence.relabelled"
    for row in core["primitives"]:
        row["primitive_id"] = primitive_ids[row["primitive_id"]]
        row["member_ids"] = [
            member_ids[member_id] for member_id in row["member_ids"]
        ]
    for row in core["relations"]:
        row["relation_id"] = relation_ids[row["relation_id"]]
        row["source_primitive_id"] = primitive_ids[
            row["source_primitive_id"]
        ]
        row["target_primitive_id"] = primitive_ids[
            row["target_primitive_id"]
        ]
        for action in row["action"]:
            action["source_member_id"] = member_ids[
                action["source_member_id"]
            ]
            action["target_member_id"] = member_ids[
                action["target_member_id"]
            ]
    for row in core["observables"]:
        row["observable_id"] = observable_ids[row["observable_id"]]
        row["carrier_primitive_id"] = primitive_ids[
            row["carrier_primitive_id"]
        ]
        for evaluation in row["evaluations"]:
            evaluation["member_id"] = member_ids[
                evaluation["member_id"]
            ]
    for row in core["inhabitants"]:
        row["inhabitant_id"] = inhabitant_ids[row["inhabitant_id"]]
        row["ambient_primitive_id"] = primitive_ids[
            row["ambient_primitive_id"]
        ]
        boundary_ids = member_ids if row["level"] == 1 else inhabitant_ids
        row["source_boundary_id"] = boundary_ids[
            row["source_boundary_id"]
        ]
        row["target_boundary_id"] = boundary_ids[
            row["target_boundary_id"]
        ]
        row["premise_inhabitant_ids"] = [
            inhabitant_ids[identifier]
            for identifier in row["premise_inhabitant_ids"]
        ]
        row["evidence_refs"] = [
            evidence_ids[identifier] for identifier in row["evidence_refs"]
        ]
    for row in core["burdens"]:
        row["burden_id"] = burden_ids[row["burden_id"]]
    core.pop("content_digest")
    return seal_conceptual_core(core)


def test_sequence_schema_is_meta_valid() -> None:
    for name in (
        "formal_concept_sequence_algebra_v1.schema.json",
        "formal_conditioned_concept_sequence_v1.schema.json",
    ):
        schema = validate_schema_file(name)
        assert schema["$id"].endswith(name)


def _apply_exact(core: dict, plan: dict) -> dict:
    constructor = (
        construct_categorical_transformation
        if plan["relation_hypothesis"]["relation_kind"]
        in {
            "mediating_factorization",
            "functorial_transfer",
            "noncommuting_composition",
        }
        else construct_hott_transformation
    )
    return constructor(
        core,
        plan["relation_hypothesis"],
        plan["witness"],
        plan["consequence_contract"],
    )


def test_conditioned_sequence_never_fabricates_an_unauthored_reverse_order() -> None:
    core = _source_core()
    category = _plan("mediating_factorization", "conditioned.category")
    category_delta = _apply_exact(core, category)
    hott = _plan("identity_transport", "conditioned.hott")
    hott_delta = _apply_exact(category_delta["after_core"], hott)

    forward = build_conditioned_formal_transformation_sequence(
        core,
        category,
        category_delta,
        hott,
        hott_delta,
    )
    assert forward["sequence_kind"] == "intermediate_conditioned_one_order"
    assert forward["second_step"]["plan_authored_from_core_digest"] == (
        category_delta["after_core"]["content_digest"]
    )
    assert forward["conditioned_path"]["reverse_order_status"] == (
        "not_constructed_without_reverse_conditioned_authorship"
    )
    assert "critical_pairs" not in forward
    assert "conceptual_core_comparison" not in forward
    assert forward["conditioned_path"]["status"] == "completed"
    assert validate_conditioned_formal_transformation_sequence(forward)[
        "status"
    ] == "valid"

    # The reverse candidate is legitimate only after its own second plan is
    # applied to the independently produced reverse intermediate.
    reverse_hott = _plan("identity_transport", "conditioned.reverse.hott")
    reverse_hott_delta = _apply_exact(core, reverse_hott)
    reverse_category = _plan(
        "mediating_factorization", "conditioned.reverse.category"
    )
    reverse_category_delta = _apply_exact(
        reverse_hott_delta["after_core"], reverse_category
    )
    reverse = build_conditioned_formal_transformation_sequence(
        core,
        reverse_hott,
        reverse_hott_delta,
        reverse_category,
        reverse_category_delta,
    )
    assert reverse["order"] == [
        "conditioned.reverse.hott",
        "conditioned.reverse.category",
    ]
    assert reverse["second_step"]["plan_authored_from_core_digest"] == (
        reverse_hott_delta["after_core"]["content_digest"]
    )
    assert reverse["content_digest"] != forward["content_digest"]
    assert reverse["conditioned_path"]["status"] == "completed"


def test_conditioned_sequence_rejects_a_second_delta_from_the_wrong_base() -> None:
    core = _source_core()
    category = _plan("mediating_factorization", "conditioned.wrong.category")
    category_delta = _apply_exact(core, category)
    hott = _plan("identity_transport", "conditioned.wrong.hott")
    wrong_base_delta = _apply_exact(core, hott)
    with pytest.raises(
        FormalConceptSequenceError,
        match=FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID,
    ):
        build_conditioned_formal_transformation_sequence(
            core,
            category,
            category_delta,
            hott,
            wrong_base_delta,
        )


def test_both_orders_replay_exact_intermediates_and_commute_up_to_ids() -> None:
    packet = build_formal_transformation_sequence(
        _source_core(),
        _plan("mediating_factorization", "sequence.factor"),
        _plan("descent_coherence", "sequence.descent"),
    )

    assert packet["coenabledness"]["status"] == "coenabled"
    assert packet["outcome"]["status"] == "isomorphic_commuting"
    assert packet["conceptual_core_comparison"]["comparison_status"] == (
        "isomorphic"
    )
    assert len(packet["critical_pairs"]) == 2
    for pair in packet["critical_pairs"]:
        assert pair["status"] == "completed"
        assert pair["intermediate_replay"]["exact_input_boundary"]
        assert pair["intermediate_replay"]["semantic_delta_replayed"]
        assert pair["residual"]["input_core_digest"] == (
            pair["first_delta"]["after_core"]["content_digest"]
        )
        assert pair["residual"]["replay"]["exact_input_boundary"]
        assert pair["final_core"] == pair["residual"]["delta"]["after_core"]
    assert len(packet["finite_handback"]["candidates"]) == 1
    assert packet["authority_boundary"]["truth_authority"] is None
    assert packet["authority_boundary"]["conceptual_merit_authority"] is None
    assert packet["authority_boundary"]["physics_authority"] is None
    assert packet["authority_boundary"]["theorem_authority"] is None
    result = validate_formal_transformation_sequence(packet)
    assert result["status"] == "valid"
    assert result["outcome_status"] == "isomorphic_commuting"


def test_productive_noncommutation_retains_both_witness_candidates() -> None:
    packet = build_formal_transformation_sequence(
        _source_core(),
        _plan("functorial_transfer", "sequence.functor"),
        _plan("identity_transport", "sequence.identity"),
    )

    assert packet["outcome"]["status"] == "productive_noncommutation"
    assert packet["conceptual_core_comparison"]["comparison_status"] == (
        "not_isomorphic"
    )
    candidates = packet["finite_handback"]["candidates"]
    assert len(candidates) == 2
    assert {row["critical_pair_ids"][0] for row in candidates} == {
        row["critical_pair_id"] for row in packet["critical_pairs"]
    }
    assert {
        text for row in candidates for text in row["burden_statements"]
    } == {CONSEQUENCE["changed_burden"]}
    assert {
        text for row in candidates for text in row["corrections"]
    } == {CONSEQUENCE["correction"]}
    assert {
        text for row in candidates for text in row["falsifiers"]
    } == {CONSEQUENCE["falsifier"]}
    assert packet["finite_handback"]["truth_authority"] is None
    assert packet["finite_handback"][
        "eligible_for_precommitted_rule_replay"
    ]
    assert not packet["outcome"]["decision_change_authorized"]


def test_exact_isomorphism_accepts_only_internal_identifier_relabelling() -> None:
    source = _source_core()
    relabelled = _relabel_core(source)
    comparison = compare_conceptual_cores(
        source, relabelled, max_permutations=65536
    )

    assert comparison["comparison_status"] == "isomorphic"
    assert comparison["semantic_root_equal"]
    assert not comparison["strict_projection_equal"]
    assert comparison["identifier_mapping"]

    changed_target = copy.deepcopy(relabelled)
    changed_target["target_id"] = "target.physics.changed"
    changed_target.pop("content_digest")
    changed_target = seal_conceptual_core(changed_target)
    mismatch = compare_conceptual_cores(source, changed_target)
    assert mismatch["comparison_status"] == "not_isomorphic"
    assert mismatch["reason_code"] == "semantic_root_mismatch"

    changed_statement = copy.deepcopy(relabelled)
    changed_statement["burdens"][0]["statement"] = "Rehashed burden."
    changed_statement.pop("content_digest")
    changed_statement = seal_conceptual_core(changed_statement)
    mismatch = compare_conceptual_cores(
        source, changed_statement, max_permutations=65536
    )
    assert mismatch["comparison_status"] == "not_isomorphic"

    changed_value = copy.deepcopy(relabelled)
    changed_value["observables"][0]["evaluations"][0]["value"] = "green"
    changed_value.pop("content_digest")
    changed_value = seal_conceptual_core(changed_value)
    mismatch = compare_conceptual_cores(
        source, changed_value, max_permutations=65536
    )
    assert mismatch["comparison_status"] == "not_isomorphic"


def test_bounded_exact_comparison_reports_typed_ceiling_unavailable() -> None:
    source = copy.deepcopy(_source_core())
    source["burdens"].append(
        {
            "burden_id": "burden.symmetric",
            "statement": source["burdens"][0]["statement"],
            "status": source["burdens"][0]["status"],
        }
    )
    source.pop("content_digest")
    source = seal_conceptual_core(source)

    comparison = compare_conceptual_cores(
        source, _relabel_core(source), max_permutations=1
    )
    assert comparison["comparison_status"] == "ceiling_unavailable"
    assert comparison["reason_code"] == (
        "bounded_exact_isomorphism_ceiling_exceeded"
    )
    assert comparison["canonical_core_digest"] is None
    assert comparison["left_candidate_permutations"] > 1


def test_sequence_retains_both_candidates_when_exact_comparison_hits_ceiling() -> None:
    packet = build_formal_transformation_sequence(
        _source_core(),
        _plan("mediating_factorization", "sequence.factor"),
        _plan("descent_coherence", "sequence.descent"),
        max_isomorphism_permutations=1,
    )

    assert packet["outcome"]["status"] == "ceiling_unavailable"
    assert packet["conceptual_core_comparison"]["comparison_status"] == (
        "ceiling_unavailable"
    )
    assert len(packet["finite_handback"]["candidates"]) == 2
    assert not packet["finite_handback"][
        "eligible_for_precommitted_rule_replay"
    ]
    result = validate_formal_transformation_sequence(packet)
    assert result["status"] == "valid"
    assert result["retained_candidate_count"] == 2


def test_partial_domain_records_noncoenabledness_and_residual_failure() -> None:
    unavailable = _plan("identity_transport", "sequence.unavailable")
    unavailable["witness"]["path_inhabitant_ids"] = [
        "path.missing.0",
        "path.missing.1",
    ]
    packet = build_formal_transformation_sequence(
        _source_core(),
        _plan("mediating_factorization", "sequence.available"),
        unavailable,
    )

    assert packet["coenabledness"]["status"] == "not_coenabled"
    assert not packet["coenabledness"]["both_defined_on_base"]
    assert {row["status"] for row in packet["critical_pairs"]} == {
        "partial_failure",
        "not_coenabled",
    }
    assert packet["conceptual_core_comparison"]["comparison_status"] == (
        "not_available"
    )
    assert packet["outcome"]["status"] == "not_coenabled"
    assert packet["finite_handback"]["candidates"] == []


def test_asymmetric_protected_erasure_retains_only_the_safe_order() -> None:
    packet = _asymmetric_protected_packet()
    safe = next(
        row for row in packet["critical_pairs"] if row["status"] == "completed"
    )
    unsafe = next(
        row
        for row in packet["critical_pairs"]
        if row["status"] == "quarantined_protected_erasure"
    )

    assert packet["coenabledness"]["status"] == "coenabled"
    assert packet["outcome"]["status"] == "partial_failure"
    assert packet["outcome"]["retained_critical_pair_ids"] == [
        safe["critical_pair_id"]
    ]
    assert packet["outcome"]["quarantined_critical_pair_ids"] == [
        unsafe["critical_pair_id"]
    ]
    handback = packet["finite_handback"]
    assert handback["handback_status"] == "partial_sequence_quarantined"
    assert len(handback["candidates"]) == 1
    assert handback["candidates"][0]["critical_pair_ids"] == [
        safe["critical_pair_id"]
    ]
    assert handback["candidates"][0]["burden_statements"] == [
        CONSEQUENCE["changed_burden"]
    ]
    assert handback["candidates"][0]["corrections"] == [
        CONSEQUENCE["correction"]
    ]
    assert handback["candidates"][0]["falsifiers"] == [
        CONSEQUENCE["falsifier"]
    ]
    assert not handback["eligible_for_precommitted_rule_replay"]
    assert handback["truth_authority"] is None
    assert handback["conceptual_merit_authority"] is None
    assert handback["physics_authority"] is None
    assert handback["theorem_authority"] is None
    assert not packet["outcome"]["decision_change_authorized"]
    assert validate_formal_transformation_sequence(packet)[
        "outcome_status"
    ] == "partial_failure"


def test_asymmetric_free_completion_retains_the_completed_order() -> None:
    """Exercise the generic classifier for a future context-sensitive free route."""

    packet = _asymmetric_protected_packet()
    pairs = copy.deepcopy(packet["critical_pairs"])
    unsafe = next(row for row in pairs if row["status"] != "completed")
    unsafe["status"] = "quarantined_free_completion"
    unsafe["reason_code"] = "free_completion_has_no_inhabitation_authority"
    unsafe["free_completion_detected"] = True
    outcome, handback = _outcome_and_handback(
        packet["base_core"],
        packet["coenabledness"],
        pairs,
        packet["conceptual_core_comparison"],
    )
    safe = next(row for row in pairs if row["status"] == "completed")

    assert outcome["status"] == "partial_failure"
    assert outcome["retained_critical_pair_ids"] == [
        safe["critical_pair_id"]
    ]
    assert outcome["quarantined_critical_pair_ids"] == [
        unsafe["critical_pair_id"]
    ]
    assert handback["handback_status"] == "partial_sequence_quarantined"
    assert len(handback["candidates"]) == 1
    assert handback["candidates"][0]["critical_pair_ids"] == [
        safe["critical_pair_id"]
    ]
    assert handback["truth_authority"] is None
    assert handback["physics_authority"] is None
    assert handback["theorem_authority"] is None


@pytest.mark.parametrize(
    ("unsafe_plan", "expected_status"),
    (
        (_protected_erasure_plan, "quarantined_protected_erasure"),
        (_free_completion_plan, "quarantined_free_completion"),
    ),
)
def test_unsafe_sequence_paths_are_quarantined_without_handback(
    unsafe_plan,
    expected_status: str,
) -> None:
    packet = build_formal_transformation_sequence(
        _source_core(),
        unsafe_plan(),
        _plan("descent_coherence", "sequence.safe"),
    )

    assert packet["outcome"]["status"] == expected_status
    assert any(
        row["status"] == expected_status for row in packet["critical_pairs"]
    )
    assert packet["finite_handback"]["handback_status"] == "quarantined"
    assert packet["finite_handback"]["candidates"] == []
    assert not packet["outcome"]["decision_change_authorized"]
    assert not packet["authority_boundary"]["proof_authorized"]


def test_asymmetric_retained_order_tampering_fails_replay() -> None:
    packet = _asymmetric_protected_packet()
    unsafe = next(
        row for row in packet["critical_pairs"] if row["status"] != "completed"
    )
    tampered = copy.deepcopy(packet)
    tampered["outcome"]["retained_critical_pair_ids"] = [
        unsafe["critical_pair_id"]
    ]
    tampered["outcome"]["outcome_digest"] = canonical_digest(
        {
            key: value
            for key, value in tampered["outcome"].items()
            if key != "outcome_digest"
        }
    )
    tampered["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in tampered.items()
            if key != "content_digest"
        }
    )

    with pytest.raises(FormalConceptSequenceError) as exc:
        validate_formal_transformation_sequence(tampered)
    assert exc.value.reason_code == FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID


def test_rehashed_handback_mutation_fails_deterministic_replay() -> None:
    packet = build_formal_transformation_sequence(
        _source_core(),
        _plan("functorial_transfer", "sequence.functor"),
        _plan("identity_transport", "sequence.identity"),
    )
    tampered = copy.deepcopy(packet)
    tampered["finite_handback"]["candidates"][0]["corrections"][0] = (
        "A rehashed correction not derived from either witness."
    )
    tampered["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in tampered.items()
            if key != "content_digest"
        }
    )

    with pytest.raises(FormalConceptSequenceError) as exc:
        validate_formal_transformation_sequence(tampered)
    assert exc.value.reason_code == FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID
