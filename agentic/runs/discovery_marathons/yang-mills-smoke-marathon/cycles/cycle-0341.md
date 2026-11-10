# cycle-0341

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# One-sided endpoint connected-cumulant screen for the post-H,K Wilson block

## Candidate Lemma

For the heat-kernel plaquette-sheet regulated three-hairpin block, after Wick-square Gram positivity and straight f f incidence cancellation, the post-H,K endpoint term is controlled by a one-sided positive-D leakage screen. This gives a valid promote/falsify/quarantine rule for this finite reflected-Wilson OS scalar only.

## Definitions

- source object: heat-kernel plaquette-sheet endpoint source classes c for the fixed three reflected Wilson hairpins after the H,K Feshbach gate.
- target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for the locked three-hairpin block, not a continuum Yang-Mills mass-gap statement.
- controlled interface: C_ep maps same-theory endpoint source derivatives and signed null incidences to one scalar interval [I_-,I_+] entering the finite OS gate.
- same-theory condition: the endpoint sources, Wilson normalizations, reflection map, and cutoff-removal bookkeeping are inherited from the same regulated Wilson algebra, with no boundary counterterm or boundary Hilbert sector added.
- endpoint source class c: endpoints aggregated only when their regulated source partition functions Z_c(s) agree as source data.
- D_c: aggregated null-channel incidence D_c=sum_{v in c}(2 b12(v)-4 b13(v)-4 b23(v)).
- kappa_c: singlet-projected connected fourth endpoint flux cumulant d_s^4 log Z_c(s)|_{0}.
- C_N: color prefactor (g^4/4)(T_F/N)^2 multiplying the connected endpoint polarization.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette-sheet Wilson regulator and reflected collar hairpins.
- Regime: fixed finite Route A three-hairpin block after the previously computed H,K Schur-Feshbach reduction.
- Uniformity: endpoint source derivative intervals and T_tail bounds are uniform in the cutoff along the chosen regulator/RG subsequence.
- Same-theory: the Wilson loops are not renormalized differently at the reflection plane, and no boundary operator is introduced to repair positivity.
- Validity: Wick-square contractions are treated as positive Gram terms and the straight C_A f f contact is removed by the null incidence identity before C_ep is formed.
- Constraint: source classes are aggregated before clipping positive D leakage; clipping endpoint-by-endpoint is only an upper-screen heuristic.

## Equations

- connected endpoint cumulant witness: `\kappa_c=\left.\partial_s^4\log Z_c(s)\right|_{s=0}=\langle X_c^4\rangle_{c,\mathrm{conn}}`. Valid when: Valid when endpoint source classes are defined by equal regulated heat-kernel source data and X_c is the singlet-projected endpoint flux variable.
- post-HK endpoint gate: `I_{\mathrm{gate}}=M_G+C_N\sum_c D_c\kappa_c+T_{\mathrm{tail}},\qquad C_N=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Valid when Wick-square Gram terms and straight f f contacts have already been removed by the three-hairpin null incidence cancellation.
- one-sided leakage lower bound: `\kappa_c\in[-B_c,0],\ |T_{\mathrm{tail}}|\le\tau\ \Longrightarrow\ I_{\mathrm{gate}}\ge M_G^- - C_N\sum_c [D_c]_+B_c-\tau`. Valid when: Requires certified nonpositive connected endpoint cumulants, nonnegative color prefactor, and a cutoff-uniform endpoint tail bound in the same Wilson theory.
- finite gate decision interval: `I_-:=M_G^- - C_N\sum_c[D_c]_+B_c-\tau,\qquad I_->0\Rightarrow Q_{\mathrm{postHK}}\ge0`. Valid when: Applies only to the fixed finite post-H,K Wilson block after the H,K matrices and null vector are held fixed.

## Attempted Derivation

- Conceptual pressure attacked: endpoint collapse must be sign-certified inside the same Wilson theory after H,K, without hiding the connected boundary-OPE polarization in symbolic R.
- Declarative tension: finite collar OS positivity, fixed gauge-invariant Wilson observables, and singular endpoint OPE must jointly hold, but H,K, half-overlap shielding, and root-quartic negativity do not determine the post-H,K scalar.
- Carrier critique: raw R is representation-limited, raw kappa_4 spectra are too strong because negative cumulants are harmless when D_c<=0, and global Schur-preimage positivity is valid but too coarse after the H,K reduction.
- Abstraction comparison: C_ep is preferable to the global Schur-preimage test for this local gate because it keeps same-theory source data, signed incidence, color prefactor, and tail budget in one scalar transfer interface.
- Use the heat-kernel plaquette-sheet regulator and fixed three-hairpin null vector; remove Wick-square Gram terms and the straight f f contact already cancelled by null incidence.
- Partition endpoints into source-equivalence classes by regulated source data, aggregate signed D before clipping, and form kappa_c=d_s^4 log Z_c(0).
- Assuming kappa_c in [-B_c,0] and |T_tail|<=tau, bound the only dangerous lowering by C_N sum [D_c]_+ B_c and derive I_-.
- Hard gate: the finite post-H,K reflected-Wilson OS transfer scalar. I_->0 promotes only this finite block; I_+<0 gives a finite same-theory falsifier; missing source or tail intervals keeps quarantine.

Blocking gap: The branch still lacks actual same-theory endpoint source intervals for all positive-D classes and a cutoff-uniform T_tail bound. The root-quartic screen supplies a sign mechanism but not the required uniform remainder certificate.

## Falsifiers

- A certified source class with D_c>0 and kappa_c<0 large enough that I_+<0 is a finite same-theory falsifier of this post-H,K block.
- The seven-point connected cumulant witness requires a boundary counterterm to stabilize the endpoint limit, showing the carrier changed theory.
- The tail T_tail is not cutoff-uniform, so endpoint locality cannot be transferred to the finite OS gate.
- Two endpoints aggregated by geometry have unequal regulated source derivatives, invalidating source-equivalence compression.
- A positive-D endpoint class violates the root-quartic remainder cap epsilon_c<1, leaving kappa_c sign-indeterminate and forcing quarantine.
- The reflected Wilson collar algebra fails to preserve the same gauge-invariant observable normalization through endpoint collapse.

## Learning

Cycle 341 makes the screened quarantine sharper and one-sided. The conceptual pressure is endpoint collapse inside the same Wilson theory. The declarative tension is collar OS positivity plus fixed Wilson observables plus singular endpoint OPE without a boundary theory. Raw R is too weak, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. The efficient representation C_ep encodes source classes, seven source values or root-quartic caps, cumulant intervals, aggregated signed D_c, C_N, M_G, and T_tail; preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; uses source differentiation, interval arithmetic, aggregation-before-clipping, color multiplication, and tail addition; identifies equivalence only by regulated source data; transfers only I_gate. Conceptual value signal: sharp finite route change. Negative SU(N) endpoint cumulants are explanatory but not the obstruction; positive-D leakage times a connected cumulant witness plus uniform tail is.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a targeted falsifier probe while the branch remains quarantined for missing endpoint source intervals.`
- Rationale: The branch has already reduced the obstruction to a finite endpoint scalar. Another abstract OS restatement is low value; the next valid learning comes from varying one endpoint-overlap parameter and observing whether the one-sided C_ep screen promotes, falsifies, or stays quarantined.
- Situation seed: SU(3) heat-kernel plaquette-sheet endpoint box for the fixed three reflected Wilson hairpins, with a single source-equivalence class carrying a connected cumulant witness kappa_c and fractional incidences b12,b13,b23.
- Varied variable: the half-overlap ratio theta=(b13+b23)/b12, so D_c=b12(2-4theta) crosses from dangerous 12-dominance to protected half-overlap.
- Held-fixed controls: same heat-kernel plaquette-sheet regulator and same Wilson collar normalization, same H,K Schur-Feshbach block and null vector used before endpoint collapse, same gauge-invariant Wilson observable algebra with no boundary counterterm, fixed color prefactor C_N and fixed Gaussian margin M_G, cutoff-uniform tail budget tau required before promotion
- Expected observation: For theta>=1/2 the source class is protected by D_c<=0 even with negative kappa_c; for theta<1/2 the lower bound decreases linearly in b12(2-4theta) and can become a finite falsifier if the connected cumulant witness is sufficiently negative.
- Transfer certificate needed: Certified seven-point source intervals or root-quartic remainder bounds for kappa_c, source-equivalence verification, and a cutoff-uniform T_tail estimate before the observation may affect proof obligations.

## Next Experiment

Proof-search plus validator-facing endpoint source computation: instantiate one SU(3) positive-D source class, compute the seven-point connected cumulant witness interval with a cutoff-uniform M_8 or root-quartic remainder bound, aggregate D_c before clipping, add T_tail, and decide promote/falsify/quarantine for the finite post-H,K gate.

# Gauge-Invariant Nontriviality Witness Selection -> finite endpoint Wilson cumulant certificate

## Candidate Lemma

Conditional finite annular Ward-Hessian theorem for the post-H,K endpoint term. For fixed H,K plus-channel hairpin sheets in one endpoint box, certified sector Hessian constants with annular exponents nu_s>2 give a lower interval for the same-theory connected Wilson cumulant R_{++}^{ren}. If Delta_R^->0, this supplies the finite Schur-Feshbach endpoint mediator; if a stable upper interval stays nonpositive, the R repair is quarantined.

## Definitions

- source object: centered flowed Wilson hairpin cumulant R_{++}^{ren}(I,t) for two H,K plus-channel endpoint sheets in a finite endpoint box I.
- target object: finite endpoint-box positivity margin Delta_R^-(I) for the Schur-Feshbach post-H,K plus channel, not a continuum mass-gap claim.
- controlled interface: endpoint sheet-current representation with Ward/cusp subtraction, plus-channel moment cancellation, dyadic annular Hessian bounds, and outward-rounded interval arithmetic.
- same-theory condition: raw hairpins, flowed fields, counterterms, recovery maps, cumulants, and leakage L_+ are evaluated in the same cutoff Yang-Mills measure and same renormalization convention.

## Assumptions

- Model: four-dimensional SU(N) Euclidean Yang-Mills with Wilson plaquette cutoff a, gradient flow time t>0, and fixed finite H,K endpoint geometry.
- Regime: endpoint cell radius eta is smaller than the H,K separation scale d0, and annuli begin outside the near cell where Taylor Hessian bounds are valid.
- Cutoff: constants G_{++}^{I,-}, C_s^{near,+}, C_{s,0}^{+}, E_rec^{I,+}, and E_6^{I,+} are certified uniformly for 0<a<=a0 at fixed t and geometry.
- Same-theory: the centered flowed Wilson cumulant is recovered from the raw Wilson hairpins without changing gauge group, action, observable algebra, or normalization.
- Validity: one-hairpin perimeter and cusp counterterms cancel before taking the connected cumulant, and the plus endpoint current has zero monopole and dipole moments.
- Local: the claim changes only finite endpoint-box positivity after H,K; Clay existence, OS/Wightman reconstruction, observable density, topology control, and Hamiltonian mass gap remain untouched.

## Equations

- same-theory endpoint cumulant: `R_{++}^{ren}(I,t)=\kappa_2\big(\widehat W_{H,+}^{ren}(I,t),\widehat W_{K,+}^{ren}(I,t)\big)`. Valid when: Valid when the two renormalized centered hairpin observables are constructed with the same cutoff measure, the same gradient-flow time, and identical perimeter/cusp subtraction rules.
- flowed cumulant decomposition: `R_{++}^{ren}=2g_t^4(N^2-1)G_{++}+g_t^4N(N^2-1)\Xi_{++}^{C4}+E_{6}+E_{rec}`. Valid when: Applies after flowed small-hairpin expansion in the fixed endpoint box, with the connected four-curvature sector separated from the explicit two-pair contraction.
- annular C4 compression: `H_{4,ann}^{I,+}=\sum_s\left(C_s^{near,+}+\frac{C_{s,0}^{+}r_0^{-2\nu_s}}{1-q_s}\right),\qquad q_s=2^{4-2\nu_s}<1`. Valid when: Requires Ward/cusp subtraction and plus-channel monopole-dipole cancellation so that each far annulus is controlled by a mixed Hessian majorant.
- certified lower interval: `R_{++}^{I,-}=g_t^4(N^2-1)\left(2G_{++}^{I,-}-N M_{2,+}^2H_{4,ann}^{I,+}\right)-E_{rec}^{I,+}-E_6^{I,+}`. Valid when: Valid when interval lower bounds for the pair baseline and interval upper bounds for all connected C4, recovery, and higher-order remainders are outward rounded.
- finite promotion margin: `\Delta_R^{-}(I)=R_{++}^{I,-}-L_+^{I},\qquad \Delta_R^{-}(I)>0`. Valid when: Applies only after the finite Schur-Feshbach leakage L_+ is computed for the same H,K endpoint box and the same plus-channel normalization.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: centered flowed Wilson hairpin cumulant R_{++}^{ren}(I,t) for two H,K plus-channel endpoint sheets in a finite endpoint box I.; target object: finite endpoint-box positivity margin Delta_R^-(I) for the Schur-Feshbach post-H,K plus channel, not a continuum mass-gap claim.; Model: four-dimensional SU(N) Euclidean Yang-Mills with Wilson plaquette cutoff a, gradient flow time t>0, and fixed finite H,K endpoint geometry..
- Freeze the Clay claim level: this cycle targets only finite endpoint-box positivity after H,K, not YM existence, OS/Wightman axioms, nontrivial continuum limit, or mass gap.
- Represent each H,K plus hairpin by a centered flowed Wilson observable and then by endpoint sheet currents through Pi_{end,t}.
- Expand the connected cumulant through the flowed small-hairpin OPE: the two-pair contraction gives the explicit positive baseline 2g_t^4(N^2-1)G_{++}.
- Use disconnected-product removal plus one-hairpin perimeter/cusp subtraction before estimating the connected four-curvature sector.
- Apply Ward identities and plus-channel endpoint moment cancellation so the far C4 kernels have no monopole or dipole contribution.
- Taylor expand each far annular kernel to second order; bound the remainder by mixed Hessian constants C_{s,0}^{+}r^{-2nu_s}.
- Sum four-dimensional dyadic annuli, giving q_s=2^{4-2nu_s}; convergence requires nu_s>2.
- Add near-cell sector constants, recovery error, and higher-order flowed remainder, obtaining R_{++}^{I,-}.
- Compare R_{++}^{I,-} to the finite Schur-Feshbach leakage L_+ to form Delta_R^-.

Blocking gap: The missing proof object is a certified table of actual Yang-Mills sector Hessian constants C_s^{near,+}, C_{s,0}^{+}, nu_s and a cutoff-uniform recovery error for the Wilson plaquette plus gradient-flow regulator.

## Falsifiers

- falsifier: a C4 sector has certified nu_s<=2, making the annular tail nonsummable.
- falsifier: Ward or cusp subtraction leaves a local endpoint term with the wrong sign or cutoff growth.
- falsifier: the plus-channel endpoint current has a nonzero dipole moment after orientation bookkeeping.
- falsifier: E_rec^{I,+} grows as a decreases, showing the endpoint-current carrier is not same-theory stable.
- falsifier: a valid outward-rounded computation gives Delta_R^-(I)<=0 and Delta_R^+(I)<=0 on a refinement plateau.
- falsifier: the positive pair baseline G_{++}^{I,-} vanishes for the actual H,K geometry.

## Learning

Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, while positive pair covariance, flow renormalization, and raw-hairpin recovery can each be valid yet connected C4 can erase R_{++}. Declarative tension: endpoint positivity, same-theory flowed cumulants, and recovery maps must jointly hold; the missing mediator is a cutoff-stable annular Ward-Hessian dominance margin. Carrier critique: raw Wilson contours are fragmented and representation-limited; global OS spectral transfer, area-law intuition, and broad same-theory nontriviality witness selection are too coarse for this finite obstruction. Better abstraction: endpoint sheet currents encode H,K sheets, endpoint moments, sector kernels, counterterms, recovery errors, and L_+; preserve gauge, color, reflection, orientation, cutoff, locality, and same-theory invariants; use cumulant expansion, Ward/cusp subtraction, Taylor Hessians, dyadic tail compression, outward-rounded interval algebra, and certified zero-pairing equivalence; keep finite endpoint locality; transfer only through centered flowed cumulants; demote on any falsifier. Hard gate: finite endpoint-box positivity after H,K. Success promotes one finite Route A gate; failure quarantines this endpoint repair. Conceptual value signal: R_{++}/kappa_4 is now a valid annular dominance certificate with a promotion/quarantine test, not a symbolic boundary-OPE term. Reporting skill: timeline-definition-assumption-elicitor.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and proof-search calibration.`
- Rationale: The branch is no longer helped by restating the Wilson/OS obstruction. The missing mediator is quantitative: whether the connected C4 annular tail can be bounded below the positive pair baseline in the same Wilson theory.
- Situation seed: SU(2) Wilson plaquette Yang-Mills at cutoff a with gradient-flow time t, two fixed reflected H,K plus-channel thin hairpins in one endpoint box, represented by endpoint sheet currents after Ward/cusp subtraction.
- Varied variable: alpha=sqrt(8t)/eta, the ratio of flow radius to endpoint-cell size.
- Held-fixed controls: Gauge group SU(2), Wilson plaquette action, and the same centered flowed Wilson cumulant R_{++}^{ren}., Fixed H,K endpoint geometry, reflection orientation, plus-channel normalization, and Schur-Feshbach leakage L_+., Same recovery map Pi_{end,t}, same zero-pairing equivalence policy, and outward-rounded interval arithmetic.
- Expected observation: As alpha enters a plateau window, G_{++}^{I,-} should stabilize while C4 Hessian constants and E_rec either remain dominated or reveal a sign/size failure. A positive stable Delta_R^- promotes the finite endpoint gate; a negative stable margin is a decisive falsifier for this R repair.
- Transfer certificate needed: A cutoff-uniform table of sector Hessian bounds, recovery errors, and annular exponents for the Wilson plaquette plus gradient-flow regulator, certified in the same-theory observable algebra before any intuition affects proof obligations.

## Next Experiment

Proof search: compute the first validator-facing annular sector-constant table for SU(2) Wilson plaquette gradient-flow regulator at fixed H,K geometry, including G_{++}^{I,-}, C_s^{near,+}, C_{s,0}^{+}, nu_s, E_rec, E_6, and L_+. Record it as a finite connected cumulant witness and same-theory nontriviality witness boundary only if the same-theory recovery map is certified; otherwise route to quarantine.

# Raw signed-orbit K4 stress witness for finite endpoint PSD

## Candidate Lemma

For a heat-kernel SU(N) finite endpoint box, certified same-regulator raw K4 signed-orbit intervals giving D_p^+<0 or L_pq(theta)^2>D_p^+D_q^+ are a valid falsifier of post-H,K endpoint PSD. Survival proves nothing beyond forcing full Delta_raw search.

## Definitions

- source object: heat-kernel regulated SU(N) lattice Wilson endpoint box with raw connected four-curvature plaquette cumulants.
- target object: Schur-corrected finite endpoint quadratic form U_sigma on the post-H,K endpoint basis.
- controlled interface: signed-orbit recovery map from raw K4 plaquette intervals to diagonal upper and phased off-diagonal lower bounds.
- same-theory condition: all Wilson contractions, OPE errors, coupling, regulator, endpoint basis, and H,K Schur blocks use the same cutoff ensemble.
- carrier: connected cumulant witness R_sigma=cum_2(Q_i,Q_j) with vacuum/perimeter disconnected parts removed.
- hard gate: D_p^+<0 or L_pq(theta)^2>D_p^+D_q^+ kills only finite Route A endpoint PSD.

## Assumptions

- Model: finite 4D hypercubic cutoff, compact SU(N), heat-kernel plaquette regulator, fixed endpoint Wilson basis.
- Cutoff: sigma/a, volume, coupling, H,K Schur data, and OPE truncation are held fixed; no continuum uniformity is claimed.
- Same-theory: raw K4 intervals, Gaussian covariance C_sigma, OPE error, and S_HK are computed in the identical regulated measure.
- Validity: signed orbit quotienting uses only exact Wilson trace identities, orientation symmetries, Hermiticity, and gauge invariance.
- Local: this changes finite endpoint-box positivity only; OS reconstruction, observable density, nontriviality, and mass gap remain untouched.

## Equations

- post_HK_endpoint_form: `U_\sigma=\Pi_E\{\alpha_N g_\sigma^4(C_\sigma\circ C_\sigma)+g_\sigma^4K_{4,\sigma}/(16N^2)+E_{\mathrm{OPE},\sigma}\}\Pi_E-S_{HK,\sigma}`. Valid when: Valid when the heat-kernel Wilson expansion, endpoint compression, OPE interval, and Schur block use one finite cutoff ensemble.
- signed_orbit_recovery: `I_{pq}^{K4}(\theta)=\sum_{o\in\mathcal O_{pq}}m_o\operatorname{Re}(e^{-i\theta}w_o\kappa_4(o))\in[I^-_{pq}(\theta),I^+_{pq}(\theta)]`. Valid when: Applies after exact Wilson quotienting preserves phases, orientations, transporters, color tensors, and Hermitian endpoint labels.
- two_sparse_stress_gate: `D_p^+<0\ \mathrm{or}\ L_{pq}(\theta)^2>D_p^+D_q^+\quad\Longrightarrow\quad U_\sigma\not\succeq0`. Valid when: Requires certified diagonal upper bounds and a certified phased off-diagonal lower bound for the same U_sigma matrix.

## Attempted Derivation

- Use heat-kernel Wilson OPE; disconnected vacuum/perimeter terms cancel in cum_2(Q_i,Q_j), leaving the Gaussian color square plus connected K4 and OPE error.
- Compress the cumulant to the post-H,K endpoint basis and subtract S_HK, producing the finite Hermitian matrix U_sigma.
- Recover D_p^+,D_q^+ and L_pq(theta) from exact signed plaquette orbits, retaining phases rather than A012 sign-losing shells.
- Apply the 2x2 Hermitian PSD condition; a negative diagonal or determinant witness gives x_stress^*U_sigma x_stress<0.

Blocking gap: The branch still lacks validator-facing numerical raw K4 signed-orbit intervals for the first endpoint pair in the heat-kernel regulator.

## Falsifiers

- falsifier: signed-orbit quotienting changes a Wilson phase or color tensor, so the interval is not invariant.
- falsifier: OPE overflow makes L_pq(theta)^2<=D_p^+D_q^+ for every certified phase sector.
- falsifier: raw K4 intervals come from a different regulator or coupling than the H,K Schur block.
- falsifier: D_p^+,D_q^+ are too loose, so tau stress is inconclusive and the branch must use full Delta_raw.

## Learning

Conceptual pressure attacked: raw non-Gaussian Wilson K4 must mediate to finite endpoint PSD without OS-density circularity. Value signal: signed orbits preserve phases lost by A012 shells and give a sharp finite falsifier gate while all Clay frontier gates remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch is looping unless a concrete connected cumulant witness is tested; varying only the stress phase probes whether signed raw K4 orbits can actually demote endpoint PSD.
- Situation seed: Finite SU(2) heat-kernel endpoint box with two collar Wilson sheets and the first off-diagonal post-H,K endpoint pair p,q.
- Varied variable: phase angle theta in x_stress=e_p+e^{i theta}e_q.
- Held-fixed controls: same heat-kernel cutoff sigma/a, volume, coupling, Wilson endpoint basis, and H,K Schur block, same raw plaquette orbit list, color tensors, OPE interval budget, and exact Wilson quotient policy
- Expected observation: A narrow theta window may make L_pq(theta)^2>D_p^+D_q^+, giving a finite falsifier; otherwise the signed-orbit tactic is demoted.
- Transfer certificate needed: Certified interval arithmetic for raw K4 signed orbits, invariant quotient audit, and recovery of D^+,L into the same U_sigma matrix.

## Next Experiment

Proof search: compute the first same-regulator raw signed-orbit K4 interval table for endpoint pair p,q, run theta-grid interval certification, and demote or promote only through tau, Delta_raw, or x_stress.

