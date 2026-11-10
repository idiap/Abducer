# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Deterministic coverage for target-scoped search and theory assimilation."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from agentic.discovery.contracts import ContractError, canonical_digest, stable_identifier
from agentic.discovery.literature import (
    LANE_TYPES,
    _merge_sources,
    assimilate_literature,
    expected_snapshot_validator_receipt_id,
    rebase_surviving_branches,
    resolve_present_literature_freshness,
    run_frontier_literature_cycle,
    select_newest_snapshot,
    validate_snapshot,
)


ROOT = Path(__file__).resolve().parents[2]
MAPPING_PLAN = json.loads(
    (
        ROOT
        / "tests/fixtures/frontier_literature_cycle/causal_mapping_plan.json"
    ).read_text(encoding="utf-8")
)


def _request(target: str = "target-a", *, theory_digest: str | None = None) -> dict:
    """Build all six genuinely differentiated lane requests."""

    digest = theory_digest or canonical_digest({"target": target, "generation": 1})
    return {
        "target_id": target,
        "claim_scope": "conceptual mechanisms and barriers",
        "theory_state_digest": digest,
        "coverage_cutoff": "2026-07-21",
        "coverage_limits": [
            "Only the named fixture indexes and exact queries were searched."
        ],
        "search_lanes": [
            {
                "lane_type": lane_type,
                "queries": [f"{target} exact {lane_type.replace('_', ' ')}"],
                "inclusion_policy": "Include target-scoped primary results.",
                "exclusion_policy": "Exclude target mismatch and duplicate versions.",
            }
            for lane_type in LANE_TYPES
        ],
    }


def _providers(
    target: str = "target-a",
    *,
    old_first: bool = False,
    failing_lane: str | None = None,
) -> dict:
    """Return actual fixture adapters whose execution can be receipt-backed."""

    providers = {}
    for index, lane_type in enumerate(LANE_TYPES):

        def provider(request: dict, index: int = index, lane_type: str = lane_type) -> dict:
            if lane_type == failing_lane:
                raise RuntimeError("fixture provider unavailable")
            year = 1965 if old_first and index == 0 else 2020 + index
            return {
                "provider": f"fixture-provider-{lane_type}",
                "index": f"fixture-index-{lane_type}",
                "execution_mode": "live",
                "status": "completed",
                "coverage_cutoff": "2026-07-21",
                "sources": [
                    {
                        "work_identity": f"{target}-work-{lane_type}-{year}",
                        "title": f"{target} result for {lane_type}",
                        "authors": [f"Author {index}"],
                        "publication_date": str(year),
                        "source_version": "v1",
                        "source_type": "primary",
                        "url": f"https://example.test/{target}/{lane_type}",
                        "correction_status": "none_known",
                        "decision_relevant": True,
                        "claims": [f"Exact source claim {index}."],
                        "limitations": [f"Only addresses fixture regime {index}."],
                    }
                ],
            }

        providers[lane_type] = provider
    return providers


def _mappings(snapshot: dict, *, first_event: str = "spawn") -> list[dict]:
    """Map every decision-relevant source, including explicit no-change cases."""

    mappings = []
    for index, source in enumerate(snapshot["sources"]):
        changed = index == 0
        policy = (
            MAPPING_PLAN["first_source"]
            if changed
            else MAPPING_PLAN["remaining_sources"]
        )
        mappings.append(
            {
                "source_id": source["source_id"],
                "theory_object_ids": [f"concept-{index}"],
                "object_kinds": ["concept", "schedule"],
                "relation": policy["relation"],
                "exact_claim": source["claims"][0],
                "source_limitation": source["limitations"][0],
                "conceptual_change": policy["conceptual_change"],
                "event_type": first_event if changed else policy["event_type"],
                "coverage_limits": list(snapshot["coverage_limits"]),
                "confidence": "high" if changed else "medium",
            }
        )
    return mappings


def _retime(snapshot: dict, completed: str) -> dict:
    """Change completion metadata and correctly rebind digest/validator identity."""

    shifted = copy.deepcopy(snapshot)
    for receipt in shifted["lane_receipts"]:
        receipt["started_at"] = completed
        receipt["completed_at"] = completed
        receipt_core = {
            key: value
            for key, value in receipt.items()
            if key not in {"content_digest", "validator_receipt_ids"}
        }
        receipt["content_digest"] = canonical_digest(receipt_core)
    shifted["search_started_at"] = completed
    shifted["search_completed_at"] = completed
    core = {
        key: value
        for key, value in shifted.items()
        if key not in {"content_digest", "validator_receipts", "validation_status"}
    }
    shifted["content_digest"] = canonical_digest(core)
    shifted["validator_receipts"][0]["validated_digest"] = shifted["content_digest"]
    shifted["validator_receipts"][0]["receipt_id"] = (
        expected_snapshot_validator_receipt_id(
            shifted, shifted["validator_receipts"][0]["validator_id"]
        )
    )
    shifted["validator_receipts"][0]["completed_at"] = completed
    return shifted


def test_live_cycle_has_six_executed_differentiated_receipts() -> None:
    snapshot = run_frontier_literature_cycle(
        _request(), providers=_providers()
    )
    validate_snapshot(snapshot)
    assert snapshot["provenance_mode"] == "live"
    assert snapshot["validation_status"] == "validated"
    assert {item["lane_type"] for item in snapshot["lane_receipts"]} == set(
        LANE_TYPES
    )
    assert all(item["queries"] and item["provider"] for item in snapshot["lane_receipts"])
    assert snapshot["search_completed_at"] == max(
        item["completed_at"] for item in snapshot["lane_receipts"]
    )


def test_frozen_response_replay_preserves_exact_acquisition_without_clock_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    acquisition = run_frontier_literature_cycle(_request(), providers=_providers())
    local_snapshot = run_frontier_literature_cycle(_request())

    def clock_forbidden() -> str:
        raise AssertionError("frozen replay attempted to acquire a new timestamp")

    monkeypatch.setattr("agentic.discovery.literature.utc_now", clock_forbidden)
    replay = run_frontier_literature_cycle(
        _request(), frozen_response_snapshot=acquisition
    )

    assert replay["provenance_mode"] == "frozen_response_replay"
    assert replay["original_acquisition_snapshot"] == acquisition
    assert replay["search_started_at"] == acquisition["search_started_at"]
    assert replay["search_completed_at"] == acquisition["search_completed_at"]
    acquired_by_lane = {
        item["lane_type"]: item for item in acquisition["lane_receipts"]
    }
    assert all(
        receipt["execution_mode"] == "frozen_response_replay"
        and receipt["started_at"]
        == acquired_by_lane[receipt["lane_type"]]["started_at"]
        and receipt["completed_at"]
        == acquired_by_lane[receipt["lane_type"]]["completed_at"]
        and receipt["original_acquisition_receipt"]
        == acquired_by_lane[receipt["lane_type"]]
        for receipt in replay["lane_receipts"]
    )
    assert (
        replay["validator_receipts"][0]["completed_at"]
        == acquisition["validator_receipts"][0]["completed_at"]
    )
    with pytest.raises(ContractError, match="mutually exclusive"):
        run_frontier_literature_cycle(
            _request(),
            providers=_providers(),
            frozen_response_snapshot=acquisition,
        )
    with pytest.raises(ContractError, match="validated live acquisition"):
        run_frontier_literature_cycle(
            _request(), frozen_response_snapshot=local_snapshot
        )


def test_frozen_response_present_use_is_bounded_by_original_acquisition() -> None:
    acquisition = run_frontier_literature_cycle(_request(), providers=_providers())
    replay = run_frontier_literature_cycle(
        _request(), frozen_response_snapshot=acquisition
    )
    completed = datetime.fromisoformat(
        replay["search_completed_at"].replace("Z", "+00:00")
    )
    mappings = _mappings(replay)

    with pytest.raises(ContractError, match="injected freshness evaluation time"):
        assimilate_literature(
            replay,
            theory_state_digest=replay["theory_state_digest"],
            theory_mappings=mappings,
            freshness_max_age_seconds=60,
        )
    packet = assimilate_literature(
        replay,
        theory_state_digest=replay["theory_state_digest"],
        theory_mappings=mappings,
        freshness_max_age_seconds=60,
        freshness_evaluated_at=completed + timedelta(seconds=30),
    )
    assert packet["resolution"]["active_investment_gate"] == "pass"
    assert packet["resolution"]["consume_before"] == (
        completed + timedelta(seconds=60)
    ).isoformat().replace("+00:00", "Z")
    with pytest.raises(ContractError, match="injected trusted clock"):
        resolve_present_literature_freshness(packet)
    assert resolve_present_literature_freshness(
        packet, now=completed + timedelta(seconds=60)
    )["active_investment_gate"] == "pass"
    expired = resolve_present_literature_freshness(
        packet, now=completed + timedelta(seconds=61)
    )
    assert expired["active_investment_gate"] == "blocked_stale"
    assert expired["reason"] == "consume_before_expired"


def test_frozen_response_replay_rejects_rehashed_receipt_tampering() -> None:
    acquisition = run_frontier_literature_cycle(_request(), providers=_providers())
    replay = run_frontier_literature_cycle(
        _request(), frozen_response_snapshot=acquisition
    )
    tampered = copy.deepcopy(replay)
    receipt = tampered["lane_receipts"][0]
    original_receipt = receipt["original_acquisition_receipt"]
    original_receipt["provider"] = "forged-original-provider"
    original_receipt["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in original_receipt.items()
            if key not in {"content_digest", "validator_receipt_ids"}
        }
    )
    original_receipt["validator_receipt_ids"] = [
        stable_identifier(
            "validator", original_receipt["lane_id"], original_receipt["content_digest"]
        )
    ]
    receipt["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in receipt.items()
            if key not in {"content_digest", "validator_receipt_ids"}
        }
    )
    receipt["validator_receipt_ids"] = [
        stable_identifier(
            "frozen-replay-lane-validator",
            receipt["lane_id"],
            original_receipt["content_digest"],
            receipt["content_digest"],
        )
    ]
    tampered["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in tampered.items()
            if key not in {"content_digest", "validator_receipts", "validation_status"}
        }
    )
    validator = tampered["validator_receipts"][0]
    validator["validated_digest"] = tampered["content_digest"]
    validator["receipt_id"] = expected_snapshot_validator_receipt_id(
        tampered, validator["validator_id"]
    )
    with pytest.raises(ContractError, match="does not exactly replay"):
        validate_snapshot(tampered)


def test_deduplication_retains_claim_conflicts_instead_of_inferring_agreement() -> None:
    providers = _providers()
    for index, lane_type in enumerate(LANE_TYPES):
        original = providers[lane_type]

        def same_work(
            request: dict,
            original=original,
            index: int = index,
        ) -> dict:
            response = original(request)
            source = response["sources"][0]
            source["work_identity"] = "shared-work"
            source["source_version"] = "v1"
            source["claims"] = [f"Lane-specific formulation {index}."]
            return response

        providers[lane_type] = same_work
    snapshot = run_frontier_literature_cycle(_request(), providers=providers)
    assert snapshot["result_count"] == 1
    assert snapshot["claim_conflicts"]
    assert all(
        conflict["resolution"].startswith("Retain both")
        for conflict in snapshot["claim_conflicts"]
    )


def test_duplicate_reduction_is_order_invariant_and_preserves_metadata_conflicts() -> None:
    observations = []
    for index in range(2):
        observations.append((f"lane-{index}", {
            "work_identity": "shared-conflicting-work", "source_id": f"provider-source-{index}", "title": f"Conflicting title {index}", "authors": [f"Author {index}"],
            "publication_date": "2026", "source_version": "v1", "source_type": "primary" if index == 0 else "survey", "url": f"https://example.test/{index}",
            "doi": f"10.1/conflict-{index}", "arxiv_id": f"2607.{index:05d}", "correction_status": "none_known" if index == 0 else "retracted",
            "decision_relevant": True, "claims": [f"Claim formulation {index}."], "limitations": [f"Limitation {index}."],
        }))
    forward = _merge_sources(observations)
    assert forward == _merge_sources(reversed(observations))
    sources, _duplicates, claim_conflicts, metadata_conflicts = forward
    assert claim_conflicts and sources[0]["correction_status"] == "unknown" and sources[0]["source_type"] == "other"
    assert sources[0]["doi"] is None and sources[0]["arxiv_id"] is None
    assert {"source_id", "title", "authors", "source_type", "doi", "arxiv_id", "correction_status"} <= {item["field"] for item in metadata_conflicts}


def test_generated_or_inline_sources_are_local_only_not_recent_live_search() -> None:
    request = _request()
    for index, lane in enumerate(request["search_lanes"]):
        lane["provider"] = "hardcoded-source-spine"
        lane["index"] = "local-json"
        lane["sources"] = _providers()[lane["lane_type"]](lane)["sources"]
    snapshot = run_frontier_literature_cycle(request)
    assert snapshot["provenance_mode"] == "local_only"
    packet = assimilate_literature(
        snapshot,
        theory_state_digest=snapshot["theory_state_digest"],
        theory_mappings=_mappings(snapshot),
    )
    assert packet["resolution"]["active_investment_gate"] == "blocked_local_only"
    assert packet["hypothesis_rebase_status"] == "provisional_local_only"


def test_one_missing_live_adapter_demotes_entire_snapshot_to_local_only() -> None:
    providers = _providers()
    providers.pop(LANE_TYPES[-1])
    request = _request()
    request["search_lanes"][-1]["sources"] = _providers()[LANE_TYPES[-1]](
        request["search_lanes"][-1]
    )["sources"]
    snapshot = run_frontier_literature_cycle(request, providers=providers)
    assert snapshot["provenance_mode"] == "local_only"


def test_wrong_target_never_satisfies_gate_even_if_newer() -> None:
    target_a = _retime(
        run_frontier_literature_cycle(_request("target-a"), providers=_providers("target-a")),
        "2026-07-20T12:00:00Z",
    )
    target_b = _retime(
        run_frontier_literature_cycle(_request("target-b"), providers=_providers("target-b")),
        "2026-07-21T12:00:00Z",
    )
    selected = select_newest_snapshot(
        [target_b, target_a],
        target_id="target-a",
        claim_scope="conceptual mechanisms and barriers",
    )
    assert selected["snapshot_id"] == target_a["snapshot_id"]
    with pytest.raises(ContractError, match="no validated target-scoped"):
        select_newest_snapshot([target_b], target_id="target-a")


def test_newest_selection_uses_completion_metadata_not_list_or_mtime_order() -> None:
    early = _retime(
        run_frontier_literature_cycle(_request(), providers=_providers()),
        "2026-07-20T12:00:00Z",
    )
    late = _retime(copy.deepcopy(early), "2026-07-21T12:00:00Z")
    selected = select_newest_snapshot(
        [early, late],
        target_id="target-a",
        claim_scope="conceptual mechanisms and barriers",
    )
    assert selected["search_completed_at"] == "2026-07-21T12:00:00Z"


def test_assimilation_emits_branch_spawn_and_justified_no_change() -> None:
    snapshot = run_frontier_literature_cycle(
        _request(), providers=_providers()
    )
    packet = assimilate_literature(
        snapshot,
        theory_state_digest=snapshot["theory_state_digest"],
        theory_mappings=_mappings(snapshot),
        hypotheses=[
            {
                "hypothesis_id": "hypothesis-a",
                "genealogy": ["intuition-before-search", "conceptual-parent"],
                "literature_relation": "partly_anticipated",
                "source_ids": [snapshot["sources"][0]["source_id"]],
                "required_revision": "Separate the old special case from the new mechanism.",
                "routing_effect": "sharpen",
            }
        ],
    )
    events = {mapping["event_type"] for mapping in packet["theory_mappings"]}
    assert "spawn" in events
    assert "justified_no_change" in events
    assert all(action["source_mapping_ids"] for action in packet["next_theory_actions"])
    assert packet["resolution"]["active_investment_gate"] == "pass"


def test_unmapped_decision_relevant_source_blocks_branch_selection() -> None:
    snapshot = run_frontier_literature_cycle(
        _request(), providers=_providers()
    )
    with pytest.raises(ContractError, match="lack claim-level mappings"):
        assimilate_literature(
            snapshot,
            theory_state_digest=snapshot["theory_state_digest"],
            theory_mappings=_mappings(snapshot)[:-1],
        )


def test_newly_discovered_old_theorem_can_create_large_theory_delta() -> None:
    prior = run_frontier_literature_cycle(
        _request(), providers=_providers()
    )
    current = run_frontier_literature_cycle(
        _request(), providers=_providers(old_first=True)
    )
    packet = assimilate_literature(
        current,
        theory_state_digest=current["theory_state_digest"],
        prior_snapshot=prior,
        theory_mappings=_mappings(current, first_event="reframe"),
    )
    assert packet["source_delta"]["newly_relevant_old_sources"]
    assert any(
        mapping["event_type"] == "reframe"
        for mapping in packet["theory_mappings"]
    )


def test_survivor_rebase_preserves_pre_search_genealogy() -> None:
    old = run_frontier_literature_cycle(
        _request(), providers=_providers()
    )
    newer = run_frontier_literature_cycle(
        _request(), providers=_providers(old_first=True)
    )
    survivors = [
        {
            "branch_id": "branch-a",
            "genealogy": ["intuition-a", "mutation-a"],
            "literature_snapshot_digest": old["content_digest"],
        },
        {
            "branch_id": "branch-b",
            "genealogy": ["intuition-b"],
            "literature_snapshot_digest": old["content_digest"],
        },
    ]
    rebased = rebase_surviving_branches(
        survivors,
        old_snapshot_digest=old["content_digest"],
        new_snapshot=newer,
        relations={
            "branch-a": {
                "literature_relation": "partly_anticipated",
                "source_ids": [newer["sources"][0]["source_id"]],
            }
        },
    )
    assert {item["literature_status"] for item in rebased} == {"rebased"}
    assert rebased[0]["pre_search_genealogy"] == ["intuition-a", "mutation-a"]
    assert all(
        item["literature_snapshot_digest"] == newer["content_digest"]
        for item in rebased
    )


def test_provider_failure_has_failed_receipt_and_invalid_snapshot() -> None:
    snapshot = run_frontier_literature_cycle(
        _request(), providers=_providers(failing_lane=LANE_TYPES[2])
    )
    failed = [
        receipt
        for receipt in snapshot["lane_receipts"]
        if receipt["status"] == "failed"
    ]
    assert len(failed) == 1
    assert failed[0]["failure"]
    assert snapshot["validation_status"] == "invalid"
    with pytest.raises(ContractError, match="no validated target-scoped"):
        select_newest_snapshot([snapshot], target_id="target-a")


def test_lane_receipt_digest_tampering_is_rejected() -> None:
    snapshot = run_frontier_literature_cycle(
        _request(), providers=_providers()
    )
    snapshot["lane_receipts"][0]["provider"] = "fabricated-provider"
    core = {
        key: value
        for key, value in snapshot.items()
        if key not in {"content_digest", "validator_receipts", "validation_status"}
    }
    snapshot["content_digest"] = canonical_digest(core)
    snapshot["validator_receipts"][0]["validated_digest"] = snapshot[
        "content_digest"
    ]
    snapshot["validator_receipts"][0]["receipt_id"] = (
        expected_snapshot_validator_receipt_id(
            snapshot, snapshot["validator_receipts"][0]["validator_id"]
        )
    )
    with pytest.raises(ContractError, match="lane .* digest mismatch"):
        validate_snapshot(snapshot)


def test_literature_validator_clis_pass() -> None:
    for script in (
        "agentic/scripts/validate_target_literature_search_snapshot.py",
        "agentic/scripts/validate_frontier_literature_assimilation.py",
    ):
        completed = subprocess.run(
            [sys.executable, script],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
