# cycle-0260

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Post-H,K endpoint kappa_4 clipping certificate for reflected Wilson hairpins

## Candidate Lemma

In the locked three-hairpin finite block, after Wick-square positivity and straight f f contact cancellation, the post-H,K endpoint contribution is a clipped incidence sum. A negative compact-group fourth cumulant can demote the Schur-Feshbach scalar only at endpoint boxes with positive 12-dominance D_v>0; D_v<=0 boxes are protective up to certified same-theory remainders.

## Definitions

- source object: heat-kernel plaquette-sheet endpoint boxes B_v at cutoff a with local source partition functions Z_v(s) for singlet Wilson flux insertions X_{i,v}.
- target object: the corrected post-H,K Schur-Feshbach null-channel scalar S_end for the same finite reflected Wilson block, not a redefined boundary theory.
- controlled interface: connected fourth source derivatives of log Z_v mapped through the null-channel endpoint incidences D_v=2G12(v)-4G13(v)-4G23(v) after the safe contractions are removed.
- same-theory condition: the endpoint boxes, Wilson renormalization, collar limit, and source probes are inherited from the locked gauge-invariant Wilson algebra without boundary counterterms or observable changes.
- X_{i,v} is the plaquette-sheet boundary flux of hairpin i restricted to B_v, with orientation signs epsilon_i(p).
- Gij(v) is the regulator-level geometric/color incidence pairing of the i and j endpoint footprints inside B_v after singlet projection.
- C_N=(g^4/4)(T_F/N)^2 is the color prefactor left by the singlet Wilson expansion in the fundamental representation.

## Assumptions

- Model: four-dimensional Euclidean SU(N) Yang-Mills is regulated by heat-kernel plaquette weights on a reflection-positive lattice collar, with gauge-invariant Wilson plaquette sheets as the test algebra.
- Regime: a<<ell_v<<delta and endpoint boxes B_v isolate corners of the reflected hairpin collars while keeping the bulk straight segments separated from the reflection plane.
- Uniformity: the endpoint cumulant expansion has a cutoff-uniform fourth-order remainder and a tail bound summable over endpoint boxes before taking the continuum limit.
- Cancellation assumption: connected-log subtraction removes Wick-square Gram terms, and the null incidence identity removes the straight C_A f f commutator contact on non-endpoint segments.
- Sign-certification assumption: each singlet endpoint fourth cumulant admits an interval kappa_v^sing=-beta_v+eps_v with 0<=beta_low(v)<=beta_v<=beta_high(v) and |eps_v|<=r_v.
- Same-theory assumption: source derivatives are evaluated in the same heat-kernel Wilson theory used for the collar OS matrix, not in an auxiliary boundary effective model.

## Equations

- endpoint source partition: `Z_v(s)=\int \exp\{-S_{HK,v}(U)+\sum_{i=1}^3 s_i X_{i,v}(U)\}\,d\mu_{HK,v}(U)`. Valid when: Valid when the endpoint box B_v is kept at positive lattice spacing and the heat-kernel plaquette-sheet regulator supplies a finite gauge-invariant local measure.
- singlet connected fourth cumulant: `\kappa^{\rm sing}_{ijkl}(v)=\left.\partial_{s_i}\partial_{s_j}\partial_{s_k}\partial_{s_l}\log Z_v(s)\right|_{s=0,\,{m singlet}}`. Valid when: Valid when the Wilson flux sources are small and the singlet color projection is taken before the endpoint-box cutoff is removed.
- endpoint incidence dominance: `G_{ij}(v)=\sum_{p,q\in B_v}\epsilon_i(p)\epsilon_j(q)\,C_v(p,q),\qquad D_v=2G_{12}(v)-4G_{13}(v)-4G_{23}(v)`. Valid when: Valid when the endpoint footprints are represented by the same plaquette-sheet regulator and C_v is the local singlet incidence kernel after safe contractions.
- post-HK endpoint polarization: `R_{\rm end}=C_N\sum_v \kappa_v^{\rm sing}D_v+T_{\rm corner},\qquad C_N={g^4\over4}\left({T_F\over N}\right)^2`. Valid when: Applies after diagonal Wilson factors, Wick-square Gram terms, and straight f f commutator contacts have been separated or cancelled in the null channel.
- clipped lower bound: `\kappa_v^{\rm sing}=-\beta_v+\varepsilon_v,\ |\varepsilon_v|\le r_v\ \Longrightarrow\ R_{\rm end}\ge C_N\sum_v\{-\beta_{\rm high}(v)[D_v]_+ +\beta_{\rm low}(v)[-D_v]_+-r_v|D_v|\}-|T_{\rm corner}|`. Valid when: Valid when the certified cumulant interval is negative up to the stated error and the corner tail is bounded in the same regulator.
- promotion interval: `\mathcal I_{260}=M_G+C_N\sum_v\{-\beta_{\rm high}(v)[D_v]_+ +\beta_{\rm low}(v)[-D_v]_+-r_v|D_v|\}+[-\tau_{\rm tail},\tau_{\rm tail}]`. Valid when: Valid when M_G is the already computed positive Gaussian Schur-Feshbach margin and tau_tail bounds all endpoint/corner remainder terms uniformly.

## Attempted Derivation

- Name of conceptual pressure: replace the abstract Wilson/OS obstruction by a finite same-theory endpoint sign interval for the connected R term after H,K are known.
- Start from the regulated Wilson plaquette-sheet expansion and write endpoint contributions as source derivatives of log Z_v, so the manipulated object is a connected cumulant in the original heat-kernel theory.
- Use the connected log to keep Wick-square contractions out of R_end; their earlier role is a positive Gram contribution and they are not a falsifier of the corrected second-order form.
- Apply the null-channel incidence identity to the straight C_A f f contact. This leaves endpoint/corner cumulants as the only possible negative contribution.
- In the small heat-kernel endpoint box, express the singlet fourth cumulant as kappa_v^sing=-beta_v+eps_v. Insert it into the pair weights 2,-4,-4 to get D_v=2G12-4G13-4G23.
- Split D_v into [D_v]_+ and [-D_v]_+. Negative kappa_4 is dangerous only on [D_v]_+; equal or balanced endpoint boxes contribute to the protective side.
- Package the result as the interval I_260 for M_G+R_end+tail. The hard gate is now finite endpoint source data plus a uniform tail estimate.

Blocking gap: The branch still lacks certified values or analytic bounds for beta_v, r_v, D_v, and tau_tail in the actual locked hairpin endpoint geometry.

## Falsifiers

- A certified source-derivative interval with D_v>0 dominance large enough that the lower endpoint of I_260 is negative is a direct post-H,K falsifier.
- The heat-kernel eighth-derivative bound M8(v) may diverge so fast that kappa_v cannot be certified uniformly in the cutoff.
- A corner tail with sign coherence in the null channel may exceed the clipped endpoint safety margin.
- The compact-group fourth cumulant might fail to stay negative after the Wilson sheet source and singlet projection are imposed in the actual endpoint box.
- A boundary counterterm or modified Wilson renormalization needed to define Z_v would violate the same-theory condition even if the interval were positive.

## Learning

Cycle 260 attacks the conceptual pressure of making the last R/kappa_4 obstruction finite and sign-certifiable. The sharp value signal is that negative compact-group kappa_4 is not intrinsically dangerous; it is dangerous only through the clipped positive endpoint dominance D_v>0 after valid cancellations. This is route-changing at the branch scope: the proof state is no longer an OS/Wilson obstruction ladder but a finite same-theory endpoint interval computation with a clear promotion or falsifier outcome.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a concrete endpoint dominance stress test, because the abstract obstruction has already been reduced to the sign of a finite R/kappa_4 interval.
- Situation seed: Asymmetric three-hairpin reflected Wilson collar with heat-kernel plaquette-sheet endpoint boxes: keep the 13 and 23 endpoint overlaps fixed while sliding the 12 pair footprints to increase their common endpoint incidence inside one box B_v.
- Varied variable: The endpoint dominance ratio eta=G12(v)/(G13(v)+G23(v)) for the single stressed endpoint box.
- Held-fixed controls: SU(N) heat-kernel plaquette regulator and singlet Wilson source normalization are fixed., The previously computed H,K finite block and its Gaussian Schur-Feshbach margin M_G are held fixed., No boundary counterterms, new Wilson renormalizations, or changes of the gauge-invariant test algebra are allowed., Endpoint box size ell_v and collar separation delta remain in the same cutoff scaling regime.
- Expected observation: For eta<=2 the negative compact-group kappa_4 is clipped into the protective or neutral side; only eta>2 can make D_v positive and create a possible negative interval. The stress case teaches whether a 12-dominant endpoint can defeat M_G before tails are considered.
- Transfer certificate needed: A same-theory source-derivative certificate for kappa_v^sing, a cutoff-uniform tail bound, and a proof that the incidence deformation is realized by admissible reflected Wilson collars rather than by an auxiliary boundary model.

## Next Experiment

Build the actual endpoint incidence table for the locked three-hairpin geometry, compute D_v box by box, then attach seven-point source-derivative intervals for the boxes with D_v>0 before spending effort on protective D_v<=0 boxes.
