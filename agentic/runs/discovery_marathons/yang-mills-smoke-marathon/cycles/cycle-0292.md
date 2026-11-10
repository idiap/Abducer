# cycle-0292

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint dominance interval certificate for the heat-kernel three-hairpin block

## Candidate Lemma

Finite endpoint dominance theorem: for the post-H,K three-hairpin null channel, the connected boundary-OPE endpoint contribution is certified by same-theory source cumulant intervals and fractional incidence intervals. If the resulting interval has nonnegative lower endpoint, the finite reflected-Wilson OS block passes this gate; if its upper endpoint is negative, it is a finite same-theory falsifier. This does not claim continuum OS reconstruction or a mass gap.

## Definitions

- source object: the fixed three-hairpin reflected Wilson collar block in four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action and plaquette-sheet Wilson regulator, after the already computed H,K Schur-Feshbach reduction to the null endpoint channel.
- target object: the scalar finite-block post-H,K OS gate I_gate whose sign decides only this regulated reflected-Wilson endpoint transfer, not the Clay continuum theory or Hamiltonian mass gap.
- controlled interface: replace the connected boundary-OPE polarization R by endpoint source classes E carrying seven source values, cumulant interval kappa_E, fractional incidences b_ij,E, color factor C_N, Gaussian margin M_G, and a uniform tail interval T_tail.
- same-theory condition: every kappa_E is a derivative of the same regulated Wilson partition function and uses the same gauge-invariant Wilson normalization as the collar OS matrix; no boundary counterterm, auxiliary edge Hilbert space, or changed observable algebra is allowed.
- Endpoint source class E: a set of endpoint boxes with identical regulated source data up to certified interval tolerance, not merely geometrically similar boxes.
- Null dominance D_E: the incidence contraction D_E=2 b_12,E-4 b_13,E-4 b_23,E inherited from the Feshbach null vector and the previously fixed hairpin pairing weights.

## Assumptions

- Model: SU(N) Euclidean lattice Yang-Mills in four dimensions with heat-kernel plaquette action and gauge-invariant Wilson plaquette-sheet sources.
- Regime: fixed finite hairpin block, fixed endpoint box scale above the lattice cutoff, and the previously established H,K null-channel reduction.
- Cutoff: all source derivative intervals, incidence intervals, M_G, and T_tail are uniform for sufficiently small lattice spacing and sufficiently large volume.
- Same-theory: the endpoint source partition functions are restrictions of the same regulated Wilson theory used to define the reflected OS matrix.
- Validity: Wick-square connected-log contributions are removed or positive Gram terms, and the straight nonabelian f f contact cancels by the null incidence identity.
- Local: all nonendpoint overlap and corner leakage not represented by endpoint classes is charged to T_tail with a signed interval, not silently discarded.

## Equations

- seven_point_endpoint_kappa4: `\widehat\kappa_E(h)=\frac{-F_E(-3h)+12F_E(-2h)-39F_E(-h)+56F_E(0)-39F_E(h)+12F_E(2h)-F_E(3h)}{6h^4},\quad F_E(s)=\log Z_E(s)`. Valid when: Valid when F_E is the same-theory heat-kernel endpoint source free energy and has a cutoff-uniform eighth source derivative on the chosen source interval.
- stencil_error_interval: `|\widehat\kappa_E(h)-\kappa_E|\le \frac{7h^4}{240}M_{8,E},\quad \kappa_E=\partial_s^4F_E(0)`. Valid when: Applies after the endpoint source class has a certified bound M_{8,E} for the eighth derivative uniformly in cutoff and volume.
- null_dominance_and_shield: `D_E=2b_{12,E}-4b_{13,E}-4b_{23,E}=2\bigl(b_{12,E}-2(b_{13,E}+b_{23,E})\bigr),\quad b_{13,E}+b_{23,E}\ge b_{12,E}/2\Rightarrow D_E\le0`. Valid when: Valid for the fixed three-hairpin Feshbach null vector and fractional endpoint incidences measured in the heat-kernel plaquette-sheet regulator.
- certified_gate_interval: `I_{\rm gate}\in M_G+C_N\sum_E n_E\,[\kappa_E^-,\kappa_E^+]\,[D_E^-,D_E^+]+[T_{\rm tail}^-,T_{\rm tail}^+]`. Valid when: Requires source-equivalent endpoint classes, positive color factor C_N, certified incidence intervals, and all leftover endpoint leakage included in T_tail.
- danger_budget_lower_bound: `I_{\rm gate}\ge M_G^-+T_{\rm tail}^- - C_N\sum_E n_E[-\kappa_E^-]_+[D_E^+]_+`. Valid when: Valid as a conservative promotion bound when the only sign-dangerous endpoint term is negative kappa4 multiplied by positive null dominance.

## Attempted Derivation

- Start with the already reduced null-channel scalar I_gate=M_G+C_N sum_v kappa_v D_v+T_tail for the heat-kernel plaquette-sheet regulator.
- Use connected log source derivatives F_v(s)=log Z_v(s) so Gaussian Wick-square pieces do not enter kappa_v; the remaining local compact-group fourth cumulant is measured by the seven-point fourth derivative.
- Use the previous null-incidence cancellation of the straight nonabelian f f contact, so endpoint/corner boxes are the only represented dangerous support.
- Partition endpoint boxes into source-equivalent classes E. Replace individual kappa_v by certified intervals [kappa_E^-,kappa_E^+] and individual D_v by fractional incidence intervals [D_E^-,D_E^+].
- Apply interval multiplication and add M_G and T_tail. The half-overlap shield is visible algebraically: if b_13+b_23>=b_12/2 then D_E<=0 and negative kappa_E cannot lower the gate.
- Promotion requires I_- >= 0. A finite falsifier requires I_+ < 0, or a same-theory failure such as nonuniform tail or added boundary counterterm.

Blocking gap: No actual seven source values, M_8 bounds, fractional incidence table, or signed T_tail interval have yet been supplied for the concrete endpoint boxes.

## Falsifiers

- A certified source class with D_E^+>0 and kappa_E^- negative enough to make I_gate^+<0 is a finite OS falsifier for this same-theory block.
- Two endpoint boxes merged by geometry but separated by their seven regulated source values falsify source-equivalence compression.
- A nonuniform endpoint/corner tail as a->0 invalidates the local carrier even if all local kappa intervals are safe.
- Any boundary counterterm needed to define F_E(s) changes the theory and demotes the bridge.
- A reflection-asymmetric endpoint source convention breaks the null-incidence cancellation and invalidates the D_E formula.

## Learning

Conceptual pressure attacked: endpoint collapse must be sign-certified in the same Wilson theory rather than hidden in symbolic R. Declarative tension: finite collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold without adding a boundary theory; the missing mediator is a cutoff-uniform endpoint source interval. Carrier critique: raw R is too weak because it hides b_ij signs; raw kappa4 spectrum is too strong because negative kappa4 is harmless under the half-overlap shield; the global Schur-preimage test is valid but too coarse after H,K. Efficient representation: encode endpoint source classes, seven source values, kappa intervals, fractional incidences, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; use source differentiation, interval arithmetic, source-equivalence, color multiplication, clipping, incidence contraction, and tail addition; identify equivalents only by regulated source data; keep locality finite through T_tail; export only the scalar interval to the finite OS gate. Hard gate changed: the finite post-H,K reflected-Wilson OS transfer gate can now be promoted, falsified, or quarantined by actual endpoint data. Conceptual value signal: sharpness and route change at finite scope; certified 12-dominance plus uncontrolled tail is the obstruction, not negative endpoint kappa4 itself. Clay continuum construction, full OS/Wightman reconstruction, nontriviality, and positive Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and data-design guide.`
- Rationale: The branch has saturated abstract endpoint-carrier language; the remaining decision is whether certified fractional 12-dominance can actually overcome the Gaussian margin in the same heat-kernel Wilson theory.
- Situation seed: SU(2) heat-kernel plaquette-sheet endpoint box for the fixed three reflected Wilson hairpins, with one endpoint source class E and singlet four-flux source F_E(s)=log Z_E(s).
- Varied variable: alpha=(b_13,E+b_23,E)/b_12,E, the fractional half-overlap ratio, varied across the shield value alpha=1/2 while kappa_E<0, C_N, and M_G are held fixed.
- Held-fixed controls: Same heat-kernel plaquette action and Wilson normalization for collar and endpoint sources., The already computed H,K null-channel reduction and its weights 2,-4,-4., No boundary counterterm and no change of gauge-invariant observable algebra., Uniform endpoint box scale and identical seven-point source stencil h.
- Expected observation: For alpha>=1/2 the endpoint class cannot lower I_gate through negative kappa4; for alpha<1/2 it lowers the gate by 2C_N|kappa_E|b_12,E(1-2alpha) plus tail, giving a quantitative demotion threshold.
- Transfer certificate needed: Actual source interval [kappa_E^-,kappa_E^+], cutoff-uniform M_8 error, certified fractional incidences, and signed T_tail must be produced before the thought experiment can affect proof obligations.

## Next Experiment

Compute the concrete SU(2) heat-kernel endpoint source stencil for the most 12-dominant endpoint class: evaluate F_E(lh) for l=-3,...,3, bound M_8,E, measure b_12,b_13,b_23, add T_tail, and report the interval for I_gate. If this cannot be done next, quarantine this branch as representation-complete but data-incomplete.

# Gauge-Invariant Nontriviality Witness Selection -> finite Route A endpoint R certificate

## Candidate Lemma

Conditional Ward-Hessian endpoint-cell enclosure for the post-H,K plus-channel Wilson mediator: after gradient flow, centering, perimeter/cusp subtraction, Ward subtraction, and plus-current monopole/dipole cancellation, the connected boundary-OPE polarization is bounded by endpoint second moments and certified near/far Hessian constants. A positive lower interval for R_{++}^{ren} promotes only finite endpoint-box positivity.

## Definitions

- source object: finite-cutoff pure SU(N) Wilson lattice gauge theory on a reflection-symmetric box, with gradient-flowed thin H,K endpoint hairpin sheet currents J_+^{a,t} and boundary point splitting epsilon.
- target object: the finite Route A endpoint-box scalar R_{++}^{ren}(t,a) entering the post-H,K Schur-Feshbach plus-channel inequality against the leakage constant L_+.
- controlled interface: the map from two centered renormalized flowed Wilson hairpins to their connected covariance, represented by endpoint sheet-current moments and Ward-subtracted four-curvature kernels.
- same-theory condition: the Wilson action, gauge group, reflection plane, flow time, endpoint geometry, normalization, and counterterms are identical to those used in the finite H,K positivity matrix.
- bridge/carrier: endpoint sheet currents with color convention tr(T^aT^b)=delta^{ab}/2, cell moments M_{0,+}, M_{1,+}, M_{2,+}, and sector kernels K_{3g}, K_{4g}, K_{ct}, K_{end}.
- preserved observables: gauge-invariant centered flowed Wilson hairpin covariances; the recovery map Pi_flow sends current data back to the same cutoff Wilson observable before any OS reconstruction.
- error budget: pair lower interval G_{++}^{I,-}, Ward-Hessian upper interval H_{4,++}^{I,+}, sixth-order remainder E_6^{I,+}, and Schur-Feshbach leakage L_+.

## Assumptions

- Model: pure SU(N) Yang-Mills regularized by the Wilson plaquette action at spacing a in finite volume, with gradient flow time t>0 and reflection-symmetric endpoint boxes.
- Regime: a << sqrt(8t) < d_endpoint and endpoint cell diameter eta sqrt(8t) is smaller than the collar separation used in the H,K construction.
- Cutoff: all curvature insertions are flowed before coincidence limits; boundary point splitting epsilon is removed only after perimeter and cusp counterterms cancel in the centered covariance.
- Same-theory: the covariance, counterterms, finite positivity matrix, and leakage L_+ are computed with the same cutoff measure and the same reflected Wilson observable family.
- Uniformity: constants H_{near}^{I,+} and H_{far}^{I,+} are required to be volume-stable and cutoff-stable over the certified interval a/sqrt(8t) in I; no continuum uniformity is claimed outside I.
- Local: the plus endpoint current satisfies certified zero monopole and zero first moment after H,K symmetrization, so the Hessian remainder is the first surviving endpoint Taylor term.
- Validity: large-field and topological summability across RG steps are not discharged; compact finite-lattice integrals make this only a finite Route A certificate.
- Constraint: if R_{++}^{I,-} beats L_+ it changes finite endpoint-box positivity only, leaving continuum existence, OS/Wightman reconstruction, observable density, and Hamiltonian mass gap untouched.

## Equations

- centered flowed hairpin observable: `\widehat W_J^{t,a}=Z_{\rm cusp}^{-1}(a,t,\epsilon)Z_{\rm per}^{-1}(a,t,\epsilon)\bigl(W_J^{t,a}-\langle W_J^{t,a}\rangle_a\bigr)`. Valid when: Valid when flowed Wilson hairpins use the same cutoff measure and the same perimeter and cusp counterterms as the finite H,K matrix.
- endpoint mediator as connected covariance: `R_{++}^{\rm ren}(t,a)=\kappa_2\bigl(\widehat W_{J_+}^{t,a},\widehat W_{J_+}^{t,a}\bigr)`. Valid when: Valid when centering removes the disconnected product and both hairpins are the reflected plus-channel endpoint observables.
- pair-plus-polarization decomposition: `R_{++}^{\rm ren}=g_t^4(N^2-1)\bigl(2G_{++}+N C_{4,++}^{\rm WS}\bigr)+O(g_t^6E_6)`. Valid when: Applies after diagonal normalization, gradient-flow renormalization, and Ward/cusp subtraction in the finite endpoint-box regime.
- connected four-curvature polarization: `C_{4,++}^{\rm WS}=\int J_+^{\otimes 4}(x_1,x_2,y_1,y_2)\,K_4^{\rm WS}(x_1,x_2;y_1,y_2;t,a)\,dx_1dx_2dy_1dy_2`. Valid when: Valid when the Ward-subtracted kernel is tested only against the same endpoint sheet current used to define the Wilson hairpins.
- plus-current moment cancellation: `\sum_{b\subset E}q_b=0,\qquad \sum_{b\subset E}q_b(x_b-x_E)=0,\qquad M_{2,+}(E)=\sum_{b\subset E}|q_b|\,|x_b-x_E|^2`. Valid when: Requires the H,K plus-channel endpoint symmetrization and the certified orientation signs of all endpoint cells.
- Ward-Hessian polarization bound: `|C_{4,++}^{\rm WS}|\le M_{2,+}^2\bigl(H_{near}^{I,+}(t,a,\rho)+H_{far}^{I,+}(t,a,\rho)\bigr)+E_{ct}^{I,+}`. Valid when: Valid when near cells use flowed heat-kernel majorants and far cells use second-order Taylor remainders after monopole and dipole cancellation.
- certified lower interval: `R_{++}^{I,-}=g_t^4(N^2-1)\Bigl(2G_{++}^{I,-}-N M_{2,+}^2(H_{near}^{I,+}+H_{far}^{I,+})\Bigr)-g_t^4N(N^2-1)E_{ct}^{I,+}-E_6^{I,+}`. Valid when: Applies when every interval endpoint is outward-rounded and all sector kernels are evaluated in the same cutoff and flow window.
- finite Route A promotion inequality: `R_{++}^{I,-}>L_++\delta_{route}\quad(\delta_{route}>0)`. Valid when: Valid as a finite endpoint-box positivity certificate once L_+ is the Schur-Feshbach leakage from the same H,K reduction.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: finite-cutoff pure SU(N) Wilson lattice gauge theory on a reflection-symmetric box, with gradient-flowed thin H,K endpoint hairpin sheet currents J_+^{a,t} and boundary point splitting epsilon.; target object: the finite Route A endpoint-box scalar R_{++}^{ren}(t,a) entering the post-H,K Schur-Feshbach plus-channel inequality against the leakage constant L_+.; Model: pure SU(N) Yang-Mills regularized by the Wilson plaquette action at spacing a in finite volume, with gradient flow time t>0 and reflection-symmetric endpoint boxes..
- Attack conceptual pressure: finite Schur-Feshbach positivity needs a same-theory endpoint mediator, while positive pair covariance can be erased by the connected four-curvature polarization.
- Fix the source theory: finite SU(N) Wilson plaquette measure, gradient flow time t, reflected H,K endpoint hairpins, and the same perimeter/cusp counterterms used in the finite positivity matrix.
- Represent each hairpin by a flowed endpoint sheet current. This carrier is sharper than raw Wilson contours because Ward subtraction, moment cancellation, zero-pairing quotienting, and interval Hessian bounds become primitive operations.
- Center the two hairpin observables; the disconnected product cancels in kappa_2 and one-hairpin perimeter/cusp factors are removed before the endpoint point-splitting limit.
- Expand the connected covariance through order g_t^4. The two cross pairings give the positive baseline 2(N^2-1)G_{++}; the non-Gaussian endpoint uncertainty is N(N^2-1)C_{4,++}^{WS}.
- Decompose K_4^{WS} into K_{3g}+K_{4g}+K_{ct}+K_{end}. Ward subtraction removes longitudinal zeroth and first endpoint terms; H,K plus-channel symmetry cancels monopole and dipole moments of J_+.
- Split endpoint cells into near and far regions at rho sqrt(8t). Near terms are bounded by flowed heat-kernel majorants plus counterterm intervals; far terms use Taylor expansion with second derivatives in endpoint coordinates.
- Combine the bounds to obtain |C_{4,++}^{WS}| <= M_{2,+}^2(H_{near}^{I,+}+H_{far}^{I,+})+E_{ct}^{I,+}, then subtract this from the explicit positive pair baseline to get R_{++}^{I,-}.
- Compare R_{++}^{I,-} with the already finite Schur-Feshbach leakage L_+. Success promotes finite endpoint-box positivity after H,K; failure quarantines this R repair only.

Blocking gap: The missing mediator is numerical-analytic certification of H_{near}^{I,+}, H_{far}^{I,+}, E_{ct}^{I,+}, and E_6^{I,+} for the actual flowed SU(N) four-curvature sectors with cutoff-stable Ward/cusp cancellation.

## Falsifiers

- falsifier: the Ward-subtracted four-curvature Hessian has an uncancelled log epsilon or power divergence after perimeter/cusp subtraction.
- falsifier: the plus-channel endpoint current fails the certified zero monopole or zero dipole test for the actual H,K geometry.
- falsifier: N M_{2,+}^2(H_{near}^{I,+}+H_{far}^{I,+}) is larger than 2G_{++}^{I,-} in every admissible flow window.
- falsifier: R_{++}^{I,-} does not exceed the same-theory Schur-Feshbach leakage L_+, so endpoint-box positivity is not repaired.
- falsifier: lattice-flow measurements or interval quadrature show no plateau as a/sqrt(8t) decreases with fixed physical endpoint geometry.
- falsifier: zero-pairing quotienting changes the flowed Wilson covariance, revealing a representation-limited carrier.

## Learning

Conceptual pressure attacked: the missing same-theory mediator between finite Schur-Feshbach positivity and Wilson cumulant positivity. Declarative tension: positive pair covariance, gradient-flow renormalization, and endpoint positivity must jointly be valid, but C4 can erase the pair term unless Ward-Hessian constants are certified. Carrier critique: raw Wilson contours are fragmented and global OS/non-Gaussian witnesses are too coarse for this local obstruction; endpoint sheet currents are sharper but must pass zero-pairing and recovery-map tests. Compared abstraction: a continuum OS spectral-transfer route is premature, while finite interval proof search directly changes the hard gate of post-H,K endpoint-box positivity. Efficient representation requirements: encode H,K sheets, endpoint currents, cell moments, sector kernels, and counterterms; preserve gauge, color, reflection, orientation, cutoff, and same-theory invariants; use cumulant expansion, Ward/cusp subtraction, endpoint Taylor expansion, heat-kernel majorants, interval quadrature, outward rounding, and zero-pairing quotienting as primitives; keep locality to endpoint cells and finite refinement depth; transfer only through centered flowed Wilson cumulants; demote on any falsifier. Conceptual value signal: R_{++}/kappa_4 becomes a route-deciding color-geometric near/far interval rather than a symbolic endpoint term. Success promotes one finite Route A gate; failure quarantines this repair. Clay existence, OS/Wightman axioms, nontrivial continuum limit, observable density, large-field/topology control, and Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and constant-calibration experiment for the finite endpoint-box gate.`
- Rationale: The branch has already isolated the R term abstractly; another restatement is low value. The decisive valid information is whether near/far Ward-Hessian constants can be small enough to preserve the positive pair baseline in the same Wilson theory.
- Situation seed: Finite SU(2) and SU(3) Wilson plaquette lattices with reflection-symmetric H,K endpoint hairpins, gradient-flowed at t, centered and cusp-renormalized, evaluated by endpoint sheet-current interval cells in one fixed physical endpoint box.
- Varied variable: rho=eta/sqrt(8t), the near/far split radius measured in flow units, with endpoint geometry otherwise fixed.
- Held-fixed controls: Same Wilson action, gauge group, reflection plane, H,K endpoint geometry, and plus-channel orientation signs., Same gradient-flow definition, perimeter/cusp subtraction, point-splitting order, and Schur-Feshbach leakage L_+., Same color normalization tr(T^aT^b)=delta^{ab}/2 and same endpoint current quotient policy., Finite volume chosen large enough that endpoint boxes are isolated from periodic images; no continuum OS transfer is inferred.
- Expected observation: If the route is viable, G_{++}^{I,-} remains positive while M_{2,+}^2(H_{near}^{I,+}+H_{far}^{I,+}) decreases or plateaus as rho is optimized, producing a stable positive interval for R_{++}^{I,-}-L_+. If it fails, the connected polarization or interval width overwhelms the pair term.
- Transfer certificate needed: A cutoff- and volume-stable interval proof that the measured or computed constants enclose the same flowed Wilson cumulant with Ward/cusp cancellation; only then may the intuition affect the finite Route A proof queue.

## Next Experiment

Build the endpoint-cell interval table for the actual H,K plus hairpin: compute G_{++}^{I,-}; decompose K_4^{WS} into K_{3g}, K_{4g}, K_{ct}, K_{end}; certify Ward/cusp cancellation; then evaluate H_{near}^{I,+}(rho) and H_{far}^{I,+}(rho) for three rho values to decide whether R_{++}^{I,-}-L_+ has a stable positive sign.

# Raw plaquette interval certificate for post-H,K Wilson endpoint positivity

## Candidate Lemma

Conditional finite Route A theorem: in a fixed heat-kernel plaquette cutoff theory, a positive raw interval margin Delta_raw(sigma) certifies Schur-corrected endpoint-box positivity for the worked H,K collar/hairpin geometry; a certified negative stress vector is a falsifier for this finite geometry only.

## Definitions

- source object: finite-volume cutoff SU(N) Yang-Mills Wilson/heat-kernel plaquette measure mu_{a,L,sigma,g} with oriented endpoint plaquette sheets, transported color plaquette variables, Wilson normal ordering, and fixed H,K hairpin data.
- target object: finite-dimensional post-H,K endpoint quadratic form on the vacuum-subtracted Wilson endpoint box E, namely the Schur-corrected block R_raw,sigma-S_HK compressed to the chosen endpoint basis.
- controlled interface: raw plaquette interval recovery map Rec_raw sending same-regulator connected plaquette cumulant intervals and OPE remainder intervals to a rigorous lower bound on lambda_min(R_raw,sigma-S_HK).
- same-theory condition: all plaquette cumulants, Wilson/OPE coefficients, normal-ordering constants, Schur blocks, coupling, cutoff a, smearing sigma, volume L, color normalization, boundary sheets, and reflection plane are identical; no continuum limit, OS spectral transfer, or Clay mass-gap conclusion is claimed.

## Assumptions

- Model: four-dimensional finite hypercubic collar or torus with compact SU(N) links and heat-kernel plaquette action at fixed a,L,sigma,g.
- Cutoff: sigma>=a and all endpoint plaquette sheets lie in one finite reflection-positive endpoint box with no limit a downarrow 0 taken in the claim.
- Same-theory: H,K Schur data and boundary Wilson cumulants are evaluated in the same cutoff measure, not imported from another regulator or RG basin.
- Validity: the boundary Wilson/OPE expansion through quadratic curvature flux has a certified interval remainder E_OPE on the endpoint basis.
- Local: QHQ on the H,K complement is strictly positive on the finite subspace, so S_HK=B^*E^{-1}B is a well-defined finite Schur subtraction.
- Uniformity: no volume-uniform, cutoff-uniform, large-field, topology-summability, or regulator-independent estimate is assumed beyond this finite endpoint box.

## Equations

- transported plaquette flux variable: `Y_{p,\sigma}^{a}=w_p(\sigma)\,\mathrm{tr}\!\left(T^a\,U_{\gamma_p}\,\frac{U_p-U_p^\dagger}{2ia^2}\,U_{\gamma_p}^{-1}\right)_{\mathrm{tf}}`. Valid when: Valid when the heat-kernel smeared plaquette p is transported to a fixed endpoint basepoint and the SU(N) generators satisfy tr(T^a T^b)=delta^{ab}/2 in the finite cutoff theory.
- raw endpoint polarization cumulant: `R^{\mathrm{raw}}_{ij,\sigma}=\operatorname{cum}_{2,\mu_{a,L,\sigma,g}}(Q_{i,\sigma},Q_{j,\sigma}),\quad Q_{i,\sigma}=:\!\sum_{p,q\in S_i}W_{i,pq}^{ab}Y_{p,\sigma}^{a}Y_{q,\sigma}^{b}\!:_{\mu}`. Valid when: Valid when the endpoint observables Q_i are vacuum-subtracted and normal ordered in the same cutoff measure, so disconnected vacuum and perimeter terms cancel before the Schur subtraction.
- Gaussian plus connected kappa4 decomposition: `R^{\mathrm{raw}}_{\sigma}=\alpha_N g_R^4\,(C_\sigma\circ C_\sigma)+\frac{g_R^4}{16N^2}K^{\mathrm{raw}}_{4,\sigma}+E_{\mathrm{OPE},\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when the Wilson/OPE expansion is truncated at quadratic transported curvature flux, crossed two-curvature contractions use the stated color normalization, and all remaining connected four-curvature terms are placed in K_raw_4 with an interval OPE remainder.
- raw kappa4 plaquette interval: `(K^{\mathrm{raw}}_{4,\sigma})_{ij}=\sum_{p,q\in S_i}\sum_{r,s\in S_j}W_{i,pq}^{ab}W_{j,rs}^{cd}\,\operatorname{Cum}_4(Y_p^a,Y_q^b,Y_r^c,Y_s^d)\in [\underline K_{ij},\overline K_{ij}]`. Valid when: Valid when every transported plaquette four-cumulant interval is computed in the same finite heat-kernel measure and summed with outward-rounded interval arithmetic over the unquotiented oriented plaquette list.
- Schur-corrected lower margin: `\lambda_{\min}(R^{\mathrm{raw}}_{\sigma}-S_{HK})\ge m_G(\sigma)-\frac{g_R^4}{16N^2}\rho_I^-(K^{\mathrm{raw}}_{4,\sigma})-e_{\mathrm{OPE}}(\sigma)-s_{HK}=\Delta_{\mathrm{raw}}(\sigma)`. Valid when: Valid when m_G is the certified minimum eigenvalue of the compressed Gaussian Hadamard-square block, rho_I^- bounds the possible negative spectral part of the kappa4 interval matrix, and s_HK bounds the finite Schur hairpin energy.
- finite promotion condition: `\Delta_{\mathrm{raw}}(\sigma)>0\;\Longrightarrow\;R^{\mathrm{raw}}_{\sigma}-S_{HK}\succ 0\text{ on }E`. Valid when: Valid when the preceding interval lower bound is rigorous on the chosen finite endpoint basis and QHQ remains invertible with the same H,K data used to define S_HK.

## Attempted Derivation

- Conceptual pressure attacked: mediate actual connected Wilson cumulants to Schur-corrected endpoint positivity without inflating a finite Wilson calculation into the Clay mass-gap theorem.
- Declarative tension: Wilson/OPE coefficients, connected kappa4 negativity, OPE errors, and H,K Schur energy must be valid in one cutoff theory, while continuum OS reconstruction, observable density, regulator-independent Schwinger functions, and physical-unit spectral transfer remain non-claims.
- Carrier critique: scalar R is representation-limited, full gauge-invariant OS observable density is too strong and circular for this local gate, shell A012 compression is convenient but quarantined, and raw plaquette enumeration is fragmented yet valid.
- Abstraction comparison: the sheet-kernel hypergraph unifies locality and color but still hides missing cumulant intervals; raw plaquette proof search is less elegant but exposes every transported cumulant, cancellation, and interval arithmetic obligation.
- Efficient representation requirements: encode oriented plaquettes, sheet weights W_i,pq, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/kappa4 separation, endpoint compression, and same-theory normalization; support cumulant contraction, interval summation, row/operator bounds, quotient auditing, and Schur subtraction; quotient only by exact Wilson identities; keep finite endpoint complexity; transfer only through Rec_raw and Delta_raw; falsifiers are negative stress vectors, margin failure, or non-invariant intervals.
- Fix the heat-kernel regulator and define transported plaquette variables Y_p^a; this preserves gauge-invariant Wilson observables because each plaquette insertion is parallel transported inside the traced endpoint sheet observable.
- Define Q_i as the normal-ordered quadratic boundary flux recovered from the endpoint Wilson OPE; connected cumulants cancel vacuum, disconnected perimeter, and one-point pieces before any positivity claim.
- Apply the cumulant identity for cum_2(:Phi_i^2:,:Phi_j^2:): crossed two-point contractions give the positive Hadamard-square Gaussian block with color factor alpha_N, while all non-Gaussian connected four-curvature terms form K_raw_4.
- Compress the resulting matrix to the post-H,K endpoint basis and subtract S_HK=B^*E^{-1}B from the finite Schur-Feshbach theorem.
- Use Weyl/Gershgorin interval bounds to obtain lambda_min(R_raw-S_HK)>=Delta_raw; this is the hard gate because Delta_raw>0 promotes finite endpoint-box positivity, while a negative stress vector kills this H,K route.

Blocking gap: No rigorous same-regulator numerical intervals for the transported plaquette four-cumulants Cum_4(Y_p,Y_q,Y_r,Y_s) are presently available; large-field and topology contributions to those finite intervals are not yet bounded.

## Falsifiers

- falsifier: Delta_raw(sigma)<=0 after sharp same-regulator interval computation and no positive margin survives Schur subtraction.
- falsifier: a rational endpoint vector v has certified U(v,sigma)<0 for v^*(R_raw-S_HK)v, proving finite endpoint positivity fails for this H,K geometry.
- Quotient compression changes any unquotiented raw interval entry, showing the representation used a non-valid Wilson identity.
- The OPE remainder interval e_OPE is of the same size as or larger than the Gaussian Hadamard-square lower eigenvalue m_G.
- The connected kappa4 negative row/operator bound grows with endpoint plaquette count faster than the Gaussian square in the finite box.
- The OS null quotient or reflection support removes the chosen endpoint Wilson combination, so the stress vector is not a valid physical finite witness.
- The Schur hairpin energy s_HK exceeds every certified raw polarization lower bound for admissible sigma/a.

## Learning

Cycle 292 produces a sharper finite bridge: R is the raw same-regulator connected plaquette cumulant cum_2(Q_i,Q_j), decomposed into a positive Gaussian color Hadamard square, one connected kappa4 interval matrix, an OPE interval, and the H,K Schur subtraction. The hard gate is Delta_raw>0 or a negative stress vector. This is valuable without implying the Clay theorem because it decides only the finite post-H,K endpoint-box positivity gate; continuum existence, OS/Wightman reconstruction, nontriviality, observable density, and Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and as the concrete next proof-search benchmark.`
- Rationale: The branch has quarantined symbolic shell thresholds; only a same-regulator raw plaquette interval can decide whether the connected boundary-OPE polarization beats the H,K Schur subtraction in the finite endpoint box.
- Situation seed: Finite SU(2) heat-kernel lattice Yang-Mills on a 4D reflected collar with two endpoint plaquette sheets from the worked H,K hairpin geometry; enumerate all oriented plaquette quadruples contributing to cum_2(:Phi_1^2:,:Phi_2^2:) and test Rec_raw.
- Varied variable: smearing ratio tau=sigma/a over a small discrete set, with all other cutoff data fixed.
- Held-fixed controls: same bare coupling g, color normalization tr(T^aT^b)=delta^{ab}/2, lattice spacing a, and finite collar volume L, same endpoint Wilson loops, plaquette sheets, H,K Schur block, reflection plane, and normal-ordering prescription, same unquotiented oriented plaquette list before any exact Wilson-identity quotient audit
- Expected observation: If tau is too small, OPE and kappa4 intervals should be wide; if tau is moderate, the Gaussian Hadamard-square block may increase relative to the negative kappa4 envelope, producing either Delta_raw>0 or a concrete stress-vector falsifier.
- Transfer certificate needed: A rigorous outward-rounded interval table for every transported plaquette four-cumulant, an audited exact quotient map or full unquotiented sum, an OPE remainder bound in the same regulator, and a certified finite Schur inverse for QHQ.

## Next Experiment

Instantiate the SU(2) reflected-collar H,K endpoint box at fixed a,L,g and tau=sigma/a=2; enumerate unquotiented oriented plaquette quadruples for Q_1,Q_2, compute interval enclosures for the first diagonal and off-diagonal K_raw_4 entries, then evaluate Delta_raw and the best rational stress vector upper bound.

