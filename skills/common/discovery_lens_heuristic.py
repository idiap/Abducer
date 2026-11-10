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

"""Heuristics for routing discovery into category-theoretic or HoTT lenses."""

from __future__ import annotations

from typing import Any


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _text_blob(rows: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for row in rows:
        parts.extend(
            [
                _clean_text(row.get("required_move")),
                _clean_text(row.get("abstraction_required")),
                _clean_text(row.get("minimal_theorem_shape")),
                _clean_text(row.get("obstruction_class")),
                _clean_text(row.get("breakthrough_family")),
            ]
        )
        parts.extend(_clean_text(value) for value in _ensure_list(row.get("search_modes")))
        parts.extend(_clean_text(value) for value in _ensure_list(row.get("sample_theorem_targets")))
    return " ".join(part for part in parts if part).lower()


def _family_set(rows: list[dict[str, Any]]) -> set[str]:
    return {
        _clean_text(row.get("breakthrough_family"))
        for row in rows
        if _clean_text(row.get("breakthrough_family"))
    }


def _queue_stats(rows: list[dict[str, Any]]) -> tuple[int, int]:
    counts: dict[str, int] = {}
    for row in rows:
        for queue_id in [_clean_text(value) for value in _ensure_list(row.get("queue_ids")) if _clean_text(value)]:
            counts[queue_id] = counts.get(queue_id, 0) + 1
    distinct = len(counts)
    overlap = sum(1 for value in counts.values() if value > 1)
    return distinct, overlap


def _criterion(criterion_id: str, active: bool, detail: str) -> dict[str, Any]:
    return {
        "criterion_id": _clean_text(criterion_id),
        "active": bool(active),
        "detail": _clean_text(detail),
    }


def _anti_trigger(trigger_id: str, active: bool, detail: str) -> dict[str, Any]:
    return {
        "trigger_id": _clean_text(trigger_id),
        "active": bool(active),
        "detail": _clean_text(detail),
    }


def _active_count(criteria: list[dict[str, Any]]) -> int:
    return sum(1 for row in criteria if bool(row.get("active")))


def build_categorical_pathway_heuristic(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Decide whether the frontier should be reframed through category-theoretic structure."""

    blob = _text_blob(rows)
    families = _family_set(rows)
    distinct_queue_count, overlap_queue_count = _queue_stats(rows)

    multiple_representations = any(
        token in blob
        for token in {
            "representation",
            "object class",
            "correspondence",
            "normal form",
            "translation",
            "reformulation",
        }
    )
    transport_or_morphism_pressure = any(
        token in blob
        for token in {
            "transport",
            "transfer",
            "formula-size",
            "model shift",
            "compilation",
            "alignment",
        }
    )
    compositional_pressure = len(families & {
        "realization",
        "transport",
        "alignment",
        "semantic bridge",
        "barrier-aware transfer",
        "constructive instantiation",
        "bridge-specificity",
    }) >= 2 or overlap_queue_count > 0 or distinct_queue_count >= 3
    mediation_or_universal_need = any(
        token in blob
        for token in {
            "mediate",
            "mediating",
            "universal",
            "factor",
            "activation",
            "induces",
            "hypotheses",
            "correspondence theorem",
        }
    )
    structural_failure_pressure = any(
        token in blob
        for token in {
            "target-alignment",
            "formula-size-transport",
            "characterization-bridge",
            "general-magnification",
            "local-reduction-barrier",
        }
    )

    criteria = [
        _criterion(
            "multiple_representations",
            multiple_representations,
            "There are multiple representations, object classes, or normal forms that need a structured correspondence.",
        ),
        _criterion(
            "transport_or_morphism_pressure",
            transport_or_morphism_pressure,
            "The frontier includes transport, transfer, or interface claims that look like morphism-level obligations.",
        ),
        _criterion(
            "compositional_pressure",
            compositional_pressure,
            "Several routes or route fragments need to compose, factor, or share a structural interface.",
        ),
        _criterion(
            "mediation_or_universal_need",
            mediation_or_universal_need,
            "The missing move looks like a mediating object, factorization, or universal-property problem.",
        ),
        _criterion(
            "structural_failure_pressure",
            structural_failure_pressure,
            "The blocked frontier already names structural failures such as alignment, transport, or characterization gaps.",
        ),
    ]

    purely_constructional = families <= {"realization", "constructive instantiation", "explicitness"} and not multiple_representations and not transport_or_morphism_pressure
    too_local = distinct_queue_count < 2 and len(families) <= 1
    anti_triggers = [
        _anti_trigger(
            "purely_constructional_frontier",
            purely_constructional,
            "The frontier is still mainly about constructing one object rather than composing interfaces.",
        ),
        _anti_trigger(
            "too_local_for_structural_reframing",
            too_local,
            "There is not yet enough multi-route or multi-representation pressure to justify a categorical reframing.",
        ),
    ]

    score = _active_count(criteria)
    threshold = 3
    recommended = score >= threshold and not all(trigger["active"] for trigger in anti_triggers)
    active_criteria = [row["criterion_id"] for row in criteria if row["active"]]
    active_anti = [row["trigger_id"] for row in anti_triggers if row["active"]]
    rationale = (
        "Route to category theory when the discovery problem is structurally about composition, mediation, and non-commuting interfaces rather than about one isolated construction."
        if recommended
        else "Do not route to category theory yet; the current frontier is still too local or too construction-heavy for a structural/compositional reframing to pay off."
    )

    return {
        "lens_id": "categorical-reframing",
        "recommended": recommended,
        "score": score,
        "threshold": threshold,
        "criteria": criteria,
        "anti_triggers": anti_triggers,
        "matched_family_count": len(families),
        "distinct_queue_count": distinct_queue_count,
        "overlap_queue_count": overlap_queue_count,
        "active_criteria": active_criteria,
        "active_anti_triggers": active_anti,
        "decision_rule": "Route to the categorical pathway only if at least three structural-composition criteria are active and the frontier is not merely a single local construction problem.",
        "rationale": rationale,
    }


def build_hott_pathway_heuristic(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Decide whether the frontier should be reframed through equivalence/coherence structure."""

    blob = _text_blob(rows)
    families = _family_set(rows)
    distinct_queue_count, overlap_queue_count = _queue_stats(rows)

    representation_identity_pressure = any(
        token in blob
        for token in {
            "equivalence",
            "same",
            "representation",
            "normal form",
            "correspondence",
            "identity",
            "object class",
        }
    )
    transport_coherence_pressure = any(
        token in blob
        for token in {
            "transport",
            "coherence",
            "alignment",
            "invariant",
            "object class",
        }
    )
    multiple_operationalizations = len(families & {
        "alignment",
        "realization",
        "explicitness",
        "semantic bridge",
        "transport",
    }) >= 2 or overlap_queue_count > 0
    identity_vs_equivalence_risk = any(
        token in blob
        for token in {
            "carrier-realization",
            "target-alignment",
            "characterization-bridge",
            "equivalent",
            "identical",
            "analogous",
            "interchangeable",
        }
    )
    transportability_need = any(
        token in blob
        for token in {
            "transport law",
            "preserve invariant",
            "coherence",
            "reformulation",
            "normal form",
        }
    )

    criteria = [
        _criterion(
            "representation_identity_pressure",
            representation_identity_pressure,
            "The frontier is asking whether two formulations are the same, equivalent, or only analogous.",
        ),
        _criterion(
            "transport_coherence_pressure",
            transport_coherence_pressure,
            "The route depends on transporting invariants or claims across an equivalence or representation shift.",
        ),
        _criterion(
            "multiple_operationalizations",
            multiple_operationalizations,
            "Several operationalizations or route interfaces are live at once, so sameness and interoperability matter.",
        ),
        _criterion(
            "identity_vs_equivalence_risk",
            identity_vs_equivalence_risk,
            "The frontier risks confusing strict identity with weaker equivalence or analogy.",
        ),
        _criterion(
            "transportability_need",
            transportability_need,
            "Discovery needs a principled account of what transports, what fails to transport, and where coherence breaks.",
        ),
    ]

    purely_bound_or_constructional = families <= {"realization", "constructive instantiation", "explicitness"} and not representation_identity_pressure and not transport_coherence_pressure
    too_local = distinct_queue_count < 2 and len(families) <= 1
    anti_triggers = [
        _anti_trigger(
            "purely_constructional_frontier",
            purely_bound_or_constructional,
            "The frontier is still about constructing or bounding an object, not about equivalence or coherence between formulations.",
        ),
        _anti_trigger(
            "too_local_for_equivalence_reframing",
            too_local,
            "There is not yet enough representational ambiguity or multi-route pressure to justify a HoTT-style reframing.",
        ),
    ]

    score = _active_count(criteria)
    threshold = 3
    recommended = score >= threshold and not all(trigger["active"] for trigger in anti_triggers)
    active_criteria = [row["criterion_id"] for row in criteria if row["active"]]
    active_anti = [row["trigger_id"] for row in anti_triggers if row["active"]]
    rationale = (
        "Route to the HoTT lens when the discovery burden is really about equivalence, transport, and coherence between live formulations."
        if recommended
        else "Do not route to the HoTT lens yet; the frontier does not yet show enough identity/equivalence or transport-coherence pressure."
    )

    return {
        "lens_id": "equivalence-coherence-reframing",
        "recommended": recommended,
        "score": score,
        "threshold": threshold,
        "criteria": criteria,
        "anti_triggers": anti_triggers,
        "matched_family_count": len(families),
        "distinct_queue_count": distinct_queue_count,
        "overlap_queue_count": overlap_queue_count,
        "active_criteria": active_criteria,
        "active_anti_triggers": active_anti,
        "decision_rule": "Route to the HoTT pathway only if at least three equivalence/coherence criteria are active and the frontier is not merely a single local construction task.",
        "rationale": rationale,
    }
