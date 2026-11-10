"""Exact certificates for the side-two four-dimensional block.

Floating-point linear algebra is used only to locate rational witnesses and
nonsingular minors.  Every published conclusion is then checked with integer
or rational arithmetic.  In particular, a decimal eigenvalue is never used as
a proof obligation.
"""
from __future__ import annotations

from fractions import Fraction as F
import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable

import numpy as np
import scipy.linalg


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "staple_dispersion_certificate.json"


def _shift(x: tuple[int, ...], direction: int) -> tuple[int, ...]:
    y = list(x)
    y[direction] += 1
    return tuple(y)


def block_incidence() -> tuple[np.ndarray, tuple, tuple, tuple]:
    """Return the integer coboundary d1 of the open side-two four-cube."""
    vertices = tuple(itertools.product(range(3), repeat=4))
    edges = tuple((x, mu) for x in vertices for mu in range(4) if x[mu] < 2)
    edge_index = {edge: i for i, edge in enumerate(edges)}
    plaquettes = tuple(
        (x, mu, nu)
        for x in vertices
        for mu in range(4)
        for nu in range(mu + 1, 4)
        if x[mu] < 2 and x[nu] < 2
    )
    d1 = np.zeros((len(plaquettes), len(edges)), dtype=int)
    for row, (x, mu, nu) in enumerate(plaquettes):
        d1[row, edge_index[(x, mu)]] = 1
        d1[row, edge_index[(_shift(x, mu), nu)]] = 1
        d1[row, edge_index[(_shift(x, nu), mu)]] = -1
        d1[row, edge_index[(x, nu)]] = -1
    return d1, vertices, edges, plaquettes


def interior_links(d1: np.ndarray) -> tuple[int, ...]:
    degree = np.sum(np.abs(d1) > 0, axis=0)
    return tuple(int(i) for i in np.flatnonzero(degree == 6))


def qmatrix(matrix: np.ndarray, denominator_bound: int) -> np.ndarray:
    return np.array(
        [[F(float(value)).limit_denominator(denominator_bound) for value in row]
         for row in matrix],
        dtype=object,
    )


def _all_zero(matrix: np.ndarray) -> bool:
    return all(value == 0 for value in matrix.flat)


def _matrix_strings(matrix: np.ndarray) -> list[list[str]]:
    return [[str(value) for value in row] for row in matrix]


def _poly_add(a: list[F], b: list[F]) -> list[F]:
    n = max(len(a), len(b))
    return [
        (a[i] if i < len(a) else F(0)) + (b[i] if i < len(b) else F(0))
        for i in range(n)
    ]


def _poly_mul(a: list[F], b: list[F]) -> list[F]:
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def _permutation_sign(perm: tuple[int, ...]) -> int:
    inversions = sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i + 1, len(perm)))
    return -1 if inversions % 2 else 1


def determinant_pencil(metric: np.ndarray, cost: np.ndarray) -> list[F]:
    """Return coefficients of det(lambda*metric-cost), low order first."""
    n = metric.shape[0]
    result = [F(0)]
    for perm in itertools.permutations(range(n)):
        term = [F(_permutation_sign(perm))]
        for i, j in enumerate(perm):
            term = _poly_mul(term, [-F(cost[i, j]), F(metric[i, j])])
        result = _poly_add(result, term)
    return result


def _expected_spill_polynomial() -> list[F]:
    # 6 (lambda-37/33)^3 (lambda-391/239)^2.
    out = [F(6)]
    for root in (F(37, 33), F(37, 33), F(37, 33), F(391, 239), F(391, 239)):
        out = _poly_mul(out, [-root, F(1)])
    return out


def projection_block_certificate(d1: np.ndarray, link: int) -> dict:
    """Certify S P S^T by the normal equations for the projection P."""
    selected = np.flatnonzero(np.abs(d1[:, link]) > 0)
    floating = np.asarray(d1, dtype=float)
    pseudo = np.linalg.pinv(floating, rcond=1.0e-12)
    lift = qmatrix(pseudo[:, selected], 100_000)
    d = np.array(d1, dtype=object)
    image = d @ lift
    coordinate = np.empty((d1.shape[0], 6), dtype=object)
    coordinate[:] = F(0)
    for j, row in enumerate(selected):
        coordinate[row, j] = F(1)
    in_image = _all_zero(d @ lift - image)
    orthogonal_residual = _all_zero(d.T @ (coordinate - image))
    if not (in_image and orthogonal_residual):
        raise ArithmeticError("rational projection witness failed")
    block = np.array([[image[selected[i], j] for j in range(6)] for i in range(6)], dtype=object)
    # Reorient every incident plaquette so that the distinguished link has
    # coefficient +1.  This is essential: the six complementary transports
    # (staples) live in one common bitorsor only after this reorientation.
    orientation = np.diag([int(d1[row, link]) for row in selected]).astype(object)
    oriented_block = orientation @ block @ orientation
    center = np.empty((6, 6), dtype=object)
    for i in range(6):
        for j in range(6):
            center[i, j] = F(5, 6) if i == j else F(-1, 6)
    centered = center @ oriented_block @ center
    # The ordering induced by the cubical complex has two oriented triples.
    expected = (F(0), F(239, 630), F(239, 630), F(33, 70), F(33, 70), F(33, 70))
    # Verify the characteristic polynomial directly rather than diagonalizing.
    metric = np.eye(6, dtype=object)
    characteristic = determinant_pencil(metric, centered)
    expected_poly = [F(1)]
    for root in expected:
        expected_poly = _poly_mul(expected_poly, [-root, F(1)])
    if characteristic != expected_poly:
        raise ArithmeticError("centered covariance characteristic polynomial failed")
    return {
        "link": int(link),
        "selected_plaquettes": [int(i) for i in selected],
        "projection_block": _matrix_strings(block),
        "oriented_projection_block": _matrix_strings(oriented_block),
        "centered_block": _matrix_strings(centered),
        "spectrum": [str(value) for value in expected],
        "normal_equations_verified_exactly": True,
        "characteristic_polynomial_verified_exactly": True,
        "maximum_lift_denominator": max(value.denominator for value in lift.flat),
    }


def _bareiss_solve(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Solve a nonsingular integer system by fraction-free elimination."""
    n = a.shape[0]
    m = b.shape[1]
    table = [list(map(int, a[i])) + list(map(int, b[i])) for i in range(n)]
    previous = 1
    for k in range(n - 1):
        if table[k][k] == 0:
            swap = next(i for i in range(k + 1, n) if table[i][k] != 0)
            table[k], table[swap] = table[swap], table[k]
        pivot = table[k][k]
        for i in range(k + 1, n):
            below = table[i][k]
            for j in range(k + 1, n + m):
                numerator = pivot * table[i][j] - below * table[k][j]
                quotient, remainder = divmod(numerator, previous)
                if remainder:
                    raise ArithmeticError("Bareiss division was not exact")
                table[i][j] = quotient
            table[i][k] = 0
        previous = pivot
    solution = np.empty((n, m), dtype=object)
    solution[:] = F(0)
    for i in range(n - 1, -1, -1):
        for j in range(m):
            rhs = F(table[i][n + j]) - sum(F(table[i][h]) * solution[h, j] for h in range(i + 1, n))
            solution[i, j] = rhs / F(table[i][i])
    return solution


def spillover_certificate(d1: np.ndarray, link: int) -> dict:
    """Certify the minimum external-curvature quadratic form for one star."""
    selected = np.flatnonzero(np.abs(d1[:, link]) > 0)
    external = np.setdiff1d(np.arange(d1.shape[0]), selected)
    columns = np.setdiff1d(np.arange(d1.shape[1]), [link])
    z = np.vstack((np.eye(5, dtype=int), -np.ones((1, 5), dtype=int)))
    metric = z.T @ z  # I+11^T, the Euclidean metric on centered star data.
    # If y=Z u, the centered star constraint R x=y is A x=u with A=A6/6.
    orientation = np.diag(d1[selected, link])
    oriented_star_map = orientation @ d1[np.ix_(selected, columns)]
    a6 = (6 * np.eye(5, dtype=int) - np.ones((5, 5), dtype=int)) @ z.T @ oriented_star_map
    external_map = d1[np.ix_(external, columns)]
    hessian = external_map.T @ external_map
    # Multiplying the KKT system by six makes every entry integral.
    kkt = np.block(
        [[6 * hessian, -a6.T], [a6, np.zeros((5, 5), dtype=int)]]
    )
    rhs = np.vstack((np.zeros((len(columns), 5), dtype=int), 6 * np.eye(5, dtype=int)))
    # Numerical pivoting only locates a full-rank minor; exact arithmetic below
    # proves that the resulting vector solves the complete singular system.
    _, triangular, column_pivots = scipy.linalg.qr(kkt.astype(float), pivoting=True, mode="economic")
    rank = int(np.sum(np.abs(np.diag(triangular)) > 1.0e-8))
    active_columns = column_pivots[:rank]
    _, row_triangular, row_pivots = scipy.linalg.qr(
        kkt[:, active_columns].T.astype(float), pivoting=True, mode="economic"
    )
    del row_triangular
    active_rows = row_pivots[:rank]
    reduced = kkt[np.ix_(active_rows, active_columns)]
    reduced_rhs = rhs[active_rows]
    reduced_solution = _bareiss_solve(reduced, reduced_rhs)
    solution = np.empty((kkt.shape[1], 5), dtype=object)
    solution[:] = F(0)
    for i, column in enumerate(active_columns):
        solution[column, :] = reduced_solution[i, :]
    if not _all_zero(np.array(kkt, dtype=object) @ solution - np.array(rhs, dtype=object)):
        raise ArithmeticError("complete KKT system did not verify")
    lift = solution[: len(columns)]
    b = np.array(external_map, dtype=object)
    cost = lift.T @ (b.T @ b) @ lift
    polynomial = determinant_pencil(np.array(metric, dtype=object), cost)
    if polynomial != _expected_spill_polynomial():
        raise ArithmeticError("spillover generalized characteristic polynomial failed")
    return {
        "link": int(link),
        "selected_plaquettes": [int(i) for i in selected],
        "external_plaquettes": int(len(external)),
        "available_noncentral_links": int(len(columns)),
        "kkt_rank": rank,
        "centered_coordinate_metric": _matrix_strings(np.array(metric, dtype=object)),
        "minimum_cost_matrix": _matrix_strings(cost),
        "generalized_spectrum": ["37/33", "37/33", "37/33", "391/239", "391/239"],
        "complete_kkt_system_verified_exactly": True,
        "characteristic_polynomial_verified_exactly": True,
        "maximum_lift_denominator": max(value.denominator for value in lift.flat),
    }


def build_certificate() -> dict:
    d1, vertices, edges, plaquettes = block_incidence()
    links = interior_links(d1)
    covariance = [projection_block_certificate(d1, link) for link in links]
    spillover = [spillover_certificate(d1, link) for link in links]
    return {
        "schema_version": 1,
        "arithmetic_contract": "floating point locates witnesses/minors; all theorem outputs pass exact rational identities",
        "block": {
            "vertices": len(vertices),
            "links": len(edges),
            "plaquettes": len(plaquettes),
            "interior_links": len(links),
            "curvature_rank": int(np.linalg.matrix_rank(d1.astype(float), tol=1.0e-10)),
            "d1_sha256": hashlib.sha256(d1.tobytes()).hexdigest(),
        },
        "centered_gaussian_covariance": {
            "certificates": covariance,
            "common_spectrum": ["0", "239/630", "239/630", "33/70", "33/70", "33/70"],
            "all_interior_links_certified": True,
        },
        "minimal_external_spillover": {
            "certificates": spillover,
            "common_generalized_spectrum": ["37/33", "37/33", "37/33", "391/239", "391/239"],
            "all_interior_links_certified": True,
        },
        "scope": {
            "finite_open_block": True,
            "linearized_about_identity": True,
            "nonlinear_measure_comparison": False,
            "continuum_or_mass_gap": False,
        },
    }


def verify_certificate(data: dict) -> None:
    fresh = build_certificate()
    if data != fresh:
        raise AssertionError("stored certificate differs from exact recomputation")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write the canonical JSON certificate")
    parser.add_argument("--verify", action="store_true", help="compare against the stored certificate")
    args = parser.parse_args()
    data = build_certificate()
    if args.write:
        CERTIFICATE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.verify:
        stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        if stored != data:
            raise AssertionError("stored certificate differs from exact recomputation")
    print(json.dumps({
        "block": data["block"],
        "gaussian_spectrum": data["centered_gaussian_covariance"]["common_spectrum"],
        "spillover_spectrum": data["minimal_external_spillover"]["common_generalized_spectrum"],
        "verified": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
