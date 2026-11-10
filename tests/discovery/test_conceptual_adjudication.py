# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial tests for blind, content-warranted conceptual adjudication."""

from __future__ import annotations

import copy
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery.conceptual_adjudication import (
    ConceptualAdjudicationError,
    DIMENSIONS,
    aggregate_adjudication,
    build_adjudication_evidence,
    build_adjudication_source_bindings,
    build_blind_packet,
    build_judge_report,
    validate_adjudication_evidence,
    validate_judge_report,
    validate_sealed_preference_authority,
)
from agentic.discovery.contracts import ContractError, canonical_digest
from agentic.discovery.contracts import validate_instance
from agentic.discovery.semantic_identity import semantic_signature
from agentic.scripts.run_discovery_operator_protocol import _conceptual_adjudication
from agentic.scripts.validate_discovery_operator_protocol import validate as validate_operator_output


def _system(system_id: str, *, deep: bool) -> dict[str, Any]:
    if deep:
        mechanism = (
            "A scale-production witness creates the candidate invariant, a detector-conservativity "
            "witness interprets every nonvacuum mode, and coherent descent preserves both across presentations."
        )
        differences = [
            "Scale production does not imply detector completeness.",
            "Detector completeness does not imply regulator-independent descent.",
            "Descent coherence does not create a positive physical scale.",
        ]
        questions = [
            "Which independent estimate produces the scale without assuming the conclusion?",
            "Which countermodel separates complete detection from stable descent?",
            "Which comparison loop reveals a nonzero holonomy obstruction?",
        ]
    else:
        mechanism = "The framework unifies everything through one deep principle."
        differences = ["Different cases remain different in appropriate ways."]
        questions = ["Can the framework be proved?"]
    return {
        "system_id": system_id,
        "primitives": ["scale witness", "detector witness", "descent witness"] if deep else ["framework"],
        "relations_operations_and_dynamics": [mechanism],
        "mechanism_or_principle": mechanism,
        "target_pressures_addressed": [
            "construct the target without assuming its conclusion",
            "preserve physical meaning through representation change",
        ],
        "identities_and_differences": differences,
        "unification_claims": {
            "unified_cases_or_routes": ["construction", "interpretation", "descent"] if deep else ["all cases"],
            "common_principle": mechanism,
            "differences_preserved": differences,
        },
        "implications_and_new_questions": questions,
        "formalization_seeds": questions,
        "correction_conditions": [
            "Reject the programme if any witness is defined by the desired conclusion.",
            "Split the mediator if a finite countermodel invalidates one claimed dependency.",
        ] if deep else ["Revise if this is wrong."],
        "residual_contradictions": [
            "No current theorem establishes all three witnesses in the target regime."
        ],
        "non_claims": ["This conceptual programme proves no target theorem."],
    }


def _round(
    system_id: str,
    index: int,
    *,
    changed_paths: tuple[str, ...] = (),
    objection: str = (
        "The mediator may rename missing estimates unless each witness has an independent correction test."
    ),
    correction_test: str = (
        "Reject the mutation unless its exact changed paths answer this objection without weakening any other conceptual dimension."
    ),
) -> dict[str, Any]:
    row = {
        "round_id": f"round-{index}",
        "system_ids": [system_id],
        "strongest_objections": [objection],
        "correction_tests": [correction_test],
        "mutation_or_synthesis": {
            "operation": "separate the three non-substitutable burdens",
            "changed_primitives_relations_or_explanation": ["detector conservativity"],
        },
        "result": "mutated",
    }
    if changed_paths:
        row["semantic_patch_links"] = [
            {
                "candidate_ref": system_id,
                "objection": objection,
                "correction_test": correction_test,
                "changed_paths": list(changed_paths),
            }
        ]
    return row


def _packet(systems: list[dict[str, Any]], rounds: list[dict[str, Any]], stage: str = "parent"):
    return build_blind_packet(
        target_id="target",
        stage_id=stage,
        target_charter={"root_tensions": ["construction versus interpretation"]},
        systems=systems,
        reflection_rounds=rounds,
        proposer_identity="proposer",
        source_bindings={"literature_digest": canonical_digest("sources")},
    )


def _judge(candidate: Mapping[str, Any], packet: Mapping[str, Any]) -> Mapping[str, Any]:
    content = candidate["content"]
    unification = content.get("unification_claims", {})
    typed_unification = "source_case_ids" in unification
    mechanism = str(content.get("mechanism_or_principle", ""))
    deep = (
        len(content.get("primitives", [])) >= 3
        and "witness" in mechanism
        and "preserves both" in mechanism
    )
    rounds = len(packet.get("reflection_rounds", []))
    paths = {
        "essential_relevance": "/target_pressures_addressed",
        "explanatory_mediation": "/mechanism_or_principle",
        "conceptual_depth": "/primitives",
        "unification_power": (
            "/unification_claims/source_case_ids"
            if typed_unification
            else "/unification_claims/unified_cases_or_routes"
        ),
        "preserved_difference": (
            "/unification_claims/preserved_differences"
            if typed_unification
            else "/unification_claims/differences_preserved"
        ),
        "generativity": "/formalization_seeds",
        "reflective_resilience": "/correction_conditions",
        "truth_aptness": "/residual_contradictions",
    }
    output = {}
    for dimension in DIMENSIONS:
        rating = "strong" if deep else "weak"
        if dimension == "reflective_resilience":
            rating = "strong" if deep and rounds >= 2 else "adequate" if deep else "weak"
        path = paths[dimension]
        value = content
        for token in path.lstrip("/").split("/"):
            value = value[token]
        output[dimension] = {
            "rating": rating,
            "warrants": [{
                "path": path,
                "value_digest": canonical_digest(value),
                "explanation": "The named mechanism assigns non-substitutable production, interpretation, and descent roles with an explicit causal order.",
            }],
            "strongest_objection": "The apparent mediator could still be decorative unless independent countermodels separate every claimed explanatory dependency.",
            "correction_test": "Construct the declared finite independence models and demote the system if any witness is definitionally circular.",
        }
    return output


def _reports(
    packet: Mapping[str, Any], *, independence_claim: str = "correlated_internal"
) -> list[dict[str, Any]]:
    return [
        build_judge_report(
            packet,
            adjudicator_id=f"judge-{index}",
            perspective=perspective,
            version="1.0.0",
            judge=_judge,
            created_at="2026-07-21T00:00:00Z",
            independence_claim=independence_claim,
        )
        for index, perspective in enumerate(
            ("explanatory", "unificatory", "adversarial"), 1
        )
    ]


def test_blind_panel_selects_content_not_system_id_or_order() -> None:
    systems = [_system("desired-looking-id", deep=False), _system("plain-id", deep=True)]
    packet, bindings = _packet(systems, [_round("plain-id", 1), _round("plain-id", 2)])
    adjudication = aggregate_adjudication(packet, _reports(packet), candidate_bindings=bindings)
    assert adjudication["selected_system_id"] == "plain-id"
    assert adjudication["authority"]["external_human_evidence_available"] is False
    assert adjudication["authority"]["external_human_evidence_status"] == "unavailable"
    assert adjudication["authority"]["plural_independent_perspectives"] is False
    assert adjudication["authority"]["panel_evidence_class"] == "correlated_internal_critique"
    renamed = copy.deepcopy(systems)
    renamed[0]["system_id"] = "plain-id-renamed-shallow"
    renamed[1]["system_id"] = "desired-looking-id-renamed-deep"
    packet2, bindings2 = _packet(list(reversed(renamed)), [_round("desired-looking-id-renamed-deep", 1), _round("desired-looking-id-renamed-deep", 2)])
    adjudication2 = aggregate_adjudication(packet2, _reports(packet2), candidate_bindings=bindings2)
    assert adjudication2["selected_system_id"] == "desired-looking-id-renamed-deep"


def test_same_field_counts_with_shallow_mechanism_do_not_pass_content_judges() -> None:
    deep = _system("deep", deep=True)
    shallow = copy.deepcopy(deep)
    shallow["system_id"] = "shallow"
    shallow["mechanism_or_principle"] = "Framework framework framework framework framework framework."
    shallow["primitives"] = ["framework", "framework-copy", "framework-shadow"]
    packet, bindings = _packet([shallow, deep], [_round("deep", 1), _round("deep", 2)])
    # This fixture judge uses typed primitives only, illustrating why judge
    # warrant logic itself must be adversarially tested. Replace its finding for
    # the shallow alias with weak content judgments and prove aggregation obeys it.
    reports = _reports(packet)
    shallow_alias = next(alias for alias, system_id in bindings.items() if system_id == "shallow")
    for report in reports:
        row = next(item for item in report["candidate_findings"] if item["candidate_alias"] == shallow_alias)
        for finding in row["dimensions"].values():
            finding["rating"] = "weak"
        report["report_digest"] = canonical_digest(report, exclude_keys=("report_digest", "created_at"))
    adjudication = aggregate_adjudication(packet, reports, candidate_bindings=bindings)
    assert adjudication["selected_system_id"] == "deep"


def test_warrant_digest_and_complete_plural_coverage_fail_closed() -> None:
    packet, _ = _packet([_system("a", deep=False), _system("b", deep=True)], [_round("b", 1)])
    report = _reports(packet)[0]
    broken = copy.deepcopy(report)
    broken["candidate_findings"][0]["dimensions"][DIMENSIONS[0]]["warrants"][0]["value_digest"] = canonical_digest("forged")
    broken["report_digest"] = canonical_digest(broken, exclude_keys=("report_digest", "created_at"))
    with pytest.raises(ContractError, match="warrant digest mismatch"):
        validate_judge_report(broken, packet)


def test_stage_comparison_requires_exact_objection_linked_content_patch() -> None:
    systems = [_system("shallow", deep=False), _system("deep", deep=True)]
    parent_packet, parent_bindings = _packet(systems, [_round("deep", 1)], "parent")
    parent = aggregate_adjudication(parent_packet, _reports(parent_packet), candidate_bindings=parent_bindings)
    synthesis_systems = copy.deepcopy(systems)
    synthesis_systems[1]["mechanism_or_principle"] += (
        " The revised account now makes the detector failure an explicit dependency rather than a tacit bridge."
    )
    synthesis_packet, synthesis_bindings = _packet(
        synthesis_systems,
        [_round("deep", 1), _round("deep", 2, changed_paths=("/mechanism_or_principle",))],
        "synthesis",
    )
    synthesis = aggregate_adjudication(
        synthesis_packet,
        _reports(synthesis_packet),
        candidate_bindings=synthesis_bindings,
        previous=parent,
        previous_packet=parent_packet,
    )
    assert synthesis["stage_comparison"]["material"] is True
    patch = synthesis["stage_comparison"]["semantic_patch"]
    assert patch["content_changed"] is True
    assert patch["all_changes_objection_linked"] is True
    assert patch["objection_links"][0]["changed_paths"] == ["/mechanism_or_principle"]
    assert patch["component_digests"]["claims"]["changed"] is True
    assert patch["component_digests"]["objections"]["changed"] is True
    assert patch["component_digests"]["corrections"]["changed"] is True
    assert parent["adjudication_id"] != synthesis["adjudication_id"]


def test_fewer_than_three_perspectives_cannot_authorize_preference() -> None:
    packet, bindings = _packet([_system("a", deep=False), _system("b", deep=True)], [_round("b", 1)])
    with pytest.raises(ContractError, match="at least three"):
        aggregate_adjudication(packet, _reports(packet)[:2], candidate_bindings=bindings)


def test_identity_labels_cannot_turn_one_callable_into_independent_judges() -> None:
    packet, bindings = _packet(
        [_system("a", deep=False), _system("b", deep=True)], [_round("b", 1)]
    )
    reports = _reports(packet, independence_claim="independent_internal")
    assert len({row["adjudicator"]["executable_digest"] for row in reports}) == 1
    with pytest.raises(ContractError, match="claimed independence.*share"):
        aggregate_adjudication(packet, reports, candidate_bindings=bindings)


def _judge_wrapper_one(
    candidate: Mapping[str, Any], packet: Mapping[str, Any]
) -> Mapping[str, Any]:
    return _judge(candidate, packet)


def _judge_wrapper_two(
    candidate: Mapping[str, Any], packet: Mapping[str, Any]
) -> Mapping[str, Any]:
    return _judge(candidate, packet)


def _judge_wrapper_three(
    candidate: Mapping[str, Any], packet: Mapping[str, Any]
) -> Mapping[str, Any]:
    return _judge(candidate, packet)


def test_shared_module_wrappers_are_still_correlated_when_claimed_independent() -> None:
    packet, bindings = _packet(
        [_system("a", deep=False), _system("b", deep=True)], [_round("b", 1)]
    )
    reports = [
        build_judge_report(
            packet,
            adjudicator_id=f"wrapper-{index}",
            perspective=perspective,
            version="1.0.0",
            judge=judge,
            independence_claim="independent_internal",
            created_at="2026-07-21T00:00:00Z",
        )
        for index, (perspective, judge) in enumerate(
            zip(
                ("explanatory", "unificatory", "adversarial"),
                (_judge_wrapper_one, _judge_wrapper_two, _judge_wrapper_three),
                strict=True,
            ),
            1,
        )
    ]
    assert len({row["adjudicator"]["executable_digest"] for row in reports}) == 3
    assert len(
        {
            row["adjudicator"]["authority"]["correlation_group_digest"]
            for row in reports
        }
    ) == 1
    with pytest.raises(ContractError, match="claimed independence.*share"):
        aggregate_adjudication(packet, reports, candidate_bindings=bindings)


def test_recorded_callable_authority_is_recomputed_when_callable_is_available() -> None:
    packet, _ = _packet(
        [_system("a", deep=False), _system("b", deep=True)], [_round("b", 1)]
    )
    report = _reports(packet)[0]
    validate_judge_report(report, packet, judge=_judge)
    with pytest.raises(ContractError, match="callable does not match"):
        validate_judge_report(report, packet, judge=_judge_wrapper_one)


def test_recursive_blinding_rejects_preference_fields_and_seals_counterbalancing() -> None:
    systems = [_system("candidate-alpha-id", deep=False), _system("candidate-beta-id", deep=True)]
    systems[0]["nested"] = {"expected_winner": "candidate-alpha-id"}
    with pytest.raises(ContractError, match="forbidden field"):
        _packet(systems, [_round("candidate-beta-id", 1)])

    clean = [_system("candidate-alpha-id", deep=False), _system("candidate-beta-id", deep=True)]
    clean[1]["conceptual_ancestors"] = ["candidate-alpha-id"]
    packet, bindings = build_blind_packet(
        target_id="target",
        stage_id="parent",
        target_charter={"root_tensions": ["construction versus interpretation"]},
        systems=clean,
        reflection_rounds=[_round("candidate-beta-id", 1)],
        proposer_identity="proposer",
        source_bindings={"literature_digest": canonical_digest("sources")},
        counterbalance_seed="sealed-test-seed",
    )
    reversed_packet, reversed_bindings = build_blind_packet(
        target_id="target",
        stage_id="parent",
        target_charter={"root_tensions": ["construction versus interpretation"]},
        systems=list(reversed(clean)),
        reflection_rounds=[_round("candidate-beta-id", 1)],
        proposer_identity="proposer",
        source_bindings={"literature_digest": canonical_digest("sources")},
        counterbalance_seed="sealed-test-seed",
    )
    assert "proposer_identity" not in packet
    assert packet["proposer_identity_digest"] == canonical_digest("proposer")
    assert packet["counterbalancing"] == reversed_packet["counterbalancing"]
    assert packet["candidates"] == reversed_packet["candidates"]
    assert bindings == reversed_bindings
    rendered = repr(packet)
    assert "candidate-alpha-id" not in rendered
    assert "candidate-beta-id" not in rendered


def test_warrant_must_name_its_dimension_and_relevant_content_surface() -> None:
    packet, _ = _packet(
        [_system("a", deep=False), _system("b", deep=True)], [_round("b", 1)]
    )
    report = _reports(packet)[0]
    broken = copy.deepcopy(report)
    finding = broken["candidate_findings"][0]["dimensions"]["essential_relevance"]
    finding["warrants"][0]["dimension"] = "conceptual_depth"
    broken["report_digest"] = canonical_digest(
        broken, exclude_keys=("report_digest", "created_at")
    )
    with pytest.raises(ContractError, match="not dimension-specific"):
        validate_judge_report(broken, packet)

    broken = copy.deepcopy(report)
    finding = broken["candidate_findings"][0]["dimensions"]["essential_relevance"]
    finding["warrants"][0]["path"] = "/mechanism_or_principle"
    finding["warrants"][0]["value_digest"] = canonical_digest(
        broken["candidate_findings"][0]
    )
    broken["report_digest"] = canonical_digest(
        broken, exclude_keys=("report_digest", "created_at")
    )
    with pytest.raises(ContractError, match="not relevant"):
        validate_judge_report(broken, packet)


def _parent_and_modified_synthesis(
    *,
    new_round: dict[str, Any],
    mechanism: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    systems = [_system("shallow", deep=False), _system("deep", deep=True)]
    parent_packet, parent_bindings = _packet(systems, [_round("deep", 1)], "parent")
    parent = aggregate_adjudication(
        parent_packet, _reports(parent_packet), candidate_bindings=parent_bindings
    )
    synthesis_systems = copy.deepcopy(systems)
    synthesis_systems[1]["mechanism_or_principle"] = mechanism or (
        synthesis_systems[1]["mechanism_or_principle"]
        + " The revised dependency explicitly answers the registered objection while preserving both witnesses."
    )
    synthesis_packet, synthesis_bindings = _packet(
        synthesis_systems, [_round("deep", 1), new_round], "synthesis"
    )
    synthesis = aggregate_adjudication(
        synthesis_packet,
        _reports(synthesis_packet),
        candidate_bindings=synthesis_bindings,
        previous=parent,
        previous_packet=parent_packet,
    )
    return parent, synthesis


def test_new_round_without_content_change_is_not_material() -> None:
    systems = [_system("shallow", deep=False), _system("deep", deep=True)]
    parent_packet, parent_bindings = _packet(systems, [_round("deep", 1)], "parent")
    parent = aggregate_adjudication(
        parent_packet, _reports(parent_packet), candidate_bindings=parent_bindings
    )
    synthesis_packet, synthesis_bindings = _packet(
        systems,
        [_round("deep", 1), _round("deep", 2, changed_paths=("/mechanism_or_principle",))],
        "synthesis",
    )
    synthesis = aggregate_adjudication(
        synthesis_packet,
        _reports(synthesis_packet),
        candidate_bindings=synthesis_bindings,
        previous=parent,
        previous_packet=parent_packet,
    )
    assert synthesis["stage_comparison"]["material"] is False
    assert synthesis["stage_comparison"]["semantic_patch"]["content_changed"] is False


def test_sham_objection_cannot_authorize_a_real_content_change() -> None:
    sham = _round(
        "deep",
        2,
        changed_paths=("/mechanism_or_principle",),
        objection="An unrelated stylistic concern asks whether the prose could be shorter for a novice reader.",
    )
    # The link cites a different objection than the round actually records.
    sham["semantic_patch_links"][0]["objection"] = (
        "The exact dependency remains circular unless the changed mechanism answers this registered objection."
    )
    _, synthesis = _parent_and_modified_synthesis(new_round=sham)
    comparison = synthesis["stage_comparison"]
    assert comparison["material"] is False
    assert comparison["semantic_patch"]["objection_links"] == []
    assert comparison["semantic_patch"]["invalid_link_reasons"]


def test_round_removal_or_history_rewrite_cannot_count_as_reflective_improvement() -> None:
    systems = [_system("shallow", deep=False), _system("deep", deep=True)]
    parent_rounds = [_round("deep", 1), _round("deep", 2)]
    parent_packet, parent_bindings = _packet(systems, parent_rounds, "parent")
    parent = aggregate_adjudication(
        parent_packet, _reports(parent_packet), candidate_bindings=parent_bindings
    )
    changed = copy.deepcopy(systems)
    changed[1]["mechanism_or_principle"] += " The mutation preserves both witnesses explicitly."
    synthesis_packet, synthesis_bindings = _packet(
        changed,
        [_round("deep", 1, changed_paths=("/mechanism_or_principle",))],
        "synthesis",
    )
    synthesis = aggregate_adjudication(
        synthesis_packet,
        _reports(synthesis_packet),
        candidate_bindings=synthesis_bindings,
        previous=parent,
        previous_packet=parent_packet,
    )
    assert synthesis["stage_comparison"]["material"] is False
    assert synthesis["stage_comparison"]["round_history_prefix_preserved"] is False
    assert synthesis["stage_comparison"]["new_reflection_rounds"] == 0


def test_equal_count_semantic_degradation_fails_closed() -> None:
    degraded = (
        "Generic framework language repeats a neutral placeholder account while decorative labels preserve every field count and apparent sentence length."
    )
    _, synthesis = _parent_and_modified_synthesis(
        new_round=_round("deep", 2, changed_paths=("/mechanism_or_principle",)),
        mechanism=degraded,
    )
    assert synthesis["stage_comparison"]["material"] is False
    assert synthesis["stage_comparison"]["nondegrading_dimension_floors"] is False


def test_candidate_and_report_permutations_preserve_the_adjudication() -> None:
    systems = [_system("candidate-a-id", deep=False), _system("candidate-b-id", deep=True)]
    packet, bindings = build_blind_packet(
        target_id="target",
        stage_id="parent",
        target_charter={"root_tensions": ["construction versus interpretation"]},
        systems=systems,
        reflection_rounds=[_round("candidate-b-id", 1)],
        proposer_identity="proposer",
        source_bindings={"literature_digest": canonical_digest("sources")},
        counterbalance_seed="permutation-seed",
    )
    permuted_packet, permuted_bindings = build_blind_packet(
        target_id="target",
        stage_id="parent",
        target_charter={"root_tensions": ["construction versus interpretation"]},
        systems=list(reversed(systems)),
        reflection_rounds=[_round("candidate-b-id", 1)],
        proposer_identity="proposer",
        source_bindings={"literature_digest": canonical_digest("sources")},
        counterbalance_seed="permutation-seed",
    )
    reports = _reports(packet)
    first = aggregate_adjudication(packet, reports, candidate_bindings=bindings)
    second = aggregate_adjudication(
        permuted_packet,
        list(reversed(_reports(permuted_packet))),
        candidate_bindings=permuted_bindings,
    )
    assert packet == permuted_packet
    assert bindings == permuted_bindings
    assert first == second


def test_schema_rejects_untyped_consensus_and_stage_comparison_mutations() -> None:
    _, synthesis = _parent_and_modified_synthesis(
        new_round=_round("deep", 2, changed_paths=("/mechanism_or_principle",))
    )
    malformed = copy.deepcopy(synthesis)
    malformed["candidate_consensus"][0]["dimensions"].pop("truth_aptness")
    with pytest.raises(ContractError, match="schema validation failed"):
        validate_instance(malformed, "conceptual_adjudication.schema.json")


def _typed_system(system_id: str, *, deep: bool) -> dict[str, Any]:
    system = _system(system_id, deep=deep)
    before_graph = {
        "nodes": [
            {
                "node_id": "construction-case",
                "node_kind": "source_case",
                "label": "Construction target burden",
                "content_paths": ["/target_pressures_addressed/0"],
            },
            {
                "node_id": "interpretation-case",
                "node_kind": "source_case",
                "label": "Interpretation target burden",
                "content_paths": ["/target_pressures_addressed/1"],
            },
        ],
        "edges": [],
    }
    added_nodes = [
        {
            "node_id": "witness-mediated-interface",
            "node_kind": "mediator",
            "label": "Witness mediated explanatory interface",
            "content_paths": [
                "/mechanism_or_principle",
                "/unification_claims/mediator/statement",
            ],
        }
    ]
    added_edges = [
        {
            "edge_id": "construction-to-mediator",
            "source_node_id": "construction-case",
            "relation_kind": "mediates",
            "target_node_id": "witness-mediated-interface",
            "statement": "Construction is mediated through an independently correctable production witness.",
            "warrant_paths": ["/mechanism_or_principle"],
        },
        {
            "edge_id": "interpretation-to-mediator",
            "source_node_id": "interpretation-case",
            "relation_kind": "constrains",
            "target_node_id": "witness-mediated-interface",
            "statement": "Interpretation is constrained by a separately falsifiable detector witness.",
            "warrant_paths": ["/mechanism_or_principle"],
        },
    ]
    after_graph = {
        "nodes": [*before_graph["nodes"], *added_nodes],
        "edges": added_edges,
    }
    system["unification_claims"] = {
        "unification_kind": "regime_indexed_mediation",
        "source_case_ids": ["construction-case", "interpretation-case"],
        "mediator": {
            "statement": (
                "An independently correctable witness interface relates construction and interpretation without identifying their burdens."
            ),
            "primitive_refs": [
                "independently correctable scale production witness primitive"
            ],
            "relation_refs": [
                "regime indexed mediation preserving non substitutable burdens"
            ],
            "node_ids": ["witness-mediated-interface"],
        },
        "mappings": [
            {
                "mapping_id": "construction-production-map",
                "source_case_id": "construction-case",
                "target_node_id": "witness-mediated-interface",
                "map_kind": "production",
                "bridge_statement": (
                    "Construction enters only through a scale-producing witness whose definition does not assume the target conclusion."
                ),
                "warrant_paths": [
                    "/mechanism_or_principle",
                    "/relations_operations_and_dynamics/0",
                ],
            },
            {
                "mapping_id": "interpretation-detector-map",
                "source_case_id": "interpretation-case",
                "target_node_id": "witness-mediated-interface",
                "map_kind": "interpretation",
                "bridge_statement": (
                    "Interpretation enters through a detector-conservativity witness with a logically separate correction condition."
                ),
                "warrant_paths": [
                    "/mechanism_or_principle",
                    "/relations_operations_and_dynamics/0",
                ],
            },
        ],
        "preserved_differences": [
            {
                "difference_id": "construction-not-interpretation",
                "source_case_ids": ["construction-case"],
                "statement": (
                    "Producing a nonzero scale remains distinct from proving that the detector interprets every relevant mode."
                ),
                "preservation_witness_paths": ["/identities_and_differences/0"],
                "witness_node_ids": [
                    "construction-case",
                    "witness-mediated-interface",
                ],
                "witness_edge_ids": ["construction-to-mediator"],
            },
            {
                "difference_id": "interpretation-not-construction",
                "source_case_ids": ["interpretation-case"],
                "statement": (
                    "Detector completeness remains distinct from constructing the positive scale it is intended to interpret."
                ),
                "preservation_witness_paths": ["/identities_and_differences/0"],
                "witness_node_ids": [
                    "interpretation-case",
                    "witness-mediated-interface",
                ],
                "witness_edge_ids": ["interpretation-to-mediator"],
            },
        ],
        "explanatory_graph_transition": {
            "before_graph": before_graph,
            "after_graph": after_graph,
            "before_graph_digest": canonical_digest(before_graph),
            "after_graph_digest": canonical_digest(after_graph),
            "added_nodes": added_nodes,
            "added_edges": added_edges,
            "new_explanatory_dependencies": [
                "Scale production now precedes detector interpretation through an independently correctable witness interface."
            ],
        },
        "scope_conditions": [
            "The mediation applies only where both witnesses are defined in the same target regime."
        ],
        "transfer_obligations": [
            "Prove that each mapping preserves its declared source burden without importing the desired conclusion."
        ],
        "erasure_risks": [
            "A single undifferentiated witness would erase the distinction between production and interpretation."
        ],
        "failure_conditions": [
            "Demote the unification if either source burden disappears from the exact explanatory graph transition."
        ],
    }
    return system


_LENS_LANGUAGE = {
    "ontological": {
        "question": "Which primitive commitments make the witness interface explanatory rather than merely notational in this target?",
        "tension": "The theory requires a real mediator while denying that construction and interpretation are the same ontological burden.",
        "assumption": "The inherited frame assumes that one primitive can simultaneously create and interpret the target structure.",
        "analysis": "The candidate improves ontology by assigning production, detection, and descent to distinct correctable witness roles.",
        "consequence": "Keep the witness interface primitive while preserving separate construction and interpretation commitments.",
        "question_out": "Which target invariant distinguishes an ontologically real witness interface from a convenient presentation device?",
    },
    "dialectical": {
        "question": "Which opposition between production and interpretation is genuinely mediated rather than hidden by the proposed interface?",
        "tension": "Construction demands a positive scale while interpretation demands conservative detection, and neither demand entails the other.",
        "assumption": "The inherited synthesis assumes disagreement disappears once both burdens receive the same abstract vocabulary.",
        "analysis": "The candidate preserves the opposition and mediates it through correction conditions that can fail independently.",
        "consequence": "Register the unresolved opposition as a constraint on every claimed bridge between the two burdens.",
        "question_out": "Which countermodel separates genuine dialectical mediation from a verbal compromise between incompatible target burdens?",
    },
    "explanatory": {
        "question": "Which dependency makes the witness interface increase understanding instead of adding another descriptive layer?",
        "tension": "The interface must compress two routes while retaining the causal order and the failure modes that distinguish them.",
        "assumption": "The inherited explanation treats co-occurrence of successful routes as sufficient evidence for a common mechanism.",
        "analysis": "The candidate adds a directional dependency from scale production through detector interpretation to coherent descent.",
        "consequence": "Require the new explanatory dependency to change a target question and survive an explicit removal test.",
        "question_out": "Which finite removal test shows that the new explanatory dependency changes the physics research programme materially?",
    },
}


def _deep_lens_judgment(
    candidate: Mapping[str, Any], packet: Mapping[str, Any], lens_family: str
) -> Mapping[str, Any]:
    language = _LENS_LANGUAGE[lens_family]
    content = candidate["content"]
    dimensions = _judge(candidate, packet)
    warrant_paths = ["/mechanism_or_principle", "/unification_claims/mediator/statement"]
    warrants = []
    for path in warrant_paths:
        value: Any = content
        for token in path.lstrip("/").split("/"):
            value = value[token]
        warrants.append(
            {
                "path": path,
                "value_digest": canonical_digest(value),
                "explanation": (
                    "This exact candidate content bears on the lens because it identifies the mediator and its non-substitutable explanatory role."
                ),
            }
        )
    return {
        "dimensions": dimensions,
        "deep_lens_analysis": {
            "lens_family": lens_family,
            "focal_question": language["question"],
            "content_warrants": warrants,
            "root_aporia_or_tension": language["tension"],
            "inherited_assumption_exposed": language["assumption"],
            "candidate_specific_analysis": language["analysis"],
            "conceptual_consequence": {
                "kind": "tension_registered" if lens_family == "dialectical" else "relation_revised",
                "changed_paths": ["/mechanism_or_principle"],
                "statement": language["consequence"],
            },
            "physics_value_handback": {
                "target_pressure_paths": ["/target_pressures_addressed/0"],
                "changed_theory_question": language["question_out"],
                "relevance_limit": (
                    "This conceptual judgment changes only the target research question and establishes no theorem, physical equivalence, or mass gap."
                ),
            },
            "strongest_objection": (
                "The proposed conceptual change may remain decorative unless its exact dependency survives an independent countermodel."
            ),
            "correction_test": (
                "Remove the declared mediator and demote the analysis unless a target-relevant explanatory dependency is thereby lost."
            ),
        },
    }


def _ontological_judge(
    candidate: Mapping[str, Any], packet: Mapping[str, Any]
) -> Mapping[str, Any]:
    return _deep_lens_judgment(candidate, packet, "ontological")


def _dialectical_judge(
    candidate: Mapping[str, Any], packet: Mapping[str, Any]
) -> Mapping[str, Any]:
    return _deep_lens_judgment(candidate, packet, "dialectical")


def _explanatory_judge(
    candidate: Mapping[str, Any], packet: Mapping[str, Any]
) -> Mapping[str, Any]:
    return _deep_lens_judgment(candidate, packet, "explanatory")


def _evidence_fixture(*, both_deep: bool = False) -> tuple[dict[str, Any], dict[str, Any]]:
    systems = [
        _typed_system("candidate-a", deep=both_deep),
        _typed_system("candidate-b", deep=True),
    ]
    rounds = [_round("candidate-b", 1), _round("candidate-b", 2)]
    genealogy = [_typed_system("ancestor-system", deep=False)]
    source_bindings = build_adjudication_source_bindings(
        run_id="run-one",
        state_version=0,
        theory_state_digest=canonical_digest("theory-state"),
        literature_snapshot_digest=canonical_digest("literature"),
        high_risk_portfolio_digest=canonical_digest("portfolio"),
        systems=systems,
        reflection_rounds=rounds,
        frozen_genealogy=genealogy,
        proposer_receipt_ids=["proposal-receipt-1"],
    )
    packet, bindings = build_blind_packet(
        target_id="target",
        stage_id="post-reflection",
        target_charter={"root_tensions": ["construction versus interpretation"]},
        systems=systems,
        reflection_rounds=rounds,
        proposer_identity="proposer",
        source_bindings=source_bindings,
        counterbalance_seed="sealed-evidence-seed",
    )
    reports = [
        build_judge_report(
            packet,
            adjudicator_id=f"judge-{lens}",
            perspective=lens,
            lens_family=lens,
            version="1.0.0",
            judge=judge,
            created_at="2026-07-22T00:00:00Z",
        )
        for lens, judge in (
            ("ontological", _ontological_judge),
            ("dialectical", _dialectical_judge),
            ("explanatory", _explanatory_judge),
        )
    ]
    context = {
        "systems": systems,
        "reflection_rounds": rounds,
        "frozen_genealogy": genealogy,
        "candidate_bindings": bindings,
        "theory_state_digest": canonical_digest("theory-state"),
        "literature_snapshot_digest": canonical_digest("literature"),
        "high_risk_portfolio_digest": canonical_digest("portfolio"),
        "proposer_receipt_ids": ["proposal-receipt-1"],
    }
    evidence = build_adjudication_evidence(
        packet=packet,
        reports=reports,
        run_id="run-one",
        state_version=0,
        created_at="2026-07-22T00:00:00Z",
        **context,
    )
    return evidence, context


def _rehash_evidence(evidence: dict[str, Any]) -> None:
    evidence["evidence_digest"] = canonical_digest(
        evidence, exclude_keys=("evidence_digest", "created_at")
    )


def test_receipt_bound_evidence_recomputes_unique_preference_and_all_closures() -> None:
    evidence, context = _evidence_fixture()
    validate_adjudication_evidence(evidence, **context)
    assert evidence["panel_seal"]["lens_families"] == [
        "dialectical",
        "explanatory",
        "ontological",
    ]
    assert evidence["unblinding_receipt"]["panel_seal_digest"] == evidence[
        "panel_seal"
    ]["panel_seal_digest"]
    assert evidence["preference_set"]["decision"] == "prefer_unique"
    assert evidence["preference_set"]["preferred_system_ids"] == ["candidate-b"]
    assert evidence["authority"]["structural_scores_authorize_preference"] is False


def test_downstream_sealed_authority_rejects_post_adjudication_content_splice() -> None:
    evidence, context = _evidence_fixture()
    preference = validate_sealed_preference_authority(
        evidence,
        target_id="target",
        run_id="run-one",
        state_version=0,
        system_ids=[row["system_id"] for row in context["systems"]],
        systems=context["systems"],
        reflection_rounds=context["reflection_rounds"],
    )
    assert preference["preferred_system_ids"] == ["candidate-b"]

    spliced_systems = copy.deepcopy(context["systems"])
    spliced_systems[1]["mechanism_or_principle"] = (
        "Post-seal content substituted under the same candidate identity."
    )
    with pytest.raises(
        ConceptualAdjudicationError, match="adjudication_input_binding_mismatch"
    ):
        validate_sealed_preference_authority(
            evidence,
            target_id="target",
            run_id="run-one",
            state_version=0,
            system_ids=[row["system_id"] for row in spliced_systems],
            systems=spliced_systems,
            reflection_rounds=context["reflection_rounds"],
        )

    spliced_rounds = copy.deepcopy(context["reflection_rounds"])
    spliced_rounds[0]["result"] = "no_change"
    with pytest.raises(
        ConceptualAdjudicationError, match="adjudication_input_binding_mismatch"
    ):
        validate_sealed_preference_authority(
            evidence,
            target_id="target",
            run_id="run-one",
            state_version=0,
            system_ids=[row["system_id"] for row in context["systems"]],
            systems=context["systems"],
            reflection_rounds=spliced_rounds,
        )


def test_registered_adjudicator_executor_rebuilds_the_sealed_evidence() -> None:
    evidence, context = _evidence_fixture()
    envelope = {
        **context,
        "blind_packet": evidence["blind_packet"],
        "judge_reports": evidence["judge_reports"],
        "created_at": evidence["created_at"],
    }
    rebuilt, unknowns = _conceptual_adjudication(
        {
            "identity": {
                "target_id": "target",
                "run_id": "run-one",
                "branch_id": "root",
                "state_version": 0,
            }
        },
        envelope,
    )
    assert rebuilt == evidence
    assert rebuilt["preference_set"]["preferred_system_ids"] == ["candidate-b"]
    assert any("not proof" in boundary for boundary in unknowns)


def test_registered_adjudicator_replays_the_complete_previous_evidence() -> None:
    previous, context = _evidence_fixture()
    envelope = {
        **context,
        "blind_packet": previous["blind_packet"],
        "judge_reports": previous["judge_reports"],
        "created_at": previous["created_at"],
        "previous_evidence": previous,
        "previous_evidence_digest": previous["evidence_digest"],
    }
    request = {
        "operator": {"operator_id": "blind-conceptual-preference-adjudicator"},
        "identity": {
            "target_id": "target",
            "run_id": "run-one",
            "branch_id": "root",
            "state_version": 0,
        },
    }

    rebuilt, _unknowns = _conceptual_adjudication(request, envelope)
    assert rebuilt["input_binding"]["previous_evidence_digest"] == previous[
        "evidence_digest"
    ]
    assert rebuilt["content_adjudication"]["stage_comparison"]["applicability"] == (
        "applicable"
    )
    validate_operator_output(
        "blind-conceptual-preference-adjudicator",
        request,
        envelope,
        rebuilt,
        workspace=Path.cwd(),
    )


@pytest.mark.parametrize("attack", ["digest_only", "mismatched_descriptor"])
def test_registered_adjudicator_rejects_prior_authority_without_exact_bytes(
    attack: str,
) -> None:
    previous, context = _evidence_fixture()
    envelope = {
        **context,
        "blind_packet": previous["blind_packet"],
        "judge_reports": previous["judge_reports"],
        "created_at": previous["created_at"],
        "previous_evidence_digest": previous["evidence_digest"],
    }
    if attack == "mismatched_descriptor":
        envelope["previous_evidence"] = previous
        envelope["previous_evidence_digest"] = canonical_digest("substituted-prior")

    with pytest.raises(ContractError, match="previous.*evidence"):
        _conceptual_adjudication(
            {
                "identity": {
                    "target_id": "target",
                    "run_id": "run-one",
                    "branch_id": "root",
                    "state_version": 0,
                }
            },
            envelope,
        )


def test_receipt_bound_evidence_preserves_plural_nondominated_preference() -> None:
    evidence, context = _evidence_fixture(both_deep=True)
    validate_adjudication_evidence(evidence, **context)
    assert evidence["preference_set"]["decision"] == "retain_plural_nondominated"
    assert evidence["preference_set"]["preferred_system_ids"] == [
        "candidate-a",
        "candidate-b",
    ]
    assert evidence["content_adjudication"]["selected_system_id"] is None
    assert evidence["content_adjudication"]["authority"][
        "conceptual_preference_authorized"
    ] is True


def test_panel_requires_ontological_dialectical_and_distinct_third_lens() -> None:
    evidence, context = _evidence_fixture()
    malformed = copy.deepcopy(evidence)
    report = next(
        row
        for row in malformed["judge_reports"]
        if row["adjudicator"]["lens_family"] == "explanatory"
    )
    report["adjudicator"]["lens_family"] = "ontological"
    for finding in report["candidate_findings"]:
        finding["deep_lens_analysis"]["lens_family"] = "ontological"
        finding["deep_lens_analysis"]["analysis_digest"] = canonical_digest(
            {
                key: value
                for key, value in finding["deep_lens_analysis"].items()
                if key != "analysis_digest"
            }
        )
    report["report_digest"] = canonical_digest(
        report, exclude_keys=("report_digest", "created_at")
    )
    _rehash_evidence(malformed)
    with pytest.raises(ConceptualAdjudicationError) as exc:
        validate_adjudication_evidence(malformed, **context)
    assert exc.value.reason_code == "adjudication_lens_floor_unmet"


def test_relabelled_duplicate_lens_analysis_is_rejected() -> None:
    evidence, context = _evidence_fixture()
    malformed = copy.deepcopy(evidence)
    ontological = next(
        row
        for row in malformed["judge_reports"]
        if row["adjudicator"]["lens_family"] == "ontological"
    )
    dialectical = next(
        row
        for row in malformed["judge_reports"]
        if row["adjudicator"]["lens_family"] == "dialectical"
    )
    for source, target in zip(
        ontological["candidate_findings"],
        dialectical["candidate_findings"],
        strict=True,
    ):
        copied = copy.deepcopy(source["deep_lens_analysis"])
        copied["lens_family"] = "dialectical"
        copied["analysis_digest"] = canonical_digest(
            {key: value for key, value in copied.items() if key != "analysis_digest"}
        )
        target["deep_lens_analysis"] = copied
    dialectical["report_digest"] = canonical_digest(
        dialectical, exclude_keys=("report_digest", "created_at")
    )
    _rehash_evidence(malformed)
    with pytest.raises(ConceptualAdjudicationError) as exc:
        validate_adjudication_evidence(malformed, **context)
    assert exc.value.reason_code == "adjudication_duplicate_lens_analysis"


def test_unblinding_must_bind_the_already_sealed_complete_panel() -> None:
    evidence, context = _evidence_fixture()
    malformed = copy.deepcopy(evidence)
    malformed["unblinding_receipt"]["panel_seal_digest"] = canonical_digest(
        "different-panel"
    )
    malformed["unblinding_receipt"]["receipt_digest"] = canonical_digest(
        {
            key: value
            for key, value in malformed["unblinding_receipt"].items()
            if key != "receipt_digest"
        }
    )
    _rehash_evidence(malformed)
    with pytest.raises(ConceptualAdjudicationError) as exc:
        validate_adjudication_evidence(malformed, **context)
    assert exc.value.reason_code == "adjudication_unblinding_order_invalid"


def test_forged_preference_set_fails_recomputation() -> None:
    evidence, context = _evidence_fixture()
    malformed = copy.deepcopy(evidence)
    malformed["preference_set"]["preferred_system_ids"] = ["candidate-a"]
    malformed["preference_set"]["preference_set_digest"] = canonical_digest(
        {
            key: value
            for key, value in malformed["preference_set"].items()
            if key != "preference_set_digest"
        }
    )
    _rehash_evidence(malformed)
    with pytest.raises(ConceptualAdjudicationError) as exc:
        validate_adjudication_evidence(malformed, **context)
    assert exc.value.reason_code == "adjudication_preference_set_mismatch"


def test_typed_unification_rejects_erasure_and_graph_digest_forgery() -> None:
    evidence, context = _evidence_fixture()
    erased_systems = copy.deepcopy(context["systems"])
    erased_systems[1]["unification_claims"]["preserved_differences"] = []
    with pytest.raises(ConceptualAdjudicationError) as exc:
        validate_adjudication_evidence(
            evidence, **{**context, "systems": erased_systems}
        )
    assert exc.value.reason_code == "adjudication_unification_erases_difference"

    forged_systems = copy.deepcopy(context["systems"])
    forged_systems[1]["unification_claims"]["explanatory_graph_transition"][
        "after_graph_digest"
    ] = canonical_digest("forged-graph")
    with pytest.raises(ConceptualAdjudicationError) as exc:
        validate_adjudication_evidence(
            evidence, **{**context, "systems": forged_systems}
        )
    assert exc.value.reason_code == "adjudication_digest_mismatch"


def test_semantic_signature_ignores_system_id_and_collection_order_only() -> None:
    original = _typed_system("candidate-original", deep=True)
    renamed = copy.deepcopy(original)
    renamed["system_id"] = "candidate-renamed"
    renamed["primitives"] = list(reversed(renamed["primitives"]))
    first = semantic_signature(original, identity_tokens=["candidate-original"])
    second = semantic_signature(renamed, identity_tokens=["candidate-renamed"])
    assert first["signature_digest"] == second["signature_digest"]

    changed = copy.deepcopy(renamed)
    changed["mechanism_or_principle"] += (
        " A new target dependency makes detector failure causally prior to descent failure."
    )
    third = semantic_signature(changed, identity_tokens=["candidate-renamed"])
    assert third["signature_digest"] != second["signature_digest"]


def test_semantic_signature_preserves_theoretical_relation_polarity() -> None:
    causes = _typed_system("candidate-causes", deep=True)
    causes["relations_operations_and_dynamics"] = [
        {
            "source": "scale witness",
            "relation": "causes",
            "target": "detector response",
        }
    ]
    prevents = copy.deepcopy(causes)
    prevents["system_id"] = "candidate-prevents"
    prevents["relations_operations_and_dynamics"][0]["relation"] = "prevents"
    assert semantic_signature(
        causes, identity_tokens=["candidate-causes"]
    )["signature_digest"] != semantic_signature(
        prevents, identity_tokens=["candidate-prevents"]
    )["signature_digest"]

    # Only an explicitly path-qualified process envelope may discard a
    # transport relation; an arbitrary nested theoretical relation may not.
    causes["process_metadata"] = {"relation": "scheduled_after"}
    prevents["process_metadata"] = {"relation": "scheduled_before"}
    assert semantic_signature(
        causes, identity_tokens=["candidate-causes"]
    )["signature_digest"] != semantic_signature(
        prevents, identity_tokens=["candidate-prevents"]
    )["signature_digest"]


@pytest.mark.parametrize(
    ("mutation", "reason_code"),
    [
        ("dangling_edge", "adjudication_unification_graph_dangling_edge"),
        ("duplicate_node", "adjudication_unification_graph_open"),
        ("unknown_relation", "adjudication_unification_relation_unknown"),
    ],
)
def test_typed_unification_graph_is_closed(
    mutation: str, reason_code: str
) -> None:
    evidence, context = _evidence_fixture()
    systems = copy.deepcopy(context["systems"])
    transition = systems[1]["unification_claims"]["explanatory_graph_transition"]
    if mutation == "dangling_edge":
        transition["after_graph"]["edges"][0]["target_node_id"] = "missing-node"
    elif mutation == "duplicate_node":
        duplicate = copy.deepcopy(transition["after_graph"]["nodes"][0])
        duplicate["label"] = "Duplicate construction burden identity"
        transition["after_graph"]["nodes"].append(duplicate)
    else:
        transition["after_graph"]["edges"][0]["relation_kind"] = "decoratively_unifies"
    with pytest.raises(ConceptualAdjudicationError) as exc:
        validate_adjudication_evidence(
            evidence, **{**context, "systems": systems}
        )
    assert exc.value.reason_code == reason_code


def test_fully_rehashed_unknown_nested_authority_field_is_rejected_by_schema() -> None:
    evidence, context = _evidence_fixture()
    malformed = copy.deepcopy(evidence)
    report = malformed["judge_reports"][0]
    authority = report["adjudicator"]["authority"]
    authority["callable"]["unregistered_semantic_override"] = "accept preferred alias"
    authority["authority_digest"] = canonical_digest(
        {key: value for key, value in authority.items() if key != "authority_digest"}
    )
    report["adjudicator"]["executable_digest"] = authority["authority_digest"]
    report["report_digest"] = canonical_digest(
        report, exclude_keys=("report_digest", "created_at")
    )
    _rehash_evidence(malformed)
    with pytest.raises(ConceptualAdjudicationError) as exc:
        validate_adjudication_evidence(malformed, **context)
    assert exc.value.reason_code == "adjudication_schema_invalid"
    assert "unregistered_semantic_override" in str(exc.value)
