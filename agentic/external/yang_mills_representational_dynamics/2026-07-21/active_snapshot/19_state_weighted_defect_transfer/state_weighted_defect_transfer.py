"""State-weighted bad-transition bounds for dependent block explorations.

This module checks the finite algebra behind Stage 19.  It neither constructs
the nonlinear Yang--Mills kernel nor asserts continuum control.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from typing import Iterable, Sequence

import numpy as np


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


@dataclass(frozen=True)
class WeightedKernelCertificate:
    weighted_ceiling: float
    scalar_row_ceiling: float
    spectral_radius: float
    weight_min: float
    weight_max: float
    certified: bool

    def to_dict(self) -> dict[str, float | bool]:
        return asdict(self)


@dataclass(frozen=True)
class ClusterCertificate:
    q: float
    degree: int
    alpha: float
    root_weight_moment: float
    branching_ratio: float
    rooted_sum_upper: float
    subcritical: bool

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


def validate_bad_kernel(matrix: Sequence[Sequence[float]]) -> np.ndarray:
    q = np.asarray(matrix, dtype=float)
    if q.ndim != 2 or q.shape[0] != q.shape[1] or q.shape[0] == 0:
        raise ValueError("bad kernel must be a nonempty square matrix")
    if not np.all(np.isfinite(q)) or np.any(q < 0.0):
        raise ValueError("bad kernel must be finite and nonnegative")
    if np.any(np.sum(q, axis=1) > 1.0 + 1e-12):
        raise ValueError("each bad-subkernel row must have mass at most one")
    return q


def weighted_kernel_certificate(
    matrix: Sequence[Sequence[float]], weight: Sequence[float]
) -> WeightedKernelCertificate:
    q = validate_bad_kernel(matrix)
    v = np.asarray(weight, dtype=float)
    if v.shape != (q.shape[0],) or not np.all(np.isfinite(v)) or np.any(v <= 0.0):
        raise ValueError("weight must be a finite positive vector of matching size")
    ratios = (q @ v) / v
    eigenvalues = np.linalg.eigvals(q)
    spectral = float(np.max(np.abs(eigenvalues)))
    ceiling = float(np.max(ratios))
    return WeightedKernelCertificate(
        weighted_ceiling=ceiling,
        scalar_row_ceiling=float(np.max(np.sum(q, axis=1))),
        spectral_radius=spectral,
        weight_min=float(np.min(v)),
        weight_max=float(np.max(v)),
        certified=bool(ceiling <= 1.0 + 1e-12),
    )


def bad_chain_probability_upper(
    root_weight_moment: float, weighted_ceiling: float, length: int
) -> float:
    moment = _positive("root_weight_moment", root_weight_moment)
    q = _positive("weighted_ceiling", weighted_ceiling)
    if not isinstance(length, int) or length < 1:
        raise ValueError("length must be a positive integer")
    return min(1.0, moment * q**length)


def rooted_connected_set_count_upper(degree: int, size: int) -> int:
    if not isinstance(degree, int) or degree < 1:
        raise ValueError("degree must be a positive integer")
    if not isinstance(size, int) or size < 1:
        raise ValueError("size must be a positive integer")
    return degree ** (2 * (size - 1))


def cluster_certificate(
    q: float, degree: int, alpha: float, root_weight_moment: float = 1.0
) -> ClusterCertificate:
    q = _positive("q", q)
    moment = _positive("root_weight_moment", root_weight_moment)
    if q > 1.0:
        raise ValueError("q must not exceed one")
    if not isinstance(degree, int) or degree < 1:
        raise ValueError("degree must be a positive integer")
    alpha = float(alpha)
    if not math.isfinite(alpha):
        raise ValueError("alpha must be finite")
    ratio = math.exp(alpha) * degree**2 * q
    # The theorem requires a strict margin.  Treat a floating-point value at
    # the analytic boundary as critical rather than accepting roundoff below
    # one as a certificate.
    subcritical = ratio < 1.0 - 1e-14
    rooted = math.inf
    if subcritical:
        rooted = moment * math.exp(alpha) * q / (1.0 - ratio)
    return ClusterCertificate(
        q=q,
        degree=degree,
        alpha=alpha,
        root_weight_moment=moment,
        branching_ratio=ratio,
        rooted_sum_upper=rooted,
        subcritical=subcritical,
    )


def alternating_cost_kernel(q: float) -> tuple[np.ndarray, np.ndarray]:
    """Kernel with scalar ceiling one and optimal weighted ceiling q.

    A low-cost state enters a high-cost state with probability q^2; once in
    the high-cost state, the next bad transition is forced.  The weight
    V=(1,1/q) accounts for the cost stored in the second state.
    """

    q = _positive("q", q)
    if q > 1.0:
        raise ValueError("q must not exceed one")
    return np.array([[0.0, q * q], [1.0, 0.0]]), np.array([1.0, 1.0 / q])


def moment_only_counterexample() -> dict[str, float | bool]:
    # P(10)=P(01)=1/2.
    return {
        "q": 0.5,
        "p_x1": 0.5,
        "p_x2": 0.5,
        "p_both": 0.0,
        "p_union": 1.0,
        "bernoulli_union": 0.75,
        "max_positive_history_conditional": 1.0,
        "intersection_moments_hold": True,
        "bernoulli_domination_holds": False,
    }


def is_connected_subset(adjacency: Sequence[Sequence[int]], subset: Iterable[int]) -> bool:
    vertices = set(subset)
    if not vertices:
        return False
    start = next(iter(vertices))
    seen = {start}
    stack = [start]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex]:
            if neighbor in vertices and neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return seen == vertices


def calibration() -> dict[str, object]:
    q_target = 0.002430277501841998
    critical = 0.0027927080803578997
    kernel, weight = alternating_cost_kernel(q_target)
    kernel_cert = weighted_kernel_certificate(kernel, weight)
    cluster = cluster_certificate(q_target, degree=18, alpha=0.1)
    return {
        "claim_level": "C2 abstract weighted-transfer theorem and finite calibration",
        "target_weighted_ceiling": q_target,
        "critical_weight": critical,
        "free_energy_threshold": -math.log(critical),
        "alternating_kernel": kernel.tolist(),
        "alternating_weight": weight.tolist(),
        "kernel_certificate": kernel_cert.to_dict(),
        "cluster_certificate": cluster.to_dict(),
        "moment_only_counterexample": moment_only_counterexample(),
        "full_su2_kernel_constructed": False,
        "continuum_claim": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
