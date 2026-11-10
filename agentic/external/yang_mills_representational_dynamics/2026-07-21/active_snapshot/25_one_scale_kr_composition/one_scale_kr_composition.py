"""One-scale positive-kernel K+R composition and budget calibration.

If a good/reference bad subkernel K0 obeys K0 V <= k V, normalized local
comparison gives K <= exp(ell) K0, and the charged residual obeys R V <= r V,
then (K+R)V <= (exp(ell)k+r)V.  This module optimizes the local-cylinder
radius so the reference and residual channels receive a declared share of the
weighted budget.  Constructing the physical K and R remains separate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import sys


PACKAGE = Path(__file__).resolve().parents[1]
for sibling in (
    "19_state_weighted_defect_transfer",
    "21_curvature_typical_set_atlas",
    "22_sharp_nonlinear_overlap",
    "23_local_cylinder_comparison",
):
    path = PACKAGE / sibling
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from state_weighted_defect_transfer import cluster_certificate  # noqa: E402
from curvature_typical_set_atlas import (  # noqa: E402
    leverage_certificate,
    local_block_union_radius,
    local_block_union_upper,
)
from sharp_nonlinear_overlap import maximal_certified_radius, sharp_overlap_certificate  # noqa: E402
from local_cylinder_comparison import local_comparison_certificate  # noqa: E402


HEAT_TIME = 3.0e-6
SUPPORT_UNITS = 216
FOUR_LINK_COVARIANCE = (
    HEAT_TIME * leverage_certificate().max_four_link_variance_coefficient
)


@dataclass(frozen=True)
class KRCompositionCertificate:
    comparison_log_loss: float
    reference_bad_ceiling: float
    comparison_corrected_reference_ceiling: float
    residual_bad_ceiling: float
    combined_weighted_ceiling: float
    target_weighted_ceiling: float
    critical_weighted_ceiling: float
    target_met: bool
    strict_cluster_subcritical: bool
    branching_ratio: float
    rooted_connected_sum_upper: float
    physical_kernel_decomposition_verified: bool

    def to_dict(self) -> dict[str, float | bool]:
        return asdict(self)


def kr_composition_certificate(
    comparison_log_loss: float,
    reference_bad_ceiling: float,
    residual_bad_ceiling: float,
    target_weighted_ceiling: float,
    critical_weighted_ceiling: float,
    degree: int = 18,
    alpha: float = 0.1,
    physical_kernel_decomposition_verified: bool = False,
) -> KRCompositionCertificate:
    ell = float(comparison_log_loss)
    k = float(reference_bad_ceiling)
    r = float(residual_bad_ceiling)
    target = float(target_weighted_ceiling)
    critical = float(critical_weighted_ceiling)
    if not math.isfinite(ell) or ell < 0.0:
        raise ValueError("comparison loss must be finite and nonnegative")
    for name, value in (("reference", k), ("residual", r)):
        if not math.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} ceiling must be finite and nonnegative")
    if not 0.0 < target < critical < 1.0:
        raise ValueError("ceilings must satisfy 0<target<critical<1")
    corrected = math.exp(ell) * k
    combined = corrected + r
    cluster = cluster_certificate(combined, degree, alpha)
    return KRCompositionCertificate(
        comparison_log_loss=ell,
        reference_bad_ceiling=k,
        comparison_corrected_reference_ceiling=corrected,
        residual_bad_ceiling=r,
        combined_weighted_ceiling=combined,
        target_weighted_ceiling=target,
        critical_weighted_ceiling=critical,
        target_met=combined <= target + 1.0e-14,
        strict_cluster_subcritical=cluster.subcritical,
        branching_ratio=cluster.branching_ratio,
        rooted_connected_sum_upper=cluster.rooted_sum_upper,
        physical_kernel_decomposition_verified=bool(physical_kernel_decomposition_verified),
    )


@lru_cache(maxsize=512)
def local_reference_budget(radius: float, support_units: int = SUPPORT_UNITS) -> tuple[float, float, float]:
    delta = local_block_union_upper(radius, support_units, 12, FOUR_LINK_COVARIANCE)
    nonlinear = sharp_overlap_certificate(radius, HEAT_TIME, 0.001)
    comparison = local_comparison_certificate(
        support_units, radius, nonlinear.total_hessian_remainder, delta
    )
    ell = comparison.log_loss_per_support
    return delta, ell, math.exp(ell) * delta


@lru_cache(maxsize=32)
def radius_for_reference_share(
    target_weighted_ceiling: float,
    reference_share: float = 0.5,
) -> float:
    target = float(target_weighted_ceiling)
    share = float(reference_share)
    if not 0.0 < target < 1.0 or not 0.0 < share < 1.0:
        raise ValueError("target and share must lie in (0,1)")
    low = local_block_union_radius(SUPPORT_UNITS, 12, FOUR_LINK_COVARIANCE, target)
    high = maximal_certified_radius(HEAT_TIME, 0.001)
    desired = share * target
    if local_reference_budget(high)[2] > desired:
        raise ValueError("the certified nonlinear window cannot meet this share")
    for _ in range(100):
        middle = 0.5 * (low + high)
        if local_reference_budget(middle)[2] > desired:
            low = middle
        else:
            high = middle
    return high


@lru_cache(maxsize=1)
def calibration() -> dict[str, object]:
    target = 0.002430277501841998
    critical = 0.0027927080803578997
    share = 0.5
    radius = radius_for_reference_share(target, share)
    delta, ell, corrected = local_reference_budget(radius)
    residual = target - corrected
    cert = kr_composition_certificate(
        ell,
        delta,
        residual,
        target,
        critical,
        physical_kernel_decomposition_verified=False,
    )
    sharp_max = maximal_certified_radius()
    return {
        "claim_level": "C2 positive-kernel K+R theorem plus C1 feasible-radius calibration",
        "selected_local_radius": radius,
        "maximum_nonlinear_radius": sharp_max,
        "radius_fraction_of_nonlinear_window": radius / sharp_max,
        "reference_budget_share": share,
        "certificate": cert.to_dict(),
        "residual_free_energy_required": -math.log(residual),
        "four_channel_alternating_total_entry_budget": residual * residual,
        "four_channel_equal_entry_budget": residual * residual / 4.0,
        "four_channel_equal_entry_free_energy": -math.log(residual * residual / 4.0),
        "nonempty_feasible_budget_region": residual > 0.0,
        "full_su2_k_plus_r_inequality_proved": False,
        "first_unproved_implication": (
            "realize the abstract K and R as the complete nonlinear SU(2) conditional "
            "subkernels and prove the residual weighted numerator bound"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
