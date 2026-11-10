"""Sharper plaquette-log majorant and nonlinear/typical-set overlap audit."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np


PACKAGE = Path(__file__).resolve().parents[1]
for sibling in (
    "07_su2_heat_kernel_initializer",
    "08_su2_nonlinear_block_geometry",
    "21_curvature_typical_set_atlas",
):
    path = PACKAGE / sibling
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from su2_heat_kernel_initializer import heat_kernel_local_certificate  # noqa: E402
from su2_nonlinear_block_geometry import (  # noqa: E402
    action_initialization_certificate,
    plaquette_log,
    product_log_bounds,
)
from curvature_typical_set_atlas import (  # noqa: E402
    leverage_certificate,
    local_block_union_radius,
    local_block_union_upper,
)


SQRT2 = math.sqrt(2.0)
SQRT6 = math.sqrt(6.0)
SQRT12 = math.sqrt(12.0)
EXACT_ORIGIN_SECOND_DERIVATIVE = 1.0 + SQRT2


@dataclass(frozen=True)
class SharpOverlapCertificate:
    heat_time: float
    local_radius: float
    curvature_radius: float
    exact_origin_second_derivative: float
    crude_third_derivative_bound: float
    refined_second_derivative_bound: float
    refined_first_derivative_bound: float
    local_derivative_deviation: float
    global_derivative_deviation: float
    nonlinear_physical_singular_floor: float
    heat_scaled_hessian_remainder: float
    metric_distortion_budget: float
    radial_action_budget: float
    curvature_chain_budget: float
    total_hessian_remainder: float
    fiber_margin: float
    generated_base_margin: float
    centered_transport_coefficient: float
    fiber_contraction_certified: bool
    generated_base_coercive: bool
    quotient_injective: bool

    def to_dict(self) -> dict[str, float | bool]:
        return asdict(self)


def origin_coefficient_matrix() -> np.ndarray:
    # The signs from exp(A1)exp(A2)exp(-A3)exp(-A4) conjugate this
    # skew matrix by a diagonal sign matrix and do not change its norm.
    matrix = np.zeros((4, 4))
    for i in range(4):
        for j in range(i + 1, 4):
            # Quaternion exponential coordinates obey [A,B]=2 A cross B;
            # the one-half in BCH therefore cancels.
            matrix[i, j] = 1.0
            matrix[j, i] = -1.0
    return matrix


def exact_origin_second_derivative_norm() -> float:
    singular = np.linalg.svd(origin_coefficient_matrix(), compute_uv=False)
    return float(singular[0])


def origin_hessian_action(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    left = np.asarray(left, dtype=float)
    right = np.asarray(right, dtype=float)
    if left.shape != (4, 3) or right.shape != (4, 3):
        raise ValueError("Hessian inputs must both have shape (4,3)")
    signs = np.array([1.0, 1.0, -1.0, -1.0])
    coefficients = signs[:, None] * origin_coefficient_matrix() * signs[None, :]
    result = np.zeros(3)
    for i in range(4):
        for j in range(4):
            result += coefficients[i, j] * np.cross(left[i], right[j])
    return result


def numerical_origin_mixed_hessian(left: np.ndarray, right: np.ndarray, step: float = 1e-5) -> np.ndarray:
    h = float(step)
    if not math.isfinite(h) or h <= 0.0:
        raise ValueError("step must be finite and positive")
    return (
        plaquette_log(h * (left + right))
        - plaquette_log(h * (left - right))
        - plaquette_log(h * (-left + right))
        + plaquette_log(-h * (left + right))
    ) / (4.0 * h * h)


def sharp_overlap_certificate(
    local_radius: float,
    heat_time: float = 3.0e-6,
    fiber_radius: float = 0.001,
) -> SharpOverlapCertificate:
    r = float(local_radius)
    t = float(heat_time)
    f = float(fiber_radius)
    if not math.isfinite(r) or r <= 0.0:
        raise ValueError("local_radius must be finite and positive")
    if not math.isfinite(t) or t <= 0.0:
        raise ValueError("heat_time must be finite and positive")
    if not math.isfinite(f) or f < 0.0:
        raise ValueError("fiber_radius must be finite and nonnegative")

    crude = product_log_bounds(4, r)
    m3 = crude.map_third_bound
    # Mean value from the exact identity Hessian, using the already certified
    # uniform third derivative on the joint four-link ball.
    m2 = EXACT_ORIGIN_SECOND_DERIVATIVE + m3 * r
    m1 = 2.0 + m2 * r
    local_deviation = m2 * r
    global_deviation = SQRT6 * local_deviation
    singular_floor = SQRT2 - global_deviation

    curvature_radius = 2.0 * r
    heat = heat_kernel_local_certificate(t, curvature_radius)
    epsilon = heat.scaled_hessian_remainder_bound
    gradient = heat.scaled_gradient_remainder_bound
    tau_heat = heat.scaled_third_derivative_bound

    metric = global_deviation * (2.0 * SQRT12 + global_deviation)
    radial = epsilon * (SQRT12 + global_deviation) ** 2
    curvature_chain = 6.0 * (curvature_radius + gradient) * m2
    eta = metric + radial + curvature_chain

    per_plaquette_third = (
        tau_heat * m1**3
        + 3.0 * (1.0 + epsilon) * m1 * m2
        + (curvature_radius + gradient) * m3
    )
    tau = 6.0 * per_plaquette_third
    eps_fiber = eta
    eps_cross = eta / SQRT2
    eps_base = eta / 2.0
    fiber_margin = 2.0 - eps_fiber
    if fiber_margin <= 0.0:
        response = math.inf
        transport = math.inf
        base_margin = -math.inf
    else:
        response = eps_cross / fiber_margin
        transport = f * (tau / SQRT2 + tau * response) / fiber_margin
        base_margin = 1.0 - (eps_base + eps_cross**2 / fiber_margin)

    return SharpOverlapCertificate(
        heat_time=t,
        local_radius=r,
        curvature_radius=curvature_radius,
        exact_origin_second_derivative=EXACT_ORIGIN_SECOND_DERIVATIVE,
        crude_third_derivative_bound=m3,
        refined_second_derivative_bound=m2,
        refined_first_derivative_bound=m1,
        local_derivative_deviation=local_deviation,
        global_derivative_deviation=global_deviation,
        nonlinear_physical_singular_floor=singular_floor,
        heat_scaled_hessian_remainder=epsilon,
        metric_distortion_budget=metric,
        radial_action_budget=radial,
        curvature_chain_budget=curvature_chain,
        total_hessian_remainder=eta,
        fiber_margin=fiber_margin,
        generated_base_margin=base_margin,
        centered_transport_coefficient=transport,
        fiber_contraction_certified=transport < 1.0,
        generated_base_coercive=base_margin > 0.0,
        quotient_injective=singular_floor > 0.0,
    )


def complete_local_certificate(certificate: SharpOverlapCertificate) -> bool:
    return bool(
        certificate.fiber_contraction_certified
        and certificate.generated_base_coercive
        and certificate.quotient_injective
    )


def maximal_certified_radius(
    heat_time: float = 3.0e-6,
    fiber_radius: float = 0.001,
    upper: float = 0.05,
) -> float:
    low = 1e-12
    high = float(upper)
    if complete_local_certificate(sharp_overlap_certificate(high, heat_time, fiber_radius)):
        raise ValueError("upper search radius is still certified")
    for _ in range(100):
        middle = 0.5 * (low + high)
        if complete_local_certificate(sharp_overlap_certificate(middle, heat_time, fiber_radius)):
            low = middle
        else:
            high = middle
    return low


def maximal_old_certificate_radius(
    heat_time: float = 3.0e-6,
    fiber_radius: float = 0.001,
    upper: float = 0.009,
) -> float:
    low = 1e-12
    high = float(upper)
    for _ in range(100):
        middle = 0.5 * (low + high)
        try:
            cert = action_initialization_certificate(heat_time, middle, fiber_radius)
            valid = cert.fiber_contraction_certified and cert.generated_base_coercive
        except ValueError:
            valid = False
        if valid:
            low = middle
        else:
            high = middle
    return low


def calibration() -> dict[str, object]:
    t = 3.0e-6
    qcrit = 0.0027927080803578997
    leverage = leverage_certificate()
    required = local_block_union_radius(
        216, 12, t * leverage.max_four_link_variance_coefficient, qcrit
    )
    sharp = sharp_overlap_certificate(required, t, 0.001)
    old = action_initialization_certificate(t, required, 0.001)
    sharp_max = maximal_certified_radius(t, 0.001)
    old_max = maximal_old_certificate_radius(t, 0.001)
    return {
        "claim_level": "C2 sharpened finite-block nonlinear overlap theorem",
        "heat_time": t,
        "critical_probability": qcrit,
        "typical_four_link_radius_required": required,
        "exact_origin_second_derivative_formula": "1+sqrt(2)",
        "exact_origin_second_derivative_numeric": exact_origin_second_derivative_norm(),
        "old_certificate": {
            "maximum_certified_radius": old_max,
            "total_hessian_remainder_at_required_radius": old.global_hessian_remainder,
            "generated_base_margin_at_required_radius": old.generated_base_margin,
            "centered_transport_at_required_radius": old.centered_transport_coefficient,
            "closes_at_required_radius": bool(
                old.fiber_contraction_certified and old.generated_base_coercive
            ),
        },
        "sharp_certificate_at_required_radius": sharp.to_dict(),
        "sharp_maximum_certified_radius": sharp_max,
        "overlap_margin_in_radius": sharp_max - required,
        "overlap_factor": sharp_max / required,
        "complement_union_upper_at_sharp_maximum": local_block_union_upper(
            sharp_max,
            216,
            12,
            t * leverage.max_four_link_variance_coefficient,
        ),
        "nonempty_local_overlap_window_proved": complete_local_certificate(sharp),
        "full_nonlinear_normalized_density_comparison_proved": False,
        "weighted_multilink_defect_charge_proved": False,
        "rg_iteration_or_mass_gap_proved": False,
        "next_target": "construct normalized good-channel comparison and state-weighted multi-link defect charge on the certified overlap window",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
