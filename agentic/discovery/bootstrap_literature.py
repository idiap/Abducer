# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Acquire current, target-scoped literature for a new canonical research run.

The network boundary is an injected Lunar public-fetch channel. This module
uses only declared Crossref/arXiv read queries, keeps the actual response bytes,
and invokes the existing six-lane literature runner. Reopening a capture checks
its bytes and source projection without contacting providers or renewing time.
Publisher metadata and abstracts are evidence for reading and interpretation;
they do not certify a paper's claims or establish exhaustive coverage.
"""

from __future__ import annotations

import base64
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

from .contracts import ContractError, canonical_digest, canonical_json, utc_now, validate_identifier
from .literature import LANE_TYPES, _merge_sources, _timestamp, run_frontier_literature_cycle, validate_snapshot


RESOURCE_ID = "discovery-live-literature"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
RESULTS_PER_QUERY = 8
CROSSREF_ENDPOINT = "https://api.crossref.org/works"
ARXIV_ENDPOINT = "https://export.arxiv.org/api/query"
LANE_TERMS = {
    "closest_known_work": "rigorous construction known results",
    "recent_frontier_preprints": "",
    "negative_results_barriers": "barriers impossibility limitations correction retraction",
    "conceptual_genealogy": "foundations historical development survey",
    "adjacent_field_mechanisms": "connections methods mechanisms",
    "dissenting_positions": "criticism counterexamples alternative formulations",
}
LIMITATIONS = [
    "Only the declared Crossref and arXiv metadata queries were executed; coverage is bounded.",
    "Retrieved abstracts and metadata are source claims, not independently verified results.",
    "Correction and retraction coverage is incomplete; unknown status is preserved.",
    "Publication date and live query completion are distinct and neither proves global latestness.",
]


def public_query_routes() -> list[dict[str, Any]]:
    """Declare narrow read-only endpoints for Lunar's host-side query validator."""
    text = {"type": "string", "minLength": 1, "maxLength": 600}
    routes = []
    for identity, endpoint, properties in (
        ("crossref-works", CROSSREF_ENDPOINT, {
            "query.bibliographic": text, "rows": {"const": str(RESULTS_PER_QUERY)},
        }),
        ("arxiv-query", ARXIV_ENDPOINT, {
            "search_query": text, "start": {"const": "0"},
            "max_results": {"const": str(RESULTS_PER_QUERY)},
            "sortBy": {"const": "submittedDate"}, "sortOrder": {"const": "descending"},
        }),
    ):
        routes.append({"id": identity, "url": endpoint, "method": "GET",
                       "query_schema": {"type": "object", "additionalProperties": False,
                                        "properties": properties, "required": list(properties)},
                       "body_schema": None, "content_type": None, "read_only": True})
    return routes


class _Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def _text(value: Any) -> str:
    parser = _Text()
    parser.feed(str(value or ""))
    return " ".join(" ".join(parser.parts).split())


def _seal(payload: dict[str, Any]) -> dict[str, Any]:
    return {**payload, "content_digest": canonical_digest(payload)}


def _write(root: Path, name: str, content: bytes) -> dict[str, Any]:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
    return {"path": name, "sha256": hashlib.sha256(content).hexdigest(), "size": len(content)}


def _read(root: Path, descriptor: Mapping[str, Any]) -> bytes:
    raw = descriptor["path"]
    relative = PurePosixPath(raw)
    if relative.is_absolute() or "\\" in raw or any(p in {"", ".", ".."} for p in raw.split("/")):
        raise ContractError("literature capture contains an unsafe artifact path")
    path = root / relative
    if any(p.is_symlink() for p in [path, *path.parents] if p != root.parent):
        raise ContractError("literature capture artifacts cannot be symlinks")
    path.resolve().relative_to(root.resolve())
    if path.stat().st_size != descriptor["size"] or path.stat().st_size > MAX_RESPONSE_BYTES * 4:
        raise ContractError("literature capture artifact size changed")
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != descriptor["sha256"]:
        raise ContractError("literature capture artifact digest changed")
    return data


def _download(public_fetch: Callable[..., dict], url: str, query_id: str) -> bytes:
    opened = public_fetch("open", url=url, resource_id=RESOURCE_ID, query_id=query_id,
                          method="GET", headers={"accept": "*/*"})
    token = opened["token"]
    parts: list[bytes] = []
    size = 0
    try:
        while True:
            chunk = base64.b64decode(public_fetch("read", token=token, size=65536)["data"], validate=True)
            size += len(chunk)
            if size > MAX_RESPONSE_BYTES:
                raise ContractError("literature response exceeded its acquisition byte budget")
            if not chunk:
                break
            parts.append(chunk)
    finally:
        public_fetch("close", token=token)
    return b"".join(parts)


def query_for(topic: str, lane_type: str) -> tuple[str, str, str]:
    """Bind each differentiated lane to an exact query before its execution."""
    if lane_type not in LANE_TYPES or not isinstance(topic, str) or not 1 <= len(topic.strip()) <= 300:
        raise ContractError("literature acquisition needs a bounded target topic and known lane")
    query = " ".join((topic.strip(), LANE_TERMS[lane_type])).strip()
    if lane_type == "recent_frontier_preprints":
        # Quote the topic as literal arXiv search data, not caller query syntax.
        query = 'all:"' + topic.replace('"', ' ').replace('\\', ' ') + '"'
        params = {"search_query": query, "start": "0", "max_results": str(RESULTS_PER_QUERY),
                  "sortBy": "submittedDate", "sortOrder": "descending"}
        return "arxiv-query", ARXIV_ENDPOINT + "?" + urlencode(params), query
    return "crossref-works", CROSSREF_ENDPOINT + "?" + urlencode({
        "query.bibliographic": query, "rows": str(RESULTS_PER_QUERY)}), query


def _crossref_sources(data: bytes) -> list[dict[str, Any]]:
    payload = json.loads(data)
    if payload.get("status") != "ok" or payload.get("message-type") != "work-list":
        raise ContractError("Crossref did not return a successful work-list")
    records = payload["message"]["items"]
    if not isinstance(records, list) or len(records) > RESULTS_PER_QUERY:
        raise ContractError("Crossref result count exceeded the declared query")
    sources = []
    for row in records:
        doi = row.get("DOI")
        title = _text((row.get("title") or [""])[0])
        authors = [_text(" ".join(filter(None, [a.get("given"), a.get("family"), a.get("name")])))
                   for a in row.get("author", [])]
        authors = [name for name in authors if name]
        if not doi or not title or not authors:
            continue  # Incomplete bibliographic rows remain visible in the raw response.
        date = row.get("published", {}).get("date-parts", [["unknown"]])[0]
        abstract = _text(row.get("abstract"))
        sources.append({"work_identity": "doi:" + doi.lower(), "doi": doi,
            "title": title, "authors": authors, "publication_date": "-".join(map(str, date)),
            "source_version": "crossref-metadata-" + canonical_digest(row).split(":")[-1],
            "source_type": "preprint" if row.get("type") == "posted-content" else "primary",
            "url": "https://doi.org/" + doi, "correction_status": "unknown",
            "decision_relevant": False, "claims": [abstract] if abstract else [],
            "limitations": ["Crossref member-deposited metadata; full text and correction history were not verified.",
                            "Relevance and scientific implications require a separate target-scoped assessment."]})
    return sources


def _arxiv_sources(data: bytes) -> list[dict[str, Any]]:
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise ContractError("arXiv response contains an unsupported XML declaration")
    feed = ET.fromstring(data)
    atom = "{http://www.w3.org/2005/Atom}"
    if feed.tag != atom + "feed":
        raise ContractError("arXiv did not return an Atom feed")
    entries = feed.findall(atom + "entry")
    if len(entries) > RESULTS_PER_QUERY:
        raise ContractError("arXiv result count exceeded the declared query")
    sources = []
    for row in entries:
        identity = (row.findtext(atom + "id") or "").strip()
        if "/api/errors" in identity:
            raise ContractError("arXiv returned an API error entry")
        if not identity.startswith(("http://arxiv.org/abs/", "https://arxiv.org/abs/")):
            raise ContractError("arXiv result has an unexpected work identity")
        arxiv_id = identity.split("/abs/", 1)[1]
        abstract = _text(row.findtext(atom + "summary"))
        sources.append({"work_identity": "arxiv:" + arxiv_id.rsplit("v", 1)[0], "arxiv_id": arxiv_id,
            "title": _text(row.findtext(atom + "title")),
            "authors": [_text(author.findtext(atom + "name")) for author in row.findall(atom + "author")],
            "publication_date": row.findtext(atom + "published") or "unknown",
            "source_version": arxiv_id, "source_type": "preprint", "url": "https://arxiv.org/abs/" + arxiv_id,
            "correction_status": "unknown", "decision_relevant": False, "claims": [abstract] if abstract else [],
            "limitations": ["arXiv author-supplied abstract; full text, peer review and correction history were not verified.",
                            "Relevance and scientific implications require a separate target-scoped assessment."]})
    return sources


def acquire_current_literature(*, target_id: str, run_id: str, theory_state_digest: str,
                               topic: str, root: Path, public_fetch: Callable[..., dict]) -> dict[str, Any]:
    """Execute all six declared queries and retain failures before refusing admission."""
    validate_identifier(target_id, "target_id")
    validate_identifier(run_id, "run_id")
    root.mkdir(parents=True, exist_ok=False)
    queries = {lane: query_for(topic, lane) for lane in LANE_TYPES}
    request = {"target_id": target_id, "claim_scope": topic, "theory_state_digest": theory_state_digest,
        "coverage_limits": LIMITATIONS, "search_lanes": [
            {"lane_type": lane, "queries": [queries[lane][2]],
             "inclusion_policy": "Retain bibliographically identified responses for subsequent relevance assessment.",
             "exclusion_policy": "Exclude records lacking identity/title/authors; retain their raw bytes for audit."}
            for lane in LANE_TYPES]}
    captures: list[dict[str, Any]] = []

    def provider(lane: Mapping[str, Any]) -> dict[str, Any]:
        lane_type = lane["lane_type"]
        query_id, url, query = queries[lane_type]
        started = utc_now()
        raw = _download(public_fetch, url, query_id)
        completed = utc_now()
        descriptor = _write(root, lane_type + "/response.raw", raw)
        sources = _arxiv_sources(raw) if query_id == "arxiv-query" else _crossref_sources(raw)
        captures.append(_seal({"lane_type": lane_type, "query_id": query_id, "url": url,
            "query": query, "started_at": started, "completed_at": completed, "response": descriptor,
            "sources_digest": canonical_digest(sources)}))
        return {"provider": "arXiv" if query_id == "arxiv-query" else "Crossref",
                "index": url.split("?", 1)[0], "execution_mode": "live", "status": "completed",
                "coverage_cutoff": completed, "sources": sources}

    # Lunar's fetch RPC carries one bounded response stream at a time.
    snapshot = run_frontier_literature_cycle(request, providers={lane: provider for lane in LANE_TYPES}, max_workers=1)
    snapshot_file = _write(root, "snapshot.json", canonical_json(snapshot) + b"\n")
    manifest = _seal({"version": 1, "target_id": target_id, "run_id": run_id,
                     "theory_state_digest": theory_state_digest, "request": request,
                     "captures": captures, "snapshot": snapshot_file})
    _write(root, "acquisition.json", canonical_json(manifest) + b"\n")
    if snapshot["provenance_mode"] != "live" or snapshot["validation_status"] != "validated":
        raise ContractError("current literature acquisition failed; inspect the retained lane receipts")
    if not any(source["claims"] for source in snapshot["sources"]):
        raise ContractError("current acquisition has no source abstracts to ground research")
    return {"manifest": manifest, "snapshot": snapshot}


def reopen_acquisition(root: Path, *, expected_digest: str, target_id: str, run_id: str,
                       theory_state_digest: str) -> dict[str, Any]:
    """Verify a previously acquired snapshot without changing its freshness."""
    manifest_path = root / "acquisition.json"
    if any(path.is_symlink() for path in (manifest_path, *manifest_path.parents)):
        raise ContractError("literature capture manifest cannot be a symlink")
    if not manifest_path.is_file() or manifest_path.stat().st_size > MAX_RESPONSE_BYTES:
        raise ContractError("literature capture manifest exceeds its byte boundary")
    manifest = json.loads(manifest_path.read_bytes())
    core = {key: value for key, value in manifest.items() if key != "content_digest"}
    if manifest["content_digest"] != expected_digest or canonical_digest(core) != expected_digest:
        raise ContractError("literature acquisition commitment changed")
    if (manifest["target_id"], manifest["run_id"], manifest["theory_state_digest"]) != (target_id, run_id, theory_state_digest):
        raise ContractError("literature acquisition crossed target/run/theory identity")
    snapshot = json.loads(_read(root, manifest["snapshot"]))
    validate_snapshot(snapshot)
    for value in (snapshot, manifest["request"]):
        if (value["target_id"], value["theory_state_digest"]) != (target_id, theory_state_digest):
            raise ContractError("literature snapshot or request crossed target/theory identity")
    if snapshot["claim_scope"] != manifest["request"]["claim_scope"]:
        raise ContractError("literature snapshot scope differs from its request")
    if snapshot["provenance_mode"] != "live" or snapshot["validation_status"] != "validated":
        raise ContractError("literature acquisition is incomplete")
    if [row["lane_type"] for row in manifest["captures"]] != list(LANE_TYPES):
        raise ContractError("literature acquisition does not contain exactly six ordered captures")
    observations = []
    for capture, receipt in zip(manifest["captures"], snapshot["lane_receipts"]):
        if _seal({k: v for k, v in capture.items() if k != "content_digest"}) != capture:
            raise ContractError("literature capture seal changed")
        if (capture["query_id"], capture["url"], capture["query"]) != query_for(snapshot["claim_scope"], capture["lane_type"]):
            raise ContractError("literature capture query differs from its target/lane")
        if (receipt["lane_type"] != capture["lane_type"]
                or receipt["index"] != capture["url"].split("?", 1)[0]
                or receipt["execution_mode"] != "live" or receipt["status"] != "completed"
                or not (_timestamp(receipt["started_at"]) <= _timestamp(capture["started_at"])
                        <= _timestamp(capture["completed_at"]) <= _timestamp(receipt["completed_at"]))
                or receipt["coverage_cutoff"] != capture["completed_at"]):
            raise ContractError("literature capture differs from its execution receipt")
        raw = _read(root, capture["response"])
        sources = _arxiv_sources(raw) if capture["query_id"] == "arxiv-query" else _crossref_sources(raw)
        if canonical_digest(sources) != capture["sources_digest"] or receipt["queries"] != [capture["query"]]:
            raise ContractError("literature sources differ from the recorded provider response")
        observations.extend((receipt["lane_id"], source) for source in sources)
    sources, duplicates, conflicts, metadata = _merge_sources(observations)
    if (sources, duplicates, conflicts, metadata) != (snapshot["sources"], snapshot["duplicate_groups"], snapshot["claim_conflicts"], snapshot["metadata_conflicts"]):
        raise ContractError("literature snapshot differs from raw response projections")
    return snapshot
