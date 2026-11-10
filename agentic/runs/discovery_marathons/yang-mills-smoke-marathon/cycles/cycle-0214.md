# cycle-0214

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Zero-sum Wilson quotient tangent lemma: if normalized same-theory Schur preimages q_delta for reflected Wilson collars satisfy q_delta=J+lambda_delta H+o(lambda_delta), lambda_delta>0, then valid OS positivity forces H>=0 on 1^perp; a negative zero-sum form is a finite Wilson falsifier.

## Definitions

- source object: finite reflected Wilson collar OS matrices N_delta from regulated reflection-positive Schwinger forms, plus boundary multiplicative matrices B_delta after additive contacts are removed.
- target object: normalized continuum OS matrices M for the locked gauge-invariant Wilson algebra, including reflection-plane limits of collar observables.
- controlled interface: Hadamard Schur preimage q_delta=Nhat_delta oslash Bhat_delta and its rank-one tangent on the zero-sum subspace.
- same-theory condition: Wilson embeddings, diagonal renormalizations, and boundary trace map are fixed before the limit; no pair-dependent counterterm, quotient algebra, or new boundary state is inserted.

## Assumptions

- A fixed finite Wilson collar family F_i(delta) has positive diagonals; Bhat_delta has unit diagonal and no zero entry.
- Collar reflection positivity gives Nhat_delta>=0, and diagonal trace continuity has killed additive contacts.
- The same-theory plane OS block is q_delta=Nhat_delta oslash Bhat_delta, not a newly renormalized boundary algebra.
- q_delta is Hermitian and admits q_delta=J+lambda_delta H+R_delta with lambda_delta down to 0 and ||P R_delta P||=o(lambda_delta).

## Equations

- same-theory Schur preimage: `\widehat M_\delta=q_\delta:=\widehat N_\delta\oslash\widehat B_\delta,\quad (q_\delta)_{ij}=(\widehat N_\delta)_{ij}/(\widehat B_\delta)_{ij}`. Valid when: valid when B entries are nonzero and all allowed boundary renormalization is already encoded in B.
- rank-one tangent: `q_\delta=J+\lambda_\delta H+R_\delta,\quad P=I-n^{-1}J,\quad \|P R_\delta P\|=o(\lambda_\delta)`. Valid when: valid for a Wilson block whose boundary OPE has a first nontrivial quotient coefficient H.
- zero-sum obstruction: `\sum_i x_i=0\Rightarrow x^*q_\delta x=\lambda_\delta x^*Hx+o(\lambda_\delta\|x\|^2)`. Valid when: valid under the tangent expansion; x*Hx<0 makes q_delta negative for small delta.

## Attempted Derivation

- Normalize N_delta and B_delta to unit diagonal; additive contacts are excluded by diagonal trace continuity and positivity.
- The intended t=0 OS matrix is q_delta=Nhat_delta oslash Bhat_delta; closed-cone positivity of N_delta alone does not imply q_delta>=0.
- Insert q_delta=J+lambda_delta H+R_delta and project with P onto 1^perp, where J vanishes exactly.
- For x in 1^perp, a negative x*Hx dominates the o(lambda_delta) remainder, giving x*q_delta*x<0 for small delta.

Blocking gap: The Yang-Mills boundary OPE must produce H and a uniform projected remainder for the locked Wilson core, especially in the semidefinite H case.

## Falsifiers

- falsifier: a reflected hairpin OPE coefficient H with x*Hx<0 for some zero-sum x makes the intended OS block indefinite.
- falsifier: pairwise quotient tests pass but a three-Wilson determinant det(Nhat oslash Bhat)<0 due to quotient phase holonomy.
- falsifier: B_delta has zeros or uncontrolled phases, so the Hadamard preimage is not a valid same-theory matrix.
- falsifier: a residual additive contact with zero diagonal survives, contradicting positive-contact Cauchy-Schwarz and diagonal trace continuity.

## Learning

Cycle 214 learned that near rank-one Wilson quotient blocks, the first OS obstruction lives exactly on 1^perp. The leading boundary OPE coefficient H is a computable necessary test; a negative zero-sum form is a valid finite falsifier without assuming log-CND.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the leading quotient kernel H for three reflected Wilson hairpins sharing a boundary footprint; test zero-sum quadratic forms before trying log-CND.
