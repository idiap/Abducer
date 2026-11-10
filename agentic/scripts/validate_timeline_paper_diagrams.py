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
"""Validate generated timeline-paper diagrams."""

from __future__ import annotations

from agentic_common import fail, load_json_object, rel, repo_path
from build_timeline_paper_diagrams import OUT_JSON, OUT_TEX


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    require(OUT_JSON.exists(), f"missing {rel(OUT_JSON)}")
    report = load_json_object(OUT_JSON)
    require(report.get("status") == "timeline_paper_diagrams_ready", "diagram report not ready")
    diagrams = report.get("diagrams", [])
    require(isinstance(diagrams, list) and diagrams, "diagram report needs diagrams")
    for diagram in diagrams:
        nodes = diagram.get("nodes", [])
        edges = diagram.get("edges", [])
        require(len(nodes) >= 5, "diagram needs at least five nodes")
        require(len(edges) >= 5, "diagram needs at least five edges")
        node_ids = {node.get("node_id") for node in nodes if isinstance(node, dict)}
        for edge in edges:
            require(edge.get("source") in node_ids and edge.get("target") in node_ids, f"edge references unknown node: {edge}")
            require(edge.get("meaning"), "diagram edge needs conceptual meaning")
        require("tikzpicture" in diagram.get("tikz", ""), "diagram missing TikZ source")
        require("Validation handoff" in diagram.get("tikz", ""), "diagram must include validation handoff node")
    tex_path = repo_path(str(report.get("artifacts", {}).get("tex")), must_exist=True)
    require("tikzpicture" in tex_path.read_text(encoding="utf-8"), f"{rel(tex_path)} missing tikzpicture")
    print(f"validated {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
