# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Build a typed coherence graph and score explanatory power/coherence deltas.

Conceptual objective:
- represent a KB + hypothesis set as a typed theory network,
- estimate global coherence of that network,
- estimate local explanatory benefit and global coherence impact for each hypothesis.

The script is intentionally deterministic and conservative: it does not try to
"prove" hypotheses, it estimates whether accepting a hypothesis would improve or
degrade the current theory web.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from contracts import validate_connection_analysis
from contracts import validate_phyp
from reasoning_log import ReasoningLogger


STATEMENT_BLOCK_PATTERN = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_]*")
ID_TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+")

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "if",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}

METHOD_TOKEN_MAP = {
    "derandomization": "derandomization",
    "pit": "derandomization",
    "pseudorandom": "derandomization",
    "communication": "communication",
    "lifting": "communication",
    "proof": "proof-complexity",
    "resolution": "proof-complexity",
    "frege": "proof-complexity",
    "algebraic": "algebraic",
    "polynomial": "algebraic",
    "circuit": "circuit-lower-bounds",
    "lower": "circuit-lower-bounds",
    "barrier": "barrier-analysis",
    "natural": "barrier-analysis",
    "relativ": "barrier-analysis",
    "algebr": "barrier-analysis",
    "magnification": "meta-complexity",
    "meta": "meta-complexity",
    "reduction": "reduction",
    "complete": "reduction",
}

POSITIVE_RELATIONS = {"supports", "explains", "reframes"}
NEGATIVE_RELATIONS = {"attacks", "blocks"}


def _clamp01(value: float) -> float:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return max(0.0, min(1.0, value))


def _safe_float(value: Any, default: float = 0.0) -> float:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_list(value: Any) -> list[Any]:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def _normalize_list(value: Any) -> list[str]:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Normalization of input structures into stable internal forms.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    if value is None:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    text = str(value).strip()
    if not text:
        return []
    if "," in text:
        return [chunk.strip() for chunk in text.split(",") if chunk.strip()]
    return [text]


def _tokenize(text: str) -> set[str]:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    out: set[str] = set()
    for token in TOKEN_PATTERN.findall(text.lower()):
        if len(token) <= 1 or token in STOPWORDS:
            continue
        out.add(token)
    return out


def _id_signature(statement_id: str) -> set[str]:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    out: set[str] = set()
    for token in ID_TOKEN_PATTERN.findall(statement_id.lower().replace("st.", "").replace("sym.", "")):
        if len(token) <= 2 or token in {"def", "thm", "lem", "obs", "item"}:
            continue
        out.add(token)
    return out


def _jaccard(a: set[str], b: set[str]) -> float:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if not a or not b:
        return 0.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def _is_barrier(payload: dict[str, Any], method_tags: set[str]) -> bool:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if bool(payload.get("is_barrier")):
        return True
    if str(payload.get("barrier_family", "")).strip():
        return True
    if "barrier-analysis" in method_tags:
        return True
    concept_roles = _normalize_list(payload.get("concept_roles"))
    return any("barrier" in role.lower() for role in concept_roles)


def _extract_method_tags(tokens: set[str], id_tokens: set[str]) -> set[str]:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    tags: set[str] = set()
    for token in tokens | id_tokens:
        for stem, tag in METHOD_TOKEN_MAP.items():
            if stem in token:
                tags.add(tag)
    return tags


def _extract_statements(kb_path: Path) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    content = kb_path.read_text(encoding="utf-8")
    out: dict[str, dict[str, Any]] = {}
    for match in STATEMENT_BLOCK_PATTERN.finditer(content):
        try:
            payload = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(payload, dict):
            continue
        sid = str(payload.get("id", "")).strip()
        kind = str(payload.get("kind", "")).strip().lower()
        if not sid or not kind:
            continue
        text = "\n".join(
            [
                str(payload.get("latex", "")),
                str(payload.get("informal", "")),
                str(payload.get("proof_sketch", "")),
                str(payload.get("notes", "")),
            ]
        )
        tokens = _tokenize(text)
        id_tokens = _id_signature(sid)
        method_tags = _extract_method_tags(tokens, id_tokens)
        out[sid] = {
            "id": sid,
            "kind": kind,
            "status": str(payload.get("status", "tentative")).strip().lower(),
            "depends_on": _normalize_list(payload.get("depends_on")),
            "used_symbols": _normalize_list(payload.get("used_symbols")),
            "text": text,
            "tokens": tokens,
            "id_tokens": id_tokens,
            "method_tags": method_tags,
            "barrier_family": str(payload.get("barrier_family", "")).strip().lower(),
            "is_barrier": _is_barrier(payload, method_tags),
        }
    return out


def _descendant_counts(nodes: list[str], adjacency: dict[str, set[str]]) -> dict[str, int]:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    counts: dict[str, int] = {}
    for node in nodes:
        visited = {node}
        queue = deque([node])
        while queue:
            cur = queue.popleft()
            for nxt in adjacency.get(cur, set()):
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        counts[node] = max(0, len(visited) - 1)
    return counts


def _analysis_score_map(analysis: dict[str, Any]) -> dict[tuple[str, str], float]:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    out: dict[tuple[str, str], float] = {}
    for item in analysis.get("connection_candidates", []):
        if not isinstance(item, dict):
            continue
        src = str(item.get("from_id", "")).strip()
        dst = str(item.get("to_id", "")).strip()
        if not src or not dst:
            continue
        out[(src, dst)] = _clamp01(_safe_float(item.get("score"), 0.0))
    return out


def _coherence_profile(nodes: dict[str, dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute global coherence profile from typed edges.

    Positive relations (`supports`, `explains`, `reframes`) increase integration.
    Negative relations (`attacks`, `blocks`) increase tension.
    """
    support_weight = 0.0
    conflict_weight = 0.0
    incoming_positive: dict[str, int] = defaultdict(int)
    positive_adj: dict[str, set[str]] = defaultdict(set)

    for edge in edges:
        rel = str(edge.get("relation", "")).strip().lower()
        w = _clamp01(_safe_float(edge.get("weight"), 0.0))
        src = str(edge.get("from", "")).strip()
        dst = str(edge.get("to", "")).strip()
        if not src or not dst:
            continue
        if rel in POSITIVE_RELATIONS:
            support_weight += w
            incoming_positive[dst] += 1
            positive_adj[src].add(dst)
            positive_adj[dst].add(src)
        elif rel in NEGATIVE_RELATIONS:
            conflict_weight += w

    node_ids = list(nodes.keys())
    node_count = max(1, len(node_ids))
    visited: set[str] = set()
    largest_component = 0
    for nid in node_ids:
        if nid in visited:
            continue
        queue = deque([nid])
        visited.add(nid)
        size = 0
        while queue:
            cur = queue.popleft()
            size += 1
            for nxt in positive_adj.get(cur, set()):
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        largest_component = max(largest_component, size)

    consistency = support_weight / (support_weight + conflict_weight + 1e-9)
    integration = largest_component / node_count
    incoming_targets = [nid for nid in node_ids if incoming_positive.get(nid, 0) > 0]
    if incoming_targets:
        explanatory_unification = sum(1 for nid in incoming_targets if incoming_positive.get(nid, 0) >= 2) / len(incoming_targets)
    else:
        explanatory_unification = 0.0
    tension = conflict_weight / (support_weight + conflict_weight + 1e-9)
    global_coherence = _clamp01(0.45 * consistency + 0.35 * integration + 0.20 * explanatory_unification)

    return {
        "global_coherence": round(global_coherence, 6),
        "consistency": round(consistency, 6),
        "integration": round(integration, 6),
        "explanatory_unification": round(explanatory_unification, 6),
        "tension": round(tension, 6),
        "support_weight": round(support_weight, 6),
        "conflict_weight": round(conflict_weight, 6),
    }


def _hypothesis_relation(kind: str) -> str:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    k = kind.strip().lower()
    if k in {"representation-shift", "normal-form-reduction"}:
        return "reframes"
    if k in {"barrier-escape-principle"}:
        return "attacks"
    if k in {"intervention-focus", "analogy-transfer"}:
        return "explains"
    return "supports"


def _hypothesis_edges(hypothesis: dict[str, Any], statements: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    hid = str(hypothesis.get("id", "")).strip()
    kind = str(hypothesis.get("kind", "bridge-link")).strip().lower()
    src = str(hypothesis.get("support_statement_id", "")).strip()
    dst = str(hypothesis.get("target_statement_id", "")).strip()
    priority = _clamp01(_safe_float(hypothesis.get("priority"), 0.0))
    rel = _hypothesis_relation(kind)
    edges: list[dict[str, Any]] = []

    if dst:
        edges.append(
            {
                "from": f"hypothesis:{hid}",
                "to": f"statement:{dst}",
                "relation": rel if kind != "barrier-escape-principle" else "explains",
                "weight": round(0.35 + 0.55 * priority, 4),
                "source": "hypothesis",
                "hypothesis_id": hid,
            }
        )

    if src and dst:
        relation = "supports"
        if kind in {"representation-shift", "normal-form-reduction"}:
            relation = "reframes"
        elif kind == "analogy-transfer":
            relation = "explains"
        edges.append(
            {
                "from": f"statement:{src}",
                "to": f"statement:{dst}",
                "relation": relation,
                "weight": round(0.30 + 0.60 * priority, 4),
                "source": "hypothesis",
                "hypothesis_id": hid,
            }
        )

    if kind == "barrier-escape-principle" and src and src in statements and statements[src].get("is_barrier"):
        edges.append(
            {
                "from": f"hypothesis:{hid}",
                "to": f"statement:{src}",
                "relation": "attacks",
                "weight": round(0.35 + 0.55 * priority, 4),
                "source": "hypothesis",
                "hypothesis_id": hid,
            }
        )
    return edges


def _build_graph(
    statements: dict[str, dict[str, Any]],
    analysis: dict[str, Any],
    phyp: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    """Construct typed coherence graph components.

    Returns:
    - nodes: statement/concept/method/barrier/hypothesis nodes
    - base_edges: KB + connector structure independent of hypothesis acceptance
    - hypothesis_edges: edges explicitly induced by hypotheses
    - relation counter: coarse relation inventory for diagnostics
    """
    nodes: dict[str, dict[str, Any]] = {}
    base_edges: list[dict[str, Any]] = []
    hypothesis_edges: list[dict[str, Any]] = []

    # Statement, concept, method, barrier, and hypothesis nodes.
    for sid, stmt in statements.items():
        snode = f"statement:{sid}"
        nodes[snode] = {
            "id": snode,
            "type": "statement",
            "statement_id": sid,
            "kind": stmt.get("kind", ""),
        }
        for sym in stmt.get("used_symbols", []):
            cnode = f"concept:{sym}"
            if cnode not in nodes:
                nodes[cnode] = {"id": cnode, "type": "concept", "label": sym}
            base_edges.append(
                {
                    "from": snode,
                    "to": cnode,
                    "relation": "uses",
                    "weight": 0.6,
                    "source": "kb",
                }
            )
            if str(stmt.get("kind", "")).lower() == "definition":
                base_edges.append(
                    {
                        "from": snode,
                        "to": cnode,
                        "relation": "defines",
                        "weight": 0.8,
                        "source": "kb",
                    }
                )
        for tag in stmt.get("method_tags", []):
            mnode = f"method:{tag}"
            if mnode not in nodes:
                nodes[mnode] = {"id": mnode, "type": "method", "label": tag}
            base_edges.append(
                {
                    "from": snode,
                    "to": mnode,
                    "relation": "uses",
                    "weight": 0.55,
                    "source": "kb",
                }
            )
        if bool(stmt.get("is_barrier")):
            bnode = f"barrier:{sid}"
            nodes[bnode] = {"id": bnode, "type": "barrier", "statement_id": sid}
            base_edges.append(
                {
                    "from": snode,
                    "to": bnode,
                    "relation": "defines",
                    "weight": 0.75,
                    "source": "kb",
                }
            )

    # Dependency and generalization structure.
    for sid, stmt in statements.items():
        dst = f"statement:{sid}"
        for dep in stmt.get("depends_on", []):
            if dep not in statements:
                continue
            src = f"statement:{dep}"
            base_edges.append(
                {
                    "from": src,
                    "to": dst,
                    "relation": "supports",
                    "weight": 0.72,
                    "source": "kb",
                }
            )
            base_edges.append(
                {
                    "from": src,
                    "to": dst,
                    "relation": "generalizes",
                    "weight": 0.55,
                    "source": "kb",
                }
            )

    # Barrier obstruction edges.
    theorem_nodes = [f"statement:{sid}" for sid, stmt in statements.items() if str(stmt.get("kind", "")).lower() == "theorem"]
    barrier_ids = [sid for sid, stmt in statements.items() if bool(stmt.get("is_barrier"))]
    for bid in barrier_ids:
        bnode = f"statement:{bid}"
        barrier_stmt = statements[bid]
        barrier_symbols = set(barrier_stmt.get("used_symbols", []))
        barrier_methods = set(barrier_stmt.get("method_tags", []))
        barrier_family = set(barrier_stmt.get("id_tokens", set()))
        for tnode in theorem_nodes:
            tid = tnode.split("statement:", 1)[1]
            if tid == bid:
                continue
            theorem_stmt = statements[tid]
            theorem_symbols = set(theorem_stmt.get("used_symbols", []))
            theorem_methods = set(theorem_stmt.get("method_tags", []))
            theorem_family = set(theorem_stmt.get("id_tokens", set()))
            symbol_overlap = _jaccard(barrier_symbols, theorem_symbols)
            method_overlap = _jaccard(barrier_methods, theorem_methods)
            family_overlap = _jaccard(barrier_family, theorem_family)
            structural_overlap = _clamp01(0.45 * symbol_overlap + 0.35 * method_overlap + 0.20 * family_overlap)
            if structural_overlap < 0.08:
                continue
            base_edges.append(
                {
                    "from": bnode,
                    "to": tnode,
                    "relation": "blocks",
                    "weight": round(0.30 + 0.50 * structural_overlap, 4),
                    "source": "kb",
                }
            )
            barrier_node = f"barrier:{bid}"
            if barrier_node in nodes:
                base_edges.append(
                    {
                        "from": barrier_node,
                        "to": tnode,
                        "relation": "obstructs",
                        "weight": round(0.30 + 0.50 * structural_overlap, 4),
                        "source": "kb",
                    }
                )

    # Connector-derived explanatory edges.
    for cand in analysis.get("connection_candidates", []):
        if not isinstance(cand, dict):
            continue
        src = str(cand.get("from_id", "")).strip()
        dst = str(cand.get("to_id", "")).strip()
        if src not in statements or dst not in statements:
            continue
        rel = str(cand.get("relation", "potential-support")).strip().lower()
        if rel in {"potential-equivalence", "definitional-expansion"}:
            edge_rel = "reframes"
        elif rel in {"method-transfer", "analogy-transfer"}:
            edge_rel = "explains"
        else:
            edge_rel = "supports"
        base_edges.append(
            {
                "from": f"statement:{src}",
                "to": f"statement:{dst}",
                "relation": edge_rel,
                "weight": round(0.25 + 0.65 * _clamp01(_safe_float(cand.get("score"), 0.0)), 4),
                "source": "analysis",
            }
        )

    # Hypothesis nodes and edges.
    for hyp in phyp.get("hypotheses", []):
        if not isinstance(hyp, dict):
            continue
        hid = str(hyp.get("id", "")).strip()
        if not hid:
            continue
        hnode = f"hypothesis:{hid}"
        nodes[hnode] = {
            "id": hnode,
            "type": "hypothesis",
            "hypothesis_id": hid,
            "kind": str(hyp.get("kind", "")).strip().lower(),
            "status": str(hyp.get("status", "tentative")).strip().lower(),
        }
        hypothesis_edges.extend(_hypothesis_edges(hyp, statements))

    relation_counter = Counter()
    for edge in base_edges + hypothesis_edges:
        relation_counter[str(edge.get("relation", "")).strip().lower()] += 1

    return nodes, base_edges, hypothesis_edges, dict(relation_counter)


def _hypothesis_signal_rows(
    statements: dict[str, dict[str, Any]],
    analysis: dict[str, Any],
    phyp: dict[str, Any],
    nodes: dict[str, dict[str, Any]],
    base_edges: list[dict[str, Any]],
    hypothesis_edges: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    """Score each hypothesis by local explanatory power and global coherence delta.

    The comparison baseline is the base graph without hypothesis edges. For each
    hypothesis we add only that hypothesis' induced edges to isolate its effect.
    """
    pair_scores = _analysis_score_map(analysis)
    hypothesis_lookup = {
        str(h.get("id", "")).strip(): h
        for h in phyp.get("hypotheses", [])
        if isinstance(h, dict) and str(h.get("id", "")).strip()
    }
    hyp_edges_by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in hypothesis_edges:
        hid = str(edge.get("hypothesis_id", "")).strip()
        if hid:
            hyp_edges_by_id[hid].append(edge)

    # Build statement dependency reachability for explanatory-power proxy.
    adjacency: dict[str, set[str]] = {sid: set() for sid in statements}
    for sid, stmt in statements.items():
        for dep in stmt.get("depends_on", []):
            if dep in adjacency:
                adjacency[dep].add(sid)
    downstream = _descendant_counts(sorted(statements.keys()), adjacency)
    max_downstream = max([1] + list(downstream.values()))

    base_profile = _coherence_profile(nodes, base_edges)
    rows: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}

    for hid, hyp in hypothesis_lookup.items():
        kind = str(hyp.get("kind", "")).strip().lower()
        target = str(hyp.get("target_statement_id", "")).strip()
        support = str(hyp.get("support_statement_id", "")).strip()
        priority = _clamp01(_safe_float(hyp.get("priority"), 0.0))
        analysis_score = _clamp01(pair_scores.get((support, target), 0.0))

        target_stmt = statements.get(target, {})
        support_stmt = statements.get(support, {})
        target_deps = {str(x).strip() for x in _as_list(target_stmt.get("depends_on")) if str(x).strip()}
        direct_dep = 1.0 if support and support in target_deps else 0.0

        coverage = 0.0
        evidence_terms = [str(x).strip().lower() for x in _as_list(hyp.get("evidence_terms")) if str(x).strip()]
        if evidence_terms:
            blob = " ".join(
                [
                    str(support_stmt.get("text", "")),
                    str(target_stmt.get("text", "")),
                    str(hyp.get("informal", "")),
                ]
            ).lower()
            hit = sum(1 for t in evidence_terms if t in blob)
            coverage = hit / len(evidence_terms)

        target_downstream_norm = _clamp01(_safe_float(downstream.get(target, 0.0), 0.0) / max_downstream)
        kind_bonus = 0.0
        if kind in {"intermediate-invariant", "definition-introduction"}:
            kind_bonus = 0.10
        elif kind in {"representation-shift", "normal-form-reduction"}:
            kind_bonus = 0.14
        elif kind == "barrier-escape-principle":
            kind_bonus = 0.12
        explanatory_power = _clamp01(
            0.34 * priority
            + 0.22 * analysis_score
            + 0.20 * target_downstream_norm
            + 0.14 * coverage
            + 0.10 * direct_dep
            + kind_bonus
        )

        hyp_edges = hyp_edges_by_id.get(hid, [])
        profile_with_hyp = _coherence_profile(nodes, base_edges + hyp_edges)
        coherence_delta = round(profile_with_hyp["global_coherence"] - base_profile["global_coherence"], 6)

        row = {
            "hypothesis_id": hid,
            "kind": kind,
            "target_statement_id": target,
            "support_statement_id": support,
            "priority": round(priority, 4),
            "explanatory_power_local": round(explanatory_power, 6),
            "coherence_delta_global": coherence_delta,
            "global_coherence_if_accepted": round(profile_with_hyp["global_coherence"], 6),
            "relation_types": sorted({str(e.get("relation", "")).strip() for e in hyp_edges if str(e.get("relation", "")).strip()}),
            "signals": {
                "analysis_score": round(analysis_score, 4),
                "direct_dependency": round(direct_dep, 4),
                "evidence_coverage": round(coverage, 4),
                "target_downstream_norm": round(target_downstream_norm, 4),
            },
        }
        rows.append(row)
        by_id[hid] = row

    rows.sort(key=lambda x: (x["explanatory_power_local"], x["coherence_delta_global"], x["priority"]), reverse=True)
    return rows, by_id, base_profile


def _hypothesis_edge_index(hypothesis_edges: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Creates the structural substrate that enables cross-stage scoring and interpretation.
    """

    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in hypothesis_edges:
        if not isinstance(edge, dict):
            continue
        hid = str(edge.get("hypothesis_id", "")).strip()
        if hid:
            out[hid].append(edge)
    return out


def _subset_objective(
    hypothesis_ids: tuple[str, ...],
    nodes: dict[str, dict[str, Any]],
    base_edges: list[dict[str, Any]],
    hypothesis_edges_by_id: dict[str, list[dict[str, Any]]],
    hypothesis_rows_by_id: dict[str, dict[str, Any]],
    statement_count: int,
) -> dict[str, Any]:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Quantitative evaluation of hypotheses or theory-graph properties.
    Contribution: Produces the quantitative signals used for retention, revision, and route prioritization.
    """

    selected_edges: list[dict[str, Any]] = list(base_edges)
    selected_rows: list[dict[str, Any]] = []
    covered_statements: set[str] = set()
    for hid in hypothesis_ids:
        selected_edges.extend(hypothesis_edges_by_id.get(hid, []))
        row = hypothesis_rows_by_id.get(hid)
        if not row:
            continue
        selected_rows.append(row)
        target = str(row.get("target_statement_id", "")).strip()
        support = str(row.get("support_statement_id", "")).strip()
        if target:
            covered_statements.add(target)
        if support:
            covered_statements.add(support)

    profile = _coherence_profile(nodes, selected_edges)
    if selected_rows:
        explanatory_avg = sum(_safe_float(r.get("explanatory_power_local"), 0.0) for r in selected_rows) / len(selected_rows)
        coherence_delta_avg = (
            sum(max(0.0, _safe_float(r.get("coherence_delta_global"), 0.0)) for r in selected_rows) / len(selected_rows)
        )
    else:
        explanatory_avg = 0.0
        coherence_delta_avg = 0.0

    coverage_ratio = len(covered_statements) / max(1, int(statement_count))
    size_penalty = len(hypothesis_ids) / max(1, len(hypothesis_rows_by_id))
    objective_score = (
        0.58 * _safe_float(profile.get("global_coherence"), 0.0)
        + 0.16 * explanatory_avg
        + 0.12 * coherence_delta_avg
        + 0.14 * coverage_ratio
        - 0.08 * size_penalty
    )

    return {
        "objective_score": round(objective_score, 6),
        "global_coherence": round(_safe_float(profile.get("global_coherence"), 0.0), 6),
        "profile": profile,
        "avg_explanatory_power": round(explanatory_avg, 6),
        "avg_positive_coherence_delta": round(coherence_delta_avg, 6),
        "coverage_ratio": round(coverage_ratio, 6),
        "size_penalty": round(size_penalty, 6),
    }


def _global_theory_search(
    nodes: dict[str, dict[str, Any]],
    base_edges: list[dict[str, Any]],
    hypothesis_edges: list[dict[str, Any]],
    hypothesis_rows: list[dict[str, Any]],
    statement_count: int,
    beam_width: int = 24,
    max_depth: int = 8,
) -> dict[str, Any]:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Selection/retrieval of the most relevant candidates for reasoning.
    Contribution: Produces a set-level coherentist objective instead of independent per-hypothesis triage.
    """

    row_by_id = {str(r.get("hypothesis_id", "")).strip(): r for r in hypothesis_rows if str(r.get("hypothesis_id", "")).strip()}
    if not row_by_id:
        return {
            "objective": "0.58*global_coherence + 0.16*avg_explanatory + 0.12*avg_positive_delta + 0.14*coverage - 0.08*size_penalty",
            "beam_width": beam_width,
            "max_depth": 0,
            "best_subset": {
                "hypothesis_ids": [],
                "objective_score": 0.0,
                "global_coherence": 0.0,
                "avg_explanatory_power": 0.0,
                "avg_positive_coherence_delta": 0.0,
                "coverage_ratio": 0.0,
                "size_penalty": 0.0,
            },
            "frontier_top": [],
        }

    edges_by_id = _hypothesis_edge_index(hypothesis_edges)
    ranked_ids = sorted(
        row_by_id.keys(),
        key=lambda hid: (
            0.50 * max(0.0, _safe_float(row_by_id[hid].get("coherence_delta_global"), 0.0))
            + 0.40 * _safe_float(row_by_id[hid].get("explanatory_power_local"), 0.0)
            + 0.10 * _safe_float(row_by_id[hid].get("priority"), 0.0)
        ),
        reverse=True,
    )
    search_depth = min(max(1, max_depth), len(ranked_ids))
    beam_width = max(1, beam_width)

    root_subset: tuple[str, ...] = tuple()
    root_metrics = _subset_objective(
        root_subset,
        nodes=nodes,
        base_edges=base_edges,
        hypothesis_edges_by_id=edges_by_id,
        hypothesis_rows_by_id=row_by_id,
        statement_count=statement_count,
    )
    frontier: list[tuple[tuple[str, ...], int, dict[str, Any]]] = [(root_subset, -1, root_metrics)]
    best_subset = root_subset
    best_metrics = root_metrics
    seen: set[tuple[str, ...]] = {root_subset}
    frontier_top: list[dict[str, Any]] = []

    for depth in range(search_depth):
        candidates: list[tuple[tuple[str, ...], int, dict[str, Any]]] = []
        for subset, last_idx, _metrics in frontier:
            for i in range(last_idx + 1, len(ranked_ids)):
                hid = ranked_ids[i]
                nxt = subset + (hid,)
                if nxt in seen:
                    continue
                seen.add(nxt)
                m = _subset_objective(
                    nxt,
                    nodes=nodes,
                    base_edges=base_edges,
                    hypothesis_edges_by_id=edges_by_id,
                    hypothesis_rows_by_id=row_by_id,
                    statement_count=statement_count,
                )
                candidates.append((nxt, i, m))

        if not candidates:
            break
        candidates.sort(key=lambda item: item[2]["objective_score"], reverse=True)
        frontier = candidates[:beam_width]
        leader_subset, _leader_idx, leader_metrics = frontier[0]
        if leader_metrics["objective_score"] > best_metrics["objective_score"]:
            best_subset = leader_subset
            best_metrics = leader_metrics
        frontier_top.append(
            {
                "depth": depth + 1,
                "best_hypothesis_ids": list(leader_subset),
                "best_objective_score": leader_metrics["objective_score"],
                "best_global_coherence": leader_metrics["global_coherence"],
            }
        )

    return {
        "objective": "0.58*global_coherence + 0.16*avg_explanatory + 0.12*avg_positive_delta + 0.14*coverage - 0.08*size_penalty",
        "beam_width": beam_width,
        "max_depth": search_depth,
        "candidate_rank": ranked_ids[:30],
        "best_subset": {
            "hypothesis_ids": list(best_subset),
            **best_metrics,
        },
        "frontier_top": frontier_top,
    }


def _revision_recommendations(
    hyp_rows: list[dict[str, Any]],
    core_theory_subset: set[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    recs: list[dict[str, Any]] = []
    core_theory_subset = core_theory_subset or set()
    for idx, row in enumerate(hyp_rows, start=1):
        hid = str(row.get("hypothesis_id", ""))
        exp = _safe_float(row.get("explanatory_power_local"), 0.0)
        delta = _safe_float(row.get("coherence_delta_global"), 0.0)
        if core_theory_subset and hid not in core_theory_subset and (delta <= 0.0 and exp < 0.35):
            recs.append(
                {
                    "revision_id": f"coh-rev.{idx:03d}",
                    "hypothesis_id": hid,
                    "priority": "high",
                    "action": "deprioritize-outside-core-theory-set",
                    "rationale": (
                        "Excluded by set-level coherentist search and shows weak local explanatory/coherence contribution."
                    ),
                }
            )
            continue
        if delta < -0.08:
            recs.append(
                {
                    "revision_id": f"coh-rev.{idx:03d}",
                    "hypothesis_id": hid,
                    "priority": "high",
                    "action": "demote-or-reformulate",
                    "rationale": f"Negative coherence delta ({delta:.4f}) indicates theory-level tension.",
                }
            )
        elif exp < 0.20 and delta <= 0:
            recs.append(
                {
                    "revision_id": f"coh-rev.{idx:03d}",
                    "hypothesis_id": hid,
                    "priority": "medium",
                    "action": "reframe-for-explanatory-power",
                    "rationale": f"Low explanatory power ({exp:.4f}) with non-positive coherence gain.",
                }
            )
    return recs[:30]


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    lines: list[str] = []
    lines.append("# Coherence and Explanatory Power Report")
    lines.append("")

    meta = report.get("metadata", {})
    profile = report.get("coherence_profile", {})
    lines.append("## Stats")
    lines.append("")
    lines.append(f"- Statements: {meta.get('statement_count', 0)}")
    lines.append(f"- Hypotheses: {meta.get('hypothesis_count', 0)}")
    lines.append(f"- Graph nodes: {meta.get('graph_node_count', 0)}")
    lines.append(f"- Graph edges: {meta.get('graph_edge_count', 0)}")
    lines.append("")

    lines.append("## Coherence Profile")
    lines.append("")
    lines.append(f"- Global coherence: {profile.get('global_coherence', 0.0)}")
    lines.append(f"- Consistency: {profile.get('consistency', 0.0)}")
    lines.append(f"- Integration: {profile.get('integration', 0.0)}")
    lines.append(f"- Explanatory unification: {profile.get('explanatory_unification', 0.0)}")
    lines.append(f"- Tension: {profile.get('tension', 0.0)}")
    lines.append("")

    set_search = report.get("global_theory_search", {}) if isinstance(report.get("global_theory_search"), dict) else {}
    best_subset = set_search.get("best_subset", {}) if isinstance(set_search.get("best_subset"), dict) else {}
    lines.append("## Global Theory Search")
    lines.append("")
    lines.append(f"- Objective: {set_search.get('objective', '')}")
    lines.append(f"- Beam width: {set_search.get('beam_width', 0)}")
    lines.append(f"- Max depth: {set_search.get('max_depth', 0)}")
    lines.append(f"- Best objective score: {best_subset.get('objective_score', 0.0)}")
    lines.append(f"- Best global coherence: {best_subset.get('global_coherence', 0.0)}")
    lines.append(f"- Best coverage ratio: {best_subset.get('coverage_ratio', 0.0)}")
    core_ids = best_subset.get("hypothesis_ids", []) if isinstance(best_subset.get("hypothesis_ids"), list) else []
    if core_ids:
        lines.append(f"- Core theory hypotheses: {', '.join(str(x) for x in core_ids)}")
    else:
        lines.append("- Core theory hypotheses: none")
    lines.append("")

    lines.append("## Hypothesis Signals")
    lines.append("")
    lines.append("| hypothesis_id | kind | explanatory_power | coherence_delta | global_if_accepted |")
    lines.append("|---|---|---|---|---|")
    for item in report.get("hypothesis_coherence", []):
        lines.append(
            f"| {item.get('hypothesis_id', '')} | {item.get('kind', '')} | "
            f"{item.get('explanatory_power_local', 0.0)} | {item.get('coherence_delta_global', 0.0)} | "
            f"{item.get('global_coherence_if_accepted', 0.0)} |"
        )
    lines.append("")

    lines.append("## Belief Revision Recommendations")
    lines.append("")
    recs = report.get("belief_revision_recommendations", [])
    if not recs:
        lines.append("- none")
    for rec in recs:
        lines.append(f"- {rec.get('hypothesis_id', '')}: {rec.get('action', '')} ({rec.get('rationale', '')})")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    """
    Relevance: Operates within the coherence evaluation layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-coherence-evaluator")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb", required=True, help="Path to KB markdown file.")
    ap.add_argument("--analysis", required=True, help="Path to connection-analysis JSON.")
    ap.add_argument("--phyp", required=True, help="Path to hypotheses YAML.")
    ap.add_argument("--output-json", help="Output JSON path.")
    ap.add_argument("--output-md", help="Output Markdown path.")
    args = ap.parse_args()
    logger.step(
        "Parsed coherence-evaluator arguments",
        "\n".join(
            [
                f"kb={args.kb}",
                f"analysis={args.analysis}",
                f"phyp={args.phyp}",
                f"output_json={args.output_json or ''}",
                f"output_md={args.output_md or ''}",
            ]
        ),
    )

    kb_path = Path(args.kb)
    analysis_path = Path(args.analysis)
    phyp_path = Path(args.phyp)
    for p in [kb_path, analysis_path, phyp_path]:
        if not p.exists():
            log_path = logger.finalize("error", summary=f"Missing input: {p}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input: {p}")

    statements = _extract_statements(kb_path)
    try:
        analysis = validate_connection_analysis(json.loads(analysis_path.read_text(encoding="utf-8")), name="analysis")
        phyp = validate_phyp(yaml.safe_load(phyp_path.read_text(encoding="utf-8")), name="phyp")
    except ValueError as exc:
        log_path = logger.finalize("error", summary=str(exc))
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] {exc}")

    # Build the theory graph once, then derive both global and per-hypothesis
    # signals from the same typed structure.
    nodes, base_edges, hypothesis_edges, relation_counts = _build_graph(statements, analysis, phyp)
    hyp_rows, hyp_by_id, base_profile = _hypothesis_signal_rows(
        statements=statements,
        analysis=analysis,
        phyp=phyp,
        nodes=nodes,
        base_edges=base_edges,
        hypothesis_edges=hypothesis_edges,
    )
    full_profile = _coherence_profile(nodes, base_edges + hypothesis_edges)
    set_search = _global_theory_search(
        nodes=nodes,
        base_edges=base_edges,
        hypothesis_edges=hypothesis_edges,
        hypothesis_rows=hyp_rows,
        statement_count=len(statements),
    )
    core_subset = {
        str(x).strip()
        for x in (set_search.get("best_subset", {}).get("hypothesis_ids", []) if isinstance(set_search, dict) else [])
        if str(x).strip()
    }
    revisions = _revision_recommendations(hyp_rows, core_theory_subset=core_subset)

    report = {
        "metadata": {
            "kb": str(kb_path),
            "analysis": str(analysis_path),
            "phyp": str(phyp_path),
            "statement_count": len(statements),
            "hypothesis_count": len(phyp.get("hypotheses", [])),
            "graph_node_count": len(nodes),
            "graph_edge_count": len(base_edges) + len(hypothesis_edges),
        },
        "coherence_profile": base_profile,
        "coherence_profile_with_all_hypotheses": full_profile,
        "global_theory_search": set_search,
        "typed_coherence_graph": {
            "nodes": list(nodes.values()),
            "edges": base_edges + hypothesis_edges,
            "relation_counts": relation_counts,
        },
        "hypothesis_coherence": hyp_rows,
        "hypothesis_coherence_index": hyp_by_id,
        "belief_revision_recommendations": revisions,
    }

    if args.output_json:
        out_json = Path(args.output_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[OK] Wrote JSON: {out_json}")
        logger.add_output("coherence_report_json", out_json)

    if args.output_md:
        out_md = Path(args.output_md)
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(_to_markdown(report), encoding="utf-8")
        print(f"[OK] Wrote Markdown: {out_md}")
        logger.add_output("coherence_report_md", out_md)

    logger.step(
        "Computed coherence profile",
        "\n".join(
            [
                f"global_coherence={base_profile.get('global_coherence', 0.0)}",
                f"core_subset_size={len(core_subset)}",
                f"hypothesis_rows={len(hyp_rows)}",
                f"revision_recommendations={len(revisions)}",
            ]
        ),
    )
    log_path = logger.finalize(
        "success",
        summary=f"Built coherence graph with {len(nodes)} nodes and {len(base_edges) + len(hypothesis_edges)} edges.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
