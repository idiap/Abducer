# cycle-0221

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Wilson quotient tangent-cone test for OS positivity

## Candidate Lemma

Finite Wilson collar quotient blocks near the rank-one matrix have a valid second-order OS tangent-cone test. If q_eta=E+eta H+eta^2 K+o(eta^2), E=11^*, is the same-theory quotient OS matrix, then q_eta>=0 for all small eta>0 forces PHP>=0 on 1^perp and, on ker(PHP), the Schur-corrected form PKP-n^{-2}PH11^*HP is nonnegative. A negative value is a finite Wilson falsifier.

## Definitions

- source object: finite collar OS blocks N_delta for locked gauge-invariant Wilson observables, a multiplicative boundary Gram block B_delta, and their diagonal normalizations.
- target object: OS-positive continuum Schwinger matrices for the unmodified Wilson observables at the reflection plane, encoded by q_delta=\widehat N_delta\oslash\widehat B_delta.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, reduced after collar passage to finite Schur-preimage positivity of q_delta.
- same-theory condition: B_delta may remove only collar artifacts already contained in the locked Wilson renormalization; no new boundary counterterm, algebra enlargement, or pair-dependent observable redefinition is allowed.

## Assumptions

- The additive boundary contact has already been eliminated or proved zero on the diagonal-positive OS block.
- Diagonal entries of N_delta and B_delta are positive and B_delta has no zero entries on the finite block.
- There is an asymptotic scale eta(delta)->0 such that q_eta=E+eta H+eta^2 K+o(eta^2) in operator norm.
- The all-ones convention E=11^* is used; P=I-E/n projects to 1^perp.

## Equations

- same-theory quotient: `q_\delta=\widehat N_\delta\oslash\widehat B_\delta,\qquad \widehat N_{ij}=N_{ij}(N_{ii}N_{jj})^{-1/2}`. Valid when: The boundary anomaly is multiplicative and the diagonal normalization is part of the locked observable convention.
- rank-one boundary expansion: `q_\eta=E+\eta H+\eta^2K+o(\eta^2),\qquad E=\mathbf 1\mathbf 1^*`. Valid when: The reflected Wilson boundary OPE has a two-term finite-block asymptotic in the cutoff-removal topology.
- first tangent gate: `P H P\ge 0\quad \text{on }\mathbf 1^\perp`. Valid when: q_eta is positive semidefinite for all sufficiently small eta>0.
- second tangent gate: `R\left(PKP-n^{-2}PH\mathbf 1\mathbf 1^*HP\right)R\ge0`. Valid when: R is the orthogonal projection onto ker(PHP) inside 1^perp; equivalently, with e=n^{-1/2}1, the correction is n^{-1}PHee^*HP.

## Attempted Derivation

- Lock a finite Wilson collar family F_i^delta and form the continuum collar OS matrix N_delta, which is positive by the closed-cone argument.
- Separate the multiplicative reflected-boundary hairpin factor B_delta from N_delta; the intended same-theory OS matrix is q_delta=hat N_delta oslash hat B_delta.
- Assume a boundary OPE scale eta(delta) with q_eta=E+eta H+eta^2K+o(eta^2), E=11^*.
- Decompose C^n=span{1} direct-sum 1^perp and use P=I-E/n.
- The scalar rank-one block is 1^*q_eta1=n^2+O(eta), hence positive for small eta.
- The Schur complement on 1^perp is S_eta=eta PHP+eta^2(PKP-n^{-2}PH11^*HP)+o(eta^2).
- Therefore any negative vector for PHP, or any negative Schur-corrected second-order vector in ker(PHP), gives a negative principal determinant for q_eta at small eta.

Blocking gap: The finite-matrix tangent lemma is valid, but Yang-Mills still has to supply the boundary OPE expansion and compute H,K for locked reflected Wilson hairpins.

## Falsifiers

- falsifier: a locked finite Wilson block with y in 1^perp and y^*Hy<0 produces an immediate negative OS determinant.
- falsifier: if PHP has a null vector y and y^*(PKP-n^{-2}PH11^*HP)y<0, second-order collar collapse breaks same-theory positivity.
- falsifier: a nonmultiplicative or indefinite additive boundary contact invalidates q_delta=hat N_delta oslash hat B_delta as the target OS matrix.
- falsifier: the required boundary OPE exists only after adding a reflection-plane counterterm or changing Wilson-loop renormalization.
- falsifier: RG convergence is valid for separated collars but too weak to control the finite reflected boundary quotient expansion.

## Learning

Cycle 221 corrected the tangent-cone bridge into a precise finite-matrix statement. With the all-ones normalization E=11^*, the second-order correction is n^{-2}PH11^*HP, equivalently n^{-1}PHee^*HP for the unit constant vector e. This makes the falsifier valid and normalization-safe: one-body Wilson renormalizations vanish on 1^perp, while genuine mixed boundary OPE data survive as H and the Schur-corrected K.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Work out a three-hairpin reflected Wilson boundary OPE ansatz, extract H and K after diagonal normalization, and test the zero-sum vector (1,-1,0) and a triangle null vector for the Schur-corrected second-order form.
