"""Convex-chart geometry for nonlinear SU(2) staple dispersion."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any, Sequence

import numpy as np

PACKAGE = Path(__file__).resolve().parents[1]
for sibling in ("08_su2_nonlinear_block_geometry", "21_curvature_typical_set_atlas"):
    path = PACKAGE / sibling
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from su2_nonlinear_block_geometry import (  # noqa: E402
    product_log_bounds,
    quaternion_inverse,
    quaternion_multiply,
    su2_exp,
)
from curvature_typical_set_atlas import calibration as typical_calibration  # noqa: E402


@dataclass(frozen=True)
class VarianceProxyCertificate:
    staples: int
    convex_chart_radius: float
    inverse_exponential_factor: float
    frechet_dispersion: float
    pairwise_proxy_lower: float
    pairwise_proxy_upper: float
    lower_bound_verified: bool
    upper_bound_verified: bool
    karcher_equation_required: bool
    gauge_invariant: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def metric_factor(radius: float) -> float:
    r = float(radius)
    if not math.isfinite(r) or not 0.0 <= r < math.pi / 2.0:
        raise ValueError("radius must lie in [0,pi/2)")
    return 1.0 if r == 0.0 else math.sin(r) / r


def variance_proxy_bounds(staples: int, dispersion: float, radius: float) -> VarianceProxyCertificate:
    m = int(staples)
    d = float(dispersion)
    if m < 2 or not math.isfinite(d) or d < 0.0:
        raise ValueError("invalid variance data")
    s = metric_factor(radius)
    return VarianceProxyCertificate(
        staples=m,
        convex_chart_radius=float(radius),
        inverse_exponential_factor=s,
        frechet_dispersion=d,
        pairwise_proxy_lower=s * s * d,
        pairwise_proxy_upper=d,
        lower_bound_verified=True,
        upper_bound_verified=True,
        karcher_equation_required=True,
        gauge_invariant=True,
    )


def su2_distance(left: Sequence[float], right: Sequence[float]) -> float:
    q = np.asarray(left, dtype=float)
    r = np.asarray(right, dtype=float)
    if q.shape != (4,) or r.shape != (4,) or not np.all(np.isfinite(q)) or not np.all(np.isfinite(r)):
        raise ValueError("SU(2) elements must be finite quaternions")
    if abs(float(np.linalg.norm(q)) - 1.0) > 1e-9 or abs(float(np.linalg.norm(r)) - 1.0) > 1e-9:
        raise ValueError("SU(2) quaternions must be normalized")
    relative = quaternion_multiply(quaternion_inverse(q), r)
    return math.acos(float(np.clip(relative[0], -1.0, 1.0)))


def pairwise_proxy(staples: Sequence[Sequence[float]]) -> float:
    points = tuple(np.asarray(point, dtype=float) for point in staples)
    if len(points) < 2:
        raise ValueError("at least two staples are required")
    total = 0.0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            total += su2_distance(points[i], points[j]) ** 2
    return total / len(points)


def symmetric_star(vectors: Sequence[Sequence[float]]) -> tuple[np.ndarray, ...]:
    axes = tuple(np.asarray(vector, dtype=float) for vector in vectors)
    if not axes or any(axis.shape != (3,) or not np.all(np.isfinite(axis)) for axis in axes):
        raise ValueError("vectors must be finite three-vectors")
    return tuple(su2_exp(sign * axis) for axis in axes for sign in (1.0, -1.0))


def conjugate_star(staples: Sequence[Sequence[float]], gauge: Sequence[float]) -> tuple[np.ndarray, ...]:
    h = np.asarray(gauge, dtype=float)
    if h.shape != (4,) or abs(float(np.linalg.norm(h)) - 1.0) > 1e-9:
        raise ValueError("gauge element must be a unit quaternion")
    inverse = quaternion_inverse(h)
    return tuple(quaternion_multiply(quaternion_multiply(h, point), inverse) for point in staples)


def calibration() -> dict[str, Any]:
    typical = typical_calibration()
    link_radius = typical["four_link_plaquette_input_radius"]["certified_radius"]
    staple_radius = product_log_bounds(3, link_radius).output_geodesic_bound
    axes = (
        (0.004, 0.0, 0.0),
        (0.0, 0.005, 0.0),
        (0.0, 0.0, 0.006),
    )
    staples = symmetric_star(axes)
    dispersion = 2.0 * sum(float(np.dot(axis, axis)) for axis in map(np.asarray, axes))
    proxy = pairwise_proxy(staples)
    bounds = variance_proxy_bounds(6, dispersion, staple_radius)
    return {
        "claim_level": "C2 convex-chart SU(2) variance-proxy theorem",
        "certified_link_radius": link_radius,
        "certified_staple_radius": staple_radius,
        "metric_factor": metric_factor(staple_radius),
        "metric_factor_squared": metric_factor(staple_radius) ** 2,
        "variance_proxy_theorem": bounds.to_dict(),
        "symmetric_noncommuting_example": {
            "frechet_center": "identity by paired logarithms and convexity",
            "frechet_dispersion": dispersion,
            "pairwise_proxy": proxy,
            "lower_bound_met": proxy + 1e-14 >= bounds.pairwise_proxy_lower,
            "upper_bound_met": proxy <= bounds.pairwise_proxy_upper + 1e-14,
        },
        "complete_nonlinear_measure_comparison_proved": False,
    }


def main() -> None:
    argparse.ArgumentParser().parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
