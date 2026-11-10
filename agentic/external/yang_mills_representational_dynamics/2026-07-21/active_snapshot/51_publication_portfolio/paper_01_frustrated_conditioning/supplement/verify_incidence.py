#!/usr/bin/env python3
"""Exact cubical-incidence certificate for the central-frustration paper."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable


Vertex = tuple[int, ...]
Edge = tuple[Vertex, int]
Plaquette = tuple[Vertex, int, int]


def add_unit(vertex: Vertex, direction: int) -> Vertex:
    result = list(vertex)
    result[direction] += 1
    return tuple(result)


def build_edges(dimension: int) -> tuple[Edge, ...]:
    edges: list[Edge] = []
    for vertex in itertools.product(range(3), repeat=dimension):
        for direction in range(dimension):
            if vertex[direction] < 2:
                edges.append((vertex, direction))
    return tuple(edges)


def build_plaquettes(dimension: int) -> tuple[Plaquette, ...]:
    plaquettes: list[Plaquette] = []
    for vertex in itertools.product(range(3), repeat=dimension):
        for mu in range(dimension):
            for nu in range(mu + 1, dimension):
                if vertex[mu] < 2 and vertex[nu] < 2:
                    plaquettes.append((vertex, mu, nu))
    return tuple(plaquettes)


def boundary_edges(plaquette: Plaquette) -> tuple[Edge, Edge, Edge, Edge]:
    base, mu, nu = plaquette
    return (
        (base, mu),
        (add_unit(base, mu), nu),
        (add_unit(base, nu), mu),
        (base, nu),
    )


def gf2_rank(rows: Iterable[Iterable[int]]) -> int:
    matrix = [list(row) for row in rows]
    if not matrix:
        return 0
    width = len(matrix[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (r for r in range(pivot_row, len(matrix)) if matrix[r][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        for row in range(len(matrix)):
            if row != pivot_row and matrix[row][column]:
                matrix[row] = [a ^ b for a, b in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def dimension_certificate(dimension: int) -> dict[str, object]:
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    edges = build_edges(dimension)
    plaquettes = build_plaquettes(dimension)
    edge_index = {edge: index for index, edge in enumerate(edges)}
    selected: Edge = ((0,) + (1,) * (dimension - 1), 0)
    incident = tuple(p for p in plaquettes if selected in boundary_edges(p))
    remaining = tuple(edge for edge in edges if edge != selected)
    matrix = [
        [int(edge in boundary_edges(plaquette)) for edge in remaining]
        for plaquette in incident
    ]
    opposites: list[Edge] = []
    for plaquette in incident:
        candidates = [
            edge
            for edge in boundary_edges(plaquette)
            if edge[1] == 0 and edge != selected
        ]
        if len(candidates) != 1:
            raise AssertionError("an incident plaquette lacks a unique opposite edge")
        opposites.append(candidates[0])
    opposite_columns = [remaining.index(edge) for edge in opposites]
    minor = [[row[column] for column in opposite_columns] for row in matrix]
    expected_identity = [
        [int(row == column) for column in range(len(incident))]
        for row in range(len(incident))
    ]
    reversed_matrix = [list(reversed(row)) for row in reversed(matrix)]
    return {
        "dimension": dimension,
        "vertices": 3**dimension,
        "edges": len(edges),
        "plaquettes": len(plaquettes),
        "selected_edge": [list(selected[0]), selected[1]],
        "selected_edge_index": edge_index[selected],
        "incident_degree": len(incident),
        "expected_degree": 2 * (dimension - 1),
        "remaining_edge_variables": len(remaining),
        "gf2_rank": gf2_rank(matrix),
        "reversed_order_gf2_rank": gf2_rank(reversed_matrix),
        "private_opposite_edges": [[list(edge[0]), edge[1]] for edge in opposites],
        "private_opposites_distinct": len(set(opposites)) == len(opposites),
        "opposite_minor": minor,
        "opposite_minor_is_identity": minor == expected_identity,
        "surjective": gf2_rank(matrix) == len(incident),
    }


def build_certificate(min_dimension: int = 2, max_dimension: int = 6) -> dict[str, object]:
    if min_dimension < 2 or max_dimension < min_dimension:
        raise ValueError("invalid dimension interval")
    source = Path(__file__).read_bytes()
    dimensions = [
        dimension_certificate(dimension)
        for dimension in range(min_dimension, max_dimension + 1)
    ]
    return {
        "schema": "ym-frustrated-incidence-certificate-v1",
        "arithmetic": "exact integers and GF(2)",
        "verifier_sha256": hashlib.sha256(source).hexdigest(),
        "dimension_range": [min_dimension, max_dimension],
        "all_checks_pass": all(
            row["incident_degree"] == row["expected_degree"]
            and row["private_opposites_distinct"]
            and row["opposite_minor_is_identity"]
            and row["surjective"]
            and row["gf2_rank"] == row["reversed_order_gf2_rank"]
            for row in dimensions
        ),
        "dimensions": dimensions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-dimension", type=int, default=2)
    parser.add_argument("--max-dimension", type=int, default=6)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = build_certificate(args.min_dimension, args.max_dimension)
    rendered = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if certificate["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
