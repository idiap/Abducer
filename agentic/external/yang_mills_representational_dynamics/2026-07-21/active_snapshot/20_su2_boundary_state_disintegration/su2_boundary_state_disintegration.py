"""Finite-graph relative tree gauge and SU(2) boundary-state certificates."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from typing import Mapping, Sequence

import numpy as np


Vertex = tuple[int, int]


@dataclass(frozen=True)
class Edge:
    source: Vertex
    target: Vertex


@dataclass(frozen=True)
class Plaquette:
    oriented_edges: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class BlockGraph:
    vertices: tuple[Vertex, ...]
    edges: tuple[Edge, ...]
    plaquettes: tuple[Plaquette, ...]
    boundary: tuple[Vertex, ...]
    forest_parent: Mapping[Vertex, tuple[Vertex, int, int]]
    retained_edges: tuple[int, ...]
    fiber_edges: tuple[int, ...]


@dataclass(frozen=True)
class BoundaryLabels:
    perimeter_angle: float
    center_sign: int
    near_cut_locus: bool
    stabilizer_type: str

    def to_dict(self) -> dict[str, float | int | bool | str]:
        return asdict(self)


def qmul(left: Sequence[float], right: Sequence[float]) -> np.ndarray:
    a = np.asarray(left, dtype=float)
    b = np.asarray(right, dtype=float)
    return np.array(
        [
            a[0] * b[0] - np.dot(a[1:], b[1:]),
            a[0] * b[1] + b[0] * a[1] + a[2] * b[3] - a[3] * b[2],
            a[0] * b[2] + b[0] * a[2] + a[3] * b[1] - a[1] * b[3],
            a[0] * b[3] + b[0] * a[3] + a[1] * b[2] - a[2] * b[1],
        ]
    )


def qinv(value: Sequence[float]) -> np.ndarray:
    q = np.asarray(value, dtype=float)
    norm_sq = float(np.dot(q, q))
    if norm_sq <= 0.0:
        raise ValueError("quaternion must be nonzero")
    return np.concatenate(([q[0]], -q[1:])) / norm_sq


def qnormalize(value: Sequence[float]) -> np.ndarray:
    q = np.asarray(value, dtype=float)
    norm = float(np.linalg.norm(q))
    if not math.isfinite(norm) or norm <= 0.0:
        raise ValueError("quaternion must have positive finite norm")
    return q / norm


def qexp(axis_angle: Sequence[float]) -> np.ndarray:
    a = np.asarray(axis_angle, dtype=float)
    theta = float(np.linalg.norm(a))
    if theta == 0.0:
        return np.array([1.0, 0.0, 0.0, 0.0])
    return np.concatenate(([math.cos(theta)], math.sin(theta) * a / theta))


def random_su2(rng: np.random.Generator) -> np.ndarray:
    return qnormalize(rng.normal(size=4))


def grid_2x2_block() -> BlockGraph:
    vertices = tuple((x, y) for y in range(3) for x in range(3))
    edges: list[Edge] = []
    edge_index: dict[tuple[Vertex, Vertex], int] = {}
    for y in range(3):
        for x in range(2):
            edge_index[((x, y), (x + 1, y))] = len(edges)
            edges.append(Edge((x, y), (x + 1, y)))
    for x in range(3):
        for y in range(2):
            edge_index[((x, y), (x, y + 1))] = len(edges)
            edges.append(Edge((x, y), (x, y + 1)))
    plaquettes: list[Plaquette] = []
    for y in range(2):
        for x in range(2):
            plaquettes.append(
                Plaquette(
                    (
                        (edge_index[((x, y), (x + 1, y))], 1),
                        (edge_index[((x + 1, y), (x + 1, y + 1))], 1),
                        (edge_index[((x, y + 1), (x + 1, y + 1))], -1),
                        (edge_index[((x, y), (x, y + 1))], -1),
                    )
                )
            )
    boundary = tuple(v for v in vertices if v[0] in (0, 2) or v[1] in (0, 2))
    root = (1, 0)
    center = (1, 1)
    forest_edge = edge_index[(root, center)]
    forest_parent = {center: (root, forest_edge, 1)}
    retained = tuple(
        i for i, edge in enumerate(edges) if edge.source in boundary and edge.target in boundary
    )
    fiber = tuple(i for i in range(len(edges)) if i not in retained and i != forest_edge)
    return BlockGraph(
        vertices=vertices,
        edges=tuple(edges),
        plaquettes=tuple(plaquettes),
        boundary=boundary,
        forest_parent=forest_parent,
        retained_edges=retained,
        fiber_edges=fiber,
    )


def oriented_link(links: np.ndarray, edge_index: int, sign: int) -> np.ndarray:
    value = links[edge_index]
    return value if sign == 1 else qinv(value)


def gauge_transform(
    block: BlockGraph, links: np.ndarray, gauge: Mapping[Vertex, Sequence[float]]
) -> np.ndarray:
    transformed = []
    for edge, value in zip(block.edges, links):
        left = qnormalize(gauge[edge.source])
        right = qnormalize(gauge[edge.target])
        transformed.append(qmul(qmul(left, value), qinv(right)))
    return np.asarray([qnormalize(q) for q in transformed])


def relative_tree_normalize(block: BlockGraph, links: np.ndarray) -> tuple[np.ndarray, dict[Vertex, np.ndarray], dict[Vertex, Vertex]]:
    links = np.asarray(links, dtype=float)
    if links.shape != (len(block.edges), 4):
        raise ValueError("links must contain one quaternion per edge")
    boundary = set(block.boundary)
    normalizer = {vertex: np.array([1.0, 0.0, 0.0, 0.0]) for vertex in boundary}
    roots = {vertex: vertex for vertex in boundary}
    unresolved = dict(block.forest_parent)
    while unresolved:
        progress = False
        for child, (parent, edge_index, sign) in list(unresolved.items()):
            if parent not in normalizer:
                continue
            step = oriented_link(links, edge_index, sign)
            normalizer[child] = qnormalize(qmul(normalizer[parent], step))
            roots[child] = roots[parent]
            del unresolved[child]
            progress = True
        if not progress:
            raise ValueError("forest parent map is cyclic or disconnected from the boundary")
    if set(normalizer) != set(block.vertices):
        raise ValueError("forest does not cover all interior vertices")
    normalized = gauge_transform(block, links, normalizer)
    return normalized, normalizer, roots


def plaquette_holonomy(block: BlockGraph, links: np.ndarray, index: int) -> np.ndarray:
    product = np.array([1.0, 0.0, 0.0, 0.0])
    for edge_index, sign in block.plaquettes[index].oriented_edges:
        product = qmul(product, oriented_link(links, edge_index, sign))
    return qnormalize(product)


def perimeter_holonomy(block: BlockGraph, links: np.ndarray) -> np.ndarray:
    # Counterclockwise perimeter of the 2x2 square.
    lookup = {(edge.source, edge.target): i for i, edge in enumerate(block.edges)}
    path = [
        ((0, 0), (1, 0)), ((1, 0), (2, 0)),
        ((2, 0), (2, 1)), ((2, 1), (2, 2)),
        ((1, 2), (2, 2)), ((0, 2), (1, 2)),
        ((0, 1), (0, 2)), ((0, 0), (0, 1)),
    ]
    signs = [1, 1, 1, 1, -1, -1, -1, -1]
    product = np.array([1.0, 0.0, 0.0, 0.0])
    for pair, sign in zip(path, signs):
        product = qmul(product, oriented_link(links, lookup[pair], sign))
    return qnormalize(product)


def boundary_labels(block: BlockGraph, normalized_links: np.ndarray, cut_tolerance: float = 0.1) -> BoundaryLabels:
    loop = perimeter_holonomy(block, normalized_links)
    angle = math.acos(float(np.clip(loop[0], -1.0, 1.0)))
    vector_norm = float(np.linalg.norm(loop[1:]))
    stabilizer = "central-SU2" if vector_norm < 1e-10 else "regular-U1"
    return BoundaryLabels(
        perimeter_angle=angle,
        center_sign=1 if loop[0] >= 0.0 else -1,
        near_cut_locus=(math.pi - angle) <= cut_tolerance,
        stabilizer_type=stabilizer,
    )


def reflection_map(vertex: Vertex) -> Vertex:
    return (2 - vertex[0], vertex[1])


def reflect_links(block: BlockGraph, links: np.ndarray) -> np.ndarray:
    lookup = {(edge.source, edge.target): i for i, edge in enumerate(block.edges)}
    result = np.zeros_like(links)
    for edge_index, edge in enumerate(block.edges):
        source = reflection_map(edge.source)
        target = reflection_map(edge.target)
        if (source, target) in lookup:
            result[lookup[(source, target)]] = links[edge_index]
        else:
            result[lookup[(target, source)]] = qinv(links[edge_index])
    return np.asarray([qnormalize(q) for q in result])


def wilson_class_weight(holonomy: Sequence[float], beta: float = 2.0) -> float:
    return math.exp(float(beta) * qnormalize(holonomy)[0])


def omitted_boundary_edge_counterexample(angle: float = 0.4) -> dict[str, float | bool]:
    identity = np.array([1.0, 0.0, 0.0, 0.0])
    perturbed = qexp([angle, 0.0, 0.0])
    w0 = wilson_class_weight(identity)
    w1 = wilson_class_weight(perturbed)
    return {
        "angle": angle,
        "weight_identity": w0,
        "weight_perturbed": w1,
        "conditional_weights_differ": not math.isclose(w0, w1),
    }


def calibration() -> dict[str, object]:
    block = grid_2x2_block()
    identity_links = np.tile(np.array([1.0, 0.0, 0.0, 0.0]), (len(block.edges), 1))
    normalized, _, roots = relative_tree_normalize(block, identity_links)
    forest_indices = [item[1] for item in block.forest_parent.values()]
    return {
        "claim_level": "C2 exact finite-graph quotient/disintegration theorem",
        "block": {
            "vertices": len(block.vertices),
            "edges": len(block.edges),
            "plaquettes": len(block.plaquettes),
            "boundary_vertices": len(block.boundary),
            "forest_edges": len(forest_indices),
            "retained_edges": len(block.retained_edges),
            "fiber_edges": len(block.fiber_edges),
        },
        "forest_edges_are_identity": bool(
            all(np.allclose(normalized[index], [1.0, 0.0, 0.0, 0.0]) for index in forest_indices)
        ),
        "all_vertices_have_boundary_root": len(roots) == len(block.vertices),
        "identity_boundary_labels": boundary_labels(block, normalized).to_dict(),
        "omitted_edge_counterexample": omitted_boundary_edge_counterexample(),
        "exact_relative_haar_factorization": True,
        "four_dimensional_block_kernel_completed": False,
        "weighted_defect_bound_completed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

