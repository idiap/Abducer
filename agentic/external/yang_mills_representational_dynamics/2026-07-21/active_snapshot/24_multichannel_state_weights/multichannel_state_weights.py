"""Exact Lyapunov weights for a multichannel star bad subkernel.

State zero is the regular retained-boundary channel.  A bad extension can
enter one of several charged channels; the next bad extension can return to
the regular state or persist in that channel.  The exact diagonal-weight
feasibility inequality identifies how rare entry and persistence must trade.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from typing import Sequence

import numpy as np


CHANNELS = ("center", "continuous", "cut_orbit", "topology")


@dataclass(frozen=True)
class StarWeightCertificate:
    channels: int
    target_ceiling: float
    root_weighted_row: float
    maximum_defect_weighted_row: float
    weighted_ceiling: float
    scalar_row_ceiling: float
    minimum_weight: float
    maximum_weight: float
    feasible: bool
    strict_subcritical: bool

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


def _vector(name: str, values: Sequence[float], length: int | None = None) -> np.ndarray:
    result = np.asarray(values, dtype=float)
    if result.ndim != 1 or result.size == 0:
        raise ValueError(f"{name} must be a nonempty vector")
    if length is not None and result.size != length:
        raise ValueError(f"{name} has the wrong length")
    if not np.all(np.isfinite(result)) or np.any(result < 0.0):
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def star_bad_kernel(
    entry_rates: Sequence[float],
    forced_returns: Sequence[float],
    persistence: Sequence[float],
) -> np.ndarray:
    entry = _vector("entry_rates", entry_rates)
    returns = _vector("forced_returns", forced_returns, entry.size)
    persist = _vector("persistence", persistence, entry.size)
    if float(np.sum(entry)) > 1.0 + 1.0e-14:
        raise ValueError("root bad mass must not exceed one")
    if np.any(returns + persist > 1.0 + 1.0e-14):
        raise ValueError("defect bad-row mass must not exceed one")
    matrix = np.zeros((entry.size + 1, entry.size + 1))
    matrix[0, 1:] = entry
    for index, (back, stay) in enumerate(zip(returns, persist), start=1):
        matrix[index, 0] = back
        matrix[index, index] = stay
    return matrix


def canonical_star_weight(
    target_ceiling: float,
    forced_returns: Sequence[float],
    persistence: Sequence[float],
) -> np.ndarray:
    q = float(target_ceiling)
    returns = _vector("forced_returns", forced_returns)
    persist = _vector("persistence", persistence, returns.size)
    if not math.isfinite(q) or not 0.0 < q < 1.0:
        raise ValueError("target_ceiling must lie in (0,1)")
    if np.any(persist >= q):
        raise ValueError("every persistence rate must be strictly below q")
    defect = returns / (q - persist)
    if np.any(defect < 1.0):
        raise ValueError("canonical charged weights must be at least one")
    return np.concatenate(([1.0], defect))


def star_feasibility_expression(
    target_ceiling: float,
    entry_rates: Sequence[float],
    forced_returns: Sequence[float],
    persistence: Sequence[float],
) -> float:
    entry = _vector("entry_rates", entry_rates)
    weight = canonical_star_weight(target_ceiling, forced_returns, persistence)
    if entry.size + 1 != weight.size:
        raise ValueError("channel vectors must have equal length")
    return float(np.dot(entry, weight[1:]))


def star_weight_certificate(
    target_ceiling: float,
    entry_rates: Sequence[float],
    forced_returns: Sequence[float],
    persistence: Sequence[float],
    critical_ceiling: float,
) -> tuple[np.ndarray, np.ndarray, StarWeightCertificate]:
    q = float(target_ceiling)
    qcrit = float(critical_ceiling)
    matrix = star_bad_kernel(entry_rates, forced_returns, persistence)
    weight = canonical_star_weight(q, forced_returns, persistence)
    ratios = (matrix @ weight) / weight
    root = float(ratios[0])
    defect = float(np.max(ratios[1:]))
    ceiling = float(np.max(ratios))
    cert = StarWeightCertificate(
        channels=matrix.shape[0] - 1,
        target_ceiling=q,
        root_weighted_row=root,
        maximum_defect_weighted_row=defect,
        weighted_ceiling=ceiling,
        scalar_row_ceiling=float(np.max(np.sum(matrix, axis=1))),
        minimum_weight=float(np.min(weight)),
        maximum_weight=float(np.max(weight)),
        feasible=ceiling <= q + 1.0e-14,
        strict_subcritical=ceiling < qcrit,
    )
    return matrix, weight, cert


def minimal_star_ceiling(
    entry_rates: Sequence[float],
    forced_returns: Sequence[float],
    persistence: Sequence[float],
) -> float:
    entry = _vector("entry_rates", entry_rates)
    returns = _vector("forced_returns", forced_returns, entry.size)
    persist = _vector("persistence", persistence, entry.size)
    low = float(np.max(persist))
    if np.any(returns < 1.0 - persist):
        # This routine keeps the canonical V>=1 branch used in the theorem.
        raise ValueError("minimal solver requires return+persistence at least one")
    high = 1.0
    def f(q: float) -> float:
        return float(np.sum(entry * returns / (q - persist)) - q)
    if f(high) > 1.0e-14:
        raise ValueError("no subunit weighted ceiling exists")
    for _ in range(120):
        middle = 0.5 * (low + high)
        if f(middle) > 0.0:
            low = middle
        else:
            high = middle
    return high


def calibration() -> dict[str, object]:
    q = 0.002430277501841998
    qcrit = 0.0027927080803578997
    channel_count = len(CHANNELS)
    total_entry_budget = q * q
    entries = np.full(channel_count, total_entry_budget / channel_count)
    returns = np.ones(channel_count)
    persistence = np.zeros(channel_count)
    matrix, weight, cert = star_weight_certificate(
        q, entries, returns, persistence, qcrit
    )
    minimum = minimal_star_ceiling(entries, returns, persistence)
    return {
        "claim_level": "C2 exact multichannel star-weight theorem plus finite calibration",
        "channels": list(CHANNELS),
        "target_weighted_ceiling": q,
        "critical_weighted_ceiling": qcrit,
        "total_entry_budget": total_entry_budget,
        "equal_entry_budget_per_channel": float(entries[0]),
        "total_entry_free_energy": -math.log(total_entry_budget),
        "per_channel_entry_free_energy": -math.log(float(entries[0])),
        "kernel": matrix.tolist(),
        "weight": weight.tolist(),
        "certificate": cert.to_dict(),
        "minimal_weighted_ceiling": minimum,
        "persistence_must_be_below_target": True,
        "retained_center_and_orbit_labels_available": True,
        "topology_label_available_on_current_local_block": False,
        "physical_su2_entry_rates_proved": False,
        "first_unproved_implication": (
            "bound the four physical channel entry numerators and persistence "
            "rates uniformly over retained boundary states"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
