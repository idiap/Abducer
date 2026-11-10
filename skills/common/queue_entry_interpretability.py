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

"""Assess whether a proof-queue entry is self-contained enough for LLM use."""

from __future__ import annotations

import re
from typing import Any

from inference_diagnosis import build_queue_inference_diagnosis


CONTRACT_VERSION = 2

_TRUNCATION_RE = re.compile(r"\.\.\.|…|tokens truncated|truncated", re.IGNORECASE)
_GENERIC_CONTEXT_RE = re.compile(r"\b(?:unspecified|underspecified|unknown|not yet typed)\b", re.IGNORECASE)
_HARD_SCHEMA_PLACEHOLDER_PATTERNS = (
    re.compile(r"\bif source theorem\s+[A-Z](?:['0-9]+)?\s+holds in regime\s+[A-Z](?:['0-9]+)?\b", re.IGNORECASE),
    re.compile(r"\b(?:source theorem|target theorem|local activation theorem|real theorem under search|theorem under search)\s+[A-Z](?:['0-9]+)?\b", re.IGNORECASE),
    re.compile(r"\btarget theorem\s+[A-Z](?:['0-9]+)?\s+is fixed\b", re.IGNORECASE),
    re.compile(r"\bfrom abstract schema\s+[A-Z](?:['0-9]+)?\b", re.IGNORECASE),
    re.compile(r"\blocal definitional object\s+[A-Z](?:['0-9]+)?\s+has property\s+[A-Z](?:['0-9]+)?\b", re.IGNORECASE),
    re.compile(r"\bif semantic object\s+[A-Z](?:['0-9]+)?\s+exists\b", re.IGNORECASE),
)
_SCHEMA_TOKEN_PATTERNS = (
    re.compile(r"\b(?:carrier|object|family|map|problem|regime|invariant|property|condition|bounds?|structure|measure|theorem|lemma)\s+([A-Z](?:['0-9]+)?)\b"),
    re.compile(r"\b([A-Z](?:['0-9]+)?)\s+in the [a-z-]+ regime\b"),
)
_GENERIC_OBJECT_PATTERNS = (
    re.compile(r"^(?:an? |the )?(?:candidate )?(?:bridge )?object$", re.IGNORECASE),
    re.compile(r"^(?:unspecified|underspecified|unknown)\b", re.IGNORECASE),
)


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _append_unique(rows: list[str], text: str) -> None:
    cleaned = _clean_text(text)
    if cleaned and cleaned not in rows:
        rows.append(cleaned)


def _has_schema_placeholder(text: str, *, field: str = "") -> bool:
    cleaned = _clean_text(text)
    if not cleaned:
        return False
    if any(pattern.search(cleaned) for pattern in _HARD_SCHEMA_PLACEHOLDER_PATTERNS):
        return True
    tokens: set[str] = set()
    for pattern in _SCHEMA_TOKEN_PATTERNS:
        tokens.update(match.group(1) for match in pattern.finditer(cleaned))
    if not tokens:
        return False
    # Real theorem excerpts often contain one symbolic parameter (for example Q),
    # which should not by itself force a defer diagnosis.
    return len(tokens) >= 2


def _field_texts(entry: dict[str, Any]) -> dict[str, str]:
    delta = _ensure_dict(entry.get("statement_delta"))
    return {
        "title": _clean_text(entry.get("title")),
        "claim_text": _clean_text(entry.get("claim_text")),
        "conjecture_statement": _clean_text(entry.get("conjecture_statement")),
        "route_synopsis": _clean_text(entry.get("route_synopsis")),
        "missing_route_lemma": _clean_text(entry.get("missing_route_lemma")),
        "conditional_proposition": _clean_text(entry.get("conditional_proposition")),
        "source_excerpt": _clean_text(entry.get("source_excerpt")),
        "target_excerpt": _clean_text(entry.get("target_excerpt")),
        "candidate_object": _clean_text(entry.get("candidate_object")),
        "carrier_kind": _clean_text(entry.get("carrier_kind")),
        "preserved_invariant": _clean_text(entry.get("preserved_invariant")),
        "negative_route": _clean_text(entry.get("negative_route")),
        "failure_diagnosis": _clean_text(entry.get("failure_diagnosis")),
        "delta_source_focus": _clean_text(delta.get("source_claim_focus")),
        "delta_target_focus": _clean_text(delta.get("target_claim_focus")),
        "delta_model_shift": _clean_text(delta.get("model_shift")),
        "delta_typing_status": _clean_text(delta.get("typing_status")),
    }


def assess_queue_entry_interpretability(entry: dict[str, Any]) -> dict[str, Any]:
    """Return a portable interpretability contract for a proof-queue entry."""

    texts = _field_texts(entry)
    blockers: list[str] = []
    warnings: list[str] = []
    strengths: list[str] = []

    core_fields = (
        "claim_text",
        "conjecture_statement",
        "route_synopsis",
        "missing_route_lemma",
        "conditional_proposition",
        "source_excerpt",
        "target_excerpt",
        "delta_source_focus",
        "delta_target_focus",
    )
    for field in core_fields:
        text = texts[field]
        if text and _TRUNCATION_RE.search(text):
            _append_unique(blockers, f"`{field}` contains truncation markers, so the theorem state is not self-contained.")
        if text and _has_schema_placeholder(text, field=field):
            _append_unique(blockers, f"`{field}` still uses schema placeholders instead of concrete mathematical content.")

    title = texts["title"]
    if title and _TRUNCATION_RE.search(title):
        _append_unique(warnings, "`title` is truncated, so the queue overview is harder to scan.")

    candidate_object = texts["candidate_object"]
    if candidate_object:
        if any(pattern.search(candidate_object) for pattern in _GENERIC_OBJECT_PATTERNS):
            _append_unique(blockers, "`candidate_object` is generic or explicitly underspecified.")
    else:
        _append_unique(warnings, "`candidate_object` is empty, so the bridge carrier is implicit.")

    for field in ("carrier_kind", "preserved_invariant", "delta_model_shift", "delta_typing_status"):
        text = texts[field]
        if text and _GENERIC_CONTEXT_RE.search(text):
            _append_unique(blockers, f"`{field}` is still marked as unspecified or not yet typed.")

    if not _clean_text(entry.get("source_statement_id")) and not texts["source_excerpt"]:
        _append_unique(blockers, "The source theorem is missing both a statement id and a theorem excerpt.")
    if not _clean_text(entry.get("target_statement_id")) and not texts["target_excerpt"]:
        _append_unique(blockers, "The target theorem is missing both a statement id and a theorem excerpt.")

    if not texts["source_excerpt"]:
        _append_unique(warnings, "`source_excerpt` is empty, so source-side premises must be recovered indirectly.")
    if not texts["target_excerpt"]:
        _append_unique(warnings, "`target_excerpt` is empty, so the target theorem body is not restated locally.")
    if not texts["missing_route_lemma"]:
        _append_unique(warnings, "`missing_route_lemma` is empty, so the next inference step is not crisply named.")
    if not texts["route_synopsis"]:
        _append_unique(warnings, "`route_synopsis` is empty, so the bridge move is not summarized locally.")
    if not _clean_text(entry.get("proof_strategy_family")):
        _append_unique(warnings, "`proof_strategy_family` is empty, so the intended proof mode is not explicit.")
    if not texts["negative_route"]:
        _append_unique(warnings, "`negative_route` is empty, so the barrier branch is not normalized.")
    if not _ensure_list(entry.get("proof_obligations")) and not _ensure_list(entry.get("candidate_lemmas")):
        _append_unique(warnings, "No proof obligations or candidate lemmas are listed yet.")

    if _clean_text(entry.get("source_statement_id")) and texts["source_excerpt"]:
        _append_unique(strengths, "The source theorem is grounded by both an id and a local excerpt.")
    if _clean_text(entry.get("target_statement_id")) and texts["target_excerpt"]:
        _append_unique(strengths, "The target theorem is grounded by both an id and a local excerpt.")
    if texts["missing_route_lemma"]:
        _append_unique(strengths, "The route already names a theorem-shaped missing lemma.")
    if candidate_object and not any(pattern.search(candidate_object) for pattern in _GENERIC_OBJECT_PATTERNS):
        _append_unique(strengths, "The bridge object has a stable local name.")

    blocker_penalty = 25 * len(blockers)
    warning_penalty = 8 * len(warnings)
    score = max(0, 100 - blocker_penalty - warning_penalty)
    ready = not blockers
    summary = (
        "Queue entry is self-contained enough for LLM proof work."
        if ready
        else "Defer until re-encoded: " + " ".join(blockers[:2])
    )
    diagnosis = build_queue_inference_diagnosis(entry, contract={
        "blockers": blockers,
        "warnings": warnings,
        "strengths": strengths,
    })
    return {
        "version": CONTRACT_VERSION,
        "status": "ready" if ready else "defer",
        "ready": ready,
        "self_contained": ready,
        "score": score,
        "summary": summary,
        "blockers": blockers,
        "warnings": warnings,
        "strengths": strengths,
        "checked_fields": sorted(texts),
        "inference_diagnosis": diagnosis,
    }
