# cycle-0023

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-magnification bridge realization: generated-OR range-balance gate

## Candidate Lemma

Range-label balance is a necessary source condition for the generated-OR carrier. For H_N(x)=OR_{j<=M} SAT(G_{N,j}(x)), M=N^{q+o(1)}, L=(log N)^d, and an all-query generator of size N^{rho+o(1)}, if U_N is the generated formula range and U_N^+,U_N^- are its satisfiable and unsatisfiable parts, then H_N has circuits of size N^{rho+o(1)}+N^{q+o(1)} min{|U_N^+|,|U_N^-|}. Hence a valid N^{1+epsilon} source lower bound with rho<1+epsilon forces min{|U_N^+|,|U_N^-|}>N^{1+epsilon-q-o(1)}.

## Definitions

- source object: the explicit Boolean function family H_N on N input bits defined by a generated OR of SAT queries, H_N(x)=OR_{j<=N^{q+o(1)}} SAT(G_{N,j}(x)).
- target object: SAT on L=(log N)^d bit encodings, with the target consequence SAT notin P/poly if the bridge preserves every polynomial SAT exponent.
- controlled interface: a nonblackbox compact all-query generator G_N of circuit size N^{rho+o(1)} producing M=N^{q+o(1)} SAT instances of length L, with every generation and membership-test cost charged to H_N.
- target-preserving condition: max{q,rho}<1+epsilon, L=(log N)^d with d>1 or otherwise lookup-safe, and no nonuniform advice about SAT beyond either a hypothesized target circuit or an explicitly charged promise/range solver.

## Assumptions

- Source lower-bound model is unrestricted nonuniform Boolean circuit size for H_N, not a restricted Gamma model.
- U_N={G_{N,j}(x): x in {0,1}^N, j<=M}; U_N^+={y in U_N: SAT(y)=1}; U_N^-=U_N\U_N^+.
- The generator outputs all M queries with total circuit size N^{rho+o(1)}; if only per-query generation is available, the rho term must be replaced by the charged total generation cost.
- The route claims only a bridge: proving the source lower bound is a separate non-natural lower-bound obligation.

## Equations

- carrier_definition: `H_N(x)=\bigvee_{j=1}^{M} SAT(G_{N,j}(x)),\qquad M=N^{q+o(1)},\quad L=(\log N)^d.`. Valid when: Valid when the generated queries are fixed nonuniformly for length N and their encoding length is polylogarithmic in the carrier input length.
- range_balance_upper_bound: `C(H_N)\le C(G_N)+O\!\left(M L\min\{|U_N^+|,|U_N^-|\}\right)+O(M).`. Valid when: Valid when membership in the smaller labeled generated range is implemented by equality-DNF circuits and all generator cost is charged once.
- necessary_balance_threshold: `C(H_N)>N^{1+\epsilon}\ \wedge\ C(G_N)\le N^{\rho+o(1)}\ \wedge\ \rho<1+\epsilon\Rightarrow \min\{|U_N^+|,|U_N^-|\}>N^{1+\epsilon-q-o(1)}.`. Valid when: Applies after the range-balance upper bound is compared with the claimed barely-superlinear source lower-bound threshold.
- target_substitution_bound: `SAT\in SIZE(n^c)\Rightarrow C(H_N)\le N^{\rho+o(1)}+N^{q+o(1)}L^c=N^{\max\{\rho,q\}+o(1)}.`. Valid when: Requires the target-preserving transfer where each generated SAT query is answered by the same nonuniform SAT circuit without extra advice leakage.

## Attempted Derivation

- Fix N and let K^+=|U_N^+|, K^-=|U_N^-|.
- If K^+<=K^-, build a membership circuit Pos_N(y)=OR_{z in U_N^+}[y=z] of size O(K^+ L). Then H_N(x)=OR_j Pos_N(G_{N,j}(x)) on every x.
- If K^-<K^+, build Neg_N(y)=OR_{z in U_N^-}[y=z] of size O(K^- L). Then H_N(x)=NOT AND_j Neg_N(G_{N,j}(x)), since every generated query lies in U_N.
- Composing either membership circuit with the charged all-query generator gives C(H_N)<=C(G_N)+O(M L min{K^+,K^-})+O(M).
- With M=N^{q+o(1)}, L=N^{o(1)}, and C(G_N)<=N^{rho+o(1)}, any claimed C(H_N)>N^{1+epsilon} lower bound with rho<1+epsilon forces min{K^+,K^-}>N^{1+epsilon-q-o(1)}.
- The target substitution calculation is unchanged: if SAT has size n^c circuits, composing those circuits with G_N gives C(H_N)<=N^{max{rho,q}+o(1)}, contradicting the source lower bound when max{rho,q}<1+epsilon.

Blocking gap: No explicit generator is known whose H_N beats unrestricted N^{1+epsilon} circuits while also defeating range-label imbalance, promise solvers on U_N, and semantic block-cover compression.

## Falsifiers

- range-label imbalance falsifier: either |U_N^+| or |U_N^-| is at most N^{1+epsilon-q-o(1)}, yielding a valid subthreshold circuit for H_N.
- promise-solver falsifier: SAT restricted to U_N has nonuniform circuits of size at most N^{1+epsilon-q-o(1)}.
- semantic block-cover falsifier: a partition of query positions has total charged OR-SAT block complexity below N^{1+epsilon-o(1)}.
- threshold-collapse falsifier: q>=1+epsilon or rho>=1+epsilon destroys the barely-superlinear magnification window.
- nonuniform leakage falsifier: uncharged advice encoding SAT labels on the generated range makes the source lower bound ill-posed.

## Learning

Cycle 23 adds an exact range-label balance gate. Even with q,rho in the valid target window, a generated-OR carrier is source-plausible only if both satisfiable and unsatisfiable parts of its actual generated range exceed N^{1+epsilon-q-o(1)}. This is a concrete falsifier derived from equality-DNF membership circuits, independent of vague barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for candidate generated-OR carriers.`
- Rationale: The branch needs a concrete way to reject generators whose target transfer looks valid but whose actual generated SAT range is label-compressible by nonuniform circuits.
- Situation seed: Take a length-N carrier with M=N^q query positions, L=(log N)^d, and let G_N enumerate formulas from a designed polylog-length template family while varying the fraction and count of satisfiable templates in the generated range.
- Varied variable: The balanced label support exponent theta defined by min{|U_N^+|,|U_N^-|}=N^{theta+o(1)}.
- Held-fixed controls: Keep q,rho<1+epsilon so the target substitution bridge remains valid., Keep L=(log N)^d with d>1 so full truth-table lookup is not a subthreshold explanation., Charge the all-query generator size C(G_N)<=N^{rho+o(1)}., Use unrestricted nonuniform circuits as the source lower-bound model.
- Expected observation: When theta<=1+epsilon-q, the equality-DNF membership construction computes H_N below N^{1+epsilon}; only theta>1+epsilon-q leaves the source lower-bound claim unfalsified by this audit.
- Transfer certificate needed: A formal proof that the chosen generator has balanced satisfiable and unsatisfiable generated support above the threshold and also lacks smaller promise-solver or semantic block-cover circuits before any intuition can enter the proof queue.

## Next Experiment

Instantiate a template generator for polylog-length 3CNFs and estimate theta=min label-support exponent; then compare it with 1+epsilon-q and with the best promise-SAT solver size on the generated template range.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Hypercontractive naturalization gate: an explicit low-degree real polynomial that separates SAT_m from SIZE(m^k) by L2-normalized absolute deviation is a valid natural-proof object at degree O(log N).

## Definitions

- source object: a poly(N)-evaluable real multilinear polynomial p on the N=2^m truth-table bits of SAT_m, with degree d, mean 0, L2 norm sigma, and claimed absolute separation.
- target object: the Razborov-Rudich natural property R_p={y in {-1,1}^N: |p(y)| >= theta} useful against SIZE(m^k).
- controlled interface: the hypercontractive L4/L2 tail lower bound converts normalized absolute deviation into largeness while preserving the same truth-table coordinates.
- target-preserving condition: p has a uniform poly(N)-time evaluator, theta <= sigma/2, SAT_m is accepted, and every size m^k circuit truth table has |p| < theta.
- largeness parameter: density at least (9/16)9^{-d}, hence polynomial when d=O(log N).
- barrier type: natural-proof barrier applies if pseudorandom functions exist in the target circuit size range.

## Assumptions

- Truth tables are encoded as {-1,1}^N and N=2^m.
- p has zero uniform mean and nonzero variance sigma^2=E[p(Y)^2].
- The coefficient description or evaluator of p is uniform and runs in poly(N), with no SAT truth-table advice.
- Usefulness is absolute: all SIZE(m^k) truth tables have |p| below theta while SAT_m has |p| at least theta.

## Equations

- hypercontractive_moment: `\|p\|_4\le 3^{d/2}\|p\|_2`. Valid when: Valid when p is a degree-d multilinear polynomial on independent uniform Boolean truth-table bits.
- paley_zygmund_density: `\Pr_{Y\leftarrow\{\pm1\}^N}[|p(Y)|\ge \sigma/2]\ge \frac{9}{16}9^{-d}`. Valid when: Applies after theta is at most sigma over two and p has zero mean with variance sigma squared.
- polynomial_largeness_threshold: `d\le (a\log N-O(1))/\log 9\ \Rightarrow\ \mu(R_p)\ge N^{-a}`. Valid when: Requires the degree bound to be logarithmic in the truth-table length and the evaluator to be polynomial time.
- usefulness_clause: `\forall C\in \mathrm{SIZE}(m^k),\ |p(T_C)|<\theta\le |p(T_{SAT_m})|`. Valid when: Applies only when the same polynomial and threshold are used for SAT_m and every target small circuit.

## Attempted Derivation

- Type the proposed proof object as p:{-1,1}^N -> R with degree d, mean zero, variance sigma^2, and uniform poly(N) evaluation.
- Let Y be a uniform random truth table and set Z=p(Y)^2.
- By Boolean hypercontractivity, E[p(Y)^4] <= 9^d sigma^4.
- Apply Paley-Zygmund to Z with lambda=1/4 to obtain Pr[|p(Y)|>=sigma/2] >= (9/16)9^{-d}.
- If theta<=sigma/2, then R_p={|p|>=theta} has at least this density.
- The assumed separation makes R_p accept SAT_m and reject every SIZE(m^k) truth table, so it is useful against the target class.
- When d=O(log N), the density is N^{-O(1)}; with poly(N) constructivity this is a natural property and a PRF falsifier in the usual full-truth-table sense.

Blocking gap: The argument does not naturalize one-sided signed high-threshold PTFs, nor any degree omega(log N) object whose density bound becomes superpolynomially small.

## Falsifiers

- Degree-1 high-threshold predicate p(y)=sum_i y_i with theta=N has density 2^{-N}; this falsifier blocks degree-only naturalization.
- A polynomial p whose coefficient table encodes SAT_m as nonuniform advice loses constructivity and is not a valid natural property.
- If d=omega(log N), the hypercontractive density (9/16)9^{-d} may be below every inverse polynomial, so the natural-proof transfer collapses.
- If some SIZE(m^k) circuit truth table has |p|>=theta, usefulness fails before any barrier discussion.
- Assuming SIZE(m^k) pseudorandom functions, any poly(N)-constructive N^{-a}-large useful R_p is a cryptographic falsifier for the route.

## Learning

Cycle 23 isolates a valid quantitative gate: L2-normalized absolute real polynomial separators of degree O(log N) are natural properties by hypercontractivity and Paley-Zygmund. The escape is not low degree itself, but high threshold, superlogarithmic degree, nonconstructivity, or failed usefulness.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a quantitative transfer test for low-degree polynomial proof objects, because degree, communication, and anti-concentration have repeatedly been insufficient without a density certificate.
- Situation seed: For each m, audit a hypothetical uniform arithmetized Cook-Levin-derived polynomial p_{m,d} on the N=2^m SAT_m truth-table bits, and form R_{m,d}={y: |p_{m,d}(y)| >= sigma_{m,d}/2}.
- Varied variable: degree slope beta in d=beta log_9 N, with the normalized threshold fixed at theta=sigma/2.
- Held-fixed controls: N=2^m truth-table model for SAT_m., Target class SIZE(m^k) and the same k across all beta., Uniform poly(N)-time evaluation of p_{m,d}., Absolute usefulness against every size m^k circuit truth table., No nonuniform coefficient advice depending on the SAT truth table.
- Expected observation: For constant beta, the induced density is at least N^{-beta}/O(1), so the object is natural and PRF-sensitive; only beta growing with N can evade this specific largeness transfer.
- Transfer certificate needed: Before intuition affects proof obligations, one must prove mean-zero normalization, compute or lower-bound sigma, preserve the SAT-versus-SIZE(m^k) threshold, and certify uniform coefficient generation without advice leakage.

## Next Experiment

Audit one-sided signed low-degree PTF separators for certified polynomial positive-tail mass; absent that certificate, quarantine them as threshold-ratio evasions rather than barrier escapes.

# MCSP carrier transfer with selector-soundness audit

## Candidate Lemma

A short MCSP carrier transfers to an E circuit lower bound only through universal no-side soundness or through a uniform selector whose chosen accepted table is hard on every source length. Existential hard witnesses inside a contaminated accepted set are not a target-preserving source condition.

## Definitions

- source object: A deterministic verifier-emitter V_m taking O(m)-bit certificates c, running in 2^{O(m)} time, and either rejecting or emitting a truth table T_{m,c} in {0,1}^{2^m}.
- target object: A language L in E with C_n(L_n)>2^{delta n} for all large n, obtained by padding selected m-bit truth tables to nearby input lengths.
- controlled interface: A uniform E-time selector S which, on input 1^m, returns an accepted certificate c_m, with C(T_{m,c_m})>2^{epsilon m}; universal soundness is the special case where every accepted certificate has this property.
- target-preserving condition: The source lengths are kappa-dense, the selector is uniform and advice-free, epsilon is below the verifier checkpoint cap alpha_V, and padding preserves the lower-bound exponent delta<epsilon/kappa.

## Assumptions

- There is an infinite cofinal set M of source lengths such that for every large n there is m in M with m<=n<=kappa m.
- For each m in M, S(1^m) outputs c_m accepted by V_m within 2^{O(m)} time.
- The selected table T_m=T_{m,c_m} has Boolean circuit complexity greater than 2^{epsilon m}.
- The selector and verifier do not use nonuniform advice depending on the target length.
- The verifier profile satisfies epsilon<=alpha_V, where alpha_V is the best known block-checkpoint upper-bound cap for emitted tables.

## Equations

- density_window: `m(n)\le n\le \kappa m(n)`. Valid when: Valid when source lengths form a named kappa-dense sequence covering all sufficiently large target lengths.
- source_threshold: `C_m(T_m)>s_m=2^{\epsilon m}`. Valid when: Valid when the selected accepted certificate is sound for MCSP no-side threshold 2^{epsilon m}.
- padding_transfer: `C_n(L_n)>2^{\delta n}\quad\text{for every }\delta<\epsilon/\kappa`. Valid when: Applies after prefix padding preserves circuits from target length n back to source length m.
- canonicalization_budget: `|c_m|=O(m),\quad \operatorname{time}(V_m,S)=2^{O(m)}`. Valid when: Requires short certificates and uniform exhaustive or direct selection within the E-time construction budget.

## Attempted Derivation

- Fix a kappa-dense source length set M and a uniform selector S that outputs an accepted certificate c_m for each m in M.
- Let T_m be the emitted m-bit truth table selected by S, and assume C(T_m)>2^{epsilon m}.
- For each target length n choose the largest or canonical m in M with m<=n<=kappa m.
- Define L_n(x_1,...,x_n)=T_m(x_1,...,x_m), ignoring the remaining n-m bits.
- Uniformity: compute m, run S and V to obtain or stream T_m, then answer the indexed bit in 2^{O(n)} time because m<=n.
- Lower bound: a circuit for L_n of size 2^{delta n} yields, by fixing ignored variables, a circuit for T_m of comparable size. For delta<epsilon/kappa this contradicts C(T_m)>2^{epsilon m} for large n.
- Tried to weaken SelectorHard to ExistsHard, but V^+ with an early all-zero certificate preserves ExistsHard and makes canonical selection easy, so the weakening is invalid.

Blocking gap: No construction is known for a short, cap-aware, advice-free verifier whose accepted set is universally hard or whose uniform selector is proved to choose only hard accepted tables.

## Falsifiers

- easy-contamination falsifier: adding one accepted all-zero certificate preserves existential hardness while invalidating canonical extraction
- selector advice leakage: a nonuniform selector can hide the hard witness and yields only a nonuniform consequence
- MCSP postfilter falsifier: brute-force filtering at threshold 2^{epsilon m} exceeds the E construction budget
- checkpoint-cap falsifier: any claimed threshold epsilon>alpha_V is contradicted by the verifier block-simulation upper bound
- density-collapse falsifier: if source lengths are not kappa-dense for constant kappa, the all-length exponent delta becomes zero
- naturalness falsifier: making the accepted set dense and constructively recognizable risks a large useful property against standard circuit classes

## Learning

Cycle 23 proves the exact selector quantifier needed by the MCSP carrier route. The valid transfer is not from existence of a hard accepted certificate, but from universal hardness of accepted certificates or from a uniform selector certified to choose a hard one. Easy contamination is a concrete falsifier for weaker source claims, and brute-force MCSP postfiltering cannot repair it within E.

## Gedanken Experiment Design Seed

- Need decision: `design now as a falsifier probe`
- Rationale: The branch now hinges on whether existential MCSP certificates can be converted into a target-preserving selector. A concrete contamination experiment tests that bridge instead of restating hardness magnification folklore.
- Situation seed: For each source length m, start with an imagined verifier V_m having one hard sequential certificate h_m for a table of complexity above 2^{epsilon m}; form V^+_m by also accepting a distinguished certificate z_m that emits the all-zero table.
- Varied variable: contamination_rank r, the position of z_m in the canonical certificate order or in the selector's search priority
- Held-fixed controls: certificate length remains O(m), verification and emission time remain 2^{O(m)}, source lengths remain kappa-dense, threshold epsilon stays below the declared cap alpha_V, no nonuniform advice is given to the selector
- Expected observation: When r is before the hard witness, lexicographic or exhaustive canonicalization outputs the zero table and the transfer gives no lower bound, even though an existential hard accepted table remains present. Only universal soundness or a separately proved hard-selector invariant survives.
- Transfer certificate needed: A formal proof that the chosen uniform selector always returns a table with C(T)>2^{epsilon m}, or a universal soundness theorem for every accepted certificate; without this certificate the intuition is not valid for the proof queue.

## Next Experiment

Test candidate sequential proof systems for universal no-side soundness under the V^+ contamination operation and compute their alpha_V cap profiles.
