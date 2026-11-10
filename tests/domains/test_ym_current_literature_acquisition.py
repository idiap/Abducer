# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Target regressions for genuine acquisition versus non-renewing replay."""

from __future__ import annotations

import copy
import json
import shutil
import sys
from pathlib import Path

import pytest

from agentic.discovery.contracts import canonical_digest, canonical_json
from agentic.discovery.literature import LANE_TYPES, run_frontier_literature_cycle


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "agentic" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import run_ym_canonical_parent_cycle_20260721 as runner  # noqa: E402
import build_ym_current_literature_capture_20260722 as current_builder  # noqa: E402


def _fixture_live_acquisition() -> dict:
    theory_digest = canonical_digest({"target": runner.TARGET_ID, "generation": 0})
    request = {
        "target_id": runner.TARGET_ID,
        "claim_scope": "fixture-only six-lane acquisition boundary",
        "theory_state_digest": theory_digest,
        "coverage_cutoff": "2026-07-22T23:59:59+02:00",
        "coverage_limits": ["Fixture providers exercise authority mechanics only."],
        "search_lanes": [
            {
                "lane_id": f"fixture-{lane_type}",
                "lane_type": lane_type,
                "queries": [f"fixture target {lane_type.replace('_', ' ')}"],
                "inclusion_policy": "Include the fixture primary result.",
                "exclusion_policy": "Exclude target mismatch.",
            }
            for lane_type in LANE_TYPES
        ],
    }
    providers = {}
    for index, lane_type in enumerate(LANE_TYPES):

        def provider(_request: dict, *, index: int = index, lane_type: str = lane_type) -> dict:
            return {
                "provider": f"fixture-provider-{lane_type}",
                "index": f"fixture-index-{lane_type}",
                "execution_mode": "live",
                "status": "completed",
                "coverage_cutoff": request["coverage_cutoff"],
                "sources": [
                    {
                        "source_id": f"fixture-source-{index}",
                        "work_identity": f"fixture:work-{index}",
                        "title": f"Fixture result {index}",
                        "authors": [f"Author {index}"],
                        "publication_date": "2026-07-22",
                        "source_version": "v1",
                        "source_type": "primary",
                        "url": f"https://example.test/fixture/{index}",
                        "correction_status": "none_known",
                        "decision_relevant": True,
                        "claims": [f"Fixture claim {index}."],
                        "limitations": ["Fixture semantics authorize no research claim."],
                    }
                ],
            }

        providers[lane_type] = provider
    return run_frontier_literature_cycle(request, providers=providers)


def test_target_replay_preserves_original_acquisition_without_clock_or_live_relabelling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    acquisition = _fixture_live_acquisition()

    def forbidden_clock() -> str:
        raise AssertionError("replay attempted to mint a timestamp")

    monkeypatch.setattr("agentic.discovery.literature.utc_now", forbidden_clock)
    replay = runner._replay_current_frontier_acquisition(acquisition)
    assert replay["provenance_mode"] == "frozen_response_replay"
    assert replay["original_acquisition_snapshot"] == acquisition
    assert replay["search_started_at"] == acquisition["search_started_at"]
    assert replay["search_completed_at"] == acquisition["search_completed_at"]
    assert all(
        row["execution_mode"] == "frozen_response_replay"
        for row in replay["lane_receipts"]
    )


def test_target_fails_closed_when_genuine_current_capture_bytes_are_absent(
    tmp_path: Path,
) -> None:
    historical_before = runner.BROAD_FRONTIER_CAPTURE.read_bytes()
    with pytest.raises(
        runner.YMCanonicalCycleError,
        match=runner.CURRENT_ACQUISITION_UNAVAILABLE,
    ):
        runner.build_current_literature_snapshot(
            theory_state_digest=canonical_digest("fixture-state"),
            output_root=tmp_path,
            capture_path=tmp_path / "missing-capture.json",
            acquisition_path=tmp_path / "missing-acquisition.json",
        )
    assert runner.BROAD_FRONTIER_CAPTURE.read_bytes() == historical_before
    assert not list(tmp_path.iterdir())


def test_normalized_metadata_without_six_raw_response_artifacts_is_rejected(
    tmp_path: Path,
) -> None:
    capture = json.loads(runner.BROAD_FRONTIER_CAPTURE.read_text(encoding="utf-8"))
    capture["capture_started_at"] = "2026-07-22T08:00:00+02:00"
    capture["capture_completed_at"] = "2026-07-22T08:10:00+02:00"
    capture["coverage_cutoff"] = capture["capture_completed_at"]
    for row, tag in zip(
        capture["raw_results"], sorted(runner.CURRENT_SURVEILLANCE_TAGS), strict=False
    ):
        row["surveillance_tags"] = [tag]
        if tag == "target_mismatch":
            row["disposition"] = "excluded_target_mismatch"
    capture["provider_response_artifacts"] = []
    capture_path = tmp_path / "frontier_search_live_capture_20260722.json"
    capture_path.write_bytes(canonical_json(capture) + b"\n")
    with pytest.raises(
        runner.YMCanonicalCycleError,
        match="exactly six provider-response byte descriptors",
    ):
        runner.load_current_frontier_acquisition(
            capture_path=capture_path,
            acquisition_path=tmp_path / "absent-acquisition.json",
        )


def test_old_capture_cannot_be_renewed_by_copying_or_rehashing(tmp_path: Path) -> None:
    capture = copy.deepcopy(
        json.loads(runner.BROAD_FRONTIER_CAPTURE.read_text(encoding="utf-8"))
    )
    capture_path = tmp_path / "frontier_search_live_capture_20260722.json"
    capture_path.write_bytes(canonical_json(capture) + b"\n")
    with pytest.raises(
        runner.YMCanonicalCycleError,
        match="not an ordered 2026-07-22 acquisition",
    ):
        runner.load_current_frontier_acquisition(
            capture_path=capture_path,
            acquisition_path=tmp_path / "absent-acquisition.json",
        )


def test_checked_in_multi_execution_bundle_is_the_exact_current_runner_authority() -> None:
    theory_digest = canonical_digest(
        runner.initial_state(runner.TARGET_ID, runner.RUN_ID)
    )
    capture, acquisition, authority = runner.load_current_frontier_acquisition(
        theory_state_digest=theory_digest
    )

    assert capture["schema_version"] == "2.1"
    assert capture["capture_mode"] == (
        "agent_observed_multi_execution_literature_capture_frozen_for_replay"
    )
    assert capture["provider"]["external_authentication_status"] == "unavailable"
    assert acquisition["theory_state_digest"] == theory_digest
    assert len(capture["lanes"]) == len(LANE_TYPES) == 6
    assert len(capture["provider_response_artifacts"]) == 6

    strict = authority["validated_acquisition_authority"]
    assert strict["source_routing_eligibility"] == {
        "aps-prd-4dxd-kh1r-2026": "unverified_audit_only",
        "arxiv-2606.19362-v1": "unverified_audit_only",
        "cambridge-coe-2025-sgpbm-retracted-v1": "negative_evidence_only",
        "harvard-chatterjee-ym-foundations-2025": "unverified_audit_only",
        "nature-reviews-physics-douglas-2026": "unverified_audit_only",
        "zenodo-18837540": "blocked_positive_support",
        "zenodo-19614728": "blocked_positive_support",
        "zenodo-19699784-dissent-v1": "unverified_audit_only",
        "zenodo-21479499": "unverified_audit_only",
    }
    graph = capture["version_lineages"][0]
    assert [row["source_version"] for row in graph["versions"]] == [
        "1.0",
        "2.0",
        "3.0",
    ]
    assert [row["status"] for row in graph["versions"]] == [
        "superseded",
        "superseded",
        "current",
    ]
    assert [row["scope_delta"]["classification"] for row in graph["edges"]] == [
        "broadened",
        "narrowed",
    ]


def test_checked_in_multi_execution_bundle_is_deterministically_reproducible() -> None:
    outputs, summary = current_builder._exact_outputs(
        current_builder.DEFAULT_OUTPUT_ROOT.resolve()
    )

    assert summary["output_count"] == 8
    assert summary["theory_state_digest"] == canonical_digest(
        runner.initial_state(runner.TARGET_ID, runner.RUN_ID)
    )
    assert all(path.read_bytes() == expected for path, expected in outputs.items())


def test_checked_in_multi_execution_bundle_rejects_one_tampered_artifact(
    tmp_path: Path,
) -> None:
    authority_root = tmp_path / "current-literature"
    authority_root.mkdir()
    capture_path = authority_root / runner.CURRENT_FRONTIER_CAPTURE.name
    acquisition_path = authority_root / runner.CURRENT_FRONTIER_ACQUISITION.name
    shutil.copy2(runner.CURRENT_FRONTIER_CAPTURE, capture_path)
    shutil.copy2(runner.CURRENT_FRONTIER_ACQUISITION, acquisition_path)
    capture = json.loads(capture_path.read_text(encoding="utf-8"))
    for descriptor in capture["provider_response_artifacts"]:
        source = runner.CURRENT_FRONTIER_CAPTURE.parent / descriptor["path"]
        destination = authority_root / descriptor["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    tampered_path = authority_root / capture["provider_response_artifacts"][0]["path"]
    tampered = json.loads(tampered_path.read_text(encoding="utf-8"))
    tampered["result_items"][0]["bounded_excerpt"] += " tampered"
    tampered_path.write_bytes(canonical_json(tampered) + b"\n")

    with pytest.raises(
        runner.YMCanonicalCycleError,
        match=runner.CURRENT_ACQUISITION_INVALID,
    ):
        runner.load_current_frontier_acquisition(
            capture_path=capture_path,
            acquisition_path=acquisition_path,
        )
