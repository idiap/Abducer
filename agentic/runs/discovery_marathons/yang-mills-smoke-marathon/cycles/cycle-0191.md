# cycle-0191

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

No-boundary-sector Schur rigidity lemma: after fixed-collar RG convergence has produced a positive collar-limit OS matrix \(N\), the intended same-theory OS matrix \(M\) is protected from a Wilson boundary anomaly \(B\) only when the boundary anomaly is a rank-one diagonal congruence. Equivalently, if \(N=B\circ M\) and \(B\) is a normalized Gram kernel of possible reflected Wilson hairpin boundary states, then the closed-cone argument is a valid same-theory positivity bridge for all finite families only if the boundary Hilbert sector is one-dimensional. A nontrivial boundary state overlap \(|B_{12}|<1\) is a finite-matrix falsifier of the bridge unless an independent Yang-Mills estimate proves that the actual collar matrices never probe the dangerous reciprocal Schur multiplier.

## Definitions

- source object: regulated reflection-positive Schwinger forms \(S_{a,L}\) on a locked gauge-invariant positive-time algebra \(\mathcal A_W^+\), with Wilson/local observables moved off the reflection plane by collar embeddings \(T_\delta\).
- target object: continuum OS-positive Schwinger functions \(S\) on the same locked gauge-invariant observable algebra, with OS matrices \(M_{ij}=S(\Theta F_i,F_j)\) for finite positive-time families \(F_i\).
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, controlled by convergence of every finite reflected collar quadratic form and by the absence of nontrivial boundary hairpin factors.
- same-theory condition: the collar limit may apply predeclared bulk Wilson renormalizations and harmless diagonal congruences, but it may not adjoin a new boundary Hilbert factor, boundary counterterm, pair-dependent cusp factor, or changed Wilson-loop algebra.

## Assumptions

- For every fixed \(\delta>0\), \(N^{(a,L,\delta)}_{ij}=S_{a,L}(\Theta T_\delta F_i,T_\delta F_j)\) is positive semidefinite by regulated reflection positivity.
- The RG/cutoff-removal topology is valid for reflected collar probes: \(N^{(a,L,\delta)}\to N^{(\delta)}\), and then \(N^{(\delta)}\to N\) entrywise for each finite family.
- Diagonal trace continuity and positivity have already removed positive additive boundary contacts, so the remaining possible defect is multiplicative: \(N_{ij}=B_{ij}M_{ij}\), with \(B_{ij}\ne0\).
- The Wilson boundary defect, if present, is representable as a normalized Gram kernel \(B_{ij}=\langle \eta_i,\eta_j\rangle_{\mathcal K_\partial}\), \(B_{ii}=1\), for boundary hairpin states \(\eta_i\). This is the natural case for a positive boundary sector produced by a collar collapse.

## Equations

- collar-limit factorization: `N_{ij}=\lim_{\delta\downarrow0}\lim_{a,L}S_{a,L}(\Theta T_\delta F_i,T_\delta F_j)=B_{ij}\,M_{ij},\qquad M_{ij}=S(\Theta F_i,F_j).`. Valid when: Valid when all additive contact terms vanish and the residual Wilson boundary anomaly is multiplicative after the fixed bulk renormalization scheme has been locked.
- reciprocal-Schur transfer condition: `M=B^{[-1]}\circ N,\qquad B^{[-1]}_{ij}=1/B_{ij};\quad N\ge0\ \forall N\ \Longrightarrow\ M\ge0\ \forall N\ \text{ only if }\ B^{[-1]}\ge0.`. Valid when: Valid as a universal finite-matrix bridge condition by the Schur product theorem; without positivity of the reciprocal kernel, collar positivity does not formally imply target OS positivity.
- normalized-Gram rigidity: `B_{ij}=\langle\eta_i,\eta_j\rangle,\ B_{ii}=1,\ B^{[-1]}\ge0\ \Longrightarrow\ 0\le\det\begin{pmatrix}1&1/B_{ij}\\1/\overline{B_{ij}}&1\end{pmatrix}=1-|B_{ij}|^{-2},\ \text{ hence } |B_{ij}|=1.`. Valid when: Valid for every two-by-two principal minor. Combined with Cauchy-Schwarz for the Gram kernel, it forces all boundary states to be collinear; normalized phases are only diagonal congruences.
- two-state damping falsifier: `B=\begin{pmatrix}1&\beta\\\overline\beta&1\end{pmatrix},\quad 0<|\beta|<1,\quad N=\begin{pmatrix}1&r\\\overline r&1\end{pmatrix},\quad |\beta|<|r|\le1\ \Longrightarrow\ M=B^{[-1]}\circ N\ \text{ has }\det M=1-|r/\beta|^2<0.`. Valid when: Valid as a finite-dimensional falsifier of any bridge that tries to infer same-theory positivity from collar positivity while allowing a nonrank-one normalized boundary damping factor.

## Attempted Derivation

- Start with the fixed-collar cone argument: for each \(\delta>0\), regulated reflection positivity gives \(N^{(a,L,\delta)}\ge0\). Because the RG topology is assumed valid for reflected collar probes, entrywise convergence passes positivity to \(N^{(\delta)}\), and the collar limit gives \(N\ge0\).
- Use the earlier trace analysis: local mirror-flat composites pass to the reflection plane by distributional continuity, and positive additive boundary contacts vanish once diagonal trace continuity is known. Therefore the unresolved Wilson obstruction can be isolated as a multiplicative matrix \(B\) with \(N=B\circ M\).
- Ask what is required to infer the intended target positivity \(M\ge0\) from the proved collar positivity \(N\ge0\). For a bridge lemma that is independent of accidental properties of one finite family, this requires the reciprocal entrywise multiplier \(B^{[-1]}\) to preserve positivity, hence to be a positive Schur multiplier on every finite OS matrix.
- Assume the boundary anomaly is not arbitrary but comes from a genuine positive boundary sector: \(B_{ij}=\langle\eta_i,\eta_j\rangle\), \(B_{ii}=1\). Then every two-by-two minor of \(B^{[-1]}\) gives \(1-|B_{ij}|^{-2}\ge0\), while Cauchy-Schwarz gives \(|B_{ij}|\le1\). Hence \(|B_{ij}|=1\), so equality in Cauchy-Schwarz forces \(\eta_i\) and \(\eta_j\) to be collinear for all pairs.
- Conclude that a valid same-theory bridge permits only a one-dimensional boundary sector, equivalently a diagonal phase/congruence already included in the locked renormalization convention. Any normalized damping \(|B_{ij}|<1\) is not a harmless Wilson-loop normalization; it is evidence that the collar construction proves positivity for an enlarged bulk-plus-boundary theory.
- Linearize this conclusion around smooth Wilson hairpins. A nonzero connected boundary covariance \(C_\partial\) yields \(|B_{\xi\eta}|<1\) for distinguishable boundary jets, hence violates the reciprocal-Schur condition. Therefore the analytic target becomes \(C_\partial=0\) or, equivalently, vanishing of all logarithmic cross-ratios \(K\) on the dense Wilson core.

Blocking gap: The missing Yang-Mills estimate is the no-boundary-sector theorem: after bulk Wilson renormalization, reflected Wilson collars must have \(B_{ij}=e^{i\alpha_i-i\alpha_j}\) and hence \(K=0\) for all finite mixed OS pairings. We do not yet have a nonperturbative bound excluding a connected coincident-footprint boundary OPE for Wilson hairpins.

## Falsifiers

- falsifier: a pair of reflected Wilson hairpin observables with normalized boundary overlap \(|B_{12}|<1\) after all accepted diagonal Wilson renormalizations are removed.
- falsifier: a nonzero logarithmic cross-ratio \(K_{12;34}\) for four mixed reflected Wilson collar pairings sharing a coincident boundary footprint.
- falsifier: a computed positive boundary covariance \(C_\partial\ne0\) in the infinitesimal hairpin expansion, since it creates a nontrivial boundary Hilbert factor rather than the intended same theory.
- falsifier: RG convergence that is valid for separated collars but loses uniformity as the collar thickness approaches the reflection plane, leaving \(B\) undefined or pair-dependent.
- falsifier: a proof of reflection positivity only for the enlarged matrix \(N\) while the recovered same-theory matrix \(M=B^{[-1]}\circ N\) fails a two-by-two determinant test.

## Learning

Cycle 191 recasts the remaining Wilson obstruction as a boundary Hilbert-sector problem. The formal closed-cone passage is valid for collar matrices, but if collar collapse produces a normalized Gram factor \(B\), then same-theory positivity requires the reciprocal Schur multiplier \(B^{[-1]}\) to be positive. Two-by-two minors plus Cauchy-Schwarz force such a Gram factor to be rank one. Thus the analytic Yang-Mills goal is sharper than generic reflection-positivity preservation: prove that reflected Wilson hairpins have no nontrivial boundary state, equivalently \(K=0\) or \(C_\partial=0\) on the locked Wilson core. Any nonzero boundary covariance is a substantive falsifier, not a removable normalization nuisance.

## Next Experiment

Try to compute the second area-variation of \(\log B_{\xi\eta}\) for two mirror-smooth Wilson hairpins with the same boundary footprint. Express it as a boundary limit of connected curvature insertions; check whether gauge invariance, reflection parity, and bulk renormalization force the resulting \(C_\partial\) to vanish or instead produce a nonzero cusp/hairpin kernel.
