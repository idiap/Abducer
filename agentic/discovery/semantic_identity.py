# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Canonical semantic identities for conceptual-system comparison.

The projection in this module deliberately removes transport, producer, and
record identities while retaining the content that gives a conceptual system
its explanatory shape.  It is an integrity surface, not an automated novelty
judge: a digest can establish that two projected contents are equal or
different, but only receipt-bound conceptual adjudication may interpret a
difference as philosophically material.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping, Sequence
from typing import Any

from .contracts import canonical_digest


SEMANTIC_SIGNATURE_VERSION = "1.1.0"

_PROCESS_FIELDS = frozenset(
    {
        "adjudicator_id",
        "candidate_alias",
        "claimed_score",
        "created_at",
        "created_utc",
        "evaluation_score",
        "expected_winner",
        "lifecycle_state",
        "preferred_candidate",
        "preferred_system_id",
        "producer_identity",
        "proposer_identity",
        "round_id",
        "selected_candidate_alias",
        "selected_system_id",
        "self_assessment",
        "structural_identity",
        "system_id",
        "winner",
    }
)
# ``relation`` is usually theoretical content: changing ``causes`` to
# ``prevents`` must change semantic identity.  It is process metadata only when
# nested under one of these explicitly named transport envelopes.  The path
# qualification prevents a globally named field from silently erasing polarity.
_PROCESS_METADATA_CONTAINERS = frozenset(
    {"execution_metadata", "process_metadata", "transport_metadata"}
)
_REFERENCE_FIELDS = frozenset(
    {
        "conceptual_ancestors",
        "genealogy_ids",
        "parent_system_ids",
        "source_case_id",
        "source_case_ids",
        "source_system",
        "source_system_id",
        "source_system_ids",
        "target_system",
        "target_system_id",
    }
)
_WHITESPACE = re.compile(r"\s+")


def _normal_text(value: str, identity_tokens: Sequence[str]) -> str:
    text = unicodedata.normalize("NFKC", value)
    for token in sorted({item for item in identity_tokens if item}, key=len, reverse=True):
        text = text.replace(token, "@system-reference")
    return _WHITESPACE.sub(" ", text).strip().casefold()


def _reference_shape(value: Any) -> Any:
    """Preserve reference arity and container shape without preserving labels."""

    if isinstance(value, Mapping):
        return {"reference_count": len(value), "container": "mapping"}
    if isinstance(value, (list, tuple)):
        return {"reference_count": len(value), "container": "sequence"}
    if value is None:
        return None
    return "@reference"


def semantic_projection(
    value: Any,
    *,
    identity_tokens: Sequence[str] = (),
    field_name: str | None = None,
    field_path: tuple[str, ...] = (),
) -> Any:
    """Return a canonical, ID-insensitive semantic projection.

    Arrays are treated as unordered semantic collections.  Where order matters,
    the conceptual contract must represent it through an explicit typed relation
    or ordinal field rather than relying on JSON transport order.
    """

    if field_name in _REFERENCE_FIELDS or (
        field_name is not None
        and (field_name.endswith("_id") or field_name.endswith("_ids"))
    ):
        return _reference_shape(value)
    if isinstance(value, Mapping):
        projected: dict[str, Any] = {}
        for raw_key, child in value.items():
            key = str(raw_key)
            if key in _PROCESS_FIELDS or (
                key == "relation"
                and bool(field_path)
                and field_path[-1] in _PROCESS_METADATA_CONTAINERS
            ):
                continue
            if key.endswith("_digest") or key.endswith("_receipt_id") or key.endswith(
                "_receipt_ids"
            ):
                continue
            projected[key] = semantic_projection(
                child,
                identity_tokens=identity_tokens,
                field_name=key,
                field_path=(*field_path, key),
            )
        return projected
    if isinstance(value, (list, tuple)):
        rows = [
            semantic_projection(
                item,
                identity_tokens=identity_tokens,
                field_name=field_name,
                field_path=field_path,
            )
            for item in value
        ]
        return sorted(rows, key=canonical_digest)
    if isinstance(value, str):
        return _normal_text(value, identity_tokens)
    return value


def _topology_material(projection: Mapping[str, Any]) -> dict[str, Any]:
    unification = projection.get("unification_claims", {})
    if not isinstance(unification, Mapping):
        unification = {}
    mappings = unification.get("mappings", [])
    transition = unification.get("explanatory_graph_transition", {})
    if not isinstance(transition, Mapping):
        transition = {}
    return {
        "primitive_count": len(projection.get("primitives", [])),
        "ontological_commitment_count": len(
            projection.get("ontological_commitments", [])
        ),
        "relation_or_dynamic_count": len(
            projection.get("relations_operations_and_dynamics", [])
        ),
        "target_pressure_count": len(projection.get("target_pressures_addressed", [])),
        "unification_mapping_count": len(mappings) if isinstance(mappings, list) else 0,
        "unification_kind": unification.get("unification_kind"),
        "added_node_count": len(transition.get("added_nodes", [])),
        "added_edge_count": len(transition.get("added_edges", [])),
        "new_dependency_count": len(
            transition.get("new_explanatory_dependencies", [])
        ),
    }


def semantic_signature(
    system: Mapping[str, Any], *, identity_tokens: Sequence[str] = ()
) -> dict[str, Any]:
    """Build a terminology-bearing but system-ID-insensitive content signature."""

    projection = semantic_projection(dict(system), identity_tokens=identity_tokens)
    role_digests = {
        key: canonical_digest(value)
        for key, value in sorted(projection.items())
    }
    topology_material = _topology_material(projection)
    core = {
        "schema_version": SEMANTIC_SIGNATURE_VERSION,
        "projection_digest": canonical_digest(projection),
        "semantic_role_digests": role_digests,
        "topology_digest": canonical_digest(topology_material),
        "identity_policy": {
            "system_and_process_ids_excluded": True,
            "collection_order_ignored": True,
            "semantic_text_retained": True,
            "theoretical_relation_polarity_retained": True,
        },
    }
    return {**core, "signature_digest": canonical_digest(core)}


def semantic_signature_closure(
    systems: Sequence[Mapping[str, Any]],
    genealogy: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Bind candidate and frozen-genealogy semantic signature multisets."""

    system_ids = [str(row.get("system_id", "")) for row in systems]
    genealogy_ids = [
        str(row.get("conceptual_system_id") or row.get("system_id") or row.get("id") or "")
        for row in genealogy
    ]
    identity_tokens = sorted({*system_ids, *genealogy_ids} - {""})
    candidate_rows = [
        {
            "system_id": str(system["system_id"]),
            "system_digest": canonical_digest(dict(system)),
            "semantic_signature": semantic_signature(
                system, identity_tokens=identity_tokens
            ),
        }
        for system in sorted(systems, key=lambda row: str(row["system_id"]))
    ]
    genealogy_rows = [
        {
            "record_index": index,
            "record_digest": canonical_digest(dict(record)),
            "semantic_signature": semantic_signature(
                record, identity_tokens=identity_tokens
            ),
        }
        for index, record in enumerate(genealogy)
    ]
    core = {
        "schema_version": SEMANTIC_SIGNATURE_VERSION,
        "candidate_signatures": candidate_rows,
        "genealogy_signatures": genealogy_rows,
        "candidate_signature_multiset_digest": canonical_digest(
            sorted(
                row["semantic_signature"]["signature_digest"]
                for row in candidate_rows
            )
        ),
        "genealogy_signature_multiset_digest": canonical_digest(
            sorted(
                row["semantic_signature"]["signature_digest"]
                for row in genealogy_rows
            )
        ),
    }
    return {**core, "closure_digest": canonical_digest(core)}


__all__ = [
    "SEMANTIC_SIGNATURE_VERSION",
    "semantic_projection",
    "semantic_signature",
    "semantic_signature_closure",
]
