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

"""Build a scene-based conceptual-space animation from conceptual-dynamics reports."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger


SCENE_STAGE_ORDER = [
    "bridge-plan",
    "conjecture",
    "strategies",
    "proof-sketch",
    "hypothesis-eval",
    "revision-loop",
    "expert-paper",
]

SCENE_META = {
    "overview": {
        "title": "Open The Conceptual Field",
        "subtitle": "Targets, invariants, bridge pressure, and proof frontier",
    },
    "bridge-plan": {
        "title": "Expose Candidate Routes",
        "subtitle": "The search commits to explicit source-target transports",
    },
    "conjecture": {
        "title": "Invent The Missing Carrier",
        "subtitle": "The system proposes typed bridge objects, not just labels",
    },
    "strategies": {
        "title": "Diversify Proof Programs",
        "subtitle": "Bridge objects are lifted into competing proof families",
    },
    "proof-sketch": {
        "title": "Declare The Proof Spine",
        "subtitle": "Lemma chains, obligations, and theorem deltas come into focus",
    },
    "hypothesis-eval": {
        "title": "Stress-Test The Route",
        "subtitle": "Evidence weighting separates promising bridges from weak ones",
    },
    "revision-loop": {
        "title": "Preserve What Survives",
        "subtitle": "The frontier is revised around the routes that remain coherent",
    },
    "expert-paper": {
        "title": "Surface The Mathematical Note",
        "subtitle": "The strongest surviving routes are rendered for expert inspection",
    },
    "closing": {
        "title": "Hold The Frontier Open",
        "subtitle": "Supported routes, remaining obligations, and unresolved questions",
    },
}

MOJIBAKE_REPLACEMENTS = {
    "Ã¢â‚¬Å“": '"',
    "Ã¢â‚¬Â": '"',
    "Ã¢â‚¬Ëœ": "'",
    "Ã¢â‚¬â„¢": "'",
    "Ã¢â‚¬â€œ": "-",
    "Ã¢â‚¬â€": "-",
    "Ã¢â€ â€™": "->",
    "Ã¢â€°Â¥": ">=",
    "Ã¢â€°Â¤": "<=",
    "Â": "",
}


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _clean_text(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    for src, dst in MOJIBAKE_REPLACEMENTS.items():
        text = text.replace(src, dst)
    return " ".join(text.split())


def _truncate(text: Any, limit: int = 240) -> str:
    cleaned = _clean_text(text)
    if len(cleaned) <= limit:
        return cleaned
    cut = cleaned[: max(0, limit - 3)].rstrip()
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut + "..."


def _stage_label(stage: str) -> str:
    label = _clean_text(stage).replace(".", " / ").replace("-", " ")
    words = [w for w in label.split() if w]
    return " ".join(word.capitalize() for word in words)


def _item_id(item: Any, fallback: str) -> str:
    if isinstance(item, dict):
        for key in ("id", "bridge_id", "conjecture_id", "sketch_id", "strategy_id", "hypothesis_id", "label"):
            value = _clean_text(item.get(key))
            if value:
                return value
    return fallback


def _item_label(item: Any, fallback: str = "") -> str:
    if isinstance(item, dict):
        for key in ("label", "title", "name", "id"):
            value = _clean_text(item.get(key))
            if value:
                return value
    return _clean_text(fallback)


def _item_kind(item: dict[str, Any], fallback: str = "concept") -> str:
    object_type = _clean_text(item.get("object_type"))
    nature = _clean_text(item.get("nature"))
    if object_type == "proof_sketch":
        return "proof"
    if object_type in {"bridge_program", "abstraction_conjecture"}:
        return "bridge"
    if object_type == "hypothesis":
        return "hypothesis"
    if "invariant" in nature:
        return "invariant"
    if "target" in nature:
        return "target"
    if "bridge" in nature or "object" in nature:
        return "bridge"
    return fallback


def _score_display(item: Any) -> str:
    if not isinstance(item, dict):
        return ""
    score = item.get("score")
    if score is None:
        return ""
    return f"{_safe_float(score):.2f}"


def _first_nonempty(*values: Any) -> str:
    for value in values:
        cleaned = _clean_text(value)
        if cleaned:
            return cleaned
    return ""


def _first_items(items: list[Any], limit: int) -> list[Any]:
    out: list[Any] = []
    seen: set[str] = set()
    for idx, item in enumerate(items):
        key = _item_id(item, f"item-{idx}")
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
        if len(out) >= limit:
            break
    return out


def _statement_delta_text(delta: dict[str, Any]) -> str:
    model_shift = _clean_text(delta.get("model_shift"))
    consequence_shift = _clean_text(delta.get("consequence_shift"))
    missing = _clean_text(delta.get("missing_witness_or_transport"))
    parts = [part for part in (model_shift, consequence_shift, missing) if part]
    return " ".join(parts)


def _content_bundle(primary: dict[str, Any]) -> dict[str, Any]:
    content = _ensure_dict(primary.get("content"))
    delta = _ensure_dict(content.get("statement_delta"))
    return {
        "route_synopsis": _first_nonempty(content.get("route_synopsis"), delta.get("route_synopsis")),
        "source_excerpt": _first_nonempty(content.get("source_excerpt"), delta.get("source_theorem_excerpt")),
        "target_excerpt": _first_nonempty(content.get("target_excerpt"), delta.get("target_theorem_excerpt")),
        "statement_delta": delta,
        "carrier_kind": _clean_text(content.get("carrier_kind")),
        "typing_status": _clean_text(content.get("typing_status")),
        "bridge_definition": _clean_text(content.get("bridge_definition")),
        "conditional_claim": _clean_text(content.get("conditional_claim")),
        "assumptions": [_clean_text(v) for v in _ensure_list(content.get("assumptions")) if _clean_text(v)],
        "obligations": [_clean_text(v) for v in _ensure_list(content.get("obligations")) if _clean_text(v)],
        "lemmas": [_clean_text(v) for v in _ensure_list(content.get("lemmas")) if _clean_text(v)],
        "proof_outline": [_clean_text(v) for v in _ensure_list(content.get("proof_outline")) if _clean_text(v)],
        "failure_diagnosis": _clean_text(content.get("failure_diagnosis")),
        "counterfactual": _clean_text(content.get("counterfactual")),
    }


def _metric_card(label: str, value: Any) -> dict[str, str]:
    return {"label": _clean_text(label), "value": _clean_text(value)}


def _detail_points(*groups: Any, limit: int = 5) -> list[str]:
    points: list[str] = []
    seen: set[str] = set()
    for group in groups:
        values = group if isinstance(group, list) else [group]
        for value in values:
            cleaned = _clean_text(value)
            if not cleaned or cleaned in seen:
                continue
            seen.add(cleaned)
            points.append(cleaned)
            if len(points) >= limit:
                return points
    return points


def _node(
    *,
    node_id: str,
    title: str,
    body: str,
    kind: str,
    x: float,
    y: float,
    emphasis: bool = False,
    chip: str = "",
    score: str = "",
    detail_title: str = "",
    detail_body: str = "",
    detail_points: list[str] | None = None,
) -> dict[str, Any]:
    cleaned_title = _clean_text(title)
    cleaned_body = _clean_text(body)
    full_detail_title = _clean_text(detail_title) or cleaned_title
    full_detail_body = _clean_text(detail_body) or cleaned_body
    return {
        "id": node_id,
        "title": _truncate(cleaned_title, 92),
        "body": _truncate(cleaned_body, 132),
        "kind": kind,
        "x": round(x, 3),
        "y": round(y, 3),
        "emphasis": bool(emphasis),
        "chip": _clean_text(chip),
        "score": _clean_text(score),
        "detail_title": full_detail_title,
        "detail_body": full_detail_body,
        "detail_points": _detail_points(detail_points or []),
    }


def _edge(source: str, target: str, label: str, kind: str = "flow") -> dict[str, str]:
    return {
        "source": source,
        "target": target,
        "label": _truncate(label, 72),
        "kind": kind,
    }


def _scene_voiceover(
    *,
    stage_label: str,
    headline: str,
    route_synopsis: str,
    statement_delta: dict[str, Any],
    primary_label: str,
    carrier_kind: str,
    obligations: list[str],
    lemmas: list[str],
    failure_diagnosis: str,
    current: dict[str, Any] | None = None,
) -> list[str]:
    current = current or {}
    lines: list[str] = []
    if headline:
        lines.append(f"Reasoning declaration: {headline}")
    elif stage_label:
        lines.append(f"Reasoning declaration: the stage focus is {stage_label.lower()}.")
    if route_synopsis:
        lines.append(f"Mathematical declaration: {route_synopsis}")
    delta_text = _statement_delta_text(statement_delta)
    if delta_text:
        lines.append(f"Mathematical delta: {delta_text}")
    if primary_label:
        carrier = f" as {carrier_kind}" if carrier_kind else ""
        lines.append(f"Primary bridge object: {primary_label}{carrier}.")
    if lemmas:
        lines.append(f"Lemma focus: {lemmas[0]}")
    elif obligations:
        lines.append(f"Proof obligation: {obligations[0]}")
    if failure_diagnosis:
        lines.append(f"Failure diagnosis: {failure_diagnosis}")
    supported = _safe_int(current.get("supported_count"))
    open_count = _safe_int(current.get("open_count"))
    if supported or open_count:
        lines.append(f"Frontier status: {supported} supported routes and {open_count} open routes remain.")
    return _first_items(lines, 6)


def _overview_scene(report: dict[str, Any]) -> dict[str, Any]:
    summary = _ensure_dict(report.get("summary"))
    current = _ensure_dict(summary.get("current"))
    highlights = _ensure_dict(current.get("highlights"))
    targets = _first_items(_ensure_list(highlights.get("leading_targets")), 2)
    invariants = _first_items(_ensure_list(highlights.get("leading_invariants")), 2)
    bridge_objects = _first_items(_ensure_list(highlights.get("leading_bridge_objects")), 2)
    sketches = _first_items(_ensure_list(highlights.get("leading_proof_sketches")), 2)
    frontier = _first_items(_ensure_list(current.get("frontier")), 2)

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    for idx, item in enumerate(targets):
        nodes.append(
            _node(
                node_id=f"overview-target-{idx}",
                title=_item_label(item, f"target {idx+1}"),
                body="Target concept anchoring the exploration.",
                kind="target",
                x=16 + idx * 18,
                y=26,
                chip="target",
                score=_score_display(item),
                detail_body=_first_nonempty(
                    _clean_text(item.get("statement_excerpt")),
                    _clean_text(item.get("route_synopsis")),
                    "Target concept anchoring the exploration.",
                ),
                detail_points=_detail_points(
                    _clean_text(item.get("nature")),
                    _clean_text(item.get("focus")),
                ),
            )
        )
    for idx, item in enumerate(invariants):
        nodes.append(
            _node(
                node_id=f"overview-invariant-{idx}",
                title=_item_label(item, f"invariant {idx+1}"),
                body="Invariant that candidate bridges must preserve.",
                kind="invariant",
                x=38 + idx * 18,
                y=20,
                chip="invariant",
                score=_score_display(item),
                detail_body=_first_nonempty(
                    _clean_text(item.get("statement_excerpt")),
                    "Invariant that candidate bridges must preserve.",
                ),
                detail_points=_detail_points(
                    _clean_text(item.get("nature")),
                    _clean_text(item.get("route_synopsis")),
                ),
            )
        )
    for idx, item in enumerate(bridge_objects):
        node_id = f"overview-bridge-{idx}"
        nodes.append(
            _node(
                node_id=node_id,
                title=_item_label(item, f"bridge object {idx+1}"),
                body="Bridge object currently leading the conceptual search.",
                kind="bridge",
                x=32 + idx * 36,
                y=50,
                emphasis=(idx == 0),
                chip=_clean_text(item.get("object_type") or item.get("nature") or "bridge object"),
                score=_score_display(item),
                detail_body=_first_nonempty(
                    _clean_text(_ensure_dict(item.get("content")).get("bridge_definition")),
                    _clean_text(_ensure_dict(item.get("content")).get("route_synopsis")),
                    "Bridge object currently leading the conceptual search.",
                ),
                detail_points=_detail_points(
                    _clean_text(_ensure_dict(item.get("content")).get("carrier_kind")),
                    _clean_text(_ensure_dict(item.get("content")).get("typing_status")),
                    _ensure_dict(item.get("content")).get("assumptions"),
                    _ensure_dict(item.get("content")).get("obligations"),
                ),
            )
        )
        for inv_idx, _ in enumerate(invariants[:1]):
            edges.append(_edge(f"overview-invariant-{inv_idx}", node_id, "preserve", "support"))
    for idx, item in enumerate(sketches):
        node_id = f"overview-proof-{idx}"
        nodes.append(
            _node(
                node_id=node_id,
                title=_item_label(item, f"proof sketch {idx+1}"),
                body="Proof object surfacing the current route program.",
                kind="proof",
                x=30 + idx * 38,
                y=76,
                chip="proof sketch",
                score=_score_display(item),
                detail_body=_first_nonempty(
                    _clean_text(_ensure_dict(item.get("content")).get("route_synopsis")),
                    _clean_text(_ensure_dict(item.get("content")).get("conditional_claim")),
                    "Proof object surfacing the current route program.",
                ),
                detail_points=_detail_points(
                    _ensure_dict(item.get("content")).get("lemmas"),
                    _ensure_dict(item.get("content")).get("obligations"),
                ),
            )
        )
        if bridge_objects:
            edges.append(_edge("overview-bridge-0", node_id, "formalize", "flow"))
    for idx, item in enumerate(frontier):
        node_id = f"overview-frontier-{idx}"
        nodes.append(
            _node(
                node_id=node_id,
                title=_item_label(item, f"frontier {idx+1}"),
                body="Open hypothesis remaining on the frontier.",
                kind="hypothesis",
                x=82 + idx * 10,
                y=68,
                chip=_clean_text(item.get("status") or "open"),
                score=_score_display(item),
                detail_body=_first_nonempty(
                    _clean_text(item.get("failure_diagnosis")),
                    _clean_text(item.get("counterfactual")),
                    "Open hypothesis remaining on the frontier.",
                ),
                detail_points=_detail_points(
                    _clean_text(item.get("status")),
                    _clean_text(item.get("reason")),
                ),
            )
        )
        if sketches:
            edges.append(_edge("overview-proof-0", node_id, "tests", "diagnostic"))

    reasoning_types = sorted(_ensure_dict(current.get("reasoning_type_counts")).keys())[:3]
    top_targets = ", ".join(_item_label(item) for item in targets) or "the current target frontier"
    top_invariants = ", ".join(_item_label(item) for item in invariants) or "the current invariants"
    bridge_focus = _item_label(bridge_objects[0]) if bridge_objects else "the leading bridge object"
    voiceover = [
        f"Reasoning declaration: the exploration opens around {top_targets}.",
        f"Mathematical declaration: the route is constrained by {top_invariants}.",
        f"Bridge pressure: {bridge_focus} currently organizes the proof search.",
    ]
    if reasoning_types:
        voiceover.append(f"Reasoning modes already active: {', '.join(reasoning_types)}.")
    if frontier:
        voiceover.append(f"Open frontier: {_item_label(frontier[0])} remains unresolved.")

    return {
        "scene_id": "scene-00-overview",
        "order": 0,
        "stage": "overview",
        "title": SCENE_META["overview"]["title"],
        "subtitle": SCENE_META["overview"]["subtitle"],
        "headline": _clean_text(
            f"{_safe_int(current.get('concept_count'))} concepts, "
            f"{_safe_int(current.get('object_count'))} proof objects, "
            f"{_safe_int(_ensure_dict(current.get('lifecycle_totals')).get('open'))} open commitments"
        ),
        "reasoning_declaration": _clean_text(
            f"The conceptual field is anchored by {top_targets} and organized by proof pressure over {bridge_focus}."
        ),
        "mathematical_declaration": _clean_text(
            "The initial mathematical content is not yet a proof; it is a shaped frontier of targets, invariants, bridge objects, and open proof obligations."
        ),
        "route_synopsis": "",
        "source_excerpt": "",
        "target_excerpt": "",
        "statement_delta": {},
        "candidate_object": {"label": bridge_focus, "carrier_kind": "", "typing_status": ""},
        "assumptions": [],
        "obligations": [],
        "lemmas": [],
        "proof_outline": [],
        "failure_diagnosis": "",
        "counterfactual": "",
        "voiceover": voiceover,
        "metrics": [
            _metric_card("concepts", current.get("concept_count", 0)),
            _metric_card("bridge objects", _ensure_dict(current.get("concept_nature_counts")).get("bridge-object", 0)),
            _metric_card("proof sketches", _ensure_dict(current.get("object_type_counts")).get("proof_sketch", 0)),
            _metric_card("open routes", _ensure_dict(current.get("lifecycle_totals")).get("open", 0)),
        ],
        "nodes": nodes,
        "edges": edges,
        "spotlight_id": "overview-bridge-0" if bridge_objects else "",
    }


def _stage_scene(row: dict[str, Any], order: int) -> dict[str, Any]:
    stage = _clean_text(row.get("stage"))
    highlights = _ensure_dict(_ensure_dict(row.get("state")).get("highlights"))
    primary = _ensure_dict(highlights.get("primary_dossier"))
    content = _content_bundle(primary)
    delta = _ensure_dict(content.get("statement_delta"))
    headline = _clean_text(highlights.get("headline"))

    stage_targets = _first_items(
        _ensure_list(highlights.get("introduced_targets")) + _ensure_list(highlights.get("leading_targets")),
        2,
    )
    stage_invariants = _first_items(
        _ensure_list(highlights.get("introduced_invariants")) + _ensure_list(highlights.get("leading_invariants")),
        2,
    )
    stage_bridge_objects = _first_items(
        _ensure_list(highlights.get("introduced_bridge_objects")) + _ensure_list(highlights.get("leading_bridge_objects")),
        2,
    )
    stage_supporting = _first_items(_ensure_list(highlights.get("supporting_dossiers")), 2)

    primary_label = _item_label(primary, _stage_label(stage))
    if primary_label and not stage_bridge_objects:
        stage_bridge_objects = [primary]

    meta = SCENE_META.get(stage, {"title": _stage_label(stage), "subtitle": headline or _stage_label(stage)})
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    primary_id = f"{stage}-primary"
    source_id = f"{stage}-source"
    target_id = f"{stage}-target"
    if content["source_excerpt"]:
        nodes.append(
            _node(
                node_id=source_id,
                title="Source theorem",
                body=content["source_excerpt"],
                kind="theorem-source",
                x=14,
                y=22,
                chip=_first_nonempty(delta.get("source_claim_focus"), delta.get("source_problem_family")),
                detail_body=content["source_excerpt"],
                detail_points=_detail_points(
                    delta.get("source_claim_focus"),
                    delta.get("source_problem_family"),
                    delta.get("model_shift"),
                ),
            )
        )
    if content["target_excerpt"]:
        nodes.append(
            _node(
                node_id=target_id,
                title="Target theorem",
                body=content["target_excerpt"],
                kind="theorem-target",
                x=86,
                y=22,
                chip=_first_nonempty(delta.get("target_claim_focus"), delta.get("target_problem_family")),
                detail_body=content["target_excerpt"],
                detail_points=_detail_points(
                    delta.get("target_claim_focus"),
                    delta.get("target_problem_family"),
                    delta.get("consequence_shift"),
                ),
            )
        )

    nodes.append(
        _node(
            node_id=primary_id,
            title=primary_label or meta["title"],
            body=_first_nonempty(content["bridge_definition"], content["conditional_claim"], content["route_synopsis"]),
            kind=_item_kind(primary, "bridge"),
            x=50,
            y=46,
            emphasis=True,
            chip=_first_nonempty(content["carrier_kind"], _clean_text(primary.get("object_type"))),
            score=_score_display(primary),
            detail_body=_first_nonempty(
                content["bridge_definition"],
                content["conditional_claim"],
                content["route_synopsis"],
            ),
            detail_points=_detail_points(
                content["carrier_kind"],
                content["typing_status"],
                content["assumptions"],
                content["obligations"],
                content["lemmas"],
            ),
        )
    )

    for idx, item in enumerate(stage_invariants[:2]):
        node_id = f"{stage}-invariant-{idx}"
        nodes.append(
            _node(
                node_id=node_id,
                title=_item_label(item, f"invariant {idx+1}"),
                body="Invariant preserved across the route.",
                kind="invariant",
                x=40 + idx * 20,
                y=14,
                chip="invariant",
                score=_score_display(item),
                detail_body=_first_nonempty(
                    _clean_text(item.get("statement_excerpt")),
                    _clean_text(item.get("route_synopsis")),
                    "Invariant preserved across the route.",
                ),
                detail_points=_detail_points(
                    _clean_text(item.get("nature")),
                    delta.get("missing_witness_or_transport"),
                    content["obligations"],
                ),
            )
        )
        edges.append(_edge(node_id, primary_id, "preserve", "support"))

    for idx, item in enumerate(stage_targets[:2]):
        node_id = f"{stage}-targetconcept-{idx}"
        nodes.append(
            _node(
                node_id=node_id,
                title=_item_label(item, f"target {idx+1}"),
                body="Target-side concept activated at this stage.",
                kind="target",
                x=74 + idx * 14,
                y=52,
                chip="target",
                score=_score_display(item),
                detail_body=_first_nonempty(
                    _clean_text(item.get("statement_excerpt")),
                    delta.get("consequence_shift"),
                    "Target-side concept activated at this stage.",
                ),
                detail_points=_detail_points(
                    _clean_text(item.get("nature")),
                    content["route_synopsis"],
                ),
            )
        )
        edges.append(_edge(primary_id, node_id, "targets", "flow"))

    secondary_candidates = stage_supporting
    if not secondary_candidates:
        secondary_candidates = _first_items(
            _ensure_list(highlights.get("stage_proof_sketches")) + _ensure_list(highlights.get("leading_proof_sketches")),
            2,
        )
    if not secondary_candidates:
        secondary_candidates = _first_items(
            _ensure_list(highlights.get("stage_conjectures")) + _ensure_list(highlights.get("leading_conjectures")),
            2,
        )

    for idx, item in enumerate(secondary_candidates[:2]):
        node_id = f"{stage}-support-{idx}"
        nodes.append(
            _node(
                node_id=node_id,
                title=_item_label(item, f"support {idx+1}"),
                body=_first_nonempty(
                    _clean_text(_ensure_dict(item.get("content")).get("route_synopsis")),
                    _clean_text(item.get("nature")),
                    "Supporting mathematical object in the route.",
                ),
                kind=_item_kind(_ensure_dict(item), "support"),
                x=28 + idx * 44,
                y=76,
                chip=_first_nonempty(_clean_text(item.get("object_type")), _clean_text(item.get("status"))),
                score=_score_display(item),
                detail_body=_first_nonempty(
                    _clean_text(_ensure_dict(item.get("content")).get("bridge_definition")),
                    _clean_text(_ensure_dict(item.get("content")).get("conditional_claim")),
                    _clean_text(_ensure_dict(item.get("content")).get("route_synopsis")),
                    _clean_text(item.get("nature")),
                    "Supporting mathematical object in the route.",
                ),
                detail_points=_detail_points(
                    _ensure_dict(item.get("content")).get("assumptions"),
                    _ensure_dict(item.get("content")).get("obligations"),
                    _ensure_dict(item.get("content")).get("lemmas"),
                ),
            )
        )
        edges.append(_edge(node_id, primary_id, "supports", "support"))

    if content["lemmas"]:
        for idx, lemma in enumerate(content["lemmas"][:2]):
            node_id = f"{stage}-lemma-{idx}"
            nodes.append(
                _node(
                    node_id=node_id,
                    title=f"Lemma {idx + 1}",
                    body=lemma,
                    kind="lemma",
                    x=34 + idx * 32,
                    y=72,
                    chip="lemma chain",
                    detail_body=lemma,
                    detail_points=_detail_points(
                        delta.get("missing_witness_or_transport"),
                        content["proof_outline"],
                    ),
                )
            )
            edges.append(_edge(primary_id, node_id, "justify", "flow"))
            if content["target_excerpt"]:
                edges.append(_edge(node_id, target_id, "pushes", "flow"))

    if content["source_excerpt"]:
        edges.append(_edge(source_id, primary_id, "source regime", "flow"))
    if content["target_excerpt"]:
        edges.append(_edge(primary_id, target_id, "target payoff", "flow"))

    state = _ensure_dict(row.get("state"))
    current_counts = {
        "supported_count": _ensure_dict(state.get("hypothesis_state_counts")).get("supported", 0),
        "open_count": _ensure_dict(state.get("lifecycle_totals")).get("open", 0),
    }
    voiceover = _scene_voiceover(
        stage_label=_stage_label(stage),
        headline=headline,
        route_synopsis=content["route_synopsis"],
        statement_delta=delta,
        primary_label=primary_label,
        carrier_kind=content["carrier_kind"],
        obligations=content["obligations"],
        lemmas=content["lemmas"],
        failure_diagnosis=content["failure_diagnosis"],
        current=current_counts,
    )

    reasoning_declaration = _first_nonempty(
        headline,
        f"{_stage_label(stage)} emphasizes {_first_nonempty(primary_label, meta['title']).lower()}.",
    )
    mathematical_declaration = _first_nonempty(
        content["route_synopsis"],
        _statement_delta_text(delta),
        content["bridge_definition"],
    )

    metrics = [
        _metric_card("concepts", state.get("concept_count", 0)),
        _metric_card("objects", state.get("object_count", 0)),
        _metric_card("supported", _ensure_dict(state.get("hypothesis_state_counts")).get("supported", 0)),
        _metric_card("open", _ensure_dict(state.get("lifecycle_totals")).get("open", 0)),
    ]

    candidate_object = {
        "label": primary_label,
        "carrier_kind": content["carrier_kind"],
        "typing_status": content["typing_status"],
        "bridge_definition": content["bridge_definition"],
        "conditional_claim": content["conditional_claim"],
    }

    return {
        "scene_id": f"scene-{order:02d}-{stage}",
        "order": order,
        "stage": stage,
        "title": meta["title"],
        "subtitle": meta["subtitle"],
        "headline": headline,
        "reasoning_declaration": reasoning_declaration,
        "mathematical_declaration": mathematical_declaration,
        "route_synopsis": content["route_synopsis"],
        "source_excerpt": content["source_excerpt"],
        "target_excerpt": content["target_excerpt"],
        "statement_delta": delta,
        "candidate_object": candidate_object,
        "assumptions": content["assumptions"][:3],
        "obligations": content["obligations"][:3],
        "lemmas": content["lemmas"][:3],
        "proof_outline": content["proof_outline"][:3],
        "failure_diagnosis": content["failure_diagnosis"],
        "counterfactual": content["counterfactual"],
        "voiceover": voiceover,
        "metrics": metrics,
        "nodes": nodes,
        "edges": edges,
        "spotlight_id": primary_id,
    }


def _closing_scene(report: dict[str, Any], order: int) -> dict[str, Any]:
    summary = _ensure_dict(report.get("summary"))
    current = _ensure_dict(summary.get("current"))
    expert_row = next((row for row in _ensure_list(report.get("timeline")) if _clean_text(row.get("stage")) == "expert-paper"), {})
    stage_scene = _stage_scene(expert_row, order) if expert_row else {}
    frontier = _first_items(_ensure_list(current.get("frontier")), 2)
    supported = _safe_int(_ensure_dict(current.get("hypothesis_state_counts")).get("supported", 0))
    unresolved = _safe_int(_ensure_dict(current.get("hypothesis_state_counts")).get("unresolved", 0))
    nodes = list(_ensure_list(stage_scene.get("nodes")))
    edges = list(_ensure_list(stage_scene.get("edges")))

    if frontier:
        for idx, item in enumerate(frontier):
            node_id = f"closing-frontier-{idx}"
            nodes.append(
                _node(
                    node_id=node_id,
                    title=_item_label(item, f"frontier {idx+1}"),
                    body="Open mathematical commitment left for the next revision cycle.",
                    kind="hypothesis",
                    x=80 + idx * 12,
                    y=78,
                    chip=_clean_text(item.get("status") or "open"),
                    score=_score_display(item),
                    detail_body=_first_nonempty(
                        _clean_text(item.get("failure_diagnosis")),
                        _clean_text(item.get("counterfactual")),
                        "Open mathematical commitment left for the next revision cycle.",
                    ),
                    detail_points=_detail_points(
                        _clean_text(item.get("status")),
                        _clean_text(item.get("reason")),
                    ),
                )
            )
            spotlight = _clean_text(stage_scene.get("spotlight_id"))
            if spotlight:
                edges.append(_edge(spotlight, node_id, "still open", "diagnostic"))

    reasoning = _clean_text(
        f"The exploration ends with {supported} supported routes and {unresolved} unresolved routes. The expert-facing note keeps the main bridge visible while leaving the frontier inspectable."
    )
    mathematical = _first_nonempty(
        stage_scene.get("mathematical_declaration"),
        "The final state is not a proof, but a content-rich conditional theorem program with explicit open lemmas.",
    )
    voiceover = _first_items(
        [
            f"Reasoning declaration: {reasoning}",
            f"Mathematical declaration: {mathematical}",
            f"Open frontier: {_item_label(frontier[0])} remains unresolved." if frontier else "",
            _clean_text(stage_scene.get("failure_diagnosis")),
        ],
        5,
    )

    return {
        **stage_scene,
        "scene_id": f"scene-{order:02d}-closing",
        "order": order,
        "stage": "closing",
        "title": SCENE_META["closing"]["title"],
        "subtitle": SCENE_META["closing"]["subtitle"],
        "headline": _clean_text(f"{supported} supported routes, {unresolved} unresolved routes"),
        "reasoning_declaration": reasoning,
        "mathematical_declaration": mathematical,
        "voiceover": voiceover,
        "metrics": [
            _metric_card("supported", supported),
            _metric_card("unresolved", unresolved),
            _metric_card("proof sketches", _ensure_dict(current.get("object_type_counts")).get("proof_sketch", 0)),
            _metric_card("bridge programs", _ensure_dict(current.get("object_type_counts")).get("bridge_program", 0)),
        ],
        "nodes": nodes,
        "edges": edges,
    }


def _build_animation_report(conceptual_report: dict[str, Any], *, source_path: str = "") -> dict[str, Any]:
    scenes = [_overview_scene(conceptual_report)]
    rows = {
        _clean_text(row.get("stage")): row
        for row in _ensure_list(conceptual_report.get("timeline"))
        if isinstance(row, dict)
    }
    order = 1
    for stage in SCENE_STAGE_ORDER:
        row = rows.get(stage)
        if not row:
            continue
        scenes.append(_stage_scene(row, order))
        order += 1
    scenes.append(_closing_scene(conceptual_report, order))

    metadata = _ensure_dict(conceptual_report.get("metadata"))
    total_nodes = sum(len(_ensure_list(scene.get("nodes"))) for scene in scenes)
    total_edges = sum(len(_ensure_list(scene.get("edges"))) for scene in scenes)
    return {
        "metadata": {
            "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "conceptual_dynamics_path": _clean_text(source_path),
            "kb": _clean_text(metadata.get("kb")),
            "kb_ref": _clean_text(metadata.get("kb_ref")),
            "artifacts_dir": _clean_text(metadata.get("artifacts_dir")),
            "selected_run_id": _clean_text(metadata.get("selected_run_id")),
        },
        "summary": {
            "scene_count": len(scenes),
            "scene_titles": [scene.get("title", "") for scene in scenes],
            "focal_stage_count": len([scene for scene in scenes if scene.get("stage") not in {"overview", "closing"}]),
            "declared_node_count": total_nodes,
            "declared_edge_count": total_edges,
        },
        "scenes": scenes,
    }


def _list_markdown(items: list[str]) -> str:
    if not items:
        return "- none\n"
    return "".join(f"- {item}\n" for item in items)


def _to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Conceptual Space Animation",
        "",
        f"Scenes: {_safe_int(_ensure_dict(report.get('summary')).get('scene_count'))}",
        "",
    ]
    for scene in _ensure_list(report.get("scenes")):
        lines.extend(
            [
                f"## {scene.get('order', 0) + 1}. {_clean_text(scene.get('title'))}",
                "",
                f"- Stage: {_clean_text(scene.get('stage'))}",
                f"- Subtitle: {_clean_text(scene.get('subtitle'))}",
                f"- Reasoning declaration: {_clean_text(scene.get('reasoning_declaration'))}",
                f"- Mathematical declaration: {_clean_text(scene.get('mathematical_declaration'))}",
                f"- Route synopsis: {_clean_text(scene.get('route_synopsis'))}",
                "",
                "### Proof Obligations",
                _list_markdown([_clean_text(v) for v in _ensure_list(scene.get("obligations"))]),
                "### Lemma Chain",
                _list_markdown([_clean_text(v) for v in _ensure_list(scene.get("lemmas"))]),
                "### Voiceover",
                _list_markdown([_clean_text(v) for v in _ensure_list(scene.get("voiceover"))]),
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _render_html(report: dict[str, Any]) -> str:
    data = json.dumps(report, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Conceptual Space Animation</title>
  <style>
    :root {{
      --bg: #f3ede3;
      --panel: rgba(255, 250, 242, 0.94);
      --panel-strong: rgba(255, 252, 247, 0.98);
      --line: rgba(31, 56, 64, 0.16);
      --text: #11252d;
      --muted: #5f6d73;
      --accent: #cf5c36;
      --shadow: 0 22px 60px rgba(17, 37, 45, 0.16);
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; min-height: 100%; }}
    body {{
      font-family: "Aptos", "Segoe UI", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at 10% 12%, rgba(207, 92, 54, 0.18), transparent 30%),
        radial-gradient(circle at 88% 10%, rgba(35, 118, 122, 0.20), transparent 26%),
        linear-gradient(180deg, #f6f1e8 0%, #efe4d5 42%, #f5ede4 100%);
    }}
    .shell {{
      min-height: 100vh;
      padding: 18px;
      display: grid;
      grid-template-columns: minmax(0, 1.72fr) minmax(390px, 1.08fr);
      gap: 18px;
    }}
    .panel {{
      border: 1px solid var(--line);
      border-radius: 26px;
      background: var(--panel);
      box-shadow: var(--shadow);
      overflow: hidden;
    }}
    .main {{
      display: grid;
      grid-template-rows: auto auto 1fr;
      min-height: calc(100vh - 36px);
    }}
    .hero {{
      padding: 18px 22px 10px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(135deg, rgba(255,255,255,0.76), rgba(250,242,230,0.88));
    }}
    .hero-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}
    .eyebrow {{
      text-transform: uppercase;
      letter-spacing: 0.14em;
      font-size: 11px;
      color: var(--muted);
      font-weight: 700;
    }}
    h1 {{
      margin: 8px 0 8px;
      font-family: "Cambria", "Georgia", serif;
      font-size: clamp(30px, 4vw, 52px);
      line-height: 0.98;
      letter-spacing: -0.03em;
    }}
    .subtitle {{
      margin: 0;
      color: #374b52;
      font-size: 16px;
      line-height: 1.5;
      max-width: 920px;
    }}
    .controls {{
      padding: 14px 22px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      border-bottom: 1px solid var(--line);
      background: rgba(255,255,255,0.56);
    }}
    .controls button,
    .controls select {{
      appearance: none;
      border: 1px solid rgba(17, 37, 45, 0.18);
      background: rgba(255,255,255,0.94);
      color: var(--text);
      border-radius: 999px;
      padding: 9px 14px;
      font-size: 13px;
      cursor: pointer;
    }}
    .controls input[type="range"] {{
      width: min(320px, 48vw);
      accent-color: var(--accent);
    }}
    .controls .meta {{
      margin-left: auto;
      color: var(--muted);
      font-size: 12px;
      white-space: nowrap;
    }}
    .stage-area {{
      position: relative;
      padding: 16px 16px 0;
      display: grid;
      grid-template-rows: 1fr auto;
      min-height: 710px;
      background: linear-gradient(180deg, rgba(23, 49, 58, 0.97), rgba(18, 38, 45, 0.95));
    }}
    .map-frame {{
      position: relative;
      min-height: 630px;
      border-radius: 22px;
      overflow: hidden;
      border: 1px solid rgba(255,255,255,0.08);
      background:
        radial-gradient(circle at 50% 48%, rgba(255, 247, 232, 0.08), transparent 34%),
        linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
    }}
    .map-grid {{
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.045) 1px, transparent 1px);
      background-size: 84px 84px;
      mask-image: linear-gradient(180deg, rgba(0,0,0,0.62), rgba(0,0,0,0.1));
    }}
    .edge-layer {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      overflow: visible;
    }}
    .edge-layer path {{
      fill: none;
      stroke-width: 2.1;
      stroke-linecap: round;
      stroke-dasharray: 8 10;
      animation: dash 1.8s linear infinite;
      opacity: 0.9;
    }}
    .edge-label {{
      fill: rgba(255,255,255,0.86);
      font-size: 11px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .spotlight {{
      position: absolute;
      width: 300px;
      height: 300px;
      margin-left: -150px;
      margin-top: -150px;
      border-radius: 50%;
      pointer-events: none;
      background: radial-gradient(circle, rgba(255, 235, 190, 0.22) 0%, rgba(255, 235, 190, 0.12) 26%, rgba(255, 235, 190, 0.0) 70%);
      filter: blur(6px);
      transition: left 520ms ease, top 520ms ease, opacity 320ms ease;
    }}
    .node-layer {{ position: absolute; inset: 0; }}
    .node {{
      position: absolute;
      width: 200px;
      min-height: 86px;
      padding: 13px 14px;
      border-radius: 18px;
      border: 1px solid rgba(255,255,255,0.12);
      color: #f7f4ee;
      background: rgba(248, 243, 234, 0.08);
      box-shadow: 0 16px 32px rgba(0,0,0,0.18);
      transform: translate(-50%, -50%) scale(0.92);
      opacity: 0;
      transition: transform 520ms cubic-bezier(.19,1,.22,1), opacity 420ms ease, box-shadow 220ms ease;
      backdrop-filter: blur(14px);
      cursor: pointer;
    }}
    .node.visible {{
      opacity: 1;
      transform: translate(-50%, -50%) scale(1);
    }}
    .node.emphasis {{
      box-shadow: 0 22px 54px rgba(0,0,0,0.28), 0 0 0 1px rgba(255,240,220,0.10);
    }}
    .node.selected {{
      box-shadow: 0 22px 54px rgba(0,0,0,0.28), 0 0 0 2px rgba(255, 228, 178, 0.72);
    }}
    .node.theorem-source,
    .node.theorem-target {{
      width: 290px;
      min-height: 120px;
      background: rgba(255, 248, 236, 0.10);
    }}
    .node.bridge {{ width: 248px; min-height: 108px; background: rgba(52, 105, 154, 0.22); }}
    .node.proof,
    .node.lemma {{ background: rgba(35, 118, 122, 0.22); }}
    .node.target {{ background: rgba(207, 92, 54, 0.20); }}
    .node.invariant {{ background: rgba(185, 134, 30, 0.24); }}
    .node.hypothesis {{ background: rgba(255,255,255,0.10); }}
    .node .chip-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 8px;
    }}
    .node .chip {{
      display: inline-flex;
      align-items: center;
      padding: 3px 9px;
      border-radius: 999px;
      background: rgba(255,255,255,0.10);
      color: rgba(255,255,255,0.84);
      font-size: 10px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      font-weight: 700;
    }}
    .node .score {{ color: rgba(255,255,255,0.82); font-size: 11px; font-weight: 700; }}
    .node h3 {{ margin: 0 0 6px; font-size: 14px; line-height: 1.18; letter-spacing: -0.02em; }}
    .node p {{
      margin: 0;
      color: rgba(255,255,255,0.82);
      font-size: 11.5px;
      line-height: 1.38;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 4;
      overflow: hidden;
    }}
    .caption-ribbon {{
      position: absolute;
      left: 18px;
      right: 18px;
      bottom: 18px;
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 14px 18px;
      border-radius: 18px;
      border: 1px solid rgba(255,255,255,0.12);
      background: linear-gradient(90deg, rgba(255, 248, 236, 0.18), rgba(255,255,255,0.08));
      box-shadow: 0 16px 40px rgba(0,0,0,0.18);
      color: #fff8ee;
    }}
    .caption-ribbon .eyebrow {{ color: rgba(255,255,255,0.72); }}
    .caption-ribbon .text {{ font-size: 15px; line-height: 1.45; font-family: "Cambria", "Georgia", serif; }}
    .scene-strip {{
      display: flex;
      gap: 10px;
      padding: 16px 0 18px;
      overflow: auto;
    }}
    .scene-pill {{
      flex: 0 0 auto;
      padding: 10px 14px;
      border-radius: 16px;
      border: 1px solid rgba(255,255,255,0.10);
      color: rgba(255,255,255,0.78);
      background: rgba(255,255,255,0.04);
      cursor: pointer;
      min-width: 140px;
    }}
    .scene-pill.active {{
      background: linear-gradient(135deg, rgba(207, 92, 54, 0.30), rgba(185, 134, 30, 0.22));
      color: #fff8ef;
    }}
    .scene-pill .k {{ display: block; font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em; opacity: 0.72; margin-bottom: 4px; }}
    .scene-pill .v {{ font-size: 13px; font-weight: 700; line-height: 1.2; }}
    .side {{
      padding: 18px;
      display: grid;
      gap: 14px;
      align-content: start;
      min-height: calc(100vh - 36px);
      overflow: auto;
    }}
    .card {{
      border-radius: 22px;
      border: 1px solid var(--line);
      background: var(--panel-strong);
      padding: 18px;
      box-shadow: 0 14px 34px rgba(17, 37, 45, 0.06);
    }}
    .card h2 {{ margin: 6px 0 10px; font-family: "Cambria", "Georgia", serif; font-size: 24px; line-height: 1.05; }}
    .card p {{ margin: 0; color: #32474d; line-height: 1.55; font-size: 14px; }}
    .metric-grid, .delta-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}
    .metric, .delta-pill {{
      padding: 12px;
      border-radius: 16px;
      border: 1px solid rgba(17, 37, 45, 0.10);
      background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(246, 240, 231, 0.92));
    }}
    .metric .label, .delta-pill .k {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--muted);
      margin-bottom: 5px;
    }}
    .metric .value {{ font-size: 20px; font-weight: 800; letter-spacing: -0.03em; }}
    .delta-pill .v {{ display: block; color: #22363c; font-size: 13px; line-height: 1.42; }}
    .split {{ display: grid; gap: 12px; }}
    .route-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}
    .quote {{
      padding: 12px 14px;
      border-radius: 16px;
      background: rgba(35, 118, 122, 0.08);
      border: 1px solid rgba(35, 118, 122, 0.14);
    }}
    .quote h4, .list-block h4 {{
      margin: 0 0 8px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: #345156;
    }}
    .quote p {{ font-family: "Cambria", "Georgia", serif; font-size: 15px; color: #22363c; }}
    .list-block ul {{ margin: 0; padding-left: 18px; color: #274048; }}
    .list-block li {{ margin: 0 0 7px; line-height: 1.45; font-size: 14px; }}
    .node-meta {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }}
    .node-meta span {{
      display: inline-flex;
      align-items: center;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(17, 37, 45, 0.06);
      color: #294047;
      font-size: 11px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      font-weight: 700;
    }}
    .inspector-body {{
      font-family: "Cambria", "Georgia", serif;
      font-size: 15px;
      color: #22363c;
      line-height: 1.55;
      margin-bottom: 12px;
    }}
    .inspector-points {{
      margin: 0;
      padding-left: 18px;
      color: #274048;
    }}
    .inspector-points li {{
      margin: 0 0 6px;
      line-height: 1.42;
      font-size: 14px;
    }}
    .footer-note {{ color: var(--muted); font-size: 12px; line-height: 1.55; }}
    @keyframes dash {{ from {{ stroke-dashoffset: 0; }} to {{ stroke-dashoffset: -36; }} }}
    @media (max-width: 1180px) {{
      .shell {{ grid-template-columns: 1fr; }}
      .main, .side {{ min-height: auto; }}
      .stage-area {{ min-height: 580px; }}
    }}
    @media (max-width: 760px) {{
      .controls .meta {{ width: 100%; margin-left: 0; }}
      .stage-area {{ min-height: 520px; }}
      .map-frame {{ min-height: 460px; }}
      .node {{ width: 200px; }}
      .node.theorem-source, .node.theorem-target {{ width: 250px; }}
      .metric-grid, .delta-grid, .route-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <section class="panel main">
      <div class="hero">
        <div class="hero-top">
          <div>
            <div class="eyebrow">Conceptual Space Animation</div>
            <h1 id="sceneTitle">Conceptual Space Animation</h1>
            <p class="subtitle" id="sceneSubtitle"></p>
          </div>
          <div class="eyebrow" id="sceneCounter"></div>
        </div>
      </div>
      <div class="controls">
        <button id="prevBtn">Prev</button>
        <button id="playBtn">Play</button>
        <button id="nextBtn">Next</button>
        <label>Scene <input id="sceneRange" type="range" min="0" max="0" value="0" /></label>
        <label>Speed
          <select id="speedSelect">
            <option value="1">1x</option>
            <option value="1.35" selected>1.35x</option>
            <option value="1.75">1.75x</option>
          </select>
        </label>
        <div class="meta" id="metaText"></div>
      </div>
      <div class="stage-area">
        <div class="map-frame">
          <div class="map-grid"></div>
          <svg class="edge-layer" id="edgeLayer" viewBox="0 0 1000 700" preserveAspectRatio="none"></svg>
          <div class="spotlight" id="spotlight"></div>
          <div class="node-layer" id="nodeLayer"></div>
          <div class="caption-ribbon">
            <div class="eyebrow">Voiceover</div>
            <div class="text" id="captionText"></div>
          </div>
        </div>
        <div class="scene-strip" id="sceneStrip"></div>
      </div>
    </section>
    <aside class="panel side">
      <section class="card">
        <div class="eyebrow">Scene Declaration</div>
        <h2 id="sceneHeading"></h2>
        <p id="headlineText"></p>
      </section>
      <section class="card"><div class="eyebrow">Metrics</div><div class="metric-grid" id="metricGrid"></div></section>
      <section class="card split">
        <div><div class="eyebrow">Reasoning Declaration</div><p id="reasoningText"></p></div>
        <div><div class="eyebrow">Mathematical Declaration</div><p id="mathText"></p></div>
      </section>
      <section class="card split">
        <div><div class="eyebrow">Route Synopsis</div><p id="routeText"></p></div>
        <div class="route-grid">
          <div class="quote"><h4>Candidate object</h4><p id="candidateText"></p></div>
          <div class="quote"><h4>Typing and claim</h4><p id="claimText"></p></div>
        </div>
      </section>
      <section class="card split">
        <div class="quote"><h4>Source theorem</h4><p id="sourceText"></p></div>
        <div class="quote"><h4>Target theorem</h4><p id="targetText"></p></div>
      </section>
      <section class="card"><div class="eyebrow">Mathematical Delta</div><div class="delta-grid" id="deltaGrid"></div></section>
      <section class="card split">
        <div class="list-block"><h4>Assumptions</h4><ul id="assumptionList"></ul></div>
        <div class="list-block"><h4>Proof Obligations</h4><ul id="obligationList"></ul></div>
      </section>
      <section class="card split">
        <div class="list-block"><h4>Lemma Chain</h4><ul id="lemmaList"></ul></div>
        <div class="list-block"><h4>Proof Outline</h4><ul id="outlineList"></ul></div>
      </section>
      <section class="card split">
        <div class="eyebrow">Selected Node</div>
        <h2 id="selectedNodeTitle"></h2>
        <div class="node-meta"><span id="selectedNodeKind"></span><span id="selectedNodeChip"></span></div>
        <p class="inspector-body" id="selectedNodeBody"></p>
        <ul class="inspector-points" id="selectedNodePoints"></ul>
      </section>
      <section class="card split">
        <div><div class="eyebrow">Failure Diagnosis</div><p id="failureText"></p></div>
        <div><div class="eyebrow">Counterfactual Probe</div><p id="counterfactualText"></p></div>
      </section>
      <section class="card footer-note">
        Manim-style here means scene-based pacing, staged reveals, and theorem narration in a single interactive artifact. The payload remains inspectable as structured mathematical content rather than a video-only presentation.
      </section>
    </aside>
  </div>
  <script>
    const DATA = {data};
    const scenes = Array.isArray(DATA.scenes) ? DATA.scenes : [];
    const sceneTitle = document.getElementById("sceneTitle");
    const sceneSubtitle = document.getElementById("sceneSubtitle");
    const sceneCounter = document.getElementById("sceneCounter");
    const sceneHeading = document.getElementById("sceneHeading");
    const headlineText = document.getElementById("headlineText");
    const reasoningText = document.getElementById("reasoningText");
    const mathText = document.getElementById("mathText");
    const routeText = document.getElementById("routeText");
    const candidateText = document.getElementById("candidateText");
    const claimText = document.getElementById("claimText");
    const sourceText = document.getElementById("sourceText");
    const targetText = document.getElementById("targetText");
    const failureText = document.getElementById("failureText");
    const counterfactualText = document.getElementById("counterfactualText");
    const captionText = document.getElementById("captionText");
    const metricGrid = document.getElementById("metricGrid");
    const deltaGrid = document.getElementById("deltaGrid");
    const assumptionList = document.getElementById("assumptionList");
    const obligationList = document.getElementById("obligationList");
    const lemmaList = document.getElementById("lemmaList");
    const outlineList = document.getElementById("outlineList");
    const selectedNodeTitle = document.getElementById("selectedNodeTitle");
    const selectedNodeKind = document.getElementById("selectedNodeKind");
    const selectedNodeChip = document.getElementById("selectedNodeChip");
    const selectedNodeBody = document.getElementById("selectedNodeBody");
    const selectedNodePoints = document.getElementById("selectedNodePoints");
    const nodeLayer = document.getElementById("nodeLayer");
    const edgeLayer = document.getElementById("edgeLayer");
    const spotlight = document.getElementById("spotlight");
    const sceneStrip = document.getElementById("sceneStrip");
    const range = document.getElementById("sceneRange");
    const playBtn = document.getElementById("playBtn");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const speedSelect = document.getElementById("speedSelect");
    const metaText = document.getElementById("metaText");
    let currentIndex = 0;
    let selectedNodeId = "";
    let playbackTimer = null;
    let captionTimer = null;
    const EDGE_COLORS = {{ flow: "rgba(255, 244, 220, 0.72)", support: "rgba(255, 213, 120, 0.72)", diagnostic: "rgba(255, 176, 154, 0.72)" }};
    function escapeHtml(value) {{
      return String(value || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }}
    function firstNonEmpty(...values) {{
      for (const value of values) {{
        const text = String(value || "").trim();
        if (text) return text;
      }}
      return "";
    }}
    function setText(el, value, fallback = "") {{
      el.textContent = firstNonEmpty(value, fallback);
    }}
    function setList(el, items) {{
      const rows = Array.isArray(items) ? items.filter(Boolean) : [];
      el.innerHTML = rows.length ? rows.map((item) => `<li>${{escapeHtml(item)}}</li>`).join("") : "<li>none</li>";
    }}
    function setMetrics(items) {{
      metricGrid.innerHTML = (Array.isArray(items) ? items : []).map((item) => `<div class="metric"><div class="label">${{escapeHtml(item.label || "")}}</div><div class="value">${{escapeHtml(item.value || "")}}</div></div>`).join("");
    }}
    function setDelta(delta) {{
      const order = [["model_shift","Model shift"],["threshold_shift","Threshold shift"],["consequence_shift","Consequence shift"],["typed_object_expectation","Typed object"],["missing_witness_or_transport","Missing transport"],["route_synopsis","Route synopsis"]];
      const cards = order.map(([key, label]) => [label, delta && delta[key]]).filter(([, value]) => String(value || "").trim()).map(([label, value]) => `<div class="delta-pill"><span class="k">${{escapeHtml(label)}}</span><span class="v">${{escapeHtml(value)}}</span></div>`);
      deltaGrid.innerHTML = cards.join("") || `<div class="delta-pill"><span class="k">Mathematical delta</span><span class="v">No explicit theorem delta declared in this scene.</span></div>`;
    }}
    function buildSceneStrip() {{
      sceneStrip.innerHTML = scenes.map((scene, idx) => `<button class="scene-pill" data-index="${{idx}}"><span class="k">${{escapeHtml(scene.stage || "scene")}}</span><span class="v">${{escapeHtml(scene.title || `Scene ${{idx + 1}}`)}}</span></button>`).join("");
      sceneStrip.querySelectorAll(".scene-pill").forEach((button) => button.addEventListener("click", () => setScene(Number(button.dataset.index || "0"))));
    }}
    function setCandidate(candidate) {{
      const carrier = firstNonEmpty(candidate && candidate.carrier_kind, "No explicit carrier typed for this scene.");
      const typing = firstNonEmpty(candidate && candidate.typing_status, "typing not declared");
      const label = firstNonEmpty(candidate && candidate.label, "No candidate object surfaced.");
      const bridgeDefinition = firstNonEmpty(candidate && candidate.bridge_definition, label);
      const conditionalClaim = firstNonEmpty(candidate && candidate.conditional_claim, "No explicit conditional claim declared.");
      setText(candidateText, `${{label}}. ${{bridgeDefinition}}`);
      setText(claimText, `Typing: ${{typing}}. Carrier: ${{carrier}}. Claim: ${{conditionalClaim}}`);
    }}
    function setSelectedNode(scene, nodeId) {{
      const nodes = Array.isArray(scene.nodes) ? scene.nodes : [];
      const node = nodes.find((item) => item && item.id === nodeId) || nodes.find((item) => item && item.id === scene.spotlight_id) || nodes[0] || {{}};
      selectedNodeId = String(node.id || "");
      setText(selectedNodeTitle, firstNonEmpty(node.detail_title, node.title), "No node selected");
      setText(selectedNodeKind, firstNonEmpty(node.kind, "node"), "node");
      setText(selectedNodeChip, firstNonEmpty(node.chip, node.score), "detail");
      setText(selectedNodeBody, firstNonEmpty(node.detail_body, node.body), "No node-level content available.");
      setList(selectedNodePoints, Array.isArray(node.detail_points) ? node.detail_points : []);
      nodeLayer.querySelectorAll(".node").forEach((el) => el.classList.toggle("selected", el.dataset.nodeId === selectedNodeId));
    }}
    function nodeCenter(node, positionMap) {{
      const hit = positionMap && positionMap.get(node.id);
      if (hit) return hit;
      return {{ x: (Number(node.x || 50) / 100) * 1000, y: (Number(node.y || 50) / 100) * 700 }};
    }}
    function edgePath(source, target) {{
      const dx = Math.max(70, Math.abs(target.x - source.x) * 0.35);
      return `M ${{source.x}} ${{source.y}} C ${{source.x + dx}} ${{source.y}}, ${{target.x - dx}} ${{target.y}}, ${{target.x}} ${{target.y}}`;
    }}
    function renderEdges(scene, positionMap) {{
      const byId = new Map((scene.nodes || []).map((node) => [node.id, node]));
      const svg = [];
      (scene.edges || []).forEach((edge) => {{
        const source = byId.get(edge.source);
        const target = byId.get(edge.target);
        if (!source || !target) return;
        const a = nodeCenter(source, positionMap);
        const b = nodeCenter(target, positionMap);
        const color = EDGE_COLORS[edge.kind] || EDGE_COLORS.flow;
        svg.push(`<g><path d="${{edgePath(a, b)}}" stroke="${{color}}"></path><text class="edge-label" x="${{(a.x + b.x) / 2}}" y="${{(a.y + b.y) / 2 - 10}}" text-anchor="middle">${{escapeHtml(edge.label || "")}}</text></g>`);
      }});
      edgeLayer.innerHTML = svg.join("");
    }}
    function clamp(value, min, max) {{
      return Math.max(min, Math.min(max, value));
    }}
    function resolveNodeLayout(scene) {{
      const frame = nodeLayer.getBoundingClientRect();
      const paddingX = 26;
      const paddingTop = 22;
      const paddingBottom = 136;
      const nodes = Array.from(nodeLayer.querySelectorAll(".node")).map((el) => {{
        const source = (scene.nodes || []).find((item) => item.id === el.dataset.nodeId) || {{}};
        return {{
          el,
          id: String(el.dataset.nodeId || ""),
          x: (Number(source.x || 50) / 100) * frame.width,
          y: (Number(source.y || 50) / 100) * (frame.height - paddingBottom),
          ox: (Number(source.x || 50) / 100) * frame.width,
          oy: (Number(source.y || 50) / 100) * (frame.height - paddingBottom),
          w: el.offsetWidth || 220,
          h: el.offsetHeight || 100,
        }};
      }});
      for (let iter = 0; iter < 80; iter += 1) {{
        nodes.forEach((node) => {{
          node.x += (node.ox - node.x) * 0.035;
          node.y += (node.oy - node.y) * 0.035;
        }});
        for (let i = 0; i < nodes.length; i += 1) {{
          for (let j = i + 1; j < nodes.length; j += 1) {{
            const a = nodes[i];
            const b = nodes[j];
            const minDx = (a.w + b.w) / 2 + 24;
            const minDy = (a.h + b.h) / 2 + 18;
            const dx = a.x - b.x;
            const dy = a.y - b.y;
            const absDx = Math.abs(dx);
            const absDy = Math.abs(dy);
            if (absDx >= minDx || absDy >= minDy) continue;
            const overlapX = minDx - absDx;
            const overlapY = minDy - absDy;
            if (overlapX < overlapY) {{
              const direction = dx === 0 ? (i < j ? -1 : 1) : Math.sign(dx);
              const shift = overlapX * 0.52;
              a.x += direction * shift;
              b.x -= direction * shift;
            }} else {{
              const direction = dy === 0 ? (i < j ? -1 : 1) : Math.sign(dy);
              const shift = overlapY * 0.52;
              a.y += direction * shift;
              b.y -= direction * shift;
            }}
          }}
        }}
        nodes.forEach((node) => {{
          node.x = clamp(node.x, paddingX + node.w / 2, frame.width - paddingX - node.w / 2);
          node.y = clamp(node.y, paddingTop + node.h / 2, frame.height - paddingBottom - node.h / 2);
        }});
      }}
      const positionMap = new Map();
      nodes.forEach((node) => {{
        node.el.style.left = `${{(node.x / frame.width) * 100}}%`;
        node.el.style.top = `${{(node.y / frame.height) * 100}}%`;
        positionMap.set(node.id, {{ x: (node.x / frame.width) * 1000, y: (node.y / frame.height) * 700 }});
      }});
      return positionMap;
    }}
    function updateSpotlight(scene, positionMap) {{
      const hit = scene.spotlight_id ? positionMap.get(scene.spotlight_id) : null;
      if (!hit) {{ spotlight.style.opacity = "0"; return; }}
      spotlight.style.opacity = "1";
      spotlight.style.left = `${{(hit.x / 1000) * 100}}%`;
      spotlight.style.top = `${{(hit.y / 700) * 100}}%`;
    }}
    function renderNodes(scene) {{
      nodeLayer.innerHTML = (scene.nodes || []).map((node, idx) => `<article class="node ${{escapeHtml(node.kind || "support")}} ${{node.emphasis ? "emphasis" : ""}}" data-node-id="${{escapeHtml(node.id || "")}}" style="left:${{Number(node.x || 50)}}%; top:${{Number(node.y || 50)}}%; transition-delay:${{Math.min(idx * 90, 480)}}ms"><div class="chip-row"><span class="chip">${{escapeHtml(node.chip || node.kind || "")}}</span><span class="score">${{escapeHtml(node.score || "")}}</span></div><h3>${{escapeHtml(node.title || "")}}</h3><p>${{escapeHtml(node.body || "")}}</p></article>`).join("");
      requestAnimationFrame(() => nodeLayer.querySelectorAll(".node").forEach((node) => node.classList.add("visible")));
      const positionMap = resolveNodeLayout(scene);
      nodeLayer.querySelectorAll(".node").forEach((node) => node.addEventListener("click", () => setSelectedNode(scene, node.dataset.nodeId || "")));
      updateSpotlight(scene, positionMap);
      setSelectedNode(scene, selectedNodeId || scene.spotlight_id || ((scene.nodes || [])[0] || {{}}).id || "");
      return positionMap;
    }}
    function renderCaptions(scene) {{
      if (captionTimer) {{ clearInterval(captionTimer); captionTimer = null; }}
      const captions = Array.isArray(scene.voiceover) && scene.voiceover.length ? scene.voiceover : [scene.headline || scene.subtitle || ""];
      let index = 0;
      captionText.textContent = captions[0] || "";
      if (captions.length > 1) {{
        captionTimer = setInterval(() => {{
          index = (index + 1) % captions.length;
          captionText.textContent = captions[index] || "";
        }}, Math.max(1500, 3000 / Number(speedSelect.value || "1")));
      }}
    }}
    function updateScenePills() {{ sceneStrip.querySelectorAll(".scene-pill").forEach((pill, idx) => pill.classList.toggle("active", idx === currentIndex)); }}
    function renderScene(index) {{
      const scene = scenes[index] || {{}};
      currentIndex = index;
      sceneTitle.textContent = scene.title || "Conceptual Space Animation";
      sceneSubtitle.textContent = scene.subtitle || "";
      sceneCounter.textContent = `Scene ${{index + 1}} / ${{scenes.length}}`;
      sceneHeading.textContent = scene.title || "";
      headlineText.textContent = scene.headline || "No scene headline available.";
      reasoningText.textContent = scene.reasoning_declaration || "No explicit reasoning declaration available.";
      mathText.textContent = scene.mathematical_declaration || "No explicit mathematical declaration available.";
      routeText.textContent = scene.route_synopsis || "No explicit route synopsis surfaced in this scene.";
      sourceText.textContent = scene.source_excerpt || "No source theorem excerpt surfaced in this scene.";
      targetText.textContent = scene.target_excerpt || "No target theorem excerpt surfaced in this scene.";
      failureText.textContent = scene.failure_diagnosis || "No explicit failure diagnosis declared for this scene.";
      counterfactualText.textContent = scene.counterfactual || "No counterfactual probe declared for this scene.";
      setCandidate(scene.candidate_object || {{}});
      setMetrics(scene.metrics || []);
      setDelta(scene.statement_delta || {{}});
      setList(assumptionList, scene.assumptions || []);
      setList(obligationList, scene.obligations || []);
      setList(lemmaList, scene.lemmas || []);
      setList(outlineList, scene.proof_outline || []);
      const positionMap = renderNodes(scene);
      renderEdges(scene, positionMap);
      renderCaptions(scene);
      range.value = String(index);
      metaText.textContent = `declared nodes: ${{(scene.nodes || []).length}} | declared edges: ${{(scene.edges || []).length}}`;
      updateScenePills();
    }}
    function stopPlayback() {{ if (playbackTimer) {{ clearInterval(playbackTimer); playbackTimer = null; }} playBtn.textContent = "Play"; }}
    function startPlayback() {{
      stopPlayback();
      playBtn.textContent = "Pause";
      playbackTimer = setInterval(() => {{
        const next = currentIndex + 1;
        if (next >= scenes.length) {{ stopPlayback(); return; }}
        renderScene(next);
      }}, Math.max(2200, 5600 / Number(speedSelect.value || "1")));
    }}
    function togglePlayback() {{ if (playbackTimer) stopPlayback(); else startPlayback(); }}
    function setScene(index) {{ renderScene(Math.max(0, Math.min(scenes.length - 1, index))); }}
    range.max = String(Math.max(0, scenes.length - 1));
    prevBtn.addEventListener("click", () => setScene(currentIndex - 1));
    nextBtn.addEventListener("click", () => setScene(currentIndex + 1));
    playBtn.addEventListener("click", togglePlayback);
    range.addEventListener("input", () => setScene(Number(range.value || "0")));
    speedSelect.addEventListener("change", () => {{ if (playbackTimer) startPlayback(); renderCaptions(scenes[currentIndex] || {{}}); }});
    window.addEventListener("resize", () => renderScene(currentIndex));
    buildSceneStrip();
    renderScene(0);
  </script>
</body>
</html>
"""


def main() -> int:
    logger = ReasoningLogger("kb-conceptual-space-animation")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref> directory.")
    ap.add_argument("--conceptual-dynamics", default="", help="Optional conceptual-dynamics JSON path.")
    ap.add_argument("--output-json", default="", help="Output path for conceptual-space-animation JSON.")
    ap.add_argument("--output-md", default="", help="Output path for conceptual-space-animation Markdown.")
    ap.add_argument("--output-html", default="", help="Output path for conceptual-space-animation HTML.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()
    conceptual_path = Path(args.conceptual_dynamics) if args.conceptual_dynamics else artifacts_dir / "conceptual-dynamics.json"
    if not conceptual_path.is_absolute():
        conceptual_path = (repo_root / conceptual_path).resolve()
    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "conceptual-space-animation.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "conceptual-space-animation.md"
    output_html = Path(args.output_html) if args.output_html else artifacts_dir / "conceptual-space-animation.html"

    logger.step(
        "Parsed conceptual-space-animation arguments",
        "\n".join(
            [
                f"artifacts_dir={artifacts_dir}",
                f"conceptual_dynamics={conceptual_path}",
                f"output_json={output_json}",
                f"output_md={output_md}",
                f"output_html={output_html}",
            ]
        ),
        surface_focus="conceptual-space-animation",
        surface_stage="conceptual-space-animation",
    )

    if not conceptual_path.exists():
        log_path = logger.finalize("error", summary=f"Conceptual dynamics JSON not found: {conceptual_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Conceptual dynamics JSON not found: {conceptual_path}")

    conceptual_report = _load_json(conceptual_path)
    animation_report = _build_animation_report(conceptual_report, source_path=str(conceptual_path))

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_html.parent.mkdir(parents=True, exist_ok=True)

    output_json.write_text(json.dumps(animation_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(_to_markdown(animation_report), encoding="utf-8")
    output_html.write_text(_render_html(animation_report), encoding="utf-8")

    logger.step(
        "Built conceptual-space animation",
        "\n".join(
            [
                f"scene_count={_ensure_dict(animation_report.get('summary')).get('scene_count', 0)}",
                f"declared_nodes={_ensure_dict(animation_report.get('summary')).get('declared_node_count', 0)}",
                f"declared_edges={_ensure_dict(animation_report.get('summary')).get('declared_edge_count', 0)}",
            ]
        ),
        surface_focus="conceptual-space-animation",
        surface_stage="conceptual-space-animation",
        surface_metrics={
            "scene_count": _ensure_dict(animation_report.get("summary")).get("scene_count", 0),
            "declared_node_count": _ensure_dict(animation_report.get("summary")).get("declared_node_count", 0),
            "declared_edge_count": _ensure_dict(animation_report.get("summary")).get("declared_edge_count", 0),
        },
        surface_taxonomy={"reasoning_types": ["conceptual-space-animation"]},
    )

    logger.add_output("conceptual_space_animation_json", output_json)
    logger.add_output("conceptual_space_animation_md", output_md)
    logger.add_output("conceptual_space_animation_html", output_html)
    log_path = logger.finalize(
        "success",
        summary=(
            f"Generated conceptual-space animation with "
            f"{_ensure_dict(animation_report.get('summary')).get('scene_count', 0)} scenes."
        ),
    )
    print(f"[OK] Wrote conceptual space animation JSON: {output_json}")
    print(f"[OK] Wrote conceptual space animation Markdown: {output_md}")
    print(f"[OK] Wrote conceptual space animation HTML: {output_html}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
