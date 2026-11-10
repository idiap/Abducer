# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Shared helpers for persistent search-space tree signatures and history."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


_SPACE_RE = re.compile(r"\s+")


def _clean_text(value: Any, fallback: str = "") -> str:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Stable normalization of search-space dimension labels.
    Contribution: Keeps route signatures and persisted state deterministic across runs.
    """

    text = str(value or "").strip()
    if not text:
        return fallback
    return _SPACE_RE.sub(" ", text)


def build_route_dimensions(
    *,
    source_statement_id: str,
    target_statement_id: str,
    bridge_type: str,
    statement_delta: dict[str, Any] | None = None,
    inferential_commitment: dict[str, Any] | None = None,
    bridge_object_label: str = "",
    carrier_kind: str = "",
) -> dict[str, str]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Canonicalization of the explored mathematical dimensions of a route.
    Contribution: Makes later search-space persistence and revisit detection stable across stages.
    """

    delta = statement_delta if isinstance(statement_delta, dict) else {}
    commitment = inferential_commitment if isinstance(inferential_commitment, dict) else {}
    source_problem = _clean_text(delta.get("source_problem_family"), "unspecified")
    target_problem = _clean_text(delta.get("target_problem_family"), "unspecified")
    model_shift = _clean_text(delta.get("model_shift"), "model shift not yet typed")
    target_payoff = _clean_text(
        commitment.get("target_consequence_schema") or delta.get("target_claim_focus"),
        "target payoff not yet typed",
    )
    invariant = _clean_text(commitment.get("preserved_invariant"), "support-to-target interface")
    typed_object = _clean_text(
        bridge_object_label or delta.get("typed_object_expectation"),
        "bridge object not yet typed",
    )
    route_label = _clean_text(
        delta.get("route_synopsis"),
        f"{_clean_text(source_statement_id)} -> {_clean_text(target_statement_id)}",
    )
    return {
        "source_statement_id": _clean_text(source_statement_id),
        "target_statement_id": _clean_text(target_statement_id),
        "bridge_type": _clean_text(bridge_type, "structural route"),
        "source_problem_family": source_problem,
        "target_problem_family": target_problem,
        "model_shift": model_shift,
        "target_payoff": target_payoff,
        "preserved_invariant": invariant,
        "typed_object": typed_object,
        "carrier_kind": _clean_text(carrier_kind),
        "route_label": route_label,
    }


def route_signature(dimensions: dict[str, Any]) -> str:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Stable identifier for a route-level search branch.
    Contribution: Allows repeated runs to match the same conceptual branch even when local IDs or ordering change.
    """

    canonical = {
        "source_statement_id": _clean_text(dimensions.get("source_statement_id")),
        "target_statement_id": _clean_text(dimensions.get("target_statement_id")),
        "bridge_type": _clean_text(dimensions.get("bridge_type")),
        "source_problem_family": _clean_text(dimensions.get("source_problem_family")),
        "target_problem_family": _clean_text(dimensions.get("target_problem_family")),
        "model_shift": _clean_text(dimensions.get("model_shift")),
        "target_payoff": _clean_text(dimensions.get("target_payoff")),
        "preserved_invariant": _clean_text(dimensions.get("preserved_invariant")),
    }
    payload = json.dumps(canonical, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:16]
    return f"route.{digest}"


def route_content_fingerprint(
    *,
    route_signature_value: str,
    statement_delta: dict[str, Any] | None = None,
    bridge_object_label: str = "",
    carrier_kind: str = "",
    proof_family: str = "",
) -> str:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Stable content fingerprint for one route realization.
    Contribution: Distinguishes a genuinely changed route formulation from a repeated pass over the same content.
    """

    delta = statement_delta if isinstance(statement_delta, dict) else {}
    canonical = {
        "route_signature": _clean_text(route_signature_value),
        "source_claim_focus": _clean_text(delta.get("source_claim_focus")),
        "target_claim_focus": _clean_text(delta.get("target_claim_focus")),
        "typed_object_expectation": _clean_text(delta.get("typed_object_expectation")),
        "missing_witness_or_transport": _clean_text(delta.get("missing_witness_or_transport")),
        "bridge_object_label": _clean_text(bridge_object_label),
        "carrier_kind": _clean_text(carrier_kind),
        "proof_family": _clean_text(proof_family),
    }
    payload = json.dumps(canonical, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:16]


def default_search_space_state(kb_ref: str = "") -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Construction of a stable empty persistent search-state object.
    Contribution: Lets stages load absent or malformed state files without special-case branching.
    """

    return {
        "metadata": {
            "state_version": 1,
            "kb_ref": _clean_text(kb_ref),
            "created_utc": "",
            "updated_utc": "",
            "run_count": 0,
            "branch_count": 0,
        },
        "branches": {},
    }


def load_search_space_state(path: Path, kb_ref: str = "") -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Safe loading of persisted search-space history.
    Contribution: Prevents downstream exploration stages from failing on first run or on malformed cache files.
    """

    if not path.exists():
        return default_search_space_state(kb_ref)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default_search_space_state(kb_ref)
    if not isinstance(payload, dict):
        return default_search_space_state(kb_ref)
    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    branches = payload.get("branches") if isinstance(payload.get("branches"), dict) else {}
    state = default_search_space_state(kb_ref or str(metadata.get("kb_ref", "")).strip())
    state["metadata"].update({str(k): v for k, v in metadata.items()})
    state["branches"] = {str(k): v for k, v in branches.items() if isinstance(v, dict)}
    state["metadata"]["branch_count"] = len(state["branches"])
    return state


def compute_revisit_signal(history: dict[str, Any] | None, content_fingerprint: str) -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Revisit-aware novelty estimate over a persisted route branch.
    Contribution: Gives planners a stable way to deprioritize stale branches without hiding them.
    """

    row = history if isinstance(history, dict) else {}
    visit_count = int(row.get("visit_count", 0) or 0)
    prior_outcome = _clean_text(row.get("latest_outcome"))
    prior_fingerprint = _clean_text(row.get("content_fingerprint"))
    same_content = bool(prior_fingerprint and prior_fingerprint == _clean_text(content_fingerprint))
    if visit_count <= 0:
        novelty_signal = 1.0
        revisit_status = "new-route"
    elif prior_outcome in {"stalled", "underspecified"}:
        novelty_signal = 0.38 if same_content else 0.74
        revisit_status = "revisited-stalled"
    elif prior_outcome == "refuted":
        novelty_signal = 0.24 if same_content else 0.58
        revisit_status = "revisited-refuted"
    elif prior_outcome == "promising":
        novelty_signal = 0.52 if same_content else 0.84
        revisit_status = "revisited-promising"
    else:
        novelty_signal = 0.58 if same_content else 0.82
        revisit_status = "revisited-open"
    score_multiplier = round(0.65 + 0.35 * novelty_signal, 4)
    return {
        "visit_count": visit_count,
        "prior_outcome": prior_outcome or "unseen",
        "same_content": same_content,
        "novelty_signal": round(novelty_signal, 4),
        "revisit_penalty": round(max(0.0, 1.0 - novelty_signal), 4),
        "score_multiplier": score_multiplier,
        "revisit_status": revisit_status,
        "last_seen_run_id": _clean_text(row.get("last_seen_run_id")),
    }
