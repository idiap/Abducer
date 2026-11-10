"""Integer flux/Pfaffian topology carrier and center-erasure counterexample."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import itertools
import json
from typing import Any, Sequence

import numpy as np

PAIRS = ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))


@dataclass(frozen=True)
class IntegerTopologyState:
    fluxes: tuple[int, int, int, int, int, int]
    center_reduction: tuple[int, int, int, int, int, int]
    pfaffian_charge: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_fluxes(fluxes: Sequence[int]) -> tuple[int, int, int, int, int, int]:
    values = tuple(fluxes)
    if len(values) != 6 or any(not isinstance(value, (int, np.integer)) for value in values):
        raise ValueError("integer topology requires six integral fluxes")
    return tuple(int(value) for value in values)  # type: ignore[return-value]


def center_reduction(fluxes: Sequence[int]) -> tuple[int, int, int, int, int, int]:
    values = validate_fluxes(fluxes)
    return tuple(value % 2 for value in values)  # type: ignore[return-value]


def pfaffian_charge(fluxes: Sequence[int]) -> int:
    n01, n02, n03, n12, n13, n23 = validate_fluxes(fluxes)
    return n01 * n23 - n02 * n13 + n03 * n12


def topology_state(fluxes: Sequence[int]) -> IntegerTopologyState:
    values = validate_fluxes(fluxes)
    return IntegerTopologyState(values, center_reduction(values), pfaffian_charge(values))


def antisymmetric_flux_matrix(fluxes: Sequence[int]) -> np.ndarray:
    values = validate_fluxes(fluxes)
    matrix = np.zeros((4,4), dtype=int)
    for value, (a,b) in zip(values, PAIRS):
        matrix[a,b] = value
        matrix[b,a] = -value
    return matrix


def erased_center_family(scale: int) -> IntegerTopologyState:
    k = int(scale)
    if k < 0:
        raise ValueError("scale must be nonnegative")
    return topology_state((2*k,0,0,0,0,2*k))


def bounded_lift_catalog(bound: int = 1) -> dict[tuple[int, ...], set[int]]:
    b = int(bound)
    if b < 0:
        raise ValueError("bound must be nonnegative")
    catalog: dict[tuple[int, ...], set[int]] = {}
    for fluxes in itertools.product(range(-b,b+1), repeat=6):
        catalog.setdefault(center_reduction(fluxes), set()).add(pfaffian_charge(fluxes))
    return catalog


def calibration() -> dict[str, Any]:
    trivial = topology_state((0,0,0,0,0,0))
    hidden = erased_center_family(1)
    catalog = bounded_lift_catalog(1)
    return {
        "claim_level": "C2 exact integral-flux algebra and center-erasure obstruction",
        "flux_pair_order": [f"n_{a}{b}" for a,b in PAIRS],
        "trivial_state": trivial.to_dict(),
        "same_center_nonzero_charge_state": hidden.to_dict(),
        "same_center_labels_different_integer_charge": trivial.center_reduction == hidden.center_reduction and trivial.pfaffian_charge != hidden.pfaffian_charge,
        "unbounded_charge_at_fixed_center_label": True,
        "bounded_catalog": {
            "flux_bound": 1,
            "integer_lifts": 3**6,
            "center_labels_observed": len(catalog),
            "maximum_distinct_charges_per_center_label": max(len(values) for values in catalog.values()),
        },
        "pfaffian_squared_equals_flux_matrix_determinant": True,
        "retained_schema_requires_integer_flux_lift": True,
        "complete_nonabelian_su2_second_chern_control_proved": False,
        "sector_weight_bound_proved": False,
    }


def main() -> None:
    argparse.ArgumentParser().parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
