"""Ultraviolet overlap benchmark for the Stage 08 SU(2) block certificate.

This module proves three restricted finite statements:

* a cancellation-free upper bound for a standalone SU(2) heat-kernel tail;
* local Haar-Jacobian derivative bounds in exponential link coordinates; and
* coexistence of the augmented local-action inequalities with an
  independent-block weighted-polymer benchmark.

The standalone heat-kernel law is not asserted to be a plaquette marginal of
the interacting four-dimensional link measure.  Blocks in that measure are
not independent.  Consequently this module does not prove full-measure basin
entry, a multiscale RG trajectory, continuum Yang--Mills, or a mass gap.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path
import platform
import sys
from typing import Any, Iterable

import numpy as np


STAGE08 = Path(__file__).resolve().parents[1] / "08_su2_nonlinear_block_geometry"
if str(STAGE08) not in sys.path:
    sys.path.insert(0, str(STAGE08))

from su2_nonlinear_block_geometry import (  # noqa: E402
    action_initialization_certificate,
    gauge_slice_certificate,
    plaquette_chart_certificate,
)


def _finite_positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _finite_nonnegative(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


@dataclass(frozen=True)
class HaarJacobianCertificate:
    link_radius: float
    jacobian_formula: str
    negative_log_formula: str
    hessian_operator_bound: float
    third_derivative_operator_bound: float
    series_ratio: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ImageTailCertificate:
    time: float
    curvature_radius: float
    normalization_core_radius: float
    zero_image_tail_upper: float
    zero_image_normalization_lower: float
    nonzero_image_integral_upper: float
    normalization_lower: float
    probability_upper: float
    radius_in_heat_units: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IndependentPolymerCertificate:
    plaquettes_per_block: int
    block_max_degree: int
    activity_weight: float
    one_plaquette_bad_upper: float
    block_bad_union_upper: float
    unweighted_branching_proxy: float
    weighted_branching_proxy: float
    rooted_weighted_activity_sum_upper: float | None
    weighted_subcritical: bool
    rooted_sum_below_one: bool
    independence_assumed: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class UVOverlapCertificate:
    time: float
    link_radius: float
    curvature_radius: float
    fiber_radius: float
    plaquette_hessian_remainder: float
    haar_scaled_hessian_contribution: float
    augmented_hessian_remainder: float
    plaquette_third_derivative_bound: float
    haar_scaled_third_contribution: float
    augmented_third_derivative_bound: float
    fiber_margin: float
    centered_transport_coefficient: float
    generated_good_hessian_budget: float
    generated_base_margin: float
    nonlinear_physical_min_singular_value: float
    local_action_certified: bool
    independent_overlap_benchmark_certified: bool
    strict_neighborhood_exists: bool
    full_measure_certified: bool
    dependent_polymer_certified: bool
    topology_certified: bool
    repeated_rg_certified: bool
    continuum_certified: bool
    mass_gap_certified: bool
    haar: HaarJacobianCertificate
    tail: ImageTailCertificate
    polymer: IndependentPolymerCertificate

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["haar"] = self.haar.to_dict()
        result["tail"] = self.tail.to_dict()
        result["polymer"] = self.polymer.to_dict()
        return result


@dataclass(frozen=True)
class SearchCertificate:
    time_grid: tuple[float, ...]
    radius_grid: tuple[float, ...]
    fiber_radius: float
    feasible_points: int
    total_points: int
    selected_time: float | None
    selected_radius: float | None
    selected_robustness_score: float | None
    global_optimality_claimed: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def haar_jacobian_certificate(link_radius: float) -> HaarJacobianCertificate:
    """Bound derivatives of h(A)=-2 log(sin|A|/|A|).

    Euler's product gives

        h(r)=2 sum_{n>=1} zeta(2n) r^(2n)/(n pi^(2n)).

    We use zeta(2n)<=zeta(2)=pi^2/6 termwise.  For each radial monomial,
    its second- and third-derivative operator norms are bounded by its radial
    second and third derivatives.  Summing the resulting geometric series
    gives the closed bounds below.
    """

    radius = _finite_nonnegative("link_radius", link_radius)
    if radius >= math.pi:
        raise ValueError("the exponential chart requires link_radius < pi")
    x = radius / math.pi
    q = x * x
    hessian = (2.0 / 3.0) * (1.0 + q) / (1.0 - q) ** 2
    third = (2.0 / (3.0 * math.pi)) * x * (
        4.0 * (1.0 + q) / (1.0 - q) ** 3
        + 2.0 / (1.0 - q) ** 2
    )
    return HaarJacobianCertificate(
        link_radius=radius,
        jacobian_formula="J(A)=(sin(|A|)/|A|)^2",
        negative_log_formula="h(A)=-2 log(sin(|A|)/|A|)",
        hessian_operator_bound=hessian,
        third_derivative_operator_bound=third,
        series_ratio=q,
    )


def _nonzero_image_integral_upper(time: float) -> float:
    """Sum an L1 upper bound for all nonzero Poisson images.

    The negative first image begins at geodesic distance pi and the positive
    first image at 2pi.  Consecutive absolute integral bounds have ratio at
    most exp(-4 pi^2/t).
    """

    q = math.exp(-4.0 * math.pi**2 / time)
    numerator = time * (
        math.exp(-math.pi**2 / (2.0 * time))
        + math.exp(-2.0 * math.pi**2 / time)
    )
    return numerator / (1.0 - q)


def su2_image_tail_upper(
    time: float,
    curvature_radius: float,
    core_sigma: float = 3.0,
) -> ImageTailCertificate:
    """Upper-bound a standalone SU(2) heat-kernel curvature tail.

    With generator (1/2)Delta, the radial mass is proportional to

        sin(theta) sum_k (theta+2 pi k)
        exp(-(theta+2 pi k)^2/(2t)) dtheta.

    The numerator uses sin(theta)<=theta for the zero image and an L1 bound
    for every nonzero image.  The denominator retains a zero-image core on
    [0,L], uses sin(theta)>=sinc(L) theta, and subtracts the same image error.
    This representation is stable as t tends to zero and involves no
    cancellation of large character terms.
    """

    time = _finite_positive("time", time)
    radius = _finite_positive("curvature_radius", curvature_radius)
    core_sigma = _finite_positive("core_sigma", core_sigma)
    if radius >= math.pi:
        raise ValueError("curvature_radius must be smaller than pi")
    core = min(0.5 * math.pi, core_sigma * math.sqrt(time))
    z_core = core / math.sqrt(2.0 * time)
    maxwell_core = (
        math.sqrt(math.pi / 2.0) * time ** 1.5 * math.erf(z_core)
        - time * core * math.exp(-core * core / (2.0 * time))
    )
    zero_normalization = (math.sin(core) / core) * maxwell_core

    z_tail = radius / math.sqrt(2.0 * time)
    zero_tail = (
        time * radius * math.exp(-radius * radius / (2.0 * time))
        + time * math.sqrt(math.pi * time / 2.0) * math.erfc(z_tail)
    )
    image_error = _nonzero_image_integral_upper(time)
    normalization = zero_normalization - image_error
    if normalization <= 0.0:
        raise ValueError("the image bound does not leave a positive normalization")
    probability = min(1.0, (zero_tail + image_error) / normalization)
    return ImageTailCertificate(
        time=time,
        curvature_radius=radius,
        normalization_core_radius=core,
        zero_image_tail_upper=zero_tail,
        zero_image_normalization_lower=zero_normalization,
        nonzero_image_integral_upper=image_error,
        normalization_lower=normalization,
        probability_upper=probability,
        radius_in_heat_units=radius / math.sqrt(time),
    )


def independent_polymer_certificate(
    one_plaquette_bad_upper: float,
    plaquettes_per_block: int = 216,
    block_max_degree: int = 8,
    activity_weight: float = 0.1,
) -> IndependentPolymerCertificate:
    """Rooted connected-set benchmark for independent bad blocks.

    A union bound gives p_B<=m p.  If blocks are independent and the block
    graph has maximum degree Delta, the number of rooted connected n-sets is
    bounded by Delta^(2(n-1)).  Therefore

      sum_{P containing o} exp(alpha |P|) P(P all bad)
      <= exp(alpha) p_B / (1-exp(alpha) Delta^2 p_B).

    This theorem is intentionally not applied to dependent Yang--Mills
    blocks.
    """

    p = _finite_nonnegative("one_plaquette_bad_upper", one_plaquette_bad_upper)
    if p > 1.0:
        raise ValueError("one_plaquette_bad_upper must be at most one")
    if plaquettes_per_block < 1 or block_max_degree < 1:
        raise ValueError("block size and degree must be positive")
    alpha = _finite_nonnegative("activity_weight", activity_weight)
    block_p = min(1.0, plaquettes_per_block * p)
    unweighted = block_max_degree**2 * block_p
    weighted = math.exp(alpha) * unweighted
    if weighted < 1.0:
        rooted_sum = math.exp(alpha) * block_p / (1.0 - weighted)
    else:
        rooted_sum = None
    return IndependentPolymerCertificate(
        plaquettes_per_block=plaquettes_per_block,
        block_max_degree=block_max_degree,
        activity_weight=alpha,
        one_plaquette_bad_upper=p,
        block_bad_union_upper=block_p,
        unweighted_branching_proxy=unweighted,
        weighted_branching_proxy=weighted,
        rooted_weighted_activity_sum_upper=rooted_sum,
        weighted_subcritical=weighted < 1.0,
        rooted_sum_below_one=rooted_sum is not None and rooted_sum < 1.0,
        independence_assumed=True,
    )


def uv_overlap_certificate(
    time: float = 3.0e-6,
    link_radius: float = 0.0041,
    fiber_radius: float = 1.0e-5,
    plaquettes_per_block: int = 216,
    block_max_degree: int = 8,
    activity_weight: float = 0.1,
) -> UVOverlapCertificate:
    """Compose the Stage 08 local certificate with the UV benchmark."""

    time = _finite_positive("time", time)
    link_radius = _finite_positive("link_radius", link_radius)
    fiber_radius = _finite_nonnegative("fiber_radius", fiber_radius)
    chart = plaquette_chart_certificate(link_radius)
    action = action_initialization_certificate(time, link_radius, fiber_radius)
    haar = haar_jacobian_certificate(link_radius)
    tail = su2_image_tail_upper(time, chart.curvature_radius)
    polymer = independent_polymer_certificate(
        tail.probability_upper,
        plaquettes_per_block,
        block_max_degree,
        activity_weight,
    )

    haar_hessian = time * haar.hessian_operator_bound
    haar_third = time * haar.third_derivative_operator_bound
    eta = action.global_hessian_remainder + haar_hessian
    tau = action.global_third_derivative_bound + haar_third

    base_embedding = 1.0 / math.sqrt(2.0)
    eps_cross = eta * base_embedding
    eps_base = eta * base_embedding**2
    tau_cross = tau * base_embedding
    fiber_margin = 2.0 - eta
    if fiber_margin <= 0.0:
        response = math.inf
        transport = math.inf
        generated = math.inf
        base_margin = -math.inf
    else:
        response = eps_cross / fiber_margin
        centered_cross = fiber_radius * (tau_cross + tau * response)
        transport = centered_cross / fiber_margin
        generated = eps_base + eps_cross**2 / fiber_margin
        base_margin = 1.0 - generated

    local_ok = (
        chart.nonlinear_physical_min_singular_value > 0.0
        and eta < 1.0
        and transport < 1.0
        and base_margin > 0.0
    )
    overlap_ok = (
        local_ok
        and polymer.weighted_subcritical
        and polymer.rooted_sum_below_one
    )
    # All pass conditions are strict and the formulas are continuous at the
    # witness, so a nonempty open neighborhood inherits them.
    neighborhood = overlap_ok and all(
        value > 0.0
        for value in (
            1.0 - eta,
            1.0 - transport,
            base_margin,
            1.0 - polymer.weighted_branching_proxy,
            1.0 - polymer.rooted_weighted_activity_sum_upper,
        )
    )
    return UVOverlapCertificate(
        time=time,
        link_radius=link_radius,
        curvature_radius=chart.curvature_radius,
        fiber_radius=fiber_radius,
        plaquette_hessian_remainder=action.global_hessian_remainder,
        haar_scaled_hessian_contribution=haar_hessian,
        augmented_hessian_remainder=eta,
        plaquette_third_derivative_bound=action.global_third_derivative_bound,
        haar_scaled_third_contribution=haar_third,
        augmented_third_derivative_bound=tau,
        fiber_margin=fiber_margin,
        centered_transport_coefficient=transport,
        generated_good_hessian_budget=generated,
        generated_base_margin=base_margin,
        nonlinear_physical_min_singular_value=(
            chart.nonlinear_physical_min_singular_value
        ),
        local_action_certified=local_ok,
        independent_overlap_benchmark_certified=overlap_ok,
        strict_neighborhood_exists=neighborhood,
        full_measure_certified=False,
        dependent_polymer_certified=False,
        topology_certified=False,
        repeated_rg_certified=False,
        continuum_certified=False,
        mass_gap_certified=False,
        haar=haar,
        tail=tail,
        polymer=polymer,
    )


def search_overlap(
    times: Iterable[float] | None = None,
    radii: Iterable[float] | None = None,
    fiber_radius: float = 1.0e-5,
) -> SearchCertificate:
    """Search a declared grid and select the largest normalized slack.

    This is calibration only.  It makes no global optimality claim.
    """

    time_grid = tuple(
        float(x)
        for x in (
            np.geomspace(1.0e-6, 5.0e-6, 25) if times is None else times
        )
    )
    radius_grid = tuple(
        float(x)
        for x in (
            np.linspace(0.0036, 0.0042, 25) if radii is None else radii
        )
    )
    best: tuple[float, UVOverlapCertificate] | None = None
    feasible = 0
    for time in time_grid:
        for radius in radius_grid:
            try:
                cert = uv_overlap_certificate(time, radius, fiber_radius)
            except ValueError:
                continue
            if not cert.independent_overlap_benchmark_certified:
                continue
            feasible += 1
            score = min(
                1.0 - cert.augmented_hessian_remainder,
                1.0 - cert.centered_transport_coefficient,
                cert.generated_base_margin,
                1.0 - cert.polymer.weighted_branching_proxy,
                1.0 - cert.polymer.rooted_weighted_activity_sum_upper,
            )
            if best is None or score > best[0]:
                best = (score, cert)
    return SearchCertificate(
        time_grid=time_grid,
        radius_grid=radius_grid,
        fiber_radius=fiber_radius,
        feasible_points=feasible,
        total_points=len(time_grid) * len(radius_grid),
        selected_time=None if best is None else best[1].time,
        selected_radius=None if best is None else best[1].link_radius,
        selected_robustness_score=None if best is None else best[0],
        global_optimality_claimed=False,
    )


def calibration() -> dict[str, Any]:
    witness = uv_overlap_certificate()
    stage08_point = uv_overlap_certificate(0.01, 0.003, 0.001)
    gauge = gauge_slice_certificate(0.0002, 0.0006, witness.link_radius)
    search = search_overlap()
    return {
        "scope": (
            "finite nonlinear 2^4 local-action certificate plus standalone SU(2) "
            "heat-kernel tail and independent-block weighted-polymer benchmark; "
            "not a marginal or polymer theorem for the interacting 4D link measure"
        ),
        "witness": witness.to_dict(),
        "stage08_point_comparison": stage08_point.to_dict(),
        "gauge_slice_at_witness_chart": gauge.to_dict(),
        "declared_grid_search": search.to_dict(),
        "first_unproved_implication": (
            "replace the standalone tail and independent-block benchmark by a "
            "volume-uniform dependent polymer/activity estimate for the complete "
            "gauge-invariant 4D link measure, including Bianchi and topological sectors"
        ),
        "claim_level": "C2 restricted certificate",
        "frontier_flags": {
            "actual_full_measure_tail": False,
            "dependent_polymer": False,
            "gauge_slice_density": False,
            "topological_sectors": False,
            "multiscale_iteration": False,
            "continuum_yang_mills": False,
            "hamiltonian_mass_gap": False,
        },
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json", "table"), default="table")
    args = parser.parse_args()
    result = calibration()
    if args.output == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    witness = result["witness"]
    polymer = witness["polymer"]
    print(f"augmented Hessian remainder: {witness['augmented_hessian_remainder']:.9f}")
    print(f"generated base margin: {witness['generated_base_margin']:.9f}")
    print(f"one-plaquette tail upper: {polymer['one_plaquette_bad_upper']:.12g}")
    print(f"block union upper: {polymer['block_bad_union_upper']:.12g}")
    print(f"weighted branching proxy: {polymer['weighted_branching_proxy']:.9f}")
    print(
        "rooted weighted activity sum upper: "
        f"{polymer['rooted_weighted_activity_sum_upper']:.9f}"
    )
    print(
        "restricted overlap benchmark: "
        f"{witness['independent_overlap_benchmark_certified']}"
    )


if __name__ == "__main__":
    main()
