# cycle-0339

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint-source quarantine for the post-H,K reflected-Wilson scalar

## Candidate Lemma

For the fixed reflected three-hairpin Wilson block, the only valid post-H,K promotion/falsifier scalar is the endpoint source interval I_gate built from same-theory connected cumulant witness data, signed incidences, color factor, Gaussian margin, and uniform tail. H,K, half-overlap shielding, and root-quartic negativity alone underdetermine the scalar, so promotion without endpoint source intervals is invalid and the branch remains quarantined.

## Definitions

- source object: heat-kernel plaquette-sheet SU(N) regulated Yang-Mills on one fixed reflected Wilson collar/hairpin block, with endpoint source classes c, log source functions log Z_{a,L,c}(s), signed incidences b_{ij,c}, color factor C_N, Gaussian Schur margin M_G, and tail interval T_tail.
- target object: the finite corrected post-H,K OS transfer scalar for the intended same-theory Wilson OS matrix; nonnegative certified lower endpoint promotes this block, while a negative certified upper endpoint gives a finite same-theory falsifier.
- controlled interface: C_ep, the endpoint carrier sending regulated source-derivative intervals and signed incidences to a scalar interval [I_-,I_+] without adding boundary degrees of freedom or changing Wilson normalization.
- same-theory condition: all source derivatives, Wilson loops, reflection maps, endpoint identifications, and cutoff labels are inherited from the same heat-kernel regulated gauge-invariant observable algebra; endpoint classes are equivalent only by equal regulated source data.
- connected cumulant witness: kappa_c is the fourth source derivative of log Z_{a,L,c} in the null-channel endpoint direction, not a raw moment and not an independent boundary field.
- efficient representation: encode source classes, seven source values, cumulant intervals, signed incidences D_c, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; use source differentiation, interval arithmetic, aggregation before clipping, color multiplication, and tail addition; export only I_gate.

## Assumptions

- Model: finite-volume SU(N) lattice Yang-Mills with heat-kernel plaquette-sheet regulator and gauge-invariant Wilson-loop observables only.
- Regime: fixed finite three-hairpin collar block after the already-computed H,K Schur-Feshbach reductions; no continuum or mass-gap conclusion is claimed.
- Cutoff: all source derivative and tail bounds must be uniform in lattice spacing and collar thickness over the finite block being certified.
- Same-theory: no boundary counterterm, boundary Hilbert sector, modified Wilson renormalization, gauge fixing change, or observable-algebra enlargement is allowed.
- Validity: source-equivalent endpoint classes are aggregated before clipping; otherwise incidence cancellations can be destroyed by the representation.
- Local: all non-endpoint and unresolved corner contributions are charged to T_tail with an explicit sign-safe interval.

## Equations

- signed endpoint incidence: `D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}`. Valid when: Valid when b_{ij,c} are the source-class endpoint incidences of the fixed reflected Wilson block after the H,K null-channel contraction.
- seven point connected cumulant interval: `\kappa_c\in \Delta_h^{(4)}\log Z_{a,L,c}(0)+\left[-\frac{7h^4}{240}M_{8,c},\frac{7h^4}{240}M_{8,c}\right]`. Valid when: Valid when log Z_{a,L,c}(s) is eight-times source differentiable on the stencil interval and M_{8,c} is a cutoff-uniform derivative bound.
- endpoint carrier scalar: `I_{\mathrm{gate}}\in M_G+C_N\sum_c D_c\,[\kappa_c^-,\kappa_c^+]+T_{\mathrm{tail}}`. Valid when: Valid when endpoint classes have been aggregated by equal regulated source data before interval multiplication and tail addition.
- root quartic analytic screen: `\kappa_c=-\frac{t_c^4}{60}\left(N\operatorname{tr}L_c^4+3(\operatorname{tr}L_c^2)^2\right)+E_c`. Valid when: Applies in small heat-kernel endpoint coordinates when L_c is the same-theory endpoint source and E_c has a uniform analytic remainder bound.
- underdetermination obstruction: `\exists\,\kappa^{+},\kappa^{-}\text{ consistent with H,K and the screen such that }I_{\mathrm{gate}}(\kappa^{+})\ge0>I_{\mathrm{gate}}(\kappa^{-})`. Valid when: Valid when a positive-D source class has unresolved cumulant width or unresolved tail width large enough to cross the finite margin.

## Attempted Derivation

- Freeze the Clay claim level: only a finite Route A reflected-Wilson block is being tested; continuum existence, observable density, OS spectral transfer, nontriviality, and mass gap are untouched.
- Use the prior H,K reduction only as input; do not restate the old threshold. The remaining scalar is written as Gaussian margin plus connected endpoint polarization plus tail.
- Represent the endpoint polarization by C_ep: aggregate source-equivalent endpoint classes, compute D_c, recover kappa_c from log Z source stencils, multiply signed intervals, add T_tail.
- Apply the root-quartic heat-kernel screen to show why kappa_c is typically negative at leading compact-group order.
- Observe that negative kappa_c lowers the scalar only for D_c>0; half-overlap classes with D_c<=0 are protective or neutral.
- Try to promote from H,K plus half-overlap plus root-quartic negativity alone.
- The attempt fails because positive-D source classes may have unresolved kappa_c intervals and T_tail may cross the margin; two same-H,K carriers with different valid source intervals can give opposite signs for I_gate.

Blocking gap: No actual cutoff-uniform endpoint source intervals for the connected cumulant witness and no uniform T_tail bound for the fixed heat-kernel endpoint boxes.

## Falsifiers

- A certified interval with I_+<0 is a finite same-theory falsifier for this post-H,K Wilson block.
- A boundary counterterm needed to define log Z_c(s) breaks the same-theory condition and demotes the route.
- A nonuniform M_8 or T_tail bound as cutoff is removed invalidates the endpoint carrier even if finite lattice data look positive.
- Geometric aggregation of endpoint boxes with unequal regulated source data is a representation falsifier for C_ep.
- A source family outside the gauge-invariant Wilson algebra can make the interval valid for another theory but not for the Clay target theory.

## Learning

Conceptual pressure attacked: sign-certify endpoint collapse inside the same Wilson theory after H,K. Declarative tension: finite collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist without a boundary theory, but H,K, half-overlap shielding, and root-quartic negativity do not determine the post-H,K scalar. Carrier audit: raw R is too weak, raw kappa_4 spectra are too strong, and the global Schur-preimage route is valid but too coarse after H,K. The sharp value signal is explanatory and route-changing at finite scope: negative SU(N) endpoint cumulants are not the obstruction; positive-D leakage times a same-theory connected cumulant witness plus uniform tail is. Hard gate: the finite post-H,K reflected-Wilson OS transfer scalar. Success promotes only this fixed block, failure gives a finite falsifier, and missing source/tail data keeps quarantine.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe while keeping the branch quarantined until endpoint source intervals are available.`
- Rationale: The branch is looping on carrier language; a concrete heat-kernel endpoint stress test is needed to decide whether positive-D leakage can overcome the finite Schur-Feshbach margin without changing the Wilson theory.
- Situation seed: Finite SU(3) heat-kernel plaquette-sheet endpoint box for the fixed reflected three-hairpin block, with seven same-theory source evaluations of log Z_c(s) for each endpoint source class and a certified T_tail interval.
- Varied variable: Fractional leakage ratio alpha_c=(b13,c+b23,c)/b12,c, varied from the half-overlap shield alpha_c=1/2 toward a 12-dominant endpoint class alpha_c=0.
- Held-fixed controls: Gauge group SU(3), heat-kernel regulator, Wilson plaquette-sheet source normalization, and reflection map are fixed., The H,K reduced finite block, null-channel weights, color factor C_N, and Gaussian margin M_G are fixed., No boundary counterterm, gauge-fixing change, or observable-algebra enlargement is allowed., The source step h and derivative error budget M_8 are certified in the same regulator family.
- Expected observation: For alpha_c>=1/2 the connected negative root-quartic cumulant should not lower I_-. For sufficiently 12-dominant alpha_c, a negative connected cumulant witness plus tail may push I_+ below zero and produce a finite falsifier.
- Transfer certificate needed: A cutoff-uniform recovery certificate for log Z_c source derivatives, a uniform T_tail bound, source-equivalence aggregation before clipping, and proof that the endpoint observables remain in the locked gauge-invariant Wilson algebra.

## Next Experiment

Proof search plus targeted endpoint-source stencil computation: for the fixed heat-kernel SU(3) three-hairpin block, compute the connected cumulant witness intervals for positive-D endpoint classes, certify T_tail, and return I_gate; otherwise keep quarantine and pivot.

# Gauge-Invariant Nontriviality Witness Selection: endpoint R++ annular plateau certificate

## Candidate Lemma

Plateau-compressed annular Ward-Hessian certificate: for fixed H,K endpoint hairpins, the renormalized plus-channel endpoint mediator R_{++}^{ren} has a computable lower interval. If its dominance margin over the Schur-Feshbach leakage L_+ is positive, finite endpoint-box positivity after H,K is promoted; if certified upper bounds remain below L_+, this R repair is quarantined.

## Definitions

- source object: the finite-volume SU(N) Wilson lattice measure at spacing a with gradient-flow time t, boundary point-splitting eta, and centered reflected hairpin variables \widehat W_{h_+}^{t,\eta},\theta\widehat W_{h_+}^{t,\eta}.
- target object: the finite post-H,K Schur-Feshbach endpoint box plus-channel inequality Q_+^{ren}>0, equivalently a positive lower interval for R_{++}^{ren}-L_+ in the fixed finite matrix problem.
- controlled interface: endpoint sheet currents carrying the H,K hairpin geometry, Ward/cusp-subtracted cumulant expansion, dyadic annular sector quadrature, and recovery errors E_rec from raw Wilson hairpins to centered flowed variables.
- same-theory condition: all Wilson variables, gradient flow, counterterms, recovery maps, and cumulants are evaluated in the same finite-cutoff Yang-Mills measure; no continuum OS spectral-transfer or full mass-gap claim is made.

## Assumptions

- Model: hypercubic finite-volume SU(N) Wilson action with reflection plane fixed and gradient-flow regulator t>0.
- Regime: endpoint cell diameter eta is smaller than the collar separation and the annular split begins outside the local endpoint box.
- Cutoff: sector Hessian majorants H_{s,j}^+ and pair intervals G_{++}^{\pm} are outward-rounded and uniform over the finite volume used.
- Same-theory: recovery errors compare raw and flowed centered hairpins inside the same Wilson measure, not through an imported continuum theory.
- Validity: Ward identity residuals, perimeter/cusp counterterms, and plus-channel monopole/dipole cancellations are certified before applying the annular tail estimate.
- Local: the claim changes only finite endpoint-box positivity after H,K; Clay existence, OS/Wightman axioms, nontriviality, observable density, and mass gap remain untouched.

## Equations

- renormalized endpoint cumulant: `R_{++}^{ren}=\kappa_2\!\left(\widehat W_{h_+}^{t,\eta},\theta\widehat W_{h_+}^{t,\eta}\right)`. Valid when: Valid when the centered flowed hairpins are recovered from raw Wilson loops in the same finite-cutoff measure with the stated point-splitting.
- lower annular dominance interval: `R_{++}^{-}=g_t^4\left[2(N^2-1)G_{++}^{-}-N(N^2-1)\sum_s A_sT_s^{+}\right]-E_{rec}^{+}-E_{6}^{+}`. Valid when: Applies after disconnected-product removal, one-hairpin perimeter and cusp subtraction, Ward subtraction, and certified plus-channel moment cancellation.
- plateau tail compression: `T_s^{+}\le \sum_{j=0}^{J}I_{s,j}^{+}+\frac{q_s}{1-q_s}(1+\varepsilon_s)\max_{J-p\le \ell\le J}I_{s,\ell}^{+},\qquad q_s=2^{4-2\nu_s}<1`. Valid when: Valid when the sector s mixed Hessian decays with exponent nu_s beyond annulus J and the last p annuli pass the plateau drift test.
- promotion margin: `\Delta_R^{-}:=R_{++}^{-}-L_+;\qquad \Delta_R^{-}>0\Rightarrow Q_+^{ren}>0`. Valid when: Requires the finite Schur-Feshbach leakage L_+ and the Wilson cumulant interval to refer to the same H,K endpoint basis.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, but positive flowed pair covariance and recovery can both be valid while connected C4 erases R_{++}.
- Start from R_{++}^{ren}=kappa_2 of two centered gradient-flow hairpins with boundary point-splitting; expand the Wilson cumulant to order g_t^4 plus a controlled E_6 remainder.
- Remove the disconnected product and one-hairpin perimeter/cusp terms; use Ward subtraction and plus-channel monopole/dipole cancellation to force the connected C4 contribution into mixed endpoint Hessians.
- Represent H,K hairpins by endpoint sheet currents; quotient only currents with certified zero pairing so gauge, color, reflection, orientation, cutoff, locality, and same-theory invariants are preserved.
- Split the mixed Hessian kernels into endpoint box plus dyadic annuli. In annulus j, use heat-kernel Hessian majorants to obtain sector intervals I_{s,j}^+ with color N(N^2-1) and sector multiplicities A_s.
- For the tail, assume a certified decay exponent nu_s>2 and plateau drift epsilon_s across the last p annuli; sum the geometric tail with q_s=2^{4-2nu_s}.
- Combine the positive pair baseline 2(N^2-1)G_{++}^- with negative C4 sector envelopes, E_rec^+, E_6^+, and L_+ to form Delta_R^-.
- Hard gate: if Delta_R^->0, finite endpoint-box positivity after H,K is promoted; if R_{++}^+<L_+, the R repair is quarantined. In both cases all Clay gates remain unproved.

Blocking gap: The missing proof object is a certified table of sector Hessian intervals I_{s,j}^+, plateau drift epsilon_s, recovery error E_rec^+, and sixth-order remainder E_6^+ for the actual H,K hairpin geometry.

## Falsifiers

- falsifier: the Ward residual or cusp counterterm is not small after outward-rounded interval evaluation.
- falsifier: the connected C4 annular ratios do not enter a stable plateau, so q_s compression is not valid.
- falsifier: the raw-to-flowed recovery error is comparable to the positive pair baseline.
- falsifier: the hairpin geometry gives G_{++}^-=0 or an endpoint current with uncancelled monopole/dipole moment.
- falsifier: R_{++}^{+}<L_+ for the fixed H,K,t,eta instance, forcing quarantine of this endpoint repair.
- falsifier: interval widths grow under cutoff refinement, showing the finite certificate is not cutoff-stable.

## Learning

Cycle 339 changes the branch from an annular-plateau idea to a validator-facing proof-search certificate: R_{++}/kappa_4 is the same-theory flowed Wilson cumulant of two centered H,K hairpins, decomposed into a positive pair baseline, connected C4 sector tails, recovery errors, and L_+. Declarative tension: endpoint positivity, positive pair covariance, and same-theory recovery must jointly be valid, yet C4 can erase the mediator. Raw Wilson contours are fragmented; global OS spectral transfer, area-law intuition, and broad same-theory nontriviality witness routes are too coarse. Efficient representation requirements are endpoint sheet currents, gauge/color/reflection/orientation/cutoff/locality invariants, Ward/cusp subtraction, Taylor Hessians, dyadic tail compression, outward-rounded intervals, certified zero-pairing equivalence, finite endpoint locality, and transfer through centered flowed cumulants. Conceptual value signal: one finite Route A gate becomes a sign/size theorem with a falsifier; all Clay commitments remain frozen.

## Gedanken Experiment Design Seed

- Need decision: `Design and use now as a falsifier probe plus proof-search guide.`
- Rationale: The branch has already reduced R_{++} to an annular dominance margin; another abstract restatement would loop, while a concrete plateau experiment decides whether the connected C4 term is actually controllable.
- Situation seed: Fixed SU(N) Wilson lattice in a large reflection-symmetric box with gradient flow time t, boundary point-splitting eta, and the actual post-H,K plus-channel endpoint hairpin pair represented by endpoint sheet currents; compute the connected cumulant witness R_{++}=kappa_2 of the two centered flowed hairpins.
- Varied variable: The annular cutoff depth J and plateau window length p for the C4 sector tail compression.
- Held-fixed controls: Gauge group SU(N), Wilson action, reflection plane, and same finite-cutoff measure., The H,K endpoint hairpin geometry, plus-channel basis, leakage L_+, and zero-pairing quotient policy., Gradient-flow time t, point-splitting eta, Ward/cusp subtraction scheme, and recovery map.
- Expected observation: Either the normalized sector intervals I_{s,j+1}/I_{s,j} fall below q_s with small plateau drift and Delta_R^- becomes positive, or the C4 tail/recovery budget dominates and supplies a valid falsifier for this finite endpoint repair.
- Transfer certificate needed: Outward-rounded interval quadrature, a Ward/cusp residual certificate, same-theory L2 recovery bounds, a sixth-order remainder bound, and a proof that the annular constants are uniform over the finite endpoint cells before the intuition may affect proof obligations.

## Next Experiment

proof search: build the outward-rounded annular plateau table for the actual H,K endpoint sheet currents, compute G_{++}^{-}, I_{s,j}^{+}, epsilon_s, E_rec^+, E_6^+, and test Delta_R^->0 or R_{++}^{+}<L_+; report as a connected cumulant witness only at finite same-theory cutoff, not as a continuum same-theory nontriviality witness.

# Raw signed-orbit K4 stress witness for finite H,K endpoint PSD

## Candidate Lemma

Signed-orbit K4 stress lemma: for a fixed heat-kernel regulated SU(N) lattice Yang-Mills endpoint pair p,q, rigorous same-regulator interval bounds D_p^+, D_q^+ for the Schur-corrected diagonals and L_{pq}(theta) for the phased off-diagonal imply a finite Route A falsifier whenever D_p^+<0, D_q^+<0, or L_{pq}(theta)^2>D_p^+D_q^+. Survival of this test is only a demand for full Delta_raw PSD proof search.

## Definitions

- source object: finite-volume four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette regulator, spacing a, smoothing scale sigma, and endpoint Wilson sheet observables Q_i built from transported plaquette curvature insertions.
- target object: the 2x2 principal compression U^{pq}_sigma of the post-H,K Schur-corrected endpoint quadratic form on the finite Wilson endpoint basis, not an OS Hilbert spectral subspace.
- controlled interface: signed-orbit raw connected cumulant witness K^{raw}_{ij,sigma} plus Gaussian Wilson covariance, OPE interval, and Schur block S_HK are mapped to interval quantities D_i^+ and L_{pq}(theta).
- same-theory condition: all Q_i, K^{raw}, Gaussian covariance C_sigma, OPE bounds, and S_HK are computed with the identical cutoff action, coupling, transporters, endpoint boxes, Wilson normalization, and quotient identities.

## Assumptions

- Model: finite lattice SU(N) Yang-Mills with heat-kernel regulator and normalized generators tr(T^aT^b)=delta^{ab}/2.
- Cutoff: a>0, sigma>=a, finite endpoint boxes, and no continuum limit is taken in this lemma.
- Same-theory: the Schur block H,K and the Wilson cumulants use the same measure, boundary reflection, and basis ordering.
- Validity: signed orbit intervals are rigorous enclosures after exact Wilson trace quotienting and Hermitian symmetrization.
- Constraint: D_i^+ are upper bounds on actual U_{ii}, while L_{pq}(theta) is a lower bound on |U_{pq}| in the chosen phase sector.

## Equations

- endpoint-observable: `Q_i=\sum_{(\pi,\pi')\in\mathcal S_i^2} w_i(\pi,\pi')\,:\!\mathcal F^a_\sigma(\pi)\mathcal F^a_\sigma(\pi')\!:`. Valid when: Valid when endpoint sheets are finite, transported curvatures are heat-kernel smeared, and Wick subtraction uses the same cutoff vacuum.
- raw-connected-K4: `K^{raw}_{ij,\sigma}=\sum_{\pi,\pi'\in\mathcal S_i}\sum_{\rho,\rho'\in\mathcal S_j} w_i(\pi,\pi')w_j(\rho,\rho')\,T_{abcd}\,\kappa^{abcd}_{4,\sigma}(\pi,\pi',\rho,\rho')`. Valid when: Applies when the four-curvature cumulant is connected, transporter-normalized, and color-contracted before any orbit quotienting.
- post-HK-form: `U_{ij,\sigma}=R^G_{ij,\sigma}+\frac{g_R^4}{16N^2}K^{raw}_{ij,\sigma}+E^{OPE}_{ij,\sigma}-S^{HK}_{ij,\sigma}`. Valid when: Valid when Gaussian, raw K4, OPE, and Schur terms are evaluated in the same finite cutoff Wilson basis.
- gaussian-color-square: `R^G_{ij,\sigma}=\alpha_N g_R^4\sum_{\pi,\pi',\rho,\rho'} w_iw_j\big(C_\sigma(\pi,\rho)C_\sigma(\pi',\rho')+C_\sigma(\pi,\rho')C_\sigma(\pi',\rho)\big),\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Requires the same transported two-curvature covariance and the fundamental SU(N) trace normalization stated in the assumptions.
- signed-orbit-recovery: `K^{raw}_{ij,\sigma}\in\sum_{o\in\mathcal O_{ij}} m_o\epsilon_o I_o,\qquad I_o=[k_o^-,k_o^+]`. Valid when: Valid when every plaquette quadruple belongs to exactly one exact Wilson symmetry orbit with preserved phase sign.
- stress-gate: `D_p^+<0\ \text{or}\ D_q^+<0\ \text{or}\ L_{pq}(\theta)^2>D_p^+D_q^+\ \Longrightarrow\ U^{pq}_\sigma\not\succeq0`. Valid when: Valid for Hermitian 2x2 endpoint compressions with rigorous diagonal upper bounds and a phased off-diagonal lower bound.

## Attempted Derivation

- Conceptual pressure attacked: the missing mediator from raw non-Gaussian Wilson K4 cumulants to a finite Schur-corrected endpoint PSD decision, not gauge-invariant observable density or OS Hilbert cyclicity.
- Declarative tension: Wilson/OPE data, raw K4 intervals, OPE error, and S_HK must hold in one cutoff theory, while continuum OS reconstruction, nontrivial Schwinger coherence, excitation-sector cyclicity, and mass-gap spectral transfer remain non-claims.
- Carrier critique: scalar R is too weak, A012 shells lose phase signs, OS Hilbert observable algebra is too strong and circular for this local gate, and full Delta_raw search is complete but expensive.
- Current route comparison: signed raw orbits preserve phases, Hermiticity, exact Wilson quotienting, color factors, and same-theory normalization, so they are the efficient negative tactic before full matrix PSD search.
- Write U^{pq}_sigma as the 2x2 Hermitian compression of R^G+(g_R^4/(16N^2))K4+E_OPE-S_HK on endpoints p,q.
- Use rigorous interval arithmetic to produce U_pp<=D_p^+, U_qq<=D_q^+, and |U_pq|>=L_pq(theta) for a certified phase theta.
- If D_p^+<0, the vector e_p has negative Rayleigh quotient. If both upper diagonals are nonnegative but L^2>D_p^+D_q^+, PSD would imply |U_pq|^2<=U_pp U_qq<=D_p^+D_q^+, a contradiction.
- Thus the hard gate D_i^+<0 or L^2>D_p^+D_q^+ changes the proof state by killing only the finite H,K endpoint route; survival forces full Delta_raw proof search, not promotion.

Blocking gap: The branch still lacks validator-produced same-regulator signed-orbit K4 intervals I_o with exact quotient audit and OPE error enclosures. Without those intervals, the stress theorem is valid but not instantiated.

## Falsifiers

- A same-regulator signed orbit gives D_i^+<0, producing an immediate finite endpoint PSD falsifier.
- A phased off-diagonal lower bound satisfies L_{pq}(theta)^2>D_p^+D_q^+, giving a two-sparse stress falsifier for the H,K route.
- Orbit representatives disagree under transporter ordering or color contraction, invalidating the signed quotient and demoting the carrier.
- OPE intervals overflow the Gaussian-plus-K4 margin, making the stress test inconclusive and forcing full Delta_raw proof search.
- Regulator mismatch between K4 intervals and S_HK invalidates same-theory transfer.
- All two-sparse stress tests survive but Delta_raw has a negative eigenvector; then the tactic was incomplete but not false.

## Learning

The cycle converts the repeated signed-orbit rhetoric into a precise finite theorem: endpoint PSD can be falsified from diagonal upper bounds and a phased off-diagonal lower bound recovered from raw connected K4 orbits. The conceptual value signal is sharp and route-changing at finite scope because Gaussian color positivity, non-Gaussian K4 danger, OPE error, and Schur hairpin energy are unified in one valid inequality, while all Clay frontier gates remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and validator-facing interval design, not as evidence for a continuum claim.`
- Rationale: The branch has looped on signed-orbit abstraction; the only useful next intuition is whether raw same-regulator K4 phases can plausibly overpower the Gaussian-Schur diagonals in a concrete H,K endpoint pair.
- Situation seed: Finite 4D SU(N) heat-kernel lattice at fixed a and finite volume, with the worked H,K collar/hairpin endpoint boxes, two endpoint sheet observables Q_p,Q_q, exact Wilson quotienting, and a connected cumulant witness K^{raw}_{pq,sigma}.
- Varied variable: sigma/a, the heat-kernel smoothing ratio controlling locality of transported curvature cumulants.
- Held-fixed controls: Same lattice action, coupling g_R, gauge group SU(N), and heat-kernel regulator for Wilson cumulants and S_HK., Fixed H,K endpoint geometry, endpoint basis ordering, Wilson normalization, reflection support, and Schur subtraction., Exact signed-orbit quotient policy with no A012 shell averaging and no OS Hilbert observable algebra import.
- Expected observation: If increasing sigma/a damps diagonal K4 faster than a coherent signed off-diagonal orbit family, L_{pq}(theta)^2 may cross D_p^+D_q^+ and produce a finite falsifier; if all phases cancel, the route must move to full Delta_raw or quarantine.
- Transfer certificate needed: Rigorous interval enclosures for the signed K4 orbit family, Gaussian covariance bounds, OPE error intervals, exact quotient audit, and same-regulator equality with the Schur block before any intuition may affect proof obligations.

## Next Experiment

Proof search: instantiate the connected cumulant witness by computing the first same-regulator signed-orbit K4 intervals for one endpoint pair p,q, then evaluate D_p^+, D_q^+, and L_{pq}(theta)^2-D_p^+D_q^+; quarantine if the intervals or quotient audit are missing.

