# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Receipt-bound tests for content-derived literature mapping and replay."""

from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path

import pytest

from agentic.discovery.contracts import ContractError, canonical_digest
from agentic.discovery.literature import (
    CLAIM_MAPPING_AUTHORITY_ID,
    LANE_TYPES,
    _normalize_claim_provenance,
    assimilate_derived_literature,
    assimilate_literature,
    bind_source_semantic_warrants,
    build_semantic_claim_layer,
    build_theory_object_catalog,
    derive_claim_mappings,
    expected_snapshot_validator_receipt_id,
    replay_literature_counterfactuals,
    run_frontier_literature_cycle,
    validate_claim_mapping_derivation,
    validate_assimilation,
    validate_literature_counterfactual_replay,
    validate_semantic_claim_layer,
)
from agentic.scripts.run_discovery_operator_protocol import _literature


ROOT = Path(__file__).resolve().parents[2]


def _snapshot(target_id: str = "mapping-target") -> dict:
    theory_digest = canonical_digest({"target": target_id, "state": 7})
    request = {
        "target_id": target_id,
        "claim_scope": "carrier mechanisms and route barriers",
        "theory_state_digest": theory_digest,
        "coverage_cutoff": "2026-07-22",
        "coverage_limits": ["Only deterministic mapping fixtures were searched."],
        "search_lanes": [
            {
                "lane_type": lane_type,
                "queries": [f"{target_id} {lane_type}"],
                "inclusion_policy": "Include exact target-scoped fixture claims.",
                "exclusion_policy": "Exclude other targets.",
            }
            for lane_type in LANE_TYPES
        ],
    }
    claims = (
        "Introduces a carrier mechanism that mediates the local-global pressure.",
        "Supports the route barrier in the protected boundary regime.",
        "The source discusses an orthogonal vocabulary without a catalog match.",
        "Distinguishes the route barrier across two inequivalent regimes.",
        "An open question remains unresolved for the carrier mechanism.",
        "Unifies the carrier mechanism and route barrier through a common mechanism.",
    )
    providers = {}
    for index, lane_type in enumerate(LANE_TYPES):

        def provider(request: dict, index: int = index, lane_type: str = lane_type) -> dict:
            return {
                "provider": f"mapping-fixture-{lane_type}",
                "index": f"mapping-index-{lane_type}",
                "execution_mode": "live",
                "status": "completed",
                "coverage_cutoff": "2026-07-22",
                "sources": [
                    {
                        "work_identity": f"mapping-work-{index}",
                        "title": f"Mapping source {index}",
                        "authors": [f"Author {index}"],
                        "publication_date": "2026",
                        "source_version": "v1",
                        "source_type": "primary",
                        "url": f"https://example.test/mapping/{index}",
                        "correction_status": "none_known",
                        "decision_relevant": True,
                        "claims": [claims[index]],
                        "claim_provenance": [{"exact_claim": claims[index], "claim_origin": "verbatim_source_excerpt", "evidence_locator": f"fixture abstract sentence {index}", "authority_id": "fixture-source-transcription.v1"}],
                        "limitations": [f"Fixture limitation {index}."],
                    }
                ],
            }

        providers[lane_type] = provider
    return run_frontier_literature_cycle(request, providers=providers)


def _catalog(snapshot: dict) -> dict:
    return build_theory_object_catalog(
        target_id=snapshot["target_id"],
        theory_state_digest=snapshot["theory_state_digest"],
        theory_objects=[
            {
                "theory_object_id": "concept.target-scope",
                "object_kind": "concept",
                "label": "Whole target scope",
                "match_terms": ["mapping target"],
                "scope_anchor": True,
            },
            {
                "theory_object_id": "mechanism.carrier",
                "object_kind": "mechanism",
                "label": "Carrier mechanism",
                "match_terms": ["carrier mechanism", "mediates"],
                "scope_anchor": False,
            },
            {
                "theory_object_id": "barrier.route",
                "object_kind": "barrier",
                "label": "Route barrier",
                "match_terms": ["route barrier"],
                "scope_anchor": False,
            },
        ],
    )


def _source_with(snapshot: dict, fragment: str) -> dict:
    return next(
        source
        for source in snapshot["sources"]
        if fragment.lower() in " ".join(source["claims"]).lower()
    )


def _worlds(snapshot: dict) -> list[dict]:
    carrier = _source_with(snapshot, "Introduces a carrier mechanism")
    return [
        {
            "world_id": "deletion",
            "operation": "delete_source",
            "source_id": carrier["source_id"],
            "expected_effect": "change",
        },
        {"world_id": "no-literature", "operation": "no_literature", "expected_effect": "change"},
        {
            "world_id": "superseded",
            "operation": "supersede_source",
            "source_id": carrier["source_id"],
            "expected_effect": "change",
        },
        {
            "world_id": "contradictory",
            "operation": "contradict_source",
            "source_id": carrier["source_id"],
            "contradictory_claim": (
                "A counterexample contradicts the carrier mechanism and rules out its mediation."
            ),
            "expected_effect": "change",
        },
        {
            "world_id": "coverage-null",
            "operation": "coverage_only_change",
            "coverage_limit": "One extra provenance-only coverage qualification.",
            "expected_effect": "null",
        },
    ]


def test_mapping_is_rederived_from_claim_content_with_actual_theory_updates() -> None:
    snapshot = _snapshot()
    catalog = _catalog(snapshot)
    derivation = derive_claim_mappings(snapshot, theory_catalog=catalog)
    assert derivation["derivation_authority"]["authority_id"] == CLAIM_MAPPING_AUTHORITY_ID
    events = {item["event_type"] for item in derivation["theory_mappings"]}
    assert {"spawn", "reprioritize", "split", "new_question", "merge", "justified_no_change"}.issubset(events)
    assert any(item["disposition"] == "spawned" for item in derivation["concept_updates"])
    assert any(item["disposition"] == "opened" for item in derivation["branch_updates"])
    assert derivation["explicit_null_effects"]
    assimilation = assimilate_derived_literature(
        snapshot,
        theory_catalog=catalog,
        mapping_derivation=derivation,
    )
    assert assimilation["mapping_provenance"] == {
        "mode": "deterministic_claim_derivation",
        "derivation_id": derivation["derivation_id"],
        "derivation_digest": derivation["content_digest"],
        "authority_id": CLAIM_MAPPING_AUTHORITY_ID,
        "semantic_claim_layer_id": derivation["semantic_claim_layer"]["layer_id"],
        "semantic_claim_layer_digest": derivation["semantic_claim_layer_digest"],
        "semantic_authority_id": derivation["semantic_claim_layer"]["authority"][
            "authority_id"
        ],
    }


def test_every_distinct_claim_is_retained_and_maximal_object_ties_survive() -> None:
    snapshot = _snapshot()
    source = _source_with(snapshot, "Introduces a carrier mechanism")
    source["claims"] = [
        "Introduces a carrier mechanism that mediates the local-global pressure.",
        "Produces a spectral bridge for the route barrier.",
    ]
    source["claim_provenance"] = _normalize_claim_provenance(
        [
            {
                "exact_claim": source["claims"][0],
                "claim_origin": "verbatim_source_excerpt",
                "evidence_locator": "fixture abstract sentence 0",
                "authority_id": "fixture-source-transcription.v1",
            },
            {
                "exact_claim": source["claims"][1],
                "claim_origin": "verbatim_source_excerpt",
                "evidence_locator": "fixture abstract sentence 0, added claim",
                "authority_id": "fixture-source-transcription.v1",
            },
        ],
        source_id=source["source_id"],
        source_version=source["source_version"],
        correction_status=source["correction_status"],
        claims=source["claims"],
    )
    source["content_digest"] = canonical_digest(
        {key: value for key, value in source.items() if key != "content_digest"}
    )
    snapshot["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in snapshot.items()
            if key not in {"content_digest", "validator_receipts", "validation_status"}
        }
    )
    snapshot["validator_receipts"][0]["validated_digest"] = snapshot["content_digest"]
    snapshot["validator_receipts"][0]["receipt_id"] = expected_snapshot_validator_receipt_id(
        snapshot, snapshot["validator_receipts"][0]["validator_id"]
    )
    catalog = build_theory_object_catalog(
        target_id=snapshot["target_id"],
        theory_state_digest=snapshot["theory_state_digest"],
        theory_objects=_catalog(snapshot)["theory_objects"]
        + [
            {
                "theory_object_id": "mechanism.carrier-tie",
                "object_kind": "mechanism",
                "label": "Carrier mediation tie",
                "match_terms": ["carrier mechanism", "mediates"],
                "scope_anchor": False,
            }
        ],
    )
    derivation = derive_claim_mappings(snapshot, theory_catalog=catalog)
    rows = [row for row in derivation["theory_mappings"] if row["source_id"] == source["source_id"]]
    assert len(rows) == 2
    carrier = next(row for row in rows if "carrier mechanism" in row["exact_claim"].lower())
    assert carrier["theory_object_ids"] == ["mechanism.carrier", "mechanism.carrier-tie"]
    assert len({row["mapping_id"] for row in rows}) == 2


def test_claim_row_removal_cannot_survive_replay_validation() -> None:
    snapshot = _snapshot()
    catalog = _catalog(snapshot)
    derivation = derive_claim_mappings(snapshot, theory_catalog=catalog)
    tampered = copy.deepcopy(derivation)
    removed = tampered["theory_mappings"].pop()
    tampered["mapping_receipts"] = [
        row for row in tampered["mapping_receipts"] if row["mapping_id"] != removed["mapping_id"]
    ]
    tampered["concept_updates"] = [
        row for row in tampered["concept_updates"] if row["mapping_id"] != removed["mapping_id"]
    ]
    tampered["branch_updates"] = [
        row for row in tampered["branch_updates"] if row["mapping_id"] != removed["mapping_id"]
    ]
    tampered["explicit_null_effects"] = [
        row for row in tampered["explicit_null_effects"] if row["mapping_id"] != removed["mapping_id"]
    ]
    tampered["content_digest"] = canonical_digest(
        {key: value for key, value in tampered.items() if key != "content_digest"}
    )
    with pytest.raises(ContractError, match="does not replay"):
        validate_claim_mapping_derivation(
            tampered, snapshot=snapshot, theory_catalog=catalog
        )


def test_registered_literature_protocol_derives_or_validates_bound_mapping_receipt() -> None:
    snapshot = _snapshot()
    catalog = _catalog(snapshot)
    request = {"identity": {"target_id": snapshot["target_id"]}}
    exact_context = {
        "snapshot": snapshot,
        "theory_catalog": catalog,
        "freshness_evaluated_at": snapshot["search_completed_at"],
    }
    derived, _unknowns = _literature(
        request, exact_context
    )
    assert derived["schema_version"] == "4.0"
    assert derived["mapping_provenance"]["mode"] == "deterministic_claim_derivation"
    derivation = derive_claim_mappings(snapshot, theory_catalog=catalog)
    rebound, _unknowns = _literature(
        request,
        {
            **exact_context,
            "mapping_derivation": derivation,
        },
    )
    assert rebound == derived
    with pytest.raises(ContractError, match="cannot also supply manual"):
        _literature(
            request,
            {
                "snapshot": snapshot,
                "theory_catalog": catalog,
                "theory_mappings": derivation["theory_mappings"],
            },
        )


def test_legacy_mapping_api_is_honestly_labeled_manual() -> None:
    snapshot = _snapshot()
    derivation = derive_claim_mappings(snapshot, theory_catalog=_catalog(snapshot))
    packet = assimilate_literature(
        snapshot,
        theory_state_digest=snapshot["theory_state_digest"],
        theory_mappings=derivation["theory_mappings"],
    )
    assert packet["mapping_provenance"]["mode"] == "operator_supplied_interpretive_mapping"
    assert packet["mapping_provenance"]["derivation_digest"] is None
    assert packet["schema_version"] == "2.0"

    historical_v1 = copy.deepcopy(packet)
    historical_v1["schema_version"] = "1.0"
    historical_v1.pop("mapping_provenance")
    historical_v1["content_digest"] = canonical_digest(
        {key: value for key, value in historical_v1.items() if key != "content_digest"}
    )
    validate_assimilation(historical_v1, snapshot=snapshot)

    retrofitted = copy.deepcopy(historical_v1)
    retrofitted["mapping_provenance"] = packet["mapping_provenance"]
    retrofitted["content_digest"] = canonical_digest(
        {key: value for key, value in retrofitted.items() if key != "content_digest"}
    )
    with pytest.raises(ContractError):
        validate_assimilation(retrofitted, snapshot=snapshot)


def test_replay_rebuilds_all_worlds_and_exposes_semantic_null_effect() -> None:
    snapshot = _snapshot()
    catalog = _catalog(snapshot)
    replay = replay_literature_counterfactuals(
        snapshot, theory_catalog=catalog, worlds=_worlds(snapshot)
    )
    results = {item["world_id"]: item for item in replay["world_results"]}
    assert results["deletion"]["effects"]["mapping_or_theory_decision_changed"]
    assert results["no-literature"]["mapping_derivation"]["theory_mappings"] == []
    assert results["no-literature"]["mapping_derivation"]["concept_updates"] == []
    superseded_events = {
        item["event_type"] for item in results["superseded"]["mapping_derivation"]["theory_mappings"]
    }
    assert "reframe" in superseded_events
    contradictory = results["contradictory"]
    contradictory_claim = contradictory["transformation"]["contradictory_claim"]
    contradictory_mapping = next(
        item
        for item in contradictory["mapping_derivation"]["theory_mappings"]
        if item["exact_claim"] == contradictory_claim
    )
    assert contradictory_mapping["semantic_relation"] == "unresolved"
    assert contradictory_mapping["event_type"] == "justified_no_change"
    assert contradictory_mapping["claim_origin"] == "model_extraction"
    contradictory_record = next(
        item
        for item in contradictory["mapping_derivation"]["semantic_claim_layer"][
            "claim_records"
        ]
        if item["exact_claim"] == contradictory_claim
    )
    assert (
        contradictory_record["extraction_provenance"]["authority_class"]
        == "unverified_provider_claim_extraction"
    )
    assert results["coverage-null"]["effects"]["snapshot_digest_changed"]
    assert results["coverage-null"]["effects"]["mapping_packet_digest_changed"]
    assert results["coverage-null"]["effects"]["null_effect"]
    assert results["coverage-null"]["effects"]["semantic_claim_layer_changed"]
    assert results["coverage-null"]["effects"]["semantic_coverage_audit_changed"]
    assert not results["coverage-null"]["effects"]["semantic_relation_decisions_changed"]
    assert replay["null_effect_world_ids"] == ["coverage-null"]
    assert all(
        item["evaluation"]["status"] == "passed"
        for item in replay["world_results"]
    )


def test_source_warrant_overrides_fallback_with_versioned_bounded_authority() -> None:
    snapshot = _snapshot()
    catalog = _catalog(snapshot)
    source = _source_with(snapshot, "Supports the route barrier")
    exact_claim = source["claims"][0]
    fallback = derive_claim_mappings(snapshot, theory_catalog=catalog)
    fallback_mapping = next(
        row for row in fallback["theory_mappings"] if row["source_id"] == source["source_id"]
    )
    assert fallback_mapping["semantic_basis_mode"] == "bounded_lexical_fallback"
    assert fallback_mapping["semantic_relation"] == "entails"

    enriched = bind_source_semantic_warrants(
        snapshot,
        [
            {
                "source_id": source["source_id"],
                "exact_claim": exact_claim,
                "theory_object_ids": ["barrier.route"],
                "relation": "leaves_open",
                "warrant_text": "The fixture audit treats support as leaving the protected-regime transfer open.",
                "evidence_locator": "fixture abstract sentence 1",
            }
        ],
        authority_id="fixture-source-audit.v1",
    )
    layer = build_semantic_claim_layer(enriched, theory_catalog=catalog)
    validate_semantic_claim_layer(layer, snapshot=enriched, theory_catalog=catalog)
    record = next(row for row in layer["claim_records"] if row["source_id"] == source["source_id"])
    assert record["source_state"] == {
        "source_version": "v1",
        "correction_status": "none_known",
        "state_authority": "frozen_snapshot_source_record",
    }
    assert record["effective_relation"] == "leaves_open"
    assert record["basis_mode"] == "source_level_explicit"
    assert record["relation_warrants"][0]["nulls"] == {
        "source_truth_authorized": False,
        "semantic_entailment_authorized": False,
        "novelty_authorized": False,
    }
    assert record["relation_warrants"][0]["authority"]["authority_class"] == "internal_target_semantic_audit"
    assert record["extraction_provenance"]["claim_origin"] == "verbatim_source_excerpt"
    derivation = derive_claim_mappings(enriched, theory_catalog=catalog)
    mapping = next(
        row for row in derivation["theory_mappings"] if row["source_id"] == source["source_id"]
    )
    assert mapping["semantic_relation"] == "leaves_open"
    assert mapping["event_type"] == "new_question"
    assert derivation["semantic_coverage_audit"]["explicit_warrant_claim_count"] == 1
    assert derivation["semantic_coverage_audit"]["truth_authorized"] is False


def test_semantic_warrant_version_correction_and_layer_mutations_fail_closed() -> None:
    snapshot = _snapshot()
    catalog = _catalog(snapshot)
    source = _source_with(snapshot, "carrier mechanism")
    enriched = bind_source_semantic_warrants(
        snapshot,
        [
            {
                "source_id": source["source_id"],
                "exact_claim": source["claims"][0],
                "theory_object_ids": ["mechanism.carrier"],
                "relation": "entails",
                "warrant_text": "Bounded fixture relation only.",
                "evidence_locator": "fixture claim 0",
            }
        ],
        authority_id="fixture-source-audit.v1",
    )
    broken_snapshot = copy.deepcopy(enriched)
    target = next(
        row for row in broken_snapshot["sources"] if row["source_id"] == source["source_id"]
    )
    target["semantic_warrants"][0]["source_version"] = "forged-v99"
    target["content_digest"] = canonical_digest(
        {key: value for key, value in target.items() if key != "content_digest"}
    )
    broken_snapshot["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in broken_snapshot.items()
            if key not in {"content_digest", "validator_receipts", "validation_status"}
        }
    )
    broken_snapshot["validator_receipts"][0]["validated_digest"] = broken_snapshot[
        "content_digest"
    ]
    broken_snapshot["validator_receipts"][0]["receipt_id"] = (
        expected_snapshot_validator_receipt_id(
            broken_snapshot,
            broken_snapshot["validator_receipts"][0]["validator_id"],
        )
    )
    with pytest.raises(ContractError, match="version or correction"):
        derive_claim_mappings(broken_snapshot, theory_catalog=catalog)

    derivation = derive_claim_mappings(enriched, theory_catalog=catalog)
    tampered = copy.deepcopy(derivation)
    tampered["semantic_claim_layer"]["claim_records"][0]["effective_relation"] = "contradicts"
    tampered["semantic_claim_layer"]["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in tampered["semantic_claim_layer"].items()
            if key != "content_digest"
        }
    )
    tampered["semantic_claim_layer_digest"] = tampered["semantic_claim_layer"]["content_digest"]
    tampered["content_digest"] = canonical_digest(
        {key: value for key, value in tampered.items() if key != "content_digest"}
    )
    with pytest.raises(ContractError, match="semantic claim layer|does not replay"):
        validate_claim_mapping_derivation(
            tampered, snapshot=enriched, theory_catalog=catalog
        )


def test_supersession_invalidates_explicit_warrant_and_rebuilds_unresolved_state() -> None:
    snapshot = _snapshot()
    catalog = _catalog(snapshot)
    source = _source_with(snapshot, "carrier mechanism")
    enriched = bind_source_semantic_warrants(
        snapshot,
        [
            {
                "source_id": source["source_id"],
                "exact_claim": source["claims"][0],
                "theory_object_ids": ["mechanism.carrier"],
                "relation": "entails",
                "warrant_text": "Bounded fixture relation only.",
                "evidence_locator": "fixture claim 0",
            }
        ],
        authority_id="fixture-source-audit.v1",
    )
    replay = replay_literature_counterfactuals(
        enriched,
        theory_catalog=catalog,
        worlds=[
            {
                "world_id": "superseded",
                "operation": "supersede_source",
                "source_id": source["source_id"],
                "source_version": "v2-correction",
                "expected_effect": "change",
            },
            {
                "world_id": "coverage-null",
                "operation": "coverage_only_change",
                "coverage_limit": "Additional audit limitation only.",
                "expected_effect": "null",
            },
        ],
    )
    results = {item["world_id"]: item for item in replay["world_results"]}
    superseded = results["superseded"]
    record = next(
        row
        for row in superseded["mapping_derivation"]["semantic_claim_layer"]["claim_records"]
        if row["source_id"] == source["source_id"]
    )
    assert record["source_state"]["source_version"] == "v2-correction"
    assert record["source_state"]["correction_status"] == "superseded"
    assert record["basis_mode"] == "bounded_lexical_fallback"
    assert record["effective_relation"] == "unresolved"
    mapping = next(
        row
        for row in superseded["mapping_derivation"]["theory_mappings"]
        if row["source_id"] == source["source_id"]
    )
    assert mapping["event_type"] == "reframe"
    assert superseded["effects"]["semantic_relation_decisions_changed"]
    coverage = results["coverage-null"]
    assert coverage["effects"]["semantic_coverage_audit_changed"]
    assert coverage["effects"]["null_effect"]


def test_wrong_authority_target_state_and_digests_fail_closed() -> None:
    snapshot = _snapshot()
    catalog = _catalog(snapshot)
    with pytest.raises(ContractError, match="unsupported claim-mapping authority"):
        derive_claim_mappings(snapshot, theory_catalog=catalog, authority_id="operator.claims.v0")

    wrong_target = build_theory_object_catalog(
        target_id="other-target",
        theory_state_digest=snapshot["theory_state_digest"],
        theory_objects=catalog["theory_objects"],
    )
    with pytest.raises(ContractError, match="target differs"):
        derive_claim_mappings(snapshot, theory_catalog=wrong_target)

    wrong_state_snapshot = _snapshot("wrong-state-target")
    wrong_state_catalog = build_theory_object_catalog(
        target_id=snapshot["target_id"],
        theory_state_digest=wrong_state_snapshot["theory_state_digest"],
        theory_objects=catalog["theory_objects"],
    )
    with pytest.raises(ContractError, match="digest binding differs"):
        derive_claim_mappings(snapshot, theory_catalog=wrong_state_catalog)

    tampered_catalog = copy.deepcopy(catalog)
    tampered_catalog["theory_objects"][1]["match_terms"] = ["fabricated term"]
    with pytest.raises(ContractError, match="catalog content digest mismatch"):
        derive_claim_mappings(snapshot, theory_catalog=tampered_catalog)

    derivation = derive_claim_mappings(snapshot, theory_catalog=catalog)
    tampered_derivation = copy.deepcopy(derivation)
    tampered_derivation["snapshot_digest"] = canonical_digest({"wrong": True})
    tampered_derivation["content_digest"] = canonical_digest(
        {key: value for key, value in tampered_derivation.items() if key != "content_digest"}
    )
    with pytest.raises(ContractError, match="snapshot digest mismatch"):
        validate_claim_mapping_derivation(
            tampered_derivation, snapshot=snapshot, theory_catalog=catalog
        )


def test_world_semantics_are_recomputed_not_retained_from_packet() -> None:
    snapshot = _snapshot()
    catalog = _catalog(snapshot)
    replay = replay_literature_counterfactuals(
        snapshot, theory_catalog=catalog, worlds=_worlds(snapshot)
    )
    tampered = copy.deepcopy(replay)
    result = tampered["world_results"][0]
    result["transformation"]["operation"] = "no_literature"
    result["transformation"].pop("source_id")
    result["transformation_digest"] = canonical_digest(result["transformation"])
    result["content_digest"] = canonical_digest(
        {key: value for key, value in result.items() if key != "content_digest"}
    )
    tampered["content_digest"] = canonical_digest(
        {key: value for key, value in tampered.items() if key != "content_digest"}
    )
    with pytest.raises(
        ContractError, match="literature replay transformations must be unique"
    ):
        validate_literature_counterfactual_replay(
            tampered, snapshot=snapshot, theory_catalog=catalog
        )


@pytest.mark.parametrize("claim,claim_origin", [
    ("The paper does not establish that the carrier mechanism supports the route.", "verbatim_source_excerpt"),
    ("The carrier mechanism might support the route barrier.", "verbatim_source_excerpt"),
    ('The phrase "supports the carrier mechanism" appears only in an objection.', "verbatim_source_excerpt"),
    ("The review reports that another author claims the carrier mechanism supports the route.", "verbatim_source_excerpt"),
    ("Supports the carrier mechanism through the route barrier.", "author_paraphrase"),
])
def test_uncertain_lexical_cases_are_unresolved(claim: str, claim_origin: str) -> None:
    snapshot = _snapshot()
    source = snapshot["sources"][0]
    source["claims"], source["semantic_warrants"] = [claim], []
    source["claim_provenance"] = _normalize_claim_provenance(
        [{"exact_claim": claim, "claim_origin": claim_origin, "evidence_locator": "fixture adversarial claim", "authority_id": "fixture-adversarial-origin.v1"}],
        source_id=source["source_id"], source_version=source["source_version"], correction_status=source["correction_status"], claims=source["claims"],
    )
    source["content_digest"] = canonical_digest({key: value for key, value in source.items() if key != "content_digest"})
    snapshot["content_digest"] = canonical_digest({key: value for key, value in snapshot.items() if key not in {"content_digest", "validator_receipts", "validation_status"}})
    snapshot["validator_receipts"][0]["validated_digest"] = snapshot["content_digest"]
    snapshot["validator_receipts"][0]["receipt_id"] = expected_snapshot_validator_receipt_id(
        snapshot, snapshot["validator_receipts"][0]["validator_id"]
    )
    mapping = next(row for row in derive_claim_mappings(snapshot, theory_catalog=_catalog(snapshot))["theory_mappings"] if row["source_id"] == source["source_id"])
    assert mapping["semantic_relation"] == "unresolved" and mapping["event_type"] == "justified_no_change"


def test_counterfactual_transformation_identity_ignores_label() -> None:
    snapshot, catalog = _snapshot(), None
    catalog = _catalog(snapshot)
    source_id = snapshot["sources"][0]["source_id"]
    first = replay_literature_counterfactuals(snapshot, theory_catalog=catalog, worlds=[{"world_id": "label-a", "operation": "delete_source", "source_id": source_id}])
    second = replay_literature_counterfactuals(snapshot, theory_catalog=catalog, worlds=[{"world_id": "label-b", "operation": "delete_source", "source_id": source_id}])
    left, right = first["world_results"][0], second["world_results"][0]
    assert first["causal_replay_id"] == second["causal_replay_id"] and left["transformation_id"] == right["transformation_id"]
    assert left["snapshot"]["content_digest"] == right["snapshot"]["content_digest"] and first["replay_id"] != second["replay_id"]


def test_unmet_declared_counterfactual_control_fails_acceptance() -> None:
    snapshot = _snapshot()
    with pytest.raises(ContractError, match="declared counterfactual control failed"):
        replay_literature_counterfactuals(snapshot, theory_catalog=_catalog(snapshot), worlds=[{"world_id": "false-change-control", "operation": "coverage_only_change", "coverage_limit": "Metadata-only addition.", "expected_effect": "change"}])


def test_standalone_v4_assimilation_recomputes_semantics_events_and_actions() -> None:
    snapshot = _snapshot()
    catalog = _catalog(snapshot)
    derivation = derive_claim_mappings(snapshot, theory_catalog=catalog)
    packet = assimilate_derived_literature(snapshot, theory_catalog=catalog, mapping_derivation=derivation)
    assert packet["schema_version"] == "4.0"
    validate_assimilation(packet)
    tampered = copy.deepcopy(packet)
    tampered["theory_mappings"][0]["event_type"] = "retire"
    tampered["content_digest"] = canonical_digest({key: value for key, value in tampered.items() if key != "content_digest"})
    with pytest.raises(ContractError, match="standalone semantic assimilation"):
        validate_assimilation(tampered)
    catalog_tamper = copy.deepcopy(packet)
    embedded = catalog_tamper["derivation_replay"]["theory_catalog"]
    embedded["theory_objects"][1]["match_terms"] = ["forged semantic term"]
    embedded["content_digest"] = canonical_digest({key: value for key, value in embedded.items() if key != "content_digest"})
    replay = catalog_tamper["derivation_replay"]
    replay["content_digest"] = canonical_digest({key: value for key, value in replay.items() if key != "content_digest"})
    catalog_tamper["content_digest"] = canonical_digest({key: value for key, value in catalog_tamper.items() if key != "content_digest"})
    with pytest.raises(ContractError):
        validate_assimilation(catalog_tamper)


def test_literature_mapping_replay_cli_passes() -> None:
    completed = subprocess.run(
        [sys.executable, "agentic/scripts/validate_literature_claim_mapping_replay.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "literature counterfactual replay: pass" in completed.stdout
