# cycle-0343

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# One-sided endpoint connected-cumulant screen for the finite post-H,K Wilson OS gate

## Candidate Lemma

For the fixed post-H,K reflected Wilson block, source-equivalent endpoint data give a valid one-sided promotion/falsifier interval: negative endpoint fourth cumulants can lower the gate only through aggregated positive D-leakage plus a uniform tail.

## Definitions

- source object: heat-kernel plaquette-sheet SU(N) endpoint source classes c, with regulated log source functions F_{a,c}(s)=log Z_{a,c}(sL_c), fractional pair incidences b_{ij}(c), and connected cumulant witness kappa_{a,c}=F_{a,c}^{(4)}(0).
- target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for the fixed three-hairpin block, not the continuum Yang-Mills theory and not the mass-gap theorem.
- controlled interface: the endpoint carrier C_ep=(F_{a,c},K_{a,c},D_c,C_N,M_G,T_tail)_c, using aggregation-before-clipping, interval multiplication, color multiplication, and tail addition.
- same-theory condition: all F_{a,c} are source derivatives of the same regulated heat-kernel Wilson action and the same locked gauge-invariant Wilson observables; no boundary counterterm, new algebra, or changed Wilson normalization is allowed.
- conceptual pressure: sign-certify endpoint collapse inside the same Wilson theory after H,K rather than hiding it in symbolic R.
- declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist, but H,K, half-overlap shielding, and root-quartic negativity do not determine I_gate.
- carrier audit: raw R is representation-limited, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K.
- efficient representation: encode endpoint source classes, seven source values or analytic caps, cumulant intervals, aggregated signed D_c, C_N, M_G, and T_tail; preserve reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; identify equivalence only by equal regulated source data; export only I_gate.

## Assumptions

- Model: four-dimensional lattice SU(N) Yang-Mills with heat-kernel plaquette action and reflection-positive collar regularization.
- Regime: fixed finite three-hairpin Wilson block after the already computed H,K Schur-Feshbach reduction; no continuum limit is claimed.
- Cutoff: estimates are uniform in the endpoint box cutoff a for the chosen finite block and fixed physical collar scale before endpoint collapse.
- Same-theory: source insertions differentiate the locked Wilson observables in the original regulated measure, with no boundary theory or ad hoc renormalization.
- Uniformity: the remainder T_tail is bounded by a cutoff- and volume-uniform interval independent of endpoint source class labels.
- Validity: source-equivalent endpoint boxes are aggregated before sign clipping, so null-channel cancellations are not destroyed by bookkeeping.

## Equations

- source_class_incidence: `D_c=\sum_{v\in c}\bigl(2b_{12}(v)-4b_{13}(v)-4b_{23}(v)\bigr)`. Valid when: Valid when source-equivalent endpoint boxes are formed after the H,K reduction and before any sign clipping.
- connected_cumulant_witness: `\kappa_{a,c}=\partial_s^4\log Z_{a,c}(sL_c)\big|_{s=0}=\langle X_c^4\rangle_{a,c}^{\mathrm{conn}}`. Valid when: Applies when the endpoint source X_c is inserted in the same heat-kernel Wilson measure and differentiated at zero source.
- finite_gate_interval: `I_{\mathrm{gate}}\in M_G+C_N\sum_c D_cK_{a,c}+T_{\mathrm{tail}},\qquad C_N=\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Valid when Wick-square Gram terms and straight f f contacts have already been removed by the H,K null-channel cancellations.
- one_sided_screen: `K_{a,c}\subset[-B_c,0]\ \Longrightarrow\ I_{\mathrm{gate}}\ge M_G-C_N\sum_c [D_c]_+B_c+\inf T_{\mathrm{tail}}`. Valid when: Requires certified nonpositive connected endpoint cumulant intervals and exact aggregation of signed incidences within the same regulated theory.
- seven_point_witness_stencil: `\widehat\kappa_{a,c}(h)=\frac{-F(3h)+12F(2h)-39F(h)+56F(0)-39F(-h)+12F(-2h)-F(-3h)}{6h^4}`. Valid when: Applies when F=log Z_{a,c} has eight controlled source derivatives on the symmetric stencil interval.
- stencil_error_bound: `\left|\widehat\kappa_{a,c}(h)-\kappa_{a,c}\right|\le \frac{7h^4}{240}\sup_{|s|\le 3h}|F^{(8)}_{a,c}(s)|`. Valid when: Valid for the seven-point fourth-derivative stencil with a uniform eighth-source-derivative bound on the same endpoint box.

## Attempted Derivation

- Freeze the Clay target boundary: this is a finite Route A post-H,K Wilson block calculation, not a construction of continuum Yang-Mills and not a mass-gap proof.
- Replace symbolic R by C_ep: source classes, connected cumulant witness intervals, signed D_c incidences, color factor C_N, Gaussian margin M_G, and T_tail.
- Use source-equivalence aggregation before clipping so that one-body Wilson factors, Wick-square Gram pieces, and straight f f contacts remain canceled in the null channel.
- Write the exact finite interval I_gate in terms of M_G+C_N sum_c D_cK_c+T_tail.
- If K_c is certified nonpositive, observe that D_c<=0 is protective and only [D_c]_+ can lower I_gate; this gives the one-sided lower bound.
- Use the root-quartic Haar-Jacobian expansion only as an analytic cap for K_c, with E_c and T_tail kept as explicit obligations.
- Promotion test: prove the lower endpoint of I_gate is nonnegative for all source classes of the fixed block. Falsifier test: certify sup I_gate<0 for the same regulated Wilson data.

Blocking gap: Actual same-theory source intervals K_c for positive-D endpoint classes and a cutoff-uniform T_tail are still missing.

## Falsifiers

- falsifier: a positive-D endpoint class has a same-theory connected cumulant witness interval so negative that sup I_gate<0 after adding the certified tail.
- A boundary counterterm or altered Wilson-loop normalization is needed to define F_{a,c}; then the same-theory condition fails.
- The tail T_tail is not cutoff-uniform or absorbs an unbounded topological/large-field contribution.
- Two geometrically similar endpoint boxes have different regulated source derivatives, invalidating a proposed source-equivalence compression.
- The root-quartic cap is sign-correct locally but the remainder E_c dominates it in the positive-D classes.

## Learning

Cycle 343 turns screened quarantine into a precise one-sided finite theorem. The conceptual pressure is endpoint collapse inside the same Wilson theory. The hard gate is the finite post-H,K reflected-Wilson OS scalar: success promotes only this block, failure gives a finite falsifier, and missing source/tail intervals keeps quarantine. The value signal is sharpness at finite Route A scope: negative SU(N) endpoint cumulants are explanatory but not the obstruction; only positive-D leakage times a connected cumulant witness plus uniform tail can lower the gate. The Clay gates of continuum construction, gauge-invariant observable density, full OS/Wightman reconstruction, nontriviality, OS spectral transfer, and positive mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while keeping the branch quarantined until source intervals exist.`
- Rationale: The branch has looped on endpoint-carrier language; a target-preserving thought experiment forces the one-sided screen to predict a measurable crossing rather than restating OS positivity.
- Situation seed: Heat-kernel SU(2) plaquette-sheet endpoint box for the fixed three-hairpin post-H,K block, with one source class c_eta satisfying b12=1 and b13=b23=eta/2, so D_eta=2-4eta.
- Varied variable: eta, the fractional leakage of the 12 endpoint footprint into the 13 and 23 endpoint source classes.
- Held-fixed controls: Same heat-kernel Wilson action and reflection-positive collar regulator., Same H,K reduced finite three-hairpin block and same null vector., No boundary counterterm, no changed Wilson normalization, and no enlarged observable algebra., Fixed source matrix L_c, color factor C_N, Gaussian margin M_G, and tail accounting convention.
- Expected observation: As eta crosses 1/2, D_eta changes from dangerous to protective; if the connected cumulant witness remains nonpositive, only eta<1/2 can lower I_gate. A negative interval at eta=0 would be a finite same-theory falsifier; a positive lower bound for all eta would promote this block.
- Transfer certificate needed: Certified same-theory source-derivative intervals for kappa_eta and a cutoff-uniform T_tail; without them the thought experiment is intuition only and cannot enter proof obligations.

## Next Experiment

Proof search: compute same-theory seven-point source intervals for positive-D endpoint classes in the heat-kernel SU(2) and SU(3) endpoint boxes, add a cutoff-uniform T_tail, and evaluate the exact I_gate interval; if data are unavailable, maintain quarantine rather than restating the obstruction.

# Gauge-Invariant Nontriviality Witness Selection: annular Ward-Hessian certificate for the H,K endpoint R term

## Candidate Lemma

Conditional finite theorem: for the flowed same-theory Wilson cumulant of the centered H,K plus hairpins, Ward/cusp subtraction and plus-channel moment cancellation reduce the connected boundary-OPE polarization to annular mixed-Hessian sector constants. If the certified lower margin Delta_R^- is positive, the finite endpoint-box Schur-Feshbach positivity gate after H,K is promoted; if not, this R repair is quarantined. No Clay continuum or mass-gap conclusion follows.

## Definitions

- source object: same-theory gradient-flow regulated SU(N) Wilson cumulant R_{++}^{ren}(t,a) of two centered H,K thin hairpin endpoint currents in one finite endpoint box.
- target object: finite Route A endpoint-box positivity margin Delta_R^- for the plus Schur-Feshbach channel after H,K.
- controlled interface: recovery map from raw Wilson hairpins to endpoint sheet currents, preserving gauge/color/reflection/orientation invariants with error E_rec.
- same-theory condition: all pair, connected C4, counterterm, and recovery quantities are computed at the same cutoff a, flow time t, Wilson action, and centering convention before any continuum claim.
- carrier object: endpoint sheet current J_+=J_H+J_K with zero monopole and zero dipole after reflection-plus symmetrization.
- hard gate changed: finite endpoint-box positivity after H,K only; OS/Wightman reconstruction, observable density, large-field/topology control, nontrivial continuum limit, and Hamiltonian mass gap remain untouched.

## Assumptions

- Model: finite four-dimensional lattice SU(N) Yang-Mills with Wilson action, gradient flow time t>0, and gauge-invariant flowed Wilson hairpins before cutoff removal.
- Regime: endpoint box diameter eta is smaller than annular base scale rho0, and flow radius sqrt(8t) is comparable to but not larger than rho0.
- Cutoff: a<eta/10 and all interval constants are required uniformly over the chosen finite cutoff range, not in an asserted continuum limit.
- Same-theory: pair baseline, connected C4 kernels, counterterms, and raw-to-current recovery errors use the same regulator and the same centering subtraction.
- Local: only endpoint cells and dyadic annuli outside the endpoint box enter; no global area-law or OS spectral-transfer input is used.
- Validity: Ward identities remove constant and first endpoint moments after disconnected-product subtraction and one-hairpin perimeter/cusp renormalization.
- Constraint: every sector s in {3g,4g,ct,end} has an interval mixed-Hessian envelope H_{s,j}^+ on dyadic annulus A_j and a tail exponent nu_s>2.

## Equations

- flowed-cumulant-decomposition: `R_{++}^{ren}=g_t^4 (N^2-1)\left(2G_{++}+N\sum_s C_{s,++}^{WS}\right)-E_{rec}`. Valid when: Valid when the centered flowed H,K Wilson hairpins are recovered as endpoint sheet currents with the same cutoff, flow time, color normalization, and perimeter/cusp subtraction.
- Ward-Hessian-sector-bound: `C_{s,++}^{WS}(A_j)\ge -M_{2,+}^2\,H_{s,j}^+`. Valid when: Applies after disconnected products, Ward-exact terms, cusp counterterms, and plus-channel monopole and dipole endpoint moments have been cancelled in each annular sector.
- annular-tail-compression: `\sum_{j\ge J}H_{s,j}^+\le H_{s,J}^+/(1-q_s),\qquad q_s=2^{4-2\nu_s}<1`. Valid when: Requires dyadic annuli outside the endpoint box, four-dimensional cell counting, and a certified mixed-Hessian decay exponent nu_s greater than two.
- dominance-margin: `\Delta_R^-:=g_t^4 (N^2-1)\left(2G_{++}^- -N M_{2,+}^2\sum_s\left[\sum_{j<J}H_{s,j}^+ +\frac{H_{s,J}^+}{1-q_s}\right]\right)-E_{rec}^+-L_+`. Valid when: Valid when G_{++}^- is an outward-rounded lower interval for the positive pair contraction and L_+ is the finite Schur-Feshbach leakage from the already fixed H,K reduction.
- finite-gate-promotion-test: `\Delta_R^->0\ \Longrightarrow\ Q_+^{HK}+R_{++}^{ren}-L_+>0`. Valid when: Applies only to the finite endpoint-box plus channel after H,K, with no inference to continuum OS positivity or Hamiltonian spectral gap.

## Attempted Derivation

- Freeze the Clay claim level: only a finite Route A endpoint-box positivity certificate is sought; no continuum YM construction, OS/Wightman reconstruction, nontriviality theorem, or mass gap is claimed.
- Represent centered H,K hairpins by endpoint sheet currents J_+ after gradient flow, disconnected-product subtraction, and one-hairpin perimeter/cusp subtraction.
- Decompose the flowed connected Wilson covariance into the positive two-curvature pair baseline 2(N^2-1)G_{++} and connected four-curvature sectors with color N(N^2-1).
- Use Ward identities and plus-channel reflection symmetry to cancel monopole and dipole endpoint moments, leaving a Taylor remainder controlled by mixed Hessians of Ward-subtracted sector kernels.
- Partition the exterior of the endpoint box into dyadic annuli A_j; a sector Hessian with decay 2^{-2nu_s j} times four-dimensional cell counting gives tail ratio q_s=2^{4-2nu_s}.
- Compress each far tail by H_{s,J}^+/(1-q_s), add finite near-annulus intervals, recovery errors, and the known Schur-Feshbach leakage L_+.
- Define Delta_R^- as the lower dominance margin; positive Delta_R^- promotes finite endpoint-box positivity after H,K, while nonpositive Delta_R^- is a valid falsifier for this R repair.

Blocking gap: The open gap is not conceptual vocabulary but certified sector input: outward-rounded same-theory bounds for H_{s,j}^+, nu_s, near-field constants, and E_rec over a fixed cutoff-flow window.

## Falsifiers

- falsifier: a Ward-subtracted sector has nu_s<=2, so dyadic annular compression is not summable.
- falsifier: outward-rounded adjacent annular ratios fail to form a cutoff-stable plateau below one.
- falsifier: the connected C4 sector interval dominates the positive pair baseline, giving Delta_R^-<=0.
- falsifier: raw Wilson hairpins and endpoint currents disagree beyond E_rec in the same-theory recovery map.
- falsifier: cusp or perimeter subtraction changes between pair and C4 evaluations, invalidating same-theory centering.
- falsifier: interval widths are larger than the claimed dominance margin, so positivity is numerically unresolved.
- falsifier: zero-pairing quotienting preserves the pair kernel but not the Ward-subtracted C4 sector kernels.

## Learning

Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, while positive flowed pair covariance, renormalization, and raw-hairpin recovery can each be valid and still be erased by connected C4. Declarative tension: endpoint positivity, same-theory flowed cumulants, and recovery maps must jointly hold; the missing mediator is a cutoff-stable annular Ward-Hessian dominance margin. Carrier critique: raw Wilson contours are fragmented and representation-limited; global OS spectral transfer, area-law intuition, and broad same-theory nontriviality witness selection are too coarse for this finite obstruction. Efficient representation: encode H,K endpoint sheet currents, cell moments, sector kernels, counterterms, recovery errors, and L_+; preserve gauge/color/reflection/orientation/cutoff/locality/same-theory invariants; use cumulant expansion, Ward/cusp subtraction, Taylor Hessians, dyadic tail compression, outward-rounded interval algebra, and certified zero-pairing equivalence; keep finite endpoint locality plus summable annuli; transfer only through centered flowed cumulants; demote on Ward, cusp, same-theory, summability, dominance, recovery, or interval-width falsifier. Hard gate: finite endpoint-box positivity after H,K; success promotes one finite Route A gate, failure quarantines this R repair. Conceptual value signal: R_{++}/kappa_4 is now a valid route-deciding color-geometric interval with a falsifier, not a symbolic boundary-OPE term. Clay existence, OS/Wightman axioms, nontrivial continuum limit, gauge-invariant observable density, large-field/topology control, OS spectral transfer, and positive Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search design, not as evidence for the Clay theorem.`
- Rationale: The branch has already reduced R_{++} to an annular dominance margin; another abstract restatement would loop. A concrete flowed-lattice endpoint experiment can decide whether the positive pair term plausibly survives connected C4 polarization in the same theory.
- Situation seed: Finite SU(3) Wilson lattice at fixed physical endpoint box: compute the gradient-flow connected cumulant of two centered H,K plus hairpins, recover endpoint sheet currents, and enclose the Ward-subtracted 3g,4g,ct,end sector kernels on dyadic annuli.
- Varied variable: The annular cutoff index J and associated plateau ratio bar q_s for the far C4 Hessian tails.
- Held-fixed controls: Same Wilson action, cutoff sequence, flow-time window, centering convention, and cusp/perimeter counterterms for pair and C4 parts., Fixed H,K endpoint geometry, plus-channel reflection symmetrization, color normalization, and Schur-Feshbach leakage L_+., Fixed recovery map from raw hairpins to endpoint currents with declared E_rec and zero-pairing quotient checks.
- Expected observation: Either the ratios r_{s,j} stabilize below one and Delta_R^- becomes positive after tail compression, or a sector plateau/dominance failure gives a clean finite falsifier for the endpoint repair.
- Transfer certificate needed: A same-theory interval certificate: Ward/cusp cancellation log, outward-rounded sector Hessian constants, recovery-error enclosure, zero-pairing verification, and a signed Delta_R^- inequality before any intuition affects proof obligations.

## Next Experiment

Route to proof search: run certified annular quadrature for the connected cumulant witness kappa_2(W_H^{cen}(t),W_K^{cen}(t)) in the same-theory nontriviality witness branch, compute sector constants H_{3g},H_{4g},H_{ct},H_{end}, verify plateau ratios, and output Delta_R^- with a promotion/quarantine decision.

# Gauge-Invariant Observable Density In The Excitation Sector / raw K4 endpoint stress audit

## Candidate Lemma

Finite signed-orbit stress lemma: in a fixed heat-kernel regulated Wilson endpoint box, diagonal upper bounds and one phased off-diagonal lower bound recovered from raw connected K4 orbits give a valid falsifier for post-H,K endpoint positive semidefiniteness.

## Definitions

- source object: heat-kernel regulated finite-volume SU(N) Wilson lattice measure at cutoff a, smearing sigma, coupling g_R, with reflected endpoint plaquette sheets and raw connected four-curvature cumulant intervals.
- target object: the finite post-H,K endpoint quadratic form U_sigma on the endpoint vector space E, whose positive semidefiniteness is the local Route A endpoint-box gate.
- controlled interface: a signed-orbit connected cumulant witness recovering phased lower bounds for U_pq and diagonal upper bounds D_i^+ from the same Wilson/OPE data and Schur blocks.
- same-theory condition: all intervals, Gaussian covariance, OPE error, and S_HK are computed with the identical cutoff, volume, regulator, coupling, Wilson basis, reflection split, and normalization.
- Q_i is the transported curvature-flux observable attached to endpoint sheet i, normal-ordered before taking Wilson cumulants.
- G_sigma is the Gaussian crossed-contraction matrix alpha_N g_R^4(C_sigma o conjugate(C_sigma)).
- K4_sigma is the compressed connected four-curvature cumulant matrix after exact Wilson trace quotienting.
- S_HK is the Schur-Feshbach hairpin subtraction B^*E^{-1}B in the same endpoint basis.

## Assumptions

- Model: finite lattice SU(N) Yang-Mills with heat-kernel plaquette regulator and gauge-invariant Wilson sheet observables only.
- Cutoff: a>0, sigma>=a, finite volume, finite endpoint box, and finite H,K Schur data are fixed throughout the lemma.
- Same-theory: the raw K4 intervals, Gaussian covariance, OPE error, and Schur blocks are all produced from the same regulated measure and Wilson normalization.
- Validity: interval arithmetic is outward-rounded and every quotient of plaquette words is justified by exact Wilson trace, orientation, reflection, and color identities.
- Local: the claim changes only the finite Route A endpoint-box PSD gate; it does not assert gauge-invariant observable density, OS reconstruction, continuum existence, or a Hamiltonian mass gap.
- Constraint: the signed-orbit carrier is used because scalar R is representation-limited, A012 shells lose phases, full Delta_raw is expensive, and OS Hilbert observable algebra is too strong for this local gate.

## Equations

- raw signed-orbit K4 recovery: `K^{(4)}_{pq,\sigma}\in \sum_{o\in\mathcal O_{pq}} m_o e^{i\phi_o} I_o(\sigma)`. Valid when: Valid when exact Wilson trace symmetries have grouped oriented plaquette quadruples without discarding phases, multiplicities, transporters, or color contractions.
- post-HK endpoint decomposition: `U_{ij,\sigma}=\alpha_N g_R^4(C_\sigma\circ\overline{C_\sigma})_{ij}+\frac{g_R^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma}-S^{HK}_{ij,\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after vacuum and perimeter terms cancel in the same normal-ordered Wilson/OPE expansion and after the H,K Schur compression is expressed in the endpoint basis.
- diagonal upper stress envelope: `D_i^+=G_{ii,\sigma}^+ + \frac{g_R^4}{16N^2}K_{ii,\sigma}^{(4),+}+e_{ii,\sigma}^+-s_{ii,\sigma}^-`. Valid when: Valid when G upper bounds, K4 interval upper endpoints, OPE upper errors, and Schur lower bounds are all computed for the same endpoint vector i.
- phased off-diagonal lower envelope: `L_{pq}(\theta)=\left[\frac{g_R^4}{16N^2}\ell^{(4)}_{pq}(\theta)-b^G_{pq}(\theta)-e^+_{pq,\sigma}-s^+_{pq,\sigma}\right]_+`. Valid when: Valid when ell captures the rigorous signed-orbit lower bound for the chosen phase theta and all non-K4 contributions are subtracted by absolute upper envelopes.
- two-sparse endpoint falsifier: `D_p^+<0\ \mathrm{or}\ D_q^+<0\ \mathrm{or}\ L_{pq}(\theta)^2>D_p^+D_q^+\quad\Longrightarrow\quad U_\sigma\not\succeq0`. Valid when: Requires the two endpoint coordinates p,q to be a principal compression of the same Hermitian endpoint matrix U_sigma with outward-rounded interval bounds.

## Attempted Derivation

- Conceptual pressure attacked: raw non-Gaussian Wilson K4 data must mediate to finite Schur-corrected endpoint PSD without falling back to OS-density cyclicity or scalar R rhetoric.
- Freeze the Clay target boundary: the local theorem may decide only finite post-H,K endpoint-box positivity; continuum YM existence, OS/Wightman reconstruction, observable density, and mass gap remain untouched.
- Represent each endpoint observable Q_i as a finite transported curvature-flux sum over oriented plaquettes in the heat-kernel cutoff theory.
- Normal-order the quadratic Wilson endpoint observable so vacuum and perimeter disconnected terms cancel before taking cum_2(:Q_i^2:,:Q_j^2:).
- Split the connected boundary-OPE polarization into the PSD Gaussian color square G_sigma, the raw connected four-curvature K4_sigma, the OPE interval E_OPE, and the Schur hairpin subtraction S_HK.
- Replace sign-losing A012 shells by signed raw orbit intervals that preserve endpoint phases, Hermiticity, exact Wilson quotienting, and same-theory normalization.
- For a chosen endpoint pair p,q and phase theta, compute diagonal upper envelopes D_p^+,D_q^+ and a phased off-diagonal lower envelope L_pq(theta).
- Use the PSD principal-minor inequality |U_pq|^2<=U_pp U_qq; if a certified upper/lower interval violates it, obtain a valid finite falsifier for U_sigma PSD.

Blocking gap: The branch still lacks actual validator-facing raw same-regulator K4 orbit intervals I_o(sigma) for the first H,K endpoint geometry; without them L_pq(theta) and D_i^+ are formal recovery functionals, not computed certificates.

## Falsifiers

- A raw K4 interval table with regulator or Wilson-basis mismatch is a falsifier for the signed-orbit transfer certificate.
- A non-invariant quotient whose orbit phase changes under another exact Wilson reduction invalidates the stress witness.
- OPE overflow e_{pq}^+ large enough to make L_pq(theta)=0 for all pairs demotes the negative tactic to full Delta_raw search.
- If D_i^+ cannot be made rigorous because S_HK or K4 diagonal intervals are absent, no valid endpoint falsifier exists.
- A certified negative stress margin kills only this finite H,K collar/hairpin endpoint route, not the Clay problem.

## Learning

Cycle 343 attacks the conceptual pressure that raw non-Gaussian Wilson K4 cumulants need a mediator to a finite endpoint PSD decision without OS-density circularity. Declarative tension: Wilson/OPE data, K4 intervals, OPE error, and S_HK must all be valid in one cutoff theory, but Clay-level OS reconstruction, gauge-invariant observable density, excitation-sector cyclicity, continuum existence, and mass gap are non-claims. Carrier critique: scalar R is too weak, A012 shells lose signs, OS Hilbert observable algebra is too strong, full Delta_raw is complete but expensive, and signed raw orbits are efficient because they preserve phases, Hermiticity, gauge invariance, exact Wilson quotienting, and same-theory normalization. Hard gate: D_i^+<0 or L_pq(theta)^2>D_p^+D_q^+ gives a valid finite falsifier; failure gives no positivity and routes to full Delta_raw proof search or quarantine. Conceptual value signal: sharp and route-changing at finite scope because Gaussian color positivity, connected non-Gaussian K4, OPE error, and Schur hairpin energy are unified in one connected cumulant witness while every Clay frontier gate remains untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and validator-facing data design.`
- Rationale: The abstraction is looping unless it produces raw K4 intervals; a concrete thought experiment fixes which orbit amplitudes and phases must be computed before the branch can move.
- Situation seed: Finite SU(2) heat-kernel lattice endpoint box for the first H,K Wilson collar/hairpin geometry: choose two reflected endpoint sheets p,q sharing one boundary plaquette ribbon and enumerate the raw plaquette quadruples in cum_2(:Q_p^2:,:Q_q^2:).
- Varied variable: The smearing-to-cutoff ratio beta_sigma=sigma/a, varied over beta_sigma in {1,2,4} while the endpoint geometry and H,K Schur blocks are held fixed.
- Held-fixed controls: Same Wilson action, volume, cutoff a, renormalized coupling g_R, reflection split, and heat-kernel regulator for every interval., Same endpoint Wilson basis, same Q_i normal-ordering, same exact Wilson quotient identities, same OPE error convention, and same S_HK matrix., No use of OS Hilbert observable algebra, gauge-invariant observable density, continuum extrapolation, or mass-gap spectral transfer.
- Expected observation: If signed K4 orbit phases align along the shared boundary ribbon, L_pq(theta)^2 may exceed D_p^+D_q^+ at small beta_sigma and give a finite falsifier; if phases cancel or OPE bounds dominate, the branch must abandon the two-sparse tactic and compute full Delta_raw.
- Transfer certificate needed: A same-theory connected cumulant witness: raw orbit interval table I_o(sigma), exact quotient audit, Hermitian phase check, diagonal/off-diagonal interval arithmetic, and a recorded inequality D_i^+<0 or L_pq(theta)^2>D_p^+D_q^+.

## Next Experiment

Proof search: enumerate the first SU(2) heat-kernel H,K endpoint pair p,q, build the signed raw K4 orbit table for cum_2(:Q_p^2:,:Q_q^2:), compute D_p^+,D_q^+,L_pq(theta) for theta in {0,pi/2,pi,3pi/2}, and either output a finite falsifier or quarantine this tactic.

