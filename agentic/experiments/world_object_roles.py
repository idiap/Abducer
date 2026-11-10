# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Closed semantic-role layer above the content-addressed storage kernel.

``world_object_graph`` proves exact bytes, safe location, and graph closure.  It
deliberately cannot infer what those bytes mean.  This module supplies the next
layer: a closed registry that separates opaque storage, thin structural headers,
and schema-bound domain payloads.  Only the last class may enter a domain
validator, and contextual validators still require their exact commission,
observation, request, or evidence context.

Reference declarations live beside the role contract.  They let callers derive
dependency edges from header fields and from the thin v3 domain atoms, then
reject a caller-authored edge label whenever the relationship is structurally
knowable.  These edges remain storage dependencies; they are not scientific
entailment or causal discovery.
"""

from __future__ import annotations

import copy
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any

from agentic.discovery.contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    canonical_json,
    stable_identifier,
    validate_payload,
)


CONTENT_OBJECT_ID_PREFIX = "world-content-object-v1"
CONTENT_OBJECT_REF_SCHEMA = "dynamic_experiment_content_object_ref_v1.schema.json"
CONTENT_OBJECT_KIND_SCHEMA = "dynamic_experiment_content_object_kind_v1.schema.json"
CONTENT_OBJECT_HEADER_SCHEMA = (
    "dynamic_experiment_content_object_headers_v1.schema.json"
)
WORLD_DOMAIN_V3_SCHEMA = "dynamic_experiment_world_domain_objects_v3.schema.json"
CAUSAL_MATERIALIZER_PORTABLE_RECORD_SCHEMA = (
    "dynamic_experiment_causal_materializer_portable_records_v3.schema.json"
)
CAUSAL_MATERIALIZER_PORTABLE_HEADER_SCHEMA = (
    "dynamic_experiment_causal_materializer_portable_headers_v3.schema.json"
)
CAUSAL_MATERIALIZER_PROTOCOL_AUTHORITY_BOUNDARY = (
    "local_exact_byte_materialization_only_not_semantic_authorship_external_"
    "independence_theory_selection_proof_or_physics_authority"
)

WORLD_V3_AUTHORITY_BOUNDARY = MappingProxyType(
    {
        "contract_scope": "typed_reference_structure_only",
        "contextual_execution_authority": "requires_separate_domain_replay",
        "experiment_subordinate_to_theory": True,
        "experiment_result_effect": "next_cycle_reflection_only",
        "current_cycle_theory_mutation_authorized": False,
        "automatic_theory_selection_authorized": False,
        "automatic_evidence_relation_authorized": False,
        "source_truth_authority": False,
        "literature_benefit_authority": False,
        "truth_authority": False,
        "proof_authority": False,
        "physics_authority": False,
    }
)

HEADER_AUTHORITY_BOUNDARY = MappingProxyType(
    {
        "storage_graph_authority": "structural_reference_only",
        "domain_payload_authority": False,
        "scientific_authority": False,
        "theory_mutation_authorized": False,
    }
)

_EDGE_KINDS = frozenset(
    {
        "content_dependency",
        "authority_dependency",
        "request_dependency",
        "observation_dependency",
        "aggregation_dependency",
        "history_dependency",
        "semantic_derivation",
    }
)


class RoleAuthority(str, Enum):
    """The strongest claim made after role payload validation."""

    OPAQUE_STORAGE = "opaque_storage"
    STRUCTURAL_REFERENCE = "structural_reference"
    SEMANTIC_DOMAIN = "semantic_domain"


@dataclass(frozen=True, slots=True)
class ReferenceDeclaration:
    """One payload field whose exact object ref entails a storage DAG edge."""

    field: str
    edge_kind: str
    allowed_target_kinds: frozenset[str]
    many: bool = False
    target_evidence_kind: str | None = None
    item_ref_field: str | None = None


@dataclass(frozen=True, slots=True)
class ContentObjectRole:
    """Closed metadata for one storage kind and its authority ceiling."""

    object_kind: str
    authority: RoleAuthority
    schema_name: str | None
    domain_validator_id: str | None = None
    references: tuple[ReferenceDeclaration, ...] = ()

    @property
    def grants_domain_authority(self) -> bool:
        """Report whether contextual semantic validation is admissible."""

        return self.authority is RoleAuthority.SEMANTIC_DOMAIN


def _one(
    field: str,
    edge_kind: str,
    *target_kinds: str,
    target_evidence_kind: str | None = None,
) -> ReferenceDeclaration:
    return ReferenceDeclaration(
        field=field,
        edge_kind=edge_kind,
        allowed_target_kinds=frozenset(target_kinds),
        target_evidence_kind=target_evidence_kind,
    )


def _many(
    field: str,
    edge_kind: str,
    *target_kinds: str,
    item_ref_field: str | None = None,
) -> ReferenceDeclaration:
    return ReferenceDeclaration(
        field=field,
        edge_kind=edge_kind,
        allowed_target_kinds=frozenset(target_kinds),
        many=True,
        item_ref_field=item_ref_field,
    )


def _semantic(
    object_kind: str,
    schema_name: str,
    domain_validator_id: str | None = None,
) -> ContentObjectRole:
    return ContentObjectRole(
        object_kind=object_kind,
        authority=RoleAuthority.SEMANTIC_DOMAIN,
        schema_name=schema_name,
        domain_validator_id=domain_validator_id,
    )


def _opaque(object_kind: str) -> ContentObjectRole:
    return ContentObjectRole(
        object_kind=object_kind,
        authority=RoleAuthority.OPAQUE_STORAGE,
        schema_name=None,
    )


def _typed_opaque(
    object_kind: str,
    schema_name: str,
    *references: ReferenceDeclaration,
) -> ContentObjectRole:
    """Schema-check protocol evidence without granting semantic authority."""

    return ContentObjectRole(
        object_kind=object_kind,
        authority=RoleAuthority.OPAQUE_STORAGE,
        schema_name=schema_name,
        references=tuple(references),
    )


def _referential_semantic(
    object_kind: str,
    *references: ReferenceDeclaration,
) -> ContentObjectRole:
    return ContentObjectRole(
        object_kind=object_kind,
        authority=RoleAuthority.SEMANTIC_DOMAIN,
        schema_name=WORLD_DOMAIN_V3_SCHEMA,
        references=tuple(references),
    )


def _header(
    object_kind: str,
    *references: ReferenceDeclaration,
) -> ContentObjectRole:
    return ContentObjectRole(
        object_kind=object_kind,
        authority=RoleAuthority.STRUCTURAL_REFERENCE,
        schema_name=CONTENT_OBJECT_HEADER_SCHEMA,
        references=tuple(references),
    )


def _portable_materializer_header(
    object_kind: str,
    *references: ReferenceDeclaration,
) -> ContentObjectRole:
    """Register a structural materializer header under its strict v3 union."""

    return ContentObjectRole(
        object_kind=object_kind,
        authority=RoleAuthority.STRUCTURAL_REFERENCE,
        schema_name=CAUSAL_MATERIALIZER_PORTABLE_HEADER_SCHEMA,
        references=tuple(references),
    )


_ROLE_ROWS = (
    _semantic(
        "literature_production_input_bundle",
        "literature_production_input_bundle.schema.json",
        "validate_portable_literature_production_input_bundle",
    ),
    _semantic(
        "world_authority_projection",
        "dynamic_experiment_world_authority_projection_v2.schema.json",
        "validate_experiment_authority_projection",
    ),
    _semantic(
        "world_matrix_commission",
        "dynamic_experiment_world_matrix_commission_v2.schema.json",
        "validate_experiment_world_matrix_commission_v2",
    ),
    _semantic(
        "causal_producer_binding",
        "dynamic_experiment_causal_producer_binding_v2.schema.json",
        "validate_experiment_causal_producer_binding",
    ),
    _semantic(
        "world_request",
        "dynamic_experiment_world_request_v2.schema.json",
        "validate_experiment_world_request",
    ),
    _semantic(
        "world_observation",
        "dynamic_experiment_world_matrix_observation_v2.schema.json",
        "validate_experiment_world_observation",
    ),
    _semantic(
        "world_observation_envelope",
        "dynamic_experiment_world_observation_envelope_v2.schema.json",
        "validate_experiment_world_observation_envelope",
    ),
    _semantic(
        "world_matrix_certificate",
        "dynamic_experiment_world_matrix_certificate_v2.schema.json",
        "validate_experiment_world_matrix_certificate_v2",
    ),
    _semantic(
        "causal_materializer_binding_v3",
        "dynamic_experiment_causal_materializer_binding_v3.schema.json",
        "validate_causal_materializer_binding_v3",
    ),
    # The local binding above intentionally remains workspace-bound compatibility
    # evidence.  Active v3 worlds may reference only the structural root below.
    _opaque("causal_materializer_artifact_evidence_v3"),
    _typed_opaque(
        "causal_materializer_request_record_v3",
        CAUSAL_MATERIALIZER_PORTABLE_RECORD_SCHEMA,
        _one(
            "artifact_ref",
            "request_dependency",
            "causal_materializer_artifact_evidence_v3",
        ),
    ),
    _typed_opaque(
        "causal_materializer_attempt_record_v3",
        CAUSAL_MATERIALIZER_PORTABLE_RECORD_SCHEMA,
        _one(
            "request_ref",
            "request_dependency",
            "causal_materializer_request_record_v3",
        ),
        _one(
            "artifact_ref",
            "content_dependency",
            "causal_materializer_artifact_evidence_v3",
        ),
    ),
    _typed_opaque(
        "causal_materializer_clock_record_v3",
        CAUSAL_MATERIALIZER_PORTABLE_RECORD_SCHEMA,
        _one(
            "request_ref",
            "authority_dependency",
            "causal_materializer_request_record_v3",
        ),
        _one(
            "successful_receipt_ref",
            "history_dependency",
            "causal_materializer_attempt_record_v3",
        ),
    ),
    _typed_opaque(
        "causal_materializer_dependency_record_v3",
        CAUSAL_MATERIALIZER_PORTABLE_RECORD_SCHEMA,
    ),
    _portable_materializer_header(
        "causal_materializer_evidence_header_v3",
        _many(
            "evidence_payload_refs",
            "content_dependency",
            "causal_materializer_artifact_evidence_v3",
            "causal_materializer_request_record_v3",
            "causal_materializer_attempt_record_v3",
            "causal_materializer_clock_record_v3",
        ),
    ),
    _portable_materializer_header(
        "causal_materializer_binding_header_v3",
        _one(
            "dependency_record_ref",
            "authority_dependency",
            "causal_materializer_dependency_record_v3",
        ),
        _one(
            "staged_input_evidence_header_ref",
            "authority_dependency",
            "causal_materializer_evidence_header_v3",
            target_evidence_kind="staged_input",
        ),
        _one(
            "producer_request_evidence_header_ref",
            "request_dependency",
            "causal_materializer_evidence_header_v3",
            target_evidence_kind="producer_request",
        ),
        _one(
            "attempt_receipts_evidence_header_ref",
            "history_dependency",
            "causal_materializer_evidence_header_v3",
            target_evidence_kind="attempt_receipts",
        ),
        _one(
            "producer_artifact_evidence_header_ref",
            "authority_dependency",
            "causal_materializer_evidence_header_v3",
            target_evidence_kind="producer_artifact",
        ),
        _one(
            "immutable_history_evidence_header_ref",
            "history_dependency",
            "causal_materializer_evidence_header_v3",
            target_evidence_kind="immutable_history",
        ),
        _one(
            "governed_clock_evidence_header_ref",
            "authority_dependency",
            "causal_materializer_evidence_header_v3",
            target_evidence_kind="governed_clock",
        ),
    ),
    _opaque("canonical_cycle_auxiliary_artifact"),
    _referential_semantic(
        "world_theory_carrier_v3",
        _one(
            "source_ref",
            "semantic_derivation",
            "producer_artifact_evidence",
        ),
        _one(
            "source_receipt_ref",
            "authority_dependency",
            "producer_receipt_evidence",
        ),
    ),
    _referential_semantic(
        "world_precommit_ancestor_carrier_v3",
        _one(
            "precommit_state_ref",
            "history_dependency",
            "immutable_history_evidence",
        ),
        _one(
            "precommit_receipt_ref",
            "authority_dependency",
            "producer_receipt_evidence",
        ),
    ),
    _referential_semantic(
        "world_plan_v3",
        _one(
            "commission_ref",
            "request_dependency",
            "world_matrix_commission_v3",
        ),
    ),
    _referential_semantic(
        "world_no_probe_decision_v3",
        _one("request_ref", "request_dependency", "world_request_v3"),
    ),
    _referential_semantic(
        "world_execution_result_v3",
        _one("request_ref", "observation_dependency", "world_request_v3"),
    ),
    _referential_semantic(
        "world_next_cycle_reflection_v3",
        _one(
            "result_ref",
            "semantic_derivation",
            "world_execution_result_v3",
        ),
    ),
    _referential_semantic(
        "world_projection_component_v3",
        _one(
            "component_payload_ref",
            "semantic_derivation",
            "world_theory_carrier_v3",
            "world_precommit_ancestor_carrier_v3",
            "literature_production_input_bundle",
        ),
    ),
    _referential_semantic(
        "world_projection_index_v3",
        _many(
            "components",
            "semantic_derivation",
            "world_projection_component_v3",
            item_ref_field="object_ref",
        ),
    ),
    _referential_semantic(
        "world_matrix_commission_v3",
        _one(
            "projection_index_ref",
            "authority_dependency",
            "world_projection_index_v3",
        ),
        _one(
            "registered_claim_ref",
            "content_dependency",
            "world_theory_carrier_v3",
        ),
        _one(
            "spec_family_ref",
            "content_dependency",
            "world_theory_carrier_v3",
        ),
        _one(
            "adjudication_materializer_binding_ref",
            "authority_dependency",
            "causal_materializer_binding_header_v3",
        ),
        _one(
            "schedule_materializer_binding_ref",
            "authority_dependency",
            "causal_materializer_binding_header_v3",
        ),
    ),
    _referential_semantic(
        "world_request_v3",
        _one("commission_ref", "request_dependency", "world_matrix_commission_v3"),
        _one(
            "world_plan_ref",
            "content_dependency",
            "world_plan_v3",
        ),
    ),
    _referential_semantic(
        "world_observation_v3",
        _one(
            "commission_ref",
            "observation_dependency",
            "world_matrix_commission_v3",
        ),
        _one("request_ref", "observation_dependency", "world_request_v3"),
        _one(
            "no_probe_decision_ref",
            "content_dependency",
            "world_no_probe_decision_v3",
        ),
        _one(
            "result_ref",
            "content_dependency",
            "world_execution_result_v3",
        ),
        _one(
            "request_materializer_binding_ref",
            "authority_dependency",
            "causal_materializer_binding_header_v3",
        ),
        _one(
            "result_materializer_binding_ref",
            "authority_dependency",
            "causal_materializer_binding_header_v3",
        ),
        _one(
            "reflection_ref",
            "semantic_derivation",
            "world_next_cycle_reflection_v3",
        ),
        _one(
            "reflection_materializer_binding_ref",
            "authority_dependency",
            "causal_materializer_binding_header_v3",
        ),
    ),
    _referential_semantic(
        "world_observation_envelope_v3",
        _one(
            "commission_ref",
            "observation_dependency",
            "world_matrix_commission_v3",
        ),
        _one("observation_ref", "observation_dependency", "world_observation_v3"),
        _one(
            "observation_materializer_binding_ref",
            "authority_dependency",
            "causal_materializer_binding_header_v3",
        ),
        _one(
            "parent_root_ref",
            "history_dependency",
            "world_matrix_anchor_root_v3",
            "world_observation_envelope_v3",
        ),
    ),
    _referential_semantic(
        "world_matrix_certificate_v3",
        _one(
            "commission_ref",
            "aggregation_dependency",
            "world_matrix_commission_v3",
        ),
        _many(
            "observation_envelopes",
            "aggregation_dependency",
            "world_observation_envelope_v3",
            item_ref_field="object_ref",
        ),
    ),
    _referential_semantic(
        "world_matrix_anchor_root_v3",
        _one(
            "literature_input_ref",
            "semantic_derivation",
            "literature_production_input_bundle",
        ),
        _one(
            "projection_index_ref",
            "authority_dependency",
            "world_projection_index_v3",
        ),
        _one(
            "commission_ref",
            "authority_dependency",
            "world_matrix_commission_v3",
        ),
        _one(
            "commission_materializer_binding_ref",
            "authority_dependency",
            "causal_materializer_binding_header_v3",
        ),
        _many(
            "world_requests",
            "request_dependency",
            "world_request_v3",
            item_ref_field="object_ref",
        ),
        _many(
            "world_request_materializer_bindings",
            "authority_dependency",
            "causal_materializer_binding_header_v3",
            item_ref_field="object_ref",
        ),
    ),
    _referential_semantic(
        "world_matrix_aggregation_root_v3",
        _one(
            "anchor_root_ref",
            "history_dependency",
            "world_matrix_anchor_root_v3",
        ),
        _many(
            "observation_envelopes",
            "aggregation_dependency",
            "world_observation_envelope_v3",
            item_ref_field="object_ref",
        ),
        _one(
            "certificate_ref",
            "aggregation_dependency",
            "world_matrix_certificate_v3",
        ),
        _one(
            "certificate_materializer_binding_ref",
            "authority_dependency",
            "causal_materializer_binding_header_v3",
        ),
    ),
    _referential_semantic(
        "world_matrix_descendant_reflection_root_v3",
        _one(
            "aggregation_root_ref",
            "semantic_derivation",
            "world_matrix_aggregation_root_v3",
        ),
    ),
    _semantic(
        "producer_request_evidence",
        "discovery_operator_request.schema.json",
        "validate_operator_request_identity",
    ),
    _semantic(
        "producer_receipt_evidence",
        "discovery_operator_receipt.schema.json",
        "validate_operator_receipt_identity",
    ),
    _opaque("producer_artifact_evidence"),
    _opaque("immutable_history_evidence"),
    _semantic(
        "governed_clock_evidence",
        "dynamic_experiment_governed_clock_evidence_v2.schema.json",
    ),
    _opaque("staged_input_evidence"),
    _header(
        "literature_projection_header",
        _one(
            "literature_input_ref",
            "semantic_derivation",
            "literature_production_input_bundle",
        ),
    ),
    _header(
        "world_authority_projection_header",
        _one(
            "projection_payload_ref",
            "authority_dependency",
            "world_authority_projection",
        ),
        _one(
            "literature_projection_header_ref",
            "semantic_derivation",
            "literature_projection_header",
        ),
        _many(
            "producer_binding_header_refs",
            "authority_dependency",
            "causal_producer_binding_header",
        ),
    ),
    _header(
        "world_matrix_commission_header",
        _one(
            "commission_payload_ref",
            "content_dependency",
            "world_matrix_commission",
        ),
        _one(
            "authority_projection_header_ref",
            "authority_dependency",
            "world_authority_projection_header",
        ),
        _one(
            "commission_producer_binding_header_ref",
            "authority_dependency",
            "causal_producer_binding_header",
        ),
    ),
    _header(
        "world_request_header",
        _one("request_payload_ref", "content_dependency", "world_request"),
        _one(
            "commission_header_ref",
            "request_dependency",
            "world_matrix_commission_header",
        ),
        _one(
            "request_producer_binding_header_ref",
            "authority_dependency",
            "causal_producer_binding_header",
        ),
    ),
    _header(
        "world_observation_header",
        _one(
            "observation_payload_ref",
            "content_dependency",
            "world_observation",
        ),
        _one(
            "envelope_payload_ref",
            "content_dependency",
            "world_observation_envelope",
        ),
        _one(
            "request_header_ref",
            "observation_dependency",
            "world_request_header",
        ),
        _one(
            "observation_producer_binding_header_ref",
            "authority_dependency",
            "causal_producer_binding_header",
        ),
    ),
    _header(
        "world_matrix_aggregation_header",
        _one(
            "certificate_payload_ref",
            "content_dependency",
            "world_matrix_certificate",
        ),
        _one(
            "commission_header_ref",
            "aggregation_dependency",
            "world_matrix_commission_header",
        ),
        _many(
            "observation_header_refs",
            "aggregation_dependency",
            "world_observation_header",
        ),
        _one(
            "aggregation_producer_binding_header_ref",
            "authority_dependency",
            "causal_producer_binding_header",
        ),
    ),
    _header(
        "causal_producer_binding_header",
        _one(
            "binding_payload_ref",
            "content_dependency",
            "causal_producer_binding",
        ),
        _one(
            "producer_request_evidence_header_ref",
            "authority_dependency",
            "producer_evidence_header",
            target_evidence_kind="producer_request",
        ),
        _one(
            "producer_receipt_evidence_header_ref",
            "authority_dependency",
            "producer_evidence_header",
            target_evidence_kind="producer_receipt",
        ),
        _one(
            "producer_artifact_evidence_header_ref",
            "authority_dependency",
            "producer_evidence_header",
            target_evidence_kind="producer_artifact",
        ),
        _one(
            "immutable_history_evidence_header_ref",
            "history_dependency",
            "producer_evidence_header",
            target_evidence_kind="immutable_history",
        ),
        _one(
            "governed_clock_evidence_header_ref",
            "authority_dependency",
            "producer_evidence_header",
            target_evidence_kind="governed_clock",
        ),
        _one(
            "staged_input_evidence_header_ref",
            "authority_dependency",
            "producer_evidence_header",
            target_evidence_kind="staged_input",
        ),
    ),
    _header(
        "producer_evidence_header",
        _one(
            "evidence_payload_ref",
            "content_dependency",
            "producer_request_evidence",
            "producer_receipt_evidence",
            "producer_artifact_evidence",
            "immutable_history_evidence",
            "governed_clock_evidence",
            "staged_input_evidence",
        ),
    ),
)

CONTENT_OBJECT_ROLES: Mapping[str, ContentObjectRole] = MappingProxyType(
    {row.object_kind: row for row in _ROLE_ROWS}
)

_DOMAIN_VALIDATORS = frozenset(
    {
        "validate_portable_literature_production_input_bundle",
        "validate_experiment_authority_projection",
        "validate_experiment_world_matrix_commission_v2",
        "validate_experiment_causal_producer_binding",
        "validate_experiment_world_request",
        "validate_experiment_world_observation",
        "validate_experiment_world_observation_envelope",
        "validate_experiment_world_matrix_certificate_v2",
        "validate_operator_request_identity",
        "validate_operator_receipt_identity",
        "validate_causal_materializer_binding_v3",
    }
)

_EVIDENCE_PAYLOAD_KIND = MappingProxyType(
    {
        "producer_request": "producer_request_evidence",
        "producer_receipt": "producer_receipt_evidence",
        "producer_artifact": "producer_artifact_evidence",
        "immutable_history": "immutable_history_evidence",
        "governed_clock": "governed_clock_evidence",
        "staged_input": "staged_input_evidence",
    }
)

_CAUSAL_MATERIALIZER_EVIDENCE_PAYLOAD_KINDS = MappingProxyType(
    {
        "staged_input": frozenset({"causal_materializer_artifact_evidence_v3"}),
        "producer_request": frozenset({"causal_materializer_request_record_v3"}),
        "attempt_receipts": frozenset({"causal_materializer_attempt_record_v3"}),
        "producer_artifact": frozenset({"causal_materializer_artifact_evidence_v3"}),
        "immutable_history": frozenset({"causal_materializer_artifact_evidence_v3"}),
        "governed_clock": frozenset({"causal_materializer_clock_record_v3"}),
    }
)


def content_object_role(object_kind: str) -> ContentObjectRole:
    """Return one closed role or reject an unregistered storage label."""

    try:
        return CONTENT_OBJECT_ROLES[object_kind]
    except (KeyError, TypeError) as exc:
        raise ContractError(f"unregistered content-object role: {object_kind!r}") from exc


def _without_digest(value: Mapping[str, Any]) -> dict[str, Any]:
    return {key: copy.deepcopy(child) for key, child in value.items() if key != "header_digest"}


def seal_content_object_header(value: Mapping[str, Any]) -> dict[str, Any]:
    """Seal and validate one thin structural header without raising its authority."""

    record = copy.deepcopy(dict(value))
    record.pop("header_digest", None)
    kind = str(record.get("header_kind", ""))
    role = content_object_role(kind)
    if role.authority is not RoleAuthority.STRUCTURAL_REFERENCE:
        raise ContractError("only a structural-reference role can be sealed as a header")
    record["header_digest"] = canonical_digest(record)
    return validate_content_object_payload(kind, record)


def validate_content_object_payload(
    object_kind: str,
    value: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate the schema/shape authorized by a role, never more than that.

    Semantic roles are checked against their exact existing schema here.  Call
    :func:`validate_semantic_content_object_payload` when contextual domain
    invariants—not merely schema conformance—are required.
    """

    if not isinstance(value, Mapping):
        raise ContractError("content-object role payload must be an object")
    role = content_object_role(object_kind)
    record = copy.deepcopy(dict(value))
    canonical_json(record)
    if role.schema_name is not None:
        validate_payload(record, role.schema_name)
    if role.schema_name == WORLD_DOMAIN_V3_SCHEMA:
        if record.get("object_kind") != object_kind:
            raise ContractError("v3 world-domain object kind differs from its storage role")
        if record.get("authority_boundary") != dict(WORLD_V3_AUTHORITY_BOUNDARY):
            raise ContractError("v3 world-domain authority boundary drifted")
        if object_kind == "world_theory_carrier_v3" and (
            record["source_semantic_digest"]
            != record["source_ref"]["semantic_digest"]
        ):
            raise ContractError("theory carrier digest differs from its exact source ref")
        if object_kind == "world_precommit_ancestor_carrier_v3" and (
            record["precommit_state_semantic_digest"]
            != record["precommit_state_ref"]["semantic_digest"]
        ):
            raise ContractError(
                "precommit ancestor digest differs from its exact committed-state ref"
            )
    if role.schema_name == CAUSAL_MATERIALIZER_PORTABLE_RECORD_SCHEMA:
        if record.get("record_kind") != object_kind:
            raise ContractError(
                "portable materializer record kind differs from its storage role"
            )
        if (
            record.get("semantic_authorship") is not False
            or record.get("authority_boundary")
            != CAUSAL_MATERIALIZER_PROTOCOL_AUTHORITY_BOUNDARY
        ):
            raise ContractError(
                "portable materializer record exceeds local protocol authority"
            )
    if role.authority is RoleAuthority.STRUCTURAL_REFERENCE:
        if record.get("header_kind") != object_kind:
            raise ContractError("structural header kind differs from its storage role")
        if record.get("authority_boundary") != dict(HEADER_AUTHORITY_BOUNDARY):
            raise ContractError("structural header authority boundary drifted")
        if record.get("header_digest") != canonical_digest(_without_digest(record)):
            raise ContractError("structural header self-digest is invalid")
        if object_kind == "producer_evidence_header":
            expected = _EVIDENCE_PAYLOAD_KIND.get(str(record.get("evidence_kind")))
            if expected is None or record["evidence_payload_ref"]["object_kind"] != expected:
                raise ContractError("evidence header payload role differs from evidence kind")
        if object_kind == "causal_materializer_evidence_header_v3":
            allowed = _CAUSAL_MATERIALIZER_EVIDENCE_PAYLOAD_KINDS.get(
                str(record.get("evidence_kind"))
            )
            payload_refs = record.get("evidence_payload_refs")
            if (
                allowed is None
                or not isinstance(payload_refs, list)
                or any(ref.get("object_kind") not in allowed for ref in payload_refs)
            ):
                raise ContractError(
                    "portable materializer evidence role differs from its payload roles"
                )
            if record["evidence_kind"] == "attempt_receipts":
                if record.get("successful_attempt") != len(payload_refs):
                    raise ContractError(
                        "portable receipt header does not name its terminal attempt"
                    )
            elif record.get("successful_attempt") is not None:
                raise ContractError(
                    "non-receipt materializer evidence cannot name a successful attempt"
                )
    return record


def require_semantic_content_object_role(object_kind: str) -> ContentObjectRole:
    """Reject opaque and structural roles at a semantic-domain boundary."""

    role = content_object_role(object_kind)
    if role.authority is not RoleAuthority.SEMANTIC_DOMAIN:
        raise ContractError(
            f"content-object role {object_kind!r} carries no semantic-domain authority"
        )
    return role


def _required_context(context: Mapping[str, Any], key: str) -> Any:
    if key not in context:
        raise ContractError(f"semantic domain validator requires context field {key!r}")
    return context[key]


def validate_semantic_content_object_payload(
    object_kind: str,
    value: Mapping[str, Any],
    *,
    context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the closed contextual validator for one semantic-domain role.

    Context is explicit because a request is semantic only relative to its exact
    commission, an envelope relative to that same commission, and a certificate
    relative to all five envelopes.  Missing context fails closed.
    """

    role = require_semantic_content_object_role(object_kind)
    record = validate_content_object_payload(object_kind, value)
    validator_id = role.domain_validator_id
    if validator_id is None:
        return record
    supplied = {} if context is None else context

    if validator_id == "validate_portable_literature_production_input_bundle":
        from agentic.discovery.literature_production_commitment import (
            validate_portable_literature_production_input_bundle,
        )

        return validate_portable_literature_production_input_bundle(record)

    if validator_id in {
        "validate_operator_request_identity",
        "validate_operator_receipt_identity",
    }:
        from agentic.discovery.receipts import (
            validate_operator_receipt_identity,
            validate_operator_request_identity,
        )

        if validator_id == "validate_operator_request_identity":
            validate_operator_request_identity(record)
        else:
            validate_operator_receipt_identity(
                record,
                _required_context(supplied, "producer_request"),
            )
        return record

    if validator_id == "validate_causal_materializer_binding_v3":
        from agentic.experiments.causal_producer_runtime_v3 import (
            validate_causal_materializer_binding_v3,
        )

        return validate_causal_materializer_binding_v3(
            record,
            workspace=_required_context(supplied, "workspace"),
        )

    from agentic.experiments.world_matrix import (
        validate_experiment_authority_projection,
        validate_experiment_causal_producer_binding,
        validate_experiment_world_matrix_certificate_v2,
        validate_experiment_world_matrix_commission_v2,
        validate_experiment_world_observation,
        validate_experiment_world_observation_envelope,
        validate_experiment_world_request,
    )

    evidence_resolver = supplied.get("evidence_resolver")
    if validator_id == "validate_experiment_authority_projection":
        return validate_experiment_authority_projection(record)
    if validator_id == "validate_experiment_causal_producer_binding":
        return validate_experiment_causal_producer_binding(
            record, evidence_resolver=evidence_resolver
        )
    if validator_id == "validate_experiment_world_matrix_commission_v2":
        return validate_experiment_world_matrix_commission_v2(
            record, evidence_resolver=evidence_resolver
        )
    commission = _required_context(supplied, "commission")
    if validator_id == "validate_experiment_world_request":
        return validate_experiment_world_request(
            commission, record, evidence_resolver=evidence_resolver
        )
    if validator_id == "validate_experiment_world_observation":
        return validate_experiment_world_observation(
            commission, record, evidence_resolver=evidence_resolver
        )
    if validator_id == "validate_experiment_world_observation_envelope":
        return validate_experiment_world_observation_envelope(
            commission, record, evidence_resolver=evidence_resolver
        )
    if validator_id == "validate_experiment_world_matrix_certificate_v2":
        return validate_experiment_world_matrix_certificate_v2(
            commission,
            _required_context(supplied, "observation_envelopes"),
            record,
            evidence_resolver=evidence_resolver,
        )
    raise ContractError(f"unimplemented semantic domain validator: {validator_id}")


def validate_role_bound_object(
    object_ref: Mapping[str, Any],
    value: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind role validation to the exact content-addressed ref for ``value``."""

    ref = copy.deepcopy(dict(object_ref))
    validate_payload(ref, CONTENT_OBJECT_REF_SCHEMA)
    record = validate_content_object_payload(str(ref["object_kind"]), value)
    data = canonical_json(record)
    sha256 = bytes_digest(data)
    semantic_digest = canonical_digest(record)
    expected_id = stable_identifier(
        CONTENT_OBJECT_ID_PREFIX,
        ref["object_kind"],
        sha256,
        semantic_digest,
    )
    if (
        ref["size_bytes"] != len(data)
        or ref["sha256"] != sha256
        or ref["semantic_digest"] != semantic_digest
        or ref["object_id"] != expected_id
    ):
        raise ContractError("role payload differs from its exact content-object ref")
    return record


def _declared_refs(
    role: ContentObjectRole,
    payload: Mapping[str, Any],
) -> tuple[tuple[ReferenceDeclaration, Mapping[str, Any]], ...]:
    rows: list[tuple[ReferenceDeclaration, Mapping[str, Any]]] = []
    for declaration in role.references:
        # Closed conditional domain sums may omit references belonging only to
        # the other variant. Schema validation above proves that every omitted
        # field is legal for this exact discriminator before edge derivation.
        if declaration.field not in payload:
            continue
        raw = payload[declaration.field]
        values = raw if declaration.many else [raw]
        for candidate in values:
            if declaration.item_ref_field is not None:
                if not isinstance(candidate, Mapping):
                    raise ContractError(
                        f"reference vector {declaration.field!r} contains a non-object entry"
                    )
                candidate = candidate[declaration.item_ref_field]
            if not isinstance(candidate, Mapping):
                raise ContractError(
                    f"header reference field {declaration.field!r} is not an object ref"
                )
            ref = copy.deepcopy(dict(candidate))
            validate_payload(ref, CONTENT_OBJECT_REF_SCHEMA)
            if ref["object_kind"] not in declaration.allowed_target_kinds:
                raise ContractError(
                    f"header reference field {declaration.field!r} names role "
                    f"{ref['object_kind']!r} outside its closed target set"
                )
            rows.append((declaration, ref))
    return tuple(rows)


def _validate_world_v3_cross_object_discriminators(
    by_id: Mapping[str, tuple[dict[str, Any], dict[str, Any]]],
) -> None:
    """Reject role-correct refs that launder the wrong semantic carrier.

    Content refs intentionally contain storage kind, not payload discriminators.
    Once exact referenced bytes are present, the full role-object set can also
    prove that projection and commission fields name the required carrier kind.
    Arithmetic ancestry and immediately-prior envelope identity remain duties
    of canonical replay, where the surrounding committed generation exists.
    """

    def payload_for(ref: Mapping[str, Any]) -> dict[str, Any]:
        return by_id[str(ref["object_id"])][1]

    for object_ref, payload in by_id.values():
        object_kind = str(object_ref["object_kind"])
        if object_kind == "world_projection_component_v3":
            component_kind = str(payload["component_kind"])
            source = payload_for(payload["component_payload_ref"])
            if (
                component_kind
                not in {"committed_ancestor", "source_authority"}
                and source.get("carrier_kind") != component_kind
            ):
                raise ContractError(
                    "projection component ref launders a different theory carrier kind"
                )
        elif object_kind == "world_matrix_commission_v3":
            registered_claim = payload_for(payload["registered_claim_ref"])
            spec_family = payload_for(payload["spec_family_ref"])
            if registered_claim.get("carrier_kind") != "registered_claim":
                raise ContractError(
                    "commission registered-claim ref launders another theory carrier"
                )
            if spec_family.get("carrier_kind") != "experiment_spec_family":
                raise ContractError(
                    "commission spec-family ref launders another theory carrier"
                )
        elif object_kind == "world_projection_index_v3":
            component_payloads = {
                str(entry["component_kind"]): payload_for(entry["object_ref"])
                for entry in payload["components"]
            }
            ancestor_component = component_payloads["committed_ancestor"]
            ancestor = payload_for(ancestor_component["component_payload_ref"])
            if (
                ancestor["precommit_state_version"] != payload["prior_state_version"]
                or ancestor["target_id"] != payload["target_id"]
                or ancestor["run_id"] != payload["run_id"]
            ):
                raise ContractError(
                    "projection precommit ancestor differs from its N-1 scalar identity"
                )


def derive_content_object_edges(
    *,
    object_ref: Mapping[str, Any],
    payload: Mapping[str, Any],
) -> tuple[dict[str, str], ...]:
    """Derive every knowable prerequisite edge for one role-bound object."""

    record = validate_role_bound_object(object_ref, payload)
    role = content_object_role(str(object_ref["object_kind"]))
    edges: list[dict[str, str]] = []
    keys: set[tuple[str, str, str]] = set()
    for declaration, source_ref in _declared_refs(role, record):
        key = (
            str(source_ref["object_id"]),
            str(object_ref["object_id"]),
            declaration.edge_kind,
        )
        if key in keys:
            raise ContractError("payload derives a duplicate typed content-object edge")
        keys.add(key)
        edges.append(
            {
                "source_object_id": key[0],
                "target_object_id": key[1],
                "edge_kind": key[2],
            }
        )
    return tuple(edges)


def validate_payload_derived_edges(
    *,
    objects: Sequence[tuple[Mapping[str, Any], Mapping[str, Any]]],
    declared_edges: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, str], ...]:
    """Require the declared edge set to equal all payload-derived references.

    Opaque and legacy semantic roles without declared content refs remain valid
    storage objects, but they cannot acquire graph authority by naming an edge.
    Every declared arrow is therefore checked, including arrows whose target
    has no reference declarations.  A future non-payload edge mechanism must
    enter through its own closed authority object rather than being silently
    ignored here.
    """

    by_id: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    expected: list[dict[str, str]] = []
    reference_targets: set[str] = set()
    for raw_ref, raw_payload in objects:
        ref = copy.deepcopy(dict(raw_ref))
        payload = validate_role_bound_object(ref, raw_payload)
        object_id = str(ref["object_id"])
        if object_id in by_id:
            raise ContractError("role-object set contains a duplicate object ID")
        by_id[object_id] = (ref, payload)
        role = content_object_role(str(ref["object_kind"]))
        if role.references:
            reference_targets.add(object_id)
            expected.extend(derive_content_object_edges(object_ref=ref, payload=payload))

    # Embedded refs must resolve to the exact supplied object ref.  Binding
    # evidence fields additionally prove their six distinct evidence roles.
    for target_id in reference_targets:
        target_ref, target_payload = by_id[target_id]
        role = content_object_role(str(target_ref["object_kind"]))
        for declaration, embedded_ref in _declared_refs(role, target_payload):
            source_id = str(embedded_ref["object_id"])
            if source_id not in by_id or by_id[source_id][0] != embedded_ref:
                raise ContractError("header reference lacks one exact supplied role object")
            if declaration.target_evidence_kind is not None:
                source_payload = by_id[source_id][1]
                if source_payload.get("evidence_kind") != declaration.target_evidence_kind:
                    raise ContractError(
                        "binding header evidence field resolves to the wrong evidence kind"
                    )

    _validate_world_v3_cross_object_discriminators(by_id)

    # Account for every caller-declared edge.  Filtering by reference-bearing
    # targets would let an opaque target manufacture reachability without a
    # payload reference, which turns a finite dependency diagram into a
    # caller-authored graph.
    actual_keys: list[tuple[str, str, str]] = []
    for raw in declared_edges:
        if not isinstance(raw, Mapping) or set(raw) != {
            "source_object_id",
            "target_object_id",
            "edge_kind",
        }:
            raise ContractError("declared content-object edge has noncanonical fields")
        if any(
            not isinstance(raw[field], str)
            for field in ("source_object_id", "target_object_id", "edge_kind")
        ):
            raise ContractError("declared content-object edge fields must be strings")
        key = (
            raw["source_object_id"],
            raw["target_object_id"],
            raw["edge_kind"],
        )
        if key[2] not in _EDGE_KINDS:
            raise ContractError("declared content-object edge has an unknown kind")
        if key[0] not in by_id or key[1] not in by_id:
            raise ContractError("declared content-object edge names an unsupplied object")
        if key[0] == key[1]:
            raise ContractError("declared content-object edge cannot be a self-edge")
        actual_keys.append(key)
    if len(actual_keys) != len(set(actual_keys)):
        raise ContractError("declared content-object edges contain a duplicate typed edge")
    expected_keys = [
        (row["source_object_id"], row["target_object_id"], row["edge_kind"])
        for row in expected
    ]
    extra = set(actual_keys) - set(expected_keys)
    if extra:
        raise ContractError(
            "declared content-object edge is not payload-derived or separately authorized"
        )
    if set(expected_keys) - set(actual_keys):
        raise ContractError(
            "declared content-object edges omit a payload-derived reference"
        )
    return tuple(copy.deepcopy(expected))


def validate_content_object_role_registry() -> None:
    """Replay closure and authority invariants for the immutable registry."""

    if len(CONTENT_OBJECT_ROLES) != len(_ROLE_ROWS):
        raise ContractError("content-object role registry contains duplicate kinds")
    for object_kind, role in CONTENT_OBJECT_ROLES.items():
        validate_payload(object_kind, CONTENT_OBJECT_KIND_SCHEMA)
        if role.object_kind != object_kind:
            raise ContractError("content-object role registry key drifted")
        if role.authority is RoleAuthority.OPAQUE_STORAGE:
            if role.domain_validator_id is not None:
                raise ContractError("opaque storage role cannot claim a domain validator")
            if role.schema_name not in {
                None,
                CAUSAL_MATERIALIZER_PORTABLE_RECORD_SCHEMA,
            }:
                raise ContractError(
                    "typed opaque storage role names an unapproved shape schema"
                )
        elif role.schema_name is None:
            raise ContractError("non-opaque content-object role lacks an exact schema")
        if role.authority is RoleAuthority.STRUCTURAL_REFERENCE:
            if role.schema_name not in {
                CONTENT_OBJECT_HEADER_SCHEMA,
                CAUSAL_MATERIALIZER_PORTABLE_HEADER_SCHEMA,
            } or not role.references:
                raise ContractError("structural role lacks an exact header/ref contract")
        if (
            role.domain_validator_id is not None
            and role.domain_validator_id not in _DOMAIN_VALIDATORS
        ):
            raise ContractError("content-object role names an unknown domain validator")
        for declaration in role.references:
            if declaration.edge_kind not in _EDGE_KINDS:
                raise ContractError("role reference names an unknown graph edge kind")
            if not declaration.allowed_target_kinds:
                raise ContractError("role reference has an empty target-role set")
            if not declaration.allowed_target_kinds.issubset(CONTENT_OBJECT_ROLES):
                raise ContractError("role reference names an unregistered target kind")
            if declaration.item_ref_field is not None and not declaration.many:
                raise ContractError("nested reference extraction requires a repeated field")


validate_content_object_role_registry()


__all__ = [
    "CAUSAL_MATERIALIZER_PORTABLE_HEADER_SCHEMA",
    "CAUSAL_MATERIALIZER_PORTABLE_RECORD_SCHEMA",
    "CAUSAL_MATERIALIZER_PROTOCOL_AUTHORITY_BOUNDARY",
    "CONTENT_OBJECT_HEADER_SCHEMA",
    "CONTENT_OBJECT_KIND_SCHEMA",
    "CONTENT_OBJECT_ROLES",
    "ContentObjectRole",
    "HEADER_AUTHORITY_BOUNDARY",
    "ReferenceDeclaration",
    "RoleAuthority",
    "WORLD_DOMAIN_V3_SCHEMA",
    "WORLD_V3_AUTHORITY_BOUNDARY",
    "content_object_role",
    "derive_content_object_edges",
    "require_semantic_content_object_role",
    "seal_content_object_header",
    "validate_content_object_payload",
    "validate_content_object_role_registry",
    "validate_payload_derived_edges",
    "validate_role_bound_object",
    "validate_semantic_content_object_payload",
]
