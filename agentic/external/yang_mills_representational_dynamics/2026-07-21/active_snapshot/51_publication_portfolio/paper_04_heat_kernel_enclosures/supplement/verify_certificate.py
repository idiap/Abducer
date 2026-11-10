"""Independent structural verifier for the serialized rational certificate."""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
import json
import math
from pathlib import Path
import sys
from math import comb, factorial


sys.set_int_max_str_digits(200000)
HERE = Path(__file__).resolve().parent


def parse(value: str) -> F:
    n, d = value.split("/")
    return F(int(n), int(d))


def partial_bell(n: int, k: int, xs: list[F]) -> F:
    if n == k == 0:
        return F(1)
    if n <= 0 or k <= 0 or k > n:
        return F(0)
    return sum(
        (
            F(comb(n - 1, j - 1))
            * xs[j - 1]
            * partial_bell(n - j, k - 1, xs)
            for j in range(1, n - k + 2)
        ),
        F(0),
    )


def recompute_log_bounds(qs: list[F]) -> list[F]:
    d = 1 - qs[0]
    return [
        F(0)
    ] + [
        sum(
            (
                F(factorial(k - 1))
                * partial_bell(m, k, qs[1:])
                / d**k
                for k in range(1, m + 1)
            ),
            F(0),
        )
        for m in range(1, len(qs))
    ]


def verify(path: Path = HERE / "heat_kernel_certificate.json") -> dict:
    doc = json.loads(path.read_text(encoding="utf-8"))
    digest = doc.pop("payload_sha256")
    canonical = json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()
    checks = {
        "payload_hash": sha256(canonical).hexdigest() == digest,
        "schema": doc["schema"] == "su2-heat-kernel-enclosure-validation-v2",
        "pi_interval_inside_archimedean_bounds": (F(333, 106) < parse(doc["pi"]["lower"])
                                                   < parse(doc["pi"]["upper"]) < F(355, 113)),
        "Q0_strict": parse(doc["image_Q"]["0"]["rational_upper"]) < 1,
        "all_ratios_contractive": all(parse(v["omitted_ratio_upper"]) < 1 for v in doc["image_Q"].values()),
        "transition_Q0_strict": parse(doc["transition_Q"]["0"]["rational_upper"]) < 1,
        "transition_ratios_contractive": all(
            parse(v["omitted_ratio_upper"]) < 1
            for v in doc["transition_Q"].values()
        ),
        "all_log_bounds_positive": all(parse(v["rational_upper"]) > 0 for v in doc["log_B"].values()),
        "tails_are_probabilities": all(F(0) < parse(v["rational_upper"]) < 1 for v in doc["normalized_tail"].values()),
        "orders_contiguous": sorted(map(int, doc["image_Q"])) == list(range(9)),
        "transition_orders_contiguous": sorted(map(int, doc["transition_Q"])) == list(range(9)),
        "transition_geometry_orders_contiguous": sorted(
            map(int, doc["transition_G"])
        ) == list(range(1, 9)),
        "domain_cover": (doc["domain_cover"]["coverage_certified"] is True
                         and len(doc["domain_cover"]["cells"]) == 3
                         and doc["passes"]["domain_cover_complete"] is True),
        "no_float_pass": doc["passes"]["binary_float_used_for_pass_decisions"] is False,
    }
    qs = [parse(doc["image_Q"][str(m)]["rational_upper"]) for m in range(9)]
    tqs = [parse(doc["transition_Q"][str(m)]["rational_upper"]) for m in range(9)]
    bs = recompute_log_bounds(qs)
    tbs = recompute_log_bounds(tqs)
    checks.update(
        {
            "identity_floor_recomputed": parse(
                doc["passes"]["positive_kernel_factor_floor"]
            )
            == 1 - qs[0],
            "transition_floor_recomputed": parse(
                doc["passes"]["transition_factor_floor"]
            )
            == 1 - tqs[0],
            "identity_B_recomputed": all(
                parse(doc["log_B"][str(m)]["rational_upper"]) == bs[m]
                for m in range(1, 9)
            ),
            "transition_B_recomputed": all(
                parse(doc["transition_B"][str(m)]["rational_upper"]) == tbs[m]
                for m in range(1, 9)
            ),
            "cut_condition_positive": parse(
                doc["domain_cover"]["cut_pair_condition_margin"]
            )
            > 0,
        }
    )
    gs = [F(0)] + [
        parse(doc["geometry_G"][str(m)]["rational_upper"]) for m in range(1, 9)
    ]
    transition_gs = [
        parse(doc["transition_G"][str(m)]["rational_upper"])
        for m in range(1, 9)
    ]
    checks["transition_geometry_positive"] = all(x > 0 for x in transition_gs)
    inst = doc["plaquette_instance"]
    checks.update(
        {
            "plaquette_R2_recomputed": parse(inst["scaled_R2_upper"])
            == F(1, 5) * (gs[2] + bs[2]),
            "plaquette_R3_recomputed": parse(inst["scaled_R3_upper"])
            == F(1, 5) * (gs[3] + bs[3]),
            "plaquette_R4_recomputed": parse(inst["scaled_R4_upper"])
            == F(1, 5) * (gs[4] + bs[4]),
            "radial_margin_recomputed": parse(
                inst["radial_convexity_margin_lower"]
            )
            == 5 - (gs[2] + bs[2]),
            "tangential_margin_recomputed": parse(
                inst["tangential_convexity_margin_lower"]
            )
            == 5 * parse(inst["cot_radius_lower"]) - (gs[2] + bs[2]),
        }
    )
    doc["payload_sha256"] = digest
    if not all(checks.values()):
        raise AssertionError(checks)
    return checks


def character_kernel(theta: float, time: float, cutoff: int = 160) -> float:
    if math.isclose(theta, math.pi):
        return sum(
            (n + 1) ** 2
            * (-1) ** n
            * math.exp(-n * (n + 2) * time / 2)
            for n in range(cutoff + 1)
        )
    return sum((n + 1) * math.exp(-n * (n + 2) * time / 2)
               * (n + 1 if theta == 0 else math.sin((n + 1) * theta) / math.sin(theta))
               for n in range(cutoff + 1))


def image_kernel(theta: float, time: float, images: int = 6) -> float:
    c = math.exp(time / 2) * math.sqrt(2 * math.pi) / (2 * time ** 1.5)
    if theta == 0:
        shape = sum((1 - (2 * math.pi * k) ** 2 / time)
                    * math.exp(-(2 * math.pi * k) ** 2 / (2 * time))
                    for k in range(-images, images + 1))
    elif math.isclose(theta, math.pi):
        shape = sum(
            (((math.pi + 2 * math.pi * k) ** 2 / time) - 1)
            * math.exp(-(math.pi + 2 * math.pi * k) ** 2 / (2 * time))
            for k in range(-images, images + 1)
        )
    else:
        shape = sum((theta + 2 * math.pi * k)
                    * math.exp(-(theta + 2 * math.pi * k) ** 2 / (2 * time))
                    for k in range(-images, images + 1)) / math.sin(theta)
    return c * shape


def crosscheck_formulas() -> dict:
    errors = []
    for time in (0.1, 0.2, 0.5):
        for theta in (0.0, 0.2, 0.6, 1.0, 2.0, 3.0, math.pi):
            a, b = character_kernel(theta, time), image_kernel(theta, time)
            errors.append(abs(a - b) / max(1.0, abs(a), abs(b)))
    result = {"cells": len(errors), "maximum_relative_or_absolute_error": max(errors)}
    if result["maximum_relative_or_absolute_error"] > 2e-12:
        raise AssertionError(result)
    return result


if __name__ == "__main__":
    print(json.dumps({"certificate": verify(), "formula_crosscheck": crosscheck_formulas()}, indent=2))
