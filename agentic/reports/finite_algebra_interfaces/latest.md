<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Finite Algebra Interfaces

- Target: `yang-mills-existence-and-mass-gap-target`
- Packet: `esr.interface.2cf225a1bb1a`
- Status: `equational_interface`
- Carrier: normalized Hermitian three-observable quotient matrix

## Exact Identities

### normalized Hermitian three-by-three determinant
\[\det Q = 1-\rho_{12}^{2}-\rho_{23}^{2}-\rho_{13}^{2}+2\rho_{12}\rho_{23}\rho_{13}\cos\Phi\]
- Valid when: Q is a normalized Hermitian 3x3 quotient matrix, 0 <= rho_ij <= 1, and Phi is the gauge-invariant cycle phase arg(Q_12 Q_23 Q_31).
- Backend: `manual_fallback`

### pairwise minor constraints
\[1-\rho_{ij}^{2}\ge 0\quad(1\le i<j\le3)\]
- Valid when: Each two-by-two principal minor of Q is required to be nonnegative.
- Backend: `manual_fallback`

### diagonal rephasing invariant
\[\Phi=\arg(Q_{12}Q_{23}Q_{31})\]
- Valid when: Q is compared modulo diagonal unitary rephasings DQD*.
- Backend: `manual_fallback`

## Side Conditions

- `side.hermitian` Q=Q*: PSD and principal minors are Hermitian matrix notions.
- `side.normalized-diagonal` Q_ii=1: The determinant formula is normalized by the diagonal Gram entries.
- `side.nonzero-quotient-entries` quotient denominators are nonzero: Schur/Hadamard quotient and phase variables must be defined.
- `side.phase-convention` Phi=arg(Q_12 Q_23 Q_31) modulo diagonal rephasing: Only the cycle product phase is invariant under local diagonal phase choices.
- `side.finite-family-scope` all entries come from one finite reflected observable family: Mixing carriers would turn the determinant test into an analogy.

## Formula-Derived Falsifier Shapes

- `fals.det-negative-pairwise-pass`: pairwise minors pass while the 3x3 determinant is negative -> Demote any route claiming pairwise quotient damping implies finite-family positivity.
- `fals.nonzero-cycle-holonomy`: no diagonal D removes all quotient phases on the support graph -> Require a phase-control lemma before Schur quotient positivity transfer.
- `fals.modulus-quotient-minor-negative`: real pairwise bounds do not produce PSD modulus quotient -> Backtrack from modulus-only positivity transfer to analytic PSD estimates.
- `fals.additive-contact-nonzero`: the quotient identity fails to represent the continuum carrier without extra contact terms -> Route next work to contact-control estimates rather than determinant algebra.

## Non-Claims

- This packet is not Lean checked.
- This packet is not theorem-prover output.
- This packet is not continuum Yang-Mills proof progress.
- This packet is not a simulation.
- This packet does not prove a mass gap.
