"""Provider-neutral workflow graph construction and validation."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

from . import __version__
from .inventory import iter_inventory_items
from .jsonio import document_hash
from .model import SCHEMA_VERSION, require_unique

EDGE_KINDS = {"data", "control", "condition", "lifecycle", "failure", "stop", "repeat"}


@dataclass(frozen=True, slots=True)
class GraphDiagnostic:
    code: str
    workflow_id: str
    message: str
    node_id: str | None = None
    edge_index: int | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
            "workflow_id": self.workflow_id,
        }
        if self.node_id is not None:
            result["node_id"] = self.node_id
        if self.edge_index is not None:
            result["edge_index"] = self.edge_index
        return result


def _short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]


def _node(item: dict[str, Any], contract_id: str) -> dict[str, Any]:
    return {
        "capabilities": {"invocation": [], "persistent": []},
        "contract_id": contract_id,
        "effects": sorted(set(item.get("side_effect_hints", []))),
        "id": "node_" + _short_hash(item["id"]),
        "kind": item["kind"],
        "name": item.get("metadata", {}).get("name") or item["path"].rsplit("/", 1)[-1],
        "source_item_ids": [item["id"]],
    }


def build_workflow_graph(
    inventory: dict[str, Any], contracts_document: dict[str, Any]
) -> dict[str, Any]:
    """Build only evidenced topology; no file-order edges are invented."""

    items = {item["id"]: item for item in iter_inventory_items(inventory)}
    workflows: list[dict[str, Any]] = []
    for contract in contracts_document.get("contracts", []):
        item = items[contract["source_item_id"]]
        node = _node(item, contract["id"])
        workflow_id = "workflow_" + _short_hash(item["id"])
        workflows.append(
            {
                "critical": item["kind"] in {"entry_point", "command", "skill"},
                "edges": [],
                "entry_node": node["id"],
                "id": workflow_id,
                "name": str(node["name"]),
                "nodes": [node],
                "review_status": (
                    "extracted"
                    if contract.get("review_status") == "extracted"
                    else "proposed"
                ),
            }
        )
    workflows.sort(key=lambda workflow: workflow["id"])
    document = {
        "artifact": "workflow",
        "contracts_hash": document_hash(contracts_document),
        "schema_version": SCHEMA_VERSION,
        "tool": {"name": "to-prism", "version": __version__},
        "workflows": workflows,
    }
    diagnostics = validate_workflow_graph(document, contracts_document)
    if diagnostics:
        raise ValueError(
            "invalid constructed workflow: " + "; ".join(d.message for d in diagnostics)
        )
    return document


def validate_workflow_graph(
    document: dict[str, Any], contracts_document: dict[str, Any] | None = None
) -> list[GraphDiagnostic]:
    diagnostics: list[GraphDiagnostic] = []
    workflows = document.get("workflows", [])
    workflow_ids = [workflow.get("id", "") for workflow in workflows]
    try:
        require_unique(workflow_ids, "workflow IDs")
    except ValueError as exc:
        diagnostics.append(GraphDiagnostic("duplicate-workflow", "", str(exc)))
    known_contracts = (
        {contract["id"] for contract in contracts_document.get("contracts", [])}
        if contracts_document is not None
        else None
    )
    for workflow in workflows:
        workflow_id = workflow.get("id", "<unknown>")
        nodes = workflow.get("nodes", [])
        node_ids = [node.get("id", "") for node in nodes]
        duplicates = sorted({node for node in node_ids if node_ids.count(node) > 1})
        for node_id in duplicates:
            diagnostics.append(
                GraphDiagnostic(
                    "duplicate-node", workflow_id, "duplicate node ID", node_id
                )
            )
        known_nodes = set(node_ids)
        entry = workflow.get("entry_node")
        if nodes and entry is None:
            diagnostics.append(
                GraphDiagnostic(
                    "ambiguous-entrypoint", workflow_id, "workflow has no entry node"
                )
            )
        elif entry is not None and entry not in known_nodes:
            diagnostics.append(
                GraphDiagnostic(
                    "dangling-entrypoint",
                    workflow_id,
                    "entry node does not exist",
                    entry,
                )
            )
        adjacency: dict[str, set[str]] = {node: set() for node in known_nodes}
        for index, edge in enumerate(workflow.get("edges", [])):
            source, target = edge.get("source"), edge.get("target")
            if edge.get("kind") not in EDGE_KINDS:
                diagnostics.append(
                    GraphDiagnostic(
                        "unknown-edge-kind",
                        workflow_id,
                        "edge kind is unsupported",
                        edge_index=index,
                    )
                )
            if source not in known_nodes or target not in known_nodes:
                diagnostics.append(
                    GraphDiagnostic(
                        "dangling-edge",
                        workflow_id,
                        "edge endpoint does not exist",
                        edge_index=index,
                    )
                )
                continue
            if not edge.get("evidence"):
                diagnostics.append(
                    GraphDiagnostic(
                        "edge-without-evidence",
                        workflow_id,
                        "edge lacks source evidence",
                        edge_index=index,
                    )
                )
            adjacency[source].add(target)
            if edge.get("kind") == "repeat":
                if (
                    not isinstance(edge.get("max_iterations"), int)
                    or edge["max_iterations"] <= 0
                ):
                    diagnostics.append(
                        GraphDiagnostic(
                            "unbounded-loop",
                            workflow_id,
                            "repeat edge needs a positive static bound",
                            edge_index=index,
                        )
                    )
                if edge.get("state_changes") is not True:
                    diagnostics.append(
                        GraphDiagnostic(
                            "unchanging-loop",
                            workflow_id,
                            "repeat edge must change state",
                            edge_index=index,
                        )
                    )
        if entry in known_nodes:
            reachable: set[str] = set()
            pending = [entry]
            while pending:
                current = pending.pop()
                if current in reachable:
                    continue
                reachable.add(current)
                pending.extend(adjacency[current] - reachable)
            for node_id in sorted(known_nodes - reachable):
                diagnostics.append(
                    GraphDiagnostic(
                        "unreachable-node", workflow_id, "node is unreachable", node_id
                    )
                )
        # A cyclic component must expose at least one explicit bounded repeat
        # transition. Plain control/data cycles cannot be rendered safely.
        cyclic_nodes: set[str] = set()
        for origin in sorted(known_nodes):
            seen: set[str] = set()
            pending = list(adjacency[origin])
            while pending:
                current = pending.pop()
                if current == origin:
                    cyclic_nodes.add(origin)
                    break
                if current in seen:
                    continue
                seen.add(current)
                pending.extend(adjacency.get(current, set()) - seen)
        if cyclic_nodes:
            repeat_edges = [
                edge
                for edge in workflow.get("edges", [])
                if edge.get("kind") == "repeat"
                and edge.get("source") in cyclic_nodes
                and edge.get("target") in cyclic_nodes
            ]
            if not repeat_edges:
                diagnostics.append(
                    GraphDiagnostic(
                        "cycle-without-repeat",
                        workflow_id,
                        "cyclic topology requires an explicit bounded repeat edge",
                    )
                )
        for node in nodes:
            if node.get("kind") != "choice":
                continue
            outgoing = [
                edge
                for edge in workflow.get("edges", [])
                if edge.get("source") == node.get("id")
                and edge.get("kind") == "condition"
            ]
            conditions = [edge.get("condition") for edge in outgoing]
            if len(outgoing) < 2 or any(
                condition in {None, ""} for condition in conditions
            ):
                diagnostics.append(
                    GraphDiagnostic(
                        "invalid-choice",
                        workflow_id,
                        "choice needs at least two explicitly conditioned branches",
                        node.get("id"),
                    )
                )
            elif len(set(conditions)) != len(conditions):
                diagnostics.append(
                    GraphDiagnostic(
                        "duplicate-choice-condition",
                        workflow_id,
                        "choice branch conditions must be distinct",
                        node.get("id"),
                    )
                )
            if node.get("exhaustive") is not True:
                diagnostics.append(
                    GraphDiagnostic(
                        "non-exhaustive-choice",
                        workflow_id,
                        "choice must declare a reviewed exhaustive closed sum",
                        node.get("id"),
                    )
                )
        for node in nodes:
            contract_id = node.get("contract_id")
            if known_contracts is not None and contract_id not in known_contracts:
                diagnostics.append(
                    GraphDiagnostic(
                        "dangling-contract",
                        workflow_id,
                        "node contract does not exist",
                        node.get("id"),
                    )
                )
    return diagnostics


build_workflows = build_workflow_graph
validate_workflow = validate_workflow_graph
