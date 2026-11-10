# cycle-0219

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

If a same-theory Wilson collar quotient q_delta=J+delta H+delta^2K+o(delta^2) is OS-positive for all small collars, then PHP>=0 and the Schur-corrected second form is nonnegative on ker(PHP); either violation is a finite falsifier.

## Definitions

- source object: finite reflected Wilson collar OS blocks N_delta with regulated positivity and boundary Gram factors B_delta.
- target object: continuum same-theory OS matrix M on the locked gauge-invariant Wilson core.
- controlled interface: normalized Schur preimage q_delta=Nhat_delta oslash Bhat_delta after additive contact elimination.
- same-theory condition: no boundary counterterm, no observable enlargement, and the diagonal congruence is fixed by predeclared Wilson renormalization.

## Assumptions

- Regulated reflection positivity gives N_delta>=0 for each fixed collar.
- The RG topology is valid for all finite reflected collar probes.
- Diagonal trace continuity and positive-contact vanishing have already been proved.
- The boundary Wilson OPE supplies Hermitian H,K and a uniform o(delta^2).
- Diagonals stay positive so the Schur quotient is defined.

## Equations

- finite Schur preimage: `q_\delta=\widehat N_\delta\oslash\widehat B_\delta,\quad M_\delta=D_\delta q_\delta D_\delta^*`. Valid when: Additive boundary contacts vanish and B_delta is the multiplicative boundary Gram factor for the same locked Wilson block.
- rank-one collar expansion: `q_\delta=J+\delta H+\delta^2K+o(\delta^2),\quad J=\mathbf1\mathbf1^*,\quad P=I-J/n,\quad u=n^{-1/2}\mathbf1`. Valid when: The reflected Wilson boundary OPE has a C^2 collar expansion uniform for the finite block.
- second-order tangent gates: `PHP\ge0,\quad x^*(PKP-n^{-1}PHuu^*HP)x\ge0\ \forall x\in\ker(PHP)`. Valid when: Necessary for q_delta>=0 for all small delta; a negative value is a valid finite Wilson falsifier.

## Attempted Derivation

- Normalize by positive diagonals; collar closed-cone passage gives N>=0, but target positivity is q=Nhat oslash Bhat>=0, not positivity of N alone.
- At delta=0, q0=J has one eigenvalue n and nullspace 1^perp. Let P project to 1^perp and u=n^{-1/2}1.
- Use the Schur complement of the u-block: q_delta>=0 implies S_delta=PqP-Pqu(u*qu)^{-1}u*qP>=0 on 1^perp.
- Expanding S_delta gives delta PHP+delta^2(PKP-n^{-1}PHu u^*HP)+o(delta^2); negativity on 1^perp or ker(PHP) gives a finite determinant falsifier.

Blocking gap: The Yang-Mills boundary OPE coefficients H,K and a uniform o(delta^2) for reflected Wilson hairpin products in the locked algebra are not yet known.

## Falsifiers

- First-order falsifier: a zero-sum vector x with x^*PHPx<0 in a realized Wilson block.
- Second-order falsifier: x in ker(PHP) with x^*(PKP-n^{-1}PHu u^*HP)x<0.
- Expansion falsifier: the boundary OPE contains delta^2 log(delta) or a nonuniform remainder, so the tangent lemma is not valid.
- Same-theory falsifier: diagonal/contact renormalization changes the Wilson core, so q_delta no longer represents the intended OS matrix.

## Learning

Cycle 219 upgrades the OS quotient obstruction from first-order PHP to the correct second-order tangent cone. The rank-one OS direction is not passive; eliminating it subtracts n^{-1}PHu u^*HP. The next valid falsifier is a boundary OPE computation of H,K for a finite Wilson block.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute H and K for a minimal three-hairpin reflected Wilson block sharing one boundary footprint; test PHP and the Schur-corrected form on ker(PHP).
