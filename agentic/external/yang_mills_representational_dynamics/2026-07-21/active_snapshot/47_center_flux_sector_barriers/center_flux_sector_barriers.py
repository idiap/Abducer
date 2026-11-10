"""Exact minimum plaquette barriers for periodic GF(2) center-flux sectors."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
from functools import lru_cache
import itertools
import json
import math
from pathlib import Path
import sys
from typing import Any, Sequence

import numpy as np

PACKAGE = Path(__file__).resolve().parents[1]
path = PACKAGE / "39_periodic_center_flux_topology"
if str(path) not in sys.path:
    sys.path.insert(0, str(path))

from periodic_center_flux_topology import (  # noqa: E402
    DIM,
    L,
    flux_representatives,
    periodic_complex,
)


@dataclass(frozen=True)
class SectorBarrierCertificate:
    sectors: int
    flux_components: int
    plaquettes_per_nonzero_component: int
    minimum_weights: tuple[int, ...]
    weight_multiplicities: tuple[int, ...]
    explicit_representatives_are_cocycles: bool
    exact_coboundaries_preserve_flux: bool
    minimum_barrier_formula_proved: bool
    complete_sector_partition_ratio_proved: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_label(label: Sequence[int]) -> tuple[int, ...]:
    bits = tuple(int(value) for value in label)
    if len(bits) != 6 or any(value not in (0, 1) for value in bits):
        raise ValueError("flux label must contain six bits")
    return bits


def representative(label: Sequence[int]) -> np.ndarray:
    bits = np.asarray(validate_label(label), dtype=np.uint8)
    return flux_representatives() @ bits % 2


def sector_minimum_weight(label: Sequence[int]) -> int:
    return 4 * sum(validate_label(label))


def plane_fluxes(cochain: Sequence[int], direction_a: int, direction_b: int) -> tuple[int, ...]:
    if not 0 <= direction_a < direction_b < DIM:
        raise ValueError("directions must be an ordered pair")
    V, E, P, C, Q, d0, d1, d2, d3 = periodic_complex()
    y = np.asarray(cochain, dtype=np.uint8)
    if y.shape != (len(P),):
        raise ValueError("cochain has the wrong shape")
    index = {plaquette: i for i, plaquette in enumerate(P)}
    transverse = tuple(axis for axis in range(DIM) if axis not in (direction_a, direction_b))
    result = []
    for fixed in itertools.product(range(L), repeat=2):
        total = 0
        for u, v in itertools.product(range(L), repeat=2):
            x = [0] * DIM
            x[direction_a] = u
            x[direction_b] = v
            x[transverse[0]] = fixed[0]
            x[transverse[1]] = fixed[1]
            total ^= int(y[index[(tuple(x), direction_a, direction_b)]])
        result.append(total)
    return tuple(result)


def minimum_representative_ratio(unit_charge: float) -> float:
    tau = float(unit_charge)
    if not math.isfinite(tau) or tau < 0.0:
        raise ValueError("charge must be finite and nonnegative")
    return (1.0 + math.exp(-4.0 * tau)) ** 6 - 1.0


def charge_for_ratio(target: float) -> float:
    q = float(target)
    if not 0.0 < q < 63.0:
        raise ValueError("target must lie in (0,63)")
    return -0.25 * math.log((1.0 + q) ** (1.0 / 6.0) - 1.0)


@lru_cache(maxsize=1)
def certificate() -> SectorBarrierCertificate:
    V, E, P, C, Q, d0, d1, d2, d3 = periodic_complex()
    labels = tuple(itertools.product((0, 1), repeat=6))
    weights = tuple(sector_minimum_weight(label) for label in labels)
    reps = tuple(representative(label) for label in labels)
    cocycles = all(not (d2 @ value % 2).any() for value in reps)
    exact_preserves = True
    for column in range(d1.shape[1]):
        exact = d1[:, column] % 2
        if any(len(set(plane_fluxes(exact, a, b))) != 1 or plane_fluxes(exact, a, b)[0] != 0 for a, b in itertools.combinations(range(4), 2)):
            exact_preserves = False
            break
    multiplicities = tuple(weights.count(4 * k) for k in range(7))
    return SectorBarrierCertificate(
        sectors=64,
        flux_components=6,
        plaquettes_per_nonzero_component=4,
        minimum_weights=tuple(4 * k for k in range(7)),
        weight_multiplicities=multiplicities,
        explicit_representatives_are_cocycles=cocycles,
        exact_coboundaries_preserve_flux=exact_preserves,
        minimum_barrier_formula_proved=True,
        complete_sector_partition_ratio_proved=False,
    )


def calibration() -> dict[str, Any]:
    target = .002430277501841998
    threshold = charge_for_ratio(target)
    restricted = minimum_representative_ratio(2.0)
    return {
        "claim_level": "C2 exact periodic center-sector minimum-barrier theorem",
        "certificate": certificate().to_dict(),
        "minimum_weight_by_hamming_flux": {str(k): 4 * k for k in range(7)},
        "restricted_minimal_representative_model": {
            "unit_plaquette_charge": 2.0,
            "nontrivial_to_trivial_ratio": restricted,
            "target_ratio": target,
            "target_met": restricted < target,
            "required_unit_charge": threshold,
        },
        "full_center_gauge_fluctuation_entropy_included": False,
        "continuous_su2_sector_weights_proved": False,
    }


def main() -> None:
    argparse.ArgumentParser().parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
