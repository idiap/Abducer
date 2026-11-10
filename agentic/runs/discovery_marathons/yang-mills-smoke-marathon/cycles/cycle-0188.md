# cycle-0188

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: boundary cross-ratio obstruction

## Candidate Lemma

Let \(F_1,\dots,F_n\) be locked gauge-invariant Wilson/composite observables in the positive-time algebra and \(T_\delta F_i\) mirror-smooth collars avoiding the reflection plane. If the fixed-collar continuum OS matrices have a boundary trace relation \(N_{ij}=\Gamma_{ij}M_{ij}+A_{ij}\), with diagonal trace continuity, positive additive contact \(A\ge0\), and vanishing logarithmic cross-ratios of the multiplicative anomaly \(K_{ik;jl}=0\), then OS positivity of \(N\) implies OS positivity of the intended target matrix \(M\). Thus the only remaining same-theory obstruction is a nonzero connected coincident-footprint Wilson boundary OPE.

## Definitions

- source object: finite cutoff/continuum-collar OS matrices \(N^{\delta}_{ij}=S(\Theta T_\delta F_i,T_\delta F_j)\) obtained from regulated reflection-positive gauge-invariant Schwinger forms after fixed-collar RG limits.
- target object: uncollared continuum OS matrix \(M_{ij}=S(\Theta F_i,F_j)\) on the locked gauge-invariant test algebra, from which the OS Hilbert space and positive Hamiltonian are reconstructed.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions via finite reflected quadratic forms and collar-to-plane trace limits.
- same-theory condition: \(F_i\) and \(T_\delta F_i\) represent the same preselected renormalized Wilson/composite observable; allowed boundary factors are only individual diagonal congruences already fixed in the observable normalization, never pair-dependent counterterms introduced to force positivity.

## Assumptions

- For every \(\delta>0\), cutoff Schwinger forms for \(T_\delta F_i\) are reflection positive and converge in a topology controlling the finite OS matrix entries.
- The collar limit admits \(N_{ij}=\lim_{\delta\downarrow0}S(\Theta T_\delta F_i,T_\delta F_j)\) and an intended trace matrix \(M_{ij}=S(\Theta F_i,F_j)\).
- Boundary comparison has the form \(N=\Gamma\circ M+A\), where \(\Gamma_{ij}\ne0\) is multiplicative and \(A\) is an additive contact matrix.
- Diagonal trace continuity holds: \(A_{ii}=0\) and \(N_{ii}=\Gamma_{ii}M_{ii}\) with \(\Gamma_{ii}>0\).
- The additive contact is OS-positive, \(A\ge0\), and the multiplicative anomaly has zero logarithmic cross-ratios on every finite test family.

## Equations

- fixed-collar positivity: `Q_\delta(c)=\sum_{i,j}\overline c_i c_j\,S(\Theta T_\delta F_i,T_\delta F_j)\ge0`. Valid when: The collars have support in positive Euclidean time separated from the reflection plane and the regulated/lattice theory is reflection positive on the locked gauge-invariant algebra.
- boundary comparison: `N_{ij}=\lim_{\delta\downarrow0}S(\Theta T_\delta F_i,T_\delta F_j)=\Gamma_{ij}M_{ij}+A_{ij}`. Valid when: The collar trace has a finite multiplicative Wilson boundary anomaly and a finite additive contact term for the same target observable \(F_i\).
- additive contact vanishing: `A\ge0,\quad A_{ii}=0\ \forall i\quad\Longrightarrow\quad A_{ij}=0\ \forall i,j`. Valid when: \(A\) is a positive semidefinite finite OS contact matrix; follows from Cauchy-Schwarz \(|A_{ij}|^2\le A_{ii}A_{jj}\).
- cross-ratio criterion: `K_{ik;jl}:=\log\Gamma_{ij}+\log\Gamma_{kl}-\log\Gamma_{il}-\log\Gamma_{kj}=0\quad\Longleftrightarrow\quad\Gamma_{ij}=\alpha_i\overline{\alpha_j}`. Valid when: All \(amma_{ij}\) are nonzero and a consistent logarithm is chosen on the finite connected index graph; phases are absorbed into \(\alpha_i\).
- positivity transfer by congruence: `N=\Gamma\circ M=D M D^*,\quad D=\operatorname{diag}(\alpha_i)\quad\Longrightarrow\quad M=D^{-1}ND^{-*}\ge0`. Valid when: The cross-ratio criterion gives an invertible diagonal congruence and no additive contact remains.

## Attempted Derivation

- Start with regulated reflection positivity for collared observables: for fixed \(a,L,\delta\), \(Q_{a,L,\delta}(c)=\sum\overline c_i c_j S_{a,L}(\Theta T_\delta F_i,T_\delta F_j)\ge0\).
- Use RG convergence at fixed \(\delta\) to pass \(a\downarrow0,L\uparrow\infty\); closedness of the positive cone gives a valid positive matrix \(N^\delta\ge0\), and subsequential collar compactness gives \(N=\lim_{\delta\downarrow0}N^\delta\ge0\).
- Compare the collar-limit matrix with the intended uncollared target by \(N=\Gamma\circ M+A\). Diagonal trace continuity plus \(A\ge0\) forces \(A=0\), so the only possible mismatch is multiplicative.
- If all logarithmic cross-ratios of \(\Gamma\) vanish, solve \(\Gamma_{ij}=\alpha_i\overline{\alpha_j}\); then \(N=DMD^*\) and \(M=D^{-1}ND^{-*}\ge0\).
- Thus the proof reduces to a Yang-Mills boundary OPE estimate: show that connected coincident-footprint Wilson cumulants vanish or are already included as individual one-body normalizations.

Blocking gap: No available multiscale estimate proves that reflected Wilson products with coincident boundary footprints have zero connected finite boundary cumulant. Gauge invariance and locality kill separated-footprint terms, but they do not yet exclude a local pair-dependent hairpin/cusp/contact operator at \(t=0\).

## Falsifiers

- falsifier: a perturbative or constructive computation of two reflected Wilson collars sharing a boundary tangent gives \(K_{12;12}\ne0\) after all one-body Wilson renormalizations are fixed.
- falsifier: the RG cutoff-removal topology controls only collars with distance \(\delta>0\) from the reflection plane and provides no uniform trace modulus as \(\delta\downarrow0\).
- falsifier: positivity is restored only after adding a pair-dependent boundary counterterm \(Z_{ij}\), which is valid for a modified boundary-renormalized algebra but violates the same-theory condition.
- falsifier: an additive mixed contact survives with zero diagonal; this would contradict positive-contact compatibility and signal that the assumed OS-positive boundary OPE decomposition is false.

## Learning

Cycle 188 turns the Wilson boundary obstruction into an exact bridge/falsifier pair. Additive contacts are harmless once diagonal trace continuity and positivity are valid; multiplicative anomalies are harmless exactly when their logarithmic cross-ratio vanishes, equivalently when they are only diagonal congruences. Therefore the real Yang-Mills problem is not generic reflection positivity preservation, but proving absence of connected coincident-footprint boundary OPE terms for reflected Wilson products. A nonzero \(K\) is the compact invariant that falsifies the same-theory bridge.

## Next Experiment

Compute the leading boundary OPE for two mirror-smooth rectangular Wilson loops whose collars form a reflected hairpin at \(t=0\); subtract individual perimeter/cusp terms and test whether the residual logarithmic cross-ratio \(K_{ik;jl}\) is zero.
