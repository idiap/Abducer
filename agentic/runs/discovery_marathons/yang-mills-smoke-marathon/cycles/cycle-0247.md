# cycle-0247

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Post-H,K endpoint kappa_4 spectral bound for reflected Wilson collars

## Candidate Lemma

For the first three-hairpin Schur-Feshbach null channel, the remaining connected boundary-OPE polarization is bounded by the negative spectrum of the singlet heat-kernel endpoint four-flux cumulant plus a controlled tail. If this endpoint deficit is smaller than the positive Gaussian margin M_G, the block passes; if it exceeds M_G stably, it is a same-theory falsifier.

## Definitions

- source object: heat-kernel plaquette-sheet regulated reflected Wilson collar block, with endpoint boxes B_v(rho) and parallel transported curvature flux insertions Phi_{v,alpha}^a.
- target object: a lower bound for the post-H,K Schur-Feshbach null scalar E_u in terms of the negative spectrum of K_v^sing.
- controlled interface: replace each connected boundary-OPE polarization R_ij by its endpoint cumulant matrix plus a tail controlled by OPE Holder regularity.
- same-theory condition: the Wilson loops, collar limiting order, heat-kernel normalization, and endpoint parallel transports are fixed before taking the continuum limit; no boundary counterterm or pair-dependent renormalization is inserted.
- K_v^sing is the irreducible singlet-projected connected four-flux cumulant after Wick-square and straight f f contact pieces are removed.
- Z_{i,v}^{alpha beta} is the endpoint pair-incidence tensor determined by the two plaquette-sheet legs of Wilson observable i at endpoint v.
- Lambda_-(A)=max(0,-lambda_min(A)) on the endpoint pair-incidence subspace.

## Assumptions

- Gauge group is SU(N), tr_F(T^a T^b)=T_F delta^{ab}, and d_A=N^2-1.
- The regulator scale satisfies a << rho << ell_min, where ell_min is the smallest non-endpoint geometric separation in the hairpin block.
- Heat-kernel plaquette-sheet Wilson observables are reflection-positive at fixed cutoff and admit uniform local cumulant bounds in endpoint boxes.
- The Wick-square contraction has already been separated as a positive Gram contribution.
- The straight-segment C_A f f commutator contact cancels against the null incidence density for the concrete hairpin geometry.
- The remaining non-endpoint OPE tail has a Holder remainder bound with exponent eta>0.

## Equations

- endpoint_flux_variable: `\Phi_{v,\alpha}^a(\rho)=\int_{\Sigma_{v,\alpha}} h_\rho(x-v)\,U_{v,x}^{ab}F_{\mu\nu}^b(x)\,d\sigma_{\alpha}^{\mu\nu}(x)`. Valid when: Valid when heat-kernel smearing radius rho is larger than the lattice spacing and smaller than the nearest geometric separation.
- singlet_endpoint_cumulant: `\mathcal K^{\rm sing}_{v,\alpha\beta;\gamma\delta}(\rho)=d_A^{-2}\delta_{ab}\delta_{cd}\,\langle \Phi_{v,\alpha}^a\Phi_{v,\beta}^b\Phi_{v,\gamma}^c\Phi_{v,\delta}^d\rangle_{c,{\rm irr}}`. Valid when: Applies after all Wick-square contractions and one-body Wilson normalizations have been subtracted in the same regulator.
- endpoint_R_matrix: `R_{ij}^{\rm end}(\rho)=\frac{g_\rho^4}{4}\left(\frac{T_F}{N}\right)^2\sum_{v,\alpha\beta\gamma\delta} Z_{i,v}^{\alpha\beta}\mathcal K^{\rm sing}_{v,\alpha\beta;\gamma\delta}(\rho)\overline{Z_{j,v}^{\gamma\delta}}`. Valid when: Valid when reflected Wilson surfaces are expanded to four endpoint flux insertions with identical plaquette-sheet smearing.
- null_incidence_norm: `b_{u,v}^{\alpha\beta}=\sum_i u_iZ_{i,v}^{\alpha\beta},\qquad I_v(u)=\sum_{\alpha\beta}|b_{u,v}^{\alpha\beta}|^2`. Valid when: Valid when u is the Schur-Feshbach null vector and the endpoint pair basis is heat-kernel normalized.
- negative_spectrum_bound: `u^*R^{\rm end}u\ge -\frac{g_\rho^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v\Lambda_-(\mathcal K_v^{\rm sing}(\rho))I_v(u)`. Valid when: Valid when Lambda_- is computed on the finite endpoint incidence subspace after the straight-contact cancellation.
- tail_bound: `T_{\rm tail}(\rho)\le C_4\|u\|_1^2(\rho/\ell_{\min})^\eta`. Valid when: Requires the regulated connected four-flux density to have an eta-Holder OPE remainder away from endpoint boxes.
- promotion_inequality: `\mathcal E_u\ge M_G-\frac{g_\rho^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v\Lambda_-(\mathcal K_v^{\rm sing})I_v(u)-T_{\rm tail}(\rho)`. Valid when: Applies after diagonal normalization, Wick-square positivity, and straight f f incidence cancellation have all been verified.

## Attempted Derivation

- Start from the post-H,K quotient block, where only the connected second boundary-OPE polarization remains in the Schur-Feshbach null scalar.
- Expand each heat-kernel plaquette-sheet Wilson observable to four endpoint flux insertions using the same parallel transports used in the regulated Wilson loop.
- Separate Wick-square contractions; they form a positive Gram matrix and therefore cannot be the negative endpoint falsifier.
- Contract the local nonabelian commutator term proportional to C_A f f with the null incidence density. On straight shared segments the signed incidence sum is zero, so this contact cancels before any endpoint estimate is needed.
- Partition the boundary footprint into endpoint boxes and straight interior pieces. The straight interior remainder has vanishing zeroth incidence moment, so the OPE Holder remainder gives T_tail <= C_4||u||_1^2(rho/ell_min)^eta.
- Inside each endpoint box the remaining irreducible singlet four-flux cumulant is a finite Hermitian matrix K_v^sing on endpoint pair-incidence tensors.
- For b_{u,v}=sum_i u_i Z_{i,v}, the endpoint contribution is prefactor times b_{u,v}^*K_v^sing b_{u,v}. The spectral theorem gives the lower bound by -Lambda_-(K_v^sing)||b_{u,v}||^2.
- Compare the resulting endpoint deficit with M_G. This is a valid regulator-level promotion/falsifier test and does not restate the earlier hairpin threshold.

Blocking gap: The missing Yang-Mills input is a signed, scale-stable computation or bound for Lambda_-(K_v^sing) and for the OPE tail constant C_4 in the heat-kernel plaquette-sheet regulator.

## Falsifiers

- A direct source-derivative computation gives a stable negative endpoint eigenvalue whose prefactor times I_v exceeds M_G; this is the main falsifier.
- The straight C_A f f contact fails to cancel after parallel-transport orientation is included, creating a non-endpoint negative term.
- The endpoint tail is not O((rho/ell_min)^eta) and remains comparable to the Gaussian margin in the collar limit.
- K_v^sing requires a pair-dependent boundary subtraction to have a continuum limit, violating the same-theory condition.
- The heat-kernel source extraction is not valid for the locked Wilson algebra because the plaquette-sheet approximation changes the reflected observable family.

## Learning

Cycle 247 turns the post-H,K R term into a concrete finite spectral computation. The actual Yang-Mills object is the singlet source derivative K_v^sing of the heat-kernel plaquette-sheet partition function. Wick-square terms are positive, straight f f contacts cancel by null incidence, and only the negative endpoint kappa_4 spectrum plus a Holder tail can demote the block. This is a valid contribution-making move because it gives the exact regulator matrix to compute and the sign/size inequality needed for promotion or falsifier status.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

At fixed lattice spacing, insert four endpoint plaquette-sheet sources in the heat-kernel action, differentiate log Z, project with d_A^{-2}delta_ab delta_cd, subtract Wick and straight f f pieces, diagonalize K_v^sing on the incidence subspace, and track Lambda_- under two regulator refinements.
