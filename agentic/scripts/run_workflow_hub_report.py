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

"""Generate workflow hub graph and Markdown report."""

from __future__ import annotations

from agentic_common import ROOT, load_json_object, write_json


def main() -> int:
    nodes = []
    edges = []
    for manifest_path in (ROOT / "registry" / "tasks").glob("*/task_registry.json"):
        manifest = load_json_object(manifest_path)
        task_id = manifest["task_id"]
        status = manifest.get("status", "unknown")
        nodes.append({"id": f"task:{task_id}", "kind": "task", "label": manifest["title"], "status": status})
        for workflow in manifest["visible_workflows"]:
            workflow_id = f"workflow:{workflow['name']}"
            nodes.append({"id": workflow_id, "kind": "workflow", "label": workflow["end_to_end_function"], "status": status})
            edges.append({"from": f"task:{task_id}", "to": workflow_id, "kind": "has-visible-workflow"})
            if workflow.get("parent_workflow"):
                edges.append({"from": f"workflow:{workflow['parent_workflow']}", "to": workflow_id, "kind": "has-subworkflow"})
            if workflow.get("domain_id"):
                domain_id = f"domain:{workflow['domain_id']}"
                nodes.append({"id": domain_id, "kind": "domain", "label": workflow["domain_id"]})
                edges.append({"from": workflow_id, "to": domain_id, "kind": "binds-domain"})
            for skill in workflow["composed_skills"]:
                nodes.append({"id": f"skill:{skill}", "kind": "skill", "label": skill})
                edges.append({"from": workflow_id, "to": f"skill:{skill}", "kind": "composes-skill"})
            for hook in workflow["deterministic_hooks"]:
                nodes.append({"id": f"hook:{hook}", "kind": "hook", "label": hook})
                edges.append({"from": workflow_id, "to": f"hook:{hook}", "kind": "uses-hook"})
            for artifact in workflow["artifacts"]:
                nodes.append({"id": f"artifact:{artifact}", "kind": "artifact", "label": artifact})
                edges.append({"from": workflow_id, "to": f"artifact:{artifact}", "kind": "produces-or-uses"})
    unique_nodes = {node["id"]: node for node in nodes}
    graph = {"nodes": sorted(unique_nodes.values(), key=lambda row: row["id"]), "edges": edges}
    write_json(ROOT / "agentic" / "state" / "workflow_graph.json", graph)
    lines = ["# Workflow Hub Report", "", f"- Nodes: {len(graph['nodes'])}", f"- Edges: {len(edges)}", "", "## Visible Workflows", ""]
    for node in graph["nodes"]:
        if node["kind"] == "workflow":
            lines.append(f"- `{node['id']}` ({node.get('status', 'unknown')}): {node['label']}")
    out = ROOT / "agentic" / "reports" / "workflow_hub" / "latest.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
