<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Contradiction Route Template

Use this template for any proof-by-contradiction branch.

## Route Packet

- `target_claim`: What is being proved or refined?
- `exact_negation`: What is the precise negated assumption, with quantifiers?
- `ambient_commitments`: Which definitions, axioms, KB claims, construction
  regimes, and artifacts stay in force?
- `contradiction_carrier`: Which mathematical object carries the contradiction?
- `derivation_sketch`: What does the negated assumption force?
- `conflict_target`: What accepted theorem, axiom, invariant, or validator-backed
  artifact is contradicted?
- `obligations`: Which lemmas are still required?
- `backtrack_signal`: What would show that the contradiction route does not pay
  off?
- `pivot_option`: Which direct, abductive, counterexample, or representation
  route should take over if this branch stalls?

## Yang-Mills Examples

- No-gap assumption: for every epsilon > 0, there exists psi_epsilon
  orthogonal to Omega with ||psi_epsilon|| = 1 and
  <psi_epsilon,H psi_epsilon> < epsilon. The carrier is a low-energy spectral
  measure or approximating observable sequence. The conflict target is a
  cutoff-uniform Euclidean decay estimate plus density of gauge-invariant
  observables in the vacuum-orthogonal sector.
- Trivial-limit assumption: all connected gauge-invariant cumulants in the
  continuum limit vanish or reduce to a Gaussian/free pattern. The carrier is
  a connected Wilson-loop or local gauge-invariant cumulant. The conflict
  target is a same-theory nontriviality witness.
- OS-positivity failure assumption: the limiting Schwinger functions admit a
  negative reflection form. The carrier is the negative quadratic form. The
  conflict target is reflection positivity of approximants plus closedness in
  the chosen topology.

## Required Interpretation

Never stop at the schema. Explain what the contradiction would mean
mathematically, why it matters for the target, what could make it fail, and
which loop action is justified next.
