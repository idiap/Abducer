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
"""Validate qualitative mechanistic graph artifacts."""

from __future__ import annotations

import argparse
import contextlib
import io
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


SCHEMA = ROOT / "agentic/spec/qualitative_mechanistic_graph.schema.json"
DEFAULT_GRAPH = ROOT / "agentic/state/qualitative_mechanistic_graphs/yang-mills-existence-and-mass-gap-target.json"


def require_fields(item: dict[str, Any], fields: list[str], source: Path, subject: str) -> None:
    for field in fields:
        if field not in item:
            fail(f"{rel(source)} {subject} missing `{field}`")


def validate_graph(graph: dict[str, Any], source: Path, schema: dict[str, Any]) -> None:
    require_fields(graph, schema["required_fields"], source, "graph")
    allowed_nodes = set(schema["allowed_node_types"])
    allowed_edges = set(schema["allowed_edge_types"])
    allowed_status = set(schema["allowed_epistemic_status"])
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    if not isinstance(nodes, list) or len(nodes) < 5:
        fail(f"{rel(source)} graph needs at least five nodes")
    if not isinstance(edges, list) or len(edges) < 4:
        fail(f"{rel(source)} graph needs at least four edges")
    node_ids = set()
    for index, node in enumerate(nodes, start=1):
        if not isinstance(node, dict):
            fail(f"{rel(source)} node {index} must be an object")
        require_fields(node, schema["node_required_fields"], source, f"node {index}")
        node_ids.add(clean_text(node["id"]))
        if node.get("node_type") not in allowed_nodes:
            fail(f"{rel(source)} node {node.get('id')} invalid node_type")
        if node.get("epistemic_status") not in allowed_status:
            fail(f"{rel(source)} node {node.get('id')} invalid epistemic_status")
        if not node.get("evidence_paths"):
            fail(f"{rel(source)} node {node.get('id')} needs evidence_paths")
    statuses = set()
    for index, edge in enumerate(edges, start=1):
        if not isinstance(edge, dict):
            fail(f"{rel(source)} edge {index} must be an object")
        require_fields(edge, schema["edge_required_fields"], source, f"edge {index}")
        if edge.get("source") not in node_ids or edge.get("target") not in node_ids:
            fail(f"{rel(source)} edge {edge.get('id')} references missing node")
        if edge.get("edge_type") not in allowed_edges:
            fail(f"{rel(source)} edge {edge.get('id')} invalid edge_type")
        if edge.get("epistemic_status") not in allowed_status:
            fail(f"{rel(source)} edge {edge.get('id')} invalid epistemic_status")
        statuses.add(edge.get("epistemic_status"))
        for list_field in ["assumptions", "failure_modes", "evidence_paths", "originating_cycle_ids"]:
            if not isinstance(edge.get(list_field), list) or not edge[list_field]:
                fail(f"{rel(source)} edge {edge.get('id')} needs {list_field}")
        text = clean_text(edge).lower()
        if "proof achieved" in text or "proves the theorem" in text:
            fail(f"{rel(source)} edge {edge.get('id')} overclaims proof progress")
        if edge.get("gedanken_packet_ids"):
            if not isinstance(edge.get("gedanken_packet_ids"), list):
                fail(f"{rel(source)} edge {edge.get('id')} gedanken_packet_ids must be a list")
            if not edge.get("gedanken_transfer_scopes"):
                fail(f"{rel(source)} edge {edge.get('id')} has Gedanken packets without transfer scopes")
            for scope in edge.get("gedanken_transfer_scopes", []):
                for field in ["packet_id", "transfer_verdict", "transfers", "does_not_transfer", "transfer_certificate_needed"]:
                    if not clean_text(scope.get(field)):
                        fail(f"{rel(source)} edge {edge.get('id')} Gedanken scope missing {field}")
    if len(statuses) < 2:
        fail(f"{rel(source)} graph should preserve more than one epistemic status")
    for update in graph.get("updates", []):
        if update.get("action") not in schema["allowed_update_actions"]:
            fail(f"{rel(source)} update {update.get('id')} invalid action")
        if clean_text(update.get("packet_id")).startswith("gedanken.") and update.get("epistemic_status") != "conceptual_probe":
            fail(f"{rel(source)} Gedanken update {update.get('id')} must remain conceptual_probe")
    summary = graph.get("summary", {})
    if int(summary.get("node_count", 0)) != len(nodes) or int(summary.get("edge_count", 0)) != len(edges):
        fail(f"{rel(source)} summary counts do not match graph")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    schema = load_json_object(SCHEMA)
    paths = [ROOT / path if not Path(path).is_absolute() else Path(path) for path in args.paths]
    if not paths:
        if not DEFAULT_GRAPH.exists():
            print("No qualitative mechanistic graph yet; validator is idle.")
            return 0
        paths = [DEFAULT_GRAPH]
    for path in paths:
        validate_graph(load_json_object(path), path, schema)
    if not args.paths:
        fixtures = ROOT / "tests/fixtures/qualitative_physics"
        valid = fixtures / "valid_graph.json"
        invalid = fixtures / "invalid_graph_edge.json"
        if valid.exists():
            validate_graph(load_json_object(valid), valid, schema)
        if invalid.exists():
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    validate_graph(load_json_object(invalid), invalid, schema)
            except SystemExit:
                pass
            else:
                fail(f"{rel(invalid)} should fail qualitative graph validation")
    print(f"validated {len(paths)} qualitative mechanistic graph(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
