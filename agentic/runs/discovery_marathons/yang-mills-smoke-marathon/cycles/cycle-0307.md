# cycle-0307

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint source leakage certificate for the post-H,K Wilson gate

## Candidate Lemma

Finite endpoint leakage certificate: for the fixed three-hairpin post-H,K block, heat-kernel endpoint source classes give a valid scalar interval whose positive lower endpoint promotes the finite reflected-Wilson OS gate, and whose negative upper endpoint is a same-theory falsifier.

## Definitions

- source object: heat-kernel plaquette-sheet endpoint carrier C_ep(a,L,delta), consisting of source-equivalence classes v, seven values log Z_v(ell h L_v), cumulant intervals kappa_v, fractional incidences b_{ij,v}, beta_v, color factor C_N, Gaussian margin M_G, and tail T_tail.
- target object: the finite post-H,K Schur-Feshbach scalar for the locked reflected Wilson three-hairpin block, before continuum OS reconstruction and before any Hamiltonian spectral-transfer claim.
- controlled interface: source differentiation, source-equivalence aggregation, signed incidence contraction, color multiplication, clipping by [D_v]_+, tail addition, and export of one interval [I_-,I_+] to the finite OS gate.
- same-theory condition: all Z_v and incidences are computed in the same heat-kernel lattice Yang-Mills regulator, with the same Wilson-loop normalization, same gauge-invariant observable algebra, no boundary counterterm, and cutoff-uniform endpoint remainders.

## Assumptions

- Model: SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflected Wilson hairpin collars collapsed only after the regulated source calculation.
- Regime: fixed finite endpoint boxes after the H,K Feshbach reduction, with small source step h and endpoint scale t_v inside the coordinate chart used for the Haar-Jacobian expansion.
- Uniformity: cumulant remainder and T_tail are bounded uniformly in the collar parameter and in the lattice cutoff along the finite block under study.
- Same-theory: source-equivalent endpoints may be merged only when their regulated source derivatives agree, and signed incidences are summed before multiplying by kappa_v.
- Validity: the finite claim concerns only this post-H,K Wilson block; it does not assert continuum existence, full OS positivity, nontriviality, or a mass gap.

## Equations

- endpoint incidence leakage: `D_v=2b_{12,v}-4b_{13,v}-4b_{23,v},\qquad [D_v]_+=\max(D_v,0)`. Valid when: Valid when b_{ij,v} are the source-equivalence aggregated fractional endpoint incidences for the locked three-hairpin null channel.
- seven point connected cumulant stencil: `\widehat\kappa_v(h)=h^{-4}\sum_{\ell=-3}^{3}c_\ell\log Z_v(\ell hL_v),\quad (c_{-3},\ldots,c_3)=(-1,12,-39,56,-39,12,-1)/6`. Valid when: Applies when log Z_v is the same-theory endpoint source partition function analytic on the seven-point source segment.
- stencil error interval: `|\widehat\kappa_v(h)-\partial_s^4\log Z_v(sL_v)|_{s=0}|\le 7h^4M_{8,v}/240`. Valid when: Requires a cutoff-uniform eighth source-derivative bound on the endpoint box throughout the seven-point stencil interval.
- safe lower gate certificate: `I_- = M_G^- - C_N^+\sum_v \beta_v^+[D_v]_+A_v^+ - T_{\rm tail}^+`. Valid when: Valid when A_v^+ bounds the magnitude of the negative connected endpoint cumulant and all protective D_v<=0 classes are discarded only for a lower bound.

## Attempted Derivation

- Attack conceptual pressure: endpoint collapse must be sign-certified in the same Wilson theory, not hidden inside symbolic R or a raw kappa_4 spectrum.
- Use the heat-kernel plaquette-sheet regulator and write endpoint source classes v by regulated source data; this makes the source object meaningful independently of the target scalar.
- Take connected log source derivatives of log Z_v; the connected log removes Wick-square Gram pieces, and the already established null incidence cancels the straight nonabelian f f contact.
- Expand the endpoint Haar factor in local SU(N) coordinates; the first non-Gaussian same-theory contribution is the negative root-quartic term -(t_v^4/60)R_4(L_v) plus E_v.
- Contract only after source-equivalence aggregation: the finite scalar receives C_N sum_v beta_v D_v kappa_v plus T_tail, so negative kappa_v lowers the gate only when D_v>0.
- Use R_4(L)<= (N+3)||L||_{HS}^4 to obtain a computable lower interval I_- without needing every source value, while the seven-point stencil supplies a sharper validator-facing connected cumulant witness when data are available.
- Hard gate: the finite post-H,K reflected-Wilson OS transfer gate. Success gives a finite same-theory promotion certificate for this block; failure gives a concrete finite falsifier. It does not touch continuum construction, OS/Wightman reconstruction, nontriviality, or the Hamiltonian mass gap.

Blocking gap: The proof still needs either actual seven-point endpoint source intervals for all positive-D classes or a cutoff-uniform bound on E_v and T_tail sharp enough to keep I_->0.

## Falsifiers

- A same-theory positive-D endpoint class has a certified negative cumulant interval large enough that I_+<0; this is the targeted finite falsifier.
- The endpoint eighth-derivative or tail bound grows with the cutoff, so the interval carrier is not valid for the intended cutoff passage.
- Source-equivalence compression merges geometrically similar endpoints with unequal regulated source derivatives, destroying the null-channel cancellation.
- A boundary counterterm or endpoint renormalization is required to define Z_v, violating the same-theory condition.
- Endpoint sources leave the local heat-kernel chart, invalidating the root-quartic estimate and forcing quarantine or a different regulator calculation.

## Learning

Conceptual pressure attacked: endpoint collapse must be made sign-certifiable in the same Wilson theory. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold without adding a boundary theory, but H,K and the half-overlap shield alone do not determine the post-H,K scalar. Carrier audit: raw R is representation-limited; raw kappa_4 spectra are too strong because negative kappa_4 is harmless when D_v<=0; global Schur-preimage positivity is valid but too coarse after H,K. Efficient representation C_ep encodes source classes, seven source values, cumulant intervals, fractional incidences, C_N, M_G, and T_tail; preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; uses source differentiation, interval arithmetic, source-equivalence, color multiplication, clipping, incidence contraction, and tail addition; equivalence is equality of regulated source data; locality cost is charged to T_tail; transfer interface is [I_-,I_+]; falsifiers are negative interval, nonuniform tail, or boundary counterterm. Conceptual value signal: sharp finite route change, because the obstruction is positive-D endpoint leakage plus uncontrolled tail, not negative SU(N) root-quartic cumulants themselves.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and validator-facing endpoint-data experiment.`
- Rationale: The branch has exhausted abstract OS closed-cone and H,K threshold work; the decisive finite gate depends on actual connected endpoint cumulant witness intervals and signed incidences.
- Situation seed: Heat-kernel SU(N) plaquette-sheet endpoint-box family for the fixed three reflected Wilson hairpins after H,K, with source classes v and scalar endpoint gate interval [I_-,I_+].
- Varied variable: Fractional leakage eta_v=(b_{13,v}+b_{23,v})/b_{12,v} for endpoint classes with fixed source norm and fixed heat-kernel scale.
- Held-fixed controls: Same heat-kernel Wilson action and same gauge-invariant Wilson observable algebra., Fixed H,K null-channel weights and fixed color normalization C_N., No boundary counterterm and cutoff-uniform source derivative/tail budget., Fixed endpoint source-equivalence policy: equality of regulated source data only.
- Expected observation: For eta_v>=1/2, negative root-quartic cumulants are protective or neutral; for eta_v<1/2, the gate can be demoted only if the certified connected cumulant magnitude plus tail exceeds the Gaussian margin.
- Transfer certificate needed: A cutoff-uniform endpoint source interval theorem or seven-point source table proving the exported [I_-,I_+] is computed in the same theory and is valid for the finite OS Schur-Feshbach gate.

## Next Experiment

Proof search and endpoint data: compute the seven log Z_v(ell hL_v) values or root-quartic remainder bounds for all positive-D endpoint classes in the heat-kernel SU(N) plaquette-sheet regulator, then run the connected cumulant witness interval test I_->0 or I_+<0.

# Gauge-Invariant Nontriviality Witness Selection -> finite endpoint R certificate

## Candidate Lemma

Finite Ward-Hessian endpoint certificate: for fixed H,K plus-channel hairpin sheets, the renormalized endpoint polarization R_{++} is bounded below by a positive flowed pair contraction minus explicit connected C4 sector Hessian constants and recovery errors. This is a finite Route A statement only.

## Definitions

- source object: the centered flowed Wilson hairpin covariance R_{++}^{ren}(t,a,eta)=kappa_2(:W_+^i(t)::W_+^j(t):) on a finite SU(N) Wilson lattice with gradient-flow regulator and boundary point-splitting.
- target object: the finite endpoint-box Schur-Feshbach scalar Q_+=P_+-L_++R_{++}^{ren} controlling the post-H,K plus channel in one reflected Wilson collar instance.
- controlled interface: endpoint sheet-current recovery map Phi_{eta,t} sending each thin hairpin to signed endpoint cell currents, preserving gauge trace, color contraction, reflection parity, and orientation.
- same-theory condition: the Wilson loops, flow map, counterterms, centered cumulants, endpoint currents, and Schur-Feshbach matrix entries are all computed from the same finite cutoff measure before any continuum or OS spectral-transfer claim.
- Sector set S4={3g,4g,ct,end} denotes one-loop three-gluon, four-gluon, counterterm, and endpoint/cusp sectors of the connected four-curvature kernel after disconnected-product removal.
- M_{2,+} is the certified second endpoint moment of the plus-channel current after monopole and dipole cancellation.
- H_s^+(rho,t,a) is an outward-rounded near/far interval upper bound for the Hessian seminorm of the Ward-subtracted sector kernel K_s^t on the endpoint cell product.

## Assumptions

- Model: finite four-dimensional hypercubic lattice SU(N), Wilson action, fixed lattice spacing a>0, fixed finite volume, and gradient flow time t>0.
- Regime: endpoint cell diameter eta satisfies eta<rho/4 and rho<=sqrt(8t), so Taylor cells are separated before the far heat-kernel estimate is invoked.
- Cutoff: all constants are cutoff-dependent finite numbers; no continuum limit, volume-uniform basin entry, or large-field/topology summability is claimed.
- Same-theory: the same flowed lattice measure supplies the pair contraction, connected C4 kernel, cusp counterterm, endpoint recovery map, and Feshbach leakage L_+.
- Validity: Ward subtraction, one-hairpin perimeter/cusp cancellation, and plus-channel monopole/dipole cancellation are separately interval-checked.
- Local: the claim changes only finite endpoint-box positivity after H,K and leaves Clay existence, OS/Wightman reconstruction, nontrivial continuum limit, and Hamiltonian mass gap untouched.

## Equations

- renormalized endpoint cumulant: `R_{++}^{ren}(t,a,\eta)=\kappa_2\big(:W_+^i(t):,:W_+^j(t):\big)`. Valid when: Valid when the centered flowed Wilson hairpins are renormalized by the same perimeter, cusp, and disconnected-product subtractions in the finite cutoff theory.
- pair baseline: `R_{pair,++}=2g_t^4\,(N^2-1)\,G_{++}^{ij}(t,a,\eta)`. Valid when: Applies after diagonal color normalization and after the two flowed curvature cross-pairings between the plus hairpins are the only Gaussian contractions retained.
- connected sector decomposition: `R_{C4,++}=g_t^4 N(N^2-1)\sum_{s\in S_4} I_{s,++}(t,a,\eta)+E_{rec}`. Valid when: Requires the same-theory boundary OPE expansion, Ward-subtracted sector kernels, and endpoint recovery errors for the fixed H,K hairpin geometry.
- Ward-Hessian sector majorant: `|I_{s,++}|\le H_s^+(\rho,t,a)\,M_{2,+}^2+E_{s,Taylor}^+(\eta,\rho,t,a)`. Valid when: Valid when the plus endpoint current has certified zero monopole and dipole moments and the sector kernel is Hessian-bounded on each near and far interval cell.
- lower interval certificate: `R_{++}^{ren}\ge g_t^4(N^2-1)\left(2G_{++}^{ij,-}-N\sum_{s\in S_4}H_s^{+}(\rho,t,a)M_{2,+}^2\right)-E_{rec}^+-E_T^+`. Valid when: Applies after outward-rounded interval arithmetic supplies lower pair bounds and upper connected-sector, recovery, and Taylor-remainder bounds for the same finite cells.
- Route A promotion inequality: `g_t^4(N^2-1)\left(2G_{++}^{ij,-}-N\sum_{s\in S_4}H_s^{+}M_{2,+}^2\right)-E_{rec}^+-E_T^+>L_+-P_+`. Valid when: Valid as a finite endpoint-box positivity test once L_+ and P_+ are the Schur-Feshbach leakage and pre-R plus-channel term from the same H,K matrix.

## Attempted Derivation

- Attacked conceptual pressure: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, while positive flowed pair covariance can be erased by connected C4 polarization.
- Expanded each centered thin hairpin through the flowed curvature sheet integral and subtracted disconnected products plus one-hairpin perimeter/cusp terms.
- Computed the Gaussian cross-pair contribution: two reflected cross-pairings give color factor 2(N^2-1) and positive geometry G_{++}^{ij}.
- Decomposed the remaining connected boundary-OPE polarization into sectors S4={3g,4g,ct,end} with common color factor N(N^2-1), plus explicit recovery error.
- Used Ward subtraction and plus-channel monopole/dipole cancellation to remove constant and linear endpoint Taylor terms in each sector kernel.
- Applied a near/far split: near cells use flowed heat-kernel majorants after cusp cancellation; far cells use Hessian sup intervals for the Ward-subtracted sector kernels.
- Obtained the lower interval R_{++}^{ren,-}=g_t^4(N^2-1)(2G_{++}^{-}-N sum_s H_s^+ M_{2,+}^2)-E_rec^+-E_T^+.
- Compared this lower interval to the finite Schur-Feshbach leakage threshold L_+-P_+; success promotes finite endpoint-box positivity after H,K, failure quarantines the R repair.

Blocking gap: The sector constants H_{3g}^+, H_{4g}^+, H_{ct}^+, and H_{end}^+ still need outward-rounded evaluation for the concrete H,K endpoint geometry; without those numbers the inequality is a valid proof obligation but not a proof.

## Falsifiers

- Ward residual falsifier: the endpoint-current moments fail M_{0,+}=M_{1,+}=0 after recovery, so Hessian suppression is invalid.
- Cusp falsifier: one-hairpin perimeter/cusp subtraction is not stable under the chosen gradient-flow and point-splitting regulator.
- Dominance falsifier: N sum_s H_s^+ M_{2,+}^2 exceeds 2G_{++}^{-} for every valid rho and eta window.
- Same-theory falsifier: the pair baseline and C4 sector kernels are computed using different regulators, counterterms, or limiting families.
- Interval falsifier: outward-rounded sector intervals plateau under refinement and cannot decide the promotion inequality.
- Geometry falsifier: the plus-channel endpoint orientation makes G_{++}^{ij,-}=0 or too small, so the positive pair baseline cannot support the route.

## Learning

Declarative tension: Schur-Feshbach endpoint positivity, positive flowed Wilson pair covariance, and same-theory renormalized cumulants must jointly be valid, but connected C4 can erase the pair term unless Ward-Hessian constants and recovery errors are certified. Carrier critique: raw Wilson contours are too fragmented; a global OS spectral-transfer route or non-Gaussian Schwinger family route is too coarse for this local obstruction. Efficient representation requirements are now explicit: encode H,K sheets, endpoint currents, cell moments, sector kernels, counterterms, and recovery errors; preserve gauge, color, reflection, orientation, cutoff, locality, and same-theory identity; use cumulant expansion, Ward/cusp subtraction, endpoint Taylor remainders, heat-kernel majorants, interval quadrature, outward rounding, and certified zero-pairing quotienting; keep locality to finite endpoint cells with bounded refinement; transfer only through centered flowed Wilson cumulants; demote on Ward, cusp, same-theory, geometry, dominance, or interval-width falsifier. Hard gate: finite endpoint-box positivity after H,K. Conceptual value signal: R_{++}/kappa_4 is now a route-deciding color-geometric lower interval with an explicit sign/size promotion test, not a symbolic threshold. Success promotes one finite Route A gate; failure quarantines the R repair while preserving all Clay target commitments.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and proof-search guide.`
- Rationale: The branch has already named the R carrier; the missing information is whether the Ward-Hessian sector constants can be small enough in an actual H,K endpoint geometry to beat Schur-Feshbach leakage.
- Situation seed: Finite SU(2) Wilson lattice on a large four-torus, fixed reflected H,K plus-channel hairpin endpoint boxes, gradient-flow time t, centered flowed Wilson cumulant R_{++}^{ren}, and outward-rounded sector-kernel quadrature for S4={3g,4g,ct,end}.
- Varied variable: The near/far split lambda=rho/sqrt(t), with eta/t^{1/2}, H,K geometry, and flow normalization held fixed.
- Held-fixed controls: Same finite lattice Wilson measure and the same flowed Wilson loops for pair and connected C4 terms., Fixed H,K endpoint sheet currents, reflection parity, orientation, color normalization, and Schur-Feshbach leakage L_+., Fixed Ward/cusp subtraction convention and endpoint-current recovery map Phi_{eta,t}., No continuum extrapolation, no OS spectral-transfer inference, and no change of regulator during the comparison.
- Expected observation: A useful route shows a lambda-window where 2G_{++}^{-}-N sum_s H_s^+M_{2,+}^2 stays positive and the full lower interval beats L_+-P_+; otherwise C4 dominance or interval plateau demotes the endpoint repair.
- Transfer certificate needed: Before intuition affects proof obligations, the calculation needs a validator-facing interval file or hand-checkable table giving G_{++}^{-}, every H_s^+, Ward and cusp residuals, recovery error, rounding mode, and the exact finite H,K Schur-Feshbach inputs.

## Next Experiment

Route to proof search: build the validator-facing sector-constant table for the fixed H,K endpoint geometry, using the connected cumulant witness R_{++}^{ren} as a finite same-theory nontriviality witness support object while explicitly separating it from continuum OS spectral-transfer hypotheses.

# Raw K4 phase-stress gate for the post-H,K endpoint box

## Candidate Lemma

If three same-regulator endpoint intervals give A_p^+>=U_pp, C_q^+>=U_qq>0, and L_pq(theta)<=Re(e^{-i theta}U_pq) with tau_pq(theta)=A_p^+-L_pq(theta)^2/C_q^+<0, then the Schur-corrected endpoint block U_sigma is not positive semidefinite. This is a finite Route A falsifier, not a Clay mass-gap claim.

## Definitions

- source object: finite heat-kernel SU(N) Wilson plaquette ensemble with endpoint sheet observables Q_i and rigorous intervals for raw connected four-curvature cumulants.
- target object: the finite Schur-corrected endpoint Hermitian matrix U_sigma on span{e_i} after the worked H,K collar/hairpin elimination.
- controlled interface: raw connected Wilson cumulant intervals are mapped to R_sigma, then to U_sigma=R_sigma-S_HK with tracked OPE and Schur errors.
- same-theory condition: same lattice cutoff a, heat-kernel width sigma, coupling g_R, Wilson basis, reflection convention, endpoint boxes, and H,K Schur blocks for all intervals.
- carrier observable: Q_i is the vacuum-subtracted quadratic transported plaquette-flux observable attached to endpoint sheet i.
- hard gate: tau_pq(theta)<0 demotes the finite H,K endpoint route; survival of all tested pairs forces full Delta_raw PSD proof search.

## Assumptions

- Model: finite four-dimensional Euclidean lattice SU(N), N>=2, heat-kernel plaquette regulator, fixed volume, fixed cutoff a, and fixed sigma/a.
- Regime: endpoint boxes are the post-H,K collar/hairpin boxes and all plaquette sheets lie in the reflection-positive half-space used by the finite construction.
- Cutoff: no continuum limit, volume limit, OS reconstruction, or spectral transfer is used in this lemma.
- Same-theory: Gaussian covariance, K4 cumulant intervals, OPE error intervals, and S_HK are computed from the identical regulated Wilson measure and endpoint basis.
- Validity: interval endpoints are rigorous outward-rounded bounds after exact Wilson trace quotienting and normal-ordering subtraction.
- Local: the finite endpoint compression is the only target gate changed by the lemma; gauge-invariant observable density and Clay mass gap remain untouched.

## Equations

- endpoint_observable: `\Phi_{\pi}^{a,\sigma}=a^2\int h_{\sigma}(x_{\pi}-y)\,\mathrm{Ad}_{T_{\pi\leftarrow y}}^{ab}F_{\mu\nu}^b(y)\,dy,\qquad Q_i=\sum_{\pi,\pi'\in\Sigma_i}w_{i;\pi\pi'}:\Phi_{\pi}^{a,\sigma}\Phi_{\pi'}^{a,\sigma}:`. Valid when: Valid when the heat-kernel transported plaquette expansion is used at fixed cutoff with the endpoint sheet weights and normal-ordering convention specified.
- connected_boundary_polarization: `R_{ij,\sigma}=\operatorname{cum}_2(Q_i,Q_j)=R^G_{ij,\sigma}+\frac{g_R^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma}`. Valid when: Valid when disconnected vacuum and perimeter terms are cancelled by normal ordering and by the connected cumulant in the same regulated Wilson ensemble.
- gaussian_color_square: `R^G_{ij,\sigma}=\alpha_N g_R^4\sum_{\pi,\pi',\rho,\rho'}w_{i;\pi\pi'}\overline{w_{j;\rho\rho'}}\big(C_\sigma(\pi,\rho)C_\sigma(\pi',\rho')+C_\sigma(\pi,\rho')C_\sigma(\pi',\rho)\big),\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after diagonal color normalization in the fundamental SU(N) Wilson trace and before adding the connected four-curvature cumulant interval.
- schur_corrected_endpoint_matrix: `U_{ij,\sigma}=R_{ij,\sigma}-S^{HK}_{ij,\sigma},\qquad S^{HK}_{\sigma}=B_{\sigma}^*E_{\sigma}^{-1}B_{\sigma}`. Valid when: Requires the H,K hairpin block E_sigma to be positive on the eliminated finite subspace with the same endpoint basis and regulator.
- phase_stress_certificate: `L_{pq}(\theta)=\underline{\operatorname{Re}(e^{-i\theta}U_{pq,\sigma})},\quad A_p^+=\overline{U_{pp,\sigma}},\quad C_q^+=\overline{U_{qq,\sigma}},\quad \tau_{pq}(\theta)=A_p^+-\frac{L_{pq}(\theta)^2}{C_q^+}`. Valid when: Valid when C_q^+ is positive and the three interval bounds enclose the same Schur-corrected endpoint entries with a common phase convention.
- negative_rayleigh_recovery: `\tau_{pq}(\theta)<0\ \Longrightarrow\ \exists x=e_p-t e^{-i\theta}e_q:\ x^*U_\sigma x<0,\quad t=L_{pq}(\theta)/C_q^+`. Valid when: Valid when the Hermitian two-by-two compression is evaluated using the same interval enclosure and the off-diagonal phase lower bound is certified.

## Attempted Derivation

- Attack conceptual pressure: turn the connected boundary-OPE polarization R into a route-deciding finite witness instead of another symbolic R or OS-density restatement.
- Write R_ij as cum_2(Q_i,Q_j) in the heat-kernel lattice regulator; normal ordering and connected cumulant remove vacuum/perimeter disconnected terms.
- Decompose R into the positive Gaussian color square, the dangerous raw connected K4 interval, and the OPE remainder, all in the same Wilson ensemble.
- Subtract the finite H,K Schur energy S_HK=B^*E^{-1}B to obtain U_sigma on the endpoint box.
- Compress U_sigma to span{e_p,e_q}; for x=e_p-t e^{-i theta}e_q, compute x^*Ux=U_pp-2t Re(e^{-i theta}U_pq)+t^2 U_qq.
- Replace U_pp and U_qq by certified upper intervals and the phased off-diagonal by a certified lower interval; minimize the upper Rayleigh bound at t=L/C.
- Obtain the falsifier condition tau=A-L^2/C<0, which proves non-PSD of the finite endpoint block.

Blocking gap: The missing proof object is not the Schur algebra but the same-regulator raw K4 interval triple for U_pp, U_qq, and Re(e^{-i theta}U_pq), including OPE and quotient audits.

## Falsifiers

- falsifier: tau_pq(theta)<0 with certified same-regulator intervals gives a negative Rayleigh vector and demotes the worked H,K endpoint route.
- A regulator mismatch between K4, Gaussian covariance, OPE remainder, and S_HK invalidates any apparent negative margin.
- If exact Wilson quotienting changes the interval sign or multiplicity, the connected cumulant witness is not valid.
- If all phase sectors satisfy tau>=0 but Delta_raw is still not positive, the two-sparse tactic is incomplete and must be demoted to full matrix proof search.
- If the OPE interval is as large as the Gaussian-Schur margin, no finite Route A promotion is allowed.

## Learning

Conceptual pressure attacked: mediate the connected boundary-OPE polarization R to finite Schur-corrected endpoint positivity without inflating a Wilson calculation into the Clay theorem. Declarative tension: Wilson/OPE coefficients, raw connected K4 negativity, OPE errors, and H,K Schur energy must be valid in one cutoff theory, while OS reconstruction, gauge-invariant observable density, nontrivial continuum YM, and Hamiltonian mass gap remain non-claims. Carrier critique: scalar R is representation-limited, OS Hilbert observable algebra is too strong and circular for this local gate, A012 shells are convenient but quarantined, and raw plaquette enumeration is fragmented yet valid. Compared with full Delta_raw PSD search, the phase-stress route is a sharper negative tactic because three endpoint intervals can falsify the route. Efficient representation requirements: encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/K4 separation, endpoint compression, same-theory normalization, and exact Wilson quotienting; support cumulant contraction, interval summation, phase certification, Rayleigh stress search, Loewner bounds, and Schur subtraction; quotient only by exact Wilson identities; keep finite endpoint-box complexity; transfer only through Delta_raw or x_stress; falsifier triggers are negative margin, missing intervals, non-invariant quotienting, or regulator mismatch. Conceptual value signal: sharp and route-changing at finite scope because R is a connected cumulant witness with explicit color, geometry, non-Gaussian K4, OPE, and Schur data in one valid inequality.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch has exhausted abstraction around R; a concrete finite Wilson thought experiment can decide whether three raw K4 intervals can falsify endpoint positivity before full Delta_raw proof search.
- Situation seed: Fixed SU(N) heat-kernel lattice H,K collar/hairpin endpoint box with two endpoint sheets p,q; evaluate the connected cumulant witness cum_2(Q_p,Q_q) after vacuum/perimeter cancellation and Schur subtraction.
- Varied variable: phase sector theta used to align Re(e^{-i theta}K^{(4)}_{pq,sigma}) in the two-sparse Rayleigh stress vector.
- Held-fixed controls: same cutoff a, heat-kernel width sigma, coupling g_R, finite volume, and Wilson action, same endpoint plaquette sheets, weights, transporters, reflection half-space, and H,K Schur blocks, same OPE truncation order, interval arithmetic convention, and exact Wilson quotient policy
- Expected observation: A narrow phase window either produces L_pq(theta)^2>A_p^+C_q^+ and hence a valid negative stress falsifier, or shows that two-sparse stress cannot beat the Gaussian plus Schur diagonal margins.
- Transfer certificate needed: Rigorous same-regulator intervals for the phased off-diagonal raw K4 entry, both diagonal entries, OPE remainders, and Schur block entries, with a quotient-invariance audit before the intuition affects proof obligations.

## Next Experiment

Run proof search for one same-theory raw K4 phase interval triple: choose endpoint pair p,q, compute K4_pp, K4_qq, Re(e^{-i theta}K4_pq), add Gaussian/OPE/Schur intervals, and test tau_pq(theta)<0; marker: connected cumulant witness, with gauge-invariant observable density explicitly quarantined.

