"""State-dependent tempered equivalence for changing weighted kernels.

This module contains finite positive-kernel mathematics only.  It does not
identify any kernel with Yang--Mills RG, an OS transfer operator, or a mass
gap.  The inequalities are algebraically exact; the executable certificates
use binary floating point with explicit tolerances.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


TOL = 1.0e-12


@dataclass(frozen=True)
class EquivalenceCertificate:
    dimensions: list[int]
    total_length: float
    a: list[float]
    b: list[float]
    scalar_centers: list[float]
    projective_half_widths: list[float]
    v_step_ceilings: list[float]
    w_step_ceilings: list[float]
    step_lower_factors: list[float]
    step_upper_factors: list[float]
    step_bounds_hold: bool
    v_product_ceiling: float
    w_product_ceiling: float
    product_lower_factor: float
    product_upper_factor: float
    product_bounds_hold: bool
    endpoint_log_coboundary: float
    cumulative_projective_width: float
    exact_centered_log_distortion: float
    centered_log_bound_holds: bool
    v_physical_rate: float
    w_physical_rate: float
    coboundary_predicted_w_rate: float
    rate_remainder: float
    rate_remainder_bound: float


@dataclass(frozen=True)
class DuhamelCertificate:
    exact_iterate: float
    homogeneous_term: float
    injected_terms: list[float]
    duhamel_sum: float
    identity_error: float


def _positive_weight(weight: Sequence[float], name: str) -> list[float]:
    out = [float(x) for x in weight]
    if not out:
        raise ValueError(f"{name} must be nonempty")
    if any((not math.isfinite(x)) or x <= 0.0 for x in out):
        raise ValueError(f"{name} must be finite and strictly positive")
    return out


def _kernel(
    kernel: Sequence[Sequence[float]], n_in: int, n_out: int
) -> list[list[float]]:
    if len(kernel) != n_in or any(len(row) != n_out for row in kernel):
        raise ValueError("kernel dimensions do not match adjacent weights")
    out = [[float(x) for x in row] for row in kernel]
    if any((not math.isfinite(x)) or x < 0.0 for row in out for x in row):
        raise ValueError("kernel entries must be finite and nonnegative")
    if any(math.fsum(row) > 1.0 + TOL for row in out):
        raise ValueError("kernel rows must be subprobability rows")
    return out


def _matvec(kernel: Sequence[Sequence[float]], vector: Sequence[float]) -> list[float]:
    return [math.fsum(x * y for x, y in zip(row, vector)) for row in kernel]


def exact_weighted_ceiling(
    kernel: Sequence[Sequence[float]],
    source_weight: Sequence[float],
    target_weight: Sequence[float],
) -> float:
    """Return the least q such that Q V_target <= q V_source."""

    source = _positive_weight(source_weight, "source weight")
    target = _positive_weight(target_weight, "target weight")
    checked = _kernel(kernel, len(source), len(target))
    ceiling = max(x / y for x, y in zip(_matvec(checked, target), source))
    if ceiling <= 0.0:
        raise ValueError("a positive ceiling is required for logarithmic rates")
    return ceiling


def equivalence_constants(
    v_weight: Sequence[float], w_weight: Sequence[float]
) -> tuple[float, float]:
    """Return sharp a,b in a V <= W <= b V."""

    v = _positive_weight(v_weight, "V")
    w = _positive_weight(w_weight, "W")
    if len(v) != len(w):
        raise ValueError("equivalent weights must live on the same state space")
    ratios = [y / x for x, y in zip(v, w)]
    return min(ratios), max(ratios)


def state_dependent_equivalence_certificate(
    kernels: Sequence[Sequence[Sequence[float]]],
    v_weights: Sequence[Sequence[float]],
    w_weights: Sequence[Sequence[float]],
    length_increments: Sequence[float],
) -> EquivalenceCertificate:
    """Certify two-sided transport under state-dependent weight equivalence.

    If a_n V_n <= W_n <= b_n V_n, then the exact step ceilings obey

      q^V_n a_{n+1}/b_n <= q^W_n <= q^V_n b_{n+1}/a_n.

    Writing c_n=sqrt(a_n b_n), eta_n=0.5 log(b_n/a_n), the logarithm of
    the product-ceiling ratio differs from log(c_N/c_0) by at most
    Omega_N=eta_0+eta_N+2 sum_{0<n<N} eta_n.
    """

    if not kernels:
        raise ValueError("at least one kernel is required")
    if len(v_weights) != len(kernels) + 1 or len(w_weights) != len(v_weights):
        raise ValueError("one V and W weight is required at every level")
    if len(length_increments) != len(kernels):
        raise ValueError("one physical-length increment per kernel is required")
    lengths = [float(x) for x in length_increments]
    if any((not math.isfinite(x)) or x <= 0.0 for x in lengths):
        raise ValueError("physical-length increments must be finite and positive")

    vs = [_positive_weight(weight, f"V[{n}]") for n, weight in enumerate(v_weights)]
    ws = [_positive_weight(weight, f"W[{n}]") for n, weight in enumerate(w_weights)]
    if any(len(v) != len(w) for v, w in zip(vs, ws)):
        raise ValueError("V and W dimensions must agree level by level")
    checked = [
        _kernel(kernel, len(vs[n]), len(vs[n + 1]))
        for n, kernel in enumerate(kernels)
    ]

    ab = [equivalence_constants(v, w) for v, w in zip(vs, ws)]
    a = [pair[0] for pair in ab]
    b = [pair[1] for pair in ab]
    centers = [math.sqrt(x * y) for x, y in ab]
    half_widths = [0.5 * math.log(y / x) for x, y in ab]

    qv = [exact_weighted_ceiling(k, vs[n], vs[n + 1]) for n, k in enumerate(checked)]
    qw = [exact_weighted_ceiling(k, ws[n], ws[n + 1]) for n, k in enumerate(checked)]
    lower = [a[n + 1] / b[n] for n in range(len(checked))]
    upper = [b[n + 1] / a[n] for n in range(len(checked))]
    step_holds = all(
        qv[n] * lower[n] <= qw[n] * (1.0 + TOL)
        and qw[n] <= qv[n] * upper[n] * (1.0 + TOL)
        for n in range(len(checked))
    )

    pv = math.prod(qv)
    pw = math.prod(qw)
    plower = math.prod(lower)
    pupper = math.prod(upper)
    product_holds = pv * plower <= pw * (1.0 + TOL) and pw <= pv * pupper * (1.0 + TOL)

    endpoint = math.log(centers[-1] / centers[0])
    omega = half_widths[0] + half_widths[-1] + 2.0 * math.fsum(half_widths[1:-1])
    centered = math.log(pw / pv) - endpoint
    centered_holds = abs(centered) <= omega + 10.0 * TOL
    length = math.fsum(lengths)
    mv = -math.log(pv) / length
    mw = -math.log(pw) / length
    predicted = mv - endpoint / length
    remainder = mw - predicted

    return EquivalenceCertificate(
        dimensions=[len(weight) for weight in vs],
        total_length=length,
        a=a,
        b=b,
        scalar_centers=centers,
        projective_half_widths=half_widths,
        v_step_ceilings=qv,
        w_step_ceilings=qw,
        step_lower_factors=lower,
        step_upper_factors=upper,
        step_bounds_hold=step_holds,
        v_product_ceiling=pv,
        w_product_ceiling=pw,
        product_lower_factor=plower,
        product_upper_factor=pupper,
        product_bounds_hold=product_holds,
        endpoint_log_coboundary=endpoint,
        cumulative_projective_width=omega,
        exact_centered_log_distortion=centered,
        centered_log_bound_holds=centered_holds,
        v_physical_rate=mv,
        w_physical_rate=mw,
        coboundary_predicted_w_rate=predicted,
        rate_remainder=remainder,
        rate_remainder_bound=omega / length,
    )


def duhamel_certificate(
    step_ceilings: Sequence[float], additive_errors: Sequence[float], initial: float
) -> DuhamelCertificate:
    """Evaluate the exact Duhamel formula in floating-point arithmetic."""

    if len(step_ceilings) != len(additive_errors) or not step_ceilings:
        raise ValueError("matching nonempty ceiling and error sequences are required")
    q = [float(x) for x in step_ceilings]
    r = [float(x) for x in additive_errors]
    x0 = float(initial)
    if any((not math.isfinite(x)) or x < 0.0 for x in q + r + [x0]):
        raise ValueError("ceilings, errors, and initial value must be finite and nonnegative")

    iterate = x0
    for factor, error in zip(q, r):
        iterate = factor * iterate + error
    homogeneous = x0 * math.prod(q)
    injected = [r[k] * math.prod(q[k + 1 :]) for k in range(len(q))]
    total = homogeneous + math.fsum(injected)
    return DuhamelCertificate(iterate, homogeneous, injected, total, abs(iterate - total))


def exponentially_weighted_error_budget(
    additive_errors: Sequence[float], cumulative_lengths_after_injection: Sequence[float], mass: float
) -> float:
    """Return sum r_k exp(m L_{k+1}), the sharp Duhamel target budget."""

    if len(additive_errors) != len(cumulative_lengths_after_injection):
        raise ValueError("one cumulative length per additive error is required")
    if not math.isfinite(mass) or mass < 0.0:
        raise ValueError("mass must be finite and nonnegative")
    pairs = [(float(r), float(length)) for r, length in zip(additive_errors, cumulative_lengths_after_injection)]
    if any((not math.isfinite(r)) or r < 0.0 or (not math.isfinite(length)) or length < 0.0 for r, length in pairs):
        raise ValueError("errors and cumulative lengths must be finite and nonnegative")
    return math.fsum(r * math.exp(mass * length) for r, length in pairs)


def scalar_coboundary_example(levels: int = 64, q: float = 0.72) -> dict:
    if levels < 2 or not 0.0 < q <= 1.0:
        raise ValueError("levels >=2 and q in (0,1] are required")
    kernels = [[[q]]] * levels
    v = [[1.0]] * (levels + 1)
    scalars = [math.exp(0.2 * math.sqrt(n + 1.0)) for n in range(levels + 1)]
    w = [[c] for c in scalars]
    cert = state_dependent_equivalence_certificate(kernels, v, w, [1.0] * levels)
    return {
        "certificate": asdict(cert),
        "exact_product_ratio": cert.w_product_ceiling / cert.v_product_ceiling,
        "endpoint_scalar_ratio": scalars[-1] / scalars[0],
        "tempered_endpoint_log_per_length": abs(math.log(scalars[-1] / scalars[0])) / levels,
        "projective_width_zero": cert.cumulative_projective_width == 0.0,
    }


def non_tempered_chart_countermodel(levels: int = 40, fake_mass: float = 0.35) -> dict:
    """Identity transport acquires a fake raw exponent in a horizon chart."""

    kernels = [[[1.0]]] * levels
    v = [[1.0]] * (levels + 1)
    scalars = [math.exp(fake_mass * (levels - n)) for n in range(levels + 1)]
    w = [[c] for c in scalars]
    cert = state_dependent_equivalence_certificate(kernels, v, w, [1.0] * levels)
    return {
        "levels": levels,
        "declared_fake_mass": fake_mass,
        "physical_identity_correlation": 1.0,
        "v_raw_rate": cert.v_physical_rate,
        "w_raw_rate": cert.w_physical_rate,
        "root_weight": scalars[0],
        "weighted_product": cert.w_product_ceiling,
        "root_times_product": scalars[0] * cert.w_product_ceiling,
        "endpoint_log_per_length": cert.endpoint_log_coboundary / levels,
        "lesson": "non-tempered endpoint normalization changes the raw exponent while the physical identity correlation is unchanged",
    }


def additive_error_countermodel(horizons: Sequence[int] = (20, 50, 100, 200, 500)) -> dict:
    """Summable polynomial injections destroy a homogeneous exponential rate."""

    q = math.exp(-1.0)
    rows = []
    for horizon in horizons:
        if horizon <= 0:
            raise ValueError("horizons must be positive")
        errors = [1.0 / (k + 2.0) ** 2 for k in range(horizon)]
        cert = duhamel_certificate([q] * horizon, errors, 1.0)
        rows.append(
            {
                "horizon": horizon,
                "iterate": cert.exact_iterate,
                "effective_rate": -math.log(cert.exact_iterate) / horizon,
                "ordinary_error_sum": math.fsum(errors),
                "target_weighted_budget": exponentially_weighted_error_budget(
                    errors, list(range(1, horizon + 1)), 1.0
                ),
            }
        )
    return {
        "homogeneous_mass": 1.0,
        "errors": "r_k=(k+2)^(-2), summable but not exponentially weighted-summable",
        "rows": rows,
        "last_effective_rate": rows[-1]["effective_rate"],
        "lesson": "ordinary summability of additive defects does not preserve a terminal exponential rate",
    }


def zero_error_without_homogeneous_rate_countermodel(horizon: int = 64) -> dict:
    """Show that an additive budget cannot replace homogeneous decay."""

    if not isinstance(horizon, int) or horizon < 1:
        raise ValueError("horizon must be a positive integer")
    ceilings = [1.0] * horizon
    errors = [0.0] * horizon
    cert = duhamel_certificate(ceilings, errors, 1.0)
    budget = exponentially_weighted_error_budget(
        errors, list(range(1, horizon + 1)), 1.0
    )
    return {
        "horizon": horizon,
        "additive_errors_identically_zero": True,
        "exponentially_weighted_error_budget": budget,
        "homogeneous_product": math.prod(ceilings),
        "terminal_iterate": cert.exact_iterate,
        "terminal_effective_rate": -math.log(cert.exact_iterate) / horizon,
        "target_positive_rate_certified": False,
        "lesson": (
            "zero additive error does not imply decay; the homogeneous product "
            "must independently satisfy the target exponential bound"
        ),
    }


def support_growth_countermodel(
    length: float = 30.0, transport_mass: float = 0.8, support_growth_rate: float = 0.8
) -> dict:
    if length <= 0.0 or transport_mass < 0.0 or support_growth_rate < 0.0:
        raise ValueError("length must be positive and rates nonnegative")
    transport = math.exp(-transport_mass * length)
    reconstruction = math.exp(support_growth_rate * length)
    observed = transport * reconstruction
    return {
        "physical_length": length,
        "transport_mass": transport_mass,
        "support_growth_rate": support_growth_rate,
        "transport_factor": transport,
        "reconstruction_factor": reconstruction,
        "observed_bound": observed,
        "observed_effective_rate": -math.log(observed) / length,
        "exact_rate_difference": transport_mass - support_growth_rate,
        "lesson": "observable reconstruction consumes the transport exponent and can cancel it exactly",
    }


def changing_space_example() -> dict:
    kernels = [
        [[0.10, 0.08, 0.02], [0.03, 0.20, 0.04]],
        [[0.15, 0.02], [0.01, 0.12], [0.06, 0.03]],
        [[0.11], [0.09]],
    ]
    v = [[1.0, 2.0], [1.5, 2.5, 4.0], [1.2, 3.0], [2.0]]
    w = [[1.1, 1.7], [2.1, 2.0, 5.2], [1.8, 2.4], [2.6]]
    return asdict(state_dependent_equivalence_certificate(kernels, v, w, [0.5, 1.0, 1.5]))


def calibration() -> dict:
    return {
        "stage": 69,
        "stream": "H2 state-dependent tempered equivalence",
        "claim_level": "C2 finite algebraic theorem with floating-point certificates and executable countermodels",
        "arithmetic_contract": (
            "the inequalities are exact mathematical statements; numerical "
            "certificates use binary floating point and tolerance checks"
        ),
        "theorem": {
            "step": "qV_n a_(n+1)/b_n <= qW_n <= qV_n b_(n+1)/a_n",
            "product": "the step factors multiply",
            "log_decomposition": "log(QW/QV)=log(c_N/c_0)+delta_N with |delta_N|<=Omega_N",
            "tempered_condition": "both |log(c_N/c_0)|/L_N and Omega_N/L_N vanish uniformly",
            "scalar_special_case": "a_n=b_n=c_n, Omega_N=0, so the product ratio telescopes exactly to c_N/c_0",
            "additive_condition": (
                "the homogeneous product must have rate m, every post-injection "
                "tail must have rate m, and sum_k r_k exp(m L_(k+1)) must remain "
                "uniformly bounded"
            ),
        },
        "changing_state_space_certificate": changing_space_example(),
        "scalar_coboundary": scalar_coboundary_example(),
        "countermodels": {
            "non_tempered_chart": non_tempered_chart_countermodel(),
            "additive_error": additive_error_countermodel(),
            "zero_error_without_homogeneous_rate": zero_error_without_homogeneous_rate_countermodel(),
            "support_growth_exact_cancellation": support_growth_countermodel(),
            "support_growth_overrun": support_growth_countermodel(support_growth_rate=1.0),
        },
        "guardrails": {
            "physical_yang_mills_kernel": False,
            "uniform_tempered_chart_atlas": False,
            "observable_pullback_control": False,
            "os_reconstruction": False,
            "continuum_mass_gap": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    payload = json.dumps(calibration(), indent=2, sort_keys=True) + "\n"
    if args.write:
        args.write.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
