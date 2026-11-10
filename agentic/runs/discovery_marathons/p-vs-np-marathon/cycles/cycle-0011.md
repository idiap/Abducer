# cycle-0011

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: lookup-lift collapse for restricted target repair

## Candidate Lemma

Lookup-lift collapse lemma. Let Gamma be a nonuniform class containing DNF lookup tables of size 2^{O(m)}poly(m) and closed under formula-style substitution. If H_N has a Gamma-oracle skeleton of size O(N^a), at most N^q SAT oracle leaves, and query length L(N)=(log N)^{o(1)}, then S_Gamma(H_N)<=N^{max(a,q)+o(1)} unconditionally. Hence a claimed source lower bound S_Gamma(H_N)>N^{1+epsilon} with max(a,q)<1+epsilon is invalid in the same regime where generic circuit-to-Gamma unrolling would preserve all fixed P/poly exponents.

## Definitions

- source object: a length-N carrier H_N with a nonuniform Gamma-oracle skeleton of Gamma-size O(N^a), at most N^q oracle leaves, and each oracle leaf querying SAT on at most L(N) bits.
- target object: SAT against arbitrary nonuniform P/poly circuits of size n^c for each fixed c>=1.
- controlled interface: replace every SAT oracle leaf by a Gamma implementation of SAT_{<=L(N)} and account for skeleton size, query multiplicity, and substitution overhead.
- target-preserving condition: for every fixed c>=1, SAT in SIZE(n^c) must imply a Gamma implementation of SAT_{<=L(N)} of size N^{o(1)}, while the same parameter regime must not already give an unconditional Gamma lookup of SAT_{<=L(N)} of size N^{o(1)}.
- Gamma-size S_Gamma means nonuniform size in the same restricted model used for the source lower bound.
- The lemma is a route falsifier, not a separation of P from NP.

## Assumptions

- Gamma contains DNF or decision-tree realizations of arbitrary m-bit predicates with size at most 2^{O(m)}poly(m).
- Gamma permits substituting an implementation for each oracle leaf with total size O(skeleton size plus number of leaves times substituted size).
- a and q are fixed constants and max(a,q)<1+epsilon.
- The intended P/poly-to-Gamma target lift is the generic unrolling of arbitrary circuits on ultra-short SAT queries.

## Equations

- oracle-substitution-bound: `S_{\Gamma}(H_N) \le O(N^a)+N^q T_{\Gamma}(SAT_{\le L(N)})`. Valid when: Valid when the source carrier is represented by a Gamma oracle skeleton and each oracle occurrence is replaced independently.
- lookup-upper-bound: `T_{\Gamma}(SAT_{\le L}) \le 2^{O(L)}\operatorname{poly}(L)`. Valid when: Valid when Gamma contains DNF or decision-tree lookup implementations for every Boolean predicate on L bits.
- ultrashort-collapse: `L(N)=(\log N)^{o(1)} \Rightarrow 2^{O(L(N))}\operatorname{poly}(L(N))=N^{o(1)}`. Valid when: Valid in the ultra-short query regime needed to preserve every fixed target exponent under exponential unrolling.
- source-lower-bound-contradiction: `S_{\Gamma}(H_N) \le N^{\max\{a,q\}+o(1)} < N^{1+\epsilon}`. Valid when: Applies after the threshold assumption max{a,q}<1+epsilon is combined with the lookup substitution bound.

## Attempted Derivation

- Start from the cycle-10 restricted bridge: a Gamma lower bound for H_N magnifies to SAT notin Gamma/poly when H_N has subpolynomial SAT queries and max(a,q)<1+epsilon.
- Try to repair the missing P/poly target by setting Gamma to De Morgan formulas and converting any hypothesized length-L SAT circuit of size L^c into a formula of size 2^{O(L^c)}.
- To preserve every fixed P/poly exponent c, require L(N)^c=o(log N) for every fixed c, hence L(N)=(log N)^{o(1)}.
- In that same regime, SAT_{<=L(N)} has an unconditional DNF lookup of size 2^{O(L(N))}poly(L(N))=N^{o(1)}.
- Substituting this lookup into the Gamma-oracle skeleton gives S_Gamma(H_N)<=N^{max(a,q)+o(1)}, contradicting the desired N^{1+epsilon} source lower bound whenever max(a,q)<1+epsilon.

Blocking gap: The missing bridge is not merely an efficient P/poly-to-Gamma simulation; it must be efficient for SAT-derived query computations while not enabling small lookup for all short query predicates. Generic unrolling cannot satisfy both requirements.

## Falsifiers

- falsifier: ultra-short query lookup gives an unconditional Gamma upper bound below the proposed barely-superlinear source lower bound.
- falsifier: generic circuit unrolling preserves all fixed P/poly exponents only in the same ultra-short regime where lookup collapse is valid.
- falsifier: log-length queries with alpha>=1 avoid N^{o(1)} lookup only by preserving at most c<=1, which is not a meaningful P/poly target for SAT.
- falsifier: any independent oracle-leaf substitution argument remains relativizing and cannot certify the needed nonblackbox target transfer.
- falsifier: Gamma classes lacking DNF lookup also lack the advertised generic P/poly lift unless an explicit nonnatural replacement is proved.

## Learning

Cycle 11 turns the cycle-10 target split into a sharper impossibility triangle. To lift Gamma lower bounds to P/poly by unrolling arbitrary SAT circuits, queries must be so short that every SAT query can also be answered by unconditional lookup inside Gamma. That gives H_N a subthreshold Gamma upper bound and falsifies the source lower bound. Intermediate log-query lengths either collapse the source or preserve only exponent c<=1. Thus black-box formula-style P/poly repair is quarantined; progress now requires a genuinely nonblackbox carrier or a proof object where target circuits are used without independent short-query lookup.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the cycle-10 P/poly target repair.`
- Rationale: The branch needs a concrete threshold test separating a genuine target-preserving lift from another black-box magnification slogan.
- Situation seed: A De Morgan formula carrier H_N with a formula skeleton of size N^a, N^q SAT-oracle leaves, and each leaf querying SAT on L(N)=(log N)^alpha bits; the source claim is FormulaSize(H_N)>N^{1+epsilon}.
- Varied variable: The log-query exponent alpha.
- Held-fixed controls: a and q are fixed with max(a,q)<1+epsilon., The target assumption being contradicted is SAT in nonuniform SIZE(n^c) for arbitrary fixed c>=1., Substitution must use the same Gamma model as the source lower bound., No H_N-specific advice is allowed beyond the hypothesized SAT circuit or the unconditional SAT_{<=L} lookup.
- Expected observation: For alpha<1, SAT_{<=L} lookup has size N^{o(1)} and invalidates the source lower bound. For alpha>=1, formula unrolling preserves only c<1/alpha<=1, so the transfer cannot reach NP not subset P/poly.
- Transfer certificate needed: A nonblackbox certificate showing transfer_tax_Gamma(L,c,N)=N^{o(1)} for all fixed c while arbitrary L-bit lookup remains above the N^{1+epsilon} source threshold; absent this, the repair is not target-preserving.

## Next Experiment

Test a nonblackbox proof-complexity carrier: encode a SAT circuit as a verifier object whose correctness is checked globally rather than by short oracle leaves, and compute whether the verifier overhead stays below N^{1+epsilon} without allowing SAT_{<=L} truth-table substitution.

# Barrier-Aware Lower-Bound Route: Local-Query Naturalization Gate

## Candidate Lemma

If a proposed SAT lower-bound proof is a deterministic or one-sided-perfect-soundness q-query oracle separator for the SAT_n truth table, then it induces a natural property of density at least 2^{-q}. Thus every O(log N)-query black-box truth-table separator is a valid natural-proof object, not a barrier escape.

## Definitions

- source object: a deterministic poly(N)-time oracle verifier V_n which queries an alleged n-bit truth table x in {0,1}^N, N=2^n, at most q(n) adaptive positions.
- target object: the SAT_n truth table f_n and the circuit class SIZE(n^k) on n input bits, for a fixed k.
- controlled interface: map V_n to the property P_n={x in {0,1}^N : V_n^x accepts}, preserving constructivity, largeness, and usefulness against the named circuit class.
- target-preserving condition: V_n accepts f_n and rejects the truth table of every n-input circuit of size at most n^k, with no advice or target-specific hidden string beyond the uniform description of V_n.
- TT(C) denotes the length-N truth table of circuit C.
- A one-sided randomized verifier is allowed only when every random string that accepts f_n still rejects all SIZE(n^k) truth tables.

## Assumptions

- V_n runs in time poly(N), so P_n is constructive in the Razborov-Rudich sense.
- V_n makes q(n) oracle queries to x and accepts f_n.
- For every n-input circuit C of size at most n^k, V_n^{TT(C)} rejects.
- The proof object is black-box in the truth table; it does not inspect an unrelativized SAT machine encoding or proof-system syntax.

## Equations

- truth_table_length: `N=2^n`. Valid when: Valid when the source object is an n-input Boolean function represented by its full truth table.
- accepting_subcube_density: `\Pr_{x\leftarrow\{0,1\}^N}[V_n^x=1]\ge 2^{-q(n)}`. Valid when: Valid when V_n is deterministic, makes at most q adaptive queries, and accepts the target truth table.
- log_query_largeness_threshold: `q(n)\le a\log_2 N \;\Rightarrow\; \mu(P_n)\ge N^{-a}`. Valid when: Applies after the query bound is measured against full truth-table length N and a is fixed.
- usefulness_condition: `P_n\cap\{TT(C): |C|\le n^k\}=\varnothing \quad\text{and}\quad f_n\in P_n`. Valid when: Requires the separator to reject every circuit truth table in the target class while accepting SAT_n.
- prf_distinguisher_advantage: `\mathrm{Adv}_{P_n}(G)\ge \mu(P_n)`. Valid when: Valid when every keyed PRF truth table computed by G has circuit size at most n^k and P_n rejects all such tables.

## Attempted Derivation

- Model the proof object as V_n, a poly(N)-time oracle algorithm on x in {0,1}^N with q adaptive queries.
- Define P_n={x:V_n^x=1}. Constructivity follows from simulating V_n on the full truth table in polynomial time.
- Use target preservation: V_n^{f_n}=1 and V_n rejects TT(C) for every circuit C of size at most n^k; hence P_n is useful against SIZE(n^k) and contains SAT_n.
- Follow the accepting computation path of V_n on f_n. At most q queried positions and their answer bits determine the same path and acceptance.
- All truth tables matching those q answers are accepted, so P_n contains a subcube of density at least 2^{-q}.
- For q<=a log_2 N, this density is at least N^{-a}, giving the largeness threshold required by natural proofs.
- If small PRF truth tables lie inside SIZE(n^k), P_n rejects every PRF output but accepts a random truth table with probability at least N^{-a}; this is a distinguisher.

Blocking gap: The derivation does not cover two-sided randomized acceptance-probability protocols, algebraic protocols, or nonblack-box proofs using SAT syntax rather than truth-table queries.

## Falsifiers

- falsifier: a proposed O(log N)-query deterministic SAT truth-table separator that claims to avoid natural proofs is invalid unless it breaks constructivity or usefulness.
- falsifier: a two-sided randomized one-query equality sampler has exponentially small threshold density, so low query complexity alone is not sufficient for naturalness.
- falsifier: adding nonuniform advice specifying the accepting transcript destroys the controlled interface because the property may no longer be uniformly constructive.
- falsifier: an algebraic extension-field protocol may avoid the subcube-density proof if acceptance is not determined by Boolean truth-table coordinates.

## Learning

Cycle 11 isolates a concrete barrier threshold: deterministic q-query black-box truth-table lower-bound certificates induce natural properties of density at least 2^{-q}. Thus O(log N)-query SAT separators are valid natural-proof objects, while two-sided randomized local protocols require a separate density/usefulness audit. This is route-level progress, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for local black-box lower-bound routes.`
- Rationale: The branch needs a quantitative threshold separating valid natural-proof quarantine from possible non-natural escape; q=O(log N) versus q=omega(log N) supplies that threshold.
- Situation seed: Imagine a family of SAT_n truth-table certificates V_n that queries q positions of the N=2^n-bit SAT truth table and rejects every SIZE(n^k) circuit truth table.
- Varied variable: q(n), swept from constant to a log N to N^{0.01}.
- Held-fixed controls: Target remains SAT_n, not an arbitrary hard function., Usefulness is against the fixed target class SIZE(n^k)., Verifier time remains poly(N) and advice-free., Access to the target is black-box truth-table access only.
- Expected observation: For q<=a log N the induced property has density at least N^{-a} and is a natural-proof object; for q=N^{0.01} the density lower bound becomes 2^{-N^{0.01}}, outside the standard largeness threshold but still requiring an independent usefulness proof.
- Transfer certificate needed: A formal certificate that V_n's accepting set is constructive, contains SAT_n, rejects all SIZE(n^k) truth tables, and does not use hidden advice or nonrelativizing syntax before the intuition can affect proof obligations.

## Next Experiment

Analyze randomized two-sided SAT truth-table protocols: determine whether amplification plus perfect usefulness can recover polynomial density, or whether they form a genuine non-natural but still target-preserving escape class.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Fix constants epsilon>0, kappa>=1, and b,a=O(1). Suppose there are uniform algorithms V_r and G_r such that V_r searches O(r)-bit certificates in time 2^{a r}, G_r streams a 2^r-bit truth table T_{r,c} in time 2^{a r}, accepted certificates exist on a kappa-dense set of lengths, and every accepted c is sound for MCSP threshold 2^{epsilon r}. Then there is L in E with circuit lower bound C(L_ell)>2^{delta ell} for every sufficiently large ell and every delta<epsilon/kappa.

## Definitions

- source object: a uniform searchable streaming MCSP-certificate family (V_r,G_r) with certificates c in {0,1}^{<=b r}, where G_r(c) sequentially emits a truth table on r input bits.
- target object: an E-uniform language L whose length-ell truth table has circuit complexity above 2^{delta ell} for all large ell; this is route-level lower-bound progress, not a proof of P != NP.
- controlled interface: exhaustive uniform search over accepted certificates and source lengths r in [ell/kappa,ell], followed by sequential access to G_r(c) to answer the prefix-indexed bit.
- target-preserving condition: V and G use no advice, accepted lengths are kappa-dense, soundness states true MCSP no-side complexity above 2^{epsilon r}, and the final padding ignores suffix bits without changing uniformity.

## Assumptions

- Completeness: for every sufficiently large target length ell there is a source length r in [ell/kappa,ell] and a certificate c with V_r(c)=1.
- Soundness: V_r(c)=1 implies circuit complexity C(T_{r,c})>2^{epsilon r}.
- Uniformity: V_r and G_r are generated by a single deterministic E-time machine; no nonuniform selector for c or r is used.
- Streaming access is allowed; random access to T_{r,c} by small circuits is not assumed.

## Equations

- source_soundness_threshold: `V_r(c)=1 \Rightarrow C(T_{r,c})>2^{\epsilon r}`. Valid when: Valid when MCSP no-side soundness is a semantic guarantee for every accepted certificate, not merely heuristic evidence.
- density_window: `\forall \ell\gg 1\;\exists r\in[\ell/\kappa,\ell]\;\exists c\in\{0,1\}^{\le br}:V_r(c)=1`. Valid when: Valid when accepted source lengths are kappa-dense and certificates are uniformly searchable in exponential time.
- padding_transfer_threshold: `\delta<\epsilon/\kappa \Rightarrow 2^{\delta \ell}+\mathrm{poly}(\ell)<2^{\epsilon r}`. Valid when: Applies after the reduction preserves length balance with r at least ell over kappa.
- uniform_search_time: `T_L(\ell)\le \sum_{r=\lceil \ell/\kappa\rceil}^{\ell}2^{br}\,2^{ar}+2^{O(r)}=2^{O(\ell)}`. Valid when: Valid when certificate length and verifier overhead remain linear in the source length.

## Attempted Derivation

- For input x of target length ell, enumerate r from ceil(ell/kappa) to ell and all c in {0,1}^{<=br}; run V_r(c) until the first accepted pair is found.
- By kappa-dense completeness, an accepted pair exists for all sufficiently large ell, so the search halts within 2^{O(ell)} time.
- Let L(x) be the bit of T_{r,c} indexed by the first r bits of x; compute it by rerunning the stream G_r(c) until that index appears.
- Assume L_ell has circuits of size 2^{delta ell}. Fix the ell-r ignored suffix bits to constants; this gives a circuit for T_{r,c} of size 2^{delta ell}+poly(ell).
- Since r>=ell/kappa, delta<epsilon/kappa implies 2^{delta ell}+poly(ell)<2^{epsilon r}, contradicting MCSP soundness for the accepted certificate.

Blocking gap: The bridge is valid, but no noncircular construction of such sound searchable streaming certificates is known.

## Falsifiers

- falsifier: accepted certificates have subthreshold random-access bit circuits, yielding small circuits for the certified tables.
- falsifier: accepted source lengths are infinitely often but not kappa-dense, giving only io-E hardness and not the all-length target consequence.
- falsifier: a nonuniform selector or advice string is needed to locate accepted certificates, downgrading the conclusion to an advice-bearing object.
- falsifier: epsilon tends to zero or kappa grows with length, causing the exponent delta<epsilon/kappa to collapse.
- falsifier: soundness is proved through a large constructive property of truth tables, reintroducing the natural-proofs barrier.
- falsifier: G streams only an externally supplied table and does not uniformly determine the bits from the certificate.

## Learning

Cycle 11 removes an unnecessary self-location demand: exhaustive uniform search over O(r)-bit certificates and the kappa-density window already locates a valid stream in E time. The new exact obstruction is random-access leakage: any bit-addressable implementation below exponent epsilon refutes the source soundness. Thus the route's valid core is a sparse, searchable, sequential-only certificate source; constructing its soundness remains the hard non-natural task.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and quantitative transfer test.`
- Rationale: The branch no longer needs another MCSP-hardness slogan; it needs to know whether streaming certificates preserve E-uniform extraction while avoiding the low-locality leakage that killed local expanders.
- Situation seed: For each source length r, an O(r)-bit transcript c is checked by V_r and then streamed by G_r into a 2^r-bit MCSP no-side truth table; target lengths ell use the first accepted r in [ell/kappa,ell] and ignore ell-r suffix bits.
- Varied variable: random-access leakage exponent alpha for a hypothetical circuit R_{r,c}(i) that computes streamed bits from the index and certificate.
- Held-fixed controls: MCSP soundness threshold C(T_{r,c})>2^{epsilon r} with fixed epsilon>0., kappa-dense accepted source lengths with fixed kappa., Uniform exhaustive certificate search in 2^{O(r)} time and no advice., Sequential streaming time 2^{O(r)} for the whole table.
- Expected observation: If alpha<epsilon, the certificate is invalid because hardwiring c gives circuits below the claimed MCSP threshold; if no such random access exists but streaming remains exponential-time uniform, the search-padded E lower-bound transfer stays valid.
- Transfer certificate needed: A formal proof that accepted certificates are sound for all circuits below 2^{epsilon r} and that V,G are uniform, advice-free, kappa-dense, and only sequentially accessible.

## Next Experiment

Audit candidate proof-complexity or algebraic transcripts as V_r certificates: measure certificate length, verifier time, kappa-density, and whether the transcript secretly gives bit-access circuits for the streamed table.
