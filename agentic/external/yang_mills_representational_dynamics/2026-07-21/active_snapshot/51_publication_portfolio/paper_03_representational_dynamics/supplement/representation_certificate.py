"""Exact finite certificates for examples in the representation-change paper.

The module uses only integers and :class:`fractions.Fraction`.  It verifies
finite examples and bookkeeping identities; it is not a numerical proof of
the infinite-dimensional recovery-to-spectrum theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Mapping, Sequence


Q = Fraction


def _q(value: int | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def _map(entries: tuple[tuple[str, Fraction], ...]) -> dict[str, Fraction]:
    return dict(entries)


def _freeze(values: Mapping[str, int | Fraction]) -> tuple[tuple[str, Fraction], ...]:
    return tuple(sorted((key, _q(value)) for key, value in values.items()))


@dataclass(frozen=True)
class CertificateProfile:
    """A finite certificate profile for a typed representation morphism.

    ``exact`` lists channels transported without defect.  ``forgotten`` lists
    channels unavailable in the target variables.  A forgotten channel may
    also occur in ``recovered`` only when a separate recovery theorem is part
    of the morphism data.  Error and pullback-Lipschitz data are heterogeneous:
    they are keyed by the property channel rather than collapsed to one score.
    """

    exact: frozenset[str]
    forgotten: frozenset[str]
    recovered: frozenset[str]
    uniform: frozenset[str]
    errors: tuple[tuple[str, Fraction], ...]
    lipschitz: tuple[tuple[str, Fraction], ...]

    @classmethod
    def make(
        cls,
        *,
        exact: Iterable[str] = (),
        forgotten: Iterable[str] = (),
        recovered: Iterable[str] = (),
        uniform: Iterable[str] = (),
        errors: Mapping[str, int | Fraction] | None = None,
        lipschitz: Mapping[str, int | Fraction] | None = None,
    ) -> "CertificateProfile":
        return cls(
            frozenset(exact),
            frozenset(forgotten),
            frozenset(recovered),
            frozenset(uniform),
            _freeze(errors or {}),
            _freeze(lipschitz or {}),
        )

    def __post_init__(self) -> None:
        if self.exact & self.forgotten:
            raise ValueError("a channel cannot be both exact and forgotten")
        if not self.recovered <= self.forgotten:
            raise ValueError("recovery must identify a forgotten channel")
        if any(value < 0 for _, value in self.errors):
            raise ValueError("error moduli must be nonnegative")
        if any(value < 0 for _, value in self.lipschitz):
            raise ValueError("Lipschitz moduli must be nonnegative")

    @property
    def available(self) -> frozenset[str]:
        return self.exact | self.recovered

    def missing(self, required: Iterable[str]) -> frozenset[str]:
        return frozenset(required) - self.available

    def compose(self, after: "CertificateProfile") -> "CertificateProfile":
        """Return the profile of ``after o self``.

        A channel is available only if both legs transport it.  It is exact
        only if both legs do so exactly.  For a property channel ``p`` the
        expectation defect obeys

        ``epsilon_total[p] = epsilon_after[p] + L_after[p] epsilon_self[p]``.
        """

        available = self.available & after.available
        exact = self.exact & after.exact
        recovered = available - exact
        universe = (
            self.exact
            | self.forgotten
            | after.exact
            | after.forgotten
            | set(_map(self.errors))
            | set(_map(after.errors))
        )
        forgotten = frozenset(universe - exact)
        first_errors, second_errors = _map(self.errors), _map(after.errors)
        first_lip, second_lip = _map(self.lipschitz), _map(after.lipschitz)
        channels = set(first_errors) | set(second_errors)
        errors = {
            p: second_errors.get(p, Q(0))
            + second_lip.get(p, Q(1)) * first_errors.get(p, Q(0))
            for p in channels
        }
        lip_channels = set(first_lip) | set(second_lip)
        lipschitz = {
            p: second_lip.get(p, Q(1)) * first_lip.get(p, Q(1))
            for p in lip_channels
        }
        return CertificateProfile.make(
            exact=exact,
            forgotten=forgotten,
            recovered=recovered,
            uniform=self.uniform & after.uniform,
            errors=errors,
            lipschitz=lipschitz,
        )


@dataclass(frozen=True)
class RepresentationMorphism:
    source: str
    target: str
    profile: CertificateProfile

    def compose(self, after: "RepresentationMorphism") -> "RepresentationMorphism":
        if self.target != after.source:
            raise ValueError("morphism endpoints do not compose")
        return RepresentationMorphism(
            self.source, after.target, self.profile.compose(after.profile)
        )


@dataclass(frozen=True)
class FiniteSemigroup:
    """Positive diagonal semigroup with a declared unique vacuum."""

    energies: tuple[Fraction, ...]
    vacuum_index: int = 0

    @classmethod
    def diagonal(
        cls, energies: Sequence[int | Fraction], vacuum_index: int = 0
    ) -> "FiniteSemigroup":
        return cls(tuple(_q(e) for e in energies), vacuum_index)

    def __post_init__(self) -> None:
        if not self.energies:
            raise ValueError("the semigroup must be nonempty")
        if not 0 <= self.vacuum_index < len(self.energies):
            raise ValueError("invalid vacuum index")
        if any(e < 0 for e in self.energies):
            raise ValueError("the generator must be positive")
        if self.energies[self.vacuum_index] != 0:
            raise ValueError("the declared vacuum must have energy zero")
        if sum(e == 0 for e in self.energies) != 1:
            raise ValueError("this certificate requires a unique vacuum")

    @property
    def gap(self) -> Fraction | None:
        positive = [e for e in self.energies if e > 0]
        return min(positive) if positive else None

    def visible_gap(self, visible_indices: Iterable[int]) -> Fraction | None:
        visible = set(visible_indices)
        values = [e for i, e in enumerate(self.energies) if i in visible and e > 0]
        return min(values) if values else None

    def is_complete(self, visible_indices: Iterable[int]) -> bool:
        visible = set(visible_indices)
        return all(i in visible for i, e in enumerate(self.energies) if e > 0)


def uniformly_gapped_truncation(n: int) -> FiniteSemigroup:
    if n < 1:
        raise ValueError("n must be positive")
    return FiniteSemigroup.diagonal([0, *range(1, n + 1)])


def gapless_truncation(n: int) -> FiniteSemigroup:
    if n < 1:
        raise ValueError("n must be positive")
    return FiniteSemigroup.diagonal([Q(0), *(Q(1, k) for k in range(1, n + 1))])


def recovery_defect(cutoff: int, volume: int) -> int:
    """The exact noncommuting-limit array d(n,L)=1[L>n]."""
    if cutoff < 1 or volume < 1:
        raise ValueError("indices must be positive")
    return int(volume > cutoff)


def finite_certificate() -> dict[str, object]:
    channels = {"gauge", "positivity", "locality", "spectral"}
    first = RepresentationMorphism(
        "lattice",
        "blocked",
        CertificateProfile.make(
            exact={"gauge", "positivity"},
            forgotten={"locality", "spectral"},
            recovered={"locality", "spectral"},
            uniform={"gauge", "positivity", "locality"},
            errors={"observable": Q(1, 100)},
            lipschitz={"observable": Q(2)},
        ),
    )
    second = RepresentationMorphism(
        "blocked",
        "euclidean",
        CertificateProfile.make(
            exact={"gauge", "positivity", "locality"},
            forgotten={"spectral"},
            recovered={"spectral"},
            uniform=channels,
            errors={"observable": Q(1, 200)},
            lipschitz={"observable": Q(3, 2)},
        ),
    )
    composite = first.compose(second)
    uniform_gaps = [uniformly_gapped_truncation(n).gap for n in range(1, 9)]
    collapsing_gaps = [gapless_truncation(n).gap for n in range(1, 9)]
    return {
        "schema_version": 1,
        "arithmetic": "exact integers and fractions",
        "composition": {
            "source": composite.source,
            "target": composite.target,
            "exact": sorted(composite.profile.exact),
            "recovered": sorted(composite.profile.recovered),
            "missing_required": sorted(composite.profile.missing(channels)),
            "observable_error": str(_map(composite.profile.errors)["observable"]),
        },
        "spectral_examples": {
            "uniform_truncation_gaps": [str(x) for x in uniform_gaps],
            "collapsing_truncation_gaps": [str(x) for x in collapsing_gaps],
            "hidden_sector_visible_gap": str(
                FiniteSemigroup.diagonal([0, 1, Q(1, 2)]).visible_gap({1})
            ),
            "hidden_sector_physical_gap": "1/2",
        },
        "limit_order": {
            "fixed_volume_eventual_defect": 0,
            "fixed_cutoff_large_volume_defect": 1,
            "uniform_volume_defect": 1,
        },
        "all_checks_pass": (
            all(x == 1 for x in uniform_gaps)
            and collapsing_gaps[-1] == Q(1, 8)
            and composite.profile.missing(channels) == frozenset()
            and _map(composite.profile.errors)["observable"] == Q(1, 50)
        ),
        "scope": "finite examples and certificate bookkeeping only",
    }


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(finite_certificate(), indent=2) + "\n")
