"""Advanced finite calibrations for the heat-kernel basin-entry programme.

Implemented experiments:

1. SU(2) heat-kernel TV distance to translation by the central element -I.
2. U(1) convolution blocking, using p_t^{*m} = p_{m t}.
3. A good-field tail and optimistic K+R row-norm proxy.
4. A one-plaquette U(1) heat-kernel/Wilson comparison at matched curvature.

Only item 1 illustrates a theorem proved for all compact groups.  Items 2--4
are finite diagnostics and are not continuum or universality proofs.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from typing import Iterable

from heat_kernel_influence import TAU, circle_heat_kernel, total_variation_translate


def _su2_cutoff(t: float, tolerance: float) -> int:
    if t <= 0.0:
        raise ValueError("heat time must be positive")
    if not 0.0 < tolerance < 1.0:
        raise ValueError("tolerance must lie in (0,1)")
    n = 0
    while (n + 1) ** 2 * math.exp(-0.5 * t * n * (n + 2)) > tolerance:
        n += 1
        if n > 100000:
            raise RuntimeError("character cutoff did not converge")
    return n


def su2_character(n: int, theta: float) -> float:
    if n < 0:
        raise ValueError("representation index must be nonnegative")
    denominator = math.sin(theta)
    if abs(denominator) < 1e-12:
        # The calibration uses midpoint quadrature, but close the endpoint case.
        sign = 1.0 if math.cos(theta) > 0.0 else (-1.0) ** n
        return sign * (n + 1)
    return math.sin((n + 1) * theta) / denominator


def su2_heat_kernel(theta: float, t: float, tolerance: float = 1e-13) -> float:
    """SU(2) heat kernel for Casimir C_2(n)=n(n+2)."""
    cutoff = _su2_cutoff(t, tolerance)
    terms = [
        (n + 1)
        * math.exp(-0.5 * t * n * (n + 2))
        * su2_character(n, theta)
        for n in range(cutoff + 1)
    ]
    value = math.fsum(terms)
    if value < 0.0 and abs(value) < 1000.0 * tolerance:
        return 0.0
    return value


def su2_antipodal_tv(t: float, grid_size: int = 16384) -> float:
    """TV(p_t(g), p_t((-I)^(-1)g)) using the SU(2) class angle."""
    if grid_size < 256:
        raise ValueError("grid_size must be at least 256")
    dx = math.pi / grid_size
    values = []
    for k in range(grid_size):
        theta = (k + 0.5) * dx
        haar = (2.0 / math.pi) * math.sin(theta) ** 2
        values.append(
            abs(su2_heat_kernel(theta, t) - su2_heat_kernel(math.pi - theta, t))
            * haar
        )
    return min(1.0, 0.5 * dx * math.fsum(values))


def circle_good_field_tail(
    t: float, rho: float, grid_size: int = 32768
) -> float:
    """P_t[distance(theta,0) > rho sqrt(t)] on U(1)."""
    if rho <= 0.0:
        raise ValueError("rho must be positive")
    threshold = min(math.pi, rho * math.sqrt(t))
    dx = TAU / grid_size
    terms = []
    for k in range(grid_size):
        theta = -math.pi + (k + 0.5) * dx
        if abs(theta) > threshold:
            terms.append(circle_heat_kernel(theta, t))
    return min(1.0, max(0.0, dx * math.fsum(terms)))


def wilson_u1_density(theta: float, beta: float, normalization: float) -> float:
    return math.exp(beta * (math.cos(theta) - 1.0)) / normalization


def heat_kernel_wilson_tv(t: float, grid_size: int = 32768) -> float:
    """One-plaquette U(1) TV at beta=1/t, matching quadratic curvature."""
    if t <= 0.0:
        raise ValueError("heat time must be positive")
    beta = 1.0 / t
    dx = TAU / grid_size
    angles = [-math.pi + (k + 0.5) * dx for k in range(grid_size)]
    normalization = dx * math.fsum(
        math.exp(beta * (math.cos(theta) - 1.0)) for theta in angles
    )
    l1 = math.fsum(
        abs(
            circle_heat_kernel(theta, t)
            - wilson_u1_density(theta, beta, normalization)
        )
        for theta in angles
    )
    return min(1.0, 0.5 * dx * l1)


@dataclass(frozen=True)
class AdvancedRow:
    heat_time: float
    su2_antipodal_tv: float
    u1_wilson_tv: float
    u1_tail_rho_2: float
    u1_local_shift_tv_c_025: float
    optimistic_degree_8_proxy: float


def advanced_calibration(
    heat_times: Iterable[float], grid_size: int = 16384
) -> list[AdvancedRow]:
    rows = []
    for t in heat_times:
        tail = circle_good_field_tail(t, 2.0, grid_size)
        local_tv = total_variation_translate(t, 0.25 * math.sqrt(t), grid_size)
        rows.append(
            AdvancedRow(
                heat_time=t,
                su2_antipodal_tv=su2_antipodal_tv(t, grid_size),
                u1_wilson_tv=heat_kernel_wilson_tv(t, grid_size),
                u1_tail_rho_2=tail,
                u1_local_shift_tv_c_025=local_tv,
                optimistic_degree_8_proxy=8.0 * (tail + local_tv),
            )
        )
    return rows


def blocking_calibration(
    microscopic_t: float, steps: Iterable[int], shift: float = math.pi
) -> list[dict[str, float | int]]:
    rows = []
    for m in steps:
        if m <= 0:
            raise ValueError("blocking steps must be positive")
        coarse_t = m * microscopic_t
        rows.append(
            {
                "steps": m,
                "coarse_heat_time": coarse_t,
                "fixed_shift_tv": total_variation_translate(coarse_t, shift),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--times", nargs="+", type=float, default=[0.5, 0.2, 0.1, 0.05])
    parser.add_argument("--grid-size", type=int, default=16384)
    parser.add_argument("--output", choices=("table", "json"), default="table")
    args = parser.parse_args()
    rows = advanced_calibration(args.times, args.grid_size)
    blocked = blocking_calibration(0.02, [1, 2, 5, 10, 20, 50])
    if args.output == "json":
        print(
            json.dumps(
                {
                    "advanced": [asdict(row) for row in rows],
                    "blocking_u1": blocked,
                    "scope": "finite calibration; not a basin-entry or universality proof",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    print("t\tSU2 antipodal TV\tU1 HK/Wilson TV\tU1 tail\tlocal TV\tdegree-8 proxy")
    for row in rows:
        print(
            f"{row.heat_time:.6g}\t{row.su2_antipodal_tv:.9f}\t"
            f"{row.u1_wilson_tv:.9f}\t{row.u1_tail_rho_2:.9f}\t"
            f"{row.u1_local_shift_tv_c_025:.9f}\t"
            f"{row.optimistic_degree_8_proxy:.9f}"
        )
    print("\nU(1) exact convolution blocking at microscopic t=0.02")
    print("steps\tcoarse t\tfixed-shift TV")
    for row in blocked:
        print(f"{row['steps']}\t{row['coarse_heat_time']:.6g}\t{row['fixed_shift_tv']:.9f}")


if __name__ == "__main__":
    main()
