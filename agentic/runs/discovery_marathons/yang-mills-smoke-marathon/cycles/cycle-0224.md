# cycle-0224

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Finite Wilson collar quotient tangent-cone lemma: if the normalized same-theory Schur preimage has q_delta=11^*+alpha_delta H+alpha_delta^2 K+o(alpha_delta^2), alpha_delta downarrow 0, then valid OS positivity forces PHP>=0 on 1^perp and, on ker(PHP), P(K-n^{-2}H11^*H)P>=0. A negative value is a finite same-theory falsifier.

## Definitions

- source object: regulated/collar OS matrices N_delta for a locked finite family of positive-time gauge-invariant Wilson observables, with closed-cone positivity inherited from the cutoff theory.
- target object: the continuum same-theory normalized OS matrix q_delta=widehat N_delta oslash widehat B_delta obtained after removing only boundary factors already present in the locked Wilson algebra.
- controlled interface: the map (widehat N_delta,widehat B_delta) -> q_delta and its expansion must be controlled for every finite reflected quadratic form in the cutoff-removal topology.
- same-theory condition: diagonal Wilson normalizations may be absorbed by fixed congruence, but no boundary counterterm, pair-dependent renormalization, or enlargement of the gauge-invariant test algebra is allowed.

## Assumptions

- The finite Wilson collar family has nonzero normalized boundary entries widehat B_{ij,delta} and additive positive contacts have vanished by diagonal trace continuity.
- q_delta is Hermitian with diagonal one and q_delta>=0 is exactly the intended finite OS condition after the collar Schur-preimage step.
- There is a scale alpha_delta>0 and Hermitian matrices H,K such that q_delta=E+alpha_delta H+alpha_delta^2 K+r_delta, E=11^*, and ||r_delta||=o(alpha_delta^2) on the finite block.
- P=I-n^{-1}11^* is the orthogonal projection onto 1^perp, n is the block size, and the e=1/sqrt(n) vacuum direction has strictly positive leading eigenvalue n.

## Equations

- same-theory Schur preimage: `q_\delta=\widehat N_\delta\oslash\widehat B_\delta,\qquad q_\delta\ge 0`. Valid when: The boundary anomaly is multiplicative with nonzero entries and all allowed one-body factors have been locked as same-theory diagonal congruences.
- boundary OPE quotient expansion: `q_\delta=E+\alpha_\delta H+\alpha_\delta^2K+r_\delta,\qquad E={\bf 1}{\bf 1}^*,\qquad \|r_\delta\|=o(\alpha_\delta^2)`. Valid when: The reflected Wilson collar OPE has a uniform finite-matrix expansion through second order in the chosen collar scale.
- first tangent gate: `P H P\ge 0\quad\text{on }{\bf 1}^{\perp}`. Valid when: q_delta is positive semidefinite for all sufficiently small collars.
- second Schur gate: `\langle x,PKPx\rangle-n^{-2}\,|\langle {\bf 1},H x\rangle|^2\ge 0\quad\text{for all }x\in\ker(PHP)`. Valid when: The first tangent gate is semidefinite and the rank-one vacuum direction is eliminated by the Schur complement.

## Attempted Derivation

- Lock a finite positive-time Wilson collar family and use the previously valid closed-cone argument to obtain collar-limit positivity for N_delta.
- After diagonal trace continuity removes positive additive contacts, encode the remaining reflected-boundary multiplicative anomaly by widehat B_delta and test the intended target matrix q_delta=widehat N_delta oslash widehat B_delta.
- Assume a uniform boundary OPE quotient expansion q_delta=E+alpha H+alpha^2K+o(alpha^2), E=11^*.
- Decompose C^n=Ce plus e^perp with e=1/sqrt(n)1. The e-block of E is n, so it remains invertible for small alpha.
- Compute the Schur complement on e^perp: S_delta=alpha PHP+alpha^2(PKP-(1/n)PHee^*HP)+o(alpha^2)=alpha PHP+alpha^2(PKP-n^{-2}PH11^*HP)+o(alpha^2).
- Since q_delta>=0 iff the e-block is positive and S_delta>=0, a negative first-order zero-sum form or a negative corrected second-order form on ker(PHP) gives a valid finite falsifier.
- Check the pure one-body case q_delta=v_delta v_delta^*: PHP=0 and PKP-n^{-2}PH11^*HP vanishes on 1^perp, confirming that the detector ignores harmless diagonal congruences.

Blocking gap: The finite Schur-complement calculation is valid, but Yang-Mills input must still prove the uniform reflected Wilson boundary OPE expansion and identify H,K for the locked observable core.

## Falsifiers

- falsifier: a locked Wilson block with a zero-sum vector x satisfying x^*PHPx<0; this breaks OS positivity at first boundary-OPE order.
- falsifier: PHP>=0 but some x in ker(PHP) has x^*[PKP-n^{-2}PH11^*HP]x<0; this is the corrected second-order mixed boundary obstruction.
- falsifier: collar remainders contain uncontrolled alpha^2 log alpha or cutoff/collar cross-terms, so the stated tangent expansion is not valid for the RG topology.
- falsifier: widehat B_delta has zeros or requires a pair-dependent boundary counterterm; then the Schur preimage is not a same-theory operation.
- falsifier: the locked gauge-invariant Wilson core is not stable under the reflected boundary OPE, so the matrix being tested belongs to a different theory.

## Learning

Cycle 224 sharpened the Wilson obstruction into a normalization-safe tangent-cone theorem. The valid finite test is Schur-complement positivity of q_delta near the rank-one vacuum matrix, not PKP alone. Pure one-body Wilson renormalizations cancel exactly, so a negative corrected K-form is a genuine mixed boundary falsifier. The remaining Yang-Mills work is now a concrete H,K boundary OPE computation with uniform remainders.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute H and the corrected K for a three- or four-hairpin Wilson block in the Gaussian/perturbative small-loop model, using zero-sum vectors to test PHP and the Schur-corrected second-order form before attempting the full nonabelian estimate.
