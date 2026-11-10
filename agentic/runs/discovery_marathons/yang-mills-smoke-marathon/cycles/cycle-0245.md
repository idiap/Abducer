# cycle-0245

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Endpoint-box kappa_4 spectral reduction for reflected Wilson hairpins

## Candidate Lemma

For the locked three-hairpin Wilson collar block, after the Wick-square Gram term and the straight f f contact are removed, the only post-H,K danger is the negative spectrum of a finite singlet-projected endpoint four-flux cumulant operator plus a tail. Thus R is reduced to a regulated endpoint eigenvalue estimate with an explicit color and incidence prefactor.

## Definitions

- source object: heat-kernel plaquette-sheet regulated reflected Wilson hairpins C_i(delta,a,epsilon), endpoint boxes E_v(r), and null coefficient w=(1,1,-2).
- target object: the same-theory OS quotient second-order scalar in the null channel after Schur-Feshbach elimination of the rank-one vacuum direction.
- controlled interface: extract the connected boundary-OPE polarization R from plaquette flux cumulants and compare its endpoint negative spectrum with the positive Gaussian margin M_G.
- same-theory condition: use the locked Wilson loop normalization, endpoint collaring, and cutoff-removal embedding; endpoint boxes localize the estimate but add no boundary counterterm or new observable.
- kappa_4 endpoint operator: the real self-adjoint operator K_v^sing on symmetric color-singlet two-flux tests A supported in E_v, obtained from the connected four-flux cumulant.
- negative spectral size: Lambda_-(v)=max(0,-lambda_min(K_v^sing)) in the endpoint-box test norm fixed by the heat-kernel plaquette covariance.
- geometric incidence: A_v(w)=sum_i w_i eta_{i,v} tensor_s eta_{i,v} and I_v(w)=||A_v(w)||_HS^2, computed from the oriented plaquettes entering the endpoint of each hairpin.

## Assumptions

- Heat-kernel plaquette-sheet regulation is reflection positive and has a gauge-invariant flux-source generating functional on each endpoint box.
- The H,K Schur-Feshbach gate is already locked and supplies a strictly positive null-channel Gaussian margin M_G before the irreducible endpoint kappa_4 term is inserted.
- The Wick-square four-flux contraction has been separated as a positive Gram contribution and is not used to create a falsifier.
- The straight-segment nonabelian f f contact cancels by the null incidence identity for the actual three-hairpin geometry; only endpoint/corner boxes and tails remain.
- Endpoint tails outside the chosen boxes admit a uniform same-theory bound T_tail(w) in the cutoff-removal regime.

## Equations

- endpoint cumulant extractor: `\kappa^{abcd}_{4,\epsilon}(p_1,p_2,p_3,p_4)=\left.\frac{\delta^4\log Z_{E_v,\epsilon}[J]}{\delta J^a_{p_1}\delta J^b_{p_2}\delta J^c_{p_3}\delta J^d_{p_4}}\right|_{J=0}`. Valid when: Valid when the endpoint box is regulated by heat-kernel plaquettes and the flux sources are gauge-covariantly parallel transported to a common endpoint frame.
- singlet connected endpoint R: `R^{\kappa_4}_{ij,v}=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\int_{E_v^4}\eta_{i,v}(x_1,x_2)\eta_{j,v}(x_3,x_4)\delta^{ab}\delta^{cd}\kappa^{abcd}_{4,\epsilon}(x_1,x_2,x_3,x_4)`. Valid when: Valid when the Wilson expansion is truncated to the connected four-flux endpoint term, with all four flux insertions supported inside one endpoint box.
- incidence norm: `A_v(w)=\sum_i w_i\,\eta_{i,v}\otimes_s\eta_{i,v},\qquad I_v(w)=\|A_v(w)\|_{HS}^2`. Valid when: Applies once the oriented endpoint plaquette incidences are fixed by the locked Wilson collars before taking the continuum limit.
- endpoint negative-spectrum bound: `\sum_{i,j}w_iw_jR^{\kappa_4}_{ij}\ge -\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v\Lambda_-(v)I_v(w)-|T_{tail}(w)|`. Valid when: Applies after the Wick-square Gram contraction is separated and the straight f f commutator contact cancels by the null incidence identity.
- promotion inequality: `M_{eff}=M_G-\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v\Lambda_-(v)I_v(w)-|T_{tail}(w)|>0`. Valid when: Valid when the corrected Schur-Feshbach H,K gate has already supplied a positive Gaussian margin M_G in the chosen null channel.

## Attempted Derivation

- Start from the locked finite Schur-Feshbach expansion of the same-theory Wilson quotient block. The rank-one vacuum direction and one-body Wilson factors have already been eliminated, leaving a positive null-channel margin M_G before irreducible endpoint terms.
- Expand each Wilson loop in the heat-kernel plaquette-sheet regulator. The product of the two second-order trace terms gives the color factor (g^4/4)(T_F/N)^2 because N^{-1}tr(T^aT^b)=(T_F/N)delta^{ab}.
- Separate the four-flux contribution into Wick-square pairings, the irreducible connected kappa_4 cumulant, and nonabelian commutator contacts. The Wick-square part is a positive Gram term, so it can only improve the null-channel lower bound.
- Use the null incidence identity on the straight shared boundary segments to cancel the length-linear f f commutator contact. This is the cancellation that localizes the remaining danger to endpoint/corner boxes plus a tail.
- For each endpoint v, view the singlet-projected connected four-flux cumulant as a self-adjoint finite regulated operator K_v^sing on symmetric two-flux tests. The null hairpin geometry inserts the specific test A_v(w)=sum_i w_i eta_i tensor_s eta_i.
- Apply the spectral theorem: <A_v(w),K_v^sing A_v(w)> >= -Lambda_-(v)||A_v(w)||^2. Summing endpoints gives the displayed lower bound for the connected boundary-OPE polarization R.
- Combine the endpoint bound with M_G. If M_eff remains positive, this block has no endpoint kappa_4 falsifier; if M_eff is negative with a realized endpoint eigenmode, the same-theory OS quotient determinant fails.

Blocking gap: The missing analytic input is a signed or scale-sharp bound for lambda_min(K_v^sing) and for T_tail(w) in four-dimensional Yang-Mills heat-kernel regulation, uniform enough for cutoff removal and obtained without assuming the target mass gap.

## Falsifiers

- A direct heat-kernel endpoint-box calculation gives (g^4/4)(T_F/N)^2 sum_v Lambda_-(v)I_v(w)+|T_tail(w)| >= M_G with nonzero overlap on the hairpin incidence vector; this is a finite Wilson OS falsifier.
- The oriented endpoint plaquette enumeration shows a residual straight-segment f f contact in the null channel, invalidating the localization used by the bound.
- The connected four-flux cumulant has a boundary-scale nonlocal part that cannot be assigned to finitely many endpoint boxes with a valid uniform tail.
- The endpoint estimate requires a boundary counterterm or a changed Wilson normalization, breaking the same-theory condition even if positivity is recovered in a modified algebra.

## Learning

Cycle 245 turns the remaining R problem into a precise finite endpoint spectral estimate. The actual Yang-Mills object is the heat-kernel plaquette-sheet singlet connected four-flux cumulant K_v^sing. Wick-square terms are harmless Gram terms, and the straight f f contact cancels by the null incidence identity; the branch is not looping. Promotion or demotion now depends on the valid inequality comparing the negative endpoint kappa_4 spectrum and tail with M_G.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Enumerate the endpoint plaquettes for the three locked hairpins, form A_v(w) and I_v(w), then compute K_v^sing from fourth derivatives of the endpoint heat-kernel flux-source log partition function after subtracting Wick-square pairings; record lambda_min, Lambda_-, and the first uniform tail bound.
