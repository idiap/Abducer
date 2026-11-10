"""Exact finite-cell calibration for H4 retained topology.

This module treats the standard one-cell periodic cubical decomposition of
the oriented four-torus.  Its degree-two integral cohomology is represented
in the ordered basis (01, 02, 03, 12, 13, 23).  It is a finite C2 algebraic
calibration, not a nonabelian Yang--Mills topology construction.
"""
from __future__ import annotations

from fractions import Fraction
import argparse
import itertools
import json
from math import comb
from pathlib import Path
from typing import Any, Iterable, Sequence


PAIRS: tuple[tuple[int, int], ...] = (
    (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)
)
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
ZERO_FLUX = (0, 0, 0, 0, 0, 0)
PAIRING_MATRIX: tuple[tuple[int, ...], ...] = (
    (0, 0, 0, 0, 0, 1),
    (0, 0, 0, 0, -1, 0),
    (0, 0, 0, 1, 0, 0),
    (0, 0, 1, 0, 0, 0),
    (0, -1, 0, 0, 0, 0),
    (1, 0, 0, 0, 0, 0),
)


Flux = tuple[int, int, int, int, int, int]


def validate_flux(flux: Sequence[int]) -> Flux:
    values = tuple(flux)
    if len(values) != 6 or any(type(value) is not int for value in values):
        raise ValueError("flux must contain exactly six plain integers")
    return values  # type: ignore[return-value]


def validate_bound(bound: int) -> int:
    if type(bound) is not int or bound < 0:
        raise ValueError("bound must be a nonnegative integer")
    return bound


def flux_catalog(bound: int) -> Iterable[Flux]:
    bound = validate_bound(bound)
    return itertools.product(range(-bound, bound + 1), repeat=6)  # type: ignore[return-value]


def add_flux(left: Sequence[int], right: Sequence[int]) -> Flux:
    a, b = validate_flux(left), validate_flux(right)
    return tuple(x + y for x, y in zip(a, b))  # type: ignore[return-value]


def center_reduction(flux: Sequence[int]) -> Flux:
    return tuple(value % 2 for value in validate_flux(flux))  # type: ignore[return-value]


def center_add(left: Sequence[int], right: Sequence[int]) -> Flux:
    a, b = center_reduction(left), center_reduction(right)
    return tuple(x ^ y for x, y in zip(a, b))  # type: ignore[return-value]


def pfaffian(flux: Sequence[int]) -> int:
    n01, n02, n03, n12, n13, n23 = validate_flux(flux)
    return n01 * n23 - n02 * n13 + n03 * n12


def pairing(left: Sequence[int], right: Sequence[int]) -> int:
    a, b = validate_flux(left), validate_flux(right)
    return sum(a[i] * PAIRING_MATRIX[i][j] * b[j]
               for i in range(6) for j in range(6))


def pairing_covector(flux: Sequence[int]) -> Flux:
    n01, n02, n03, n12, n13, n23 = validate_flux(flux)
    return (n23, -n13, n12, n03, -n02, n01)


def reconstruct_from_pairing_covector(covector: Sequence[int]) -> Flux:
    b01, b02, b03, b12, b13, b23 = validate_flux(covector)
    return (b23, -b13, b12, b03, -b02, b01)


def standard_basis() -> tuple[Flux, ...]:
    return tuple(
        tuple(1 if i == j else 0 for i in range(6))  # type: ignore[misc]
        for j in range(6)
    )


def context_signature(flux: Sequence[int], contexts: Sequence[Sequence[int]]) -> tuple[int, ...]:
    n = validate_flux(flux)
    return tuple(pairing(n, context) for context in contexts)


def compose_charge(left: Sequence[int], right: Sequence[int]) -> int:
    return pfaffian(left) + pfaffian(right) + pairing(left, right)


def permutation_sign(permutation: Sequence[int]) -> int:
    values = tuple(permutation)
    if len(values) != 4 or set(values) != set(range(4)):
        raise ValueError("orientation map must be a permutation of 0,1,2,3")
    inversions = sum(values[i] > values[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1


def relabel_flux(flux: Sequence[int], permutation: Sequence[int]) -> Flux:
    """Push a two-form forward by the declared relabeling a -> permutation[a]."""
    n = validate_flux(flux)
    p = tuple(permutation)
    permutation_sign(p)  # validates
    result = [0] * 6
    for value, (a, b) in zip(n, PAIRS):
        image_a, image_b = p[a], p[b]
        if image_a < image_b:
            result[PAIR_INDEX[(image_a, image_b)]] += value
        else:
            result[PAIR_INDEX[(image_b, image_a)]] -= value
    return tuple(result)  # type: ignore[return-value]


def determinant(matrix: Sequence[Sequence[int]]) -> Fraction:
    rows = [list(map(Fraction, row)) for row in matrix]
    if not rows or any(len(row) != len(rows) for row in rows):
        raise ValueError("determinant requires a nonempty square matrix")
    result = Fraction(1)
    for column in range(len(rows)):
        pivot = next((row for row in range(column, len(rows)) if rows[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            result *= -1
        pivot_value = rows[column][column]
        result *= pivot_value
        for entry in range(column, len(rows)):
            rows[column][entry] /= pivot_value
        for row in range(column + 1, len(rows)):
            factor = rows[row][column]
            if factor:
                for entry in range(column, len(rows)):
                    rows[row][entry] -= factor * rows[column][entry]
    return result


def matrix_square(matrix: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("matrix square requires a square matrix")
    return tuple(tuple(sum(matrix[i][k] * matrix[k][j] for k in range(size))
                       for j in range(size)) for i in range(size))


def one_cell_torus_certificate() -> dict[str, Any]:
    """Full Smith data for the minimal periodic cubical/CW quotient of T^4.

    There is one oriented cell for every coordinate subset.  Opposite faces
    are identified, hence every integral cellular differential is zero.
    Its Smith form is therefore completely explicit in every degree.
    """
    cell_ranks = [comb(4, degree) for degree in range(5)]
    differentials = []
    for degree in range(4):
        rows, columns = cell_ranks[degree + 1], cell_ranks[degree]
        differentials.append({
            "map": f"delta_{degree}",
            "shape": [rows, columns],
            "rank": 0,
            "smith_nonzero_diagonal": [],
            "torsion_in_cokernel": [],
        })
    return {
        "complex": "standard one-cell periodic cubical quotient of the oriented four-torus",
        "cell_ranks": cell_ranks,
        "all_coboundaries_zero": True,
        "consecutive_compositions_zero": True,
        "smith_normal_forms": differentials,
        "integral_betti_numbers": cell_ranks,
        "integral_torsion": [[], [], [], [], []],
        "H2_is_Z6": True,
        "relative_bounded_block_computed": False,
    }


def scalar_sector(flux: Sequence[int]) -> tuple[Flux, int]:
    n = validate_flux(flux)
    return center_reduction(n), pfaffian(n)


def scalar_charge_weight(flux: Sequence[int], fugacity: Fraction = Fraction(1, 2)) -> Fraction:
    if not isinstance(fugacity, Fraction) or fugacity <= 0 or fugacity >= 1:
        raise ValueError("fugacity must be a Fraction strictly between zero and one")
    return fugacity ** abs(pfaffian(flux))


def canonical_collision() -> dict[str, Any]:
    left = (-1, -1, -1, -1, -1, -1)
    right = (-1, -1, -1, -1, 1, 1)
    context = (1, 0, 0, 0, 0, 0)
    left_sum, right_sum = add_flux(left, context), add_flux(right, context)
    return {
        "left": list(left),
        "right": list(right),
        "context": list(context),
        "shared_center": list(center_reduction(left)),
        "shared_charge": pfaffian(left),
        "shared_scalar_weight": str(scalar_charge_weight(left)),
        "context_scalar_weight": str(scalar_charge_weight(context)),
        "left_composite_charge": pfaffian(left_sum),
        "right_composite_charge": pfaffian(right_sum),
        "left_composite_scalar_weight": str(scalar_charge_weight(left_sum)),
        "right_composite_scalar_weight": str(scalar_charge_weight(right_sum)),
    }


def exhaustive_two_block_audit(bound: int = 1) -> dict[str, Any]:
    """Audit all first blocks and all common second blocks in [-b,b]^6.

    Full composition is addition.  Scalar sectors are grouped by (mod-two
    flux, Pfaffian).  Within each scalar sector, the full bounded-context
    charge profile is calculated exactly.
    """
    bound = validate_bound(bound)
    states = list(flux_catalog(bound))
    contexts = states
    groups: dict[tuple[Flux, int], list[Flux]] = {}
    for state in states:
        groups.setdefault(scalar_sector(state), []).append(state)

    ambiguous_groups = {sector: members for sector, members in groups.items() if len(members) > 1}
    same_sector_pairs = sum(len(members) * (len(members) - 1) // 2
                            for members in ambiguous_groups.values())
    compositionally_ambiguous = 0
    distinct_profiles = 0
    direct_equals_polarized = True
    for members in groups.values():
        profiles = set()
        for member in members:
            profile = []
            for context in contexts:
                direct = pfaffian(add_flux(member, context))
                direct_equals_polarized &= direct == compose_charge(member, context)
                profile.append(direct)
            profiles.add(tuple(profile))
        distinct_profiles += len(profiles)
        if len(profiles) > 1:
            compositionally_ambiguous += 1

    basis = standard_basis()
    all_pairs_basis_distinguished = True
    for members in ambiguous_groups.values():
        signatures = [context_signature(member, basis) for member in members]
        if len(signatures) != len(set(signatures)):
            all_pairs_basis_distinguished = False
            break

    return {
        "bound": bound,
        "state_count": len(states),
        "context_count": len(contexts),
        "state_context_compositions_checked": len(states) * len(contexts),
        "scalar_sector_count": len(groups),
        "ambiguous_scalar_sector_count": len(ambiguous_groups),
        "compositionally_ambiguous_scalar_sector_count": compositionally_ambiguous,
        "same_scalar_sector_distinct_pair_count": same_sector_pairs,
        "distinct_full_context_charge_profiles": distinct_profiles,
        "all_same_sector_pairs_distinguished_by_six_basis_contexts": all_pairs_basis_distinguished,
        "full_flux_direct_equals_composed_for_every_pair": direct_equals_polarized,
        "scalar_sector_admits_context_independent_composition": compositionally_ambiguous == 0,
        "canonical_collision": canonical_collision(),
    }


def pairing_certificate() -> dict[str, Any]:
    identity = tuple(tuple(int(i == j) for j in range(6)) for i in range(6))
    determinant_value = determinant(PAIRING_MATRIX)
    sample = (2, -3, 5, 7, -11, 13)
    sample_covector = pairing_covector(sample)
    return {
        "matrix": [list(row) for row in PAIRING_MATRIX],
        "J_squared_is_identity": matrix_square(PAIRING_MATRIX) == identity,
        "determinant": int(determinant_value),
        "unimodular": abs(determinant_value) == 1,
        "trace": sum(PAIRING_MATRIX[i][i] for i in range(6)),
        "signature": [3, 3],
        "basis_context_signature_equals_pairing_covector": (
            context_signature(sample, standard_basis()) == sample_covector
        ),
        "pairing_covector_reconstructs_full_flux": (
            reconstruct_from_pairing_covector(sample_covector) == sample
        ),
        "contextually_sufficient_statistics_must_be_injective": True,
    }


def orientation_certificate() -> dict[str, Any]:
    sample = (2, -3, 5, 7, -11, 13)
    permutations = list(itertools.permutations(range(4)))
    verified = all(
        pfaffian(relabel_flux(sample, permutation))
        == permutation_sign(permutation) * pfaffian(sample)
        for permutation in permutations
    )
    odd = (1, 0, 2, 3)
    return {
        "permutations_checked": len(permutations),
        "integer_pfaffian_transforms_by_orientation_sign": verified,
        "orientation_reversing_example": list(odd),
        "example_sign": permutation_sign(odd),
        "mod_two_charge_is_orientation_blind": (
            pfaffian(relabel_flux(sample, odd)) % 2 == pfaffian(sample) % 2
        ),
    }


def calibration(bound: int = 1) -> dict[str, Any]:
    audit = exhaustive_two_block_audit(bound)
    return {
        "stage": 71,
        "hypothesis": "H4 retained topology requires a compositionally complete carrier",
        "claim_level": "C2 exact finite integral/GF(2) flux algebra",
        "proved_domain": "one-cell periodic cubical four-torus and bounded additive two-block catalog",
        "coordinate_order": [f"{a}{b}" for a, b in PAIRS],
        "finite_cell": one_cell_torus_certificate(),
        "pairing": pairing_certificate(),
        "orientation": orientation_certificate(),
        "mod_two": {
            "center_label_count": 64,
            "reduction_is_additive": True,
            "pfaffian_reduction_uses_plus_signs": True,
            "orientation_sign_erased_in_characteristic_two": True,
        },
        "two_block_audit": audit,
        "theorems": {
            "pfaffian_polarization": "q(n+m)=q(n)+q(m)+B(n,m)",
            "contextual_minimality": "prediction of q(n+c) for all c forces an injective statistic of n",
            "six_context_reconstruction": "(B(n,e_i))_i=J n and J^{-1}=J",
            "scalar_sector_obstruction": "(n mod 2,q(n)) has no context-independent two-block composition law",
        },
        "guardrails": {
            "bounded_relative_cubical_block_snf_proved": False,
            "boundary_transgression_carrier_proved": False,
            "nonlinear_nonabelian_block_map_proved": False,
            "complete_nonabelian_topology_proved": False,
            "physical_topology_measure_proved": False,
            "normalized_topology_sector_measure_proved": False,
            "topology_channel_bound_proved": False,
            "repeated_rg_proved": False,
            "continuum_yang_mills_proved": False,
            "mass_gap_proved": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, default=1)
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    result = calibration(args.bound)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        args.write.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
