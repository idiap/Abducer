"""Exact finite core for the relational-rigidity Yang--Mills programme.

This module checks finite spectral supports and typed representation-morphism
bookkeeping.  It intentionally does not approximate or claim the analytic
four-dimensional continuum estimates.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from typing import FrozenSet, Iterable, Sequence, Tuple


Q = Fraction


def _q(value: int | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


@dataclass(frozen=True)
class SpectralAtom:
    energy: Fraction
    weight: Fraction

    def __post_init__(self) -> None:
        if self.energy < 0:
            raise ValueError("positive-energy condition failed")
        if self.weight < 0:
            raise ValueError("spectral positivity failed")


@dataclass(frozen=True)
class SpectralMeasure:
    """A finite positive spectral measure for one centered observable vector."""

    atoms: Tuple[SpectralAtom, ...]

    @classmethod
    def from_pairs(
        cls, pairs: Iterable[tuple[int | Fraction, int | Fraction]]
    ) -> "SpectralMeasure":
        return cls(tuple(SpectralAtom(_q(e), _q(w)) for e, w in pairs))

    def support(self) -> Tuple[Fraction, ...]:
        return tuple(sorted({a.energy for a in self.atoms if a.weight > 0}))

    def support_gap(self, centered: bool = True) -> Fraction | None:
        energies = [a.energy for a in self.atoms if a.weight > 0]
        if centered:
            energies = [e for e in energies if e > 0]
        return min(energies) if energies else None

    def has_support_below(self, mass: int | Fraction) -> bool:
        m = _q(mass)
        return any(a.weight > 0 and 0 < a.energy < m for a in self.atoms)

    def certifies_decay_rate(self, mass: int | Fraction) -> bool:
        """Exact finite form of support in {0} union [mass, infinity)."""
        m = _q(mass)
        if m <= 0:
            raise ValueError("mass must be positive")
        return not self.has_support_below(m)


@dataclass(frozen=True)
class FiniteHamiltonian:
    """A finite diagonal Hamiltonian with a declared unique vacuum index."""

    energies: Tuple[Fraction, ...]
    vacuum_index: int = 0

    @classmethod
    def diagonal(
        cls, energies: Sequence[int | Fraction], vacuum_index: int = 0
    ) -> "FiniteHamiltonian":
        return cls(tuple(_q(e) for e in energies), vacuum_index)

    def __post_init__(self) -> None:
        if not self.energies:
            raise ValueError("Hamiltonian must be nonempty")
        if not 0 <= self.vacuum_index < len(self.energies):
            raise ValueError("invalid vacuum index")
        if any(e < 0 for e in self.energies):
            raise ValueError("Hamiltonian must be positive")
        if self.energies[self.vacuum_index] != 0:
            raise ValueError("declared vacuum must have zero energy")
        if sum(e == 0 for e in self.energies) != 1:
            raise ValueError("this core requires a unique vacuum")

    @property
    def gap(self) -> Fraction | None:
        positive = [e for e in self.energies if e > 0]
        return min(positive) if positive else None

    def spectral_measure(self, squared_amplitudes: Sequence[int | Fraction]) -> SpectralMeasure:
        if len(squared_amplitudes) != len(self.energies):
            raise ValueError("amplitude dimension mismatch")
        weights = tuple(_q(x) for x in squared_amplitudes)
        if any(w < 0 for w in weights):
            raise ValueError("squared amplitudes must be nonnegative")
        if weights[self.vacuum_index] != 0:
            raise ValueError("observable vector is not centered")
        return SpectralMeasure(tuple(SpectralAtom(e, w) for e, w in zip(self.energies, weights)))


@dataclass(frozen=True)
class MorphismCertificate:
    gauge_invariant: bool = True
    reflection_positive: bool = True
    local: bool = True
    observable_complete: bool = True
    uniform_in_volume: bool = True

    def compose(self, other: "MorphismCertificate") -> "MorphismCertificate":
        return MorphismCertificate(
            gauge_invariant=self.gauge_invariant and other.gauge_invariant,
            reflection_positive=self.reflection_positive and other.reflection_positive,
            local=self.local and other.local,
            observable_complete=self.observable_complete and other.observable_complete,
            uniform_in_volume=self.uniform_in_volume and other.uniform_in_volume,
        )

    def missing(self) -> FrozenSet[str]:
        return frozenset(
            name
            for name in (
                "gauge_invariant",
                "reflection_positive",
                "local",
                "observable_complete",
                "uniform_in_volume",
            )
            if not getattr(self, name)
        )


@dataclass(frozen=True)
class RepresentationMorphism:
    source: str
    target: str
    error: Fraction
    certificate: MorphismCertificate
    stages: Tuple[str, ...] = ()

    @classmethod
    def exact(
        cls, source: str, target: str, certificate: MorphismCertificate
    ) -> "RepresentationMorphism":
        return cls(source, target, Fraction(0), certificate, (f"{source}->{target}",))

    def __post_init__(self) -> None:
        if self.error < 0:
            raise ValueError("error budget cannot be negative")

    def compose(self, after: "RepresentationMorphism") -> "RepresentationMorphism":
        """Return after o self, with an additive worst-case error budget."""
        if self.target != after.source:
            raise ValueError("morphism endpoints do not compose")
        return RepresentationMorphism(
            source=self.source,
            target=after.target,
            error=self.error + after.error,
            certificate=self.certificate.compose(after.certificate),
            stages=self.stages + after.stages,
        )

    def within(self, budget: int | Fraction) -> bool:
        return self.error <= _q(budget)


def physical_gap(lattice_gap: int | Fraction, spacing: int | Fraction) -> Fraction:
    """Convert a dimensionless transfer gap to inverse-length units."""
    delta, a = _q(lattice_gap), _q(spacing)
    if delta < 0 or a <= 0:
        raise ValueError("invalid lattice gap or spacing")
    return delta / a


def observable_sector_is_complete(
    hamiltonian: FiniteHamiltonian, visible_indices: Iterable[int]
) -> bool:
    visible = set(visible_indices)
    required = {i for i, e in enumerate(hamiltonian.energies) if e > 0}
    return required <= visible


def nonuniform_gap_sequence(n: int) -> tuple[Fraction, Fraction, Fraction]:
    """Spacing a=1/n, lattice gap a^2, physical gap a -> 0."""
    if n <= 0:
        raise ValueError("n must be positive")
    a = Fraction(1, n)
    delta = a * a
    return a, delta, physical_gap(delta, a)
