# cycle-0349

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: one-sided endpoint source screen

## Candidate Lemma

One-sided root-quartic leakage screen: for the fixed post-H,K reflected-Wilson hairpin block, the endpoint part of the connected boundary-OPE polarization admits a same-theory lower bound depending only on positive aggregated D leakage, root-quartic source norms, and a uniform tail.

## Definitions

- source object: heat-kernel plaquette-sheet endpoint source classes c, with class source L_c in su(N), heat time t_c, and regulated endpoint partition function Z_c(sL_c).
- target object: the finite post-H,K reflected-Wilson OS Schur-Feshbach scalar I_gate for the fixed three-hairpin block, not a continuum mass-gap statement.
- controlled interface: C_ep maps same-theory endpoint source derivatives, aggregated signed incidences D_c, color factor C_N, Gaussian margin M_G, and tail interval T_tail to a lower interval for I_gate.
- same-theory condition: every Z_c(sL_c) is computed in the same reflection-positive heat-kernel Wilson regulator with the locked Wilson observable normalization and no boundary counterterm.
- A_c=-iL_c is the Hermitian traceless endpoint source representative; ||A_c||_2^2=tr(A_c^2).
- D_c is the source-equivalence aggregated null-channel incidence; clipping is applied after aggregation, never before.
- C_N=(g_a^4/4)(T_F/N)^2 is the singlet color prefactor inherited from the Wilson four-flux contraction.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflected Wilson plaquette-sheet collar regulator.
- Regime: fixed finite H,K hairpin block after Wick-square positivity and straight f f contact cancellation have already been certified.
- Cutoff: t_c, source support, endpoint boxes, and the tail estimate are chosen uniformly in the collar cutoff window used for this finite block.
- Same-theory: source derivatives are derivatives of the original Wilson expectation, not of a boundary-renormalized or enlarged endpoint theory.
- Uniformity: the endpoint remainder satisfies |E_c|<=epsilon_c and the off-box remainder satisfies |T_tail|<=T_tail^max with constants stable under the finite cutoff removal tested here.
- Validity: the root-quartic Haar expansion is used only inside normal-coordinate endpoint boxes where the heat-kernel small-field remainder is bounded.
- Local: the lemma changes only the finite post-H,K OS transfer gate; continuum existence, gauge-invariant observable density, OS spectral transfer, nontriviality, and mass gap remain untouched.

## Equations

- connected endpoint cumulant witness: `\kappa_c(L_c)=\left.\partial_s^4\log Z_c(sL_c)\right|_{s=0}=\langle X_c(L_c)^4\rangle_{c,\mathrm{conn}}`. Valid when: Valid when the endpoint source is inserted in the locked heat-kernel Wilson regulator and the connected logarithm is taken before source-equivalence aggregation.
- root-quartic endpoint expansion: `\kappa_c(L_c)=-\frac{t_c^4}{60}\mathcal R_4(A_c)+E_c,\qquad \mathcal R_4(A)=N\operatorname{tr}(A^4)+3(\operatorname{tr}A^2)^2`. Valid when: Applies inside a heat-kernel endpoint normal-coordinate box after the Gaussian fourth derivative vanishes and the Haar-Jacobian quartic term dominates the certified remainder.
- SU(N) quartic norm cap: `4\|A_c\|_2^4\le \mathcal R_4(A_c)\le (N+3)\|A_c\|_2^4`. Valid when: Valid for Hermitian traceless SU(N) source representatives using tr(A^4) between (tr A^2)^2/N and (tr A^2)^2.
- one-sided post-HK lower screen: `I_{\mathrm{gate}}\ge M_G-C_N\sum_{c:D_c>0}D_c\left(\frac{t_c^4}{60}(N+3)\|A_c\|_2^4+\epsilon_c\right)-T_{\mathrm{tail}}^{\max}`. Valid when: Requires the fixed H,K block cancellations, source-equivalence aggregation before clipping, nonnegative color prefactor, and cutoff-uniform endpoint and tail error bounds.

## Attempted Derivation

- Attack conceptual pressure: endpoint collapse must be sign-certified inside the same Wilson theory after H,K, rather than hidden in symbolic R or raw kappa spectra.
- Fix the heat-kernel plaquette-sheet regulator and the locked finite three-hairpin Wilson block; keep the already validated Wick-square Gram positivity and straight f f null-incidence cancellation.
- Replace endpoint boxes by source-equivalence classes using equality of regulated source data; aggregate signed D_c before clipping so null-channel cancellations survive.
- Use heat-kernel normal coordinates at an endpoint: the Gaussian log is quadratic, hence contributes no fourth connected source derivative; the first non-Gaussian term is the negative SU(N) Haar root-quartic cumulant.
- Bound the root-quartic invariant by 4||A||_2^4 and (N+3)||A||_2^4, giving a conservative one-sided lower screen depending only on positive D_c leakage.
- Insert endpoint remainders epsilon_c and a uniform tail T_tail^max to obtain a finite interval lower bound for I_gate.

Blocking gap: No actual same-theory source stencil intervals or cutoff-uniform tail bound are available for the positive-D endpoint classes, so the branch cannot promote the finite block.

## Falsifiers

- A positive-D source class with a certified negative connected cumulant witness large enough that the full I_gate interval lies below zero is a finite same-theory falsifier.
- The endpoint tail T_tail fails to be cutoff-uniform or has a negative lower bound exceeding the Gaussian margin.
- The seven source evaluations require a boundary counterterm, showing that the carrier no longer computes the same Wilson theory.
- Source-equivalence aggregation identifies boxes with different regulated source data, invalidating the signed cancellation.
- The heat-kernel normal-coordinate remainder epsilon_c is too large for the root-quartic one-sided screen to be valid.

## Learning

Cycle 349 adds a concrete estimate rather than another quarantine slogan. The declarative tension is collar OS positivity plus fixed gauge-invariant Wilson observables plus singular endpoint OPE without adding a boundary theory; raw R is too weak, raw kappa spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. The efficient representation C_ep must encode source classes, source stencils or root-quartic caps, cumulant intervals, aggregated D_c, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; use source differentiation, interval arithmetic, aggregation before clipping, color multiplication, and tail addition; identify equivalence only by regulated source data; export only I_gate; and demote on a negative interval, nonuniform tail, or boundary counterterm. The hard gate changed is the finite post-H,K reflected-Wilson OS scalar: success promotes only this finite block, failure gives a finite falsifier, and missing data keeps quarantine. The conceptual value signal is sharp finite Route A progress: negative SU(N) endpoint cumulants are explanatory but not the obstruction; only positive-D leakage times a same-theory connected cumulant witness plus uniform tail can lower the gate. Clay continuum construction, gauge-invariant observable density, full OS/Wightman reconstruction, nontriviality, OS spectral transfer, and positive mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use as a concrete falsifier probe now, while keeping quarantine until actual endpoint source intervals are supplied.`
- Rationale: The branch has looped on carrier language; a target-preserving endpoint experiment tests the only remaining finite obstruction, positive-D leakage times a connected cumulant witness plus uniform tail.
- Situation seed: SU(N) heat-kernel plaquette-sheet endpoint box for the fixed post-H,K three-hairpin collar block; choose one source class with b12=1 and b13=b23=alpha/2, then compute the seven-point log-source stencil for L_c.
- Varied variable: alpha, the fractional overlap leakage from the 12 endpoint footprint into the 13 and 23 endpoint footprints, so D_c=2-4alpha crosses the half-overlap shield at alpha=1/2.
- Held-fixed controls: The heat-kernel Wilson plaquette regulator and reflection-positive lattice measure., The fixed H,K hairpin block, null vector, Wilson normalization, and color factor C_N., The same endpoint source L_c and same-theory connected cumulant witness computed by log Z_c source derivatives., The tail accounting rule charging all off-box contributions to T_tail.
- Expected observation: For alpha>=1/2 the negative root-quartic cumulant is shielded in the lower screen; for alpha<1/2 the gate decreases linearly in 2-4alpha and can become a finite falsifier only if the source interval plus tail overwhelms M_G.
- Transfer certificate needed: A cutoff-uniform seven-point source interval, a valid M8 remainder, no boundary counterterm, and a same-theory proof that all nonendpoint interactions are included in T_tail before the intuition affects proof obligations.

## Next Experiment

Run targeted proof search for the positive-D endpoint classes: compute the same-theory connected cumulant witness by the seven-point heat-kernel source stencil, certify M8 and T_tail, then return the interval sign of I_gate; otherwise keep quarantine.

# Gauge-Invariant Nontriviality Witness Selection: first-annulus R++ quadrature certificate

## Candidate Lemma

First-annulus plateau quadrature gives a conditional finite lower interval for the actual post-H,K connected boundary-OPE polarization R_{++}^{ren}; if the certified margin Delta_R^- is positive it promotes finite endpoint-box positivity, and if not it quarantines this R repair without implying any Clay mass-gap claim.

## Definitions

- source object: finite-volume lattice SU(N) Yang-Mills with Wilson action at spacing a, gradient-flowed curvature F_t, reflected H,K thin hairpin endpoint sheet currents J_H,J_K, and centered perimeter/cusp-subtracted Wilson observables \widehat W_t(J).
- target object: the finite post-H,K Schur-Feshbach endpoint-box plus-channel positivity margin Delta_R^- compared with the known leakage scalar L_+.
- controlled interface: an outward-rounded annular Ward-Hessian quadrature that maps the same-theory connected flowed Wilson cumulant R_{++}^{ren} to a color-geometric lower interval.
- same-theory condition: the cumulants, counterterms, recovery maps, annular kernels, H,K sheets, flow time t, and leakage input L_+ all come from one cutoff family and one limiting Schwinger candidate.
- carrier: endpoint sheet currents modulo certified zero-pairing equivalence, not raw Wilson contours.
- first annulus: A_0={z:r_0<=|z-z_E|<=2r_0} in endpoint relative coordinates, with r_0 comparable to sqrt(8t) and separated from other collars.
- connected cumulant witness: R_{++}^{ren}=kappa_2 of two centered renormalized H,K plus-hairpin observables, used only as a finite same-theory nontriviality witness boundary.

## Assumptions

- Model: finite torus lattice SU(N), N>=2, Wilson gauge action, gauge-invariant flowed observables, and no gauge fixing in the observable definition.
- Regime: a<<sqrt(8t), endpoint cell diameter eta sqrt(8t) with eta<1/8, and H,K endpoint boxes disjoint from nonlocal contour intersections.
- Cutoff: gradient flow supplies smooth F_t and all point-splitting/cusp subtractions are performed before taking any continuum-scaling comparison.
- Same-theory: the Wilson measure, flowed Wilson cumulants, recovery maps, and Schur-Feshbach finite matrices are evaluated on the same regulator trajectory.
- Uniformity: the annular Hessian majorants and recovery errors are bounded uniformly for the finite volume and cutoff window used by the certificate.
- Validity: Ward and cusp subtractions remove the endpoint monopole and tangent cusp terms, leaving the plus-channel monopole/dipole moments zero.
- Local: only the first plateau annulus and its dyadic tail are used; no continuum OS reconstruction or Hamiltonian spectral statement is claimed.
- Constraint: outward-rounded interval quadrature encloses every cell kernel value and every arithmetic operation in the lower-bound formula.

## Equations

- same-theory cumulant carrier: `R_{++}^{ren}(t,a)=\kappa_2\big(\widehat W_t(J_+),\widehat W_t(J_+)\big),\qquad J_+=J_H+J_K`. Valid when: Valid when the centered flowed Wilson hairpins use the same cutoff ensemble, identical H,K endpoint currents, and the stated perimeter/cusp subtraction scheme.
- Ward-plus moment cancellation: `\int_{E} J_+(x)\,dx=0,\qquad \int_E (x-x_E)_\alpha J_+(x)\,dx=0`. Valid when: Valid when the reflected H,K endpoint sheets have matched orientation and the Ward/cusp counterterms have been applied before annular expansion.
- positive pair baseline: `P_{++}=g_t^4\,2(N^2-1)\,G_{++},\qquad G_{++}=\int J_+(x)K_{2,t}(x-y)J_+(y)\,dx\,dy\ge0`. Valid when: Valid when K_{2,t} is the flowed two-curvature covariance restricted to gauge-invariant sheet currents in the finite reflected endpoint geometry.
- first-annulus Hessian enclosure: `U_s^{(0)}\in \sum_{Q\in\mathcal P_0}|Q|\,[\inf_Q h_s,\sup_Q h_s],\qquad h_s(z)=\|\nabla_z^2 K^{ren}_{4,s}(t,z)\|`. Valid when: Valid when the connected four-curvature sector kernel is Ward-subtracted, smooth on each first-annulus cell, and evaluated with outward-rounded interval arithmetic.
- plateau tail compression: `T_s^{tail,+}\le \frac{U_s^{(0),+}}{1-q_s^+},\qquad q_s^+=\sup_n\frac{U_s^{(n+1),+}}{U_s^{(n),-}}<1`. Valid when: Valid when the dyadic annular sector constants satisfy a certified plateau ratio below one throughout the regulated endpoint window.
- promotion margin: `\Delta_R^-=g_t^4(N^2-1)\left(2G_{++}^- -N M_{2,+}^2\sum_s(U_{s,near}^+ +T_s^{tail,+})\right)-E_{rec}^+-E_6^+-L_+`. Valid when: Valid when the pair lower interval, C4 sector upper intervals, same-theory recovery error, Wilson expansion remainder, and Schur-Feshbach leakage are all certified in the same finite H,K instance.

## Attempted Derivation

- Attack pressure: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator; positive pair covariance and recovery can both be valid while connected C4 still destroys R_{++}.
- Expand each centered flowed hairpin in endpoint sheet currents through order g_t^4, with disconnected products and one-hairpin perimeter/cusp pieces subtracted.
- The two-curvature cross-pairings give the positive baseline 2(N^2-1)G_{++}; positivity follows from the reflected covariance on the endpoint sheet current span.
- Decompose the connected four-curvature remainder into renormalized sectors s: three-gluon exchange, four-gluon vertex, counterterm, and endpoint subtraction kernels, each with color factor N(N^2-1).
- Use Ward/cusp subtraction and plus-channel moment cancellation to remove constant and linear endpoint Taylor terms; the first surviving bound is a mixed Hessian times M_{2,+}^2.
- Localize the dangerous C4 contribution to a near box plus dyadic annuli; represent the first plateau annulus by interval cells Q and bound h_s=||nabla^2 K_{4,s}^{ren}|| on each cell.
- Compress remaining annuli by a certified ratio q_s^+<1 and insert the resulting tail bound into Delta_R^-.
- Compare Delta_R^- with zero: positive promotes finite endpoint-box positivity after H,K; nonpositive or uncertified plateau is a route-deciding falsifier for this R repair.

Blocking gap: The first-annulus sector constants U_s^{(0)}, the plateau ratios q_s^+, and E_rec have not yet been numerically or analytically enclosed with outward-rounded intervals for the concrete H,K geometry.

## Falsifiers

- First-annulus interval width is so large that Delta_R^- cannot be signed.
- A sector plateau ratio q_s^+ is >=1 or cutoff-dependent, invalidating dyadic tail compression.
- Ward or cusp residuals leave a nonzero monopole/dipole term, so Hessian suppression is false.
- The H,K plus geometry makes G_{++}^-=0 or too small compared with certified C4 majorants.
- The recovery error E_rec between raw Wilson contours and endpoint currents exceeds the positive pair baseline.
- A same-theory check fails because R_{++}, counterterms, and L_+ are computed on different regulator trajectories.
- The connected cumulant witness survives only at finite cutoff and has no stable plateau in physical units.
- Interval quadrature loses gauge/color/reflection/orientation invariants under cell subdivision.

## Learning

Cycle 349 attacks the conceptual pressure that finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator. The declarative tension is exact: endpoint positivity, positive flowed pair covariance, and raw-hairpin recovery may each be valid while connected C4 erases R_{++}. The current raw-contour carrier is fragmented and representation-limited; global OS spectral transfer, area-law intuition, and broad non-Gaussian Schwinger family witness selection are too coarse for this finite obstruction. Endpoint sheet currents are the sharper abstraction because they encode H,K sheets, endpoint moments, sector kernels, counterterms, recovery errors, and L_+; preserve gauge, color, reflection, orientation, cutoff, locality, and same-theory invariants; use cumulant expansion, Ward/cusp subtraction, Taylor Hessian remainders, heat-kernel majorants, dyadic tail compression, outward-rounded interval algebra, and certified zero-pairing equivalence; keep finite endpoint locality plus summable annuli; and expose falsifiers. Hard gate: finite endpoint-box positivity after H,K. Success promotes one finite Route A gate; failure quarantines the R repair. Conceptual value signal: the connected boundary-OPE polarization is now a first-annulus quadrature theorem with a dominance margin, not a symbolic endpoint term; every Clay target gate remains untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and proof-search calibration for the first-annulus certificate.`
- Rationale: The branch has already reduced R_{++} to an annular Ward-Hessian dominance margin; another abstract restatement would not decide whether C4 erases the positive pair mediator.
- Situation seed: Finite torus SU(N) Wilson lattice Yang-Mills with gradient flow at fixed physical t, reflected H,K endpoint hairpins, centered flowed Wilson variables, and outward-rounded quadrature of the first plateau annulus A_0 for each connected C4 sector.
- Varied variable: rho=r_0/sqrt(8t), the inner radius of the first annulus in flow units, varied over a small admissible grid while eta, H,K geometry, and t remain fixed.
- Held-fixed controls: Same Wilson action, same RG/cutoff trajectory, and same gradient-flow definition for all cumulants., The reflected H,K endpoint sheet currents, plus-channel combination J_+, and Schur-Feshbach leakage L_+ are held fixed., Ward/cusp subtraction scheme, zero-pairing quotient tests, color normalization tr(T^aT^b)=delta^{ab}/2, and outward-rounded interval arithmetic are held fixed., Finite volume is chosen larger than the endpoint collar plus annular tail radius, with boundary effects included in E_rec.
- Expected observation: If the route is viable, normalized sector constants U_s^{(1)}/U_s^{(0)} cluster below a stable q_s^+<1 and Delta_R^- remains positive for a nonempty rho window; if not, a concrete dominance or plateau falsifier appears.
- Transfer certificate needed: A cutoff-uniform same-theory recovery bound and flowed cumulant convergence certificate showing that the quadrature intervals bound the exact regulated R_{++}^{ren} used in the finite H,K Schur-Feshbach matrix.

## Next Experiment

Route to proof search: instantiate the concrete H,K first-annulus cell partition, evaluate sector Hessian intervals U_s^{(0)} with outward rounding, compute q_s^+ and E_rec, then decide the connected cumulant witness margin Delta_R^- as promotion or falsifier.

# Gauge-Invariant Observable Density In The Excitation Sector

## Candidate Lemma

Finite support-function stress theorem: for a fixed heat-kernel cutoff and worked H,K endpoint box, diagonal upper bounds and a support-function lower bound for one signed off-diagonal connected cumulant witness falsify Schur-corrected endpoint PSD whenever D_p^+<0, D_q^+<0, or L_{pq}^2>D_p^+D_q^+. This is a finite Route A falsifier, not a Clay mass-gap theorem.

## Definitions

- source object: the heat-kernel regulated finite-lattice SU(N) Wilson endpoint data R_G, K^{(4)}, E^{OPE}, and S_{HK} for the same H,K collar/hairpin endpoint box.
- target object: the two-dimensional compression U_{pq,\sigma}=P_{pq}(R_G+K^{(4)}+E^{OPE}-S_{HK})P_{pq} of the post-H,K endpoint quadratic form.
- controlled interface: a signed-orbit support-function recovery map sending raw connected K4 plaquette intervals to a lower bound L_{pq} on the modulus of the actual off-diagonal entry U_{pq}.
- same-theory condition: all Gaussian contractions, raw K4 intervals, OPE errors, Schur blocks, Wilson normalizations, coupling, cutoff a, and smoothing scale \sigma are taken from one regulated Yang-Mills measure.
- D_i^+ is a validator-facing upper bound for the actual diagonal entry U_{ii}.
- C_{pq} is the complex interval zonotope containing the actual off-diagonal U_{pq}.
- L_{pq} is a certified lower bound for |U_{pq}| obtained from a support direction rather than a phase-net scan.

## Assumptions

- Model: four-dimensional finite hypercubic torus lattice SU(N) Yang-Mills with heat-kernel plaquette regulator, spacing a, and smoothing scale \sigma.
- Cutoff: the H,K collar/hairpin Wilson endpoint box, endpoint index set, and Schur complement block are finite and fixed before interval extraction.
- Same-theory: R_G, K^{(4)}, E^{OPE}, and S_{HK} are computed with the same cutoff measure, same Wilson basis, and same reflected endpoint normalization.
- Validity: interval arithmetic is outward-rounded, Hermitian symmetry U_{qp}=\overline{U_{pq}} is enforced, and only exact Wilson trace identities are used for quotienting.
- Local: the theorem changes only the finite Route A endpoint PSD gate; OS reconstruction, gauge-invariant observable density, excitation-sector cyclicity, continuum nontriviality, and Hamiltonian mass gap remain untouched.

## Equations

- post_HK_endpoint_matrix: `U_\sigma=P_E\left(R_{G,\sigma}+K^{(4)}_\sigma+E^{OPE}_\sigma-S_{HK,\sigma}\right)P_E`. Valid when: Valid when the endpoint compression P_E, Wilson OPE expansion, and Schur block are all fixed in the same heat-kernel cutoff theory.
- diagonal_upper_bound: `U_{ii,\sigma}\le D_i^+:=G_{ii}^++K_{ii}^{(4),+}+e_{ii}^{OPE,+}-s_{ii}^{HK,-}`. Valid when: Applies when each diagonal ingredient has an outward interval bound and s_{ii}^{HK,-} is a lower bound for the same Schur energy.
- signed_orbit_offdiagonal_zonotope: `U_{pq,\sigma}\in C_{pq}:=c_{pq}+\sum_{o\in\mathcal O_{pq}}[-r_o,r_o]w_o+B_{\varepsilon_{pq}}(0)`. Valid when: Requires the signed raw K4 orbit quotient, Gaussian off-diagonal term, OPE interval, and Schur subtraction to use the identical regulator.
- support_lower_bound: `L_{pq}:=\sup_{|u|=1}\left(\Re(\overline u c_{pq})-\sum_o r_o|\Re(\overline u w_o)|-\varepsilon_{pq}\right)_+\le |U_{pq,\sigma}|`. Valid when: Valid when C_{pq} contains the actual off-diagonal entry and the displayed support inequality is certified for all orbit uncertainties.
- two_sparse_hard_gate: `D_p^+<0\ \vee\ D_q^+<0\ \vee\ L_{pq}^2>D_p^+D_q^+\quad\Longrightarrow\quad P_{pq}U_\sigma P_{pq}\not\succeq0`. Valid when: Applies to a Hermitian two-endpoint compression after the diagonal and off-diagonal interval bounds enclose the same actual matrix entries.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: the heat-kernel regulated finite-lattice SU(N) Wilson endpoint data R_G, K^{(4)}, E^{OPE}, and S_{HK} for the same H,K collar/hairpin endpoint box.; target object: the two-dimensional compression U_{pq,\sigma}=P_{pq}(R_G+K^{(4)}+E^{OPE}-S_{HK})P_{pq} of the post-H,K endpoint quadratic form.; Model: four-dimensional finite hypercubic torus lattice SU(N) Yang-Mills with heat-kernel plaquette regulator, spacing a, and smoothing scale \sigma..
- Freeze the Clay target boundary: only a finite Route A endpoint-box PSD decision is being attacked; continuum Schwinger coherence, OS positivity, gauge-invariant observable density, excitation-sector cyclicity, and mass gap transfer are non-claims.
- Define the same-theory post-H,K matrix U_sigma from the Gaussian Wilson contraction, raw connected K4 cumulant, OPE interval, and Schur hairpin subtraction in one heat-kernel cutoff theory.
- Recover the off-diagonal entry U_pq as a complex signed-orbit interval zonotope C_pq, retaining orientation phases that A012 shell compression would lose.
- Use the support function of C_pq to certify a lower bound L_pq for |U_pq| without relying on a finite phase-net scan.
- Invoke the two-by-two PSD necessary condition: a Hermitian PSD matrix must satisfy U_pp>=0, U_qq>=0, and |U_pq|^2<=U_pp U_qq.
- Combine actual diagonal upper bounds U_pp<=D_p^+, U_qq<=D_q^+ with |U_pq|>=L_pq; the hard gate D_p^+<0, D_q^+<0, or L_pq^2>D_p^+D_q^+ contradicts PSD.
- Recover an explicit stress vector from the support direction when the strict off-diagonal gate holds.

Blocking gap: The branch still lacks same-regulator raw K4 orbit intervals and a certified support-function optimization certificate for a concrete endpoint pair p,q.

## Falsifiers

- falsifier: the raw signed K4 orbit intervals make C_pq contain the origin, forcing L_pq=0 and killing the two-sparse demotion route.
- falsifier: OPE overflow or Schur interval uncertainty raises D_p^+D_q^+ above every certified L_pq^2.
- falsifier: exact Wilson quotient auditing finds that a signed orbit identification changed a phase or orientation sign.
- falsifier: the K4 intervals come from a regulator, coupling, volume, or Wilson normalization different from the Gaussian and Schur data.
- falsifier: support-function certification succeeds only on a phase net but fails under rigorous interval optimization between sampled phases.
- Stress case: D_p^+,D_q^+ are small positive numbers while the off-diagonal K4 orbit center is nearly radial; the support theorem should demote quickly if intervals are valid.
- Failure case: all two-sparse stress gates survive; this gives no positivity and forces full Delta_raw Loewner proof search or quarantine.

## Learning

Conceptual pressure attacked: raw non-Gaussian Wilson K4 data must mediate to a finite Schur-corrected endpoint PSD decision without circular OS Hilbert observable algebra or gauge-invariant observable density claims. Declarative tension: Wilson/OPE data, signed K4 orbit intervals, OPE error, and S_HK must all be valid in one cutoff theory, but continuum existence, OS positivity, excitation-sector cyclicity, observable density, and the Clay mass gap are barred conclusions. Carrier audit: scalar R is too weak, A012 shells are sign-losing, phase nets are merely convenient and discretization-sensitive, full Delta_raw is complete but expensive, and signed raw orbits plus support functions preserve phases, Hermiticity, gauge invariance, color, exact quotienting, locality, and same-theory normalization. Efficient representation requirements: encode oriented plaquettes, sheet weights, transporters, color tensors, cumulant intervals, OPE intervals, endpoint phases, support directions, and Schur blocks; preserve gauge invariance, reflection support, Hermiticity, Gaussian/K4 separation, exact Wilson quotienting, and same-theory normalization; primitive operations are cumulant contraction, signed orbit summation, support-function certification, Rayleigh stress search, Loewner bounds, and Schur subtraction; equivalence is only exact Wilson identity quotienting; locality budget is the finite endpoint box; transfer is only through tau, Delta_raw, or x_stress; falsifiers are negative-margin failure, missing intervals, OPE overflow, non-invariant quotienting, or regulator mismatch. Hard gate: D_i^+<0 or L_pq^2>D_p^+D_q^+ gives a valid finite falsifier for the worked H,K endpoint gate; failure gives no positivity and forces full Delta_raw proof search or quarantine. Conceptual value signal: sharp and route-changing at finite scope because Gaussian color positivity, connected non-Gaussian K4, OPE error, and Schur hairpin energy are unified in one same-theory connected cumulant witness while every larger Yang-Mills gate remains untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a target-preserving falsifier probe for the finite endpoint route.`
- Rationale: The branch is blocked by missing raw K4 interval data, not by the OS/Wilson obstruction ladder. A concrete thought experiment tests whether support-function separation can plausibly beat phase-net scanning before requesting validator computation.
- Situation seed: Heat-kernel regulated SU(3) lattice Yang-Mills on a finite four-torus with the worked H,K collar/hairpin endpoint box; choose one reflected Wilson endpoint pair p,q and recover its connected cumulant witness from signed raw K4 plaquette orbits.
- Varied variable: chi, the signed off-diagonal K4 orbit center-to-total-radius ratio along the best support direction, including the phase concentration of orbit weights xi_o.
- Held-fixed controls: Same cutoff a, smoothing scale sigma, coupling g_R, endpoint Wilson basis, and heat-kernel regulator for all terms., Same Schur hairpin block S_HK and same OPE error budget used in the endpoint matrix U_sigma., Exact Wilson trace quotienting, Hermiticity, gauge invariance, and reflected endpoint normalization., Clay-level OS Hilbert observable algebra, gauge-invariant observable density, continuum existence, and mass gap are held as non-claims.
- Expected observation: As chi increases, the support lower bound L_pq should cross sqrt(D_p^+D_q^+) before full Delta_raw PSD can be decided; if it never separates from zero, signed-orbit stress is likely too weak for this geometry.
- Transfer certificate needed: A validator-facing certificate containing raw same-regulator orbit intervals I_o, exact multiplicities n_o, complex phases xi_o, outward diagonal bounds D_i^+, support optimizer proof for u_*, and a check that all entries are from the same finite Wilson theory.

## Next Experiment

Proof search: compute one same-regulator signed raw K4 orbit interval family for a concrete H,K endpoint pair p,q, assemble C_pq and D_p^+,D_q^+, certify the support lower bound L_pq, and either output x_stress as a finite falsifier or quarantine to full Delta_raw interval proof search.

