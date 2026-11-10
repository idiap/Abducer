# cycle-0315

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology -> finite endpoint cumulant screen

## Candidate Lemma

For the fixed post-H,K three-hairpin Wilson block in the heat-kernel plaquette-sheet regulator, the connected endpoint boundary-OPE polarization admits a clipped interval cap. If the lower endpoint I_- is positive, the finite null Schur-Feshbach gate is promoted; if the upper endpoint I_+ is negative, the same-theory Wilson OS passage has a finite falsifier.

## Definitions

- source object: C_ep(a,t,h) is the heat-kernel plaquette-sheet endpoint carrier for the fixed three-hairpin Wilson block: source classes c, seven source values Z_c(kh), k=-3,...,3, cumulant intervals K_c, fractional incidences b_{ij,c}, color factor C_N, Gaussian margin M_G, and tail interval T_tail.
- target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for this same regulated Wilson block; positivity promotes only this finite Route A gate and does not assert continuum existence, OS/Wightman reconstruction, nontriviality, or mass gap.
- controlled interface: source-equivalent endpoint source data are mapped by fourth-source differentiation, incidence contraction D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}, positive-D clipping, color multiplication, and tail addition into a certified interval [I_-,I_+] for I_gate.
- same-theory condition: the Wilson normalization, gauge-invariant test algebra, reflection map, heat-kernel regulator, endpoint recovery maps, and source insertions are fixed before and after collar collapse; no boundary counterterm, algebra enlargement, or gauge-fixed observable replacement is allowed.
- connected cumulant witness: kappa_c is the fourth derivative of log Z_c(sL_c), so Wick-square disconnected terms are removed before incidence contraction.
- carrier critique: symbolic R is representation-limited because it hides endpoint incidences; a raw kappa_4 spectrum is too strong because negative kappa_4 is harmless when D_c<=0; the global Schur-preimage test is valid but too coarse after H,K.
- efficient representation: encode endpoint source classes, seven source values, cumulant intervals, signed incidences, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; use source differentiation, interval arithmetic, source-equivalence, color multiplication, clipping, incidence contraction, and tail addition; identify carriers only by equal regulated source data; export only [I_-,I_+] to the finite OS gate.

## Assumptions

- Model: four-dimensional Euclidean SU(N) Yang-Mills in a heat-kernel plaquette-sheet cutoff around the fixed reflected Wilson three-hairpin block.
- Regime: finite Route A endpoint boxes after H,K have small heat-kernel endpoint time t_c and symmetric source step h.
- Uniformity: the endpoint expansion remainder satisfies |E_c|<=epsilon_c and the nonendpoint connected tail satisfies |T_tail|<=tau with constants uniform in the cutoff for the selected block.
- Same-theory: the source insertions are gauge-invariant Wilson plaquette-sheet sources and use the same regulated Schwinger family as the collar OS matrix.
- Local: straight-segment f f contacts cancel by the null-incidence identity, and Wick-square contractions are removed by log Z_c before defining kappa_c.
- Constraint: endpoint classes may be aggregated only after equality of regulated source values on the seven-point stencil has been certified.

## Equations

- endpoint_gate_decomposition: `I_{\mathrm{gate}}=M_G+C_N\sum_c D_c\,\kappa_c+T_{\mathrm{tail}},\qquad D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}`. Valid when: Valid when the endpoint source classes are source-equivalent, additive contacts and one-body Wilson factors have already been removed, and T_tail contains every nonendpoint connected contribution.
- suN_root_quartic_cumulant: `\kappa_c=\left.\frac{d^4}{ds^4}\log Z_c(sL_c)\right|_{s=0}=-\frac{t_c^4}{60}R_4(L_c)+E_c,\quad R_4(L)=N\operatorname{tr}(L^4)+3(\operatorname{tr}(L^2))^2`. Valid when: Valid when the heat-kernel endpoint coordinate expansion is used in an SU(N) box with small t_c, bounded eighth source derivative, and no boundary counterterm.
- clipped_interval_screen: `I_-:=M_G-C_N\sum_c [D_c]_+A_c^+-C_N\sum_c |D_c|\epsilon_c-\tau\le I_{\mathrm{gate}}\le I_+:=M_G-C_N\sum_c [D_c]_+A_c^-+C_N\sum_c[-D_c]_+A_c^++C_N\sum_c|D_c|\epsilon_c+\tau`. Valid when: Applies when the SU(N) root quartic is bounded by Frobenius norm and the endpoint remainders and tails are uniform in the cutoff.
- root_quartic_bounds: `A_c^-\le \frac{t_c^4}{60}R_4(L_c)\le A_c^+,
\qquad 0\le A_c^-\le A_c^+\le \frac{t_c^4}{60}(N+3)\|L_c\|_2^4`. Valid when: Valid when L_c is measured in the fundamental Frobenius norm and the SU(N) root identity for R4 is used in one endpoint box.
- seven_point_source_stencil: `\kappa_c=\frac{-f_c(-3h)+12f_c(-2h)-39f_c(-h)+56f_c(0)-39f_c(h)+12f_c(2h)-f_c(3h)}{6h^4}+\mathcal E_h,\quad |\mathcal E_h|\le \frac{7h^4}{240}M_{8,c}`. Valid when: Requires the same-theory heat-kernel source family at seven symmetric source values with an eighth-derivative bound on the whole stencil interval.
- half_overlap_shield: `D_c\le0\quad\Longleftrightarrow\quad b_{13,c}+b_{23,c}\ge \frac12 b_{12,c}`. Valid when: Valid when b_ij are fractional endpoint footprint incidences measured in the same regulator and the null vector contraction has weights 2,-4,-4.

## Attempted Derivation

- Attack the conceptual pressure: endpoint collar collapse must be sign-certified inside the same Wilson theory, not hidden in symbolic R or repaired by a boundary theory.
- Fix the heat-kernel plaquette-sheet regulator and endpoint source classes for the already computed H,K three-hairpin block; preserve the gauge-invariant Wilson observables and reflection map.
- Use the connected source functional f_c(s)=log Z_c(sL_c); this removes Wick-square disconnected contractions, while the straight C_A f f contact has already canceled by the null-incidence identity.
- Expand the SU(N) endpoint Haar Jacobian: the s^4 coefficient is -t_c^4 R4(L_c)/1440, hence the fourth connected source cumulant has leading term -t_c^4 R4(L_c)/60 plus a uniform remainder E_c.
- Contract with the null-channel incidence D_c=2b12-4b13-4b23; since the leading cumulant is nonpositive, only D_c>0 can lower the finite gate.
- Bound R4 by the Frobenius root-quartic cap and carry all uncomputed endpoint and nonendpoint terms into epsilon_c and T_tail, producing the certified interval [I_-,I_+].
- Derive the seven-point fourth-source stencil so the next validator-facing computation needs only seven same-theory source values per source class plus an M8 error bound.

Blocking gap: The actual endpoint source values, eighth-derivative bounds, and cutoff-uniform T_tail estimate are not yet computed for the Yang-Mills regulator; without them the cap is a valid finite theorem schema but not a promotion certificate.

## Falsifiers

- Finite falsifier: a source-certified positive-D endpoint class gives I_+<0 after the seven-point connected cumulant witness and tail bound.
- Same-theory falsifier: the endpoint source expansion requires a boundary counterterm or a changed Wilson-loop normalization at the reflection plane.
- Uniformity falsifier: epsilon_c or T_tail grows with cutoff or volume, so the finite interval is not valid for the intended regulator passage.
- Representation falsifier: early clipping before source-equivalent signed aggregation creates a negative interval that disappears after valid aggregation.
- Regulator falsifier: the heat-kernel plaquette-sheet endpoint family is outside the RG basin used for the locked gauge-invariant Schwinger functions.

## Learning

Conceptual pressure: endpoint collapse must be sign-certified in the same Wilson theory. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold without adding a boundary theory; H,K and the half-overlap shield alone do not decide the scalar. Carrier audit: raw R is too weak, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. The efficient carrier C_ep is source-equivalent, incidence-signed, cutoff-budgeted, and exports only [I_-,I_+]. Hard gate: the finite post-H,K reflected-Wilson OS transfer scalar; success promotes this finite block, failure gives a finite same-theory falsifier, and missing data keeps quarantine. Conceptual value signal: sharp finite route change, because negative SU(N) root-quartic endpoint cumulants are explanatory but not the obstruction; only source-certified positive-D leakage plus uniform tail can demote the block. Clay continuum construction, nontriviality, full OS/Wightman reconstruction, and positive mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while keeping the branch quarantined until source intervals are available.`
- Rationale: The branch has already reduced post-H,K R to endpoint connected cumulants; another abstract OS restatement would not decide the finite gate, whereas varying endpoint dominance directly tests the only remaining demotion mechanism.
- Situation seed: A heat-kernel SU(N) endpoint-box family for the fixed three-hairpin Wilson block, with one source-equivalent class c carrying a connected cumulant witness kappa_c from seven log Z_c(sL) evaluations.
- Varied variable: eta=(b_{13,c}+b_{23,c})/b_{12,c}, the fractional overlap ratio controlling D_c=2b_{12,c}(1-2eta).
- Held-fixed controls: Gauge group SU(N), heat-kernel plaquette-sheet regulator, and the same gauge-invariant Wilson source functional., The previously computed H,K finite block, Gaussian margin M_G, null vector, and color factor C_N., No boundary counterterm, no gauge-fixed observable replacement, and no change of Wilson normalization., Uniform endpoint remainder epsilon_c and nonendpoint tail budget tau are treated as certified controls.
- Expected observation: For eta>=1/2 the half-overlap shield gives D_c<=0, so negative root-quartic kappa_c is protective up to remainders; for eta<1/2 the seven-point source stencil decides whether positive-D leakage can overcome M_G and produce a finite OS falsifier.
- Transfer certificate needed: A cutoff-uniform source-stencil interval for kappa_c, a valid eighth-derivative error bound, a same-theory endpoint recovery map, and a T_tail bound before the observation may promote or demote the finite post-H,K proof obligation.

## Next Experiment

Proof search plus endpoint source-stencil computation: build the connected cumulant witness table for heat-kernel SU(N) endpoint classes, vary eta across the half-overlap threshold, certify [I_-,I_+], and either promote the finite post-H,K reflected-Wilson OS gate or record a finite same-theory falsifier.

# Endpoint Ward-Hessian certificate for the post-H,K Wilson polarization

## Candidate Lemma

For the H,K plus-channel endpoint sheet current, Ward, cusp, and plus-moment cancellations reduce the connected boundary-OPE polarization term R_{++} to a finite sector-Hessian interval. If the resulting lower endpoint interval beats the Schur-Feshbach leakage L_+, finite endpoint-box positivity after H,K is promoted; otherwise this R-repair is quarantined. This is a finite Route A claim, not the Clay mass gap theorem.

## Definitions

- source object: a finite-volume four-dimensional SU(N) Yang-Mills cutoff theory with Wilson action or equivalent ultraviolet regulator, gradient-flow time t>0, boundary point-splitting epsilon, centered renormalized thin Wilson hairpins, and endpoint cells I of diameter eta sqrt(8t).
- target object: the scalar plus-channel Schur-Feshbach endpoint coefficient Q_+^{eff} in the already finite H,K reduction, including the leakage L_+=B_{+R}D^{-1}B_{R+} and the Wilson endpoint correction R_{++}^{ren}.
- controlled interface: the recovery map rho from raw hairpin Wilson contours to endpoint sheet currents J_+ with cell moments, sector kernels, counterterms, and certified recovery error E_rec, preserving gauge, color, reflection, orientation, cutoff, and locality invariants.
- same-theory condition: pair contractions, connected four-curvature cumulants, Ward subtractions, cusp counterterms, and recovery errors are all computed in the same regulated Yang-Mills measure and flowed observable family; no Gaussian replacement or imported Schwinger family is used.
- endpoint moment M_{2,+}(I) is the absolute second moment of the plus endpoint current about the cell center after monopole and dipole moments vanish.
- sector Hessian H_sigma(I,t) is the supremum over the endpoint cell of the mixed second endpoint derivatives of the Ward-subtracted connected four-curvature sector kernel K_sigma^t, with sigma in {3g,4g,ct,end}.

## Assumptions

- Model: finite-volume Euclidean SU(N) Yang-Mills with a reflection-compatible cutoff, Wilson hairpins lying in the H,K endpoint collar, and gradient-flowed curvature insertions at time t>0.
- Regime: endpoint cell diameter eta sqrt(8t) is smaller than the separation to nonlocal collars, and epsilon satisfies a << epsilon << sqrt(8t) before the endpoint-cell estimate is invoked.
- Cutoff: perimeter and cusp divergences of each one-hairpin observable are subtracted before the connected cumulant is formed, and the remaining flowed kernels admit cutoff-stable interval enclosures.
- Same-theory: the centered flowed Wilson cumulant, pair baseline, connected C4 sectors, and recovery errors are evaluated under one cutoff measure and one renormalization prescription.
- Validity: the plus-channel endpoint current has certified zero monopole and zero dipole moments after zero-pairing quotienting; otherwise the Hessian reduction is invalid.
- Local: the claim concerns only the finite endpoint boxes in the H,K Schur-Feshbach matrix and does not assert continuum existence, OS reconstruction, observable density, or Hamiltonian spectral gap.

## Equations

- centered endpoint cumulant defining R: `R_{++}^{ren}(a,t,\eta)=\kappa^{a,t}_2\big(\widehat W^{ren}_+[I],\widehat W^{ren}_+[I]\big)_{\mathrm{endpoint}}`. Valid when: Valid when the two centered renormalized hairpins are recovered from the same cutoff Wilson measure with the same flow time and endpoint cell.
- pair plus connected sector decomposition: `R_{++}^{ren}=g_t^4\Big(2(N^2-1)G_{++}+N(N^2-1)\sum_{\sigma\in\{3g,4g,ct,end\}}\Xi_\sigma\Big)+E_{\ge 6}+E_{rec}`. Valid when: Valid when the boundary OPE is truncated after four flowed curvatures with the sixth-order and recovery remainders separately interval-bounded.
- Ward-Hessian sector bound: `|\Xi_\sigma(I)|\le {1\over4}H_\sigma^{I,+}(t,\epsilon,a)\,M_{2,+}(I)^2`. Valid when: Applies after Ward subtraction, one-hairpin cusp cancellation, and certified plus-channel monopole and dipole moment cancellation inside the endpoint cell.
- certified lower interval: `R_{++}^{I,-}=g_t^4(N^2-1)\left(2G_{++}^{I,-}-{N\over4}\sum_\sigma H_\sigma^{I,+}M_{2,+}(I)^2\right)-E_{\ge6}^{I,+}-E_{rec}^{I,+}`. Valid when: Valid when every G, H, sixth-order, and recovery quantity is enclosed by outward-rounded intervals in the same cutoff and flow window.
- finite promotion inequality: `Q_+^{eff}\ge Q_+^0-L_+ + R_{++}^{I,-},\qquad R_{++}^{I,-}>L_+-Q_+^0+\delta_{cert}`. Valid when: Requires the finite H,K Schur-Feshbach reduction already fixed and the endpoint R interval computed for that identical plus-channel vector.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, while positive pair covariance and flow renormalization remain compatible with a negative connected C4 polarization.
- Replace raw H,K plus hairpins by endpoint sheet currents through rho, retaining E_rec; raw contours are too fragmented, while global OS spectral transfer or a non-Gaussian Schwinger-family route is too coarse for this finite obstruction.
- Expand the centered flowed Wilson hairpin covariance through the boundary OPE: the disconnected product and one-hairpin perimeter/cusp terms cancel before the endpoint cumulant is read as R_{++}^{ren}.
- The Gaussian pair part gives the positive color-geometric baseline 2(N^2-1)G_{++}. The connected four-curvature part splits into 3g, 4g, counterterm, and endpoint-subtraction sectors with color factor N(N^2-1).
- Apply Ward subtraction and plus-channel moment constraints: total endpoint charge and first endpoint moment vanish in each cell, so the constant and linear Taylor terms of each sector kernel disappear.
- Bound each remaining sector by the mixed endpoint Hessian supremum times M_{2,+}^2/4. This converts the unknown sign of C4 into explicit near/far constants.
- Insert the lower interval R_{++}^{I,-} into the finite Schur-Feshbach scalar Q_+^{eff}=Q_+^0-L_+ + R_{++}+higher certified terms.
- Hard gate: finite endpoint-box positivity after H,K. Success promotes exactly this finite Route A gate; failure quarantines the R repair and leaves the Clay existence and mass-gap gates untouched.

Blocking gap: The derivation still needs outward-rounded numerical or analytic interval values for H_{3g}, H_{4g}, H_ct, H_end, E_{>=6}, and E_rec in the selected H,K endpoint geometry, uniformly over the cutoff window.

## Falsifiers

- Ward or cusp subtraction leaves a monopole or dipole term in the plus endpoint current; this falsifier destroys the Hessian scaling.
- The connected sector Hessian constants are so large that 2G_{++}^{I,-}-N sum_sigma H_sigma^{I,+}M_{2,+}^2/4 is nonpositive.
- The recovery map rho changes the centered flowed Wilson cumulant by an error comparable to the pair baseline.
- No stable flow/cutoff plateau exists for R_{++}^{I,-} as a and epsilon vary with fixed t.
- The finite lower interval fails the promotion inequality R_{++}^{I,-}>L_+-Q_+^0+delta_cert.
- A topological or large-field sector produces an unbounded contribution not captured by the flowed sector kernels.

## Learning

Cycle 315 makes the pressure explicit: Schur-Feshbach endpoint positivity, positive flowed pair covariance, and same-theory recovery must jointly be valid, but connected four-curvature polarization can still erase the mediator. The carrier critique is that raw Wilson contours are representation-limited and fragmented; global OS spectral transfer and non-Gaussian Schwinger-family witnesses are too coarse for this local finite obstruction. Endpoint sheet currents are efficient because they encode H,K sheets, endpoint moments, sector kernels, counterterms, and recovery errors; preserve gauge/color/reflection/orientation/cutoff/locality/same-theory invariants; use Ward/cusp subtraction, Taylor Hessians, heat-kernel majorants, outward-rounded interval arithmetic, and zero-pairing quotienting as primitives; keep finite endpoint-cell locality; and expose falsifiers. The conceptual value signal is local but route-changing: R_{++}/kappa_4 is now a finite color-geometric lower interval with a sign/size test, not a symbolic endpoint term. Success changes only finite endpoint-box positivity after H,K; Clay existence, OS/Wightman axioms, nontrivial continuum limit, observable density, large-field/topology control, OS spectral transfer, and positive Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a validator-facing falsifier probe for the same-theory nontriviality witness-compatible endpoint cumulant.`
- Rationale: The branch has already restated the sector-constant route many times; the next valid information is whether Ward-Hessian scaling can actually dominate the connected C4 polarization in the H,K endpoint geometry.
- Situation seed: Finite-volume SU(3) Wilson lattice Yang-Mills with reflection plane fixed, gradient-flow time t, two H,K plus-channel endpoint boxes, centered renormalized thin hairpins recovered as endpoint sheet currents, and R_{++}^{ren} evaluated by flowed pair and Ward-subtracted C4 sector kernels.
- Varied variable: eta, the endpoint-cell diameter divided by sqrt(8t), varied through eta=1/16,1/24,1/32 while keeping the endpoint separation in flow units fixed.
- Held-fixed controls: same cutoff measure, Wilson action, volume, reflection plane, H,K endpoint geometry, and plus-channel vector, same gradient-flow time t, point-splitting hierarchy a << epsilon << sqrt(8t), and one-hairpin cusp subtraction, same zero-pairing quotient policy and recovery map rho with outward-rounded recovery error, same Schur-Feshbach leakage L_+ and finite matrix normalization
- Expected observation: If the endpoint-moment mechanism is real, the dominance ratio D(eta)=N sum_sigma H_sigma^{I,+}M_{2,+}^2/(8G_{++}^{I,-}) should decrease like O(eta^2) until recovery and interval-width errors dominate. A flat or increasing D is a demoting falsifier.
- Transfer certificate needed: A deterministic interval certificate, not Monte Carlo evidence: outward-rounded pair lower bounds, sector Hessian upper bounds, recovery errors, and cutoff-window stability sufficient to insert R_{++}^{I,-} into the same finite Schur-Feshbach inequality.

## Next Experiment

Route explicitly to proof search: compute outward-rounded near/far Hessian intervals for {3g,4g,ct,end} in the fixed H,K endpoint geometry, certify the zero-pairing recovery map, and test the connected cumulant witness inequality R_{++}^{I,-}>L_+-Q_+^0+delta_cert.

# Raw K4 connected cumulant witness for finite post-H,K endpoint stress

## Candidate Lemma

Finite raw-K4 phase functional lemma: in one heat-kernel cutoff theory, rigorous plaquette-level intervals for the connected four-curvature cumulant give a computable lower bound on the phased off-diagonal endpoint entry. If the resulting two-sparse Rayleigh upper bound tau_pq(theta) is negative, the worked H,K endpoint matrix is not positive semidefinite. This is a finite Route A falsifier only.

## Definitions

- source object: heat-kernel regulated finite-volume SU(N) lattice Yang-Mills measure at spacing a, smearing sigma, coupling g_R, with oriented endpoint plaquette sheets and Wilson transporters.
- target object: the finite Schur-corrected endpoint Hermitian matrix U_sigma on the post-H,K boundary basis, not the continuum Hamiltonian.
- controlled interface: raw connected plaquette cumulant witness mapping same-regulator Wilson/OPE data to U_sigma interval entries and two-sparse Rayleigh tests.
- same-theory condition: the cumulants, Gaussian covariance, OPE error, endpoint Wilson basis, and H,K Schur blocks use the identical cutoff action, volume, coupling, smearing, and normalization.
- bridge carrier: endpoint observables Q_i are normal-ordered quadratic transported curvature fluxes built from oriented plaquettes in the boundary collar.
- recovery map: raw plaquette cumulant intervals are summed with Wilson sheet weights, color contractions, OPE intervals, and Schur data to recover interval enclosures for U_sigma entries.

## Assumptions

- Model: finite heat-kernel SU(N) lattice Yang-Mills on a four-dimensional torus; no continuum, infinite-volume, or Hamiltonian claim is made.
- Cutoff: the smearing radius sigma and lattice spacing a are fixed with finite endpoint sheets and finite H,K blocks.
- Same-theory: all intervals are computed under the same cutoff measure, same Wilson transporters, and same endpoint basis used in the Schur subtraction.
- Validity: interval arithmetic encloses the exact finite-dimensional group integrals or an independently certified constructive bound.
- Local: only endpoint-box plaquettes entering Q_p and Q_q are summed; distant plaquettes enter only through certified OPE remainders.
- Constraint: exact Wilson trace identities may be quotiented, but heuristic sheet symmetries without an invariant audit are invalid.

## Equations

- transported plaquette curvature: `X_{r}^{a}(b)= -\frac{2}{a^{2}}\operatorname{Tr}\!\left(T^{a}U_{b\leftarrow r}\frac{U_{r}-U_{r}^{\dagger}}{2i}U_{r\leftarrow b}\right)`. Valid when: Valid when the plaquette r lies in the finite endpoint collar and the transporter path to basepoint b is fixed in the Wilson sheet definition.
- normal-ordered endpoint carrier: `Q_i=:\sum_{r,s\in S_i} w_{ir}w_{is}\,X_r^a(b)X_s^a(b):`. Valid when: Applies after same-cutoff vacuum and perimeter subtractions are fixed for the endpoint Wilson observable Q_i.
- connected boundary polarization: `R_{ij,\sigma}=\operatorname{cum}_2(Q_i,Q_j)=\langle Q_iQ_j\rangle_\sigma-\langle Q_i\rangle_\sigma\langle Q_j\rangle_\sigma`. Valid when: Valid when Q_i and Q_j are evaluated in the identical heat-kernel cutoff theory with the same reflection support convention.
- raw K4 decomposition: `R_{ij,\sigma}=\alpha_N g_R^4(C_\sigma\circ C_\sigma)_{ij}+\frac{g_R^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma}`. Valid when: Requires the boundary OPE expansion through four transported curvatures and certified control of the discarded higher plaquette terms.
- Schur-corrected endpoint entry: `U_{ij,\sigma}=R_{ij,\sigma}-(B_\sigma^*E_\sigma^{-1}B_\sigma)_{ij}`. Valid when: Valid when the H,K hairpin block E_sigma is positive on the eliminated subspace and the Schur complement uses the same Wilson basis.
- raw interval phase lower bound: `L_{pq}(\theta)=\underline{\operatorname{Re}(e^{i\theta}U_{pq,\sigma})}=G_{pq}^{\theta,-}+\frac{g_R^4}{16N^2}\sum_\nu \min_{z\in I_\nu}\operatorname{Re}(e^{i\theta}c_\nu z)-e^{\mathrm{OPE}}_{pq}-s_{pq}^{\theta,+}`. Valid when: Applies when every raw K4 cumulant interval I_nu entering U_pq has a certified coefficient c_nu and outward-rounded interval arithmetic.
- two-sparse stress certificate: `\tau_{pq}(\theta)=u_{pp}^{+}-\frac{L_{pq}(\theta)^2}{u_{qq}^{+}},\qquad x_{pq}=e_p-e^{-i\theta}\frac{L_{pq}(\theta)}{u_{qq}^{+}}e_q`. Valid when: Valid when u_pp^+ and u_qq^+ are rigorous diagonal upper bounds, u_qq^+ is positive, and L_pq(theta) is positive.

## Attempted Derivation

- Conceptual pressure attacked: replace the quarantined phase-stress abstraction by a validator-facing raw K4 interval computation for the connected boundary-OPE polarization.
- Declarative tension: Wilson/OPE coefficients, raw connected K4 negativity, OPE error, and H,K Schur subtraction must all hold in one cutoff theory, while OS reconstruction, gauge-invariant observable density, excitation-sector cyclicity, continuum nontriviality, and the mass gap are barred as conclusions.
- Carrier critique: scalar R is too weak, A012 shells are convenient but quarantined, OS Hilbert observable algebra is too strong and circular for this local gate, and raw plaquette enumeration is fragmented yet valid.
- Compared route: full Delta_raw PSD proof search is stronger but expensive; two-sparse raw K4 stress search is a sharper negative tactic because three interval types can yield a falsifier.
- Define transported plaquette curvatures X_r^a at a common basepoint and build normal-ordered quadratic endpoint carriers Q_i.
- Use connected cumulants; the vacuum/perimeter and disconnected two-point pieces cancel by normal ordering and cum_2, leaving the Gaussian crossed contraction plus connected K4 and OPE remainder.
- Compress R_sigma by the same post-H,K Schur complement to obtain U_sigma.
- For each pair p,q and phase theta, interval-sum the raw K4 coefficients with outward rounding to get L_pq(theta).
- Use the two-sparse vector x=e_p-exp(-i theta)L/u_qq^+ e_q to derive x^*U_sigma x <= tau_pq(theta).
- Hard gate: tau_pq(theta)<0 produces a finite connected cumulant witness falsifier for endpoint PSD; tau survival changes no positivity theorem and sends the branch to full Delta_raw proof search.

Blocking gap: The missing object is still numerical or symbolic-certified same-regulator raw K4 interval data I_nu for the actual endpoint plaquette cumulants. Without those intervals, the phase functional is only an admissible proof recipe.

## Falsifiers

- falsifier: a certified pair p,q,theta with tau_pq(theta)<0 gives a negative Rayleigh vector and demotes the worked finite H,K endpoint route.
- A regulator mismatch between raw K4 intervals and the Schur block invalidates the same-theory transfer.
- A non-invariant plaquette quotient that changes L_pq(theta) under exact Wilson identities invalidates the interval certificate.
- If all same-regulator intervals are too wide to determine L_pq(theta), the phase-stress abstraction remains quarantined and cannot be promoted.
- A higher-rank negative vector after tau survival is a falsifier for the claim that two-sparse survival implied endpoint positivity.

## Learning

Cycle 315 shifts the branch from repeating the tau criterion to specifying the raw interval functional that a validator can compute. The efficient representation must encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/K4 separation, endpoint compression, same-theory normalization, and exact Wilson quotienting; support cumulant contraction, interval summation, phase certification, Rayleigh stress search, Loewner bounds, and Schur subtraction; quotient only by exact Wilson identities; keep finite endpoint-box complexity; transfer only through tau, Delta_raw, or x_stress; and demote on negative margin, missing intervals, non-invariant quotienting, or regulator mismatch. Conceptual value signal: sharp and route-changing at finite scope because R is now a connected cumulant witness with an explicit raw plaquette interval recovery map, not a scalar parameter or an OS-density restatement.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: Recent cycles established that abstract phase-stress language is looping; a concrete cutoff thought experiment is needed to expose whether raw connected K4 intervals can actually decide the finite endpoint gate.
- Situation seed: Heat-kernel SU(2) lattice Yang-Mills on a finite 4D torus with one fixed H,K collar/hairpin endpoint box, two boundary plaquette sheets p and q, normal-ordered quadratic curvature carriers Q_p,Q_q, and the connected cumulant witness R_pq,sigma.
- Varied variable: rho=sigma/a, the heat-kernel smearing-to-lattice-spacing ratio in the endpoint collar.
- Held-fixed controls: Same lattice action, finite volume, bare/renormalized coupling convention, and Wilson transporter paths., Same post-H,K endpoint basis, Schur block B^*E^{-1}B, normal-ordering convention, and OPE truncation order., Exact Wilson trace quotient policy and outward-rounded interval arithmetic for every plaquette cumulant.
- Expected observation: As rho varies, either the phased off-diagonal raw K4 lower interval exceeds the Gaussian-Schur-OPE diagonal threshold and yields tau_pq(theta)<0, or it stays below threshold and forces full Delta_raw search rather than another abstraction cycle.
- Transfer certificate needed: A same-theory interval certificate for all plaquette cumulants entering K4_pq, diagonal upper intervals for U_pp and U_qq, an invariant quotient audit, and a proof that the heat-kernel regulator used in intervals is identical to the regulator used in H,K.

## Next Experiment

Proof search: compute the first same-regulator raw K4 interval set for one SU(2) heat-kernel endpoint pair p,q,theta, recover the connected cumulant witness L_pq(theta), and either output x_stress as a falsifier or hand off to full Delta_raw Loewner certification.

