# cycle-0174

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Collar-to-boundary OS positivity extension: if the RG continuum limit preserves reflection positivity for every fixed positive-time collar and the continuum Schwinger functional has a same-theory trace modulus as the collar is collapsed onto the reflection plane, then the limiting Schwinger functions are OS-positive on the full gauge-invariant positive-time test algebra. The closed-cone step is valid for fixed collars; the new content is the boundary trace estimate.

## Definitions

- source object: a cutoff net \(S_{a,L}\) of gauge-invariant regulated Schwinger functionals on reflected lattice/continuum observables, with \(Q_{a,L}(F,c)\ge 0\) for all finite positive-time observable vectors \(F\) in the cutoff algebra.
- target object: a continuum Schwinger functional \(S\) on a fixed gauge-invariant Euclidean observable algebra \(\mathcal A_+\), satisfying OS reflection positivity \(Q_S(F,c)\ge 0\) for all finite \(F\subset \mathcal A_+\).
- controlled interface: RG convergence must dominate the reflected quadratic probes \(Q^{\delta}_{a,L}(F,c)\) for every fixed collar distance \(\delta>0\), and the continuum limit must admit a trace modulus \(Q_S^{\delta}(F,c)\to Q_S(F,c)\) as \(\delta\downarrow0\).
- same-theory condition: the collar-shifted observables \(T_\delta F\) converge back to \(F\) in the locked continuum gauge-invariant observable topology, with no \(\delta\)-dependent change of algebra, no boundary counterterm, and no replacement by a different renormalized observable.
- \(\Theta\) is Euclidean time reflection with orientation reversal for loop observables and complex conjugation on coefficients.
- \(T_\delta\) is a positive-time collar insertion: it translates or mollifies the time support of every factor of \(F\) into \(t\ge\delta\) while preserving gauge invariance.

## Assumptions

- For every cutoff \((a,L)\), the regulated gauge-invariant functional is reflection-positive on the cutoff positive-time algebra.
- For each fixed \(\delta>0\), the observables \(T_\delta F_i\) are represented in the cutoff algebra by the same observable-identification maps used to define the continuum theory.
- For each fixed \(\delta>0\), RG convergence implies convergence of every finite reflected collar quadratic form.
- The continuum functional has a trace modulus \(\omega_{F,c}(\delta)\to0\) controlling the collision of reflected supports with the plane \(t=0\).
- The trace modulus is intrinsic to the original gauge-invariant algebra; it is not obtained by adding boundary degrees of freedom or imposing a new reflection-plane renormalization prescription.

## Equations

- collar quadratic form: `Q_S^{\delta}(F,c)=\sum_{i,j}\overline{c_i}c_j\,S(\Theta T_\delta F_i,\,T_\delta F_j)`. Valid when: This formula is valid when \(T_\delta F_i\) has support in \(t\ge\delta\), \(\Theta T_\delta F_i\) has support in \(t\le-\delta\), and both are evaluated in the same gauge-invariant continuum observable algebra.
- fixed-collar closed-cone passage: `Q_{a,L}^{\delta}(F,c)\ge0,\qquad Q_{a,L}^{\delta}(F,c)\longrightarrow Q_S^{\delta}(F,c)\quad\Longrightarrow\quad Q_S^{\delta}(F,c)\ge0`. Valid when: The RG cutoff-removal topology controls the finite reflected collar probe indexed by \((\delta,F,c)\).
- boundary trace modulus: `\left|Q_S(F,c)-Q_S^{\delta}(F,c)\right|\le \omega_{F,c}(\delta),\qquad \lim_{\delta\downarrow0}\omega_{F,c}(\delta)=0`. Valid when: Valid only after proving that reflection-plane contact terms, cusp divergences of loop observables, and composite-field renormalizations do not create a residual boundary defect.
- full OS positivity from collars: `Q_S(F,c)=\lim_{\delta\downarrow0}Q_S^{\delta}(F,c)\ge0`. Valid when: Every fixed-collar form is nonnegative and the trace modulus is same-theory continuous.

## Attempted Derivation

- Fix a finite positive-time gauge-invariant observable vector \(F=(F_1,\ldots,F_N)\) and coefficients \(c\in\mathbb C^N\). The desired OS inequality is \(Q_S(F,c)\ge0\).
- For \(\delta>0\), replace each observable by its collar version \(F_i^\delta=T_\delta F_i\), so reflected and unreflected supports are separated by a gap \(2\delta\).
- At the cutoff level, reflection positivity gives \(Q_{a,L}^{\delta}(F,c)=\sum_{i,j}\overline c_i c_j S_{a,L}(\Theta F_i^\delta,F_j^\delta)\ge0\).
- Use the RG-to-OS domination assumption for fixed collars to pass to the continuum: \(Q_{a,L}^{\delta}(F,c)\to Q_S^{\delta}(F,c)\). Since \([0,\infty)\) is closed, \(Q_S^{\delta}(F,c)\ge0\). This is the valid closed-cone step.
- Invoke the trace modulus \(|Q_S(F,c)-Q_S^{\delta}(F,c)|\le\omega_{F,c}(\delta)\), with \( omega_{F,c}(\delta)\to0\), to identify \(Q_S(F,c)=\lim_{\delta\downarrow0}Q_S^{\delta}(F,c)\).
- Conclude \(Q_S(F,c)\ge0\) as a limit of nonnegative real numbers, provided the trace modulus is same-theory and no boundary defect has been inserted or subtracted.

Blocking gap: The missing Yang-Mills estimate is a uniform reflection-plane trace theorem for the locked gauge-invariant algebra. It must control contact terms of curvature composites, cusp/edge divergences of Wilson-loop observables, and possible boundary renormalizations as \(T_\delta F\to F\).

## Falsifiers

- falsifier: an RG compactness topology that controls ordinary Schwinger distributions but not the mixed reflected seminorms \(S(\Theta T_\delta F_i,T_\delta F_j)\) for fixed \(\delta\).
- falsifier: a Wilson-loop family whose reflection-plane cusp renormalization produces a nonzero defect \(B(F,c)\), so the collar boundary value is not the intended OS quadratic form.
- falsifier: curvature-composite observables with reflection-plane contact terms requiring a boundary counterterm; this would make the closed-cone argument valid only for a modified theory.
- falsifier: the collar map \(T_\delta\) converges in a weak distribution topology but not in the OS quadratic-form topology, preventing \(Q_S^{\delta}(F,c)\to Q_S(F,c)\).
- falsifier: the cutoff observable embeddings depend on \(\delta\) or on the side of the reflection plane, meaning the proof has changed the gauge-invariant test algebra across the limit.

## Learning

Cycle 174 isolates the exact non-tautological bridge. Reflection positivity is not lost in the fixed-collar continuum passage: that part is a valid closed-cone argument once RG convergence controls reflected probes. The unresolved mathematical content is the trace modulus at the reflection plane. This estimate is also the same-theory certificate: if the collar limit requires subtracting a boundary defect, adding a counterterm, or changing Wilson-loop renormalization at the plane, then the proof may preserve positivity but for the wrong theory. The most useful next work is therefore not another abstract topology name, but a model trace estimate for a dense gauge-invariant core and a search for a concrete falsifier among cusp loops or curvature contact terms.

## Next Experiment

Test the trace modulus first in a controlled Gaussian/linearized Yang-Mills model for smeared curvature observables: compute \(Q_S^{\delta}(F,c)-Q_S(F,c)\) as \(\delta\downarrow0\), identify the required Sobolev trace regularity, then repeat for a smoothed rectangular Wilson-loop observable approaching the reflection plane to see whether a cusp-defect falsifier appears.
