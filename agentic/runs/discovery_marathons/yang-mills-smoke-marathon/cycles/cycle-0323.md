# cycle-0323

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: endpoint-source screen for post-H,K Wilson transfer

## Candidate Lemma

Source-equivalent clipped endpoint screen: for the finite three-hairpin post-H,K gate, the connected boundary-OPE polarization is controlled by same-theory endpoint source classes before clipping; under a nonpositive root-quartic window the only lowering term is positive D-class leakage plus the uniform tail.

## Definitions

- source object: heat-kernel plaquette-sheet SU(N) endpoint boxes with locked Wilson source partition functions Z_c(s) for source-equivalent endpoint classes c.
- target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for the already computed three-hairpin block, not a continuum mass-gap assertion.
- controlled interface: C_ep, the source-equivalent endpoint carrier encoding kappa_c intervals, signed D_c incidences, color factor C_N, Gaussian margin M_G, and tau_tail.
- same-theory condition: endpoint classes are identified only by equal regulated Wilson source data in the original gauge-invariant lattice theory, with no boundary counterterm or algebra enlargement.

## Assumptions

- Model: four-dimensional lattice SU(N) Yang-Mills with heat-kernel plaquette-sheet regulator and reflection-positive finite collars.
- Regime: fixed finite H,K three-hairpin block after Wick-square Gram positivity and straight f f incidence cancellation have already been applied.
- Cutoff: endpoint boxes have size comparable to the collar cutoff and all source derivative remainders are bounded uniformly in the finite-volume/cutoff window used for the block.
- Same-theory: the source Z_c(s) is obtained by inserting the same Wilson flux source used to define the reflected Wilson observables, not by adding a boundary field theory.
- Uniformity: the tail tau_tail bounds all non-endpoint and class-coarsening errors after source-equivalence aggregation.
- Validity: kappa_c lies in a certified nonpositive interval [-A_c,0] from the SU(N) root-quartic screen or from validator-facing source stencils.
- Constraint: signed incidences are summed inside each source-equivalence class before applying [D_c]_+; clipping individual boxes first is not valid.

## Equations

- connected endpoint cumulant witness: `\kappa_c=\left.\partial_s^4\log Z_c(s)\right|_{s=0}`. Valid when: Valid when the heat-kernel endpoint box c is represented by the locked same-theory Wilson source family and the lower source moments are normalized consistently.
- signed endpoint incidence: `D_c=\sum_{v\in c}\bigl(2b_{12}(v)-4b_{13}(v)-4b_{23}(v)\bigr)`. Valid when: Valid when endpoint boxes have first been grouped by equal regulated source data and the null-channel incidence signs are preserved.
- post-HK endpoint scalar: `I_{gate}=M_G+C_N\sum_c D_c\kappa_c+T_{tail}`. Valid when: Valid when the H,K Schur-Feshbach reductions are fixed and only the connected endpoint boundary-OPE polarization remains unabsorbed.
- clipped promotion lower bound: `I_{gate}\ge I_-:=M_G-C_N\sum_c A_c[D_c]_+-\tau_{tail}`. Valid when: Valid when every source-equivalence class satisfies the certified nonpositive window \kappa_c\in[-A_c,0] and |T_tail| is at most tau_tail.
- finite gate decision: `I_-\ge0\Rightarrow \hbox{finite block promoted},\qquad I_+<0\Rightarrow \hbox{finite same\mbox{-}theory falsifier}`. Valid when: Valid when I_+ is computed by the same endpoint carrier and all source, incidence, color, and tail intervals are cutoff-uniform.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel plaquette-sheet SU(N) endpoint boxes with locked Wilson source partition functions Z_c(s) for source-equivalent endpoint classes c.; target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for the already computed three-hairpin block, not a continuum mass-gap assertion.; Model: four-dimensional lattice SU(N) Yang-Mills with heat-kernel plaquette-sheet regulator and reflection-positive finite collars..
- Start from the finite Schur-Feshbach post-H,K scalar after the three-hairpin H and K data are fixed; no continuum or spectral transfer is invoked.
- Use the heat-kernel plaquette-sheet regulator and expand the reflected Wilson collar product into endpoint boxes plus a tail.
- Apply the already established cancellations: disconnected Wick-square terms enter as positive Gram pieces, and the straight nonabelian f f contact cancels in the null incidence channel.
- Represent the remaining connected boundary-OPE polarization by kappa_c=partial_s^4 log Z_c(0) on source-equivalent endpoint classes.
- Compress equal regulated source data before clipping, giving I_gate=M_G+C_N sum_c D_c kappa_c+T_tail.
- Use the SU(N) Haar-Jacobian root-quartic expansion to certify kappa_c<=0 when the endpoint remainder is below the root-quartic cap.
- Conclude the finite promotion screen I_-=M_G-C_N sum_c A_c[D_c]_+-tau_tail; this is sharp because negative-D endpoint classes are protective rather than dangerous.

Blocking gap: The branch still lacks actual same-theory endpoint source intervals or a proof of the root-quartic remainder bound for every source-equivalence class with D_c>0 and for tau_tail uniformly in the cutoff window.

## Falsifiers

- A validator-facing source stencil giving I_+<0 is a finite same-theory falsifier for the post-H,K reflected-Wilson OS transfer scalar.
- A source-equivalence class with D_c>0 and kappa_c more negative than the root-quartic cap plus tail can demote the block.
- Failure of cutoff-uniform tau_tail control invalidates the finite promotion screen even if all local endpoint boxes look safe.
- Any boundary counterterm or changed Wilson source normalization violates the same-theory condition and demotes the bridge.
- Premature boxwise clipping before source-equivalence aggregation is a representation falsifier because it can create a false negative interval.

## Learning

Conceptual pressure attacked: endpoint collapse must be sign-certified inside the same Wilson theory after H,K. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist without a boundary theory, while raw R is representation-limited, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. Hard gate: the finite post-H,K reflected-Wilson OS transfer scalar; success promotes this one finite block, failure gives a finite same-theory falsifier, and missing source/tail data keeps quarantine. Conceptual value signal: sharp finite route change. Negative SU(N) root-quartic endpoint cumulants are explanatory but not themselves the obstruction; only positive-D leakage times same-theory connected cumulants plus uniform tail can demote the gate. Clay continuum construction, full OS/Wightman reconstruction, nontriviality, and positive mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while keeping the branch in screened quarantine until source data arrive.`
- Rationale: The branch has reduced the obstruction to a finite endpoint connected cumulant witness; another abstract OS-positivity restatement would not decide the sign of the post-H,K gate.
- Situation seed: Heat-kernel SU(N) lattice plaquette-sheet endpoint family for the fixed three-hairpin Wilson block, with endpoint classes c having fractional overlaps b12,b13,b23 and same-theory seven-point source evaluations of log Z_c(s).
- Varied variable: Endpoint leakage ratio alpha_c=(b13(c)+b23(c))/b12(c), varied through the half-overlap threshold while holding the source cumulant interval fixed.
- Held-fixed controls: Gauge group SU(N), heat-kernel regulator, reflection plane, and finite-volume collar geometry are fixed., The H,K Schur-Feshbach data, Gaussian margin M_G, color factor C_N, and null vector are fixed., Same-theory Wilson source normalization and source-equivalence policy are fixed., No boundary counterterm, no gauge fixing change, and no enlargement of the observable algebra are allowed.
- Expected observation: For alpha_c>=1/2 the incidence D_c<=0 is protective under kappa_c<=0; for alpha_c<1/2 the class becomes a possible finite falsifier only if its negative connected cumulant plus tau_tail overwhelms M_G.
- Transfer certificate needed: A cutoff-uniform interval certificate for kappa_c from seven-point source stencils or the root-quartic remainder bound, plus a uniform tau_tail estimate and equality of regulated source data within every compressed class.

## Next Experiment

Route to proof search plus validator-facing endpoint source computation: enumerate source-equivalence endpoint classes, compute the connected cumulant witness kappa_c by seven-point log Z_c stencils or root-quartic remainder bounds, aggregate D_c before clipping, certify tau_tail, and decide the finite I_gate interval.

# Gauge-Invariant Nontriviality Witness Selection: finite R++ annular certificate

## Candidate Lemma

Finite annular Ward-Hessian certificate for the connected boundary-OPE polarization. If the centered flowed plus-hairpin endpoint current has zero monopole and dipole moments, and each Ward/cusp-subtracted connected C4 sector has cutoff-uniform mixed-Hessian decay exponent nu_s>2 on far annuli, then R_{++}^{ren} has a computable lower interval. A positive dominance margin over L_+ promotes only finite endpoint-box positivity after H,K; a nonpositive margin is a falsifier for this R repair.

## Definitions

- source object: centered gradient-flow Wilson plus-hairpin cumulant R_{++}^{ren}(t,eta,a) in finite-volume SU(N) lattice Yang-Mills with endpoint boxes and H,K sheets.
- target object: finite lower interval R_{++}^{I,-} that can be compared with Schur-Feshbach leakage L_+ for endpoint-box positivity.
- controlled interface: endpoint sheet-current recovery map from renormalized thin Wilson hairpins to balanced endpoint currents, with explicit recovery error E_rec.
- same-theory condition: the pair term, connected C4 sector kernels, counterterms, and recovery map are evaluated in the same Wilson/gradient-flow regularized measure before any continuum or OS transfer.
- carrier: endpoint sheet currents J_+ with cell radius eta, second moment M_{2,+}, and certified zero-pairing quotient guards.
- C4 sectors: s in {3g,4g,ct,end} denotes triple-gluon, four-gluon, counterterm, and endpoint-renormalization kernels after disconnected-product subtraction.

## Assumptions

- Model: finite-volume reflection-compatible SU(N) Wilson plaquette lattice Yang-Mills with gradient flow time t>0 and lattice spacing a.
- Regime: a < eta < rho_0/4 and c_0 eta^2 <= t <= c_1 rho_0^2, so endpoint Taylor expansion is separated from diagonal flow singularities.
- Cutoff: Hessian constants H_{s,n}^{I,+}, A_{s,J}^{I,+}, recovery error E_rec^{I,+}, and pair interval G_{++}^{I,-} are uniform for all a <= a_0 in the finite calculation window.
- Same-theory: the centered hairpins, pair covariance, connected C4 cumulant, counterterms, and recovery map use one bare action trajectory and one flow normalization.
- Local: only endpoint boxes of the fixed H,K collar/hairpin configuration are varied; continuum existence, OS reconstruction, and Hamiltonian spectral transfer are not claimed.
- Validity: each far sector has dyadic exponent nu_s>2, hence q_s=2^{4-2nu_s}<1; otherwise the annular tail certificate is invalid.

## Equations

- flowed cumulant carrier: `R_{++}^{\mathrm{ren}}(t,\eta,a)=\kappa_2(W_{+,t,\eta,a}^{\mathrm{ren}},W_{+,t,\eta,a}^{\mathrm{ren}})`. Valid when: Valid when W_+ is the centered flowed plus-hairpin observable recovered from the fixed H,K endpoint sheets in one Wilson lattice measure.
- pair-plus-connected decomposition: `R_{++}^{\mathrm{ren}}=g_t^4\{2(N^2-1)G_{++}+N(N^2-1)\Xi_{++}\}+E_{\mathrm{rec}}+O(g_t^6)`. Valid when: Applies in the finite flow window after perimeter, cusp, and disconnected-product subtractions have been made before cutoff removal.
- plus-channel moment cancellation: `\int_{B_e}J_+(z)\,dz=0,\qquad \int_{B_e}(z-z_e)J_+(z)\,dz=0`. Valid when: Requires the reflected plus endpoint current from the H,K collar to be orientation balanced inside each endpoint cell.
- annular C4 tail: `T_{s,>J}\le M_{2,+}^2\,\frac{A_{s,J}^{I,+}}{1-q_s},\qquad q_s=2^{4-2\nu_s}<1`. Valid when: Valid when the Ward-subtracted sector Hessian has dyadic decay exponent nu_s greater than two on all far annuli.
- certified lower interval: `R_{++}^{I,-}=g_t^4\left[2(N^2-1)G_{++}^{I,-}-N(N^2-1)M_{2,+}^2\left(\sum_s H_{s,\le J}^{I,+}+\sum_s\frac{A_{s,J}^{I,+}}{1-q_s}\right)\right]-E_{\mathrm{rec}}^{I,+}-E_6^{I,+}`. Valid when: Applies after outward-rounded interval bounds are available for pair covariance, near sectors, far tails, recovery, and sixth-order remainder.
- finite endpoint promotion test: `\Delta_R:=R_{++}^{I,-}-L_+^{I,+}>0\ \Longrightarrow\ Q_{+,\mathrm{post}}^{I,-}>0`. Valid when: Valid for the finite Schur-Feshbach endpoint block with the same H,K basis and fixed positive remainder D.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, but positive flowed pair covariance and same-theory recovery can both be valid while connected C4 erases the mediator.
- Declarative tension: endpoint positivity, Wilson cumulant positivity, and recovery from raw Wilson hairpins must jointly hold; the missing mediator is a cutoff-stable Ward-Hessian annular dominance interval for R_{++}.
- Start with the regulator: finite-volume SU(N) Wilson plaquette action, gradient flow at time t, boundary endpoint point-splitting eta, and centered renormalized H,K plus-hairpin observable W_+.
- Expand the connected cumulant kappa_2(W_+,W_+) through order g_t^4 after subtracting disconnected products, one-hairpin perimeter factors, and cusp counterterms.
- The two-curvature cross-pairing gives the positive baseline 2(N^2-1)G_{++}; the connected four-curvature polarization is grouped into 3g, 4g, counterterm, and endpoint sectors with color N(N^2-1).
- Replace raw Wilson contours by endpoint sheet currents only through the recovery map; impose zero monopole, zero dipole, and certified zero-pairing quotient guards.
- On each near cell, bound the Ward/cusp-subtracted sector kernel by outward-rounded interval quadrature of its mixed Hessian against M_{2,+}^2.
- On far annuli, use heat-kernel Hessian decay to prove T_{s,n+1} <= q_s T_{s,n} with q_s=2^{4-2nu_s}<1, then sum the geometric tail from the first certified annulus.
- Assemble R_{++}^{I,-} from the positive pair interval minus near C4 intervals, far C4 tails, recovery error, and sixth-order remainder; compare Delta_R=R_{++}^{I,-}-L_+^{I,+} with zero.

Blocking gap: The proof still lacks outward-rounded numerical or analytic constants H_{s,<=J}^{I,+}, A_{s,J}^{I,+}, E_rec^{I,+}, and E_6^{I,+} for the actual H,K endpoint geometry.

## Falsifiers

- falsifier: a Ward or cusp subtraction leaves a nonintegrable endpoint singular in any C4 sector.
- falsifier: plus-channel monopole or dipole cancellation fails for the recovered endpoint current.
- falsifier: a far annulus has certified q_s>=1 or an observed interval ratio exceeding 2^{4-2nu_s}.
- falsifier: the recovery map changes the pair covariance by a nonzero interval not absorbed in E_rec.
- falsifier: R_{++}^{I,-}<=L_+^{I,+}, so the endpoint repair cannot beat Schur-Feshbach leakage.
- falsifier: the lower interval is positive only at one cutoff but has no stable flow-window plateau.
- falsifier: the computation imports a different regulator or observable family, breaking the same-theory condition.

## Learning

Cycle 323 makes the next contribution-shaped move: the connected boundary-OPE polarization R_{++}/kappa_4 is reduced to a same-theory annular Ward-Hessian interval with explicit pair color, connected C4 color, moment cancellation, geometric tail ratio, recovery errors, and a dominance margin against L_+. The hard gate is finite endpoint-box positivity after H,K. Success promotes one finite Route A gate; failure quarantines this endpoint repair. Clay existence, OS/Wightman axioms, nontriviality, gauge-invariant observable density, large-field/topology control, OS spectral transfer, and mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has already abstracted R_{++}; the next valid learning comes from a concrete annular interval stress test, not another restatement of the Wilson/OS obstruction ladder.
- Situation seed: Finite-volume SU(N) Wilson lattice Yang-Mills with the fixed reflected H,K plus-hairpin endpoint boxes, gradient-flow time t, centered flowed Wilson cumulant R_{++}, and Ward/cusp-subtracted C4 sector kernels.
- Varied variable: annular split index J, equivalently the first far radius rho_J=2^J rho_0 used to start the dyadic tail bound.
- Held-fixed controls: same bare Wilson action trajectory, same gradient-flow normalization, and same centered plus-hairpin observable, fixed H,K endpoint geometry, reflection plane, color normalization, and Schur-Feshbach leakage L_+, fixed endpoint cell radius eta, zero-pairing quotient policy, and Ward/cusp counterterm scheme
- Expected observation: As J increases, near-sector intervals widen mildly while the far-tail bound shrinks geometrically; a stable positive Delta_R plateau promotes the finite endpoint gate, while monotone negative or unstable margins demote the R repair.
- Transfer certificate needed: A cutoff-uniform, same-theory interval certificate for G_{++}^{I,-}, all H_{s,<=J}^{I,+}, all A_{s,J}^{I,+}, E_rec^{I,+}, E_6^{I,+}, and q_s<1 in the specified flow window before the intuition may enter proof obligations.

## Next Experiment

Proof search: compute outward-rounded annular constants for the actual H,K endpoint cells in the same Wilson/gradient-flow regulator, then run the same-theory nontriviality witness bookkeeping only as a validator-facing marker for the centered connected cumulant witness R_{++}; promote on Delta_R>0, otherwise quarantine the endpoint R repair.

# Signed-Orbit Raw K4 Stress Witness For The Finite H,K Endpoint Box

## Candidate Lemma

Signed-orbit recovery gives a finite same-regulator falsifier for post-H,K endpoint positivity: if certified orbit intervals imply L_{pq}(theta)^2>D_p^+D_q^+, then the Schur-corrected endpoint compression has a negative two-sparse Rayleigh vector. This changes only the finite Route A endpoint-box gate, not Clay YM existence or the mass gap.

## Definitions

- source object: finite heat-kernel regulated SU(N) lattice Yang-Mills Schwinger functional on a reflected endpoint box, with Wilson sheet observables W_i and raw plaquette curvature insertions F_r.
- target object: the 2x2 Schur-corrected endpoint compression U_{pq}=P_{pq}(R_G+R_{K4}+E_{OPE}-S_{HK})P_{pq} on two endpoint basis vectors e_p,e_q.
- controlled interface: the signed-orbit recovery map Rec_{sigma,a}^{pq,theta} sending raw connected four-plaquette cumulant intervals and exact Wilson quotient data to certified intervals for D_p^+,D_q^+,L_{pq}(theta).
- same-theory condition: all Wilson observables, heat-kernel transporters, OPE errors, kappa_4 intervals, and H,K Schur blocks are evaluated at the same cutoff a, smearing sigma, coupling convention, boundary geometry, and reflection normalization.
- carrier object: a connected cumulant witness, not an OS Hilbert observable algebra or gauge-invariant observable density claim.
- orbit data: Gamma_{pq} acts only by exact Wilson trace identities, reflection-compatible sheet symmetries, orientation reversal, and color-index relabeling preserving Hermiticity.

## Assumptions

- Model: finite-volume hypercubic heat-kernel lattice Yang-Mills with compact gauge group SU(N), fixed reflected endpoint box, and finite Wilson sheet basis.
- Cutoff: a>0 and sigma>=a are fixed before Wilson OPE expansion, plaquette transport, cumulant interval formation, and Schur subtraction.
- Same-theory: R_G, K^{(4)}, E_{OPE}, and S_{HK}=B^*E^{-1}B use the identical H,K Wilson basis and identical vacuum/perimeter normalization.
- Validity: each raw four-plaquette cumulant interval I_O encloses the connected non-Gaussian Schwinger family cumulant for every representative in its signed orbit.
- Constraint: the quotient map is admitted only if it preserves signs, multiplicities, color tensors, reflection support, and endpoint labels exactly.
- Local: no volume/cutoff-uniform basin entry, large-field summability, continuum OS positivity, excitation-sector cyclicity, or physical spectral transfer is inferred.

## Equations

- transported endpoint flux: `\Phi_i=\sum_{r\in S_i} w_{i,r}\,\operatorname{Ad}(U_{\gamma_{i,r}})^{ab}F_r^b`. Valid when: Valid when the heat-kernel cutoff, transport paths, endpoint sheets, and plaquette weights are fixed before cumulant expansion.
- raw connected polarization split: `R^{raw}_{ij}=\operatorname{cum}_2(:\Phi_i^2:,:\Phi_j^2:)=\alpha_N g_R^4(C_\sigma\circ C_\sigma)_{ij}+\frac{g_R^4}{16N^2}K^{(4)}_{ij}+E^{OPE}_{ij}`. Valid when: Applies after same-regulator vacuum and perimeter cancellations remove disconnected Wilson factors in the finite endpoint box.
- signed-orbit offdiagonal enclosure: `\operatorname{Re}(e^{-i\theta}U_{pq})\in I^{G}_{pq}(\theta)+\frac{g_R^4}{16N^2}\sum_{\mathcal O\in\Gamma_{pq}\backslash\mathfrak Q_{pq}}c^{pq}_{\mathcal O}(\theta)I_{\mathcal O}+I^{OPE}_{pq}(\theta)-I^{HK}_{pq}(\theta)`. Valid when: Requires exact Wilson quotienting and same-theory interval arithmetic for Gaussian, K4, OPE, and Schur terms.
- negative offdiagonal magnitude: `D_p^+=\sup I_{pp},\quad D_q^+=\sup I_{qq},\quad L_{pq}(\theta)=\max\{0,-\sup \operatorname{Re}(e^{-i\theta}I_{pq})\}`. Valid when: Valid when the phased offdiagonal interval is certified real-negative after Hermitian symmetrization of U_{pq}.
- two-sparse stress falsifier: `L_{pq}(\theta)^2>D_p^+D_q^+\Longrightarrow \det U_{\{p,q\}}<0\Longrightarrow \exists z\in\operatorname{span}\{e_p,e_q\}:z^*Uz<0`. Valid when: Requires nonnegative diagonal upper bounds or an already negative diagonal endpoint certificate in the same compression.

## Attempted Derivation

- Freeze the Clay claim level: the branch proves or falsifies only a finite post-H,K endpoint-box positivity statement; continuum YM existence, nontriviality, OS/Wightman reconstruction, gauge-invariant observable density, and mass gap remain non-claims.
- Use the heat-kernel cutoff to write each endpoint Wilson sheet as a transported plaquette flux expansion Phi_i plus a controlled OPE remainder.
- Apply same-theory vacuum/perimeter cancellation so cum_2(:Phi_i^2:,:Phi_j^2:) removes disconnected Wilson factors and leaves a Gaussian crossed contraction plus connected K4.
- Compress R_G+R_{K4}+E_{OPE} by the same endpoint basis used in the H,K Schur-Feshbach correction and subtract S_HK=B^*E^{-1}B.
- For a fixed endpoint pair p,q and phase theta, group raw four-plaquette cumulants into signed orbits under exact Wilson symmetries; multiply each orbit interval by its signed color-geometric coefficient c_O^{pq}(theta).
- Form interval enclosures I_pp,I_qq,I_pq for the Hermitian 2x2 compression and compute D_p^+,D_q^+,L_{pq}(theta).
- If L_{pq}(theta)^2>D_p^+D_q^+, recover the explicit stress vector z=e_p-t e^{i theta}e_q with t between L/D_q^+ and D_p^+/L and obtain z^*Uz<0.

Blocking gap: The actual same-regulator K4 signed-orbit intervals I_O have not yet been computed for the first H,K endpoint geometry; without them the theorem is only a validator-facing recovery map and negative tactic.

## Falsifiers

- A certified endpoint diagonal interval has sup I_pp<0, giving an immediate finite falsifier independent of offdiagonal phase stress.
- For some p,q,theta, signed-orbit recovery gives L_{pq}(theta)^2>D_p^+D_q^+, producing a valid two-sparse falsifier for the H,K endpoint PSD route.
- All recovered K4 intervals are too wide or sign-indefinite, so no validator can distinguish negativity from interval slack.
- The signed quotient identifies two plaquette quadruples with opposite Wilson orientation signs, invalidating the orbit aggregation.
- The OPE interval or Schur hairpin energy is computed with a different regulator, breaking the same-theory condition.
- The stress vector lies in a null quotient of the finite Wilson Gram form, so it cannot falsify the physical endpoint compression without a repaired basis.

## Learning

Conceptual pressure attacked: turn the connected boundary-OPE polarization R into an actual connected cumulant witness that can decide a finite Schur-corrected endpoint gate, rather than restating OS Hilbert observable algebra or gauge-invariant observable density. Declarative tension: Wilson/OPE coefficients, raw non-Gaussian K4 intervals, OPE error, and S_HK must all be valid in one cutoff theory, but continuum existence, excitation-sector cyclicity, and the mass gap are barred. Carrier audit: scalar R is too weak, A012 shells are convenient but quarantined, full Delta_raw search is complete but expensive, and signed-orbit K4 intervals are the sharp negative tactic. Efficient representation requirements are now explicit: encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Hermiticity, Gaussian/K4 separation, same-theory normalization, and exact Wilson quotienting; support cumulant contraction, phase interval summation, Rayleigh stress search, Loewner bounds, and Schur subtraction; use a finite endpoint-box complexity budget; transfer only through tau, Delta_raw, or x_stress; demote on negative margin, missing intervals, non-invariant quotienting, or regulator mismatch. Hard gate: L_{pq}(theta)^2>D_p^+D_q^+ gives a valid finite falsifier, while survival forces full Delta_raw proof search. Conceptual value signal: sharp and route-changing at finite scope because it unifies Gaussian color positivity, non-Gaussian K4 danger, OPE error, and Schur hairpin energy in one same-theory inequality without implying the Clay theorem.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the first H,K endpoint box.`
- Rationale: The branch is looping unless the connected boundary-OPE polarization is tested by raw same-regulator intervals rather than scalar R language or OS-density abstractions.
- Situation seed: Finite SU(N) heat-kernel lattice endpoint box with the worked H,K collar/hairpin geometry; choose the nearest offdiagonal endpoint pair p,q and recover signed orbits of raw four-plaquette K4 cumulants contributing to Re(e^{-i theta}U_pq).
- Varied variable: signed-orbit radius rho, the maximum graph distance of plaquette quadruples from the endpoint collar included before using a tail interval.
- Held-fixed controls: Heat-kernel regulator a,sigma and coupling convention., Endpoint Wilson sheets, H,K Schur blocks, and reflection normalization., Exact Wilson quotient rules and color-tensor normalization., OPE error budget and vacuum/perimeter subtraction scheme.
- Expected observation: If the first few signed orbits coherently drive the phased K4 offdiagonal negative, L_{pq}(theta)^2 may exceed D_p^+D_q^+ and demote the endpoint route; if the signal cancels or the tail dominates, the negative tactic is inconclusive and full Delta_raw proof search is required.
- Transfer certificate needed: A same-theory connected cumulant witness certificate: interval enclosures for representative K4 orbits, an invariant signed quotient audit, a rigorous omitted-orbit tail bound, and Schur/OPE intervals in the identical cutoff theory.

## Next Experiment

Proof search: compute the first same-regulator signed-orbit K4 intervals for the nearest H,K endpoint pair, assemble the connected cumulant witness intervals I_pp,I_qq,I_pq, test L_{pq}(theta)^2>D_p^+D_q^+, and quarantine the phase abstraction if no raw interval certificate is produced.

