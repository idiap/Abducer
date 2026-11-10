# cycle-0244

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Post-H,K endpoint kappa_4 spectral bound for reflected Wilson hairpins

## Candidate Lemma

In the first three-hairpin Wilson block, after H,K and the corrected Schur-Feshbach form are fixed, the remaining dangerous R contribution is a finite endpoint-box spectral problem: the null-channel endpoint term is bounded below by the negative spectrum of the singlet connected four-flux cumulant times an explicit endpoint incidence norm, plus a tail.

## Definitions

- source object: heat-kernel plaquette-sheet regulated SU(N) Yang-Mills Wilson hairpin block with lattice cutoff a, smearing scale sigma, endpoint boxes Box_v(ell), and locked fundamental trace normalization.
- target object: the signed endpoint contribution to the corrected second-order Schur-Feshbach null-channel form after the H,K Wilson collar data are known.
- controlled interface: replace symbolic R_ij by the singlet-projected connected four-flux cumulant localized in endpoint boxes, with explicit color factor (g^4/4)(T_F/N)^2 and geometric incidence tensors J_v.
- same-theory condition: the endpoint-box limit uses the same Wilson-loop renormalization, the same gauge-invariant test algebra, and no added boundary counterterm at the reflection plane.

## Assumptions

- Heat-kernel plaquette-sheet regulation is used, with a << sigma << ell smaller than the separation between distinct nonincident endpoint boxes.
- Flux insertions are parallel transported to the endpoint before color contraction, so the endpoint cumulant is gauge invariant after singlet projection.
- Wick-square contractions have been separated as a positive Gram contribution and do not enter the negative endpoint spectrum.
- The straight-segment nonabelian f f contact cancels in the null incidence channel already isolated for the first hairpin block.
- Endpoint tails outside the boxes satisfy a uniform cluster/OPE remainder bound Tail_{sigma,ell}(z).

## Equations

- endpoint connected four-flux cumulant: `\mathcal C^{(4),\sigma}_{v;ABCD}:=\int_{\Box_v(\ell)^4}\prod_{r=1}^4 d\Sigma_r\,\eta_\sigma(x_r-v)\,\langle \mathcal F_A(x_1)\mathcal F_B(x_2)\mathcal F_C(x_3)\mathcal F_D(x_4)\rangle_c^{\mathrm{sing}}`. Valid when: Valid when the heat-kernel plaquette-sheet regulator parallel-transports all flux insertions to the endpoint before color-singlet projection.
- endpoint R decomposition: `z^*R_{\mathrm{end}}z=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\sum_{v}\langle J_v(z),\mathcal C^{(4),\sigma}_{v}J_v(z)\rangle+\operatorname{Tail}_{\sigma,\ell}(z)`. Valid when: Applies after diagonal normalization, Wick-square Gram removal, and straight f f incidence cancellation have been performed.
- negative-spectrum endpoint bound: `z^*R_{\mathrm{end}}z\ge -\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\Lambda_-(\sigma,\ell) I_{\partial}(z)-|\operatorname{Tail}_{\sigma,\ell}(z)|,\qquad I_{\partial}(z)=\sum_v\|J_v(z)\|^2`. Valid when: Valid when Lambda_- is the largest negative eigenvalue magnitude of every endpoint cumulant matrix in the regulated boxes.
- ultraviolet endpoint OPE size test: `\Lambda_-(\sigma,\ell)\le C_{\mathrm{ep}}\,C_A\,g_R^2(\ell^{-1})+O(g_R^4(\ell^{-1}))+O(\sigma/\ell)`. Valid when: Valid in the ultraviolet endpoint-box regime where the connected four-flux OPE is asymptotically free and no new cusp counterterm is introduced.
- promotion inequality: `\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\Lambda_-(\sigma,\ell)I_{\partial}(z)+|\operatorname{Tail}_{\sigma,\ell}(z)|<M_G`. Valid when: Requires the same-theory boundary OPE and the previously computed positive Gaussian margin for this finite hairpin block.

## Attempted Derivation

- Expand each reflected Wilson hairpin as a heat-kernel plaquette-sheet exponential and keep the fourth flux order contributing to the post-H,K polarization R.
- Subtract the two-pair Wick contractions; their contribution is a positive Gram form and cannot be the endpoint falsifier.
- Use the null-channel incidence identity to cancel the straight-segment C_A f f commutator contact, leaving only endpoint and corner boxes plus a tail.
- Localize the remaining support with a partition of unity around each boundary endpoint v and parallel transport all flux insertions to v before taking the singlet color projection.
- The normalized fundamental trace gives the color prefactor (g^4/4)(T_F/N)^2, while all geometry is carried by endpoint incidence tensors J_v(z).
- Taking the negative spectral part of the finite endpoint cumulant matrix gives the lower bound by Lambda_-(sigma,ell) I_partial(z).
- The connected four-flux cumulant has no Gaussian term after Wick subtraction, so its first UV contribution is controlled by C_A g_R^2(ell^{-1}) times an endpoint vertex kernel.

Blocking gap: The missing estimate is a cutoff-uniform signed bound on Lambda_-(sigma,ell) and on Tail_{sigma,ell}(z), including corner/cusp path-ordering terms, in the actual Yang-Mills measure.

## Falsifiers

- A lattice heat-kernel endpoint measurement finds Lambda_- I_partial large enough that the endpoint term exceeds the positive Gaussian margin; this is the direct finite-block falsifier.
- A residual straight-segment f f contact survives after exact path ordering, invalidating the cancellation used before endpoint localization.
- The endpoint tail is not local because a boundary mode produces power leakage between distinct endpoint boxes.
- Wilson cusp renormalization at the reflection plane requires a new boundary counterterm, so the same-theory condition is false even if positivity is restored.
- The irreducible four-flux cumulant contains an O(1) negative contact after Wick subtraction, contradicting the UV endpoint OPE size test.

## Learning

The branch did not restate the threshold. It identified the actual Yang-Mills object that remains: the heat-kernel plaquette-sheet singlet connected four-flux endpoint cumulant. Wick-square terms are safe positive Gram terms, and straight f f contacts cancel in the null incidence channel. The remaining valid promotion or falsifier is a finite endpoint negative-spectrum inequality with explicit color factor, incidence norm, and tail.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the endpoint cumulant matrix C^{(4),sigma}_v for one plaquette-sheet endpoint box: enumerate the incidence tensors J_v for the three hairpins, evaluate the one-interaction color/geometric kernel V^{(4),sigma}_v, and extract its lowest singlet eigenvalue against the null vector z.
