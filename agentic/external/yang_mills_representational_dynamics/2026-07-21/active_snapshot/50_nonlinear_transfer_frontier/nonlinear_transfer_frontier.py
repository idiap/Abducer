"""Composite conservative audit of Stages 41--49."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any

PACKAGE = Path(__file__).resolve().parents[1]
MODULES = (
    ("41_nonlinear_dispersion_geometry", "nonlinear_dispersion_geometry"),
    ("42_dispersion_tail_transfer", "dispersion_tail_transfer"),
    ("43_centered_star_repair", "centered_star_repair"),
    ("44_link_lift_spillover", "link_lift_spillover"),
    ("45_coordinated_repair_frontier", "coordinated_repair_frontier"),
    ("46_history_uniform_dispersion_comparison", "history_uniform_dispersion_comparison"),
    ("47_center_flux_sector_barriers", "center_flux_sector_barriers"),
    ("48_integer_topology_carrier", "integer_topology_carrier"),
    ("49_updated_multichannel_budget", "updated_multichannel_budget"),
)
for directory, _ in MODULES:
    path = PACKAGE / directory
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import nonlinear_dispersion_geometry as s41  # noqa: E402
import dispersion_tail_transfer as s42  # noqa: E402
import centered_star_repair as s43  # noqa: E402
import link_lift_spillover as s44  # noqa: E402
import coordinated_repair_frontier as s45  # noqa: E402
import history_uniform_dispersion_comparison as s46  # noqa: E402
import center_flux_sector_barriers as s47  # noqa: E402
import integer_topology_carrier as s48  # noqa: E402
import updated_multichannel_budget as s49  # noqa: E402


@dataclass(frozen=True)
class FrontierCertificate:
    stages_composed: int
    nonlinear_variance_geometry_proved: bool
    normalized_tail_transfer_theorem_proved: bool
    restricted_continuous_channel_closed: bool
    physical_boundary_uniform_transfer_proved: bool
    ideal_tangent_repair_closed: bool
    generic_single_star_link_repair_closed: bool
    coordinated_repair_criterion_proved: bool
    physical_coordinated_repair_constructed: bool
    adaptive_history_implication_proved: bool
    physical_history_table_proved: bool
    center_sector_minimum_barriers_proved: bool
    center_sector_partition_ratios_proved: bool
    integer_topology_carrier_required: bool
    complete_nonabelian_topology_controlled: bool
    physical_multichannel_ratio_proved: bool
    one_scale_basin_entry_proved: bool
    continuum_mass_gap_proved: bool
    claim_level: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@lru_cache(maxsize=1)
def calibration() -> dict[str, Any]:
    a41 = s41.calibration()
    a42 = s42.calibration()
    a43 = s43.calibration()
    a44 = s44.calibration()
    a45 = s45.calibration()
    a46 = s46.calibration()
    a47 = s47.calibration()
    a48 = s48.calibration()
    a49 = s49.calibration()
    frontier = FrontierCertificate(
        stages_composed=10,
        nonlinear_variance_geometry_proved=a41["variance_proxy_theorem"]["lower_bound_verified"],
        normalized_tail_transfer_theorem_proved=a42["certificate"]["normalized_transfer_theorem_proved"],
        restricted_continuous_channel_closed=a42["restricted_centered_reference_high_channel_closed"] and a46["history_certificate"]["numerical_table_closes"],
        physical_boundary_uniform_transfer_proved=a42["certificate"]["complete_nonlinear_transfer_proved"],
        ideal_tangent_repair_closed=a43["ideal_tangent_star_repair_closes"],
        generic_single_star_link_repair_closed=not a44["generic_single_star_repair_falsified"],
        coordinated_repair_criterion_proved=a45["coordinated_polymer_sufficient_condition_proved"],
        physical_coordinated_repair_constructed=a45["physical_coordinated_repair_constructed"],
        adaptive_history_implication_proved=a46["history_certificate"]["adaptive_domination_implication_available"],
        physical_history_table_proved=a46["physical_positive_mass_history_table_proved"],
        center_sector_minimum_barriers_proved=a47["certificate"]["minimum_barrier_formula_proved"],
        center_sector_partition_ratios_proved=a47["certificate"]["complete_sector_partition_ratio_proved"],
        integer_topology_carrier_required=a48["retained_schema_requires_integer_flux_lift"],
        complete_nonabelian_topology_controlled=a48["complete_nonabelian_su2_second_chern_control_proved"],
        physical_multichannel_ratio_proved=a49["complete_physical_multichannel_ratio_proved"],
        one_scale_basin_entry_proved=False,
        continuum_mass_gap_proved=False,
        claim_level="C2 exact/conditional finite theorems and restricted nonlinear-reference closure",
    )
    transfer = a42["certificate"]
    remedy = a45
    allocation = a49["allocation"]
    return {
        "frontier": frontier.to_dict(),
        "strongest_positive_result": "the nonlinear dispersion event is transported by an exact normalized theorem and closes in the centered retained reference",
        "restricted_continuous_probability_upper": a46["history_certificate"]["numerical_maximum_row"],
        "first_open_physical_comparison": (
            "uniformly over every finite volume and positive-mass retained history h, prove "
            "mu_h(A intersect G_h) <= exp(ell_h) nu_h(A intersect G_h) and mu_h(G_h^c) <= q_exc,h "
            "with q_low,h + exp(ell_h) q_gauss,h + q_exc,h <= 0.0009721110007367992"
        ),
        "repair_route_obstruction": {
            "actual_single_star_spill": a44["spillover"]["maximum_spill_coefficient"],
            "maximum_admissible_spill_at_upper_split": remedy["maximum_admissible_spill_at_upper_split"],
            "generic_single_star_repair_falsified": a44["generic_single_star_repair_falsified"],
        },
        "remaining_open_channel_budget": allocation["residual_budget"],
        "equal_open_channel_free_energy": allocation["required_free_energies"][0],
        "ranked_next_targets": [
            "prove the boundary-uniform normalized density and chart-complement comparison",
            "construct a coordinated polymer repair only as an independent backup route",
            "convert center minimum barriers into full sector partition-ratio bounds",
            "bound the cut/orbit channel on a complete retained atlas",
            "construct nonabelian integer topology and uniform sector weights",
            "only then claim physical one-scale basin entry and attempt repeated RG",
        ],
        "not_proved": [
            "physical nonlinear continuous-channel bound",
            "complete multichannel one-scale ratio",
            "volume-uniform basin entry",
            "repeated gauge-covariant RG",
            "continuum Yang-Mills construction",
            "Hamiltonian mass gap",
        ],
        "reference_transfer_components": {
            "comparison_log_loss": transfer["comparison_log_loss"],
            "chart_complement_upper": transfer["chart_complement_upper"],
            "reference_tail_upper": transfer["reference_tail_upper"],
        },
    }


def main() -> None:
    argparse.ArgumentParser().parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
