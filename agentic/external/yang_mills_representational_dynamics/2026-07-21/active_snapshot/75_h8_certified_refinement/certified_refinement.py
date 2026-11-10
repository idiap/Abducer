"""Exact finite partition refinement for retained-state kernels.

The module implements the finite C2 core of H8.  All kernel arithmetic uses
``fractions.Fraction``.  Floating-point inputs are rejected so that a reported
split always has an exact witness.  The result is an abstract certificate; no
physical SU(2) boundary-state kernel is constructed here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import argparse
import itertools
import json
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence


RationalInput = int | str | Fraction
Matrix = tuple[tuple[Fraction, ...], ...]
Partition = tuple[int, ...]


def rational(value: RationalInput) -> Fraction:
    """Parse an exact rational, deliberately rejecting bools and floats."""

    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError("use int, Fraction, or a rational/decimal string")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, (int, str)):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError(f"invalid rational value: {value!r}") from exc
    raise TypeError("use int, Fraction, or a rational/decimal string")


def validate_kernel(rows: Sequence[Sequence[RationalInput]]) -> Matrix:
    """Return a nonnegative square sub-Markov kernel in exact arithmetic."""

    if not isinstance(rows, Sequence) or not rows:
        raise ValueError("kernel must be a nonempty square sequence")
    n = len(rows)
    if any(not isinstance(row, Sequence) or len(row) != n for row in rows):
        raise ValueError("kernel must be square")
    matrix = tuple(tuple(rational(value) for value in row) for row in rows)
    if any(value < 0 for row in matrix for value in row):
        raise ValueError("kernel entries must be nonnegative")
    if any(sum(row, Fraction(0)) > 1 for row in matrix):
        raise ValueError("kernel rows must have mass at most one")
    return matrix


def canonical_partition(labels: Sequence[Any], size: int | None = None) -> Partition:
    """Canonicalize labels in first-occurrence order."""

    if not isinstance(labels, Sequence) or not labels:
        raise ValueError("partition must be nonempty")
    if size is not None and len(labels) != size:
        raise ValueError("partition length must match kernel size")
    dictionary: dict[Any, int] = {}
    result: list[int] = []
    for label in labels:
        try:
            if label not in dictionary:
                dictionary[label] = len(dictionary)
            result.append(dictionary[label])
        except TypeError as exc:
            raise TypeError("partition labels must be hashable") from exc
    return tuple(result)


def blocks(partition: Partition) -> tuple[tuple[int, ...], ...]:
    count = max(partition) + 1
    return tuple(tuple(i for i, label in enumerate(partition) if label == cell) for cell in range(count))


def aggregate_rows(matrix: Matrix, partition: Partition) -> tuple[tuple[Fraction, ...], ...]:
    cells = blocks(partition)
    return tuple(
        tuple(sum((matrix[i][j] for j in cell), Fraction(0)) for cell in cells)
        for i in range(len(matrix))
    )


def refine_once(matrix: Matrix, partition: Partition) -> Partition:
    aggregate = aggregate_rows(matrix, partition)
    signatures = tuple((partition[i], aggregate[i]) for i in range(len(matrix)))
    return canonical_partition(signatures, len(matrix))


def is_refinement(fine: Partition, coarse: Partition) -> bool:
    """Whether every fine cell is contained in a coarse cell."""

    if len(fine) != len(coarse):
        return False
    seen: dict[int, int] = {}
    for fine_label, coarse_label in zip(fine, coarse):
        previous = seen.setdefault(fine_label, coarse_label)
        if previous != coarse_label:
            return False
    return True


def equivalent_partition(left: Partition, right: Partition) -> bool:
    return is_refinement(left, right) and is_refinement(right, left)


def stable(matrix: Matrix, partition: Partition) -> bool:
    return equivalent_partition(refine_once(matrix, partition), partition)


def exact_lumpability_defect(matrix: Matrix, partition: Partition) -> Fraction:
    aggregate = aggregate_rows(matrix, partition)
    maximum = Fraction(0)
    for cell in blocks(partition):
        for i, j in itertools.combinations(cell, 2):
            for left, right in zip(aggregate[i], aggregate[j]):
                maximum = max(maximum, abs(left - right))
    return maximum


@dataclass(frozen=True)
class SplitWitness:
    round: int
    source_cell: tuple[int, ...]
    left_state: int
    right_state: int
    target_cell: tuple[int, ...]
    left_mass: Fraction
    right_mass: Fraction

    def to_dict(self) -> dict[str, Any]:
        return fraction_json(asdict(self))


def split_witnesses(
    matrix: Matrix, old: Partition, new: Partition, round_number: int
) -> tuple[SplitWitness, ...]:
    """Emit one exact distinguishing target cell for every pair of child cells."""

    if not is_refinement(new, old):
        raise ValueError("new partition must refine old partition")
    old_cells = blocks(old)
    aggregate = aggregate_rows(matrix, old)
    witnesses: list[SplitWitness] = []
    for source in old_cells:
        children: dict[int, list[int]] = {}
        for state in source:
            children.setdefault(new[state], []).append(state)
        child_cells = list(children.values())
        for left_child, right_child in itertools.combinations(child_cells, 2):
            left, right = left_child[0], right_child[0]
            for target_index, target in enumerate(old_cells):
                if aggregate[left][target_index] != aggregate[right][target_index]:
                    witnesses.append(
                        SplitWitness(
                            round=round_number,
                            source_cell=source,
                            left_state=left,
                            right_state=right,
                            target_cell=target,
                            left_mass=aggregate[left][target_index],
                            right_mass=aggregate[right][target_index],
                        )
                    )
                    break
            else:
                raise AssertionError("a declared split lacks a transition witness")
    return tuple(witnesses)


def verify_split_witness(
    matrix: Matrix, old: Partition, new: Partition, witness: SplitWitness
) -> bool:
    cells = blocks(old)
    if witness.source_cell not in cells or witness.target_cell not in cells:
        return False
    i, j = witness.left_state, witness.right_state
    if i not in witness.source_cell or j not in witness.source_cell or new[i] == new[j]:
        return False
    left = sum((matrix[i][k] for k in witness.target_cell), Fraction(0))
    right = sum((matrix[j][k] for k in witness.target_cell), Fraction(0))
    return left == witness.left_mass and right == witness.right_mass and left != right


@dataclass(frozen=True)
class RefinementCertificate:
    states: int
    initial_blocks: int
    final_blocks: int
    strict_rounds: int
    termination_bound: int
    history: tuple[Partition, ...]
    initial_defect: Fraction
    final_defect: Fraction
    monotone: bool
    terminated: bool
    stable: bool
    witnesses: tuple[SplitWitness, ...]
    all_witnesses_verified: bool

    def to_dict(self) -> dict[str, Any]:
        return fraction_json(asdict(self))


def refine_partition(
    rows: Sequence[Sequence[RationalInput]] | Matrix, labels: Sequence[Any]
) -> RefinementCertificate:
    matrix = validate_kernel(rows)
    initial = canonical_partition(labels, len(matrix))
    history: list[Partition] = [initial]
    witnesses: list[SplitWitness] = []
    current = initial
    while True:
        new = refine_once(matrix, current)
        if equivalent_partition(new, current):
            break
        if not is_refinement(new, current):
            raise AssertionError("refinement algorithm merged a cell")
        witnesses.extend(split_witnesses(matrix, current, new, len(history)))
        history.append(new)
        current = new
        if len(history) > len(matrix):
            raise AssertionError("finite termination bound was exceeded")
    monotone = all(is_refinement(fine, coarse) for coarse, fine in zip(history, history[1:]))
    verified = all(
        verify_split_witness(matrix, history[item.round - 1], history[item.round], item)
        for item in witnesses
    )
    initial_blocks = len(blocks(initial))
    return RefinementCertificate(
        states=len(matrix),
        initial_blocks=initial_blocks,
        final_blocks=len(blocks(current)),
        strict_rounds=len(history) - 1,
        termination_bound=len(matrix) - initial_blocks,
        history=tuple(history),
        initial_defect=exact_lumpability_defect(matrix, initial),
        final_defect=exact_lumpability_defect(matrix, current),
        monotone=monotone,
        terminated=(len(history) - 1 <= len(matrix) - initial_blocks),
        stable=stable(matrix, current),
        witnesses=tuple(witnesses),
        all_witnesses_verified=verified,
    )


def all_partitions(size: int) -> Iterator[Partition]:
    """Generate canonical restricted-growth strings."""

    if not isinstance(size, int) or size < 1:
        raise ValueError("size must be a positive integer")

    def extend(prefix: tuple[int, ...], maximum: int) -> Iterator[Partition]:
        if len(prefix) == size:
            yield prefix
            return
        for label in range(maximum + 2):
            yield from extend(prefix + (label,), max(maximum, label))

    yield from extend((0,), 0)


def exhaustive_coarsest_stable_check(
    rows: Sequence[Sequence[RationalInput]] | Matrix,
    initial_labels: Sequence[Any],
    candidate_labels: Sequence[Any],
    maximum_states: int = 8,
) -> dict[str, Any]:
    """Exhaustively check the coarsest-stable claim on a small fixture."""

    matrix = validate_kernel(rows)
    n = len(matrix)
    if n > maximum_states:
        raise ValueError("exhaustive partition check is restricted to small fixtures")
    initial = canonical_partition(initial_labels, n)
    candidate = canonical_partition(candidate_labels, n)
    admissible = [
        partition
        for partition in all_partitions(n)
        if is_refinement(partition, initial) and stable(matrix, partition)
    ]
    passed = (
        is_refinement(candidate, initial)
        and stable(matrix, candidate)
        and all(is_refinement(partition, candidate) for partition in admissible)
    )
    return {
        "partitions_enumerated": sum(1 for _ in all_partitions(n)),
        "stable_refinements_of_initial": len(admissible),
        "candidate_is_coarsest_stable": passed,
    }


def permute_kernel(matrix: Matrix, new_to_old: Sequence[int]) -> Matrix:
    permutation = tuple(new_to_old)
    n = len(matrix)
    if sorted(permutation) != list(range(n)):
        raise ValueError("new_to_old must be a state permutation")
    return tuple(tuple(matrix[permutation[i]][permutation[j]] for j in range(n)) for i in range(n))


def equivariance_check(matrix: Matrix, labels: Sequence[Any], new_to_old: Sequence[int]) -> bool:
    original = refine_partition(matrix, labels).history[-1]
    permuted_matrix = permute_kernel(matrix, new_to_old)
    permuted_labels = tuple(labels[old] for old in new_to_old)
    permuted = refine_partition(permuted_matrix, permuted_labels).history[-1]
    pulled = tuple(original[old] for old in new_to_old)
    return equivalent_partition(permuted, canonical_partition(pulled))


def stage52_kernel() -> Matrix:
    return validate_kernel(
        [
            ["9/10", 0, "1/10", 0],
            [0, "9/10", 0, "1/10"],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
        ]
    )


def stage18_moment_only_regression() -> dict[str, Any]:
    # P(10)=P(01)=1/2.  An indiscrete state observation is always lumpable,
    # yet it cannot certify Bernoulli domination.
    matrix = validate_kernel([[0, 1], [1, 0]])
    certificate = refine_partition(matrix, [0, 0])
    return {
        "distribution": {"10": "1/2", "01": "1/2"},
        "declared_q": "1/2",
        "singleton_moments_bounded": True,
        "intersection_moment_bounded": True,
        "actual_union_probability": "1",
        "iid_union_probability": "3/4",
        "maximum_positive_history_conditional": "1",
        "bernoulli_domination_holds": False,
        "indiscrete_partition_stable": certificate.stable,
        "refinement_detects_missing_history_from_indiscrete_seed": False,
        "lesson": "refinement cannot create an observable label absent from its seed partition",
    }


def stage19_weighted_two_state_regression() -> dict[str, Any]:
    legacy_decimal = "0.002430277501841998"
    q = rational(legacy_decimal)
    matrix = validate_kernel([[0, q * q], [1, 0]])
    weight = (Fraction(1), 1 / q)
    ratios = tuple(sum((matrix[i][j] * weight[j] for j in range(2)), Fraction(0)) / weight[i] for i in range(2))
    certificate = refine_partition(matrix, [0, 1])
    return {
        "q": str(q),
        "legacy_display_decimal": legacy_decimal,
        "q_origin": (
            "exact rational parsed from the displayed Stage 19 decimal; this "
            "is not an independent exact recovery of any underlying real parameter"
        ),
        "kernel": fraction_json(matrix),
        "weight": fraction_json(weight),
        "weighted_row_ratios": fraction_json(ratios),
        "exact_QV_equals_qV": all(value == q for value in ratios),
        "partition_certificate": certificate.to_dict(),
    }


CHANNELS = ("center", "continuous", "cut_orbit", "topology")


def star_kernel(
    entries: Sequence[Fraction], returns: Sequence[Fraction], persistence: Sequence[Fraction]
) -> Matrix:
    if not (len(entries) == len(returns) == len(persistence) == 4):
        raise ValueError("the H8 star fixture has exactly four channels")
    rows: list[list[Fraction]] = [[Fraction(0) for _ in range(5)] for _ in range(5)]
    rows[0][1:] = entries
    for index, (back, stay) in enumerate(zip(returns, persistence), 1):
        rows[index][0] = back
        rows[index][index] = stay
    return validate_kernel(rows)


def stage24_unequal_persistence_regression() -> dict[str, Any]:
    q = Fraction(1, 400)
    persistence = (Fraction(0), Fraction(1, 4000), Fraction(1, 3000), Fraction(1, 2500))
    returns = tuple(1 - value for value in persistence)
    entries = tuple(q * q / 8 for _ in CHANNELS)
    unequal = star_kernel(entries, returns, persistence)
    initial = (0, 1, 1, 1, 1)
    certificate = refine_partition(unequal, initial)
    weight = (Fraction(1),) + tuple(back / (q - stay) for back, stay in zip(returns, persistence))
    ratios = tuple(
        sum((unequal[i][j] * weight[j] for j in range(5)), Fraction(0)) / weight[i]
        for i in range(5)
    )

    equal_persistence = tuple(Fraction(0) for _ in CHANNELS)
    equal_returns = tuple(Fraction(1) for _ in CHANNELS)
    equal = star_kernel(entries, equal_returns, equal_persistence)
    equal_certificate = refine_partition(equal, initial)
    charged_permutation = (0, 3, 1, 4, 2)
    return {
        "channels": CHANNELS,
        "q": str(q),
        "persistence": fraction_json(persistence),
        "returns": fraction_json(returns),
        "entries": fraction_json(entries),
        "unequal_kernel": fraction_json(unequal),
        "unequal_partition_certificate": certificate.to_dict(),
        "canonical_weight": fraction_json(weight),
        "weighted_row_ratios": fraction_json(ratios),
        "weighted_ceiling_at_most_q": max(ratios) <= q,
        "equal_channel_partition_remains_two_blocks": equal_certificate.final_blocks == 2,
        "equal_channel_symmetry_preserved": equivariance_check(equal, initial, charged_permutation),
        "unequal_kernel_relabeling_equivariant": equivariance_check(unequal, initial, charged_permutation),
    }


def delayed_distinction_kernel(states: int) -> Matrix:
    """Deterministic chain that realizes the n-b termination bound."""

    if not isinstance(states, int) or states < 2:
        raise ValueError("states must be an integer at least two")
    rows = [[Fraction(0) for _ in range(states)] for _ in range(states)]
    for state in range(states):
        rows[state][max(0, state - 1)] = Fraction(1)
    return validate_kernel(rows)


def state_explosion_diagnostics(maximum_boundary_bits: int = 7) -> list[dict[str, Any]]:
    if not isinstance(maximum_boundary_bits, int) or not 1 <= maximum_boundary_bits <= 10:
        raise ValueError("boundary-bit range must lie between one and ten")
    diagnostics = []
    for bits in range(1, maximum_boundary_bits + 1):
        states = 2**bits
        matrix = delayed_distinction_kernel(states)
        initial = (0,) + tuple(1 for _ in range(states - 1))
        certificate = refine_partition(matrix, initial)
        diagnostics.append(
            {
                "boundary_bits": bits,
                "states": states,
                "initial_blocks": certificate.initial_blocks,
                "final_blocks": certificate.final_blocks,
                "strict_rounds": certificate.strict_rounds,
                "termination_bound": certificate.termination_bound,
                "bound_saturated": certificate.strict_rounds == certificate.termination_bound,
            }
        )
    return diagnostics


def fraction_json(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {str(key): fraction_json(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [fraction_json(item) for item in value]
    return value


def results() -> dict[str, Any]:
    stage52 = stage52_kernel()
    initial = (0, 0, 1, 1)
    certificate = refine_partition(stage52, initial)
    coarsest = exhaustive_coarsest_stable_check(stage52, initial, certificate.history[-1])
    permutation = (2, 0, 3, 1)
    return {
        "stage": 75,
        "hypothesis": "H8 hostile boundaries are retained-state completeness detectors",
        "claim_level": "C2 exact finite partition-refinement theorem and explicitly rationalized regressions",
        "theorem": {
            "statement": (
                "For every finite nonnegative sub-Markov kernel and seed partition, "
                "exact signature refinement terminates after at most n-b strict rounds "
                "at the unique coarsest stable refinement of the seed."
            ),
            "proof_status": "proved by finite partition induction; exhaustively checked on the Stage 52 fixture",
            "arithmetic": "fractions.Fraction only",
        },
        "stage52_reproduction": {
            "kernel": fraction_json(stage52),
            "initial_labels": list(initial),
            "certificate": certificate.to_dict(),
            "coarsest_stable_exhaustive_check": coarsest,
            "permutation_equivariance": equivariance_check(stage52, initial, permutation),
        },
        "regressions": {
            "stage18_moment_only": stage18_moment_only_regression(),
            "stage19_weighted_two_state": stage19_weighted_two_state_regression(),
            "stage24_unequal_persistence": stage24_unequal_persistence_regression(),
        },
        "state_explosion": state_explosion_diagnostics(),
        "scope": {
            "abstract_finite_theorem": True,
            "physical_su2_boundary_table_constructed": False,
            "uniform_volume_or_cutoff_control": False,
            "continuum_yang_mills": False,
            "mass_gap": False,
        },
        "first_open_physical_implication": (
            "construct a normalized finite SU(2) retained-boundary transition table, "
            "choose a gauge-invariant seed partition, and prove that its stable "
            "refinement has uniformly controlled size and weighted defect ceiling"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    payload = json.dumps(results(), indent=2, sort_keys=True) + "\n"
    if args.write:
        args.write.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
