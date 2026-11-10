"""Normalized comparison on dependency-safe local cylinders.

The theorem in this module is measure-theoretic.  It turns a uniform
oscillation bound on a good set and a reference complement bound into a
normalized density comparison.  The calibration combines the local-union
certificate of Stage 21 with the sharp finite-radius remainder of Stage 22.
It does not assert that these estimates are already uniform over every
retained Yang--Mills boundary state.
"""

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
for sibling in ("21_curvature_typical_set_atlas", "22_sharp_nonlinear_overlap"):
    path = PACKAGE / sibling
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from curvature_typical_set_atlas import (  # noqa: E402
    leverage_certificate,
    local_block_union_radius,
    local_block_union_upper,
)
from sharp_nonlinear_overlap import sharp_overlap_certificate  # noqa: E402


@dataclass(frozen=True)
class LocalComparisonCertificate:
    support_units: int
    local_radius: float
    local_hessian_remainder: float
    oscillation_loss_per_support: float
    reference_complement_upper: float
    coverage_log_loss: float
    total_log_loss: float
    log_loss_per_support: float
    target_log_loss_per_support: float
    target_met: bool
    normalized_restriction_theorem_applies: bool
    uniform_boundary_hypothesis_verified: bool
    full_measure_comparison_proved: bool

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


@dataclass(frozen=True)
class FiniteKernelCertificate:
    normalizer: float
    good_mass: float
    bad_mass: float
    conditional_good_probability: float
    strictly_positive: bool
    normalized: bool

    def to_dict(self) -> dict[str, float | bool]:
        return asdict(self)


def normalized_restriction_log_loss(
    oscillation_loss: float, reference_complement_upper: float
) -> float:
    """Return kappa-log(1-delta) for the restricted-density theorem.

    If ``d mu_G/d nu_G`` is proportional to ``exp(-R)`` on ``G``, with
    ``osc_G R <= kappa`` and ``nu(G)>=1-delta``, then

        mu_G(A) <= exp(kappa)/(1-delta) * nu(A).
    """

    kappa = float(oscillation_loss)
    delta = float(reference_complement_upper)
    if not math.isfinite(kappa) or kappa < 0.0:
        raise ValueError("oscillation_loss must be finite and nonnegative")
    if not math.isfinite(delta) or not 0.0 <= delta < 1.0:
        raise ValueError("reference complement must lie in [0,1)")
    return kappa - math.log1p(-delta)


def local_comparison_certificate(
    support_units: int,
    local_radius: float,
    local_hessian_remainder: float,
    reference_complement_upper: float,
    target_log_loss_per_support: float = 0.2,
    uniform_boundary_hypothesis_verified: bool = False,
) -> LocalComparisonCertificate:
    m = int(support_units)
    r = float(local_radius)
    h = float(local_hessian_remainder)
    delta = float(reference_complement_upper)
    target = float(target_log_loss_per_support)
    if m < 1:
        raise ValueError("support_units must be positive")
    if not math.isfinite(r) or r <= 0.0:
        raise ValueError("local_radius must be finite and positive")
    if not math.isfinite(h) or h < 0.0:
        raise ValueError("local_hessian_remainder must be finite and nonnegative")
    if not math.isfinite(target) or target <= 0.0:
        raise ValueError("target must be finite and positive")
    local_oscillation = h * r * r
    total_oscillation = m * local_oscillation
    total = normalized_restriction_log_loss(total_oscillation, delta)
    return LocalComparisonCertificate(
        support_units=m,
        local_radius=r,
        local_hessian_remainder=h,
        oscillation_loss_per_support=local_oscillation,
        reference_complement_upper=delta,
        coverage_log_loss=-math.log1p(-delta),
        total_log_loss=total,
        log_loss_per_support=total / m,
        target_log_loss_per_support=target,
        target_met=total / m <= target,
        normalized_restriction_theorem_applies=True,
        uniform_boundary_hypothesis_verified=bool(uniform_boundary_hypothesis_verified),
        full_measure_comparison_proved=False,
    )


def finite_positive_conditional_kernel(
    weights: Sequence[float], good_mask: Sequence[bool]
) -> tuple[np.ndarray, FiniteKernelCertificate]:
    """Normalize a finite positive fiber weight and expose its good channel."""

    values = np.asarray(weights, dtype=float)
    mask = np.asarray(good_mask, dtype=bool)
    if values.ndim != 1 or values.size == 0 or mask.shape != values.shape:
        raise ValueError("weights and good_mask must be matching nonempty vectors")
    if not np.all(np.isfinite(values)) or np.any(values <= 0.0):
        raise ValueError("conditional weights must be finite and strictly positive")
    normalizer = float(np.sum(values))
    probabilities = values / normalizer
    good = float(np.sum(values[mask]))
    bad = normalizer - good
    cert = FiniteKernelCertificate(
        normalizer=normalizer,
        good_mass=good,
        bad_mass=bad,
        conditional_good_probability=good / normalizer,
        strictly_positive=True,
        normalized=abs(float(np.sum(probabilities)) - 1.0) <= 1.0e-14,
    )
    return probabilities, cert


def calibration() -> dict[str, object]:
    t = 3.0e-6
    blocks = 216
    dimension = 12
    qcrit = 0.0027927080803578997
    leverage = leverage_certificate()
    covariance = t * leverage.max_four_link_variance_coefficient
    radius = local_block_union_radius(blocks, dimension, covariance, qcrit)
    delta = local_block_union_upper(radius, blocks, dimension, covariance)
    nonlinear = sharp_overlap_certificate(radius, t, 0.001)
    comparison = local_comparison_certificate(
        blocks,
        radius,
        nonlinear.total_hessian_remainder,
        delta,
        0.2,
        uniform_boundary_hypothesis_verified=False,
    )
    _, finite = finite_positive_conditional_kernel([1.0, 2.0, 3.0], [True, True, False])
    return {
        "claim_level": "C2 normalized local-cylinder theorem plus C1 frozen-reference calibration",
        "heat_time": t,
        "comparison": comparison.to_dict(),
        "finite_positive_kernel_example": finite.to_dict(),
        "global_ball_replaced_by_local_cylinders": True,
        "frozen_centered_reference_loss_target_closed": comparison.target_met,
        "complete_boundary_uniform_su2_comparison_proved": False,
        "first_unproved_implication": (
            "prove the same local oscillation and complement estimates uniformly over "
            "every positive-mass retained SU(2) boundary state"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
