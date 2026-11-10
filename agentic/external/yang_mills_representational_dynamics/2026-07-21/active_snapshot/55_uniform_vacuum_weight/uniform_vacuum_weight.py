"""Finite Perron/Harnack certificates for inverse vacuum weights."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class HarnackCertificate:
    eigenvalue: float
    vacuum_amplitude: list[float]
    inverse_cost_weight: list[float]
    residual: float
    minimum_entry: float
    maximum_entry: float
    actual_amplitude_ratio: float
    entrywise_harnack_bound: float
    bound_holds: bool
    root_moment_upper: float


def _positive_square(matrix: Sequence[Sequence[float]]) -> list[list[float]]:
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("a nonempty square matrix is required")
    out = [[float(x) for x in row] for row in matrix]
    if any((not math.isfinite(x)) or x <= 0.0 for row in out for x in row):
        raise ValueError("the transfer matrix must be entrywise strictly positive")
    return out


def _matvec(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> list[float]:
    return [math.fsum(a * b for a, b in zip(row, vector)) for row in matrix]


def principal_vector(matrix: Sequence[Sequence[float]], tolerance: float = 1e-14) -> tuple[float, list[float], float]:
    matrix = _positive_square(matrix)
    n = len(matrix)
    vector = [1.0 / n] * n
    for _ in range(100000):
        image = _matvec(matrix, vector)
        scale = max(image)
        nxt = [x / scale for x in image]
        if max(abs(a - b) for a, b in zip(nxt, vector)) <= tolerance:
            vector = nxt
            break
        vector = nxt
    else:
        raise ArithmeticError("Perron iteration did not converge")
    image = _matvec(matrix, vector)
    ratios = [a / b for a, b in zip(image, vector)]
    eigenvalue = 0.5 * (min(ratios) + max(ratios))
    residual = max(abs(a - eigenvalue * b) for a, b in zip(image, vector))
    return eigenvalue, vector, residual


def harnack_certificate(matrix: Sequence[Sequence[float]], root_law: Sequence[float] | None = None) -> HarnackCertificate:
    matrix = _positive_square(matrix)
    eigenvalue, psi, residual = principal_vector(matrix)
    maximum_psi = max(psi)
    minimum_psi = min(psi)
    inverse = [maximum_psi / x for x in psi]
    minimum_entry = min(x for row in matrix for x in row)
    maximum_entry = max(x for row in matrix for x in row)
    bound = maximum_entry / minimum_entry
    ratio = maximum_psi / minimum_psi
    if root_law is None:
        root_law = [1.0 / len(matrix)] * len(matrix)
    if len(root_law) != len(matrix) or any(x < 0.0 for x in root_law):
        raise ValueError("root law must be a nonnegative vector of matching size")
    mass = math.fsum(root_law)
    if abs(mass - 1.0) > 1e-12:
        raise ValueError("root law must have unit mass")
    root_moment = math.fsum(p * v for p, v in zip(root_law, inverse))
    return HarnackCertificate(
        eigenvalue=eigenvalue,
        vacuum_amplitude=psi,
        inverse_cost_weight=inverse,
        residual=residual,
        minimum_entry=minimum_entry,
        maximum_entry=maximum_entry,
        actual_amplitude_ratio=ratio,
        entrywise_harnack_bound=bound,
        bound_holds=ratio <= bound * (1.0 + 1e-12),
        root_moment_upper=root_moment,
    )


def doob_kernel(matrix: Sequence[Sequence[float]]) -> dict:
    matrix = _positive_square(matrix)
    eigenvalue, psi, _ = principal_vector(matrix)
    kernel = [
        [matrix[i][j] * psi[j] / (eigenvalue * psi[i]) for j in range(len(matrix))]
        for i in range(len(matrix))
    ]
    return {
        "kernel": kernel,
        "row_error": max(abs(math.fsum(row) - 1.0) for row in kernel),
        "eigenvalue": eigenvalue,
        "vacuum_amplitude": psi,
    }


def two_sector_transfer(level: int) -> list[list[float]]:
    epsilon = math.exp(-float(level))
    return [[1.0, epsilon], [epsilon, 2.0 * epsilon * epsilon]]


def nonuniform_family(max_level: int = 20) -> list[dict]:
    rows = []
    for level in range(1, max_level + 1):
        # Concentrate the hostile root law on the vacuum-suppressed sector.
        cert = harnack_certificate(two_sector_transfer(level), [0.0, 1.0])
        rows.append(
            {
                "level": level,
                "actual_ratio": cert.actual_amplitude_ratio,
                "entrywise_bound": cert.entrywise_harnack_bound,
                "root_moment": cert.root_moment_upper,
            }
        )
    return rows


def inverse_partition_comparison(vacuum: Sequence[float], partition: Sequence[float]) -> dict:
    if len(vacuum) != len(partition) or not vacuum:
        raise ValueError("matching nonempty vectors required")
    if any(x <= 0.0 for x in vacuum) or any(z <= 0.0 for z in partition):
        raise ValueError("vacuum and partition weights must be positive")
    v = [max(vacuum) / x for x in vacuum]
    zinv_raw = [1.0 / z for z in partition]
    zinv = [x / min(zinv_raw) for x in zinv_raw]
    ratios = [a / b for a, b in zip(v, zinv)]
    factor = max(ratios) / min(ratios)
    return {"vacuum_inverse": v, "partition_inverse": zinv, "comparison_factor": factor}


def calibration() -> dict:
    uniform_matrix = [[1.0, 0.2, 0.3], [0.4, 0.8, 0.2], [0.3, 0.25, 0.9]]
    uniform = harnack_certificate(uniform_matrix, [0.2, 0.5, 0.3])
    nonuniform = nonuniform_family()
    comparison = inverse_partition_comparison(uniform.vacuum_amplitude, [1.1, 0.9, 0.7])
    return {
        "stage": 55,
        "target": "uniform vacuum-weight criterion",
        "theorem": {
            "statement": "if 0<m<=T_ij<=M uniformly, then max(psi)/min(psi)<=M/m and every normalized inverse-vacuum root moment is <=M/m",
            "uniform_example": asdict(uniform),
            "doob": doob_kernel(uniform_matrix),
        },
        "nonuniform_counterexample": nonuniform,
        "inverse_partition_diagnostic": comparison,
        "claim_level": "C2 finite Harnack theorem; cutoff-uniform SU(2) minorization open",
        "guardrails": {
            "uniform_physical_minorization": False,
            "uniform_root_moment": False,
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
