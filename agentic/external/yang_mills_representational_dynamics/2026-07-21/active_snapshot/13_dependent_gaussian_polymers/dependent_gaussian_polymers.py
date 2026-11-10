"""Dependent bad-plaquette bounds in the linearized 4D gauge model.

After quotienting gauge directions on the contractible side-two block, the
linearized curvature F=d1 A is distributed as an isotropic Gaussian on
im(d1) tensor R^3.  In ambient plaquette coordinates its covariance is t P,
where P is an orthogonal projection.  Hence every coordinate restriction has
covariance at most t I even though plaquettes are dependent through shared
links and Bianchi constraints.

For a set S of k plaquettes, the event ||F_p||>=rho for every p in S implies
||F_S||^2>=k rho^2.  A quadratic exponential moment gives

  P(all p in S bad) <= exp(-k J_3(rho^2/t)),
  J_3(s)=1/2 (s-3-3 log(s/3)),   s>3.

Together with a maximum-degree connected-set count this yields a rooted
polymer sum without any independence hypothesis.  The theorem is exact for
the Gaussian model, not the nonlinear SU(2) measure.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np


PACKAGE = Path(__file__).resolve().parents[1]
for sibling in (
    PACKAGE / "08_su2_nonlinear_block_geometry",
    PACKAGE / "12_center_contour_charging",
):
    if str(sibling) not in sys.path:
        sys.path.insert(0, str(sibling))

from su2_nonlinear_block_geometry import build_block_complex  # noqa: E402
from center_contour_charging import center_complex_certificate  # noqa: E402


@dataclass(frozen=True)
class ProjectionCertificate:
    scalar_curvature_rank: int
    color_curvature_dimension: int
    ambient_color_dimension: int
    symmetry_error: float
    idempotence_error: float
    minimum_eigenvalue: float
    maximum_eigenvalue: float
    minimum_diagonal: float
    maximum_diagonal: float
    covariance_contraction_certified: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GaussianJointTailCertificate:
    heat_time: float
    curvature_radius: float
    normalized_radius_squared: float
    color_dimension_per_plaquette: int
    plaquettes_in_event: int
    joint_rate_per_plaquette: float
    joint_probability_upper: float
    dependence_retained: bool
    independence_assumed: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GaussianPolymerCertificate:
    heat_time: float
    curvature_radius: float
    alpha: float
    adjacency_degree: int
    rate_per_plaquette: float
    effective_bad_weight: float
    branching_ratio: float
    rooted_weighted_connected_sum_upper: float
    maximum_certified_heat_time: float
    witness_heat_time_slack: float
    dependent_gaussian_polymer_certified: bool
    mayer_activity_expansion_certified: bool
    nonlinear_su2_polymer_certified: bool
    repeated_rg_certified: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _finite_positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


@lru_cache(maxsize=1)
def curvature_projection() -> np.ndarray:
    block = build_block_complex()
    d1 = np.asarray(block.d1, dtype=float)
    projection = d1 @ np.linalg.pinv(d1, rcond=1.0e-12)
    return 0.5 * (projection + projection.T)


def projection_certificate() -> ProjectionCertificate:
    projection = curvature_projection()
    eigenvalues = np.linalg.eigvalsh(projection)
    rank = int(np.count_nonzero(eigenvalues > 0.5))
    symmetry = float(np.linalg.norm(projection - projection.T, ord=2))
    idempotence = float(np.linalg.norm(projection @ projection - projection, ord=2))
    return ProjectionCertificate(
        scalar_curvature_rank=rank,
        color_curvature_dimension=3 * rank,
        ambient_color_dimension=3 * projection.shape[0],
        symmetry_error=symmetry,
        idempotence_error=idempotence,
        minimum_eigenvalue=float(eigenvalues[0]),
        maximum_eigenvalue=float(eigenvalues[-1]),
        minimum_diagonal=float(np.min(np.diag(projection))),
        maximum_diagonal=float(np.max(np.diag(projection))),
        covariance_contraction_certified=bool(
            symmetry < 1.0e-10
            and idempotence < 1.0e-10
            and eigenvalues[0] > -1.0e-10
            and eigenvalues[-1] < 1.0 + 1.0e-10
        ),
    )


def radial_gaussian_rate(normalized_radius_squared: float, color_dimension: int = 3) -> float:
    s = float(normalized_radius_squared)
    d = int(color_dimension)
    if not math.isfinite(s) or s <= 0.0:
        raise ValueError("normalized_radius_squared must be finite and positive")
    if d < 1:
        raise ValueError("color_dimension must be positive")
    if s <= d:
        return 0.0
    return 0.5 * (s - d - d * math.log(s / d))


def joint_tail_certificate(
    plaquettes_in_event: int = 1,
    heat_time: float = 3.0e-6,
    curvature_radius: float = 0.0082,
) -> GaussianJointTailCertificate:
    k = int(plaquettes_in_event)
    if k < 1:
        raise ValueError("plaquettes_in_event must be positive")
    t = _finite_positive("heat_time", heat_time)
    rho = _finite_positive("curvature_radius", curvature_radius)
    s = rho * rho / t
    rate = radial_gaussian_rate(s, 3)
    exponent = k * rate
    upper = math.exp(-exponent) if exponent < 745.0 else 0.0
    return GaussianJointTailCertificate(
        heat_time=t,
        curvature_radius=rho,
        normalized_radius_squared=s,
        color_dimension_per_plaquette=3,
        plaquettes_in_event=k,
        joint_rate_per_plaquette=rate,
        joint_probability_upper=upper,
        dependence_retained=True,
        independence_assumed=False,
    )


def maximum_heat_time(
    curvature_radius: float,
    alpha: float,
    adjacency_degree: int,
) -> float:
    rho = _finite_positive("curvature_radius", curvature_radius)
    alpha = float(alpha)
    degree = int(adjacency_degree)
    if not math.isfinite(alpha) or alpha < 0.0:
        raise ValueError("alpha must be finite and nonnegative")
    if degree < 1:
        raise ValueError("adjacency_degree must be positive")
    target = alpha + 2.0 * math.log(degree)
    low_s = 3.0
    high_s = 4.0
    while radial_gaussian_rate(high_s, 3) <= target:
        high_s *= 2.0
    for _ in range(100):
        middle = 0.5 * (low_s + high_s)
        if radial_gaussian_rate(middle, 3) > target:
            high_s = middle
        else:
            low_s = middle
    return rho * rho / high_s


def polymer_certificate(
    heat_time: float = 3.0e-6,
    curvature_radius: float = 0.0082,
    alpha: float = 0.1,
) -> GaussianPolymerCertificate:
    t = _finite_positive("heat_time", heat_time)
    rho = _finite_positive("curvature_radius", curvature_radius)
    alpha = float(alpha)
    if not math.isfinite(alpha) or alpha < 0.0:
        raise ValueError("alpha must be finite and nonnegative")
    degree = center_complex_certificate().link_adjacency_max_degree
    rate = radial_gaussian_rate(rho * rho / t, 3)
    q = math.exp(-rate)
    ratio = math.exp(alpha) * degree * degree * q
    rooted = math.exp(alpha) * q / (1.0 - ratio) if ratio < 1.0 else math.inf
    t_max = maximum_heat_time(rho, alpha, degree)
    return GaussianPolymerCertificate(
        heat_time=t,
        curvature_radius=rho,
        alpha=alpha,
        adjacency_degree=degree,
        rate_per_plaquette=rate,
        effective_bad_weight=q,
        branching_ratio=ratio,
        rooted_weighted_connected_sum_upper=rooted,
        maximum_certified_heat_time=t_max,
        witness_heat_time_slack=t_max - t,
        dependent_gaussian_polymer_certified=ratio < 1.0 and rooted < 1.0,
        mayer_activity_expansion_certified=False,
        nonlinear_su2_polymer_certified=False,
        repeated_rg_certified=False,
    )


def calibration() -> dict[str, Any]:
    return {
        "projection": projection_certificate().to_dict(),
        "one_plaquette": joint_tail_certificate().to_dict(),
        "six_plaquettes": joint_tail_certificate(6).to_dict(),
        "dependent_polymer": polymer_certificate().to_dict(),
        "claim_level": "C2 exact dependent linearized Gaussian theorem",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2))


if __name__ == "__main__":
    main()
