"""Exact finite theorem model for H7 normalized atlas gluing.

The carrier is a six-atom section of the two-center SU(2) cover.  All
probabilities, partition weights, and coordinate-density transitions are
computed with :class:`fractions.Fraction`, so every asserted gluing and
cocycle identity is exact rather than numerical.

This module proves a C2 *finite atlas theorem*.  It intentionally does not
construct the physical Yang--Mills conditional measure and does not establish
history-uniform exceptional control.
"""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, Mapping, Sequence, Tuple


PLUS = "+"
MINUS = "-"
CHARTS = (PLUS, MINUS)

ATOMS = (
    "plus_pole",
    "plus_bulk",
    "equator_x",
    "equator_y",
    "minus_bulk",
    "minus_pole",
)
OVERLAP = ("equator_x", "equator_y")
EXCEPTIONAL = ("equator_y",)

# Exact unit-quaternion representatives.  The equator points lie in both
# radius-pi/2 charts; the poles show why one center chart cannot cover SU(2).
QUATERNIONS = {
    "plus_pole": (1, 0, 0, 0),
    "plus_bulk": (Fraction(3, 5), Fraction(4, 5), 0, 0),
    "equator_x": (0, 1, 0, 0),
    "equator_y": (0, 0, 1, 0),
    "minus_bulk": (Fraction(-3, 5), Fraction(4, 5), 0, 0),
    "minus_pole": (-1, 0, 0, 0),
}

SUPPORT = {
    PLUS: frozenset(("plus_pole", "plus_bulk", *OVERLAP)),
    MINUS: frozenset((*OVERLAP, "minus_bulk", "minus_pole")),
}

# A subordinate partition of unity.  Every active chart weight is strictly
# positive; inactive chart weights are zero by subordination.
PARTITION = {
    PLUS: {
        "plus_pole": Fraction(1),
        "plus_bulk": Fraction(1),
        "equator_x": Fraction(2, 5),
        "equator_y": Fraction(3, 5),
        "minus_bulk": Fraction(0),
        "minus_pole": Fraction(0),
    },
    MINUS: {
        "plus_pole": Fraction(0),
        "plus_bulk": Fraction(0),
        "equator_x": Fraction(3, 5),
        "equator_y": Fraction(2, 5),
        "minus_bulk": Fraction(1),
        "minus_pole": Fraction(1),
    },
}

# Chart-coordinate carrier masses model the Haar Jacobian in two coordinate
# systems.  Nontrivial rational ratios make omission/inversion detectable.
COORDINATE_MASS = {
    PLUS: {"equator_x": Fraction(2), "equator_y": Fraction(5)},
    MINUS: {"equator_x": Fraction(3), "equator_y": Fraction(2)},
}

# Distinct logarithmic half-turn coordinates in the two center charts.  A
# coordinate v denotes exp((pi/2)v) at +I and -exp((pi/2)v) at -I.  Therefore
# the same equator quaternion is represented by opposite signed axes.
CHART_COORDINATES = {
    PLUS: {"equator_x": (1, 0, 0), "equator_y": (0, 1, 0)},
    MINUS: {"equator_x": (-1, 0, 0), "equator_y": (0, -1, 0)},
}
CENTER_SCALAR = {PLUS: 1, MINUS: -1}


def _validate_probability(mu: Mapping[str, Fraction]) -> None:
    if set(mu) != set(ATOMS):
        raise ValueError("a history must assign every atlas atom exactly once")
    if any(value <= 0 for value in mu.values()):
        raise ValueError("the finite theorem uses positive-mass histories")
    if sum(mu.values(), Fraction(0)) != 1:
        raise ValueError("history masses must sum exactly to one")


def regular_history() -> Dict[str, Fraction]:
    """A positive reference history with nontrivial overlap and exception."""

    return {
        "plus_pole": Fraction(24, 100),
        "plus_bulk": Fraction(20, 100),
        "equator_x": Fraction(12, 100),
        "equator_y": Fraction(8, 100),
        "minus_bulk": Fraction(18, 100),
        "minus_pole": Fraction(18, 100),
    }


def hostile_chart_history(n: int) -> Dict[str, Fraction]:
    """Return a history whose plus-chart mass tends to zero as ``n`` grows.

    With ``delta=1/n``, each plus-chart atom has mass ``delta/4`` and the two
    minus-only atoms split the remaining mass.  The plus-chart mass is exactly
    ``3 delta / 4`` while the normalized plus probability of ``plus_pole`` is
    exactly ``1/3``.
    """

    if n <= 1:
        raise ValueError("n must exceed one")
    delta = Fraction(1, n)
    quarter = delta / 4
    remainder = (1 - delta) / 2
    return {
        "plus_pole": quarter,
        "plus_bulk": quarter,
        "equator_x": quarter,
        "equator_y": quarter,
        "minus_bulk": remainder,
        "minus_pole": remainder,
    }


def hostile_exception_history(n: int) -> Dict[str, Fraction]:
    """Keep atlas coverage fixed while exceptional probability tends to one."""

    if n <= 1:
        raise ValueError("n must exceed one")
    residual = Fraction(1, n)
    ordinary = residual / 5
    return {
        "plus_pole": ordinary,
        "plus_bulk": ordinary,
        "equator_x": ordinary,
        "equator_y": 1 - residual,
        "minus_bulk": ordinary,
        "minus_pole": ordinary,
    }


def check_cover() -> bool:
    """The two chart supports cover every carrier point."""

    return SUPPORT[PLUS] | SUPPORT[MINUS] == frozenset(ATOMS)


def multiplicity(atom: str) -> int:
    return sum(atom in SUPPORT[chart] for chart in CHARTS)


def partition_sum(atom: str) -> Fraction:
    return sum((PARTITION[chart][atom] for chart in CHARTS), Fraction(0))


def chart_mass(mu: Mapping[str, Fraction], chart: str) -> Fraction:
    _validate_probability(mu)
    if chart not in CHARTS:
        raise ValueError("unknown chart")
    return sum((mu[x] * PARTITION[chart][x] for x in ATOMS), Fraction(0))


def chart_conditional(
    mu: Mapping[str, Fraction], chart: str
) -> Dict[str, Fraction]:
    """Return the normalized partition-weighted chart conditional."""

    mass = chart_mass(mu, chart)
    if mass == 0:
        raise ZeroDivisionError("zero-mass chart has no normalized conditional")
    return {x: mu[x] * PARTITION[chart][x] / mass for x in ATOMS}


def event_mass(mu: Mapping[str, Fraction], event: Iterable[str]) -> Fraction:
    chosen = frozenset(event)
    return sum((mu[x] for x in chosen), Fraction(0))


def conditional_event_mass(
    conditional: Mapping[str, Fraction], event: Iterable[str]
) -> Fraction:
    chosen = frozenset(event)
    return sum((conditional[x] for x in chosen), Fraction(0))


def glued_event_mass(mu: Mapping[str, Fraction], event: Iterable[str]) -> Fraction:
    """Reconstruct a global event from normalized local chart laws."""

    return sum(
        (
            chart_mass(mu, chart)
            * conditional_event_mass(chart_conditional(mu, chart), event)
            for chart in CHARTS
        ),
        Fraction(0),
    )


def coordinate_density(
    mu: Mapping[str, Fraction], chart: str, atom: str
) -> Fraction:
    """Density of a chart conditional relative to its coordinate carrier."""

    if atom not in OVERLAP:
        raise ValueError("transition densities are defined on the overlap")
    return chart_conditional(mu, chart)[atom] / COORDINATE_MASS[chart][atom]


def jacobian(source: str, target: str, atom: str) -> Fraction:
    """Coordinate-measure Jacobian ``d kappa_target / d kappa_source``."""

    if source == target:
        return Fraction(1)
    if source not in CHARTS or target not in CHARTS or atom not in OVERLAP:
        raise ValueError("Jacobian requires two atlas charts and an overlap atom")
    return COORDINATE_MASS[target][atom] / COORDINATE_MASS[source][atom]


def transition_factor(
    mu: Mapping[str, Fraction], source: str, target: str, atom: str
) -> Fraction:
    """Full normalized density cocycle, including weights and Jacobian.

    The identity is ``f_target = C_source,target f_source`` with

    ``C = (w_target/w_source)(p_source/p_target) / J_source,target``.
    """

    if source == target:
        return Fraction(1)
    source_weight = PARTITION[source][atom]
    target_weight = PARTITION[target][atom]
    if source_weight <= 0 or target_weight <= 0:
        raise ValueError("transition factor requires a genuine overlap")
    return (
        target_weight
        / source_weight
        * chart_mass(mu, source)
        / chart_mass(mu, target)
        / jacobian(source, target, atom)
    )


def transition_residual(
    mu: Mapping[str, Fraction], source: str, target: str, atom: str
) -> Fraction:
    left = coordinate_density(mu, target, atom)
    right = transition_factor(mu, source, target, atom) * coordinate_density(
        mu, source, atom
    )
    return left - right


def half_turn_exponential(coordinate: Sequence[int]) -> Tuple[int, int, int, int]:
    """Evaluate exp((pi/2)v) exactly for a signed coordinate unit axis."""

    values = tuple(coordinate)
    if (
        len(values) != 3
        or any(type(value) is not int for value in values)
        or sum(abs(value) for value in values) != 1
    ):
        raise ValueError("a half-turn coordinate must be a signed integer unit axis")
    return (0, values[0], values[1], values[2])


def reconstruct_from_chart_coordinate(
    chart: str, coordinate: Sequence[int]
) -> Tuple[int, int, int, int]:
    """Apply the declared center and exact half-turn exponential."""

    if chart not in CHARTS:
        raise ValueError("unknown chart")
    exponential = half_turn_exponential(coordinate)
    center = CENTER_SCALAR[chart]
    return tuple(center * value for value in exponential)  # type: ignore[return-value]


def reconstruct_overlap_coordinate(
    atom: str,
    chart: str,
    coordinate_override: Sequence[int] | None = None,
) -> Tuple[int, int, int, int]:
    """Reconstruct an overlap quaternion from genuinely chart-relative data."""

    if atom not in OVERLAP or chart not in CHARTS:
        raise ValueError("only overlap coordinates admit both reconstructions")
    coordinate = (
        CHART_COORDINATES[chart][atom]
        if coordinate_override is None
        else tuple(coordinate_override)
    )
    return reconstruct_from_chart_coordinate(chart, coordinate)


@dataclass(frozen=True)
class ExceptionalDecomposition:
    regular_chart_coefficients: Dict[str, Fraction]
    exceptional_coefficient: Fraction
    regular_chart_conditionals: Dict[str, Dict[str, Fraction]]
    exceptional_conditional: Dict[str, Fraction]


def exceptional_decomposition(
    mu: Mapping[str, Fraction],
) -> ExceptionalDecomposition:
    """Split the global law into two regular chart channels and one exception."""

    _validate_probability(mu)
    good = frozenset(ATOMS) - frozenset(EXCEPTIONAL)
    coefficients: Dict[str, Fraction] = {}
    conditionals: Dict[str, Dict[str, Fraction]] = {}
    for chart in CHARTS:
        raw = {
            x: mu[x] * PARTITION[chart][x] if x in good else Fraction(0)
            for x in ATOMS
        }
        coefficient = sum(raw.values(), Fraction(0))
        coefficients[chart] = coefficient
        conditionals[chart] = {x: raw[x] / coefficient for x in ATOMS}
    epsilon = event_mass(mu, EXCEPTIONAL)
    exc_conditional = {
        x: (mu[x] / epsilon if x in EXCEPTIONAL else Fraction(0)) for x in ATOMS
    }
    if sum(coefficients.values(), Fraction(0)) + epsilon != 1:
        raise AssertionError("exceptional-channel coefficients do not sum to one")
    return ExceptionalDecomposition(
        regular_chart_coefficients=coefficients,
        exceptional_coefficient=epsilon,
        regular_chart_conditionals=conditionals,
        exceptional_conditional=exc_conditional,
    )


def exceptional_glued_event_mass(
    mu: Mapping[str, Fraction], event: Iterable[str]
) -> Fraction:
    decomposition = exceptional_decomposition(mu)
    total = decomposition.exceptional_coefficient * conditional_event_mass(
        decomposition.exceptional_conditional, event
    )
    for chart in CHARTS:
        total += decomposition.regular_chart_coefficients[chart] * conditional_event_mass(
            decomposition.regular_chart_conditionals[chart], event
        )
    return total


def all_events() -> Iterable[Tuple[str, ...]]:
    for size in range(len(ATOMS) + 1):
        yield from itertools.combinations(ATOMS, size)


def two_block_overlap_certificate(mu: Mapping[str, Fraction]) -> Dict[str, object]:
    """Check adjacent blocks that use opposite charts on one retained edge.

    Block L uses the plus chart and block R the minus chart.  On either overlap
    atom their shared retained edge reconstructs exactly.  The density change
    along ``+ -> - -> +`` and the four-step product-word square both have unit
    cocycle.  This is a finite shared-edge theorem, not a full lattice forest.
    """

    records = []
    for atom in OVERLAP:
        forward = transition_factor(mu, PLUS, MINUS, atom)
        backward = transition_factor(mu, MINUS, PLUS, atom)
        square = forward * backward * forward * backward
        plus_coordinate = CHART_COORDINATES[PLUS][atom]
        minus_coordinate = CHART_COORDINATES[MINUS][atom]
        plus_quaternion = reconstruct_overlap_coordinate(atom, PLUS)
        minus_quaternion = reconstruct_overlap_coordinate(atom, MINUS)
        hostile_minus = reconstruct_overlap_coordinate(
            atom, MINUS, coordinate_override=plus_coordinate
        )
        records.append(
            {
                "atom": atom,
                "plus_chart_coordinate": plus_coordinate,
                "minus_chart_coordinate": minus_coordinate,
                "chart_coordinates_are_distinct": plus_coordinate != minus_coordinate,
                "plus_reconstructed_quaternion": plus_quaternion,
                "minus_reconstructed_quaternion": minus_quaternion,
                "same_retained_quaternion": plus_quaternion == minus_quaternion == QUATERNIONS[atom],
                "hostile_same_sign_minus_coordinate": hostile_minus,
                "hostile_coordinate_perturbation_detected": hostile_minus != plus_quaternion,
                "round_trip_cocycle": forward * backward,
                "product_word_square_cocycle": square,
                "transition_residual": transition_residual(mu, PLUS, MINUS, atom),
            }
        )
    return {
        "records": records,
        "all_shared_coordinates_exact": all(
            record["chart_coordinates_are_distinct"]
            and record["same_retained_quaternion"]
            and record["hostile_coordinate_perturbation_detected"]
            for record in records
        ),
        "all_cocycles_exact": all(
            record["round_trip_cocycle"] == 1
            and record["product_word_square_cocycle"] == 1
            and record["transition_residual"] == 0
            for record in records
        ),
    }


def _fraction_record(value: Fraction) -> Dict[str, object]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "exact": str(value),
        "decimal": float(value),
    }


def _jsonify(value: object) -> object:
    if isinstance(value, Fraction):
        return _fraction_record(value)
    if isinstance(value, dict):
        return {str(key): _jsonify(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonify(item) for item in value]
    return value


def calibration() -> Dict[str, object]:
    mu = regular_history()
    maximum_gluing_residual = max(
        abs(event_mass(mu, event) - glued_event_mass(mu, event))
        for event in all_events()
    )
    maximum_exceptional_residual = max(
        abs(event_mass(mu, event) - exceptional_glued_event_mass(mu, event))
        for event in all_events()
    )
    transition_records = {
        atom: {
            "jacobian_plus_to_minus": jacobian(PLUS, MINUS, atom),
            "factor_plus_to_minus": transition_factor(mu, PLUS, MINUS, atom),
            "factor_minus_to_plus": transition_factor(mu, MINUS, PLUS, atom),
            "round_trip": transition_factor(mu, PLUS, MINUS, atom)
            * transition_factor(mu, MINUS, PLUS, atom),
            "density_residual": transition_residual(mu, PLUS, MINUS, atom),
        }
        for atom in OVERLAP
    }
    hostile_records = []
    for n in (4, 16, 256, 65536):
        hostile = hostile_chart_history(n)
        plus_mass = chart_mass(hostile, PLUS)
        pole_numerator = hostile["plus_pole"]
        pole_conditional = chart_conditional(hostile, PLUS)["plus_pole"]
        hostile_records.append(
            {
                "n": n,
                "plus_chart_mass": plus_mass,
                "unnormalized_plus_pole_numerator": pole_numerator,
                "normalized_plus_pole_probability": pole_conditional,
                "amplification": pole_conditional / pole_numerator,
            }
        )
    exceptional_records = []
    for n in (4, 16, 256, 65536):
        hostile = hostile_exception_history(n)
        exceptional_records.append(
            {
                "n": n,
                "atlas_coverage_fraction": Fraction(1),
                "exceptional_probability": event_mass(hostile, EXCEPTIONAL),
            }
        )
    result = {
        "stage": 74,
        "hypothesis": "H7 atlas-relative locality",
        "theorem": "exact normalized gluing on a finite two-center atlas",
        "claim_level": "C2 finite atlas theorem",
        "carrier": {
            "atoms": ATOMS,
            "charts": {chart: sorted(SUPPORT[chart]) for chart in CHARTS},
            "overlap": OVERLAP,
            "exceptional_channel": EXCEPTIONAL,
            "cover_exact": check_cover(),
            "maximum_multiplicity": max(multiplicity(atom) for atom in ATOMS),
            "partition_sums": {atom: partition_sum(atom) for atom in ATOMS},
            "chart_coordinates": CHART_COORDINATES,
            "coordinate_reconstruction": (
                "center(chart) times exp((pi/2) coordinate), evaluated exactly "
                "on signed unit axes"
            ),
        },
        "regular_history": {
            "probability": mu,
            "chart_masses": {chart: chart_mass(mu, chart) for chart in CHARTS},
            "chart_conditional_sums": {
                chart: sum(chart_conditional(mu, chart).values(), Fraction(0))
                for chart in CHARTS
            },
            "exceptional_probability": event_mass(mu, EXCEPTIONAL),
        },
        "global_gluing": {
            "events_exhaustively_checked": 2 ** len(ATOMS),
            "maximum_exact_residual": maximum_gluing_residual,
            "maximum_exceptional_channel_residual": maximum_exceptional_residual,
        },
        "transition_cocycle": transition_records,
        "two_block_overlap": two_block_overlap_certificate(mu),
        "hostile_small_chart_histories": hostile_records,
        "coverage_probability_separation": exceptional_records,
        "guardrails": {
            "physical_boundary_uniform_SU2_kernel_proved": False,
            "history_uniform_exceptional_bound_proved": False,
            "full_boundary_rooted_forest_gluing_proved": False,
            "RG_iteration_proved": False,
            "continuum_or_mass_gap_proved": False,
            "next_physical_target": "H7-PT1 boundary-uniform normalized nonlinear SU(2) atlas reconstruction",
        },
    }
    return _jsonify(result)  # type: ignore[return-value]


def write_results(path: Path) -> None:
    path.write_text(json.dumps(calibration(), indent=2, sort_keys=True) + "\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", type=Path, help="write canonical JSON results")
    args = parser.parse_args(argv)
    results = calibration()
    if args.write:
        args.write.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    else:
        print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
