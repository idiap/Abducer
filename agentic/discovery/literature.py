# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Target-scoped frontier literature search and causal theory assimilation.

The module keeps three notions deliberately separate: when a search actually
completed, when a work was published, and when a file happened to be written.
Only receipt-backed lane completion establishes search freshness.  Replaying
frozen response bytes is a separate, non-renewing mode: it retains the exact
original live-acquisition snapshot, lane receipts, and timestamps, and requires
an injected clock before it can support present use.  A frozen snapshot then
becomes useful only through claim-level mappings that name the
concepts, mechanisms, barriers, hypotheses, or actions it changes.  Before
mapping, every exact source claim is lifted into a version- and
correction-bound semantic record.  Explicit source-level warrants take
precedence; a deterministic lexical classifier remains a visibly bounded
fallback and never acquires truth, entailment, novelty, or coverage authority.

Provider integrations are dependency-injected callables.  This lets production
adapters perform live searches while tests use immutable fixture providers; an
inline/local corpus is always classified ``local_only`` and can never launder a
generated bibliography into a recent search.
"""

from __future__ import annotations

import copy
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
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

CLAIM_MAPPING_AUTHORITY_ID = "deterministic-claim-mapper.v3"
CLAIM_MAPPING_ALGORITHM_ID = "semantic-origin-and-uncertainty-rules.v3"
SEMANTIC_CLAIM_AUTHORITY_ID = "source-semantic-claim-layer.v2"
SEMANTIC_CLAIM_ALGORITHM_ID = "typed-origin-warrant-then-conservative-lexical.v2"
SEMANTIC_CONTRACT_VERSION = "typed-claim-origin-and-authority.v1"
SEMANTIC_RELATIONS = {"entails", "contradicts", "leaves_open", "unresolved"}
CLAIM_ORIGINS = {"verbatim_source_excerpt", "author_paraphrase", "model_extraction", "internal_target_audit"}
CLAIM_AUTHORITY_CLASSES = {
    "locator_bound_source_excerpt", "author_supplied_paraphrase",
    "receipt_bound_model_extraction", "unverified_provider_claim_extraction",
    "internal_target_claim_audit", "missing_claim_null",
}
SEMANTIC_WARRANT_AUTHORITY_CLASSES = {
    "source_bound_semantic_annotation", "author_paraphrase_interpretation",
    "model_extraction_interpretation", "internal_target_semantic_audit",
    "deterministic_internal_lexical_fallback",
}
SNAPSHOT_VALIDATOR_RECEIPT_DERIVATIONS = {
    "target-literature-snapshot-validator.v1": "snapshot-validator",
    "source-semantic-snapshot-validator.v1": "semantic-snapshot-validator",
    "target-literature-frozen-replay-validator.v1": "frozen-replay-snapshot-validator",
}
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
LITERATURE_FRESHNESS_POLICY = "search_completion_bounded_consumption_v1"
DEFAULT_LITERATURE_FRESHNESS_SECONDS = 30 * 24 * 60 * 60
LITERATURE_RESOLUTION_AUTHORITY_SCOPE = (
    "historical_assimilation_only; present use must recompute against consume_before"
)
_TEMPORAL_RESOLUTION_FIELDS = {
    "freshness_policy",
    "evaluated_at",
    "max_age_seconds",
    "consume_before",
    "authority_scope",
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
    "semantic_relation_precedence": (
        "exact source/version/correction-bound warrant, then bounded lexical fallback"
    ),
    "semantic_authority_boundary": (
        "relations route internal theory updates but do not establish semantic entailment, "
        "source truth, novelty, exhaustiveness, or external validation"
    ),
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
_LEXICAL_UNCERTAINTY_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("negation_or_failed_establishment", re.compile(
        r"\b(?:does|do|did|is|are|was|were|has|have|had|can|could|would|should|may|might|must)\s+not\b|"
        r"\bno\s+(?:evidence|proof|support)\b|\b(?:fails?|failed|failure)\s+to\s+"
        r"(?:establish|confirm|prove|show|support|construct|rule\s+out)\b|\bwithout\s+"
        r"(?:establishing|confirming|proving|showing|supporting|constructing|ruling\s+out)\b", re.I)),
    ("modality_or_hedging", re.compile(
        r"\b(?:may|might|could|perhaps|possibly|plausibly|suggests?|appears?|seems?|conjectures?|hypothesi[sz]es?|speculates?)\b", re.I)),
    ("quotation_without_adoption", re.compile(r"[\"'“”‘’]|\b(?:quotes?|quoted|quotation)\b", re.I)),
    ("attributed_claim_without_adoption", re.compile(
        r"\baccording\s+to\b|\b(?:authors?|paper|article|review|report)\s+"
        r"(?:claims?|argues?|states?|reports?|suggests?|attributes?)\b|"
        r"\b(?:claims?|arguments?|statements?)\s+(?:by|from)\b", re.I)),
    ("explicit_paraphrase", re.compile(r"\bparaphras(?:e|ed|es|ing)\b", re.I)),
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


def _bounded_freshness_fields(
    snapshot: Mapping[str, Any], max_age_seconds: int | None,
    evaluated_at: str | datetime | None,
) -> dict[str, Any]:
    """Freeze a replayable consumption deadline without asserting present freshness.

    The immutable assimilation packet records the window that applied to its
    historical decision.  Consumers must call
    :func:`resolve_present_literature_freshness` with their own clock before a
    new investment; replaying the packet never rewrites that historical state.
    ``None`` is reserved for validating pre-policy historical packets.
    """

    if max_age_seconds is None:
        if evaluated_at is not None:
            raise ContractError(
                "literature freshness evaluation time requires a max-age policy"
            )
        return {}
    if (
        isinstance(max_age_seconds, bool)
        or not isinstance(max_age_seconds, int)
        or not 0 < max_age_seconds <= DEFAULT_LITERATURE_FRESHNESS_SECONDS
    ):
        raise ContractError(
            "literature freshness max age must be a positive integer no greater "
            "than the thirty-day policy ceiling"
        )
    if evaluated_at is None:
        raise ContractError(
            "bounded literature freshness requires an explicit evaluation time"
        )
    completed = _timestamp(str(snapshot["search_completed_at"]))
    evaluated = (
        evaluated_at.astimezone(timezone.utc)
        if isinstance(evaluated_at, datetime) and evaluated_at.tzinfo is not None
        else _timestamp(str(evaluated_at))
    )
    if isinstance(evaluated_at, datetime) and evaluated_at.tzinfo is None:
        raise ContractError("literature freshness evaluation time must be timezone-aware")
    consume_before = completed + timedelta(seconds=max_age_seconds)
    return {
        "freshness_policy": LITERATURE_FRESHNESS_POLICY,
        "evaluated_at": evaluated.isoformat().replace("+00:00", "Z"),
        "max_age_seconds": max_age_seconds,
        "consume_before": consume_before.isoformat().replace("+00:00", "Z"),
        "authority_scope": LITERATURE_RESOLUTION_AUTHORITY_SCOPE,
    }


def _normalize_freshness_evaluation(
    evaluated_at: str | datetime | None, max_age_seconds: int | None,
    *, snapshot: Mapping[str, Any] | None = None,
) -> str | None:
    """Resolve one clock instant without letting frozen replay renew recency."""

    if max_age_seconds is None:
        if evaluated_at is not None:
            raise ContractError(
                "literature freshness evaluation time requires a max-age policy"
            )
        if snapshot is not None and snapshot.get("provenance_mode") == "frozen_response_replay":
            raise ContractError(
                "frozen-response replay requires bounded freshness authority"
            )
        return None
    if (
        evaluated_at is None
        and snapshot is not None
        and snapshot.get("provenance_mode") == "frozen_response_replay"
    ):
        raise ContractError(
            "frozen-response replay requires an injected freshness evaluation time"
        )
    raw = utc_now() if evaluated_at is None else evaluated_at
    if isinstance(raw, datetime):
        if raw.tzinfo is None:
            raise ContractError(
                "literature freshness evaluation time must be timezone-aware"
            )
        parsed = raw.astimezone(timezone.utc)
    else:
        parsed = _timestamp(str(raw))
    return parsed.isoformat().replace("+00:00", "Z")


def _freshness_status_at(
    selected_snapshot: Mapping[str, Any], resolution: Mapping[str, Any],
    instant: datetime,
) -> tuple[str, str, str]:
    """Classify one instant against a validated immutable freshness window."""

    if selected_snapshot["provenance_mode"] not in {
        "live", "frozen_response_replay",
    }:
        return "local_only", "blocked_local_only", "snapshot_not_live"
    completed = _timestamp(str(selected_snapshot["search_completed_at"]))
    if instant < completed:
        return "refresh_required", "blocked_invalid", "clock_precedes_search_completion"
    if instant <= _timestamp(str(resolution["consume_before"])):
        return "current", "pass", "inside_bounded_consumption_window"
    return "refresh_required", "blocked_stale", "consume_before_expired"


def _validate_temporal_resolution(packet: Mapping[str, Any]) -> bool:
    """Validate a bounded historical window; return false for legacy packets."""

    resolution = packet["resolution"]
    present = _TEMPORAL_RESOLUTION_FIELDS.intersection(resolution)
    if not present:
        return False
    if present != _TEMPORAL_RESOLUTION_FIELDS:
        missing = sorted(_TEMPORAL_RESOLUTION_FIELDS - present)
        raise ContractError(
            "literature temporal authority is incomplete: " + ", ".join(missing)
        )
    if resolution["freshness_policy"] != LITERATURE_FRESHNESS_POLICY:
        raise ContractError("literature freshness policy is unsupported")
    if resolution["authority_scope"] != LITERATURE_RESOLUTION_AUTHORITY_SCOPE:
        raise ContractError("literature resolution authority scope is unsupported")
    expected = _bounded_freshness_fields(
        {"search_completed_at": packet["selected_snapshot"]["search_completed_at"]},
        resolution["max_age_seconds"],
        resolution["evaluated_at"],
    )
    if any(resolution[key] != expected[key] for key in _TEMPORAL_RESOLUTION_FIELDS):
        raise ContractError(
            "literature consume-before deadline does not replay from search completion"
        )
    expected_freshness, expected_gate, _reason = _freshness_status_at(
        packet["selected_snapshot"], resolution,
        _timestamp(str(resolution["evaluated_at"])),
    )
    if (
        resolution["freshness_status"] != expected_freshness
        or resolution["active_investment_gate"] != expected_gate
    ):
        raise ContractError(
            "historical literature gate does not match its recorded evaluation time"
        )
    return True


def resolve_present_literature_freshness(
    packet: Mapping[str, Any], *, now: datetime | None = None
) -> dict[str, Any]:
    """Recompute whether an immutable assimilation may support a new investment.

    This is deliberately a projection, not a mutation.  Old packets remain
    valid historical evidence, while missing temporal authority, clock skew,
    local-only provenance, and expired windows all fail closed for present use.
    """

    validate_assimilation(packet)
    if (
        packet["selected_snapshot"]["provenance_mode"]
        == "frozen_response_replay"
        and now is None
    ):
        raise ContractError(
            "frozen-response present use requires an injected trusted clock"
        )
    instant = now or datetime.now(timezone.utc)
    if instant.tzinfo is None:
        raise ContractError("literature freshness clock must be timezone-aware")
    normalized = instant.astimezone(timezone.utc)
    evaluated_at = normalized.isoformat().replace("+00:00", "Z")
    resolution = packet["resolution"]
    if not _TEMPORAL_RESOLUTION_FIELDS.issubset(resolution):
        return {
            "evaluated_at": evaluated_at,
            "freshness_status": "refresh_required",
            "active_investment_gate": "blocked_invalid",
            "reason": "temporal_authority_unavailable",
        }
    freshness, gate, reason = _freshness_status_at(
        packet["selected_snapshot"], resolution, normalized
    )
    return {
        "evaluated_at": evaluated_at,
        "freshness_status": freshness,
        "active_investment_gate": gate,
        "reason": reason,
    }


def _source_identity(source: Mapping[str, Any]) -> str:
    """Resolve explicit lineage first so disputed identifiers remain conflicts."""

    explicit = str(source.get("work_identity") or "").strip().lower()
    if explicit:
        return explicit

    doi = str(source.get("doi") or "").strip().lower()
    if doi:
        return f"doi:{doi.removeprefix('https://doi.org/')}"
    arxiv = str(source.get("arxiv_id") or "").strip().lower()
    if arxiv:
        return f"arxiv:{arxiv.removeprefix('arxiv:')}"
    title = " ".join(str(source.get("title") or "").lower().split())
    authors = ",".join(sorted(str(item).strip().lower() for item in source.get("authors", [])))
    if not title or not authors:
        raise ContractError("a source needs DOI, arXiv ID, work_identity, or title plus authors")
    return f"title-author:{canonical_digest([title, authors]).split(':', 1)[-1][:24]}"


def _exact_claim_text(value: Any) -> str:
    """Normalize whitespace while preserving the source's lexical content."""

    if value is None:
        return ""
    return " ".join(str(value).split())


def expected_snapshot_validator_receipt_id(
    snapshot: Mapping[str, Any], validator_id: str
) -> str:
    """Reconstruct one registered snapshot-validator receipt identity.

    Validator classes are closed because their receipt namespaces differ.  A
    semantic annotation pass is not interchangeable with the search-snapshot
    validator even when both bind the same final content digest.
    """

    prefix = SNAPSHOT_VALIDATOR_RECEIPT_DERIVATIONS.get(str(validator_id))
    if prefix is None:
        raise ContractError(f"unregistered snapshot validator: {validator_id!r}")
    return stable_identifier(
        prefix,
        snapshot.get("snapshot_id"),
        snapshot.get("content_digest"),
    )


def _normalize_claim_provenance(
    raw_records: Sequence[Mapping[str, Any]], *, source_id: str,
    source_version: str, correction_status: str, claims: Sequence[str],
) -> list[dict[str, Any]]:
    """Type every claim origin without inventing source or external authority."""

    by_claim = {item.casefold(): item for item in claims}
    supplied: dict[str, Mapping[str, Any]] = {}
    for raw in raw_records:
        exact_claim = _exact_claim_text(raw.get("exact_claim"))
        if exact_claim.casefold() not in by_claim:
            raise ContractError("claim provenance does not bind an exact source claim")
        key = exact_claim.casefold()
        if key in supplied:
            raise ContractError("a source claim has duplicate provenance records")
        supplied[key] = raw
    records: list[dict[str, Any]] = []
    for claim_index, exact_claim in enumerate(claims):
        raw = supplied.get(exact_claim.casefold(), {})
        claim_origin = str(raw.get("claim_origin") or "model_extraction").strip()
        if claim_origin not in CLAIM_ORIGINS:
            raise ContractError(f"unsupported claim origin: {claim_origin!r}")
        locator = _exact_claim_text(raw.get("evidence_locator"))
        extractor_receipt_id = str(raw.get("extractor_receipt_id") or "").strip() or None
        authority_id = str(raw.get("authority_id") or "").strip()
        if claim_origin == "verbatim_source_excerpt":
            if not locator:
                raise ContractError("verbatim source excerpts require an exact evidence locator")
            authority_class, authority_id = "locator_bound_source_excerpt", authority_id or "source-excerpt-locator.unverified"
        elif claim_origin == "author_paraphrase":
            if not locator:
                raise ContractError("author paraphrases require an exact evidence locator")
            authority_class, authority_id = "author_supplied_paraphrase", authority_id or "author-paraphrase.unverified"
        elif claim_origin == "internal_target_audit":
            authority_class, authority_id = "internal_target_claim_audit", authority_id or "internal-target-claim-audit.v1"
            locator = locator or "internal target audit; no source excerpt claimed"
        elif extractor_receipt_id:
            authority_class, authority_id = "receipt_bound_model_extraction", authority_id or "model-claim-extractor.receipt-bound"
            locator = locator or "extractor receipt binds the provider claim field"
        else:
            authority_class, authority_id = "unverified_provider_claim_extraction", authority_id or "provider-claim-extraction.unverified"
            locator = locator or "provider claim field; exact source locator unavailable"
        if str(raw.get("authority_class") or authority_class) != authority_class:
            raise ContractError("claim provenance authority class conflicts with its origin")
        if raw.get("external_authentication_status") not in {None, "unavailable"}:
            raise ContractError("claim provenance cannot self-assert external authentication")
        core = {
            "exact_claim": exact_claim, "claim_digest": canonical_digest(exact_claim),
            "claim_index": claim_index, "claim_origin": claim_origin,
            "evidence_locator": locator, "extractor_receipt_id": extractor_receipt_id,
            "authority_id": authority_id, "authority_class": authority_class,
            "external_authentication_status": "unavailable", "source_version": source_version,
            "correction_status": correction_status,
        }
        record = {"provenance_id": stable_identifier("source-claim-provenance", source_id, core), **core}
        record["content_digest"] = canonical_digest(record)
        records.append(record)
    return records


def _normalize_source_semantic_warrant(
    raw: Mapping[str, Any],
    *,
    source_id: str,
    source_version: str,
    correction_status: str,
    claims: Sequence[str],
    claim_provenance: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Bind an interpretive warrant to one exact source claim and source state.

    These records are causal inputs, not external semantic judgments.  Their
    authority identifier records who supplied the interpretation, while the
    downstream semantic layer always retains explicit truth and entailment
    nulls.
    """

    exact_claim = _exact_claim_text(raw.get("exact_claim"))
    by_identity = {item.casefold(): item for item in claims}
    if not exact_claim or exact_claim.casefold() not in by_identity:
        raise ContractError(
            f"semantic warrant for {source_id!r} does not bind an exact source claim"
        )
    exact_claim = by_identity[exact_claim.casefold()]
    relation = str(raw.get("relation") or "").strip()
    if relation not in SEMANTIC_RELATIONS:
        raise ContractError(f"unsupported semantic relation: {relation!r}")
    theory_object_ids = sorted(
        {str(item).strip() for item in raw.get("theory_object_ids", []) if str(item).strip()}
    )
    if not theory_object_ids:
        raise ContractError("source semantic warrant requires theory_object_ids")
    warrant_text = _exact_claim_text(raw.get("warrant_text"))
    evidence_locator = _exact_claim_text(raw.get("evidence_locator"))
    authority_id = str(raw.get("authority_id") or "").strip()
    if not warrant_text or not evidence_locator or not authority_id:
        raise ContractError(
            "source semantic warrant requires warrant_text, evidence_locator, and authority_id"
        )
    claim_digest = canonical_digest(exact_claim)
    provenance = next(item for item in claim_provenance if item["claim_digest"] == claim_digest)
    claim_origin = str(provenance["claim_origin"])
    authority_class = str(raw.get("authority_class") or "internal_target_semantic_audit")
    if authority_class not in SEMANTIC_WARRANT_AUTHORITY_CLASSES - {"deterministic_internal_lexical_fallback"}:
        raise ContractError(f"unsupported semantic warrant authority class: {authority_class!r}")
    required_origin = {
        "source_bound_semantic_annotation": "verbatim_source_excerpt",
        "author_paraphrase_interpretation": "author_paraphrase",
        "model_extraction_interpretation": "model_extraction",
    }.get(authority_class)
    if required_origin is not None and claim_origin != required_origin:
        raise ContractError("semantic warrant authority class conflicts with the typed claim origin")
    warrant = {
        "warrant_id": stable_identifier(
            "source-semantic-warrant",
            source_id,
            source_version,
            correction_status,
            claim_digest,
            theory_object_ids,
            relation,
            warrant_text,
            evidence_locator,
            authority_id,
            claim_origin,
            authority_class,
        ),
        "exact_claim": exact_claim,
        "claim_digest": claim_digest,
        "source_version": source_version,
        "correction_status": correction_status,
        "theory_object_ids": theory_object_ids,
        "relation": relation,
        "warrant_text": warrant_text,
        "evidence_locator": evidence_locator,
        "authority_id": authority_id,
        "claim_origin": claim_origin,
        "authority_class": authority_class,
        "extractor_receipt_id": provenance["extractor_receipt_id"],
        "external_authentication_status": "unavailable",
    }
    return warrant


def _normalize_source(raw: Mapping[str, Any], lane_id: str) -> dict[str, Any]:
    """Normalize a provider source into the immutable snapshot representation."""

    source = copy.deepcopy(dict(raw))
    identity = _source_identity(source)
    source_id = str(source.get("source_id") or stable_identifier("source", identity, source.get("source_version", "unknown")))
    claims = sorted(
        {_exact_claim_text(item) for item in source.get("claims", []) if _exact_claim_text(item)}
    )
    source_version = str(source.get("source_version") or "version-unknown").strip()
    correction_status = str(source.get("correction_status") or "unknown")
    claim_provenance = _normalize_claim_provenance(
        list(source.get("claim_provenance", [])), source_id=source_id,
        source_version=source_version, correction_status=correction_status, claims=claims,
    )
    semantic_warrants = [
        _normalize_source_semantic_warrant(
            item,
            source_id=source_id,
            source_version=source_version,
            correction_status=correction_status,
            claims=claims,
            claim_provenance=claim_provenance,
        )
        for item in source.get("semantic_warrants", [])
    ]
    if len({item["warrant_id"] for item in semantic_warrants}) != len(semantic_warrants):
        raise ContractError(f"source {source_id!r} contains duplicate semantic warrants")
    normalized: dict[str, Any] = {
        "source_id": source_id,
        "work_identity": identity,
        "title": str(source.get("title") or "").strip(),
        "authors": sorted({str(item).strip() for item in source.get("authors", []) if str(item).strip()}),
        "publication_date": str(source.get("publication_date") or "unknown").strip(),
        "source_version": source_version,
        "source_type": str(source.get("source_type") or "other"),
        "url": str(source.get("url") or "unavailable").strip(),
        "doi": source.get("doi"),
        "arxiv_id": source.get("arxiv_id"),
        "correction_status": correction_status,
        "lane_ids": [lane_id],
        "decision_relevant": bool(source.get("decision_relevant", True)),
        "claims": claims,
        "claim_provenance": claim_provenance,
        "semantic_warrants": sorted(
            semantic_warrants, key=lambda item: item["warrant_id"]
        ),
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
) -> tuple[list[dict[str, Any]], list[list[str]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Canonically reduce duplicates without completion-order first-wins state."""

    observations = sorted(
        [(lane_id, _normalize_source(raw, lane_id)) for lane_id, raw in lane_sources],
        key=lambda item: (item[1]["work_identity"], item[1]["source_version"], item[0], item[1]["source_id"], item[1]["content_digest"]),
    )
    grouped: dict[tuple[str, str], list[tuple[str, dict[str, Any]]]] = {}
    for lane_id, source in observations:
        grouped.setdefault((source["work_identity"], source["source_version"]), []).append((lane_id, source))
    merged_sources: list[dict[str, Any]] = []
    duplicate_groups: list[list[str]] = []
    claim_conflicts: list[dict[str, Any]] = []
    metadata_conflicts: list[dict[str, Any]] = []

    def variants(rows: Sequence[tuple[str, Mapping[str, Any]]], field: str) -> list[Any]:
        unique = {canonical_digest(source[field]): copy.deepcopy(source[field]) for _lane, source in rows}
        return [unique[key] for key in sorted(unique)]

    def preserve(*, canonical_source_id: str, key: tuple[str, str], field: str,
                 rows: Sequence[tuple[str, Mapping[str, Any]]], effective: Any, status: str) -> None:
        values = sorted([{"lane_id": lane, "source_id": source["source_id"], "value": copy.deepcopy(source[field])} for lane, source in rows], key=canonical_digest)
        metadata_conflicts.append({
            "conflict_id": stable_identifier("literature-metadata-conflict", key, field, values),
            "canonical_source_id": canonical_source_id, "work_identity": key[0],
            "source_version": key[1], "field": field, "observations": values,
            "resolution": {"status": status, "effective_value": copy.deepcopy(effective)},
        })

    for key in sorted(grouped):
        rows = grouped[key]
        if len(rows) == 1:
            merged_sources.append(copy.deepcopy(rows[0][1]))
            continue
        source_ids = sorted({source["source_id"] for _lane, source in rows})
        canonical_source_id = stable_identifier("source-version", key) if len(source_ids) > 1 else source_ids[0]
        if len(source_ids) > 1:
            duplicate_groups.append(source_ids)
        effective = copy.deepcopy(rows[0][1])
        effective["source_id"] = canonical_source_id
        effective["lane_ids"] = sorted({lane for lane, _source in rows})
        if len(source_ids) > 1:
            preserve(canonical_source_id=canonical_source_id, key=key, field="source_id", rows=rows, effective=canonical_source_id, status="aggregate_identifier_unresolved")
        policies = {
            "title": "canonical_display_only", "authors": "canonical_display_only", "publication_date": "canonical_display_only",
            "source_type": "unresolved_to_other", "url": "unresolved_locator", "doi": "unresolved_identifier",
            "arxiv_id": "unresolved_identifier", "correction_status": "unresolved_causal_state", "decision_relevant": "conservative_any_true",
        }
        for field, status in policies.items():
            values = variants(rows, field)
            if len(values) == 1:
                effective[field] = values[0]
                continue
            value: Any = (
                "other" if field == "source_type" else "unavailable" if field == "url"
                else None if field in {"doi", "arxiv_id"} else "unknown" if field == "correction_status"
                else any(bool(item) for item in values) if field == "decision_relevant" else values[0]
            )
            effective[field] = copy.deepcopy(value)
            preserve(canonical_source_id=canonical_source_id, key=key, field=field, rows=rows, effective=value, status=status)
        claim_sets = {canonical_digest(source["claims"]): source["claims"] for _lane, source in rows}
        if len(claim_sets) > 1:
            claim_conflicts.append(
                {
                    "conflict_id": stable_identifier("literature-claim-conflict", key, claim_sets),
                    "work_identity": key[0], "source_version": key[1], "source_ids": source_ids,
                    "claim_observations": sorted([{"lane_id": lane, "source_id": source["source_id"], "claims": source["claims"]} for lane, source in rows], key=canonical_digest),
                    "resolution": (
                        "Retain both source-scoped formulations for claim-level "
                        "assimilation; deduplication does not infer agreement."
                    ),
                }
            )
        effective["claims"] = sorted({claim for _lane, source in rows for claim in source["claims"]})
        provenance_by_claim: dict[str, list[Mapping[str, Any]]] = {}
        for _lane, source in rows:
            for provenance in source["claim_provenance"]:
                provenance_by_claim.setdefault(provenance["claim_digest"], []).append(provenance)
        provenance_inputs: list[dict[str, Any]] = []
        for claim in effective["claims"]:
            claim_digest = canonical_digest(claim)
            source_records = provenance_by_claim.get(claim_digest, [])
            semantic_variants = {
                canonical_digest(_without(record, "provenance_id", "content_digest", "claim_index", "source_version", "correction_status")): record
                for record in source_records
            }
            if len(semantic_variants) == 1:
                chosen = next(iter(semantic_variants.values()))
                provenance_inputs.append({"exact_claim": claim, "claim_origin": chosen["claim_origin"], "evidence_locator": chosen["evidence_locator"], "extractor_receipt_id": chosen["extractor_receipt_id"], "authority_id": chosen["authority_id"]})
            else:
                provenance_inputs.append({"exact_claim": claim, "claim_origin": "model_extraction", "evidence_locator": "conflicting claim provenance; exact source locator unavailable", "authority_id": "claim-provenance-conflict.unresolved"})
                if len(semantic_variants) > 1:
                    provenance_rows = [(lane, {**source, "claim_provenance": [item for item in source["claim_provenance"] if item["claim_digest"] == claim_digest]}) for lane, source in rows if any(item["claim_digest"] == claim_digest for item in source["claim_provenance"])]
                    preserve(canonical_source_id=canonical_source_id, key=key, field="claim_provenance", rows=provenance_rows, effective=provenance_inputs[-1], status="unresolved_to_unverified_extraction")
        effective["claim_provenance"] = _normalize_claim_provenance(
            provenance_inputs, source_id=canonical_source_id, source_version=effective["source_version"],
            correction_status=effective["correction_status"], claims=effective["claims"],
        )
        warrants: dict[str, dict[str, Any]] = {}
        for _lane, source in rows:
            for warrant in source.get("semantic_warrants", []):
                incumbent = warrants.get(warrant["warrant_id"])
                if incumbent is not None and incumbent != warrant:
                    raise ContractError(f"semantic warrant identity conflict for {warrant['warrant_id']}")
                warrants[warrant["warrant_id"]] = warrant
        effective["semantic_warrants"] = [] if effective["correction_status"] == "unknown" or len(source_ids) > 1 else sorted(warrants.values(), key=lambda item: item["warrant_id"])
        effective["limitations"] = sorted({limitation for _lane, source in rows for limitation in source["limitations"]})
        effective["content_digest"] = canonical_digest(_without(effective, "content_digest"))
        merged_sources.append(effective)
    return (
        sorted(merged_sources, key=lambda item: item["source_id"]),
        sorted(duplicate_groups),
        sorted(
            claim_conflicts,
            key=lambda item: (
                item["work_identity"],
                canonical_digest(item),
            ),
        ),
        sorted(metadata_conflicts, key=lambda item: item["conflict_id"]),
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


def _assert_frozen_replay_request_matches(
    request: Mapping[str, Any], original: Mapping[str, Any]
) -> None:
    """Require the replay request to name the exact acquired target and lanes."""

    for request_key, snapshot_key in (
        ("target_id", "target_id"),
        ("claim_scope", "claim_scope"),
        ("theory_state_digest", "theory_state_digest"),
    ):
        if str(request.get(request_key) or "").strip() != original[snapshot_key]:
            raise ContractError(
                f"frozen-response replay {request_key} differs from original acquisition"
            )
    for key in ("coverage_cutoff", "inclusion_policy", "exclusion_policy"):
        if key in request and str(request[key]) != original[key]:
            raise ContractError(
                f"frozen-response replay {key} differs from original acquisition"
            )
    if "coverage_limits" in request:
        limits = [str(item).strip() for item in request["coverage_limits"] if str(item).strip()]
        if limits != original["coverage_limits"]:
            raise ContractError(
                "frozen-response replay coverage_limits differ from original acquisition"
            )
    if request.get("claim_conflicts"):
        raise ContractError(
            "frozen-response replay cannot add request-time claim conflicts"
        )

    requested_lanes = list(request.get("search_lanes", []))
    if len(requested_lanes) != len(LANE_TYPES):
        raise ContractError(
            "frozen-response replay requires the original six differentiated lanes"
        )
    originals = {item["lane_type"]: item for item in original["lane_receipts"]}
    seen: set[str] = set()
    for raw in requested_lanes:
        lane = dict(raw)
        lane_type = str(lane.get("lane_type") or "")
        if lane_type in seen or lane_type not in originals:
            raise ContractError(
                "frozen-response replay requires one exact request per original lane"
            )
        seen.add(lane_type)
        receipt = originals[lane_type]
        queries = [str(item).strip() for item in lane.get("queries", []) if str(item).strip()]
        lane_id = str(
            lane.get("lane_id")
            or stable_identifier("literature-lane", lane_type, lane.get("queries", []))
        )
        inclusion = str(
            lane.get("inclusion_policy")
            or "Include sources responsive to the exact target and lane scope."
        )
        exclusion = str(
            lane.get("exclusion_policy")
            or "Exclude target-mismatched, unverifiable, and duplicate-version records."
        )
        if (
            lane_id != receipt["lane_id"]
            or queries != receipt["queries"]
            or inclusion != receipt["inclusion_policy"]
            or exclusion != receipt["exclusion_policy"]
        ):
            raise ContractError(
                f"frozen-response replay lane {lane_type!r} differs from original acquisition"
            )
        for key in ("provider", "index", "coverage_cutoff"):
            if key in lane and str(lane[key]) != receipt[key]:
                raise ContractError(
                    f"frozen-response replay lane {lane_type!r} changes {key}"
                )
        if "sources" in lane:
            raise ContractError(
                "frozen-response replay content must come only from the original snapshot"
            )
    if seen != set(LANE_TYPES):
        raise ContractError(
            "frozen-response replay requires the original six differentiated lanes"
        )


def _build_frozen_response_replay_snapshot(
    original: Mapping[str, Any],
) -> dict[str, Any]:
    """Derive a non-renewing snapshot from one exact validated acquisition."""

    acquisition = copy.deepcopy(dict(original))
    replay = copy.deepcopy(acquisition)
    replay["snapshot_id"] = stable_identifier(
        "literature-frozen-response-replay",
        acquisition["snapshot_id"],
        acquisition["content_digest"],
    )
    replay["provenance_mode"] = "frozen_response_replay"
    replay["original_acquisition_snapshot"] = acquisition
    for receipt in replay["lane_receipts"]:
        original_receipt = copy.deepcopy(receipt)
        receipt["execution_mode"] = "frozen_response_replay"
        receipt["original_acquisition_receipt"] = original_receipt
        receipt["content_digest"] = canonical_digest(
            _without(receipt, "content_digest", "validator_receipt_ids")
        )
        receipt["validator_receipt_ids"] = [
            stable_identifier(
                "frozen-replay-lane-validator",
                receipt["lane_id"],
                original_receipt["content_digest"],
                receipt["content_digest"],
            )
        ]
    replay["content_digest"] = canonical_digest(
        _without(replay, "content_digest", "validator_receipts", "validation_status")
    )
    validator_id = "target-literature-frozen-replay-validator.v1"
    replay["validator_receipts"] = [
        {
            "receipt_id": stable_identifier(
                SNAPSHOT_VALIDATOR_RECEIPT_DERIVATIONS[validator_id],
                replay["snapshot_id"],
                replay["content_digest"],
            ),
            "validator_id": validator_id,
            "status": "passed",
            "validated_digest": replay["content_digest"],
            # Validation of frozen bytes is historical protocol replay, not a
            # fresh acquisition event.  Preserve the original validator time.
            "completed_at": acquisition["validator_receipts"][0]["completed_at"],
            "reason_codes": [],
        }
    ]
    replay["validation_status"] = "validated"
    return replay


def run_frontier_literature_cycle(
    request: Mapping[str, Any],
    *,
    providers: Mapping[str, Provider] | None = None,
    frozen_response_snapshot: Mapping[str, Any] | None = None,
    max_workers: int = 6,
) -> dict[str, Any]:
    """Execute six independent search lanes and freeze a validated snapshot.

    ``providers`` is keyed by lane type.  A callable is the execution boundary;
    without one, that lane is explicitly local-only.  ``frozen_response_snapshot``
    is a mutually exclusive replay boundary: it must be an exact validated live
    acquisition and cannot acquire new timestamps or content.  The runner never
    promotes inline data or provider labels to live or replay provenance.
    """

    target_id = str(request.get("target_id") or "").strip()
    claim_scope = str(request.get("claim_scope") or "").strip()
    theory_digest = str(request.get("theory_state_digest") or "").strip()
    if not target_id or not claim_scope or not theory_digest:
        raise ContractError("target_id, claim_scope, and theory_state_digest are required")
    lane_requests = [dict(item) for item in request.get("search_lanes", [])]
    requested = {str(item.get("lane_type")): item for item in lane_requests}
    if len(lane_requests) != len(requested):
        raise ContractError("literature request repeats a differentiated lane")
    missing = [lane_type for lane_type in LANE_TYPES if lane_type not in requested]
    if missing:
        raise ContractError(f"missing differentiated literature lanes: {', '.join(missing)}")
    providers = dict(providers or {})
    if frozen_response_snapshot is not None:
        if providers:
            raise ContractError(
                "frozen-response replay is mutually exclusive with provider execution"
            )
        acquisition = copy.deepcopy(dict(frozen_response_snapshot))
        validate_snapshot(acquisition)
        if (
            acquisition["provenance_mode"] != "live"
            or acquisition["validation_status"] != "validated"
        ):
            raise ContractError(
                "frozen-response replay requires an original validated live acquisition"
            )
        _assert_frozen_replay_request_matches(request, acquisition)
        replay = _build_frozen_response_replay_snapshot(acquisition)
        validate_snapshot(replay)
        return replay
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
    sources, duplicate_groups, detected_claim_conflicts, metadata_conflicts = _merge_sources(
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
        "semantic_contract_version": SEMANTIC_CONTRACT_VERSION,
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
            + sorted(copy.deepcopy(list(request.get("claim_conflicts", []))), key=canonical_digest)
        ),
        "metadata_conflicts": metadata_conflicts,
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
    if all(
        receipt["execution_mode"] == "live" and receipt["status"] == "completed"
        for receipt in receipts
    ):
        expected_mode = "live"
    elif all(
        receipt["execution_mode"] == "frozen_response_replay"
        and receipt["status"] == "completed"
        for receipt in receipts
    ):
        expected_mode = "frozen_response_replay"
    else:
        expected_mode = "local_only"
    if snapshot["provenance_mode"] != expected_mode:
        raise ContractError(
            "snapshot provenance does not match the six differentiated lane executions"
        )
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
    if snapshot["provenance_mode"] == "frozen_response_replay":
        acquisition = snapshot["original_acquisition_snapshot"]
        validate_snapshot(acquisition)
        if (
            acquisition["provenance_mode"] != "live"
            or acquisition["validation_status"] != "validated"
        ):
            raise ContractError(
                "frozen-response replay lacks an original validated live acquisition"
            )
        expected_replay = _build_frozen_response_replay_snapshot(acquisition)
        if dict(snapshot) != expected_replay:
            raise ContractError(
                "frozen-response snapshot does not exactly replay its original acquisition"
            )
    known_lanes = {receipt["lane_id"] for receipt in receipts}
    typed_semantics = snapshot.get("semantic_contract_version") == SEMANTIC_CONTRACT_VERSION
    if snapshot.get("semantic_contract_version") not in {None, SEMANTIC_CONTRACT_VERSION}:
        raise ContractError("snapshot declares an unsupported semantic contract")
    if typed_semantics and "metadata_conflicts" not in snapshot:
        raise ContractError("typed semantic snapshots require metadata conflict records")
    for source in snapshot["sources"]:
        if not set(source["lane_ids"]).issubset(known_lanes):
            raise ContractError(f"source {source['source_id']} cites an unknown lane")
        expected_source = canonical_digest(_without(source, "content_digest"))
        if source["content_digest"] != expected_source:
            raise ContractError(f"source {source['source_id']} content digest mismatch")
        claims = {_exact_claim_text(item).casefold() for item in source["claims"]}
        if typed_semantics:
            expected_provenance = _normalize_claim_provenance(
                list(source.get("claim_provenance", [])), source_id=source["source_id"],
                source_version=source["source_version"], correction_status=source["correction_status"], claims=source["claims"],
            )
            if source.get("claim_provenance") != expected_provenance or len(expected_provenance) != len(claims):
                raise ContractError("typed source claim provenance does not replay")
        provenance_by_digest = {item["claim_digest"]: item for item in source.get("claim_provenance", [])}
        warrant_ids: set[str] = set()
        for warrant in source.get("semantic_warrants", []):
            if warrant["warrant_id"] in warrant_ids:
                raise ContractError(
                    f"source {source['source_id']} repeats a semantic warrant"
                )
            warrant_ids.add(warrant["warrant_id"])
            if _exact_claim_text(warrant["exact_claim"]).casefold() not in claims:
                raise ContractError("source semantic warrant crossed its exact claim")
            if warrant["claim_digest"] != canonical_digest(
                _exact_claim_text(warrant["exact_claim"])
            ):
                raise ContractError("source semantic warrant claim digest mismatch")
            if (
                warrant["source_version"] != source["source_version"]
                or warrant["correction_status"] != source["correction_status"]
            ):
                raise ContractError(
                    "source semantic warrant crossed its version or correction state"
                )
            if warrant["relation"] not in SEMANTIC_RELATIONS:
                raise ContractError("source semantic warrant has an unknown relation")
            if typed_semantics:
                provenance = provenance_by_digest.get(warrant["claim_digest"])
                if provenance is None or warrant.get("claim_origin") != provenance["claim_origin"]:
                    raise ContractError("semantic warrant claim origin is not source-bound")
                expected_warrant = _normalize_source_semantic_warrant(
                    warrant, source_id=source["source_id"], source_version=source["source_version"],
                    correction_status=source["correction_status"], claims=source["claims"], claim_provenance=source["claim_provenance"],
                )
                if warrant != expected_warrant:
                    raise ContractError("typed semantic warrant does not replay")
    if typed_semantics:
        conflict_ids = [item["conflict_id"] for item in snapshot["metadata_conflicts"]]
        if len(conflict_ids) != len(set(conflict_ids)) or conflict_ids != sorted(conflict_ids):
            raise ContractError("metadata conflicts require unique canonical identifiers")
        sources_by_id = {item["source_id"]: item for item in snapshot["sources"]}
        for conflict in snapshot["metadata_conflicts"]:
            source = sources_by_id.get(conflict["canonical_source_id"])
            if source is None:
                raise ContractError("metadata conflict cites an unknown canonical source")
            if conflict["field"] == "correction_status" and source["correction_status"] != "unknown":
                raise ContractError("correction-state conflict must remain unresolved")
    validators = list(snapshot["validator_receipts"])
    if len(validators) != 1:
        raise ContractError("snapshot requires exactly one registered validator receipt")
    for receipt in validators:
        if receipt["receipt_id"] != expected_snapshot_validator_receipt_id(
            snapshot, receipt["validator_id"]
        ):
            raise ContractError("snapshot validator receipt identity mismatch")
    passed = [receipt for receipt in validators if receipt["status"] == "passed"]
    if snapshot["validation_status"] == "validated" and not any(
        receipt["validated_digest"] == snapshot["content_digest"] for receipt in passed
    ):
        raise ContractError("validated snapshot lacks a passing digest-bound validator receipt")


def bind_source_semantic_warrants(
    snapshot: Mapping[str, Any],
    warrants: Sequence[Mapping[str, Any]],
    *,
    authority_id: str,
) -> dict[str, Any]:
    """Freeze source-level interpretive warrants into a new snapshot identity.

    The binding is deliberately separate from search execution: lane receipts
    retain their original recency semantics, while the new snapshot digest makes
    every downstream semantic decision causally depend on the exact annotation
    bytes.  Existing warrants are replaced so repeated annotation cannot inherit
    stale version or correction state.
    """

    validate_snapshot(snapshot)
    if not authority_id:
        raise ContractError("semantic warrant binding requires authority_id")
    if snapshot["provenance_mode"] == "frozen_response_replay":
        enriched_acquisition = bind_source_semantic_warrants(
            snapshot["original_acquisition_snapshot"],
            warrants,
            authority_id=authority_id,
        )
        enriched_replay = _build_frozen_response_replay_snapshot(
            enriched_acquisition
        )
        validate_snapshot(enriched_replay)
        return enriched_replay
    enriched = copy.deepcopy(dict(snapshot))
    enriched["semantic_contract_version"] = SEMANTIC_CONTRACT_VERSION
    enriched.setdefault("metadata_conflicts", [])
    for source in enriched["sources"]:
        source["claim_provenance"] = _normalize_claim_provenance(
            list(source.get("claim_provenance", [])), source_id=source["source_id"],
            source_version=source["source_version"], correction_status=source["correction_status"], claims=source["claims"],
        )
        source["content_digest"] = canonical_digest(_without(source, "content_digest"))
    sources = {item["source_id"]: item for item in enriched["sources"]}
    grouped: dict[str, list[dict[str, Any]]] = {source_id: [] for source_id in sources}
    for raw in warrants:
        source_id = str(raw.get("source_id") or "").strip()
        if source_id not in sources:
            raise ContractError(
                f"semantic warrant cites source outside snapshot: {source_id!r}"
            )
        source = sources[source_id]
        normalized = _normalize_source_semantic_warrant(
            {**dict(raw), "authority_id": str(raw.get("authority_id") or authority_id)},
            source_id=source_id,
            source_version=source["source_version"],
            correction_status=source["correction_status"],
            claims=source["claims"],
            claim_provenance=source["claim_provenance"],
        )
        grouped[source_id].append(normalized)
    for source_id, source in sources.items():
        source_warrants = sorted(grouped[source_id], key=lambda item: item["warrant_id"])
        if len({item["warrant_id"] for item in source_warrants}) != len(source_warrants):
            raise ContractError(f"duplicate semantic warrant for source {source_id!r}")
        source["semantic_warrants"] = source_warrants
        source["content_digest"] = canonical_digest(_without(source, "content_digest"))
    enriched["snapshot_id"] = stable_identifier(
        "literature-semantic-snapshot",
        enriched["target_id"],
        enriched["theory_state_digest"],
        enriched["search_started_at"],
        enriched["search_completed_at"],
        enriched["sources"],
    )
    enriched["content_digest"] = canonical_digest(
        _without(enriched, "content_digest", "validator_receipts", "validation_status")
    )
    enriched["validator_receipts"] = [
        {
            "receipt_id": stable_identifier(
                "semantic-snapshot-validator",
                enriched["snapshot_id"],
                enriched["content_digest"],
            ),
            "validator_id": "source-semantic-snapshot-validator.v1",
            "status": "passed",
            "validated_digest": enriched["content_digest"],
            "completed_at": enriched["search_completed_at"],
            "reason_codes": [],
        }
    ]
    enriched["validation_status"] = "validated"
    validate_snapshot(enriched)
    return enriched


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


def _bounded_lexical_semantic_relation(
    source: Mapping[str, Any], *, matched: bool, claim: str, claim_provenance: Mapping[str, Any]
) -> tuple[str, list[str]]:
    """Classify an asserted relation without pretending to understand a source.

    The result is an internal routing hint.  Negation, paraphrase, morphology,
    mathematical scope, and genuine entailment remain unresolved by design.
    """

    correction_status = str(source.get("correction_status") or "unknown")
    if correction_status in {"corrected", "superseded", "retracted"}:
        return "unresolved", [f"correction_status:{correction_status}"]
    if not matched:
        return "unresolved", ["no_exact_catalog_term_match"]
    normalized = " ".join(claim.lower().split())
    uncertainty = [code for code, pattern in _LEXICAL_UNCERTAINTY_PATTERNS if pattern.search(claim)]
    if claim_provenance["claim_origin"] != "verbatim_source_excerpt":
        uncertainty.append(f"nonverbatim_claim_origin:{claim_provenance['claim_origin']}")
    if uncertainty:
        return "unresolved", sorted(set(uncertainty))
    signals_by_event = {
        event_type: [signal for signal in signals if signal in normalized]
        for event_type, signals in _CLAIM_SIGNALS
    }
    if signals_by_event.get("demote"):
        return "contradicts", signals_by_event["demote"]
    if signals_by_event.get("new_question"):
        return "leaves_open", signals_by_event["new_question"]
    positive = [
        signal
        for event_type in ("split", "merge", "spawn", "reprioritize")
        for signal in signals_by_event.get(event_type, [])
    ]
    if positive:
        return "entails", positive
    return "unresolved", ["no_relation_signal_after_exact_term_match"]


def _build_semantic_claim_layer(
    snapshot: Mapping[str, Any], catalog: Mapping[str, Any]
) -> dict[str, Any]:
    """Lift every distinct source claim into one typed effective warrant."""

    object_by_id = {
        item["theory_object_id"]: item for item in catalog["theory_objects"]
    }
    scope_anchor = next(
        item for item in catalog["theory_objects"] if item["scope_anchor"]
    )
    claim_records: list[dict[str, Any]] = []
    claimless_source_ids: list[str] = []
    explicit_count = 0
    fallback_count = 0
    for source in sorted(snapshot["sources"], key=lambda item: item["source_id"]):
        distinct_claims: dict[str, str] = {}
        for raw_claim in source["claims"]:
            exact_claim = _exact_claim_text(raw_claim)
            incumbent = distinct_claims.get(exact_claim.casefold())
            if incumbent is None or exact_claim < incumbent:
                distinct_claims[exact_claim.casefold()] = exact_claim
        if not distinct_claims:
            claimless_source_ids.append(source["source_id"])
            placeholder = "Source supplied no separately transcribed claim."
            distinct_claims[placeholder.casefold()] = placeholder
        source_warrants: dict[str, list[Mapping[str, Any]]] = {}
        for warrant in source.get("semantic_warrants", []):
            source_warrants.setdefault(warrant["claim_digest"], []).append(warrant)
        provenance_by_digest = {item["claim_digest"]: item for item in source.get("claim_provenance", [])}
        for claim_index, exact_claim in enumerate(sorted(distinct_claims.values())):
            claim_digest = canonical_digest(exact_claim)
            claim_id = stable_identifier(
                "source-semantic-claim",
                source["source_id"],
                source["source_version"],
                source["correction_status"],
                claim_digest,
            )
            matches = _claim_object_matches(exact_claim, catalog["theory_objects"])
            claim_provenance = provenance_by_digest.get(claim_digest) or {
                "claim_origin": "internal_target_audit" if not source["claims"] else "model_extraction",
                "evidence_locator": "missing claim null" if not source["claims"] else "legacy untyped provider claim field",
                "extractor_receipt_id": None,
                "authority_id": "missing-claim-null.v1" if not source["claims"] else "legacy-provider-claim.unverified",
                "authority_class": "missing_claim_null" if not source["claims"] else "unverified_provider_claim_extraction",
                "external_authentication_status": "unavailable",
            }
            explicit = source_warrants.get(claim_digest, [])
            relation_warrants: list[dict[str, Any]] = []
            if explicit:
                explicit_count += 1
                for raw_warrant in explicit:
                    unknown = sorted(
                        set(raw_warrant["theory_object_ids"]) - set(object_by_id)
                    )
                    if unknown:
                        raise ContractError(
                            "source semantic warrant cites unknown theory objects: "
                            + ", ".join(unknown)
                        )
                    core = {
                        "warrant_id": raw_warrant["warrant_id"],
                        "relation": raw_warrant["relation"],
                        "theory_object_ids": list(raw_warrant["theory_object_ids"]),
                        "matched_terms": sorted(
                            {
                                term
                                for match in matches
                                if match["theory_object_id"]
                                in raw_warrant["theory_object_ids"]
                                for term in match["matched_terms"]
                            }
                        ),
                        "basis_mode": "source_level_explicit",
                        "basis_evidence": [
                            raw_warrant["warrant_text"],
                            f"locator:{raw_warrant['evidence_locator']}",
                        ],
                        "authority": {
                            "authority_id": raw_warrant["authority_id"],
                            "authority_class": raw_warrant.get("authority_class", "internal_target_semantic_audit"),
                            "external_authentication_status": "unavailable",
                        },
                        "claim_origin": claim_provenance["claim_origin"],
                        "nulls": {
                            "source_truth_authorized": False,
                            "semantic_entailment_authorized": False,
                            "novelty_authorized": False,
                        },
                    }
                    core["warrant_digest"] = canonical_digest(core)
                    relation_warrants.append(core)
                effective_relations = {
                    item["relation"] for item in relation_warrants
                }
                effective_relation = (
                    next(iter(effective_relations))
                    if len(effective_relations) == 1
                    else "unresolved"
                )
                effective_ids = sorted(
                    {
                        object_id
                        for item in relation_warrants
                        for object_id in item["theory_object_ids"]
                    }
                )
                basis_mode = "source_level_explicit"
            else:
                fallback_count += 1
                selected = matches or [
                    {
                        "theory_object_id": scope_anchor["theory_object_id"],
                        "object_kind": scope_anchor["object_kind"],
                        "matched_terms": [],
                        "matched_weight": 0,
                    }
                ]
                effective_ids = [item["theory_object_id"] for item in selected]
                effective_relation, signals = _bounded_lexical_semantic_relation(
                    source, matched=bool(matches), claim=exact_claim, claim_provenance=claim_provenance
                )
                basis_mode = "bounded_lexical_fallback"
                core = {
                    "warrant_id": stable_identifier(
                        "lexical-semantic-warrant",
                        claim_id,
                        effective_ids,
                        effective_relation,
                        signals,
                    ),
                    "relation": effective_relation,
                    "theory_object_ids": effective_ids,
                    "matched_terms": sorted(
                        {term for item in selected for term in item["matched_terms"]}
                    ),
                    "basis_mode": basis_mode,
                    "basis_evidence": signals,
                    "authority": {
                        "authority_id": SEMANTIC_CLAIM_AUTHORITY_ID,
                        "authority_class": "deterministic_internal_lexical_fallback",
                        "external_authentication_status": "unavailable",
                    },
                    "claim_origin": claim_provenance["claim_origin"],
                    "nulls": {
                        "source_truth_authorized": False,
                        "semantic_entailment_authorized": False,
                        "novelty_authorized": False,
                    },
                }
                core["warrant_digest"] = canonical_digest(core)
                relation_warrants.append(core)
            record = {
                "claim_id": claim_id,
                "source_id": source["source_id"],
                "work_identity": source["work_identity"],
                "source_content_digest": source["content_digest"],
                "source_state": {
                    "source_version": source["source_version"],
                    "correction_status": source["correction_status"],
                    "state_authority": "frozen_snapshot_source_record",
                },
                "exact_claim": exact_claim,
                "claim_digest": claim_digest,
                "extraction_provenance": {
                    "mode": (
                        "missing_claim_null"
                        if not source["claims"]
                        else "snapshot_exact_claim"
                    ),
                    "claim_index": claim_index if source["claims"] else None,
                    "lane_ids": list(source["lane_ids"]),
                    "snapshot_id": snapshot["snapshot_id"],
                    "claim_origin": claim_provenance["claim_origin"],
                    "evidence_locator": claim_provenance["evidence_locator"],
                    "extractor_receipt_id": claim_provenance["extractor_receipt_id"],
                    "authority_id": claim_provenance["authority_id"],
                    "authority_class": claim_provenance["authority_class"],
                    "external_authentication_status": "unavailable",
                },
                "effective_relation": effective_relation,
                "effective_theory_object_ids": effective_ids,
                "basis_mode": basis_mode,
                "relation_warrants": sorted(
                    relation_warrants, key=lambda item: item["warrant_id"]
                ),
            }
            record["record_digest"] = canonical_digest(record)
            claim_records.append(record)
    unresolved_claim_ids = sorted(
        item["claim_id"]
        for item in claim_records
        if item["effective_relation"] == "unresolved"
    )
    if not claim_records:
        coverage_status = "empty_snapshot"
    elif explicit_count == len(claim_records):
        coverage_status = (
            "source_warrant_complete_with_unresolved"
            if unresolved_claim_ids
            else "source_warrant_complete"
        )
    elif fallback_count == len(claim_records):
        coverage_status = "lexical_fallback_only"
    else:
        coverage_status = "bounded_mixed"
    coverage_audit = {
        "decision_relevant_source_ids": sorted(
            item["source_id"]
            for item in snapshot["sources"]
            if item["decision_relevant"]
        ),
        "source_count": len(snapshot["sources"]),
        "claim_record_count": len(claim_records),
        "explicit_warrant_claim_count": explicit_count,
        "lexical_fallback_claim_count": fallback_count,
        "unresolved_claim_ids": unresolved_claim_ids,
        "claimless_source_ids": sorted(claimless_source_ids),
        "corrected_or_superseded_source_ids": sorted(
            item["source_id"]
            for item in snapshot["sources"]
            if item["correction_status"] in {"corrected", "superseded"}
        ),
        "retracted_source_ids": sorted(
            item["source_id"]
            for item in snapshot["sources"]
            if item["correction_status"] == "retracted"
        ),
        "coverage_status": coverage_status,
        "coverage_limits": list(snapshot["coverage_limits"]),
        "claim_origin_counts": {
            origin: sum(item["extraction_provenance"]["claim_origin"] == origin for item in claim_records)
            for origin in sorted(CLAIM_ORIGINS)
        },
        "claim_provenance_gap_ids": sorted(
            item["claim_id"] for item in claim_records
            if item["extraction_provenance"]["authority_class"] in {"unverified_provider_claim_extraction", "missing_claim_null"}
        ),
        "snapshot_claim_enumeration_complete": True,
        "semantic_resolution_complete": not unresolved_claim_ids,
        "truth_authorized": False,
        "exhaustiveness_authorized": False,
        "novelty_authorized": False,
    }
    layer: dict[str, Any] = {
        "schema_version": "1.0",
        "layer_id": stable_identifier(
            "literature-semantic-claim-layer",
            snapshot["content_digest"],
            catalog["content_digest"],
            claim_records,
        ),
        "target_id": snapshot["target_id"],
        "theory_state_digest": snapshot["theory_state_digest"],
        "snapshot_id": snapshot["snapshot_id"],
        "snapshot_digest": snapshot["content_digest"],
        "theory_catalog_id": catalog["catalog_id"],
        "theory_catalog_digest": catalog["content_digest"],
        "claim_records": claim_records,
        "coverage_audit": coverage_audit,
        "authority": {
            "authority_id": SEMANTIC_CLAIM_AUTHORITY_ID,
            "algorithm_id": SEMANTIC_CLAIM_ALGORITHM_ID,
            "authority_class": "deterministic_internal_semantic_routing",
        },
        "epistemic_nulls": {
            "source_truth_authorized": False,
            "semantic_entailment_authorized": False,
            "exhaustive_coverage_authorized": False,
            "novelty_authorized": False,
            "external_validation_status": "unavailable",
        },
    }
    layer["content_digest"] = canonical_digest(_without(layer, "content_digest"))
    return layer


def build_semantic_claim_layer(
    snapshot: Mapping[str, Any], *, theory_catalog: Mapping[str, Any]
) -> dict[str, Any]:
    """Build and validate the source/version/correction-aware semantic layer."""

    validate_snapshot(snapshot)
    validate_theory_object_catalog(theory_catalog)
    if snapshot["target_id"] != theory_catalog["target_id"]:
        raise ContractError("semantic claim layer target mismatch")
    if snapshot["theory_state_digest"] != theory_catalog["theory_state_digest"]:
        raise ContractError("semantic claim layer theory-state mismatch")
    layer = _build_semantic_claim_layer(snapshot, theory_catalog)
    validate_semantic_claim_layer(
        layer, snapshot=snapshot, theory_catalog=theory_catalog
    )
    return layer


def validate_semantic_claim_layer(
    layer: Mapping[str, Any],
    *,
    snapshot: Mapping[str, Any],
    theory_catalog: Mapping[str, Any],
) -> None:
    """Reject semantic-layer mutation, stale source state, or coverage inflation."""

    validate_payload(dict(layer), "literature_semantic_claim_layer.schema.json")
    if layer["content_digest"] != canonical_digest(_without(layer, "content_digest")):
        raise ContractError("semantic claim layer content digest mismatch")
    if (
        layer["snapshot_digest"] != snapshot["content_digest"]
        or layer["theory_catalog_digest"] != theory_catalog["content_digest"]
    ):
        raise ContractError("semantic claim layer crossed its frozen inputs")
    expected = _build_semantic_claim_layer(snapshot, theory_catalog)
    if dict(layer) != expected:
        raise ContractError("semantic claim layer does not replay from snapshot claims")


def _derive_event(
    source: Mapping[str, Any], *, semantic_relation: str, claim: str
) -> str:
    """Derive one causal event from correction state and the effective warrant."""

    correction_status = str(source.get("correction_status") or "unknown")
    if correction_status == "retracted":
        return "retire"
    if correction_status in {"superseded", "corrected"}:
        return "reframe"
    if semantic_relation == "contradicts":
        return "demote"
    if semantic_relation == "leaves_open":
        return "new_question"
    if semantic_relation == "unresolved":
        return "justified_no_change"
    normalized_claim = " ".join(claim.lower().split())
    for event_type, signals in _CLAIM_SIGNALS:
        if event_type in {"demote", "new_question"}:
            continue
        if any(signal in normalized_claim for signal in signals):
            return event_type
    return "reprioritize"


def _derive_one_claim_mapping(
    *,
    source: Mapping[str, Any],
    claim_record: Mapping[str, Any],
    theory_objects: Sequence[Mapping[str, Any]],
    scope_anchor: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    catalog: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Derive one independently receipted mapping from one distinct claim."""

    exact_claim = str(claim_record["exact_claim"])
    matches = _claim_object_matches(exact_claim, theory_objects)
    lexically_matched = bool(matches)
    explicitly_bound = claim_record["basis_mode"] == "source_level_explicit"
    semantically_bound = explicitly_bound or lexically_matched
    by_id = {item["theory_object_id"]: item for item in theory_objects}
    selected_objects = [
        {
            **by_id[object_id],
            "matched_terms": next(
                (
                    item["matched_terms"]
                    for item in matches
                    if item["theory_object_id"] == object_id
                ),
                [],
            ),
            "matched_weight": next(
                (
                    item["matched_weight"]
                    for item in matches
                    if item["theory_object_id"] == object_id
                ),
                0,
            ),
        }
        for object_id in claim_record["effective_theory_object_ids"]
    ]
    semantic_relation = str(claim_record["effective_relation"])
    event_type = _derive_event(
        source, semantic_relation=semantic_relation, claim=exact_claim
    )
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
    if semantically_bound:
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
            else ("medium" if semantically_bound else "low")
        ),
        "source_version": source["source_version"],
        "source_correction_status": source["correction_status"],
        "semantic_claim_id": claim_record["claim_id"],
        "semantic_claim_digest": claim_record["claim_digest"],
        "semantic_relation": semantic_relation,
        "semantic_warrant_ids": [
            item["warrant_id"] for item in claim_record["relation_warrants"]
        ],
        "semantic_warrant_digest": canonical_digest(
            [item["warrant_digest"] for item in claim_record["relation_warrants"]]
        ),
        "semantic_basis_mode": claim_record["basis_mode"],
        "claim_origin": claim_record["extraction_provenance"]["claim_origin"],
        "claim_authority_class": claim_record["extraction_provenance"]["authority_class"],
        "semantic_authority_classes": sorted({item["authority"]["authority_class"] for item in claim_record["relation_warrants"]}),
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
            "source_level_explicit_warrant_then_correction_relation_rules"
            if explicitly_bound
            else (
                "bounded_lexical_maximal_term_tie_then_status_and_ordered_claim_signals"
                if lexically_matched
                else "bounded_lexical_unmatched_to_scope_anchor_justified_no_change"
            )
        ),
        "event_type": event_type,
        "policy_digest": canonical_digest(_MAPPING_POLICY),
        "source_version": source["source_version"],
        "source_correction_status": source["correction_status"],
        "semantic_claim_id": claim_record["claim_id"],
        "semantic_claim_digest": claim_record["claim_digest"],
        "semantic_relation": semantic_relation,
        "semantic_warrant_ids": mapping["semantic_warrant_ids"],
        "semantic_warrant_digest": mapping["semantic_warrant_digest"],
        "semantic_basis_mode": claim_record["basis_mode"],
        "claim_origin": mapping["claim_origin"],
        "claim_authority_class": mapping["claim_authority_class"],
        "semantic_authority_classes": mapping["semantic_authority_classes"],
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
    semantic_layer = _build_semantic_claim_layer(snapshot, catalog)
    theory_mappings: list[dict[str, Any]] = []
    mapping_receipts: list[dict[str, Any]] = []
    concept_updates: list[dict[str, Any]] = []
    branch_updates: list[dict[str, Any]] = []
    source_by_id = {item["source_id"]: item for item in snapshot["sources"]}
    for claim_record in semantic_layer["claim_records"]:
        source = source_by_id[claim_record["source_id"]]
        mapping, receipt, concept_update, branch_update = _derive_one_claim_mapping(
            source=source,
            claim_record=claim_record,
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
        "schema_version": "2.0",
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
        "semantic_claim_layer": semantic_layer,
        "semantic_claim_layer_digest": semantic_layer["content_digest"],
        "semantic_coverage_audit": copy.deepcopy(semantic_layer["coverage_audit"]),
        "derivation_authority": {
            "authority_id": CLAIM_MAPPING_AUTHORITY_ID,
            "algorithm_id": CLAIM_MAPPING_ALGORITHM_ID,
            "policy_digest": canonical_digest(_MAPPING_POLICY),
            "authority_class": "deterministic_internal_derivation",
            "semantic_layer_authority_id": SEMANTIC_CLAIM_AUTHORITY_ID,
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
            "The mapper deterministically consumes exact source-level warrants, "
            "with a bounded lexical/status fallback, and records their theory-side "
            "consequences. It does not establish source truth, semantic entailment, "
            "exhaustiveness, novelty, conceptual quality, or efficacy."
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
    validate_semantic_claim_layer(
        packet["semantic_claim_layer"],
        snapshot=snapshot,
        theory_catalog=theory_catalog,
    )
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
    freshness_max_age_seconds: int | None = DEFAULT_LITERATURE_FRESHNESS_SECONDS,
    freshness_evaluated_at: str | datetime | None = None,
) -> dict[str, Any]:
    """Consume only a recomputable mapping derivation at the assimilation boundary."""

    validate_claim_mapping_derivation(
        mapping_derivation, snapshot=snapshot, theory_catalog=theory_catalog
    )
    mapping_provenance = {
        "mode": "deterministic_claim_derivation", "derivation_id": mapping_derivation["derivation_id"],
        "derivation_digest": mapping_derivation["content_digest"], "authority_id": mapping_derivation["derivation_authority"]["authority_id"],
        "semantic_claim_layer_id": mapping_derivation["semantic_claim_layer"]["layer_id"],
        "semantic_claim_layer_digest": mapping_derivation["semantic_claim_layer_digest"],
        "semantic_authority_id": mapping_derivation["semantic_claim_layer"]["authority"]["authority_id"],
    }
    normalized_evaluated_at = _normalize_freshness_evaluation(
        freshness_evaluated_at, freshness_max_age_seconds, snapshot=snapshot
    )
    replay_core: dict[str, Any] = {
        "source_snapshot": copy.deepcopy(dict(snapshot)), "theory_catalog": copy.deepcopy(dict(theory_catalog)),
        "mapping_derivation": copy.deepcopy(dict(mapping_derivation)), "hypothesis_inputs": copy.deepcopy(list(hypotheses)),
        "prior_snapshot": copy.deepcopy(dict(prior_snapshot)) if prior_snapshot is not None else None,
        "candidate_snapshot_ids": sorted(set(candidate_snapshot_ids)),
    }
    if freshness_max_age_seconds is not None:
        # The policy input belongs in the replay core; otherwise a caller could
        # rewrite the deadline without changing the claimed derivation inputs.
        replay_core["freshness_max_age_seconds"] = freshness_max_age_seconds
        replay_core["freshness_evaluated_at"] = normalized_evaluated_at
    replay_core["content_digest"] = canonical_digest(replay_core)
    return assimilate_literature(
        snapshot,
        theory_state_digest=theory_catalog["theory_state_digest"],
        theory_mappings=mapping_derivation["theory_mappings"],
        hypotheses=hypotheses,
        prior_snapshot=prior_snapshot,
        candidate_snapshot_ids=candidate_snapshot_ids,
        mapping_provenance=mapping_provenance,
        semantic_claim_layer=mapping_derivation["semantic_claim_layer"],
        derivation_replay=replay_core,
        freshness_max_age_seconds=freshness_max_age_seconds,
        freshness_evaluated_at=normalized_evaluated_at,
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


def _normalize_counterfactual_world(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Separate causal transformation identity from labels and expectations."""

    allowed = {"world_id", "operation", "source_id", "source_version", "replacement_claim", "contradictory_claim", "coverage_limit", "expected_effect"}
    unexpected = sorted(set(raw) - allowed)
    if unexpected:
        raise ContractError("counterfactual world contains unsupported fields: " + ", ".join(unexpected))
    label, operation = str(raw.get("world_id") or "").strip(), str(raw.get("operation") or "")
    if not label:
        raise ContractError("every replay world requires world_id")
    if operation not in LITERATURE_REPLAY_OPERATIONS:
        raise ContractError(f"unsupported literature replay operation: {operation!r}")
    transformation = {key: copy.deepcopy(raw[key]) for key in ("operation", "source_id", "source_version", "replacement_claim", "contradictory_claim", "coverage_limit") if key in raw}
    expected = str(raw.get("expected_effect") or "unspecified")
    if expected not in {"change", "null", "unspecified"}:
        raise ContractError("expected_effect must be change, null, or unspecified")
    return {"world_label": label, "transformation": transformation, "transformation_id": stable_identifier("literature-counterfactual-transformation", transformation), "expected_effect": expected}


def _replay_snapshot(
    snapshot: Mapping[str, Any], transformation: Mapping[str, Any]
) -> dict[str, Any]:
    """Create a deterministic, internally valid counterfactual snapshot."""

    operation = str(transformation.get("operation") or "")
    if operation not in LITERATURE_REPLAY_OPERATIONS:
        raise ContractError(f"unsupported literature replay operation: {operation!r}")
    transformed = copy.deepcopy(dict(snapshot))
    source_id = str(transformation.get("source_id") or "")
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
            transformation.get("source_version") or f"{source['source_version']}.superseded"
        )
        if transformation.get("replacement_claim"):
            source["claims"] = [str(transformation["replacement_claim"])]
        # A source-level warrant is exact-version evidence.  It cannot survive a
        # synthetic supersession or silently migrate to replacement text.
        source["semantic_warrants"] = []
        source["claim_provenance"] = _normalize_claim_provenance([], source_id=source["source_id"], source_version=source["source_version"], correction_status=source["correction_status"], claims=source["claims"])
        source["content_digest"] = canonical_digest(_without(source, "content_digest"))
    elif operation == "contradict_source":
        source = source_by_id[source_id]
        contradictory_claim = str(transformation.get("contradictory_claim") or "").strip()
        if not contradictory_claim:
            raise ContractError("contradict_source requires contradictory_claim")
        source["claims"] = [contradictory_claim]
        source["correction_status"] = "none_known"
        source["source_version"] = f"{source['source_version']}.contradictory"
        source["semantic_warrants"] = []
        source["claim_provenance"] = _normalize_claim_provenance([], source_id=source["source_id"], source_version=source["source_version"], correction_status=source["correction_status"], claims=source["claims"])
        source["content_digest"] = canonical_digest(_without(source, "content_digest"))
    elif operation == "coverage_only_change":
        coverage_limit = str(transformation.get("coverage_limit") or "").strip()
        if not coverage_limit:
            raise ContractError("coverage_only_change requires coverage_limit")
        transformed["coverage_limits"] = sorted(
            set(transformed["coverage_limits"] + [coverage_limit])
        )

    # Counterfactual source worlds are locally generated protocol probes.  A
    # live baseline receipt cannot lend them live-search authority.
    transformed["provenance_mode"] = "local_only"
    transformed.pop("original_acquisition_snapshot", None)
    retained_ids = {item["source_id"] for item in transformed["sources"]}
    for receipt in transformed["lane_receipts"]:
        receipt["execution_mode"] = "local_only"
        receipt.pop("original_acquisition_receipt", None)
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
    transformed["metadata_conflicts"] = []
    transformed["snapshot_id"] = stable_identifier(
        "literature-replay-snapshot",
        snapshot["snapshot_id"],
        snapshot["content_digest"],
        transformation,
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
                    "source_version",
                    "source_correction_status",
                    "semantic_claim_id",
                    "semantic_claim_digest",
                    "semantic_relation",
                    "semantic_warrant_ids",
                    "semantic_warrant_digest",
                    "semantic_basis_mode",
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
    candidate_snapshot_ids: Sequence[str],
    freshness_max_age_seconds: int | None,
    freshness_evaluated_at: str | datetime | None,
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
        candidate_snapshot_ids=candidate_snapshot_ids,
        freshness_max_age_seconds=freshness_max_age_seconds,
        freshness_evaluated_at=freshness_evaluated_at,
    )
    baseline_projection = _literature_decision_projection(
        baseline_derivation, baseline_assimilation
    )
    results: list[dict[str, Any]] = []
    normalized_worlds = sorted((_normalize_counterfactual_world(dict(raw)) for raw in worlds), key=lambda item: (item["transformation_id"], item["world_label"]))
    if len({item["world_label"] for item in normalized_worlds}) != len(normalized_worlds):
        raise ContractError("literature replay world labels must be unique")
    if len({item["transformation_id"] for item in normalized_worlds}) != len(normalized_worlds):
        raise ContractError("literature replay transformations must be unique")
    for world in normalized_worlds:
        counterfactual_snapshot = _replay_snapshot(snapshot, world["transformation"])
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
            candidate_snapshot_ids=sorted(
                set(candidate_snapshot_ids) | {snapshot["snapshot_id"]}
            ),
            freshness_max_age_seconds=freshness_max_age_seconds,
            freshness_evaluated_at=freshness_evaluated_at,
        )
        projection = _literature_decision_projection(derivation, assimilation)
        projection_changed = projection != baseline_projection
        expectation = world["expected_effect"]
        expectation_met = expectation == "unspecified" or (expectation == "change" and projection_changed) or (expectation == "null" and not projection_changed)
        if not expectation_met:
            raise ContractError(f"declared counterfactual control failed: {world['world_label']} expected {expectation}")
        result = {
            "world_id": world["world_label"], "transformation_id": world["transformation_id"],
            "transformation": world["transformation"], "transformation_digest": canonical_digest(world["transformation"]),
            "evaluation": {"expected_effect": expectation, "observed_effect": "change" if projection_changed else "null", "status": "passed"},
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
                "semantic_claim_layer_changed": derivation[
                    "semantic_claim_layer_digest"
                ]
                != baseline_derivation["semantic_claim_layer_digest"],
                "semantic_relation_decisions_changed": [
                    (
                        item["source_id"],
                        item["semantic_claim_id"],
                        item["semantic_relation"],
                        item["semantic_basis_mode"],
                    )
                    for item in derivation["theory_mappings"]
                ]
                != [
                    (
                        item["source_id"],
                        item["semantic_claim_id"],
                        item["semantic_relation"],
                        item["semantic_basis_mode"],
                    )
                    for item in baseline_derivation["theory_mappings"]
                ],
                "semantic_coverage_audit_changed": derivation[
                    "semantic_coverage_audit"
                ]
                != baseline_derivation["semantic_coverage_audit"],
                "null_effect": not projection_changed,
            },
        }
        result["content_digest"] = canonical_digest(_without(result, "content_digest"))
        results.append(result)
    causal_replay_id = stable_identifier("literature-counterfactual-causal-replay", snapshot["content_digest"], theory_catalog["content_digest"], sorted(item["transformation_id"] for item in results))
    replay: dict[str, Any] = {
        "schema_version": "2.0",
        "replay_id": stable_identifier(
            "literature-counterfactual-evaluation", causal_replay_id,
            baseline_assimilation["content_digest"],
            [(item["world_id"], item["evaluation"]["expected_effect"]) for item in results],
        ),
        "causal_replay_id": causal_replay_id,
        "causal_transformation_ids": sorted(item["transformation_id"] for item in results),
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
        "control_status": "passed",
        "claim_boundary": (
            "Replay demonstrates deterministic sensitivity or insensitivity of "
            "this source-warrant/lexical-fallback mapping policy on supplied worlds. "
            "It is not evidence that a relation is a semantic entailment, that a "
            "source is true, that coverage is exhaustive, or that the derived "
            "concepts are novel, deep, or discovery-effective."
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
    candidate_snapshot_ids: Sequence[str] = (),
    freshness_max_age_seconds: int | None = DEFAULT_LITERATURE_FRESHNESS_SECONDS,
    freshness_evaluated_at: str | datetime | None = None,
) -> dict[str, Any]:
    """Rebuild every world under the baseline's exact assimilation context."""

    validate_snapshot(snapshot)
    validate_theory_object_catalog(theory_catalog)
    if len(worlds) < 1:
        raise ContractError("literature counterfactual replay requires at least one world")
    normalized_evaluated_at = _normalize_freshness_evaluation(
        freshness_evaluated_at, freshness_max_age_seconds, snapshot=snapshot
    )
    replay = _build_literature_counterfactual_replay(
        snapshot,
        theory_catalog=theory_catalog,
        worlds=worlds,
        hypotheses=hypotheses,
        candidate_snapshot_ids=candidate_snapshot_ids,
        freshness_max_age_seconds=freshness_max_age_seconds,
        freshness_evaluated_at=normalized_evaluated_at,
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
        worlds=[{"world_id": item["world_id"], **item["transformation"], "expected_effect": item["evaluation"]["expected_effect"]} for item in replay["world_results"]],
        hypotheses=hypotheses,
        candidate_snapshot_ids=replay["baseline"]["assimilation"]
        .get("derivation_replay", {})
        .get("candidate_snapshot_ids", []),
        freshness_max_age_seconds=replay["baseline"]["assimilation"]
        .get("derivation_replay", {})
        .get("freshness_max_age_seconds"),
        freshness_evaluated_at=replay["baseline"]["assimilation"]
        .get("derivation_replay", {})
        .get("freshness_evaluated_at"),
    )
    if dict(replay) != expected:
        raise ContractError(
            "literature counterfactual replay does not rebuild from snapshot contents"
        )


def _build_assimilation_packet(
    snapshot: Mapping[str, Any],
    *,
    theory_state_digest: str,
    theory_mappings: Sequence[Mapping[str, Any]],
    hypotheses: Sequence[Mapping[str, Any]] = (),
    prior_snapshot: Mapping[str, Any] | None = None,
    candidate_snapshot_ids: Sequence[str] = (),
    mapping_provenance: Mapping[str, Any] | None = None,
    semantic_claim_layer: Mapping[str, Any] | None = None,
    derivation_replay: Mapping[str, Any] | None = None,
    freshness_max_age_seconds: int | None = DEFAULT_LITERATURE_FRESHNESS_SECONDS,
    freshness_evaluated_at: str | datetime | None = None,
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
        if semantic_claim_layer is not None:
            semantic_fields = (
                "source_version",
                "source_correction_status",
                "semantic_claim_id",
                "semantic_claim_digest",
                "semantic_relation",
                "semantic_warrant_ids",
                "semantic_warrant_digest",
                "semantic_basis_mode",
                "claim_origin", "claim_authority_class", "semantic_authority_classes",
            )
            if any(field not in mapping for field in semantic_fields):
                raise ContractError(
                    "derived semantic mapping lacks exact claim/warrant bindings"
                )
            normalized.update({field: copy.deepcopy(mapping[field]) for field in semantic_fields})
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
    normalized_evaluated_at = _normalize_freshness_evaluation(
        freshness_evaluated_at, freshness_max_age_seconds, snapshot=snapshot
    )
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
        if semantic_claim_layer is not None:
            validate_payload(
                dict(semantic_claim_layer),
                "literature_semantic_claim_layer.schema.json",
            )
            if (
                provenance.get("semantic_claim_layer_id")
                != semantic_claim_layer["layer_id"]
                or provenance.get("semantic_claim_layer_digest")
                != semantic_claim_layer["content_digest"]
                or provenance.get("semantic_authority_id")
                != SEMANTIC_CLAIM_AUTHORITY_ID
            ):
                raise ContractError("derived assimilation semantic-layer binding mismatch")
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
                **(
                    {
                        "semantic_claim_id": mapping["semantic_claim_id"],
                        "semantic_relation": mapping["semantic_relation"],
                        "semantic_warrant_digest": mapping["semantic_warrant_digest"],
                    }
                    if "semantic_claim_id" in mapping
                    else {}
                ),
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
    temporal_resolution = _bounded_freshness_fields(
        snapshot, freshness_max_age_seconds, normalized_evaluated_at
    )
    if temporal_resolution:
        freshness, investment_gate, _reason = _freshness_status_at(
            snapshot, temporal_resolution,
            _timestamp(str(temporal_resolution["evaluated_at"])),
        )
    else:
        # Legacy packets retain their historical shape, but the present-use
        # resolver will fail them closed because they lack a bounded window.
        freshness = "current" if snapshot["provenance_mode"] == "live" else "local_only"
        investment_gate = "pass" if freshness == "current" else "blocked_local_only"
    rebase_status = (
        "current"
        if freshness == "current"
        else "provisional_local_only"
        if freshness == "local_only"
        else "stale"
    )
    packet: dict[str, Any] = {
        "schema_version": "4.0" if derivation_replay is not None else ("3.0" if semantic_claim_layer is not None else "2.0"),
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
            "active_investment_gate": investment_gate,
            **temporal_resolution,
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
    if semantic_claim_layer is not None:
        packet["semantic_claim_layer_digest"] = semantic_claim_layer["content_digest"]
        packet["semantic_coverage_audit"] = copy.deepcopy(
            semantic_claim_layer["coverage_audit"]
        )
        packet["explicit_unknowns"].extend(
            f"Semantic relation remains unresolved for claim {claim_id}."
            for claim_id in semantic_claim_layer["coverage_audit"]["unresolved_claim_ids"]
        )
    if derivation_replay is not None:
        packet["derivation_replay"] = copy.deepcopy(dict(derivation_replay))
    packet["content_digest"] = canonical_digest(_without(packet, "content_digest"))
    return packet


def assimilate_literature(
    snapshot: Mapping[str, Any], *, theory_state_digest: str,
    theory_mappings: Sequence[Mapping[str, Any]], hypotheses: Sequence[Mapping[str, Any]] = (),
    prior_snapshot: Mapping[str, Any] | None = None, candidate_snapshot_ids: Sequence[str] = (),
    mapping_provenance: Mapping[str, Any] | None = None, semantic_claim_layer: Mapping[str, Any] | None = None,
    derivation_replay: Mapping[str, Any] | None = None,
    freshness_max_age_seconds: int | None = DEFAULT_LITERATURE_FRESHNESS_SECONDS,
    freshness_evaluated_at: str | datetime | None = None,
) -> dict[str, Any]:
    """Assimilate manually, or emit a standalone-replayable current packet."""

    normalized_evaluated_at = _normalize_freshness_evaluation(
        freshness_evaluated_at, freshness_max_age_seconds, snapshot=snapshot
    )
    packet = _build_assimilation_packet(
        snapshot, theory_state_digest=theory_state_digest, theory_mappings=theory_mappings,
        hypotheses=hypotheses, prior_snapshot=prior_snapshot, candidate_snapshot_ids=candidate_snapshot_ids,
        mapping_provenance=mapping_provenance, semantic_claim_layer=semantic_claim_layer, derivation_replay=derivation_replay,
        freshness_max_age_seconds=freshness_max_age_seconds,
        freshness_evaluated_at=normalized_evaluated_at,
    )
    validate_assimilation(packet, snapshot=snapshot)
    return packet


def validate_assimilation(packet: Mapping[str, Any], *, snapshot: Mapping[str, Any] | None = None) -> None:
    """Reject non-causal bibliographies, wrong-target packets, and novelty laundering."""

    validate_payload(dict(packet), "literature_assimilation_packet.schema.json")
    if packet["content_digest"] != canonical_digest(_without(packet, "content_digest")):
        raise ContractError("literature assimilation content digest mismatch")
    has_temporal_authority = _validate_temporal_resolution(packet)
    if (
        packet["selected_snapshot"]["provenance_mode"]
        == "frozen_response_replay"
        and not has_temporal_authority
    ):
        raise ContractError(
            "frozen-response assimilation requires bounded temporal authority"
        )
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
        if packet["schema_version"] in {"3.0", "4.0"}:
            semantic_digest = packet["semantic_claim_layer_digest"]
            if (
                provenance.get("semantic_claim_layer_digest") != semantic_digest
                or provenance.get("semantic_authority_id")
                != SEMANTIC_CLAIM_AUTHORITY_ID
            ):
                raise ContractError("semantic assimilation lacks exact layer authority")
            audit = packet["semantic_coverage_audit"]
            mappings = packet["theory_mappings"]
            claim_ids = [item.get("semantic_claim_id") for item in mappings]
            if (
                len(set(claim_ids)) != len(claim_ids)
                or audit["claim_record_count"] != len(mappings)
                or audit["explicit_warrant_claim_count"]
                + audit["lexical_fallback_claim_count"]
                != len(mappings)
            ):
                raise ContractError("semantic assimilation coverage cardinality drift")
            unresolved = sorted(
                item["semantic_claim_id"]
                for item in mappings
                if item["semantic_relation"] == "unresolved"
            )
            if audit["unresolved_claim_ids"] != unresolved:
                raise ContractError("semantic assimilation unresolved-claim audit drift")
        if packet["schema_version"] == "4.0":
            replay = packet["derivation_replay"]
            if replay["content_digest"] != canonical_digest(_without(replay, "content_digest")):
                raise ContractError("assimilation derivation replay digest mismatch")
            embedded_snapshot, catalog, derivation = replay["source_snapshot"], replay["theory_catalog"], replay["mapping_derivation"]
            validate_snapshot(embedded_snapshot)
            validate_theory_object_catalog(catalog)
            validate_claim_mapping_derivation(derivation, snapshot=embedded_snapshot, theory_catalog=catalog)
            if replay["prior_snapshot"] is not None:
                validate_snapshot(replay["prior_snapshot"])
            expected_provenance = {
                "mode": "deterministic_claim_derivation", "derivation_id": derivation["derivation_id"],
                "derivation_digest": derivation["content_digest"], "authority_id": derivation["derivation_authority"]["authority_id"],
                "semantic_claim_layer_id": derivation["semantic_claim_layer"]["layer_id"], "semantic_claim_layer_digest": derivation["semantic_claim_layer_digest"],
                "semantic_authority_id": derivation["semantic_claim_layer"]["authority"]["authority_id"],
            }
            expected_packet = _build_assimilation_packet(
                embedded_snapshot, theory_state_digest=catalog["theory_state_digest"], theory_mappings=derivation["theory_mappings"],
                hypotheses=replay["hypothesis_inputs"], prior_snapshot=replay["prior_snapshot"], candidate_snapshot_ids=replay["candidate_snapshot_ids"],
                mapping_provenance=expected_provenance, semantic_claim_layer=derivation["semantic_claim_layer"], derivation_replay=replay,
                freshness_max_age_seconds=replay.get("freshness_max_age_seconds"),
                freshness_evaluated_at=replay.get("freshness_evaluated_at"),
            )
            if dict(packet) != expected_packet:
                raise ContractError("standalone semantic assimilation does not replay from embedded inputs")
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
        if packet["schema_version"] in {"3.0", "4.0"}:
            sources = {item["source_id"]: item for item in snapshot["sources"]}
            for mapping in packet["theory_mappings"]:
                source = sources[mapping["source_id"]]
                if (
                    mapping["source_version"] != source["source_version"]
                    or mapping["source_correction_status"]
                    != source["correction_status"]
                ):
                    raise ContractError(
                        "semantic assimilation mapping crossed source version/correction state"
                    )
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
    "CLAIM_ORIGINS",
    "LANE_TYPES",
    "LITERATURE_REPLAY_OPERATIONS",
    "SEMANTIC_CLAIM_ALGORITHM_ID",
    "SEMANTIC_CLAIM_AUTHORITY_ID",
    "SEMANTIC_CONTRACT_VERSION",
    "SEMANTIC_RELATIONS",
    "DEFAULT_LITERATURE_FRESHNESS_SECONDS",
    "LITERATURE_FRESHNESS_POLICY",
    "assimilate_literature",
    "assimilate_derived_literature",
    "build_theory_object_catalog",
    "bind_source_semantic_warrants",
    "build_semantic_claim_layer",
    "build_demo_literature_snapshot",
    "derive_claim_mappings",
    "rebase_surviving_branches",
    "replay_literature_counterfactuals",
    "resolve_present_literature_freshness",
    "run_frontier_literature_cycle",
    "select_newest_snapshot",
    "validate_assimilation",
    "validate_claim_mapping_derivation",
    "validate_literature_counterfactual_replay",
    "validate_snapshot",
    "validate_semantic_claim_layer",
    "validate_theory_object_catalog",
]
