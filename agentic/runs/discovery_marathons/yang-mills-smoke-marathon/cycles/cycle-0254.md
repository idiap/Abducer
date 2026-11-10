# cycle-0254

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Endpoint kappa_4 incidence bound for the post-H,K Wilson hairpin block

## Candidate Lemma

For the fixed three-hairpin block after H,K are known, the endpoint part of the connected boundary-OPE polarization is dangerous only through a signed endpoint-incidence dominance functional. If the compact-group fourth cumulant has the heat-kernel form kappa_4_v(b)=-chi_v B_v(b)+epsilon_v with chi_v>=0, then endpoint boxes with 2B_12,v<=4B_13,v+4B_23,v cannot demote the corrected Schur-Feshbach scalar. A valid falsifier must certify net 12-endpoint dominance large enough to exceed the positive Gaussian margin and all remainder/tail bounds.

## Definitions

- source object: heat-kernel plaquette-sheet regulated SU(N) Wilson endpoint boxes for the already fixed three-hairpin H,K block, with reflection collar width delta and lattice scale a.
- target object: the scalar post-H,K Schur-Feshbach null-channel endpoint contribution R_null that decides whether the positive Gaussian margin survives.
- controlled interface: extract R_null from diagonal-normalized reflected Wilson OS entries using connected log Z_v fourth source derivatives after Wick-square and straight f f cancellations.
- same-theory condition: the same heat-kernel Wilson sheet regulator, color representation, endpoint boxes, and diagonal normalization are used for H,K,R and no boundary counterterm or algebra enlargement is introduced.

## Assumptions

- The first-order PHP gate has the one-dimensional null vector z=(1,1,-2) for the fixed three-hairpin block.
- Heat-kernel endpoint localization separates straight shared-boundary contacts from endpoint/corner boxes with a uniform tail estimate E_tail.
- Disconnected Wick-square contractions are kept as positive Gram terms and are not counted as dangerous connected R.
- The straight nonabelian C_A f f contact has the same oriented incidence on the three entries, so the z-null incidence cancels it away from endpoints.
- For each endpoint box v, the singlet projected fourth cumulant has kappa_4_v(b)=-chi_v B_v(b)+epsilon_v with chi_v>=0 and certified epsilon_v.

## Equations

- null-channel weights: `z=(1,1,-2),\qquad z^{*}Rz=2R_{12}-4R_{13}-4R_{23}`. Valid when: Valid when the Schur-Feshbach null vector is the kernel direction of PHP for the fixed three-hairpin Wilson block.
- endpoint cumulant source: `\kappa_{4,v}^{\mathrm{sing}}(b)=\left.\partial_s^4\log Z_v(s;b)\right|_{s=0}=\langle X_{v,b}^4\rangle_{c,v}`. Valid when: Applies after heat-kernel plaquette-sheet localization isolates one endpoint box and the source b is gauge-singlet projected.
- endpoint R scalar: `R_{\mathrm{null}}^{\mathrm{end}}=C_{\mathrm{col}}\sum_v\{2\kappa_{4,v}(b_{12,v})-4\kappa_{4,v}(b_{13,v})-4\kappa_{4,v}(b_{23,v})\}+E_{\mathrm{tail}},\quad C_{\mathrm{col}}=\frac{g_a^4}{24}\left(\frac{T_F}{N}\right)^2`. Valid when: Requires diagonal normalization, connected logarithms, Wick-square cancellation, and null-incidence cancellation of straight nonabelian f f contacts.
- dominance variable: `\kappa_{4,v}(b_{ij,v})=-\chi_v B_{ij,v}+\epsilon_{ij,v},\qquad D_v=2B_{12,v}-4B_{13,v}-4B_{23,v}`. Valid when: Valid in the small endpoint-box heat-kernel regime where the root-Jacobian quartic term dominates the sixth-order remainder.
- safe endpoint bound: `S_{\mathrm{null}}\ge M_G-C_{\mathrm{col}}\sum_v\chi_v[D_v]_+-C_{\mathrm{col}}\sum_{v,ij}|w_{ij}|\,|\epsilon_{ij,v}|-|E_{\mathrm{tail}}|`. Valid when: Applies when the positive Gaussian Schur margin M_G has already been computed from H and K.

## Attempted Derivation

- Start with the Schur-Feshbach-reduced null scalar S_null=M_G+z^*Rz+tails for the fixed three-hairpin block, where z=(1,1,-2).
- Write z^*Rz as the weighted connected endpoint contribution with weights w_12=2, w_13=-4, w_23=-4 after diagonal normalization removes one-body Wilson factors.
- Use heat-kernel plaquette-sheet localization: straight shared-boundary contractions decompose into Wick-square Gram terms plus a local C_A f f contact. The Gram part is nonnegative, and the straight f f part cancels by the null incidence identity.
- The remaining local endpoint box v is described by F_v(s;b)=log Z_v(s;b). Its fourth source derivative is the singlet connected Wilson four-flux cumulant kappa_4_v(b).
- Insert the compact-group small-box expansion kappa_4_v(b)=-chi_v B_v(b)+epsilon_v. Since chi_v>=0, the only negative contribution to S_null comes from endpoint boxes with D_v=2B_12,v-4B_13,v-4B_23,v positive.
- This yields the valid bound S_null>=M_G-C_col sum_v chi_v[D_v]_+-remainder-tail. Equal disjoint endpoint boxes or boxes dominated by 13/23 incidence are safe rather than dangerous.

Blocking gap: The actual plaquette-sheet endpoint incidence table B_12,v,B_13,v,B_23,v and the uniform epsilon_v plus E_tail bounds have not yet been certified for the geometric three-hairpin collars.

## Falsifiers

- A regulator-level endpoint table with positive dominance C_col sum_v chi_v[D_v]_+ exceeding M_G plus all remainder and tail bounds is a concrete falsifier.
- A same-theory seven-point computation of kappa_4_v that gives a larger negative value than the root-quartic bound permits would demote the expansion.
- A failure of the straight C_A f f null-incidence cancellation at oriented corners would reintroduce a bulk connected R term not covered by the endpoint estimate.
- A boundary counterterm or changed Wilson normalization between H,K and R would invalidate the same-theory condition even if the finite matrix stayed positive.
- A tail estimate with negative sign and size comparable to M_G would prevent promotion despite safe local endpoint boxes.

## Learning

Cycle 254 shows that the negative compact-group endpoint kappa_4 is not automatically dangerous. In the actual null channel its pair weights are 2,-4,-4, so only certified 12-endpoint dominance can overcome the positive Schur-Feshbach margin. This is a sharper valid R/kappa_4 endpoint-box test and a concrete falsifier criterion, not another restatement of the Wilson/OS obstruction ladder.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Draw the regulated three-hairpin plaquette sheets, list all endpoint boxes, compute the singlet incidence norms B_12,v,B_13,v,B_23,v, then evaluate D_+=sum_v[2B_12,v-4B_13,v-4B_23,v]_+ and the seven-point kappa_4 intervals for the boxes with D_v>0.
