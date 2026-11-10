# cycle-0222

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Rank-one-normalized Wilson collar quotients have a valid second-order OS obstruction: if M_eta=11^*+eta H+eta^2 K+o(eta^2) is required to be positive for eta>0, then PHP>=0 on 1^perp, and on L=ker(PHP) the Schur-corrected form Omega_2=PKP-n^{-2}PH11^*HP must be nonnegative. This test is invariant under harmless one-body diagonal Wilson renormalizations.

## Definitions

- source object: finite locked reflected Wilson collar quotient blocks M_eta=widehat N_eta oslash widehat B_eta from regulated reflection-positive Schwinger forms, after diagonal normalization M_{ii}=1 and common boundary-footprint collapse.
- target object: OS-positive continuum Schwinger functions on the unchanged gauge-invariant Wilson algebra, equivalently all finite same-theory reflected quadratic matrices are positive semidefinite.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions by closed-cone passage plus finite Schur-preimage positivity of Wilson boundary quotients.
- same-theory condition: diagonal/rank-one one-body Wilson factors may be absorbed as congruences, but no mixed boundary counterterm, non-diagonal Schur factor, or observable-algebra change may be used to repair positivity.

## Assumptions

- M_eta is Hermitian and entrywise admits a two-term boundary OPE expansion M_eta=11^*+eta H+eta^2 K+o(eta^2) for eta downarrow 0.
- e=n^{-1/2}1 and P=I-ee^*; H and K are the locked mixed boundary OPE coefficients after additive positive contacts have been eliminated by diagonal trace continuity.
- The expansion remainder is uniform on the chosen finite Wilson block, so Schur-complement signs are valid for sufficiently small eta.
- The Schur denominator n+eta e^*He+O(eta^2) stays positive, which follows from the rank-one leading block 11^*.

## Equations

- finite Schur-preimage OS matrix: `M_\eta=\widehat N_\eta\oslash\widehat B_\eta,\qquad M_\eta\ge 0`. Valid when: Additive contacts have vanished, every boundary factor entry in widehat B_eta is nonzero, and this is the same Wilson test family before and after collar collapse.
- rank-one boundary expansion: `M_\eta=\mathbf 1\mathbf 1^*+\eta H+\eta^2K+o(\eta^2)`. Valid when: The reflected Wilson boundary OPE is valid entrywise with a uniform finite-block remainder.
- first tangent gate: `P H P\ge 0\quad\text{on }\mathbf 1^\perp`. Valid when: M_eta is positive for all sufficiently small eta>0; a negative vector in 1^perp is an immediate falsifier.
- second tangent gate: `x^*\left(PKP-n^{-2}PH\mathbf 1\mathbf 1^*HP\right)x\ge0,\qquad x\in\ker(PHP)`. Valid when: The first gate is semidefinite and x lies in its null space; this is the Schur complement against the large rank-one OS direction.

## Attempted Derivation

- Normalize a finite Wilson collar quotient so its leading collapsed block is J=11^* and its diagonal entries are one.
- Decompose C^n=C e direct sum e^perp with e=n^{-1/2}1 and P=I-ee^*.
- Write the block Schur complement of M_eta relative to the large eigenvalue n+eta e^*He+O(eta^2).
- The projected Schur complement is eta PHP+eta^2(PKP-n^{-1}PHee^*HP)+o(eta^2), equivalently eta PHP+eta^2(PKP-n^{-2}PH11^*HP)+o(eta^2).
- Therefore a negative value of PHP on 1^perp gives a first-order determinant falsifier; if PHP has a null vector, the corrected second-order form decides the next obstruction.
- Check diagonal congruence D_eta: H gains a1^*+1a^*, K gains the expected cross terms. On x in ker(PHP), the added |x^*a|^2 and cross terms cancel exactly against the changed Schur correction.

Blocking gap: No Yang-Mills estimate yet supplies the finite-block reflected Wilson boundary OPE coefficients H,K with a valid uniform remainder for actual hairpin/cusp collars.

## Falsifiers

- falsifier: a locked Wilson block with some x in 1^perp and x^*PHPx<0, producing a negative OS determinant at order eta.
- falsifier: PHP>=0 but a null vector x has x^*(PKP-n^{-2}PH11^*HP)x<0.
- falsifier: a three-hairpin quotient determinant det(widehat N oslash widehat B)<0 even though all pairwise damping inequalities are valid.
- falsifier: positivity can be restored only by a non-diagonal boundary counterterm or by changing the Wilson test algebra at the reflection plane.
- falsifier: the RG cutoff-removal topology does not control the reflected Wilson OPE remainder strongly enough to make the tangent expansion valid.

## Learning

Cycle 222 made the second-order Wilson obstruction normalization-invariant. The valid finite test is not PKP alone: the large rank-one OS direction subtracts n^{-2}PH11^*HP. This correction also cancels every one-body diagonal Wilson renormalization, so a remaining negative value is a genuine mixed boundary falsifier. The branch has therefore isolated a concrete analytic target: compute H and K for locked reflected Wilson hairpin blocks with uniform collar remainders.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Pick three mirror-smooth Wilson hairpin observables with a common reflection-plane footprint, derive the boundary OPE coefficients H and K for M_eta=widehat N_eta oslash widehat B_eta, and test PHP and Omega_2 on 1^perp and ker(PHP).
