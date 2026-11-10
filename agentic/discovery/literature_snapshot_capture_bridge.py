# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Replay a typed lineage from retained search bytes to a semantic snapshot.

A raw search capture and a canonical semantic literature snapshot answer
different integrity questions.  The raw SHA-256 identifies the bytes actually
retained from search; the semantic content digest identifies normalized source
records consumed by the discovery runtime.  This module links those roots
without pretending that their hashes, data models, or authority are equal.

The bridge proves a deliberately bounded derivation: every raw result whose
disposition begins with ``included`` has exactly one semantic source with the
same source identifier, URL, and lane membership; every other raw result is
absent; lane types, queries, and coverage cutoff replay; and semantic
materialization occurs after capture completion.  Authors, claims,
interpretive warrants, and display-title normalization remain properties of
the independently validated semantic root, not facts inferred from raw search
metadata.
"""

from __future__ import annotations

import copy
import datetime as dt
from collections.abc import Mapping
from typing import Any

from .conceptual_ancestry_v3 import (
    validate_bounded_current_literature_bundle,
)
from .contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    validate_payload,
)
from .literature import validate_snapshot


SCHEMA_VERSION = "1.0.0"
ARTIFACT_KIND = "literature_snapshot_capture_bridge"
DERIVATION_RELATION = (
    "semantic_snapshot_is_selection_identity_projection_of_retained_raw_capture"
)
SELECTION_RULE = "raw_disposition_prefix_included_v1"
SOURCE_IDENTITY_RULE = "exact_source_id_url_and_lane_membership_v1"
NORMALIZATION_SCOPE = (
    "display_and_semantic_enrichment_remain_semantic_root_only"
)
ROOT_RELATION = (
    "cryptographically_distinct_roots_linked_by_replayed_derivation"
)
AUTHORITY = {
    "raw_capture_byte_identity": True,
    "semantic_snapshot_validation": True,
    "selection_bijection": True,
    "source_locator_bijection": True,
    "semantic_enrichment_from_capture_authority": None,
    "source_truth_authority": None,
    "global_latestness_authority": None,
    "exhaustiveness_authority": None,
    "proof_authority": None,
    "world_authority": None,
}
AUTHORITY_BOUNDARY = (
    "This bridge proves only that one exact validated semantic snapshot root is "
    "a post-capture selection, source-identity, URL, and lane projection of one "
    "exact retained raw-capture byte root. It keeps both roots distinct and "
    "makes no hash-equality claim. Display normalization, authorship metadata, "
    "claims, limitations, semantic warrants, source truth, global latestness, "
    "exhaustiveness, proof, and world truth do not derive from this bridge."
)
_SCHEMA_NAME = "literature_snapshot_capture_bridge_v1.schema.json"


class LiteratureSnapshotCaptureBridgeError(ContractError):
    """Carry a stable rejection code for bridge construction and replay."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(
            f"literature_snapshot_capture_bridge[{reason_code}]: {message}"
        )


def _fail(reason_code: str, message: str) -> None:
    raise LiteratureSnapshotCaptureBridgeError(reason_code, message)


def _timestamp(value: Any, label: str) -> dt.datetime:
    """Parse one timezone-explicit instant for cross-root ordering checks."""

    if not isinstance(value, str):
        _fail("timestamp_invalid", f"{label} must be a timestamp string")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise LiteratureSnapshotCaptureBridgeError(
            "timestamp_invalid", f"{label} is not an ISO date-time"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        _fail("timestamp_invalid", f"{label} must carry a timezone")
    return parsed.astimezone(dt.UTC)


def _validated_inputs(
    literature_bundle: Mapping[str, Any],
    semantic_snapshot: Mapping[str, Any],
    *,
    present_use_at: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate both authority roots before deriving any relationship."""

    try:
        bundle = validate_bounded_current_literature_bundle(
            literature_bundle, present_use_at=present_use_at
        )
        snapshot = copy.deepcopy(dict(semantic_snapshot))
        validate_snapshot(snapshot)
    except ContractError as exc:
        raise LiteratureSnapshotCaptureBridgeError(
            "input_contract_invalid",
            f"raw bundle or semantic snapshot is invalid: {exc}",
        ) from exc
    if snapshot["validation_status"] != "validated":
        _fail(
            "semantic_snapshot_unvalidated",
            "the semantic root must carry validated snapshot status",
        )
    return bundle, snapshot


def _capture_lane_membership(
    capture: Mapping[str, Any],
) -> dict[str, list[str]]:
    """Reconstruct the exact raw-result-to-lane relation."""

    membership = {
        str(row["result_id"]): [] for row in capture["raw_results"]
    }
    for lane in capture["lanes"]:
        for result_id in lane["raw_result_ids"]:
            membership[str(result_id)].append(str(lane["lane_id"]))
    return {
        result_id: sorted(lane_ids)
        for result_id, lane_ids in membership.items()
    }


def _derive_bridge_core(
    literature_bundle: Mapping[str, Any],
    semantic_snapshot: Mapping[str, Any],
    *,
    present_use_at: str | None,
) -> dict[str, Any]:
    """Derive all bridge rows from the two independently validated roots."""

    bundle, snapshot = _validated_inputs(
        literature_bundle,
        semantic_snapshot,
        present_use_at=present_use_at,
    )
    capture = bundle["capture"]
    capture_descriptor = bundle["capture_descriptor"]
    raw_sha256 = capture_descriptor["sha256"]
    semantic_digest = snapshot["content_digest"]
    if raw_sha256 == semantic_digest:
        _fail(
            "root_hash_conflation",
            "raw bytes and semantic snapshot must remain non-equal roots",
        )
    if bundle["target_id"] != snapshot["target_id"]:
        _fail(
            "target_mismatch",
            "raw capture and semantic snapshot target different problems",
        )
    if _timestamp(
        capture["coverage_cutoff"], "raw capture coverage cutoff"
    ) != _timestamp(snapshot["coverage_cutoff"], "semantic coverage cutoff"):
        _fail(
            "coverage_cutoff_mismatch",
            "semantic snapshot does not retain the raw capture cutoff instant",
        )
    capture_completed = _timestamp(
        capture["capture_completed_at"], "raw capture completion"
    )
    if _timestamp(
        snapshot["search_started_at"], "semantic snapshot start"
    ) < capture_completed:
        _fail(
            "temporal_order_invalid",
            "semantic materialization predates raw capture completion",
        )

    raw_results = [copy.deepcopy(dict(row)) for row in capture["raw_results"]]
    raw_result_ids = [str(row["result_id"]) for row in raw_results]
    raw_source_ids = [str(row["source_id"]) for row in raw_results]
    if len(raw_result_ids) != len(set(raw_result_ids)) or len(
        raw_source_ids
    ) != len(set(raw_source_ids)):
        _fail(
            "raw_source_identity_ambiguous",
            "bridge v1 requires unique raw result and source identifiers",
        )
    semantic_sources = [
        copy.deepcopy(dict(row)) for row in snapshot["sources"]
    ]
    semantic_source_ids = [str(row["source_id"]) for row in semantic_sources]
    if len(semantic_source_ids) != len(set(semantic_source_ids)):
        _fail(
            "semantic_source_identity_ambiguous",
            "semantic snapshot repeats a source identifier",
        )

    included_results = [
        row
        for row in raw_results
        if str(row["disposition"]).startswith("included")
    ]
    excluded_results = [
        row
        for row in raw_results
        if not str(row["disposition"]).startswith("included")
    ]
    if not included_results:
        _fail(
            "included_source_bijection_invalid",
            "raw capture has no results admitted by the inclusion rule",
        )
    included_source_ids = {
        str(row["source_id"]) for row in included_results
    }
    if included_source_ids != set(semantic_source_ids):
        _fail(
            "included_source_bijection_invalid",
            "included raw source IDs and semantic source IDs are not bijective",
        )
    if {
        str(row["source_id"]) for row in excluded_results
    } & set(semantic_source_ids):
        _fail(
            "excluded_source_leak",
            "an excluded raw result entered the semantic source set",
        )

    raw_by_result_id = {
        str(row["result_id"]): row for row in raw_results
    }
    raw_by_source_id = {
        str(row["source_id"]): row for row in raw_results
    }
    semantic_by_source_id = {
        str(row["source_id"]): row for row in semantic_sources
    }
    membership = _capture_lane_membership(capture)
    capture_lanes = {
        str(row["lane_id"]): copy.deepcopy(dict(row))
        for row in capture["lanes"]
    }
    semantic_lanes = {
        str(row["lane_id"]): copy.deepcopy(dict(row))
        for row in snapshot["lane_receipts"]
    }
    if set(capture_lanes) != set(semantic_lanes):
        _fail(
            "lane_bijection_invalid",
            "capture lanes and semantic lane receipts are not bijective",
        )

    lane_bindings: list[dict[str, Any]] = []
    for lane_id in sorted(capture_lanes):
        capture_lane = capture_lanes[lane_id]
        semantic_lane = semantic_lanes[lane_id]
        lane_results = [
            raw_by_result_id[str(result_id)]
            for result_id in capture_lane["raw_result_ids"]
        ]
        expected_source_ids = sorted(
            str(row["source_id"])
            for row in lane_results
            if str(row["disposition"]).startswith("included")
        )
        expected_excluded_ids = sorted(
            str(row["result_id"])
            for row in lane_results
            if not str(row["disposition"]).startswith("included")
        )
        if (
            semantic_lane["lane_type"] != capture_lane["lane_type"]
            or semantic_lane["queries"] != capture_lane["queries"]
            or sorted(semantic_lane["source_ids"]) != expected_source_ids
            or semantic_lane["result_count"] != len(expected_source_ids)
            or semantic_lane["status"] != "completed"
            or _timestamp(
                semantic_lane["coverage_cutoff"],
                f"semantic lane {lane_id} cutoff",
            )
            != _timestamp(
                capture["coverage_cutoff"], "raw capture coverage cutoff"
            )
        ):
            _fail(
                "lane_projection_mismatch",
                f"semantic lane {lane_id!r} does not replay capture selection",
            )
        lane_bindings.append(
            {
                "lane_id": lane_id,
                "lane_type": str(capture_lane["lane_type"]),
                "capture_lane_digest": canonical_digest(capture_lane),
                "semantic_lane_digest": semantic_lane["content_digest"],
                "queries_digest": canonical_digest(capture_lane["queries"]),
                "included_source_ids": expected_source_ids,
                "excluded_result_ids": expected_excluded_ids,
            }
        )

    source_bindings: list[dict[str, Any]] = []
    for source_id in sorted(included_source_ids):
        raw_result = raw_by_source_id[source_id]
        semantic_source = semantic_by_source_id[source_id]
        capture_lane_ids = membership[str(raw_result["result_id"])]
        semantic_lane_ids = sorted(semantic_source["lane_ids"])
        if capture_lane_ids != semantic_lane_ids:
            _fail(
                "source_lane_mismatch",
                f"source {source_id!r} changed lane membership",
            )
        raw_url = str(raw_result["url"])
        semantic_url = str(semantic_source["url"])
        if raw_url != semantic_url:
            _fail(
                "source_locator_mismatch",
                f"source {source_id!r} changed its retained URL",
            )
        source_bindings.append(
            {
                "result_id": str(raw_result["result_id"]),
                "source_id": source_id,
                "raw_result_digest": canonical_digest(raw_result),
                "semantic_source_digest": semantic_source["content_digest"],
                "shared_locator_digest": canonical_digest(
                    {"source_id": source_id, "url": raw_url}
                ),
                "raw_url": raw_url,
                "semantic_url": semantic_url,
                "raw_title_digest": canonical_digest(raw_result["title"]),
                "semantic_title_digest": canonical_digest(
                    semantic_source["title"]
                ),
                "title_relation": (
                    "exact"
                    if raw_result["title"] == semantic_source["title"]
                    else "normalized_display_only"
                ),
                "capture_lane_ids": capture_lane_ids,
                "semantic_lane_ids": semantic_lane_ids,
            }
        )

    excluded_bindings = [
        {
            "result_id": str(row["result_id"]),
            "source_id": str(row["source_id"]),
            "disposition": str(row["disposition"]),
            "claim_status": str(row["claim_status"]),
            "raw_result_digest": canonical_digest(row),
            "capture_lane_ids": membership[str(row["result_id"])],
            "semantic_source_absent": True,
        }
        for row in sorted(
            excluded_results, key=lambda item: str(item["result_id"])
        )
    ]
    raw_root = {
        "literature_bundle_id": bundle["bundle_id"],
        "literature_bundle_digest": bundle["content_digest"],
        "capture_id": capture["capture_id"],
        "target_id": bundle["target_id"],
        "sha256": raw_sha256,
        "byte_length": capture_descriptor["byte_length"],
        "capture_completed_at": capture["capture_completed_at"],
        "coverage_cutoff": capture["coverage_cutoff"],
        "lane_count": len(capture_lanes),
        "raw_result_count": len(raw_results),
    }
    semantic_root = {
        "snapshot_id": snapshot["snapshot_id"],
        "target_id": snapshot["target_id"],
        "content_digest": semantic_digest,
        "theory_state_digest": snapshot["theory_state_digest"],
        "search_started_at": snapshot["search_started_at"],
        "search_completed_at": snapshot["search_completed_at"],
        "coverage_cutoff": snapshot["coverage_cutoff"],
        "provenance_mode": snapshot["provenance_mode"],
        "validation_status": snapshot["validation_status"],
        "lane_count": len(semantic_lanes),
        "source_count": len(semantic_sources),
    }
    derivation = {
        "relation": DERIVATION_RELATION,
        "selection_rule": SELECTION_RULE,
        "source_identity_rule": SOURCE_IDENTITY_RULE,
        "normalization_scope": NORMALIZATION_SCOPE,
        "included_source_bijection": "exact",
        "coverage_cutoff_relation": "same_instant",
        "temporal_order": (
            "semantic_snapshot_materialized_not_before_capture_completion"
        ),
        "lane_bindings": lane_bindings,
        "source_bindings": source_bindings,
        "excluded_bindings": excluded_bindings,
    }
    derivation["projection_digest"] = canonical_digest(
        {
            "raw_capture_root": raw_root,
            "semantic_snapshot_root": semantic_root,
            **derivation,
        }
    )
    bridge_id = stable_identifier(
        "literature-snapshot-capture-bridge",
        raw_sha256,
        semantic_digest,
        derivation["projection_digest"],
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": ARTIFACT_KIND,
        "bridge_id": bridge_id,
        "target_id": bundle["target_id"],
        "run_id": bundle["run_id"],
        "state_version": bundle["state_version"],
        "raw_capture_root": raw_root,
        "semantic_snapshot_root": semantic_root,
        "derivation": derivation,
        "root_separation": {
            "relation": ROOT_RELATION,
            "raw_capture_sha256": raw_sha256,
            "semantic_snapshot_content_digest": semantic_digest,
            "roots_distinct": True,
            "hash_equality_claim": False,
        },
        "authority": copy.deepcopy(AUTHORITY),
        "authority_boundary": AUTHORITY_BOUNDARY,
    }


def _seal(core: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(core))
    value["content_digest"] = canonical_digest(value)
    return value


def build_literature_snapshot_capture_bridge(
    *,
    literature_bundle: Mapping[str, Any],
    semantic_snapshot: Mapping[str, Any],
    present_use_at: str | None = None,
) -> dict[str, Any]:
    """Build one exact two-root derivation artifact.

    ``literature_bundle`` supplies the retained raw UTF-8 bytes and their
    bounded currentness contract.  ``semantic_snapshot`` supplies the
    independently validated normalized root.  ``present_use_at`` is optional;
    when supplied it rechecks the bounded bundle's consumption window rather
    than replacing its recorded time.
    """

    bridge = _seal(
        _derive_bridge_core(
            literature_bundle,
            semantic_snapshot,
            present_use_at=present_use_at,
        )
    )
    return validate_literature_snapshot_capture_bridge(
        bridge,
        literature_bundle=literature_bundle,
        semantic_snapshot=semantic_snapshot,
        present_use_at=present_use_at,
    )


def validate_literature_snapshot_capture_bridge(
    bridge: Mapping[str, Any],
    *,
    literature_bundle: Mapping[str, Any],
    semantic_snapshot: Mapping[str, Any],
    present_use_at: str | None = None,
) -> dict[str, Any]:
    """Replay a bridge from both exact roots and reject detached certificates."""

    value = copy.deepcopy(dict(bridge))
    try:
        validate_payload(value, _SCHEMA_NAME)
    except ContractError as exc:
        raise LiteratureSnapshotCaptureBridgeError(
            "bridge_schema_invalid", str(exc)
        ) from exc
    if (
        value["raw_capture_root"]["sha256"]
        == value["semantic_snapshot_root"]["content_digest"]
        or value["root_separation"]["raw_capture_sha256"]
        == value["root_separation"]["semantic_snapshot_content_digest"]
    ):
        _fail(
            "root_hash_conflation",
            "bridge artifact equates raw and semantic hash roots",
        )
    expected_digest = canonical_digest(
        {
            key: item
            for key, item in value.items()
            if key != "content_digest"
        }
    )
    if value["content_digest"] != expected_digest:
        _fail("bridge_digest_mismatch", "bridge content digest does not replay")
    expected = _seal(
        _derive_bridge_core(
            literature_bundle,
            semantic_snapshot,
            present_use_at=present_use_at,
        )
    )
    if value != expected:
        _fail(
            "bridge_replay_mismatch",
            "bridge differs from the exact raw-to-semantic derivation replay",
        )
    return copy.deepcopy(value)


__all__ = [
    "ARTIFACT_KIND",
    "AUTHORITY",
    "AUTHORITY_BOUNDARY",
    "DERIVATION_RELATION",
    "LiteratureSnapshotCaptureBridgeError",
    "NORMALIZATION_SCOPE",
    "ROOT_RELATION",
    "SCHEMA_VERSION",
    "SELECTION_RULE",
    "SOURCE_IDENTITY_RULE",
    "build_literature_snapshot_capture_bridge",
    "validate_literature_snapshot_capture_bridge",
]
