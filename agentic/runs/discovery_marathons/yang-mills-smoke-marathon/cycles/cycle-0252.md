# cycle-0252

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Endpoint heat-kernel kappa_4 curvature estimate for post-H,K Wilson null form

## Candidate Lemma

In the heat-kernel plaquette-sheet endpoint regulator, after the Wick-square Gram term and straight f f incidence term have been cancelled, the scalar null-channel endpoint cumulant has a signed local leading term: kappa_4,v(B_v)=-(t_a^4/120) sum_{alpha>0} alpha(B_v)^4 plus controlled image, BCH, and tail errors. Thus the remaining R_end term is nonpositive to leading order and is promoted exactly when its certified magnitude plus tails stays below the positive Schur-Feshbach margin M_G.

## Definitions

- source object: heat-kernel plaquette-sheet endpoint box B_v for SU(N) with plaquette time t_a, Haar measure, locked Wilson color normalization T_F, and a scalar null-channel source X_v(B_v).
- target object: the post-H,K endpoint contribution R_end(u) to the corrected Schur-Feshbach null form for the already fixed three-hairpin Wilson block.
- controlled interface: replace the seven-point source stencil for d_s^4 log Z_v(0) by a heat-kernel normal-coordinate expansion with explicit remainder and the same endpoint-box regulator.
- same-theory condition: the source derivative is taken inside the original heat-kernel lattice Yang-Mills endpoint box, with no boundary counterterm, no altered Wilson normalization, and the same collar/hairpin observables.
- B_v is the Lie-algebra source direction obtained by contracting the endpoint plaquette flux insertions with the Feshbach null vector and the signed collar incidence matrix.
- M_G denotes the positive Gaussian Schur-Feshbach margin already left after H,K and the safe Wick-square part are removed.

## Assumptions

- G=SU(N), t_a is small enough that endpoint plaquette holonomies are exponentially concentrated in one injectivity ball.
- The endpoint source is centered and linear to leading order in geodesic coordinates; BCH nonlinearities are placed in the certified remainder E_rem.
- The connected log Z_v is used, so Gaussian Wick-square contractions do not contribute to kappa_4,v.
- The straight-segment C_A f f commutator contact has zero contraction with the null incidence vector before endpoint localization.
- Endpoint tails from neighboring collar boxes obey a same-regulator bound E_tail with no new boundary counterterm.

## Equations

- endpoint source partition function: `Z_v(s;B_v)=\int_{\mathfrak g_{inj}}\exp(s\langle B_v,A\rangle)K_{t_a}(e^A)J(A)\,dA+Z_v^{img}(s)`. Valid when: Valid when the endpoint plaquette holonomies are localized inside the injectivity ball and all outside sheet variables are either fixed boundary data or integrated with the same heat-kernel measure.
- local heat-kernel density with Haar curvature: `K_t(e^A)J(A)=c_t e^{-\|A\|^2/(2t)}\exp\left[-\frac{1}{24}\sum_{\alpha>0}\alpha(A)^2-\frac{1}{2880}\sum_{\alpha>0}\alpha(A)^4+O(\|A\|^6+t\|A\|^4)\right]+O(e^{-r_{inj}^2/(8t)})`. Valid when: Applies after choosing geodesic coordinates for a small endpoint box and excluding image terms by the heat-kernel off-diagonal bound.
- signed endpoint kappa_4 leading term: `\kappa_{4,v}(B_v)=\partial_s^4\log Z_v(s;B_v)|_{s=0}=-\frac{t_a^4}{120}\sum_{\alpha>0}\alpha(B_v)^4+\mathcal R_v`. Valid when: Requires the connected source log and the null-incidence cancellations already used to remove Wick-square and straight f f contact terms.
- SU(N) root quartic: `\sum_{\alpha>0}\alpha(B)^4=\sum_{i<j}(b_i-b_j)^4=N\operatorname{tr}_F(B^4)+3(\operatorname{tr}_F B^2)^2`. Valid when: Valid when B is conjugated into the traceless Hermitian Cartan and tr_F fixes the fundamental normalization.
- endpoint contribution to R: `R_{end}(u)=\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v \omega_v\kappa_{4,v}(B_v)+Tail_a`. Valid when: Applies after diagonal normalization of the Wilson block and after summing only endpoint boxes left by the straight-segment cancellation.
- promotion inequality: `M_G-\frac{g_a^4}{480}\left(\frac{T_F}{N}\right)^2\sum_v\omega_v t_a^4\sum_{\alpha>0}\alpha(B_v)^4-E_{rem}-E_{tail}>0`. Valid when: Valid when the remainder and tail bounds are certified uniformly over the endpoint collar regulator.

## Attempted Derivation

- Write the endpoint box with the original heat-kernel plaquette action and insert a scalar source s X_v only as a derivative at s=0, preserving the same theory.
- Use geodesic coordinates U=e^A at the endpoint. The product of heat kernel and Haar density is Gaussian times sqrt(J(A)), up to image and Hadamard-coefficient errors.
- Expand log sqrt(J(A)) as -sum_alpha alpha(A)^2/24 - sum_alpha alpha(A)^4/2880 + higher terms. The quadratic term changes the variance gate but cannot create the fourth connected cumulant at this order.
- Tilt the Gaussian by exp(s <B_v,A>). Under the tilt, E_s[alpha(A)^4] contains the term t_a^4 s^4 alpha(B_v)^4. Applying -d_s^4 to the quartic Jacobian contribution gives -24/2880 times the root quartic, namely -t_a^4 sum_alpha alpha(B_v)^4/120.
- The connected log removes Gaussian Wick-square pieces, and the previously established null incidence identity removes the straight f f contact. Therefore the first surviving local endpoint contribution is the negative Haar-curvature kappa_4 term, plus image, BCH, and tail remainders.
- Multiplying by the Wilson color prefactor (g_a^4/4)(T_F/N)^2 and summing endpoint incidences yields a concrete sign/size condition against M_G.

Blocking gap: The remaining gap is a uniform reduction from the full multi-plaquette endpoint box to the single normal-coordinate source direction B_v with explicit E_rem, including BCH source nonlinearities and possible boundary holonomy dependence.

## Falsifiers

- falsifier: heat-kernel mass outside the injectivity ball is not exponentially small at the RG endpoint scale, so image terms can alter the sign of kappa_4.
- falsifier: BCH nonlinearities in the endpoint Wilson source produce another O(t_a^4) connected term not included in the root-quartic curvature coefficient.
- falsifier: a direct seven-point same-theory source evaluation of log Z_v gives a kappa_4 interval below the curvature estimate by more than E_rem.
- falsifier: corner plaquettes break the null-incidence cancellation of the straight C_A f f contact, reintroducing a non-endpoint contribution to R.
- falsifier: the certified inequality for M_G+R_end is negative after adding E_tail, yielding an actual finite Wilson OS determinant failure.

## Learning

The post-H,K R term is no longer a black-box endpoint cumulant: in the small heat-kernel endpoint box, its first connected non-Gaussian contribution is the negative root-quartic curvature of the compact group measure. This is a valid contribution-making move because it names the regulator, the cumulant d_s^4 log Z_v, the cancellations used, and the precise promotion/falsifier inequality. The branch is not looping; it now needs actual B_v incidence data and uniform remainder bounds.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the actual endpoint incidence directions B_v for the three-hairpin null vector, evaluate sum_v omega_v sum_{alpha>0} alpha(B_v)^4 using the SU(N) trace formula, and pair it with a heat-kernel C^6/C^8 remainder bound to certify the interval for M_G+R_end.
