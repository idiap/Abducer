# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial tests for sealed current-literature acquisition authority."""

from __future__ import annotations

import copy
import hashlib
import sys
from pathlib import Path

import pytest

from agentic.discovery.contracts import canonical_digest, canonical_json
from agentic.discovery.literature import LANE_TYPES, run_frontier_literature_cycle
from agentic.discovery.literature_acquisition import (
    LiteratureAcquisitionError,
    reconstruct_normalized_sources,
    top_level_content_digest,
    validate_capture_acquisition_bundle,
    validate_source_routing_consumption,
    validate_source_version_graph,
    validate_tool_response_artifact,
)


TARGET = "yang-mills-existence-and-mass-gap-target"
STAMP = "2026-07-22T10:00:00Z"
QUERIES = {
    "closest_known_work": "Yang-Mills existence mass gap closest constructive result 2026",
    "recent_frontier_preprints": "Yang-Mills lattice mass gap constructive latest preprint 2026",
    "negative_results_barriers": "Yang-Mills continuum reflection positivity barriers 2026",
    "conceptual_genealogy": "Yang-Mills constructive QFT conceptual genealogy 2026",
    "adjacent_field_mechanisms": "Yang-Mills generalized symmetry adjacent mechanism 2026",
    "dissenting_positions": "Yang-Mills claimed proof critique retraction open problem 2026",
}


def _seal(payload: dict, field: str) -> dict:
    payload[field] = top_level_content_digest(payload, field)
    return payload


def _evidence(
    evidence_id: str,
    authority_class: str,
    predicate: str,
    subject: str,
    object_value,
    *,
    record: str,
    source_field: str,
    claim: str | None = None,
) -> dict:
    return _seal(
        {
            "evidence_id": evidence_id,
            "authority_class": authority_class,
            "predicate": predicate,
            "subject": subject,
            "object": object_value,
            "claim_digest": None if claim is None else canonical_digest(claim),
            "source_locator": f"https://zenodo.org/api/records/{record}",
            "source_field": source_field,
        },
        "evidence_digest",
    )


def _source(index: int) -> dict:
    if index < 3:
        record = ("18837540", "19614728", "21479499")[index]
        records = ("18837540", "19614728", "21479499")
        version = ("1.0", "2.0", "3.0")[index]
        correction = ("superseded", "superseded", "none_known")[index]
        publication = ("2026-03-02", "2026-04-16", "2026-07-21")[index]
        created = (
            "2026-03-02T09:00:00Z",
            "2026-04-16T09:00:00Z",
            "2026-07-21T09:00:00Z",
        )[index]
        updated = (
            "2026-03-02T10:00:00Z",
            "2026-04-16T10:00:00Z",
            "2026-07-21T10:00:00Z",
        )[index]
        title = (
            "Volume-uniform functional inequalities",
            "Lattice coercivity and a symmetry-forced Haar measure",
            "Karcher blocking and exact Haar-pivot matching",
        )[index]
        source_id = f"zenodo-{record}"
        record_doi = f"10.5281/zenodo.{record}"
        concept_doi = "10.5281/zenodo.18837539"
        claims = [f"Version {version} makes an unverified construction claim."]
        transition_claims: tuple[str, str, str] | None = None
        if index:
            transition_claims = (
                f"Version {version} explicitly corrects the preceding record.",
                f"Version {version} narrows the stated construction scope.",
                f"Version {version} replaces a load-bearing architecture.",
            )
            claims.extend(transition_claims)
        evidence = [
            _evidence(
                f"record-doi-{record}",
                "primary_repository_metadata",
                "record_doi",
                source_id,
                record_doi,
                record=record,
                source_field="/doi",
            ),
            _evidence(
                f"record-concept-{record}",
                "primary_repository_metadata",
                "record_member_of_concept",
                record_doi,
                concept_doi,
                record=record,
                source_field="/conceptdoi",
            ),
            _evidence(
                f"record-version-{record}",
                "primary_repository_metadata",
                "record_version",
                record_doi,
                version,
                record=record,
                source_field="/metadata/version",
            ),
            _evidence(
                f"record-created-{record}",
                "primary_repository_metadata",
                "record_created_at",
                record_doi,
                created,
                record=record,
                source_field="/created",
            ),
            _evidence(
                f"record-updated-{record}",
                "primary_repository_metadata",
                "record_updated_at",
                record_doi,
                updated,
                record=record,
                source_field="/updated",
            ),
            _evidence(
                f"record-status-{record}",
                "primary_repository_metadata",
                "record_status",
                record_doi,
                "current" if index == 2 else "superseded",
                record=record,
                source_field="/links/latest",
            ),
        ]
        if index == 2:
            evidence.append(
                _evidence(
                    "lineage-membership-18837539",
                    "primary_repository_relation",
                    "lineage_ordered_record_dois",
                    concept_doi,
                    [f"10.5281/zenodo.{item}" for item in records],
                    record=record,
                    source_field="/links/versions",
                )
            )
        if index and transition_claims is not None:
            predecessor_doi = f"10.5281/zenodo.{records[index - 1]}"
            evidence.extend(
                [
                    _evidence(
                        f"revision-{records[index - 1]}-{record}",
                        "primary_repository_relation",
                        "successor_revision_of",
                        record_doi,
                        predecessor_doi,
                        record=record,
                        source_field="/links/prev",
                    ),
                    _evidence(
                        f"supersedes-{records[index - 1]}-{record}",
                        "primary_repository_relation",
                        "successor_supersedes_predecessor",
                        record_doi,
                        predecessor_doi,
                        record=record,
                        source_field="/links/prev",
                    ),
                    _evidence(
                        f"corrects-{records[index - 1]}-{record}",
                        "primary_record_note",
                        "successor_corrects_predecessor",
                        record_doi,
                        predecessor_doi,
                        record=record,
                        source_field="/metadata/notes",
                        claim=transition_claims[0],
                    ),
                    _evidence(
                        f"scope-{records[index - 1]}-{record}",
                        "primary_record_note",
                        "successor_narrows_scope",
                        record_doi,
                        predecessor_doi,
                        record=record,
                        source_field="/metadata/notes",
                        claim=transition_claims[1],
                    ),
                    _evidence(
                        f"architecture-{records[index - 1]}-{record}",
                        "primary_record_note",
                        "successor_changes_architecture",
                        record_doi,
                        predecessor_doi,
                        record=record,
                        source_field="/metadata/notes",
                        claim=transition_claims[2],
                    ),
                ]
            )
        return {
            "source_id": source_id,
            "work_identity": "doi:10.5281/zenodo.18837539",
            "title": title,
            "authors": ["Kirk, Harold D."],
            "publication_date": publication,
            "source_version": version,
            "source_type": "preprint",
            "url": f"https://zenodo.org/records/{record}",
            "doi": record_doi,
            "arxiv_id": None,
            "correction_status": correction,
            "decision_relevant": True,
            "claims": claims,
            "limitations": ["Repository metadata and author claims are not independent proof validation."],
            "lineage_evidence": evidence,
        }
    source_id = ("clay-current", "nature-review-2026", "cambridge-retraction")[index - 3]
    source_type = ("primary", "survey", "retraction")[index - 3]
    correction = ("none_known", "none_known", "retracted")[index - 3]
    return {
        "source_id": source_id,
        "work_identity": f"fixture:{source_id}",
        "title": f"Authority fixture {source_id}",
        "authors": ["Fixture Author"],
        "publication_date": "2026-01-12",
        "source_version": "observed-1",
        "source_type": source_type,
        "url": f"https://example.test/{source_id}",
        "doi": None,
        "arxiv_id": None,
        "correction_status": correction,
        "decision_relevant": True,
        "claims": [f"Bounded fixture claim for {source_id}."],
        "limitations": ["Fixture semantics exercise acquisition authority only."],
    }


def _artifact(index: int, lane_type: str) -> dict:
    lane_id = f"ym-current-{lane_type.replace('_', '-')}"
    observation = _seal(_source(index), "observation_digest")
    excerpt = "Bounded tool visible metadata only"
    item = _seal(
        {
            "item_id": f"tool-item-{index + 1}",
            "provider_rank": 0,
            "title": observation["title"],
            "url": observation["url"],
            "displayed_publication": observation["publication_date"],
            "bounded_excerpt": excerpt,
            "excerpt_word_count": len(excerpt.split()),
            "retrieval_class": "primary_page_metadata",
            "source_observation": observation,
        },
        "item_digest",
    )
    request = _seal(
        {
            "tool_name": "web.run",
            "search_query": {"q": QUERIES[lane_type]},
            "response_length": "long",
        },
        "request_digest",
    )
    disposition = (
        "included_authoritative_status"
        if index == 3
        else "included_current_review"
        if index == 4
        else "included_correction_or_supersession"
        if index in {0, 1, 5}
        else "included_unverified_challenger"
    )
    items = [item]
    links = [
        {
            "item_id": item["item_id"],
            "capture_result_id": f"CURRENT-{index + 1:03d}",
            "source_id": observation["source_id"],
            "disposition": disposition,
            "reason": "The record changes the bounded target audit or version state.",
        }
    ]
    if index == 5:
        mismatch_observation = _seal(
            {
                "source_id": "excluded-classical-gap",
                "work_identity": "fixture:excluded-classical-gap",
                "title": "Classical energy-gap result outside the Yang-Mills target",
                "authors": ["Fixture Author"],
                "publication_date": "2026-02-01",
                "source_version": "observed-1",
                "source_type": "other",
                "url": "https://example.test/excluded-classical-gap",
                "doi": None,
                "arxiv_id": None,
                "correction_status": "none_known",
                "decision_relevant": False,
                "claims": ["This result addresses a different energy-gap target."],
                "limitations": ["It cannot support the Yang-Mills existence and mass-gap target."],
            },
            "observation_digest",
        )
        mismatch_excerpt = "Different target retained only for negative surveillance"
        mismatch_item = _seal(
            {
                "item_id": "tool-item-target-mismatch",
                "provider_rank": 1,
                "title": mismatch_observation["title"],
                "url": mismatch_observation["url"],
                "displayed_publication": mismatch_observation["publication_date"],
                "bounded_excerpt": mismatch_excerpt,
                "excerpt_word_count": len(mismatch_excerpt.split()),
                "retrieval_class": "search_result_metadata",
                "source_observation": mismatch_observation,
            },
            "item_digest",
        )
        items.append(mismatch_item)
        links.append(
            {
                "item_id": mismatch_item["item_id"],
                "capture_result_id": "CURRENT-007",
                "source_id": mismatch_observation["source_id"],
                "disposition": "excluded_target_mismatch",
                "reason": "Retained as an explicit target-mismatch negative control.",
            }
        )
    return _seal(
        {
            "schema_version": "1.0",
            "artifact_kind": "codex_tool_visible_search_response",
            "target_id": TARGET,
            "lane_id": lane_id,
            "lane_type": lane_type,
            "request": request,
            "execution": {
                "tool_call_id": f"web-search-{index + 1}",
                "observed_started_at": STAMP,
                "observed_completed_at": STAMP,
                "execution_mode": "live_tool_call",
                "external_provider_request_id": None,
                "external_authentication_status": "unavailable",
                "exposure_boundary": (
                    "Only bounded result metadata exposed by the Codex web tool is retained; "
                    "raw provider HTTP, index state, and ranking traces were not exposed."
                ),
            },
            "response_exposure": {
                "capture_mode": "bounded_tool_visible_result_metadata",
                "complete_backend_payload_available": False,
                "complete_ranking_trace_available": False,
                "selected_result_count": len(items),
                "selection_rule": (
                    "Retain the decision-relevant primary or correction record and any explicit "
                    "negative-surveillance control selected for this fixture lane."
                ),
            },
            "result_items": items,
            "normalization_links": links,
            "claim_boundary": {
                "source_truth_authority": False,
                "peer_review_authority": False,
                "exhaustiveness_authority": False,
                "novelty_authority": False,
                "allowed_use": "bounded discovery routing and explicit claim-audit creation only",
            },
        },
        "content_digest",
    )


def _artifacts() -> list[dict]:
    return [_artifact(index, lane_type) for index, lane_type in enumerate(LANE_TYPES)]


def _artifact_v2_from_v1(artifact: dict, *, bind_api: bool = False) -> dict:
    """Migrate a fixture to the multi-execution envelope without changing content."""

    web_request = _seal(
        {
            "request_id": f"request-{artifact['lane_id']}-web",
            "operation": "search_query",
            "locator": artifact["request"]["search_query"]["q"],
            "domains": [],
            "response_length": artifact["request"]["response_length"],
        },
        "request_digest",
    )
    web_execution = _seal(
        {
            "execution_id": f"execution-{artifact['lane_id']}-web",
            "tool_name": "web.run",
            "request": web_request,
            "observed_started_at": artifact["execution"]["observed_started_at"],
            "observed_completed_at": artifact["execution"]["observed_completed_at"],
            "execution_mode": "agent_observed_tool_call",
            "external_provider_request_id": None,
            "external_authentication_status": "unavailable",
            "complete_response_available_to_agent": False,
            "raw_response_retained": False,
            "response_projection_mode": "bounded_tool_visible_metadata",
            "observation_authority": "agent_recorded_unauthenticated_execution",
            "exposure_boundary": "The tool exposed bounded metadata without a provider receipt.",
        },
        "execution_digest",
    )
    item_ids = [item["item_id"] for item in artifact["result_items"]]
    evidence_ids = [
        row["evidence_id"]
        for item in artifact["result_items"]
        for row in item["source_observation"].get("lineage_evidence", [])
    ]
    executions = [web_execution]
    bindings = [
        _seal(
            {
                "execution_id": web_execution["execution_id"],
                "item_ids": item_ids,
                "lineage_evidence_ids": [] if bind_api else evidence_ids,
            },
            "binding_digest",
        )
    ]
    items = copy.deepcopy(artifact["result_items"])
    if bind_api:
        assert len(items) == 1
        items[0]["retrieval_class"] = "primary_api_metadata"
        _seal(items[0], "item_digest")
        locator = items[0]["source_observation"]["lineage_evidence"][0]["source_locator"]
        api_request = _seal(
            {
                "request_id": f"request-{artifact['lane_id']}-api",
                "operation": "https_get",
                "locator": locator,
                "domains": [],
                "response_length": None,
            },
            "request_digest",
        )
        api_execution = _seal(
            {
                "execution_id": f"execution-{artifact['lane_id']}-api",
                "tool_name": "zenodo.records-api",
                "request": api_request,
                "observed_started_at": STAMP,
                "observed_completed_at": STAMP,
                "execution_mode": "agent_observed_https_request",
                "external_provider_request_id": None,
                "external_authentication_status": "unavailable",
                "complete_response_available_to_agent": True,
                "raw_response_retained": False,
                "response_projection_mode": "bounded_primary_api_metadata",
                "observation_authority": "agent_recorded_unauthenticated_execution",
                "exposure_boundary": "The response was observed but only a bounded projection is sealed.",
            },
            "execution_digest",
        )
        executions.append(api_execution)
        bindings.append(
            _seal(
                {
                    "execution_id": api_execution["execution_id"],
                    "item_ids": item_ids,
                    "lineage_evidence_ids": evidence_ids,
                },
                "binding_digest",
            )
        )
    return _seal(
        {
            "schema_version": "2.0",
            "artifact_kind": "codex_multi_execution_literature_observation",
            "target_id": artifact["target_id"],
            "lane_id": artifact["lane_id"],
            "lane_type": artifact["lane_type"],
            "executions": executions,
            "execution_bindings": bindings,
            "response_exposure": {
                "capture_mode": "bounded_multi_execution_metadata_projection",
                "complete_backend_payload_available": False,
                "complete_ranking_trace_available": False,
                "selected_result_count": len(items),
                "lane_outcome": "completed_with_results",
                "selection_rule": "Retain the exact bounded fixture items.",
            },
            "result_items": items,
            "normalization_links": copy.deepcopy(artifact["normalization_links"]),
            "claim_boundary": {
                **copy.deepcopy(artifact["claim_boundary"]),
                "provider_authentication_authority": False,
            },
        },
        "content_digest",
    )


def _binding(artifact: dict, evidence_id: str) -> dict:
    item = artifact["result_items"][0]
    observation = item["source_observation"]
    evidence = next(
        row for row in observation["lineage_evidence"] if row["evidence_id"] == evidence_id
    )
    return {
        "artifact_lane_id": artifact["lane_id"],
        "artifact_content_digest": artifact["content_digest"],
        "item_id": item["item_id"],
        "item_digest": item["item_digest"],
        "source_id": observation["source_id"],
        "observation_digest": observation["observation_digest"],
        "evidence_id": evidence_id,
        "evidence_digest": evidence["evidence_digest"],
        "evidence_kind": evidence["authority_class"],
    }


def _relation(artifact: dict, relation: str, evidence_id: str) -> dict:
    binding = _binding(artifact, evidence_id)
    evidence = next(
        row
        for row in artifact["result_items"][0]["source_observation"]["lineage_evidence"]
        if row["evidence_id"] == evidence_id
    )
    return _seal(
        {
            "relation": relation,
            "claim_digests": [] if evidence["claim_digest"] is None else [evidence["claim_digest"]],
            "evidence_bindings": [binding],
        },
        "relation_digest",
    )


def _delta(artifact: dict, classification: str, evidence_id: str) -> dict:
    binding = _binding(artifact, evidence_id)
    evidence = next(
        row
        for row in artifact["result_items"][0]["source_observation"]["lineage_evidence"]
        if row["evidence_id"] == evidence_id
    )
    return _seal(
        {
            "classification": classification,
            "claim_digests": [] if evidence["claim_digest"] is None else [evidence["claim_digest"]],
            "evidence_bindings": [binding],
        },
        "delta_digest",
    )


def _version_graph(artifacts: list[dict]) -> dict:
    versions = []
    records = ("18837540", "19614728", "21479499")
    dates = ("2026-03-02", "2026-04-16", "2026-07-21")
    created = (
        "2026-03-02T09:00:00Z",
        "2026-04-16T09:00:00Z",
        "2026-07-21T09:00:00Z",
    )
    updated = (
        "2026-03-02T10:00:00Z",
        "2026-04-16T10:00:00Z",
        "2026-07-21T10:00:00Z",
    )
    for index, record in enumerate(records):
        versions.append(
            {
                "ordinal": index + 1,
                "source_id": f"zenodo-{record}",
                "record_doi": f"10.5281/zenodo.{record}",
                "source_version": f"{index + 1}.0",
                "publication_date": dates[index],
                "repository_created_at": created[index],
                "repository_updated_at": updated[index],
                "status": "current" if index == 2 else "superseded",
                "decision_role": (
                    "current_unverified_claim_audit"
                    if index == 2
                    else "historical_correction_context_only"
                ),
                "present_investment_eligibility": (
                    "unverified_audit_only" if index == 2 else "blocked_positive_support"
                ),
                "predecessor_source_id": None if index == 0 else f"zenodo-{records[index - 1]}",
                "successor_source_id": None if index == 2 else f"zenodo-{records[index + 1]}",
                "identity_evidence_bindings": [
                    _binding(artifacts[index], f"record-doi-{record}"),
                    _binding(artifacts[index], f"record-concept-{record}"),
                    _binding(artifacts[index], f"record-version-{record}"),
                ],
                "ordering_evidence_bindings": [
                    _binding(artifacts[index], f"record-created-{record}"),
                    _binding(artifacts[index], f"record-updated-{record}"),
                ],
                "status_evidence_bindings": [
                    _binding(artifacts[index], f"record-status-{record}")
                ],
                "claim_authority": "unverified_author_claims_only",
            }
        )
    edges = []
    for index in range(2):
        successor_artifact = artifacts[index + 1]
        transition = f"{records[index]}-{records[index + 1]}"
        edges.append(
            _seal(
                {
                    "edge_id": f"zenodo-lineage-edge-{index + 1}",
                    "from_source_id": f"zenodo-{records[index]}",
                    "to_source_id": f"zenodo-{records[index + 1]}",
                    "relations": [
                        _relation(successor_artifact, "revision", f"revision-{transition}"),
                        _relation(successor_artifact, "supersedes", f"supersedes-{transition}"),
                        _relation(successor_artifact, "corrects", f"corrects-{transition}"),
                        _relation(successor_artifact, "narrows_scope", f"scope-{transition}"),
                        _relation(
                            successor_artifact,
                            "changes_architecture",
                            f"architecture-{transition}",
                        ),
                    ],
                    "scope_delta": _delta(
                        successor_artifact, "narrowed", f"scope-{transition}"
                    ),
                    "architecture_delta": _delta(
                        successor_artifact, "changed", f"architecture-{transition}"
                    ),
                },
                "edge_digest",
            )
        )
    return _seal(
        {
            "schema_version": "2.0",
            "graph_id": "zenodo-18837539-lineage",
            "target_id": TARGET,
            "work_identity": "doi:10.5281/zenodo.18837539",
            "concept_doi": "10.5281/zenodo.18837539",
            "observed_at": STAMP,
            "terminal_source_id": "zenodo-21479499",
            "current_source_id": "zenodo-21479499",
            "lineage_membership": _seal(
                {
                    "ordered_record_dois": [
                        f"10.5281/zenodo.{record}" for record in records
                    ],
                    "evidence_bindings": [
                        _binding(artifacts[2], "lineage-membership-18837539")
                    ],
                },
                "membership_digest",
            ),
            "versions": versions,
            "edges": edges,
            "authority_boundary": {
                "version_metadata_authority": "primary_repository_record_plus_sealed_tool_visible_capture",
                "claim_truth_authority": False,
                "peer_validation_authority": False,
                "allowed_use": "supersession-aware discovery routing and claim-specific audit creation",
            },
        },
        "content_digest",
    )


def _bundle(monkeypatch: pytest.MonkeyPatch) -> tuple[dict, dict, dict[str, tuple[dict, bytes]], dict]:
    artifacts = _artifacts()
    monkeypatch.setattr("agentic.discovery.literature.utc_now", lambda: STAMP)
    lanes = []
    providers = {}
    for artifact in artifacts:
        lane_type = artifact["lane_type"]
        lanes.append(
            {
                "lane_id": artifact["lane_id"],
                "lane_type": lane_type,
                "queries": [QUERIES[lane_type]],
                "inclusion_policy": "Include the exact fixture observation.",
                "exclusion_policy": "Exclude target mismatch and unbound metadata.",
            }
        )
        raw_source = copy.deepcopy(artifact["result_items"][0]["source_observation"])
        raw_source.pop("observation_digest")

        def provider(_request: dict, *, source: dict = raw_source, lane_type: str = lane_type) -> dict:
            return {
                "provider": "openai-web-search-tool-visible-capture",
                "index": f"tool-visible-{lane_type}",
                "execution_mode": "live",
                "status": "completed",
                "coverage_cutoff": STAMP,
                "sources": [copy.deepcopy(source)],
            }

        providers[lane_type] = provider
    acquisition = run_frontier_literature_cycle(
        {
            "target_id": TARGET,
            "claim_scope": "fixture authority boundary",
            "theory_state_digest": canonical_digest({"target": TARGET, "generation": 0}),
            "coverage_cutoff": STAMP,
            "coverage_limits": ["Fixture search is bounded and non-exhaustive."],
            "inclusion_policy": "Include exact decision-relevant fixture observations.",
            "exclusion_policy": "Exclude target mismatches.",
            "search_lanes": lanes,
        },
        providers=providers,
    )
    graph = _version_graph(artifacts)
    artifacts_by_path = {}
    descriptors = []
    raw_results = []
    capture_lanes = []
    for artifact, receipt in zip(
        sorted(artifacts, key=lambda row: LANE_TYPES.index(row["lane_type"])),
        sorted(acquisition["lane_receipts"], key=lambda row: LANE_TYPES.index(row["lane_type"])),
        strict=True,
    ):
        path = f"tool-responses/{artifact['lane_id']}.json"
        data = canonical_json(artifact) + b"\n"
        artifacts_by_path[path] = (artifact, data)
        descriptors.append(
            {
                "lane_id": artifact["lane_id"],
                "path": path,
                "sha256": hashlib.sha256(data).hexdigest(),
                "size_bytes": len(data),
                "acquired_at": receipt["completed_at"],
                "provider_request_id": artifact["execution"]["tool_call_id"],
                "source_ids": list(receipt["source_ids"]),
            }
        )
        item_by_id = {item["item_id"]: item for item in artifact["result_items"]}
        lane_result_ids = []
        for link in artifact["normalization_links"]:
            item = item_by_id[link["item_id"]]
            lane_result_ids.append(link["capture_result_id"])
            index_by_source = {
                "zenodo-18837540": ("correction_context", ["correction", "supersession"]),
                "zenodo-19614728": ("correction_context", ["correction", "supersession"]),
                "zenodo-21479499": ("unverified_challenger", ["direct_claim"]),
                "clay-current": ("authoritative_open_status", ["authoritative_status"]),
                "nature-review-2026": (
                    "current_review_boundary",
                    ["current_review", "conceptual_genealogy", "adjacent_field"],
                ),
                "cambridge-retraction": (
                    "correction_context",
                    ["correction", "withdrawal"],
                ),
                "excluded-classical-gap": (
                    "excluded_target_mismatch",
                    ["target_mismatch"],
                ),
            }
            claim_status, surveillance_tags = index_by_source[link["source_id"]]
            if link["source_id"] == "zenodo-21479499":
                surveillance_tags = [*surveillance_tags, "bounded_lattice"]
            retrieval_status = {
                "search_result_metadata": "tool_visible_search_metadata_captured",
                "primary_page_metadata": "primary_page_metadata_captured",
                "primary_api_metadata": "primary_api_metadata_captured",
                "publisher_metadata": "publisher_metadata_captured",
            }[item["retrieval_class"]]
            raw_results.append(
                {
                    "result_id": link["capture_result_id"],
                    "source_id": link["source_id"],
                    "title": item["title"],
                    "url": item["url"],
                    "retrieval_status": retrieval_status,
                    "disposition": link["disposition"],
                    "reason": link["reason"],
                    "claim_status": claim_status,
                    "surveillance_tags": surveillance_tags,
                }
            )
        capture_lanes.append(
            {
                "lane_id": artifact["lane_id"],
                "lane_type": artifact["lane_type"],
                "queries": [artifact["request"]["search_query"]["q"]],
                "query_policy": "No known identifier was seeded.",
                "status": "completed",
                "raw_result_ids": lane_result_ids,
            }
        )
    capture = _seal(
        {
            "schema_version": "2.0",
            "capture_id": "ym-current-fixture",
            "target_id": TARGET,
            "capture_started_at": STAMP,
            "capture_completed_at": STAMP,
            "coverage_cutoff": STAMP,
            "capture_mode": "live_external_web_search_frozen_for_replay",
            "provider": {
                "provider_id": "openai-web-search",
                "name": "Codex web search tool",
                "index": "bounded tool-visible result representation",
                "execution_boundary": "The tool exposed bounded result metadata only.",
                "raw_payload_retention": "No provider HTTP payload or ranking trace was exposed.",
                "receipt_status": "externally_executed_then_frozen",
                "executable_replay_status": "frozen_response_adapter_only",
                "external_authentication_status": "unavailable",
            },
            "exhaustive_coverage_claim": False,
            "peer_validation_claim": False,
            "source_correctness_claim": False,
            "coverage_limits": [
                "The six fixture queries are bounded and non-exhaustive.",
                "Search-provider ranking internals were unavailable.",
                "No raw provider HTTP payload was exposed.",
                "Metadata capture does not validate source claims.",
                "Correction surveillance is bounded to selected records.",
                "The fixture does not establish novelty or peer consensus.",
            ],
            "inclusion_policy": "Include exact decision-relevant observations and explicit surveillance controls.",
            "exclusion_policy": "Exclude mismatched results from normalized evidence while retaining their audit row.",
            "lanes": capture_lanes,
            "raw_results": raw_results,
            "provider_response_artifacts": descriptors,
            "version_lineages": [graph],
        },
        "content_digest",
    )
    return capture, acquisition, artifacts_by_path, graph


def test_tool_response_and_version_graph_accept_exact_sealed_bytes() -> None:
    artifacts = _artifacts()
    for artifact in artifacts:
        validate_tool_response_artifact(artifact)
    sources = reconstruct_normalized_sources(artifacts)
    validate_source_version_graph(_version_graph(artifacts), artifacts=artifacts, sources=sources)
    assert {source["source_id"] for source in sources}.issuperset(
        {"zenodo-18837540", "zenodo-19614728", "zenodo-21479499"}
    )


def test_tool_response_nested_rehash_is_required() -> None:
    artifact = _artifacts()[0]
    artifact["result_items"][0]["source_observation"]["claims"] = ["Altered claim."]
    _seal(artifact, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_tool_response_artifact(artifact)
    assert caught.value.reason_code == "source_observation_digest_mismatch"


@pytest.mark.parametrize(
    ("mutation", "reason_code"),
    [
        (
            lambda graph: graph["versions"][1].update(predecessor_source_id=None),
            "version_neighbor_mismatch",
        ),
        (
            lambda graph: graph["versions"][2].update(status="superseded"),
            "version_routing_role_mismatch",
        ),
        (
            lambda graph: graph["edges"][0].update(to_source_id="zenodo-21479499"),
            "version_edge_digest_mismatch",
        ),
        (
            lambda graph: graph["versions"][0]["identity_evidence_bindings"][0].update(
                item_id="missing-item"
            ),
            "version_item_binding_missing",
        ),
    ],
)
def test_version_graph_rejects_chain_and_evidence_forgery(mutation, reason_code: str) -> None:
    artifacts = _artifacts()
    graph = _version_graph(artifacts)
    mutation(graph)
    _seal(graph, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts)
    assert caught.value.reason_code == reason_code


def test_capture_bundle_reconstructs_every_source_field(monkeypatch: pytest.MonkeyPatch) -> None:
    capture, acquisition, artifacts_by_path, graph = _bundle(monkeypatch)
    authority = validate_capture_acquisition_bundle(
        capture=capture,
        acquisition=acquisition,
        artifacts_by_path=artifacts_by_path,
        version_graphs=[graph],
    )
    assert authority["acquisition_content_digest"] == acquisition["content_digest"]
    assert authority["source_ids"] == sorted(source["source_id"] for source in acquisition["sources"])


def test_target_integration_accepts_the_strict_current_capture(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    capture, _acquisition, _artifacts_by_path, _graph = _bundle(monkeypatch)
    scripts = Path(__file__).resolve().parents[2] / "agentic" / "scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    import integrate_ym_representational_dynamics_20260721 as integration

    integration.validate_frontier_search_capture(capture)


def test_same_source_ids_with_rehashed_claim_forgery_do_not_pass(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    capture, acquisition, artifacts_by_path, graph = _bundle(monkeypatch)
    path = next(
        path for path, (artifact, _data) in artifacts_by_path.items()
        if artifact["lane_type"] == "conceptual_genealogy"
    )
    artifact = copy.deepcopy(artifacts_by_path[path][0])
    observation = artifact["result_items"][0]["source_observation"]
    observation["claims"] = ["A fully rehashed but unobserved substitute claim."]
    _seal(observation, "observation_digest")
    _seal(artifact["result_items"][0], "item_digest")
    _seal(artifact, "content_digest")
    data = canonical_json(artifact) + b"\n"
    artifacts_by_path[path] = (artifact, data)
    descriptor = next(row for row in capture["provider_response_artifacts"] if row["path"] == path)
    descriptor["sha256"] = hashlib.sha256(data).hexdigest()
    descriptor["size_bytes"] = len(data)
    _seal(capture, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_capture_acquisition_bundle(
            capture=capture,
            acquisition=acquisition,
            artifacts_by_path=artifacts_by_path,
            version_graphs=[graph],
        )
    assert caught.value.reason_code == "acquisition_source_reconstruction_mismatch"


def test_response_descriptor_cannot_cross_bind_another_lane(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    capture, acquisition, artifacts_by_path, graph = _bundle(monkeypatch)
    first, second = capture["provider_response_artifacts"][:2]
    first["provider_request_id"] = second["provider_request_id"]
    _seal(capture, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_capture_acquisition_bundle(
            capture=capture,
            acquisition=acquisition,
            artifacts_by_path=artifacts_by_path,
            version_graphs=[graph],
        )
    assert caught.value.reason_code == "response_lane_semantic_mismatch"


def test_capture_rejects_orphan_result(monkeypatch: pytest.MonkeyPatch) -> None:
    capture, acquisition, artifacts_by_path, graph = _bundle(monkeypatch)
    capture["raw_results"].append(
        {
            "result_id": "ORPHAN",
            "source_id": "orphan",
            "title": "Orphan",
            "url": "https://example.test/orphan",
            "retrieval_status": "tool_visible_search_metadata_captured",
            "disposition": "excluded_target_mismatch",
            "reason": "Unbound fixture row.",
            "claim_status": "excluded_target_mismatch",
            "surveillance_tags": ["target_mismatch"],
        }
    )
    _seal(capture, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_capture_acquisition_bundle(
            capture=capture,
            acquisition=acquisition,
            artifacts_by_path=artifacts_by_path,
            version_graphs=[graph],
        )
    assert caught.value.reason_code == "capture_result_orphan"


def test_version_evidence_cannot_bind_another_source() -> None:
    artifacts = _artifacts()
    graph = _version_graph(artifacts)
    graph["versions"][0]["identity_evidence_bindings"][0] = _binding(
        artifacts[1], "record-doi-19614728"
    )
    _seal(graph, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts)
    assert caught.value.reason_code == "version_evidence_source_mismatch"


def test_cross_target_artifact_set_is_rejected() -> None:
    artifacts = _artifacts()
    artifacts[-1]["target_id"] = "another-target"
    _seal(artifacts[-1], "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(_version_graph(artifacts), artifacts=artifacts)
    assert caught.value.reason_code == "tool_target_set_mismatch"


def test_bad_capture_digest_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    capture, acquisition, artifacts_by_path, graph = _bundle(monkeypatch)
    capture["inclusion_policy"] = "Forged after sealing."
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_capture_acquisition_bundle(
            capture=capture,
            acquisition=acquisition,
            artifacts_by_path=artifacts_by_path,
            version_graphs=[graph],
        )
    assert caught.value.reason_code == "capture_digest_mismatch"


def test_extra_loaded_response_file_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    capture, acquisition, artifacts_by_path, graph = _bundle(monkeypatch)
    artifacts_by_path["tool-responses/unbound.json"] = next(iter(artifacts_by_path.values()))
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_capture_acquisition_bundle(
            capture=capture,
            acquisition=acquisition,
            artifacts_by_path=artifacts_by_path,
            version_graphs=[graph],
        )
    assert caught.value.reason_code == "response_artifact_set_mismatch"


def test_tool_item_title_must_match_observation() -> None:
    artifact = _artifacts()[0]
    artifact["result_items"][0]["title"] = "Relabelled title"
    _seal(artifact["result_items"][0], "item_digest")
    _seal(artifact, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_tool_response_artifact(artifact)
    assert caught.value.reason_code == "tool_item_observation_metadata_mismatch"


def test_top_level_digest_does_not_erase_nested_self_hash_names() -> None:
    payload = {"nested": {"content_digest": "scientific-value"}}
    baseline = top_level_content_digest(payload, "content_digest")
    payload["nested"]["content_digest"] = "different-scientific-value"
    assert top_level_content_digest(payload, "content_digest") != baseline


def _reseal_artifact(artifact: dict) -> None:
    item = artifact["result_items"][0]
    observation = item["source_observation"]
    _seal(observation, "observation_digest")
    _seal(item, "item_digest")
    _seal(artifact, "content_digest")


def _terminal_singleton(status: str) -> tuple[list[dict], dict]:
    artifacts = _artifacts()
    artifact = artifacts[2]
    observation = artifact["result_items"][0]["source_observation"]
    evidence = {row["evidence_id"]: row for row in observation["lineage_evidence"]}
    status_atom = evidence["record-status-21479499"]
    status_atom["object"] = status
    if status in {"corrected", "withdrawn", "retracted"}:
        claim = f"The terminal repository record is explicitly {status}."
        observation["claims"].append(claim)
        status_atom["claim_digest"] = canonical_digest(claim)
        status_atom["authority_class"] = (
            "primary_record_note" if status == "corrected" else "publisher_status_notice"
        )
    _seal(status_atom, "evidence_digest")
    membership_atom = evidence["lineage-membership-18837539"]
    membership_atom["object"] = ["10.5281/zenodo.21479499"]
    _seal(membership_atom, "evidence_digest")
    observation["correction_status"] = "none_known" if status == "current" else status
    _reseal_artifact(artifact)
    graph = _version_graph(artifacts)
    terminal = graph["versions"][2]
    terminal.update(
        ordinal=1,
        predecessor_source_id=None,
        successor_source_id=None,
        status=status,
        decision_role=(
            "negative_withdrawal_evidence"
            if status in {"withdrawn", "retracted"}
            else "current_unverified_claim_audit"
        ),
        present_investment_eligibility=(
            "negative_evidence_only"
            if status in {"withdrawn", "retracted"}
            else "unverified_audit_only"
        ),
        status_evidence_bindings=[_binding(artifact, "record-status-21479499")],
    )
    graph["versions"] = [terminal]
    graph["edges"] = []
    graph["terminal_source_id"] = terminal["source_id"]
    graph["current_source_id"] = (
        None if status in {"withdrawn", "retracted"} else terminal["source_id"]
    )
    graph["lineage_membership"] = _seal(
        {
            "ordered_record_dois": [terminal["record_doi"]],
            "evidence_bindings": [
                _binding(artifact, "lineage-membership-18837539")
            ],
        },
        "membership_digest",
    )
    _seal(graph, "content_digest")
    return artifacts, graph


def test_graph_only_concept_and_work_identity_forgery_is_rejected() -> None:
    artifacts = _artifacts()
    graph = _version_graph(artifacts)
    graph["concept_doi"] = "10.5281/zenodo.99999999"
    graph["work_identity"] = "doi:10.5281/zenodo.99999999"
    _seal(graph, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts)
    assert caught.value.reason_code == "version_membership_evidence_mismatch"


def test_graph_only_record_identity_forgery_is_rejected() -> None:
    artifacts = _artifacts()
    graph = _version_graph(artifacts)
    graph["versions"][0]["record_doi"] = "10.5281/zenodo.99999998"
    graph["lineage_membership"]["ordered_record_dois"][0] = "10.5281/zenodo.99999998"
    _seal(graph["lineage_membership"], "membership_digest")
    _seal(graph, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts)
    assert caught.value.reason_code == "version_membership_evidence_mismatch"


def test_fully_rehashed_missing_middle_version_fails_repository_membership() -> None:
    artifacts = _artifacts()
    graph = _version_graph(artifacts)
    first, terminal = graph["versions"][0], graph["versions"][2]
    first["successor_source_id"] = terminal["source_id"]
    terminal.update(ordinal=2, predecessor_source_id=first["source_id"])
    graph["versions"] = [first, terminal]
    graph["lineage_membership"]["ordered_record_dois"] = [
        first["record_doi"],
        terminal["record_doi"],
    ]
    _seal(graph["lineage_membership"], "membership_digest")
    graph["edges"] = []
    _seal(graph, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts)
    assert caught.value.reason_code == "version_membership_evidence_mismatch"


def test_fully_rehashed_relation_relabel_fails_exact_predicate_binding() -> None:
    artifacts = _artifacts()
    graph = _version_graph(artifacts)
    relation = graph["edges"][0]["relations"][2]
    relation["relation"] = "broadens_scope"
    _seal(relation, "relation_digest")
    _seal(graph["edges"][0], "edge_digest")
    _seal(graph, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts)
    assert caught.value.reason_code == "version_relation_evidence_mismatch"


def test_fully_rehashed_scope_delta_relabel_fails_exact_predicate_binding() -> None:
    artifacts = _artifacts()
    graph = _version_graph(artifacts)
    delta = graph["edges"][0]["scope_delta"]
    delta["classification"] = "broadened"
    _seal(delta, "delta_digest")
    _seal(graph["edges"][0], "edge_digest")
    _seal(graph, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts)
    assert caught.value.reason_code == "version_scope_delta_evidence_mismatch"


def test_unknown_edge_endpoint_has_stable_reason_after_edge_rehash() -> None:
    artifacts = _artifacts()
    graph = _version_graph(artifacts)
    graph["edges"][0]["to_source_id"] = "missing-source"
    _seal(graph["edges"][0], "edge_digest")
    _seal(graph, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts)
    assert caught.value.reason_code == "version_edge_endpoint_unknown"


def test_claim_mutation_cannot_preserve_lineage_evidence_digest() -> None:
    artifact = _artifacts()[1]
    observation = artifact["result_items"][0]["source_observation"]
    observation["claims"][1] = "A substituted correction claim."
    _reseal_artifact(artifact)
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_tool_response_artifact(artifact)
    assert caught.value.reason_code == "lineage_evidence_claim_digest_mismatch"


@pytest.mark.parametrize("status", ["current", "corrected", "withdrawn", "retracted"])
def test_singleton_terminal_status_algebra_is_valid(status: str) -> None:
    artifacts, graph = _terminal_singleton(status)
    validate_source_version_graph(graph, artifacts=artifacts)


@pytest.mark.parametrize("status", ["withdrawn", "retracted"])
def test_negative_terminal_cannot_name_a_current_source(status: str) -> None:
    artifacts, graph = _terminal_singleton(status)
    graph["current_source_id"] = graph["terminal_source_id"]
    _seal(graph, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts)
    assert caught.value.reason_code == "version_current_source_mismatch"


def test_same_day_versions_use_repository_timestamps_and_doi_tiebreaker() -> None:
    artifacts = _artifacts()
    common_created = "2026-07-21T09:00:00Z"
    common_updated = "2026-07-21T10:00:00Z"
    for artifact in artifacts[:3]:
        observation = artifact["result_items"][0]["source_observation"]
        for evidence in observation["lineage_evidence"]:
            if evidence["predicate"] == "record_created_at":
                evidence["object"] = common_created
                _seal(evidence, "evidence_digest")
            elif evidence["predicate"] == "record_updated_at":
                evidence["object"] = common_updated
                _seal(evidence, "evidence_digest")
        _reseal_artifact(artifact)
    graph = _version_graph(artifacts)
    for version in graph["versions"]:
        version["publication_date"] = "2026-07-21"
        version["repository_created_at"] = common_created
        version["repository_updated_at"] = common_updated
    _seal(graph, "content_digest")
    validate_source_version_graph(graph, artifacts=artifacts)


def test_same_day_order_reversal_is_rejected_even_when_graph_is_rehashed() -> None:
    artifacts = _artifacts()
    graph = _version_graph(artifacts)
    graph["versions"][0]["repository_created_at"] = "2026-07-21T09:00:00Z"
    graph["versions"][0]["repository_updated_at"] = "2026-07-21T10:00:00Z"
    _seal(graph, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts)
    assert caught.value.reason_code == "version_order_evidence_mismatch"


def test_repository_evidenced_chronology_reversal_is_rejected() -> None:
    artifacts = _artifacts()
    artifact = artifacts[0]
    observation = artifact["result_items"][0]["source_observation"]
    for evidence in observation["lineage_evidence"]:
        if evidence["predicate"] == "record_created_at":
            evidence["object"] = "2026-06-01T09:00:00Z"
            _seal(evidence, "evidence_digest")
        elif evidence["predicate"] == "record_updated_at":
            evidence["object"] = "2026-06-01T10:00:00Z"
            _seal(evidence, "evidence_digest")
    _reseal_artifact(artifact)
    graph = _version_graph(artifacts)
    graph["versions"][0]["repository_created_at"] = "2026-06-01T09:00:00Z"
    graph["versions"][0]["repository_updated_at"] = "2026-06-01T10:00:00Z"
    _seal(graph, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts)
    assert caught.value.reason_code == "version_chronology_invalid"


def test_wrong_authority_class_cannot_support_correction_relation() -> None:
    artifacts = _artifacts()
    artifact = artifacts[1]
    observation = artifact["result_items"][0]["source_observation"]
    evidence = next(
        row
        for row in observation["lineage_evidence"]
        if row["predicate"] == "successor_corrects_predecessor"
    )
    evidence["authority_class"] = "primary_repository_relation"
    _seal(evidence, "evidence_digest")
    _reseal_artifact(artifact)
    graph = _version_graph(artifacts)
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts)
    assert caught.value.reason_code == "version_relation_evidence_mismatch"


def test_fork_edge_is_rejected_after_nested_rehash() -> None:
    artifacts = _artifacts()
    graph = _version_graph(artifacts)
    fork = copy.deepcopy(graph["edges"][1])
    fork["edge_id"] = "zenodo-lineage-fork"
    fork["from_source_id"] = graph["versions"][0]["source_id"]
    _seal(fork, "edge_digest")
    graph["edges"].append(fork)
    _seal(graph, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts)
    assert caught.value.reason_code == "version_relation_evidence_mismatch"


def test_same_title_cannot_join_an_unrelated_work_identity() -> None:
    artifacts = _artifacts()
    artifact = artifacts[1]
    observation = artifact["result_items"][0]["source_observation"]
    observation["work_identity"] = "doi:10.5281/zenodo.99999997"
    observation["title"] = artifacts[0]["result_items"][0]["title"]
    artifact["result_items"][0]["title"] = observation["title"]
    _reseal_artifact(artifact)
    graph = _version_graph(artifacts)
    sources = reconstruct_normalized_sources(artifacts)
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_version_graph(graph, artifacts=artifacts, sources=sources)
    assert caught.value.reason_code == "version_source_metadata_mismatch"


def test_bundle_cannot_split_one_work_across_two_graphs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    capture, acquisition, artifacts_by_path, graph = _bundle(monkeypatch)
    duplicate = copy.deepcopy(graph)
    duplicate["graph_id"] = "zenodo-18837539-lineage-duplicate"
    _seal(duplicate, "content_digest")
    capture["version_lineages"] = [graph, duplicate]
    _seal(capture, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_capture_acquisition_bundle(
            capture=capture,
            acquisition=acquisition,
            artifacts_by_path=artifacts_by_path,
            version_graphs=[graph, duplicate],
        )
    assert caught.value.reason_code == "version_graph_duplicate_work_identity"


def _safe_routing_mappings(source_ids: list[str]) -> list[dict]:
    return [
        {
            "source_id": source_id,
            "relation": "leaves_open",
            "event_type": "justified_no_change",
            "semantic_relation": "unresolved",
        }
        for source_id in source_ids
    ]


def test_bundle_routing_authority_covers_every_acquired_source_exactly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    capture, acquisition, artifacts_by_path, graph = _bundle(monkeypatch)
    authority = validate_capture_acquisition_bundle(
        capture=capture,
        acquisition=acquisition,
        artifacts_by_path=artifacts_by_path,
        version_graphs=[graph],
    )
    source_ids = sorted(row["source_id"] for row in acquisition["sources"])
    assert sorted(authority["source_routing_eligibility"]) == source_ids
    certificate = validate_source_routing_consumption(
        authority=authority,
        sources=acquisition["sources"],
        stage="mapping_derivation",
        theory_mappings=_safe_routing_mappings(source_ids),
        require_complete_mapping=True,
    )
    assert certificate["source_ids"] == source_ids
    assert certificate["mapping_source_ids"] == source_ids
    assert certificate["authority_boundary"].startswith("version-state routing only")


def test_routing_gate_rejects_source_set_drift() -> None:
    authority = {
        "source_routing_eligibility": {
            "source-a": "unverified_audit_only",
            "source-b": "blocked_positive_support",
        }
    }
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_routing_consumption(
            authority=authority,
            sources=["source-a"],
            stage="assimilation",
        )
    assert caught.value.reason_code == "source_routing_source_set_mismatch"


@pytest.mark.parametrize(
    "eligibility",
    ["unverified_audit_only", "blocked_positive_support"],
)
def test_routing_gate_rejects_positive_support_from_unverified_or_blocked_source(
    eligibility: str,
) -> None:
    mapping = _safe_routing_mappings(["source-a"])[0]
    mapping["semantic_relation"] = "entails"
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_routing_consumption(
            authority={"source_routing_eligibility": {"source-a": eligibility}},
            sources=["source-a"],
            stage="investment",
            theory_mappings=[mapping],
            require_complete_mapping=True,
        )
    assert caught.value.reason_code == "source_routing_positive_support_forbidden"


def test_routing_gate_rejects_negative_only_reframing_or_open_warrant() -> None:
    authority = {
        "source_routing_eligibility": {"withdrawn-source": "negative_evidence_only"}
    }
    with pytest.raises(LiteratureAcquisitionError) as mapping_error:
        validate_source_routing_consumption(
            authority=authority,
            sources=["withdrawn-source"],
            stage="scheduling",
            theory_mappings=[
                {
                    "source_id": "withdrawn-source",
                    "relation": "reframes",
                    "event_type": "reframe",
                    "semantic_relation": "unresolved",
                }
            ],
            require_complete_mapping=True,
        )
    assert mapping_error.value.reason_code == "source_routing_negative_only_violation"
    with pytest.raises(LiteratureAcquisitionError) as warrant_error:
        validate_source_routing_consumption(
            authority=authority,
            sources=["withdrawn-source"],
            stage="semantic_warrants",
            semantic_warrants=[
                {"source_id": "withdrawn-source", "relation": "leaves_open"}
            ],
        )
    assert warrant_error.value.reason_code == "source_routing_negative_only_violation"


def test_routing_gate_rejects_unsafe_relation_event_pair() -> None:
    mapping = _safe_routing_mappings(["source-a"])[0]
    mapping["event_type"] = "demote"
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_routing_consumption(
            authority={
                "source_routing_eligibility": {
                    "source-a": "unverified_audit_only"
                }
            },
            sources=["source-a"],
            stage="acceptance",
            theory_mappings=[mapping],
            require_complete_mapping=True,
        )
    assert caught.value.reason_code == "source_routing_relation_event_unsafe"


def test_multi_execution_artifact_binds_web_and_primary_api_separately() -> None:
    artifact = _artifact_v2_from_v1(_artifacts()[0], bind_api=True)
    validate_tool_response_artifact(artifact)
    assert [row["tool_name"] for row in artifact["executions"]] == [
        "web.run",
        "zenodo.records-api",
    ]
    assert artifact["claim_boundary"]["provider_authentication_authority"] is False


def test_multi_execution_artifact_represents_an_honest_empty_lane() -> None:
    artifact = _artifact_v2_from_v1(_artifacts()[4])
    artifact["result_items"] = []
    artifact["normalization_links"] = []
    artifact["execution_bindings"][0]["item_ids"] = []
    artifact["execution_bindings"][0]["lineage_evidence_ids"] = []
    _seal(artifact["execution_bindings"][0], "binding_digest")
    artifact["response_exposure"]["selected_result_count"] = 0
    artifact["response_exposure"]["lane_outcome"] = "completed_no_results"
    _seal(artifact, "content_digest")
    validate_tool_response_artifact(artifact)


def test_multi_execution_artifact_rejects_unbound_lineage_evidence() -> None:
    artifact = _artifact_v2_from_v1(_artifacts()[0], bind_api=True)
    artifact["execution_bindings"][1]["lineage_evidence_ids"].pop()
    _seal(artifact["execution_bindings"][1], "binding_digest")
    _seal(artifact, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_tool_response_artifact(artifact)
    assert caught.value.reason_code == "tool_execution_evidence_closure_mismatch"


def test_multi_execution_artifact_rejects_api_endpoint_laundering() -> None:
    artifact = _artifact_v2_from_v1(_artifacts()[0], bind_api=True)
    execution = artifact["executions"][1]
    execution["request"]["locator"] = "https://zenodo.org/api/records/99999999"
    _seal(execution["request"], "request_digest")
    _seal(execution, "execution_digest")
    _seal(artifact, "content_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_tool_response_artifact(artifact)
    assert caught.value.reason_code == "tool_execution_evidence_locator_mismatch"
