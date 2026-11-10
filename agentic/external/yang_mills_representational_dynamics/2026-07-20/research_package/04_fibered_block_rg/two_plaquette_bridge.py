"""Two-plaquette heat-kernel bridge and fibered-RG calibrations.

For U(1), two adjacent heat-kernel plaquettes with retained total holonomy s
have conditional density

    gamma_t^s(q) = p_t(q) p_t(s-q) / p_{2t}(s).

The retained mode is s.  The eliminated fiber coordinate is r=q-s/2.  This
module compares the boundary sensitivity of q with that of r and implements
restricted defect-percolation and regulator-comparison bounds.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from statistics import median
from typing import Iterable, Sequence

import sys
from pathlib import Path

_PARENT_CALIBRATION = Path(__file__).resolve().parents[1] / "ym_basin_entry_attack"
if str(_PARENT_CALIBRATION) not in sys.path:
    sys.path.insert(0, str(_PARENT_CALIBRATION))

from heat_kernel_influence import TAU, circle_heat_kernel  # noqa: E402
from advanced_regulator_calibration import heat_kernel_wilson_tv  # noqa: E402


def circular_distance(a: float, b: float) -> float:
    return abs((a - b + math.pi) % TAU - math.pi)


def bridge_density(q: float, t: float, total_holonomy: float) -> float:
    if t <= 0.0:
        raise ValueError("heat time must be positive")
    denominator = circle_heat_kernel(total_holonomy, 2.0 * t)
    if denominator <= 0.0:
        raise ValueError("bridge normalization is not positive")
    return (
        circle_heat_kernel(q, t)
        * circle_heat_kernel(total_holonomy - q, t)
        / denominator
    )


def centered_bridge_density(r: float, t: float, total_holonomy: float) -> float:
    return bridge_density(r + 0.5 * total_holonomy, t, total_holonomy)


def density_grid(
    density,
    grid_size: int = 8192,
) -> tuple[list[float], float]:
    if grid_size < 256 or grid_size % 2:
        raise ValueError("grid_size must be an even integer at least 256")
    dx = TAU / grid_size
    values = [density(-math.pi + (k + 0.5) * dx) for k in range(grid_size)]
    normalization = dx * math.fsum(values)
    if normalization <= 0.0:
        raise ValueError("density normalization failed")
    return [value / normalization for value in values], dx


def circle_wasserstein_from_densities(
    p: Sequence[float], q: Sequence[float], dx: float
) -> float:
    """Geodesic W1 on a circle via the median-corrected CDF formula."""
    if len(p) != len(q) or not p:
        raise ValueError("density grids must be nonempty and equally sized")
    cumulative = 0.0
    cdf_difference = []
    for p_value, q_value in zip(p, q):
        cumulative += (p_value - q_value) * dx
        cdf_difference.append(cumulative)
    offset = median(cdf_difference)
    return dx * math.fsum(abs(value - offset) for value in cdf_difference)


def bridge_wasserstein(
    t: float,
    s0: float,
    s1: float,
    centered: bool,
    grid_size: int = 8192,
) -> float:
    density = centered_bridge_density if centered else bridge_density
    p, dx = density_grid(lambda x: density(x, t, s0), grid_size)
    q, _ = density_grid(lambda x: density(x, t, s1), grid_size)
    return circle_wasserstein_from_densities(p, q, dx)


def bridge_lipschitz_coefficient(
    t: float,
    s0: float,
    s1: float,
    centered: bool,
    grid_size: int = 8192,
) -> float:
    boundary_distance = circular_distance(s0, s1)
    if boundary_distance == 0.0:
        raise ValueError("boundary holonomies must differ")
    return bridge_wasserstein(t, s0, s1, centered, grid_size) / boundary_distance


def centered_bridge_defect_tail(
    t: float,
    total_holonomy: float,
    rho: float,
    grid_size: int = 8192,
) -> float:
    """Probability |r| > rho sqrt(t/2) for the centered bridge coordinate."""
    if rho <= 0.0:
        raise ValueError("rho must be positive")
    threshold = min(math.pi, rho * math.sqrt(t / 2.0))
    density, dx = density_grid(
        lambda r: centered_bridge_density(r, t, total_holonomy), grid_size
    )
    terms = []
    for k, value in enumerate(density):
        r = -math.pi + (k + 0.5) * dx
        if abs(r) > threshold:
            terms.append(value)
    return min(1.0, max(0.0, dx * math.fsum(terms)))


def gaussian_bridge_tail(rho: float) -> float:
    """Exact P(|N(0,1)| > rho)."""
    if rho <= 0.0:
        raise ValueError("rho must be positive")
    return math.erfc(rho / math.sqrt(2.0))


def connected_bad_cluster_bound(
    bad_probability: float, max_degree: int, cluster_size: int
) -> float:
    """Crude rooted connected-cluster union bound p (Delta^2 p)^(n-1)."""
    if not 0.0 <= bad_probability <= 1.0:
        raise ValueError("bad probability must lie in [0,1]")
    if max_degree < 1 or cluster_size < 1:
        raise ValueError("degree and cluster size must be positive")
    return min(
        1.0,
        bad_probability
        * (max_degree * max_degree * bad_probability) ** (cluster_size - 1),
    )


def product_block_tv_upper(single_plaquette_tv: float, plaquettes: int) -> float:
    """Tensorization bound TV(mu^m,nu^m) <= m TV(mu,nu)."""
    if not 0.0 <= single_plaquette_tv <= 1.0 or plaquettes < 1:
        raise ValueError("invalid TV or block size")
    return min(1.0, plaquettes * single_plaquette_tv)


@dataclass(frozen=True)
class FiberCalibrationRow:
    heat_time: float
    boundary_increment: float
    full_mode_coefficient: float
    centered_fiber_coefficient: float
    centered_defect_tail_rho_3: float
    degree_8_branching_proxy: float
    hk_wilson_one_plaquette_tv: float
    hk_wilson_16_plaquette_upper: float


def calibrate_fibers(
    heat_times: Iterable[float],
    increment_scale: float = 0.1,
    rho: float = 3.0,
    grid_size: int = 8192,
) -> list[FiberCalibrationRow]:
    rows = []
    for t in heat_times:
        increment = increment_scale * math.sqrt(t)
        full = bridge_lipschitz_coefficient(t, 0.0, increment, False, grid_size)
        fiber = bridge_lipschitz_coefficient(t, 0.0, increment, True, grid_size)
        tail = centered_bridge_defect_tail(t, 0.0, rho, grid_size)
        one_tv = heat_kernel_wilson_tv(t, max(8192, grid_size))
        rows.append(
            FiberCalibrationRow(
                heat_time=t,
                boundary_increment=increment,
                full_mode_coefficient=full,
                centered_fiber_coefficient=fiber,
                centered_defect_tail_rho_3=tail,
                degree_8_branching_proxy=64.0 * tail,
                hk_wilson_one_plaquette_tv=one_tv,
                hk_wilson_16_plaquette_upper=product_block_tv_upper(one_tv, 16),
            )
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--times", nargs="+", type=float, default=[0.5, 0.2, 0.1, 0.05])
    parser.add_argument("--grid-size", type=int, default=8192)
    parser.add_argument("--output", choices=("table", "json"), default="table")
    args = parser.parse_args()
    rows = calibrate_fibers(args.times, grid_size=args.grid_size)
    payload = {
        "rows": [asdict(row) for row in rows],
        "gaussian_tangent": {
            "full_mode_coefficient": 0.5,
            "centered_fiber_coefficient": 0.0,
            "defect_tail_rho_3": gaussian_bridge_tail(3.0),
            "degree_8_branching_factor": 64.0 * gaussian_bridge_tail(3.0),
        },
        "scope": "finite U(1) and Gaussian tangent calibration; not 4D basin entry",
    }
    if args.output == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    print(
        "t\tdelta\tfull coeff\tfiber coeff\ttail(rho=3)\t64 tail\t"
        "HK/W TV\t16-plaq upper"
    )
    for row in rows:
        print(
            f"{row.heat_time:.6g}\t{row.boundary_increment:.6g}\t"
            f"{row.full_mode_coefficient:.9f}\t"
            f"{row.centered_fiber_coefficient:.9f}\t"
            f"{row.centered_defect_tail_rho_3:.9f}\t"
            f"{row.degree_8_branching_proxy:.9f}\t"
            f"{row.hk_wilson_one_plaquette_tv:.9f}\t"
            f"{row.hk_wilson_16_plaquette_upper:.9f}"
        )


if __name__ == "__main__":
    main()
