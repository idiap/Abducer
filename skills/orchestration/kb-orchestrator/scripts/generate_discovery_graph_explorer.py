#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Generate a dynamic JavaScript explorer for conceptual discovery graphs."""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import Counter
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import canonical_artifacts_dir
from kb_context import resolve_kb_reference
from reasoning_log import ReasoningLogger
from statement_text import load_statement_index
from statement_text import humanize_schema_label
from statement_text import normalize_math_text
from statement_text import statement_excerpt


STAGE_SPECS: tuple[dict[str, Any], ...] = (
    {
        "key": "analysis",
        "label": "Landscape Model",
        "origins": ("analysis",),
        "artifact_kinds": ("connection-analysis",),
        "description": "Build the base concept landscape from axioms, theorems, methods, signatures, and dependency-adjacent relations.",
    },
    {
        "key": "phyp",
        "label": "Bridge Hypotheses",
        "origins": ("phyp",),
        "artifact_kinds": ("phyp",),
        "description": "Promote potential links into explicit bridge hypotheses with antecedents, consequences, invariants, and barrier scopes.",
    },
    {
        "key": "coherence",
        "label": "Coherence Layer",
        "origins": ("coherence",),
        "artifact_kinds": ("coherence-report",),
        "description": "Expose support, attack, explanation, and reframing relations so local bridge moves can be judged against theory-wide fit.",
    },
    {
        "key": "hardness",
        "label": "Barrier Diagnosis",
        "origins": ("hardness",),
        "artifact_kinds": ("epistemic-hardness",),
        "description": "Add explicit epistemic bottlenecks so the graph shows why certain bridge moves remain blocked or underdetermined.",
    },
    {
        "key": "bridge-plan",
        "label": "Bridge Programs",
        "origins": ("bridge-plan",),
        "artifact_kinds": ("bridge-plan",),
        "description": "Turn promising interfaces into concrete bridge programs linking source statements, target statements, and inferential commitments.",
    },
    {
        "key": "conjecture",
        "label": "Abstraction Conjectures",
        "origins": ("conjecture",),
        "artifact_kinds": ("concept-gap-abstractions",),
        "description": "Conjecture missing bridge objects and abstraction families that could make the remaining conceptual gaps testable.",
    },
    {
        "key": "proof-sketch",
        "label": "Proof Sketches",
        "origins": ("proof-sketch",),
        "artifact_kinds": ("proof-sketches",),
        "description": "Introduce theorem-pair proof routes with explicit obligations, lemma chains, and failure probes so the graph reflects mathematical construction rather than only bridge intent.",
    },
)

STAGE_INDEX = {spec["key"]: idx for idx, spec in enumerate(STAGE_SPECS)}
ORIGIN_TO_STAGE = {
    origin: spec["key"]
    for spec in STAGE_SPECS
    for origin in spec.get("origins", ())
}
ARTIFACT_KIND_TO_STAGE = {
    artifact_kind: spec["key"]
    for spec in STAGE_SPECS
    for artifact_kind in spec.get("artifact_kinds", ())
}

TYPE_TO_FAMILY = {
    "statement": "proposition",
    "claim-signature": "concept",
    "antecedent-signature": "concept",
    "consequence-signature": "concept",
    "implication-signature": "concept",
    "concept": "concept",
    "complexity-class": "concept",
    "problem": "concept",
    "model-signature": "concept",
    "reduction-signature": "concept",
    "proof-regime": "concept",
    "method": "concept",
    "barrier": "concept",
    "barrier-signal": "concept",
    "hypothesis": "proposition",
    "bridge-program": "proof-object",
    "abstraction-conjecture": "proof-object",
    "abstraction-family": "proof-object",
    "proof-sketch": "proof-object",
    "hardness-element": "proposition",
    "anchor-concept": "concept",
    "invariant": "proof-object",
    "unknown": "concept",
}

TYPE_TO_ROLE = {
    "statement": "proposition",
    "claim-signature": "claim-concept",
    "antecedent-signature": "antecedent-concept",
    "consequence-signature": "consequence-concept",
    "implication-signature": "transfer-concept",
    "concept": "concept",
    "complexity-class": "complexity-class",
    "problem": "problem",
    "model-signature": "model-regime",
    "reduction-signature": "reduction-schema",
    "proof-regime": "proof-regime",
    "method": "proof-method",
    "barrier": "barrier-concept",
    "barrier-signal": "barrier-concept",
    "hypothesis": "hypothesis",
    "bridge-program": "bridge-program",
    "abstraction-conjecture": "bridge-object",
    "abstraction-family": "object-family",
    "proof-sketch": "proof-sketch",
    "hardness-element": "obstruction-claim",
    "anchor-concept": "anchor-concept",
    "invariant": "invariant",
    "unknown": "concept",
}

ANALYSIS_NODE_TYPES = {
    "statement",
    "concept",
    "complexity-class",
    "problem",
    "proof-regime",
    "barrier",
    "barrier-signal",
}

COHERENCE_NODE_TYPES = {
    "statement",
    "hypothesis",
    "barrier",
}

EDGE_RELATION_PRIORITY = {
    "explains": 9,
    "defines": 8,
    "supports": 8,
    "reframes": 7,
    "preserves": 7,
    "proposes": 7,
    "grounds": 7,
    "targets": 7,
    "instantiates": 6,
    "confronts": 6,
    "depends_on": 5,
    "anchors": 5,
    "invokes": 5,
    "motivates": 5,
    "articulates": 5,
    "situates_in": 4,
    "obstructs": 3,
}

EDGE_SOURCE_TOTAL_LIMITS = {
    "analysis": 2,
    "coherence": 2,
}

EDGE_SOURCE_RELATION_LIMITS = {
    ("analysis", "situates_in"): 2,
    ("analysis", "confronts"): 1,
    ("analysis", "reframes"): 1,
    ("coherence", "obstructs"): 1,
    ("coherence", "supports"): 1,
    ("coherence", "reframes"): 1,
    ("coherence", "defines"): 1,
    ("coherence", "explains"): 1,
}


def _safe_float(value: Any, default: float = 0.0) -> float:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Defensive conversion/parsing to keep graph assembly robust.
    Contribution: Prevents malformed artifacts from destabilizing visualization generation.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clean_display_text(value: Any, *, limit: int = 0) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Display-oriented normalization of textual mathematical content.
    Contribution: Keeps graph inspectors readable when upstream artifacts contain long theorem excerpts or noisy whitespace.
    """

    text = " ".join(str(value or "").split()).strip()
    if limit and len(text) > limit:
        text = text[: max(0, limit - 3)].rstrip() + "..."
    return text


def _clean_display_list(values: Any, *, limit: int = 4, text_limit: int = 220) -> list[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable compaction of short textual content lists.
    Contribution: Lets the graph inspector expose obligations, lemmas, and assumptions without flooding the panel.
    """

    if not isinstance(values, list):
        return []
    out: list[str] = []
    seen: set[str] = set()
    for item in values:
        text = _clean_display_text(item, limit=text_limit)
        if text and text not in seen:
            seen.add(text)
            out.append(text)
        if len(out) >= limit:
            break
    return out


def _first_nonempty(*values: Any, limit: int = 0) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Fallback selection across multiple candidate text fields.
    Contribution: Prefers theorem-grounded wording when multiple artifact stages describe the same node.
    """

    for value in values:
        text = _clean_display_text(value, limit=limit)
        if text:
            return text
    return ""


def _extract_text_rows(rows: Any, *, keys: tuple[str, ...], limit: int = 4, text_limit: int = 220) -> list[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Projection of structured row lists into human-readable strings.
    Contribution: Makes proof obligations and lemma chains inspectable inside the graph explorer.
    """

    if not isinstance(rows, list):
        return []
    out: list[str] = []
    seen: set[str] = set()
    for row in rows:
        if isinstance(row, dict):
            text = _first_nonempty(*(row.get(key, "") for key in keys), limit=text_limit)
        else:
            text = _clean_display_text(row, limit=text_limit)
        if text and text not in seen:
            seen.add(text)
            out.append(text)
        if len(out) >= limit:
            break
    return out


def _statement_delta_payload(delta: Any) -> dict[str, str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Compact serialization of theorem-pair deltas.
    Contribution: Gives selected graph nodes a mathematically meaningful before/after description.
    """

    if not isinstance(delta, dict):
        return {}
    limits = {
        "source_problem_family": 120,
        "target_problem_family": 120,
        "source_model": 160,
        "target_model": 160,
        "source_claim_focus": 180,
        "target_claim_focus": 180,
        "route_synopsis": 320,
        "model_shift": 220,
        "threshold_shift": 220,
        "consequence_shift": 260,
        "typed_object_expectation": 180,
        "typing_status": 60,
        "missing_witness_or_transport": 260,
    }
    out: dict[str, str] = {}
    for key in (
        "source_problem_family",
        "target_problem_family",
        "source_model",
        "target_model",
        "source_claim_focus",
        "target_claim_focus",
        "route_synopsis",
        "model_shift",
        "threshold_shift",
        "consequence_shift",
        "typed_object_expectation",
        "typing_status",
        "missing_witness_or_transport",
    ):
        text = _clean_display_text(delta.get(key, ""), limit=limits.get(key, 220))
        if text:
            out[key] = text
    return out


def _merge_detail_value(existing: Any, new_value: Any) -> Any:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Non-destructive merge for node-detail payloads.
    Contribution: Allows later stages to enrich existing bridge nodes without discarding earlier provenance.
    """

    if existing in (None, "", [], {}):
        return new_value
    if new_value in (None, "", [], {}):
        return existing
    if isinstance(existing, dict) and isinstance(new_value, dict):
        out = dict(existing)
        for key, value in new_value.items():
            out[str(key)] = _merge_detail_value(out.get(str(key)), value)
        return out
    if isinstance(existing, list) and isinstance(new_value, list):
        out = list(existing)
        for value in new_value:
            if value not in out:
                out.append(value)
        return out
    if isinstance(existing, str) and isinstance(new_value, str):
        return new_value if len(new_value) > len(existing) else existing
    return new_value


def _clean_anchor_label(value: Any) -> str:
    """
    Relevance: Operates within the graph-explorer synthesis layer.
    Concept: Canonical normalization for human-facing anchor labels.
    Contribution: Prevents the explorer from surfacing raw schema signatures or lightly corrupted theorem text as concept labels.
    """

    raw = str(value or "").strip()
    if not raw:
        return ""
    if any(token in raw for token in ("\\", "Qtext", "Rightarrow", "mathcal", "mathbb", "emph")):
        return normalize_math_text(raw)
    return humanize_schema_label(raw) or raw


def _merge_detail_dict(existing: Any, new_value: Any) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Merge helper for rich node-detail payloads.
    Contribution: Preserves theorem excerpts, obligations, and proof content across multiple discovery stages.
    """

    base = existing if isinstance(existing, dict) else {}
    extra = new_value if isinstance(new_value, dict) else {}
    out = dict(base)
    for key, value in extra.items():
        out[str(key)] = _merge_detail_value(out.get(str(key)), value)
    return out


def _detail_payload(
    *,
    route_synopsis: str = "",
    statement_excerpt: str = "",
    source_excerpt: str = "",
    target_excerpt: str = "",
    statement_delta: Any = None,
    carrier_kind: str = "",
    typing_status: str = "",
    bridge_definition: str = "",
    conditional_claim: str = "",
    assumptions: Any = None,
    obligations: Any = None,
    lemmas: Any = None,
    proof_outline: Any = None,
    failure_diagnosis: str = "",
    counterfactual: str = "",
    context_points: Any = None,
    related_routes: Any = None,
    linked_objects: Any = None,
    expert_actions: Any = None,
    evidence: Any = None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Normalized content payload for graph nodes.
    Contribution: Gives the selected-node inspector a stable theorem/proof schema regardless of artifact source.
    """

    return {
        "route_synopsis": _clean_display_text(route_synopsis, limit=320),
        "statement_excerpt": _clean_display_text(statement_excerpt, limit=320),
        "source_excerpt": _clean_display_text(source_excerpt, limit=300),
        "target_excerpt": _clean_display_text(target_excerpt, limit=300),
        "statement_delta": _statement_delta_payload(statement_delta),
        "carrier_kind": _clean_display_text(carrier_kind, limit=180),
        "typing_status": _clean_display_text(typing_status, limit=60),
        "bridge_definition": _clean_display_text(bridge_definition, limit=380),
        "conditional_claim": _clean_display_text(conditional_claim, limit=340),
        "assumptions": _clean_display_list(assumptions, limit=4, text_limit=220),
        "obligations": _clean_display_list(obligations, limit=5, text_limit=220),
        "lemmas": _clean_display_list(lemmas, limit=5, text_limit=220),
        "proof_outline": _clean_display_list(proof_outline, limit=4, text_limit=220),
        "failure_diagnosis": _clean_display_text(failure_diagnosis, limit=280),
        "counterfactual": _clean_display_text(counterfactual, limit=280),
        "context_points": _clean_display_list(context_points, limit=6, text_limit=180),
        "related_routes": _clean_display_list(related_routes, limit=5, text_limit=240),
        "linked_objects": _clean_display_list(linked_objects, limit=8, text_limit=180),
        "expert_actions": _clean_display_list(expert_actions, limit=5, text_limit=220),
        "evidence": _clean_display_list(evidence, limit=5, text_limit=220),
    }


def _generic_detail_from_meta(row: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Lightweight content extraction for nodes without proof-specific schemas.
    Contribution: Ensures even analysis, hypothesis, and hardness nodes have meaningful inspector summaries.
    """

    if not isinstance(row, dict):
        return {}
    summary = _first_nonempty(
        row.get("rationale", ""),
        row.get("description", ""),
        row.get("summary", ""),
        row.get("significance", ""),
        limit=320,
    )
    obligations = _clean_display_list(
        [row.get("preserved_invariant", ""), row.get("barrier_scope", ""), row.get("severity", "")],
        limit=3,
        text_limit=180,
    )
    return _detail_payload(route_synopsis=summary, obligations=obligations)


def _node_statement_id(node: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable recovery of a canonical statement id from heterogeneous node encodings.
    Contribution: Lets the explorer enrich statement nodes from the KB and route artifacts after graph assembly.
    """

    if not isinstance(node, dict):
        return ""
    meta = node.get("meta", {}) if isinstance(node.get("meta"), dict) else {}
    statement_id = str(meta.get("statement_id", "")).strip()
    if statement_id:
        return statement_id
    node_id = str(node.get("id", "")).strip()
    if node_id.startswith("statement:"):
        return node_id.split(":", 1)[1].strip()
    return ""


def _merge_text_values(*value_groups: Any, limit: int = 5, text_limit: int = 220) -> list[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable union of short human-readable text lists.
    Contribution: Allows node dossiers to accumulate route content from multiple artifacts without repetition.
    """

    out: list[str] = []
    seen: set[str] = set()
    for group in value_groups:
        if isinstance(group, list):
            items = group
        elif group in (None, ""):
            items = []
        else:
            items = [group]
        for item in items:
            text = _clean_display_text(item, limit=text_limit)
            if text and text not in seen:
                seen.add(text)
                out.append(text)
            if len(out) >= limit:
                return out
    return out


def _route_preview(detail: dict[str, Any]) -> str:
    """
    Relevance: Operates within the graph-explorer synthesis layer.
    Concept: Compact route-summary extraction from a node detail payload.
    Contribution: Gives non-route nodes access to the strongest nearby mathematical route summaries.
    """

    if not isinstance(detail, dict):
        return ""
    return _first_nonempty(
        detail.get("route_synopsis", ""),
        detail.get("conditional_claim", ""),
        detail.get("statement_excerpt", ""),
        limit=320,
    )


def _neighbor_object_label(node: dict[str, Any], relation: str) -> str:
    """
    Relevance: Operates within the graph-explorer synthesis layer.
    Concept: Compact label for nearby graph objects.
    Contribution: Makes inspector dossiers explain which proof objects and statements are attached to a node.
    """

    label = str(node.get("label", "")).strip() or str(node.get("id", "")).strip()
    relation_text = str(relation or "").strip().replace("_", " ")
    if relation_text:
        return f"{label} ({relation_text})"
    return label


def _expert_bridge_rows(expert_paper: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the graph-explorer synthesis layer.
    Concept: Canonical extraction of bridge-first expert rows from the expert paper artifact.
    Contribution: Lets the explorer reuse expert-facing mathematical dossiers to enrich node inspection content.
    """

    if not isinstance(expert_paper, dict):
        return []
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for key in ("bridge_portfolio", "recommended_bridges"):
        payload = expert_paper.get(key, [])
        if not isinstance(payload, list):
            continue
        for row in payload:
            if not isinstance(row, dict):
                continue
            bridge_id = str(row.get("bridge_id", "")).strip()
            signature = bridge_id or json.dumps(row, sort_keys=True, ensure_ascii=False)
            if signature in seen:
                continue
            seen.add(signature)
            rows.append(row)
    return rows


def _recommended_hypothesis_rows(expert_paper: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the graph-explorer synthesis layer.
    Concept: Canonical extraction of expert-recommended hypotheses.
    Contribution: Makes hypothesis nodes inspectable in the same expert vocabulary used by the paper artifact.
    """

    payload = expert_paper.get("recommended_hypotheses", []) if isinstance(expert_paper, dict) else []
    if not isinstance(payload, list):
        return []
    return [row for row in payload if isinstance(row, dict)]


def _enrich_graph_details(
    nodes: dict[str, dict[str, Any]],
    edges: list[dict[str, Any]],
    *,
    statement_index: dict[str, dict[str, Any]],
    analysis: dict[str, Any],
    expert_paper: dict[str, Any],
) -> None:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Post-assembly enrichment of node dossiers from KB statements, local neighborhoods, and expert artifacts.
    Contribution: Prevents the graph explorer from being visually rich but mathematically thin, especially for statement and concept nodes.
    """

    adjacency: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for edge in edges:
        source = str(edge.get("source", "")).strip()
        target = str(edge.get("target", "")).strip()
        relation = str(edge.get("type", "related")).strip() or "related"
        if source and target:
            adjacency[source].append((relation, target))
            adjacency[target].append((relation, source))

    intervention_by_statement: dict[str, dict[str, Any]] = {}
    concept_focus_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in analysis.get("top_interventions", []) if isinstance(analysis.get("top_interventions"), list) else []:
        if not isinstance(row, dict):
            continue
        statement_id = str(row.get("statement_id", "")).strip()
        if statement_id:
            intervention_by_statement[statement_id] = row
        for concept in row.get("concept_focus", []) if isinstance(row.get("concept_focus"), list) else []:
            concept_text = _clean_anchor_label(concept)
            if concept_text:
                concept_focus_index[concept_text].append(row)

    expert_bridge_by_statement: dict[str, list[dict[str, Any]]] = defaultdict(list)
    expert_bridge_by_label: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in _expert_bridge_rows(expert_paper):
        for key in ("source_statement_id", "target_statement_id"):
            statement_id = str(row.get(key, "")).strip()
            if statement_id:
                expert_bridge_by_statement[statement_id].append(row)
        labels = [
            row.get("abstraction_label", ""),
            row.get("preserved_invariant", ""),
            row.get("support_antecedent_schema", ""),
            row.get("target_consequence_schema", ""),
        ]
        delta = row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}
        labels.extend(
            [
                delta.get("source_problem_family", ""),
                delta.get("target_problem_family", ""),
                delta.get("source_claim_focus", ""),
                delta.get("target_claim_focus", ""),
            ]
        )
        for label in labels:
            label_text = _clean_anchor_label(label)
            if label_text:
                expert_bridge_by_label[label_text].append(row)

    expert_hypothesis_by_node: dict[str, list[dict[str, Any]]] = defaultdict(list)
    expert_hypothesis_by_statement: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in _recommended_hypothesis_rows(expert_paper):
        hypothesis_id = str(row.get("hypothesis_id", "")).strip()
        if hypothesis_id:
            expert_hypothesis_by_node[f"hypothesis:{hypothesis_id}"].append(row)
        for key in ("support_statement_id", "target_statement_id"):
            statement_id = str(row.get(key, "")).strip()
            if statement_id:
                expert_hypothesis_by_statement[statement_id].append(row)

    for node in nodes.values():
        if str(node.get("type", "")).strip() != "statement":
            continue
        detail = node.get("detail", {}) if isinstance(node.get("detail"), dict) else {}
        statement_id = _node_statement_id(node)
        statement_row = statement_index.get(statement_id, {}) if statement_id else {}
        excerpt = statement_excerpt(statement_row, limit=320)
        if excerpt and not _clean_display_text(detail.get("statement_excerpt", "")):
            detail["statement_excerpt"] = excerpt

        intervention = intervention_by_statement.get(statement_id, {})
        if isinstance(intervention, dict) and intervention:
            if not _clean_display_text(detail.get("route_synopsis", "")):
                detail["route_synopsis"] = _first_nonempty(intervention.get("rationale", ""), limit=320)
            detail["context_points"] = _merge_text_values(
                detail.get("context_points", []),
                [_clean_anchor_label(item) for item in intervention.get("concept_focus", []) if _clean_anchor_label(item)],
                limit=6,
                text_limit=180,
            )
            evidence_rows: list[str] = []
            partner = str(intervention.get("best_cross_component_partner", "")).strip()
            if partner:
                evidence_rows.append(f"Best cross-component partner: {partner}")
            score = intervention.get("score")
            if score is not None:
                evidence_rows.append(f"Intervention score: {_safe_float(score):.4f}")
            evidence_rows.append(_first_nonempty(intervention.get("rationale", ""), limit=220))
            detail["evidence"] = _merge_text_values(
                detail.get("evidence", []),
                evidence_rows,
                limit=5,
                text_limit=220,
            )

        for row in expert_bridge_by_statement.get(statement_id, []):
            detail["related_routes"] = _merge_text_values(
                detail.get("related_routes", []),
                row.get("route_synopsis", ""),
                limit=5,
                text_limit=240,
            )
            detail["linked_objects"] = _merge_text_values(
                detail.get("linked_objects", []),
                _first_nonempty(row.get("abstraction_label", ""), row.get("bridge_id", ""), limit=180),
                limit=8,
                text_limit=180,
            )
            detail["expert_actions"] = _merge_text_values(
                detail.get("expert_actions", []),
                row.get("expert_actions", []),
                limit=5,
                text_limit=220,
            )
            detail["obligations"] = _merge_text_values(
                detail.get("obligations", []),
                row.get("proof_obligations", []),
                limit=5,
                text_limit=220,
            )
            detail["lemmas"] = _merge_text_values(
                detail.get("lemmas", []),
                row.get("candidate_lemmas", []),
                limit=5,
                text_limit=220,
            )
            detail["proof_outline"] = _merge_text_values(
                detail.get("proof_outline", []),
                row.get("proof_outline", []),
                row.get("expert_actions", []),
                limit=5,
                text_limit=220,
            )
        for row in expert_hypothesis_by_statement.get(statement_id, []):
            detail["expert_actions"] = _merge_text_values(
                detail.get("expert_actions", []),
                row.get("expert_actions", []),
                limit=5,
                text_limit=220,
            )
            detail["evidence"] = _merge_text_values(
                detail.get("evidence", []),
                _first_nonempty(row.get("kind", ""), row.get("tier", ""), limit=180),
                limit=5,
                text_limit=180,
            )
        node["detail"] = detail

    for node in nodes.values():
        detail = node.get("detail", {}) if isinstance(node.get("detail"), dict) else {}
        route_summaries: list[str] = []
        neighbor_excerpts: list[str] = []
        linked_objects: list[str] = []
        obligations: list[str] = []
        lemmas: list[str] = []
        proof_outline: list[str] = []
        expert_actions: list[str] = []
        evidence: list[str] = []
        context_points: list[str] = []

        for relation, neighbor_id in adjacency.get(str(node.get("id", "")).strip(), []):
            neighbor = nodes.get(neighbor_id)
            if not isinstance(neighbor, dict):
                continue
            linked_objects.append(_neighbor_object_label(neighbor, relation))
            neighbor_detail = neighbor.get("detail", {}) if isinstance(neighbor.get("detail"), dict) else {}
            if str(neighbor.get("family", "")).strip() == "proof-object":
                route_preview = _route_preview(neighbor_detail)
                if route_preview:
                    route_summaries.append(route_preview)
                obligations.extend(neighbor_detail.get("obligations", []) if isinstance(neighbor_detail.get("obligations"), list) else [])
                lemmas.extend(neighbor_detail.get("lemmas", []) if isinstance(neighbor_detail.get("lemmas"), list) else [])
                proof_outline.extend(neighbor_detail.get("proof_outline", []) if isinstance(neighbor_detail.get("proof_outline"), list) else [])
                expert_actions.extend(neighbor_detail.get("expert_actions", []) if isinstance(neighbor_detail.get("expert_actions"), list) else [])
            if str(neighbor.get("type", "")).strip() == "statement":
                excerpt = _first_nonempty(
                    neighbor_detail.get("statement_excerpt", ""),
                    neighbor_detail.get("source_excerpt", ""),
                    neighbor_detail.get("target_excerpt", ""),
                    limit=320,
                )
                if excerpt:
                    neighbor_excerpts.append(excerpt)
                statement_route = _route_preview(neighbor_detail)
                if statement_route and str(node.get("type", "")).strip() != "statement":
                    route_summaries.append(statement_route)
            if str(neighbor.get("family", "")).strip() == "concept":
                context_points.append(str(neighbor.get("label", "")).strip())

        statement_id = _node_statement_id(node)
        if statement_id:
            for row in expert_bridge_by_statement.get(statement_id, []):
                route_summaries.append(_first_nonempty(row.get("route_synopsis", ""), limit=320))
                expert_actions.extend(row.get("expert_actions", []) if isinstance(row.get("expert_actions"), list) else [])
        else:
            label_text = _clean_anchor_label(node.get("label", ""))
            if label_text:
                for row in concept_focus_index.get(label_text, []):
                    route_summaries.append(_first_nonempty(row.get("rationale", ""), limit=320))
                    evidence.append(_first_nonempty(row.get("statement_id", ""), limit=120))
                for row in expert_bridge_by_label.get(label_text, []):
                    route_summaries.append(_first_nonempty(row.get("route_synopsis", ""), limit=320))
                    expert_actions.extend(row.get("expert_actions", []) if isinstance(row.get("expert_actions"), list) else [])
                    obligations.extend(row.get("proof_obligations", []) if isinstance(row.get("proof_obligations"), list) else [])
                    lemmas.extend(row.get("candidate_lemmas", []) if isinstance(row.get("candidate_lemmas"), list) else [])
                    proof_outline.extend(row.get("proof_outline", []) if isinstance(row.get("proof_outline"), list) else [])

        if not _clean_display_text(detail.get("route_synopsis", "")):
            node_type = str(node.get("type", "")).strip()
            if route_summaries:
                if node_type == "invariant":
                    detail["route_synopsis"] = _clean_display_text(
                        f"Preserved across {len(route_summaries)} active routes. Strongest route: {route_summaries[0]}",
                        limit=320,
                    )
                elif node_type == "anchor-concept":
                    detail["route_synopsis"] = _clean_display_text(
                        f"Anchors {len(route_summaries)} active abstraction or proof routes. Strongest route: {route_summaries[0]}",
                        limit=320,
                    )
                elif node_type == "statement":
                    detail["route_synopsis"] = route_summaries[0]
                else:
                    detail["route_synopsis"] = _clean_display_text(
                        f"Connected to {len(route_summaries)} active routes. Strongest route: {route_summaries[0]}",
                        limit=320,
                    )
            elif node_type == "statement" and _clean_display_text(detail.get("statement_excerpt", "")):
                detail["route_synopsis"] = _clean_display_text(
                    f"Canonical statement in the current search space: {detail.get('statement_excerpt', '')}",
                    limit=320,
                )

        if neighbor_excerpts and not _clean_display_text(detail.get("statement_excerpt", "")) and str(node.get("type", "")).strip() != "statement":
            detail["statement_excerpt"] = neighbor_excerpts[0]

        detail["context_points"] = _merge_text_values(
            detail.get("context_points", []),
            context_points,
            limit=6,
            text_limit=180,
        )
        detail["related_routes"] = _merge_text_values(
            detail.get("related_routes", []),
            route_summaries,
            limit=5,
            text_limit=240,
        )
        detail["linked_objects"] = _merge_text_values(
            detail.get("linked_objects", []),
            linked_objects,
            limit=8,
            text_limit=180,
        )
        detail["expert_actions"] = _merge_text_values(
            detail.get("expert_actions", []),
            expert_actions,
            limit=5,
            text_limit=220,
        )
        detail["evidence"] = _merge_text_values(
            detail.get("evidence", []),
            evidence,
            limit=5,
            text_limit=220,
        )
        detail["obligations"] = _merge_text_values(
            detail.get("obligations", []),
            obligations,
            limit=5,
            text_limit=220,
        )
        detail["lemmas"] = _merge_text_values(
            detail.get("lemmas", []),
            lemmas,
            limit=5,
            text_limit=220,
        )
        detail["proof_outline"] = _merge_text_values(
            detail.get("proof_outline", []),
            proof_outline,
            limit=5,
            text_limit=220,
        )
        node["detail"] = detail


def _load_json(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides typed inputs for graph assembly and timeline synthesis.
    """

    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_yaml(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Allows the discovery explorer to treat hypothesis artifacts as first-class graph inputs.
    """

    if not path.exists():
        return {}
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _node_label(node: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable label normalization for heterogeneous node payloads.
    Contribution: Keeps the explorer interpretable across mixed artifact schemas.
    """

    for key in ("label", "abstraction_label", "statement_id", "name", "id"):
        value = str(node.get(key, "")).strip()
        if value:
            return value
    return "node"


def _stage_key_for_origin(origin: str) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Typed mapping from artifact origin to discovery stage.
    Contribution: Lets the explorer replay graph growth using the framework's conceptual stages.
    """

    return ORIGIN_TO_STAGE.get(str(origin).strip(), "analysis")


def _stage_index_for_origin(origin: str) -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable ordering of artifact-origin stages.
    Contribution: Supports deterministic timeline construction and layout.
    """

    return STAGE_INDEX.get(_stage_key_for_origin(origin), 0)


def _family_for_type(node_type: str) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Typed abstraction over many fine-grained graph node kinds.
    Contribution: Gives the visualization a readable conceptual grammar instead of dozens of unrelated colors.
    """

    return TYPE_TO_FAMILY.get(str(node_type).strip() or "unknown", "concept")


def _role_for_type(node_type: str) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Fine-grained epistemic typing on top of the higher-level visual families.
    Contribution: Keeps the explorer readable as concepts, propositions, and proof objects while preserving a precise role label.
    """

    return TYPE_TO_ROLE.get(str(node_type).strip() or "unknown", "concept")


def _include_analysis_node(node_type: str) -> bool:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Filtering of low-level artifact internals before graph visualization.
    Contribution: Removes signature clutter so the graph foregrounds concepts, propositions, and proof objects.
    """

    return str(node_type).strip() in ANALYSIS_NODE_TYPES


def _include_coherence_node(node_type: str) -> bool:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Filtering of low-level artifact internals before graph visualization.
    Contribution: Keeps the coherence layer aligned with epistemic objects rather than implementation-only scaffolding.
    """

    return str(node_type).strip() in COHERENCE_NODE_TYPES


def _epistemic_relation(raw_relation: str, *, target_type: str = "") -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Translation from implementation-level relation labels to epistemic relations.
    Contribution: Makes the explorer edges speak in inferential terms rather than artifact plumbing.
    """

    relation = str(raw_relation).strip().lower() or "related"
    target = str(target_type).strip().lower()
    if relation == "uses":
        if target in {"problem", "complexity-class", "proof-regime", "model-signature"}:
            return "situates_in"
        if target in {"barrier", "barrier-signal"}:
            return "confronts"
        return "invokes"
    if relation == "asserts":
        return "articulates"
    if relation == "yields":
        return "supports"
    if relation == "requires":
        if target == "antecedent-signature":
            return "assumes"
        return "depends_on"
    if relation == "instantiates":
        return "realizes"
    if relation == "reduces_via":
        return "transports_via"
    if relation == "reexpresses":
        return "reframes"
    if relation == "reframes":
        return "reframes"
    if relation == "defines":
        return "defines"
    if relation == "supports":
        return "supports"
    if relation == "explains":
        return "explains"
    if relation == "attacks":
        return "challenges"
    if relation in {"blocks", "obstructs"}:
        return "obstructs"
    if relation == "hypothesis-source":
        return "motivates"
    if relation == "hypothesis-target":
        return "targets"
    if relation == "bridge-source":
        return "grounds"
    if relation == "bridge-target":
        return "targets"
    if relation == "conjectures":
        return "proposes"
    if relation == "conjecture-source":
        return "grounds"
    if relation == "conjecture-target":
        return "targets"
    if relation == "family-instantiates":
        return "instantiates"
    if relation == "anchors_on":
        return "anchors"
    if relation == "hardness-evidence":
        return "obstructs"
    if relation == "preserves":
        return "preserves"
    return relation


def _append_origin(record: dict[str, Any], origin: str) -> None:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Normalization of multi-source provenance into a compact node/edge form.
    Contribution: Preserves the fact that conceptual objects can be revisited by multiple stages.
    """

    origin_s = str(origin).strip() or "analysis"
    origins = record.setdefault("origins", [])
    if origin_s not in origins:
        origins.append(origin_s)
    stage_key = _stage_key_for_origin(origin_s)
    stage_index = _stage_index_for_origin(origin_s)
    current_stage_key = str(record.get("stage_key", "")).strip() or stage_key
    current_stage_index = int(record.get("stage_index", stage_index))
    if stage_index < current_stage_index:
        record["stage_key"] = stage_key
        record["stage_index"] = stage_index
    else:
        record.setdefault("stage_key", current_stage_key)
        record.setdefault("stage_index", current_stage_index)


def _ensure_node(
    node_id: str,
    nodes: dict[str, dict[str, Any]],
    *,
    node_type: str = "unknown",
    label: str | None = None,
    origin: str = "analysis",
    meta: dict[str, Any] | None = None,
    detail: dict[str, Any] | None = None,
) -> None:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Idempotent graph-node materialization utility.
    Contribution: Prevents duplicate or inconsistent node records when fusing multiple discovery artifacts.
    """

    node_key = str(node_id).strip()
    if not node_key:
        return
    if node_key not in nodes:
        stage_key = _stage_key_for_origin(origin)
        stage_index = _stage_index_for_origin(origin)
        nodes[node_key] = {
            "id": node_key,
            "label": (label.strip() if isinstance(label, str) else "") or node_key,
            "type": node_type or "unknown",
            "family": _family_for_type(node_type or "unknown"),
            "role": _role_for_type(node_type or "unknown"),
            "origin": str(origin).strip() or "analysis",
            "origins": [str(origin).strip() or "analysis"],
            "stage_key": stage_key,
            "stage_index": stage_index,
            "meta": meta or {},
            "detail": detail or {},
        }
        return
    node = nodes[node_key]
    if label and not str(node.get("label", "")).strip():
        node["label"] = label
    if node_type and str(node.get("type", "")).strip() in {"", "unknown"}:
        node["type"] = node_type
        node["family"] = _family_for_type(node_type)
        node["role"] = _role_for_type(node_type)
    _append_origin(node, origin)
    if isinstance(meta, dict) and meta:
        base = node.get("meta", {})
        if not isinstance(base, dict):
            base = {}
        base.update(meta)
        node["meta"] = base
    if isinstance(detail, dict) and detail:
        node["detail"] = _merge_detail_dict(node.get("detail", {}), detail)


def _add_edge(
    edges: list[dict[str, Any]],
    *,
    source: str,
    target: str,
    edge_type: str,
    origin: str,
    weight: float = 1.0,
    meta: dict[str, Any] | None = None,
) -> None:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Typed edge-construction helper.
    Contribution: Preserves relation typing and stage provenance in the discovery explorer.
    """

    src = str(source).strip()
    dst = str(target).strip()
    if not src or not dst:
        return
    stage_key = _stage_key_for_origin(origin)
    edges.append(
        {
            "id": f"{origin}:{edge_type}:{src}->{dst}:{len(edges)}",
            "source": src,
            "target": dst,
            "type": str(edge_type).strip() or "related",
            "origin": str(origin).strip() or "analysis",
            "origins": [str(origin).strip() or "analysis"],
            "stage_key": stage_key,
            "stage_index": _stage_index_for_origin(origin),
            "weight": float(weight),
            "meta": meta or {},
        }
    )


def _edge_sort_key(edge: dict[str, Any], nodes: dict[str, dict[str, Any]]) -> tuple[Any, ...]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Salience ordering over epistemic relations for visual pruning.
    Contribution: Prefers explanatory and bridge-bearing edges over background context when the graph is dense.
    """

    source = nodes.get(str(edge.get("source", "")).strip(), {})
    target = nodes.get(str(edge.get("target", "")).strip(), {})
    relation = str(edge.get("type", "related")).strip() or "related"
    weight = _safe_float(edge.get("weight"), 0.0)
    cross_family = int(
        str(source.get("family", "")).strip() != str(target.get("family", "")).strip()
    )
    return (
        EDGE_RELATION_PRIORITY.get(relation, 0),
        weight,
        cross_family,
        str(edge.get("target", "")).strip(),
        str(edge.get("id", "")).strip(),
    )


def _prune_edges(
    edges: list[dict[str, Any]],
    nodes: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Salience-preserving edge thinning for dense epistemic maps.
    Contribution: Keeps the explorer readable by capping low-signal contextual and obstruction edges per source.
    """

    prunable_origins = set(EDGE_SOURCE_TOTAL_LIMITS)
    kept_ids: set[str] = set()
    for origin in prunable_origins:
        source_groups: dict[str, list[dict[str, Any]]] = {}
        for edge in edges:
            if str(edge.get("origin", "")).strip() != origin:
                continue
            source = str(edge.get("source", "")).strip()
            if not source:
                continue
            source_groups.setdefault(source, []).append(edge)
        for source, source_edges in source_groups.items():
            relation_counts: Counter[str] = Counter()
            kept_for_source = 0
            total_limit = EDGE_SOURCE_TOTAL_LIMITS.get(origin, len(source_edges))
            for edge in sorted(source_edges, key=lambda row: _edge_sort_key(row, nodes), reverse=True):
                relation = str(edge.get("type", "related")).strip() or "related"
                relation_limit = EDGE_SOURCE_RELATION_LIMITS.get((origin, relation), total_limit)
                if kept_for_source >= total_limit or relation_counts[relation] >= relation_limit:
                    continue
                kept_ids.add(str(edge.get("id", "")).strip())
                kept_for_source += 1
                relation_counts[relation] += 1
            if not kept_for_source and source_edges:
                best_edge = max(source_edges, key=lambda row: _edge_sort_key(row, nodes))
                kept_ids.add(str(best_edge.get("id", "")).strip())
    return [
        edge
        for edge in edges
        if str(edge.get("origin", "")).strip() not in prunable_origins
        or str(edge.get("id", "")).strip() in kept_ids
    ]


def _conjecture_label(row: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Human-readable naming for abstraction conjecture nodes.
    Contribution: Keeps the conjecture layer legible in the explorer without losing traceability.
    """

    label = str(row.get("abstraction_label", "")).strip()
    if label:
        return label
    abstraction_type = str(row.get("abstraction_type", "")).strip()
    if abstraction_type:
        return abstraction_type
    return str(row.get("conjecture_id", "")).strip() or "abstraction conjecture"


def _timeline_metrics(reasoning_dynamics: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Extraction of stage-wise discovery metrics from the reasoning-dynamics artifact.
    Contribution: Aligns graph replay with the actual evolution of conceptual metrics over the run.
    """

    concept = (
        reasoning_dynamics.get("summary", {}).get("concept_evolution", {})
        if isinstance(reasoning_dynamics.get("summary"), dict)
        else {}
    )
    updates = concept.get("updates", []) if isinstance(concept.get("updates"), list) else []
    by_stage: dict[str, dict[str, Any]] = {}
    cumulative: dict[str, Any] = {}
    for spec in STAGE_SPECS:
        stage_updates = [
            row
            for row in updates
            if isinstance(row, dict)
            and ARTIFACT_KIND_TO_STAGE.get(str(row.get("artifact_kind", "")).strip()) == spec["key"]
        ]
        if stage_updates:
            latest = stage_updates[-1]
            metrics = latest.get("metrics", {}) if isinstance(latest.get("metrics"), dict) else {}
            cumulative.update(metrics)
            by_stage[spec["key"]] = {
                "timestamp": str(latest.get("timestamp", "")).strip(),
                "artifact_kind": str(latest.get("artifact_kind", "")).strip(),
                "metrics": dict(cumulative),
            }
        else:
            by_stage[spec["key"]] = {
                "timestamp": "",
                "artifact_kind": "",
                "metrics": dict(cumulative),
            }
    return by_stage


def _build_graph_data(
    analysis: dict[str, Any],
    phyp: dict[str, Any],
    coherence: dict[str, Any],
    bridges: dict[str, Any],
    conjectures: dict[str, Any],
    proof_sketches: dict[str, Any],
    hardness: dict[str, Any],
    expert_paper: dict[str, Any],
    reasoning_dynamics: dict[str, Any],
    statement_index: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Multi-artifact typed graph fusion for discovery-centric visualization.
    Contribution: Produces a single inspectable conceptual network linking landscape structure, hypotheses, bridge programs, conjectured abstractions, and hardness signals.
    """

    random.seed(13)
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []

    concept_graph = analysis.get("concept_graph", {}) if isinstance(analysis.get("concept_graph"), dict) else {}
    for row in concept_graph.get("nodes", []) if isinstance(concept_graph.get("nodes"), list) else []:
        if not isinstance(row, dict):
            continue
        node_id = str(row.get("id", "")).strip()
        node_type = str(row.get("type", "unknown")).strip() or "unknown"
        if not node_id:
            continue
        if not _include_analysis_node(node_type):
            continue
        _ensure_node(
            node_id,
            nodes,
            node_type=node_type,
            label=_node_label(row),
            origin="analysis",
            meta=row,
            detail=_generic_detail_from_meta(row),
        )
    for row in concept_graph.get("relations", []) if isinstance(concept_graph.get("relations"), list) else []:
        if not isinstance(row, dict):
            continue
        src = str(row.get("from", "")).strip()
        dst = str(row.get("to", "")).strip()
        if src not in nodes or dst not in nodes:
            continue
        rel = _epistemic_relation(
            str(row.get("relation", "related")).strip() or "related",
            target_type=str(nodes.get(dst, {}).get("type", "")).strip(),
        )
        _add_edge(
            edges,
            source=src,
            target=dst,
            edge_type=rel,
            origin="analysis",
            weight=float(row.get("weight", 1.0) or 1.0),
            meta=row,
        )

    for row in phyp.get("hypotheses", []) if isinstance(phyp.get("hypotheses"), list) else []:
        if not isinstance(row, dict):
            continue
        hypothesis_id = str(row.get("id", "")).strip()
        if not hypothesis_id:
            continue
        hnode = f"hypothesis:{hypothesis_id}"
        _ensure_node(
            hnode,
            nodes,
            node_type="hypothesis",
            label=str(row.get("title", "")).strip() or str(row.get("kind", "")).strip() or hypothesis_id,
            origin="phyp",
            meta=row,
            detail=_detail_payload(
                route_synopsis=_first_nonempty(
                    row.get("title", ""),
                    row.get("summary", ""),
                    row.get("claim", ""),
                    limit=320,
                ),
                bridge_definition=_first_nonempty(row.get("kind", ""), limit=180),
                assumptions=[row.get("support_statement_id", ""), row.get("target_statement_id", "")],
                obligations=[row.get("preserved_invariant", ""), row.get("status", "")],
            ),
        )
        support_id = str(row.get("support_statement_id", "")).strip()
        target_id = str(row.get("target_statement_id", "")).strip()
        if support_id:
            snode = support_id if support_id.startswith("statement:") else f"statement:{support_id}"
            _ensure_node(snode, nodes, node_type="statement", label=support_id, origin="phyp")
            _add_edge(
                edges,
                source=snode,
                target=hnode,
                edge_type=_epistemic_relation("hypothesis-source"),
                origin="phyp",
                weight=max(0.25, _safe_float(row.get("priority"), 0.0)),
                meta={"status": row.get("status", ""), "kind": row.get("kind", "")},
            )
        if target_id:
            tnode = target_id if target_id.startswith("statement:") else f"statement:{target_id}"
            _ensure_node(tnode, nodes, node_type="statement", label=target_id, origin="phyp")
            _add_edge(
                edges,
                source=hnode,
                target=tnode,
                edge_type=_epistemic_relation("hypothesis-target"),
                origin="phyp",
                weight=max(0.25, _safe_float(row.get("priority"), 0.0)),
                meta={"status": row.get("status", ""), "kind": row.get("kind", "")},
            )
        invariant = str(row.get("preserved_invariant", "")).strip()
        if invariant and invariant.lower() not in {"", "support interface", "support-to-target interface"}:
            inode = f"invariant:{invariant}"
            _ensure_node(
                inode,
                nodes,
                node_type="invariant",
                label=invariant,
                origin="phyp",
                meta={"source": hypothesis_id},
            )
            _add_edge(
                edges,
                source=hnode,
                target=inode,
                edge_type=_epistemic_relation("preserves"),
                origin="phyp",
                weight=0.66,
                meta={"hypothesis_id": hypothesis_id},
            )

    typed_coherence = (
        coherence.get("typed_coherence_graph", {})
        if isinstance(coherence.get("typed_coherence_graph"), dict)
        else {}
    )
    for row in typed_coherence.get("nodes", []) if isinstance(typed_coherence.get("nodes"), list) else []:
        if not isinstance(row, dict):
            continue
        node_id = str(row.get("id", "")).strip()
        node_type = str(row.get("type", "unknown")).strip() or "unknown"
        if not node_id:
            continue
        if not _include_coherence_node(node_type):
            continue
        _ensure_node(
            node_id,
            nodes,
            node_type=node_type,
            label=_node_label(row),
            origin="coherence",
            meta=row,
            detail=_generic_detail_from_meta(row),
        )
    for row in typed_coherence.get("edges", []) if isinstance(typed_coherence.get("edges"), list) else []:
        if not isinstance(row, dict):
            continue
        src = str(row.get("from", "")).strip()
        dst = str(row.get("to", "")).strip()
        if src not in nodes or dst not in nodes:
            continue
        rel = _epistemic_relation(
            str(row.get("relation", "related")).strip() or "related",
            target_type=str(nodes.get(dst, {}).get("type", "")).strip(),
        )
        _add_edge(
            edges,
            source=src,
            target=dst,
            edge_type=rel,
            origin="coherence",
            weight=float(row.get("weight", 1.0) or 1.0),
            meta=row,
        )

    for row in bridges.get("bridge_programs", []) if isinstance(bridges.get("bridge_programs"), list) else []:
        if not isinstance(row, dict):
            continue
        bridge_id = str(row.get("bridge_id", "")).strip()
        if not bridge_id:
            continue
        bridge_node = f"bridge:{bridge_id}"
        _ensure_node(
            bridge_node,
            nodes,
            node_type="bridge-program",
            label=str(row.get("bridge_type", "")).strip() or bridge_id,
            origin="bridge-plan",
            meta=row,
            detail=_detail_payload(
                route_synopsis=_first_nonempty(
                    (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("route_synopsis", ""),
                    limit=320,
                ),
                source_excerpt=_first_nonempty(
                    (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("source_theorem_excerpt", ""),
                    limit=300,
                ),
                target_excerpt=_first_nonempty(
                    (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("target_theorem_excerpt", ""),
                    limit=300,
                ),
                statement_delta=row.get("statement_delta", {}),
                carrier_kind=_first_nonempty(
                    (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("typed_object_expectation", ""),
                    limit=180,
                ),
                typing_status=_first_nonempty(
                    (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("typing_status", ""),
                    limit=60,
                ),
                bridge_definition=_first_nonempty(
                    (row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("bridge_question", ""),
                    limit=380,
                ),
                conditional_claim=_first_nonempty(
                    (row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("theorem_template", ""),
                    limit=340,
                ),
                assumptions=[
                    (row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("source_assumption", ""),
                    (row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("target_payoff", ""),
                    (row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("invariant_transport", ""),
                ],
                obligations=(row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("inspection_checklist", []),
                failure_diagnosis=_first_nonempty(
                    (row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("obstruction_pressure", ""),
                    limit=280,
                ),
            ),
        )
        src = str(row.get("from_id", "")).strip()
        dst = str(row.get("to_id", "")).strip()
        if src:
            src_node = src if src.startswith("statement:") else f"statement:{src}"
            _ensure_node(src_node, nodes, node_type="statement", label=src, origin="bridge-plan")
            _add_edge(
                edges,
                source=src_node,
                target=bridge_node,
                edge_type=_epistemic_relation("bridge-source"),
                origin="bridge-plan",
                weight=float(row.get("bridge_score", 1.0) or 1.0),
                meta={"bridge_type": row.get("bridge_type", "")},
            )
        if dst:
            dst_node = dst if dst.startswith("statement:") else f"statement:{dst}"
            _ensure_node(dst_node, nodes, node_type="statement", label=dst, origin="bridge-plan")
            _add_edge(
                edges,
                source=bridge_node,
                target=dst_node,
                edge_type=_epistemic_relation("bridge-target"),
                origin="bridge-plan",
                weight=float(row.get("bridge_score", 1.0) or 1.0),
                meta={"bridge_type": row.get("bridge_type", "")},
            )
        inferential_commitment = row.get("inferential_commitment", {})
        if not isinstance(inferential_commitment, dict):
            inferential_commitment = {}
        preserved_invariant = str(
            inferential_commitment.get("preserved_invariant", "") or row.get("preserved_invariant", "")
        ).strip()
        if preserved_invariant:
            invariant_node = f"invariant:{preserved_invariant}"
            _ensure_node(
                invariant_node,
                nodes,
                node_type="invariant",
                label=preserved_invariant,
                origin="bridge-plan",
                meta={"bridge_id": bridge_id},
            )
            _add_edge(
                edges,
                source=bridge_node,
                target=invariant_node,
                edge_type=_epistemic_relation("preserves"),
                origin="bridge-plan",
                weight=0.7,
                meta={"bridge_id": bridge_id},
            )

    for row in conjectures.get("abstraction_conjectures", []) if isinstance(conjectures.get("abstraction_conjectures"), list) else []:
        if not isinstance(row, dict):
            continue
        conjecture_id = str(row.get("conjecture_id", "")).strip()
        if not conjecture_id:
            continue
        cnode = f"conjecture:{conjecture_id}"
        _ensure_node(
            cnode,
            nodes,
            node_type="abstraction-conjecture",
            label=_conjecture_label(row),
            origin="conjecture",
            meta=row,
            detail=_detail_payload(
                route_synopsis=_first_nonempty(
                    (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("route_synopsis", ""),
                    ((row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("statement_delta", {}) if isinstance((row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("statement_delta", {}), dict) else {}).get("route_synopsis", ""),
                    limit=320,
                ),
                source_excerpt=_first_nonempty(
                    (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("source_theorem_excerpt", ""),
                    ((row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("statement_delta", {}) if isinstance((row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("statement_delta", {}), dict) else {}).get("source_theorem_excerpt", ""),
                    limit=300,
                ),
                target_excerpt=_first_nonempty(
                    (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("target_theorem_excerpt", ""),
                    ((row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("statement_delta", {}) if isinstance((row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("statement_delta", {}), dict) else {}).get("target_theorem_excerpt", ""),
                    limit=300,
                ),
                statement_delta=row.get("statement_delta", {})
                if isinstance(row.get("statement_delta"), dict)
                else (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("statement_delta", {}),
                carrier_kind=_first_nonempty(
                    row.get("carrier_kind", ""),
                    (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("carrier_kind", ""),
                    limit=180,
                ),
                typing_status=_first_nonempty(
                    row.get("typing_status", ""),
                    (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("typing_status", ""),
                    limit=60,
                ),
                bridge_definition=_first_nonempty(
                    (row.get("definitional_profile", {}) if isinstance(row.get("definitional_profile"), dict) else {}).get("bridging_concept_definition", ""),
                    (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("definition_template", ""),
                    limit=380,
                ),
                conditional_claim=_first_nonempty(
                    (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("conditional_claim", ""),
                    limit=340,
                ),
                assumptions=(row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("assumptions", []),
                obligations=(row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("proof_obligation_templates", []),
                proof_outline=(row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("inspection_focus", []),
                failure_diagnosis=_first_nonempty(
                    (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("obstruction_template", ""),
                    limit=280,
                ),
                counterfactual=_first_nonempty(
                    " / ".join(
                        part
                        for part in (
                            str(((row.get("counterfactual_probes", [])[0] if isinstance(row.get("counterfactual_probes"), list) and row.get("counterfactual_probes") else {}) if isinstance((row.get("counterfactual_probes", [])[0] if isinstance(row.get("counterfactual_probes"), list) and row.get("counterfactual_probes") else {}), dict) else {}).get("intervention", "")).strip(),
                            str(((row.get("counterfactual_probes", [])[0] if isinstance(row.get("counterfactual_probes"), list) and row.get("counterfactual_probes") else {}) if isinstance((row.get("counterfactual_probes", [])[0] if isinstance(row.get("counterfactual_probes"), list) and row.get("counterfactual_probes") else {}), dict) else {}).get("expected_bridge_effect", "")).strip(),
                        )
                        if part
                    ),
                    limit=280,
                ),
            ),
        )
        bridge_id = str(row.get("bridge_id", "")).strip()
        if bridge_id:
            bridge_node = f"bridge:{bridge_id}"
            _ensure_node(
                bridge_node,
                nodes,
                node_type="bridge-program",
                label=bridge_id,
                origin="conjecture",
            )
            _add_edge(
                edges,
                source=bridge_node,
                target=cnode,
                edge_type=_epistemic_relation("conjectures"),
                origin="conjecture",
                weight=max(0.25, _safe_float(row.get("priority"), 0.0)),
                meta={"abstraction_type": row.get("abstraction_type", "")},
            )
        for statement_key in ("from_id", "to_id"):
            statement_id = str(row.get(statement_key, "")).strip()
            if not statement_id:
                continue
            snode = statement_id if statement_id.startswith("statement:") else f"statement:{statement_id}"
            _ensure_node(snode, nodes, node_type="statement", label=statement_id, origin="conjecture")
            edge_type = "conjecture-source" if statement_key == "from_id" else "conjecture-target"
            if statement_key == "from_id":
                _add_edge(
                    edges,
                    source=snode,
                    target=cnode,
                    edge_type=_epistemic_relation(edge_type),
                    origin="conjecture",
                    weight=0.56,
                )
            else:
                _add_edge(
                    edges,
                    source=cnode,
                    target=snode,
                    edge_type=_epistemic_relation(edge_type),
                    origin="conjecture",
                    weight=0.56,
                )
        abstraction_type = str(row.get("abstraction_type", "")).strip()
        if abstraction_type:
            family_node = f"abstraction-family:{abstraction_type}"
            _ensure_node(
                family_node,
                nodes,
                node_type="abstraction-family",
                label=abstraction_type,
                origin="conjecture",
                meta={"role": "abstraction-family"},
            )
            _add_edge(
                edges,
                source=family_node,
                target=cnode,
                edge_type=_epistemic_relation("family-instantiates"),
                origin="conjecture",
                weight=0.72,
            )
        for concept in row.get("anchor_concepts", []) if isinstance(row.get("anchor_concepts"), list) else []:
            concept_text = _clean_anchor_label(concept)
            if not concept_text:
                continue
            anode = f"anchor:{concept_text}"
            _ensure_node(
                anode,
                nodes,
                node_type="anchor-concept",
                label=concept_text,
                origin="conjecture",
                meta={"role": "anchor-concept"},
            )
            _add_edge(
                edges,
                source=cnode,
                target=anode,
                edge_type=_epistemic_relation("anchors_on"),
                origin="conjecture",
                weight=0.64,
            )
        preserved_invariant = str(row.get("preserved_invariant", "")).strip()
        if preserved_invariant:
            invariant_node = f"invariant:{preserved_invariant}"
            _ensure_node(
                invariant_node,
                nodes,
                node_type="invariant",
                label=preserved_invariant,
                origin="conjecture",
                meta={"conjecture_id": conjecture_id},
            )
            _add_edge(
                edges,
                source=cnode,
                target=invariant_node,
                edge_type=_epistemic_relation("preserves"),
                origin="conjecture",
                weight=0.68,
                meta={"conjecture_id": conjecture_id},
            )

    for row in proof_sketches.get("proof_sketches", []) if isinstance(proof_sketches.get("proof_sketches"), list) else []:
        if not isinstance(row, dict):
            continue
        sketch_id = str(row.get("sketch_id", "")).strip()
        if not sketch_id:
            continue
        sketch_node = f"proof-sketch:{sketch_id}"
        _ensure_node(
            sketch_node,
            nodes,
            node_type="proof-sketch",
            label=str(row.get("title", "")).strip() or sketch_id,
            origin="proof-sketch",
            meta=row,
            detail=_detail_payload(
                route_synopsis=_first_nonempty(
                    (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("route_synopsis", ""),
                    ((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("statement_delta", {}) if isinstance((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("statement_delta", {}), dict) else {}).get("route_synopsis", ""),
                    limit=320,
                ),
                source_excerpt=_first_nonempty(
                    (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("source_theorem_excerpt", ""),
                    ((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("statement_delta", {}) if isinstance((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("statement_delta", {}), dict) else {}).get("source_theorem_excerpt", ""),
                    (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("source_theorem_excerpt", ""),
                    limit=300,
                ),
                target_excerpt=_first_nonempty(
                    (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("target_theorem_excerpt", ""),
                    ((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("statement_delta", {}) if isinstance((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("statement_delta", {}), dict) else {}).get("target_theorem_excerpt", ""),
                    (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("target_theorem_excerpt", ""),
                    limit=300,
                ),
                statement_delta=(row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("statement_delta", {})
                or (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}),
                carrier_kind=_first_nonempty(
                    row.get("carrier_kind", ""),
                    (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("carrier_kind", ""),
                    limit=180,
                ),
                typing_status=_first_nonempty(
                    row.get("typing_status", ""),
                    (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("typing_status", ""),
                    limit=60,
                ),
                bridge_definition=_first_nonempty(
                    (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("bridge_definition", ""),
                    limit=380,
                ),
                conditional_claim=_first_nonempty(
                    (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("proposition", ""),
                    limit=340,
                ),
                assumptions=(row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("assumptions", []),
                obligations=_extract_text_rows(row.get("proof_obligations", []), keys=("requirement", "claim_template"), limit=5, text_limit=220),
                lemmas=[
                    *_extract_text_rows(row.get("candidate_lemmas", []), keys=("statement",), limit=5, text_limit=220),
                    *(
                        (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("lemma_chain", [])
                        if isinstance((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("lemma_chain", []), list)
                        else []
                    ),
                ],
                proof_outline=[
                    *_extract_text_rows(row.get("proof_outline_steps", []), keys=("objective", "expected_output"), limit=4, text_limit=220),
                    *(
                        (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("inspection_points", [])
                        if isinstance((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("inspection_points", []), list)
                        else []
                    ),
                ],
                failure_diagnosis=_first_nonempty(
                    (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("failure_mode", ""),
                    *((row.get("abort_conditions", []) if isinstance(row.get("abort_conditions"), list) else [])[:1]),
                    limit=280,
                ),
                counterfactual=_first_nonempty(
                    " / ".join(
                        part
                        for part in (
                            str((row.get("counterfactual_test", {}) if isinstance(row.get("counterfactual_test"), dict) else {}).get("intervention", "")).strip(),
                            str((row.get("counterfactual_test", {}) if isinstance(row.get("counterfactual_test"), dict) else {}).get("expected_bridge_effect", "")).strip(),
                        )
                        if part
                    ),
                    limit=280,
                ),
            ),
        )
        bridge_id = str(row.get("bridge_id", "")).strip()
        if bridge_id:
            bridge_node = f"bridge:{bridge_id}"
            _ensure_node(bridge_node, nodes, node_type="bridge-program", label=bridge_id, origin="proof-sketch")
            _add_edge(
                edges,
                source=bridge_node,
                target=sketch_node,
                edge_type="instantiates",
                origin="proof-sketch",
                weight=max(0.35, _safe_float(row.get("sketch_score"), 0.0)),
                meta={"proof_strategy_family": row.get("proof_strategy_family", "")},
            )
        conjecture_id = str(row.get("conjecture_id", "")).strip()
        if conjecture_id:
            conjecture_node = f"conjecture:{conjecture_id}"
            _ensure_node(conjecture_node, nodes, node_type="abstraction-conjecture", label=conjecture_id, origin="proof-sketch")
            _add_edge(
                edges,
                source=conjecture_node,
                target=sketch_node,
                edge_type="grounds",
                origin="proof-sketch",
                weight=0.62,
            )
        source_statement_id = str(row.get("source_statement_id", "")).strip()
        if source_statement_id:
            source_node = source_statement_id if source_statement_id.startswith("statement:") else f"statement:{source_statement_id}"
            _ensure_node(source_node, nodes, node_type="statement", label=source_statement_id, origin="proof-sketch")
            _add_edge(
                edges,
                source=source_node,
                target=sketch_node,
                edge_type="grounds",
                origin="proof-sketch",
                weight=0.58,
            )
        target_statement_id = str(row.get("target_statement_id", "")).strip()
        if target_statement_id:
            target_node = target_statement_id if target_statement_id.startswith("statement:") else f"statement:{target_statement_id}"
            _ensure_node(target_node, nodes, node_type="statement", label=target_statement_id, origin="proof-sketch")
            _add_edge(
                edges,
                source=sketch_node,
                target=target_node,
                edge_type="targets",
                origin="proof-sketch",
                weight=0.58,
            )
        preserved_invariant = str(row.get("preserved_invariant", "")).strip()
        if preserved_invariant:
            invariant_node = f"invariant:{preserved_invariant}"
            _ensure_node(
                invariant_node,
                nodes,
                node_type="invariant",
                label=preserved_invariant,
                origin="proof-sketch",
                meta={"sketch_id": sketch_id},
            )
            _add_edge(
                edges,
                source=sketch_node,
                target=invariant_node,
                edge_type="preserves",
                origin="proof-sketch",
                weight=0.66,
                meta={"sketch_id": sketch_id},
            )

    expert_bridges = []
    if isinstance(expert_paper, dict):
        if isinstance(expert_paper.get("recommended_bridges"), list):
            expert_bridges = expert_paper.get("recommended_bridges", [])
        elif isinstance(expert_paper.get("bridge_portfolio"), list):
            expert_bridges = expert_paper.get("bridge_portfolio", [])
    for row in expert_bridges:
        if not isinstance(row, dict):
            continue
        bridge_id = str(row.get("bridge_id", "")).strip()
        if not bridge_id:
            continue
        bridge_node = f"bridge:{bridge_id}"
        _ensure_node(
            bridge_node,
            nodes,
            node_type="bridge-program",
            label=str(row.get("abstraction_label", "")).strip() or bridge_id,
            origin="proof-sketch",
            meta={"expert_paper": row},
            detail=_detail_payload(
                route_synopsis=_first_nonempty(row.get("route_synopsis", ""), limit=320),
                source_excerpt=_first_nonempty(row.get("source_excerpt", ""), limit=300),
                target_excerpt=_first_nonempty(row.get("target_excerpt", ""), limit=300),
                statement_delta=row.get("statement_delta", {}),
                carrier_kind=_first_nonempty(row.get("carrier_kind", ""), limit=180),
                typing_status=_first_nonempty(row.get("typing_status", ""), limit=60),
                bridge_definition=_first_nonempty(row.get("bridge_definition", ""), limit=380),
                conditional_claim=_first_nonempty(row.get("conditional_proposition", ""), limit=340),
                assumptions=row.get("mathematical_assumptions", []),
                obligations=row.get("proof_obligations", []),
                lemmas=row.get("candidate_lemmas", []),
                proof_outline=row.get("proof_outline", []) if isinstance(row.get("proof_outline"), list) else row.get("expert_actions", []),
                failure_diagnosis=_first_nonempty(row.get("failure_diagnosis", ""), limit=280),
                counterfactual=_first_nonempty(
                    row.get("negative_route", ""),
                    *((row.get("abort_conditions", []) if isinstance(row.get("abort_conditions"), list) else [])[:1]),
                    limit=280,
                ),
                expert_actions=row.get("expert_actions", []),
                evidence=[
                    _first_nonempty(row.get("missing_route_lemma", ""), limit=220),
                    *(
                        [
                            f"{_clean_display_text(link.get('hypothesis_id', ''), limit=120)} [{_clean_display_text(link.get('tier', ''), limit=80)}]"
                            for link in row.get("linked_hypothesis_rows", [])
                            if isinstance(link, dict)
                        ]
                        if isinstance(row.get("linked_hypothesis_rows"), list)
                        else []
                    ),
                ],
            ),
        )

    for row in hardness.get("essential_elements", []) if isinstance(hardness.get("essential_elements"), list) else []:
        if not isinstance(row, dict):
            continue
        name = str(row.get("name", "")).strip()
        if not name:
            continue
        hid = f"hardness:{name.lower().replace(' ', '-')}"
        _ensure_node(
            hid,
            nodes,
            node_type="hardness-element",
            label=name,
            origin="hardness",
            meta=row,
            detail=_detail_payload(
                route_synopsis=_first_nonempty(row.get("description", ""), row.get("name", ""), limit=320),
                obligations=row.get("minimal_conceptual_changes", []),
                failure_diagnosis=_first_nonempty(row.get("severity", ""), limit=120),
            ),
        )
        for sid in row.get("evidence_ids", []) if isinstance(row.get("evidence_ids"), list) else []:
            sid_s = str(sid).strip()
            if not sid_s:
                continue
            st_node = sid_s if sid_s.startswith("statement:") else f"statement:{sid_s}"
            _ensure_node(st_node, nodes, node_type="statement", label=sid_s, origin="hardness")
            _add_edge(
                edges,
                source=hid,
                target=st_node,
                edge_type=_epistemic_relation("hardness-evidence"),
                origin="hardness",
                weight=0.9,
                meta={"severity": row.get("severity", "")},
            )

    edges = _prune_edges(edges, nodes)
    _enrich_graph_details(
        nodes,
        edges,
        statement_index=statement_index or {},
        analysis=analysis,
        expert_paper=expert_paper,
    )

    degree: Counter[str] = Counter()
    relation_counts: Counter[str] = Counter()
    stage_counts: dict[str, dict[str, int]] = {
        spec["key"]: {"nodes": 0, "edges": 0}
        for spec in STAGE_SPECS
    }
    for edge in edges:
        degree[str(edge.get("source", "")).strip()] += 1
        degree[str(edge.get("target", "")).strip()] += 1
        relation_counts[str(edge.get("type", "related")).strip() or "related"] += 1
        stage_counts[str(edge.get("stage_key", "analysis"))]["edges"] += 1

    family_counts: Counter[str] = Counter()
    family_lane = {
        "concept": 0,
        "proposition": 1,
        "proof-object": 2,
    }
    bucket_members: dict[tuple[int, str], list[dict[str, Any]]] = {}
    for node in nodes.values():
        node["degree"] = int(degree.get(str(node.get("id", "")).strip(), 0))
        node["family"] = _family_for_type(str(node.get("type", "")).strip() or "unknown")
        node["role"] = _role_for_type(str(node.get("type", "")).strip() or "unknown")
        family_counts[node["family"]] += 1
        stage_counts[str(node.get("stage_key", "analysis"))]["nodes"] += 1
        bucket_key = (int(node.get("stage_index", 0)), str(node.get("family", "concept")))
        bucket_members.setdefault(bucket_key, []).append(node)

    golden_angle = math.pi * (3.0 - math.sqrt(5.0))
    for (stage_idx, family), members in sorted(bucket_members.items()):
        members.sort(key=lambda row: (-int(row.get("degree", 0)), str(row.get("label", "")).lower(), row["id"]))
        lane_idx = family_lane.get(family, 0)
        count = len(members)
        center_x = 165.0 + stage_idx * 335.0
        center_y = 150.0 + lane_idx * 270.0
        radius_x = min(126.0, 34.0 + math.sqrt(count) * 20.0)
        radius_y = min(104.0, 28.0 + math.sqrt(count) * 18.0)
        for index, node in enumerate(members):
            ring_scale = math.sqrt((index + 0.5) / max(1, count))
            angle = index * golden_angle
            jitter = (random.random() - 0.5) * 5.0
            node["anchor_x"] = center_x + math.cos(angle) * radius_x * ring_scale
            node["anchor_y"] = center_y + math.sin(angle) * radius_y * ring_scale
            node["x"] = node["anchor_x"] + jitter
            node["y"] = node["anchor_y"] + jitter
            node["vx"] = 0.0
            node["vy"] = 0.0

    stage_metric_map = _timeline_metrics(reasoning_dynamics)
    present_stage_keys = [
        spec["key"]
        for spec in STAGE_SPECS
        if stage_counts.get(spec["key"], {}).get("nodes", 0) > 0
        or stage_counts.get(spec["key"], {}).get("edges", 0) > 0
    ]
    states: list[dict[str, Any]] = []
    cumulative_stage_keys: list[str] = []
    seen_nodes: set[str] = set()
    seen_edges: set[str] = set()
    for index, stage_key in enumerate(present_stage_keys):
        spec = next(item for item in STAGE_SPECS if item["key"] == stage_key)
        cumulative_stage_keys.append(stage_key)
        node_ids = [
            node["id"]
            for node in sorted(nodes.values(), key=lambda row: row["id"])
            if str(node.get("stage_key", "analysis")) in cumulative_stage_keys
        ]
        edge_ids = [
            edge["id"]
            for edge in edges
            if str(edge.get("stage_key", "analysis")) in cumulative_stage_keys
        ]
        new_node_ids = [node_id for node_id in node_ids if node_id not in seen_nodes]
        new_edge_ids = [edge_id for edge_id in edge_ids if edge_id not in seen_edges]
        seen_nodes.update(new_node_ids)
        seen_edges.update(new_edge_ids)
        metric_bundle = stage_metric_map.get(stage_key, {})
        states.append(
            {
                "index": index,
                "stage_key": stage_key,
                "stage_label": spec["label"],
                "description": spec["description"],
                "timestamp": str(metric_bundle.get("timestamp", "")).strip(),
                "artifact_kind": str(metric_bundle.get("artifact_kind", "")).strip(),
                "node_ids": node_ids,
                "edge_ids": edge_ids,
                "new_node_ids": new_node_ids,
                "new_edge_ids": new_edge_ids,
                "metrics": metric_bundle.get("metrics", {}),
            }
        )

    return {
        "metadata": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "relation_counts": dict(sorted(relation_counts.items())),
            "family_counts": dict(sorted(family_counts.items())),
            "stage_counts": stage_counts,
            "timeline_state_count": len(states),
            "origins": sorted(
                {
                    origin
                    for node in nodes.values()
                    for origin in node.get("origins", [])
                    if str(origin).strip()
                }
            ),
        },
        "nodes": sorted(nodes.values(), key=lambda row: row["id"]),
        "edges": edges,
        "states": states,
        "stage_specs": list(STAGE_SPECS),
    }


def _render_html(title: str, graph: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Self-contained HTML/JavaScript rendering for interactive graph exploration.
    Contribution: Produces a portable, stage-aware discovery explorer without external dependencies.
    """

    payload = json.dumps(graph, ensure_ascii=False)
    title_safe = title.replace("<", "&lt;").replace(">", "&gt;")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title_safe}</title>
  <style>
    :root {{
      --bg: #f5efe3;
      --bg-deep: #efe6d3;
      --panel: rgba(255, 251, 244, 0.92);
      --panel-strong: rgba(255, 252, 247, 0.97);
      --ink: #1f2a22;
      --muted: #617063;
      --line: rgba(65, 85, 71, 0.16);
      --accent: #194c45;
      --accent-soft: #2f7b6d;
      --warm: #c45c37;
      --warm-soft: #efb286;
      --gold: #d0a447;
      --cream: #fff8ef;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Space Grotesk", "Aptos", "IBM Plex Sans", "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at 8% 10%, rgba(208, 164, 71, 0.18), transparent 28%),
        radial-gradient(circle at 84% 82%, rgba(47, 123, 109, 0.18), transparent 30%),
        linear-gradient(135deg, var(--bg) 0%, var(--bg-deep) 100%);
      overflow: hidden;
    }}
    .app {{
      display: grid;
      grid-template-columns: 360px 1fr 340px;
      height: 100vh;
      gap: 12px;
      padding: 12px;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 18px;
      box-shadow: 0 18px 40px rgba(33, 44, 37, 0.08);
      backdrop-filter: blur(14px);
      overflow: hidden;
    }}
    .sidebar {{
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      overflow: auto;
    }}
    .title {{
      margin: 0;
      font-size: 24px;
      line-height: 1.05;
      letter-spacing: -0.03em;
      color: var(--accent);
    }}
    .subtle {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
    }}
    .block {{
      border: 1px solid var(--line);
      border-radius: 16px;
      background: var(--panel-strong);
      padding: 12px;
    }}
    .block h2 {{
      margin: 0 0 8px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
    }}
    .search {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: #fffdfa;
      padding: 9px 11px;
      font-size: 13px;
      color: var(--ink);
    }}
    .row {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin: 6px 0;
      font-size: 12px;
    }}
    .legend-swatch {{
      width: 12px;
      height: 12px;
      border-radius: 999px;
      box-shadow: inset 0 0 0 1px rgba(255,255,255,0.65), 0 0 0 1px rgba(0,0,0,0.08);
      flex: 0 0 auto;
    }}
    .chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .chip {{
      padding: 6px 8px;
      border-radius: 999px;
      font-size: 11px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.74);
    }}
    .timeline-row {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      align-items: center;
      font-size: 12px;
      padding: 8px 10px;
      border-radius: 12px;
      cursor: pointer;
      border: 1px solid transparent;
    }}
    .timeline-row.active {{
      background: rgba(25, 76, 69, 0.11);
      border-color: rgba(25, 76, 69, 0.24);
    }}
    .timeline-row:hover {{
      background: rgba(196, 92, 55, 0.08);
    }}
    .timeline-row .stage-name {{
      font-weight: 600;
      color: var(--ink);
    }}
    .timeline-row .counts {{
      color: var(--muted);
      font-size: 11px;
    }}
    .canvas-panel {{
      position: relative;
      overflow: hidden;
      background:
        radial-gradient(circle at 20% 18%, rgba(47, 123, 109, 0.12), transparent 28%),
        radial-gradient(circle at 78% 82%, rgba(196, 92, 55, 0.11), transparent 30%),
        linear-gradient(160deg, rgba(255, 252, 247, 0.94) 0%, rgba(245, 239, 227, 0.85) 100%);
    }}
    canvas {{
      width: 100%;
      height: 100%;
      display: block;
      cursor: grab;
    }}
    .toolbar {{
      position: absolute;
      left: 14px;
      right: 14px;
      top: 14px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      background: rgba(255, 251, 244, 0.88);
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 10px 12px;
      backdrop-filter: blur(12px);
      z-index: 3;
    }}
    .toolbar button, .toolbar select {{
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 7px 10px;
      background: #fffdfa;
      color: var(--ink);
      font-size: 12px;
    }}
    .toolbar input[type="range"] {{
      width: 220px;
    }}
    .toolbar label {{
      font-size: 12px;
      color: var(--muted);
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .status-badge {{
      margin-left: auto;
      font-size: 12px;
      color: var(--muted);
      white-space: nowrap;
    }}
    .rightbar {{
      padding: 18px;
      overflow: auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .hero {{
      padding: 14px;
      border-radius: 16px;
      background:
        linear-gradient(145deg, rgba(25, 76, 69, 0.92) 0%, rgba(47, 123, 109, 0.9) 100%);
      color: #f6f1e8;
      box-shadow: inset 0 0 0 1px rgba(255,255,255,0.08);
    }}
    .hero .eyebrow {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      opacity: 0.82;
    }}
    .hero .stage {{
      margin-top: 6px;
      font-size: 24px;
      line-height: 1.05;
      letter-spacing: -0.03em;
    }}
    .hero .desc {{
      margin-top: 8px;
      font-size: 13px;
      line-height: 1.45;
      opacity: 0.92;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}
    .metric {{
      border: 1px solid var(--line);
      border-radius: 14px;
      background: rgba(255,255,255,0.82);
      padding: 10px;
    }}
    .metric .label {{
      font-size: 11px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .metric .value {{
      margin-top: 6px;
      font-size: 18px;
      font-weight: 700;
      letter-spacing: -0.03em;
      color: var(--ink);
    }}
    .mono {{
      font-family: ui-monospace, "Cascadia Code", "SFMono-Regular", Consolas, monospace;
      font-size: 11px;
      white-space: pre-wrap;
      line-height: 1.45;
      max-height: 320px;
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 10px;
      background: rgba(255,255,255,0.8);
    }}
    .selected-card {{
      display: grid;
      gap: 10px;
    }}
    .selected-title {{
      font-size: 15px;
      line-height: 1.3;
      font-weight: 700;
      color: var(--accent);
    }}
    .selected-meta {{
      color: var(--muted);
      font-size: 11px;
      line-height: 1.45;
    }}
    .selected-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .selected-tag {{
      padding: 4px 8px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.84);
      font-size: 11px;
      color: var(--ink);
    }}
    .selected-section {{
      display: grid;
      gap: 5px;
    }}
    .selected-section-title {{
      color: var(--muted);
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .selected-section-body {{
      font-size: 12px;
      line-height: 1.52;
      color: var(--ink);
    }}
    .selected-quote {{
      border-left: 3px solid rgba(25, 76, 69, 0.35);
      background: rgba(25, 76, 69, 0.06);
      border-radius: 0 12px 12px 0;
      padding: 8px 10px;
      font-size: 12px;
      line-height: 1.5;
    }}
    .selected-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
    }}
    .selected-cell {{
      border: 1px solid var(--line);
      border-radius: 12px;
      background: rgba(255,255,255,0.76);
      padding: 8px 9px;
      min-width: 0;
    }}
    .selected-cell .cell-key {{
      color: var(--muted);
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 4px;
    }}
    .selected-cell .cell-value {{
      font-size: 11px;
      line-height: 1.45;
      overflow-wrap: anywhere;
    }}
    .selected-list {{
      margin: 0;
      padding-left: 18px;
      font-size: 12px;
      line-height: 1.5;
    }}
    .selected-list li + li {{
      margin-top: 4px;
    }}
    .tooltip {{
      position: absolute;
      max-width: 380px;
      pointer-events: none;
      background: rgba(24, 33, 28, 0.95);
      color: #f5efe3;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 14px;
      padding: 10px 12px;
      font-size: 11px;
      line-height: 1.45;
      box-shadow: 0 16px 34px rgba(12, 18, 15, 0.28);
      z-index: 6;
    }}
    .tooltip.hidden {{
      display: none;
    }}
    .tooltip .label {{
      font-weight: 700;
      color: #fffaf2;
      margin-bottom: 4px;
    }}
    .tooltip .meta-row {{
      color: #d8e4dc;
      margin-top: 2px;
      overflow-wrap: anywhere;
    }}
    .tooltip .meta-key {{
      color: #9ed7c3;
    }}
    @media (max-width: 1400px) {{
      .app {{
        grid-template-columns: 320px 1fr;
      }}
      .right-shell {{
        display: none;
      }}
    }}
    @media (max-width: 980px) {{
      .app {{
        grid-template-columns: 1fr;
        height: auto;
        min-height: 100vh;
      }}
      .canvas-panel {{
        min-height: 72vh;
      }}
      .selected-grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <div class="app">
    <aside class="panel sidebar">
      <div>
        <div class="subtle">Discovery Explorer</div>
        <h1 class="title">{title_safe}</h1>
        <div class="subtle" id="graphMeta"></div>
      </div>

      <div class="block">
        <h2>Search</h2>
        <input id="search" class="search" placeholder="Filter nodes by label, id, role, or epistemic class..." />
        <div class="row"><label><input id="showLabels" type="checkbox" /> Show labels</label></div>
        <div class="row"><label><input id="showEdgeLabels" type="checkbox" /> Show edge labels</label></div>
        <div class="row"><label><input id="showContextEdges" type="checkbox" /> Show contextual edges</label></div>
      </div>

      <div class="block">
        <h2>Epistemic Classes</h2>
        <div id="familyFilters"></div>
      </div>

      <div class="block">
        <h2>Timeline</h2>
        <div id="timelineList"></div>
      </div>

      <div class="block">
        <h2>Selected Node</h2>
        <div id="selectedNode" class="subtle">Click a node to inspect its structured payload.</div>
      </div>
    </aside>

    <main class="panel canvas-panel" id="viewport">
      <div class="toolbar">
        <button id="prevBtn">Prev</button>
        <button id="playBtn">Play</button>
        <button id="nextBtn">Next</button>
        <label>Stage <input id="stageRange" type="range" min="0" max="0" value="0" /></label>
        <label>Layout
          <select id="layoutMode">
            <option value="discovery">Epistemic Map</option>
            <option value="free">Free Layout</option>
          </select>
        </label>
        <button id="fitBtn">Recenter</button>
        <div class="status-badge" id="statusBadge"></div>
      </div>
      <canvas id="graphCanvas"></canvas>
      <div class="tooltip hidden" id="tooltip"></div>
    </main>

    <aside class="panel right-shell rightbar">
      <div class="hero">
        <div class="eyebrow">Current Discovery Layer</div>
        <div class="stage" id="stageTitle">-</div>
        <div class="desc" id="stageDescription">-</div>
      </div>

      <div class="metrics" id="metricCards"></div>

      <div class="block">
        <h2>Visible Mix</h2>
        <div class="chips" id="visibleMix"></div>
      </div>

      <div class="block">
        <h2>Stage Metrics</h2>
        <div id="stageMetrics" class="mono">No metrics loaded.</div>
      </div>
    </aside>
  </div>

  <script>
    const DATA = {payload};
    const canvas = document.getElementById("graphCanvas");
    const ctx = canvas.getContext("2d");
    const viewport = document.getElementById("viewport");
    const tooltipEl = document.getElementById("tooltip");
    const graphMetaEl = document.getElementById("graphMeta");
    const selectedNodeEl = document.getElementById("selectedNode");
    const statusBadgeEl = document.getElementById("statusBadge");
    const metricCardsEl = document.getElementById("metricCards");
    const visibleMixEl = document.getElementById("visibleMix");
    const stageMetricsEl = document.getElementById("stageMetrics");
    const stageTitleEl = document.getElementById("stageTitle");
    const stageDescriptionEl = document.getElementById("stageDescription");
    const stageRange = document.getElementById("stageRange");
    const layoutModeEl = document.getElementById("layoutMode");
    const playBtn = document.getElementById("playBtn");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const fitBtn = document.getElementById("fitBtn");
    const searchEl = document.getElementById("search");
    const showLabelsEl = document.getElementById("showLabels");
    const showEdgeLabelsEl = document.getElementById("showEdgeLabels");
    const showContextEdgesEl = document.getElementById("showContextEdges");

    const nodes = (DATA.nodes || []).map((node) => ({{ ...node }}));
    const edges = (DATA.edges || []).map((edge) => ({{ ...edge }}));
    const states = Array.isArray(DATA.states) ? DATA.states : [];
    const stageSpecs = Array.isArray(DATA.stage_specs) ? DATA.stage_specs : [];
    const nodeById = new Map(nodes.map((node) => [node.id, node]));
    const edgeById = new Map(edges.map((edge) => [edge.id, edge]));
    const stageIndexByKey = new Map(stageSpecs.map((spec, index) => [spec.key, index]));

    const FAMILY_COLORS = {{
      concept: "#194c45",
      proposition: "#c45c37",
      "proof-object": "#d0a447",
    }};

    const EDGE_COLORS = {{
      articulates: "#2f7b6d",
      anchors: "#c98b3c",
      assumes: "#5f8d4e",
      challenges: "#9d4a40",
      confronts: "#8f3d32",
      defines: "#194c45",
      depends_on: "#5f8d4e",
      explains: "#24776a",
      grounds: "#b8892e",
      instantiates: "#d0a447",
      invokes: "#6f8d84",
      motivates: "#d87a54",
      obstructs: "#8f3d32",
      preserves: "#b26743",
      proposes: "#c45c37",
      realizes: "#cb8b39",
      reframes: "#c98b3c",
      situates_in: "#6f8d84",
      supports: "#3a8c6b",
      targets: "#c45c37",
      transports_via: "#7c8f44",
    }};

    const familyOrder = ["concept", "proposition", "proof-object"];
    const familyLabels = {{
      concept: "Concepts",
      proposition: "Propositions",
      "proof-object": "Proof Objects",
    }};
    const contextualEdgeTypes = new Set(["situates_in", "anchors"]);

    const familyEnabled = new Set(familyOrder);
    let searchTerm = "";
    let showLabels = false;
    let showEdgeLabels = false;
    let showContextEdges = false;
    let layoutMode = "discovery";
    let currentStateIndex = Math.max(0, states.length - 1);

    let dpr = Math.max(1, window.devicePixelRatio || 1);
    let width = 0;
    let height = 0;
    let scale = 1.0;
    let offsetX = 0;
    let offsetY = 0;
    let draggingNode = null;
    let draggingPan = false;
    let selectedNode = null;
    let hoveredNode = null;
    let hoveredEdge = null;
    let lastX = 0;
    let lastY = 0;
    let timer = null;

    function currentState() {{
      return states[Math.max(0, Math.min(currentStateIndex, states.length - 1))] || null;
    }}

    function revealedNodeIds() {{
      const state = currentState();
      return new Set(state && Array.isArray(state.node_ids) ? state.node_ids : []);
    }}

    function revealedEdgeIds() {{
      const state = currentState();
      return new Set(state && Array.isArray(state.edge_ids) ? state.edge_ids : []);
    }}

    function setCanvasSize() {{
      const rect = viewport.getBoundingClientRect();
      width = Math.max(1, rect.width);
      height = Math.max(1, rect.height);
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }}

    function escapeHtml(value) {{
      return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
    }}

    function previewValue(value) {{
      if (value === null || value === undefined) return "null";
      if (typeof value === "string") return value.length > 180 ? `${{value.slice(0, 177)}}...` : value;
      const text = JSON.stringify(value);
      return text && text.length > 180 ? `${{text.slice(0, 177)}}...` : (text || "");
    }}

    function cleanText(value) {{
      return String(value ?? "").trim();
    }}

    function firstNonEmpty(...values) {{
      for (const value of values) {{
        const text = cleanText(value);
        if (text) return text;
      }}
      return "";
    }}

    function detailSection(title, value) {{
      const text = cleanText(value);
      if (!text) return "";
      return `<div class="selected-section"><div class="selected-section-title">${{escapeHtml(title)}}</div><div class="selected-section-body">${{escapeHtml(text)}}</div></div>`;
    }}

    function detailQuote(title, value) {{
      const text = cleanText(value);
      if (!text) return "";
      return `<div class="selected-section"><div class="selected-section-title">${{escapeHtml(title)}}</div><div class="selected-quote">${{escapeHtml(text)}}</div></div>`;
    }}

    function detailList(title, values, limit = 5) {{
      const rows = (Array.isArray(values) ? values : []).map(cleanText).filter(Boolean).slice(0, limit);
      if (!rows.length) return "";
      return `<div class="selected-section"><div class="selected-section-title">${{escapeHtml(title)}}</div><ul class="selected-list">${{rows.map((row) => `<li>${{escapeHtml(row)}}</li>`).join("")}}</ul></div>`;
    }}

    function detailDelta(delta) {{
      const row = delta && typeof delta === "object" ? delta : {{}};
      const labels = [
        ["source_problem_family", "Source family"],
        ["target_problem_family", "Target family"],
        ["source_model", "Source model"],
        ["target_model", "Target model"],
        ["source_claim_focus", "Source focus"],
        ["target_claim_focus", "Target focus"],
        ["model_shift", "Model shift"],
        ["threshold_shift", "Threshold shift"],
        ["consequence_shift", "Consequence shift"],
        ["typed_object_expectation", "Expected object"],
        ["missing_witness_or_transport", "Missing lemma"],
      ];
      const cells = labels
        .map(([key, title]) => {{
          const text = cleanText(row[key]);
          return text
            ? `<div class="selected-cell"><div class="cell-key">${{escapeHtml(title)}}</div><div class="cell-value">${{escapeHtml(text)}}</div></div>`
            : "";
        }})
        .filter(Boolean);
      if (!cells.length) return "";
      return `<div class="selected-section"><div class="selected-section-title">Mathematical delta</div><div class="selected-grid">${{cells.join("")}}</div></div>`;
    }}

    function compactMetaRows(node) {{
      const rows = [
        `id: ${{cleanText(node.id)}}`,
        `class: ${{cleanText(node.family || "concept")}}`,
        `role: ${{cleanText(node.role || "concept")}}`,
        `type: ${{cleanText(node.type || "unknown")}}`,
        `stage: ${{cleanText(node.stage_key || "analysis")}}`,
      ].filter(Boolean);
      return rows.join(" | ");
    }}

    function tooltipRows(meta, maxItems = 6) {{
      if (!meta || typeof meta !== "object") return "";
      const entries = Object.entries(meta).filter(([key, value]) =>
        String(key || "").trim() && previewValue(value).trim()
      );
      const rows = entries.slice(0, maxItems).map(([key, value]) =>
        `<div class="meta-row"><span class="meta-key">${{escapeHtml(key)}}:</span> ${{escapeHtml(previewValue(value))}}</div>`
      );
      if (entries.length > maxItems) {{
        rows.push(`<div class="meta-row">... +${{entries.length - maxItems}} more fields</div>`);
      }}
      return rows.join("");
    }}

    function showTooltip(px, py, html) {{
      tooltipEl.innerHTML = html;
      tooltipEl.classList.remove("hidden");
      const rect = viewport.getBoundingClientRect();
      let left = px + 16;
      let top = py + 16;
      if (left > rect.width - 390) left = px - 360;
      if (top > rect.height - 210) top = py - 180;
      tooltipEl.style.left = `${{Math.max(8, left)}}px`;
      tooltipEl.style.top = `${{Math.max(8, top)}}px`;
    }}

    function hideTooltip() {{
      tooltipEl.classList.add("hidden");
      tooltipEl.innerHTML = "";
    }}

    function familyColor(family) {{
      return FAMILY_COLORS[family] || "#567164";
    }}

    function edgeColor(type, family) {{
      return EDGE_COLORS[type] || familyColor(family);
    }}

    function toWorld(px, py) {{
      return {{
        x: (px - offsetX) / scale,
        y: (py - offsetY) / scale,
      }};
    }}

    function toScreen(wx, wy) {{
      return {{
        x: wx * scale + offsetX,
        y: wy * scale + offsetY,
      }};
    }}

    function isNodeVisible(node) {{
      if (!revealedNodeIds().has(node.id)) return false;
      if (!familyEnabled.has(node.family || "concept")) return false;
      if (!searchTerm) return true;
      const blob = `${{node.id}} ${{node.label || ""}} ${{node.type || ""}} ${{node.role || ""}} ${{node.family || ""}}`.toLowerCase();
      return blob.includes(searchTerm);
    }}

    function visibleGraph() {{
      const nodeIds = revealedNodeIds();
      const edgeIds = revealedEdgeIds();
      const visibleNodes = nodes.filter((node) => nodeIds.has(node.id) && isNodeVisible(node));
      const visibleNodeSet = new Set(visibleNodes.map((node) => node.id));
      const visibleEdges = edges.filter((edge) =>
        edgeIds.has(edge.id) &&
        (showContextEdges || !contextualEdgeTypes.has(String(edge.type || ""))) &&
        visibleNodeSet.has(edge.source) &&
        visibleNodeSet.has(edge.target)
      );
      return {{ visibleNodes, visibleEdges, visibleNodeSet }};
    }}

    function drawNodeShape(node, point, radius, strokeOnly = false) {{
      const family = node.family || "concept";
      const role = node.role || "";
      ctx.beginPath();
      if (role.includes("barrier") || role.includes("obstruction")) {{
        ctx.moveTo(point.x, point.y - radius);
        ctx.lineTo(point.x + radius, point.y + radius);
        ctx.lineTo(point.x - radius, point.y + radius);
        ctx.closePath();
      }} else if (family === "proposition") {{
        ctx.moveTo(point.x, point.y - radius);
        ctx.lineTo(point.x + radius, point.y);
        ctx.lineTo(point.x, point.y + radius);
        ctx.lineTo(point.x - radius, point.y);
        ctx.closePath();
      }} else if (family === "proof-object" && (role === "bridge-object" || role === "object-family")) {{
        const sides = 6;
        for (let i = 0; i < sides; i++) {{
          const angle = -Math.PI / 2 + (Math.PI * 2 * i) / sides;
          const x = point.x + Math.cos(angle) * radius;
          const y = point.y + Math.sin(angle) * radius;
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }}
        ctx.closePath();
      }} else if (family === "proof-object") {{
        ctx.roundRect(point.x - radius, point.y - radius, radius * 2, radius * 2, 5);
      }} else {{
        ctx.arc(point.x, point.y, radius, 0, Math.PI * 2);
      }}
      if (!strokeOnly) ctx.fill();
      ctx.stroke();
    }}

    function stageAnchor(node) {{
      if (Number.isFinite(Number(node.anchor_x)) && Number.isFinite(Number(node.anchor_y))) {{
        return {{
          x: Number(node.anchor_x),
          y: Number(node.anchor_y),
        }};
      }}
      const stageIndex = Number(node.stage_index || 0);
      const familyIndex = Math.max(0, familyOrder.indexOf(node.family || "concept"));
      const bandWidth = Math.max(220, (width - 220) / Math.max(1, states.length || 1));
      const laneHeight = Math.max(140, (height - 240) / Math.max(1, familyOrder.length));
      return {{
        x: 170 + stageIndex * bandWidth,
        y: 145 + familyIndex * laneHeight,
      }};
    }}

    function simulate() {{
      const {{ visibleNodes, visibleEdges }} = visibleGraph();
      const repel = 9800;
      const springK = 0.018;
      const centerK = 0.0008;
      const damping = 0.78;

      for (let i = 0; i < visibleNodes.length; i++) {{
        const a = visibleNodes[i];
        for (let j = i + 1; j < visibleNodes.length; j++) {{
          const b = visibleNodes[j];
          let dx = a.x - b.x;
          let dy = a.y - b.y;
          let d2 = dx * dx + dy * dy;
          if (d2 < 0.01) {{
            dx = (Math.random() - 0.5) * 0.2;
            dy = (Math.random() - 0.5) * 0.2;
            d2 = dx * dx + dy * dy;
          }}
          const dist = Math.sqrt(d2) || 1;
          const minDist = 42 + Math.sqrt(Number(a.degree || 0) + Number(b.degree || 0)) * 5;
          if (dist < minDist) {{
            const push = (minDist - dist) * 0.3;
            const ux = dx / dist;
            const uy = dy / dist;
            a.vx += ux * push;
            a.vy += uy * push;
            b.vx -= ux * push;
            b.vy -= uy * push;
          }}
          const force = repel / d2;
          const fx = force * dx;
          const fy = force * dy;
          a.vx += fx;
          a.vy += fy;
          b.vx -= fx;
          b.vy -= fy;
        }}
      }}

      for (const edge of visibleEdges) {{
        const a = nodeById.get(edge.source);
        const b = nodeById.get(edge.target);
        if (!a || !b) continue;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const dist = Math.sqrt(dx * dx + dy * dy) || 1;
        const rest = 58 + (1 - Math.min(1, Number(edge.weight || 1))) * 34;
        const force = springK * (dist - rest);
        const fx = force * (dx / dist);
        const fy = force * (dy / dist);
        a.vx += fx;
        a.vy += fy;
        b.vx -= fx;
        b.vy -= fy;
      }}

      for (const node of visibleNodes) {{
        if (draggingNode && draggingNode.id === node.id) {{
          node.vx = 0;
          node.vy = 0;
          continue;
        }}
        if (layoutMode === "discovery") {{
          const anchor = stageAnchor(node);
          node.vx += (anchor.x - node.x) * 0.03;
          node.vy += (anchor.y - node.y) * 0.026;
        }} else {{
          node.vx += -node.x * centerK;
          node.vy += -node.y * centerK;
        }}
        node.vx *= damping;
        node.vy *= damping;
        node.x += node.vx * 0.06;
        node.y += node.vy * 0.06;
      }}
    }}

    function drawStageBands() {{
      if (layoutMode !== "discovery") return;
      const bandWidth = Math.max(220, (width - 220) / Math.max(1, states.length || 1));
      states.forEach((state, index) => {{
        const left = 90 + index * bandWidth;
        const active = index <= currentStateIndex;
        ctx.fillStyle = active
          ? "rgba(25, 76, 69, 0.06)"
          : "rgba(97, 112, 99, 0.03)";
        ctx.fillRect(left, 92, bandWidth - 24, height - 165);
        ctx.fillStyle = active ? "#194c45" : "#77857a";
        ctx.font = "600 12px Space Grotesk, Aptos, IBM Plex Sans, sans-serif";
        ctx.fillText(state.stage_label || state.stage_key || `stage ${{index + 1}}`, left + 10, 78);
      }});

      familyOrder.forEach((family) => {{
        const anchorY = stageAnchor({{ stage_index: 0, family }}).y;
        ctx.strokeStyle = "rgba(97, 112, 99, 0.08)";
        ctx.beginPath();
        ctx.moveTo(74, anchorY);
        ctx.lineTo(width - 46, anchorY);
        ctx.stroke();
        ctx.fillStyle = "#6a776c";
        ctx.font = "11px Space Grotesk, Aptos, IBM Plex Sans, sans-serif";
        ctx.fillText(familyLabels[family] || family, 16, anchorY + 4);
      }});
    }}

    function draw() {{
      ctx.clearRect(0, 0, width, height);
      drawStageBands();

      const state = currentState();
      const newNodeIds = new Set(state && Array.isArray(state.new_node_ids) ? state.new_node_ids : []);
      const newEdgeIds = new Set(state && Array.isArray(state.new_edge_ids) ? state.new_edge_ids : []);
      const {{ visibleNodes, visibleEdges }} = visibleGraph();

      for (const edge of visibleEdges) {{
        const source = nodeById.get(edge.source);
        const target = nodeById.get(edge.target);
        if (!source || !target) continue;
        const a = toScreen(source.x, source.y);
        const b = toScreen(target.x, target.y);
        const hovered = hoveredEdge && hoveredEdge.id === edge.id;
        const accent = newEdgeIds.has(edge.id);
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = edgeColor(edge.type, source.family);
        ctx.globalAlpha = accent ? 0.72 : (hovered ? 0.74 : 0.26);
        ctx.lineWidth = (hovered ? 2.4 : 1.1) + Math.min(2.5, Number(edge.weight || 1) * 1.2);
        ctx.stroke();
        ctx.globalAlpha = 1;
        if (showEdgeLabels) {{
          const mx = (a.x + b.x) / 2;
          const my = (a.y + b.y) / 2;
          ctx.fillStyle = "rgba(47, 56, 49, 0.74)";
          ctx.font = "10px Space Grotesk, Aptos, IBM Plex Sans, sans-serif";
          ctx.fillText(String(edge.type || "related"), mx + 4, my - 4);
        }}
      }}

      for (const node of visibleNodes) {{
        const point = toScreen(node.x, node.y);
        const hovered = hoveredNode && hoveredNode.id === node.id;
        const selected = selectedNode && selectedNode.id === node.id;
        const isNew = newNodeIds.has(node.id);
        const radius = 5.6 + Math.min(8.5, Math.sqrt(Number(node.degree || 0)));

        if (isNew) {{
          ctx.save();
          ctx.strokeStyle = "rgba(196, 92, 55, 0.20)";
          ctx.lineWidth = 10;
          drawNodeShape(node, point, radius + 5, true);
          ctx.restore();
        }}

        ctx.save();
        ctx.fillStyle = familyColor(node.family || "concept");
        ctx.strokeStyle = selected ? "#ffffff" : (hovered ? "#fff5e8" : "rgba(255,255,255,0.78)");
        ctx.lineWidth = selected ? 2.2 : 1.4;
        drawNodeShape(node, point, selected ? radius + 1.8 : radius, false);
        ctx.restore();

        if (showLabels && (selected || hovered || isNew || Number(node.degree || 0) >= 5)) {{
          ctx.fillStyle = "#263329";
          ctx.font = "11px Space Grotesk, Aptos, IBM Plex Sans, sans-serif";
          ctx.fillText(String(node.label || node.id), point.x + radius + 6, point.y - radius - 2);
        }}
      }}
    }}

    function pointSegmentDistance(px, py, x1, y1, x2, y2) {{
      const dx = x2 - x1;
      const dy = y2 - y1;
      if (dx === 0 && dy === 0) {{
        const ex = px - x1;
        const ey = py - y1;
        return Math.sqrt(ex * ex + ey * ey);
      }}
      const t = Math.max(0, Math.min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)));
      const projX = x1 + t * dx;
      const projY = y1 + t * dy;
      const ex = px - projX;
      const ey = py - projY;
      return Math.sqrt(ex * ex + ey * ey);
    }}

    function pickNode(px, py) {{
      const world = toWorld(px, py);
      let best = null;
      let bestDistance = Infinity;
      const {{ visibleNodes }} = visibleGraph();
      for (const node of visibleNodes) {{
        const dx = node.x - world.x;
        const dy = node.y - world.y;
        const distance = dx * dx + dy * dy;
        if (distance < bestDistance && distance < 18 * 18 / (scale * scale)) {{
          best = node;
          bestDistance = distance;
        }}
      }}
      return best;
    }}

    function pickEdge(px, py) {{
      const {{ visibleEdges }} = visibleGraph();
      let best = null;
      let bestDistance = Infinity;
      for (const edge of visibleEdges) {{
        const source = nodeById.get(edge.source);
        const target = nodeById.get(edge.target);
        if (!source || !target) continue;
        const a = toScreen(source.x, source.y);
        const b = toScreen(target.x, target.y);
        const distance = pointSegmentDistance(px, py, a.x, a.y, b.x, b.y);
        if (distance < bestDistance && distance <= 7.0) {{
          best = edge;
          bestDistance = distance;
        }}
      }}
      return best;
    }}

    function updateHover(px, py) {{
      if (draggingNode || draggingPan) {{
        hoveredNode = null;
        hoveredEdge = null;
        hideTooltip();
        return;
      }}
      const node = pickNode(px, py);
      if (node) {{
        hoveredNode = node;
        hoveredEdge = null;
        const detail = node.detail && typeof node.detail === "object" ? node.detail : {{}};
        showTooltip(px, py, [
          `<div class="label">${{escapeHtml(node.label || node.id)}}</div>`,
          `<div class="meta-row"><span class="meta-key">id:</span> ${{escapeHtml(node.id)}}</div>`,
          `<div class="meta-row"><span class="meta-key">class:</span> ${{escapeHtml(node.family || "concept")}}</div>`,
          `<div class="meta-row"><span class="meta-key">role:</span> ${{escapeHtml(node.role || "concept")}}</div>`,
          `<div class="meta-row"><span class="meta-key">type:</span> ${{escapeHtml(node.type || "unknown")}}</div>`,
          `<div class="meta-row"><span class="meta-key">stage:</span> ${{escapeHtml(node.stage_key || "analysis")}}</div>`,
          firstNonEmpty(detail.route_synopsis, detail.statement_excerpt, detail.conditional_claim)
            ? `<div class="meta-row"><span class="meta-key">content:</span> ${{escapeHtml(previewValue(firstNonEmpty(detail.route_synopsis, detail.statement_excerpt, detail.conditional_claim)))}}</div>`
            : "",
          tooltipRows(node.meta, 5),
        ].join(""));
        return;
      }}

      const edge = pickEdge(px, py);
      if (edge) {{
        hoveredEdge = edge;
        hoveredNode = null;
        showTooltip(px, py, [
          `<div class="label">${{escapeHtml(edge.type || "related")}}</div>`,
          `<div class="meta-row"><span class="meta-key">source:</span> ${{escapeHtml(edge.source)}}</div>`,
          `<div class="meta-row"><span class="meta-key">target:</span> ${{escapeHtml(edge.target)}}</div>`,
          `<div class="meta-row"><span class="meta-key">stage:</span> ${{escapeHtml(edge.stage_key || "analysis")}}</div>`,
          `<div class="meta-row"><span class="meta-key">weight:</span> ${{escapeHtml(Number(edge.weight || 0).toFixed(3))}}</div>`,
          tooltipRows(edge.meta, 4),
        ].join(""));
        return;
      }}

      hoveredNode = null;
      hoveredEdge = null;
      hideTooltip();
    }}

    function updateSelectedPanel(node) {{
      if (!node) {{
        selectedNodeEl.textContent = "Click a node to inspect its structured payload.";
        return;
      }}
      const detail = node.detail && typeof node.detail === "object" ? node.detail : {{}};
      const meta = node.meta && typeof node.meta === "object" ? node.meta : {{}};
      const tags = [
        cleanText(node.family || ""),
        cleanText(node.role || ""),
        cleanText(node.type || ""),
        cleanText(node.stage_key || ""),
      ].filter(Boolean);
      const fallbackSummary = firstNonEmpty(
        detail.route_synopsis,
        detail.statement_excerpt,
        meta.rationale,
        meta.description,
        meta.summary,
      );
      const hasStructuredContent =
        cleanText(detail.route_synopsis) ||
        cleanText(detail.statement_excerpt) ||
        cleanText(detail.source_excerpt) ||
        cleanText(detail.target_excerpt) ||
        cleanText(detail.bridge_definition) ||
        cleanText(detail.conditional_claim) ||
        cleanText(detail.failure_diagnosis) ||
        cleanText(detail.counterfactual) ||
        (Array.isArray(detail.context_points) && detail.context_points.length) ||
        (Array.isArray(detail.related_routes) && detail.related_routes.length) ||
        (Array.isArray(detail.linked_objects) && detail.linked_objects.length) ||
        (Array.isArray(detail.expert_actions) && detail.expert_actions.length) ||
        (Array.isArray(detail.evidence) && detail.evidence.length) ||
        (detail.statement_delta && Object.keys(detail.statement_delta).length) ||
        (Array.isArray(detail.assumptions) && detail.assumptions.length) ||
        (Array.isArray(detail.obligations) && detail.obligations.length) ||
        (Array.isArray(detail.lemmas) && detail.lemmas.length) ||
        (Array.isArray(detail.proof_outline) && detail.proof_outline.length);

      if (!hasStructuredContent) {{
        selectedNodeEl.innerHTML = `
          <div class="selected-card">
            <div class="selected-title">${{escapeHtml(node.label || node.id)}}</div>
            <div class="selected-meta">${{escapeHtml(compactMetaRows(node))}}</div>
            ${{tags.length ? `<div class="selected-tags">${{tags.map((tag) => `<span class="selected-tag">${{escapeHtml(tag)}}</span>`).join("")}}</div>` : ""}}
            ${{fallbackSummary ? detailSection("Summary", fallbackSummary) : ""}}
            <div class="mono">${{escapeHtml(JSON.stringify(meta, null, 2))}}</div>
          </div>
        `;
        return;
      }}

      selectedNodeEl.innerHTML = `
        <div class="selected-card">
          <div class="selected-title">${{escapeHtml(node.label || node.id)}}</div>
          <div class="selected-meta">${{escapeHtml(compactMetaRows(node))}}</div>
          ${{tags.length ? `<div class="selected-tags">${{tags.map((tag) => `<span class="selected-tag">${{escapeHtml(tag)}}</span>`).join("")}}</div>` : ""}}
          ${{detailSection("Route synopsis", detail.route_synopsis || fallbackSummary)}}
          ${{detailQuote("Statement", detail.statement_excerpt)}}
          ${{detailQuote("Source theorem", detail.source_excerpt)}}
          ${{detailQuote("Target theorem", detail.target_excerpt)}}
          ${{detailDelta(detail.statement_delta)}}
          ${{(cleanText(detail.carrier_kind) || cleanText(detail.typing_status))
            ? `<div class="selected-section"><div class="selected-section-title">Candidate object</div><div class="selected-grid">${{
                cleanText(detail.carrier_kind) ? `<div class="selected-cell"><div class="cell-key">Carrier</div><div class="cell-value">${{escapeHtml(detail.carrier_kind)}}</div></div>` : ""
              }}${{
                cleanText(detail.typing_status) ? `<div class="selected-cell"><div class="cell-key">Typing status</div><div class="cell-value">${{escapeHtml(detail.typing_status)}}</div></div>` : ""
              }}</div></div>`
            : ""}}
          ${{detailList("Context threads", detail.context_points, 6)}}
          ${{detailList("Related routes", detail.related_routes, 5)}}
          ${{detailList("Linked objects", detail.linked_objects, 8)}}
          ${{detailList("Evidence", detail.evidence, 5)}}
          ${{detailSection("Definition", detail.bridge_definition)}}
          ${{detailSection("Conditional claim", detail.conditional_claim)}}
          ${{detailList("Assumptions", detail.assumptions, 4)}}
          ${{detailList("Proof obligations", detail.obligations, 5)}}
          ${{detailList("Lemma chain", detail.lemmas, 5)}}
          ${{detailList("Proof outline", detail.proof_outline, 4)}}
          ${{detailList("Expert actions", detail.expert_actions, 5)}}
          ${{detailSection("Failure diagnosis", detail.failure_diagnosis)}}
          ${{detailSection("Counterfactual probe", detail.counterfactual)}}
        </div>
      `;
    }}

    function renderMetricCards() {{
      const state = currentState();
      const metrics = state && typeof state.metrics === "object" ? state.metrics : {{}};
      const {{ visibleNodes, visibleEdges }} = visibleGraph();
      const cards = [
        ["Visible nodes", visibleNodes.length],
        ["Visible edges", visibleEdges.length],
        ["Hypotheses", metrics.hypothesis_total ?? 0],
        ["Coherence", metrics.coherence_global != null ? Number(metrics.coherence_global).toFixed(3) : "n/a"],
        ["Bridge programs", metrics.bridge_program_count ?? 0],
        ["Hardness elements", metrics.hardness_elements ?? 0],
      ];
      metricCardsEl.innerHTML = cards.map(([label, value]) =>
        `<div class="metric"><div class="label">${{escapeHtml(label)}}</div><div class="value">${{escapeHtml(value)}}</div></div>`
      ).join("");
      stageMetricsEl.textContent = JSON.stringify(metrics, null, 2);
    }}

    function renderVisibleMix() {{
      const {{ visibleNodes }} = visibleGraph();
      const counts = new Map();
      visibleNodes.forEach((node) => {{
        const key = node.family || "concept";
        counts.set(key, (counts.get(key) || 0) + 1);
      }});
      visibleMixEl.innerHTML = [...counts.entries()].sort((a, b) => b[1] - a[1]).map(([family, count]) =>
        `<div class="chip" style="border-color:${{familyColor(family)}}33;background:${{familyColor(family)}}11;color:${{familyColor(family)}}">${{escapeHtml(familyLabels[family] || family)}}: ${{count}}</div>`
      ).join("") || `<div class="chip">No visible nodes</div>`;
    }}

    function renderTimelineList() {{
      const timelineList = document.getElementById("timelineList");
      timelineList.innerHTML = states.map((state, index) => {{
        const stageCounts = (DATA.metadata && DATA.metadata.stage_counts && DATA.metadata.stage_counts[state.stage_key]) || {{}};
        const activeClass = index === currentStateIndex ? "timeline-row active" : "timeline-row";
        return `
          <div class="${{activeClass}}" data-stage-index="${{index}}">
            <div>
              <div class="stage-name">${{escapeHtml(state.stage_label || state.stage_key || `stage ${{index + 1}}`)}}</div>
              <div class="counts">${{escapeHtml(state.timestamp || "no timestamp")}}</div>
            </div>
            <div class="counts">${{stageCounts.nodes || 0}}n / ${{stageCounts.edges || 0}}e</div>
          </div>
        `;
      }}).join("");
      timelineList.querySelectorAll("[data-stage-index]").forEach((row) => {{
        row.addEventListener("click", () => {{
          const idx = Number(row.getAttribute("data-stage-index") || "0");
          setStateIndex(idx);
        }});
      }});
    }}

    function renderStatus() {{
      const state = currentState();
      if (!state) {{
        statusBadgeEl.textContent = "No states available";
        return;
      }}
      statusBadgeEl.textContent = `${{state.index + 1}} / ${{states.length}} · ${{state.stage_label || state.stage_key}}`;
      stageTitleEl.textContent = state.stage_label || state.stage_key || "-";
      stageDescriptionEl.textContent = state.description || "-";
      graphMetaEl.textContent = `nodes ${{DATA.metadata.node_count || 0}} · edges ${{DATA.metadata.edge_count || 0}} · stages ${{states.length}}`;
    }}

    function fitView() {{
      const {{ visibleNodes }} = visibleGraph();
      if (!visibleNodes.length) return;
      const xs = visibleNodes.map((node) => node.x);
      const ys = visibleNodes.map((node) => node.y);
      const minX = Math.min(...xs);
      const maxX = Math.max(...xs);
      const minY = Math.min(...ys);
      const maxY = Math.max(...ys);
      const worldWidth = Math.max(200, maxX - minX + 180);
      const worldHeight = Math.max(180, maxY - minY + 180);
      scale = Math.max(0.25, Math.min(1.4, Math.min(width / worldWidth, height / worldHeight)));
      offsetX = width / 2 - ((minX + maxX) / 2) * scale;
      offsetY = height / 2 - ((minY + maxY) / 2) * scale;
    }}

    function setStateIndex(index) {{
      currentStateIndex = Math.max(0, Math.min(index, states.length - 1));
      stageRange.value = String(currentStateIndex);
      renderTimelineList();
      renderStatus();
      renderMetricCards();
      renderVisibleMix();
      fitView();
      updateHover(lastX, lastY);
    }}

    function stopPlayback() {{
      if (timer) {{
        clearInterval(timer);
        timer = null;
      }}
      playBtn.textContent = "Play";
    }}

    function startPlayback() {{
      if (timer) {{
        stopPlayback();
        return;
      }}
      playBtn.textContent = "Pause";
      timer = setInterval(() => {{
        if (currentStateIndex >= states.length - 1) {{
          stopPlayback();
          return;
        }}
        setStateIndex(currentStateIndex + 1);
      }}, 900);
    }}

    function buildFamilyFilters() {{
      const root = document.getElementById("familyFilters");
      root.innerHTML = familyOrder.map((family) => `
        <label class="row">
          <input type="checkbox" data-family="${{family}}" checked />
          <span class="legend-swatch" style="background:${{familyColor(family)}}"></span>
          <span>${{escapeHtml(familyLabels[family] || family)}}</span>
        </label>
      `).join("");
      root.querySelectorAll("[data-family]").forEach((checkbox) => {{
        checkbox.addEventListener("change", () => {{
          const family = String(checkbox.getAttribute("data-family") || "");
          if (checkbox.checked) familyEnabled.add(family);
          else familyEnabled.delete(family);
          renderMetricCards();
          renderVisibleMix();
          updateHover(lastX, lastY);
        }});
      }});
    }}

    function animationFrame() {{
      simulate();
      draw();
      requestAnimationFrame(animationFrame);
    }}

    canvas.addEventListener("mousedown", (event) => {{
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      lastX = x;
      lastY = y;
      const node = pickNode(x, y);
      if (node) {{
        draggingNode = node;
        selectedNode = node;
        updateSelectedPanel(node);
        canvas.style.cursor = "grabbing";
      }} else {{
        draggingPan = true;
        canvas.style.cursor = "grabbing";
      }}
      updateHover(x, y);
    }});

    window.addEventListener("mousemove", (event) => {{
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      const dx = x - lastX;
      const dy = y - lastY;
      lastX = x;
      lastY = y;
      if (draggingNode) {{
        const world = toWorld(x, y);
        draggingNode.x = world.x;
        draggingNode.y = world.y;
        draggingNode.vx = 0;
        draggingNode.vy = 0;
      }} else if (draggingPan) {{
        offsetX += dx;
        offsetY += dy;
      }}
      updateHover(x, y);
    }});

    window.addEventListener("mouseup", () => {{
      draggingNode = null;
      draggingPan = false;
      canvas.style.cursor = "grab";
      updateHover(lastX, lastY);
    }});

    canvas.addEventListener("mouseleave", () => {{
      hoveredNode = null;
      hoveredEdge = null;
      hideTooltip();
    }});

    canvas.addEventListener("wheel", (event) => {{
      event.preventDefault();
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      const before = toWorld(x, y);
      const factor = event.deltaY < 0 ? 1.10 : 0.91;
      scale = Math.max(0.15, Math.min(3.6, scale * factor));
      const after = toScreen(before.x, before.y);
      offsetX += x - after.x;
      offsetY += y - after.y;
      updateHover(x, y);
    }}, {{ passive: false }});

    prevBtn.addEventListener("click", () => setStateIndex(currentStateIndex - 1));
    nextBtn.addEventListener("click", () => setStateIndex(currentStateIndex + 1));
    playBtn.addEventListener("click", startPlayback);
    fitBtn.addEventListener("click", fitView);
    stageRange.addEventListener("input", () => setStateIndex(Number(stageRange.value || "0")));
    layoutModeEl.addEventListener("change", () => {{
      layoutMode = layoutModeEl.value || "discovery";
      fitView();
    }});
    searchEl.addEventListener("input", () => {{
      searchTerm = String(searchEl.value || "").trim().toLowerCase();
      renderMetricCards();
      renderVisibleMix();
      updateHover(lastX, lastY);
    }});
    showLabelsEl.addEventListener("change", () => {{
      showLabels = !!showLabelsEl.checked;
    }});
    showEdgeLabelsEl.addEventListener("change", () => {{
      showEdgeLabels = !!showEdgeLabelsEl.checked;
    }});
    showContextEdgesEl.addEventListener("change", () => {{
      showContextEdges = !!showContextEdgesEl.checked;
      renderMetricCards();
      renderVisibleMix();
      updateHover(lastX, lastY);
    }});

    setCanvasSize();
    window.addEventListener("resize", () => {{
      setCanvasSize();
      fitView();
    }});

    stageRange.max = String(Math.max(0, states.length - 1));
    stageRange.value = String(currentStateIndex);
    buildFamilyFilters();
    renderTimelineList();
    renderStatus();
    renderMetricCards();
    renderVisibleMix();
    fitView();
    animationFrame();
  </script>
</body>
</html>
"""


def main() -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds artifact loading, graph fusion, timeline synthesis, and HTML emission into a reproducible visualization stage.
    """

    logger = ReasoningLogger("kb-discovery-graph-explorer")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb", required=True, help="Path to KB markdown file.")
    ap.add_argument("--kb-ref", default="", help="Optional canonical KB reference.")
    ap.add_argument("--artifacts-dir", default="", help="Optional explicit artifacts directory.")
    ap.add_argument("--analysis", default="", help="Optional connection-analysis JSON path.")
    ap.add_argument("--phyp", default="", help="Optional proof-hypotheses YAML path.")
    ap.add_argument("--coherence", default="", help="Optional coherence-report JSON path.")
    ap.add_argument("--bridges", default="", help="Optional bridge-plan JSON path.")
    ap.add_argument("--conjectures", default="", help="Optional concept-gap-abstractions JSON path.")
    ap.add_argument("--proof-sketches", default="", help="Optional proof-sketches JSON path.")
    ap.add_argument("--hardness", default="", help="Optional epistemic-hardness JSON path.")
    ap.add_argument("--expert-paper", default="", help="Optional expert-hypothesis-paper JSON path.")
    ap.add_argument("--reasoning-dynamics", default="", help="Optional reasoning-dynamics JSON path.")
    ap.add_argument("--title", default="", help="Visualization title.")
    ap.add_argument("--output-html", default="", help="Output path for the generated explorer HTML.")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[4]
    kb = Path(args.kb)
    if not kb.exists():
        log_path = logger.finalize("error", summary=f"KB not found: {kb}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] KB not found: {kb}")

    try:
        kb_ctx = resolve_kb_reference(kb, explicit_kb_ref=args.kb_ref)
    except ValueError as exc:
        log_path = logger.finalize("error", summary=str(exc))
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] {exc}")
    kb_ref = str(kb_ctx.get("kb_ref", "")).strip()
    artifacts_dir = canonical_artifacts_dir(repo, kb_ref)
    if args.artifacts_dir:
        requested = Path(args.artifacts_dir)
        if not requested.is_absolute():
            requested = (repo / requested).resolve()
        if requested != artifacts_dir:
            log_path = logger.finalize(
                "error",
                summary=(
                    "Non-canonical artifacts directory rejected. "
                    f"expected={artifacts_dir} requested={requested}"
                ),
            )
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(
                "[ERROR] artifacts are associated with the reference KB name. "
                f"Use canonical path: {artifacts_dir}"
            )

    analysis_path = Path(args.analysis) if args.analysis else artifacts_dir / "connection-analysis.json"
    phyp_path = Path(args.phyp) if args.phyp else repo / "phyp" / f"{kb_ref}.proof-hypotheses.yaml"
    coherence_path = Path(args.coherence) if args.coherence else artifacts_dir / "coherence-report.json"
    bridge_path = Path(args.bridges) if args.bridges else artifacts_dir / "bridge-plan.json"
    conjecture_path = Path(args.conjectures) if args.conjectures else artifacts_dir / "concept-gap-abstractions.json"
    proof_sketch_path = Path(args.proof_sketches) if args.proof_sketches else artifacts_dir / "proof-sketches.json"
    hardness_path = Path(args.hardness) if args.hardness else artifacts_dir / "epistemic-hardness.json"
    expert_paper_path = Path(args.expert_paper) if args.expert_paper else artifacts_dir / "expert-hypothesis-paper.json"
    dynamics_path = Path(args.reasoning_dynamics) if args.reasoning_dynamics else artifacts_dir / "reasoning-dynamics.json"
    output_html = Path(args.output_html) if args.output_html else artifacts_dir / "discovery-graph-explorer.html"
    title = str(args.title).strip() or f"Discovery Graph Explorer: {kb_ref}"

    logger.step(
        "Parsed discovery-graph-explorer arguments",
        "\n".join(
            [
                f"kb={kb}",
                f"kb_ref={kb_ref}",
                f"artifacts_dir={artifacts_dir}",
                f"analysis={analysis_path}",
                f"phyp={phyp_path}",
                f"coherence={coherence_path}",
                f"bridges={bridge_path}",
                f"conjectures={conjecture_path}",
                f"proof_sketches={proof_sketch_path}",
                f"hardness={hardness_path}",
                f"expert_paper={expert_paper_path}",
                f"reasoning_dynamics={dynamics_path}",
                f"output_html={output_html}",
            ]
        ),
    )

    graph = _build_graph_data(
        analysis=_load_json(analysis_path),
        phyp=_load_yaml(phyp_path),
        coherence=_load_json(coherence_path),
        bridges=_load_json(bridge_path),
        conjectures=_load_json(conjecture_path),
        proof_sketches=_load_json(proof_sketch_path),
        hardness=_load_json(hardness_path),
        expert_paper=_load_json(expert_paper_path),
        reasoning_dynamics=_load_json(dynamics_path),
        statement_index=load_statement_index(kb),
    )

    html = _render_html(title=title, graph=graph)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(html, encoding="utf-8")

    logger.add_output("discovery_graph_explorer_html", output_html)
    logger.step(
        "Built discovery graph explorer",
        "\n".join(
            [
                f"nodes={graph.get('metadata', {}).get('node_count', 0)}",
                f"edges={graph.get('metadata', {}).get('edge_count', 0)}",
                f"timeline_states={graph.get('metadata', {}).get('timeline_state_count', 0)}",
            ]
        ),
    )
    log_path = logger.finalize("success", summary=f"Wrote discovery graph explorer to {output_html}.")
    print(f"[OK] Wrote discovery graph explorer: {output_html}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
