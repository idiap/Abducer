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
"""Validate finite Route A sigma/tau margin certificates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


OUT_DIR = Path("agentic/reports/results_ellaboration/a-finite-schur-feshbach-test-for-reflected-wilson-blocks-an-explicit-four-dimens")


def interval(value: Any, name: str) -> tuple[float, float]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{name} must be [lower, upper]")
    lo, hi = float(value[0]), float(value[1])
    if lo > hi:
        raise ValueError(f"{name} lower bound exceeds upper bound")
    return lo, hi


def classify(sig: tuple[float, float] | None, tau: tuple[float, float] | None) -> str:
    if sig is None or tau is None:
        return "needs_same_regulator_wilson_estimator"
    if sig[0] > 0 and tau[0] > 0:
        return "strictly_positive_finite_certificate"
    if sig[1] <= 0 or tau[1] <= 0:
        return "nonpositive_or_invalid_for_strict_margin"
    return "inconclusive_interval"


def default_protocol() -> dict[str, Any]:
    return {
        "schema": "abducer.routea_finite_margin_input.v1",
        "status": "protocol_only",
        "lattice": {"note": "choose finite T,L,kappa,r,s,h before promotion"},
        "observable_provenance": "missing_same_regulator_wilson_estimator",
        "sigma_interval": None,
        "tau_interval": None,
        "uncertainty_sources": ["estimator_not_supplied"],
        "nonclaims": ["no finite positivity certificate", "no cutoff-uniform lower bound", "no continuum conclusion"]
    }


def evaluate(data: dict[str, Any]) -> dict[str, Any]:
    provenance = data.get("observable_provenance", "")
    sig = interval(data["sigma_interval"], "sigma_interval") if data.get("sigma_interval") is not None else None
    tau = interval(data["tau_interval"], "tau_interval") if data.get("tau_interval") is not None else None
    status = classify(sig, tau)
    if "same_regulator" not in provenance and status != "needs_same_regulator_wilson_estimator":
        status = "quarantined_non_wilson_or_unclear_provenance"
    return {
        "schema": "abducer.routea_finite_margin_certificate.v1",
        "status": status,
        "lattice": data.get("lattice", {}),
        "observable_provenance": provenance,
        "sigma_interval": list(sig) if sig else None,
        "tau_interval": list(tau) if tau else None,
        "uncertainty_sources": data.get("uncertainty_sources", []),
        "finite_only_nonclaims": [
            "does not prove cutoff-uniform lower bounds",
            "does not imply OS reconstruction",
            "does not imply a mass gap"
        ],
        "paper_result_form": "finite_example_proposition" if status == "strictly_positive_finite_certificate" else "appendix_protocol_or_no_claim",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("--output", type=Path, default=OUT_DIR / "routea_finite_margin_certificate.json")
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8")) if args.input else default_protocol()
    report = evaluate(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
