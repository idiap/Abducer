# cycle-0336

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: quarantined endpoint-source interval gate

## Candidate Lemma

For the fixed post-H,K three-hairpin reflected-Wilson block, the endpoint contribution to the Schur-Feshbach scalar is validly represented by a source-equivalence interval carrier C_ep. If I_gate^- >= 0 the finite block is promoted; if I_gate^+ < 0 it is a same-theory finite falsifier; otherwise the branch remains quarantined pending endpoint data.

## Definitions

- source object: heat-kernel plaquette-sheet SU(N) endpoint boxes with regulated source partition functions Z_c(s), seven-point source stencils, signed Wilson incidence numbers b_{ij,v}, color factor C_N, Gaussian margin M_G, and tail interval T_tail.
- target object: the finite post-H,K Schur-Feshbach scalar deciding OS positivity for the locked reflected-Wilson three-hairpin block, not the continuum Yang-Mills mass gap theorem.
- controlled interface: C_ep aggregates endpoint boxes only by equal regulated source data, contracts signed null-channel incidences, multiplies by connected cumulant intervals, adds M_G and T_tail, and exports a scalar interval I_gate.
- same-theory condition: the Wilson loops, source insertions, heat-kernel regulator, reflection operation, and endpoint limits are those of the same gauge-invariant lattice theory, with no boundary counterterm or algebra enlargement.

## Assumptions

- Model: finite-volume four-dimensional SU(N) lattice gauge theory with heat-kernel plaquette action and reflection-positive Wilson loop algebra.
- Regime: fixed collar thickness before collapse and fixed finite H,K three-hairpin block after the previously established null-channel cancellations.
- Cutoff: all endpoint source derivatives are computed at common lattice spacing a and endpoint box scale t_v with a regulator-independent tail budget stated separately.
- Same-theory: source-equivalent classes are identified only by equality of regulated Z_c(s) data, not by geometric similarity or a new boundary theory.
- Uniformity: T_tail and the finite-difference derivative bound are uniform over the endpoint classes used in the finite block.
- Validity: the statement is a restricted finite witness theorem and makes no continuum, observable-density, OS spectral-transfer, or mass-gap claim.

## Equations

- source-class-incidence: `D_c=\sum_{v\in c}\bigl(2b_{12,v}-4b_{13,v}-4b_{23,v}\bigr)`. Valid when: Valid when endpoint boxes are first partitioned by equal regulated source data and only then signed incidences are aggregated.
- seven-point-connected-cumulant-stencil: `\widehat\kappa_c(h)=\frac{1}{6h^4}\sum_{\ell=-3}^{3}(1,-12,39,-56,39,-12,1)_\ell\,\log Z_c(\ell h)`. Valid when: Valid when the heat-kernel endpoint source partition function is analytic for the seven real source values used in the stencil.
- certified-cumulant-interval: `\mathcal K_c(h)=\left[\widehat\kappa_c(h)-\frac{7h^4}{240}M_{8,c},\ \widehat\kappa_c(h)+\frac{7h^4}{240}M_{8,c}\right]`. Valid when: Applies after the eighth-source-derivative bound is uniform on the closed stencil interval around the origin.
- endpoint-gate-interval: `I_{\rm gate}=M_G+C_N\sum_c {\rm IntMul}(D_c,\mathcal K_c)+T_{\rm tail}`. Valid when: Requires aggregate-before-clipping source classes and validated tail intervals for all endpoint boxes touching the reflected Wilson boundary.
- decision-rule: `I_{\rm gate}^-\ge0\Rightarrow {\rm finite\ promotion},\qquad I_{\rm gate}^+<0\Rightarrow {\rm finite\ falsifier}`. Valid when: Valid only for this locked finite Wilson block after H,K cancellations and same-theory endpoint source certification.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel plaquette-sheet SU(N) endpoint boxes with regulated source partition functions Z_c(s), seven-point source stencils, signed Wilson incidence numbers b_{ij,v}, color factor C_N, Gaussian margin M_G, and tail interval T_tail.; target object: the finite post-H,K Schur-Feshbach scalar deciding OS positivity for the locked reflected-Wilson three-hairpin block, not the continuum Yang-Mills mass gap theorem.; Model: finite-volume four-dimensional SU(N) lattice gauge theory with heat-kernel plaquette action and reflection-positive Wilson loop algebra..
- Fix the heat-kernel plaquette-sheet regulator and the locked three-hairpin Wilson block after the previously computed H,K cancellations.
- Represent the post-H,K endpoint polarization by endpoint boxes v carrying Wilson incidence data b_{ij,v} and regulated source partition functions Z_v(s).
- Coarsen endpoint boxes only by equality of the regulated source data; then aggregate D_c=sum_v(2b12-4b13-4b23) before any sign clipping.
- Estimate the connected endpoint fourth cumulant kappa_c from the seven-point fourth derivative of log Z_c, with the eighth-derivative stencil error included as an interval.
- Form I_gate=M_G+C_N sum_c IntMul(D_c,K_c)+T_tail and apply the finite decision rule I_gate^- >=0, I_gate^+<0, or quarantine.
- Use the SU(N) root-quartic term only as an analytic screen: it predicts negative cumulants but does not decide the gate without positive-D leakage and tail control.

Blocking gap: Actual endpoint source values log Z_c(ell h), uniform M_8,c bounds, and a cutoff-uniform T_tail estimate are not present in branch memory.

## Falsifiers

- A source-certified class with D_c>0, K_c entirely negative, and T_tail small enough to force I_gate^+<0 is a finite same-theory falsifier.
- A nonuniform endpoint or corner tail T_tail(a) that grows under cutoff removal invalidates the finite-to-continuum use of the gate.
- A boundary counterterm needed to define Z_c(s) violates the same-theory condition even if the interval is positive.
- Two endpoint boxes aggregated by geometry but not by equal regulated source data would be a representation falsifier for C_ep.
- Failure of the heat-kernel regulator to preserve reflection positivity for the locked Wilson observables demotes the whole finite transfer.

## Learning

Conceptual pressure attacked: endpoint collapse must be sign-certified inside the same Wilson theory after H,K. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist without a boundary theory; H,K, half-overlap shielding, and root-quartic negativity still do not decide the scalar. Carrier critique: raw R is representation-limited, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. Abstraction comparison: C_ep is sharper because it encodes source classes, seven source values, cumulant intervals, signed incidences, C_N, M_G, and T_tail; preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; uses source differentiation, interval arithmetic, aggregation before clipping, color multiplication, and tail addition; identifies equivalence only by regulated source data; exports only I_gate. Hard gate: the finite post-H,K reflected-Wilson OS transfer scalar. Success promotes only this block; failure gives a finite falsifier; missing data keeps quarantine. Conceptual value signal: negative SU(N) endpoint cumulants are explanatory but not the obstruction; positive-D leakage times a connected cumulant witness plus uniform tail is the sharp finite obstruction. Clay continuum construction, gauge-invariant observable density, full OS/Wightman reconstruction, nontriviality, OS spectral transfer, and mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a validator-facing falsifier probe while the branch remains quarantined for real endpoint data.`
- Rationale: The abstract OS cone route is exhausted; the only undecided local scalar is the connected boundary-OPE endpoint term, so a concrete heat-kernel source sweep can decide or demote the finite post-H,K gate.
- Situation seed: Fixed SU(N) heat-kernel lattice endpoint-box family for the locked three-hairpin reflected-Wilson block; compute the connected cumulant witness log Z_c(ell h) for one 12-dominant endpoint class and one half-overlap protected class.
- Varied variable: The positive-D leakage fraction alpha=b12/(b13+b23+epsilon) of a single source-equivalence class.
- Held-fixed controls: Heat-kernel plaquette-sheet regulator and reflection-positive finite lattice volume., The H,K null vector, Gaussian margin M_G, color factor C_N, and Wilson loop normalization., Same-theory gauge-invariant Wilson algebra with no boundary counterterm or source redefinition., Seven-point source stencil radius h and uniform tail accounting convention.
- Expected observation: For alpha below the half-overlap shield, negative root-quartic cumulants protect or cancel; for sufficiently large alpha, a measured negative kappa interval can push I_gate below zero if the tail is small.
- Transfer certificate needed: A same-theory certificate that the source derivatives are regulated Wilson cumulants, a uniform M_8 and T_tail bound, and a proof that the endpoint class list covers all post-H,K boundary contributions.

## Next Experiment

Validator-facing connected cumulant witness computation: in the heat-kernel plaquette-sheet regulator, evaluate seven source values for each positive-D endpoint source class, certify M_8 and T_tail, form I_gate, and either promote this finite post-H,K block or keep quarantine.

# Gauge-Invariant Nontriviality Witness Selection via finite H,K endpoint Wilson cumulants

## Candidate Lemma

Conditional annular-plateau certificate: if the Ward-Hessian C4 majorants and same-theory recovery errors are interval-certified, then Delta_R^->0 promotes finite H,K endpoint-box positivity in the plus channel; Delta_R^-<=0 is a falsifier for this R repair.

## Definitions

- source object: centered gradient-flowed SU(N) Wilson hairpin endpoint sheet currents J_+^t on finite H,K endpoint cells.
- target object: finite Route A endpoint-box positivity margin Delta_R^- for the plus channel after the Schur-Feshbach H,K reduction.
- controlled interface: same-theory flowed Wilson cumulant R_{++}^{ren}=kappa_2(W_+^t,W_+^t)_c with recovery error from raw hairpins.
- same-theory condition: the flowed, centered, cusp-subtracted observables are recovered in the same lattice YM measure used for H,K.
- carrier: endpoint sheet currents with cell moments, annular sector kernels, counterterms, recovery errors, and leakage L_+.
- efficient representation: preserve gauge/color/reflection/orientation/cutoff/locality invariants; primitives are cumulants, Ward/cusp subtraction, Hessian bounds, dyadic tails, outward intervals; equivalence only certified zero-pairing currents.

## Assumptions

- Model: finite-cutoff Wilson SU(N) Yang-Mills on a reflection-symmetric lattice, with gradient flow time t>0 and endpoint point-splitting rho.
- Regime: endpoint diameter eta is below the flow radius and collar width; dyadic annuli start outside the endpoint cell.
- Cutoff: constants G^- and H_s^+ are stable on the tested a,t,rho window; no continuum basin, OS positivity, or mass-gap claim follows.
- Same-theory: raw H,K hairpins recover to centered flowed hairpins with error E_rec^+ without changing measure, boundary algebra, or coupling trajectory.
- Validity: disconnected products and one-hairpin perimeter/cusp counterterms are subtracted; plus endpoint current has zero monopole and dipole moments.
- Local: the hard gate changed is finite endpoint-box positivity after H,K; Clay existence, observable density, OS spectral transfer, and mass gap remain untouched.

## Equations

- flowed-cumulant-decomposition: `R_{++}^{ren}(t,a)=\kappa_2(\widehat W_+^t,\widehat W_+^t)_c=P_{++}(t,a)+C_{4,++}^{WS}(t,a)+E_{rec}(t,a)`. Valid when: Valid when the centered flowed hairpins and recovery map obey the Same-theory and Validity assumptions above.
- annular-Ward-Hessian-bound: `|C_{4,++}^{WS}|\le g_t^4N(N^2-1)M_{2,+}^2\sum_s H_s^+ +E_{cusp}^+,\quad \sum_{j\ge J_s}A_{s,j}\le A_{s,J_s}/(1-q_s)`. Valid when: Applies after Ward subtraction, plus-moment cancellation, and dyadic annular Hessian bounds with q_s<1.
- endpoint-dominance-margin: `\Delta_R^-:=2g_t^4(N^2-1)G_{++}^- -g_t^4N(N^2-1)M_{2,+}^2\sum_sH_s^+-E_{rec}^+-E_{cusp}^+-L_+`. Valid when: Valid in the finite H,K endpoint-box regime when all displayed intervals use outward rounding and shared cutoff data.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: centered gradient-flowed SU(N) Wilson hairpin endpoint sheet currents J_+^t on finite H,K endpoint cells.; target object: finite Route A endpoint-box positivity margin Delta_R^- for the plus channel after the Schur-Feshbach H,K reduction.; Model: finite-cutoff Wilson SU(N) Yang-Mills on a reflection-symmetric lattice, with gradient flow time t>0 and endpoint point-splitting rho..
- Recover raw H,K hairpins to centered flowed endpoint sheet currents; subtract disconnected products plus one-hairpin perimeter/cusp terms.
- Expand the Wilson cumulant into the positive pair contraction with color 2(N^2-1) and the connected four-curvature polarization with color N(N^2-1).
- Use Ward identities and plus-channel monopole/dipole cancellation to replace the endpoint C4 kernel by mixed Hessian bounds times M_{2,+}^2.
- Compress far sectors by dyadic annular ratios q_s and form Delta_R^- against Schur-Feshbach leakage L_+.

Blocking gap: No certified outward-rounded intervals yet for G_{++}^-, all H_s^+, q_s, and E_rec^+ on a common cutoff-flow plateau.

## Falsifiers

- Ward/cusp falsifier: subtraction leaves a nonzero endpoint monopole or dipole, so the Hessian eta^2 reduction is invalid.
- Annular falsifier: some q_s>=1 or the tail interval is wider than the pair baseline, forcing Delta_R^-<=0.
- Same-theory falsifier: the recovery map changes the Wilson measure or loses the H,K observable in the reconstructed algebra.
- Plateau falsifier: Delta_R^- changes sign under allowed a,t,rho refinement, so no valid cutoff-stable endpoint certificate exists.

## Learning

Declarative tension: endpoint positivity, positive pair covariance, and same-theory recovery can all be valid while C4 erases R. Raw contours are fragmented; global OS or nontriviality-witness routes are too coarse. Endpoint currents with annular intervals directly decide one finite gate.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the finite endpoint-box gate.`
- Rationale: Abstract restatement is exhausted; the branch needs a concrete cutoff-flow plateau test deciding whether C4 erases the positive pair mediator.
- Situation seed: Finite SU(N) Wilson lattice with fixed H,K hairpin endpoint boxes; evaluate centered gradient-flowed hairpin cumulants by endpoint sheet currents and annular C4 kernels.
- Varied variable: theta=eta/sqrt(8t), the endpoint-cell diameter relative to flow radius, while keeping the H,K geometry fixed.
- Held-fixed controls: Same Wilson measure, coupling trajectory, and reflection-symmetric H,K geometry., Same Ward/cusp subtraction, plus current normalization, zero-pairing equivalence, and recovery-map definition.
- Expected observation: A stable positive Delta_R^- plateau promotes finite endpoint-box positivity; a sign flip or nonpositive plateau is a valid demotion of the R repair and informs the connected cumulant witness boundary.
- Transfer certificate needed: Outward-rounded interval proof for G_{++}^-, H_s^+, q_s, E_rec^+, and Ward/cusp cancellations on the same cutoff-flow data, with no continuum or OS spectral transfer inference.

## Next Experiment

Proof search: compute outward-rounded annular intervals for G_{++}^-, H_s^+, q_s, E_rec^+ as a validator-facing connected cumulant witness boundary; promote on Delta_R^->0, quarantine on a valid nonpositive margin.

# Cycle 336 raw signed-orbit K4 stress recovery

## Candidate Lemma

Finite lemma: same-regulator signed K4 orbit intervals recover a valid two-sparse stress test for the post-H,K endpoint compression; it proves only endpoint PSD failure or forces full Delta_raw search.

## Definitions

- source object: heat-kernel regulated SU(N) lattice YM on a finite endpoint box, with Wilson endpoint sheets S_i and raw connected four-plaquette cumulant intervals I_o.
- target object: the finite Schur-corrected endpoint compression U_sigma on the post-H,K Wilson basis, with PSD or a negative Rayleigh vector as the target property.
- controlled interface: Rec_sigma maps oriented signed plaquette orbits to R_ij, D_i^+, L_ij(theta), and x_stress after OPE enclosure and H,K Schur subtraction.
- same-theory condition: identical cutoff a, smoothing sigma, coupling convention, Wilson basis, reflection plane, normal-ordering, OPE subtraction, and H,K Schur blocks.
- carrier critique: scalar R is too weak; A012 shells lose phase; OS Hilbert observable algebra is too strong and circular; signed raw orbits preserve Hermiticity and exact Wilson quotienting.

## Assumptions

- Model: finite-volume 4D SU(N) heat-kernel lattice Yang-Mills with reflected Wilson endpoint observables only.
- Cutoff: a>0 and sigma/a fixed; no volume limit, continuum limit, OS reconstruction, or gauge-invariant observable density claim is used.
- Same-theory: C_sigma, K4 orbit intervals, E_OPE, and S_HK are recovered from the same regulated measure and Wilson basis.
- Validity: quotienting is only by exact Wilson trace, orientation, reflection, and color identities; signed phases are retained.

## Equations

- signed K4 orbit recovery: `K^{(4)}_{ij}=\sum_{o\in\mathcal O_{ij}} e^{i\phi_o}m_o I_o`. Valid when: Valid when oriented plaquette quadruples are partitioned only by exact Wilson identities, with regulator and endpoint sheets fixed.
- connected boundary polarization: `R_{ij,\sigma}=\alpha_N g_R^4(C_\sigma\circ C_\sigma)_{ij}+\frac{g_R^4}{16N^2}K^{(4)}_{ij}+E^{OPE}_{ij},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid after heat-kernel smoothing, vacuum/perimeter normal-ordering, and the boundary OPE in the fixed cutoff endpoint box.
- two-sparse stress gate: `D_i^+=\overline U_{ii},\quad L_{ij}(\theta)=\underline{-\Re(e^{i\theta}U_{ij})},\quad D_i^+<0\ \text{or}\ L_{ij}(\theta)^2>D_i^+D_j^+\Rightarrow\exists x:\ x^*U^{ij}x<0`. Valid when: Applies when interval arithmetic gives Hermitian upper diagonal bounds and a phased lower off-diagonal bound for the same Schur-corrected compression.

## Attempted Derivation

- Declarative tension: Wilson/OPE data, raw K4, OPE error, and S_HK must share one cutoff, while continuum YM, OS reconstruction, excitation-sector cyclicity, and mass gap are non-claims.
- Normal-order the endpoint flux observables Q_i so vacuum and perimeter pieces cancel; the remaining R_ij is the connected cumulant witness cum_2(Q_i,Q_j).
- Decompose R into the positive Gaussian color square, signed non-Gaussian K4 orbit intervals, and OPE error, then subtract the same-basis Schur hairpin block S_HK to form U_sigma.
- Compress U_sigma to indices i,j. Certified D_i^+,D_j^+ and L_ij(theta) yield a valid negative Rayleigh falsifier if D_i^+<0 or L_ij(theta)^2>D_i^+D_j^+.

Blocking gap: No validator-facing raw same-regulator K4 signed-orbit intervals for the actual H,K endpoint sheets have been produced, so D_i^+, L_ij(theta), and the stress sign remain uncomputed.

## Falsifiers

- falsifier: exact Wilson quotienting changes a recovered phase or violates Hermiticity, so signed-orbit intervals cannot feed U_sigma.
- falsifier: OPE interval overflow makes D_i^+D_j^+ too large for any off-diagonal K4 lower bound to demote the route.
- falsifier: same-regulator K4 intervals are missing or use a different smoothing sigma, invalidating same-theory transfer.
- falsifier: all two-sparse stresses survive but full Delta_raw has a negative eigenvector outside the tested pair, forcing full matrix search.

## Learning

Cycle 336 says the only valid contribution now is raw signed-orbit interval production. The local gate changed is finite Route A endpoint PSD; volume/cutoff basin entry, continuum Schwinger functions, OS positivity, observable density, and Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe.`
- Rationale: The branch is looping on signed-stress abstraction; a concrete raw-orbit computation is needed to decide whether the finite H,K endpoint gate is killed or escalated to full Delta_raw proof search.
- Situation seed: Finite SU(N) heat-kernel lattice YM endpoint box with two H,K Wilson sheets p,q crossing the reflection collar; recover signed four-plaquette cumulant orbits for cum_2(Q_p,Q_q).
- Varied variable: Vary the smoothing ratio sigma/a while keeping the endpoint sheet geometry fixed.
- Held-fixed controls: same Wilson endpoint basis and H,K Schur blocks, same heat-kernel regulator, coupling convention, and normal-ordering, exact Wilson trace/reflection quotient policy, finite endpoint-box plaquette complexity budget
- Expected observation: A phase window where L_pq(theta)^2 exceeds D_p^+D_q^+ would give a finite falsifier; uniform survival suggests abandoning two-sparse stress for full Delta_raw.
- Transfer certificate needed: A validator-facing table of signed orbit intervals I_o, OPE error bounds, exact quotient audit, and interval arithmetic proving the resulting U_sigma entries are same-theory and Hermitian.

## Next Experiment

Proof search: compute a validator-facing connected cumulant witness for one H,K pair by enumerating signed raw K4 plaquette orbits, bounding E_OPE, forming U^{ij}, and testing D_i^+<0 or L_ij(theta)^2>D_i^+D_j^+.

