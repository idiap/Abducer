# cycle-0187

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: Wilson Boundary Cross-Ratio Localization

## Candidate Lemma

Boundary-footprint localization bridge for Wilson OS anomalies. For a finite mirror-smooth Wilson core, let N_{ij}=lim_{\delta\downarrow0} S(\Theta W(T_\delta C_i) W(T_\delta D_j)) be the collar OS matrix and M_{ij}=S(\Theta W(C_i)W(D_j)) the intended target matrix. Assume diagonal trace continuity, no positive additive contact defect, and a local multiplicative anomaly representation \Gamma_{ij}=\exp(\alpha_i+\overline{\alpha_j}+B(\beta_i,\beta_j)), where \beta_i,\beta_j are reflection-plane boundary footprints and B is supported only on coincident footprints. Then every separated-footprint finite OS matrix transfers positivity by a rank-one congruence; equivalently the logarithmic cross-ratio K_{ik;jl} vanishes. Thus the only remaining same-theory obstruction is a connected coincident-footprint boundary OPE term detected by K\ne0.

## Definitions

- source object: cutoff reflection-positive gauge-invariant Schwinger functionals S_{a,L} on a locked positive-time Wilson/core algebra, with collar maps T_\delta pushing plane-touching observables into t>\delta.
- target object: continuum gauge-invariant Schwinger functional S on the same Wilson/core algebra, satisfying OS positivity for finite reflected quadratic forms including observables with support at the reflection plane.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, first for fixed collars through the closed cone topology and then through a boundary trace theorem for Wilson OS matrices.
- same-theory condition: Wilson-loop renormalizations and observable embeddings are fixed before the collar limit; allowed boundary factors are only one-body diagonal congruences already built into that identification, never pair-dependent counterterms introduced to repair positivity.

## Assumptions

- For each fixed collar width \delta>0 and finite coefficient vector c, Q_{a,L,\delta}(c)=\sum_{i,j}\overline c_i c_j S_{a,L}(\Theta W(T_\delta C_i)W(T_\delta D_j))\ge0, and the cutoff-removal topology is valid for these reflected Wilson products.
- The fixed-collar continuum limit exists: N^\delta_{ij}=S(\Theta W(T_\delta C_i)W(T_\delta D_j)) and N^\delta\to N entrywise along \delta\downarrow0 for the finite matrix under study.
- Diagonal trace continuity is locked in the same theory: N_{ii}=\Gamma_{ii}M_{ii} with \Gamma_{ii}>0 and no independent additive diagonal contact term.
- Any additive boundary contact matrix A appearing in N=\Gamma\circ M+A is positive semidefinite as a boundary OS contribution; hence zero diagonal forces A=0.
- The multiplicative anomaly admits a local footprint decomposition \log\Gamma_{ij}=\alpha_i+\overline{\alpha_j}+B(\beta_i,\beta_j), where B(\beta_i,\beta_j)=0 when the two boundary footprints are separated by a positive distance in the reflection plane.
- The one-body terms \alpha_i are valid same-theory renormalizations, i.e. they implement an invertible diagonal congruence rather than changing the target Schwinger functions.

## Equations

- fixed-collar OS matrix: `N^\delta_{ij}=S(\Theta W(T_\delta C_i)W(T_\delta D_j)),\qquad \sum_{i,j}\overline c_i c_j N^\delta_{ij}\ge0`. Valid when: The Wilson loops after collaring lie strictly in positive/negative time and the regulated reflection positivity survives the RG limit for these fixed reflected probes.
- boundary anomaly decomposition: `N_{ij}=\Gamma_{ij}M_{ij}+A_{ij},\qquad \log\Gamma_{ij}=\alpha_i+\overline{\alpha_j}+B(\beta_i,\beta_j)`. Valid when: The collar limit exists entrywise and the only loss between the collar matrix and the intended target matrix is a multiplicative Wilson boundary factor plus a separately positive additive contact contribution.
- additive contact vanishing: `A\ge0,\quad A_{ii}=0\ \forall i\quad\Longrightarrow\quad |A_{ij}|^2\le A_{ii}A_{jj}=0\quad\Longrightarrow\quad A=0`. Valid when: The boundary contact term is itself an OS-positive matrix and diagonal trace continuity has already removed diagonal contact defects.
- cross-ratio detector: `K_{ik;jl}=\log\Gamma_{ij}+\log\Gamma_{kl}-\log\Gamma_{il}-\log\Gamma_{kj}=B(\beta_i,\beta_j)+B(\beta_k,\beta_l)-B(\beta_i,\beta_l)-B(\beta_k,\beta_j)`. Valid when: The logarithmic anomaly decomposition is valid; one-body congruence terms cancel exactly.
- rank-one transfer: `K_{ik;jl}=0\ \forall i,k,j,l\quad\Longrightarrow\quad \Gamma_{ij}=d_i\overline{d_j},\quad N=DMD^*,\quad M=D^{-1}ND^{-*}\ge0`. Valid when: The finite anomaly matrix has nonzero entries and the vanishing cross-ratio holds on the finite Wilson OS matrix under consideration.

## Attempted Derivation

- Start with a finite Wilson core {W(C_i)} in the positive half-space closure and apply collaring T_\delta so every observable has support in t>\delta. For each cutoff, reflection positivity gives Q_{a,L,\delta}(c)\ge0.
- Use the RG-to-OS passage only for fixed collars: S_{a,L}(\Theta W(T_\delta C_i)W(T_\delta D_j)) converges to N^\delta_{ij}, and the closed positive cone gives N^\delta\ge0. Taking \delta\downarrow0 entrywise gives N\ge0 when the trace limit is controlled.
- Compare N with the intended plane-touching target matrix M. The most general boundary discrepancy compatible with earlier cycles is N=\Gamma\circ M+A, with A additive and \Gamma multiplicative.
- Invoke diagonal trace continuity. If A is a positive boundary OS contribution, finite-dimensional Cauchy-Schwarz gives A=0. This removes additive contacts unless positivity of the boundary OPE itself fails.
- Write \log\Gamma_{ij}=\alpha_i+\overline{\alpha_j}+B(\beta_i,\beta_j). The one-body terms are exactly diagonal congruences and cancel from K_{ik;jl}. Thus K is the finite difference of only the connected boundary footprint interaction B.
- If the footprints are separated, locality predicts B=0; then \Gamma_{ij}=d_i\overline{d_j}, so N=DMD^* and M\ge0 follows. This part of the OS bridge is valid provided the local anomaly decomposition is valid.
- For coincident footprints, test B perturbatively by the reflected Wilson product. At leading gauge-field order a possible connected term has the schematic form B(C,D)\sim g^2 C_2\lim_{\delta\downarrow0}\left[\int_{\partial C\times\partial D}\frac{\dot\gamma(s)\cdot\dot\eta(t)}{|\gamma(s)-\eta(t)|^2+(2\delta)^2}\,ds\,dt-\text{one-body perimeter/cusp subtractions}\right]. If the remaining finite part has nonzero four-point finite difference, K\ne0 and the same-theory bridge fails.
- The derivation therefore reduces the analytic Yang-Mills problem to a boundary OPE statement: prove the connected post-subtraction kernel B has zero finite differences on a dense Wilson core, or exhibit a nonzero K.

Blocking gap: The missing theorem is a gauge-invariant nonperturbative boundary OPE/renormalization result for reflected Wilson collar products at the reflection plane. Current RG compactness controls fixed collars but does not yet prove that the connected finite boundary kernel B vanishes or is separable after all same-theory Wilson renormalizations.

## Falsifiers

- Separated-footprint falsifier: find four Wilson collar families whose boundary footprints remain a positive distance apart in the reflection plane but whose logarithmic anomaly cross-ratio K_{ik;jl} is nonzero after cutoff removal.
- Coincident-footprint falsifier: compute the reflected Wilson boundary OPE for a hairpin/cusp family and find a finite connected post-subtraction term whose four-point finite difference K does not vanish.
- Additive-contact falsifier: diagonal trace continuity holds but an off-diagonal additive contact remains; this would show the contact is not a positive OS contribution or that the same-theory diagonal locking was false.
- Topology falsifier: the RG cutoff-removal topology gives convergence of individual Wilson loops but not of the reflected products S(\Theta W(T_\delta C_i)W(T_\delta D_j)), so the fixed-collar matrix N is not a valid limit.
- Observable-algebra falsifier: eliminating K requires adding pair-dependent boundary counterterms or changing Wilson-loop renormalization at t=0; then positivity may hold, but not for the intended same theory.

## Learning

Cycle 187 isolates a sharper invariant-preservation mechanism. One-body Wilson boundary renormalizations are harmless because they are diagonal congruences; additive positive contacts vanish once diagonal trace continuity is valid; and separated boundary footprints should have no connected anomaly by locality. Therefore the entire same-theory OS obstruction is the connected coincident-footprint Wilson boundary OPE, measured by the logarithmic cross-ratio K. A nonzero K is a genuine falsifier, while K=0 on a dense Wilson core would promote the reflection-positivity closed-cone bridge from formal topology to a real Yang-Mills continuum passage lemma.

## Next Experiment

Compute the leading-order reflected Wilson collar cross-ratio for four mirror-smooth hairpin loops with the same boundary point but varied tangent/curvature, after subtracting perimeter and cusp one-body terms. In parallel, prove the easier separated-footprint estimate B=0 using locality of the regulated covariance/RG kernel to certify the first nontrivial valid subcore.
