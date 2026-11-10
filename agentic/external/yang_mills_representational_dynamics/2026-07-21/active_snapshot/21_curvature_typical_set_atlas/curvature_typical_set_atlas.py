"""Dependency-aware Gaussian typical sets and a two-center SU(2) atlas."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path
import sys
from typing import Sequence

import numpy as np


PACKAGE = Path(__file__).resolve().parents[1]
STAGE08 = PACKAGE / "08_su2_nonlinear_block_geometry"
STAGE17 = PACKAGE / "17_chart_density_comparison"
for path in (STAGE08, STAGE17):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from su2_nonlinear_block_geometry import build_block_complex  # noqa: E402
from chart_density_comparison import gaussian_ball_log_mass  # noqa: E402


@dataclass(frozen=True)
class LocalRadiusCertificate:
    block_count: int
    block_dimension: int
    covariance_operator_coefficient: float
    heat_time: float
    target_complement_probability: float
    certified_radius: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


@dataclass(frozen=True)
class LeverageCertificate:
    physical_scalar_dimension: int
    hessian_min: float
    hessian_max: float
    max_link_variance_coefficient: float
    max_four_link_variance_coefficient: float
    max_curvature_variance_coefficient: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def local_block_union_radius(
    block_count: int,
    block_dimension: int,
    covariance_operator: float,
    target_complement_probability: float,
) -> float:
    if not isinstance(block_count, int) or block_count < 1:
        raise ValueError("block_count must be a positive integer")
    if not isinstance(block_dimension, int) or block_dimension < 1:
        raise ValueError("block_dimension must be a positive integer")
    covariance_operator = float(covariance_operator)
    delta = float(target_complement_probability)
    if not math.isfinite(covariance_operator) or covariance_operator <= 0.0:
        raise ValueError("covariance_operator must be finite and positive")
    if not math.isfinite(delta) or not 0.0 < delta < 1.0:
        raise ValueError("target probability must lie strictly between zero and one")
    return math.sqrt(covariance_operator) * (
        math.sqrt(block_dimension) + math.sqrt(2.0 * math.log(block_count / delta))
    )


def local_block_union_upper(
    radius: float,
    block_count: int,
    block_dimension: int,
    covariance_operator: float,
) -> float:
    radius = float(radius)
    if not math.isfinite(radius) or radius < 0.0:
        raise ValueError("radius must be finite and nonnegative")
    scale = math.sqrt(float(covariance_operator))
    standardized = radius / scale
    if standardized <= math.sqrt(block_dimension):
        return 1.0
    exponent = 0.5 * (standardized - math.sqrt(block_dimension)) ** 2
    return min(1.0, block_count * math.exp(-exponent))


def physical_covariance() -> tuple[object, np.ndarray, np.ndarray, np.ndarray]:
    block = build_block_complex()
    # Columns of Q span ker(d0^T), the Coulomb physical link space.
    _, singular, vh = np.linalg.svd(block.d0.T, full_matrices=True)
    rank = int(np.sum(singular > 1e-10))
    q = vh[rank:].T
    hessian = q.T @ block.d1.T @ block.d1 @ q
    covariance = q @ np.linalg.inv(hessian) @ q.T
    curvature_covariance = block.d1 @ covariance @ block.d1.T
    return block, hessian, covariance, curvature_covariance


def leverage_certificate() -> LeverageCertificate:
    block, hessian, covariance, curvature = physical_covariance()
    local_max = 0.0
    for row in block.d1:
        edges = np.flatnonzero(row)
        local = covariance[np.ix_(edges, edges)]
        local_max = max(local_max, float(np.linalg.eigvalsh(local)[-1]))
    return LeverageCertificate(
        physical_scalar_dimension=hessian.shape[0],
        hessian_min=float(np.linalg.eigvalsh(hessian)[0]),
        hessian_max=float(np.linalg.eigvalsh(hessian)[-1]),
        max_link_variance_coefficient=float(np.max(np.diag(covariance))),
        max_four_link_variance_coefficient=local_max,
        max_curvature_variance_coefficient=float(np.max(np.diag(curvature))),
    )


def su2_exp(axis_angle: Sequence[float]) -> np.ndarray:
    x = np.asarray(axis_angle, dtype=float)
    radius = float(np.linalg.norm(x))
    if radius == 0.0:
        return np.array([1.0, 0.0, 0.0, 0.0])
    return np.concatenate(([math.cos(radius)], math.sin(radius) * x / radius))


def center_atlas_coordinate(quaternion: Sequence[float]) -> tuple[int, np.ndarray]:
    q = np.asarray(quaternion, dtype=float)
    norm = float(np.linalg.norm(q))
    if not math.isfinite(norm) or norm <= 0.0:
        raise ValueError("quaternion must have positive finite norm")
    q = q / norm
    center = 1 if q[0] >= 0.0 else -1
    local = center * q
    angle = math.acos(float(np.clip(local[0], -1.0, 1.0)))
    vector_norm = float(np.linalg.norm(local[1:]))
    if vector_norm < 1e-15:
        coordinate = np.zeros(3)
    else:
        coordinate = angle * local[1:] / vector_norm
    return center, coordinate


def center_atlas_reconstruct(center: int, coordinate: Sequence[float]) -> np.ndarray:
    if center not in (-1, 1):
        raise ValueError("center must be +1 or -1")
    return center * su2_exp(coordinate)


def normalized_haar_jacobian(radius: float) -> float:
    radius = float(radius)
    if not math.isfinite(radius) or radius < 0.0 or radius > math.pi:
        raise ValueError("radius must lie in [0,pi]")
    sinc = 1.0 if radius == 0.0 else math.sin(radius) / radius
    return sinc * sinc / (2.0 * math.pi**2)


def center_atlas_jacobian_ratio_bound() -> float:
    # Every element is represented within radius pi/2 of one of the two centers.
    return (math.pi / 2.0) ** 2


def calibration() -> dict[str, object]:
    t = 3.0e-6
    plaquettes = 216
    qcrit = 0.0027927080803578997
    leverage = leverage_certificate()
    link = LocalRadiusCertificate(
        plaquettes, 3, leverage.max_link_variance_coefficient, t, qcrit,
        local_block_union_radius(plaquettes, 3, t * leverage.max_link_variance_coefficient, qcrit),
    )
    local = LocalRadiusCertificate(
        plaquettes, 12, leverage.max_four_link_variance_coefficient, t, qcrit,
        local_block_union_radius(plaquettes, 12, t * leverage.max_four_link_variance_coefficient, qcrit),
    )
    curvature = LocalRadiusCertificate(
        plaquettes, 3, leverage.max_curvature_variance_coefficient, t, qcrit,
        local_block_union_radius(plaquettes, 3, t * leverage.max_curvature_variance_coefficient, qcrit),
    )
    global_log_mass = gaussian_ball_log_mass(408, t, 0.003)
    return {
        "claim_level": "C2 Gaussian local-union theorem plus C1 finite spectral calibration",
        "heat_time": t,
        "plaquettes": plaquettes,
        "critical_complement_probability": qcrit,
        "leverage": leverage.to_dict(),
        "link_radius": link.to_dict(),
        "four_link_plaquette_input_radius": local.to_dict(),
        "curvature_radius": curvature.to_dict(),
        "existing_local_radius": 0.003,
        "existing_local_radius_union_upper": local_block_union_upper(
            0.003, plaquettes, 12, t * leverage.max_four_link_variance_coefficient
        ),
        "global_408_ball_log_mass_at_0_003": global_log_mass,
        "two_center_atlas": {
            "covers_su2": True,
            "maximum_local_radius": math.pi / 2.0,
            "maximum_multiplicity": 2,
            "normalized_haar_jacobian_max": normalized_haar_jacobian(0.0),
            "normalized_haar_jacobian_min": normalized_haar_jacobian(math.pi / 2.0),
            "jacobian_ratio_bound": center_atlas_jacobian_ratio_bound(),
            "tree_gauge_faddeev_popov_factor": 1.0,
        },
        "nonlinear_overlap_proved": False,
        "full_measure_defect_charge_proved": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
