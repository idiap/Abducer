# cycle-0180

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: mixed Wilson boundary-defect criterion

## Candidate Lemma

Finite OS Matrix Trace-Modulus Bridge. Let S be a continuum Schwinger functional obtained as a cutoff limit of reflection-positive regulated gauge-invariant Schwinger forms. For a locked positive-time gauge-invariant algebra A_+ and collar maps T_delta moving observables into t >= delta, assume fixed-collar OS positivity and finite OS matrix trace continuity: for every finite family F_1,...,F_n in A_+, the matrices M^delta_{ij}=S(Theta T_delta F_i T_delta F_j) converge in operator norm to M^0_{ij}=S(Theta F_i F_j). Then S is OS-positive on A_+. A nonzero mixed boundary defect not removable by a pre-locked diagonal congruence is a falsifier of this bridge, because fixed-collar positivity then proves positivity of a boundary-renormalized matrix rather than of the target OS matrix.

## Definitions

- source object: regulated reflection-positive Schwinger forms S_{a,L} on a fixed gauge-invariant positive-time test algebra, together with their continuum limit S and collar approximants T_delta F inherited from the same cutoff observables.
- target object: OS-positive continuum Schwinger functions on the locked Yang-Mills gauge-invariant algebra A_+, inducing the sesquilinear form <F,G>_OS=S(Theta F G), the OS quotient Hilbert space, vacuum vector, and positive time-translation semigroup.
- controlled interface: finite reflected quadratic forms Q_S(F,c)=sum_{i,j} overline{c_i} c_j S(Theta F_i F_j) and their collar matrices M^delta, controlled in the finite OS matrix/operator-norm topology.
- same-theory condition: the observable embedding, product, reflection, and renormalization conventions are fixed before cutoff removal and before delta downarrow 0; no extra reflection-plane observable, boundary counterterm, or post hoc Wilson-loop normalization may be introduced to make the limiting positivity statement valid.

## Assumptions

- For every fixed delta>0 and every finite family F_i in A_+, RG convergence is strong enough for the reflected collar probes Theta T_delta F_i · T_delta F_j, so the closed-cone argument gives M^delta >= 0.
- The collar maps T_delta preserve the locked algebraic identification: T_delta(Theta F)=Theta T_delta(F) after reflection and T_delta(FG) approximates the same product observable, not a changed boundary theory.
- For each finite family F, omega_F(delta)=||M^delta-M^0||_op tends to 0 as delta downarrow 0.
- The Schwinger functional is already defined on the uncollared observables F_i, so M^0 is not being defined by the positive collar limit itself.

## Equations

- finite OS matrix trace modulus: `M^\delta_{ij}=S(\Theta T_\delta F_i\,T_\delta F_j),\qquad M^0_{ij}=S(\Theta F_i\,F_j),\qquad \omega_F(\delta)=\|M^\delta-M^0\|_{op}\to 0`. Valid when: The cutoff-removal topology controls every reflected collar probe and the delta downarrow 0 trace limit is taken inside the same locked gauge-invariant algebra.
- positivity transfer by matrix norm: `\sum_{i,j}\overline c_i c_j M^0_{ij}=\sum_{i,j}\overline c_i c_j M^\delta_{ij}+\sum_{i,j}\overline c_i c_j(M^0_{ij}-M^\delta_{ij})\ge -\|c\|^2\omega_F(\delta)\xrightarrow{\delta\downarrow0}0`. Valid when: M^delta is positive semidefinite for each fixed collar delta and omega_F(delta) tends to zero.
- boundary defect obstruction: `M^\delta\longrightarrow M^0+B_F,\qquad B_F\ne 0\quad\Longrightarrow\quad M^0+B_F\ge0\ \text{does not imply}\ M^0\ge0`. Valid when: The defect matrix B_F is a mixed reflection-plane contribution not already encoded by the source and target observable normalization.

## Attempted Derivation

- Start with regulated reflection positivity: for cutoff Schwinger forms S_{a,L} and any positive-time gauge-invariant collar observables T_delta F_i, Q_{a,L}(T_delta F,c)=sum_{i,j} overline{c_i} c_j S_{a,L}(Theta T_delta F_i,T_delta F_j)>=0.
- Use the RG-to-OS fixed-collar convergence topology: for fixed delta>0, every reflected product Theta T_delta F_i · T_delta F_j is separated from the reflection plane, so S_{a,L} -> S gives M^delta_{ij}=S(Theta T_delta F_i T_delta F_j) and M^delta is positive semidefinite.
- For uncollared F_i, write M^0_{ij}=S(Theta F_i F_j). If the finite-matrix trace modulus omega_F(delta)=||M^delta-M^0||_op tends to zero, then for every c, c^*M^0 c >= c^*M^delta c - ||c||^2 omega_F(delta) >= -||c||^2 omega_F(delta), hence c^*M^0 c>=0 after delta downarrow 0.
- For mirror-flat local composites, T_delta f -> f in the test-function topology and the Schwinger distributions are continuous, so the trace modulus follows unless there is an unrenormalized boundary contact term.
- For Wilson loops, try to express the collar limit as M^delta_{ij}->overline{lambda_i}lambda_j M^0_{ij}+E_{ij}. The diagonal congruence part is positivity-safe if lambda_i is locked in the observable definition. The remaining mixed term E_{ij}, or a nonfactorizing Schur factor R_{ij}, is the obstruction.
- The algebraic two-by-two model shows why this distinction matters: a mixed damping factor can make R circ M^0 positive even when M^0 is not positive, so closed-cone positivity of the collar limit cannot be quoted as OS positivity of the intended Schwinger functions.

Blocking gap: There is no proved Yang-Mills trace theorem for mixed reflected Wilson products as the reflected and unreflected networks collide at t=0. In particular, we lack a uniform no-new-boundary-renormalization/factorization estimate excluding cusp, hairpin, and curvature-contact defects in every finite OS matrix entry.

## Falsifiers

- Wilson-pair falsifier: find loops C_i,D_j whose collar product Theta C_i^delta with D_j^delta develops a cusp/hairpin at t=0 with a finite nonfactorizing mixed factor R_{ij}, so M^delta -> R circ M^0 rather than M^0.
- Boundary-counterterm falsifier: the collar limit of reflected Wilson products requires adding a plane-supported term such as an effective integral over t=0 of a gauge-invariant curvature density; then the positive form belongs to an enlarged boundary theory, not the same theory.
- Renormalization-ratio falsifier: the limit of Z_a(Theta C_delta · D_delta)/(Z_a(C_delta)Z_a(D_delta)) is nontrivial and pair-dependent as a->0 and delta->0, showing that individual Wilson renormalizations do not control mixed OS entries.
- Topology falsifier: Balaban-style or multiscale compactness controls separated probes for every fixed delta but gives no estimate uniform enough to pass delta downarrow 0 in finite OS matrices.
- Density falsifier: the mirror-flat local core plus admissible Wilson collars is not OS-dense in the locked positive-time algebra, so positivity on the controlled core does not extend to the desired target object.

## Learning

Cycle 180 refines the obstruction: not every Wilson boundary anomaly is equally fatal. A purely individual, pre-locked diagonal congruence preserves OS positivity, but a pair-dependent mixed defect can make the collar-limit matrix positive while the intended target matrix is indefinite. Thus the real same-theory condition is a finite-matrix factorization/no-defect theorem for reflected Wilson products at t=0. The local mirror-flat sector remains plausibly valid by distributional continuity; the decisive falsifier is now a nonfactorizing mixed Wilson cusp, hairpin, or boundary-contact term.

## Next Experiment

Analyze a two-by-two family of reflected rectangular or hairpin Wilson loops whose collars approach t=0. Track whether the known/expected cusp or perimeter renormalization of Theta C_delta · D_delta factorizes into individual loop normalizations or leaves a pair-dependent mixed factor; this gives the quickest concrete falsifier or proof target for the finite OS matrix trace modulus.
