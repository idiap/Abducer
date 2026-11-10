#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Validate Abducer target dependency graphs."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel, repo_path


SCHEMA = ROOT / "agentic" / "spec" / "dependency_graph_schema.json"


def _require_object_list(graph: dict[str, Any], key: str, path: Path) -> list[dict[str, Any]]:
    value = graph.get(key)
    if not isinstance(value, list):
        fail(f"{rel(path)} missing list field: {key}")
    rows: list[dict[str, Any]] = []
    for row in value:
        if not isinstance(row, dict):
            fail(f"{rel(path)} {key} entries must be objects")
        rows.append(row)
    return rows


def validate_graph(path: Path) -> dict[str, Any]:
    schema = load_json_object(SCHEMA)
    graph = load_json_object(path)
    for field in schema["required_fields"]:
        if field not in graph:
            fail(f"{rel(path)} missing required field: {field}")
    repo_path(str(graph["kb_path"]), must_exist=True)
    nodes = _require_object_list(graph, "nodes", path)
    edges = _require_object_list(graph, "edges", path)
    node_ids: set[str] = set()
    for node in nodes:
        for field in schema["node_required_fields"]:
            if field not in node:
                fail(f"{rel(path)} node missing {field}: {node.get('id')}")
        node_id = clean_text(node.get("id"))
        if not node_id or node_id in node_ids:
            fail(f"{rel(path)} missing or duplicate node id: {node_id}")
        node_ids.add(node_id)
        if node["status"] not in schema["allowed_node_status"]:
            fail(f"{rel(path)} node {node_id} has unknown status: {node['status']}")
        if not isinstance(node.get("evidence_paths"), list):
            fail(f"{rel(path)} node {node_id} evidence_paths must be a list")
        if not isinstance(node.get("parents"), list):
            fail(f"{rel(path)} node {node_id} parents must be a list")
        open_node = node["status"] not in schema["terminal_status"]
        if open_node and not clean_text(node.get("next_action")) and not clean_text(node.get("blocker")):
            fail(f"{rel(path)} open node lacks next_action or blocker: {node_id}")
    for edge in edges:
        for field in schema["edge_required_fields"]:
            if field not in edge:
                fail(f"{rel(path)} edge missing {field}")
        if edge["from"] not in node_ids:
            fail(f"{rel(path)} edge has unknown source node: {edge['from']}")
        if edge["to"] not in node_ids:
            fail(f"{rel(path)} edge has unknown target node: {edge['to']}")
    frontier = _require_object_list(graph, "frontier", path)
    for row in frontier:
        if row.get("id") not in node_ids:
            fail(f"{rel(path)} frontier references unknown node: {row.get('id')}")
        if not clean_text(row.get("next_action")) and not clean_text(row.get("blocker")):
            fail(f"{rel(path)} frontier row lacks next_action or blocker: {row.get('id')}")
    summary = graph.get("summary")
    if not isinstance(summary, dict) or summary.get("node_count") != len(nodes):
        fail(f"{rel(path)} summary node_count does not match nodes")
    return {"path": rel(path), "nodes": len(nodes), "frontier": len(frontier)}


def discover_default_graphs() -> list[Path]:
    return sorted((ROOT / "agentic" / "state" / "dependency_graphs").glob("*.json"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graphs", nargs="*", help="Dependency graph JSON paths.")
    args = parser.parse_args()

    paths = [Path(raw) for raw in args.graphs] if args.graphs else discover_default_graphs()
    if not paths:
        fail("no dependency graphs found")
    for path in paths:
        row = validate_graph(path)
        print(f"validated dependency graph {row['path']} ({row['nodes']} nodes, {row['frontier']} frontier)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
