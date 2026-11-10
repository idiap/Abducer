<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Equational Symbolic Reasoning Layer

This layer gives Abducer a non-Lean way to turn conceptual discovery progress
into exact finite algebra interfaces. It is deliberately narrower than theorem
proving and narrower than simulation.

## Scope

Allowed tasks:

- exact determinant expansion for finite matrices;
- principal minor and PSD side-condition extraction;
- Schur/Hadamard quotient normalization;
- quotient holonomy and cycle-product algebra;
- diagonal rephasing and coboundary equations;
- symbolic counterexample-family and falsifier-shape generation;
- formula-to-analytic-obligation extraction.

Excluded tasks for this phase:

- Lean proof generation, Lake builds, mathlib integration, or theorem-prover
  proof checking;
- continuum Yang-Mills formalization;
- unbounded CAS exploration;
- full lattice simulation;
- promotion of a finite algebra identity into proof progress without a
  separate analytic transfer certificate.

## Status Labels

- `symbolic_formula`: an exact identity or equivalence in a finite carrier.
- `equational_interface`: a structured packet containing formulas, variables,
  side conditions, falsifiers, and obligations.
- `side_condition_ledger`: the explicit assumptions under which formulas are
  valid.
- `falsifier_shape`: a formula-derived failure pattern that can guide branch
  demotion or bounded search.
- `analytic_obligation`: a theorem-shaped estimate or same-theory condition
  that remains open after the finite algebra is known.

## Discovery Value

The point is not to prove the target. The point is to remove ambiguity from the
interface between creative hypothesis exploration and proof-control. A symbolic
packet tells the loop:

- which variables are actually in play;
- which assumptions are required before the formula is valid;
- which exact identities are available;
- which side conditions would fail a branch;
- which analytic estimates must be proved next.

For the Yang-Mills run, the current carrier is a normalized Hermitian
three-by-three quotient matrix:

\[
\det Q =
1-\rho_{12}^{2}-\rho_{23}^{2}-\rho_{13}^{2}
+2\rho_{12}\rho_{23}\rho_{13}\cos\Phi .
\]

This is valid only when \(Q_{ii}=1\), \(Q=Q^{*}\),
\(Q_{ij}=\rho_{ij}e^{i\theta_{ij}}\), \(0\le\rho_{ij}\le1\), and
\(\Phi=\arg(Q_{12}Q_{23}Q_{31})\) is the invariant quotient holonomy under
diagonal rephasing. It says what finite positivity requires. It does not
construct Yang-Mills, a Hilbert space, or a mass gap.

A target-agnostic example is a finite correlation matrix in any theory where a
proposed mechanism implies pairwise compatibility. The equational layer can
show that pairwise constraints do not imply global PSD unless a determinant or
cycle-holonomy side condition also holds.

## Backend Policy

SymPy is the preferred optional backend for determinant expansion,
simplification, and symbolic equation manipulation. Sage may be useful later for
heavier algebraic exploration, but it is not required for the initial finite
matrix layer. Known current formulas must have manual fallbacks so the workflow
can validate without any CAS installed.

Lean, Lake, mathlib, and theorem-prover proof checking are out of scope for this
phase.
