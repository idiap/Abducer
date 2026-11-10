# cycle-0259

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Post-H,K endpoint-box clipping for reflected Wilson hairpins

## Candidate Lemma

After the three-hairpin H,K gate is fixed, the remaining connected boundary-OPE polarization is controlled by a clipped endpoint half-dominance quantity. In heat-kernel plaquette-sheet regulation, negative compact-group fourth cumulants are dangerous only at endpoint boxes with D_v=2G12(v)-4G13(v)-4G23(v)>0, equivalently eta_v=(G13+G23)/G12<1/2. Thus equal or symmetric endpoint boxes promote the block; only certified 12-dominance or a negative tail can be a falsifier.

## Definitions

- source object: regulated SU(N) heat-kernel plaquette-sheet Wilson three-hairpin collar block with endpoint boxes v, singlet fourth flux cumulants, and fixed color normalization T_F/N.
- target object: the post-H,K Schur-Feshbach null-channel scalar whose positivity decides same-theory OS positivity for this finite Wilson block.
- controlled interface: contraction of the connected endpoint Wilson cumulant with the Feshbach null vector a=(1,1,-2), represented by endpoint overlap entries G_ij(v).
- same-theory condition: the same heat-kernel Wilson observable algebra, loop renormalization, endpoint partition functions, and color conventions are used for the collar limit and the intended quotient matrix; no boundary counterterm is inserted.
- M_G is the positive Gaussian Schur-Feshbach margin already left after PHP and the corrected second-order form.
- beta_v=-kappa_{4,v}^{sing} is the positive magnitude of the local compact-group fourth cumulant in endpoint box v.
- T_a is the residual endpoint/corner tail after removing Wick-square Gram terms and the straight f f contact.

## Assumptions

- Model: four-dimensional Euclidean SU(N) Yang-Mills approximated by heat-kernel plaquette sheets before cutoff removal.
- Regime: endpoint boxes are smaller than the collar scale but larger than the plaquette cutoff, so local heat-kernel cumulant expansion is uniform.
- Uniformity: the eighth-source-derivative bound controlling endpoint stencils is summable over endpoint boxes.
- Cancellation: connected logarithms remove Wick-square disconnected terms, and the null incidence identity removes straight C_A f f contacts on shared straight segments.
- Same-theory condition: Wilson loops are not reweighted at the reflection plane and the endpoint source derivatives are evaluated in the locked gauge-invariant algebra.

## Equations

- endpoint scalar decomposition: `\mathcal S_{\rm end}=M_G+\mathcal R_{\rm end},\qquad \mathcal R_{\rm end}=-\alpha_a\sum_{v}\beta_v D_v+\mathcal T_a,\quad \alpha_a={g_a^4\over4}\left({T_F\over N}\right)^2`. Valid when: Applies after heat-kernel plaquette-sheet regularization, after H,K are fixed, and after Wick-square plus straight-contact cancellations are valid.
- incidence polarization: `D_v=2G_{12}(v)-4G_{13}(v)-4G_{23}(v)=2G_{12}(v)\bigl(1-2\eta_v\bigr),\qquad \eta_v={G_{13}(v)+G_{23}(v)\over G_{12}(v)}`. Valid when: Valid when G12(v) is nonzero and endpoint overlaps are computed from the same null-channel Wilson incidence table.
- clipped promotion bound: `\mathcal S_{\rm end}\ge M_G-\alpha_a\sum_v\beta_v[D_v]_+-|\mathcal T_a|`. Valid when: Requires beta_v nonnegative for the compact-group endpoint cumulant and a certified absolute bound on all endpoint and corner tails.
- interval falsifier test: `M_G-\underline{\alpha_a\sum_v\beta_v[D_v]_+}+\overline{\alpha_a\sum_v\beta_v[-D_v]_+}+\overline{\mathcal T_a}<0\ \Longrightarrow\ \mathcal S_{\rm end}<0`. Valid when: Valid for interval arithmetic whose lower and upper bounds enclose the regulated endpoint source derivatives before continuum extrapolation.

## Attempted Derivation

- Conceptual pressure attacked: the branch must decide the post-H,K endpoint R/kappa_4 term, not restate OS positivity or the earlier hairpin threshold.
- Start with the fixed three-hairpin null channel after the valid Schur-Feshbach correction; denote its remaining scalar by S_end=M_G+R_end with M_G>0.
- Use heat-kernel plaquette-sheet regulation and write R_end as a sum of endpoint-box connected fourth Wilson flux cumulants plus a corner tail.
- Connected log cumulants remove Wick-square Gram pieces; the null incidence identity cancels the straight-segment C_A f f commutator contact.
- The local compact-group fourth cumulant has sign kappa_4^{sing}=-beta_v with beta_v>=0 in the small heat-kernel endpoint box.
- Contracting with the null weights produces D_v=2G12(v)-4G13(v)-4G23(v); hence negative kappa_4 is harmful only where D_v>0.
- Separating D_v into positive and negative parts gives a valid clipped bound: only sum beta_v[D_v]_+ competes against M_G, while beta_v[-D_v]_+ is protective.
- Hard gate: produce certified intervals for beta_v, D_v, and T_a. Success promotes this finite Wilson block through the post-H,K handoff; failure by a negative interval gives an explicit same-theory OS falsifier.

Blocking gap: The actual endpoint incidence table B_v and uniform tail interval are still missing at proof level; the derivation gives the sharp scalar certificate but not the numerical or analytic endpoint-box bounds.

## Falsifiers

- A certified endpoint interval with eta_v<1/2 on enough beta_v mass and an upper bound making S_end<0 is a finite same-theory falsifier.
- A valid source-stencil computation showing a negative nonlocal corner tail larger than M_G demotes the endpoint-box route.
- If the straight f f contact fails to cancel after using the actual plaquette orientations, the clipped endpoint formula is invalid.
- If Wilson loop renormalization at the reflection plane changes the endpoint source algebra, the same-theory bridge is falsified even if the regulated matrix stays positive.

## Learning

Cycle 259 sharpens the remaining R problem: the negative compact-group endpoint kappa_4 is dangerous only after clipping by positive half-dominance D_v>0. Equal endpoint boxes are not merely harmless heuristically; they enter the protective part beta_v[-D_v]_+. The conceptual value signal is sharpness and route change: the proof state is now a finite interval problem for endpoint dominance and tails, not an abstract OS/Wilson obstruction ladder.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has already fixed H,K and reduced R to endpoint cumulants; another abstract restatement would loop. The concrete thought experiment tests the only remaining sign mechanism.
- Situation seed: Three reflected SU(N) Wilson hairpins in a heat-kernel plaquette-sheet regulator, with the fixed Feshbach null vector and endpoint boxes partitioned into symmetric boxes and pair-12-dominated boxes.
- Varied variable: Endpoint dominance ratio eta_v=(G13(v)+G23(v))/G12(v), varied from eta_v=1 for symmetric endpoints to eta_v=0 for pure 12 endpoints.
- Held-fixed controls: Same heat-kernel regulator and gauge-invariant Wilson test algebra on source and target sides., Fixed color normalization alpha_a=(g_a^4/4)(T_F/N)^2 and fixed post-H,K Gaussian margin M_G., Fixed collar geometry away from endpoint redistribution, so PHP and the corrected second-order gate are unchanged., No boundary counterterm, no altered Wilson loop renormalization, and no change of reflection plane.
- Expected observation: The endpoint contribution changes sign at eta_v=1/2. Symmetric endpoint boxes increase the margin, while sufficiently many pair-12-dominated boxes can overcome M_G and produce a determinant-level falsifier.
- Transfer certificate needed: Certified source-derivative intervals for beta_vD_v, a uniform bound on endpoint/corner tails, and a cutoff-stable incidence table before the thought experiment can alter proof obligations.

## Next Experiment

Build the endpoint incidence table for the actual three-hairpin plaquette-sheet geometry, compute D_v=2G12-4G13-4G23 per endpoint box, and run the seven-point source stencil only on boxes with D_v>0 first.
