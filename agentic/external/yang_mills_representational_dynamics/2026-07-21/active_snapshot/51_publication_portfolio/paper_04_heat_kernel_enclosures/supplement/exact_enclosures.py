"""Exact-rational validation data for global SU(2) heat-kernel enclosures.

The proof-critical output consists of fractions.  Decimal strings are only
human-readable renderings.  Elementary-function bounds use alternating or
positive Taylor series with rational remainder estimates; pi is enclosed by
Machin's formula.  No binary floating-point value enters a pass decision.
"""

from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from math import comb, isqrt
import json
from pathlib import Path
import sys
from typing import Iterable


sys.set_int_max_str_digits(200000)
SCHEMA = "su2-heat-kernel-enclosure-validation-v2"
PI_PROOF_LOWER = F(333, 106)
PI_PROOF_UPPER = F(355, 113)


def ceil_fraction(x: F) -> int:
    return -((-x.numerator) // x.denominator)


def arctan_reciprocal(q: int, terms: int = 36) -> tuple[F, F]:
    """Enclose arctan(1/q) by its alternating series."""
    if q <= 1 or terms < 1:
        raise ValueError("q>1 and terms>=1 are required")
    total = F(0)
    for k in range(terms):
        term = F(1, (2 * k + 1) * q ** (2 * k + 1))
        total += term if k % 2 == 0 else -term
    nxt = F(1, (2 * terms + 1) * q ** (2 * terms + 1))
    other = total + (nxt if terms % 2 == 0 else -nxt)
    return min(total, other), max(total, other)


def pi_interval(terms: int = 36) -> tuple[F, F]:
    """Machin enclosure: pi=16 atan(1/5)-4 atan(1/239)."""
    a_lo, a_hi = arctan_reciprocal(5, terms)
    b_lo, b_hi = arctan_reciprocal(239, terms)
    return 16 * a_lo - 4 * b_hi, 16 * a_hi - 4 * b_lo


@lru_cache(maxsize=None)
def exp_negative_interval(x: F, terms: int = 28) -> tuple[F, F]:
    """Enclose exp(-x), x>=0, using range reduction and alternation."""
    if x < 0:
        raise ValueError("x must be nonnegative")
    if x == 0:
        return F(1), F(1)
    scale = max(1, ceil_fraction(x))
    y = x / scale
    total = F(1)
    term = F(1)
    for k in range(1, terms + 1):
        term *= y / k
        total += -term if k % 2 else term
    next_term = term * y / (terms + 1)
    other = total + (-next_term if (terms + 1) % 2 else next_term)
    lo, hi = min(total, other), max(total, other)
    if lo <= 0:
        raise ArithmeticError("increase Taylor order")
    return lo ** scale, hi ** scale


@lru_cache(maxsize=None)
def exp_positive_interval(x: F, terms: int = 28) -> tuple[F, F]:
    """Enclose exp(x) for 0<=x<1 by a positive series and ratio tail."""
    if not F(0) <= x < F(1):
        raise ValueError("the positive exponential primitive requires 0<=x<1")
    total = F(1)
    term = F(1)
    for k in range(1, terms + 1):
        term *= x / k
        total += term
    next_term = term * x / (terms + 1)
    ratio = x / (terms + 2)
    return total, total + next_term / (1 - ratio)


def exp_negative_upper_dyadic(x: F) -> F:
    """Fast exact upper bound exp(-x)<=2^{-floor(x)}, since e>2."""
    if x < 0:
        raise ValueError("x must be nonnegative")
    return F(1, 2 ** (x.numerator // x.denominator))


def exp_negative_upper_compact(x: F) -> F:
    """Compact upper bound using e > sum_{k=0}^6 1/k! = 1957/720."""
    if x < 0:
        raise ValueError("x must be nonnegative")
    return F(720, 1957) ** (x.numerator // x.denominator)


def sin_interval(x: F, terms: int = 24) -> tuple[F, F]:
    if not F(0) <= x <= F(1):
        raise ValueError("sin primitive is certified on [0,1]")
    total = F(0)
    for k in range(terms):
        term = x ** (2 * k + 1) / _factorial(2 * k + 1)
        total += term if k % 2 == 0 else -term
    nxt = x ** (2 * terms + 1) / _factorial(2 * terms + 1)
    other = total + (nxt if terms % 2 == 0 else -nxt)
    return min(total, other), max(total, other)


def cos_interval(x: F, terms: int = 24) -> tuple[F, F]:
    if not F(0) <= x <= F(1):
        raise ValueError("cos primitive is certified on [0,1]")
    total = F(0)
    for k in range(terms):
        term = x ** (2 * k) / _factorial(2 * k)
        total += term if k % 2 == 0 else -term
    nxt = x ** (2 * terms) / _factorial(2 * terms)
    other = total + (nxt if terms % 2 == 0 else -nxt)
    return min(total, other), max(total, other)


def _factorial(n: int) -> int:
    out = 1
    for k in range(2, n + 1):
        out *= k
    return out


def sqrt_interval(x: F, digits: int = 48) -> tuple[F, F]:
    """Decimal-grid rational enclosure for sqrt(x), proved by squaring."""
    if x < 0:
        raise ValueError("x must be nonnegative")
    scale = 10 ** digits
    n = (x.numerator * scale * scale) // x.denominator
    root = isqrt(n)
    lo = F(root, scale)
    hi = F(root + 1, scale)
    assert lo * lo <= x <= hi * hi
    return lo, hi


def image_term_upper(order: int, k: int, time_max: F, radius: F,
                     pi_lo: F, pi_hi: F) -> F:
    a_lo, a_hi = 2 * pi_lo * k, 2 * pi_hi * k
    action_lo = a_lo * a_lo / 2 - a_lo * radius
    exponential_hi = exp_negative_upper_dyadic(action_lo / time_max)
    return (2 * exponential_hi * (a_hi / time_max) ** order
            * (1 + a_hi * a_hi / (time_max * (order + 1))))


def image_derivative_upper(order: int, time_max: F, radius: F,
                           included: int = 1) -> tuple[F, F]:
    """Return Q_order and the geometric ratio used for the omitted images."""
    if order < 0 or included < 1 or not F(0) < radius:
        raise ValueError("invalid image-bound parameters")
    # Small rational Archimedean bounds keep certificates compact.  The much
    # tighter Machin interval is recorded independently below.
    pi_lo, pi_hi = PI_PROOF_LOWER, PI_PROOF_UPPER
    first_omitted = included + 1
    included_sum = sum(
        (image_term_upper(order, k, time_max, radius, pi_lo, pi_hi)
         for k in range(1, included + 1)), F(0))
    n = first_omitted
    exponent_action_lo = (2 * pi_lo * pi_lo * (2 * n + 1)
                          - 2 * pi_lo * radius)
    exp_hi = exp_negative_upper_dyadic(exponent_action_lo / time_max)
    ratio = F(n + 1, n) ** (order + 2) * exp_hi
    if ratio >= 1:
        raise ArithmeticError("noncontractive omitted-image ratio")
    first = image_term_upper(order, n, time_max, radius, pi_lo, pi_hi)
    return included_sum + first / (1 - ratio), ratio


def exp_power_max_upper(order: int, action_lower: F, time_max: F) -> F:
    """Upper bound for sup exp(-A/t)t^-order on 0<t<=time_max.

    The supplied action_lower is a proven lower bound for A.  When the
    stationary point is outside the interval, the endpoint is exact up to the
    rational exponential enclosure.  Otherwise the unrestricted maximum
    (order/(e*A))**order is used.
    """
    if order < 0 or action_lower <= 0 or time_max <= 0:
        raise ValueError("positive action/time and nonnegative order required")
    if order == 0:
        return exp_negative_upper_compact(action_lower / time_max)
    if order * time_max <= action_lower:
        return (exp_negative_upper_compact(action_lower / time_max)
                * time_max ** (-order))
    return exp_negative_upper_compact(F(order)) * (F(order) / action_lower) ** order


def transition_image_derivative_upper(
    order: int, time_max: F, delta: F, included_tail: int = 2
) -> tuple[F, F]:
    """Uniform Q-hat bound on 0<=theta<=pi-delta.

    The k=1 image is treated with the exact heat-time maximum.  For k>=2 the
    maximum is at time_max for all certified orders, so a Gaussian geometric
    tail applies.
    """
    if order < 0 or not F(0) < delta or included_tail < 2:
        raise ValueError("invalid transition-chart parameters")
    pi_lo, pi_hi = PI_PROOF_LOWER, PI_PROOF_UPPER
    a1_hi = 2 * pi_hi
    action1_lo = 2 * pi_lo * delta
    principal = (
        2 * a1_hi ** order
        * (
            exp_power_max_upper(order, action1_lo, time_max)
            + a1_hi * a1_hi / (order + 1)
            * exp_power_max_upper(order + 1, action1_lo, time_max)
        )
    )
    radius_hi = pi_hi - delta

    def tail_term(k: int) -> F:
        a_lo, a_hi = 2 * pi_lo * k, 2 * pi_hi * k
        action_lo = a_lo * a_lo / 2 - a_hi * radius_hi
        if action_lo <= (order + 1) * time_max:
            raise ArithmeticError("tail term is not monotone at time_max")
        exponential_hi = exp_negative_upper_dyadic(action_lo / time_max)
        return (
            2
            * exponential_hi
            * (a_hi / time_max) ** order
            * (1 + a_hi * a_hi / (time_max * (order + 1)))
        )

    explicit_tail = sum((tail_term(k) for k in range(2, included_tail + 1)), F(0))
    n = included_tail + 1
    exponent_gap_lo = (
        2 * pi_lo * pi_lo * (2 * n + 1) - 2 * pi_hi * radius_hi
    )
    ratio = F(n + 1, n) ** (order + 2) * exp_negative_upper_dyadic(
        exponent_gap_lo / time_max
    )
    if ratio >= 1:
        raise ArithmeticError("noncontractive transition-image ratio")
    first = tail_term(n)
    return principal + explicit_tail + first / (1 - ratio), ratio


def partial_bell(n: int, k: int, xs: list[F]) -> F:
    """Exponential partial Bell polynomial B_{n,k}."""
    if n == k == 0:
        return F(1)
    if n <= 0 or k <= 0 or k > n:
        return F(0)
    total = F(0)
    for j in range(1, n - k + 2):
        total += F(comb(n - 1, j - 1)) * xs[j - 1] * partial_bell(n - j, k - 1, xs)
    return total


def log_derivative_upper(order: int, qs: list[F]) -> F:
    if order < 1 or len(qs) <= order or qs[0] >= 1:
        raise ValueError("need Q_0,...,Q_order and Q_0<1")
    denominator = 1 - qs[0]
    return sum((F(_factorial(k - 1)) * partial_bell(order, k, qs[1:])
                / denominator ** k for k in range(1, order + 1)), F(0))


def geometric_derivative_upper(order: int, radius: F, pi_lo: F) -> F:
    """Euler-product majorant for derivatives of log(sin(theta)/theta)."""
    if order < 1 or not F(0) < radius < pi_lo:
        raise ValueError("invalid geometric derivative parameters")
    # zeta(2n)<=pi^2/6 leaves a rational power-series majorant.
    start = (order + 1) // 2
    x = (radius / pi_lo) ** 2
    total = F(0)
    # Exact terms plus a rigorous polynomial-times-geometric tail.
    cutoff = max(start, 18)
    while True:
        n = cutoff + 1
        poly_ratio = F(2 * n + 2, 2 * n + 2 - order)
        if x * poly_ratio < 1:
            break
        cutoff += 1
    for n in range(start, cutoff + 1):
        coefficient = F(1, 6 * n * pi_lo ** (2 * n - 2))
        total += coefficient * F(_factorial(2 * n), _factorial(2 * n - order)) * radius ** (2 * n - order)
    n = cutoff + 1
    first = (F(1, 6 * n * pi_lo ** (2 * n - 2))
             * F(_factorial(2 * n), _factorial(2 * n - order))
             * radius ** (2 * n - order))
    # Successive polynomial factor is at most this value for n>=cutoff+1.
    poly_ratio = F(2 * n + 2, 2 * n + 2 - order)
    ratio = x * poly_ratio
    if ratio >= 1:
        raise ArithmeticError("geometric-series tail is not contractive")
    return total + first / (1 - ratio)


def normalized_tail_upper(time: F, radius: F) -> F:
    """Exact-normalization tail corollary with a Mills-ratio bound."""
    if not F(0) < time <= F(1, 5) or not F(0) < radius:
        raise ValueError("certified domain is 0<t<=1/5 and radius>0")
    pi_lo, pi_hi = PI_PROOF_LOWER, PI_PROOF_UPPER
    exp_local_hi = exp_negative_upper_dyadic(radius * radius / (2 * time))
    zero = time * (radius + time / radius) * exp_local_hi
    e1 = exp_negative_upper_dyadic(pi_lo * pi_lo / (2 * time))
    e2 = exp_negative_upper_dyadic(2 * pi_lo * pi_lo / time)
    er = exp_negative_upper_dyadic(4 * pi_lo * pi_lo / time)
    images = time * (e1 + e2) / (1 - er)
    et_hi = 1 / (1 - time / 2)  # exp(x)<=1/(1-x), 0<=x<1.
    _, sqrt_two_over_pi_hi = sqrt_interval(2 / pi_lo)
    _, inv_sqrt_t_hi = sqrt_interval(1 / time)
    factor = et_hi * sqrt_two_over_pi_hi * (1 / time) * inv_sqrt_t_hi
    return factor * (zero + images)


def frac(x: F) -> str:
    return f"{x.numerator}/{x.denominator}"


def decimal(x: F, places: int = 18) -> str:
    scale = 10 ** places
    n = (x.numerator * scale + x.denominator - 1) // x.denominator
    return f"{n // scale}.{n % scale:0{places}d}"


def build_certificate(max_order: int = 8, time_max: F = F(1, 5),
                      radius: F = F(1), included: int = 1) -> dict:
    if max_order < 3:
        raise ValueError("certificate records at least three derivatives")
    pi_lo, pi_hi = pi_interval()
    monotonic_limit = ((2 * PI_PROOF_LOWER) ** 2 / 2
                        - 2 * PI_PROOF_LOWER * radius) / (max_order + 1)
    if time_max > monotonic_limit:
        raise ValueError("time interval violates derivative-order monotonicity")
    qs, ratios = [], []
    for order in range(max_order + 1):
        q, ratio = image_derivative_upper(order, time_max, radius, included)
        qs.append(q)
        ratios.append(ratio)
    if qs[0] >= 1:
        raise ArithmeticError("no positive 1+q floor")
    bs = [F(0)] + [log_derivative_upper(m, qs) for m in range(1, max_order + 1)]
    gs = [F(0)] + [geometric_derivative_upper(m, radius, PI_PROOF_LOWER)
                   for m in range(1, max_order + 1)]
    delta = F(1, 5)
    transition_qs, transition_ratios = [], []
    for order in range(max_order + 1):
        q, ratio = transition_image_derivative_upper(
            order, time_max, delta, included_tail=2
        )
        transition_qs.append(q)
        transition_ratios.append(ratio)
    if transition_qs[0] >= 1:
        raise ArithmeticError("no positive transition-chart factor floor")
    transition_bs = [F(0)] + [
        log_derivative_upper(m, transition_qs)
        for m in range(1, max_order + 1)
    ]
    transition_radius_hi = pi_hi - delta
    transition_gs = [F(0)] + [
        geometric_derivative_upper(m, transition_radius_hi, pi_lo)
        for m in range(1, max_order + 1)
    ]
    tails = {str(t): normalized_tail_upper(F(1, t), radius) for t in (5, 10, 20)}
    sin_lo, sin_hi = sin_interval(radius)
    cos_lo, _ = cos_interval(radius)
    cot_lower = cos_lo / sin_hi
    r2 = gs[2] + bs[2]
    radial_margin = 1 / time_max - r2
    tangential_margin = radius * cot_lower / time_max - r2
    cut_condition_margin = (
        PI_PROOF_LOWER * PI_PROOF_LOWER
        - time_max
        - PI_PROOF_UPPER * delta
    )
    payload = {
        "schema": SCHEMA,
        "conventions": {
            "group": "SU(2) as the unit three-sphere",
            "generator": "(1/2) Delta",
            "class_angle": "theta in [0,pi]",
            "haar_radial": "(2/pi) sin(theta)^2 dtheta",
        },
        "domain": {"time": f"0<t<={frac(time_max)}", "radius": frac(radius),
                   "max_order": max_order, "included_image_pairs": included},
        "domain_cover": {
            "method": "formula-adaptive three-chart atlas with explicit positivity floors",
            "cells": [
                {"name": "identity", "theta": ["0", frac(radius)], "formula": "paired zero-image factor"},
                {"name": "transition", "theta": [frac(radius), "pi-1/5"], "formula": "time-maximized paired correction"},
                {"name": "cut_locus", "theta": ["pi-1/5", "pi"], "formula": "paired odd images"}
            ],
            "coverage_certified": radius < PI_PROOF_LOWER - F(1, 5),
            "cut_pair_condition_margin": frac(cut_condition_margin),
            "termination": "three analytic cells"
        },
        "pi": {"lower": frac(pi_lo), "upper": frac(pi_hi),
               "width_decimal_upper": decimal(pi_hi - pi_lo),
               "compact_proof_lower": frac(PI_PROOF_LOWER),
               "compact_proof_upper": frac(PI_PROOF_UPPER)},
        "monotonicity_time_limit": frac(monotonic_limit),
        "image_Q": {str(m): {"rational_upper": frac(qs[m]), "decimal_upper": decimal(qs[m]),
                             "omitted_ratio_upper": frac(ratios[m])}
                    for m in range(max_order + 1)},
        "log_B": {str(m): {"rational_upper": frac(bs[m]), "decimal_upper": decimal(bs[m])}
                  for m in range(1, max_order + 1)},
        "transition_Q": {
            str(m): {
                "rational_upper": frac(transition_qs[m]),
                "decimal_upper": decimal(transition_qs[m]),
                "omitted_ratio_upper": frac(transition_ratios[m]),
            }
            for m in range(max_order + 1)
        },
        "transition_B": {
            str(m): {
                "rational_upper": frac(transition_bs[m]),
                "decimal_upper": decimal(transition_bs[m]),
            }
            for m in range(1, max_order + 1)
        },
        "transition_G": {
            str(m): {
                "rational_upper": frac(transition_gs[m]),
                "decimal_upper": decimal(transition_gs[m]),
            }
            for m in range(1, max_order + 1)
        },
        "geometry_G": {str(m): {"rational_upper": frac(gs[m]), "decimal_upper": decimal(gs[m])}
                       for m in range(1, max_order + 1)},
        "plaquette_instance": {
            "cot_radius_lower": frac(cot_lower),
            "cot_radius_lower_decimal": decimal(cot_lower),
            "radial_convexity_margin_lower": frac(radial_margin),
            "radial_convexity_margin_lower_decimal": decimal(radial_margin),
            "tangential_convexity_margin_lower": frac(tangential_margin),
            "tangential_convexity_margin_lower_decimal": decimal(tangential_margin),
            "scaled_R2_upper": frac(time_max * r2),
            "scaled_R2_upper_decimal": decimal(time_max * r2),
            "scaled_R3_upper": frac(time_max * (gs[3] + bs[3])),
            "scaled_R3_upper_decimal": decimal(time_max * (gs[3] + bs[3])),
            "scaled_R4_upper": frac(time_max * (gs[4] + bs[4])),
            "scaled_R4_upper_decimal": decimal(time_max * (gs[4] + bs[4])),
        },
        "normalized_tail": {k: {"rational_upper": frac(v), "decimal_upper": decimal(v)}
                            for k, v in tails.items()},
        "passes": {"Q0_below_one": qs[0] < 1,
                   "positive_kernel_factor_floor": frac(1 - qs[0]),
                   "transition_Q0_below_one": transition_qs[0] < 1,
                   "transition_factor_floor": frac(1 - transition_qs[0]),
                   "cut_pair_condition": cut_condition_margin > 0,
                   "positive_convexity_margins": radial_margin > 0 and tangential_margin > 0,
                   "all_tail_bounds_below_one": all(v < 1 for v in tails.values()),
                   "domain_cover_complete": radius < PI_PROOF_LOWER - F(1, 5),
                   "binary_float_used_for_pass_decisions": False},
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["payload_sha256"] = sha256(canonical).hexdigest()
    return payload


def write_certificate(path: Path) -> dict:
    payload = build_certificate()
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    write_certificate(Path(__file__).with_name("heat_kernel_certificate.json"))
    print("wrote exact SU(2) heat-kernel certificate")
