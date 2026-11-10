# cycle-0012

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Polylog-window nonblackbox bridge: if a carrier H_N has a fixed evaluator that can use an exact SAT circuit of length L(N) as compact advice with overhead N^a poly(|D|), then an i.o. lower bound C(H_N)>N^{1+epsilon} with a<1+epsilon implies SAT notin P/poly, provided L(N)=(log N)^d for some d>1.

## Definitions

- source object: an explicit length-indexed carrier H={H_N} with H_N subseteq {0,1}^N and a claimed i.o. lower bound C(H_N)>N^{1+epsilon} against unrestricted nonuniform Boolean circuits.
- target object: SAT_L on Boolean formulas or circuits of length L, with target consequence SAT notin P/poly, equivalently no fixed c has C(SAT_L)<=L^c eventually.
- controlled interface: a nonblackbox advice-amortized evaluator E_N(x,D) that decides H_N when D is an exact SAT_{L(N)} circuit and whose circuit size is at most N^a poly(|D|,L(N)).
- target-preserving condition: L(N)=N^{o(1)} while full SAT lookup 2^{L(N)} is not subthreshold; D is hardwired only in the conditional upper bound and is not part of the H_N input.

## Assumptions

- There is a computable unbounded length map L(N)=(ceil log N)^d with d>1, or an equivalent schedule N(L)=ceil exp(L^{1/d}).
- For every N and every exact SAT_{L(N)} circuit D, E_N(.,D) computes H_N.
- The evaluator overhead exponent a is fixed and satisfies a<1+epsilon.
- The source lower bound is against unrestricted SIZE circuits, not merely the restricted Gamma model.

## Equations

- conditional_upper: `C(H_N) \leq K N^a |D_{L(N)}|^b L(N)^r`. Valid when: Valid when the evaluator has fixed nonuniform circuits and the only target-dependent advice is an exact SAT circuit D_{L(N)} substituted into it.
- target_amortization: `C(SAT_L) \leq L^c \;\Rightarrow\; C(H_N) \leq K N^a L(N)^{bc+r}=N^{a+o(1)}`. Valid when: Applies when L(N) is subpolynomial in N and c,b,r are fixed constants independent of the carrier length.
- magnification_contrapositive: `(\exists^\infty N)\; C(H_N)>N^{1+\epsilon} \;\Rightarrow\; SAT\notin P/poly`. Valid when: Requires the conditional upper bound for all large N under SAT in P/poly and the strict threshold gap a<1+epsilon.
- lookup_boundary: `N^a2^{L(N)}<N^{1+\epsilon} \text{ if } L(N)<(1+\epsilon-a-o(1))\log_2 N`. Valid when: Valid when the interface can be replaced by a full SAT truth-table lookup rather than a compact nonblackbox target circuit.

## Attempted Derivation

- Fix d>1 and L(N)=(ceil log N)^d. Assume for contradiction SAT in SIZE(n^c) for some fixed c, eventually.
- For each large N choose a correct SAT_{L(N)} circuit D_{L(N)} of size at most L(N)^c. Nonuniformity allows this circuit to be hardwired into the H_N upper-bound circuit.
- Substitute D_{L(N)} into E_N. By the interface bound, C(H_N)<=K N^a L(N)^{bc+r}.
- Since L(N)=N^{o(1)}, for any delta>0 and all large N, L(N)^{bc+r}<=N^delta. Choose delta<(1+epsilon-a).
- Then SAT in SIZE(n^c) implies C(H_N)<=N^{1+epsilon-delta'} for all large N, contradicting an i.o. source lower bound C(H_N)>N^{1+epsilon}.
- Check against the old black-box falsifier: the unconditional lookup implementation has size N^a2^{L(N)}, which is superpolynomial for L=(log N)^d, d>1, so it does not itself refute the source lower bound.

Blocking gap: No explicit carrier H_N and evaluator E_N are yet exhibited whose computation genuinely exploits compact SAT circuits rather than ordinary oracle answers, and no N^{1+epsilon} lower bound for such an H_N is known.

## Falsifiers

- falsifier: logarithmic L(N) permits full SAT truth-table substitution of size below N^{1+epsilon}, collapsing the carrier lower bound unconditionally.
- falsifier: if the target circuit D is part of the input, then input-reading or nonuniform leakage reintroduces the positive target-size exponent and destroys all-exponent transfer.
- falsifier: if E_N is merely a black-box SAT-query algorithm, superlogarithmic L blocks lookup but gives no reason that compact SAT circuits can be used without duplicating queries above threshold.
- falsifier: if the source lower bound is only for formulas, AC0, or another Gamma not containing the substituted evaluator, the conclusion is only SAT notin Gamma/poly, not NP notin P/poly.

## Learning

Cycle 12 identifies a real surviving window: superlogarithmic subpolynomial target lengths, especially L=(log N)^d with d>1. In this window SAT circuits of size L^c amortize to N^{o(1)}, but SAT truth tables cost 2^L and no longer give the old subthreshold lookup falsifier. The bridge is valid only for nonblackbox compact-circuit consumers; it is not a P vs NP proof without the explicit carrier and lower bound.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and bridge calibration experiment.`
- Rationale: The branch has quarantined black-box lookup and formula-unrolling repairs; the remaining live route needs a concrete superlogarithmic but subpolynomial length window where compact target circuits are cheap and full truth tables are expensive.
- Situation seed: Let L(N)=(log N)^d and imagine a carrier H_N whose evaluator E_N takes x in {0,1}^N and a hardwired exact SAT_L circuit D_L, then checks a poly(N)-size local consistency predicate generated by a Cook-Levin self-reduction whose only semantic oracle is D_L.
- Varied variable: The exponent d in the polylogarithmic target length L(N)=(log N)^d.
- Held-fixed controls: Source threshold C(H_N)>N^{1+epsilon} against unrestricted nonuniform circuits., Evaluator overhead N^a poly(|D_L|,L) with fixed a<1+epsilon., Target assumption SAT in SIZE(L^c) for an arbitrary fixed c., D_L is advice in the conditional upper bound and is not encoded in the H_N input.
- Expected observation: For d<=1 the truth table 2^L may be subthreshold and is a falsifier; for every fixed d>1, L^c=N^{o(1)} preserves the target transfer while 2^L is superpolynomial, isolating the compact-circuit/nonblackbox advantage.
- Transfer certificate needed: A formal evaluator certificate showing E_N(.,D_L)=H_N for every exact SAT_L circuit, size N^a poly(|D_L|), uniform length coverage N(L), and no alternative unconditional table-based implementation below N^{1+epsilon}.

## Next Experiment

Instantiate H_N as a proof-checking or self-reduction transcript language whose verifier can call a compact SAT_L circuit nonblackbox; compute its exact overhead a and test whether full truth-table substitution or input-encoded D leakage gives a subthreshold upper bound.

# Barrier-Aware Lower-Bound Route: randomized local naturalization threshold

## Candidate Lemma

A two-sided randomized q-query truth-table separator naturalizes only after a seed-majority conversion whose query cost is q times the circuit-counting seed cost; the natural-proof largeness threshold is q gamma^{-2} s log s = O(log N), not merely q=O(log N).

## Definitions

- source object: randomized q-query oracle truth-table separator A_n for a target truth table K_n in {0,1}^N, with completeness c, soundness a, gap gamma=c-a>0, and target class H_{s,n}=SIZE(s(n)) truth tables.
- target object: Razborov-Rudich-style natural property P_n computable in poly(N), useful against H_{s,n}, and large with density at least N^{-O(1)} under the uniform distribution on {0,1}^N.
- controlled interface: seed-majority derandomization of A_n into a deterministic decision tree D_{B,n} using t fixed random seeds and at most Q=t q oracle queries.
- target-preserving condition: the fixed seed multiset B_n must preserve acceptance of K_n and rejection of every h in H_{s,n}, while being explicit or safely hardwired within the constructivity model.
- N=2^n is the truth-table length; s is measured as circuit size on n input bits; |H_{s,n}| <= 2^{O(s log s)}.

## Assumptions

- For every h in H_{s,n}, Pr_r[A_n^h(r)=1] <= a, and Pr_r[A_n^{K_n}(r)=1] >= c.
- Random seeds used in B are independent, and the gap gamma is at least inverse-polynomially describable.
- A_n is poly(N)-time after oracle answers and the chosen seed are supplied.
- The seed multiset B_n is explicit in poly(N) time, or the route states a nonuniform-natural model and pays for advice leakage.

## Equations

- seed_count: `t \ge C\gamma^{-2}(s(n)\log s(n)+\log(1/\eta))`. Valid when: Valid when independent random seeds are sampled and the union bound ranges over all size-s circuits.
- query_blowup: `Q(n)=t\,q(n)`. Valid when: Valid when the deterministic simulation runs the same q-query oracle procedure on each selected seed.
- deterministic_path_density: `\mu(P_{B,n})\ge 2^{-Q(n)}`. Valid when: Valid when D_B accepts K_n, since the accepting adaptive path fixes at most Q truth-table coordinates.
- natural_largeness_gate: `q(n)\gamma^{-2}s(n)\log s(n)=O(\log N)=O(n)`. Valid when: Valid when inverse-polynomial largeness is required for a natural property over N-bit truth tables.

## Attempted Derivation

- Start with a two-sided randomized q-query separator A_n for K_n versus SIZE(s).
- Try to define the threshold property P_theta={x: Pr_r[A_n^x(r)=1] >= theta}. This is useful when a<theta<c.
- Completeness puts K_n in P_theta, but gives no lower bound on mu(P_theta) over random truth tables.
- The q=1 coordinate-sampling construction around an average-case-hard K_n makes P_theta an exponentially small Hamming ball, giving a concrete falsifier to automatic largeness.
- Repair by fixing t random seeds and using majority. Chernoff plus a union bound over 2^{O(s log s)} circuits gives a target-preserving deterministic separator.
- Apply deterministic decision-tree naturalization to the fixed-seed separator. The density lower bound becomes 2^{-tq}, so inverse-polynomial largeness requires q gamma^{-2} s log s=O(log N).

Blocking gap: There is no general density lower bound for the two-sided threshold property P_theta; seed elimination preserves usefulness only at the cost t=Theta(gamma^{-2}s log s), which usually destroys largeness for s=n^k.

## Falsifiers

- q=1 coordinate sampling around an average-case-hard target gives a valid randomized separator whose threshold property is exponentially small, so small q alone is not a natural-proof trigger.
- For s(n)=n^k and constant gamma, seed-majority gives Q=Omega(q n^k log n); even q=1 fails inverse-polynomial largeness for every k>=1.
- A nonexplicit seed multiset B_n preserves soundness nonconstructively but leaks advice into the property, invalidating a uniform natural-proof transfer.
- Perfect-soundness protocols are not a counterexample: they naturalize by P_exists and therefore fall back under the deterministic q=O(log N) audit.

## Learning

Cycle 12 refines the natural-proof barrier for randomized local certificates. Deterministic q-query certificates naturalize at q=O(log N), but two-sided randomized certificates require seed elimination over all small circuits, causing a q s log s blowup. A q=1 Hamming-ball separator is a concrete falsifier to automatic randomized naturalization. This is valid route-level progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The previous cycle left two-sided randomized local protocols unaudited. A concrete coordinate-sampling case tests whether randomized q=1 certificates force largeness or can remain outside the natural-proof barrier for a quantitative reason.
- Situation seed: For each n, let K_n be the SAT truth table on n-bit encodings, padded so K_n(i) is decidable in time poly(N). Assume hypothetically that dist(K_n,SIZE(n^k))>=delta N. The verifier chooses a uniform coordinate i and accepts candidate truth table x iff x_i=K_n(i).
- Varied variable: The relative distance delta in (1/2,1), equivalently the threshold theta chosen between 1-delta and 1.
- Held-fixed controls: N=2^n and constructivity time poly(N)., Target class remains SIZE(n^k) on n-bit inputs., Oracle query budget is fixed at q=1., No nonuniform advice is allowed in the property beyond the target-preserving bit computation K_n(i).
- Expected observation: For every theta>1/2 the accepted threshold property is a Hamming ball of density 2^{-Theta(N)}, while soundness against SIZE(n^k) follows from the distance premise. Thus randomized locality and usefulness coexist with non-largeness.
- Transfer certificate needed: Before this intuition affects proof obligations, the route must supply either a direct inverse-polynomial density proof for its actual P_theta, or an explicit seed-majority conversion with tq=O(log N), or seedwise perfect soundness.

## Next Experiment

Audit an MCSP-based randomized local certificate under the same gate: compute q, gamma, s, seed length, and whether its threshold property has direct density or only seed-majority density.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Linear-budget sequential MCSP certificates transfer to all-length E lower bounds; the certificate-search overhead affects only E-uniformity, while the lower-bound exponent loses only the source-length gap kappa.

## Definitions

- source object: A uniform relation V_m(c) with |c|<=sigma m+O(1) that, on acceptance within 2^{tau m+O(1)} time, emits a 2^m-bit truth table T_m with circuit complexity C(T_m)>2^{epsilon m}.
- target object: A deterministic E language L whose length-n slice is a padded copy of the lexicographically first accepted T_m for a source length m in [n/kappa-O(1),n].
- controlled interface: Exhaustively search all O(m)-bit certificates, choose the first accepting stream, and answer the requested padded coordinate by one sequential scan; no bit-address oracle or advice selector is used.
- target-preserving condition: The source lengths are kappa-dense with constant kappa, epsilon>0 is constant, sigma and tau are constants, and every accepted certificate is sound on the MCSP no-side threshold.
- Circuit model C is fixed before the source is stated; changing C during extraction is invalid.
- Completeness supplies at least one accepting certificate on every source length used by the density selector.

## Assumptions

- V and the selector m(n) are uniform and use no nonuniform advice.
- The padding map allows a circuit for L_n to be restricted to a circuit for T_m by fixing n-m prefix bits.
- All accepted streams are high-complexity; soundness is universal over certificates, not just over the first accepted one.
- The verifier emits a stream sequentially; random access is not part of the source interface.

## Equations

- MCSP-no-side threshold: `K_m=2^{\epsilon m},\qquad C(T_m)>K_m.`. Valid when: Valid when the source relation accepts only truth tables on m variables and soundness is measured against the named circuit model C.
- exhaustive-search time: `T_{search}(m)\le 2^{\sigma m+O(1)}\cdot 2^{\tau m+O(1)}=2^{(\sigma+\tau)m+O(1)}.`. Valid when: Valid when certificate length and single-certificate streaming verification have constant linear exponents and enumeration is deterministic.
- density window: `\forall n\gg1\;\exists m\in S:\quad n/\kappa-O(1)\le m\le n.`. Valid when: Valid when the source-length set is constant-gap dense rather than merely infinite or externally selected by advice.
- target lower-bound transfer: `\operatorname{Size}(L_n)>2^{\delta n}\quad\text{for every constant }\delta<\epsilon/\kappa.`. Valid when: Applies after padding preserves restrictions and a circuit for L_n yields a circuit for the selected T_m by fixing prefix bits.
- budget collapse boundary: `|c(m)|=\omega(m)\Rightarrow T_{search}(m)=2^{\omega(m)}\notin 2^{O(n)}\text{ for }n=\Theta(m).`. Valid when: Valid when the target class is E with all-length inputs and the density gap kappa remains a fixed constant.

## Attempted Derivation

- Fix target length n and choose a source length m in S with n/kappa-O(1)<=m<=n.
- Enumerate all certificates c of length at most sigma m+O(1), run V_m(c), and select the lexicographically first accepting stream.
- Define L_n by padding this selected T_m; on input of length n, scan the stream until the corresponding m-bit coordinate is reached.
- The uniform running time is at most 2^{(sigma+tau)m+O(1)}<=2^{O(n)}, hence L is in E under constant kappa.
- Assume L_n has circuits of size 2^{delta n}; fixing the padding prefix gives circuits for T_m of size 2^{delta n}+poly(n).
- Since n<=kappa m+O(1), this is at most 2^{delta kappa m+o(m)}, contradicting C(T_m)>2^{epsilon m} when delta<epsilon/kappa.
- Thus the extraction theorem is valid conditional on completeness and soundness of the sequential certificate source; sigma and tau do not reduce the lower-bound exponent.

Blocking gap: No non-circular construction of V_m is known with O(m)-bit certificates, 2^{O(m)} sequential verification, kappa-dense completeness, and universal MCSP no-side soundness.

## Falsifiers

- falsifier: an accepted stream has bit-address circuits or generators of size 2^{alpha m} for alpha<epsilon, contradicting the claimed MCSP no-side threshold.
- falsifier: certificate length omega(m) with constant kappa forces exhaustive search time 2^{omega(m)}, so the target language is not certified to be in E.
- falsifier: source lengths are only infinitely often or chosen with advice; the all-length padding transfer and exponent delta<epsilon/kappa are invalid.
- falsifier: the verifier checks a dense externally supplied property of truth tables; this reenters the natural-proofs obstruction rather than producing a sparse carrier.
- falsifier: soundness is obtained by brute-force enumeration of circuits of size 2^{epsilon m}; the verification time becomes 2^{2^{epsilon m}poly(m)}, far above E.
- falsifier: the accepting certificate is selected nonuniformly; the consequence becomes an E/advice or nonuniform object, not the target E language.

## Learning

Cycle 12 sharpens the valid transfer into a budget theorem: O(m)-bit sequential certificates and 2^{O(m)} verification are exactly compatible with E extraction at constant density, while omega(m)-bit certificates or subthreshold random access are formal falsifiers. The bridge is route-level progress only; constructing a sparse, sound, non-natural MCSP certificate source is still the hard task.

## Gedanken Experiment Design Seed

- Need decision: `design now`
- Rationale: The bridge theorem is already conditionally valid; the remaining quantitative uncertainty is the exact certificate-budget boundary compatible with E-uniform extraction and no random-access leakage.
- Situation seed: Padded MCSP-certificate family: for each kappa-dense source length m, a verifier V_m(c) emits a 2^m-bit no-side table, and L_n pads the lexicographically first accepted table for some m in [n/kappa,n].
- Varied variable: certificate-length exponent beta in |c|=m^beta, with verifier streaming time fixed at 2^{tau m}.
- Held-fixed controls: MCSP threshold K_m=2^{epsilon m} and fixed circuit model C., Constant source gap kappa and deterministic lexicographic exhaustive search., Sequential-only emission; no random-access bit oracle and no advice selector., Padding restriction that recovers T_m from L_n by fixing prefix bits.
- Expected observation: beta=1 is the E boundary: beta<=1 preserves target membership and delta<epsilon/kappa, while beta>1 gives search time 2^{m^beta} for n=Theta(m) and collapses the transfer before any lower-bound consequence.
- Transfer certificate needed: A uniform proof that every accepted stream has C(T_m)>2^{epsilon m}, plus an audit that the proof is non-large and provides no subthreshold random-access implementation.

## Next Experiment

Instantiate V_m from a proof-complexity transcript for MCSP no-instances and audit whether transcript checking is linear-budget sequential-only or secretly dense, random-access, or advice-dependent.
