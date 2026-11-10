# cycle-0209

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: Wilson boundary Schur-preimage test

## Candidate Lemma

For a locked finite Wilson OS block with additive boundary contacts removed, same-theory OS positivity at the reflection plane is exactly positivity of the normalized Schur quotient q=\widehat N\oslash\widehat B. If the quotient is realized by a continuous Hadamard collar semigroup, then this finite test is certified by a Hermitian conditionally positive logarithm.

## Definitions

- source object: finite families F_i^\delta of gauge-invariant Wilson/hairpin observables in t>\delta, their regulated reflected OS matrices N^\delta_{ij}=S(\Theta F_i^\delta,F_j^\delta), and the multiplicative boundary Gram anomaly B from collar collapse.
- target object: the continuum OS matrix M_{ij}=S(\Theta F_i,F_j) for the same locked Wilson observables at the reflection plane, hence the physical OS pre-Hilbert form after null-vector quotient.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions through finite reflected Wilson quadratic forms, collar trace limits, and q=\widehat N\oslash\widehat B.
- same-theory condition: observable labels, diagonal Wilson renormalizations, loop/smearing classes, and reflection action are fixed before and after collar removal; dividing by B is valid only when B is an internal trace factor, not a new boundary field or counterterm.

## Assumptions

- Fixed-collar reflection positivity and RG convergence give N^\delta\to N with N\ge0 for every finite locked Wilson family.
- Diagonal trace continuity holds and any positive additive boundary contact has zero diagonal, hence vanishes on the block.
- On the nonzero support graph of B, the collar OPE factorizes as \widehat N=\widehat B\circ\widehat M with B_{ii}=N_{ii}=M_{ii}=1 after normalization.
- Optional semigroup certificate: realized collar refinements provide q_t with q_0=1, q_{s+t}=q_s\circ q_t, q_t=q_t^*, and q_t continuous for 0\le s,t,s+t\le1.

## Equations

- collar limit positivity: `N_{ij}=\lim_{\delta\downarrow0}S(\Theta F_i^\delta,F_j^\delta),\qquad N\ge0`. Valid when: The RG cutoff-removal topology is valid for every reflected finite Wilson probe at fixed positive collar.
- same-theory Schur preimage: `\widehat M_{ij}=q_{ij}:=\widehat N_{ij}/\widehat B_{ij},\qquad M\ge0\Longleftrightarrow q\ge0`. Valid when: B_{ij}\ne0 on the tested block, target diagonals are positive, and additive contacts have been eliminated without changing the theory.
- three-hairpin determinant falsifier: `\det q=1+2\operatorname{Re}(q_{12}q_{23}\overline{q_{13}})-|q_{12}|^2-|q_{23}|^2-|q_{13}|^2\ge0`. Valid when: q is a normalized Hermitian 3 by 3 quotient matrix; violation is a finite OS falsifier.
- log-CPD semigroup certificate: `q_t=e^{t\ell},\qquad \sum_{i,j}\overline c_i c_j\ell_{ij}\ge0\quad\text{whenever }\sum_i c_i=0`. Valid when: A continuous Hadamard collar semigroup exists with a Hermitian logarithm \ell; by Schoenberg this is valid and sufficient for q_t\ge0 for all t\ge0.

## Attempted Derivation

- Fix a finite locked Wilson family and move each observable to a positive collar. Regulated reflection positivity gives N^\delta\ge0.
- Use the RG topology to pass to N=\lim_{\delta\downarrow0}N^\delta, so N\ge0 by closedness of the positive matrix cone.
- Write the boundary OPE as N=B\circ M+A. Diagonal trace continuity gives A_{ii}=0; if A is a positive additive contact, Cauchy-Schwarz gives A=0.
- Normalize diagonals. Then same-theory positivity of M is equivalent to q=\widehat N\oslash\widehat B being positive semidefinite on every finite realized block.
- For triples, this gives the explicit determinant test 1+2Re(q12 q23 conjugate(q13))-|q12|^2-|q23|^2-|q13|^2>=0, which detects phase and modulus defects missed by pairwise damping.
- If collar refinements produce q_{s+t}=q_s\circ q_t, scalar continuity gives q_tij=exp(t ell_ij). Positivity of q_t and the zero-sum condition on c imply 0<=sum cbar_i c_j q_tij=t sum cbar_i c_j ell_ij+o(t), hence ell is CPD.
- Conversely, Hermitian CPD ell gives exp(t ell)>=0 by Schoenberg, so the quotient obstruction is removed on that block.

Blocking gap: The Yang-Mills analysis has not proved the required boundary OPE with A=0, nonzero controllable B, and either direct q>=0 or a continuous Hadamard semigroup for Wilson collar quotients. Non-Abelian path ordering and connected fields spanning adjacent collar layers may break the semigroup.

## Falsifiers

- falsifier: a three-hairpin Wilson block with det(\widehat N\oslash\widehat B)<0, even though all two-by-two minors are nonnegative.
- falsifier: under a valid collar semigroup, a zero-sum vector c with \sum\overline c_i c_j\ell_{ij}<0 for the logarithmic quotient kernel.
- falsifier: B_{ij}=0 while N_{ij}\ne0, making the Schur preimage singular rather than merely indefinite.
- falsifier: the collar quotient fails q_{s+t}=q_s\circ q_t because connected Yang-Mills boundary fields couple the two subcollars.
- falsifier: additive contact removal requires a boundary counterterm or Wilson renormalization not present in the locked same-theory algebra.
- falsifier: the RG compactness topology is not valid for reflected Wilson products as collars collapse to the reflection plane.

## Learning

Cycle 209 corrects the role of log-CPD. The exact same-theory obstruction is finite positivity of q=\widehat N\oslash\widehat B; log-CPD is not automatically necessary for one realized block. It becomes necessary and sufficient only when Wilson collar quotients form a continuous Hadamard semigroup, i.e. an infinite-divisibility structure. The next real work is therefore a boundary OPE calculation that either proves q>=0 on the locked Wilson core or produces a determinant/log-quadratic falsifier.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the leading boundary OPE for three mirror-smooth rectangular Wilson hairpins sharing a reflection-plane footprint. Extract \widehat N, \widehat B, q=\widehat N\oslash\widehat B, evaluate the 3 by 3 determinant, and test whether splitting the collar gives q_{s+t}=q_s\circ q_t.
