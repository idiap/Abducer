# cycle-0347

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint leakage cap for the post-H,K reflected-Wilson gate

## Candidate Lemma

One-sided endpoint leakage cap: for the fixed three-hairpin heat-kernel Wilson block, after Wick-square Gram positivity and straight f f incidence cancellation, the post-H,K scalar is lowered only by source-certified positive-D endpoint classes times the connected cumulant witness plus a uniform tail. This is a finite Route A theorem, not a Clay mass-gap claim.

## Definitions

- source object: finite-volume four-dimensional SU(N) heat-kernel plaquette-sheet regulator with the fixed three reflected Wilson hairpin collar block and endpoint source partition functions Z_c(s).
- target object: the finite post-H,K Schur-Feshbach OS transfer scalar I_gate for this Wilson block, whose nonnegativity promotes only this block.
- controlled interface: source-equivalent endpoint classes c carrying seven-point source data, aggregated signed incidence D_c, color factor C_N, Gaussian margin M_G, and tail budget T_tail.
- same-theory condition: all source derivatives are computed from the same regulated Wilson loops, heat-kernel action, Haar measure, reflection, and normalization; no boundary counterterm or new endpoint theory is introduced.
- carrier C_ep: a validator-facing connected cumulant witness interval for endpoint collapse, not symbolic R and not a raw kappa_4 spectrum.
- conceptual pressure: sign-certify endpoint collapse inside the same Wilson theory after the finite H,K computation.
- declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist without adding a boundary theory; raw R forgets incidence signs and cannot mediate them.

## Assumptions

- Model: finite lattice Euclidean SU(N) Yang-Mills with heat-kernel plaquette action and reflection-positive Wilson observables.
- Regime: the three-hairpin block is fixed after the H,K Schur-Feshbach reduction, and only endpoint-box R/kappa_4 terms remain.
- Cutoff: endpoint boxes have heat-kernel time t_c within a small-source expansion radius, with constants uniform over the fixed finite block.
- Uniformity: the omitted non-endpoint and corner remainder is bounded by a regulator-uniform scalar T_tail before cutoff removal is discussed.
- Same-theory: Wilson normalizations, reflection map, source insertions, and gauge-invariant observable algebra are identical to the collar theory.
- Validity: source classes may be aggregated only when their seven regulated log Z source values agree within certified intervals.
- Local: the lemma concerns a restricted finite Wilson block and leaves continuum construction, observable density, OS spectral transfer, nontriviality, and mass gap untouched.

## Equations

- endpoint connected cumulant stencil: `\kappa_c=\partial_s^4\log Z_c(s)|_{s=0},\quad \widehat\kappa_c(h)=\frac{-f_c(-3h)+12f_c(-2h)-39f_c(-h)+56f_c(0)-39f_c(h)+12f_c(2h)-f_c(3h)}{6h^4}`. Valid when: Valid when f_c(s)=log Z_c(s) is evaluated in the same heat-kernel endpoint box and has a uniform eighth-source-derivative bound.
- signed endpoint incidence: `D_c=\sum_{v\in c}\left(2b_{12}(v)-4b_{13}(v)-4b_{23}(v)\right),\quad D_c\le 0\ \text{if}\ b_{13}+b_{23}\ge b_{12}/2`. Valid when: Valid when b_ij(v) are the fractional endpoint overlaps from the fixed null-channel three-hairpin geometry after H,K reduction.
- SU(N) root-quartic screen: `\kappa_c\in[-A_c-E_c,-A_c+E_c],\quad A_c=\frac{t_c^4}{60}\left(N\operatorname{tr}L_c^4+3(\operatorname{tr}L_c^2)^2\right)`. Valid when: Applies in heat-kernel endpoint coordinates for small sources L_c with the Haar-Jacobian fourth-order expansion and certified remainder E_c.
- one-sided finite gate lower bound: `I_- = M_G+C_N\sum_c\left(D_c^+\kappa_c^- -D_c^-\kappa_c^+\right)-T_{tail}^{abs}\ge M_G-C_N\sum_c D_c^+(A_c+E_c)-T_{tail}^{abs}`. Valid when: Valid when kappa_c intervals, aggregated D_c signs, color factor C_N, Gaussian margin M_G, and uniform tail bound are all same-theory certified.

## Attempted Derivation

- Freeze the Clay boundary: the local target is only a finite reflected-Wilson OS scalar; continuum existence, nontriviality, gauge-invariant observable density, OS spectral transfer, and mass gap remain untouched.
- Use the earlier H,K computation only as input: Wick-square Wilson contractions are positive Gram terms, and straight C_A f f contacts cancel in the null incidence channel.
- Replace symbolic R by C_ep: endpoint source classes, seven log Z values, cumulant intervals, signed D_C, C_N, M_G, and T_tail.
- Compare routes: global Schur-preimage positivity is valid but too coarse after H,K; raw kappa_4 spectra are too strong because negative cumulants are harmless when D_C<=0; C_ep is the efficient local carrier.
- Derive the source stencil for kappa_C and attach the root-quartic SU(N) screen with a certified error E_C.
- Aggregate source-equivalent endpoints before clipping, then multiply intervals by signed D_C and add the uniform tail.
- Obtain the one-sided lower bound I_- >= M_G-C_N sum D_C^+(A_C+E_C)-T_tail_abs when kappa_C is certified nonpositive.

Blocking gap: Actual same-theory endpoint source intervals and a regulator-uniform tail estimate are still missing for the positive-D classes.

## Falsifiers

- A positive-D endpoint class with a certified negative connected cumulant witness large enough that I_+<0 is a finite same-theory falsifier.
- The eighth-derivative or tail bound grows with cutoff or volume, invalidating the claimed uniform screen.
- A boundary counterterm is needed to define endpoint source derivatives, violating the same-theory condition.
- Two geometrically similar endpoints have different seven-point regulated source data, falsifying coarse aggregation by geometry alone.
- A negative interval caused by clipping before aggregation is a spurious falsifier and demotes the carrier, not the Wilson block.

## Learning

Cycle 347 makes the quarantined endpoint problem one-sided and computable: after valid cancellations, negative SU(N) endpoint cumulants are not themselves the obstruction; only positive-D leakage times a same-theory connected cumulant witness plus uniform tail can lower the finite OS gate. The sharp carrier is C_ep with aggregation before clipping and interval multiplication after source equivalence.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while keeping quarantine until endpoint source data are computed.`
- Rationale: The branch is looping on endpoint-carrier language; a target-preserving finite thought experiment focuses the next proof obligation on one measurable connected cumulant witness rather than another abstraction restatement.
- Situation seed: Heat-kernel SU(N) plaquette-sheet endpoint boxes for the same three reflected Wilson hairpins after the fixed H,K Schur-Feshbach reduction; all boxes share the same Wilson normalization and reflection map.
- Varied variable: The leakage ratio alpha=b12/(2(b13+b23)) for a source-equivalent endpoint class, varied from alpha<=1 shielded overlap to alpha>1 certified 12-dominance.
- Held-fixed controls: Gauge group SU(N), heat-kernel regulator, finite volume, and fixed lattice spacing during the finite calculation., The same three Wilson hairpins, null vector, H,K data, color factor C_N, and Gaussian margin M_G., No boundary counterterm, no change of test algebra, and no change of Wilson normalization., Uniform tail budget T_tail_abs and the same seven-point endpoint source stencil.
- Expected observation: For alpha<=1, negative root-quartic endpoint cumulants cannot lower the finite gate; for alpha>1, the interval M_G-C_N D^+(A+E)-T_tail_abs gives the first quantitative promotion or falsifier threshold.
- Transfer certificate needed: A validator-facing certificate that the endpoint source evaluations are same-theory Wilson derivatives, the source-equivalence aggregation is valid, and the tail bound is uniform before the intuition can alter proof obligations.

## Next Experiment

Run the validator-facing heat-kernel endpoint source computation for positive-D classes: compute f_c(jh), certify kappa_c intervals with the seven-point stencil or root-quartic cap, aggregate D_C before clipping, add C_N and T_tail_abs, and return the sign of [I_-,I_+] for promote/falsifier/quarantine.

# Annular Ward-Hessian compression for the H,K endpoint R term

## Candidate Lemma

Plateau-compressed annular Ward-Hessian lemma: for the same-theory flowed H,K plus hairpins, if each Ward-subtracted connected C4 sector has one certified stabilization annulus with decay q_s<1, then the endpoint polarization R_{++}^{ren} has an explicit lower interval Delta_R^-; Delta_R^->0 promotes finite endpoint-box positivity after H,K, while Delta_R^-<=0 is a valid quarantine falsifier for this R repair.

## Definitions

- source object: SU(N) Yang-Mills Wilson/gradient-flow regulator at flow time t with two centered renormalized H,K endpoint hairpin observables W_+^ren and endpoint sheet currents J_+.
- target object: the finite Route A endpoint-box dominance margin Delta_R^- deciding whether R_{++}^ren beats the Schur-Feshbach leakage L_+.
- controlled interface: Ward-subtracted endpoint sheet-current cumulant expansion with a recovery map from raw Wilson hairpins to centered flowed Wilson cumulants.
- same-theory condition: all pair, C4, counterterm, and recovery terms are computed in the same cutoff/flow Schwinger family before any finite endpoint-box transfer.
- observable: R_{++}^ren is the connected cumulant witness kappa_2(W_+^ren,W_+^ren) restricted to the H,K endpoint boxes, not a full non-Gaussian Schwinger family claim.
- hard gate changed: finite endpoint-box positivity after H,K; continuum construction, OS/Wightman axioms, observable density, topology control, OS spectral transfer, and the Hamiltonian mass gap remain untouched.

## Assumptions

- Model: four-dimensional SU(N) Euclidean Yang-Mills with Wilson lattice regulator or equivalent heat-kernel regularization, positive flow time t, and fixed finite H,K endpoint geometry.
- Regime: endpoint-box diameter rho is positive, sqrt(8t)/rho lies in a fixed compact window, and hairpin thickness eta is small enough for the endpoint moment expansion.
- Cutoff: outward-rounded interval constants are uniform over lattice spacing a below a_0 and over volumes containing the endpoint boxes with a fixed collar margin.
- Same-theory: raw-hairpin recovery, centered flowed Wilson cumulants, pair contractions, counterterms, and C4 sectors are all evaluated along one cutoff sequence and one bare-coupling tuning.
- Validity: Ward/cusp subtraction removes the disconnected product, one-hairpin perimeter/cusp terms, endpoint monopoles, and plus-channel dipoles before the Hessian bound is applied.
- Local: the claim is finite and endpoint-box restricted; it does not assert a continuum Schwinger family, OS positivity, or a spectral mass gap.

## Equations

- endpoint cumulant carrier: `R_{++}^{\mathrm{ren}}=\kappa_2(W_+^{\mathrm{ren}},W_+^{\mathrm{ren}})`. Valid when: Valid when W_+^ren is the centered flowed H,K hairpin observable recovered from the same cutoff Wilson action.
- pair minus C4 lower interval: `R_{++}^{\mathrm{ren}}\ge g_t^4(N^2-1)\left(2G_{++}^{-}-N M_{2,+}^2\sum_s T_s^{+}\right)-E_{\mathrm{rec}}^{+}`. Valid when: Requires Ward and cusp subtraction, plus-channel moment cancellation, and cutoff-uniform sector Hessian majorants.
- plateau tail compression: `T_s^{+}=\sum_{j<J}H_{s,j}^{+}+\frac{H_{s,J}^{+}+\varepsilon_{s,J}^{+}}{1-q_s},\qquad q_s=2^{4-2\nu_s}<1`. Valid when: Applies after a stabilization annulus J is certified with sector decay exponent nu_s greater than two.
- dominance margin: `\Delta_R^{-}=g_t^4(N^2-1)\left(2G_{++}^{-}-N M_{2,+}^2\sum_s T_s^{+}\right)-E_{\mathrm{rec}}^{+}-L_+`. Valid when: Valid when G, T_s, E_rec, and L_+ are enclosed with outward-rounded intervals in fixed endpoint boxes.
- finite endpoint promotion: `\Delta_R^{-}>0\Longrightarrow Q_+^{\mathrm{endpoint}}>0`. Valid when: Requires the finite Schur-Feshbach theorem and the same-theory lower interval Delta_R^- to be strictly positive.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: SU(N) Yang-Mills Wilson/gradient-flow regulator at flow time t with two centered renormalized H,K endpoint hairpin observables W_+^ren and endpoint sheet currents J_+.; target object: the finite Route A endpoint-box dominance margin Delta_R^- deciding whether R_{++}^ren beats the Schur-Feshbach leakage L_+.; Model: four-dimensional SU(N) Euclidean Yang-Mills with Wilson lattice regulator or equivalent heat-kernel regularization, positive flow time t, and fixed finite H,K endpoint geometry..
- Start from two centered flowed H,K plus hairpins W_+^ren and expand their covariance by the sheet-current cumulant expansion at positive flow time t.
- Subtract disconnected products and one-hairpin perimeter/cusp counterterms; the remaining Gaussian pair contraction has positive color factor 2(N^2-1) and gives G_{++}^-.
- For the connected four-curvature polarization, use Ward identities and plus-channel endpoint moment cancellation to eliminate monopole and dipole terms, leaving a mixed-Hessian remainder bounded by M_{2,+}^2 H_{s,j} on each sector-annulus cell.
- Split the endpoint complement into dyadic annuli. If sector s has derivative decay exponent nu_s>2 after stabilization annulus J, then H_{s,j+1}<=q_s H_{s,j}+epsilon_{s,j} with q_s=2^{4-2nu_s}<1.
- Sum the certified geometric tail and combine it with the finite near-annulus constants, recovery error E_rec^+, and Schur-Feshbach leakage L_+ to obtain Delta_R^-.

Blocking gap: The proof still lacks independently certified first-plateau constants H_{s,J}^+, epsilon_{s,J}^+, and cutoff-uniform nu_s>2 for the 3g, 4g, counterterm, and endpoint sectors.

## Falsifiers

- Falsifier: an annular sector with q_s>=1 makes the connected C4 tail non-summable in this carrier.
- Falsifier: Ward or cusp subtraction leaves a residual monopole or dipole endpoint term of order M_{1,+} rather than M_{2,+}.
- Falsifier: the lower interval Delta_R^- is nonpositive after outward rounding, so the endpoint repair cannot beat L_+.
- Falsifier: recovery from raw Wilson hairpins to centered flowed cumulants changes the Schwinger family or introduces regulator-dependent advice.
- Falsifier: zero-pairing quotienting hides a color, reflection, or orientation sign that changes the pair baseline.
- Stress case: shrink the endpoint separation toward the flow radius; if G_{++}^- collapses faster than the Hessian tail, the branch must quarantine the R repair.

## Learning

The conceptual pressure is the missing same-theory mediator between finite Schur-Feshbach positivity and Wilson cumulant positivity. The declarative tension is exact: positive flowed pair covariance, same-theory recovery, and endpoint positivity can each be valid while connected C4 destroys R_{++}. Raw Wilson contours are representation-limited; endpoint sheet currents are efficient because they preserve gauge, color, reflection, orientation, cutoff, locality, and same-theory invariants, use Ward/cusp subtraction, Hessian Taylor remainders, dyadic tail compression, outward-rounded intervals, and zero-pairing equivalence, and expose falsifiers. The value signal is local but route-changing: R_{++}/kappa_4 is a plateau-compressed annular dominance theorem rather than a symbolic boundary-OPE term. Reporting skill: timeline-definition-assumption-elicitor.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and quadrature rehearsal.`
- Rationale: The branch has a valid symbolic dominance margin but needs concrete annular constants; another abstract restatement will not decide whether endpoint-box positivity after H,K is plausible.
- Situation seed: SU(2) hypercubic Wilson lattice with gradient flow, two reflected H,K plus hairpins in fixed endpoint boxes, Ward/cusp-subtracted centered flowed Wilson cumulant R_{++}^{ren}, and outward-rounded interval quadrature for the first two annuli.
- Varied variable: alpha=sqrt(8t)/rho, the flow-radius to endpoint-box diameter ratio, varied over a compact interval such as [1/4,1].
- Held-fixed controls: Gauge group SU(2), H,K endpoint geometry, reflection orientation, and plus-channel current normalization are fixed., The same cutoff sequence, raw-hairpin recovery map, Ward/cusp subtraction, and Schur-Feshbach leakage L_+ are held fixed., Only centered flowed Wilson cumulants in the same theory are sampled; no area-law or external spectral assumption is imported.
- Expected observation: Either Delta_R^-(alpha) obtains a stable positive plateau on a subinterval, suggesting promotion of the finite endpoint gate, or a negative/unstable interval supplies a concrete falsifier and quarantine signal.
- Transfer certificate needed: A cutoff- and volume-uniform interval proof for G_{++}^-, H_{s,J}^+, q_s<1, recovery errors, and Ward/cusp cancellations before the intuition may affect proof obligations.

## Next Experiment

proof_search: run first-plateau annulus interval quadrature for the SU(2) H,K plus hairpin R_{++}^{ren}; record it as a connected cumulant witness and same-theory nontriviality witness only at finite local scope, not as a non-Gaussian Schwinger family or mass-gap proof.

# Raw signed-orbit K4 stress certificate for finite post-H,K endpoint PSD

## Candidate Lemma

Finite theorem: in one heat-kernel cutoff Yang-Mills theory, a signed-orbit lower bound on one phased off-diagonal raw K4 entry, together with two Schur-corrected diagonal upper bounds, gives a valid two-sparse falsifier for post-H,K endpoint positive semidefiniteness. It changes only the finite Route A endpoint-box gate.

## Definitions

- source object: heat-kernel lattice SU(N) Yang-Mills cutoff measure at spacing a, smoothing sigma, renormalized coupling g_R, and a fixed finite endpoint box carrying reflected Wilson collar/hairpin observables Q_i.
- target object: the finite Schur-corrected endpoint Hermitian interval matrix U_sigma on the post-H,K endpoint index set, not a continuum Hamiltonian or mass-gap operator.
- controlled interface: raw connected Wilson plaquette cumulant intervals recover entries of R_sigma and hence U_sigma through exact Wilson quotienting, OPE intervals, and S_HK subtraction.
- same-theory condition: all Wilson weights, heat-kernel transporters, K4 intervals, OPE errors, and H,K Schur blocks use the same cutoff action, coupling, regulator sigma, boundary normalization, and endpoint basis.
- connected cumulant witness: Q_i is the normal-ordered quadratic transported plaquette-flux observable assigned to endpoint i.
- signed raw orbit: an exact Wilson quotient class of oriented plaquette quadruples with multiplicity, color tensor, transporter phase, and interval enclosure for the connected four-flux cumulant.
- stress data: D_i^+ is an upper interval endpoint for U_ii and L_pq(theta) is a lower bound for |Re(e^{-i theta} U_pq)|.

## Assumptions

- Model: finite-volume heat-kernel lattice SU(N) Yang-Mills with reflection plane fixed before endpoint compression.
- Cutoff: a>0 and sigma>=a are fixed; no continuum, infinite-volume, or RG-uniform conclusion is claimed.
- Same-theory: the Gaussian covariance, raw K4 cumulants, OPE remainder, Wilson normalization, and Schur block S_HK are computed from the same regulated measure.
- Regime: the endpoint set is finite and the H,K hairpin block has already passed the finite Schur-Feshbach construction with QHQ invertible on the eliminated sector.
- Validity: interval arithmetic is outward-rounded, Hermitian, and quotiented only by exact Wilson trace, orientation, and reflection identities.
- Constraint: D_q^+>0 for the optimized two-sparse test; if D_i^+<0, PSD is already falsified.

## Equations

- endpoint quadratic flux observable: `Q_i=:\!\sum_{p,q\in\Sigma_i} W_i^{pq}\,X_p^a\,X_q^a\!:\,,\qquad X_p^a=\mathrm{Tr}\big(T^a\,\mathcal U_{p\to i}\,\log U_p\,\mathcal U_{p\to i}^{-1}\big)`. Valid when: Valid when the heat-kernel logarithm is taken inside the chosen plaquette chart and the endpoint sheet weights define the finite Wilson collar observable.
- connected boundary polarization: `R_{ij,\sigma}=\operatorname{cum}_{2,\mu_{a,g_R,\sigma}}(Q_i,Q_j)`. Valid when: Valid when Q_i and Q_j are vacuum-normalized in the same cutoff measure so disconnected perimeter and vacuum factors cancel.
- Gaussian plus K4 plus OPE decomposition: `R_{ij,\sigma}=\alpha_N g_R^4\,(C_\sigma\circ C_\sigma)_{ij}+\frac{g_R^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after normal ordering and crossed Wick contraction are separated from the connected four-flux cumulant in the same heat-kernel regulator.
- Schur-corrected endpoint matrix: `U_\sigma=R_\sigma-S_{HK,\sigma},\qquad S_{HK,\sigma}=B_\sigma^*E_\sigma^{-1}B_\sigma`. Valid when: Requires the finite H,K decomposition with positive eliminated block E_sigma and the identical endpoint basis used for R_sigma.
- two-sparse stress functional: `\tau_{pq}(\theta)=D_p^+-\frac{L_{pq}(\theta)^2}{D_q^+},\qquad L_{pq}(\theta)\le |\mathrm{Re}(e^{-i\theta}U_{pq})|`. Valid when: Valid when D_p^+ and D_q^+ are diagonal upper interval bounds and L_pq(theta) is certified from signed raw K4 orbit intervals plus Gaussian, OPE, and Schur terms.
- PSD falsifier vector: `x_{pq,\theta}=e_p-e^{i\theta}\frac{L_{pq}(\theta)}{D_q^+}e_q,\qquad x_{pq,\theta}^*U_\sigma x_{pq,\theta}\le \tau_{pq}(\theta)`. Valid when: Applies for a Hermitian interval matrix U_sigma with D_q^+ positive and phase theta chosen from a certified finite phase net.

## Attempted Derivation

- Conceptual pressure attacked: raw non-Gaussian Wilson K4 cumulants must mediate to a finite Schur-corrected endpoint PSD decision without circular OS Hilbert observable algebra or gauge-invariant observable density assumptions.
- Declarative tension: Wilson/OPE coefficients, K4 intervals, OPE error, and S_HK must be valid in one cutoff theory, but continuum Schwinger coherence, OS positivity, excitation-sector cyclicity, and Hamiltonian mass gap are non-claims.
- Choose the heat-kernel regulator and define endpoint observables Q_i as normal-ordered quadratic transported plaquette-flux sums in the finite H,K endpoint box.
- Use vacuum/perimeter cancellation and normal ordering to remove disconnected cumulant pieces; the remaining R_ij is a Gaussian crossed-flux contraction plus one connected four-flux cumulant K4 plus an OPE interval.
- Insert the already finite Schur-Feshbach subtraction S_HK=B^*E^{-1}B to form U_sigma=R_sigma-S_HK in the same endpoint basis.
- Recover K4_ij from signed raw plaquette orbits, preserving orientation, transporter phases, color tensors, Hermiticity, and exact Wilson quotienting; reject A012 shell data because it loses the phase needed for off-diagonal stress.
- For endpoints p,q form diagonal upper bounds D_p^+,D_q^+ and a phased off-diagonal lower bound L_pq(theta) from Gaussian, K4, OPE, and Schur intervals.
- Test x=e_p-e^{i theta}(L_pq/D_q^+)e_q; interval Rayleigh arithmetic gives x^*U_sigma x<=D_p^+-L_pq(theta)^2/D_q^+.
- Discretize theta with a phase net only after adding the angular derivative loss, so the stress certificate is finite and validator-facing.

Blocking gap: No actual same-regulator signed raw K4 orbit intervals I_O_sigma have been produced for the H,K endpoint geometry; the theorem is ready, but the numerical or rigorous interval input is missing.

## Falsifiers

- A valid same-regulator K4 orbit recovery gives D_i^+<0, immediately falsifying finite endpoint PSD.
- A phase theta with L_pq(theta)^2>D_p^+D_q^+ gives a two-sparse stress falsifier for the worked H,K collar/hairpin endpoint route.
- The signed-orbit quotient identifies plaquette quadruples with different transporter phases, making the interval non-invariant and invalid.
- The OPE remainder interval exceeds the Gaussian plus K4 margin, so the finite endpoint gate cannot be decided.
- The heat-kernel regulator used for K4 intervals differs from the one used for S_HK or Gaussian covariance, violating the same-theory condition.
- All phase-net stresses survive, but full Delta_raw has a negative eigenvector; this falsifier shows the two-sparse tactic was incomplete, not that the route is valid.

## Learning

Cycle 347 attacks the conceptual pressure that raw non-Gaussian Wilson K4 data must become a finite endpoint PSD decision without OS-density circularity. The declarative tension is that Wilson/OPE data, signed K4 orbit intervals, OPE error, and S_HK must all hold in one cutoff theory while Clay-level continuum existence, OS positivity, excitation-sector cyclicity, observable density, and mass gap remain untouched. Carrier audit: scalar R is too weak, A012 shells are sign-losing, OS Hilbert observable algebra is too strong and circular, and full Delta_raw is complete but expensive; signed raw orbits plus a finite phase net are efficient because they preserve gauge invariance, Hermiticity, phases, color, exact Wilson quotienting, locality, and same-theory normalization. Hard gate: D_i^+<0 or L_pq(theta)^2>D_p^+D_q^+ supplies a valid finite falsifier; failure gives no positivity and forces full Delta_raw proof search or quarantine. Conceptual value signal: sharp and route-changing at finite scope because Gaussian color positivity, connected non-Gaussian K4, OPE error, and Schur hairpin energy are unified in one connected cumulant witness without implying the Clay theorem.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and validator-facing computation design.`
- Rationale: The branch is looping unless it produces raw same-regulator K4 intervals; a concrete thought experiment isolates whether signed phases can actually beat diagonal Gaussian-Schur protection in the finite H,K endpoint matrix.
- Situation seed: SU(3) heat-kernel lattice on a fixed reflected endpoint box with two post-H,K endpoint observables Q_p,Q_q supported on adjacent collar plaquette sheets and one hairpin Schur block S_HK already computed as an interval matrix.
- Varied variable: The smoothing ratio beta=sigma/a, varied over a finite grid while keeping the endpoint geometry and H,K Schur block construction fixed.
- Held-fixed controls: Same Wilson action, coupling g_R, heat-kernel regulator, reflection plane, and boundary normalization for Gaussian, K4, OPE, and S_HK data., Exact endpoint basis, signed-orbit quotient policy, transporter convention, color tensors, and phase-net mesh rule., Finite endpoint-box locality budget and no continuum, OS spectral-transfer, or mass-gap inference.
- Expected observation: Either a beta-window produces L_pq(theta)^2>D_p^+D_q^+ and demotes the H,K endpoint route, or the off-diagonal K4 phases never overcome diagonal protection and the branch must attempt full Delta_raw PSD proof search.
- Transfer certificate needed: A same-theory connected cumulant witness certificate listing orbit intervals I_O_sigma, quotient invariance checks, OPE interval bounds, Schur block intervals, phase-net derivative loss, and outward-rounded Rayleigh arithmetic before the intuition may affect proof obligations.

## Next Experiment

Proof search: compute the first SU(3) same-regulator signed-orbit K4 intervals for one adjacent endpoint pair (p,q), assemble D_p^+, D_q^+, and L_pq(theta) with Gaussian, OPE, and S_HK terms, then either emit x_stress as a finite falsifier or hand off to full Delta_raw PSD search.

