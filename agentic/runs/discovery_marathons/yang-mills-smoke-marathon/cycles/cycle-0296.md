# cycle-0296

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint-source cutset for the post-H,K reflected-Wilson OS gate

## Candidate Lemma

Endpoint positive-dominance is a necessary data cutset: after the finite H,K Schur-Feshbach reduction, no valid same-theory promotion can be inferred from the half-overlap shield alone unless every source-equivalence class with possible positive D has a certified connected fourth source interval and a cutoff-uniform tail bound.

## Definitions

- source object: heat-kernel plaquette-sheet endpoint carrier C_ep(a,L) consisting of source-equivalence classes alpha, seven source values for log Z_alpha(s), kappa_4 intervals K_alpha, fractional incidences b_ij, color factor C_N, Gaussian margin M_G, and tail interval T_tail.
- target object: the finite post-H,K reflected-Wilson OS gate for the fixed three-hairpin block, namely the scalar lower endpoint of the Schur-Feshbach null-channel interval whose positivity promotes only this finite block.
- controlled interface: C_ep exports only the interval [I_-,I_+] obtained by same-theory source differentiation, incidence contraction, color multiplication, interval multiplication, clipping only as a lower-bound operation, and tail addition.
- same-theory condition: all source values are derivatives of the same regulated Wilson plaquette action with the same loop normalization, no boundary counterterm, no changed gauge-invariant algebra, and no boundary Hilbert sector added.
- Endpoint dominance is D_alpha=2 b_{12,alpha}-4 b_{13,alpha}-4 b_{23,alpha}.
- The connected cumulant witness is kappa_alpha=partial_s^4 log Z_alpha(s)|_{s=0} after subtracting lower Wick-square contractions by connected logarithmic differentiation.
- A source-equivalence class means equality of all regulated source derivatives used in the stencil, not geometric resemblance of endpoint boxes.

## Assumptions

- Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action and gauge-invariant Wilson collar observables.
- Regime: finite lattice spacing a>0, finite volume L, fixed reflected three-hairpin collar geometry, and post-H,K endpoint boxes smaller than the collar scale.
- Cutoff: the endpoint classes and T_tail are defined before cutoff removal and must admit bounds uniform in a,L along the intended RG subsequence.
- Same-theory: the source deformation is used only for differentiation at s=0 and is not added as a new boundary interaction in the target theory.
- Validity: the prior Schur-Feshbach reduction has already removed one-body Wilson factors, Wick-square Gram terms, and straight f f incidence contacts.
- Local: all unresolved nonlocal or overlapping endpoint effects not assigned to a source-equivalence class are charged to T_tail.
- Constraint: C_N>0 and M_G>0 are fixed by the already computed finite H,K block and are not refitted using endpoint data.

## Equations

- endpoint gate scalar: `I_{\rm gate}=M_G+C_N\sum_{\alpha}\kappa_{\alpha}D_{\alpha}+T_{\rm tail}`. Valid when: Valid when the reflected Wilson block has passed the finite H,K Schur-Feshbach reduction and the remaining connected boundary OPE is localized into source-equivalent endpoint classes.
- null incidence dominance: `D_{\alpha}=2b_{12,\alpha}-4b_{13,\alpha}-4b_{23,\alpha}`. Valid when: Valid when the three fixed hairpin observables use the previously locked null vector and b_ij are same-theory fractional endpoint incidences.
- rectangular interval lower endpoint: `I_- = M_G+C_N\sum_{\alpha}\min\{k^-_{\alpha}d^-_{\alpha},k^-_{\alpha}d^+_{\alpha},k^+_{\alpha}d^-_{\alpha},k^+_{\alpha}d^+_{\alpha}\}-\tau`. Valid when: Applies when kappa_alpha lies in [k^-_alpha,k^+_alpha], D_alpha lies in [d^-_alpha,d^+_alpha], and |T_tail| is bounded by tau uniformly in cutoff.
- H,K insufficiency crossing: `\kappa_{\alpha_*}^{\rm crit}=-\frac{M_G+C_N\sum_{\alpha\ne\alpha_*}\kappa_{\alpha}D_{\alpha}+T_{\rm tail}}{C_ND_{\alpha_*}}\quad(D_{\alpha_*}>0)`. Valid when: Valid as a finite carrier stress test when one positive-dominance endpoint class remains source-uncomputed while all H,K data and incidences are held fixed.

## Attempted Derivation

- Start from the already reduced finite Schur-Feshbach null channel, where M_G>0 is the Gaussian margin and all one-body, Wick-square, and straight f f contact pieces have been removed.
- Represent the remaining connected boundary OPE by source-equivalence classes alpha with scalar contribution C_N kappa_alpha D_alpha plus T_tail.
- Observe that D_alpha is fixed by fractional incidence data and is independent of the connected fourth source cumulant kappa_alpha.
- If some class alpha_* has D_alpha_*>0 and kappa_alpha_* is not certified, then varying only kappa_alpha_* in the endpoint carrier crosses I_gate=0 at kappa_alpha_*^crit while leaving H,K and the half-overlap bookkeeping unchanged.
- Therefore H,K plus half-overlap data are not sufficient to promote the finite OS gate; a valid proof must provide source intervals for all positive-dominance classes and a uniform tail bound.
- For source-equivalent boxes, sum signed D first; this preserves null cancellations that would be destroyed by absolute-value or raw-spectrum carriers.

Blocking gap: No same-theory heat-kernel endpoint source intervals and no cutoff-uniform T_tail estimate are available for the positive-D source classes.

## Falsifiers

- falsifier: an endpoint source computation gives I_-<0 for a same-theory positive-D class with uniform tail, producing a finite reflected-Wilson OS counterexample.
- falsifier: the seven-point source stencils require a boundary counterterm or changed Wilson-loop normalization, breaking the same-theory condition.
- falsifier: T_tail is not cutoff-uniform and can dominate the positive H,K margin.
- A valid demotion of the cutset lemma would be a Ward identity proving all positive-D connected fourth cumulant contributions are nonnegative without using endpoint data.
- A stress case is a tiny 12-only endpoint box with D>0 and a large negative connected cumulant witness, while H,K and all collar data remain unchanged.

## Learning

Conceptual pressure attacked: endpoint collapse must be sign-certified in the same Wilson theory, not hidden in symbolic R. Declarative tension: finite collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist without adding a boundary theory, but H,K plus half-overlap data do not determine the post-H,K scalar. Carrier critique: raw R is too weak, raw kappa_4 spectra are too strong, and the global Schur-preimage test is valid but too coarse after H,K. The efficient representation is C_ep: source classes, seven source values, kappa intervals, signed incidences, C_N, M_G, and T_tail, preserving Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables. Conceptual value signal: route-changing sharpness at finite scope; the obstruction is missing positive-D connected cumulant witness data plus tail, not negative kappa_4 itself.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe while the branch remains quarantined for missing endpoint source data.`
- Rationale: The branch is otherwise looping on endpoint-carrier language. A concrete positive-D endpoint source stress test shows exactly what data can promote or demote the finite post-H,K gate without touching Clay-level claims.
- Situation seed: Heat-kernel SU(N) plaquette-sheet endpoint box for the fixed three-hairpin reflected Wilson collar, with one source-equivalence class alpha_* chosen to be 12-dominant so D_alpha_*>0 and all other endpoint classes held source-neutral.
- Varied variable: The dimensionless connected cumulant witness beta=-C_N kappa_alpha_* D_alpha_*/M_G, including its finite-difference source interval width and tail budget.
- Held-fixed controls: Same regulated Wilson action and same gauge-invariant Wilson loop normalization., The previously computed H,K Schur-Feshbach data, null vector, M_G, C_N, and fractional incidences b_ij., Reflection symmetry and no boundary counterterm or boundary Hilbert-sector enlargement., Cutoff-uniform tail accounting through a single tau parameter.
- Expected observation: For beta+tau/M_G<1 the finite block is promoted; for beta-tau/M_G>1 the same finite block is demoted by a valid OS determinant falsifier; if the interval straddles one, quarantine remains mathematically forced.
- Transfer certificate needed: A validator-facing same-theory source-derivative certificate: seven heat-kernel source values for log Z_alpha, a fourth-derivative error bound, source-equivalence proof, and a cutoff-uniform T_tail estimate before the intuition may enter proof obligations.

## Next Experiment

Compute a validator-facing connected cumulant witness for the smallest positive-D 12-dominant endpoint source class: seven heat-kernel source values for log Z_alpha, a fourth-derivative interval for kappa_alpha, the signed D_alpha incidence, C_N, M_G, and cutoff-uniform T_tail; then evaluate [I_-,I_+] and either promote, demote by falsifier, or keep quarantine.

# Gauge-Invariant Nontriviality Witness Selection -> finite endpoint R certificate

## Candidate Lemma

Conditional finite Route A lemma: for the H,K plus endpoint box, the Ward-subtracted connected boundary-OPE polarization is bounded by endpoint second moments, yielding a same-theory lower interval for R_{++}^{ren}. If this lower interval exceeds the Schur-Feshbach leakage L_+, then the post-H,K endpoint block is positive in this finite problem. This does not claim YM existence or a mass gap.

## Definitions

- source object: centered flowed Wilson hairpin cumulant R_{++}^{ren}(t,eta,a) in SU(N) lattice Yang-Mills with Wilson action, gradient flow time t, and point-split endpoint boxes.
- target object: finite Route A endpoint-box positivity certificate Q_+^{end}>0 for the post-H,K Schur-Feshbach block.
- controlled interface: Ward-subtracted endpoint sheet-current representation with zero-pairing quotient, cell moments, and interval near/far heat-kernel Hessian bounds.
- same-theory condition: the Wilson cumulant, counterterms, recovery map, and Feshbach matrix entries are computed in one cutoff family and one continuum Schwinger family, without changing observables or normalization.
- bridge/carrier: endpoint sheet current J_+=sum_c q_c sigma_c supported in endpoint cells, with reflection and orientation inherited from the H,K hairpin geometry.
- R term: R_{++}^{ren}=kappa_2(\widehat W_{J_+},\widehat W_{J_+}) after disconnected-product removal and one-hairpin perimeter/cusp subtraction.
- pair baseline: G_{++} is the positive flowed two-curvature cross-pairing of J_+ with itself after color contraction.
- polarization: Xi_{++}^{WS} is the Ward-subtracted connected four-curvature endpoint kernel integrated against four endpoint sheet currents.
- hard gate changed: finite endpoint-box positivity after H,K; continuum existence, OS/Wightman reconstruction, observable density, and Hamiltonian mass gap remain untouched.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with Wilson plaquette action, gradient-flowed gauge field B(t), and fixed finite H,K hairpin geometry.
- Regime: a << sqrt(8t) <= eta << d, where d is the collar separation scale and eta is the endpoint-box diameter.
- Cutoff: all counterterms are the standard one-hairpin perimeter/cusp subtractions used before taking the same cutoff limit.
- Same-theory: R_{++}^{ren}, L_+, G_{++}, and Xi_{++}^{WS} are evaluated in the same regulated Wilson theory and along the same RG/flow window.
- Uniformity: near/far kernel constants and recovery-map errors are bounded uniformly for all endpoint cells in the chosen finite partition.
- Validity: the endpoint current has certified zero monopole and dipole moments after the zero-pairing quotient and recovery map are applied.
- Local: the claim concerns only endpoint boxes and a finite Schur-Feshbach matrix; it is a restricted finite witness, not a continuum spectral theorem.

## Equations

- flowed Wilson endpoint cumulant decomposition: `R_{++}^{ren}=g_t^4 (N^2-1)\bigl(2G_{++}+N\Xi_{++}^{WS}\bigr)+E_6(t,\eta,a)`. Valid when: Valid after gradient flow, disconnected-product removal, one-hairpin cusp subtraction, and truncation with a certified sixth-order remainder.
- Ward-Hessian polarization bound: `|\Xi_{++}^{WS}|\le H_{4,++}^{I,+}(t,\eta,a)\,M_{2,+}^2+\epsilon_{rec}^{I,+}`. Valid when: Valid when Ward identities remove contact terms and the recovered endpoint current has zero monopole and dipole moments.
- computable lower interval: `R_{++}^{I,-}=g_t^4 (N^2-1)\bigl(2G_{++}^{I,-}-N H_{4,++}^{I,+}M_{2,+}^2\bigr)-E_6^{I,+}-g_t^4N(N^2-1)\epsilon_{rec}^{I,+}`. Valid when: Applies on a fixed endpoint-cell partition with outward-rounded intervals for pair, Hessian, recovery, and remainder terms.
- finite endpoint promotion inequality: `R_{++}^{I,-}>L_+\quad\Longrightarrow\quad Q_+^{end}=R_{++}^{ren}-L_+>0`. Valid when: Valid for the finite H,K Schur-Feshbach block when L_+ is the already certified leakage scalar in the same basis.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: centered flowed Wilson hairpin cumulant R_{++}^{ren}(t,eta,a) in SU(N) lattice Yang-Mills with Wilson action, gradient flow time t, and point-split endpoint boxes.; target object: finite Route A endpoint-box positivity certificate Q_+^{end}>0 for the post-H,K Schur-Feshbach block.; Model: four-dimensional SU(N) lattice Yang-Mills with Wilson plaquette action, gradient-flowed gauge field B(t), and fixed finite H,K hairpin geometry..
- Fix SU(N), Wilson plaquette cutoff a, gradient flow time t, endpoint diameter eta, and the previously computed finite H,K plus-channel leakage L_+.
- Represent each thin hairpin by a centered flowed Wilson observable and then by an endpoint sheet current J_+ after disconnected-product, perimeter, and cusp subtraction.
- Expand the second cumulant to the first nontrivial endpoint order: the pair contraction gives color 2(N^2-1)G_{++}; the connected four-curvature sector gives color N(N^2-1)Xi_{++}^{WS}.
- Use Ward identities to remove longitudinal/contact pieces and use the plus-channel endpoint symmetry to cancel monopole and dipole moments of J_+.
- Taylor expand each Ward-subtracted sector kernel around the endpoint-cell centers. The zero and first-order terms vanish, leaving a Hessian remainder bounded by H_{4,++}^{I,+}M_{2,+}^2.
- Split endpoint-cell pairs into near cells, controlled by flowed heat-kernel Hessian suprema at scale t, and far cells, controlled by algebraic decay in separation with interval quadrature.
- Insert the lower interval R_{++}^{I,-} into the finite Schur-Feshbach endpoint scalar Q_+^{end}=R_{++}^{ren}-L_+. If R_{++}^{I,-}>L_+, the finite endpoint box is certified positive.

Blocking gap: The missing proof object is a certified table of Ward-subtracted near/far Hessian constants C_s for the 3g, 4g, counterterm, and endpoint-contact sectors, plus a recovery-map error epsilon_rec that is uniform on a flow-time plateau.

## Falsifiers

- falsifier: the Ward-subtracted connected four-curvature kernel has an uncancelled contact term whose Hessian bound is not finite at the endpoint diagonal.
- falsifier: after recovery from Wilson contours to sheet currents, the plus endpoint current has a nonzero dipole moment producing an O(eta) term instead of the required O(eta^2) remainder.
- falsifier: interval refinement does not shrink H_{4,++}^{I,+} or epsilon_rec, indicating a representation or regulator failure rather than a numerical-width issue.
- falsifier: the flow-time plateau a << sqrt(8t) <= eta is absent, so the same-theory cutoff limit cannot use the computed R_{++}^{I,-}.
- falsifier: R_{++}^{I,-}<=L_+ for all admissible eta/sqrt(8t), which quarantines the endpoint R repair while leaving other Clay gates unchanged.
- falsifier: the one-hairpin cusp subtraction used in R is not the same counterterm family used to define the Wilson observables entering H,K.

## Learning

Conceptual pressure attacked: finite Feshbach positivity needs a same-theory Wilson mediator, while positive pair covariance and gradient-flow renormalization can both be valid and still be erased by the connected four-curvature polarization. Declarative tension: Schur-Feshbach positivity, Wilson cumulant positivity, and same-theory recovery must jointly hold, but raw Wilson contours are fragmented and representation-limited. Compared route: global OS spectral transfer or a non-Gaussian Schwinger family witness is too coarse for this local obstruction; endpoint sheet currents are sharper because Ward subtraction, moment cancellation, heat-kernel Hessians, interval arithmetic, and zero-pairing quotienting become primitive. Efficient representation: encode H,K sheets, endpoint currents, cell moments, sector kernels, counterterms, and recovery errors; preserve gauge, color, reflection, orientation, cutoff, and same-theory invariants; use cumulant expansion, Ward/cusp subtraction, endpoint Taylor remainders, near/far heat-kernel majorants, outward-rounded quadrature, and finite refinement; quotient only certified zero-pairing currents; transfer only through centered flowed Wilson cumulants; demote on any falsifier. Hard gate: finite endpoint-box positivity after H,K. Success promotes one finite Route A gate; failure quarantines this R repair. Clay existence, OS/Wightman axioms, nontrivial continuum limit, observable density, large-field/topology control, and positive Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a validator-facing falsifier probe and proof-search guide.`
- Rationale: The branch has repeated the near/far interval plan; the next information must come from a concrete regulator-preserving stress case for the connected cumulant witness, not from another abstraction restatement.
- Situation seed: On a periodic four-dimensional SU(N) Wilson lattice, take the fixed H,K plus hairpin endpoint box, apply gradient flow at time t, replace hairpins by recovered endpoint sheet currents, and compute the outward-rounded interval for G_{++}, H_{4,++}, epsilon_rec, and R_{++}^{I,-}.
- Varied variable: rho=eta/sqrt(8t), with rho varied over a dyadic grid while the finite H,K geometry and leakage L_+ are fixed.
- Held-fixed controls: Same SU(N) Wilson action, boundary conditions, H,K plus-channel geometry, and Schur-Feshbach basis., Same disconnected-product removal and one-hairpin perimeter/cusp counterterms for every rho., Same zero-pairing quotient policy and recovery map Rec_a., Same renormalized coupling prescription g_t and fixed finite endpoint-cell refinement budget.
- Expected observation: If Ward and plus-moment cancellations are real, H_{4,++}^{I,+}M_{2,+}^2 scales like O(rho^2) relative to the positive pair baseline over a plateau, so R_{++}^{I,-}-L_+ becomes positive for at least one rho. If not, the branch gets a concrete demotion.
- Transfer certificate needed: A cutoff-uniform same-theory recovery certificate showing that the lattice-flow cumulant interval converges to the same continuum Schwinger family used for the Wilson observables and that no OS spectral-transfer or mass-gap claim is inferred from this finite test.

## Next Experiment

Proof search: build the validator-facing interval table for the same-theory nontriviality witness carrier at the finite endpoint level: fixed H,K plus sheet current, dyadic rho, flowed Wilson connected cumulant witness R_{++}^{ren}, sectorwise Ward-Hessian constants, recovery errors, and the sign of R_{++}^{I,-}-L_+.

# Raw plaquette K4 stress screen for the post-H,K endpoint form

## Candidate Lemma

Two-sparse raw-K4 stress screen. In a fixed heat-kernel cutoff, let M_sigma=R_sigma-S_HK,sigma be the Schur-corrected endpoint matrix on the finite collar/hairpin Wilson basis. If an interval upper Rayleigh bound U_pq(eta)<0 for some endpoint pair p,q and scalar eta, then the worked H,K endpoint route has a valid finite falsifier. If instead Delta_raw=lambda_min(L_sigma)>0 for the interval lower matrix, the finite endpoint box is certified positive. Neither conclusion implies continuum YM existence or a Hamiltonian mass gap.

## Definitions

- source object: finite-volume heat-kernel regulated SU(N) Wilson measure mu_{a,sigma,g,V} with raw oriented plaquette curvature coordinates X_{sigma,p}^a and exact Wilson trace identities.
- target object: finite Schur-corrected endpoint quadratic form M_sigma=R_sigma-S_{HK,sigma} on the selected Wilson collar/hairpin endpoint basis, not the OS Hilbert space or continuum Hamiltonian.
- controlled interface: connected cumulant witness R_{ij,sigma}=cum_2(:Q_i^2:,:Q_j^2:) recovered from raw plaquette contractions and inserted into the Schur-Feshbach endpoint test.
- same-theory condition: R_sigma, K4_sigma, E_OPE,sigma, and S_HK,sigma use the same lattice spacing, heat-kernel regulator, coupling, finite box, reflection convention, Wilson basis, and normalization.
- Carrier critique: scalar R is representation-limited, OS observable density is too strong and circular for this local gate, shell A012 is quarantined, and raw plaquette enumeration is fragmented but valid.
- Efficient representation: encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, and H,K Schur blocks; preserve gauge invariance, reflection support, Gaussian/kappa4 separation, endpoint compression, and same-theory normalization; primitive operations are cumulant contraction, interval summation, Rayleigh/stress bounds, exact quotient audit, and Schur subtraction; equivalence is only by exact Wilson identities; locality budget is the finite endpoint box.

## Assumptions

- Model: finite-volume lattice SU(N) Yang-Mills with heat-kernel plaquette action and reflection-compatible endpoint box; no continuum limit is taken in this lemma.
- Cutoff: lattice spacing a>0, smoothing radius sigma>=2a, renormalized coupling g_R(a,sigma), and finite volume V are fixed throughout the calculation.
- Same-theory: the plaquette cumulants, Wilson OPE coefficients, H,K Schur blocks, and endpoint basis are computed from the same regulated measure, not imported from another regulator or effective model.
- Validity: interval enclosures for K4_sigma and E_OPE,sigma are outward-rounded and remain valid after every exact Wilson quotient used in the compression.
- Local: the endpoint supports and hairpin blocks lie in the finite reflected collar so that the Schur-Feshbach theorem applies to the same Gram matrix truncation.
- Constraint: this is a finite Route A endpoint theorem; OS/Wightman reconstruction, nontrivial continuum limit, observable density, and physical-unit spectral transfer remain untouched.

## Equations

- heat-kernel plaquette curvature coordinate: `X_{\sigma,p}^{a}=a^{-2}\sum_{q}K_{\sigma}(p,q)\,\operatorname{Tr}\big(T^{a}(U_{q}-U_{q}^{-1})\big)`. Valid when: Valid when the heat-kernel plaquette fields are defined at fixed lattice spacing a and the smoothing radius sigma remains inside the finite endpoint box.
- transported sheet flux: `Q_i=\sum_{p\in S_i}w_{i,p}\,\tau_{i,p}^{ab}\,X_{\sigma,p}^{b}`. Valid when: Valid when each sheet S_i has fixed plaquette weights and adjoint transporters chosen from the same Wilson endpoint observable.
- raw connected boundary polarization: `R_{ij,\sigma}=\operatorname{cum}_{2}\big(:Q_i^{2}:,:Q_j^{2}:\big)`. Valid when: Applies after vacuum subtraction and perimeter normalization in the same cutoff measure so disconnected Wilson factors cancel before Schur subtraction.
- Gaussian color square: `G_{ij,\sigma}=\alpha_N g_R^{4}\,(C_{\sigma}\odot C_{\sigma})_{ij},\qquad \alpha_N=\frac{N^{2}-1}{8N^{2}}`. Valid when: Requires the reflected heat-kernel two-curvature contraction and SU(N) trace normalization used in the same endpoint Wilson basis.
- raw connected four-curvature cumulant: `(K4_{\sigma})_{ij}=\sum_{p,q\in S_i}\sum_{r,s\in S_j}w_{i,p}w_{i,q}w_{j,r}w_{j,s}\,\tau^{abcd}_{pqrs}\,\operatorname{cum}_{4}(X_p^a,X_q^b,X_r^c,X_s^d)`. Valid when: Valid for finite plaquette sheets after exact transporter insertion and before any non-exact shell compression or asymptotic cluster replacement.
- Schur-corrected endpoint matrix: `M_{\sigma}=G_{\sigma}+\frac{g_R^{4}}{16N^{2}}K4_{\sigma}+E_{OPE,\sigma}-S_{HK,\sigma}`. Valid when: Applies after the H,K hairpin variables are eliminated by the finite Schur-Feshbach map in the same Wilson Gram truncation.
- two-sparse falsifier upper bound: `U_{pq}(\eta)=(e_p-\eta e_q)^{*}\Big(G_{\sigma}+\frac{g_R^{4}}{16N^{2}}K4^{+}_{\sigma}+E^{+}_{OPE,\sigma}-S_{HK,\sigma}\Big)(e_p-\eta e_q)`. Valid when: Valid when K4_sigma and E_OPE,sigma are interval-bounded above as quadratic forms on the chosen two-dimensional endpoint subspace.
- raw promotion lower matrix: `L_{\sigma}=G_{\sigma}-S_{HK,\sigma}-E^{abs}_{OPE,\sigma}-\frac{g_R^{4}}{16N^{2}}B^{-}_{4,\sigma},\qquad \Delta_{raw}=\lambda_{\min}(L_{\sigma})`. Valid when: Valid when B4_minus dominates the negative part of K4_sigma on the full finite endpoint basis after exact quotient auditing.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: finite-volume heat-kernel regulated SU(N) Wilson measure mu_{a,sigma,g,V} with raw oriented plaquette curvature coordinates X_{sigma,p}^a and exact Wilson trace identities.; target object: finite Schur-corrected endpoint quadratic form M_sigma=R_sigma-S_{HK,sigma} on the selected Wilson collar/hairpin endpoint basis, not the OS Hilbert space or continuum Hamiltonian.; Model: finite-volume lattice SU(N) Yang-Mills with heat-kernel plaquette action and reflection-compatible endpoint box; no continuum limit is taken in this lemma..
- Conceptual pressure attacked: replace symbolic endpoint polarization by a same-regulator connected cumulant witness that can either certify or falsify the Schur-corrected endpoint form.
- Fix heat-kernel lattice SU(N) YM at (a,sigma,g_R,V) and choose the finite H,K Wilson collar/hairpin endpoint basis; this freezes the Clay claim level to a finite Route A calculation.
- Represent each endpoint Wilson OPE carrier by transported plaquette fluxes Q_i=sum w tau X_sigma and expand the boundary polarization as R_ij=cum_2(:Q_i^2:,:Q_j^2:).
- Use vacuum/perimeter normal ordering to cancel one-point and disconnected Wilson factors; crossed two-curvature contractions give the PSD Gaussian matrix G_sigma with color factor alpha_N=(N^2-1)/(8N^2).
- Place all non-Gaussian four-curvature input in the raw interval matrix K4_sigma and all truncation leakage in E_OPE,sigma; subtract S_HK,sigma from the same finite Schur-Feshbach calculation.
- For promotion, compute a lower matrix L_sigma and prove Delta_raw=lambda_min(L_sigma)>0. For demotion, search two-sparse x=e_p-eta e_q and prove the interval upper Rayleigh value U_pq(eta)<0.
- Use exact quotient admissibility only after verifying Pi recovers raw Rayleigh intervals; otherwise return to raw plaquette enumeration.

Blocking gap: The missing mediator is now numerical-rigorous, not conceptual: no same-regulator interval enclosure for the decisive K4 plaquette cumulants has been supplied, especially for the most negative two-sparse directions after Schur subtraction.

## Falsifiers

- A valid falsifier is a recovered raw vector x with x^*(G+g_R^4 K4^+/(16N^2)+E_OPE^+-S_HK)x<0 in the same cutoff theory.
- If K4 intervals are so wide that both Delta_raw and all stress upper bounds are inconclusive, the raw endpoint route is quarantined rather than promoted.
- If exact quotient auditing fails, any quotient-compressed certificate is invalid and must be demoted to raw plaquette enumeration.
- If the OPE remainder interval exceeds the Gaussian margin after Schur subtraction, the worked H,K endpoint positivity gate fails without affecting Clay-level existence or mass-gap gates.
- If K4 is imported from a different regulator, coupling, volume, or Wilson basis, the same-theory condition fails and the branch must backtrack.

## Learning

Declarative tension: finite Wilson/OPE coefficients, connected kappa4 negativity, OPE error, and H,K Schur subtraction must jointly control one endpoint quadratic form in a single cutoff theory, while Clay-level continuum and spectral claims must remain quarantined. Carrier revision: scalar R is too weak, OS observable density is too strong and circular here, shell A012 is convenient but quarantined, and raw plaquette enumeration is fragmented yet valid. Compared with full matrix Delta search, the two-sparse stress route is a sharper negative tactic because it can demote the H,K endpoint route from a small number of same-regulator K4 intervals. Efficient representation requirements are now explicit: encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, interval cumulants, OPE intervals, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/kappa4 separation, endpoint compression, and same-theory normalization; support cumulant contraction, interval summation, exact quotient audit, Rayleigh stress search, and Schur subtraction; transfer only through Delta_raw or a recovered stress falsifier. Hard gate: Delta_raw>0 promotes only finite endpoint-box positivity, while U_pq(eta)<0 kills this H,K collar/hairpin route. Conceptual value signal: the result is route-changing at finite scope because it turns the connected boundary-OPE polarization into a validator-facing connected cumulant witness with color, geometry, non-Gaussian K4, OPE, and Schur data in one valid inequality.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide, not as evidence for continuum spectral transfer.`
- Rationale: The branch has quarantined symbolic shells; the next valuable move is to see whether actual raw K4 intervals can beat or kill the finite Schur-corrected endpoint margin.
- Situation seed: Finite SU(2) heat-kernel lattice endpoint box containing two collar plaquette sheets and the already fixed H,K hairpin block; compute the connected cumulant witness R_ij=cum_2(:Q_i^2:,:Q_j^2:) from raw plaquette variables.
- Varied variable: rho=sigma/a, the heat-kernel smoothing radius measured in lattice units.
- Held-fixed controls: The same H,K Wilson collar/hairpin endpoint geometry and endpoint basis., The same finite volume, boundary reflection convention, heat-kernel action, and coupling normalization., Exact Wilson quotient policy; no shell A012 compression is allowed., Clay-level non-claims: no continuum limit, no OS spectral transfer, and no mass-gap conclusion.
- Expected observation: As rho varies, the Gaussian Hadamard square should remain PSD while the upper interval for the most negative two-sparse K4 direction either stays below the Schur-adjusted margin, yielding a stress falsifier, or becomes dominated by the Gaussian margin, yielding a candidate Delta_raw certificate.
- Transfer certificate needed: A rigorous same-regulator interval enclosure for the relevant four-plaquette connected cumulants, exact recovery of quotient vectors to raw plaquette coordinates, and an outward-rounded Rayleigh bound before the intuition may enter proof obligations.

## Next Experiment

Proof search: choose the largest Schur-energy endpoint pair (p,q), compute same-regulator four-plaquette connected cumulant intervals entering K4^+_{pp}, K4^+_{pq}, K4^+_{qq}, minimize U_pq(eta), and either output a recovered stress falsifier or certify that this pair cannot demote the endpoint route.

