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
"""Certify two-sided Route A endpoint error budgets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def interval(x: Any, name: str) -> tuple[float, float]:
    if isinstance(x, (int, float)):
        v = float(x)
        return v, v
    if isinstance(x, list) and len(x) == 2:
        lo, hi = float(x[0]), float(x[1])
        if lo > hi:
            raise ValueError(f"{name} lower bound exceeds upper bound")
        return lo, hi
    raise ValueError(f"{name} must be number or [lower, upper]")


def fixture(name: str) -> dict[str, Any]:
    base = {
        "schema": "abducer.routea_endpoint_error_budget_input.v1",
        "M_G": [0.4, 0.42],
        "R_hat": [-0.1, -0.08],
        "error_terms": [
            {"name": "stencil", "bound": 0.02, "sided": "two"},
            {"name": "tail", "bound": 0.03, "sided": "two"}
        ]
    }
    if name == "negative":
        base["M_G"] = [0.05, 0.06]
        base["R_hat"] = [-0.3, -0.28]
    elif name == "inconclusive":
        base["M_G"] = [0.1, 0.12]
        base["R_hat"] = [-0.11, -0.09]
    elif name == "invalid_one_sided":
        base["error_terms"] = [{"name": "tail", "bound": 0.02, "sided": "lower"}]
    return base


def certify(data: dict[str, Any]) -> dict[str, Any]:
    mg = interval(data["M_G"], "M_G")
    rh = interval(data["R_hat"], "R_hat")
    total = 0.0
    invalid_terms = []
    terms = []
    for term in data.get("error_terms", []):
        sided = term.get("sided", "two")
        bound = abs(float(term.get("bound", 0.0)))
        terms.append({"name": term.get("name", "unnamed"), "bound": bound, "sided": sided})
        if sided != "two":
            invalid_terms.append(term.get("name", "unnamed"))
        total += bound
    if invalid_terms:
        klass = "invalid_missing_two_sided_control"
    elif mg[0] + rh[0] - total > 0:
        klass = "positive_certificate"
    elif mg[1] + rh[1] + total < 0:
        klass = "negative_certificate"
    else:
        klass = "inconclusive"
    return {
        "schema": "abducer.routea_endpoint_error_budget_certificate.v1",
        "M_G_interval": list(mg),
        "R_hat_interval": list(rh),
        "error_terms": terms,
        "Delta_end": total,
        "certificate_class": klass,
        "positive_test_value": mg[0] + rh[0] - total,
        "negative_test_value": mg[1] + rh[1] + total,
        "invalid_terms": invalid_terms,
        "paper_result_form": "proposition" if klass in {"positive_certificate", "negative_certificate"} else "inconclusive_certificate_note",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("--fixture", choices=["positive", "negative", "inconclusive", "invalid_one_sided"])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.fixture:
        data = fixture(args.fixture)
    elif args.input:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    else:
        data = fixture("positive")
    report = certify(data)
    text = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text)
    return 0 if report["certificate_class"] != "invalid_missing_two_sided_control" else 1


if __name__ == "__main__":
    raise SystemExit(main())
