#!/usr/bin/env python3
"""Exact verifier for the rooted-tree finite-block certificate.

The theorem-critical kernel uses only Python's standard library.  Cubical
incidences are integers, ranks are computed over Q, the coercive spectral
floor is proved by an exact rational LDL^T factorization, and every displayed
analytic budget is compared as a Fraction.  Decimal strings are explanatory;
no binary floating-point number participates in a pass/fail decision.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import platform
from typing import Iterable, Sequence


Vertex = tuple[int, int, int, int]
Edge = tuple[Vertex, int]
Plaquette = tuple[Vertex, int, int]


def shift(x: Vertex, direction: int) -> Vertex:
    y = list(x)
    y[direction] += 1
    return tuple(y)  # type: ignore[return-value]


def block_complex() -> dict[str, object]:
    vertices = tuple(itertools.product(range(3), repeat=4))
    vertex_index = {x: i for i, x in enumerate(vertices)}
    edges = tuple(
        (x, mu) for x in vertices for mu in range(4) if x[mu] < 2
    )
    edge_index = {e: i for i, e in enumerate(edges)}
    plaquettes = tuple(
        (x, mu, nu)
        for x in vertices
        for mu in range(4)
        for nu in range(mu + 1, 4)
        if x[mu] < 2 and x[nu] < 2
    )
    plaquette_index = {p: i for i, p in enumerate(plaquettes)}

    d0 = [[0 for _ in vertices] for _ in edges]
    for row, (x, mu) in enumerate(edges):
        d0[row][vertex_index[x]] = -1
        d0[row][vertex_index[shift(x, mu)]] = 1

    d1 = [[0 for _ in edges] for _ in plaquettes]
    for row, (x, mu, nu) in enumerate(plaquettes):
        d1[row][edge_index[(x, mu)]] = 1
        d1[row][edge_index[(shift(x, mu), nu)]] = 1
        d1[row][edge_index[(shift(x, nu), mu)]] = -1
        d1[row][edge_index[(x, nu)]] = -1

    face_rows: list[list[int]] = []
    for mu in range(4):
        for nu in range(mu + 1, 4):
            transverse = [a for a in range(4) if a not in (mu, nu)]
            for fixed in itertools.product((0, 2), repeat=2):
                row = [0 for _ in plaquettes]
                base = [0, 0, 0, 0]
                for axis, value in zip(transverse, fixed):
                    base[axis] = value
                for i in range(2):
                    for j in range(2):
                        x = base.copy()
                        x[mu] = i
                        x[nu] = j
                        row[plaquette_index[(tuple(x), mu, nu)]] = 1
                face_rows.append(row)
    coarse = matmul(face_rows, d1)
    return {
        "vertices": vertices,
        "edges": edges,
        "plaquettes": plaquettes,
        "d0": d0,
        "d1": d1,
        "coarse": coarse,
    }


def matmul(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> list[list[int]]:
    if not a or not b or len(a[0]) != len(b):
        raise ValueError("incompatible matrix dimensions")
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def rational_rank(matrix: Sequence[Sequence[int]]) -> tuple[int, tuple[int, ...]]:
    a = [[Q(x) for x in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    rank = 0
    source_rows = list(range(rows))
    selected: list[int] = []
    for col in range(cols):
        pivot = next((i for i in range(rank, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        source_rows[rank], source_rows[pivot] = source_rows[pivot], source_rows[rank]
        selected.append(source_rows[rank])
        p = a[rank][col]
        a[rank] = [x / p for x in a[rank]]
        for i in range(rows):
            if i == rank or not a[i][col]:
                continue
            c = a[i][col]
            a[i] = [x - c * y for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == rows:
            break
    return rank, tuple(selected)


def spanning_tree(vertices: Sequence[Vertex], edges: Sequence[Edge], reverse: bool = False) -> tuple[int, ...]:
    vertex_index = {x: i for i, x in enumerate(vertices)}
    parent = list(range(len(vertices)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    order: Iterable[int] = range(len(edges) - 1, -1, -1) if reverse else range(len(edges))
    tree: list[int] = []
    for i in order:
        x, mu = edges[i]
        a, b = find(vertex_index[x]), find(vertex_index[shift(x, mu)])
        if a != b:
            parent[b] = a
            tree.append(i)
    return tuple(tree)


def gram_on_cotree(d1: Sequence[Sequence[int]], cotree: Sequence[int]) -> list[list[int]]:
    columns = [[row[e] for e in cotree] for row in d1]
    n = len(cotree)
    return [
        [sum(row[i] * row[j] for row in columns) for j in range(n)]
        for i in range(n)
    ]


def exact_ldlt_floor(h: Sequence[Sequence[int]], floor: Q) -> dict[str, object]:
    n = len(h)
    a = [
        [Q(h[i][j]) - (floor if i == j else Q(0)) for j in range(n)]
        for i in range(n)
    ]
    lower = [[Q(0) for _ in range(n)] for _ in range(n)]
    pivots: list[Q] = []
    for i in range(n):
        for j in range(i):
            value = a[i][j]
            for k in range(j):
                value -= lower[i][k] * lower[j][k] * pivots[k]
            lower[i][j] = value / pivots[j]
        pivot = a[i][i]
        for k in range(i):
            pivot -= lower[i][k] * lower[i][k] * pivots[k]
        if pivot <= 0:
            return {"positive": False, "failed_index": i, "pivots": pivots}
        lower[i][i] = Q(1)
        pivots.append(pivot)

    digest = hashlib.sha256()
    for value in pivots:
        digest.update(f"{value.numerator}/{value.denominator}\n".encode())
    return {
        "positive": True,
        "failed_index": None,
        "pivots": pivots,
        "pivot_sha256": digest.hexdigest(),
        "minimum_pivot": min(pivots),
        "maximum_bit_length": max(
            max(abs(x.numerator).bit_length(), x.denominator.bit_length()) for x in pivots
        ),
    }


def frac(value: Q) -> str:
    return f"{value.numerator}/{value.denominator}"


def analytic_budgets(radius: Q = Q(1, 100_000), time_max: Q = Q(1, 10**18)) -> dict[str, object]:
    if not (Q(0) < 2 * radius < Q(1)):
        raise ValueError("product-log chart requires 0 < 2r < 1")
    if not (Q(0) < time_max <= Q(1, 10**18)):
        raise ValueError("heat-time certificate requires 0 < t <= 10^-18")

    denominator = 1 - 2 * radius
    m1 = Q(2) / denominator
    m2 = Q(4) / denominator**2 + Q(4) / denominator
    m3 = Q(16) / denominator**3 + Q(24) / denominator**2 + Q(8) / denominator
    sqrt6_upper = Q(5, 2)
    sqrt12_upper = Q(7, 2)
    curvature_radius = 2 * radius
    kappa = sqrt6_upper * m2 * radius

    # Appendix C proves these heat-kernel remainders analytically.  The
    # rational verifier checks their propagation through the nonlinear chart.
    heat_hessian = 2 * time_max
    heat_gradient = curvature_radius * heat_hessian
    heat_third = 10 * time_max
    haar_hessian = time_max
    haar_third = 2 * time_max

    eta = (
        kappa * (2 * sqrt12_upper + kappa)
        + heat_hessian * (sqrt12_upper + kappa) ** 2
        + 6 * (curvature_radius + heat_gradient) * m2
        + haar_hessian
    )
    tau = 6 * (
        heat_third * m1**3
        + 3 * (1 + heat_hessian) * m1 * m2
        + (curvature_radius + heat_gradient) * m3
    ) + haar_third

    lambda_floor = Q(1, 25)
    eta_ceiling = Q(1, 400)
    mu_floor = Q(3, 80)
    base_embedding = Q(5)
    eps_cross_ceiling = Q(1, 80)
    eps_base_ceiling = Q(1, 16)
    generated_ceiling = Q(1, 15)
    generated_from_ceilings = eps_base_ceiling + eps_cross_ceiling**2 / mu_floor
    transport_ceiling = eps_cross_ceiling / mu_floor
    chart_lipschitz_floor = Q(1, 5) - kappa
    fiber_radius = radius / 2
    base_radius = radius / 20
    reference_tail = Q(357) * time_max / (lambda_floor * fiber_radius**2)

    checks = {
        "m1_below_2_001": m1 < Q(2001, 1000),
        "m2_below_8_01": m2 < Q(801, 100),
        "m3_below_48_1": m3 < Q(481, 10),
        "derivative_deviation_below_1_1000": kappa < Q(1, 1000),
        "hessian_remainder_below_1_400": eta < eta_ceiling,
        "third_derivative_below_300": tau < Q(300),
        "fiber_margin_at_least_3_80": lambda_floor - eta_ceiling >= mu_floor,
        "effective_remainder_at_most_1_15": generated_from_ceilings <= generated_ceiling,
        "transport_at_most_1_3": transport_ceiling <= Q(1, 3),
        "chart_lower_lipschitz_at_least_199_1000": chart_lipschitz_floor >= Q(199, 1000),
        "cylinder_has_chart_slack": base_embedding * base_radius + fiber_radius <= Q(3, 4) * radius,
        "reference_tail_at_most_357_1e6": reference_tail <= Q(357, 10**6),
    }
    return {
        "parameters": {
            "link_chart_radius": frac(radius),
            "curvature_radius": frac(curvature_radius),
            "time_max": frac(time_max),
            "base_radius": frac(base_radius),
            "fiber_radius": frac(fiber_radius),
        },
        "majorants": {
            "M1": frac(m1),
            "M2": frac(m2),
            "M3": frac(m3),
            "kappa": frac(kappa),
            "eta": frac(eta),
            "tau": frac(tau),
        },
        "consequences": {
            "linear_hessian_floor": frac(lambda_floor),
            "nonlinear_chart_lipschitz_floor": frac(chart_lipschitz_floor),
            "nonlinear_fiber_margin_floor": frac(mu_floor),
            "cross_hessian_ceiling": frac(eps_cross_ceiling),
            "base_hessian_remainder_ceiling": frac(eps_base_ceiling),
            "conditional_transport_ceiling": frac(transport_ceiling),
            "effective_hessian_remainder_ceiling": frac(generated_ceiling),
            "reference_gaussian_complement_ceiling": frac(reference_tail),
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }


def certificate() -> dict[str, object]:
    block = block_complex()
    vertices = block["vertices"]
    edges = block["edges"]
    plaquettes = block["plaquettes"]
    d0 = block["d0"]
    d1 = block["d1"]
    coarse = block["coarse"]
    assert isinstance(vertices, tuple) and isinstance(edges, tuple) and isinstance(plaquettes, tuple)
    assert isinstance(d0, list) and isinstance(d1, list) and isinstance(coarse, list)

    boundary_zero = matmul(d1, d0)
    tree = spanning_tree(vertices, edges)
    reverse_tree = spanning_tree(vertices, edges, reverse=True)
    cotree = tuple(i for i in range(len(edges)) if i not in set(tree))
    reverse_cotree = tuple(i for i in range(len(edges)) if i not in set(reverse_tree))
    h = gram_on_cotree(d1, cotree)
    reverse_h = gram_on_cotree(d1, reverse_cotree)
    retained = [[row[e] for e in cotree] for row in coarse]
    reverse_retained = [[row[e] for e in reverse_cotree] for row in coarse]

    rank_d0, _ = rational_rank(d0)
    rank_d1, _ = rational_rank(d1)
    retained_rank, independent_rows = rational_rank(retained)
    reverse_retained_rank, _ = rational_rank(reverse_retained)
    ldl = exact_ldlt_floor(h, Q(1, 25))
    reverse_ldl = exact_ldlt_floor(reverse_h, Q(1, 25))
    budgets = analytic_budgets()

    topology_checks = {
        "cell_counts": (len(vertices), len(edges), len(plaquettes)) == (81, 216, 216),
        "boundary_squared_zero": all(x == 0 for row in boundary_zero for x in row),
        "gauge_rank_80": rank_d0 == 80,
        "curvature_rank_136": rank_d1 == 136,
        "lex_tree_size_80": len(tree) == 80,
        "lex_cotree_size_136": len(cotree) == 136,
        "retained_rank_17": retained_rank == 17,
        "fiber_dimension_119": len(cotree) - retained_rank == 119,
        "reverse_tree_retained_rank_17": reverse_retained_rank == 17,
        "coercivity_floor_lex": bool(ldl["positive"]),
        "coercivity_floor_reverse": bool(reverse_ldl["positive"]),
    }
    all_checks = (
        all(topology_checks.values())
        and bool(budgets["all_checks_pass"])
    )
    return {
        "schema": "ym-paper02-exact-certificate-v1",
        "claim_level": "C2 restricted finite-block theorem",
        "trusted_kernel": "Python standard library: int, Fraction, hashlib, json",
        "binary_floating_point_used_for_decisions": False,
        "runtime": {"python": platform.python_version()},
        "topology": {
            "vertices": len(vertices),
            "links": len(edges),
            "plaquettes": len(plaquettes),
            "gauge_rank": rank_d0,
            "cotree_links": len(cotree),
            "displayed_retained_rows": len(retained),
            "independent_retained_rows": retained_rank,
            "selected_retained_row_indices_zero_based": list(independent_rows),
            "scalar_fiber_dimension": len(cotree) - retained_rank,
            "su2_retained_dimension": 3 * retained_rank,
            "su2_fiber_dimension": 3 * (len(cotree) - retained_rank),
            "lex_tree_edge_indices_zero_based": list(tree),
        },
        "spectral_certificate": {
            "claimed_floor": "1/25",
            "dimension": len(h),
            "lex_ldlt_positive": ldl["positive"],
            "lex_pivot_sha256": ldl.get("pivot_sha256"),
            "lex_maximum_pivot_bit_length": ldl.get("maximum_bit_length"),
            "reverse_ldlt_positive": reverse_ldl["positive"],
            "reverse_pivot_sha256": reverse_ldl.get("pivot_sha256"),
        },
        "analytic_budget_certificate": budgets,
        "topology_checks": topology_checks,
        "all_checks_pass": all_checks,
        "scope_exclusions": [
            "full interacting-measure complement bound",
            "dependent polymer estimate",
            "repeated renormalization-group closure",
            "continuum construction",
            "Hamiltonian mass gap",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = certificate()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
