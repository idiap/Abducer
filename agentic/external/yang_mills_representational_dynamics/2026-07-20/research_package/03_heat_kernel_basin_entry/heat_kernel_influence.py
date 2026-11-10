"""Finite calibration for the heat-kernel basin-entry obstruction.

The U(1) heat kernel is used as an exactly specified compact-group model:

    p_t(theta) = (2 pi)^(-1) [1 + 2 sum_{n>=1} exp(-n^2 t / 2) cos(n theta)].

The script computes total-variation distances between p_t and its translate.
It illustrates, but does not replace, the general compact-group proof in the
accompanying paper.
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import json
import math
from typing import Iterable


TAU = 2.0 * math.pi


def _fourier_cutoff(t: float, tolerance: float) -> int:
    if t <= 0.0:
        raise ValueError("heat time must be positive")
    if not 0.0 < tolerance < 1.0:
        raise ValueError("tolerance must lie in (0,1)")
    return max(1, math.ceil(math.sqrt(2.0 * math.log(1.0 / tolerance) / t)))


def circle_heat_kernel(theta: float, t: float, tolerance: float = 1e-14) -> float:
    """Evaluate the normalized U(1) heat kernel by its character expansion."""
    cutoff = _fourier_cutoff(t, tolerance)
    terms = [1.0]
    terms.extend(
        2.0 * math.exp(-0.5 * n * n * t) * math.cos(n * theta)
        for n in range(1, cutoff + 1)
    )
    value = math.fsum(terms) / TAU
    # Fourier truncation can produce a negative value at roundoff scale.
    if value < 0.0 and abs(value) < 100.0 * tolerance:
        return 0.0
    return value


def total_variation_translate(
    t: float,
    shift: float,
    grid_size: int = 32768,
    tolerance: float = 1e-14,
) -> float:
    """Trapezoidal total variation between p_t and p_t(. - shift)."""
    if grid_size < 128 or grid_size % 2:
        raise ValueError("grid_size must be an even integer at least 128")
    dx = TAU / grid_size
    l1_terms = []
    for k in range(grid_size):
        theta = -math.pi + (k + 0.5) * dx
        p = circle_heat_kernel(theta, t, tolerance)
        q = circle_heat_kernel(theta - shift, t, tolerance)
        l1_terms.append(abs(p - q))
    tv = 0.5 * dx * math.fsum(l1_terms)
    return min(1.0, max(0.0, tv))


def gaussian_translation_limit(scale: float) -> float:
    """TV limit for N(0,1) and N(scale,1)."""
    return math.erf(abs(scale) / (2.0 * math.sqrt(2.0)))


@dataclass(frozen=True)
class CalibrationRow:
    heat_time: float
    fixed_shift_tv: float
    scaled_shift_tv: float
    scaled_gaussian_limit: float


def calibrate(
    heat_times: Iterable[float],
    fixed_shift: float = math.pi,
    scaled_shift: float = 0.5,
    grid_size: int = 32768,
) -> list[CalibrationRow]:
    rows = []
    limit = gaussian_translation_limit(scaled_shift)
    for t in heat_times:
        rows.append(
            CalibrationRow(
                heat_time=t,
                fixed_shift_tv=total_variation_translate(t, fixed_shift, grid_size),
                scaled_shift_tv=total_variation_translate(
                    t, scaled_shift * math.sqrt(t), grid_size
                ),
                scaled_gaussian_limit=limit,
            )
        )
    return rows


def rows_as_json(rows: list[CalibrationRow]) -> str:
    return json.dumps([row.__dict__ for row in rows], indent=2, sort_keys=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--times", nargs="+", type=float, default=[1.0, 0.5, 0.2, 0.1, 0.05, 0.02]
    )
    parser.add_argument("--grid-size", type=int, default=32768)
    parser.add_argument("--fixed-shift", type=float, default=math.pi)
    parser.add_argument("--scaled-shift", type=float, default=0.5)
    parser.add_argument("--output", choices=("table", "json"), default="table")
    args = parser.parse_args()
    rows = calibrate(args.times, args.fixed_shift, args.scaled_shift, args.grid_size)
    if args.output == "json":
        print(rows_as_json(rows))
        return
    print("t\tTV(fixed shift)\tTV(shift=c sqrt(t))\tGaussian limit")
    for row in rows:
        print(
            f"{row.heat_time:.6g}\t{row.fixed_shift_tv:.9f}\t"
            f"{row.scaled_shift_tv:.9f}\t{row.scaled_gaussian_limit:.9f}"
        )


if __name__ == "__main__":
    main()
