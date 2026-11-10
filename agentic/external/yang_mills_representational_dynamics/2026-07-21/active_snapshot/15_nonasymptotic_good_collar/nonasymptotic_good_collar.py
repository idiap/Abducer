"""Finite-time coherent-staple conditional bounds on SU(2).

For coherent staples Q_i with d(I,Q_i)<=eta and a denominator ball
d(I,V)<=delta, radial monotonicity and the local Poisson-image envelope give

 P[d(I,VQ_j)>=rho]
 <= v(delta)^(-1) (rho/sin rho) c_t^(m+1)
    exp(-(rho^2-m(eta+delta)^2)/(2t)),

where v(delta) is normalized SU(2) Haar ball volume and
c_t=(1+q_t)/(1-q_t).  Unlike Stage 11, every finite-time prefactor is kept.
The theorem still assumes that the staple collar is coherent.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any


STAGE07 = Path(__file__).resolve().parents[1] / "07_su2_heat_kernel_initializer"
if str(STAGE07) not in sys.path:
    sys.path.insert(0, str(STAGE07))

from su2_heat_kernel_initializer import image_derivative_bounds  # noqa: E402


@dataclass(frozen=True)
class FiniteCollarCertificate:
    heat_time: float
    curvature_radius: float
    coherence_radius: float
    denominator_ball_radius: float
    incident_staples: int
    denominator_plaquette_radius: float
    normalized_haar_ball_volume: float
    image_remainder_bound: float
    heat_kernel_ratio_factor: float
    finite_time_energy_gap: float
    log_bad_probability_upper_raw: float
    bad_probability_upper: float
    finite_time_bound_nontrivial: bool
    coherent_collar_required: bool
    collar_probability_certified: bool
    full_su2_block_measure_certified: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DeltaSearchCertificate:
    heat_time: float
    admissible_delta_upper: float
    selected_delta: float
    selected_log_bound: float
    iterations: int
    global_optimality_claimed: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FiniteCollarCalibration:
    frozen_witness: FiniteCollarCertificate
    frozen_delta_search: DeltaSearchCertificate
    target_bad_weight: float
    maximum_certified_heat_time_for_target: float
    threshold_delta: float
    threshold_certificate: FiniteCollarCertificate
    radial_monotonicity_used: bool
    claim_level: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def normalized_haar_ball_volume(radius: float) -> float:
    """Normalized Haar volume of a geodesic ball in SU(2)=S^3."""

    radius = _positive("radius", radius)
    if radius >= math.pi:
        raise ValueError("radius must be below pi")
    if radius < 1.0e-3:
        r2 = radius * radius
        return (
            radius**3
            * (2.0 / 3.0 - 2.0 * r2 / 15.0 + 4.0 * r2 * r2 / 315.0)
            / math.pi
        )
    return (radius - 0.5 * math.sin(2.0 * radius)) / math.pi


def finite_collar_certificate(
    heat_time: float,
    curvature_radius: float,
    coherence_radius: float,
    denominator_ball_radius: float,
    incident_staples: int = 6,
) -> FiniteCollarCertificate:
    t = _positive("heat_time", heat_time)
    rho = _positive("curvature_radius", curvature_radius)
    eta = _positive("coherence_radius", coherence_radius)
    delta = _positive("denominator_ball_radius", denominator_ball_radius)
    m = int(incident_staples)
    if m < 2:
        raise ValueError("incident_staples must be at least two")
    local_radius = max(rho, eta + delta)
    if local_radius >= math.pi / 2.0:
        raise ValueError("the Poisson-image certificate requires radius < pi/2")
    gap = rho * rho - m * (eta + delta) ** 2
    if gap <= 0.0:
        raise ValueError("denominator radius exhausts the finite-time energy gap")
    q = image_derivative_bounds(t, local_radius, included_images=1).q0
    if not 0.0 <= q < 1.0:
        raise ArithmeticError("image correction did not yield a ratio envelope")
    ratio = (1.0 + q) / (1.0 - q)
    volume = normalized_haar_ball_volume(delta)
    log_upper = (
        -math.log(volume)
        + math.log(rho / math.sin(rho))
        + (m + 1.0) * math.log(ratio)
        - gap / (2.0 * t)
    )
    probability = 1.0 if log_upper >= 0.0 else math.exp(log_upper)
    return FiniteCollarCertificate(
        heat_time=t,
        curvature_radius=rho,
        coherence_radius=eta,
        denominator_ball_radius=delta,
        incident_staples=m,
        denominator_plaquette_radius=eta + delta,
        normalized_haar_ball_volume=volume,
        image_remainder_bound=q,
        heat_kernel_ratio_factor=ratio,
        finite_time_energy_gap=gap,
        log_bad_probability_upper_raw=log_upper,
        bad_probability_upper=probability,
        finite_time_bound_nontrivial=log_upper < 0.0,
        coherent_collar_required=True,
        collar_probability_certified=False,
        full_su2_block_measure_certified=False,
    )


def search_delta(
    heat_time: float,
    curvature_radius: float,
    coherence_radius: float,
    incident_staples: int = 6,
    iterations: int = 120,
) -> DeltaSearchCertificate:
    """Golden-section calibration of the auxiliary denominator radius.

    The returned point is always admissible.  No global optimality theorem is
    attached to this numerical search.
    """

    t = _positive("heat_time", heat_time)
    rho = _positive("curvature_radius", curvature_radius)
    eta = _positive("coherence_radius", coherence_radius)
    m = int(incident_staples)
    if m < 2 or iterations < 20:
        raise ValueError("invalid staple count or search iteration count")
    upper = rho / math.sqrt(m) - eta
    if upper <= 0.0:
        raise ValueError("no admissible denominator radius exists")
    left = max(1.0e-15, upper * 1.0e-9)
    right = upper * (1.0 - 1.0e-10)
    phi = (1.0 + math.sqrt(5.0)) / 2.0

    def objective(delta: float) -> float:
        return finite_collar_certificate(t, rho, eta, delta, m).log_bad_probability_upper_raw

    x1 = right - (right - left) / phi
    x2 = left + (right - left) / phi
    f1, f2 = objective(x1), objective(x2)
    for _ in range(iterations):
        if f1 <= f2:
            right, x2, f2 = x2, x1, f1
            x1 = right - (right - left) / phi
            f1 = objective(x1)
        else:
            left, x1, f1 = x1, x2, f2
            x2 = left + (right - left) / phi
            f2 = objective(x2)
    selected = x1 if f1 <= f2 else x2
    value = min(f1, f2)
    return DeltaSearchCertificate(
        heat_time=t,
        admissible_delta_upper=upper,
        selected_delta=selected,
        selected_log_bound=value,
        iterations=iterations,
        global_optimality_claimed=False,
    )


def maximum_heat_time_for_target(
    target_probability: float,
    curvature_radius: float = 0.0082,
    coherence_radius: float = 0.001,
    incident_staples: int = 6,
    time_upper: float = 3.0e-6,
) -> tuple[float, float]:
    target = float(target_probability)
    if not math.isfinite(target) or not 0.0 < target < 1.0:
        raise ValueError("target_probability must lie in (0,1)")
    upper = _positive("time_upper", time_upper)
    rho = _positive("curvature_radius", curvature_radius)
    eta = _positive("coherence_radius", coherence_radius)
    log_target = math.log(target)
    low = upper * 1.0e-5
    if search_delta(low, rho, eta, incident_staples).selected_log_bound > log_target:
        raise ValueError("time search lower endpoint does not certify the target")
    if search_delta(upper, rho, eta, incident_staples).selected_log_bound <= log_target:
        selected = search_delta(upper, rho, eta, incident_staples)
        return upper, selected.selected_delta
    for _ in range(70):
        mid = 0.5 * (low + upper)
        value = search_delta(mid, rho, eta, incident_staples).selected_log_bound
        if value <= log_target:
            low = mid
        else:
            upper = mid
    selected = search_delta(low, rho, eta, incident_staples)
    return low, selected.selected_delta


def calibration() -> FiniteCollarCalibration:
    t, rho, eta, m = 3.0e-6, 0.0082, 0.001, 6
    alpha, degree = 0.1, 18
    target = math.exp(-alpha) / degree**2
    frozen_search = search_delta(t, rho, eta, m)
    frozen = finite_collar_certificate(
        t, rho, eta, frozen_search.selected_delta, m
    )
    threshold_time, threshold_delta = maximum_heat_time_for_target(
        target, rho, eta, m, t
    )
    threshold = finite_collar_certificate(
        threshold_time, rho, eta, threshold_delta, m
    )
    return FiniteCollarCalibration(
        frozen_witness=frozen,
        frozen_delta_search=frozen_search,
        target_bad_weight=target,
        maximum_certified_heat_time_for_target=threshold_time,
        threshold_delta=threshold_delta,
        threshold_certificate=threshold,
        radial_monotonicity_used=True,
        claim_level="C2 finite-time one-link theorem under coherent collar",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    args = parser.parse_args()
    print(json.dumps(calibration().to_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
