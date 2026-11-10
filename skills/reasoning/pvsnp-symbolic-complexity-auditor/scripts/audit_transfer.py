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
"""Audit P vs NP transfer exponents exactly.

This helper is intentionally narrow. It evaluates the common route pattern:

    source lower bound:        carrier requires SIZE(N^a)
    induced upper bound under target assumption: SIZE(N^(q + beta*c))

where `c` is the SAT/NP circuit exponent, `q` is carrier overhead, and `beta`
measures how strongly the target circuit is queried. If beta is positive, the
route can exclude only a bounded exponent window unless extra nonblackbox or
subpolynomial structure is supplied.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


def frac(value: Any, default: str = "0") -> Fraction:
    if value is None or value == "":
        value = default
    return Fraction(str(value))


def as_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def maybe_sympy_formula(q: Fraction, beta: Fraction) -> str:
    try:
        import sympy as sp  # type: ignore

        c = sp.symbols("c", nonnegative=True)
        return str(sp.simplify(sp.Rational(q.numerator, q.denominator) + sp.Rational(beta.numerator, beta.denominator) * c))
    except Exception:
        if beta == 0:
            return as_text(q)
        return f"{as_text(q)} + ({as_text(beta)})*c"


def audit(spec: dict[str, Any]) -> dict[str, Any]:
    a = frac(spec.get("a") or spec.get("source_lower_exponent"), "0")
    q = frac(spec.get("q") or spec.get("overhead_exponent"), "0")
    beta = frac(spec.get("beta") or spec.get("target_query_exponent"), "0")
    padding_k = frac(spec.get("padding_k") or spec.get("k"), "1")
    advice_bits = str(spec.get("advice_bits", "explicit_unknown"))
    target = str(spec.get("target_class", "NP not subset P/poly"))
    source = str(spec.get("source_carrier", "explicit_unknown"))

    margin = a - q
    if beta == 0:
        if margin > 0:
            disposition = "potential_all_polynomial_exclusion"
            window = "all c >= 0, subject to uniformity/advice/barrier side conditions"
            stop_or_continue = "continue_only_if_the_beta_zero_interface_is_not_a_hidden_projection_or_advice_leak"
        elif margin == 0:
            disposition = "threshold_tie_no_strict_contradiction"
            window = "no strict exponent window without lower-order or logarithmic separation"
            stop_or_continue = "adapt_by_searching_for_a_strict_margin_or_a_stronger_source_bound"
        else:
            disposition = "overhead_dominates_no_exclusion"
            window = "none"
            stop_or_continue = "backtrack_or_quarantine_unless_q_can_be_reduced"
    else:
        c_star = margin / beta
        if c_star > 0:
            disposition = "bounded_exponent_window_only"
            window = f"c < {as_text(c_star)}"
            stop_or_continue = "convert_to_no_go_or_find_subpolynomial_nonblackbox_interface"
        else:
            disposition = "no_positive_exponent_window"
            window = "none"
            stop_or_continue = "quarantine_unless_source_bound_or_overhead_changes"

    padding_note = (
        "padding_identity"
        if padding_k == 1
        else f"length map N=n^{as_text(padding_k)} must be carried through every lower-bound and upper-bound exponent"
    )

    barrier_flags = {
        "naturalness_status": str(spec.get("naturalness_status", "explicit_unknown")),
        "relativization_status": str(spec.get("relativization_status", "explicit_unknown")),
        "algebrization_status": str(spec.get("algebrization_status", "explicit_unknown")),
        "uniformity_status": str(spec.get("uniformity_status", "explicit_unknown")),
        "advice_bits": advice_bits,
    }

    return {
        "version": 1,
        "source_carrier": source,
        "target_class": target,
        "variables": {
            "a_source_lower_exponent": as_text(a),
            "q_overhead_exponent": as_text(q),
            "beta_target_query_exponent": as_text(beta),
            "padding_k": as_text(padding_k),
        },
        "transfer_formula": {
            "induced_upper_exponent_in_N": maybe_sympy_formula(q, beta),
            "strict_contradiction_condition": "a > q + beta*c",
            "margin_a_minus_q": as_text(margin),
            "excluded_c_window": window,
        },
        "disposition": disposition,
        "stop_or_continue": stop_or_continue,
        "padding_note": padding_note,
        "barrier_flags": barrier_flags,
        "non_claims": [
            "This audit does not prove P != NP.",
            "A bounded exponent window is not NP not subset P/poly.",
            "Finite or symbolic probes require a separate theorem statement before paper-level promotion.",
        ],
    }


def load_spec(args: argparse.Namespace) -> dict[str, Any]:
    if args.spec:
        return json.loads(Path(args.spec).read_text(encoding="utf-8"))
    return {
        "source_carrier": args.source_carrier,
        "target_class": args.target_class,
        "a": args.a,
        "q": args.q,
        "beta": args.beta,
        "padding_k": args.padding_k,
        "advice_bits": args.advice_bits,
        "naturalness_status": args.naturalness_status,
        "relativization_status": args.relativization_status,
        "algebrization_status": args.algebrization_status,
        "uniformity_status": args.uniformity_status,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", help="JSON spec containing source_carrier, target_class, a, q, beta, and optional barrier fields.")
    parser.add_argument("--source-carrier", default="explicit_unknown")
    parser.add_argument("--target-class", default="NP not subset P/poly")
    parser.add_argument("--a", default="0", help="Source lower-bound exponent in N^a.")
    parser.add_argument("--q", default="0", help="Carrier overhead exponent in N^q.")
    parser.add_argument("--beta", default="0", help="Target-query exponent multiplying c.")
    parser.add_argument("--padding-k", default="1", help="Padding map N=n^k.")
    parser.add_argument("--advice-bits", default="explicit_unknown")
    parser.add_argument("--naturalness-status", default="explicit_unknown")
    parser.add_argument("--relativization-status", default="explicit_unknown")
    parser.add_argument("--algebrization-status", default="explicit_unknown")
    parser.add_argument("--uniformity-status", default="explicit_unknown")
    parser.add_argument("--output", help="Optional JSON output path.")
    args = parser.parse_args()
    result = audit(load_spec(args))
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
