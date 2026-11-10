# cycle-0010

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Let Gamma be a nonuniform circuit class closed under projections, Boolean substitution, and fan-in composition with at most constant-factor or polylogarithmic size loss. If a carrier H_N has Gamma-oracle circuits of internal size N^a making at most N^q queries to SAT instances of length L(N), then a source lower bound S_Gamma(H_N)>N^{1+epsilon} transfers to SAT notin Gamma[n^c] exactly in the threshold regime a<1+epsilon and q+log_N(L(N)^c)<1+epsilon. For L(N)=N^{o(1)}, this excludes every fixed c, but only for the restricted target Gamma/poly, not for P/poly unless Gamma can simulate the target circuits.

## Definitions

- source object: the length-N carrier family H={H_N} with source lower-bound model GammaSIZE and threshold S_Gamma(H_N)>N^{1+epsilon}.
- target object: SAT_{<=n} against Gamma-circuits of size n^c, yielding the route-level target consequence SAT notin Gamma/poly when all fixed c are excluded.
- controlled interface: a Gamma-oracle implementation A_N for H_N with internal size N^a, at most N^q SAT queries, and query length L(N).
- target-preserving condition: the target class must be the same Gamma under substitution, or else a separate nonuniform lift from the intended target circuits into Gamma must be proved with subthreshold overhead.

## Assumptions

- Gamma is closed under substituting Gamma-circuits for oracle gates without increasing the exponent beyond the displayed additive query term.
- The oracle algorithm A_N is nonuniformly Gamma-realizable, including query generation and final aggregation.
- The lower bound S_Gamma(H_N)>N^{1+epsilon} holds for all sufficiently large valid input lengths N, not merely off the carrier's promise.
- The target statement is restricted to Gamma/poly unless a P/poly-to-Gamma lift is supplied.

## Equations

- substitution_upper_bound: `S_{\Gamma}(H_N) \le \widetilde O\bigl(N^a+N^q\,S_{\Gamma}(SAT_{\le L(N)})\bigr)`. Valid when: Valid when Gamma is explicitly closed under oracle-gate substitution and query-generation circuits are counted.
- polynomial_query_length_transfer: `L(N)=N^{\beta},\ S_{\Gamma}(SAT_n)\le n^c\ \Longrightarrow\ S_{\Gamma}(H_N)\le N^{\max\{a,q+\beta c\}+o(1)}`. Valid when: Applies when query lengths have fixed polynomial exponent beta and c is fixed.
- finite_exponent_exclusion: `S_{\Gamma}(H_N)>N^{1+\epsilon}\ \Longrightarrow\ SAT\notin \Gamma[n^c]\quad \text{for } c<(1+\epsilon-q)/\beta \text{ and } a<1+\epsilon`. Valid when: Requires positive beta and compares the transferred exponent with the source threshold.
- subpolynomial_query_magnification: `L(N)=N^{o(1)},\ \max\{a,q\}<1+\epsilon\ \Longrightarrow\ SAT\notin \Gamma[n^c]\text{ for every fixed }c`. Valid when: Valid when the o(1) term is uniform for each fixed target exponent c.

## Attempted Derivation

- Fix Gamma and an oracle Gamma-circuit A_N for H_N with N^a internal gates and at most N^q SAT queries of length at most L(N).
- Assume the restricted target negation: SAT_{<=n} has Gamma-circuits of size n^c for all large n.
- Replace each SAT oracle gate in A_N by the corresponding Gamma-circuit for SAT_{<=L(N)} and use Gamma substitution closure.
- Obtain S_Gamma(H_N)<=tilde O(N^a+N^q L(N)^c).
- For L=N^beta, compare the exponent max(a,q+beta c) with 1+epsilon to exclude only c below (1+epsilon-q)/beta.
- For L=N^{o(1)}, obtain S_Gamma(H_N)<=N^{max(a,q)+o(1)} for each fixed c, contradicting the source bound if max(a,q)<1+epsilon.
- Attempt to replace the restricted target assumption SAT in Gamma/poly by SAT in P/poly. This requires converting arbitrary SAT circuits into Gamma-circuits on the queried lengths.
- No such conversion follows from the interface. Therefore the valid conclusion is Gamma/poly separation, while the P/poly consequence remains unproved.

Blocking gap: The target-preserving lift from arbitrary P/poly SAT circuits to Gamma-circuits is absent; without it, restricted-source magnification leaks the target model.

## Falsifiers

- falsifier: if beta>0, the transfer excludes only c<(1+epsilon-q)/beta, so all-exponent magnification collapses.
- falsifier: if max(a,q)>=1+epsilon, even subpolynomial SAT queries do not beat the source threshold.
- falsifier: if Gamma is weaker than P/poly and no P/poly-to-Gamma lift is valid, the target class silently changes to Gamma/poly.
- falsifier: a natural-proof style dense useful property computable in Gamma/poly would not be a credible P/poly route under standard pseudorandom-function assumptions; it must be non-natural or outside that barrier's scope.

## Learning

Cycle 10 proves a valid restricted-model closure bridge and names the precise target-preservation failure. Subpolynomial queries plus max(a,q)<1+epsilon magnify a Gamma lower bound to SAT notin Gamma/poly for every fixed exponent. This is real route-level progress, but it is not NP notin P/poly: the missing object is a nonuniform P/poly-to-Gamma lift with subthreshold tax, and its absence is the decisive falsifier for advertising the bridge as a P vs NP route.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Test a non-natural nonblackbox carrier whose query length is N^{o(1)} and whose use of a SAT circuit is semantic rather than oracle substitution; compute whether its lift tax delta is below the source slack epsilon.

# Barrier-Aware Lower-Bound Route, cycle 10: Hamming thickening audit

## Candidate Lemma

For the SAT_n truth-table Hamming-ball property P_{N,r}, constructivity is easy, but natural largeness appears only when r/N is within Theta(sqrt(log N/N)) of 1/2. At that threshold, target-preserving usefulness is an average-case lower bound saying every n^k-size circuit has SAT agreement at most 1/2+Theta(sqrt(log N/N)). Thus a singleton-SAT route escapes natural proofs by non-largeness, while any polynomially large thickening re-enters the natural-proof barrier under matching PRFs.

## Definitions

- source object: the uniform truth-table property P_{N,r} centered at T_n=TT(SAT_n), where N=2^n and P_{N,r}(x)=1 iff the Hamming distance Delta(x,T_n) is at most r.
- target object: nonuniform lower bounds for the length-n SAT slice against SIZE(n^k), with the strengthened average-case target measured under the uniform distribution on n-bit encodings.
- controlled interface: a poly(N)-time truth-table test whose acceptance set is a Hamming ball around SAT_n and whose rejection of small-circuit truth tables is used as the lower-bound certificate.
- target-preserving condition: for every n-input circuit C of size n^k, TT(C) must be outside P_{N,r}; equivalently C must err on more than r of the N inputs, so exact lower bounds are preserved only through this rejection condition.
- largeness parameter: the Razborov-Rudich audit uses density at least N^{-a} for a fixed a>0 against poly(N)-time distinguishers.
- barrier scope: the obstruction is valid only when the useful property is constructive, polynomially large, and the assumed PRFs are computable inside the same target circuit scale n^k or below.

## Assumptions

- SAT_n is encoded so that each length-n instance can be solved by exhaustive search in 2^{O(n)} time.
- The property is evaluated on a complete N-bit truth table, so poly(N) time equals 2^{O(n)} time.
- The circuit target is nonuniform SIZE(n^k) over n input bits; no uniform P-machine conclusion is inferred.
- The natural-proof barrier is invoked only under a matching PRF hypothesis secure against poly(N)-time truth-table tests with noticeable N^{-a} advantage.

## Equations

- hamming_ball_density: `P_{N,r}(x)=1 \iff \Delta(x,T_n)\le r,\quad \mu(P_{N,r})=2^{-N}\sum_{i=0}^{r}{N\choose i}`. Valid when: Valid when P_{N,r} is measured under the uniform distribution on all N-bit truth tables.
- entropy_asymptotic: `r=\delta N,\ 0\le \delta\le 1/2 \quad\Rightarrow\quad \log_2 \mu(P_{N,r})=-N(1-H(\delta))+O(\log N)`. Valid when: Valid when r is an integral Hamming radius and the binary entropy estimate applies uniformly below one half.
- polynomial_largeness_threshold: `\mu(P_{N,r})\ge N^{-a}\quad\Rightarrow\quad 1-H(\delta)\le {a\log_2 N+O(\log N)\over N}`. Valid when: Valid when the Razborov-Rudich largeness requirement is the polynomial density bound N^{-a}.
- near_half_radius: `\delta=1/2-\varepsilon,\quad 1-H(\delta)={2\over \ln 2}\varepsilon^2+O(\varepsilon^4),\quad \varepsilon=O\left(\sqrt{\log N/N}\right)`. Valid when: Valid when the thickening radius is close enough to N/2 for the entropy Taylor expansion.
- usefulness_equals_average_case_lb: `P_{N,r}\cap TT(SIZE(n^k))=\varnothing \iff \forall C\in SIZE(n^k),\ \Pr_x[C(x)=SAT_n(x)]<1-r/N`. Valid when: Valid when target circuits are n-input nonuniform circuits compared on every n-bit string.
- truth_table_constructivity: `\mathrm{Time}(x\mapsto P_{N,r}(x))\le N\cdot 2^{O(n)}=N^{O(1)}`. Valid when: Valid when SAT on length-n formulas is solved by exhaustive search while reading an N-bit table.

## Attempted Derivation

- Define T_n=TT(SAT_n) and P_{N,r}={x in {0,1}^N : Delta(x,T_n)<=r}.
- Compute constructivity: generate each SAT_n bit by exhaustive search in 2^{O(n)} time and compare N bits, giving N^{O(1)} truth-table time.
- Compute density exactly as a Hamming-ball volume divided by 2^N.
- Apply the entropy estimate to obtain mu(P_{N,delta N})=2^{-N(1-H(delta))+O(log N)} for delta<=1/2.
- Impose RR largeness mu>=N^{-a}; this forces 1-H(delta)<=O(log N/N), hence delta=1/2-O(sqrt(log N/N)).
- Translate usefulness into circuit error: every n^k-size circuit must be farther than r from SAT_n, so its agreement is below 1-r/N.
- At the large-property threshold this becomes agreement at most 1/2+O(sqrt(log N/N)), a near-random average-case lower bound, not a mere worst-case lower bound.

Blocking gap: The entropy and constructivity calculations are valid, but the missing lower-bound step is proving usefulness of P_{N,r}; at polynomial density that usefulness is exactly the kind of natural property contradicted by matching PRFs.

## Falsifiers

- falsifier: a claimed large Hamming-thickened SAT property with poly(N) constructivity and usefulness against SIZE(n^k) contradicts the matching PRF hypothesis, so the route must reject that hypothesis or lose validity.
- falsifier: if the distribution is not uniform over full n-bit truth tables, the Hamming-ball entropy threshold no longer certifies natural largeness.
- falsifier: if PRF implementations require size n^b with b>k, the natural-proof barrier is not valid at exponent k and the audit must record only limited scope.
- falsifier: if the proof of usefulness relativizes uniformly to SAT^O, a BGS oracle with P^O=NP^O blocks target preservation.
- falsifier: if the route infers lower bounds from the small density of the SAT singleton alone, it is circular counting and proves no rejection of small circuits.

## Learning

Cycle 10 isolates the exact point where a SAT-specific constructive certificate becomes natural: Hamming thickening must reach radius N/2-O(sqrt(N log N)) to have polynomial density, and usefulness then asserts near-random average-case SAT hardness against SIZE(n^k). This is valid route-level progress and a falsifier for both overbroad natural-proof quarantine and naive thickening-as-lower-bound claims.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Audit whether a non-large SAT-specific property of intermediate density 2^{-N^alpha} can support a nonrelativizing usefulness proof, or whether all known constructions either collapse to singleton circularity or thicken into the RR-large average-case regime.

# MCSP / Meta-Complexity Carrier Transfer: self-locating streaming certificates

## Candidate Lemma

A self-locating streaming MCSP certificate-expander with kappa-dense accepted lengths yields a valid route-level E circuit lower bound: for every delta<epsilon/kappa, some L in E has C(L_n)>2^{delta n} for all sufficiently large n. The same bridge is invalid for bitwise-local expanders of exponent lambda<epsilon, because locality itself gives small circuits for the certified truth tables.

## Definitions

- source object: a deterministic E-uniform streaming pair (G,V) where G(m,z) prints a truth table Y_{m,z} in {0,1}^{2^m}, |z|<=b m, and V(m,z,c) runs in 2^{tau m} with |c|<=a m; acceptance is a sound certificate that C(Y_{m,z})>2^{epsilon m}.
- target object: a uniform language L in E=DTIME(2^{O(n)}) with all-sufficient-length Boolean circuit lower bound C(L_n)>2^{delta n} against unrestricted fan-in-two circuits.
- controlled interface: on input x of length n, uniformly enumerate all r<=n and all (z,c) of linear length, choose the largest accepted r, stream G(r,z) up to the index given by the first r bits of x, and ignore the remaining n-r bits.
- target-preserving condition: accepted source lengths are kappa-dense, i.e. every large n has an accepted r in [n/kappa,n], acceptance is sound for threshold 2^{epsilon r}, and the generator is not replaced by a random-access local map of circuit exponent below epsilon.
- self-location: the length r and seed z are found by the E computation itself, not supplied by advice or an external witness locator.
- barrier posture: the accepted range may be exponentially sparse among truth tables, so the bridge is outside the largeness requirement of natural proofs; dense constructive variants remain a natural-proofs falsifier.

## Assumptions

- Constants a,b,tau,sigma,kappa are fixed and independent of m.
- For every accepted (m,z,c), V is sound: C(Y_{m,z})>2^{epsilon m}.
- For every sufficiently large n, some accepted source length r lies in [n/kappa,n].
- G is streaming-output explicit in time 2^{sigma m}; no promise of poly(m)-size random access to bits is used.
- Circuit size C(.) is nonuniform Boolean circuit size for the length-indexed truth table.

## Equations

- mcsp_threshold: `C(Y_{m,z})>2^{\epsilon m}=N^{\epsilon}\quad(N=2^m)`. Valid when: Applies when Y_m has N=2^m bits and the MCSP threshold is the fixed polynomial N^epsilon with 0<epsilon<1.
- kappa_density: `\forall n\ge n_0\;\exists m\in[n/\kappa,n]\;\exists z,c\; V(m,z,c)=1`. Valid when: Applies after accepted source lengths are uniformly enumerable and have multiplicative gaps at most kappa.
- search_runtime: `T_L(n)\le \sum_{r\le n}2^{(a+b+\tau+O(1))r}+2^{\sigma n}=2^{O(n)}`. Valid when: Valid when seed length, certificate length, verification time, and streaming generation exponent are all fixed constants.
- padding_projection_transfer: `C(L_n)\ge C(Y_{m,z})-O(n)>2^{\epsilon m}-O(n)>2^{\delta n}\quad(\delta<\epsilon/\kappa)`. Valid when: Requires choosing an accepted m between n/kappa and n so any circuit for L_n restricts to a circuit for Y_m.
- locality_collapse_boundary: `C(Y_{m,z})\le 2^{\lambda m}+O(m)\;\bot\; C(Y_{m,z})>2^{\epsilon m}\quad(\lambda<\epsilon-o(1))`. Valid when: Applies when the proposed expander has bitwise random access computable by circuits of exponent lambda after hardwiring the seed.

## Attempted Derivation

- Assume a sound streaming certificate-expander with constants epsilon,kappa,a,b,tau,sigma and kappa-dense accepted lengths.
- Define L on inputs x of length n by enumerating all r<=n and all linear-size pairs (z,c), running V(r,z,c), and selecting the largest accepted r with a fixed lexicographic tie-breaker.
- Let Y=G(r,z). Output the bit of Y indexed by the first r bits of x, obtained by streaming G until that position. The search and streaming cost is 2^{O(n)}, so L is in E.
- For every large n, density gives selected r>=n/kappa. If a circuit D_n of size s computes L_n, hardwire the ignored suffix bits to obtain a circuit for Y of size s+O(n).
- Soundness gives s+O(n)>=C(Y)>2^{epsilon r}>=2^{epsilon n/kappa}. Hence for any delta<epsilon/kappa and large n, C(L_n)>2^{delta n}.
- Audit the expander interface: if the construction instead gives bitwise LocG circuits of size 2^{lambda r} with lambda<epsilon, then hardwiring z yields C(Y)<=2^{lambda r}+O(r), contradicting soundness.

Blocking gap: The bridge is valid, but it does not construct the source. The remaining gap is a sparse, non-natural, self-locating, streaming verifier whose soundness proves high MCSP without already encoding an E lower bound or providing subthreshold random access.

## Falsifiers

- falsifier: carrier is not explicit enough for the E machine to find the accepted length and seed.
- falsifier: extraction loses the needed class because the chosen table is supplied by advice.
- falsifier: consequence is only nonuniform, namely a dense sequence of hard tables rather than one L in E.
- falsifier: a proposed certificate-expander is bitwise-local with circuit exponent lambda<epsilon, causing MCSP threshold collapse.
- falsifier: verifier accepts a dense polynomial-time decidable property of truth tables excluding small circuits, triggering the natural-proofs obstruction under standard PRF assumptions.
- falsifier: accepted lengths have superconstant multiplicative gaps, reducing epsilon/kappa to zero and destroying the target exponent.

## Learning

Cycle 10 adds a concrete interface theorem and a new obstruction. The valid bridge uses self-locating streaming certificates and transfers threshold 2^{epsilon m} on kappa-dense source lengths to E lower bound exponent any delta<epsilon/kappa. The hidden falsifier is subthreshold random access: a locally computable expander would itself give small circuits for the certified tables. Thus future source attempts must be sparse, non-natural, uniform, streaming, and sound without low-locality or advice.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Audit proof-complexity carriers: can short IPS/Frege-style certificates soundly certify C(Y)>2^{epsilon m} for a streaming-generated sparse range without yielding a subthreshold locator or a dense natural property?
