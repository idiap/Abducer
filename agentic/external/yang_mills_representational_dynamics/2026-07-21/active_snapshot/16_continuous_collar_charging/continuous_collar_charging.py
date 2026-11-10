"""Deterministic continuous SU(2) charging of incoherent staple collars.

If P_i=U S_i are the plaquettes incident on a selected link, bi-invariance
gives d(S_i,S_j)=d(P_i,P_j).  Failure of a common eta-ball implies staple
diameter greater than eta.  Hence, for every selected-link value U, some
incident plaquette has curvature greater than eta/2 and the sum of the two
corresponding squared curvatures exceeds eta^2/2.

Combining this exact charge with eta<rho/sqrt(m) exposes a quantitative no-go:
at the frozen ultraviolet witness the largest locally chargeable exponent is
far below the Stage 14 collar-rate target.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any, Iterable

import numpy as np


STAGE08 = Path(__file__).resolve().parents[1] / "08_su2_nonlinear_block_geometry"
if str(STAGE08) not in sys.path:
    sys.path.insert(0, str(STAGE08))

from su2_nonlinear_block_geometry import quaternion_multiply  # noqa: E402


@dataclass(frozen=True)
class CollarChargeCertificate:
    coherence_radius: float
    incident_staples: int
    failure_implies_diameter_above: float
    guaranteed_single_curvature_above: float
    guaranteed_incident_energy_above: float
    link_value_uniform: bool
    gauge_covariant: bool
    probability_bound_certified: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CompatibilityCertificate:
    heat_time: float
    curvature_radius: float
    incident_staples: int
    collar_rate_target: float
    maximum_admissible_coherence_radius: float
    maximum_single_charge_radius: float
    maximum_single_charge_scaled_radius: float
    maximum_single_charge_radial_rate: float
    maximum_total_energy_exponent: float
    energy_charge_meets_target: bool
    radial_charge_meets_target: bool
    maximum_time_for_energy_target: float
    radial_scaled_radius_required: float
    maximum_time_for_radial_target: float
    frozen_witness_compatible: bool
    multi_link_repair_required: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _unit_quaternion(value: Iterable[float]) -> np.ndarray:
    q = np.asarray(tuple(value), dtype=float)
    if q.shape != (4,) or not np.all(np.isfinite(q)):
        raise ValueError("a finite four-component quaternion is required")
    norm = float(np.linalg.norm(q))
    if abs(norm - 1.0) > 1.0e-9:
        raise ValueError("quaternion must have unit norm")
    return q / norm


def su2_distance(q: Iterable[float], r: Iterable[float]) -> float:
    """Bi-invariant S^3 geodesic distance on SU(2), not SO(3)."""

    qv, rv = _unit_quaternion(q), _unit_quaternion(r)
    dot = float(np.dot(qv, rv))
    return math.acos(max(-1.0, min(1.0, dot)))


def relative_distance_errors(
    selected_link: Iterable[float], staples: Iterable[Iterable[float]]
) -> tuple[float, ...]:
    """Numerically check d(S_i,S_j)=d(U S_i,U S_j) for all pairs."""

    u = _unit_quaternion(selected_link)
    family = tuple(_unit_quaternion(s) for s in staples)
    if len(family) < 2:
        raise ValueError("at least two staples are required")
    plaquettes = tuple(quaternion_multiply(u, s) for s in family)
    errors = []
    for i in range(len(family)):
        for j in range(i + 1, len(family)):
            errors.append(
                abs(
                    su2_distance(family[i], family[j])
                    - su2_distance(plaquettes[i], plaquettes[j])
                )
            )
    return tuple(errors)


def collar_charge_certificate(
    coherence_radius: float, incident_staples: int = 6
) -> CollarChargeCertificate:
    eta = _positive("coherence_radius", coherence_radius)
    m = int(incident_staples)
    if eta >= math.pi or m < 2:
        raise ValueError("eta must be below pi and at least two staples are required")
    return CollarChargeCertificate(
        coherence_radius=eta,
        incident_staples=m,
        failure_implies_diameter_above=eta,
        guaranteed_single_curvature_above=eta / 2.0,
        guaranteed_incident_energy_above=eta * eta / 2.0,
        link_value_uniform=True,
        gauge_covariant=True,
        probability_bound_certified=False,
    )


def radial_gaussian_rate(scaled_radius: float, color_dimension: int = 3) -> float:
    s = _positive("scaled_radius", scaled_radius)
    d = int(color_dimension)
    if d < 1:
        raise ValueError("color_dimension must be positive")
    if s <= d:
        return 0.0
    return 0.5 * (s - d - d * math.log(s / d))


def scaled_radius_for_rate(target_rate: float, color_dimension: int = 3) -> float:
    target = _positive("target_rate", target_rate)
    d = int(color_dimension)
    if d < 1:
        raise ValueError("color_dimension must be positive")
    low, high = float(d), max(2.0 * d, 2.0 * target + d)
    while radial_gaussian_rate(high, d) < target:
        high *= 2.0
    for _ in range(100):
        mid = 0.5 * (low + high)
        if radial_gaussian_rate(mid, d) < target:
            low = mid
        else:
            high = mid
    return high


def compatibility_certificate(
    heat_time: float = 3.0e-6,
    curvature_radius: float = 0.0082,
    incident_staples: int = 6,
    collar_rate_target: float = 7.0,
) -> CompatibilityCertificate:
    t = _positive("heat_time", heat_time)
    rho = _positive("curvature_radius", curvature_radius)
    target = _positive("collar_rate_target", collar_rate_target)
    m = int(incident_staples)
    if rho >= math.pi or m < 2:
        raise ValueError("invalid curvature radius or staple count")
    eta_max = rho / math.sqrt(m)
    charge_radius = eta_max / 2.0
    scaled = charge_radius**2 / t
    radial_rate = radial_gaussian_rate(scaled, 3)
    energy_exponent = eta_max**2 / (4.0 * t)
    energy_time = rho**2 / (4.0 * m * target)
    required_s = scaled_radius_for_rate(target, 3)
    radial_time = rho**2 / (4.0 * m * required_s)
    energy_ok = energy_exponent >= target
    radial_ok = radial_rate >= target
    return CompatibilityCertificate(
        heat_time=t,
        curvature_radius=rho,
        incident_staples=m,
        collar_rate_target=target,
        maximum_admissible_coherence_radius=eta_max,
        maximum_single_charge_radius=charge_radius,
        maximum_single_charge_scaled_radius=scaled,
        maximum_single_charge_radial_rate=radial_rate,
        maximum_total_energy_exponent=energy_exponent,
        energy_charge_meets_target=energy_ok,
        radial_charge_meets_target=radial_ok,
        maximum_time_for_energy_target=energy_time,
        radial_scaled_radius_required=required_s,
        maximum_time_for_radial_target=radial_time,
        frozen_witness_compatible=energy_ok and radial_ok,
        multi_link_repair_required=not (energy_ok and radial_ok),
    )


def calibration() -> dict[str, Any]:
    eta = 0.001
    return {
        "exact_charge": collar_charge_certificate(eta).to_dict(),
        "frozen_compatibility": compatibility_certificate().to_dict(),
        "stage14_minimum_rate_compatibility": compatibility_certificate(
            collar_rate_target=6.6653484269034
        ).to_dict(),
        "scope": (
            "exact deterministic continuous SU(2) collar charge and quantitative "
            "local-charging no-go; no probability law, multi-link integration, RG, "
            "continuum theory, or mass gap is certified"
        ),
        "claim_level": "C2 deterministic geometry plus restricted Gaussian calibration",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    args = parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
