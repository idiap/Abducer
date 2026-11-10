"""Normalized Gaussian-to-nonlinear comparison on a retained chart.

If mu_D is obtained from a reference nu_D by density exp(-R), then
osc_D(R)<=kappa implies mu_D(A)<=exp(kappa) nu_D(A).  Comparing with the
untruncated reference adds the unavoidable coverage loss -log nu(D).

On a convex radius-r ball with R(0)=dR(0)=0 and ||d^2 R||<=H,
osc_D(R)<=H r^2.  The Stage 08 local action oscillation is tiny, while the
only directly certified high-dimensional inner-ball mass is astronomically
small.  The calculation isolates chart coverage, rather than local action
geometry, as the unresolved normalization cost.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any

from scipy.special import gammainc


STAGE08 = Path(__file__).resolve().parents[1] / "08_su2_nonlinear_block_geometry"
if str(STAGE08) not in sys.path:
    sys.path.insert(0, str(STAGE08))

from su2_nonlinear_block_geometry import (  # noqa: E402
    action_initialization_certificate,
    incidence_certificate,
)


@dataclass(frozen=True)
class DensityComparisonCertificate:
    hessian_remainder_bound: float
    retained_radius: float
    reference_log_mass_lower: float
    support_size: int
    oscillation_loss: float
    coverage_loss: float
    total_log_comparison_loss: float
    comparison_loss_per_support: float
    target_loss_per_support: float
    target_met: bool
    same_chart_normalization_compared: bool
    full_measure_certified: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ChartCalibration:
    heat_time: float
    gaussian_dimension: int
    plaquettes: int
    local_chart_inner_radius: float
    inner_ball_log_mass: float
    density_comparison: DensityComparisonCertificate
    radius_needed_for_loss_target: float
    radius_enlargement_factor_for_loss_target: float
    radius_for_reference_log_mass_minus_point_one: float
    radius_enlargement_factor_for_high_mass: float
    radius_requirements_are_diagnostic_only: bool
    stage08_chart_enlargement_certified: bool
    claim_level: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def log_chi_square_cdf(degrees_of_freedom: int, threshold: float) -> float:
    """Stable log P[chi^2_n <= threshold], including deep lower tails."""

    n = int(degrees_of_freedom)
    x2 = _positive("threshold", threshold) / 2.0
    if n < 1:
        raise ValueError("degrees_of_freedom must be positive")
    a = n / 2.0
    if x2 < a + 1.0:
        term = 1.0 / a
        total = term
        ap = a
        for _ in range(100000):
            ap += 1.0
            term *= x2 / ap
            total += term
            if abs(term) <= abs(total) * 1.0e-16:
                break
        else:
            raise ArithmeticError("incomplete-gamma series did not converge")
        return -x2 + a * math.log(x2) - math.lgamma(a) + math.log(total)
    probability = float(gammainc(a, x2))
    if not 0.0 < probability <= 1.0:
        raise ArithmeticError("incomplete-gamma evaluation lost probability range")
    return math.log(probability)


def gaussian_ball_log_mass(
    dimension: int, heat_time: float, radius: float
) -> float:
    t = _positive("heat_time", heat_time)
    r = _positive("radius", radius)
    return log_chi_square_cdf(int(dimension), r * r / t)


def density_comparison_certificate(
    hessian_remainder_bound: float,
    retained_radius: float,
    reference_log_mass_lower: float,
    support_size: int,
    target_loss_per_support: float = 0.2,
) -> DensityComparisonCertificate:
    hessian = _positive("hessian_remainder_bound", hessian_remainder_bound)
    radius = _positive("retained_radius", retained_radius)
    log_mass = float(reference_log_mass_lower)
    target = _positive("target_loss_per_support", target_loss_per_support)
    support = int(support_size)
    if not math.isfinite(log_mass) or log_mass > 0.0:
        raise ValueError("reference_log_mass_lower must be finite and nonpositive")
    if support < 1:
        raise ValueError("support_size must be positive")
    oscillation = hessian * radius * radius
    coverage = -log_mass
    total = oscillation + coverage
    per_support = total / support
    return DensityComparisonCertificate(
        hessian_remainder_bound=hessian,
        retained_radius=radius,
        reference_log_mass_lower=log_mass,
        support_size=support,
        oscillation_loss=oscillation,
        coverage_loss=coverage,
        total_log_comparison_loss=total,
        comparison_loss_per_support=per_support,
        target_loss_per_support=target,
        target_met=per_support <= target,
        same_chart_normalization_compared=True,
        full_measure_certified=False,
    )


def radius_for_log_mass(
    dimension: int, heat_time: float, target_log_mass: float
) -> float:
    n = int(dimension)
    t = _positive("heat_time", heat_time)
    target = float(target_log_mass)
    if n < 1 or not math.isfinite(target) or target >= 0.0:
        raise ValueError("dimension must be positive and target log mass negative")
    low, high = 0.0, math.sqrt(t * (n + 20.0 * math.sqrt(2.0 * n)))
    while gaussian_ball_log_mass(n, t, high) < target:
        high *= 2.0
    for _ in range(100):
        mid = 0.5 * (low + high)
        if gaussian_ball_log_mass(n, t, mid) < target:
            low = mid
        else:
            high = mid
    return high


def radius_for_loss_target(
    dimension: int,
    heat_time: float,
    hessian_remainder_bound: float,
    support_size: int,
    target_loss_per_support: float,
) -> float:
    h = _positive("hessian_remainder_bound", hessian_remainder_bound)
    target = _positive("target_loss_per_support", target_loss_per_support)
    support = int(support_size)
    if support < 1:
        raise ValueError("support_size must be positive")

    def loss(radius: float) -> float:
        return (
            h * radius * radius
            - gaussian_ball_log_mass(dimension, heat_time, radius)
        ) / support

    low = math.sqrt(float.fromhex("0x1.0p-1022"))
    high = math.sqrt(heat_time * dimension)
    while loss(high) > target:
        high *= 1.2
        if h * high * high / support > target and high > 10.0:
            raise ValueError("no certified radius meets the requested loss")
    for _ in range(100):
        mid = 0.5 * (low + high)
        if loss(mid) > target:
            low = mid
        else:
            high = mid
    return high


def calibration() -> ChartCalibration:
    t = 3.0e-6
    local_radius = 0.003
    incidence = incidence_certificate()
    dimension = 3 * incidence.physical_dimension_scalar
    plaquettes = incidence.plaquettes
    action = action_initialization_certificate(
        time_max=t, local_link_radius=local_radius, fiber_radius=0.001
    )
    log_mass = gaussian_ball_log_mass(dimension, t, local_radius)
    comparison = density_comparison_certificate(
        action.global_hessian_remainder,
        local_radius,
        log_mass,
        plaquettes,
        target_loss_per_support=0.2,
    )
    needed = radius_for_loss_target(
        dimension,
        t,
        action.global_hessian_remainder,
        plaquettes,
        0.2,
    )
    high_mass = radius_for_log_mass(dimension, t, -0.1)
    return ChartCalibration(
        heat_time=t,
        gaussian_dimension=dimension,
        plaquettes=plaquettes,
        local_chart_inner_radius=local_radius,
        inner_ball_log_mass=log_mass,
        density_comparison=comparison,
        radius_needed_for_loss_target=needed,
        radius_enlargement_factor_for_loss_target=needed / local_radius,
        radius_for_reference_log_mass_minus_point_one=high_mass,
        radius_enlargement_factor_for_high_mass=high_mass / local_radius,
        radius_requirements_are_diagnostic_only=True,
        stage08_chart_enlargement_certified=False,
        claim_level="C2 normalized density theorem plus restricted chart calibration",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    args = parser.parse_args()
    print(json.dumps(calibration().to_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
