"""Explicit nonlinear geometry on the 2^4 SU(2) lattice block.

This module closes a finite-dimensional bridge between the one-plaquette
heat-kernel estimates of Stage 07 and the abstract one-step norm of Stage 06.
It uses the unit-quaternion model of SU(2), a Banach-algebra logarithm bound,
the exact 2^4 incidence complex, and a local Coulomb gauge contraction.

The certificate is deliberately local.  It does not control the complement
of the logarithmic chart, dependent bad blocks, a multiscale RG trajectory,
the continuum limit, or a Hamiltonian mass gap.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import itertools
import json
import math
from pathlib import Path
import platform
import sys
from typing import Any, Iterable

import numpy as np


STAGE07 = Path(__file__).resolve().parents[1] / "07_su2_heat_kernel_initializer"
if str(STAGE07) not in sys.path:
    sys.path.insert(0, str(STAGE07))

from su2_heat_kernel_initializer import (  # noqa: E402
    character_tail_probability,
    heat_kernel_local_certificate,
)


SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SQRT6 = math.sqrt(6.0)
SQRT12 = math.sqrt(12.0)


def _finite_nonnegative(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


def _finite_positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


@dataclass(frozen=True)
class BlockComplex:
    vertices: tuple[tuple[int, ...], ...]
    edges: tuple[tuple[tuple[int, ...], int], ...]
    plaquettes: tuple[tuple[tuple[int, ...], int, int], ...]
    d0: np.ndarray
    d1: np.ndarray
    coarse_flux: np.ndarray


@dataclass(frozen=True)
class IncidenceCertificate:
    vertices: int
    links: int
    plaquettes: int
    max_vertex_degree: int
    max_link_plaquette_degree: int
    plaquette_boundary_links: int
    gauge_rank: int
    curvature_rank: int
    physical_dimension_scalar: int
    displayed_coarse_fluxes: int
    independent_coarse_fluxes: int
    fiber_dimension_scalar: int
    d0_operator_norm: float
    d1_operator_norm: float
    physical_min_singular_value: float
    certified_d0_operator_norm: float
    certified_d1_operator_norm: float
    certified_physical_min_singular_value: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProductLogBounds:
    factor_count: int
    input_radius: float
    algebra_distance_bound: float
    log_first_bound: float
    log_second_bound: float
    log_third_bound: float
    product_first_bound: float
    product_second_bound: float
    product_third_bound: float
    map_first_bound: float
    map_second_bound: float
    map_third_bound: float
    derivative_deviation_bound: float
    output_geodesic_bound: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlaquetteChartCertificate:
    local_link_radius: float
    curvature_radius: float
    linear_local_norm: float
    derivative_local_norm: float
    second_derivative_local_norm: float
    third_derivative_local_norm: float
    local_derivative_deviation: float
    global_derivative_deviation: float
    linear_global_norm: float
    nonlinear_global_derivative_bound: float
    physical_linear_min_singular_value: float
    nonlinear_physical_min_singular_value: float
    inverse_lipschitz_bound: float
    injective_on_coulomb_slice: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GaugeSliceCertificate:
    input_field_radius: float
    gauge_parameter_radius: float
    local_three_factor_radius: float
    algebra_distance_bound: float
    edge_second_derivative_bound: float
    contraction_coefficient: float
    ball_mapping_slack: float
    transformed_field_norm_bound: float
    action_chart_radius: float
    contraction_certified: bool
    action_chart_entry_certified: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ActionInitializationCertificate:
    time_max: float
    local_link_radius: float
    curvature_radius: float
    heat_scaled_gradient_bound: float
    heat_scaled_hessian_bound: float
    heat_scaled_third_bound: float
    global_hessian_remainder: float
    global_third_derivative_bound: float
    coordinate_base_embedding_bound: float
    eps_fiber: float
    eps_cross: float
    eps_base: float
    tau_fiber: float
    tau_cross: float
    lambda_fiber: float
    lambda_base: float
    fiber_radius: float
    fiber_margin: float
    minimizer_response_bound: float
    centered_cross_budget: float
    centered_transport_coefficient: float
    generated_good_hessian_budget: float
    generated_base_margin: float
    local_norm_initialized: bool
    fiber_contraction_certified: bool
    generated_base_coercive: bool
    full_measure_certified: bool
    polymer_certified: bool
    continuum_certified: bool
    mass_gap_certified: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _shift(x: tuple[int, ...], direction: int) -> tuple[int, ...]:
    y = list(x)
    y[direction] += 1
    return tuple(y)


def build_block_complex() -> BlockComplex:
    """Return the scalar cochain matrices of the side-two four-cube."""

    dimension = 4
    n = 2
    vertices = tuple(itertools.product(range(n + 1), repeat=dimension))
    vertex_index = {x: i for i, x in enumerate(vertices)}
    edges = tuple(
        (x, mu)
        for x in vertices
        for mu in range(dimension)
        if x[mu] < n
    )
    edge_index = {edge: i for i, edge in enumerate(edges)}
    plaquettes = tuple(
        (x, mu, nu)
        for x in vertices
        for mu in range(dimension)
        for nu in range(mu + 1, dimension)
        if x[mu] < n and x[nu] < n
    )
    plaquette_index = {p: i for i, p in enumerate(plaquettes)}

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

    face_rows: list[np.ndarray] = []
    for mu in range(dimension):
        for nu in range(mu + 1, dimension):
            transverse = [a for a in range(dimension) if a not in (mu, nu)]
            for fixed in itertools.product((0, n), repeat=dimension - 2):
                base = [0] * dimension
                for axis, value in zip(transverse, fixed):
                    base[axis] = value
                row = np.zeros(len(plaquettes), dtype=float)
                for i in range(n):
                    for j in range(n):
                        x = base.copy()
                        x[mu] = i
                        x[nu] = j
                        row[plaquette_index[(tuple(x), mu, nu)]] = 1.0
                face_rows.append(row)
    coarse_flux = np.stack(face_rows) @ d1
    return BlockComplex(vertices, edges, plaquettes, d0, d1, coarse_flux)


def incidence_certificate() -> IncidenceCertificate:
    block = build_block_complex()
    vertex_degrees = np.sum(np.abs(block.d0), axis=0)
    link_degrees = np.sum(np.abs(block.d1), axis=0)
    plaquette_sizes = np.sum(np.abs(block.d1), axis=1)
    gauge_rank = int(np.linalg.matrix_rank(block.d0, tol=1e-10))
    curvature_rank = int(np.linalg.matrix_rank(block.d1, tol=1e-10))
    coarse_rank = int(np.linalg.matrix_rank(block.coarse_flux, tol=1e-10))
    physical_dimension = len(block.edges) - gauge_rank
    return IncidenceCertificate(
        vertices=len(block.vertices),
        links=len(block.edges),
        plaquettes=len(block.plaquettes),
        max_vertex_degree=int(np.max(vertex_degrees)),
        max_link_plaquette_degree=int(np.max(link_degrees)),
        plaquette_boundary_links=int(np.max(plaquette_sizes)),
        gauge_rank=gauge_rank,
        curvature_rank=curvature_rank,
        physical_dimension_scalar=physical_dimension,
        displayed_coarse_fluxes=block.coarse_flux.shape[0],
        independent_coarse_fluxes=coarse_rank,
        fiber_dimension_scalar=physical_dimension - coarse_rank,
        d0_operator_norm=float(np.linalg.norm(block.d0, 2)),
        d1_operator_norm=float(np.linalg.norm(block.d1, 2)),
        physical_min_singular_value=SQRT2,
        certified_d0_operator_norm=SQRT12,
        certified_d1_operator_norm=SQRT12,
        certified_physical_min_singular_value=SQRT2,
    )


def quaternion_multiply(q: Iterable[float], r: Iterable[float]) -> np.ndarray:
    qv = np.asarray(tuple(q), dtype=float)
    rv = np.asarray(tuple(r), dtype=float)
    if qv.shape != (4,) or rv.shape != (4,):
        raise ValueError("quaternions must have four real components")
    q0, qx = qv[0], qv[1:]
    r0, rx = rv[0], rv[1:]
    return np.concatenate(
        ([q0 * r0 - float(np.dot(qx, rx))], q0 * rx + r0 * qx + np.cross(qx, rx))
    )


def quaternion_inverse(q: Iterable[float]) -> np.ndarray:
    qv = np.asarray(tuple(q), dtype=float)
    if qv.shape != (4,):
        raise ValueError("quaternion must have four real components")
    norm_sq = float(np.dot(qv, qv))
    if norm_sq == 0.0:
        raise ValueError("zero quaternion has no inverse")
    return np.concatenate(([qv[0]], -qv[1:])) / norm_sq


def su2_exp(a: Iterable[float]) -> np.ndarray:
    av = np.asarray(tuple(a), dtype=float)
    if av.shape != (3,) or not np.all(np.isfinite(av)):
        raise ValueError("Lie-algebra coordinate must be a finite three-vector")
    theta = float(np.linalg.norm(av))
    if theta < 1e-8:
        sinc = 1.0 - theta**2 / 6.0 + theta**4 / 120.0
    else:
        sinc = math.sin(theta) / theta
    return np.concatenate(([math.cos(theta)], sinc * av))


def su2_log(q: Iterable[float]) -> np.ndarray:
    qv = np.asarray(tuple(q), dtype=float)
    if qv.shape != (4,) or not np.all(np.isfinite(qv)):
        raise ValueError("group coordinate must be a finite quaternion")
    norm = float(np.linalg.norm(qv))
    if abs(norm - 1.0) > 1e-9:
        raise ValueError("SU(2) quaternion must have unit norm")
    qv = qv / norm
    vector_norm = float(np.linalg.norm(qv[1:]))
    if vector_norm < 1e-14:
        if qv[0] < 0.0:
            raise ValueError("the principal logarithm is undefined at the cut locus")
        return np.zeros(3)
    theta = math.atan2(vector_norm, float(qv[0]))
    if math.pi - theta < 1e-12:
        raise ValueError("the principal logarithm is too close to the cut locus")
    return theta * qv[1:] / vector_norm


def product_log_bounds(factor_count: int, input_radius: float) -> ProductLogBounds:
    """Banach-algebra derivative bounds for log(prod exp(a_i))."""

    if factor_count < 1:
        raise ValueError("factor_count must be positive")
    radius = _finite_positive("input_radius", input_radius)
    root_m = math.sqrt(float(factor_count))
    delta = root_m * radius
    if delta >= 1.0:
        raise ValueError("the Banach logarithm requires sqrt(m) * radius < 1")
    denominator = 1.0 - delta
    l1 = denominator**-1
    l2 = denominator**-2
    l3 = 2.0 * denominator**-3
    p1 = root_m
    p2 = float(factor_count)
    p3 = factor_count * root_m
    m1 = l1 * p1
    m2 = l2 * p1**2 + l1 * p2
    m3 = l3 * p1**3 + 3.0 * l2 * p1 * p2 + l1 * p3
    return ProductLogBounds(
        factor_count=factor_count,
        input_radius=radius,
        algebra_distance_bound=delta,
        log_first_bound=l1,
        log_second_bound=l2,
        log_third_bound=l3,
        product_first_bound=p1,
        product_second_bound=p2,
        product_third_bound=p3,
        map_first_bound=m1,
        map_second_bound=m2,
        map_third_bound=m3,
        derivative_deviation_bound=m2 * radius,
        output_geodesic_bound=root_m * radius,
    )


def plaquette_log(local_links: np.ndarray) -> np.ndarray:
    links = np.asarray(local_links, dtype=float)
    if links.shape != (4, 3) or not np.all(np.isfinite(links)):
        raise ValueError("local_links must be a finite 4 by 3 array")
    factors = (
        su2_exp(links[0]),
        su2_exp(links[1]),
        su2_exp(-links[2]),
        su2_exp(-links[3]),
    )
    product = np.array([1.0, 0.0, 0.0, 0.0])
    for factor in factors:
        product = quaternion_multiply(product, factor)
    return su2_log(product / np.linalg.norm(product))


def plaquette_chart_certificate(local_link_radius: float) -> PlaquetteChartCertificate:
    bounds = product_log_bounds(4, local_link_radius)
    local_deviation = bounds.derivative_deviation_bound
    global_deviation = SQRT6 * local_deviation
    nonlinear_min = SQRT2 - global_deviation
    if nonlinear_min <= 0.0:
        raise ValueError("nonlinear deviation exhausts quotient injectivity")
    return PlaquetteChartCertificate(
        local_link_radius=float(local_link_radius),
        curvature_radius=2.0 * float(local_link_radius),
        linear_local_norm=2.0,
        derivative_local_norm=bounds.map_first_bound,
        second_derivative_local_norm=bounds.map_second_bound,
        third_derivative_local_norm=bounds.map_third_bound,
        local_derivative_deviation=local_deviation,
        global_derivative_deviation=global_deviation,
        linear_global_norm=SQRT12,
        nonlinear_global_derivative_bound=SQRT12 + global_deviation,
        physical_linear_min_singular_value=SQRT2,
        nonlinear_physical_min_singular_value=nonlinear_min,
        inverse_lipschitz_bound=1.0 / nonlinear_min,
        injective_on_coulomb_slice=True,
    )


def gauge_slice_certificate(
    input_field_radius: float,
    gauge_parameter_radius: float,
    action_chart_radius: float,
) -> GaugeSliceCertificate:
    """Contraction certificate for the local logarithmic Coulomb slice.

    Gauge parameters are mean-zero vertex fields.  The derivative at the
    origin is minus the graph Laplacian, whose inverse norm on mean-zero
    fields is one.  Constant gauge rotations remain as residual conjugations.
    """

    field_radius = _finite_nonnegative("input_field_radius", input_field_radius)
    gauge_radius = _finite_positive("gauge_parameter_radius", gauge_parameter_radius)
    chart_radius = _finite_positive("action_chart_radius", action_chart_radius)
    local_radius = math.sqrt(field_radius**2 + 2.0 * gauge_radius**2)
    edge_bounds = product_log_bounds(3, local_radius)
    contraction = math.sqrt(8.0) * SQRT12 * edge_bounds.derivative_deviation_bound
    slack = (1.0 - contraction) * gauge_radius - field_radius
    transformed_bound = field_radius + 4.0 * gauge_radius
    contraction_ok = contraction < 1.0 and slack >= 0.0
    chart_ok = contraction_ok and transformed_bound <= chart_radius
    return GaugeSliceCertificate(
        input_field_radius=field_radius,
        gauge_parameter_radius=gauge_radius,
        local_three_factor_radius=local_radius,
        algebra_distance_bound=edge_bounds.algebra_distance_bound,
        edge_second_derivative_bound=edge_bounds.map_second_bound,
        contraction_coefficient=contraction,
        ball_mapping_slack=slack,
        transformed_field_norm_bound=transformed_bound,
        action_chart_radius=chart_radius,
        contraction_certified=contraction_ok,
        action_chart_entry_certified=chart_ok,
    )


def transform_link_field(
    link_field: np.ndarray, gauge_parameter: np.ndarray, block: BlockComplex | None = None
) -> np.ndarray:
    block = build_block_complex() if block is None else block
    field = np.asarray(link_field, dtype=float)
    phi = np.asarray(gauge_parameter, dtype=float)
    if field.shape != (len(block.edges), 3):
        raise ValueError("link_field has incompatible shape")
    if phi.shape != (len(block.vertices), 3):
        raise ValueError("gauge_parameter has incompatible shape")
    vertex_index = {x: i for i, x in enumerate(block.vertices)}
    transformed = np.empty_like(field)
    for edge_index, (x, mu) in enumerate(block.edges):
        source = vertex_index[x]
        target = vertex_index[_shift(x, mu)]
        q = quaternion_multiply(su2_exp(phi[source]), su2_exp(field[edge_index]))
        q = quaternion_multiply(q, su2_exp(-phi[target]))
        transformed[edge_index] = su2_log(q / np.linalg.norm(q))
    return transformed


def solve_local_coulomb_slice(
    link_field: np.ndarray,
    tolerance: float = 1e-13,
    max_iterations: int = 100,
) -> tuple[np.ndarray, np.ndarray, int, float]:
    """Numerically execute the certified fixed-point map for calibration."""

    block = build_block_complex()
    field = np.asarray(link_field, dtype=float)
    if field.shape != (len(block.edges), 3):
        raise ValueError("link_field has incompatible shape")
    laplacian_pseudoinverse = np.linalg.pinv(block.d0.T @ block.d0, rcond=1e-13)
    phi = np.zeros((len(block.vertices), 3), dtype=float)
    residual = math.inf
    for iteration in range(1, max_iterations + 1):
        transformed = transform_link_field(field, phi, block)
        divergence = block.d0.T @ transformed
        residual = float(np.linalg.norm(divergence))
        if residual <= tolerance:
            return phi, transformed, iteration, residual
        phi = phi + laplacian_pseudoinverse @ divergence
        phi = phi - np.mean(phi, axis=0, keepdims=True)
    raise RuntimeError(f"Coulomb iteration did not converge; residual={residual}")


def action_initialization_certificate(
    time_max: float = 0.01,
    local_link_radius: float = 0.003,
    fiber_radius: float = 0.001,
) -> ActionInitializationCertificate:
    """Initialize all five Stage-06 good-chart derivative components."""

    time_max = _finite_positive("time_max", time_max)
    fiber_radius = _finite_nonnegative("fiber_radius", fiber_radius)
    chart = plaquette_chart_certificate(local_link_radius)
    heat = heat_kernel_local_certificate(time_max, chart.curvature_radius)
    epsilon = heat.scaled_hessian_remainder_bound
    gradient = heat.scaled_gradient_remainder_bound
    tau_heat = heat.scaled_third_derivative_bound
    kappa = chart.global_derivative_deviation
    m1 = chart.derivative_local_norm
    m2 = chart.second_derivative_local_norm
    m3 = chart.third_derivative_local_norm
    rho = chart.curvature_radius

    eta = (
        kappa * (2.0 * SQRT12 + kappa)
        + epsilon * (SQRT12 + kappa) ** 2
        + 6.0 * (rho + gradient) * m2
    )
    per_plaquette_third = (
        tau_heat * m1**3
        + 3.0 * (1.0 + epsilon) * m1 * m2
        + (rho + gradient) * m3
    )
    tau = 6.0 * per_plaquette_third

    # H-whitened retained coordinates have reference Hessian I and embedding
    # norm at most 1/sqrt(2); the Euclidean fiber embedding has norm one and
    # reference Hessian at least 2.
    base_embedding = 1.0 / SQRT2
    eps_fiber = eta
    eps_cross = eta * base_embedding
    eps_base = eta * base_embedding**2
    tau_fiber = tau
    tau_cross = tau * base_embedding
    lambda_fiber = 2.0
    lambda_base = 1.0
    fiber_margin = lambda_fiber - eps_fiber
    if fiber_margin <= 0.0:
        raise ValueError("the chart does not preserve the fiber margin")
    minimizer_response = eps_cross / fiber_margin
    centered_cross = fiber_radius * (
        tau_cross + tau_fiber * minimizer_response
    )
    transport = centered_cross / fiber_margin
    generated_good = eps_base + eps_cross**2 / fiber_margin
    generated_base_margin = lambda_base - generated_good
    return ActionInitializationCertificate(
        time_max=time_max,
        local_link_radius=float(local_link_radius),
        curvature_radius=rho,
        heat_scaled_gradient_bound=gradient,
        heat_scaled_hessian_bound=epsilon,
        heat_scaled_third_bound=tau_heat,
        global_hessian_remainder=eta,
        global_third_derivative_bound=tau,
        coordinate_base_embedding_bound=base_embedding,
        eps_fiber=eps_fiber,
        eps_cross=eps_cross,
        eps_base=eps_base,
        tau_fiber=tau_fiber,
        tau_cross=tau_cross,
        lambda_fiber=lambda_fiber,
        lambda_base=lambda_base,
        fiber_radius=fiber_radius,
        fiber_margin=fiber_margin,
        minimizer_response_bound=minimizer_response,
        centered_cross_budget=centered_cross,
        centered_transport_coefficient=transport,
        generated_good_hessian_budget=generated_good,
        generated_base_margin=generated_base_margin,
        local_norm_initialized=True,
        fiber_contraction_certified=transport < 1.0,
        generated_base_coercive=generated_base_margin > 0.0,
        full_measure_certified=False,
        polymer_certified=False,
        continuum_certified=False,
        mass_gap_certified=False,
    )


def calibration() -> dict[str, Any]:
    incidence = incidence_certificate()
    plaquette = plaquette_chart_certificate(0.003)
    gauge = gauge_slice_certificate(0.0002, 0.0006, 0.003)
    action = action_initialization_certificate()
    probability = character_tail_probability(
        action.time_max, action.curvature_radius, highest_character=200
    )
    return {
        "scope": (
            "exact finite 2^4 quaternion/logarithm, incidence, local Coulomb-slice, "
            "and good-chart action-norm certificate; excludes the chart complement, "
            "dependent polymers, repeated RG, continuum construction, and mass gap"
        ),
        "incidence": incidence.to_dict(),
        "plaquette_chart": plaquette.to_dict(),
        "gauge_slice": gauge.to_dict(),
        "action_initialization": action.to_dict(),
        "small_chart_probability_obstruction": probability.to_dict(),
        "frontier_flags": {
            "full_measure": False,
            "dependent_polymer": False,
            "multiscale_iteration": False,
            "reflection_positivity_transfer": False,
            "continuum_yang_mills": False,
            "hamiltonian_mass_gap": False,
        },
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json", "table"), default="table")
    args = parser.parse_args()
    result = calibration()
    if args.output == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    action = result["action_initialization"]
    gauge = result["gauge_slice"]
    tail = result["small_chart_probability_obstruction"]
    print(f"global Hessian remainder: {action['global_hessian_remainder']:.9f}")
    print(f"fiber transport coefficient: {action['centered_transport_coefficient']:.9f}")
    print(f"generated base margin: {action['generated_base_margin']:.9f}")
    print(f"gauge contraction: {gauge['contraction_coefficient']:.9f}")
    print(f"P(theta >= rho) at t_max: [{tail['lower']:.12f}, {tail['upper']:.12f}]")


if __name__ == "__main__":
    main()
