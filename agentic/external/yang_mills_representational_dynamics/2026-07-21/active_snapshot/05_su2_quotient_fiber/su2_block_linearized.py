"""Linearized SU(2) quotient-fiber analysis on a 2^4 cubical block.

The scalar cubical cochain complex is tensored with su(2), so every scalar
mode occurs with color multiplicity three.  Gauge directions are im(d0).
The physical tangent space is ker(d0^T), and retained coarse data are the
24 oriented fluxes through the 2x2 boundary faces of the coarse hypercube.

The module computes the finite-dimensional Gaussian core of a proposed
heat-kernel block RG step.  It does not implement the nonlinear SU(2) measure
or a full four-dimensional RG trajectory.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
from fractions import Fraction
import itertools
import json
import math
from typing import Iterable

import numpy as np
from scipy.linalg import null_space


@dataclass(frozen=True)
class CubicalBlock:
    dimension: int
    side_subdivisions: int
    vertices: tuple[tuple[int, ...], ...]
    edges: tuple[tuple[tuple[int, ...], int], ...]
    plaquettes: tuple[tuple[tuple[int, ...], int, int], ...]
    d0: np.ndarray
    d1: np.ndarray
    coarse_face_sum: np.ndarray
    coarse_flux: np.ndarray


@dataclass(frozen=True)
class BlockAnalysis:
    dimension: int
    side_subdivisions: int
    scalar_vertices: int
    scalar_edges: int
    scalar_plaquettes: int
    scalar_gauge_rank: int
    scalar_curvature_rank: int
    scalar_physical_dimension: int
    displayed_coarse_fluxes: int
    independent_coarse_fluxes: int
    scalar_fiber_dimension: int
    su2_gauge_dimension: int
    su2_physical_dimension: int
    su2_base_dimension: int
    su2_fiber_dimension: int
    complex_residual_norm: float
    gauge_orthogonality_residual: float
    physical_min_eigenvalue: float
    physical_max_eigenvalue: float
    certified_physical_lower_bound: float
    fiber_min_eigenvalue: float
    fiber_max_eigenvalue: float
    coarse_map_min_nonzero_singular_value: float
    full_coordinate_response_norm: float
    centered_fiber_response_norm: float


@dataclass(frozen=True)
class GaussianConditional:
    mean: np.ndarray
    covariance: np.ndarray
    centered_covariance: np.ndarray


def _shift(x: tuple[int, ...], direction: int, amount: int = 1) -> tuple[int, ...]:
    result = list(x)
    result[direction] += amount
    return tuple(result)


def build_cubical_block(dimension: int = 4, side_subdivisions: int = 2) -> CubicalBlock:
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    if side_subdivisions < 1:
        raise ValueError("side_subdivisions must be positive")

    n = side_subdivisions
    vertices = tuple(itertools.product(range(n + 1), repeat=dimension))
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}

    edges_list: list[tuple[tuple[int, ...], int]] = []
    for x in vertices:
        for mu in range(dimension):
            if x[mu] < n:
                edges_list.append((x, mu))
    edges = tuple(edges_list)
    edge_index = {edge: index for index, edge in enumerate(edges)}

    plaquette_list: list[tuple[tuple[int, ...], int, int]] = []
    for x in vertices:
        for mu in range(dimension):
            for nu in range(mu + 1, dimension):
                if x[mu] < n and x[nu] < n:
                    plaquette_list.append((x, mu, nu))
    plaquettes = tuple(plaquette_list)
    plaquette_index = {
        plaquette: index for index, plaquette in enumerate(plaquettes)
    }

    d0 = np.zeros((len(edges), len(vertices)), dtype=float)
    for row, (x, mu) in enumerate(edges):
        d0[row, vertex_index[x]] = -1.0
        d0[row, vertex_index[_shift(x, mu)]] = 1.0

    d1 = np.zeros((len(plaquettes), len(edges)), dtype=float)
    for row, (x, mu, nu) in enumerate(plaquettes):
        d1[row, edge_index[(x, mu)]] = 1.0
        d1[row, edge_index[(_shift(x, mu), nu)]] = 1.0
        d1[row, edge_index[(_shift(x, nu), mu)]] = -1.0
        d1[row, edge_index[(x, nu)]] = -1.0

    # Each row sums the fine plaquette curvatures over one 2-dimensional
    # boundary face of the coarse hypercube.  There are C(d,2) 2^(d-2) rows.
    face_rows = []
    for mu in range(dimension):
        for nu in range(mu + 1, dimension):
            transverse = [axis for axis in range(dimension) if axis not in (mu, nu)]
            for fixed_values in itertools.product((0, n), repeat=dimension - 2):
                base = [0] * dimension
                for axis, value in zip(transverse, fixed_values):
                    base[axis] = value
                row = np.zeros(len(plaquettes), dtype=float)
                for i in range(n):
                    for j in range(n):
                        x = base.copy()
                        x[mu] = i
                        x[nu] = j
                        row[plaquette_index[(tuple(x), mu, nu)]] = 1.0
                face_rows.append(row)
    coarse_face_sum = np.stack(face_rows)
    coarse_flux = coarse_face_sum @ d1

    return CubicalBlock(
        dimension=dimension,
        side_subdivisions=n,
        vertices=vertices,
        edges=edges,
        plaquettes=plaquettes,
        d0=d0,
        d1=d1,
        coarse_face_sum=coarse_face_sum,
        coarse_flux=coarse_flux,
    )


def numerical_rank(matrix: np.ndarray, tolerance: float = 1e-10) -> int:
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    return int(np.count_nonzero(singular_values > tolerance))


def exact_rational_rank(matrix: np.ndarray) -> int:
    """Exact Gaussian-elimination rank for a small integer/rational matrix."""
    if matrix.ndim != 2:
        raise ValueError("matrix must be two-dimensional")
    rows = [[Fraction(value) for value in row] for row in matrix.tolist()]
    row_count, column_count = matrix.shape
    rank = 0
    for column in range(column_count):
        pivot_row = next(
            (row for row in range(rank, row_count) if rows[row][column] != 0),
            None,
        )
        if pivot_row is None:
            continue
        rows[rank], rows[pivot_row] = rows[pivot_row], rows[rank]
        pivot = rows[rank][column]
        rows[rank] = [value / pivot for value in rows[rank]]
        for row in range(row_count):
            if row == rank or rows[row][column] == 0:
                continue
            factor = rows[row][column]
            rows[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(rows[row], rows[rank])
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def scalar_decomposition(
    block: CubicalBlock, tolerance: float = 1e-10
) -> dict[str, np.ndarray | int]:
    physical_basis = null_space(block.d0.T, rcond=tolerance)
    if physical_basis.shape[1] == 0:
        raise ValueError("physical quotient is empty")

    curvature_hessian = block.d1.T @ block.d1
    physical_hessian = physical_basis.T @ curvature_hessian @ physical_basis
    coarse_on_physical = block.coarse_flux @ physical_basis

    u, singular_values, _ = np.linalg.svd(coarse_on_physical, full_matrices=False)
    base_rank = int(np.count_nonzero(singular_values > tolerance))
    if base_rank == 0:
        raise ValueError("retained coarse map has zero rank")
    independent_base_map = u[:, :base_rank].T @ coarse_on_physical
    fiber_basis_in_physical = null_space(independent_base_map, rcond=tolerance)
    fiber_hessian = fiber_basis_in_physical.T @ physical_hessian @ fiber_basis_in_physical

    inverse_physical_hessian = np.linalg.inv(physical_hessian)
    base_gram = (
        independent_base_map
        @ inverse_physical_hessian
        @ independent_base_map.T
    )
    conditional_mean_map = (
        inverse_physical_hessian
        @ independent_base_map.T
        @ np.linalg.inv(base_gram)
    )
    conditional_covariance_unit_time = inverse_physical_hessian - (
        inverse_physical_hessian
        @ independent_base_map.T
        @ np.linalg.inv(base_gram)
        @ independent_base_map
        @ inverse_physical_hessian
    )

    return {
        "physical_basis": physical_basis,
        "physical_hessian": physical_hessian,
        "coarse_on_physical": coarse_on_physical,
        "independent_base_map": independent_base_map,
        "fiber_basis_in_physical": fiber_basis_in_physical,
        "fiber_hessian": fiber_hessian,
        "conditional_mean_map": conditional_mean_map,
        "conditional_covariance_unit_time": conditional_covariance_unit_time,
        "base_rank": base_rank,
        "coarse_singular_values": singular_values[:base_rank],
    }


def certified_physical_lower_bound(dimension: int, side_subdivisions: int) -> float:
    """Analytic lower bound used by the theorem dossier.

    For the four-dimensional product of length-two interval complexes, the
    product Hodge-spectrum calculation gives ||d1 A||^2 >= 2 ||A||^2 on
    ker(d0^T).  Other blocks are deliberately rejected rather than assigned an
    unsupported certificate.
    """
    if dimension != 4 or side_subdivisions != 2:
        raise ValueError("the analytic certificate is frozen to the 2^4 block")
    return 2.0


def analyze_block(
    dimension: int = 4, side_subdivisions: int = 2, tolerance: float = 1e-10
) -> BlockAnalysis:
    block = build_cubical_block(dimension, side_subdivisions)
    decomposition = scalar_decomposition(block, tolerance)
    physical_basis = decomposition["physical_basis"]
    physical_hessian = decomposition["physical_hessian"]
    fiber_basis = decomposition["fiber_basis_in_physical"]
    fiber_hessian = decomposition["fiber_hessian"]
    coarse_singular_values = decomposition["coarse_singular_values"]
    conditional_mean_map = decomposition["conditional_mean_map"]

    physical_eigenvalues = np.linalg.eigvalsh(physical_hessian)
    fiber_eigenvalues = np.linalg.eigvalsh(fiber_hessian)
    gauge_rank = numerical_rank(block.d0, tolerance)
    curvature_rank = numerical_rank(block.d1, tolerance)
    base_rank = int(decomposition["base_rank"])
    physical_dimension = physical_basis.shape[1]
    fiber_dimension = fiber_basis.shape[1]

    return BlockAnalysis(
        dimension=dimension,
        side_subdivisions=side_subdivisions,
        scalar_vertices=len(block.vertices),
        scalar_edges=len(block.edges),
        scalar_plaquettes=len(block.plaquettes),
        scalar_gauge_rank=gauge_rank,
        scalar_curvature_rank=curvature_rank,
        scalar_physical_dimension=physical_dimension,
        displayed_coarse_fluxes=block.coarse_flux.shape[0],
        independent_coarse_fluxes=base_rank,
        scalar_fiber_dimension=fiber_dimension,
        su2_gauge_dimension=3 * gauge_rank,
        su2_physical_dimension=3 * physical_dimension,
        su2_base_dimension=3 * base_rank,
        su2_fiber_dimension=3 * fiber_dimension,
        complex_residual_norm=float(np.linalg.norm(block.d1 @ block.d0, ord=2)),
        gauge_orthogonality_residual=float(
            np.linalg.norm(block.d0.T @ physical_basis, ord=2)
        ),
        physical_min_eigenvalue=float(physical_eigenvalues[0]),
        physical_max_eigenvalue=float(physical_eigenvalues[-1]),
        certified_physical_lower_bound=certified_physical_lower_bound(
            dimension, side_subdivisions
        ),
        fiber_min_eigenvalue=float(fiber_eigenvalues[0]),
        fiber_max_eigenvalue=float(fiber_eigenvalues[-1]),
        coarse_map_min_nonzero_singular_value=float(coarse_singular_values[-1]),
        full_coordinate_response_norm=float(
            np.linalg.svd(conditional_mean_map, compute_uv=False)[0]
        ),
        centered_fiber_response_norm=0.0,
    )


def gaussian_conditional(
    base_value: Iterable[float], heat_time: float, tolerance: float = 1e-10
) -> GaussianConditional:
    if heat_time <= 0.0:
        raise ValueError("heat_time must be positive")
    block = build_cubical_block()
    decomposition = scalar_decomposition(block, tolerance)
    base = np.asarray(tuple(base_value), dtype=float)
    base_rank = int(decomposition["base_rank"])
    if base.shape != (base_rank,):
        raise ValueError(f"base_value must have shape ({base_rank},)")
    mean = decomposition["conditional_mean_map"] @ base
    centered_covariance = (
        heat_time * decomposition["conditional_covariance_unit_time"]
    )
    return GaussianConditional(
        mean=mean,
        covariance=centered_covariance,
        centered_covariance=centered_covariance.copy(),
    )


def nonlinear_fiber_margin(scaled_hessian_remainder: float) -> float:
    """Certified strong-convexity numerator 2-eta on the frozen block."""
    if scaled_hessian_remainder < 0.0:
        raise ValueError("scaled_hessian_remainder must be nonnegative")
    margin = certified_physical_lower_bound(4, 2) - scaled_hessian_remainder
    if margin <= 0.0:
        raise ValueError("remainder exhausts the certified coercivity margin")
    return margin


def centered_transport_coefficient(
    scaled_hessian_remainder: float, scaled_centered_cross_gradient: float
) -> float:
    """L/alpha bound when alpha=(2-eta)/t and L=chi/t."""
    if scaled_centered_cross_gradient < 0.0:
        raise ValueError("cross-gradient bound must be nonnegative")
    return scaled_centered_cross_gradient / nonlinear_fiber_margin(
        scaled_hessian_remainder
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("table", "json"), default="table")
    args = parser.parse_args()
    analysis = analyze_block()
    payload = {
        "analysis": asdict(analysis),
        "nonlinear_certificate_examples": [
            {
                "scaled_hessian_remainder": eta,
                "scaled_centered_cross_gradient": chi,
                "fiber_margin": nonlinear_fiber_margin(eta),
                "transport_coefficient_upper": centered_transport_coefficient(
                    eta, chi
                ),
            }
            for eta, chi in ((0.25, 0.20), (0.50, 0.50), (1.00, 0.75))
        ],
        "scope": (
            "exact scalar cubical complex tensored with su(2), Gaussian tangent "
            "conditional law, and abstract nonlinear derivative certificate; "
            "not a nonlinear full-measure SU(2) RG theorem"
        ),
    }
    if args.output == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    for key, value in asdict(analysis).items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
