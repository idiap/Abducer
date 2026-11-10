"""Target-scoped frontier literature search and causal theory assimilation.

The module keeps three notions deliberately separate: when a search actually
completed, when a work was published, and when a file happened to be written.
Only receipt-backed lane completion establishes search freshness.  A frozen
snapshot then becomes useful only through claim-level mappings that name the
concepts, mechanisms, barriers, hypotheses, or actions it changes.

Provider integrations are dependency-injected callables.  This lets production
adapters perform live searches while tests use immutable fixture providers; an
inline/local corpus is always classified ``local_only`` and can never launder a
generated bibliography into a recent search.
"""

from __future__ import annotations

import copy
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Mapping, Sequence

from .contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    utc_now,
    validate_payload,
)


LANE_TYPES: tuple[str, ...] = (
    "closest_known_work",
    "recent_frontier_preprints",
    "negative_results_barriers",
    "conceptual_genealogy",
    "adjacent_field_mechanisms",
    "dissenting_positions",
)
MAPPING_EVENTS = {
    "spawn",
    "merge",
    "split",
    "reframe",
    "demote",
    "retire",
    "reprioritize",
    "new_question",
    "justified_no_change",
}
HYPOTHESIS_RELATIONS = {
    "apparently_open",
    "partly_anticipated",
    "known_special_case",
    "absorbed",
    "contradicted",
    "independent",
    "cross_field_bridge",
    "coverage_unknown",
}
Provider = Callable[[Mapping[str, Any]], Mapping[str, Any]]

CLAIM_MAPPING_AUTHORITY_ID = "deterministic-claim-mapper.v1"
CLAIM_MAPPING_ALGORITHM_ID = "content-token-and-status-rules.v1"
THEORY_OBJECT_KINDS = {
    "concept",
    "assumption",
    "mechanism",
    "barrier",
    "comparator",
    "hypothesis",
    "genealogy",
    "proof_obligation",
    "schedule",
}
LITERATURE_REPLAY_OPERATIONS = {
    "delete_source",
    "no_literature",
    "supersede_source",
    "contradict_source",
    "coverage_only_change",
}
_TOKEN = re.compile(r"[a-z0-9][a-z0-9_-]*", re.I)
_MAPPING_POLICY = {
    "algorithm_id": CLAIM_MAPPING_ALGORITHM_ID,
    "normalization": "lowercase alphanumeric tokens; exact term-token containment",
    "object_selection": "all theory objects tied for maximal positive matched-term weight",
    "unmatched_policy": "map to the unique scope anchor as justified_no_change",
    "status_precedence": ["retracted", "superseded_or_corrected", "claim_signals"],
    "claim_signal_precedence": [
        "contradiction",
        "split",
        "merge",
        "spawn",
        "new_question",
        "reprioritize",
        "justified_no_change",
    ],
}
_EVENT_LANGUAGE = {
    "spawn": ("sharpens", "spawned", "opened"),
    "merge": ("absorbs", "merged", "reframed"),
    "split": ("reframes", "split", "opened"),
    "reframe": ("reframes", "reframed", "reframed"),
    "demote": ("contradicts", "challenged", "demoted"),
    "retire": ("contradicts", "retired", "retired"),
    "reprioritize": ("supports", "reprioritized", "reprioritized"),
    "new_question": ("leaves_open", "question_spawned", "opened"),
    "justified_no_change": ("leaves_open", "unchanged", "preserved"),
}
_CLAIM_SIGNALS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "demote",
        (
            "contradict",
            "counterexample",
            "incompatible",
            "impossible",
            "no-go",
            "rules out",
            "cannot hold",
            "fails",
        ),
    ),
    ("split", ("distinguishes", "separates", "splits", "inequivalent regimes")),
    ("merge", ("unifies", "absorbs", "equivalent", "common mechanism", "same mechanism")),
    ("spawn", ("introduces", "constructs", "new mechanism", "new concept", "mediates", "defines")),
    ("new_question", ("open question", "remains open", "unknown whether", "unresolved")),
    (
        "reprioritize",
        (
            "supports",
            "confirms",
            "establishes",
            "proves",
            "strengthens",
            "yields",
            "produces",
            "carries",
            "obtains",
        ),
    ),
)


def _without(payload: Mapping[str, Any], *keys: str) -> dict[str, Any]:
    """Return a deep copy without envelope fields that would make a digest circular."""

    result = copy.deepcopy(dict(payload))
    for key in keys:
        result.pop(key, None)
    return result


def _timestamp(raw: str) -> datetime:
    """Parse an RFC-3339 timestamp and require an explicit timezone."""

    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ContractError(f"invalid timestamp: {raw!r}") from exc
    if parsed.tzinfo is None:
        raise ContractError(f"timestamp lacks timezone: {raw!r}")
    return parsed.astimezone(timezone.utc)


def _source_identity(source: Mapping[str, Any]) -> str:
    """Resolve work identity by DOI, arXiv, explicit ID, then title/author lineage."""

    doi = str(source.get("doi") or "").strip().lower()
    if doi:
        return f"doi:{doi.removeprefix('https://doi.org/')}"
    arxiv = str(source.get("arxiv_id") or "").strip().lower()
    if arxiv:
        return f"arxiv:{arxiv.removeprefix('arxiv:')}"
    explicit = str(source.get("work_identity") or "").strip().lower()
    if explicit:
        return explicit
    title = " ".join(str(source.get("title") or "").lower().split())
    authors = ",".join(sorted(str(item).strip().lower() for item in source.get("authors", [])))
    if not title or not authors:
        raise ContractError("a source needs DOI, arXiv ID, work_identity, or title plus authors")
    return f"title-author:{canonical_digest([title, authors]).split(':', 1)[-1][:24]}"


def _normalize_source(raw: Mapping[str, Any], lane_id: str) -> dict[str, Any]:
    """Normalize a provider source into the immutable snapshot representation."""

    source = copy.deepcopy(dict(raw))
    identity = _source_identity(source)
    source_id = str(source.get("source_id") or stable_identifier("source", identity, source.get("source_version", "unknown")))
    normalized: dict[str, Any] = {
        "source_id": source_id,
        "work_identity": identity,
        "title": str(source.get("title") or "").strip(),
        "authors": [str(item).strip() for item in source.get("authors", []) if str(item).strip()],
        "publication_date": str(source.get("publication_date") or "unknown").strip(),
        "source_version": str(source.get("source_version") or "version-unknown").strip(),
        "source_type": str(source.get("source_type") or "other"),
        "url": str(source.get("url") or "unavailable").strip(),
        "doi": source.get("doi"),
        "arxiv_id": source.get("arxiv_id"),
        "correction_status": str(source.get("correction_status") or "unknown"),
        "lane_ids": [lane_id],
        "decision_relevant": bool(source.get("decision_relevant", True)),
        "claims": sorted({str(item).strip() for item in source.get("claims", []) if str(item).strip()}),
        "limitations": sorted(
            {str(item).strip() for item in source.get("limitations", []) if str(item).strip()}
            or {"Provider did not supply a more specific limitation."}
        ),
    }
    if not normalized["title"] or not normalized["authors"]:
        raise ContractError(f"source {source_id!r} lacks title or authors")
    normalized["content_digest"] = canonical_digest(_without(normalized, "content_digest"))
    return normalized


def _merge_sources(
    lane_sources: Iterable[tuple[str, Mapping[str, Any]]],
) -> tuple[list[dict[str, Any]], list[list[str]], list[dict[str, Any]]]:
    """Deduplicate work/version identities and retain claim disagreements."""

    by_identity: dict[tuple[str, str], dict[str, Any]] = {}
    duplicate_groups: dict[tuple[str, str], list[str]] = {}
    claim_conflicts: list[dict[str, Any]] = []
    for lane_id, raw in lane_sources:
        source = _normalize_source(raw, lane_id)
        key = (source["work_identity"], source["source_version"])
        if key not in by_identity:
            by_identity[key] = source
            duplicate_groups[key] = [source["source_id"]]
            continue
        incumbent = by_identity[key]
        duplicate_groups[key].append(source["source_id"])
        incumbent_claims = set(incumbent["claims"])
        incoming_claims = set(source["claims"])
        if incumbent_claims and incoming_claims and incumbent_claims != incoming_claims:
            claim_conflicts.append(
                {
                    "work_identity": source["work_identity"],
                    "source_version": source["source_version"],
                    "source_ids": sorted(
                        {incumbent["source_id"], source["source_id"]}
                    ),
                    "claims_by_lane": {
                        incumbent["lane_ids"][0]: sorted(incumbent_claims),
                        lane_id: sorted(incoming_claims),
                    },
                    "resolution": (
                        "Retain both source-scoped formulations for claim-level "
                        "assimilation; deduplication does not infer agreement."
                    ),
                }
            )
        incumbent["lane_ids"] = sorted(set(incumbent["lane_ids"] + source["lane_ids"]))
        incumbent["claims"] = sorted(set(incumbent["claims"] + source["claims"]))
        incumbent["limitations"] = sorted(set(incumbent["limitations"] + source["limitations"]))
        incumbent["decision_relevant"] = incumbent["decision_relevant"] or source["decision_relevant"]
        incumbent["content_digest"] = canonical_digest(_without(incumbent, "content_digest"))
    groups = [sorted(set(ids)) for ids in duplicate_groups.values() if len(set(ids)) > 1]
    return (
        sorted(by_identity.values(), key=lambda item: item["source_id"]),
        sorted(groups),
        sorted(
            claim_conflicts,
            key=lambda item: (
                item["work_identity"],
                canonical_digest(item),
            ),
        ),
    )


def _execute_lane(lane_request: Mapping[str, Any], provider: Provider | None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Execute one differentiated lane and return an every-attempt receipt.

    Absence of an adapter is not treated as remote execution.  Inline sources
    form a bounded local corpus and therefore force ``local_only`` provenance.
    """

    lane = copy.deepcopy(dict(lane_request))
    lane_type = str(lane.get("lane_type") or "")
    if lane_type not in LANE_TYPES:
        raise ContractError(f"unsupported literature lane: {lane_type!r}")
    lane_id = str(lane.get("lane_id") or stable_identifier("literature-lane", lane_type, lane.get("queries", [])))
    queries = [str(item).strip() for item in lane.get("queries", []) if str(item).strip()]
    if not queries:
        raise ContractError(f"lane {lane_id} requires at least one exact query")
    started = utc_now()
    failure: str | None = None
    try:
        if provider is None:
            response: Mapping[str, Any] = {
                "provider": lane.get("provider", "bounded-local-corpus"),
                "index": lane.get("index", "inline-records"),
                "execution_mode": "local_only",
                "sources": lane.get("sources", []),
                "coverage_cutoff": lane.get("coverage_cutoff", "explicitly unknown"),
            }
        else:
            # A deep copy prevents a provider from changing the request shared by
            # other parallel lanes.  The adapter itself declares live/local mode.
            response = provider(copy.deepcopy(lane))
        sources = [copy.deepcopy(dict(item)) for item in response.get("sources", [])]
        status = str(response.get("status", "completed"))
        if status not in {"completed", "partial", "failed"}:
            raise ContractError(f"provider returned unsupported status {status!r}")
    except Exception as exc:  # Every operational failure still becomes a receipt.
        response = {
            "provider": lane.get("provider", "unavailable"),
            "index": lane.get("index", "unavailable"),
            "execution_mode": "local_only",
            "coverage_cutoff": lane.get("coverage_cutoff", "explicitly unknown"),
        }
        sources = []
        status = "failed"
        failure = f"{type(exc).__name__}: {exc}"
    completed = utc_now()
    execution_mode = str(response.get("execution_mode", "local_only"))
    if execution_mode not in {"live", "local_only"}:
        execution_mode = "local_only"
    provider_name = str(response.get("provider") or lane.get("provider") or "unavailable")
    index_name = str(response.get("index") or lane.get("index") or "unavailable")
    source_ids = [str(item.get("source_id") or stable_identifier("source", _source_identity(item), item.get("source_version", "unknown"))) for item in sources]
    receipt_core = {
        "lane_id": lane_id,
        "lane_type": lane_type,
        "queries": queries,
        "provider": provider_name,
        "index": index_name,
        "execution_mode": execution_mode,
        "started_at": started,
        "completed_at": completed,
        "status": status,
        "result_count": len(sources),
        "source_ids": sorted(set(source_ids)),
        "coverage_cutoff": str(response.get("coverage_cutoff") or lane.get("coverage_cutoff") or "explicitly unknown"),
        "inclusion_policy": str(lane.get("inclusion_policy") or "Include sources responsive to the exact target and lane scope."),
        "exclusion_policy": str(lane.get("exclusion_policy") or "Exclude target-mismatched, unverifiable, and duplicate-version records."),
        "failure": failure,
    }
    receipt_core["content_digest"] = canonical_digest(receipt_core)
    receipt_core["validator_receipt_ids"] = [stable_identifier("validator", lane_id, receipt_core["content_digest"])]
    return receipt_core, sources


def run_frontier_literature_cycle(
    request: Mapping[str, Any],
    *,
    providers: Mapping[str, Provider] | None = None,
    max_workers: int = 6,
) -> dict[str, Any]:
    """Execute six independent search lanes and freeze a validated snapshot.

    ``providers`` is keyed by lane type.  A callable is the execution boundary;
    without one, that lane is explicitly local-only.  The runner never promotes
    inline data to live provenance based on caller labels.
    """

    target_id = str(request.get("target_id") or "").strip()
    claim_scope = str(request.get("claim_scope") or "").strip()
    theory_digest = str(request.get("theory_state_digest") or "").strip()
    if not target_id or not claim_scope or not theory_digest:
        raise ContractError("target_id, claim_scope, and theory_state_digest are required")
    requested = {str(item.get("lane_type")): dict(item) for item in request.get("search_lanes", [])}
    missing = [lane_type for lane_type in LANE_TYPES if lane_type not in requested]
    if missing:
        raise ContractError(f"missing differentiated literature lanes: {', '.join(missing)}")
    providers = dict(providers or {})
    receipts: list[dict[str, Any]] = []
    raw_sources: list[tuple[str, Mapping[str, Any]]] = []
    with ThreadPoolExecutor(max_workers=max(1, min(max_workers, len(LANE_TYPES)))) as executor:
        future_lanes = {
            executor.submit(_execute_lane, requested[lane_type], providers.get(lane_type)): lane_type
            for lane_type in LANE_TYPES
        }
        for future in as_completed(future_lanes):
            receipt, sources = future.result()
            receipts.append(receipt)
            raw_sources.extend((receipt["lane_id"], source) for source in sources)
    receipts.sort(key=lambda item: LANE_TYPES.index(item["lane_type"]))
    sources, duplicate_groups, detected_claim_conflicts = _merge_sources(
        raw_sources
    )
    search_started = min(receipt["started_at"] for receipt in receipts)
    search_completed = max(receipt["completed_at"] for receipt in receipts)
    fully_live = all(
        receipt["execution_mode"] == "live" and receipt["status"] == "completed"
        for receipt in receipts
    )
    core: dict[str, Any] = {
        "schema_version": "1.0",
        "snapshot_id": stable_identifier("literature-snapshot", target_id, claim_scope, theory_digest, receipts, sources),
        "target_id": target_id,
        "claim_scope": claim_scope,
        "theory_state_digest": theory_digest,
        "search_started_at": search_started,
        "search_completed_at": search_completed,
        "coverage_cutoff": str(request.get("coverage_cutoff") or max(receipt["coverage_cutoff"] for receipt in receipts)),
        "provenance_mode": "live" if fully_live else "local_only",
        "inclusion_policy": str(request.get("inclusion_policy") or "Lane-specific responsive sources with resolvable work identity."),
        "exclusion_policy": str(request.get("exclusion_policy") or "Target mismatch, duplicate versions, unverifiable identity, and explicit exclusions."),
        "lane_receipts": receipts,
        "sources": sources,
        "result_count": len(sources),
        "coverage_limits": [
            str(item).strip()
            for item in request.get("coverage_limits", ["Coverage is bounded by the named queries, providers, indexes, and cutoff."])
            if str(item).strip()
        ],
        "duplicate_groups": duplicate_groups,
        "claim_conflicts": (
            detected_claim_conflicts
            + copy.deepcopy(list(request.get("claim_conflicts", [])))
        ),
    }
    core["content_digest"] = canonical_digest(_without(core, "content_digest", "validator_receipts", "validation_status"))
    validator_status = "passed" if all(receipt["status"] == "completed" for receipt in receipts) else "failed"
    core["validator_receipts"] = [
        {
            "receipt_id": stable_identifier("snapshot-validator", core["snapshot_id"], core["content_digest"]),
            "validator_id": "target-literature-snapshot-validator.v1",
            "status": validator_status,
            "validated_digest": core["content_digest"],
            "completed_at": utc_now(),
            "reason_codes": [] if validator_status == "passed" else ["incomplete_search_lane"],
        }
    ]
    core["validation_status"] = "validated" if validator_status == "passed" else "invalid"
    validate_snapshot(core)
    return core


def validate_snapshot(snapshot: Mapping[str, Any]) -> None:
    """Validate schema plus freshness, target, digest, and lane-provenance invariants."""

    validate_payload(dict(snapshot), "target_literature_search_snapshot.schema.json")
    receipts = list(snapshot["lane_receipts"])
    lane_types = [receipt["lane_type"] for receipt in receipts]
    if set(lane_types) != set(LANE_TYPES) or len(lane_types) != len(set(lane_types)):
        raise ContractError("snapshot must contain exactly one receipt for every differentiated lane")
    if snapshot["result_count"] != len(snapshot["sources"]):
        raise ContractError("result_count does not match reduced source count")
    expected = canonical_digest(_without(snapshot, "content_digest", "validator_receipts", "validation_status"))
    if snapshot["content_digest"] != expected:
        raise ContractError("snapshot content digest mismatch")
    completion = max(_timestamp(receipt["completed_at"]) for receipt in receipts)
    if _timestamp(snapshot["search_completed_at"]) != completion:
        raise ContractError("snapshot completion must be the latest actual lane completion")
    starts = min(_timestamp(receipt["started_at"]) for receipt in receipts)
    if _timestamp(snapshot["search_started_at"]) != starts:
        raise ContractError("snapshot start must be the earliest actual lane start")
    expected_mode = "live" if all(
        receipt["execution_mode"] == "live" and receipt["status"] == "completed"
        for receipt in receipts
    ) else "local_only"
    if snapshot["provenance_mode"] != expected_mode:
        raise ContractError("live provenance requires every differentiated lane to execute successfully through a live adapter")
    all_lanes_completed = all(
        receipt["status"] == "completed" for receipt in receipts
    )
    if snapshot["validation_status"] == "validated" and not all_lanes_completed:
        raise ContractError(
            "a validated snapshot cannot contain partial or failed search lanes"
        )
    for receipt in receipts:
        receipt_core = _without(
            receipt, "content_digest", "validator_receipt_ids"
        )
        if receipt["content_digest"] != canonical_digest(receipt_core):
            raise ContractError(
                f"literature lane {receipt['lane_id']} content digest mismatch"
            )
    known_lanes = {receipt["lane_id"] for receipt in receipts}
    for source in snapshot["sources"]:
        if not set(source["lane_ids"]).issubset(known_lanes):
            raise ContractError(f"source {source['source_id']} cites an unknown lane")
        expected_source = canonical_digest(_without(source, "content_digest"))
        if source["content_digest"] != expected_source:
            raise ContractError(f"source {source['source_id']} content digest mismatch")
    passed = [receipt for receipt in snapshot["validator_receipts"] if receipt["status"] == "passed"]
    if snapshot["validation_status"] == "validated" and not any(
        receipt["validated_digest"] == snapshot["content_digest"] for receipt in passed
    ):
        raise ContractError("validated snapshot lacks a passing digest-bound validator receipt")


def select_newest_snapshot(
    snapshots: Iterable[Mapping[str, Any]],
    *,
    target_id: str,
    claim_scope: str | None = None,
    theory_state_digest: str | None = None,
) -> dict[str, Any]:
    """Select by validated completion metadata and digest, never file mtime or alias."""

    admissible: list[dict[str, Any]] = []
    for candidate in snapshots:
        snapshot = copy.deepcopy(dict(candidate))
        try:
            validate_snapshot(snapshot)
        except ContractError:
            continue
        if snapshot["validation_status"] != "validated" or snapshot["target_id"] != target_id:
            continue
        if claim_scope is not None and snapshot["claim_scope"] != claim_scope:
            continue
        if theory_state_digest is not None and snapshot["theory_state_digest"] != theory_state_digest:
            continue
        admissible.append(snapshot)
    if not admissible:
        raise ContractError("no validated target-scoped snapshot matches the active target, scope, and theory state")
    return max(admissible, key=lambda item: (_timestamp(item["search_completed_at"]), item["content_digest"]))


def _source_delta(snapshot: Mapping[str, Any], prior_snapshot: Mapping[str, Any] | None) -> dict[str, list[str]]:
    """Separate work/version changes from source age; old discoveries remain salient."""

    current = {item["source_id"]: item for item in snapshot["sources"]}
    prior = {item["source_id"]: item for item in (prior_snapshot or {}).get("sources", [])}
    added = sorted(set(current) - set(prior))
    removed = sorted(
        source_id for source_id in set(prior) - set(current)
        if prior[source_id].get("correction_status") == "retracted"
    )
    corrected = sorted(
        source_id for source_id in set(current) & set(prior)
        if current[source_id].get("source_version") != prior[source_id].get("source_version")
        or current[source_id].get("correction_status") != prior[source_id].get("correction_status")
    )
    search_year = _timestamp(snapshot["search_completed_at"]).year
    old_new: list[str] = []
    for source_id in added:
        raw = str(current[source_id].get("publication_date", ""))[:4]
        if raw.isdigit() and search_year - int(raw) >= 10:
            old_new.append(source_id)
    unchanged = sorted(
        source_id for source_id in set(current) & set(prior)
        if current[source_id].get("decision_relevant") and source_id not in corrected
    )
    return {
        "added": added,
        "removed_or_retracted": removed,
        "corrected_or_superseded": corrected,
        "newly_relevant_old_sources": sorted(old_new),
        "unchanged_decisive_sources": unchanged,
    }


def _tokens(value: str) -> frozenset[str]:
    """Return the auditable token representation used by the claim mapper."""

    return frozenset(match.group(0).lower() for match in _TOKEN.finditer(value))


def build_theory_object_catalog(
    *,
    target_id: str,
    theory_state_digest: str,
    theory_objects: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Freeze the theory-side vocabulary against which source claims are mapped.

    A catalog describes theory objects and their admissible matching vocabulary;
    it does not prescribe a literature relation or event.  Those outcomes are
    derived from source status and claim content by the fixed mapping policy.
    Exactly one scope anchor is required so an unrelated source can produce an
    explicit, auditable no-change result rather than disappearing silently.
    """

    if not target_id or not theory_state_digest:
        raise ContractError("theory catalog requires target_id and theory_state_digest")
    normalized: list[dict[str, Any]] = []
    for raw in theory_objects:
        theory_object_id = str(raw.get("theory_object_id") or "").strip()
        object_kind = str(raw.get("object_kind") or "").strip()
        label = str(raw.get("label") or "").strip()
        match_terms = sorted(
            {" ".join(str(item).lower().split()) for item in raw.get("match_terms", []) if str(item).strip()}
        )
        if not theory_object_id or not label or not match_terms:
            raise ContractError(
                "every theory object needs theory_object_id, label, and non-empty match_terms"
            )
        if object_kind not in THEORY_OBJECT_KINDS:
            raise ContractError(f"unsupported theory object kind: {object_kind!r}")
        normalized.append(
            {
                "theory_object_id": theory_object_id,
                "object_kind": object_kind,
                "label": label,
                "match_terms": match_terms,
                "scope_anchor": bool(raw.get("scope_anchor", False)),
            }
        )
    if not normalized:
        raise ContractError("theory catalog requires at least one theory object")
    if len({item["theory_object_id"] for item in normalized}) != len(normalized):
        raise ContractError("theory object identifiers must be unique")
    anchors = [item for item in normalized if item["scope_anchor"]]
    if len(anchors) != 1:
        raise ContractError("theory catalog requires exactly one scope anchor")
    catalog: dict[str, Any] = {
        "schema_version": "1.0",
        "catalog_id": stable_identifier(
            "theory-object-catalog", target_id, theory_state_digest, normalized
        ),
        "target_id": target_id,
        "theory_state_digest": theory_state_digest,
        "theory_objects": sorted(normalized, key=lambda item: item["theory_object_id"]),
    }
    catalog["content_digest"] = canonical_digest(_without(catalog, "content_digest"))
    validate_theory_object_catalog(catalog)
    return catalog


def validate_theory_object_catalog(catalog: Mapping[str, Any]) -> None:
    """Validate a theory catalog and its content binding."""

    validate_payload(dict(catalog), "theory_object_catalog.schema.json")
    if catalog["content_digest"] != canonical_digest(_without(catalog, "content_digest")):
        raise ContractError("theory object catalog content digest mismatch")
    anchors = [item for item in catalog["theory_objects"] if item["scope_anchor"]]
    if len(anchors) != 1:
        raise ContractError("theory object catalog must retain exactly one scope anchor")
    if len({item["theory_object_id"] for item in catalog["theory_objects"]}) != len(
        catalog["theory_objects"]
    ):
        raise ContractError("theory object catalog contains duplicate identifiers")


def _claim_object_matches(
    claim: str,
    theory_objects: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Score explicit term containment without inferring semantic agreement."""

    claim_tokens = _tokens(claim)
    matches: list[dict[str, Any]] = []
    for theory_object in theory_objects:
        if theory_object["scope_anchor"]:
            continue
        matched_terms: list[str] = []
        matched_weight = 0
        for term in theory_object["match_terms"]:
            term_tokens = _tokens(term)
            if term_tokens and term_tokens.issubset(claim_tokens):
                matched_terms.append(term)
                matched_weight += len(term_tokens)
        if matched_terms:
            matches.append(
                {
                    "theory_object_id": theory_object["theory_object_id"],
                    "object_kind": theory_object["object_kind"],
                    "matched_terms": matched_terms,
                    "matched_weight": matched_weight,
                }
            )
    if not matches:
        return []
    maximum = max(item["matched_weight"] for item in matches)
    return sorted(
        (item for item in matches if item["matched_weight"] == maximum),
        key=lambda item: item["theory_object_id"],
    )


def _derive_event(source: Mapping[str, Any], *, matched: bool, claim: str) -> str:
    """Derive one causal event from immutable status and ordered claim signals."""

    if not matched:
        return "justified_no_change"
    correction_status = str(source.get("correction_status") or "unknown")
    if correction_status == "retracted":
        return "retire"
    if correction_status in {"superseded", "corrected"}:
        return "reframe"
    normalized_claim = " ".join(claim.lower().split())
    for event_type, signals in _CLAIM_SIGNALS:
        if any(signal in normalized_claim for signal in signals):
            return event_type
    return "justified_no_change"


def _derive_one_claim_mapping(
    *,
    source: Mapping[str, Any],
    exact_claim: str,
    theory_objects: Sequence[Mapping[str, Any]],
    scope_anchor: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    catalog: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Derive one independently receipted mapping from one distinct claim."""

    matches = _claim_object_matches(exact_claim, theory_objects)
    matched = bool(matches)
    selected_objects = matches or [
        {
            "theory_object_id": scope_anchor["theory_object_id"],
            "object_kind": scope_anchor["object_kind"],
            "matched_terms": [],
            "matched_weight": 0,
        }
    ]
    event_type = _derive_event(source, matched=matched, claim=exact_claim)
    relation, concept_disposition, branch_disposition = _EVENT_LANGUAGE[event_type]
    theory_object_ids = [item["theory_object_id"] for item in selected_objects]
    object_kinds = sorted({item["object_kind"] for item in selected_objects})
    exact_claim_digest = canonical_digest(exact_claim)
    mapping_id = stable_identifier(
        "derived-source-theory-map",
        source["source_id"],
        source["content_digest"],
        catalog["content_digest"],
        theory_object_ids,
        event_type,
        exact_claim_digest,
    )
    if matched:
        conceptual_change = (
            f"Derived {event_type} for {', '.join(theory_object_ids)} from "
            f"source claim {exact_claim_digest}: {exact_claim}"
        )
    else:
        conceptual_change = (
            f"Justified no change to scope anchor {scope_anchor['theory_object_id']}: "
            f"no catalog match term occurs in claim {exact_claim_digest}."
        )
    mapping = {
        "mapping_id": mapping_id,
        "source_id": source["source_id"],
        "theory_object_ids": theory_object_ids,
        "object_kinds": object_kinds,
        "relation": relation,
        "exact_claim": exact_claim,
        "source_limitation": sorted(source["limitations"])[0],
        "conceptual_change": conceptual_change,
        "event_type": event_type,
        "coverage_limits": list(snapshot["coverage_limits"]),
        "confidence": (
            "high"
            if sum(item["matched_weight"] for item in matches) >= 3
            else ("medium" if matched else "low")
        ),
    }
    matched_terms = sorted(
        {term for item in selected_objects for term in item["matched_terms"]}
    )
    receipt = {
        "receipt_id": stable_identifier(
            "claim-mapping-receipt", mapping_id, source["content_digest"]
        ),
        "mapping_id": mapping_id,
        "source_id": source["source_id"],
        "source_content_digest": source["content_digest"],
        "exact_claim_digest": exact_claim_digest,
        "selected_theory_object_ids": theory_object_ids,
        "matched_terms": matched_terms,
        "match_weight": sum(item["matched_weight"] for item in matches),
        "decision_rule": (
            "per_claim_maximal_term_tie_then_status_and_ordered_claim_signals"
            if matched
            else "per_claim_unmatched_to_scope_anchor_justified_no_change"
        ),
        "event_type": event_type,
        "policy_digest": canonical_digest(_MAPPING_POLICY),
    }
    concept_update = {
        "update_id": stable_identifier(
            "literature-concept-update", mapping_id, concept_disposition
        ),
        "mapping_id": mapping_id,
        "disposition": concept_disposition,
        "generated_object_id": stable_identifier(
            "literature-derived-concept",
            source["content_digest"],
            exact_claim_digest,
            theory_object_ids,
            concept_disposition,
        ),
        "parent_theory_object_ids": theory_object_ids,
        "source_id": source["source_id"],
        "claim_digest": exact_claim_digest,
        "statement": conceptual_change,
    }
    branch_update = {
        "update_id": stable_identifier(
            "literature-branch-update", mapping_id, branch_disposition
        ),
        "mapping_id": mapping_id,
        "disposition": branch_disposition,
        "generated_branch_id": stable_identifier(
            "literature-derived-branch",
            source["content_digest"],
            exact_claim_digest,
            theory_object_ids,
            branch_disposition,
        ),
        "theory_object_ids": theory_object_ids,
        "source_id": source["source_id"],
        "maturation_question": (
            f"What target-preserving consequence follows from the {event_type} "
            f"relation in claim {exact_claim_digest}?"
        ),
    }
    return mapping, receipt, concept_update, branch_update


def _build_claim_mapping_derivation(
    snapshot: Mapping[str, Any], catalog: Mapping[str, Any]
) -> dict[str, Any]:
    """Build the deterministic packet after both input contracts have passed."""

    theory_objects = list(catalog["theory_objects"])
    scope_anchor = next(item for item in theory_objects if item["scope_anchor"])
    theory_mappings: list[dict[str, Any]] = []
    mapping_receipts: list[dict[str, Any]] = []
    concept_updates: list[dict[str, Any]] = []
    branch_updates: list[dict[str, Any]] = []
    for source in sorted(snapshot["sources"], key=lambda item: item["source_id"]):
        distinct_claims: dict[str, str] = {}
        for raw_claim in source["claims"] or ["Source supplied no separately transcribed claim."]:
            exact_claim = " ".join(str(raw_claim).split())
            normalized_identity = exact_claim.casefold()
            incumbent = distinct_claims.get(normalized_identity)
            if incumbent is None or exact_claim < incumbent:
                distinct_claims[normalized_identity] = exact_claim
        for exact_claim in sorted(distinct_claims.values()):
            mapping, receipt, concept_update, branch_update = _derive_one_claim_mapping(
                source=source,
                exact_claim=exact_claim,
                theory_objects=theory_objects,
                scope_anchor=scope_anchor,
                snapshot=snapshot,
                catalog=catalog,
            )
            theory_mappings.append(mapping)
            mapping_receipts.append(receipt)
            concept_updates.append(concept_update)
            branch_updates.append(branch_update)
    packet: dict[str, Any] = {
        "schema_version": "1.0",
        "derivation_id": stable_identifier(
            "claim-mapping-derivation",
            snapshot["content_digest"],
            catalog["content_digest"],
            theory_mappings,
        ),
        "target_id": snapshot["target_id"],
        "theory_state_digest": snapshot["theory_state_digest"],
        "snapshot_id": snapshot["snapshot_id"],
        "snapshot_digest": snapshot["content_digest"],
        "theory_catalog_id": catalog["catalog_id"],
        "theory_catalog_digest": catalog["content_digest"],
        "derivation_authority": {
            "authority_id": CLAIM_MAPPING_AUTHORITY_ID,
            "algorithm_id": CLAIM_MAPPING_ALGORITHM_ID,
            "policy_digest": canonical_digest(_MAPPING_POLICY),
            "authority_class": "deterministic_internal_derivation",
        },
        "theory_mappings": theory_mappings,
        "mapping_receipts": mapping_receipts,
        "concept_updates": concept_updates,
        "branch_updates": branch_updates,
        "explicit_null_effects": [
            {
                "source_id": mapping["source_id"],
                "mapping_id": mapping["mapping_id"],
                "reason": mapping["conceptual_change"],
            }
            for mapping in theory_mappings
            if mapping["event_type"] == "justified_no_change"
        ],
        "epistemic_boundary": (
            "The mapper deterministically records lexical/status relations and "
            "their theory-side consequences. It does not establish source truth, "
            "semantic entailment, novelty, conceptual quality, or efficacy."
        ),
    }
    packet["content_digest"] = canonical_digest(_without(packet, "content_digest"))
    return packet


def derive_claim_mappings(
    snapshot: Mapping[str, Any],
    *,
    theory_catalog: Mapping[str, Any],
    authority_id: str = CLAIM_MAPPING_AUTHORITY_ID,
) -> dict[str, Any]:
    """Derive source-to-theory mappings from content rather than caller copies."""

    validate_snapshot(snapshot)
    validate_theory_object_catalog(theory_catalog)
    if authority_id != CLAIM_MAPPING_AUTHORITY_ID:
        raise ContractError(
            f"unsupported claim-mapping authority {authority_id!r}; "
            f"expected {CLAIM_MAPPING_AUTHORITY_ID!r}"
        )
    if theory_catalog["target_id"] != snapshot["target_id"]:
        raise ContractError("theory catalog target differs from literature snapshot target")
    if theory_catalog["theory_state_digest"] != snapshot["theory_state_digest"]:
        raise ContractError("theory catalog digest binding differs from literature theory state")
    packet = _build_claim_mapping_derivation(snapshot, theory_catalog)
    validate_claim_mapping_derivation(
        packet, snapshot=snapshot, theory_catalog=theory_catalog
    )
    return packet


def validate_claim_mapping_derivation(
    packet: Mapping[str, Any],
    *,
    snapshot: Mapping[str, Any],
    theory_catalog: Mapping[str, Any],
) -> None:
    """Recompute a claim mapping and reject wrong target, digest, or authority."""

    validate_payload(dict(packet), "literature_claim_mapping_derivation.schema.json")
    validate_snapshot(snapshot)
    validate_theory_object_catalog(theory_catalog)
    if packet["content_digest"] != canonical_digest(_without(packet, "content_digest")):
        raise ContractError("claim-mapping derivation content digest mismatch")
    if packet["target_id"] != snapshot["target_id"] or packet["target_id"] != theory_catalog["target_id"]:
        raise ContractError("claim-mapping derivation target mismatch")
    if packet["snapshot_digest"] != snapshot["content_digest"]:
        raise ContractError("claim-mapping derivation snapshot digest mismatch")
    if packet["theory_catalog_digest"] != theory_catalog["content_digest"]:
        raise ContractError("claim-mapping derivation theory catalog digest mismatch")
    authority = packet["derivation_authority"]
    if (
        authority["authority_id"] != CLAIM_MAPPING_AUTHORITY_ID
        or authority["algorithm_id"] != CLAIM_MAPPING_ALGORITHM_ID
        or authority["policy_digest"] != canonical_digest(_MAPPING_POLICY)
    ):
        raise ContractError("claim-mapping derivation authority or policy mismatch")
    expected = _build_claim_mapping_derivation(snapshot, theory_catalog)
    if dict(packet) != expected:
        raise ContractError("claim-mapping derivation does not replay from snapshot contents")


def assimilate_derived_literature(
    snapshot: Mapping[str, Any],
    *,
    theory_catalog: Mapping[str, Any],
    mapping_derivation: Mapping[str, Any],
    hypotheses: Sequence[Mapping[str, Any]] = (),
    prior_snapshot: Mapping[str, Any] | None = None,
    candidate_snapshot_ids: Sequence[str] = (),
) -> dict[str, Any]:
    """Consume only a recomputable mapping derivation at the assimilation boundary."""

    validate_claim_mapping_derivation(
        mapping_derivation, snapshot=snapshot, theory_catalog=theory_catalog
    )
    return assimilate_literature(
        snapshot,
        theory_state_digest=theory_catalog["theory_state_digest"],
        theory_mappings=mapping_derivation["theory_mappings"],
        hypotheses=hypotheses,
        prior_snapshot=prior_snapshot,
        candidate_snapshot_ids=candidate_snapshot_ids,
        mapping_provenance={
            "mode": "deterministic_claim_derivation",
            "derivation_id": mapping_derivation["derivation_id"],
            "derivation_digest": mapping_derivation["content_digest"],
            "authority_id": mapping_derivation["derivation_authority"]["authority_id"],
        },
    )


def derive_hypothesis_rebase(
    mapping_derivation: Mapping[str, Any],
    hypotheses: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Rebuild hypothesis/source relations from one exact mapping derivation."""

    mappings = list(mapping_derivation["theory_mappings"])
    rows: list[dict[str, Any]] = []
    for raw in hypotheses:
        hypothesis_id = str(raw.get("hypothesis_id") or "").strip()
        if not hypothesis_id:
            raise ContractError("derived hypothesis rebase requires hypothesis_id")
        impacts = [
            row
            for row in mappings
            if hypothesis_id in row.get("theory_object_ids", [])
        ]
        event_types = {str(row["event_type"]) for row in impacts}
        if event_types & {"demote", "retire"}:
            relation = "contradicted"
        elif impacts and event_types != {"justified_no_change"}:
            relation = "partly_anticipated"
        elif impacts:
            relation = "apparently_open"
        else:
            relation = "coverage_unknown"
        rows.append(
            {
                "hypothesis_id": hypothesis_id,
                "genealogy": list(raw.get("genealogy") or [hypothesis_id]),
                "literature_relation": relation,
                "source_ids": sorted({str(row["source_id"]) for row in impacts}),
                "required_revision": (
                    "Rebuild this branch from derived mapping receipts "
                    + ", ".join(sorted(str(row["mapping_id"]) for row in impacts))
                    if impacts
                    else "No claim matched this branch; preserve it only as coverage-unknown."
                ),
                "routing_effect": "targeted_reading" if impacts else "incubate",
            }
        )
    return rows


def _replay_snapshot(
    snapshot: Mapping[str, Any], world: Mapping[str, Any]
) -> dict[str, Any]:
    """Create a deterministic, internally valid counterfactual snapshot."""

    operation = str(world.get("operation") or "")
    if operation not in LITERATURE_REPLAY_OPERATIONS:
        raise ContractError(f"unsupported literature replay operation: {operation!r}")
    transformed = copy.deepcopy(dict(snapshot))
    source_id = str(world.get("source_id") or "")
    source_by_id = {item["source_id"]: item for item in transformed["sources"]}
    if operation in {"delete_source", "supersede_source", "contradict_source"}:
        if source_id not in source_by_id:
            raise ContractError(f"replay world cites source outside snapshot: {source_id!r}")
    if operation == "delete_source":
        transformed["sources"] = [
            item for item in transformed["sources"] if item["source_id"] != source_id
        ]
    elif operation == "no_literature":
        transformed["sources"] = []
    elif operation == "supersede_source":
        source = source_by_id[source_id]
        source["correction_status"] = "superseded"
        source["source_version"] = str(
            world.get("source_version") or f"{source['source_version']}.superseded"
        )
        if world.get("replacement_claim"):
            source["claims"] = [str(world["replacement_claim"])]
        source["content_digest"] = canonical_digest(_without(source, "content_digest"))
    elif operation == "contradict_source":
        source = source_by_id[source_id]
        contradictory_claim = str(world.get("contradictory_claim") or "").strip()
        if not contradictory_claim:
            raise ContractError("contradict_source requires contradictory_claim")
        source["claims"] = [contradictory_claim]
        source["correction_status"] = "none_known"
        source["source_version"] = f"{source['source_version']}.contradictory"
        source["content_digest"] = canonical_digest(_without(source, "content_digest"))
    elif operation == "coverage_only_change":
        coverage_limit = str(world.get("coverage_limit") or "").strip()
        if not coverage_limit:
            raise ContractError("coverage_only_change requires coverage_limit")
        transformed["coverage_limits"] = sorted(
            set(transformed["coverage_limits"] + [coverage_limit])
        )

    # Counterfactual source worlds are locally generated protocol probes.  A
    # live baseline receipt cannot lend them live-search authority.
    transformed["provenance_mode"] = "local_only"
    retained_ids = {item["source_id"] for item in transformed["sources"]}
    for receipt in transformed["lane_receipts"]:
        receipt["execution_mode"] = "local_only"
        receipt["source_ids"] = sorted(
            source for source in receipt["source_ids"] if source in retained_ids
        )
        receipt["result_count"] = len(receipt["source_ids"])
        receipt["content_digest"] = canonical_digest(
            _without(receipt, "content_digest", "validator_receipt_ids")
        )
        receipt["validator_receipt_ids"] = [
            stable_identifier(
                "validator", receipt["lane_id"], receipt["content_digest"]
            )
        ]
    transformed["result_count"] = len(transformed["sources"])
    transformed["duplicate_groups"] = []
    transformed["claim_conflicts"] = []
    transformed["snapshot_id"] = stable_identifier(
        "literature-replay-snapshot",
        snapshot["snapshot_id"],
        snapshot["content_digest"],
        world,
    )
    transformed["content_digest"] = canonical_digest(
        _without(
            transformed,
            "content_digest",
            "validator_receipts",
            "validation_status",
        )
    )
    transformed["validator_receipts"] = [
        {
            "receipt_id": stable_identifier(
                "snapshot-validator",
                transformed["snapshot_id"],
                transformed["content_digest"],
            ),
            "validator_id": "target-literature-snapshot-validator.v1",
            "status": "passed",
            "validated_digest": transformed["content_digest"],
            "completed_at": transformed["search_completed_at"],
            "reason_codes": [],
        }
    ]
    transformed["validation_status"] = "validated"
    validate_snapshot(transformed)
    return transformed


def _literature_decision_projection(
    derivation: Mapping[str, Any], assimilation: Mapping[str, Any]
) -> dict[str, Any]:
    """Project only theory decisions, excluding snapshot/provenance churn."""

    return {
        "mappings": [
            {
                key: mapping[key]
                for key in (
                    "source_id",
                    "theory_object_ids",
                    "object_kinds",
                    "relation",
                    "exact_claim",
                    "conceptual_change",
                    "event_type",
                    "confidence",
                )
            }
            for mapping in derivation["theory_mappings"]
        ],
        "concept_updates": [
            _without(item, "update_id") for item in derivation["concept_updates"]
        ],
        "branch_updates": [
            _without(item, "update_id") for item in derivation["branch_updates"]
        ],
        "actions": [
            {
                "action": item["action"],
                "target_object_ids": item["target_object_ids"],
            }
            for item in assimilation["next_theory_actions"]
        ],
    }


def _build_literature_counterfactual_replay(
    snapshot: Mapping[str, Any],
    *,
    theory_catalog: Mapping[str, Any],
    worlds: Sequence[Mapping[str, Any]],
    hypotheses: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build baseline and counterfactual mapping-to-assimilation executions."""

    baseline_derivation = derive_claim_mappings(
        snapshot, theory_catalog=theory_catalog
    )
    baseline_hypotheses = derive_hypothesis_rebase(
        baseline_derivation, hypotheses
    )
    baseline_assimilation = assimilate_derived_literature(
        snapshot,
        theory_catalog=theory_catalog,
        mapping_derivation=baseline_derivation,
        hypotheses=baseline_hypotheses,
    )
    baseline_projection = _literature_decision_projection(
        baseline_derivation, baseline_assimilation
    )
    results: list[dict[str, Any]] = []
    for raw_world in worlds:
        world = copy.deepcopy(dict(raw_world))
        world_id = str(world.get("world_id") or "").strip()
        if not world_id:
            raise ContractError("every replay world requires world_id")
        counterfactual_snapshot = _replay_snapshot(snapshot, world)
        derivation = derive_claim_mappings(
            counterfactual_snapshot, theory_catalog=theory_catalog
        )
        world_hypotheses = derive_hypothesis_rebase(derivation, hypotheses)
        assimilation = assimilate_derived_literature(
            counterfactual_snapshot,
            theory_catalog=theory_catalog,
            mapping_derivation=derivation,
            hypotheses=world_hypotheses,
            prior_snapshot=snapshot,
            candidate_snapshot_ids=[snapshot["snapshot_id"]],
        )
        projection = _literature_decision_projection(derivation, assimilation)
        projection_changed = projection != baseline_projection
        expectation = str(world.get("expected_effect") or "unspecified")
        if expectation not in {"change", "null", "unspecified"}:
            raise ContractError("expected_effect must be change, null, or unspecified")
        result = {
            "world_id": world_id,
            "world_spec": world,
            "world_spec_digest": canonical_digest(world),
            "snapshot": counterfactual_snapshot,
            "mapping_derivation": derivation,
            "assimilation": assimilation,
            "decision_projection_digest": canonical_digest(projection),
            "effects": {
                "snapshot_digest_changed": counterfactual_snapshot["content_digest"]
                != snapshot["content_digest"],
                "mapping_packet_digest_changed": derivation["content_digest"]
                != baseline_derivation["content_digest"],
                "assimilation_packet_digest_changed": assimilation["content_digest"]
                != baseline_assimilation["content_digest"],
                "mapping_or_theory_decision_changed": projection_changed,
                "concept_updates_changed": derivation["concept_updates"]
                != baseline_derivation["concept_updates"],
                "branch_updates_changed": derivation["branch_updates"]
                != baseline_derivation["branch_updates"],
                "null_effect": not projection_changed,
                "expected_effect": expectation,
                "expectation_met": expectation == "unspecified"
                or (expectation == "change" and projection_changed)
                or (expectation == "null" and not projection_changed),
            },
        }
        result["content_digest"] = canonical_digest(_without(result, "content_digest"))
        results.append(result)
    if len({item["world_id"] for item in results}) != len(results):
        raise ContractError("literature replay world identifiers must be unique")
    replay: dict[str, Any] = {
        "schema_version": "1.0",
        "replay_id": stable_identifier(
            "literature-counterfactual-replay",
            snapshot["content_digest"],
            theory_catalog["content_digest"],
            [item["world_spec_digest"] for item in results],
        ),
        "target_id": snapshot["target_id"],
        "theory_state_digest": snapshot["theory_state_digest"],
        "baseline_snapshot_id": snapshot["snapshot_id"],
        "baseline_snapshot_digest": snapshot["content_digest"],
        "theory_catalog_id": theory_catalog["catalog_id"],
        "theory_catalog_digest": theory_catalog["content_digest"],
        "baseline": {
            "mapping_derivation": baseline_derivation,
            "assimilation": baseline_assimilation,
            "decision_projection_digest": canonical_digest(baseline_projection),
        },
        "world_results": results,
        "null_effect_world_ids": [
            item["world_id"] for item in results if item["effects"]["null_effect"]
        ],
        "claim_boundary": (
            "Replay demonstrates deterministic sensitivity or insensitivity of "
            "this mapping policy on supplied worlds. It is not evidence that the "
            "derived concepts are true, novel, deep, or discovery-effective."
        ),
    }
    replay["content_digest"] = canonical_digest(_without(replay, "content_digest"))
    return replay


def replay_literature_counterfactuals(
    snapshot: Mapping[str, Any],
    *,
    theory_catalog: Mapping[str, Any],
    worlds: Sequence[Mapping[str, Any]],
    hypotheses: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Rebuild snapshot -> mapping -> assimilation for every declared world."""

    validate_snapshot(snapshot)
    validate_theory_object_catalog(theory_catalog)
    if len(worlds) < 1:
        raise ContractError("literature counterfactual replay requires at least one world")
    replay = _build_literature_counterfactual_replay(
        snapshot,
        theory_catalog=theory_catalog,
        worlds=worlds,
        hypotheses=hypotheses,
    )
    validate_literature_counterfactual_replay(
        replay,
        snapshot=snapshot,
        theory_catalog=theory_catalog,
        hypotheses=hypotheses,
    )
    return replay


def validate_literature_counterfactual_replay(
    replay: Mapping[str, Any],
    *,
    snapshot: Mapping[str, Any],
    theory_catalog: Mapping[str, Any],
    hypotheses: Sequence[Mapping[str, Any]] = (),
) -> None:
    """Replay every world again and reject retained/manual mapping substitutions."""

    validate_payload(dict(replay), "literature_counterfactual_replay.schema.json")
    validate_snapshot(snapshot)
    validate_theory_object_catalog(theory_catalog)
    if replay["content_digest"] != canonical_digest(_without(replay, "content_digest")):
        raise ContractError("literature counterfactual replay content digest mismatch")
    if replay["target_id"] != snapshot["target_id"] or replay["target_id"] != theory_catalog["target_id"]:
        raise ContractError("literature counterfactual replay target mismatch")
    if replay["baseline_snapshot_digest"] != snapshot["content_digest"]:
        raise ContractError("literature counterfactual baseline digest mismatch")
    if replay["theory_catalog_digest"] != theory_catalog["content_digest"]:
        raise ContractError("literature counterfactual theory catalog digest mismatch")
    expected = _build_literature_counterfactual_replay(
        snapshot,
        theory_catalog=theory_catalog,
        worlds=[item["world_spec"] for item in replay["world_results"]],
        hypotheses=hypotheses,
    )
    if dict(replay) != expected:
        raise ContractError(
            "literature counterfactual replay does not rebuild from snapshot contents"
        )


def assimilate_literature(
    snapshot: Mapping[str, Any],
    *,
    theory_state_digest: str,
    theory_mappings: Sequence[Mapping[str, Any]],
    hypotheses: Sequence[Mapping[str, Any]] = (),
    prior_snapshot: Mapping[str, Any] | None = None,
    candidate_snapshot_ids: Sequence[str] = (),
    mapping_provenance: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Turn source claims into theory events while naming mapping authority.

    ``theory_mappings`` remains as a compatibility surface for existing
    interpretive callers.  Such packets are explicitly labeled
    ``operator_supplied_interpretive_mapping``.  New runtime integrations should
    call :func:`assimilate_derived_literature`, which validates and binds a
    deterministic derivation receipt before reaching this reducer.
    """

    validate_snapshot(snapshot)
    if snapshot["theory_state_digest"] != theory_state_digest:
        raise ContractError("snapshot is bound to a different theory-state digest")
    sources = {item["source_id"]: item for item in snapshot["sources"]}
    normalized_mappings: list[dict[str, Any]] = []
    mapped_sources: set[str] = set()
    for raw in theory_mappings:
        mapping = copy.deepcopy(dict(raw))
        source_id = str(mapping.get("source_id") or "")
        if source_id not in sources:
            raise ContractError(f"mapping cites source outside snapshot: {source_id!r}")
        event_type = str(mapping.get("event_type") or "")
        if event_type not in MAPPING_EVENTS:
            raise ContractError(f"mapping {source_id!r} needs an allowed causal event type")
        theory_ids = sorted({str(item) for item in mapping.get("theory_object_ids", []) if str(item)})
        object_kinds = sorted({str(item) for item in mapping.get("object_kinds", []) if str(item)})
        if not theory_ids or not object_kinds:
            raise ContractError(f"mapping {source_id!r} must name exact theory objects and kinds")
        conceptual_change = str(mapping.get("conceptual_change") or "").strip()
        if not conceptual_change:
            raise ContractError(f"mapping {source_id!r} lacks a conceptual change or justified no-change rationale")
        coverage = [str(item).strip() for item in mapping.get("coverage_limits", snapshot["coverage_limits"]) if str(item).strip()]
        if not coverage:
            raise ContractError(f"mapping {source_id!r} lacks coverage limits")
        normalized = {
            "mapping_id": str(mapping.get("mapping_id") or stable_identifier("source-theory-map", snapshot["content_digest"], source_id, theory_ids, event_type)),
            "source_id": source_id,
            "theory_object_ids": theory_ids,
            "object_kinds": object_kinds,
            "relation": str(mapping.get("relation") or "leaves_open"),
            "exact_claim": str(mapping.get("exact_claim") or (sources[source_id]["claims"] or ["Source claim was not separately transcribed."])[0]),
            "source_limitation": str(mapping.get("source_limitation") or sources[source_id]["limitations"][0]),
            "conceptual_change": conceptual_change,
            "event_type": event_type,
            "coverage_limits": coverage,
            "confidence": str(mapping.get("confidence") or "medium"),
        }
        normalized_mappings.append(normalized)
        mapped_sources.add(source_id)
    missing = sorted(
        source_id for source_id, source in sources.items()
        if source["decision_relevant"] and source_id not in mapped_sources
    )
    if missing:
        raise ContractError(f"decision-relevant sources lack claim-level mappings: {', '.join(missing)}")

    rebase: list[dict[str, Any]] = []
    for raw in hypotheses:
        hypothesis = copy.deepcopy(dict(raw))
        hypothesis_id = str(hypothesis.get("hypothesis_id") or "")
        if not hypothesis_id:
            raise ContractError("every hypothesis rebase needs a hypothesis_id")
        relation = str(hypothesis.get("literature_relation") or "coverage_unknown")
        if relation not in HYPOTHESIS_RELATIONS:
            raise ContractError(f"unsupported literature relation {relation!r}")
        source_ids = sorted({str(item) for item in hypothesis.get("source_ids", [])})
        if not set(source_ids).issubset(sources):
            raise ContractError(f"hypothesis {hypothesis_id} cites a source outside the frozen snapshot")
        rebase.append(
            {
                "hypothesis_id": hypothesis_id,
                "pre_search_genealogy": list(hypothesis.get("genealogy") or [hypothesis_id]),
                "literature_relation": relation,
                "source_ids": source_ids,
                "required_revision": str(hypothesis.get("required_revision") or "none; preserve the articulated pre-search mechanism"),
                "routing_effect": str(hypothesis.get("routing_effect") or ("targeted_reading" if relation == "coverage_unknown" else "continue")),
                "rebased_snapshot_digest": snapshot["content_digest"],
            }
        )
    freshness = "current" if snapshot["provenance_mode"] == "live" else "local_only"
    rebase_status = "current" if freshness == "current" else "provisional_local_only"
    provenance = copy.deepcopy(
        dict(
            mapping_provenance
            or {
                "mode": "operator_supplied_interpretive_mapping",
                "derivation_id": None,
                "derivation_digest": None,
                "authority_id": "operator.unverified-interpretive-mapping",
            }
        )
    )
    if provenance.get("mode") not in {
        "operator_supplied_interpretive_mapping",
        "deterministic_claim_derivation",
    }:
        raise ContractError("unsupported literature mapping provenance mode")
    if provenance["mode"] == "deterministic_claim_derivation":
        if not provenance.get("derivation_id") or not provenance.get("derivation_digest"):
            raise ContractError("derived literature assimilation requires a derivation receipt")
        if provenance.get("authority_id") != CLAIM_MAPPING_AUTHORITY_ID:
            raise ContractError("derived literature assimilation authority mismatch")
    else:
        provenance["derivation_id"] = None
        provenance["derivation_digest"] = None
        provenance["authority_id"] = str(
            provenance.get("authority_id") or "operator.unverified-interpretive-mapping"
        )
    ledger_events = [
        {
            "event_id": stable_identifier("literature-event", mapping["mapping_id"], mapping["event_type"]),
            "event_type": f"literature_{mapping['event_type']}",
            "source_mapping_ids": [mapping["mapping_id"]],
            "affected_object_ids": mapping["theory_object_ids"],
            "payload": {
                "relation": mapping["relation"],
                "conceptual_change": mapping["conceptual_change"],
                "snapshot_digest": snapshot["content_digest"],
            },
        }
        for mapping in normalized_mappings
    ]
    actions = [
        {
            "action_id": stable_identifier("literature-action", mapping["mapping_id"]),
            "action": (
                "record justified no-change and preserve current priority"
                if mapping["event_type"] == "justified_no_change"
                else f"apply {mapping['event_type']} before branch selection or further investment"
            ),
            "source_mapping_ids": [mapping["mapping_id"]],
            "target_object_ids": mapping["theory_object_ids"],
        }
        for mapping in normalized_mappings
    ]
    packet: dict[str, Any] = {
        "schema_version": "2.0",
        "packet_id": stable_identifier("literature-assimilation", snapshot["snapshot_id"], theory_state_digest, normalized_mappings, rebase),
        "target_id": snapshot["target_id"],
        "theory_state_digest": theory_state_digest,
        "prior_snapshot_id": prior_snapshot.get("snapshot_id") if prior_snapshot else None,
        "selected_snapshot": {
            "snapshot_id": snapshot["snapshot_id"],
            "content_digest": snapshot["content_digest"],
            "search_completed_at": snapshot["search_completed_at"],
            "coverage_cutoff": snapshot["coverage_cutoff"],
            "provenance_mode": snapshot["provenance_mode"],
            "coverage_limits": list(snapshot["coverage_limits"]),
            "validator_receipt_ids": [item["receipt_id"] for item in snapshot["validator_receipts"] if item["status"] == "passed"],
        },
        "resolution": {
            "freshness_status": freshness,
            "candidate_snapshot_ids": sorted(set(candidate_snapshot_ids) | {snapshot["snapshot_id"]}),
            "selection_reason": "Newest matching validated search-completion metadata and digest; file mtime and global aliases were ignored.",
            "target_match": "pass",
            "active_investment_gate": "pass" if freshness == "current" else "blocked_local_only",
        },
        "source_delta": _source_delta(snapshot, prior_snapshot),
        "mapping_provenance": provenance,
        "theory_mappings": normalized_mappings,
        "hypothesis_rebase_status": rebase_status,
        "hypothesis_rebase": rebase,
        "opportunity_frontier": {
            "neglected_conceptual_corners": [mapping["conceptual_change"] for mapping in normalized_mappings if mapping["event_type"] == "spawn"],
            "cross_field_connections": [mapping["conceptual_change"] for mapping in normalized_mappings if mapping["relation"] == "transfers"],
            "unresolved_source_tensions": [mapping["conceptual_change"] for mapping in normalized_mappings if mapping["relation"] in {"contradicts", "leaves_open"}],
            "newly_available_mechanisms": [mapping["conceptual_change"] for mapping in normalized_mappings if "mechanism" in mapping["object_kinds"] and mapping["event_type"] != "justified_no_change"],
        },
        "ledger_events": ledger_events,
        "stale_branch_ids": [item["hypothesis_id"] for item in rebase if item["literature_relation"] in {"absorbed", "contradicted", "coverage_unknown"}],
        "explicit_unknowns": list(snapshot["coverage_limits"]),
        "next_theory_actions": actions,
    }
    packet["content_digest"] = canonical_digest(_without(packet, "content_digest"))
    validate_assimilation(packet, snapshot=snapshot)
    return packet


def validate_assimilation(packet: Mapping[str, Any], *, snapshot: Mapping[str, Any] | None = None) -> None:
    """Reject non-causal bibliographies, wrong-target packets, and novelty laundering."""

    validate_payload(dict(packet), "literature_assimilation_packet.schema.json")
    if packet["content_digest"] != canonical_digest(_without(packet, "content_digest")):
        raise ContractError("literature assimilation content digest mismatch")
    if packet["schema_version"] == "1.0":
        if "mapping_provenance" in packet:
            raise ContractError("legacy v1 assimilation packets cannot be retrofitted with provenance")
    else:
        provenance = packet["mapping_provenance"]
        if provenance["mode"] == "deterministic_claim_derivation":
            if (
                not provenance["derivation_id"]
                or not provenance["derivation_digest"]
                or provenance["authority_id"] != CLAIM_MAPPING_AUTHORITY_ID
            ):
                raise ContractError("derived assimilation lacks an exact mapping receipt")
        elif provenance["derivation_id"] is not None or provenance["derivation_digest"] is not None:
            raise ContractError("manual interpretive mappings cannot cite a derived receipt")
    if snapshot is not None:
        validate_snapshot(snapshot)
        if packet["target_id"] != snapshot["target_id"]:
            raise ContractError("assimilation target differs from selected snapshot target")
        if packet["selected_snapshot"]["content_digest"] != snapshot["content_digest"]:
            raise ContractError("assimilation selected digest differs from frozen snapshot")
        required = {item["source_id"] for item in snapshot["sources"] if item["decision_relevant"]}
        mapped = {item["source_id"] for item in packet["theory_mappings"]}
        if not required.issubset(mapped):
            raise ContractError("branch selection cannot consume a snapshot with unmapped decision-relevant sources")
    mapping_ids = {item["mapping_id"] for item in packet["theory_mappings"]}
    for action in packet["next_theory_actions"]:
        if not set(action["source_mapping_ids"]).issubset(mapping_ids):
            raise ContractError("a scheduling action lacks a source-to-theory mapping")
    if packet["selected_snapshot"]["provenance_mode"] == "local_only":
        if packet["hypothesis_rebase_status"] != "provisional_local_only":
            raise ContractError("local-only evidence cannot satisfy a completed hypothesis rebase")
        if packet["resolution"]["active_investment_gate"] != "blocked_local_only":
            raise ContractError("local-only evidence must block active investment and novelty claims")


def rebase_surviving_branches(
    branches: Sequence[Mapping[str, Any]],
    *,
    old_snapshot_digest: str,
    new_snapshot: Mapping[str, Any],
    relations: Mapping[str, Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Rebase every survivor while preserving its complete pre-search genealogy."""

    validate_snapshot(new_snapshot)
    relations = dict(relations or {})
    rebased: list[dict[str, Any]] = []
    for raw in branches:
        branch = copy.deepcopy(dict(raw))
        branch_id = str(branch.get("branch_id") or branch.get("hypothesis_id") or "")
        if not branch_id:
            raise ContractError("every surviving branch needs a stable branch_id")
        if branch.get("literature_snapshot_digest") not in {None, old_snapshot_digest}:
            raise ContractError(f"branch {branch_id} did not originate from the declared frozen snapshot")
        relation = dict(relations.get(branch_id, {}))
        genealogy = list(branch.get("genealogy") or [branch_id])
        branch["pre_search_genealogy"] = genealogy
        branch["literature_snapshot_digest"] = new_snapshot["content_digest"]
        branch["literature_snapshot_id"] = new_snapshot["snapshot_id"]
        branch["literature_relation"] = str(relation.get("literature_relation") or "coverage_unknown")
        branch["literature_source_ids"] = list(relation.get("source_ids") or [])
        branch["literature_status"] = "rebased"
        branch["rebase_receipt"] = {
            "receipt_id": stable_identifier("branch-rebase", branch_id, old_snapshot_digest, new_snapshot["content_digest"]),
            "branch_id": branch_id,
            "from_digest": old_snapshot_digest,
            "to_digest": new_snapshot["content_digest"],
            "preserved_genealogy": genealogy,
            "completed_at": utc_now(),
        }
        rebased.append(branch)
    return rebased


def build_demo_literature_snapshot(
    *,
    target_id: str = "demo-target",
    theory_state_digest: str | None = None,
) -> dict[str, Any]:
    """Build a bounded local snapshot for CLI self-checks and documentation.

    The helper intentionally returns local-only provenance. It is useful for
    validating contracts without network access but cannot satisfy an
    active-investment or novelty gate.
    """

    theory_digest = theory_state_digest or canonical_digest(
        {"target_id": target_id, "state_version": 0}
    )
    lanes = []
    for index, lane_type in enumerate(LANE_TYPES):
        lanes.append(
            {
                "lane_type": lane_type,
                "queries": [f"{target_id} {lane_type.replace('_', ' ')}"],
                "provider": "bounded-demo-corpus",
                "index": f"demo-{lane_type}",
                "coverage_cutoff": "explicitly unknown",
                "inclusion_policy": "Include the one target-scoped demonstration source.",
                "exclusion_policy": "Exclude all claims outside this contract self-check.",
                "sources": [
                    {
                        "work_identity": f"demo-work-{index}",
                        "title": f"Demonstration source for {lane_type}",
                        "authors": ["Abducer contract fixture"],
                        "publication_date": str(1990 + index),
                        "source_version": "fixture-v1",
                        "source_type": "primary",
                        "url": f"https://example.invalid/{target_id}/{lane_type}",
                        "correction_status": "none_known",
                        "decision_relevant": True,
                        "claims": [
                            f"Bounded fixture claim for the {lane_type} lane."
                        ],
                        "limitations": [
                            "This is immutable local test data, not a live literature search."
                        ],
                    }
                ],
            }
        )
    return run_frontier_literature_cycle(
        {
            "target_id": target_id,
            "claim_scope": "contract self-check only",
            "theory_state_digest": theory_digest,
            "coverage_cutoff": "explicitly unknown",
            "coverage_limits": [
                "Demonstration sources exercise contracts but provide no real literature coverage."
            ],
            "search_lanes": lanes,
        }
    )


__all__ = [
    "CLAIM_MAPPING_ALGORITHM_ID",
    "CLAIM_MAPPING_AUTHORITY_ID",
    "LANE_TYPES",
    "LITERATURE_REPLAY_OPERATIONS",
    "assimilate_literature",
    "assimilate_derived_literature",
    "build_theory_object_catalog",
    "build_demo_literature_snapshot",
    "derive_claim_mappings",
    "rebase_surviving_branches",
    "replay_literature_counterfactuals",
    "run_frontier_literature_cycle",
    "select_newest_snapshot",
    "validate_assimilation",
    "validate_claim_mapping_derivation",
    "validate_literature_counterfactual_replay",
    "validate_snapshot",
    "validate_theory_object_catalog",
]
