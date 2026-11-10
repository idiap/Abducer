# cycle-0034

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: tuple-feature residual gate

## Candidate Lemma

For the generated-OR SAT carrier, any low-cost arity-t tuple-feature transcript plus a low-cost residual circuit is a concrete subthreshold upper bound for H_N. Therefore a valid N^{1+epsilon} source lower bound must defeat every such tuple-feature residual system below the threshold, not only single-formula selectors or separators.

## Definitions

- source object: H_N(x)=OR_{j<M_N} SAT(B_N(x)_j), where |x|=N, M_N=N^q, B_N outputs M_N formulas of length L=(log N)^d with d>1, and B_N has nonuniform circuit size N^{rho+o(1)}.
- target object: SAT notin P/poly, obtained route-theoretically from a general-circuit lower bound C(H_N)>N^{1+epsilon} under the generated-query substitution interface.
- controlled interface: hypothetical SAT circuits are substituted only into the generated polylogarithmic queries; source-side falsifiers are nonuniform tuple-feature transcripts followed by an aggregator and a residual correction circuit.
- target-preserving condition: max{rho,q}<1+epsilon with a fixed positive margin, L=(log N)^d for d>1, no N-dependent advice except the circuits being counted, and no exhaustive SAT lookup hidden inside the source audit.
- A tuple-feature system has arity t, r=N^s predicates P_i on t generated formulas, predicate cost N^{alpha+o(1)}, aggregator cost N^gamma, and residual E_N=H_N xor S_N of cost N^lambda.
- The transcript bit z_i(x) is OR over all ordered t-tuples of generated formulas of P_i(B_N(x)_{j_1},...,B_N(x)_{j_t}); S_N(x)=A_N(z_1(x),...,z_r(x)).

## Assumptions

- q,rho,epsilon are fixed constants and max{rho,q}<1+epsilon is separated by Omega(1).
- The batch generator B_N is shared once; tuple enumeration costs M_N^t=N^{tq}.
- Predicate, aggregator, and residual circuits are nonuniform but receive only their specified inputs.
- The source lower bound is against unrestricted Boolean circuits for H_N, not against a restricted tuple-feature model.

## Equations

- tuple_feature_upper_bound: `C(H_N) \le N^{\rho+o(1)}+N^{s+tq+\alpha+o(1)}+N^\gamma+N^\lambda.`. Valid when: Valid when the batch generator is shared once, tuple features are densely enumerated over all M_N^t tuples, and E_N exactly computes H_N xor S_N.
- subthreshold_falsifier_exponent: `\theta_t:=\max\{\rho,\,s+tq+\alpha,\,\gamma,\,\lambda\}<1+\epsilon \;\Rightarrow\; C(H_N)\le N^{1+\epsilon-\Omega(1)}.`. Valid when: Valid when all exponent inequalities have a fixed margin and polynomially many additive circuit components are absorbed into the maximum exponent.
- target_substitution_bridge: `SAT\in SIZE(n^c) \;\Rightarrow\; C(H_N)\le N^{\max\{\rho,q\}+o(1)}.`. Valid when: Applies after SAT circuits are substituted only into length L=(log N)^d generated queries, so L^c=N^{o(1)} for each fixed c.
- route_magnification_consequence: `C(H_N)>N^{1+\epsilon}\ \text{eventually and}\ \max\{\rho,q\}<1+\epsilon \;\Rightarrow\; SAT\notin P/poly.`. Valid when: Requires an eventually valid unrestricted-circuit lower bound for the named carrier and fixed target-preserving parameters q,rho,epsilon with positive slack.

## Attempted Derivation

- Fix the generated-OR carrier H_N from the previous cycles with M_N=N^q generated SAT instances of length L=(log N)^d and batch generator size N^{rho+o(1)}.
- Choose r=N^s arity-t predicates P_i. After computing the batch B_N(x), enumerate all M_N^t ordered tuples and OR the predicate outputs to obtain transcript bits z_i(x).
- The transcript circuit size is at most N^{rho+o(1)} plus r M_N^t N^{alpha+o(1)}, giving exponent max{rho,s+tq+alpha}.
- Apply an aggregator A_N of size N^gamma to obtain S_N(x). If a residual circuit E_N of size N^lambda computes H_N(x) xor S_N(x), then H_N is computed by S_N xor E_N.
- Summing these components gives C(H_N)<=N^{rho+o(1)}+N^{s+tq+alpha+o(1)}+N^gamma+N^lambda.
- Thus any claimed source lower bound C(H_N)>N^{1+epsilon} must imply theta_t>=1+epsilon-o(1) for every such tuple-feature residual system.
- Independently, if SAT has n^c-size circuits, substituting them into the M_N polylogarithmic generated queries gives C(H_N)<=N^{max{rho,q}+o(1)}, so the target bridge remains valid when max{rho,q}<1+epsilon.

Blocking gap: The derivation gives an exact upper-bound falsifier class, but it does not prove that arbitrary small circuits for H_N factor through low-arity tuple transcripts. The remaining source obligation is a genuine unrestricted-circuit lower bound or a non-natural theorem ruling out all residual systems and all non-factored circuits.

## Falsifiers

- tuple-feature falsifier: some arity t system has max{rho,s+tq+alpha,gamma,lambda}<1+epsilon and an exact or low-cost residual for H_N.
- sparse-tuple falsifier: the carrier admits a selector or algebraic shortcut computing the same tuple transcript below the dense M_N^t exponent.
- target-window falsifier: max{rho,q}>=1+epsilon, so the SAT-circuit substitution no longer contradicts the claimed source lower bound.
- lookup falsifier: L or the generated range is small enough that SAT labels on the relevant range are nonuniformly tabulated below N^{1+epsilon}.
- nonuniform-leakage falsifier: advice encodes a hitting family for positive bags or a separator for negative bags with subthreshold residual correction.
- natural-proof falsifier: the only available source proof is a large constructive property of truth tables, leaving the route blocked under standard PRF-based natural-proofs barriers.
- model-mismatch falsifier: the tuple lower bound is proved only for restricted circuits while the target bridge requires unrestricted P/poly substitution.

## Learning

Cycle 34 adds a quantitative tuple-arity term to the generated-OR audit. The valid target bridge still needs only max{rho,q}<1+epsilon, but the source lower bound must rule out every subthreshold tuple-feature transcript with exponent s+tq+alpha and residual exponent lambda. This yields a finite dense-arity falsifier search and a sharper nonuniform-leakage obstruction, without claiming P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the generated-OR carrier.`
- Rationale: The previous feature-aggregator audit covered single-formula leakage; a concrete pairwise or low-arity construction tests whether correlations among generated formulas collapse H_N below the source threshold while preserving the SAT-substitution target bridge.
- Situation seed: Construct a generated-OR family with M_N=N^q polylog-length SAT queries per input, where individual formula labels look balanced but positive bags contain a detectable pair pattern P_2(phi_i,phi_j) and negative bags contain no such pair. The carrier remains H_N(x)=OR_j SAT(phi_j), but S_N(x)=OR_{i,j} P_2(phi_i,phi_j) is intended to match H_N on most or all inputs.
- Varied variable: Tuple arity t, starting with t=2 and then increasing until the dense enumeration exponent tq crosses 1+epsilon.
- Held-fixed controls: L=(log N)^d with d>1, so full SAT lookup on all possible queries is not a subthreshold explanation., Batch generator size exponent rho and query-count exponent q remain below 1+epsilon, preserving the target bridge., No extra advice is allowed beyond the nonuniform circuits counted in rho, alpha, gamma, and lambda., The source lower bound remains an unrestricted circuit lower bound for H_N, not a restricted-model claim.
- Expected observation: If 2q+alpha<1+epsilon and the pair predicate leaves residual exponent lambda<1+epsilon, then the generated-OR source lower bound is invalid for this carrier even though local selector audits may pass. If 2q>=1+epsilon, pair leakage is not a subthreshold falsifier without a sparse shortcut.
- Transfer certificate needed: A formal construction of B_N and P_t proving S_N=H_N or bounding C(H_N xor S_N), plus verification that SAT-circuit substitution still gives C(H_N)<=N^{max{rho,q}+o(1)} and that P_t does not hide exhaustive SAT lookup.

## Next Experiment

Instantiate the pair-pattern thought experiment for t=2: choose q with q<1+epsilon and test whether 2q+alpha<1+epsilon permits a subthreshold pair separator S_N; compute the residual complexity C(H_N xor S_N) and check for hidden SAT lookup.

# Barrier-Aware Lower-Bound Route: balanced matrix rank gate

## Candidate Lemma

Balanced matrix rank is a valid lower-bound carrier only for target classes with a proved low balanced-communication or low rank-decomposition upper bound. It cannot by itself target full nonuniform SIZE(poly), since an equality slice has maximum rank and linear-size Boolean circuits.

## Definitions

- source object: for an m-bit Boolean slice f_m and a fixed balanced partition pi=(X,Y), define the communication matrix M_pi(f_m) with rows x in {0,1}^r and columns y in {0,1}^r, where r=floor(m/2).
- target object: nonuniform SIZE(m^k), or a restricted class T_s whose functions have balanced deterministic communication cost at most c_T(m,s) under the same partition.
- controlled interface: a rank lower bound transfers only through a certified upper bound rank_F(M_pi(g)) <= R_T(m,s) for every target function g, with the same field, partition, and input length.
- target-preserving condition: pi, F, m, and s=m^k are fixed before seeing the candidate hard slice, and no advice may choose a partition that hides high-rank easy functions.

## Assumptions

- Field F is fixed and explicitly named; F_2 and R are the main audit cases.
- The rank certificate is computed from the full truth table of f_m, so constructivity is measured in poly(N) time for N=2^m.
- For the transfer half, every function in the named target class has a deterministic balanced protocol or equivalent rank-one decomposition of the stated cost.
- For the full-SIZE refutation, the target includes ordinary fan-in-two Boolean circuits with NOT gates and polynomial size.

## Equations

- matrix_definition: `M_{\pi}(f)[x,y]=f(\pi^{-1}(x,y)),\quad x,y\in\{0,1\}^{r},\quad N=2^{m},\quad \dim M_{\pi}=2^{r}\times 2^{r}.`. Valid when: Valid when the input slice length and balanced partition are fixed before evaluating the rank certificate.
- protocol_rank_upper_bound: `\operatorname{rank}_{F}(M_{\pi}(g))\le 2^{D_{\pi}(g)}.`. Valid when: Applies when a deterministic protocol partitions the same matrix into at most 2^{D_pi(g)} monochromatic rectangles.
- restricted_transfer: `\bigl[\operatorname{rank}_{F}(M_{\pi}(f))>2^{c_T(m,s)}\bigr]\ \wedge\ \bigl[\forall g\in T_s,\\ D_{\pi}(g)\le c_T(m,s)\bigr]\Rightarrow f\notin T_s.`. Valid when: Requires the target-preserving communication upper bound for every target function under the identical partition and size parameter.
- equality_max_rank: `\operatorname{rank}_{F}(M_{\pi}(EQ_r))=2^{r}=\sqrt{N}\quad\text{and}\quad EQ_r\in SIZE(O(m)).`. Valid when: Valid when EQ_r compares the two sides of the audited balanced partition and F is any field.
- full_size_threshold_collapse: `\sup_{g\in SIZE(O(m))}\operatorname{rank}_{F}(M_{\pi}(g))=2^{r}.`. Valid when: Valid for every fixed balanced partition because the corresponding equality function is easy and achieves maximum rank.

## Attempted Derivation

- Fix m=2r and a balanced partition pi of SAT_m's input bits.
- Try to prove rank_F(M_pi(SAT_m)) > m^k and infer SAT_m notin SIZE(m^k).
- Use the standard bridge rank_F(M_pi(g)) <= 2^{D_pi(g)} for functions with deterministic communication cost D_pi(g).
- The needed target bound would be D_pi(g) <= O(log m) for every g in SIZE(m^k), or equivalently rank_F(M_pi(g)) <= poly(m).
- This target bound is false: EQ_r under the same partition has rank 2^r and has Boolean circuit size O(m).
- The only valid conclusion from a rank lower bound is separation from classes with separately proved low balanced communication, not from full SIZE(poly).

Blocking gap: There is no target-preserving theorem converting polynomial Boolean circuit size into sublinear balanced communication or low matrix rank. The threshold collapses to the maximum rank sqrt(N).

## Falsifiers

- EQ_r is a concrete falsifier: it has O(m)-size Boolean circuits and rank_F(M_pi(EQ_r))=2^r for every field.
- If c_T(m,s) >= r, then the transfer threshold 2^{c_T} is at least the maximum possible rank, making the route vacuous.
- Choosing pi after seeing SAT_m is an advice-leakage falsifier unless the same pi also upper-bounds every target circuit.
- High real sign rank, high F_2 rank, and high deterministic communication complexity are invalid as full-SIZE(poly) certificates without an additional low-protocol theorem for the target class.

## Learning

Cycle 34 isolates a valid quantitative gate: balanced matrix rank proves lower bounds only for low-communication or low-rank-decomposition targets with threshold rank>2^{c_T}. The full SIZE(poly) route fails because equality is easy and has maximum rank under the audited partition. This is route-level barrier progress, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe.`
- Rationale: The branch needs to test whether matrix-rank evidence distinguishes hard languages from easy high-rank gadgets, rather than merely restating a communication-complexity lower bound.
- Situation seed: For each m=2r+p, define an easy padded slice E_{r,p}(x,y,z)=1[x=y], where x,y in {0,1}^r are the two sides of the audited partition and z is ignored padding.
- Varied variable: Vary the equality-block fraction beta=2r/m while holding the target SIZE(m^k) fixed.
- Held-fixed controls: The partition pi is announced before rank computation., The field F is fixed, e.g. F_2 or R., The target class remains ordinary nonuniform Boolean SIZE(m^k)., The construction is explicit and decidable in polynomial time.
- Expected observation: As beta increases, rank_F(M_pi(E_{r,p})) grows as 2^r=2^{beta m/2}, while circuit size stays O(m). Thus rank can be maximized by an easy language.
- Transfer certificate needed: Before rank intuition may enter the proof queue, the route must prove a low-rank or low-communication upper bound for every function in the named target class under the same partition; this certificate is impossible for full SIZE(poly) because of the equality falsifier.

## Next Experiment

Audit multiparty cylinder-intersection or tensor-rank routes with the same gate: name the target class, compute the NOF protocol threshold, and test generalized equality or inner-product gadgets as falsifiers for full SIZE(poly).

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For a canonical low-image MCSP carrier, forcing one 2^{epsilon m}-hard row through the ranked aggregate decoder requires an aggregate lower bound above the full selector-multiplexer threshold M_m 2^{epsilon m}. Conversely, a single hard row gives the multiplexed E language a lower bound of exponent epsilon/(1+D) before kappa padding. This is a valid bridge lemma and a quantitative falsifier for under-threshold aggregate certificates.

## Definitions

- source object: a canonical distinct-image family I_m={y_{m,0},...,y_{m,M_m-1}} subset {0,1}^{2^m} emitted by E-verifiable short MCSP certificates, with M_m<=2^{D m+o(m)}.
- target object: the E-uniform aggregate language A(1^m,j,x)=y_{m,j}[x] on rank j and row index x, padded from kappa-dense source lengths to all target lengths.
- controlled interface: ranked aggregate decoding with E-canonical unranking, no advice, no nonuniform hard-row selector, and no subthreshold random access to rows.
- target-preserving condition: kappa-dense source lengths, verifier cap epsilon<=alpha_V, unrestricted circuit lower bounds, E-uniform quotient/unranking, and row truth tables interpreted as MCSP no-side witnesses at threshold 2^{epsilon m}.

## Assumptions

- Rows are Boolean truth tables on m input bits, so row length is N_m=2^m.
- The number of distinct emitted rows satisfies M_m<=2^{D m+o(m)} for a fixed D>=0.
- The aggregate decoder is computable in deterministic 2^{O((1+D)m)} time by canonical unranking and sequential emission.
- Circuit lower bounds are against unrestricted nonuniform Boolean circuits unless a restricted class is explicitly named.
- The source verifier accepts only rows intended for the carrier; existential hardness is allowed because the aggregate target contains all ranks.

## Equations

- image_entropy: `M_m=|I_m|\le 2^{D m+o(m)},\quad \ell_m=m+\lceil \log M_m\rceil=(1+D)m+o(m)`. Valid when: Valid when the image family has at most 2^{D m+o(m)} distinct rows and rank bits are part of the target input.
- all_easy_mux_upper_bound: `C(A_m)\le \sum_{j<M_m}(C(y_{m,j})+m^{O(1)})\le M_m(2^{\epsilon m}+m^{O(1)})\le 2^{(D+\epsilon)m+o(m)}`. Valid when: Valid when every row has a general Boolean circuit of size at most 2^{epsilon m} and unrestricted circuits may multiplex by equality on the rank.
- aggregate_forces_row: `C(A_m)>2^{(D+\epsilon)m+o(m)}\Rightarrow \exists j<M_m\; C(y_{m,j})>2^{\epsilon m}`. Valid when: Valid when the aggregate lower bound is for unrestricted circuits and exceeds the full selector-multiplexer upper bound for all-easy rows.
- extracted_target_exponent: `\delta<\frac{\epsilon}{\kappa(1+D)}`. Valid when: Applies after kappa-dense source lengths are padded uniformly and the aggregate input length is (1+D)m+o(m).
- aggregate_certificate_threshold: `\eta_{force}=\frac{D+\epsilon}{1+D}`. Valid when: Valid when aggregate hardness is quoted as a size exponent relative to its own input length ell_m.

## Attempted Derivation

- Define the canonical image matrix with M_m<=2^{D m+o(m)} rows and 2^m columns; its entry function is A_m(j,x).
- Assume for contradiction that every emitted row has circuits of size at most 2^{epsilon m}.
- Build an unrestricted selector circuit for A_m by testing j against each rank and routing x into that row's circuit; size is at most M_m(2^{epsilon m}+m^{O(1)}).
- Conclude that an aggregate lower bound below 2^{(D+epsilon)m+o(m)} cannot force any row to be MCSP-hard.
- Conversely, if some row is 2^{epsilon m}-hard, fixing rank bits in any circuit for A_m gives a row circuit, so A_m has size greater than 2^{epsilon m}.
- After padding kappa-dense source lengths and accounting for rank length, the valid extracted E lower-bound exponent is delta<epsilon/(kappa(1+D)).

Blocking gap: No noncircular method is known here for proving the required unrestricted aggregate lower bound above exponent eta_force=(D+epsilon)/(1+D). Such a theorem is itself a strong explicit E lower bound for A_m, while weaker aggregate evidence is consistent with all rows being easy.

## Falsifiers

- falsifier: a ranked aggregate decoder of size <=2^{epsilon m-o(m)} makes every emitted row MCSP-easy at the claimed threshold.
- falsifier: an aggregate lower bound with exponent eta<=(D+epsilon)/(1+D) cannot force a hard row, since the all-easy selector circuit remains possible.
- falsifier: nonuniform choice of a hard row gives only an advice-dependent language and is not a valid E-uniform target.
- falsifier: superlinear certificate length or noncanonical quotient unranking breaks E canonicalization before the carrier reaches the target.
- falsifier: using a restricted-class lower bound for A_m without selector-closure does not preserve unrestricted MCSP hardness.
- falsifier: adding dense random salt to raise image entropy risks a large constructive property and re-enters the natural-proofs obstruction.

## Learning

Cycle 34 converts the ranked-decoder concern into an exact threshold theorem. Low distinct-image entropy D costs twice: it reduces the extracted E exponent to epsilon/(kappa(1+D)) and raises the aggregate lower bound needed to force row hardness to (D+epsilon)/(1+D). The route remains valid but only with a very small-D, cap-compatible, non-natural source or a genuinely unrestricted aggregate lower bound; otherwise the aggregate method is circular or falsified.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The route now depends on the exact tradeoff between image entropy D, source threshold epsilon, and the aggregate lower-bound exponent. A concrete parameter sweep exposes whether low-image carriers help or merely move the lower-bound burden to A_m.
- Situation seed: For each m, let a sequential verifier accept a canonical set of M_m=2^{D m} certificates whose distinct outputs form an M_m by 2^m truth-table matrix; study the aggregate entry function A_m(j,x) with epsilon=0.1, kappa=1, and verifier cap alpha_V=1/2.
- Varied variable: image entropy rate D, tested at D=0, D=1/4, and D=1/2 while keeping the row threshold fixed.
- Held-fixed controls: unrestricted circuit MCSP threshold 2^{epsilon m} with epsilon=0.1, E-uniform canonical unranking and sequential emission, with no advice, kappa=1 source length density and padding discipline, verifier cap alpha_V=1/2, so epsilon is cap-compatible, aggregate target uses rank bits plus row index bits, not a nonuniform selected row
- Expected observation: As D increases, the forcing threshold eta_force=(D+epsilon)/(1+D) rises from 0.1 to 0.28 to 0.4, while the extracted exponent delta<epsilon/(1+D) falls from 0.1 to 0.08 to about 0.066. Thus bounded image entropy is only useful when D is very small and the source proof is genuinely structural.
- Transfer certificate needed: Before this intuition can enter the proof queue, provide either an unrestricted aggregate lower bound above 2^{(D+epsilon)m+o(m)} or an independent non-natural row-hardness certificate, plus E-uniform quotient unranking and proof that no subthreshold ranked decoder exists.

## Next Experiment

Instantiate a D=0 or D=o(1) canonical source candidate and audit whether its verifier can prove row hardness structurally while all ranked decoders require size >2^{epsilon m-o(m)}; reject it immediately if the proof reduces to counting images or to restricted-class aggregate hardness.
