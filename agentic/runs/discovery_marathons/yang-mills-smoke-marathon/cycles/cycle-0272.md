# cycle-0272

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Post-H,K endpoint source-interval gate

## Candidate Lemma

For the already computed finite three-hairpin H,K block, the remaining connected boundary-OPE polarization can be represented by same-theory heat-kernel endpoint source derivatives. After Wick-square Gram positivity and straight f f incidence cancellation, the corrected null scalar is certified by a clipped endpoint interval. This is a finite post-H,K Wilson calculation, not a Clay mass gap claim.

## Definitions

- source object: cutoff heat-kernel plaquette-sheet endpoint carrier E_a=(V_partial,Z_v,L_{v,i},[beta_v^-,beta_v^+],[d_v^-,d_v^+],tau) extracted from the same regulated reflected Wilson hairpin block.
- target object: the finite corrected Schur-Feshbach null scalar I_gate for the fixed three-hairpin H,K block, with the positive Gaussian margin denoted M_G.
- controlled interface: source differentiation of log Z_v, endpoint incidence contraction, color multiplication by C_N, clipping, and tail addition recover the post-H,K boundary-OPE polarization entering I_gate.
- same-theory condition: the Wilson loops, heat-kernel regulator, reflection map, normalization, and endpoint collapse are identical before and after carrier extraction; no boundary counterterm or changed test algebra is allowed.
- bridge/carrier: the carrier is local endpoint source data, not symbolic R; equivalent carriers must have identical regulated source derivatives and identical endpoint incidence maps.
- hard gate changed: success promotes this finite post-H,K reflected-Wilson OS transfer block; failure gives a finite same-theory falsifier. Continuum existence, full OS/Wightman reconstruction, nontriviality, and Hamiltonian mass gap remain untouched.
- conceptual pressure: endpoint collapse must be sign-certified while preserving collar OS positivity and the unchanged gauge-invariant Wilson algebra.
- declarative tension: collar positivity, same Wilson observables, and singular endpoint OPE must jointly hold, but raw R is representation-limited and a raw kappa4 spectrum is too strong because it forgets null incidence signs.

## Assumptions

- Model/regime: SU(N) Yang-Mills in finite volume with heat-kernel plaquette-sheet regulator at cutoff a, using fundamental Wilson traces and reflection-positive collar construction.
- Uniformity: endpoint boxes have source-analytic log partition functions in a cutoff-independent disk for the chosen finite hairpin geometry, with eighth-derivative bound M_{8,v}.
- Same-theory condition: endpoint source derivatives are taken inside the original regulated Wilson observable, not in a boundary-renormalized or algebra-enlarged theory.
- Finite evidence boundary: H,K, the null vector, and M_G are treated as already fixed finite-route data; no continuum limit or mass gap inference is made.
- Cancellation assumptions: connected logarithms remove Wick-square disconnected pieces, and the straight C_A f f contact cancels under the previously verified null-incidence identity.
- Tail control: all non-endpoint overlap, corner leakage, and large-field/topological residues are charged to a signed interval T_tail subset [-tau,tau] uniformly in the cutoff range.

## Equations

- endpoint mixed Wilson cumulant defining R: `R_{ij}^{\partial}=C_N\sum_{v\in V_{\partial}}\left.\partial_{s_i}^2\partial_{s_j}^2\log Z_v\left(\sum_k s_kL_{v,k}\right)\right|_{s=0}+T_{ij}^{\partial},\quad C_N=\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Valid when the heat-kernel endpoint boxes are disjoint after locality extraction and the fundamental Wilson trace expansion is taken in the same regulated theory.
- seven point endpoint source stencil: `\kappa_{4,v}^{\mathrm{sing}}(L_v)=\left.\partial_s^4\log Z_v(sL_v)\right|_{0}=h^{-4}\sum_{r=-3}^{3}c_r\log Z_v(rhL_v)+\epsilon_{v,h},\quad c_0=28/3,\ c_{\pm1}=-13/2,\ c_{\pm2}=2,\ c_{\pm3}=-1/6,\ |\epsilon_{v,h}|\le 7h^4M_{8,v}/240`. Valid when: Valid when log Z_v is eight times source differentiable on the whole stencil segment and the same endpoint box is used at all source values.
- null endpoint dominance: `D_v=2G_{12}(v)-4G_{13}(v)-4G_{23}(v),\quad G_{ij}(v)=\langle L_{v,i},L_{v,j}\rangle_{\mathrm{sing}}`. Valid when: Valid after the post-H,K null vector has been fixed and the endpoint source directions L_{v,i} use the locked reflected Wilson geometry.
- interval product carrier: `\kappa_{4,v}^{\mathrm{sing}}\in[-\beta_v^+,-\beta_v^-],\quad D_v\in[d_v^-,d_v^+],\quad J_v=\left[\min_{\beta\in\{\beta_v^-,\beta_v^+\},d\in\{d_v^-,d_v^+\}}(-\beta d),\max_{\beta\in\{\beta_v^-,\beta_v^+\},d\in\{d_v^-,d_v^+\}}(-\beta d)\right]`. Valid when: Valid when the endpoint fourth cumulant is certified nonpositive on the scalar source line and the incidence interval encloses all cutoff representatives.
- finite gate interval: `I_{\mathrm{gate}}\in M_G+C_N\sum_{v\in V_{\partial}}J_v+[-\tau,\tau],\quad I_{\mathrm{gate}}^-\ge M_G-C_N\sum_v\beta_v^+[d_v^+]_+-\tau`. Valid when: Valid when all residual corner, topology, and large-field endpoint leakage is included in T_tail and no boundary counterterm is introduced.
- promotion and falsifier criterion: `I_{\mathrm{gate}}^->0\Rightarrow \text{finite null channel promoted},\qquad I_{\mathrm{gate}}^+<0\Rightarrow \text{finite OS falsifier}`. Valid when: Valid only for this finite post-H,K block and only after the source carrier has recovered the same regulated Wilson cumulant.

## Attempted Derivation

- Freeze claim level: this cycle targets only the finite post-H,K reflected-Wilson OS transfer gate; the Clay continuum, OS/Wightman, nontriviality, and mass-gap gates remain untouched.
- Replace symbolic R by the same-theory endpoint carrier E_a: endpoint boxes, source partition functions, source directions L_{v,i}, incidence intervals, color factor C_N, and tail interval.
- Write R_{ij}^{partial} as a mixed fourth source derivative of log Z_v. This is the actual connected Wilson cumulant; the connected logarithm removes disconnected Wick-square contractions.
- Use the verified null-incidence cancellation to remove straight C_A f f contacts. The only local term left in the null scalar is the endpoint fourth cumulant multiplied by D_v.
- Use the heat-kernel Haar-Jacobian expansion to compute the leading compact-group contribution: it is negative along a scalar source line and bounded by d_A C_A^2 t_v^4 ||Y||^4/120 plus a remainder.
- Convert kappa4 and D_v into an interval product J_v. The lower bound shows the sharp obstruction: only positive endpoint dominance [d_v^+]_+ can turn negative kappa4 into a dangerous term.
- Route the result through timeline-definition-assumption-elicitor: missing definitions are now actual endpoint incidence values, source-stencil intervals, beta remainders, and cutoff-uniform tail bounds.

Blocking gap: The actual three-hairpin endpoint incidence table G_{ij}(v), the numerical or symbolic source-stencil intervals for log Z_v, and the cutoff-uniform tail tau have not yet been evaluated.

## Falsifiers

- Finite falsifier: certified source intervals give I_gate^+<0 for the post-H,K null channel.
- Same-theory falsifier: matching the endpoint carrier requires a boundary counterterm, changed Wilson-loop normalization, or enlarged boundary observable algebra.
- Uniformity falsifier: the M8 stencil bound or T_tail grows as the cutoff is removed, so the finite estimate cannot support any later RG-to-OS transfer.
- Geometry falsifier: the actual endpoint incidence table has large positive 12-only dominance D_v>0 at enough endpoints to overwhelm M_G.
- Representation falsifier: two carriers with identical symbolic R but different regulated source derivatives produce different gate intervals, proving symbolic R is invalid as the proof object.

## Learning

The sharp local value signal is that the dangerous object is not negative kappa4 itself but negative kappa4 times certified positive null endpoint dominance plus tail. The efficient representation is endpoint source intervals: encode endpoint boxes, L_v source stencils, beta intervals, G/D incidence, C_N, and tau; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; use source differentiation, interval arithmetic, color multiplication, clipping, and tail addition; identify carriers only by equal regulated source derivatives; keep locality finite by charging leftovers to T_tail; transfer only I_gate to the finite OS gate. Compared with the global Schur-preimage route this is local after H,K; compared with formal OPE language it is computable and has a valid falsifier.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete thought experiment now as a falsifier probe and endpoint-data rehearsal.`
- Rationale: The branch has passed the formal finite Schur-Feshbach and H,K stages; another abstract OS restatement would loop. The remaining decision is the sign and size of the connected endpoint boundary-OPE polarization in the same heat-kernel Wilson regulator.
- Situation seed: Take the fixed three-hairpin SU(N) heat-kernel plaquette-sheet block with the known post-H,K null vector and isolate four endpoint boxes: two shared only by the 12 pair, one shared by 13, one shared by 23, plus a uniform tail budget.
- Varied variable: Vary the endpoint dominance ratio eta=(sum_v G12(v))/(2 sum_v G13(v)+2 sum_v G23(v)) by sliding the 12 boundary footprints while keeping loop areas and collar width fixed.
- Held-fixed controls: Same SU(N) heat-kernel plaquette-sheet regulator and same fundamental Wilson trace normalization., The already computed H,K data, null vector, color factor C_N, and positive margin M_G., Reflection symmetry, gauge-invariant Wilson observables, and no boundary counterterms., Uniform source-stencil radius h and a fixed tail accounting rule for non-endpoint overlaps.
- Expected observation: For eta below the dominance threshold, D_v is nonpositive or small and negative kappa4 is protective or harmless; for large eta, the interval lower bound decreases and may become a finite OS falsifier if the upper endpoint interval is also negative.
- Transfer certificate needed: A certified endpoint incidence table, same-theory source derivative intervals for each Z_v, a cutoff-uniform M8 and T_tail bound, and a recovery proof that their sum equals the regulated connected Wilson cumulant entering the finite Schur-Feshbach scalar.

## Next Experiment

Compute the actual V_partial incidence table for the first three-hairpin block, form D_v intervals, evaluate seven same-theory log Z_v(rhL_v) source values or analytic bounds, assemble I_gate, and decide promotion or finite falsifier.

# Post-H,K endpoint-box R/kappa_4 Ward-majorant enclosure

## Candidate Lemma

Endpoint-moment Ward-majorant lemma: for the actual flowed Wilson hairpin covariance, after disconnected, perimeter/cusp, and longitudinal Ward subtractions, the connected boundary-OPE polarization in the plus endpoint box is bounded by second endpoint moments. If the H,K plus endpoint currents have zero monopole and dipole moments, the normalized connected polarization is O(eta^2), giving a valid finite lower interval for R_{++}/kappa_4.

## Definitions

- source object: same-theory gradient-flow regulated SU(N) Yang-Mills Wilson hairpin family at finite volume, cutoff a, flow time t, point splitting epsilon, and endpoint boxes B_i.
- target object: finite post-H,K endpoint-box scalar R_{++}/kappa_4 entering the plus-channel Schur-Feshbach positivity test, not the continuum mass gap.
- controlled interface: sheet-current/endpoint-current representation mapping each hairpin to flowed curvature cumulants with Ward-subtracted cell kernels and explicit color factors.
- same-theory condition: all limits, renormalizations, recovery maps, and Wilson observables come from the Schwinger family intended for OS reconstruction; no auxiliary Gaussian theory is substituted.
- carrier: oriented sheet currents J_i and endpoint currents e_i encode the H,K hairpins; raw Wilson contours are too fragmented for Ward cancellation and interval arithmetic.
- observable: X_i^ren is the centered cusp/perimeter-renormalized flowed Wilson hairpin; R_{++} is kappa_2(X_1^ren,X_2^ren).
- regulator: Wilson plaquette cutoff or equivalent gauge-invariant cutoff plus Yang-Mills gradient flow, with a^2 << t << d^2 and rho/d=eta.
- preserved invariants: gauge invariance, color contraction, reflection plus-channel symmetry, sheet orientation, endpoint locality, and same-theory recovery of Wilson Schwinger functions.
- hard gate changed: finite endpoint-box positivity after H,K; Clay continuum construction, OS/Wightman axioms, nontriviality, and Hamiltonian mass gap remain untouched.

## Assumptions

- Model/regime: SU(N) Yang-Mills at finite cutoff and finite volume, with gradient flow time t, point splitting epsilon, endpoint box radius rho, and endpoint separation d.
- Uniformity condition: the bound is finite-regulator valid only in a chosen flow window; volume- and cutoff-uniform basin entry is not assumed.
- Same-theory cutoff condition: Z_cusp, perimeter subtraction, and flow recovery maps are applied to the same Wilson measure that supplies the H,K observables.
- H,K condition: the collar/hairpin objects and the plus-channel vector have already been extracted, with Schur-Feshbach leakage scalar L_+ fixed.
- Endpoint symmetry condition: the plus-channel endpoint currents are reflected and centered so that their zeroth and first endpoint moments vanish inside each endpoint box.
- Ward-kernel condition: each connected four-curvature sector K_4^W in I_3g, I_4g, I_ct, and I_end has a cellwise C^2 interval majorant away from coincident endpoints.
- Error budget: Delta_cell, Delta_flow, and E_{>=6} bound quadrature width, flow-window drift, and higher Wilson-sheet expansion terms in the same theory.
- Frontier condition: large-field summability, topology control across RG steps, regulator-independent continuum Schwinger functions, OS positivity, observable density, and spectral transfer are not discharged.

## Equations

- renormalized hairpin observable: `X_i^{\rm ren}=Z_{\rm cusp}^{-1}(t,\epsilon)\left(N^{-1}{\rm Tr}\,U_t(\Gamma_i)-\left\langle N^{-1}{\rm Tr}\,U_t(\Gamma_i)\right\rangle\right)`. Valid when: Valid when the finite-cutoff flowed Wilson loop is point-split and the same cusp/perimeter renormalization is used for both hairpins.
- endpoint R cumulant: `R_{++}^{\rm ren}(t,\epsilon)=\kappa_2\left(X_1^{\rm ren},X_2^{\rm ren}\right)`. Valid when: Valid when the two centered hairpins are the H,K plus-channel endpoint-box observables in the same regulated Yang-Mills measure.
- pair plus connected decomposition: `\frac{R_{++}^{\rm ren}}{\kappa_4}=2(N^2-1){\mathcal G}_{++}+N(N^2-1){\mathcal G}_{++}\Xi_{++}^{W}+E_{\ge 6}`. Valid when: Applies after diagonal Wilson normalization, disconnected-product subtraction, and one-hairpin perimeter/cusp subtraction in the thin-sheet expansion.
- plus-channel endpoint moment cancellation: `\int_{B_i}e_i(\xi)\,d\xi=0,\qquad \int_{B_i}\xi_\alpha e_i(\xi)\,d\xi=0`. Valid when: Requires the H,K plus-channel endpoint currents to be reflection-symmetrized inside each endpoint box before Ward subtraction.
- Ward-subtracted endpoint Taylor bound: `\left|\int e_1(\xi)e_2(\zeta)K_4^W(z+\xi-\zeta)\,d\xi d\zeta\right|\le \frac12 M_2(e_1,e_2)\sup_{\Omega_{12}}\|D^2K_4^W\|`. Valid when: Valid when endpoint boxes are disjoint, the Ward-subtracted kernel is C^2 on their separation cell, and zero/first moments vanish.
- normalized polarization majorant: `|\Xi_{++}^{W}|\le C_W(t,d,N)\eta^2+\Delta_{\rm cell}+\Delta_{\rm flow},\qquad \eta=\rho/d`. Valid when: Applies when second endpoint moments scale like rho squared and the cell majorant controls every Ward-subtracted sector.
- finite promotion inequality: `(N^2-1){\mathcal G}_{++}\left[2-N\left(C_W\eta^2+\Delta_{\rm cell}+\Delta_{\rm flow}\right)\right]-|E_{\ge6}|>L_+`. Valid when: Valid as a finite Schur-Feshbach promotion test after H,K and the leakage scalar L_+ have been fixed.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: same-theory gradient-flow regulated SU(N) Yang-Mills Wilson hairpin family at finite volume, cutoff a, flow time t, point splitting epsilon, and endpoint boxes B_i.; target object: finite post-H,K endpoint-box scalar R_{++}/kappa_4 entering the plus-channel Schur-Feshbach positivity test, not the continuum mass gap.; Model/regime: SU(N) Yang-Mills at finite cutoff and finite volume, with gradient flow time t, point splitting epsilon, endpoint box radius rho, and endpoint separation d..
- Conceptual pressure attacked: finite Schur-Feshbach positivity requires a same-theory endpoint mediator, but pair positivity and gradient-flow renormalization do not control the connected four-curvature polarization C4.
- Critical carrier revision: raw Wilson contours are representation-limited and fragmented; sheet currents plus endpoint currents encode gauge/color/reflection/orientation invariants and make Ward subtraction, endpoint moments, heat-kernel majorants, and interval arithmetic primitive.
- Compared abstraction: a global non-Gaussian OS witness is too weakly targeted for this obstruction, while a finite endpoint-current interval route directly tests the post-H,K endpoint-box gate.
- Expand each centered renormalized flowed hairpin to the first nontrivial sheet-curvature order; centering removes the disconnected product and one-hairpin perimeter/cusp subtraction removes local self terms.
- Compute the cross-pair Wilson contraction: two cross pairings of flowed two-curvature propagators give the explicit positive factor 2(N^2-1)G_{++}.
- Project the remaining connected four-curvature cumulant onto the same sheet currents; the one-loop color projector is N(N^2-1), absorbed into G_{++}Xi_{++}^W.
- Apply Ward identities to longitudinal pieces of the flowed curvature kernel; after cusp subtraction only endpoint-current terms in the endpoint boxes remain.
- Use plus-channel reflection centering: endpoint monopole and dipole moments vanish, so Taylor expansion of K_4^W about the endpoint separation z has no zeroth or first contribution.
- Bound the residual by the Hessian of the Ward-subtracted kernel on the separation cell, giving |Xi_{++}^W| <= C_W eta^2 + Delta_cell + Delta_flow.
- Insert this lower bound into the finite Schur-Feshbach inequality. Success promotes endpoint-box positivity after H,K; failure is a falsifier for the R repair.

Blocking gap: The C^2 interval majorants for K_4^W in sectors I_3g, I_4g, I_ct, and I_end have not been certified for the actual H,K geometry, and E_{>=6} lacks a same-theory numerical enclosure.

## Falsifiers

- falsifier: the extracted H,K plus endpoint currents have a nonzero first moment, producing O(eta) rather than O(eta^2) polarization.
- falsifier: cusp/perimeter subtraction leaves a local endpoint contact term not absorbed by Z_cusp in the same theory.
- falsifier: an interval enclosure gives N(C_W eta^2+Delta_cell+Delta_flow)>=2 before beating L_+.
- falsifier: the positive pair geometry G_{++} vanishes or is too small for the endpoint boxes actually supplied by H,K.
- falsifier: the flow-window plateau is absent, so R_{++}^{ren} changes sign or size under admissible t variation.
- falsifier: the Ward-subtracted K_4^W sector is not C^2 on the chosen cells because endpoint boxes overlap or topology sectors introduce unsummed singular tails.
- falsifier: the R cumulant is computed in a different regulator, volume, or observable algebra from the Schur-Feshbach H,K data.

## Learning

The cycle attacks the conceptual pressure that finite Feshbach positivity needs an endpoint mediator in the same Wilson theory, while positive pair covariance alone leaves C4 uncontrolled. The sharp new value signal is the endpoint-moment mechanism: after Ward and cusp cancellation, plus-channel monopole/dipole cancellation converts the dangerous connected boundary-OPE term into a Hessian-controlled O(eta^2) interval problem. This is route-changing only locally: success promotes finite endpoint-box positivity after H,K; failure quarantines the R repair; the Clay gates for continuum existence, OS/Wightman axioms, nontriviality, and positive Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide.`
- Rationale: The branch no longer needs another Wilson/OS obstruction restatement; the missing mediator is the sign and size of the connected endpoint polarization after H,K. Varying one geometric small parameter tests whether the proposed Ward-moment eta^2 suppression is real enough to beat L_+.
- Situation seed: Finite SU(3) Wilson plaquette Yang-Mills on a four-torus with gradient flow; insert the already extracted H,K plus-channel thin hairpin sheets into two endpoint boxes, compute kappa_2 of centered cusp-renormalized flowed Wilson hairpins, and decompose it into pair, I_3g, I_4g, I_ct, and I_end sectors.
- Varied variable: eta=rho/d, the endpoint-box radius divided by endpoint separation, with flow ratio sqrt(8t)/d kept inside a fixed plateau window.
- Held-fixed controls: Gauge group SU(3), Wilson regulator, finite volume shape, and boundary conditions., The H,K sheet geometry, plus-channel reflection normalization, and Schur-Feshbach leakage scalar L_+., The same cusp/perimeter renormalization, gradient-flow recovery map, and Wilson observable algebra., The cell partition symmetry used to enforce endpoint monopole and dipole cancellation.
- Expected observation: If the Ward-moment mechanism is correct, the interval for Xi_{++}^W divided by eta^2 remains bounded while the pair baseline stays positive; a persistent O(eta) term or a negative interval large enough to violate the promotion inequality demotes the branch.
- Transfer certificate needed: A same-theory interval proof of the Ward-subtracted Hessian bounds and truncation errors, stable over the admissible flow window and compatible with the H,K normalization; only after that may the finite endpoint-box proof obligation be updated.

## Next Experiment

Build the actual H,K sheet/endpoint-current file, verify plus-channel endpoint moment cancellation, interval-evaluate G_{++} and the Hessian majorants for I_3g, I_4g, I_ct, and I_end over eta cells, then test the lower bound against L_+.

# Post-H,K endpoint-box kappa4 shell certificate for reflected Wilson Route A

## Candidate Lemma

Finite same-regulator endpoint-box certificate. Let V_E be the first post-H,K endpoint coefficient space. If the heat-kernel Wilson boundary-OPE polarization decomposes as R_sigma=R^G_sigma+g_R^4 kappa_{4,sigma}/(16N^2)+E^OPE_sigma and the certified intervals satisfy gamma_sigma:=m_G-g_R^4 B_4/(16N^2)-e_OPE-s_HK>0, then the Schur-corrected endpoint quadratic form Delta_sigma is positive on V_E. This changes only the finite Route A endpoint-box positivity gate; it does not prove OS reconstruction, continuum existence, or the Hamiltonian mass gap.

## Definitions

- source object: finite-volume cutoff SU(N) Yang-Mills with heat-kernel smearing scale sigma, Wilson endpoint sheets, transported curvature fluxes, and known finite H,K collar/hairpin data.
- target object: the finite quadratic form Delta_sigma on the endpoint coefficient space V_E after Schur-Feshbach subtraction of the H,K hairpin block.
- controlled interface: sheet-kernel hypergraph encoding sheets, weights, heat-kernel transporters, color tensors, shell labels, OPE errors, multiplicities, and Schur data.
- same-theory condition: the cutoff action, heat-kernel regulator, reflection plane, coupling normalization, Wilson normalization, H,K matrices, kappa4 cumulant, and OPE remainder are all computed before any continuum or spectral transfer.

## Assumptions

- Model: finite cutoff SU(N) Yang-Mills on a reflection-positive box or torus with heat-kernel curvature smearing sigma >= c a and finite endpoint support.
- Regime: V_E is finite, the Wilson boundary OPE is used only through fourth curvature order, and all remainder terms are bounded in the same regulator.
- Uniformity: no volume- or cutoff-uniform statement is assumed; the lemma is a restricted finite certificate.
- Hairpin condition: QHQ on the eliminated H,K sector is strictly positive with a certified inverse interval, giving S_HK=B^*E^{-1}B.
- Cumulant condition: the compressed connected four-curvature cumulant kappa_{4,sigma} has a shell row-sum envelope B_4 valid for the chosen endpoint sheets.
- Naturalness condition: quotienting of sheets is allowed only by gauge-invariant Wilson trace identities and reflection-preserving sheet symmetries.
- Same-theory boundary: R_sigma, S_HK, and E^OPE_sigma are not imported from different regulators, gauges, or normalizations.

## Equations

- transported flux covariance: `C_{pq,\sigma}=\left\langle \Phi_p^a\Phi_q^a\right\rangle_c,\quad \Phi_p^a=\int_{\Sigma_p} h_\sigma(x_p,x)\,\mathrm{Ad}_{U_{x\to x_0}}F_{\mu\nu}^a(x)\,dS^{\mu\nu}`. Valid when: Valid when heat-kernel smearing, parallel transport paths, and trace normalization are fixed in the same cutoff theory.
- Gaussian endpoint polarization: `(R^G_\sigma)_{ij}=\alpha_N g_R^4\sum_{p\in i}\sum_{q\in j} w_{ip}w_{jq}\,C_{pq,\sigma}^2,\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when the boundary OPE is truncated at fourth curvature order and disconnected vacuum/perimeter factors have been cancelled.
- connected four-curvature shell envelope: `M_4^-(\sigma)\le \|\kappa_{4,\sigma}\|\le B_4(\rho)+T_4(\rho),\quad B_4(\rho)=\max_i\sum_j |(\kappa_{4,\sigma}^{\le \rho})_{ij}|`. Valid when: Applies after endpoint compression to a finite sheet set with a certified shell tail T_4(rho).
- Schur-corrected endpoint form: `\Delta_\sigma=R^G_\sigma+\frac{g_R^4}{16N^2}\kappa_{4,\sigma}+E^{\mathrm{OPE}}_\sigma-S_{HK},\quad S_{HK}=B^*E^{-1}B`. Valid when: Requires H,K Schur data, the R decomposition, and OPE error intervals to use identical regulator and Wilson normalization.
- promotion margin: `\lambda_{\min}(\Delta_\sigma)\ge m_G-\frac{g_R^4}{16N^2}B_4-e_{\mathrm{OPE}}-s_{HK}=\gamma_\sigma`. Valid when: Valid when m_G, B_4, e_OPE, and s_HK are rigorous intervals in the finite endpoint space.

## Attempted Derivation

- Conceptual pressure attacked: the branch needs a mediator from actual connected Wilson cumulants to Schur-corrected endpoint positivity, not another OS observable-density restatement.
- Declarative tension: Wilson/OPE coefficients, connected kappa4 negativity, and S_HK must be simultaneously valid in one cutoff theory, while the result must remain a finite Wilson calculation and not claim the Clay theorem.
- Current carrier audit: scalar R is too weak and representation-limited; full OS density is too strong and circular for this local gate; raw plaquette enumeration is fragmented. The sheet-kernel hypergraph is retained because it preserves color, locality, transporters, cumulant cancellations, OPE errors, and Schur data.
- Define transported fluxes Phi_p by heat-kernel smearing of curvature over endpoint sheets and parallel transport to fixed basepoints; this preserves gauge-invariant Wilson traces after color contraction.
- Expand vacuum/perimeter-normalized endpoint Wilson observables to fourth curvature order. Disconnected vacuum and perimeter terms cancel before endpoint compression, leaving crossed two-curvature contractions plus the connected four-curvature cumulant.
- Compute the crossed Gaussian color factor with normalized fundamental trace, giving alpha_N=(N^2-1)/(8N^2), so R^G_sigma=alpha_N g_R^4(C_sigma o C_sigma) on the endpoint sheet lift.
- Compress the connected four-curvature cumulant to V_E and split it by shell radius rho. Gershgorin gives M4^- <= ||kappa4|| <= B4(rho)+T4(rho).
- Insert the finite Schur-Feshbach correction S_HK=B^*E^{-1}B and apply Weyl's inequality to obtain lambda_min(Delta_sigma)>=m_G-g_R^4B4/(16N^2)-e_OPE-s_HK.
- Hard gate: gamma_sigma>0 promotes the finite endpoint-box positivity certificate; gamma_sigma<=0 or a negative endpoint vector demotes the Wilson collar/hairpin route for this geometry.

Blocking gap: The missing proof object is a certified same-regulator bound for the first connected four-curvature shell envelope B_4(rho) and tail T_4(rho), with the actual H,K endpoint geometry and OPE error intervals inserted.

## Falsifiers

- A same-regulator endpoint vector c with c^*Delta_sigma c<0 is a decisive falsifier for this finite Route A endpoint geometry.
- If B_4 exceeds 16N^2(m_G-e_OPE-s_HK)/g_R^4, the row-sum certificate cannot promote without a sharper operator or sign-cancellation estimate.
- If the connected four-curvature cumulant has a long shell tail T_4(rho) that is not summable at fixed sigma/a, the sheet-kernel interval is invalid.
- If vacuum/perimeter cancellation changes under the chosen Wilson normalization, the R decomposition is not same-theory valid.
- If quotienting identifies sheets with different color tensors or reflection orientations, the hypergraph carrier is representation-invalid.
- If QHQ has spectrum near zero, S_HK is uncontrolled and the Schur subtraction can dominate the positive Gaussian term.

## Learning

Cycle 272 converts the repeated Delta_sigma aspiration into a finite same-regulator inequality with named inputs: PSD Gaussian color square, connected kappa4 shell envelope, OPE error, and Schur hairpin subtraction. The conceptual value signal is sharp and route-changing at finite scope because success proves only endpoint-box positivity for the worked Wilson H,K geometry, while failure gives a concrete falsifier. The larger Yang-Mills Clay gates remain untouched and explicitly quarantined.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and first-shell extraction guide.`
- Rationale: The branch has repeatedly named Delta_sigma; it now needs a concrete same-regulator shell computation to avoid abstraction-only looping and to test whether kappa4 can overwhelm the Gaussian color square after Schur subtraction.
- Situation seed: Finite heat-kernel regulated SU(N) endpoint box containing the first known H,K collar/hairpin sheets adjacent to a reflection plane; compute the compressed connected four-curvature cumulant between two boundary plaquette sheets using the same Wilson normalization that defines S_HK.
- Varied variable: Shell cutoff rho/sigma for the kappa4 plaquette-sheet separation envelope.
- Held-fixed controls: Gauge group SU(N), fundamental trace normalization, and renormalized coupling g_R(sigma)., Same cutoff action, heat-kernel smearing scale sigma, reflection plane, Wilson endpoint basis, and H,K Schur data., Vacuum/perimeter-normalized Wilson observables and the fourth-order boundary OPE truncation., Finite endpoint coefficient space V_E; no continuum or Hamiltonian spectral transfer is allowed.
- Expected observation: If the first shell already gives B_4 large enough to make gamma_sigma<=0, the route is probably false for this geometry; if B_4 is small and the tail decreases by shell geometry, Delta_sigma may obtain a finite positive interval.
- Transfer certificate needed: A signed interval evaluation of kappa_{4,sigma}^{<=rho}, a rigorous tail bound T_4(rho), an OPE remainder bound e_OPE, and verification that all are computed in the same regulator and endpoint compression as S_HK.

## Next Experiment

Instantiate the first H,K endpoint box as a sheet-kernel hypergraph, compute the shell-0 and shell-1 connected four-curvature cumulant intervals with heat-kernel regulator, then evaluate gamma_sigma=m_G-g_R^4B_4/(16N^2)-e_OPE-s_HK.

