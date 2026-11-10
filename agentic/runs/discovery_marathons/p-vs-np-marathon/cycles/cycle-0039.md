# cycle-0039

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# High-q generated-OR carrier: partial-certificate cover gate

## Candidate Lemma

For the high-q generated-OR CNF carrier, a small position-indexed cover by satisfying partial assignments gives a subthreshold nonuniform circuit for H_N. Therefore a valid N^{1+epsilon} source lower bound must first prove superthreshold partial-term cover complexity, not merely large realized full-witness entropy.

## Definitions

- source object: H_N(x)=OR_{j<=M} SAT(F_{N,j}(x)) on N-bit x, with M=N^q, F_{N,j} produced by a shared nonuniform generator G_N of size N^{rho+o(1)}, and each query a CNF of length L=(log N)^d.
- target object: CNF-SAT on L-bit formulas, with target consequence SAT notin P/poly only after the generated-OR lower bound and the substitution bridge both remain valid for every fixed target exponent.
- controlled interface: if SAT has circuits of size n^c, substitute them into the M generated queries after computing the shared query list once; the source upper bound is N^{rho+o(1)}+N^{q+o(1)}.
- target-preserving condition: require d>1, max{rho,q}<1+epsilon, q>(1+epsilon)/2 for dense tuple leakage, uniform query length L=polylog N, and no advice except G_N plus the assumed target SAT circuits.

## Assumptions

- Source lower-bound model is nonuniform Boolean circuit SIZE on N-bit inputs.
- Generated queries are CNF encodings so a partial assignment p is a sound certificate when every clause has a literal fixed true by p.
- A cover P={P_j} is complete for the generated range when SAT(F_{N,j}(x)) implies some p in P_j satisfies F_{N,j}(x) as a partial assignment.
- Verifier overhead for checking a hardwired partial assignment against an L-bit CNF is L^{O(1)}=N^{o(1)}.

## Equations

- generated_or_carrier: `H_N(x)=\bigvee_{j=1}^{M}\operatorname{SAT}(F_{N,j}(x)),\qquad M=N^q,\qquad |F_{N,j}|=L=(\log N)^d.`. Valid when: Valid when the source object is the generated-OR CNF carrier with shared generator outputs and fixed q,d.
- partial_term_cover_complexity: `\tau_N^{\mathrm{term}}=\min_{\mathcal P}\sum_{j\le M}\sum_{p\in\mathcal P_j}(1+|p|).`. Valid when: Valid when each hardwired partial assignment p must satisfy every clause it certifies in the actual generated CNF range.
- cover_upper_bound: `\operatorname{SIZE}(H_N)\le C(G_N)+\tau_N^{\mathrm{term}}L^{O(1)}.`. Valid when: Applies when the generator computes all query blocks once and the circuit verifies each hardwired term locally.
- subthreshold_falsifier: `\tau_N^{\mathrm{term}}\le N^{1+\epsilon-\delta}\ \wedge\ C(G_N)\le N^{1+\epsilon-\delta}\Rightarrow \operatorname{SIZE}(H_N)\le N^{1+\epsilon-\delta/2}.`. Valid when: Requires polylogarithmic query length so the verifier overhead is swallowed by the exponent slack.
- target_substitution_bridge: `\operatorname{SAT}\in\operatorname{SIZE}(n^c)\Rightarrow \operatorname{SIZE}(H_N)\le N^{\max\{\rho,q\}+o(1)}.`. Valid when: Applies after the reduction preserves nonuniform advice accounting, shared generation, and the q,rho threshold parameters.

## Attempted Derivation

- Start with the previous necessary condition W_N^*>N^{1+epsilon-o(1)} for realized full satisfying witnesses.
- Try to infer SIZE(H_N)>N^{1+epsilon} from high W_N^* plus the valid target bridge max{rho,q}<1+epsilon.
- Observe that a circuit for H_N need not enumerate full witnesses; it may hardwire a partial term or another sound local certificate per position and verify it against the generated CNF.
- Construct the circuit OR_{j,p in P_j} TermSat(F_{N,j}(x),p) after computing all F_{N,j}(x) once; this decides H_N whenever P is a complete satisfying-term cover.
- Conclude that full-witness entropy is only a weak necessary condition and must be replaced by tau_N^{term}, or more robustly K_N^{cert}.

Blocking gap: No valid extraction theorem converts an arbitrary small circuit for H_N into a small full-witness set, and partial certificates give a concrete counter-mechanism.

## Falsifiers

- Small position-indexed satisfying-term cover tau_N^{term}<=N^{1+epsilon-delta} is a direct falsifier for the claimed source lower bound.
- Large full-witness projection entropy W_N^* with tiny planted partial terms falsifies the cycle-38 audit as sufficient evidence.
- A compact sound local certificate cover K_N^{cert} below threshold is a stronger nonuniform-leakage falsifier than promise-SAT easiness.
- If the query encoding is not CNF or lacks a cheap sound partial-certificate verifier, the term-cover lemma is not valid and must be replaced by the certificate-cover version.
- If rho or q reaches 1+epsilon, the target-preserving bridge collapses independently of the source audit.

## Learning

Cycle 39 sharpens the generated-OR source audit: full realized witness entropy is not the right gate because partial satisfying terms can compress many witnesses. The valid target bridge remains max{rho,q}<1+epsilon, but the route now needs a superthreshold lower bound against position-indexed partial-term covers, and ultimately against sound local certificate covers.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the witness-projection gate.`
- Rationale: The branch has repeatedly repaired leakage audits; a concrete planted-term generated range tests whether high realized witness entropy can coexist with an easy H_N, which directly affects the proof queue.
- Situation seed: Let G_N generate M=N^q CNF queries of length L=(log N)^d. At each position j, satisfiable queries contain one of h_j hardwired planted r-literal terms, while the remaining v-r variables are unconstrained enough to realize exponentially many full satisfying assignments.
- Varied variable: The planted term width r, with h=sum_j h_j adjusted near N^{1+epsilon-q}.
- Held-fixed controls: q in ((1+epsilon)/2,1+epsilon) so dense tuple features remain threshold-blocked., rho<1+epsilon and d>1 so the original target substitution bridge remains valid., Source lower-bound model is nonuniform SIZE on N-bit inputs., No target SAT circuit advice is used in the falsifier circuit; only G_N and the planted term cover are hardwired.
- Expected observation: For small r and h<=N^{1+epsilon-delta}, tau_N^{term} is subthreshold while W_N^* can be h 2^{v-r}; hence witness entropy can look large although H_N has a valid N^{1+epsilon-delta/2} upper bound.
- Transfer certificate needed: A formal generator specification proving CNF length L, shared generation size N^{rho+o(1)}, term-cover completeness on every generated positive query, and sound rejection of generated negative queries before the intuition can affect source lower-bound obligations.

## Next Experiment

Formalize tau_N^{term} as a set-cover problem over generated CNF ranges and test whether random-looking high-q generators can force tau_N^{term}>N^{1+epsilon} without making G_N nonexplicit or violating rho<1+epsilon.

# Barrier-Aware Lower-Bound Route: OBDD Target Gate

## Candidate Lemma

An OBDD lower bound is a valid bridge only to target classes with a proved OBDD compilation bound. A superpolynomial OBDD lower bound for SAT does not imply P != NP; the missing P-to-OBDD compiler is falsified by HWB in P.

## Definitions

- source object: a deterministic OBDD lower bound L(m) for SAT_m or another NP-complete Boolean function on m input bits, preferably minimizing over all variable orders.
- target object: P versus NP, formalized as excluding every uniform polynomial-time decider for SAT, not merely excluding OBDD or read-once branching programs.
- controlled interface: a compiler mapping each target computation of time or circuit size s(m) to an equivalent OBDD of size B_C(m,s), with variable-order advice explicitly counted.
- target-preserving condition: for every polynomial target bound s=m^k, the source lower bound must satisfy L(m)>B_C(m,s) after reductions, padding, and order conventions are preserved.

## Assumptions

- OBDD size is deterministic and exact; randomized or nondeterministic branching programs require a separate model audit.
- If a fixed variable order is used, the target class must include that same fixed-order restriction; otherwise quantify over all orders.
- Karp reductions are not automatically OBDD-friendly; projections or read-once substitutions need separate preservation proofs.
- The route is outside no known barrier merely by being combinatorial; the obstruction here is target-model simulation, not relativization folklore.

## Equations

- restricted_transfer: `\operatorname{OBDD}(f_m)>B_{\mathcal C}(m,s)\ \Rightarrow\ f_m\notin\mathcal C_s`. Valid when: Valid when every size-s target computation in C has a proved OBDD compilation of size at most B_C(m,s).
- pnp_assumption_only_gives_circuits: `P=NP\ \Rightarrow\ \mathrm{SAT}_m\in TIME(m^k)\subseteq SIZE(m^{k+O(1)})\ \text{for some }k`. Valid when: Applies only after assuming a uniform polynomial-time SAT decider and using the standard time-to-circuit simulation.
- compiler_falsifier: `\operatorname{OBDD}(\mathrm{HWB}_m)=2^{\Omega(m)},\qquad \mathrm{HWB}\in P\subseteq SIZE(m^{O(1)})`. Valid when: Valid for deterministic OBDDs minimizing over variable orders and the standard hidden-weighted-bit function.

## Attempted Derivation

- Assume a route proves OBDD(SAT_m)>m^a, or even 2^{Omega(m)}, under all variable orders.
- Under P=NP we obtain a uniform time m^k SAT decider and hence polynomial-size Boolean circuits for SAT_m.
- To contradict the OBDD lower bound, we need a uniform compilation of every such P computation into OBDDs of size below L(m).
- HWB_m is in P and has exponential OBDD size for every order, so the needed universal P-to-OBDD compilation is false.

Blocking gap: No target-preserving p-simulation from P or SIZE(poly) into polynomial-size OBDDs exists; the bridge collapses before reaching P vs NP.

## Falsifiers

- HWB_m is the decisive falsifier: it lies in P yet has OBDD size 2^{Omega(m)} for every variable order.
- Polynomial-size circuits can compute functions with exponential OBDD size, so SIZE(poly) is not contained in OBDD(poly).
- Standard many-one reductions can destroy OBDD structure; NP-completeness alone is not an OBDD-preserving transfer certificate.
- Per-length variable-order advice can leak nonuniform power; fixed-order lower bounds are invalid for best-order OBDD targets unless advice is controlled.

## Learning

Cycle 39 adds a valid target gate: OBDD lower bounds transfer only to OBDD-compilable classes with an explicit B_C threshold. HWB in P is a concrete falsifier to direct P-vs-NP transfer. This is route-level progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe.`
- Rationale: The route risks confusing a restricted branching-program lower bound with a P-vs-NP separation; the real variable is a compilation threshold from P to OBDDs.
- Situation seed: Padded SAT family g_{m,t}(x,0^t)=SAT_m(x) paired with the HWB_m control function on the same m data variables; test any claimed polynomial P-to-OBDD compiler.
- Varied variable: OBDD compilation exponent alpha in B_P(m,m^k)=m^alpha, compared with a source lower bound L(m)=2^{cm}.
- Held-fixed controls: Uniform SAT encoding and padding map are held fixed., Deterministic exact OBDD semantics are held fixed., Variable-order descriptions are either minimized over or counted as advice., The computed Boolean function must be preserved exactly.
- Expected observation: For HWB, every fixed alpha fails, so a universal polynomial P-to-OBDD compiler cannot exist. A SAT OBDD lower bound only proves NP not subset OBDD(poly).
- Transfer certificate needed: A valid bridge must prove a uniform p-simulation from the named target class to OBDDs, or restrict the target to OBDD-compilable subclasses before any intuition affects proof obligations.

## Next Experiment

Audit read-k branching-program or OBDD-with-advice lower bounds: compute the exact advice and read parameter needed before a restricted lower bound can target NC, L, or P.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

A kappa-dense, E-canonical low-image MCSP carrier with an actual hard row at threshold 2^{epsilon m} yields an E-language lower bound of exponent every delta<epsilon/(kappa(1+D)). This is a route bridge, not a proof of P != NP.

## Definitions

- source object: For source length m, V_m is an E-uniform certificate verifier/emitter whose distinct accepted images are truth tables T_{m,r}:{0,1}^m->{0,1}, r<M_m, with M_m<=2^{D m+o(m)}.
- target object: L_V is the padded multiplexed E language whose core maps (r,x) to T_{m,r}(x), with |r|=ceil(log M_m) and |x|=m.
- controlled interface: Parameters epsilon,D,kappa and an E-canonical distinct-image unranking algorithm; on each source length there is an accepted row T_{m,r} with unrestricted circuit complexity C(T_{m,r})>2^{epsilon m}.
- target-preserving condition: The source length schedule, row ranks, unranking, and padding are uniform and advice-free; padding changes only input length and preserves the nonuniform circuit lower-bound implication.
- kappa-density means successive usable core lengths grow by at most a factor kappa+o(1).
- The row complexity C(T) is unrestricted Boolean circuit size for the m-input function whose truth table is T.

## Assumptions

- Source lengths form a kappa-dense infinite set, or an all-length padded schedule with the same multiplicative loss.
- Distinct-image unranking runs in 2^{O(m)} time, so the multiplexed target language is in E.
- For every usable m, at least one canonical row has MCSP no-side threshold C(T)>2^{epsilon m}.
- No nonuniform selector or advice is used to choose m, r, or a duplicate representative.

## Equations

- image_entropy: `M_m \le 2^{D m+o(m)}`. Valid when: Valid when duplicate certificates are quotiented by an E-canonical distinct-image ranking procedure.
- core_length: `n_m=m+\lceil \log M_m\rceil=(1+D)m+o(m)`. Valid when: Applies when rank bits and row input bits are both present in the multiplexed target.
- direct_transfer: `\delta < \frac{\epsilon}{\kappa(1+D)}`. Valid when: Applies after the hard row is multiplexed, padding is uniform, and source lengths are kappa-dense.
- row_fixing_contrapositive: `C(T_{m,r})>2^{\epsilon m}\;\Longrightarrow\; C(A_m)>2^{\epsilon m-o(m)}`. Valid when: Requires the unrestricted nonuniform circuit model where fixing rank bits is a valid size-preserving restriction.

## Attempted Derivation

- Let d_m=ceil(log M_m) and A_m(r,x)=T_{m,r}(x).
- Assume every row is easy: C(T_{m,r})<=2^{epsilon m}. Hardwire the M_m row circuits and select by r; this gives C(A_m)<=2^{(D+epsilon)m+o(m)}.
- Therefore an unrestricted aggregate lower bound C(A_m)>2^{q(d_m+m)} forces a hard row only when q(1+D)>D+epsilon.
- If such a hard row exists directly, the multiplexed target already has lower bound exponent epsilon/(1+D) on core lengths, and kappa-padding gives delta<epsilon/(kappa(1+D)).
- Trying to replace the unrestricted aggregate lower bound by uniform decoder hardness fails: nonuniform circuits can hardwire row circuits, and constant-row or easy-row aggregates defeat the implication.

Blocking gap: The route still lacks a source theorem proving either an actual MCSP-hard canonical row or an unrestricted aggregate lower bound above q_force with cap slack.

## Falsifiers

- falsifier: a ranked decoder of size 2^{beta(1+D)m} with beta<epsilon/(1+D) makes every canonical row subthreshold for MCSP.
- falsifier: D exceeds the aggregate cap slack D<(alpha_A-epsilon)/(1-alpha_A), so aggregate row-forcing cannot be certified by that method.
- falsifier: the aggregate lower bound is only uniform, restricted-circuit, algebraic, or index-hardness; it does not imply unrestricted row hardness.
- falsifier: the length schedule or hard-row choice uses nonuniform advice, invalidating the E target-preserving extraction.
- falsifier: accepted images are not E-canonically unrankable, so the multiplexed language is not a valid E object.

## Learning

Cycle 39 separates three exponents: q_extract=epsilon/(1+D) for direct hard-row transfer, q_force=(D+epsilon)/(1+D) for unrestricted aggregate row-forcing, and the ranked-decoder leakage cutoff epsilon/(1+D). The valid bridge survives, but aggregate evidence is useful only above q_force with cap slack; otherwise the route must produce a tiny-D direct row-hardness certificate.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch needs a concrete parameter audit distinguishing direct hard-row extraction from aggregate row-forcing; another abstract MCSP-carrier slogan would not decide which source theorem remains viable.
- Situation seed: For each m and D, define a padded low-image carrier V_{m,D} with M=2^{D m} canonical ranks. Rank 0 emits a candidate high-MCSP table H_m, all other ranks emit a fixed easy table, and the target core is A_{m,D}(r,x).
- Varied variable: Distinct-image entropy D, varied from 0 to 1 while epsilon and kappa are held fixed.
- Held-fixed controls: Unrestricted nonuniform circuit size is the lower-bound model for rows and aggregates., The candidate hard row threshold is C(H_m)>2^{epsilon m}., Canonical unranking is E-uniform and advice-free., Padding preserves kappa-dense target lengths., No natural large property over a dense set of truth tables is introduced.
- Expected observation: Direct extraction gives exponent epsilon/(kappa(1+D)) whenever H_m is genuinely hard, but aggregate forcing requires q>(D+epsilon)/(1+D). With alpha_A=1/2 and epsilon=0.45, D>0.1 is a cap-slack falsifier for aggregate forcing while direct row extraction would still be valid if H_m were certified.
- Transfer certificate needed: A non-natural, advice-free proof that H_m has unrestricted circuit complexity above 2^{epsilon m}, or alternatively an unrestricted aggregate lower bound above q_force with declared cap slack; uniform or restricted lower bounds are not valid certificates.

## Next Experiment

Try D=o(1) direct-row carriers: formalize a certificate object whose verification is sequential E-time, has no ranked decoder below 2^{epsilon m-o(m)}, and proves one canonical row is MCSP-hard without a large constructive property.
