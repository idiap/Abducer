# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial checks for semantic roles above the opaque object store.

The storage kernel is intentionally able to preserve any registered canonical
JSON object.  These tests prove that domain consumption is stricter: semantic
roles use their exact existing schemas, opaque roles cannot cross that boundary,
and caller-authored graph labels cannot replace reference-derived header edges.
"""

from __future__ import annotations

import copy
from pathlib import Path
from types import MappingProxyType

import pytest

from agentic.discovery.contracts import ContractError, load_schema
from agentic.experiments.world_object_graph import (
    VerifiedContentObjectGraph,
    build_content_object_graph,
    prepare_content_object,
)
from agentic.experiments.world_object_roles import (
    CAUSAL_MATERIALIZER_PORTABLE_HEADER_SCHEMA,
    CONTENT_OBJECT_HEADER_SCHEMA,
    CONTENT_OBJECT_KIND_SCHEMA,
    CONTENT_OBJECT_ROLES,
    HEADER_AUTHORITY_BOUNDARY,
    RoleAuthority,
    content_object_role,
    derive_content_object_edges,
    require_semantic_content_object_role,
    seal_content_object_header,
    validate_content_object_payload,
    validate_content_object_role_registry,
    validate_payload_derived_edges,
    validate_role_bound_object,
)


def _evidence_header(payload_ref: dict[str, object]) -> dict[str, object]:
    return seal_content_object_header(
        {
            "schema_version": "1.0.0",
            "header_kind": "producer_evidence_header",
            "evidence_authority_id": "authority.fixture",
            "stage_id": "stage.fixture",
            "producer_role": "producer.fixture",
            "target_id": "target.fixture",
            "run_id": "run.fixture",
            "state_version": 3,
            "evidence_kind": "staged_input",
            "evidence_payload_ref": payload_ref,
            "authority_boundary": dict(HEADER_AUTHORITY_BOUNDARY),
        }
    )


def test_registry_exactly_covers_closed_kind_schema_and_is_immutable() -> None:
    validate_content_object_role_registry()
    kind_schema = load_schema(CONTENT_OBJECT_KIND_SCHEMA)
    assert set(CONTENT_OBJECT_ROLES) == set(kind_schema["enum"])
    assert isinstance(CONTENT_OBJECT_ROLES, MappingProxyType)
    with pytest.raises(TypeError):
        CONTENT_OBJECT_ROLES["forged"] = content_object_role(  # type: ignore[index]
            "world_request"
        )
    with pytest.raises(ContractError, match="unregistered"):
        content_object_role("forged-domain-role")


def test_semantic_roles_bind_exact_existing_schemas_and_validators() -> None:
    expected = {
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
        "world_matrix_certificate": (
            "dynamic_experiment_world_matrix_certificate_v2.schema.json",
            "validate_experiment_world_matrix_certificate_v2",
        ),
        "causal_producer_binding": (
            "dynamic_experiment_causal_producer_binding_v2.schema.json",
            "validate_experiment_causal_producer_binding",
        ),
    }
    for object_kind, (schema_name, validator_id) in expected.items():
        role = require_semantic_content_object_role(object_kind)
        assert role.authority is RoleAuthority.SEMANTIC_DOMAIN
        assert role.schema_name == schema_name
        assert role.domain_validator_id == validator_id
        with pytest.raises(ContractError):
            validate_content_object_payload(object_kind, {"forged": True})


def test_storage_kind_alone_does_not_confer_semantic_authority() -> None:
    # The low-level store accepts canonical bytes under a closed storage label.
    # The higher semantic boundary must still reject a forged domain payload.
    forged = prepare_content_object(
        object_kind="world_matrix_commission",
        value={"forged": True},
        path="objects/forged-commission.json",
    )
    assert forged.ref["object_kind"] == "world_matrix_commission"
    with pytest.raises(ContractError):
        validate_role_bound_object(forged.ref, forged.value)


@pytest.mark.parametrize(
    "object_kind",
    [
        "producer_artifact_evidence",
        "immutable_history_evidence",
        "staged_input_evidence",
    ],
)
def test_opaque_storage_roles_cannot_cross_semantic_boundary(
    object_kind: str,
) -> None:
    payload = {"role_specific_bytes": {"remain": "opaque"}}
    assert validate_content_object_payload(object_kind, payload) == payload
    role = content_object_role(object_kind)
    assert role.authority is RoleAuthority.OPAQUE_STORAGE
    assert role.schema_name is None
    assert role.domain_validator_id is None
    with pytest.raises(ContractError, match="no semantic-domain authority"):
        require_semantic_content_object_role(object_kind)


def test_structural_header_seals_exact_null_authority_and_derives_edge() -> None:
    staged = prepare_content_object(
        object_kind="staged_input_evidence",
        value={"staged": "exact-input"},
        path="objects/staged-input.json",
    )
    header_value = _evidence_header(dict(staged.ref))
    header = prepare_content_object(
        object_kind="producer_evidence_header",
        value=header_value,
        path="headers/staged-input.json",
    )
    assert header_value["authority_boundary"] == dict(HEADER_AUTHORITY_BOUNDARY)
    assert content_object_role("producer_evidence_header").authority is (
        RoleAuthority.STRUCTURAL_REFERENCE
    )
    with pytest.raises(ContractError, match="no semantic-domain authority"):
        require_semantic_content_object_role("producer_evidence_header")

    expected = (
        {
            "source_object_id": staged.ref["object_id"],
            "target_object_id": header.ref["object_id"],
            "edge_kind": "content_dependency",
        },
    )
    assert derive_content_object_edges(
        object_ref=header.ref,
        payload=header.value,
    ) == expected
    assert validate_payload_derived_edges(
        objects=((staged.ref, staged.value), (header.ref, header.value)),
        declared_edges=expected,
    ) == expected


def test_header_edge_label_and_reference_membership_are_not_caller_authored() -> None:
    staged = prepare_content_object(
        object_kind="staged_input_evidence",
        value={"staged": "exact-input"},
        path="objects/staged-input.json",
    )
    header = prepare_content_object(
        object_kind="producer_evidence_header",
        value=_evidence_header(dict(staged.ref)),
        path="headers/staged-input.json",
    )
    derived = list(
        derive_content_object_edges(object_ref=header.ref, payload=header.value)
    )
    wrong_label = copy.deepcopy(derived)
    wrong_label[0]["edge_kind"] = "history_dependency"
    with pytest.raises(ContractError, match="payload-derived"):
        validate_payload_derived_edges(
            objects=((staged.ref, staged.value), (header.ref, header.value)),
            declared_edges=wrong_label,
        )
    with pytest.raises(ContractError, match="lacks one exact supplied"):
        validate_payload_derived_edges(
            objects=((header.ref, header.value),),
            declared_edges=derived,
        )


def test_every_declared_edge_is_accounted_for_even_between_opaque_roles() -> None:
    """An opaque target cannot hide a caller-authored reachability arrow."""

    source = prepare_content_object(
        object_kind="canonical_cycle_auxiliary_artifact",
        value={"fixture": "opaque-source"},
        path="objects/opaque-source.json",
    )
    target = prepare_content_object(
        object_kind="canonical_cycle_auxiliary_artifact",
        value={"fixture": "opaque-target"},
        path="objects/opaque-target.json",
    )
    invented = {
        "source_object_id": source.ref["object_id"],
        "target_object_id": target.ref["object_id"],
        "edge_kind": "content_dependency",
    }
    with pytest.raises(ContractError, match="not payload-derived"):
        validate_payload_derived_edges(
            objects=((source.ref, source.value), (target.ref, target.value)),
            declared_edges=(invented,),
        )


def test_total_edge_validation_rejects_smuggling_relabel_and_duplicates() -> None:
    staged = prepare_content_object(
        object_kind="staged_input_evidence",
        value={"staged": "exact-input"},
        path="objects/staged-input.json",
    )
    header = prepare_content_object(
        object_kind="producer_evidence_header",
        value=_evidence_header(dict(staged.ref)),
        path="headers/staged-input.json",
    )
    exact = list(
        derive_content_object_edges(object_ref=header.ref, payload=header.value)
    )

    duplicate = [*copy.deepcopy(exact), copy.deepcopy(exact[0])]
    with pytest.raises(ContractError, match="duplicate typed edge"):
        validate_payload_derived_edges(
            objects=((staged.ref, staged.value), (header.ref, header.value)),
            declared_edges=duplicate,
        )

    relabelled = copy.deepcopy(exact)
    relabelled[0]["edge_kind"] = "history_dependency"
    with pytest.raises(ContractError, match="not payload-derived"):
        validate_payload_derived_edges(
            objects=((staged.ref, staged.value), (header.ref, header.value)),
            declared_edges=relabelled,
        )

    unsupplied = copy.deepcopy(exact)
    unsupplied[0]["source_object_id"] = "smuggled-object-not-in-role-set"
    with pytest.raises(ContractError, match="unsupplied object"):
        validate_payload_derived_edges(
            objects=((staged.ref, staged.value), (header.ref, header.value)),
            declared_edges=unsupplied,
        )


def test_resolved_import_source_cannot_authorize_an_unreferenced_edge() -> None:
    """Imported bytes participate only through an exact payload reference."""

    imported_source = prepare_content_object(
        object_kind="staged_input_evidence",
        value={"staged": "resolved-from-prior-commit"},
        path="prior/imported-source.json",
    )
    header = prepare_content_object(
        object_kind="producer_evidence_header",
        value=_evidence_header(dict(imported_source.ref)),
        path="generation-two/header.json",
    )
    opaque_target = prepare_content_object(
        object_kind="canonical_cycle_auxiliary_artifact",
        value={"fixture": "local-opaque-target"},
        path="generation-two/opaque-target.json",
    )
    exact = list(
        derive_content_object_edges(object_ref=header.ref, payload=header.value)
    )
    objects = (
        (imported_source.ref, imported_source.value),
        (header.ref, header.value),
        (opaque_target.ref, opaque_target.value),
    )
    assert validate_payload_derived_edges(
        objects=objects,
        declared_edges=exact,
    ) == tuple(exact)

    invented_import_edge = {
        "source_object_id": imported_source.ref["object_id"],
        "target_object_id": opaque_target.ref["object_id"],
        "edge_kind": "content_dependency",
    }
    with pytest.raises(ContractError, match="not payload-derived"):
        validate_payload_derived_edges(
            objects=objects,
            declared_edges=(*exact, invented_import_edge),
        )


def test_root_closure_cannot_be_manufactured_by_an_invented_edge(
    tmp_path: Path,
) -> None:
    """Storage reopening succeeds only until semantic edge replay rejects it."""

    source = prepare_content_object(
        object_kind="canonical_cycle_auxiliary_artifact",
        value={"fixture": "opaque-source"},
        path="objects/opaque-source.json",
    )
    root = prepare_content_object(
        object_kind="canonical_cycle_auxiliary_artifact",
        value={"fixture": "opaque-root"},
        path="objects/opaque-root.json",
    )
    smuggled = prepare_content_object(
        object_kind="canonical_cycle_auxiliary_artifact",
        value={"fixture": "smuggled"},
        path="objects/smuggled.json",
    )
    invented = {
        "source_object_id": source.ref["object_id"],
        "target_object_id": root.ref["object_id"],
        "edge_kind": "content_dependency",
    }

    # An unreferenced object is rejected by graph-root closure.  Adding a fake
    # arrow can satisfy storage reachability, so semantic replay must then
    # reject that arrow rather than silently filtering it out.
    with pytest.raises(ContractError, match="outside root closure"):
        build_content_object_graph(
            local_descriptors=(source.descriptor, root.descriptor, smuggled.descriptor),
            imported_handles=(),
            ordered_roots=(root.ref["object_id"],),
            edges=(invented,),
            topological_order=(
                source.ref["object_id"],
                root.ref["object_id"],
                smuggled.ref["object_id"],
            ),
        )

    graph = build_content_object_graph(
        local_descriptors=(source.descriptor, root.descriptor),
        imported_handles=(),
        ordered_roots=(root.ref["object_id"],),
        edges=(invented,),
        topological_order=(source.ref["object_id"], root.ref["object_id"]),
    )
    for prepared in (source, root):
        destination = tmp_path / str(prepared.descriptor["path"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(prepared.data)
    resolved = VerifiedContentObjectGraph(
        local_root=tmp_path,
        graph=graph,
    ).verify_closure()
    with pytest.raises(ContractError, match="not payload-derived"):
        validate_payload_derived_edges(
            objects=tuple((row.ref, row.value) for row in resolved),
            declared_edges=graph["edges"],
        )


def test_evidence_discriminator_rejects_role_laundering() -> None:
    staged = prepare_content_object(
        object_kind="staged_input_evidence",
        value={"staged": "exact-input"},
        path="objects/staged-input.json",
    )
    forged = _evidence_header(dict(staged.ref))
    forged["evidence_kind"] = "producer_artifact"
    forged.pop("header_digest")
    with pytest.raises(ContractError):
        seal_content_object_header(forged)


def test_role_payload_must_replay_exact_content_ref() -> None:
    prepared = prepare_content_object(
        object_kind="staged_input_evidence",
        value={"staged": "exact-input"},
        path="objects/staged-input.json",
    )
    assert validate_role_bound_object(prepared.ref, prepared.value) == prepared.value
    with pytest.raises(ContractError, match="differs from its exact"):
        validate_role_bound_object(prepared.ref, {"staged": "changed"})


def test_header_schema_and_projection_wrapper_resolve_locally() -> None:
    header_schema = load_schema(CONTENT_OBJECT_HEADER_SCHEMA)
    projection_schema = load_schema(
        "dynamic_experiment_world_authority_projection_v2.schema.json"
    )
    assert len(header_schema["oneOf"]) == 8
    assert projection_schema["$ref"].endswith("#/$defs/authorityProjection")


def test_every_structural_role_has_payload_reference_declarations() -> None:
    structural = [
        role
        for role in CONTENT_OBJECT_ROLES.values()
        if role.authority is RoleAuthority.STRUCTURAL_REFERENCE
    ]
    assert {role.object_kind for role in structural} == {
        "literature_projection_header",
        "world_authority_projection_header",
        "world_matrix_commission_header",
        "world_request_header",
        "world_observation_header",
        "world_matrix_aggregation_header",
        "causal_producer_binding_header",
        "producer_evidence_header",
        "causal_materializer_evidence_header_v3",
        "causal_materializer_binding_header_v3",
    }
    assert all(
        role.schema_name
        in {CONTENT_OBJECT_HEADER_SCHEMA, CAUSAL_MATERIALIZER_PORTABLE_HEADER_SCHEMA}
        for role in structural
    )
    assert {
        role.object_kind
        for role in structural
        if role.schema_name == CAUSAL_MATERIALIZER_PORTABLE_HEADER_SCHEMA
    } == {
        "causal_materializer_evidence_header_v3",
        "causal_materializer_binding_header_v3",
    }
    assert all(role.references for role in structural)
