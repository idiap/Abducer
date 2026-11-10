# cycle-0172

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Collar-to-plane OS extension lemma: Suppose a cutoff Yang-Mills net of gauge-invariant Schwinger functionals is reflection positive on every positive-time collar algebra, converges to a continuum functional in a topology dominating all fixed-collar reflected quadratic forms, and the continuum functional has a reflection-plane trace modulus for collar translations. Then the continuum Schwinger functional is OS reflection positive on the full positive-time gauge-invariant test algebra.

## Definitions

- source object: a net \(S_{a,L}\) of regulated gauge-invariant Schwinger functionals on one fixed abstract observable algebra \(\mathcal A\), with positive-time collar subalgebras \(\mathcal A_+^\delta\subset \mathcal A_+\) and reflection \(\Theta\).
- target object: a continuum Schwinger functional \(S\) on the same gauge-invariant Euclidean test algebra such that \(Q_S(F,c)\ge 0\) for all finite \(F_i\in\mathcal A_+\), giving the OS pre-Hilbert space before any Hamiltonian or mass-gap argument is invoked.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions through two maps: cutoff removal on fixed collars \(\delta>0\), followed by the valid \(\delta\downarrow0\) trace passage at the reflection plane.
- same-theory condition: the embeddings \(\iota_{a,L}:\mathcal A\to\mathcal A_{a,L}\) and collar translations \(T_\delta:\mathcal A_+\to\mathcal A_+^\delta\) commute with gauge-invariant renormalization, reflection, and the continuum identification, so the limiting observable is not replaced by a gauge-fixed, quotient, or boundary-renormalized different theory.
- For \(\delta>0\), \(\mathcal A_+^\delta\) denotes gauge-invariant observables whose smearing support lies in \(\{x_0\ge \delta\}\); \(T_\delta F\) is the positive time translation/collar regularization of \(F\).
- The OS quadratic form is \(Q_S(F,c)=\sum_{i,j}\overline c_i c_j S((\Theta F_i)^*F_j)\), with the product interpreted in the Euclidean gauge-invariant test algebra.

## Assumptions

- For every cutoff \((a,L)\), the regulated Wilson/Yang-Mills measure or transfer-matrix construction is reflection positive for all embedded collar observables \(\iota_{a,L}(F_i)\).
- For each fixed \(\delta>0\) and finite collar family \(F_1,\dots,F_n\in\mathcal A_+^\delta\), the RG cutoff-removal topology implies convergence of the reflected quadratic form \(Q_{a,L}^\delta(F,c)\to Q_S^\delta(F,c)\).
- The continuum functional has a trace/collar modulus: for each finite family \(F_i\in\mathcal A_+\), \(Q_S(T_\delta F,c)\to Q_S(F,c)\) as \(\delta\downarrow0\), uniformly for \(c\) in bounded subsets of \(\mathbb C^n\).
- Gauge-invariant composite renormalization does not introduce uncancelled reflection-plane counterterms that are invisible to the collar algebra.

## Equations

- regulated collar positivity: `Q_{a,L}^{\delta}(F,c)=\sum_{i,j}\overline c_i c_j\,S_{a,L}\big((\Theta\iota_{a,L}F_i)^*\iota_{a,L}F_j\big)\ge 0`. Valid when: Valid for \(F_i\in\mathcal A_+^\delta\), \(a\ll\delta\), finite volume large enough to contain supports, and a reflection-positive lattice or regulated construction.
- fixed-collar dominated cutoff passage: `\left|Q_{a,L}^{\delta}(F,c)-Q_S^{\delta}(F,c)\right|\le \varepsilon_{\delta,F,c}(a,L),\qquad \varepsilon_{\delta,F,c}(a,L)\to0`. Valid when: Valid exactly when the actual RG convergence topology dominates the finite OS seminorm determined by the reflected collar probe \((F,c,\delta)\).
- closed cone on each collar: `Q_S^{\delta}(F,c)=\lim_{a\to0,L\to\infty}Q_{a,L}^{\delta}(F,c)\ge0`. Valid when: Valid after the previous two hypotheses; this is the formal closed-cone step and contains no further Yang-Mills dynamics.
- reflection-plane trace modulus: `\left|Q_S(T_\delta F,c)-Q_S(F,c)\right|\le \omega_F(\delta)\,\|c\|^2,\qquad \omega_F(\delta)\downarrow0`. Valid when: Valid only if Schwinger distributions have controlled boundary values as reflected supports approach the plane and contact/cusp counterterms are either absent, already included in the same observable, or positive-compatible.
- full OS positivity: `Q_S(F,c)=\lim_{\delta\downarrow0}Q_S(T_\delta F,c)\ge0`. Valid when: Valid when collar positivity holds for every \(\delta>0\) and the trace modulus holds for the chosen full positive-time finite family.

## Attempted Derivation

- Fix a finite family \(F_1,\dots,F_n\in\mathcal A_+\) and coefficients \(c\in\mathbb C^n\). The target OS inequality is \(Q_S(F,c)\ge0\).
- For \(\delta>0\), replace each observable by its collar translate \(F_i^\delta=T_\delta F_i\in\mathcal A_+^\delta\). This avoids the reflection plane and makes the regulated reflection-positive inequality directly applicable for all sufficiently fine cutoffs.
- At cutoff level, reflection positivity gives \(Q_{a,L}^{\delta}(F,c)\ge0\). This is valid before the continuum limit and uses only the regulated positive-time algebra.
- Use the domination hypothesis \(\tau_{RG}\succeq\tau_{OS}(\mathcal A_+^\delta)\) to pass to the limit at fixed \(\delta\): \(Q_S(T_\delta F,c)=\lim Q_{a,L}^{\delta}(F,c)\ge0\).
- If the trace modulus \(|Q_S(T_\delta F,c)-Q_S(F,c)|\le\omega_F(\delta)\|c\|^2\) is available, let \(\delta\downarrow0\) and obtain \(Q_S(F,c)\ge0\).
- Because the argument applies to every finite family and coefficient vector, it would give OS positivity for the continuum gauge-invariant Schwinger functions and hence the OS reconstruction pre-Hilbert space.

Blocking gap: The missing Yang-Mills estimate is the reflection-plane trace modulus for the locked gauge-invariant algebra. Existing multiscale bounds plausibly control separated bulk correlations, but they do not automatically control the limit where reflected supports collide, Wilson loops acquire cusps at the plane, or composite curvature observables require boundary-sensitive renormalization.

## Falsifiers

- falsifier: construct a sequence of gauge-invariant Wilson-loop collar observables \(T_\delta W\) for which \(Q_S(T_\delta W,c)\ge0\) for every \(\delta>0\) but the limit as \(\delta\downarrow0\) is divergent, regulator-dependent, or not equal to the intended \(Q_S(W,c)\).
- falsifier: show that the RG compactness topology controls separated Schwinger distributions but not the product distribution \((\Theta T_\delta F)^*T_\delta G\) uniformly as supports approach the reflection plane.
- falsifier: find an unavoidable gauge-invariant reflection-plane counterterm with an indefinite matrix contribution to the OS quadratic form.
- falsifier: prove lattice reflection positivity only for transfer-matrix cylinder functions while the continuum test algebra uses smeared curvature composites or Wilson loops not approximable in the same positive-time algebra.
- falsifier: demonstrate that the collar translation \(T_\delta\) fails to commute with the continuum observable identification, so the limiting positive forms concern a different observable than the one appearing in the Yang-Mills Schwinger functions.

## Learning

Cycle 172 identifies the first genuinely non-tautological bridge after the closed-cone observation. Fixed-collar OS positivity is formally preserved once RG convergence is valid for reflected probes; the hard part is extending from collars to the reflection plane without changing the theory. The decisive estimate is a trace modulus for \(Q_S(T_\delta F,c)\to Q_S(F,c)\). This reframes the branch: reflection positivity is not merely closedness of a cone, but closedness plus a boundary-value theorem for gauge-invariant observables as reflected supports collide.

## Next Experiment

Work on a model finite family: two smeared curvature-square observables supported near \(x_0=0\). Translate them to collars, express the reflected quadratic form as a separated four-point distribution, and test whether known multiscale bounds imply a \(\delta\downarrow0\) modulus or whether a reflection-plane contact counterterm appears.
