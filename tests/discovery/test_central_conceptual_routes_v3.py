# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Constructive and adversarial tests for the canonical five-route protocol."""

from __future__ import annotations

import base64
import copy
import dataclasses
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import agentic.discovery.central_conceptual_routes_v3 as central_routes
from agentic.discovery.central_conceptual_routes_v3 import (
    ADJUDICATION_CRITERIA,
    ROUTE_ORDER,
    CentralConceptualRouteError,
    build_committed_route_input,
    commission_from_verified_commit,
    decode_central_conceptual_route_packet,
    execute_route_author_payload,
    load_central_route_registry,
    reopen_authoritative_central_conceptual_route_packet,
    run_central_conceptual_routes,
    validate_committed_route_input,
)
from agentic.discovery.blind_conceptual_judge_v3 import (
    execute_blind_conceptual_judgment,
)
from agentic.discovery.contracts import (
    Namespace,
    bytes_digest,
    canonical_digest,
    canonical_json,
    validate_schema_file,
)
from agentic.state.discovery_transaction import (
    CommitArtifact,
    DiscoveryTransactionStore,
)
from skills.common.formal_concept_transformations import seal_conceptual_core


TARGET_ID = "target.physics.central.routes.v3"
RUN_ID = "run.central.routes.v3"
BRANCH_ID = "root"
INPUT_PATH = "branches/root/central/route-input-v3.json"


def _primitive(identifier: str, prefix: str) -> dict:
    return {
        "primitive_id": identifier,
        "statement": f"Finite conceptual carrier {identifier}.",
        "member_ids": [f"{prefix}{index}" for index in range(4)],
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


def _observable(identifier: str, prefix: str) -> dict:
    return {
        "observable_id": f"observable.{identifier}",
        "carrier_primitive_id": identifier,
        "statement": f"Protected binary distinction on {identifier}.",
        "protected": True,
        "evaluations": [
            {
                "member_id": f"{prefix}{index}",
                "value": "red" if index % 2 == 0 else "blue",
            }
            for index in range(4)
        ],
    }


def _path(
    identifier: str,
    source: str,
    target: str,
    *,
    ambient: str = "A",
    derivation_rule: str = "declared_domain_constructor",
) -> dict:
    return {
        "inhabitant_id": identifier,
        "level": 1,
        "ambient_primitive_id": ambient,
        "source_boundary_id": source,
        "target_boundary_id": target,
        "derivation_rule": derivation_rule,
        "premise_inhabitant_ids": [],
        "evidence_refs": (
            [] if derivation_rule == "reflexivity" else [f"evidence.{identifier}"]
        ),
    }


def _cell(
    identifier: str,
    source_path: str,
    target_path: str,
    *,
    ambient: str,
) -> dict:
    return {
        "inhabitant_id": identifier,
        "level": 2,
        "ambient_primitive_id": ambient,
        "source_boundary_id": source_path,
        "target_boundary_id": target_path,
        "derivation_rule": "declared_coherence_constructor",
        "premise_inhabitant_ids": [source_path, target_path],
        "evidence_refs": [f"evidence.{identifier}"],
    }


def _core() -> dict:
    return seal_conceptual_core(
        {
            "schema_version": "2.0.0",
            "core_id": "core.central.routes.v3",
            "target_id": TARGET_ID,
            "obligation_id": "obligation.central.routes.v3",
            "physical_carrier": (
                "gauge-invariant observable content in one declared finite "
                "representation"
            ),
            "regime": (
                "finite conceptual calibration before continuum or theorem "
                "transport"
            ),
            "quantifiers": [
                {
                    "quantifier_id": "quantifier.every.member",
                    "statement": "For every member of each declared finite carrier.",
                },
                {
                    "quantifier_id": "quantifier.every.observable",
                    "statement": "For every explicitly protected observable.",
                },
            ],
            "primitives": [
                _primitive("A", "a"),
                _primitive("B", "b"),
                _primitive("C", "c"),
                _primitive("D", "d"),
            ],
            "relations": [
                _relation(
                    "map.f_ab",
                    "A",
                    "B",
                    [(f"a{index}", f"b{index}") for index in range(4)],
                ),
                _relation(
                    "map.g_bc",
                    "B",
                    "C",
                    [(f"b{index}", f"c{index}") for index in range(4)],
                ),
                _relation(
                    "map.f_ba_inverse",
                    "B",
                    "A",
                    [(f"b{index}", f"a{index}") for index in range(4)],
                ),
                _relation(
                    "map.h_ad",
                    "A",
                    "D",
                    [(f"a{index}", f"d{index}") for index in range(4)],
                ),
                _relation(
                    "map.k_dc",
                    "D",
                    "C",
                    [("d0", "c1"), ("d1", "c0"), ("d2", "c3"), ("d3", "c2")],
                ),
                _relation(
                    "map.id_a",
                    "A",
                    "A",
                    [(f"a{index}", f"a{index}") for index in range(4)],
                ),
                _relation(
                    "map.swap_a_forward",
                    "A",
                    "A",
                    [("a0", "a2"), ("a1", "a3"), ("a2", "a0"), ("a3", "a1")],
                ),
                _relation(
                    "map.swap_a_inverse",
                    "A",
                    "A",
                    [("a0", "a2"), ("a1", "a3"), ("a2", "a0"), ("a3", "a1")],
                ),
            ],
            "observables": [
                _observable("A", "a"),
                _observable("B", "b"),
                _observable("C", "c"),
                _observable("D", "d"),
            ],
            "inhabitants": [
                _path("path.a0-a2", "a0", "a2"),
                _path("path.a1-a3", "a1", "a3"),
                _path("path.a2-a0", "a2", "a0"),
                _path("path.a3-a1", "a3", "a1"),
                _path(
                    "path.id-a0.left",
                    "a0",
                    "a0",
                    derivation_rule="reflexivity",
                ),
                _path(
                    "path.id-a0.right",
                    "a0",
                    "a0",
                    derivation_rule="reflexivity",
                ),
                *[
                    _path(
                        f"path.id-a{index}",
                        f"a{index}",
                        f"a{index}",
                        derivation_rule="reflexivity",
                    )
                    for index in range(1, 4)
                ],
                *[
                    _path(
                        f"path.id-b{index}",
                        f"b{index}",
                        f"b{index}",
                        ambient="B",
                        derivation_rule="reflexivity",
                    )
                    for index in range(4)
                ],
                _cell(
                    "cell.id-a0-left-right",
                    "path.id-a0.left",
                    "path.id-a0.right",
                    ambient="A",
                ),
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


def _seal(raw: dict, field: str) -> dict:
    result = copy.deepcopy(raw)
    result[field] = canonical_digest(result)
    return result


def _decision_rule(core: dict) -> dict:
    predicate = _seal(
        {
            "predicate_id": "finite-carrier-predicate.central.v3",
            "predicate_kind": (
                "finite_carrier_nontriviality_conservativity_and_obstruction_predicate"
            ),
            "before_core_digest": core["content_digest"],
            "target_burden_id": "burden.original",
            "protected_observable_digests": sorted(
                canonical_digest(row)
                for row in core["observables"]
                if row["protected"]
            ),
            "require_exact_carrier_regime_quantifiers": True,
            "require_changed_core": True,
            "require_changed_burden": True,
            "require_finite_relation_witness": True,
            "nontriviality_contract": copy.deepcopy(
                central_routes._NONTRIVIALITY_CONTRACT
            ),
            "counterexample_policy": (
                "any_protected_observable_or_member_value_change_fails"
            ),
        },
        "predicate_digest",
    )
    eligible_action = central_routes._canonical_eligible_action(
        {"physical_carrier": core["physical_carrier"]}, predicate
    )
    return _seal(
        {
            "rule_id": "physics-decision-rule.central.v3",
            "target_id": core["target_id"],
            "obligation_id": core["obligation_id"],
            "physical_carrier": core["physical_carrier"],
            "regime": core["regime"],
            "quantifiers": [row["statement"] for row in core["quantifiers"]],
            "protected_successes": [
                "Gauge-invariant carrier distinctions stay explicit.",
                "Declared finite observables remain protected.",
            ],
            "incumbent_decision": {
                "decision_id": "decision.incumbent",
                "action": "Continue the incumbent representation audit.",
                "target_burden_id": "burden.original",
            },
            "eligible_decision": {
                "decision_id": "decision.candidate",
                "action": eligible_action,
                "target_burden_id": "burden.original",
            },
            "explanatory_dependency": (
                "Localize the dependency between representation and preserved "
                "observable content."
            ),
            "changed_burden_template": (
                "Construct the carrier-specific relation while preserving every "
                "protected observable."
            ),
            "correction": (
                "Revert if a protected distinction collapses or an inhabitant "
                "is freely added."
            ),
            "falsifier": (
                "Exhibit one declared finite carrier member where the transported "
                "protected value changes."
            ),
            "physics_next_action": (
                "Derive the corresponding carrier-level counterexample before "
                "any continuum claim."
            ),
            "untouched_physics_gates": [
                "Continuum construction remains open.",
                "The spectral gap remains open.",
            ],
            "carrier_predicate": predicate,
            "entailment_table": [
                {
                    "outcome": "predicate_failed",
                    "predicate_value": False,
                    "decision_id": "decision.incumbent",
                    "action_kind": "retain_incumbent",
                    "target_burden_id": "burden.original",
                },
                {
                    "outcome": "predicate_satisfied",
                    "predicate_value": True,
                    "decision_id": "decision.candidate",
                    "action_kind": "inspect_witnessed_finite_carrier_delta",
                    "target_burden_id": "burden.original",
                },
            ],
        },
        "decision_rule_digest",
    )


def _adjudication_rule() -> dict:
    judge_rule = _seal(
        {
            "criteria": list(ADJUDICATION_CRITERIA),
            "evidence_statuses": ["failed", "partial", "satisfied"],
            "selection_policy": "set_valued_pareto_nondomination",
            "aggregation_policy": "no_scalar_aggregation",
            "ties_allowed": True,
            "candidate_order_policy": (
                "canonical_opaque_nonce_order_order_ignored"
            ),
        },
        "rule_digest",
    )
    return _seal(
        {
            "rule_id": "blind-pareto-rule.central.v3",
            "judge_rule": judge_rule,
            "route_labels_visible": False,
            "formal_vocabulary_bonus": False,
            "capable_nonformal_eligible": True,
        },
        "content_digest",
    )


def _committed_input() -> dict:
    core = _core()
    return build_committed_route_input(
        target_id=TARGET_ID,
        run_id=RUN_ID,
        source_cycle_id="cycle.central.routes.v3",
        conceptual_core=core,
        literature_projection={
            "snapshot_id": "literature-snapshot.current.central.v3",
            "snapshot_digest": canonical_digest("current literature snapshot"),
            "production_projection_digest": canonical_digest(
                "current literature production projection"
            ),
            "consume_before": "2099-07-22T00:00:00+00:00",
            "present_use_evaluated_at": "2026-07-21T20:00:00+00:00",
            "present_use_reason": "Current bounded snapshot at plan-free precommit.",
        },
        conceptual_ancestry_digest=canonical_digest("conceptual ancestry v3"),
        physics_decision_rule=_decision_rule(core),
        adjudication_rule=_adjudication_rule(),
    )


def _store_with_input(
    root: Path,
    *,
    canonical_bytes: bool = True,
) -> tuple[DiscoveryTransactionStore, object, str]:
    payload = _committed_input()
    data = (
        canonical_json(payload) + b"\n"
        if canonical_bytes
        else json.dumps(payload, indent=2).encode("utf-8") + b"\n"
    )
    store = DiscoveryTransactionStore(root, target_id=TARGET_ID, run_id=RUN_ID)
    store.commit(
        expected_generation=0,
        state={
            "schema_version": "1.0.0",
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "generation": 1,
        },
        artifacts=[
            CommitArtifact(
                INPUT_PATH,
                data,
                Namespace(TARGET_ID, RUN_ID, BRANCH_ID, 0),
            )
        ],
        idempotency_key="central-route-input-v3",
        request_digest=canonical_digest(payload),
    )
    return store, store.read_verified_commit(), INPUT_PATH


def _direct_commission() -> tuple[dict, dict]:
    payload = _committed_input()
    data = canonical_json(payload) + b"\n"
    commission = {
        "committed_input_base64": base64.b64encode(data).decode("ascii"),
        "committed_input_sha256": bytes_digest(data),
        "committed_input_byte_length": len(data),
        "committed_input_content_digest": payload["content_digest"],
    }
    commission["commission_digest"] = canonical_digest(commission)
    return commission, payload


def _execute_direct(route_id: str) -> dict:
    commission, _ = _direct_commission()
    request = {
        "schema_version": "3.0.0",
        "route_id": route_id,
        "commission": commission,
    }
    request["payload_digest"] = canonical_digest(request)
    return execute_route_author_payload(request)


def test_schemas_and_five_route_registry_are_exact() -> None:
    for name in (
        "central_conceptual_route_input_v3.schema.json",
        "central_conceptual_route_packet_v3.schema.json",
    ):
        assert validate_schema_file(name)["$id"].endswith(name)
    binding, raw = load_central_route_registry()
    assert [row["route_id"] for row in binding["routes"]] == list(ROUTE_ORDER)
    assert len({row["producer_id"] for row in binding["routes"]}) == 5
    assert binding["execution_contract"]["caller_plans_forbidden"] is True
    assert binding["judge"]["route_labels_visible"] is False
    assert binding["registry_file_sha256"] == bytes_digest(raw)


def test_committed_input_is_plan_free_current_and_ancestry_bound() -> None:
    payload = _committed_input()
    assert validate_committed_route_input(payload) == payload
    assert payload["conceptual_ancestry_digest"] == canonical_digest(
        "conceptual ancestry v3"
    )
    assert not {"route_plans", "transformations", "scores", "winner"}.intersection(
        payload
    )
    forged = copy.deepcopy(payload)
    forged["transformations"] = []
    with pytest.raises(CentralConceptualRouteError, match="schema failure|keys differ"):
        validate_committed_route_input(forged)


def test_all_five_authors_derive_postcommit_plans_and_exact_ordered_sequences() -> None:
    outputs = {route_id: _execute_direct(route_id) for route_id in ROUTE_ORDER}
    assert all(output["route_status"] == "completed" for output in outputs.values())
    assert all(output["caller_plan_used"] is False for output in outputs.values())
    assert all(
        output["physics_handback"]["handback_status"]
        == "admissible_for_blind_comparison"
        for output in outputs.values()
    )
    assert [
        row["skill_id"]
        for row in outputs["categorical"]["evidence"]["skill_reuse"]
    ] == ["categorical-concept-forger"]
    assert [
        row["skill_id"]
        for row in outputs["hott"]["evidence"]["skill_reuse"]
    ] == ["hott-equivalence-coherence-forger"]
    assert outputs["categorical"]["evidence"]["plan"]["relation_hypothesis"][
        "relation_kind"
    ] == "mediating_factorization"
    assert outputs["hott"]["evidence"]["plan"]["relation_hypothesis"][
        "relation_kind"
    ] == "equivalence_coherence"
    forward = outputs["category_then_hott"]["evidence"]["sequence"]
    reverse = outputs["hott_then_category"]["evidence"]["sequence"]
    assert [
        forward["first_step"]["plan"]["relation_hypothesis"][
            "relation_kind"
        ],
        forward["second_step"]["plan"]["relation_hypothesis"][
            "relation_kind"
        ],
    ] == ["mediating_factorization", "equivalence_coherence"]
    assert [
        reverse["first_step"]["plan"]["relation_hypothesis"][
            "relation_kind"
        ],
        reverse["second_step"]["plan"]["relation_hypothesis"][
            "relation_kind"
        ],
    ] == ["equivalence_coherence", "mediating_factorization"]
    assert forward["order"] != reverse["order"]
    assert "critical_pairs" not in forward
    assert "critical_pairs" not in reverse
    assert forward["conditioned_path"]["reverse_order_status"] == (
        "not_constructed_without_reverse_conditioned_authorship"
    )
    assert reverse["conditioned_path"]["reverse_order_status"] == (
        "not_constructed_without_reverse_conditioned_authorship"
    )
    assert forward["second_step"]["plan_authored_from_core_digest"] == (
        forward["first_step"]["delta"]["after_core"]["content_digest"]
    )
    assert reverse["second_step"]["plan_authored_from_core_digest"] == (
        reverse["first_step"]["delta"]["after_core"]["content_digest"]
    )
    forward_evidence = outputs["category_then_hott"]["evidence"]
    reverse_evidence = outputs["hott_then_category"]["evidence"]
    assert forward_evidence["second_plan_authored_from_core_digest"] == (
        forward_evidence["conditioned_delta"]["first_delta"]["after_core"][
            "content_digest"
        ]
    )
    assert reverse_evidence["second_plan_authored_from_core_digest"] == (
        reverse_evidence["conditioned_delta"]["first_delta"]["after_core"][
            "content_digest"
        ]
    )
    assert forward_evidence["second_plan_authored_from_core_digest"] != _core()[
        "content_digest"
    ]
    assert all(
        row["artifact_replay"]["status"] == "valid"
        for route_id in ROUTE_ORDER[:-1]
        for row in outputs[route_id]["evidence"]["skill_reuse"]
    )
    assert outputs["hott"]["records"][0]["hott_check"][
        "round_trip_holds"
    ] is True
    hott_scope = outputs["hott"]["records"][0]["hott_check"]["finite_scope"]
    assert hott_scope["scope_kind"] == (
        "finite_distinct_carrier_equivalence_with_coherence"
    )
    assert hott_scope["source_carrier_binding"]["primitive_id"] == "A"
    assert hott_scope["target_carrier_binding"]["primitive_id"] == "B"
    assert hott_scope["source_carrier_binding"]["primitive_digest"] != (
        hott_scope["target_carrier_binding"]["primitive_digest"]
    )
    assert hott_scope["inverse_scope"] == (
        "one_explicit_forward_and_inverse_relation_pair"
    )
    assert hott_scope["round_trip_scope"] == (
        "both_registered_carriers_replayed_pointwise"
    )
    assert hott_scope["transport_scope"] == (
        "paired_protected_observable_evaluations_on_both_carriers_only"
    )
    assert hott_scope["naturality_scope"] == (
        "forward_inverse_protected_predicate_squares_pointwise_only"
    )
    assert hott_scope["coherence_scope"] == (
        "listed_declared_level_two_cells_between_selected_parallel_"
        "roundtrip_paths_only"
    )
    assert hott_scope["coherence_cell_ids"] == ["cell.id-a0-left-right"]
    assert all(
        row["identity_replayed"]
        for row in (
            hott_scope["source_round_trip_rows"]
            + hott_scope["target_round_trip_rows"]
        )
    )
    assert all(
        row["forward_value_preserved"] and row["inverse_value_preserved"]
        for row in hott_scope["transport_rows"]
    )
    assert hott_scope["judgmental_equality_authorized"] is False
    assert hott_scope["univalence_authorized"] is False
    category_case = outputs["categorical"]["evidence"]["skill_reuse"][0][
        "case"
    ]["task_semantics"]["task_relations"][0]
    hott_case = outputs["hott"]["evidence"]["skill_reuse"][0]["case"][
        "task_semantics"
    ]["task_relations"][0]
    assert category_case["source_anchor"].startswith("A:")
    assert category_case["target_anchor"].startswith("B:")
    assert hott_case["source_anchor"].startswith("A:")
    assert hott_case["target_anchor"].startswith("B:")
    assert all(
        row["case_binding_valid"] and row["delta_binding_valid"]
        for route_id in ROUTE_ORDER[:-1]
        for row in outputs[route_id]["physics_handback"]["content_projection"][
            "decision_rule_evidence"
        ]["skill_replays"]
    )
    assert all(
        all(
            certificate["exact_scope_replayed"]
            and not certificate["identity_only"]
            and not certificate["mere_relabeling"]
            and not certificate["physically_inert_completion"]
            for certificate in output["physics_handback"]["content_projection"][
                "decision_rule_evidence"
            ]["predicate_evaluation"]["nontriviality_evaluation"][
                "stage_certificates"
            ]
        )
        for output in outputs.values()
    )
    comparison = central_routes._conditioned_order_comparison(outputs)
    assert comparison["independently_conditioned"] is True
    assert comparison["asymmetric_order_replayed"] is True
    assert comparison["isomorphism_aware"] is True
    assert comparison["isomorphism_scope"] == (
        "bounded_exact_internal_relabelling_via_formal_concept_sequence_algebra"
    )
    assert comparison["productive_noncommutation_retained"] == (
        comparison["isomorphism_comparison"]["comparison_status"]
        == "not_isomorphic"
    )
    assert comparison["comparison_kind"] in {
        "strictly_equal",
        "isomorphic_commuting",
        "productive_noncommutation",
        "ceiling_unavailable",
    }
    substituted = copy.deepcopy(outputs)
    substituted["hott_then_category"] = copy.deepcopy(
        outputs["category_then_hott"]
    )
    rejected = central_routes._conditioned_order_comparison(substituted)
    assert rejected["independently_conditioned"] is False
    assert rejected["asymmetric_order_replayed"] is False
    assert rejected["productive_noncommutation_retained"] is False
    rule = _committed_input()["physics_decision_rule"]
    projections = [
        outputs[route_id]["physics_handback"]["content_projection"]
        for route_id in ROUTE_ORDER
    ]
    assert len(
        {projection["candidate_physics_basis_digest"] for projection in projections}
    ) == len(ROUTE_ORDER)
    assert all(
        projection["physical_interpretation"]
        == projection["explanatory_dependency"]
        and projection["physical_interpretation"]
        != rule["explanatory_dependency"]
        and projection["correction"] != rule["correction"]
        and projection["falsifier"] != rule["falsifier"]
        and projection["physics_next_action"] != rule["physics_next_action"]
        and projection["changed_burdens"]
        and projection["candidate_physics_basis_digest"].startswith("sha256:")
        for projection in projections
    )


def test_positive_mediator_and_functor_replay_while_trivial_cases_fail() -> None:
    core = _core()
    identity_only = seal_conceptual_core(
        {
            **{
                key: copy.deepcopy(value)
                for key, value in core.items()
                if key != "content_digest"
            },
            "relations": [
                row
                for row in core["relations"]
                if row["relation_id"] == "map.id_a"
            ],
        }
    )
    assert (
        central_routes._derive_hott_plan(
            identity_only, _decision_rule(identity_only)
        )
        is None
    )
    assert (
        central_routes._derive_category_plan(
            identity_only, _decision_rule(identity_only)
        )
        is None
    )

    relabel_only_raw = {
        key: copy.deepcopy(value)
        for key, value in core.items()
        if key != "content_digest"
    }
    relabel_only_raw["relations"] = [
        row
        for row in core["relations"]
        if row["relation_id"] == "map.f_ab"
    ]
    for observable in relabel_only_raw["observables"]:
        if observable["carrier_primitive_id"] == "B":
            for evaluation in observable["evaluations"]:
                evaluation["value"] = "indistinguishable"
    relabel_only = seal_conceptual_core(relabel_only_raw)
    assert (
        central_routes._derive_category_plan(
            relabel_only, _decision_rule(relabel_only)
        )
        is None
    )

    one_map_raw = {
        key: copy.deepcopy(value)
        for key, value in core.items()
        if key != "content_digest"
    }
    one_map_raw["relations"] = [
        row for row in core["relations"] if row["relation_id"] == "map.f_ab"
    ]
    one_map = seal_conceptual_core(one_map_raw)
    rule = _decision_rule(one_map)
    mediator_plan = central_routes._derive_category_plan(one_map, rule)
    assert mediator_plan is not None
    assert mediator_plan["relation_hypothesis"]["relation_kind"] == (
        "mediating_factorization"
    )
    mediator_scope = mediator_plan["finite_scope"]
    assert mediator_scope["mediator_distinct_from_endpoints"] is True
    assert mediator_scope[
        "mediator_members_disjoint_from_registered_carriers"
    ] is True
    assert mediator_scope["copied_interface_authorized"] is False
    assert all(
        row["factored_target_member_id"] == row["direct_target_member_id"]
        for row in mediator_scope["pointwise_factorization_rows"]
    )
    mediator_delta, _ = central_routes._apply_postcommit_plan(
        one_map, mediator_plan
    )
    mediator_certificate = central_routes._stage_nontriviality_certificate(
        one_map, mediator_plan, mediator_delta, stage="single"
    )
    assert mediator_certificate["exact_scope_replayed"] is True
    assert mediator_certificate["trivial_copied_mediator"] is False
    assert mediator_certificate["physically_inert_completion"] is False

    functor_plan = central_routes._derive_category_plan(
        mediator_delta["after_core"], rule
    )
    assert functor_plan is not None
    assert functor_plan["relation_hypothesis"]["relation_kind"] == (
        "functorial_transfer"
    )
    functor_scope = functor_plan["finite_scope"]
    assert functor_scope["transferred_carriers_distinct_and_disjoint"] is True
    assert all(row["pointwise_equal"] for row in functor_scope["naturality_rows"])
    functor_delta, _ = central_routes._apply_postcommit_plan(
        mediator_delta["after_core"], functor_plan
    )
    functor_certificate = central_routes._stage_nontriviality_certificate(
        mediator_delta["after_core"],
        functor_plan,
        functor_delta,
        stage="second",
    )
    assert functor_certificate["exact_scope_replayed"] is True
    assert functor_certificate["physically_inert_completion"] is False


def test_hott_scope_substitution_cannot_authorize_a_handback() -> None:
    output = _execute_direct("hott")
    committed = _committed_input()
    plan = copy.deepcopy(output["evidence"]["plan"])
    plan["finite_scope"]["inverse_relation_id"] = "map.id_a"
    skill_evidence = [
        central_routes._forge_skill_evidence(
            core=committed["conceptual_core"],
            rule=committed["physics_decision_rule"],
            plan=plan,
            route_id="hott",
            stage="single",
        )
    ]
    handback = central_routes._shared_handback(
        route_id="hott",
        payload=committed,
        status="completed",
        evidence={"adversary": "finite-scope-substitution"},
        changed_burdens=[
            output["evidence"]["delta"]["semantic_delta"]["changed_burden"]
        ],
        changed_resource=plan["relation_hypothesis"]["statement"],
        unification_links=["adversarial:hott-scope"],
        quarantine_reasons=[],
        candidate_delta=output["evidence"]["delta"],
        skill_evidence=skill_evidence,
    )
    rule_evidence = handback["content_projection"]["decision_rule_evidence"]
    assert rule_evidence["checks"]["registered_semantic_producer_replayed"] is True
    assert rule_evidence["checks"]["exact_finite_scope_replayed"] is False
    assert rule_evidence["predicate_satisfied"] is False
    assert handback["handback_status"] == "quarantined_or_unavailable"


def test_completion_without_exact_rule_witness_cannot_change_research_action() -> None:
    committed = _committed_input()
    handback = central_routes._shared_handback(
        route_id="capable_nonformal",
        payload=committed,
        status="completed",
        evidence={"self_report": "completed"},
        changed_burdens=["A caller claims one burden changed."],
        changed_resource="A caller claims one conceptual resource changed.",
        unification_links=["caller:self-report"],
        quarantine_reasons=[],
        candidate_delta=None,
        skill_evidence=[],
    )
    assert handback["handback_status"] == "quarantined_or_unavailable"
    projection = handback["content_projection"]
    assert projection["decision_rule_evidence"]["predicate_satisfied"] is False
    assert projection["decision_replay"]["research_action_changed"] is False
    assert projection["decision_replay"]["candidate"] == projection[
        "decision_replay"
    ]["baseline"]


def test_arbitrary_policy_text_cannot_become_the_entailed_physics_action() -> None:
    core = _core()
    rule = _decision_rule(core)
    rule["eligible_decision"]["action"] = (
        "Archive every unrelated manuscript without inspecting the conceptual witness."
    )
    rule["decision_rule_digest"] = canonical_digest(
        {key: value for key, value in rule.items() if key != "decision_rule_digest"}
    )
    with pytest.raises(CentralConceptualRouteError, match="not derived"):
        central_routes.validate_physics_decision_rule(rule)


def test_foreign_forge_artifact_cannot_authorize_an_unrelated_candidate_delta() -> None:
    categorical = _execute_direct("categorical")
    hott = _execute_direct("hott")
    committed = _committed_input()
    handback = central_routes._shared_handback(
        route_id="categorical",
        payload=committed,
        status="completed",
        evidence=categorical["evidence"],
        changed_burdens=[
            categorical["evidence"]["delta"]["semantic_delta"]["changed_burden"]
        ],
        changed_resource=categorical["evidence"]["plan"][
            "relation_hypothesis"
        ]["statement"],
        unification_links=["adversarial:foreign-artifact"],
        quarantine_reasons=[],
        candidate_delta=categorical["evidence"]["delta"],
        skill_evidence=hott["evidence"]["skill_reuse"],
    )
    rule_evidence = handback["content_projection"]["decision_rule_evidence"]
    assert rule_evidence["predicate_satisfied"] is False
    assert rule_evidence["checks"]["registered_semantic_producer_replayed"] is False
    assert handback["content_projection"]["decision_replay"][
        "research_action_changed"
    ] is False


def test_protected_member_counterexample_blocks_the_finite_entailment() -> None:
    output = _execute_direct("capable_nonformal")
    committed = _committed_input()
    delta = copy.deepcopy(output["evidence"]["typed_conceptual_delta"])
    after = copy.deepcopy(delta["after_core"])
    after["observables"][0]["evaluations"][0]["value"] = "tampered-value"
    after = seal_conceptual_core(
        {key: value for key, value in after.items() if key != "content_digest"}
    )
    delta["after_core"] = after
    delta["content_digest"] = canonical_digest(
        {key: value for key, value in delta.items() if key != "content_digest"}
    )
    handback = central_routes._shared_handback(
        route_id="capable_nonformal",
        payload=committed,
        status="completed",
        evidence={"adversary": "protected-member-counterexample"},
        changed_burdens=delta["changed_burdens"],
        changed_resource=delta["changed_conceptual_resource"],
        unification_links=["adversarial:protected-member"],
        quarantine_reasons=[],
        candidate_delta=delta,
        skill_evidence=[],
    )
    rule_evidence = handback["content_projection"]["decision_rule_evidence"]
    assert rule_evidence["checks"]["carrier_counterexample_absent"] is False
    assert rule_evidence["predicate_satisfied"] is False
    assert handback["content_projection"]["decision_replay"][
        "research_action_changed"
    ] is False


def test_content_only_judge_allows_nonformal_to_win_or_cowin() -> None:
    category = _execute_direct("categorical")["physics_handback"][
        "content_projection"
    ]
    nonformal = _execute_direct("capable_nonformal")["physics_handback"][
        "content_projection"
    ]
    # A substantive formal candidate and the independently typed nonformal
    # candidate receive the same evidence-ledger opportunity.  No route name,
    # notation count, list length, or text enters the judge request.
    candidates = [
        central_routes._blind_candidate("a" * 64, category),
        central_routes._blind_candidate("b" * 64, nonformal),
    ]
    request = {
        "schema_version": "3.0.0",
        "commission_digest": canonical_digest("blind commission"),
        "adjudication_rule": _adjudication_rule()["judge_rule"],
        "opaque_candidates": candidates,
    }
    request["request_digest"] = canonical_digest(request)
    judgment = execute_blind_conceptual_judgment(request)
    assert judgment["preference_set"] == ["a" * 64, "b" * 64]
    assert all(row["pareto_nondominated"] for row in judgment["records"])
    assert judgment["judge_authority"]["route_labels_observed"] is False
    nonformal_checks = _execute_direct("capable_nonformal")[
        "physics_handback"
    ]["content_projection"]["decision_rule_evidence"]["checks"]
    assert nonformal_checks["nonidentity_or_contrastive_effect_replayed"] is True
    assert nonformal_checks["carrier_semantics_or_countermodel_replayed"] is True
    assert set(request) == {
        "schema_version",
        "commission_digest",
        "adjudication_rule",
        "opaque_candidates",
        "request_digest",
    }
    assert all(
        set(candidate)
        == {
            "opaque_candidate_nonce",
            "criterion_evidence_ledger",
            "evidence_ledger_digest",
        }
        for candidate in candidates
    )


def test_commission_requires_exact_current_store_reopened_commit(tmp_path: Path) -> None:
    store, commit, path = _store_with_input(tmp_path / "store")
    commission = commission_from_verified_commit(
        store=store,
        verified_commit=commit,
        committed_input_path=path,
    )
    assert commission["verified_commit"]["commit_id"] == commit.commit_id
    detached = dataclasses.replace(commit, commit_id="detached-commit")
    with pytest.raises(CentralConceptualRouteError, match="differs"):
        commission_from_verified_commit(
            store=store,
            verified_commit=detached,
            committed_input_path=path,
        )
    store.commit(
        expected_generation=1,
        state={
            "schema_version": "1.0.0",
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "generation": 2,
        },
        artifacts=[],
        idempotency_key="advance-head",
        request_digest=canonical_digest("advance-head"),
    )
    with pytest.raises(CentralConceptualRouteError, match="not the current"):
        commission_from_verified_commit(
            store=store,
            verified_commit=commit,
            committed_input_path=path,
        )


def test_commission_rejects_semantically_equal_noncanonical_artifact_bytes(
    tmp_path: Path,
) -> None:
    store, commit, path = _store_with_input(
        tmp_path / "store", canonical_bytes=False
    )
    with pytest.raises(CentralConceptualRouteError, match="exact canonical"):
        commission_from_verified_commit(
            store=store,
            verified_commit=commit,
            committed_input_path=path,
        )


def test_full_process_wave_overlaps_and_blindly_returns_a_set(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store, commit, path = _store_with_input(tmp_path / "store")
    observed_boundaries: list[str] = []
    original_recheck = central_routes._revalidate_live_commission

    def record_recheck(**kwargs: object) -> dict:
        observed_boundaries.append(str(kwargs["boundary"]))
        return original_recheck(**kwargs)

    monkeypatch.setattr(
        central_routes, "_revalidate_live_commission", record_recheck
    )
    packet = run_central_conceptual_routes(
        store=store,
        verified_commit=commit,
        committed_input_path=path,
        output_root=tmp_path / "runs",
    )
    bundle = tmp_path / "runs" / packet["commission_id"]
    assert decode_central_conceptual_route_packet(packet) == packet
    assert (
        reopen_authoritative_central_conceptual_route_packet(
            packet, bundle_root=bundle, store=store
        )
        == packet
    )
    assert observed_boundaries[:6] == [
        "commission",
        "after_bundle_lock",
        "before_author_launch",
        "before_judge_launch",
        "before_packet_publication",
        "before_cache_return",
    ]
    barrier = packet["terminal_barrier"]
    assert barrier["all_routes_terminal"] is True
    assert barrier["all_routes_started_as_distinct_processes"] is True
    assert barrier["parallel_process_overlap_observed"] is True
    assert packet["matched_comparison_eligible"] is True
    assert len(packet["route_terminals"]) == 5
    assert len({row["process_id"] for row in packet["route_terminals"]}) == 5
    assert len(packet["blind_identity_rebindings"]) == packet[
        "blind_candidate_count"
    ]
    assert packet["selected_route_set"]
    assert packet["blind_judge_request"] is not None
    assert packet["blind_binding_record_reference"] is not None
    assert packet["blind_binding_record_digest"] is not None
    assert packet["blind_judge_receipt_summary"]["role"] == "judge"
    assert [
        row["opaque_candidate_nonce"]
        for row in packet["blind_judge_request"]["opaque_candidates"]
    ] == sorted(
        row["opaque_candidate_nonce"]
        for row in packet["blind_judge_request"]["opaque_candidates"]
    )
    assert all(
        len(row["opaque_candidate_nonce"]) == 64
        for row in packet["blind_identity_rebindings"]
    )
    assert packet["blind_judgment"]["judge_authority"][
        "route_labels_observed"
    ] is False
    assert packet["conditioned_order_comparison"][
        "productive_noncommutation_retained"
    ] is True
    assert packet["conditioned_order_comparison"][
        "comparative_value_authorized"
    ] is False
    assert packet["blind_nonce_policy"] == {
        "generation": "system_csprng_256_bit_route_independent",
        "presentation": "lexicographic_opaque_nonce",
        "request_protocol_route_labels_absent": True,
        "parent_process_mapping_retained": True,
        "host_mapping_access_denied": False,
        "bindings_publication_stage": "post_judgment_only",
        "randomness_authorized": False,
        "counterbalancing_authorized": False,
    }
    assert all(
        output["committed_input_sha256"]
        == packet["route_outputs"][0]["committed_input_sha256"]
        for output in packet["route_outputs"]
    )

    forged = copy.deepcopy(packet)
    forged["blind_identity_rebindings"][0]["route_id"] = "capable_nonformal"
    forged["content_digest"] = canonical_digest(
        {key: value for key, value in forged.items() if key != "content_digest"}
    )
    with pytest.raises(CentralConceptualRouteError, match="rebinds"):
        decode_central_conceptual_route_packet(forged)

    substituted = copy.deepcopy(packet)
    substituted["commission_artifact_reference"][
        "relative_path"
    ] = "substituted-commission.json"
    substituted["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in substituted.items()
            if key != "content_digest"
        }
    )
    assert decode_central_conceptual_route_packet(substituted) == substituted
    with pytest.raises(CentralConceptualRouteError, match="unavailable"):
        reopen_authoritative_central_conceptual_route_packet(
            substituted, bundle_root=bundle, store=store
        )

    replayed = run_central_conceptual_routes(
        store=store,
        verified_commit=commit,
        committed_input_path=path,
        output_root=tmp_path / "runs",
    )
    assert replayed == packet

    store.commit(
        expected_generation=1,
        state={
            "schema_version": "1.0.0",
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "generation": 2,
        },
        artifacts=[],
        idempotency_key="advance-after-cache-fill",
        request_digest=canonical_digest("advance-after-cache-fill"),
    )
    assert decode_central_conceptual_route_packet(packet) == packet
    with pytest.raises(CentralConceptualRouteError, match="head advanced"):
        reopen_authoritative_central_conceptual_route_packet(
            packet, bundle_root=bundle, store=store
        )
    with pytest.raises(CentralConceptualRouteError, match="not the current"):
        run_central_conceptual_routes(
            store=store,
            verified_commit=commit,
            committed_input_path=path,
            output_root=tmp_path / "runs",
        )


def test_literature_deadline_is_rechecked_after_bundle_lock(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store, commit, path = _store_with_input(tmp_path / "store")
    deadline = datetime(2099, 7, 22, tzinfo=timezone.utc)
    instants = iter((deadline - timedelta(microseconds=1), deadline))
    monkeypatch.setattr(central_routes, "_system_utc_now", lambda: next(instants))
    with pytest.raises(
        CentralConceptualRouteError,
        match="after_bundle_lock: committed literature consume-before deadline expired",
    ):
        run_central_conceptual_routes(
            store=store,
            verified_commit=commit,
            committed_input_path=path,
            output_root=tmp_path / "expired-runs",
        )


def test_failed_author_remains_terminal_and_blocks_matched_adjudication(
    tmp_path: Path,
) -> None:
    store, commit, path = _store_with_input(tmp_path / "store")
    faults = {route_id: None for route_id in ROUTE_ORDER}
    faults["hott"] = "exit_nonzero"
    packet = run_central_conceptual_routes(
        store=store,
        verified_commit=commit,
        committed_input_path=path,
        output_root=tmp_path / "faulted-runs",
        route_fault_modes=faults,
    )
    assert decode_central_conceptual_route_packet(packet) == packet
    assert (
        reopen_authoritative_central_conceptual_route_packet(
            packet,
            bundle_root=tmp_path / "faulted-runs" / packet["commission_id"],
            store=store,
        )
        == packet
    )
    assert packet["route_terminals"][1]["terminal_status"] == "failed"
    assert packet["route_outputs"][1] is None
    assert packet["matched_comparison_eligible"] is False
    assert packet["blind_judgment"] is None
    assert packet["blind_judge_request"] is None
    assert packet["blind_binding_record_reference"] is None
    assert packet["blind_judge_receipt_summary"] is None
    assert packet["blind_identity_rebindings"] == []
    assert packet["selected_route_set"] == []


def test_blind_freeze_and_judge_receipt_survive_injected_parent_crashes(
    tmp_path: Path,
) -> None:
    store, commit, path = _store_with_input(tmp_path / "store")
    run_root = tmp_path / "crash-runs"
    with pytest.raises(CentralConceptualRouteError, match="after blind freeze"):
        run_central_conceptual_routes(
            store=store,
            verified_commit=commit,
            committed_input_path=path,
            output_root=run_root,
            persistence_failpoint="after_blind_freeze_before_judge",
        )
    bundles = [candidate for candidate in run_root.iterdir() if candidate.is_dir()]
    assert len(bundles) == 1
    freeze_path = bundles[0] / "blind-binding-request-freeze-v3.json"
    freeze_before = freeze_path.read_bytes()

    with pytest.raises(CentralConceptualRouteError, match="after judge receipt"):
        run_central_conceptual_routes(
            store=store,
            verified_commit=commit,
            committed_input_path=path,
            output_root=run_root,
            persistence_failpoint="after_judge_receipt_before_packet",
        )
    assert freeze_path.read_bytes() == freeze_before

    packet = run_central_conceptual_routes(
        store=store,
        verified_commit=commit,
        committed_input_path=path,
        output_root=run_root,
    )
    freeze = json.loads(freeze_before)
    assert packet["blind_judge_request"] == freeze["request"]
    assert packet["blind_identity_rebindings"] == freeze["bindings"]


def test_bundle_lock_serializes_racers_and_cache_corruption_fails_closed(
    tmp_path: Path,
) -> None:
    store, commit, path = _store_with_input(tmp_path / "store")
    run_root = tmp_path / "race-runs"

    def run_once() -> dict:
        return run_central_conceptual_routes(
            store=store,
            verified_commit=commit,
            committed_input_path=path,
            output_root=run_root,
        )

    with ThreadPoolExecutor(max_workers=2) as pool:
        first_future = pool.submit(run_once)
        second_future = pool.submit(run_once)
        first = first_future.result()
        second = second_future.result()
    assert first == second

    packet_path = (
        run_root
        / first["commission_id"]
        / "central-conceptual-route-packet-v3.json"
    )
    forged = copy.deepcopy(first)
    forged["selected_route_set"] = []
    forged["content_digest"] = canonical_digest(
        {key: value for key, value in forged.items() if key != "content_digest"}
    )
    packet_path.write_bytes(canonical_json(forged) + b"\n")
    with pytest.raises(CentralConceptualRouteError, match="selected route set"):
        run_once()
