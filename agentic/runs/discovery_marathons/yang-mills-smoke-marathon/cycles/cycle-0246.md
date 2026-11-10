# cycle-0246

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Endpoint-box kappa_4 compression for the post-H,K Wilson collar term

## Candidate Lemma

For the first reflected Wilson hairpin triple, after the Wick-square Gram part and the straight f f commutator contact are removed, the remaining post-H,K null-channel R contribution is a finite endpoint-box singlet four-flux cumulant plus a tail. A uniform negative-spectrum bound on this endpoint matrix is a valid promotion test, and a violating aligned negative eigenvector is a same-theory falsifier.

## Definitions

- source object: heat-kernel plaquette-sheet regulated Wilson hairpin triple with endpoint boxes B_v(ell) and collar width delta before delta downarrow 0.
- target object: corrected Schur-Feshbach null-channel endpoint contribution to the continuum OS quotient matrix after H,K are fixed.
- controlled interface: regulated singlet connected four-flux cumulants K_v^sing and endpoint tails replace the abstract R_ij entries.
- same-theory condition: Wilson loops, heat-kernel smearing, color trace normalization, and endpoint-box subtraction are locked before and after collar removal; no boundary counterterm or changed loop algebra is allowed.
- Endpoint label alpha denotes an oriented plaquette-sheet germ incident at v, including its bivector n_alpha and Wilson-loop membership.
- p_{i,v}=sym(sigma_{i,v} otimes sigma_{i,v}) is the pair-incidence vector for loop i at endpoint v, and p_{xi,v}=sum_i xi_i p_{i,v} for the Schur-Feshbach null vector xi.

## Assumptions

- The heat-kernel regulator h_epsilon is gauge-covariant, reflection compatible, and removed only after the endpoint-box estimates are uniform in epsilon and lattice spacing.
- The Wilson expansion is used only inside fixed endpoint boxes; the remainder is bounded uniformly by a local exponential moment for smeared plaquette fluxes.
- Wick pairings of the four flux insertions have already been placed in the positive Gram term and are not counted inside K_v^sing.
- The straight-segment C_A f f contact cancels under the previously identified null incidence identity, leaving only endpoint/corner support and the irreducible connected cumulant.
- The endpoint boxes are disjoint at scale ell, and the outside contribution is collected in E_tail with a regulator-uniform bound.

## Equations

- smeared endpoint flux: `\Phi_{\alpha,v}^a(\epsilon)=\int_{\Sigma_\alpha\cap B_v(\ell)}\int h_\epsilon(x-y)\,n_\alpha^{\mu\nu}(x)F_{\mu\nu}^a(y)\,d^4y\,d\sigma_x`. Valid when: Valid when the reflected Wilson sheets are represented by heat-kernel smeared plaquette surfaces inside a fixed endpoint box.
- singlet connected four-flux endpoint matrix: `(\mathcal K_v^{\rm sing})_{\alpha\beta;\gamma\delta}=\delta_{ab}\delta_{cd}\,\langle\Phi_{\alpha,v}^a\Phi_{\beta,v}^b\Phi_{\gamma,v}^c\Phi_{\delta,v}^d\rangle_c`. Valid when: Applies after Wick pairings are subtracted and only the irreducible connected four-flux cumulant remains.
- endpoint contribution to R: `R_{ij,v}^{(4,c)}=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\langle p_{i,v},\mathcal K_v^{\rm sing}p_{j,v}\rangle+E_{ij,v}^{\rm tail}`. Valid when: Requires the same-theory boundary OPE normalization for traced fundamental Wilson loops and fixed endpoint boxes.
- null-channel compression: `\mathcal R_{\xi,v}^{(4,c)}=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\langle p_{\xi,v},\mathcal K_v^{\rm sing}p_{\xi,v}\rangle+E_{\xi,v}^{\rm tail},\qquad p_{\xi,v}=\sum_i\xi_i p_{i,v}`. Valid when: Valid when the Schur-Feshbach null vector is applied after H passes PHP and the corrected K gate is isolated.
- negative-spectrum bound: `\mathcal R_{\xi}^{(4,c)}\ge -\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v \Lambda_v^-\,\|p_{\xi,v}\|^2-|E_\xi^{\rm tail}|,\quad \Lambda_v^-:=\max(0,-\lambda_{\min}\mathcal K_v^{\rm sing})`. Valid when: Applies after diagonal normalization and after endpoint/corner tails have been separated from the local cumulant matrix.
- promotion inequality: `\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v\Lambda_v^- I_v+|E_\xi^{\rm tail}|<M_G,\qquad I_v:=\|p_{\xi,v}\|^2`. Valid when: Valid when M_G is the already computed positive Gaussian Schur-Feshbach margin for this hairpin block.

## Attempted Derivation

- Start from heat-kernel plaquette-sheet Wilson observables and expand each endpoint-local holonomy to fourth order in the smeared flux Phi_alpha,v.
- Separate disconnected Wick contractions. Their contribution is a positive Gram square in the OS quotient and cannot decrease the corrected Schur-Feshbach null form.
- Project the remaining four-flux cumulant to the singlet color channel. The fundamental traces give the factor (T_F/N)^2, and the two second-order insertions give the coefficient g^4/4.
- Write each loop's endpoint contribution as p_i,v=sym(sigma_i,v otimes sigma_i,v). Bilinearity gives R_ij,v=(g^4/4)(T_F/N)^2 <p_i,v,K_v^sing p_j,v> plus tail.
- Apply the null vector only after the H,K Schur-Feshbach reduction. This replaces the finite matrix combination of R_ij by the single compressed vector p_xi,v=sum_i xi_i p_i,v.
- Use the previously checked straight-incidence identity to kill the local C_A f f contact on non-endpoint portions; any surviving commutator term is pushed into endpoint/corner support.
- Bound the compressed endpoint contribution below by the negative spectral radius Lambda_v^- times the incidence norm I_v=||p_xi,v||^2, then add the absolute endpoint tail bound.
- Compare this negative allowance with the positive Gaussian Schur-Feshbach margin M_G. Strict domination promotes the finite hairpin block; violation with a stable eigenvector demotes it.

Blocking gap: The signed or scale-sharp estimate of lambda_min(K_v^sing) for the actual regulated Yang-Mills endpoint box is still missing.

## Falsifiers

- A direct plaquette-source derivative computation gives lambda_min(K_v^sing)<0 with the aligned incidence norm large enough to violate the promotion inequality; this is the main finite endpoint falsifier.
- The straight f f contact cancellation fails at corners because the endpoint orientation data do not satisfy the same null incidence identity as the straight shared segment.
- The heat-kernel regulator produces a boundary counterterm or cusp renormalization not expressible through the locked Wilson-loop normalization, breaking the same-theory condition.
- The endpoint tail is not small uniformly as epsilon and the lattice spacing are removed, so the finite endpoint-box reduction is not valid.
- The connected four-flux cumulant has a reflection-plane contact term with indefinite sign that is not captured by the singlet endpoint matrix.

## Learning

Cycle 246 compresses the remaining R problem to a finite endpoint spectral inequality. The actual Yang-Mills input is K_v^sing, the heat-kernel plaquette-sheet connected four-flux cumulant. Wick-square positivity and straight f f incidence cancellation remove the safe pieces; only negative endpoint spectrum and tails can defeat the positive Schur-Feshbach margin. The branch is not looping because it now has a computable regulator-level matrix, an incidence norm, and a valid promotion/falsifier inequality.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Introduce endpoint plaquette sources J_alpha in one heat-kernel box, compute K_v^sing as the fourth connected derivative of log <prod W_i exp(sum J_alpha Phi_alpha)> at J=0, reduce by endpoint dihedral and color symmetries, then estimate the smallest eigenvalue on the span of p_xi,v.
