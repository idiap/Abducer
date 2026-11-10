"""Exact center-sector charging of the Stage 10 frustrated conditioning.

Center-valued SU(2) links are bits x on edges and negative plaquettes are the
exact two-cochain y=d1 x over GF(2).  The cubical Bianchi identity is d2 y=0.
On the open side-two four-cube the complex is exact at plaquettes.

The Stage 10 incident pattern (one negative staple and five positive staples)
cannot be realized by an isolated plaquette.  An exact syndrome search proves
that it forces at least five negative plaquettes in the full center field, and
the original one-negative-link certificate attains five.

This yields a genuine charged-contour estimate in the center subsector.  It is
not a bound for continuous nonabelian SU(2) fluctuations.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import itertools
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np


PACKAGE = Path(__file__).resolve().parents[1]
for sibling in (
    PACKAGE / "08_su2_nonlinear_block_geometry",
    PACKAGE / "10_frustrated_conditioning_obstruction",
):
    if str(sibling) not in sys.path:
        sys.path.insert(0, str(sibling))

from su2_nonlinear_block_geometry import build_block_complex  # noqa: E402
from frustrated_conditioning import staple_realization_certificate  # noqa: E402


@dataclass(frozen=True)
class CenterComplexCertificate:
    links: int
    plaquettes: int
    three_cells: int
    rank_d1_gf2: int
    rank_d2_gf2: int
    plaquette_exactness_dimension_sum: int
    bianchi_composition_zero: bool
    exact_at_plaquettes: bool
    link_adjacency_max_degree: int
    bianchi_adjacency_max_degree: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FrustrationChargeCertificate:
    selected_link_index: int
    target_plaquette_index: int
    forbidden_incident_plaquettes: tuple[int, ...]
    candidate_negative_links: tuple[int, ...]
    candidate_negative_plaquettes: tuple[int, ...]
    candidate_weight: int
    no_solution_weight_at_most_four: bool
    exact_minimum_weight: int
    global_nonempty_center_cocycle_minimum: int
    target_pattern_charged: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CenterContourCertificate:
    relative_negative_plaquette_weight: float
    alpha: float
    adjacency_degree: int
    smallest_nonempty_contour: int
    target_frustration_minimum_size: int
    convergence_threshold: float
    branching_ratio: float
    rooted_weighted_contour_sum_upper: float
    least_suppressed_target_factor: float
    heat_time: float
    asymptotic_log_weight_proxy: float
    center_sector_convergent: bool
    continuous_su2_measure_certified: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _shift(x: tuple[int, ...], direction: int) -> tuple[int, ...]:
    y = list(x)
    y[direction] += 1
    return tuple(y)


def build_d2_gf2() -> tuple[tuple[tuple[tuple[int, ...], int, int, int], ...], np.ndarray]:
    """Return three-cells and the plaquette-to-three-cell coboundary mod two."""

    block = build_block_complex()
    plaquette_index = {p: i for i, p in enumerate(block.plaquettes)}
    cells = tuple(
        (x, a, b, c)
        for x in block.vertices
        for a, b, c in itertools.combinations(range(4), 3)
        if x[a] < 2 and x[b] < 2 and x[c] < 2
    )
    d2 = np.zeros((len(cells), len(block.plaquettes)), dtype=np.uint8)
    for row, (x, a, b, c) in enumerate(cells):
        directions = (a, b, c)
        for normal in directions:
            face_directions = tuple(d for d in directions if d != normal)
            low = (x, face_directions[0], face_directions[1])
            high_x = _shift(x, normal)
            high = (high_x, face_directions[0], face_directions[1])
            d2[row, plaquette_index[low]] = 1
            d2[row, plaquette_index[high]] = 1
    return cells, d2


def gf2_rank(matrix: np.ndarray) -> int:
    a = np.asarray(matrix, dtype=np.uint8).copy() % 2
    row = 0
    for col in range(a.shape[1]):
        pivots = np.flatnonzero(a[row:, col])
        if len(pivots) == 0:
            continue
        pivot = row + int(pivots[0])
        a[[row, pivot]] = a[[pivot, row]]
        for other in range(a.shape[0]):
            if other != row and a[other, col]:
                a[other] ^= a[row]
        row += 1
        if row == a.shape[0]:
            break
    return row


def link_plaquette_adjacency() -> tuple[tuple[int, ...], ...]:
    block = build_block_complex()
    support = np.abs(block.d1).astype(bool)
    neighbors = [set() for _ in block.plaquettes]
    for link in range(len(block.edges)):
        incident = [int(x) for x in np.flatnonzero(support[:, link])]
        for p in incident:
            neighbors[p].update(q for q in incident if q != p)
    return tuple(tuple(sorted(x)) for x in neighbors)


def plaquette_adjacency() -> tuple[tuple[int, ...], ...]:
    """Bianchi adjacency: plaquettes are adjacent in a common three-cell.

    This is the correct component graph for center cocycles.  In particular,
    opposite faces of one three-cell are adjacent even though they share no
    link, so the parity constraint cannot split across components.
    """

    _, d2 = build_d2_gf2()
    neighbors = [set() for _ in range(d2.shape[1])]
    for row in range(d2.shape[0]):
        faces = [int(x) for x in np.flatnonzero(d2[row])]
        for p in faces:
            neighbors[p].update(q for q in faces if q != p)
    return tuple(tuple(sorted(x)) for x in neighbors)


def center_complex_certificate() -> CenterComplexCertificate:
    block = build_block_complex()
    _, d2 = build_d2_gf2()
    d1 = np.abs(block.d1).astype(np.uint8) % 2
    rank1 = gf2_rank(d1)
    rank2 = gf2_rank(d2)
    composition = (d2 @ d1) % 2
    link_adjacency = link_plaquette_adjacency()
    bianchi_adjacency = plaquette_adjacency()
    return CenterComplexCertificate(
        links=len(block.edges),
        plaquettes=len(block.plaquettes),
        three_cells=d2.shape[0],
        rank_d1_gf2=rank1,
        rank_d2_gf2=rank2,
        plaquette_exactness_dimension_sum=rank1 + rank2,
        bianchi_composition_zero=not composition.any(),
        exact_at_plaquettes=rank1 + rank2 == len(block.plaquettes),
        link_adjacency_max_degree=max(len(x) for x in link_adjacency),
        bianchi_adjacency_max_degree=max(len(x) for x in bianchi_adjacency),
    )


def _column_masks(matrix: np.ndarray) -> tuple[int, ...]:
    masks: list[int] = []
    for col in range(matrix.shape[1]):
        value = 0
        for row in np.flatnonzero(matrix[:, col]):
            value |= 1 << int(row)
        masks.append(value)
    return tuple(masks)


def _has_extra_subset_at_most_three(
    masks: tuple[int, ...], target: int, allowed: tuple[int, ...]
) -> bool:
    """Exact meet-in-the-middle search for 0--3 distinct extra plaquettes."""

    if target == 0:
        return True
    singles: dict[int, list[int]] = {}
    for i in allowed:
        singles.setdefault(masks[i], []).append(i)
    if target in singles:
        return True
    pairs: dict[int, list[tuple[int, int]]] = {}
    for pos, i in enumerate(allowed):
        for j in allowed[pos + 1 :]:
            pairs.setdefault(masks[i] ^ masks[j], []).append((i, j))
    if target in pairs:
        return True
    for k in allowed:
        needed = target ^ masks[k]
        for i, j in pairs.get(needed, ()):
            if k != i and k != j:
                return True
    return False


def _global_nonempty_minimum(d2: np.ndarray, d1: np.ndarray) -> int:
    masks = _column_masks(d2)
    if any(mask == 0 for mask in masks):
        return 1
    if len(set(masks)) != len(masks):
        return 2
    link_degrees = np.sum(d1, axis=0).astype(int)
    candidate_link = int(np.flatnonzero(link_degrees == np.min(link_degrees))[0])
    candidate = d1[:, candidate_link]
    if int(candidate.sum()) != 3 or ((d2 @ candidate) % 2).any():
        raise RuntimeError("the expected three-plaquette corner cocycle failed")
    return 3


def frustration_charge_certificate() -> FrustrationChargeCertificate:
    block = build_block_complex()
    _, d2 = build_d2_gf2()
    d1 = np.abs(block.d1).astype(np.uint8) % 2
    realization = staple_realization_certificate(0)
    x = np.zeros(len(block.edges), dtype=np.uint8)
    x[list(realization.negative_center_link_indices)] = 1
    y = (d1 @ x) % 2
    incident = realization.incident_plaquette_indices
    target = incident[0]
    forbidden = tuple(incident[1:])
    if y[target] != 1 or any(y[p] for p in forbidden):
        raise RuntimeError("Stage 10 assignment does not match its incident pattern")
    if ((d2 @ y) % 2).any():
        raise RuntimeError("candidate violates the cubical Bianchi identity")
    masks = _column_masks(d2)
    allowed = tuple(
        p for p in range(len(block.plaquettes)) if p not in set(incident)
    )
    small_exists = _has_extra_subset_at_most_three(masks, masks[target], allowed)
    candidate_negative = tuple(int(p) for p in np.flatnonzero(y))
    candidate_weight = int(y.sum())
    if candidate_weight != 5:
        raise RuntimeError("the matching center certificate must have weight five")
    global_min = _global_nonempty_minimum(d2, d1)
    return FrustrationChargeCertificate(
        selected_link_index=realization.selected_link_index,
        target_plaquette_index=target,
        forbidden_incident_plaquettes=forbidden,
        candidate_negative_links=realization.negative_center_link_indices,
        candidate_negative_plaquettes=candidate_negative,
        candidate_weight=candidate_weight,
        no_solution_weight_at_most_four=not small_exists,
        exact_minimum_weight=5 if not small_exists else -1,
        global_nonempty_center_cocycle_minimum=global_min,
        target_pattern_charged=not small_exists and candidate_weight == 5,
    )


def center_contour_certificate(
    relative_negative_plaquette_weight: float = 1.0e-4,
    alpha: float = 0.1,
    heat_time: float = 3.0e-6,
) -> CenterContourCertificate:
    q = float(relative_negative_plaquette_weight)
    alpha = float(alpha)
    t = float(heat_time)
    if not math.isfinite(q) or not 0.0 < q < 1.0:
        raise ValueError("relative weight must lie in (0,1)")
    if not math.isfinite(alpha) or alpha < 0.0:
        raise ValueError("alpha must be finite and nonnegative")
    if not math.isfinite(t) or t <= 0.0:
        raise ValueError("heat_time must be finite and positive")
    complex_cert = center_complex_certificate()
    charge = frustration_charge_certificate()
    degree = complex_cert.bianchi_adjacency_max_degree
    ratio = math.exp(alpha) * degree * degree * q
    threshold = math.exp(-alpha) / (degree * degree)
    if ratio < 1.0:
        rooted = (
            math.exp(3.0 * alpha)
            * q**3
            * degree**4
            / (1.0 - ratio)
        )
    else:
        rooted = math.inf
    return CenterContourCertificate(
        relative_negative_plaquette_weight=q,
        alpha=alpha,
        adjacency_degree=degree,
        smallest_nonempty_contour=charge.global_nonempty_center_cocycle_minimum,
        target_frustration_minimum_size=charge.exact_minimum_weight,
        convergence_threshold=threshold,
        branching_ratio=ratio,
        rooted_weighted_contour_sum_upper=rooted,
        least_suppressed_target_factor=q ** charge.exact_minimum_weight,
        heat_time=t,
        asymptotic_log_weight_proxy=-(math.pi**2) / (2.0 * t),
        center_sector_convergent=ratio < 1.0,
        continuous_su2_measure_certified=False,
    )


def calibration() -> dict[str, Any]:
    return {
        "complex": center_complex_certificate().to_dict(),
        "frustration_charge": frustration_charge_certificate().to_dict(),
        "center_contour": center_contour_certificate().to_dict(),
        "claim_level": "C2 exact center-sector contour theorem",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=("json",), default="json")
    parser.parse_args()
    print(json.dumps(calibration(), indent=2))


if __name__ == "__main__":
    main()
