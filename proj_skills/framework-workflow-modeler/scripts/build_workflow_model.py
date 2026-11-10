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
"""Build typed workflow topology while avoiding runtime claims."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

NODE_KINDS = {"workflow", "stage", "skill", "operator", "artifact", "state_store", "gate", "validator", "actor"}
EDGE_KINDS = {"contains", "invokes", "consumes", "produces", "validates", "gates", "hands_off_to", "persists_to", "feeds_back_to"}


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def input_digest(index: dict[str, Any]) -> str:
    value = str(index.get("digest", ""))
    return value if value.startswith("sha256:") and len(value) == 71 else digest(index)


def build(index: dict[str, Any]) -> dict[str, Any]:
    records = index.get("records", index.get("evidence", []))
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    warnings = []
    for record in records:
        evidence_id = str(record.get("id", record.get("evidence_id", "")))
        if not evidence_id:
            continue
        metadata = record.get("metadata", {})
        for raw in metadata.get("workflow_nodes", record.get("workflow_nodes", [])):
            kind = raw.get("kind")
            if kind not in NODE_KINDS:
                raise ValueError(f"unknown workflow node kind: {kind}")
            node_id = str(raw["id"])
            nodes[node_id] = {"node_id": node_id, "node_type": kind, "label": raw.get("label", node_id),
                              "evidence_ids": [evidence_id]}
        for raw in metadata.get("workflow_edges", record.get("workflow_edges", [])):
            kind = raw.get("kind")
            if kind not in EDGE_KINDS:
                raise ValueError(f"unknown workflow edge kind: {kind}")
            edges.append({"edge_id": raw.get("id", f"edge-{len(edges)+1}"), "edge_type": kind,
                          "source": str(raw["source"]), "target": str(raw["target"]),
                          "posture": raw.get("posture", "declared"), "evidence_ids": [evidence_id]})
    known = set(nodes)
    for edge in edges:
        if edge["source"] not in known or edge["target"] not in known:
            raise ValueError(f"workflow edge {edge['edge_id']} has an unknown endpoint")
    if not nodes:
        warnings.append("No explicit typed workflow nodes were present; topology remains unknown.")
    failure_paths = [str(raw.get("id", f"edge-{i+1}")) for record in records
                     for i, raw in enumerate(record.get("metadata", {}).get("workflow_edges", record.get("workflow_edges", [])))
                     if raw.get("failure_or_stop")]
    feedback_loops = [edge["edge_id"] for edge in edges if edge["edge_type"] == "feeds_back_to"]
    result = {"schema_version": "1.0.0", "model_id": "workflow-structure-model",
              "input_digest": input_digest(index),
              "nodes": [nodes[key] for key in sorted(nodes)],
              "edges": sorted(edges, key=lambda edge: str(edge["edge_id"])),
              "failure_paths": failure_paths + warnings, "feedback_loops": feedback_loops}
    result["model_digest"] = digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_index", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build(json.loads(args.evidence_index.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
