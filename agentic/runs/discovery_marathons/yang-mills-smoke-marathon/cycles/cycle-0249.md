# cycle-0249

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Endpoint-box kappa_4 null-channel finite-difference test

## Candidate Lemma

For the locked three-hairpin post-H,K null channel, the dangerous connected boundary-OPE polarization R is certified by scalar fourth source differences of heat-kernel endpoint-box partition functions. Full kappa_4 diagonalization is unnecessary unless the Feshbach null space has dimension greater than one.

## Definitions

- source object: heat-kernel plaquette-sheet regulated reflected Wilson hairpin endpoint boxes, with singlet flux sources coupled to the same lattice action as the collar observables.
- target object: a certified lower and upper interval for the post-H,K endpoint contribution to the corrected Schur-Feshbach null-channel quadratic form.
- controlled interface: central fourth source differences of log endpoint-box partition functions give the connected four-flux boundary cumulant with an explicit sixth-derivative error.
- same-theory condition: the endpoint boxes, sources, Wilson trace normalization, and collar-to-boundary limit use the locked gauge-invariant Wilson algebra without boundary counterterms or altered renormalization.
- Phi_{v,alpha} denotes the oriented singlet boundary flux insertion in endpoint box v, including the Wilson expansion sign convention and color trace normalization.
- epsilon_{i,v,alpha} is the oriented incidence of hairpin i at endpoint v in flux channel alpha; xi_v(z)=sum_i z_i epsilon_{i,v,alpha} is the compressed null-channel source.
- M_G(z) is the already extracted positive corrected Schur-Feshbach margin from Gaussian/Wick-square safe terms, not a new symbolic threshold.

## Assumptions

- The regulator is the heat-kernel plaquette-sheet regulator at lattice spacing a, with endpoint box radius r satisfying a << r and containing every corner plaquette touched by the reflected collar collapse.
- z is normalized, z perpendicular to the vacuum vector e, and z lies in ker(PHP) for the corrected post-H,K finite block.
- Wick-square contractions are kept in the safe positive margin M_G(z), while straight-segment f f commutator contacts cancel by the null-incidence identity away from endpoint boxes.
- The endpoint source functional log Z_v(eta) is analytic for |eta| <= 2h||xi_v(z)|| and has a certified sixth directional derivative bound M_{6,v}(z).
- The omitted exterior of endpoint boxes has a same-theory tail bound |Tail_{r,a}(z)| <= T_tail(r,a,z) for the same Wilson observables.

## Equations

- endpoint source cumulant: `Z_v(\eta)=\int \exp\{\sum_\alpha \eta_\alpha \Phi_{v,\alpha}(U)\}\,d\mu^{heat}_{v,a}(U),\quad K^{sing}_{v,\alpha\beta\gamma\delta}=\partial_\alpha\partial_\beta\partial_\gamma\partial_\delta\log Z_v(0)`. Valid when: Valid when the heat-kernel endpoint box contains every plaquette within distance r of a reflected hairpin endpoint and all inserted fluxes are singlet projected.
- direct null-channel contraction: `\kappa_{4,v}(z)=K^{sing}_v(\xi_v(z),\xi_v(z),\xi_v(z),\xi_v(z)),\quad \xi_{v,\alpha}(z)=\sum_i z_i\varepsilon_{i,v,\alpha}`. Valid when: Valid when z is a normalized vector in the Schur-Feshbach null channel and epsilon records the oriented endpoint incidence of the locked hairpins.
- fourth finite-difference estimator: `\widehat\kappa_{4,v,h}(z)=h^{-4}\sum_{q=-2}^{2}(-1)^q\binom{4}{2+q}\log Z_v(qh\xi_v(z)),\quad |\widehat\kappa_{4,v,h}(z)-\kappa_{4,v}(z)|\le h^2M_{6,v}(z)/6`. Valid when: Applies after h is chosen inside a common analytic source disk and the sixth directional derivative is uniformly bounded there by M_6.
- crude heat-kernel sixth-derivative bound: `M_{6,v}(z)\le C_6(SU(N))\,P_v^6\,\|\xi_v(z)\|_1^6\,t_a^{-3}`. Valid when: Applies when the source insertions are realized as left-invariant heat-kernel derivatives and the endpoint box has P_v active plaquettes.
- endpoint R interval: `R_{end}(z)\in I_R(z):=\frac{g^4}{4}(T_F/N)^2\sum_v[\widehat\kappa_{4,v,h}(z)-h^2M_{6,v}(z)/6,\widehat\kappa_{4,v,h}(z)+h^2M_{6,v}(z)/6]+[-T_{tail},T_{tail}]`. Valid when: Valid when Wick-square Gram terms and straight f f contacts have already been removed by the null-incidence cancellation and tails are bounded by T_tail.
- promotion and falsifier interval: `I_S(z)=M_G(z)+I_R(z),\quad \inf I_S(z)>0\Rightarrow \mathrm{promote},\quad \sup I_S(z)<0\Rightarrow \mathrm{falsifier}`. Valid when: Requires the same-theory boundary OPE normalization and the corrected Schur-Feshbach margin for the selected post-H,K null channel.

## Attempted Derivation

- Start from the corrected Schur-Feshbach scalar in a post-H,K null vector z; only the connected endpoint part of R can still lower the form.
- Use the heat-kernel plaquette-sheet regulator and decompose the reflected Wilson cumulant into Wick-square pairings, straight f f commutator contacts, endpoint boxes, and exterior tails.
- Discard no dangerous negative term in the first two pieces: Wick-square terms are positive Gram contributions included in M_G, and straight f f contacts vanish under the null-incidence identity on non-corner plaquettes.
- Compress all endpoint color/geometric incidence into a single singlet source direction xi_v(z), so the needed cumulant is the scalar fourth derivative d^4/ds^4 log Z_v(s xi_v(z)) at s=0.
- Apply the symmetric five-point fourth-difference formula. Taylor expansion gives the exact h^2 M_6/6 remainder because the sixth-power stencil moment equals 120.
- Combine endpoint intervals with the explicit prefactor (g^4/4)(T_F/N)^2 and the tail enclosure T_tail, then compare M_G+R_end with zero.

Blocking gap: The branch still lacks certified values or rigorous enclosures for the five endpoint partition-function evaluations and for the same-theory tail T_tail in the continuum scaling window.

## Falsifiers

- A certified interval with sup(M_G+I_R)<0 is the direct finite-block falsifier for same-theory OS positivity.
- The straight f f cancellation fails if endpoint orientation or color trace conventions make the null incidence identity false at a non-corner plaquette.
- The sixth-derivative bound grows so fast with t_a^{-1} that every useful h makes the finite-difference interval wider than M_G.
- The exterior tail cannot be bounded in the locked Wilson algebra without adding a boundary counterterm or changing Wilson renormalization.
- Non-singlet endpoint states survive the reflected product, showing that the singlet-projected endpoint box is not a valid same-theory reduction.

## Learning

The useful next R computation is scalar, not spectral: the Feshbach null vector contracts the singlet endpoint kappa_4 before any eigenvalue problem is needed. This turns the connected Wilson boundary-OPE polarization into finite source evaluations of log Z_v and exposes the exact valid sign test: compare the certified interval for M_G+R_end with zero. The branch is not looping, but promotion now depends on actual endpoint-box data or a sharper analytic bound than the crude t_a^{-3} sixth-derivative estimate.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute or bound log Z_v(qh xi_v(z)) for q=-2,-1,0,1,2 in the smallest heat-kernel endpoint box; use heat-kernel derivative bounds to choose h minimizing h^2M_6/6 plus numerical/source-evaluation error, then test the interval for M_G+R_end.
