#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Build an exact Route A symbolic/CAS audit report.

The report is scoped to the finite SU(2) reflected Wilson-block paper. It
verifies symbolic facts that may support finite theorem/proposition/lemma text
and marks everything else as an open proof obligation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = ROOT / "agentic/reports/results_ellaboration/a-finite-schur-feshbach-test-for-reflected-wilson-blocks-an-explicit-four-dimens"
DEFAULT_OUT = OUT_DIR / "routea_symbolic_cas_audit.json"


def matrix_strings(matrix: sp.Matrix) -> list[list[str]]:
    return [[sp.sstr(sp.factor(sp.simplify(matrix[i, j]))) for j in range(matrix.cols)] for i in range(matrix.rows)]


def bool_check(value: Any) -> bool:
    return bool(sp.simplify(value) == 0 if not isinstance(value, bool) else value)


def schur_source_collision() -> dict[str, Any]:
    eps, sigma, tau = sp.symbols("eps sigma tau", positive=True, real=True)
    one = sp.Matrix([1, 1, 1])
    b = sp.Matrix([1, -1, 0])
    c = sp.Matrix([0, 0, 1])
    z = sp.Matrix([1, 1, -2])
    e = one / sp.sqrt(3)
    P = sp.eye(3) - e * e.T

    N = one * one.T + eps * sigma * (b * b.T) + eps**2 * tau * (c * c.T)
    D = sp.diag(
        (1 + eps * sigma) ** sp.Rational(-1, 2),
        (1 + eps * sigma) ** sp.Rational(-1, 2),
        (1 + eps**2 * tau) ** sp.Rational(-1, 2),
    )
    q = sp.simplify(D * N * D)
    H = q.applyfunc(lambda entry: sp.diff(entry, eps).subs(eps, 0))
    K = q.applyfunc(lambda entry: sp.diff(entry, eps, 2).subs(eps, 0) / 2)
    A = sp.simplify(P * H * P)
    C = sp.simplify(P * (K - sp.Rational(1, 3) * H * e * e.T * H) * P)
    PKP = sp.simplify(P * K * P)
    correction = sp.simplify(sp.Rational(1, 3) * P * H * e * e.T * H * P)

    expected_A = sigma * b * b.T
    expected_C = -sigma**2 * b * b.T + (tau / 9) * z * z.T
    det_expected = 4 * eps**3 * sigma * tau / ((1 + eps * sigma) ** 2 * (1 + eps**2 * tau))
    u = b / sp.sqrt(2)
    v = z / sp.sqrt(6)

    checks = {
        "H_from_normalized_block": matrix_strings(H),
        "K_from_normalized_block": matrix_strings(K),
        "A_equals_sigma_bbT": sp.simplify(A - expected_A) == sp.zeros(3),
        "C_equals_corrected_formula": sp.simplify(C - expected_C) == sp.zeros(3),
        "det_q_formula": sp.simplify(q.det() - det_expected) == 0,
        "u_A_u_equals_2sigma": sp.simplify((u.T * A * u)[0] - 2 * sigma) == 0,
        "v_C_v_equals_2tau_over_3": sp.simplify((v.T * C * v)[0] - sp.Rational(2, 3) * tau) == 0,
        "z_PKP_z_uncorrected": sp.sstr(sp.factor((z.T * PKP * z)[0])),
        "z_correction_z": sp.sstr(sp.factor((z.T * correction * z)[0])),
        "z_C_z_corrected": sp.sstr(sp.factor((z.T * C * z)[0])),
        "spurious_sigma2_removed": sp.simplify((z.T * PKP * z)[0] - (z.T * correction * z)[0] - 4 * tau) == 0,
    }
    passed = all(value is True for key, value in checks.items() if key not in {"H_from_normalized_block", "K_from_normalized_block", "z_PKP_z_uncorrected", "z_correction_z", "z_C_z_corrected"})
    return {
        "status": "exact_symbolic_certificate" if passed else "failed_symbolic_certificate",
        "mathematical_object": "finite source-collision normalized reflected Gram block",
        "variables": ["eps", "sigma", "tau"],
        "checks": checks,
        "paper_support": [
            "rank-one Schur-Feshbach coefficient theorem application",
            "evaluated finite source-collision gate",
            "spurious sigma^2 Schur-correction explanation",
        ],
        "non_claims": [
            "does not construct a geometric collar",
            "does not prove cutoff-uniform nonvanishing of sigma or tau",
            "does not imply continuum reconstruction or a mass gap",
        ],
    }


def endpoint_incidence_identity() -> dict[str, Any]:
    r12, r13, r23 = sp.symbols("R12 R13 R23", real=True)
    R = sp.Matrix([[0, r12, r13], [r12, 0, r23], [r13, r23, 0]])
    z = sp.Matrix([1, 1, -2])
    identity = sp.expand((z.T * R * z)[0])
    expected = 2 * r12 - 4 * r13 - 4 * r23
    return {
        "status": "paper_safe_lemma" if sp.simplify(identity - expected) == 0 else "failed_symbolic_certificate",
        "mathematical_object": "zero-diagonal endpoint/null-channel incidence form",
        "null_vector": [1, 1, -2],
        "identity": sp.sstr(identity),
        "expected_identity": sp.sstr(expected),
        "paper_support": "endpoint bookkeeping lemma only after endpoint coefficients are regulator-derived",
        "non_claim": "incidence algebra alone does not determine endpoint sign",
    }


def normalization_counterexample() -> dict[str, Any]:
    r = sp.Rational(1, 2)
    B = sp.Matrix([[1, r, r], [r, 1, r], [r, r, 1]])
    Binv_hadamard = B.applyfunc(lambda x: sp.simplify(1 / x))
    eig_B = [sp.sstr(v) for v in B.eigenvals().keys()]
    eig_inv = [sp.sstr(v) for v in Binv_hadamard.eigenvals().keys()]
    return {
        "status": "finite_counterexample",
        "mathematical_object": "same-theory normalization quotient gate",
        "B": matrix_strings(B),
        "entrywise_inverse": matrix_strings(Binv_hadamard),
        "B_eigenvalues": eig_B,
        "entrywise_inverse_eigenvalues": eig_inv,
        "conclusion": "positive pair-dependent denominators do not make entrywise division positivity preserving",
        "paper_support": "normalization proposition must require congruence, positive-kernel Schur product, or direct Gram realization",
    }


def endpoint_error_logic() -> dict[str, Any]:
    M, Rhat, Delta = sp.symbols("M_G Rhat Delta", real=True)
    return {
        "status": "conditional_gate",
        "mathematical_object": "two-sided endpoint certificate logic",
        "positive_certificate": sp.sstr(M + Rhat - Delta > 0),
        "negative_certificate": sp.sstr(M + Rhat + Delta < 0),
        "inconclusive_region": "M_G + Rhat - Delta <= 0 <= M_G + Rhat + Delta",
        "invalid_negative_use": "a one-sided lower bound can certify positivity but cannot certify a negative obstruction",
        "paper_support": "endpoint certificate proposition and error-budget gate",
    }


def geometric_coefficient_obligations() -> dict[str, Any]:
    return {
        "status": "proof_obligation",
        "mathematical_object": "future geometric-collar q_{k,delta} coefficient theorem",
        "required_symbolic_objects": [
            "entry definition q_{k,delta}(i,j) from actual Wilson paths",
            "same-theory normalization certificate before expansion",
            "H_k and K_k computed from q_{k,delta}, not imported from source collision",
            "operator-norm remainder sup_k ||R_{k,delta}||/delta^2 -> 0",
            "reduced A_k=PH_kP and C_k=P(K_k-1/3 H_k e e^T H_k)P",
        ],
        "cas_role": "differentiate or expand a typed finite expression after the Wilson block is defined",
        "demotion_condition": "if no typed q_{k,delta} exists, CAS cannot promote G3 beyond a coefficient-extraction gate",
    }


def build_report() -> dict[str, Any]:
    checks = [
        schur_source_collision(),
        endpoint_incidence_identity(),
        normalization_counterexample(),
        endpoint_error_logic(),
        geometric_coefficient_obligations(),
    ]
    return {
        "schema": "abducer.routea_symbolic_cas_audit.v1",
        "target_paper": "finite_wilson_os_routeA_SU2_attack_integrated.tex",
        "claim_boundary": "finite source-collision and local symbolic gates only; no continuum or spectral promotion",
        "symbolic_reasoning_types": [
            "rank_one_schur_feshbach_algebra",
            "source_collision_coefficient_audit",
            "same_theory_normalization_counterexample",
            "endpoint_null_channel_incidence_identity",
            "two_sided_endpoint_certificate_logic",
            "geometric_collar_coefficient_obligation_extraction",
        ],
        "checks": checks,
        "required_followup_skills": [
            "routea-geometric-coefficient-extractor",
            "routea-same-theory-normalization-certifier",
            "routea-endpoint-local-integral-calculator",
            "routea-endpoint-error-budget-certifier",
            "routea-paper-result-integrator",
        ],
        "paper_safe_summary": (
            "Exact symbolic algebra supports the finite source-collision Schur-Feshbach certificate, "
            "the endpoint incidence identity, the two-sided endpoint logic, and the normalization quotient warning. "
            "It does not discharge geometric-collar construction, same-theory endpoint derivation, cutoff-uniform margins, "
            "continuum reconstruction, or spectral-gap implications."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    report = build_report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
