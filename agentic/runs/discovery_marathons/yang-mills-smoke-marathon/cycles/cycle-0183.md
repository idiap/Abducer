# cycle-0183

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Finite Schur-reciprocal boundary-anomaly bridge: fix a finite positive-time gauge-invariant family F=(F_1,...,F_n). Suppose the collared regulated OS matrices converge to a positive matrix N and the intended continuum OS matrix M is related to N by a nonzero Hermitian entrywise boundary anomaly N=\Gamma\circ M. Then M is positive whenever the entrywise reciprocal H=\Gamma^{[-1]}=(\gamma_{ij}^{-1}) is positive semidefinite, since M=H\circ N and Schur multiplication by a positive matrix preserves positivity. Conversely, if the bridge is required to be valid for all possible positive collar limits N, positivity of H is necessary. If in addition \Gamma is itself a positive boundary covariance kernel with positive diagonal, then H\ge0 forces \Gamma to be rank one, i.e. \gamma_{ij}=\overline z_i z_j. Thus any nonfactorizing mixed Wilson boundary anomaly is not cosmetic: it is a same-theory falsifier unless an independent Yang-Mills estimate proves that the actual N lies in a smaller cone where H\circ N remains positive.

## Definitions

- source object: finite cutoff/collared gauge-invariant OS matrices N^{a,L,\delta}_{ij}=S_{a,L}(\Theta T_\delta F_i,T_\delta F_j) produced from reflection-positive regulated Schwinger forms on the positive-time algebra.
- target object: the intended continuum OS matrix M_{ij}=S(\Theta F_i,F_j) for the locked gauge-invariant continuum Schwinger functional, before adding any boundary counterterm or changing Wilson-loop renormalization at the reflection plane.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions by convergence of every finite reflected quadratic form together with a trace comparison N=\Gamma\circ M between collar limits and reflection-plane target values.
- same-theory condition: the embeddings T_\delta, observable normalizations, and gauge-invariant test algebra are fixed before the positivity argument; a diagonal congruence already built into these choices is harmless, but a pair-dependent mixed anomaly \Gamma is a change of theory unless its reciprocal Schur action is proved valid for the intended target matrix cone.
- Entrywise product convention: (A\circ B)_{ij}=A_{ij}B_{ij}; \Gamma^{[-1]} denotes entrywise reciprocal, not the matrix inverse.
- Finite OS matrix convention: OS positivity for F is equivalent to c^*Mc\ge0 for every c\in\mathbb C^n.

## Assumptions

- For every fixed collar width \delta>0 and cutoff pair (a,L), regulated reflection positivity gives N^{a,L,\delta}\ge0.
- The cutoff-removal topology is valid for the reflected probes under consideration, so N^\delta=\lim_{a,L}N^{a,L,\delta}\ge0 and N=\lim_{\delta\downarrow0}N^\delta\ge0 entrywise as a finite matrix.
- The reflection-plane trace discrepancy for this finite family is purely multiplicative and nonvanishing: N_{ij}=\gamma_{ij}M_{ij}, with \Gamma=\Gamma^* and \gamma_{ii}>0.
- For the direct Schur transfer conclusion, H=\Gamma^{[-1]} is positive semidefinite. For the rigidity conclusion, \Gamma is also positive semidefinite as a boundary anomaly covariance kernel.

## Equations

- collared OS matrix: `N^{a,L,\delta}_{ij}=S_{a,L}(\Theta T_\delta F_i,T_\delta F_j),\qquad c^*N^{a,L,\delta}c\ge0`. Valid when: The collared observables T_\delta F_i lie strictly in the positive-time regulated gauge-invariant algebra and the lattice/regulated measure is reflection positive.
- closed cone collar limit: `N^{a,L,\delta}\to N\quad\Longrightarrow\quad c^*Nc=\lim_{\delta}\lim_{a,L}c^*N^{a,L,\delta}c\ge0`. Valid when: The RG cutoff-removal topology controls the finite reflected quadratic form for this fixed finite family and collar trace.
- multiplicative boundary anomaly: `N_{ij}=\gamma_{ij}M_{ij},\qquad H_{ij}=\gamma_{ij}^{-1},\qquad M=H\circ N`. Valid when: No additive reflection-plane contact term remains and every pairwise Wilson/composite trace defect is represented by a nonzero finite multiplicative factor.
- Schur reciprocal transfer: `H\ge0,\;N\ge0\quad\Longrightarrow\quad M=H\circ N\ge0`. Valid when: The entrywise reciprocal anomaly matrix H is positive semidefinite; this is exactly the condition making the recovery map a positive Schur multiplier on all finite positive collar matrices.
- positive-anomaly rigidity: `\Gamma\ge0,\;H=\Gamma^{[-1]}\ge0\quad\Longrightarrow\quad |\gamma_{ij}|^2=\gamma_{ii}\gamma_{jj}\quad\forall i,j\quad\Longrightarrow\quad \Gamma=zz^*`. Valid when: The anomaly kernel has positive diagonal and both the anomaly and its entrywise reciprocal are positive semidefinite on the same finite index set.
- two-by-two damping falsifier: `\Gamma=\begin{pmatrix}1&\beta\\ \overline\beta&1\end{pmatrix},\quad 0<|\beta|<1,\quad H=\begin{pmatrix}1&\beta^{-1}\\ \overline\beta^{-1}&1\end{pmatrix},\quad \det H=1-|\beta|^{-2}<0`. Valid when: A normalized mixed Wilson boundary damping factor |\beta|<1 is present; taking a rank-one positive collar matrix N shows that the intended recovered matrix M=H\circ N can be indefinite.

## Attempted Derivation

- Start with a finite positive-time observable vector F=(F_1,\ldots,F_n) in the locked gauge-invariant continuum algebra and choose collar embeddings T_\delta F_i supported at t\ge\delta.
- For every cutoff and collar, regulated reflection positivity gives c^*N^{a,L,\delta}c=\sum_{ij}\overline c_i c_j S_{a,L}(\Theta T_\delta F_i,T_\delta F_j)\ge0.
- Assuming the RG topology is valid for these reflected probes, pass first to the continuum cutoff limit and then to the collar limit; the cone of positive finite matrices is closed, so N\ge0.
- Compare N with the intended target OS matrix M_{ij}=S(\Theta F_i,F_j). If the trace defect is multiplicative, write N=\Gamma\circ M with nonzero Hermitian \Gamma.
- Recover M entrywise as M=H\circ N where H=\Gamma^{[-1]}. If H\ge0, the Schur product theorem gives M\ge0, hence the finite OS quadratic form for the intended continuum Schwinger functions is positive.
- Check rigidity under the additional natural hypothesis that \Gamma is itself a positive anomaly kernel: positivity of every 2-by-2 principal minor of \Gamma gives |\gamma_{ij}|^2\le\gamma_{ii}\gamma_{jj}; positivity of the corresponding minor of H gives |\gamma_{ij}|^2\ge\gamma_{ii}\gamma_{jj}. Therefore equality holds for every pair, forcing rank-one factorization \gamma_{ij}=\overline z_i z_j.
- Conclude that a genuine positive, nonfactorizing mixed anomaly cannot both arise as a covariance-like defect and allow a universal Schur recovery of target positivity. In normalized two-by-two form, any damping |\beta|<1 makes H indefinite and supplies an explicit linear algebra falsifier.

Blocking gap: The derivation does not yet prove that Yang-Mills Wilson collar limits have a purely multiplicative defect N=\Gamma\circ M, nor that the anomaly kernel \Gamma is positive, nor that additive cusp/contact terms vanish. Those are analytic Wilson-loop trace estimates at the reflection plane, not formal consequences of closed-cone topology.

## Falsifiers

- falsifier: a two-loop reflected Wilson family with normalized mixed collar anomaly 0<|\beta|<1; then the reciprocal Schur matrix has negative determinant and the positivity transfer from N to M is not valid.
- falsifier: an additive reflection-plane contact matrix B in N=M+B for mixed Wilson products, since the Schur-reciprocal bridge assumes a purely multiplicative trace comparison.
- falsifier: a collar construction whose individual loop renormalizations are finite but whose mixed reflected product has a pair-dependent cusp or hairpin factor not expressible as \overline z_i z_j.
- falsifier: the RG compactness topology controls separated Wilson loops but not the colliding reflected products needed for the finite OS matrix entries.
- falsifier: the gauge-invariant test algebra is enlarged after taking the collar limit by adding boundary observables or counterterms; positivity may remain true but not for the same theory.

## Learning

Cycle 183 improves the previous rank-one warning into an exact finite matrix mechanism. The closed-cone argument gives N\ge0, but the intended target matrix is M=\Gamma^{[-1]}\circ N when a multiplicative boundary anomaly is present. The bridge is valid if the reciprocal anomaly is a positive Schur multiplier. Under the natural extra assumption that the anomaly itself is a positive boundary kernel, this condition forces rank-one diagonal congruence; hence a nonfactorizing mixed Wilson damping is a real same-theory falsifier, not a normalization nuisance. The remaining Yang-Mills work is therefore sharply stated: prove that mixed reflected Wilson collar limits have no additive contact term and no nonfactorizing anomaly, or exhibit the two-by-two damping counterexample.

## Next Experiment

Work out a model two-Wilson-loop collar calculation for a reflected hairpin/cusp geometry: identify whether the known cusp anomalous dimension contributes as an individual diagonal factor, a rank-one congruence, or a genuinely mixed damping \beta. The decisive output should be the 2-by-2 anomaly matrix \Gamma and the determinant of its reciprocal H.
