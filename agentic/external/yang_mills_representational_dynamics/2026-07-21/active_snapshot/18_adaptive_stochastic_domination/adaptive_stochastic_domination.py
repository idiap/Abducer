"""Adaptive conditional probabilities imply stochastic domination.

For an ordered Boolean field X_1,...,X_N, suppose every positive-probability
history satisfies P(X_i=1 | X_1,...,X_{i-1})<=q_i.  A shared-uniform
sequential construction couples X below independent Bernoulli(q_i) variables.
This supplies a valid event-to-cluster conversion without identifying
Mayer/Ursell activities.

Intersection moment bounds alone are insufficient.  The distribution placing
mass 1/2 on 10 and 1/2 on 01 obeys P(X_i=1)<=1/2 and
P(X_1=X_2=1)<=1/4, yet the increasing union event has probability one rather
than 3/4 and a history conditional equals one.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import itertools
import json
import math
from pathlib import Path
import sys
from typing import Any, Mapping


STAGE14 = Path(__file__).resolve().parents[1] / "14_nonlinear_activity_transfer"
if str(STAGE14) not in sys.path:
    sys.path.insert(0, str(STAGE14))

from nonlinear_activity_transfer import transfer_certificate  # noqa: E402


Distribution = Mapping[tuple[int, ...], float]


@dataclass(frozen=True)
class DominationBudgetCertificate:
    site_bad_probability_bound: float
    alpha: float
    adjacency_degree: int
    critical_probability: float
    branching_ratio: float
    rooted_connected_sum_upper: float
    subcritical: bool
    adaptive_history_bound_required: bool
    shared_uniform_coupling_theorem_proved: bool
    stochastic_domination_conclusion_under_premise: bool
    mayer_activity_identification_required: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MomentCounterexampleCertificate:
    sites: int
    declared_moment_weight: float
    all_intersection_moment_bounds_hold: bool
    maximum_history_conditional: float
    actual_union_probability: float
    iid_union_probability: float
    stochastic_domination_holds: bool
    moment_bounds_suffice_for_domination: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AdaptiveBridgeCalibration:
    stage14_effective_weight: float
    domination_budget: DominationBudgetCertificate
    moment_counterexample: MomentCounterexampleCertificate
    abstract_conversion_gate_closed: bool
    full_su2_adaptive_history_bound_verified: bool
    full_su2_stochastic_domination_verified: bool
    first_unproved_implication: str
    claim_level: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _validate_distribution(distribution: Distribution) -> int:
    if not distribution:
        raise ValueError("distribution must be nonempty")
    keys = tuple(distribution)
    n = len(keys[0])
    if n < 1 or any(len(key) != n or any(bit not in (0, 1) for bit in key) for key in keys):
        raise ValueError("distribution keys must be equal-length Boolean tuples")
    values = tuple(float(distribution[key]) for key in keys)
    if any(not math.isfinite(p) or p < 0.0 for p in values):
        raise ValueError("probabilities must be finite and nonnegative")
    if abs(math.fsum(values) - 1.0) > 1.0e-12:
        raise ValueError("probabilities must sum to one")
    return n


def intersection_probability(distribution: Distribution, sites: tuple[int, ...]) -> float:
    n = _validate_distribution(distribution)
    if len(set(sites)) != len(sites) or any(not 0 <= i < n for i in sites):
        raise ValueError("sites must be distinct valid indices")
    return math.fsum(
        float(probability)
        for state, probability in distribution.items()
        if all(state[i] == 1 for i in sites)
    )


def all_intersection_moments_bounded(distribution: Distribution, q: float) -> bool:
    n = _validate_distribution(distribution)
    q = float(q)
    if not math.isfinite(q) or not 0.0 <= q <= 1.0:
        raise ValueError("q must lie in [0,1]")
    for size in range(1, n + 1):
        for sites in itertools.combinations(range(n), size):
            if intersection_probability(distribution, sites) > q**size + 1.0e-14:
                return False
    return True


def maximum_history_conditional(
    distribution: Distribution, order: tuple[int, ...] | None = None
) -> float:
    n = _validate_distribution(distribution)
    order = tuple(range(n)) if order is None else tuple(order)
    if sorted(order) != list(range(n)):
        raise ValueError("order must be a permutation of the sites")
    maximum = 0.0
    for position, site in enumerate(order):
        previous = order[:position]
        for history in itertools.product((0, 1), repeat=position):
            denominator = math.fsum(
                float(p)
                for state, p in distribution.items()
                if all(state[j] == bit for j, bit in zip(previous, history))
            )
            if denominator <= 0.0:
                continue
            numerator = math.fsum(
                float(p)
                for state, p in distribution.items()
                if state[site] == 1
                and all(state[j] == bit for j, bit in zip(previous, history))
            )
            maximum = max(maximum, numerator / denominator)
    return maximum


def union_probability(distribution: Distribution) -> float:
    _validate_distribution(distribution)
    return math.fsum(float(p) for state, p in distribution.items() if any(state))


def domination_budget(
    site_bad_probability_bound: float,
    alpha: float = 0.1,
    adjacency_degree: int = 18,
    adaptive_history_bound_verified: bool = True,
) -> DominationBudgetCertificate:
    q = float(site_bad_probability_bound)
    alpha = float(alpha)
    degree = int(adjacency_degree)
    if not math.isfinite(q) or not 0.0 <= q < 1.0:
        raise ValueError("site bad probability must lie in [0,1)")
    if not math.isfinite(alpha) or alpha < 0.0 or degree < 1:
        raise ValueError("invalid counting parameters")
    critical = math.exp(-alpha) / degree**2
    ratio = math.exp(alpha) * degree**2 * q
    rooted = math.exp(alpha) * q / (1.0 - ratio) if ratio < 1.0 else math.inf
    theorem_conclusion = bool(adaptive_history_bound_verified)
    return DominationBudgetCertificate(
        site_bad_probability_bound=q,
        alpha=alpha,
        adjacency_degree=degree,
        critical_probability=critical,
        branching_ratio=ratio,
        rooted_connected_sum_upper=rooted,
        subcritical=ratio < 1.0,
        adaptive_history_bound_required=True,
        shared_uniform_coupling_theorem_proved=True,
        stochastic_domination_conclusion_under_premise=theorem_conclusion,
        mayer_activity_identification_required=False,
    )


def moment_counterexample() -> MomentCounterexampleCertificate:
    distribution = {(1, 0): 0.5, (0, 1): 0.5}
    q = 0.5
    actual_union = union_probability(distribution)
    iid_union = 1.0 - (1.0 - q) ** 2
    maximum = maximum_history_conditional(distribution)
    moment_ok = all_intersection_moments_bounded(distribution, q)
    dominates = actual_union <= iid_union + 1.0e-14
    return MomentCounterexampleCertificate(
        sites=2,
        declared_moment_weight=q,
        all_intersection_moment_bounds_hold=moment_ok,
        maximum_history_conditional=maximum,
        actual_union_probability=actual_union,
        iid_union_probability=iid_union,
        stochastic_domination_holds=dominates,
        moment_bounds_suffice_for_domination=False,
    )


def calibration() -> AdaptiveBridgeCalibration:
    stage14 = transfer_certificate()
    q = stage14.combined_effective_weight
    # The numerical budget is evaluated under the theorem's adaptive-history
    # premise.  That premise is not yet verified for the nonlinear SU(2) law.
    budget = domination_budget(q, stage14.alpha, stage14.adjacency_degree, True)
    return AdaptiveBridgeCalibration(
        stage14_effective_weight=q,
        domination_budget=budget,
        moment_counterexample=moment_counterexample(),
        abstract_conversion_gate_closed=(
            budget.shared_uniform_coupling_theorem_proved and budget.subcritical
        ),
        full_su2_adaptive_history_bound_verified=False,
        full_su2_stochastic_domination_verified=False,
        first_unproved_implication=(
            "construct an adaptive multi-link/block exposure for the complete SU(2) "
            "measure and prove every positive-history bad-block conditional is at most "
            f"q_eff={q:.12g} uniformly in volume"
        ),
        claim_level="C2 finite stochastic-domination theorem with open SU(2) premise",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    args = parser.parse_args()
    print(json.dumps(calibration().to_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
