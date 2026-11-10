# cycle-0063

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For a label-free XOR SAT carrier with polylogarithmic target queries, the beta=0 target bridge remains valid, but rank-based source evidence has a sharp fork: constructive low rank gives a subthreshold upper-bound falsifier, while very high rank makes the induced lower-bound property large in label space, so any poly(2^L)-constructive useful certificate is natural-proof exposed. A proof-relevant source lower bound must therefore be direct, non-large, nonconstructive, proof-mediated, or genuinely SAT-semantic and nonrelativizing.

## Definitions

- source object: H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)) on N-bit source inputs, where G_N is a label-free generator outputting SAT instances of length L=(log N)^d and M_N<=N^{q+o(1)}.
- target object: SAT_L as the length-L satisfiability language against nonuniform circuits SIZE(L^c), with the target consequence SAT notin P/poly when the implication holds for every fixed c.
- controlled interface: the F_2 incidence map A_N from label vectors ell on the generated formula universe U_N to source truth tables H_N^ell, together with generator overhead N^{rho+o(1)} and query budget N^{q+o(1)}.
- target-preserving condition: beta=0 via L=(log N)^d, d>1, max{rho,q}<1+epsilon, no SAT-label advice inside G_N, and the claimed lower bound is for the actual SAT label vector rather than for random labels.

## Assumptions

- Circuit model is nonuniform Boolean SIZE, and all source lower bounds are measured as C(H_N)>s_N with s_N=N^{1+epsilon}.
- The generator G_N is uniform or has its advice charged inside N^{rho+o(1)}; otherwise nonuniform leakage invalidates the transfer.
- For every fixed target exponent c, a hypothesized SAT circuit of size L^c may be substituted independently into all generated queries.
- The rank r_N is rank over F_2 of A_N; constructive low rank additionally means a row-coordinate decoder of size D_N computes coefficients of each source row in a fixed basis.
- The naturalness conclusion is conditional on a certificate being decidable from the length-|U_N| label truth table in poly(2^L) time, large under uniform random labels, and useful against all SIZE(L^c) label functions.

## Equations

- xor_carrier_definition: `H_N^{\ell}(x)=\bigoplus_{j\le M_N}\ell(G_N(x,j))=(A_N\ell)(x)`. Valid when: Valid when G_N is label-free, repeated generated formulas are counted modulo two, and ell is any Boolean label vector on the generated formula universe.
- beta_zero_target_substitution: `C(H_N^{SAT})\le N^{\rho+o(1)}+N^{q+o(1)}L^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after SAT has SIZE(L^c) circuits, L=(log N)^d is polylogarithmic, and generator/advice overhead is charged in rho.
- magnification_implication: `C(H_N^{SAT})>N^{1+\epsilon}\ \wedge\ \max\{\rho,q\}<1+\epsilon\ \Rightarrow\ SAT\notin SIZE(n^c)\text{ for every fixed }c`. Valid when: Requires the same carrier family, beta zero target-query length, and a valid source lower bound for the actual SAT labels.
- rank_density_count: `\Pr_{\ell\leftarrow\{0,1\}^{U_N}}[C(A_N\ell)\le s_N]\le 2^{O(s_N\log(s_N+N))-r_N}`. Valid when: Valid when A_N has F_2 rank r_N and low-complexity N-input source functions are counted by circuits of size at most s_N.
- constructive_low_rank_falsifier: `C(H_N^{SAT})\le D_N+O(r_N)`. Valid when: Requires an explicit row-coordinate decoder of size D_N and hardwiring the r_N basis parities of the actual SAT label vector as advice bits.

## Attempted Derivation

- Fix L=(log N)^d with d>1 and define A_N so that H_N^ell=A_N ell is the XOR of N^{q+o(1)} generated length-L labels per source input.
- Assume SAT_L has circuits of size L^c. Substitute the circuit into each query and add the generator cost to get C(H_N^{SAT})<=N^{max{rho,q}+o(1)}.
- If max{rho,q}<1+epsilon and a genuine source lower bound C(H_N^{SAT})>N^{1+epsilon} is available, the substitution contradicts SAT_L in SIZE(L^c) for that fixed c; since c was arbitrary, this is the valid beta=0 bridge to SAT notin P/poly.
- Audit the source proof. If rows of A_N have a basis-coordinate decoder of size D_N and rank r_N with D_N+O(r_N)<N^{1+epsilon}, hardwire the r_N SAT basis parities and compute H_N^{SAT} below threshold; this is a concrete falsifier.
- If r_N is much larger than s_N log(s_N+N), random label vectors produce high-complexity source functions with probability at least 1-2^{O(s_N log(s_N+N))-r_N}. Thus the semantic property C(A_N ell)>s_N is large in label space.
- Any certificate Q_N contained in this property, decidable from the label truth table in poly(2^L), accepting SAT, and rejecting every label function with SIZE(L^c) circuits is a natural-proof-style object against SIZE(L^c). The route must then state a non-natural escape or remain only outside the known barrier conditionally.
- Finally, rank-only hypotheses are relativizing-invalid: setting all labels to zero preserves A_N and its rank but makes H_N constant.

Blocking gap: The branch still lacks a direct non-natural lower bound for H_N^{SAT} or a nonrelativizing theorem extracting a label-free sketch from every small H_N circuit.

## Falsifiers

- positive beta black-box transfer cap q+beta*c+o(1), which blocks all-exponent target preservation unless beta=0 or subpolynomial
- constructive low-rank row-coordinate decoder with D_N+O(r_N)<N^{1+epsilon}
- label-free global codebook or sparse quotient-polynomial sketch below the source threshold
- rank-only proof surviving replacement of SAT labels by the zero oracle
- large poly(2^L)-constructive certificate useful against SIZE(L^c), triggering natural-proof exposure rather than a barrier escape

## Learning

Cycle 63 upgrades the rank-density fork into a quantitative gate: low constructive rank is a direct upper-bound falsifier, while high rank makes any efficient useful certificate large in label space. The beta=0 magnification bridge is still valid, but rank-only evidence is quarantined unless the source proof is direct or explicitly non-natural and nonrelativizing.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The current obstruction is not another abstract hardness-magnification slogan; it depends on the quantitative rank threshold r_N versus N^{1+epsilon} log N and on whether the certificate is constructive and large.
- Situation seed: Take an XOR carrier with L=(log N)^2, beta=0, q=(1+epsilon)/2, rho<1+epsilon, and a label-free generator whose incidence matrix A_N is compared against a planted low-rank variant with an explicit row-coordinate decoder.
- Varied variable: theta_N=r_N/(N^{1+epsilon} log N), the normalized F_2 incidence rank after SAT-preserving quotienting.
- Held-fixed controls: The target bridge parameters beta=0, q<1+epsilon, and rho<1+epsilon remain fixed., The source threshold remains C(H_N^{SAT})>N^{1+epsilon}., The generator is label-free and all advice is charged to rho or to the decoder cost., The target object is still SAT_L against SIZE(L^c) for arbitrary fixed c.
- Expected observation: For theta_N below the decoder threshold the low-rank falsifier computes H_N^{SAT} by hardwired basis parities; for theta_N well above a constant, random labels almost always yield hard H_N^ell, so an efficient semantic certificate becomes large and naturalness-exposed.
- Transfer certificate needed: Before the intuition may affect proof obligations, prove either D_N+O(r_N)<N^{1+epsilon} for the planted low-rank case, or prove that any proposed high-rank certificate is non-large, nonconstructive, proof-mediated, or SAT-semantic in a way not captured by label-space naturalness.

## Next Experiment

Perform the finite prior-art boundary check for the label-space naturalness claim, then instantiate the thought experiment with a concrete pairwise-independent generator and compute r_N, quotient rank, and any row-coordinate decoder cost D_N.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Seeded SAT-labelled point-agreement certificates cannot be simultaneously poly(N)-large, poly(N)-constructive, and useful against SIZE_m(m^k) for k>2 when the seed length is O(log N).

## Definitions

- source object: a seed e of length r selecting h distinct m-bit SAT instances x_i(e) with labels b_i=SAT(x_i(e)).
- target object: nonuniform Boolean circuits SIZE_m(s) on m inputs, with s=m^k and truth-table length N=2^m.
- controlled interface: property P_{r,h} accepts a truth table f iff some seed e has f(x_i(e))=b_i for all i.
- target-preserving condition: P_{r,h} contains TT(SAT_m) and excludes every truth table computed by SIZE_m(s).

## Assumptions

- The selector x_i(e) is computable and enumerable in poly(N) time when r=O(log N) and h=poly(m).
- SAT labels on m-bit instances are computable in poly(N) time by exhaustive search, so the property is constructive in truth-table input length.
- Usefulness means no size-s m-input circuit has a truth table in P_{r,h}; it is not merely separation from a named finite list.
- Circuit size counts an equality test to a fixed m-bit point as O(m), so h labelled points can be memorized by O(hm) DNF size.

## Equations

- density_union_bound: `\rho(P_{r,h})\le \min\{1,2^{r-h}\},\quad \rho(P_{r,h})\ge 2^{-h}\text{ if nonempty}`. Valid when: Valid when each seed imposes h distinct point labels and P is the union of those agreement cylinders.
- memorizer_size: `\exists g_e\in SIZE_m(C h m)\;\forall i\; g_e(x_i(e))=SAT(x_i(e))`. Valid when: Valid when the target model allows nonuniform DNF circuits with hardwired selected points and labels.
- threshold_conflict: `\text{useful and natural require } h> s/(Cm)\text{ and }h-r\le A m`. Valid when: Applies when usefulness is against SIZE_m(s) and natural largeness means density at least N^{-A}.

## Attempted Derivation

- Define P_{r,h} as the union over all seeds of h-point SAT agreement cylinders; TT(SAT_m) is accepted if at least one valid seed is promised.
- For r=O(log N), enumeration plus brute-force SAT labels gives poly(N)-constructivity; largeness at level N^{-A} forces h-r=O(m).
- For every accepted seed e, build a DNF g_e that outputs 1 on positive labelled points and 0 elsewhere; it matches all h labels and has size O(hm).
- If h<=s/(Cm), TT(g_e) lies in P_{r,h} and in SIZE_m(s), contradicting usefulness; with s=m^k and r=O(m), k>2 has no valid natural-useful regime.

Blocking gap: The derivation covers exact local agreement cylinders, not global algebraic certificates, proof-system soundness predicates, or non-large semantic witnesses.

## Falsifiers

- falsifier: choose h=m^{k-1} and r=O(m); usefulness may survive memorization, but density is at most 2^{-m^{k-1}+O(m)}, so the object is non-large.
- falsifier: take r=Theta(h) to restore density; then seed enumeration is superpolynomial in N unless h=O(m), causing constructivity or advice leakage failure.
- falsifier: a proof-system-specific certificate whose acceptance is not pointwise agreement is outside this lemma and needs a separate soundness-to-lower-bound bridge.
- falsifier: for k=2 constants matter; h=Theta(m) can sit near both thresholds, so the no-go is asymptotic for k>2 unless constants are audited.

## Learning

Cycle 63 adds a seeded-cylinder gate: searchable local SAT witnesses with O(log N) seed length cannot be valid natural useful properties for SIZE_m(m^k), k>2. The obstruction is the exact clash h>m^{k-1}/C versus h=O(m), not generic barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: This branch needs a concrete threshold test for searchable local witnesses rather than another natural-proof slogan.
- Situation seed: For padded SAT_m, let a public seed e select h=m^alpha formula encodings and define P_{r,h} by exact agreement with their SAT labels.
- Varied variable: alpha in h=m^alpha, with seed length fixed at r=c m.
- Held-fixed controls: Target class is nonuniform SIZE_m(m^k) for one fixed k>2., The selector is poly(N)-enumerable and uses no hidden advice., Property acceptance is an existential union of exact SAT-labelled cylinders., SAT labels are computed by exhaustive search in poly(N) time.
- Expected observation: As alpha crosses 1, largeness collapses; as alpha crosses k-1, memorization stops. For k>2 the intervals do not overlap.
- Transfer certificate needed: A formal proof that every accepted cylinder has an O(hm) memorizing circuit and that poly(N)-constructivity really requires enumerating all 2^r seeds.

## Next Experiment

Audit the k=2 borderline: fix DNF size constant C and density exponent A, then determine whether any h=c m window can be both useful against SIZE(m^2) and natural without invoking PRF assumptions.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Generated anti-ball carrier bridge with latency ledger: a kappa-dense, advice-free, low-image family of generated MCSP anti-ball witnesses transfers to an E lower bound with exponent delta<theta/(kappa(1+D)); total generated proof length is harmless, but constant row-bit latency is required for E membership and subthreshold indexed row access is a source falsifier.

## Definitions

- source object: for each source length m, an advice-free deterministic generator G_m canonically emits a distinct row family F_m={T_{m,r}: r<R_m} of N=2^m bit truth tables and at least one generated nonblackbox proof pi_{m,r*} certifying C(T_{m,r*})>2^{theta m}.
- target object: the multiplexed language L_G has finite table H_m(r,x)=T_{m,r}(x) on M_m=m+ceil(log_2 R_m) input bits, padded across kappa-dense source lengths to an all-length E language.
- controlled interface: the only allowed transfer operations are E-uniform distinct-row unranking, sequential or streamed row-bit generation with constant exponential latency, and certificate generation without advice; no nonuniform hard-row selector is used.
- target-preserving condition: theta>0, D=limsup_m log_2 R_m/m is constant, source lengths are computably kappa-dense, row-bit latency is 2^{O(m)}, proof-generation rate is constant when proofs are used as searchable evidence, and the proof is sound for unrestricted nonuniform Boolean circuits.
- C(f) denotes minimum fan-in-two nonuniform Boolean circuit size for the finite truth table f, up to polynomially irrelevant encoding overhead.
- A row decoder is an indexed algorithm or circuit that on input (r,x) outputs T_{m,r}(x) without sequentially regenerating the full row family.

## Assumptions

- Circuit model: unrestricted nonuniform Boolean circuits over a fixed finite basis; all lower bounds are against this model unless explicitly restricted.
- Uniformity regime: G_m, the unranking map, and the padding map are generated by fixed Turing machines with no length advice or hard-row advice.
- Density regime: every target input length n is within a multiplicative kappa+o(1) padding window of some source parameter M_m.
- Soundness regime: the generated proof pi_{m,r*} implies the semantic anti-ball claim C(T_{m,r*})>2^{theta m}; syntactic proof acceptance alone is not enough.
- Entropy regime: duplicate certificates are quotiented before R_m is counted; D measures distinct image entropy, not raw certificate count.
- Latency regime: computing H_m(r,x) may scan a sequential generator for 2^{gamma_bit m+o(m)} steps with gamma_bit=O(1), while any separate indexed row decoder of exponent lambda<theta contradicts source soundness.

## Equations

- image_entropy_and_target_length: `N=2^m,\quad R_m\le 2^{D m+o(m)},\quad M_m=m+\lceil\log_2 R_m\rceil=(1+D+o(1))m`. Valid when: Valid when distinct generated rows are canonically quotiented and D is the limsup image-entropy rate.
- hard_row_forces_multiplexed_hardness: `C(H_m)>2^{\theta m}-O(M_m)=2^{(\theta/(1+D)-o(1))M_m}`. Valid when: Applies when some generated row r* is soundly anti-ball hard and fixing r* in a circuit for H_m costs only O(M_m) gates.
- all_length_padding_transfer: `\forall \delta<\frac{\theta}{\kappa(1+D)}\quad C_{L_G}(n)>2^{\delta n}\text{ for all large padded }n`. Valid when: Requires computable kappa-dense source lengths and padding that preserves uniformity, row rank bits, and circuit-size thresholds.
- E_membership_latency_bound: `T_{L_G}(n)\le 2^{\gamma_{bit}m+o(m)}\le 2^{O(n)}\quad\text{if }\gamma_{bit}=O(1)`. Valid when: Valid when row bits of H_m are produced by an advice-free generator with constant exponential latency and n=Theta(m).
- indexed_access_falsifier: `\text{RowAccess}_{\lambda}\Rightarrow C(T_{m,r})\le 2^{\lambda m+o(m)};\quad \lambda<\theta\text{ falsifies }C(T_{m,r})>2^{\theta m}`. Valid when: Applies when the proposed carrier exposes an indexed row decoder or opening mechanism computing every row bit with subthreshold exponent.

## Attempted Derivation

- Start with source length m and a distinct generated row family F_m of size R_m<=2^{D m+o(m)}; define H_m(r,x)=T_{m,r}(x).
- Use a sound generated anti-ball proof for one row r*: if C(T_{m,r*})>2^{theta m}, then any circuit for H_m of size s yields a circuit for T_{m,r*} of size s+O(M_m) by hardwiring r*.
- Convert the row lower bound into a multiplexed lower bound on M_m=(1+D+o(1))m bits, giving exponent theta/(1+D)-o(1).
- Pad across computably kappa-dense source lengths; circuit lower-bound exponent becomes any delta<theta/(kappa(1+D)).
- Check uniformity: deciding L_G on input (r,x) requires only canonical unranking and row-bit generation. If row-bit latency is 2^{O(m)}, then L_G is in E because n=Theta(m).
- Run the negative tactic: if the proof, locator, or binding mechanism supplies an indexed row decoder with exponent lambda<theta, then the certified row has circuits below the claimed MCSP threshold, so the source proposal is invalid.

Blocking gap: No current construction gives a sparse, generated, advice-free, non-natural anti-ball proof against unrestricted circuits while keeping row-bit latency constant and avoiding subthreshold indexed openings.

## Falsifiers

- falsifier: row-opening or commitment interface computes certified row bits with exponent lambda<theta
- falsifier: proof or row generator has unbounded exponential rate, moving the target language outside E
- falsifier: hard row is chosen by nonuniform advice rather than multiplexed rank bits
- falsifier: proof certifies aggregate or average hardness but no row usable by the multiplexed table
- falsifier: projection repair makes a poly(N)-decidable useful large property while excluding small circuits
- falsifier: black-box transcript verifier queries o(2^{theta m}/m) row positions and can be fooled by sparse easy tables

## Learning

Cycle 63 adds a latency ledger: constant total proof generation is not the decisive issue; the valid transfer needs constant E-time row-bit generation, while any separate indexed row opening below theta is an immediate MCSP-source falsifier. The extraction exponent remains delta<theta/(kappa(1+D)), and the unresolved work is a nonblackbox generated anti-ball source with no advice and no subthreshold openings.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The route now hinges on whether generated proof binding leaks a row decoder. A concrete latency experiment tests the exact distinction between harmless long proof generation and invalid indexed access.
- Situation seed: For each m, imagine a deterministic generated anti-ball MCSP certificate family AB_{theta,D}: it outputs R_m=2^{D m} rows, one sound nonblackbox proof that a row is outside every circuit ball of radius zero at size 2^{theta m}, and a binding commitment supporting row openings.
- Varied variable: lambda_open, the exponent of the fastest indexed opening algorithm x -> T_{m,r}(x) derived from the proof or commitment.
- Held-fixed controls: theta, D, and kappa are fixed constants with theta>0 and D>=0., The generator, unranking, and padding are advice-free and E-uniform., The circuit model remains unrestricted nonuniform Boolean circuits., The proof may be exponentially long but must be generated at a constant exponential rate.
- Expected observation: If lambda_open<theta, the opening algorithm becomes a nonuniform circuit for the certified row and falsifies the source. If lambda_open>=theta while row-bit generation remains 2^{O(m)}, the bridge remains conditionally valid with delta<theta/(kappa(1+D)).
- Transfer certificate needed: A formal opening-to-circuit lemma for the chosen proof system, plus a soundness proof that the generated certificate implies C(T)>2^{theta m} without advice-selected rows or natural-size projections.

## Next Experiment

Instantiate the binding-opening audit for one named proof framework, e.g. an algebraic/PCP-style commitment to truth-table anti-ball constraints, and compute whether its row openings have exponent lambda_open below the claimed theta threshold.
