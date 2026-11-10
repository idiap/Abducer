<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Proof By Contradiction Route Validation

- Fixture routes: 4
- Active bridge routes: 3
- Verdict mismatches: 0
- Critical findings: 5

## Generative Review

The validation probes separate typed structure from mathematical interpretation. The valid no-gap route is accepted only as a proof obligation because observable density, spectral support, and cutoff-uniform decay remain to be proved. The bad fixtures are not merely schema failures: cross-cutoff contradiction is quarantined, overstrong negation is repaired, and missing OS-positivity closedness becomes an evidence-acquisition task.

## fixture.valid-no-gap-spectral-reductio

- Source: `fixture`
- Computed verdict: `promote`
- Expected verdict: `promote`
- Mathematical learning: The route is promotable as a proof obligation: it has a precise negation, same-theory carrier, explicit conflict target status, and domain-specific mathematical obligations.

## fixture.invalid-cross-cutoff-gap

- Source: `fixture`
- Computed verdict: `quarantine`
- Expected verdict: `quarantine`
- Mathematical learning: The route teaches a boundary: contradiction cannot be derived by crossing cutoff, Hilbert-space, observable, or theory identity.

### Findings
- `cross_theory_slippage`: Cross-theory or cutoff slippage detected: finite lattice only, fixed cutoff only.
- `incompatible_conflict_target`: Conflict target belongs to an incompatible object or regime.

## fixture.too-strong-negation

- Source: `fixture`
- Computed verdict: `repair`
- Expected verdict: `repair`
- Mathematical learning: The route teaches that reductio pressure begins with the exact logical negation; overstrong assumptions make the contradiction mathematically uninformative.

### Findings
- `weak_exact_negation`: Exact negation is too thin to control quantifiers and objects.
- `too_strong_negation`: Negation appears stronger than the target: every possible, all observables vanish.

## fixture.missing-conflict-target

- Source: `fixture`
- Computed verdict: `evidence-acquire`
- Expected verdict: `evidence-acquire`
- Mathematical learning: The reductio has the right shape but teaches that the missing theorem or closedness result must be acquired before contradiction can carry proof weight.

### Findings
- `missing_conflict_target`: Conflict target is not established; this is an evidence task, not proof progress.

## ym-reductio.166efc89f93d

- Source: `yang_mills_bridge_packet`
- Computed verdict: `promote`
- Expected verdict: `promote`
- Mathematical learning: The route is promotable as a proof obligation: it has a precise negation, same-theory carrier, explicit conflict target status, and domain-specific mathematical obligations.

## ym-reductio.5c647a12c20d

- Source: `yang_mills_bridge_packet`
- Computed verdict: `promote`
- Expected verdict: `promote`
- Mathematical learning: The route is promotable as a proof obligation: it has a precise negation, same-theory carrier, explicit conflict target status, and domain-specific mathematical obligations.

## ym-reductio.c3895125c2cd

- Source: `yang_mills_bridge_packet`
- Computed verdict: `promote`
- Expected verdict: `promote`
- Mathematical learning: The route is promotable as a proof obligation: it has a precise negation, same-theory carrier, explicit conflict target status, and domain-specific mathematical obligations.
