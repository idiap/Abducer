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
"""Build a holistic relational-coherence report for the ERFL flow bundle."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentic.orchestration.reasoning_flow_language import parse_file, validate_relational_coherence

ROOT = Path(__file__).resolve().parents[2]
FLOW_ROOT = ROOT / "agentic/reasoning_flows"
PROJECTIONS = ROOT / "agentic/state/reasoning_type_workflow_projections.json"
OUTPUT = ROOT / "agentic/state/reasoning_flow_coherence.json"


def strongly_connected(graph: dict[str, set[str]]) -> list[list[str]]:
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indexes: dict[str, int] = {}
    low: dict[str, int] = {}
    components: list[list[str]] = []

    def visit(node: str) -> None:
        nonlocal index
        indexes[node] = low[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for target in graph.get(node, set()):
            if target not in indexes:
                visit(target)
                low[node] = min(low[node], low[target])
            elif target in on_stack:
                low[node] = min(low[node], indexes[target])
        if low[node] == indexes[node]:
            component: list[str] = []
            while True:
                value = stack.pop()
                on_stack.remove(value)
                component.append(value)
                if value == node:
                    break
            if len(component) > 1 or node in graph.get(node, set()):
                components.append(sorted(component))

    for node in sorted(graph):
        if node not in indexes:
            visit(node)
    return sorted(components)


def build() -> dict:
    paths = sorted(FLOW_ROOT.glob("*.prism"))
    known = {path.stem for path in paths}
    flows = [parse_file(path, known_workflows=known) for path in paths]
    graph = {flow["id"]: set() for flow in flows}
    local: list[dict] = []
    for flow in flows:
        checks = validate_relational_coherence(flow)
        targets = [
            row["action"][8:]
            for row in flow["handlers"]
            if row["action"].startswith("switch @")
        ]
        graph[flow["id"]].update(targets)
        local.append({
            "flow_id": flow["id"],
            "version": flow["version"],
            "relations_checked": len(checks),
            "unknown_gap_relations": sum(row["coherence"] == "unknown_gap" for row in checks),
            "switch_targets": targets,
            "local_status": "unknown" if any(row["coherence"] == "unknown_gap" for row in checks) else "coherent_hypothesis",
        })
    cycles = strongly_connected(graph)
    source = json.loads(PROJECTIONS.read_text(encoding="utf-8"))
    degraded = [row["workflow_id"] for row in source["workflows"] if row["projection_status"] != "complete"]
    blockers = []
    if degraded:
        blockers.append("source_projection_incomplete")
    if cycles:
        blockers.append("global_switch_cycles_lack_shared_budget_or_well_founded_progress_rank")
    if any(row["unknown_gap_relations"] for row in local):
        blockers.append("unresolved_reasoning_type_gaps")
    return {
        "schema_version": "0.2",
        "language": "ERFL",
        "relational_coherence": "unknown" if blockers else "validated",
        "executable": not blockers,
        "state_conservation": ["claim_identity", "scope", "provenance", "taints", "claim_ceiling", "open_obligations"],
        "local_flows": local,
        "switch_graph": {key: sorted(value) for key, value in sorted(graph.items())},
        "unbounded_switch_cycles": cycles,
        "global_switch_budget": None,
        "blockers": blockers,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--require-executable", action="store_true")
    args = parser.parse_args()
    payload = build()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.write:
        OUTPUT.write_text(rendered, encoding="utf-8")
    elif not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != rendered:
        raise SystemExit("stale reasoning-flow coherence report; run with --write")
    if args.require_executable and not payload["executable"]:
        raise SystemExit("reasoning-flow bundle is not executable: " + ", ".join(payload["blockers"]))
    print(json.dumps({"relational_coherence": payload["relational_coherence"], "blockers": payload["blockers"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
