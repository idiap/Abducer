# cycle-0314

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint root-quartic screen for the post-H,K Wilson block

## Candidate Lemma

Clipped root-quartic endpoint screen: for the heat-kernel plaquette-sheet three-hairpin block, after the H,K Schur-Feshbach reduction and the known Wick-square and straight f f cancellations, the finite same-theory OS gate is promoted by a computable lower interval depending only on positive-D endpoint leakage, source-derivative errors, and a tail budget.

## Definitions

- source object: heat-kernel plaquette-sheet SU(N) endpoint source classes C with regulated log partition functions Z_c(s) and signed fractional incidences b_ij(c).
- target object: the finite post-H,K reflected-Wilson OS gate for the locked three-hairpin block, represented by a scalar lower interval I_gate.
- controlled interface: C_ep maps endpoint connected fourth source derivatives and signed incidences to the Schur-Feshbach scalar without adding boundary counterterms.
- same-theory condition: the Wilson loops, source insertions, heat-kernel regulator, normalization, and recovery maps are identical before collar collapse and at the finite OS gate.
- endpoint observable: kappa_c=partial_s^4 log Z_c(sL_c)|_{s=0} is the connected cumulant witness for the endpoint source class c.
- incidence dominance: D_c=2b_12(c)-4b_13(c)-4b_23(c) is the null-channel endpoint leakage coefficient.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action, finite volume, and a reflection plane cutting only the regulated Wilson collars.
- Regime: endpoint boxes are smaller than the collar scale but larger than the plaquette cutoff, so the local heat-kernel source expansion and endpoint/tail separation are valid.
- Cutoff: the endpoint expansion has kappa_c=-(t_c^4/60)R4(L_c)+E_c with |E_c|<=epsilon_c uniformly over the selected endpoint classes.
- Same-theory: no boundary counterterm, no change of Wilson normalization, and no enlargement of the gauge-invariant observable algebra is allowed during collar collapse.
- Uniformity: T_tail and epsilon_c are bounded independently of cutoff along the regulator/RG subsequence used for the finite block.
- Validity: Wick-square Gram terms are kept positive or discarded, and straight C_A f f contacts cancel by the already verified null-incidence identity.

## Equations

- endpoint_gate: `I_{\mathrm{gate}}=M_G+C_N\sum_{c\in C}D_c\,\kappa_c+T_{\mathrm{tail}}`. Valid when: Valid when endpoint classes are source-equivalent and all non-endpoint Wilson contractions are either included in M_G or charged to T_tail.
- signed_leakage: `D_c=2b_{12}(c)-4b_{13}(c)-4b_{23}(c),\qquad b_{ij}(c)\in[0,1]`. Valid when: Valid when b_ij are the fractional endpoint incidences of the same regulated hairpin footprints after source-class aggregation.
- root_quartic_cumulant: `\kappa_c=-\frac{t_c^4}{60}\,R_4(L_c)+E_c,\qquad R_4(L)=N\operatorname{tr}(L^4)+3(\operatorname{tr}(L^2))^2\ge0`. Valid when: Valid in heat-kernel endpoint coordinates after the Haar-Jacobian expansion is controlled through fourth source order.
- clipped_lower_screen: `I_{\mathrm{gate}}\ge M_G-C_N\sum_{c\in C}\left([D_c]_+\frac{t_c^4}{60}R_4(L_c)+|D_c|\epsilon_c\right)-|T_{\mathrm{tail}}|`. Valid when: Valid when C_N is positive and the only signed endpoint uncertainty is the uniform remainder E_c and tail term.
- half_overlap_shield: `b_{13}(c)+b_{23}(c)\ge \frac12 b_{12}(c)\quad\Longrightarrow\quad D_c\le0`. Valid when: Valid for the three-hairpin null weights used in this block and before any non-source-equivalent endpoint aggregation.

## Attempted Derivation

- Conceptual pressure attacked: endpoint collapse must be sign-certified inside the same Wilson theory rather than hidden in symbolic R or in a raw kappa_4 spectrum.
- Declarative tension: fixed-collar reflection positivity, fixed gauge-invariant Wilson observables, and a singular connected endpoint boundary OPE must jointly hold; the missing mediator is a cutoff-uniform signed endpoint source carrier with no boundary theory.
- Carrier audit: raw R is representation-limited because it hides b_ij signs; raw kappa_4 spectra are too strong because negative endpoint cumulants are protective when D_c<=0; global Schur-preimage positivity is valid but too coarse after H,K.
- Use the already established H,K finite block and null vector to isolate the post-H,K scalar M_G plus endpoint connected polarization and tail.
- In heat-kernel plaquette-sheet regulation, connected log derivatives remove Wick-square contractions; the straight C_A f f contact cancels by the null-incidence identity, leaving endpoint source cumulants and T_tail.
- Expand each endpoint source class in heat-kernel coordinates: the SU(N) Haar-Jacobian root-quartic term gives kappa_c=-(t_c^4/60)R4(L_c)+E_c with R4(L_c)>=0.
- Contract with the signed null-channel incidence D_c=2b12-4b13-4b23. The dangerous contribution is only [D_c]_+ times the negative root-quartic cap; D_c<=0 is shielded up to the error |D_c|epsilon_c.
- Therefore a valid finite promotion certificate is M_G greater than the clipped positive-D root-quartic cap plus uniform source and tail errors. A valid falsifier is a certified negative sign interval for the same scalar.

Blocking gap: The branch still lacks actual validator-facing endpoint source intervals, uniform M8 or epsilon_c bounds for all source classes, and a cutoff-uniform T_tail estimate in the interacting four-dimensional regulator.

## Falsifiers

- A source-equivalent endpoint class with D_c>0 and a seven-point connected cumulant witness whose upper endpoint makes I_gate<0 is a finite same-theory falsifier.
- The eighth-derivative bound M8(c) or the endpoint tail T_tail grows as the cutoff is removed, so the claimed interval is not valid uniformly.
- A boundary counterterm is needed to define Z_c(sL_c) at the reflected endpoint, which violates the same-theory condition.
- Geometric endpoint aggregation merges non-equivalent source classes and changes the signed incidence contraction.
- A nonlocal corner tail couples separated endpoint classes in a way not charged to T_tail, invalidating the clipped locality budget.

## Learning

Cycle 314 sharpens quarantine into a clipped analytic screen. The hard gate is the finite post-H,K reflected-Wilson OS transfer scalar: success gives a finite same-theory promotion certificate, failure gives a finite falsifier, and missing source data keeps quarantine. The conceptual value signal is sharpness: negative SU(N) root-quartic endpoint cumulants are not the obstruction; only source-certified positive-D leakage plus uniform tail can demote the block. This is novel only at finite Route A scope and leaves all Clay-level continuum and mass-gap gates open.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe and validator-facing endpoint computation design.`
- Rationale: The branch has already reduced the Wilson/OS obstruction to a finite post-H,K endpoint scalar; another abstract restatement would not decide promotion, while source intervals can.
- Situation seed: In finite-volume four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action, take the locked three-hairpin reflected Wilson collar block and replace each endpoint box by a source class c with seven evaluations of log Z_c(sL_c).
- Varied variable: The fractional leakage ratio alpha_c=b12(c)/(2(b13(c)+b23(c))+eta), crossing the half-overlap shield at alpha_c=1 as eta -> 0.
- Held-fixed controls: The same gauge-invariant Wilson hairpins, null vector, and H,K Schur-Feshbach reduction are held fixed., The heat-kernel plaquette-sheet regulator, color factor C_N, Wilson normalization, and reflection map are held fixed., No boundary counterterm, gauge fixing change, or observable-algebra enlargement is allowed., The Gaussian margin M_G and endpoint source direction L_c are held fixed while alpha_c is varied by endpoint geometry.
- Expected observation: Classes with alpha_c<=1 contribute only protective root-quartic mass up to certified errors; classes with alpha_c>1 are the only possible negative leakage and must be compared quantitatively with M_G.
- Transfer certificate needed: Uniform same-theory source derivative intervals, a cutoff-uniform T_tail, and a proof that the finite endpoint source carrier recovers the intended reflected Wilson OS matrix entries without changing the theory.

## Next Experiment

Proof search plus validator-facing endpoint source computation: enumerate source-equivalent endpoint classes for the heat-kernel three-hairpin block, compute the seven-point connected cumulant witness intervals, certify M8 and T_tail, then decide I_gate; remain in quarantine until this finite same-theory screen is valid.

# Gauge-Invariant Nontriviality Witness Selection: endpoint R++ sector certificate

## Candidate Lemma

Conditional Ward-Hessian endpoint-cell certificate: for the H,K plus hairpin endpoint box, the renormalized connected boundary-OPE polarization R_{++}^{ren} has a computable lower interval consisting of the positive flowed pair contraction minus sector Hessian majorants for the connected four-curvature cumulant and same-theory recovery errors. If this lower interval beats the finite Schur-Feshbach leakage L_+, endpoint-box positivity is promoted; if not, the R repair is demoted by a valid falsifier.

## Definitions

- source object: SU(N) Euclidean Yang-Mills Wilson hairpin family at lattice cutoff a or continuum regulator cutoff Lambda, evolved by gradient flow time t>0 and boundary point-splitting epsilon, with perimeter/cusp-renormalized centered observables \widehat W_{+,I}.
- target object: the finite Route A post-H,K plus-channel Schur-Feshbach scalar Q_+^{ren} for the endpoint box, not the continuum Hamiltonian mass gap.
- controlled interface: endpoint sheet-current carrier J_{+,I} with color, orientation, reflection, and endpoint moments, mapped to centered flowed Wilson cumulants by recovery errors E_{rec}(a,t,epsilon).
- same-theory condition: all pair terms, connected C4 sectors, counterterms, quotient maps, and recovery errors are computed in the same regulated Wilson measure and only then compared along one cutoff-removal family.

## Assumptions

- Model: pure SU(N) Yang-Mills with Wilson plaquette regulator or an equivalent gauge-invariant UV cutoff admitting gradient flow and reflection across the chosen endpoint hyperplane.
- Regime: endpoint cells I,J have diameter rho, separation d, hairpin thickness eta, and flow radius sqrt(8t) satisfying a << epsilon <= eta <= rho << d with fixed finite H,K geometry.
- Cutoff: flowed curvature cumulants up to order four admit local counterterms cancelling perimeter, cusp, and endpoint self-pair divergences uniformly on the endpoint cell partition.
- Same-theory: the centered Wilson observables, sheet-current recovery map, Ward-subtracted kernels, and Feshbach matrix entries are all taken from one Schwinger/Wilson family, so no imported non-Gaussian Schwinger family is substituted.
- Local: plus-channel endpoint currents satisfy certified monopole and dipole cancellation in each endpoint cell after zero-pairing quotienting.
- Validity: sector kernels K_s^{WS}, s in {3g,4g,ct,end}, have interval-enclosed mixed endpoint Hessians H_s^+(I,J;t,a) after Ward/cusp subtraction.

## Equations

- centered flowed hairpin: `\widehat W_{+,I}=Z_{pc}(t,\epsilon,a)^{-1}\left(W_{+,I}(t,\epsilon,a)-\langle W_{+,I}(t,\epsilon,a)\rangle\right)`. Valid when: Valid when the same regulated Wilson measure supplies the expectation, flow, point splitting, and perimeter/cusp counterterm.
- endpoint polarization definition: `R_{++}^{ren}(I,J)=\kappa_2\left(\widehat W_{+,I},\widehat W_{+,J}\right)_{\mathrm{endpoint}}`. Valid when: Valid when disconnected products and one-hairpin self terms have been subtracted before restricting to endpoint boxes.
- pair plus connected sector split: `R_{++}^{ren}=g_t^4\,2(N^2-1)\,\mathcal G_{++}+g_t^6\,N(N^2-1)\sum_{s}\Xi_s^{WS}+E_{rec}`. Valid when: Valid in the small endpoint-sheet expansion after Ward/cusp subtraction and before taking any continuum or large-volume limit.
- Ward-Hessian sector majorant: `|\Xi_s^{WS}(I,J)|\le H_s^+(I,J;t,a)\,M_{2,+}(I)M_{2,+}(J)+E_s^{tail}`. Valid when: Valid when plus-channel monopole and dipole moments vanish and K_s^{WS} has an interval mixed-Hessian enclosure on I times J.
- lower interval and promotion test: `R_{++}^{I,-}=g_t^4\,2(N^2-1)\mathcal G_{++}^{I,-}-g_t^6N(N^2-1)\sum_s H_s^{I,+}M_{2,+}(I)M_{2,+}(J)-E_{rec}^{I,+}-\sum_sE_s^{tail,+}`. Valid when: Valid for the fixed endpoint partition when all interval enclosures use outward rounding and the recovery map is same-theory certified.
- finite endpoint positivity implication: `R_{++}^{I,-}>L_+ +\mu\quad(\mu>0)\ \Longrightarrow\ Q_+^{ren}\ge \mu`. Valid when: Valid when L_+ is the Schur-Feshbach leakage computed from the same finite H,K matrix normalization.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator; positive flowed pair covariance and renormalization are individually valid but connected C4 can erase the pair contribution.
- Use gradient flow plus boundary point splitting to expand each centered hairpin in endpoint sheet currents; subtract disconnected product, one-hairpin perimeter terms, cusp terms, and endpoint self-pair terms.
- The two cross-pair curvature contractions give the positive baseline g_t^4 2(N^2-1) G_{++}; the color factor comes from two adjoint delta contractions after tracing the two fundamental hairpins.
- Decompose the remaining connected four-curvature polarization into 3g, 4g, counterterm, and endpoint-contact sectors with color factor N(N^2-1).
- Apply Ward identities and plus-channel orientation symmetry to remove endpoint monopole and dipole moments. Taylor expand each Ward-subtracted sector kernel around the endpoint cell centers.
- Bound each sector by the mixed endpoint Hessian interval H_s^+ times the second moments M_{2,+}(I)M_{2,+}(J), plus a tail remainder from sixth and higher endpoint moments.
- Combine the lower interval for R_{++}^{ren} with the finite Schur-Feshbach leakage L_+. If R_{++}^{I,-}>L_+ + mu, then the finite endpoint-box Q_+ is positive with margin mu.

Blocking gap: The missing mediator is a certified cutoff-stable numerical or analytic enclosure of H_s^+(I,J;t,a), E_s^{tail}, and E_{rec} for the actual H,K endpoint cells.

## Falsifiers

- Ward/cusp subtraction leaves a first-moment term, invalidating the Hessian M2^2 suppression.
- A zero-pairing discarded current has small pair norm but a large connected C4 sector contribution.
- The outward-rounded interval gives R_{++}^{I,-}\le L_+, so the endpoint-box repair is not positive.
- The flow-window plateau fails: varying t changes the sign or size of R_{++}^{I,-} beyond declared recovery errors.
- The same-theory recovery error E_{rec} is comparable to or larger than the pair baseline.
- Large-field or topological sectors contribute endpoint-contact terms not covered by the sector counterterms.
- The finite connected cumulant witness survives only as a regulator artifact and vanishes in the Schwinger limit.

## Learning

The declarative tension is now precise: Schur-Feshbach endpoint positivity, positive flowed Wilson pair covariance, and same-theory recovery must jointly hold, but connected four-curvature polarization can invalidate the endpoint mediator. Raw Wilson contours are fragmented and representation-limited; global OS spectral transfer or a non-Gaussian Schwinger family route is too coarse for this local obstruction. Endpoint sheet currents are the sharper abstraction because Ward/cusp subtraction, plus-moment cancellation, mixed Hessian bounds, interval arithmetic, and zero-pairing quotienting directly compute R_{++}. Conceptual value signal: the branch is route-changing at finite scope by turning R_{++}/kappa_4 into a falsifiable color-geometric lower interval with explicit sector constants and recovery errors, while all Clay target commitments remain frozen and unclaimed.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and proof-search target for the endpoint R++ interval.`
- Rationale: The branch has repeated the sector-certificate plan; the next valid contribution must test whether Ward-Hessian suppression can numerically beat Schur-Feshbach leakage in the actual H,K endpoint geometry.
- Situation seed: A flowed SU(2) Wilson lattice in a finite reflected box with the fixed H,K plus-channel hairpin endpoint currents, centered perimeter/cusp-renormalized hairpins, and sector kernels {3g,4g,ct,end} evaluated on an endpoint-cell partition.
- Varied variable: lambda=eta/sqrt(8t), the ratio of hairpin thickness to gradient-flow radius, with endpoint separation d and cell diameter rho held in the Route A scaling window.
- Held-fixed controls: The H,K endpoint sheet-current geometry and plus-channel orientation signs are fixed., The Schur-Feshbach leakage L_+ is computed once from the same finite H,K matrix normalization., The Wilson measure, gradient-flow definition, point-splitting rule, and counterterm scheme are held same-theory across all lambda., The endpoint partition, outward-rounded interval arithmetic, and zero-pairing quotient tolerance are fixed.
- Expected observation: If Ward/cusp and plus-moment cancellations are effective, the dimensionless dominance ratio D(lambda)=R_{++}^{I,-}/L_+ develops a positive plateau above 1; if C4 dominates, D(lambda) stays below 1 or changes sign, giving a falsifier for this R repair.
- Transfer certificate needed: An outward-rounded interval certificate for G_{++}^{I,-}, all H_s^{I,+}, E_s^{tail,+}, and E_{rec}^{I,+}, plus a same-theory recovery proof that the computed centered flowed Wilson cumulant is the finite connected cumulant witness used in Q_+.

## Next Experiment

Route explicitly to proof search: build the validator-facing same-theory nontriviality witness file for the H,K endpoint cells by interval-evaluating G_{++}^{I,-}, H_{3g}^{I,+}, H_{4g}^{I,+}, H_{ct}^{I,+}, H_{end}^{I,+}, E_tail, and E_rec across lambda=eta/sqrt(8t), then report either the promotion certificate R_{++}^{I,-}>L_+ + mu or the falsifier R_{++}^{I,-}\le L_+.

# Cycle 314: quarantine abstraction, route raw K4 phase-stress to interval proof search

## Candidate Lemma

Finite phase-stress quarantine theorem: in a fixed heat-kernel cutoff theory, a two-sparse negative Rayleigh certificate for the Schur-corrected endpoint matrix U_sigma is a valid falsifier for the worked H,K endpoint route; absence of the required raw intervals permits no promotion and quarantines the abstraction.

## Definitions

- source object: finite heat-kernel regulated SU(N) Wilson plaquette cumulant data on one reflected endpoint box, including oriented plaquette sheets, transporters, color tensors, OPE error intervals, and the already fixed H,K Schur blocks.
- target object: a two-sparse Rayleigh stress certificate or survival state for the Schur-corrected endpoint quadratic form on the finite endpoint span.
- controlled interface: the map from raw connected plaquette cumulant intervals to the compressed matrix U_sigma=R_G+R_K+E_OPE-S_HK, followed only by exact Wilson quotienting and phase Rayleigh evaluation.
- same-theory condition: the cutoff action, heat-kernel smearing sigma, coupling normalization, Wilson basis, reflection plane, and H,K Schur data are identical in every term entering U_sigma.
- carrier: a connected cumulant witness R_{ij}=cum_2(Q_i,Q_j) with Q_i=:Phi_i^A Phi_i^A: built from transported smeared plaquette curvature in endpoint sheet i.

## Assumptions

- Model: finite-volume lattice SU(N) Yang-Mills with heat-kernel plaquette action or an equivalent reflection-positive heat-kernel regulator.
- Cutoff: a>0 and sigma>=a are fixed before interval extraction; no continuum or infinite-volume limit is used.
- Same-theory: R_G, K^{(4)}, E_OPE, and S_HK are computed from the same Wilson basis and the same H,K Schur-Feshbach normalization.
- Validity: raw K4 intervals are rigorous enclosures for phase-resolved connected four-curvature cumulants after exact Wilson quotienting.
- Local: the endpoint set is finite and contains only the H,K collar/hairpin endpoint box under audit.
- Constraint: success or failure changes only finite Route A endpoint-box positivity; OS reconstruction, gauge-invariant observable density, excitation-sector cyclicity, and the Clay mass gap remain non-claims.

## Equations

- transported-flux-endpoint-observable: `\Phi_i^A=\sum_{\pi\in S_i} w_{i\pi}\,\operatorname{Ad}(U_{i\pi})^{AB}F_{\pi,\sigma}^B,\qquad Q_i=:\Phi_i^A\Phi_i^A:`. Valid when: Valid when the endpoint sheet S_i, heat-kernel smearing, transporter convention, and Wick or cumulant normal ordering are fixed in the same cutoff Wilson theory.
- raw-connected-polarization-decomposition: `R_{ij}^{\mathrm{raw}}=\operatorname{cum}_2(Q_i,Q_j)=\alpha_N g_R^4(C_\sigma\circ C_\sigma)_{ij}+\frac{g_R^4}{16N^2}K_{ij}^{(4)}+E_{ij}^{\mathrm{OPE}},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when the boundary OPE is truncated at the quadratic curvature square, disconnected vacuum and perimeter terms are subtracted, and K^{(4)} denotes the remaining connected four-curvature cumulant in the same regulator.
- schur-corrected-endpoint-matrix: `U_\sigma=R^{\mathrm{raw}}_\sigma-S_{HK},\qquad S_{HK}=B_{HK}^*E_{HK}^{-1}B_{HK}`. Valid when: Valid when the H,K off-endpoint block E_{HK} is strictly positive on its finite range and the same endpoint basis is used for R_raw and the Schur subtraction.
- phase-upper-offdiagonal: `B_{pq}^+(\theta)=\Re(e^{i\theta}G_{pq})+\frac{g_R^4}{16N^2}K_{pq}^{+,\theta}+E_{pq}^{+,\theta}-S_{pq}^{-,\theta},\qquad L_{pq}(\theta)=\max\{0,-B_{pq}^+(\theta)\}`. Valid when: Applies when K_{pq}^{+,theta}, E_{pq}^{+,theta}, and S_{pq}^{-,theta} are certified interval endpoints for the same phased real part of the compressed matrix entry.
- two-sparse-demotion-gate: `D_r^+=G_{rr}+\frac{g_R^4}{16N^2}K_{rr}^+ +E_{rr}^+-S_{rr}^-,\qquad \tau_{pq}(\theta)=D_p^+-\frac{L_{pq}(\theta)^2}{D_q^+}`. Valid when: Valid when D_q^+ is positive, all diagonal and off-diagonal interval endpoints are same-theory upper or lower bounds, and the stress vector is x=e_p+(L_{pq}/D_q^+)e^{i\theta}e_q.
- finite-falsifier-condition: `\tau_{pq}(\theta)<0\;\Longrightarrow\; x^*U_\sigma x<0\;\Longrightarrow\;U_\sigma\not\succeq0`. Valid when: Valid when the preceding interval inequalities enclose the exact finite endpoint matrix entries and the Rayleigh vector x is evaluated in the unquotiented or exactly quotiented endpoint space.

## Attempted Derivation

- Conceptual pressure attacked: replace symbolic boundary polarization R by a validator-facing connected cumulant witness without inflating a finite Wilson computation into the Clay theorem.
- Declarative tension: Wilson/OPE coefficients, raw connected K4 negativity, OPE errors, and H,K Schur subtraction must jointly control one finite endpoint quadratic form in the same cutoff theory, while OS reconstruction, gauge-invariant observable density, excitation-sector cyclicity, nontrivial continuum YM, and Hamiltonian mass gap are barred as conclusions.
- Carrier audit: scalar R is too weak, A012 shells are convenient but quarantined, raw plaquette enumeration is fragmented yet valid, and the OS Hilbert observable algebra is too strong and circular for this local gate.
- Compared route: full Delta_raw PSD search is complete but data-heavy; the two-sparse phase-stress route is a sharper negative tactic because three interval types can already produce a falsifier.
- Representation requirements fixed: encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/K4 separation, endpoint compression, same-theory normalization, and exact Wilson quotienting; support cumulant contraction, interval summation, phase certification, Rayleigh stress search, Loewner bounds, and Schur subtraction; quotient only by exact Wilson identities; transfer only through tau, Delta_raw, or x_stress.
- Starting from Q_i=:Phi_i^A Phi_i^A:, vacuum and perimeter subtraction removes disconnected terms; the Gaussian crossed contractions give alpha_N g_R^4(C_sigma o C_sigma), which is PSD on every finite endpoint set.
- All possible route-killing negativity is localized to the phase-resolved K4 interval, the OPE interval, or the Schur subtraction; hence the first hard gate is tau_pq(theta)<0.
- If tau_pq(theta)<0, the constructed vector x=e_p+(L_pq/D_q^+)e^{i theta}e_q gives x^*U_sigma x<0 using only interval upper bounds, so endpoint PSD fails.
- If tau is nonnegative or raw intervals are missing, no positivity conclusion follows; the branch must either compute raw K4 intervals or run full Delta_raw interval PSD search.

Blocking gap: No same-regulator, quotient-audited phase intervals for Re(e^{i theta}K^{(4)}_{pq}) and the corresponding diagonal K^{(4)} entries have been supplied for the actual H,K endpoint geometry.

## Falsifiers

- A negative tau_pq(theta) with quotient-audited same-regulator intervals is a valid finite falsifier for the H,K endpoint-box positivity route.
- Regulator mismatch between K4 intervals and S_HK invalidates the connected cumulant witness.
- Non-invariant Wilson quotienting that changes signs, transporter paths, or multiplicities demotes the certificate.
- Two-sparse survival with a hidden three-sparse negative Rayleigh vector falsifies any attempted promotion from tau tests to PSD.
- If the OPE interval is wider than the Gaussian-Schur margin, the route is inconclusive and must be quarantined rather than promoted.
- If exact raw enumeration cannot reproduce the compressed interval after quotient expansion, the sheet-kernel carrier is representation-limited and must be abandoned.

## Learning

Cycle 314 confirms the phase-stress abstraction is now looping unless raw same-regulator K4 intervals are produced. The sharp contribution is a quarantine theorem: tau_pq(theta)<0 is a finite connected cumulant witness falsifier, but tau survival is not endpoint positivity. The conceptual value signal is route-changing at finite scope because Gaussian color positivity, non-Gaussian K4 danger, OPE error, and Schur hairpin energy are unified in one valid inequality while all Clay-level YM commitments remain non-claims.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe before any further abstraction.`
- Rationale: The branch has looped on phase-stress language; only a same-regulator raw K4 interval computation can decide whether the finite H,K endpoint route survives.
- Situation seed: Finite SU(2) heat-kernel lattice Yang-Mills on a four-dimensional torus with the already fixed reflected H,K collar/hairpin endpoint box; compute the connected cumulant witness R_{pq}=cum_2(:Phi_p^2:,:Phi_q^2:) by character-expansion intervals for the oriented plaquette sheets contributing to one candidate off-diagonal pair p,q.
- Varied variable: rho=sigma/a, the heat-kernel smearing-to-lattice-spacing ratio, varied over rho in {1,2,4} while the endpoint geometry is unchanged.
- Held-fixed controls: Same Wilson action, coupling normalization g_R, volume, reflection plane, H,K endpoint basis, and Schur block S_HK., Exact Wilson quotient policy and the same OPE truncation order for all rho values., The phase theta and endpoint pair p,q selected before interval evaluation to avoid advice leakage.
- Expected observation: Either the phase-resolved off-diagonal K4 interval becomes negative enough to make tau_pq(theta)<0, demoting the route, or it remains below the Gaussian-Schur-OPE threshold and forces full Delta_raw proof search.
- Transfer certificate needed: A rigorous interval enclosure for the connected four-plaquette cumulant with exact quotient audit, plus a same-theory recovery map from raw plaquette sheets to U_sigma entries.

## Next Experiment

Proof search: compute one quotient-audited same-regulator raw K4 phase interval triple for a fixed endpoint pair p,q and theta in the H,K collar/hairpin box; if unavailable, quarantine this branch and hand off to literature import or raw plaquette enumeration.

