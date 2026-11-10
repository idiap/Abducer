"""State-weight cocycles and their physical-length interpretation."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Sequence


Q_TARGET = 0.002430277501841998


@dataclass(frozen=True)
class CocycleCertificate:
    step_ceilings: list[float]
    product_ceiling: float
    root_moment: float
    exact_chain_mass: float
    probability_bound: float
    bound_holds: bool


def _validate_kernel(kernel: Sequence[Sequence[float]], n_in: int, n_out: int) -> list[list[float]]:
    if len(kernel) != n_in or any(len(row) != n_out for row in kernel):
        raise ValueError("kernel dimensions do not match adjacent state spaces")
    out = [[float(x) for x in row] for row in kernel]
    if any((not math.isfinite(x)) or x < 0.0 for row in out for x in row):
        raise ValueError("kernel entries must be finite and nonnegative")
    if any(math.fsum(row) > 1.0 + 1e-12 for row in out):
        raise ValueError("each kernel row must be subprobability")
    return out


def _matvec(kernel: Sequence[Sequence[float]], vector: Sequence[float]) -> list[float]:
    return [math.fsum(a * b for a, b in zip(row, vector)) for row in kernel]


def _row_push(law: Sequence[float], kernel: Sequence[Sequence[float]]) -> list[float]:
    return [math.fsum(law[i] * kernel[i][j] for i in range(len(law))) for j in range(len(kernel[0]))]


def cocycle_certificate(
    kernels: Sequence[Sequence[Sequence[float]]],
    weights: Sequence[Sequence[float]],
    root_law: Sequence[float],
) -> CocycleCertificate:
    """Prove Q_n V_{n+1} <= q_n V_n and compose the inequalities."""

    if len(weights) != len(kernels) + 1 or not weights:
        raise ValueError("one more weight than kernels is required")
    if any(any((not math.isfinite(x)) or x < 1.0 for x in weight) for weight in weights):
        raise ValueError("every cocycle weight must satisfy V>=1")
    if len(root_law) != len(weights[0]) or any(x < 0.0 for x in root_law):
        raise ValueError("invalid root law")
    if abs(math.fsum(root_law) - 1.0) > 1e-12:
        raise ValueError("root law must have unit mass")
    ceilings = []
    validated = []
    for index, kernel in enumerate(kernels):
        k = _validate_kernel(kernel, len(weights[index]), len(weights[index + 1]))
        validated.append(k)
        image = _matvec(k, weights[index + 1])
        ceilings.append(max(a / b for a, b in zip(image, weights[index])))
    product = math.prod(ceilings)
    root_moment = math.fsum(p * v for p, v in zip(root_law, weights[0]))
    law = list(root_law)
    for kernel in validated:
        law = _row_push(law, kernel)
    exact_mass = math.fsum(law)
    bound = root_moment * product
    return CocycleCertificate(
        step_ceilings=ceilings,
        product_ceiling=product,
        root_moment=root_moment,
        exact_chain_mass=exact_mass,
        probability_bound=bound,
        bound_holds=exact_mass <= bound * (1.0 + 1e-12),
    )


def two_state_kernel(q: float) -> list[list[float]]:
    if not 0.0 < q < 1.0:
        raise ValueError("q must be in (0,1)")
    return [[0.0, q * q], [1.0, 0.0]]


def two_state_weight(q: float) -> list[float]:
    return [1.0, 1.0 / q]


def physical_length_certificate(step_ceilings: Sequence[float], length_increments: Sequence[float]) -> dict:
    if len(step_ceilings) != len(length_increments) or not step_ceilings:
        raise ValueError("matching nonempty ceiling and length sequences required")
    if any(not 0.0 < q < 1.0 for q in step_ceilings):
        raise ValueError("ceilings must lie strictly between zero and one")
    if any((not math.isfinite(x)) or x <= 0.0 for x in length_increments):
        raise ValueError("physical increments must be finite and positive")
    log_contraction = -math.fsum(math.log(q) for q in step_ceilings)
    length = math.fsum(length_increments)
    return {
        "total_length": length,
        "product_ceiling": math.prod(step_ceilings),
        "effective_mass": log_contraction / length,
        "log_contraction": log_contraction,
    }


def geometric_level_counterexample(levels: int = 20, block_factor: float = 2.0, q: float = Q_TARGET) -> dict:
    increments = [block_factor**n for n in range(levels)]
    certs = [physical_length_certificate([q] * n, increments[:n]) for n in range(1, levels + 1)]
    return {
        "block_factor": block_factor,
        "constant_level_ceiling": q,
        "power_law_exponent": -math.log(q) / math.log(block_factor),
        "certificates": certs,
        "last_effective_mass": certs[-1]["effective_mass"],
        "lesson": "constant contraction per geometric RG level is power-law in terminal physical scale, not exponential in physical distance",
    }


def mass_scaled_cocycle(levels: int = 10, mass: float = 0.4, block_factor: float = 2.0) -> dict:
    # Ten levels keep exp(-m ell_n) above floating-point underflow.  The
    # theorem itself is the log-domain identity used by
    # physical_length_certificate, not this finite display choice.
    increments = [block_factor**n for n in range(levels)]
    ceilings = [math.exp(-mass * length) for length in increments]
    cert = physical_length_certificate(ceilings, increments)
    cert["declared_mass"] = mass
    cert["mass_error"] = abs(cert["effective_mass"] - mass)
    return cert


def calibration() -> dict:
    kernels = [two_state_kernel(Q_TARGET)] * 6
    weights = [two_state_weight(Q_TARGET)] * 7
    finite = cocycle_certificate(kernels, weights, [1.0, 0.0])
    return {
        "stage": 57,
        "target": "state-weight cocycle and physical-length criterion",
        "finite_cocycle": asdict(finite),
        "geometric_level_counterexample": geometric_level_counterexample(),
        "mass_scaled_cocycle": mass_scaled_cocycle(),
        "theorem": "Q_n V_{n+1}<=q_n V_n composes with product q_n; a physical mass m additionally requires product q_n<=exp(-m sum ell_n)",
        "claim_level": "C2 finite cocycle plus C3 conditional physical-length criterion",
        "guardrails": {
            "physical_rg_kernels": False,
            "uniform_length_scaled_contraction": False,
            "continuum_os": False,
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
