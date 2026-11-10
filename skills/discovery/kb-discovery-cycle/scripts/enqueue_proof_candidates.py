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

"""Populate the persistent proof queue from discovery-stage artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
_BREAKTHROUGH_SCRIPT_DIR = Path(__file__).resolve().parents[3] / "evaluation" / "kb-discovery-breakthrough-profiler" / "scripts"
_PROVE_SCRIPT_DIR = Path(__file__).resolve().parents[3] / "discovery" / "kb-prove-cycle" / "scripts"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))
if str(_BREAKTHROUGH_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_BREAKTHROUGH_SCRIPT_DIR))
if str(_PROVE_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_PROVE_SCRIPT_DIR))

from generate_discovery_breakthrough_profile import build_report as build_breakthrough_report
from generate_discovery_breakthrough_profile import build_discovery_lens_artifacts
from generate_discovery_breakthrough_profile import build_expanded_prompt_pack as build_breakthrough_prompt_pack
from generate_discovery_breakthrough_profile import compile_pdf as compile_breakthrough_pdf
from generate_discovery_breakthrough_profile import build_discovery_pattern_routing
from generate_discovery_breakthrough_profile import render_discovery_lens_artifacts_markdown
from generate_discovery_breakthrough_profile import render_discovery_lens_artifacts_tex
from generate_discovery_breakthrough_profile import render_markdown as render_breakthrough_markdown
from generate_discovery_breakthrough_profile import render_discovery_pattern_routing_markdown
from generate_discovery_breakthrough_profile import render_discovery_pattern_routing_tex
from generate_discovery_breakthrough_profile import render_prompt_pack_markdown
from generate_discovery_breakthrough_profile import render_prompt_pack_tex
from generate_discovery_breakthrough_profile import render_tex as render_breakthrough_tex
from generate_discovery_breakthrough_profile import spawn_discovery_branches
from kb_context import canonical_artifacts_dir
from kb_context import kb_ref_from_artifacts_dir
from negative_route_heuristic import build_negative_route_heuristic
from problem_mathlib import mathlib_root
from generate_proof_cycle_summary import refresh_summary_from_sources
from proof_queue import enqueue_entries
from proof_queue import load_proof_queue
from proof_queue import make_queue_key
from proof_queue import proof_queue_paths
from proof_queue import save_proof_queue
from reasoning_log import ReasoningLogger


PREFERRED_REPAIR_ABSTRACTION_TYPES = [
    "canonical-obstruction-family",
    "reduction-gadget-family",
    "normal-form-translation",
    "surrogate-promise-problem",
    "algebraic-certificate",
    "pseudorandom-object",
    "proof-potential-measure",
    "intermediate-complexity-measure",
]


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _load_attempt_payload(artifacts_dir: Path, attempt_id: str) -> dict[str, Any]:
    attempt_id = _clean_text(attempt_id)
    if not attempt_id:
        return {}
    return _load_json(artifacts_dir / "proof-attempts" / f"{attempt_id}.json")


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _queue_has_active_entries(queue: dict[str, Any]) -> bool:
    return any(
        isinstance(row, dict) and _clean_text(row.get("status")).lower() in {"pending", "in_progress"}
        for row in _ensure_list(queue.get("entries"))
    )


def _first_nonempty(*values: Any) -> str:
    for value in values:
        text = _clean_text(value)
        if text:
            return text
    return ""


def _bridge_rows(expert: dict[str, Any]) -> list[dict[str, Any]]:
    """Return a deduplicated bridge frontier, backfilling beyond the fixed recommended slice."""
    recommended = [row for row in _ensure_list(expert.get("recommended_bridges")) if isinstance(row, dict)]
    portfolio = [row for row in _ensure_list(expert.get("bridge_portfolio")) if isinstance(row, dict)]
    recommended.sort(key=lambda row: _safe_float(row.get("priority")), reverse=True)
    portfolio.sort(key=lambda row: _safe_float(row.get("priority")), reverse=True)

    rows: list[dict[str, Any]] = []
    seen_bridge_ids: set[str] = set()
    for row in [*recommended, *portfolio]:
        bridge_id = _clean_text(row.get("bridge_id"))
        if not bridge_id or bridge_id in seen_bridge_ids:
            continue
        seen_bridge_ids.add(bridge_id)
        rows.append(row)
    return rows


def _abstraction_rows(gap_abstractions: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        row
        for row in _ensure_list(
            gap_abstractions.get("abstraction_conjectures") or gap_abstractions.get("conjectures")
        )
        if isinstance(row, dict)
    ]


def _search_space_route_index(search_space: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        _clean_text(row.get("bridge_id")): row
        for row in _ensure_list(search_space.get("routes"))
        if isinstance(row, dict) and _clean_text(row.get("bridge_id"))
    }


def _frontier_index(search_space: dict[str, Any]) -> dict[str, dict[str, Any]]:
    frontier = _ensure_dict(search_space.get("frontier"))
    rows = _ensure_list(frontier.get("resume")) + _ensure_list(frontier.get("deprioritized"))
    return {
        _clean_text(row.get("bridge_id")): row
        for row in rows
        if isinstance(row, dict) and _clean_text(row.get("bridge_id"))
    }


def _blocked_bridge_ids(queue: dict[str, Any]) -> list[str]:
    blocked_entries = [
        row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict) and _clean_text(row.get("status")).lower() == "blocked"
    ]
    blocked_entries.sort(key=lambda row: _safe_float(row.get("priority")), reverse=True)
    seen: set[str] = set()
    ordered: list[str] = []
    for row in blocked_entries:
        bridge_id = _clean_text(row.get("bridge_id"))
        if not bridge_id or bridge_id in seen:
            continue
        seen.add(bridge_id)
        ordered.append(bridge_id)
    return ordered


def _blocked_route_entries(queue: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict)
        and _clean_text(row.get("status")).lower() == "blocked"
        and _clean_text(row.get("claim_type")).lower() == "route-conjecture"
    ]
    rows.sort(key=lambda row: _safe_float(row.get("priority")), reverse=True)
    return rows


def _blocked_abstraction_entries(queue: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict)
        and _clean_text(row.get("status")).lower() == "blocked"
        and _clean_text(row.get("claim_type")).lower() == "abstraction-conjecture"
    ]
    rows.sort(key=lambda row: _safe_float(row.get("priority")), reverse=True)
    return rows


def _build_title(bridge: dict[str, Any]) -> str:
    delta = _ensure_dict(bridge.get("statement_delta"))
    abstraction = _first_nonempty(bridge.get("abstraction_label"), bridge.get("bridge_id"))
    target = _first_nonempty(delta.get("target_claim_focus"), bridge.get("target_statement_id"))
    return _clean_text(f"{abstraction}: {target}")


def _build_abstraction_title(conjecture: dict[str, Any]) -> str:
    delta = _ensure_dict(conjecture.get("statement_delta"))
    abstraction = _first_nonempty(conjecture.get("abstraction_label"), conjecture.get("conjecture_id"))
    target = _first_nonempty(delta.get("target_claim_focus"), conjecture.get("to_id"))
    return _clean_text(f"{abstraction}: {target}")


def _build_repair_lemma_title(target: dict[str, Any], focus_label: str) -> str:
    delta = _ensure_dict(target.get("statement_delta"))
    target_focus = _first_nonempty(delta.get("target_claim_focus"), target.get("target_statement_id"))
    return _clean_text(f"{focus_label}: {target_focus}")


def _is_named_value(text: str) -> bool:
    return bool(text) and text.lower() not in {"unspecified", "unknown", "none", "n/a"}


def _with_indefinite_article(text: str) -> str:
    cleaned = _clean_text(text)
    if not cleaned:
        return ""
    lowered = cleaned.lower()
    if lowered.startswith(("a ", "an ", "the ")):
        return cleaned
    article = "an" if lowered[:1] in {"a", "e", "i", "o", "u"} else "a"
    return f"{article} {cleaned}"


def _context_phrase(problem_family: Any, model: Any) -> str:
    problem_text = _clean_text(problem_family)
    model_text = _clean_text(model)
    if _is_named_value(problem_text) and _is_named_value(model_text):
        return f"{problem_text} in {model_text}"
    if _is_named_value(problem_text):
        return problem_text
    if _is_named_value(model_text):
        return model_text
    return ""


def _build_conjecture_statement(bridge: dict[str, Any]) -> tuple[str, str]:
    delta = _ensure_dict(bridge.get("statement_delta"))
    candidate_object = _first_nonempty(
        bridge.get("abstraction_label"),
        bridge.get("carrier_kind"),
        delta.get("typed_object_expectation"),
        bridge.get("bridge_id"),
    )
    if not _is_named_value(candidate_object):
        candidate_object = "candidate bridge object"
    carrier_kind = _clean_text(bridge.get("carrier_kind"))
    source_focus = _first_nonempty(
        delta.get("source_claim_focus"),
        bridge.get("source_excerpt"),
        bridge.get("source_statement_id"),
    )
    target_focus = _first_nonempty(
        delta.get("target_claim_focus"),
        bridge.get("target_excerpt"),
        bridge.get("target_statement_id"),
    )
    preserved_invariant = _clean_text(bridge.get("preserved_invariant"))
    source_context = _context_phrase(delta.get("source_problem_family"), delta.get("source_model")) or "the source regime"
    target_context = _context_phrase(delta.get("target_problem_family"), delta.get("target_model"))
    model_shift = _clean_text(delta.get("model_shift"))

    carrier_clause = f", realized as {_with_indefinite_article(carrier_kind)}," if carrier_kind else ","
    invariant_clause = f" while preserving the invariant {preserved_invariant}" if preserved_invariant else ""
    transport_clause = ""
    if "->" in model_shift:
        transport_clause = f" across the transfer {model_shift}"
    elif target_context and target_context != source_context:
        transport_clause = f" from {source_context} to {target_context}"
    target_context_clause = f" for {target_context}" if target_context and target_context != source_context else ""
    statement = _clean_text(
        f"There exists an admissible {candidate_object}{carrier_clause} such that whenever {source_focus} holds for {source_context},"
        f" the object organizes the source-side mathematical content{invariant_clause}{transport_clause}"
        f" and yields {target_focus}{target_context_clause}."
    )
    return "route-conjecture", statement


def _negative_reasoning_program(
    *,
    candidate_object: str,
    source_focus: str,
    target_focus: str,
    invariant: str,
    negative_route: str,
    failure_diagnosis: str,
    barrier_scope: str = "",
    missing_route_lemma: str = "",
    carrier_kind: str = "",
) -> dict[str, Any]:
    """Build a portable contradiction/impossibility schema for queue items."""

    clean_object = _clean_text(candidate_object) or "candidate bridge object"
    clean_source = _clean_text(source_focus) or "source theorem"
    clean_target = _clean_text(target_focus) or "target consequence"
    clean_invariant = _clean_text(invariant) or "route invariant"
    clean_negative = _clean_text(negative_route)
    clean_failure = _clean_text(failure_diagnosis)
    clean_barrier = _clean_text(barrier_scope)
    clean_missing = _clean_text(missing_route_lemma)

    mode = "obstruction"
    negated_claim = f"Assume the route from `{clean_source}` to `{clean_target}` does not go through `{clean_object}`."
    contradiction_target = (
        f"Show that no admissible realization of `{clean_object}` can preserve `{clean_invariant}` strongly enough to force `{clean_target}`."
    )
    forbidden_outcome = clean_failure or f"`{clean_object}` degenerates into topical overlap rather than theorem-level content."
    impossibility_claim = (
        f"No admissible realization of `{clean_object}` currently supports the full bundle `{clean_source}` + `{clean_invariant}` + `{clean_target}`."
    )

    if clean_barrier and clean_barrier.lower() != "none":
        mode = "barrier-impossibility"
        negated_claim = f"Assume every realization of `{clean_object}` remains trapped inside barrier `{clean_barrier}`."
        contradiction_target = f"Show that the route cannot escape barrier `{clean_barrier}` while preserving `{clean_invariant}`."
        forbidden_outcome = clean_failure or f"All realizations of `{clean_object}` collapse back into barrier `{clean_barrier}`."
        impossibility_claim = (
            f"Every admissible realization of `{clean_object}` in the current encoding remains blocked by barrier `{clean_barrier}` and cannot force `{clean_target}`."
        )
    elif "contradict" in clean_negative.lower() or "collapse" in clean_negative.lower():
        mode = "contradiction"
        negated_claim = f"Assume `{clean_target}` fails despite the route through `{clean_object}`."
        contradiction_target = clean_negative or "Derive a forbidden collapse or contradiction with accepted local mathematics."
        forbidden_outcome = clean_failure or "A forbidden collapse or contradiction appears."
        impossibility_claim = (
            f"If negating `{clean_target}` forces the forbidden outcome, then the route through `{clean_object}` must yield `{clean_target}`."
        )
    elif "transport" in clean_missing.lower() or "transfer" in clean_missing.lower():
        mode = "transport-obstruction"
        negated_claim = f"Assume the transport from `{clean_source}` to `{clean_target}` loses `{clean_invariant}`."
        contradiction_target = clean_missing or "Locate the first transport law whose failure makes the route impossible."
        forbidden_outcome = clean_failure or f"`{clean_invariant}` cannot survive the required transport."
        impossibility_claim = (
            f"No transport map currently known can carry `{clean_source}` to `{clean_target}` while preserving `{clean_invariant}`."
        )
    elif any(token in clean_object.lower() for token in ("obstruction", "witness", "certificate")):
        mode = "non-realization"
        negated_claim = f"Assume `{clean_object}` cannot be realized as a mathematically usable carrier."
        contradiction_target = clean_negative or "Localize failure to carrier realization, witness preservation, or payoff forcing."
        forbidden_outcome = clean_failure or f"`{clean_object}` exists only as a role-description."
        impossibility_claim = (
            f"No admissible carrier realizing `{clean_object}` currently absorbs `{clean_source}`, preserves `{clean_invariant}`, and forces `{clean_target}`."
        )

    heuristic = build_negative_route_heuristic(
        candidate_object=clean_object,
        source_focus=clean_source,
        target_focus=clean_target,
        invariant=clean_invariant,
        negative_route=clean_negative or contradiction_target,
        failure_diagnosis=clean_failure or forbidden_outcome,
        barrier_scope=clean_barrier,
        missing_route_lemma=clean_missing,
        carrier_kind=_clean_text(carrier_kind),
    )

    return {
        "negative_mode": mode,
        "negated_claim": negated_claim,
        "contradiction_target": contradiction_target,
        "forbidden_outcome": forbidden_outcome,
        "impossibility_claim_template": impossibility_claim,
        "designated_negative_route": clean_negative or contradiction_target,
        "failure_value": "A precise negative result would compress the search space and clarify whether the route is impossible as stated.",
        "heuristic": heuristic,
    }


def _repair_abstraction_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    abstraction_type = _clean_text(row.get("abstraction_type"))
    try:
        type_index = PREFERRED_REPAIR_ABSTRACTION_TYPES.index(abstraction_type)
    except ValueError:
        type_index = len(PREFERRED_REPAIR_ABSTRACTION_TYPES)
    label = _clean_text(row.get("abstraction_label")).lower()
    typing_status = _clean_text(row.get("typing_status")).lower()
    named_penalty = 1 if label.startswith("unspecified") else 0
    typed_penalty = 0 if typing_status == "typed" else 1
    return (
        typed_penalty,
        named_penalty,
        type_index,
        -_safe_float(row.get("priority")),
        -_safe_float(row.get("definitional_completeness")),
        -_safe_float(row.get("counterfactual_sharpness")),
    )


def _repair_lemma_spec(attempt: dict[str, Any]) -> dict[str, str]:
    target = _ensure_dict(attempt.get("target"))
    summary = _clean_text(_ensure_dict(attempt.get("final_assessment")).get("summary")).lower()
    result_statement = _clean_text(_ensure_dict(attempt.get("proof_attempt")).get("result_statement"))
    candidate_object = _first_nonempty(target.get("candidate_object"), "candidate bridge object")
    bridge_id = _clean_text(target.get("bridge_id"))
    source_id = _clean_text(target.get("source_statement_id"))
    target_id = _clean_text(target.get("target_statement_id"))
    source_focus = _first_nonempty(_ensure_dict(target.get("statement_delta")).get("source_claim_focus"), source_id)
    target_focus = _first_nonempty(_ensure_dict(target.get("statement_delta")).get("target_claim_focus"), target_id)
    invariant = _clean_text(target.get("preserved_invariant"))
    lemma = _clean_text(target.get("missing_route_lemma"))

    if "formula-size" in summary or "formula-size" in result_statement.lower():
        focus = "Formula-Size Transport Lemma"
        claim = (
            f"Prove a theorem transporting `{candidate_object}` from the nonuniform-circuits regime into the formula-size regime "
            f"while preserving `{invariant}` strongly enough to lift `{source_focus}` into `{target_focus}`."
        )
        diagnosis = (
            "The current route is blocked by a missing cross-model transport theorem, not just by the lack of a named carrier."
        )
    elif "black-box hitting-set" in summary or "pit-derandomization" in summary or "derandomization" in summary:
        focus = "PIT Upgrade Lemma"
        claim = (
            f"Prove an upgrade theorem turning the semantic black-box PIT object behind `{candidate_object}` into an algorithmic "
            f"PIT-derandomization premise strong enough to derive `{target_focus}`."
        )
        diagnosis = "The route is blocked at the semantic-to-algorithmic upgrade from hitting sets or certificates to derandomization."
    elif "local reductions" in summary or "local-reduction" in summary:
        focus = "Local Reduction Gadget Lemma"
        claim = (
            f"Construct and verify an explicit local reduction gadget family witnessing how `{source_focus}` transfers into "
            f"the MCSP local-reduction regime while preserving `{invariant}`."
        )
        diagnosis = "The route is blocked by the absence of an explicit local reduction family realizing the transfer."
    elif "natural np-complete examples" in summary or "concrete natural np-complete examples" in summary:
        focus = "Schema-To-Examples Construction Lemma"
        claim = (
            f"Construct a reduction family that turns the abstract schema `{source_focus}` into concrete natural examples "
            f"realizing `{target_focus}`."
        )
        diagnosis = "The route is blocked by a constructive gap from abstract schema to explicit natural examples."
    elif "generic distinguisher" in summary or "sparse-code" in summary or "general-purpose atserias-muller" in summary.lower():
        focus = "Target Alignment Lemma"
        claim = (
            f"Prove an alignment theorem identifying `{candidate_object}` with the target object class needed to lift "
            f"`{source_focus}` into `{target_focus}`."
        )
        diagnosis = "The route is blocked by object-class mismatch between the MCSP-specific source and the generic target theorem."
    elif "biconditional" in summary or "np=conp" in summary or "cook-reckhow" in summary:
        focus = "Characterization Bridge Lemma"
        claim = (
            f"Prove the semantic bridge needed to turn the definitional source statement `{source_focus}` into the characterization "
            f"`{target_focus}`, rather than only normalizing encodings."
        )
        diagnosis = "The route is blocked by a characterization theorem gap, not by syntax or encoding alone."
    else:
        focus = "Carrier Realization Lemma"
        claim = (
            f"Construct an explicit realization theorem for `{candidate_object}` showing how it absorbs `{source_focus}`, preserves "
            f"`{invariant}`, and materially forces `{target_focus}` on the route `{bridge_id}`."
        )
        diagnosis = "The route is blocked because the stronger carrier is still only a role-description rather than a realized mathematical object."

    return {
        "focus_label": focus,
        "claim_text": _clean_text(claim),
        "diagnosis": diagnosis,
        "result_statement": result_statement,
        "bridge_id": bridge_id,
        "source_id": source_id,
        "target_id": target_id,
        "lemma": lemma,
    }


def _breakthrough_priority_index(
    breakthrough_profile: dict[str, Any] | None,
    queue: dict[str, Any],
) -> dict[str, Any]:
    profiles = [
        row
        for row in _ensure_list(_ensure_dict(breakthrough_profile).get("profiles"))
        if isinstance(row, dict)
    ]
    if not profiles:
        return {"by_queue_id": {}, "by_bridge_id": {}, "family_order": []}

    queue_rows = {
        _clean_text(row.get("queue_id")): row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict) and _clean_text(row.get("queue_id"))
    }
    by_queue_id: dict[str, dict[str, Any]] = {}
    by_bridge_id: dict[str, dict[str, Any]] = {}
    family_order: list[str] = []
    for rank, profile in enumerate(profiles):
        family = _clean_text(profile.get("breakthrough_family")) or "unclassified"
        if family not in family_order:
            family_order.append(family)
        info = {
            "breakthrough_family": family,
            "obstruction_class": _clean_text(profile.get("obstruction_class")),
            "breakthrough_rank": rank,
            "breakthrough_pressure": _safe_float(profile.get("pressure_score")),
            "breakthrough_top_priority": _safe_float(profile.get("top_priority")),
        }
        for queue_id in [_clean_text(value) for value in _ensure_list(profile.get("queue_ids")) if _clean_text(value)]:
            current = by_queue_id.get(queue_id)
            if current is None or int(info["breakthrough_rank"]) < int(current.get("breakthrough_rank", 10**6)):
                by_queue_id[queue_id] = dict(info)
            queue_row = _ensure_dict(queue_rows.get(queue_id))
            bridge_id = _clean_text(queue_row.get("bridge_id"))
            if not bridge_id:
                continue
            current_bridge = by_bridge_id.get(bridge_id)
            if current_bridge is None or int(info["breakthrough_rank"]) < int(current_bridge.get("breakthrough_rank", 10**6)):
                by_bridge_id[bridge_id] = dict(info)
    return {
        "by_queue_id": by_queue_id,
        "by_bridge_id": by_bridge_id,
        "family_order": family_order,
    }


def _annotate_with_breakthrough(entry: dict[str, Any], breakthrough_info: dict[str, Any] | None) -> dict[str, Any]:
    if not breakthrough_info:
        return entry
    annotated = dict(entry)
    annotated["breakthrough_family"] = _clean_text(breakthrough_info.get("breakthrough_family"))
    annotated["obstruction_class"] = _clean_text(breakthrough_info.get("obstruction_class"))
    annotated["breakthrough_rank"] = int(breakthrough_info.get("breakthrough_rank", 0) or 0)
    annotated["breakthrough_pressure"] = _safe_float(breakthrough_info.get("breakthrough_pressure"))
    why_now = [value for value in _ensure_list(annotated.get("why_now")) if _clean_text(value)]
    if annotated["breakthrough_family"]:
        why_now.insert(
            0,
            _clean_text(
                f"This candidate is prioritized under breakthrough family `{annotated['breakthrough_family']}`"
                f" via obstruction `{annotated.get('obstruction_class', '') or 'blocked frontier'}`."
            ),
        )
    annotated["why_now"] = why_now
    return annotated


def _entry_priority_sort_key(entry: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -_safe_float(entry.get("breakthrough_pressure")),
        -_safe_float(entry.get("priority")),
        _clean_text(entry.get("title")).lower(),
    )


def _select_entries_by_breakthrough_family(
    entries: list[dict[str, Any]],
    *,
    breakthrough_index: dict[str, Any],
    top_k: int,
) -> list[dict[str, Any]]:
    if not entries:
        return []

    family_order = [str(value) for value in _ensure_list(breakthrough_index.get("family_order")) if _clean_text(value)]
    if not family_order:
        return sorted(entries, key=_entry_priority_sort_key)[: max(1, top_k)]

    buckets: dict[str, list[dict[str, Any]]] = {}
    family_ranks: dict[str, int] = {}
    for entry in entries:
        family = _clean_text(entry.get("breakthrough_family")) or "unclassified"
        buckets.setdefault(family, []).append(entry)
        family_ranks[family] = min(
            family_ranks.get(family, 10**6),
            int(entry["breakthrough_rank"]) if entry.get("breakthrough_rank") is not None else 10**6,
        )
    for bucket in buckets.values():
        bucket.sort(key=_entry_priority_sort_key)

    ordered_families = sorted(
        buckets.keys(),
        key=lambda family: (
            family_ranks.get(family, 10**6),
            family_order.index(family) if family in family_order else len(family_order),
            family,
        ),
    )
    selected: list[dict[str, Any]] = []
    while len(selected) < max(1, top_k):
        progressed = False
        for family in ordered_families:
            bucket = buckets.get(family, [])
            if not bucket:
                continue
            selected.append(bucket.pop(0))
            progressed = True
            if len(selected) >= max(1, top_k):
                break
        if not progressed:
            break
    return selected


def build_repair_queue_entries(
    *,
    gap_abstractions: dict[str, Any],
    queue: dict[str, Any],
    kb_ref: str,
    breakthrough_profile: dict[str, Any] | None = None,
    top_k: int = 4,
) -> list[dict[str, Any]]:
    blocked_bridge_ids = _blocked_bridge_ids(queue)
    if not blocked_bridge_ids:
        return []

    abstractions_by_bridge: dict[str, list[dict[str, Any]]] = {}
    for row in _abstraction_rows(gap_abstractions):
        bridge_id = _clean_text(row.get("bridge_id"))
        if bridge_id:
            abstractions_by_bridge.setdefault(bridge_id, []).append(row)

    breakthrough_index = _breakthrough_priority_index(breakthrough_profile, queue)
    entries: list[dict[str, Any]] = []
    for bridge_id in blocked_bridge_ids:
        candidates = abstractions_by_bridge.get(bridge_id, [])
        if not candidates:
            continue
        best = sorted(candidates, key=_repair_abstraction_sort_key)[0]
        mathematical_spec = _ensure_dict(best.get("mathematical_specification"))
        delta = _ensure_dict(best.get("statement_delta")) or _ensure_dict(mathematical_spec.get("statement_delta"))
        definitional_profile = _ensure_dict(best.get("definitional_profile"))
        counterfactuals = [row for row in _ensure_list(best.get("counterfactual_probes")) if isinstance(row, dict)]
        conjecture_id = _clean_text(best.get("conjecture_id"))
        claim_text = _first_nonempty(
            definitional_profile.get("bridging_concept_definition"),
            mathematical_spec.get("definition_template"),
            best.get("mathematical_object_role"),
            conjecture_id,
        )
        claim_type = "abstraction-conjecture"
        target_statement_id = _clean_text(best.get("to_id"))
        source_statement_id = _clean_text(best.get("from_id"))
        abstraction_type = _clean_text(best.get("abstraction_type"))
        abstraction_label = _first_nonempty(best.get("abstraction_label"), conjecture_id)
        missing_route_lemma = _first_nonempty(
            mathematical_spec.get("missing_route_lemma"),
            delta.get("missing_witness_or_transport"),
        )
        negative_route = _first_nonempty(
            _ensure_dict(counterfactuals[0]).get("intervention") if counterfactuals else "",
            mathematical_spec.get("obstruction_template"),
        )
        negative_program = _negative_reasoning_program(
            candidate_object=abstraction_label,
            source_focus=_first_nonempty(delta.get("source_claim_focus"), source_statement_id),
            target_focus=_first_nonempty(delta.get("target_claim_focus"), target_statement_id),
            invariant=_clean_text(best.get("preserved_invariant")),
            negative_route=negative_route,
            failure_diagnosis=_clean_text(mathematical_spec.get("obstruction_template")),
            barrier_scope=_clean_text(best.get("barrier_scope")),
            missing_route_lemma=missing_route_lemma,
            carrier_kind=_clean_text(best.get("carrier_kind")),
        )
        blocked_route = next(
            (
                row
                for row in _blocked_route_entries(queue)
                if _clean_text(row.get("bridge_id")) == bridge_id
            ),
            {},
        )
        entry = {
                "queue_key": make_queue_key(
                    bridge_id=bridge_id,
                    claim_text=claim_text,
                    target_statement_id=target_statement_id,
                    claim_slug=f"{claim_type}-{conjecture_id or abstraction_type or abstraction_label}",
                ),
                "kb_ref": kb_ref,
                "title": _build_abstraction_title(best),
                "status": "pending",
                "priority": _safe_float(best.get("priority")),
                "bridge_id": bridge_id,
                "conjecture_id": conjecture_id,
                "claim_type": claim_type,
                "claim_text": claim_text,
                "conjecture_statement": claim_text,
                "source_statement_id": source_statement_id,
                "target_statement_id": target_statement_id,
                "source_excerpt": _first_nonempty(delta.get("source_theorem_excerpt"), best.get("source_excerpt")),
                "target_excerpt": _first_nonempty(delta.get("target_theorem_excerpt"), best.get("target_excerpt")),
                "route_synopsis": _first_nonempty(delta.get("route_synopsis"), best.get("route_synopsis")),
                "candidate_object": abstraction_label,
                "carrier_kind": _clean_text(best.get("carrier_kind")),
                "preserved_invariant": _clean_text(best.get("preserved_invariant")),
                "proof_strategy_family": abstraction_type or "route-repair",
                "missing_route_lemma": missing_route_lemma,
                "conditional_proposition": _clean_text(mathematical_spec.get("conditional_claim")),
                "proof_obligations": [
                    _clean_text(value)
                    for value in _ensure_list(mathematical_spec.get("proof_obligation_templates"))[:5]
                    if _clean_text(value)
                ],
                "candidate_lemmas": [
                    _clean_text(value)
                    for value in _ensure_list(mathematical_spec.get("inspection_focus"))[:5]
                    if _clean_text(value)
                ],
                "negative_route": _clean_text(negative_route),
                "failure_diagnosis": _clean_text(mathematical_spec.get("obstruction_template")),
                "negative_reasoning_program": negative_program,
                "impossibility_conjecture": _clean_text(negative_program.get("impossibility_claim_template")),
                "statement_delta": delta,
                "abstraction_type": abstraction_type,
                "why_now": [
                    _clean_text(
                        f"The first-layer route `{bridge_id}` is blocked, so discovery escalates to a typed repair object `{abstraction_label}`."
                    ),
                    _clean_text(
                        f"This conjecture targets the same theorem delta `{_first_nonempty(delta.get('source_claim_focus'), source_statement_id)}`"
                        f" -> `{_first_nonempty(delta.get('target_claim_focus'), target_statement_id)}` but with a stronger carrier."
                    ),
                    _clean_text(
                        f"Even a negative resolution is valuable because it would clarify whether `{abstraction_label}` is a genuine bridge"
                        f" or just a renamed obstruction."
                    ),
                ],
                "exploration_policy": "re-encode-blocked-route",
                "provenance": {
                    "source_artifacts": ["concept-gap-abstractions", "proof-queue"],
                    "linked_hypothesis_ids": [],
                },
            }
        entry = _annotate_with_breakthrough(
            entry,
            _ensure_dict(breakthrough_index.get("by_bridge_id")).get(bridge_id)
            or _ensure_dict(breakthrough_index.get("by_queue_id")).get(_clean_text(_ensure_dict(blocked_route).get("queue_id"))),
        )
        entries.append(entry)
    return _select_entries_by_breakthrough_family(entries, breakthrough_index=breakthrough_index, top_k=top_k)


def build_repair_lemma_entries(
    *,
    artifacts_dir: Path,
    queue: dict[str, Any],
    kb_ref: str,
    breakthrough_profile: dict[str, Any] | None = None,
    top_k: int = 6,
) -> list[dict[str, Any]]:
    breakthrough_index = _breakthrough_priority_index(breakthrough_profile, queue)
    entries: list[dict[str, Any]] = []
    for row in _blocked_abstraction_entries(queue):
        attempt = _load_attempt_payload(artifacts_dir, _clean_text(row.get("final_attempt_id")))
        if not attempt:
            continue
        target = _ensure_dict(attempt.get("target"))
        final_summary = _clean_text(_ensure_dict(attempt.get("final_assessment")).get("summary"))
        if not final_summary:
            continue
        repair = _repair_lemma_spec(attempt)
        focus_label = repair["focus_label"]
        claim_text = repair["claim_text"]
        target_statement_id = _clean_text(target.get("target_statement_id"))
        source_statement_id = _clean_text(target.get("source_statement_id"))
        candidate_object = _first_nonempty(target.get("candidate_object"), focus_label)
        negative_program = _negative_reasoning_program(
            candidate_object=candidate_object,
            source_focus=_first_nonempty(_ensure_dict(target.get("statement_delta")).get("source_claim_focus"), source_statement_id),
            target_focus=_first_nonempty(_ensure_dict(target.get("statement_delta")).get("target_claim_focus"), target_statement_id),
            invariant=_clean_text(target.get("preserved_invariant")),
            negative_route=_clean_text(
                _ensure_dict(_ensure_dict(attempt.get("proof_attempt")).get("negative_argument")).get("counterexample_or_barrier")
            ),
            failure_diagnosis=_clean_text(repair["diagnosis"]),
            barrier_scope=_clean_text(target.get("barrier_scope")),
            missing_route_lemma=_first_nonempty(repair["lemma"], claim_text),
            carrier_kind=_clean_text(target.get("carrier_kind")),
        )
        entry = {
                "queue_key": make_queue_key(
                    bridge_id=_clean_text(target.get("bridge_id")),
                    claim_text=claim_text,
                    target_statement_id=target_statement_id,
                    claim_slug=f"repair-lemma-{focus_label}",
                ),
                "kb_ref": kb_ref,
                "title": _build_repair_lemma_title(target, focus_label),
                "status": "pending",
                "priority": max(_safe_float(row.get("priority")) - 0.03, 0.0),
                "bridge_id": _clean_text(target.get("bridge_id")),
                "claim_type": "repair-lemma",
                "claim_text": claim_text,
                "conjecture_statement": claim_text,
                "source_statement_id": source_statement_id,
                "target_statement_id": target_statement_id,
                "source_excerpt": _clean_text(target.get("source_excerpt")),
                "target_excerpt": _clean_text(target.get("target_excerpt")),
                "route_synopsis": _clean_text(target.get("route_synopsis")),
                "candidate_object": candidate_object,
                "carrier_kind": _clean_text(target.get("carrier_kind")),
                "preserved_invariant": _clean_text(target.get("preserved_invariant")),
                "proof_strategy_family": "repair-lemma",
                "missing_route_lemma": _first_nonempty(repair["lemma"], claim_text),
                "conditional_proposition": claim_text,
                "proof_obligations": [
                    _clean_text(
                        f"State `{focus_label}` on the theorem pair `{source_statement_id}` -> `{target_statement_id}`."
                    ),
                    _clean_text(
                        f"Show why the blocked route summary `{final_summary}` reduces to this lemma rather than to a broader bridge search."
                    ),
                    _clean_text(
                        f"Either prove the lemma locally or explain why the local artifact stack still cannot realize it."
                    ),
                ],
                "candidate_lemmas": [
                    _clean_text(repair["diagnosis"]),
                    _clean_text(_ensure_dict(attempt.get("proof_attempt")).get("result_statement")),
                ],
                "negative_route": _clean_text(
                    _ensure_dict(_ensure_dict(attempt.get("proof_attempt")).get("negative_argument")).get("counterexample_or_barrier")
                ),
                "failure_diagnosis": _clean_text(repair["diagnosis"]),
                "negative_reasoning_program": negative_program,
                "impossibility_conjecture": _clean_text(negative_program.get("impossibility_claim_template")),
                "statement_delta": _ensure_dict(target.get("statement_delta")),
                "why_now": [
                    _clean_text(
                        f"The second-order conjecture `{row.get('queue_id', '')}` is blocked, so discovery escalates to the narrower repair lemma `{focus_label}`."
                    ),
                    _clean_text(repair["diagnosis"]),
                    _clean_text(
                        f"Even a negative result is valuable because it would certify that the missing step on route `{target.get('bridge_id', '')}` has now been localized as tightly as possible."
                    ),
                ],
                "exploration_policy": "repair-blocked-abstraction",
                "provenance": {
                    "source_artifacts": ["proof-cycle-summary", "proof-attempts"],
                    "linked_hypothesis_ids": [],
                },
            }
        entry = _annotate_with_breakthrough(
            entry,
            _ensure_dict(breakthrough_index.get("by_queue_id")).get(_clean_text(row.get("queue_id")))
            or _ensure_dict(breakthrough_index.get("by_bridge_id")).get(_clean_text(target.get("bridge_id"))),
        )
        entries.append(entry)
    return _select_entries_by_breakthrough_family(entries, breakthrough_index=breakthrough_index, top_k=top_k)


def build_queue_entries(
    *,
    expert: dict[str, Any],
    search_space: dict[str, Any],
    kb_ref: str,
    top_k: int = 8,
) -> list[dict[str, Any]]:
    route_index = _search_space_route_index(search_space)
    frontier_index = _frontier_index(search_space)
    entries: list[dict[str, Any]] = []
    for bridge in _bridge_rows(expert)[: max(1, top_k)]:
        bridge_id = _clean_text(bridge.get("bridge_id"))
        if not bridge_id:
            continue
        route = _ensure_dict(route_index.get(bridge_id))
        frontier = _ensure_dict(frontier_index.get(bridge_id))
        exploration_policy = _first_nonempty(frontier.get("policy"), route.get("exploration_policy"), "continue")
        if exploration_policy == "re-encode-before-retrying":
            continue
        claim_type, claim_text = _build_conjecture_statement(bridge)
        target_statement_id = _clean_text(bridge.get("target_statement_id"))
        source_statement_id = _clean_text(bridge.get("source_statement_id"))
        queue_priority = max(
            _safe_float(bridge.get("priority")),
            _safe_float(frontier.get("priority")),
            _safe_float(route.get("priority")),
        )
        delta = _ensure_dict(bridge.get("statement_delta"))
        negative_program = _negative_reasoning_program(
            candidate_object=_first_nonempty(bridge.get("abstraction_label"), bridge.get("carrier_kind")),
            source_focus=_first_nonempty(delta.get("source_claim_focus"), source_statement_id),
            target_focus=_first_nonempty(delta.get("target_claim_focus"), target_statement_id),
            invariant=_clean_text(bridge.get("preserved_invariant")),
            negative_route=_clean_text(bridge.get("negative_route")),
            failure_diagnosis=_clean_text(bridge.get("failure_diagnosis")),
            barrier_scope=_clean_text(bridge.get("barrier_scope")),
            missing_route_lemma=_clean_text(bridge.get("missing_route_lemma")),
            carrier_kind=_clean_text(bridge.get("carrier_kind")),
        )
        entries.append(
            {
                "queue_key": make_queue_key(
                    bridge_id=bridge_id,
                    claim_text=claim_text,
                    target_statement_id=target_statement_id,
                    claim_slug="route-conjecture",
                ),
                "kb_ref": kb_ref,
                "title": _build_title(bridge),
                "status": "pending",
                "priority": queue_priority,
                "bridge_id": bridge_id,
                "claim_type": claim_type,
                "claim_text": claim_text,
                "conjecture_statement": claim_text,
                "source_statement_id": source_statement_id,
                "target_statement_id": target_statement_id,
                "source_excerpt": _clean_text(bridge.get("source_excerpt")),
                "target_excerpt": _clean_text(bridge.get("target_excerpt")),
                "route_synopsis": _clean_text(bridge.get("route_synopsis")),
                "candidate_object": _first_nonempty(bridge.get("abstraction_label"), bridge.get("carrier_kind")),
                "carrier_kind": _clean_text(bridge.get("carrier_kind")),
                "preserved_invariant": _clean_text(bridge.get("preserved_invariant")),
                "proof_strategy_family": _clean_text(bridge.get("proof_strategy_family")),
                "missing_route_lemma": _clean_text(bridge.get("missing_route_lemma")),
                "conditional_proposition": _clean_text(bridge.get("conditional_proposition")),
                "proof_obligations": [
                    _clean_text(value)
                    for value in _ensure_list(bridge.get("proof_obligations"))[:5]
                    if _clean_text(value)
                ],
                "candidate_lemmas": [
                    _clean_text(value)
                    for value in _ensure_list(bridge.get("candidate_lemmas"))[:5]
                    if _clean_text(value)
                ],
                "negative_route": _clean_text(bridge.get("negative_route")),
                "failure_diagnosis": _clean_text(bridge.get("failure_diagnosis")),
                "negative_reasoning_program": negative_program,
                "impossibility_conjecture": _clean_text(negative_program.get("impossibility_claim_template")),
                "statement_delta": delta,
                "why_now": [
                    _clean_text(
                        f"Exploration policy `{exploration_policy}` for route `{bridge_id}` with priority {queue_priority:.3f}."
                    ),
                    _clean_text(
                        f"Attempt this next because the route centers on `{_first_nonempty(delta.get('source_claim_focus'), source_statement_id)}`"
                        f" -> `{_first_nonempty(delta.get('target_claim_focus'), target_statement_id)}`."
                    ),
                    _clean_text(
                        f"Positive and negative resolution are both informative: proving the claim would stabilize the route,"
                        f" while disproving it would sharpen or rule out `{_first_nonempty(bridge.get('abstraction_label'), bridge_id)}`."
                    ),
                ],
                "exploration_policy": exploration_policy,
                "route_signature": _clean_text(route.get("route_signature")),
                "search_dimensions": _ensure_dict(route.get("dimensions")),
                "provenance": {
                    "source_artifacts": ["expert-hypothesis-paper", "search-space-tree"],
                    "linked_hypothesis_ids": [
                        _clean_text(value)
                        for value in _ensure_list(bridge.get("linked_hypothesis_ids"))
                        if _clean_text(value)
                    ],
                },
            }
        )
    return entries


def _write_breakthrough_profile(
    *,
    artifacts_dir: Path,
    kb_ref: str,
    prior_art: dict[str, Any],
    queue: dict[str, Any],
) -> tuple[
    dict[str, Any],
    tuple[Path, Path, Path, Path],
    tuple[Path, Path, Path, Path],
    tuple[Path, Path, Path, Path],
    tuple[Path, Path, Path, Path],
    tuple[Path, Path],
    list[dict[str, str]],
]:
    report = build_breakthrough_report(prior_art=prior_art, queue=queue, kb_ref=kb_ref)
    output_json = artifacts_dir / "discovery-breakthrough-profile.json"
    output_md = artifacts_dir / "discovery-breakthrough-profile.md"
    output_tex = artifacts_dir / "discovery-breakthrough-profile.tex"
    output_pdf = artifacts_dir / "discovery-breakthrough-profile.pdf"
    prompt_pack = build_breakthrough_prompt_pack(report)
    routing = build_discovery_pattern_routing(report, prompt_pack)
    lens_artifacts = build_discovery_lens_artifacts(report, prompt_pack, routing)
    prompt_json = artifacts_dir / "discovery-family-prompts.json"
    prompt_md = artifacts_dir / "discovery-family-prompts.md"
    prompt_tex = artifacts_dir / "discovery-family-prompts.tex"
    prompt_pdf = artifacts_dir / "discovery-family-prompts.pdf"
    routing_json = artifacts_dir / "discovery-pattern-routing.json"
    routing_md = artifacts_dir / "discovery-pattern-routing.md"
    routing_tex = artifacts_dir / "discovery-pattern-routing.tex"
    routing_pdf = artifacts_dir / "discovery-pattern-routing.pdf"
    lens_json = artifacts_dir / "discovery-lens-artifacts.json"
    lens_md = artifacts_dir / "discovery-lens-artifacts.md"
    lens_tex = artifacts_dir / "discovery-lens-artifacts.tex"
    lens_pdf = artifacts_dir / "discovery-lens-artifacts.pdf"
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_breakthrough_markdown(report), encoding="utf-8")
    output_tex.write_text(render_breakthrough_tex(report), encoding="utf-8")
    prompt_json.write_text(json.dumps(prompt_pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    prompt_md.write_text(render_prompt_pack_markdown(prompt_pack), encoding="utf-8")
    prompt_tex.write_text(render_prompt_pack_tex(prompt_pack), encoding="utf-8")
    routing_json.write_text(json.dumps(routing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    routing_md.write_text(render_discovery_pattern_routing_markdown(routing), encoding="utf-8")
    routing_tex.write_text(render_discovery_pattern_routing_tex(routing), encoding="utf-8")
    lens_json.write_text(json.dumps(lens_artifacts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lens_md.write_text(render_discovery_lens_artifacts_markdown(lens_artifacts), encoding="utf-8")
    lens_tex.write_text(render_discovery_lens_artifacts_tex(lens_artifacts), encoding="utf-8")
    compile_breakthrough_pdf(output_tex, output_pdf, preferred_engine="auto")
    compile_breakthrough_pdf(prompt_tex, prompt_pdf, preferred_engine="auto")
    compile_breakthrough_pdf(routing_tex, routing_pdf, preferred_engine="auto")
    compile_breakthrough_pdf(lens_tex, lens_pdf, preferred_engine="auto")
    _branch_state, branch_paths, branch_dossiers = spawn_discovery_branches(
        routing,
        artifacts_dir=artifacts_dir,
        activate_top_k=4,
    )
    return (
        report,
        (output_json, output_md, output_tex, output_pdf),
        (prompt_json, prompt_md, prompt_tex, prompt_pdf),
        (routing_json, routing_md, routing_tex, routing_pdf),
        (lens_json, lens_md, lens_tex, lens_pdf),
        branch_paths,
        branch_dossiers,
    )


def main() -> int:
    logger = ReasoningLogger("kb-discovery-cycle")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    ap.add_argument("--kb-ref", default="", help="Optional KB reference override.")
    ap.add_argument("--top-k", type=int, default=8, help="Maximum number of queue entries to materialize.")
    ap.add_argument("--output-json", default="", help="Optional proof-queue JSON path.")
    ap.add_argument("--output-md", default="", help="Optional proof-queue Markdown path.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()
    kb_ref = _first_nonempty(args.kb_ref, kb_ref_from_artifacts_dir(artifacts_dir))
    if not kb_ref:
        raise SystemExit("[ERROR] Could not resolve kb_ref for discovery cycle.")

    queue_json, queue_md = proof_queue_paths(repo_root, kb_ref)
    if args.output_json:
        queue_json = Path(args.output_json)
    if args.output_md:
        queue_md = Path(args.output_md)

    expert = _load_json(artifacts_dir / "expert-hypothesis-paper.json")
    search_space = _load_json(artifacts_dir / "search-space-tree.json")
    gap_abstractions = _load_json(artifacts_dir / "concept-gap-abstractions.json")
    if not expert:
        raise SystemExit(f"[ERROR] Missing expert paper at {artifacts_dir / 'expert-hypothesis-paper.json'}")

    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    entries = build_queue_entries(expert=expert, search_space=search_space, kb_ref=kb_ref, top_k=args.top_k)
    breakthrough_outputs: tuple[Path, Path, Path, Path] | None = None
    breakthrough_prompt_outputs: tuple[Path, Path, Path, Path] | None = None
    breakthrough_routing_outputs: tuple[Path, Path, Path, Path] | None = None
    breakthrough_lens_outputs: tuple[Path, Path, Path, Path] | None = None
    breakthrough_branch_outputs: tuple[Path, Path] | None = None
    breakthrough_branch_dossiers: list[dict[str, str]] = []
    breakthrough_report: dict[str, Any] | None = None
    discovery_layer_count = 0
    discovery_branch_count = 0
    if not _queue_has_active_entries(queue):
        prior_art = _load_json(artifacts_dir / "prior-art-pass-report.json")
        if prior_art:
            (
                breakthrough_report,
                breakthrough_outputs,
                breakthrough_prompt_outputs,
                breakthrough_routing_outputs,
                breakthrough_lens_outputs,
                breakthrough_branch_outputs,
                breakthrough_branch_dossiers,
            ) = _write_breakthrough_profile(artifacts_dir=artifacts_dir, kb_ref=kb_ref, prior_art=prior_art, queue=queue)
            discovery_layer_count = int(
                _load_json(breakthrough_routing_outputs[0]).get("metadata", {}).get("layer_count", 0) or 0
            )
            discovery_branch_count = int(
                _load_json(breakthrough_branch_outputs[0]).get("metadata", {}).get("branch_count", 0) or 0
            )
        entries.extend(
            build_repair_queue_entries(
                gap_abstractions=gap_abstractions,
                queue=queue,
                kb_ref=kb_ref,
                breakthrough_profile=breakthrough_report,
                top_k=max(1, args.top_k),
            )
        )
        entries.extend(
            build_repair_lemma_entries(
                artifacts_dir=artifacts_dir,
                queue=queue,
                kb_ref=kb_ref,
                breakthrough_profile=breakthrough_report,
                top_k=max(1, args.top_k),
            )
        )
    added, updated = enqueue_entries(queue, entries)
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)
    refresh_summary_from_sources(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        queue=queue,
    )

    logger.step(
        "Queued proof candidates",
        "\n".join(
            [
                f"kb_ref={kb_ref}",
                f"artifacts_dir={artifacts_dir}",
                f"queue_entries_built={len(entries)}",
                f"queue_entries_added={added}",
                f"queue_entries_updated={updated}",
                f"breakthrough_profiles={int(_ensure_dict(breakthrough_report).get('metadata', {}).get('profile_count', 0) or 0)}",
                f"discovery_layers={discovery_layer_count}",
                f"discovery_branches={discovery_branch_count}",
                f"mathlib_root={mathlib_root(repo_root, kb_ref)}",
            ]
        ),
        surface_focus="discovery-proof-queue",
        surface_stage="discovery-cycle",
        surface_metrics={
            "added": added,
            "updated": updated,
            "entries": len(queue.get('entries', [])),
            "discovery_layers": discovery_layer_count,
            "discovery_branches": discovery_branch_count,
        },
        surface_taxonomy={"reasoning_types": ["discovery-cycle", "queue-building"]},
    )
    logger.add_output("proof_queue_json", queue_json)
    logger.add_output("proof_queue_md", queue_md)
    if breakthrough_outputs is not None:
        logger.add_output("discovery_breakthrough_profile_json", breakthrough_outputs[0])
        logger.add_output("discovery_breakthrough_profile_md", breakthrough_outputs[1])
        logger.add_output("discovery_breakthrough_profile_tex", breakthrough_outputs[2])
        logger.add_output("discovery_breakthrough_profile_pdf", breakthrough_outputs[3])
    if breakthrough_prompt_outputs is not None:
        logger.add_output("discovery_family_prompts_json", breakthrough_prompt_outputs[0])
        logger.add_output("discovery_family_prompts_md", breakthrough_prompt_outputs[1])
        logger.add_output("discovery_family_prompts_tex", breakthrough_prompt_outputs[2])
        logger.add_output("discovery_family_prompts_pdf", breakthrough_prompt_outputs[3])
    if breakthrough_routing_outputs is not None:
        logger.add_output("discovery_pattern_routing_json", breakthrough_routing_outputs[0])
        logger.add_output("discovery_pattern_routing_md", breakthrough_routing_outputs[1])
        logger.add_output("discovery_pattern_routing_tex", breakthrough_routing_outputs[2])
        logger.add_output("discovery_pattern_routing_pdf", breakthrough_routing_outputs[3])
    if breakthrough_lens_outputs is not None:
        logger.add_output("discovery_lens_artifacts_json", breakthrough_lens_outputs[0])
        logger.add_output("discovery_lens_artifacts_md", breakthrough_lens_outputs[1])
        logger.add_output("discovery_lens_artifacts_tex", breakthrough_lens_outputs[2])
        logger.add_output("discovery_lens_artifacts_pdf", breakthrough_lens_outputs[3])
    if breakthrough_branch_outputs is not None:
        logger.add_output("discovery_branch_queue_json", breakthrough_branch_outputs[0])
        logger.add_output("discovery_branch_queue_md", breakthrough_branch_outputs[1])
        for row in breakthrough_branch_dossiers[:6]:
            branch_key = _clean_text(row.get("branch_id")).replace("-", "_").replace(".", "_")
            logger.add_output(f"discovery_branch_{branch_key}_md", Path(row["md"]))
    log_path = logger.finalize(
        "success",
        summary=f"Queued {len(entries)} proof candidates for `{kb_ref}` (added={added}, updated={updated}).",
    )
    print(f"[OK] Wrote proof queue JSON: {queue_json}")
    print(f"[OK] Wrote proof queue Markdown: {queue_md}")
    if breakthrough_outputs is not None:
        print(f"[OK] Wrote breakthrough profile JSON: {breakthrough_outputs[0]}")
        print(f"[OK] Wrote breakthrough profile Markdown: {breakthrough_outputs[1]}")
        print(f"[OK] Wrote breakthrough profile TeX: {breakthrough_outputs[2]}")
        print(f"[OK] Wrote breakthrough profile PDF: {breakthrough_outputs[3]}")
    if breakthrough_prompt_outputs is not None:
        print(f"[OK] Wrote discovery family prompts JSON: {breakthrough_prompt_outputs[0]}")
        print(f"[OK] Wrote discovery family prompts Markdown: {breakthrough_prompt_outputs[1]}")
        print(f"[OK] Wrote discovery family prompts TeX: {breakthrough_prompt_outputs[2]}")
        print(f"[OK] Wrote discovery family prompts PDF: {breakthrough_prompt_outputs[3]}")
    if breakthrough_routing_outputs is not None:
        print(f"[OK] Wrote discovery pattern routing JSON: {breakthrough_routing_outputs[0]}")
        print(f"[OK] Wrote discovery pattern routing Markdown: {breakthrough_routing_outputs[1]}")
        print(f"[OK] Wrote discovery pattern routing TeX: {breakthrough_routing_outputs[2]}")
        print(f"[OK] Wrote discovery pattern routing PDF: {breakthrough_routing_outputs[3]}")
    if breakthrough_lens_outputs is not None:
        print(f"[OK] Wrote discovery lens artifacts JSON: {breakthrough_lens_outputs[0]}")
        print(f"[OK] Wrote discovery lens artifacts Markdown: {breakthrough_lens_outputs[1]}")
        print(f"[OK] Wrote discovery lens artifacts TeX: {breakthrough_lens_outputs[2]}")
        print(f"[OK] Wrote discovery lens artifacts PDF: {breakthrough_lens_outputs[3]}")
    if breakthrough_branch_outputs is not None:
        print(f"[OK] Wrote discovery branch queue JSON: {breakthrough_branch_outputs[0]}")
        print(f"[OK] Wrote discovery branch queue Markdown: {breakthrough_branch_outputs[1]}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
