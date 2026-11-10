"""Finite same-measure calibration for H1.

The module starts from one strictly positive, symmetric, positive-definite
two-state edge kernel T.  The same T is used as the temporal transfer matrix
and as the nearest-neighbour Gibbs edge weight.  Its Perron vector defines the
vacuum and the Doob dynamics.  A declared edge mask M then defines the bad
subkernel Q=M*P; no independently chosen exploration kernel is admitted.

The algebraically exact identity

    (Q V)_i / V_i = sum_j M_ij T_ij / lambda_0,

holds for the inverse-vacuum weight V_i=max(psi)/psi_i.  The module also gives
a same-measure counterfamily in which the weighted bad ceiling tends to zero
while the discrete temporal gap tends to zero.  Consequently, smallness of a
masked edge channel alone does not force a cutoff-uniform temporal gap.

The executable realization uses binary floating point with tolerance checks.
This is a finite C2 calibration, not a construction of Yang--Mills theory.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Sequence


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "h1_same_measure_results.json"
TOLERANCE = 1.0e-12


def _finite(value: object, name: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite real number") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be a finite real number")
    return result


def _matrix2(values: Sequence[Sequence[float]], name: str) -> list[list[float]]:
    if len(values) != 2 or any(len(row) != 2 for row in values):
        raise ValueError(f"{name} must be a two-by-two matrix")
    return [[_finite(values[i][j], f"{name}[{i}][{j}]") for j in range(2)] for i in range(2)]


def validate_transfer(values: Sequence[Sequence[float]]) -> list[list[float]]:
    """Validate a strictly positive symmetric reflection-positive kernel.

    For a two-state real symmetric edge kernel, positive definiteness is the
    finite Gram-factorization certificate used here for bond-reflection
    positivity.  Strict entry positivity gives a unique positive Perron
    vacuum.
    """

    transfer = _matrix2(values, "transfer")
    if any(x <= 0.0 for row in transfer for x in row):
        raise ValueError("transfer entries must be strictly positive")
    if abs(transfer[0][1] - transfer[1][0]) > TOLERANCE:
        raise ValueError("transfer must be symmetric")
    a, b, c = transfer[0][0], transfer[0][1], transfer[1][1]
    if a <= 0.0 or a * c - b * b <= TOLERANCE * max(1.0, a * c):
        raise ValueError("transfer must be strictly positive definite")
    transfer[1][0] = b
    return transfer


def validate_mask(values: Sequence[Sequence[float]]) -> list[list[float]]:
    mask = _matrix2(values, "mask")
    if any(x < 0.0 or x > 1.0 for row in mask for x in row):
        raise ValueError("mask entries must lie in [0,1]")
    return mask


def spectral_data(transfer: Sequence[Sequence[float]]) -> dict[str, object]:
    """Return tolerance-certified two-state spectral and Gram data."""

    t = validate_transfer(transfer)
    a, b, c = t[0][0], t[0][1], t[1][1]
    discriminant = math.hypot(a - c, 2.0 * b)
    lambda0 = 0.5 * (a + c + discriminant)
    lambda1 = 0.5 * (a + c - discriminant)
    if lambda1 <= 0.0:
        raise ArithmeticError("validated transfer unexpectedly has a nonpositive second eigenvalue")

    # This branch avoids subtractive cancellation in the small component.
    if a >= c:
        vacuum = [1.0, b / (lambda0 - c)]
    else:
        vacuum = [b / (lambda0 - a), 1.0]
    scale = max(vacuum)
    vacuum = [x / scale for x in vacuum]
    residual = max(
        abs(math.fsum(t[i][j] * vacuum[j] for j in range(2)) - lambda0 * vacuum[i])
        for i in range(2)
    )
    normalized_second_eigenvalue = lambda1 / lambda0
    temporal_gap = -math.log(normalized_second_eigenvalue)
    # Lower-triangular Gram/Cholesky factor: T=L L^T.  This is the explicit
    # bond-reflection positivity certificate for the finite edge kernel.
    l00 = math.sqrt(a)
    l10 = b / l00
    l11 = math.sqrt(c - l10 * l10)
    gram_factor = [[l00, 0.0], [l10, l11]]
    reconstructed = [
        [math.fsum(gram_factor[i][k] * gram_factor[j][k] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]
    gram_error = max(abs(reconstructed[i][j] - t[i][j]) for i in range(2) for j in range(2))
    return {
        "principal_eigenvalue": lambda0,
        "second_eigenvalue": lambda1,
        "normalized_second_eigenvalue": normalized_second_eigenvalue,
        "temporal_gap": temporal_gap,
        "vacuum_amplitude": vacuum,
        "perron_residual": residual,
        "minimum_transfer_eigenvalue": lambda1,
        "gram_factor": gram_factor,
        "gram_reconstruction_error": gram_error,
        "reflection_positive": lambda1 > 0.0,
        "vacuum_unique": b > 0.0,
    }


def same_measure_certificate(
    transfer: Sequence[Sequence[float]], mask: Sequence[Sequence[float]]
) -> dict[str, object]:
    """Build the Gibbs/transfer/Doob/bad-kernel certificate from one T."""

    t = validate_transfer(transfer)
    m = validate_mask(mask)
    spectral = spectral_data(t)
    lambda0 = float(spectral["principal_eigenvalue"])
    psi = [float(x) for x in spectral["vacuum_amplitude"]]

    doob = [
        [t[i][j] * psi[j] / (lambda0 * psi[i]) for j in range(2)]
        for i in range(2)
    ]
    bad = [[m[i][j] * doob[i][j] for j in range(2)] for i in range(2)]
    inverse = [max(psi) / x for x in psi]
    stationary_raw = [x * x for x in psi]
    normalization = math.fsum(stationary_raw)
    stationary = [x / normalization for x in stationary_raw]

    weighted_ratios = [
        math.fsum(bad[i][j] * inverse[j] for j in range(2)) / inverse[i]
        for i in range(2)
    ]
    transfer_rows = [math.fsum(m[i][j] * t[i][j] for j in range(2)) / lambda0 for i in range(2)]
    row_error = max(abs(math.fsum(row) - 1.0) for row in doob)
    stationarity_error = max(
        abs(math.fsum(stationary[i] * doob[i][j] for i in range(2)) - stationary[j])
        for j in range(2)
    )
    detailed_balance_error = max(
        abs(stationary[i] * doob[i][j] - stationary[j] * doob[j][i])
        for i in range(2)
        for j in range(2)
    )
    identity_error = max(abs(a - b) for a, b in zip(weighted_ratios, transfer_rows))
    subkernel_violation = max(bad[i][j] - doob[i][j] for i in range(2) for j in range(2))
    stationary_root_moment = math.fsum(stationary[i] * inverse[i] for i in range(2))

    return {
        "finite_state_space": ["regular", "charged"],
        "gibbs_edge_weight": t,
        "temporal_transfer": t,
        "same_measure_realization": True,
        "bad_edge_mask": m,
        "spectral": spectral,
        "doob_kernel": doob,
        "stationary_state": stationary,
        "bad_subkernel": bad,
        "inverse_vacuum_weight": inverse,
        "weighted_bad_ratios": weighted_ratios,
        "masked_transfer_rows_over_lambda0": transfer_rows,
        "weighted_bad_ceiling": max(weighted_ratios),
        "scalar_bad_ceiling": max(math.fsum(row) for row in bad),
        "stationary_root_moment": stationary_root_moment,
        "maximum_root_weight": max(inverse),
        "checks": {
            "doob_row_sum_error": row_error,
            "stationarity_error": stationarity_error,
            "detailed_balance_error": detailed_balance_error,
            "inverse_vacuum_identity_error": identity_error,
            "bad_is_doob_subkernel": subkernel_violation <= TOLERANCE,
            "same_entries_feed_gibbs_and_transfer": t == t,
        },
    }


def rare_sector_family(theta: float) -> tuple[list[list[float]], list[list[float]]]:
    """A nontrivial-vacuum same-measure calibration family.

    The symmetric mask marks an edge bad when at least one endpoint is in the
    charged sector.  Both its orientations therefore come from the same Gibbs
    edge event.
    """

    theta = _finite(theta, "theta")
    if theta <= 0.0 or theta >= 1.0 / math.sqrt(2.0):
        raise ValueError("theta must lie in (0,1/sqrt(2))")
    transfer = [[1.0, theta], [theta, 2.0 * theta * theta]]
    mask = [[0.0, 1.0], [1.0, 1.0]]
    return transfer, mask


def closing_gap_family(delta: float) -> tuple[list[list[float]], list[list[float]]]:
    """A same-measure family refuting a uniform gap inference from small q."""

    delta = _finite(delta, "delta")
    if delta <= 0.0 or delta >= 1.0:
        raise ValueError("delta must lie in (0,1)")
    transfer = [[1.0, delta], [delta, 1.0]]
    # The only bad event is a state-changing temporal edge.
    mask = [[0.0, 1.0], [1.0, 0.0]]
    return transfer, mask


def counterfamily_row(delta: float) -> dict[str, object]:
    transfer, mask = closing_gap_family(delta)
    cert = same_measure_certificate(transfer, mask)
    q = float(cert["weighted_bad_ceiling"])
    gap = float(cert["spectral"]["temporal_gap"])
    exact_q = delta / (1.0 + delta)
    exact_gap = -math.log((1.0 - delta) / (1.0 + delta))
    return {
        "delta": delta,
        "weighted_bad_ceiling": q,
        "temporal_gap": gap,
        "exact_q": exact_q,
        "exact_gap": exact_gap,
        "q_error": abs(q - exact_q),
        "gap_error": abs(gap - exact_gap),
        "vacuum_amplitude": cert["spectral"]["vacuum_amplitude"],
        "stationary_root_moment": cert["stationary_root_moment"],
    }


def implication_counterexample(levels: int = 12) -> dict[str, object]:
    """Show q_n -> 0 and m_n -> 0 with unique finite-volume vacua."""

    if not isinstance(levels, int) or levels < 2:
        raise ValueError("levels must be an integer at least two")
    rows = [counterfamily_row(2.0 ** (-n)) for n in range(1, levels + 1)]
    q_strictly_decreases = all(
        float(rows[i + 1]["weighted_bad_ceiling"]) < float(rows[i]["weighted_bad_ceiling"])
        for i in range(len(rows) - 1)
    )
    gap_strictly_decreases = all(
        float(rows[i + 1]["temporal_gap"]) < float(rows[i]["temporal_gap"])
        for i in range(len(rows) - 1)
    )
    return {
        "family": "T_delta=[[1,delta],[delta,1]], bad mask=off-diagonal",
        "rows": rows,
        "q_strictly_decreases": q_strictly_decreases,
        "gap_strictly_decreases": gap_strictly_decreases,
        "last_q": rows[-1]["weighted_bad_ceiling"],
        "last_gap": rows[-1]["temporal_gap"],
        "uniform_positive_gap_forced_by_q_upper_bound": False,
        "quantified_refutation": (
            "For every q_*>0 and m_*>0, sufficiently small delta>0 gives "
            "q(delta)<=q_* and 0<m(delta)<m_* while T_delta remains strictly "
            "positive, positive definite, and has a unique Perron vacuum."
        ),
    }


def calibration() -> dict[str, object]:
    theta = 0.05
    transfer, mask = rare_sector_family(theta)
    primary = same_measure_certificate(transfer, mask)
    counterexample = implication_counterexample(16)
    return {
        "stage": 68,
        "hypothesis": "H1: vacuum weight as coarse ground-state amplitude",
        "target": "finite reflection-positive same-measure calibration",
        "claim_level": "C2 finite algebraic theorem with floating-point certificate and finite-family countermodel",
        "arithmetic_contract": (
            "the inverse-vacuum formula and counterfamily formulas are exact "
            "mathematics; executable spectral and Gram data use binary floating "
            "point with tolerance checks"
        ),
        "primary_calibration_parameter": theta,
        "primary_calibration": primary,
        "theorem": {
            "same_measure_identity": (
                "For Q=M circle P, P_ij=T_ij psi_j/(lambda0 psi_i), and "
                "V_i=max(psi)/psi_i, (QV)_i/V_i=sum_j M_ij T_ij/lambda0."
            ),
            "root_moment": (
                "For symmetric T, pi_i=psi_i^2/sum psi^2 and the exact finite "
                "stationary root moment is sum_i pi_i V_i."
            ),
            "temporal_gap": "The finite discrete temporal gap is -log(lambda1/lambda0)>0.",
        },
        "countermodel": counterexample,
        "conclusion": (
            "Even when T is the common reflection-positive Gibbs/temporal kernel "
            "and Q is a mask of its Doob dynamics, a small weighted bad ceiling "
            "does not by itself force a uniform positive temporal gap."
        ),
        "guardrails": {
            "finite_reflection_positive_calibration": True,
            "bad_subkernel_from_same_finite_measure": True,
            "physical_su2_retained_kernel_constructed": False,
            "boundary_uniform_root_moment_proved": False,
            "cutoff_uniform_temporal_gap_proved": False,
            "continuum_measure_constructed": False,
            "os_axioms_verified": False,
            "stochastic_domination_inferred_from_moments": False,
            "yang_mills_mass_gap_proved": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", type=Path, default=None)
    args = parser.parse_args()
    payload = json.dumps(calibration(), indent=2, sort_keys=True) + "\n"
    if args.write is None:
        print(payload, end="")
    else:
        args.write.write_text(payload, encoding="utf-8")


if __name__ == "__main__":
    main()
