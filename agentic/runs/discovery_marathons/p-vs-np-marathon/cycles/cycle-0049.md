# cycle-0049

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: locality extraction threshold

## Candidate Lemma

A generated-OR source lower bound can be certified from separator-denominator hardness only through a nonrelativizing extraction theorem with subthreshold loss: if every SIZE(S) circuit for H_N yields a one-sided local separator cover of denominator at most S/N^{1+sigma}+N^kappa and kappa<epsilon-sigma, then a denominator lower bound N^{epsilon-sigma+omega(1)} implies C(H_N)>N^{1+epsilon-o(1)}; with max{rho,q}<1+epsilon this gives the target SAT notin P/poly implication.

## Definitions

- source object: H_N^G(x)=OR_{1<=j<=N^q} SAT(G_N(x,j)), where x has length N, each query has length L=(log N)^d with d>1, and C(G_N)<=N^rho.
- target object: SAT notin P/poly, reached only by substituting hypothetical polynomial-size SAT circuits into all generated queries.
- controlled interface: arbitrary circuit for H_N is transformed into a one-sided local separator cover for the actual generated SAT bags, with denominator D_{sigma,E} and error budget E.
- target-preserving condition: max{rho,q}<1+epsilon, extraction loss kappa<epsilon-sigma, error E<N^{epsilon-o(1)}, and the extraction must use real SAT semantics rather than relativizing oracle access.
- D_{sigma,E} counts residual positive-bag caps after charging N^{1+sigma} gates per local predicate and EN gates for corrected bad bags.

## Assumptions

- The separator lower bound is proved for the actual generated range, not for an enlarged promise range.
- The extraction theorem works for every nonuniform circuit A deciding H_N, not just for syntactic OR-of-local-predicates circuits.
- The proof is nonrelativizing; planted-control oracle worlds are admitted as a falsifier for relativizing versions.
- Polylogarithmic query length keeps SAT substitution cost N^{q+o(1)} for every fixed polynomial SAT exponent.

## Equations

- generated_or_carrier: `H_N^G(x)=\bigvee_{j=1}^{N^q} SAT(G_N(x,j)),\quad |G_N(x,j)|=(\log N)^d`. Valid when: Valid when the source object is the high-q generated-OR carrier with explicitly bounded generator complexity.
- target_substitution_bound: `SAT\in SIZE(n^c)\Rightarrow C(H_N^G)\le N^\rho+N^q(\log N)^{dc}+O(N^q)=N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when SAT circuits are nonuniform, c is fixed, and generated queries have polylogarithmic length.
- needed_extraction_bound: `A\in SIZE(S),\ A=H_N^G\Rightarrow D_{\sigma,E}(G;A)\le S/N^{1+\sigma}\cdot polylog(N)+N^\kappa`. Valid when: Valid when a nonrelativizing locality-extraction theorem converts arbitrary global H circuits into one-sided local covers.
- separator_to_source_threshold: `D_{\sigma,E}(G)>N^{\epsilon-\sigma+\omega(1)},\ E<N^{\epsilon-o(1)},\ \kappa<\epsilon-\sigma\Rightarrow C(H_N^G)>N^{1+\epsilon-o(1)}`. Valid when: Valid when the denominator lower bound holds for all residual covers produced by the extraction theorem.

## Attempted Derivation

- Assume a circuit A of size S<N^{1+epsilon} decides H_N^G.
- Use A to define a residual positive distribution over generated bags and try to build one-sided local predicates accepting at least one satisfiable query per positive bag.
- Attempt SAT self-reduction on a generated formula y=G_N(x,j); this manipulates assignments inside y but does not produce nearby inputs x' that alter only y.
- Add a hypothetical neutralizing map E_j(y); then A(E_j(y)) exactly decides SAT on R_j, giving extraction but also demagnifying the source obligation to restricted SAT hardness.
- Therefore the useful bridge is not separator hardness alone but the quantitative nonrelativizing extraction bound D<=S/N^{1+sigma}+N^kappa with kappa<epsilon-sigma.

Blocking gap: There is no valid operation converting an arbitrary global H circuit into local SAT-range separators without either neutralizing the generator or using a new real-SAT, nonrelativizing locality principle.

## Falsifiers

- falsifier: extraction tax kappa>=epsilon-sigma makes the separator lower bound too weak to force C(H_N)>N^{1+epsilon}.
- falsifier: neutralizing embeddings provide a valid extraction but turn the source lower bound into a direct restricted-SAT lower bound at threshold N^{1+epsilon}.
- falsifier: a planted-control oracle can keep one-sided local separators hard while making H_N easy, so any relativizing extraction theorem is false.
- falsifier: a subthreshold promise solver on the actual generated range gives C(H_N)<=N^rho+N^q T_N+N^{q+o(1)}.
- falsifier: a dense constructive direct-H lower-bound property triggers the natural-proofs obstruction under standard PRF hardness assumptions.

## Learning

Cycle 49 converts the surviving generated-OR route into an exact extraction-threshold problem. Separator-denominator hardness is a valid source certificate only if every small H circuit yields covers with denominator S/N^{1+sigma}+N^kappa and kappa<epsilon-sigma. Neutralization gives a concrete extraction but is a demagnifying falsifier, because it asks for restricted-SAT hardness rather than a barely-superlinear H lower bound.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for proposed locality-extraction mechanisms.`
- Rationale: The branch no longer needs another magnification slogan; it needs to know whether arbitrary H circuits can be localized without projection-style demagnification.
- Situation seed: High-q generated-OR carrier with q in ((1+epsilon)/2,1+epsilon), L=(log N)^d for d>1, and a tunable family G_N^theta where N^theta positions have neutralizing embeddings while the remaining positions are high-entropy real-SAT queries.
- Varied variable: theta, the exponent of neutralizable generated positions.
- Held-fixed controls: max{rho,q}<1+epsilon so the target substitution bridge stays valid, no SAT advice beyond the assumed target circuits, real SAT semantics rather than an oracle SAT predicate, separator predicate size charged as N^{1+sigma} per cap with fixed sigma<epsilon
- Expected observation: For theta=0, separator hardness can be disconnected from C(H_N); for theta near q, extraction becomes valid but source hardness reduces to restricted-SAT hardness. A useful route must exhibit an intermediate nonrelativizing extraction with kappa<epsilon-sigma and no neutralization demagnifier.
- Transfer certificate needed: A theorem mapping every SIZE(S) H_N circuit to one-sided covers of the actual generated positive fibers with denominator S/N^{1+sigma}+N^kappa, kappa<epsilon-sigma, while proving the construction fails in planted-control oracle worlds.

## Next Experiment

Formalize one candidate extraction using SAT self-reducibility plus generator local decodability, then compute whether the required decodability already implies neutralizing embeddings and hence demagnification.

# Barrier audit for Fourier-tail lower-bound routes

## Candidate Lemma

Fourier-tail lower bounds give a valid target gate for constant-depth AC0 via LMN concentration, but they do not transfer to P or unrestricted SIZE without an additional low-tail compiler; PARITY is the falsifier for that compiler.

## Definitions

- source object: the uniform truth table of f_m=SAT_m or a named NP carrier on m input bits, represented as a {-1,1}-valued function with Walsh-Fourier coefficients under the uniform cube.
- target object: depth-d unbounded fan-in AC0 circuits of size at most m^k; the audited non-target is unrestricted Boolean SIZE(m^k) and uniform P machines.
- controlled interface: the LMN concentration theorem, which upper-bounds the Fourier mass above degree t for every circuit in the named AC0 target class.
- target-preserving condition: a P-vs-NP transfer would need a proof that every P-time or SIZE(m^k) decider for the same m-bit language has low Fourier tail at the same t and epsilon parameters, with no padding or encoding leakage.

## Assumptions

- d and k are fixed constants; s=m^k is the AC0 size threshold.
- Fourier degree is measured on the same m-bit representation used by the target circuits.
- The lower-bound claim is about tail mass, not merely existence of one high-degree coefficient.
- No advice-dependent encoding of the truth table is allowed unless it is counted in the target interface.

## Equations

- tail_definition: `W_{>t}(f)=\sum_{S\subseteq[m],\ |S|>t}\widehat f(S)^2`. Valid when: Valid when f is represented as a {-1,1}-valued Boolean function under the uniform measure on m input bits.
- LMN_gate: `f\in AC0_d[\mathrm{size}\le s]\ \Rightarrow\ W_{>t}(f)\le \varepsilon\quad\text{for }t\ge C_d(\log(s/\varepsilon))^{d-1}`. Valid when: Applies for constant depth d AC0 over the uniform cube with standard LMN Fourier concentration parameters.
- AC0_transfer: `W_{>t}(SAT_m)>\varepsilon\ \wedge\ t\ge C_d(k\log m+\log(1/\varepsilon))^{d-1}\ \Rightarrow\ SAT_m\notin AC0_d[m^k]`. Valid when: Requires the lower bound and the LMN threshold to use the same input length, encoding, depth, and epsilon.
- SIZE_collapse: `\exists g\in P\cap SIZE(O(m)):\quad W_{>m-1}(g)=1\quad(g=PARITY_m)`. Valid when: Valid when the target class permits XOR or general Boolean circuits rather than constant-depth AC0 without parity gates.
- largeness_audit: `\Pr_F[W_{>t}(F)>1/2]\ge 1-2D_t/2^m,\quad D_t=\sum_{i\le t}\binom mi`. Valid when: Valid for uniformly random Boolean truth tables after applying Markov to the low-degree Fourier mass.

## Attempted Derivation

- Assume a proposed route proves W_{>t}(SAT_m)>epsilon for t=polylog(m).
- Apply LMN: if t exceeds C_d(k log m+log(1/epsilon))^{d-1}, then SAT_m is not in AC0_d[m^k].
- Try to upgrade to SAT_m notin P by asserting that P or SIZE(m^k) computations have low Fourier tail at comparable t.
- Test the assertion on PARITY_m, which is in P and linear-size circuits but has all Fourier mass at degree m.
- Test encoding robustness on the branched language L_{n,r,p}, which is NP-complete yet has constant tail mass coming solely from an easy parity slice.

Blocking gap: There is no valid low-tail compiler for P or unrestricted SIZE, and Fourier tail is not stable under NP-complete recodings with easy high-frequency branches.

## Falsifiers

- PARITY_m is a falsifier for any claim that polynomial-time or polynomial-size computation implies low Fourier tail.
- The branched NP-complete language L_{n,r,p} is a falsifier for arbitrary NP-complete-carrier Fourier-tail evidence, because the measured tail can come from an easy parity slice.
- If P_{t,theta} is claimed useful against SIZE(poly), its largeness and poly(N) constructivity trigger the natural-proof audit unless a non-natural escape feature is named.
- Padding with ignored variables is a falsifier for thresholds stated in the wrong length parameter, since LMN uses the ambient m while hardness may live in a smaller core.

## Learning

Cycle 49 isolates the Fourier-tail route exactly: LMN gives a valid quantitative AC0 bridge at t >= C_d(k log m+log(1/epsilon))^{d-1}, while unrestricted P/SIZE transfer collapses because parity has maximal tail in linear size. A branched NP-complete language shows high tail can be injected by an easy parity slice while preserving many-one SAT hardness, so arbitrary NP-complete-carrier Fourier evidence is quarantined. This is route-level barrier progress, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for Fourier-tail routes.`
- Rationale: The route needs a concrete target-preserving test because Fourier mass is sensitive to harmless encodings and can certify an easy high-frequency gadget rather than computational hardness.
- Situation seed: Define L_{n,r,p}(phi,z,u,b) by accepting SAT_n(phi) on the b=0 slice and accepting PARITY_r(z) on the b=1 slice; SAT reduces by fixing b=0, z=0^r, and u=0^p, so NP-hardness is preserved while an easy parity branch is inserted.
- Varied variable: Vary beta in r=m^beta, the parity-branch length as a fraction of the total input length m.
- Held-fixed controls: The target AC0 depth d and size exponent k are fixed., The Fourier measure is the uniform truth-table measure over the total m input bits., The many-one reduction from SAT always uses the b=0 slice and has no advice., The LMN threshold is computed with the same ambient m and epsilon.
- Expected observation: As beta grows, the degree-r parity character keeps coefficient magnitude 1/2 in the sign representation, so W_{>=r} stays at least 1/4 even if the SAT branch is ignored. This shows high tail can be target-preserving for NP-hardness but not hardness-preserving for P-vs-NP.
- Transfer certificate needed: Before the intuition may affect proof obligations, the route needs a formal certificate that excludes easy high-frequency slices, fixes a canonical SAT encoding, or proves a reduction-invariant low-tail obstruction for the actual target class.

## Next Experiment

Audit Fourier entropy or spectral-spread routes next: compute whether small P functions such as inner product or addressing already realize the proposed entropy threshold, and separate restricted-class transfer from P-vs-NP extrapolation.

# MCSP / Meta-Complexity Carrier Transfer: interval-decoder leakage audit

## Candidate Lemma

Interval-access leakage lemma. Let U_m be a low-image MCSP carrier whose rows are N-bit truth tables, N=2^m, and suppose every accepted row is claimed to have circuit complexity greater than s_m=2^{epsilon m}. If there is an indexed interval decoder which, for some block exponent lambda, outputs the 2^{lambda m}-bit block of any row from its row seed and block index using circuit or restart complexity 2^{tau(lambda)m+o(m)} and checkpoint complexity 2^{chi(lambda)m+o(m)}, then every row has unrestricted circuits of size at most 2^{max{lambda,tau(lambda),chi(lambda)}m+o(m)}. Hence a valid no-side MCSP carrier must satisfy inf_lambda max{lambda,tau(lambda),chi(lambda)} >= epsilon, up to lower-order terms.

## Definitions

- source object: a uniform low-distinct-image MCSP certificate carrier U_m of N=2^m bit truth tables, with row seed length at most Dm and claimed row hardness against unrestricted circuits of size 2^{epsilon m}.
- target object: an E-uniform multiplexed language obtained by ranking the distinct carrier rows, intended to yield an E circuit lower bound with exponent delta below epsilon/(kappa(1+D)).
- controlled interface: sequential row emission is allowed, but any indexed block, interval, restart, or checkpoint decoder for row bits is charged by exponents lambda, tau(lambda), and chi(lambda).
- target-preserving condition: the carrier remains no-advice, kappa-dense across source lengths, E-canonicalizable, and has no subthreshold interval decoder; otherwise the extracted E lower bound is invalid.

## Assumptions

- Rows are Boolean truth tables on m input bits; unrestricted circuit size is the MCSP measure.
- For fixed row seed a, nonuniform circuits may hardwire a; row-seed length is not a hardness resource.
- An interval decoder receives a row seed and a block index and returns all bits in that block, or equivalently has a restart mechanism whose advice/checkpoint can be computed with exponent chi(lambda).
- The claimed MCSP threshold is s_m=2^{epsilon m} with constant epsilon>0, not epsilon(m)=o(1).

## Equations

- row-size-from-interval-decoder: `size(row_a) <= 2^{max(lambda,tau(lambda),chi(lambda)) m + o(m)}`. Valid when: Valid when the interval decoder is indexed by block number and the fixed row seed may be hardwired nonuniformly into the final row circuit.
- interval-leakage-falsifier: `inf_{0<=lambda<=1} max(lambda,tau(lambda),chi(lambda)) < epsilon => U_m is not an MCSP no-side carrier at threshold 2^{epsilon m}`. Valid when: Applies when the source soundness claims every accepted row has unrestricted circuit complexity exceeding the named MCSP threshold.
- admissible-source-cutoff: `alpha_int(U)=inf_lambda max(lambda,tau(lambda),chi(lambda));  valid source requires epsilon <= alpha_int(U)+o(1)`. Valid when: Requires a declared access profile for the source emitter and excludes hidden advice that would change the checkpoint exponent.

## Attempted Derivation

- Start with the random robust low-D family from L49.3, which satisfies the MCSP no-side and sparse-correction requirements with overwhelming probability.
- Try to derandomize it by a seed-indexed selector S_m(a) whose full output stream is E-time computable and whose image count is 2^{Dm+o(m)}.
- Give S_m an indexed restart feature so the verifier or unranking algorithm can recompute a requested block of length 2^{lambda m} without scanning the whole row.
- For a fixed seed a, hardwire a into the block decoder. On input x, compute the block index and offset, run the interval decoder, and select the desired bit.
- This gives row circuits of size 2^{max(lambda,tau(lambda),chi(lambda))m+o(m)}. If this exponent is below epsilon, the selected row is not on the MCSP no-side.
- Therefore PRG-like, locally decodable, or checkpoint-rich repairs cannot instantiate the random carrier unless their interval access exponent already meets the MCSP threshold.

Blocking gap: We still lack a no-advice E-uniform selector that proves robust bad-ball avoidance while having alpha_int at least epsilon. Known explicitness methods provide either local/block access and become easy, or only nonconstructive random existence.

## Falsifiers

- interval-access falsifier: some lambda has max(lambda,tau(lambda),chi(lambda))<epsilon for the proposed row emitter
- local-bit falsifier: the selector gives a seed-indexed circuit for individual truth-table bits of size 2^{o(m)}
- checkpoint-table falsifier: restart advice or a computable checkpoint function yields subthreshold indexed recovery
- nonuniform-length falsifier: the source uses advice to choose the kappa-dense hard lengths
- natural-property falsifier: the proof of robust avoidance defines a large constructive property of truth tables
- threshold-collapse falsifier: epsilon(m)=o(1) after accounting for image entropy, padding, or verifier overhead

## Learning

Cycle 49 adds a quantitative interval-decoder leakage theorem. The previous local-decoder falsifier extends to any indexed block restart: a source with alpha_int<epsilon cannot be an MCSP no-side carrier. Random robust low-D carriers still exist combinatorially, so the real obstruction is an E-uniform, no-advice, non-natural selector whose access profile is itself hard. The established extraction exponent delta<epsilon/(kappa(1+D)) remains valid conditional on such a source.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe`
- Rationale: The current route is blocked at the explicit selector, and interval restart is the most tempting way to make sequential carriers verifiable; the thought experiment tests exactly when that repair destroys MCSP hardness.
- Situation seed: For each m, imagine a random robust family R_m of 2^{Dm} truth tables, each N=2^m bits and farther than r=2^{eta m} from every circuit of size 2^{epsilon m}. Replace the random choice by a candidate E-uniform sequential selector S_m(a) that additionally supports indexed block restarts.
- Varied variable: lambda, the block-length exponent in B=2^{lambda m} for the restart or interval decoder; tau(lambda) and chi(lambda) are measured as dependent access exponents.
- Held-fixed controls: MCSP threshold s_m=2^{epsilon m} with constant epsilon, distinct-image entropy D and kappa-density of source lengths, no advice in length selection or row selection, target extraction by certificate-index multiplexing into E, unrestricted Boolean circuit lower bound as the target measure
- Expected observation: When lambda and the associated restart exponents fall below epsilon, every selected row becomes circuit-easy despite random-carrier intuition. Only purely sequential or decoder-hard selectors with alpha_int>=epsilon remain target-preserving.
- Transfer certificate needed: A formal access-profile lower bound for S_m showing alpha_int(S)>=epsilon, or a nonrelativizing non-natural proof of robust bad-ball disjointness that does not introduce subthreshold interval decoders.

## Next Experiment

Audit one candidate sequential selector family with declared tau(lambda): monotone lexicographic search using a PSPACE predicate, time-hierarchy diagonal row emitters, or proof-transcript emitters, and compute whether any hidden checkpoint gives alpha_int<epsilon.
