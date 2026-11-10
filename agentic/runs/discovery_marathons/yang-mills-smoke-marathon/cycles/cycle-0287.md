# cycle-0287

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint source intervals for the reflected-Wilson post-HK gate

## Candidate Lemma

For the heat-kernel plaquette-sheet regulator, the connected endpoint boundary-OPE contribution to the finite reflected-Wilson null channel is certified by same-theory endpoint source derivatives. After Wick-square Gram positivity and straight f f incidence cancellation, endpoint boxes with half-overlap shielding cannot lower the finite OS gate; only certified 12-dominant boxes plus a uniform tail can be a falsifier.

## Definitions

- source object: regulated SU(N) heat-kernel plaquette-sheet endpoint boxes B_v carrying Wilson hairpin source values ell_{a,v}(kh), fractional incidences b_{ij}(v), and a cutoff tail budget T_tail.
- target object: the finite post-HK reflected-Wilson Schur-Feshbach gate for the locked three-hairpin OS matrix, expressed as a scalar interval I_gate for the null channel.
- controlled interface: the same-theory endpoint carrier C_ep=(ell_{a,v}(kh),b_{ij}(v),C_N,M_G,T_tail) maps regulated connected Wilson source cumulants to a finite OS-gate interval without adding boundary degrees of freedom.
- same-theory condition: Wilson loop normalization, heat-kernel regulator, reflection map, endpoint source directions, and gauge-invariant observable algebra are identical before and after collar collapse; no boundary counterterm or algebra enlargement is allowed.
- Declarative tension: collar reflection positivity, fixed gauge-invariant Wilson observables, and singular endpoint boundary OPE must jointly hold, but raw R hides incidence signs and raw kappa4 overstates danger.
- Carrier critique: C_ep is sharper than raw R and less coarse than the global Schur-preimage matrix because it remembers source data, color factors, and fractional endpoint incidence.
- Efficient representation: encode endpoint boxes, seven source values, beta intervals, b_ij incidences, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; primitive operations are source differentiation, interval arithmetic, color multiplication, clipping, incidence contraction, and tail addition; equivalence is equality of regulated source data; locality cost is charged to T_tail; transfer exports only I_gate.

## Assumptions

- Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action and gauge-invariant Wilson plaquette-sheet approximants for the reflected hairpins.
- Regime: finite lattice spacing a, finite endpoint box B_v, small heat-kernel time t_a on the endpoint chart, and fixed collar geometry before taking any continuum limit.
- Cutoff: all source derivatives, M_8 bounds, and T_tail are uniform over the finite cutoff range used by the finite Route A block.
- Same-theory: the endpoint source carrier is computed from the same regulated Wilson observables used in the collar OS matrix, not from a boundary-renormalized surrogate theory.
- Local: endpoint boxes are disjoint after the prescribed partition; all nonlocal overlap, source-direction mismatch, and corner leakage are charged to T_tail.
- Validity: the Wick-square term is treated as a positive Gram contribution, and the straight nonabelian f f contact is removed only when the already-verified null incidence identity holds.

## Equations

- endpoint source log: `Z_{a,v}(s)=\int_{G^{E_v}}\exp\{-S_{HK,a,v}(U)+s\,\mathcal L_v(U)\}\,d\mu_{HK}(U),\qquad \ell_{a,v}(s)=\log Z_{a,v}(s)`. Valid when: Valid when the endpoint box is cut from the heat-kernel plaquette-sheet regulator with the same Wilson source used in the reflected OS block.
- seven point fourth cumulant stencil: `\widehat\kappa_{4,a,v}(h)=h^{-4}\left[-\tfrac16\ell_{a,v}(-3h)+2\ell_{a,v}(-2h)-\tfrac{13}{2}\ell_{a,v}(-h)+\tfrac{28}{3}\ell_{a,v}(0)-\tfrac{13}{2}\ell_{a,v}(h)+2\ell_{a,v}(2h)-\tfrac16\ell_{a,v}(3h)\right]`. Valid when: Valid when ell_{a,v} is C^8 on the source interval and the eighth derivative is bounded uniformly by the endpoint-box estimate.
- stencil error interval: `\left|\widehat\kappa_{4,a,v}(h)-\partial_s^4\ell_{a,v}(0)\right|\le \frac{7h^4}{240}M_{8,a,v}`. Valid when: Valid when the same regulated source line is evaluated at all seven stencil points and M_{8,a,v} bounds the eighth source derivative.
- compact group quartic seed: `\partial_s^4\ell_{a,v}(0)=-\frac{t_a^4}{120}\operatorname{Tr}_{ad}\!\left((\operatorname{ad}Y_v)^4\right)+O\!\left(t_a^5\|Y_v\|^4+t_a^4\epsilon_{geom,v}\right)`. Valid when: Valid for small heat-kernel time in exponential endpoint coordinates after the Gaussian Wick-square part has been separated as a positive Gram term.
- clipped lower gate: `I_{gate}^{lo}=M_G-C_N\sum_v \overline\beta_v\,[D_v]_+-T_{tail},\qquad D_v=2b_{12}(v)-4b_{13}(v)-4b_{23}(v),\qquad C_N=\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Valid when beta intervals enclose minus the connected endpoint fourth cumulant and all leftover endpoint leakage is included in T_tail.
- half overlap shield: `b_{13}(v)+b_{23}(v)\ge \tfrac12 b_{12}(v)\quad\Longrightarrow\quad D_v\le 0`. Valid when: Valid when fractional incidences are nonnegative and normalized against the same endpoint source direction for all three Wilson pairings.

## Attempted Derivation

- Fix the conceptual pressure: endpoint collapse must be sign-certified in the same Wilson theory, not by adding a boundary OPE theory after the fact.
- Start with the heat-kernel plaquette-sheet endpoint partition Z_{a,v}(s) and use the connected log ell_{a,v}(s), so disconnected Wick-square contractions are not counted as dangerous endpoint R.
- In exponential endpoint coordinates, expand the compact-group Haar factor; its first non-Gaussian quartic source contribution is negative, with leading coefficient -(t_a^4/120)Tr_ad((ad Y_v)^4), while the Gaussian part remains a positive Gram term.
- Use the already established null incidence identity to cancel straight C_A f f contacts along non-endpoint segments; charge source-direction mismatch and corner leakage to T_tail.
- Estimate the connected fourth source derivative by the seven-point stencil; the leading truncation error is bounded by 7 h^4 M_8/240, giving a valid interval for beta_v=-kappa4_v.
- Contract the endpoint interval with D_v=2b12-4b13-4b23. The half-overlap shield b13+b23>=b12/2 implies D_v<=0, so a negative compact-group kappa4 is protective or neutral there.
- Export only I_gate to the finite Schur-Feshbach OS gate: I_gate^lo>0 promotes this finite Wilson block, while I_gate^hi<0 is a same-theory finite falsifier.

Blocking gap: The actual fractional b_{ij}(v) table, uniform M_8 bounds, and T_tail estimates for the concrete hairpin endpoint geometry are not yet certified from regulator data.

## Falsifiers

- A 12-dominant endpoint box with certified D_v>0 and beta_v large enough to force I_gate^hi<0 is a finite same-theory falsifier of this post-HK block.
- The source derivative ell_{a,v}(s) requires a boundary counterterm or boundary state not present in the locked Wilson algebra.
- The eighth-derivative bound M_8 or the tail T_tail grows with the cutoff so the endpoint interval is not uniform in the finite regulator range.
- Endpoint source directions fail to factor through a common singlet unit source, making D_v clipping invalid rather than merely conservative.
- A residual straight f f contact survives the null incidence contraction, invalidating the cancellation used before the endpoint interval is formed.

## Learning

Cycle 287 attacks the conceptual pressure of endpoint collapse in the same Wilson theory. The declarative tension is collar OS positivity plus fixed gauge-invariant Wilson observables plus a singular connected endpoint OPE, with no permission to add a boundary theory. Raw R is too weak because it hides incidence signs; raw kappa4 is too strong because negative compact-group kappa4 is harmless whenever the half-overlap shield gives D_v<=0; the global Schur-preimage route is valid but too coarse after H,K. The sharper carrier is C_ep: endpoint boxes, seven source values, beta intervals, fractional incidences, C_N, M_G, and T_tail, with primitive operations source differentiation, interval arithmetic, color multiplication, clipping, incidence contraction, and tail addition. The hard gate changed is the finite post-HK reflected-Wilson OS transfer gate: success promotes this finite block, failure gives a concrete falsifier. The conceptual value signal is sharpness and route change at finite scope: the dangerous object is certified 12-dominance plus uncontrolled tail, not negative endpoint kappa4 itself. Clay continuum construction, nontriviality, full OS/Wightman reconstruction, and mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has reduced the obstruction to endpoint source data; another abstract OS restatement would not decide whether the finite post-HK Wilson block promotes or produces a valid falsifier.
- Situation seed: Heat-kernel SU(N) endpoint box for the three reflected Wilson hairpin footprints, with seven same-theory source evaluations of ell_v(s) and fractional incidences b12,b13,b23 assigned by plaquette-sheet overlap inside one endpoint cube.
- Varied variable: eta=(b13+b23)/b12, the fractional non-12 overlap shielding ratio, varied from 0 to 1 while keeping the endpoint source norm fixed.
- Held-fixed controls: Gauge group SU(N), heat-kernel plaquette action, and Wilson plaquette-sheet normalization are fixed., The Schur-Feshbach null-channel weights 2,-4,-4 and the straight f f cancellation identity are held fixed., No boundary counterterm, boundary Hilbert sector, or change of gauge-invariant observable algebra is allowed., The same h, M_8 certification method, color factor C_N, and tail bookkeeping are used for all eta.
- Expected observation: The endpoint term can lower the gate only for eta<1/2; at eta>=1/2 the half-overlap shield makes D_v<=0, so negative compact-group kappa4 is neutral or protective up to T_tail.
- Transfer certificate needed: A cutoff-uniform source-derivative interval for beta_v, a verified fractional incidence table for the concrete hairpin endpoint boxes, and a tail bound proving that unmodeled corners cannot change the sign of I_gate.

## Next Experiment

Compute the concrete endpoint incidence table and seven-point heat-kernel source intervals for the smallest SU(2) and SU(3) plaquette-sheet endpoint boxes; report I_gate^lo/I_gate^hi with M_8 and T_tail separated.

# Gauge-Invariant Nontriviality Witness Selection -> finite endpoint R/kappa4 certificate

## Candidate Lemma

Conditional Ward-Hessian endpoint-cell enclosure: for the H,K plus-channel endpoint current, the same-theory flowed Wilson covariance has a certified lower interval once the Ward-subtracted connected four-curvature kernel has a cutoff-uniform Hessian majorant on the endpoint cells.

## Definitions

- source object: finite-volume SU(N) Wilson lattice Yang-Mills at spacing a, side L, gradient-flow time t>0, point-splitting rho, and the H,K plus-channel endpoint sheet current J_+ supported in endpoint boxes B_eta.
- target object: a scalar lower certificate R_{++}^{-}(a,L,t,rho,eta) for the endpoint mediator entering the finite Schur-Feshbach plus-channel inequality, not a continuum mass-gap claim.
- controlled interface: the centered renormalized flowed Wilson hairpin covariance is decomposed into an explicit two-curvature pair contraction plus a Ward/cusp-subtracted connected four-curvature polarization bounded by endpoint cell moments.
- same-theory condition: the Wilson loops, gradient flow, counterterms, cumulants, and Feshbach coefficients are computed from the same lattice YM measure and the same cutoff-removal family; no imported Gaussian process or auxiliary theory is substituted.
- Observable: \widehat W_+^{ren} is the centered plus-channel product/linear combination of the two thin hairpin Wilson observables after one-hairpin perimeter and cusp subtraction.
- Carrier: endpoint sheet currents encode oriented plaquette sheets and endpoint charges; currents are quotiented only by certified zero-pairing equivalence against the flowed two-curvature kernel.

## Assumptions

- Model: four-dimensional hypercubic lattice SU(N) Yang-Mills with Wilson action, finite torus volume, Luescher gradient flow, and gauge-invariant Wilson hairpin observables.
- Regime: a << rho <= sqrt(8t) <= c eta << d, where d is the separation between the two endpoint boxes and c is fixed small enough to keep near/far cells distinct.
- Cutoff: all interval bounds are uniform for a<a0(t,rho,eta) and L>L0(d,eta); the statement is finite-cutoff conditional until this uniformity is verified.
- Same-theory: the renormalized hairpin subtraction, flowed curvature kernels, and Schur-Feshbach leakage L_+ use the same bare coupling trajectory and the same observable normalization.
- Validity: Ward subtraction removes gauge-longitudinal endpoint terms and the one-hairpin perimeter/cusp counterterm removes local self-energy contributions before the connected C4 bound is applied.
- Local: the claim concerns only the finite endpoint boxes after the H,K reduction; continuum existence, OS positivity, observable density, topology control, and Hamiltonian spectral transfer remain untouched.

## Equations

- flowed endpoint covariance carrier: `R_{++}^{a,L,t,\rho}:=\kappa_2^{a,L}\!\left(\widehat W_+^{ren}(t,\rho),\widehat W_+^{ren}(t,\rho)\right)_{end}`. Valid when: Valid when the centered renormalized hairpin observables are built from the same flowed lattice YM measure and only endpoint-supported cumulant contributions are retained.
- pair-plus-connected decomposition: `R_{++}^{a,L,t,\rho}=g_t^4 (N^2-1)\left(2G_{++}^{a,L,t,\rho}+N\Xi_{++}^{WS,a,L,t,\rho}\right)+\mathcal E_6^{a,L,t,\rho}`. Valid when: Applies after disconnected-product subtraction, one-hairpin perimeter/cusp subtraction, and fourth-order Wilson expansion in endpoint boxes with controlled sixth-order remainder.
- endpoint moment cancellation: `\sum_{c\subset B_\eta} q_c=0,\qquad \sum_{c\subset B_\eta}q_c(x_c-x_B)_\mu=0`. Valid when: Requires the plus-channel H,K endpoint current orientation and the Ward-subtracted sheet-current representation on each endpoint cell.
- Ward-Hessian C4 enclosure: `|\Xi_{++}^{WS,a,L,t,\rho}|\le H_{4,++}^{a,L,t,\rho,+}(B_\eta)\,M_{2,+}(B_\eta)^2`. Valid when: Valid when the Ward-subtracted connected four-curvature kernel has a certified interval Hessian bound over the endpoint boxes and the monopole and dipole moments vanish.
- computable lower interval: `R_{++}^{-}=g_t^4 (N^2-1)\left(2G_{++}^{-}-N H_{4,++}^{+}M_{2,+}^2\right)-E_6^{+}`. Valid when: Valid in the finite endpoint-cell partition after interval lower bounding the pair contraction and interval upper bounding the C4 Hessian and sixth-order remainder.
- finite Route A promotion inequality: `A_{+}^{-}+R_{++}^{-}>L_{+}^{+}`. Valid when: Applies only to the post-H,K finite Schur-Feshbach plus channel, with A_+ the already-enclosed non-endpoint contribution and L_+ the same finite leakage term.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: finite-volume SU(N) Wilson lattice Yang-Mills at spacing a, side L, gradient-flow time t>0, point-splitting rho, and the H,K plus-channel endpoint sheet current J_+ supported in endpoint boxes B_eta.; target object: a scalar lower certificate R_{++}^{-}(a,L,t,rho,eta) for the endpoint mediator entering the finite Schur-Feshbach plus-channel inequality, not a continuum mass-gap claim.; Model: four-dimensional hypercubic lattice SU(N) Yang-Mills with Wilson action, finite torus volume, Luescher gradient flow, and gauge-invariant Wilson hairpin observables..
- Start from the same-theory finite-cutoff covariance R_{++}=kappa_2(W_+^{ren},W_+^{ren})_{end} for gradient-flowed Wilson hairpins.
- Expand each small endpoint hairpin by the nonabelian Stokes/plaquette-sheet expansion through order g_t^4; center the observables so disconnected products cancel.
- Use one-hairpin perimeter and cusp counterterms to remove local self-contractions; the surviving order-g_t^4 terms split into two flowed two-curvature cross pairings and one connected four-curvature cumulant.
- Contract color traces in the pair sector, giving the positive baseline 2(N^2-1)G_{++}; collect the connected color structure as N(N^2-1)Xi_{++}^{WS}.
- Represent H,K plus-channel endpoint data by sheet currents. Ward subtraction plus plus-channel orientation gives zero monopole and dipole moments cellwise.
- Taylor expand the Ward-subtracted C4 kernel in endpoint-cell coordinates. Constant and linear terms vanish; the remainder is bounded by the cell Hessian majorant times M_{2,+}^2.
- Combine the pair lower interval, C4 upper interval, and sixth-order remainder upper interval to obtain R_{++}^{-}. Compare A_{+}^{-}+R_{++}^{-} with the finite Schur-Feshbach leakage L_{+}^{+}.

Blocking gap: The missing proof object is a cutoff-uniform near/far Hessian majorant for the Ward-subtracted connected four-curvature kernel C_{4,t}^{WS}, together with a certified sixth-order Wilson remainder on the same regulator plateau.

## Falsifiers

- Ward-subtracted endpoint currents fail the cellwise monopole/dipole cancellation in the actual H,K geometry.
- The pair interval G_{++}^{-} is zero or negative after orientation and reflection signs are inserted.
- The connected C4 Hessian bound grows like a negative power of a and has no cutoff plateau at fixed positive flow time.
- Cusp or perimeter subtraction leaves a rho-dependent divergence in R_{++}^{-}.
- The zero-pairing quotient identifies two sheet representatives with different Wilson cumulant intervals.
- The finite promotion inequality A_{+}^{-}+R_{++}^{-}>L_{+}^{+} fails on all admissible eta,t,rho windows; this is the decisive falsifier for the endpoint repair.

## Learning

Conceptual pressure attacked: the missing mediator between finite Schur-Feshbach positivity and same-theory Wilson cumulant positivity. Declarative tension: pair covariance and gradient-flow renormalization are valid local inputs, but the connected four-curvature polarization can erase the positive pair term unless a cutoff-uniform Ward-Hessian interval exists. Carrier critique: raw Wilson contours are fragmented and representation-limited; global OS/non-Gaussian witnesses are too coarse for this finite obstruction. Efficient representation requirements are now precise: encode H,K sheets, endpoint currents, cell moments, sector kernels, and counterterms; preserve gauge, color, reflection, orientation, cutoff, and same-theory invariants; use cumulant expansion, Ward/cusp subtraction, endpoint Taylor expansion, heat-kernel majorants, interval arithmetic, and zero-pairing quotienting as primitives; keep locality to endpoint cells; transfer only through flowed Wilson cumulants; demote on any falsifier. Conceptual value signal: R_{++}/kappa4 becomes a route-deciding finite color-geometric interval certificate, not a symbolic endpoint term.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and interval-calibration experiment.`
- Rationale: The branch is blocked by the size of the connected boundary-OPE polarization, not by abstract OS language. A concrete H,K endpoint-cell experiment tests whether Ward-Hessian suppression can beat Schur-Feshbach leakage in the same Wilson theory.
- Situation seed: Finite SU(2) and SU(3) Wilson lattice YM on a large four-torus with gradient flow, two fixed H,K plus-channel hairpin endpoint boxes, centered renormalized Wilson hairpins, and interval-enclosed sheet currents.
- Varied variable: The endpoint-cell scale ratio theta=eta/d, with a << rho <= sqrt(8t) <= c eta and the H,K geometry held fixed.
- Held-fixed controls: Same Wilson lattice measure, gauge group N, bare-coupling trajectory, gradient-flow definition, and hairpin renormalization counterterms., Same H,K endpoint sheet-current orientation, reflection convention, Schur-Feshbach leakage interval L_+, and non-endpoint lower interval A_+., Same near/far cell partition rule and zero-pairing equivalence policy.
- Expected observation: If the mechanism is real, 2G_{++}^{-} remains order theta^0 in the normalized endpoint units while the Ward-subtracted C4 penalty scales like O(theta^2), producing a nonempty window with zeta_{++}<1. If not, C4 has no theta^2 suppression or the interval width swamps the sign.
- Transfer certificate needed: A regulator-plateau certificate showing the pair lower bound, Ward-Hessian upper bound, cusp subtraction, and sixth-order remainder are uniform in a and L for the same flowed Wilson cumulant before the result may enter the finite Schur-Feshbach proof queue.

## Next Experiment

Build the H,K endpoint-cell table for SU(2) at fixed t,rho,eta: compute interval G_{++}^{-}, verify M_0=M_1=0, estimate H_near^{+} by certified quadrature, bound H_far^{+} by flowed heat-kernel derivatives, and report zeta_{++} with the first falsifier threshold.

# Post-HK A012 quarantine and raw kappa4 interval refit

## Candidate Lemma

Finite Route A endpoint positivity has a valid certificate only after same-regulator shell intervals for the connected four-curvature polarization are supplied. Without A0,A1,A2 and a tail bound in the identical heat-kernel cutoff theory, the post-H,K Wilson collar/hairpin route is quarantined rather than promoted.

## Definitions

- source object: finite-volume heat-kernel regulated SU(N) lattice Yang-Mills measure mu_{a,L,g} on a fixed reflected endpoint box, with Wilson sheets Sigma_i, transported curvature fluxes Phi_i^sigma, and vacuum/perimeter normal ordering.
- target object: the finite Schur-corrected endpoint quadratic form Q_sigma=R_sigma-S_{HK,sigma} on the post-H,K Wilson endpoint subspace; positivity of Q_sigma is only a Route A local gate.
- controlled interface: the sheet-kernel hypergraph recovery map Rec_sigma sends sheet-pair nodes and shell labels to C_sigma, K_{4,sigma}, E_{OPE,sigma}, and S_{HK,sigma}, preserving trace identities and reflection support.
- same-theory condition: all entries use the identical cutoff a, volume L, heat-kernel smearing sigma, coupling g_R, Wilson basis, boundary normalization, and Schur data; no imported continuum or different-regulator intervals are admissible.
- observable manipulated: R_sigma is the connected boundary-OPE polarization cum_2(:tr(Phi_i^2):,:tr(Phi_j^2):), not a symbolic scalar.
- conceptual pressure: mediate actual connected Wilson cumulants to Schur-corrected endpoint positivity without inflating a finite calculation into the Clay theorem.
- declarative tension: Wilson/OPE coefficients, kappa4 negativity, OPE errors, and H,K Schur energy must be valid in one cutoff theory, while OS reconstruction and spectral-transfer claims remain non-claims.

## Assumptions

- Model: compact-gauge finite lattice SU(N) Yang-Mills with heat-kernel plaquette action and reflected endpoint support.
- Cutoff: a,L,sigma,g_R are fixed during the certificate; no continuum, thermodynamic, or regulator-independent inference is made.
- Same-theory: C_sigma, K_{4,sigma}, E_{OPE,sigma}, and S_{HK,sigma} are computed from the same Wilson basis and normalization.
- Validity: the boundary OPE is truncated only with a certified same-regulator tail T_{>2}(sigma).
- Local: the endpoint box, H,K collar/hairpin spaces, and Schur complement are finite dimensional.
- Constraint: vacuum/perimeter normal ordering cancels disconnected Wilson pieces before the connected cumulant is compressed.

## Equations

- transported endpoint flux: `\Phi_i^\sigma=\sum_{p\in\Sigma_i} w_{i,p}\,U_{\gamma_{i,p}}F_p^\sigma U_{\gamma_{i,p}}^{-1}`. Valid when: Valid when heat-kernel smearing is applied on the fixed finite endpoint box and each plaquette curvature is parallel transported to the chosen sheet basepoint.
- connected boundary polarization: `(R_\sigma)_{ij}=\operatorname{cum}_{2,\mu_{a,L,g}}\left(:\operatorname{tr}((\Phi_i^\sigma)^2):,:\operatorname{tr}((\Phi_j^\sigma)^2):\right)`. Valid when: Valid when vacuum/perimeter normal ordering and the same finite cutoff measure are used for both Wilson endpoint observables.
- Gaussian plus kappa4 decomposition: `R_\sigma=\alpha_N g_R^4(C_\sigma\circ C_\sigma)+\frac{g_R^4}{16N^2}K_{4,\sigma}+E_{\mathrm{OPE},\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Requires the boundary OPE in the same heat-kernel regulator, with transported adjoint covariance C_sigma and certified remainder E_OPE,sigma.
- A012 negative envelope: `M_{4,\sigma}^{-,012}\le d_0A_0(\sigma)+d_1A_1(\sigma)+d_2A_2(\sigma)+T_{>2}(\sigma)`. Valid when: Applies only after the sheet-kernel quotient has been audited and same-regulator shell amplitudes dominate the negative spectrum of K4.
- endpoint gate: `\Delta_\sigma^{(012)}=m_G(\sigma)-\frac{g_R^4}{16N^2}M_{4,\sigma}^{-,012}-e_{\mathrm{OPE}}(\sigma)-s_{HK}(\sigma)`. Valid when: Valid when m_G is the least eigenvalue of the Gaussian color square and s_HK is the same-basis Schur hairpin energy.
- certificate implication: `\Delta_\sigma^{(012)}>0\Longrightarrow Q_\sigma=R_\sigma-S_{HK,\sigma}\succeq \Delta_\sigma^{(012)}I`. Valid when: Requires all four terms in Delta_sigma to be certified in the identical finite heat-kernel Wilson truncation.

## Attempted Derivation

- Start with the same-regulator endpoint observables :tr(Phi_i^2): and expand their connected Wilson cumulant after vacuum/perimeter cancellation.
- Separate the crossed Gaussian curvature contractions, giving alpha_N g_R^4(C_sigma o C_sigma), a positive semidefinite Hadamard square with known SU(N) color factor.
- Compress the non-Gaussian connected four-curvature term into K_{4,sigma}; its dangerous contribution is only its negative spectral part after endpoint projection.
- Apply a Schur-Feshbach correction from the already fixed H,K collar/hairpin block, subtracting S_{HK,sigma} in the same Wilson basis.
- Use Gershgorin or row-sum shell envelopes A0,A1,A2 plus T_{>2} to obtain Delta_sigma^(012) as the hard finite gate.
- Audit the carrier: scalar R is too weak, full OS observable density is too strong and circular, and raw plaquette enumeration is exact but fragmented; the sheet-kernel hypergraph remains useful only as an interval carrier.

Blocking gap: No certified same-regulator intervals for A0,A1,A2,T_{>2}, and e_OPE are available, and no quotient-invariance audit has been completed.

## Falsifiers

- falsifier: a same-regulator certified interval with inf Delta_sigma^(012)<=0 demotes the H,K collar/hairpin endpoint route.
- falsifier: quotient averaging that reduces the K4 row envelope below the raw plaquette-sheet row sum invalidates the sheet-kernel compression.
- falsifier: an OPE tail T_{>2}(sigma) larger than the Gaussian margin keeps the finite endpoint gate closed.
- falsifier: computing R_sigma and S_HK with different cutoffs, couplings, Wilson bases, or boundary normalizations breaks the same-theory condition.
- Stress case: opposite-orientation sheets have canceling averaged K4 entries but nonzero absolute row sums, so a naive quotient certificate is invalid.

## Learning

Conceptual pressure attacked: mediate actual connected Wilson cumulants to Schur-corrected positivity without overclaiming Clay. Hard gate: Delta_sigma^(012) changes the proof state only by promoting or killing finite endpoint-box positivity for this H,K geometry. Conceptual value signal: the cycle is sharp because it turns repeated A012 aspiration into an admissibility theorem and quarantine criterion; the next valid move is raw plaquette interval proof search, not another OS-density or symbolic R restatement.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search calibrator, not as evidence for the Clay theorem.`
- Rationale: The branch has exhausted abstraction-only A012 consolidation; the live mathematical pressure is whether a same-regulator kappa4 shell envelope can beat the Schur hairpin energy in a concrete finite endpoint box.
- Situation seed: Finite SU(N) heat-kernel lattice endpoint box with the fixed post-H,K Wilson collar/hairpin sheets, raw plaquette-sheet nodes, and normal-ordered curvature-flux observables :tr(Phi_i^2):.
- Varied variable: The smearing-to-lattice ratio sigma/a, varied over a small discrete set while keeping the endpoint geometry fixed.
- Held-fixed controls: The cutoff a, volume L, coupling g_R, gauge group SU(N), Wilson sheet basis, and reflected endpoint support are fixed within each trial., The H,K Schur matrix S_HK, boundary normalization, shell quotient policy, and vacuum/perimeter normal ordering are held fixed., No continuum extrapolation, OS spectral transfer, or observable-density assumption is allowed to enter the observation.
- Expected observation: Either a window appears where the Gaussian minimum m_G(sigma) dominates certified kappa4, OPE, and Schur costs, or every tested sigma/a gives a negative or uncertified Delta interval, demoting this finite route.
- Transfer certificate needed: Before intuition affects proof obligations, produce outward-rounded same-regulator intervals for A0,A1,A2,T_{>2}, e_OPE, m_G, and s_HK, plus a quotient-invariance audit comparing compressed and raw row sums.

## Next Experiment

Run a raw plaquette-sheet interval audit for shell 0 first: compute the heat-kernel connected four-curvature cumulant with transported color tensors, compare raw and quotient row sums, then update Delta_sigma^(012) with outward-rounded intervals.

