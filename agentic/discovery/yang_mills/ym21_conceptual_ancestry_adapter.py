# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Exact Yang--Mills 2026-07-21 adapter for conceptual ancestry v3.

The generic ancestry contract accepts any exact retained frozen capture with a
registered latest-allowed date and an optional registered method-only lane.
This module owns the target-specific closure: the exact local YM21 capture
bytes, the direct unverified challenger, the withdrawn negative control, and
the five user-nominated adjacent arXiv versions.  None of the adjacent records
has Yang--Mills existence or mass-gap authority.
"""

from __future__ import annotations

import copy
import datetime as dt
from collections.abc import Mapping
from typing import Any

from ..conceptual_ancestry_v3 import (
    DEFAULT_MAX_AGE_SECONDS,
    build_bounded_current_literature_bundle,
    build_registered_adjacent_abstraction_method_lane,
    validate_adjacent_abstraction_method_lane,
    validate_bounded_current_literature_bundle,
    validate_conceptual_ancestry_v3,
)
from ..contracts import ContractError
from ..literature_snapshot_capture_bridge import (
    build_literature_snapshot_capture_bridge,
    validate_literature_snapshot_capture_bridge,
)


YM21_TARGET_ID = "yang-mills-existence-and-mass-gap-target"
YM21_CAPTURE_ID = "ym21-broad-frontier-search-20260721"
YM21_CAPTURE_SHA256 = (
    "sha256:83073f245995253e9c5a5972b9054962b3e7b780f0ba13fe9a0138477b2dcbe9"
)
YM21_CAPTURE_BYTE_LENGTH = 20859
YM21_LATEST_ALLOWED_CAPTURE_DATE = "2026-07-21"
YM21_REJECTED_LOCAL_CAPTURE_DATE = "2026-07-22"
YM21_CAPTURE_COMPLETED_AT_UTC = "2026-07-21T20:23:45Z"
YM21_ADJACENT_LANE_OBSERVED_AT = YM21_CAPTURE_COMPLETED_AT_UTC
YM21_DIRECT_CHALLENGER_SOURCE_ID = "arxiv-2606.19362"
YM21_WITHDRAWN_CONTROL_SOURCE_ID = "arxiv-2506.00284-withdrawn"
YM21_CANONICAL_SEMANTIC_SNAPSHOT_ID = (
    "literature-snapshot.48e474c17e6c8c1918896fdc"
)
YM21_CANONICAL_SEMANTIC_SNAPSHOT_DIGEST = (
    "sha256:71f3d7489dddacc5cccbe5467234eaf9eab29446713b2a6f3a1065d67cf03f57"
)
YM21_CANONICAL_SEMANTIC_SOURCE_COUNT = 21

YM21_CAPTURE_LANE_TYPES = frozenset(
    {
        "closest_known_work",
        "recent_frontier_preprints",
        "negative_results_barriers",
        "conceptual_genealogy",
        "adjacent_field_mechanisms",
        "dissenting_positions",
    }
)

YM21_ADJACENT_SOURCE_RECORDS: tuple[dict[str, Any], ...] = (
    {
        "source_id": "arxiv-2603.19525",
        "version_id": "2603.19525v1",
        "title": "Homotopy lattice gauge fields 1: The fields and their properties",
        "authors": ["Juan Orendain", "Ivan Sanchez", "José A. Zapata"],
        "version_date": "2026-03-19",
        "version_event": "submitted",
        "url": "https://arxiv.org/abs/2603.19525",
        "method_topic": "homotopy-coherent lattice gauge fields",
        "method_relevance": (
            "May inform abstraction choices for lattice fields, coherence, "
            "local-to-global organization, and comparison maps."
        ),
        "target_relevance": "adjacent_method_only_no_direct_target_support",
    },
    {
        "source_id": "arxiv-2411.07195",
        "version_id": "2411.07195v4",
        "title": (
            "An Explicit Categorical Construction of Instanton Density in "
            "Lattice Yang-Mills Theory"
        ),
        "authors": ["Peng Zhang", "Jing-Yuan Chen"],
        "version_date": "2025-06-21",
        "version_event": "revised",
        "url": "https://arxiv.org/abs/2411.07195",
        "method_topic": "categorical lattice instanton-density construction",
        "method_relevance": (
            "May inform typed local-to-global constructions and observable "
            "bookkeeping at an adjacent abstraction level."
        ),
        "target_relevance": "adjacent_method_only_no_direct_target_support",
    },
    {
        "source_id": "arxiv-2606.02269",
        "version_id": "2606.02269v2",
        "title": (
            "A Cohesive ∞-Topos with a Quantum Modality from "
            "Finite-Dimensional C*-Algebras"
        ),
        "authors": ["Joey Woo"],
        "version_date": "2026-06-03",
        "version_event": "revised",
        "url": "https://arxiv.org/abs/2606.02269",
        "method_topic": "cohesive higher-topos and quantum modality",
        "method_relevance": (
            "May inform modal separation of classical, cohesive, and quantum "
            "structure without transferring a target theorem."
        ),
        "target_relevance": "adjacent_method_only_no_direct_target_support",
    },
    {
        "source_id": "arxiv-2606.12534",
        "version_id": "2606.12534v1",
        "title": "Higher Gauge Theory via Differential Nonabelian Cohomology",
        "authors": ["Hisham Sati", "Urs Schreiber"],
        "version_date": "2026-06-10",
        "version_event": "submitted",
        "url": "https://arxiv.org/abs/2606.12534",
        "method_topic": "differential nonabelian cohomology for higher gauge theory",
        "method_relevance": (
            "May inform typed higher-gauge and cocycle vocabulary for conceptual "
            "modeling only."
        ),
        "target_relevance": "adjacent_method_only_no_direct_target_support",
    },
    {
        "source_id": "arxiv-2509.15301",
        "version_id": "2509.15301v2",
        "title": "Higher-form symmetries as higher automorphism bundles",
        "authors": ["Alonso Perez-Lona"],
        "version_date": "2025-10-06",
        "version_event": "revised",
        "url": "https://arxiv.org/abs/2509.15301",
        "method_topic": "higher-form symmetry via higher automorphism bundles",
        "method_relevance": (
            "May inform symmetry and bundle-level abstraction vocabulary while "
            "preserving all target-specific analytic burdens."
        ),
        "target_relevance": "adjacent_method_only_no_direct_target_support",
    },
)
YM21_ADJACENT_SOURCE_IDS: tuple[str, ...] = tuple(
    row["source_id"] for row in YM21_ADJACENT_SOURCE_RECORDS
)

_YM21_PERMITTED_USES = (
    "abstraction_vocabulary",
    "typed_relation_design",
    "conceptual_mechanism_questions",
    "local_to_global_representation_comparison",
)
_YM21_FORBIDDEN_USES = (
    "direct_target_support",
    "yang_mills_existence_support",
    "yang_mills_mass_gap_support",
    "proof_or_theorem_support",
    "source_truth_inference",
    "global_latestness_claim",
    "exhaustive_coverage_claim",
    "novelty_or_publication_claim",
)
_YM21_TARGET_SPECIFIC_FORBIDDEN_CLAIMS = (
    "yang_mills_existence_support",
    "yang_mills_mass_gap_support",
)


class YM21ConceptualAncestryAdapterError(ContractError):
    """Carry a stable target-adapter rejection code."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"ym21_conceptual_ancestry[{reason_code}]: {message}")


def _fail(reason_code: str, message: str) -> None:
    raise YM21ConceptualAncestryAdapterError(reason_code, message)


def _timestamp(value: Any, label: str) -> dt.datetime:
    if not isinstance(value, str):
        _fail("timestamp_invalid", f"{label} must be a timestamp")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise YM21ConceptualAncestryAdapterError(
            "timestamp_invalid", f"{label} is invalid"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        _fail("timestamp_invalid", f"{label} must carry a timezone")
    return parsed.astimezone(dt.UTC)


def build_ym21_adjacent_abstraction_method_lane(
    *,
    observed_at: str = YM21_ADJACENT_LANE_OBSERVED_AT,
) -> dict[str, Any]:
    """Build the exact five-paper, method-only YM21 adjacent lane."""

    return build_registered_adjacent_abstraction_method_lane(
        target_id=YM21_TARGET_ID,
        selection_basis={
            "kind": "user_nominated_exact_arxiv_versions",
            "observed_at": observed_at,
            "record_count": 5,
            "primary_record_class": "arxiv_abstract_version_metadata",
        },
        sources=YM21_ADJACENT_SOURCE_RECORDS,
        permitted_uses=_YM21_PERMITTED_USES,
        forbidden_uses=_YM21_FORBIDDEN_USES,
        excluded_target_source_ids=[
            YM21_DIRECT_CHALLENGER_SOURCE_ID,
            YM21_WITHDRAWN_CONTROL_SOURCE_ID,
        ],
        excluded_capture_dates=[YM21_REJECTED_LOCAL_CAPTURE_DATE],
        target_specific_forbidden_claims=_YM21_TARGET_SPECIFIC_FORBIDDEN_CLAIMS,
    )


def validate_ym21_adjacent_abstraction_method_lane(
    lane: Mapping[str, Any],
) -> dict[str, Any]:
    """Require the exact five source versions and explicit no-mass-gap use."""

    try:
        value = validate_adjacent_abstraction_method_lane(lane)
    except ContractError as exc:
        raise YM21ConceptualAncestryAdapterError(
            "adjacent_lane_contract_invalid",
            f"generic adjacent-lane validation rejected YM21 input: {exc}",
        ) from exc
    expected = build_ym21_adjacent_abstraction_method_lane(
        observed_at=value["selection_basis"]["observed_at"]
    )
    observed = _timestamp(
        value["selection_basis"]["observed_at"], "adjacent lane observed_at"
    )
    cutoff = _timestamp(
        YM21_CAPTURE_COMPLETED_AT_UTC, "YM21 registered capture cutoff"
    )
    latest_source_version = max(
        dt.date.fromisoformat(str(row["version_date"]))
        for row in value["sources"]
    )
    if (
        latest_source_version > observed.date()
        or observed > cutoff
        or observed.date()
        > dt.date.fromisoformat(YM21_LATEST_ALLOWED_CAPTURE_DATE)
    ):
        _fail(
            "adjacent_lane_chronology_invalid",
            "YM21 requires source version <= observation <= exact capture cutoff",
        )
    if value != expected:
        _fail(
            "adjacent_lane_substitution",
            "exact YM21 adjacent versions or no-target-support boundary changed",
        )
    if (
        tuple(row["source_id"] for row in value["sources"])
        != YM21_ADJACENT_SOURCE_IDS
        or set(value["target_separation"]["target_specific_forbidden_claims"])
        != set(_YM21_TARGET_SPECIFIC_FORBIDDEN_CLAIMS)
        or value["authority"]["direct_target_claim_authority"] is not False
    ):
        _fail(
            "adjacent_lane_authority_forgery",
            "YM21 adjacent lane gained existence or mass-gap authority",
        )
    return copy.deepcopy(value)


def _validate_ym21_bundle_contents(
    bundle: Mapping[str, Any],
) -> None:
    capture = bundle["capture"]
    descriptor = bundle["capture_descriptor"]
    currentness = bundle["currentness"]
    if (
        bundle["target_id"] != YM21_TARGET_ID
        or capture["capture_id"] != YM21_CAPTURE_ID
        or descriptor["capture_id"] != YM21_CAPTURE_ID
        or descriptor["sha256"] != YM21_CAPTURE_SHA256
        or descriptor["byte_length"] != YM21_CAPTURE_BYTE_LENGTH
        or currentness["latest_allowed_capture_date"]
        != YM21_LATEST_ALLOWED_CAPTURE_DATE
        or len(capture["lanes"]) != 6
        or frozenset(row["lane_type"] for row in capture["lanes"])
        != YM21_CAPTURE_LANE_TYPES
        or len(capture["raw_results"]) != 27
    ):
        _fail(
            "capture_substitution",
            "exact YM21 capture bytes, lane closure, or registered cutoff changed",
        )
    completed = _timestamp(capture["capture_completed_at"], "capture completion")
    if completed.date() > dt.date.fromisoformat(
        YM21_LATEST_ALLOWED_CAPTURE_DATE
    ):
        _fail(
            "future_dated_capture_forbidden",
            "the 2026-07-22 local capture is historical and cannot become current",
        )
    by_source = {
        str(row["source_id"]): row for row in capture["raw_results"]
    }
    direct = by_source.get(YM21_DIRECT_CHALLENGER_SOURCE_ID)
    withdrawn = by_source.get(YM21_WITHDRAWN_CONTROL_SOURCE_ID)
    if (
        direct is None
        or direct["disposition"] != "included_unverified_challenger"
        or direct["claim_status"] != "unverified_challenger"
    ):
        _fail(
            "direct_challenger_missing",
            "arXiv:2606.19362 must remain an unverified challenger",
        )
    if (
        withdrawn is None
        or withdrawn["disposition"]
        != "included_negative_control_excluded_from_support"
        or withdrawn["claim_status"] != "withdrawn_not_support"
    ):
        _fail(
            "withdrawn_control_promoted",
            "arXiv:2506.00284 must remain withdrawn and excluded from support",
        )
    lane = bundle["adjacent_abstraction_method_lane"]
    if not isinstance(lane, Mapping):
        _fail(
            "adjacent_lane_missing",
            "exact YM21 ancestry requires the five-paper method lane",
        )
    validate_ym21_adjacent_abstraction_method_lane(lane)


def build_ym21_bounded_current_literature_bundle(
    *,
    capture_bytes: bytes,
    run_id: str,
    state_version: int,
    present_use_at: str,
    adjacent_method_lane: Mapping[str, Any] | None = None,
    max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS,
) -> dict[str, Any]:
    """Build the exact YM21 capture bundle without the legacy July-22 chain."""

    bundle = build_bounded_current_literature_bundle(
        capture_bytes=capture_bytes,
        target_id=YM21_TARGET_ID,
        run_id=run_id,
        state_version=state_version,
        present_use_at=present_use_at,
        latest_allowed_capture_date=YM21_LATEST_ALLOWED_CAPTURE_DATE,
        adjacent_method_lane=(
            build_ym21_adjacent_abstraction_method_lane()
            if adjacent_method_lane is None
            else adjacent_method_lane
        ),
        max_age_seconds=max_age_seconds,
    )
    return validate_ym21_bounded_current_literature_bundle(bundle)


def validate_ym21_bounded_current_literature_bundle(
    bundle: Mapping[str, Any],
    *,
    present_use_at: str | None = None,
) -> dict[str, Any]:
    """Replay the generic bundle, then the exact target-specific closure."""

    value = validate_bounded_current_literature_bundle(
        bundle, present_use_at=present_use_at
    )
    _validate_ym21_bundle_contents(value)
    return copy.deepcopy(value)


def _validate_ym21_snapshot_bridge_contents(
    bridge: Mapping[str, Any],
) -> None:
    """Pin only the exact target adapter to the canonical YM semantic root."""

    raw_root = bridge["raw_capture_root"]
    semantic_root = bridge["semantic_snapshot_root"]
    if (
        bridge["target_id"] != YM21_TARGET_ID
        or raw_root["capture_id"] != YM21_CAPTURE_ID
        or raw_root["sha256"] != YM21_CAPTURE_SHA256
        or semantic_root["snapshot_id"]
        != YM21_CANONICAL_SEMANTIC_SNAPSHOT_ID
        or semantic_root["content_digest"]
        != YM21_CANONICAL_SEMANTIC_SNAPSHOT_DIGEST
        or semantic_root["source_count"]
        != YM21_CANONICAL_SEMANTIC_SOURCE_COUNT
    ):
        _fail(
            "snapshot_capture_bridge_substitution",
            "YM21 bridge changed its exact raw or canonical semantic root",
        )


def build_ym21_literature_snapshot_capture_bridge(
    *,
    literature_bundle: Mapping[str, Any],
    semantic_snapshot: Mapping[str, Any],
    present_use_at: str | None = None,
) -> dict[str, Any]:
    """Build the exact YM21 two-root bridge through the generic contract.

    The generic bridge establishes selection and source-identity derivation.
    This adapter alone pins the retained July-21 capture and the canonical
    normalized YM snapshot.  Their unequal hashes remain separately visible.
    """

    bundle = validate_ym21_bounded_current_literature_bundle(
        literature_bundle, present_use_at=present_use_at
    )
    bridge = build_literature_snapshot_capture_bridge(
        literature_bundle=bundle,
        semantic_snapshot=semantic_snapshot,
        present_use_at=present_use_at,
    )
    _validate_ym21_snapshot_bridge_contents(bridge)
    return copy.deepcopy(bridge)


def validate_ym21_literature_snapshot_capture_bridge(
    bridge: Mapping[str, Any],
    *,
    literature_bundle: Mapping[str, Any],
    semantic_snapshot: Mapping[str, Any],
    present_use_at: str | None = None,
) -> dict[str, Any]:
    """Replay both generic derivation and exact YM root selection."""

    bundle = validate_ym21_bounded_current_literature_bundle(
        literature_bundle, present_use_at=present_use_at
    )
    value = validate_literature_snapshot_capture_bridge(
        bridge,
        literature_bundle=bundle,
        semantic_snapshot=semantic_snapshot,
        present_use_at=present_use_at,
    )
    _validate_ym21_snapshot_bridge_contents(value)
    return copy.deepcopy(value)


def validate_ym21_conceptual_ancestry_v3(
    ancestry: Mapping[str, Any],
    *,
    present_use_at: str | None = None,
) -> dict[str, Any]:
    """Require the exact YM21 bundle inside an otherwise generic ancestry."""

    value = validate_conceptual_ancestry_v3(
        ancestry, present_use_at=present_use_at
    )
    if value["target_id"] != YM21_TARGET_ID:
        _fail("target_mismatch", "YM21 adapter received another target")
    stages = {row["stage_id"]: row["artifact"] for row in value["stages"]}
    validate_ym21_bounded_current_literature_bundle(
        stages["current_bounded_literature"],
        present_use_at=present_use_at,
    )
    return copy.deepcopy(value)


__all__ = [
    "YM21_ADJACENT_LANE_OBSERVED_AT",
    "YM21_ADJACENT_SOURCE_IDS",
    "YM21_CANONICAL_SEMANTIC_SNAPSHOT_DIGEST",
    "YM21_CANONICAL_SEMANTIC_SNAPSHOT_ID",
    "YM21_CANONICAL_SEMANTIC_SOURCE_COUNT",
    "YM21_CAPTURE_ID",
    "YM21_CAPTURE_COMPLETED_AT_UTC",
    "YM21_CAPTURE_SHA256",
    "YM21ConceptualAncestryAdapterError",
    "YM21_LATEST_ALLOWED_CAPTURE_DATE",
    "YM21_TARGET_ID",
    "build_ym21_adjacent_abstraction_method_lane",
    "build_ym21_bounded_current_literature_bundle",
    "build_ym21_literature_snapshot_capture_bridge",
    "validate_ym21_adjacent_abstraction_method_lane",
    "validate_ym21_bounded_current_literature_bundle",
    "validate_ym21_conceptual_ancestry_v3",
    "validate_ym21_literature_snapshot_capture_bridge",
]
