"""Explicit local initialization data for the SU(2) heat-kernel action.

Convention
----------
SU(2) is identified with the unit three-sphere.  The heat semigroup has
generator (1/2) Delta, so the character expansion is

    p_t(theta) = sum_{n>=0} (n+1) exp[-n(n+2)t/2]
                 sin((n+1)theta)/sin(theta).

The local action is s_t(theta) = -log p_t(theta).  This module certifies the
curvature-coordinate remainder relative to theta^2/(2t).  It does not supply
the nonlinear 2^4 plaquette BCH chart constants or a dependent block-polymer
estimate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
import platform
from typing import Any

import numpy as np


TAU = 2.0 * math.pi


def _finite_positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _finite_nonnegative(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


@dataclass(frozen=True)
class ImageDerivativeBounds:
    q0: float
    q1: float
    q2: float
    q3: float
    included_images: int
    omitted_tail_bounds: tuple[float, float, float, float]
    omitted_tail_log_bounds: tuple[float, float, float, float]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HeatKernelLocalCertificate:
    time_max: float
    curvature_radius: float
    geometric_hessian_bound: float
    geometric_third_bound: float
    image_log_hessian_bound: float
    image_log_third_bound: float
    scaled_gradient_remainder_bound: float
    scaled_hessian_remainder_bound: float
    scaled_third_derivative_bound: float
    image_bounds: ImageDerivativeBounds
    uniform_time_condition: float

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["image_bounds"] = self.image_bounds.to_dict()
        return result


@dataclass(frozen=True)
class ChartNorm:
    """Declared derivative bounds for a curvature chart X(A)."""

    linear_norm: float
    derivative_norm: float
    derivative_deviation: float
    second_derivative_norm: float
    third_derivative_norm: float

    def __post_init__(self) -> None:
        for name, value in asdict(self).items():
            object.__setattr__(self, name, _finite_nonnegative(name, value))


@dataclass(frozen=True)
class ComposedChartBudget:
    per_plaquette_hessian_budget: float
    per_plaquette_third_budget: float
    aggregation_constant: float
    aggregated_hessian_budget: float
    aggregated_third_budget: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProbabilityInterval:
    time: float
    curvature_radius: float
    partial_sum: float
    lower: float
    upper: float
    analytic_truncation_bound: float
    floating_roundoff_allowance: float
    highest_character: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _image_term_bound(j: int, time_max: float, radius: float, k: int) -> float:
    log_value = _image_term_log_bound(j, time_max, radius, k)
    if log_value < math.log(math.ulp(0.0)):
        return 0.0
    return math.exp(log_value)


def _image_term_log_bound(j: int, time_max: float, radius: float, k: int) -> float:
    a = TAU * k
    exponent = -(a * a - 2.0 * a * radius) / (2.0 * time_max)
    return (
        math.log(2.0)
        + exponent
        + j * math.log(a / time_max)
        + math.log1p(a * a / (time_max * (j + 1.0)))
    )


def image_derivative_bounds(
    time_max: float,
    radius: float,
    included_images: int = 1,
) -> ImageDerivativeBounds:
    """Bound sup |q^(j)|, j=0,...,3, in the exact Poisson image formula.

    Pairing images k and -k removes the apparent singularity at theta=0.
    The bound follows from sinh(u)/u = integral_0^1 cosh(su) ds.  The
    omitted k-tail is bounded by a geometric ratio after the last image.
    """

    time_max = _finite_positive("time_max", time_max)
    radius = _finite_positive("radius", radius)
    if radius >= math.pi / 2.0:
        raise ValueError("the local certificate requires radius < pi/2")
    if included_images < 1:
        raise ValueError("included_images must be at least one")

    first_image = TAU
    c1 = (first_image**2 - 2.0 * first_image * radius) / 2.0
    uniform_time_condition = c1 / 4.0
    if time_max > uniform_time_condition:
        raise ValueError("time range is too large for the declared uniform image bound")

    values: list[float] = []
    tails: list[float] = []
    log_tails: list[float] = []
    a_quadratic = TAU**2 / (2.0 * time_max)
    b_linear = TAU * radius / time_max
    first_omitted = included_images + 1
    for j in range(4):
        included = math.fsum(
            _image_term_bound(j, time_max, radius, k)
            for k in range(1, included_images + 1)
        )
        ratio = (
            ((first_omitted + 1.0) / first_omitted) ** (j + 2)
            * math.exp(
                -a_quadratic * (2.0 * first_omitted + 1.0) + b_linear
            )
        )
        if not 0.0 <= ratio < 1.0:
            raise ValueError("image-tail ratio is not contractive")
        log_first = _image_term_log_bound(
            j, time_max, radius, first_omitted
        )
        log_tail = log_first - math.log1p(-ratio)
        if log_tail < math.log(math.ulp(0.0)):
            tail = math.ulp(0.0)
        else:
            tail = math.exp(log_tail)
        values.append(included + tail)
        tails.append(tail)
        log_tails.append(log_tail)
    return ImageDerivativeBounds(
        q0=values[0],
        q1=values[1],
        q2=values[2],
        q3=values[3],
        included_images=included_images,
        omitted_tail_bounds=tuple(tails),
        omitted_tail_log_bounds=tuple(log_tails),
    )


def heat_kernel_local_certificate(
    time_max: float,
    radius: float,
    included_images: int = 1,
) -> HeatKernelLocalCertificate:
    """Return uniform local action budgets for 0 < t <= time_max."""

    bounds = image_derivative_bounds(time_max, radius, included_images)
    if bounds.q0 >= 1.0:
        raise ValueError("image correction is too large to control log(1+q)")
    denominator = 1.0 - bounds.q0
    image_hessian = (
        bounds.q2 / denominator + bounds.q1**2 / denominator**2
    )
    image_third = (
        bounds.q3 / denominator
        + 3.0 * bounds.q1 * bounds.q2 / denominator**2
        + 2.0 * bounds.q1**3 / denominator**3
    )

    sine = math.sin(radius)
    cosine = math.cos(radius)
    geometric_hessian = 1.0 / sine**2 - 1.0 / radius**2
    geometric_third = 2.0 / radius**3 - 2.0 * cosine / sine**3
    scaled_hessian = time_max * (geometric_hessian + image_hessian)
    scaled_gradient = radius * scaled_hessian
    # For a radial C3 remainder, the Euclidean third derivative tensor is
    # bounded by four times the radial third-derivative supremum.
    scaled_third = 4.0 * time_max * (geometric_third + image_third)

    first_image = TAU
    uniform_condition = (
        first_image**2 - 2.0 * first_image * radius
    ) / 8.0
    return HeatKernelLocalCertificate(
        time_max=float(time_max),
        curvature_radius=float(radius),
        geometric_hessian_bound=geometric_hessian,
        geometric_third_bound=geometric_third,
        image_log_hessian_bound=image_hessian,
        image_log_third_bound=image_third,
        scaled_gradient_remainder_bound=scaled_gradient,
        scaled_hessian_remainder_bound=scaled_hessian,
        scaled_third_derivative_bound=scaled_third,
        image_bounds=bounds,
        uniform_time_condition=uniform_condition,
    )


def compose_with_curvature_chart(
    certificate: HeatKernelLocalCertificate,
    chart: ChartNorm,
    aggregation_constant: float = 1.0,
) -> ComposedChartBudget:
    """Propagate the curvature-action budgets through X(A) by the chain rule.

    ``aggregation_constant`` is a declared operator-norm aggregation factor.
    It is not silently set equal to the number of plaquettes.
    """

    aggregation_constant = _finite_positive(
        "aggregation_constant", aggregation_constant
    )
    rho = certificate.curvature_radius
    epsilon = certificate.scaled_hessian_remainder_bound
    gradient = certificate.scaled_gradient_remainder_bound
    tau = certificate.scaled_third_derivative_bound
    m0 = chart.linear_norm
    m1 = chart.derivative_norm
    delta1 = chart.derivative_deviation
    m2 = chart.second_derivative_norm
    m3 = chart.third_derivative_norm

    hessian = (
        delta1 * (m1 + m0)
        + epsilon * m1**2
        + (rho + gradient) * m2
    )
    third = (
        tau * m1**3
        + 3.0 * (1.0 + epsilon) * m1 * m2
        + (rho + gradient) * m3
    )
    return ComposedChartBudget(
        per_plaquette_hessian_budget=hessian,
        per_plaquette_third_budget=third,
        aggregation_constant=aggregation_constant,
        aggregated_hessian_budget=aggregation_constant * hessian,
        aggregated_third_budget=aggregation_constant * third,
    )


def su2_character_kernel(theta: float, time: float, highest_character: int) -> float:
    """Truncated SU(2) character expansion in the declared normalization."""

    time = _finite_positive("time", time)
    theta = _finite_nonnegative("theta", theta)
    if theta >= math.pi:
        raise ValueError("theta must lie in [0, pi)")
    if highest_character < 0:
        raise ValueError("highest_character must be nonnegative")
    near_zero = theta < 1e-10
    denominator = 1.0 if near_zero else math.sin(theta)
    terms = []
    for n in range(highest_character + 1):
        dimension = n + 1.0
        character = dimension if near_zero else math.sin(dimension * theta) / denominator
        terms.append(
            dimension * math.exp(-0.5 * n * (n + 2.0) * time) * character
        )
    return math.fsum(terms)


def su2_image_kernel_shape(theta: float, time: float, image_cutoff: int) -> float:
    """Poisson-image heat-kernel shape, up to a theta-independent factor."""

    time = _finite_positive("time", time)
    theta = _finite_nonnegative("theta", theta)
    if theta >= math.pi:
        raise ValueError("theta must lie in [0, pi)")
    if image_cutoff < 1:
        raise ValueError("image_cutoff must be positive")
    if theta < 1e-10:
        return math.fsum(
            (1.0 - (TAU * k) ** 2 / time)
            * math.exp(-(TAU * k) ** 2 / (2.0 * time))
            for k in range(-image_cutoff, image_cutoff + 1)
        )
    numerator = math.fsum(
        (theta + TAU * k)
        * math.exp(-(theta + TAU * k) ** 2 / (2.0 * time))
        for k in range(-image_cutoff, image_cutoff + 1)
    )
    return numerator / math.sin(theta)


def _tail_integral(m: int, radius: float) -> float:
    if m == 1:
        return 0.5 * (math.pi - radius) + 0.25 * math.sin(2.0 * radius)
    return -0.5 * (
        math.sin((m - 1.0) * radius) / (m - 1.0)
        - math.sin((m + 1.0) * radius) / (m + 1.0)
    )


def character_tail_probability(
    time: float,
    radius: float,
    highest_character: int = 80,
) -> ProbabilityInterval:
    """Enclose P_t(theta >= radius) using an analytic character tail bound."""

    time = _finite_positive("time", time)
    radius = _finite_nonnegative("radius", radius)
    if radius > math.pi:
        raise ValueError("radius must lie in [0, pi]")
    if highest_character < 1:
        raise ValueError("highest_character must be at least one")

    terms = []
    for n in range(highest_character + 1):
        m = n + 1
        terms.append(
            (2.0 / math.pi)
            * m
            * math.exp(-0.5 * n * (n + 2.0) * time)
            * _tail_integral(m, radius)
        )
    partial = math.fsum(terms)
    first_n = highest_character + 1
    first = 2.0 * (first_n + 1.0) * math.exp(
        -0.5 * first_n * (first_n + 2.0) * time
    )
    ratio = (
        (first_n + 2.0) / (first_n + 1.0)
        * math.exp(-0.5 * (2.0 * first_n + 3.0) * time)
    )
    if not 0.0 <= ratio < 1.0:
        raise ValueError("increase highest_character to obtain a geometric tail")
    analytic_tail = first / (1.0 - ratio)
    roundoff = 64.0 * np.finfo(float).eps * math.fsum(abs(x) for x in terms) + 1e-15
    lower = max(0.0, partial - analytic_tail - roundoff)
    upper = min(1.0, partial + analytic_tail + roundoff)
    return ProbabilityInterval(
        time=time,
        curvature_radius=radius,
        partial_sum=partial,
        lower=lower,
        upper=upper,
        analytic_truncation_bound=analytic_tail,
        floating_roundoff_allowance=roundoff,
        highest_character=highest_character,
    )


def calibration() -> dict[str, Any]:
    local_02 = heat_kernel_local_certificate(0.2, 1.0, 1)
    local_01 = heat_kernel_local_certificate(0.1, 1.0, 1)
    identity_chart = compose_with_curvature_chart(
        local_02, ChartNorm(1.0, 1.0, 0.0, 0.0, 0.0)
    )
    illustrative_chart = compose_with_curvature_chart(
        local_02,
        ChartNorm(1.0, 1.1, 0.1, 0.2, 0.3),
        aggregation_constant=6.0,
    )

    character_at_zero = su2_character_kernel(0.0, 0.2, 80)
    image_at_zero = su2_image_kernel_shape(0.0, 0.2, 4)
    representation_checks = []
    for theta in (0.2, 0.6, 1.0):
        character_ratio = su2_character_kernel(theta, 0.2, 80) / character_at_zero
        image_ratio = su2_image_kernel_shape(theta, 0.2, 4) / image_at_zero
        representation_checks.append(
            {
                "theta": theta,
                "character_ratio": character_ratio,
                "image_ratio": image_ratio,
                "absolute_difference": abs(character_ratio - image_ratio),
            }
        )

    probabilities = [
        character_tail_probability(t, 1.0, 80).to_dict()
        for t in (0.2, 0.1, 0.05)
    ]
    return {
        "scope": (
            "exact one-plaquette SU(2) heat-kernel action in logarithmic "
            "curvature coordinates, analytic image-tail bounds, and "
            "character-tail probability enclosure; not a 2^4 BCH block or "
            "dependent polymer theorem"
        ),
        "normalization": {
            "generator": "(1/2) Laplace-Beltrami on the unit S^3",
            "casimir_exponent": "exp(-n(n+2)t/2)",
            "principal_action": "theta^2/(2t)",
            "haar_radial_density": "(2/pi) sin(theta)^2 dtheta",
        },
        "local_certificates": [local_02.to_dict(), local_01.to_dict()],
        "representation_consistency": representation_checks,
        "tail_probabilities": probabilities,
        "chart_composition": {
            "identity_chart": identity_chart.to_dict(),
            "illustrative_only_nonlinear_chart": illustrative_chart.to_dict(),
            "warning": "the illustrative chart values are not certified BCH constants",
        },
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
