"""Finite spectral certificates for the H9 temporal-density hypothesis.

The analytic theorem is elementary but structurally important.  For a finite
positive self-adjoint Hamiltonian ``H`` with vacuum ``omega``, centered probe
vectors span a space ``D``.  Their time translates generate the invariant
spectral closure

    K = direct_sum_lambda ran(P_lambda | D).

Decay of all norm-compatible bilinear forms on a dense ``K = omega^perp``
extends to the full vacuum-orthogonal operator norm.  If ``K`` is not dense,
the conclusion is restricted to ``K`` and slower invisible modes may remain.

The computations below are finite floating-point calibrations of that theorem;
they are not an OS reconstruction or a continuum Yang--Mills result.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np


ArrayLike = Sequence[Sequence[float]] | Sequence[float] | np.ndarray


def _real_array(value: ArrayLike, *, name: str) -> np.ndarray:
    array = np.asarray(value)
    if np.iscomplexobj(array):
        if np.max(np.abs(np.imag(array))) > 1.0e-12:
            raise ValueError(f"{name} must be real in this executable calibration")
        array = np.real(array)
    try:
        array = np.asarray(array, dtype=float)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be a finite real array") from exc
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def validate_hamiltonian(hamiltonian: ArrayLike, *, tol: float = 1.0e-10) -> np.ndarray:
    """Validate a nonempty real self-adjoint positive-semidefinite matrix."""

    matrix = _real_array(hamiltonian, name="hamiltonian")
    if matrix.ndim != 2 or matrix.shape[0] == 0 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("hamiltonian must be a nonempty square matrix")
    if not np.allclose(matrix, matrix.T, atol=tol, rtol=0.0):
        raise ValueError("hamiltonian must be self-adjoint")
    matrix = (matrix + matrix.T) / 2.0
    if float(np.min(np.linalg.eigvalsh(matrix))) < -tol:
        raise ValueError("hamiltonian must be positive semidefinite")
    return matrix


def validate_vacuum(
    hamiltonian: np.ndarray, omega: ArrayLike, *, tol: float = 1.0e-10
) -> np.ndarray:
    vector = _real_array(omega, name="vacuum").reshape(-1)
    if vector.shape != (hamiltonian.shape[0],):
        raise ValueError("vacuum dimension must match hamiltonian")
    norm = float(np.linalg.norm(vector))
    if abs(norm - 1.0) > tol:
        raise ValueError("vacuum must be normalized")
    if float(np.linalg.norm(hamiltonian @ vector)) > tol:
        raise ValueError("vacuum must be a zero-energy eigenvector")
    return vector


def centered_probes(probes: ArrayLike, omega: np.ndarray, *, tol: float = 1.0e-10) -> np.ndarray:
    """Return centered probe columns, rejecting an empty centered family."""

    matrix = _real_array(probes, name="probes")
    if matrix.ndim == 1:
        matrix = matrix.reshape(-1, 1)
    if matrix.ndim != 2 or matrix.shape[0] != omega.size or matrix.shape[1] == 0:
        raise ValueError("probes must be an n by k array with k >= 1")
    centered = matrix - np.outer(omega, omega @ matrix)
    if float(np.linalg.norm(centered)) <= tol:
        raise ValueError("at least one probe must have a nonzero centered component")
    return centered


def orthonormal_basis(columns: np.ndarray, *, tol: float = 1.0e-10) -> np.ndarray:
    if columns.ndim != 2:
        raise ValueError("basis input must be a matrix of columns")
    if columns.shape[1] == 0:
        return np.zeros((columns.shape[0], 0))
    u, singular, _ = np.linalg.svd(columns, full_matrices=False)
    scale = max(1.0, float(singular[0])) if singular.size else 1.0
    rank = int(np.count_nonzero(singular > tol * scale))
    return u[:, :rank]


def vacuum_complement(omega: np.ndarray) -> np.ndarray:
    """Orthonormal columns spanning omega-perp."""

    _, _, vh = np.linalg.svd(omega.reshape(1, -1), full_matrices=True)
    return vh[1:, :].T


def _eigen_groups(eigenvalues: np.ndarray, *, tol: float) -> list[tuple[np.ndarray, float]]:
    groups: list[list[int]] = []
    for index, value in enumerate(eigenvalues):
        if not groups or abs(value - eigenvalues[groups[-1][0]]) > tol:
            groups.append([index])
        else:
            groups[-1].append(index)
    return [(np.asarray(group, dtype=int), float(np.mean(eigenvalues[group]))) for group in groups]


@dataclass(frozen=True)
class SpectralCertificate:
    dimension: int
    vacuum_orthogonal_dimension: int
    eigenvalues_on_vacuum_orthogonal: tuple[float, ...]
    true_gap: float
    raw_centered_probe_rank: int
    generated_invariant_rank: int
    dense_in_vacuum_orthogonal: bool
    state_separating: bool
    visible_gap: float
    lowest_mode_visible: bool
    spectral_rank_table: tuple[dict[str, Any], ...]
    invisible_spectral_dimensions: int
    conclusion: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _spectral_data(
    hamiltonian: ArrayLike,
    omega: ArrayLike,
    probes: ArrayLike,
    *,
    tol: float = 1.0e-10,
) -> tuple[SpectralCertificate, np.ndarray, np.ndarray, np.ndarray]:
    h = validate_hamiltonian(hamiltonian, tol=tol)
    vacuum = validate_vacuum(h, omega, tol=tol)
    centered = centered_probes(probes, vacuum, tol=tol)
    h0_basis = vacuum_complement(vacuum)
    h0 = h0_basis.T @ h @ h0_basis
    eigenvalues, eigenvectors = np.linalg.eigh((h0 + h0.T) / 2.0)
    eigenvalues[np.abs(eigenvalues) < tol] = 0.0
    probe_coordinates = h0_basis.T @ centered
    raw_basis = orthonormal_basis(probe_coordinates, tol=tol)

    generated_parts: list[np.ndarray] = []
    rank_table: list[dict[str, Any]] = []
    visible_values: list[float] = []
    invisible_dimensions = 0
    for indices, value in _eigen_groups(eigenvalues, tol=tol):
        eigenspace = eigenvectors[:, indices]
        coefficients = eigenspace.T @ probe_coordinates
        coefficient_basis = orthonormal_basis(coefficients, tol=tol)
        visible_rank = coefficient_basis.shape[1]
        multiplicity = indices.size
        invisible = multiplicity - visible_rank
        if visible_rank:
            generated_parts.append(h0_basis @ eigenspace @ coefficient_basis)
            visible_values.append(value)
        invisible_dimensions += invisible
        rank_table.append(
            {
                "eigenvalue": value,
                "multiplicity": int(multiplicity),
                "visible_rank": int(visible_rank),
                "invisible_rank": int(invisible),
            }
        )

    generated = (
        np.concatenate(generated_parts, axis=1)
        if generated_parts
        else np.zeros((h.shape[0], 0))
    )
    generated = orthonormal_basis(generated, tol=tol)
    h0_dimension = h.shape[0] - 1
    dense = generated.shape[1] == h0_dimension
    true_gap = float(eigenvalues[0])
    visible_gap = float(min(visible_values))
    lowest_visible = abs(visible_gap - true_gap) <= tol
    certificate = SpectralCertificate(
        dimension=h.shape[0],
        vacuum_orthogonal_dimension=h0_dimension,
        eigenvalues_on_vacuum_orthogonal=tuple(float(x) for x in eigenvalues),
        true_gap=true_gap,
        raw_centered_probe_rank=raw_basis.shape[1],
        generated_invariant_rank=generated.shape[1],
        dense_in_vacuum_orthogonal=dense,
        state_separating=dense,
        visible_gap=visible_gap,
        lowest_mode_visible=lowest_visible,
        spectral_rank_table=tuple(rank_table),
        invisible_spectral_dimensions=invisible_dimensions,
        conclusion=(
            "full vacuum-orthogonal spectral conclusion"
            if dense
            else "restricted conclusion on the generated invariant subspace K"
        ),
    )
    return certificate, h, h0_basis, generated


def spectral_certificate(
    hamiltonian: ArrayLike,
    omega: ArrayLike,
    probes: ArrayLike,
    *,
    tol: float = 1.0e-10,
) -> SpectralCertificate:
    """Compute true/visible gaps and the finite density-rank certificate."""

    return _spectral_data(hamiltonian, omega, probes, tol=tol)[0]


def semigroup(hamiltonian: ArrayLike, time: float) -> np.ndarray:
    h = validate_hamiltonian(hamiltonian)
    if not math.isfinite(time) or time < 0:
        raise ValueError("time must be finite and nonnegative")
    eigenvalues, eigenvectors = np.linalg.eigh(h)
    return (eigenvectors * np.exp(-time * eigenvalues)) @ eigenvectors.T


@dataclass(frozen=True)
class BilinearDecayCertificate:
    candidate_mass: float
    visible_gap: float
    generated_invariant_rank: int
    dense_extension: bool
    times: tuple[float, ...]
    generated_operator_norms: tuple[float, ...]
    candidate_bounds: tuple[float, ...]
    norm_compatible_checks_pass: bool
    full_operator_norm_checks_pass: bool | None
    conclusion: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def bilinear_decay_certificate(
    hamiltonian: ArrayLike,
    omega: ArrayLike,
    probes: ArrayLike,
    candidate_mass: float,
    times: Iterable[float],
    *,
    tol: float = 1.0e-10,
) -> BilinearDecayCertificate:
    """Check the sharp Hilbert-norm bilinear bound on the generated subspace.

    For an orthonormal basis Q of K, ``||Q* exp(-tH) Q||`` equals the
    supremum of ``|<x,exp(-tH)y>|`` over unit x,y in K.  This is the
    norm-compatible quantity that extends by density.
    """

    if not math.isfinite(candidate_mass) or candidate_mass < 0:
        raise ValueError("candidate_mass must be finite and nonnegative")
    sample_times = tuple(float(t) for t in times)
    if not sample_times or any(not math.isfinite(t) or t < 0 for t in sample_times):
        raise ValueError("times must be a nonempty finite nonnegative sequence")
    cert, h, h0_basis, generated = _spectral_data(
        hamiltonian, omega, probes, tol=tol
    )
    generated_norms: list[float] = []
    full_norms: list[float] = []
    bounds: list[float] = []
    for time in sample_times:
        transfer = semigroup(h, time)
        generated_norms.append(float(np.linalg.norm(generated.T @ transfer @ generated, 2)))
        full_norms.append(float(np.linalg.norm(h0_basis.T @ transfer @ h0_basis, 2)))
        bounds.append(math.exp(-candidate_mass * time))
    # Sampled values are useful diagnostics, but t=0 alone contains no rate
    # information.  The finite spectral theorem gives the all-time decision:
    # ||exp(-tH)|_K|| <= exp(-m t) for every t >= 0 exactly when
    # m <= min spec(H|_K).  Keep the sampled checks as hostile numerical
    # witnesses, while requiring the corresponding spectral-edge comparison
    # before calling the rate certified.
    sampled_restricted_pass = all(
        left <= right + tol for left, right in zip(generated_norms, bounds)
    )
    sampled_full_pass = all(
        left <= right + tol for left, right in zip(full_norms, bounds)
    )
    restricted_pass = sampled_restricted_pass and candidate_mass <= cert.visible_gap + tol
    full_pass = sampled_full_pass and candidate_mass <= cert.true_gap + tol
    return BilinearDecayCertificate(
        candidate_mass=float(candidate_mass),
        visible_gap=cert.visible_gap,
        generated_invariant_rank=cert.generated_invariant_rank,
        dense_extension=cert.dense_in_vacuum_orthogonal,
        times=sample_times,
        generated_operator_norms=tuple(generated_norms),
        candidate_bounds=tuple(bounds),
        norm_compatible_checks_pass=restricted_pass,
        full_operator_norm_checks_pass=full_pass if cert.dense_in_vacuum_orthogonal else None,
        conclusion=(
            "the bilinear estimate extends to all of omega-perp"
            if cert.dense_in_vacuum_orthogonal and restricted_pass
            else "only the generated invariant subspace K is certified"
            if restricted_pass
            else "the proposed decay rate is not certified"
        ),
    )


def transfer_from_hamiltonian(hamiltonian: ArrayLike, step_size: float) -> np.ndarray:
    if not math.isfinite(step_size) or step_size <= 0:
        raise ValueError("step_size must be finite and positive")
    return semigroup(hamiltonian, step_size)


def transfer_spectral_certificate(
    transfer: ArrayLike,
    omega: ArrayLike,
    step_size: float,
    *,
    tol: float = 1.0e-10,
) -> dict[str, Any]:
    """Recover the finite physical-time spectral rate from a positive transfer."""

    if not math.isfinite(step_size) or step_size <= 0:
        raise ValueError("step_size must be finite and positive")
    matrix = _real_array(transfer, name="transfer")
    if matrix.ndim != 2 or matrix.shape[0] == 0 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("transfer must be a nonempty square matrix")
    if not np.allclose(matrix, matrix.T, atol=tol, rtol=0.0):
        raise ValueError("transfer must be self-adjoint")
    eigenvalues = np.linalg.eigvalsh((matrix + matrix.T) / 2.0)
    if float(np.min(eigenvalues)) <= tol:
        raise ValueError("transfer must be strictly positive")
    if float(np.max(eigenvalues)) > 1.0 + tol:
        raise ValueError("transfer must be a contraction")
    vacuum = _real_array(omega, name="vacuum").reshape(-1)
    if vacuum.shape != (matrix.shape[0],) or abs(float(np.linalg.norm(vacuum)) - 1.0) > tol:
        raise ValueError("vacuum must be normalized and dimension-compatible")
    if float(np.linalg.norm(matrix @ vacuum - vacuum)) > tol:
        raise ValueError("vacuum must be a unit-eigenvalue transfer state")
    h0_basis = vacuum_complement(vacuum)
    restricted = h0_basis.T @ matrix @ h0_basis
    largest_excited = float(np.max(np.linalg.eigvalsh(restricted)))
    step_exponent = -math.log(largest_excited)
    return {
        "step_size": step_size,
        "largest_excited_transfer_eigenvalue": largest_excited,
        "decay_exponent_per_step": step_exponent,
        "physical_time_gap": step_exponent / step_size,
        "positive_self_adjoint_contraction": True,
    }


def hidden_low_mode_fixture() -> dict[str, Any]:
    h = np.diag([0.0, 0.4, 1.2])
    omega = np.array([1.0, 0.0, 0.0])
    hidden = spectral_certificate(h, omega, np.array([0.0, 0.0, 1.0]))
    dense = spectral_certificate(h, omega, np.eye(3)[:, 1:])
    return {
        "hamiltonian_diagonal": [0.0, 0.4, 1.2],
        "hidden_core": hidden.to_dict(),
        "dense_core": dense.to_dict(),
        "overestimate": hidden.visible_gap - hidden.true_gap,
    }


def multiplicity_fixture() -> dict[str, Any]:
    h = np.diag([0.0, 0.4, 0.4, 1.2])
    omega = np.array([1.0, 0.0, 0.0, 0.0])
    probes = np.array([[0.0], [1.0], [1.0], [1.0]])
    cert = spectral_certificate(h, omega, probes)
    return {
        "certificate": cert.to_dict(),
        "lesson": "visible_gap_equals_true_gap does not imply density when an eigenspace has unseen multiplicity",
    }


def physical_time_collapse(levels: int = 7) -> dict[str, Any]:
    """Positive per-step exponents a^2 whose physical rates a collapse."""

    if not isinstance(levels, int) or isinstance(levels, bool) or levels < 2:
        raise ValueError("levels must be an integer at least two")
    rows: list[dict[str, float]] = []
    for level in range(levels):
        cutoff = 2.0 ** (-level)
        transfer = np.diag([1.0, math.exp(-(cutoff**2))])
        cert = transfer_spectral_certificate(transfer, [1.0, 0.0], cutoff)
        rows.append({"cutoff": cutoff, **cert})
    return {
        "family": "T_a = diag(1, exp(-a^2))",
        "levels": rows,
        "all_step_exponents_positive": all(row["decay_exponent_per_step"] > 0 for row in rows),
        "physical_rates_strictly_decrease": all(
            left["physical_time_gap"] > right["physical_time_gap"]
            for left, right in zip(rows, rows[1:])
        ),
        "limiting_physical_gap": 0.0,
    }


def results() -> dict[str, Any]:
    hidden = hidden_low_mode_fixture()
    h = np.diag([0.0, 0.4, 1.2])
    omega = np.array([1.0, 0.0, 0.0])
    times = [0.0, 0.25, 1.0, 3.0]
    hidden_decay = bilinear_decay_certificate(h, omega, [0.0, 0.0, 1.0], 1.2, times)
    dense_decay = bilinear_decay_certificate(h, omega, np.eye(3)[:, 1:], 0.4, times)
    transfer = transfer_spectral_certificate(
        transfer_from_hamiltonian(h, 0.25), omega, 0.25
    )
    return {
        "stage": 76,
        "hypothesis": "H9 temporal density",
        "claim_level": "C2 finite theorem and executable calibration",
        "main_theorem": {
            "finite_density_criterion": "K = omega-perp iff rank(K) = dim(H)-1",
            "spectral_closure": "K = direct_sum_lambda ran(P_lambda restricted to D)",
            "dense_extension": "a Hilbert-norm bilinear e^{-mt} bound on dense K extends to the full omega-perp operator norm",
            "incomplete_conclusion": "without density, only the invariant subspace K has the certified visible gap",
        },
        "hidden_low_mode_1_2_vs_0_4": hidden,
        "multiplicity_counterexample": multiplicity_fixture(),
        "norm_compatible_bilinear_decay": {
            "hidden_core": hidden_decay.to_dict(),
            "dense_core": dense_decay.to_dict(),
        },
        "positive_transfer_certificate": transfer,
        "cutoff_physical_time_collapse": physical_time_collapse(),
        "scope": {
            "finite_self_adjoint_theorem": True,
            "density_rank_criterion": True,
            "restricted_subspace_guardrail": True,
            "os_reconstruction_constructed": False,
            "continuum_theory_identity_established": False,
            "continuum_yang_mills_mass_gap": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        type=Path,
        default=Path(__file__).with_name("dense_core_spectral_results.json"),
    )
    args = parser.parse_args()
    payload = results()
    args.write.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
