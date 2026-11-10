# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Acceptance tests for the strict reference-only world-v3 vocabulary.

The v3 schema is deliberately a shape-and-reference contract, not experiment
or physics authority.  This fixture therefore does two narrow jobs:

* construct every closed union variant, including the no-probe fiber and all
  four executed fibers; and
* state the exact storage edge implied by every payload reference without
  treating those edges as scientific causality.

Whole-history ancestry, producer execution, and cross-generation world closure
belong to the contextual replay layer.  These tests must not imply that schema
validity alone supplies any of those stronger claims.
"""

from __future__ import annotations

import copy
import json
from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any

import pytest

from agentic.discovery.contracts import (
    ContractError,
    SchemaValidationError,
)
from agentic.experiments.world_object_graph import (
    PreparedContentObject,
    prepare_content_object,
)
from agentic.experiments.world_object_roles import (
    CAUSAL_MATERIALIZER_PORTABLE_HEADER_SCHEMA,
    WORLD_DOMAIN_V3_SCHEMA,
    WORLD_V3_AUTHORITY_BOUNDARY,
    RoleAuthority,
    content_object_role,
    derive_content_object_edges,
    require_semantic_content_object_role,
    validate_content_object_payload,
    validate_role_bound_object,
)


WORLD_IDS = (
    "no_probe",
    "neutral_inconclusive",
    "misleading_toy_positive",
    "registered_premise_falsifier",
    "operational_failure",
)
COMPONENT_KINDS = (
    "committed_ancestor",
    "theory_programme",
    "reflection_packet",
    "conceptual_systems",
    "genealogy",
    "source_authority",
    "registered_claim",
    "generator_authority",
    "adjudication_authority",
    "schedule",
)
THEORY_CARRIER_KINDS = (
    "theory_programme",
    "reflection_packet",
    "conceptual_systems",
    "genealogy",
    "registered_claim",
    "generator_authority",
    "adjudication_authority",
    "schedule",
    "experiment_spec_family",
)
WORLD_ROLE_KINDS = (
    "world_theory_carrier_v3",
    "world_precommit_ancestor_carrier_v3",
    "world_plan_v3",
    "world_no_probe_decision_v3",
    "world_execution_result_v3",
    "world_next_cycle_reflection_v3",
    "world_projection_component_v3",
    "world_projection_index_v3",
    "world_matrix_commission_v3",
    "world_request_v3",
    "world_observation_v3",
    "world_observation_envelope_v3",
    "world_matrix_certificate_v3",
    "world_matrix_anchor_root_v3",
    "world_matrix_aggregation_root_v3",
)
EXPECTED_VARIANT_COUNTS = {
    "world_theory_carrier_v3": 9,
    "world_precommit_ancestor_carrier_v3": 1,
    "world_plan_v3": 5,
    "world_no_probe_decision_v3": 1,
    "world_execution_result_v3": 4,
    "world_next_cycle_reflection_v3": 4,
    "world_projection_component_v3": 10,
    "world_projection_index_v3": 1,
    "world_matrix_commission_v3": 1,
    "world_request_v3": 5,
    "world_observation_v3": 5,
    "world_observation_envelope_v3": 5,
    "world_matrix_certificate_v3": 1,
    "world_matrix_anchor_root_v3": 1,
    "world_matrix_aggregation_root_v3": 1,
}
INTERVENTION_BY_WORLD = {
    "no_probe": "suppress_execution",
    "neutral_inconclusive": "bounded_resource_cutoff",
    "misleading_toy_positive": "scoped_positive_fixture",
    "registered_premise_falsifier": "scoped_counterexample_fixture",
    "operational_failure": "adapter_operational_failure",
}
RESULT_STATUS_BY_WORLD = {
    "neutral_inconclusive": "inconclusive",
    "misleading_toy_positive": "scoped_positive",
    "registered_premise_falsifier": "registered_premise_falsified",
    "operational_failure": "operational_failure",
}


def _ref(object_kind: str, label: str) -> dict[str, Any]:
    """Mint an exact ref used as a typed external prerequisite in the fixture."""

    return dict(
        prepare_content_object(
            object_kind=object_kind,
            value={"fixture": label},
            path=f"objects/{label}.json",
        ).ref
    )


def _prepare(
    object_kind: str,
    payload: Mapping[str, Any],
    label: str,
) -> PreparedContentObject:
    return prepare_content_object(
        object_kind=object_kind,
        value=payload,
        path=f"world-v3/{label}.json",
    )


def _base(*, object_kind: str, contract_version: str) -> dict[str, Any]:
    return {
        "schema_version": "3.0.0",
        "contract_version": contract_version,
        "object_kind": object_kind,
        "authority_boundary": dict(WORLD_V3_AUTHORITY_BOUNDARY),
    }


def _entry(world_id: str, object_ref: Mapping[str, Any]) -> dict[str, Any]:
    return {"world_id": world_id, "object_ref": dict(object_ref)}


def _expected_edge(
    source_ref: Mapping[str, Any],
    target_ref: Mapping[str, Any],
    edge_kind: str,
) -> dict[str, str]:
    return {
        "source_object_id": str(source_ref["object_id"]),
        "target_object_id": str(target_ref["object_id"]),
        "edge_kind": edge_kind,
    }


def _valid_fixture() -> dict[str, Any]:
    """Build the closed 15-variant vocabulary over all five world fibers."""

    prepared_objects: list[PreparedContentObject] = []
    expected_edges: dict[str, tuple[dict[str, str], ...]] = {}
    role_examples: dict[str, PreparedContentObject] = {}

    def add(
        object_kind: str,
        payload: Mapping[str, Any],
        label: str,
        edge_sources: Sequence[tuple[Mapping[str, Any], str]] = (),
    ) -> PreparedContentObject:
        prepared = _prepare(object_kind, payload, label)
        prepared_objects.append(prepared)
        role_examples.setdefault(object_kind, prepared)
        expected_edges[str(prepared.ref["object_id"])] = tuple(
            _expected_edge(source_ref, prepared.ref, edge_kind)
            for source_ref, edge_kind in edge_sources
        )
        return prepared

    # Theory carriers are typed adapters over exact producer bytes.  The
    # carrier digest must repeat the source ref's semantic digest exactly.
    theory_carriers: dict[str, PreparedContentObject] = {}
    for carrier_kind in THEORY_CARRIER_KINDS:
        source_ref = _ref(
            "producer_artifact_evidence",
            f"theory-source-{carrier_kind}",
        )
        source_receipt_ref = _ref(
            "producer_receipt_evidence",
            f"theory-source-receipt-{carrier_kind}",
        )
        payload = {
            **_base(
                object_kind="world_theory_carrier_v3",
                contract_version="experiment-world-theory-carrier/3.0.0",
            ),
            "carrier_id": f"carrier.{carrier_kind}",
            "carrier_kind": carrier_kind,
            "source_ref": source_ref,
            "source_semantic_digest": source_ref["semantic_digest"],
            "source_receipt_ref": source_receipt_ref,
        }
        theory_carriers[carrier_kind] = add(
            "world_theory_carrier_v3",
            payload,
            f"theory-carrier-{carrier_kind}",
            (
                (source_ref, "semantic_derivation"),
                (source_receipt_ref, "authority_dependency"),
            ),
        )

    precommit_state_ref = _ref(
        "immutable_history_evidence",
        "committed-generation-6-state",
    )
    precommit_receipt_ref = _ref(
        "producer_receipt_evidence",
        "committed-generation-6-receipt",
    )
    precommit_ancestor = add(
        "world_precommit_ancestor_carrier_v3",
        {
            **_base(
                object_kind="world_precommit_ancestor_carrier_v3",
                contract_version=(
                    "experiment-world-precommit-ancestor-carrier/3.0.0"
                ),
            ),
            "ancestor_id": "ancestor.generation-6",
            "target_id": "target.fixture",
            "run_id": "run.fixture",
            "precommit_state_version": 7,
            "ancestry_relation": "committed_generation_N_minus_1",
            "precommit_state_ref": precommit_state_ref,
            "precommit_state_semantic_digest": precommit_state_ref[
                "semantic_digest"
            ],
            "precommit_receipt_ref": precommit_receipt_ref,
        },
        "precommit-ancestor",
        (
            (precommit_state_ref, "history_dependency"),
            (precommit_receipt_ref, "authority_dependency"),
        ),
    )

    literature_ref = _ref(
        "literature_production_input_bundle",
        "literature-input",
    )
    component_sources: dict[str, Mapping[str, Any]] = {
        "committed_ancestor": precommit_ancestor.ref,
        "source_authority": literature_ref,
        **{
            component_kind: theory_carriers[component_kind].ref
            for component_kind in COMPONENT_KINDS
            if component_kind not in {"committed_ancestor", "source_authority"}
        },
    }
    components: dict[str, PreparedContentObject] = {}
    for component_kind in COMPONENT_KINDS:
        component_source = component_sources[component_kind]
        components[component_kind] = add(
            "world_projection_component_v3",
            {
                **_base(
                    object_kind="world_projection_component_v3",
                    contract_version=(
                        "experiment-world-projection-component/3.0.0"
                    ),
                ),
                "component_id": f"component.{component_kind}",
                "component_kind": component_kind,
                "component_payload_ref": dict(component_source),
            },
            f"projection-component-{component_kind}",
            ((component_source, "semantic_derivation"),),
        )

    projection = add(
        "world_projection_index_v3",
        {
            **_base(
                object_kind="world_projection_index_v3",
                contract_version="experiment-world-projection-index/3.0.0",
            ),
            "projection_id": "projection.fixture",
            "target_id": "target.fixture",
            "run_id": "run.fixture",
            "prior_state_version": 7,
            "components": [
                {
                    "component_kind": component_kind,
                    "object_ref": dict(components[component_kind].ref),
                }
                for component_kind in COMPONENT_KINDS
            ],
        },
        "projection-index",
        tuple(
            (components[component_kind].ref, "semantic_derivation")
            for component_kind in COMPONENT_KINDS
        ),
    )

    adjudication_binding_ref = _ref(
        "causal_materializer_binding_header_v3",
        "adjudication-binding",
    )
    schedule_binding_ref = _ref(
        "causal_materializer_binding_header_v3",
        "schedule-binding",
    )
    commission = add(
        "world_matrix_commission_v3",
        {
            **_base(
                object_kind="world_matrix_commission_v3",
                contract_version=(
                    "dynamic-experiment-world-matrix-commission/3.0.0"
                ),
            ),
            "commission_id": "commission.fixture",
            "target_id": "target.fixture",
            "run_id": "run.fixture",
            "prior_state_version": 7,
            "projection_index_ref": dict(projection.ref),
            "registered_claim_ref": dict(
                theory_carriers["registered_claim"].ref
            ),
            "spec_family_ref": dict(
                theory_carriers["experiment_spec_family"].ref
            ),
            "adjudication_materializer_binding_ref": adjudication_binding_ref,
            "schedule_materializer_binding_ref": schedule_binding_ref,
            "world_order": list(WORLD_IDS),
        },
        "commission",
        (
            (projection.ref, "authority_dependency"),
            (
                theory_carriers["registered_claim"].ref,
                "content_dependency",
            ),
            (
                theory_carriers["experiment_spec_family"].ref,
                "content_dependency",
            ),
            (adjudication_binding_ref, "authority_dependency"),
            (schedule_binding_ref, "authority_dependency"),
        ),
    )

    plans: dict[str, PreparedContentObject] = {}
    requests: dict[str, PreparedContentObject] = {}
    request_bindings: dict[str, dict[str, Any]] = {}
    for ordinal, world_id in enumerate(WORLD_IDS):
        plan_digest = _ref(
            "canonical_cycle_auxiliary_artifact",
            f"plan-source-{world_id}",
        )["semantic_digest"]
        plans[world_id] = add(
            "world_plan_v3",
            {
                **_base(
                    object_kind="world_plan_v3",
                    contract_version="experiment-world-plan/3.0.0",
                ),
                "plan_id": f"plan.{world_id}",
                "world_id": world_id,
                "world_ordinal": ordinal,
                "commission_ref": dict(commission.ref),
                "execution_disposition": (
                    "not_executed" if world_id == "no_probe" else "executed"
                ),
                "intervention_kind": INTERVENTION_BY_WORLD[world_id],
                "source_plan_digest": plan_digest,
            },
            f"plan-{world_id}",
            ((commission.ref, "request_dependency"),),
        )
        requests[world_id] = add(
            "world_request_v3",
            {
                **_base(
                    object_kind="world_request_v3",
                    contract_version="experiment-world-request/3.0.0",
                ),
                "request_id": f"request.{world_id}",
                "world_id": world_id,
                "world_ordinal": ordinal,
                "execution_disposition": (
                    "not_executed" if world_id == "no_probe" else "executed"
                ),
                "commission_ref": dict(commission.ref),
                "world_plan_ref": dict(plans[world_id].ref),
            },
            f"request-{world_id}",
            (
                (commission.ref, "request_dependency"),
                (plans[world_id].ref, "content_dependency"),
            ),
        )
        request_bindings[world_id] = _ref(
            "causal_materializer_binding_header_v3",
            f"request-binding-{world_id}",
        )

    commission_binding_ref = _ref(
        "causal_materializer_binding_header_v3",
        "commission-root-binding",
    )
    anchor = add(
        "world_matrix_anchor_root_v3",
        {
            **_base(
                object_kind="world_matrix_anchor_root_v3",
                contract_version="experiment-world-anchor-root/3.0.0",
            ),
            "anchor_id": "anchor.fixture",
            "target_id": "target.fixture",
            "run_id": "run.fixture",
            "prior_state_version": 7,
            "literature_input_ref": literature_ref,
            "projection_index_ref": dict(projection.ref),
            "commission_ref": dict(commission.ref),
            "commission_materializer_binding_ref": commission_binding_ref,
            "world_requests": [
                _entry(world_id, requests[world_id].ref)
                for world_id in WORLD_IDS
            ],
            "world_request_materializer_bindings": [
                _entry(world_id, request_bindings[world_id])
                for world_id in WORLD_IDS
            ],
            "world_order": list(WORLD_IDS),
        },
        "anchor",
        (
            (literature_ref, "semantic_derivation"),
            (projection.ref, "authority_dependency"),
            (commission.ref, "authority_dependency"),
            (commission_binding_ref, "authority_dependency"),
            *tuple(
                (requests[world_id].ref, "request_dependency")
                for world_id in WORLD_IDS
            ),
            *tuple(
                (request_bindings[world_id], "authority_dependency")
                for world_id in WORLD_IDS
            ),
        ),
    )

    no_probe_decision = add(
        "world_no_probe_decision_v3",
        {
            **_base(
                object_kind="world_no_probe_decision_v3",
                contract_version=(
                    "experiment-world-no-probe-decision/3.0.0"
                ),
            ),
            "decision_id": "decision.no-probe",
            "world_id": "no_probe",
            "world_ordinal": 0,
            "request_ref": dict(requests["no_probe"].ref),
            "decision_kind": "precommitted_no_probe",
            "execution_disposition": "not_executed",
            "source_decision_digest": _ref(
                "canonical_cycle_auxiliary_artifact",
                "no-probe-decision-source",
            )["semantic_digest"],
        },
        "no-probe-decision",
        ((requests["no_probe"].ref, "request_dependency"),),
    )

    results: dict[str, PreparedContentObject] = {}
    reflections: dict[str, PreparedContentObject] = {}
    for ordinal, world_id in enumerate(WORLD_IDS[1:], start=1):
        results[world_id] = add(
            "world_execution_result_v3",
            {
                **_base(
                    object_kind="world_execution_result_v3",
                    contract_version=(
                        "experiment-world-execution-result/3.0.0"
                    ),
                ),
                "result_id": f"result.{world_id}",
                "world_id": world_id,
                "world_ordinal": ordinal,
                "request_ref": dict(requests[world_id].ref),
                "result_status": RESULT_STATUS_BY_WORLD[world_id],
                "source_result_digest": _ref(
                    "canonical_cycle_auxiliary_artifact",
                    f"result-source-{world_id}",
                )["semantic_digest"],
                "result_effect": "next_cycle_reflection_only",
            },
            f"result-{world_id}",
            ((requests[world_id].ref, "observation_dependency"),),
        )
        reflections[world_id] = add(
            "world_next_cycle_reflection_v3",
            {
                **_base(
                    object_kind="world_next_cycle_reflection_v3",
                    contract_version=(
                        "experiment-world-next-cycle-reflection/3.0.0"
                    ),
                ),
                "reflection_id": f"reflection.{world_id}",
                "world_id": world_id,
                "world_ordinal": ordinal,
                "result_ref": dict(results[world_id].ref),
                "reflection_disposition": (
                    "pending_next_cycle_reflection_only"
                ),
                "source_reflection_digest": _ref(
                    "canonical_cycle_auxiliary_artifact",
                    f"reflection-source-{world_id}",
                )["semantic_digest"],
                "current_cycle_theory_mutation_authorized": False,
            },
            f"reflection-{world_id}",
            ((results[world_id].ref, "semantic_derivation"),),
        )

    observations: dict[str, PreparedContentObject] = {}
    observation_bindings: dict[str, dict[str, Any]] = {}
    no_probe_payload = {
        **_base(
            object_kind="world_observation_v3",
            contract_version="experiment-world-observation/3.0.0",
        ),
        "observation_id": "observation.no-probe",
        "world_id": "no_probe",
        "world_ordinal": 0,
        "observation_kind": "no_probe_decision",
        "commission_ref": dict(commission.ref),
        "request_ref": dict(requests["no_probe"].ref),
        "no_probe_decision_ref": dict(no_probe_decision.ref),
        "result_effect": "next_cycle_reflection_only",
    }
    observations["no_probe"] = add(
        "world_observation_v3",
        no_probe_payload,
        "observation-no-probe",
        (
            (commission.ref, "observation_dependency"),
            (requests["no_probe"].ref, "observation_dependency"),
            (no_probe_decision.ref, "content_dependency"),
        ),
    )
    observation_bindings["no_probe"] = _ref(
        "causal_materializer_binding_header_v3",
        "observation-binding-no-probe",
    )

    for ordinal, world_id in enumerate(WORLD_IDS[1:], start=1):
        result_binding_ref = _ref(
            "causal_materializer_binding_header_v3",
            f"result-binding-{world_id}",
        )
        reflection_binding_ref = _ref(
            "causal_materializer_binding_header_v3",
            f"reflection-binding-{world_id}",
        )
        observations[world_id] = add(
            "world_observation_v3",
            {
                **_base(
                    object_kind="world_observation_v3",
                    contract_version="experiment-world-observation/3.0.0",
                ),
                "observation_id": f"observation.{world_id}",
                "world_id": world_id,
                "world_ordinal": ordinal,
                "observation_kind": "executed_result_with_reflection",
                "commission_ref": dict(commission.ref),
                "request_ref": dict(requests[world_id].ref),
                "result_ref": dict(results[world_id].ref),
                "request_materializer_binding_ref": request_bindings[world_id],
                "result_materializer_binding_ref": result_binding_ref,
                "reflection_ref": dict(reflections[world_id].ref),
                "reflection_materializer_binding_ref": reflection_binding_ref,
                "result_effect": "next_cycle_reflection_only",
            },
            f"observation-{world_id}",
            (
                (commission.ref, "observation_dependency"),
                (requests[world_id].ref, "observation_dependency"),
                (results[world_id].ref, "content_dependency"),
                (request_bindings[world_id], "authority_dependency"),
                (result_binding_ref, "authority_dependency"),
                (reflections[world_id].ref, "semantic_derivation"),
                (reflection_binding_ref, "authority_dependency"),
            ),
        )
        observation_bindings[world_id] = _ref(
            "causal_materializer_binding_header_v3",
            f"observation-binding-{world_id}",
        )

    envelopes: dict[str, PreparedContentObject] = {}
    parent_ref: Mapping[str, Any] = anchor.ref
    for ordinal, world_id in enumerate(WORLD_IDS):
        envelopes[world_id] = add(
            "world_observation_envelope_v3",
            {
                **_base(
                    object_kind="world_observation_envelope_v3",
                    contract_version=(
                        "experiment-world-observation-envelope/3.0.0"
                    ),
                ),
                "envelope_id": f"envelope.{world_id}",
                "world_id": world_id,
                "world_ordinal": ordinal,
                "commission_ref": dict(commission.ref),
                "observation_ref": dict(observations[world_id].ref),
                "observation_materializer_binding_ref": (
                    observation_bindings[world_id]
                ),
                "parent_root_ref": dict(parent_ref),
                "observation_materialization_scope": (
                    "typed_observation_storage_only"
                ),
                "experiment_execution_implied": False,
            },
            f"envelope-{world_id}",
            (
                (commission.ref, "observation_dependency"),
                (observations[world_id].ref, "observation_dependency"),
                (
                    observation_bindings[world_id],
                    "authority_dependency",
                ),
                (parent_ref, "history_dependency"),
            ),
        )
        parent_ref = envelopes[world_id].ref

    certificate = add(
        "world_matrix_certificate_v3",
        {
            **_base(
                object_kind="world_matrix_certificate_v3",
                contract_version="experiment-world-certificate/3.0.0",
            ),
            "certificate_id": "certificate.fixture",
            "commission_ref": dict(commission.ref),
            "observation_envelopes": [
                _entry(world_id, envelopes[world_id].ref)
                for world_id in WORLD_IDS
            ],
            "world_order": list(WORLD_IDS),
            "result_effect": "next_cycle_reflection_only",
        },
        "certificate",
        (
            (commission.ref, "aggregation_dependency"),
            *tuple(
                (envelopes[world_id].ref, "aggregation_dependency")
                for world_id in WORLD_IDS
            ),
        ),
    )

    certificate_binding_ref = _ref(
        "causal_materializer_binding_header_v3",
        "certificate-binding",
    )
    aggregation = add(
        "world_matrix_aggregation_root_v3",
        {
            **_base(
                object_kind="world_matrix_aggregation_root_v3",
                contract_version=(
                    "experiment-world-aggregation-root/3.0.0"
                ),
            ),
            "aggregation_id": "aggregation.fixture",
            "target_id": "target.fixture",
            "run_id": "run.fixture",
            "anchor_root_ref": dict(anchor.ref),
            "observation_envelopes": [
                _entry(world_id, envelopes[world_id].ref)
                for world_id in WORLD_IDS
            ],
            "certificate_ref": dict(certificate.ref),
            "certificate_materializer_binding_ref": certificate_binding_ref,
            "world_order": list(WORLD_IDS),
            "result_effect": "next_cycle_reflection_only",
        },
        "aggregation",
        (
            (anchor.ref, "history_dependency"),
            *tuple(
                (envelopes[world_id].ref, "aggregation_dependency")
                for world_id in WORLD_IDS
            ),
            (certificate.ref, "aggregation_dependency"),
            (certificate_binding_ref, "authority_dependency"),
        ),
    )

    return {
        "prepared_objects": prepared_objects,
        "expected_edges": expected_edges,
        "role_examples": role_examples,
        "theory_carriers": theory_carriers,
        "precommit_ancestor": precommit_ancestor,
        "components": components,
        "projection": projection,
        "commission": commission,
        "plans": plans,
        "requests": requests,
        "anchor": anchor,
        "no_probe_decision": no_probe_decision,
        "results": results,
        "reflections": reflections,
        "observations": observations,
        "envelopes": envelopes,
        "certificate": certificate,
        "aggregation": aggregation,
    }


def test_all_fifteen_v3_variants_and_five_world_branches_are_strict() -> None:
    fixture = _valid_fixture()
    counts = Counter(
        str(prepared.ref["object_kind"])
        for prepared in fixture["prepared_objects"]
    )
    assert counts == EXPECTED_VARIANT_COUNTS
    assert set(counts) == set(WORLD_ROLE_KINDS)

    for prepared in fixture["prepared_objects"]:
        object_kind = str(prepared.ref["object_kind"])
        assert validate_content_object_payload(object_kind, prepared.value) == (
            prepared.value
        )
        assert validate_role_bound_object(prepared.ref, prepared.value) == (
            prepared.value
        )
        role = require_semantic_content_object_role(object_kind)
        assert role.authority is RoleAuthority.SEMANTIC_DOMAIN
        assert role.schema_name == WORLD_DOMAIN_V3_SCHEMA
        assert role.domain_validator_id is None

    assert tuple(fixture["plans"]) == WORLD_IDS
    assert tuple(fixture["requests"]) == WORLD_IDS
    assert tuple(fixture["observations"]) == WORLD_IDS
    assert tuple(fixture["envelopes"]) == WORLD_IDS
    assert tuple(fixture["results"]) == WORLD_IDS[1:]
    assert tuple(fixture["reflections"]) == WORLD_IDS[1:]


def test_no_probe_and_all_four_executed_observation_variants_are_closed() -> None:
    fixture = _valid_fixture()
    no_probe = fixture["observations"]["no_probe"].value
    assert no_probe["observation_kind"] == "no_probe_decision"
    assert no_probe["no_probe_decision_ref"] == fixture["no_probe_decision"].ref
    assert {
        "result_ref",
        "request_materializer_binding_ref",
        "result_materializer_binding_ref",
        "reflection_ref",
        "reflection_materializer_binding_ref",
    }.isdisjoint(no_probe)

    for ordinal, world_id in enumerate(WORLD_IDS[1:], start=1):
        plan = fixture["plans"][world_id].value
        request = fixture["requests"][world_id].value
        result = fixture["results"][world_id].value
        reflection = fixture["reflections"][world_id].value
        observation = fixture["observations"][world_id].value
        result_ref = fixture["results"][world_id].ref

        assert plan["world_ordinal"] == ordinal
        assert plan["execution_disposition"] == "executed"
        assert plan["intervention_kind"] == INTERVENTION_BY_WORLD[world_id]
        assert request["execution_disposition"] == "executed"
        assert result["result_status"] == RESULT_STATUS_BY_WORLD[world_id]
        assert reflection["result_ref"] == result_ref
        assert observation["observation_kind"] == (
            "executed_result_with_reflection"
        )
        assert observation["result_ref"] == result_ref
        assert observation["reflection_ref"] == fixture["reflections"][
            world_id
        ].ref
        assert "no_probe_decision_ref" not in observation


def test_every_v3_payload_derives_its_exact_ordered_edge_vector() -> None:
    fixture = _valid_fixture()
    for prepared in fixture["prepared_objects"]:
        actual = derive_content_object_edges(
            object_ref=prepared.ref,
            payload=prepared.value,
        )
        expected = fixture["expected_edges"][prepared.ref["object_id"]]
        assert actual == expected, (
            prepared.ref["object_kind"],
            prepared.ref["object_id"],
        )
        assert all(
            edge["target_object_id"] == prepared.ref["object_id"]
            for edge in actual
        )

    projection = fixture["projection"]
    projection_edges = derive_content_object_edges(
        object_ref=projection.ref,
        payload=projection.value,
    )
    assert [edge["source_object_id"] for edge in projection_edges] == [
        fixture["components"][component_kind].ref["object_id"]
        for component_kind in COMPONENT_KINDS
    ]
    assert {edge["edge_kind"] for edge in projection_edges} == {
        "semantic_derivation"
    }


def test_v3_union_rejects_embedded_values_open_fields_and_role_laundering() -> None:
    fixture = _valid_fixture()
    request = fixture["requests"]["neutral_inconclusive"].value
    forbidden = {
        "authority_projection": {"legacy": "embedded-v2-value"},
        "commission": {"legacy": "embedded-v2-value"},
        "request": {"legacy": "embedded-v2-value"},
        "envelope": {"legacy": "embedded-v2-value"},
        "artifact_value": {"forbidden": True},
        "bytes_base64": "Zm9yYmlkZGVu",
        "path": "../../forbidden",
        "callback": "module:function",
        "open_object": {"anything": ["goes"]},
    }
    for field, value in forbidden.items():
        forged = copy.deepcopy(request)
        forged[field] = value
        with pytest.raises(SchemaValidationError):
            validate_content_object_payload("world_request_v3", forged)

    nested_ref_forgery = copy.deepcopy(request)
    nested_ref_forgery["commission_ref"]["path"] = "objects/commission.json"
    with pytest.raises(SchemaValidationError):
        validate_content_object_payload("world_request_v3", nested_ref_forgery)

    nested_entry_forgery = copy.deepcopy(fixture["anchor"].value)
    nested_entry_forgery["world_requests"][0]["request"] = {
        "legacy": "embedded-v2-value"
    }
    with pytest.raises(SchemaValidationError):
        validate_content_object_payload(
            "world_matrix_anchor_root_v3",
            nested_entry_forgery,
        )

    local_binding_forgery = copy.deepcopy(fixture["commission"].value)
    local_binding_forgery["adjudication_materializer_binding_ref"] = _ref(
        "causal_materializer_binding_v3",
        "workspace-bound-local-binding",
    )
    with pytest.raises(SchemaValidationError):
        validate_content_object_payload(
            "world_matrix_commission_v3",
            local_binding_forgery,
        )

    encoded = json.dumps(
        [prepared.value for prepared in fixture["prepared_objects"]],
        sort_keys=True,
    )
    for forbidden_name in (
        '"artifact_value"',
        '"bytes_base64"',
        '"path"',
        '"callback"',
        '"authority_projection"',
        '"base_materializer_binding_refs"',
        '"aggregation_materializer_binding_ref"',
    ):
        assert forbidden_name not in encoded


def test_v3_union_fixes_reference_roles_world_order_and_authority_nulls() -> None:
    fixture = _valid_fixture()

    wrong_ref = copy.deepcopy(fixture["commission"].value)
    wrong_ref["projection_index_ref"] = _ref(
        "canonical_cycle_auxiliary_artifact",
        "laundered-projection",
    )
    with pytest.raises(SchemaValidationError):
        validate_content_object_payload("world_matrix_commission_v3", wrong_ref)

    source_component = copy.deepcopy(
        fixture["components"]["source_authority"].value
    )
    source_component["component_payload_ref"] = _ref(
        "canonical_cycle_auxiliary_artifact",
        "laundered-literature",
    )
    with pytest.raises(SchemaValidationError):
        validate_content_object_payload(
            "world_projection_component_v3",
            source_component,
        )

    nonsource_component = copy.deepcopy(
        fixture["components"]["theory_programme"].value
    )
    nonsource_component["component_payload_ref"] = _ref(
        "literature_production_input_bundle",
        "laundered-auxiliary",
    )
    with pytest.raises(SchemaValidationError):
        validate_content_object_payload(
            "world_projection_component_v3",
            nonsource_component,
        )

    wrong_position = copy.deepcopy(
        fixture["requests"]["neutral_inconclusive"].value
    )
    wrong_position["world_ordinal"] = 4
    with pytest.raises(SchemaValidationError):
        validate_content_object_payload("world_request_v3", wrong_position)

    for field in ("world_requests", "world_request_materializer_bindings"):
        short = copy.deepcopy(fixture["anchor"].value)
        short[field] = short[field][:-1]
        with pytest.raises(SchemaValidationError):
            validate_content_object_payload("world_matrix_anchor_root_v3", short)

        reordered = copy.deepcopy(fixture["anchor"].value)
        reordered[field][0], reordered[field][1] = (
            reordered[field][1],
            reordered[field][0],
        )
        with pytest.raises(SchemaValidationError):
            validate_content_object_payload(
                "world_matrix_anchor_root_v3",
                reordered,
            )

    extra = copy.deepcopy(fixture["certificate"].value)
    extra["observation_envelopes"].append(
        extra["observation_envelopes"][-1]
    )
    with pytest.raises(SchemaValidationError):
        validate_content_object_payload("world_matrix_certificate_v3", extra)

    reversed_order = copy.deepcopy(fixture["aggregation"].value)
    reversed_order["world_order"] = list(reversed(WORLD_IDS))
    with pytest.raises(SchemaValidationError):
        validate_content_object_payload(
            "world_matrix_aggregation_root_v3",
            reversed_order,
        )

    for field, forged_value in (
        ("experiment_result_effect", "current_cycle_selection"),
        ("current_cycle_theory_mutation_authorized", True),
        ("automatic_theory_selection_authorized", True),
        ("proof_authority", True),
        ("physics_authority", True),
    ):
        authority_forgery = copy.deepcopy(fixture["aggregation"].value)
        authority_forgery["authority_boundary"][field] = forged_value
        with pytest.raises(SchemaValidationError):
            validate_content_object_payload(
                "world_matrix_aggregation_root_v3",
                authority_forgery,
            )


def test_v3_failures_expose_typed_schema_or_exact_contract_diagnostics() -> None:
    fixture = _valid_fixture()

    role_laundering = copy.deepcopy(fixture["commission"].value)
    with pytest.raises(ContractError) as role_error:
        validate_content_object_payload("world_request_v3", role_laundering)
    assert type(role_error.value) is ContractError
    assert str(role_error.value) == (
        "v3 world-domain object kind differs from its storage role"
    )

    theory_digest_forgery = copy.deepcopy(
        fixture["theory_carriers"]["theory_programme"].value
    )
    theory_digest_forgery["source_semantic_digest"] = _ref(
        "producer_artifact_evidence",
        "different-theory-source",
    )["semantic_digest"]
    with pytest.raises(ContractError) as theory_error:
        validate_content_object_payload(
            "world_theory_carrier_v3",
            theory_digest_forgery,
        )
    assert type(theory_error.value) is ContractError
    assert str(theory_error.value) == (
        "theory carrier digest differs from its exact source ref"
    )

    ancestor_digest_forgery = copy.deepcopy(
        fixture["precommit_ancestor"].value
    )
    ancestor_digest_forgery["precommit_state_semantic_digest"] = _ref(
        "immutable_history_evidence",
        "different-precommit-state",
    )["semantic_digest"]
    with pytest.raises(ContractError) as ancestor_error:
        validate_content_object_payload(
            "world_precommit_ancestor_carrier_v3",
            ancestor_digest_forgery,
        )
    assert type(ancestor_error.value) is ContractError
    assert str(ancestor_error.value) == (
        "precommit ancestor digest differs from its exact committed-state ref"
    )

    no_probe_execution_smuggling = copy.deepcopy(
        fixture["observations"]["no_probe"].value
    )
    no_probe_execution_smuggling["result_ref"] = dict(
        fixture["results"]["neutral_inconclusive"].ref
    )
    with pytest.raises(SchemaValidationError) as schema_error:
        validate_content_object_payload(
            "world_observation_v3",
            no_probe_execution_smuggling,
        )
    assert schema_error.value.schema_name == WORLD_DOMAIN_V3_SCHEMA
    assert schema_error.value.locations == ("$",)


def test_materializer_and_opaque_authority_boundaries_remain_distinct() -> None:
    materializer = require_semantic_content_object_role(
        "causal_materializer_binding_v3"
    )
    assert materializer.schema_name == (
        "dynamic_experiment_causal_materializer_binding_v3.schema.json"
    )
    assert materializer.domain_validator_id == (
        "validate_causal_materializer_binding_v3"
    )

    portable_materializer = content_object_role(
        "causal_materializer_binding_header_v3"
    )
    assert portable_materializer.authority is RoleAuthority.STRUCTURAL_REFERENCE
    assert portable_materializer.schema_name == (
        CAUSAL_MATERIALIZER_PORTABLE_HEADER_SCHEMA
    )
    with pytest.raises(ContractError, match="no semantic-domain authority"):
        require_semantic_content_object_role(
            "causal_materializer_binding_header_v3"
        )

    auxiliary = content_object_role("canonical_cycle_auxiliary_artifact")
    assert auxiliary.authority is RoleAuthority.OPAQUE_STORAGE
    assert auxiliary.schema_name is None
    with pytest.raises(ContractError, match="no semantic-domain authority"):
        require_semantic_content_object_role(
            "canonical_cycle_auxiliary_artifact"
        )


def test_existing_v2_role_contracts_remain_exactly_bound() -> None:
    expected = {
        "world_authority_projection": (
            "dynamic_experiment_world_authority_projection_v2.schema.json",
            "validate_experiment_authority_projection",
        ),
        "world_matrix_commission": (
            "dynamic_experiment_world_matrix_commission_v2.schema.json",
            "validate_experiment_world_matrix_commission_v2",
        ),
        "world_request": (
            "dynamic_experiment_world_request_v2.schema.json",
            "validate_experiment_world_request",
        ),
        "world_observation_envelope": (
            "dynamic_experiment_world_observation_envelope_v2.schema.json",
            "validate_experiment_world_observation_envelope",
        ),
    }
    for object_kind, (schema_name, validator_id) in expected.items():
        role = content_object_role(object_kind)
        assert role.schema_name == schema_name
        assert role.domain_validator_id == validator_id
