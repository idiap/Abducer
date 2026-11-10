# cycle-0288

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint-source interval gate for the post-H,K Wilson hairpin term

## Candidate Lemma

Fractional endpoint dominance interval theorem: after the already-computed H,K Schur-Feshbach cancellations, the remaining connected endpoint-OPE polarization for the three-hairpin finite block is promoted by a scalar interval I_gate; negative endpoint kappa_4 is dangerous only on boxes with certified positive 12-dominance D_v>0, while boxes satisfying the half-overlap shield D_v<=0 are protective or ignorable for lower bounds.

## Definitions

- source object: finite-volume SU(N) heat-kernel plaquette-sheet Yang-Mills at lattice spacing a, collar epsilon, locked reflected Wilson hairpins C1,C2,C3, and Schur-Feshbach null vector z=(1,1,-2).
- target object: the scalar finite post-H,K reflected-Wilson OS transfer gate I_gate=M_G+R_end+T_tail for this one Wilson block, not a continuum theory and not a mass-gap statement.
- controlled interface: the endpoint source carrier C_ep records endpoint boxes v, same-theory source derivatives kappa_{4,v}, fractional pair incidences b_{ij,v}, color factor C_N, Gaussian margin M_G, and tail budget T_tail, then exports one interval to the finite OS gate.
- same-theory condition: the endpoint sources are derivatives of the same heat-kernel Wilson partition function with the same Wilson normalization, with no reflection-plane counterterm, boundary Hilbert sector, algebra enlargement, or regulator switch.
- fractional incidence b_{ij,v}: the normalized overlap of the i-j reflected hairpin pair footprint with endpoint box v, including geometric signs already fixed by the null-channel orientation.
- endpoint dominance D_v: the null-channel incidence scalar D_v=2 b_{12,v}-4 b_{13,v}-4 b_{23,v}.
- kappa interval: kappa_{4,v}^{sing} in [-bar_beta_v,-under_beta_v] with 0<=under_beta_v<=bar_beta_v, certified from same-theory source data.
- conceptual pressure: endpoint collapse must be sign-certified inside the fixed Wilson theory rather than hidden in a symbolic R term.

## Assumptions

- Model: SU(N) lattice Yang-Mills with heat-kernel plaquette action, finite volume, gauge-invariant Wilson loops, and the standard reflection-positive lattice reflection.
- Regime: the H,K three-hairpin block is fixed, endpoint boxes shrink inside a collar, and all non-endpoint straight-segment contacts are assigned to the previously controlled cancellations or to T_tail.
- Cutoff: beta intervals, incidence intervals, and T_tail are uniform along the cutoff-removal subsequence relevant to this finite block, but no full continuum OS theorem is claimed.
- Same-theory: source insertions defining kappa_{4,v}^{sing} are logarithmic derivatives of the locked Wilson expectation functional, not new boundary observables.
- Validity: Wick-square terms are kept as positive Gram contributions, straight C_A f f contacts cancel by the null-incidence identity, and only connected endpoint/corner cumulants enter R_end.
- Local: endpoint boxes are disjoint after collar localization, and any overlap not assigned to a box is charged to T_tail.
- Constraint: fractional incidences satisfy 0<=b_{ij,v}<=1 after normalization and use the same orientation convention as the computed H,K block.

## Equations

- endpoint dominance scalar: `D_v=2b_{12,v}-4b_{13,v}-4b_{23,v}=2\bigl(b_{12,v}-2b_{13,v}-2b_{23,v}\bigr)`. Valid when: Valid when the three reflected Wilson hairpins use the fixed null vector z=(1,1,-2) and the fractional endpoint incidences are measured in the same heat-kernel collar boxes.
- half-overlap shield: `b_{13,v}+b_{23,v}\ge \frac12 b_{12,v}\quad\Longrightarrow\quad D_v\le 0`. Valid when: Valid for normalized nonnegative endpoint incidences in the finite three-hairpin block after the H,K null-channel orientation has been fixed.
- adversarial lower gate: `I_-^{adv}=M_G-C_N\sum_v \bar\beta_v\,[\overline D_v]_+-T_{tail}`. Valid when: Applies when kappa_{4,v}^{sing}\in[-\bar\beta_v,-\underline\beta_v], D_v\in[\underline D_v,\overline D_v], and all unlocalized endpoint remnants are bounded by T_tail.
- promotion and falsifier interval: `I_{gate}=M_G+C_N\sum_v [\kappa_{4,v}^{sing}]\,[D_v]+[-T_{tail},T_{tail}],\quad I_- >0\Rightarrow \mathrm{promote},\quad I_+<0\Rightarrow \mathrm{falsifier}`. Valid when: Valid when interval arithmetic uses same-theory source derivative intervals and the finite Schur-Feshbach gate has no additional boundary counterterm or algebra change.

## Attempted Derivation

- Freeze claim level: this cycle targets a finite post-H,K reflected-Wilson OS transfer gate only; it does not assert continuum existence, OS/Wightman reconstruction for all observables, nontriviality, or a mass gap.
- Conceptual pressure attacked: endpoint collapse must be sign-certified in the same Wilson theory, because the formal collar positivity bridge is useless if the endpoint OPE secretly introduces a boundary theory.
- Declarative tension: finite collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold; symbolic R is representation-limited because it hides incidence signs, while a raw kappa_4 spectrum is too strong because negative kappa_4 is harmless when D_v<=0.
- Compare routes: the global Schur-preimage matrix test is valid but coarse after H,K; formal OPE language is flexible but not decision-grade; the C_ep source-interval carrier is local, computable, and exports one scalar gate.
- Use the known cancellations as inputs: Wick-square contractions are nonnegative Gram terms, straight C_A f f contacts cancel in the null channel, and one-body or length-linear Wilson renormalizations vanish in the corrected Schur-Feshbach scalar.
- Partition the remaining collar-contact support into endpoint boxes v and define fractional incidences b_{ij,v}; contraction with z=(1,1,-2) gives D_v=2b12-4b13-4b23.
- Derive the half-overlap shield: if b13+b23>=b12/2 then D_v<=0, so a negative endpoint kappa_4 cannot lower the gate from that box; only certified 12-dominant boxes enter the adversarial lower bound.
- Represent kappa_{4,v}^{sing} by same-theory source derivatives of ell_v=log Z_v and bound it with the seven-point fourth-derivative stencil plus the 7h^4 M8/240 error term.
- Assemble the interval I_gate=M_G+C_N sum_v[kappa_v][D_v]+[-T_tail,T_tail]; I_->0 is a finite promotion certificate, I_+<0 is a concrete finite falsifier.
- Hard gate changed: success promotes the finite post-H,K reflected-Wilson OS block to the closed-cone/collar transfer queue; failure quarantines this hairpin route by producing an explicit same-theory endpoint counterexample.
- Conceptual value signal: sharpness and route change at finite scope, because the obstruction is not endpoint kappa_4 negativity itself but certified positive 12-dominance plus nonuniform or negative tail.

Blocking gap: No certified numerical or analytic intervals yet for the same-theory endpoint source values, fractional b_{ij,v} in the actual hairpin geometry, M_{8,v}, and T_tail. Without these data the theorem is a valid finite certificate template, not a promoted block.

## Falsifiers

- A source-stencil computation in the same heat-kernel Wilson theory yields I_+<0 for a 12-dominant endpoint configuration; this is a finite same-theory falsifier of the post-H,K block.
- The endpoint collapse requires a reflection-plane counterterm, cusp renormalization ratio, or boundary Hilbert sector not present in the locked Wilson algebra.
- The tail T_tail is not cutoff-uniform, so the endpoint interval cannot be valid in the cutoff-removal topology.
- Measured fractional incidences violate the half-overlap shield with large b12 and small b13+b23, while beta_v remains strongly positive and M_G is too small.
- The seven-point source evaluations fail analyticity or gauge-invariant same-theory normalization, making the kappa_4 interval an artifact rather than Yang-Mills input.

## Learning

Cycle 288 makes the endpoint obstruction decision-grade. The actual post-H,K object is not symbolic R and not raw negative kappa_4; it is the same-theory interval M_G+C_N sum_v kappa_v D_v plus tail. The new sharp computation is D_v=2b12-4b13-4b23 and the half-overlap shield b13+b23>=b12/2. Thus only certified 12-dominant endpoint boxes can be dangerous. This is novel at the branch scope because it converts endpoint collapse from a representational slogan into a finite source-derivative and incidence problem with a valid promotion/falsifier criterion.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and endpoint-data prioritizer.`
- Rationale: The branch has exhausted abstract OS-closed-cone refinements; the decisive uncertainty is whether actual endpoint geometry produces 12-dominant positive D_v with negative connected kappa_4 large enough to beat M_G.
- Situation seed: Take the fixed heat-kernel SU(2) or SU(3) three-hairpin reflected Wilson block and replace the endpoint partition by a one-parameter family of fractional endpoint boxes with b12=1, b13=b23=eta/2, while keeping the same plaquette-sheet source L_v and null vector z=(1,1,-2).
- Varied variable: The half-overlap ratio eta=(b13+b23)/b12 across the endpoint box, varied through the shield threshold eta=1/2.
- Held-fixed controls: Heat-kernel plaquette regulator, Wilson normalization, and finite volume are fixed., The three hairpin loops, Schur-Feshbach null vector, color factor C_N, and Gaussian margin M_G are fixed., No boundary counterterm, algebra enlargement, or cusp-renormalization division is allowed., The same seven-point source stencil and M8 tail protocol are used for every eta.
- Expected observation: For eta>=1/2 the endpoint contribution is shielded because D_v<=0; for eta<1/2 the interval should expose whether 12-dominance can turn negative kappa_4 into I_+<0 or whether M_G and T_tail keep I_->0.
- Transfer certificate needed: A cutoff-uniform proof that the fractional endpoint incidences and source derivative intervals arise from the same regulated Wilson observables, plus a uniform T_tail bound, before the thought experiment may affect proof obligations.

## Next Experiment

For the actual H,K hairpin geometry, tabulate endpoint boxes v with b12,b13,b23; compute D_v and mark shielded boxes; for unshielded 12-dominant boxes, evaluate the seven-point same-theory source stencil for ell_v=log Z_v and assemble I_gate with a cutoff-uniform T_tail interval.

# Endpoint Ward-Hessian enclosure for the post-H,K R mediator

## Candidate Lemma

Conditional finite Route A lemma: a cutoff-uniform Ward-Hessian near/far enclosure for the flowed connected four-curvature endpoint polarization gives a valid lower interval for R_{++}; if it beats L_+, the H,K endpoint-box positivity gate is promoted.

## Definitions

- source object: finite-volume lattice SU(N) Yang-Mills Wilson measure at spacing a with gradient-flow time t>0 and centered renormalized H,K endpoint hairpin Wilson cumulant.
- target object: finite Route A endpoint-box mediator lower interval R_{++}^{I,-} used only in the Schur-Feshbach plus channel.
- controlled interface: endpoint sheet-current map J_+ with Ward/cusp subtraction, zero monopole/dipole moments, and interval Hessian bounds for the C4 kernel.
- same-theory condition: pair term, connected C4 term, counterterms, and leakage comparison are computed from the same cutoff measure and flow regulator.
- carrier: endpoint cells C with signed sheet currents, moments M_2(C), sector kernels K_4^{WS}, and certified zero-pairing current equivalence.

## Assumptions

- Model: SU(N), N>=2, finite torus, Wilson plaquette action, fixed H,K sheet currents, and Luescher gradient flow time t>0.
- Regime: endpoint cell diameter eta <= c sqrt(8t); nonendpoint sheet pieces stay outside the endpoint collar used for the local bound.
- Cutoff: constants are uniform for a<eta/8 and volume larger than four flow radii; this is no continuum or mass-gap claim.
- Same-theory: all cumulants, counterterms, and g_t normalization use one bare action and one flow-time prescription.
- Local: the plus endpoint current has zero charge and zero first moment after reflection symmetrization of the H,K geometry.
- Validity: Ward and cusp subtractions leave no first-derivative boundary term in the endpoint Taylor expansion.

## Equations

- R-decomposition: `R_{++}^{ren}=g_t^4\{2(N^2-1)G_{++}+N(N^2-1)\Xi_{++}^{WS}\}+E_6`. Valid when: Valid when the centered flowed hairpins are expanded to fourth curvature order with disconnected, perimeter, and cusp terms subtracted in the same Wilson measure.
- Ward-Hessian cell bound: `\Xi_{++}^{WS}\ge-\sum_{C,D}H_{CD}^{I,+}M_2(C)M_2(D)`. Valid when: Applies after Ward subtraction and plus-channel monopole/dipole cancellation, with endpoint cells small enough for second-order Taylor remainders to dominate.
- promotion inequality: `g_t^4(N^2-1)\left(2G_{++}^{I,-}-N\sum_{C,D}H_{CD}^{I,+}M_2(C)M_2(D)\right)-E_6^{I,+}>L_+`. Valid when: Requires cutoff-uniform intervals for G, H, and E6 on the fixed H,K endpoint geometry and the finite Schur-Feshbach leakage L_+.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: finite-volume lattice SU(N) Yang-Mills Wilson measure at spacing a with gradient-flow time t>0 and centered renormalized H,K endpoint hairpin Wilson cumulant.; target object: finite Route A endpoint-box mediator lower interval R_{++}^{I,-} used only in the Schur-Feshbach plus channel.; Model: SU(N), N>=2, finite torus, Wilson plaquette action, fixed H,K sheet currents, and Luescher gradient flow time t>0..
- Expand the two centered flowed hairpins to fourth curvature order; disconnected products and one-hairpin perimeter/cusp terms cancel, leaving the positive pair term plus C4 polarization.
- Replace raw contours by endpoint sheet currents. Ward subtraction removes longitudinal pieces, and plus-channel charge/dipole cancellation kills constant and first Taylor terms.
- Split endpoint cell pairs into near and far sectors. Use heat-kernel majorants near the diagonal and derivative bounds away from it to certify H_{CD}^{I,+}.
- Insert the interval C4 lower bound into the finite Schur-Feshbach plus-channel inequality and compare against the already computed leakage L_+.

Blocking gap: The actual H,K geometry still needs certified numerical or analytic H_near, H_far, E6, and zero-moment checks uniform in a for the chosen flow window.

## Falsifiers

- Ward falsifier: the H,K plus endpoint current retains residual charge or dipole moment, producing an O(eta) C4 term.
- Regulator falsifier: the R_{++}^{I,-} sign is not stable as a/sqrt(8t) decreases or no flow-time plateau exists.
- Geometry falsifier: near-cell Hessian constants make N sum H M2 M2 exceed 2G_{++}^{I,-} before comparison with L_+.
- Same-theory falsifier: cusp, perimeter, or coupling normalization is imported from a different Wilson measure or flow prescription.

## Learning

Conceptual pressure: finite Schur-Feshbach positivity needs a same-theory Wilson mediator. Tension: pair covariance is valid but C4 can erase it. Endpoint currents beat raw contours and global OS witnesses because Ward moments, heat-kernel Hessians, and interval arithmetic become primitive.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a concrete finite calculation because the valid obstruction is no longer conceptual; it is whether the C4 endpoint polarization can erase the positive pair mediator.
- Situation seed: Finite torus SU(N) Wilson lattice action with Luescher flow, fixed H,K endpoint sheet currents, and interval cells covering the endpoint collar.
- Varied variable: rho=eta/sqrt(8t), the endpoint-cell diameter divided by the flow radius.
- Held-fixed controls: Same H,K sheet-current geometry and plus-channel reflection symmetrization., Same bare lattice measure, flow-time normalization, and cusp/perimeter subtraction., Fixed finite Schur-Feshbach leakage L_+ and no continuum or spectral-gap claim.
- Expected observation: For small rho, Ward moments should force the C4 lower error to scale like rho^2 while the pair interval stays positive; failure gives a clean demotion.
- Transfer certificate needed: Cutoff-uniform Ward identities, cusp cancellation, heat-kernel Hessian majorants, and a stable flow-time plateau before the intuition affects proof obligations.

## Next Experiment

Compute interval bounds for H_near(t), H_far(t,d), G_{++}, E6, and the zero-moment matrix for the fixed H,K endpoint cells while sweeping rho in a single same-theory lattice-flow window.

# Raw plaquette interval certificate for post-H,K boundary polarization

## Candidate Lemma

Finite raw-plaquette endpoint certificate: same-regulator intervals U_ell bounding the compressed negative connected four-curvature cumulant imply Q_end>=Delta_sigma^plaq. If Delta_sigma^plaq>0, Schur-corrected endpoint positivity holds for the worked H,K box only.

## Definitions

- source object: finite-volume lattice SU(N) Yang-Mills with heat-kernel smearing scale sigma, spacing a, Wilson sheet basis S_i, and plaquette curvatures F_p transported to common endpoints.
- target object: the finite endpoint quadratic form on reflected Wilson endpoint vectors after the H,K Schur-Feshbach subtraction, with numerical lower margin Delta_sigma^plaq.
- controlled interface: raw plaquette interval bounds U_ell for the compressed connected four-curvature cumulant K^(4), plus C_sigma, E_OPE, and s_HK in the same basis.
- same-theory condition: identical cutoff box, bare coupling, heat-kernel regulator, Wilson normalization, reflection plane, endpoint compression, and H,K Schur data are used for every term.
- carrier: sheet-kernel hypergraph with sheet-pair nodes and transported plaquette-quadruple edges carrying color tensors, shell labels, weights, multiplicities, OPE intervals, and Schur data.

## Assumptions

- Model: compact SU(N) lattice Yang-Mills on a finite endpoint box with Wilson or heat-kernel action fixed before calculation; no continuum limit is invoked.
- Regime: sigma/a is fixed and large enough for the boundary OPE remainder to be bounded by e_OPE on the selected Wilson sheets.
- Same-theory: C_sigma, K^(4), E_OPE, and s_HK are evaluated at the same cutoff, coupling, volume, and Wilson-loop normalization.
- Validity: raw plaquette interval arithmetic is outward-rounded and quotients only by trace identities and sheet symmetries preserving the Wilson cumulant.

## Equations

- transported flux carrier: `\Phi_i^A=\sum_{p\in S_i}w_i(p)K_\sigma(x_i,p)\,\mathrm{Ad}(U_{i,p})^{AB}F_p^B`. Valid when: Valid when heat-kernel smearing, endpoint transporters, and Wilson sheet weights are fixed in the finite cutoff box.
- connected polarization decomposition: `R_{ij}=\mathrm{cum}_2(:\Phi_i^A\Phi_i^A:,:\Phi_j^B\Phi_j^B:)=\alpha_N g_R^4(C_\sigma\circ C_\sigma)_{ij}+\frac{g_R^4}{16N^2}K^{(4)}_{ij}+E^{\mathrm{OPE}}_{ij}`. Valid when: Applies after same-cutoff normal ordering cancels vacuum and perimeter disconnected pieces in the reflected Wilson cumulant.
- raw plaquette margin: `\Delta_\sigma^{\mathrm{plaq}}\ge \alpha_N g_R^4\lambda_{\min}(C_\sigma\circ C_\sigma)-\frac{g_R^4}{16N^2}\max_i\sum_\ell n_{i\ell}U_\ell-e_{\mathrm{OPE}}-s_{HK}`. Valid when: Requires outward-rounded shell intervals U_ell, same-regulator OPE error, and the H,K Schur energy in one endpoint basis.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: finite-volume lattice SU(N) Yang-Mills with heat-kernel smearing scale sigma, spacing a, Wilson sheet basis S_i, and plaquette curvatures F_p transported to common endpoints.; target object: the finite endpoint quadratic form on reflected Wilson endpoint vectors after the H,K Schur-Feshbach subtraction, with numerical lower margin Delta_sigma^plaq.; Model: compact SU(N) lattice Yang-Mills on a finite endpoint box with Wilson or heat-kernel action fixed before calculation; no continuum limit is invoked..
- Expand each endpoint Wilson observable to the quadratic heat-kernel flux Phi_i through its plaquette sheet; keep the same regulator and endpoint transporters as the H,K computation.
- Use cutoff normal-ordering. Disconnected vacuum and perimeter terms cancel from cum_2(:Phi_i^2:,:Phi_j^2:); crossed pairings and the connected four-curvature cumulant remain.
- Evaluate crossed pairings by color trace identities, giving alpha_N=(N^2-1)/(8N^2) and a positive semidefinite Hadamard square C_sigma o C_sigma.
- Compress the connected four-curvature remainder to sheet-pair nodes. Bound its negative spectrum by raw shell intervals U_ell, subtract e_OPE and s_HK, and test Delta_sigma^plaq>0.

Blocking gap: No same-regulator outward-rounded U_ell for the actual H,K plaquette sheets has been computed; prior A012 shell symbols remain quarantined.

## Falsifiers

- falsifier: outward-rounded U_ell make alpha_N g_R^4 lambda_min minus K4, OPE, and s_HK terms nonpositive.
- falsifier: connected K^(4) intervals are not stable under changing the plaquette quotient to an equivalent Wilson trace basis.
- falsifier: e_OPE cannot be bounded at chosen sigma/a without importing continuum regularity.
- falsifier: H,K Schur energy s_HK was computed with a different normalization or regulator.

## Learning

Conceptual pressure: replace symbolic A012 by raw plaquette proof search. Declarative tension: Wilson/OPE, K4 negativity, and s_HK must share one cutoff while Clay gates stay non-claims. Sheet hypergraph beats scalar R and OS density. Value: finite route-deciding Delta; changes endpoint positivity only.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe for the quarantined A012 route.`
- Rationale: The branch is blocked by absent raw intervals, not by missing vocabulary; only a plaquette-level K^(4) computation can decide the finite endpoint gate.
- Situation seed: Finite SU(2) heat-kernel lattice endpoint box containing two reflected rectangular Wilson sheets and the worked H,K hairpin collar; enumerate all plaquette quadruples contributing to K^(4).
- Varied variable: sigma/a, varied over the fixed finite set {2,3,4,5}.
- Held-fixed controls: Same Wilson endpoint basis and reflected support used in the H,K calculation., Same finite lattice box, boundary conditions, bare coupling convention, and heat-kernel action., Same normal-ordering and vacuum/perimeter cancellation in every cumulant.
- Expected observation: If U_0,U_1,U_2 stay below the PSD color-square margin as sigma/a varies, Delta is positive; otherwise the finite H,K route demotes.
- Transfer certificate needed: Outward-rounded interval proof mapping raw plaquette quadruple sums to K^(4) entries, preserving gauge-invariant trace identities and Schur normalization.

## Next Experiment

Hand-calculate SU(2), one reflection-paired plaquette rectangle, sigma/a=3: enumerate K^(4) shell-0 quadruples, compute color-factor intervals, and test Delta sign with existing s_HK.

