# cycle-0220

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: Wilson quotient tangent cone

## Candidate Lemma

Second-order tangent-cone bridge for Wilson collar collapse. For a locked finite Wilson block with normalized same-theory quotient q_eta tending to the all-one matrix J, target OS positivity forces PHP>=0 on 1^perp and, on ker(PHP), the corrected second-order form P(K-n^{-1}Huu^*H)P to be nonnegative. A negative value is a finite Wilson falsifier.

## Definitions

- source object: finite collar Wilson OS blocks N_eta obtained as RG limits of regulated reflection-positive gauge-invariant Schwinger forms
- target object: continuum OS matrix for the same locked Wilson observables after the collar is collapsed to the reflection plane
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, reduced to finite Schur-preimage positivity q_eta>=0
- same-theory condition: the boundary collapse may use only the prescribed Wilson renormalization; any extra multiplicative factor B_eta must be divided out without adding boundary degrees of freedom or changing the test algebra
- u=n^{-1/2}(1,...,1) and P=I-uu^* project off the rank-one OS vacuum direction.
- J is the all-one matrix, J=n uu^*. q_eta is the normalized Schur quotient q_eta=widehat N_eta oslash widehat B_eta.

## Assumptions

- The fixed-collar closed-cone passage is valid: N_eta>=0 for each eta>0 after cutoff removal.
- B_eta is Hermitian with positive diagonal and no zero entries on the finite block.
- The quotient has a uniform boundary OPE expansion q_eta=J+eta H+eta^2 K+o(eta^2) with H,K Hermitian and q_eta,ii=1.
- The finite Wilson block is locked before taking eta->0, so the quotient tests the same theory rather than an enlarged boundary algebra.

## Equations

- normalized quotient expansion: `q_\eta=\widehat N_\eta\oslash\widehat B_\eta=J+\eta H+\eta^2K+o(\eta^2),\quad J_{ij}=1`. Valid when: Valid when the reflected Wilson boundary OPE is uniform on the chosen finite block and diagonal renormalizations have been removed by congruence.
- Schur complement after removing J direction: `S_\eta=\eta PHP+\eta^2P\bigl(K-n^{-1}Huu^*H\bigr)P+o(\eta^2)`. Valid when: Valid for u=n^{-1/2}(1,...,1), P=I-uu^*, and eta small enough that the rank-one block n+O(eta) is invertible.
- first and second tangent gates: `PHP\ge0,\qquad x^*P\bigl(K-n^{-1}Huu^*H\bigr)Px\ge0\quad(x\in\ker(PHP))`. Valid when: Necessary for q_eta>=0 as eta downarrow 0; sufficient to second order if the displayed forms have a positive gap on their active subspaces.

## Attempted Derivation

- Start with regulated reflection positivity: every cutoff collar block N_{a,L,eta} is PSD for gauge-invariant Wilson observables supported in t>eta.
- Use the cutoff-removal topology only on fixed collars to pass to N_eta>=0. This part is a valid closed-cone argument.
- Model the eta->0 collapse by a multiplicative boundary matrix B_eta. The target same-theory matrix is M_eta=B_eta^{[-1]} circ N_eta, not N_eta itself.
- Normalize by positive diagonals. OS positivity of M_eta is equivalent to PSD of q_eta=widehat N_eta oslash widehat B_eta.
- Assume a finite-block boundary OPE q_eta=J+eta H+eta^2K+o(eta^2). Decompose C^n=span{u} plus u^perp.
- The u-block equals n+O(eta), so it is invertible. Its Schur complement on u^perp is eta PHP+eta^2 P(K-n^{-1}Huu^*H)P+o(eta^2).
- Therefore q_eta>=0 forces PHP>=0. If x lies in ker(PHP), the eta^2 coefficient gives the corrected second-order test.

Blocking gap: No Yang-Mills estimate currently computes or bounds the finite-block Wilson boundary OPE coefficients H and K for reflected hairpins with coincident boundary footprint.

## Falsifiers

- falsifier: a locked Wilson block with a zero-sum vector x and x^*PHPx<0 gives an immediate negative OS determinant for small collar width.
- falsifier: PHP>=0 but a null vector x has x^*P(K-n^{-1}Huu^*H)Px<0, showing a second-order boundary obstruction.
- falsifier: the collar collapse produces B_ij=0 or a nonmultiplicative/additive boundary contact not killed by diagonal trace continuity, so q is not a valid same-theory quotient.
- falsifier: RG convergence controls fixed collars but not the reflected Wilson OPE uniformly as eta->0, leaving the closed-cone topology too weak for the target OS matrix.

## Learning

Cycle 220 converts the previous warning about second order into a precise valid tangent-cone lemma. The rank-one OS direction contributes the correction -n^{-1}Huu^*H, so the next falsifier is not just a negative K term but a negative Schur-corrected boundary OPE form on ker(PHP). The branch has reduced the nonformal Yang-Mills task to computing H and K for locked reflected Wilson blocks.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the boundary OPE for three or four small reflected Wilson hairpins with common footprint; extract H,K, project to 1^perp, and test PHP and P(K-n^{-1}Huu^*H)P on the null space.
