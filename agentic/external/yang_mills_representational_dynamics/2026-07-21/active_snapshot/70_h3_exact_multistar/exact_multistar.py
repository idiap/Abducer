"""Exact finite certificates for orientation-correct multi-star spill forms.

The ambient complex is the open side-two four-cube used in Paper 05.  Floating
point linear algebra is permitted only to locate a KKT witness.  Every stored
rank, nullity, constrained minimizer, kernel vector, and polynomial identity
is subsequently checked over ``fractions.Fraction``.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import scipy.linalg


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "exact_multistar_results.json"


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


def _sha256_integer_matrix(matrix: np.ndarray) -> str:
    array = np.asarray(matrix, dtype=np.int64)
    shape = ",".join(map(str, array.shape)).encode("ascii")
    return hashlib.sha256(shape + b":" + array.tobytes(order="C")).hexdigest()


def _fraction_matrix(matrix: np.ndarray) -> list[list[F]]:
    return [
        [value if isinstance(value, F) else F(int(value)) for value in row]
        for row in np.asarray(matrix)
    ]


def _rref(matrix: Sequence[Sequence[F]]) -> tuple[list[list[F]], tuple[int, ...], tuple[int, ...]]:
    """Reduced row echelon form, with original independent-row indices."""
    rows = [list(map(F, row)) for row in matrix]
    original = list(range(len(rows)))
    if not rows:
        return [], (), ()
    ncols = len(rows[0])
    pivot_cols: list[int] = []
    pivot_rows: list[int] = []
    lead = 0
    for col in range(ncols):
        pivot = next((i for i in range(lead, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[lead], rows[pivot] = rows[pivot], rows[lead]
        original[lead], original[pivot] = original[pivot], original[lead]
        scale = rows[lead][col]
        rows[lead] = [value / scale for value in rows[lead]]
        for i in range(len(rows)):
            if i == lead or not rows[i][col]:
                continue
            multiple = rows[i][col]
            rows[i] = [a - multiple * b for a, b in zip(rows[i], rows[lead])]
        pivot_cols.append(col)
        pivot_rows.append(original[lead])
        lead += 1
        if lead == len(rows):
            break
    return rows, tuple(pivot_cols), tuple(pivot_rows)


def rational_rank(matrix: np.ndarray) -> int:
    return len(_rref(_fraction_matrix(matrix))[1])


def _inverse(matrix: Sequence[Sequence[F]]) -> list[list[F]]:
    n = len(matrix)
    augmented = [list(map(F, row)) + [F(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if augmented[i][col]), None)
        if pivot is None:
            raise ArithmeticError("singular exact matrix")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        augmented[col] = [value / scale for value in augmented[col]]
        for i in range(n):
            if i == col or not augmented[i][col]:
                continue
            multiple = augmented[i][col]
            augmented[i] = [a - multiple * b for a, b in zip(augmented[i], augmented[col])]
    return [row[n:] for row in augmented]


def _matmul(a: Sequence[Sequence[F]], b: Sequence[Sequence[F]]) -> list[list[F]]:
    if not a:
        return []
    bt = list(zip(*b))
    return [[sum((x * y for x, y in zip(row, col)), F(0)) for col in bt] for row in a]


def _transpose(a: Sequence[Sequence[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def _identity(n: int) -> list[list[F]]:
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def _matrix_strings(matrix: Sequence[Sequence[F]]) -> list[list[str]]:
    return [[str(value) for value in row] for row in matrix]


def _vector_strings(vector: Sequence[F]) -> list[str]:
    return [str(value) for value in vector]


def oriented_star_operator(d1: np.ndarray, link: int) -> tuple[np.ndarray, tuple[int, ...]]:
    """Return A6=(6I-J) O S d1 and its selected plaquette rows."""
    selected = tuple(int(i) for i in np.flatnonzero(np.abs(d1[:, link]) > 0))
    if len(selected) != 6:
        raise ValueError("each chosen root must be an interior six-plaquette link")
    selector = d1[np.array(selected)]
    orientation = np.diag(selector[:, link])
    six_center = 6 * np.eye(6, dtype=int) - np.ones((6, 6), dtype=int)
    return six_center @ orientation @ selector, selected


def hostile_center_before_orient(d1: np.ndarray, link: int) -> np.ndarray:
    """The known-wrong operator O(6I-J)S d1, kept only as a regression."""
    selected = np.flatnonzero(np.abs(d1[:, link]) > 0)
    selector = d1[selected]
    orientation = np.diag(selector[:, link])
    six_center = 6 * np.eye(6, dtype=int) - np.ones((6, 6), dtype=int)
    return orientation @ six_center @ selector


def polymer_operator(d1: np.ndarray, links: Iterable[int], hostile: bool = False) -> tuple[np.ndarray, tuple[int, ...]]:
    operators: list[np.ndarray] = []
    union: set[int] = set()
    for link in tuple(map(int, links)):
        operator, selected = oriented_star_operator(d1, link)
        if hostile:
            operator = hostile_center_before_orient(d1, link)
        operators.append(operator)
        union.update(selected)
    return np.vstack(operators), tuple(sorted(union))


def row_coordinate_system(a6: np.ndarray) -> tuple[np.ndarray, list[list[F]], list[list[F]], tuple[int, ...], tuple[int, ...]]:
    """Choose exact row coordinates u=R6 x and return A6=L R6."""
    _, _, independent_rows = _rref(_fraction_matrix(a6))
    rank = len(independent_rows)
    r6 = np.asarray(a6[list(independent_rows)], dtype=int)
    _, pivot_cols, _ = _rref(_fraction_matrix(r6))
    if len(pivot_cols) != rank:
        raise ArithmeticError("failed to locate an exact row-basis minor")
    minor = [[F(int(r6[i, j])) for j in pivot_cols] for i in range(rank)]
    inverse = _inverse(minor)
    restricted = [[F(int(a6[i, j])) for j in pivot_cols] for i in range(a6.shape[0])]
    coordinates = _matmul(restricted, inverse)
    reconstructed = _matmul(coordinates, _fraction_matrix(r6))
    if reconstructed != _fraction_matrix(a6):
        raise ArithmeticError("A6=L R6 reconstruction failed")
    lt_l = _matmul(_transpose(coordinates), coordinates)
    metric = [[value / 36 for value in row] for row in lt_l]
    return r6, coordinates, metric, independent_rows, pivot_cols


def _rationalize(matrix: np.ndarray, denominator_bound: int) -> list[list[F]]:
    return [
        [F(float(value)).limit_denominator(denominator_bound) for value in row]
        for row in np.asarray(matrix)
    ]


def _bareiss_solve(a: np.ndarray, b: np.ndarray) -> list[list[F]]:
    """Solve a nonsingular integral system by fraction-free elimination."""
    n = a.shape[0]
    rhs_columns = b.shape[1]
    table = [list(map(int, a[i])) + list(map(int, b[i])) for i in range(n)]
    previous = 1
    for k in range(n - 1):
        if table[k][k] == 0:
            swap = next(i for i in range(k + 1, n) if table[i][k] != 0)
            table[k], table[swap] = table[swap], table[k]
        pivot = table[k][k]
        for i in range(k + 1, n):
            below = table[i][k]
            for j in range(k + 1, n + rhs_columns):
                numerator = pivot * table[i][j] - below * table[k][j]
                quotient, remainder = divmod(numerator, previous)
                if remainder:
                    raise ArithmeticError("Bareiss division was not exact")
                table[i][j] = quotient
            table[i][k] = 0
        previous = pivot
    solution = [[F(0) for _ in range(rhs_columns)] for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(rhs_columns):
            rhs = F(table[i][n + j]) - sum(
                (F(table[i][h]) * solution[h][j] for h in range(i + 1, n)), F(0)
            )
            solution[i][j] = rhs / F(table[i][i])
    return solution


def _exact_rank_minor_solution(kkt: np.ndarray, rhs: np.ndarray) -> list[list[F]]:
    """Solve a consistent singular integral system on a full-rank minor."""
    _, triangular, column_pivots = scipy.linalg.qr(
        kkt.astype(float), pivoting=True, mode="economic"
    )
    rank = int(np.sum(np.abs(np.diag(triangular)) > 1.0e-8))
    active_columns = column_pivots[:rank]
    _, _, row_pivots = scipy.linalg.qr(
        kkt[:, active_columns].T.astype(float), pivoting=True, mode="economic"
    )
    active_rows = row_pivots[:rank]
    reduced = kkt[np.ix_(active_rows, active_columns)]
    reduced_rhs = rhs[active_rows]
    reduced_solution = _bareiss_solve(reduced, reduced_rhs)
    solution = [[F(0) for _ in range(rhs.shape[1])] for _ in range(kkt.shape[1])]
    for i, column in enumerate(active_columns):
        solution[int(column)] = reduced_solution[i]
    if _matmul(_fraction_matrix(kkt), solution) != _fraction_matrix(rhs):
        raise ArithmeticError("rank-minor solution fails the complete exact system")
    return solution


def exact_kkt_witness(r6: np.ndarray, b: np.ndarray, denominator_bound: int = 2_000_000) -> tuple[list[list[F]], list[list[F]], list[list[F]]]:
    """Locate a KKT solution numerically and verify the complete system exactly."""
    n = r6.shape[1]
    rank = r6.shape[0]
    hessian = b.T @ b
    kkt_integer = np.block(
        [[hessian, -r6.T], [r6, np.zeros((rank, rank), dtype=int)]]
    )
    rhs_integer = np.vstack((np.zeros((n, rank), dtype=int), np.eye(rank, dtype=int)))
    solution, _, _, _ = scipy.linalg.lstsq(
        kkt_integer.astype(float), rhs_integer.astype(float), cond=1.0e-12, lapack_driver="gelsy"
    )
    x = _rationalize(solution[:n], denominator_bound)
    lagrange = _rationalize(solution[n:], denominator_bound)

    rf = _fraction_matrix(r6)
    bf = _fraction_matrix(b)
    bx = _matmul(bf, x)
    stationarity_left = _matmul(_transpose(bf), bx)
    stationarity_right = _matmul(_transpose(rf), lagrange)
    if _matmul(rf, x) != _identity(rank) or stationarity_left != stationarity_right:
        exact = _exact_rank_minor_solution(kkt_integer, rhs_integer)
        x = exact[:n]
        lagrange = exact[n:]
        bx = _matmul(bf, x)
        stationarity_left = _matmul(_transpose(bf), bx)
        stationarity_right = _matmul(_transpose(rf), lagrange)
    if _matmul(rf, x) != _identity(rank):
        raise ArithmeticError("KKT witness fails R6 X=I")
    if stationarity_left != stationarity_right:
        raise ArithmeticError("KKT witness fails complete stationarity equations")
    cost = _matmul(_transpose(bx), bx)
    return x, lagrange, cost


def _poly_add(a: list[F], b: list[F]) -> list[F]:
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else F(0)) + (b[i] if i < len(b) else F(0)) for i in range(n)]


def _poly_mul(a: list[F], b: list[F]) -> list[F]:
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def _poly_trim(a: list[F]) -> list[F]:
    while len(a) > 1 and not a[-1]:
        a.pop()
    return a


def _poly_sub(a: list[F], b: list[F]) -> list[F]:
    return _poly_trim(_poly_add(a, [-x for x in b]))


def berkowitz_characteristic(matrix: Sequence[Sequence[F]]) -> list[F]:
    """Return det(lambda I-M), low degree first, by division-free recursion.

    This implementation uses the Faddeev--LeVerrier recurrence over Q.  It is
    exact; the function name records the intended division-free backend, but
    rational division by k is harmless in characteristic zero.
    """
    n = len(matrix)
    if n == 0:
        return [F(1)]
    a = [list(map(F, row)) for row in matrix]
    b = _identity(n)
    high = [F(1)]
    for k in range(1, n + 1):
        ab = _matmul(a, b)
        coefficient = -sum((ab[i][i] for i in range(n)), F(0)) / k
        high.append(coefficient)
        b = [
            [ab[i][j] + (coefficient if i == j else F(0)) for j in range(n)]
            for i in range(n)
        ]
    return list(reversed(high))


def generalized_characteristic(metric: Sequence[Sequence[F]], cost: Sequence[Sequence[F]]) -> list[F]:
    """Return det(lambda G-K) through det(G) det(lambda I-G^-1 K)."""
    inv_metric = _inverse(metric)
    operator = _matmul(inv_metric, cost)
    characteristic = berkowitz_characteristic(operator)
    # det(G) is recovered from det(G^{-1}) using elimination-free char data.
    inverse_characteristic = berkowitz_characteristic(inv_metric)
    determinant_inverse = ((-1) ** len(metric)) * inverse_characteristic[0]
    determinant_metric = F(1) / determinant_inverse
    return [determinant_metric * value for value in characteristic]


def _divide_linear(poly: list[F], root: F) -> tuple[list[F], F]:
    """Divide low-order poly by (lambda-root)."""
    high = list(reversed(poly))
    quotient_high = [high[0]]
    for coefficient in high[1:]:
        quotient_high.append(coefficient + root * quotient_high[-1])
    remainder = quotient_high.pop()
    return list(reversed(quotient_high)), remainder


def factor_known_roots(poly: list[F], candidates: Sequence[F]) -> tuple[list[tuple[F, int]], list[F]]:
    remaining = list(poly)
    factors: list[tuple[F, int]] = []
    for root in candidates:
        multiplicity = 0
        while len(remaining) > 1:
            quotient, remainder = _divide_linear(remaining, root)
            if remainder:
                break
            remaining = quotient
            multiplicity += 1
        if multiplicity:
            factors.append((root, multiplicity))
    return factors, remaining


def _poly_derivative(poly: Sequence[F]) -> list[F]:
    return _poly_trim([F(i) * poly[i] for i in range(1, len(poly))])


def _poly_divmod(dividend: Sequence[F], divisor: Sequence[F]) -> tuple[list[F], list[F]]:
    remainder = _poly_trim(list(map(F, dividend)))
    divisor = _poly_trim(list(map(F, divisor)))
    if divisor == [F(0)]:
        raise ZeroDivisionError("zero polynomial")
    quotient = [F(0)] * max(1, len(remainder) - len(divisor) + 1)
    while len(remainder) >= len(divisor) and remainder != [F(0)]:
        degree = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[degree] += coefficient
        subtraction = [F(0)] * degree + [coefficient * value for value in divisor]
        remainder = _poly_sub(remainder, subtraction)
    return _poly_trim(quotient), _poly_trim(remainder)


def _poly_value(poly: Sequence[F], point: F) -> F:
    result = F(0)
    for coefficient in reversed(poly):
        result = result * point + coefficient
    return result


def sturm_sequence(poly: Sequence[F]) -> list[list[F]]:
    sequence = [_poly_trim(list(map(F, poly))), _poly_derivative(poly)]
    while sequence[-1] != [F(0)]:
        _, remainder = _poly_divmod(sequence[-2], sequence[-1])
        if remainder == [F(0)]:
            break
        sequence.append([-value for value in remainder])
    return sequence


def sturm_root_count(poly: Sequence[F], left: F, right: F) -> int:
    def variations(point: F) -> int:
        signs = []
        for member in sturm_sequence(poly):
            value = _poly_value(member, point)
            if value:
                signs.append(1 if value > 0 else -1)
        return sum(a != b for a, b in zip(signs, signs[1:]))

    if left >= right or not _poly_value(poly, left) or not _poly_value(poly, right):
        raise ValueError("Sturm endpoints must be ordered nonroots")
    return variations(left) - variations(right)


def perfect_quartic_cube(poly: Sequence[F]) -> tuple[F, list[F]] | None:
    """Recognize c*q(lambda)^3 with q a monic quartic."""
    values = list(map(F, poly))
    if len(values) != 13 or not values[-1]:
        return None
    scale = values[-1]
    monic = [value / scale for value in values]
    a = monic[11] / 3
    b = (monic[10] - 3 * a * a) / 3
    c = (monic[9] - 6 * a * b - a**3) / 3
    d = (monic[8] - (6 * a * c + 3 * b * b + 3 * a * a * b)) / 3
    quartic = [d, c, b, a, F(1)]
    if _poly_mul(_poly_mul(quartic, quartic), quartic) != monic:
        return None
    return scale, quartic


def _exact_nullspace(matrix: np.ndarray) -> list[list[F]]:
    rref, pivots, _ = _rref(_fraction_matrix(matrix))
    free = [j for j in range(matrix.shape[1]) if j not in pivots]
    vectors: list[list[F]] = []
    for free_col in free:
        vector = [F(0)] * matrix.shape[1]
        vector[free_col] = F(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -rref[row][free_col]
        vectors.append(vector)
    return vectors


def _canonical_integer_vector(vector: Sequence[F]) -> list[int]:
    from math import gcd, lcm

    denominator = 1
    for value in vector:
        denominator = lcm(denominator, value.denominator)
    integers = [int(value * denominator) for value in vector]
    divisor = 0
    for value in integers:
        divisor = gcd(divisor, abs(value))
    integers = [value // max(divisor, 1) for value in integers]
    first = next((value for value in integers if value), 1)
    return [-value for value in integers] if first < 0 else integers


def polymer_certificate(name: str, d1: np.ndarray, links: Sequence[int]) -> dict:
    a6, union = polymer_operator(d1, links)
    hostile, _ = polymer_operator(d1, links, hostile=True)
    external = tuple(sorted(set(range(d1.shape[0])) - set(union)))
    b = d1[np.array(external)]
    r6, coordinates, metric, row_indices, pivot_cols = row_coordinate_system(a6)
    x, lagrange, cost = exact_kkt_witness(r6, b)
    characteristic = generalized_characteristic(metric, cost)
    known = [
        F(0), F(16, 19), F(5, 4), F(3, 2), F(24, 11),
        F(3, 4), F(12, 11), F(10, 7), F(37, 33), F(391, 239),
    ]
    factors, residual = factor_known_roots(characteristic, known)
    algebraic_factor = None
    cubic = perfect_quartic_cube(residual)
    if cubic is not None:
        scale, quartic = cubic
        intervals = [
            (F(5912, 10000), F(5913, 10000)),
            (F(9871, 10000), F(9872, 10000)),
            (F(22091, 10000), F(22092, 10000)),
            (F(22551, 10000), F(22552, 10000)),
        ]
        counts = [sturm_root_count(quartic, left, right) for left, right in intervals]
        if counts != [1, 1, 1, 1]:
            raise ArithmeticError("quartic root isolation failed")
        algebraic_factor = {
            "scale": str(scale),
            "quartic_low_first": [str(value) for value in quartic],
            "multiplicity": 3,
            "rational_isolating_intervals": [
                {"left": str(left), "right": str(right), "root_count_by_sturm": count}
                for (left, right), count in zip(intervals, counts)
            ],
            "perfect_cube_identity_verified_over_Q": True,
            "four_distinct_positive_real_roots_verified_by_sturm": True,
        }
    cost_strings = _matrix_strings(cost)
    metric_strings = _matrix_strings(metric)
    cost_rank = rational_rank(np.array(cost, dtype=object))
    nullspace = _exact_nullspace(np.array(cost, dtype=object))
    witnesses = [_canonical_integer_vector(vector) for vector in nullspace]
    for witness in nullspace:
        if any(sum(cost[i][j] * witness[j] for j in range(len(witness))) for i in range(len(cost))):
            raise ArithmeticError("stored kernel witness fails exactly")
    hostile_same = bool(np.array_equal(a6, hostile))
    return {
        "name": name,
        "links": [int(link) for link in links],
        "operator_shape": list(a6.shape),
        "star_union_plaquettes": len(union),
        "external_plaquettes": len(external),
        "operator_sha256": _sha256_integer_matrix(a6),
        "external_map_sha256": _sha256_integer_matrix(b),
        "row_basis_sha256": _sha256_integer_matrix(r6),
        "star_data_rank_over_Q": len(r6),
        "spill_cost_rank_over_Q": cost_rank,
        "spill_nullity_over_Q": len(r6) - cost_rank,
        "independent_operator_rows": list(map(int, row_indices)),
        "row_basis_pivot_columns": list(map(int, pivot_cols)),
        "metric": metric_strings,
        "minimum_cost_matrix": cost_strings,
        "generalized_characteristic_polynomial_low_first": [str(value) for value in characteristic],
        "certified_rational_factors": [
            {"root": str(root), "multiplicity": multiplicity} for root, multiplicity in factors
        ],
        "residual_characteristic_factor_low_first": [str(value) for value in residual],
        "residual_algebraic_factorization": algebraic_factor,
        "kernel_witnesses_in_row_coordinates": witnesses,
        "kkt_witness_sha256": hashlib.sha256(
            json.dumps(_matrix_strings(x), separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "lagrange_witness_sha256": hashlib.sha256(
            json.dumps(_matrix_strings(lagrange), separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "complete_kkt_system_verified_over_Q": True,
        "characteristic_polynomial_verified_over_Q": True,
        "kernel_witnesses_verified_over_Q": True,
        "orientation_hostile_regression": {
            "orient_then_center_operator_equals_center_then_orient": hostile_same,
            "correct_operator_sha256": _sha256_integer_matrix(a6),
            "hostile_operator_sha256": _sha256_integer_matrix(hostile),
            "operators_differ": not hostile_same,
        },
    }


def orientation_regression_certificate(d1: np.ndarray, link: int) -> dict:
    correct, union = polymer_operator(d1, (link,))
    hostile, _ = polymer_operator(d1, (link,), hostile=True)
    external = tuple(sorted(set(range(d1.shape[0])) - set(union)))
    b = d1[np.array(external)]
    correct_r, _, _, _, _ = row_coordinate_system(correct)
    hostile_r, _, _, _, _ = row_coordinate_system(hostile)
    _, _, correct_cost = exact_kkt_witness(correct_r, b)
    _, _, hostile_cost = exact_kkt_witness(hostile_r, b)
    correct_nullity = len(correct_r) - rational_rank(np.array(correct_cost, dtype=object))
    hostile_nullity = len(hostile_r) - rational_rank(np.array(hostile_cost, dtype=object))
    difference = correct - hostile
    if (correct_nullity, hostile_nullity) != (0, 1):
        raise ArithmeticError("orientation-hostile one-star regression changed")
    return {
        "root_link": int(link),
        "correct_convention": "(6I-J) O S d1: orient before centering",
        "hostile_convention": "O (6I-J) S d1: center before orienting",
        "correct_operator_sha256": _sha256_integer_matrix(correct),
        "hostile_operator_sha256": _sha256_integer_matrix(hostile),
        "difference_nonzero_entries": int(np.count_nonzero(difference)),
        "difference_rank_over_Q": rational_rank(difference),
        "correct_spill_nullity_over_Q": correct_nullity,
        "hostile_spill_nullity_over_Q": hostile_nullity,
        "spurious_hostile_zero_mode_detected_exactly": True,
    }


def build_results() -> dict:
    d1, vertices, edges, plaquettes = block_incidence()
    links = interior_links(d1)
    systems = {
        "adjacent_pair": (links[0], links[4]),
        "central_four": links[4:8],
        "all_eight": links,
    }
    certificates = {name: polymer_certificate(name, d1, chosen) for name, chosen in systems.items()}
    return {
        "schema_version": 1,
        "claim_level": "C2 exact finite rational multi-star certificate",
        "arithmetic_contract": "floating point locates KKT witnesses; every conclusion is verified over Q",
        "ambient_block": {
            "vertices": len(vertices),
            "links": len(edges),
            "plaquettes": len(plaquettes),
            "interior_links": len(links),
            "interior_link_coordinates": [str(edges[index]) for index in links],
            "d1_rank_over_Q": rational_rank(d1),
            "d1_sha256": _sha256_integer_matrix(d1),
        },
        "certificates": certificates,
        "orientation_hostile_regression": orientation_regression_certificate(d1, links[0]),
        "scope": {
            "finite_open_side_two_four_cube": True,
            "linearized_about_identity": True,
            "orientation_correct": True,
            "physical_boundary_law": False,
            "nonlinear_gauge_covariant_repair": False,
            "measure_or_partition_ratio": False,
            "continuum_yang_mills": False,
            "mass_gap": False,
        },
    }


def verify_stored() -> None:
    stored = json.loads(RESULTS.read_text(encoding="utf-8"))
    fresh = build_results()
    if stored != fresh:
        raise AssertionError("stored result differs from exact recomputation")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    data = build_results()
    if args.write:
        RESULTS.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.verify:
        stored = json.loads(RESULTS.read_text(encoding="utf-8"))
        if stored != data:
            raise AssertionError("stored result differs from exact recomputation")
    print(json.dumps({
        "claim_level": data["claim_level"],
        "systems": {
            name: {
                "rank": cert["star_data_rank_over_Q"],
                "nullity": cert["spill_nullity_over_Q"],
                "factors": cert["certified_rational_factors"],
                "residual_degree": len(cert["residual_characteristic_factor_low_first"]) - 1,
            }
            for name, cert in data["certificates"].items()
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
