<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Symbolic Matrix Probe

- Target: `yang-mills-existence-and-mass-gap-target`
- Status: `symbolic_formula`
- Backend: `manual_fallback`

## Exact Interfaces

### normalized Hermitian three-by-three determinant
\[\det Q = 1-\rho_{12}^{2}-\rho_{23}^{2}-\rho_{13}^{2}+2\rho_{12}\rho_{23}\rho_{13}\cos\Phi\]
- Valid when: Q is a normalized Hermitian 3x3 quotient matrix, 0 <= rho_ij <= 1, and Phi is the gauge-invariant cycle phase arg(Q_12 Q_23 Q_31).
- Status: `symbolic_formula`

### pairwise minor constraints
\[1-\rho_{ij}^{2}\ge 0\quad(1\le i<j\le3)\]
- Valid when: Each two-by-two principal minor of Q is required to be nonnegative.
- Status: `symbolic_formula`

### diagonal rephasing invariant
\[\Phi=\arg(Q_{12}Q_{23}Q_{31})\]
- Valid when: Q is compared modulo diagonal unitary rephasings DQD*.
- Status: `symbolic_formula`

## Falsifier Templates

- `fals.det-negative`: pairwise minors hold but det(Q) < 0 (Demote any branch claiming pairwise quotient positivity suffices for finite-family positivity.)
- `fals.nonzero-holonomy`: Phi is not 0 modulo pi after diagonal rephasing (Require phase-control or coboundary lemma before Schur quotient positivity transfer.)

## Non-Claims

- This is not a Yang-Mills existence proof.
- This does not establish a continuum Hilbert space.
- This does not prove a spectral gap.
- This is not a simulation.
