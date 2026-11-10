"""Exact finite retained-state disintegration and normalized bad kernels.

This module is deliberately finite.  It implements the algebraic object that
the nonlinear SU(2) analysis must eventually construct uniformly, without
claiming that the finite table is the physical Yang--Mills kernel.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Sequence


TOL = 1.0e-12
Q_TARGET = 0.002430277501841998


@dataclass(frozen=True)
class KernelCertificate:
    transition: List[List[float]]
    bad_kernel: List[List[float]]
    normalizers: List[float]
    row_errors: List[float]
    bad_row_masses: List[float]


def _validate_table(
    weights: Sequence[Sequence[float]],
    next_state: Sequence[Sequence[int]],
    bad: Sequence[Sequence[bool]],
) -> int:
    n = len(weights)
    if n == 0 or len(next_state) != n or len(bad) != n:
        raise ValueError("nonempty state-indexed tables of equal size required")
    for i, (wr, tr, br) in enumerate(zip(weights, next_state, bad)):
        if not wr or len(wr) != len(tr) or len(wr) != len(br):
            raise ValueError(f"row {i} has incompatible fiber tables")
        if any((not math.isfinite(x)) or x <= 0.0 for x in wr):
            raise ValueError("fiber weights must be finite and strictly positive")
        if any(t < 0 or t >= n for t in tr):
            raise ValueError("next-state map leaves the retained state space")
    return n


def build_kernel(
    weights: Sequence[Sequence[float]],
    next_state: Sequence[Sequence[int]],
    bad: Sequence[Sequence[bool]],
) -> KernelCertificate:
    """Push forward each normalized conditional fiber onto retained states."""

    n = _validate_table(weights, next_state, bad)
    transition = [[0.0] * n for _ in range(n)]
    bad_kernel = [[0.0] * n for _ in range(n)]
    normalizers = []
    for i, (wr, tr, br) in enumerate(zip(weights, next_state, bad)):
        z = math.fsum(wr)
        normalizers.append(z)
        for w, j, is_bad in zip(wr, tr, br):
            transition[i][j] += w / z
            if is_bad:
                bad_kernel[i][j] += w / z
    row_errors = [abs(math.fsum(row) - 1.0) for row in transition]
    bad_row_masses = [math.fsum(row) for row in bad_kernel]
    if max(row_errors) > TOL or max(bad_row_masses) > 1.0 + TOL:
        raise ArithmeticError("normalization certificate failed")
    return KernelCertificate(
        transition=transition,
        bad_kernel=bad_kernel,
        normalizers=normalizers,
        row_errors=row_errors,
        bad_row_masses=bad_row_masses,
    )


def weighted_bad_ratios(
    weights: Sequence[Sequence[float]],
    next_state: Sequence[Sequence[int]],
    bad: Sequence[Sequence[bool]],
    state_weight: Sequence[float],
) -> dict:
    cert = build_kernel(weights, next_state, bad)
    if len(state_weight) != len(weights) or any(v < 1.0 for v in state_weight):
        raise ValueError("state weight must have one entry per state and satisfy V>=1")
    kernel_ratios = []
    fiber_ratios = []
    for i, (wr, tr, br) in enumerate(zip(weights, next_state, bad)):
        kernel_ratios.append(
            math.fsum(cert.bad_kernel[i][j] * state_weight[j] for j in range(len(weights)))
            / state_weight[i]
        )
        fiber_ratios.append(
            math.fsum(w * state_weight[j] for w, j, flag in zip(wr, tr, br) if flag)
            / (math.fsum(wr) * state_weight[i])
        )
    return {
        "kernel_ratios": kernel_ratios,
        "fiber_ratios": fiber_ratios,
        "identity_error": max(abs(a - b) for a, b in zip(kernel_ratios, fiber_ratios)),
        "weighted_ceiling": max(kernel_ratios),
    }


def relabel_table(
    weights: Sequence[Sequence[float]],
    next_state: Sequence[Sequence[int]],
    bad: Sequence[Sequence[bool]],
    state_perm: Sequence[int],
    fiber_perms: Sequence[Sequence[int]],
) -> tuple[list[list[float]], list[list[int]], list[list[bool]]]:
    """Transport the disintegration through state/fiber relabelings."""

    n = _validate_table(weights, next_state, bad)
    if sorted(state_perm) != list(range(n)) or len(fiber_perms) != n:
        raise ValueError("invalid state permutation")
    out_w: list[list[float]] = [[] for _ in range(n)]
    out_t: list[list[int]] = [[] for _ in range(n)]
    out_b: list[list[bool]] = [[] for _ in range(n)]
    for i in range(n):
        pf = list(fiber_perms[i])
        if sorted(pf) != list(range(len(weights[i]))):
            raise ValueError("invalid fiber permutation")
        ni = state_perm[i]
        size = len(weights[i])
        out_w[ni] = [0.0] * size
        out_t[ni] = [0] * size
        out_b[ni] = [False] * size
        for f in range(size):
            nf = pf[f]
            out_w[ni][nf] = weights[i][f]
            out_t[ni][nf] = state_perm[next_state[i][f]]
            out_b[ni][nf] = bad[i][f]
    return out_w, out_t, out_b


def covariance_error(original: KernelCertificate, relabeled: KernelCertificate, perm: Sequence[int]) -> float:
    n = len(perm)
    errors = []
    for i in range(n):
        for j in range(n):
            errors.extend(
                [
                    abs(original.transition[i][j] - relabeled.transition[perm[i]][perm[j]]),
                    abs(original.bad_kernel[i][j] - relabeled.bad_kernel[perm[i]][perm[j]]),
                ]
            )
    return max(errors, default=0.0)


def four_channel_disintegration(q: float = Q_TARGET) -> tuple[list, list, list, list]:
    """Exact normalized finite realization of the Stage-53 star subkernel."""

    if not 0.0 < q < 1.0:
        raise ValueError("q must lie in (0,1)")
    k = 4
    entry = q * q / k
    weights = [[1.0 - q * q] + [entry] * k]
    next_state = [[0, 1, 2, 3, 4]]
    bad = [[False, True, True, True, True]]
    for _ in range(k):
        weights.append([1.0])
        next_state.append([0])
        bad.append([True])
    state_weight = [1.0] + [1.0 / q] * k
    return weights, next_state, bad, state_weight


def collapsed_normalizer_counterexample(max_level: int = 12) -> list[dict]:
    """Both absolute pieces vanish while the normalized bad row tends to one."""

    rows = []
    for level in range(1, max_level + 1):
        z_good = math.exp(-2.0 * level)
        z_bad = math.exp(-1.0 * level)
        rows.append(
            {
                "level": level,
                "good_weight": z_good,
                "bad_weight": z_bad,
                "normalizer": z_good + z_bad,
                "bad_probability": z_bad / (z_good + z_bad),
            }
        )
    return rows


def calibration() -> dict:
    weights, next_state, bad, state_weight = four_channel_disintegration()
    cert = build_kernel(weights, next_state, bad)
    ratios = weighted_bad_ratios(weights, next_state, bad, state_weight)
    state_perm = [0, 3, 4, 1, 2]
    fiber_perms = [[0, 3, 4, 1, 2], [0], [0], [0], [0]]
    rw, rt, rb = relabel_table(weights, next_state, bad, state_perm, fiber_perms)
    relabeled = build_kernel(rw, rt, rb)
    collapse = collapsed_normalizer_counterexample()
    return {
        "stage": 54,
        "target": "exact normalized retained-kernel interface",
        "four_channel": {
            "certificate": asdict(cert),
            "state_weight": state_weight,
            "weighted_identity": ratios,
            "covariance_error": covariance_error(cert, relabeled, state_perm),
        },
        "normalizer_counterexample": collapse,
        "claim_level": "C2 finite normalized-kernel theorem; physical nonlinear SU(2) row open",
        "guardrails": {
            "physical_su2_kernel": False,
            "uniform_boundary_estimate": False,
            "basin_entry": False,
            "mass_gap": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    result = calibration()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        args.write.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
