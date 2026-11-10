"""Executable first probes for the ten conceptual Yang--Mills hypotheses.

The probes are deliberately finite or abstract.  They test algebraic
mechanisms and mandatory counterexamples; they do not establish nonlinear
Yang--Mills estimates, RG basin entry, a continuum theory, or a mass gap.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "hypothesis_probe_results.json"


def h1_vacuum_weight_probe(q: float = 0.08) -> dict[str, object]:
    """Exact two-state Perron weight defeating the scalar worst-row ceiling."""
    if not 0.0 < q < 1.0:
        raise ValueError("q must lie in (0,1)")
    kernel = np.array([[0.0, q * q], [1.0, 0.0]])
    weight = np.array([q, 1.0])
    ratios = kernel @ weight / weight
    return {
        "hypothesis": "H1 vacuum weight as coarse ground-state amplitude",
        "kernel": kernel.tolist(),
        "positive_weight": weight.tolist(),
        "weighted_row_ratios": ratios.tolist(),
        "weighted_ceiling": float(np.max(ratios)),
        "spectral_radius": float(max(abs(np.linalg.eigvals(kernel)))),
        "scalar_row_ceiling": float(np.max(np.sum(kernel, axis=1))),
        "status": "survives exact finite-matrix probe",
        "claim_level": "C1 toy positive-kernel certificate",
    }


def _cocycle_rate(factors: Sequence[float], lengths: Sequence[float]) -> float:
    f = np.asarray(factors, dtype=float)
    ell = np.asarray(lengths, dtype=float)
    if f.shape != ell.shape or f.ndim != 1 or f.size == 0:
        raise ValueError("factors and lengths must be equal nonempty vectors")
    if np.any(f <= 0.0) or np.any(f > 1.0) or np.any(ell <= 0.0):
        raise ValueError("factors must lie in (0,1] and lengths must be positive")
    return float(-np.sum(np.log(f)) / np.sum(ell))


def h2_lyapunov_gap_probe() -> dict[str, object]:
    """Show why strict stepwise contraction is weaker than a physical rate."""
    uniform_q = 0.7
    uniform_rate = _cocycle_rate([uniform_q] * 20, [1.0] * 20)
    n = np.arange(1.0, 401.0)
    nonuniform = np.exp(-1.0 / n)
    nonuniform_rate = _cocycle_rate(nonuniform, np.ones_like(nonuniform))
    return {
        "hypothesis": "H2 mass as a negative Lyapunov exponent",
        "uniform_factor": uniform_q,
        "uniform_physical_rate": uniform_rate,
        "expected_uniform_rate": -math.log(uniform_q),
        "strict_but_nonuniform_factors": "exp(-1/n), n=1,...,400",
        "finite_horizon_nonuniform_rate": nonuniform_rate,
        "asymptotic_nonuniform_rate": 0.0,
        "lesson": "q_n<1 at every scale is insufficient; an extensive physical log contraction is required",
        "status": "sharpened by a counterexample",
        "claim_level": "C1 exact scalar-cocycle calculation",
    }


def _shift(x: tuple[int, ...], direction: int) -> tuple[int, ...]:
    y = list(x)
    y[direction] += 1
    return tuple(y)


def block_incidence() -> tuple[np.ndarray, tuple[tuple[tuple[int, ...], int], ...], tuple]:
    """Integer d1 for the open side-two four-cube."""
    vertices = tuple(itertools.product(range(3), repeat=4))
    edges = tuple((x, mu) for x in vertices for mu in range(4) if x[mu] < 2)
    edge_index = {edge: i for i, edge in enumerate(edges)}
    plaquettes = tuple(
        (x, mu, nu)
        for x in vertices
        for mu in range(4)
        for nu in range(mu + 1, 4)
        if x[mu] < 2 and x[nu] < 2
    )
    d1 = np.zeros((len(plaquettes), len(edges)), dtype=float)
    for row, (x, mu, nu) in enumerate(plaquettes):
        d1[row, edge_index[(x, mu)]] = 1.0
        d1[row, edge_index[(_shift(x, mu), nu)]] = 1.0
        d1[row, edge_index[(_shift(x, nu), mu)]] = -1.0
        d1[row, edge_index[(x, nu)]] = -1.0
    return d1, edges, plaquettes


def interior_links(d1: np.ndarray) -> tuple[int, ...]:
    degree = np.sum(np.abs(d1) > 0.0, axis=0)
    return tuple(int(i) for i in np.flatnonzero(degree == 6))


def _centered_oriented_star_map(d1: np.ndarray, link: int) -> tuple[np.ndarray, np.ndarray]:
    selected = np.flatnonzero(np.abs(d1[:, link]) > 0.0)
    selector = d1[selected]
    orientation = np.diag(d1[selected, link])
    center = np.eye(6) - np.ones((6, 6)) / 6.0
    return center @ orientation @ selector, selected


def minimum_polymer_spill(d1: np.ndarray, links: Iterable[int]) -> dict[str, object]:
    """Numerically minimize external curvature for all feasible polymer data.

    If A maps link variations to the stacked centered star data and B maps
    them to plaquettes outside the polymer star union, eliminate ker(A) from
    B and diagonalize the resulting minimum-cost form on im(A).
    """
    chosen = tuple(int(link) for link in links)
    maps: list[np.ndarray] = []
    selected_rows: set[int] = set()
    for link in chosen:
        star, selected = _centered_oriented_star_map(d1, link)
        maps.append(star)
        selected_rows.update(map(int, selected))
    a = np.vstack(maps)
    external = np.array(sorted(set(range(d1.shape[0])) - selected_rows), dtype=int)
    b = d1[external]
    u, singular, vh = np.linalg.svd(a, full_matrices=True)
    tolerance = 1.0e-10
    rank = int(np.sum(singular > tolerance))
    vr = vh[:rank].T
    x0 = vr / singular[:rank]
    null = vh[rank:].T
    bn = b @ null
    if bn.size:
        ub, sb, _ = np.linalg.svd(bn, full_matrices=False)
        brank = int(np.sum(sb > tolerance))
        projector = ub[:, :brank] @ ub[:, :brank].T
    else:
        projector = np.zeros((len(external), len(external)))
    transfer = (np.eye(len(external)) - projector) @ b @ x0
    spectrum = np.linalg.eigvalsh(transfer.T @ transfer)
    spectrum[np.abs(spectrum) < 1.0e-10] = 0.0
    positive = spectrum[spectrum > 1.0e-9]
    return {
        "links": list(chosen),
        "star_data_rank": rank,
        "star_union_plaquettes": len(selected_rows),
        "external_plaquettes": len(external),
        "zero_spill_modes": int(np.sum(spectrum == 0.0)),
        "positive_modes": int(len(positive)),
        "minimum_positive_spill": None if not len(positive) else float(positive[0]),
        "maximum_spill": None if not len(positive) else float(positive[-1]),
        "spectrum": [float(value) for value in spectrum],
    }


def h3_polymer_spill_probe() -> dict[str, object]:
    d1, edges, _ = block_incidence()
    links = interior_links(d1)
    nested = {
        "one_star": (links[0],),
        "adjacent_pair": (links[0], links[4]),
        "central_four_directions": links[4:8],
        "all_eight_interior_links": links,
    }
    probes = {name: minimum_polymer_spill(d1, subset) for name, subset in nested.items()}
    one = np.asarray(probes["one_star"]["spectrum"])
    exact = np.asarray([37 / 33] * 3 + [391 / 239] * 2)
    exact_match = bool(np.allclose(one, exact, atol=2.0e-9, rtol=2.0e-9))
    return {
        "hypothesis": "H3 coordinated polymer spill obeys a boundary law",
        "interior_link_coordinates": [str(edges[index]) for index in links],
        "nested_polymer_probes": probes,
        "single_star_matches_exact_paper05_spectrum": exact_match,
        "boundary_law_established": False,
        "status": "open; finite probes test cancellation but do not establish scaling",
        "claim_level": "C1 numerical multi-star diagnostic with C2 single-star cross-check",
    }


def _center(flux: Sequence[int]) -> tuple[int, ...]:
    return tuple(int(value) % 2 for value in flux)


def _pfaffian(flux: Sequence[int]) -> int:
    n01, n02, n03, n12, n13, n23 = map(int, flux)
    return n01 * n23 - n02 * n13 + n03 * n12


def _find_contextual_topology_collision() -> dict[str, object]:
    states = list(itertools.product(range(-1, 2), repeat=6))
    groups: dict[tuple[tuple[int, ...], int], list[tuple[int, ...]]] = {}
    for state in states:
        groups.setdefault((_center(state), _pfaffian(state)), []).append(state)
    contexts = [tuple(1 if i == j else 0 for i in range(6)) for j in range(6)]
    contexts += [tuple(-value for value in context) for context in contexts]
    for (label, charge), group in groups.items():
        if len(group) < 2:
            continue
        for left, right in itertools.combinations(group, 2):
            for context in contexts:
                left_sum = tuple(a + b for a, b in zip(left, context))
                right_sum = tuple(a + b for a, b in zip(right, context))
                if _pfaffian(left_sum) != _pfaffian(right_sum):
                    return {
                        "shared_center_label": list(label),
                        "shared_pfaffian_charge": charge,
                        "left_flux": list(left),
                        "right_flux": list(right),
                        "common_added_context": list(context),
                        "left_blocked_charge": _pfaffian(left_sum),
                        "right_blocked_charge": _pfaffian(right_sum),
                    }
    raise AssertionError("expected a contextual topology collision")


def h4_graded_cocycle_probe() -> dict[str, object]:
    collision = _find_contextual_topology_collision()
    return {
        "hypothesis": "H4 retained topology is a graded cocycle",
        "contextual_collision": collision,
        "center_plus_pfaffian_is_compositionally_sufficient": False,
        "full_six_component_integer_flux_is_additively_closed": True,
        "lesson": "retain the integer flux lift or equivalent bilinear pairing data, not only center and total charge",
        "status": "sharpened: a smaller proposed topology state is falsified",
        "claim_level": "C2 exact finite integral-flux obstruction",
    }


def _kl(p: np.ndarray, q: np.ndarray) -> float:
    mask = p > 0.0
    return float(np.sum(p[mask] * np.log(p[mask] / q[mask])))


def h5_free_energy_probe() -> dict[str, object]:
    weights = np.array([1.0, 2.0, 4.0, 8.0])
    mu = weights / np.sum(weights)
    event = np.array([False, False, True, True])
    conditional = np.where(event, mu / np.sum(mu[event]), 0.0)
    event_cost = -math.log(float(np.sum(mu[event])))
    conditional_kl = _kl(conditional, mu)

    p = np.array([0.1, 0.2, 0.3, 0.4])
    q = np.array([0.25, 0.25, 0.25, 0.25])
    coarse_p = np.array([p[:2].sum(), p[2:].sum()])
    coarse_q = np.array([q[:2].sum(), q[2:].sum()])

    action_charge = 5.0
    multiplicity = 1000
    bad_mass = multiplicity * math.exp(-action_charge)
    bad_probability = bad_mass / (1.0 + bad_mass)
    return {
        "hypothesis": "H5 free-energy rigidity is more fundamental than action rigidity",
        "event_probability": float(np.sum(mu[event])),
        "negative_log_event_probability": event_cost,
        "conditional_relative_entropy": conditional_kl,
        "variational_identity_error": abs(event_cost - conditional_kl),
        "fine_relative_entropy": _kl(p, q),
        "coarse_relative_entropy": _kl(coarse_p, coarse_q),
        "data_processing_verified": _kl(coarse_p, coarse_q) <= _kl(p, q) + 1.0e-14,
        "action_only_counterexample": {
            "individual_charge": action_charge,
            "bad_state_multiplicity": multiplicity,
            "normalized_bad_probability": bad_probability,
        },
        "status": "survives exact discrete identities; physical quasi-factorization remains open",
        "claim_level": "C1 finite probability-space certificate",
    }


def h6_representation_curvature_probe() -> dict[str, object]:
    d1, _, _ = block_incidence()
    link = interior_links(d1)[0]
    selected = np.flatnonzero(np.abs(d1[:, link]) > 0.0)
    signs = d1[selected, link]
    center = np.eye(6) - np.ones((6, 6)) / 6.0
    orientation = np.diag(signs)
    commutator = center @ orientation - orientation @ center
    projection = d1 @ np.linalg.pinv(d1)
    block = projection[np.ix_(selected, selected)]
    raw = center @ block @ center
    corrected = center @ orientation @ block @ orientation @ center
    return {
        "hypothesis": "H6 representation changes possess curvature defects",
        "incident_orientation_signs": [int(value) for value in signs],
        "centering_orientation_commutator_rank": int(np.linalg.matrix_rank(commutator, tol=1.0e-10)),
        "centering_orientation_commutator_norm": float(np.linalg.norm(commutator, ord=2)),
        "raw_centered_covariance_spectrum": [float(x) for x in np.linalg.eigvalsh(raw)],
        "oriented_centered_covariance_spectrum": [float(x) for x in np.linalg.eigvalsh(corrected)],
        "path_independent": bool(np.linalg.norm(raw - corrected) < 1.0e-12),
        "status": "noncommutation detected; geometric interpretation remains conjectural",
        "claim_level": "C1 exact-matrix/numerical-rank diagnostic",
    }


def _su2_exp(x: np.ndarray) -> np.ndarray:
    radius = float(np.linalg.norm(x))
    if radius == 0.0:
        return np.array([1.0, 0.0, 0.0, 0.0])
    return np.concatenate(([math.cos(radius)], math.sin(radius) * x / radius))


def _center_coordinate(q: np.ndarray) -> tuple[int, np.ndarray]:
    q = q / np.linalg.norm(q)
    center = 1 if q[0] >= 0.0 else -1
    local = center * q
    angle = math.acos(float(np.clip(local[0], -1.0, 1.0)))
    vector_norm = float(np.linalg.norm(local[1:]))
    coordinate = np.zeros(3) if vector_norm < 1.0e-14 else angle * local[1:] / vector_norm
    return center, coordinate


def h7_atlas_locality_probe(samples: int = 5000) -> dict[str, object]:
    rng = np.random.default_rng(20260721)
    quaternions = rng.normal(size=(samples, 4))
    quaternions /= np.linalg.norm(quaternions, axis=1)[:, None]
    radii: list[float] = []
    errors: list[float] = []
    for q in quaternions:
        center, coordinate = _center_coordinate(q)
        reconstructed = center * _su2_exp(coordinate)
        radii.append(float(np.linalg.norm(coordinate)))
        errors.append(float(np.linalg.norm(q - reconstructed)))
    minus_identity = np.array([-1.0, 0.0, 0.0, 0.0])
    center, coordinate = _center_coordinate(minus_identity)
    return {
        "hypothesis": "H7 locality is atlas-relative",
        "deterministic_samples": samples,
        "maximum_two_center_radius": max(radii),
        "certified_global_radius_bound": math.pi / 2.0,
        "maximum_reconstruction_error": max(errors),
        "minus_identity_selected_center": center,
        "minus_identity_local_radius": float(np.linalg.norm(coordinate)),
        "single_identity_log_chart_global": False,
        "status": "supported for the exact two-center SU(2) coordinate atlas",
        "claim_level": "C1 sampling check backed by the package's C2 atlas theorem",
    }


def _aggregate_rows(matrix: np.ndarray, labels: Sequence[int]) -> np.ndarray:
    blocks = sorted(set(labels))
    return np.array([[row[np.array(labels) == block].sum() for block in blocks] for row in matrix])


def _refine_partition(matrix: np.ndarray, labels: Sequence[int]) -> tuple[list[int], list[list[int]]]:
    current = list(map(int, labels))
    history = [current.copy()]
    while True:
        aggregate = _aggregate_rows(matrix, current)
        signatures = [(current[i], tuple(np.round(aggregate[i], 12))) for i in range(len(current))]
        dictionary: dict[tuple[object, ...], int] = {}
        refined: list[int] = []
        for signature in signatures:
            if signature not in dictionary:
                dictionary[signature] = len(dictionary)
            refined.append(dictionary[signature])
        history.append(refined.copy())
        if refined == current:
            return refined, history
        current = refined


def _lumpability_defect(matrix: np.ndarray, labels: Sequence[int]) -> float:
    aggregate = _aggregate_rows(matrix, labels)
    defect = 0.0
    for block in set(labels):
        indices = [i for i, label in enumerate(labels) if label == block]
        for i, j in itertools.combinations(indices, 2):
            defect = max(defect, float(np.max(np.abs(aggregate[i] - aggregate[j]))))
    return defect


def h8_completeness_detector_probe() -> dict[str, object]:
    transition = np.array([
        [0.9, 0.0, 0.1, 0.0],
        [0.0, 0.9, 0.0, 0.1],
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ])
    initial = [0, 0, 1, 1]
    final, history = _refine_partition(transition, initial)
    return {
        "hypothesis": "H8 hostile boundaries are retained-state completeness detectors",
        "transition_kernel": transition.tolist(),
        "initial_regular_defect_partition": initial,
        "refinement_history": history,
        "stable_partition": final,
        "initial_lumpability_defect": _lumpability_defect(transition, initial),
        "final_lumpability_defect": _lumpability_defect(transition, final),
        "status": "supported by a terminating finite-state refinement algorithm",
        "claim_level": "C1 finite Markov-kernel certificate",
    }


def h9_os_density_probe() -> dict[str, object]:
    energies = np.array([0.0, 0.4, 1.2])
    times = np.array([0.0, 0.5, 1.0, 2.0])
    # Positive-time Gram matrix for two nonvacuum spectral atoms.
    gram = sum(np.outer(np.exp(-energy * times), np.exp(-energy * times)) for energy in energies[1:])
    return {
        "hypothesis": "H9 mass gap can be separated from confinement but not from observable completeness",
        "hamiltonian_spectrum": energies.tolist(),
        "true_nonvacuum_gap": float(energies[1]),
        "rate_seen_by_complete_nonvacuum_core": float(min(energies[1:])),
        "apparent_rate_seen_by_incomplete_high_mode_core": float(energies[2]),
        "positive_time_gram_minimum_eigenvalue": float(np.linalg.eigvalsh(gram)[0]),
        "wilson_area_law_used": False,
        "status": "conditional spectral mechanism verified; density remains indispensable",
        "claim_level": "C1 finite-dimensional OS-semigroup model",
    }


def h10_recovery_probe() -> dict[str, object]:
    lift = np.array([
        [1.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
        [0.0, 1.0],
    ])
    coarse = 0.5 * lift.T
    recovery_projection = lift @ coarse
    invariant_error = np.linalg.norm(coarse @ lift - np.eye(2), ord=2)
    gauge_variant = np.array([1.0, -1.0, 0.0, 0.0])
    full_error = np.linalg.norm(gauge_variant - recovery_projection @ gauge_variant) / np.linalg.norm(gauge_variant)
    return {
        "hypothesis": "H10 renormalization has an observable-selective recovery structure",
        "coarse_map": coarse.tolist(),
        "observable_lift": lift.tolist(),
        "recovery_projection": recovery_projection.tolist(),
        "invariant_observable_recovery_error": float(invariant_error),
        "gauge_variant_recovery_error": float(full_error),
        "lesson": "irreversibility can coexist with exact recovery on a typed physical subalgebra",
        "status": "supported only in a finite gauge-copy toy model",
        "claim_level": "C1 finite linear-algebra model",
    }


def _partial_trace_last(rho: np.ndarray, kept_dimension: int, traced_dimension: int) -> np.ndarray:
    reshaped = rho.reshape(kept_dimension, traced_dimension, kept_dimension, traced_dimension)
    return np.einsum("iaja->ij", reshaped)


def substrate_operator_system_probe() -> dict[str, object]:
    """Exact region-scale coherence for matrix algebras and partial traces."""
    rho_a = np.array([[0.7, 0.1], [0.1, 0.3]])
    rho_b = np.array([[0.6, 0.0], [0.0, 0.4]])
    rho_c = np.array([[0.8, 0.0], [0.0, 0.2]])
    rho_abc = np.kron(np.kron(rho_a, rho_b), rho_c)
    rho_ab = _partial_trace_last(rho_abc, 4, 2)
    rho_a_two_step = _partial_trace_last(rho_ab, 2, 2)
    # Directly trace the joint BC factor.
    rho_a_direct = _partial_trace_last(rho_abc, 2, 4)

    observable_a = np.array([[1.0, 0.2], [0.2, -0.5]])
    lifted_abc = np.kron(np.kron(observable_a, np.eye(2)), np.eye(2))
    fine_expectation = float(np.trace(rho_abc @ lifted_abc).real)
    coarse_expectation = float(np.trace(rho_a_direct @ observable_a).real)
    return {
        "substrate": "finite region-scale graph of matrix operator systems and completely positive maps",
        "fine_algebra": "M_2 tensor M_2 tensor M_2",
        "intermediate_algebra": "M_2 tensor M_2",
        "coarse_algebra": "M_2",
        "state_trace": float(np.trace(rho_abc).real),
        "minimum_fine_state_eigenvalue": float(np.linalg.eigvalsh(rho_abc)[0]),
        "two_step_direct_state_coherence_error": float(np.linalg.norm(rho_a_two_step - rho_a_direct)),
        "observable_state_pairing_error": abs(fine_expectation - coarse_expectation),
        "observable_embedding_is_unital": bool(np.allclose(lifted_abc, np.kron(np.kron(observable_a, np.eye(2)), np.eye(2)))),
        "interpretation": "regional inclusions are star-homomorphisms; state reduction is CPTP; observable pullback is UCP",
        "claim_level": "C1 exact finite operator-system realization",
    }


def run_all() -> dict[str, object]:
    return {
        "schema_version": 1,
        "date": "2026-07-21",
        "scope": {
            "purpose": "first formal and executable probes of ten conceptual hypotheses",
            "strongest_claim_ceiling": "C2 restricted integral-flux and single-star results; otherwise C1",
            "physical_one_scale_basin_entry": False,
            "repeated_rg": False,
            "continuum_yang_mills": False,
            "hamiltonian_mass_gap": False,
        },
        "H1": h1_vacuum_weight_probe(),
        "H2": h2_lyapunov_gap_probe(),
        "H3": h3_polymer_spill_probe(),
        "H4": h4_graded_cocycle_probe(),
        "H5": h5_free_energy_probe(),
        "H6": h6_representation_curvature_probe(),
        "H7": h7_atlas_locality_probe(),
        "H8": h8_completeness_detector_probe(),
        "H9": h9_os_density_probe(),
        "H10": h10_recovery_probe(),
        "minimal_substrate": substrate_operator_system_probe(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    results = run_all()
    if args.write:
        RESULTS.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
