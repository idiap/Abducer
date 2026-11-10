"""End-to-end finite and conditional development of H1.

H1 concerns the relation among a positive transfer amplitude T, its vacuum
eigenfunction psi, the Doob-normalized state dynamics P, and a forward
rare-state Lyapunov weight V.  The key convention is that P uses psi whereas
the forward cost weight is naturally V=1/psi.  The module also proves the
Perron optimality of the existing multichannel star weight and composes it
with the rooted connected-cluster threshold.

No function constructs the nonlinear Yang--Mills retained-state kernel.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
from typing import Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "h1_vacuum_weight_results.json"


def _matrix(name: str, values: Sequence[Sequence[float]]) -> np.ndarray:
    matrix = np.asarray(values, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or matrix.shape[0] == 0:
        raise ValueError(f"{name} must be a nonempty square matrix")
    if not np.all(np.isfinite(matrix)):
        raise ValueError(f"{name} must be finite")
    return matrix


def _positive_vector(name: str, values: Sequence[float], size: int) -> np.ndarray:
    vector = np.asarray(values, dtype=float)
    if vector.shape != (size,) or not np.all(np.isfinite(vector)) or np.any(vector <= 0.0):
        raise ValueError(f"{name} must be a strictly positive vector of matching size")
    return vector


@dataclass(frozen=True)
class PerronCertificate:
    states: int
    spectral_radius: float
    weighted_ceiling: float
    weighted_floor: float
    scalar_row_ceiling: float
    eigen_residual: float
    collatz_gap: float
    positive_weight: bool
    optimal_within_positive_weights: bool

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


@dataclass(frozen=True)
class DoobCertificate:
    states: int
    principal_eigenvalue: float
    minimum_transfer_eigenvalue: float
    transfer_symmetric: bool
    vacuum_minimum: float
    vacuum_maximum: float
    row_sum_error: float
    minimum_transition: float
    stationarity_error: float
    detailed_balance_error: float
    inverse_amplitude_identity_error: float
    inverse_amplitude_weight_minimum: float
    inverse_amplitude_weight_maximum: float
    vacuum_weighted_bad_ceiling: float
    scalar_bad_probability_ceiling: float

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


@dataclass(frozen=True)
class ClusterCertificate:
    q: float
    degree: int
    alpha: float
    root_moment: float
    branching_ratio: float
    rooted_sum_upper: float
    strict_subcritical: bool

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


def perron_right(matrix: Sequence[Sequence[float]], root: int = 0) -> tuple[float, np.ndarray]:
    q = _matrix("kernel", matrix)
    if np.any(q < 0.0):
        raise ValueError("Perron kernel must be nonnegative")
    eigenvalues, eigenvectors = np.linalg.eig(q)
    # The Perron root is the largest real eigenvalue.  This selects +rho for
    # periodic kernels that also have -rho.
    index = int(np.argmax(eigenvalues.real))
    rho = float(eigenvalues[index].real)
    if abs(eigenvalues[index].imag) > 1.0e-10 or rho <= 0.0:
        raise ValueError("kernel has no usable positive Perron root")
    vector = np.asarray(eigenvectors[:, index].real)
    if vector[root] < 0.0:
        vector = -vector
    if np.any(vector <= 1.0e-13):
        raise ValueError("kernel does not have a strictly positive Perron vector")
    vector = vector / vector[root]
    return rho, vector


def perron_certificate(
    matrix: Sequence[Sequence[float]], weight: Sequence[float] | None = None
) -> tuple[np.ndarray, PerronCertificate]:
    q = _matrix("kernel", matrix)
    if np.any(q < 0.0):
        raise ValueError("kernel must be nonnegative")
    if np.any(np.sum(q, axis=1) > 1.0 + 1.0e-12):
        raise ValueError("bad subkernel rows must have mass at most one")
    rho, perron = perron_right(q)
    vector = perron if weight is None else _positive_vector("weight", weight, len(q))
    ratios = q @ vector / vector
    residual = float(np.linalg.norm(q @ perron - rho * perron, ord=np.inf))
    ceiling = float(np.max(ratios))
    floor = float(np.min(ratios))
    return perron, PerronCertificate(
        states=len(q),
        spectral_radius=rho,
        weighted_ceiling=ceiling,
        weighted_floor=floor,
        scalar_row_ceiling=float(np.max(np.sum(q, axis=1))),
        eigen_residual=residual,
        collatz_gap=ceiling - rho,
        positive_weight=bool(np.all(vector > 0.0)),
        optimal_within_positive_weights=bool(abs(ceiling - rho) < 1.0e-11),
    )


def principal_transfer_data(
    transfer: Sequence[Sequence[float]], root: int = 0
) -> tuple[float, np.ndarray, np.ndarray]:
    t = _matrix("transfer", transfer)
    if np.any(t < 0.0):
        raise ValueError("transfer entries must be nonnegative")
    values, right_vectors = np.linalg.eig(t)
    index = int(np.argmax(values.real))
    lam = float(values[index].real)
    if abs(values[index].imag) > 1.0e-10 or lam <= 0.0:
        raise ValueError("transfer has no positive principal eigenvalue")
    right = np.asarray(right_vectors[:, index].real)
    if right[root] < 0.0:
        right = -right
    if np.any(right <= 1.0e-13):
        raise ValueError("transfer vacuum is not strictly positive")
    right /= np.max(right)

    left_values, left_vectors = np.linalg.eig(t.T)
    left_index = int(np.argmin(np.abs(left_values - lam)))
    left = np.asarray(left_vectors[:, left_index].real)
    if float(np.dot(left, right)) < 0.0:
        left = -left
    if np.any(left <= 1.0e-13):
        raise ValueError("transfer left vacuum is not strictly positive")
    left /= float(np.dot(left, right))
    return lam, right, left


def doob_transform(
    transfer: Sequence[Sequence[float]], mask: Sequence[Sequence[float]]
) -> dict[str, object]:
    """Construct the vacuum Doob dynamics and forward inverse-amplitude bound.

    With P_ij=T_ij psi_j/(lambda psi_i), V_i=1/psi_i and a bad edge mask M,

        ((M*P)V)_i/V_i = sum_j M_ij T_ij/lambda.

    Thus the forward cost tilt cancels the vacuum-amplitude ratios exactly.
    """
    t = _matrix("transfer", transfer)
    m = _matrix("mask", mask)
    if m.shape != t.shape or np.any(m < 0.0) or np.any(m > 1.0):
        raise ValueError("mask must match the transfer and lie in [0,1]")
    lam, psi, left = principal_transfer_data(t)
    p = t * psi[None, :] / (lam * psi[:, None])
    stationary = left * psi
    stationary /= np.sum(stationary)
    bad = m * p
    inverse = 1.0 / psi
    inverse /= np.min(inverse)
    weighted_ratios = bad @ inverse / inverse
    amplitude_rows = np.sum(m * t, axis=1) / lam
    detailed = stationary[:, None] * p - stationary[None, :] * p.T
    symmetric = bool(np.allclose(t, t.T, atol=1.0e-13))
    if symmetric:
        eigen_min = float(np.linalg.eigvalsh(t)[0])
    else:
        eigen_min = float("nan")
    certificate = DoobCertificate(
        states=len(t),
        principal_eigenvalue=lam,
        minimum_transfer_eigenvalue=eigen_min,
        transfer_symmetric=symmetric,
        vacuum_minimum=float(np.min(psi)),
        vacuum_maximum=float(np.max(psi)),
        row_sum_error=float(np.max(np.abs(np.sum(p, axis=1) - 1.0))),
        minimum_transition=float(np.min(p)),
        stationarity_error=float(np.max(np.abs(stationary @ p - stationary))),
        detailed_balance_error=float(np.max(np.abs(detailed))),
        inverse_amplitude_identity_error=float(np.max(np.abs(weighted_ratios - amplitude_rows))),
        inverse_amplitude_weight_minimum=float(np.min(inverse)),
        inverse_amplitude_weight_maximum=float(np.max(inverse)),
        vacuum_weighted_bad_ceiling=float(np.max(weighted_ratios)),
        scalar_bad_probability_ceiling=float(np.max(np.sum(bad, axis=1))),
    )
    return {
        "transfer": t.tolist(),
        "mask": m.tolist(),
        "principal_eigenvalue": lam,
        "vacuum_amplitude": psi.tolist(),
        "left_vacuum": left.tolist(),
        "stationary_state": stationary.tolist(),
        "doob_kernel": p.tolist(),
        "bad_subkernel": bad.tolist(),
        "forward_cost_weight": inverse.tolist(),
        "weighted_bad_ratios": weighted_ratios.tolist(),
        "normalized_transfer_amplitude_rows": amplitude_rows.tolist(),
        "certificate": certificate.to_dict(),
    }


def two_sector_transfer(epsilon: float) -> tuple[np.ndarray, np.ndarray]:
    e = float(epsilon)
    if not math.isfinite(e) or not 0.0 < e < 1.0 / math.sqrt(2.0):
        raise ValueError("epsilon must lie in (0,1/sqrt(2))")
    # Positive-definite symmetric transfer amplitude.  Sector 1 has vacuum
    # amplitude of order epsilon.
    transfer = np.array([[1.0, e], [e, 2.0 * e * e]])
    # A bad extension is a next boundary state in the rare sector.
    mask = np.array([[0.0, 1.0], [0.0, 1.0]])
    return transfer, mask


def multichannel_star_kernel(q: float, channels: int = 4) -> tuple[np.ndarray, np.ndarray]:
    q = float(q)
    if not math.isfinite(q) or not 0.0 < q < 1.0:
        raise ValueError("q must lie in (0,1)")
    if not isinstance(channels, int) or channels < 1:
        raise ValueError("channels must be a positive integer")
    matrix = np.zeros((channels + 1, channels + 1))
    matrix[0, 1:] = q * q / channels
    matrix[1:, 0] = 1.0
    weight = np.concatenate(([1.0], np.full(channels, 1.0 / q)))
    return matrix, weight


def cluster_certificate(
    q: float, degree: int, alpha: float, root_moment: float = 1.0
) -> ClusterCertificate:
    q = float(q)
    alpha = float(alpha)
    moment = float(root_moment)
    if not 0.0 < q <= 1.0 or not isinstance(degree, int) or degree < 1:
        raise ValueError("invalid cluster parameters")
    if not math.isfinite(alpha) or not math.isfinite(moment) or moment <= 0.0:
        raise ValueError("invalid alpha or root moment")
    ratio = math.exp(alpha) * degree * degree * q
    strict = ratio < 1.0 - 1.0e-14
    rooted = math.inf if not strict else moment * math.exp(alpha) * q / (1.0 - ratio)
    return ClusterCertificate(q, degree, alpha, moment, ratio, rooted, strict)


def chain_certificate(
    kernel: Sequence[Sequence[float]], weight: Sequence[float], length_max: int = 12
) -> dict[str, object]:
    q = _matrix("kernel", kernel)
    v = _positive_vector("weight", weight, len(q))
    if not isinstance(length_max, int) or length_max < 1:
        raise ValueError("length_max must be positive")
    ceiling = float(np.max(q @ v / v))
    root = np.zeros(len(q))
    root[0] = 1.0
    ones = np.ones(len(q))
    rows = []
    power = np.eye(len(q))
    for length in range(1, length_max + 1):
        power = power @ q
        exact = float(root @ power @ ones)
        upper = float(v[0] * ceiling**length)
        rows.append({
            "length": length,
            "exact_bad_chain_mass": exact,
            "weighted_upper": upper,
            "bound_holds": exact <= upper + 1.0e-13,
        })
    return {
        "weighted_ceiling": ceiling,
        "root_weight_moment": float(v[0]),
        "rows": rows,
        "all_bounds_hold": all(row["bound_holds"] for row in rows),
    }


def convention_counterexample(epsilon: float) -> dict[str, object]:
    transfer, mask = two_sector_transfer(epsilon)
    data = doob_transform(transfer, mask)
    psi = np.asarray(data["vacuum_amplitude"])
    pbad = np.asarray(data["bad_subkernel"])
    amplitude_weight = psi / np.min(psi)
    amplitude_ratios = pbad @ amplitude_weight / amplitude_weight
    inverse_ratios = np.asarray(data["weighted_bad_ratios"])
    target_rows = np.asarray(data["normalized_transfer_amplitude_rows"])
    return {
        "amplitude_weight": amplitude_weight.tolist(),
        "inverse_amplitude_weight": data["forward_cost_weight"],
        "amplitude_weighted_ratios": amplitude_ratios.tolist(),
        "inverse_amplitude_weighted_ratios": inverse_ratios.tolist(),
        "inverse_identity_error": float(np.max(np.abs(inverse_ratios - target_rows))),
        "amplitude_identity_error": float(np.max(np.abs(amplitude_ratios - target_rows))),
        "lesson": "psi normalizes the Doob transform; inverse psi is the forward rarity cost weight",
    }


def nonuniformity_counterexample(max_size: int = 20) -> dict[str, object]:
    sizes = np.arange(1, max_size + 1, dtype=float)
    rare_amplitudes = np.exp(-sizes)
    maximum_cost_weights = 1.0 / rare_amplitudes
    return {
        "sizes": [int(x) for x in sizes],
        "rare_vacuum_amplitudes": rare_amplitudes.tolist(),
        "maximum_inverse_weights": maximum_cost_weights.tolist(),
        "last_maximum_weight": float(maximum_cost_weights[-1]),
        "uniform_weight_bound_exists": False,
        "lesson": "finite-volume positivity does not provide volume-uniform Harnack or root-moment control",
    }


def cross_stage_consistency() -> dict[str, object]:
    package = HERE.parent
    stage19 = json.loads((package / "19_state_weighted_defect_transfer" / "state_weighted_defect_transfer_calibration.json").read_text(encoding="utf-8"))
    stage24 = json.loads((package / "24_multichannel_state_weights" / "multichannel_state_weights_calibration.json").read_text(encoding="utf-8"))
    stage25 = json.loads((package / "25_one_scale_kr_composition" / "one_scale_kr_composition_calibration.json").read_text(encoding="utf-8"))
    q19 = float(stage19["target_weighted_ceiling"])
    q24 = float(stage24["target_weighted_ceiling"])
    q25 = float(stage25["certificate"]["target_weighted_ceiling"])
    c19 = float(stage19["cluster_certificate"]["branching_ratio"])
    c25 = float(stage25["certificate"]["branching_ratio"])
    return {
        "stage19_target": q19,
        "stage24_target": q24,
        "stage25_target": q25,
        "target_agreement_error": max(q19, q24, q25) - min(q19, q24, q25),
        "stage19_stage25_branching_error": abs(c19 - c25),
        "stage24_weight": stage24["weight"],
        "all_targets_agree": bool(max(q19, q24, q25) - min(q19, q24, q25) < 1.0e-15),
        "branching_constants_agree": bool(abs(c19 - c25) < 1.0e-15),
    }


def calibration() -> dict[str, object]:
    q_target = 0.002430277501841998
    q_critical = 0.0027927080803578997

    transfer, mask = two_sector_transfer(q_target)
    doob = doob_transform(transfer, mask)

    star, declared_weight = multichannel_star_kernel(q_target, 4)
    optimal_weight, star_perron = perron_certificate(star, declared_weight)
    _, optimal_certificate = perron_certificate(star, optimal_weight)
    chains = chain_certificate(star, declared_weight, 12)
    cluster = cluster_certificate(q_target, 18, 0.1, root_moment=1.0)

    return {
        "schema_version": 1,
        "date": "2026-07-21",
        "hypothesis": "H1 vacuum-weight duality for retained-state defect transfer",
        "conceptual_correction": {
            "vacuum_amplitude_role": "psi is the positive eigenfunction used in the Doob transform",
            "forward_cost_role": "V=1/psi is the natural rare-state Lyapunov weight",
            "optimal_defect_role": "the Perron vector of Q minimizes the positive weighted ceiling",
            "these_vectors_need_not_coincide": True,
        },
        "two_sector_vacuum_doob": doob,
        "four_channel_star": {
            "channels": ["center", "continuous", "cut_orbit", "integer_topology"],
            "kernel": star.tolist(),
            "declared_weight": declared_weight.tolist(),
            "computed_perron_weight": optimal_weight.tolist(),
            "declared_weight_certificate": star_perron.to_dict(),
            "computed_optimum_certificate": optimal_certificate.to_dict(),
            "target_weighted_ceiling": q_target,
            "critical_weighted_ceiling": q_critical,
            "strictly_below_cluster_critical": q_target < q_critical,
        },
        "chain_iteration": chains,
        "cluster_certificate": cluster.to_dict(),
        "convention_counterexample": convention_counterexample(q_target),
        "nonuniformity_counterexample": nonuniformity_counterexample(),
        "cross_stage_consistency": cross_stage_consistency(),
        "yang_mills_handoff": {
            "finite_regulator_and_retained_state_frozen": False,
            "physical_normalized_bad_kernel_constructed": False,
            "vacuum_amplitude_constructed_uniformly": False,
            "inverse_amplitude_root_moment_uniform": False,
            "boundary_uniform_partition_ratio_proved": False,
            "one_scale_basin_entry": False,
            "repeated_rg": False,
            "continuum_os_gap": False,
            "first_open_implication": (
                "construct the normalized nonlinear SU(2) retained-state transfer and a positive "
                "vacuum/cost weight with uniform bad-row and root-moment bounds"
            ),
        },
        "claim_level": "C2 finite positive-transfer and weighted-kernel theorems; physical Yang--Mills premise open",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = calibration()
    if args.write:
        RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
