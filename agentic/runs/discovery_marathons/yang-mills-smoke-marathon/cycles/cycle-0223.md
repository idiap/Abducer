# cycle-0223

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

For a locked finite reflected Wilson hairpin block with a uniform second-order collar quotient expansion near the rank-one matrix, OS positivity of the same-theory target has a valid tangent test: PHP>=0 and a Schur-corrected K-form is nonnegative on ker(PHP).

## Definitions

- source object: diagonal-normalized collar quotient matrices q_delta=Nh_delta oslash Bh_delta from regulated reflected Wilson OS blocks.
- target object: finite OS quadratic forms of the intended continuum Schwinger functions on the same Wilson observables.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions via Schur-preimage positivity after collar collapse.
- same-theory condition: remove only the locked boundary Gram factor; add no boundary observable, counterterm, or changed Wilson-loop renormalization.

## Assumptions

- Bh_delta has nonzero entries and q_delta is Hermitian with diagonal one.
- q_delta=E+eta_delta H+eta_delta^2 K+o(eta_delta^2) uniformly for the finite block, with H,K Hermitian.
- q_delta>=0 is equivalent to OS positivity of the intended Schur-preimage matrix for this block.
- The collar RG convergence is valid for all reflected Wilson products used in H and K.

## Equations

- normalized quotient expansion: `q_\delta=\widehat N_\delta\oslash\widehat B_\delta=E+\eta_\delta H+\eta_\delta^2K+o(\eta_\delta^2),\quad E={\bf1}{\bf1}^*`. Valid when: valid when the boundary Wilson OPE gives a uniform second-order collar expansion.
- Schur complement at vacuum direction: `S_\delta=\eta PHP+\eta^2P(K-n^{-1}Hee^*H)P+o(\eta^2)`. Valid when: valid for e=n^{-1/2}{\bf1}, P=I-ee^*, after eliminating the large rank-one OS direction.
- second-order falsifier: `v\in\ker(PHP),\quad v^*P(K-n^{-1}Hee^*H)Pv<0\Rightarrow q_\delta\not\ge0`. Valid when: valid for small eta_delta if the remainder is uniform on the chosen finite Wilson block.

## Attempted Derivation

- Normalize the finite Wilson block so diagonal entries are one; the collar quotient then tends to E=11^*.
- Decompose C^n=Ce plus 1^perp. Positivity of q_delta is equivalent to positivity of the Schur complement because the e-block is n+O(eta).
- Expanding the Schur complement gives eta PHP plus eta^2 P(K-n^{-1}Hee^*H)P; one-body diagonal congruences vanish under P.
- If PHP has a negative vector, or the corrected K-form is negative on ker(PHP), then q_delta has a negative quadratic form for small collars.

Blocking gap: No Yang-Mills estimate yet supplies uniform H,K and o(eta^2) for reflected Wilson hairpin products in the locked algebra.

## Falsifiers

- first-order falsifier: a vector v in 1^perp with v^*PHPv<0 for a computed Wilson hairpin block.
- second-order falsifier: PHP>=0 but u in ker(PHP) makes u^*P(K-n^{-1}Hee^*H)Pu<0.
- The collar OPE remainder is not uniform, so the tangent sign does not control actual q_delta for small cutoff.
- Bh_delta requires a boundary counterterm or changed Wilson renormalization, violating the same-theory condition.

## Learning

Cycle 223 made the Wilson obstruction a normalization-safe tangent-cone lemma. The correction -n^{-1}PHee^*HP is forced by the rank-one vacuum direction, so a negative corrected K-form is a genuine mixed boundary falsifier, not a one-body renormalization artifact.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the boundary OPE coefficients H and K for the smallest three-hairpin reflected Wilson block and test the Schur-corrected determinant.
