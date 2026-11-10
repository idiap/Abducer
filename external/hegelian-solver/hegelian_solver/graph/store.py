# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Concept graph storage and query helpers.

`ConceptGraph` is the solver's persistent record of accepted/provisional development: nodes
are concepts (`ConceptGraphNode`), edges are validated transformations
(`ConceptGraphEdge`, built by `edge_from_candidate` from a candidate + its validation packet
+ ranking decision), and `rejected_candidates` keeps the boundary evidence — candidates that
were tried and failed — instead of discarding it. The query helpers
(`successors`/`predecessors`/`open_residual_limits`/`active_frontier`) are what the
explanation and report stages walk to describe "what happened and what's still open".
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from hegelian_solver.ids import stable_id
from hegelian_solver.io import read_structured, write_structured
from hegelian_solver.schemas import (
    ConceptGraphEdge,
    ConceptGraphNode,
    ConceptNode,
    RankingDecision,
    TransformationCandidate,
    ValidationPacket,
)


class ConceptGraph(BaseModel):
    nodes: dict[str, ConceptGraphNode] = Field(default_factory=dict)
    edges: dict[str, ConceptGraphEdge] = Field(default_factory=dict)
    rejected_candidates: list[dict[str, Any]] = Field(default_factory=list)

    def add_node(self, node: ConceptGraphNode) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: ConceptGraphEdge) -> None:
        self.edges[edge.id] = edge

    def successors(self, node_id: str) -> list[ConceptGraphEdge]:
        return [edge for edge in self.edges.values() if edge.source == node_id]

    def predecessors(self, node_id: str) -> list[ConceptGraphEdge]:
        return [edge for edge in self.edges.values() if edge.target == node_id]

    def open_residual_limits(self) -> list[dict[str, Any]]:
        return [
            {"edge": edge.id, "target": edge.target, "residual_limit": residual}
            for edge in self.edges.values()
            for residual in edge.residual_limits
        ]

    def active_frontier(self) -> list[ConceptGraphNode]:
        sources = {edge.source for edge in self.edges.values()}
        targets = {edge.target for edge in self.edges.values()}
        frontier_ids = (targets - sources) or set(self.nodes)
        return [self.nodes[node_id] for node_id in sorted(frontier_ids) if node_id in self.nodes]

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": {key: value.model_dump(mode="json") for key, value in self.nodes.items()},
            "edges": {key: value.model_dump(mode="json") for key, value in self.edges.items()},
            "rejected_candidates": self.rejected_candidates,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ConceptGraph":
        return cls(
            nodes={
                key: ConceptGraphNode.model_validate(value)
                for key, value in payload.get("nodes", {}).items()
            },
            edges={
                key: ConceptGraphEdge.model_validate(value)
                for key, value in payload.get("edges", {}).items()
            },
            rejected_candidates=payload.get("rejected_candidates", []),
        )

    @classmethod
    def load(cls, path: str | Path) -> "ConceptGraph":
        return cls.from_dict(read_structured(path))

    def save(self, path: str | Path) -> None:
        write_structured(path, self.to_dict())


def node_from_concept(concept: ConceptNode, status: str | None = None) -> ConceptGraphNode:
    """Wrap a formalized concept as a graph node, embedding its full payload so the graph
    file is self-contained and doesn't need a side lookup table."""

    return ConceptGraphNode(
        id=concept.id,
        name=concept.name,
        domain=concept.domain,
        concept=concept.model_dump(mode="json"),
        status=status or concept.status,
    )


def _edge_relation(candidate: TransformationCandidate) -> str:
    return candidate.preservation_map.get("relation", "extends")


def edge_from_candidate(
    source: ConceptNode,
    candidate: TransformationCandidate,
    packet: ValidationPacket,
    decision: RankingDecision,
) -> ConceptGraphEdge:
    """Turn an accepted/provisional candidate into a `ConceptGraphEdge`, carrying its
    trigger, operator, preservation map, obligations, residual limits, and ranking decision
    so the edge alone explains why the move was made and what remains open."""

    target = candidate.target_concept
    trigger = {"type": "Unknown", "id": candidate.triggered_by[0] if candidate.triggered_by else ""}
    if candidate.triggered_by:
        trigger = {
            "type": "FailureCertificateOrDiscoverySignal",
            "id": candidate.triggered_by[0],
            "label": candidate.resolution_mechanism.split()[-1],
        }
    payload = {
        "source": source.id,
        "target": target["id"],
        "relation": _edge_relation(candidate),
        "trigger": trigger,
        "operator": candidate.operator,
        "map": candidate.preservation_map,
        "regime": target.get("regime"),
        "obligations": [item.model_dump(mode="json") for item in packet.obligations],
        "certificates": [packet.model_dump(mode="json")],
        "residual_limits": candidate.residual_limits,
        "ranking": decision.model_dump(mode="json"),
        "status": "validated" if decision.decision in {"accept", "accept_as_branch"} else decision.decision,
    }
    payload["id"] = stable_id("edge", payload)
    return ConceptGraphEdge.model_validate(payload)
