"""A frustrated-conditioning obstruction on the side-two 4D SU(2) block.

An interior link belongs to six plaquettes.  Center-valued assignments of the
other links can realize five identity staples and one minus-identity staple.
Conditioned on those links, the selected link has density

    p_t(U)^5 p_t(-U) dU.

The weak-coupling class-angle rate is

    I(theta)=5 theta^2 + (pi-theta)^2,

with minimizer theta=pi/6.  The frustrated plaquette therefore has angle
5pi/6, not a small curvature.  This gives an exact obstruction to any proof
that requires a rare-bad-plaquette bound uniform over every microscopic
boundary conditioning.

The obstruction is restricted.  It does not rule out contour expansions,
good-collar conditioning, multi-link block integration, or full-measure
dependent polymer estimates that charge the frustrating boundary itself.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import platform
import sys
from typing import Any

import numpy as np


STAGE08 = Path(__file__).resolve().parents[1] / "08_su2_nonlinear_block_geometry"
if str(STAGE08) not in sys.path:
    sys.path.insert(0, str(STAGE08))

from su2_nonlinear_block_geometry import build_block_complex  # noqa: E402


@dataclass(frozen=True)
class StapleRealizationCertificate:
    selected_link_index: int
    selected_link: tuple[tuple[int, ...], int]
    incident_plaquette_indices: tuple[int, ...]
    incidence_degree: int
    remaining_link_variables: int
    center_staple_map_rank: int
    target_incident_position: int
    requested_staple_bits: tuple[int, ...]
    realized_staple_bits: tuple[int, ...]
    negative_center_link_indices: tuple[int, ...]
    surjective: bool
    target_realized: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ConditionalLawCertificate:
    incident_plaquettes: int
    identity_staples: int
    negative_identity_staples: int
    density_formula: str
    radial_density_formula: str
    target_plaquette_angle_formula: str
    exact_center_conditioning: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RateObstructionCertificate:
    incident_degree: int
    curvature_radius: float
    rate_formula: str
    minimizer_angle: float
    minimum_rate: float
    target_angle_at_minimizer: float
    good_region_start: float
    good_event_rate_infimum: float
    good_event_rate_gap: float
    scaled_log_probability_limit: float
    bad_probability_tends_to_one: bool
    uniform_microscopic_conditional_tail_possible: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class NumericalConditionalCalibration:
    time: float
    curvature_radius: float
    quadrature_nodes: int
    mode_angle: float
    target_angle_at_mode: float
    log_good_probability: float
    bad_probability: float
    scaled_negative_log_good_probability: float
    exact_rate_gap: float
    scaled_rate_relative_error: float
    numerical_only: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _gf2_rank(matrix: np.ndarray) -> int:
    a = np.asarray(matrix, dtype=np.uint8).copy() % 2
    row = 0
    for col in range(a.shape[1]):
        pivots = np.flatnonzero(a[row:, col])
        if len(pivots) == 0:
            continue
        pivot = row + int(pivots[0])
        a[[row, pivot]] = a[[pivot, row]]
        for other in range(a.shape[0]):
            if other != row and a[other, col]:
                a[other] ^= a[row]
        row += 1
        if row == a.shape[0]:
            break
    return row


def _gf2_solve(matrix: np.ndarray, target: np.ndarray) -> np.ndarray:
    a = np.asarray(matrix, dtype=np.uint8).copy() % 2
    b = np.asarray(target, dtype=np.uint8).copy() % 2
    if a.ndim != 2 or b.shape != (a.shape[0],):
        raise ValueError("incompatible GF(2) system")
    augmented = np.concatenate((a, b[:, None]), axis=1)
    row = 0
    pivots: list[int] = []
    for col in range(a.shape[1]):
        candidates = np.flatnonzero(augmented[row:, col])
        if len(candidates) == 0:
            continue
        pivot = row + int(candidates[0])
        augmented[[row, pivot]] = augmented[[pivot, row]]
        for other in range(a.shape[0]):
            if other != row and augmented[other, col]:
                augmented[other] ^= augmented[row]
        pivots.append(col)
        row += 1
        if row == a.shape[0]:
            break
    for remaining in range(row, a.shape[0]):
        if not augmented[remaining, :-1].any() and augmented[remaining, -1]:
            raise ValueError("GF(2) system is inconsistent")
    solution = np.zeros(a.shape[1], dtype=np.uint8)
    for pivot_row, pivot_col in enumerate(pivots):
        solution[pivot_col] = augmented[pivot_row, -1]
    if not np.array_equal((a @ solution) % 2, b):
        raise RuntimeError("GF(2) solver verification failed")
    return solution


def staple_realization_certificate(
    target_incident_position: int = 0,
) -> StapleRealizationCertificate:
    """Realize one negative-center staple around a degree-six link."""

    block = build_block_complex()
    link_degrees = np.sum(np.abs(block.d1), axis=0).astype(int)
    candidates = np.flatnonzero(link_degrees == 6)
    if len(candidates) == 0:
        raise RuntimeError("the block contains no degree-six link")
    selected = int(candidates[0])
    incident = tuple(int(i) for i in np.flatnonzero(block.d1[:, selected]))
    if not 0 <= target_incident_position < len(incident):
        raise ValueError("target_incident_position is outside the incident set")
    remaining = tuple(i for i in range(len(block.edges)) if i != selected)
    # Center signs ignore orientation because (-I)^(-1)=-I.
    staple_map = (
        np.abs(block.d1[np.ix_(incident, remaining)]).astype(np.uint8) % 2
    )
    requested = np.zeros(len(incident), dtype=np.uint8)
    requested[target_incident_position] = 1
    assignment = _gf2_solve(staple_map, requested)
    realized = (staple_map @ assignment) % 2
    negative_links = tuple(
        remaining[i] for i in np.flatnonzero(assignment)
    )
    rank = _gf2_rank(staple_map)
    return StapleRealizationCertificate(
        selected_link_index=selected,
        selected_link=block.edges[selected],
        incident_plaquette_indices=incident,
        incidence_degree=len(incident),
        remaining_link_variables=len(remaining),
        center_staple_map_rank=rank,
        target_incident_position=target_incident_position,
        requested_staple_bits=tuple(int(x) for x in requested),
        realized_staple_bits=tuple(int(x) for x in realized),
        negative_center_link_indices=negative_links,
        surjective=rank == len(incident),
        target_realized=np.array_equal(requested, realized),
    )


def conditional_law_certificate() -> ConditionalLawCertificate:
    realization = staple_realization_certificate()
    degree = realization.incidence_degree
    return ConditionalLawCertificate(
        incident_plaquettes=degree,
        identity_staples=degree - 1,
        negative_identity_staples=1,
        density_formula="gamma_t(dU) proportional to p_t(U)^5 p_t(-U) dU",
        radial_density_formula=(
            "gamma_t(dtheta) proportional to sin(theta)^2 "
            "p_t(theta)^5 p_t(pi-theta) dtheta"
        ),
        target_plaquette_angle_formula="theta_target=pi-theta",
        exact_center_conditioning=(
            realization.surjective and realization.target_realized
        ),
    )


def rate_obstruction_certificate(
    curvature_radius: float = 0.0082,
    incident_degree: int = 6,
) -> RateObstructionCertificate:
    rho = float(curvature_radius)
    degree = int(incident_degree)
    if not math.isfinite(rho) or not 0.0 < rho < math.pi:
        raise ValueError("curvature_radius must lie in (0, pi)")
    if degree < 2:
        raise ValueError("incident_degree must be at least two")
    theta_star = math.pi / degree
    target_angle = math.pi - theta_star
    minimum = math.pi**2 * (degree - 1.0) / degree
    good_start = math.pi - rho
    if rho < target_angle:
        good_infimum = (
            (degree - 1.0) * good_start**2 + (math.pi - good_start) ** 2
        )
        gap = degree * (target_angle - rho) ** 2
        tends_bad = True
    else:
        good_infimum = minimum
        gap = 0.0
        tends_bad = False
    return RateObstructionCertificate(
        incident_degree=degree,
        curvature_radius=rho,
        rate_formula=f"I_{degree}(theta)=({degree}-1) theta^2+(pi-theta)^2",
        minimizer_angle=theta_star,
        minimum_rate=minimum,
        target_angle_at_minimizer=target_angle,
        good_region_start=good_start,
        good_event_rate_infimum=good_infimum,
        good_event_rate_gap=gap,
        scaled_log_probability_limit=-gap,
        bad_probability_tends_to_one=tends_bad,
        uniform_microscopic_conditional_tail_possible=not tends_bad,
    )


def log_su2_image_kernel_shape(
    theta: float,
    time: float,
    image_cutoff: int = 2,
) -> float:
    """Stable logarithm of the Poisson-image heat-kernel shape.

    A theta-independent normalization cancels from every conditional ratio.
    The signed log-sum avoids underflow at the Stage 09 ultraviolet time.
    """

    theta = float(theta)
    time = float(time)
    if not 0.0 < theta < math.pi:
        raise ValueError("theta must lie strictly between zero and pi")
    if not math.isfinite(time) or time <= 0.0:
        raise ValueError("time must be finite and positive")
    if image_cutoff < 1:
        raise ValueError("image_cutoff must be positive")
    logs: list[float] = []
    signs: list[float] = []
    for k in range(-image_cutoff, image_cutoff + 1):
        x = theta + 2.0 * math.pi * k
        if x == 0.0:
            continue
        logs.append(math.log(abs(x)) - x * x / (2.0 * time))
        signs.append(1.0 if x > 0.0 else -1.0)
    maximum = max(logs)
    signed = math.fsum(
        sign * math.exp(value - maximum) for sign, value in zip(signs, logs)
    )
    if signed <= 0.0:
        raise ArithmeticError("truncated image shape lost positivity")
    return maximum + math.log(signed) - math.log(math.sin(theta))


@lru_cache(maxsize=8)
def _legendre_rule(nodes: int) -> tuple[np.ndarray, np.ndarray]:
    if nodes < 32:
        raise ValueError("quadrature requires at least 32 nodes")
    x, w = np.polynomial.legendre.leggauss(nodes)
    return x, w


def _log_integral(log_density, left: float, right: float, nodes: int) -> float:
    if not left < right:
        raise ValueError("integration interval must be nonempty")
    x, w = _legendre_rule(nodes)
    half = 0.5 * (right - left)
    midpoint = 0.5 * (right + left)
    theta = midpoint + half * x
    logs = np.array(
        [log_density(float(value)) for value in theta], dtype=float
    ) + np.log(half * w)
    maximum = float(np.max(logs))
    return maximum + math.log(math.fsum(np.exp(logs - maximum)))


def numerical_conditional_calibration(
    time: float,
    curvature_radius: float = 0.0082,
    incident_degree: int = 6,
    quadrature_nodes: int = 512,
) -> NumericalConditionalCalibration:
    """Calibrate the exact conditional law in logarithmic arithmetic."""

    time = float(time)
    rho = float(curvature_radius)
    if not math.isfinite(time) or time <= 0.0:
        raise ValueError("time must be finite and positive")
    rate = rate_obstruction_certificate(rho, incident_degree)

    def log_density(theta: float) -> float:
        return (
            (incident_degree - 1)
            * log_su2_image_kernel_shape(theta, time)
            + log_su2_image_kernel_shape(math.pi - theta, time)
            + 2.0 * math.log(math.sin(theta))
        )

    log_total = _log_integral(log_density, 0.0, math.pi, quadrature_nodes)
    log_good = _log_integral(
        log_density, math.pi - rho, math.pi, quadrature_nodes
    )
    log_probability = log_good - log_total
    bad_probability = -math.expm1(log_probability) if log_probability > -50.0 else 1.0
    scaled = -2.0 * time * log_probability

    theta_star = rate.minimizer_angle
    window = max(0.05, 8.0 * math.sqrt(time))
    left = max(1.0e-12, theta_star - window)
    right = min(math.pi - 1.0e-12, theta_star + window)
    grid = np.linspace(left, right, 4001)
    values = np.array([log_density(float(theta)) for theta in grid])
    mode = float(grid[int(np.argmax(values))])
    relative = abs(scaled - rate.good_event_rate_gap) / rate.good_event_rate_gap
    return NumericalConditionalCalibration(
        time=time,
        curvature_radius=rho,
        quadrature_nodes=quadrature_nodes,
        mode_angle=mode,
        target_angle_at_mode=math.pi - mode,
        log_good_probability=log_probability,
        bad_probability=bad_probability,
        scaled_negative_log_good_probability=scaled,
        exact_rate_gap=rate.good_event_rate_gap,
        scaled_rate_relative_error=relative,
        numerical_only=True,
    )


def calibration() -> dict[str, Any]:
    realization = staple_realization_certificate()
    law = conditional_law_certificate()
    rate = rate_obstruction_certificate()
    numerical = [
        numerical_conditional_calibration(time).to_dict()
        for time in (0.05, 0.02, 0.01, 3.0e-6)
    ]
    return {
        "scope": (
            "exact center-staple realization and small-time conditional-rate "
            "obstruction on one degree-six link of the finite 2^4 SU(2) block; "
            "not a no-go theorem for contour or dependent-polymer methods"
        ),
        "staple_realization": realization.to_dict(),
        "conditional_law": law.to_dict(),
        "rate_obstruction": rate.to_dict(),
        "numerical_calibration": numerical,
        "first_unproved_implication": (
            "construct a volume-uniform contour or polymer activity bound that "
            "charges the frustrating boundary pattern instead of taking a "
            "supremum over arbitrary microscopic conditionings"
        ),
        "claim_level": "C2 restricted obstruction theorem",
        "frontier_flags": {
            "uniform_single_link_dobrushin_route": False,
            "good_collar_conditional_bound": False,
            "multi_link_block_activity": False,
            "dependent_polymer": False,
            "topological_sector_control": False,
            "multiscale_iteration": False,
            "continuum_yang_mills": False,
            "hamiltonian_mass_gap": False,
        },
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json", "table"), default="table")
    args = parser.parse_args()
    result = calibration()
    if args.output == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    realization = result["staple_realization"]
    rate = result["rate_obstruction"]
    witness = result["numerical_calibration"][-1]
    print(f"center-staple map rank: {realization['center_staple_map_rank']}")
    print(f"conditional minimizer theta*: {rate['minimizer_angle']:.12f}")
    print(
        "frustrated target angle: "
        f"{rate['target_angle_at_minimizer']:.12f}"
    )
    print(f"good-event rate gap: {rate['good_event_rate_gap']:.12f}")
    print(
        "Stage 09 scaled -log good probability: "
        f"{witness['scaled_negative_log_good_probability']:.12f}"
    )
    print(
        "uniform microscopic conditional tail possible: "
        f"{rate['uniform_microscopic_conditional_tail_possible']}"
    )


if __name__ == "__main__":
    main()

