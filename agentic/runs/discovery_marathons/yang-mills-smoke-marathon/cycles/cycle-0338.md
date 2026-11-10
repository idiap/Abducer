# cycle-0338

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint source-interval gate for the post-H,K Wilson R term

## Candidate Lemma

Finite endpoint source-interval gate: for the fixed three-hairpin reflected Wilson block, the post-H,K null-channel scalar is decided by a same-theory connected cumulant witness interval. If the interval lower end is nonnegative the finite block passes this OS transfer gate; if the upper end is negative it is a finite same-theory falsifier; otherwise the branch remains quarantined pending endpoint data.

## Definitions

- source object: finite SU(N) heat-kernel plaquette-sheet endpoint source carrier C_ep for the fixed reflected Wilson three-hairpin block, including source classes, seven source values, kappa intervals, signed incidences, C_N, M_G, and T_tail.
- target object: the finite post-H,K Schur-Feshbach OS scalar I_gate controlling the null channel of that same reflected Wilson block.
- controlled interface: aggregate-before-clipping interval map from endpoint connected fourth source cumulants and signed incidences to I_gate.
- same-theory condition: all source derivatives are computed with the locked heat-kernel Wilson observables, unchanged reflection map, no boundary counterterm, and cutoff-uniform tail bounds.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action and gauge-invariant Wilson plaquette-sheet sources near reflected endpoints.
- Regime: fixed finite three-hairpin block after the previously computed H,K Schur-Feshbach reduction; this is not a continuum or mass-gap claim.
- Cutoff: endpoint source derivatives and T_tail are bounded uniformly in lattice spacing for the chosen finite block and collar geometry.
- Same-theory: Wilson normalization, reflection map, source algebra, and endpoint limiting procedure are identical before and after the collar collapse.
- Validity: connected log source derivatives define the endpoint fourth cumulant; Wick-square pieces are removed by connectedness and straight f f contacts cancel by the null-incidence identity.

## Equations

- signed endpoint leakage: `D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}`. Valid when: Valid when b_{ij,c} are fractional endpoint incidences for the fixed three-hairpin null channel after H,K normalization.
- seven-point connected cumulant interval: `\kappa_c\in \Delta_h^{(4)}\log Z_c(0)+[-7h^4M_{8,c}/240,\,7h^4M_{8,c}/240]`. Valid when: Valid when log Z_c is eight times source differentiable on the heat-kernel endpoint box and the stencil remains inside one source class.
- aggregate-before-clipping gate interval: `I_{\mathrm{gate}}\in M_G+C_N\sum_{\alpha}\bar D_{\alpha}[\kappa_{\alpha}]+T_{\mathrm{tail}},\qquad \bar D_{\alpha}=\sum_{c\in\alpha}D_c`. Valid when: Valid when source-equivalent endpoint boxes are aggregated before interval multiplication and all nonendpoint OPE leftovers are charged to T_tail.
- finite decision rule: `\inf I_{\mathrm{gate}}\ge0\Rightarrow Q_{\mathrm{post\mbox{-}HK}}\ge0,\qquad \sup I_{\mathrm{gate}}<0\Rightarrow \exists u:\ u^*Q_{\mathrm{post\mbox{-}HK}}u<0`. Valid when: Valid when the finite Schur-Feshbach reduction has already removed the rank-one OS direction and the PHP null channel is fixed.

## Attempted Derivation

- Fix the three-hairpin reflected Wilson block and take the already reduced post-H,K null channel; denote its positive Gaussian margin by M_G.
- Represent the endpoint part of the connected boundary-OPE polarization by heat-kernel plaquette-sheet sources L_c and source partition functions Z_c.
- Use connected log derivatives so Wick-square contractions do not enter kappa_c; use the null-incidence identity to remove straight nonabelian f f contact terms.
- Assign each endpoint source class a signed leakage D_c=2b12,c-4b13,c-4b23,c and color factor C_N from the singlet Wilson contraction.
- Aggregate source-equivalent boxes by equal seven source values, then multiply the aggregated signed incidence by the common connected cumulant interval.
- Add the uniform endpoint/corner tail T_tail to obtain I_gate, whose sign decides the finite Schur-Feshbach OS scalar.

Blocking gap: No certified endpoint source intervals or cutoff-uniform T_tail have yet been supplied for a positive-D leakage class. The root-quartic screen bounds the danger but does not compute the connected cumulant witness in the actual regulator data.

## Falsifiers

- Finite same-theory falsifier: a positive-D source class with a certified negative connected cumulant interval and tail such that sup I_gate<0.
- Nonuniform-tail falsifier: T_tail grows with cutoff or collar collapse and forces a boundary counterterm.
- Carrier falsifier: geometric endpoint aggregation identifies boxes with unequal regulated source stencils and breaks valid null-channel cancellation.
- Same-theory falsifier: the endpoint stencil requires a new boundary Wilson renormalization not present in the locked observable algebra.
- Analytic-screen falsifier: the eighth-derivative or root-quartic remainder bound fails in the heat-kernel endpoint chart.

## Learning

Conceptual pressure attacked: endpoint collapse must be sign-certified inside the same Wilson theory after H,K. Declarative tension: finite collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist without adding a boundary theory, but H,K, half-overlap shielding, and root-quartic negativity do not decide the scalar. Carrier audit: raw R is too weak, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. Efficient representation: C_ep encodes endpoint source classes, seven source values, cumulant intervals, signed incidences, C_N, M_G, and T_tail; preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; uses source differentiation, interval arithmetic, aggregation before clipping, color multiplication, and tail addition; identifies equivalence only by regulated source data; exports only I_gate. Conceptual value signal: sharp finite route change. Negative SU(N) endpoint cumulants are explanatory but not the obstruction; positive-D leakage times a connected cumulant witness plus uniform tail is.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while the branch remains quarantined from promotion.`
- Rationale: The branch has been looping on endpoint-carrier language; a concrete heat-kernel endpoint source experiment tests the finite post-H,K gate without restating the OS obstruction ladder.
- Situation seed: Fixed SU(N) heat-kernel plaquette-sheet regulator for the three reflected Wilson hairpins after H,K, with null vector in the Feshbach channel and endpoint source classes evaluated by a seven-point log Z stencil.
- Varied variable: The fractional leakage ratio r=(b13+b23)/b12 for a single source-equivalent endpoint class, varied through the half-overlap threshold while keeping the cumulant stencil fixed.
- Held-fixed controls: Same heat-kernel plaquette action and same locked gauge-invariant Wilson observables., Same reflection map, Wilson normalization, color factor C_N, and finite three-hairpin H,K block., Same source step h, endpoint chart, M_G margin, and tail-budget definition T_tail.
- Expected observation: For r>=1/2 the signed leakage D is nonpositive and negative endpoint cumulants are protective or neutral; for r<1/2 positive-D leakage can demote the finite OS scalar only if the connected cumulant witness and tail overcome M_G.
- Transfer certificate needed: A certified equality class of seven regulated source values, cutoff-uniform M8 and T_tail bounds, and a same-theory statement that no boundary counterterm or observable-algebra change was used.

## Next Experiment

Run proof search and endpoint-source computation: build the C_ep table for the actual heat-kernel plaquette-sheet three-hairpin endpoints, evaluate seven log Z source values per source class, certify kappa intervals and T_tail, then return the single interval I_gate for promotion, falsifier, or continued quarantine.

# Annular Plateau Certificate for the Flowed Wilson Endpoint R++

## Candidate Lemma

If the Ward-subtracted connected four-curvature sector kernels have a cutoff-stable annular Hessian plateau with exponent nu_s>2, then the post-H,K endpoint mediator R_{++}^{ren} has an explicit lower interval. A positive margin Delta_R^- proves the finite endpoint-box positivity gate; a nonpositive margin is a falsifier for this R-repair, not for Yang-Mills mass gap.

## Definitions

- source object: finite-volume lattice SU(N) Yang-Mills with Wilson action, spacing a, gradient flow time t>0, centered renormalized H,K hairpin Wilson variables, and endpoint sheet current J_+ in a fixed endpoint box.
- target object: the finite Schur-Feshbach plus-channel endpoint-box positivity margin Delta_R^- = R_{++}^{ren,-}-L_+ for the already isolated H,K block.
- controlled interface: recovery map Rec_{a,t} from raw thin Wilson hairpins to flowed endpoint sheet currents, preserving gauge, color, reflection, orientation, locality, and recording epsilon_rec.
- same-theory condition: pair covariance, connected C4 polarization, counterterms, recovery errors, and leakage L_+ are computed inside the same cutoff family before any continuum or OS spectral-transfer claim.
- Carrier: endpoint sheet currents replace raw Wilson contours; raw contours are fragmented for Ward moment cancellation, while endpoint currents expose monopole/dipole zero modes and annular Hessian primitives.
- Declarative tension: finite Schur-Feshbach positivity, positive flowed pair covariance, and same-theory recovery must jointly be valid, but connected C4 can erase the mediator unless the annular plateau constants are certified.
- Efficient representation requirements: encode H,K sheets, endpoint currents, cell moments, sector kernels, counterterms, recovery errors, and L_+; preserve gauge/color/reflection/orientation/cutoff/locality/same-theory invariants; use cumulant expansion, Ward/cusp subtraction, Taylor Hessian remainders, dyadic tail compression, outward-rounded interval algebra, and zero-pairing quotienting; keep finite endpoint cells plus summable annuli; transfer only through centered flowed Wilson cumulants.

## Assumptions

- Model: four-dimensional lattice SU(N) Yang-Mills in finite volume with Wilson plaquette action and gradient-flow regularized Wilson observables.
- Regime: endpoint boxes are separated from non-endpoint sheet pieces by rho_0>c sqrt(t), and endpoint cell diameter eta is small compared with rho_0.
- Cutoff: constants are required uniformly for a<=a_0 at fixed physical t, eta, rho_0, and volume collar; otherwise the result is only finite-cutoff evidence.
- Same-theory: the raw hairpin variables, flowed recovery variables, connected cumulants, and Schur-Feshbach leakage L_+ belong to the same regulated Yang-Mills measure.
- Validity: Ward/cusp subtraction removes contact, perimeter, and disconnected product terms before Taylor expansion of the connected C4 kernels.
- Local: plus-channel endpoint current has zero monopole and dipole moments after reflection pairing, so the first surviving far-field term is Hessian-controlled.
- Constraint: for every connected sector s, the annular decay exponent satisfies nu_s>2 and the outward-rounded plateau constant C_s^{plat,+} is finite.
- Non-claim: the lemma proves only a finite Route A endpoint-box certificate; it does not construct continuum Schwinger functions, OS positivity, observable density, or a Hamiltonian mass gap.

## Equations

- flowed R decomposition: `R_{++}^{ren}=P_{++}+C_{4,++}^{WS}+E_{\ge 6}+E_{rec}`. Valid when: Valid when centered flowed Wilson hairpins are expanded after disconnected-product, perimeter, cusp, and endpoint recovery subtractions in the same cutoff Yang-Mills measure.
- positive pair baseline: `P_{++}=g_t^4\,2(N^2-1)\,G_{++}^{(t)},\qquad G_{++}^{(t)}\ge G_{++}^{-}>0`. Valid when: Valid when the two-curvature cross-pairing kernel is evaluated between the fixed plus endpoint sheet currents with the same gradient-flow time t.
- Ward-Hessian C4 majorant: `|C_{4,++}^{WS}|\le g_t^4\,N(N^2-1)\,M_{2,+}^2\left(H_{near}^{+}+\sum_s H_{s,far}^{+}\right)`. Valid when: Applies after Ward subtraction and plus-channel moment cancellation make constant and linear endpoint Taylor terms vanish on every certified cell.
- dyadic annular tail compression: `H_{s,far}^{+}(J_0)\le C_s^{plat,+}\,{2^{(4-2\nu_s)J_0}\over 1-2^{4-2\nu_s}},\qquad \nu_s>2`. Valid when: Valid when annular Hessian suprema for sector s obey the plateau bound on all dyadic annuli beyond J0 with outward-rounded constants.
- dominance margin: `\Delta_R^-:=g_t^4\left[2(N^2-1)G_{++}^{-}-N(N^2-1)M_{2,+}^2\left(H_{near}^{+}+\sum_s H_{s,far}^{+}\right)\right]-E_{\ge6}^{+}-\epsilon_{rec}^{+}-L_+`. Valid when: Valid when pair, C4, higher-cumulant, recovery, and leakage intervals are all computed for the same H,K endpoint geometry and cutoff family.

## Attempted Derivation

- Freeze the Clay claim level: only a finite H,K endpoint-box positivity certificate is pursued; continuum construction, OS/Wightman axioms, nontrivial continuum limit, gauge-invariant observable density, and Hamiltonian mass gap are untouched.
- Start with the centered flowed Wilson connected cumulant R_{++}^{ren}=kappa_2(tilde W_+,tilde W_+) for the fixed H,K plus endpoint current.
- Use disconnected-product subtraction and one-hairpin perimeter/cusp counterterms to isolate the pair term P_{++} and the Ward-subtracted connected four-curvature polarization C_{4,++}^{WS}.
- Evaluate the pair color contraction: two cross-pairings give the positive factor 2(N^2-1) multiplying the same-theory geometric kernel G_{++}^{(t)}.
- Decompose C_{4,++}^{WS} into sector kernels s in the three-gluon, four-gluon, counterterm, and endpoint-contact families, with overall color majorant N(N^2-1).
- Use Ward identities and reflection-plus current symmetry to cancel endpoint monopole and dipole terms; the Taylor remainder begins with mixed Hessians weighted by M_{2,+}^2.
- Split the far region into dyadic annuli. If Hessian annular suprema scale as 2^{-2nu_s J} while annular volume contributes 2^{4J}, the tail ratio is q_s=2^{4-2nu_s}.
- Compress the tail for nu_s>2 and assemble the lower interval Delta_R^- by subtracting C4, higher-cumulant, recovery, and Schur-Feshbach leakage upper intervals from the pair lower interval.

Blocking gap: The actual H,K endpoint geometry still lacks certified outward-rounded values for G_{++}^-, H_{near}^+, C_s^{plat,+}, E_{>=6}^+, epsilon_rec^+, and cutoff-stable plateau exponents nu_s.

## Falsifiers

- falsifier: a Ward-subtracted sector retains a contact or cusp delta term, invalidating the Hessian remainder bound.
- falsifier: some annular exponent has nu_s<=2, so q_s=2^{4-2nu_s} is not summable.
- falsifier: outward-rounded plateau constants grow with cutoff refinement and destroy cutoff-uniform dominance.
- falsifier: the recovery map from raw thin hairpins to flowed endpoint currents has epsilon_rec larger than the pair margin.
- falsifier: certified G_{++}^- is zero because the plus endpoint geometry has accidental cancellation.
- falsifier: Delta_R^-<=0 after including L_+, near-zone constants, higher cumulants, and recovery errors.
- falsifier: zero-pairing quotient identifies currents with a nonzero pair or C4 cell moment.
- falsifier: the finite-volume collar or topology sector changes the same-theory cumulant being evaluated.

## Learning

Cycle 338 sharpens the R_{++}/kappa_4 task from an annular plateau idea to a conditional finite theorem with an explicit tail ratio q_s=2^{4-2nu_s}, a dominance margin Delta_R^-, and a quarantine criterion. The conceptual pressure is the missing same-theory mediator between finite Schur-Feshbach endpoint positivity and flowed Wilson cumulant positivity. The value signal is local and route-changing: the connected boundary-OPE polarization becomes a valid falsifiable color-geometric interval rather than a symbolic endpoint term, while every Clay target commitment remains unclaimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe and proof-search driver.`
- Rationale: The branch is past symbolic thresholds; it needs a target-preserving test of whether the connected boundary-OPE polarization is summably smaller than the positive pair covariance in the actual H,K endpoint geometry.
- Situation seed: Finite-volume SU(2) or SU(3) Wilson lattice Yang-Mills on a four-torus with fixed physical gradient-flow time t, fixed H,K hairpin endpoint boxes, centered flowed Wilson variables, and outward-rounded interval evaluation of Ward-subtracted C4 annular Hessian kernels.
- Varied variable: Dyadic annular start J0 for the far-zone compression, with the plateau exponent nu_s and constants audited as J0 increases.
- Held-fixed controls: Same Wilson action, gauge group N, volume collar, endpoint box geometry, and reflection-plus H,K current., Same gradient-flow time t, same raw-to-flowed recovery map Rec_{a,t}, and same Schur-Feshbach leakage L_+., Same Ward/cusp subtraction scheme, disconnected-product subtraction, and zero-pairing quotient policy., No OS spectral-transfer, area-law, or continuum mass-gap assumption is imported.
- Expected observation: If the route is viable, C_{s,J}^{plat} stabilizes and q_s<1 so the compressed far tail decays below the positive pair baseline, yielding Delta_R^->0 for some J0. If not, the plateau drift or non-summable q_s is an immediate demotion signal.
- Transfer certificate needed: A certified same-theory interval package: outward-rounded pair lower bound, sector Hessian upper bounds, Ward/cusp cancellation proof, recovery-error bound, higher-cumulant remainder bound, cutoff-uniform plateau audit, and a validation note that this is a connected cumulant witness only for the finite endpoint gate.

## Next Experiment

Proof search: build the outward-rounded annular plateau table for the actual H,K endpoint current, compute G_{++}^-, H_{near}^+, C_s^{plat,+}, epsilon_rec^+, and E_{>=6}^+, then evaluate Delta_R^-. Mark the artifact as a same-theory nontriviality witness boundary and connected cumulant witness only for the finite endpoint-box gate, not for continuum mass gap.

# Raw signed-orbit K4 stress gate for the post-H,K endpoint matrix

## Candidate Lemma

Finite signed-orbit stress falsifier: in one heat-kernel cutoff theory, recovered raw kappa4 orbit intervals give a valid two-sparse obstruction to post-H,K endpoint positivity. If some recovered diagonal upper bound satisfies D_i^+<0, or if for some i,j,theta the phased off-diagonal lower bound satisfies L_{ij}(theta)^2>D_i^+D_j^+, then the finite endpoint matrix U_sigma is not positive semidefinite. This falsifies only the worked H,K collar/hairpin endpoint route, not Yang-Mills existence or the mass gap.

## Definitions

- source object: finite heat-kernel regulated SU(N) lattice Yang-Mills endpoint box B_sigma with oriented plaquette variables F_p transported to a fixed endpoint basepoint and Wilson sheet weights w_i(p).
- target object: the finite Hermitian post-H,K endpoint matrix U_sigma=R_sigma-S_HK acting on the chosen endpoint Wilson basis.
- controlled interface: the recovery map Rec_sigma sending raw signed plaquette-orbit kappa4 intervals, Gaussian covariance C_sigma, OPE intervals, and Schur block S_HK to rigorous entry intervals for U_sigma.
- same-theory condition: all cumulants, covariance entries, OPE errors, and Schur blocks are computed for the identical cutoff, action, coupling, boundary normalization, reflection plane, and Wilson basis.
- connected cumulant witness: K_raw is the non-Gaussian fourth connected cumulant part of cum_2(:Phi_i^2:,:Phi_j^2:) after vacuum and perimeter subtraction.
- stress carrier: the two-dimensional span of endpoint basis vectors e_i,e_j with phase theta, not the OS Hilbert observable algebra or gauge-invariant observable density carrier.

## Assumptions

- Model: four-dimensional finite-volume hypercubic SU(N) lattice Yang-Mills with heat-kernel plaquette action and fixed reflection plane.
- Cutoff: lattice spacing a>0, smoothing scale sigma>=a, endpoint box diameter O(sigma), and finite Wilson sheet family P_i are fixed before interval recovery.
- Same-theory: Gaussian covariance, kappa4 intervals, OPE error bounds, and S_HK come from the same cutoff measure and the same Wilson normalization.
- Validity: Wilson logarithms and transported curvature insertions are used only inside the finite OPE collar where the stated OPE error interval is certified.
- Local: the claim is a finite Route A endpoint PSD obstruction and does not assert OS reconstruction, excitation-sector cyclicity, continuum Schwinger convergence, or a Hamiltonian mass gap.

## Equations

- transported-plaquette-flux: `F_p^a=\operatorname{Tr}\!\left(T^a U_{\gamma_p}(\log U_p)_\sigma U_{\gamma_p}^{-1}\right),\qquad \Phi_i^a=\sum_{p\in P_i}w_i(p)F_p^a`. Valid when: Valid when the heat-kernel logarithm is chosen inside the fixed endpoint collar and each plaquette is transported by the same Wilson path convention.
- raw-connected-kappa4-entry: `K^{\rm raw}_{ij}=\sum_{p,p'\in P_i}\sum_{q,q'\in P_j}w_i(p)w_i(p')\overline{w_j(q)w_j(q')}\,\kappa_4(F_p^a,F_{p'}^a,F_q^b,F_{q'}^b)`. Valid when: Applies after vacuum and perimeter cumulants are subtracted in the same finite heat-kernel lattice theory.
- post-HK-endpoint-entry: `U_{ij}=\alpha_N g_R^4 C^{(2)}_{ij}+\frac{g_R^4}{16N^2}K^{\rm raw}_{ij}+E^{\rm OPE}_{ij}-(S_{HK})_{ij},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Requires the same-regulator Wilson OPE decomposition and the Schur-Feshbach H,K block computed in the identical endpoint basis.
- phased-interval-recovery: `\operatorname{Re}(e^{-i\theta}U_{ij})\in I_{ij}(\theta),\qquad L_{ij}(\theta)=\inf_{x\in I_{ij}(\theta)}|x|,\qquad D_i^+=\sup I_{ii}(0)`. Valid when: Valid when signed orbit intervals are Hermitian, phase resolved, and combined with outward-rounded interval arithmetic.
- two-sparse-stress-falsifier: `D_i^+<0\quad {\rm or}\quad L_{ij}(\theta)^2>D_i^+D_j^+\ \Longrightarrow\ U_\sigma\not\succeq0`. Valid when: Applies to a finite Hermitian endpoint compression whose diagonal and phased off-diagonal intervals enclose the exact U_sigma entries.

## Attempted Derivation

- Attack conceptual pressure: R must be a same-theory connected cumulant witness mediating raw Wilson K4 data to Schur-corrected finite endpoint PSD, not scalar R, A012 shell aspiration, OS Hilbert observable algebra, or gauge-invariant observable density rhetoric.
- Fix the heat-kernel cutoff theory, endpoint box B_sigma, Wilson sheets P_i, transported plaquette fluxes F_p, and endpoint basis before any quotient or interval arithmetic.
- Use vacuum/perimeter cancellation to write the connected boundary-OPE polarization as a PSD Gaussian color square plus one raw connected kappa4 operator plus an OPE remainder.
- Subtract the already finite H,K Schur energy S_HK in the same endpoint basis, producing the Hermitian matrix U_sigma=R_sigma-S_HK.
- Recover phase-resolved entry intervals I_ij(theta) from signed raw plaquette orbits, preserving color tensors, transporter paths, endpoint labels, orientation phases, and Hermiticity.
- For a two-sparse stress vector x=e_i-t e^{i theta}e_j, PSD of U_sigma implies U_ii>=0, U_jj>=0, and |U_ij|^2<=U_ii U_jj.
- Thus D_i^+<0 or L_ij(theta)^2>D_i^+D_j^+ yields an explicit negative Rayleigh vector after optimizing t, hence a finite falsifier for endpoint PSD.
- Survival of all such tests is only evidence against this negative tactic; it forces full Delta_raw interval PSD search and does not touch continuum YM gates.

Blocking gap: No validator-facing raw signed-orbit kappa4 intervals I_O have yet been produced for the first H,K endpoint geometry, so the hard gate cannot be numerically or rigorously decided in this cycle.

## Falsifiers

- falsifier: a recovered same-regulator orbit interval gives D_i^+<0 for some endpoint i, producing a negative diagonal Rayleigh witness.
- falsifier: a phase theta and endpoint pair i,j satisfy L_ij(theta)^2>D_i^+D_j^+, producing a two-sparse negative determinant witness.
- Missing raw kappa4 intervals after signed-orbit recovery demote the abstraction and require quarantine rather than another restatement.
- A regulator mismatch between K4 intervals, OPE errors, and S_HK invalidates the same-theory transfer certificate.
- A quotient that loses orientation phase or color contraction makes L_ij(theta) invalid and kills the signed-orbit tactic.
- If OPE error intervals dominate so that every L_ij(theta)=0 and diagonals are wide positive, the negative tactic has no route-deciding force.

## Learning

Conceptual pressure attacked: the missing mediator from raw non-Gaussian Wilson K4 cumulants to a finite Schur-corrected endpoint PSD decision. Declarative tension: Wilson/OPE data, raw K4 intervals, OPE error, and S_HK must jointly hold in one cutoff theory, while OS reconstruction, continuum Schwinger coherence, gauge-invariant observable density, excitation-sector cyclicity, and mass gap transfer remain non-claims. Carrier critique: scalar R is too weak, OS Hilbert observable algebra is too strong and circular for this local gate, A012 shells are sign-losing, and full Delta_raw search is complete but expensive. Compared with those routes, signed raw orbits are the efficient representation because they encode oriented plaquettes, sheet weights, transporters, color tensors, cumulant intervals, OPE intervals, endpoint phases, and Schur blocks; preserve gauge invariance, reflection support, Hermiticity, Gaussian/K4 separation, same-theory normalization, and exact Wilson quotienting; support cumulant contraction, phase interval summation, Rayleigh stress search, Loewner bounds, and Schur subtraction; quotient only by exact identities; keep a finite endpoint-box complexity budget; transfer only through tau, Delta_raw, or x_stress; and expose falsifiers by negative margin, missing intervals, non-invariant quotienting, OPE overflow, or regulator mismatch. Conceptual value signal: sharp and route-changing at finite scope because Gaussian color positivity, non-Gaussian K4 danger, OPE error, and Schur hairpin energy are unified in one valid inequality that can kill only the finite H,K endpoint route while leaving every Clay frontier gate untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the first raw signed-orbit interval computation.`
- Rationale: The branch has exhausted abstraction-only phase-stress cycles; a concrete heat-kernel endpoint box can reveal whether a single non-Gaussian orbit can overpower Gaussian color positivity, OPE error, and H,K Schur energy.
- Situation seed: Finite SU(2) heat-kernel lattice Yang-Mills on a 4D endpoint box straddling the reflection plane, with the first H,K collar/hairpin Wilson sheets fixed and the connected cumulant witness restricted to the nearest signed plaquette-quadruple orbit crossing the endpoint boundary.
- Varied variable: The certified lower endpoint rho of Re(e^{-i theta} kappa_4) for the nearest signed orbit, with theta chosen to align the off-diagonal stress phase.
- Held-fixed controls: Same heat-kernel regulator, lattice spacing a, smoothing sigma, bare coupling, and finite volume for covariance, kappa4, OPE, and Schur data., The H,K endpoint Wilson basis, transporter convention, reflection plane, color normalization, and outward-rounded interval arithmetic., The Gaussian color factor alpha_N=(N^2-1)/(8N^2), OPE error budget, and S_HK block are not retuned while rho varies.
- Expected observation: There is an explicit threshold rho_* at which L_pq(theta)^2 crosses D_p^+D_q^+; crossing gives a finite falsifier, while non-crossing identifies whether the obstruction is genuinely small K4 or merely missing interval precision.
- Transfer certificate needed: A rigorous same-regulator raw cumulant interval for the chosen orbit, an exact signed-orbit quotient audit, and a verified recovery map Rec_sigma into U_sigma before the intuition may affect proof obligations.

## Next Experiment

Proof search: compute the first same-regulator raw signed-orbit K4 interval for the nearest H,K endpoint plaquette quadruple in the heat-kernel SU(2) box; recover D_p^+, D_q^+, and L_pq(theta) for the connected cumulant witness; record that OS Hilbert observable algebra, gauge-invariant observable density, excitation-sector cyclicity, and any vacuum-orthogonal spectral witness are non-claims unless a separate Clay-level frontier gate is discharged.

