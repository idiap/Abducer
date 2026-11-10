"""Residual multichannel budget after the nonlinear dispersion calibration."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import sys
from typing import Any, Mapping, Sequence

PACKAGE = Path(__file__).resolve().parents[1]
for sibling in (
    "44_link_lift_spillover",
    "46_history_uniform_dispersion_comparison",
    "47_center_flux_sector_barriers",
    "48_integer_topology_carrier",
):
    path = PACKAGE / sibling
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from link_lift_spillover import calibration as spill_calibration  # noqa: E402
from history_uniform_dispersion_comparison import calibration as history_calibration  # noqa: E402
from center_flux_sector_barriers import calibration as center_calibration  # noqa: E402
from integer_topology_carrier import calibration as integer_calibration  # noqa: E402

OPEN_CHANNELS = ("center", "cut_orbit", "integer_topology")


@dataclass(frozen=True)
class ResidualAllocationCertificate:
    total_target: float
    certified_restricted_contribution: float
    residual_budget: float
    open_channels: tuple[str, ...]
    shares: tuple[float, ...]
    channel_ceilings: tuple[float, ...]
    required_free_energies: tuple[float, ...]
    exact_budget_identity: bool
    restricted_continuous_premises_physical: bool
    all_open_channel_bounds_proved: bool
    physical_union_bound_proved: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def residual_allocation(
    total_target: float,
    certified_contributions: Mapping[str, float],
    open_channels: Sequence[str],
    shares: Sequence[float],
    comparison_losses: Sequence[float] | None = None,
    certified_premises_physical: bool = False,
    open_bounds_proved: bool = False,
) -> ResidualAllocationCertificate:
    target = float(total_target)
    channels = tuple(open_channels)
    fractions = tuple(float(value) for value in shares)
    losses = tuple(float(value) for value in (comparison_losses if comparison_losses is not None else [0.0] * len(channels)))
    values = tuple(float(value) for value in certified_contributions.values())
    if not 0.0 < target < 1.0 or not channels or len(channels) != len(fractions) or len(losses) != len(channels):
        raise ValueError("invalid allocation dimensions")
    if any(not math.isfinite(value) or value < 0.0 for value in values + losses) or any(value <= 0.0 for value in fractions):
        raise ValueError("allocation data must be finite and nonnegative")
    if abs(sum(fractions) - 1.0) > 1e-12:
        raise ValueError("shares must sum to one")
    used = math.fsum(values)
    residual = target - used
    if residual <= 0.0:
        raise ValueError("certified contributions exhaust the target")
    ceilings = tuple(residual * fraction for fraction in fractions)
    free = tuple(loss - math.log(ceiling) for loss, ceiling in zip(losses, ceilings))
    physical = bool(certified_premises_physical and open_bounds_proved)
    return ResidualAllocationCertificate(
        total_target=target,
        certified_restricted_contribution=used,
        residual_budget=residual,
        open_channels=channels,
        shares=fractions,
        channel_ceilings=ceilings,
        required_free_energies=free,
        exact_budget_identity=abs(used + sum(ceilings) - target) < 1e-14,
        restricted_continuous_premises_physical=bool(certified_premises_physical),
        all_open_channel_bounds_proved=bool(open_bounds_proved),
        physical_union_bound_proved=physical,
    )


@lru_cache(maxsize=1)
def calibration() -> dict[str, Any]:
    target = .002430277501841998
    continuous = history_calibration()["history_certificate"]["numerical_maximum_row"]
    allocation = residual_allocation(target, {"continuous_dispersion": continuous}, OPEN_CHANNELS, [1/3]*3)
    center = center_calibration()
    integer = integer_calibration()
    spill = spill_calibration()
    return {
        "claim_level": "C2 exact residual-budget theorem and conservative channel audit",
        "allocation": allocation.to_dict(),
        "channel_status": [
            {"channel": "continuous_dispersion", "restricted_numerical_bound": continuous, "physical_uniform_bound": False},
            {"channel": "center", "minimum_barrier_proved": center["certificate"]["minimum_barrier_formula_proved"], "physical_uniform_bound": False},
            {"channel": "cut_orbit", "atlas_only": True, "physical_uniform_bound": False},
            {"channel": "integer_topology", "carrier_required": integer["retained_schema_requires_integer_flux_lift"], "physical_uniform_bound": False},
        ],
        "single_star_repair_available_as_channel_bound": not spill["generic_single_star_repair_falsified"],
        "restricted_continuous_bound_releases_budget": True,
        "complete_physical_multichannel_ratio_proved": False,
    }


def main() -> None:
    argparse.ArgumentParser().parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
