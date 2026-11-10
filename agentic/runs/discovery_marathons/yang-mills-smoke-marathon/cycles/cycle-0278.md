# cycle-0278

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Post-H,K endpoint-source interval certificate for reflected Wilson hairpins

## Candidate Lemma

Finite endpoint clipping certificate: in the heat-kernel plaquette-sheet regulator, the post-H,K null-channel endpoint contribution is bounded by a scalar interval determined by singlet fourth source cumulants and the binary endpoint incidence table. If I_->0 the finite reflected-Wilson block passes this endpoint gate; if I_+<0 it is a same-theory falsifier for this block only.

## Definitions

- source object: regulated SU(N) Yang-Mills heat-kernel plaquette-sheet endpoint boxes v carrying localized Wilson flux sources L_v for the three reflected hairpin pairings 12,13,23.
- target object: the finite post-H,K Schur-Feshbach null-channel OS scalar for the locked three-hairpin Wilson block, not a continuum mass gap statement.
- controlled interface: the carrier C_ep=(b_{12},b_{13},b_{23},beta_v^-,beta_v^+,tau_v)_v transferred to the scalar interval [I_-,I_+].
- same-theory condition: the Wilson loops, heat-kernel normalization, reflection map, null vector, and source derivatives are those of the original regulated gauge-invariant lattice theory with no boundary counterterm or algebra enlargement.
- endpoint box: a cutoff-local box around a reflected Wilson endpoint after Wick-square Gram terms and straight-segment f f contacts have been removed.
- binary incidence: b_{ij}(v)=1 exactly when endpoint box v belongs to the ij reflected-pair overlap footprint, otherwise b_{ij}(v)=0.
- negative cumulant magnitude: kappa_{4,v}^{sing} in [-beta_v^+,-beta_v^-] with 0<=beta_v^-<=beta_v^+.
- tail budget: tau bounds all cross-box, corner, nonlocal, and cutoff remainder terms not represented by the endpoint-box sum.

## Assumptions

- Model: four-dimensional lattice SU(N) Yang-Mills with Wilson heat-kernel plaquette action and gauge-invariant Wilson observables only.
- Regime: fixed finite three-hairpin collar block after the already computed H,K Schur-Feshbach reductions, with endpoint boxes small compared with collar separation scale.
- Cutoff: all beta and tau bounds are uniform over the cutoff range used for the finite Route A certificate.
- Same-theory: source differentiation is applied to the same regulated Wilson partition function that defines the collar OS matrix.
- Local: non-endpoint connected cumulants are either canceled by the null incidence identity or charged to tau.
- Validity: the claim is a finite endpoint gate and does not assert continuum existence, OS density, Wightman reconstruction, or a Hamiltonian mass gap.

## Equations

- binary_endpoint_incidence_table: `D_v=2b_{12}(v)-4b_{13}(v)-4b_{23}(v),\quad (D_{000},D_{100},D_{010},D_{001},D_{110},D_{101},D_{011},D_{111})=(0,2,-4,-4,-2,-2,-8,-6).`. Valid when: Valid when each endpoint box has binary membership in the three reflected-pair footprints after the H,K null vector is fixed.
- singlet_endpoint_cumulant_interval: `\kappa_{4,v}^{\mathrm{sing}}=\left.\partial_s^4\log Z_v(sL_v)\right|_{s=0}\in[-\beta_v^+,-\beta_v^-],\qquad 0\le \beta_v^-\le\beta_v^+.`. Valid when: Valid when the localized heat-kernel source partition function has a certified fourth connected derivative interval in the same regulated theory.
- post_HK_gate_interval: `I_-:=M_G-C_N\sum_v\beta_v^+[D_v]_+ +C_N\sum_v\beta_v^-[-D_v]_+ -\tau\le I_{\mathrm{gate}}\le M_G-C_N\sum_v\beta_v^-[D_v]_+ +C_N\sum_v\beta_v^+[-D_v]_+ +\tau=:I_+,\quad C_N={g^4\over4}\left({T_F\over N}\right)^2.`. Valid when: Applies after Wick-square Gram positivity and straight f f incidence cancellation have removed the non-dangerous Wilson contractions.

## Attempted Derivation

- Conceptual pressure attacked: endpoint collapse must be sign-certified while preserving collar OS positivity and the fixed gauge-invariant Wilson algebra.
- Declarative tension: finite collar reflection positivity, unchanged Wilson observables, and singular connected endpoint OPE must jointly hold, but raw R is representation-limited and raw kappa_4 is too strong because it forgets incidence signs.
- Use the heat-kernel plaquette-sheet regulator and localize the remaining post-H,K connected Wilson contraction to endpoint boxes after Wick-square Gram positivity and straight f f null-incidence cancellation.
- Contract the endpoint fourth cumulant with the already fixed Feshbach null weights; this gives D_v=2b12-4b13-4b23 and the explicit binary table with only the 100 class dangerous for negative kappa_4.
- Represent kappa_{4,v}^{sing} by seven same-theory source values of F_v(s)=log Z_v(sL_v), with the fourth-difference error controlled by 7h^4M8/240.
- Convert kappa intervals and the incidence table into [I_-,I_+]; promotion and demotion are now scalar interval decisions for this finite Wilson block.

Blocking gap: Actual beta_v intervals and a cutoff-uniform tau are still missing for the concrete endpoint geometry; without them the certificate is a valid finite theorem schema but not a numerical promotion.

## Falsifiers

- A seven-point source computation in the same heat-kernel theory gives enough 12-only endpoint dominance that I_+<0; this is the intended finite falsifier.
- The eighth-derivative bound M8 or the tail tau is not cutoff-uniform, so the endpoint interval cannot be transferred beyond the regulator scale.
- A hidden endpoint class has b13 or b23 incidence omitted from the binary carrier, invalidating the claimed positive/protective cancellation.
- The endpoint cumulant requires a boundary counterterm or a changed Wilson normalization; then the calculation is not same-theory even if the interval is positive.
- Cross-box connected cumulants have a signed negative contribution larger than tau, demoting the clipped endpoint abstraction.

## Learning

Cycle 278 converts the clipped endpoint carrier from a slogan into a finite interval theorem with a computed binary incidence table. The conceptual pressure is endpoint collapse in the same Wilson theory. The declarative tension is collar OS positivity plus fixed gauge-invariant Wilson observables plus singular connected endpoint OPE; the missing mediator is a cutoff-uniform source carrier. Raw R is representation-limited, and a raw kappa_4 spectrum is too strong because it ignores null incidence. Compared with the global Schur-preimage route, C_ep is local and computable after H,K; compared with formal OPE language, it supplies primitive operations: source differentiation, interval arithmetic, color multiplication, incidence clipping, and tail addition. Efficient representation requirements are now concrete: encode endpoint boxes, seven source values, beta intervals, binary incidences, C_N, M_G, and tau; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff bookkeeping, and same-theory observables; identify carriers only by equal regulated source data; keep locality finite through tau; transfer only [I_-,I_+] to the finite OS gate. The hard gate changed is the finite post-H,K reflected-Wilson OS transfer gate. The conceptual value signal is sharpness and route change: negative compact-group kappa_4 is not itself the obstruction; only certified 12-only endpoint dominance plus uncontrolled tail can be a falsifier.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and endpoint-data design, not as another abstract restatement.`
- Rationale: The branch has already isolated H,K and the endpoint carrier; the only proof-relevant uncertainty is whether same-theory endpoint source intervals make the finite gate positive or negative.
- Situation seed: Fixed SU(N) heat-kernel plaquette-sheet three-hairpin block with identical H,K data and endpoint boxes sorted into binary incidence classes 100,010,001,110,101,011,111.
- Varied variable: p12, the fraction or weighted count of endpoint boxes that are 12-only with D_v=2.
- Held-fixed controls: The Wilson loops, reflection map, Feshbach null vector, heat-kernel regulator, and color factor C_N are held fixed., The seven-point source stencil step h, the Gaussian margin M_G, and the same-theory no-boundary-counterterm rule are held fixed., All non-endpoint and cross-box terms are charged to the same tail budget tau.
- Expected observation: As p12 increases, the certified interval lower endpoint decreases; crossing I_+<0 gives a finite same-theory falsifier, while I_->0 for the measured p12 promotes the endpoint gate.
- Transfer certificate needed: Cutoff-uniform source derivative intervals for every endpoint class plus a locality proof that all omitted cumulants are bounded by tau without changing the Wilson observable algebra.

## Next Experiment

Compute the actual endpoint incidence multiset for the three hairpin geometry, evaluate or bound F_v(rh)=log Z_v(rhL_v) for r=-3,...,3 in the heat-kernel endpoint box, derive beta_v intervals and tau, then decide the sign of [I_-,I_+].

# Endpoint-moment Hessian certificate for the post-H,K Wilson R term

## Candidate Lemma

Endpoint-moment Hessian certificate: for flowed, centered, cusp/perimeter-renormalized thin Wilson hairpins in the plus channel, the connected boundary-OPE polarization term satisfies a computable lower interval bound R_{++}^{ren} >= 2(N^2-1)G_{++}-N(N^2-1)eta^2 M_+^2 H_4-E_{ren}-E_6. If this lower bound beats the finite Schur-Feshbach leakage L_+, the endpoint-box positivity gate after H,K is promoted; otherwise this R repair is demoted. This is a local finite theorem candidate, not a Clay mass-gap claim.

## Definitions

- source object: finite-volume lattice SU(N) Yang-Mills with Wilson action, lattice spacing a, gradient-flow time t>0, reflection plane fixed, and two reflected thin Wilson hairpins represented by oriented plaquette-sheet currents J_1,J_2.
- target object: the scalar same-theory endpoint mediator R_{++}^{ren} entering the finite H,K plus-channel Schur-Feshbach endpoint box; the target property is a numerical positivity margin R_{++}^{ren}>L_+/kappa_4, not continuum existence or a Hamiltonian mass gap.
- controlled interface: sheet-current-to-Wilson recovery map plus flowed Wilson cumulants, with disconnected-product subtraction, one-hairpin perimeter/cusp subtraction, Ward subtraction, endpoint Taylor expansion, and interval Hessian enclosure of the connected four-curvature kernel.
- same-theory condition: all Wilson observables, gradient-flow fields, renormalization constants, cumulants, endpoint currents, and cutoff removals are taken in one lattice Wilson family and one candidate continuum Schwinger family; no auxiliary Gaussian or representation-dynamics theory may replace it.
- R_{++}^{ren}: kappa_2 of the two centered renormalized plus-channel hairpin observables after the H,K endpoint projection.
- G_{++}: positive pair-contraction geometry integral of two flowed curvature two-point functions over the reflected endpoint sheets.
- C_{4,++}^{WS}: Ward-subtracted connected four-curvature polarization kernel contribution to the same Wilson cumulant.
- eta: endpoint-box radius; H_4: certified supremum of the mixed endpoint Hessian of the Ward-subtracted connected four-curvature kernel on the interval cells.

## Assumptions

- Model: hypercubic finite-volume lattice SU(N), N>=2, Wilson action, gauge-invariant Wilson-loop observables, and reflection-positive measure before inserting flowed observables.
- Regime: endpoint boxes are separated by distance d >= 8 sqrt(8t)+4 eta from each other, collars, and non-endpoint sheet pieces, with eta <= c sqrt(8t).
- Cutoff: a << eta and t >= c_0 a^2; the interval constants H_4,E_{ren},E_6 must be bounded uniformly over the stated cutoff window.
- Same-theory: the same bare coupling trajectory, flow time prescription, centering, cusp/perimeter normalization, and endpoint projection define both the pair term and C_{4,++}^{WS}.
- Local: the claim concerns only the finite endpoint box after the H,K collar/hairpin reduction; continuum OS/Wightman axioms, nontriviality, and spectral mass gap remain untouched.
- Constraint: plus-channel endpoint charges obey Ward, monopole, and dipole cancellation; violations are treated as a falsifier, not as removable notation.
- Validity: the fourth-order boundary OPE remainder E_6 is interval-bounded in the same endpoint-cell partition used for H_4.

## Equations

- renormalized-centered-hairpin: `\mathcal O_J^{ren}(t,a)=Z_{per}^{-1}Z_{cusp}^{-1}\left(N^{-1}\operatorname{Re}\operatorname{Tr}U_t(\partial\Sigma_J)-\langle N^{-1}\operatorname{Re}\operatorname{Tr}U_t(\partial\Sigma_J)\rangle\right)`. Valid when: Valid when the lattice Wilson action, gradient flow, centering, and cusp/perimeter renormalization are fixed before taking cumulants.
- endpoint-R-cumulant: `R_{++}^{ren}(t,a,\eta)=\kappa_2\left(\mathcal O_{J_+^{(1)}}^{ren},\mathcal O_{J_+^{(2)}}^{ren}\right)`. Valid when: Applies to the reflected plus-channel endpoint hairpins after the H,K projection and same-theory centering have been performed.
- pair-plus-connected-decomposition: `R_{++}^{ren}=2(N^2-1)\mathcal G_{++}+N(N^2-1)\Xi_{++}^{WS}+E_6`. Valid when: Valid in the fourth-order flowed boundary OPE after disconnected products and one-hairpin perimeter/cusp pieces have been subtracted.
- connected-polarization-integral: `\Xi_{++}^{WS}=\int J_+^{(1)}(x_1)J_+^{(1)}(x_2)J_+^{(2)}(y_1)J_+^{(2)}(y_2)K_{4,t}^{WS}(x_1,x_2;y_1,y_2)\,dx\,dy`. Valid when: Requires the Ward-subtracted connected four-curvature kernel for the same flowed Wilson measure and the same endpoint sheet-current representation.
- plus-channel-moment-cancellation: `\sum_e q_e=0,\qquad \sum_e q_e(z_e-z_0)=0`. Valid when: Valid for the chosen plus endpoint current only after orientation, reflection, and collar endpoint charges are checked cell by cell.
- hessian-C4-bound: `|\Xi_{++}^{WS}|\le \eta^2 M_+^2 H_4(t,d,\eta)+E_{Ward}+E_{cusp}`. Valid when: Applies when monopole and dipole moments vanish and K_{4,t}^{WS} has a certified mixed endpoint Hessian on every interval cell.
- R-lower-interval: `R_{++}^{ren}\ge 2(N^2-1)\mathcal G_{++}-N(N^2-1)\eta^2M_+^2H_4-E_{Ward}-E_{cusp}-E_6`. Valid when: Valid when the pair geometry integral is positive, the C4 Hessian enclosure is cutoff-uniform, and all listed errors share the same theory.
- promotion-inequality: `2(N^2-1)\mathcal G_{++}-N(N^2-1)\eta^2M_+^2H_4-E_{tot}>L_+/\kappa_4`. Valid when: Promotes only the finite endpoint-box positivity gate when L_+ is the Schur-Feshbach leakage from the already fixed H,K finite matrix.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach positivity needs a same-theory endpoint mediator; positive flowed pair covariance and Wilson renormalization are valid but do not stop C_{4,++}^{WS} from erasing the pair term.
- Freeze claim level: prove at most a finite endpoint-box positivity certificate after H,K; the Clay requirements of four-dimensional YM existence, OS/Wightman axioms, nontrivial continuum limit, and positive Hamiltonian mass gap remain untouched.
- Represent each H,K plus-channel hairpin by an oriented flowed endpoint sheet current J_+ and recover the original Wilson observable through Pi with E_{sheet}.
- Use the centered renormalized Wilson cumulant R_{++}^{ren}=kappa_2(O_{J_+^{(1)}}^{ren},O_{J_+^{(2)}}^{ren}) as the source-to-target carrier, not an auxiliary Gaussian model.
- Expand the endpoint-local flowed boundary OPE through fourth order: the two cross-pairings give 2(N^2-1)G_{++}; the remaining connected four-curvature term has color factor N(N^2-1) and kernel K_{4,t}^{WS}.
- Apply disconnected-product cancellation and one-hairpin perimeter/cusp subtraction; then enforce Ward plus-channel monopole and dipole cancellations on the endpoint charges.
- Taylor expand K_{4,t}^{WS} inside endpoint boxes. The constant and linear terms vanish by moment cancellation, leaving a mixed-Hessian remainder bounded by eta^2 M_+^2 H_4 plus Ward/cusp residuals.
- Insert the resulting lower interval R_- into Q_{+}^{bare}+kappa_4R_- - L_+. Success changes the hard gate of finite endpoint-box positivity after H,K; failure quarantines this R repair.

Blocking gap: The missing proof object is a certified cutoff-uniform interval enclosure of H_4 and E_6 for the Ward-subtracted connected four-curvature sectors I_3g, I_4g, I_ct, and I_end in the actual lattice-flow regulator.

## Falsifiers

- falsifier: the plus-channel endpoint current fails exact monopole or dipole cancellation after orientation and reflection are checked.
- falsifier: the Ward-subtracted C4 Hessian H_4 grows like eta^{-2} or faster, eliminating endpoint-moment suppression.
- falsifier: cusp/perimeter subtraction has no same-theory plateau as a->0 at fixed flow time.
- falsifier: the certified lower interval R_- satisfies Q_{+}^{bare}+kappa_4R_- - L_+ <= 0.
- falsifier: non-Abelian Stokes/path-ordering recovery error E_{sheet} is of the same size as the positive pair term.
- falsifier: finite-volume or topological sectors contribute endpoint-local terms not captured by the cell Hessian kernel.
- stress case: take eta comparable to sqrt(8t) and endpoint separation minimal; if interval width explodes, demote to quarantine rather than promote.

## Learning

Declarative tension: finite Schur-Feshbach positivity, positive flowed pair covariance, and same-theory Wilson renormalization must jointly hold, but the connected four-curvature polarization can erase the pair term unless a cutoff-uniform Hessian interval is valid. Current carrier critique: raw contours are too fragmented; global non-Gaussian OS witnesses are too coarse for this local obstruction. Endpoint sheet currents are the efficient representation because they encode H,K sheets and endpoint charges, preserve gauge/color/reflection/orientation/same-theory invariants, use Ward subtraction and interval Hessians as primitives, enforce certified zero-pairing equivalence, keep locality to endpoint cells, and expose falsifiers. Conceptual value signal: local route-changing; R_{++}/kappa_4 becomes a concrete Wilson cumulant with a color-geometric lower interval, not a symbolic threshold. Hard gate changed: finite endpoint-box positivity after H,K; all Clay gates remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide, not as evidence for the Clay theorem.`
- Rationale: The branch no longer needs another abstract OS/Wilson restatement; it needs a concrete test of whether endpoint-moment cancellation can make C_{4,++}^{WS} small compared with the positive pair baseline in the same Wilson theory.
- Situation seed: Finite-volume lattice SU(2) and SU(3) Wilson action with gradient-flowed reflected H,K plus-channel hairpins, endpoint boxes partitioned into interval cells, and R_{++}^{ren} computed from the Ward-subtracted connected four-plaquette-sheet cumulant.
- Varied variable: sigma=eta/sqrt(8t), the endpoint-box radius measured in flow units, varied from 0.1 to 0.8 while endpoint separation d/sqrt(8t) is held fixed.
- Held-fixed controls: Same Wilson lattice action, bare-coupling trajectory, reflection plane, H,K hairpin geometry, and plus-channel endpoint orientation., Same cusp/perimeter renormalization, centering convention, gradient-flow time prescription, and Schur-Feshbach leakage L_+ normalization., Same interval-cell partition policy and same Ward-subtracted sector decomposition I_3g,I_4g,I_ct,I_end.
- Expected observation: If the endpoint-moment mechanism is valid, C_{4,++}^{WS}/G_{++} scales like O(sigma^2) after Ward and cusp cancellation while G_{++}>0 remains stable; if the ratio plateaus negative or grows, the R repair is falsified.
- Transfer certificate needed: A rigorous interval arithmetic certificate, uniform in lattice spacing over the flow window and tied to the same Wilson cumulants, must replace numerical intuition before any promotion of finite endpoint-box positivity.

## Next Experiment

Construct the interval kernel table for K_{4,t}^{WS}: split I_3g,I_4g,I_ct,I_end, compute heat-kernel majorants and mixed endpoint Hessian suprema on the fixed H,K endpoint cells, then evaluate the certified lower bound R_- against L_+ for SU(2) and SU(3).

# First same-regulator kappa4 shell interval for the post-H,K Wilson endpoint

## Candidate Lemma

Finite endpoint-box positivity follows from a same-regulator shell bound on the compressed connected four-curvature cumulant after the H,K Schur subtraction.

## Definitions

- source object: finite SU(N) heat-kernel regulated Wilson endpoint box at cutoff a, smoothing scale sigma, coupling g_R, and fixed H,K collar/hairpin Wilson basis.
- target object: Schur-corrected endpoint quadratic form on the finite endpoint subspace E_end, not the reconstructed continuum Hamiltonian spectrum.
- controlled interface: sheet-kernel hypergraph Rec_sigma mapping Wilson plaquette sheets to C_sigma, K4_sigma, E_OPE_sigma, and S_HK without changing regulator or observable algebra.
- same-theory condition: C_sigma, K4_sigma, E_OPE_sigma, and S_HK are extracted from the same cutoff action, same boundary Wilson basis, same reflection split, and same normalization.
- Boundary-OPE polarization R_sigma is the connected vacuum/perimeter-subtracted covariance of endpoint Wilson observables after transported curvature expansion.
- C_sigma is the transported two-curvature sheet covariance matrix; K4_sigma is the compressed connected four-curvature cumulant matrix; S_HK=B^*E^{-1}B is the finite Schur hairpin energy.

## Assumptions

- Model: four-dimensional finite-volume SU(N) lattice Yang-Mills with heat-kernel action and reflected endpoint Wilson sheets inside one collar box.
- Regime: sigma/a is fixed during the finite computation and the boundary OPE is used only for loops whose sheet diameter is O(sigma).
- Cutoff: all matrices are finite-dimensional before any volume, cutoff, or continuum limit is invoked.
- Same-theory: the OPE coefficients, cumulants, and H,K Schur block are computed in the identical cutoff measure; no imported continuum spectral data are used.
- Local: endpoint sheets remain at positive reflected time separation except at the controlled boundary collar where the OPE remainder is assigned to E_OPE_sigma.
- Validity: Delta_sigma>0 certifies only this finite Route A endpoint-box positivity gate and does not imply OS reconstruction, nontrivial continuum existence, or a Clay mass gap.

## Equations

- connected Wilson polarization decomposition: `R_{\sigma}=\alpha_N g_R^4\,(C_{\sigma}\circ C_{\sigma})+\frac{g_R^4}{16N^2}K4_{\sigma}+E_{\mathrm{OPE},\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when the same heat-kernel cutoff Wilson endpoints are vacuum/perimeter subtracted and the transported boundary curvature OPE is applied inside the finite collar box.
- four-curvature shell envelope: `\rho_{-}(K4_{\sigma})\le \rho(|K4_{\sigma}|)\le \max_{v\in E_{\mathrm{end}}}\sum_{s=0}^{S}\sum_{u\in \mathcal S_s(v)} |K4_{\sigma,uv}|\le \sum_{s=0}^{S} n_s A_s(\sigma)`. Valid when: Applies when the sheet-kernel hypergraph quotient preserves Wilson trace symmetries and each shell s has multiplicity n_s with uniform entry bound A_s(sigma).
- Schur-corrected endpoint margin: `\Delta_{\sigma}:=\lambda_{\min}\!\left(\alpha_N g_R^4(C_{\sigma}\circ C_{\sigma})\right)-\frac{g_R^4}{16N^2}\sum_s n_s A_s(\sigma)-\|E_{\mathrm{OPE},\sigma}\|-\|S_{HK}\|`. Valid when: Valid when C_sigma, shell amplitudes A_s, OPE norm, and S_HK are computed for the same finite endpoint basis and operator norm.
- finite endpoint certificate: `\Delta_{\sigma}>0\;\Longrightarrow\; P_{\mathrm{end}}\bigl(R_{\sigma}-S_{HK}\bigr)P_{\mathrm{end}}\ge \Delta_{\sigma} I_{E_{\mathrm{end}}}`. Valid when: Requires the finite Schur-Feshbach block decomposition, endpoint compression, and the preceding same-regulator row-sum bound on the negative kappa4 contribution.

## Attempted Derivation

- Conceptual pressure attacked: mediate actual connected Wilson cumulants to Schur-corrected endpoint positivity without inflating a finite Wilson computation into OS reconstruction or a Clay mass-gap proof.
- Declarative tension: Wilson/OPE coefficients, connected kappa4 negativity, OPE error, and H,K Schur energy must be valid in one cutoff theory, while continuum OS positivity, observable density, and physical-unit spectral transfer remain quarantined.
- The scalar R carrier is too weak and representation-limited; full gauge-invariant OS density is too strong and circular for this local gate; raw plaquette enumeration is exact but fragmented.
- Chosen abstraction: sheet-kernel hypergraph, because it encodes sheets, weights, heat-kernel transporters, SU(N) trace tensors, shell labels, multiplicities, OPE intervals, and Schur data.
- Efficient representation requirements: preserve gauge invariance, reflection support, Gaussian/kappa4 separation, endpoint compression, and same-theory normalization; primitive operations are cumulant contraction, quotient auditing, shell row/operator bounds, interval arithmetic, and Schur subtraction.
- Starting from W_u=tr P exp(i g_R integral_{partial Sigma_u} A), use the transported small-sheet expansion and subtract <W_u><W_v>; disconnected vacuum and perimeter terms cancel in the connected covariance.
- The crossed two-curvature contractions yield alpha_N g_R^4(C_sigma o C_sigma), with alpha_N=(N^2-1)/(8N^2) in the fundamental trace normalization tr(T^aT^b)=delta^{ab}/2.
- The remaining four-field connected part is K4_sigma/(16N^2) times g_R^4 plus E_OPE_sigma; its negative spectral contribution is bounded by Gershgorin/Schur row sums over hypergraph locality shells.
- Combine the lower bound on the PSD Gaussian square with the upper bound on the negative kappa4 part, the OPE norm, and the H,K Schur energy to obtain Delta_sigma.
- Hard gate: Delta_sigma>0 promotes only finite endpoint-box positivity for the worked H,K geometry; Delta_sigma<=0 is a valid falsifier or demotion trigger for this Wilson collar/hairpin route.

Blocking gap: No rigorous numerical or symbolic shell amplitudes A_s(sigma) have yet been computed for the actual H,K endpoint sheet list; the heat-kernel connected four-curvature cumulant still needs a same-cutoff cluster/plaquette-sheet bound with color tensors included.

## Falsifiers

- falsifier: the first computed shell envelope satisfies sum_s n_s A_s(sigma) >= 16N^2(g_R^{-4}(m_G-e_OPE-s_HK)) for every admissible sigma, making Delta_sigma nonpositive.
- falsifier: Rec_sigma identifies two sheet configurations by a trace symmetry but their transported color contractions differ after reflection, invalidating the quotient.
- falsifier: the OPE remainder is comparable to or larger than the PSD Gaussian floor for the actual collar geometry.
- falsifier: S_HK has a localized hairpin mode aligned with the smallest eigenvector of C_sigma o C_sigma, erasing the endpoint margin.
- Stress case: adjacent endpoint sheets sharing a boundary plaquette maximize kappa4 contact terms and test whether shell s=0 already kills the route.
- Failure case: if A_s(sigma) decays only by volume multiplicity compensation rather than locally summable shell decay, the finite evidence cannot be promoted to any frontier RG gate.

## Learning

Cycle 278 converts the repeated R/kappa4 aspiration into a sharper finite shell certificate: the actual connected Wilson polarization is decomposed into a PSD Gaussian color square, a compressed four-curvature cumulant with Gershgorin shell envelope, an OPE interval, and the H,K Schur subtraction. The hard gate is Delta_sigma. Success changes only the finite Route A endpoint-box proof state; failure gives a valid falsifier for this collar/hairpin geometry. The conceptual value signal is explanatory and route-changing at finite scope because it identifies exactly which computable object--the same-regulator shell amplitudes A_s(sigma)--must be bounded next.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and finite-computation design, not as continuum evidence.`
- Rationale: The branch has repeated the Delta_sigma abstraction; the concrete next learning requires seeing whether same-regulator kappa4 contact shells can numerically or rigorously dominate the positive Gaussian color square in the actual endpoint geometry.
- Situation seed: Finite SU(N) heat-kernel lattice endpoint box containing the worked H,K Wilson collar/hairpin sheets, with endpoint plaquette sheets expanded to transported curvature variables and reflected support fixed.
- Varied variable: sigma/a, the smoothing-to-lattice spacing ratio controlling the width of the heat-kernel boundary OPE and the contact strength of the kappa4 shell.
- Held-fixed controls: same H,K endpoint Wilson basis and Schur block S_HK, same finite cutoff action, volume box, coupling g_R, and SU(N) trace normalization, same vacuum/perimeter subtraction and reflected Wilson support, same hypergraph quotient policy and endpoint compression
- Expected observation: If kappa4 is local and summably bounded, A_0 dominates but finite shells give a stable interval for Delta_sigma; a sign flip as sigma/a varies identifies whether contact kappa4 or hairpin Schur energy is the route killer.
- Transfer certificate needed: A rigorous same-cutoff plaquette-sheet cumulant bound for K4_sigma with color tensors, OPE remainder interval, and quotient-invariance audit before the observation may enter proof obligations.

## Next Experiment

Compute the first two heat-kernel plaquette-sheet shells A_0(sigma), A_1(sigma) for the actual H,K endpoint basis, including SU(N) trace tensors, transported covariance kernels, connected cumulant subtraction, and the Schur energy alignment with the weakest Gaussian endpoint mode.

