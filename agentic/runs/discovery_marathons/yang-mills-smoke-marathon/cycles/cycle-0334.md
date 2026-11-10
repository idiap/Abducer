# cycle-0334

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint Source Interval Carrier for Post-H,K Wilson Gate

## Candidate Lemma

For the fixed three-hairpin post-H,K block, C_ep is a valid finite carrier: aggregate source-equivalent endpoints before clipping; I_gate bounds the corrected endpoint R term. I_->=0 promotes this finite gate; I_+<0 is a same-theory falsifier; otherwise quarantine.

## Definitions

- source object: heat-kernel regulated SU(N) plaquette-sheet endpoint source classes c for the fixed three-hairpin Wilson block after H,K, with log Z_c(sL_c) measured in the original gauge-invariant lattice theory.
- target object: the finite post-H,K Schur-Feshbach OS null-channel scalar I_gate for this Wilson block; it is not a continuum Schwinger family, Wightman theory, or mass-gap statement.
- controlled interface: C_ep aggregates source-equivalent endpoints before clipping, multiplies signed incidences D_c by connected cumulant witness intervals K_c, adds C_N, M_G, and T_tail, then exports one interval.
- same-theory condition: sources differentiate the same normalized Wilson products used in the collar OS matrix; reflection, cutoff, gauge invariance, and observable algebra are unchanged, with no boundary counterterm.
- declarative tension: collar OS positivity, fixed Wilson observables, and singular endpoint OPE must coexist; H,K and half-overlap shielding do not decide the endpoint scalar.
- carrier audit: raw R is too weak, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K.
- efficient representation: encode source classes, seven source values, K intervals, D incidences, C_N, M_G, and T_tail; preserve null cancellations; use source differencing, interval product, color scaling, and tail addition.
- equivalence policy: endpoint carriers are identified only when their regulated source data agree; locality cost outside endpoint boxes is charged to T_tail.

## Assumptions

- Model: finite 4D SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflected Wilson hairpin observables at fixed cutoff and volume.
- Regime: small collar collapse after the H,K Schur-Feshbach reduction, with endpoint boxes disjoint except for overlap charged to T_tail.
- Uniformity: K_c intervals and T_tail are cutoff-uniform for this finite block; otherwise the transfer is invalid.
- Same-theory: no gauge fixing, boundary counterterm, normalization change, or Wilson algebra enlargement is allowed.
- Local: success changes only the finite post-H,K reflected-Wilson OS gate; continuum existence, observable density, OS spectral transfer, and mass gap remain untouched.

## Equations

- endpoint incidence carrier: `D_c=2b_{12,c}-4b_{13,c}-4b_{23,c},\quad R_{\rm end}\in C_N\sum_c D_c\,\mathcal K_c+[-T_{\rm tail},T_{\rm tail}]`. Valid when: Valid when C_ep source classes use equal regulated endpoint data, signed incidences are aggregated before clipping, and nonendpoint overlap is bounded by T_tail.
- seven point cumulant interval: `\mathcal K_c\subset h^{-4}\sum_{r=-3}^{3}w_r\log Z_c(rh;L_c)+[-7h^4M_{8,c}/240,7h^4M_{8,c}/240]`. Valid when: Applies when log Z_c is the same-theory endpoint source partition function, is C^8 in s, and the source step h stays inside the heat-kernel chart.
- finite gate decision: `I_{\rm gate}=[I_-,I_+]=M_G+R_{\rm end},\quad I_-\ge0\Rightarrow {\rm pass},\quad I_+<0\Rightarrow {\rm falsifier}`. Valid when: Valid when the H,K Schur-Feshbach reduction has already removed the vacuum direction and all stated endpoint intervals enclose their regulated values.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel regulated SU(N) plaquette-sheet endpoint source classes c for the fixed three-hairpin Wilson block after H,K, with log Z_c(sL_c) measured in the original gauge-invariant lattice theory.; target object: the finite post-H,K Schur-Feshbach OS null-channel scalar I_gate for this Wilson block; it is not a continuum Schwinger family, Wightman theory, or mass-gap statement.; Model: finite 4D SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflected Wilson hairpin observables at fixed cutoff and volume..
- Use heat-kernel plaquette sheets. In the post-H,K null channel, Wick-square four-flux contractions are positive Gram terms and cannot be the demoting R contribution.
- The null incidence identity cancels the straight f f contact; one-body Wilson factors vanish on the reduced channel, so only endpoint connected four-flux cumulants and tails remain.
- Group endpoints by equal regulated log Z source data. Sum D_c=2b12-4b13-4b23 inside each class before multiplying by K_c; this preserves cancellations lost by raw R.
- Interval arithmetic gives I_gate. I_->=0 promotes the finite gate; I_+<0 gives a realized same-theory determinant falsifier; otherwise the branch remains quarantined.

Blocking gap: No computed seven-point heat-kernel endpoint source intervals or cutoff-uniform T_tail are available; the root-quartic screen alone is not decisive.

## Falsifiers

- falsifier: a source class with D_c>0 and certified K_c<0 makes I_+<0 after tail control; the finite same-theory OS block demotes.
- falsifier: T_tail is not cutoff-uniform or needs a boundary counterterm; then C_ep is not a valid same-theory carrier.
- falsifier: source-equivalent aggregation hides unequal regulated log Z data, so incidence cancellations are representation artifacts.
- falsifier: the seven-point source probe changes Wilson normalization or leaves the heat-kernel chart, invalidating connected cumulant witness intervals.

## Learning

Conceptual pressure: endpoint collapse must be sign-certified in the same Wilson theory. C_ep turns R into an exact interval product; negative endpoint cumulants demote only through positive-D leakage plus uniform tail. Hard gate: finite post-H,K OS scalar; success promotes this block, failure falsifies it, missing data keeps quarantine.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch was looping on quarantine language. A concrete endpoint source experiment tests the finite post-H,K gate without restating OS closed-cone topology or claiming a continuum theorem.
- Situation seed: Fixed SU(N) heat-kernel plaquette-sheet three-hairpin endpoint box; compute seven values log Z_c(rh;L_c) for each source-equivalent endpoint class and the D_c incidences after H,K.
- Varied variable: endpoint dominance eta_c=b12,c/(b13,c+b23,c+epsilon), swept from half-overlap shield to 12-only dominance while h, regulator, and box scale are fixed.
- Held-fixed controls: heat-kernel regulator and same normalized gauge-invariant Wilson loops, H,K null channel and incidence weights 2,-4,-4, no boundary counterterm, gauge fixing, or observable-algebra enlargement, fixed color factor C_N, Gaussian margin M_G, and T_tail protocol
- Expected observation: eta near the shield should give protective or harmless intervals; 12-dominant classes with negative K_c threaten I_gate. I_+<0 is a finite falsifier; I_->=0 promotes only this block.
- Transfer certificate needed: Same-theory equality of regulated source data, cutoff-uniform C^8 stencil bounds, uniform T_tail, and proof that the probe is the locked Wilson observable; no OS spectral transfer or mass-gap inference follows.

## Next Experiment

Route to proof search plus validator endpoint stencil: compute log Z_c(rh;L_c), form connected cumulant witness intervals K_c, aggregate D_c before clipping, add C_N,M_G,T_tail, and return I_gate; remain quarantined until data arrive.

# Annular plateau certificate for the H,K endpoint Wilson mediator

## Candidate Lemma

Conditional finite Route A certificate: an outward-rounded annular plateau enclosure for the Ward-subtracted flowed hairpin cumulant gives a rigorous lower bound for the endpoint mediator R_{++}^{ren}; if the resulting margin beats the Schur-Feshbach leakage L_+, the post-H,K endpoint-box positivity gate is promoted, and if it fails the R repair is quarantined.

## Definitions

- source object: centered gradient-flowed Wilson hairpin covariance R_{++}^{ren}(t,eta) for the fixed H,K endpoint sheet currents in one cutoff Yang-Mills family.
- target object: finite endpoint-box Schur-Feshbach positivity margin Delta_R for the plus channel after the H,K reduction, not the Clay mass gap.
- controlled interface: Ward/cusp-subtracted endpoint sheet-current representation with cell moments, sector Hessian kernels, dyadic annuli, recovery errors, and leakage L_+.
- same-theory condition: raw hairpins, flowed hairpins, counterterms, recovery maps, and cumulants are taken along the same regulator sequence, coupling normalization, boundary geometry, and OS-positive candidate Schwinger family.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with Wilson plaquette action, positive gradient-flow time t, and fixed finite endpoint boxes before any continuum claim.
- Regime: endpoint cell diameter eta satisfies eta < c sqrt(8t) and annuli start outside the near box so heat-kernel Hessian bounds are finite.
- Cutoff: constants are uniform over lattice spacings a <= a0 with t and eta held in physical units for this finite certificate.
- Same-theory: the centered flowed Wilson cumulant is recovered from the same raw H,K hairpins with a certified error E_rec^+, so no auxiliary theory supplies R_{++}.
- Validity: Ward subtraction removes gauge-gradient pieces, cusp/perimeter counterterms are one-hairpin local, and plus-channel monopole and dipole moments vanish in the quotient current.
- Local: the claim changes only finite endpoint-box positivity after H,K; continuum existence, observable density, OS spectral transfer, and Hamiltonian mass gap remain untouched.

## Equations

- annular-lower-bound: `R_{++}^{ren,-}=g_t^4 (N^2-1)\left(2G_{++}^{-}-N M_{2,+}^2\sum_{s\in\{3g,4g,ct,end\}}(H_{s,near}^{+}+T_s^{+})\right)-E_{rec}^{+}-E_6^{+}`. Valid when: Valid when the flowed hairpin cumulant is expanded in endpoint sheet currents, Ward and cusp subtractions are certified, and all interval constants are outward rounded for the same cutoff family.
- dyadic-tail-compression: `T_s^{+}(J)=\sum_{j\ge J}A_{s,j}^{+}\le \frac{A_{s,J}^{+}}{1-q_s^{+}},\qquad q_s^{+}:=\max_{j\in[J,J+r]}\frac{A_{s,j+1}^{+}}{A_{s,j}^{+}}<1`. Valid when: Applies after annular sector bounds are nonnegative, plateau ratios are computed on consecutive far annuli, and heat-kernel Hessian decay dominates endpoint-cell volume growth.
- promotion-margin: `\Delta_R^{-}:=R_{++}^{ren,-}-L_{+},\qquad \Delta_R^{-}>0\Rightarrow Q_{+}^{ren}>0`. Valid when: Requires the finite Schur-Feshbach H,K leakage L_+ to be already certified and the lower interval for R_{++}^{ren} to use the identical plus-channel normalization.
- quarantine-margin: `R_{++}^{ren,+}<L_{+}\quad\text{or}\quad q_s^{+}\ge1\ \text{for some }s\ \Rightarrow\ \text{quarantine endpoint R repair}`. Valid when: Valid as a branch-control conclusion when upper intervals, plateau ratios, or summability tests are certified in the same endpoint geometry and cutoff regime.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: centered gradient-flowed Wilson hairpin covariance R_{++}^{ren}(t,eta) for the fixed H,K endpoint sheet currents in one cutoff Yang-Mills family.; target object: finite endpoint-box Schur-Feshbach positivity margin Delta_R for the plus channel after the H,K reduction, not the Clay mass gap.; Model: four-dimensional SU(N) lattice Yang-Mills with Wilson plaquette action, positive gradient-flow time t, and fixed finite endpoint boxes before any continuum claim..
- Start with the same-theory centered cumulant R_{++}^{ren}=kappa_2(W_+^{flow}-<W_+^{flow}>,W_+^{flow}-<W_+^{flow}>) after one-hairpin perimeter and cusp subtraction.
- Expand the thin endpoint hairpins to fourth curvature order inside the endpoint sheet-current representation; the Gaussian pair term gives +2g_t^4(N^2-1)G_{++}.
- Use Ward subtraction to remove longitudinal gauge-gradient kernels and use plus-channel monopole/dipole cancellation to make the connected C4 remainder depend on mixed Hessians rather than on zeroth or first endpoint moments.
- Partition the complement of the near endpoint box into dyadic annuli; for each sector s in {3g,4g,ct,end}, bound the annular Hessian contribution by A_{s,j}^+ M_{2,+}^2.
- Compress the far tail by a plateau ratio q_s^+<1, giving T_s^+(J)<=A_{s,J}^+/(1-q_s^+), and add near constants, recovery error, and sixth-order Taylor error.
- Subtract the finite Schur-Feshbach leakage L_+ from the resulting lower interval; Delta_R^->0 promotes endpoint-box positivity, while failure is a real falsifier for this R-mediated repair.

Blocking gap: The proof queue still lacks certified outward-rounded numerical or analytic intervals for G_{++}^-, H_{s,near}^+, A_{s,J}^+, q_s^+, E_rec^+, and E_6^+ in the fixed H,K geometry.

## Falsifiers

- falsifier: the annular plateau ratio q_s^+ is >= 1 or unstable under one refinement of the endpoint partition.
- falsifier: Ward or cusp subtraction leaves a nonlocal boundary term not absorbed by E_rec^+.
- falsifier: the connected C4 upper majorant N M_{2,+}^2 sum_s(H_{s,near}^+ + T_s^+) exceeds the positive pair baseline 2G_{++}^- by more than L_+.
- falsifier: zero-pairing quotienting discards a current with visible pairing against a retained sector kernel.
- falsifier: the lower margin is positive only at finite cutoff and has no valid cutoff-uniform plateau window.

## Learning

Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, but positive flowed pair covariance and raw-hairpin recovery can both be valid while connected C4 destroys R_{++}. Declarative tension: endpoint positivity, same-theory flowed Wilson cumulants, and recovery maps must jointly hold; the missing mediator is a cutoff-stable annular Ward-Hessian dominance margin. Carrier critique: raw contours are too fragmented, while global OS spectral transfer, area-law intuition, and broad same-theory nontriviality witness routes are too coarse for this finite obstruction. Efficient representation requirements are now precise: encode H,K sheets, endpoint currents, cell moments, sector kernels, counterterms, recovery errors, and L_+; preserve gauge/color/reflection/orientation/cutoff/locality/same-theory invariants; use cumulant expansion, Ward/cusp subtraction, endpoint Taylor remainders, heat-kernel majorants, dyadic tail compression, outward-rounded interval algebra, and certified zero-pairing quotienting; keep finite endpoint cells plus summable annuli; transfer only through centered flowed Wilson cumulants; demote on any falsifier. Conceptual value signal: R_{++}/kappa_4 is a route-deciding finite annular sign/size certificate, not a symbolic boundary-OPE term. Hard gate: finite endpoint-box positivity after H,K; success promotes one finite Route A gate, failure quarantines this repair while Clay existence, OS/Wightman axioms, nontriviality, observable density, large-field/topology control, OS spectral transfer, and mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete thought experiment now as a falsifier probe and proof-search guide.`
- Rationale: The branch has been repeating plateau language; the next valid move must expose whether the connected boundary-OPE polarization is summably smaller than the positive pair covariance in the actual H,K endpoint geometry.
- Situation seed: SU(2) Wilson lattice Yang-Mills with gradient-flow time t, fixed H,K plus-channel endpoint sheet currents, one near endpoint box, and dyadic annuli carrying Ward-Hessian sector kernels for the connected cumulant witness R_{++}.
- Varied variable: rho=sqrt(8t)/eta, equivalently the flow-radius to endpoint-cell diameter ratio controlling Hessian decay and annular plateau ratios.
- Held-fixed controls: same cutoff sequence, Wilson action, bare-to-flow coupling convention, and recovery maps for raw and flowed hairpins, fixed H,K endpoint geometry, plus-channel orientation, Ward/cusp subtraction prescription, and Schur-Feshbach leakage L_+, fixed outward-rounded interval arithmetic and zero-pairing quotient tests for all retained sector kernels
- Expected observation: For a valid mediator window, G_{++}^- is stable while q_s^+(rho)<1 and Delta_R^-(rho)>0 on a nontrivial rho interval; if q_s^+ drifts to 1 or Delta_R^- stays negative, the endpoint R repair is demoted.
- Transfer certificate needed: A cutoff-uniform interval quadrature certificate for the pair term, near constants, annular ratios, recovery errors, and Taylor remainder, plus verification that the cumulant is the same-theory flowed Wilson cumulant used by the finite H,K Schur-Feshbach gate.

## Next Experiment

Route to proof search: build the validator-facing interval table for the same-theory nontriviality witness boundary, namely the connected cumulant witness R_{++}; compute G_{++}^-, H_{s,near}^+, A_{s,J}^+, q_s^+, E_rec^+, E_6^+, and Delta_R^- for SU(2) and SU(3) H,K endpoint geometry with outward rounding, then promote only on Delta_R^->0 or quarantine on the stated falsifier.

# Gauge-Invariant Observable Density In The Excitation Sector / finite Route A raw K4 endpoint audit

## Candidate Lemma

Signed-orbit raw K4 stress lemma: for a fixed heat-kernel cutoff and fixed H,K endpoint basis, exact signed orbit intervals for the connected four-curvature Wilson cumulant recover a Hermitian interval enclosure of the Schur-corrected endpoint form U_sigma. If D_i^+<0 or L_{ij}(theta)^2>D_i^+D_j^+, then U_sigma is not positive semidefinite. This is a finite falsifier for the worked collar/hairpin endpoint route; survival of the test is not a proof of positivity.

## Definitions

- source object: heat-kernel regulated SU(N) Wilson endpoint data consisting of oriented plaquette sheets, transported curvature insertions, raw connected K4 cumulant intervals, OPE intervals, and H,K Schur blocks.
- target object: the finite Hermitian post-H,K endpoint quadratic form U_sigma on the endpoint-box span, with target property U_sigma >= 0 or an explicit negative Rayleigh stress.
- controlled interface: the recovery map Rec_orb that sums exact Wilson trace-orbit intervals with phases, color tensors, sheet weights, OPE errors, and Schur subtraction into U_sigma interval data.
- same-theory condition: the cutoff a, smoothing sigma, coupling g_R(sigma), Wilson normalization, endpoint basis, gauge measure, and H,K Schur data are identical in every recovered term.
- connected cumulant witness: R_ij is represented by raw cumulants of transported curvature products, not by scalar R, A012 shell envelopes, or OS Hilbert observable algebra.
- efficient carrier: signed raw plaquette orbits encode orientation, phase, color tensor, multiplicity, endpoint indices, and exact quotient identities while preserving Hermiticity and gauge invariance.

## Assumptions

- Model: finite four-dimensional Euclidean heat-kernel cutoff Yang-Mills with compact gauge group SU(N), fixed reflection plane, and finite endpoint boxes.
- Cutoff: a, sigma, g_R(sigma), Wilson-loop normalization, and OPE truncation order are held fixed across Gaussian, K4, OPE, and Schur terms.
- Same-theory: the cumulants, recovery map, and H,K Schur subtraction use one cutoff measure and no imported regulator, sector projection, advice, or representation change.
- Local: the lemma concerns only the finite post-H,K collar/hairpin endpoint compression and makes no continuum, volume-uniform, OS reconstruction, or mass-gap claim.
- Validity: raw intervals must enclose connected cumulants after vacuum and perimeter disconnected cancellations, with exact Wilson quotienting and Hermitian interval closure.

## Equations

- transported endpoint flux: `Q_i(\sigma)=\sum_{p\in P_i} w_{i,p}\,\operatorname{Ad}_{U_{\gamma_{i,p}}} F_p(\sigma)`. Valid when: Valid when the heat-kernel transported plaquette curvatures are evaluated at fixed cutoff, fixed smoothing scale, and fixed endpoint sheet weights.
- signed orbit K4 recovery: `K^{(4)}_{ij}\in \sum_{\mathcal O\in \mathrm{Orb}(i,j)} m_{\mathcal O}\,\zeta_{\mathcal O}\,T_{\mathcal O}\,[\ell_{\mathcal O},u_{\mathcal O}]`. Valid when: Valid when orbit quotients are exact Wilson trace symmetries and no absolute-value shell compression has been applied.
- Schur-corrected endpoint matrix: `U_{ij}=\alpha_N g_R^4( C_\sigma\circ \overline{C_\sigma})_{ij}+\frac{g_R^4}{16N^2}K^{(4)}_{ij}+E^{\mathrm{OPE}}_{ij}-S^{HK}_{ij},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after vacuum and perimeter disconnected terms cancel inside the same cutoff Wilson cumulant expansion.
- phase interval and lower modulus: `I_{ij}(\theta)\supset \operatorname{Re}(e^{-i\theta}U_{ij}),\quad L_{ij}(\theta)=\operatorname{dist}(0,I_{ij}(\theta)),\quad D_i^+\ge U_{ii}`. Valid when: Requires Hermitian interval enclosure of the same Schur-corrected endpoint compression for nodes p and q.
- two-sparse PSD falsifier: `D_i^+<0\ \mathrm{or}\ \exists\theta:\ L_{ij}(\theta)^2>D_i^+D_j^+\ \Longrightarrow\ U_\sigma\not\succeq 0`. Valid when: Valid when D_p^+ and D_q^+ are finite upper diagonal enclosures for the same Hermitian endpoint matrix.

## Attempted Derivation

- Freeze the Clay claim level: this cycle attacks only the finite Route A post-H,K endpoint-box gate, not gauge-invariant observable density, excitation-sector cyclicity, OS reconstruction, continuum existence, or the Hamiltonian mass gap.
- Write each endpoint Wilson polarization as a connected cumulant of transported curvature fluxes Q_i; vacuum and perimeter terms cancel before R_ij is assembled.
- Separate R_ij into the PSD Gaussian color square with alpha_N=(N^2-1)/(8N^2), the non-Gaussian connected K4 cumulant, the same-regulator OPE remainder, and the H,K Schur subtraction S_HK.
- Replace sign-losing A012 shell envelopes by exact signed orbit intervals m_O zeta_O T_O[ell_O,u_O]; this preserves phase, color, sheet geometry, Hermiticity, and exact Wilson quotient identities.
- For any endpoint pair i,j and phase theta, form an interval I_ij(theta) for Re(e^{-i theta}U_ij), upper diagonal enclosures D_i^+,D_j^+, and lower distance L_ij(theta).
- Use the 2x2 PSD necessary condition |U_ij|^2<=U_ii U_jj; the interval condition D_i^+<0 or L_ij(theta)^2>D_i^+D_j^+ gives a rigorous negative Rayleigh stress.

Blocking gap: No same-regulator raw signed K4 orbit intervals have been produced for the first H,K endpoint pair; without them the stress gate is valid but not instantiated.

## Falsifiers

- falsifier: a recovered same-regulator pair with D_i^+<0 immediately kills finite endpoint positivity for this H,K route.
- falsifier: a phase theta with L_ij(theta)^2>D_i^+D_j^+ gives a two-sparse negative Rayleigh stress.
- Regulator mismatch between K4 intervals and S_HK invalidates the entire recovery map.
- Exact Wilson quotienting that changes signs or loses Hermiticity demotes the signed-orbit carrier.
- OPE interval overflow larger than the stress margin prevents any valid route decision.
- If all two-sparse stresses fail and full Delta_raw also lacks a positive Loewner lower bound, the endpoint route remains quarantined rather than promoted.

## Learning

Conceptual pressure attacked: R must be an actual same-theory connected cumulant witness, not scalar endpoint rhetoric, A012 shell aspiration, OS Hilbert observable algebra, or a gauge-invariant observable density restatement. Declarative tension: Wilson/OPE data, raw non-Gaussian K4, OPE error, and S_HK must jointly control one finite endpoint quadratic form in one cutoff theory, while continuum OS reconstruction, excitation-sector cyclicity, nontrivial YM, observable density, and the mass gap are barred. Carrier revision: scalar R is too weak, A012 is sign-losing, full Delta_raw is complete but expensive, and signed raw orbits are efficient because phases and exact quotient identities are preserved. Hard gate: D_i^+<0 or L_ij(theta)^2>D_i^+D_j^+ changes the proof state only by falsifying the finite H,K endpoint route; survival forces full Delta_raw proof search. Conceptual value signal: sharp and route-changing at finite scope because Gaussian color positivity, non-Gaussian K4 danger, OPE error, and Schur hairpin energy are unified in one valid inequality while every Clay frontier gate remains untouched.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch has exhausted abstract R, A012, and phase-stress restatements. A concrete same-regulator signed-orbit experiment is needed to decide whether the connected cumulant witness can actually falsify the H,K endpoint gate.
- Situation seed: SU(2) heat-kernel cutoff on one finite four-dimensional endpoint box with two reflected Wilson sheet-pair nodes p,q from the worked H,K collar/hairpin geometry; compute representative raw K4 orbit intervals entering U_pq and U_pp,U_qq.
- Varied variable: smoothing ratio r=sigma/a^2, with phases theta sampled only to certify the best lower off-diagonal interval distance.
- Held-fixed controls: Same cutoff lattice, gauge group, heat-kernel regulator, coupling g_R(sigma), and Wilson normalization for K4, OPE, Gaussian, and Schur terms., Fixed H,K endpoint basis, reflected support, endpoint geometry, exact Wilson quotient policy, and finite endpoint-box complexity budget., No continuum limit, OS Hilbert observable algebra, or gauge-invariant observable density claim is allowed during the experiment.
- Expected observation: Either signed orbit phases produce a stable lower off-diagonal K4 contribution exceeding the Gaussian-Schur-OPE diagonal threshold, giving a finite falsifier, or cancellations keep L_pq^2 below D_p^+D_q^+ and force full Delta_raw proof search.
- Transfer certificate needed: A validator-facing table of raw K4 orbit intervals with regulator labels, color tensors, phases, multiplicities, OPE interval, Schur block, Hermiticity audit, and interval proof of D_i^+<0 or L_pq(theta)^2>D_i^+D_q^+ before intuition may affect proof obligations.

## Next Experiment

Proof search: build the first validator-facing connected cumulant witness table for one H,K endpoint pair p,q under the heat-kernel regulator; compute signed raw K4 orbit intervals, Gaussian color-square contribution, OPE interval, and S_HK entries, then test D_i^+<0 or L_pq(theta)^2>D_i^+D_q^+. If the table is unavailable, quarantine this branch rather than returning to gauge-invariant observable density or OS Hilbert observable algebra rhetoric.

