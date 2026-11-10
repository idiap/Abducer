# cycle-0328

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Finite Route A endpoint-source gate quarantine

## Candidate Lemma

Endpoint-source data are necessary for the post-H,K three-hairpin gate: H,K, half-overlap shielding, and the SU(N) root-quartic screen do not validly promote OS positivity unless the positive-D connected cumulant witness and uniform tail are certified. With compatible unmeasured endpoint cumulants one obtains both positive and negative gate assignments, so the branch must quarantine rather than claim the finite block.

## Definitions

- source object: heat-kernel plaquette-sheet SU(N) endpoint source carrier C_ep=(source classes c, endpoint partition functions Z_c(s), stencil scale h, incidences b_ij,c, cutoff a, endpoint box scale eps).
- target object: finite post-H,K reflected-Wilson OS transfer scalar for the locked three-hairpin block, not the continuum Yang-Mills mass gap or full OS reconstruction.
- controlled interface: aggregate same-theory endpoint source derivatives and signed null-channel incidences into the scalar interval I_gate exported to the finite Schur-Feshbach OS gate.
- same-theory condition: the Wilson loops, reflection map, heat-kernel regulator, source deformation, and normalization are unchanged; no boundary counterterm, extra boundary Hilbert sector, or advice observable is introduced.
- bridge observable: the connected cumulant witness kappa_c=(d^4/ds^4) log Z_c(sL_c)|_{s=0} contracted with D_c=2b_12,c-4b_13,c-4b_23,c.
- hard gate changed: success promotes only this finite post-H,K reflected-Wilson block; failure gives a finite same-theory falsifier; missing data keeps quarantine.

## Assumptions

- Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette-sheet Wilson insertions in finite volume before any continuum claim.
- Regime: H and K for the three-hairpin collar block are already fixed, Wick-square Gram terms are removed, and straight f f contacts cancel by the null incidence identity.
- Cutoff: endpoint source intervals, source-equivalence classes, and T_tail must be bounded uniformly along the selected cutoff-refinement window.
- Same-theory: source differentiation probes the same regulated Wilson endpoint partition function and is not a boundary theory or counterterm renormalization.
- Validity: the root-quartic Haar coefficient is an analytic screen only; it cannot replace measured source intervals when positive-D leakage is present.
- Local: this is a restricted finite Route A theorem and leaves continuum existence, OS/Wightman reconstruction, nontriviality, and mass gap untouched.

## Equations

- endpoint_stencil: `\kappa_c=\left.\partial_s^4\log Z_c(sL_c)\right|_{s=0}=h^{-4}\sum_{r=-3}^{3}w_r\log Z_c(rhL_c)+E_c(h)`. Valid when: Applies when the heat-kernel endpoint source family is analytic in s uniformly in the chosen cutoff window.
- signed_incidence: `D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}`. Valid when: Valid when b_{ij,c} are aggregated over source-equivalent endpoint boxes before any clipping operation is applied.
- finite_gate_interval: `I_{\rm gate}=M_G+C_N\sum_c D_c\,\kappa_c+T_{\rm tail}\in [I_-,I_+]`. Valid when: Requires the same-theory endpoint source intervals, fixed null incidences, explicit color factor, and cutoff-uniform tail bound.
- indistinguishable_sign_assignments: `I_{\rm safe}=M_G>0,\qquad I_{\rm bad}=M_G-C_ND_+K_+-\tau<0`. Valid when: Valid when only the root-quartic cap is known and positive-D source cumulants have not been measured.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel plaquette-sheet SU(N) endpoint source carrier C_ep=(source classes c, endpoint partition functions Z_c(s), stencil scale h, incidences b_ij,c, cutoff a, endpoint box scale eps).; target object: finite post-H,K reflected-Wilson OS transfer scalar for the locked three-hairpin block, not the continuum Yang-Mills mass gap or full OS reconstruction.; Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette-sheet Wilson insertions in finite volume before any continuum claim..
- Start from the finite Schur-Feshbach post-H,K scalar for the locked three-hairpin Wilson block after removing the rank-one vacuum direction.
- Use the established cancellations: Wick-square contractions are positive Gram terms, straight nonabelian f f contacts cancel in the null incidence channel, and one-body Wilson renormalizations disappear.
- Represent the remaining connected boundary-OPE polarization by C_ep: source-equivalent endpoint classes, seven source values, cumulant intervals, signed D_c incidences, color factor C_N, Gaussian margin M_G, and T_tail.
- Aggregate incidences within each source class before clipping; this preserves the null-channel cancellation that raw R and raw kappa_4 spectra lose.
- Insert the SU(N) root-quartic screen to bound possible negative connected endpoint cumulants, but keep it separate from the measured connected cumulant witness.
- Try to prove I_gate>=0 using only H,K, half-overlap shielding, and the root-quartic cap.
- Construct a stress assignment with all unmeasured positive-D cumulants zero giving I_safe=M_G>0, and another assignment saturating the negative cap plus tail giving I_bad<0 whenever C_N D_+ K_+ + tau > M_G.

Blocking gap: The positive-D endpoint source intervals and the cutoff-uniform tail are not computed; the existing abstractions underdetermine the finite OS gate.

## Falsifiers

- A certified negative interval I_+<0 is a finite same-theory falsifier for the post-H,K OS transfer block.
- A boundary counterterm or boundary Hilbert-sector source needed to define Z_c violates the same-theory condition.
- Endpoint source classes that look geometrically identical but have unequal regulated source data falsify source-equivalence compression.
- A nonuniform T_tail along cutoff refinement blocks any valid transfer from the finite regulator calculation.
- If positive-D leakage exceeds the root-quartic cap and the tail is not charged, the analytic screen is invalid.

## Learning

Conceptual pressure attacked: endpoint collapse must be sign-certified inside the same Wilson theory after H,K. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist without adding a boundary theory, but H,K, half-overlap shielding, and the root-quartic screen do not determine the scalar. Carrier audit: raw R is too weak, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. Efficient representation: C_ep encodes endpoint source classes, seven source values, cumulant intervals, signed incidences, C_N, M_G, and T_tail; preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; uses source differentiation, interval arithmetic, aggregation before clipping, color multiplication, and tail addition; equivalence is regulated source data only; transfer exports I_gate. Conceptual value signal: sharp route change at finite scope. Negative SU(N) endpoint cumulants are explanatory but not the obstruction; positive-D leakage times same-theory connected cumulant witness plus uniform tail is. The branch is looping on promotion language, so quarantine is the valid proof-state update.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a validator-facing falsifier probe while the branch is quarantined from promotion.`
- Rationale: The branch has looped on screened quarantine; a concrete one-parameter endpoint family tests whether missing connected cumulant witness data are genuinely decisive rather than representational bookkeeping.
- Situation seed: Heat-kernel SU(N) plaquette-sheet three-hairpin endpoint box with fixed H,K block, one source-equivalence class c_gamma, and endpoint footprints chosen so D_gamma=2b12-4b13-4b23 varies from shielded to 12-dominant while the Wilson loops and regulator remain unchanged.
- Varied variable: positive-D leakage gamma=D_gamma with gamma=0 at the half-overlap shield and gamma>0 for certified 12-dominant endpoint support.
- Held-fixed controls: Same heat-kernel plaquette-sheet regulator and finite cutoff window., Locked gauge-invariant Wilson hairpin algebra, reflection map, null vector, and H,K data., No boundary counterterm, no new observable algebra, and same source stencil scale h., Fixed color factor C_N, Gaussian margin M_G, and prescribed tail budget tau_tail.
- Expected observation: There should be a threshold gamma_c=(M_G-tau_margin)/(C_N |kappa_c|): below it the finite gate is safely positive, above it a measured negative connected cumulant witness can become a finite falsifier.
- Transfer certificate needed: Uniform seven-point source intervals for kappa_c, proof that endpoint tails are bounded by tau_tail across cutoff refinement, and a same-theory certificate that source deformation is a derivative of the original Wilson endpoint partition.

## Next Experiment

Route to targeted proof search plus endpoint source computation: build the C_ep table for the positive-D connected cumulant witness in the heat-kernel plaquette-sheet three-hairpin regulator, then certify I_gate or produce the finite falsifier.

# Endpoint R++ annular plateau certificate with quarantine guard

## Candidate Lemma

For the fixed post-H,K plus endpoint box, a same-theory flowed Wilson cumulant lower interval proves finite endpoint-box positivity if Ward-subtracted connected C4 annular tails have a certified plateau ratio below one and the resulting margin Delta_R^- beats the exact Schur-Feshbach leakage L_+. Failure is a local falsifier for this R-repair, not for Yang-Mills existence or mass gap.

## Definitions

- source object: the centered gradient-flowed Wilson hairpin covariance R_{++}^{ren}(t,a,eta) in four-dimensional SU(N) Yang-Mills, localized to the post-H,K plus endpoint boxes and expanded in the same Wilson regulator.
- target object: a finite Schur-Feshbach endpoint-box positivity certificate Delta_R^- > 0 for the plus channel after subtracting the exact leakage L_+; this is not an OS spectral gap or continuum-existence claim.
- controlled interface: endpoint sheet currents J_+ with Ward/cusp subtraction, plus-channel moment cancellation, dyadic annular Hessian bounds for connected four-curvature sectors, and an outward-rounded recovery map from raw Wilson hairpins.
- same-theory condition: all flowed cumulants, counterterms, recovery errors, and Schur-Feshbach coefficients are computed in one regulator/RG family and one limiting gauge-invariant Schwinger family when that limit is invoked.
- G_{++} is the positive flowed two-curvature cross-pairing of the two plus endpoint sheet currents.
- C_{4,++}^{WS} is the Ward-subtracted connected four-curvature polarization after disconnected-product and one-hairpin perimeter/cusp cancellation.
- A_{s,j} is the outward-rounded mixed-Hessian majorant for C4 sector s on dyadic annulus j; H_{s,near} is the corresponding finite near-cell majorant.
- M_{2,+} is the certified second endpoint moment of the plus current after monopole and dipole cancellation; E_{rec} bounds raw-hairpin recovery and zero-pairing quotient errors.

## Assumptions

- Model: four-dimensional Euclidean SU(N) Yang-Mills with Wilson lattice regulator or heat-kernel continuum cutoff, evaluated at positive gradient-flow time t.
- Cutoff: endpoint cell radius eta and separation d obey a << eta <= sqrt(8t) << d, with constants tracked uniformly over the finite H,K geometry.
- Same-theory: the centered flowed Wilson cumulant, counterterms, and recovery map are all drawn from the same regulator family; no imported continuum Schwinger result is used as a black box.
- Uniformity: annular Hessian bounds are cutoff-stable after Ward/cusp subtraction and include outward rounding and counterterm uncertainty.
- Local: the claim changes only finite endpoint-box positivity after H,K; continuum existence, gauge-invariant observable density, OS spectral transfer, nontriviality, and Hamiltonian mass gap remain untouched.
- Validity: the connected C4 sector kernels are C^2 on separated endpoint cells at positive flow time and satisfy a dyadic decay exponent nu_s>2 after moment cancellation.

## Equations

- same-theory R decomposition: `R_{++}^{ren}=g_t^4(N^2-1)\{2G_{++}+N C_{4,++}^{WS}\}-E_{rec}`. Valid when: Valid when the source object is the centered flowed Wilson covariance, the regulator is fixed, and disconnected, perimeter, and cusp counterterms are subtracted in the same-theory Wilson family.
- Ward-Hessian C4 majorant: `-C_{4,++}^{WS}\le M_{2,+}^2\sum_s\left(H_{s,near}+\sum_{j\ge J}A_{s,j}\right)`. Valid when: Requires Ward/cusp subtraction, plus-channel moment cancellation, and C^2 sector kernels on separated endpoint cells at positive flow time.
- plateau tail compression: `\sum_{j\ge J}A_{s,j}\le \frac{A_{s,J}^+}{1-\bar q_s},\qquad \bar q_s:=\max(P_{s,J},2^{4-2\nu_s})+\rho_s<1`. Valid when: Applies when annular interval evaluation certifies nonnegative A_{s,j} and a stable ratio \bar q_s<1 beyond the chosen plateau annulus.
- dominance margin: `\Delta_R^-:=g_t^4(N^2-1)\left(2G_{++}^- - N M_{2,+}^2\sum_s\left(H_{s,near}^+ + \frac{A_{s,J}^+}{1-\bar q_s}\right)\right)-E_{rec}^+-L_+`. Valid when: Valid when all interval endpoints are outward rounded and L_+ is the same finite Schur-Feshbach leakage for the H,K reduction.
- finite endpoint promotion test: `\Delta_R^->0\Rightarrow Q_{+,endpoint}>0,\qquad \Delta_R^-\le0\text{ quarantines this R-repair}`. Valid when: Applies only to the finite endpoint box after H,K and does not transfer to OS spectral mass-gap statements.

## Attempted Derivation

- Fix the gradient-flow regulator t>0 and the actual H,K plus endpoint sheet currents; keep the raw-hairpin recovery map and error E_rec in the same Wilson theory.
- Expand the centered hairpin covariance. Disconnected products and one-hairpin perimeter/cusp terms cancel by centering and renormalization; Ward subtraction removes gauge-gradient artifacts.
- The Gaussian pair contraction gives the positive color factor 2(N^2-1)G_{++}. The connected four-curvature sectors carry color N(N^2-1) and are the only sign-indefinite part kept in R_{++}^{ren}.
- Use plus-channel monopole and dipole cancellation to replace the C4 sector integral over separated endpoint cells by a second-moment factor M_{2,+}^2 times a mixed-Hessian supremum.
- Split the Hessian domain into finite near cells and dyadic annuli. On annulus j, outward-rounded interval quadrature gives A_{s,j}; the heat-kernel Hessian decay gives the model ratio 2^{4-2nu_s}, while adjacent computed ratios give the plateau ratio P_{s,J}.
- If \bar q_s=max(P_{s,J},2^{4-2nu_s})+rho_s<1, compress the tail geometrically and subtract it, the near constants, E_rec, and the exact leakage L_+ to obtain Delta_R^-.
- A positive Delta_R^- proves the finite endpoint-box positivity condition Q_{+,endpoint}>0 after H,K. A nonpositive or uncertified margin is a falsifier for this local R-repair only.

Blocking gap: The missing proof object is the certified numerical or analytic interval list for the actual H,K geometry: G_{++}^-, M_{2,+}, H_{s,near}^+, A_{s,J}^+, plateau ratios P_{s,J}, rho_s, and same-theory recovery errors.

## Falsifiers

- Plateau falsifier: some connected C4 sector has certified \bar q_s>=1 for every allowed annulus start J.
- Dominance falsifier: the outward-rounded lower margin Delta_R^- is nonpositive after including L_+ and E_rec.
- Same-theory falsifier: the recovery map from raw Wilson hairpins to endpoint sheet currents uses a different regulator, counterterm scheme, or Schwinger family.
- Ward/cusp falsifier: disconnected-product, perimeter, cusp, or gauge-gradient cancellations leave an uncancelled first-moment term.
- Geometry falsifier: the H,K plus endpoint current has M_{2,+} too large or G_{++}^-=0, so the positive pair baseline cannot dominate.
- Interval-width falsifier: outward-rounded annular constants are wider than the pair margin under the declared finite complexity budget.

## Learning

Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, while connected C4 can erase the positive pair covariance. Declarative tension: endpoint positivity, positive flowed pair covariance, and raw-hairpin recovery must jointly be valid, but the missing mediator is a cutoff-stable annular plateau bound for R_{++}/kappa_4. Carrier critique: raw Wilson contours are fragmented and representation-limited; global OS spectral transfer and a non-Gaussian Schwinger family or same-theory nontriviality witness route are too coarse for this finite obstruction. Efficient representation: encode H,K sheets, endpoint currents, moments, sector kernels, counterterms, recovery errors, and L_+; preserve gauge, color, reflection, orientation, cutoff, locality, and same-theory invariants; use cumulant expansion, Ward/cusp subtraction, Taylor Hessian remainders, heat-kernel majorants, dyadic tail compression, outward-rounded intervals, and zero-pairing quotienting; keep finite endpoint cells plus summable annuli; transfer only through centered flowed Wilson cumulants; demote on any falsifier. Hard gate: finite endpoint-box positivity after H,K. Value signal: R_{++}/kappa_4 is now a plateau-tested annular sign/size certificate, not a symbolic boundary-OPE term; success promotes one finite Route A gate, failure quarantines this repair while all Clay commitments remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and proof-search guide.`
- Rationale: The branch needs a concrete target-preserving computation because the only remaining mediator between finite Schur-Feshbach positivity and Wilson cumulant positivity is the sign/size of the connected boundary-OPE polarization R_{++}. More abstraction would merely restate the obstruction.
- Situation seed: Use SU(2) and SU(3) Wilson lattice Yang-Mills at positive gradient flow, fixed H,K plus hairpin endpoint boxes, endpoint sheet currents with Ward/cusp subtraction, and sector kernels I_3g, I_4g, I_ct, and I_end for the centered flowed Wilson covariance.
- Varied variable: The single varied variable is the plateau start annulus J for the dyadic C4 Hessian tail, with endpoint geometry, flow time, and H,K currents held fixed.
- Held-fixed controls: Fixed Clay boundary: no claim of continuum existence, OS/Wightman axioms, nontrivial continuum limit, observable density, OS spectral transfer, or Hamiltonian mass gap., Fixed regulator family and same-theory recovery map for raw Wilson hairpins and endpoint sheet currents., Fixed H,K plus-channel geometry, endpoint cell radius eta, gradient-flow time t, and Schur-Feshbach leakage L_+., Fixed primitive operations: centered cumulant expansion, Ward/cusp subtraction, plus-moment cancellation, outward-rounded interval arithmetic, and zero-pairing quotient checks.
- Expected observation: Either the annular ratios enter a stable plateau with \bar q_s<1 and Delta_R^->0, promoting finite endpoint-box positivity, or the ratio/margin fails and supplies a clean falsifier for the R_{++} repair.
- Transfer certificate needed: A validator-facing interval file or proof object listing G_{++}^-, M_{2,+}, H_{s,near}^+, A_{s,J}^+, \bar q_s, E_rec^+, and L_+ in the same-theory Wilson family; only then may the intuition affect proof obligations for the finite Route A gate.

## Next Experiment

Proof search: compute the actual H,K plus-hairpin annular sector constants for the centered flowed Wilson cumulant, record a same-theory nontriviality witness marker for validator continuity, and decide promotion or quarantine from the certified Delta_R^- interval.

# Signed-orbit raw K4 stress certificate for finite H,K endpoint box

## Candidate Lemma

For a finite heat-kernel endpoint pair p,q, exact signed Wilson-orbit intervals for K4 give computable D_p^+,D_q^+,L_pq(theta). The hard gate L_pq(theta)^2>D_p^+D_q^+ is a valid falsifier for endpoint PSD; survival forces full Delta_raw search.

## Definitions

- source object: finite heat-kernel regulated SU(N) lattice YM Wilson sheet data with oriented plaquette fluxes Q_{i,sigma}.
- target object: finite Hermitian endpoint compression U_sigma on span{e_p,e_q}, whose PSD is a local endpoint positivity property.
- controlled interface: connected cumulant witness cum_2(:Q_i^2:,:Q_j^2:) transferred by exact signed-orbit intervals and Schur subtraction.
- same-theory condition: R, K4, OPE error, and S_HK use one cutoff, coupling, Wilson basis, regulator, and normal ordering.
- carrier: signed-orbit table encoding plaquette quadruples, sheet weights, transporters, color tensors, signs, multiplicities, and interval bounds.

## Assumptions

- Model: finite-volume heat-kernel regulated SU(N) lattice Yang-Mills with Wilson action, cutoff a, smoothing sigma, and fixed H,K endpoint geometry.
- Cutoff: sigma/a and endpoint box size are fixed before intervals are formed; no volume or continuum uniformity is claimed.
- Same-theory: R_raw, K^{raw}, E^{OPE}, and S^{HK} are evaluated with the same regulator, coupling, Wilson basis, and normal ordering.
- Validity: signed orbits use only exact Wilson trace identities, orientation reversal, reflection symmetry, and color contractions preserving Hermiticity.
- Local: finite endpoint compression only; OS Hilbert observable algebra, gauge-invariant observable density, and mass gap are non-claims.

## Equations

- Schur-corrected raw endpoint form: `U_{ij,\sigma}=\alpha_N g_R^4(C_i\circ C_j)_\sigma+\frac{g_R^4}{16N^2}K^{raw}_{ij,\sigma}+E^{OPE}_{ij,\sigma}-S^{HK}_{ij}`. Valid when: Valid when heat-kernel plaquette fluxes are normal ordered, perimeter and vacuum disconnected terms cancel, and H,K Schur data use the same cutoff.
- signed-orbit K4 interval recovery: `K^{raw}_{pq,\sigma}\in\sum_{O\in\mathfrak O_{pq}} m_O\epsilon_O I_O(\sigma)`. Valid when: Applies when every plaquette quadruple in the connected four-curvature cumulant is assigned to an exact Wilson trace orbit with a certified interval.
- two-sparse stress demotion gate: `L_{pq}(\theta)^2>D_p^+D_q^+\Rightarrow \exists x_{pq}:x_{pq}^*U_\sigma x_{pq}<0`. Valid when: Requires a Hermitian two-endpoint compression, diagonal upper bounds, and a phase-sector lower bound on the Schur-corrected off diagonal.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: finite heat-kernel regulated SU(N) lattice YM Wilson sheet data with oriented plaquette fluxes Q_{i,sigma}.; target object: finite Hermitian endpoint compression U_sigma on span{e_p,e_q}, whose PSD is a local endpoint positivity property.; Model: finite-volume heat-kernel regulated SU(N) lattice Yang-Mills with Wilson action, cutoff a, smoothing sigma, and fixed H,K endpoint geometry..
- Expand each endpoint Wilson sheet as Q_i=sum_s w_{is} Tr(T^a U_s F_s^a); normal ordering cancels vacuum and perimeter disconnected pieces in cum_2(:Q_i^2:,:Q_j^2:).
- Separate crossed Gaussian curvature contractions with color factor alpha_N=(N^2-1)/(8N^2); put every non-Gaussian four-curvature term into K^{raw}_{ij,sigma}.
- Partition K^{raw}_{pq,sigma} plaquette quadruples into exact signed Wilson orbits O and sum m_O epsilon_O I_O to get phase lower L_pq(theta) and diagonal uppers D_p^+,D_q^+.
- Apply the 2x2 determinant/Rayleigh test: L^2>D_p^+D_q^+ gives x_stress and kills finite endpoint positivity; otherwise only full Delta_raw proof search remains.

Blocking gap: The first same-regulator signed-orbit K4 intervals I_O(sigma) for the selected H,K endpoint pair have not been computed.

## Falsifiers

- falsifier: an exact Wilson identity splits or merges signed orbits so the interval table is not invariant.
- A same-regulator K4 interval is unavailable or too wide to produce a valid phase lower bound L_pq(theta).
- The diagonal upper bounds D_p^+,D_q^+ exceed the off-diagonal stress for every phase sector.
- The OPE error or H,K Schur block was computed with a different cutoff, coupling, or Wilson normalization.

## Learning

Conceptual pressure: R must be a same-theory connected cumulant witness, not OS Hilbert observable algebra or scalar R. Declarative tension: Wilson/OPE, raw K4, and S_HK must share one cutoff while gauge-invariant observable density, continuum existence, and mass gap stay non-claims. Signed orbits are sharper than A012 shells because signs and exact quotients are retained.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the finite H,K endpoint route.`
- Rationale: The branch is looping unless raw signed-orbit intervals exist. Varying one regulator ratio tests whether the connected cumulant witness can beat the Schur and OPE margins.
- Situation seed: Finite SU(2) heat-kernel lattice endpoint box with two reflected Wilson sheets p,q; enumerate all plaquette quadruples in K^{raw}_{pq} and quotient them into signed Wilson trace orbits.
- Varied variable: smoothing ratio rho=sigma/a.
- Held-fixed controls: Same lattice action, coupling, Wilson basis, normal ordering, and endpoint H,K geometry., Same Schur block S_HK, same OPE truncation rule, exact Wilson quotient policy, and finite endpoint box.
- Expected observation: If a few signed orbits dominate the phase-resolved off diagonal as rho varies, L_pq(theta)^2 may cross D_p^+D_q^+ and produce a route-killing stress vector.
- Transfer certificate needed: A validator-facing orbit table with exact symmetry proof, interval enclosures I_O(rho), color factors, OPE budget, Schur data, and recovery of U_sigma entries.

## Next Experiment

Proof search: compute the first same-regulator signed-orbit K4 interval table for one endpoint pair p,q and test L_pq(theta)^2>D_p^+D_q^+. If absent, quarantine; if negative, output x_stress as connected cumulant witness. Gauge-invariant observable density remains a non-claim.

