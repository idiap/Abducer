# cycle-0351

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Finite post-H,K endpoint cumulant screen for reflected Wilson OS transfer

## Candidate Lemma

In the heat-kernel plaquette-sheet regulator, after source-equivalence aggregation the connected endpoint boundary-OPE polarization for the fixed post-H,K three-hairpin block is a one-sided interval product. Negative SU(N) endpoint fourth cumulants lower the finite OS gate only through positive aggregated D_c leakage plus a uniform tail.

## Definitions

- source object: heat-kernel regulated SU(N) plaquette-sheet endpoint classes c with source partition functions Z_{a,c}(s), fourth connected source cumulants kappa_c, fractional incidences b_{ij,c}, and tail budget T_tail.
- target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for the fixed three-hairpin block; it is a finite Route A gate and not the continuum Clay mass-gap target.
- controlled interface: C_ep, a source-equivalence endpoint carrier exporting only an interval [I_-,I_+] after aggregation-before-clipping, color multiplication, and tail addition.
- same-theory condition: the Wilson normalization, heat-kernel regulator, source derivatives, and gauge-invariant observable algebra are identical on collar and endpoint sides; no boundary counterterm or endpoint algebra enlargement is allowed.
- observable manipulated: the connected cumulant witness kappa_c=partial_s^4 log Z_{a,c}(0) contracted with the null-channel incidence D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}.
- declarative tension: collar reflection positivity, fixed gauge-invariant Wilson observables, and singular endpoint OPE must jointly hold without adding a boundary theory; raw R forgets incidence signs and raw kappa_4 spectra overstate danger.

## Assumptions

- Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflected Wilson hairpin plaquette sheets.
- Regime: fixed finite three-hairpin block after the H,K Schur-Feshbach reduction; no continuum or infinite-volume claim is made.
- Cutoff: endpoint boxes, source derivative bounds M_{8,c}, and T_tail are uniform over the finite cutoff/refinement range used for the block certificate.
- Same-theory: source-equivalence aggregation is allowed only for endpoint boxes with equal regulated source data Z_{a,c}(s), not merely similar geometry.
- Local: Wick-square Gram terms are retained as nonnegative or discarded only in lower bounds, and straight f f contacts cancel by the previously fixed null-incidence identity.
- Validity: the color prefactor C_N is positive and fixed by the same Wilson normalization, so interval signs are not changed by representation changes.

## Equations

- endpoint stencil interval: `\kappa_c\in D_h^{(4)}\log Z_{a,c}(0)+[-7h^4M_{8,c}/240,\,7h^4M_{8,c}/240]`. Valid when: Valid when log Z_{a,c}(s) has a uniform eighth source derivative bound on the seven-point stencil interval.
- aggregated null incidence: `D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}=2b_{12,c}\bigl(1-2\eta_c\bigr),\quad \eta_c=(b_{13,c}+b_{23,c})/b_{12,c}`. Valid when: Applies after source-equivalent endpoint boxes are aggregated before clipping and b_{12,c}>0 for the class.
- one-sided endpoint gate: `I_{\rm gate}\ge M_G+T_-+C_N\sum_c \kappa^-_c\,[D_c]^+`. Valid when: Requires certified nonpositive cumulant intervals kappa_c subset (-infty,0] and uses only lower-bound dangerous leakage.
- exact interval product gate: `I_{\rm gate}\in M_G+[T_-,T_+]+C_N\sum_c [\kappa^-_c,\kappa^+_c]\,[D^-_c,D^+_c]`. Valid when: Valid when cumulant and incidence intervals are independently certified for each source-equivalence class.
- root quartic screen: `\kappa_c=-(t_c^4/60)\,R_4(L_c)+E_c,\quad R_4(L)=N\operatorname{tr}(L^4)+3(\operatorname{tr}L^2)^2\ge0`. Valid when: Valid in small heat-kernel endpoint coordinates with Hermitian source L_c and controlled higher-order remainder E_c.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel regulated SU(N) plaquette-sheet endpoint classes c with source partition functions Z_{a,c}(s), fourth connected source cumulants kappa_c, fractional incidences b_{ij,c}, and tail budget T_tail.; target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for the fixed three-hairpin block; it is a finite Route A gate and not the continuum Clay mass-gap target.; Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflected Wilson hairpin plaquette sheets..
- Fix the post-H,K null channel and source-equivalence endpoint classes before any sign clipping.
- Write the connected endpoint polarization as C_N sum_c D_c kappa_c plus T_tail; Wick-square contractions are nonnegative Gram terms and straight f f contact terms cancel by null incidence.
- Use the heat-kernel endpoint coordinate expansion of the SU(N) Haar Jacobian to obtain the leading connected fourth cumulant kappa_c=-(t_c^4/60)R_4(L_c)+E_c with R_4(L_c)>=0.
- Since C_N>0, a certified nonpositive kappa_c can lower I_gate only when D_c>0; if D_c<=0 its leading contribution is protective or zero.
- Therefore aggregate source-equivalent boxes first, compute D_c, discard shielded classes only for lower-bound purposes, and send the exact interval product to the finite OS gate.

Blocking gap: The branch lacks actual endpoint source intervals for the positive-D classes and a cutoff-uniform T_tail bound; without them I_gate cannot be signed.

## Falsifiers

- A positive-D endpoint class has certified kappa_c<0 with C_N kappa_c D_c+T_tail<-M_G, producing a negative finite OS interval falsifier.
- The endpoint tail T_tail is not cutoff-uniform or contains a hidden boundary counterterm, invalidating same-theory transfer.
- Two endpoint boxes aggregated as source-equivalent have different regulated Z_{a,c}(s), so incidence cancellation used before clipping is invalid.
- The straight f f null-incidence cancellation fails at corners after the heat-kernel endpoint refinement.
- The reflected Wilson source algebra changes at the endpoint, making the carrier valid for a boundary-modified theory rather than the intended Yang-Mills theory.

## Learning

Cycle 351 adds a one-sided endpoint leakage theorem: after valid Wick-square positivity and straight f f cancellation, the post-H,K connected boundary-OPE term is dangerous only through positive aggregated D_c multiplied by a same-theory connected cumulant witness and a uniform tail. This is sharp finite Route A progress, but the proof state remains quarantined without endpoint source data.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while the branch remains quarantined pending endpoint source intervals.`
- Rationale: The branch is looping on promotion language unless the one-sided endpoint screen is tested on actual positive-D source classes. A concrete heat-kernel endpoint experiment can decide whether the finite post-H,K block is promoted, falsified, or remains quarantined.
- Situation seed: Fixed SU(N) heat-kernel plaquette-sheet regulator for the three reflected Wilson hairpin endpoints after the H,K Schur-Feshbach reduction; endpoint boxes are grouped by equal regulated source partition functions and tested as connected cumulant witness classes.
- Varied variable: The fractional leakage ratio eta_c=(b_{13,c}+b_{23,c})/b_{12,c}, crossing the shield threshold eta_c=1/2.
- Held-fixed controls: Same Wilson loop normalization and heat-kernel regulator on collar and endpoint sides., Fixed post-H,K null-channel weights 2,-4,-4 and fixed positive color prefactor C_N., No boundary counterterm, no endpoint algebra enlargement, and no change of gauge-invariant observables., Uniform seven-point source stencil error bound M_{8,c} and explicit T_tail accounting.
- Expected observation: For eta_c>=1/2 the leading negative root-quartic cumulant cannot lower the gate; for eta_c<1/2 the gate decreases linearly in (1-2eta_c) until source intervals or T_tail decide promotion versus falsifier.
- Transfer certificate needed: A validator-facing table of Z_{a,c}(mh) source values, kappa_c intervals, aggregated D_c intervals, C_N, M_G, and T_tail, with equality-of-source-data certificates for every aggregation.

## Next Experiment

Compute the positive-D endpoint source table for the heat-kernel SU(N) three-hairpin block: seven log Z_{a,c}(jh) values per source-equivalence class, kappa_c intervals, D_c, C_N, M_G, and T_tail; route result to proof search if I_->=0, to falsifier write-up if I_+<0, and to quarantine if intervals overlap zero.

# Gauge-Invariant Nontriviality Witness Selection: first-annulus R++ certificate

## Candidate Lemma

First-annulus Ward-Hessian certificate: if the flowed endpoint-current representation of the H,K plus hairpin has certified Ward/cusp and monopole/dipole cancellations, then the connected boundary-OPE polarization R_{++} admits a computable lower interval. A positive dominance margin promotes finite endpoint-box positivity after H,K; a nonpositive margin is a falsifier for this R repair only.

## Definitions

- source object: centered gradient-flow regularized SU(N) Wilson hairpin cumulant R_{++}^{ren}(t,a) in a fixed finite H,K endpoint box.
- target object: finite-dimensional Schur-Feshbach plus-channel endpoint positivity margin for the H,K collar/hairpin subspace.
- controlled interface: endpoint sheet-current recovery map from raw Wilson hairpins to centered flowed currents, with error E_rec and certified zero-pairing quotient.
- same-theory condition: same cutoff Yang-Mills measure, bare coupling trajectory, flow time rule, centering, and counterterm scheme are used on both sides.
- observable: W_+^{ren}(t,a) is the centered gauge-invariant Wilson hairpin observable represented by the plus endpoint current J_+.
- carrier: sector kernels K_s for s in {3g,4g,ct,end} encode the Ward-subtracted connected four-curvature polarization on endpoint cells.

## Assumptions

- Model: four-dimensional SU(N) Yang-Mills with Wilson lattice cutoff a, finite volume first, and gradient flow time t satisfying a^2 << t << rho_0^2.
- Regime: fixed finite H,K endpoint geometry, fixed physical endpoint distance rho_0, and endpoint box size eta smaller than the first annulus radius.
- Same-theory: the pair term, connected C4 sectors, recovery error, and Schur-Feshbach leakage L_+ are all computed from the same cutoff family before any continuum claim.
- Cutoff: constants H_{s,0}^+ and G_{++}^- are outward-rounded intervals uniform on the tested cutoff window, not imported continuum estimates.
- Local: this changes only the finite Route A endpoint-box gate after H,K; it does not claim OS reconstruction, nontrivial continuum limit, observable density, or Hamiltonian mass gap.

## Equations

- flowed connected Wilson cumulant: `R_{++}^{ren}(t,a)=\kappa_2(W_+^{ren},W_+^{ren})=g_t^4(N^2-1)\{2G_{++}+N C_{4,++}^{WS}\}+\mathcal E_6`. Valid when: Valid when the raw H,K Wilson hairpins are centered, flowed, and renormalized inside one cutoff Yang-Mills measure.
- Ward and plus-moment cancellation: `\int_E J_+(x)\,dx=0,\qquad \int_E (x-x_E)\otimes J_+(x)\,dx=0`. Valid when: Requires Ward subtraction, cusp counterterm cancellation, and the plus-channel endpoint-current normalization for the fixed H,K geometry.
- first-annulus Hessian constant: `H_{s,0}^{+}:=\sum_{Q\in\mathcal P_0}|Q|\,\sup_{(x,y)\in Q}\|D_xD_yK_s(x,y;t,a)\|_{op}`. Valid when: Applies after the first annulus A_0 is partitioned into certified endpoint cells with outward-rounded kernel bounds.
- first-annulus C4 majorant: `C_{4,++}^{WS}(A_0)\ge -M_{2,+}^2\sum_s H_{s,0}^{+}`. Valid when: Valid when constant and linear Taylor terms vanish by the stated Ward and plus-moment cancellations.
- annular compressed lower margin: `\Delta_R^-:=g_t^4(N^2-1)\left(2G_{++}^- -N M_{2,+}^2\sum_s\frac{H_{s,0}^{+}}{1-q_s}\right)-E_{rec}^+-L_+`. Valid when: Requires sector tail ratios q_s<1, same-theory recovery error control, and the finite Schur-Feshbach leakage L_+.
- finite gate promotion: `\Delta_R^->0\quad\Longrightarrow\quad Q_+^{endpoint}\ge \Delta_R^-`. Valid when: Valid only for the finite H,K plus-channel endpoint box with the certified interval inputs above.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: centered gradient-flow regularized SU(N) Wilson hairpin cumulant R_{++}^{ren}(t,a) in a fixed finite H,K endpoint box.; target object: finite-dimensional Schur-Feshbach plus-channel endpoint positivity margin for the H,K collar/hairpin subspace.; Model: four-dimensional SU(N) Yang-Mills with Wilson lattice cutoff a, finite volume first, and gradient flow time t satisfying a^2 << t << rho_0^2..
- Attack pressure: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator; positive pair covariance alone is compatible with connected C4 erasing R_{++}.
- Freeze the source as the centered flowed Wilson cumulant of two H,K plus hairpins and the target as the finite Schur-Feshbach endpoint margin Q_+, keeping both independently meaningful.
- Replace fragmented raw contours by endpoint sheet currents through Rec_t, but charge every non-identical replacement to E_rec^+ and guard zero-pairing equivalence.
- Expand kappa_2(W_+^{ren},W_+^{ren}) after disconnected-product subtraction and one-hairpin perimeter/cusp subtraction. The pair contraction contributes +2g_t^4(N^2-1)G_{++}.
- Decompose the connected four-curvature polarization into sectors 3g, 4g, counterterm, and endpoint. On the first annulus A_0, Taylor expand each Ward-subtracted sector kernel on cells Q in P_0.
- Use Ward/cusp and plus-channel monopole/dipole cancellation to remove constant and linear cell terms. Bound the remainder by mixed Hessian intervals H_{s,0}^+ times M_{2,+}^2.
- Compress outer annuli by sector ratios q_s<1 and add E_rec^+, epsilon_zp, and the known Schur-Feshbach leakage L_+ with adverse signs.
- Obtain Delta_R^-. If Delta_R^->0 uniformly on the cutoff plateau, the finite endpoint-box plus channel is positive; if not, the R repair is falsified or quarantined.

Blocking gap: The first-annulus outward-rounded quadrature H_{s,0}^+ has not yet been numerically enclosed for the actual H,K endpoint geometry and sector kernels.

## Falsifiers

- Ward or cusp subtraction leaves a nonzero monopole/dipole moment, making the Hessian reduction invalid.
- The first-annulus sector interval is too large and forces Delta_R^-<=0; this is the main dominance falsifier.
- A tail sector has q_s>=1 or an uncertified dyadic remainder, breaking annular summability.
- The endpoint-current recovery map changes the centered flowed Wilson cumulant beyond E_rec^+.
- A cutoff plateau failure shows that the positive margin is a regulator artifact.
- The zero-pairing quotient identifies currents whose sector pairings differ outside certified tolerance.
- The tested observable fails to remain a same-theory connected cumulant witness under the chosen flow and counterterm scheme.

## Learning

Cycle 351 attacks the conceptual pressure that finite Schur-Feshbach positivity needs a same-theory Wilson mediator. The declarative tension is exact: endpoint positivity, positive flowed pair covariance, and recovery from raw hairpins can each be valid while connected C4 erases R_{++}. Raw contours are too fragmented; global OS transfer, area-law intuition, and broad same-theory nontriviality witness selection are too coarse. Endpoint sheet currents are efficient only with encoded H,K sheets, endpoint moments, sector kernels, counterterms, recovery errors, L_+, preserved gauge/color/reflection/orientation/cutoff/locality invariants, Ward/cusp subtraction, Taylor Hessians, dyadic intervals, outward rounding, certified zero-pairing equivalence, finite endpoint locality, and falsifiers. Value signal: the first annulus is now a validator-facing Ward-Hessian quadrature certificate for a connected cumulant witness, not a symbolic boundary-OPE term.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete thought experiment now as a falsifier probe and proof-search guide.`
- Rationale: The branch no longer needs another obstruction restatement; the decisive unknown is whether the actual first-annulus connected C4 polarization can be bounded below strongly enough to beat L_+.
- Situation seed: SU(N) hypercubic Wilson lattice with fixed H,K plus hairpin endpoint geometry, gradient-flow time t(a), and first annulus A_0={rho_0<=|x-y|<2rho_0} for the Ward-subtracted endpoint sheet-current kernels.
- Varied variable: plateau ratio p=rho_0/sqrt(8t), varied over a small interval while keeping physical H,K geometry fixed.
- Held-fixed controls: same bare-coupling trajectory and cutoff family for pair term, C4 sectors, recovery map, and L_+, same centered flowed Wilson hairpin observable W_+^{ren} and same counterterm scheme, same endpoint cell partition rule up to certified refinement and outward rounding, same finite-volume separation so endpoint annuli do not touch boundaries
- Expected observation: A stable positive lower interval Delta_R^-(p) would promote finite endpoint-box positivity after H,K; a sign change, wide interval, or negative value would quarantine the R++ repair.
- Transfer certificate needed: Outward-rounded quadrature for H_{s,0}^+(p), certified Ward/cusp cancellation, recovery error bound E_rec^+, dyadic tail ratios q_s<1, and cutoff-plateau validation before the intuition affects proof obligations.

## Next Experiment

Proof search: perform outward-rounded first-annulus quadrature for H_{3g,0}^+, H_{4g,0}^+, H_{ct,0}^+, and H_{end,0}^+ for the actual H,K endpoint currents, then evaluate Delta_R^- as a validator-facing same-theory nontriviality witness boundary and connected cumulant witness quarantine test.

# Support-function raw K4 stress witness for finite YM endpoint PSD

## Candidate Lemma

In a fixed heat-kernel cutoff endpoint box, a support-function lower bound on one signed raw K4 off-diagonal, together with two diagonal upper bounds, gives a valid finite falsifier of Schur-corrected endpoint PSD.

## Definitions

- source object: finite SU(N) heat-kernel lattice endpoint box with Wilson plaquette sheets Q_i, signed raw connected K4 orbit intervals, OPE intervals, and H,K Schur blocks.
- target object: the Schur-corrected finite endpoint Hermitian matrix U_sigma on the worked Wilson basis, whose PSD is only the local Route A endpoint gate.
- controlled interface: Rec_sigma maps Gaussian color squares, signed K4 supports, OPE intervals, and S_HK into interval entries, then tests a two-sparse Rayleigh stress.
- same-theory condition: the same lattice spacing a, regulator sigma, coupling g_R, Wilson basis, transporters, reflection support, and H,K data are used throughout.

## Assumptions

- Model: finite-volume lattice Yang-Mills with compact SU(N), heat-kernel plaquette regulator, and a fixed endpoint collar/hairpin geometry.
- Cutoff: a and sigma are fixed with finite endpoint complexity; no continuum, volume-uniform, or OS spectral-transfer claim is made.
- Same-theory: vacuum/perimeter cancellation, Wilson centering, and exact quotient identities are performed before interval compression.
- Validity: signed orbit intervals are outward-rounded and Hermitian; support functions enclose all raw K4 phases without phase-net discretization.

## Equations

- Schur-corrected endpoint entry: `U_{ij}=G_{ij,\sigma}+\frac{g_R^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma}-S^{HK}_{ij}`. Valid when: Valid when the finite heat-kernel endpoint basis, same Wilson normalization, and Schur blocks are fixed before interval recovery.
- support lower bound: `L_{pq}(\nu)=\underline{\mathrm{Re}(\overline{\nu}U_{pq})}\le |U_{pq}|,\qquad |\nu|=1`. Valid when: Valid when signed K4 orbit intervals are outward-rounded and exact Wilson quotienting preserves Hermitian phases.
- two-sparse stress gate: `D_p^+<0\quad\text{or}\quad D_p^+D_q^+-L_{pq}(\nu)^2<0\;\Rightarrow\; U_\sigma\not\succeq0`. Valid when: Valid when D_p^+ and D_q^+ are diagonal upper bounds and L_pq(nu) is a lower bound for the off-diagonal modulus.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: finite SU(N) heat-kernel lattice endpoint box with Wilson plaquette sheets Q_i, signed raw connected K4 orbit intervals, OPE intervals, and H,K Schur blocks.; target object: the Schur-corrected finite endpoint Hermitian matrix U_sigma on the worked Wilson basis, whose PSD is only the local Route A endpoint gate.; Model: finite-volume lattice Yang-Mills with compact SU(N), heat-kernel plaquette regulator, and a fixed endpoint collar/hairpin geometry..
- Fix the endpoint Wilson basis and compute G from crossed heat-kernel curvature contractions; centering cancels disconnected vacuum and perimeter pieces.
- Recover K^{(4)}_{pq} from signed raw plaquette orbits and apply the support direction nu to bound Re(conj(nu)U_pq) without a phase-net gap.
- Combine diagonal upper intervals D_p^+,D_q^+ with L_pq(nu); a negative 2x2 determinant gives an explicit Rayleigh stress vector.
- Non-claim boundary: absence of stress is not PSD; it only routes to full Delta_raw proof search or quarantine, while gauge-invariant observable density stays untouched.

Blocking gap: The actual same-regulator signed K4 support intervals for the chosen p,q endpoint pair are not yet computed.

## Falsifiers

- falsifier: outward-rounded raw K4 intervals make L_pq(nu)^2<=D_p^+D_q^+ for every support direction tested or certified.
- falsifier: exact Wilson quotienting changes a signed orbit phase, invalidating the Hermitian support lower bound.
- falsifier: OPE overflow or Schur hairpin energy raises D_p^+D_q^+ enough to remove every negative Rayleigh margin.
- falsifier: K4 intervals were computed at a different regulator, coupling, boundary support, or Wilson normalization.

## Learning

Conceptual pressure: raw K4 data must mediate to finite endpoint PSD without OS-density circularity. Support functions are sharper than phase nets because one convex certificate controls phases. Value signal: a valid finite falsifier or full-Delta handoff, with Clay gates untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the finite H,K endpoint route.`
- Rationale: The branch is looping unless raw non-Gaussian K4 data becomes a connected cumulant witness; support functions test phases without importing OS Hilbert observable algebra.
- Situation seed: Fixed SU(2) heat-kernel lattice endpoint box with two reflected Wilson sheets p,q after the same H,K Schur subtraction; raw plaquette orbits crossing the shared boundary supply K4 intervals.
- Varied variable: Support direction nu on the complex off-diagonal K4 orbit cone.
- Held-fixed controls: lattice spacing a, regulator sigma, coupling g_R, and endpoint Wilson basis, H,K Schur block, reflection support, Wilson centering, and exact quotient identities
- Expected observation: Either some nu gives L_pq(nu)^2>D_p^+D_q^+, yielding a finite stress falsifier, or no support direction does and the branch must attempt full Delta_raw.
- Transfer certificate needed: A validator-facing interval file for signed K4 orbits, OPE bounds, Gaussian G, and S_HK, with same-theory metadata and Hermitian quotient audit.

## Next Experiment

proof search: compute one same-theory connected cumulant witness for p,q signed K4 supports and test D_i^+<0 or L_pq(nu)^2>D_p^+D_q^+; keep gauge-invariant observable density quarantined.

