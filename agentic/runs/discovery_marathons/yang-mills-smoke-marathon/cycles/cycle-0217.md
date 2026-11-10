# cycle-0217

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: Wilson boundary tangent cone

## Candidate Lemma

For a finite locked Wilson collar family whose same-theory normalized OS matrix is q_eta=\widehat N_eta\oslash\widehat B_eta and q_eta=J+eta H+eta^2G+o(eta^2) near the rank-one matrix J, OS positivity forces PHP>=0 on 1^perp. If PHP has null space K, the next valid obstruction is C|_K>=0 with C=PGP-(1/m)PHee^*HP. A vector u in K with u^*Cu<0 is a finite same-theory falsifier.

## Definitions

- source object: regulated reflection-positive cutoff/collar Schwinger matrices N^{a,L,delta}_{ij}=S_{a,L}(Theta W_i^delta,W_j^delta) for locked gauge-invariant Wilson observables.
- target object: continuum Schwinger functional S on the same Wilson/local observable algebra whose finite reflected matrices are OS-positive after collar removal.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, with convergence valid for each finite reflected matrix entry and for the collar trace asymptotics.
- same-theory condition: plane-touching Wilson observables are obtained by the no-new-boundary-counterterm collar trace in the locked renormalized algebra; only prelocked diagonal congruences may be ignored.
- J is the m by m all-ones matrix, e=m^{-1/2}(1,...,1), and P=I-ee^* projects onto 1^perp.
- \widehat B is the normalized multiplicative boundary Gram/anomaly factor and \widehat N is the normalized positive collar-limit matrix.

## Assumptions

- Fixed-collar cutoff removal is valid: every finite reflected Wilson matrix entry converges in the RG topology.
- Additive boundary contacts have vanished by diagonal trace continuity and positivity, so the remaining defect is multiplicative.
- All entries of \widehat B_eta are nonzero for small eta, so Hadamard division is defined.
- The quotient q_eta=\widehat N_eta\oslash\widehat B_eta has a Hermitian second-order expansion uniform on the chosen finite Wilson family.
- The finite family is realized inside the locked gauge-invariant algebra, not enlarged by boundary states.

## Equations

- exact Schur-preimage condition: `\widehat N_\eta=\widehat B_\eta\circ q_\eta,\qquad q_\eta=\widehat N_\eta\oslash\widehat B_\eta,\qquad q_\eta\ge 0`. Valid when: The boundary defect is purely multiplicative and the intended same-theory OS matrix is obtained by dividing out that defect entrywise.
- rank-one expansion: `q_\eta=J+\eta H+\eta^2G+o(\eta^2),\qquad J=\mathbf 1\mathbf 1^*,\quad H=H^*,\quad G=G^*`. Valid when: The Wilson collar family approaches a common reflection-plane observable and the boundary OPE has a second-order finite-matrix asymptotic.
- Schur complement at J: `S_\eta=\eta PHP+\eta^2\left(PGP-\frac{1}{m}PHee^*HP\right)+o(\eta^2)`. Valid when: Block-decompose q_eta relative to span{e}\oplus 1^perp; the e-block stays positive, equal to m+O(eta).
- first and second tangent gates: `PHP\ge 0,\qquad u^*\left(PGP-\frac{1}{m}PHee^*HP\right)u\ge0\quad (u\in\ker(PHP))`. Valid when: q_eta is positive semidefinite for all sufficiently small eta>0.
- second-order falsifier: `u\in 1^\perp,\quad u^*PHPu=0,\quad u^*Cu<0\ \Longrightarrow\ q_\eta\not\ge0\text{ for small }\eta`. Valid when: C=PGP-(1/m)PHee^*HP and the remainder is o(eta^2) on the finite block.

## Attempted Derivation

- Start with regulated reflection positivity: each fixed collar gives N^{a,L,delta}>=0 for reflected Wilson test families.
- Use the RG-to-OS convergence topology to pass fixed-collar positivity to the continuum collar matrix N_delta and then to the collar limit \widehat N_eta, assuming the trace limit is valid.
- After additive contacts vanish, write the collar-limit matrix as \widehat N_eta=\widehat B_eta\circ q_eta, where q_eta is the intended same-theory OS matrix.
- Normalize diagonals and impose the rank-one boundary expansion q_eta=J+eta H+eta^2G+o(eta^2).
- Decompose C^m=span{e}\oplus1^perp. Since the e-block is m+O(eta)>0, q_eta>=0 is equivalent to positivity of its Schur complement on 1^perp.
- Expanding the Schur complement gives S_eta=eta PHP+eta^2(PGP-(1/m)PHee^*HP)+o(eta^2).
- Therefore PHP>=0 is necessary. On null directions of PHP the order-eta term vanishes, so the displayed C-form is the next necessary obstruction; if it is negative, q_eta has a negative vector for small eta.

Blocking gap: The finite-dimensional PSD calculus is clear; the missing Yang-Mills input is a controlled reflected Wilson boundary OPE giving H,G and an o(eta^2) remainder for the locked observable algebra.

## Falsifiers

- falsifier: a realized Wilson triple or quadruple with PHP>=0 but a vector u in ker(PHP) satisfying u^*Cu<0.
- falsifier: failure of nonzero entrywise boundary factors, making q=\widehat N\oslash\widehat B ill-defined for the intended Wilson block.
- falsifier: a surviving additive contact with zero diagonal, contradicting the positive-contact vanishing argument and invalidating the multiplicative reduction.
- falsifier: the cutoff-removal topology gives fixed-collar convergence but no valid second-order reflected collar expansion.
- falsifier: the needed null vector exists only after enlarging the Wilson algebra by boundary states, so the calculation is not same-theory.

## Learning

Cycle 217 identifies the next valid obstruction after the first-order kernel test. Near the rank-one quotient J, OS positivity is governed by the PSD tangent cone: first PHP>=0 on 1^perp, then a Schur-complement second-order form on ker(PHP). This is sharper than saying nonrank-one anomaly; it gives a computable finite falsifier from Wilson boundary OPE data.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute H and G for a minimal three- or four-hairpin reflected Wilson collar family with coincident boundary footprint; search first for ker(PHP), then evaluate C=PGP-(1/m)PHee^*HP on that kernel.
