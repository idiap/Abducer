<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Parsimonious Probe Policy

This policy controls when Abducer should derive a formula, estimate an
inequality, run a tiny numerical probe, or refuse computation during qualitative
physics reasoning.

## Decision Ladder

1. **Exact symbolic derivation first.** Use algebraic manipulation when the
   carrier is finite and typed, such as a normalized Hermitian matrix,
   determinant, minor, quotient phase, diagonal rephasing equation, or
   Schur/Hadamard quotient.
2. **Analytic estimates second.** If the exact interface is known, ask what
   bound, positivity condition, limit interchange, density claim, or
   same-theory transfer certificate would make the interface relevant to the
   target.
3. **Bounded numeric probes third.** Run a small deterministic search only if it
   answers a named qualitative decision question, such as whether a proposed
   inequality is sharp or whether a parameter region creates a falsifier shape.
4. **Full simulation only as evidence-only.** Heavy simulations and lattice
   frameworks may motivate hypotheses or evidence requests, but they do not
   discharge proof obligations without an analytic transfer certificate.

## Probe Classes

- `symbolic_formula`: an exact finite algebra identity or equivalent condition.
- `analytic_estimate`: a theorem-shaped estimate or continuity obligation
  induced by a symbolic interface.
- `bounded_numeric_search`: a small reproducible search over a bounded domain
  with a stated stopping condition and non-proof boundary.
- `toy_model_execution`: a concrete model used to expose a mechanism or failure
  mode, not to prove the target.
- `external_lattice_evidence`: related empirical or computational evidence kept
  outside the proof-promotion path.
- `not_needed`: computation adds no decision value because the qualitative
  relation is already symbolically or analytically typed.

## Proof Safety

Numeric and simulation outputs may be recorded only as `calibration_only`,
`validated_probe`, `falsifier_candidate`, or `evidence_task`. They may not be
promoted to `proof_obligation_discharged`, `established`, or theorem progress
unless a separate analytic transfer certificate proves that the computed carrier
is the same mathematical object required by the target.

## Current Yang-Mills Default

For the current finite quotient obstruction in the Yang-Mills exploration, the
right first move is symbolic:

\[
\det Q = 1-\rho_{12}^{2}-\rho_{23}^{2}-\rho_{13}^{2}
  +2\rho_{12}\rho_{23}\rho_{13}\cos\Phi .
\]

This formula is valid for a normalized Hermitian three-by-three quotient matrix
with diagonal entries one, off-diagonal moduli
\(0 \le \rho_{ij} \le 1\), and gauge-invariant quotient holonomy
\(\Phi=\arg(q_{12}q_{23}q_{31})\). It gives a finite algebra interface. The
Yang-Mills work starts only after this interface is translated into analytic
obligations: boundary OPE control, additive contact control, quotient phase
control, modulus quotient positivity, and same-theory observable realization.

## Examples

- A three-hairpin Schur quotient should derive determinant and minor
  inequalities before any numerical sampling.
- A quotient phase obstruction should ask whether diagonal rephasing can remove
  phases; if the cycle product has nonzero phase, the obstruction is a holonomy,
  not a coordinate artifact.
- Boundary OPE coefficient estimates should be posed as analytic estimate
  obligations before they are sampled.
- Noncommuting-limit toy functions may be executed as toy models to expose
  order-of-limits hazards, but they remain conceptual probes.
- Spectral-measure tail examples may calibrate how decay bounds behave, but they
  do not construct the Hilbert space or prove a spectral gap.

## Dependency Policy

The optional PMP environment uses:

- `sympy` for exact finite symbolic algebra.
- `numpy` for bounded deterministic grids.
- `scipy` for rare local optimization probes after formulas exist.

The workflow must degrade gracefully without these packages. Exact known
formulas and small pure-Python grids remain available.

`qutip` is not selected for the current finite-matrix and spectral-measure probe
layer: its natural domain is open quantum-system dynamics, not the present
quotient determinant, PSD, holonomy, and analytic-estimate interface.

Chroma, openQCD, Bridge++, Grid, and similar lattice gauge frameworks are future
evidence-only integrations. They are not part of the proof-control loop unless a
separate workflow explicitly scopes them as evidence acquisition.
