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
"""Check finite Schur-factor candidates for Route A normalization."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def mat(data: Any) -> list[list[float]]:
    if not isinstance(data, list) or not data or any(not isinstance(r, list) for r in data):
        raise ValueError("matrix must be a nonempty list of rows")
    n = len(data)
    if any(len(r) != n for r in data):
        raise ValueError("matrix must be square")
    return [[float(x) for x in r] for r in data]


def is_symmetric(a: list[list[float]], tol: float = 1e-9) -> bool:
    return all(abs(a[i][j] - a[j][i]) <= tol for i in range(len(a)) for j in range(len(a)))


def jacobi_eigenvalues(a: list[list[float]], tol: float = 1e-12, max_iter: int = 10000) -> list[float]:
    n = len(a)
    b = [row[:] for row in a]
    for _ in range(max_iter):
        p, q, max_val = 0, 1 if n > 1 else 0, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(b[i][j]) > max_val:
                    p, q, max_val = i, j, abs(b[i][j])
        if max_val < tol or n == 1:
            break
        if abs(b[p][p] - b[q][q]) < tol:
            angle = math.pi / 4
        else:
            angle = 0.5 * math.atan2(2 * b[p][q], b[q][q] - b[p][p])
        c, s = math.cos(angle), math.sin(angle)
        app = c * c * b[p][p] - 2 * s * c * b[p][q] + s * s * b[q][q]
        aqq = s * s * b[p][p] + 2 * s * c * b[p][q] + c * c * b[q][q]
        b[p][q] = b[q][p] = 0.0
        b[p][p], b[q][q] = app, aqq
        for r in range(n):
            if r in (p, q):
                continue
            brp, brq = b[r][p], b[r][q]
            b[r][p] = b[p][r] = c * brp - s * brq
            b[r][q] = b[q][r] = s * brp + c * brq
    return sorted(b[i][i] for i in range(n))


def entrywise_inverse(a: list[list[float]]) -> list[list[float]]:
    out = []
    for row in a:
        out_row = []
        for x in row:
            if abs(x) < 1e-15:
                raise ValueError("entrywise inverse has zero denominator")
            out_row.append(1.0 / x)
        out.append(out_row)
    return out


def check_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    a = mat(candidate["matrix"])
    eig = jacobi_eigenvalues(a) if is_symmetric(a) else []
    psd = bool(eig) and min(eig) >= -1e-9
    inv_report: dict[str, Any]
    try:
        inv = entrywise_inverse(a)
        inv_eig = jacobi_eigenvalues(inv) if is_symmetric(inv) else []
        inv_psd = bool(inv_eig) and min(inv_eig) >= -1e-9
        inv_report = {"defined": True, "psd": inv_psd, "eigenvalues": inv_eig}
    except ValueError as exc:
        inv_report = {"defined": False, "psd": False, "error": str(exc)}
    factor_type = candidate.get("factor_type", "unknown")
    same_theory_claim = candidate.get("same_theory_realization")
    admissible = factor_type in {"diagonal_one_body", "block_congruence"} or (
        factor_type in {"schur_kernel", "reflected_gram_kernel"} and psd and bool(same_theory_claim)
    )
    quotient_risk = factor_type == "entrywise_quotient" and not inv_report.get("psd", False)
    if quotient_risk:
        verdict = "inadmissible_quotient_obstruction"
    elif admissible:
        verdict = "admissible_if_realization_is_correct"
    elif psd and not same_theory_claim:
        verdict = "finite_psd_but_same_theory_missing"
    else:
        verdict = "not_certified"
    return {
        "name": candidate.get("name", "unnamed"),
        "factor_type": factor_type,
        "psd": psd,
        "eigenvalues": eig,
        "entrywise_inverse": inv_report,
        "same_theory_realization_present": bool(same_theory_claim),
        "verdict": verdict,
    }


def built_in() -> dict[str, Any]:
    return {
        "schema": "abducer.routea_schur_factor_candidates.v1",
        "candidates": [
            {
                "name": "psd_denominator_with_bad_entrywise_inverse",
                "factor_type": "entrywise_quotient",
                "matrix": [[1.0, 0.5, 0.25], [0.5, 1.0, 0.5], [0.25, 0.5, 1.0]]
            },
            {
                "name": "diagonal_observable_rescaling",
                "factor_type": "diagonal_one_body",
                "matrix": [[2.0, 0.0], [0.0, 3.0]],
                "same_theory_realization": "observable rescaling by positive diagonal factors"
            }
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8")) if args.input else built_in()
    report = {
        "schema": "abducer.routea_schur_factor_check.v1",
        "results": [check_candidate(c) for c in data.get("candidates", [])],
    }
    text = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
