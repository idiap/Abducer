# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Shared normalization helpers for expert-grade theorem packets."""

from __future__ import annotations

import re
from typing import Any


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _unique_texts(values: list[Any]) -> list[str]:
    rows: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = _clean_text(value)
        if not text or text in seen:
            continue
        seen.add(text)
        rows.append(text)
    return rows


def _sanitize_id(value: Any) -> str:
    text = _clean_text(value).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-")


def _canonical_mode(value: Any) -> str:
    normalized = _sanitize_id(value)
    aliases = {
        "transport": "transport-lemma",
        "equivalence-transport": "equivalence-theorem",
        "equivalence": "equivalence-theorem",
        "barrier": "no-go-theorem",
        "no-go": "no-go-theorem",
        "constructive-realization": "special-case",
        "invariant-realization": "special-case",
        "constructive-instantiation": "special-case",
    }
    return aliases.get(normalized, normalized)


def _default_strategy_family(*, mode: str, target_id: str) -> str:
    if mode == "transport-lemma":
        return "transport"
    if mode == "equivalence-theorem":
        return "equivalence-transport"
    if mode == "no-go-theorem":
        return "barrier"
    if mode == "threshold-version":
        return "threshold-localization"
    target = _sanitize_id(target_id)
    if target == "invariant-discovery":
        return "invariant-realization"
    if target == "constructive-instantiation":
        return "constructive-instantiation"
    return "constructive-realization"


def _default_negative_route(*, mode: str, bridge_name: str, invariant: str) -> str:
    name = _clean_text(bridge_name) or "the bridge object"
    inv = _clean_text(invariant)
    if mode == "transport-lemma":
        if inv:
            return _clean_text(f"Assume the transport through `{name}` fails to preserve `{inv}`.")
        return _clean_text(f"Assume the transport through `{name}` fails in the intended transfer.")
    if mode == "equivalence-theorem":
        return _clean_text(f"Assume no equivalence witness for `{name}` aligns the route-side and target-side objects.")
    if mode == "no-go-theorem":
        return _clean_text(f"Assume every attempted realization of `{name}` collapses into the current barrier.")
    if mode == "threshold-version":
        if inv:
            return _clean_text(f"Assume no threshold-localized version of `{name}` preserves `{inv}` strongly enough for the restricted target.")
        return _clean_text(f"Assume no threshold-localized version of `{name}` is strong enough for the restricted target.")
    if inv:
        return _clean_text(f"Assume `{name}` cannot be realized while preserving `{inv}` strongly enough to activate the local target claim.")
    return _clean_text(f"Assume `{name}` cannot be realized strongly enough to activate the local target claim.")


def _default_failure_diagnosis(
    *,
    mode: str,
    bridge_name: str,
    invariant: str,
    negative_outputs: list[Any],
) -> str:
    name = _clean_text(bridge_name) or "the bridge object"
    inv = _clean_text(invariant)
    lead_negative = _clean_text(negative_outputs[0]) if negative_outputs else ""
    if mode == "transport-lemma":
        base = (
            f"The route fails if `{name}` does not preserve `{inv}` across the intended transfer."
            if inv
            else f"The route fails if `{name}` does not support the intended transport."
        )
    elif mode == "equivalence-theorem":
        base = (
            f"The route fails if no equivalence witness for `{name}` transports `{inv}` to the target-side operationalization."
            if inv
            else f"The route fails if no equivalence witness for `{name}` aligns the route-side and target-side operationalizations."
        )
    elif mode == "no-go-theorem":
        base = f"The route fails if every admissible realization of `{name}` remains trapped behind the current barrier."
    elif mode == "threshold-version":
        base = f"The route fails if no threshold-localized version of `{name}` preserves `{inv}` strongly enough to force the restricted target."
    elif inv:
        base = f"The route fails if `{name}` cannot be realized while preserving `{inv}`."
    else:
        base = f"The route fails if `{name}` cannot be realized as a usable bridge object."
    if lead_negative:
        base = f"{base} Local negative probe: {lead_negative}."
    return _clean_text(base)


def _default_proof_obligations(
    *,
    mode: str,
    bridge_name: str,
    invariant: str,
    first_nontrivial_lemma: dict[str, Any],
    branch_to_definition: dict[str, Any],
) -> list[str]:
    lemma = _ensure_dict(first_nontrivial_lemma)
    branch_defs = _ensure_dict(branch_to_definition)
    obligations = _unique_texts(
        [
            lemma.get("statement"),
            *_ensure_list(branch_defs.get("transport_laws"))[:2],
            *_ensure_list(branch_defs.get("equivalence_claims"))[:1],
            *_ensure_list(branch_defs.get("commutative_diagram_obligations"))[:1],
        ]
    )
    if obligations:
        return obligations[:4]
    name = _clean_text(bridge_name) or "the bridge object"
    inv = _clean_text(invariant)
    if mode == "equivalence-theorem":
        return [_clean_text(f"Build an explicit equivalence witness for `{name}` and show that it preserves `{inv}`.")]
    if mode == "transport-lemma":
        return [_clean_text(f"Show that the transport through `{name}` preserves `{inv}`.")]
    if mode == "threshold-version":
        return [_clean_text(f"Identify a threshold regime where `{name}` already preserves `{inv}` strongly enough to imply the restricted target.")]
    if mode == "no-go-theorem":
        return [_clean_text(f"Show that every admissible realization of `{name}` collapses into the barrier.")]
    if inv:
        return [_clean_text(f"Realize `{name}` while preserving `{inv}` strongly enough to activate the local target claim.")]
    return [_clean_text(f"Realize `{name}` as a usable local bridge object.")]


def _default_candidate_lemmas(
    *,
    mode: str,
    bridge_name: str,
    first_nontrivial_lemma: dict[str, Any],
    branch_to_definition: dict[str, Any],
) -> list[str]:
    lemma = _ensure_dict(first_nontrivial_lemma)
    branch_defs = _ensure_dict(branch_to_definition)
    name = _clean_text(bridge_name) or "bridge object"
    rows = _unique_texts(
        [
            lemma.get("title"),
            *_ensure_list(branch_defs.get("candidate_lemmas")),
            f"Equivalence transport lemma for {name}" if _ensure_list(branch_defs.get("equivalence_claims")) else "",
            f"Coherence diagram lemma for {name}" if _ensure_list(branch_defs.get("commutative_diagram_obligations")) else "",
            f"Threshold localization lemma for {name}" if mode == "threshold-version" else "",
            f"Barrier obstruction lemma for {name}" if mode == "no-go-theorem" else "",
        ]
    )
    if rows:
        return rows[:4]
    fallback = _clean_text(lemma.get("statement"))
    if fallback:
        return [fallback]
    return [_clean_text(f"Route lemma for {name}")]


def normalize_expert_packet_fields(
    *,
    mode: Any,
    target_id: Any = "",
    bridge_name: Any = "",
    invariant: Any = "",
    first_nontrivial_lemma: dict[str, Any] | None = None,
    negative_barrier_version: Any = "",
    branch_to_definition: dict[str, Any] | None = None,
    proof_strategy_family: Any = "",
    negative_route: Any = "",
    failure_diagnosis: Any = "",
    proof_obligations: Any = None,
    candidate_lemmas: Any = None,
    negative_outputs: Any = None,
) -> dict[str, Any]:
    normalized_mode = _canonical_mode(mode)
    bridge = _clean_text(bridge_name)
    inv = _clean_text(invariant)
    lemma = _ensure_dict(first_nontrivial_lemma)
    branch_defs = _ensure_dict(branch_to_definition)
    negative_rows = _ensure_list(negative_outputs)
    obligations = _unique_texts(_ensure_list(proof_obligations))
    lemmas = _unique_texts(_ensure_list(candidate_lemmas))
    return {
        "proof_strategy_family": _clean_text(proof_strategy_family) or _default_strategy_family(mode=normalized_mode, target_id=_clean_text(target_id)),
        "negative_route": _clean_text(negative_route) or _default_negative_route(mode=normalized_mode, bridge_name=bridge, invariant=inv),
        "failure_diagnosis": _clean_text(failure_diagnosis) or _default_failure_diagnosis(
            mode=normalized_mode,
            bridge_name=bridge,
            invariant=inv,
            negative_outputs=negative_rows,
        ),
        "proof_obligations": obligations or _default_proof_obligations(
            mode=normalized_mode,
            bridge_name=bridge,
            invariant=inv,
            first_nontrivial_lemma=lemma,
            branch_to_definition=branch_defs,
        ),
        "candidate_lemmas": lemmas or _default_candidate_lemmas(
            mode=normalized_mode,
            bridge_name=bridge,
            first_nontrivial_lemma=lemma,
            branch_to_definition=branch_defs,
        ),
    }
