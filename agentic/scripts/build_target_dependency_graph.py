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

"""Build a recursive target dependency graph from existing Abducer artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from agentic_common import (
    ROOT,
    clean_text,
    ensure_list,
    kb_ref_from_path,
    load_json_object,
    load_optional_json,
    parse_kb_statements,
    parse_phyp_file,
    rel,
    repo_path,
    stable_id,
    utc_now,
    write_json,
)


TERMINAL = {"grounded", "accepted-local", "refuted"}


class GraphBuilder:
    """Incrementally build a typed dependency graph."""

    def __init__(self, target: dict[str, Any]) -> None:
        self.target = target
        self.kb = repo_path(str(target["kb_path"]), must_exist=True)
        self.kb_ref = kb_ref_from_path(self.kb)
        self.artifacts = ROOT / "artifacts" / self.kb_ref
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: list[dict[str, Any]] = []
        self.statements = parse_kb_statements(self.kb)
        self.visiting: set[str] = set()

    def add_node(
        self,
        node_id: str,
        *,
        kind: str,
        status: str,
        label: str,
        source_artifact: str,
        evidence_paths: list[str] | None = None,
        parents: list[str] | None = None,
        next_action: str = "",
        blocker: str = "",
        payload: dict[str, Any] | None = None,
    ) -> None:
        existing = self.nodes.get(node_id)
        evidence = list(dict.fromkeys(evidence_paths or []))
        parents_clean = list(dict.fromkeys(parents or []))
        if existing:
            existing["evidence_paths"] = sorted(set(existing.get("evidence_paths", [])) | set(evidence))
            existing["parents"] = sorted(set(existing.get("parents", [])) | set(parents_clean))
            if existing["status"] in TERMINAL and status not in TERMINAL:
                return
            if existing["status"] != "grounded":
                existing["status"] = status
            if next_action and not existing.get("next_action"):
                existing["next_action"] = next_action
            if blocker and not existing.get("blocker"):
                existing["blocker"] = blocker
            existing.setdefault("payload", {}).update(payload or {})
            return
        self.nodes[node_id] = {
            "id": node_id,
            "kind": kind,
            "status": status,
            "label": clean_text(label)[:600],
            "source_artifact": source_artifact,
            "evidence_paths": evidence,
            "parents": parents_clean,
            "next_action": next_action,
            "blocker": blocker,
            "payload": payload or {},
        }

    def add_edge(self, source: str, target: str, *, kind: str, source_artifact: str) -> None:
        edge = {"from": source, "to": target, "kind": kind, "source_artifact": source_artifact}
        if edge not in self.edges:
            self.edges.append(edge)

    def add_statement_dependency(self, statement_id: str, parent: str | None = None) -> None:
        statement = self.statements.get(statement_id)
        if not statement:
            self.add_node(
                f"missing:{statement_id}",
                kind="missing_statement",
                status="missing-premise",
                label=f"Statement ID not found in KB: {statement_id}",
                source_artifact=rel(self.kb),
                evidence_paths=[rel(self.kb)],
                parents=[parent] if parent else [],
                next_action="Resolve the missing statement ID or add a KB statement before continuing.",
                blocker="LINT-003",
            )
            if parent:
                self.add_edge(parent, f"missing:{statement_id}", kind="missing-kb-statement", source_artifact=rel(self.kb))
            return
        status = "accepted-local" if statement.get("status") == "accepted" else "tentative-local"
        label = statement.get("informal") or statement.get("latex") or statement_id
        self.add_node(
            f"statement:{statement_id}",
            kind=str(statement.get("kind", "statement")),
            status=status,
            label=label,
            source_artifact=rel(self.kb),
            evidence_paths=[rel(self.kb)],
            parents=[parent] if parent else [],
            next_action="Use this grounded statement as local evidence." if status == "accepted-local" else "Review tentative statement before using it as a dependency.",
            payload={"statement_id": statement_id, "source_ids": statement.get("source_ids", [])},
        )
        if parent:
            self.add_edge(parent, f"statement:{statement_id}", kind="kb-depends-on", source_artifact=rel(self.kb))
        if statement_id in self.visiting:
            self.add_node(
                f"cycle:{statement_id}",
                kind="cycle",
                status="blocked",
                label=f"Dependency cycle detected at {statement_id}",
                source_artifact=rel(self.kb),
                evidence_paths=[rel(self.kb)],
                parents=[f"statement:{statement_id}"],
                next_action="Inspect cyclic KB dependencies before recursive expansion.",
                blocker="dependency-cycle",
            )
            return
        self.visiting.add(statement_id)
        for dep in ensure_list(statement.get("depends_on")):
            if isinstance(dep, str) and dep.strip():
                self.add_statement_dependency(dep.strip(), parent=f"statement:{statement_id}")
        self.visiting.remove(statement_id)

    def add_connection_analysis(self) -> None:
        path = self.artifacts / "connection-analysis.json"
        analysis = load_optional_json(path)
        if not analysis:
            return
        main_claims = set(self.target["main_claim_ids"])
        for row in ensure_list(analysis.get("top_interventions"))[:20]:
            if not isinstance(row, dict):
                continue
            statement_id = clean_text(row.get("statement_id"))
            if not statement_id:
                continue
            node_id = f"intervention:{statement_id}"
            self.add_node(
                node_id,
                kind="intervention",
                status="bridge-obligation",
                label=row.get("rationale") or f"Intervention candidate {statement_id}",
                source_artifact=rel(path),
                evidence_paths=[rel(path)],
                parents=[f"statement:{statement_id}"],
                next_action="Use connector evidence to decide whether this intervention belongs in the target route.",
                payload={"score": row.get("score"), "concept_focus": row.get("concept_focus", [])},
            )
            self.add_statement_dependency(statement_id, parent=node_id)
            for dep in ensure_list(row.get("missing_dependencies")):
                dep_id = clean_text(dep)
                if dep_id:
                    self.add_node(
                        f"missing-dependency:{dep_id}",
                        kind="missing_dependency",
                        status="missing-premise",
                        label=f"Connector reported unresolved dependency {dep_id}",
                        source_artifact=rel(path),
                        evidence_paths=[rel(path)],
                        parents=[node_id],
                        next_action="Add, import, or refute this dependency before using the route.",
                        blocker="connector-unresolved-dependency",
                    )
                    self.add_edge(node_id, f"missing-dependency:{dep_id}", kind="requires", source_artifact=rel(path))
            if statement_id in main_claims:
                self.add_edge(f"statement:{statement_id}", node_id, kind="target-intervention", source_artifact=rel(path))

        candidates = ensure_list(analysis.get("connection_candidates"))[:40]
        for row in candidates:
            if not isinstance(row, dict):
                continue
            from_id = clean_text(row.get("from_id"))
            to_id = clean_text(row.get("to_id"))
            if not from_id or not to_id:
                continue
            if from_id not in main_claims and to_id not in main_claims:
                continue
            node_id = stable_id("bridge", from_id, to_id, row.get("relation"))
            self.add_node(
                node_id,
                kind="connector_bridge",
                status="bridge-obligation",
                label=f"{from_id} -> {to_id} ({row.get('relation', 'candidate-link')})",
                source_artifact=rel(path),
                evidence_paths=[rel(path)],
                parents=[f"statement:{from_id}", f"statement:{to_id}"],
                next_action="Test whether this connector link is a genuine proof dependency or only semantic proximity.",
                payload={"score": row.get("score"), "relation": row.get("relation"), "evidence_terms": row.get("evidence_terms", [])},
            )
            self.add_statement_dependency(from_id, parent=node_id)
            self.add_statement_dependency(to_id, parent=node_id)

    def add_phyp(self) -> None:
        path = ROOT / "phyp" / f"{self.kb_ref}.proof-hypotheses.yaml"
        main_claims = set(self.target["main_claim_ids"])
        for row in parse_phyp_file(path):
            target = clean_text(row.get("target_statement_id") or row.get("target"))
            support = clean_text(row.get("support_statement_id") or row.get("support"))
            if target not in main_claims and support not in main_claims:
                continue
            hyp_id = clean_text(row.get("id")) or stable_id("hyp", target, support)
            node_id = f"hypothesis:{hyp_id}"
            self.add_node(
                node_id,
                kind=str(row.get("kind", "hypothesis")),
                status="tentative-local",
                label=row.get("informal") or row.get("hypothesis_latex") or hyp_id,
                source_artifact=rel(path),
                evidence_paths=[rel(path)],
                parents=[f"statement:{target}"] if target else [],
                next_action="Evaluate this hypothesis before promoting it to a route dependency.",
                payload={"priority": row.get("priority"), "target_statement_id": target, "support_statement_id": support},
            )
            if target:
                self.add_statement_dependency(target, parent=node_id)
            if support:
                self.add_statement_dependency(support, parent=node_id)

    def add_pathways(self) -> None:
        path = self.artifacts / "entrypoint-pathways.json"
        payload = load_optional_json(path)
        main_claims = set(self.target["main_claim_ids"])
        for row in ensure_list(payload.get("pathways")):
            if not isinstance(row, dict):
                continue
            ids = {clean_text(row.get("entry_statement_id"))}
            for hyp in ensure_list(row.get("supporting_hypotheses")):
                if isinstance(hyp, dict):
                    ids.add(clean_text(hyp.get("target")))
                    ids.add(clean_text(hyp.get("support")))
            if not (ids & main_claims):
                continue
            path_id = clean_text(row.get("path_id")) or stable_id("path", row.get("goal"))
            node_id = f"pathway:{path_id}"
            self.add_node(
                node_id,
                kind="pathway",
                status="proof-debt",
                label=row.get("goal") or path_id,
                source_artifact=rel(path),
                evidence_paths=[rel(path)],
                parents=[f"statement:{item}" for item in sorted(ids) if item],
                next_action="Convert this pathway into theorem-shaped obligations or reject it as non-actionable.",
                payload={"score": row.get("pathway_score"), "execution_plan": row.get("execution_plan", [])},
            )
            for item in sorted(ids):
                if item:
                    self.add_statement_dependency(item, parent=node_id)

    def add_json_obligations(self, path: Path, rows_key: str, prefix: str) -> None:
        payload = load_optional_json(path)
        rows = ensure_list(payload.get(rows_key))
        main_claims = set(self.target["main_claim_ids"])
        for row in rows:
            if not isinstance(row, dict):
                continue
            source = clean_text(row.get("source_statement_id") or row.get("anchor_statement_id"))
            target = clean_text(row.get("target_statement_id"))
            if source not in main_claims and target not in main_claims:
                continue
            row_id = clean_text(row.get("sketch_id") or row.get("bridge_id") or row.get("conjecture_id") or row.get("id"))
            node_id = f"{prefix}:{row_id or stable_id(prefix, source, target)}"
            label = row.get("title") or row.get("route_synopsis") or row.get("conjectured_object") or node_id
            self.add_node(
                node_id,
                kind=prefix,
                status="route-lemma" if prefix == "proof-sketch" else "bridge-obligation",
                label=label,
                source_artifact=rel(path),
                evidence_paths=[rel(path)],
                parents=[f"statement:{item}" for item in [source, target] if item],
                next_action="Discharge or refute the route obligations attached to this artifact.",
                payload={"score": row.get("sketch_score") or row.get("priority"), "object": row.get("conjectured_object") or row.get("abstraction_label")},
            )
            for item in [source, target]:
                if item:
                    self.add_statement_dependency(item, parent=node_id)
            for obligation in ensure_list(row.get("proof_obligations"))[:8]:
                if isinstance(obligation, dict):
                    text = obligation.get("requirement") or obligation.get("claim_template") or obligation.get("kind")
                    obl_id = obligation.get("obligation_id") or stable_id("obl", node_id, text)
                else:
                    text = str(obligation)
                    obl_id = stable_id("obl", node_id, text)
                child_id = f"obligation:{obl_id}"
                self.add_node(
                    child_id,
                    kind="proof_obligation",
                    status="proof-debt",
                    label=text,
                    source_artifact=rel(path),
                    evidence_paths=[rel(path)],
                    parents=[node_id],
                    next_action="Promote this obligation to a proof queue item, prove it, refute it, or mark it blocked with evidence.",
                )
                self.add_edge(node_id, child_id, kind="has-proof-obligation", source_artifact=rel(path))

    def add_proof_queue(self) -> None:
        path = self.artifacts / "proof-queue.json"
        payload = load_optional_json(path)
        main_claims = set(self.target["main_claim_ids"])
        for row in ensure_list(payload.get("entries")):
            if not isinstance(row, dict):
                continue
            source = clean_text(row.get("source_statement_id"))
            target = clean_text(row.get("target_statement_id"))
            if source not in main_claims and target not in main_claims:
                continue
            queue_key = clean_text(row.get("queue_key")) or stable_id("queue", source, target, row.get("title"))
            status = clean_text(row.get("status")).lower()
            node_status = "accepted-local" if status == "completed" else "proof-debt"
            if status in {"blocked", "deferred"}:
                node_status = "blocked"
            node_id = f"queue:{queue_key}"
            self.add_node(
                node_id,
                kind="proof_queue_entry",
                status=node_status,
                label=row.get("title") or row.get("claim_text") or queue_key,
                source_artifact=rel(path),
                evidence_paths=[rel(path)],
                parents=[f"statement:{item}" for item in [source, target] if item],
                next_action="Consume this queue entry in the prove cycle." if node_status == "proof-debt" else "Use queue terminal status as evidence.",
                blocker=row.get("deferred_by") if node_status == "blocked" else "",
                payload={"priority": row.get("priority"), "queue_status": row.get("status"), "bridge_id": row.get("bridge_id")},
            )
            for item in [source, target]:
                if item:
                    self.add_statement_dependency(item, parent=node_id)

    def build(self) -> dict[str, Any]:
        target_node = f"target:{self.target['target_id']}"
        self.add_node(
            target_node,
            kind="target",
            status="proof-debt",
            label=self.target["raw_goal"],
            source_artifact="agentic/state/current_target.json",
            evidence_paths=["agentic/state/current_target.json"],
            next_action="Resolve the recursive dependency frontier before release.",
        )
        for claim_id in self.target["main_claim_ids"]:
            self.add_statement_dependency(str(claim_id), parent=target_node)
        self.add_connection_analysis()
        self.add_phyp()
        self.add_pathways()
        self.add_json_obligations(self.artifacts / "bridge-plan.json", "bridges", "bridge-plan")
        self.add_json_obligations(self.artifacts / "concept-gap-abstractions.json", "conjectures", "conjecture")
        self.add_json_obligations(self.artifacts / "proof-sketches.json", "proof_sketches", "proof-sketch")
        self.add_proof_queue()

        frontier = [
            {
                "id": node["id"],
                "kind": node["kind"],
                "status": node["status"],
                "next_action": node.get("next_action", ""),
                "blocker": node.get("blocker", ""),
            }
            for node in self.nodes.values()
            if node["status"] not in TERMINAL
        ]
        frontier.sort(key=lambda row: (row["status"], row["kind"], row["id"]))
        summary = {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "frontier_count": len(frontier),
            "status_counts": {},
            "kind_counts": {},
        }
        for node in self.nodes.values():
            summary["status_counts"][node["status"]] = summary["status_counts"].get(node["status"], 0) + 1
            summary["kind_counts"][node["kind"]] = summary["kind_counts"].get(node["kind"], 0) + 1
        return {
            "graph_id": f"depgraph.{self.target['target_id']}",
            "target_id": self.target["target_id"],
            "kb_path": self.target["kb_path"],
            "generated_utc": utc_now(),
            "nodes": sorted(self.nodes.values(), key=lambda row: row["id"]),
            "edges": sorted(self.edges, key=lambda row: (row["from"], row["to"], row["kind"])),
            "frontier": frontier,
            "summary": summary,
        }


def render_markdown(graph: dict[str, Any]) -> str:
    lines = [
        f"# Dependency Closure: {graph['target_id']}",
        "",
        f"- Nodes: {graph['summary']['node_count']}",
        f"- Edges: {graph['summary']['edge_count']}",
        f"- Open frontier: {graph['summary']['frontier_count']}",
        "",
        "## Status Counts",
        "",
    ]
    for status, count in sorted(graph["summary"]["status_counts"].items()):
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "## Open Frontier", ""])
    for row in graph["frontier"][:40]:
        lines.append(f"- `{row['id']}` ({row['status']}): {row['next_action'] or row['blocker']}")
    lines.extend(["", "## Boundary", ""])
    lines.append("Connector links and graph centrality are treated as route obligations, not as proof dependencies, until discharged by later proof work.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="Target packet JSON path.")
    parser.add_argument("--output-json", required=True, help="Output dependency graph JSON path.")
    parser.add_argument("--output-md", required=True, help="Output dependency closure report path.")
    args = parser.parse_args()

    target = load_json_object(Path(args.target))
    graph = GraphBuilder(target).build()
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    write_json(output_json, graph)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(graph), encoding="utf-8")
    print(f"Wrote {rel(output_json)}")
    print(f"Wrote {rel(output_md)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
