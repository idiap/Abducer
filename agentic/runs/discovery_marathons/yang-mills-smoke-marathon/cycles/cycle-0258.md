# cycle-0258

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Post-H,K endpoint-box incidence bound for connected Wilson R

## Candidate Lemma

For the locked three-hairpin Wilson collar block, the post-H,K connected endpoint polarization is controlled by a signed endpoint incidence imbalance. After Wick-square removal and straight f f cancellation, a negative compact-group kappa_4 is dangerous only on endpoint boxes where the 12 incidence dominates the 13 and 23 incidences by the Feshbach null weights.

## Definitions

- source object: heat-kernel plaquette-sheet regulated SU(N) Wilson collar observables W_i(a,delta) for the already-fixed three-hairpin block, with endpoint boxes B_v(r) around hairpin corners.
- target object: the corrected Schur-Feshbach null-channel scalar M_nu=M_G+R_nu^{end}+R_nu^{tail} whose positivity promotes the post-H,K OS bridge for this finite block.
- controlled interface: the boundary OPE map sending reflected Wilson products to singlet connected four-flux endpoint cumulants kappa_v, with color factor c_N=(g_a^4/4)(T_F/N)^2 and uniform endpoint-tail remainder.
- same-theory condition: the heat-kernel regulator, Wilson normalization, collar embeddings, endpoint sources, and cutoff-removal topology are the locked Yang-Mills ones, with no added boundary counterterm or algebra enlargement.
- G_{ij,v} is the squared geometric/color incidence of the endpoint source in box B_v for the reflected pair (i,j), after singlet projection.
- D_v:=2G_{12,v}-4G_{13,v}-4G_{23,v} is the Feshbach-null endpoint imbalance; D_v^+=max(D_v,0).
- kappa_v is the fourth derivative at zero of log Z_v(su_v), hence the connected fourth cumulant of the endpoint Wilson flux source.

## Assumptions

- Model: four-dimensional Euclidean SU(N) Yang-Mills is regulated by lattice heat-kernel plaquette sheets with gauge-invariant Wilson observables only.
- Regime: endpoint boxes are disjoint, smaller than the collar scale, and large enough to contain the local hairpin endpoint OPE support.
- Uniformity: the fourth-cumulant OPE and the endpoint-tail estimate are uniform in a, delta, and box radius along the chosen continuum passage.
- Cancellation input: connected logarithms remove Wick-square Gram terms from the dangerous scalar, and the straight C_A f f contact cancels by the null incidence identity of the three-hairpin block.
- Sign input: the compact-group small-time endpoint cumulant has certified interval kappa_v<=0, or else the bound is interpreted with the full interval for kappa_v.
- Non-claim boundary: this lemma only handles the endpoint-local R contribution after H,K are known; it does not prove the full Clay mass gap or continuum existence.

## Equations

- endpoint_R_pair_decomposition: `R_{ij}^{\mathrm{end}}=c_N\sum_{v\in E}\kappa_v\,G_{ij,v}+\tau_{ij},\qquad c_N=\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Valid when heat-kernel plaquette sheets are localized in disjoint endpoint boxes and the singlet four-flux boundary OPE has a uniform tail remainder.
- null_endpoint_contraction: `R_{\nu}^{\mathrm{end}}=2R_{12}^{\mathrm{end}}-4R_{13}^{\mathrm{end}}-4R_{23}^{\mathrm{end}}=c_N\sum_{v\in E}\kappa_vD_v+\tau_\nu,\quad D_v=2G_{12,v}-4G_{13,v}-4G_{23,v}`. Valid when: Applies after the finite Schur-Feshbach null vector is fixed and one-body, length-linear, Wick-square, and straight f f contributions have been cancelled.
- safe_interval_gate: `\underline M_\nu:=M_G-c_N\sum_{v\in E}\kappa_v^-D_v^+-|\tau_\nu|,\qquad \underline M_\nu>0\Rightarrow M_\nu>0`. Valid when: Valid when each endpoint cumulant interval satisfies kappa_v in [-kappa_v^-,0] and the tail bound controls every omitted corner and off-box contribution.
- endpoint_falsifier_gate: `\overline M_\nu:=M_G+c_N\sum_{v\in E}[\kappa_vD_v]^{\sup}+[\tau_\nu]^{\sup},\qquad \overline M_\nu<0\Rightarrow \text{same\mbox{-}theory falsifier}`. Valid when: Requires certified interval arithmetic for the same regulated endpoint cumulants and no change of Wilson normalization between collar and target observables.
- seven_point_kappa4_stencil: `\widehat\kappa_v(u)=\frac{-f(-3h)+12f(-2h)-39f(-h)+56f(0)-39f(h)+12f(2h)-f(3h)}{6h^4},\quad f(s)=\log Z_v(su)`. Valid when: Valid when log Z_v is analytic for |s|<=3h and the eighth source derivative is bounded on that same endpoint box interval.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel plaquette-sheet regulated SU(N) Wilson collar observables W_i(a,delta) for the already-fixed three-hairpin block, with endpoint boxes B_v(r) around hairpin corners.; target object: the corrected Schur-Feshbach null-channel scalar M_nu=M_G+R_nu^{end}+R_nu^{tail} whose positivity promotes the post-H,K OS bridge for this finite block.; Model: four-dimensional Euclidean SU(N) Yang-Mills is regulated by lattice heat-kernel plaquette sheets with gauge-invariant Wilson observables only..
- Start with the already-proved finite Schur-Feshbach reduction for the three-hairpin block and keep only the post-H,K connected polarization scalar in the null direction.
- Represent each R_{ij} by heat-kernel plaquette-sheet source derivatives of log Z for the reflected Wilson product; the connected logarithm removes Wick-square disconnected contractions from the dangerous term.
- Use the previously established null incidence identity to cancel straight-segment nonabelian C_A f f contacts; only endpoint and corner boxes remain.
- Project each endpoint four-flux source to the singlet channel. This gives the color factor c_N=(g_a^4/4)(T_F/N)^2 and endpoint cumulants kappa_v contracted with incidences G_{ij,v}.
- Contract with the Feshbach null pair weights 2,-4,-4. The endpoint imbalance is D_v=2G_{12,v}-4G_{13,v}-4G_{23,v}.
- Since the compact-group small-time kappa_4 is negative, only D_v>0 can make the endpoint contribution negative. Thus 12-dominance, not generic endpoint negativity, is the actual falsifier mechanism.
- Split D_v into positive and negative parts and combine the negative part with the positive Gaussian margin M_G to obtain a certified interval gate for M_nu.

Blocking gap: The actual endpoint incidence table G_{ij,v} and the same-theory tail interval tau_nu have not yet been computed for the full regulated hairpin geometry.

## Falsifiers

- A certified interval overline M_nu<0 from the same heat-kernel endpoint sources is a direct same-theory falsifier of the finite block.
- The straight C_A f f contact could fail to cancel after the real endpoint orientations are inserted, invalidating the incidence-only reducer.
- Endpoint-box overlap could create a nonlocal connected cumulant not bounded by tau_nu, defeating the local OPE interface.
- The compact-group kappa_4 interval could include a positive component large enough to nullify the 12-dominance interpretation.
- A boundary counterterm or Wilson renormalization change needed to define Z_v would violate the same-theory condition.

## Learning

Cycle 258 computes the sign mechanism of the remaining post-H,K R term. The negative compact-group endpoint kappa_4 is not by itself a danger; after the valid cancellations, it is multiplied by D_v=2G12-4G13-4G23. Equal endpoint boxes are safe. The conceptual value signal is sharpness: the branch has localized the only remaining demotion mechanism to certified 12-endpoint dominance or a negative tail, a route-changing reduction from abstract OS positivity to finite endpoint source intervals.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has passed H,K and reduced the remaining obstruction to endpoint kappa_4; another abstract OS restatement would loop, while varying endpoint incidence directly tests the promotion/falsifier gate.
- Situation seed: A heat-kernel SU(N) plaquette-sheet three-hairpin Wilson block with disjoint endpoint boxes, fixed Feshbach null vector, and source derivatives f_v(s)=log Z_v(su_v) evaluated by the seven-point fourth-derivative stencil.
- Varied variable: Endpoint dominance ratio d=\sum_v G_{12,v}/(\sum_vG_{13,v}+\sum_vG_{23,v}) while keeping the total endpoint box scale and source norm fixed.
- Held-fixed controls: Same regulated Yang-Mills heat-kernel action and gauge-invariant Wilson algebra., Already computed H,K block and corrected Schur-Feshbach margin M_G., Null pair weights 2,-4,-4 and the straight f f cancellation identity., Uniform endpoint-box radius, singlet projection, and finite-difference error bound.
- Expected observation: For d near 1 the negative compact-group kappa_4 raises or preserves M_nu; demotion begins only past a 12-dominance threshold determined by M_G, c_N, |kappa|, and the tail interval.
- Transfer certificate needed: A uniform endpoint OPE remainder plus same-theory cutoff-removal certificate showing that the finite source derivative intervals converge to the Wilson collar R_nu without boundary counterterms.

## Next Experiment

Compute the real endpoint table G_{12,v}, G_{13,v}, G_{23,v} for the three hairpins, then evaluate seven same-theory source values f_v(kh) per endpoint box to certify kappa_v and the interval sign of M_nu.
