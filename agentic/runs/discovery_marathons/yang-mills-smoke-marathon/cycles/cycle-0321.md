# cycle-0321

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint Source Interval Screen for Post-HK Wilson Gate

## Candidate Lemma

Finite Route A lemma: in the heat-kernel plaquette-sheet regulator, the post-H,K endpoint contribution is bounded from below by a clipped positive-D leakage budget. If the root-quartic cap plus uniform tail is smaller than the Gaussian Schur-Feshbach margin, this finite reflected-Wilson block is promoted; if a certified interval is negative, it is a same-theory falsifier. This attacks the conceptual pressure that endpoint collapse must be sign-certified without adding a boundary theory.

## Definitions

- source object: heat-kernel plaquette-sheet SU(N) endpoint source classes c for the three reflected Wilson hairpins, represented by F_c(s)=log Z_c(sL_c), a seven-point source stencil, fractional incidences b_{ij,c}, and a cutoff-uniform tail budget.
- target object: the finite post-H,K reflected-Wilson OS transfer scalar G_ep for this one hairpin block, not a continuum Schwinger family, nontriviality theorem, or mass-gap claim.
- controlled interface: C_ep maps same-theory endpoint connected cumulant intervals and signed incidences to an interval [I_-,I_+] for G_ep after Wick-square positivity and straight f f null-incidence cancellation.
- same-theory condition: the endpoint regulator, Wilson normalization, gauge-invariant observable algebra, reflection map, and source insertions are identical to the collar theory; no boundary counterterm or changed loop renormalization is allowed.
- declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold, while H,K and the half-overlap shield alone do not decide the scalar.
- carrier audit: raw R is representation-limited, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K; C_ep is source-equivalent, incidence-signed, and cutoff-budgeted.

## Assumptions

- Model: finite-volume SU(N) lattice Yang-Mills with heat-kernel plaquette action and fundamental Wilson hairpin observables before cutoff removal.
- Regime: endpoint boxes are small enough for a BCH endpoint chart and source parameters s in {-3h,-2h,-h,0,h,2h,3h}.
- Uniformity: eighth source derivatives, root-quartic remainders E_c, and endpoint tails tau_tail are bounded uniformly in cutoff and collar thickness for the fixed finite block.
- Same-theory: source insertions differentiate the same regulated Wilson observables used in the collar OS matrix; no boundary counterterm, quotient change, or extra observable is introduced.
- Local: H,K gates and the positive Gaussian margin M_G are already fixed for this three-hairpin block after one-body and straight f f cancellations.
- Validity: the lemma is a sufficient finite promotion screen; failure of the screen alone is not a falsifier unless the certified interval becomes negative.

## Equations

- seven_point_connected_cumulant_stencil: `\widehat\kappa_c(h)=h^{-4}\sum_{r=-3}^{3}a_r F_c(rh),\quad a_0=\frac{28}{3},\ a_{\pm1}=-\frac{13}{2},\ a_{\pm2}=2,\ a_{\pm3}=-\frac16`. Valid when: Valid when F_c has eight bounded source derivatives in the same endpoint chart.
- stencil_error: `|\widehat\kappa_c(h)-\partial_s^4F_c(0)|\le \frac{7h^4}{240}M_{8,c}`. Valid when: Valid when the seven source evaluations remain inside one heat-kernel endpoint chart.
- root_quartic_endpoint_expansion: `\kappa_c:=\partial_s^4F_c(0)=-\frac{t_c^4}{60}R_4(L_c)+E_c,\quad R_4(L)=N\operatorname{tr}L^4+3(\operatorname{tr}L^2)^2`. Valid when: Applies after heat-kernel endpoint rescaling and singlet source normalization for SU(N).
- negative_cumulant_cap: `(-\kappa_c)_+\le \beta_c:=\frac{t_c^4}{60}(N+3)\|L_c\|_2^4+|E_c|`. Valid when: Valid when L_c is traceless Hermitian and the endpoint remainder is certified.
- signed_incidence_and_shield: `D_c=2b_{12,c}-4b_{13,c}-4b_{23,c},\quad b_{13,c}+b_{23,c}\ge b_{12,c}/2\Rightarrow D_c\le0`. Valid when: Valid for the fixed null-channel incidences of this three-hairpin endpoint block.
- clipped_gate_lower_bound: `C_N=\frac{g^4}{4}(T_F/N)^2,\quad I_-:=M_G-C_N\sum_c[D_c]_+\beta_c-\tau_{\rm tail},\quad I_->0\Rightarrow G_{\rm ep}>0`. Valid when: Valid after Wick-square positivity and straight f f null-incidence cancellation are imposed.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel plaquette-sheet SU(N) endpoint source classes c for the three reflected Wilson hairpins, represented by F_c(s)=log Z_c(sL_c), a seven-point source stencil, fractional incidences b_{ij,c}, and a cutoff-uniform tail budget.; target object: the finite post-H,K reflected-Wilson OS transfer scalar G_ep for this one hairpin block, not a continuum Schwinger family, nontriviality theorem, or mass-gap claim.; Model: finite-volume SU(N) lattice Yang-Mills with heat-kernel plaquette action and fundamental Wilson hairpin observables before cutoff removal..
- Fix the heat-kernel plaquette-sheet regulator and one source-equivalence endpoint class c; write F_c(s)=log Z_c(sL_c) so the fourth source derivative is the connected four-flux cumulant.
- Use the seven-point centered stencil to estimate kappa_c with error 7h^4 M_{8,c}/240; the log removes disconnected Wick-square pieces from this cumulant channel.
- Use the SU(N) endpoint Haar-Jacobian expansion in the BCH chart to get the leading negative root-quartic term and bound R_4(L_c) by (N+3)||L_c||_2^4.
- Use the already established null-channel cancellations: one-body Wilson factors vanish, Wick-square terms are positive, and straight f f contacts cancel. The remaining sign enters through D_c=2b12-4b13-4b23.
- Clip only positive D_c, because negative D_c multiplies negative endpoint cumulants protectively. This yields the lower bound I_-=M_G-C_N sum [D_c]_+ beta_c-tau_tail.
- Apply source-equivalence compression only after verifying identical regulated source data, then export the scalar interval [I_-,I_+] to the finite OS gate.

Blocking gap: The proof still needs a cutoff-uniform BCH remainder E_c and tail tau_tail for the actual plaquette-sheet endpoint boxes, plus actual seven-source data for every positive-D class.

## Falsifiers

- A positive-D endpoint source class has a certified negative connected cumulant interval large enough that I_+<0; this is the intended finite same-theory falsifier.
- The endpoint tail tau_tail is not cutoff-uniform, so the clipped interval is not valid for the same regulated-to-continuum passage.
- The BCH endpoint chart remainder E_c grows with cutoff or endpoint refinement and invalidates the root-quartic cap.
- A boundary counterterm or changed Wilson-loop normalization is required to define the zero-collar endpoint source, breaking the same-theory condition.
- Two endpoint boxes merged by geometry have different seven-point source data, showing that the proposed compression was representation-limited.
- A stress case with alpha=(b13+b23)/b12<1/2 and large ||L||_2 produces positive-D leakage exceeding M_G before tail control.

## Learning

Conceptual pressure: endpoint collapse must be sign-certified inside the same Wilson theory. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist without a boundary theory, but H,K and half-overlap data do not decide the scalar. Carrier critique: raw R is too weak, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. The sharper abstraction is C_ep with endpoint source classes, seven source values, kappa intervals, signed incidences, C_N, M_G, and tau_tail; it preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; primitive operations are source differentiation, interval arithmetic, source-equivalence, color multiplication, clipping, incidence contraction, and tail addition; equivalence is equality of regulated source data; locality cost is tau_tail; transfer exports only [I_-,I_+]. Conceptual value signal: sharp finite route change. Negative SU(N) root-quartic endpoint cumulants are explanatory but not the obstruction; only positive-D leakage times same-theory connected cumulants plus uniform tail can demote the finite post-H,K gate. Clay continuum construction, full OS/Wightman reconstruction, nontriviality, and positive mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe and analytic screen.`
- Rationale: The branch is data-quarantined unless the endpoint carrier produces a valid finite decision. Varying endpoint leakage tests whether positive-D dominance, not negative kappa_4 alone, can demote the finite Wilson block.
- Situation seed: Finite SU(N) heat-kernel plaquette-sheet endpoint box for the three reflected Wilson hairpins after H,K reduction, with F_c(s)=log Z_c(sL_c) evaluated on the seven-point stencil and exported as a connected cumulant witness.
- Varied variable: The leakage ratio alpha_c=(b13,c+b23,c)/b12,c, with alpha_c crossing the half-overlap shield value 1/2.
- Held-fixed controls: Same heat-kernel regulator, same Wilson loops, and same reflection map as the collar OS matrix., Fixed H,K Schur-Feshbach margin M_G and fixed null vector u=(1,1,-2)., No boundary counterterm, no gauge fixing change, and no enlargement of the gauge-invariant observable algebra., Uniform source-derivative budget M_8 and endpoint tail tau_tail for the tested finite block.
- Expected observation: For alpha_c>=1/2 the endpoint class is shielded because D_c<=0. For alpha_c<1/2 the lower bound decreases by C_N(2-4alpha_c)b12,c beta_c; a certified crossing below zero would be a finite same-theory falsifier.
- Transfer certificate needed: A cutoff-uniform endpoint chart remainder, source-equivalence certificate, and tail bound are required before this finite intuition may affect the OS proof queue; no continuum or spectral transfer is inferred.

## Next Experiment

Proof search for cutoff-uniform E_c and tau_tail, then compute seven-point endpoint source stencils for every positive-D class in the heat-kernel plaquette-sheet regulator; report the connected cumulant witness interval [I_-,I_+] and either promote the finite gate, demote by falsifier, or keep quarantine.

# Gauge-Invariant Nontriviality Witness Selection via finite Route A endpoint R certificate

## Candidate Lemma

Annular Ward-Hessian tail lemma: after Ward, cusp, and plus-channel monopole/dipole cancellation, the far connected boundary-OPE polarization in R_{++}^{ren} is bounded by a dyadic geometric tail with explicit ratio q_s=2^{4-2\nu_s}.

## Definitions

- source object: centered flowed Wilson hairpin endpoint sheet current j_+ for the post-H,K plus channel, represented by endpoint boxes and oriented sheet currents.
- target object: the finite plus-channel Schur-Feshbach endpoint margin \Delta_R(J) whose positivity certifies the local endpoint-box repair.
- controlled interface: the flowed connected Wilson cumulant \kappa_2(W_{j_+}^{ren},W_{j_+}^{ren}) decomposed into positive pair covariance, connected C4 sectors, and recovery errors.
- same-theory condition: all Wilson loops, endpoint currents, gradient-flow fields, counterterms, and recovery maps come from the same cutoff Yang-Mills measure and the same renormalized Schwinger family.
- Carrier: endpoint sheet currents with cell moments, sector kernels K_s, dyadic annuli A_j, and certified zero-pairing quotients.
- Hard gate changed: finite endpoint-box positivity after H,K; continuum existence, OS/Wightman reconstruction, observable density, topology control, and Hamiltonian mass gap remain untouched.

## Assumptions

- Model: four-dimensional Euclidean SU(N) Yang-Mills with Wilson lattice regulator a and positive gradient-flow time t, used only as a finite same-theory regulator.
- Regime: a << eta <= rho_0 <= d and dyadic annuli A_j={rho_j <= |z| < 2 rho_j}, rho_j=2^j rho_0, stay outside the endpoint boxes.
- Uniformity: sector Hessian constants A_s and exponents nu_s are cutoff-stable for a <= a_0 and for the fixed H,K geometry.
- Cutoff: perimeter, cusp, and one-hairpin endpoint counterterms are subtracted before centering the Wilson observables.
- Same-theory: recovery error E_rec compares the endpoint-current cumulant to the original H,K Wilson hairpin cumulant without changing regulator, flow time, or observable algebra.
- Local: the plus current has zero endpoint monopole and zero endpoint dipole, so the first nonzero Taylor remainder is controlled by M_{2,+}.

## Equations

- sector Hessian majorant: `\sup_{x,y\in A_j}\left|\nabla_x^2\nabla_y^2K_s^{ren}(x,y;t,a)\right|\le A_s\,(\rho_j^2+8t)^{-\nu_s}`. Valid when: Valid when the Ward-subtracted connected C4 sector kernel is evaluated outside endpoint boxes with cutoff-stable flowed heat-kernel bounds.
- dyadic tail ratio: `q_s=2^{4-2\nu_s},\qquad T_s(J)\le C_{ann}M_{2,+}^2A_s\frac{\rho_J^{4-2\nu_s}}{1-q_s}\quad(\nu_s>2)`. Valid when: Applies after plus-channel moment cancellation reduces each annular contribution to a Hessian remainder times four-dimensional shell volume.
- endpoint dominance margin: `\Delta_R(J)=g_t^4(N^2-1)\left(2G_{++}^{-}-N\sum_sT_s^{+}(J)\right)-E_{rec}^{+}-L_+`. Valid when: Valid when the pair covariance lower interval, connected sector tail upper intervals, recovery error, and Schur-Feshbach leakage use identical H,K endpoint geometry.
- promotion inequality: `\Delta_R(J)>0\ \Longrightarrow\ Q_{+,endpoint}^{ren}>0`. Valid when: Requires the finite Schur-Feshbach theorem and the same-theory flowed Wilson cumulant lower bound for the post-H,K endpoint box.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: centered flowed Wilson hairpin endpoint sheet current j_+ for the post-H,K plus channel, represented by endpoint boxes and oriented sheet currents.; target object: the finite plus-channel Schur-Feshbach endpoint margin \Delta_R(J) whose positivity certifies the local endpoint-box repair.; Model: four-dimensional Euclidean SU(N) Yang-Mills with Wilson lattice regulator a and positive gradient-flow time t, used only as a finite same-theory regulator..
- Attack conceptual pressure: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, while positive pair covariance can be erased by connected C4 polarization.
- Write the post-H,K endpoint cumulant as R_{++}^{ren}=g_t^4(N^2-1)(2G_{++}-N\sum_s C_{4,s})-E_{rec}.
- Use Ward and cusp subtraction to remove disconnected products, one-hairpin perimeter terms, and endpoint contact terms before centering.
- Represent the plus hairpin by endpoint currents with zero monopole and dipole; Taylor expand each far-sector kernel around the endpoint-cell center.
- The zeroth and first Taylor terms cancel; the remainder is bounded by M_{2,+}^2 times the mixed Hessian supremum of the renormalized C4 sector kernel.
- On annulus A_j, insert the assumed heat-kernel Hessian majorant A_s(\rho_j^2+8t)^{-\nu_s}; four-dimensional shell volume contributes the factor proportional to \rho_j^4.
- For rho_j^2>=8t, adjacent annular contributions have ratio at most q_s=2^{4-2\nu_s}; hence the far tail is a geometric series if \nu_s>2.
- Subtract the tail upper interval, recovery error, and Schur-Feshbach leakage L_+ from the positive pair lower interval to obtain \Delta_R(J).

Blocking gap: The derivation is conditional until the actual sector constants A_s, exponents nu_s, pair lower bound G_{++}^{-}, and recovery error E_rec are certified for the chosen Wilson regulator and H,K geometry.

## Falsifiers

- falsifier: a Ward-subtracted C4 sector has tail exponent nu_s<=2, so the annular series is not summable.
- falsifier: the recovery map from raw Wilson contours to endpoint currents has an error larger than the positive pair baseline.
- falsifier: a zero-pairing quotient current has a hidden nonzero pairing against one connected sector kernel.
- falsifier: the certified lower margin Delta_R(J) is nonpositive throughout the admissible flow and endpoint-size window.
- falsifier: the positive pair interval G_{++}^{-} collapses after the same-theory normalization or endpoint geometry is enforced.
- falsifier: cusp or perimeter subtractions fail to commute with gradient flow in the finite cutoff family.

## Learning

Declarative tension: Schur-Feshbach endpoint positivity, positive same-theory flowed Wilson pair covariance, and recovery from raw Wilson hairpins must jointly be valid, but connected C4 can erase the mediator. Carrier critique: raw Wilson contours are fragmented; global OS spectral transfer and non-Gaussian Schwinger-family witnesses are too coarse for this finite obstruction. Better abstraction: endpoint sheet currents with cell moments, sector kernels, counterterms, recovery errors, Ward/cusp subtraction, plus-moment cancellation, heat-kernel Hessian majorants, outward-rounded intervals, and zero-pairing quotient guards. Efficient representation must encode H,K sheets and endpoints, preserve gauge/color/reflection/orientation/cutoff/locality/same-theory invariants, use cumulant expansion and annular tail summation as primitives, keep finite endpoint-cell locality, transfer only through centered flowed Wilson cumulants, and demote on any falsifier. Conceptual value signal: R_{++}/kappa_4 is now a valid annular sign/size certificate with q_s=2^{4-2nu_s}, not a symbolic boundary-OPE term. Hard gate: finite endpoint-box positivity after H,K; success promotes one finite Route A gate, failure quarantines this R repair while all Clay target commitments remain unclaimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide.`
- Rationale: The branch needs a concrete target-preserving computation because the symbolic R term has already been replaced by a Ward-Hessian interval; the remaining uncertainty is numerical/analytic dominance of pair covariance over connected C4 tails.
- Situation seed: SU(N) Wilson lattice Yang-Mills with gradient-flowed H,K hairpin endpoint boxes; compute the centered flowed Wilson connected cumulant witness R_{++}^{ren} using endpoint sheet currents, Ward-subtracted C4 sector kernels, and dyadic annular tails.
- Varied variable: The annular split index J, equivalently the far-tail radius rho_J relative to the flow radius sqrt(8t).
- Held-fixed controls: Same Wilson action, same gauge group SU(N), and same cutoff family for raw hairpins and endpoint currents., Same H,K endpoint geometry, plus-channel orientation, reflection assignment, and Schur-Feshbach leakage L_+., Same gradient-flow time window, counterterm prescription, Ward/cusp subtraction, and outward-rounded interval arithmetic.
- Expected observation: If q_s<1 with small certified A_s and E_rec, Delta_R(J) should plateau positive for a finite J; if not, the endpoint R repair is locally demoted.
- Transfer certificate needed: A cutoff-stable same-theory recovery map plus certified sector Hessian constants and pair lower intervals before the thought experiment can alter proof obligations.

## Next Experiment

Route to proof search: compute certified A_s, nu_s, G_{++}^{-}, and E_rec for the gradient-flow Wilson endpoint cells, then evaluate Delta_R(J). Include validator-facing same-theory nontriviality witness language only as a finite connected cumulant witness, not as a Clay mass-gap claim.

# Signed-Orbit Raw K4 Stress Witness for the Finite H,K Endpoint Gate

## Candidate Lemma

Finite signed-orbit stress theorem: in a fixed heat-kernel regulated endpoint box, certified raw signed-orbit intervals for the connected four-flux cumulant give a valid two-sparse falsifier of Schur-corrected endpoint positivity whenever a phased off-diagonal lower bound overwhelms the two certified diagonal upper bounds.

## Definitions

- source object: finite heat-kernel regulated SU(N) lattice Yang-Mills endpoint box B_sigma with oriented plaquette fluxes Phi_alpha^a(sigma), sheet weights w_{p,alpha}, and raw connected four-flux cumulant intervals I_o for signed Wilson orbits.
- target object: the Schur-corrected two-endpoint Hermitian compression U_{pq} whose positivity is necessary for the finite post-H,K Route A endpoint-box certificate.
- controlled interface: Rec_orb maps raw signed-orbit K4 intervals plus Gaussian covariance, OPE interval, and H,K Schur block into diagonal upper bounds D_r^+ and phased off-diagonal lower bounds L_{pq}(theta).
- same-theory condition: all intervals use the same heat-kernel regulator sigma, lattice cutoff a, renormalized coupling g_R(a,sigma), Wilson transporters, endpoint basis, reflection plane, and H,K Schur data; no OS Hilbert observable algebra or continuum spectral transfer is imported.
- bridge/carrier: the validator-facing connected cumulant witness is R_{pq,sigma}=cum_2(Q_p,Q_q), compressed only after gauge-invariant Wilson trace normalization and Schur subtraction.
- non-claim boundary: the lemma changes only the finite Route A endpoint-box gate; gauge-invariant observable density, excitation-sector cyclicity, OS/Wightman reconstruction, continuum existence, and Hamiltonian mass gap remain untouched.

## Assumptions

- Model: finite-volume lattice SU(N) pure Yang-Mills with heat-kernel plaquette action and reflection plane chosen before endpoint compression.
- Cutoff: 0<a<sigma and B_sigma contains only finitely many oriented plaquettes, so all cumulant sums and Schur blocks are finite matrices.
- Same-theory: Gaussian covariance C_sigma, K4 intervals, OPE remainder, and S_HK are computed in the same cutoff measure and Wilson endpoint basis.
- Validity: interval arithmetic is outward-rounded and the signed-orbit quotient is audited against exact Wilson trace identities and Hermiticity.
- Local: the H,K collar/hairpin Schur data are fixed finite objects; survival or failure of this test is not a Clay-level spectral statement.

## Equations

- endpoint quadratic Wilson flux: `Q_p=:\sum_{\alpha,\beta\in S_p} w_{p,\alpha\beta}\,\Phi_\alpha^a(\sigma)\Phi_\beta^a(\sigma):`. Valid when: Valid when the endpoint sheet S_p is finite, heat-kernel transported, and normal ordered by the same cutoff vacuum.
- connected boundary polarization: `R_{pq,\sigma}=\operatorname{cum}_2(Q_p,Q_q)=\langle Q_pQ_q\rangle_\sigma-\langle Q_p\rangle_\sigma\langle Q_q\rangle_\sigma`. Valid when: Valid when vacuum and perimeter terms are subtracted in the same Wilson normalization before endpoint compression.
- post-HK Schur compression entry: `U_{pq}=\alpha_N g_R^4(C_{pq}\circ C_{pq})+\frac{g_R^4}{16N^2}K^{(4)}_{pq}+E^{\mathrm{OPE}}_{pq}-S^{HK}_{pq},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when the boundary OPE is truncated in the endpoint box and the H,K Schur block is invertible on Q-space.
- signed-orbit interval recovery: `K^{(4)}_{pq}\in \sum_{o\in\mathcal O_{pq}} m_o s_o I_o,\qquad s_o\in\{\pm1,\pm i\}`. Valid when: Valid when every plaquette quadruple contributing to K4 is assigned to an exact Wilson signed orbit with multiplicity m_o.
- phased off-diagonal lower bound: `L_{pq}(\theta)=\max\{0,\underline{\operatorname{Re}}(e^{-i\theta}U_{pq})\}`. Valid when: Valid when the Hermitian interval enclosure for U_pq includes Gaussian, K4, OPE, and Schur terms with the same phase convention.
- two-sparse stress falsifier: `L_{pq}(\theta)^2>D_p^+D_q^+\ \Longrightarrow\ \exists x_{pq,\theta}:\ x_{pq,\theta}^*U_{\{p,q\}}x_{pq,\theta}<0`. Valid when: Valid when D_p^+ and D_q^+ are certified upper bounds for the corresponding real diagonal entries of U.

## Attempted Derivation

- Conceptual pressure attacked: R must be a connected cumulant witness with raw same-regulator K4 content, not scalar R rhetoric or an OS-density restatement.
- Declarative tension: Wilson/OPE coefficients, raw K4 intervals, OPE error, and S_HK must jointly control one finite endpoint quadratic form, while OS reconstruction, gauge-invariant observable density, excitation-sector cyclicity, continuum existence, and mass gap are barred as conclusions.
- Carrier critique: scalar R is representation-limited, OS Hilbert observable algebra is too strong and circular for this local gate, A012 shells are convenient but quarantined, and raw plaquette enumeration is fragmented but valid.
- Route comparison: full Delta_raw PSD proof is promotion-capable but data-hungry; signed-orbit two-sparse stress is a sharper negative tactic because a few orbit intervals can falsify endpoint PSD.
- Decompose R_{pq,sigma} into the PSD Gaussian color square, one raw K4 signed-orbit interval sum, an OPE interval, and the H,K Schur entry in the same cutoff theory.
- Construct D_p^+,D_q^+ from diagonal upper interval endpoints and L_{pq}(theta) from a phased lower endpoint of Re(e^{-i theta}U_pq).
- Use the 2x2 PSD necessary condition |U_pq|^2<=U_pp U_qq; if L_{pq}(theta)^2>D_p^+D_q^+, choose the corresponding phase stress vector to get a negative Rayleigh quotient.

Blocking gap: No certified same-regulator raw K4 signed-orbit intervals I_o have been supplied for the actual H,K endpoint geometry, so the theorem is validator-facing but not numerically discharged.

## Falsifiers

- A concrete falsifier is any phase theta and endpoint pair p,q with L_{pq}(theta)^2>D_p^+D_q^+, since it gives a negative Rayleigh vector for the Schur-corrected endpoint compression.
- Regulator mismatch between K4 intervals and the Gaussian/OPE/Schur data invalidates the same-theory recovery map.
- A non-Hermitian signed-orbit enclosure falsifies the quotient and forces raw plaquette enumeration.
- If all signed-orbit intervals are too wide to decide L_{pq}(theta)^2>D_p^+D_q^+, the negative tactic is inconclusive and the branch must not claim endpoint positivity.
- If diagonal upper bounds are already negative, endpoint positivity is killed without using the off-diagonal stress test.

## Learning

Cycle 321 makes the hard gate explicit: L_{pq}(theta)^2>D_p^+D_q^+ is a valid finite falsifier for the H,K endpoint PSD, while survival forces full Delta_raw proof search. The conceptual value signal is sharp and route-changing at finite scope because Gaussian color positivity, raw non-Gaussian K4, OPE error, and Schur hairpin energy are unified in one same-theory connected cumulant witness. The larger YM gates--volume/cutoff-uniform basin entry, large-field/topology control, regulator-independent Schwinger functions, OS positivity, gauge-invariant observable density, excitation-sector cyclicity, and physical-unit spectral transfer--remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the signed-orbit raw K4 route.`
- Rationale: The branch has repeated abstraction; the next valid learning comes from testing whether a few same-regulator orbit intervals can dominate Gaussian color positivity and Schur/OPE uncertainties in a finite endpoint box.
- Situation seed: Heat-kernel SU(2) lattice endpoint box with two reflected Wilson endpoint sheets p,q, one coplanar signed K4 orbit O_c, one twisted hairpin orbit O_h, fixed H,K Schur block, and raw interval enclosures for kappa_4 on O_c and O_h.
- Varied variable: rho, the certified negative off-diagonal signed-orbit imbalance contributed by O_h relative to O_c in Re(e^{-i theta}K4_pq).
- Held-fixed controls: Same cutoff a, regulator sigma, coupling g_R, reflection plane, and endpoint Wilson basis., Fixed Gaussian covariance C_sigma, OPE error interval, and H,K Schur block S_HK., Exact Wilson signed-orbit quotient policy with Hermiticity and transporter paths audited., Finite endpoint-box complexity; no continuum or OS spectral transfer assumptions.
- Expected observation: As rho increases, L_{pq}(theta)^2 should cross D_p^+D_q^+ if the non-Gaussian K4 off-diagonal polarization can falsify endpoint PSD; if it never crosses under certified intervals, the route must proceed to full Delta_raw instead of repeating phase stress.
- Transfer certificate needed: A validator-facing certificate listing orbit representatives, multiplicities, signs, raw K4 intervals, diagonal upper bounds, OPE and Schur intervals, and the recovered stress vector x_stress in the same cutoff theory.

## Next Experiment

Proof search: compute the first signed-orbit raw K4 interval table for a fixed H,K endpoint pair p,q, then evaluate D_p^+, D_q^+, L_{pq}(theta), and either output x_stress as a connected cumulant witness falsifier or hand off to full Delta_raw Loewner certification.

