"""Exact finite observable recovery on a two-vertex Z2 gauge graph.

The graph has three parallel oriented edges between two vertices.  A local
gauge transformation multiplies every edge by ``g_left * g_right``.  The two
independent Wilson products ``e0*e1`` and ``e1*e2`` coordinatize the orbit
quotient.  All arithmetic used for observable errors is exact ``Fraction``
arithmetic.  This is a finite C2 toy theorem, not an SU(2) construction.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import itertools
import json
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "observable_recovery_results.json"

Sign = int
FineConfig = tuple[Sign, Sign, Sign]
GaugeElement = tuple[Sign, Sign]
QuotientConfig = tuple[Sign, Sign]
LabeledQuotientConfig = tuple[Sign, Sign, Sign]

FINE_CONFIGS: tuple[FineConfig, ...] = tuple(itertools.product((-1, 1), repeat=3))
GAUGE_GROUP: tuple[GaugeElement, ...] = tuple(itertools.product((-1, 1), repeat=2))
QUOTIENT_CONFIGS: tuple[QuotientConfig, ...] = tuple(
    itertools.product((-1, 1), repeat=2)
)
MASKS: tuple[tuple[int, int], ...] = ((0, 0), (1, 0), (0, 1), (1, 1))


def _validate_sign(value: object, label: str) -> Sign:
    if isinstance(value, bool) or value not in (-1, 1):
        raise ValueError(f"{label} must be -1 or +1")
    return int(value)


def validate_fine(x: Sequence[int]) -> FineConfig:
    if len(x) != 3:
        raise ValueError("a fine configuration has exactly three edge signs")
    return tuple(_validate_sign(value, f"edge[{i}]") for i, value in enumerate(x))  # type: ignore[return-value]


def validate_gauge(g: Sequence[int]) -> GaugeElement:
    if len(g) != 2:
        raise ValueError("a gauge element has one sign at each of two vertices")
    return tuple(_validate_sign(value, f"gauge[{i}]") for i, value in enumerate(g))  # type: ignore[return-value]


def validate_quotient(y: Sequence[int]) -> QuotientConfig:
    if len(y) != 2:
        raise ValueError("the quotient has two independent Wilson coordinates")
    return tuple(_validate_sign(value, f"quotient[{i}]") for i, value in enumerate(y))  # type: ignore[return-value]


def gauge_action(g: Sequence[int], x: Sequence[int]) -> FineConfig:
    """Apply the two-vertex local Z2 action to all three parallel edges."""

    left, right = validate_gauge(g)
    fine = validate_fine(x)
    factor = left * right
    return tuple(factor * edge for edge in fine)  # type: ignore[return-value]


def wilson_01(x: Sequence[int]) -> Sign:
    edge = validate_fine(x)
    return edge[0] * edge[1]


def wilson_12(x: Sequence[int]) -> Sign:
    edge = validate_fine(x)
    return edge[1] * edge[2]


def wilson_02(x: Sequence[int]) -> Sign:
    edge = validate_fine(x)
    return edge[0] * edge[2]


def quotient_block(x: Sequence[int]) -> QuotientConfig:
    """The exact orbit map B(x)=(W_01(x),W_12(x))."""

    return (wilson_01(x), wilson_12(x))


def canonical_reconstruct(y: Sequence[int]) -> FineConfig:
    """Choose the slice e0=1 in every orbit."""

    first, second = validate_quotient(y)
    return (1, first, first * second)


def recovery_projection(x: Sequence[int]) -> FineConfig:
    return canonical_reconstruct(quotient_block(x))


def gauge_orbit(x: Sequence[int]) -> tuple[FineConfig, ...]:
    return tuple(sorted(set(gauge_action(g, x) for g in GAUGE_GROUP)))


def gauge_equivalent(x: Sequence[int], z: Sequence[int]) -> bool:
    target = validate_fine(z)
    return target in gauge_orbit(x)


def _fraction(value: int | str | F) -> F:
    if isinstance(value, float):
        raise TypeError("binary floating point is forbidden in exact observables")
    return value if isinstance(value, F) else F(value)


@dataclass(frozen=True)
class InvariantObservable:
    """Rational linear combination of the four quotient characters.

    Coefficients are ordered as 1, W_01, W_12, and W_01 W_12 = W_02.
    Their span is the complete rational invariant algebra on this finite
    quotient.  The coefficient l1 norm is a submultiplicative declared norm.
    """

    name: str
    coefficients: tuple[F, F, F, F]

    @classmethod
    def from_coefficients(
        cls, name: str, coefficients: Sequence[int | str | F]
    ) -> "InvariantObservable":
        if not name:
            raise ValueError("an observable needs a nonempty name")
        if len(coefficients) != 4:
            raise ValueError("exactly four character coefficients are required")
        return cls(name, tuple(_fraction(value) for value in coefficients))  # type: ignore[arg-type]

    def on_quotient(self, y: Sequence[int]) -> F:
        first, second = validate_quotient(y)
        values = (1, first, second, first * second)
        return sum(coefficient * value for coefficient, value in zip(self.coefficients, values))

    def on_fine(self, x: Sequence[int]) -> F:
        return self.on_quotient(quotient_block(x))

    @property
    def coefficient_norm(self) -> F:
        return sum(abs(value) for value in self.coefficients)

    @property
    def sup_norm(self) -> F:
        return max(abs(self.on_quotient(y)) for y in QUOTIENT_CONFIGS)

    @property
    def complexity(self) -> int:
        return max(
            (sum(mask) for coefficient, mask in zip(self.coefficients, MASKS) if coefficient),
            default=0,
        )

    def multiply(self, other: "InvariantObservable", name: str | None = None) -> "InvariantObservable":
        output = [F(0) for _ in MASKS]
        mask_index = {mask: i for i, mask in enumerate(MASKS)}
        for i, left in enumerate(self.coefficients):
            for j, right in enumerate(other.coefficients):
                mask = (MASKS[i][0] ^ MASKS[j][0], MASKS[i][1] ^ MASKS[j][1])
                output[mask_index[mask]] += left * right
        return InvariantObservable.from_coefficients(
            name or f"({self.name})({other.name})", output
        )

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "coefficients": [str(value) for value in self.coefficients],
            "coefficient_l1_norm": str(self.coefficient_norm),
            "sup_norm": str(self.sup_norm),
            "complexity": self.complexity,
            "values_on_quotient": {
                str(y): str(self.on_quotient(y)) for y in QUOTIENT_CONFIGS
            },
        }


ONE = InvariantObservable.from_coefficients("1", (1, 0, 0, 0))
W01 = InvariantObservable.from_coefficients("W01", (0, 1, 0, 0))
W12 = InvariantObservable.from_coefficients("W12", (0, 0, 1, 0))
W02 = InvariantObservable.from_coefficients("W02=W01*W12", (0, 0, 0, 1))
CHARACTER_BASIS: tuple[InvariantObservable, ...] = (ONE, W01, W12, W02)
INITIAL_PROBES: tuple[InvariantObservable, ...] = (ONE, W01)


def observable_error(
    block: Callable[[FineConfig], Sequence[int]],
    reconstruct: Callable[[Sequence[int]], FineConfig],
    observable: InvariantObservable,
) -> dict[str, object]:
    pointwise: dict[str, str] = {}
    absolute: list[F] = []
    for x in FINE_CONFIGS:
        recovered = validate_fine(reconstruct(block(x)))
        defect = observable.on_fine(recovered) - observable.on_fine(x)
        pointwise[str(x)] = str(defect)
        absolute.append(abs(defect))
    return {
        "observable": observable.name,
        "pointwise_defects": pointwise,
        "linfinity_error": str(max(absolute)),
        "l1_uniform_fine_error": str(sum(absolute) / len(absolute)),
        "exact_recovery": all(value == 0 for value in absolute),
    }


@dataclass(frozen=True)
class QuotientMap:
    """A deterministic endomap of the four physical orbit labels."""

    name: str
    images: tuple[QuotientConfig, ...]

    @classmethod
    def from_mapping(
        cls, name: str, mapping: Mapping[QuotientConfig, Sequence[int]]
    ) -> "QuotientMap":
        if not name:
            raise ValueError("a quotient map needs a nonempty name")
        if set(mapping) != set(QUOTIENT_CONFIGS):
            raise ValueError("the map must define exactly every quotient state")
        return cls(name, tuple(validate_quotient(mapping[y]) for y in QUOTIENT_CONFIGS))

    def __call__(self, y: Sequence[int]) -> QuotientConfig:
        state = validate_quotient(y)
        return self.images[QUOTIENT_CONFIGS.index(state)]

    def compose(self, right: "QuotientMap", name: str | None = None) -> "QuotientMap":
        return QuotientMap.from_mapping(
            name or f"({self.name})o({right.name})",
            {y: self(right(y)) for y in QUOTIENT_CONFIGS},
        )

    def lifted_recovery(self, x: Sequence[int]) -> FineConfig:
        return canonical_reconstruct(self(quotient_block(x)))


def quotient_observable_error(map_: QuotientMap, observable: InvariantObservable) -> F:
    return max(
        abs(observable.on_quotient(map_(y)) - observable.on_quotient(y))
        for y in QUOTIENT_CONFIGS
    )


def composition_certificate(
    first: QuotientMap,
    second: QuotientMap,
    observable: InvariantObservable,
) -> dict[str, object]:
    """Certify e_O(second o first) <= e_O(first)+e_O(second)."""

    first_error = quotient_observable_error(first, observable)
    second_error = quotient_observable_error(second, observable)
    composed = second.compose(first)
    total_error = quotient_observable_error(composed, observable)
    return {
        "observable": observable.name,
        "first_map": first.name,
        "second_map": second.name,
        "first_error": str(first_error),
        "second_error": str(second_error),
        "two_step_error": str(total_error),
        "sum_bound": str(first_error + second_error),
        "inequality_verified": total_error <= first_error + second_error,
    }


def all_quotient_maps() -> Iterable[QuotientMap]:
    for index, images in enumerate(itertools.product(QUOTIENT_CONFIGS, repeat=4)):
        yield QuotientMap(f"f{index}", tuple(images))


def exhaustive_composition_check() -> dict[str, object]:
    maps = tuple(all_quotient_maps())
    state_index = {state: index for index, state in enumerate(QUOTIENT_CONFIGS)}
    error_table = {
        map_.images: tuple(
            quotient_observable_error(map_, observable)
            for observable in CHARACTER_BASIS
        )
        for map_ in maps
    }
    checks = 0
    worst_slack: F | None = None
    for first in maps:
        for second in maps:
            composed_images = tuple(
                second.images[state_index[state]] for state in first.images
            )
            first_errors = error_table[first.images]
            second_errors = error_table[second.images]
            composed_errors = error_table[composed_images]
            for observable_index in range(len(CHARACTER_BASIS)):
                bound = (
                    first_errors[observable_index] + second_errors[observable_index]
                )
                two_step = composed_errors[observable_index]
                if two_step > bound:
                    raise AssertionError("the exact two-step composition bound failed")
                slack = bound - two_step
                worst_slack = slack if worst_slack is None else min(worst_slack, slack)
                checks += 1
    return {
        "number_of_quotient_maps": len(maps),
        "observable_basis_size": len(CHARACTER_BASIS),
        "certified_map_pair_observable_triples": checks,
        "minimum_slack": str(worst_slack),
        "all_inequalities_verified": True,
    }


def gauge_quotient_certificate() -> dict[str, object]:
    fibres = {
        str(y): [list(x) for x in FINE_CONFIGS if quotient_block(x) == y]
        for y in QUOTIENT_CONFIGS
    }
    gauge_invariant = all(
        quotient_block(gauge_action(g, x)) == quotient_block(x)
        for g in GAUGE_GROUP
        for x in FINE_CONFIGS
    )
    left_inverse = all(
        quotient_block(canonical_reconstruct(y)) == y for y in QUOTIENT_CONFIGS
    )
    orbit_recovery = all(gauge_equivalent(x, recovery_projection(x)) for x in FINE_CONFIGS)
    projection_erases_copies = all(
        recovery_projection(gauge_action(g, x)) == recovery_projection(x)
        for g in GAUGE_GROUP
        for x in FINE_CONFIGS
    )
    exact_errors = {
        observable.name: observable_error(
            quotient_block, canonical_reconstruct, observable
        )
        for observable in CHARACTER_BASIS
    }
    return {
        "fine_configuration_count": len(FINE_CONFIGS),
        "gauge_group_count": len(GAUGE_GROUP),
        "effective_orbit_size": len(gauge_orbit(FINE_CONFIGS[0])),
        "quotient_count": len(QUOTIENT_CONFIGS),
        "fibres": fibres,
        "each_fibre_is_one_orbit": all(
            len(points) == 2 and set(map(tuple, points)) == set(gauge_orbit(points[0]))
            for points in fibres.values()
        ),
        "block_is_gauge_invariant": gauge_invariant,
        "B_after_R_is_identity": left_inverse,
        "R_after_B_is_orbit_equivalent_to_identity": orbit_recovery,
        "R_after_B_erases_gauge_copies": projection_erases_copies,
        "basis_observable_errors": exact_errors,
        "all_basis_observables_exactly_recovered": all(
            row["exact_recovery"] for row in exact_errors.values()
        ),
    }


def observable_class_certificate() -> dict[str, object]:
    separates = all(
        y == z
        or any(observable.on_quotient(y) != observable.on_quotient(z) for observable in CHARACTER_BASIS)
        for y in QUOTIENT_CONFIGS
        for z in QUOTIENT_CONFIGS
    )
    evaluation_matrix = [
        [observable.on_quotient(y) for observable in CHARACTER_BASIS]
        for y in QUOTIENT_CONFIGS
    ]
    # The character table is a 4x4 Hadamard matrix; exact elimination records rank.
    matrix = [row[:] for row in evaluation_matrix]
    rank = 0
    for column in range(4):
        pivot = next((row for row in range(rank, 4) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(4):
            if row != rank and matrix[row][column]:
                factor = matrix[row][column]
                matrix[row] = [a - factor * b for a, b in zip(matrix[row], matrix[rank])]
        rank += 1
    closure = all(
        left.multiply(right).coefficients
        == next(
            candidate.coefficients
            for candidate in CHARACTER_BASIS
            if all(
                candidate.on_quotient(y)
                == left.on_quotient(y) * right.on_quotient(y)
                for y in QUOTIENT_CONFIGS
            )
        )
        for left in CHARACTER_BASIS
        for right in CHARACTER_BASIS
    )
    return {
        "basis": [observable.to_json() for observable in CHARACTER_BASIS],
        "separates_quotient_points": separates,
        "evaluation_matrix_rank": rank,
        "invariant_function_space_dimension": len(QUOTIENT_CONFIGS),
        "basis_spans_all_rational_invariant_functions": rank == len(QUOTIENT_CONFIGS),
        "closed_under_products": closure,
        "W02_is_product_of_initial_independent_loops": W01.multiply(W12).coefficients
        == W02.coefficients,
        "declared_norm_submultiplicative": all(
            left.multiply(right).coefficient_norm
            <= left.coefficient_norm * right.coefficient_norm
            for left in CHARACTER_BASIS
            for right in CHARACTER_BASIS
        ),
    }


def counterexamples() -> dict[str, object]:
    def collapse_block(_: FineConfig) -> QuotientConfig:
        return (1, 1)

    erasure_errors = {
        observable.name: observable_error(
            collapse_block, canonical_reconstruct, observable
        )
        for observable in CHARACTER_BASIS
    }
    collapse_erases = all(
        collapse_block(gauge_action(g, x)) == collapse_block(x)
        for g in GAUGE_GROUP
        for x in FINE_CONFIGS
    )

    def labeled_block(x: FineConfig) -> LabeledQuotientConfig:
        fine = validate_fine(x)
        y = quotient_block(fine)
        return (y[0], y[1], fine[0])

    def labeled_reconstruct(label: Sequence[int]) -> FineConfig:
        if len(label) != 3:
            raise ValueError("a labeled quotient has two invariants and one copy sign")
        first, second = validate_quotient(label[:2])
        copy = _validate_sign(label[2], "copy_label")
        return (copy, copy * first, copy * first * second)

    labeled_exact = all(labeled_reconstruct(labeled_block(x)) == x for x in FINE_CONFIGS)
    labeled_erases = all(
        labeled_block(gauge_action(g, x)) == labeled_block(x)
        for g in GAUGE_GROUP
        for x in FINE_CONFIGS
    )
    labeled_errors = {
        observable.name: observable_error(labeled_block, labeled_reconstruct, observable)
        for observable in CHARACTER_BASIS
    }

    hidden_flip = QuotientMap.from_mapping(
        "flip_hidden_W12_coordinate", {y: (y[0], -y[1]) for y in QUOTIENT_CONFIGS}
    )
    incomplete_errors = {
        observable.name: str(quotient_observable_error(hidden_flip, observable))
        for observable in CHARACTER_BASIS
    }
    return {
        "erasure_without_recovery": {
            "block_is_gauge_invariant": collapse_erases,
            "number_of_retained_physical_labels": 1,
            "number_of_true_orbits": len(QUOTIENT_CONFIGS),
            "observable_errors": erasure_errors,
            "recovery_fails": any(
                not row["exact_recovery"] for row in erasure_errors.values()
            ),
        },
        "recovery_without_erasure": {
            "R_labeled_after_B_labeled_is_fine_identity": labeled_exact,
            "all_invariant_observables_exactly_recovered": all(
                row["exact_recovery"] for row in labeled_errors.values()
            ),
            "block_erases_gauge_copies": labeled_erases,
            "retains_vertical_copy_label": not labeled_erases,
            "observable_errors": labeled_errors,
        },
        "incomplete_probe_class": {
            "initial_probe_names": [observable.name for observable in INITIAL_PROBES],
            "map": hidden_flip.name,
            "basis_errors": incomplete_errors,
            "all_initial_probes_recovered": all(
                quotient_observable_error(hidden_flip, observable) == 0
                for observable in INITIAL_PROBES
            ),
            "separating_class_not_recovered": any(
                quotient_observable_error(hidden_flip, observable) != 0
                for observable in CHARACTER_BASIS
            ),
            "hidden_W12_error": incomplete_errors[W12.name],
            "product_W02_error": incomplete_errors[W02.name],
        },
    }


def calibration(run_exhaustive: bool = True) -> dict[str, object]:
    flip_first = QuotientMap.from_mapping(
        "flip_first_loop", {y: (-y[0], y[1]) for y in QUOTIENT_CONFIGS}
    )
    flip_second = QuotientMap.from_mapping(
        "flip_second_loop", {y: (y[0], -y[1]) for y in QUOTIENT_CONFIGS}
    )
    average = InvariantObservable.from_coefficients("(W01+W12)/2", (0, "1/2", "1/2", 0))
    theorem = gauge_quotient_certificate()
    observable_class = observable_class_certificate()
    model_counterexamples = counterexamples()
    composition = composition_certificate(flip_first, flip_second, average)
    exhaustive = exhaustive_composition_check() if run_exhaustive else {
        "not_run": True
    }
    return {
        "schema": "h10-observable-recovery-v1",
        "stage": 77,
        "hypothesis": "H10",
        "claim_level": "C2 exact finite toy theorem",
        "model": {
            "gauge_group": "Z2 at each of two vertices (global diagonal kernel)",
            "graph": "two vertices joined by three parallel edges",
            "fine_space": "{-1,+1}^3",
            "quotient_coordinates": ["W01=e0*e1", "W12=e1*e2"],
            "reconstruction_slice": "e0=+1",
        },
        "quotient_recovery_theorem": theorem,
        "observable_class": observable_class,
        "observable_indexed_examples": {
            "elementary_W01": theorem["basis_observable_errors"][W01.name],
            "elementary_W12": theorem["basis_observable_errors"][W12.name],
            "product_outside_initial_probe_family_W02": theorem["basis_observable_errors"][W02.name],
        },
        "two_step_composition": {
            "theorem": "e_O(g o f) <= e_O(f) + e_O(g)",
            "calibrated_equality_case": composition,
            "exhaustive_finite_check": exhaustive,
        },
        "counterexamples": model_counterexamples,
        "strongest_relation": "exact quotient plus exact recovery of the complete rational invariant observable algebra on the declared finite graph",
        "uniformity_domain": "all 8 fine configurations and all 4 local gauge elements of one fixed finite Z2 graph",
        "guardrails": {
            "nonlinear_SU2_block_map_constructed": False,
            "cutoff_uniform_recovery_proved": False,
            "volume_uniform_recovery_proved": False,
            "continuum_observable_density_proved": False,
            "continuum_Yang_Mills_measure_constructed": False,
            "Osterwalder_Schrader_reconstruction_proved": False,
            "positive_Yang_Mills_mass_gap_proved": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write canonical JSON output")
    parser.add_argument(
        "--skip-exhaustive", action="store_true", help="omit the 262144 composition checks"
    )
    args = parser.parse_args()
    result = calibration(run_exhaustive=not args.skip_exhaustive)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        RESULTS.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
