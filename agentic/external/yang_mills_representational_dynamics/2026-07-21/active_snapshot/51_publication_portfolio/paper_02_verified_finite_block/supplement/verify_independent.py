#!/usr/bin/env python3
"""Independent fraction-free cross-check of the spectral/rank certificate.

This verifier shares only the declarative cubical constructor with the main
checker.  It uses modular Gaussian elimination for ranks and Bareiss
fraction-free leading-principal-minor elimination for Sylvester positivity;
it does not call the Fraction LDL routine.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from supplement.verify_finite_block import (
    block_complex,
    gram_on_cotree,
    spanning_tree,
)


def rank_mod_prime(matrix: list[list[int]], prime: int) -> int:
    a = [[x % prime for x in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((i for i in range(rank, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], -1, prime)
        a[rank] = [(x * inv) % prime for x in a[rank]]
        for i in range(rank + 1, rows):
            if not a[i][col]:
                continue
            factor = a[i][col]
            a[i] = [(x - factor * y) % prime for x, y in zip(a[i], a[rank])]
        rank += 1
    return rank


def bareiss_positive_leading_minors(h: list[list[int]]) -> dict[str, object]:
    # H - I/25 is positive iff K=25H-I is positive.
    n = len(h)
    a = [[25 * h[i][j] - (1 if i == j else 0) for j in range(n)] for i in range(n)]
    previous = 1
    leading: list[int] = []
    for k in range(n - 1):
        pivot = a[k][k]
        leading.append(pivot)
        if pivot <= 0:
            return {"positive": False, "failed_index": k}
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                quotient, remainder = divmod(numerator, previous)
                if remainder:
                    raise ArithmeticError("Bareiss division was not exact")
                a[i][j] = quotient
        for i in range(k + 1, n):
            a[i][k] = 0
            a[k][i] = 0
        previous = pivot
    leading.append(a[n - 1][n - 1])
    if leading[-1] <= 0:
        return {"positive": False, "failed_index": n - 1}
    digest = hashlib.sha256()
    for value in leading:
        digest.update(f"{value}\n".encode())
    return {
        "positive": True,
        "failed_index": None,
        "leading_minor_sha256": digest.hexdigest(),
        "maximum_bit_length": max(abs(x).bit_length() for x in leading),
    }


def independent_certificate() -> dict[str, object]:
    block = block_complex()
    vertices = block["vertices"]
    edges = block["edges"]
    d0 = block["d0"]
    d1 = block["d1"]
    coarse = block["coarse"]
    tree = spanning_tree(vertices, edges)
    cotree = [i for i in range(len(edges)) if i not in set(tree)]
    retained = [[row[e] for e in cotree] for row in coarse]
    h = gram_on_cotree(d1, cotree)
    modular = {
        str(p): {
            "rank_d0": rank_mod_prime(d0, p),
            "rank_d1": rank_mod_prime(d1, p),
            "rank_retained": rank_mod_prime(retained, p),
        }
        for p in (2, 101, 1_000_003)
    }
    bareiss = bareiss_positive_leading_minors(h)
    checks = {
        "all_modular_ranks_agree": all(
            x == {"rank_d0": 80, "rank_d1": 136, "rank_retained": 17}
            for x in modular.values()
        ),
        "bareiss_sylvester_positive": bool(bareiss["positive"]),
    }
    return {
        "schema": "ym-paper02-independent-certificate-v1",
        "arithmetic": "modular ranks plus integer Bareiss/Sylvester test",
        "modular_rank_checks": modular,
        "spectral_cross_check": bareiss,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = independent_certificate()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
