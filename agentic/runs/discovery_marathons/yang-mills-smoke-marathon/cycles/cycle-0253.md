# cycle-0253

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: endpoint kappa_4 scalar test

## Candidate Lemma

For the first three-hairpin Schur-Feshbach null channel, the small heat-kernel endpoint-box contribution from the compact-group volume density is explicitly signed: each pair endpoint cumulant has leading term -t_v^4 Tr_ad(ad_B^4)/15, and the null scalar is governed by the incidence combination 2 A_12 - 4 A_13 - 4 A_23 plus controlled tails.

## Definitions

- source object: the heat-kernel plaquette-sheet endpoint partition function Z_v(s;B) for the singlet Wilson four-flux cumulant in one endpoint box v.
- target object: the scalar post-H,K Schur-Feshbach null-channel endpoint contribution R_end to the finite Wilson OS quotient block.
- controlled interface: replace the abstract connected boundary-OPE polarization R_ij by endpoint source derivatives d_s^4 log Z_v(0;B_ij,v) with explicit color and incidence factors.
- same-theory condition: the endpoint sources B_ij,v are obtained from the locked Wilson plaquette sheets without adding boundary counterterms, changing loop renormalization, or replacing the observable algebra.

## Assumptions

- Gauge group SU(N) or compact semisimple G, with tr_F(T^a T^b)=T_F delta_ab and adjoint trace Tr_ad.
- Endpoint boxes are smaller than the injectivity radius, and the heat-kernel time t_v is in the small-time regime used by the plaquette-sheet regulator.
- The known first three-hairpin Feshbach null vector is eta=(1,1,-2), while one-body and length-linear second terms have already canceled.
- The connected log is used, so Gaussian Wick-square pieces are removed; straight C_A f f contacts cancel by the null-incidence identity.
- Endpoint transport and corner tails are bounded by a remainder E_tail that is independent of the cutoff after same-theory normalization.

## Equations

- endpoint heat-kernel source model: `Z_v(s;B)=\int_{\mathfrak g} e^{s\langle B,A\rangle} e^{-\|A\|^2/(4t_v)} J(A)^{1/2}(1+\mathcal E_t(A))\,dA,\quad \log J(A)^{1/2}=Q_2(A)-\frac{1}{5760}\operatorname{Tr}_{ad}(\operatorname{ad}_A^4)+O(\|A\|^6)`. Valid when: Valid when the endpoint box lies inside one exponential chart and the heat-kernel time t_v is small compared with the box scale.
- connected endpoint fourth cumulant: `\kappa_{4,v}(B):=\left.\partial_s^4\log Z_v(s;B)\right|_{s=0}=-\frac{t_v^4}{15}\operatorname{Tr}_{ad}(\operatorname{ad}_B^4)+O(t_v^5\|B\|^4+t_v^6\|B\|^6)`. Valid when: Applies after Q_2 has been absorbed into the covariance and B stays in a bounded endpoint source set.
- null contraction weights: `\eta=(1,1,-2),\quad \eta^T R\eta=2R_{12}-4R_{13}-4R_{23}`. Valid when: Valid when the three locked hairpin observables use the known Feshbach null vector and diagonal terms were normalized away.
- root-quartic endpoint contribution: `R_{end}^{(4)}=-\frac{g^4}{60}\left(\frac{T_F}{N}\right)^2\sum_v t_v^4\left(2\mathcal A_{12,v}-4\mathcal A_{13,v}-4\mathcal A_{23,v}\right),\quad \mathcal A_{ij,v}=\operatorname{Tr}_{ad}(\operatorname{ad}_{B_{ij,v}}^4)\ge0`. Valid when: Requires the heat-kernel plaquette-sheet regulator, singlet Wilson projection, and cancellations of Wick-square and straight f f contacts.
- promotion or falsifier inequality: `S_{end}:=\sum_v t_v^4(2\mathcal A_{12,v}-4\mathcal A_{13,v}-4\mathcal A_{23,v}),\quad R_{end}=-c_{YM}S_{end}+E_{tail},\quad c_{YM}=\frac{g^4}{60}\left(\frac{T_F}{N}\right)^2`. Valid when: Applies after diagonal normalization and after endpoint boxes have been separated from straight-collar contact contributions.

## Attempted Derivation

- Use exponential coordinates A in each heat-kernel endpoint box and write the plaquette-sheet endpoint source as exp(s <B_ij,v,A>).
- The Gaussian heat-kernel part gives log Z quadratic in s, so its fourth connected derivative vanishes; this is the connected Wick-square cancellation in scalar form.
- The root Jacobian of the compact group has quartic term -Tr_ad(ad_A^4)/5760. Tilting the Gaussian by s <B,A> shifts the mean by 2 t_v s B.
- Only the homogeneous quartic evaluated on the shifted mean contributes to the fourth derivative at leading order: -24(2t_v)^4 Tr_ad(ad_B^4)/5760=-t_v^4 Tr_ad(ad_B^4)/15.
- Multiplying by the singlet Wilson color factor (g^4/4)(T_F/N)^2 gives the coefficient -g^4(T_F/N)^2/60 for each pair endpoint cumulant.
- Contracting with eta=(1,1,-2) gives the incidence weights 2,-4,-4. Thus equal disjoint endpoint boxes make the root-quartic term promote positivity, while a demoting contribution needs dominance of the 12 endpoint incidence or a negative tail.

Blocking gap: The actual endpoint table B_ij,v, including coalesced corner boxes and parallel-transported sheet normals, has not yet been enumerated, and the O(t_v^5 ||B||^4 + t_v^6 ||B||^6) plus corner-tail bound is not uniform enough for a certified sign interval.

## Falsifiers

- A certified endpoint table with S_end>0 and c_YM S_end exceeding the Gaussian Schur-Feshbach margin plus positive tail allowance is a same-theory falsifier.
- A noncancelled straight C_A f f contact in the same null channel would invalidate the endpoint-only decomposition.
- Failure of the heat-kernel endpoint expansion uniformly near coalesced corners would demote this regulator computation to a heuristic.
- If B_ij,v requires a boundary counterterm or a changed Wilson-loop normalization, the calculation is valid only for a different theory.
- A seven-point finite-difference interval for d_s^4 log Z_v that excludes the root-quartic prediction would falsify the small-box asymptotic used here.

## Learning

The connected endpoint R term is not an arbitrary symbolic parameter. In the heat-kernel plaquette-sheet regulator, the first non-Gaussian compact-group contribution is a negative fourth cumulant for each endpoint source, but the Feshbach null scalar applies mixed weights 2,-4,-4. Therefore equal disjoint endpoint boxes are actually safe; a falsifier needs 12-endpoint dominance or a genuinely negative tail. This is valid progress beyond the threshold because it computes the regulator-level kappa_4 coefficient and exposes the exact incidence data still missing.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Enumerate the endpoint boxes of the locked three-hairpin plaquette sheets, compute B_12,v, B_13,v, B_23,v and S_end, then bound the heat-kernel transport and corner-tail remainder by the same seven-point source-derivative certification.
