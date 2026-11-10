"""Retained-history interface for nonlinear low/high dispersion comparison."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any, Mapping, Sequence

PACKAGE = Path(__file__).resolve().parents[1]
for sibling in (
    "32_dispersion_conditional_optimizer",
    "36_adaptive_dispersion_filtration",
    "42_dispersion_tail_transfer",
):
    path = PACKAGE / sibling
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from dispersion_conditional_optimizer import certificate as low_certificate  # noqa: E402
from adaptive_dispersion_filtration import adaptive_certificate  # noqa: E402
from dispersion_tail_transfer import calibration as transfer_calibration  # noqa: E402


@dataclass(frozen=True)
class HistoryRow:
    low_conditional_upper: float
    reference_high_tail_upper: float
    comparison_log_loss: float
    chart_complement_upper: float
    density_premise_verified: bool
    complement_premise_verified: bool
    positive_mass: bool = True

    def total_upper(self) -> float:
        return self.low_conditional_upper + math.exp(self.comparison_log_loss) * self.reference_high_tail_upper + self.chart_complement_upper


@dataclass(frozen=True)
class HistoryComparisonCertificate:
    required_positive_mass_histories: int
    supplied_histories: int
    numerical_maximum_row: float
    target_continuous_budget: float
    numerical_table_closes: bool
    all_density_premises_verified: bool
    all_complement_premises_verified: bool
    physical_history_uniform_bound_proved: bool
    adaptive_domination_implication_available: bool
    retained_state_conditionally_sufficient_assumed: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def history_comparison_certificate(
    rows: Mapping[tuple[int, ...], HistoryRow],
    required_histories: Sequence[tuple[int, ...]],
    target_continuous_budget: float,
) -> HistoryComparisonCertificate:
    required = tuple(required_histories)
    target = float(target_continuous_budget)
    if not required or len(set(required)) != len(required) or not 0.0 < target < 1.0:
        raise ValueError("invalid history specification")
    if set(rows) != set(required):
        raise ValueError("history table must cover exactly the positive-mass histories")
    if any(not row.positive_mass for row in rows.values()):
        raise ValueError("zero-mass histories must not be inserted as required rows")
    totals = []
    for row in rows.values():
        values = (row.low_conditional_upper, row.reference_high_tail_upper, row.comparison_log_loss, row.chart_complement_upper)
        if any(not math.isfinite(value) or value < 0.0 for value in values):
            raise ValueError("history bounds must be finite and nonnegative")
        totals.append(row.total_upper())
    maximum = max(totals)
    density = all(row.density_premise_verified for row in rows.values())
    complement = all(row.complement_premise_verified for row in rows.values())
    numerical = maximum <= target
    return HistoryComparisonCertificate(
        required_positive_mass_histories=len(required),
        supplied_histories=len(rows),
        numerical_maximum_row=maximum,
        target_continuous_budget=target,
        numerical_table_closes=numerical,
        all_density_premises_verified=density,
        all_complement_premises_verified=complement,
        physical_history_uniform_bound_proved=numerical and density and complement,
        adaptive_domination_implication_available=True,
        retained_state_conditionally_sufficient_assumed=True,
    )


def calibration() -> dict[str, Any]:
    rho = 2.0 * .011453785959974176
    low = low_certificate(6.0 * .006**2, rho).probability_upper
    high = transfer_calibration()["certificate"]
    row = HistoryRow(
        low,
        high["reference_tail_upper"],
        high["comparison_log_loss"],
        high["chart_complement_upper"],
        False,
        False,
    )
    histories = ((), (0,), (1,))
    rows = {history: row for history in histories}
    continuous_budget = 2.0 * .0004860555003683996
    cert = history_comparison_certificate(rows, histories, continuous_budget)
    illustrative_table = {history: cert.numerical_maximum_row for history in histories}
    adaptive = adaptive_certificate(illustrative_table, 2, .002430277501841998)
    return {
        "claim_level": "C2 exact retained-history comparison interface plus restricted numerical table",
        "retained_schema_additions": [
            "density_comparison_class",
            "chart_complement_certificate",
            "repair_spill_spectrum",
        ],
        "history_certificate": cert.to_dict(),
        "restricted_adaptive_certificate": adaptive.to_dict(),
        "physical_positive_mass_history_table_proved": False,
        "first_open_supremum": "supremum of density loss and nonlinear chart-complement mass over every positive-mass retained history and finite volume",
    }


def main() -> None:
    argparse.ArgumentParser().parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
