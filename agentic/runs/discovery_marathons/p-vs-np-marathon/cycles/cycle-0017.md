# cycle-0017

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: positioned-range entropy audit

## Candidate Lemma

For a compact SAT-query carrier H_N computed by an oracle circuit K_N of size N^rho with t_N<=N^q SAT gates of length L_N=(log N)^d, an N^{1+epsilon} ordinary circuit lower bound magnifies to SAT notin P/poly when max{rho,q}<1+epsilon, but the source lower bound is falsified whenever the positioned effective range entropy e_eff is also below 1+epsilon.

## Definitions

- source object: an explicit length-N Boolean family H_N computed by a compact oracle circuit K_N with at most t_N=N^q SAT gates, each querying a formula of length L_N=(log N)^d over v_N variables.
- target object: nonuniform SAT circuits; the target consequence is SAT notin P/poly, hence NP not subset P/poly, only after the route bridge hypotheses are proven.
- controlled interface: replace each SAT oracle gate of K_N either by a target SAT circuit of size L_N^c or by an unconditional per-position simulation using its image range or variable assignments.
- target-preserving condition: K_N is uniform enough to name H_N, has no advice table encoding SAT answers, and satisfies max{rho,q}<1+epsilon while the source lower bound is against ordinary SIZE(N^{1+epsilon}) circuits.

## Assumptions

- There is a fixed epsilon>0 and an explicit family H_N with H_N notin SIZE(N^{1+epsilon}) for all large valid N.
- The compact oracle circuit K_N has size at most N^rho and at most N^q oracle gates, with rho,q<1+epsilon.
- For every oracle gate g, R_{g,N} is the set of length-L_N formulas that appear at that gate over all H_N inputs.
- The source model is ordinary nonuniform Boolean circuits on N input bits, not a restricted Gamma model unless explicitly restated.

## Equations

- target-substitution-size: `S_{\mathrm{SAT}}(N,c) \le N^{\rho}+t_N L_N^c\,\mathrm{poly}(L_N)=N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when SAT has nonuniform circuits of size n^c and every oracle query length is L_N=(log N)^d.
- positioned-effective-entropy: `e_{\mathrm{eff}}(N)=\log_N\left(\sum_{g\in K_N}\min\{|R_{g,N}|,2^{v_N}\}\right)`. Valid when: Valid when each oracle position has a well-defined image over all N-bit inputs of H_N.
- unconditional-range-upper-bound: `S_{\mathrm{uncond}}(N) \le O(N^{\rho})+\mathrm{poly}(L_N)\sum_g\min\{|R_{g,N}|,2^{v_N}\}=N^{\max\{\rho,e_{\mathrm{eff}}\}+o(1)}`. Valid when: Applies when oracle gates may be replaced by per-position range DNFs or exhaustive assignment checks.
- magnification-implication: `H_N\notin SIZE(N^{1+\epsilon})\ \wedge\ \max\{\rho,q\}<1+\epsilon\ \Longrightarrow\ SAT\notin P/poly`. Valid when: Requires the source lower bound to be valid in the same nonuniform circuit model used by the target substitution.
- source-falsifier-threshold: `\max\{\rho,e_{\mathrm{eff}}\}<1+\epsilon-\delta\ \Longrightarrow\ H_N\in SIZE(N^{1+\epsilon-\delta/2})`. Valid when: Valid when the entropy bound holds eventually and polylogarithmic replacement factors are absorbed by the delta margin.

## Attempted Derivation

- Fix K_N with ordinary gates plus SAT oracle gates g=1,...,t_N, t_N<=N^q, query length L_N=(log N)^d, and overhead size N^rho.
- Assume SAT has circuits C_L of size L^c. Replace every SAT gate by C_{L_N}; the resulting H_N circuit has size N^rho+t_NL_N^c=N^{max{rho,q}+o(1)}.
- Thus an eventual lower bound H_N notin SIZE(N^{1+epsilon}) contradicts SAT in SIZE(n^c) for each fixed c if max{rho,q}<1+epsilon.
- Audit the source claim without assuming SAT circuits. For each oracle position g, replace SAT on the finite image R_{g,N} by a DNF table for satisfiable members of R_{g,N}, costing O(|R_{g,N}|L_N), or by exhaustive assignment enumeration, costing 2^{v_N}poly(L_N).
- Summing over positions gives H_N in size O(N^rho)+poly(L_N) sum_g min{|R_{g,N}|,2^{v_N}}.
- Therefore any proposed source lower bound with max{rho,e_eff}<1+epsilon by a margin is internally inconsistent; high positioned effective entropy becomes a necessary certificate.

Blocking gap: No explicit target-clean carrier is known with q,rho<1+epsilon, e_eff>=1+epsilon-o(1), and a non-natural N^{1+epsilon} lower bound against general circuits.

## Falsifiers

- threshold collapse: max{rho,q}>=1+epsilon makes SAT substitution too large to contradict the source lower bound.
- positioned range entropy falsifier: sum_g min{|R_g|,2^v}<N^{1+epsilon-delta} yields an unconditional subthreshold circuit for H_N.
- low variable entropy: q+v_N/log N<1+epsilon by a margin lets exhaustive assignment simulation kill the source claim.
- nonuniform leakage: K_N may hide SAT answers in advice-like query selection or gate wiring, invalidating target preservation.
- model mismatch: a lower bound only for a restricted circuit class Gamma does not imply NP not subset P/poly without a separate lift.
- natural-proof obstruction: a large constructive property proving the source lower bound against P/poly would collide with standard PRG-based natural proofs barriers.

## Learning

Cycle 17 adds a sharper necessary condition for the generated-OR route: not only q,rho<1+epsilon, but the positioned effective range entropy sum_g min{|R_g|,2^v} must reach the lower-bound threshold. This converts low-range query generation into an explicit falsifier and preserves the valid target transfer only for high-entropy, target-clean carriers.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has a concrete generated-OR carrier; the next mathematical risk is not the target substitution but whether the source lower bound is already refuted by positioned lookup or assignment simulation.
- Situation seed: Consider K_N with M=N^q SAT gates, query length L=(log N)^d, compact overhead N^rho, v=alpha log N variables per formula, and each gate query depending on exactly s log N live input bits so |R_g| about N^s.
- Varied variable: the positioned range exponent s, while q,rho,d,alpha,epsilon are held fixed.
- Held-fixed controls: q<1+epsilon and rho<1+epsilon so target SAT-circuit substitution remains subthreshold., d>1 so full length-L truth-table lookup costs N^{omega(1)} per N^q gates and is not the old falsifier., The carrier is target-clean: no hardwired SAT-answer advice is allowed in K_N., The source lower-bound model is ordinary nonuniform SIZE on N input bits.
- Expected observation: If q+min{s,alpha}<1+epsilon, the carrier has a subthreshold unconditional circuit; if q+min{s,alpha}>1+epsilon while q,rho<1+epsilon, the entropy audit no longer falsifies the route and the lower-bound obligation becomes genuinely nontrivial.
- Transfer certificate needed: A formal certificate that sum_g min{|R_g|,2^v}>=N^{1+epsilon-o(1)}, plus uniform construction of K_N and a proof that the source lower-bound argument is non-natural or outside known natural-proof scope.

## Next Experiment

Instantiate K_N from a specific extractor-like generator of polylog-length CNFs and compute |R_g|, v_N, q, and rho exactly to see whether the positioned entropy threshold can be met without advice leakage.

# Barrier-Aware Lower-Bound Route: adaptive affine-sketch naturalization gate

## Candidate Lemma

Adaptive affine-sketch SAT separators with q=O(log N) queries naturalize. Let L_m be the SAT truth table on m-bit inputs, N=2^m. If a poly(N)-uniform deterministic verifier makes q adaptive affine F2 queries to an oracle truth table f, accepts L_m, and rejects every truth table computed by SIZE(m^k) circuits, then the accepting transcript for L_m defines a poly(N)-constructive property of density at least 2^{-q} containing L_m and useful against SIZE(m^k). Thus global parity queries are not a valid natural-proof escape at logarithmic query complexity.

## Definitions

- source object: poly(N)-uniform deterministic adaptive affine-sketch separator V_m for SAT truth tables f in {0,1}^N, N=2^m, using q(m) parity/affine queries over F2.
- target object: Razborov-Rudich style natural property P_m subset {0,1}^N with poly(N) constructivity, inverse-polynomial largeness when q=O(log N), and usefulness against SIZE(m^k).
- controlled interface: fix the accepting transcript tau of V_m on L_m; freeze the adaptive affine query rows chosen along tau; define P_tau by the resulting affine constraints and accepting leaf.
- target-preserving condition: V_m has exact completeness on L_m, universal soundness against all SIZE(m^k) truth tables, and a uniform row/coefficient generator running in polynomial time in N without hidden advice.

## Assumptions

- Truth tables are indexed over m-bit inputs; N=2^m is the natural-property input length.
- Each query answer is an affine functional <a_i,f>+c_i over F2; adaptivity may depend only on previous answers.
- The separator rejects every small-circuit truth table, not merely most circuits under a distribution.
- The coefficient generator for query vectors is explicit enough that membership in P_tau is decidable from the full truth table in poly(N) time.

## Equations

- parameters: `N=2^m,\quad s=m^k,\quad q=q(m)`. Valid when: Valid when N is the truth-table length for m-bit SAT encodings and s denotes the target circuit-size bound.
- accepting_affine_cell: `\mathcal{P}_\tau=\{f\in\{0,1\}^N:A_\tau f=b_\tau\}`. Valid when: Valid when the accepting SAT transcript fixes every adaptive query vector before the candidate truth table is tested.
- density_bound: `\mu(\mathcal{P}_\tau)=2^{-\operatorname{rank}(A_\tau)}\ge 2^{-q}`. Valid when: Valid when all transcript constraints are affine over F2 and redundant constraints are accounted for by rank.
- constructivity_time: `T_{\mathcal{P}}(N)\le \operatorname{poly}(N)+O(qN\,t_{bit}(N))`. Valid when: Valid when each queried coefficient is uniformly computable in t_bit(N) time and the tester receives the full truth table.
- large_threshold: `q\le a\log_2 N\Rightarrow \mu(\mathcal{P}_\tau)\ge N^{-a}`. Valid when: Valid when q is at most logarithmic in truth-table length and density is measured under the uniform distribution.
- usefulness_transfer: `\mathcal{P}_\tau\cap TT(\mathrm{SIZE}(s))=\varnothing,\quad L_m\in\mathcal{P}_\tau`. Valid when: Valid when soundness is universal over every size-s circuit truth table, not merely distributional or average-case.

## Attempted Derivation

- Fix the accepting transcript tau of the affine verifier on the SAT truth table L_m.
- Along tau, adaptivity disappears: each query vector and affine offset is now a fixed explicit row.
- The set of truth tables producing tau is the solution set of at most q affine equations over F2.
- A rank-r affine subspace has density 2^{-r}; since r<=q, density is at least 2^{-q}.
- Membership is tested by recomputing the q affine forms on the supplied truth table, giving poly(N) constructivity under the row-uniformity assumption.
- Completeness gives L_m in P_tau; universal soundness gives no SIZE(m^k) truth table in P_tau.
- Therefore q<=a log N yields an N^{-a}-large constructive property useful against SIZE(m^k), so the route hits the natural-proof barrier under standard PRF hypotheses.

Blocking gap: No gap for affine sketches under the stated assumptions. The remaining gap is applicability: many proposed lower-bound arguments are not honestly affine-sketch objects or hide nonuniform query descriptions.

## Falsifiers

- A one-query equality predicate Q(f)=1 iff f=SAT_m is a falsifier to any claim that low nonlinear global query complexity alone implies largeness.
- If q=log^2 N, the affine-cell density can be 2^{-log^2 N}=N^{-log N}, below the usual inverse-polynomial natural-proof threshold.
- If query rows require superpolynomial advice to describe, constructivity fails even though the affine density calculation remains formally valid.
- If soundness only holds for random small circuits, usefulness against SIZE(m^k) does not transfer.
- If the certificate queries an encoded witness rather than the truth table itself, the affine-cell argument is not target-preserving without a decoding lemma.

## Learning

Cycle 17 adds a concrete bridge lemma: adaptive affine truth-table sketches naturalize exactly like accepting leaves, with density 2^{-rank}>=2^{-q}. The valid escape threshold is not global linear access but nonlinear cells without largeness, q=omega(log N), nonuniform row advice, or weakened soundness. This is route-level progress only, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for linear-global-query escape claims.`
- Rationale: Recent cycles closed bit-query, short-witness, public-coin, and adaptive-leaf loopholes. The next plausible escape is to replace local bit queries by global parity measurements; this needs a concrete density computation, not another barrier slogan.
- Situation seed: Imagine a claimed SAT lower-bound certificate V_m that uses q=beta log_2 N adaptive parity queries to the full SAT truth table and then rejects every m^k-size circuit truth table.
- Varied variable: beta, the coefficient in q=beta log_2 N parity queries.
- Held-fixed controls: SAT completeness on the exact truth table L_m., Universal soundness against all SIZE(m^k) truth tables., Poly(N)-uniform generation of every parity row along every transcript., No advice beyond the public verifier description.
- Expected observation: The accepting transcript defines an affine subspace of density at least N^{-beta}. For constant beta this is a large constructive natural property, so global linearity gives no barrier escape; only beta growing with N drops below the largeness threshold.
- Transfer certificate needed: A formal extraction of the SAT accepting transcript, a proof that all induced queries are affine and uniformly generable, and a proof that soundness excludes every small-circuit truth table inside the same affine cell.

## Next Experiment

Audit low-degree polynomial query separators over F_p: compute whether degree d and q=O(log N) force any inverse-polynomial largeness, or whether nonlinear low-degree cells already provide a genuine density escape.

# MCSP / Meta-Complexity Carrier Transfer, cycle 17: space-sensitive checkpoint leakage

## Candidate Lemma

Space-sensitive checkpoint leakage lemma: an O(m)-certificate sequential MCSP no-side source whose accepted table is emitted by a deterministic verifier with configuration length S(m) has nonuniform circuits of size O((N/B)S(m)+B poly(m)) for every checkpoint spacing B. Hence a valid source claiming MCSP threshold K(m)=2^{epsilon m} must defeat every indexed checkpoint/replay tradeoff below K(m); in particular polyspace streaming sources cannot support epsilon >= 1/2.

## Definitions

- source object: a uniform deterministic verifier V_m(z) with |z|=O(m) that emits a truth table y in {0,1}^{N}, N=2^m, in time N poly(m) or 2^{O(m)}, and whose sound accepted outputs are intended to satisfy MCSP(y)>K(m).
- target object: an E-uniform language L whose length-m truth tables are the accepted y_m on kappa-dense source lengths, yielding nonuniform circuit lower bounds SIZE(2^{delta n}) for every delta<epsilon/kappa after padding/interpolation.
- controlled interface: the only information passed from the MCSP carrier to the target is a uniformly searchable accepted certificate plus a sound no-side lower bound MCSP(y_m)>2^{epsilon m}; no nonuniform selector or external truth-table advice may enter.
- target-preserving condition: certificate search, output indexing, and length interpolation must run in 2^{O(n)} time, preserve kappa-density, and keep the MCSP threshold exponent epsilon constant enough that delta<epsilon/kappa remains positive.

## Assumptions

- V is deterministic after fixing m and z; randomized certificates require fixing all coins or adding them to z.
- The nonuniform circuit for y_i may hardwire checkpoint configurations, since MCSP measures ordinary nonuniform circuit size of the emitted table.
- Configuration length S(m) includes work tapes, head positions, m, z, and finite control; if V uses exponential space, the checkpoint bound weakens accordingly.
- The bridge consequence is route-level only: it gives an E lower bound if the source exists; it is not a proof of P != NP.

## Equations

- truth_table_and_threshold: `N=2^m,\qquad K(m)=2^{\epsilon m}=N^{\epsilon}.`. Valid when: Valid when the source length m indexes full Boolean truth tables and epsilon is a fixed positive MCSP threshold exponent.
- checkpoint_upper_bound: `\operatorname{SIZE}(y)\le O\big((N/B)S(m)+B\,\operatorname{poly}(m)\big).`. Valid when: Applies when checkpoint configurations every B output steps can be hardwired and replayed deterministically to recover the requested bit.
- optimized_checkpoint_bound: `\operatorname{SIZE}(y)\le 2^{((1+\sigma)/2)m+o(m)}\quad\text{if }S(m)=2^{\sigma m+o(m)}.`. Valid when: Requires the verifier configuration length to have exponential rate sigma and the output time to be near linear in N.
- source_feasibility_constraint: `\epsilon < (1+\sigma)/2\quad\text{is necessary to avoid the generic checkpoint falsifier}.`. Valid when: Valid when the claimed no-side bound is MCSP(y)>2^{epsilon m} and the optimized checkpoint circuit is available nonuniformly.
- carrier_transfer_bound: `\forall\delta<\epsilon/\kappa,\qquad L\notin \operatorname{SIZE}(2^{\delta n})\text{ on all large lengths}.`. Valid when: Applies after the reduction preserves uniform certificate search, kappa-dense source lengths, and constant threshold exponent epsilon.

## Attempted Derivation

- Fix an accepted certificate z and emitted table y of length N=2^m.
- Choose checkpoint spacing B. Hardwire in a Boolean circuit all configurations of V_m(z) immediately before output positions 0,B,2B,... . This costs about (N/B)S(m) bits/gates up to indexing overhead.
- On input i in {0,1}^m, compute q=floor(i/B) and r=i-qB, select the hardwired q-th configuration, and simulate V for r<=B output steps to recover y_i. This costs B poly(m) gates for a fixed universal transition implementation.
- Therefore y has circuits of size O((N/B)S(m)+B poly(m)); optimizing gives O(sqrt(N S(m) poly(m))).
- If S(m)=2^{sigma m+o(m)}, every accepted output has circuits of size 2^{((1+sigma)/2)m+o(m)}. A claimed MCSP no-side threshold 2^{epsilon m} is impossible when epsilon>(1+sigma)/2 plus margin.
- The carrier-to-E extraction remains valid only after choosing epsilon below this universal upper bound and below any stronger indexed replay scheme present in the proposed source.

Blocking gap: This does not construct any high-MCSP source; it only gives a necessary anti-checkpoint condition. A source might use large space sigma or nonlocal global computation, so the lemma is an obstruction, not a completeness theorem.

## Falsifiers

- A polyspace or logspace streaming source claiming MCSP threshold 2^{epsilon m} with epsilon>=1/2 is refuted by the generic checkpoint falsifier.
- Any indexed checkpoint table plus replay algorithm with size A(m)+R(m)poly(m)<2^{epsilon m} invalidates the no-side MCSP claim for its accepted output.
- A source using omega(m)-bit certificates destroys the E exhaustive-search budget unless a separate compression or direct indexing theorem is proved.
- A dense locally decidable accepted-table property re-enters the natural-proofs barrier unless it is shown non-large or nonconstructive in the relevant regime.
- An extraction that selects among accepted certificates using nonuniform advice proves only a nonuniform artifact and is not a valid target-preserving transfer.

## Learning

Cycle 17 adds a quantitative upper-bound obstruction: any sequential certificate verifier with configuration exponent sigma automatically gives its emitted tables circuits of exponent at most (1+sigma)/2 via hardwired checkpoints. Thus a constant MCSP threshold is not merely about anti-random-access; it must also be below the universal checkpoint exponent, or the source is invalid. The carrier-to-E bridge remains valid but only after this space-sensitive threshold audit.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The route now hinges on a quantitative source-side obstruction, not on another abstract MCSP magnification slogan. The checkpoint upper bound gives a concrete threshold to test proposed sequential certificate sources before spending proof effort on soundness.
- Situation seed: Consider a family V_m(z) with |z|=cm that emits N=2^m bits in N poly(m) time and configuration length S(m)=2^{sigma m}. Its accepted outputs are claimed to be GapMCSP no-instances with threshold K=2^{epsilon m}.
- Varied variable: configuration exponent sigma, with checkpoint spacing B optimized as a dependent parameter.
- Held-fixed controls: certificate length O(m) and exhaustive uniform search in E, kappa-dense source lengths and target transfer exponent delta<epsilon/kappa, ordinary nonuniform circuit size as the MCSP target measure, no external truth-table advice or nonuniform certificate selector
- Expected observation: For sigma=0 the generic checkpoint circuit has exponent 1/2, so epsilon>=1/2 collapses. More generally, the minimum safe state exponent to avoid this falsifier is sigma>2epsilon-1 up to lower-order terms.
- Transfer certificate needed: A formal proof that hardwired checkpoints yield ordinary Boolean circuits for the emitted truth table, plus a density-preserving extraction lemma showing that any remaining sound source transfers to E lower bounds without importing nonuniform leakage.

## Next Experiment

Audit a proof-complexity-style transcript source at epsilon<1/2: compute its configuration exponent sigma, its best checkpoint spacing B, and whether its soundness argument is non-enumerative and non-large.
