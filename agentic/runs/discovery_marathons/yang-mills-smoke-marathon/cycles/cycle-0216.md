# cycle-0216

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

For finite locked Wilson collars with q_delta=Nhat_delta oslash Bhat_delta=J+epsilon_delta H+epsilon_delta^2 R+o(epsilon_delta^2), valid same-theory OS positivity forces PHP>=0 on 1^perp. If K=ker(PHP), it also forces the second Schur form C_K>=0. Either negative form is a falsifier.

## Definitions

- source object: finite locked Wilson collar OS blocks N_delta and boundary anomaly blocks B_delta with positive diagonals, after cutoff removal in the RG topology.
- target object: OS-positive same-theory continuum block M_delta=Nhat_delta oslash Bhat_delta and its boundary limit as collars collapse.
- controlled interface: normalized Schur preimage q_delta=Nhat_delta oslash Bhat_delta; only finite reflected Wilson matrices are transported.
- same-theory condition: Wilson-loop renormalization and test algebra are locked before the collar limit; no new boundary counterterm, quotient, or observable relabeling is allowed.

## Assumptions

- N_delta is the closed-cone collar limit of regulated reflection-positive blocks; B_delta records only Wilson boundary OPE factors.
- q_delta has a Hermitian two-term expansion for a fixed finite Wilson family, with epsilon_delta>0 and o(epsilon_delta^2) in operator norm.
- Diagonal normalization removes harmless locked one-body congruences: q_{ii}=1+o(epsilon_delta^2).
- The same finite family is realized in the gauge-invariant test algebra before and after cutoff removal.

## Equations

- normalized quotient expansion: `q_\delta=\widehat N_\delta\oslash\widehat B_\delta=J+\varepsilon_\delta H+\varepsilon_\delta^2R+o(\varepsilon_\delta^2),\quad J={\bf1}{\bf1}^*`. Valid when: valid when the reflected Wilson boundary OPE has a uniform two-term mixed-matrix expansion.
- first tangent positivity: `P H P\succeq0\text{ on }{\bf1}^{\perp},\quad P=I-\frac1n{\bf1}{\bf1}^*`. Valid when: valid for any q_delta positive semidefinite for arbitrarily small positive epsilon_delta.
- degenerate second Schur test: `C_K=P_K\left(PRP-\frac1n(e^*HP)^*(e^*HP)\right)P_K\succeq0,\quad e=n^{-1/2}{\bf1}`. Valid when: valid when K=ker(PHP|_{1^perp}); it is the second-order Schur complement after eliminating the J direction.

## Attempted Derivation

- Normalize N_delta and B_delta by their diagonals; the same-theory target block is q_delta=Nhat_delta oslash Bhat_delta, so OS positivity is q_delta>=0 on each realized finite Wilson family.
- Decompose C^n=C1 plus 1^perp. Since J vanishes on 1^perp, testing z in 1^perp gives z^*Hz>=0 as the first nonzero term.
- Take the Schur complement against the positive J eigenline. It equals epsilon_delta PHP+epsilon_delta^2(PRP-(e^*HP)^*(e^*HP)/n)+o(epsilon_delta^2).
- On K=ker(PHP), the first term vanishes; a negative second Schur form yields a negative eigenvalue for small collars.

Blocking gap: No Yang-Mills estimate yet computes H and R from the reflected Wilson boundary OPE for mixed hairpin products.

## Falsifiers

- A boundary OPE calculation finds z in 1^perp with z^*Hz<0; this first-order falsifier breaks same-theory OS positivity.
- PHP>=0 but some z in K has z^*C_Kz<0; pairwise first-order tests pass while a small-collar determinant becomes negative.
- Mixed Wilson products lack an operator-norm two-term expansion, so the tangent bridge is not valid for the cutoff-removal topology.
- B_delta has zero or oscillatory entries, or forces new Wilson renormalization at t=0; then q=N/B is not the same theory.

## Learning

Cycle 216 learned that H>=0 on 1^perp is only the first gate. If H has null directions, the valid next obstruction is a Schur-complement second-order boundary OPE form. This gives a sharper falsifier than generic nonrank-one anomaly language.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute H and C_K for three reflected Wilson hairpins sharing one boundary footprint; test zero-sum and kernel vectors before invoking any log-CND semigroup.
