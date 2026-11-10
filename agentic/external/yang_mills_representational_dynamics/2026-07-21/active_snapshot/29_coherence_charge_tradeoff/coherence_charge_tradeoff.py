"""Overlap-correct multi-link charging and the coherence--charge trade-off.

If each failed collar forces incident squared-curvature energy eta^2/2 and
each plaquette is counted by at most nu selected witnesses, k witnesses force
global energy at least k eta^2/(2 nu).  With heat-kernel exponent 1/(2t), the
Gibbs exponent is k eta^2/(4 nu t).

Connected-witness entropy at degree D and state weight alpha is controlled by

    theta = exp(alpha) D^2 exp[-eta^2/(4 nu t)].

This module tests whether the eta accepted by the coherent conditional bound
also makes theta<1 and supplies the required residual free energy.  It does
not assume additivity when witnesses overlap.
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
    "22_sharp_nonlinear_overlap",
    "25_one_scale_kr_composition",
    "28_coherent_partition_optimizer",
):
    path = PACKAGE / sibling
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from sharp_nonlinear_overlap import maximal_certified_radius  # noqa: E402
from one_scale_kr_composition import local_reference_budget  # noqa: E402
from coherent_partition_optimizer import (  # noqa: E402
    HEAT_TIME,
    INCIDENT_STAPLES,
    TARGET_WEIGHTED_CEILING,
    optimize_delta,
)


DEGREE = 18
ALPHA = 0.1


@dataclass(frozen=True)
class MultiWitnessChargeCertificate:
    witness_count: int
    coherence_radius: float
    overlap_multiplicity: int
    local_energy_charge: float
    global_energy_charge: float
    gibbs_exponent: float
    naive_disjoint_exponent: float
    overlap_correction_applied: bool

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


@dataclass(frozen=True)
class ContourFreeEnergyCertificate:
    coherence_radius: float
    heat_time: float
    overlap_multiplicity: int
    adjacency_degree: int
    state_weight_alpha: float
    minimum_contour_size: int
    exponent_per_witness: float
    effective_activity: float
    branching_ratio: float
    rooted_sum_upper: float
    rooted_free_energy_lower: float
    strict_entropy_convergence: bool
    required_free_energy: float
    required_free_energy_met: bool

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


@dataclass(frozen=True)
class TradeoffCertificate:
    maximum_nonlinear_local_radius: float
    maximum_curvature_chain_radius: float
    available_coherent_probability_budget: float
    maximum_coherence_radius_accepted_by_coherent_bound: float
    minimum_coherence_radius_for_entropy_convergence: float
    minimum_coherence_radius_for_required_contour_free_energy: float
    overlap_multiplicity: int
    feasible_interval_width: float
    common_eta_exists: bool
    maximum_effective_degree_for_convergence: float
    maximum_effective_degree_for_required_free_energy: float | None
    actual_degree: int
    degree_reduction_factor_for_convergence: float
    degree_reduction_factor_for_required_free_energy: float | None
    degree_only_repair_suffices_for_required_free_energy: bool
    charge_amplification_for_convergence: float
    charge_amplification_for_required_free_energy: float
    complete_measure_numerator_proved: bool

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


def _positive(name: str, value: float) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return x


def multi_witness_charge(witness_count: int, coherence_radius: float, overlap_multiplicity: int, heat_time: float = HEAT_TIME) -> MultiWitnessChargeCertificate:
    k = int(witness_count)
    nu = int(overlap_multiplicity)
    eta = _positive("coherence_radius", coherence_radius)
    t = _positive("heat_time", heat_time)
    if k < 1 or nu < 1 or nu > k:
        raise ValueError("require 1 <= overlap_multiplicity <= witness_count")
    local = eta * eta / 2.0
    global_charge = k * local / nu
    exponent = global_charge / (2.0 * t)
    naive = k * local / (2.0 * t)
    return MultiWitnessChargeCertificate(
        witness_count=k,
        coherence_radius=eta,
        overlap_multiplicity=nu,
        local_energy_charge=local,
        global_energy_charge=global_charge,
        gibbs_exponent=exponent,
        naive_disjoint_exponent=naive,
        overlap_correction_applied=True,
    )


def eta_for_entropy_convergence(overlap_multiplicity: int = 1, degree: int = DEGREE, alpha: float = ALPHA, heat_time: float = HEAT_TIME) -> float:
    nu, d = int(overlap_multiplicity), int(degree)
    t = _positive("heat_time", heat_time)
    a = float(alpha)
    if nu < 1 or d < 2 or not math.isfinite(a) or a < 0.0:
        raise ValueError("invalid overlap, degree, or alpha")
    return math.sqrt(4.0 * nu * t * (a + 2.0 * math.log(d)))


def contour_free_energy(coherence_radius: float, overlap_multiplicity: int = 1, minimum_contour_size: int = 2, required_free_energy: float = 6.712921011389365, degree: int = DEGREE, alpha: float = ALPHA, heat_time: float = HEAT_TIME) -> ContourFreeEnergyCertificate:
    eta = _positive("coherence_radius", coherence_radius)
    nu, k0, d = int(overlap_multiplicity), int(minimum_contour_size), int(degree)
    required = _positive("required_free_energy", required_free_energy)
    t = _positive("heat_time", heat_time)
    a = float(alpha)
    if nu < 1 or k0 < 1 or d < 2 or not math.isfinite(a) or a < 0.0:
        raise ValueError("invalid contour parameters")
    exponent = eta * eta / (4.0 * nu * t)
    activity = math.exp(-exponent)
    theta = math.exp(a) * d * d * activity
    if theta < 1.0:
        rooted = math.exp(a * k0) * activity**k0 * d ** (2 * (k0 - 1)) / (1.0 - theta)
        free_energy = -math.log(rooted)
    else:
        rooted = math.inf
        free_energy = -math.inf
    return ContourFreeEnergyCertificate(
        coherence_radius=eta,
        heat_time=t,
        overlap_multiplicity=nu,
        adjacency_degree=d,
        state_weight_alpha=a,
        minimum_contour_size=k0,
        exponent_per_witness=exponent,
        effective_activity=activity,
        branching_ratio=theta,
        rooted_sum_upper=rooted,
        rooted_free_energy_lower=free_energy,
        strict_entropy_convergence=theta < 1.0,
        required_free_energy=required,
        required_free_energy_met=free_energy > required,
    )


def eta_for_contour_target(required_free_energy: float = 6.712921011389365, overlap_multiplicity: int = 1, minimum_contour_size: int = 2, degree: int = DEGREE, alpha: float = ALPHA) -> float:
    required = _positive("required_free_energy", required_free_energy)
    low = eta_for_entropy_convergence(overlap_multiplicity, degree, alpha) * (1.0 + 1.0e-12)
    high = max(2.0 * low, 0.02)
    while not contour_free_energy(high, overlap_multiplicity, minimum_contour_size, required, degree, alpha).required_free_energy_met:
        high *= 1.5
        if high >= 1.0:
            raise ArithmeticError("failed to bracket the contour free-energy target")
    for _ in range(120):
        middle = 0.5 * (low + high)
        if contour_free_energy(middle, overlap_multiplicity, minimum_contour_size, required, degree, alpha).required_free_energy_met:
            high = middle
        else:
            low = middle
    return high


def rooted_free_energy_at_degree(coherence_radius: float, degree: float, overlap_multiplicity: int = 1, minimum_contour_size: int = 2, alpha: float = ALPHA, heat_time: float = HEAT_TIME, charge_amplification: float = 1.0) -> float:
    eta = _positive("coherence_radius", coherence_radius)
    d = float(degree)
    nu, k0 = int(overlap_multiplicity), int(minimum_contour_size)
    t = _positive("heat_time", heat_time)
    amplification = _positive("charge_amplification", charge_amplification)
    if not math.isfinite(d) or d < 1.0 or nu < 1 or k0 < 1:
        raise ValueError("invalid continuous contour parameters")
    exponent = amplification * eta * eta / (4.0 * nu * t)
    theta = math.exp(alpha) * d * d * math.exp(-exponent)
    if theta >= 1.0:
        return -math.inf
    return k0 * exponent - alpha * k0 - 2.0 * (k0 - 1) * math.log(d) + math.log(1.0 - theta)


def maximum_degree_for_target(coherence_radius: float, required_free_energy: float, overlap_multiplicity: int = 1, minimum_contour_size: int = 2, degree_upper: float = DEGREE) -> float | None:
    eta = _positive("coherence_radius", coherence_radius)
    required = _positive("required_free_energy", required_free_energy)
    upper = _positive("degree_upper", degree_upper)
    low = 1.0
    if rooted_free_energy_at_degree(eta, low, overlap_multiplicity, minimum_contour_size) <= required:
        return None
    if rooted_free_energy_at_degree(eta, upper, overlap_multiplicity, minimum_contour_size) > required:
        return upper
    high = upper
    for _ in range(120):
        middle = 0.5 * (low + high)
        if rooted_free_energy_at_degree(eta, middle, overlap_multiplicity, minimum_contour_size) > required:
            low = middle
        else:
            high = middle
    return low


def coherent_eta_ceiling(curvature_radius: float, probability_budget: float) -> float:
    rho = _positive("curvature_radius", curvature_radius)
    target = float(probability_budget)
    if not math.isfinite(target) or not 0.0 < target < 1.0:
        raise ValueError("probability_budget must lie in (0,1)")

    def log_value(eta: float) -> float:
        try:
            return optimize_delta(HEAT_TIME, rho, eta, INCIDENT_STAPLES).log_probability_upper
        except ValueError:
            return math.inf

    low, high = 0.0, rho / math.sqrt(INCIDENT_STAPLES) * (1.0 - 1.0e-10)
    target_log = math.log(target)
    if log_value(low) > target_log:
        raise ValueError("even ideal coherence does not meet the probability budget")
    if log_value(high) <= target_log:
        return high
    for _ in range(120):
        middle = 0.5 * (low + high)
        if log_value(middle) <= target_log:
            low = middle
        else:
            high = middle
    return low


def tradeoff_certificate(overlap_multiplicity: int = 1, minimum_contour_size: int = 2, required_free_energy: float = 6.712921011389365) -> TradeoffCertificate:
    nu = int(overlap_multiplicity)
    if nu < 1:
        raise ValueError("overlap_multiplicity must be positive")
    maximum = maximal_certified_radius(HEAT_TIME, 0.001)
    probe = maximum * (1.0 - 1.0e-9)
    _, _, corrected_reference = local_reference_budget(probe)
    available = TARGET_WEIGHTED_CEILING - corrected_reference
    if available <= 0.0:
        raise ArithmeticError("no coherent probability budget remains")
    rho = 2.0 * probe
    eta_coherent = coherent_eta_ceiling(rho, available)
    eta_entropy = eta_for_entropy_convergence(nu)
    eta_target = eta_for_contour_target(required_free_energy, nu, minimum_contour_size)
    width = eta_coherent - eta_target
    exponent_at_ceiling = eta_coherent**2 / (4.0 * nu * HEAT_TIME)
    convergence_degree = math.exp(0.5 * (exponent_at_ceiling - ALPHA))
    target_degree = maximum_degree_for_target(
        eta_coherent, required_free_energy, nu, minimum_contour_size
    )
    convergence_amplification = (ALPHA + 2.0 * math.log(DEGREE)) / exponent_at_ceiling
    target_amplification = (eta_target / eta_coherent) ** 2
    return TradeoffCertificate(
        maximum_nonlinear_local_radius=probe,
        maximum_curvature_chain_radius=rho,
        available_coherent_probability_budget=available,
        maximum_coherence_radius_accepted_by_coherent_bound=eta_coherent,
        minimum_coherence_radius_for_entropy_convergence=eta_entropy,
        minimum_coherence_radius_for_required_contour_free_energy=eta_target,
        overlap_multiplicity=nu,
        feasible_interval_width=width,
        common_eta_exists=width > 0.0,
        maximum_effective_degree_for_convergence=convergence_degree,
        maximum_effective_degree_for_required_free_energy=target_degree,
        actual_degree=DEGREE,
        degree_reduction_factor_for_convergence=DEGREE / convergence_degree,
        degree_reduction_factor_for_required_free_energy=(
            DEGREE / target_degree if target_degree is not None else None
        ),
        degree_only_repair_suffices_for_required_free_energy=target_degree is not None,
        charge_amplification_for_convergence=convergence_amplification,
        charge_amplification_for_required_free_energy=target_amplification,
        complete_measure_numerator_proved=False,
    )


def identical_witness_counterexample(witness_count: int = 8, coherence_radius: float = 0.001) -> dict[str, float | int | bool]:
    k = int(witness_count)
    if k < 2:
        raise ValueError("counterexample requires at least two repeated witnesses")
    corrected = multi_witness_charge(k, coherence_radius, k)
    return {
        "witness_count": k,
        "overlap_multiplicity": k,
        "naive_gibbs_exponent": corrected.naive_disjoint_exponent,
        "overlap_corrected_gibbs_exponent": corrected.gibbs_exponent,
        "naive_overstatement_factor": corrected.naive_disjoint_exponent / corrected.gibbs_exponent,
        "additivity_without_overlap_control_valid": False,
    }


def calibration() -> dict[str, Any]:
    tradeoff = tradeoff_certificate()
    eta_target = tradeoff.minimum_coherence_radius_for_required_contour_free_energy
    return {
        "claim_level": "C2 overlap-correct charge theorem and quantitative trade-off no-overlap result",
        "multi_witness_example": multi_witness_charge(5, 0.001, 2).to_dict(),
        "identical_witness_counterexample": identical_witness_counterexample(),
        "ideal_overlap_one_tradeoff": tradeoff.to_dict(),
        "overlap_two_tradeoff": tradeoff_certificate(overlap_multiplicity=2).to_dict(),
        "contour_target_witness": contour_free_energy(eta_target * (1.0 + 1.0e-8)).to_dict(),
        "same_eta_closes_coherent_and_incoherent_channels": tradeoff.common_eta_exists,
        "interpretation": (
            "even at overlap multiplicity one and the largest certified nonlinear radius, "
            "the current coherent-bound eta ceiling lies below the eta needed to pay "
            "degree-18 connected entropy and the required free energy"
        ),
        "repair_options": [
            "reduce the effective connected-witness branching degree",
            "strengthen deterministic collar-failure charge by the calibrated amplification factor",
            "improve the coherent numerator comparison so that it accepts a larger eta",
            "construct a sector-aware polymer whose entropy is lower than D^2 counting",
        ],
        "volume_uniform_complete_su2_numerator_proved": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
