# cycle-0041

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# One-sided promise-separator gate for high-q generated-OR magnification

## Candidate Lemma

For the high-q generated-OR carrier, the target substitution bridge remains valid, but any claimed N^{1+epsilon} source lower bound must first prove a superthreshold lower bound against approximate one-sided promise separators on the generated SAT ranges.

## Definitions

- source object: H_N(x)=OR_{j<=M_N} SAT(G_N(x,j)) on N input bits, where M_N=N^q and G_N emits L_N-bit 3CNF formulas.
- target object: SAT on L_N-bit formulas, with target consequence SAT notin P/poly, equivalently SAT notin SIZE(n^c) for every fixed c.
- controlled interface: G_N is a nonuniform or uniform-clean compact generator with C(G_N)<=N^{rho+o(1)}, and target circuits for SAT are substituted only into the emitted instances.
- target-preserving condition: q,rho<1+epsilon, d>1 for L_N=(log N)^d, no advice leakage in G_N, and the source lower bound is against general SIZE circuits for H_N.
- Sep_N^{1s}(E) is the minimum total size sum_j |D_j| of predicates D_j such that D_j(phi)=1 implies SAT(phi) on the relevant formula universe and at most E positive inputs x with H_N(x)=1 are missed by all D_j(G_N(x,j)).

## Assumptions

- epsilon>0 is fixed; q is in ((1+epsilon)/2,1+epsilon) to keep dense tuple features above threshold.
- L_N=(log N)^d with d>1, so L_N^c=N^{o(1)} for every fixed target exponent c.
- The error patch for E missed positive inputs is implemented by equality circuits of total size O(E N).
- One-sided soundness is semantic: false positives on unsatisfiable generated formulas are disallowed.

## Equations

- carrier: `H_N(x)=OR_{j=1}^{M_N} SAT(G_N(x,j)), M_N=N^q, L_N=(log N)^d`. Valid when: Valid when the source object is the generated-OR carrier with fixed position count and polylogarithmic emitted SAT length.
- target-substitution: `SAT in SIZE(n^c) => C(H_N) <= C(G_N)+O(M_N L_N^c+M_N)=N^{max{rho,q}+o(1)}`. Valid when: Applies after the reduction preserves nonuniformity and each emitted SAT query has length L_N=(log N)^d.
- separator-composition: `C(H_N) <= C(G_N)+O(Sep_N^{1s}(E)+E N)`. Valid when: Valid when the predicates are one-sided sound and the E missed positive inputs are patched by equality gates.
- necessary-source-gate: `C(H_N)>N^{1+epsilon} => Sep_N^{1s}(N^{epsilon-eta})>N^{1+epsilon-eta-o(1)} for every fixed eta>0`. Valid when: Requires C(G_N)<=N^{rho+o(1)} with rho<1+epsilon and uses the explicit equality-patching cost.
- magnification-consequence: `[C(H_N)>N^{1+epsilon} and max{rho,q}<1+epsilon] => SAT notin SIZE(n^c) for every fixed c`. Valid when: Valid when the lower bound is for the same H_N family and target substitution incurs only N^{o(1)} SAT-circuit overhead.

## Attempted Derivation

- Start with H_N(x)=OR_j SAT(G_N(x,j)) and retain q,rho<1+epsilon, L_N=(log N)^d.
- Substitute an assumed SAT circuit of size n^c into every emitted formula; since L_N^c=N^{o(1)}, obtain C(H_N)<=N^{max{rho,q}+o(1)}.
- Define D_j as one-sided promise separators for satisfiable formulas in the j-th generated range; OR_j D_j(G_N(x,j)) has no false positives for H_N.
- Patch E missed positive inputs by equality tests on x, giving C(H_N)<=C(G_N)+O(sum_j |D_j|+E N).
- Therefore any valid N^{1+epsilon} lower bound for H_N must lower-bound Sep_N^{1s}(N^{epsilon-eta}) above N^{1+epsilon-eta-o(1)} for every fixed eta>0.
- A random k-CNF calculation shows partial-assignment term covers need 2^{Omega((log N)^d)} terms per position, far above the allowed N^{1+epsilon-q} budget.
- Attempt to promote term-cover hardness to separator hardness by SAT self-reduction fails because D_j is promised only on generated formulas, and restrictions of generated formulas need not remain in the generated range.

Blocking gap: No valid extractor converts arbitrary one-sided semantic separators into partial witnesses; range closure under restrictions is absent, so term-cover calibration cannot certify Sep_N^{1s} lower bounds.

## Falsifiers

- threshold collapse if q>=1+epsilon or rho>=1+epsilon
- nonuniform leakage through small one-sided promise separators D_j
- model mismatch between syntactic term covers and semantic separators
- range-closure failure blocking witness extraction from D_j
- random-label or random-formula evidence that is not target-preserving for SAT
- natural-proof-style largeness if the separator lower bound is proved only by random counting

## Learning

Cycle 41 isolates the exact semantic object behind the sound-local-certificate audit: Sep_N^{1s}(E). Random term-cover calculations support the high-q polylog design, but they do not imply the needed separator lower bound. The main new obstruction is the term-cover versus one-sided semantic-separator gap.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and calibration experiment, not as proof evidence by itself.`
- Rationale: The route now hinges on whether high-entropy generated formulas defeat one-sided local separators; another abstract restatement would not distinguish certificate entropy from semantic separator leakage.
- Situation seed: High-q generated-OR carrier where G_N is intended to output pseudorandom k-CNF formulas on v=(log N)^d variables and m=alpha v clauses, with H_N(x)=OR_{j<=N^q} SAT(G_N(x,j)).
- Varied variable: Clause density alpha in the random k-CNF output distribution.
- Held-fixed controls: q in ((1+epsilon)/2,1+epsilon) so tuple-feature leakage is threshold-blocked, rho<1+epsilon and d>1 so the SAT-substitution target bridge remains valid, one-sided soundness: local predicates may not accept unsatisfiable generated formulas, no advice leakage beyond the circuit description of G_N
- Expected observation: As alpha stays below the satisfiability threshold but bounded away from zero, every fixed term list of size below 2^{gamma alpha v} covers only an exponentially small fraction of random formulas, while the decisive unknown is whether arbitrary size-N^{1+epsilon} semantic separators also fail.
- Transfer certificate needed: An explicit generator and a proof that its actual SAT-labeled range has Sep_N^{1s}(N^{epsilon-eta})>N^{1+epsilon-eta-o(1)}; term-cover resistance or random-label counting alone is not a valid target-preserving certificate.

## Next Experiment

Test a range-closure repair: augment G_N so restrictions of emitted formulas also appear in controlled positions, compute the q/rho overhead, and see whether this lets a one-sided separator self-reduce to a term cover without breaking the N^{1+epsilon} threshold.

# Barrier-Aware Lower-Bound Route: Bit-Query Threshold Collapse

## Candidate Lemma

A deterministic bit-query lower bound for SAT_m transfers to a time lower bound only up to the input-length ceiling. Thus it cannot be a valid P-vs-NP route for any exponent k>1, because every total m-bit slice has decision-tree complexity at most m.

## Definitions

- source object: deterministic adaptive bit-decision-tree complexity D(L_m) of the m-bit slice of SAT or an NP-complete language.
- target object: random-access deterministic time lower bound SAT notin DTIME(m^k) for a named fixed k, as a component of a P-vs-NP route.
- controlled interface: a T(m)-time random-access algorithm induces a decision tree of depth at most O(T(m)) by exposing only the input-bit probes along each computation path.
- target-preserving condition: the query lower bound must exceed the same-slice time threshold m^k after encoding, padding, and uniformity parameters are fixed; otherwise the transfer is not target-preserving.

## Assumptions

- The input is a total m-bit language slice, not a promise problem.
- The lower-bound method counts only queried input bits and gives no lower bound on computation after the bits are read.
- The time model charges at least one step for each input-bit probe.
- The target is P versus NP, not merely separation from sublinear-time or query algorithms.

## Equations

- full-read-upper-bound: `D(L_m) \le m`. Valid when: Valid when L_m is represented as a total Boolean function on exactly m accessible input bits.
- time-to-query-interface: `L \in \mathrm{DTIME}(t(m)) \Rightarrow D(L_m) \le O(t(m))`. Valid when: Applies when the random-access machine simulation preserves the same input encoding and bit-probe cost.
- query-to-time-contrapositive: `D(L_m)>c\,t(m) \Rightarrow L\notin \mathrm{DTIME}(t(m))`. Valid when: Requires that the only resource lower-bounded is deterministic input-query depth on the identical language slice.
- polynomial-threshold-collapse: `k>1 \Rightarrow \forall L_m,\; D(L_m)\le m < m^k`. Valid when: Valid in the asymptotic regime m to infinity with fixed polynomial-time exponent k greater than one.

## Attempted Derivation

- Type the source model as deterministic adaptive bit-query complexity D(SAT_m).
- Use the valid interface: any DTIME(t(m)) random-access algorithm for SAT_m yields a depth-O(t(m)) decision tree.
- Try to refute SAT in DTIME(m^k) by proving D(SAT_m)>c m^k.
- Observe the universal ceiling D(SAT_m)<=m for every m-bit total slice.
- For k>1, the required lower bound is mathematically impossible, independent of SAT structure.
- Test padding: ignored padding preserves NP-hardness but changes the target threshold from n^k to M^k while leaving the core query complexity at most n.

Blocking gap: The source measure lower-bounds only the number of input bits inspected. Polynomial-time algorithms may inspect all m bits and then perform m^k computation, so query hardness cannot exceed the threshold needed for P-vs-NP.

## Falsifiers

- Parity on m bits is in linear time and has D=R_0=m, a falsifier for maximal-query-complexity-to-P-hardness claims.
- Ignored-padding SAT remains NP-complete under polynomial many-one reductions but has query complexity only that of the unpadded core, exposing padding noninvariance.
- Exact-zero padded SAT can force queries to padding bits; such lower bounds certify syntax checking, not SAT hardness.
- Any full-scan algorithm that reads all bits before computing is a falsifier to claims that Omega(m) query lower bounds imply superlinear or superpolynomial time lower bounds.

## Learning

Cycle 41 adds a quantitative target gate for input-query lower-bound routes. A valid time transfer requires D(SAT_m)>m^k on the same slice, but D<=m for every total m-bit language. Padding makes the collapse sharper: NP-hard ignored-padding SAT has query complexity bounded by the unpadded core while the P-time threshold is measured in the padded length. This is route-level barrier progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a target-preserving falsifier probe for black-box input-query routes.`
- Rationale: Query lower bounds often look strong for SAT because they can reach the maximum m, but P-vs-NP needs exclusion of m^k time for arbitrary fixed k. Padding cleanly reveals the quantitative mismatch.
- Situation seed: Ignored-padding SAT family Pad_betaSAT_M(y,z)=SAT_n(y), with M=n^beta and beta constant; the padding coordinates are ignored, and NP-hardness is preserved by mapping y to (y,0^{M-n}).
- Varied variable: padding exponent beta
- Held-fixed controls: The SAT core encoding and NP-completeness reduction are fixed., The source lower-bound model is deterministic or bounded-error bit-query complexity., The target time class is random-access polynomial time measured in the total length M., Padding bits are ignored, not checked, so padding cannot create spurious query hardness.
- Expected observation: D(Pad_betaSAT_M)=D(SAT_n)<=n=M^{1/beta}. For every target exponent k>1/beta, even maximal core query hardness is below M^k, so the route loses target-preserving force.
- Transfer certificate needed: A formal padding-robust transfer showing the lower-bound measure exceeds the random-access time threshold in the total encoded length; without this certificate the intuition cannot enter the P-vs-NP proof queue.

## Next Experiment

Audit streaming-space lower bounds for SAT: vary pass count p and memory s, hold NP-completeness and total input length fixed, and compute whether a P-time algorithm can be compiled into the streaming model below the claimed lower-bound threshold.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

A direct-row MCSP carrier whose global proof invariant is a nonempty affine-linear syndrome of rank R contains a row with unrestricted circuit size O(Rm). Therefore such an invariant cannot soundly certify MCSP threshold s=2^{epsilon m} unless R=Omega(2^{epsilon m}/m).

## Definitions

- source object: a direct-row MCSP certificate family whose accepted rows y in {0,1}^{2^m} satisfy affine equations A_z y=b_z over F_2.
- target object: an unrestricted Boolean circuit lower bound CC_m(y)>s_m for the row truth table, later usable in the E-extraction bridge.
- controlled interface: certificate z exposes only an E-uniform affine syndrome matrix/vector pair and claims every accepted row is on the MCSP no-side.
- target-preserving condition: no advice, nonuniform selector, or hidden canonical choice may be used to delete the low-weight coset representative; the lower bound is for ordinary nonuniform circuits.
- rank R_z is rank(A_z) over F_2, not the number of written equations.
- circuit basis is fan-in two De Morgan gates; equality to an m-bit address has size O(m).

## Assumptions

- N=2^m and s_m=2^{epsilon m} with constant epsilon in (0,1).
- The affine property P_z={y: A_z y=b_z} is nonempty.
- Soundness claim is universal: P_z is a subset of the no-side of MCSP_{m,s_m}.
- The verifier may be global and sparse; no largeness assumption is used.

## Equations

- row-threshold: `N=2^m,\quad s_m=N^{\epsilon}=2^{\epsilon m}`. Valid when: Valid when m is the source input length and N is the full truth-table length of a candidate row.
- affine-coset-model: `\mathcal{P}_z=\{y\in \mathbb{F}_2^N: A_z y=b_z\},\quad \operatorname{rank}(A_z)=R_z`. Valid when: Valid when the proposed certificate predicate is exactly an affine-linear syndrome condition over truth-table bits.
- sparse-representative-bound: `\min_{y\in \mathcal{P}_z} CC_m(y)\le C R_z m`. Valid when: Valid when the affine coset is nonempty, because pivot columns span b_z and yield a support-at-most-R_z representative.
- soundness-rank-threshold: `\mathcal{P}_z\subseteq\{y:CC_m(y)>s_m\}\ \Longrightarrow\ R_z> s_m/(C m)`. Valid when: Valid when the source claims universal no-side soundness against unrestricted nonuniform circuits at threshold s_m.
- exponent-form: `R_z=2^{\beta m}\ \Longrightarrow\ \text{certifiable }\epsilon\le \beta+o(1)`. Valid when: Valid in the constant-exponent regime where polynomial and linear factors in m are absorbed into o(1).

## Attempted Derivation

- Model the requested global proof invariant as an explicit affine syndrome A_m y=b_m on the full truth table y of length N=2^m.
- Let R=rank(A_m). Since the accepted coset is nonempty, b_m lies in the span of the columns of A_m.
- Choose R pivot columns spanning the column space and solve A_m y=b_m using only those pivot coordinates.
- The resulting row has Hamming support at most R and is computed by an OR of at most R equality tests, giving circuit size O(Rm).
- Thus any affine syndrome of rank 2^{beta m} with beta<epsilon-o(1) accepts a row on the MCSP yes-side for threshold 2^{epsilon m}.
- The derivation therefore refutes affine/parity-check global invariants rather than proving a hard carrier.

Blocking gap: A surviving source must use a genuinely nonlinear, non-natural, advice-free global invariant. High-rank affine syndromes only avoid this falsifier at beta>=epsilon and still do not by themselves prove all accepted rows hard.

## Falsifiers

- low-rank affine or parity-check syndrome with rank exponent beta<epsilon
- coordinate-supported row evidence touching T<2^{epsilon m}/poly(m) positions
- canonical selector that hides pivot choices or hard rows as nonuniform advice
- aggregate lower bound for a restricted decoder rather than unrestricted row circuits
- unbounded distinct-image entropy D that collapses delta<epsilon/(kappa(1+D))
- verifier cap alpha_V below the claimed source threshold epsilon

## Learning

Cycle 41 proves an unconditional affine-invariant no-go: every nonempty rank-R affine syndrome over a truth table contains a support-at-most-R representative and hence a circuit of size O(Rm). This makes low-rank parity/checksum carriers a concrete falsifier even when they are sparse and outside the usual large natural-property barrier. The valid carrier-to-E transfer is unchanged; the source search is narrowed to nonlinear global invariants with bounded D and no advice.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The previous cycle demanded a global invariant; affine syndromes are the simplest global, sparse, non-large candidate, so testing them gives a concrete target-preserving falsifier rather than another slogan.
- Situation seed: For each m, take an E-explicit rank R=2^{beta m} parity-check matrix A_m over F_2 and syndrome b_m, and let the proposed MCSP carrier accept every truth table y with A_m y=b_m as a direct hard row.
- Varied variable: beta, the exponent in the affine rank R=2^{beta m}.
- Held-fixed controls: MCSP no-side threshold s_m=2^{epsilon m} for a fixed epsilon., Unrestricted nonuniform Boolean circuit target model., No advice and no nonuniform selector for choosing among rows in the coset., Image entropy D and padding loss kappa held fixed for the downstream extraction audit.
- Expected observation: For beta<epsilon, the pivot-supported coset representative has circuit size 2^{beta m+o(m)}, so the source is falsified. At beta>=epsilon the affine no-go no longer refutes soundness, but the syndrome still supplies no positive hard-row proof.
- Transfer certificate needed: Before intuition may affect proof obligations, certify that the source predicate is exactly affine and nonempty; if a nonlinear canonical selection is added, prove E-uniformity, no-advice selection, bounded D, cap compatibility, and unrestricted row hardness separately.

## Next Experiment

Audit low-degree polynomial and circuit-SAT-derived global invariants: determine whether they also contain low-circuit satisfying rows, or identify a nonlinear certificate model that evades affine sparse representatives without becoming large or advice-dependent.
