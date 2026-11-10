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

"""Generate requirement-driven compliance report for the control plane."""

from __future__ import annotations

from agentic_common import ROOT, kb_ref_from_path, load_json_array, load_json_object, repo_path


def main() -> int:
    target_path = ROOT / "agentic" / "state" / "current_target.json"
    todos_path = ROOT / "agentic" / "todos" / "looper_integration_todos.yaml"
    target = load_json_object(target_path)
    kb_ref = kb_ref_from_path(repo_path(target["kb_path"], must_exist=True))
    graph_path = ROOT / "agentic" / "state" / "dependency_graphs" / f"{kb_ref}.json"
    graph = load_json_object(graph_path)
    todos = load_json_array(todos_path)
    blocking_gates = [gate for gate in target["acceptance_gates"] if gate.get("blocks_release")]
    open_frontier = [row for row in graph["frontier"] if row["status"] not in {"grounded", "accepted-local", "refuted"}]
    in_progress_todos = [row for row in todos if row["status"] in {"open", "in_progress", "blocked"}]
    lines = [
        "# Looper Compliance Report",
        "",
        f"- Target: `{target['target_id']}`",
        f"- Blocking acceptance gates: {len(blocking_gates)}",
        f"- Dependency nodes: {graph['summary']['node_count']}",
        f"- Open dependency frontier: {len(open_frontier)}",
        f"- Active TODO cards: {len(in_progress_todos)}",
        "",
        "## Gate Evidence",
        "",
    ]
    for gate in blocking_gates:
        lines.append(f"- `{gate['gate_id']}`: requires {', '.join(gate['required_evidence'])}")
    lines.extend(["", "## Frontier Health", ""])
    status_counts = graph["summary"]["status_counts"]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "## Compliance Decision", ""])
    if blocking_gates and graph["frontier"]:
        lines.append("warn: control-plane evidence is present, but the mathematical target still has open proof/dependency frontier nodes.")
    else:
        lines.append("pass: no blocking control-plane evidence gaps detected.")
    out = ROOT / "agentic" / "reports" / "compliance" / "latest.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
