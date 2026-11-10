"""Robust Perron envelopes for multichannel retained-state kernels."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


Q_TARGET = 0.002430277501841998
Q_CRITICAL = 0.0027927080803578997


@dataclass(frozen=True)
class RobustCertificate:
    spectral_radius: float
    perron_weight: list[float]
    eigen_residual: float
    weighted_ceiling: float
    strict_subcritical: bool


def _validate(matrix: Sequence[Sequence[float]]) -> list[list[float]]:
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("nonempty square matrix required")
    out = [[float(x) for x in row] for row in matrix]
    if any((not math.isfinite(x)) or x < 0.0 for row in out for x in row):
        raise ValueError("kernel entries must be finite and nonnegative")
    if any(math.fsum(row) > 1.0 + 1e-12 for row in out):
        raise ValueError("bad kernel must be substochastic")
    return out


def _matvec(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> list[float]:
    return [math.fsum(a * b for a, b in zip(row, vector)) for row in matrix]


def perron_certificate(matrix: Sequence[Sequence[float]]) -> RobustCertificate:
    matrix = _validate(matrix)
    n = len(matrix)
    shift = 1.0
    shifted = [[matrix[i][j] + (shift if i == j else 0.0) for j in range(n)] for i in range(n)]
    vector = [1.0] * n
    for _ in range(200000):
        image = _matvec(shifted, vector)
        scale = max(image)
        nxt = [x / scale for x in image]
        if max(abs(a - b) for a, b in zip(nxt, vector)) < 1e-14:
            vector = nxt
            break
        vector = nxt
    else:
        raise ArithmeticError("shifted Perron iteration did not converge")
    image = _matvec(matrix, vector)
    ratios = [a / b for a, b in zip(image, vector)]
    radius = 0.5 * (min(ratios) + max(ratios))
    residual = max(abs(a - radius * b) for a, b in zip(image, vector))
    normalized = [x / min(vector) for x in vector]
    weighted = max(a / b for a, b in zip(_matvec(matrix, normalized), normalized))
    return RobustCertificate(
        spectral_radius=radius,
        perron_weight=normalized,
        eigen_residual=residual,
        weighted_ceiling=weighted,
        strict_subcritical=weighted < Q_CRITICAL,
    )


def star_envelope(q: float = Q_TARGET, channels: int = 4, persistence: float = 0.0, cross_total: float = 0.0) -> list[list[float]]:
    if not 0.0 < q < 1.0 or channels < 2 or persistence < 0.0 or cross_total < 0.0:
        raise ValueError("invalid star parameters")
    size = channels + 1
    matrix = [[0.0] * size for _ in range(size)]
    for a in range(1, size):
        matrix[0][a] = q * q / channels
        matrix[a][0] = 1.0 - persistence - cross_total
        matrix[a][a] = persistence
        for b in range(1, size):
            if b != a:
                matrix[a][b] = cross_total / (channels - 1)
    return _validate(matrix)


def symmetric_radius(q: float, persistence: float = 0.0, cross_total: float = 0.0) -> float:
    s = persistence + cross_total
    return 0.5 * (s + math.sqrt(s * s + 4.0 * q * q * (1.0 - s)))


def envelope_dominates(candidate: Sequence[Sequence[float]], envelope: Sequence[Sequence[float]]) -> bool:
    candidate = _validate(candidate)
    envelope = _validate(envelope)
    return len(candidate) == len(envelope) and all(
        candidate[i][j] <= envelope[i][j] + 1e-15
        for i in range(len(candidate))
        for j in range(len(candidate))
    )


def weighted_ceiling(matrix: Sequence[Sequence[float]], weight: Sequence[float]) -> float:
    matrix = _validate(matrix)
    if len(weight) != len(matrix) or any(x <= 0.0 for x in weight):
        raise ValueError("strictly positive matching weight required")
    return max(a / b for a, b in zip(_matvec(matrix, weight), weight))


def dominated_kernel_certificate(candidate: Sequence[Sequence[float]], envelope: Sequence[Sequence[float]]) -> dict:
    cert = perron_certificate(envelope)
    dominated = envelope_dominates(candidate, envelope)
    candidate_ceiling = weighted_ceiling(candidate, cert.perron_weight)
    return {
        "dominated": dominated,
        "envelope_radius": cert.spectral_radius,
        "candidate_weighted_ceiling": candidate_ceiling,
        "bound_holds": dominated and candidate_ceiling <= cert.weighted_ceiling + 1e-12,
    }


def persistence_budget(q: float = Q_TARGET, q_critical: float = Q_CRITICAL) -> float:
    """Maximum total charged-to-charged mass in the row-stochastic star family."""
    return (q_critical * q_critical - q * q) / (q_critical - q * q)


def calibration() -> dict:
    base = star_envelope()
    base_cert = perron_certificate(base)
    multiplicative_slack = Q_CRITICAL / Q_TARGET - 1.0
    additive_weighted_slack = Q_CRITICAL - Q_TARGET
    persistence_slack = persistence_budget()
    half = star_envelope(persistence=0.5 * persistence_slack)
    half_cert = perron_certificate(half)
    candidate = [[0.9 * x for x in row] for row in half]
    robust = dominated_kernel_certificate(candidate, half)
    return {
        "stage": 56,
        "target": "robust multichannel Perron closure",
        "base": asdict(base_cert),
        "slack": {
            "multiplicative_relative": multiplicative_slack,
            "additive_weighted": additive_weighted_slack,
            "total_persistence_or_cross_mass": persistence_slack,
        },
        "half_persistence": {
            "declared": 0.5 * persistence_slack,
            "closed_form_radius": symmetric_radius(Q_TARGET, 0.5 * persistence_slack),
            "certificate": asdict(half_cert),
        },
        "dominated_candidate": robust,
        "theorem": "entrywise Q<=B and B V=rho(B)V imply QV<=rho(B)V",
        "claim_level": "C2 robust finite multichannel theorem; physical channel envelopes open",
        "guardrails": {
            "physical_channel_rows": False,
            "uniform_topology_control": False,
            "basin_entry": False,
            "mass_gap": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    payload = json.dumps(calibration(), indent=2, sort_keys=True) + "\n"
    if args.write:
        args.write.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
