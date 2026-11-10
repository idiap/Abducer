# cycle-0248

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Endpoint kappa_4 source-difference certificate for reflected Wilson hairpins

## Candidate Lemma

Endpoint source-difference certificate. In the heat-kernel plaquette-sheet regulator, after Wick-square Gram positivity and straight f f null-incidence cancellation, the post-H,K endpoint term is bounded by central fourth differences of local singlet source log partition functions. This gives a valid promotion or falsifier inequality against the positive Schur-Feshbach margin M_G.

## Definitions

- source object: heat-kernel plaquette-sheet endpoint-box partition functions Z_{v,a,epsilon}(J) with singlet Wilson four-flux sources parallel transported to the endpoint frame.
- target object: a regulator-uniform signed bound for the connected boundary-OPE polarization R_endpoint entering the corrected second-order Wilson OS gate.
- controlled interface: central fourth source differences D_h log Z_v and sixth-cumulant error bounds controlling the negative spectrum of K_v^sing.
- same-theory condition: the sources are infinitesimal variations of the locked Wilson plaquette-sheet observables, with no added boundary counterterm, no changed loop renormalization, and the same heat-kernel regulator used in H,K.
- K_v^sing[z] is the irreducible connected singlet four-flux cumulant localized in endpoint box B_v along normalized incidence-color source z.
- M_G denotes the already computed positive corrected Schur-Feshbach margin of the finite hairpin block, without restating its threshold formula.

## Assumptions

- Endpoint boxes B_v of size epsilon isolate all non-straight Wilson sheet collisions, and their complements are included in a tail tau_end.
- The heat-kernel lattice action is reflection positive and admits source derivatives up to order six on |s|<=2h uniformly in the endpoint box.
- The null-channel incidence vector has zero straight-segment incidence, so the local f f commutator contact vanishes away from endpoints.
- The Wick-square part of the connected Wilson contraction is a positive Gram contribution and is not used to create a negative estimate.
- The corrected finite Schur-Feshbach H,K gate has positive margin M_G for the locked finite block.

## Equations

- endpoint source cumulant: `\ell_v(s,z)=\log Z_{v,a,\epsilon}(s z),\qquad K_v^{\mathrm{sing}}[z]=\left.\frac{d^4}{ds^4}\ell_v(s,z)\right|_{s=0}`. Valid when: Applies when z is a normalized endpoint incidence-color source supported inside one heat-kernel endpoint box.
- central fourth difference with certified error: `D_h\ell_v(z)=\frac{\ell_v(2hz)-4\ell_v(hz)+6\ell_v(0)-4\ell_v(-hz)+\ell_v(-2hz)}{h^4},\qquad |D_h\ell_v(z)-K_v^{\mathrm{sing}}[z]|\le \frac{h^2}{6}M_{6,v}(z,h)`. Valid when: Valid when ell_v is six times differentiable on the source segment |s|<=2h with bounded sixth derivative.
- post-cancellation endpoint decomposition: `R_{\mathrm{null}}=R_{\mathrm{Wick}}^{\mathrm{Gram}}+R_{ff}^{\mathrm{straight}}+\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v K_v^{\mathrm{sing}}[z_v]+\tau_{\mathrm{end}},\qquad R_{\mathrm{Wick}}^{\mathrm{Gram}}\ge0,\quad R_{ff}^{\mathrm{straight}}=0`. Valid when: Requires the heat-kernel plaquette-sheet Wilson expansion with null incidence cancellation on every straight shared segment.
- promotion inequality: `\Lambda_{-,v}(h)=\sup_{z\in S_v}\left[-D_h\ell_v(z)+\frac{h^2}{6}M_{6,v}(z,h)\right]_+,\qquad \frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v I_v\Lambda_{-,v}(h)+|\tau_{\mathrm{end}}|<M_G`. Valid when: Applies after the H,K Schur-Feshbach gate supplies a positive margin M_G for the locked finite block.
- demotion certificate: `\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v I_v\left[-D_h\ell_v(z_v)-\frac{h^2}{6}M_{6,v}(z_v,h)\right]_+-|\tau_{\mathrm{end}}|>M_G\ \Longrightarrow\ \hbox{endpoint falsifier}`. Valid when: Valid when explicit endpoint sources are chosen and all endpoint-tail signs are bounded with the same regulator.
- Gaussian tangent cancellation: `\ell_v^{G}(s,z)=\ell_v(0)+\frac{s^2}{2}\chi_v(z)\quad\Longrightarrow\quad D_h\ell_v^{G}(z)=0`. Valid when: Applies when the endpoint source law is replaced by its abelian Gaussian tangent approximation.

## Attempted Derivation

- Fix the heat-kernel plaquette-sheet regulator and isolate each reflected Wilson hairpin endpoint in a box B_v of width epsilon.
- Represent endpoint Wilson variations by singlet flux sources J, parallel transported to one endpoint color frame; the connected four-flux cumulant is the fourth derivative of log Z_v(J).
- Decompose the second boundary-OPE polarization into Wick-square, straight f f commutator, endpoint irreducible kappa_4, and endpoint-tail pieces.
- Use the known cancellation: the Wick-square term is a positive Gram form, and the straight f f term is proportional to the null incidence on each straight shared segment, hence vanishes there.
- Localize the remaining irreducible connected part to endpoint boxes and write it as K_v^sing[z_v] with the prefactor (g_a^4/4)(T_F/N)^2 and incidence norm I_v.
- Replace the formal fourth derivative by the computable central difference D_h log Z_v; Taylor expansion gives the explicit error h^2 M_6/6.
- Compare the certified negative endpoint contribution plus tau_end with the positive finite Schur-Feshbach margin M_G to obtain a promotion inequality and a demotion falsifier inequality.

Blocking gap: The finite endpoint heat-kernel group integral Z_v(s z) has not yet been evaluated, and a regulator-uniform sixth source derivative bound M_6 plus endpoint-tail bound tau_end is still missing.

## Falsifiers

- A computed central fourth source difference with certified negative part large enough to exceed M_G after the prefactor is a same-theory endpoint falsifier.
- A nonzero straight f f contribution after checking the exact null incidence would falsify the claimed cancellation and reopen the H,K decomposition.
- A sixth source derivative bound M_6 that diverges faster than the finite-difference signal as a->0 or epsilon->0 would make the certificate invalid.
- If defining Z_v(J) requires a boundary counterterm or a Wilson-loop renormalization not present in H,K, the calculation is not same-theory.
- Endpoint tails comparable to M_G after Wick-square and straight-contact cancellation would demote the endpoint-local reduction.

## Learning

Cycle 248 does not repeat the prior threshold. It converts the remaining post-H,K R term into a finite endpoint source-derivative computation: D_h log Z_v estimates the singlet connected four-flux kappa_4 with an explicit h^2 M_6/6 error. The leading Gaussian part is killed by the fourth difference, Wick-square contractions are positive, and straight f f contacts cancel by null incidence. The only dangerous quantity is therefore a certified negative non-Gaussian endpoint cumulant plus tail, with a valid promotion/falsifier inequality against M_G.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

For one endpoint box, choose a basis of normalized incidence-color sources z, evaluate log Z_v at 0, +/-h, and +/-2h using the heat-kernel character expansion or finite link integration, estimate M_6, then diagonalize the flattened Kmat_v^sing negative spectrum and compare the prefactored result with M_G.
