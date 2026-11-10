"""Conservative basin/OS audit after the five-target H1 run."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


Q_TARGET = 0.002430277501841998
Q_CRITICAL = 0.0027927080803578997


@dataclass(frozen=True)
class FrontierGates:
    physical_normalized_kernel: bool
    uniform_vacuum_or_lyapunov_weight: bool
    complete_multichannel_weighted_ceiling: bool
    physical_length_rg_contraction: bool
    continuum_os_construction: bool
    observable_core_density: bool
    pure_yang_mills_identity: bool
    every_compact_simple_group: bool


def temporal_transfer(epsilon: float) -> list[list[float]]:
    """Positive symmetric transfer with eigenvalues 1 and exp(-epsilon)."""
    if not math.isfinite(epsilon) or epsilon <= 0.0:
        raise ValueError("epsilon must be finite and positive")
    r = math.exp(-epsilon)
    return [[0.5 * (1.0 + r), 0.5 * (1.0 - r)], [0.5 * (1.0 - r), 0.5 * (1.0 + r)]]


def eigenvalues_symmetric_two(matrix: list[list[float]]) -> tuple[float, float]:
    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        raise ValueError("two by two matrix required")
    a, b = matrix[0]
    c, d = matrix[1]
    if abs(b - c) > 1e-12:
        raise ValueError("symmetric matrix required")
    trace = a + d
    disc = math.sqrt((a - d) ** 2 + 4.0 * b * b)
    return 0.5 * (trace + disc), 0.5 * (trace - disc)


def temporal_gap(epsilon: float, time_step: float = 1.0) -> float:
    if not math.isfinite(time_step) or time_step <= 0.0:
        raise ValueError("time step must be finite and positive")
    top, second = eigenvalues_symmetric_two(temporal_transfer(epsilon))
    return -math.log(second / top) / time_step


def one_scale_independence_counterexample(epsilons: list[float] | None = None) -> list[dict]:
    if epsilons is None:
        epsilons = [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]
    return [
        {
            "spatial_weighted_ceiling": Q_TARGET,
            "temporal_epsilon": epsilon,
            "temporal_gap": temporal_gap(epsilon),
        }
        for epsilon in epsilons
    ]


def cutoff_gap_collapse(levels: int = 12) -> list[dict]:
    """Every regulator has a gap, while the physical gap epsilon(a)/a vanishes."""
    rows = []
    for n in range(1, levels + 1):
        cutoff = 2.0 ** (-n)
        epsilon = cutoff * cutoff
        rows.append(
            {
                "level": n,
                "time_step": cutoff,
                "transfer_epsilon": epsilon,
                "regulated_gap": temporal_gap(epsilon, cutoff),
                "spatial_weighted_ceiling": Q_TARGET,
            }
        )
    return rows


def audit_claim_level(gates: FrontierGates) -> dict:
    values = asdict(gates)
    ordered = list(values.items())
    first_failure = next((name for name, value in ordered if not value), None)
    if all(values.values()):
        level = "C6"
    elif all(
        [
            gates.physical_normalized_kernel,
            gates.uniform_vacuum_or_lyapunov_weight,
            gates.complete_multichannel_weighted_ceiling,
            gates.physical_length_rg_contraction,
            gates.continuum_os_construction,
            gates.observable_core_density,
            gates.pure_yang_mills_identity,
        ]
    ):
        level = "C5"
    elif all(
        [
            gates.physical_normalized_kernel,
            gates.uniform_vacuum_or_lyapunov_weight,
            gates.complete_multichannel_weighted_ceiling,
            gates.physical_length_rg_contraction,
        ]
    ):
        level = "C4"
    elif gates.physical_normalized_kernel and gates.uniform_vacuum_or_lyapunov_weight:
        level = "C3"
    else:
        level = "C2"
    return {"claim_level": level, "first_failure": first_failure, "gates": values}


def os_gap_handoff(mass: float, continuum_os: bool, dense_core_decay: bool, theory_identity: bool) -> dict:
    if mass <= 0.0:
        raise ValueError("mass must be positive")
    premises = {
        "continuum_os": continuum_os,
        "dense_core_temporal_decay": dense_core_decay,
        "pure_yang_mills_identity": theory_identity,
    }
    return {
        "premises": premises,
        "conditional_gap_lower": mass if all(premises.values()) else None,
        "proved": all(premises.values()),
    }


def calibration() -> dict:
    actual = FrontierGates(False, False, False, False, False, False, False, False)
    finite_run = {
        "target54_normalized_finite_kernel": True,
        "target55_finite_harnack_criterion": True,
        "target56_robust_perron_envelope": True,
        "target57_weight_cocycle": True,
        "target58_temporal_countermodel": True,
    }
    return {
        "stage": 58,
        "target": "basin-entry and OS frontier audit",
        "five_target_finite_results": finite_run,
        "physical_audit": audit_claim_level(actual),
        "one_scale_temporal_independence": one_scale_independence_counterexample(),
        "cutoff_gap_collapse": cutoff_gap_collapse(),
        "conditional_os_handoff": os_gap_handoff(0.4, False, False, False),
        "limit_order": [
            "construct every finite-volume normalized row",
            "prove volume-uniform thermodynamic control",
            "prove cutoff-uniform physical-length contraction",
            "construct the OS continuum theory and identify pure Yang--Mills",
            "establish density of the decaying observable core",
            "apply the spectral-measure gap implication",
        ],
        "first_open_physical_implication": "complete boundary-uniform nonlinear SU(2) normalized kernel and root-weight moment",
        "claim_level": "C2 finite theorem suite with C3 conditional bridges",
        "guardrails": {
            "physical_basin_entry": False,
            "continuum_yang_mills": False,
            "os_reconstruction": False,
            "hamiltonian_mass_gap": False,
            "clay_problem": False,
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
