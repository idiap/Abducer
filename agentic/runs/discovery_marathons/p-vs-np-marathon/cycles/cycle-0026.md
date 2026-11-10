# cycle-0026

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Approximate selector leakage lemma: for a generated-OR carrier H_N, any small circuit selecting one queried formula whose SAT value agrees with H_N except on M_N inputs, together with a small promise solver for SAT on the selected image, gives a circuit for H_N of size selector plus extractor plus promise-solver plus O(N M_N). Hence an N^{1+epsilon} source lower bound must defeat approximate selectors with M_N<N^{epsilon-o(1)}, not only exact witness selectors.

## Definitions

- source object: H_N(x)=OR_{j<t(N)} SAT(E_N(x,j)) on N input bits, with t(N)=N^q, SAT instance length L(N)=(log N)^d, and coordinate extractor E_N of circuit size at most N^{rho+o(1)}.
- target object: SAT on length n inputs is excluded from SIZE(n^c) for every fixed c, yielding the nonuniform target consequence NP not subset P/poly only after the bridge is valid for all large N in the chosen length map.
- controlled interface: a SAT upper bound may be substituted only through the generated query strings E_N(x,j), while selectors, promise solvers, and correction tables are charged as nonuniform leakage in the source model.
- target-preserving condition: q<1+epsilon, rho<1+epsilon, L(N)^c=N^{o(1)} for every fixed c, and no hidden advice may be moved from the target SAT circuit into the carrier generator or selector.
- approximate selector: a circuit sigma_N maps x to an index in [t(N)], producing A_{sigma,P}(x)=P_N(E_N(x,sigma_N(x))) for a promise SAT solver P_N on the selected image.
- bad set: B_{sigma,P}={x in {0,1}^N : A_{sigma,P}(x) != H_N(x)}; a sparse bad set is correctable by equality-DNF advice of size O(N|B_{sigma,P}|).

## Assumptions

- E_N is explicit enough that the coordinate E_N(x,j) is computable by nonuniform circuits of size N^{rho+o(1)}.
- The claimed source lower bound is SIZE(H_N)>N^{1+epsilon} against unrestricted Boolean circuits on N input bits.
- The target transfer is nonadaptive OR-of-queries substitution; this lemma audits extra nonuniform leakage not used by the clean target bridge.
- Promise solver P_N need only agree with SAT on the selected image U_{sigma}={E_N(x,sigma_N(x)):x in {0,1}^N}.
- Circuit size for equality with one N-bit exceptional input is O(N), so M exceptions cost O(NM) nonuniformly.

## Equations

- generated_or_carrier: `H_N(x)=\bigvee_{j<t(N)} SAT(E_N(x,j)),\qquad t(N)=N^q,\quad L(N)=(\log N)^d.`. Valid when: Valid when the source carrier is the explicit generated-OR family with named query count, query length, and coordinate extractor.
- clean_target_substitution: `SAT_L\in SIZE(L^c)\ \Longrightarrow\ C(H_N)\le N^{\rho+o(1)}+N^q L^c=N^{\max\{\rho,q\}+o(1)}.`. Valid when: Applies after the reduction preserves nonuniform size accounting and L(N)^c is subpolynomial for every fixed target exponent c.
- approx_selector_upper_bound: `C(H_N)\le C(\sigma_N)+C(E_N)+C(P_N)+O(L+\log t)+O(N\,|B_{\sigma,P}|).`. Valid when: Valid when P_N agrees with SAT on the selected image and the remaining disagreements are corrected by nonuniform equality tests.
- bad_set_threshold: `|B_{\sigma,P}|\le N^{\delta}\ \Longrightarrow\ O(N|B_{\sigma,P}|)\le N^{1+\delta+o(1)}.`. Valid when: Requires the correction to be by explicit exceptional-input advice in unrestricted circuits over N-bit carrier inputs.
- source_obligation_minimax: `\Lambda_N:=\min_{\sigma,P}\{C(\sigma_N)+C(E_N)+C(P_N)+N|B_{\sigma,P}|\}>N^{1+\epsilon-o(1)}.`. Valid when: Necessary when an N^{1+epsilon} lower bound for H_N is asserted in the same unrestricted circuit model.

## Attempted Derivation

- Fix sigma_N and P_N, and compute A(x)=P_N(E_N(x,sigma_N(x))).
- On inputs outside B_{sigma,P}, A(x)=H_N(x) by definition of the bad set.
- For each bad input b, add an equality gate EQ_b(x); XOR A with OR_{b in B} EQ_b(x) to flip exactly the wrong outputs.
- The correction costs O(N|B|), while selector, extractor, and promise solver costs add linearly up to standard fan-in overhead.
- Thus any sparse-error approximate selector with small selected-range SAT solver gives a subthreshold circuit for H_N and refutes the proposed source lower bound.
- Combining this with the clean target bridge shows the remaining route obligation is a minimax lower bound against all approximate selector-plus-promise-solver pairs.

Blocking gap: No concrete E_N is known for which Lambda_N>N^{1+epsilon-o(1)} can be proved in unrestricted circuits; proving it appears to require non-natural, selector-resistant lower-bound machinery rather than entropy counting.

## Falsifiers

- approximate-selector falsifier: a selector correct except on N^{epsilon-eta} carrier inputs plus a subthreshold selected-range promise solver gives H_N circuits below N^{1+epsilon}
- exact-selector leakage from cycle 25 remains a special case with empty bad set
- threshold collapse if max{q,rho}>=1+epsilon in the clean target substitution
- lookup falsifier when query length and variable entropy make SAT on the generated range tabulatable below the source threshold
- nonuniform leakage through a compact selected image U_sigma with easy promise SAT despite high full-range entropy
- natural-proof risk: a large constructive property proving selector-cover hardness for many generators would conflict with standard P/poly pseudorandom-function assumptions

## Learning

Cycle 26 adds an approximate-selector gate. Exact witness selection was too weak as a source audit: even a selector wrong on N^{delta} inputs collapses H_N below N^{1+epsilon} when delta<epsilon, because unrestricted circuits correct the errors with equality advice. The valid route obligation is the minimax lower bound Lambda_N>N^{1+epsilon-o(1)}, while the clean target bridge q,rho<1+epsilon remains intact.

## Gedanken Experiment Design Seed

- Need decision: `design now as a falsifier probe`
- Rationale: The branch now hinges on whether source lower bounds for generated-OR carriers can survive nonuniform leakage through approximate witness selection; another abstract bridge restatement would not test the new minimax threshold.
- Situation seed: Take H_N=OR_{j<N^q} SAT(E_N(x,j)) with L=(log N)^d, q,rho<1+epsilon. Plant an easy selected subrange R_sel whose formulas have a tiny promise SAT solver, and arrange that all but N^delta positive inputs have at least one satisfiable query in R_sel; sigma_N chooses the first planted satisfiable-looking coordinate.
- Varied variable: bad-set exponent delta where |B_{sigma,P}|=N^delta.
- Held-fixed controls: q<1+epsilon and rho<1+epsilon so the clean target bridge remains valid, d>1 so exhaustive truth-table lookup for all generated formulas is not automatically subthreshold, the selected-image promise solver is charged as source-side nonuniform advice, the target SAT circuit is not allowed to encode sigma_N or the exceptional set
- Expected observation: If delta<epsilon and the planted selected range has solver size below N^{1+epsilon-eta}, the carrier source lower bound is killed by O(N^{1+delta}) correction. If delta>epsilon, sparse correction no longer suffices, so the route must prove a real approximate-selector lower bound.
- Transfer certificate needed: A formal circuit construction for sigma_N, a promise solver bound on U_sigma, and a rigorous count of bad inputs; conversely, a promotion certificate must lower-bound Lambda_N against every sigma_N and P_N in unrestricted circuits.

## Next Experiment

Instantiate the thought experiment with a block generator E_N whose coordinates are grouped into planted easy and hard ranges; compute the smallest delta forced by coverage of positive inputs and test whether selected-range promise SAT stays subthreshold.

# Barrier-Aware Lower-Bound Route: Sparse Fourier Naturalization Gate

## Candidate Lemma

Let N=2^m. Suppose a total poly(N)-decidable Boolean property R_N on N-bit truth tables accepts the SAT_m truth table, rejects every truth table computed by SIZE(m^k) circuits, and has Walsh-Fourier support M_N<=N^a for fixed a. Then R_N is a valid Razborov-Rudich natural property of density at least N^{-a} useful against SIZE(m^k). Hence any route using such a sparse spectral separator naturalizes; a barrier escape must use superpolynomial Fourier support, nonconstructivity, a promise-only domain, or weakened usefulness.

## Definitions

- source object: a Walsh-sparse explicit truth-table separator R_N:{0,1}^N->{0,1} for SAT_m, with N=2^m, R_N(T_{SAT_m})=1, poly(N)-time evaluation, and Fourier support M_N.
- target object: nonuniform Boolean circuits of size m^k on m inputs, identified with their N-bit truth tables; the PRF audit subtarget is any target-computable function family secure against poly(N)-time distinguishers.
- controlled interface: map the spectral proof object to a natural-proof property by preserving constructivity, deriving largeness from Fourier uncertainty, and importing usefulness from rejection of all target circuit truth tables.
- target-preserving condition: the property is total on the full N-bit truth-table cube, uses the same m and N=2^m parameters, rejects all target truth tables without advice leakage, and does not hide PRF outputs behind a promise.
- Walsh character convention: chi_S(x)=(-1)^{sum_{i in S} x_i} and Fourier support is measured over the full Boolean cube {0,1}^N.

## Assumptions

- Fixed constants k and a are independent of m.
- R_N is a Boolean indicator, not merely a signed or approximate score.
- Usefulness is universal: for every circuit C of size m^k, R_N(T_C)=0.
- Constructivity is uniform poly(N) evaluation from the full truth table x.
- The natural-proof audit is conditional on target-computable PRFs with security at advantage at least N^{-a} against poly(N)-time distinguishers.

## Equations

- walsh_sparsity: `R_N(x)=\sum_{S\subseteq [N]}\widehat R_N(S)\chi_S(x),\quad M_N=|\{S:\widehat R_N(S)\ne 0\}|`. Valid when: Valid when R_N is treated as a total real-valued indicator on the full truth-table cube {0,1}^N.
- uncertainty_largeness: `\mu_N(R)=\Pr_{X\leftarrow \{0,1\}^N}[R_N(X)=1]=|\operatorname{supp}(R_N)|/2^N\ge 1/M_N`. Valid when: Applies when R_N is nonzero and Walsh sparsity M_N is measured on the same full N-bit cube.
- polynomial_density_threshold: `M_N\le N^a\quad\Rightarrow\quad \mu_N(R)\ge N^{-a}`. Valid when: Requires a fixed exponent a independent of m and no hidden restriction to a smaller promise domain.
- prf_distinguisher_advantage: `\operatorname{Adv}_D\ge \Pr_{U}[R_N(U)=1]-\Pr_{K}[R_N(T_{F_K})=1]\ge 1/M_N`. Valid when: Applies after usefulness rejects every target-computable PRF truth table and the evaluator D runs in polynomial time in N.

## Attempted Derivation

- Type the source as a total Boolean property R_N on all N-bit truth tables, with N=2^m and R_N(T_{SAT_m})=1.
- Because R_N is nonzero, apply finite-group Fourier uncertainty on (Z_2)^N: |supp(R_N)| |supp(\widehat R_N)| >= 2^N.
- Substitute |supp(\widehat R_N)|=M_N to get density mu_N(R)>=1/M_N.
- If M_N<=N^a, the property is large with inverse-polynomial density in the truth-table length N.
- The assumed evaluator gives constructivity, and rejection of all SIZE(m^k) truth tables gives usefulness against the named target class.
- If target-computable PRFs exist with poly(N)-time security, R_N itself is a distinguisher with advantage at least 1/M_N, so the proposed lower-bound route lies inside the natural-proof obstruction.

Blocking gap: The derivation does not construct such an R_N and does not prove PRFs exist; it only proves that an exact low-sparsity spectral separator is barrier-invalid under the standard PRF hypothesis.

## Falsifiers

- Point-mass acceptance R_N(x)=1[x=T_{SAT_m}] is a falsifier to density-free spectral optimism: it can be useful but has M_N=2^N and density 2^{-N}.
- Low Fourier degree alone is not enough; OR/AND-type predicates can have full or superpolynomial support, so the new gate is exact support, not degree.
- A promise-only spectral test on encoded truth tables falsifies naive application of uncertainty unless extended to a total poly(N)-constructive property on {0,1}^N.
- If the target rejection omits PRF truth tables through advice or padding leakage, the PRF distinguisher transfer is invalid.

## Learning

Cycle 26 identifies exact Walsh support as a new naturalization threshold. Low support M_N<=poly(N), together with total constructivity and full usefulness, forces density by Fourier uncertainty and yields a valid natural-proof/PRF obstruction. This is route-level barrier progress only.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch needs a concrete quantitative threshold for spectral separator routes; exact Fourier sparsity supplies a measurable parameter rather than another natural-proof slogan.
- Situation seed: Imagine a family R_N of total poly(N)-time evaluable Walsh-sparse properties that accept the padded SAT_m truth table and reject every SIZE(m^k) truth table, with N=2^m.
- Varied variable: alpha=log_N M_N, the Fourier support exponent of R_N.
- Held-fixed controls: N=2^m and the target class SIZE(m^k) are fixed across the transfer., R_N is total on the full truth-table cube and has no promise restriction., The evaluator for R_N runs in poly(N) time uniformly., Usefulness rejects every target circuit truth table, not merely most or encoded ones.
- Expected observation: For constant alpha, uncertainty forces density at least N^{-alpha}, giving a natural property and PRF distinguisher advantage N^{-alpha}; for alpha=omega(1), the largeness bridge collapses and the route may escape only if constructivity and usefulness still transfer.
- Transfer certificate needed: A formal certificate of totality, exact Walsh support bound, uniform poly(N) evaluation, and full target usefulness before the spectral intuition may enter the proof queue.

## Next Experiment

Audit approximate Fourier sparsity: determine whether l1 mass concentration on poly(N) characters also forces a polynomial-density natural property, or whether cancellation gives a genuine falsifier.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Entropy-compressed existential MCSP carrier bridge: if a uniform linear-certificate MCSP verifier has at most 2^{h m+O(1)} accepted certificates at source length m and at least one accepted truth table has circuit complexity greater than 2^{epsilon m}, then lexicographic-rank multiplexing gives an E-uniform target language with lower-bound exponent epsilon/(1+h), and kappa-dense source lengths give all-length exponent any delta<epsilon/((1+h)kappa). This replaces the previous loss factor 1+c by accepted-set entropy h whenever the accepted set is canonical.

## Definitions

- source object: a uniform verifier/emitter V which, on source length m, certificate y in {0,1}^{ell_m} with ell_m<=c m, and index x in {0,1}^m, decides acceptance of y and emits the bit T_{m,y}(x) in time 2^{O(m)}.
- target object: an E language L whose length n_m=m+q_m+O(log m) layer is the multiplexed table M_m(r,x)=T_{m,y_r}(x), where y_r is the r-th accepted certificate in lexicographic order and out-of-range r outputs 0.
- controlled interface: use canonical lexicographic unranking of accepted certificates, not a nonuniform selector, so an existential hard accepted certificate becomes one hard slice of the multiplexed target.
- target-preserving condition: the accepted-set entropy q_m=ceil(log max(1,|A_m|)) is at most h m+O(1), source hard lengths are kappa-dense and uniformly recognizable, and epsilon is below the verifier circuit upper-bound cap alpha_V.

## Assumptions

- For infinitely many or kappa-dense source lengths m, the accepted set A_m is nonempty and contains some y with C(T_{m,y})>2^{epsilon m}.
- Acceptance and bit emission for V are E-uniform: exhaustive lexicographic unranking over all 2^{c m} certificates costs only 2^{O(n_m)} after compression because c and h are constants.
- The lower-bound measure is ordinary Boolean circuit size for truth tables on m input bits and the target language is uniform E, not merely nonuniform advice.
- The padding map from hard target lengths n_m to all lengths has overhead at most kappa in the source parameter, up to o(m) length-coding terms.

## Equations

- accepted_entropy: `q_m=\left\lceil \log_2 \max(1,|A_m|)\right\rceil \le h m+O(1)`. Valid when: Valid when A_m is the canonical accepted certificate set for one fixed verifier and h is a uniform constant entropy-rate upper bound.
- compressed_target_length: `n_m=m+q_m+O(\log m)\le (1+h)m+O(\log m)`. Valid when: Valid when the target input encodes a rank, a table index, and a self-delimiting source length without advice.
- hard_slice_to_multiplex_lower_bound: `C(M_m)\ge \max_{y\in A_m} C(T_{m,y})-O(n_m)>2^{\epsilon m}-O(n_m)`. Valid when: Applies after the hard certificate is included in the lexicographic-rank image and circuits may hardwire its rank.
- all_length_exponent: `\delta<\frac{\epsilon}{(1+h)\kappa}`. Valid when: Requires kappa-dense source lengths, entropy-compressed target length, and padding that preserves uniform E decidability and circuit thresholds.

## Attempted Derivation

- Fix a hard source length m and let A_m be the canonical accepted certificates of V.
- Let q_m=ceil(log max(1,|A_m|)) and define M_m(r,x) by lexicographic unranking of r into A_m, with zero output if r is out of range.
- The unranking scan over 2^{c m} certificates and one final bit-emission call costs 2^{O(m)}, hence 2^{O(n_m)}, so the target language is in E.
- If y* in A_m has C(T_{m,y*})>2^{epsilon m}, let r* be its rank. Any circuit S for M_m, with r* hardwired, gives a circuit S+O(n_m) for T_{m,y*}. Therefore C(M_m)>2^{epsilon m}-O(n_m).
- Since n_m<=(1+h)m+O(log m), the hard target length has exponent epsilon/(1+h)-o(1). Kappa-padding converts kappa-dense hard lengths to all sufficiently large target lengths with any delta<epsilon/((1+h)kappa).

Blocking gap: The derivation does not construct a source verifier with low accepted entropy and an accepted MCSP-hard table; it only proves that such a source would transfer with the sharper entropy loss.

## Falsifiers

- falsifier: |A_m| has entropy rate h_m tending to infinity on the hard lengths, so the lower-bound exponent collapses to o(1).
- falsifier: the accepted set is canonical but contains no table above the claimed MCSP threshold 2^{epsilon m}.
- falsifier: certificate length or verifier overhead is superlinear enough that unranking is no longer E-uniform at the compressed target length.
- falsifier: source lengths are chosen by nonuniform advice, invalidating the E target language even though the nonuniform lower-bound statement looks plausible.
- falsifier: epsilon is larger than the verifier cap alpha_V, so the verifier itself supplies smaller circuits for every emitted table.
- falsifier: a dense constructive accepted property reappears; then the source may fall back into the natural-proofs largeness obstruction rather than a sparse carrier route.

## Learning

Cycle 26 sharpens the multiplexing repair: the exponent loss is controlled by accepted-set entropy h, not raw certificate length c. Canonical lexicographic unranking is E-uniform for linear certificates, so existential hard accepted witnesses transfer without a selector and without easy-contamination failure. The remaining obstruction is now a low-entropy, cap-compatible, non-natural MCSP source with constant epsilon; unbounded accepted entropy is a valid quantitative falsifier.

## Gedanken Experiment Design Seed

- Need decision: `Design and use now as a falsifier probe for source proposals.`
- Rationale: The previous bridge used raw certificate rate c. The concrete question is whether accepted-set entropy h, not certificate length, is the true quantitative loss parameter for the MCSP carrier route.
- Situation seed: A family of MCSP certificate verifiers V_m with ell_m=c m certificate bits, E-time bit emission, kappa-dense hard source lengths, and exactly 2^{h m} accepted certificates arranged lexicographically; one accepted certificate emits a table of circuit complexity greater than 2^{epsilon m}.
- Varied variable: accepted-set entropy rate h in the interval 0<=h<=c, while keeping raw certificate length c fixed.
- Held-fixed controls: source MCSP threshold 2^{epsilon m} with epsilon<=alpha_V, kappa-density of hard source lengths, E-uniform lexicographic unranking by exhaustive scan, no nonuniform selector or length advice, ordinary Boolean circuit-size lower-bound target
- Expected observation: The target exponent should follow the curve delta_max=epsilon/((1+h)kappa), interpolating from no selector loss at h=0 to the old full-certificate loss at h=c. If a proposed source violates this curve, the violation is a quantitative falsifier for the transfer claim.
- Transfer certificate needed: A formal proof that lexicographic rank multiplexing is E-uniform, includes the hard accepted certificate as a slice, and preserves lower bounds under hardwiring and kappa-padding.

## Next Experiment

Audit candidate MCSP certificate sources for accepted-set entropy h: start with deterministic proof-transcript carriers and compute whether their accepted transcript count is O(2^{h m}) with h<c, while checking alpha_V and natural-proofs largeness.
