#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Build the sealed 2026-07-22 Yang--Mills literature acquisition.

This is a deterministic freezer, not a network client.  Its embedded bounded
metadata records six differentiated ``web.run`` searches observed between
12:38:08Z and 12:38:50Z and four unauthenticated Zenodo Records API responses
observed by 12:39:00Z.  The full provider index, ranking trace, raw web payload,
source truth, peer validation, novelty, and exhaustive coverage were not
available and are never asserted here.

The three Zenodo records sharing concept DOI 10.5281/zenodo.18837539 are kept as
separate source versions.  Primary API metadata and author-supplied revision
notes bind the exact v1 -> v2 -> v3 lineage.  Superseded versions are therefore
available only as correction context, while v3 remains an unverified claim-audit
input.  Re-running this program only reproduces the frozen bytes; it does not
renew their acquisition time or freshness authority.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import os
import sys
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import agentic.discovery.literature as literature_runtime  # noqa: E402
from agentic.discovery.contracts import (  # noqa: E402
    canonical_digest,
    canonical_json,
)
from agentic.discovery.ledger import initial_state  # noqa: E402
from agentic.discovery.literature import (  # noqa: E402
    LANE_TYPES,
    run_frontier_literature_cycle,
)
from agentic.discovery.literature_acquisition import (  # noqa: E402
    top_level_content_digest,
    validate_capture_acquisition_bundle,
    validate_tool_response_artifact,
)


TARGET_ID = "yang-mills-existence-and-mass-gap-target"
RUN_ID = "ym21-canonical-parent-20260721"
CAPTURE_STARTED_AT = "2026-07-22T12:38:08Z"
WEB_OBSERVATION_COMPLETED_AT = "2026-07-22T12:38:50Z"
CAPTURE_COMPLETED_AT = "2026-07-22T12:39:00Z"
DEFAULT_OUTPUT_ROOT = (
    ROOT / "agentic" / "evals" / "ym_representational_dynamics_20260721"
)
CAPTURE_NAME = "frontier_search_live_capture_20260722.json"
ACQUISITION_NAME = "frontier_search_live_acquisition_20260722.json"
RESPONSE_DIRECTORY = "frontier_search_live_capture_20260722_tool_responses"

QUERIES = {
    "closest_known_work": (
        "four dimensional Yang Mills mass gap closest constructive rigorous result "
        "continuum lattice 2026"
    ),
    "recent_frontier_preprints": (
        "Yang Mills mass gap latest preprint reflection positivity continuum "
        "construction 2026"
    ),
    "negative_results_barriers": (
        "Yang Mills mass gap retraction correction barrier continuum limit 2025 2026"
    ),
    "conceptual_genealogy": (
        "Yang Mills constructive quantum field theory conceptual genealogy "
        "Osterwalder Schrader 2025 lecture"
    ),
    "adjacent_field_mechanisms": (
        "Yang Mills generalized symmetry category topological field theory "
        "adjacent mechanism 2026"
    ),
    "dissenting_positions": (
        "Yang Mills mass gap dissent framework dependent dissolution continuum 2026"
    ),
}

LANE_IDS = {
    lane_type: f"ym22-current-{lane_type.replace('_', '-')}"
    for lane_type in LANE_TYPES
}

ZENODO_RECORD_ENDPOINTS = {
    "zenodo-18837540": "https://zenodo.org/api/records/18837540",
    "zenodo-19614728": "https://zenodo.org/api/records/19614728",
    "zenodo-21479499": "https://zenodo.org/api/records/21479499",
}
ZENODO_VERSIONS_ENDPOINT = (
    "https://zenodo.org/api/records/21479499/versions?page=1&size=25&sort=version"
)
ZENODO_CONCEPT_DOI = "10.5281/zenodo.18837539"


def _seal(payload: dict[str, Any], field: str) -> dict[str, Any]:
    payload[field] = top_level_content_digest(payload, field)
    return payload


def _bounded_excerpt(text: str) -> tuple[str, int]:
    count = len(text.split())
    if not 1 <= count <= 24:
        raise ValueError(f"bounded excerpt has {count} words, expected 1..24")
    return text, count


def _observation(
    *,
    source_id: str,
    work_identity: str,
    title: str,
    authors: Sequence[str],
    publication_date: str,
    source_version: str,
    source_type: str,
    url: str,
    correction_status: str,
    decision_relevant: bool,
    claims: Sequence[str],
    limitations: Sequence[str],
    doi: str | None = None,
    arxiv_id: str | None = None,
    lineage_evidence: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "source_id": source_id,
        "work_identity": work_identity,
        "title": title,
        "authors": list(authors),
        "publication_date": publication_date,
        "source_version": source_version,
        "source_type": source_type,
        "url": url,
        "doi": doi,
        "arxiv_id": arxiv_id,
        "correction_status": correction_status,
        "decision_relevant": decision_relevant,
        "claims": list(claims),
        "limitations": list(limitations),
    }
    if lineage_evidence:
        payload["lineage_evidence"] = [copy.deepcopy(dict(row)) for row in lineage_evidence]
    return _seal(payload, "observation_digest")


def _evidence(
    *,
    evidence_id: str,
    authority_class: str,
    predicate: str,
    subject: str,
    object_value: str | list[str],
    source_locator: str,
    source_field: str,
    claim: str | None = None,
) -> dict[str, Any]:
    return _seal(
        {
            "evidence_id": evidence_id,
            "authority_class": authority_class,
            "predicate": predicate,
            "subject": subject,
            "object": object_value,
            "claim_digest": None if claim is None else canonical_digest(claim),
            "source_locator": source_locator,
            "source_field": source_field,
        },
        "evidence_digest",
    )


def _request(
    *,
    request_id: str,
    operation: str,
    locator: str,
    response_length: str | None,
) -> dict[str, Any]:
    return _seal(
        {
            "request_id": request_id,
            "operation": operation,
            "locator": locator,
            "domains": [],
            "response_length": response_length,
        },
        "request_digest",
    )


def _execution(
    *,
    execution_id: str,
    tool_name: str,
    request: Mapping[str, Any],
    started_at: str,
    completed_at: str,
) -> dict[str, Any]:
    is_web = tool_name == "web.run"
    return _seal(
        {
            "execution_id": execution_id,
            "tool_name": tool_name,
            "request": copy.deepcopy(dict(request)),
            "observed_started_at": started_at,
            "observed_completed_at": completed_at,
            "execution_mode": (
                "agent_observed_tool_call"
                if is_web
                else "agent_observed_https_request"
            ),
            "external_provider_request_id": None,
            "external_authentication_status": "unavailable",
            "complete_response_available_to_agent": not is_web,
            "raw_response_retained": False,
            "response_projection_mode": (
                "bounded_tool_visible_metadata"
                if is_web
                else "bounded_primary_api_metadata"
            ),
            "observation_authority": "agent_recorded_unauthenticated_execution",
            "exposure_boundary": (
                "The interval is a conservative agent-recorded session window. "
                "Only bounded metadata is frozen; no provider receipt, raw web "
                "payload, ranking trace, or external authentication is available."
                if is_web
                else "The unauthenticated JSON response was observable to the agent, "
                "but only this bounded projection is retained; it supplies metadata "
                "and author-note provenance, not source-claim truth."
            ),
        },
        "execution_digest",
    )


def _execution_binding(
    execution_id: str,
    item_ids: Sequence[str],
    evidence_ids: Sequence[str],
) -> dict[str, Any]:
    return _seal(
        {
            "execution_id": execution_id,
            "item_ids": list(item_ids),
            "lineage_evidence_ids": list(evidence_ids),
        },
        "binding_digest",
    )


def _item(
    *,
    item_id: str,
    provider_rank: int | None,
    observation: Mapping[str, Any],
    excerpt: str,
    retrieval_class: str,
) -> dict[str, Any]:
    bounded, word_count = _bounded_excerpt(excerpt)
    return _seal(
        {
            "item_id": item_id,
            "provider_rank": provider_rank,
            "title": observation["title"],
            "url": observation["url"],
            "displayed_publication": observation["publication_date"],
            "bounded_excerpt": bounded,
            "excerpt_word_count": word_count,
            "retrieval_class": retrieval_class,
            "source_observation": copy.deepcopy(dict(observation)),
        },
        "item_digest",
    )


def _standard_artifact(
    *,
    lane_type: str,
    entries: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    lane_id = LANE_IDS[lane_type]
    request = _request(
        request_id=f"ym22-request-{lane_type}-web",
        operation="search_query",
        locator=QUERIES[lane_type],
        response_length="long",
    )
    execution = _execution(
        execution_id=f"ym22-execution-{lane_type}-web",
        tool_name="web.run",
        request=request,
        started_at=CAPTURE_STARTED_AT,
        completed_at=WEB_OBSERVATION_COMPLETED_AT,
    )
    items: list[dict[str, Any]] = []
    links: list[dict[str, Any]] = []
    for entry in entries:
        item = _item(
            item_id=str(entry["item_id"]),
            provider_rank=int(entry["provider_rank"]),
            observation=entry["observation"],
            excerpt=str(entry["excerpt"]),
            retrieval_class=str(entry["retrieval_class"]),
        )
        items.append(item)
        links.append(
            {
                "item_id": item["item_id"],
                "capture_result_id": entry["result_id"],
                "source_id": item["source_observation"]["source_id"],
                "disposition": entry["disposition"],
                "reason": entry["reason"],
            }
        )
    return _seal(
        {
            "schema_version": "2.0",
            "artifact_kind": "codex_multi_execution_literature_observation",
            "target_id": TARGET_ID,
            "lane_id": lane_id,
            "lane_type": lane_type,
            "executions": [execution],
            "execution_bindings": [
                _execution_binding(
                    execution["execution_id"],
                    [item["item_id"] for item in items],
                    [],
                )
            ],
            "response_exposure": {
                "capture_mode": "bounded_multi_execution_metadata_projection",
                "complete_backend_payload_available": False,
                "complete_ranking_trace_available": False,
                "selected_result_count": len(items),
                "lane_outcome": "completed_with_results",
                "selection_rule": (
                    "Retain only decision-relevant bounded metadata and explicit "
                    "negative-surveillance controls from this differentiated lane."
                ),
            },
            "result_items": items,
            "normalization_links": links,
            "claim_boundary": {
                "source_truth_authority": False,
                "peer_review_authority": False,
                "exhaustiveness_authority": False,
                "novelty_authority": False,
                "provider_authentication_authority": False,
                "allowed_use": (
                    "bounded discovery routing and explicit claim-audit creation only"
                ),
            },
        },
        "content_digest",
    )


def _zenodo_observations() -> list[dict[str, Any]]:
    records = ("18837540", "19614728", "21479499")
    record_dois = [f"10.5281/zenodo.{record}" for record in records]
    versions = ("1.0", "2.0", "3.0")
    publications = ("2026-03-02", "2026-04-16", "2026-07-21")
    created = (
        "2026-03-02T15:30:03.262746+00:00",
        "2026-04-16T18:05:49.397997+00:00",
        "2026-07-21T19:35:44.319690+00:00",
    )
    updated = (
        "2026-04-16T23:42:04.431381+00:00",
        "2026-04-18T20:31:53.369973+00:00",
        "2026-07-21T20:49:55.649420+00:00",
    )
    titles = (
        "The Mass Gap of Four-Dimensional Yang–Mills Theory via Volume-Uniform Functional Inequalities",
        "Mass Gap and Nontriviality for Four-Dimensional Yang–Mills via Lattice Coercivity and a Symmetry-Forced Haar Measure",
        "Mass Gap and Nontriviality for Four-Dimensional SU(2) Yang–Mills Theory via Karcher Blocking and Exact Haar-Pivot Matching",
    )
    direct_claims = (
        "The version 1 record's author claims a four-dimensional Yang-Mills construction through volume-uniform functional inequalities.",
        "The version 2 record's author claims mass gap and nontriviality through lattice coercivity and a symmetry-forced Haar measure.",
        "The version 3 record's author claims mass gap and nontriviality for SU(2) through Karcher blocking and exact Haar-pivot matching.",
    )
    v1_gap_claim = (
        "The version 1 record note says its nontriviality argument has a gap at the weak-to-strong variance-transport step."
    )
    v12_corrects = (
        "The version 1 record note says version 2 supersedes version 1 and replaces its incomplete nontriviality argument."
    )
    v12_scope = (
        "The version 1 record note says version 2 broadens the stated scope to mass gap, nontriviality, and non-Gaussianity."
    )
    v12_architecture = (
        "The version 1 record note says version 2 replaces susceptibility transport with a symmetry-forced Haar-measure mechanism."
    )
    v23_corrects = (
        "The version 3 record note describes corrections to the ultraviolet, normal-section, large-field, macrobridge, transfer-gap, reflection-positivity, continuum-covariance, and nontriviality arguments."
    )
    v23_scope = (
        "The version 3 record note restricts prior arbitrary-group claims to SU(2) and does not claim uniqueness of the subsequential continuum limit."
    )
    v23_architecture = (
        "The version 3 record note replaces the earlier lattice-coercivity and symmetry-forced Haar-measure architecture with Karcher blocking and exact Haar-pivot matching."
    )

    observations: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        source_id = f"zenodo-{record}"
        record_doi = record_dois[index]
        endpoint = ZENODO_RECORD_ENDPOINTS[source_id]
        evidence = [
            _evidence(
                evidence_id=f"ym22-record-doi-{record}",
                authority_class="primary_repository_metadata",
                predicate="record_doi",
                subject=source_id,
                object_value=record_doi,
                source_locator=endpoint,
                source_field="/doi",
            ),
            _evidence(
                evidence_id=f"ym22-record-concept-{record}",
                authority_class="primary_repository_metadata",
                predicate="record_member_of_concept",
                subject=record_doi,
                object_value=ZENODO_CONCEPT_DOI,
                source_locator=endpoint,
                source_field="/conceptdoi",
            ),
            _evidence(
                evidence_id=f"ym22-record-version-{record}",
                authority_class="primary_repository_metadata",
                predicate="record_version",
                subject=record_doi,
                object_value=versions[index],
                source_locator=endpoint,
                source_field="/metadata/version",
            ),
            _evidence(
                evidence_id=f"ym22-record-created-{record}",
                authority_class="primary_repository_metadata",
                predicate="record_created_at",
                subject=record_doi,
                object_value=created[index],
                source_locator=endpoint,
                source_field="/created",
            ),
            _evidence(
                evidence_id=f"ym22-record-updated-{record}",
                authority_class="primary_repository_metadata",
                predicate="record_updated_at",
                subject=record_doi,
                object_value=updated[index],
                source_locator=endpoint,
                source_field="/updated",
            ),
            _evidence(
                evidence_id=f"ym22-record-status-{record}",
                authority_class="primary_repository_metadata",
                predicate="record_status",
                subject=record_doi,
                object_value="current" if index == 2 else "superseded",
                source_locator=ZENODO_VERSIONS_ENDPOINT,
                source_field=(
                    "/hits/hits locally ordered by parsed metadata.version; "
                    "terminal-versus-nonterminal classification"
                ),
            ),
        ]
        claims = [direct_claims[index]]
        if index == 0:
            claims.append(v1_gap_claim)
        if index == 1:
            claims.extend([v12_corrects, v12_scope, v12_architecture])
            evidence.extend(
                [
                    _evidence(
                        evidence_id="ym22-revision-18837540-19614728",
                        authority_class="primary_repository_relation",
                        predicate="successor_revision_of",
                        subject=record_doi,
                        object_value=record_dois[0],
                        source_locator=ZENODO_VERSIONS_ENDPOINT,
                        source_field="/hits/hits locally ordered by parsed metadata.version",
                    ),
                    _evidence(
                        evidence_id="ym22-supersedes-18837540-19614728",
                        authority_class="primary_repository_relation",
                        predicate="successor_supersedes_predecessor",
                        subject=record_doi,
                        object_value=record_dois[0],
                        source_locator=ZENODO_VERSIONS_ENDPOINT,
                        source_field="/hits/hits locally ordered by parsed metadata.version",
                    ),
                    _evidence(
                        evidence_id="ym22-corrects-18837540-19614728",
                        authority_class="primary_record_note",
                        predicate="successor_corrects_predecessor",
                        subject=record_doi,
                        object_value=record_dois[0],
                        source_locator=ZENODO_RECORD_ENDPOINTS["zenodo-18837540"],
                        source_field="/metadata/notes",
                        claim=v12_corrects,
                    ),
                    _evidence(
                        evidence_id="ym22-scope-18837540-19614728",
                        authority_class="primary_record_note",
                        predicate="successor_broadens_scope",
                        subject=record_doi,
                        object_value=record_dois[0],
                        source_locator=ZENODO_RECORD_ENDPOINTS["zenodo-18837540"],
                        source_field="/metadata/notes",
                        claim=v12_scope,
                    ),
                    _evidence(
                        evidence_id="ym22-architecture-18837540-19614728",
                        authority_class="primary_record_note",
                        predicate="successor_changes_architecture",
                        subject=record_doi,
                        object_value=record_dois[0],
                        source_locator=ZENODO_RECORD_ENDPOINTS["zenodo-18837540"],
                        source_field="/metadata/notes",
                        claim=v12_architecture,
                    ),
                ]
            )
        if index == 2:
            claims.extend([v23_corrects, v23_scope, v23_architecture])
            evidence.extend(
                [
                    _evidence(
                        evidence_id="ym22-lineage-membership-18837539",
                        authority_class="primary_repository_relation",
                        predicate="lineage_ordered_record_dois",
                        subject=ZENODO_CONCEPT_DOI,
                        object_value=record_dois,
                        source_locator=ZENODO_VERSIONS_ENDPOINT,
                        source_field=(
                            "/hits/hits projected by parsed metadata.version ascending"
                        ),
                    ),
                    _evidence(
                        evidence_id="ym22-revision-19614728-21479499",
                        authority_class="primary_repository_relation",
                        predicate="successor_revision_of",
                        subject=record_doi,
                        object_value=record_dois[1],
                        source_locator=ZENODO_VERSIONS_ENDPOINT,
                        source_field="/hits/hits locally ordered by parsed metadata.version",
                    ),
                    _evidence(
                        evidence_id="ym22-supersedes-19614728-21479499",
                        authority_class="primary_repository_relation",
                        predicate="successor_supersedes_predecessor",
                        subject=record_doi,
                        object_value=record_dois[1],
                        source_locator=ZENODO_VERSIONS_ENDPOINT,
                        source_field="/hits/hits locally ordered by parsed metadata.version",
                    ),
                    _evidence(
                        evidence_id="ym22-corrects-19614728-21479499",
                        authority_class="primary_record_note",
                        predicate="successor_corrects_predecessor",
                        subject=record_doi,
                        object_value=record_dois[1],
                        source_locator=endpoint,
                        source_field="/metadata/notes",
                        claim=v23_corrects,
                    ),
                    _evidence(
                        evidence_id="ym22-scope-19614728-21479499",
                        authority_class="primary_record_note",
                        predicate="successor_narrows_scope",
                        subject=record_doi,
                        object_value=record_dois[1],
                        source_locator=endpoint,
                        source_field="/metadata/notes",
                        claim=v23_scope,
                    ),
                    _evidence(
                        evidence_id="ym22-architecture-19614728-21479499",
                        authority_class="primary_record_note",
                        predicate="successor_changes_architecture",
                        subject=record_doi,
                        object_value=record_dois[1],
                        source_locator=endpoint,
                        source_field="/metadata/notes",
                        claim=v23_architecture,
                    ),
                ]
            )
        observations.append(
            _observation(
                source_id=source_id,
                work_identity=f"doi:{ZENODO_CONCEPT_DOI}",
                title=titles[index],
                authors=["Kirk, Harold D."],
                publication_date=publications[index],
                source_version=versions[index],
                source_type="preprint",
                url=f"https://zenodo.org/records/{record}",
                doi=record_doi,
                arxiv_id=None,
                correction_status="none_known" if index == 2 else "superseded",
                decision_relevant=True,
                claims=claims,
                limitations=[
                    "Repository metadata and author revision notes do not independently validate the mathematical claims.",
                    "The capture establishes version-aware audit routing, not theorem truth, novelty, peer review, or Clay acceptance.",
                ],
                lineage_evidence=evidence,
            )
        )
    return observations


def _recent_frontier_artifact() -> dict[str, Any]:
    lane_type = "recent_frontier_preprints"
    lane_id = LANE_IDS[lane_type]
    observations = _zenodo_observations()
    items = [
        _item(
            item_id=f"ym22-item-zenodo-{record}",
            provider_rank=None,
            observation=observation,
            excerpt=(
                "Primary repository metadata and revision notes retained for exact "
                f"version {observation['source_version']} lineage routing"
            ),
            retrieval_class="primary_api_metadata",
        )
        for record, observation in zip(
            ("18837540", "19614728", "21479499"), observations, strict=True
        )
    ]
    links = [
        {
            "item_id": items[index]["item_id"],
            "capture_result_id": f"YM22-RAW-{index + 2:03d}",
            "source_id": observations[index]["source_id"],
            "disposition": (
                "included_unverified_challenger"
                if index == 2
                else "included_correction_or_supersession"
            ),
            "reason": (
                "The terminal record is retained only as a current unverified "
                "claim-audit input."
                if index == 2
                else "The superseded record is retained only to preserve exact "
                "correction and architecture-change context."
            ),
        }
        for index in range(3)
    ]
    web_request = _request(
        request_id="ym22-request-recent-frontier-preprints-web",
        operation="search_query",
        locator=QUERIES[lane_type],
        response_length="long",
    )
    web_execution = _execution(
        execution_id="ym22-execution-recent-frontier-preprints-web",
        tool_name="web.run",
        request=web_request,
        started_at=CAPTURE_STARTED_AT,
        completed_at=WEB_OBSERVATION_COMPLETED_AT,
    )
    executions = [web_execution]
    bindings = [
        _execution_binding(web_execution["execution_id"], [items[0]["item_id"]], [])
    ]
    item_by_source = {
        item["source_observation"]["source_id"]: item for item in items
    }
    endpoint_labels = {
        ZENODO_RECORD_ENDPOINTS["zenodo-18837540"]: "record-18837540",
        ZENODO_RECORD_ENDPOINTS["zenodo-19614728"]: "record-19614728",
        ZENODO_RECORD_ENDPOINTS["zenodo-21479499"]: "record-21479499",
        ZENODO_VERSIONS_ENDPOINT: "versions-18837539",
    }
    for locator, label in endpoint_labels.items():
        request = _request(
            request_id=f"ym22-request-{label}-api",
            operation="https_get",
            locator=locator,
            response_length=None,
        )
        execution = _execution(
            execution_id=f"ym22-execution-{label}-api",
            tool_name="zenodo.records-api",
            request=request,
            started_at=WEB_OBSERVATION_COMPLETED_AT,
            completed_at=CAPTURE_COMPLETED_AT,
        )
        bound_item_ids: list[str] = []
        evidence_ids: list[str] = []
        for source_id, item in item_by_source.items():
            matching = [
                atom["evidence_id"]
                for atom in item["source_observation"].get("lineage_evidence", [])
                if atom["source_locator"] == locator
            ]
            if matching:
                bound_item_ids.append(item["item_id"])
                evidence_ids.extend(matching)
        executions.append(execution)
        bindings.append(
            _execution_binding(
                execution["execution_id"], bound_item_ids, evidence_ids
            )
        )
    artifact = _seal(
        {
            "schema_version": "2.0",
            "artifact_kind": "codex_multi_execution_literature_observation",
            "target_id": TARGET_ID,
            "lane_id": lane_id,
            "lane_type": lane_type,
            "executions": executions,
            "execution_bindings": bindings,
            "response_exposure": {
                "capture_mode": "bounded_multi_execution_metadata_projection",
                "complete_backend_payload_available": False,
                "complete_ranking_trace_available": False,
                "selected_result_count": len(items),
                "lane_outcome": "completed_with_results",
                "selection_rule": (
                    "The web search exposed v1; the exact primary repository concept "
                    "lineage then supplied v2 and v3. Preserve all three versions so "
                    "superseded mechanisms cannot be silently treated as current."
                ),
            },
            "result_items": items,
            "normalization_links": links,
            "claim_boundary": {
                "source_truth_authority": False,
                "peer_review_authority": False,
                "exhaustiveness_authority": False,
                "novelty_authority": False,
                "provider_authentication_authority": False,
                "allowed_use": (
                    "bounded discovery routing and explicit claim-audit creation only"
                ),
            },
        },
        "content_digest",
    )
    validate_tool_response_artifact(artifact)
    return artifact


def _source_entries() -> dict[str, list[dict[str, Any]]]:
    arxiv = _observation(
        source_id="arxiv-2606.19362-v1",
        work_identity="arxiv:2606.19362",
        title=(
            "Reflection-Positive Construction of a Four-Dimensional SU(N) "
            "Yang-Mills Theory with Mass Gap and Confinement"
        ),
        authors=["Mir Faizal", "Arshid Shabir"],
        publication_date="2026-06-09",
        source_version="v1",
        source_type="preprint",
        url="https://arxiv.org/abs/2606.19362",
        doi="10.48550/arXiv.2606.19362",
        arxiv_id="2606.19362",
        correction_status="none_known",
        decision_relevant=True,
        claims=[
            "The search metadata reports that the authors claim a reflection-positive four-dimensional SU(N) Yang-Mills construction with mass gap and confinement.",
            "The search metadata reports author claims of a uniform transfer-operator gap, continuum clustering, Osterwalder-Schrader reconstruction, and regulator-independent universality.",
        ],
        limitations=[
            "The bounded search metadata and arXiv record do not independently verify any theorem, dependency, or universality claim.",
            "This source remains a direct challenger requiring claim-specific proof audit before theory investment."
        ],
    )
    retraction = _observation(
        source_id="cambridge-coe-2025-sgpbm-retracted-v1",
        work_identity="doi:10.33774/coe-2025-sgpbm",
        title="RETRACTED: A Rigorous Proof of the Mass Gap in SU(N) Yang-Mills Theory",
        authors=["Yuta Agawa"],
        publication_date="2025-03-13",
        source_version="v1-retracted",
        source_type="retraction",
        url=(
            "https://client.prod.orp.cambridge.org/engage/coe/article-details/"
            "67cb65676dde43c908f9dab6"
        ),
        doi="10.33774/coe-2025-sgpbm",
        arxiv_id=None,
        correction_status="retracted",
        decision_relevant=True,
        claims=[
            "The publisher search metadata labels the working paper retracted and says it was not peer reviewed by Cambridge University Press.",
            "The retraction notice says the author regarded the work as a preliminary hypothesis insufficiently validated for formal publication."
        ],
        limitations=[
            "This is negative correction evidence only and cannot support any positive Yang-Mills construction claim.",
            "The capture retains a bounded notice summary rather than the complete publisher payload."
        ],
    )
    review = _observation(
        source_id="nature-reviews-physics-douglas-2026",
        work_identity="doi:10.1038/s42254-025-00909-2",
        title="The Yang-Mills Millennium problem",
        authors=["Michael R. Douglas"],
        publication_date="2026",
        source_version="publisher-page-observed-2026-07-22",
        source_type="survey",
        url="https://www.nature.com/articles/s42254-025-00909-2",
        doi="10.1038/s42254-025-00909-2",
        arxiv_id=None,
        correction_status="none_known",
        decision_relevant=True,
        claims=[
            "The current review metadata frames the problem as both mathematical definition of Yang-Mills theory and proof of the mass-gap property.",
            "The review metadata identifies a well-defined arbitrarily-high-energy continuum limit as part of the definition problem."
        ],
        limitations=[
            "A review boundary does not validate any 2026 direct proof claim.",
            "Only bounded search metadata was retained; the capture is not an exhaustive review of the article or field."
        ],
    )
    mismatch = _observation(
        source_id="arxiv-1203.6538-target-mismatch",
        work_identity="arxiv:1203.6538",
        title="Resummation scheme for 3d Yang-Mills and the two-loop magnetic mass for hot gauge theories",
        authors=["Authors not exposed in the bounded search result"],
        publication_date="2012",
        source_version="search-metadata-observed-2026-07-22",
        source_type="preprint",
        url="https://arxiv.org/abs/1203.6538",
        doi=None,
        arxiv_id="1203.6538",
        correction_status="none_known",
        decision_relevant=False,
        claims=[
            "The search result concerns a three-dimensional resummation scheme and magnetic mass in hot gauge theories."
        ],
        limitations=[
            "The dimensional, thermal, and target mismatch prevents use as evidence for the four-dimensional pure Yang-Mills existence and mass-gap target."
        ],
    )
    genealogy = _observation(
        source_id="harvard-chatterjee-ym-foundations-2025",
        work_identity=(
            "url:https://www.math.harvard.edu/event/millennium-prize-problems-"
            "lecture-sourav-chatterjee-yang-mills-existence-and-mass-gap/"
        ),
        title="Yang-Mills and the foundations of quantum field theory",
        authors=["Sourav Chatterjee", "Harvard Mathematics Department"],
        publication_date="2025-10-15",
        source_version="event-page-observed-2026-07-22",
        source_type="survey",
        url=(
            "https://www.math.harvard.edu/event/millennium-prize-problems-lecture-"
            "sourav-chatterjee-yang-mills-existence-and-mass-gap/"
        ),
        doi=None,
        arxiv_id=None,
        correction_status="none_known",
        decision_relevant=True,
        claims=[
            "The lecture metadata places the Yang-Mills target in the constructive-field-theory programme initiated in the 1960s.",
            "The lecture metadata says that constructive field theory has had many successes but has not reached its original goal."
        ],
        limitations=[
            "A public lecture supplies conceptual genealogy and problem framing, not a proof-status or theorem-validity certificate.",
            "The bounded event metadata does not exhaust the lecture's historical or technical claims."
        ],
    )
    adjacent = _observation(
        source_id="aps-prd-4dxd-kh1r-2026",
        work_identity="doi:10.1103/4dxd-kh1r",
        title=(
            "Sandwich construction of symmetry topological field theories for "
            "the center symmetries of Chern-Simons, Yang-Mills, and Einstein gravity"
        ),
        authors=["Leron Borsten", "Dimitri Kanakaris", "Hyungrok Kim"],
        publication_date="2026-06-22",
        source_version="publisher-page-observed-2026-07-22",
        source_type="primary",
        url="https://journals.aps.org/prd/abstract/10.1103/4dxd-kh1r",
        doi="10.1103/4dxd-kh1r",
        arxiv_id=None,
        correction_status="none_known",
        decision_relevant=True,
        claims=[
            "The publisher search metadata reports a sandwich construction of symmetry topological field theories manifesting Yang-Mills center symmetries.",
            "The reported construction uses an AKSZ sigma-model filling with a Weil-algebra target and discrete topological-boundary-condition data."
        ],
        limitations=[
            "This adjacent symmetry mechanism does not establish a four-dimensional continuum Yang-Mills theory or a physical mass gap.",
            "Categorical or topological structure may generate concepts only after an explicit physics bridge and cannot substitute for the target deliverables."
        ],
    )
    dissent = _observation(
        source_id="zenodo-19699784-dissent-v1",
        work_identity="doi:10.5281/zenodo.19699784",
        title=(
            "The Yang-Mills Mass Gap From Proof Attempts to Dissolution by "
            "Holographic Finiteness"
        ),
        authors=[
            "Watt, Henry",
            "Claude Opus 4.7",
            "Claude Opus 4.6",
            "Gemini 3.1 Pro",
            "Grok 4.20",
        ],
        publication_date="2026-04-22",
        source_version="v1",
        source_type="other",
        url="https://zenodo.org/records/19699784",
        doi="10.5281/zenodo.19699784",
        arxiv_id=None,
        correction_status="none_known",
        decision_relevant=True,
        claims=[
            "The search metadata reports the authors' dissenting claim that the continuum formulation removes the mechanism they associate with a gap.",
            "The record explicitly says it does not claim to solve the Millennium Prize as stated and instead advances a framework-dependent recontextualisation."
        ],
        limitations=[
            "The record's physical and mathematical claims are unverified and cannot redefine the exact Clay target.",
            "Its value here is adversarial conceptual pressure on framework assumptions, not positive theorem support."
        ],
    )
    return {
        "closest_known_work": [
            {
                "item_id": "ym22-item-arxiv-2606.19362",
                "provider_rank": 0,
                "observation": arxiv,
                "excerpt": "Direct reflection-positive continuum construction claim retained for dependency and universality audit",
                "retrieval_class": "search_result_metadata",
                "result_id": "YM22-RAW-001",
                "disposition": "included_unverified_challenger",
                "reason": "The direct target-overlapping claim requires an exact proof-dependency audit; search visibility supplies no validation.",
            }
        ],
        "negative_results_barriers": [
            {
                "item_id": "ym22-item-cambridge-retraction",
                "provider_rank": 6,
                "observation": retraction,
                "excerpt": "Publisher search metadata exposes an author retraction and explicit insufficient-validation notice",
                "retrieval_class": "publisher_metadata",
                "result_id": "YM22-RAW-005",
                "disposition": "included_correction_or_supersession",
                "reason": "Retain as negative evidence preventing retracted proof claims from routing positive investment.",
            },
            {
                "item_id": "ym22-item-nature-review-2026",
                "provider_rank": 3,
                "observation": review,
                "excerpt": "Current review metadata preserves the continuum-definition boundary against direct proof overclaim",
                "retrieval_class": "publisher_metadata",
                "result_id": "YM22-RAW-006",
                "disposition": "included_current_review",
                "reason": "Use as a current problem-boundary comparator, never as validation or exhaustive consensus.",
            },
            {
                "item_id": "ym22-item-target-mismatch-3d",
                "provider_rank": 14,
                "observation": mismatch,
                "excerpt": "Three-dimensional thermal magnetic-mass result retained only as an explicit target-mismatch control",
                "retrieval_class": "search_result_metadata",
                "result_id": "YM22-RAW-007",
                "disposition": "excluded_target_mismatch",
                "reason": "Dimension, thermal setting, and claimed object differ from the exact four-dimensional pure-Yang-Mills target.",
            },
        ],
        "conceptual_genealogy": [
            {
                "item_id": "ym22-item-chatterjee-genealogy",
                "provider_rank": 0,
                "observation": genealogy,
                "excerpt": "Constructive-field-theory genealogy and its still-open foundational objective retained for reflective synthesis",
                "retrieval_class": "search_result_metadata",
                "result_id": "YM22-RAW-008",
                "disposition": "included_conceptual_genealogy",
                "reason": "The source locates the target in a long-running conceptual programme without granting theorem authority.",
            }
        ],
        "adjacent_field_mechanisms": [
            {
                "item_id": "ym22-item-aps-symtft",
                "provider_rank": 1,
                "observation": adjacent,
                "excerpt": "Recent SymTFT sandwich construction retained as adjacent higher-structural concept material",
                "retrieval_class": "publisher_metadata",
                "result_id": "YM22-RAW-009",
                "disposition": "included_adjacent_mechanism",
                "reason": "It offers a categorical symmetry language only after explicit translation to target physics obligations.",
            }
        ],
        "dissenting_positions": [
            {
                "item_id": "ym22-item-dissent-holographic-finiteness",
                "provider_rank": 1,
                "observation": dissent,
                "excerpt": "Framework-dependent dissent retained as adversarial conceptual pressure, not target redefinition",
                "retrieval_class": "search_result_metadata",
                "result_id": "YM22-RAW-010",
                "disposition": "included_unverified_challenger",
                "reason": "The dissent probes continuum assumptions while remaining explicitly outside proof of the stated target.",
            }
        ],
    }


def _build_artifacts() -> list[dict[str, Any]]:
    entries = _source_entries()
    artifacts: list[dict[str, Any]] = []
    for lane_type in LANE_TYPES:
        if lane_type == "recent_frontier_preprints":
            artifact = _recent_frontier_artifact()
        else:
            artifact = _standard_artifact(
                lane_type=lane_type,
                entries=entries[lane_type],
            )
        validate_tool_response_artifact(artifact)
        artifacts.append(artifact)
    return artifacts


def _evidence_binding(
    artifact: Mapping[str, Any], *, source_id: str, evidence_id: str
) -> dict[str, Any]:
    item = next(
        row
        for row in artifact["result_items"]
        if row["source_observation"]["source_id"] == source_id
    )
    observation = item["source_observation"]
    evidence = next(
        row
        for row in observation.get("lineage_evidence", [])
        if row["evidence_id"] == evidence_id
    )
    return {
        "artifact_lane_id": artifact["lane_id"],
        "artifact_content_digest": artifact["content_digest"],
        "item_id": item["item_id"],
        "item_digest": item["item_digest"],
        "source_id": source_id,
        "observation_digest": observation["observation_digest"],
        "evidence_id": evidence_id,
        "evidence_digest": evidence["evidence_digest"],
        "evidence_kind": evidence["authority_class"],
    }


def _relation(
    artifact: Mapping[str, Any],
    *,
    source_id: str,
    relation: str,
    evidence_id: str,
) -> dict[str, Any]:
    binding = _evidence_binding(
        artifact, source_id=source_id, evidence_id=evidence_id
    )
    item = next(
        row
        for row in artifact["result_items"]
        if row["source_observation"]["source_id"] == source_id
    )
    evidence = next(
        row
        for row in item["source_observation"]["lineage_evidence"]
        if row["evidence_id"] == evidence_id
    )
    return _seal(
        {
            "relation": relation,
            "claim_digests": (
                []
                if evidence["claim_digest"] is None
                else [evidence["claim_digest"]]
            ),
            "evidence_bindings": [binding],
        },
        "relation_digest",
    )


def _delta(
    artifact: Mapping[str, Any],
    *,
    source_id: str,
    classification: str,
    evidence_id: str,
) -> dict[str, Any]:
    relation = _relation(
        artifact,
        source_id=source_id,
        relation=(
            "broadens_scope" if classification == "broadened" else "narrows_scope"
        ),
        evidence_id=evidence_id,
    )
    return _seal(
        {
            "classification": classification,
            "claim_digests": relation["claim_digests"],
            "evidence_bindings": relation["evidence_bindings"],
        },
        "delta_digest",
    )


def _architecture_delta(
    artifact: Mapping[str, Any], *, source_id: str, evidence_id: str
) -> dict[str, Any]:
    relation = _relation(
        artifact,
        source_id=source_id,
        relation="changes_architecture",
        evidence_id=evidence_id,
    )
    return _seal(
        {
            "classification": "changed",
            "claim_digests": relation["claim_digests"],
            "evidence_bindings": relation["evidence_bindings"],
        },
        "delta_digest",
    )


def _version_graph(recent_artifact: Mapping[str, Any]) -> dict[str, Any]:
    records = ("18837540", "19614728", "21479499")
    dates = ("2026-03-02", "2026-04-16", "2026-07-21")
    created = (
        "2026-03-02T15:30:03.262746+00:00",
        "2026-04-16T18:05:49.397997+00:00",
        "2026-07-21T19:35:44.319690+00:00",
    )
    updated = (
        "2026-04-16T23:42:04.431381+00:00",
        "2026-04-18T20:31:53.369973+00:00",
        "2026-07-21T20:49:55.649420+00:00",
    )
    versions: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        source_id = f"zenodo-{record}"
        versions.append(
            {
                "ordinal": index + 1,
                "source_id": source_id,
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
                    "unverified_audit_only"
                    if index == 2
                    else "blocked_positive_support"
                ),
                "predecessor_source_id": (
                    None if index == 0 else f"zenodo-{records[index - 1]}"
                ),
                "successor_source_id": (
                    None if index == 2 else f"zenodo-{records[index + 1]}"
                ),
                "identity_evidence_bindings": [
                    _evidence_binding(
                        recent_artifact,
                        source_id=source_id,
                        evidence_id=f"ym22-record-doi-{record}",
                    ),
                    _evidence_binding(
                        recent_artifact,
                        source_id=source_id,
                        evidence_id=f"ym22-record-concept-{record}",
                    ),
                    _evidence_binding(
                        recent_artifact,
                        source_id=source_id,
                        evidence_id=f"ym22-record-version-{record}",
                    ),
                ],
                "ordering_evidence_bindings": [
                    _evidence_binding(
                        recent_artifact,
                        source_id=source_id,
                        evidence_id=f"ym22-record-created-{record}",
                    ),
                    _evidence_binding(
                        recent_artifact,
                        source_id=source_id,
                        evidence_id=f"ym22-record-updated-{record}",
                    ),
                ],
                "status_evidence_bindings": [
                    _evidence_binding(
                        recent_artifact,
                        source_id=source_id,
                        evidence_id=f"ym22-record-status-{record}",
                    )
                ],
                "claim_authority": "unverified_author_claims_only",
            }
        )
    edge_specs = (
        {
            "from": "zenodo-18837540",
            "to": "zenodo-19614728",
            "transition": "18837540-19614728",
            "scope_relation": "broadens_scope",
            "scope_classification": "broadened",
        },
        {
            "from": "zenodo-19614728",
            "to": "zenodo-21479499",
            "transition": "19614728-21479499",
            "scope_relation": "narrows_scope",
            "scope_classification": "narrowed",
        },
    )
    edges: list[dict[str, Any]] = []
    for index, spec in enumerate(edge_specs, start=1):
        transition = str(spec["transition"])
        successor = str(spec["to"])
        edges.append(
            _seal(
                {
                    "edge_id": f"ym22-zenodo-lineage-edge-{index}",
                    "from_source_id": spec["from"],
                    "to_source_id": successor,
                    "relations": [
                        _relation(
                            recent_artifact,
                            source_id=successor,
                            relation="revision",
                            evidence_id=f"ym22-revision-{transition}",
                        ),
                        _relation(
                            recent_artifact,
                            source_id=successor,
                            relation="supersedes",
                            evidence_id=f"ym22-supersedes-{transition}",
                        ),
                        _relation(
                            recent_artifact,
                            source_id=successor,
                            relation="corrects",
                            evidence_id=f"ym22-corrects-{transition}",
                        ),
                        _relation(
                            recent_artifact,
                            source_id=successor,
                            relation=str(spec["scope_relation"]),
                            evidence_id=f"ym22-scope-{transition}",
                        ),
                        _relation(
                            recent_artifact,
                            source_id=successor,
                            relation="changes_architecture",
                            evidence_id=f"ym22-architecture-{transition}",
                        ),
                    ],
                    "scope_delta": _delta(
                        recent_artifact,
                        source_id=successor,
                        classification=str(spec["scope_classification"]),
                        evidence_id=f"ym22-scope-{transition}",
                    ),
                    "architecture_delta": _architecture_delta(
                        recent_artifact,
                        source_id=successor,
                        evidence_id=f"ym22-architecture-{transition}",
                    ),
                },
                "edge_digest",
            )
        )
    return _seal(
        {
            "schema_version": "2.0",
            "graph_id": "ym22-zenodo-18837539-lineage",
            "target_id": TARGET_ID,
            "work_identity": f"doi:{ZENODO_CONCEPT_DOI}",
            "concept_doi": ZENODO_CONCEPT_DOI,
            "observed_at": CAPTURE_COMPLETED_AT,
            "terminal_source_id": "zenodo-21479499",
            "current_source_id": "zenodo-21479499",
            "lineage_membership": _seal(
                {
                    "ordered_record_dois": [
                        f"10.5281/zenodo.{record}" for record in records
                    ],
                    "evidence_bindings": [
                        _evidence_binding(
                            recent_artifact,
                            source_id="zenodo-21479499",
                            evidence_id="ym22-lineage-membership-18837539",
                        )
                    ],
                },
                "membership_digest",
            ),
            "versions": versions,
            "edges": edges,
            "authority_boundary": {
                "version_metadata_authority": (
                    "primary_repository_record_plus_sealed_tool_visible_capture"
                ),
                "claim_truth_authority": False,
                "peer_validation_authority": False,
                "allowed_use": (
                    "supersession-aware discovery routing and claim-specific audit creation"
                ),
            },
        },
        "content_digest",
    )


def _artifact_window(artifact: Mapping[str, Any]) -> tuple[str, str]:
    starts = [str(row["observed_started_at"]) for row in artifact["executions"]]
    completions = [str(row["observed_completed_at"]) for row in artifact["executions"]]
    return min(starts), max(completions)


def _build_acquisition(artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    lane_requests: list[dict[str, Any]] = []
    providers: dict[str, Any] = {}
    clock_values: list[str] = []
    for artifact in artifacts:
        lane_type = str(artifact["lane_type"])
        lane_requests.append(
            {
                "lane_id": artifact["lane_id"],
                "lane_type": lane_type,
                "queries": [QUERIES[lane_type]],
                "inclusion_policy": (
                    "Include only the exact bounded observations linked as included "
                    "by the sealed lane artifact."
                ),
                "exclusion_policy": (
                    "Exclude target mismatch and insufficiently bound metadata; retain "
                    "explicit corrections solely for negative or historical routing."
                ),
            }
        )
        included_sources: list[dict[str, Any]] = []
        item_by_id = {
            str(item["item_id"]): item for item in artifact["result_items"]
        }
        for link in artifact["normalization_links"]:
            if not str(link["disposition"]).startswith("included"):
                continue
            observation = copy.deepcopy(
                item_by_id[str(link["item_id"])]["source_observation"]
            )
            observation.pop("observation_digest", None)
            included_sources.append(observation)

        def provider(
            _request: Mapping[str, Any],
            *,
            lane_type: str = lane_type,
            sources: list[dict[str, Any]] = included_sources,
        ) -> dict[str, Any]:
            return {
                "provider": "codex-multi-execution-literature-observation",
                "index": f"bounded-web-plus-primary-api:{lane_type}:2026-07-22",
                "execution_mode": "live",
                "status": "completed",
                "coverage_cutoff": CAPTURE_COMPLETED_AT,
                "sources": copy.deepcopy(sources),
            }

        providers[lane_type] = provider
        started, completed = _artifact_window(artifact)
        clock_values.extend([started, completed])
    clock_values.append(CAPTURE_COMPLETED_AT)
    iterator = iter(clock_values)
    original_clock = literature_runtime.utc_now
    literature_runtime.utc_now = lambda: next(iterator)
    try:
        acquisition = run_frontier_literature_cycle(
            {
                "target_id": TARGET_ID,
                "claim_scope": (
                    "Current correction-aware Yang-Mills existence and mass-gap "
                    "discovery routing as bounded on 2026-07-22"
                ),
                "theory_state_digest": canonical_digest(
                    initial_state(TARGET_ID, RUN_ID)
                ),
                "coverage_cutoff": CAPTURE_COMPLETED_AT,
                "coverage_limits": [
                    "Six exact differentiated queries are bounded and non-exhaustive.",
                    "Search-provider index state and ranking internals were unavailable.",
                    "No raw web-provider HTTP payload or provider receipt was exposed.",
                    "Unauthenticated Zenodo API metadata does not validate author claims.",
                    "Correction surveillance is limited to the selected visible records.",
                    "The capture does not establish novelty, peer consensus, or Clay acceptance.",
                    "Adjacent categorical mechanisms require an explicit physics-value bridge.",
                    "Dissenting framework claims cannot redefine the exact target."
                ],
                "inclusion_policy": (
                    "Include exact decision-relevant bounded observations, current "
                    "problem-boundary material, correction lineages, conceptual genealogy, "
                    "adjacent mechanisms, and dissent with explicit authority limits."
                ),
                "exclusion_policy": (
                    "Exclude target mismatches from normalized evidence and block "
                    "superseded or retracted records from positive support."
                ),
                "search_lanes": lane_requests,
            },
            providers=providers,
            max_workers=1,
        )
    finally:
        literature_runtime.utc_now = original_clock
    return acquisition


def _primary_search_execution(artifact: Mapping[str, Any]) -> Mapping[str, Any]:
    return next(row for row in artifact["executions"] if row["tool_name"] == "web.run")


def _capture_result_metadata(source_id: str) -> tuple[str, list[str]]:
    return {
        "arxiv-2606.19362-v1": ("unverified_challenger", ["direct_claim"]),
        "zenodo-18837540": (
            "correction_context",
            ["correction", "supersession", "bounded_lattice"],
        ),
        "zenodo-19614728": (
            "correction_context",
            ["correction", "supersession", "bounded_lattice"],
        ),
        "zenodo-21479499": (
            "unverified_challenger",
            ["direct_claim", "bounded_lattice"],
        ),
        "cambridge-coe-2025-sgpbm-retracted-v1": (
            "correction_context",
            ["correction", "withdrawal"],
        ),
        "nature-reviews-physics-douglas-2026": (
            "current_review_boundary",
            ["authoritative_status", "current_review"],
        ),
        "arxiv-1203.6538-target-mismatch": (
            "excluded_target_mismatch",
            ["target_mismatch"],
        ),
        "harvard-chatterjee-ym-foundations-2025": (
            "conceptual_context",
            ["conceptual_genealogy", "current_review"],
        ),
        "aps-prd-4dxd-kh1r-2026": (
            "bounded_result",
            ["adjacent_field"],
        ),
        "zenodo-19699784-dissent-v1": (
            "conceptual_context",
            ["direct_claim"],
        ),
    }[source_id]


def build_bundle() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, tuple[dict[str, Any], bytes]],
]:
    artifacts = _build_artifacts()
    recent = next(
        artifact
        for artifact in artifacts
        if artifact["lane_type"] == "recent_frontier_preprints"
    )
    graph = _version_graph(recent)
    acquisition = _build_acquisition(artifacts)
    receipts = {row["lane_id"]: row for row in acquisition["lane_receipts"]}
    descriptors: list[dict[str, Any]] = []
    capture_lanes: list[dict[str, Any]] = []
    raw_results: list[dict[str, Any]] = []
    artifacts_by_path: dict[str, tuple[dict[str, Any], bytes]] = {}
    for artifact in artifacts:
        lane_id = str(artifact["lane_id"])
        relative_path = f"{RESPONSE_DIRECTORY}/{lane_id}.json"
        data = canonical_json(artifact) + b"\n"
        artifacts_by_path[relative_path] = (artifact, data)
        receipt = receipts[lane_id]
        primary_search = _primary_search_execution(artifact)
        included_source_ids = sorted(
            link["source_id"]
            for link in artifact["normalization_links"]
            if str(link["disposition"]).startswith("included")
        )
        descriptors.append(
            {
                "lane_id": lane_id,
                "path": relative_path,
                "sha256": hashlib.sha256(data).hexdigest(),
                "size_bytes": len(data),
                "acquired_at": receipt["completed_at"],
                "provider_request_id": primary_search["execution_id"],
                "source_ids": included_source_ids,
            }
        )
        item_by_id = {
            str(item["item_id"]): item for item in artifact["result_items"]
        }
        result_ids: list[str] = []
        for link in artifact["normalization_links"]:
            item = item_by_id[str(link["item_id"])]
            source_id = str(link["source_id"])
            claim_status, tags = _capture_result_metadata(source_id)
            result_ids.append(str(link["capture_result_id"]))
            raw_results.append(
                {
                    "result_id": link["capture_result_id"],
                    "source_id": source_id,
                    "title": item["title"],
                    "url": item["url"],
                    "retrieval_status": {
                        "search_result_metadata": "tool_visible_search_metadata_captured",
                        "primary_page_metadata": "primary_page_metadata_captured",
                        "primary_api_metadata": "primary_api_metadata_captured",
                        "publisher_metadata": "publisher_metadata_captured",
                    }[item["retrieval_class"]],
                    "disposition": link["disposition"],
                    "reason": link["reason"],
                    "claim_status": claim_status,
                    "surveillance_tags": tags,
                }
            )
        capture_lanes.append(
            {
                "lane_id": lane_id,
                "lane_type": artifact["lane_type"],
                "queries": [primary_search["request"]["locator"]],
                "query_policy": (
                    "No known author, title, DOI, arXiv ID, repository record ID, "
                    "or other exact identifier was seeded into the differentiated query."
                ),
                "status": "completed",
                "raw_result_ids": result_ids,
            }
        )
    capture = _seal(
        {
            "schema_version": "2.1",
            "capture_id": "ym22-current-frontier-multi-execution-20260722",
            "target_id": TARGET_ID,
            "capture_started_at": CAPTURE_STARTED_AT,
            "capture_completed_at": CAPTURE_COMPLETED_AT,
            "coverage_cutoff": CAPTURE_COMPLETED_AT,
            "capture_mode": (
                "agent_observed_multi_execution_literature_capture_frozen_for_replay"
            ),
            "provider": {
                "provider_id": "codex-multi-execution-literature-observation",
                "name": "Codex bounded web search plus Zenodo Records API observations",
                "index": "bounded tool-visible web metadata and selected primary API metadata observed on 2026-07-22",
                "execution_boundary": (
                    "Six separate web searches and four unauthenticated primary API "
                    "requests were observed, then projected into closed artifacts."
                ),
                "raw_payload_retention": (
                    "No raw web payload or ranking trace is retained; primary API "
                    "responses are represented only by bounded digest-linked metadata atoms."
                ),
                "receipt_status": (
                    "agent_observed_unauthenticated_executions_then_frozen"
                ),
                "executable_replay_status": "frozen_response_adapter_only",
                "external_authentication_status": "unavailable",
            },
            "exhaustive_coverage_claim": False,
            "peer_validation_claim": False,
            "source_correctness_claim": False,
            "coverage_limits": list(acquisition["coverage_limits"]),
            "inclusion_policy": acquisition["inclusion_policy"],
            "exclusion_policy": acquisition["exclusion_policy"],
            "lanes": capture_lanes,
            "raw_results": raw_results,
            "provider_response_artifacts": descriptors,
            "version_lineages": [graph],
        },
        "content_digest",
    )
    validate_capture_acquisition_bundle(
        capture=capture,
        acquisition=acquisition,
        artifacts_by_path=artifacts_by_path,
        version_graphs=[graph],
    )
    return capture, acquisition, artifacts_by_path


def _exact_outputs(
    output_root: Path,
) -> tuple[dict[Path, bytes], dict[str, Any]]:
    capture, acquisition, artifacts_by_path = build_bundle()
    outputs = {
        output_root / CAPTURE_NAME: canonical_json(capture) + b"\n",
        output_root / ACQUISITION_NAME: canonical_json(acquisition) + b"\n",
    }
    outputs.update(
        {
            output_root / relative_path: data
            for relative_path, (_artifact, data) in artifacts_by_path.items()
        }
    )
    summary = {
        "capture_content_digest": capture["content_digest"],
        "acquisition_content_digest": acquisition["content_digest"],
        "theory_state_digest": acquisition["theory_state_digest"],
        "source_ids": [source["source_id"] for source in acquisition["sources"]],
        "output_count": len(outputs),
    }
    return outputs, summary


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate deterministic reproduction without changing any file",
    )
    args = parser.parse_args()
    output_root = args.output_root.resolve()
    outputs, summary = _exact_outputs(output_root)
    if args.check:
        drift = [str(path) for path, data in outputs.items() if not path.is_file() or path.read_bytes() != data]
        if drift:
            raise SystemExit("frozen literature bundle drift:\n" + "\n".join(drift))
    else:
        for path, data in sorted(outputs.items(), key=lambda row: str(row[0])):
            _atomic_write(path, data)
    print(canonical_json(summary).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
