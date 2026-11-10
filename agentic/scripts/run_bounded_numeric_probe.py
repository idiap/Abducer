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
"""Run guarded bounded numeric probes for PMP."""

from __future__ import annotations

import argparse
import math
from typing import Any

from agentic_common import ROOT, utc_now, write_json


OUT_DIR = ROOT / "agentic/reports/bounded_numeric_probe"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"


def det_value(r12: float, r23: float, r13: float, phi: float) -> float:
    return 1 - r12 * r12 - r23 * r23 - r13 * r13 + 2 * r12 * r23 * r13 * math.cos(phi)


def quotient_determinant_search(grid: int) -> dict[str, Any]:
    grid = max(3, min(grid, 81))
    values = [i / (grid - 1) for i in range(grid)]
    phases = [math.pi * i / (grid - 1) for i in range(grid)]
    best = {"det": 1.0, "rho12": 0.0, "rho23": 0.0, "rho13": 0.0, "Phi": 0.0}
    hits = 0
    for r12 in values:
        for r23 in values:
            for r13 in values:
                for phi in phases:
                    det = det_value(r12, r23, r13, phi)
                    if det < best["det"]:
                        best = {"det": det, "rho12": r12, "rho23": r23, "rho13": r13, "Phi": phi}
                    if det < -1e-12:
                        hits += 1
    return {
        "probe_kind": "quotient-determinant-search",
        "bounded_domain": [f"rho_ij in [0,1] on {grid}-point grid", f"Phi in [0,pi] on {grid}-point grid"],
        "stopping_condition": f"exhaustive deterministic grid of {grid ** 4} points",
        "result": {
            "negative_determinant_hits": hits,
            "most_negative_sample": best,
            "qualitative_lesson": "Pairwise minor bounds do not suffice when the cycle phase and three moduli make the normalized determinant negative.",
        },
    }


def phase_bound_sharpness(grid: int) -> dict[str, Any]:
    grid = max(3, min(grid, 201))
    rho = 0.9
    threshold = None
    for i in range(grid):
        phi = math.pi * i / (grid - 1)
        if det_value(rho, rho, rho, phi) < 0:
            threshold = phi
            break
    return {
        "probe_kind": "phase-bound-sharpness",
        "bounded_domain": [f"rho12=rho23=rho13={rho}", f"Phi in [0,pi] on {grid}-point grid"],
        "stopping_condition": "first deterministic grid point where determinant becomes negative",
        "result": {
            "first_negative_phi": threshold,
            "first_negative_phi_over_pi": None if threshold is None else threshold / math.pi,
            "qualitative_lesson": "For large moduli, phase control is not cosmetic; it decides whether the finite quotient is PSD.",
        },
    }


def noncommuting_limit_toy(grid: int) -> dict[str, Any]:
    grid = max(3, min(grid, 200))
    samples = []
    for n in range(1, grid + 1):
        a = 1 / n
        t = n
        samples.append({"n": n, "a": a, "t": t, "fixed_t_then_a": math.exp(-t) * (1 + a), "coupled_t_equals_1_over_a": math.exp(-a * t)})
    return {
        "probe_kind": "noncommuting-limit-toy",
        "bounded_domain": [f"n in [1,{grid}]", "a=1/n", "t=n"],
        "stopping_condition": "finite deterministic sequence",
        "result": {
            "last_sample": samples[-1],
            "qualitative_lesson": "A decay-looking statement can change meaning when time and cutoff limits are coupled; the workflow must keep limit order typed.",
        },
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    if args.probe == "quotient-determinant-search":
        probe = quotient_determinant_search(args.grid)
    elif args.probe == "phase-bound-sharpness":
        probe = phase_bound_sharpness(args.grid)
    else:
        probe = noncommuting_limit_toy(args.grid)
    return {
        "version": 1,
        "target_id": "yang-mills-existence-and-mass-gap-target",
        "generated_utc": utc_now(),
        "status": "calibration_only" if args.probe != "quotient-determinant-search" else "falsifier_candidate",
        "decision_packet": {
            "decision": "run_bounded_numeric_probe",
            "question": args.question,
            "symbolic_precondition": "Exact determinant and holonomy formulas already exist in agentic/reports/symbolic_matrix_probe/latest.json.",
            "analytic_precondition": "Analytic estimate obligations already exist in agentic/reports/analytic_estimate_obligations/latest.json.",
            "non_proof_boundary": "This bounded probe can rank or falsify local interfaces, but it cannot prove Yang-Mills claims.",
        },
        "probe": probe,
        "deterministic_reproducibility": {
            "random_seed": "not_used",
            "grid_size": args.grid,
            "runtime_scope": "small deterministic grid or finite toy sequence",
        },
        "transfer_boundary": "The result remains a local finite-interface probe until a same-theory analytic transfer certificate is proved.",
        "validation_handoff": "python agentic/scripts/validate_bounded_numeric_probe.py",
    }


def render_markdown(report: dict[str, Any]) -> str:
    result = report["probe"]["result"]
    return "\n".join(
        [
            "# Bounded Numeric Probe",
            "",
            f"- Status: `{report['status']}`",
            f"- Probe: `{report['probe']['probe_kind']}`",
            f"- Domain: `{'; '.join(report['probe']['bounded_domain'])}`",
            f"- Stopping: {report['probe']['stopping_condition']}",
            f"- Lesson: {result.get('qualitative_lesson', '')}",
            f"- Transfer boundary: {report['transfer_boundary']}",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", choices=["quotient-determinant-search", "phase-bound-sharpness", "noncommuting-limit-toy"], default="quotient-determinant-search")
    parser.add_argument("--grid", type=int, default=9)
    parser.add_argument("--question", default="Does the finite symbolic interface expose a local falsifier or sharpness region?")
    args = parser.parse_args()
    report = build_report(args)
    write_json(OUT_JSON, report)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
