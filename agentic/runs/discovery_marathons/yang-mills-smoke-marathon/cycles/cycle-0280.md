# cycle-0280

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint source intervals for post-H,K Wilson gate

## Candidate Lemma

For the fixed three-hairpin reflected Wilson block in the heat-kernel plaquette-sheet regulator, the post-H,K Schur-Feshbach null-channel OS transfer is decided by one same-theory endpoint interval. Negative compact-group fourth cumulants are dangerous only after multiplication by positive endpoint dominance D_v>0; I_->=0 promotes this finite block, while I_+<0 gives a finite same-theory falsifier.

## Definitions

- source object: regulated SU(N) heat-kernel plaquette-sheet Schwinger functional on the fixed three-hairpin collar block, with endpoint boxes B_v and source partition functions Z_v(s).
- target object: intended finite same-theory OS quotient scalar for the post-H,K Schur-Feshbach null channel of the reflected Wilson block.
- controlled interface: endpoint source carrier C_ep=(B_v,L_v,beta_v,D_v,C_N,M_G,T_tail) maps regulated connected four-flux cumulants to a certified interval for the target scalar.
- same-theory condition: Wilson loops, endpoint sources, heat-kernel normalization, reflection map, and collar-removal limit are inherited from the original gauge-invariant lattice theory without boundary counterterms or algebra enlargement.
- bridge/carrier: C_ep stores seven source values per endpoint, fractional footprint incidences b_v^{ij}, color factor C_N=(g^4/4)(T_F/N)^2, Gaussian margin M_G, and a cutoff-uniform tail budget.
- observable manipulated: the connected endpoint four-flux cumulant kappa_{4,v}=d_s^4 log Z_v(0) after Wick-square and straight f f contact cancellations.

## Assumptions

- Model: four-dimensional pure SU(N) lattice Yang-Mills with reflection-positive heat-kernel plaquette-sheet regulator and locked gauge-invariant Wilson-loop algebra.
- Regime: finite three-hairpin block after the already computed H,K Schur-Feshbach reduction, with endpoint boxes smaller than the collar scale and larger than the cutoff scale.
- Cutoff: the eighth source-derivative bound M_{8,v} and tail T_tail are uniform for the endpoint-box scaling window a<<ell_v<<delta.
- Same-theory: endpoint sources are infinitesimal insertions used only to differentiate the original Wilson expectation and are set to zero before transfer to the OS gate.
- Uniformity: all remainders from non-endpoint overlaps, corners, and higher cumulants are charged to T_tail with a cutoff-independent upper interval.
- Validity: the finite claim does not assert continuum existence, full OS reconstruction, nontriviality, or a Hamiltonian mass gap.

## Equations

- fractional null endpoint dominance: `D_v=2b_v^{12}-4b_v^{13}-4b_v^{23}`. Valid when: Valid when B_v is an endpoint box in the heat-kernel plaquette-sheet regulator and b_v^{ij} are same-theory footprint fractions after the H,K null incidence contraction.
- seven-point connected fourth source stencil: `\widehat\kappa_{4,v}(h)=\frac{-f_v(-3h)+12f_v(-2h)-39f_v(-h)+56f_v(0)-39f_v(h)+12f_v(2h)-f_v(3h)}{6h^4},\quad f_v(s)=\log Z_v(s)`. Valid when: Applies when f_v is eight times source differentiable on |s|<=3h with all endpoint sources kept inside the same regulated Wilson theory.
- certified negative-cumulant interval: `\beta_v=-\kappa_{4,v}\in -\widehat\kappa_{4,v}(h)+[-7h^4M_{8,v}/240,\,7h^4M_{8,v}/240]`. Valid when: Valid when M_{8,v} bounds the eighth derivative of log Z_v throughout the seven-point source stencil in the endpoint box.
- finite endpoint OS gate interval: `[I_-,I_+]=[M_G^-,M_G^+]+C_N\sum_v[\kappa_{4,v}][D_v]+[-T_{tail}^+,T_{tail}^+],\quad I_-\ge M_G^- - C_N^+\sum_v\overline\beta_v[\overline D_v]_+-T_{tail}^+`. Valid when: Requires the post-H,K null-channel reduction, Wick-square Gram positivity, straight f f incidence cancellation, and cutoff-uniform endpoint tail control for the same Wilson block.

## Attempted Derivation

- Conceptual pressure attacked: endpoint collapse must be sign-certified while preserving finite collar OS positivity and the fixed gauge-invariant Wilson algebra.
- Declarative tension: collar positivity gives a positive quotient before endpoint collapse, the same-theory condition forbids boundary counterterms, and the connected endpoint OPE can be singular; the missing mediator is a cutoff-uniform source carrier that remembers incidence signs.
- Critique of current carrier: raw R is representation-limited because it forgets endpoint incidence, while raw kappa_4 spectrum is too strong because it treats every negative endpoint cumulant as dangerous.
- Compared routes: global Schur-preimage testing is exact but too coarse after H,K; the endpoint source carrier is local, computable, and transfers one scalar interval to the finite OS gate.
- Define heat-kernel endpoint sources Z_v(s) by inserting exp(s L_v) in the same regulated Wilson plaquette sheet and differentiating log Z_v at s=0.
- Use the connected logarithm to remove Wick-square contractions; use the already established null incidence identity to cancel the straight C_A f f contact along shared segments.
- Localize the remaining connected boundary OPE to endpoint boxes B_v plus a tail T_tail; write R_end=C_N sum_v kappa_{4,v} D_v + T_tail.
- Compute D_v=2b12-4b13-4b23, so negative leading kappa_4 lowers the margin only through [D_v]_+.
- Approximate kappa_{4,v} by the seven-point fourth source stencil and attach the rigorous 7h^4 M8/240 error interval.
- Combine the positive Gaussian Schur-Feshbach margin M_G, color factor C_N, beta intervals, D_v intervals, and T_tail into [I_-,I_+].

Blocking gap: No actual endpoint source data, M8 bound, and cutoff-uniform T_tail estimate have yet been supplied for the SU(N) endpoint boxes; without them the interval theorem is valid as a finite certificate but not a completed promotion.

## Falsifiers

- A cutoff-uniform computation with I_+<0 is a finite reflected-Wilson same-theory falsifier for the post-H,K OS transfer gate.
- The endpoint source derivative requires a boundary counterterm or altered Wilson normalization, breaking the same-theory condition.
- The eighth-derivative or large-field/topology tail bound grows with cutoff removal, so the interval is not valid for the intended endpoint collapse.
- Fractional footprint weights fail to converge or become regulator-scheme dependent, making D_v an invalid carrier.
- A corner tail with negative sign exceeds the Gaussian margin even when all 12-only endpoint boxes are absent.

## Learning

Cycle 280 attacks endpoint-collapse sign certification in the same Wilson theory. The declarative tension is collar OS positivity plus fixed gauge-invariant Wilson observables plus singular connected endpoint OPE, with no permission to add a boundary theory. Raw R is too weak and raw kappa_4 is too strong; C_ep is the sharper carrier because it records source data and incidence signs. Efficient representation: encode endpoint boxes, seven source values, beta intervals, fractional incidences, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; use source differentiation, interval arithmetic, color multiplication, clipping, and tail addition; identify carriers only by equal regulated source derivatives; keep locality finite through T_tail; export only [I_-,I_+] to the finite OS gate. Conceptual value signal: sharpness and route change at finite scope. Negative compact-group kappa_4 is not the falsifier; certified 12-dominance plus uncontrolled tail is. The Clay continuum and mass-gap gates remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and interval-calibration experiment.`
- Rationale: The branch has a finite post-H,K scalar gate; another abstract OS restatement would not decide whether endpoint collapse preserves the same Wilson theory.
- Situation seed: Finite SU(2) heat-kernel endpoint star for the same three reflected Wilson hairpins, with seven source evaluations of log Z_v in each endpoint box and the H,K null vector held fixed.
- Varied variable: Fractional 12-dominance p=b_v^{12} with b_v^{13}=b_v^{23}=(1-p)/2, so D_v=6p-4 and the dangerous region starts at p>2/3.
- Held-fixed controls: Same heat-kernel plaquette-sheet regulator and locked gauge-invariant Wilson observables., Same H,K Schur-Feshbach reduction, null vector, color factor C_N, and Gaussian margin M_G., Endpoint source is differentiated at zero and no boundary counterterm or algebra enlargement is allowed., Tail budget T_tail and derivative bound M8 are required to be cutoff-uniform in the endpoint scaling window.
- Expected observation: As p crosses 2/3, the negative Haar-quartic beta_v switches from protective/cancelled to margin-reducing; a certified interval crossing below zero would be a concrete finite falsifier, while a positive lower interval promotes this block.
- Transfer certificate needed: A uniform seven-point source-derivative interval, stable footprint fractions, and a no-boundary-renormalization certificate connecting the endpoint star back to the same regulated Wilson Schwinger functional.

## Next Experiment

Instantiate the SU(2) heat-kernel endpoint star, compute f_v(kh)=log Z_v(kh) for k=-3,...,3 in one 12-only endpoint box and one mixed 12/13 endpoint box, certify M8 and T_tail, then evaluate [I_-,I_+] for the fixed post-H,K null channel.

# Endpoint-current Hessian certificate for the post-H,K Wilson polarization

## Candidate Lemma

Endpoint-current Ward-Hessian lower interval. For a fixed H,K plus-channel endpoint box I, the same-theory flowed Wilson covariance R_{++}^I has the certified lower bound R_{++}^{I,-}=g_t^4(N^2-1)(2G_{++}^{I,-}-N H_{4}^{I,+}M_{2,+}^2)-E_{6}^{I,+}. If R_{++}^{I,-}>L_+^I-B_+^I, the finite endpoint-box Schur-Feshbach scalar is positive in this box; if not, the R repair is not promoted.

## Definitions

- source object: finite-cutoff four-dimensional SU(N) Yang-Mills Wilson ensemble with gradient-flow time t>0, endpoint box I, and centered plus-channel H,K hairpin sheet current J_+^I.
- target object: the finite Schur-Feshbach endpoint-box scalar Q_+^I=B_+^I+R_{++}^I-L_+^I whose positivity is meaningful before any continuum or spectral claim.
- controlled interface: the flowed Wilson covariance R_{++}^I supplies the boundary-OPE polarization input used only in the H,K finite tangent-cone certificate.
- same-theory condition: the Wilson cumulant, flow time, counterterms, current normalization, and Schur-Feshbach coefficients are taken from one regulator/RG basin candidate, with no imported dynamics.
- J_+^I is the oriented endpoint sheet-current representative of the plus hairpin combination after quotienting only by certified zero-pairing currents.
- G_{++}^{I,-} is a rigorous lower interval for the positive two-curvature reflected pairing of J_+^I.
- H_4^{I,+} is an upper interval for the operator norm of the Ward-subtracted connected four-curvature kernel Hessian on I.
- M_{2,+} is the second endpoint moment norm of J_+^I after plus-channel monopole and dipole cancellation.
- E_6^{I,+} bounds sixth and higher terms in the centered flowed Wilson cumulant expansion.

## Assumptions

- Model: finite hypercubic lattice or continuum cutoff SU(N) Yang-Mills with Wilson action, gradient-flow smearing, and gauge-invariant Wilson sheet observables.
- Regime: endpoint diameter eta is smaller than the flow radius sqrt(8t), and the reflected endpoint boxes are separated from nonlocal collars by a fixed positive distance.
- Cutoff: the intervals G_{++}^{I,-}, H_4^{I,+}, and E_6^{I,+} are computed with constants uniform for all a below a declared a0 at fixed physical t.
- Same-theory: the same flowed Schwinger/Wilson family supplies the pair term, the connected C4 term, the counterterms, and the finite Schur-Feshbach coefficients.
- Validity: Ward subtraction removes gauge-longitudinal pieces and perimeter/cusp counterterms remove one-hairpin local divergences before endpoint Taylor expansion.
- Local: the claim concerns one finite endpoint box and does not assert continuum existence, OS reconstruction, observable density, or a Hamiltonian mass gap.

## Equations

- plus-current endpoint moments: `\int_I J_+^I(x)\,dx=0,\qquad \int_I (x-x_I)_\alpha J_+^I(x)\,dx=0`. Valid when: Valid when the reflected plus hairpin current is represented by endpoint sheet currents after Ward and cusp subtraction.
- flowed covariance expansion: `R_{++}^I=g_t^4\{2(N^2-1)G_{++}^I+N(N^2-1)C_{4,++}^{WS,I}\}+O_6^I`. Valid when: Applies for the finite-cutoff centered flowed Wilson cumulant after perimeter and cusp renormalization in the endpoint box.
- Ward-Hessian C4 enclosure: `|C_{4,++}^{WS,I}|\le H_4^{I,+}M_{2,+}^2+E_{6}^{I,+}/(g_t^4N(N^2-1))`. Valid when: Requires zero monopole and dipole endpoint moments plus a valid Hessian interval for the Ward-subtracted four-curvature kernel.
- certified lower interval: `R_{++}^{I,-}=g_t^4(N^2-1)(2G_{++}^{I,-}-NH_4^{I,+}M_{2,+}^2)-E_6^{I,+}`. Valid when: Valid when all interval inputs are produced from the same regulator, flow time, current normalization, and endpoint partition.
- finite promotion test: `B_+^I+R_{++}^{I,-}-L_+^I>0`. Valid when: Applies only to the finite H,K endpoint-box Schur-Feshbach scalar, not to continuum spectral transfer.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: finite-cutoff four-dimensional SU(N) Yang-Mills Wilson ensemble with gradient-flow time t>0, endpoint box I, and centered plus-channel H,K hairpin sheet current J_+^I.; target object: the finite Schur-Feshbach endpoint-box scalar Q_+^I=B_+^I+R_{++}^I-L_+^I whose positivity is meaningful before any continuum or spectral claim.; Model: finite hypercubic lattice or continuum cutoff SU(N) Yang-Mills with Wilson action, gradient-flow smearing, and gauge-invariant Wilson sheet observables..
- Conceptual pressure attacked: finite Schur-Feshbach positivity needs a same-theory endpoint mediator; positive flowed pair covariance alone is not enough because the connected four-curvature polarization can erase it.
- Start with the centered flowed Wilson observable W(J_+^I)=\operatorname{Tr}\,P\exp(i\int J_+^I\cdot F_t) after perimeter and cusp subtraction.
- Expand the finite-cutoff covariance \kappa_2(W(J_+^I),W(J_+^I)) through fourth curvature order and isolate the positive pair term with color factor 2(N^2-1).
- Represent the connected C4 term by endpoint sheet-current cells and impose Ward subtraction before taking absolute values, preserving gauge, color, reflection, orientation, and same-theory invariants.
- Use plus-channel monopole and dipole cancellation to remove the constant and linear endpoint Taylor coefficients of the Ward-subtracted C4 kernel.
- Bound the remaining C4 contribution by a Hessian interval H_4^{I,+} times the squared second endpoint moment M_{2,+}^2, plus an explicit sixth-order remainder E_6^{I,+}.
- Insert the lower interval into Q_+^I=B_+^I+R_{++}^I-L_+^I to obtain the finite promotion or falsifier inequality.

Blocking gap: The missing proof object is a cutoff-uniform, Ward-respecting interval certificate for H_4^{I,+} and E_6^{I,+}; without it the lower interval is a sharp finite target but not yet a theorem.

## Falsifiers

- Ward subtraction leaves a residual endpoint dipole, invalidating the Hessian-only C4 estimate.
- The same-theory flowed Wilson normalization changes between G_{++}, H_4, E_6, and the Schur-Feshbach coefficients.
- The near-cell interval for K_4^{WS} is negative or too wide and makes 2G_{++}^{I,-}-NH_4^{I,+}M_{2,+}^2 nonpositive.
- The sixth-order cumulant remainder E_6^{I,+} is not small on the eta/sqrt(t) window.
- The cutoff plateau for R_{++}^{I,-} fails as a decreases at fixed physical flow time.
- Endpoint geometry has zero or nearly zero G_{++}^{I,-}, so the positive pair baseline cannot dominate.
- Large-field or topological sectors contribute non-summable tails across the regulator/RG window.

## Learning

Declarative tension: finite Schur-Feshbach positivity, positive flowed pair covariance, and same-theory Wilson renormalization must jointly hold, but C4 can erase the pair term unless a cutoff-uniform Ward-Hessian interval is valid. Carrier critique: raw Wilson contours are too fragmented; global non-Gaussian OS witnesses are too coarse for this local obstruction; endpoint sheet currents are sharper because Ward subtraction, moment cancellation, heat-kernel majorants, and interval arithmetic become primitive. Efficient representation requirements: encode H,K sheets, endpoint currents, cell moments, sector kernels, and counterterms; preserve gauge, color, reflection, orientation, cutoff, and same-theory invariants; use cumulant expansion, Ward/cusp subtraction, endpoint Taylor expansion, near/far heat-kernel bounds, and interval quadrature; quotient only by certified zero-pairing currents; keep locality to finite endpoint cells; transfer only through flowed Wilson cumulants; demote on Ward, cusp, plateau, geometry, cutoff-uniformity, or interval-width falsifier. Hard gate: finite endpoint-box positivity after H,K; success promotes one finite Route A gate, failure quarantines the R repair. Conceptual value signal: R_{++}/kappa_4 is now a computable color-geometric lower interval, not a symbolic threshold, while Clay existence, OS/Wightman axioms, nontrivial continuum limit, and positive Hamiltonian mass gap remain untouched. Reporting skill: timeline-definition-assumption-elicitor should audit definitions, assumptions, valid regimes, and non-claims.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the endpoint-current Hessian certificate.`
- Rationale: The branch already has a formal R_{++} interval; it now needs a concrete target-preserving stress case to test whether the C4 Hessian can really be made eta^2-suppressed relative to the positive pair baseline.
- Situation seed: A finite SU(N) Wilson lattice family with gradient-flow time t in physical units, one reflected H,K plus-hairpin endpoint box I, centered Wilson sheet currents, and Ward/cusp subtractions fixed.
- Varied variable: theta=eta/sqrt(8t), the endpoint-box diameter measured in flow-radius units.
- Held-fixed controls: Same Wilson lattice action, gauge group SU(N), reflection plane, H,K hairpin currents, and endpoint orientation data., Same perimeter/cusp counterterms, same gradient-flow definition, and same finite Schur-Feshbach leakage L_+^I., Same endpoint-cell partition rule up to uniform refinement and same zero-pairing current quotient policy.
- Expected observation: As theta decreases, G_{++}^{I,-} should plateau while H_4^{I,+}M_{2,+}^2 should scale like O(theta^4) or better after moment cancellation; failure of this scaling is a valid falsifier for the R repair.
- Transfer certificate needed: A cutoff-uniform interval plateau for G_{++}^{I,-}, H_4^{I,+}, and E_6^{I,+}, plus verified Ward identities and same-theory counterterm matching, before the observation can enter proof obligations.

## Next Experiment

Run proof search for one endpoint box: choose theta values 1/4, 1/6, 1/8; compute interval G_{++}^{I,-}; enclose K_{3g}, K_{4g}, K_{ct}, K_{end} Hessians by near-cell quadrature and far heat-kernel tails; bound E_6; report whether B_+^I+g_t^4(N^2-1)(2G_{++}^{I,-}-NH_4^{I,+}M_{2,+}^2)-E_6^{I,+}-L_+^I is positive, negative, or interval-inconclusive.

# Post-H,K same-regulator kappa4 shell certificate

## Candidate Lemma

Finite Route A certificate: for the heat-kernel SU(N) cutoff theory and the fixed H,K endpoint Wilson family, the Schur-corrected endpoint form is positive if the computable shell margin Delta_sigma is positive; if its rigorous upper interval is negative, the same data give a finite falsifier for this collar/hairpin route. This changes only the finite endpoint-box gate, not Clay-level existence or mass gap.

## Definitions

- source object: the finite heat-kernel regulated SU(N) lattice Yang-Mills measure mu_{a,L,g} and its reflected, perimeter-renormalized endpoint Wilson cumulants in a fixed endpoint box B.
- target object: the finite H,K endpoint-box quadratic form Q^B_sigma=R^B_sigma-S_{HK,sigma} on the vacuum-subtracted Wilson endpoint span.
- controlled interface: a sheet-kernel hypergraph encoding sheets Sigma_i, weights w_{i,p}, heat-kernel transporters, color tensors, reflection shells, OPE error intervals, and Schur data B_sigma,E_sigma.
- same-theory condition: R^B_sigma, C_sigma, K^{(4),B}_sigma, E^B_{OPE,sigma}, and S_{HK,sigma} are computed from the same cutoff measure, coupling, smearing sigma, Wilson normalization, and H,K basis.
- bridge observable: R^B_sigma is the connected boundary-OPE polarization of reflected Wilson observables after vacuum and perimeter cancellation.
- recovery map: cumulant_contract maps the hypergraph to C_sigma, K^{(4),B}_sigma, E^B_{OPE,sigma}, and S_{HK,sigma} without changing observables.

## Assumptions

- Model: finite hypercubic heat-kernel lattice Yang-Mills with compact group SU(N), N>=2, finite volume L, cutoff a>0, and a reflection plane compatible with B.
- Regime: sigma>=c a, the H,K endpoint Wilson loops are finite, and all sheets remain inside B at positive lattice distance from the boundary.
- Same-theory: all Wilson expectations, OPE coefficients, four-curvature cumulants, and Schur blocks use mu_{a,L,g} and the same renormalized coupling g_R(a).
- Validity: the fourth-order boundary OPE has an operator-norm remainder bounded by e_{OPE,sigma} on the endpoint Wilson span.
- Local: shell(i,j)=ell partitions only the finite sheet-kernel hypergraph of B; no continuum or volume-uniform summability is assumed.
- Constraint: E_sigma=QHQ is strictly positive on the hairpin complement, so S_{HK,sigma}=B_sigma^*E_sigma^{-1}B_sigma is well defined.

## Equations

- connected endpoint polarization: `R^{B}_{ij,\sigma}=\operatorname{Conn}_{\mu_{a,L,g}}(\widehat W_i,\theta\widehat W_j)\big|_{B,\mathrm{OPE}}`. Valid when: Valid when the heat-kernel cutoff, smearing, Wilson basis, and reflection plane are fixed before endpoint compression.
- transported curvature flux: `X_i^a(\sigma)=\sum_{p\in\Sigma_i}w_{i,p}(\sigma)\,\operatorname{Ad}_{U_{\gamma_{ip}}}^{ab}F_p^b`. Valid when: Valid when each sheet has a chosen basepoint transporter and heat-kernel smearing radius sigma at the cutoff a.
- Gaussian covariance and color factor: `C_{ij,\sigma}=\sum_a\langle X_i^a(\sigma)\,\theta X_j^a(\sigma)\rangle_{2,c},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after normalized trace convention tr_N(T^aT^b)=delta^{ab}/(2N) and color-diagonal two-curvature contraction.
- R decomposition: `R^{B}_{\sigma}=\alpha_N g_R^4(C_\sigma\circ C_\sigma)+\frac{g_R^4}{16N^2}K^{(4),B}_\sigma+E^{B}_{\mathrm{OPE},\sigma}`. Valid when: Requires the same-theory boundary OPE through fourth order and cancellation of vacuum and perimeter disconnected Wilson terms.
- shell envelope for kappa4 negativity: `A_\ell(\sigma)=\sup_i\sum_{j:\operatorname{shell}(i,j)=\ell}|K^{(4),B}_{ij,\sigma}|,\quad M_4^-(\sigma)\le \sum_\ell A_\ell(\sigma)`. Valid when: Valid when the finite sheet-kernel hypergraph has been quotient-audited by Wilson trace symmetries without changing matrix entries.
- Schur hairpin energy: `S_{HK,\sigma}=B_\sigma^*E_\sigma^{-1}B_\sigma,\quad s_{HK,\sigma}=\|S_{HK,\sigma}\|_{op}`. Valid when: Applies after the QHQ hairpin block is positive and the same endpoint basis is used for B_sigma.
- endpoint margin: `\Delta_\sigma=\alpha_N g_R^4\lambda_{\min}(C_\sigma\circ C_\sigma)-\frac{g_R^4}{16N^2}\sum_\ell A_\ell(\sigma)-e_{\mathrm{OPE},\sigma}-s_{HK,\sigma}`. Valid when: Valid when the Gaussian square, kappa4 shell envelope, OPE norm, and Schur subtraction are all certified in one cutoff theory.
- finite positivity conclusion: `Q^{B}_\sigma=R^{B}_\sigma-S_{HK,\sigma}\succeq \Delta_\sigma I`. Valid when: Applies only to the finite endpoint Wilson span after the preceding same-regulator interval bounds have been proved.

## Attempted Derivation

- Freeze claim level: finite same-regulator endpoint positivity only; no OS/Wightman reconstruction, nontrivial continuum limit, or Hamiltonian mass gap is claimed.
- Use the heat-kernel lattice regulator and expand the fixed H,K endpoint Wilson loops through fourth boundary-OPE order in transported curvature fluxes X_i^a(sigma).
- Apply exact vacuum subtraction and same-regulator perimeter normalization so the endpoint polarization is the connected cumulant Conn_mu(widehat W_i,theta widehat W_j).
- Evaluate the crossed two-curvature contraction: normalized SU(N) trace gives alpha_N=(N^2-1)/(8N^2), and Schur-product positivity gives alpha_N g_R^4(C_sigma o C_sigma)>=0.
- Represent the remaining connected four-curvature term as K^{(4),B}_sigma on the sheet-kernel hypergraph, then compress its negative spectral size by Gershgorin shell envelopes A_ell(sigma).
- Subtract the finite Schur-Feshbach hairpin energy S_HK=B^*E^{-1}B and collect the OPE remainder into e_OPE,sigma.
- The hard gate is Delta_sigma. If Delta_sigma>0, Q^B_sigma is positive on the finite endpoint span; if a certified interval forces Delta_sigma<0 or gives u^*Q^B_sigma u<0, the collar/hairpin route is falsified for this geometry.

Blocking gap: The first same-regulator numerical or symbolic interval for A_0(sigma) and A_1(sigma) of the actual H,K endpoint hypergraph is not yet certified; the current output supplies the valid carrier and inequality, not the finished interval.

## Falsifiers

- falsifier: a same-regulator endpoint vector u with u^*Q^B_sigma u<0 after exact H,K Schur subtraction demotes the Wilson collar/hairpin route.
- A_0(sigma)+A_1(sigma)+... exceeding 16N^2( alpha_N lambda_min(C o C)-e_OPE/g_R^4-s_HK/g_R^4 ) is a valid sign-size failure.
- Non-invariant sheet quotienting that changes any K^{(4),B}_{ij,sigma} invalidates the hypergraph carrier.
- A heat-kernel kappa4 tail with non-summable shell envelope destroys the finite-to-local transfer even before continuum questions arise.
- If E_sigma is not positive on the Q block, the Schur-Feshbach correction cannot be formed and the branch must backtrack to H,K geometry.

## Learning

Conceptual pressure attacked: mediate actual connected Wilson cumulants to Schur-corrected endpoint positivity without inflating a finite calculation into the Clay mass-gap theorem. Declarative tension: Wilson/OPE coefficients, connected kappa4 negativity, OPE error, and H,K Schur energy must be valid in one cutoff theory, while continuum OS reconstruction and spectral transfer remain quarantined. The scalar R carrier is too weak and representation-limited; full gauge-invariant OS density is too strong and circular for this local gate; raw plaquette enumeration is exact but fragmented. The sheet-kernel hypergraph is retained because it encodes sheets, weights, transporters, color tensors, shell labels, multiplicities, OPE intervals, and Schur data; preserves gauge invariance, reflection support, Gaussian/kappa4 separation, endpoint compression, and same-theory normalization; supports cumulant contraction, quotient auditing, shell row/operator bounds, interval arithmetic, and Schur subtraction; quotients only by Wilson trace and sheet symmetries; keeps a finite endpoint-box locality budget; transfers only through Delta_sigma; and has falsifiers by margin failure, nonuniform envelopes, or non-invariant quotienting. Conceptual value signal: the result is sharp and route-changing at finite scope because R is decomposed into a computable positive color square plus one dangerous shell-bounded connected four-curvature operator, with the Schur hairpin energy in the same inequality. The larger YM gates--volume/cutoff-uniform basin entry, large-field/topology control, regulator-independent Schwinger functions, OS positivity, observable density, and physical-unit spectral transfer--are untouched but cleanly separated.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the first A_ell certificate.`
- Rationale: The branch no longer needs another abstract OS-density restatement; it needs a concrete same-regulator stress test showing whether the connected kappa4 shell envelope can be smaller than the Gaussian color square after H,K Schur subtraction.
- Situation seed: Fixed finite SU(2) hypercubic heat-kernel lattice, one reflected endpoint box B, and the already selected H,K collar/hairpin Wilson sheet hypergraph; compute C_sigma, shell counts, and interval enclosures for K^{(4),B}_sigma.
- Varied variable: rho=sigma/a, the heat-kernel smearing radius in lattice units.
- Held-fixed controls: Same Wilson endpoint basis and same H,K Schur blocks B_sigma,E_sigma for every rho., Same heat-kernel cutoff measure mu_{a,L,g}, coupling g_R(a), reflection plane, trace normalization, and perimeter centering., No continuum limit, no volume-uniform claim, and no OS spectral-transfer inference from the finite experiment.
- Expected observation: If Delta_sigma stays positive on a rho interval, the worked endpoint box earns finite Route A promotion; if Delta_sigma becomes negative or unstable, the connected kappa4 polarization or Schur hairpin energy is the active obstruction.
- Transfer certificate needed: A validator-checkable table of C_sigma, A_ell(sigma), e_OPE,sigma, s_HK,sigma, quotient audits, and interval arithmetic proving the sign of Delta_sigma in the same cutoff theory.

## Next Experiment

Compute the first same-regulator H,K shell intervals A_0(sigma) and A_1(sigma) from the heat-kernel connected four-curvature cumulant, then evaluate Delta_sigma with certified interval arithmetic.

