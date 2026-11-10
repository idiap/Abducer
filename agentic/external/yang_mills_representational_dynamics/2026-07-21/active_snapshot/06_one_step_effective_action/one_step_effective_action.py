"""One-step effective-action certificates for a retained/fiber split.

The module implements the finite-dimensional algebra behind one exact RG
marginalization.  Its inputs are *declared derivative bounds* on a local
effective action.  It does not establish those bounds for the full
four-dimensional Yang--Mills measure.

All derivative budgets are dimensionless.  With heat-time parameter ``t``:

    t ||R_zz|| <= eps_fiber
    t ||R_zy|| <= eps_cross
    t ||R_yy|| <= eps_base
    t ||D_z R_zz|| <= tau_fiber
    t ||D_z R_zy|| <= tau_cross

The tangent quadratic fiber operator has lower bound ``lambda_fiber``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from typing import Any

import numpy as np


def _finite_nonnegative(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


def _finite_positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


@dataclass(frozen=True)
class LocalActionNorm:
    """Scaled local derivative budgets for ``S=Q/t+R``."""

    eps_fiber: float
    eps_cross: float
    eps_base: float
    tau_fiber: float
    tau_cross: float

    def __post_init__(self) -> None:
        for name, value in asdict(self).items():
            object.__setattr__(self, name, _finite_nonnegative(name, value))


@dataclass(frozen=True)
class DefectNorm:
    """Scaled C2 budget for the bad/good partition-function ratio delta.

    ``activity`` bounds delta itself, ``gradient`` bounds
    ``sqrt(t)||D delta||``, and ``hessian`` bounds ``t||D2 delta||``.
    The pointwise conditions delta >= 0 and gauge invariance are theorem
    hypotheses external to this numerical record.
    """

    activity: float = 0.0
    gradient: float = 0.0
    hessian: float = 0.0

    def __post_init__(self) -> None:
        for name, value in asdict(self).items():
            object.__setattr__(self, name, _finite_nonnegative(name, value))

    @property
    def effective_hessian_budget(self) -> float:
        return self.hessian + self.gradient**2


@dataclass(frozen=True)
class OneStepCertificate:
    lambda_fiber: float
    lambda_base: float
    fiber_radius: float
    fiber_margin: float
    minimizer_response_bound: float
    centered_cross_budget: float
    centered_transport_coefficient: float
    generated_good_hessian_budget: float
    defect_hessian_budget: float
    generated_full_hessian_budget: float
    generated_base_margin: float
    fiber_contraction_certified: bool
    generated_base_coercive: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def one_step_certificate(
    lambda_fiber: float,
    lambda_base: float,
    fiber_radius: float,
    action: LocalActionNorm,
    defect: DefectNorm | None = None,
) -> OneStepCertificate:
    """Calculate the exact theorem budgets and fail closed on lost coercivity."""

    lambda_fiber = _finite_positive("lambda_fiber", lambda_fiber)
    lambda_base = _finite_nonnegative("lambda_base", lambda_base)
    fiber_radius = _finite_nonnegative("fiber_radius", fiber_radius)
    defect = defect if defect is not None else DefectNorm()

    fiber_margin = lambda_fiber - action.eps_fiber
    if fiber_margin <= 0.0:
        raise ValueError("fiber Hessian budget exhausts the coercivity margin")

    minimizer_response = action.eps_cross / fiber_margin
    centered_cross = fiber_radius * (
        action.tau_cross + action.tau_fiber * minimizer_response
    )
    transport = centered_cross / fiber_margin
    generated_good = action.eps_base + action.eps_cross**2 / fiber_margin
    defect_budget = defect.effective_hessian_budget
    generated_full = generated_good + defect_budget
    base_margin = lambda_base - generated_full

    return OneStepCertificate(
        lambda_fiber=lambda_fiber,
        lambda_base=lambda_base,
        fiber_radius=fiber_radius,
        fiber_margin=fiber_margin,
        minimizer_response_bound=minimizer_response,
        centered_cross_budget=centered_cross,
        centered_transport_coefficient=transport,
        generated_good_hessian_budget=generated_good,
        defect_hessian_budget=defect_budget,
        generated_full_hessian_budget=generated_full,
        generated_base_margin=base_margin,
        fiber_contraction_certified=transport < 1.0,
        generated_base_coercive=base_margin > 0.0,
    )


def _symmetric_matrix(name: str, value: np.ndarray) -> np.ndarray:
    matrix = np.asarray(value, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"{name} must be square")
    if not np.all(np.isfinite(matrix)):
        raise ValueError(f"{name} must be finite")
    if not np.allclose(matrix, matrix.T, atol=1e-12, rtol=1e-12):
        raise ValueError(f"{name} must be symmetric")
    return matrix


def gaussian_effective_hessian(
    base_hessian: np.ndarray,
    cross_hessian: np.ndarray,
    fiber_hessian: np.ndarray,
) -> np.ndarray:
    """Return the exact Schur-complement Hessian after Gaussian integration."""

    base = _symmetric_matrix("base_hessian", base_hessian)
    fiber = _symmetric_matrix("fiber_hessian", fiber_hessian)
    cross = np.asarray(cross_hessian, dtype=float)
    if cross.shape != (base.shape[0], fiber.shape[0]):
        raise ValueError("cross_hessian has incompatible dimensions")
    if not np.all(np.isfinite(cross)):
        raise ValueError("cross_hessian must be finite")
    if float(np.linalg.eigvalsh(fiber)[0]) <= 0.0:
        raise ValueError("fiber_hessian must be positive definite")
    return base - cross @ np.linalg.solve(fiber, cross.T)


def gaussian_conditional_data(
    cross_hessian: np.ndarray,
    fiber_hessian: np.ndarray,
    heat_time: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return conditional-mean map and centered covariance for a Gaussian."""

    heat_time = _finite_positive("heat_time", heat_time)
    fiber = _symmetric_matrix("fiber_hessian", fiber_hessian)
    cross = np.asarray(cross_hessian, dtype=float)
    if cross.ndim != 2 or cross.shape[1] != fiber.shape[0]:
        raise ValueError("cross_hessian has incompatible dimensions")
    if not np.all(np.isfinite(cross)):
        raise ValueError("cross_hessian must be finite")
    if float(np.linalg.eigvalsh(fiber)[0]) <= 0.0:
        raise ValueError("fiber_hessian must be positive definite")
    mean_map = -np.linalg.solve(fiber, cross.T)
    covariance = heat_time * np.linalg.inv(fiber)
    return mean_map, covariance


def orthogonal_transform_blocks(
    base_hessian: np.ndarray,
    cross_hessian: np.ndarray,
    fiber_hessian: np.ndarray,
    base_frame: np.ndarray,
    fiber_frame: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Change orthonormal retained/fiber frames for covariance tests."""

    base = _symmetric_matrix("base_hessian", base_hessian)
    fiber = _symmetric_matrix("fiber_hessian", fiber_hessian)
    cross = np.asarray(cross_hessian, dtype=float)
    qb = np.asarray(base_frame, dtype=float)
    qf = np.asarray(fiber_frame, dtype=float)
    if cross.shape != (base.shape[0], fiber.shape[0]):
        raise ValueError("cross_hessian has incompatible dimensions")
    if qb.shape != base.shape or qf.shape != fiber.shape:
        raise ValueError("orthogonal frames have incompatible dimensions")
    if not np.allclose(qb.T @ qb, np.eye(qb.shape[0]), atol=1e-10):
        raise ValueError("base_frame must be orthogonal")
    if not np.allclose(qf.T @ qf, np.eye(qf.shape[0]), atol=1e-10):
        raise ValueError("fiber_frame must be orthogonal")
    return qb.T @ base @ qb, qb.T @ cross @ qf, qf.T @ fiber @ qf


def calibration() -> dict[str, Any]:
    """Produce the deterministic calibration shipped with the theorem dossier."""

    examples = []
    inputs = [
        (
            "small",
            LocalActionNorm(0.25, 0.20, 0.10, 0.30, 0.20),
            DefectNorm(0.01, 0.02, 0.03),
            0.50,
        ),
        (
            "moderate",
            LocalActionNorm(0.50, 0.40, 0.20, 0.50, 0.40),
            DefectNorm(0.04, 0.05, 0.08),
            0.50,
        ),
        (
            "near_fiber_margin",
            LocalActionNorm(1.50, 0.40, 0.20, 0.50, 0.50),
            DefectNorm(0.10, 0.10, 0.15),
            0.20,
        ),
    ]
    for label, action, defect, radius in inputs:
        certificate = one_step_certificate(2.0, 1.0, radius, action, defect)
        examples.append(
            {
                "label": label,
                "action_norm": asdict(action),
                "defect_norm": asdict(defect),
                "certificate": certificate.to_dict(),
            }
        )

    base_reference = np.diag([1.0, 1.5, 2.0])
    base_perturbation = np.diag([0.10, -0.05, 0.02])
    fiber_reference = np.diag([2.0, 3.0, 4.0, 5.0])
    fiber_perturbation = np.diag([-0.20, 0.10, -0.05, 0.15])
    cross = np.array(
        [
            [0.10, -0.04, 0.00, 0.03],
            [0.02, 0.08, -0.05, 0.00],
            [-0.03, 0.00, 0.06, 0.04],
        ]
    )
    fiber = fiber_reference + fiber_perturbation
    base = base_reference + base_perturbation
    effective = gaussian_effective_hessian(base, cross, fiber)
    actual_remainder = float(np.linalg.norm(effective - base_reference, 2))
    eps_fiber = float(np.linalg.norm(fiber_perturbation, 2))
    eps_cross = float(np.linalg.norm(cross, 2))
    eps_base = float(np.linalg.norm(base_perturbation, 2))
    theorem_bound = eps_base + eps_cross**2 / (2.0 - eps_fiber)

    return {
        "scope": (
            "exact finite-dimensional marginalization theorem for declared local "
            "derivative and defect norms; not a proof that the four-dimensional "
            "Yang--Mills RG trajectory satisfies those norms"
        ),
        "input_from_stage_05": {
            "certified_fiber_lower_bound": 2.0,
            "su2_retained_dimension": 51,
            "su2_fiber_dimension": 357,
        },
        "certificate_examples": examples,
        "gaussian_witness": {
            "base_dimension": 3,
            "fiber_dimension": 4,
            "eps_fiber": eps_fiber,
            "eps_cross": eps_cross,
            "eps_base": eps_base,
            "actual_generated_remainder_norm": actual_remainder,
            "theorem_upper_bound": theorem_bound,
            "bound_respected": actual_remainder <= theorem_bound + 1e-12,
            "effective_hessian_eigenvalues": np.linalg.eigvalsh(effective).tolist(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
