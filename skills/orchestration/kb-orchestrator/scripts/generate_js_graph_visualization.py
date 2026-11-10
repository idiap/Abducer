#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Generate a standalone JavaScript-based graph visualization from KB artifacts."""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import canonical_artifacts_dir
from kb_context import resolve_kb_reference
from reasoning_log import ReasoningLogger


def _load_json(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream graph assembly stays auditable.
    """

    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _node_label(node: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable label normalization for heterogeneous node payloads.
    Contribution: Makes graph nodes interpretable across mixed artifact schemas.
    """

    for key in ("label", "statement_id", "name", "id"):
        value = str(node.get(key, "")).strip()
        if value:
            return value
    return "node"


def _ensure_node(
    node_id: str,
    nodes: dict[str, dict[str, Any]],
    *,
    node_type: str = "unknown",
    label: str | None = None,
    origin: str = "derived",
    meta: dict[str, Any] | None = None,
) -> None:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Idempotent graph-node materialization utility.
    Contribution: Prevents duplicate or inconsistent node records when merging multiple artifact sources.
    """

    node_key = str(node_id).strip()
    if not node_key:
        return
    if node_key not in nodes:
        nodes[node_key] = {
            "id": node_key,
            "label": (label.strip() if isinstance(label, str) else "") or node_key,
            "type": node_type or "unknown",
            "origin": origin,
            "meta": meta or {},
        }
        return
    if label and not str(nodes[node_key].get("label", "")).strip():
        nodes[node_key]["label"] = label
    if node_type and str(nodes[node_key].get("type", "")).strip() in {"", "unknown"}:
        nodes[node_key]["type"] = node_type
    if isinstance(meta, dict) and meta:
        base = nodes[node_key].get("meta", {})
        if not isinstance(base, dict):
            base = {}
        base.update(meta)
        nodes[node_key]["meta"] = base


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
    Contribution: Preserves relation typing and source provenance in the rendered graph.
    """

    src = str(source).strip()
    dst = str(target).strip()
    if not src or not dst:
        return
    edges.append(
        {
            "id": f"{origin}:{edge_type}:{src}->{dst}:{len(edges)}",
            "source": src,
            "target": dst,
            "type": str(edge_type).strip() or "related",
            "origin": str(origin).strip() or "derived",
            "weight": float(weight),
            "meta": meta or {},
        }
    )


def _build_graph(
    analysis: dict[str, Any],
    coherence: dict[str, Any],
    bridges: dict[str, Any],
    hardness: dict[str, Any],
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Multi-artifact typed graph fusion for visualization.
    Contribution: Produces a single inspectable conceptual network linking statements, concepts, barriers, bridges, and hardness signals.
    """

    random.seed(13)
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []

    concept_graph = analysis.get("concept_graph", {}) if isinstance(analysis.get("concept_graph"), dict) else {}
    for row in concept_graph.get("nodes", []) if isinstance(concept_graph.get("nodes"), list) else []:
        if not isinstance(row, dict):
            continue
        node_id = str(row.get("id", "")).strip()
        if not node_id:
            continue
        _ensure_node(
            node_id,
            nodes,
            node_type=str(row.get("type", "unknown")).strip() or "unknown",
            label=_node_label(row),
            origin="analysis",
            meta=row,
        )
    for row in concept_graph.get("relations", []) if isinstance(concept_graph.get("relations"), list) else []:
        if not isinstance(row, dict):
            continue
        src = str(row.get("from", "")).strip()
        dst = str(row.get("to", "")).strip()
        rel = str(row.get("relation", "related")).strip() or "related"
        _ensure_node(src, nodes, origin="analysis")
        _ensure_node(dst, nodes, origin="analysis")
        _add_edge(
            edges,
            source=src,
            target=dst,
            edge_type=rel,
            origin="analysis",
            weight=float(row.get("weight", 1.0) or 1.0),
            meta=row,
        )

    typed_coherence = coherence.get("typed_coherence_graph", {}) if isinstance(coherence.get("typed_coherence_graph"), dict) else {}
    for row in typed_coherence.get("nodes", []) if isinstance(typed_coherence.get("nodes"), list) else []:
        if not isinstance(row, dict):
            continue
        node_id = str(row.get("id", "")).strip()
        if not node_id:
            continue
        _ensure_node(
            node_id,
            nodes,
            node_type=str(row.get("type", "unknown")).strip() or "unknown",
            label=_node_label(row),
            origin="coherence",
            meta=row,
        )
    for row in typed_coherence.get("edges", []) if isinstance(typed_coherence.get("edges"), list) else []:
        if not isinstance(row, dict):
            continue
        src = str(row.get("from", "")).strip()
        dst = str(row.get("to", "")).strip()
        rel = str(row.get("relation", "related")).strip() or "related"
        _ensure_node(src, nodes, origin="coherence")
        _ensure_node(dst, nodes, origin="coherence")
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
            label=bridge_id,
            origin="bridge-plan",
            meta=row,
        )
        src = str(row.get("from_id", "")).strip()
        dst = str(row.get("to_id", "")).strip()
        if src:
            _ensure_node(src, nodes, origin="bridge-plan")
            _add_edge(
                edges,
                source=src,
                target=bridge_node,
                edge_type="bridge-source",
                origin="bridge-plan",
                weight=float(row.get("bridge_score", 1.0) or 1.0),
                meta={"bridge_type": row.get("bridge_type", "")},
            )
        if dst:
            _ensure_node(dst, nodes, origin="bridge-plan")
            _add_edge(
                edges,
                source=bridge_node,
                target=dst,
                edge_type="bridge-target",
                origin="bridge-plan",
                weight=float(row.get("bridge_score", 1.0) or 1.0),
                meta={"bridge_type": row.get("bridge_type", "")},
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
        )
        for sid in row.get("evidence_ids", []) if isinstance(row.get("evidence_ids"), list) else []:
            sid_s = str(sid).strip()
            if not sid_s:
                continue
            st_node = sid_s if sid_s.startswith("statement:") else f"statement:{sid_s}"
            _ensure_node(st_node, nodes, origin="hardness")
            _add_edge(
                edges,
                source=hid,
                target=st_node,
                edge_type="hardness-evidence",
                origin="hardness",
                weight=0.9,
                meta={"severity": row.get("severity", "")},
            )

    # Populate coordinates once so initial render is stable.
    node_list = list(nodes.values())
    for idx, node in enumerate(node_list):
        node["x"] = 150.0 * (random.random() - 0.5) + (idx % 8) * 20.0
        node["y"] = 150.0 * (random.random() - 0.5) + (idx // 8) * 20.0
        node["vx"] = 0.0
        node["vy"] = 0.0

    relation_counts: dict[str, int] = {}
    for edge in edges:
        et = str(edge.get("type", "related")).strip() or "related"
        relation_counts[et] = relation_counts.get(et, 0) + 1

    return {
        "metadata": {
            "node_count": len(node_list),
            "edge_count": len(edges),
            "relation_counts": relation_counts,
            "origins": sorted({str(node.get("origin", "")) for node in node_list if str(node.get("origin", "")).strip()}),
        },
        "nodes": node_list,
        "edges": edges,
    }


def _render_html(title: str, graph: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Self-contained HTML/JavaScript rendering for interactive graph exploration.
    Contribution: Produces a portable visualization artifact without external library dependencies.
    """

    graph_json = json.dumps(graph, ensure_ascii=False)
    title_safe = title.replace("<", "&lt;").replace(">", "&gt;")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title_safe}</title>
  <style>
    :root {{
      --bg: #f4f6f8;
      --panel: #ffffff;
      --ink: #20242b;
      --muted: #637082;
      --border: #d8dee7;
      --accent: #0f5aa6;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
      overflow: hidden;
    }}
    .app {{
      display: grid;
      grid-template-columns: 320px 1fr;
      height: 100vh;
    }}
    .panel {{
      background: var(--panel);
      border-right: 1px solid var(--border);
      padding: 14px 14px 18px;
      overflow: auto;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 18px;
      line-height: 1.3;
      color: var(--accent);
    }}
    .meta {{
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 10px;
      line-height: 1.4;
    }}
    .block {{
      border: 1px solid var(--border);
      border-radius: 8px;
      margin-bottom: 10px;
      padding: 8px;
      background: #fbfcfe;
    }}
    .block h2 {{
      margin: 0 0 6px;
      font-size: 13px;
      color: #384555;
    }}
    .search {{
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 7px 8px;
      font-size: 13px;
      margin-bottom: 8px;
    }}
    .row {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      margin: 4px 0;
    }}
    .legend-dot {{
      width: 10px;
      height: 10px;
      border-radius: 999px;
      border: 1px solid #ffffff;
      box-shadow: 0 0 0 1px rgba(0,0,0,0.12);
      flex: 0 0 auto;
    }}
    .small {{
      font-size: 11px;
      color: var(--muted);
    }}
    .mono {{
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 11px;
      white-space: pre-wrap;
      max-height: 180px;
      overflow: auto;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 6px;
      background: #fff;
    }}
    #viewport {{
      position: relative;
      overflow: hidden;
      background:
        radial-gradient(circle at 15% 20%, rgba(15,90,166,0.07), transparent 35%),
        radial-gradient(circle at 80% 80%, rgba(31,142,112,0.08), transparent 40%),
        linear-gradient(150deg, #f7f9fb 0%, #eef2f7 100%);
    }}
    canvas {{
      width: 100%;
      height: 100%;
      display: block;
      cursor: grab;
    }}
    .topbar {{
      position: absolute;
      top: 10px;
      right: 12px;
      background: rgba(255,255,255,0.86);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 8px 10px;
      font-size: 11px;
      color: #415063;
      backdrop-filter: blur(3px);
    }}
    .tooltip {{
      position: absolute;
      max-width: 360px;
      pointer-events: none;
      background: rgba(18, 25, 35, 0.94);
      color: #eff4fb;
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 8px;
      padding: 8px 10px;
      font-size: 11px;
      line-height: 1.35;
      box-shadow: 0 10px 28px rgba(10, 20, 36, 0.34);
      z-index: 5;
    }}
    .tooltip.hidden {{
      display: none;
    }}
    .tooltip .label {{
      font-weight: 600;
      margin-bottom: 4px;
      color: #ffffff;
    }}
    .tooltip .meta-row {{
      color: #d2dcec;
      margin-top: 2px;
      overflow-wrap: anywhere;
    }}
    .tooltip .meta-key {{
      color: #8ec7ff;
    }}
  </style>
</head>
<body>
  <div class="app">
    <aside class="panel">
      <h1>{title_safe}</h1>
      <div class="meta" id="meta"></div>

      <div class="block">
        <h2>Search</h2>
        <input id="search" class="search" placeholder="Filter nodes by id/label/type..." />
        <label class="row"><input id="showLabels" type="checkbox" checked /> show labels</label>
      </div>

      <div class="block">
        <h2>Node Types</h2>
        <div id="nodeTypeFilters"></div>
      </div>

      <div class="block">
        <h2>Edge Types</h2>
        <div id="edgeTypeFilters"></div>
      </div>

      <div class="block">
        <h2>Origins</h2>
        <div id="originFilters"></div>
      </div>

      <div class="block">
        <h2>Selected Node</h2>
        <div id="selected" class="small">Click a node to inspect details.</div>
      </div>

      <div class="small">
        Drag nodes to reposition. Drag empty space to pan. Use wheel to zoom.
      </div>
    </aside>

    <main id="viewport">
      <canvas id="graph"></canvas>
      <div class="topbar" id="stats"></div>
      <div class="tooltip hidden" id="tooltip"></div>
    </main>
  </div>

  <script>
    const DATA = {graph_json};
    const canvas = document.getElementById("graph");
    const ctx = canvas.getContext("2d");
    const viewport = document.getElementById("viewport");
    const statsEl = document.getElementById("stats");
    const selectedEl = document.getElementById("selected");
    const metaEl = document.getElementById("meta");
    const nodes = DATA.nodes.map((n) => ({{ ...n }}));
    const nodeById = new Map(nodes.map((n) => [n.id, n]));
    const edges = DATA.edges.map((e) => ({{ ...e }}));
    const tooltipEl = document.getElementById("tooltip");

    const uniqueNodeTypes = [...new Set(nodes.map((n) => n.type || "unknown"))].sort();
    const uniqueEdgeTypes = [...new Set(edges.map((e) => e.type || "related"))].sort();
    const uniqueOrigins = [...new Set([
      ...nodes.map((n) => n.origin || "derived"),
      ...edges.map((e) => e.origin || "derived")
    ])].sort();

    const nodeTypeEnabled = new Set(uniqueNodeTypes);
    const edgeTypeEnabled = new Set(uniqueEdgeTypes);
    const originEnabled = new Set(uniqueOrigins);
    let searchTerm = "";
    let showLabels = true;

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

    function hashColor(text, sat = 68, light = 48) {{
      let h = 0;
      const t = String(text || "x");
      for (let i = 0; i < t.length; i++) h = ((h << 5) - h) + t.charCodeAt(i);
      h = Math.abs(h) % 360;
      return `hsl(${{h}} ${{sat}}% ${{light}}%)`;
    }}

    function setCanvasSize() {{
      const rect = viewport.getBoundingClientRect();
      width = Math.max(1, rect.width);
      height = Math.max(1, rect.height);
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
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

    function escapeHtml(value) {{
      return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
    }}

    function valuePreview(value) {{
      if (value === null || value === undefined) return "null";
      if (typeof value === "string") return value;
      const text = JSON.stringify(value);
      if (!text) return "";
      return text.length > 140 ? `${{text.slice(0, 137)}}...` : text;
    }}

    function metaRowsHtml(meta, maxItems = 6) {{
      if (!meta || typeof meta !== "object") return "";
      const entries = Object.entries(meta).filter(([k, v]) =>
        String(k || "").trim() && valuePreview(v).trim()
      );
      if (!entries.length) return "";
      const sliced = entries.slice(0, maxItems);
      const rows = sliced.map(([key, val]) =>
        `<div class="meta-row"><span class="meta-key">${{escapeHtml(key)}}:</span> ${{escapeHtml(valuePreview(val))}}</div>`
      );
      if (entries.length > maxItems) {{
        rows.push(`<div class="meta-row">… +${{entries.length - maxItems}} more fields</div>`);
      }}
      return rows.join("");
    }}

    function showTooltip(px, py, html) {{
      tooltipEl.innerHTML = html;
      tooltipEl.classList.remove("hidden");
      const pad = 14;
      const rect = viewport.getBoundingClientRect();
      let left = px + pad;
      let top = py + pad;
      if (left > rect.width - 380) left = px - 360;
      if (left < 8) left = 8;
      if (top > rect.height - 180) top = py - 130;
      if (top < 8) top = 8;
      tooltipEl.style.left = `${{left}}px`;
      tooltipEl.style.top = `${{top}}px`;
    }}

    function hideTooltip() {{
      tooltipEl.classList.add("hidden");
      tooltipEl.innerHTML = "";
    }}

    function isNodeVisible(node) {{
      if (!nodeTypeEnabled.has(node.type || "unknown")) return false;
      if (!originEnabled.has(node.origin || "derived")) return false;
      if (!searchTerm) return true;
      const blob = `${{node.id}} ${{node.label || ""}} ${{node.type || ""}}`.toLowerCase();
      return blob.includes(searchTerm);
    }}

    function visibleGraph() {{
      const visibleNodes = nodes.filter(isNodeVisible);
      const idSet = new Set(visibleNodes.map((n) => n.id));
      const visibleEdges = edges.filter((e) => {{
        if (!edgeTypeEnabled.has(e.type || "related")) return false;
        if (!originEnabled.has(e.origin || "derived")) return false;
        return idSet.has(e.source) && idSet.has(e.target);
      }});
      return {{ visibleNodes, visibleEdges, idSet }};
    }}

    function buildCheckboxes(containerId, items, enabledSet, colorBy) {{
      const root = document.getElementById(containerId);
      root.innerHTML = "";
      for (const item of items) {{
        const row = document.createElement("label");
        row.className = "row";
        const cb = document.createElement("input");
        cb.type = "checkbox";
        cb.checked = enabledSet.has(item);
        cb.addEventListener("change", () => {{
          if (cb.checked) enabledSet.add(item);
          else enabledSet.delete(item);
          updateHover(lastX, lastY);
        }});
        const dot = document.createElement("span");
        dot.className = "legend-dot";
        dot.style.background = colorBy(item);
        const txt = document.createElement("span");
        txt.textContent = item;
        row.appendChild(cb);
        row.appendChild(dot);
        row.appendChild(txt);
        root.appendChild(row);
      }}
    }}

    function pickNode(px, py) {{
      const world = toWorld(px, py);
      let best = null;
      let bestDist = Infinity;
      for (const node of nodes) {{
        if (!isNodeVisible(node)) continue;
        const dx = node.x - world.x;
        const dy = node.y - world.y;
        const d2 = dx * dx + dy * dy;
        if (d2 < bestDist && d2 < 14 * 14 / (scale * scale)) {{
          bestDist = d2;
          best = node;
        }}
      }}
      return best;
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

    function pickEdge(px, py) {{
      const {{ visibleEdges }} = visibleGraph();
      let best = null;
      let bestDist = Infinity;
      for (const edge of visibleEdges) {{
        const source = nodeById.get(edge.source);
        const target = nodeById.get(edge.target);
        if (!source || !target) continue;
        const a = toScreen(source.x, source.y);
        const b = toScreen(target.x, target.y);
        const dist = pointSegmentDistance(px, py, a.x, a.y, b.x, b.y);
        if (dist < bestDist && dist <= 7.5) {{
          bestDist = dist;
          best = edge;
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
        const html = [
          `<div class="label">${{escapeHtml(node.label || node.id)}}</div>`,
          `<div class="meta-row"><span class="meta-key">id:</span> ${{escapeHtml(node.id)}}</div>`,
          `<div class="meta-row"><span class="meta-key">type:</span> ${{escapeHtml(node.type || "unknown")}}</div>`,
          `<div class="meta-row"><span class="meta-key">origin:</span> ${{escapeHtml(node.origin || "derived")}}</div>`,
          metaRowsHtml(node.meta, 5),
        ].join("");
        showTooltip(px, py, html);
        return;
      }}

      const edge = pickEdge(px, py);
      if (edge) {{
        hoveredNode = null;
        hoveredEdge = edge;
        const html = [
          `<div class="label">${{escapeHtml(edge.type || "related")}}</div>`,
          `<div class="meta-row"><span class="meta-key">source:</span> ${{escapeHtml(edge.source)}}</div>`,
          `<div class="meta-row"><span class="meta-key">target:</span> ${{escapeHtml(edge.target)}}</div>`,
          `<div class="meta-row"><span class="meta-key">origin:</span> ${{escapeHtml(edge.origin || "derived")}}</div>`,
          `<div class="meta-row"><span class="meta-key">weight:</span> ${{escapeHtml(Number(edge.weight || 0).toFixed(3))}}</div>`,
          metaRowsHtml(edge.meta, 4),
        ].join("");
        showTooltip(px, py, html);
        return;
      }}

      hoveredNode = null;
      hoveredEdge = null;
      hideTooltip();
    }}

    function simulate() {{
      const {{ visibleNodes, visibleEdges }} = visibleGraph();
      const repel = 3200;
      const springK = 0.02;
      const springLen = 48;
      const centerK = 0.0008;
      const damping = 0.86;

      for (let i = 0; i < visibleNodes.length; i++) {{
        const a = visibleNodes[i];
        for (let j = i + 1; j < visibleNodes.length; j++) {{
          const b = visibleNodes[j];
          let dx = a.x - b.x;
          let dy = a.y - b.y;
          let d2 = dx * dx + dy * dy;
          if (d2 < 0.01) {{
            dx = (Math.random() - 0.5) * 0.3;
            dy = (Math.random() - 0.5) * 0.3;
            d2 = dx * dx + dy * dy;
          }}
          const f = repel / d2;
          const fx = f * dx;
          const fy = f * dy;
          a.vx += fx;
          a.vy += fy;
          b.vx -= fx;
          b.vy -= fy;
        }}
      }}

      for (const e of visibleEdges) {{
        const a = nodeById.get(e.source);
        const b = nodeById.get(e.target);
        if (!a || !b) continue;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const dist = Math.sqrt(dx * dx + dy * dy) || 1;
        const rest = springLen + (1.0 - Math.min(1, Number(e.weight || 1))) * 24;
        const force = springK * (dist - rest);
        const fx = force * (dx / dist);
        const fy = force * (dy / dist);
        a.vx += fx;
        a.vy += fy;
        b.vx -= fx;
        b.vy -= fy;
      }}

      for (const n of visibleNodes) {{
        if (draggingNode && draggingNode.id === n.id) {{
          n.vx = 0;
          n.vy = 0;
          continue;
        }}
        n.vx += -n.x * centerK;
        n.vy += -n.y * centerK;
        n.vx *= damping;
        n.vy *= damping;
        n.x += n.vx * 0.06;
        n.y += n.vy * 0.06;
      }}
    }}

    function draw() {{
      ctx.clearRect(0, 0, width, height);
      const {{ visibleNodes, visibleEdges }} = visibleGraph();

      for (const e of visibleEdges) {{
        const a = nodeById.get(e.source);
        const b = nodeById.get(e.target);
        if (!a || !b) continue;
        const pa = toScreen(a.x, a.y);
        const pb = toScreen(b.x, b.y);
        const isHovered = hoveredEdge && hoveredEdge.id === e.id;
        ctx.beginPath();
        ctx.moveTo(pa.x, pa.y);
        ctx.lineTo(pb.x, pb.y);
        ctx.strokeStyle = isHovered ? "#0f5aa6" : hashColor(e.type || "related", 52, 40);
        ctx.globalAlpha = isHovered ? 0.8 : 0.28;
        ctx.lineWidth = (isHovered ? 2.4 : 1) + Math.min(2.5, Number(e.weight || 1) * 1.2);
        ctx.stroke();
      }}
      ctx.globalAlpha = 1;

      for (const n of visibleNodes) {{
        const p = toScreen(n.x, n.y);
        const isSelected = n.id === (selectedNode && selectedNode.id);
        const isHovered = n.id === (hoveredNode && hoveredNode.id);
        const r = isSelected ? 7.8 : (isHovered ? 6.8 : 5.5);
        ctx.beginPath();
        ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
        ctx.fillStyle = hashColor(n.type || "unknown");
        ctx.fill();
        ctx.strokeStyle = isHovered ? "#0f5aa6" : "#ffffff";
        ctx.lineWidth = isHovered ? 2.0 : 1.4;
        ctx.stroke();
      }}

      if (showLabels) {{
        ctx.font = "11px IBM Plex Sans, Segoe UI, sans-serif";
        ctx.fillStyle = "#243041";
        for (const n of visibleNodes) {{
          const p = toScreen(n.x, n.y);
          const label = String(n.label || n.id);
          ctx.fillText(label, p.x + 8, p.y - 7);
        }}
      }}

      statsEl.textContent =
        `nodes: ${{visibleNodes.length}} / ${{nodes.length}} | edges: ${{visibleEdges.length}} / ${{edges.length}} | zoom: ${{scale.toFixed(2)}}x`;
    }}

    function frame() {{
      simulate();
      draw();
      requestAnimationFrame(frame);
    }}

    function updateSelectedPanel(node) {{
      if (!node) {{
        selectedEl.textContent = "Click a node to inspect details.";
        return;
      }}
      const payload = {{
        id: node.id,
        label: node.label,
        type: node.type,
        origin: node.origin,
        meta: node.meta || {{}},
      }};
      selectedEl.innerHTML = `<div class="mono">${{JSON.stringify(payload, null, 2)}}</div>`;
    }}

    canvas.addEventListener("mousedown", (ev) => {{
      const rect = canvas.getBoundingClientRect();
      const x = ev.clientX - rect.left;
      const y = ev.clientY - rect.top;
      lastX = x;
      lastY = y;
      const hit = pickNode(x, y);
      if (hit) {{
        draggingNode = hit;
        selectedNode = hit;
        updateSelectedPanel(hit);
        canvas.style.cursor = "grabbing";
      }} else {{
        draggingPan = true;
        canvas.style.cursor = "grabbing";
      }}
      updateHover(x, y);
    }});

    window.addEventListener("mousemove", (ev) => {{
      const rect = canvas.getBoundingClientRect();
      const x = ev.clientX - rect.left;
      const y = ev.clientY - rect.top;
      const dx = x - lastX;
      const dy = y - lastY;
      lastX = x;
      lastY = y;
      if (draggingNode) {{
        const w = toWorld(x, y);
        draggingNode.x = w.x;
        draggingNode.y = w.y;
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

    canvas.addEventListener("wheel", (ev) => {{
      ev.preventDefault();
      const rect = canvas.getBoundingClientRect();
      const x = ev.clientX - rect.left;
      const y = ev.clientY - rect.top;
      const before = toWorld(x, y);
      const factor = ev.deltaY < 0 ? 1.10 : 0.91;
      scale = Math.max(0.15, Math.min(4.2, scale * factor));
      const after = toScreen(before.x, before.y);
      offsetX += x - after.x;
      offsetY += y - after.y;
      updateHover(x, y);
    }}, {{ passive: false }});

    document.getElementById("search").addEventListener("input", (ev) => {{
      searchTerm = String(ev.target.value || "").trim().toLowerCase();
      updateHover(lastX, lastY);
    }});
    document.getElementById("showLabels").addEventListener("change", (ev) => {{
      showLabels = !!ev.target.checked;
      updateHover(lastX, lastY);
    }});

    buildCheckboxes("nodeTypeFilters", uniqueNodeTypes, nodeTypeEnabled, (x) => hashColor(x));
    buildCheckboxes("edgeTypeFilters", uniqueEdgeTypes, edgeTypeEnabled, (x) => hashColor(x, 52, 40));
    buildCheckboxes("originFilters", uniqueOrigins, originEnabled, (x) => hashColor(x, 46, 46));

    metaEl.textContent =
      `Total nodes: ${{nodes.length}} | total edges: ${{edges.length}} | relation types: ${{uniqueEdgeTypes.length}}`;

    setCanvasSize();
    offsetX = width * 0.52;
    offsetY = height * 0.52;
    window.addEventListener("resize", setCanvasSize);
    frame();
  </script>
</body>
</html>
"""


def main() -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds artifact loading, graph fusion, and HTML emission into a reproducible visualization stage.
    """

    logger = ReasoningLogger("kb-js-graph-visualizer")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb", required=True, help="Path to KB markdown file.")
    ap.add_argument("--kb-ref", default="", help="Optional canonical KB reference.")
    ap.add_argument("--artifacts-dir", default="", help="Optional explicit artifacts directory.")
    ap.add_argument("--analysis", default="", help="Optional connection-analysis JSON path.")
    ap.add_argument("--coherence", default="", help="Optional coherence-report JSON path.")
    ap.add_argument("--bridges", default="", help="Optional bridge-plan JSON path.")
    ap.add_argument("--hardness", default="", help="Optional epistemic-hardness JSON path.")
    ap.add_argument(
        "--title",
        default="",
        help="Visualization title. Default: KB Graph Visualization: <kb-ref>.",
    )
    ap.add_argument(
        "--output-html",
        default="",
        help="Output path (default: artifacts/<kb-ref>/kb-graph-visualization.html).",
    )
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
    coherence_path = Path(args.coherence) if args.coherence else artifacts_dir / "coherence-report.json"
    bridge_path = Path(args.bridges) if args.bridges else artifacts_dir / "bridge-plan.json"
    hardness_path = Path(args.hardness) if args.hardness else artifacts_dir / "epistemic-hardness.json"
    output_html = Path(args.output_html) if args.output_html else artifacts_dir / "kb-graph-visualization.html"
    title = str(args.title).strip() or f"KB Graph Visualization: {kb_ref}"

    logger.step(
        "Parsed JS graph-visualizer arguments",
        "\n".join(
            [
                f"kb={kb}",
                f"kb_ref={kb_ref}",
                f"artifacts_dir={artifacts_dir}",
                f"analysis={analysis_path}",
                f"coherence={coherence_path}",
                f"bridges={bridge_path}",
                f"hardness={hardness_path}",
                f"output_html={output_html}",
            ]
        ),
    )

    analysis = _load_json(analysis_path)
    coherence = _load_json(coherence_path)
    bridges = _load_json(bridge_path)
    hardness = _load_json(hardness_path)

    graph = _build_graph(analysis=analysis, coherence=coherence, bridges=bridges, hardness=hardness)
    html = _render_html(title=title, graph=graph)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(html, encoding="utf-8")

    logger.add_output("js_graph_visualization_html", output_html)
    logger.step(
        "Built JavaScript graph visualization",
        "\n".join(
            [
                f"nodes={graph.get('metadata', {}).get('node_count', 0)}",
                f"edges={graph.get('metadata', {}).get('edge_count', 0)}",
                f"relation_types={len((graph.get('metadata', {}).get('relation_counts', {}) or {}))}",
            ]
        ),
    )
    log_path = logger.finalize("success", summary=f"Wrote JavaScript graph visualization to {output_html}.")
    print(f"[OK] Wrote JavaScript graph visualization: {output_html}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
