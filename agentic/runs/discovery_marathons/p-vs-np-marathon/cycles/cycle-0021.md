# cycle-0021

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: Shared-Generator Semantic Block-Cover Gate

## Candidate Lemma

For a generated-OR carrier, any source lower bound C(H_N)>N^{1+epsilon} must defeat not only singleton SAT substitution but every shared-generator semantic block cover of the generated query tuple. The target bridge remains valid when max{rho,q}<1+epsilon, but source plausibility now requires a high lower bound on min_Pi sum_{B in Pi} C_{R_B}(OR-SAT_B).

## Definitions

- source object: H_N(x)=OR_{1<=j<=M} SAT(G_{N,j}(x)), with input length N, M=N^q, query length L(N)=(log N)^d, and a nonuniform generator circuit G_N of size N^{rho+o(1)} outputting all query strings.
- target object: SAT restricted to formulas of length L(N), with the target consequence SAT notin P/poly if the bridge contradicts every fixed polynomial-size SAT circuit family.
- controlled interface: substitute a candidate SAT_L circuit only at generated query positions, and separately audit every block predicate that may exploit the realized tuple range of the generator.
- target-preserving condition: q<1+epsilon and rho<1+epsilon, with d>1 or a certified lookup-safety condition, so the carrier upper bound from SAT circuits is below the claimed N^{1+epsilon} source threshold.
- For a partition Pi of [M], R_B={ (G_{N,j}(x))_{j in B}: x in {0,1}^N } is the realized tuple range of block B.
- C_{R_B}(OR-SAT_B) is the minimum circuit size of a predicate Q_B on |B| generated formulas that agrees with OR_{j in B} SAT(y_j) on all tuples in R_B; behavior outside R_B is irrelevant.
- A shared-generator block cover has cost C(G_N)+sum_{B in Pi} C_{R_B}(OR-SAT_B)+O(|Pi|).

## Assumptions

- Circuit size is nonuniform Boolean circuit size with fan-in two unless stated otherwise.
- The generator has no target advice depending on a hypothetical SAT circuit beyond its fixed nonuniform description for length N.
- The source lower bound is an eventually-all-N lower bound for the explicit carrier H_N, not merely an infinitely-often or average-case statement.
- The range-restricted block circuits are allowed arbitrary nonuniform advice for length N; hence this is a strong falsifier gate for source lower bounds.

## Equations

- E1_target_substitution_upper_bound: `C(H_N) \le N^{\rho+o(1)}+N^q\,C(SAT_L)+O(N^q) \le N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when SAT has circuits of size L^c for a fixed c and L=(log N)^d makes L^c=N^{o(1)}.
- E2_target_preserving_magnification: `\big(C(H_N)>N^{1+\epsilon}\ \text{and}\ \max\{\rho,q\}<1+\epsilon\big)\Rightarrow SAT\notin P/poly`. Valid when: Applies after the generated-OR carrier is target-clean and the lower bound holds against nonuniform circuits for all sufficiently large N.
- E3_shared_block_cover_upper_bound: `C(H_N)\le C(G_N)+\min_{\Pi}\left(\sum_{B\in\Pi} C_{R_B}(OR\text{-}SAT_B)+O(|\Pi|)\right)`. Valid when: Valid when each block circuit only needs to agree on the realized tuple range emitted by the shared generator.
- E4_source_gate_consequence: `C(H_N)>N^{1+\epsilon}\Rightarrow \forall\Pi:\ C(G_N)+\sum_{B\in\Pi} C_{R_B}(OR\text{-}SAT_B)\ge N^{1+\epsilon-o(1)}`. Valid when: Requires the claimed source lower bound to be stronger than every semantic block-cover upper bound, including nonuniform block advice.

## Attempted Derivation

- Let M=N^q and let G_N(x) output the M formulas y_1(x),...,y_M(x) of length L=(log N)^d using N^{rho+o(1)} gates.
- Fix a partition Pi of [M]. For each block B, define R_B as the set of generated tuples y_B(x) and choose a smallest circuit Q_B agreeing with OR_{j in B} SAT(y_j) on R_B.
- Compose one copy of G_N with all Q_B circuits, wire each Q_B to its block tuple, and OR the block answers. This computes H_N exactly.
- The resulting size is N^{rho+o(1)}+sum_B C_{R_B}(OR-SAT_B)+O(|Pi|), proving the shared-generator cover upper bound.
- For singleton blocks, if SAT has L^c-size circuits, then each block cost is at most L^c, giving C(H_N)<=N^{rho+o(1)}+N^qL^c and hence the target-preserving contradiction when max{rho,q}<1+epsilon.
- Therefore a valid source lower bound must simultaneously rule out all nonuniform semantic block covers; otherwise the cover is an explicit falsifier.

Blocking gap: No candidate generator is known for which min_Pi sum_B C_{R_B}(OR-SAT_B) can be proved at N^{1+epsilon-o(1)} in general circuits.

## Falsifiers

- semantic block-cover collapse: some partition Pi has C(G_N)+sum_B C_{R_B}(OR-SAT_B)<N^{1+epsilon-delta}
- range-compression falsifier: block OR-SAT values factor through short features A_B with total cost below the claimed threshold
- nonuniform block advice leakage: Q_B encodes the satisfiability pattern on the realized range and bypasses the intended SAT hardness
- generator output-size tax: producing all query bits already forces rho or q to violate max{rho,q}<1+epsilon
- lookup boundary failure: d<=1 with constants allowing truth-table lookup below N^{1+epsilon}
- natural-proof obstruction: a large constructive method proving the source lower bound for many generated carriers would distinguish pseudorandom functions, so a valid proof must be range-specific or non-natural

## Learning

Cycle 21 replaces the previous block-cover warning by an exact shared-generator semantic-cover lemma. The valid target bridge is unchanged, but the source lower bound must beat C(G_N)+min_Pi sum_B C_{R_B}(OR-SAT_B). This creates a concrete falsifier: any subthreshold semantic block partition kills the generated-OR carrier before it can contribute to SAT notin P/poly.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The abstract bridge is now calibrated; the missing issue is whether block semantic covers are generically subthreshold for plausible generated-OR carriers. A concrete block-size sweep can expose a threshold-collapse falsifier before more route lemmas are added.
- Situation seed: Take H_N(x)=OR_{j<=N^q} SAT(G_{N,j}(x)) with L=(log N)^d, d>1, q<1+epsilon, rho<1+epsilon. Group consecutive generated queries into blocks of size b=N^theta and estimate the range-restricted predicate cost U(theta)=C_{R_B}(OR-SAT_B) for typical or designed high-entropy blocks.
- Varied variable: theta, the exponent of the semantic block size b=N^theta.
- Held-fixed controls: The target transfer parameters q,rho,d,epsilon remain in the valid regime max{q,rho}<1+epsilon., The generator is shared once across all blocks; block circuits receive only generated query tuples, not extra SAT advice., The target consequence remains SAT notin P/poly, not a restatement of P versus NP., The carrier is exact worst-case H_N, with no average-case relaxation.
- Expected observation: If N^{q-theta}U(theta)+N^{rho} drops below N^{1+epsilon} for any theta, the source lower bound is falsified. If all theta appear above threshold, the route earns a precise proof obligation: prove a polynomial lower bound on the full semantic block-cover functional.
- Transfer certificate needed: A formal upper or lower bound for U(theta) in nonuniform circuits, plus a composition proof showing that the block circuits and the shared generator yield an exact circuit for H_N without changing the target-preserving parameters.

## Next Experiment

Run the block-size thought experiment for b=N^theta: derive upper bounds on U(theta) from range cardinality, feature compression, and OR compression, then identify whether any theta gives N^{rho}+N^{q-theta}U(theta)<N^{1+epsilon}.

# Barrier-Aware Lower-Bound Route: regular halfspace naturalization gate

## Candidate Lemma

An explicit regular weighted halfspace over the SAT truth table, if it separates SAT_m from SIZE(m^k) at Gaussian-tail threshold, is a valid natural property and therefore not a natural-proof escape.

## Definitions

- source object: an explicit regular weighted halfspace H_N(f)=1[sum_z a_z (-1)^{f(z)} >= tau] over the N=2^m truth-table bits, proposed as a SAT_m separator.
- target object: a Razborov-Rudich natural property useful against SIZE(m^k) truth tables with density at least N^{-A} and poly(N)-time decidability.
- controlled interface: coefficient generator plus threshold plus proof that H_N(SAT_m)=1 and H_N(g)=0 for every g computed by circuits of size m^k.
- target-preserving condition: the same explicit halfspace, with no advice-dependent reweighting, must reject the entire target circuit class and have anti-concentration under the uniform random truth table.
- regularity parameter: sigma^2=sum_z a_z^2 and Delta=max_z |a_z|/sigma.

## Assumptions

- N=2^m, coefficients are rationals of poly(N) bit complexity, and H_N is decidable in poly(N) time from the full truth table.
- Under a uniform random Boolean function F, the signs (-1)^{F(z)} are independent Rademacher variables.
- Let T=tau/sigma. For fixed c and A with A>c^2/2, assume T<=c sqrt(ln N) and Delta <= (2 C_BE)^{-1} N^{-A} for all large N.
- Usefulness is syntactic: every m-input circuit of size m^k has truth table rejected by this same H_N.

## Equations

- normalization: `\sigma^2=\sum_{z\in\{0,1\}^m}a_z^2,\quad \Delta=\max_z |a_z|/\sigma,\quad T=\tau/\sigma`. Valid when: Valid when the source separator is a weighted halfspace with a nonzero coefficient vector and random truth tables are sampled uniformly.
- berry_esseen_tail: `\mu_N(H_N)=\Pr_F\left[\sum_z a_z(-1)^{F(z)}\ge \tau\right]\ge \overline{\Phi}(T)-C_{BE}\Delta`. Valid when: Valid when the coefficient vector is Delta-regular and the full truth table distribution supplies independent Rademacher input bits.
- polynomial_density_threshold: `T\le c\sqrt{\ln N},\ A>c^2/2,\ \Delta\le (2C_{BE})^{-1}N^{-A}\quad\Longrightarrow\quad \mu_N(H_N)\ge \tfrac12 N^{-A}`. Valid when: Applies after the Gaussian tail is polynomially larger than the Berry-Esseen error and N is sufficiently large.
- usefulness_transfer: `\left[H_N(SAT_m)=1\land \forall C\in SIZE(m^k),\ H_N(tt(C))=0\right]\Rightarrow H_N\text{ is useful against }SIZE(m^k)`. Valid when: Requires the target-preserving rejection condition to use exactly the same halfspace and threshold for SAT and every small circuit truth table.

## Attempted Derivation

- Model the proposed lower-bound certificate as H_N(f)=1[sum_z a_z(-1)^{f(z)}>=tau] with coefficients generated in poly(N) time.
- Under a uniformly random truth table F, replace bits by independent signs X_z=(-1)^{F(z)} and normalize L=sum_z a_z X_z by sigma.
- Apply Berry-Esseen: the distribution of L/sigma differs from a standard Gaussian by at most C_BE Delta.
- If tau/sigma<=c sqrt(ln N) and Delta is below the polynomial Gaussian tail, infer density at least N^{-A}/2.
- Poly(N)-time coefficient generation and rational comparison give constructivity of H_N.
- The promised rejection of all SIZE(m^k) truth tables gives usefulness; hence H_N is a natural property and a PRF distinguisher.

Blocking gap: The route must prove a genuine anti-concentration condition, such as Delta <= N^{-A}/polylog(N), for the actual coefficients used by the separator. Without it, dominated halfspaces have exponentially small density.

## Falsifiers

- falsifier: powers-of-two halfspace accepts exactly one truth table while having degree 1 and constant normalized threshold.
- falsifier: a separator whose coefficients depend on hidden advice may be nonconstructive and loses the natural-proof transfer.
- falsifier: if Delta is larger than the Gaussian tail, Berry-Esseen error can swamp the density lower bound.
- falsifier: if the halfspace rejects only a restricted circuit subclass, usefulness against SIZE(m^k) is not target-preserving.
- falsifier: exponentially secure PRFs in SIZE(m^k) rule out any valid constructive large property useful against that same class.

## Learning

The missing parameter for halfspace lower-bound certificates is not threshold degree but anti-concentration of the coefficient vector. Regular halfspaces at polynomial Gaussian tail naturalize with density N^{-A}; irregular dominated halfspaces are a concrete falsifier to degree-only or normalized-threshold-only claims. This is valid route-level barrier progress, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: Cycle 20 left low-degree PTF routes unresolved because degree alone gives neither largeness nor escape. A concrete regularity experiment tests the missing quantitative parameter rather than repeating PTF folklore.
- Situation seed: For each m, imagine an explicit weighted SAT_m truth-table halfspace H_{beta,c} with N=2^m, threshold tau=c sigma sqrt(ln N), coefficient regularity Delta=N^{-beta}, and a claimed proof that it rejects every SIZE(m^k) truth table.
- Varied variable: beta, the exponent controlling halfspace regularity Delta=N^{-beta}.
- Held-fixed controls: N=2^m and the target class SIZE(m^k) are fixed., The threshold ratio c and desired density exponent A>c^2/2 are fixed., Coefficient generation and comparison remain poly(N)-uniform with no hidden advice., The same halfspace must accept SAT_m and reject all target circuit truth tables.
- Expected observation: When beta>A plus the Berry-Esseen slack, the acceptance density is polynomial and the route naturalizes. When beta is small or constant regularity fails, dominated-weight behavior can make density exponentially small, so no valid natural-proof transfer is certified.
- Transfer certificate needed: A formal anti-concentration theorem for the actual coefficient family, plus a uniformity certificate and a same-threshold usefulness proof against SIZE(m^k), is required before the intuition can enter the proof queue.

## Next Experiment

Test whether low-depth AC0 predicates over truth-table bits with bottom fan-in w=O(log N) similarly contain a large accepting restriction, or whether switching-lemma parameters allow an escape without losing constructivity.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Let V be a uniform short-certificate sequential MCSP carrier. On certificate y of length O(m), V emits an N=2^m bit truth table T_y using configurations of size at most 2^{sigma m+o(m)} bits. If tau_V(lambda) is the circuit-size exponent needed to replay 2^{lambda m} consecutive outputs from a stored configuration, then every accepted T_y has circuit complexity at most 2^{alpha_V m+o(m)}, where alpha_V=inf_lambda max{1-lambda+sigma,tau_V(lambda)}. Thus a claimed MCSP no-side threshold 2^{epsilon m} is valid only when epsilon<=alpha_V; epsilon>alpha_V is a route falsifier.

## Definitions

- source object: uniform short-certificate sequential MCSP carrier V={V_m} emitting truth tables T_y of length N=2^m from certificates |y|=O(m).
- target object: an E language L whose length-n slices avoid SIZE(2^{delta n}) for a fixed delta>0 after padding transfer.
- controlled interface: exhaustive E-time canonicalization of accepted certificates plus MCSP no-side soundness C(T_y)>2^{epsilon m} on kappa-dense source lengths.
- target-preserving condition: the verifier is uniform, certificates have O(m) bits, source lengths are kappa-dense below target lengths, and no nonuniform selector, salt-density repair, or low-local decoder is used.
- sigma is the configuration-entropy exponent: a stored configuration has 2^{sigma m+o(m)} bits.
- tau_V(lambda) is the replay exponent for producing a block of 2^{lambda m} outputs from one stored configuration.
- alpha_V is an unconditional nonuniform circuit upper-bound cap for every emitted table in this verifier model.

## Assumptions

- V deterministically emits the truth table in a fixed order and its transition/replay procedure is uniform in m.
- For every accepted certificate y, source soundness asserts general Boolean circuit complexity C(T_y)>2^{epsilon m}.
- A block-start configuration can be hardwired into a circuit and selected by the high-order bits of the input index.
- The replay profile tau_V(lambda) is certified without using nonuniform advice depending on the target input length beyond the hardwired checkpoints.

## Equations

- checkpoint_upper: `C(T_y) \le 2^{(\max\{1-\lambda+\sigma,\tau_V(\lambda)\}+o(1))m}`. Valid when: Valid when V emits the table sequentially from stored configurations and a 2^{lambda m}-output replay circuit can be unrolled uniformly.
- optimized_cap: `\alpha_V=\inf_{0\le \lambda\le 1}\max\{1-\lambda+\sigma,\tau_V(\lambda)\},\quad C(T_y)\le 2^{(\alpha_V+o(1))m}`. Valid when: Applies after the replay profile is fixed independently of the certificate and checkpoint descriptions are hardwired nonuniformly into the test circuit.
- linear_replay_cap: `\tau_V(\lambda)=\lambda \Rightarrow \alpha_V=(1+\sigma)/2`. Valid when: Valid for ordinary one-pass polynomial-space emitters whose next-output simulation costs one step per emitted bit.
- transfer_ceiling: `\delta<\epsilon/\kappa\quad\text{and}\quad \epsilon\le \alpha_V`. Valid when: Requires the target-preserving kappa-density transfer and the checkpoint cap not already refuting the claimed MCSP threshold.

## Attempted Derivation

- Fix an accepted certificate y at length m and let T_y be the emitted table of N=2^m bits.
- Choose a block length B=2^{lambda m}; hardwire V's configuration at the start of each of the N/B blocks.
- The checkpoint advice has size 2^{(1-lambda+sigma)m+o(m)} because there are 2^{(1-lambda)m} blocks and each configuration has 2^{sigma m+o(m)} bits.
- On an m-bit input index i, a circuit selects the checkpoint for i's block and replays at most B outputs, costing 2^{tau_V(lambda)m+o(m)} gates.
- Thus C(T_y) is bounded by 2^{max{1-lambda+sigma,tau_V(lambda)}m+o(m)} for every lambda, and optimizing gives alpha_V.
- For polynomial-space linear replay, lambda=1/2 gives C(T_y)<=2^{m/2+o(m)}, contradicting any asserted MCSP threshold 2^{epsilon m} with epsilon>1/2.

Blocking gap: The derivation only supplies an upper-bound cap. For epsilon<=alpha_V it gives no source soundness, and constructing a sparse non-natural high-MCSP certificate family remains open.

## Falsifiers

- falsifier: a polynomial-space linear-replay certificate source claiming MCSP threshold 2^{epsilon m} with epsilon>1/2 is invalid by checkpoint circuits.
- falsifier: any declared source with alpha_V<epsilon cannot be a sound no-side GapMCSP carrier.
- falsifier: subthreshold indexed restart, short local decoding, or advice-aided random access gives circuits below the claimed threshold.
- falsifier: nonuniform selection of accepted certificates destroys the target E language and yields only a nonuniform consequence.
- falsifier: adding near-N salt to buy density risks largeness; if constructivity is restored, the natural-proofs barrier applies.
- falsifier: an oracle-only or algebraized soundness proof for the carrier does not by itself transfer to an unrelativized E lower bound.

## Learning

Cycle 21 turns anti-restart intuition into a concrete block-checkpoint cap. For polynomial-space linear sequential emitters, alpha_V=1/2, so any MCSP no-side claim above 2^{m/2+o(m)} is an invalid source proposal. The carrier bridge is still valid only in the window epsilon<=alpha_V and delta<epsilon/kappa; this is route-level progress and a falsifier for overstrong carriers, not progress on the main P != NP conjecture itself.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch already has the carrier-to-E bridge; the missing information is the quantitative feasibility window for short sequential MCSP certificate sources. A concrete cap probe tests whether proposed sources collapse before soundness is attempted.
- Situation seed: Define a family V_sigma of uniform O(m)-certificate MCSP carriers. On input certificate y, V_sigma sequentially emits an N=2^m truth table using 2^{sigma m} bits of working configuration, no salt, no local decoder, and claimed no-side threshold 2^{epsilon m} on kappa-dense lengths.
- Varied variable: configuration exponent sigma, with replay profile fixed to tau_V(lambda)=lambda unless explicitly certified otherwise
- Held-fixed controls: certificate length O(m) so exhaustive canonicalization remains in E, kappa-density of source lengths for the padding transfer, soundness required for every accepted certificate, not just a chosen witness, no nonuniform selector, no random-access generator, and no density-amplifying salt
- Expected observation: The optimized checkpoint cap is alpha_V=(1+sigma)/2. For sigma=0, every accepted table has circuits 2^{m/2+o(m)}, so epsilon>1/2 is invalid. Raising sigma enlarges the permissible epsilon but also makes the verifier profile a required part of the source certificate.
- Transfer certificate needed: Before intuition affects proof obligations, provide a formal tau_V replay bound, an E-time canonical search bound, and a non-natural nonuniform-free proof that all accepted tables exceed 2^{epsilon m} with epsilon<=alpha_V.

## Next Experiment

Instantiate the cap audit on proof-complexity-style MCSP certificates: compute sigma and tau_V for transcript-checking emitters, then test whether any epsilon>0 survives without enumeration, local decoding, or nonuniform certificate selection.
