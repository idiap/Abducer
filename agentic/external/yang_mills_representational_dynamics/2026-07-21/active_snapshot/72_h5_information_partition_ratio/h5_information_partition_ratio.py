"""Finite information and partition-ratio core for hypothesis H5.

Everything in this module is finite.  The product tensorization theorem is an
algebraically exact restricted-model statement, while the executable
certificates use binary floating point.  The module does not assert a
quasi-factorization theorem for an interacting nonlinear Yang--Mills measure.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Hashable, Iterable, Sequence


TOL = 1.0e-12


def _probability_vector(values: Sequence[float], name: str) -> list[float]:
    if not values:
        raise ValueError(f"{name} must be nonempty")
    out = [float(x) for x in values]
    if any((not math.isfinite(x)) or x < 0.0 for x in out):
        raise ValueError(f"{name} must contain finite nonnegative entries")
    if abs(math.fsum(out) - 1.0) > TOL:
        raise ValueError(f"{name} must be normalized")
    return out


def kl_divergence(nu: Sequence[float], mu: Sequence[float]) -> float:
    """Return D(nu||mu), with infinity on support mismatch."""

    p = _probability_vector(nu, "nu")
    q = _probability_vector(mu, "mu")
    if len(p) != len(q):
        raise ValueError("nu and mu must have the same finite support")
    terms = []
    for x, y in zip(p, q):
        if x == 0.0:
            continue
        if y == 0.0:
            return math.inf
        terms.append(x * math.log(x / y))
    return math.fsum(terms)


def condition_on_event(mu: Sequence[float], event: Sequence[bool]) -> tuple[list[float], float]:
    q = _probability_vector(mu, "mu")
    if len(event) != len(q) or not any(event):
        raise ValueError("event must be a nonempty Boolean mask on the support")
    mass = math.fsum(x for x, flag in zip(q, event) if flag)
    if mass <= 0.0:
        raise ValueError("event must have positive mu mass")
    return ([x / mass if flag else 0.0 for x, flag in zip(q, event)], mass)


def event_kl_certificate(
    mu: Sequence[float], event: Sequence[bool], nu: Sequence[float]
) -> dict:
    """Certify D(nu||mu)=D(nu||mu(.|B))-log(mu(B))."""

    q = _probability_vector(mu, "mu")
    p = _probability_vector(nu, "nu")
    if len(q) != len(p) or len(event) != len(q):
        raise ValueError("mu, nu, and event must use the same support")
    if any(x > TOL and not flag for x, flag in zip(p, event)):
        raise ValueError("nu must be supported on the event")
    conditioned, mass = condition_on_event(q, event)
    lhs = kl_divergence(p, q)
    conditional_excess = kl_divergence(p, conditioned)
    optimum = -math.log(mass)
    if not math.isfinite(lhs) or not math.isfinite(conditional_excess):
        raise ValueError("nu must be absolutely continuous with respect to mu on the event")
    return {
        "event_mass": mass,
        "conditioned_measure": conditioned,
        "divergence_to_mu": lhs,
        "conditional_excess": conditional_excess,
        "variational_optimum": optimum,
        "chain_rule_residual": lhs - conditional_excess - optimum,
        "is_minimizer": conditional_excess <= TOL,
    }


def _pushforward(values: Sequence[float], labels: Sequence[Hashable]) -> tuple[list[float], list[str]]:
    if len(values) != len(labels):
        raise ValueError("coarse labels must have one entry per support point")
    order: list[Hashable] = []
    index: dict[Hashable, int] = {}
    for label in labels:
        try:
            present = label in index
        except TypeError as exc:
            raise ValueError("coarse labels must be hashable") from exc
        if not present:
            index[label] = len(order)
            order.append(label)
    out = [0.0] * len(order)
    for value, label in zip(values, labels):
        out[index[label]] += value
    return out, [str(x) for x in order]


def data_processing_certificate(
    nu: Sequence[float], mu: Sequence[float], labels: Sequence[Hashable]
) -> dict:
    p = _probability_vector(nu, "nu")
    q = _probability_vector(mu, "mu")
    if len(p) != len(q):
        raise ValueError("nu and mu must have the same support")
    coarse_p, names = _pushforward(p, labels)
    coarse_q, _ = _pushforward(q, labels)
    fine = kl_divergence(p, q)
    coarse = kl_divergence(coarse_p, coarse_q)
    return {
        "coarse_labels": names,
        "pushed_nu": coarse_p,
        "pushed_mu": coarse_q,
        "fine_divergence": fine,
        "coarse_divergence": coarse,
        "data_processing_gap": fine - coarse,
        "passes": fine + TOL >= coarse,
    }


def partition_ratio_certificate(z_bad: float, z_good: float, epsilon: float) -> dict:
    """Certify P(B)<=epsilon iff Z_B/Z_G<=epsilon/(1-epsilon)."""

    if any((not math.isfinite(x)) or x <= 0.0 for x in (z_bad, z_good)):
        raise ValueError("restricted partition functions must be finite and positive")
    if not math.isfinite(epsilon) or not 0.0 < epsilon < 1.0:
        raise ValueError("epsilon must lie strictly between zero and one")
    probability = z_bad / (z_bad + z_good)
    ratio = z_bad / z_good
    ratio_threshold = epsilon / (1.0 - epsilon)
    probability_bound = probability <= epsilon + TOL
    ratio_bound = ratio <= ratio_threshold + TOL
    return {
        "z_bad": z_bad,
        "z_good": z_good,
        "bad_probability": probability,
        "bad_good_ratio": ratio,
        "epsilon": epsilon,
        "ratio_threshold": ratio_threshold,
        "probability_bound": probability_bound,
        "ratio_bound": ratio_bound,
        "equivalence": probability_bound == ratio_bound,
        "algebraic_residual": probability - ratio / (1.0 + ratio),
    }


def multiplicity_counterexample(count: int = 1000, action_penalty: float = 5.0) -> dict:
    if count < 1 or not math.isfinite(action_penalty):
        raise ValueError("positive multiplicity and finite action penalty required")
    individual_weight = math.exp(-action_penalty)
    total_bad_weight = count * individual_weight
    return {
        "bad_multiplicity": count,
        "individual_action_penalty": action_penalty,
        "individual_weight": individual_weight,
        "total_bad_weight": total_bad_weight,
        "bad_probability": total_bad_weight / (1.0 + total_bad_weight),
        "entropy_minus_action": math.log(count) - action_penalty,
    }


def collapsing_normalizer_counterexample(levels: Iterable[int] = range(1, 13)) -> list[dict]:
    """Bad weight vanishes, yet bad probability tends to one."""

    rows = []
    for level in levels:
        if level < 1:
            raise ValueError("levels must be positive integers")
        z_bad = math.exp(-float(level))
        z_good = math.exp(-2.0 * float(level))
        rows.append(
            {
                "level": level,
                "z_bad": z_bad,
                "z_good": z_good,
                "normalizer": z_bad + z_good,
                "bad_probability": z_bad / (z_bad + z_good),
                "bad_good_ratio": z_bad / z_good,
            }
        )
    return rows


def product_reference(local_measures: Sequence[Sequence[float]]) -> tuple[list[tuple[int, ...]], list[float]]:
    locals_checked = [_probability_vector(row, f"local measure {j}") for j, row in enumerate(local_measures)]
    states = list(itertools.product(*(range(len(row)) for row in locals_checked)))
    probabilities = [math.prod(locals_checked[j][x] for j, x in enumerate(state)) for state in states]
    return states, probabilities


def _coordinate_marginals(
    probabilities: Sequence[float], states: Sequence[tuple[int, ...]], dimensions: Sequence[int]
) -> list[list[float]]:
    marginals = [[0.0] * d for d in dimensions]
    for mass, state in zip(probabilities, states):
        for j, x in enumerate(state):
            marginals[j][x] += mass
    return marginals


def product_tensorization_certificate(
    local_reference: Sequence[Sequence[float]], nu_joint: Sequence[float]
) -> dict:
    """Numerically certify finite tensorization by the exact chain rule."""

    states, reference = product_reference(local_reference)
    nu = _probability_vector(nu_joint, "nu_joint")
    if len(nu) != len(states):
        raise ValueError("nu_joint has the wrong product-space dimension")
    dimensions = [len(row) for row in local_reference]
    marginals = _coordinate_marginals(nu, states, dimensions)
    marginal_sum = math.fsum(
        kl_divergence(marginal, reference_local)
        for marginal, reference_local in zip(marginals, local_reference)
    )
    product_of_marginals = [math.prod(marginals[j][x] for j, x in enumerate(state)) for state in states]
    total_correlation = kl_divergence(nu, product_of_marginals)
    joint = kl_divergence(nu, reference)
    return {
        "number_of_blocks": len(local_reference),
        "joint_divergence": joint,
        "sum_local_divergences": marginal_sum,
        "total_correlation": total_correlation,
        "chain_rule_residual": joint - marginal_sum - total_correlation,
        "tensorization_gap": joint - marginal_sum,
        "c_qf_proved": 1.0,
        "passes": joint + TOL >= marginal_sum,
    }


def product_all_bad_certificate(number_of_blocks: int = 8, local_bad_probability: float = 0.2) -> dict:
    if number_of_blocks < 1 or not 0.0 < local_bad_probability < 1.0:
        raise ValueError("positive block count and a probability in (0,1) required")
    event_probability = local_bad_probability**number_of_blocks
    local_cost = -math.log(local_bad_probability)
    global_cost = -math.log(event_probability)
    return {
        "number_of_blocks": number_of_blocks,
        "local_bad_probability": local_bad_probability,
        "all_bad_probability": event_probability,
        "global_event_kl_cost": global_cost,
        "sum_local_event_kl_costs": number_of_blocks * local_cost,
        "additivity_residual": global_cost - number_of_blocks * local_cost,
        "decay_rate_per_block": global_cost / number_of_blocks,
    }


def interacting_common_bit_certificate(
    number_of_blocks: int, common_bad_probability: float = 0.2
) -> dict:
    """Full-support correlated law defeating a uniform local-KL sum bound.

    The law is (1-epsilon)[(1-p) delta_0^n + p delta_1^n] plus epsilon
    times the uniform product law, with epsilon=exp(-n^2).  Conditioning on
    the all-one atom costs only once globally but each local observation sees
    essentially the same cost.
    """

    if number_of_blocks < 2 or not 0.0 < common_bad_probability < 1.0:
        raise ValueError("at least two blocks and a probability in (0,1) required")
    n = number_of_blocks
    log_epsilon = -(n**2)
    epsilon = math.exp(log_epsilon)
    epsilon_underflowed = epsilon == 0.0
    all_bad_mass = (1.0 - epsilon) * common_bad_probability + epsilon * (2.0 ** (-n))
    marginal_bad_mass = (1.0 - epsilon) * common_bad_probability + epsilon * 0.5
    global_cost = -math.log(all_bad_mass)
    local_sum = n * (-math.log(marginal_bad_mass))
    return {
        "number_of_blocks": n,
        "regularization_epsilon_float": epsilon,
        "regularization_log_epsilon": log_epsilon,
        "float_regularization_underflowed": epsilon_underflowed,
        "full_support": True,
        "full_support_basis": "epsilon=exp(-n^2)>0 mathematically for every finite n",
        "all_bad_mass": all_bad_mass,
        "marginal_bad_mass": marginal_bad_mass,
        "global_event_kl_cost": global_cost,
        "sum_local_event_kl_costs": local_sum,
        "admissible_c_qf_ceiling": global_cost / local_sum,
        "product_c_qf_one_fails": global_cost + TOL < local_sum,
    }


def calibration() -> dict:
    mu = [0.1, 0.2, 0.3, 0.4]
    event = [False, False, True, True]
    conditioned, _ = condition_on_event(mu, event)
    candidate = [0.0, 0.0, 0.25, 0.75]
    minimizer_certificate = event_kl_certificate(mu, event, conditioned)
    candidate_certificate = event_kl_certificate(mu, event, candidate)

    fine_mu = [0.1, 0.2, 0.3, 0.4]
    fine_nu = [0.18, 0.12, 0.42, 0.28]
    dpi = data_processing_certificate(fine_nu, fine_mu, [0, 0, 1, 1])

    local_reference = [[0.8, 0.2], [0.7, 0.3], [0.6, 0.4]]
    correlated_nu = [0.22, 0.08, 0.05, 0.15, 0.06, 0.14, 0.10, 0.20]
    product_tensorization = product_tensorization_certificate(local_reference, correlated_nu)
    interacting = [interacting_common_bit_certificate(n) for n in (2, 4, 8, 12, 16, 20)]

    return {
        "stage": 72,
        "hypothesis": "H5: normalized free-energy/information rigidity",
        "event_kl": {
            "mu": mu,
            "event": event,
            "minimizer": minimizer_certificate,
            "nonminimizing_candidate": candidate_certificate,
        },
        "data_processing": dpi,
        "partition_ratio": {
            "boundary_case": partition_ratio_certificate(3.0, 17.0, 0.15),
            "strict_case": partition_ratio_certificate(2.0, 18.0, 0.15),
        },
        "counterexamples": {
            "multiplicity": multiplicity_counterexample(),
            "collapsing_normalizer": collapsing_normalizer_counterexample(),
        },
        "separated_blocks": {
            "proved_product_tensorization": product_tensorization,
            "proved_product_all_bad": product_all_bad_certificate(),
            "interacting_full_support_counterexample": interacting,
        },
        "claim_level": "C1 floating-point certificates of finite algebraic identities and counterexamples; C2 mathematical finite-product tensorization only",
        "arithmetic_contract": (
            "KL and partition-ratio outputs are binary floating-point evaluations; "
            "exactness refers only to the stated mathematical identities"
        ),
        "first_open_physical_implication": "Prove a boundary-, cutoff-, volume-, and history-uniform partition ratio or defect quasi-factorization for the actual nonlinear constrained Yang-Mills conditional measure.",
        "guardrails": {
            "nonlinear_yang_mills_quasi_factorization": False,
            "uniform_physical_partition_ratio": False,
            "retained_kernel_insertion": False,
            "continuum_construction": False,
            "os_mass_gap": False,
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
