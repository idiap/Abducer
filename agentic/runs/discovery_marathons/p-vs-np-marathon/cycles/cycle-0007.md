# cycle-0007

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: black-box substitution cap

## Candidate Lemma

Let L_N be an N-bit carrier with nonuniform lower bound SIZE(L_N)>N^{1+epsilon} on infinitely many valid lengths. If L has an oracle-circuit reduction to SAT using N^{a+o(1)} non-oracle size, N^{q+o(1)} SAT queries, and maximum query length N^{beta+o(1)}, then the bridge excludes only SAT circuits of exponent c with a<1+epsilon and q+beta c<1+epsilon. Thus any fixed beta>0 gives a finite exponent window, not NP not subset P/poly.

## Definitions

- source object: a length-indexed Boolean carrier L_N subset {0,1}^N with lower bound against nonuniform Boolean circuits of size N^{1+epsilon} on the stated valid lengths.
- target object: SAT_m with target consequence SAT notin SIZE(m^c); exclusion for every fixed c would imply NP not subset P/poly by standard NP-completeness transfer.
- controlled interface: a nonuniform SAT-oracle circuit A_N deciding L_N with ordinary size N^{a+o(1)}, at most N^{q+o(1)} oracle gates, and queried formula length at most N^{beta+o(1)}.
- target-preserving condition: all advice and preprocessing are counted in A_N, only SAT circuits are substituted for oracle gates, valid source lengths map to bounded target lengths, and no hidden nonuniform witness search is used.

## Assumptions

- epsilon>0 is fixed independently of c.
- The source lower bound is for the same nonuniform circuit model used after substitution.
- SAT in SIZE(m^c) means a circuit family of size O(m^c) for every relevant target length m.
- Adaptive queries are represented as oracle gates in A_N, so gate-by-gate substitution is legitimate.

## Equations

- substitution_upper_bound: `SIZE(L_N) \le N^{a+o(1)}+N^{q+o(1)}\cdot (N^{\beta+o(1)})^c = N^{\max\{a,q+\beta c\}+o(1)}`. Valid when: Valid when the source oracle circuit explicitly counts advice, preprocessing, and every SAT oracle gate before substitution.
- contrapositive_window: `SIZE(L_N)>N^{1+\epsilon} \Rightarrow SAT \notin SIZE(m^c) \text{ for } c<\frac{1+\epsilon-q}{\beta}, \ a<1+\epsilon, \ \beta>0`. Valid when: Applies after the reduction preserves target lengths and the lower bound holds on matching valid source lengths.
- all_exponent_obstruction: `\forall c\;[SAT\notin SIZE(m^c)] \text{ from fixed } \epsilon \text{ requires } \beta=0 \text{ and } \max\{a,q\}<1+\epsilon`. Valid when: Requires fixed epsilon and black-box substitution as the only target-preserving complexity-class transfer mechanism.

## Attempted Derivation

- Assume SAT has nonuniform circuits of size O(m^c) for every queried formula length m.
- Model the carrier algorithm as an oracle circuit A_N with explicit ordinary gates and explicit SAT-query gates; adaptivity is absorbed into the circuit DAG.
- Replace each SAT-query gate of length at most N^{beta+o(1)} by the corresponding SAT circuit of size N^{beta c+o(1)}.
- The resulting L_N circuit has size at most N^{a+o(1)}+N^{q+beta c+o(1)}.
- Contrapose against SIZE(L_N)>N^{1+epsilon}: only exponents c satisfying q+beta c<1+epsilon and a<1+epsilon are ruled out.
- Therefore a positive polynomial query-length exponent beta is a quantitative threshold-collapse falsifier for deriving NP not subset P/poly from one fixed barely-superlinear source lower bound.

Blocking gap: The only unquarantined escape is to construct a nonprojection carrier with N^{o(1)} target query length, sub-N^{1+epsilon} interface size, and a valid N^{1+epsilon} nonuniform lower bound.

## Falsifiers

- falsifier: beta>0 leaves only the finite window c<(1+epsilon-q)/beta, so all-exponent NP/poly separation cannot follow.
- falsifier: q>=1+epsilon means the oracle interface alone already exceeds the source lower-bound threshold.
- falsifier: a>=1+epsilon means preprocessing or advice leakage consumes the entire barely-superlinear margin.
- falsifier: projection or padding carriers with subpolynomial query length demagnify the source lower bound into a strong target lower bound, as in the earlier projection-sandwich quarantine.

## Learning

Cycle 7 generalizes the MCSP and padding failures to an oracle-interface theorem. A barely-superlinear carrier lower bound transfers through a black-box SAT interface as max{a,q+beta c}; hence positive target-query length exponent beta is the decisive threshold-collapse falsifier. The remaining valid route must either use subpolynomial target queries with a genuinely nonprojection carrier or abandon black-box substitution.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Test a succinct local-consistency or proof-complexity carrier with N^{o(1)} SAT queries: compute a,q,beta, then run the projection-demagnification falsifier before claiming any magnification.

# Barrier-Aware Lower-Bound Route, cycle 7

## Candidate Lemma

Lexicographic avoidance of size-s circuits gives a uniform hard truth table only at the enumeration threshold. For n-bit functions, N=2^n, the selector is target-preserving for E only when s(n)log s(n)=O(n); at s(n)=n^k with k>1 it lands in DTIME(2^{Theta(n^k log n)}) and gives no valid NP or E lower-bound bridge.

## Definitions

- source object: lexicographic circuit-avoidance selector over all Boolean circuits of size at most s(n) for n-bit functions.
- target object: a uniform language L_s whose n-bit truth table avoids SIZE(s(n)), with intended target class NP or E and lower-bound threshold s(n)=n^k.
- controlled interface: enumeration of circuit descriptions plus target-preserving computation of selected truth-table bits from input x without advice.
- target-preserving condition: the bit L_s(x) must be computable inside the named target class while preserving the same input length n and size threshold s(n).
- barrier posture: the selector is non-large, so the usual natural-proof largeness premise is absent, but the construction is relativizing and quantitatively too slow for the intended target.

## Assumptions

- Circuits are fan-in two Boolean circuits over a fixed finite basis.
- The number of size-s circuits on n inputs is at most 2^{O(s log s)} after standard encoding.
- To select the lexicographically first missing truth table, the route has no nonenumerative certificate of absence from all size-s circuit truth tables.
- Target E means DTIME(2^{O(n)}) for n-bit inputs; target NP requires polynomial-time verifiable witnesses.

## Equations

- circuit_count: `C_s(n) \le 2^{O(s\log s)}`. Valid when: Valid when circuits use a fixed finite basis and standard descriptions with O(s log s) bits.
- selector_time: `T_{sel}(n,s) \le 2^n\,2^{O(s\log s)}\,poly(n,s)`. Valid when: Applies when the selector constructs or queries the avoided table by exhaustive circuit enumeration.
- E_threshold: `T_{sel}(n,s) \le 2^{O(n)} \iff s(n)\log s(n)=O(n)`. Valid when: Requires comparing the exhaustive selector running time with the E time bound on n-bit inputs.
- polynomial_size_collapse: `s(n)=n^k,\ k>1 \Rightarrow T_{sel}(n,s)=2^{\Theta(n^k\log n)}`. Valid when: Valid when k is fixed above one and the enumeration term dominates the truth-table length.

## Attempted Derivation

- Set N=2^n and list all size-s circuits on n inputs; there are 2^{O(s log s)} descriptions.
- Evaluate each listed circuit on all N inputs and mark its N-bit truth table.
- Choose the lexicographically first unmarked N-bit string y_n and define L_s(x)=y_n[x].
- By construction, the n-bit slice of L_s is not computed by any size-s circuit.
- The direct bit algorithm recomputes the marked set or an equivalent avoidance certificate, costing 2^n 2^{O(s log s)} poly(n,s).
- Thus E preservation forces s log s=O(n), while polynomial lower-bound thresholds s=n^k for k>1 move the language outside E and far outside NP.

Blocking gap: No local NP-checkable or E-time certificate is supplied for the statement that the chosen prefix remains outside every size-s circuit truth table.

## Falsifiers

- falsifier: s(n)=n^2 yields selector time 2^{Theta(n^2 log n)}, invalidating any claimed E-preserving transfer by raw counting.
- falsifier: advice of length 2^{O(s log s)} can encode the relevant avoidance information, so advice-bearing targets suffer nonuniform leakage.
- falsifier: the same circuit enumeration works relative to an oracle, so a fully relativizing version cannot imply an unrelativized P != NP separation.
- falsifier: calling the selected table non-natural is insufficient; the obstruction here is explicitness and target-time collapse.

## Learning

Cycle 7 turns counting-diagonalization optimism into a concrete threshold lemma: exhaustive lexicographic avoidance yields hard slices, but preserves E only for s log s=O(n). Polynomial thresholds such as n^2 require 2^{Theta(n^2 log n)} time, so the bridge is invalid for NP and for E at the desired lower-bound scale. This is valid barrier-aware route progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Test whether an MCSP-gap certificate can replace global circuit enumeration: source GapMCSP_{s,2s}, target NP language, threshold s=n^k, with audits for natural-proof largeness and advice leakage.

# MCSP / Meta-Complexity Carrier Transfer, Cycle 7: Searchable Certificate Repair

## Candidate Lemma

Searchable succinct high-MCSP certificates with constant gap imply an all-large-length E lower bound. Fix epsilon>0 and kappa>=1. If a deterministic certificate verifier soundly accepts only decoders for m-bit functions of circuit complexity greater than 2^{epsilon m}, has O(m)-bit searchable certificates, and has an accepted pair in every interval [ceil(n/kappa),n], then for every delta<epsilon/kappa there is L in E with CC(L_n)>2^{delta n} for all sufficiently large n.

## Definitions

- source object: a searchable succinct no-side MCSP certificate system (V,D) where a code u defines f_u:{0,1}^m->{0,1}, V(1^m,u,pi) is deterministic, and acceptance soundly implies CC(f_u)>2^{epsilon m}.
- target object: an all-large-length language L in E=DTIME(2^{O(n)}) satisfying CC(L_n)>2^{delta n} for each sufficiently large input length n.
- controlled interface: on input length n, search m in [ceil(n/kappa),n] and all pairs (u,pi) of total length at most c m; select the first accepted pair and set L(x)=D(u,prefix_m(x)).
- target-preserving condition: V and D run in 2^{O(m)}, witnesses have length O(m), accepted pairs exist in every kappa-gap interval, and no advice or nonuniform selector is used.

## Assumptions

- Constants epsilon>0, kappa>=1, c>0 are fixed independently of m and n.
- Soundness is semantic: V(1^m,u,pi)=1 implies every Boolean circuit computing f_u has size greater than 2^{epsilon m}.
- For every sufficiently large n, some m in [ceil(n/kappa),n] has an accepted pair (u,pi) with |u|+|pi|<=c m.
- The decoder D(u,z) computes f_u(z) deterministically in 2^{O(m)} time.

## Equations

- search_time: `T_L(n) \le \sum_{m=\lceil n/\kappa\rceil}^{n} 2^{c m}(T_V(m)+T_D(m)) \le 2^{O(n)}`. Valid when: Valid when code-plus-proof length is linear in m and both verifier and decoder have single-exponential running time.
- padding_transfer: `\mathrm{CC}(f_u) \le \mathrm{CC}(L_n)+O(n)`. Valid when: Applies when L_n is defined by f_u on the first m input bits and the remaining n-m bits are fixed.
- exponent_margin: `2^{\delta n}+O(n) < 2^{\epsilon m}\quad(m\ge n/\kappa,\ \delta<\epsilon/\kappa)`. Valid when: Requires a fixed positive exponent margin epsilon/kappa minus delta on sufficiently large input lengths.
- target_lower_bound: `\mathrm{CC}(L_n)>2^{\delta n}\text{ for all sufficiently large }n`. Valid when: Valid after the sound accepted certificate is found in every kappa-gap interval without advice.

## Attempted Derivation

- Replace the nonuniform hard truth-table carrier by a uniform search space of compact pairs (u,pi).
- Use V-soundness so that every accepted pair defines a genuinely high-MCSP function f_u, rather than an advised candidate.
- For each target length n, scan source lengths m in [ceil(n/kappa),n] and all O(m)-bit pairs until an accepted pair is found.
- Define L on n-bit inputs by applying the selected decoder to the first m bits and ignoring the padding bits.
- The search and evaluation cost is 2^{O(n)}, so L is in E.
- If L_n had circuits of size 2^{delta n}, fixing the ignored bits would give circuits for f_u of size 2^{delta n}+O(n).
- Since m>=n/kappa and delta<epsilon/kappa, this contradicts V-soundness for all large n.

Blocking gap: No construction is known for a sound verifier with O(m)-bit certificates and kappa-gap existence that is not already smuggling in the desired lower bound.

## Falsifiers

- falsifier: accepted pairs exist only via advice-selected (u_m,pi_m), causing nonuniform leakage and invalidating the E target.
- falsifier: |u|+|pi|=m^{1+Omega(1)} or T_V(m)=2^{m^{1+Omega(1)}}, so exhaustive extraction leaves E.
- falsifier: accepted source lengths have gap kappa(n)->infty, forcing the lower-bound exponent delta to collapse to 0.
- falsifier: the certificate set becomes a dense poly(N)-time decidable truth-table property, triggering the natural-proofs obstruction under exponentially secure PRFs.
- falsifier: V certifies only average-case, approximate, or promise MCSP hardness without a reduction to exact worst-case circuit lower bound for f_u.
- falsifier: D uses randomized choices or hidden advice, so the constructed language is not a deterministic uniform E language.

## Learning

Cycle 7 repairs the circular carrier by making the source a searchable proof-like object. The valid bridge now has a sharp threshold: O(m)-bit sound certificates on kappa-gap source lengths yield E lower bounds with exponent delta<epsilon/kappa. The remaining task is not another hardness-magnification slogan but construction of a sparse, non-natural, nonuniform-free certificate source; dense constructive variants hit the natural-proofs falsifier.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Try to instantiate V as a sparse proof-complexity certificate for succinct lower-bound tautologies LB(u,2^{epsilon m}); measure proof-code length, verifier time, gap coverage, and whether the induced accepted truth-table set is non-natural rather than dense.
