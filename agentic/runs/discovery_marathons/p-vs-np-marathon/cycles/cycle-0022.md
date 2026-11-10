# cycle-0022

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the generated-OR carrier, the target bridge is valid but any subthreshold range-restricted SAT solver is a route-killing falsifier. Let L=(log N)^d, M=N^q, and let G_N of size at most N^rho output M SAT instances of length L. If C(H_N)>N^{1+epsilon} and max{rho,q}<1+epsilon, then SAT is not in P/poly. Conversely, if SAT on the union range U_N={G_{N,j}(x):x in {0,1}^N,j<=M} has a nonuniform circuit of size T_N with q+tau<1+epsilon for T_N=N^{tau+o(1)}, then the proposed source lower bound is false.

## Definitions

- source object: the Boolean carrier H_N on N seed bits defined by H_N(x)=OR_{j<=N^q} SAT(G_{N,j}(x)), measured against general nonuniform circuits.
- target object: SAT on length L=(log N)^d instances and the route-level consequence SAT notin P/poly, hence NP not subset P/poly by completeness, not a direct P != NP proof.
- controlled interface: a compact generator G_N of circuit size N^rho produces M=N^q queries and the consumer is only the OR of their SAT values.
- target-preserving condition: max{rho,q}<1+epsilon and substitution copies a fixed length-L SAT circuit without advice depending on the seed x or on the individual query position.

## Assumptions

- d>1 is the intended lookup-safe polylogarithmic regime, though the target-transfer inequality only needs L=N^{o(1)}.
- The source lower bound is C(H_N)>N^{1+epsilon} for infinitely many or all large valid N in general circuit size.
- The target upper-bound hypothesis is SAT in SIZE(n^c) for an arbitrary fixed c.
- Restricted solvers for U_N are allowed nonuniform advice depending on N; this is exactly the nonuniform leakage that the source lower bound must defeat.

## Equations

- carrier_definition: `H_N(x)=\bigvee_{j=1}^{M} \mathrm{SAT}(G_{N,j}(x)),\quad M=N^q,\quad L=(\log N)^d`. Valid when: Valid when G_N is a fixed nonuniform generator family and x ranges over N-bit seeds.
- target_substitution_transfer: `\mathrm{SAT}\in \mathrm{SIZE}(n^c)\Rightarrow C(H_N)\le N^\rho+N^q(\log N)^{dc}+O(N^qL) = N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies when each generated query has length L and the SAT circuit is copied for every query position.
- restricted_solver_falsifier_bound: `C_{U_N}(\mathrm{SAT})\le T_N\Rightarrow C(H_N)\le N^\rho+N^qT_N+O(N^qL)`. Valid when: Valid when one length-L circuit decides SAT correctly on the generated union range U_N.
- necessary_range_hardness: `C(H_N)>N^{1+\epsilon}\ \wedge\ \rho<1+\epsilon\Rightarrow C_{U_N}(\mathrm{SAT})>N^{1+\epsilon-q-o(1)}`. Valid when: Requires the generated-OR lower bound and the copied restricted solver upper bound to be compared at the same N.

## Attempted Derivation

- Fix c and assume SAT has length-n circuits of size n^c.
- For each N, copy the length-L SAT circuit into each of the M=N^q query positions produced by G_N.
- The resulting circuit for H_N has size N^rho+N^q(log N)^{dc}+O(N^qL)=N^{max{rho,q}+o(1)}.
- If max{rho,q}<1+epsilon, a valid lower bound C(H_N)>N^{1+epsilon} contradicts the assumed SAT circuits, giving the route-level target consequence SAT notin P/poly.
- Now audit the source claim: if SAT restricted to U_N has promise circuits of size T_N, the same substitution gives C(H_N)<=N^rho+N^qT_N+O(N^qL).
- Therefore any source lower bound must also prove C_{U_N}(SAT)>N^{1+epsilon-q-o(1)} and must beat all semantic block covers.

Blocking gap: No current argument proves the required promise-SAT or block-cover lower bound for an explicit high-entropy generated range U_N; entropy and query length do not imply semantic circuit hardness.

## Falsifiers

- falsifier: q>=1+epsilon or rho>=1+epsilon collapses the target threshold before SAT hardness transfers.
- falsifier: a promise solver for SAT on U_N of size at most N^{1+epsilon-q-o(1)} gives a direct small circuit for H_N.
- falsifier: a semantic block partition with total cost below N^{1+epsilon-o(1)} kills the generated-OR lower bound.
- falsifier: a generator whose formulas lie in a syntactically rich but semantically easy SAT family defeats entropy-only lower-bound arguments.
- falsifier: advice depending on N but not on x is allowed in P/poly and must be charged in every valid source-model audit.

## Learning

Cycle 22 isolates the next exact gate: the generated-OR bridge is valid only if the source lower bound defeats nonuniform promise solvers on the actual SAT range. The new quantitative obstruction is T_N>N^{1+epsilon-q-o(1)} for SAT restricted to U_N, plus the earlier semantic block-cover threshold. This is route-level progress, not a proof of P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the generated-OR carrier.`
- Rationale: The route already has a valid target transfer; the missing issue is whether the source lower bound survives nonuniform promise solvers on the generated range.
- Situation seed: Let G_N output M=N^q length-(log N)^d CNF encodings from a high-entropy planted family U_N whose satisfiability is determined by a hidden summary h_N(phi) of size N^tau, and define H_N as the OR of their SAT values.
- Varied variable: Vary tau, the exponent of the smallest nonuniform circuit deciding SAT on U_N, while keeping q,rho,d,epsilon fixed.
- Held-fixed controls: q<1+epsilon and rho<1+epsilon so the SAT-to-H_N target bridge remains valid., d>1 so exhaustive truth-table lookup for all length-L instances is not a subthreshold explanation., The source model remains unrestricted nonuniform circuit size on N-bit inputs., G_N is fixed independently of any assumed global SAT circuit.
- Expected observation: The carrier has size at most N^{max{rho,q+tau}+o(1)}; a lower bound N^{1+epsilon} can only be plausible when q+tau>=1+epsilon and all block-cover variants also exceed the threshold.
- Transfer certificate needed: Before the intuition may affect proof obligations, one must prove a promise-SAT lower bound C_{U_N}(SAT)>N^{1+epsilon-q-o(1)} or the stronger semantic block-cover lower bound in the same nonuniform circuit model.

## Next Experiment

Instantiate G_N with a high-entropy family of polylog-size 3-CNF formulas and compute the best promise solver or block-cover upper bound; vary tau to locate the first threshold-respecting candidate.

# Barrier-Aware Lower-Bound Route: communication-rectangle min-entropy gate

## Candidate Lemma

A deterministic two-party communication separator for SAT truth tables naturalizes only after certifying polynomial density of the accepting rectangle containing SAT. Communication cost c=O(log N) alone is not a valid largeness certificate.

## Definitions

- source object: a deterministic two-party communication protocol Pi_m for a truth-table property Q_m subset {0,1}^N, N=2^m, under the fixed split x=(x_L,x_R) with |x_L|=|x_R|=N/2.
- target object: a Razborov-Rudich natural property P_m subset {0,1}^N useful against SIZE(m^k), decidable in poly(N), and dense at least N^{-a}.
- controlled interface: choose the accepting transcript rectangle R_tau=A_tau x B_tau that contains the SAT_m truth table and test membership in R_tau.
- target-preserving condition: Pi_m rejects every SIZE(m^k) truth table, R_tau has density at least N^{-a}, and the description of R_tau is computable from m in poly(N) without circuit-dependent advice.

## Assumptions

- The protocol is deterministic; randomized protocols require a separate seed and soundness audit.
- Local computation by the parties is free in the communication model, but the extracted property must be poly(N)-constructive.
- Usefulness is universal over all m-input circuits of size m^k, not merely over sampled circuits.
- The split of the N truth-table coordinates is fixed uniformly from m.

## Equations

- truth_table_length: `N=2^m`. Valid when: Valid when the source object is a Boolean truth-table property on m-bit inputs.
- rectangle_density: `R_{\tau}=A_{\tau}\times B_{\tau},\qquad \Pr_{X\leftarrow\{0,1\}^N}[X\in R_{\tau}]=\frac{|A_{\tau}||B_{\tau}|}{2^N}=2^{-\rho_{\tau}}`. Valid when: Valid when the fixed two-party split partitions the N truth-table bits into two blocks.
- largeness_threshold: `\rho_{\tau}\le a\log_2 N\quad\Longrightarrow\quad \mu(R_{\tau})\ge N^{-a}`. Valid when: Applies when the accepting SAT transcript has certified min-entropy loss at most logarithmic in N.
- usefulness_transfer: `P_m:=R_{\tau},\qquad P_m(T_{SAT_m})=1\ \wedge\ \forall C\in SIZE(m^k),\ P_m(T_C)=0`. Valid when: Requires the protocol soundness to reject every small-circuit truth table, not just most such tables.

## Attempted Derivation

- Start with a deterministic c-bit protocol Pi_m accepting T_SAT and rejecting all SIZE(m^k) truth tables.
- The transcript partition has at most 2^c rectangles, so the average rectangle under the uniform input distribution has total mass about 2^{-c}.
- Try to infer that the particular accepting rectangle containing T_SAT has mass at least 2^{-c}.
- This inference is false: a partition may contain one singleton accepting rectangle and a few large rejecting rectangles.
- Therefore the valid extraction is P_m=R_tau only when rho_tau=-log_2 mu(R_tau)=O(log N) is separately certified.

Blocking gap: Communication complexity bounds the number of rectangles, not the density of the distinguished SAT-containing rectangle.

## Falsifiers

- Singleton equality protocol: constant communication, accepting density 2^{-N}, no natural largeness.
- A protocol that isolates SAT_m by hardwired truth-table advice would be nonuniform leakage, not a valid target-preserving proof object.
- A balancedness claim based only on at most 2^c transcripts is invalid for a distinguished input.
- If rho_tau=omega(log N), the natural-proof bridge loses density even when communication remains O(1).

## Learning

Cycle 22 separates communication cost from natural-proof largeness. Deterministic low-communication SAT separators naturalize only with a polynomial-density SAT-containing rectangle. Singleton rectangles are a concrete falsifier to the tempting bridge from cc=O(log N) to density. This is valid route-level barrier progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and threshold calibration.`
- Rationale: Low-communication truth-table separators look like a possible escape from prior local-query naturalization, but the actual transfer parameter is rectangle min-entropy, not communication cost.
- Situation seed: For the SAT_m truth table T=(T_L,T_R), consider rectangle tests R_rho=A_rho x B_rho containing T, where A_rho and B_rho are fixed cylinders around T_L and T_R of total density 2^{-rho}; Alice and Bob each test local membership and exchange one bit.
- Varied variable: rho=-log_2 mu(R_rho), the min-entropy loss of the accepting rectangle, varied from O(log N) to Theta(N).
- Held-fixed controls: The truth-table length remains N=2^m and the target class remains SIZE(m^k)., The protocol family is required to be poly(N)-uniform and not use circuit-dependent advice., Soundness, when hypothesized, is universal rejection of every small-circuit truth table., The extracted property is the actual accepting rectangle containing SAT_m, not an average rectangle.
- Expected observation: For rho<=a log N the rectangle is a valid natural property if soundness holds; for rho>>log N the same O(1)-communication interface becomes non-large and the naturalization transfer collapses.
- Transfer certificate needed: A proof that the route's SAT-containing accepting rectangle has rho=O(log N), or an alternative non-natural and target-preserving lower-bound transfer that does not use largeness.

## Next Experiment

Audit randomized and Merlinized communication separators: determine whether fixing public coins or witnesses yields a rectangle of density at least p_accept·2^{-rho}, and locate the soundness threshold needed before naturalization is valid.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Cap-aware short-certificate MCSP carriers transfer to E lower bounds only under universal soundness or an E-uniform good-certificate selector; existential completeness alone is not target-preserving.

## Definitions

- source object: A kappa-dense length set M and an E-uniform verifier/emitter V(m,z) with |z|<=cm, acceptance A(m,z), emitted truth table Y_{m,z} in {0,1}^{2^m}, emission time 2^{am+o(m)}, and block-checkpoint profile (sigma,tau_V).
- target object: A uniform language L in E whose n-bit slice is a padded selected table from some source length m in M with m<=n<=kappa m, giving circuit lower bound 2^{delta n} on all large target lengths.
- controlled interface: Enumerate O(m)-bit certificates in E; select lexicographically only when every accepted certificate is sound, otherwise use an E-computable selector Sel(m) with no advice, randomness, MCSP oracle, or nonuniform ranking.
- target-preserving condition: M is kappa-dense, selected outputs satisfy MCSP(Y_{m,z})>2^{epsilon m}, epsilon<=alpha_V, and selection plus emission remain uniform E procedures without large-property salt leakage.
- universal soundness: for every accepted z at length m, the emitted table has circuit complexity greater than 2^{epsilon m}.
- selector soundness: Sel(m) returns an accepted z and the emitted table has circuit complexity greater than 2^{epsilon m}, with Sel computable in 2^{O(m)} time uniformly.

## Assumptions

- For every sufficiently large m in M there is at least one accepted certificate.
- Either universal soundness holds, or selector soundness holds for an E-uniform Sel.
- Certificate length is O(m), so exhaustive search over certificates costs 2^{O(m)}.
- The block-checkpoint cap alpha_V has been computed for the same emitter used by the source.
- Padding maps every target length n to a source length m with m<=n<=kappa m.

## Equations

- checkpoint_cap: `\alpha_V=\inf_{0<\lambda<1}\max\{1-\lambda+\sigma,\tau_V(\lambda)\}`. Valid when: Valid when V emits sequentially with checkpoint state exponent sigma and uniform block simulation exponent tau_V(lambda).
- nonvacuous_threshold: `\epsilon\leq \alpha_V+o(1)`. Valid when: Requires the emitter profile to give circuits for every accepted emitted table before claiming MCSP no-side soundness.
- padding_transfer: `\delta<\epsilon/\kappa`. Valid when: Applies after padding a selected m-bit hard table to every target length n satisfying m<=n<=kappa m.
- enumeration_budget: `T_{ext}(n)\leq 2^{(c+a+o(1))m}\leq 2^{O(n)}`. Valid when: Requires O(m)-bit certificates, kappa-dense padding, deterministic acceptance testing, and no advice in certificate selection.
- soundness_quantifier: `\forall z\,(A(m,z)\Rightarrow CC(Y_{m,z})>2^{\epsilon m})\ \lor\ CC(Y_{m,Sel(m)})>2^{\epsilon m}`. Valid when: Valid when the extractor cannot directly decide high MCSP in E time and must trust the source interface.

## Attempted Derivation

- Assume a short MCSP carrier V with kappa-dense source lengths and threshold 2^{epsilon m}.
- Run the E extractor by enumerating O(m)-bit certificates and selecting a canonical accepted certificate.
- If universal soundness holds, every canonical accepted output is high-MCSP, so padding gives circuit lower bound exponent any delta<epsilon/kappa.
- If universal soundness is absent, replace V by a contaminated V' that also accepts a lexicographically first certificate emitting the zero table.
- The contaminated source still has existential high witnesses, the same length balance, and the same emission budget, but canonical extraction gives an easy language.
- An O(m)-bit advice string can name a good certificate, but that changes the target to E/O(m) and triggers the nonuniform leakage falsifier.
- The checkpoint cap remains an independent consistency check: any claimed epsilon above alpha_V is impossible for outputs of V itself.

Blocking gap: Construct a sparse, cap-aware source with universal no-side soundness, or give an E-uniform selector whose correctness is proved without MCSP oracle, advice, randomness, or large salt.

## Falsifiers

- falsifier: carrier has only existential good witnesses and also accepts an easy table.
- falsifier: selector for hard certificates uses O(m) advice, yielding only a nonuniform E/O(m) consequence.
- falsifier: claimed MCSP threshold epsilon exceeds the computed checkpoint cap alpha_V.
- falsifier: certificate length becomes superlinear and exhaustive E canonicalization fails.
- falsifier: near-N salt makes the constructive carrier image large enough for the natural-proofs obstruction.
- falsifier: extraction loses kappa-density, so padding gives no all-length lower-bound exponent.
- falsifier: block random access below 2^{epsilon m-o(m)} yields small circuits for the emitted table.

## Learning

Cycle 22 finds a hidden soundness quantifier. A short MCSP carrier with existential hard witnesses is not enough: the valid bridge to E lower bounds needs every accepted table to be hard, or a uniform selector for a hard accepted table. Otherwise a contaminated easy certificate is a formal falsifier. This is route-level progress, not evidence for P != NP itself.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for source proposals.`
- Rationale: The branch already has a valid quantitative carrier transfer; the unresolved issue is whether a proposed MCSP source supplies the correct soundness quantifier without nonuniform leakage.
- Situation seed: Contaminated padded GapMCSP carrier: at every source length m, certificate 0^{cm} emits the zero truth table, while one hidden O(m)-bit certificate emits a table promised to have MCSP greater than 2^{epsilon m}; padding covers all n with m<=n<=kappa m.
- Varied variable: selector advice leakage b(m), ranging from b=0 uniform selection to b=O(m) naming the hidden hard certificate.
- Held-fixed controls: certificate length O(m) and deterministic 2^{O(m)} emission, kappa-dense source lengths and padding transfer delta<epsilon/kappa, checkpoint cap window epsilon<=alpha_V, with alpha_V=1/2 for polynomial-space linear sequential emitters, no MCSP oracle and no randomized selector
- Expected observation: With b=0, extraction is valid only if universal soundness or an E-uniform selector rejects the zero certificate. With b=O(m), the hard table can be selected but the target becomes nonuniform, so the route fails despite existential high witnesses.
- Transfer certificate needed: A proof that the selected certificate is high-MCSP by a uniform, advice-free, non-large predicate; equivalently, universal soundness for all accepted certificates under the declared cap profile.

## Next Experiment

Audit one concrete proof-complexity or algebraic-transcript carrier by adding the contaminated-zero certificate test; compute whether its acceptance rule proves universal high-MCSP soundness or merely existential completeness.
