# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Deterministic and adversarial tests for the two-root literature bridge.

The generic fixture proves that the bridge has no Yang--Mills dependency.  The
YM fixture then pins the exact retained July-21 bytes to the exact canonical
semantic snapshot while checking that their unequal hashes remain visible.
Adversarial cases target root conflation, detached certificates, changed raw
selection, changed semantic locators, and authority escalation.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

from agentic.discovery import literature as literature_runtime
from agentic.discovery.conceptual_ancestry_v3 import (
    build_bounded_current_literature_bundle,
)
from agentic.discovery.contracts import canonical_digest, canonical_json
from agentic.discovery.literature import (
    LANE_TYPES,
    expected_snapshot_validator_receipt_id,
    run_frontier_literature_cycle,
    validate_snapshot,
)
from agentic.discovery.literature_snapshot_capture_bridge import (
    AUTHORITY,
    LiteratureSnapshotCaptureBridgeError,
    build_literature_snapshot_capture_bridge,
    validate_literature_snapshot_capture_bridge,
)
from agentic.discovery.yang_mills.ym21_conceptual_ancestry_adapter import (
    YM21_CANONICAL_SEMANTIC_SNAPSHOT_DIGEST,
    YM21_CANONICAL_SEMANTIC_SNAPSHOT_ID,
    YM21_CAPTURE_ID,
    YM21_CAPTURE_SHA256,
    YM21_TARGET_ID,
    YM21ConceptualAncestryAdapterError,
    build_ym21_bounded_current_literature_bundle,
    build_ym21_literature_snapshot_capture_bridge,
    validate_ym21_literature_snapshot_capture_bridge,
)


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT
    / "agentic/spec/literature_snapshot_capture_bridge_v1.schema.json"
)
GENERIC_MODULE_PATH = (
    ROOT / "agentic/discovery/literature_snapshot_capture_bridge.py"
)
YM_CAPTURE_PATH = (
    ROOT
    / "agentic/evals/ym_representational_dynamics_20260721"
    / "frontier_search_live_capture_20260721.json"
)
YM_SEMANTIC_SNAPSHOT_PATH = (
    ROOT
    / "agentic/reports/ym_representational_dynamics_integration/2026-07-21"
    / "canonical_parent_cycle/workspace/artifacts"
    / "00-frozen-live-literature-snapshot.json"
)
YM_ALTERNATE_SEMANTIC_SNAPSHOT_PATH = (
    ROOT
    / "agentic/reports/ym_representational_dynamics_integration/2026-07-21"
    / "canonical_parent_cycle_pre_spectral_descent/workspace/artifacts"
    / "00-frozen-live-literature-snapshot.json"
)
YM_PRESENT_USE_AT = "2026-07-21T21:16:00Z"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_bytes())


def _reseal_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Rebind a deliberately changed but otherwise valid semantic snapshot."""

    value = copy.deepcopy(snapshot)
    value["content_digest"] = canonical_digest(
        {
            key: item
            for key, item in value.items()
            if key
            not in {"content_digest", "validator_receipts", "validation_status"}
        }
    )
    validator = value["validator_receipts"][0]
    validator["validated_digest"] = value["content_digest"]
    validator["receipt_id"] = expected_snapshot_validator_receipt_id(
        value, validator["validator_id"]
    )
    validate_snapshot(value)
    return value


def _reseal_bridge(bridge: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(bridge)
    value["content_digest"] = canonical_digest(
        {key: item for key, item in value.items() if key != "content_digest"}
    )
    return value


@pytest.fixture(scope="module")
def ym_material() -> dict[str, Any]:
    capture_bytes = YM_CAPTURE_PATH.read_bytes()
    semantic_snapshot = _load_json(YM_SEMANTIC_SNAPSHOT_PATH)
    literature_bundle = build_ym21_bounded_current_literature_bundle(
        capture_bytes=capture_bytes,
        run_id="ym21-snapshot-capture-bridge-test",
        state_version=0,
        present_use_at=YM_PRESENT_USE_AT,
    )
    bridge = build_ym21_literature_snapshot_capture_bridge(
        literature_bundle=literature_bundle,
        semantic_snapshot=semantic_snapshot,
        present_use_at=YM_PRESENT_USE_AT,
    )
    return {
        "capture_bytes": capture_bytes,
        "capture": json.loads(capture_bytes),
        "semantic_snapshot": semantic_snapshot,
        "literature_bundle": literature_bundle,
        "bridge": bridge,
    }


def _generic_fixture(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Create six generic lanes whose semantic records derive from raw rows."""

    semantic_time = "2030-01-02T00:00:00Z"
    capture_time = "2030-01-01T00:00:00Z"
    target_id = "generic-snapshot-capture-bridge-target"
    monkeypatch.setattr(literature_runtime, "utc_now", lambda: semantic_time)
    search_lanes: list[dict[str, Any]] = []
    providers: dict[str, Any] = {}
    capture_lanes: list[dict[str, Any]] = []
    raw_results: list[dict[str, Any]] = []
    for index, lane_type in enumerate(LANE_TYPES):
        lane_id = f"generic-bridge-lane-{index}"
        result_id = f"generic-bridge-result-{index}"
        source_id = f"generic-bridge-source-{index}"
        query = f"generic bridge query {index}"
        title = f"Generic bridge result {index}"
        url = f"https://example.test/generic-bridge/{index}"
        search_lanes.append(
            {
                "lane_id": lane_id,
                "lane_type": lane_type,
                "queries": [query],
                "coverage_cutoff": capture_time,
                "inclusion_policy": "Include target-scoped fixture sources.",
                "exclusion_policy": "Exclude unrelated fixture sources.",
            }
        )

        def provider(
            _request: dict[str, Any],
            *,
            index: int = index,
            lane_type: str = lane_type,
            source_id: str = source_id,
            title: str = title,
            url: str = url,
        ) -> dict[str, Any]:
            return {
                "provider": f"generic-provider-{lane_type}",
                "index": f"generic-index-{index}",
                "execution_mode": "live",
                "status": "completed",
                "coverage_cutoff": capture_time,
                "sources": [
                    {
                        "source_id": source_id,
                        "work_identity": f"generic:work:{index}",
                        "title": title,
                        "authors": [f"Fixture Author {index}"],
                        "publication_date": "2029-12-01",
                        "source_version": "v1",
                        "source_type": "primary",
                        "url": url,
                        "correction_status": "none_known",
                        "decision_relevant": True,
                        "claims": [f"Generic fixture claim {index}."],
                        "limitations": ["Deterministic fixture only."],
                    }
                ],
            }

        providers[lane_type] = provider
        capture_lanes.append(
            {
                "lane_id": lane_id,
                "lane_type": lane_type,
                "queries": [query],
                "query_policy": "Generic target terms without record identifiers.",
                "status": "completed",
                "raw_result_ids": [result_id],
            }
        )
        raw_results.append(
            {
                "result_id": result_id,
                "source_id": source_id,
                "title": title,
                "url": url,
                "retrieval_status": "fixture_metadata",
                "disposition": "included_fixture_source",
                "reason": "Retain one deterministic generic source per lane.",
                "claim_status": "fixture_only",
            }
        )

    semantic_snapshot = run_frontier_literature_cycle(
        {
            "target_id": target_id,
            "claim_scope": "generic bridge derivation fixture",
            "theory_state_digest": canonical_digest(
                {"target_id": target_id, "generation": 0}
            ),
            "coverage_cutoff": capture_time,
            "coverage_limits": ["Only deterministic fixture sources exist."],
            "search_lanes": search_lanes,
        },
        providers=providers,
    )
    capture = {
        "schema_version": "1.0",
        "capture_id": "generic-snapshot-capture-bridge",
        "target_id": target_id,
        "capture_started_at": capture_time,
        "capture_completed_at": capture_time,
        "coverage_cutoff": capture_time,
        "capture_mode": "live_external_web_search_frozen_for_replay",
        "provider": {
            "provider_id": "generic-fixture-provider",
            "name": "Generic fixture provider",
            "index": "deterministic fixture index",
            "execution_boundary": (
                "Fixture metadata represents an external execution frozen for "
                "deterministic replay."
            ),
            "raw_payload_retention": "Normalized fixture metadata only.",
            "receipt_status": "externally_executed_then_frozen",
            "executable_replay_status": "frozen_response_adapter_only",
        },
        "lanes": capture_lanes,
        "raw_results": raw_results,
        "inclusion_policy": "Include the six target-scoped fixture sources.",
        "exclusion_policy": "Exclude unrelated fixture sources.",
        "coverage_limits": ["Only deterministic fixture sources exist."],
        "exhaustive_coverage_claim": False,
        "source_correctness_claim": False,
        "peer_validation_claim": False,
    }
    literature_bundle = build_bounded_current_literature_bundle(
        capture_bytes=canonical_json(capture),
        target_id=target_id,
        run_id="generic-snapshot-capture-bridge-run",
        state_version=0,
        present_use_at=semantic_time,
        latest_allowed_capture_date="2030-01-01",
    )
    bridge = build_literature_snapshot_capture_bridge(
        literature_bundle=literature_bundle,
        semantic_snapshot=semantic_snapshot,
        present_use_at=semantic_time,
    )
    return literature_bundle, semantic_snapshot, bridge


def test_generic_schema_and_runtime_are_domain_neutral(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    schema = _load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    generic_text = (
        GENERIC_MODULE_PATH.read_text(encoding="utf-8")
        + SCHEMA_PATH.read_text(encoding="utf-8")
    )
    assert YM21_TARGET_ID not in generic_text
    assert YM21_CAPTURE_SHA256 not in generic_text
    assert "arxiv-2606.19362" not in generic_text

    literature_bundle, semantic_snapshot, bridge = _generic_fixture(monkeypatch)
    replay = validate_literature_snapshot_capture_bridge(
        bridge,
        literature_bundle=literature_bundle,
        semantic_snapshot=semantic_snapshot,
        present_use_at="2030-01-02T00:00:00Z",
    )
    assert replay == bridge
    assert bridge["target_id"] == "generic-snapshot-capture-bridge-target"
    assert len(bridge["derivation"]["source_bindings"]) == len(LANE_TYPES)
    assert bridge["derivation"]["excluded_bindings"] == []
    assert {
        row["title_relation"] for row in bridge["derivation"]["source_bindings"]
    } == {"exact"}


def test_ym21_bridge_retains_two_exact_non_equal_roots(
    ym_material: dict[str, Any],
) -> None:
    bridge = ym_material["bridge"]
    replay = validate_ym21_literature_snapshot_capture_bridge(
        bridge,
        literature_bundle=ym_material["literature_bundle"],
        semantic_snapshot=ym_material["semantic_snapshot"],
        present_use_at=YM_PRESENT_USE_AT,
    )
    assert replay == bridge
    assert bridge["raw_capture_root"]["capture_id"] == YM21_CAPTURE_ID
    assert bridge["raw_capture_root"]["sha256"] == YM21_CAPTURE_SHA256
    assert (
        bridge["semantic_snapshot_root"]["snapshot_id"]
        == YM21_CANONICAL_SEMANTIC_SNAPSHOT_ID
    )
    assert (
        bridge["semantic_snapshot_root"]["content_digest"]
        == YM21_CANONICAL_SEMANTIC_SNAPSHOT_DIGEST
    )
    assert (
        bridge["raw_capture_root"]["sha256"]
        != bridge["semantic_snapshot_root"]["content_digest"]
    )
    assert bridge["root_separation"] == {
        "relation": (
            "cryptographically_distinct_roots_linked_by_replayed_derivation"
        ),
        "raw_capture_sha256": YM21_CAPTURE_SHA256,
        "semantic_snapshot_content_digest": (
            YM21_CANONICAL_SEMANTIC_SNAPSHOT_DIGEST
        ),
        "roots_distinct": True,
        "hash_equality_claim": False,
    }
    assert bridge["authority"] == AUTHORITY
    assert len(bridge["derivation"]["source_bindings"]) == 21
    assert len(bridge["derivation"]["excluded_bindings"]) == 6
    assert len(bridge["derivation"]["lane_bindings"]) == 6
    assert {
        row["source_id"]
        for row in bridge["derivation"]["source_bindings"]
        if row["title_relation"] == "normalized_display_only"
    } == {"arxiv-2506.00284-withdrawn", "clay-ym-current"}


def test_bridge_build_and_replay_are_deterministic(
    ym_material: dict[str, Any],
) -> None:
    rebuilt = build_ym21_literature_snapshot_capture_bridge(
        literature_bundle=ym_material["literature_bundle"],
        semantic_snapshot=ym_material["semantic_snapshot"],
        present_use_at=YM_PRESENT_USE_AT,
    )
    assert rebuilt == ym_material["bridge"]


def test_bridge_rejects_raw_and_semantic_hash_conflation(
    ym_material: dict[str, Any],
) -> None:
    forged = copy.deepcopy(ym_material["bridge"])
    semantic_digest = forged["semantic_snapshot_root"]["content_digest"]
    forged["raw_capture_root"]["sha256"] = semantic_digest
    forged["root_separation"]["raw_capture_sha256"] = semantic_digest
    forged = _reseal_bridge(forged)
    with pytest.raises(
        LiteratureSnapshotCaptureBridgeError
    ) as raised:
        validate_literature_snapshot_capture_bridge(
            forged,
            literature_bundle=ym_material["literature_bundle"],
            semantic_snapshot=ym_material["semantic_snapshot"],
            present_use_at=YM_PRESENT_USE_AT,
        )
    assert raised.value.reason_code == "root_hash_conflation"


def test_bridge_rejects_reclassified_raw_selection(
    ym_material: dict[str, Any],
) -> None:
    changed_capture = copy.deepcopy(ym_material["capture"])
    changed_capture["raw_results"][0][
        "disposition"
    ] = "excluded_adversarial_reclassification"
    changed_bundle = build_bounded_current_literature_bundle(
        capture_bytes=canonical_json(changed_capture),
        target_id=YM21_TARGET_ID,
        run_id="generic-reclassified-capture-run",
        state_version=0,
        present_use_at=YM_PRESENT_USE_AT,
        latest_allowed_capture_date="2026-07-21",
    )
    with pytest.raises(
        LiteratureSnapshotCaptureBridgeError
    ) as raised:
        build_literature_snapshot_capture_bridge(
            literature_bundle=changed_bundle,
            semantic_snapshot=ym_material["semantic_snapshot"],
            present_use_at=YM_PRESENT_USE_AT,
        )
    assert raised.value.reason_code == "included_source_bijection_invalid"


def test_bridge_rejects_changed_semantic_source_locator(
    ym_material: dict[str, Any],
) -> None:
    changed_snapshot = copy.deepcopy(ym_material["semantic_snapshot"])
    changed_source = changed_snapshot["sources"][0]
    changed_source["url"] = changed_source["url"] + "?detached=1"
    changed_source["content_digest"] = canonical_digest(
        {
            key: item
            for key, item in changed_source.items()
            if key != "content_digest"
        }
    )
    changed_snapshot = _reseal_snapshot(changed_snapshot)
    with pytest.raises(
        LiteratureSnapshotCaptureBridgeError
    ) as raised:
        build_literature_snapshot_capture_bridge(
            literature_bundle=ym_material["literature_bundle"],
            semantic_snapshot=changed_snapshot,
            present_use_at=YM_PRESENT_USE_AT,
        )
    assert raised.value.reason_code == "source_locator_mismatch"


def test_bridge_rejects_detached_but_valid_semantic_root(
    ym_material: dict[str, Any],
) -> None:
    alternate_snapshot = _load_json(YM_ALTERNATE_SEMANTIC_SNAPSHOT_PATH)
    validate_snapshot(alternate_snapshot)
    with pytest.raises(
        LiteratureSnapshotCaptureBridgeError
    ) as raised:
        validate_literature_snapshot_capture_bridge(
            ym_material["bridge"],
            literature_bundle=ym_material["literature_bundle"],
            semantic_snapshot=alternate_snapshot,
            present_use_at=YM_PRESENT_USE_AT,
        )
    assert raised.value.reason_code == "bridge_replay_mismatch"


def test_ym_adapter_rejects_another_valid_semantic_snapshot(
    ym_material: dict[str, Any],
) -> None:
    alternate_snapshot = _load_json(YM_ALTERNATE_SEMANTIC_SNAPSHOT_PATH)
    with pytest.raises(YM21ConceptualAncestryAdapterError) as raised:
        build_ym21_literature_snapshot_capture_bridge(
            literature_bundle=ym_material["literature_bundle"],
            semantic_snapshot=alternate_snapshot,
            present_use_at=YM_PRESENT_USE_AT,
        )
    assert raised.value.reason_code == "snapshot_capture_bridge_substitution"


def test_bridge_schema_rejects_authority_escalation(
    ym_material: dict[str, Any],
) -> None:
    forged = copy.deepcopy(ym_material["bridge"])
    forged["authority"]["source_truth_authority"] = "asserted"
    forged = _reseal_bridge(forged)
    with pytest.raises(
        LiteratureSnapshotCaptureBridgeError
    ) as raised:
        validate_literature_snapshot_capture_bridge(
            forged,
            literature_bundle=ym_material["literature_bundle"],
            semantic_snapshot=ym_material["semantic_snapshot"],
            present_use_at=YM_PRESENT_USE_AT,
        )
    assert raised.value.reason_code == "bridge_schema_invalid"
