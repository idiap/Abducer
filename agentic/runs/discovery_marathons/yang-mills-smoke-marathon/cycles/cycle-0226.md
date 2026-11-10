# cycle-0226

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Uniform rank-one tangent-cone lemma: PSD of the same-theory Wilson quotient q_delta forces PHP>=0 and S>=0 on ker(PHP); conversely, quantitative gaps plus uniform remainder make q_delta PSD. A negative S-vector is a valid falsifier.

## Definitions

- source object: finite locked reflected Wilson collar OS matrices N_delta with boundary Gram anomaly B_delta and diagonal normalization fixed before cutoff removal.
- target object: continuum OS-positive Schwinger matrix for the same Wilson observables after removing the collar and anomaly quotient.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions through q_delta=Nhat_delta oslash Bhat_delta.
- same-theory condition: the quotient uses only prelocked Wilson renormalizations; no boundary counterterm, algebra enlargement, or pair-dependent redefinition is allowed.

## Assumptions

- q_delta is Hermitian and has a finite-block expansion in operator norm with uniform cutoff/collar remainder.
- e=n^{-1/2}(1,...,1), P=I-ee^*, and q_delta is PSD for every small delta if the OS bridge is valid.
- Additive positive contacts have been eliminated by diagonal trace continuity; H,K record mixed boundary OPE data.

## Equations

- Wilson quotient expansion: `q_\delta=\widehat N_\delta\oslash \widehat B_\delta=\mathbf 1\mathbf 1^*+\delta H+\delta^2K+R_\delta,\quad \|PR_\delta P\|=o(\delta^2)`. Valid when: valid after nonzero boundary Gram entries, diagonal normalization, and uniform finite-block collar expansion.
- rank-one Schur complement: `\operatorname{Sc}(q_\delta)=Pq_\delta P-(Pq_\delta e)(e^*q_\delta e)^{-1}(e^*q_\delta P)=\delta PHP+\delta^2P(K-n^{-1}Hee^*H)P+o(\delta^2)`. Valid when: valid because e^*q_delta e=n+O(delta), so the vacuum rank-one direction can be eliminated.
- second-order obstruction: `q_\delta\ge0\Rightarrow PHP\ge0,\quad x\in\ker(PHP)\Rightarrow \langle x,P(K-n^{-1}Hee^*H)Px\rangle\ge0`. Valid when: valid for every fixed Wilson block with the expansion above and OS positivity for all sufficiently small collars.

## Attempted Derivation

- Normalize collar OS data by q_delta=Nhat_delta oslash Bhat_delta so the vacuum limit is 11^* rather than an arbitrary diagonal congruence.
- Decompose C^n=Ce⊕e^perp. Since the e-block is n+O(delta), PSD of q_delta is equivalent to PSD of its Schur complement for small delta.
- Expanding the Schur complement gives delta PHP plus delta^2 P(K-n^{-1}Hee^*H)P. Thus PHP is the first zero-sum gate.
- On ker(PHP), the first term vanishes, so the corrected K-form is the next valid obstruction; a negative value yields a finite Wilson falsifier.

Blocking gap: The finite-matrix argument is conditional on a uniform second-order boundary OPE for locked Wilson collars in the actual cutoff-removal topology.

## Falsifiers

- falsifier: PHP has a negative zero-sum eigenvalue for a realized Wilson collar block; first-order OS positivity already fails.
- falsifier: there is x in ker(PHP) with <x,P(K-n^{-1}Hee^*H)Px><0, giving a negative small-collar determinant.
- falsifier: Bhat_delta has zeros or discontinuous phases, so the same-theory Hadamard quotient is not valid.
- falsifier: cusp or hairpin OPE terms make R_delta non-uniform, invalidating the tangent-cone passage from RG convergence to OS positivity.

## Learning

Cycle 226 made the obstruction normalization-safe and finite-dimensional: after removing the rank-one vacuum direction, the valid second-order test is S=P(K-n^{-1}Hee^*H)P on ker(PHP). One-body Wilson factors cancel; a negative S-form is a genuine mixed boundary falsifier.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the boundary OPE H,K for three mirror Wilson hairpins sharing a reflection-plane footprint, then test PHP and the corrected S-form on zero-sum vectors.
