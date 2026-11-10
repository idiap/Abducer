"""Exact normalized Haar geometry for local SU(2) partition comparisons.

With the bi-invariant geodesic metric and normalized Haar measure,
SU(2)=S^3 and

    v(r) = (r - sin(r) cos(r))/pi
         = (2/pi) integral_0^r sin(u)^2 du.

For 0 <= r <= 1, elementary sine bounds give

    2 r^3/(3 pi) (1-r^2/5) <= v(r) <= 2 r^3/(3 pi).

The module turns these identities into stable executable entropy certificates.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path
from typing import Any


PACKAGE = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class HaarEntropyCertificate:
    radius: float
    exact_ball_volume: float
    cubic_lower_volume: float
    cubic_upper_volume: float
    exact_negative_log_volume: float
    entropy_lower: float
    entropy_upper: float
    exact_inside_bounds: bool
    relative_bracket_width: float

    def to_dict(self) -> dict[str, float | bool]:
        return asdict(self)


@dataclass(frozen=True)
class TwoCenterAtlasCertificate:
    chart_radius: float
    ball_mass: float
    union_covers_su2: bool
    overlap_has_haar_measure_zero: bool
    almost_everywhere_multiplicity: int
    boundary_multiplicity: int

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


def _radius(radius: float, *, allow_pi: bool = True) -> float:
    r = float(radius)
    upper_ok = r <= math.pi if allow_pi else r < math.pi
    if not math.isfinite(r) or r < 0.0 or not upper_ok:
        raise ValueError("radius must lie in [0,pi]" if allow_pi else "radius must lie in [0,pi)")
    return r


def normalized_haar_ball_volume(radius: float) -> float:
    """Normalized Haar mass of a closed geodesic ball about any center."""

    r = _radius(radius)
    if r == 0.0:
        return 0.0
    if r == math.pi:
        return 1.0
    if r < 1.0e-3:
        r2 = r * r
        # Alternating expansion through r^11; the omitted term is negligible
        # at the branch point and avoids cancellation in r-sin(r)cos(r).
        return (
            r**3
            * (
                2.0 / 3.0
                - 2.0 * r2 / 15.0
                + 4.0 * r2**2 / 315.0
                - 2.0 * r2**3 / 2835.0
                + 4.0 * r2**4 / 155925.0
            )
            / math.pi
        )
    return (r - math.sin(r) * math.cos(r)) / math.pi


def normalized_haar_sphere_density(radius: float) -> float:
    """Derivative v'(r)=2 sin(r)^2/pi."""

    r = _radius(radius)
    return 2.0 * math.sin(r) ** 2 / math.pi


def normalized_haar_shell_volume(inner: float, outer: float) -> float:
    a, b = _radius(inner), _radius(outer)
    if a > b:
        raise ValueError("shell radii must satisfy inner <= outer")
    return normalized_haar_ball_volume(b) - normalized_haar_ball_volume(a)


def cubic_volume_bounds(radius: float) -> tuple[float, float]:
    """Elementary certified bounds valid on 0 <= r <= 1."""

    r = _radius(radius)
    if r > 1.0:
        raise ValueError("cubic bounds are certified only for radius <= 1")
    leading = 2.0 * r**3 / (3.0 * math.pi)
    return leading * (1.0 - r * r / 5.0), leading


def entropy_certificate(radius: float) -> HaarEntropyCertificate:
    r = _radius(radius, allow_pi=False)
    if r <= 0.0 or r > 1.0:
        raise ValueError("entropy certificate requires 0 < radius <= 1")
    exact = normalized_haar_ball_volume(r)
    lower_v, upper_v = cubic_volume_bounds(r)
    exact_h = -math.log(exact)
    lower_h = -math.log(upper_v)
    upper_h = -math.log(lower_v)
    return HaarEntropyCertificate(
        radius=r,
        exact_ball_volume=exact,
        cubic_lower_volume=lower_v,
        cubic_upper_volume=upper_v,
        exact_negative_log_volume=exact_h,
        entropy_lower=lower_h,
        entropy_upper=upper_h,
        exact_inside_bounds=lower_v <= exact <= upper_v,
        relative_bracket_width=(upper_v - lower_v) / exact,
    )


def two_center_atlas_certificate() -> TwoCenterAtlasCertificate:
    radius = math.pi / 2.0
    return TwoCenterAtlasCertificate(
        chart_radius=radius,
        ball_mass=normalized_haar_ball_volume(radius),
        union_covers_su2=True,
        overlap_has_haar_measure_zero=True,
        almost_everywhere_multiplicity=1,
        boundary_multiplicity=2,
    )


def calibration() -> dict[str, Any]:
    registry = json.loads((PACKAGE / "partition_ratio_frontier_parameter_registry.json").read_text())
    selected = registry["stage25_kr_budget"]["selected_radius"]
    maximum = registry["stage25_kr_budget"]["maximum_nonlinear_radius"]
    radii = {
        "stage21_four_link_radius": registry["stage23_local_comparison"]["required_radius"],
        "stage25_selected_local_radius": selected,
        "stage25_selected_curvature_chain_radius": 2.0 * selected,
        "stage22_maximum_local_radius": maximum,
        "stage22_maximum_curvature_chain_radius": 2.0 * maximum,
        "stage15_frozen_curvature_radius": 0.0082,
        "stage21_curvature_radius": 0.009288521129471943,
    }
    return {
        "claim_level": "C2 exact SU(2) Haar geometry and certified entropy brackets",
        "formula": "v(r)=(r-sin(r)cos(r))/pi=(2/pi) integral_0^r sin(u)^2 du",
        "small_ball_bounds": "2r^3(1-r^2/5)/(3pi) <= v(r) <= 2r^3/(3pi), 0<=r<=1",
        "active_radii": {name: entropy_certificate(value).to_dict() for name, value in radii.items()},
        "two_center_atlas": two_center_atlas_certificate().to_dict(),
        "interpretation": (
            "the cubic Haar cost is an exact finite-dimensional entropy term; "
            "it must be paid by action/free-energy gain in any denominator-ball comparison"
        ),
        "physical_partition_ratio_proved": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
