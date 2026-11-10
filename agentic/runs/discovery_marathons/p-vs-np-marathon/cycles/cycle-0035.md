# cycle-0035

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: high-q arity cutoff for generated-OR carriers

## Candidate Lemma

For the polylog-query generated-OR carrier, choosing q>(1+epsilon)/2 while keeping max{rho,q}<1+epsilon preserves the target SAT-to-H_N bridge and makes every dense tuple-feature leakage transcript of arity t>=2 automatically superthreshold. The remaining source obligation is a unary-feature residual lower bound, not an unbounded tuple-arity audit.

## Definitions

- source object: H_N(x)=OR_{1<=j<=M_N} SAT(G_N(x,j)), with M_N=N^q, query length L_N=(log N)^d for fixed d>1, and bulk generator size C(G_N)<=N^{rho+o(1)}.
- target object: SAT on L_N-bit formulas; the target consequence is SAT notin P/poly, obtained by contraposition from SAT in SIZE(n^c) for each fixed c.
- controlled interface: compact nonblackbox generated-OR substitution, where SAT circuits are used only on the generated polylog-length instances and all generator, transcript, aggregator, and residual costs are charged nonuniformly.
- target-preserving condition: max{rho,q}<1+epsilon and no subthreshold unary feature transcript plus residual correction computes H_N; dense tuple transcripts with t>=2 are excluded by the high-q arity cutoff.

## Assumptions

- General nonuniform Boolean circuit size is the source lower-bound model: C(H_N)>N^{1+epsilon-o(1)}.
- The generator is target-clean: its nonuniform advice is included in C(G_N), and it does not contain SAT labels for the generated range.
- Feature family parameters are: N^s feature predicates, tuple arity t, composed feature cost N^{alpha+o(1)}, aggregator size N^{a+o(1)}, and residual correction size N^{lambda+o(1)}.
- The tuple transcript is dense: all ordered t-tuples from [M_N]^t may be inspected; sparse selected-tuple leakage is charged separately as selector advice.

## Equations

- carrier_parameters: `M_N=N^q,\quad L_N=(\log N)^d,\quad C(G_N)\le N^{\rho+o(1)}`. Valid when: Valid when the carrier family has fixed exponents q,rho,d and the generator cost is charged in the N-input circuit model.
- target_substitution: `SAT\in SIZE(n^c)\ \Longrightarrow\ C(H_N)\le N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies when d>1 is fixed, c is constant, and each length-L_N SAT circuit contributes only L_N^c=N^{o(1)} overhead.
- dense_tuple_transcript_cost: `C(T_{s,t,\alpha})\le N^{s+tq+\alpha+o(1)}`. Valid when: Valid when N^s feature predicates are evaluated on all N^{tq} generated t-tuples and each composed predicate costs N^{alpha+o(1)}.
- compression_falsifier_bound: `C(H_N)\le N^{\max\{\rho,s+tq+\alpha,a,\lambda\}+o(1)}`. Valid when: Valid when an aggregator of size N^a on the transcript and a residual correction of size N^lambda exactly recover H_N.
- source_obligation: `C(H_N)>N^{1+\epsilon-o(1)}\Rightarrow \max\{\rho,s+tq+\alpha,a,\lambda\}\ge 1+\epsilon-o(1)`. Valid when: Requires the claimed source lower bound to hold against every nonuniform transcript, aggregator, and correction family in the named source model.
- high_q_cutoff: `q>(1+\epsilon)/2\ \wedge\ t\ge2\ \Longrightarrow\ s+tq+\alpha>1+\epsilon`. Valid when: Valid when feature-count and feature-composition exponents are nonnegative and dense enumeration of all t-tuples is charged.

## Attempted Derivation

- Instantiate H_N with M_N=N^q and L_N=(log N)^d, d>1, so SAT circuits of size L_N^c are N^{o(1)} after substitution.
- Assume SAT in SIZE(n^c). Composing the SAT circuit with the bulk generator and the OR over M_N queries gives C(H_N)<=N^{max{rho,q}+o(1)}; hence a valid H_N lower bound above N^{1+epsilon} contradicts every fixed c when max{rho,q}<1+epsilon.
- Model nonuniform leakage by N^s predicates on t-tuples of generated formulas, each composed predicate costing N^{alpha+o(1)}. Dense enumeration gives N^{s+tq+alpha+o(1)} transcript cost.
- If a size N^a aggregator plus residual correction of size N^lambda recovers H_N, then H_N has size N^{max{rho,s+tq+alpha,a,lambda}+o(1)}. Therefore any source lower bound must force this maximum to be at least 1+epsilon-o(1).
- Choose q>(1+epsilon)/2. Since s,alpha>=0, every t>=2 dense tuple transcript has exponent s+tq+alpha>1+epsilon, so it cannot be a subthreshold falsifier. The audit collapses to t=1 transcripts and residual corrections.

Blocking gap: No proof is known that an explicit high-q generator defeats all unary range-local transcripts and subthreshold residual corrections. High q may even help unary predicates by presenting many chances to hit a satisfiable generated formula.

## Falsifiers

- Unary feature residual compression with exponent max{rho,s+q+alpha,a,lambda}<1+epsilon is the decisive remaining falsifier.
- If q<=(1+epsilon)/2, binary tuple-feature transcripts can still be subthreshold and the high-q repair is invalid.
- If rho>=1+epsilon, the generator alone destroys the target-preserving bridge.
- If the generated range has a small promise SAT separator or low positive-fiber hitting cover, H_N may be easy despite global SAT hardness.
- If a proposed lower-bound proof yields a dense constructive truth-table property, the natural-proofs obstruction applies; the route must be range-dependent or otherwise non-natural.
- If the generator leaks SAT labels through advice or indexing structure, the source lower bound collapses by nonuniform leakage.

## Learning

Cycle 35 finds a parameter repair: set q in ((1+epsilon)/2,1+epsilon) to preserve the generated-OR target bridge while forcing every dense tuple-feature transcript of arity at least two above the N^{1+epsilon} threshold. The route-level lower-bound obligation is now the sharper unary residual minimax gate, not an infinite tuple-arity audit.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and parameter-selection certificate.`
- Rationale: The target bridge is already exact; the live uncertainty is whether tuple-feature leakage can be quantitatively quarantined before attempting a unary residual lower bound.
- Situation seed: Take H_N(x)=OR_{j<=N^q} SAT(G_N(x,j)) with L_N=(log N)^2, epsilon=0.20, rho=0.95, and a bulk generator producing polylog-size 3CNF instances without SAT-label advice.
- Varied variable: The query multiplicity exponent q is swept from 0.45 to 1.15.
- Held-fixed controls: Source model is general nonuniform circuits with threshold N^{1.20-o(1)}., Target consequence is SAT notin P/poly via length-(log N)^2 substitution., Truth-table lookup is disallowed by cost because 2^{L_N}=N^{omega(1)}., Aggregator, feature, selector, and residual correction costs are all charged in the N-input circuit budget.
- Expected observation: At q=0.60 the binary transcript exponent 2q reaches 1.20; for q>0.60 all dense arity-t>=2 leakage is superthreshold while the target bridge remains valid until q reaches 1.20. The experiment should leave unary residual compression as the only dense-arity falsifier.
- Transfer certificate needed: A formal certificate must show that the chosen high-q generator keeps rho<1.20, maintains semantic label balance on its generated range, and satisfies the unary residual minimax lower bound; otherwise the arity-cutoff intuition cannot enter the proof queue.

## Next Experiment

Formalize unary transcripts as monotone OR-of-range predicates, then test whether random-looking high-q generators make every subthreshold unary transcript leave residual circuit complexity above N^{1+epsilon-o(1)} or whether a selected-image separator falsifier appears.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Exact extension-complexity lower bounds are valid lower bounds for compact LP formulations, but they are not target-preserving for P versus NP. The implication xc(P_L,n)>poly(n) => L notin P is refuted by polynomial-time optimization problems whose polytopes have exponential extension complexity.

## Definitions

- source object: slack matrix S(P_n) of a 0/1 polytope family P_n, with rows indexed by facets and columns indexed by vertices; the source lower bound is nonnegative rank or extension complexity.
- target object: exact polynomial-size linear extended formulations LP_EF(n^k), not Boolean SIZE(n^k) circuits, P/poly, or uniform polynomial-time algorithms.
- controlled interface: Yannakakis factorization maps nonnegative factorizations of S(P_n) to LP extensions and back, preserving inequality count up to additive constants.
- target-preserving condition: any claimed P-vs-NP transfer must provide an algorithm-to-EF compiler for the same encoded optimization problem; otherwise the valid target remains only LP_EF.

## Assumptions

- P_n is a bounded polytope with a fixed facet-vertex slack matrix over rational data or an explicitly stated real-coefficient model.
- The lower bound is for exact LP extended formulations, not separation oracles, SDP lifts, randomized algorithms, or Turing-machine decision procedures.
- Input length is measured by the natural combinatorial encoding; for PM_m, the edge-coordinate dimension is e=binom(m,2).

## Equations

- Yannakakis factorization identity: `\operatorname{xc}(P)=\operatorname{rank}_{+}(S_P)`. Valid when: Valid when P is a bounded polytope with a named facet-vertex slack matrix and exact linear extensions are counted by inequalities.
- perfect matching falsifier threshold: `\operatorname{xc}(PM_m)=2^{\Omega(m)}=2^{\Omega(\sqrt e)}`. Valid when: Applies for the perfect-matching polytope of K_m with e=binom(m,2) edge coordinates and exact nonsymmetric LP extensions.
- forbidden compiler consequence: `(PM_m\in P \ \wedge\ \text{P-to-EF}_{\beta})\Rightarrow \operatorname{xc}(PM_m)\le e^{\beta}`. Valid when: Requires a target-preserving compiler turning every polynomial-time optimizer on e-bit encodings into exact LP extensions of size e^beta.

## Attempted Derivation

- Encode a candidate NP-complete family as 0/1 polytopes P_n and prove rank_+(S(P_n))>n^k for every fixed k.
- By Yannakakis, conclude P_n has no polynomial-size exact LP extended formulation.
- Try to infer that no polynomial-time algorithm decides the encoded language.
- This inference needs a compiler from arbitrary polynomial-time algorithms, or at least from polynomial-size circuits, into polynomial-size exact LP lifts for the same family.
- The compiler is impossible in this generality: perfect matching is in P while xc(PM_m)=2^{Omega(m)}.

Blocking gap: Static exact LP extension size is not a target-preserving proxy for adaptive polynomial-time computation.

## Falsifiers

- Perfect matching: PM_m is solvable in polynomial time but has exact LP extension complexity 2^{Omega(m)}, so EF hardness is not P-hardness.
- Polynomial-time separation does not imply compact extension: matching has efficient optimization/separation despite exponential exact xc.
- A lower bound on a TSP, cut, or SAT polytope may rule out one LP model but remains compatible with non-LP algorithms unless the target-preserving compiler is named.
- The barrier hypothesis 'nonnegative rank lower bound separates P from NP' is invalid without a valid algorithm-to-EF bridge.

## Learning

Cycle 35 isolates a concrete target-model failure: nonnegative-rank or extension-complexity lower bounds are valid for exact LP formulations, but not for P-vs-NP. Perfect matching is the decisive falsifier because it is in P and has exponential exact LP extension complexity. This is route-level progress only.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a concrete falsifier probe for the LP-extension route.`
- Rationale: The branch needs a target-preserving model audit because another abstract barrier label would miss the exact failure: EF lower bounds are strong but target the wrong computational object.
- Situation seed: Compare a hypothetical exponential lower bound for a SAT assignment polytope with Rothvoss's exponential lower bound for the perfect-matching polytope PM_m, while both are viewed through exact LP extended formulations.
- Varied variable: The compiler overhead beta in a proposed theorem saying that every n^a-time 0/1 optimizer yields an exact LP extension of size n^beta.
- Held-fixed controls: Exact LP extensions, not SDP lifts or randomized algorithms., Uniform polynomial-bit descriptions when an algorithmic implication is claimed., The natural edge-coordinate encoding e=binom(m,2) for PM_m., Target ambition remains P-vs-NP, so the transfer must reach arbitrary polynomial-time algorithms, not only LP_EF.
- Expected observation: For any finite beta, the proposed compiler predicts xc(PM_m)<=e^beta, contradicting xc(PM_m)=2^{Omega(sqrt e)} while PM_m remains polynomial-time solvable.
- Transfer certificate needed: A special nonblack-box compiler from SAT algorithms to compact exact EFs that explicitly excludes the matching falsifier, or else a retreat to the valid LP_EF target.

## Next Experiment

Audit semidefinite extension and PSD-rank routes: identify whether a polynomial-time problem with high SDP extension complexity gives the analogous falsifier, or whether the valid restricted target becomes SDP_EF rather than P.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For a kappa-dense E-canonical low-image MCSP carrier, aggregate decoder hardness below the full multiplex threshold is not a valid certificate of any high-MCSP row. It is target-preserving only if a hard row is certified directly, or if every small-row circuit-output unranker is excluded at the required quantitative level.

## Definitions

- source object: a family F_m of accepted certificates whose distinct emitted truth tables T_{m,r}:{0,1}^m->{0,1} have canonical ranks r in [M_m], M_m <= 2^{D m+o(m)}, and are verified in 2^{O(m)} time without advice.
- target object: an E-uniform language obtained from the multiplexed table G_m(r,x)=T_{m,r}(x), padded over kappa-dense source lengths, with desired unrestricted circuit lower bound 2^{delta n}.
- controlled interface: E-canonical distinct-image unranking plus an audited ranked decoder; no nonuniform selector, advice string, or subthreshold random-access implementation may choose the hard row.
- target-preserving condition: row hardness must be for unrestricted Boolean circuits at threshold 2^{epsilon m}, and ranking/padding overhead must preserve E-uniformity and the exponent delta < epsilon/(kappa(1+D)).

## Assumptions

- Source lengths are kappa-dense and certificate length is O(m), so exhaustive canonicalization remains in E.
- The verifier cap alpha_V satisfies epsilon <= alpha_V; otherwise the proposed MCSP no-side claim is already refuted by checkpoint circuits.
- Distinct-image entropy D is constant or o(1), and duplicate accepted certificates are quotiented before multiplexing.
- All lower bounds discussed for rows and for G_m are against unrestricted nonuniform Boolean circuits unless a restricted source model is explicitly named.
- A circuit-output unranker means a circuit family W_m(r,j) that outputs or evaluates a size-S circuit description for row r.

## Equations

- image_entropy: `M_m \le 2^{D m+o(m)}`. Valid when: Valid when duplicate accepted certificates are quotiented by an E-canonical distinct-image ranking before multiplexing.
- aggregate_length: `n_m=(1+D)m+o(m)`. Valid when: Valid when rank bits and row input bits are concatenated with only sublinear framing overhead.
- row_to_aggregate_extraction: `C(T_{m,r})>2^{\epsilon m} \Rightarrow C(G_m)>2^{\epsilon m}=2^{(\epsilon/(1+D)+o(1))n_m}`. Valid when: Applies after a fixed rank can be hardwired into any circuit for the aggregate decoder.
- unranker_leakage: `(\forall r\; C(T_{m,r})\le S)\land C(W_m)\le R \Rightarrow C(G_m)\le R+poly(S,m)`. Valid when: Requires the unranker to output or evaluate row circuits uniformly enough for universal-circuit composition.
- brute_multiplex_forcing_threshold: `C(G_m)>2^{(D+\epsilon)m+o(m)} \Rightarrow \exists r\; C(T_{m,r})>2^{\epsilon m}`. Valid when: Valid when no shared circuit-output unranker is assumed and the proof must rely only on brute multiplexing all easy rows.
- padded_E_exponent: `\delta < \epsilon/(\kappa(1+D))`. Valid when: Applies after source lengths are kappa-dense and the multiplexed language is padded to all relevant E input lengths.

## Attempted Derivation

- Let F_m have M_m<=2^{D m+o(m)} distinct accepted tables T_{m,r}, and form G_m(r,x)=T_{m,r}(x).
- A genuinely hard row immediately gives C(G_m)>2^{epsilon m}, because any circuit for G_m hardwired with r computes that row.
- To infer a hard row from aggregate hardness alone, assume contrapositively that every row has a circuit of size at most S=2^{epsilon m}.
- Without a shared circuit-output unranker, the only universal nonuniform simulation hardwires all row circuits and costs M_m*S=2^{(D+epsilon)m+o(m)}.
- Therefore aggregate hardness below q_force=(D+epsilon)/(1+D) can be explained by hard indexing, not row MCSP hardness.
- If a small circuit-output unranker W exists, then G_m has size R+poly(S,m); so aggregate hardness separates into either row hardness or unranker hardness.
- Combining with an aggregate access cap alpha_A gives the new viability inequality q_force<=alpha_A, equivalently D<=(alpha_A-epsilon)/(1-alpha_A).

Blocking gap: No current source construction supplies a bounded-D, cap-compatible, non-natural certificate of a hard row. Aggregate-only lower bounds in the intermediate window are not target-preserving.

## Falsifiers

- falsifier: aggregate lower bound with epsilon/(1+D)<q<(D+epsilon)/(1+D) but no direct row-hard certificate; hardness may be only rank-index hardness.
- falsifier: D>(alpha_A-epsilon)/(1-alpha_A), so the aggregate lower bound needed to force a row exceeds the checkpoint cap and is not valid.
- falsifier: a subthreshold circuit-output unranker W_m turns the ranked decoder into small circuits and invalidates the MCSP no-side claim.
- falsifier: sparse linear-form image family with hard-to-unrank coefficient set; all rows are easy although the ranked decoder can look hard.
- falsifier: nonuniform row selector or advice-dependent source length selection; the extracted E language would not be uniform.
- falsifier: restoring largeness by adding random salt; this re-enters the natural-proofs obstruction and also raises D.

## Learning

Cycle 35 identifies a sharper obstruction: low-image entropy D creates an index-hardness channel. The valid extraction exponent remains delta<epsilon/(kappa(1+D)) from an actual hard row, but aggregate-only row forcing needs q_force=(D+epsilon)/(1+D) and must also satisfy q_force<=alpha_A. Thus, with alpha_A=1/2, D<=1-2epsilon is mandatory; near the cap only D=o(1) is viable. This is route-level progress and a falsifier for aggregate shortcuts, not a proof of P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design-now-as-falsifier-probe`
- Rationale: The route now hinges on whether aggregate decoder hardness certifies row MCSP hardness or merely hides rank-index complexity. A concrete probe is more informative than another abstract barrier citation.
- Situation seed: Sparse linear-form carrier: choose an E-decidable sparse coefficient set S_m of size 2^{D m}; accepted images are T_a(x)=<a,x> mod 2 for a in S_m; the ranked decoder is G_m(r,x)=<unrank_{S_m}(r),x> mod 2. Every row has O(m)-size circuits, so any apparent MCSP no-side evidence must come from the unranking interface.
- Varied variable: D, the distinct-image entropy rate of the sparse coefficient set.
- Held-fixed controls: epsilon is a fixed positive row-hardness threshold, e.g. epsilon=0.45, and rows are tested against unrestricted Boolean circuits., kappa=1 source-length density and E-canonical distinct-image ranking are held fixed., No advice, nonuniform selector, or certificate-order ranking is allowed., Aggregate access cap alpha_A=1/2 is used as the checkpoint-control benchmark.
- Expected observation: For small but positive D, aggregate evaluation can appear hard because unrank_{S_m} is hard, while every row remains MCSP-easy. As D grows, q_force=(D+epsilon)/(1+D) crosses the cap-compatible window, certifying that aggregate-only forcing is invalid.
- Transfer certificate needed: Before this intuition may affect proof obligations, one must prove either a direct high-MCSP row certificate, or an aggregate lower bound at q_force that is below the declared cap alpha_A and cannot be attributed to circuit-output unranking hardness.

## Next Experiment

Audit D=o(1) certificate sources: polynomially many canonical images, epsilon<1/2 cap, no advice, and a proof-complexity or meta-complexity certificate that directly marks one row as MCSP-hard without using aggregate decoder hardness.
