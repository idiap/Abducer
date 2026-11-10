# cycle-0285

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: endpoint-source interval gate

## Candidate Lemma

Fractional endpoint shield theorem: for the heat-kernel plaquette-sheet three-hairpin block after the H,K Schur-Feshbach reduction, a box v whose protective overlap satisfies b13(v)+b23(v) >= b12(v)/2 cannot contribute a negative compact-group fourth-cumulant endpoint term to the null-channel scalar. Hence only certified positive D_v=2b12-4b13-4b23 boxes, plus tail, can demote the finite same-theory OS gate.

## Definitions

- source object: finite-cutoff SU(N) heat-kernel plaquette-sheet Wilson endpoint data C_ep(a,L) consisting of endpoint boxes v, seven source values log Z_v(rhL_v), fourth-cumulant intervals beta_v, fractional incidence intervals b_ij(v), color factor C_N, Gaussian margin M_G, and tail T_tail.
- target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for the locked three-hairpin block with Feshbach null vector, not the continuum Schwinger family and not the mass gap.
- controlled interface: the carrier map C_ep -> [I_-,I_+] obtained by connected source differentiation, null-incidence contraction, color multiplication, clipping of dangerous D_v>0 boxes, and tail addition.
- same-theory condition: the endpoint sources are inserted in the original heat-kernel Wilson action and normalized Wilson loops with no boundary counterterm, no algebra enlargement, and no change of gauge-invariant observable identification.
- endpoint dominance: D_v=2b12(v)-4b13(v)-4b23(v), with b_ij(v) the fractional endpoint share of the reflected Wilson pair ij in box v.
- dangerous cumulant: beta_v is the singlet connected fourth source derivative of log Z_v; in the compact endpoint small-box regime its leading Haar-Jacobian contribution is nonpositive.

## Assumptions

- Model: four-dimensional finite-volume SU(N) lattice Yang-Mills with heat-kernel plaquette action and gauge-invariant Wilson plaquette-sheet observables.
- Regime: the H,K three-hairpin block and its Schur-Feshbach null channel have already been fixed; only the endpoint R/kappa_4 term is being bounded.
- Cutoff: endpoint boxes obey a << ell_v << fixed collar scale, and the finite-difference source step h lies inside a common analyticity radius for log Z_v.
- Uniformity: beta_v intervals, fractional incidence intervals, and T_tail are bounded uniformly in the finite cutoff window used for this finite theorem.
- Same-theory: the same Wilson normalization and the same endpoint source derivative define both the collar data and the target endpoint limit; boundary counterterms are forbidden.
- Validity: connected log-source derivatives remove Wick-square Gaussian pieces, and the straight C_A f f contact has already canceled by the null-incidence identity.
- Local: all non-endpoint overlap, corner leakage, and partition errors not assigned to a box are charged to T_tail.

## Equations

- seven-point endpoint fourth cumulant interval: `\widehat\beta_v(h)=\frac{-\ell_v(-3h)+12\ell_v(-2h)-39\ell_v(-h)+56\ell_v(0)-39\ell_v(h)+12\ell_v(2h)-\ell_v(3h)}{6h^4},\quad \ell_v(s)=\log Z_v(sL_v),\quad \beta_v\in[\widehat\beta_v-\varepsilon_v,\widehat\beta_v+\varepsilon_v],\ \varepsilon_v\le 7h^4M_{8,v}/240`. Valid when: Valid when the endpoint source partition is fixed, log Z_v is eight-times differentiable in the stated heat-kernel source radius, and the same Wilson action supplies all seven source evaluations.
- fractional half-overlap shield: `D_v=2b_{12}(v)-4b_{13}(v)-4b_{23}(v)=2\bigl(b_{12}(v)-2b_{13}(v)-2b_{23}(v)\bigr),\quad D_v\le0\Longleftrightarrow b_{13}(v)+b_{23}(v)\ge b_{12}(v)/2`. Valid when: Valid when b_ij(v) are measured by the same endpoint partition of unity and the Feshbach null weights of the three-hairpin block are fixed.
- dangerous clipped lower gate: `I_{\rm gate}\ge \underline I_{\rm gate}:=M_G+C_N\sum_v \beta_v^-\,[D_v^+]_+ -T_{\rm tail},\quad C_N=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Valid when beta_v intervals are certified nonpositive, D_v^+ bounds the upper endpoint dominance in each box, and all unlocalized endpoint or corner contributions are included in T_tail.
- finite promotion and falsifier test: `\underline I_{\rm gate}>0\Rightarrow \text{finite post-H,K block promoted},\qquad \overline I_{\rm gate}<0\Rightarrow \text{same-theory finite falsifier}`. Valid when: Valid when [I_-,I_+] is computed by full interval arithmetic from the same C_ep carrier, including source errors, incidence errors, color factors, and tail bounds.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: finite-cutoff SU(N) heat-kernel plaquette-sheet Wilson endpoint data C_ep(a,L) consisting of endpoint boxes v, seven source values log Z_v(rhL_v), fourth-cumulant intervals beta_v, fractional incidence intervals b_ij(v), color factor C_N, Gaussian margin M_G, and tail T_tail.; target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for the locked three-hairpin block with Feshbach null vector, not the continuum Schwinger family and not the mass gap.; Model: four-dimensional finite-volume SU(N) lattice Yang-Mills with heat-kernel plaquette action and gauge-invariant Wilson plaquette-sheet observables..
- Conceptual pressure attacked: endpoint collapse must be sign-certified in the same Wilson theory while finite collar OS positivity and fixed gauge-invariant observables are preserved.
- Declarative tension: collar reflection positivity gives a finite positive matrix, but the endpoint boundary OPE can add a connected R term; raw R is too weak because it hides incidence, and raw kappa_4 is too strong because negative kappa_4 is harmless unless multiplied by positive endpoint dominance.
- Freeze the source: use the heat-kernel plaquette-sheet regulator and define beta_v by the fourth derivative of log Z_v(sL_v) from seven same-theory source evaluations.
- Use the connected logarithm to remove Wick-square/Gaussian contractions and use the previously isolated null-incidence identity to cancel the straight nonabelian C_A f f contact.
- Contract the remaining endpoint cumulant with the three-hairpin null-channel weights, giving the scalar local factor beta_v D_v with D_v=2b12-4b13-4b23.
- Derive the half-overlap shield: for beta_v<=0, any box with b13+b23>=b12/2 has D_v<=0 and therefore cannot lower the OS gate; the only dangerous boxes have certified 12-dominance D_v>0.
- Transfer the finite endpoint data to the OS gate through the clipped lower interval M_G+C_N sum beta_v^- [D_v^+]_+ - T_tail.

Blocking gap: The branch still lacks certified fractional incidence intervals b_ij(v), same-theory source intervals beta_v, and a cutoff-uniform T_tail for the actual endpoint geometry.

## Falsifiers

- A valid endpoint source computation with D_v^+>0 and beta_v^-<0 large enough to make the full I_gate interval negative is a finite same-theory falsifier.
- The seven-point source stencil fails cutoff-uniform analyticity or requires a boundary counterterm at t=0.
- Endpoint partitions cannot make the residual corner and overlap contribution T_tail smaller than the Gaussian margin M_G.
- Fractional incidences are not stable under refinement of the plaquette-sheet partition, so the half-overlap shield is regulator-artificial.
- A same-theory Wilson source derivative gives a positive fourth cumulant in the dangerous channel, invalidating the compact-group sign assumption used for clipping.
- The fixed Wilson observable algebra changes during endpoint collapse; then any positivity transfer is valid only for a different boundary theory.

## Learning

Cycle 285 attacks the conceptual pressure of endpoint collapse in the same Wilson theory. The declarative tension is finite collar OS positivity plus fixed gauge-invariant Wilson observables plus a singular connected endpoint OPE, with no boundary theory allowed. The current raw R carrier is representation-limited, and a raw kappa_4 spectrum is too strong because negative compact-group kappa_4 is not a falsifier unless D_v>0. Compared with the global Schur-preimage route, C_ep is local after H,K and exports one scalar interval; compared with formal OPE language, it has primitive operations: source differentiation, interval arithmetic, incidence contraction, clipping, color multiplication, and tail addition. Efficient representation requirements are now fixed: encode endpoint boxes, seven source values, beta intervals, fractional b_ij incidences, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; identify carriers only by regulated source data; keep locality finite through T_tail; transfer only [I_-,I_+] to the finite OS gate. The conceptual value signal is sharpness and route change: the half-overlap shield D_v<=0 proves which endpoint boxes are harmless and leaves only certified 12-dominance plus tail as the demotion mechanism.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and endpoint-data computation.`
- Rationale: The branch has exhausted abstract OS-cone restatements; the decisive finite gate is the sign of a concrete endpoint-source interval after H,K, so varying one incidence parameter can expose whether the half-overlap shield is real or cosmetic.
- Situation seed: Heat-kernel SU(N) plaquette-sheet three-hairpin endpoint-box family at fixed finite cutoff, with the H,K null channel fixed and endpoint source log Z_v(sL_v) evaluated on the same Wilson action.
- Varied variable: The fractional overlap ratio eta_v=(b13(v)+b23(v))/b12(v), varied through the threshold eta_v=1/2 while keeping beta_v and the non-endpoint Wilson geometry fixed.
- Held-fixed controls: Same heat-kernel Wilson action, reflection plane, gauge group SU(N), and Wilson-loop normalization., Fixed three-hairpin H,K data, null vector, color factor C_N, and Gaussian margin M_G., Fixed endpoint box size regime a << ell_v << collar scale and the same seven-point source stencil., No boundary counterterm, no enlarged boundary algebra, and all residual overlap charged to T_tail.
- Expected observation: For eta_v>=1/2 the negative compact-group fourth cumulant is shielded and cannot lower the finite gate; for eta_v<1/2 a controlled negative beta_v can drive I_gate below zero only if T_tail is also too large or the 12-dominance is certified.
- Transfer certificate needed: A cutoff-uniform source-derivative interval for beta_v, a regulator-stable incidence interval for b_ij(v), and a same-theory tail bound proving that the exported [I_-,I_+] is a valid finite OS gate input.

## Next Experiment

Compute the fractional incidence table b_ij(v) and seven-point log Z_v source intervals for SU(2) and SU(3) heat-kernel endpoint boxes, then evaluate [I_-,I_+] with T_tail refinement to test the half-overlap shield.

# Endpoint-cell Ward-Hessian R++ enclosure

## Candidate Lemma

Finite conditional lemma: a Ward-subtracted flowed four-curvature kernel with computable near/far Hessian constants gives a valid lower interval for the H,K plus endpoint Wilson cumulant R_{++}.

## Definitions

- source object: two centered thin plus-hairpin Wilson sheet currents J_+^I in a finite 4D SU(N) Wilson lattice Yang-Mills box, regulated by gradient flow time t and point splitting epsilon.
- target object: the finite Route A Schur-Feshbach endpoint-box certificate R_{++}^{I,-}>L_+ for the fixed H,K instance, not a continuum mass-gap statement.
- controlled interface: cumulant expansion of the same flowed Wilson observables into pair covariance G_{++} and Ward-subtracted connected four-curvature kernel K_{4,t}^{WS}.
- same-theory condition: G_{++}, K_{4,t}^{WS}, counterterms, and L_+ are evaluated in the same cutoff family and normalization before any OS reconstruction claim.
- carrier: endpoint sheet currents with cell moments M_{2,+}(I), preserving gauge, color, reflection, orientation, cutoff, and endpoint locality invariants.
- efficient representation: encode sheets, endpoint charges, cells, sector kernels, counterterms; primitives are Ward/cusp subtraction, Taylor remainder, heat-kernel majorants, and interval arithmetic.

## Assumptions

- Model: finite-volume 4D SU(N) lattice Yang-Mills with Wilson action, gradient flow t>0, and fixed H,K collar/hairpin geometry.
- Cutoff: a<=epsilon<=eta<rho/4<=sqrt(t)/2, with constants required uniformly over the finite endpoint cells used in the interval certificate.
- Same-theory: all Wilson cumulants and subtractions come from one regulator/RG family; imported representational-dynamics results are support-only.
- Validity: Ward and cusp counterterms cancel one-hairpin perimeter/cusp pieces, and the plus endpoint current has zero monopole and dipole in each cell.
- Local: success changes only finite endpoint-box positivity after H,K; continuum existence, OS/Wightman axioms, nontriviality, and Hamiltonian mass gap remain untouched.

## Equations

- Ward-Hessian C4 enclosure: `\left|\langle J_+^I\otimes J_+^I,K_{4,t}^{WS}\rangle\right|\le M_{2,+}(I)^2 H_4^{I,+}(\rho)`. Valid when: Valid when Ward/cusp subtraction and plus-channel monopole-dipole cancellation hold cellwise for the same flowed Wilson cumulant.
- near-far Hessian envelope: `H_4^{I,+}(\rho)\le A_{near}t^{-5}+A_{far}\rho^{-10}`. Valid when: Applies when color-stripped sector kernels I_{3g}, I_{4g}, I_{ct}, and I_{end} obey flowed heat-kernel derivative majorants on cells of diameter eta.
- endpoint promotion interval: `R_{++}^{I,-}=g_t^4(N^2-1)\{2G_{++}^{I,-}-N M_{2,+}(I)^2(A_{near}t^{-5}+A_{far}\rho^{-10})\}-E_6^{I,+}>L_+`. Valid when: Requires the fixed H,K Schur-Feshbach leakage L_+ and the same-theory cumulant expansion through the controlled sixth-order remainder.

## Attempted Derivation

- Expand the two centered flowed hairpins to order g_t^4. Disconnected products and one-hairpin cusp/perimeter terms cancel; the pair part has color 2(N^2-1)G_{++}.
- Color-strip the connected four-curvature term. The remaining polarization carries N(N^2-1) and is paired with endpoint currents through K_{4,t}^{WS}.
- Use Ward identities plus the H,K plus-channel moment cancellation to remove constant and linear endpoint Taylor terms; bound the remainder by a Hessian norm times M_{2,+}^2.
- Split the Hessian majorant into near flowed and far cell regimes, insert it into the Schur-Feshbach endpoint inequality, and compare the resulting lower interval with L_+.

Blocking gap: The proof still needs certified constants A_near,A_far and E_6 from the regulated sector kernels, uniformly in cutoff and endpoint cells.

## Falsifiers

- falsifier: Ward/cusp subtraction leaves an epsilon-dependent logarithm in K_{4,t}^{WS}, so H_4 is not same-theory finite.
- falsifier: the certified A_near t^{-5}+A_far rho^{-10} makes the C4 penalty exceed 2G_{++}^{I,-} for every valid regulator window.
- falsifier: the actual H,K endpoint current has a residual dipole, invalidating the Hessian-only Taylor remainder bound.
- falsifier: R_{++}^{I,-}-L_+ changes sign across the required flow plateau, showing regulator-window fragility.

## Learning

Pressure: the missing mediator between finite Feshbach positivity and Wilson cumulant positivity. Tension: pair positivity and flow renormalization are valid but C4 can erase them. Endpoint currents beat raw contours and global OS witnesses. Efficient route: proof search for near/far Hessian constants, zero-pairing equivalence, and same-theory interval transfer.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the finite endpoint-box route.`
- Rationale: The abstract R term is already localized; the missing information is whether Ward-Hessian suppression survives actual H,K geometry and regulator windows.
- Situation seed: Finite SU(2) Wilson lattice box with the fixed H,K plus hairpin endpoint cells, gradient flow t, point splitting epsilon, and centered Wilson sheet currents J_+^I.
- Varied variable: eta/sqrt(t), the endpoint-cell diameter relative to flow radius, with rho=4eta held as the near/far split.
- Held-fixed controls: Fixed H,K sheet-current geometry and plus-channel orientation., Same Wilson action, same gradient-flow cumulants, and same cusp/Ward counterterms., Fixed Schur-Feshbach leakage L_+ and color normalization.
- Expected observation: If moment cancellation is effective, the C4 penalty scales like M_{2,+}^2 H_4 and an eta-window gives R_{++}^{I,-}>L_+; otherwise the endpoint repair is demoted.
- Transfer certificate needed: Certified cutoff-uniform A_near,A_far,E_6 intervals and a Ward/cusp subtraction identity before the thought experiment can affect proof obligations.

## Next Experiment

Compute interval bounds for A_near,A_far on the fixed endpoint cell partition using flowed heat-kernel derivative envelopes, then run the eta/rho/t plateau test against L_+.

# Gauge-Invariant Observable Density In The Excitation Sector -> finite post-H,K Wilson endpoint audit

## Candidate Lemma

Finite Route A certificate: for a fixed reflected H,K collar/hairpin endpoint box in heat-kernel regulated SU(N) lattice Yang-Mills, the post-H,K endpoint form is positive if the same-regulator shell margin Delta_sigma^(012) is positive. This proves only a finite Schur-corrected Wilson endpoint statement, not existence, OS reconstruction, or a Hamiltonian mass gap.

## Definitions

- source object: finite heat-kernel regulated SU(N) lattice Yang-Mills measure on one reflection-symmetric endpoint box, with Wilson plaquette sheets, transported curvature insertions, and the fixed H,K collar/hairpin basis.
- target object: the finite endpoint quadratic form R_sigma-S_HK on the post-H,K Wilson boundary subspace, not a continuum Hamiltonian spectral statement.
- controlled interface: sheet-kernel hypergraph Rec_sigma sending Wilson sheet pairs to C_sigma, K4_sigma, E_OPE,sigma, shell amplitudes A_l, and the Schur datum S_HK.
- same-theory condition: all cumulants, OPE coefficients, heat-kernel smearing, coupling g_R, Wilson basis, reflection support, and Schur subtraction are computed in the identical cutoff theory and normalization.
- Bridge/carrier: Rec_sigma has vertices equal to transported plaquette-pair insertions and edges weighted by connected four-curvature cumulants, with quotient only by Wilson trace identities and sheet symmetries.
- Hard gate: Delta_sigma^(012)>0 promotes finite endpoint-box positivity; Delta_sigma^(012)<=0 is a valid falsifier for this H,K collar/hairpin route.

## Assumptions

- Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action and fundamental trace normalization Tr(T^aT^b)=delta_ab/2.
- Regime: finite endpoint box, fixed lattice spacing a>0, smoothing scale sigma>=a, and no infinite-volume or continuum limit is taken.
- Cutoff: the OPE expansion is truncated after the quadratic transported-curvature term, with a rigorous same-regulator remainder interval e_OPE,sigma.
- Same-theory: C_sigma, K4_sigma, A_l, E_OPE,sigma, and S_HK are extracted from the same Wilson basis and same heat-kernel cutoff; no imported continuum glueball sector is used.
- Local: only shells l=0,1,2 inside the endpoint box are evaluated explicitly, while the tail l>=3 is bounded by T_ge3(sigma).
- Validity: the compressed endpoint subspace is finite-dimensional and the H,K Schur complement QHQ is strictly positive on the eliminated hairpin subspace.
- Constraint: the sheet-kernel quotient must be invariant under gauge transport, reflection, orientation reversal, and Wilson trace cyclicity.

## Equations

- transported sheet flux: `\Phi_i^a(\sigma)=\sum_{p\in S_i}w_i(p)\,\operatorname{Ad}_{U_{p\to *}}^{ab}F_p^b(\sigma)`. Valid when: Valid when the heat-kernel lattice regulator fixes transported plaquette curvatures and each Wilson sheet S_i carries oriented weights.
- connected endpoint polarization: `R_{ij,\sigma}=\operatorname{cum}_2\big(:\!\Phi_i^a\Phi_i^a\!:,:\!\Phi_j^b\Phi_j^b\!:\big)`. Valid when: Applies after vacuum and perimeter counterterms are subtracted in the same reflected endpoint Wilson box.
- Gaussian covariance block: `C_{ij,\sigma}=\sum_{p\in S_i,q\in S_j}w_i(p)w_j(q)\,\langle \operatorname{Ad}_{U_{p\to *}}F_p^a(\sigma)\operatorname{Ad}_{U_{q\to *}}F_q^a(\sigma)\rangle_c`. Valid when: Valid for the same heat-kernel cutoff and base-point transport used to define the Wilson sheet fluxes.
- R decomposition: `R_\sigma=\alpha_N g_R^4(C_\sigma\circ C_\sigma)+\frac{g_R^4}{16N^2}K^{(4)}_\sigma+E_{\mathrm{OPE},\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Requires fundamental SU(N) color normalization, connected cumulant subtraction, and the quadratic boundary OPE in one cutoff theory.
- A012 negative-size bound: `\lambda_{\min}(K^{(4)}_\sigma)\ge -\big(A_0(\sigma)+A_1(\sigma)+A_2(\sigma)+T_{\ge3}(\sigma)\big)`. Valid when: Valid when the sheet-kernel hypergraph shells give a Gershgorin row-sum envelope for the compressed four-curvature cumulant.
- finite endpoint margin: `\Delta_\sigma^{(012)}=m_G(\sigma)-\frac{g_R^4}{16N^2}\big(A_0+A_1+A_2+T_{\ge3}\big)-e_{\mathrm{OPE},\sigma}-s_{HK}`. Valid when: Applies after diagonal normalization of the endpoint basis and Schur subtraction using the same H,K Wilson geometry.
- promotion implication: `\Delta_\sigma^{(012)}>0\ \Longrightarrow\ R_\sigma-S_{HK}\succeq \Delta_\sigma^{(012)}I_{\mathrm{end}}`. Valid when: Valid only for the finite endpoint subspace and does not transfer to continuum OS spectral positivity.

## Attempted Derivation

- Conceptual pressure attacked: mediate actual connected Wilson cumulants to Schur-corrected endpoint positivity without inflating a finite Wilson calculation into the Clay theorem.
- Declarative tension: Wilson/OPE coefficients, connected kappa4 negativity, OPE error, and H,K Schur energy must be valid in one cutoff theory, while continuum OS reconstruction and spectral transfer remain quarantined.
- Expand each endpoint Wilson sheet product through the heat-kernel quadratic boundary OPE and define transported fluxes Phi_i^a(sigma).
- Use same-regulator vacuum and perimeter cancellation to replace the polarization by R_ij,sigma=cum_2(:Phi_i^2:,:Phi_j^2:).
- Separate Wick-pair crossed contractions from the connected four-curvature cumulant; the crossed term gives alpha_N g_R^4(C_sigma o C_sigma) and is positive semidefinite by the Schur product theorem.
- Compress the connected four-curvature cumulant onto sheet-pair nodes and group entries by hypergraph shell distance l=0,1,2 plus a tail l>=3.
- Apply Gershgorin or row-sum domination to obtain lambda_min(K4_sigma)>=-(A0+A1+A2+T_ge3).
- Subtract the finite Schur-Feshbach hairpin energy S_HK=B^*E^{-1}B and the OPE interval e_OPE,sigma in the same normalized endpoint basis.
- Conclude R_sigma-S_HK >= Delta_sigma^(012) I_end if Delta_sigma^(012)>0.

Blocking gap: The proof skeleton is valid finite linear algebra, but the actual same-regulator intervals for A0(sigma), A1(sigma), A2(sigma), T_ge3(sigma), and e_OPE,sigma have not yet been computed for the worked H,K geometry.

## Falsifiers

- Finite falsifier: Delta_sigma^(012)<=0 after rigorous same-regulator interval arithmetic for the H,K endpoint box.
- Carrier falsifier: Wilson-invariant refinement of the sheet-kernel hypergraph changes A_l or the sign of Delta_sigma^(012).
- Regulator falsifier: the heat-kernel OPE remainder e_OPE,sigma is of the same size as the Gaussian margin for all allowed sigma/a.
- Locality falsifier: the tail T_ge3(sigma) is not summable or dominates A0+A1+A2 in the finite endpoint geometry.
- Schur falsifier: the hairpin energy s_HK exceeds the positive Gaussian color-square floor m_G(sigma).
- Same-theory falsifier: any input to C_sigma, K4_sigma, or S_HK requires a different measure, coupling normalization, or Wilson basis.

## Learning

Cycle 285 makes the fourth A012 consolidation move concrete: R is the same-regulator connected Wilson cumulant cum_2(:Phi_i^2:,:Phi_j^2:), not a symbolic endpoint parameter. The efficient carrier remains the sheet-kernel hypergraph because scalar R is too weak, OS density is too strong and circular for this local gate, and raw enumeration is exact but fragmented. The hard gate is Delta_sigma^(012). Success changes only finite Route A endpoint-box positivity; failure is a precise falsifier for the worked H,K collar/hairpin route. The conceptual value signal is sharp and unifying at finite scope: one inequality combines the positive Gaussian color square, the dangerous kappa4 shell envelope, the OPE interval, and Schur hairpin energy while preserving Clay target commitments and non-claims.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the final A012 consolidation cycle.`
- Rationale: The branch has already fixed the abstract carrier; the missing mathematical information is whether the concrete connected boundary-OPE polarization can survive Schur subtraction in the worked H,K endpoint geometry.
- Situation seed: Take SU(3) heat-kernel lattice Yang-Mills on a finite reflection-symmetric 4D endpoint box with the fixed H,K collar/hairpin Wilson sheets; enumerate transported plaquette-pair nodes and compute interval enclosures for C_sigma and K4_sigma shells l=0,1,2.
- Varied variable: Vary only rho=sigma/a, the heat-kernel smoothing radius in lattice units.
- Held-fixed controls: Wilson H,K collar/hairpin sheet geometry and endpoint basis., Fundamental SU(3) color normalization and heat-kernel plaquette action., Same reflected endpoint box, coupling convention g_R, and Schur datum S_HK., Same normal-ordering, vacuum/perimeter subtraction, and OPE truncation rule.
- Expected observation: If Delta_sigma^(012) has a positive interval for some rho window, the finite endpoint-box route gets a valid promotion target; if the interval remains nonpositive, kappa4, OPE error, or hairpin coupling kills this geometry.
- Transfer certificate needed: A rigorous same-regulator interval certificate for A0,A1,A2,T_ge3,e_OPE,m_G,s_HK plus a quotient audit proving Rec_sigma preserves Wilson trace identities and reflection support.

## Next Experiment

Enumerate the actual H,K endpoint sheet-pair hypergraph for SU(3) heat-kernel lattice YM, compute C_sigma and K4_sigma shell intervals A0,A1,A2 at rho=sigma/a in a fixed finite box, then evaluate the rigorous sign of Delta_sigma^(012).

