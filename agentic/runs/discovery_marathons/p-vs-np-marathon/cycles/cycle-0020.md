# cycle-0020

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: Semantic Block-Cover Gate

## Candidate Lemma

For generated-OR carriers, the valid source-side obstruction is the minimum semantic block cover, not the singleton range sum. A subthreshold block cover is a falsifier of any claimed N^{1+epsilon} general-circuit lower bound, while the target bridge remains the same q,rho<1+epsilon substitution lemma.

## Definitions

- source object: H_N(x)=\bigvee_{j\le t(N)} SAT(G_{N,j}(x)), where |x|=N, t(N)=N^q, each G_{N,j}(x) is a valid SAT instance of length L=(\log N)^d, and the shared generator has circuit/output cost N^{\rho+o(1)}.
- target object: SAT on inputs of length L and the consequence SAT\notin P/poly, hence NP\nsubseteq P/poly, obtained only by contrapositive substitution into H_N.
- controlled interface: one common length-L SAT circuit may be substituted into all generated queries; no per-query or per-block target advice is allowed in the target transfer, and the OR fan-in is t=N^q.
- target-preserving condition: max{q,rho}<1+epsilon, d>1 or another lookup-safe regime, valid encodings for every generated query, and source lower bounds against nonuniform general circuits for H_N.
- For a partition Pi of [t], define R_B={ (G_{N,j}(x))_{j in B}: x in {0,1}^N } and F_B((phi_j)_{j in B})=\bigvee_{j in B} SAT(phi_j).
- K_B is the minimum circuit size of F_B restricted to R_B, and M_N=min_{Pi}\sum_{B in Pi} K_B.

## Assumptions

- The generator output can be shared among all block predicates with cost N^{rho+o(1)} plus routing N^{q+o(1)}.
- The block circuits K_B are nonuniform and range-restricted; this is intentional because source lower bounds are against nonuniform general circuits.
- The target substitution uses a single SAT_L circuit and therefore does not inherit the stronger per-block advice used only in the source falsifier audit.
- There is fixed slack delta>0 with max{q,rho}<=1+epsilon-delta when deriving the clean necessary lower bound on M_N.

## Equations

- target_substitution: `SAT_L\in SIZE(L^c)\ \Rightarrow\ C(H_N)\le N^{\rho+o(1)}+N^q L^{c+O(1)}=N^{\max\{\rho,q\}+o(1)}.`. Valid when: Valid when the generator is shareable, all queries have length L=(log N)^d, and one nonuniform SAT_L circuit is reused for every generated query position.
- magnification_contrapositive: `[\ C(H_N)>N^{1+\epsilon}\ \text{eventually}\ \wedge\ \max\{q,\rho\}<1+\epsilon\ ]\ \Rightarrow\ SAT\notin P/poly.`. Valid when: Applies when SAT in P/poly would give some fixed exponent c and polylogarithmic query length makes L^c=N^{o(1)} under the target-preserving interface.
- block_cover_upper_bound: `C(H_N)\le N^{\rho+o(1)}+N^{q+o(1)}+\sum_{B\in\Pi} K_B.`. Valid when: Valid when Pi is any nonuniform partition of query positions and each K_B circuit decides the block OR predicate only on its generated tuple range R_B.
- necessary_block_gate: `C(H_N)>N^{1+\epsilon}\ \Rightarrow\ M_N:=\min_{\Pi}\sum_{B\in\Pi}K_B\ge N^{1+\epsilon-o(1)}.`. Valid when: Requires the generator and routing overheads to be below N^{1+epsilon} by fixed polynomial slack so that a subthreshold block cover would contradict the source lower bound.

## Attempted Derivation

- Fix N, t=N^q, L=(log N)^d, and generator G_N producing all query strings G_{N,1}(x),...,G_{N,t}(x).
- Assume SAT_L has circuits of size L^c. Compute G_N once, feed the same SAT_L circuit to each of the t positions, and OR the answers; this gives size N^{rho+o(1)}+N^q L^{c+O(1)}.
- Since L is polylogarithmic, any fixed SAT P/poly exponent contributes only N^{o(1)} per query, so max{q,rho}<1+epsilon gives the valid contrapositive target implication.
- For the source audit, take any nonuniform partition Pi of positions. For each block B, use an optimal range-restricted circuit D_B of size K_B deciding whether any generated formula in that block is satisfiable.
- Compute G_N once, route each block tuple to D_B, then OR the block outputs. This yields C(H_N)<=N^{rho+o(1)}+N^{q+o(1)}+sum_B K_B.
- Therefore a claimed lower bound C(H_N)>N^{1+epsilon} forces M_N>=N^{1+epsilon-o(1)} whenever generator and routing costs have fixed slack below the threshold.
- This repairs the previous semantic-cover gate: singleton S_N is only the partition into singletons and can miss block-level OR compression.

Blocking gap: No direct-sum theorem converts M_N>=N^{1+epsilon-o(1)} into C(H_N)>N^{1+epsilon}. A circuit for H_N may compute the union of positive preimages without decomposing along any chosen partition.

## Falsifiers

- block semantic collapse: M_N<N^{1+epsilon-o(1)} for a nonuniform partition even though singleton S_N appears large
- dominating coordinate: each block contains an always-satisfiable generated formula, making H_N or block predicates easy
- threshold collapse: max{q,rho}>=1+epsilon invalidates the target-preserving magnification inequality
- nonuniform leakage: a source lower-bound argument ignores range-restricted per-block circuits that are legal in the general-circuit source model
- model mismatch: proving lower bounds only for uniform algorithms or restricted circuits does not imply the required nonuniform SIZE lower bound for H_N
- natural-proof pressure: a constructive large property proving the H_N lower bound against P/poly would need to be non-natural or outside the standard PRG-based natural proofs obstruction

## Learning

Cycle 20 sharpens the generated-OR route: the valid target bridge is unchanged, but the source plausibility gate must minimize over semantic block covers. Singleton range complexity is too weak because OR compression and nonuniform block advice can falsify an N^{1+epsilon} source lower bound. This is route-level progress, not a proof of P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The route now depends on whether semantic richness survives OR compression. A concrete generated-OR example can separate singleton cover intuition from the valid block-cover obligation without changing the target transfer.
- Situation seed: Let L=(log N)^2, t=N^q with q=1+epsilon/3, and rho=1+epsilon/3. Partition positions into blocks of size N^kappa. In each block, include many decoy generated SAT formulas with large ranges, but also include one tag-controlled formula that is a fixed satisfiable tautology whenever a simple block tag holds; choose tags so the block OR is computable by a small circuit.
- Varied variable: kappa, the logarithmic block size exponent controlling how many query positions share one simple block-level OR certificate.
- Held-fixed controls: Keep max{q,rho}<1+epsilon so the SAT-to-H_N target substitution remains valid., Keep L=(log N)^2 so exhaustive truth-table lookup costs are superpolynomial in N and do not explain the collapse., Use valid SAT encodings for every generated query., Allow no per-position advice in the target transfer, but allow nonuniform range-restricted block circuits in the source falsifier audit.
- Expected observation: As kappa grows, singleton semantic cover can remain large because of decoy ranges, while M_N drops to about N^{q-kappa+o(1)} or lower. Once this is below N^{1+epsilon}, the proposed source lower bound is falsified although the target bridge equation remains valid.
- Transfer certificate needed: Before this intuition affects proof obligations, formalize the partition Pi, prove the range-restricted K_B upper bounds, and verify that the same generator still satisfies the target-clean common-SAT-circuit substitution condition.

## Next Experiment

Instantiate M_N for a nontrivial generator without dominated coordinates, e.g. a universal verifier family whose queries are Cook-Levin encodings of polylog-size computations, and compute whether block predicates admit compression below N^{1+epsilon}.

# Barrier-Aware Lower-Bound Route: Real PTF Largeness Gate

## Candidate Lemma

Degree-only real polynomial-threshold SAT separators do not automatically naturalize. A valid natural-property transfer additionally needs an explicit density lower bound; degree 1 can have exponentially small acceptance.

## Definitions

- source object: explicit real polynomial-threshold separator p_N on N=2^m truth-table bits, degree d, coefficient bit length B, with p_N(SAT_m)>=0 and p_N(TT(C))<0 for SIZE(m^k).
- target object: Razborov-Rudich natural property against SIZE(m^k): poly(N)-decidable, N^{-a}-large, and useful.
- controlled interface: send p_N to P_N={x in {0,1}^N : p_N(x)>=0}; preserve constructivity and usefulness before asking for largeness.
- target-preserving condition: the same P_N must accept the SAT truth table, reject every m-input circuit of size m^k, and have density at least N^{-a} without nonuniform leakage.

## Assumptions

- p_N is uniformly evaluable in poly(N); degree alone is not the constructivity certificate.
- Usefulness quantifies over every truth table computed by circuits of size m^k.
- The audit is route-level: it can create a natural-proof falsifier, not a proof of P != NP.

## Equations

- induced_density: `\mu_N(P_N)=2^{-N}\left|\{x\in\{0,1\}^N:p_N(x)\ge 0\}\right|`. Valid when: Valid when P_N is the Boolean truth-table property induced by a uniformly evaluable threshold polynomial.
- degree_one_counterexample: `p_N^*(x)=\sum_{i=1}^N x_i-(N-\tfrac12),\quad \deg(p_N^*)=1,\quad \mu_N(\{p_N^*\ge0\})=2^{-N}`. Valid when: Valid for Boolean inputs with the usual zero-one encoding and threshold acceptance of real polynomials.
- naturalization_gate: `\mathrm{poly}(N)\text{-eval}(p_N)\wedge \mathrm{useful}_k(P_N)\wedge \mu_N(P_N)\ge N^{-a}\Rightarrow P_N\text{ is }RR(k,a)\text{-natural}`. Valid when: Applies after the induced property uses the same input length and excludes all target small-circuit truth tables.

## Attempted Derivation

- Assume a uniform real PTF separator p_N with degree O(log N) and poly(N)-time evaluation.
- Induce P_N={x:p_N(x)>=0}; constructivity and usefulness are valid if p_N rejects every SIZE(m^k) truth table.
- Try to inherit the F_2 low-degree weight floor from cycle 19; this is invalid because real threshold inequalities do not obey Reed-Muller minimum distance.
- The singleton threshold p_N^* has degree 1 and density 2^{-N}, so the missing bridge is an anti-concentration or largeness certificate for the actual separator.

Blocking gap: No condition from real degree, coefficient bit length, or evaluation circuit size alone forces mu_N(P_N)>=N^{-a}.

## Falsifiers

- falsifier: p_N^*=sum_i x_i-(N-1/2) is degree 1 yet accepts only 1^N, so low real degree plus explicitness is not large.
- falsifier: a Hamming ball around SAT_m may be useful if disjoint from small circuits, but for small radius its density is exponentially tiny.
- falsifier: coefficients encoding SAT_m nonuniformly can fake separation while losing the uniform target-preserving interface.
- falsifier: if polynomial-density usefulness is proved black-box for all oracles, relativization blocks any direct P vs NP conclusion.

## Learning

Cycle 20 proves a route gate: low real threshold degree is neither a valid naturalness certificate nor a barrier escape by itself. The exact missing parameter is acceptance density or anti-concentration, with uniformity and usefulness preserved.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: Real PTF separators look like an escape from the F_2 low-degree gate; varying density tests whether the escape is real or only below the natural-proof threshold.
- Situation seed: Use linear thresholds p_{N,r}(x)=r-d_H(x,SAT_N), Hamming balls around the SAT truth table, and consider only radii still disjoint from every SIZE(m^k) truth table.
- Varied variable: beta in r=N/2-beta*sqrt(N log N), which controls the ball density.
- Held-fixed controls: center is the exact SAT_N truth table and is generable in poly(N) time from length-N indexing, target usefulness remains rejection of all SIZE(m^k) truth tables, property evaluation is uniform poly(N) given x and the radius, target class and input length N=2^m are unchanged
- Expected observation: When beta is constant the density is polynomially small, so a disjointness proof would yield a valid natural property; for much smaller balls the route escapes naturalness but gives no lower-bound transfer.
- Transfer certificate needed: A proof that the chosen beta-ball is disjoint from all SIZE(m^k) truth tables plus a uniform coefficient-generation audit; otherwise the experiment is only a falsifier probe.

## Next Experiment

Audit bounded-margin real PTF separators: determine whether normalization plus margin lower bounds imply polynomial density or whether singleton-style thresholds still refute the bridge.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Entropy-aware checkpoint cap: any proposed sequential MCSP no-side certificate source has a nonuniform upper-bound profile determined by certificate entropy, checkpoint storage, and block simulation. If the claimed MCSP threshold exceeds this cap, the source is invalid; if it survives, the carrier-to-E transfer exponent is capped by the same profile divided by the density gap.

## Definitions

- source object: a uniform streaming verifier V_m with certificate length b(m), entropy exponent eta=limsup_m log b(m)/m, configuration length 2^{sigma m+o(m)}, and accepted outputs T_{m,c} in {0,1}^{2^m}.
- target object: MCSP no-side at threshold s(m)=2^{epsilon m} for truth tables of length N=2^m, transferred to an E language requiring nonuniform circuits larger than 2^{delta n}.
- controlled interface: exhaustive canonicalization over short certificates chooses an accepted stream, while checkpoint circuitization gives a nonuniform circuit upper bound for every emitted table.
- target-preserving condition: source lengths are kappa-dense, V is uniform and advice-free, b(m)=O(m) for E extraction, and epsilon <= alpha_V so the checkpoint cap is not a falsifier.
- C(T) denotes the minimum nonuniform Boolean circuit size of the m-bit function with truth table T.
- tau_V(lambda) is the exponent for circuitizing V over a block of 2^{lambda m} output positions from a checkpoint, certificate, and offset.

## Assumptions

- For every fixed 0<lambda<1, a block of 2^{lambda m} streaming steps can be unrolled or otherwise circuitized with size 2^{tau_V(lambda)m+o(m)}.
- Checkpoint states for V have encodings of length 2^{sigma m+o(m)} and may be hardwired as nonuniform constants when upper-bounding C(T_{m,c}).
- MCSP soundness means every accepted output T_{m,c} has C(T_{m,c})>2^{epsilon m}; no average-case or promise-only interpretation is allowed.
- The E extraction uses a uniform exhaustive search over certificates, so the target-preserving regime requires b(m)=O(m), not merely subexponential certificate entropy.

## Equations

- entropy-aware-cap: `\alpha_V(\eta,\sigma)=\inf_{0<\lambda<1}\max\{\eta,1-\lambda+\sigma,\tau_V(\lambda)\}`. Valid when: Valid when block simulation and checkpoint selection are circuitizable uniformly, and exponents are measured relative to m.
- emitted-table-upper-bound: `C(T_{m,c})\le 2^{(\alpha_V(\eta,\sigma)+o(1))m}`. Valid when: Valid when the certificate and checkpoints may be hardwired as nonuniform constants in the MCSP circuit model.
- sound-source-necessary-condition: `\epsilon\le \alpha_V(\eta,\sigma)+o(1)`. Valid when: Applies when accepted-output soundness claims MCSP no-side at threshold 2^{epsilon m} for every accepted stream.
- cap-aware-transfer-ceiling: `\delta<\epsilon/\kappa\le (\alpha_V(\eta,\sigma)+o(1))/\kappa`. Valid when: Requires the target-preserving dense source schedule and the checkpoint cap not to falsify the MCSP threshold.
- e-canonicalization-budget: `b(m)=O(m)\Rightarrow \text{search time }2^{O(m)},\quad b(m)=\omega(m)\Rightarrow \text{exhaustive search not certified in E}`. Valid when: Valid when the extraction locates the canonical accepted certificate by uniform exhaustive enumeration without extra advice.

## Attempted Derivation

- Start with the viable sparse source shape: O(m)-bit certificates, uniform sequential verifier, accepted truth tables promised to have C(T)>2^{epsilon m}.
- Try to increase robustness by appending salt z of length b(m)=2^{eta m} and accepting many salted streams, hoping for density without changing the MCSP threshold.
- Run the entropy-aware cap: the certificate term eta enters alpha_V, while exhaustive canonicalization now costs about 2^{b(m)}, not 2^{O(m)} unless b(m)=O(m).
- If eta is small but positive, the image is still far from large yet the E extraction is already not certified by exhaustive search.
- If eta approaches 1, largeness can appear, but constructivity plus high-MCSP usefulness becomes a natural-proofs falsifier under PRF assumptions.
- Therefore salt does not repair the source problem: the target-preserving regime remains sparse, short-certificate, non-large, and cap-aware.

Blocking gap: No non-enumerative, nonuniform-free proof is known that a sparse canonical stream has MCSP complexity above 2^{epsilon m} while every checkpoint/block upper bound stays at exponent at least epsilon.

## Falsifiers

- Checkpoint falsifier: some lambda gives max{eta,1-lambda+sigma,tau_V(lambda)}<epsilon, yielding circuits smaller than the claimed MCSP threshold.
- Extraction falsifier: b(m)=omega(m) and the only locator is exhaustive search, so the canonical language is not certified in E.
- Natural-proofs falsifier: a salt-rich constructive carrier becomes large enough to collide with standard PRF-based barrier assumptions.
- Nonuniform leakage falsifier: advice supplies the accepting certificate or source length selector, so the consequence is only nonuniform and not a valid E extraction.
- Threshold-collapse falsifier: the only soundness proof is brute-force enumeration against circuits of size O(m/log m), giving epsilon_m=O(log m/m) and delta=o(1).
- Relativization/algebrization obstruction: a proof using only black-box truth-table access cannot certify MCSP no-side against nonuniform circuit syntax; the viable object must be circuit-syntactic, non-large, and outside merely relativizing evidence.

## Learning

Cycle 20 adds an entropy-aware checkpoint cap. The valid route is narrower: short certificates keep the carrier sparse and E-canonicalizable, but any source must satisfy epsilon<=alpha_V and cannot use salt to buy density. This is route-level progress and a falsifier for source proposals, not a proof of P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for proposed MCSP certificate sources.`
- Rationale: The branch already has a valid carrier-to-E bridge; the unresolved issue is whether density or salt can repair source construction without breaking uniform extraction or triggering barriers.
- Situation seed: A salt-augmented MCSP certificate family V_{m,eta}: a short core certificate p plus salt z of length b(m)=2^{eta m} drives a uniform sequential verifier emitting a length-2^m truth table claimed to be outside SIZE(2^{epsilon m}).
- Varied variable: certificate entropy exponent eta in b(m)=2^{eta m}, with eta=0 interpreted as subexponential entropy and the target-preserving subcase b(m)=O(m).
- Held-fixed controls: MCSP threshold s(m)=2^{epsilon m} with constant epsilon>0., kappa-dense source lengths for all-length transfer., Uniform advice-free verifier and canonical lexicographic extraction., Nonuniform circuit model for both MCSP upper bounds and target lower bounds.
- Expected observation: For eta>0, exhaustive canonicalization stops being E-time before the image becomes usefully large; for eta near 1, largeness may appear but constructivity becomes a natural-proofs falsifier. Thus salt cannot be a free target-preserving density repair.
- Transfer certificate needed: A formal certificate must show b(m)=O(m), alpha_V(0,sigma)>=epsilon, kappa-density, and sound MCSP no-side for every accepted stream without nonuniform selectors or black-box relativizing proof methods.

## Next Experiment

Pick a concrete globally sequential verifier template, compute tau_V(lambda) and sigma, and test whether any constant epsilon survives the entropy-aware checkpoint cap before attempting a soundness proof.
