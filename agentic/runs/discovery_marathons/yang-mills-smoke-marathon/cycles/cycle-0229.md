# cycle-0229

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

For a finite locked Wilson collar block, same-theory OS positivity after collar collapse is finite PSD of the Schur quotient. Near the vacuum rank-one matrix, the first negative vacuum-Feshbach reduced coefficient is a normalization-safe falsifier.

## Definitions

- source object: finite reflected Wilson collar OS matrices N_delta from regulated reflection-positive lattice/RG Schwinger forms, with boundary anomaly matrices B_delta and collar scale delta>0.
- target object: continuum OS quadratic form on the same finite Wilson observables at the reflection plane.
- controlled interface: q_delta=hat N_delta oslash hat B_delta finite matrix PSD tests after diagonal normalization and removal of proven additive contacts.
- same-theory condition: B_delta records only collar renormalization of locked observables; no boundary operator, quotient gauge algebra, or Wilson renormalization convention is changed.

## Assumptions

- Regulated reflection positivity and RG convergence give N_delta>=0 for each fixed collar and convergence of all finite reflected entries.
- B_delta has no zero entries and positive diagonal; diagonal trace continuity has removed positive additive contacts.
- After diagonal normalization, q_delta=J+epsilon H+epsilon^2 K+O(epsilon^3) in operator norm, with H,K Hermitian and e=n^{-1/2}1.
- The O(epsilon^3) remainder is uniform for the locked finite Wilson block.

## Equations

- exact quotient criterion: `M_\delta=B_\delta^{[-1]}\circ N_\delta,\qquad M_\delta\ge0`. Valid when: valid when collar collapse is purely multiplicative and B has no zero entries; this is the exact finite same-theory OS test.
- vacuum expansion: `q_\delta=J+\varepsilon H+\varepsilon^2K+O(\varepsilon^3),\quad J={\bf1}{\bf1}^*=n ee^*,\quad P=I-ee^*`. Valid when: valid after diagonal/one-body normalization and a uniform Wilson boundary OPE in collar scale epsilon.
- second Feshbach gate: `A_1=PHP,\qquad A_2=\Pi_1P(K-n^{-1}Hee^*H)P\Pi_1,\quad \Pi_1=\operatorname{pr}_{\ker A_1}`. Valid when: valid if A1 is PSD and has a spectral gap off its kernel; a negative A1 or A2 gives a finite Wilson falsifier.

## Attempted Derivation

- For fixed collar, regulated positivity plus RG convergence puts each finite reflected Wilson matrix N_delta in the closed PSD cone.
- If additive contacts vanish, collar collapse factors as N_delta=B_delta circ M_delta; hence the intended same-theory matrix is M_delta=B_delta^{[-1]} circ N_delta.
- After diagonal normalization q_delta tends to J. Splitting C^n=Ce plus e^perp, the Schur complement of the vacuum eigenvalue n gives epsilon PHP plus the second-order correction.
- Thus negative PHP on e^perp, or negative corrected A2 on ker(PHP), is a valid finite obstruction; positive reduced coefficients with gaps promote the block.

Blocking gap: No Yang-Mills proof yet gives the uniform reflected Wilson hairpin boundary OPE producing H,K and remainders for the locked gauge-invariant algebra.

## Falsifiers

- falsifier: a computed hairpin block has v^*Hv<0 for some v perpendicular to 1.
- falsifier: PHP>=0 but v^*A2v<0 on ker(PHP), with the -n^{-1}Hee^*H correction included.
- falsifier: q_delta has a negative 3 by 3 determinant although every pairwise damping inequality holds.
- falsifier: collar collapse requires a boundary counterterm or altered Wilson renormalization not encoded in B_delta.

## Learning

Cycle 229 makes the obstruction an exact finite quotient problem near the vacuum matrix. The valid test is not B alone, nor pairwise damping, nor raw PKP. Remove the rank-one OS direction, then use Feshbach reductions; the first negative reduced coefficient is the genuine same-theory falsifier.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the epsilon and epsilon^2 boundary OPE coefficients for three mirror Wilson hairpins with common footprint, normalize q_delta, and test PHP plus the corrected A2.
