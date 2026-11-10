# cycle-0305

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint root-quartic carrier for post-H,K reflected Wilson block

## Candidate Lemma

Finite endpoint root-quartic interval certificate: for the three-hairpin post-H,K null channel, the connected boundary-OPE polarization is controlled by a same-theory endpoint source carrier; negative SU(N) endpoint kappa_4 is dangerous only through positive endpoint dominance D_v>0 plus tail.

## Definitions

- source object: heat-kernel regulated SU(N) reflected Wilson hairpin endpoint boxes with plaquette-sheet sources L_v and source partition functions Z_v(s).
- target object: finite post-H,K OS transfer scalar for the three-hairpin block, not the continuum Yang-Mills mass gap theorem.
- controlled interface: endpoint source carrier C_ep sending regulated connected fourth source derivatives and signed incidences to one Schur-Feshbach interval.
- same-theory condition: the Wilson loops, heat-kernel plaquette sheets, reflection map, and source insertions are identical before collar collapse and after endpoint aggregation; no boundary counterterm or algebra enlargement is allowed.
- carrier critique: raw R is representation-limited because it hides incidence signs; raw kappa_4 spectra are too strong because negative kappa_4 is harmless under D_v<=0.
- efficient representation: encode endpoint classes, seven source values, kappa intervals, b_ij incidences, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette-sheet regularization of reflected Wilson hairpin collars.
- Regime: finite three-hairpin block after the previously computed H,K Schur-Feshbach reduction; endpoint boxes are small but cutoff-resolved.
- Cutoff: the endpoint source expansion uses heat-kernel coordinates inside a fixed injectivity radius with remainders uniform in the collar collapse.
- Uniformity: the error intervals E_v and tail T_tail are bounded independently of lattice spacing along the selected regulator/RG basin.
- Same-theory: endpoint source derivatives are evaluated in the original gauge-invariant Wilson theory and not in a boundary-renormalized theory.
- Local: all non-endpoint overlap, corner leakage, and unclassified geometry is charged to T_tail before transfer.
- Validity: this is a restricted finite Wilson-block certificate and does not assert continuum existence, observable density, OS reconstruction for all fields, nontriviality, or mass gap.

## Equations

- endpoint cumulant source: `\kappa_v(L_v)=\left.\frac{d^4}{ds^4}\log Z_v(sL_v)\right|_{s=0}`. Valid when: Valid when Z_v is the heat-kernel endpoint-box source partition function for the same regulated Wilson plaquette sheet.
- SU(N) root-quartic term: `\kappa_v(L_v)=-\frac{t_v^4}{60}R_4(L_v)+E_v,\qquad R_4(L)=N\operatorname{tr}(L^4)+3(\operatorname{tr}(L^2))^2`. Valid when: Valid in heat-kernel endpoint coordinates for small source norm, with E_v absorbing sixth and higher Haar-Jacobian and interaction terms.
- root-quartic norm cap: `0\le R_4(L_v)\le (N+3)\|L_v\|_2^4`. Valid when: Applies after diagonal normalization of the Hermitian endpoint source L_v in the fundamental trace convention.
- null-channel endpoint incidence: `D_v=2b_{12}(v)-4b_{13}(v)-4b_{23}(v),\qquad b_{13}(v)+b_{23}(v)\ge b_{12}(v)/2\Rightarrow D_v\le 0`. Valid when: Valid for the previously fixed three-hairpin null vector and fractional endpoint incidences measured in the same endpoint class.
- safe lower interval: `I_- = M_G-\frac{C_N}{60}\sum_v [D_v]_+t_v^4\overline{R}_{4,v}-C_N\sum_v |D_v|\overline E_v-T_{tail}`. Valid when: Valid when protective D_v<0 root-quartic contributions are discarded and all remainder signs are bounded adversarially.
- promotion and falsifier tests: `I_-\ge 0\Rightarrow \text{finite block promoted},\qquad I_+<0\Rightarrow \text{finite same-theory falsifier}`. Valid when: Valid after the same endpoint source classes, color factor C_N, Gaussian margin M_G, and tail interval define both I_- and I_+.

## Attempted Derivation

- Freeze the Clay claim level: this cycle targets only the finite post-H,K reflected-Wilson OS block; continuum construction, OS/Wightman reconstruction, nontriviality, and mass gap remain untouched.
- Use heat-kernel plaquette-sheet endpoint boxes as source objects and keep Wilson loops gauge-invariant throughout; this preserves the same-theory observable algebra.
- Expand the local SU(N) Haar-Jacobian factor in endpoint coordinates; the fourth connected source derivative gives the negative root-quartic term -(t_v^4/60)R4(L_v) plus an explicit remainder interval E_v.
- Apply previous cancellations: connected log removes Wick-square disconnected pieces from kappa_v, positive Wick-square Gram pieces are not a demoter, and the straight C_A f f contact cancels in the H,K null incidence channel.
- Contract with the fixed null-channel endpoint incidences to obtain D_v=2b12-4b13-4b23; the half-overlap shield b13+b23>=b12/2 makes D_v<=0 and therefore protective for the negative root-quartic term.
- Replace uncomputed endpoint source data by intervals: upper R4, E_v, color factor C_N, Gaussian margin M_G, and T_tail define I_-; if I_- is nonnegative, the finite block is promoted.
- Define the negative tactic: compute I_+ with lower dangerous root-quartic and upper protective/tail budgets; I_+<0 is a concrete finite same-theory falsifier.

Blocking gap: Actual regulated endpoint source intervals, fractional incidence data for the selected hairpin geometry, and cutoff-uniform tail bounds are not yet computed.

## Falsifiers

- A positive-D endpoint source class has certified negative cumulant leakage large enough that I_+<0; this is a finite same-theory falsifier.
- The tail T_tail is not cutoff-uniform, so endpoint locality fails before the OS transfer gate.
- The fourth source cumulant requires a boundary counterterm or modified Wilson normalization, breaking the same-theory condition.
- Source-equivalence aggregation by geometry rather than regulated source data erases a 12-dominant class.
- The heat-kernel endpoint expansion is not valid uniformly in the selected RG basin or leaves the injectivity radius.

## Learning

Conceptual pressure attacked: endpoint collapse must be sign-certified in the same Wilson theory, not hidden in symbolic R. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint boundary OPE must jointly hold without a boundary theory; H,K plus half-overlap data do not decide the scalar. Carrier audit: raw R is too weak, raw kappa_4 spectra are too strong, and the global Schur-preimage test is valid but too coarse after H,K. Conceptual value signal: the SU(N) root-quartic cumulant is explicitly negative but not itself the obstruction; only positive-D endpoint dominance plus uncontrolled tail can demote the finite block. This is sharp and route-changing at finite scope, while all Clay-level continuum, nontriviality, full OS/Wightman, and mass-gap gates remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe for the quarantined endpoint carrier.`
- Rationale: The branch is data-waiting; another abstract OS/Wilson restatement would not change the proof state, while varying endpoint dominance directly tests the only remaining demotion mechanism after H,K.
- Situation seed: Heat-kernel SU(N) plaquette-sheet endpoint-box family for the fixed three reflected Wilson hairpins, with one source-equivalence class carrying a connected cumulant witness from seven evaluations of log Z_v.
- Varied variable: alpha=(b13+b23)/b12, the fractional half-overlap ratio controlling D_v=2b12-4b13-4b23.
- Held-fixed controls: Gauge group SU(N), fundamental trace normalization, and heat-kernel plaquette-sheet regulator., The previously computed H,K finite block and null vector used for the Schur-Feshbach endpoint scalar., Same-theory Wilson loop algebra, reflection map, source stencil, color factor C_N, and Gaussian margin M_G., No boundary counterterm, no change of observable algebra, and a fixed tail budget T_tail.
- Expected observation: For alpha>=1/2 the leading negative root-quartic cumulant is protective or neutral; for alpha<1/2 it leaks into [D_v]_+ and can become a falsifier only if the certified source interval overwhelms M_G and tails.
- Transfer certificate needed: A cutoff-uniform endpoint source interval theorem, fractional incidence table, and same-theory recovery map proving that the finite source carrier equals the Wilson boundary-OPE contribution before it may affect OS proof obligations.

## Next Experiment

Proof search plus endpoint-data computation: build the heat-kernel SU(N) endpoint-box connected cumulant witness, vary alpha below and above one half, compute seven-point log Z_v intervals and D_v incidences, then certify either I_->=0 for finite promotion or I_+<0 as a valid finite falsifier.

# Gauge-Invariant Nontriviality Witness Selection -> finite endpoint R_{++} sector certificate

## Candidate Lemma

Conditional finite theorem: for the concrete post-H,K plus endpoint box, the renormalized flowed Wilson covariance R_{++}^{ren} has a certified lower interval equal to the positive pair contraction minus Ward-Hessian majorants for the connected four-curvature polarization and recovery errors. If this lower interval beats the Schur-Feshbach leakage L_+, finite endpoint-box positivity is promoted; otherwise this R repair is quarantined.

## Definitions

- source object: the centered same-theory flowed Wilson hairpin covariance R_{++}^{ren}(t,a;I)=\kappa_2(\widetilde W_+^t(J_H),\widetilde W_+^t(J_K)) after disconnected-product removal and one-hairpin perimeter/cusp counterterms.
- target object: the finite Route A endpoint-box positivity margin \Delta_+=R_{++}^{ren}-L_+ for the already derived Schur-Feshbach plus channel, not a continuum mass-gap statement.
- controlled interface: endpoint sheet-current representation with cell moments, sector kernels, recovery map \rho_{a,t}, and outward-rounded interval arithmetic for the same Wilson observable family.
- same-theory condition: all Wilson loops, flow-time fields, counterterms, recovery maps, and cumulants are taken along one lattice Yang-Mills regulator/RG family and one limiting Schwinger family, with no auxiliary Gaussian theory substituted.

## Assumptions

- Model: pure SU(N) Yang-Mills on a hypercubic lattice with Wilson plaquette action, positive gradient-flow time t, and flowed curvature insertions used only as gauge-invariant regulators of Wilson cumulants.
- Regime: endpoint boxes have diameter eta, mutual separation d, eta <= d/8, a << sqrt(8t) <= d/4, and H,K sheets are the fixed collar/hairpin sheets from the finite Route A instance.
- Cutoff: the heat-kernel Hessian constants, cusp counterterm intervals, and recovery errors are bounded uniformly for all a below a validator-specified a0 on the chosen RG trajectory.
- Same-theory: R_{++}^{ren}, the positive pair term, the connected C4 sectors, and L_+ are evaluated for the same H,K Wilson observables and not transferred from a different continuum measure.
- Validity: the g_t^4 displayed expansion is used as an interval identity with an explicit E_6 remainder; without a certified E_6 bound it is only a perturbative sketch.
- Local: the claim changes only finite endpoint-box positivity after H,K; continuum construction, OS/Wightman axioms, observable density, and Hamiltonian mass gap remain untouched.

## Equations

- renormalized endpoint covariance decomposition: `R_{++}^{ren}=g_t^4(N^2-1)\bigl(2G_{++}^{I}+N C_{4,++}^{WS,I}\bigr)+E_6^{I}`. Valid when: Valid when the centered flowed Wilson hairpins are expanded through fourth order with perimeter, cusp, and disconnected products subtracted in the same regulated Yang-Mills family.
- plus-channel Ward moment cancellation: `\sum_{e\in E_+}q_e^a=0,\qquad \sum_{e\in E_+}q_e^a(x_e-x_0)_\mu=0`. Valid when: Applies when the H,K plus endpoint current is built from the reflected collar and hairpin sheets with the certified orientation and color conventions.
- connected C4 Ward-Hessian majorant: `|C_{4,++}^{WS,I}|\le M_{2,+}^2\bigl(H_{3g}^{I,+}+H_{4g}^{I,+}+H_{ct}^{I,+}+H_{end}^{I,+}+H_{far}^{I,+}\bigr)+\varepsilon_{rec}^{I}`. Valid when: Valid after Ward and cusp subtraction remove zeroth and first endpoint moments, leaving only Hessian-controlled cell remainders in each sector kernel.
- route-deciding lower interval: `R_{++}^{I,-}=g_t^4(N^2-1)\left(2G_{++}^{I,-}-N M_{2,+}^2H_4^{I,+}\right)-g_t^4N(N^2-1)\varepsilon_{rec}^{I}-E_6^{I,+}`. Valid when: Requires outward-rounded intervals for G_{++}, all H_4 sector constants, recovery errors, and the sixth-order Wilson remainder at fixed flow time.
- finite endpoint promotion inequality: `R_{++}^{I,-}>L_+`. Valid when: Valid as a finite Route A positivity certificate only when L_+ is the Schur-Feshbach leakage computed for the identical H,K finite matrix block.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, while positive flowed pair covariance can be erased by connected C4 polarization.
- Declarative tension: Schur-Feshbach positivity, Wilson cumulant positivity, and same-theory recovery must jointly be valid; the missing mediator is a cutoff-stable Ward-Hessian sector bound for C4 plus recovery errors.
- Carrier critique: raw Wilson contours are fragmented and representation-limited; global OS spectral transfer or a non-Gaussian Schwinger family route is too coarse for this finite obstruction.
- Abstraction comparison: endpoint sheet currents are sharper because they encode H,K sheets, endpoint charges, cell moments, sector kernels, and counterterms while making Ward subtraction, heat-kernel majorants, interval quadrature, and zero-pairing quotienting primitive.
- Expand each centered flowed Wilson hairpin to the quadratic curvature sheet term; after disconnected-product and one-hairpin perimeter/cusp subtraction, the cross-pair Wick contraction gives the positive baseline 2g_t^4(N^2-1)G_{++}.
- Collect the non-pair fourth-order remainder into C_{4,++}^{WS} and decompose it into I_{3g}, I_{4g}, I_{ct}, I_{end}, and I_{far}; this names the actual connected Wilson contraction being evaluated.
- Use the plus endpoint current identities sum q=0 and sum q(x-x0)=0 to cancel monopole and dipole terms in each local sector kernel; the remaining Taylor term is bounded by M_{2,+}^2 times a sector Hessian supremum.
- Split cells into near and far boxes; near boxes require outward-rounded quadrature of Hessian kernels, while far boxes are bounded by flowed heat-kernel Gaussian tails.
- Insert the C4 majorant and recovery budget into R_{++}^{I,-}; compare with the previously fixed Schur-Feshbach leakage L_+ to decide the finite endpoint-box gate.

Blocking gap: The proof still lacks certified numerical or analytic intervals for H_{3g}^{I,+}, H_{4g}^{I,+}, H_{ct}^{I,+}, H_{end}^{I,+}, H_{far}^{I,+}, and E_6^{I,+} for the concrete H,K geometry.

## Falsifiers

- falsifier: the plus-channel endpoint current fails the certified monopole or dipole cancellation after recovery, so Hessian suppression is invalid.
- falsifier: the connected C4 sector interval satisfies N M_{2,+}^2H_4^{I,+} >= 2G_{++}^{I,-}, erasing the positive pair baseline before comparison with L_+.
- falsifier: the sixth-order Wilson remainder E_6^{I,+} is not controlled uniformly in the regulator window.
- falsifier: the flowed covariance plateau changes sign or size under allowed t variation, indicating regulator fragility rather than a same-theory endpoint term.
- falsifier: zero-pairing quotienting identifies two sheet currents with different C4 sector intervals.
- falsifier: the lower interval R_{++}^{I,-} is valid but does not beat L_+, so endpoint-box positivity is not promoted for this H,K repair.

## Learning

Cycle 305 makes a contribution-shaped refinement: the actual boundary-OPE polarization R_{++} is decomposed into a positive pair contraction plus named connected C4 sector kernels, then bounded by Ward-Hessian endpoint moments and recovery errors. The hard gate is finite endpoint-box positivity after H,K. The conceptual value signal is local but route-changing: a symbolic endpoint term becomes a valid falsifiable color-geometric interval certificate. Efficient representation requirements are explicit: encode H,K sheets, endpoint currents, cell moments, sector kernels, counterterms, and recovery errors; preserve gauge, color, reflection, orientation, cutoff, locality, and same-theory identity; use cumulant expansion, Ward/cusp subtraction, endpoint Taylor remainders, heat-kernel majorants, outward-rounded interval quadrature, and zero-pairing quotienting; keep finite endpoint-cell locality; transfer only through centered flowed Wilson cumulants; demote on any falsifier. Clay existence, OS/Wightman axioms, nontrivial continuum limit, gauge-invariant observable density, large-field/topology control, and positive Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the certified sector-constant proof search.`
- Rationale: The branch has repeated the interval architecture; the concrete mathematical pressure is whether Ward-Hessian suppression of connected C4 is strong enough in an actual H,K endpoint box before further abstraction is useful.
- Situation seed: SU(2) Wilson lattice Yang-Mills with gradient flow at t, fixed reflected H,K collar/hairpin sheets, centered flowed Wilson hairpins in two endpoint boxes, and interval evaluation of the connected cumulant witness R_{++}^{ren}.
- Varied variable: The endpoint-cell diameter ratio alpha=eta/sqrt(8t), varied over alpha in [1/8,1/2] while keeping eta <= d/8.
- Held-fixed controls: Same bare-coupling/RG trajectory and same flowed Wilson observable family for pair and C4 terms., Fixed H,K geometry, reflection orientation, color normalization tr(T^aT^b)=delta^{ab}/2, and Schur-Feshbach leakage L_+., Fixed counterterm prescription: disconnected product removal plus one-hairpin perimeter and cusp subtraction., Fixed finite endpoint-cell refinement depth and outward-rounded interval arithmetic.
- Expected observation: If the Ward-Hessian mechanism is real, the ratio |C4_{++}^{WS}|/G_{++} decreases like O(alpha^2) after moment cancellation, and a nonempty alpha window yields R_{++}^{I,-}>L_+; if not, C4 remains order one and the R repair is demoted.
- Transfer certificate needed: A cutoff-uniform interval proof that the lattice-flowed sector constants, recovery errors, and E_6 remainder bound the same-theory Wilson cumulant used in the finite H,K Schur-Feshbach block.

## Next Experiment

Route to proof search: implement a validator-facing same-theory nontriviality witness boundary check by computing the centered flowed Wilson connected cumulant R_{++}^{ren} for the concrete H,K endpoint cells, enclosing G_{++}, H_{3g}, H_{4g}, H_{ct}, H_{end}, H_{far}, E_6, and recovery errors, then decide the finite inequality R_{++}^{I,-}>L_+ or quarantine this endpoint repair.

# Raw K4 two-sparse connected-cumulant stress certificate

## Candidate Lemma

Finite theorem: for endpoint nodes p,q, same-regulator intervals for U=R_sigma-S_HK give b_i>=U_ii and ell_theta<=|Re(e^{-i theta}U_pq)|. If b_q>0 and tau=b_p-ell_theta^2/b_q<0, a two-sparse vector falsifies endpoint PSD.

## Definitions

- source object: heat-kernel regulated SU(N) lattice YM Wilson OPE data for finite H,K endpoint plaquette sheets, including connected four-curvature cumulant intervals.
- target object: finite two-dimensional endpoint compression U_{pq,sigma}=R_sigma-S_{HK,sigma} on the post-H,K Wilson basis, not a continuum Hamiltonian spectrum.
- controlled interface: raw plaquette interval sums recover the Schur-corrected endpoint quadratic form through R_G+K4+E_OPE-S_HK with explicit error budgets.
- same-theory condition: the Wilson sheets, regulator sigma, cutoff a, coupling g_R, vacuum subtraction, and H,K Schur blocks are all from the same cutoff measure.
- bridge carrier: validator-facing connected cumulant witness encoded by oriented plaquette quartets, transported color tensors, sheet weights, and interval arithmetic.
- non-claim boundary: no gauge-invariant observable density, OS reconstruction, continuum nontriviality, or Clay mass gap follows from this finite stress test.

## Assumptions

- Model: finite-volume SU(N) heat-kernel lattice gauge theory with reflection-compatible Wilson endpoint boxes.
- Regime: fixed cutoff a>0 and regulator width sigma/a fixed; no volume or continuum uniformity is asserted.
- Same-theory: R_sigma, K4 intervals, OPE bounds, and S_HK are computed from the identical action, basis, normalization, and vacuum subtraction.
- Validity: interval endpoints are outward-rounded after exact Wilson trace quotienting and preserve Hermitian symmetry of U.
- Local: only the p,q endpoint compression is tested; survival of this test forces full Delta_raw proof search.

## Equations

- raw R decomposition: `R_{ij,\sigma}=\alpha_N g_R^4\sum_{\pi\in S_i,\rho\in S_j} w_i(\pi)w_j(\rho)C_\sigma(\pi,\rho)^2+\frac{g_R^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma}`. Valid when: Valid when heat-kernel regulated Wilson loops are expanded to endpoint boundary-OPE order with vacuum and perimeter disconnected cumulants subtracted.
- phased raw K4 contraction: `K^{(4)}_{pq,\sigma}(\theta)=\operatorname{Re}\,e^{-i\theta}\sum_{\pi_1,\pi_2\in S_p\atop \rho_1,\rho_2\in S_q}W_{pq}^{abcd}\kappa^{abcd}_{\sigma,c}(\pi_1,\pi_2,\rho_1,\rho_2)`. Valid when: Applies after exact Wilson trace quotienting fixes orientations, transporters, color tensors, sheet weights, and connected four-curvature cumulant conventions.
- two-sparse demotion margin: `b_i=\overline U_{ii},\quad \ell_\theta=\max(0,-\underline{\operatorname{Re}(e^{-i\theta}U_{pq})}),\quad \tau_{pq}(\theta)=b_p-\ell_\theta^2/b_q`. Valid when: Valid when U=R_\sigma-S_{HK,\sigma} is Hermitian, b_q>0, and intervals enclose every same-regulator OPE and Schur contribution.

## Attempted Derivation

- Conceptual pressure: turn boundary-OPE polarization into a route-deciding finite witness, not another OS-density or symbolic R restatement.
- Declarative tension: Wilson/OPE data, connected K4 negativity, OPE error, and H,K Schur subtraction must share one cutoff while Clay-level spectral conclusions are barred.
- Carrier critique: scalar R is too weak, OS Hilbert observable algebra is circular here, A012 shells remain quarantined; raw plaquette intervals are fragmented but valid.
- For x=(1,-e^{-i theta}ell_theta/b_q), interval arithmetic gives x^*Ux<=tau; tau<0 contradicts endpoint PSD and demotes this H,K geometry.

Blocking gap: No certified raw same-regulator intervals yet for the selected plaquette quartets in K^{(4)}_{pq,sigma}(theta).

## Falsifiers

- falsifier: the K4 phased lower interval widens so ell_theta^2<=b_p b_q for every admissible phase sector.
- falsifier: exact Wilson trace quotienting changes the sign or multiplicity of a contributing plaquette quartet.
- falsifier: OPE or Schur intervals are not computed in the same cutoff theory as the connected cumulant witness.
- falsifier: tau>=0 for all two-sparse pairs; then this negative tactic is demoted and full Delta_raw proof search is required.

## Learning

The new contribution is a phase-resolved raw K4 stress gate. It is sharp and explanatory because three same-theory endpoint intervals can falsify post-H,K positivity. It changes only the finite Route A endpoint-box gate; OS/Wightman reconstruction, nontrivial continuum YM, gauge-invariant observable density, and Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for finite Route A.`
- Rationale: The branch needs concrete raw K4 intervals; more abstraction would loop after the tau theorem.
- Situation seed: First H,K endpoint box in heat-kernel SU(2) lattice YM, with two reflected Wilson sheet nodes p,q and their oriented plaquette quartet list.
- Varied variable: phase sector theta used to align the off-diagonal connected four-curvature cumulant.
- Held-fixed controls: same cutoff a, regulator sigma, coupling g_R, Wilson basis, and vacuum subtraction, same H,K Schur block S_HK and the same endpoint compression U, exact Wilson trace quotienting and Hermitian interval enclosure
- Expected observation: A theta with tau<0 gives a finite stress falsifier; absence of such theta transfers the pair to full Delta_raw PSD search.
- Transfer certificate needed: A validator-facing interval certificate for K4_{pq}(theta), U_pp, U_qq, OPE error, and S_HK with exact quotient audit and same-theory tags.

## Next Experiment

Proof search: compute a validator-facing connected cumulant witness for one SU(2) H,K endpoint pair p,q, including raw K4 phased interval, Gaussian color square, OPE interval, and Schur block; gauge-invariant observable density remains a non-claim.

