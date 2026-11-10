# cycle-0337

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: endpoint source interval quarantine

## Candidate Lemma

Endpoint source intervals decide the remaining finite post-H,K gate: after valid cancellations, same-theory OS transfer for the fixed block follows from I_gate^- >=0 and is a falsifier if I_gate^+<0; otherwise quarantine remains.

## Definitions

- source object: heat-kernel plaquette-sheet SU(N) endpoint boxes with source-deformed Wilson flux partition functions Z_c(s).
- target object: finite post-H,K reflected-Wilson OS transfer scalar for the fixed three-hairpin block.
- controlled interface: C_ep maps endpoint source cumulant intervals and signed incidences to I_gate without adding boundary degrees of freedom.
- same-theory condition: source classes are equivalent only by equal regulated Wilson source data and use the locked gauge-invariant observable algebra.
- connected cumulant witness: kappa_c is the fourth source derivative of log Z_c for the singlet endpoint flux source L_c.
- hard gate: the finite post-H,K reflected-Wilson OS scalar; it changes only this block, not continuum existence or mass gap.

## Assumptions

- Model: four-dimensional SU(N) lattice YM with heat-kernel plaquette action on finite endpoint boxes.
- Regime: fixed finite H,K hairpin block; endpoint width and source step are small in a cutoff-uniform collar window.
- Cutoff: eighth source-derivative bounds and T_tail are uniform in plaquette spacing for the endpoint classes used.
- Same-theory: no boundary counterterm or new boundary Hilbert sector is introduced during endpoint collapse.
- Validity: connected logs remove Wick-square Gram pieces, and null incidence cancels straight C_A f f contact terms.

## Equations

- endpoint source cumulant interval: `\kappa_c=\partial_s^4\log Z_c(s)|_{s=0}\in[\Delta_h^4\log Z_c-\epsilon_{c,h},\Delta_h^4\log Z_c+\epsilon_{c,h}]`. Valid when: Valid when the heat-kernel endpoint box and source line are fixed, and the eighth source derivative bound is cutoff-uniform.
- finite endpoint gate interval: `I_{\rm gate}=M_G+C_N\sum_c D_c[\kappa_c^-,\kappa_c^+]+[-T_{\rm tail},T_{\rm tail}],\quad D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}`. Valid when: Applies after source-equivalent endpoint classes are aggregated before clipping, with Wilson one-body factors and straight ff contacts already canceled.
- root-quartic analytic screen: `\kappa_c=-\frac{t_c^4}{60}\{N\operatorname{tr}L_c^4+3(\operatorname{tr}L_c^2)^2\}+E_c,\quad |E_c|\le\varepsilon_c`. Valid when: Requires small heat-kernel endpoint coordinates in one SU(N) chart, with the remainder bounded uniformly before cutoff removal.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel plaquette-sheet SU(N) endpoint boxes with source-deformed Wilson flux partition functions Z_c(s).; target object: finite post-H,K reflected-Wilson OS transfer scalar for the fixed three-hairpin block.; Model: four-dimensional SU(N) lattice YM with heat-kernel plaquette action on finite endpoint boxes..
- Lock the finite H,K hairpin block, then aggregate endpoint boxes by equal heat-kernel source data; signed incidences b_ij,c are summed before clipping.
- Define kappa_c by the connected log source derivative; Wick-square Gram terms drop out and straight f f contacts cancel by the null-channel incidence identity.
- Insert the SU(N) root-quartic screen and interval remainder into I_gate; D_c<=0 classes are protective for the negative leading cumulant, while D_c>0 classes are dangerous.
- Decision rule: I_gate^->=0 promotes this finite block, I_gate^+<0 gives a same-theory falsifier, and a straddling interval preserves quarantine.

Blocking gap: No cutoff-uniform numerical or analytic intervals are yet supplied for positive-D endpoint source classes and T_tail.

## Falsifiers

- A positive-D endpoint class has certified kappa_c<0 large enough that I_gate^+<0; this is a finite same-theory falsifier.
- The tail T_tail is not uniform in cutoff or volume, so the endpoint screen cannot be valid in the collar limit.
- Endpoint collapse requires a boundary counterterm or altered Wilson normalization, breaking the same-theory condition.
- Source-equivalent aggregation fails because equal regulated source data do not persist under refinement of the heat-kernel endpoint box.

## Learning

Conceptual pressure: sign-certify endpoint collapse in the same Wilson theory. Raw R is too weak, raw kappa_4 spectra too strong, and global Schur preimage too coarse. C_ep is sharp because only positive-D leakage times a connected cumulant witness plus uniform tail can decide the finite gate.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch is looping without endpoint data; a concrete heat-kernel endpoint source probe is needed to test the finite gate rather than restating OS closed-cone logic.
- Situation seed: Fixed SU(N) heat-kernel plaquette-sheet three-hairpin endpoint box, with one source-equivalent class carrying a connected cumulant witness kappa_c.
- Varied variable: eta=(b13+b23)/b12, so D=2b12(1-2 eta) varies through the half-overlap shield.
- Held-fixed controls: Locked H,K finite hairpin block and Feshbach null vector., Same gauge-invariant Wilson algebra and heat-kernel regulator., No boundary counterterm, no new boundary Hilbert sector, and fixed one-body Wilson normalization., Uniform source-stencil error and T_tail budget.
- Expected observation: For eta>=1/2, negative root-quartic kappa is protective; for eta<1/2, the interval can cross zero only if positive-D leakage and tail exceed M_G.
- Transfer certificate needed: A cutoff-uniform source-stencil interval for kappa_c and T_tail, plus equality of regulated source data for every aggregated endpoint class.

## Next Experiment

Run proof search for uniform source-stencil bounds, then evaluate the heat-kernel endpoint connected cumulant witness for positive-D classes; report I_gate interval or keep quarantine.

# Annular Ward-Hessian certificate for the H,K endpoint R term

## Candidate Lemma

If the Ward/cusp-subtracted connected four-curvature kernel has a certified dyadic plateau ratio q_J<1, then R_{++}^{ren} has a valid lower interval; positivity above L_+ promotes finite endpoint-box positivity after H,K.

## Definitions

- source object: centered flowed SU(N) Wilson hairpin covariance kappa_2(W_H^c,W_K^c) at lattice spacing a and flow time t.
- target object: finite H,K endpoint-box Schur-Feshbach plus-channel matrix with leakage scalar L_+.
- controlled interface: recovery map from raw Wilson hairpins to oriented endpoint sheet currents with cumulant error E_rec.
- same-theory condition: source and target use the same Wilson action, same N, same flow-time family, and no imported continuum theory.
- carrier: endpoint sheet currents; raw Wilson contours are fragmented, while global OS or non-Gaussian witness routes are too coarse for this finite obstruction.
- morphism: contours -> sheet currents preserving gauge, color, reflection, orientation, cutoff locality, and zero-pairing equivalence.
- efficient representation: encode H,K sheets, endpoint moments, sector kernels, counterterms, E_rec, and L_+; primitives are Ward subtraction, Taylor Hessians, annular tails, and intervals.
- local value: changes only finite endpoint-box positivity after H,K; Clay existence, OS positivity, observable density, large-field control, and mass gap remain untouched.

## Assumptions

- Model: four-dimensional hypercubic Wilson lattice SU(N) with gradient-flowed Wilson observables before any continuum claim.
- Regime: endpoint box radius eps, flow radius sqrt(8t)<eps, and dyadic annuli separated from the cusp cells.
- Cutoff: annular Hessian bounds, Ward subtraction, and recovery error are uniform for a below a_0 at fixed physical endpoint geometry.
- Same-theory: the cumulant, counterterms, sheet-current quotient, and Schur-Feshbach matrix are computed in one cutoff family.
- Validity: plus-channel endpoint currents have zero monopole and dipole moments after H,K symmetrization.
- Constraint: no claim of OS reconstruction, nontrivial continuum limit, gauge-invariant observable density, or spectral gap follows from the lemma.

## Equations

- R-decomposition: `R_{++}^{ren}=g_t^4(N^2-1)\{2G_{++}-N C_{4,++}^{WS}\}-E_{rec}`. Valid when: Valid when centered flowed hairpins are recovered as endpoint sheet currents with Ward and cusp counterterms fixed.
- annular-Hessian-bound: `C_{4,++}^{WS}\le M_{2,+}^2\left(H_{\le J}^{+}+\frac{H_J^{+}}{1-q_J^{+}}\right),\quad q_J^{+}<1`. Valid when: Applies after plus-channel monopole and dipole cancellation on all cells outside the near annulus.
- dominance-margin: `\Delta_R^-:=g_t^4(N^2-1)\left[2G_{++}^- -N M_{2,+}^2\left(H_{\le J}^+ +\frac{H_J^+}{1-q_J^+}\right)\right]-E_{rec}^+-L_+`. Valid when: Requires the same-theory lower pair interval, upper C4 interval, recovery bound, and finite Feshbach leakage.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: centered flowed SU(N) Wilson hairpin covariance kappa_2(W_H^c,W_K^c) at lattice spacing a and flow time t.; target object: finite H,K endpoint-box Schur-Feshbach plus-channel matrix with leakage scalar L_+.; Model: four-dimensional hypercubic Wilson lattice SU(N) with gradient-flowed Wilson observables before any continuum claim..
- Expand kappa_2(W_H^c,W_K^c) after flow; disconnected products and one-hairpin perimeter/cusp pieces cancel, leaving a positive pair term and connected C4 polarization.
- Push H,K contours through the recovery morphism to endpoint sheet currents; plus-channel symmetry gives zero total charge and zero first moment.
- Taylor expand the Ward-subtracted C4 kernel on dyadic annuli; the first surviving term is bounded by M_{2,+}^2 times a mixed-Hessian interval.
- Compress the far tail by the certified plateau ratio q_J^+ and insert the resulting R_{++}^{ren} lower interval into the Schur-Feshbach margin against L_+.

Blocking gap: Need outward-rounded certified intervals for H_{<=J}^+, H_J^+, q_J^+, G_{++}^-, and E_rec^+ in the same Wilson-flow regulator.

## Falsifiers

- falsifier: a Ward or cusp counterterm leaves an O(eta) monopole/dipole residual, invalidating the Hessian bound.
- falsifier: the annular ratio q_J^+ is >=1 or lacks a cutoff-uniform plateau, so the tail cannot be summed.
- falsifier: the certified margin Delta_R^- is nonpositive after E_rec and L_+ are included.
- falsifier: zero-pairing quotienting changes the centered Wilson cumulant, breaking the same-theory recovery map.

## Learning

Conceptual pressure: finite Schur-Feshbach positivity needs a same-theory Wilson mediator. The sharp value signal is that R_{++} is reduced to an annular plateau dominance margin with color factors and recovery errors; success promotes one finite endpoint gate, failure quarantines it, and all Clay gates remain unclaimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the finite Route A endpoint mediator.`
- Rationale: The branch is blocked by a concrete sign/size question for connected boundary-OPE polarization, not by missing OS vocabulary.
- Situation seed: Flowed SU(N) Wilson lattice with fixed H,K endpoint hairpins, endpoint sheet currents, Ward/cusp subtraction, and dyadic annuli around one endpoint box.
- Varied variable: rho=sqrt(8t)/eps, the flow-radius to endpoint-box ratio.
- Held-fixed controls: same Wilson action, N, H,K geometry, and plus-channel normalization, same recovery map, counterterm prescription, outward-rounded interval arithmetic, and leakage L_+, finite endpoint-cell partition and certified zero-pairing quotient policy
- Expected observation: A stable rho window should give q_J^+<1 and a Delta_R^- interval whose sign is insensitive to one annular refinement; sign loss quarantines the R repair.
- Transfer certificate needed: Cutoff-uniform Ward identities, recovery error bounds, annular Hessian intervals, and a proof that the flowed cumulant remains a same-theory nontriviality witness boundary object.

## Next Experiment

Route to proof search: compute outward-rounded annular plateau intervals for the connected cumulant witness R_{++}, varying rho only, and demote on Ward, plateau, same-theory, or dominance falsifier.

# Raw signed-orbit K4 interval gate for post-H,K endpoint PSD

## Candidate Lemma

In a finite same-regulator H,K endpoint box, certified signed-orbit K4 intervals satisfying the diagonal or two-sparse phase gate give a valid stress vector with negative Rayleigh quotient for U_sigma. Survival is inconclusive and forces full Delta_raw proof search.

## Definitions

- source object: heat-kernel regulated finite SU(N) lattice YM endpoint Wilson data Q_i with vacuum-subtracted connected plaquette cumulants.
- target object: finite Hermitian Schur-corrected endpoint matrix U_sigma=R_sigma-S_HK,sigma whose PSD is the Route A endpoint gate.
- controlled interface: signed-orbit raw plaquette cumulant recovery map from oriented plaquette-quadruple intervals to D_i^+ and L_ij(theta).
- same-theory condition: identical cutoff, volume, heat-kernel sigma, coupling, Wilson basis, quotient identities, OPE window, and H,K Schur data.
- connected cumulant witness: R_ij,sigma=cum_2(Q_i,Q_j), with vacuum and perimeter factors removed before K4 extraction.
- carrier audit: scalar R is too weak, A012 shells are sign-losing, OS Hilbert observable algebra is too strong for this finite gate.

## Assumptions

- Model: finite-volume SU(N) lattice Yang-Mills with heat-kernel plaquette regulator and fixed reflected endpoint boxes.
- Cutoff: a,L,sigma are fixed, sigma/a lies in the boundary-OPE window, and no continuum uniformity is claimed.
- Same-theory: Gaussian covariance, K4 intervals, OPE error, and S_HK are computed from one regulated Wilson measure.
- Validity: orbit quotienting preserves orientation, color trace, transporter class, Hermitian conjugation, and exact Wilson identities.
- Local: the result changes only finite Route A endpoint PSD; OS positivity, gauge-invariant observable density, and the Clay mass gap remain untouched.

## Equations

- raw-connected-polarization: `R_{ij,\sigma}=\operatorname{cum}_2(Q_i,Q_j)=\alpha_N g_\sigma^4G_{ij,\sigma}+\frac{g_\sigma^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when Q_i are vacuum-subtracted heat-kernel endpoint Wilson fluxes and the connected cumulant removes vacuum and perimeter factors before boundary OPE expansion.
- signed-orbit-K4-lower: `\underline K^{(4)}_{ij,\sigma}(\theta)=\sum_{\mathcal O\subset(i,j)}m_{\mathcal O}\inf_{z\in I_{\mathcal O,\sigma}}\Re(e^{-i\theta}\chi_{\mathcal O}z)`. Valid when: Applies when raw plaquette quadruples are grouped only by exact Wilson symmetries preserving orientation, color trace, transporter class, and Hermitian conjugation.
- two-sparse-stress-gate: `U_\sigma=R_\sigma-S_{HK,\sigma};\quad D_i^+=\overline U_{ii};\quad L_{ij}=\underline{\Re(e^{-i\theta}U_{ij})};\quad D_i^+<0\lor(D_i^+,D_j^+>0\land L_{ij}^2>D_i^+D_j^+)\Rightarrow U_\sigma\not\succeq0`. Valid when: Requires a finite Hermitian endpoint compression after same-theory Schur subtraction, with certified interval upper diagonals and phase lower off-diagonals.

## Attempted Derivation

- Conceptual pressure: mediate raw connected Wilson cumulants to Schur-corrected finite endpoint PSD; gauge-invariant observable density is too strong and circular here.
- Use connected cumulant cancellation in the heat-kernel regulator: vacuum and perimeter terms drop, leaving the Gaussian color square, raw K4, and OPE error.
- Replace sign-losing A012 shells by signed raw orbits; exact quotienting keeps phases, Hermiticity, gauge invariance, and same-theory normalization.
- Compress U_sigma to span{e_i,e_j}; diagonal upper intervals and one phased off-diagonal lower interval yield the Rayleigh stress gate.

Blocking gap: No validated same-regulator signed-orbit K4 interval table I_{O,sigma} for the concrete H,K endpoint geometry is yet present.

## Falsifiers

- falsifier: a certified D_i^+<0 gives e_i^*U_sigma e_i<0 and kills finite endpoint PSD.
- falsifier: a phase with L_ij(theta)^2>D_i^+D_j^+ gives a two-sparse negative Rayleigh quotient.
- falsifier: non-invariant orbit quotienting changes a phase or transporter class, making L_ij invalid.
- falsifier: OPE overflow or missing raw K4 intervals demotes signed-orbit search to quarantine or full Delta_raw proof search.

## Learning

Cycle 337 attacks the missing mediator from raw Wilson K4 data to finite endpoint PSD. The sharp value signal is a valid signed-orbit stress falsifier: it unifies Gaussian color positivity, non-Gaussian K4, OPE error, and Schur hairpin energy while leaving Clay gates untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe for finite Route A, not as continuum evidence.`
- Rationale: The branch is looping unless raw signed-orbit K4 intervals are produced; theta-stress can demote the H,K endpoint route from few same-theory numbers.
- Situation seed: Finite SU(3) heat-kernel lattice endpoint box with the worked H,K collar/hairpin Wilson basis; enumerate signed K4 plaquette orbits for one endpoint pair p,q.
- Varied variable: phase theta used in the two-sparse Rayleigh stress lower bound L_pq(theta).
- Held-fixed controls: cutoff a, finite volume L, heat-kernel sigma, and coupling g_sigma, same endpoint Wilson basis, exact quotient identities, OPE error budget, and S_HK Schur block
- Expected observation: A phase sector either gives L_pq(theta)^2>D_p^+D_q^+ and a finite falsifier, or all phases survive and force full Delta_raw PSD search.
- Transfer certificate needed: Validator-certified interval arithmetic for every signed orbit, with exact Wilson quotient audit and same-regulator recovery of Gaussian, K4, OPE, and Schur terms.

## Next Experiment

Proof search: build the validator-facing connected cumulant witness table I_{O,sigma} for one H,K endpoint pair, compute D_i^+,D_j^+,L_ij(theta), and test the stress gate; OS Hilbert observable algebra remains a non-claim.

