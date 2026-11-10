# cycle-0276

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: endpoint-source interval handoff

## Candidate Lemma

For the known three-hairpin H,K block, the post-H,K endpoint contribution has a valid scalar interval certificate: only endpoint boxes whose binary footprint is 12-only can use negative compact-group kappa_4 to demote the finite OS gate; all boxes touching 13 or 23 are protective or cancel, up to the certified tail.

## Definitions

- source object: heat-kernel plaquette-sheet regulated SU(N) Wilson three-hairpin block with known H,K data, endpoint boxes B_v, source derivatives of log Z_v, and cutoff a,L kept finite.
- target object: finite post-H,K Schur-Feshbach scalar gate I_gate for the null vector z=(1,1,-2), not continuum OS positivity, Wightman reconstruction, or a Hamiltonian mass gap.
- controlled interface: a representation morphism from same-theory connected endpoint four-flux cumulant intervals and binary footprint incidences to a certified interval [I_-,I_+] for the scalar finite OS gate.
- same-theory condition: all source derivatives use the original heat-kernel Wilson action and locked gauge-invariant Wilson normalization; no boundary counterterm, gauge-fixed substitute, or observable-algebra change is allowed.
- carrier object: C_ep=(V_partial,S_v,[beta_v^-,beta_v^+],C_N,M_G,tau), where S_v records which of 12,13,23 occupy endpoint box v.
- recovery map: R_{ij}^{end} is recovered by differentiating the same regulated Wilson generating functional in the plaquette-sheet source direction for the reflected pair ij.
- invariants preserved: gauge invariance, reflection symmetry, Wilson normalization, the H,K block, the null-channel contractions, and the endpoint tail budget.
- conceptual pressure: endpoint collapse must be sign-certified in the same Wilson theory without confusing negative kappa_4 with an OS falsifier by itself.

## Assumptions

- Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action, fundamental Wilson loops, and reflection across t=0.
- Regime: finite collar/hairpin block after H,K are fixed; endpoint boxes are smaller than the collar scale but larger than the plaquette scale for the finite regulator calculation.
- Cutoff: all formulae are at fixed a,L unless the beta_v intervals and tau tail are separately proved uniform in cutoff and volume.
- Same-theory: the endpoint source Z_v(s) is inserted into the original Wilson action; no boundary renormalization is absorbed into the observable definitions.
- Local: endpoint boxes are disjoint after the chosen partition; overlaps not assigned to one binary footprint are charged to T_tail.
- Uniformity: large-field and topological sectors are support-only here and must be included in tau before any continuum statement is attempted.
- Validity: singlet endpoint projection reduces the local connected four-flux cumulant to signed scalar beta_v intervals, with angular and commutator remainders included in tau.
- Constraint: the lemma changes only the finite post-H,K reflected-Wilson OS transfer gate; Clay-level existence, OS/Wightman reconstruction for all observables, nontriviality, and mass gap remain untouched.

## Equations

- endpoint_connected_R_decomposition: `2R_{12}^{end}-4R_{13}^{end}-4R_{23}^{end}=C_N\sum_{v\in V_\partial}\kappa_{4,v}^{sing}D_v+T_{tail}`. Valid when: Valid when heat-kernel endpoint boxes are disjoint after collar collapse and the singlet endpoint projection plus null-incidence cancellation assumptions hold.
- binary_endpoint_incidence: `D_v=2\mathbf 1_{12}(v)-4\mathbf 1_{13}(v)-4\mathbf 1_{23}(v),\quad D_v(S)\in\{0,2,-4,-2,-8,-6\}`. Valid when: Valid when each endpoint box records only binary membership in the three reflected hairpin pair footprints.
- compact_group_sign_interval: `\kappa_{4,v}^{sing}\in[-\beta_v^+,-\beta_v^-],\quad 0\le \beta_v^-\le \beta_v^+`. Valid when: Applies after the heat-kernel endpoint source derivative has certified a nonpositive connected fourth cumulant interval for the same Wilson source.
- clipped_gate_interval: `I_-=M_G-C_N\sum_{D_v>0}\beta_v^+D_v+C_N\sum_{D_v<0}\beta_v^-(-D_v)-\tau,\quad I_+=M_G-C_N\sum_{D_v>0}\beta_v^-D_v+C_N\sum_{D_v<0}\beta_v^+(-D_v)+\tau`. Valid when: Valid when the endpoint cumulant intervals, positive color factor C_N, Gaussian margin M_G, and symmetric tail bound |T_tail|<=tau are all certified in the same regulator.
- finite_promotion_or_falsifier: `I_->0\Rightarrow \text{finite block promoted},\qquad I_+<0\Rightarrow \text{finite same-theory falsifier}`. Valid when: Valid only for the fixed three-hairpin post-H,K Schur-Feshbach scalar and not for continuum OS reconstruction or the Clay mass-gap theorem.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel plaquette-sheet regulated SU(N) Wilson three-hairpin block with known H,K data, endpoint boxes B_v, source derivatives of log Z_v, and cutoff a,L kept finite.; target object: finite post-H,K Schur-Feshbach scalar gate I_gate for the null vector z=(1,1,-2), not continuum OS positivity, Wightman reconstruction, or a Hamiltonian mass gap.; Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action, fundamental Wilson loops, and reflection across t=0..
- Freeze the Clay target boundary: this cycle proves only a finite regulated Wilson endpoint interval; it does not construct continuum Schwinger functions, OS/Wightman fields, nontriviality, or a Hamiltonian mass gap.
- Start from the known post-H,K scalar gate for the first three-hairpin null channel and isolate the positive Gaussian margin M_G from the endpoint connected R contribution.
- Use the heat-kernel plaquette-sheet regulator and define R_{ij}^{end} by the singlet connected fourth source derivative of log Z_v in the reflected Wilson pair ij endpoint direction.
- Apply the two cancellations already established for this finite block: the connected log removes disconnected Wick-square pieces from kappa_4, and the straight C_A f f contact cancels under the null incidence identity.
- Partition the remaining boundary support into endpoint boxes B_v. Boxes with unresolved overlap, large-field leakage, or topology-changing plaquette sheets are not forced into the local term; they are charged to T_tail.
- Under the local singlet projection, replace each endpoint box by a scalar nonpositive cumulant kappa_{4,v}^{sing}=-beta_v and a binary incidence D_v=2 1_12-4 1_13-4 1_23.
- Compute the incidence table: empty gives 0; 12-only gives 2; 13-only and 23-only give -4; 12+13 and 12+23 give -2; 13+23 gives -8; all three give -6. Hence only 12-only boxes are dangerous.
- Propagate certified beta_v intervals and the tail bound through interval arithmetic to obtain [I_-,I_+]. Promotion is I_->0; a finite same-theory falsifier is I_+<0.
- Extract beta_v intervals by the seven-point fourth-derivative stencil on f_v(s)=log Z_v(sY_v), with the 7h^4 M8_v/240 error budget.

Blocking gap: Actual endpoint-box source data, eighth-derivative bounds, and a cutoff-controlled tail estimate are still missing. The binary singlet projection must also be verified for the specific geometric endpoint boxes rather than assumed.

## Falsifiers

- falsifier: a certified interval I_+<0 from many 12-only endpoint boxes gives a finite same-theory post-H,K OS obstruction.
- falsifier: the endpoint source derivative requires a boundary counterterm or changed Wilson-loop normalization, breaking the same-theory condition.
- falsifier: M8_v or T_tail diverges with cutoff so the finite interval cannot be made valid in the claimed regulator regime.
- falsifier: an endpoint box touching 13 or 23 nevertheless contributes with D_v>0 after the actual color/geometric contraction, invalidating the binary incidence carrier.
- Stress case: all endpoint boxes are 12-only, beta_v are near their upper intervals, and protective P is zero; then the promotion inequality can fail sharply.
- Failure case: topological sectors or large-field excursions produce nonlocal endpoint correlations not chargeable to tau, so locality budget is representation-limited.

## Learning

Cycle 276 makes the endpoint carrier operational: the post-H,K R/kappa_4 term is a clipped same-theory interval, not a symbolic parameter and not a raw negative-spectrum alarm. The declarative tension is finite collar OS positivity plus fixed gauge-invariant Wilson observables plus singular endpoint OPE; the missing mediator is the regulated endpoint source carrier C_ep. The current raw R carrier is representation-limited because it forgets incidence signs; a global Schur-preimage route is too coarse after H,K, while the endpoint source route is local, computable, and has a valid falsifier. Efficient representation requirements are explicit: encode endpoint boxes, seven-point source stencils, beta intervals, S_v incidences, C_N, M_G, and tau; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff bookkeeping, and same-theory observables; use source differentiation, interval arithmetic, clipping, incidence contraction, and tail addition; identify equivalent carriers only by equal regulated source derivatives; keep locality cost finite through T_tail; transfer only [I_-,I_+] to the finite OS gate. Hard gate changed: the finite post-H,K reflected-Wilson OS transfer gate can now be promoted or falsified by actual endpoint data. Larger Clay gates remain untouched and explicitly non-claimed. Conceptual value signal: sharpness and route change; negative compact-group kappa_4 is not the falsifier, certified 12-only endpoint dominance plus uncontrolled tail is.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the finite post-H,K endpoint interval.`
- Rationale: The branch no longer needs another abstract OS/Wilson restatement. The decisive local unknown is whether actual heat-kernel endpoint source data can make 12-only dominance exceed the Gaussian Schur-Feshbach margin while preserving the same Wilson theory.
- Situation seed: A finite SU(N) heat-kernel plaquette-sheet model containing the first three reflected Wilson hairpins, with endpoint boxes classified by S_v subset {12,13,23} and source derivatives f_v(s)=log Z_v(sY_v) evaluated by the seven-point stencil.
- Varied variable: Endpoint overlap resolution eta, equivalently the fraction r of total certified beta_v mass assigned to 12-only boxes rather than boxes touching 13 or 23.
- Held-fixed controls: Same heat-kernel Wilson action and gauge-invariant Wilson observables; no boundary counterterm or gauge-fixed substitute., Known H,K three-hairpin data, null vector z=(1,1,-2), positive color factor C_N, and Gaussian margin M_G., Reflection symmetry, Wilson normalization, and the rule that unresolved overlap or large-field/topological leakage is charged to T_tail., Finite regulator a,L during the experiment; continuum claims remain forbidden without uniform estimates.
- Expected observation: As r increases, the lower gate bound decreases linearly like M_G-2C_NB_12^+-tau, while endpoint boxes touching 13 or 23 raise the lower bound. The experiment should identify a critical dominance ratio r_* beyond which a finite falsifier becomes possible.
- Transfer certificate needed: Before intuition affects proof obligations, one needs certified source intervals for beta_v, a uniform M8_v stencil error, a valid binary incidence proof for the actual endpoint geometry, and a tail bound tau that includes large-field and topological sectors without changing the theory.

## Next Experiment

Compute the endpoint incidence/source table for the actual three-hairpin geometry: enumerate endpoint boxes, label S_v, evaluate or analytically bound the seven heat-kernel source values for each box type, form beta_v intervals, set tau for unresolved overlap and large-field/topology tails, then output [I_-,I_+] for the finite OS gate.

# Post-H,K endpoint-box R/kappa4 Hessian enclosure

## Candidate Lemma

Under finite flowed Wilson regularization, Ward/cusp and plus-moment cancellations give a valid lower interval for R_{++}/kappa_4. If it beats L_+, finite endpoint-box positivity is promoted; otherwise the R repair is falsified.

## Definitions

- source object: finite-cutoff SU(N) Yang-Mills Wilson ensemble with gradient-flowed thin H,K hairpin sheets and endpoint currents in boxes B_eta.
- target object: finite Schur-Feshbach plus-channel endpoint-box lower bound for the post-H,K R/kappa_4 term against leakage L_+.
- controlled interface: centered renormalized flowed Wilson covariance R_{++}^{ren} decomposed into positive pair baseline plus Ward-subtracted connected four-curvature polarization.
- same-theory condition: same bare action, flow time window, Wilson observable algebra, counterterms, and H,K recovery maps are used in source cumulants and target finite matrix.
- carrier: sheet-current morphism Phi maps each hairpin sheet to signed endpoint current J with gauge, color, orientation, and reflection labels retained.
- error budget: finite certificate records H_eta, M2(J_+), E6, cutoff drift Delta_a, and flow drift Delta_t; only certified intervals may enter promotion.

## Assumptions

- Model: pure SU(N) Euclidean YM with Wilson or heat-kernel lattice action; observables are gauge-invariant traced flowed Wilson hairpins.
- Cutoff: finite volume and a>0 first; flow time t obeys a^2 << t << eta^2, with uniform a,V limits left as frontier obligations.
- Same-theory: no measure change or auxiliary advice; flow, centering, cusp counterterm, and color normalization match the H,K extraction.
- Validity: Ward and cusp subtractions leave zero endpoint monopole and dipole for J_+; otherwise the Hessian reduction is invalid.
- Local: endpoint boxes are disjoint from nonlocal sheet intersections; eta is smaller than hairpin separation and curvature scale.
- Constraint: connected six-curvature and higher terms are enclosed by E6 in the same interval certificate.

## Equations

- R decomposition: `\kappa_4^{-1}R_{++}^{ren}=2(N^2-1)\mathcal G_{++}+N(N^2-1)C_{4,++}^{WS}+E_6`. Valid when: Valid when the flowed hairpin covariance is expanded in the same finite Wilson ensemble with disconnected products and one-hairpin perimeter/cusp counterterms subtracted.
- Ward-moment Hessian bound: `|C_{4,++}^{WS}|\le H_\eta M_2(J_+)^2,\quad M_0(J_+)=M_1(J_+)=0`. Valid when: Applies after Ward subtraction and plus-channel endpoint-current cancellation make the constant and linear Taylor terms vanish inside each endpoint box.
- finite promotion inequality: `\underline R_{++}:=\kappa_4\{2(N^2-1)\mathcal G_{++}-N(N^2-1)H_\eta M_2(J_+)^2-|E_6|\}>L_+`. Valid when: Requires the same-theory H,K matrices, certified leakage L_+, and interval bounds for H_eta, M2, G++, and E6 at fixed regulator.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: finite-cutoff SU(N) Yang-Mills Wilson ensemble with gradient-flowed thin H,K hairpin sheets and endpoint currents in boxes B_eta.; target object: finite Schur-Feshbach plus-channel endpoint-box lower bound for the post-H,K R/kappa_4 term against leakage L_+.; Model: pure SU(N) Euclidean YM with Wilson or heat-kernel lattice action; observables are gauge-invariant traced flowed Wilson hairpins..
- Expand two centered flowed hairpins to the kappa_4 endpoint sector; subtract the disconnected product and one-hairpin perimeter/cusp terms in the original Wilson measure.
- Represent the connected four-curvature boundary-OPE term as endpoint-current pairing with Ward-subtracted kernel K_4^{WS}; pair baseline keeps color factor 2(N^2-1).
- Use plus-channel monopole and dipole cancellation. Taylor expand K_4^{WS} inside B_eta; constant and linear pieces vanish, leaving a Hessian bound H_eta M2(J_+)^2.
- Combine the lower interval with Schur-Feshbach leakage L_+. Success promotes finite endpoint-box positivity; failure quarantines this R repair without touching Clay gates.

Blocking gap: Need a certified C^2 interval for K_4^{WS} and E6 in a flow window, including large-field and topological summability across cutoff refinement.

## Falsifiers

- Ward/cusp subtraction leaves a residual monopole, dipole, or cusp logarithm, so the Hessian estimate is not valid.
- The certified lower interval satisfies underline R_{++} <= L_+, demoting endpoint-box positivity after H,K.
- Flow or cutoff plateaus drift beyond the error budget, breaking the same-theory transfer certificate.
- Large-field or topological sectors make K_4^{WS} non-summable or not C^2 on endpoint boxes.

## Learning

Conceptual pressure: finite Feshbach positivity needs a same-theory endpoint mediator. Declarative tension: pair covariance and flow renormalization are valid but C4 can erase them. Endpoint currents beat raw contours because Ward moments and interval Hessians become primitive; success or failure changes only finite endpoint-box positivity.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and interval-calibration experiment.`
- Rationale: The branch has H,K leakage but lacks a valid sign/size certificate for the same-theory endpoint mediator R_{++}; another abstract OS restatement would loop.
- Situation seed: Finite-volume SU(N) lattice YM with gradient-flowed plus-channel H,K hairpin endpoint boxes; evaluate the Ward-subtracted connected four-plaquette sheet cumulant by heat-kernel interval cells.
- Varied variable: Endpoint box radius eta, with a^2 << t << eta^2 and fixed hairpin separation d.
- Held-fixed controls: Same Wilson action, gauge group, color trace normalization, and gradient-flow definition., Same H,K sheet geometry, plus-channel endpoint-current normalization, and recovery maps., Same disconnected-product removal, perimeter/cusp subtraction, and finite Schur-Feshbach leakage L_+.
- Expected observation: After moment cancellation, the connected polarization interval scales like H_eta M2^2 while the positive pair baseline stays stable; either underline R_{++}>L_+ or a falsifier appears.
- Transfer certificate needed: Certified interval bounds uniform in a,V over a flow window, plus large-field/topological summability and inclusion of the flowed Wilson observable in the same OS algebra.

## Next Experiment

Build the finite endpoint-box interval table for G_{++}, H_eta, M2(J_+), and E6 under gradient flow; test underline R_{++}>L_+ and record the first falsifier if it fails.

# Post-H,K endpoint-box kappa4 shell interval certificate

## Candidate Lemma

For fixed heat-kernel SU(N) cutoff data and known H,K, a certified shell row-sum bound on the compressed connected four-curvature cumulant gives a finite valid endpoint-box positivity test after Schur-Feshbach subtraction.

## Definitions

- source object: heat-kernel regulated SU(N) Wilson endpoint-box cumulants for reflected plaquette sheets at cutoff a, volume L, smearing sigma, and coupling g_R.
- target object: finite Schur-corrected endpoint quadratic form on the P collar subspace; it is not OS reconstruction, continuum existence, or a Hamiltonian mass-gap claim.
- controlled interface: sheet-kernel hypergraph recovery map Rec_sigma sends sheets, weights, transporters, color tensors, shells, OPE errors, and H,K Schur data to C_sigma,K4_sigma,E_OPE,S_HK.
- same-theory condition: identical cutoff, volume, heat-kernel time, coupling, Wilson basis, reflection support, and H,K data are used in every term of R_sigma and S_HK.
- bridge observable: R_sigma is the connected boundary-OPE polarization of two reflected Wilson endpoint sheets; vacuum/perimeter disconnected factors are cancelled before compression.
- carrier audit: scalar R is too weak, OS density is too strong and circular, and raw plaquette enumeration is fragmented; the hypergraph keeps color, geometry, locality, transport, and cancellations.
- efficient representation: encode sheets, colors, shells, multiplicities, OPE budgets, and Schur blocks; preserve gauge trace, reflection support, Gaussian/kappa4 split; quotient only Wilson-invariant symmetries.

## Assumptions

- Model: finite heat-kernel lattice/cutoff SU(N) Yang-Mills with gauge-invariant Wilson loops and transported curvature insertions only.
- Regime: fixed endpoint box and finite sheet family with sigma/a^2 bounded below; no volume- or cutoff-uniform basin is asserted.
- Same-theory: the Wilson contraction, kappa4 cumulant, OPE remainder, and Schur hairpin energy use the same regulator and normalization.
- Validity: M4_sigma^- is certified by a shell row-sum or operator-norm interval bound for the actual compressed K4_sigma matrix.
- Local: large-field and topological effects are quarantined inside K4_sigma and E_OPE budgets; RG summability is not claimed.
- Constraint: success changes only the finite Route A endpoint-box positivity gate; OS/Wightman axioms, continuum Schwinger functions, and spectral transfer remain untouched.

## Equations

- connected-kappa4-entry: `(K_{4,\sigma})_{uv}=\int_{S_u^2\times S_v^2} w_u w_v\,\mathcal T_{abmn}\,\langle F^aF^bF^mF^n\rangle_{c,\sigma}`. Valid when: Valid when sheets u,v are transported to the common collar frame in the finite heat-kernel cutoff and disconnected Wilson factors have been subtracted.
- R-decomposition: `R_\sigma=\alpha_N g_R^4(C_\sigma\circ C_\sigma)+\frac{g_R^4}{16N^2}K_{4,\sigma}+E_{\mathrm{OPE},\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after same-regulator boundary OPE normalization, SU(N) trace contraction, and vacuum/perimeter cancellation in the fixed Wilson endpoint basis.
- endpoint-certificate: `\Delta_\sigma:=\lambda_{\min}(\alpha_N g_R^4(C_\sigma\circ C_\sigma))-\frac{g_R^4}{16N^2}M_{4,\sigma}^- -e_{\mathrm{OPE},\sigma}-s_{HK,\sigma}\ge0\Rightarrow P(R_\sigma-S_{HK,\sigma})P\succeq0`. Valid when: Requires M4_sigma^- to bound the negative spectrum of K4_sigma and e_OPE,s_HK to bound the same-basis OPE and Schur errors.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: heat-kernel regulated SU(N) Wilson endpoint-box cumulants for reflected plaquette sheets at cutoff a, volume L, smearing sigma, and coupling g_R.; target object: finite Schur-corrected endpoint quadratic form on the P collar subspace; it is not OS reconstruction, continuum existence, or a Hamiltonian mass-gap claim.; Model: finite heat-kernel lattice/cutoff SU(N) Yang-Mills with gauge-invariant Wilson loops and transported curvature insertions only..
- Expand the two reflected endpoint Wilson observables by the heat-kernel boundary OPE and subtract vacuum/perimeter disconnected factors before compression to P.
- Contract the Gaussian two-curvature pieces with SU(N) trace identities; Schur product positivity makes alpha_N g_R^4(C_sigma o C_sigma) positive semidefinite.
- Represent the connected four-curvature remainder as K4_sigma on the sheet-kernel hypergraph and bound its negative spectrum by certified shell row sums or operator intervals.
- Subtract the known H,K Schur energy and OPE norm; Delta_sigma>=0 proves finite endpoint positivity, while Delta_sigma<0 is a route-local falsifier.

Blocking gap: The first actual shell entries of K4_sigma and the same-regulator OPE interval are not yet computed for the selected H,K endpoint geometry.

## Falsifiers

- A direct K4_sigma interval has negative spectral size exceeding the Gaussian margin after the 1/(16N^2) color factor.
- The Wilson-invariant quotient changes a transported color sign or multiplicity, so Rec_sigma is not representation-invariant.
- Large-field or topological sectors make E_OPE nonlocal in the endpoint box, invalidating the finite shell budget.
- The exact H,K Schur block yields s_HK larger than the positive Gaussian endpoint margin.

## Learning

Conceptual pressure: mediate actual connected Wilson cumulants to Schur-corrected positivity without inflating to Clay. The valid value signal is sharp: Delta_sigma unifies Gaussian color square, kappa4 negativity, OPE error, and H,K energy into one finite falsifier-ready interval.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide.`
- Rationale: The branch needs one concrete same-regulator interval for K4_sigma; more abstraction would loop around Delta_sigma without testing the actual connected Wilson polarization.
- Situation seed: Heat-kernel SU(2) first endpoint box: two reflected rectangular plaquette sheets sharing a collar; enumerate first shell transported four-curvature cumulants defining K4_sigma.
- Varied variable: rho=sigma/a^2, the heat-kernel smearing-to-lattice scale ratio.
- Held-fixed controls: Same finite volume, cutoff, coupling g_R, Wilson endpoint basis, and reflected support., Same H,K Schur blocks, vacuum/perimeter cancellation rule, color normalization, and Wilson trace quotient policy.
- Expected observation: As rho varies, the Gaussian PSD margin should remain stable while the K4 row-sum interval either stays below the margin or produces a negative Delta_sigma falsifier.
- Transfer certificate needed: A same-regulator interval-arithmetic table for all first-shell K4 entries, OPE remainders, quotient invariance, and S_HK norm before any intuition affects proof obligations.

## Next Experiment

Build the first-shell heat-kernel SU(2) endpoint table: enumerate sheet pairs u,v, compute color tensor T_abmn, record geometric weights, bound K4_sigma row sums over rho, then evaluate Delta_sigma.

