"""Uniform small-time curvature control under coherent SU(2) staples.

For m staples S_i lying in a common geodesic eta-ball, translate its center C
and write Q_i=C^{-1}S_i.  The one-link conditional energy is

    E(V)=sum_i d(I,V Q_i)^2,        V=U C.

Since E(I)<=m eta^2, while a target plaquette outside radius rho contributes
at least rho^2, the normalized small-time rate gap is at least
rho^2-m eta^2.  This is positive exactly under the certified sufficient
condition eta<rho/sqrt(m).

The theorem supplies the good-collar half of a two-tier argument.  It does not
bound the probability that the collar is incoherent.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import itertools
import json
import math
from typing import Any, Iterable


@dataclass(frozen=True)
class GoodCollarRateCertificate:
    incident_staples: int
    curvature_radius: float
    coherence_radius: float
    admissible_coherence_threshold: float
    reference_energy_upper: float
    bad_energy_lower: float
    uniform_rate_gap_lower: float
    scaled_log_bad_probability_limsup_upper: float
    rate_concentration_certified: bool
    gauge_covariant_condition: bool
    collar_failure_probability_certified: bool
    full_measure_certified: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CommutingStressCertificate:
    incident_staples: int
    coherence_radius: float
    extreme_assignments_checked: int
    worst_target_deviation: float
    exact_box_bound: float
    general_metric_bound: float
    extremizer: tuple[float, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GoodCollarCalibration:
    heat_time: float
    rate_certificate: GoodCollarRateCertificate
    asymptotic_bad_probability_proxy: float
    negative_log_proxy: float
    center_frustration_coherence_radius: float
    center_frustration_excluded: bool
    commuting_stress: CommutingStressCertificate
    claim_level: str

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        return result


def _finite_positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def good_collar_rate_certificate(
    curvature_radius: float = 0.0082,
    coherence_radius: float = 0.001,
    incident_staples: int = 6,
) -> GoodCollarRateCertificate:
    """Return the exact energy-comparison certificate.

    The heat-kernel normalization is p_t(g)~exp(-d(I,g)^2/(2t)), so
    `2t log P(bad)` has limsup at most minus the reported gap.
    """

    rho = _finite_positive("curvature_radius", curvature_radius)
    eta = _finite_positive("coherence_radius", coherence_radius)
    m = int(incident_staples)
    if m < 2:
        raise ValueError("incident_staples must be at least two")
    if rho >= math.pi or eta >= math.pi:
        raise ValueError("radii must lie below the SU(2) cut radius pi")
    threshold = rho / math.sqrt(m)
    reference = m * eta * eta
    bad_lower = rho * rho
    gap = max(0.0, bad_lower - reference)
    certified = eta < threshold
    return GoodCollarRateCertificate(
        incident_staples=m,
        curvature_radius=rho,
        coherence_radius=eta,
        admissible_coherence_threshold=threshold,
        reference_energy_upper=reference,
        bad_energy_lower=bad_lower,
        uniform_rate_gap_lower=gap,
        scaled_log_bad_probability_limsup_upper=-gap,
        rate_concentration_certified=certified,
        gauge_covariant_condition=True,
        collar_failure_probability_certified=False,
        full_measure_certified=False,
    )


def commuting_minimizer(staple_angles: Iterable[float]) -> tuple[float, tuple[float, ...]]:
    """Exact minimizer in a common one-parameter subgroup without wrapping."""

    angles = tuple(float(x) for x in staple_angles)
    if len(angles) < 2 or any(not math.isfinite(x) for x in angles):
        raise ValueError("at least two finite staple angles are required")
    if max(abs(x) for x in angles) >= math.pi / 2.0:
        raise ValueError("commuting calibration requires the convex chart")
    minimizer = -math.fsum(angles) / len(angles)
    plaquette_angles = tuple(abs(minimizer + x) for x in angles)
    return minimizer, plaquette_angles


def commuting_stress_certificate(
    coherence_radius: float = 0.001,
    incident_staples: int = 6,
) -> CommutingStressCertificate:
    """Enumerate the box vertices and recover the sharp scalar deviation."""

    eta = _finite_positive("coherence_radius", coherence_radius)
    m = int(incident_staples)
    if m < 2:
        raise ValueError("incident_staples must be at least two")
    if eta >= math.pi / 2.0:
        raise ValueError("coherence_radius must stay in the convex chart")
    worst = -1.0
    extremizer: tuple[float, ...] = ()
    for signs in itertools.product((-1.0, 1.0), repeat=m):
        angles = tuple(eta * sign for sign in signs)
        _, deviations = commuting_minimizer(angles)
        candidate = max(deviations)
        if candidate > worst:
            worst = candidate
            extremizer = angles
    exact = 2.0 * (m - 1.0) * eta / m
    return CommutingStressCertificate(
        incident_staples=m,
        coherence_radius=eta,
        extreme_assignments_checked=2**m,
        worst_target_deviation=worst,
        exact_box_bound=exact,
        general_metric_bound=math.sqrt(m) * eta,
        extremizer=extremizer,
    )


def center_frustration_coherence_radius() -> float:
    """Smallest common-ball radius containing I and -I in SU(2)."""

    return math.pi / 2.0


def calibration(
    heat_time: float = 3.0e-6,
    curvature_radius: float = 0.0082,
    coherence_radius: float = 0.001,
    incident_staples: int = 6,
) -> GoodCollarCalibration:
    t = _finite_positive("heat_time", heat_time)
    rate = good_collar_rate_certificate(
        curvature_radius, coherence_radius, incident_staples
    )
    if rate.rate_concentration_certified:
        negative_log = rate.uniform_rate_gap_lower / (2.0 * t)
        proxy = math.exp(-negative_log) if negative_log < 745.0 else 0.0
    else:
        negative_log = 0.0
        proxy = 1.0
    center_radius = center_frustration_coherence_radius()
    return GoodCollarCalibration(
        heat_time=t,
        rate_certificate=rate,
        asymptotic_bad_probability_proxy=proxy,
        negative_log_proxy=negative_log,
        center_frustration_coherence_radius=center_radius,
        center_frustration_excluded=coherence_radius < center_radius,
        commuting_stress=commuting_stress_certificate(
            coherence_radius, incident_staples
        ),
        claim_level="C2 small-time coherent-collar theorem",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.add_argument("--time", type=float, default=3.0e-6)
    parser.add_argument("--rho", type=float, default=0.0082)
    parser.add_argument("--eta", type=float, default=0.001)
    args = parser.parse_args()
    print(json.dumps(calibration(args.time, args.rho, args.eta).to_dict(), indent=2))


if __name__ == "__main__":
    main()

