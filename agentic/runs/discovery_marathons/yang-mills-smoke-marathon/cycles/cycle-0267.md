# cycle-0267

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology -> post-H,K endpoint-kappa4 gate

## Candidate Lemma

In the heat-kernel plaquette-sheet regulator for the locked three-hairpin Wilson block, the first compact-group endpoint contribution to the connected boundary-OPE polarization is a negative fourth cumulant with explicit adjoint quartic color factor; after the null-channel contraction it is dangerous only through clipped positive endpoint dominance D_v>0, not through negativity of kappa4 alone.

## Definitions

- source object: the regulated endpoint-box generating functions Z_{v,a}(s)=<exp(s X_{v,a})> for same-theory SU(N) heat-kernel plaquette sheets meeting the reflection-plane endpoints of the fixed three-hairpin Wilson collar block.
- target object: the scalar post-H,K Schur-Feshbach null-channel endpoint contribution I_gate(a) for this finite Wilson OS quotient block, not the continuum Yang-Mills mass gap.
- controlled interface: source derivatives d_s^4 log Z_{v,a}(0), endpoint incidence tensors B_{ij,v}, color factor C_N, and a tail interval are converted into a lower/upper interval for the finite OS gate.
- same-theory condition: the sources differentiate the original regulated Wilson plaquette-sheet action and observable algebra; no boundary counterterm, altered Wilson normalization, or new reflection-plane degree of freedom is introduced.
- Conceptual pressure: make singular endpoint collapse sign-certifiable while preserving the same Wilson theory that supplied collar OS positivity.
- Declarative tension: finite collar OS positivity, unchanged gauge-invariant Wilson observables, and connected endpoint boundary-OPE singularities must jointly hold; symbolic R is representation-limited because it forgets endpoint incidence signs.
- Carrier critique: a raw kappa4 spectrum is too strong and can falsely demote safe blocks; a global Schur-preimage matrix is valid but less local than the clipped endpoint source carrier.
- Efficient representation requirements: encode endpoint boxes, source stencil values, beta intervals, D_v incidence intervals, color factors, and tails; preserve Wilson normalization, null-channel cancellations, cutoff uniformity, and same-theory observables; allow source differentiation, interval arithmetic, clipping, incidence contraction, color multiplication, and tail addition; identify equivalent carriers only by equal regulated source derivatives; charge nonlocal leftovers to T_tail; transfer only I_gate to the finite OS gate.

## Assumptions

- Model/regime: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action, finite volume and cutoff a>0, then endpoint boxes of side ell_v with a<<ell_v before any continuum claim.
- Uniformity: the endpoint BCH expansion and eighth source derivatives of log Z_{v,a} are bounded uniformly on |s|<=3h and on the chosen endpoint box family.
- Same-theory cutoff condition: H,K, the null vector, and the Wilson hairpin observables are the previously locked regulated observables; only source differentiation is added as a bookkeeping device.
- Cancellation condition: disconnected Wick-square pieces are removed by log Z, and straight-segment C_A f f contacts cancel under the established null-incidence identity; uncancelled endpoint/corner overlap is put in T_tail.
- Naturalness condition: endpoint sources are gauge-covariant singlet flux contractions, so the target scalar is invariant under local gauge rotations and reflection-compatible.
- Non-claim boundary: this lemma is a finite regulator-level R/kappa4 computation and does not construct continuum YM, prove full OS axioms, or imply a positive Hamiltonian mass gap.

## Equations

- endpoint Haar-Jacobian expansion: `\log J(\xi)=-\frac{1}{24}\operatorname{tr}_{\mathrm{ad}}((\operatorname{ad}_{\xi})^2)-\frac{1}{2880}\operatorname{tr}_{\mathrm{ad}}((\operatorname{ad}_{\xi})^4)+O(\|\xi\|^6)`. Valid when: Valid when the endpoint box is parametrized by exponential Lie-algebra coordinates with heat-kernel time small enough for the BCH and Haar-density expansion to be uniform.
- compact-group fourth cumulant coefficient: `\kappa^{J}_{4,v}(B)=\left.\partial_s^4\log J(sB)\right|_{0}=-\frac{1}{120}\operatorname{tr}_{\mathrm{ad}}((\operatorname{ad}_{B})^4)=-\frac{1}{120}\{2N\operatorname{tr}_{F}(B^4)+6(\operatorname{tr}_{F}(B^2))^2\}\le 0`. Valid when: Applies for SU(N) with fundamental normalization after the endpoint source reduces to one singlet Lie-algebra direction B inside a single regulated endpoint box.
- endpoint incidence contraction: `R_{\mathrm{end}}(a)=-C_N\sum_{v}\beta_{v,a}D_v(a)+T_{\mathrm{tail}}(a),\quad D_v=2G_{12,v}-4G_{13,v}-4G_{23,v},\quad C_N=\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Requires the locked three-hairpin null-channel weights, connected source derivatives of the same Wilson regulator, and prior cancellation of Wick-square and straight f f contacts.
- clipped lower gate interval: `I_{\mathrm{gate}}^{\mathrm{lo}}=M_G-C_N\sum_v \beta^{+}_{v,a}[D_v(a)]_{+}-\tau_{\mathrm{tail}}(a),\quad [x]_+=\max(x,0)`. Valid when: Valid when beta_{v,a} lies in certified intervals [0,beta^+_{v,a}] and the remaining endpoint/corner contributions are bounded in absolute value by tau_tail.
- seven-point fourth-source stencil: `\widehat\beta_{v,a}(h)=-h^{-4}\sum_{r=-3}^{3}\omega_r\log Z_{v,a}(rh),\quad \omega=(-1/6,2,-13/2,28/3,-13/2,2,-1/6)`. Valid when: Applies when log Z_{v,a}(s) is evaluated in the same regulated theory for |s|<=3h and its eighth derivative is uniformly bounded.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: the regulated endpoint-box generating functions Z_{v,a}(s)=<exp(s X_{v,a})> for same-theory SU(N) heat-kernel plaquette sheets meeting the reflection-plane endpoints of the fixed three-hairpin Wilson collar block.; target object: the scalar post-H,K Schur-Feshbach null-channel endpoint contribution I_gate(a) for this finite Wilson OS quotient block, not the continuum Yang-Mills mass gap.; Model/regime: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action, finite volume and cutoff a>0, then endpoint boxes of side ell_v with a<<ell_v before any continuum claim..
- Fix the heat-kernel plaquette-sheet regulator and the already locked three-hairpin Wilson block; keep H,K, the null vector, reflection map, and Wilson normalization unchanged.
- Localize the remaining connected boundary-OPE polarization to endpoint boxes, charging every nonendpoint overlap and corner remainder to T_tail.
- Represent each endpoint box by exponential Lie-algebra coordinates. The Haar density gives the quartic term -tr_ad(ad_B^4)/2880 in log J, hence the fourth source cumulant -tr_ad(ad_B^4)/120.
- Use the SU(N) adjoint quartic identity to expose the color/geometric factors: 2N tr_F(B^4)+6(tr_F(B^2))^2. This supplies beta_v>=0 for the negative compact-group kappa4 magnitude.
- Contract the pair contributions with the fixed null-channel weights. The scalar endpoint contribution is -C_N sum_v beta_v D_v plus T_tail, with D_v=2G12-4G13-4G23.
- Clip the sign: only D_v>0 can lower the OS gate. Equal disjoint endpoint boxes, where the positive dominance vanishes or is outweighed, are protective rather than dangerous.
- Extract beta_v by the seven-point fourth-source stencil in log Z_v, with error controlled by an eighth-derivative bound, and combine beta, D_v, color, margin, and tail into [I_gate^lo,I_gate^up].

Blocking gap: The exact endpoint incidence table B_{ij,v} and a cutoff-uniform bound on the non-Jacobian endpoint remainder plus T_tail are still missing; without them the interval may remain undecided.

## Falsifiers

- falsifier: a same-theory endpoint source computation with I_gate^up<0 gives a finite reflected-Wilson OS determinant obstruction after H,K.
- A valid stress case is endpoint dominance D_v>0 concentrated at the 12 endpoints with beta_v large enough that the clipped negative term exceeds M_G.
- The route fails if the heat-kernel source derivatives require a boundary counterterm or altered Wilson normalization, because that violates the same-theory condition.
- The carrier is too weak if nonlocal corner overlap cannot be bounded by a finite T_tail without changing the endpoint decomposition.
- A sign falsifier would be loss of the straight f f null-incidence cancellation in the actual endpoint orientation table.

## Learning

Cycle 267 attacks the conceptual pressure of endpoint collapse in the same Wilson theory. The new computation is the endpoint Haar-Jacobian fourth cumulant: kappa4 is negative with explicit adjoint quartic color factor, but after the null-channel incidence contraction it is dangerous only through clipped positive D_v and tail. Hard gate changed: the finite post-H,K reflected-Wilson OS transfer gate can now be promoted or falsified by endpoint source intervals. Larger Clay gates remain untouched: continuum existence, full OS/Wightman reconstruction, nontriviality, and positive Hamiltonian mass gap are not implied. Conceptual value signal: sharpness and route change, because negative kappa4 is no longer mistaken for the falsifier; endpoint dominance plus uncontrolled tail is the actual obstruction.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete falsifier probe now.`
- Rationale: The branch already has H,K and the corrected null-channel gate; another abstract OS restatement would loop. The remaining decision is whether endpoint kappa4 incidence can overcome the finite positive margin in the same regulated Wilson theory.
- Situation seed: Take the fixed three-hairpin reflected Wilson collar block in SU(N) heat-kernel plaquette-sheet regulation and replace its endpoint boxes by a one-parameter family with the same Wilson contours but tunable overlap dominance at the 12 endpoints.
- Varied variable: Endpoint dominance ratio eta=sum_{v in E12}[D_v]_+/(sum_v |D_v|+1), implemented by sliding only the relative endpoint-box overlap weights while keeping the hairpin contours and H,K data fixed.
- Held-fixed controls: Gauge group SU(N), heat-kernel plaquette action, reflection map, and gauge-invariant Wilson observable algebra., The locked H,K block, Feshbach null vector, Wilson normalization, color factor C_N, and no-boundary-counterterm same-theory condition., Stencil step h and endpoint-box scale ell_v are chosen inside a regime with uniform eighth-derivative and tail bounds.
- Expected observation: If eta can be increased while beta_v intervals stay near the negative Haar-Jacobian coefficient, I_gate should cross from promoted to falsified at a calculable eta_star; if it never crosses under certified tails, the endpoint kappa4 obstruction is demoted for this block.
- Transfer certificate needed: A cutoff-uniform endpoint incidence table, certified source-derivative intervals for beta_v, and a tail bound proving that the thought-experiment deformations are realized by the same regulated Wilson theory before the intuition affects proof obligations.

## Next Experiment

Compute the actual endpoint incidence table for the three-hairpin block: list B_{12,v}, B_{13,v}, B_{23,v}, form D_v=2G12-4G13-4G23, then run the seven-point log Z_v stencil with a uniform M8 and T_tail bound to decide the interval sign.

# Cycle 267: Ward-subtracted endpoint-box Xi interval enclosure

## Candidate Lemma

For fixed finite H,K endpoint hairpins, the same-theory flowed Wilson covariance entry R_{++}^{ren}/kappa_4 admits an interval enclosure from Ward-subtracted heat-kernel cell integrals. If its lower endpoint beats the known Schur-Feshbach leakage L_+, finite endpoint-box positivity is promoted; if not, this repair is demoted without claiming the Clay theorem.

## Definitions

- source object: SU(N) Euclidean Yang-Mills Schwinger family at cutoff a with gradient-flow time tau>0, boundary point splitting eps, and cusp/perimeter-renormalized thin Wilson hairpins H_+,K_+ represented by oriented sheet currents J_H,J_K.
- target object: the finite scalar R_{++}^{ren}/kappa_4 entering the already-extracted H,K Schur-Feshbach endpoint-box matrix after the leakage L_+ is fixed.
- controlled interface: the centered covariance kappa_2(X_{H_+}^{tau,eps},X_{K_+}^{tau,eps}) expanded into a positive two-curvature pair term plus a connected four-curvature polarization Xi_{++}.
- same-theory condition: the cutoff measure, flow equation, Wilson renormalization, sheet currents, and endpoint subtraction are the same in the covariance, pair baseline, connected kernel, and finite H,K transfer; no auxiliary Gaussian theory supplies R_{++}.
- Flowed curvature is G_{mu nu}^a(t,x) of the Yang-Mills gradient-flow field B_mu(t,x).
- The sheet-current carrier is the oriented surface 2-current J_S^{mu nu}(x) with endpoint current partial J_S supported in the collar boxes.
- The Ward-subtracted kernel K_W is the sum of one-loop 3-gluon, 4-gluon, counterterm, and endpoint-current kernels after disconnected and one-hairpin subtractions.

## Assumptions

- Model/regime: fixed N>=2, finite reflected lattice torus or a continuum candidate family with the same gauge-invariant Wilson observables and positive flow time tau.
- Cutoff/uniformity: a << eps <= sqrt(8 tau) << d, where d is the endpoint-box separation; constants in the interval bound are uniform for a below the partition scale.
- Renormalization: cusp and perimeter factors are fixed from the one-hairpin expectation before taking the connected covariance.
- Perturbative option: the displayed sector decomposition is valid to one loop in a flow-window coupling g_R(mu); nonperturbative lattice-flow data may replace it but must use the same centered observables.
- Naturalness: H_+,K_+ are the finite collar/hairpin objects already used to form the H,K Schur-Feshbach matrix, not newly optimized witnesses.
- Same-theory transfer: R_{++}^{ren} is inserted only into the finite endpoint-box theorem and does not assert continuum existence, OS/Wightman reconstruction, nontriviality, or a Hamiltonian mass gap.

## Equations

- flowed curvature covariance kernel: `D_{\mu\nu,\rho\sigma}^{ab,\tau}(r)=\delta^{ab}(\partial_\mu\partial_\rho\delta_{\nu\sigma}-\partial_\mu\partial_\sigma\delta_{\nu\rho}-\partial_\nu\partial_\rho\delta_{\mu\sigma}+\partial_\nu\partial_\sigma\delta_{\mu\rho})\Phi_{2\tau}(r),\quad \Phi_u(r)=\frac{1-e^{-|r|^2/(4u)}}{4\pi^2|r|^2}.`. Valid when: Valid in Feynman gauge for the flowed tree-level curvature covariance at positive flow time tau, away from coincident unflowed singularities and before adding interaction-sector kernels.
- endpoint covariance decomposition: `\frac{R_{++}^{ren}}{\kappa_4}=(N^2-1)\left(2\mathcal G_{++}+N g_R^2\Xi_{++}\right)+O(g_R^4 M_{++}).`. Valid when: Applies after centering both flowed hairpins and subtracting cusp and perimeter factors, with fixed H,K sheets in a perturbative regulator window.
- positive pair baseline: `\mathcal G_{++}=\int_{\Sigma_H^2\times\Sigma_K^2}(J_H^1D^\tau J_K^1)(J_H^2D^\tau J_K^2)\,d\sigma_H^1d\sigma_H^2d\sigma_K^1d\sigma_K^2\ge 0.`. Valid when: Valid when the reflected sheet orientations are fixed and the two-curvature cross-pairing is evaluated with the same flowed covariance kernel.
- connected polarization sector split: `\Xi_{++}=I_{3g}[J_H,J_K]+I_{4g}[J_H,J_K]+I_{ct}[J_H,J_K]+I_{end}[J_H,J_K].`. Valid when: Requires the one-loop flowed Yang-Mills cumulant expansion with Ward subtraction, endpoint-current bookkeeping, and the same cusp-renormalized Wilson hairpins.
- cell interval enclosure: `\Xi_{++}\in\sum_{Q\in\mathcal P^4}{\rm Vol}(Q)[\inf_Q\mathcal K_W^{\tau,\epsilon},\sup_Q\mathcal K_W^{\tau,\epsilon}]+[-E_{near},E_{near}].`. Valid when: Valid after the endpoint boxes are partitioned into cells resolving cusp neighborhoods, with heat-kernel derivative majorants controlling every near-diagonal cell.
- finite endpoint promotion inequality: `\underline R_{++}:=(N^2-1)\left(2\mathcal G_{++}+Ng_R^2\underline\Xi_{++}-g_R^4M_{++}\right)>L_+.`. Valid when: Applies only after H,K and L_+ are already known, the interval lower endpoint is certified, and the remainder bound M_{++} is same-theory.

## Attempted Derivation

- Replace each raw Wilson hairpin by a cusp-renormalized flowed observable X_S^{tau,eps}; the nonabelian Stokes expansion is organized by sheet current J_S and endpoint current partial J_S.
- Center X_H and X_K. The disconnected product and one-hairpin perimeter/cusp terms cancel before the covariance is expanded; this is the cancellation being used.
- The quadratic curvature part gives two cross-pairings. With tr(T^aT^b)=delta^{ab}/2 and the plus-channel normalization, the pair color factor is 2(N^2-1), leaving the positive geometry G_{++}.
- The first non-Gaussian correction is the connected four-curvature cumulant. Its one-loop pieces are assigned to I_{3g}, I_{4g}, I_ct, and I_end with common sheet-current arguments.
- Use the flowed transverse curvature kernel to integrate longitudinal derivatives by parts. Endpoint remnants are exactly the I_end terms; they cancel the cusp-local counterterm pieces if the same one-hairpin renormalization is used.
- Partition the endpoint boxes into cells. On separated cells use sup/inf heat-kernel derivative bounds; on near cells use the Ward-subtracted BV majorant E_near.
- Insert the resulting lower endpoint underline Xi_{++} into underline R_{++}>L_+. This is a finite Schur-Feshbach endpoint-box certificate, not an OS reconstruction or spectral-gap proof.

Blocking gap: No certified numerical or symbolic interval for I_{3g}+I_{4g}+I_ct+I_end has yet been produced for the actual H,K geometry; the one-loop remainder M_{++} also needs a same-theory bound or a lattice-flow replacement.

## Falsifiers

- Certified Xi_{++} interval is so negative that underline R_{++} <= L_+, demoting the endpoint-box repair.
- Ward-subtracted kernel retains eps^{-p} cusp dependence after one-hairpin renormalization.
- The R_{++} interval has no stable plateau as a->0 at fixed physical tau window.
- The plus-channel geometry has G_{++}=0 because the extracted H,K sheets have cancelling orientation current.
- The one-loop estimate is not valid and no nonperturbative lattice-flow interval can replace it.
- The interval width remains larger than the Schur-Feshbach margin under all feasible cell refinements.

## Learning

Conceptual pressure attacked: finite Schur-Feshbach positivity needs a same-theory endpoint mediator, while positive pair covariance and gradient-flow renormalization alone do not control the connected four-curvature polarization. The hard gate is finite endpoint-box positivity after H,K; success promotes this local gate, failure quarantines the R repair, and both leave Clay continuum existence, OS/Wightman axioms, nontriviality, and Hamiltonian mass gap untouched. The conceptual value signal is sharp and route-changing at local scope: R_{++} is converted from a symbolic placeholder into a valid falsifiable interval problem with regulator, cumulant, color factors, Ward cancellation, and promotion inequality.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has already named the R term; the non-looping move is a concrete same-theory regulator-window falsifier for the connected polarization Xi_{++}, not another Wilson/OS obstruction restatement.
- Situation seed: SU(3) Wilson plaquette lattice on a reflected four-torus with the extracted H_+,K_+ endpoint hairpin sheets fixed in physical units; measure centered flowed Wilson hairpin covariance and separately interval-bound the Ward-subtracted one-loop sheet-current kernel in the endpoint boxes.
- Varied variable: flow ratio alpha=sqrt(8 tau)/d, varied over a/d << alpha <= 1/6 while the endpoint separation d and point-splitting rule eps=sqrt(8 tau)/2 are held fixed.
- Held-fixed controls: Same Wilson lattice action, same reflection plane, and same gauge-invariant flowed hairpin observables in every measurement., Same H,K finite Schur-Feshbach data and fixed leakage L_+; no re-optimization of the witness after seeing R_{++}., Same cusp/perimeter renormalization from one-hairpin expectations and same sheet-current orientation convention., Same continuum physical volume window and endpoint-box partition refinement policy.
- Expected observation: A valid route shows a plateau in (2G_{++}+Ng_R^2Xi_{++}) with a positive lower interval exceeding L_+/(N^2-1). A falsifier is a stable negative connected polarization or regulator drift that prevents this inequality.
- Transfer certificate needed: Uniform a->0 control at positive flow time, verified Ward/cusp cancellation, a certified interval or lattice error bar for Xi_{++}, and proof that the covariance is the same-theory Wilson cumulant inserted into the finite H,K Schur-Feshbach theorem.

## Next Experiment

Derive explicit heat-kernel sup/inf formulas for the first endpoint-box cell partition, then enclose I_{3g}, I_{4g}, I_ct, and I_end for SU(2) and SU(3) with fixed H_+,K_+ currents and test underline R_{++}>L_+.

# Post-H,K endpoint-box kappa4 shell interval certificate

## Candidate Lemma

For a fixed reflected Wilson collar/hairpin endpoint basis with known H,K and heat-kernel regulator sigma, Schur-corrected endpoint positivity is certified by one finite interval gamma_sigma. The branch is valid only if the connected four-curvature cumulant negative part, OPE remainder, and Schur hairpin energy are dominated by the PSD crossed-curvature Gaussian square.

## Definitions

- source object: heat-kernel regulated SU(N) Wilson endpoint sheets S_i with transported curvature fluxes Phi_i^a(sigma) and connected Wilson cumulants computed before OS reconstruction.
- target object: the finite Schur-corrected endpoint-box matrix Delta_sigma acting on the post-H,K endpoint coefficient space, not the full Yang-Mills Hamiltonian.
- controlled interface: a sheet-kernel hypergraph whose vertices are transported curvature insertions, hyperedges are connected cumulants, shell labels encode endpoint-box locality, and Schur data encode B^*E^{-1}B.
- same-theory condition: the regulator sigma, renormalized coupling g_R(sigma), Wilson basis, endpoint normalization, reflected support, and H,K Schur subtraction are identical in the Gaussian, kappa4, OPE, and endpoint matrices.

## Assumptions

- Model/regime: finite endpoint Wilson algebra in four-dimensional Euclidean SU(N) Yang-Mills with heat-kernel mollified curvature and reflection-positive Wilson expectations at cutoff a or a controlled continuum regulator.
- Uniformity: the endpoint box contains finitely many collar sheets and hairpin channels, with sigma >= c a and a fixed shell budget L_max before any continuum inference is attempted.
- Same-theory cutoff: H,K, C_sigma, kappa4_sigma, and E_OPE are evaluated from the same Wilson measure and the same transport convention; no imported effective theory coefficients are allowed.
- Schur hypothesis: the hairpin block E=QHQ is positive with known spectral floor eta_sigma>0, so S_HK=B^*E^{-1}B is a finite positive semidefinite matrix.
- OPE hypothesis: the Wilson logarithm admits a boundary OPE through the two-curvature crossed term with a certified operator-norm remainder e_OPE(sigma,a,L_max).
- Cumulant hypothesis: the connected four-curvature cumulant compressed to the endpoint basis has a shell row envelope b_l(sigma,a) giving a computable bound on its negative spectral part.
- Non-claim boundary: success changes only the finite Route A endpoint-box positivity gate; OS/Wightman axioms, continuum existence, and the positive Hamiltonian mass gap remain untouched.

## Equations

- transported-flux-covariance: `C_{ij}^{\sigma}=\sum_a\langle \Phi_i^a(\sigma)\Phi_j^a(\sigma)\rangle_c,\quad \Phi_i^a(\sigma)=\int_{S_i} h_\sigma(x-y)\,\mathrm{Ad}_{U_{x_0x}}(F_{\mu\nu}(x))^a\,dS_i^{\mu\nu}(x)`. Valid when: Valid when heat-kernel smearing, parallel transport, and reflected endpoint sheets are fixed before taking connected Wilson expectations.
- endpoint-polarization-decomposition: `R_{ij}^{\sigma}=\alpha_N g_R(\sigma)^4\,(C^{\sigma}\circ C^{\sigma})_{ij}+\frac{g_R(\sigma)^4}{16N^2}(\kappa_{4}^{\sigma})_{ij}+(E_{\mathrm{OPE}}^{\sigma})_{ij},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after vacuum, perimeter, and disconnected two-loop pieces are cancelled by connected Wilson normalization in the same regulated theory.
- connected-four-curvature-compression: `(\kappa_4^{\sigma})_{ij}=\int_{S_i^2\times S_j^2} W_i(x_1,x_2)W_j(y_1,y_2)\,\langle F(x_1)F(x_2)F(y_1)F(y_2)\rangle_{c,\mathrm{tr}}^{\sigma}\,dx\,dy`. Valid when: Requires the same transported color trace, sheet weights, and heat-kernel mollifier used in the Wilson OPE expansion.
- shell-row-negative-bound: `M_{4,\sigma}^{-}:=\| (\kappa_4^{\sigma})_-\|\le \|\kappa_4^{\sigma}\|\le \max_i\sum_j\sum_{\ell\le L_{\max}} n_{ij\ell}|w_iw_j|\,b_\ell(\sigma,a)+\varepsilon_{\mathrm{tail}}(L_{\max})`. Valid when: Valid when the sheet-kernel hypergraph quotient preserves Wilson symmetries and every cumulant hyperedge is assigned to exactly one locality shell.
- schur-corrected-margin: `\Delta_\sigma=R_\sigma-S_{HK}^{\sigma},\quad S_{HK}^{\sigma}=B_\sigma^*E_\sigma^{-1}B_\sigma,\quad \lambda_{\min}(\Delta_\sigma)\ge m_G^\sigma-\frac{g_R(\sigma)^4}{16N^2}M_{4,\sigma}^- - e_{\mathrm{OPE}}^\sigma-s_{HK}^\sigma=:\gamma_\sigma`. Valid when: Valid when E_sigma has spectral floor eta_sigma and all matrices are compressed to the identical post-H,K endpoint basis.

## Attempted Derivation

- Attack conceptual pressure: the route needs a mediator from actual connected Wilson cumulants to Schur-corrected endpoint positivity, not another OS density or symbolic R discussion.
- Declarative tension: same-theory Wilson/OPE coefficients, finite Schur-Feshbach subtraction, and endpoint positivity must jointly hold, but scalar R is too weak and raw plaquette enumeration is fragmented; full OS observable density is too strong and circular for this local gate.
- Choose the heat-kernel regulator sigma and transported curvature flux Phi_i^a(sigma) on each endpoint collar sheet; keep the H,K endpoint basis fixed.
- Expand the connected Wilson endpoint cumulant through crossed two-curvature order; vacuum, perimeter, and disconnected products cancel because the endpoint observable is connected and vacuum-subtracted.
- Contract SU(N) traces with tr(T^aT^b)=delta^{ab}/2; the crossed Gaussian part becomes alpha_N g_R^4(C_sigma o C_sigma), hence PSD by the Schur product theorem.
- Compress the remaining connected four-curvature cumulant into kappa4_sigma; encode its integration domains, color tensors, sheet weights, and locality shells in the sheet-kernel hypergraph.
- Use shell row sums to bound the negative spectral size M4_sigma^-; this is crude but valid for a first finite falsifier because it upper-bounds the operator norm.
- Subtract the known Schur hairpin energy S_HK=B^*E^{-1}B and define gamma_sigma as the finite lower margin for Delta_sigma.

Blocking gap: The missing proof object is the first same-regulator shell envelope b_l(sigma,a) for the connected four-curvature cumulant, plus a reproducible H,K Schur matrix for the chosen collar/hairpin geometry.

## Falsifiers

- falsifier: gamma_sigma<0 for the first same-regulator endpoint box after rigorous row-sum and Schur subtraction, demoting this collar/hairpin geometry.
- falsifier: the connected kappa4 shell envelope is nonuniform in sigma/a or grows faster than the Gaussian margin under endpoint refinement.
- falsifier: quotienting plaquette sheets by geometric symmetry changes a Wilson trace identity or color tensor, making the interval non-invariant.
- falsifier: H,K extracted at the same regulator alter S_HK enough to erase every positive Gaussian-square margin.
- falsifier: OPE remainder cannot be bounded within the endpoint locality budget, so R_sigma is not a valid finite object.

## Learning

Cycle 267 attacks the conceptual pressure that the post-H,K route lacks a valid mediator between concrete connected Wilson cumulants and Schur-corrected endpoint positivity. The declarative tension is explicit: Wilson/OPE data, kappa4 negativity, and Schur subtraction must be computed in the same theory, but scalar R is representation-limited, full OS density is too strong, and raw plaquette enumeration is fragmented. The sheet-kernel hypergraph is retained because it encodes sheets, weights, transporters, color tensors, shell labels, multiplicities, OPE errors, and Schur data; preserves gauge invariance, reflection support, Gaussian/kappa4 separation, endpoint compression, and same-theory normalization; supports cumulant contraction, quotienting, shell row/operator bounds, interval arithmetic, and Schur subtraction; quotients only by Wilson-invariant trace identities; and exposes falsifiers by margin failure or non-invariance. The value signal is sharp and route-changing at finite scope: gamma_sigma turns the unknown boundary-OPE polarization into a computable sign/size interval without claiming the Clay theorem.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and coefficient-extraction guide.`
- Rationale: The branch already has the abstract Delta_sigma formula; the decisive missing information is whether the actual heat-kernel connected four-curvature shell contribution is small enough after Schur subtraction.
- Situation seed: A single SU(2) or SU(3) heat-kernel regulated endpoint box with two reflected collar sheets and one hairpin channel, using the same Wilson transporters to compute C_sigma, kappa4_sigma, E_OPE, and S_HK.
- Varied variable: The dyadic shell cutoff L_max for the connected four-curvature hyperedges, equivalently the maximum endpoint-box separation measured in units of sigma.
- Held-fixed controls: Gauge group SU(N), generator normalization, and renormalized coupling g_R(sigma)., The H,K collar/hairpin endpoint basis and the Schur block E with its spectral floor eta_sigma., The heat-kernel regulator sigma/a and the reflected Wilson normalization that cancels vacuum and perimeter terms., The Wilson-invariant quotient rules for sheet symmetries and trace identities.
- Expected observation: If the route is viable, the partial row-sum bound for M4_sigma^- stabilizes below m_G^sigma-e_OPE^sigma-s_HK^sigma; if it crosses that margin, the endpoint-box route has a concrete valid falsifier.
- Transfer certificate needed: A same-regulator interval proof that every omitted shell is bounded by epsilon_tail(L_max), every hyperedge is counted once, and the resulting gamma_sigma interval is invariant under Wilson sheet symmetries.

## Next Experiment

Build the first same-regulator endpoint-box table: enumerate collar/hairpin sheets, compute C_sigma color-square entries, extract or bound kappa4 shell row sums through L_max=2, insert the known S_HK interval, and report gamma_sigma with a falsifier flag.
