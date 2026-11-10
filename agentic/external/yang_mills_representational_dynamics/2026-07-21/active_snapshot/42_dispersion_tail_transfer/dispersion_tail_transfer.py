"""Conditional transfer of a Gaussian dispersion tail to a nonlinear chart."""
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
    "08_su2_nonlinear_block_geometry",
    "21_curvature_typical_set_atlas",
    "23_local_cylinder_comparison",
    "35_linearized_dispersion_spectrum",
    "41_nonlinear_dispersion_geometry",
):
    path = PACKAGE / sibling
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from su2_nonlinear_block_geometry import product_log_bounds  # noqa: E402
from curvature_typical_set_atlas import (  # noqa: E402
    leverage_certificate,
    local_block_union_upper,
)
from local_cylinder_comparison import calibration as comparison_calibration  # noqa: E402
from linearized_dispersion_spectrum import tail_certificate  # noqa: E402
from nonlinear_dispersion_geometry import metric_factor  # noqa: E402


@dataclass(frozen=True)
class TailTransferCertificate:
    nonlinear_rms_threshold: float
    metric_factor: float
    logarithmic_remainder_per_staple: float
    reference_rms_threshold: float
    reference_tail_upper: float
    comparison_log_loss: float
    chart_complement_upper: float
    transferred_probability_upper: float
    target_probability: float
    restricted_reference_target_met: bool
    event_inclusion_proved: bool
    normalized_transfer_theorem_proved: bool
    density_comparison_uniform_in_retained_state: bool
    complement_uniform_in_retained_state: bool
    complete_nonlinear_transfer_proved: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def logarithmic_remainder_per_staple(link_radius: float) -> float:
    r = float(link_radius)
    if not math.isfinite(r) or r <= 0.0:
        raise ValueError("link radius must be finite and positive")
    bounds = product_log_bounds(3, r)
    return 0.5 * bounds.map_second_bound * 3.0 * r * r


def reference_rms_threshold(
    nonlinear_rms: float, staple_radius: float, remainder_per_staple: float
) -> float:
    eta = float(nonlinear_rms)
    epsilon = float(remainder_per_staple)
    if not math.isfinite(eta) or eta <= 0.0 or not math.isfinite(epsilon) or epsilon < 0.0:
        raise ValueError("invalid threshold data")
    return max(0.0, metric_factor(staple_radius) * eta - epsilon)


def transfer_certificate(
    nonlinear_rms: float,
    link_radius: float,
    comparison_log_loss: float,
    chart_complement_upper: float,
    target_probability: float,
    density_uniform: bool = False,
    complement_uniform: bool = False,
) -> TailTransferCertificate:
    r = float(link_radius)
    ell = float(comparison_log_loss)
    q_exc = float(chart_complement_upper)
    target = float(target_probability)
    if not math.isfinite(ell) or ell < 0.0 or not 0.0 <= q_exc < 1.0 or not 0.0 < target < 1.0:
        raise ValueError("invalid transfer inputs")
    staple_radius = product_log_bounds(3, r).output_geodesic_bound
    remainder = logarithmic_remainder_per_staple(r)
    reference_rms = reference_rms_threshold(nonlinear_rms, staple_radius, remainder)
    if reference_rms <= 0.0:
        q_reference = 1.0
    else:
        q_reference = tail_certificate(reference_rms).probability_upper
    transferred = math.exp(ell) * q_reference + q_exc
    premise = bool(density_uniform and complement_uniform)
    return TailTransferCertificate(
        nonlinear_rms_threshold=float(nonlinear_rms),
        metric_factor=metric_factor(staple_radius),
        logarithmic_remainder_per_staple=remainder,
        reference_rms_threshold=reference_rms,
        reference_tail_upper=q_reference,
        comparison_log_loss=ell,
        chart_complement_upper=q_exc,
        transferred_probability_upper=transferred,
        target_probability=target,
        restricted_reference_target_met=transferred <= target,
        event_inclusion_proved=True,
        normalized_transfer_theorem_proved=True,
        density_comparison_uniform_in_retained_state=bool(density_uniform),
        complement_uniform_in_retained_state=bool(complement_uniform),
        complete_nonlinear_transfer_proved=premise and transferred <= target,
    )


def calibration() -> dict[str, Any]:
    t = 3.0e-6
    blocks = 216
    star_plaquettes = 6
    dimension = 12
    qcrit = 0.0027927080803578997
    target = 0.0004860555003683996
    comparison = comparison_calibration()["comparison"]
    radius = comparison["local_radius"]
    covariance = t * leverage_certificate().max_four_link_variance_coefficient
    star_complement = local_block_union_upper(radius, star_plaquettes, dimension, covariance)
    ell = star_plaquettes * comparison["log_loss_per_support"]
    cert = transfer_certificate(.006, radius, ell, star_complement, target)
    return {
        "claim_level": "C2 normalized tail-transfer theorem plus restricted centered-reference calibration",
        "heat_time": t,
        "whole_block_locations": blocks,
        "star_plaquettes": star_plaquettes,
        "certificate": cert.to_dict(),
        "restricted_centered_reference_high_channel_closed": cert.restricted_reference_target_met,
        "physical_boundary_uniform_density_comparison_proved": False,
        "physical_boundary_uniform_complement_bound_proved": False,
        "first_open_implication": "establish both transfer premises for every positive-mass retained nonlinear SU(2) history",
    }


def main() -> None:
    argparse.ArgumentParser().parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
