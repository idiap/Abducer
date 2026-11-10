"""Channel-resolved audit of the exact conditional partition-ratio frontier.

This module composes only previously certified inputs.  It distinguishes
restricted center-sector closure, coherent-collar conditional closure,
quantitatively open incoherent collars, chart/cut-locus normalization, and
unrepresented topology.  It also prints a continuous repair frontier trading
stronger global charge against lower connected-witness entropy.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any, Iterable


PACKAGE = Path(__file__).resolve().parents[1]
for sibling in (
    "12_center_contour_charging",
    "26_partition_ratio_frontier",
    "28_coherent_partition_optimizer",
    "29_coherence_charge_tradeoff",
):
    path = PACKAGE / sibling
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from center_contour_charging import calibration as center_calibration  # noqa: E402
from partition_ratio_frontier import calibration as partition_calibration  # noqa: E402
from coherent_partition_optimizer import joint_kr_certificate  # noqa: E402
from coherence_charge_tradeoff import (  # noqa: E402
    DEGREE,
    rooted_free_energy_at_degree,
    tradeoff_certificate,
)


@dataclass(frozen=True)
class ChannelStatus:
    channel: str
    retained_representation: str
    strongest_certificate: str
    status: str
    numerical_bound: float | None
    normalized_partition_bound: bool
    boundary_state_uniform: bool
    volume_uniform: bool
    physical_su2_channel_closed: bool
    first_open_requirement: str

    def to_dict(self) -> dict[str, str | float | bool | None]:
        return asdict(self)


@dataclass(frozen=True)
class RemedyPoint:
    charge_amplification: float
    maximum_effective_degree_for_required_free_energy: float | None
    current_degree_admissible: bool
    required_free_energy: float

    def to_dict(self) -> dict[str, float | bool | None]:
        return asdict(self)


@dataclass(frozen=True)
class FrontierCertificate:
    channel_count: int
    restricted_or_conditional_progress_count: int
    physically_closed_channel_count: int
    required_uniform_free_energy: float
    physical_partition_ratio_proved: bool
    one_scale_basin_entry_proved: bool
    continuum_yang_mills_proved: bool
    mass_gap_proved: bool
    claim_level: str

    def to_dict(self) -> dict[str, float | int | bool | str]:
        return asdict(self)


def _max_degree_with_amplification(coherence_radius: float, required_free_energy: float, amplification: float) -> float | None:
    amp = float(amplification)
    if not math.isfinite(amp) or amp <= 0.0:
        raise ValueError("amplification must be finite and positive")
    low, high = 1.0, float(DEGREE)
    at_low = rooted_free_energy_at_degree(coherence_radius, low, charge_amplification=amp)
    if at_low <= required_free_energy:
        return None
    at_high = rooted_free_energy_at_degree(coherence_radius, high, charge_amplification=amp)
    if at_high > required_free_energy:
        return high
    for _ in range(120):
        middle = 0.5 * (low + high)
        value = rooted_free_energy_at_degree(coherence_radius, middle, charge_amplification=amp)
        if value > required_free_energy:
            low = middle
        else:
            high = middle
    return low


def remedy_frontier(amplifications: Iterable[float] = (1.0, 1.2, 1.4, 1.55294508627244)) -> tuple[RemedyPoint, ...]:
    tradeoff = tradeoff_certificate()
    eta = tradeoff.maximum_coherence_radius_accepted_by_coherent_bound
    required = 6.712921011389365
    points = []
    for amplification in amplifications:
        degree = _max_degree_with_amplification(eta, required, amplification)
        points.append(
            RemedyPoint(
                charge_amplification=float(amplification),
                maximum_effective_degree_for_required_free_energy=degree,
                current_degree_admissible=degree is not None and degree >= DEGREE - 1.0e-9,
                required_free_energy=required,
            )
        )
    return tuple(points)


def channel_ledger() -> tuple[ChannelStatus, ...]:
    center = center_calibration()["center_contour"]
    coherent = joint_kr_certificate()
    tradeoff = tradeoff_certificate()
    return (
        ChannelStatus(
            channel="center",
            retained_representation="GF(2) center cocycle and Bianchi contour",
            strongest_certificate="exact five-plaquette frustration charge and restricted rooted contour",
            status="restricted_exact; continuous-SU(2) transfer open",
            numerical_bound=center["rooted_weighted_contour_sum_upper"],
            normalized_partition_bound=False,
            boundary_state_uniform=False,
            volume_uniform=False,
            physical_su2_channel_closed=False,
            first_open_requirement="derive the relative center activity from the complete SU(2) conditional partition ratio",
        ),
        ChannelStatus(
            channel="continuous_coherent",
            retained_representation="common eta-ball staple collar",
            strongest_certificate="optimized finite-time conditional tail plus strict local K+R budget",
            status="closed conditional on collar coherence",
            numerical_bound=coherent.coherent_bad_ceiling,
            normalized_partition_bound=True,
            boundary_state_uniform=False,
            volume_uniform=False,
            physical_su2_channel_closed=False,
            first_open_requirement="prove the collar hypothesis or compose it with a normalized complement estimate",
        ),
        ChannelStatus(
            channel="continuous_incoherent",
            retained_representation="overlap-costed connected collar-failure witnesses",
            strongest_certificate="multi-witness charge and quantified coherence-charge gap",
            status="quantitatively open",
            numerical_bound=tradeoff.feasible_interval_width,
            normalized_partition_bound=False,
            boundary_state_uniform=False,
            volume_uniform=False,
            physical_su2_channel_closed=False,
            first_open_requirement="construct a canonical low-entropy witness polymer on the remedy frontier",
        ),
        ChannelStatus(
            channel="cut_orbit",
            retained_representation="two-center atlas and relative tree-gauge boundary state",
            strongest_certificate="global atlas coverage and exact finite Haar disintegration",
            status="geometric representation available; weighted numerator open",
            numerical_bound=None,
            normalized_partition_bound=False,
            boundary_state_uniform=False,
            volume_uniform=False,
            physical_su2_channel_closed=False,
            first_open_requirement="bound chart-transition/cut-locus numerator relative to the retained-state normalizer",
        ),
        ChannelStatus(
            channel="topology",
            retained_representation="no topology label on the present open local block",
            strongest_certificate="scope obstruction identified",
            status="structurally unrepresented",
            numerical_bound=None,
            normalized_partition_bound=False,
            boundary_state_uniform=False,
            volume_uniform=False,
            physical_su2_channel_closed=False,
            first_open_requirement="move to periodic/relative-topology blocks and retain sector labels through blocking",
        ),
    )


def frontier_certificate() -> FrontierCertificate:
    channels = channel_ledger()
    progressed = sum(c.status.startswith("restricted_exact") or c.status.startswith("closed conditional") for c in channels)
    physical = sum(c.physical_su2_channel_closed for c in channels)
    required = partition_calibration()["required_uniform_charged_free_energy"]
    return FrontierCertificate(
        channel_count=len(channels),
        restricted_or_conditional_progress_count=progressed,
        physically_closed_channel_count=physical,
        required_uniform_free_energy=required,
        physical_partition_ratio_proved=physical == len(channels),
        one_scale_basin_entry_proved=False,
        continuum_yang_mills_proved=False,
        mass_gap_proved=False,
        claim_level="C2 exact/conditional finite theorems with audited physical frontier",
    )


def calibration() -> dict[str, Any]:
    tradeoff = tradeoff_certificate()
    frontier = frontier_certificate()
    return {
        "frontier": frontier.to_dict(),
        "channels": [c.to_dict() for c in channel_ledger()],
        "charge_entropy_remedy_frontier": [p.to_dict() for p in remedy_frontier()],
        "strongest_new_positive_result": (
            "the coherent continuous channel has a strict conditional K+R budget "
            "inside the certified nonlinear window"
        ),
        "strongest_new_negative_result": (
            "the current coherent eta ceiling and degree-18 incoherent contour "
            "free-energy threshold are disjoint even at overlap one"
        ),
        "first_open_physical_inequality": (
            "construct a gauge-covariant canonical witness polymer and prove, uniformly "
            "in finite volume, retained state, adaptive history, and channel, its "
            "normalized bad numerator has free energy >6.71292101139; at the current "
            f"coherent eta this requires a point on the charge/entropy remedy frontier "
            f"(unit-charge effective degree <= {tradeoff.maximum_effective_degree_for_required_free_energy:.12g}, "
            f"or degree-18 charge amplification >= {tradeoff.charge_amplification_for_required_free_energy:.12g}, "
            "or a certified combination)"
        ),
        "ranked_next_targets": [
            "canonical sector-aware witness selection with an exact overlap and counting theorem",
            "combined charge/entropy estimate landing on the executable remedy frontier",
            "retained-state normalized partition comparison for that polymer",
            "periodic or relative-topology block carrying explicit sector labels",
            "only after all channels close: volume-uniform one-scale basin entry and RG iteration",
        ],
        "epistemic_stop": (
            "no physical channel is yet closed uniformly; no one-scale basin entry, "
            "continuum Yang-Mills construction, or mass gap is claimed"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
