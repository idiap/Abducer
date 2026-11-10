"""Exact conditional partition-ratio reduction for the nonlinear frontier.

For each retained boundary state s, split the compact fiber into good and bad
parts.  The bad weighted row of the conditional kernel is exactly the bad
weighted partition numerator divided by the full normalizer and V(s).  A
uniform free-energy inequality relative to the good reference partition
therefore suffices for the Stage 19 weighted ceiling.  This module proves the
reduction, exhibits entropy and boundary-state counterexamples, and records
the precise SU(2) inequality that remains open.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import sys
from typing import Sequence

import numpy as np


PACKAGE = Path(__file__).resolve().parents[1]
stage25 = PACKAGE / "25_one_scale_kr_composition"
if str(stage25) not in sys.path:
    sys.path.insert(0, str(stage25))

from one_scale_kr_composition import calibration as kr_calibration  # noqa: E402


@dataclass(frozen=True)
class PartitionRatioCertificate:
    retained_states: int
    maximum_exact_weighted_bad_ratio: float
    target_ceiling: float
    target_met: bool
    full_normalizer_used: bool
    zero_mass_state_excluded: bool

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


@dataclass(frozen=True)
class FreeEnergyCertificate:
    good_comparison_loss: float
    charged_free_energy: float
    implied_weighted_ceiling: float
    target_ceiling: float
    required_free_energy: float
    strict_target_met: bool

    def to_dict(self) -> dict[str, float | bool]:
        return asdict(self)


def exact_weighted_bad_ratios(
    good_partition: Sequence[float],
    bad_partition: Sequence[float],
    bad_weighted_numerator: Sequence[float],
    current_weight: Sequence[float],
) -> np.ndarray:
    zg = np.asarray(good_partition, dtype=float)
    zb = np.asarray(bad_partition, dtype=float)
    bv = np.asarray(bad_weighted_numerator, dtype=float)
    v = np.asarray(current_weight, dtype=float)
    if zg.ndim != 1 or zg.size == 0 or any(x.shape != zg.shape for x in (zb, bv, v)):
        raise ValueError("all partition vectors must be matching and nonempty")
    if not all(np.all(np.isfinite(x)) for x in (zg, zb, bv, v)):
        raise ValueError("partition data must be finite")
    if np.any(zg < 0.0) or np.any(zb < 0.0) or np.any(bv < 0.0) or np.any(v <= 0.0):
        raise ValueError("partition data must be nonnegative and weights positive")
    normalizer = zg + zb
    if np.any(normalizer <= 0.0):
        raise ValueError("every retained state must have positive conditional mass")
    return bv / (normalizer * v)


def partition_ratio_certificate(
    good_partition: Sequence[float],
    bad_partition: Sequence[float],
    bad_weighted_numerator: Sequence[float],
    current_weight: Sequence[float],
    target_ceiling: float,
) -> PartitionRatioCertificate:
    target = float(target_ceiling)
    if not math.isfinite(target) or not 0.0 < target < 1.0:
        raise ValueError("target_ceiling must lie in (0,1)")
    ratios = exact_weighted_bad_ratios(
        good_partition, bad_partition, bad_weighted_numerator, current_weight
    )
    maximum = float(np.max(ratios))
    return PartitionRatioCertificate(
        retained_states=ratios.size,
        maximum_exact_weighted_bad_ratio=maximum,
        target_ceiling=target,
        target_met=maximum <= target,
        full_normalizer_used=True,
        zero_mass_state_excluded=True,
    )


def free_energy_certificate(
    good_comparison_loss: float,
    charged_free_energy: float,
    target_ceiling: float,
) -> FreeEnergyCertificate:
    ell = float(good_comparison_loss)
    charge = float(charged_free_energy)
    target = float(target_ceiling)
    if not math.isfinite(ell) or ell < 0.0:
        raise ValueError("comparison loss must be finite and nonnegative")
    if not math.isfinite(charge) or charge < 0.0:
        raise ValueError("charged free energy must be finite and nonnegative")
    if not math.isfinite(target) or not 0.0 < target < 1.0:
        raise ValueError("target must lie in (0,1)")
    implied = math.exp(ell - charge)
    required = ell - math.log(target)
    return FreeEnergyCertificate(
        good_comparison_loss=ell,
        charged_free_energy=charge,
        implied_weighted_ceiling=implied,
        target_ceiling=target,
        required_free_energy=required,
        strict_target_met=implied < target,
    )


def entropy_cancellation_counterexample(action_charge: float = 10.0) -> dict[str, float | int | bool]:
    charge = float(action_charge)
    if not math.isfinite(charge) or charge <= 0.0:
        raise ValueError("action_charge must be finite and positive")
    multiplicity = int(math.ceil(math.exp(charge)))
    good = 1.0
    bad = multiplicity * math.exp(-charge)
    probability = bad / (good + bad)
    return {
        "action_charge": charge,
        "bad_multiplicity": multiplicity,
        "bad_partition": bad,
        "bad_probability": probability,
        "action_charge_alone_controls_probability": False,
        "free_energy_including_entropy_required": True,
    }


def retained_state_counterexample(epsilon: float = 1.0e-9) -> dict[str, float | bool]:
    eps = float(epsilon)
    if not math.isfinite(eps) or not 0.0 < eps < 1.0:
        raise ValueError("epsilon must lie in (0,1)")
    good = [1.0, eps]
    bad = [eps, eps]
    weighted = bad
    ratios = exact_weighted_bad_ratios(good, bad, weighted, [1.0, 1.0])
    return {
        "epsilon": eps,
        "first_state_bad_ratio": float(ratios[0]),
        "second_state_bad_ratio": float(ratios[1]),
        "pointwise_good_formula_same": True,
        "boundary_uniform_normalizer_control_required": True,
    }


@lru_cache(maxsize=1)
def calibration() -> dict[str, object]:
    kr = kr_calibration()
    ell = kr["certificate"]["comparison_log_loss"]
    residual = kr["certificate"]["residual_bad_ceiling"]
    required = ell - math.log(residual)
    illustrative = free_energy_certificate(ell, required + 0.1, residual)
    exact = partition_ratio_certificate(
        [1.0, 2.0],
        [residual / 2.0, residual],
        [residual / 2.0, 2.0 * residual],
        [1.0, 2.0],
        residual,
    )
    return {
        "claim_level": "C2 exact partition-ratio reduction with open physical numerator inequality",
        "selected_local_radius": kr["selected_local_radius"],
        "residual_weighted_budget": residual,
        "required_uniform_charged_free_energy": required,
        "illustrative_strict_certificate": illustrative.to_dict(),
        "finite_exact_ratio_example": exact.to_dict(),
        "entropy_counterexample": entropy_cancellation_counterexample(),
        "retained_state_counterexample": retained_state_counterexample(),
        "finite_compact_positive_su2_conditional_kernel_exists": True,
        "uniform_physical_partition_ratio_bound_proved": False,
        "volume_uniform_one_scale_basin_entry_proved": False,
        "first_unproved_inequality": (
            "sup over finite volumes, positive-mass retained states, and defect "
            "channels of B_V(s)/(Z_G_ref(s)V(s)) <= exp(-F_*), with "
            f"F_*>{required:.12g}"
        ),
        "not_implied": [
            "repeated RG stability",
            "cutoff-uniform continuum construction",
            "Osterwalder-Schrader Hamiltonian gap",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
