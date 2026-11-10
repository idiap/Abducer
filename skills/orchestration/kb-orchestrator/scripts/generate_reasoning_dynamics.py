#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Compute reasoning-dynamics metrics and visualization artifacts from process-graph evolution."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger


AGENT_FROM_DESC_RE = re.compile(r"^(.+?)\s+started log\s+", re.IGNORECASE)
_OP_EDGE_TO_KEY = {
    "stage_started": "stage_started",
    "stage_completed": "stage_completed",
    "declares_output": "declared_output",
    "declared_output": "declared_output",
    "emits_output": "emits_output",
    "invokes_agent": "invokes_agent",
}


def _safe_float(value: Any, default: float = 0.0) -> float:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _load_json(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _parse_ts(value: str) -> dt.datetime | None:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    text = (value or "").strip()
    if not text:
        return None
    try:
        return dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def _normalize_counter(counter: Counter[str]) -> dict[str, int]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Normalization of input structures into stable internal forms.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    return {k: int(v) for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))}


def _distribution(counter: Counter[str]) -> dict[str, float]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    total = sum(counter.values())
    if total <= 0:
        return {}
    return {k: round(v / total, 6) for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))}


def _series_min_max(values: list[float]) -> tuple[float, float]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if not values:
        return (0.0, 0.0)
    return (min(values), max(values))


def _entropy(counts: dict[str, int]) -> float:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    total = sum(max(0, int(v)) for v in counts.values())
    if total <= 0:
        return 0.0
    ent = 0.0
    for val in counts.values():
        p = max(0.0, float(val) / total)
        if p > 0:
            ent -= p * math.log(p, 2)
    return ent


def _edge_type_counts(edge_ids: list[str], edge_map: dict[str, dict[str, Any]]) -> Counter[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    c: Counter[str] = Counter()
    for eid in edge_ids:
        edge = edge_map.get(eid, {})
        et = str(edge.get("edge_type", "unknown")).strip() or "unknown"
        c[et] += 1
    return c


def _node_type_counts(node_ids: list[str], node_map: dict[str, dict[str, Any]]) -> Counter[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    c: Counter[str] = Counter()
    for nid in node_ids:
        node = node_map.get(nid, {})
        nt = str(node.get("node_type", "unknown")).strip() or "unknown"
        c[nt] += 1
    return c


def _infer_agent_from_state(
    state: dict[str, Any],
    added_nodes: list[dict[str, Any]],
    added_edges: list[dict[str, Any]],
) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    desc = str(state.get("description", "")).strip()
    m = AGENT_FROM_DESC_RE.match(desc)
    if m:
        return m.group(1).strip()

    for node in added_nodes:
        if str(node.get("node_type", "")).strip() == "step":
            meta = node.get("meta", {})
            if isinstance(meta, dict):
                agent = str(meta.get("agent", "")).strip()
                if agent:
                    return agent

    for edge in added_edges:
        if str(edge.get("edge_type", "")).strip() == "executed_by":
            target = str(edge.get("target", "")).strip()
            if target.startswith("agent:"):
                return target.split("agent:", 1)[1]
    return ""


def _artifact_metrics_from_connection_analysis(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    stats = payload.get("stats", {}) if isinstance(payload.get("stats"), dict) else {}
    concept_graph = payload.get("concept_graph", {}) if isinstance(payload.get("concept_graph"), dict) else {}
    relations = concept_graph.get("relations", []) if isinstance(concept_graph.get("relations"), list) else []
    nodes = concept_graph.get("nodes", []) if isinstance(concept_graph.get("nodes"), list) else []
    rel_counts: dict[str, int] = {}
    for rel in relations:
        if not isinstance(rel, dict):
            continue
        name = str(rel.get("relation", "unknown")).strip() or "unknown"
        rel_counts[name] = rel_counts.get(name, 0) + 1
    return {
        "concept_graph_nodes": len(nodes),
        "concept_graph_relations": len(relations),
        "concept_relation_types": rel_counts,
        "analysis_statement_count": _safe_int(stats.get("statement_count", 0)),
        "analysis_dependency_edges": _safe_int(stats.get("edge_count", 0)),
        "analysis_missing_dependency_count": _safe_int(stats.get("missing_dependency_count", 0)),
        "analysis_connection_candidates": len(payload.get("connection_candidates", []))
        if isinstance(payload.get("connection_candidates"), list)
        else 0,
        "analysis_top_interventions": len(payload.get("top_interventions", []))
        if isinstance(payload.get("top_interventions"), list)
        else 0,
    }


def _artifact_metrics_from_hypotheses(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    hypotheses = payload.get("hypotheses", []) if isinstance(payload.get("hypotheses"), list) else []
    kind_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    for hyp in hypotheses:
        if not isinstance(hyp, dict):
            continue
        kind = str(hyp.get("kind", "unknown")).strip() or "unknown"
        status = str(hyp.get("status", "unknown")).strip() or "unknown"
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1
    return {
        "hypothesis_total": len(hypotheses),
        "hypothesis_kind_counts": kind_counts,
        "hypothesis_status_counts": status_counts,
    }


def _artifact_metrics_from_coherence(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    profile = payload.get("coherence_profile", {}) if isinstance(payload.get("coherence_profile"), dict) else {}
    graph = payload.get("typed_coherence_graph", {}) if isinstance(payload.get("typed_coherence_graph"), dict) else {}
    relation_counts = graph.get("relation_counts", {}) if isinstance(graph.get("relation_counts"), dict) else {}
    return {
        "coherence_global": _safe_float(profile.get("global_coherence", 0.0)),
        "coherence_consistency": _safe_float(profile.get("consistency", 0.0)),
        "coherence_integration": _safe_float(profile.get("integration", 0.0)),
        "coherence_tension": _safe_float(profile.get("tension", 0.0)),
        "coherence_explanatory_unification": _safe_float(profile.get("explanatory_unification", 0.0)),
        "coherence_graph_nodes": len(graph.get("nodes", [])) if isinstance(graph.get("nodes"), list) else 0,
        "coherence_graph_edges": len(graph.get("edges", [])) if isinstance(graph.get("edges"), list) else 0,
        "coherence_relation_types": {str(k): _safe_int(v) for k, v in relation_counts.items()},
    }


def _artifact_metrics_from_entrypoints(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return {
        "entrypoint_count": len(payload.get("ranked_entrypoints", []))
        if isinstance(payload.get("ranked_entrypoints"), list)
        else 0,
        "concept_track_count": len(payload.get("concept_tracks", []))
        if isinstance(payload.get("concept_tracks"), list)
        else 0,
    }


def _artifact_metrics_from_pathways(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return {
        "pathway_count": len(payload.get("pathways", [])) if isinstance(payload.get("pathways"), list) else 0,
    }


def _artifact_metrics_from_hardness(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return {
        "hardness_elements": len(payload.get("essential_elements", []))
        if isinstance(payload.get("essential_elements"), list)
        else 0,
        "anti_barrier_programs": len(payload.get("anti_barrier_programs", []))
        if isinstance(payload.get("anti_barrier_programs"), list)
        else 0,
    }


def _artifact_metrics_from_bridge_plan(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    programs = payload.get("bridge_programs", []) if isinstance(payload.get("bridge_programs"), list) else []
    avg_score = 0.0
    if programs:
        avg_score = sum(_safe_float(p.get("bridge_score", 0.0)) for p in programs if isinstance(p, dict)) / len(programs)
    return {
        "bridge_program_count": len(programs),
        "bridge_program_score_avg": round(avg_score, 6),
    }


def _artifact_metrics_from_strategies(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    strategies = payload.get("strategies", []) if isinstance(payload.get("strategies"), list) else []
    fert = []
    for item in strategies:
        if isinstance(item, dict):
            fert.append(_safe_float(item.get("concept_fertility", 0.0)))
    avg_fert = sum(fert) / len(fert) if fert else 0.0
    return {
        "strategy_count": len(strategies),
        "strategy_fertility_avg": round(avg_fert, 6),
    }


def _artifact_metrics_from_hypothesis_eval(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    summary = payload.get("summary", {}) if isinstance(payload.get("summary"), dict) else {}
    verdict = summary.get("verdict_counts", {}) if isinstance(summary.get("verdict_counts"), dict) else {}
    return {
        "hyp_eval_supported": _safe_int(verdict.get("supported", 0))
        + _safe_int(verdict.get("provisionally-supported", 0)),
        "hyp_eval_refuted": _safe_int(verdict.get("refuted", 0))
        + _safe_int(verdict.get("provisionally-refuted", 0)),
        "hyp_eval_inconclusive": _safe_int(verdict.get("inconclusive", 0)),
    }


def _artifact_metrics_from_hypothesis_loop(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    meta = payload.get("metadata", {}) if isinstance(payload.get("metadata"), dict) else {}
    final = payload.get("final_summary", {}) if isinstance(payload.get("final_summary"), dict) else {}
    return {
        "loop_rounds_executed": _safe_int(meta.get("rounds_executed", 0)),
        "loop_supported_count": _safe_int(final.get("supported_count", 0)),
        "loop_refuted_count": _safe_int(final.get("refuted_count", 0)),
        "loop_open_count": _safe_int(final.get("open_count", 0)),
    }


def _artifact_metrics_from_revision(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    summary = payload.get("revision_summary", {}) if isinstance(payload.get("revision_summary"), dict) else {}
    return {
        "revision_count": _safe_int(summary.get("revision_count", 0)),
        "revision_low_coherence_hypotheses": _safe_int(summary.get("low_coherence_hypotheses", 0)),
    }


def _artifact_metrics_from_log_index(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    summary = payload.get("summary", {}) if isinstance(payload.get("summary"), dict) else {}
    return {
        "log_coverage_missing_expected_agents": len(summary.get("missing_expected_agents", []))
        if isinstance(summary.get("missing_expected_agents"), list)
        else 0,
        "log_indexed_count": _safe_int(summary.get("log_count", 0)),
    }


def _extract_artifact_metrics(path: Path) -> tuple[str, dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    name = path.name
    if not path.exists() or not path.is_file():
        return ("missing", {})
    if path.suffix.lower() == ".json":
        try:
            payload = _load_json(path)
        except Exception:
            return ("invalid-json", {})
        if name.endswith("connection-analysis.json"):
            return ("connection-analysis", _artifact_metrics_from_connection_analysis(payload))
        if name.endswith("coherence-report.json"):
            return ("coherence-report", _artifact_metrics_from_coherence(payload))
        if name.endswith("entrypoints.json"):
            return ("entrypoints", _artifact_metrics_from_entrypoints(payload))
        if name.endswith("entrypoint-pathways.json"):
            return ("entrypoint-pathways", _artifact_metrics_from_pathways(payload))
        if name.endswith("epistemic-hardness.json"):
            return ("epistemic-hardness", _artifact_metrics_from_hardness(payload))
        if name.endswith("bridge-plan.json"):
            return ("bridge-plan", _artifact_metrics_from_bridge_plan(payload))
        if name.endswith("proof-strategies.json"):
            return ("proof-strategies", _artifact_metrics_from_strategies(payload))
        if name.endswith("hypothesis-evaluation.json"):
            return ("hypothesis-evaluation", _artifact_metrics_from_hypothesis_eval(payload))
        if name.endswith("hypothesis-refutation-loop.json"):
            return ("hypothesis-refutation-loop", _artifact_metrics_from_hypothesis_loop(payload))
        if name.endswith("revision-loop.json"):
            return ("revision-loop", _artifact_metrics_from_revision(payload))
        if name.endswith("reasoning-log-index.json"):
            return ("reasoning-log-index", _artifact_metrics_from_log_index(payload))
        return ("json", {})

    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            return ("invalid-yaml", {})
        if not isinstance(payload, dict):
            return ("yaml", {})
        if ".proof-hypotheses." in name or ".hypotheses-reviewed." in name:
            return ("phyp", _artifact_metrics_from_hypotheses(payload))
        return ("yaml", {})
    return ("other", {})


def _merge_concept_state(current: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    out = dict(current)
    for key, value in updates.items():
        out[key] = value
    return out


def _compute_concept_topology_index(state: dict[str, Any]) -> float:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    concept_nodes = _safe_float(state.get("concept_graph_nodes", 0.0), 0.0)
    concept_relations = _safe_float(state.get("concept_graph_relations", 0.0), 0.0)
    coherence_global = max(0.0, min(1.0, _safe_float(state.get("coherence_global", 0.0), 0.0)))
    relation_types = state.get("concept_relation_types", {})
    if not isinstance(relation_types, dict):
        relation_types = {}
    type_diversity = 0.0
    if relation_types:
        total = sum(max(0, _safe_int(v, 0)) for v in relation_types.values())
        type_diversity = min(1.0, len(relation_types) / max(1.0, total))
    density = 0.0
    if concept_nodes > 1:
        density = max(0.0, min(1.0, concept_relations / (concept_nodes * (concept_nodes - 1))))
    topology_index = max(0.0, min(1.0, 0.40 * density + 0.35 * type_diversity + 0.25 * coherence_global))
    return round(topology_index, 6)


def _build_dynamics(
    evolution: dict[str, Any],
    artifact_root: Path,
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Creates the structural substrate that enables cross-stage scoring and interpretation.
    """

    states = evolution.get("states", []) if isinstance(evolution.get("states"), list) else []
    final_graph = evolution.get("final_graph", {}) if isinstance(evolution.get("final_graph"), dict) else {}
    node_map = {
        str(n.get("id", "")).strip(): n
        for n in final_graph.get("nodes", [])
        if isinstance(n, dict) and str(n.get("id", "")).strip()
    }
    edge_map = {
        str(e.get("id", "")).strip(): e
        for e in final_graph.get("edges", [])
        if isinstance(e, dict) and str(e.get("id", "")).strip()
    }

    timeline: list[dict[str, Any]] = []
    event_counter: Counter[str] = Counter()
    added_edge_counter: Counter[str] = Counter()
    agent_counter: Counter[str] = Counter()
    run_counter: Counter[str] = Counter()
    seen_artifacts: set[str] = set()
    concept_state: dict[str, Any] = {}
    concept_updates: list[dict[str, Any]] = []

    first_ts: dt.datetime | None = None
    last_ts: dt.datetime | None = None
    operation_totals = {
        "stage_started": 0,
        "stage_completed": 0,
        "declared_output": 0,
        "emits_output": 0,
        "invokes_agent": 0,
    }

    for idx, state in enumerate(states):
        node_ids = [str(x).strip() for x in state.get("node_ids", []) if str(x).strip()]
        edge_ids = [str(x).strip() for x in state.get("edge_ids", []) if str(x).strip()]
        added_node_ids = [str(x).strip() for x in state.get("added_node_ids", []) if str(x).strip()]
        added_edge_ids = [str(x).strip() for x in state.get("added_edge_ids", []) if str(x).strip()]

        ts = _parse_ts(str(state.get("timestamp", "")))
        if ts and first_ts is None:
            first_ts = ts
        if ts:
            last_ts = ts
        elapsed_s = 0.0
        if ts and first_ts:
            elapsed_s = (ts - first_ts).total_seconds()

        added_nodes = [node_map[nid] for nid in added_node_ids if nid in node_map]
        added_edges = [edge_map[eid] for eid in added_edge_ids if eid in edge_map]
        node_types = _node_type_counts(node_ids, node_map)
        edge_types = _edge_type_counts(edge_ids, edge_map)

        event_type = str(state.get("event_type", "unknown")).strip() or "unknown"
        event_counter[event_type] += 1
        run_key = str(state.get("run_key", "")).strip() or "(unknown)"
        run_counter[run_key] += 1

        agent = _infer_agent_from_state(state, added_nodes, added_edges)
        if agent:
            agent_counter[agent] += 1

        added_edge_types: Counter[str] = Counter()
        for edge in added_edges:
            et = str(edge.get("edge_type", "unknown")).strip() or "unknown"
            added_edge_types[et] += 1
            added_edge_counter[et] += 1
            op_key = _OP_EDGE_TO_KEY.get(et)
            if op_key:
                operation_totals[op_key] += 1

        artifact_updates: list[dict[str, Any]] = []
        for node in added_nodes:
            if str(node.get("node_type", "")).strip() != "artifact":
                continue
            meta = node.get("meta", {})
            if not isinstance(meta, dict):
                continue
            path_text = str(meta.get("path", "")).strip()
            if not path_text:
                continue
            abs_path = Path(path_text)
            if not abs_path.is_absolute():
                abs_path = (artifact_root / abs_path).resolve()
            key = str(abs_path)
            if key in seen_artifacts:
                continue
            seen_artifacts.add(key)
            artifact_kind, metrics = _extract_artifact_metrics(abs_path)
            if not metrics:
                continue
            concept_state = _merge_concept_state(concept_state, metrics)
            concept_state["concept_topology_index"] = _compute_concept_topology_index(concept_state)
            update = {
                "state_index": idx,
                "timestamp": str(state.get("timestamp", "")),
                "artifact_path": key,
                "artifact_kind": artifact_kind,
                "metrics": metrics,
            }
            artifact_updates.append(update)
            concept_updates.append(update)

        n = len(node_ids)
        m = len(edge_ids)
        density = 0.0
        if n > 1:
            density = m / float(n * (n - 1))
        timeline.append(
            {
                "index": _safe_int(state.get("index", idx), idx),
                "timestamp": str(state.get("timestamp", "")),
                "elapsed_s": round(elapsed_s, 6),
                "run_key": run_key,
                "event_type": event_type,
                "description": str(state.get("description", "")),
                "agent": agent,
                "graph": {
                    "node_count": n,
                    "edge_count": m,
                    "density": round(density, 6),
                    "node_type_counts": dict(node_types),
                    "edge_type_counts": dict(edge_types),
                    "node_type_entropy": round(_entropy(dict(node_types)), 6),
                    "edge_type_entropy": round(_entropy(dict(edge_types)), 6),
                },
                "process": {
                    "added_node_count": len(added_node_ids),
                    "added_edge_count": len(added_edge_ids),
                    "added_edge_type_counts": dict(added_edge_types),
                    "cumulative_event_counts": dict(event_counter),
                    "cumulative_operation_counts": dict(operation_totals),
                },
                "concept": dict(concept_state),
                "artifact_updates": artifact_updates,
            }
        )

    graph_nodes_series = [float(item["graph"]["node_count"]) for item in timeline]
    graph_edges_series = [float(item["graph"]["edge_count"]) for item in timeline]
    density_series = [float(item["graph"]["density"]) for item in timeline]
    concept_idx_series = [float(item.get("concept", {}).get("concept_topology_index", 0.0) or 0.0) for item in timeline]

    total_time_s = 0.0
    if first_ts and last_ts:
        total_time_s = max(0.0, (last_ts - first_ts).total_seconds())

    graph_growth_nodes = 0.0
    graph_growth_edges = 0.0
    if graph_nodes_series:
        graph_growth_nodes = graph_nodes_series[-1] - graph_nodes_series[0]
    if graph_edges_series:
        graph_growth_edges = graph_edges_series[-1] - graph_edges_series[0]

    concept_final = timeline[-1]["concept"] if timeline else {}
    summary = {
        "state_count": len(timeline),
        "time_span_seconds": round(total_time_s, 6),
        "graph_growth": {
            "nodes_initial": int(graph_nodes_series[0]) if graph_nodes_series else 0,
            "nodes_final": int(graph_nodes_series[-1]) if graph_nodes_series else 0,
            "nodes_growth": int(graph_growth_nodes),
            "edges_initial": int(graph_edges_series[0]) if graph_edges_series else 0,
            "edges_final": int(graph_edges_series[-1]) if graph_edges_series else 0,
            "edges_growth": int(graph_growth_edges),
            "density_min_max": [round(x, 6) for x in _series_min_max(density_series)],
        },
        "process_distribution": {
            "event_type_counts": _normalize_counter(event_counter),
            "event_type_distribution": _distribution(event_counter),
            "operation_edge_type_counts": _normalize_counter(added_edge_counter),
            "agent_activity_counts": _normalize_counter(agent_counter),
            "run_activity_counts": _normalize_counter(run_counter),
        },
        "operation_totals": {k: int(v) for k, v in operation_totals.items()},
        "concept_evolution": {
            "update_count": len(concept_updates),
            "final_state": concept_final,
            "topology_index_min_max": [round(x, 6) for x in _series_min_max(concept_idx_series)],
            "updates": concept_updates[:300],
        },
    }

    return {
        "summary": summary,
        "timeline": timeline,
        "metric_catalog": [
            {
                "name": "graph.node_count",
                "category": "graph",
                "description": "Cumulative number of nodes in the reasoning process graph.",
            },
            {
                "name": "graph.edge_count",
                "category": "graph",
                "description": "Cumulative number of typed edges in the reasoning process graph.",
            },
            {
                "name": "graph.density",
                "category": "graph",
                "description": "Directed edge density m/(n*(n-1)), used as topological compactness proxy.",
            },
            {
                "name": "process.added_edge_type_counts",
                "category": "process",
                "description": "Number of new operations by typed edge additions per state.",
            },
            {
                "name": "process.cumulative_event_counts",
                "category": "process",
                "description": "Cumulative distribution of event types over reasoning time.",
            },
            {
                "name": "concept.concept_topology_index",
                "category": "concept",
                "description": "Composite index from concept density, relation-type diversity, and coherence.",
            },
            {
                "name": "concept.coherence_global",
                "category": "concept",
                "description": "Global coherence signal from coherence-report snapshots when available.",
            },
            {
                "name": "concept.hypothesis_total",
                "category": "concept",
                "description": "Current hypothesis population from phyp artifacts over time.",
            },
            {
                "name": "concept.loop_open_count",
                "category": "concept",
                "description": "Open hypotheses count from refutation-loop outputs.",
            },
        ],
    }


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    graph = summary.get("graph_growth", {}) if isinstance(summary.get("graph_growth"), dict) else {}
    process = summary.get("process_distribution", {}) if isinstance(summary.get("process_distribution"), dict) else {}
    concept = summary.get("concept_evolution", {}) if isinstance(summary.get("concept_evolution"), dict) else {}
    lines: list[str] = []
    lines.append("# Reasoning Dynamics Report")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(f"- States: {summary.get('state_count', 0)}")
    lines.append(f"- Time span (s): {summary.get('time_span_seconds', 0.0)}")
    lines.append(f"- Node growth: {graph.get('nodes_initial', 0)} -> {graph.get('nodes_final', 0)}")
    lines.append(f"- Edge growth: {graph.get('edges_initial', 0)} -> {graph.get('edges_final', 0)}")
    lines.append(f"- Concept update checkpoints: {concept.get('update_count', 0)}")
    lines.append("")

    lines.append("## Process Distribution")
    lines.append("")
    event_counts = process.get("event_type_counts", {}) if isinstance(process.get("event_type_counts"), dict) else {}
    for key, value in event_counts.items():
        lines.append(f"- event `{key}`: {value}")
    lines.append("")

    lines.append("## Operation Totals")
    lines.append("")
    op_totals = summary.get("operation_totals", {}) if isinstance(summary.get("operation_totals"), dict) else {}
    for key, value in sorted(op_totals.items()):
        lines.append(f"- `{key}`: {value}")
    lines.append("")

    lines.append("## Conceptual Topology")
    lines.append("")
    final_concept = concept.get("final_state", {}) if isinstance(concept.get("final_state"), dict) else {}
    for key in [
        "concept_graph_nodes",
        "concept_graph_relations",
        "coherence_global",
        "hypothesis_total",
        "loop_open_count",
        "concept_topology_index",
    ]:
        if key in final_concept:
            lines.append(f"- {key}: {final_concept.get(key)}")
    lines.append("")

    lines.append("## Interpretation Hints")
    lines.append("")
    lines.append("- Rising `graph.edge_count` with stable or improving `concept_topology_index` indicates productive expansion.")
    lines.append("- High `stage_started` but low `declared_output` suggests orchestration churn without artifact yield.")
    lines.append("- Falling `loop_open_count` with non-negative `coherence_global` indicates healthier inferential convergence.")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _render_html(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    payload = json.dumps(report, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Reasoning Dynamics Dashboard</title>
  <style>
    :root {{
      --bg: #f2f6fb;
      --panel: #ffffff;
      --line: #d8e1ea;
      --text: #132437;
      --muted: #5f7284;
      --accent: #0b7285;
    }}
    body {{
      margin: 0;
      background: radial-gradient(circle at 10% 10%, #e7eef7 0%, #f2f6fb 45%, #edf3fa 100%);
      color: var(--text);
      font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
    }}
    .wrap {{
      max-width: 1480px;
      margin: 0 auto;
      padding: 16px;
      display: grid;
      grid-template-columns: 1fr 360px;
      gap: 16px;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 12px;
      box-shadow: 0 10px 20px rgba(19, 36, 55, 0.08);
      overflow: hidden;
    }}
    .toolbar {{
      padding: 12px;
      border-bottom: 1px solid var(--line);
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }}
    .toolbar input[type=range] {{ width: 280px; }}
    .toolbar button {{
      border: 1px solid #c4d1de;
      background: #fff;
      border-radius: 8px;
      padding: 6px 10px;
      cursor: pointer;
      color: #16324b;
    }}
    .toolbar button:hover {{ background: #f3f8fd; }}
    .meta {{ margin-left: auto; color: var(--muted); font-size: 12px; }}
    .charts {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      padding: 12px;
    }}
    .chart {{
      border: 1px solid var(--line);
      border-radius: 10px;
      overflow: hidden;
      background: #fbfdff;
    }}
    .chart h4 {{
      margin: 0;
      padding: 8px 10px;
      border-bottom: 1px solid var(--line);
      font-size: 13px;
      color: #2d4b66;
      text-transform: uppercase;
      letter-spacing: .03em;
    }}
    canvas {{ width: 100%; height: 250px; display: block; }}
    .side {{
      padding: 12px;
      font-size: 13px;
      line-height: 1.35;
    }}
    .kpi {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 10px;
    }}
    .kpi .item {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px;
      background: #fbfdff;
    }}
    .kpi .label {{ color: var(--muted); font-size: 11px; text-transform: uppercase; }}
    .kpi .value {{ font-weight: 600; font-size: 16px; }}
    .list {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px;
      background: #fbfdff;
      max-height: 280px;
      overflow: auto;
    }}
    .row {{ display: flex; justify-content: space-between; gap: 8px; margin: 4px 0; }}
    .row span:first-child {{ color: #2e4f6d; }}
    .row span:last-child {{ color: #132437; font-weight: 600; }}
    .state {{
      margin-top: 10px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px;
      background: #fbfdff;
    }}
    .state .title {{
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      margin-bottom: 6px;
    }}
    .state .desc {{ font-weight: 600; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="panel">
      <div class="toolbar">
        <button id="prevBtn">Prev</button>
        <button id="playBtn">Play</button>
        <button id="nextBtn">Next</button>
        <label>State <input id="stateRange" type="range" min="0" max="0" value="0"/></label>
        <div class="meta" id="metaText"></div>
      </div>
      <div class="charts">
        <div class="chart"><h4>Graph Growth</h4><canvas id="graphChart" width="700" height="250"></canvas></div>
        <div class="chart"><h4>Operation Dynamics</h4><canvas id="opsChart" width="700" height="250"></canvas></div>
        <div class="chart"><h4>Concept Evolution</h4><canvas id="conceptChart" width="700" height="250"></canvas></div>
        <div class="chart"><h4>Event Distribution</h4><canvas id="eventChart" width="700" height="250"></canvas></div>
      </div>
    </div>
    <div class="panel side">
      <div class="kpi" id="kpi"></div>
      <h4 style="margin:8px 0;">Agent Activity</h4>
      <div class="list" id="agentList"></div>
      <h4 style="margin:8px 0;">Operation Totals</h4>
      <div class="list" id="opsList"></div>
      <div class="state">
        <div class="title">Current State</div>
        <div><strong id="stateIdx">0</strong> <span id="stateTs"></span></div>
        <div id="stateEvt"></div>
        <div class="desc" id="stateDesc"></div>
      </div>
    </div>
  </div>
  <script>
    const DATA = {payload};
    const timeline = Array.isArray(DATA.timeline) ? DATA.timeline : [];
    const summary = DATA.summary || {{}};

    const range = document.getElementById("stateRange");
    const playBtn = document.getElementById("playBtn");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const metaText = document.getElementById("metaText");
    const stateIdx = document.getElementById("stateIdx");
    const stateTs = document.getElementById("stateTs");
    const stateEvt = document.getElementById("stateEvt");
    const stateDesc = document.getElementById("stateDesc");
    const kpi = document.getElementById("kpi");
    const agentList = document.getElementById("agentList");
    const opsList = document.getElementById("opsList");

    range.max = Math.max(0, timeline.length - 1);
    range.value = String(Math.max(0, timeline.length - 1));
    metaText.textContent = `States: ${{timeline.length}}`;

    function byKey(obj) {{
      return Object.entries(obj || {{}}).sort((a,b)=>b[1]-a[1]);
    }}

    function drawKPI() {{
      const g = summary.graph_growth || {{}};
      const c = (summary.concept_evolution || {{}}).final_state || {{}};
      const cards = [
        ["States", summary.state_count || 0],
        ["Node Growth", `${{g.nodes_initial||0}} -> ${{g.nodes_final||0}}`],
        ["Edge Growth", `${{g.edges_initial||0}} -> ${{g.edges_final||0}}`],
        ["Concept Topology", c.concept_topology_index ?? 0],
        ["Coherence", c.coherence_global ?? 0],
        ["Open Hypotheses", c.loop_open_count ?? 0],
      ];
      kpi.innerHTML = cards.map(([k,v]) => `<div class="item"><div class="label">${{k}}</div><div class="value">${{v}}</div></div>`).join("");

      const agents = byKey((summary.process_distribution || {{}}).agent_activity_counts);
      agentList.innerHTML = agents.map(([k,v]) => `<div class="row"><span>${{k}}</span><span>${{v}}</span></div>`).join("") || "<div class='row'><span>none</span><span>0</span></div>";

      const ops = byKey(summary.operation_totals || {{}});
      opsList.innerHTML = ops.map(([k,v]) => `<div class="row"><span>${{k}}</span><span>${{v}}</span></div>`).join("") || "<div class='row'><span>none</span><span>0</span></div>";
    }}

    function getSeries(selector) {{
      return timeline.map(selector);
    }}

    function drawLineChart(canvasId, series, cursorIndex) {{
      const canvas = document.getElementById(canvasId);
      const ctx = canvas.getContext("2d");
      const w = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0,0,w,h);
      const pad = 34;
      const xs = Math.max(1, timeline.length - 1);
      let ymin = Infinity, ymax = -Infinity;
      for (const s of series) {{
        for (const v of s.values) {{
          if (v === null || v === undefined || Number.isNaN(v)) continue;
          ymin = Math.min(ymin, v);
          ymax = Math.max(ymax, v);
        }}
      }}
      if (!Number.isFinite(ymin) || !Number.isFinite(ymax)) {{ ymin = 0; ymax = 1; }}
      if (Math.abs(ymax - ymin) < 1e-9) ymax = ymin + 1;

      ctx.strokeStyle = "#d7e1ea";
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(pad, h-pad); ctx.lineTo(w-pad, h-pad); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(pad, pad); ctx.lineTo(pad, h-pad); ctx.stroke();

      function px(i) {{ return pad + (w-2*pad) * (i/xs); }}
      function py(v) {{ return h-pad - (h-2*pad) * ((v-ymin)/(ymax-ymin)); }}

      for (const s of series) {{
        ctx.strokeStyle = s.color;
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        let started = false;
        for (let i=0;i<s.values.length;i++) {{
          const v = s.values[i];
          if (v === null || v === undefined || Number.isNaN(v)) {{
            started = false;
            continue;
          }}
          const x = px(i), y = py(v);
          if (!started) {{ ctx.moveTo(x,y); started = true; }}
          else {{ ctx.lineTo(x,y); }}
        }}
        ctx.stroke();
      }}

      const cx = px(Math.max(0, Math.min(cursorIndex, xs)));
      ctx.strokeStyle = "#9aa8b8";
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(cx, pad); ctx.lineTo(cx, h-pad); ctx.stroke();

      ctx.font = "11px IBM Plex Sans, Segoe UI, sans-serif";
      let lx = pad + 8;
      for (const s of series) {{
        ctx.fillStyle = s.color;
        ctx.fillRect(lx, 8, 10, 10);
        ctx.fillStyle = "#33485f";
        ctx.fillText(s.name, lx + 14, 17);
        lx += 14 + ctx.measureText(s.name).width + 16;
      }}
    }}

    function drawBarChart(canvasId, pairs) {{
      const canvas = document.getElementById(canvasId);
      const ctx = canvas.getContext("2d");
      const w = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0,0,w,h);
      const pad = 34;
      const maxV = Math.max(1, ...pairs.map(p=>p[1]));
      const barW = (w - 2*pad) / Math.max(1, pairs.length);
      ctx.strokeStyle = "#d7e1ea";
      ctx.beginPath(); ctx.moveTo(pad, h-pad); ctx.lineTo(w-pad, h-pad); ctx.stroke();
      ctx.font = "10px IBM Plex Sans, Segoe UI, sans-serif";
      for (let i=0;i<pairs.length;i++) {{
        const [k,v] = pairs[i];
        const x = pad + i*barW + 3;
        const bh = (h - 2*pad) * (v / maxV);
        const y = h - pad - bh;
        ctx.fillStyle = "#4c78a8";
        ctx.fillRect(x, y, Math.max(8, barW - 6), bh);
        ctx.fillStyle = "#35506a";
        ctx.save();
        ctx.translate(x + 2, h - pad + 10);
        ctx.rotate(-0.45);
        ctx.fillText(k, 0, 0);
        ctx.restore();
      }}
    }}

    function renderAt(idx) {{
      const i = Math.max(0, Math.min(idx, timeline.length - 1));
      const s = timeline[i] || {{}};
      stateIdx.textContent = String(i);
      stateTs.textContent = s.timestamp || "";
      stateEvt.textContent = `event=${{s.event_type || ''}} run=${{s.run_key || ''}} agent=${{s.agent || ''}}`;
      stateDesc.textContent = s.description || "";

      drawLineChart("graphChart", [
        {{ name: "nodes", color: "#1f77b4", values: getSeries(t => (t.graph||{{}}).node_count ?? 0) }},
        {{ name: "edges", color: "#ff7f0e", values: getSeries(t => (t.graph||{{}}).edge_count ?? 0) }},
        {{ name: "density(x100)", color: "#2ca02c", values: getSeries(t => 100*((t.graph||{{}}).density ?? 0)) }},
      ], i);

      drawLineChart("opsChart", [
        {{ name: "stage_started", color: "#2a9d8f", values: getSeries(t => (((t.process||{{}}).cumulative_operation_counts||{{}}).stage_started ?? 0)) }},
        {{ name: "stage_completed", color: "#3a86ff", values: getSeries(t => (((t.process||{{}}).cumulative_operation_counts||{{}}).stage_completed ?? 0)) }},
        {{ name: "declared_output", color: "#8338ec", values: getSeries(t => (((t.process||{{}}).cumulative_operation_counts||{{}}).declared_output ?? 0)) }},
        {{ name: "invokes_agent", color: "#ef476f", values: getSeries(t => (((t.process||{{}}).cumulative_operation_counts||{{}}).invokes_agent ?? 0)) }},
      ], i);

      drawLineChart("conceptChart", [
        {{ name: "concept_nodes", color: "#118ab2", values: getSeries(t => ((t.concept||{{}}).concept_graph_nodes ?? null)) }},
        {{ name: "concept_relations", color: "#06d6a0", values: getSeries(t => ((t.concept||{{}}).concept_graph_relations ?? null)) }},
        {{ name: "hypothesis_total", color: "#f4a261", values: getSeries(t => ((t.concept||{{}}).hypothesis_total ?? null)) }},
        {{ name: "coherence(x100)", color: "#e63946", values: getSeries(t => (t.concept && t.concept.coherence_global != null ? 100*t.concept.coherence_global : null)) }},
        {{ name: "topology_index(x100)", color: "#264653", values: getSeries(t => (t.concept && t.concept.concept_topology_index != null ? 100*t.concept.concept_topology_index : null)) }},
      ], i);

      const evt = Object.entries((summary.process_distribution || {{}}).event_type_counts || {{}}).sort((a,b)=>b[1]-a[1]).slice(0,10);
      drawBarChart("eventChart", evt);
    }}

    let timer = null;
    function stop() {{
      if (timer) clearInterval(timer);
      timer = null;
      playBtn.textContent = "Play";
    }}
    function play() {{
      if (timer) {{ stop(); return; }}
      playBtn.textContent = "Pause";
      timer = setInterval(() => {{
        const next = Math.min(timeline.length - 1, Number(range.value) + 1);
        range.value = String(next);
        renderAt(next);
        if (next >= timeline.length - 1) stop();
      }}, 500);
    }}

    range.addEventListener("input", () => renderAt(Number(range.value)));
    playBtn.addEventListener("click", play);
    prevBtn.addEventListener("click", () => {{
      const v = Math.max(0, Number(range.value) - 1);
      range.value = String(v);
      renderAt(v);
    }});
    nextBtn.addEventListener("click", () => {{
      const v = Math.min(timeline.length - 1, Number(range.value) + 1);
      range.value = String(v);
      renderAt(v);
    }});

    drawKPI();
    renderAt(Number(range.value));
  </script>
</body>
</html>
"""


def main() -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-reasoning-dynamics")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Artifacts directory for a target KB.")
    ap.add_argument("--process-graph-evolution", default="", help="Optional explicit process-graph-evolution.json path.")
    ap.add_argument("--output-json", default="")
    ap.add_argument("--output-md", default="")
    ap.add_argument("--output-html", default="")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()
    evolution_path = (
        Path(args.process_graph_evolution)
        if args.process_graph_evolution
        else artifacts_dir / "process-graph-evolution.json"
    )
    if not evolution_path.is_absolute():
        evolution_path = (repo_root / evolution_path).resolve()

    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "reasoning-dynamics.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "reasoning-dynamics.md"
    output_html = Path(args.output_html) if args.output_html else artifacts_dir / "reasoning-dynamics.html"

    logger.step(
        "Parsed reasoning-dynamics arguments",
        "\n".join(
            [
                f"artifacts_dir={artifacts_dir}",
                f"process_graph_evolution={evolution_path}",
                f"output_json={output_json}",
                f"output_md={output_md}",
                f"output_html={output_html}",
            ]
        ),
    )

    if not artifacts_dir.exists():
        log_path = logger.finalize("error", summary=f"Artifacts directory not found: {artifacts_dir}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Artifacts directory not found: {artifacts_dir}")
    if not evolution_path.exists():
        log_path = logger.finalize("error", summary=f"Missing process graph evolution file: {evolution_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing process graph evolution file: {evolution_path}")

    evolution = _load_json(evolution_path)
    report = _build_dynamics(evolution=evolution, artifact_root=repo_root)
    report["metadata"] = {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "artifacts_dir": str(artifacts_dir),
        "process_graph_evolution": str(evolution_path),
    }
    logger.step(
        "Computed reasoning dynamics",
        "\n".join(
            [
                f"states={report.get('summary', {}).get('state_count', 0)}",
                f"time_span_seconds={report.get('summary', {}).get('time_span_seconds', 0.0)}",
                f"concept_updates={report.get('summary', {}).get('concept_evolution', {}).get('update_count', 0)}",
            ]
        ),
    )

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_html.parent.mkdir(parents=True, exist_ok=True)

    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(_to_markdown(report), encoding="utf-8")
    output_html.write_text(_render_html(report), encoding="utf-8")

    print(f"[OK] Wrote reasoning dynamics JSON: {output_json}")
    print(f"[OK] Wrote reasoning dynamics Markdown: {output_md}")
    print(f"[OK] Wrote reasoning dynamics HTML: {output_html}")

    logger.add_output("reasoning_dynamics_json", output_json)
    logger.add_output("reasoning_dynamics_md", output_md)
    logger.add_output("reasoning_dynamics_html", output_html)
    log_path = logger.finalize(
        "success",
        summary=f"Generated reasoning dynamics artifacts for {report.get('summary', {}).get('state_count', 0)} states.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
