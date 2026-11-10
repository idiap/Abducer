# cycle-0213

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

For a finite locked Wilson collar block, if the normalized same-theory quotient q_delta=Nhat_delta oslash Bhat_delta has expansion J+eps_delta H+o(eps_delta), then OS positivity of the intended limit forces H to be positive on the zero-sum subspace. A negative zero-sum form is a valid falsifier.

## Definitions

- source object: fixed-collar reflected Wilson OS matrices N_delta obtained from regulated reflection-positive Schwinger forms after RG convergence.
- target object: continuum OS-positive Schwinger functions on the locked gauge-invariant Wilson algebra, with no boundary counterterm or algebra change.
- controlled interface: quotient Schur preimage q_delta=Nhat_delta oslash Bhat_delta after diagonal normalization and removal of positive additive contacts.
- same-theory condition: B_delta is only the collar-collapse boundary factor already present in the locked Wilson renormalization; q_delta, not a modified algebra, must be PSD.

## Assumptions

- Fixed-collar OS matrices N_delta are PSD and converge entrywise for every finite reflected Wilson family.
- Bhat_delta has nonzero entries and unit diagonal after the allowed diagonal congruence normalization.
- The boundary OPE gives q_delta=J+eps_delta H+o(eps_delta) uniformly on the chosen finite block, with eps_delta>0.
- The same Wilson observables label N_delta, B_delta, and the target block; no new boundary observable is inserted.

## Equations

- exact same-theory quotient: `M_\delta=\widehat N_\delta\oslash \widehat B_\delta=:q_\delta`. Valid when: Multiplicative boundary factors are isolated and no entry of Bhat_delta vanishes.
- tangent expansion: `q_\delta=\mathbf 1\mathbf 1^*+\varepsilon_\delta H+o(\varepsilon_\delta)`. Valid when: The reflected Wilson boundary OPE has a uniform leading quotient kernel on the finite block.
- zero-sum obstruction: `\sum_i c_i=0,\quad c^*Hc<0\ \Longrightarrow\ c^*q_\delta c<0\text{ for small }\delta`. Valid when: epsilon_delta is positive and the o(epsilon_delta) remainder is uniform for that vector c.

## Attempted Derivation

- Start with fixed-collar reflection positivity: N_delta>=0. The intended target is not N_delta if collar collapse contributes Bhat_delta; it is the Schur preimage q_delta=Nhat_delta oslash Bhat_delta.
- Normalize diagonals to one. At exact collision the quotient base is J=11*, whose nullspace is the zero-sum subspace.
- Insert the boundary OPE q_delta=J+eps_delta H+o(eps_delta). For any c with sum c_i=0, the J term vanishes, so c*q_delta c=eps_delta c*Hc+o(eps_delta).
- If c*Hc<0, q_delta has a negative quadratic form for small delta; hence the same-theory OS block is indefinite although the collar block N_delta was positive.

Blocking gap: No Yang-Mills computation yet identifies the leading quotient kernel H and proves the expansion is uniform for reflected Wilson hairpin triples.

## Falsifiers

- falsifier: a reflected Wilson triple has q_delta determinant negative, equivalently a zero-sum vector detects c*Hc<0 at leading OPE order.
- falsifier: Bhat_delta has zeros or nonuniform phases, so the Schur preimage is not a well-defined same-theory limit.
- falsifier: additive boundary contacts survive despite diagonal trace continuity, invalidating the quotient-only reduction.
- falsifier: proving positivity requires adding a boundary Wilson operator or changing loop renormalization, so the bridge is valid only for a different theory.

## Learning

Cycle 213 adds an infinitesimal falsifier to the exact Schur-preimage bridge. If the quotient q_delta is near the rank-one matrix J, OS positivity first lives on the zero-sum tangent space. Thus the leading boundary OPE kernel H must be positive there; a negative zero-sum form is a valid finite Wilson obstruction before invoking log-CND or semigroups.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the leading quotient kernel H for three reflected Wilson hairpins with a common boundary footprint; test c=(1,-1,0) and c=(1,1,-2) zero-sum forms.
