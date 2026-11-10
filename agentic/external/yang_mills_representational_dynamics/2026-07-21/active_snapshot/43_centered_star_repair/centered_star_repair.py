"""Exact radial repair on the centered tangent space of one staple star."""
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

from su2_nonlinear_block_geometry import product_log_bounds  # noqa: E402
from curvature_typical_set_atlas import calibration as typical_calibration  # noqa: E402


@dataclass(frozen=True)
class CenteredRepairCertificate:
    staples: int
    color_dimension: int
    centered_dimension: int
    heat_time: float
    bad_rms_threshold: float
    chart_maximum_rms: float
    repaired_maximum_rms: float
    contraction: float
    minimum_action_drop: float
    log_jacobian_loss: float
    ideal_free_energy: float
    ideal_congestion_upper: float
    maps_chart_into_good_region: bool
    mean_preserved: bool
    adjoint_equivariant: bool
    complete_link_fiber_lift_proved: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def centered_projection(staples: int) -> np.ndarray:
    m = int(staples)
    if m < 2:
        raise ValueError("at least two staples are required")
    return np.eye(m) - np.ones((m, m)) / m


def centered_rms(vectors: Sequence[Sequence[float]]) -> float:
    values = np.asarray(vectors, dtype=float)
    if values.ndim != 2 or values.shape[0] < 2 or not np.all(np.isfinite(values)):
        raise ValueError("vectors must be a finite matrix with at least two rows")
    centered = centered_projection(values.shape[0]) @ values
    return math.sqrt(float(np.sum(centered * centered)) / values.shape[0])


def repair_centered(vectors: Sequence[Sequence[float]], contraction: float) -> np.ndarray:
    values = np.asarray(vectors, dtype=float)
    a = float(contraction)
    if values.ndim != 2 or values.shape[0] < 2 or not np.all(np.isfinite(values)):
        raise ValueError("invalid staple coordinates")
    if not math.isfinite(a) or not 0.0 < a < 1.0:
        raise ValueError("contraction must lie strictly between zero and one")
    mean = np.mean(values, axis=0, keepdims=True)
    return mean + a * (values - mean)


def repair_certificate(
    staples: int,
    color_dimension: int,
    heat_time: float,
    bad_rms_threshold: float,
    chart_maximum_rms: float,
    repaired_maximum_rms: float,
) -> CenteredRepairCertificate:
    m = int(staples)
    c = int(color_dimension)
    t = float(heat_time)
    eta = float(bad_rms_threshold)
    maximum = float(chart_maximum_rms)
    target = float(repaired_maximum_rms)
    if m < 2 or c < 1 or t <= 0.0 or eta <= 0.0 or maximum <= eta or not 0.0 < target < eta:
        raise ValueError("invalid repair parameters")
    a = target / maximum
    dimension = c * (m - 1)
    action_drop = (1.0 - a * a) * m * eta * eta / (2.0 * t)
    jacobian = dimension * math.log(1.0 / a)
    free_energy = action_drop - jacobian
    return CenteredRepairCertificate(
        staples=m,
        color_dimension=c,
        centered_dimension=dimension,
        heat_time=t,
        bad_rms_threshold=eta,
        chart_maximum_rms=maximum,
        repaired_maximum_rms=target,
        contraction=a,
        minimum_action_drop=action_drop,
        log_jacobian_loss=jacobian,
        ideal_free_energy=free_energy,
        ideal_congestion_upper=math.exp(-free_energy),
        maps_chart_into_good_region=a * maximum <= target + 1e-15,
        mean_preserved=True,
        adjoint_equivariant=True,
        complete_link_fiber_lift_proved=False,
    )


def calibration() -> dict[str, Any]:
    link_radius = typical_calibration()["four_link_plaquette_input_radius"]["certified_radius"]
    staple_radius = product_log_bounds(3, link_radius).output_geodesic_bound
    maximum_rms = 2.0 * staple_radius
    certificate = repair_certificate(6, 3, 3e-6, .006, maximum_rms, .00594)
    return {
        "claim_level": "C2 exact centered-Gaussian star repair theorem",
        "certificate": certificate.to_dict(),
        "equal_channel_free_energy_target": 7.62918774229502,
        "ideal_tangent_star_repair_closes": certificate.ideal_free_energy > 7.62918774229502,
        "haar_density_loss_included": False,
        "external_plaquette_spillover_included": False,
        "nonlinear_link_realizability_proved": False,
    }


def main() -> None:
    argparse.ArgumentParser().parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
