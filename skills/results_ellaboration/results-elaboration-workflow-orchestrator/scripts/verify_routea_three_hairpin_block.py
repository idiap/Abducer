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
"""Symbolic and numerical verification for the Route A SU(2) three-hairpin block.

This is a repo-integrated version of the supplied verification script.  It checks:

* exact normalized block q = D N D;
* Taylor coefficients H and K;
* Schur-Feshbach reduced coefficients A = P H P and
  C = P(K - 1/3 H e e^T H)P;
* determinant formula and reduced margins;
* the concrete spurious sigma^2 term removed by the correction.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = ROOT / "agentic/reports/results_ellaboration/a-finite-schur-feshbach-test-for-reflected-wilson-blocks-an-explicit-four-dimens"


@dataclass(frozen=True)
class NumericParameters:
    sigma: float
    tau: float
    epsilon: float

    def validate(self) -> None:
        if self.sigma < 0 or self.tau < 0 or self.epsilon < 0:
            raise ValueError("sigma, tau, and epsilon must be nonnegative")


def matrix_to_strings(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(sp.factor(sp.simplify(matrix[i, j]))) for j in range(matrix.cols)] for i in range(matrix.rows)]


def symbolic_checks() -> dict[str, Any]:
    eps, sigma, tau = sp.symbols("eps sigma tau", nonnegative=True, real=True)

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

    expected_A = sigma * b * b.T
    expected_C = -sigma**2 * b * b.T + (tau / 9) * z * z.T
    expected_det = 4 * eps**3 * sigma * tau / (
        (1 + eps * sigma) ** 2 * (1 + eps**2 * tau)
    )

    checks = {
        "A_equals_sigma_bbT": sp.simplify(A - expected_A) == sp.zeros(3),
        "C_equals_corrected_formula": sp.simplify(C - expected_C) == sp.zeros(3),
        "determinant_formula": sp.simplify(q.det() - expected_det) == 0,
        "null_corrected_scalar_z": sp.simplify((z.T * C * z)[0] - 4 * tau) == 0,
        "null_uncorrected_scalar_z": sp.simplify((z.T * P * K * P * z)[0] - (sigma**2 + 4 * tau)) == 0,
        "spurious_sigma2_removed": sp.simplify(
            (z.T * (sp.Rational(1, 3) * P * H * e * e.T * H * P) * z)[0]
            - sigma**2
        )
        == 0,
    }

    u = b / sp.sqrt(2)
    v = z / sp.sqrt(6)
    checks.update(
        {
            "first_reduced_margin_u": sp.simplify((u.T * A * u)[0] - 2 * sigma) == 0,
            "corrected_null_margin_v": sp.simplify((v.T * C * v)[0] - sp.Rational(2, 3) * tau) == 0,
            "mixed_corrected_uv_zero": sp.simplify((u.T * C * v)[0]) == 0,
        }
    )

    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"symbolic checks failed: {failed}")

    return {
        "symbols": {"epsilon": "eps", "sigma": "sigma", "tau": "tau"},
        "checks": checks,
        "matrices": {
            "N": matrix_to_strings(N),
            "q": matrix_to_strings(q),
            "H": matrix_to_strings(H),
            "K": matrix_to_strings(K),
            "A": matrix_to_strings(A),
            "C": matrix_to_strings(C),
        },
        "scalars": {
            "det_q": str(sp.factor(q.det())),
            "z_C_z": str(sp.factor((z.T * C * z)[0])),
            "z_PKP_z": str(sp.factor((z.T * P * K * P * z)[0])),
            "z_correction_z": str(sp.factor((z.T * (sp.Rational(1, 3) * P * H * e * e.T * H * P) * z)[0])),
            "u_A_u": str(sp.factor((u.T * A * u)[0])),
            "v_C_v": str(sp.factor((v.T * C * v)[0])),
            "u_C_v": str(sp.factor((u.T * C * v)[0])),
        },
    }


def numeric_report(params: NumericParameters) -> dict[str, Any]:
    params.validate()
    sigma, tau, eps = params.sigma, params.tau, params.epsilon

    one = np.ones(3)
    b = np.array([1.0, -1.0, 0.0])
    c = np.array([0.0, 0.0, 1.0])

    N = np.outer(one, one) + eps * sigma * np.outer(b, b) + eps**2 * tau * np.outer(c, c)
    D = np.diag(
        [
            (1.0 + eps * sigma) ** -0.5,
            (1.0 + eps * sigma) ** -0.5,
            (1.0 + eps**2 * tau) ** -0.5,
        ]
    )
    q = D @ N @ D
    return {
        "parameters": {"sigma": sigma, "tau": tau, "epsilon": eps},
        "q": q.tolist(),
        "eigvalsh_q": np.linalg.eigvalsh(q).tolist(),
        "det_q": float(np.linalg.det(q)),
        "first_reduced_margin_2sigma": 2.0 * sigma,
        "corrected_null_margin_2tau_over_3": 2.0 * tau / 3.0,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Route A Three-Hairpin Verification Certificate",
        "",
        "All symbolic identities verified.",
        "",
        "## Verified Identities",
        "",
    ]
    for name, passed in payload["symbolic"]["checks"].items():
        lines.append(f"- `{name}`: `{passed}`")
    lines += [
        "",
        "## Key Scalars",
        "",
    ]
    for name, value in payload["symbolic"]["scalars"].items():
        lines.append(f"- `{name}`: `{value}`")
    lines += [
        "",
        "## Narrative Consequence",
        "",
        "This certificate validates the finite source-collision Route A algebra. It does not validate the geometric collar open modules G1-G4, endpoint modules E1-E2, or continuum/gap modules M1-M2.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sigma", type=float, default=0.3)
    parser.add_argument("--tau", type=float, default=0.2)
    parser.add_argument("--epsilon", type=float, default=0.1)
    args = parser.parse_args()

    payload = {
        "schema": "abducer.results_elaboration.routea_three_hairpin_certificate.v1",
        "symbolic": symbolic_checks(),
        "numeric": numeric_report(NumericParameters(args.sigma, args.tau, args.epsilon)),
        "claim_boundary": [
            "verifies exact finite source-collision algebra",
            "does not prove geometric collar collapse",
            "does not prove endpoint cumulant estimates",
            "does not prove continuum reconstruction or a mass gap",
        ],
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "routea_three_hairpin_certificate.json"
    md_path = OUT_DIR / "routea_three_hairpin_certificate.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print("All symbolic identities verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
