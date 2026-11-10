"""Conceptual pressure interpretation and downstream impact analysis."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any

from tdr.domain.models import PressureItem, bounded, stable_id


PRESSURE_KINDS = {
    "anomaly": ("anomal", "contradict", "disagree", "violate"),
    "proof_blocker": ("proof", "lemma", "unproved", "cannot derive", "type error"),
    "fragmentation": ("fragment", "incompat", "translation", "false friend"),
    "explanatory_gap": ("explain", "why", "mechanism", "opaque"),
    "predictive_gap": ("predict", "forecast", "held-out", "novel consequence"),
    "pragmatic_need": ("compute", "experiment", "design", "algorithm", "measurement"),
    "scope_failure": ("regime", "boundary", "scale", "scope", "limit"),
}


def classify_pressure(text: str) -> str:
    lowered = text.lower()
    scores = {kind: sum(token in lowered for token in tokens) for kind, tokens in PRESSURE_KINDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "conceptual_gap"


def dependency_impact(nodes: list[str], edges: list[list[str]], locus: list[str]) -> float:
    """Return normalized downstream reach from a locus in a dependency DAG/graph."""
    if not nodes:
        return 0.0
    graph: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        if len(edge) == 2:
            graph[str(edge[0])].add(str(edge[1]))
    seen = set(map(str, locus))
    queue = deque(seen)
    while queue:
        current = queue.popleft()
        for child in graph[current]:
            if child not in seen:
                seen.add(child)
                queue.append(child)
    return min(1.0, len(seen) / max(1, len(set(map(str, nodes)))))


def interpret_pressures(payload: dict[str, Any]) -> list[PressureItem]:
    events = payload.get("events") or payload.get("anomalies") or []
    graph = dict(payload.get("dependency_graph") or {})
    output: list[PressureItem] = []
    for index, raw in enumerate(events):
        event = {"description": raw} if isinstance(raw, str) else dict(raw)
        description = str(event.get("description", "")).strip()
        if not description:
            continue
        locus = [str(item) for item in event.get("locus", [])]
        impact = event.get("downstream_impact")
        if impact is None:
            impact = dependency_impact(graph.get("nodes", []), graph.get("edges", []), locus)
        evidence = list(event.get("evidence", []))
        reliability = event.get("reliability")
        if reliability is None:
            reliability = sum(float(item.get("reliability", 0.5)) for item in evidence) / max(1, len(evidence))
        output.append(
            PressureItem(
                pressure_id=str(event.get("pressure_id") or stable_id("pressure", [description, index])),
                kind=str(event.get("kind") or classify_pressure(description)),
                description=description,
                locus=locus,
                evidence=evidence,
                severity=bounded(event.get("severity", 0.5), 0.5),
                downstream_impact=bounded(impact, 0.2),
                reliability=bounded(reliability, 0.5),
                preferred_solution=event.get("preferred_solution"),
            )
        )
    return output

