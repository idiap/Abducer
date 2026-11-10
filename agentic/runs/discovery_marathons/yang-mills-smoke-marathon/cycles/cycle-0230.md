# cycle-0230

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: Wilson collar Feshbach quotient test

## Candidate Lemma

For any finite reflected Wilson collar block whose same-theory boundary anomaly is multiplicative and whose normalized Schur quotient tends to the vacuum matrix, OS positivity of the intended boundary block is equivalent, up to the proven OPE order, to positivity of the recursive Feshbach reduced coefficients after removing the vacuum direction. The first negative reduced coefficient is a valid same-theory falsifier.

## Definitions

- source object: regulated reflection-positive Schwinger functionals S_{a,L} on a locked gauge-invariant positive-time test algebra, plus finite Wilson collar blocks T_delta F_i.
- target object: continuum OS quadratic forms S(Theta F_i,F_j) on the uncollared locked gauge-invariant Wilson observables.
- controlled interface: finite reflected OS matrices, diagonal normalizations, and the Schur quotient q_delta obtained by dividing out only boundary factors already present in the same theory.
- same-theory condition: collar collapse may use diagonal congruences and fixed observable embeddings only; no pair-dependent counterterm, boundary algebra enlargement, or changed Wilson renormalization is allowed.

## Assumptions

- Regulated reflection positivity holds for each collar-separated block and RG convergence is valid for every reflected matrix entry.
- The collar maps T_delta F converge to F in the locked cutoff-removal topology and preserve the gauge-invariant test algebra.
- After additive contacts are eliminated by diagonal trace continuity, the remaining boundary anomaly has the form N_delta=B_delta circ M_delta plus a uniform finite-block remainder.
- All entries of B_delta used in the quotient are nonzero and the normalized intended quotient q_delta has a Hermitian expansion q_tau=J+tau H+tau^2 K+... with tau(delta)->0.
- The recursive Feshbach reductions are computed with remainders small compared with the first nonzero reduced coefficient on each null sector.

## Equations

- collar OS matrix: `N_\delta(i,j)=S(\Theta T_\delta F_i,T_\delta F_j)\ge0`. Valid when: T_delta F_i are supported a positive distance from the reflection plane and the RG-to-OS convergence controls these reflected probes.
- same-theory quotient: `q_\delta=\widehat M_\delta=\widehat N_\delta\oslash\widehat B_\delta,\qquad N_\delta=B_\delta\circ M_\delta+o(\tau^m)`. Valid when: The boundary OPE is multiplicative on the finite block and diagonal normalization is a same-theory congruence.
- vacuum Schur complement: `q_\tau=J+\tau H+\tau^2K+O(\tau^3),\quad e=n^{-1/2}{\bf 1},\quad P=I-ee^*,\quad T_\tau=Pq_\tau P-Pq_\tau e(e^*q_\tau e)^{-1}e^*q_\tau P`. Valid when: q_tau is close to the rank-one vacuum matrix J={\bf 1}{\bf 1}^* and e^*q_tau e remains strictly positive.
- second coefficient after vacuum removal: `T_\tau=\tau PHP+\tau^2P(K-n^{-1}Hee^*H)P+O(\tau^3)`. Valid when: The expansion is C^2 in tau with uniform finite-block remainder; the correction is forced by the large rank-one OS direction.
- recursive Feshbach reduction: `\mathfrak F_\Pi(A(\tau))=\Pi A(\tau)\Pi-\Pi A(\tau)R(RA(\tau)R)^{-1}RA(\tau)\Pi`. Valid when: R projects onto the positive spectral subspace already certified and Pi projects onto its null sector.

## Attempted Derivation

- Lock a finite positive-time Wilson family F_1,...,F_n and replace it by collars T_delta F_i so the regulated reflection-positive cone gives N_delta>=0 after RG convergence.
- Assume the same-theory boundary OPE separates the collar matrix as N_delta=B_delta circ M_delta plus a small remainder, with B_delta containing only allowed boundary factors.
- Remove diagonal one-body Wilson factors by congruence and form q_delta=widehat N_delta oslash widehat B_delta; this is the intended normalized OS matrix if the same-theory condition is true.
- For hairpin-style collar collapse q_delta approaches J=11^*, so decompose C^n=C e plus e^perp and take the Schur complement of the positive vacuum direction.
- The expansion of the Schur complement gives the invariant first test PHP and the corrected second test P(K-n^{-1}Hee^*H)P; the correction cannot be omitted because the vacuum direction couples at order tau.
- If PHP has a positive gap, finite-block positivity follows by norm domination. If PHP has null directions, apply the Feshbach map recursively; the first negative reduced coefficient constructs a vector c_tau with c_tau^*q_tau c_tau<0.
- This produces a normalization-safe falsifier: one-body renormalizations cancel under P, while mixed reflected boundary OPE data survive in the reduced coefficients.

Blocking gap: The finite-dimensional Feshbach theorem is valid, but Yang-Mills still lacks the needed reflected Wilson boundary OPE with multiplicative quotient form, Hermitian coefficients H,K,..., and uniform remainders for locked gauge-invariant hairpin blocks.

## Falsifiers

- A finite reflected Wilson hairpin block has a zero-sum vector v with v^*PHP v<0; this is an immediate first-order falsifier.
- PHP is PSD, but on ker(PHP) the corrected form P(K-n^{-1}Hee^*H)P is negative.
- A higher Feshbach reduction is negative after coupling to a positive earlier sector, showing that raw PKP or PLP gave a misleading test.
- The boundary OPE contains an additive contact whose diagonal does not vanish under the same collar trace, contradicting the multiplicative quotient setup.
- The quotient B_delta requires pair-dependent Wilson renormalization or a boundary observable not in the locked algebra, so the positivity bridge proves a different theory.
- The RG cutoff-removal topology controls separated collars but gives no uniform remainder as reflected Wilson supports collide with the reflection plane.

## Learning

Cycle 230 turns the Wilson obstruction into a precise tangent-cone algorithm. The valid test is Schur complement of the vacuum direction followed by recursive Feshbach reductions on null sectors. A positive first reduced kernel promotes a finite block; the first negative reduced coefficient is a genuine mixed-boundary same-theory falsifier. The remaining work is no longer abstract reflection positivity but a concrete reflected Wilson boundary OPE with uniform remainders.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the leading H and corrected K for a three-hairpin reflected Wilson block with common boundary footprint; test PHP on 1^perp and, if null, evaluate P(K-n^{-1}Hee^*H)P on the null sector.
