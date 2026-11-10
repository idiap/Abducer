"""Exact typed commuting-square certificates for H6.

All finite-dimensional transport calculations use ``fractions.Fraction``.
The module proves algebraic representation identities only; it does not
instantiate a nonlinear Yang--Mills block map or a positive OS reconstruction.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import itertools
import hashlib
import json
import math
from pathlib import Path
import random
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "h6_typed_square_defects_results.json"


def q(value: int | str | F) -> F:
    """Coerce an exact scalar without accepting binary floating point."""

    if isinstance(value, float):
        raise TypeError("binary floating point is forbidden in exact certificates")
    return value if isinstance(value, F) else F(value)


@dataclass(frozen=True, order=True)
class VectorSpace:
    name: str
    dimension: int

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("a vector space needs a nonempty name")
        if self.dimension <= 0:
            raise ValueError("a vector space needs positive dimension")


@dataclass(frozen=True)
class LinearMap:
    """An exact matrix with an explicit domain and codomain."""

    name: str
    domain: VectorSpace
    codomain: VectorSpace
    entries: tuple[tuple[F, ...], ...]

    @classmethod
    def from_rows(
        cls,
        name: str,
        domain: VectorSpace,
        codomain: VectorSpace,
        rows: Sequence[Sequence[int | str | F]],
    ) -> "LinearMap":
        converted = tuple(tuple(q(x) for x in row) for row in rows)
        return cls(name, domain, codomain, converted)

    def __post_init__(self) -> None:
        if len(self.entries) != self.codomain.dimension:
            raise ValueError(
                f"{self.name}: row count must equal codomain dimension"
            )
        if any(len(row) != self.domain.dimension for row in self.entries):
            raise ValueError(
                f"{self.name}: column count must equal domain dimension"
            )

    def compose(self, right: "LinearMap", name: str | None = None) -> "LinearMap":
        """Return ``self o right``, rejecting merely dimension-compatible types."""

        if right.codomain != self.domain:
            raise TypeError(
                f"cannot compose {self.name}:{self.domain.name}->{self.codomain.name} "
                f"after {right.name}:{right.domain.name}->{right.codomain.name}"
            )
        rows = [
            [
                sum(
                    self.entries[i][k] * right.entries[k][j]
                    for k in range(self.domain.dimension)
                )
                for j in range(right.domain.dimension)
            ]
            for i in range(self.codomain.dimension)
        ]
        return LinearMap.from_rows(
            name or f"({self.name})o({right.name})",
            right.domain,
            self.codomain,
            rows,
        )

    def _combine(self, other: "LinearMap", sign: int, name: str) -> "LinearMap":
        if self.domain != other.domain or self.codomain != other.codomain:
            raise TypeError("maps can be combined only when both endpoint types agree")
        rows = [
            [self.entries[i][j] + sign * other.entries[i][j]
             for j in range(self.domain.dimension)]
            for i in range(self.codomain.dimension)
        ]
        return LinearMap.from_rows(name, self.domain, self.codomain, rows)

    def add(self, other: "LinearMap", name: str | None = None) -> "LinearMap":
        return self._combine(other, 1, name or f"({self.name})+({other.name})")

    def subtract(self, other: "LinearMap", name: str | None = None) -> "LinearMap":
        return self._combine(other, -1, name or f"({self.name})-({other.name})")

    def scale(self, scalar: int | str | F, name: str | None = None) -> "LinearMap":
        factor = q(scalar)
        return LinearMap.from_rows(
            name or f"{factor}({self.name})",
            self.domain,
            self.codomain,
            [[factor * x for x in row] for row in self.entries],
        )

    def norm_infinity(self) -> F:
        """Exact induced infinity norm (maximum absolute row sum)."""

        return max(sum(abs(x) for x in row) for row in self.entries)

    def norm_one(self) -> F:
        """Exact induced one norm (maximum absolute column sum)."""

        return max(
            sum(abs(self.entries[i][j]) for i in range(self.codomain.dimension))
            for j in range(self.domain.dimension)
        )

    def is_zero(self) -> bool:
        return all(x == 0 for row in self.entries for x in row)

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "domain": {"name": self.domain.name, "dimension": self.domain.dimension},
            "codomain": {
                "name": self.codomain.name,
                "dimension": self.codomain.dimension,
            },
            "entries": [[str(x) for x in row] for row in self.entries],
            "norm_infinity": str(self.norm_infinity()),
        }


def identity(space: VectorSpace, name: str | None = None) -> LinearMap:
    return LinearMap.from_rows(
        name or f"I_{space.name}",
        space,
        space,
        [[1 if i == j else 0 for j in range(space.dimension)]
         for i in range(space.dimension)],
    )


def zero_map(domain: VectorSpace, codomain: VectorSpace, name: str) -> LinearMap:
    return LinearMap.from_rows(
        name,
        domain,
        codomain,
        [[0] * domain.dimension for _ in range(codomain.dimension)],
    )


def add_maps(maps: Sequence[LinearMap], name: str) -> LinearMap:
    if not maps:
        raise ValueError("cannot add an empty map family without endpoint types")
    total = zero_map(maps[0].domain, maps[0].codomain, "zero")
    for item in maps:
        total = total.add(item)
    return LinearMap(name, total.domain, total.codomain, total.entries)


@dataclass(frozen=True)
class TypedTower:
    """Two representation towers joined by levelwise maps R_k."""

    x_spaces: tuple[VectorSpace, ...]
    y_spaces: tuple[VectorSpace, ...]
    b_maps: tuple[LinearMap, ...]
    t_maps: tuple[LinearMap, ...]
    r_maps: tuple[LinearMap, ...]

    def __post_init__(self) -> None:
        if len(self.x_spaces) < 2:
            raise ValueError("a tower requires at least one square")
        n = len(self.x_spaces) - 1
        if len(self.y_spaces) != n + 1:
            raise ValueError("X and Y towers must have the same number of levels")
        if len(self.b_maps) != n or len(self.t_maps) != n:
            raise ValueError("one B and T arrow is required per square")
        if len(self.r_maps) != n + 1:
            raise ValueError("one representation map R is required per level")
        for k in range(n):
            self._expect(self.b_maps[k], self.x_spaces[k], self.x_spaces[k + 1], f"B[{k}]")
            self._expect(self.t_maps[k], self.y_spaces[k], self.y_spaces[k + 1], f"T[{k}]")
        for k, map_ in enumerate(self.r_maps):
            self._expect(map_, self.x_spaces[k], self.y_spaces[k], f"R[{k}]")

    @staticmethod
    def _expect(map_: LinearMap, domain: VectorSpace, codomain: VectorSpace, label: str) -> None:
        if map_.domain != domain or map_.codomain != codomain:
            raise TypeError(f"{label} has incorrect typed endpoints")

    @property
    def steps(self) -> int:
        return len(self.b_maps)

    def _product(
        self,
        arrows: Sequence[LinearMap],
        spaces: Sequence[VectorSpace],
        start: int,
        end: int,
        label: str,
    ) -> LinearMap:
        if not (0 <= start <= end <= self.steps):
            raise IndexError("invalid tower interval")
        product = identity(spaces[start], f"{label}_{{{start}:{start}}}")
        for k in range(start, end):
            product = arrows[k].compose(product, f"{label}_{{{k + 1}:{start}}}")
        return product

    def b_product(self, start: int, end: int) -> LinearMap:
        return self._product(self.b_maps, self.x_spaces, start, end, "B")

    def t_product(self, start: int, end: int) -> LinearMap:
        return self._product(self.t_maps, self.y_spaces, start, end, "T")

    def square_defect(self, k: int) -> LinearMap:
        if not 0 <= k < self.steps:
            raise IndexError("square index out of range")
        upper = self.t_maps[k].compose(self.r_maps[k], f"T{k}R{k}")
        lower = self.r_maps[k + 1].compose(self.b_maps[k], f"R{k + 1}B{k}")
        return upper.subtract(lower, f"Omega_{k}")

    def total_transport_defect(self, end: int | None = None) -> LinearMap:
        n = self.steps if end is None else end
        upper = self.t_product(0, n).compose(self.r_maps[0], "upper_path")
        lower = self.r_maps[n].compose(self.b_product(0, n), "lower_path")
        return upper.subtract(lower, f"Delta_{n}:0")

    def telescoping_terms(self, end: int | None = None) -> tuple[LinearMap, ...]:
        n = self.steps if end is None else end
        terms: list[LinearMap] = []
        for j in range(n):
            middle = self.square_defect(j).compose(self.b_product(0, j))
            term = self.t_product(j + 1, n).compose(middle, f"transported_Omega_{j}")
            terms.append(term)
        return tuple(terms)

    def telescoping_certificate(self, end: int | None = None) -> dict[str, object]:
        n = self.steps if end is None else end
        lhs = self.total_transport_defect(n)
        terms = self.telescoping_terms(n)
        rhs = add_maps(terms, "telescoping_sum")
        bound_terms: list[dict[str, str | int]] = []
        for j, term in enumerate(terms):
            prefix = self.b_product(0, j).norm_infinity()
            epsilon = self.square_defect(j).norm_infinity()
            future = self.t_product(j + 1, n).norm_infinity()
            bound_terms.append(
                {
                    "step": j,
                    "prefix_B_norm": str(prefix),
                    "square_defect_norm": str(epsilon),
                    "future_T_norm": str(future),
                    "term_norm": str(term.norm_infinity()),
                    "submultiplicative_bound": str(prefix * epsilon * future),
                }
            )
        total_bound = sum(q(row["submultiplicative_bound"]) for row in bound_terms)
        return {
            "end_level": n,
            "identity_exact": lhs.entries == rhs.entries,
            "lhs": lhs.to_json(),
            "rhs": rhs.to_json(),
            "accumulated_norm": str(lhs.norm_infinity()),
            "triangle_product_bound": str(total_bound),
            "norm_bound_exactly_verified": lhs.norm_infinity() <= total_bound,
            "per_step_ledger": bound_terms,
        }

    def recovered_certificate(self, recovery: LinearMap) -> dict[str, object]:
        n = self.steps
        self._expect(recovery, self.y_spaces[n], self.x_spaces[n], "S[n]")
        b_total = self.b_product(0, n)
        t_total = self.t_product(0, n)
        lhs = recovery.compose(t_total).compose(self.r_maps[0]).subtract(b_total, "recovered_lhs")
        recovery_error = recovery.compose(self.r_maps[n]).subtract(identity(self.x_spaces[n]), "S_nR_n-I")
        recovery_term = recovery_error.compose(b_total, "terminal_recovery_term")
        transported: list[LinearMap] = []
        ledger: list[dict[str, str | int]] = []
        for j in range(n):
            prefix = self.b_product(0, j)
            future = recovery.compose(self.t_product(j + 1, n), f"S_nT_{{n:{j + 1}}}")
            term = future.compose(self.square_defect(j)).compose(prefix, f"recovered_Omega_{j}")
            transported.append(term)
            bound = future.norm_infinity() * self.square_defect(j).norm_infinity() * prefix.norm_infinity()
            ledger.append(
                {
                    "step": j,
                    "recovered_future_norm": str(future.norm_infinity()),
                    "square_defect_norm": str(self.square_defect(j).norm_infinity()),
                    "prefix_B_norm": str(prefix.norm_infinity()),
                    "term_norm": str(term.norm_infinity()),
                    "submultiplicative_bound": str(bound),
                }
            )
        rhs = recovery_term.add(add_maps(transported, "recovered_defect_sum"), "recovered_rhs")
        terminal_bound = recovery_error.norm_infinity() * b_total.norm_infinity()
        transported_bound = sum(q(row["submultiplicative_bound"]) for row in ledger)
        total_bound = terminal_bound + transported_bound
        return {
            "identity_exact": lhs.entries == rhs.entries,
            "lhs": lhs.to_json(),
            "rhs": rhs.to_json(),
            "terminal_recovery_error_norm": str(recovery_error.norm_infinity()),
            "terminal_recovery_term_norm": str(recovery_term.norm_infinity()),
            "terminal_recovery_bound": str(terminal_bound),
            "accumulated_norm": str(lhs.norm_infinity()),
            "recovered_transport_bound": str(total_bound),
            "norm_bound_exactly_verified": lhs.norm_infinity() <= total_bound,
            "per_step_ledger": ledger,
        }


def random_rational_map(
    rng: random.Random,
    name: str,
    domain: VectorSpace,
    codomain: VectorSpace,
) -> LinearMap:
    rows = [
        [F(rng.randint(-4, 4), rng.randint(1, 5)) for _ in range(domain.dimension)]
        for _ in range(codomain.dimension)
    ]
    return LinearMap.from_rows(name, domain, codomain, rows)


def random_tower(seed: int, x_dimensions: Sequence[int], y_dimensions: Sequence[int]) -> TypedTower:
    if len(x_dimensions) != len(y_dimensions) or len(x_dimensions) < 2:
        raise ValueError("dimension sequences need equal length at least two")
    rng = random.Random(seed)
    xs = tuple(VectorSpace(f"X{k}", d) for k, d in enumerate(x_dimensions))
    ys = tuple(VectorSpace(f"Y{k}", d) for k, d in enumerate(y_dimensions))
    bs = tuple(random_rational_map(rng, f"B{k}", xs[k], xs[k + 1]) for k in range(len(xs) - 1))
    ts = tuple(random_rational_map(rng, f"T{k}", ys[k], ys[k + 1]) for k in range(len(ys) - 1))
    rs = tuple(random_rational_map(rng, f"R{k}", xs[k], ys[k]) for k in range(len(xs)))
    return TypedTower(xs, ys, bs, ts, rs)


def _poly_add(a: Sequence[F], b: Sequence[F]) -> list[F]:
    return [
        (a[i] if i < len(a) else F(0)) + (b[i] if i < len(b) else F(0))
        for i in range(max(len(a), len(b)))
    ]


def _poly_mul(a: Sequence[F], b: Sequence[F]) -> list[F]:
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def _permutation_sign(perm: Sequence[int]) -> int:
    inversions = sum(
        perm[i] > perm[j]
        for i in range(len(perm))
        for j in range(i + 1, len(perm))
    )
    return -1 if inversions % 2 else 1


def characteristic_polynomial(matrix: Sequence[Sequence[F]]) -> list[F]:
    """Return det(lambda I-A), coefficients in ascending order."""

    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("characteristic polynomial requires a nonempty square matrix")
    result = [F(0)]
    for perm in itertools.permutations(range(n)):
        term = [F(_permutation_sign(perm))]
        for i, j in enumerate(perm):
            factor = [-matrix[i][j], F(1)] if i == j else [-matrix[i][j]]
            term = _poly_mul(term, factor)
        result = _poly_add(result, term)
    return result


def polynomial_from_roots(roots: Iterable[F]) -> list[F]:
    out = [F(1)]
    for root in roots:
        out = _poly_mul(out, [-root, F(1)])
    return out


def matrix_multiply(a: Sequence[Sequence[F]], b: Sequence[Sequence[F]]) -> list[list[F]]:
    if not a or not b or any(len(row) != len(b) for row in a):
        raise ValueError("untyped matrix multiplication dimension mismatch")
    columns = len(b[0])
    if any(len(row) != columns for row in b):
        raise ValueError("ragged matrix")
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(columns)]
        for i in range(len(a))
    ]


def matrix_subtract(a: Sequence[Sequence[F]], b: Sequence[Sequence[F]]) -> list[list[F]]:
    if len(a) != len(b) or any(len(x) != len(y) for x, y in zip(a, b)):
        raise ValueError("matrix subtraction dimension mismatch")
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def transpose(a: Sequence[Sequence[F]]) -> list[list[F]]:
    if not a or any(len(row) != len(a[0]) for row in a):
        raise ValueError("transpose requires a nonempty rectangular matrix")
    return [list(column) for column in zip(*a)]


def exact_rank(matrix: Sequence[Sequence[F]]) -> int:
    work = [list(row) for row in matrix]
    if not work:
        return 0
    rows, columns = len(work), len(work[0])
    if any(len(row) != columns for row in work):
        raise ValueError("rank requires a rectangular matrix")
    rank = 0
    for column in range(columns):
        pivot = next((i for i in range(rank, rows) if work[i][column] != 0), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [x / scale for x in work[rank]]
        for i in range(rows):
            if i != rank and work[i][column] != 0:
                multiple = work[i][column]
                work[i] = [x - multiple * y for x, y in zip(work[i], work[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def balanced_star_certificate() -> dict[str, object]:
    """Exact rank/norm and correct-versus-hostile spectrum certificate."""

    n = 6
    signs = [F(-1)] * 3 + [F(1)] * 3
    center = [[(F(1) if i == j else F(0)) - F(1, n) for j in range(n)] for i in range(n)]
    orient = [[signs[i] if i == j else F(0) for j in range(n)] for i in range(n)]
    commutator = matrix_subtract(matrix_multiply(center, orient), matrix_multiply(orient, center))
    expected_commutator = [[(signs[i] - signs[j]) / n for j in range(n)] for i in range(n)]
    gram = matrix_multiply(transpose(commutator), commutator)
    active_projector = [[(F(1) + signs[i] * signs[j]) / n for j in range(n)] for i in range(n)]

    # Canonical exact star compression from the side-two open four-cube.
    strings = [
        ["1999/3780", "391/3780", "391/3780", "-31/540", "-391/3780", "-391/3780"],
        ["391/3780", "1999/3780", "391/3780", "-391/3780", "-31/540", "-391/3780"],
        ["391/3780", "391/3780", "1999/3780", "-391/3780", "-391/3780", "-31/540"],
        ["-31/540", "-391/3780", "-391/3780", "1999/3780", "391/3780", "391/3780"],
        ["-391/3780", "-31/540", "-391/3780", "391/3780", "1999/3780", "391/3780"],
        ["-391/3780", "-391/3780", "-31/540", "391/3780", "391/3780", "1999/3780"],
    ]
    projection_block = [[F(x) for x in row] for row in strings]
    source_fixture_sha256 = hashlib.sha256(
        json.dumps(strings, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    hostile = matrix_multiply(matrix_multiply(center, projection_block), center)
    oriented_block = matrix_multiply(matrix_multiply(orient, projection_block), orient)
    correct = matrix_multiply(matrix_multiply(center, oriented_block), center)
    hostile_roots = [F(0), F(239, 630), F(239, 630), F(33, 70), F(33, 70), F(1)]
    correct_roots = [F(0), F(239, 630), F(239, 630), F(33, 70), F(33, 70), F(33, 70)]
    hostile_poly = characteristic_polynomial(hostile)
    correct_poly = characteristic_polynomial(correct)

    return {
        "orientation_signs": [str(x) for x in signs],
        "commutator_formula_exact": commutator == expected_commutator,
        "commutator_rank": exact_rank(commutator),
        "gram_is_rank_two_orthogonal_projector": gram == active_projector,
        "euclidean_operator_norm": "1",
        "norm_certificate": "[C,O]^T[C,O]=(11^T+ss^T)/6, the orthogonal projector onto span{1,s}",
        "hostile_center_before_common_orientation_spectrum": [str(x) for x in hostile_roots],
        "correct_orient_then_center_spectrum": [str(x) for x in correct_roots],
        "hostile_characteristic_polynomial": [str(x) for x in hostile_poly],
        "correct_characteristic_polynomial": [str(x) for x in correct_poly],
        "hostile_characteristic_polynomial_exact": hostile_poly == polynomial_from_roots(hostile_roots),
        "correct_characteristic_polynomial_exact": correct_poly == polynomial_from_roots(correct_roots),
        "spectra_differ": hostile_poly != correct_poly,
        "source": (
            "displayed rational six-star fixture transcribed from the prior "
            "side-two open-four-cube work"
        ),
        "source_fixture_sha256": source_fixture_sha256,
        "geometric_provenance_derived_or_hash_linked_in_stage73": False,
        "provenance_downgrade": (
            "Stage 73 proves the theorem for this displayed rational matrix; "
            "it does not independently derive the matrix from Stage 70 geometry"
        ),
    }


def rational_rotation(parameter: F) -> list[list[F]]:
    """Rational parametrization of SO(2), with angle 2 arctan(parameter)."""

    t = q(parameter)
    denominator = 1 + t * t
    return [
        [(1 - t * t) / denominator, -2 * t / denominator],
        [2 * t / denominator, (1 - t * t) / denominator],
    ]


def matrix_power(matrix: Sequence[Sequence[F]], exponent: int) -> list[list[F]]:
    if exponent < 0 or not matrix or len(matrix) != len(matrix[0]):
        raise ValueError("matrix power requires a nonnegative exponent and square matrix")
    n = len(matrix)
    result = [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]
    base = [list(row) for row in matrix]
    power = exponent
    while power:
        if power & 1:
            result = matrix_multiply(result, base)
        base = matrix_multiply(base, base)
        power >>= 1
    return result


def matrix_infinity_norm(matrix: Sequence[Sequence[F]]) -> F:
    return max(sum(abs(x) for x in row) for row in matrix)


def counterexamples() -> dict[str, object]:
    """Four exact hostile models fixing the transport hypotheses."""

    # Small rotations: exact one-step defects accumulate without summability.
    t = F(1, 100)
    rotation = rational_rotation(t)
    identity2 = [[F(1), F(0)], [F(0), F(1)]]
    one_step = matrix_infinity_norm(matrix_subtract(rotation, identity2))
    steps = 79
    accumulated = matrix_infinity_norm(matrix_subtract(matrix_power(rotation, steps), identity2))

    # A defect hidden from e1* becomes visible after an exact coordinate swap.
    omega = [[F(0), F(0)], [F(1), F(0)]]
    swap = [[F(0), F(1)], [F(1), F(0)]]
    current_probe = [omega[0][0], omega[0][1]]
    future_defect = matrix_multiply(swap, omega)
    final_probe = [future_defect[0][0], future_defect[0][1]]

    # Exact inverse recovery has an unbounded family of condition numbers.
    delta = F(1, 1000)
    representation = [[F(1), F(0)], [F(0), delta]]
    recovery = [[F(1), F(0)], [F(0), 1 / delta]]
    recovery_identity = matrix_multiply(recovery, representation)
    small_defect = [[F(0)], [delta]]
    recovered_defect = matrix_multiply(recovery, small_defect)

    # An unnormalized support sum magnifies a uniform cellwise defect.
    support_size = 100
    per_cell = F(1, support_size)
    support_sum = support_size * per_cell

    return {
        "small_rotations": {
            "rational_parameter": str(t),
            "steps": steps,
            "one_step_infinity_norm": str(one_step),
            "one_step_infinity_norm_decimal": float(one_step),
            "accumulated_infinity_norm": str(accumulated),
            "accumulated_infinity_norm_decimal": float(accumulated),
            "one_step_below_1_over_40": one_step < F(1, 40),
            "accumulated_above_one": accumulated > 1,
            "lesson": "uniformly small square defects need summability or future contraction",
        },
        "hidden_to_visible_swap": {
            "current_visible_probe": [str(x) for x in current_probe],
            "future_visible_probe": [str(x) for x in final_probe],
            "currently_invisible": current_probe == [F(0), F(0)],
            "later_visible_with_unit_amplitude": final_probe == [F(1), F(0)],
            "lesson": "insertion-scale seminorms need forward-invariant blind sectors or future-aware propagation",
        },
        "ill_conditioned_recovery": {
            "delta": str(delta),
            "S_R_is_identity": recovery_identity == identity2,
            "recovery_infinity_norm": str(matrix_infinity_norm(recovery)),
            "input_defect_infinity_norm": str(matrix_infinity_norm(small_defect)),
            "recovered_defect_infinity_norm": str(matrix_infinity_norm(recovered_defect)),
            "vanishing_family_magnified_to_unit": recovered_defect == [[F(0)], [F(1)]],
            "lesson": "exact recovery is insufficient without a uniform condition bound",
        },
        "support_multiplicity": {
            "support_size": support_size,
            "per_cell_defect": str(per_cell),
            "unnormalized_sum_defect": str(support_sum),
            "unit_accumulation": support_sum == 1,
            "lesson": "support growth and observable normalization must enter every defect seminorm",
        },
    }


def calibration() -> dict[str, object]:
    dimensions = ([2, 3, 2, 2], [3, 2, 3, 2])
    tower = random_tower(617, *dimensions)
    terminal_recovery = random_rational_map(
        random.Random(991), "S3", tower.y_spaces[-1], tower.x_spaces[-1]
    )
    trials = []
    for seed in (3, 17, 101, 617, 2027):
        trial = random_tower(seed, *dimensions)
        certificate = trial.telescoping_certificate()
        trials.append(
            {
                "seed": seed,
                "identity_exact": certificate["identity_exact"],
                "norm_bound_exactly_verified": certificate["norm_bound_exactly_verified"],
            }
        )
    return {
        "schema_version": 1,
        "stage": 73,
        "stream": "H6 typed square defects",
        "claim_level": "C2 exact finite-dimensional algebra and abstract rational transport",
        "strongest_claim": "typed rational square defects telescope exactly, including terminal recovery, with exact accumulated induced-infinity-norm ledgers",
        "typed_calibration": {
            "x_dimensions": dimensions[0],
            "y_dimensions": dimensions[1],
            "telescoping": tower.telescoping_certificate(),
            "recovered_transport": tower.recovered_certificate(terminal_recovery),
        },
        "random_rational_regression_trials": trials,
        "balanced_star": balanced_star_certificate(),
        "counterexamples": counterexamples(),
        "guardrails": {
            "nonlinear_SU2_block_instantiated": False,
            "gauge_covariance_proved": False,
            "positivity_or_reflection_positivity_proved": False,
            "uniform_volume_cutoff_transport_proved": False,
            "continuum_OS_reconstruction_proved": False,
            "mass_gap_proved": False,
        },
        "first_open_implication": "instantiate the typed square and recovered bound for one nonlinear gauge-covariant SU(2) block in support-indexed physical seminorms, uniformly in boundary history",
    }


def write_results(path: Path = RESULTS) -> dict[str, object]:
    result = calibration()
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write canonical JSON")
    args = parser.parse_args()
    result = write_results() if args.write else calibration()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
