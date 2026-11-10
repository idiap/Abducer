"""Spectral remedy frontier for coordinated curvature-polymer repairs."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any, Sequence

PACKAGE = Path(__file__).resolve().parents[1]
for sibling in (
    "32_dispersion_conditional_optimizer",
    "35_linearized_dispersion_spectrum",
    "42_dispersion_tail_transfer",
    "43_centered_star_repair",
    "44_link_lift_spillover",
):
    path = PACKAGE / sibling
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from dispersion_conditional_optimizer import calibration as low_calibration  # noqa: E402
from linearized_dispersion_spectrum import calibration as gaussian_calibration  # noqa: E402
from dispersion_tail_transfer import (  # noqa: E402
    logarithmic_remainder_per_staple,
)
from centered_star_repair import calibration as repair_calibration  # noqa: E402
from link_lift_spillover import calibration as spill_calibration  # noqa: E402


@dataclass(frozen=True)
class RemedyPoint:
    split_rms: float
    contraction: float
    spill_coefficient: float
    free_energy: float
    required_free_energy: float
    closes: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repair_free_energy(
    split_rms: float,
    maximum_rms: float,
    spill_coefficient: float,
    repaired_fraction: float = .99,
    staples: int = 6,
    colors: int = 3,
    heat_time: float = 3e-6,
    fixed_log_losses: float = 0.000398677049214764,
) -> float:
    eta = float(split_rms)
    maximum = float(maximum_rms)
    lam = float(spill_coefficient)
    fraction = float(repaired_fraction)
    if eta <= 0.0 or maximum <= eta or lam < 0.0 or not 0.0 < fraction < 1.0:
        raise ValueError("invalid remedy point")
    a = fraction * eta / maximum
    base = staples * eta * eta / (2.0 * heat_time)
    action = (1.0 - a * a) * base
    spill = (1.0 - a) ** 2 * lam * base
    jacobian = colors * (staples - 1) * math.log(1.0 / a)
    return action - spill - jacobian - fixed_log_losses


def admissible_spill_coefficient(
    split_rms: float,
    maximum_rms: float,
    required_free_energy: float,
    repaired_fraction: float = .99,
) -> float:
    eta = float(split_rms)
    maximum = float(maximum_rms)
    required = float(required_free_energy)
    a = repaired_fraction * eta / maximum
    if eta <= 0.0 or maximum <= eta or required < 0.0 or not 0.0 < a < 1.0:
        raise ValueError("invalid admissibility input")
    base = 6.0 * eta * eta / (2.0 * 3e-6)
    jacobian = 15.0 * math.log(1.0 / a)
    fixed = 0.000398677049214764
    numerator = (1.0 - a * a) * base - jacobian - fixed - required
    return max(0.0, numerator / ((1.0 - a) ** 2 * base))


def remedy_curve(
    splits: Sequence[float], maximum_rms: float, spill_coefficient: float, required: float
) -> tuple[RemedyPoint, ...]:
    result = []
    for split in splits:
        a = .99 * float(split) / maximum_rms
        free = repair_free_energy(split, maximum_rms, spill_coefficient)
        result.append(RemedyPoint(float(split), a, float(spill_coefficient), free, required, free > required))
    return tuple(result)


def calibration() -> dict[str, Any]:
    repair = repair_calibration()["certificate"]
    actual = spill_calibration()["spillover"]["maximum_spill_coefficient"]
    required = 7.62918774229502
    gaussian = gaussian_calibration()
    upper = min(
        low_calibration()["maximum_effective_rms_radius"],
        gaussian["maximum_rms_radius_for_coherent_channel"],
    )
    gaussian_min = gaussian["minimum_rms_radius_for_required_free_energy"]
    epsilon = logarithmic_remainder_per_staple(.006023157807602598)
    metric = .9999818608837214
    nonlinear_min = (gaussian_min + epsilon) / metric
    points = remedy_curve((nonlinear_min, .005, .006, .0065, .007, upper), repair["chart_maximum_rms"], actual, required)
    best = max(points, key=lambda point: point.free_energy)
    allowed = admissible_spill_coefficient(upper, repair["chart_maximum_rms"], required)
    return {
        "claim_level": "C2 exact spectral sufficient condition and finite remedy frontier",
        "nonlinear_split_interval": [nonlinear_min, upper],
        "actual_single_star_spill_coefficient": actual,
        "remedy_curve": [point.to_dict() for point in points],
        "best_actual_single_star_point": best.to_dict(),
        "maximum_admissible_spill_at_upper_split": allowed,
        "required_spill_reduction_factor": allowed / actual,
        "actual_single_star_route_closes_anywhere": any(point.closes for point in points),
        "coordinated_polymer_sufficient_condition_proved": True,
        "physical_coordinated_repair_constructed": False,
    }


def main() -> None:
    argparse.ArgumentParser().parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
