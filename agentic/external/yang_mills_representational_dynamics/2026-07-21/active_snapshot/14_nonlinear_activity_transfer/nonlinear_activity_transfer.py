"""Two-tier transfer from dependent Gaussian defects to nonlinear activities.

For each connected plaquette set X, split the nonlinear bad event into a
coherent-collar channel and a charged collar-failure channel.  Suppose

  mu(B_X and G_X)   <= exp(-(J-kappa)|X|),
  mu(B_X and not G_X) <= exp(-K|X|).

Then

  mu(B_X) <= q_eff^|X|,
  q_eff = exp(kappa-J) + exp(-K).

With maximum plaquette adjacency degree Delta and connected-set count bounded
by Delta^(2(n-1)), the rooted weighted sum converges when

  exp(alpha) Delta^2 q_eff < 1.

The transfer and its parameter budget are exact.  Establishing the two input
inequalities for the full nonlinear SU(2) measure remains the analytic
frontier.
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
    PACKAGE / "12_center_contour_charging",
    PACKAGE / "13_dependent_gaussian_polymers",
):
    if str(sibling) not in sys.path:
        sys.path.insert(0, str(sibling))

from center_contour_charging import center_complex_certificate  # noqa: E402
from dependent_gaussian_polymers import radial_gaussian_rate  # noqa: E402


@dataclass(frozen=True)
class ActivityTransferCertificate:
    heat_time: float
    curvature_radius: float
    gaussian_rate_J: float
    nonlinear_comparison_loss_kappa: float
    charged_collar_rate_K: float
    alpha: float
    adjacency_degree: int
    good_collar_effective_weight: float
    collar_failure_effective_weight: float
    combined_effective_weight: float
    critical_effective_weight: float
    effective_weight_slack: float
    branching_ratio: float
    rooted_weighted_activity_sum_upper: float
    maximum_kappa_without_collar_failures: float
    minimum_K_at_declared_kappa: float
    abstract_transfer_certified: bool
    declared_parameters_subcritical: bool
    mayer_activity_identification_certified: bool
    nonlinear_su2_hypotheses_verified: bool
    basin_entry_certified: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MultiscaleCompositionCertificate:
    scale_count: int
    per_scale_effective_weights: tuple[float, ...]
    per_scale_branching_ratios: tuple[float, ...]
    per_scale_rooted_bounds: tuple[float, ...]
    total_rooted_error_upper: float
    all_declared_scales_subcritical: bool
    finite_registry_summable: bool
    infinite_scale_uniformity_verified: bool
    actual_rg_maps_verified: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _finite_positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def effective_weight(gaussian_rate_J: float, kappa: float, collar_rate_K: float) -> float:
    J = _finite_positive("gaussian_rate_J", gaussian_rate_J)
    K = _finite_positive("collar_rate_K", collar_rate_K)
    kappa = float(kappa)
    if not math.isfinite(kappa) or kappa < 0.0:
        raise ValueError("kappa must be finite and nonnegative")
    return math.exp(kappa - J) + math.exp(-K)


def transfer_certificate(
    heat_time: float = 3.0e-6,
    curvature_radius: float = 0.0082,
    kappa: float = 0.2,
    collar_rate_K: float = 7.0,
    alpha: float = 0.1,
    adjacency_degree: int | None = None,
) -> ActivityTransferCertificate:
    t = _finite_positive("heat_time", heat_time)
    rho = _finite_positive("curvature_radius", curvature_radius)
    K = _finite_positive("collar_rate_K", collar_rate_K)
    kappa = float(kappa)
    alpha = float(alpha)
    if not math.isfinite(kappa) or kappa < 0.0:
        raise ValueError("kappa must be finite and nonnegative")
    if not math.isfinite(alpha) or alpha < 0.0:
        raise ValueError("alpha must be finite and nonnegative")
    degree = (
        center_complex_certificate().link_adjacency_max_degree
        if adjacency_degree is None
        else int(adjacency_degree)
    )
    if degree < 1:
        raise ValueError("adjacency_degree must be positive")
    J = radial_gaussian_rate(rho * rho / t, 3)
    if J <= 0.0:
        raise ValueError("the Gaussian radial rate must be positive")
    good = math.exp(kappa - J)
    collar = math.exp(-K)
    combined = good + collar
    critical = math.exp(-alpha) / (degree * degree)
    ratio = math.exp(alpha) * degree * degree * combined
    rooted = math.exp(alpha) * combined / (1.0 - ratio) if ratio < 1.0 else math.inf
    max_kappa = J + math.log(critical)
    remaining = critical - good
    min_K = -math.log(remaining) if remaining > 0.0 else math.inf
    return ActivityTransferCertificate(
        heat_time=t,
        curvature_radius=rho,
        gaussian_rate_J=J,
        nonlinear_comparison_loss_kappa=kappa,
        charged_collar_rate_K=K,
        alpha=alpha,
        adjacency_degree=degree,
        good_collar_effective_weight=good,
        collar_failure_effective_weight=collar,
        combined_effective_weight=combined,
        critical_effective_weight=critical,
        effective_weight_slack=critical - combined,
        branching_ratio=ratio,
        rooted_weighted_activity_sum_upper=rooted,
        maximum_kappa_without_collar_failures=max_kappa,
        minimum_K_at_declared_kappa=min_K,
        abstract_transfer_certified=True,
        declared_parameters_subcritical=ratio < 1.0 and rooted < 1.0,
        mayer_activity_identification_certified=False,
        nonlinear_su2_hypotheses_verified=False,
        basin_entry_certified=False,
    )


def multiscale_composition_certificate(
    scale_parameters: Iterable[tuple[float, float, float]],
    alpha: float = 0.1,
    adjacency_degree: int = 18,
) -> MultiscaleCompositionCertificate:
    """Compose a finite declared registry of (J,kappa,K) bounds.

    This verifies only the abstract summation.  It does not construct the RG
    maps or prove that actual Yang--Mills parameters obey the registry.
    """

    params = tuple((float(J), float(kappa), float(K)) for J, kappa, K in scale_parameters)
    if not params:
        raise ValueError("at least one scale is required")
    if not math.isfinite(alpha) or alpha < 0.0 or adjacency_degree < 1:
        raise ValueError("invalid multiscale counting parameters")
    weights: list[float] = []
    ratios: list[float] = []
    rooted: list[float] = []
    for J, kappa, K in params:
        q = effective_weight(J, kappa, K)
        ratio = math.exp(alpha) * adjacency_degree**2 * q
        bound = math.exp(alpha) * q / (1.0 - ratio) if ratio < 1.0 else math.inf
        weights.append(q)
        ratios.append(ratio)
        rooted.append(bound)
    total = math.fsum(rooted)
    all_subcritical = all(r < 1.0 and math.isfinite(b) for r, b in zip(ratios, rooted))
    return MultiscaleCompositionCertificate(
        scale_count=len(params),
        per_scale_effective_weights=tuple(weights),
        per_scale_branching_ratios=tuple(ratios),
        per_scale_rooted_bounds=tuple(rooted),
        total_rooted_error_upper=total,
        all_declared_scales_subcritical=all_subcritical,
        finite_registry_summable=all_subcritical and math.isfinite(total),
        infinite_scale_uniformity_verified=False,
        actual_rg_maps_verified=False,
    )


def calibration() -> dict[str, Any]:
    single = transfer_certificate()
    registry = (
        (single.gaussian_rate_J, 0.2, 7.0),
        (7.0, 0.2, 7.4),
        (7.5, 0.2, 7.8),
        (8.0, 0.2, 8.2),
    )
    return {
        "one_scale_transfer": single.to_dict(),
        "declared_four_scale_registry": multiscale_composition_certificate(registry).to_dict(),
        "first_unproved_implication": (
            "prove uniform nonlinear good-collar comparison kappa<=0.2 and "
            "charged collar-failure rate K>=7.0 for the complete SU(2) link measure, "
            "then construct or dominate the corresponding connected activities"
        ),
        "claim_level": "C2 abstract transfer theorem with conditional SU(2) gate",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2))


if __name__ == "__main__":
    main()
