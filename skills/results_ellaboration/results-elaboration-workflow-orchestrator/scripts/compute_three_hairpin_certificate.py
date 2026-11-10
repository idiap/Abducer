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
"""Compute the exact finite three-hairpin Schur-Feshbach certificate."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = ROOT / "agentic/reports/results_ellaboration/finite-wilson-os-schur-feshbach-paper-restructured"


def matrix_to_strings(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(sp.simplify(matrix[i, j])) for j in range(matrix.cols)] for i in range(matrix.rows)]


def main() -> int:
    sqrt = sp.sqrt
    one = sp.Matrix([1, 1, 1])
    e = one / sqrt(3)
    u = sp.Matrix([1, -1, 0]) / sqrt(2)
    z = sp.Matrix([1, 1, -2]) / sqrt(6)
    identity = sp.eye(3)
    P = identity - e * e.T

    H = 2 * (u * u.T) + e * z.T + z * e.T
    K = z * z.T
    A = sp.simplify(P * H * P)
    C = sp.simplify(P * (K - sp.Rational(1, 3) * H * e * e.T * H) * P)

    basis = sp.Matrix.hstack(u, z)
    A_reduced = sp.simplify(basis.T * A * basis)
    C_reduced = sp.simplify(basis.T * C * basis)
    z_margin = sp.simplify((z.T * C * z)[0])
    u_margin = sp.simplify((u.T * A * u)[0])

    payload = {
        "schema": "abducer.results_elaboration.three_hairpin_certificate.v1",
        "basis": {
            "e": ["1/sqrt(3)", "1/sqrt(3)", "1/sqrt(3)"],
            "u": ["1/sqrt(2)", "-1/sqrt(2)", "0"],
            "z": ["1/sqrt(6)", "1/sqrt(6)", "-2/sqrt(6)"],
        },
        "matrices": {
            "H_standard_basis": matrix_to_strings(H),
            "K_standard_basis": matrix_to_strings(K),
            "A_PHP_standard_basis": matrix_to_strings(A),
            "C_corrected_standard_basis": matrix_to_strings(C),
            "A_reduced_basis_u_z": matrix_to_strings(A_reduced),
            "C_reduced_basis_u_z": matrix_to_strings(C_reduced),
        },
        "certificate": {
            "first_order_positive_direction": "u",
            "first_order_margin_on_u": str(u_margin),
            "first_order_null_direction": "z",
            "corrected_second_order_margin_on_z": str(z_margin),
            "decision": "strict_second_order_validation",
        },
        "interpretation": (
            "This is an exact finite coefficient model. It validates the Schur-Feshbach "
            "mechanism and the table algebra, but it is not a completed regulator-specific "
            "Wilson coefficient derivation."
        ),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "three_hairpin_certificate.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
