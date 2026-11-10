# cycle-0300

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint root-quartic interval for the finite reflected-Wilson post-H,K gate

## Candidate Lemma

For the finite three-hairpin post-H,K block in the heat-kernel plaquette-sheet regulator, the leading endpoint connected fourth cumulant is the negative Haar-Jacobian root-quartic term. After null-channel incidence contraction, only positive endpoint dominance D_v>0 can lower the gate at leading order; half-overlap endpoint classes are leading-order protective but not a proof because remainders and tails remain.

## Definitions

- source object: heat-kernel plaquette-sheet endpoint box v for SU(N) regulated Yang-Mills, with endpoint source sL_v inserted into the singlet Wilson flux variable X_v in exponential coordinates.
- target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for the locked three-hairpin null channel; I_gate>0 promotes only this finite block and does not imply continuum OS reconstruction or a mass gap.
- controlled interface: the endpoint carrier C_ep maps same-theory source derivatives kappa_v=partial_s^4 log Z_v(s)|0 and signed incidence D_v=2b12(v)-4b13(v)-4b23(v) to a certified scalar interval for I_gate.
- same-theory condition: every Z_v(s) is computed from the original heat-kernel Wilson plaquette measure and the same gauge-invariant Wilson observables, with no boundary counterterm, gauge fixing change, or endpoint algebra enlargement.
- declarative tension: collar OS positivity, fixed Wilson observables, and singular connected endpoint OPE must coexist, but H,K and half-overlap data do not determine the endpoint source cumulant.
- carrier critique: symbolic R is representation-limited because it hides incidence signs; raw kappa_4 spectra are too strong because negative kappa_4 is harmless when D_v<=0.
- efficient representation: encode endpoint source classes, seven source values, kappa intervals, signed fractional incidences, C_N, M_G, epsilon_v, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; use source differentiation, interval arithmetic, source-equivalence, color multiplication, clipping, incidence contraction, and tail addition; identify carriers only by equal regulated source data; export only [I_-,I_+] to the finite OS gate.

## Assumptions

- Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action, restricted to the finite reflected Wilson three-hairpin block after H,K have been fixed.
- Regime: endpoint boxes lie in an exponential coordinate ball, the endpoint heat time t_v is small, and all nonendpoint straight contacts have already been removed by the prior cancellations.
- Uniformity: the remainder epsilon_v and the tail T_tail must be bounded uniformly in lattice spacing and finite volume for this finite block; otherwise the statement is only regulated evidence.
- Same-theory: source differentiation is performed on the locked gauge-invariant Wilson plaquette-sheet partition function and not on a boundary-renormalized or enlarged observable algebra.
- Validity: Wick-square Gram contributions are treated as positive, and the straight C_A f f contact is canceled by the previously established null-incidence identity.

## Equations

- Haar-Jacobian quartic endpoint expansion: `\log J(x)=-\frac{1}{12}\sum_{\alpha>0}(\alpha\cdot x)^2-\frac{1}{1440}\sum_{\alpha>0}(\alpha\cdot x)^4+O(\|x\|^6)`. Valid when: Valid when x remains inside the endpoint exponential chart for SU(N) and the heat-kernel endpoint box is small enough that the Jacobian expansion is uniform.
- connected endpoint fourth cumulant: `\kappa_v(L_v)=\left.\partial_s^4\log Z_v(s)\right|_{s=0}=-\frac{t_v^4}{60}R_4(L_v)+E_v`. Valid when: Applies after tilted Gaussian endpoint evaluation in heat-kernel coordinates, with connected-log subtraction killing Wick-square pieces and E_v collecting uniform nonquartic and interaction remainders.
- root quartic identity: `R_4(L)=\sum_{\alpha>0}(\alpha(L))^4=N\operatorname{tr}_F(L^4)+3\big(\operatorname{tr}_F L^2\big)^2`. Valid when: Valid for traceless Hermitian SU(N) endpoint source directions in fundamental trace normalization, using the positive-root system alpha_ij=e_i-e_j.
- root quartic norm envelope: `3\|L\|_{2,F}^4\le R_4(L)\le (N+3)\|L\|_{2,F}^4`. Valid when: Valid for the same SU(N) traceless endpoint sources, since tr_F L^4 is nonnegative and at most (tr_F L^2)^2.
- leading safe-side gate bound: `I_{\rm gate}\ge M_G-C_N\sum_v\left([D_v]_+\frac{t_v^4}{60}(N+3)\|L_v\|_{2,F}^4+|D_v|\epsilon_v\right)-|T_{\rm tail}|`. Valid when: Requires the post-H,K null-channel incidence D_v, the root-quartic endpoint expansion, and cutoff-uniform bounds |E_v|<=epsilon_v and |tail|<=|T_tail| for the same Wilson theory.

## Attempted Derivation

- Freeze the Clay target commitments: this branch may certify only a finite reflected-Wilson endpoint gate and makes no continuum or mass-gap claim.
- Use heat-kernel endpoint exponential coordinates and expand the SU(N) Haar Jacobian through quartic order.
- Tilt the endpoint Gaussian by sL_v and differentiate log Z_v(s) four times; the quartic Jacobian gives -t_v^4 R4(L_v)/60.
- Use the SU(N) root identity R4(L)=N tr_F L^4+3(tr_F L^2)^2 and the norm envelope to get a regulator-visible upper bound on the magnitude of the negative leading cumulant.
- Contract with the already fixed post-H,K null incidence D_v=2b12-4b13-4b23; only [D_v]_+ can lower the gate at leading order.
- Add the uniform endpoint error epsilon_v and tail T_tail without using their sign, producing a conservative valid lower interval for I_gate.
- Compare the result with the global Schur-preimage route: that route is valid but too coarse after H,K, while C_ep preserves the incidence signs needed for this finite scalar decision.

Blocking gap: The derivation still lacks actual same-theory endpoint source intervals or a cutoff-uniform proof of the epsilon_v and T_tail bounds for the 12-dominant classes; this is the current hard gate.

## Falsifiers

- A same-theory seven-point source stencil for a positive-D endpoint class certifies kappa_C so negative that I_+<0; this is the direct finite falsifier.
- The heat-kernel endpoint remainder E_v or T_tail grows with cutoff removal, invalidating the claimed uniform interval even if regulated signs look safe.
- A boundary counterterm or endpoint-specific Wilson normalization is needed to define Z_v(s), breaking the same-theory condition.
- Source-equivalence aggregation identifies boxes with unequal regulated connected cumulant witness data, hiding a dangerous 12-dominant class.
- Topology or large-field sectors contribute to endpoint boxes outside the exponential-chart tail budget, so the root-quartic local carrier is not valid.

## Learning

Conceptual pressure attacked: endpoint collapse must be sign-certified in the same Wilson theory rather than hidden inside symbolic R. The declarative tension is finite collar OS positivity plus fixed gauge-invariant Wilson observables plus singular connected endpoint OPE, with no boundary theory allowed. The new value signal is sharp and route-changing at finite scope: the leading endpoint cumulant is explicitly the negative SU(N) root-quartic Haar term, but it can demote the block only through positive D endpoint dominance and uncontrolled tails. This changes the finite post-H,K reflected-Wilson OS transfer gate only; Clay continuum construction, OS/Wightman reconstruction, nontriviality, and the mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while the branch remains quarantined for missing endpoint data.`
- Rationale: The branch has already reduced the post-H,K obstruction to endpoint source intervals; another abstract OS restatement would not change the proof state, whereas varying endpoint dominance tests the exact finite gate.
- Situation seed: In the SU(N) heat-kernel plaquette-sheet three-hairpin block, take two source-equivalence endpoint classes with the same L and t: one half-overlap class and one 12-dominant class, and compute their connected cumulant witness intervals from seven source values of log Z_C(s).
- Varied variable: theta=(b13+b23)/b12, the fractional endpoint overlap ratio controlling D=2b12-4b13-4b23.
- Held-fixed controls: The heat-kernel regulator, Wilson normalization, and gauge-invariant observable algebra are unchanged., The H,K Schur-Feshbach reduction, null vector, Gaussian margin M_G, and color factor C_N are fixed., No boundary counterterm, gauge fixing change, or endpoint algebra enlargement is allowed., The same cutoff-uniform tail budget T_tail is used for every endpoint class.
- Expected observation: For theta>=1/2 the leading root-quartic term is protective or neutral, while theta<1/2 creates a negative contribution of size proportional to (2-4theta)b12 t^4 R4(L)/60; the sign of I_gate then decides promotion, falsifier status, or quarantine.
- Transfer certificate needed: Certified same-theory connected cumulant witness intervals for d_s^4 log Z_C, a cutoff-uniform endpoint remainder and tail bound, and validator-facing evidence that the source data are from the locked Wilson observables.

## Next Experiment

Proof search plus endpoint data: for SU(2) and SU(3) heat-kernel endpoint classes, compute the seven-point connected cumulant witness for d_s^4 log Z_C, aggregate source-equivalent D_C before clipping, insert the root-quartic error bound, and output the finite interval [I_-,I_+] for promotion, falsifier, or continued quarantine.

# Cycle 300: Ward-Hessian endpoint certificate for the connected R++ polarization

## Candidate Lemma

Endpoint-cell Ward-Hessian certificate: for two plus-channel H,K hairpin endpoint boxes I,J in the same flowed Wilson regulator, the renormalized endpoint mediator R_{++}^{ren} has a computable lower interval equal to the positive two-curvature pair baseline minus Ward-subtracted connected four-curvature near/far majorants and recovery errors.

## Definitions

- source object: the centered gradient-flow-regulated SU(N) Wilson hairpin covariance R_{++}^{ren}(I,J;t,epsilon,a,V) computed from the same cutoff measure as the H,K finite test.
- target object: a finite endpoint-box Schur-Feshbach plus-channel positivity certificate Q_+>0 for the post-H,K Route A matrix.
- controlled interface: the endpoint sheet-current recovery map W^{ren}->(J_+,M_{2,+},G_{++},K_4^{WS}) with Ward/cusp subtraction and outward-rounded interval error budget.
- same-theory condition: all cumulants, counterterms, and recovery errors come from the same Wilson/flow regulator family before any continuum or OS spectral-transfer claim.
- J_+ is the signed endpoint sheet current obtained from the H,K collar/hairpin surfaces after perimeter and cusp centering.
- K_4^{WS} is the Ward-subtracted connected four-curvature kernel, decomposed into 3g, 4g, counterterm, and endpoint sectors.

## Assumptions

- Model: finite-volume SU(N) Wilson plaquette Yang-Mills with gradient-flow time t>0 and boundary point splitting epsilon>0, then a controlled a->0 or fixed-cutoff interval statement only.
- Regime: endpoint boxes have side eta, separation d>=4eta, and flow radius sqrt(8t)<=eta/4 so near/far cells are geometrically separated.
- Cutoff: flowed curvature cumulants are evaluated at positive flow time before thin-loop renormalization; perimeter and cusp counterterms are subtracted in the same cutoff ensemble.
- Same-theory: R_{++}^{ren}, G_{++}, K_4^{WS}, E_6, and the H,K Schur-Feshbach leakage L_+ are recovered from the same Wilson observable family and normalization.
- Uniformity: the stated promotion test is finite-gate evidence unless the constants are bounded uniformly in volume, cutoff, and regulator window.
- Local: only endpoint boxes adjacent to the H,K hairpin boundary are varied; bulk Wilson/OS reconstruction and spectral transfer remain untouched.

## Equations

- flowed endpoint cumulant definition: `R_{++}^{ren}(I,J;t,\epsilon)=\kappa_2\big(:W_+^{I}:_{t,\epsilon},:W_+^{J}:_{t,\epsilon}\big)`. Valid when: Valid when both centered hairpin observables use the same flowed Wilson cutoff measure and identical perimeter-cusp subtraction.
- pair-plus-connected decomposition: `R_{++}^{ren}=g_t^4(N^2-1)\{2G_{++}+N C_{4,++}^{WS}\}+E_6+E_{rec}`. Valid when: Applies after fourth-order Wilson expansion, same-theory centering, Ward subtraction, and a separately bounded sixth-order remainder.
- plus-channel moment cancellation: `\int_E J_+(u)\,du=0,\qquad \int_E u_\alpha J_+(u)\,du=0`. Valid when: Requires the reflected H,K plus endpoint geometry, oriented sheet currents, and exact cusp/perimeter counterterm cancellation.
- near-far C4 majorant: `|C_{4,++}^{WS}|\le H_{far}^+(\rho,t)M_{2,+}^2+H_{near}^+(\rho,t)A_{near}+\Delta_{ct}^+`. Valid when: Valid when K_4^{WS} is C^2 on far cells and near cells are enclosed by flowed heat-kernel majorants.
- finite promotion inequality: `g_t^4(N^2-1)\{2G_{++}^- -N[H_{far}^+M_{2,+}^2+H_{near}^+A_{near}+\Delta_{ct}^+]\}-E_6^+-E_{rec}^+>L_+`. Valid when: Valid for the finite H,K Schur-Feshbach endpoint block with positive remainder matrix D and certified interval bounds.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: the centered gradient-flow-regulated SU(N) Wilson hairpin covariance R_{++}^{ren}(I,J;t,epsilon,a,V) computed from the same cutoff measure as the H,K finite test.; target object: a finite endpoint-box Schur-Feshbach plus-channel positivity certificate Q_+>0 for the post-H,K Route A matrix.; Model: finite-volume SU(N) Wilson plaquette Yang-Mills with gradient-flow time t>0 and boundary point splitting epsilon>0, then a controlled a->0 or fixed-cutoff interval statement only..
- Fix Wilson plaquette SU(N) at cutoff a, finite volume V, flow time t, point splitting epsilon, and the H,K plus-channel endpoint boxes I,J.
- Expand the two centered renormalized hairpins through fourth order in the flowed curvature insertion; disconnected products and one-hairpin perimeter/cusp terms cancel by centering.
- Identify the two cross pairings of flowed curvatures; their color trace gives the positive factor 2(N^2-1)G_{++}.
- Collect the genuine connected four-curvature terms into K_4^{WS}=K_{3g}+K_{4g}+K_{ct}+K_{end} with color factor N(N^2-1).
- Replace raw endpoint contours by sheet currents only after checking zero-pairing equivalence and recording E_pair,E_rec.
- Use plus-channel reflection to get zero monopole and dipole endpoint moments; Taylor expand K_4^{WS} on far cells so the constant and linear terms vanish.
- Bound far cells by H_far^+ M_{2,+}^2 and near cells by heat-kernel majorants H_near^+ A_near; add counterterm and sixth-order interval remainders.
- Insert the resulting lower interval for R_{++}^{ren} into Q_+^{end}=R_{++}^{ren}-L_+.

Blocking gap: The missing proof-search object is a cutoff-stable numerical or analytic enclosure of H_far^+(rho,t), H_near^+(rho,t), E_6^+, and E_rec^+ for the actual H,K endpoint sheets.

## Falsifiers

- falsifier: the Ward/cusp subtraction leaves a nonzero monopole or dipole moment in the plus endpoint current.
- falsifier: the connected four-curvature near-cell heat-kernel majorant exceeds the positive pair baseline for every admissible rho and t.
- falsifier: zero-pairing quotienting changes the flowed Wilson covariance beyond E_pair, so endpoint currents are not a valid carrier.
- falsifier: the lower interval R_{++}^{ren,-} fails to beat the Schur-Feshbach leakage L_+.
- falsifier: interval widths or recovery errors do not stabilize as a decreases at fixed physical t and endpoint geometry.

## Learning

Conceptual pressure attacked: the missing same-theory mediator between finite Schur-Feshbach endpoint positivity and Wilson cumulant positivity. Declarative tension: positive flowed pair covariance, same-theory renormalization, and finite endpoint positivity must all be valid, but the connected four-curvature polarization can erase the pair term unless Ward-Hessian constants and recovery errors are certified. Carrier critique: raw Wilson contours are fragmented and representation-limited; global OS spectral transfer or a non-Gaussian Schwinger family route is too coarse for this finite obstruction. Efficient representation requirements are now explicit: encode H,K sheets, endpoint currents, cell moments, sector kernels, counterterms, and recovery errors; preserve gauge, color, reflection, orientation, cutoff, locality, and same-theory invariants; use cumulant expansion, Ward/cusp subtraction, endpoint Taylor remainders, heat-kernel majorants, interval quadrature, outward rounding, and zero-pairing quotienting; transfer only through centered flowed Wilson cumulants; demote on any falsifier. Hard gate: finite endpoint-box positivity after H,K. Value signal: R_{++}/kappa_4 is a valid route-deciding color-geometric interval certificate, not a symbolic endpoint term, while Clay existence and mass gap remain unclaimed.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete falsifier probe now.`
- Rationale: The branch is past abstract Wilson/OS restatement; the proof state turns on whether the connected C4 endpoint polarization can be bounded below in the same Wilson theory.
- Situation seed: Finite-volume SU(2) Wilson plaquette Yang-Mills with gradient-flow time t, two reflected H,K plus-channel hairpin endpoint boxes of side eta and separation d=6eta, centered flowed Wilson hairpins, and Ward-subtracted endpoint sheet currents.
- Varied variable: The near/far split radius rho/eta, varied from 1.25 to 3 while holding flow radius sqrt(8t)=eta/4 fixed.
- Held-fixed controls: Same cutoff action, flow equation, counterterm prescription, and centered Wilson hairpin observables for all cumulants., Same H,K endpoint geometry, orientation, reflection parity, and color trace normalization., Same finite Schur-Feshbach leakage L_+ and same outward-rounded interval arithmetic., No continuum OS spectral-transfer or mass-gap inference from the finite observation.
- Expected observation: If the Ward-Hessian mechanism is real, the certified lower interval for R_{++}^{ren} has a rho plateau with 2G_{++}^- dominating N(H_far M2^2+H_near A_near); if not, near-cell C4 or recovery error kills positivity.
- Transfer certificate needed: Before intuition affects proof obligations, provide cutoff-stable interval enclosures for G_{++}, H_far, H_near, E_6, and E_rec plus a same-theory recovery proof from raw Wilson hairpins to endpoint sheet currents.

## Next Experiment

proof_search: instantiate the SU(2) H,K endpoint sheets, compute G_{++}^- analytically from the flowed two-curvature kernel, interval-enclose K_{3g}, K_{4g}, K_ct, and K_end for rho/eta in [1.25,3], and report whether the connected cumulant witness support term R_{++}^{ren,-} beats L_+ as a same-theory nontriviality witness boundary object.

# Gauge-Invariant Observable Density In The Excitation Sector

## Candidate Lemma

Fixed-regulator two-sparse Rayleigh intervals give a valid finite falsifier for the post-H,K endpoint positivity gate: if an interval upper bound for x^*U_sigma x is negative for x=e_i-eta e^{i theta}e_j, then the worked Wilson collar/hairpin Route A endpoint matrix is not positive semidefinite after Schur-Feshbach subtraction.

## Definitions

- source object: finite-volume SU(N) lattice Yang-Mills at cutoff a with heat-kernel flow scale sigma, oriented plaquette curvature variables, Wilson sheet weights, and same-regulator connected cumulants C_sigma and K4_sigma.
- target object: the finite Hermitian endpoint-box quadratic form U_sigma on post-H,K Wilson endpoint coordinates whose positivity is required for the finite Route A Schur-Feshbach certificate.
- controlled interface: the recovery map Rec_sigma contracts raw plaquette cumulant intervals with sheet weights and color tensors to obtain R_sigma, adds OPE intervals, and subtracts S_HK=B^*E^{-1}B in the same endpoint basis.
- same-theory condition: all Wilson sheets, heat-kernel transporters, cumulants, OPE remainders, Schur blocks, couplings, volume, cutoff, gauge group, and normalizations come from the identical regulated Yang-Mills theory.
- bridge observable: the validator-facing connected cumulant witness R_{ij,sigma}=cum_2(:Phi_i^2:,:Phi_j^2:) for reflected Wilson endpoint sheets.

## Assumptions

- Model: finite hypercubic SU(N) Yang-Mills with a reflection-symmetric Wilson or heat-kernel plaquette action and heat-kernel flowed links at scale sigma.
- Cutoff: a, volume L, endpoint set I, H,K blocks, and sigma are fixed before intervals are formed; no continuum or infinite-volume conclusion is claimed.
- Same-theory: the raw K4 intervals, Gaussian covariance, OPE error, and S_HK are computed from the same regulator and Wilson basis, not imported from a different ensemble.
- Validity: interval arithmetic is outward-rounded and respects Hermitian symmetry, reflection support, and exact Wilson trace identities.
- Local: endpoint sheets lie in the finite collar/hairpin box after H,K compression, so the claim changes only the finite Route A endpoint positivity gate.

## Equations

- transported plaquette curvature: `Y_{i,p}^A(\sigma)=\operatorname{Ad}_{V_{i,p}(\sigma)}^{AB}\,a^{-2}\operatorname{Im}\operatorname{tr}(T^B U_p(\sigma)),\qquad \Phi_i^A(\sigma)=\sum_{p\in S_i}w_{i,p}Y_{i,p}^A(\sigma)`. Valid when: Valid when heat-kernel flowed plaquette holonomies are oriented and transported to the sheet basepoint before color contraction.
- raw connected four-curvature compression: `\mathcal K_4(pA,qB,rC,sD)=\operatorname{cum}_4(Y_p^A,Y_q^B,Y_r^C,Y_s^D),\quad K^{\mathrm{raw}}_{ij}=\sum_{p,q\in S_i}\sum_{r,s\in S_j}w_{i,p}w_{i,q}w_{j,r}w_{j,s}\mathcal K_4(pA,qA,rB,sB)`. Valid when: Applies after the same transported plaquette variables and sheet weights define both endpoint fluxes in one cutoff theory.
- boundary-polarization decomposition: `R_{ij,\sigma}=\alpha_N g_R^4 G_{ij,\sigma}+\frac{g_R^4}{16N^2}K^{\mathrm{raw}}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Requires the normal-ordered Wilson boundary OPE where disconnected vacuum and perimeter pieces cancel in the same regulator.
- post-HK endpoint matrix: `U_\sigma=R_\sigma-S_{HK,\sigma},\qquad S_{HK,\sigma}=B_\sigma^*E_\sigma^{-1}B_\sigma`. Valid when: Valid when the H,K Schur block E_sigma is strictly positive on the eliminated hairpin subspace.
- two-sparse Rayleigh upper interval: `\overline q_{ij}(\eta,\theta)=\overline U_{ii}+\eta^2\overline U_{jj}-2\eta\,\underline{\operatorname{Re}(e^{-i\theta}U_{ij})};\qquad \overline q_{ij}(\eta,\theta)<0\Rightarrow U_\sigma\not\succeq0`. Valid when: Applies when interval endpoints enclose the true Hermitian entries of U_sigma with a certified phase sector.

## Attempted Derivation

- Conceptual pressure attacked: decide whether the non-Gaussian connected K4 part can kill the finite H,K endpoint route without requiring a full matrix PSD proof.
- Start with transported heat-kernel plaquette curvatures Y_p^A and endpoint fluxes Phi_i^A=sum_p w_{i,p}Y_p^A in the same finite Wilson collar/hairpin box.
- Use normal ordering in R_{ij}=cum_2(:Phi_i^2:,:Phi_j^2:) so disconnected vacuum and perimeter pieces cancel; the remaining Gaussian crossed contraction is the PSD color square alpha_N g_R^4 G_{ij}.
- Compress the connected four-curvature cumulant by the same sheet weights to obtain K4_raw, keep E_OPE as an interval, and subtract S_HK=B^*E^{-1}B from the finite Schur-Feshbach theorem.
- For x=e_i-eta e^{i theta}e_j compute x^*U_sigma x and bound it above by overline U_ii+eta^2 overline U_jj-2 eta lower Re(e^{-i theta}U_ij).
- If this upper interval is negative, the actual Rayleigh quotient is negative, giving a valid falsifier of endpoint PSD and demoting only the finite Route A H,K geometry.

Blocking gap: The branch still lacks actual same-regulator raw K4 intervals for a named endpoint pair and a certified phase-sector interval for U_ij; without these numbers the theorem is a proof-search template, not a completed Wilson calculation.

## Falsifiers

- A certified two-sparse stress vector with overline q_ij(eta,theta)<0 is a finite falsifier for the worked H,K endpoint route.
- Regulator mismatch between K4 intervals and S_HK invalidates the same-theory recovery map.
- Non-invariant Wilson quotienting can fabricate signs in K4_raw and demotes the interval certificate.
- An OPE error interval larger than the Gaussian margin plus Schur margin prevents a valid promotion.
- Failure of reflection reality forces complex interval search; if no phase sector is certified, the two-sparse shortcut is invalid.
- A finite positive Delta_raw would still not imply gauge-invariant observable density, OS reconstruction, or the Clay mass gap.

## Learning

Cycle 300 attacks the conceptual pressure of turning the connected boundary-OPE polarization into a route-deciding finite witness rather than another symbolic R or OS-density restatement. Declarative tension: Wilson/OPE coefficients, connected K4 negativity, OPE errors, and H,K Schur subtraction must jointly control one endpoint quadratic form in a single cutoff theory, while Clay-level continuum existence, OS/Wightman reconstruction, gauge-invariant observable density, and Hamiltonian mass gap are barred as conclusions. Carrier critique: scalar R is too weak and representation-limited; OS Hilbert observable algebra and excitation-sector cyclicity are too strong and circular for this local gate; shell A012 is convenient but quarantined; raw plaquette enumeration is fragmented yet valid. Compared with full Delta_raw matrix search, the two-sparse stress route is the sharper negative tactic because three or four same-regulator K4 intervals can demote the H,K endpoint route. Efficient representation requirements are now fixed: encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/K4 separation, endpoint compression, same-theory normalization, and exact Wilson quotienting; support cumulant contraction, interval summation, phase-sector certification, Rayleigh stress search, Loewner lower bounds, and Schur subtraction; quotient only by exact Wilson identities; keep finite endpoint-box complexity; transfer only through Delta_raw or x_stress; and expose falsifiers by negative Rayleigh margin, missing intervals, non-invariant quotienting, or regulator mismatch. Conceptual value signal: sharp, explanatory, and route-changing at finite scope because R is a connected cumulant witness with explicit color, geometry, non-Gaussian K4, OPE, and Schur data in one valid inequality.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the raw K4 two-sparse proof search.`
- Rationale: The branch has quarantined symbolic shells; another abstraction restatement is low value. A concrete two-coordinate endpoint stress experiment can decide whether a few connected cumulant intervals demote the H,K collar/hairpin route before full matrix enumeration.
- Situation seed: Finite SU(N) heat-kernel lattice endpoint box after the H,K Schur compression, with two reflected Wilson sheet coordinates i and j sharing a collar plaquette cluster and separated from the endpoint boundary by the same OPE collar width.
- Varied variable: The Rayleigh weight eta in x=e_i-eta e^{i theta}e_j, with theta fixed by the certified reflection phase sector.
- Held-fixed controls: Cutoff a, volume L, heat-kernel scale sigma, gauge group SU(N), and renormalized coupling g_R., The same Wilson sheet weights, transported plaquette variables, OPE normalization, and Schur block S_HK., The finite endpoint coordinate set and exact Wilson trace/reflection quotient policy., Clay target boundary: no continuum, OS spectral, or gauge-invariant observable density conclusion is inferred.
- Expected observation: If the off-diagonal connected K4 interval plus Schur subtraction makes min_eta overline q_ij negative, the route is demoted by a small connected cumulant witness; if the minimum stays positive with margin, the pair survives and full Delta_raw proof search is justified.
- Transfer certificate needed: Outward-rounded same-regulator intervals for K4_ii, K4_jj, K4_ij, E_OPE entries, Gaussian covariance entries, and exact S_HK entries, plus a reflection/phase audit proving the stress vector is expressed in the same endpoint basis.

## Next Experiment

Proof search: choose one endpoint pair (i,j) in the worked H,K collar/hairpin box and compute same-regulator raw K4_ii, K4_jj, K4_ij intervals, Gaussian entries, OPE entries, and S_HK; then test min_eta overline q_ij. Report as a connected cumulant witness for finite Route A, while marking gauge-invariant observable density and the OS Hilbert observable algebra as untouched.

