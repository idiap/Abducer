# cycle-0251

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Endpoint kappa_4 scalar certification for the post-H,K Wilson block

## Candidate Lemma

For the heat-kernel plaquette-sheet regulator, the post-H,K null-channel endpoint contribution is a same-theory scalar fourth source derivative of the endpoint-box log partition function. A seven-point central stencil gives a certified interval for this connected kappa_4 term with error 7 h^4 M_8/240; the valid promotion or falsifier test is the sign of the interval for M_G+R_end.

## Definitions

- source object: heat-kernel regulated endpoint box Z_v(s) for the plaquette sheet, with localized singlet source s Xi_v obtained from the Feshbach null incidence alpha=(1,1,-2) and parallel-transported endpoint plaquette fluxes.
- target object: the scalar post-H,K Schur-Feshbach endpoint correction S_null=M_G+R_end+Tail for the locked three-hairpin Wilson OS block.
- controlled interface: replace the connected boundary-OPE polarization R in the null channel by same-regulator endpoint source derivatives of log Z_v, preserving the Wilson collar normalization already used for H and K.
- same-theory condition: the source is only a derivative probe at s=0 of the original heat-kernel Wilson measure; no boundary counterterm, altered Wilson-loop renormalization, or enlarged observable algebra is introduced.
- X_v=<Xi_v,F_v> is the singlet endpoint flux insertion; F_v denotes plaquette curvatures parallel transported to v.
- M_G is the already certified positive Gaussian Schur-Feshbach margin after the H,K computation; it is not recomputed in this cycle.

## Assumptions

- The regulator is the reflection-positive heat-kernel plaquette action on a fixed endpoint box B_v before the continuum limit.
- The localized source keeps log Z_v(s) C^8 for |s|<=3h, with a certified bound M_{8,v} on |d^8/ds^8 log Z_v(s)|.
- Endpoint boxes cover all corners where the reflected hairpin sheets meet the boundary; the complement is controlled by a tail bound E_tail.
- Straight boundary-edge incidences satisfy the null identity for alpha, so the local C_A f f contact has zero null-channel contraction.
- The connected log partition function is used, so disconnected Wick-square contributions are not counted inside kappa_v; their remaining Gram part is nonnegative and safe.

## Equations

- endpoint source derivative: `f_v(s)=\log Z_v(s),\qquad \kappa_v(\alpha)=f_v^{(4)}(0)=\langle X_v^4\rangle_{c,v}`. Valid when: Valid when the endpoint source is localized inside one heat-kernel plaquette box and differentiated at s=0.
- straight ff contact cancellation: `R_{ff,null}=c_a C_A T_F\sum_{e\subset\partial B_v}\left(\sum_{r=1}^3\alpha_r\eta_{r,e}\right)^2=0`. Valid when: Valid when the three hairpin footprints have the same oriented straight-edge incidence used in the H,K block.
- seven point fourth derivative stencil: `D_h f_v=\frac{-f_v(3h)+12f_v(2h)-39f_v(h)+56f_v(0)-39f_v(-h)+12f_v(-2h)-f_v(-3h)}{6h^4}`. Valid when: Valid when log Z_v is evaluated at the seven same-theory source strengths 0, plus or minus h, 2h, and 3h.
- stencil remainder: `|\kappa_v(\alpha)-D_h f_v|\le \frac{7}{240}h^4 M_{8,v}`. Valid when: Valid when the eighth source derivative of log Z_v is bounded throughout the interval |s|<=3h.
- certified endpoint interval: `\mathcal I_{end}=\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v\omega_v\,[D_hf_v-\epsilon_v,D_hf_v+\epsilon_v]+[-E_{tail},E_{tail}],\qquad \epsilon_v=\frac{7}{240}h^4M_{8,v}`. Valid when: Valid when endpoint weights omega_v encode the actual null-channel orientation and all non-endpoint contributions are included in E_tail.
- promotion and falsifier sign test: `\inf(M_G+\mathcal I_{end})>0\Rightarrow \text{promote},\qquad \sup(M_G+\mathcal I_{end})<0\Rightarrow \text{falsifier}`. Valid when: Valid when M_G is the previously normalized Schur-Feshbach margin and the interval encloses every endpoint and tail error.

## Attempted Derivation

- Contract the post-H,K endpoint boundary OPE with the Feshbach null vector alpha=(1,1,-2), so only the scalar null-channel polarization is needed.
- Use the connected log Z_v(s) to identify the irreducible endpoint cumulant as kappa_v(alpha)=d^4/ds^4 log Z_v(s)|_{0}=<X_v^4>_c.
- Check cancellations before estimating signs: the fourth connected derivative removes disconnected Wick-square pieces, and the null incidence identity kills the straight C_A f f boundary contact.
- Solve the symmetric seven-point moment equations for a fourth derivative stencil: c0+2(c1+c2+c3)=0, c1+4c2+9c3=0, 2(c1+16c2+81c3)=24, and c1+64c2+729c3=0. This gives c0=28/3, c1=-13/2, c2=2, c3=-1/6.
- The eighth-moment residue is 2(c1+256c2+6561c3)/8!=-7/240, hence |kappa_v-D_h f_v|<=7h^4 M_{8,v}/240.
- Insert the color/geometric factor (g_a^4/4)(T_F/N)^2, endpoint orientation weights omega_v, and the tail interval to form I_end. The valid finite-block decision is now interval arithmetic on M_G+I_end.

Blocking gap: No actual endpoint-box values f_v(±h), f_v(±2h), f_v(±3h), no sharp M_{8,v}, and no certified E_tail have been computed for the Yang-Mills endpoint geometry.

## Falsifiers

- Certified upper endpoint interval sup(M_G+I_end)<0; this is the direct finite-block falsifier for same-theory OS positivity in the post-H,K null channel.
- Failure of the straight-edge incidence identity after parallel transport conventions are fixed; then the C_A f f contact was wrongly canceled.
- A nonzero boundary counterterm is needed to define Z_v(s) or its fourth derivative; this breaks the same-theory condition even if the modified matrix is positive.
- The eighth-derivative or tail bounds diverge so strongly under cutoff removal that no valid continuum endpoint interval survives.
- Endpoint character truncation reveals a large negative connected kappa_4 contribution exceeding the Gaussian margin for every admissible h.

## Learning

Cycle 251 turns the scalar endpoint-kappa_4 plan into an exact certified stencil. The new contribution is the explicit seven-point fourth-derivative formula, its 7h^4 M_8/240 error, and the interval sign test for the post-H,K endpoint term. The regulator is the heat-kernel plaquette sheet; the cumulant is <X_v^4>_c from log Z_v; the cancellations are connected Wick-square removal and straight C_A f f null-incidence cancellation. The branch is not looping, but it now needs actual endpoint-box data or a sharp analytic M_8/tail estimate.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute one actual endpoint topology: choose h, evaluate log Z_v(s) for s=0, ±h, ±2h, ±3h using the SU(N) heat-kernel character expansion, bound M_8 and E_tail, and report the certified interval for M_G+R_end.
