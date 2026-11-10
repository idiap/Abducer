"""Certified action--Haar-entropy optimization for coherent SU(2) collars.

The Stage 15 logarithmic conditional bound is

 L(delta) = -log v(delta) + log(rho/sin rho)
            +(m+1)log c_t -[rho^2-m(eta+delta)^2]/(2t).

On its admissible interval, the unique interior minimizer solves

    v'(delta)/v(delta) = m(eta+delta)/t.

The equation is independent of rho.  This module brackets it by bisection,
solves the curvature threshold for a declared probability budget, and then
re-optimizes the Stage 25 K+R radius instead of retaining its arbitrary equal
budget split.  All statements remain conditional on the coherent collar.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any


PACKAGE = Path(__file__).resolve().parents[1]
for sibling in (
    "07_su2_heat_kernel_initializer",
    "22_sharp_nonlinear_overlap",
    "25_one_scale_kr_composition",
    "27_su2_haar_entropy",
):
    path = PACKAGE / sibling
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from su2_heat_kernel_initializer import image_derivative_bounds  # noqa: E402
from sharp_nonlinear_overlap import maximal_certified_radius  # noqa: E402
from one_scale_kr_composition import local_reference_budget  # noqa: E402
from su2_haar_entropy import (  # noqa: E402
    normalized_haar_ball_volume,
    normalized_haar_sphere_density,
)


HEAT_TIME = 3.0e-6
INCIDENT_STAPLES = 6
TARGET_WEIGHTED_CEILING = 0.002430277501841998
STAGE26_RESIDUAL_CEILING = 0.001215138750921001


@dataclass(frozen=True)
class DeltaOptimizerCertificate:
    heat_time: float
    curvature_radius: float
    coherence_radius: float
    incident_staples: int
    admissible_delta_upper: float
    selected_delta: float
    stationarity_left: float
    stationarity_right: float
    stationarity_residual: float
    log_probability_upper: float
    probability_upper: float
    finite_time_energy_gap: float
    unique_interior_minimum: bool
    bisection_iterations: int
    coherent_collar_required: bool

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


@dataclass(frozen=True)
class CurvatureThresholdCertificate:
    target_probability: float
    coherence_radius: float
    selected_curvature_radius: float
    selected_local_radius: float
    selected_delta: float
    attained_log_bound: float
    target_logarithm: float
    below_maximum_nonlinear_radius: bool
    monotone_grid_verified: bool

    def to_dict(self) -> dict[str, float | bool]:
        return asdict(self)


@dataclass(frozen=True)
class JointKRCertificate:
    coherence_radius: float
    selected_local_radius: float
    curvature_chain_radius: float
    maximum_nonlinear_radius: float
    reference_bad_ceiling: float
    comparison_log_loss: float
    corrected_reference_ceiling: float
    coherent_bad_ceiling: float
    combined_ceiling: float
    target_ceiling: float
    strict_target_met: bool
    radius_inside_nonlinear_window: bool
    collar_occurrence_certified: bool
    physical_kernel_decomposition_certified: bool

    def to_dict(self) -> dict[str, float | bool]:
        return asdict(self)


def _positive(name: str, value: float) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return x


def _nonnegative(name: str, value: float) -> float:
    x = float(value)
    if not math.isfinite(x) or x < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return x


def stationarity_balance(delta: float, heat_time: float, coherence_radius: float, incident_staples: int) -> float:
    d = _positive("delta", delta)
    t = _positive("heat_time", heat_time)
    eta = _nonnegative("coherence_radius", coherence_radius)
    m = int(incident_staples)
    if m < 2 or d >= 1.0:
        raise ValueError("require at least two staples and 0<delta<1")
    volume = normalized_haar_ball_volume(d)
    return normalized_haar_sphere_density(d) / volume - m * (eta + d) / t


def stationary_delta(heat_time: float, coherence_radius: float, incident_staples: int = INCIDENT_STAPLES) -> tuple[float, float, float]:
    """Return a sign-bracketed root of the unique stationarity equation."""

    t = _positive("heat_time", heat_time)
    eta = _nonnegative("coherence_radius", coherence_radius)
    m = int(incident_staples)
    if m < 2:
        raise ValueError("incident_staples must be at least two")
    left, right = 1.0e-12, min(0.25, 8.0 * math.sqrt(t / m) + 2.0 * eta)
    f_left = stationarity_balance(left, t, eta, m)
    f_right = stationarity_balance(right, t, eta, m)
    while f_right >= 0.0 and right < 0.99:
        right = min(0.99, 2.0 * right)
        f_right = stationarity_balance(right, t, eta, m)
    if f_left <= 0.0 or f_right >= 0.0:
        raise ArithmeticError("failed to bracket the stationary denominator radius")
    original_left, original_right = left, right
    for _ in range(120):
        middle = 0.5 * (left + right)
        if stationarity_balance(middle, t, eta, m) > 0.0:
            left = middle
        else:
            right = middle
    return 0.5 * (left + right), original_left, original_right


def log_conditional_bound(heat_time: float, curvature_radius: float, coherence_radius: float, delta: float, incident_staples: int = INCIDENT_STAPLES) -> float:
    t = _positive("heat_time", heat_time)
    rho = _positive("curvature_radius", curvature_radius)
    eta = _nonnegative("coherence_radius", coherence_radius)
    d = _positive("delta", delta)
    m = int(incident_staples)
    if m < 2 or rho >= math.pi / 2.0:
        raise ValueError("invalid staple count or curvature radius")
    gap = rho * rho - m * (eta + d) ** 2
    if gap <= 0.0:
        raise ValueError("the finite-time energy gap must be positive")
    q = image_derivative_bounds(t, rho, included_images=1).q0
    ratio = (1.0 + q) / (1.0 - q)
    return (
        -math.log(normalized_haar_ball_volume(d))
        + math.log(rho / math.sin(rho))
        + (m + 1.0) * math.log(ratio)
        - gap / (2.0 * t)
    )


def optimize_delta(heat_time: float, curvature_radius: float, coherence_radius: float, incident_staples: int = INCIDENT_STAPLES) -> DeltaOptimizerCertificate:
    t = _positive("heat_time", heat_time)
    rho = _positive("curvature_radius", curvature_radius)
    eta = _nonnegative("coherence_radius", coherence_radius)
    m = int(incident_staples)
    if m < 2:
        raise ValueError("incident_staples must be at least two")
    delta, bracket_left, bracket_right = stationary_delta(t, eta, m)
    upper = rho / math.sqrt(m) - eta
    if upper <= delta:
        raise ValueError("curvature radius does not admit the interior entropy optimum")
    log_bound = log_conditional_bound(t, rho, eta, delta, m)
    gap = rho * rho - m * (eta + delta) ** 2
    left_term = normalized_haar_sphere_density(delta) / normalized_haar_ball_volume(delta)
    right_term = m * (eta + delta) / t
    return DeltaOptimizerCertificate(
        heat_time=t,
        curvature_radius=rho,
        coherence_radius=eta,
        incident_staples=m,
        admissible_delta_upper=upper,
        selected_delta=delta,
        stationarity_left=left_term,
        stationarity_right=right_term,
        stationarity_residual=left_term - right_term,
        log_probability_upper=log_bound,
        probability_upper=1.0 if log_bound >= 0.0 else math.exp(log_bound),
        finite_time_energy_gap=gap,
        unique_interior_minimum=True,
        bisection_iterations=120,
        coherent_collar_required=True,
    )


def curvature_threshold(target_probability: float, coherence_radius: float, heat_time: float = HEAT_TIME, incident_staples: int = INCIDENT_STAPLES) -> CurvatureThresholdCertificate:
    target = float(target_probability)
    eta = _nonnegative("coherence_radius", coherence_radius)
    t = _positive("heat_time", heat_time)
    m = int(incident_staples)
    if not math.isfinite(target) or not 0.0 < target < 1.0:
        raise ValueError("target_probability must lie in (0,1)")
    delta, _, _ = stationary_delta(t, eta, m)
    low = math.sqrt(m) * (eta + delta) * (1.0 + 1.0e-10)
    high = 2.0 * maximal_certified_radius(t, 0.001)
    target_log = math.log(target)
    if log_conditional_bound(t, high, eta, delta, m) > target_log:
        raise ValueError("target is not met inside the certified nonlinear window")
    grid = [low + (high - low) * j / 256.0 for j in range(257)]
    values = [log_conditional_bound(t, r, eta, delta, m) for r in grid]
    monotone = all(values[j + 1] < values[j] for j in range(len(values) - 1))
    if not monotone:
        raise ArithmeticError("curvature monotonicity failed on the certified grid")
    for _ in range(120):
        middle = 0.5 * (low + high)
        if log_conditional_bound(t, middle, eta, delta, m) > target_log:
            low = middle
        else:
            high = middle
    selected = high
    return CurvatureThresholdCertificate(
        target_probability=target,
        coherence_radius=eta,
        selected_curvature_radius=selected,
        selected_local_radius=selected / 2.0,
        selected_delta=delta,
        attained_log_bound=log_conditional_bound(t, selected, eta, delta, m),
        target_logarithm=target_log,
        below_maximum_nonlinear_radius=selected / 2.0 < maximal_certified_radius(t, 0.001),
        monotone_grid_verified=monotone,
    )


def joint_kr_certificate(coherence_radius: float = 0.001, target_ceiling: float = TARGET_WEIGHTED_CEILING) -> JointKRCertificate:
    eta = _nonnegative("coherence_radius", coherence_radius)
    target = float(target_ceiling)
    if not math.isfinite(target) or not 0.0 < target < 1.0:
        raise ValueError("target_ceiling must lie in (0,1)")
    maximum = maximal_certified_radius(HEAT_TIME, 0.001)

    def budget(radius: float) -> tuple[float, float, float, float, float]:
        reference, ell, corrected = local_reference_budget(radius)
        coherent = optimize_delta(HEAT_TIME, 2.0 * radius, eta).probability_upper
        return reference, ell, corrected, coherent, corrected + coherent

    low = max(0.5 * curvature_threshold(0.5, eta).selected_curvature_radius, 0.005)
    high = maximum * (1.0 - 1.0e-10)
    if budget(high)[-1] >= target:
        raise ValueError("joint K+R target does not close inside nonlinear window")
    for _ in range(120):
        middle = 0.5 * (low + high)
        if budget(middle)[-1] >= target:
            low = middle
        else:
            high = middle
    # Move a controlled amount into the strict feasible side.
    selected = high + 1.0e-4 * (maximum - high)
    reference, ell, corrected, coherent, combined = budget(selected)
    return JointKRCertificate(
        coherence_radius=eta,
        selected_local_radius=selected,
        curvature_chain_radius=2.0 * selected,
        maximum_nonlinear_radius=maximum,
        reference_bad_ceiling=reference,
        comparison_log_loss=ell,
        corrected_reference_ceiling=corrected,
        coherent_bad_ceiling=coherent,
        combined_ceiling=combined,
        target_ceiling=target,
        strict_target_met=combined < target,
        radius_inside_nonlinear_window=selected < maximum,
        collar_occurrence_certified=False,
        physical_kernel_decomposition_certified=False,
    )


def calibration() -> dict[str, Any]:
    selected_registry = json.loads((PACKAGE / "partition_ratio_frontier_parameter_registry.json").read_text())
    old_radius = selected_registry["stage25_kr_budget"]["selected_radius"]
    return {
        "claim_level": "C2 coherent-collar conditional theorem and certified radius optimization",
        "stationarity_equation": "v'(delta)/v(delta)=m(eta+delta)/t",
        "ideal_stage26_threshold": curvature_threshold(STAGE26_RESIDUAL_CEILING, 0.0).to_dict(),
        "declared_stage26_threshold": curvature_threshold(STAGE26_RESIDUAL_CEILING, 0.001).to_dict(),
        "old_equal_split_radius_certificate": optimize_delta(HEAT_TIME, 2.0 * old_radius, 0.001).to_dict(),
        "joint_kr_optimized": joint_kr_certificate().to_dict(),
        "coherent_channel_budget_closed_conditionally": True,
        "coherent_collar_occurrence_under_complete_measure_proved": False,
        "full_nonlinear_su2_partition_ratio_proved": False,
        "next_obstruction": (
            "control the incoherent-collar numerator with the same coherence radius, "
            "including overlap, entropy, retained state, and normalizer"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
