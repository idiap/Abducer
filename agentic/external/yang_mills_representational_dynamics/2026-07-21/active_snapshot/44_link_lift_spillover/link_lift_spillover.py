"""Exact linear link-lift spillover for a centered plaquette-star repair."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np

PACKAGE = Path(__file__).resolve().parents[1]
for sibling in (
    "08_su2_nonlinear_block_geometry",
    "23_local_cylinder_comparison",
    "41_nonlinear_dispersion_geometry",
    "43_centered_star_repair",
):
    path = PACKAGE / sibling
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from su2_nonlinear_block_geometry import build_block_complex  # noqa: E402
from local_cylinder_comparison import calibration as comparison_calibration  # noqa: E402
from nonlinear_dispersion_geometry import metric_factor  # noqa: E402
from centered_star_repair import calibration as repair_calibration  # noqa: E402


@dataclass(frozen=True)
class SpilloverCertificate:
    interior_links: int
    selected_plaquettes: int
    centered_scalar_dimension: int
    centered_constraint_rank: int
    zero_spill_modes: int
    minimum_spill_eigenvalues: tuple[float, ...]
    maximum_spill_coefficient: float
    spectra_equal_for_all_interior_links: bool
    central_link_excluded_from_lift: bool
    exact_external_minimization: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def centered_basis(size: int) -> np.ndarray:
    m = int(size)
    if m < 2:
        raise ValueError("size must be at least two")
    seed = np.vstack((np.eye(m - 1), -np.ones(m - 1)))
    q, _ = np.linalg.qr(seed)
    return q


def _minimum_spill_spectrum(link: int) -> tuple[float, ...]:
    block = build_block_complex()
    d1 = block.d1
    selected = np.flatnonzero(np.abs(d1[:, link]) > 0.0)
    if len(selected) != 6:
        raise ValueError("link must have six incident plaquettes")
    external = np.setdiff1d(np.arange(d1.shape[0]), selected)
    columns = np.setdiff1d(np.arange(d1.shape[1]), [link])
    q = centered_basis(6)
    center = np.eye(6) - np.ones((6, 6)) / 6.0
    a = q.T @ center @ d1[np.ix_(selected, columns)]
    b = d1[np.ix_(external, columns)]
    if np.linalg.matrix_rank(a, tol=1e-10) != 5:
        raise ArithmeticError("centered star constraints lost rank")
    lift0 = a.T @ np.linalg.inv(a @ a.T)
    _, singular, vh = np.linalg.svd(a, full_matrices=True)
    rank = int(np.sum(singular > 1e-10))
    null = vh[rank:].T
    bnull = b @ null
    residual = b @ lift0 - bnull @ np.linalg.pinv(bnull, rcond=1e-12) @ (b @ lift0)
    values = np.linalg.eigvalsh(residual.T @ residual)
    return tuple(round(max(0.0, float(value)), 12) for value in values)


@lru_cache(maxsize=1)
def spillover_certificate() -> SpilloverCertificate:
    block = build_block_complex()
    degrees = np.sum(np.abs(block.d1) > 0.0, axis=0)
    links = tuple(int(i) for i in np.flatnonzero(degrees == 6))
    spectra = tuple(_minimum_spill_spectrum(link) for link in links)
    reference = spectra[0]
    equal = all(max(abs(a - b) for a, b in zip(reference, spectrum)) < 1e-9 for spectrum in spectra)
    return SpilloverCertificate(
        interior_links=len(links),
        selected_plaquettes=6,
        centered_scalar_dimension=5,
        centered_constraint_rank=5,
        zero_spill_modes=sum(value < 1e-10 for value in reference),
        minimum_spill_eigenvalues=reference,
        maximum_spill_coefficient=max(reference),
        spectra_equal_for_all_interior_links=equal,
        central_link_excluded_from_lift=True,
        exact_external_minimization=True,
    )


def lifted_free_energy(
    spill_coefficient: float,
    action_drop: float,
    contraction: float,
    base_bad_action: float,
    log_jacobian_loss: float,
    haar_loss: float,
    comparison_loss: float,
) -> float:
    lam = float(spill_coefficient)
    if min(lam, action_drop, base_bad_action, log_jacobian_loss, haar_loss, comparison_loss) < 0.0:
        raise ValueError("all losses and actions must be nonnegative")
    if not 0.0 < contraction < 1.0:
        raise ValueError("invalid contraction")
    spill = (1.0 - contraction) ** 2 * lam * base_bad_action
    return action_drop - spill - log_jacobian_loss - haar_loss - comparison_loss


def calibration() -> dict[str, Any]:
    repair = repair_calibration()["certificate"]
    spill = spillover_certificate()
    comparison = comparison_calibration()["comparison"]
    m = repair["staples"]
    eta = repair["bad_rms_threshold"]
    t = repair["heat_time"]
    base = m * eta * eta / (2.0 * t)
    staple_radius = repair["chart_maximum_rms"] / 2.0
    haar_loss = -2.0 * m * math.log(metric_factor(staple_radius))
    local_loss = m * comparison["log_loss_per_support"]
    free = lifted_free_energy(
        spill.maximum_spill_coefficient,
        repair["minimum_action_drop"],
        repair["contraction"],
        base,
        repair["log_jacobian_loss"],
        haar_loss,
        local_loss,
    )
    target = 7.62918774229502
    numerator = repair["minimum_action_drop"] - repair["log_jacobian_loss"] - haar_loss - local_loss - target
    admissible = max(0.0, numerator / ((1.0 - repair["contraction"]) ** 2 * base))
    return {
        "claim_level": "C2 exact linearized block lift and repair obstruction",
        "spillover": spill.to_dict(),
        "repair_accounting": {
            "base_bad_action": base,
            "haar_log_loss": haar_loss,
            "comparison_log_loss": local_loss,
            "lifted_worst_mode_free_energy": free,
            "required_free_energy": target,
            "maximum_admissible_spill_coefficient": admissible,
            "actual_to_admissible_ratio": spill.maximum_spill_coefficient / admissible,
            "single_star_link_lift_closes": free > target,
        },
        "favorable_zero_external_curvature_assumed": True,
        "generic_single_star_repair_falsified": True,
        "coordinated_polymer_repair_proved": False,
    }


def main() -> None:
    argparse.ArgumentParser().parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
