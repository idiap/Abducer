# cycle-0054

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: XOR Carrier Approximate Affine-Sketch Gate

## Candidate Lemma

For the generated XOR-SAT carrier, any subthreshold approximate piecewise-affine sketch of the parity-incidence map gives an unrestricted circuit upper bound for the carrier. Thus a barely-superlinear source lower bound is valid only after ruling out these sketches, not merely after showing large formula-range entropy.

## Definitions

- source object: H_N(x)=\bigoplus_{j\le M} SAT(G_{N,j}(x)), where M=N^q, each query has length L=(\log N)^d, and A_N(x)\in\mathbb F_2^{U_L} is the parity-incidence vector of generated formulas.
- target object: SAT on L-bit instances, with intended consequence SAT\notin SIZE(n^c) for every fixed c, hence NP\not\subseteq P/poly if the carrier lower bound and transfer are both valid.
- controlled interface: G_N has circuit size N^{\rho+o(1)} and SAT\in SIZE(n^c) substitutes into all M polylog-length queries with total size N^{\max\{\rho,q\}+o(1)}.
- target-preserving condition: d>1 and \max\{\rho,q\}<1+\epsilon; source audits may hardwire constants only as upper-bound falsifiers and must not be advertised as target lower-bound evidence.

## Assumptions

- There is a circuit S_N of size s that, on input x, outputs a piece index t\in[K] and coordinates z\in\mathbb F_2^r.
- For all but E exceptional inputs x, A_N(x)=a_t+\sum_{i\le r} z_i b_{t,i} over \mathbb F_2, where a_t,b_{t,i}\in\mathbb F_2^{U_L} are nonuniformly fixed for the carrier length.
- Exceptional inputs are patched by equality gates of total size O(EN).
- Circuit size is unrestricted nonuniform Boolean circuit size for H_N.

## Equations

- incidence_pullback: `H_N(x)=\langle A_N(x),Y_{SAT}\rangle_{\mathbb F_2}`. Valid when: Valid when A_N records generated formulas with parity multiplicity and Y_{SAT} is the fixed truth-label vector on L-bit formulas.
- piecewise_affine_evaluation: `H_N(x)=\lambda_t\oplus\bigoplus_{i\le r} z_i\mu_{t,i},\quad \lambda_t=\langle a_t,Y_{SAT}\rangle,\ \mu_{t,i}=\langle b_{t,i},Y_{SAT}\rangle`. Valid when: Valid when x is nonexceptional and the sketch representation of A_N(x) holds inside the selected affine piece.
- sketch_upper_bound: `C(H_N)\le O(s+Kr+K\log K+EN)`. Valid when: Applies when the sketch circuit computes piece indices and coordinates and exceptional seeds are corrected by explicit equality tests.
- source_falsifier_threshold: `s+Kr+EN\le N^{1+\epsilon-\Omega(1)}\ \Longrightarrow\ C(H_N)\not> N^{1+\epsilon-o(1)}`. Valid when: Valid in the barely-superlinear source regime where lower bounds are measured against unrestricted nonuniform circuits of input length N.

## Attempted Derivation

- Represent the XOR carrier as H_N(x)=<A_N(x),Y_SAT> over F_2.
- Try to prove C(H_N)>N^{1+epsilon} from the claim that A_N({0,1}^N) has no low-dimensional affine sketch.
- Observe that any exact or approximate piecewise-affine sketch yields a small H_N circuit by hardwiring the SAT inner products of the affine bases.
- Strengthen the necessary audit to piecewise-affine sketches with exceptional-set correction cost EN.
- Test whether large rank alone suffices; it fails because the fixed SAT label vector may be simple on the generated image.

Blocking gap: Need a direct lower bound for the SAT-label pullback x -> <A_N(x),Y_SAT>, or a non-natural real-SAT theorem showing that every subthreshold H_N circuit induces a subthreshold approximate affine-incidence sketch. Current rank and sketch audits are only falsifiers.

## Falsifiers

- falsifier: an exact affine incidence representation of rank r<N^{1+epsilon-o(1)} makes H_N easy by hardwiring basis parities.
- falsifier: an approximate piecewise-affine sketch with s+Kr+EN<N^{1+epsilon-o(1)} kills the source lower bound after equality patching.
- falsifier: a linear or low-degree algebraic generator whose parity-incidence map has computable rank O(N polylog N) collapses the XOR carrier to near-linear size.
- falsifier: a SAT-monochromatic generated range makes H_N constant even if the incidence image has high rank.
- falsifier: q>=1+epsilon or rho>=1+epsilon causes quantitative target-threshold collapse.
- falsifier: d<=1 with small lookup exponent may reintroduce exhaustive SAT-label leakage below the source threshold.

## Learning

Cycle 54 strengthens the XOR route with an approximate piecewise-affine incidence-sketch conservation law. Bad seeds cost EN gates to patch, and a sketch of total cost s+Kr+EN below N^{1+epsilon} is a concrete falsifier for the source lower bound. High incidence rank alone is not valid lower-bound evidence because the SAT label functional may be simple on the generated image.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for candidate XOR generators.`
- Rationale: The branch no longer needs another hardness-magnification slogan; it needs to know whether explicit XOR carriers survive the new approximate affine-sketch upper bound while preserving the valid polylog-query target bridge.
- Situation seed: Fix L=(log N)^d with d>1, M=N^q with q in ((1+epsilon)/2,1+epsilon), and compare two generators: a linear seeded sparse-incidence generator A_N(x)=Bx over F_2, and a hash-based nonlinear generator producing M formula indices by independent-looking polylogarithmic hashes.
- Varied variable: The affine-sketch exponent alpha, where r=N^alpha, together with a small piece exponent kappa for K=N^kappa while monitoring the total cost s+Kr+EN.
- Held-fixed controls: The target bridge parameters d>1 and max{rho,q}<1+epsilon remain fixed., The carrier remains XOR of real SAT labels on generated polylog-length formulas., No advice depending on x is allowed; only length-dependent constants such as basis parities may be hardwired for upper-bound falsifiers., The lower-bound target remains C(H_N)>N^{1+epsilon-o(1)}, not P != NP itself.
- Expected observation: The linear generator fails with alpha<=1 and gives a small carrier circuit. A genuinely nonlinear hash generator may have no visible subthreshold affine cover, but this observation is only suggestive until tied to the SAT-label pullback rather than to incidence rank alone.
- Transfer certificate needed: A formal certificate must prove either a direct unrestricted-circuit lower bound for H_N, or a nonrelativizing extraction theorem converting every small H_N circuit into an approximate piecewise-affine incidence sketch with loss below N^{1+epsilon}.

## Next Experiment

Instantiate the hash-based XOR generator and compute whether its incidence map has an explicit low-cost piecewise-affine cover; if none is found, formulate the exact extraction theorem needed to turn small H_N circuits into such covers.

# Barrier-Aware Lower-Bound Route: Fourier Spectral Norm Gate

## Candidate Lemma

A Fourier L1/spectral-norm lower bound is a valid bridge only for target classes with a proved spectral-norm upper compiler. It separates L-leaf decision trees, but it gives no P-vs-NP transfer for unrestricted polynomial-size circuits.

## Definitions

- source object: the +/-1 truth table f:{0,1}^m->{-1,1}, with intended source f=SAT_m and N=2^m truth-table length.
- target object: deterministic decision trees with L leaves, or a named subclass C[m^k] such that every target function h has ||hat h||_1 <= B_C(m,k).
- controlled interface: Walsh-Fourier L1 norm computed from the complete truth table; transfer uses only the inequality ||hat f||_1>B_C(m,k).
- target-preserving condition: the threshold must be on the same m-bit slice, must exceed the named target upper bound, and must not be supplied by padding or an easy NP-complete carrier branch.

## Assumptions

- Fourier characters are over the uniform Boolean cube and functions are encoded as +/-1.
- The target model C is fixed before the lower bound is interpreted.
- No invariance under arbitrary many-one reductions is assumed.

## Equations

- spectral_norm: `\|\widehat f\|_1=\sum_{S\subseteq[m]} |\mathbb E_x f(x)\chi_S(x)|`. Valid when: Valid when f is a +/-1 truth table on m Boolean inputs and Fourier characters use the uniform cube measure.
- decision_tree_upper_bound: `h\in DT_{leaf}(L)\;\Rightarrow\;\|\widehat h\|_1\le L`. Valid when: Applies when h is computed by a deterministic decision tree with L leaves over the same m coordinates.
- inner_product_falsifier_norm: `\|\widehat{IP_r}\|_1=2^r=2^{m/2}\quad (m=2r)`. Valid when: Valid for the +/-1 inner-product function on m=2r inputs with characters indexed by F_2 subsets.
- conditional_transfer: `\|\widehat{SAT_m}\|_1>B_C(m,k)\;\Rightarrow\; SAT_m\notin C[m^k]`. Valid when: Requires a proved spectral-norm upper bound B_C for every size m^k target computation on exactly the same m input bits.

## Attempted Derivation

- Assume a proof establishes ||hat SAT_m||_1 > m^k or even > 2^{alpha m}.
- Try to infer SAT_m notin SIZE(m^k) by treating small circuits as low spectral-norm objects.
- The required target lemma would be: every size m^k circuit h has ||hat h||_1 <= B_SIZE(m,k) below the SAT threshold.
- This target lemma is false: IP_r has O(m^2)-size circuits and ||hat IP_r||_1=2^{m/2}.
- Restricting to L-leaf decision trees repairs the derivation because B_DT=L is true.

Blocking gap: No nontrivial Fourier L1 upper bound exists for unrestricted polynomial-size circuits; the target threshold collapses before reaching P-vs-NP.

## Falsifiers

- IP_r is in P and has O(m^2)-size circuits but Fourier spectral norm 2^{m/2}; this falsifier kills any high-spectral-norm-to-SIZE(poly) transfer.
- The tagged language G_{n,r} is NP-complete via the SAT slice and has norm at least 2^r from an easy branch; this falsifier kills arbitrary NP-complete-carrier evidence.
- Random truth tables give a large, poly(N)-constructive high-norm property; if claimed useful against full circuits it would be a natural proof, but usefulness fails because of IP_r.

## Learning

Cycle 54 isolates a valid Fourier spectral-norm gate: ||hat f||_1>L proves lower bounds for L-leaf decision trees and any class with a named spectral ceiling B_C. The unrestricted P-vs-NP transfer fails because IP_r is a small-circuit high-norm falsifier, and tagged SAT/IP carriers show that arbitrary NP-complete high-norm evidence is not target-preserving.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for spectral-norm lower-bound routes.`
- Rationale: The route has an apparently quantitative lower-bound statistic, but the statistic may be dominated by padding or easy branches. A concrete tagged carrier tests whether the proposed transfer is target-preserving rather than another abstract barrier slogan.
- Situation seed: Construct G_{n,r}(u,b,v): on tag b=0 output SAT_n(u), on tag b=1 output IP_r(v). SAT reduces to G by x -> (x,0,0^{2r}), while the IP slice has Fourier L1 norm 2^r and polynomial-size circuits.
- Varied variable: The IP block length r, equivalently the fraction rho=2r/(n+1+2r) of coordinates assigned to the easy high-norm branch.
- Held-fixed controls: The target class is unrestricted nonuniform SIZE(m^k) measured on the total input length m=n+1+2r., The reduction witnessing NP-completeness always lands in the b=0 SAT slice., The statistic is the full Walsh-Fourier L1 norm of the whole truth table., The IP branch remains uniformly polynomial-time computable with O(r^2) circuits.
- Expected observation: As r grows to Theta(m), ||hat G_{n,r}||_1 >= 2^r regardless of the SAT slice. NP-completeness remains fixed, so high spectral norm can be entirely non-SAT evidence.
- Transfer certificate needed: Before the intuition may enter a proof queue, one must prove either a SAT-slice spectral lower bound that survives restriction accounting, or a true target upper bound B_C for the named class. For C=SIZE(poly), the certificate is impossible because IP violates it.

## Next Experiment

Audit Fourier entropy or Fourier dimension routes with the same target-ceiling test: compute the exact value for IP_r, then run the tagged SAT/IP carrier falsifier before allowing any P-vs-NP interpretation.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

A kappa-dense, E-canonical, low-distinct-image MCSP carrier with one row satisfying the diagonal anti-ball condition at exponent epsilon-rho yields a valid E-language unrestricted circuit lower bound with exponent any delta<(epsilon-rho)/(kappa(1+D)). This is a route bridge only, not P != NP.

## Definitions

- source object: a sequence of image families I_m subset {0,1}^{2^m} with distinct-image entropy D, canonical unranking in E time, and at least one row T in I_m satisfying AB_{epsilon,rho}.
- target object: the padded multiplexed language L_I(i,x,pad)=T_i(x), where i indexes a canonical distinct image and x has length m.
- controlled interface: MCSP-type anti-ball row witness -> E circuit lower bound via distinct-image multiplexing and kappa-balanced padding.
- target-preserving condition: all indexing, length selection, and unranking are uniform without advice, and the source lengths are kappa-dense enough to transfer the lower bound to the declared target lengths.

## Assumptions

- Constants epsilon,rho,D are fixed with 0<rho<epsilon<1 and D>=0.
- For each relevant m, I_m has at most 2^{D m+O(1)} distinct rows and admits bit computation T_i(x) in 2^{O(m)} time.
- Source lengths are kappa-dense: every large target length n maps to an m with n<=kappa(1+D)m+O(1).
- The anti-ball condition ranges over unrestricted Boolean circuits, not merely uniform or restricted circuit classes.

## Equations

- AB-diagonal: `\mathrm{AB}_{\epsilon,\rho}(T):\quad \forall \xi,\eta\ge 0,\ \max\{\xi,\eta\}\le \epsilon-\rho,\ \forall A\ (|A|\le 2^{\xi m})\Rightarrow \operatorname{dist}(T,A)>2^{\eta m}`. Valid when: Valid when distances are between length-2^m truth tables and circuits are unrestricted Boolean circuits on m inputs.
- rooted-edit-upper-bound: `\operatorname{dist}(T,A)\le 2^{\eta m}\ \wedge\ C(A)\le 2^{\xi m}\quad\Rightarrow\quad C(T)\le C(A)+O(m2^{\eta m})\le 2^{\max\{\xi,\eta\}m+o(m)}`. Valid when: Applies when T is obtained from A by explicitly hardwiring at most 2^{eta m} edited input points.
- multiplex-transfer: `C_n(L_I)>2^{\delta n}\quad\text{for every}\quad \delta<\frac{\epsilon-\rho}{\kappa(1+D)}`. Valid when: Requires the padding map and distinct-image multiplexing preserve uniformity without advice on every target length.
- forbidden-cover-size: `\log_2\left|\bigcup_{|A|\le 2^{\xi m}} B(A,2^{\eta m})\right|\le 2^{\max\{\xi,\eta\}m+O(\log m)}`. Valid when: Valid when xi and eta are fixed below one and circuits use a standard finite gate basis.

## Attempted Derivation

- Define U_m as the union, over all unrestricted circuits A of size at most 2^{xi m} and all max{xi,eta}<=epsilon-rho, of Hamming balls B(A,2^{eta m}).
- The cover bound gives log_2|U_m|<=2^{(epsilon-rho)m+O(log m)}, so random truth tables avoid U_m with probability 1-o(1). Hence M=2^{D m} random rows are simultaneously anti-ball with overwhelming probability.
- Try to choose the lexicographically first M rows outside U_m to obtain a canonical low-D carrier.
- Testing whether a candidate row lies outside U_m requires enumerating threshold circuits, taking time 2^{2^{epsilon m+o(m)}}, so lex-first selection is not E-canonical.
- Try to derandomize the random rows by a standard succinct PRG or local sampler. If its point-access exponent alpha is below epsilon-rho, each row has circuits of size 2^{alpha m+o(m)}, which is a falsifier for MCSP no-side soundness.
- The only surviving source shape is a sparse no-advice sequential unranker with point-access exponent at least epsilon-rho, together with a non-large proof of diagonal anti-ball soundness.

Blocking gap: No current construction gives a no-advice, low-D, E-canonical image family with a proof of diagonal anti-ball avoidance without either dense naturalness, brute-force enumeration, or subthreshold decoder leakage.

## Falsifiers

- falsifier: a source row T has dist(T,A)<=2^{eta m} from a circuit A of size 2^{xi m} with max{xi,eta}<epsilon-rho; rooted edits then give a subthreshold circuit for T.
- falsifier: the anti-ball certificate is a dense poly(N)-time predicate over all truth tables, making the route a natural-proof object rather than a sparse carrier.
- falsifier: the unranker or decoder computes T_i(x) with point-access exponent alpha<epsilon-rho, yielding small circuits for every row.
- falsifier: source soundness is justified only by enumerating all size-2^{epsilon m} circuits, exceeding the 2^{O(m)} E-canonical interface.
- falsifier: a nonuniform selector or advice string names the hard row or the source length, so the target lower bound is only nonuniform leakage.
- falsifier: the source exists only infinitely often without kappa-dense padding, giving at best an i.o. target and not the claimed all-length transfer.

## Learning

Cycle 54 converts the previous rooted-volume ambiguity into a precise diagonal anti-ball invariant. The invariant is sufficient for MCSP row hardness and transfers through low-D multiplexing with exponent delta<(epsilon-rho)/(kappa(1+D)). Random anti-ball carriers exist by a strong cover bound, but lex-first, brute-force, dense constructive, and local-decoder implementations are invalid. The remaining task is a sparse, no-advice, non-natural anti-ball certificate, not a proof of P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design-now-as-falsifier-probe`
- Rationale: The extraction theorem is now sharp; the live uncertainty is whether explicit anti-ball sources can avoid local-decoder leakage and naturalness. Varying one access parameter tests exactly where source proposals become invalid.
- Situation seed: For each m take M=2^{D m} random truth tables conditioned to avoid every ball B(A,2^{eta m}) around every unrestricted circuit A of size 2^{xi m} for all max{xi,eta}<=epsilon-rho; then imagine replacing this random family by a padded sequential unranker G_alpha(i,x).
- Varied variable: point-evaluation exponent alpha, where G_alpha(i,x) runs in time 2^{alpha m+o(m)} for one requested truth-table bit
- Held-fixed controls: epsilon,rho,D,kappa are fixed constants with delta target below (epsilon-rho)/(kappa(1+D))., No advice, no nonuniform hard-row selector, and canonical distinct-image indexing are allowed., The target language remains the same padded multiplexed E language., The anti-ball condition ranges over unrestricted circuits and all diagonal pairs max{xi,eta}<=epsilon-rho.
- Expected observation: For alpha<epsilon-rho the source is invalid by a direct small-circuit upper bound. For alpha>=epsilon-rho the source is compatible with MCSP soundness, and the random model predicts robust anti-ball existence because the forbidden union is exponentially tiny inside truth-table space.
- Transfer certificate needed: Before the intuition affects proof obligations, one needs an E-uniform sparse unranker plus a proof that some indexed row satisfies the diagonal anti-ball condition; the proof must be non-large or nonconstructive over full truth-table space and must not introduce a subthreshold decoder.

## Next Experiment

Audit one concrete sequential unranker family, such as a code/expander-based sampler with deliberately expensive point evaluation: compute its alpha, D, kappa, and whether its soundness proof excludes all unrestricted subthreshold circuits or only profile/restricted circuits.
