# cycle-0008

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization, cycle 8: subpolynomial-query threshold repair

## Candidate Lemma

Let K={K_N} be computable by nonuniform oracle circuits of ordinary size N^{a+o(1)}, with at most N^{q+o(1)} SAT gates, each receiving queries of length s(N)=N^{o(1)}. If K requires circuits of size >N^{1+epsilon} for all large N and max(a,q)<1+epsilon, then SAT is not in SIZE(n^c) for every fixed c; hence NP is not contained in P/poly. This is a valid route lemma, not a proof of the source lower bound.

## Definitions

- source object: A Boolean family K={K_N} on N input bits, measured against nonuniform Boolean circuits, with source threshold C(K_N)>N^{1+epsilon}.
- target object: SAT against nonuniform Boolean circuits, with target consequence SAT notin SIZE(n^c) for every fixed c, which implies NP not subset P/poly.
- controlled interface: Oracle circuits for K_N of ordinary size A(N)=N^{a+o(1)}, at most Q(N)=N^{q+o(1)} adaptive SAT gates, and maximum query length s(N)=N^{o(1)}.
- target-preserving condition: The source lower bound is against the same or stronger circuit model obtained after substituting SAT circuits, and no advice other than the hypothesized SAT circuits is added.

## Assumptions

- epsilon>0 is fixed independently of c.
- The SAT encoding is length-padded so every shorter query is handled by one SAT circuit on length s(N)+O(1).
- Adaptive oracle gates are circuit gates; replacing each by a SAT circuit composes without decision-tree blowup.
- The source lower bound holds eventually, or on a cofinal length set on which the oracle-circuit upper bound also holds.
- The target claim is nonuniform; a merely uniform source lower bound is a model-mismatch falsifier.

## Equations

- oracle-substitution-size: `C_K(N) \le A(N)+Q(N)\cdot(C_{SAT}(s(N))+O(s(N)))+O(1).`. Valid when: Valid when the source oracle circuit explicitly counts all query-building wires outside the SAT oracle gates.
- polynomial-query-transfer: `C_{SAT}(n)\le n^c,\ A(N)\le N^{a+o(1)},\ Q(N)\le N^{q+o(1)},\ s(N)=N^{\beta(N)} \Rightarrow C_K(N)\le N^{\max\{a,q+\beta(N)\max(c,1)\}+o(1)}.`. Valid when: Applies after the reduction preserves nonuniformity and pads all SAT queries to one controlled length.
- subpoly-query-collapse: `s(N)=N^{o(1)} \Rightarrow C_K(N)\le N^{\max\{a,q\}+o(1)} \quad \text{for each fixed } c.`. Valid when: Valid when c is fixed before taking N large, so c times the query-length exponent is still o(1).
- magnified-consequence: `C_K(N)>N^{1+\epsilon}\ \wedge\ \max\{a,q\}<1+\epsilon\ \Rightarrow\ \forall c\ C_{SAT}(n)\not\le n^c.`. Valid when: Requires the target-preserving complexity-class transfer and an eventual source lower bound on the same circuit basis.

## Attempted Derivation

- Fix an arbitrary constant c and assume for contradiction that SAT has nonuniform circuits of size n^c for all sufficiently large n.
- Pad all SAT queries made by the K_N oracle circuit to one length s(N)+O(1); finite small exceptions are hardwired and do not affect the exponent.
- Replace each SAT oracle gate by the corresponding SAT circuit. Adaptivity causes no exponential blowup because the oracle computation is already represented as a circuit DAG with oracle gates.
- The resulting K_N circuit has size at most A(N)+Q(N)(s(N)^c+O(s(N)))+O(1).
- With A=N^{a+o(1)}, Q=N^{q+o(1)}, and s=N^{o(1)}, this size is N^{max(a,q)+o(1)} for the fixed c.
- Choose eta>0 with max(a,q)+eta<1+epsilon. For all large N the substituted K_N circuits have size <N^{1+epsilon}, contradicting the source lower bound.
- Since c was arbitrary, SAT is not in SIZE(n^c) for any fixed c; therefore SAT notin P/poly and NP not subset P/poly.

Blocking gap: No concrete non-natural carrier K is known with both a near-linear subpolynomial-query SAT interface and an N^{1+epsilon} nonuniform circuit lower bound. MCSP-like truth-table carriers fail because their SAT-verification queries have polynomial, usually linear, dependence on N.

## Falsifiers

- falsifier: s(N)=N^beta for beta>0 causes threshold collapse and excludes only c<(1+epsilon-q)/beta.
- falsifier: q>=1+epsilon or ordinary overhead a>=1+epsilon leaves no room below the source lower-bound threshold.
- falsifier: the source theorem is uniform-only or restricted-model, while SAT notin P/poly requires a nonuniform target-preserving contradiction.
- falsifier: a hidden advice string used to choose queries or decompressions is not counted in A(N), creating nonuniform leakage.
- falsifier: the proposed carrier is a large constructive useful truth-table property; under standard PRF assumptions a natural proof of its P/poly usefulness is blocked.
- falsifier: if both the bridge and the source lower-bound proof relativize, oracle worlds with NP^O subset P^O/poly prevent promotion to a main P vs NP proof.

## Learning

Cycle 8 repairs the remaining route exactly: subpolynomial SAT-query length is sufficient to remove the c-dependent threshold term, so N^{1+epsilon} lower bounds magnify only when max(a,q)<1+epsilon. The valid contribution is a quantified bridge plus a model-preservation gate; the unresolved hard task is finding a concrete carrier satisfying the interface and source lower bound without natural-proof or nonuniform-leakage failure.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Search for non-truth-table carriers in P^SAT with near-linear ordinary work and subpolynomial SAT queries, e.g. succinct consistency or decompression-check problems, then compute A,Q,s and test against L8.1 before discussing P vs NP.

# Barrier-Aware Lower-Bound Route: SAT-Speedup Threshold Audit

## Candidate Lemma

Let C be a reasonable Boolean circuit class closed under projections, AC0-style local reductions, composition, and bounded fan-in AND/OR. If C-SAT on m-variable size m^d C-circuits has deterministic running time 2^m/m^q for every fixed d and sufficiently large q demanded by the reduction, then NEXP is not contained in C[poly]. Quantitatively, for target exponent c, a saving q exceeding the easy-witness and encoding overhead gives NTIME(2^n) not contained in C[n^c].

## Definitions

- source object: a uniform deterministic SAT algorithm A_C for m-input C-circuits of size m^d with running time 2^m/m^q.
- target object: the route-level lower bound NEXP not subset C[poly], not the main P != NP conjecture.
- controlled interface: Williams-style easy-witness compression plus C-closure under local Cook-Levin verification, projections, composition, and final satisfiability calls.
- target-preserving condition: the assumed C[n^c] circuits for the NEXP verifier and witnesses must compose into size m^d C-SAT instances while the saving m^{-q} remains larger than all polynomial overheads.
- reasonable C means circuit evaluation is polynomial-time decidable and the verifier reductions do not leave C after substituting small witness circuits.
- The parameter m is the logarithmic tableau-address or verifier-choice length after succinct encoding, not the original exponential witness length.

## Assumptions

- C is fixed before choosing d and q, and has a uniform encoding for the SAT solver.
- For each target size exponent c there is a polynomial overhead m^{b(c)} in the easy-witness and verifier-composition stage.
- The nondeterministic time hierarchy supplies a language in NTIME(2^n) outside NTIME(2^n/n^r) for some r above simulation overhead.
- The SAT algorithm is not merely a truth-table property test; it accepts succinct C-circuit descriptions.

## Equations

- source_sat_saving: `T_{C\text{-}SAT}(m,m^d) \le 2^m/m^q`. Valid when: Valid when m counts Boolean variables of the generated C-SAT instance and d is fixed before the saving exponent q is chosen.
- composed_decision_time: `T_{derived}(n) \le 2^n\,n^{b(c)}/n^q = 2^n/n^{q-b(c)}`. Valid when: Applies after the easy-witness lemma and C-closure produce only polynomial overhead n^{b(c)} for target exponent c.
- hierarchy_margin: `q > b(c)+r \implies NTIME(2^n) \nsubseteq C[n^c]`. Valid when: Requires the nondeterministic hierarchy margin r to exceed the universal simulation and padding losses in the contradiction.

## Attempted Derivation

- Assume for contradiction that a fixed NEXP-complete language L has C-circuits of size n^c.
- Apply the easy-witness lemma: accepting witnesses for L can be represented by small circuits compatible with C-composition under the containment assumption.
- Encode the verifier's local consistency checks as C-circuits on m=Theta(n) address and choice variables, with size m^{d(c)} and overhead m^{b(c)}.
- Run the uniform C-SAT algorithm on the composed instances in time 2^m/m^q.
- Choose q>b(c)+r so the derived nondeterministic decision time is 2^n/n^r after all reductions.
- Contradict the nondeterministic time hierarchy for NTIME(2^n), yielding NEXP not subset C[n^c].

Blocking gap: The derivation is conditional on the source SAT algorithm and stops at NEXP. It supplies no NP hierarchy, no advice-removal theorem, and no direct P != NP consequence.

## Falsifiers

- falsifier: the alleged C-SAT solver works only on explicit truth tables, so the route loses succinctness and is invalid for the bridge.
- falsifier: the circuit class C is not closed under the verifier-composition operations, so the generated SAT instance exits the source model.
- falsifier: the saving is fixed at 2^m/m while the reduction overhead is m^{b} with b>=1, causing quantitative threshold collapse.
- falsifier: a claimed NP lower bound follows only by replacing NEXP with NP in the conclusion; this is not a valid target-preserving transfer.
- falsifier: an oracle-gate version is asserted without specifying how the SAT algorithm handles oracle gates, reviving the relativization audit.

## Learning

Cycle 8 isolates a valid quantitative bridge: sufficiently strong uniform C-SAT savings, after easy-witness compression and C-closure, imply NEXP not subset C[poly] with threshold q>b(c)+r. The same bridge is invalid as a P-vs-NP route because the hierarchy margin and witness-compression interface are exponential-time objects.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Instantiate b(c) for ACC0-SAT and TC0-SAT reductions, then check whether known or conjectured savings are large enough to yield NEXP lower bounds without triggering natural-proof or oracle-gate falsifiers.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Short, uniform, sound certificates for kappa-dense GapMCSP no-instances give an all-length E circuit lower bound with exponent any delta<epsilon/kappa; this is a route-level bridge, not a proof of P != NP.

## Definitions

- source object: constants epsilon>0, kappa>=1, lambda,tau=O(1), a uniform verifier V(1^m,c), and a uniform bit-decompressor D(c,z) with |c|<=lambda m and z in {0,1}^m.
- target object: a language F in E such that SIZE(F_n)>2^{delta n} for every sufficiently large n and every fixed delta<epsilon/kappa.
- controlled interface: on input x of length n, search m in [ceil(n/kappa),n] and c in {0,1}^{<=lambda m}; choose the lexicographically first accepted pair and output D(c,prefix_m(x)).
- target-preserving condition: V and D run in 2^{tau m} time, no c_m is supplied as advice, accepted source lengths are kappa-dense, and V is sound for MCSP no-side threshold 2^{epsilon m}.

## Assumptions

- Existence: for every sufficiently large n there is m in [ceil(n/kappa),n] and c with V(1^m,c)=1.
- Soundness: if V(1^m,c)=1, then the m-bit truth-table function y_c(z)=D(c,z) has Boolean circuit complexity greater than 2^{epsilon m}.
- Uniformity: the search for m,c and the evaluation of D are performed by one deterministic machine, not by a nonuniform selector.
- Sparsity: the accepted truth tables at length m are at most 2^{lambda m}, so the induced useful property is not large in the Razborov-Rudich sense.

## Equations

- mcsp_threshold: `s(m)=2^{\epsilon m}`. Valid when: Valid when MCSP inputs are truth tables of m-bit Boolean functions and the no-side threshold is fixed exponentially in m.
- gap_choice: `m(n)\in[\lceil n/\kappa\rceil,n]`. Valid when: Valid when accepted source lengths are kappa-dense below every sufficiently large target input length.
- uniform_search_time: `T_F(n)\le \sum_{m=\lceil n/\kappa\rceil}^{n}2^{\lambda m}2^{\tau m}+2^{\tau n}=2^{O(n)}`. Valid when: Applies after certificate length and verifier-decompressor running times have fixed constant linear exponents in m.
- lower_bound_transfer: `SIZE(F_n)\ge 2^{\epsilon m(n)}-O(n)>2^{\delta n}\quad(\delta<\epsilon/\kappa)`. Valid when: Requires the target-preserving reduction from circuits for F_n to circuits for the certified m(n)-bit source function.
- non_largeness_audit: `\Pr_{y\in\{0,1\}^{2^m}}[y\text{ is accepted via some }c]\le 2^{\lambda m-2^m}`. Valid when: Valid when every accepted truth table is produced by at least one certificate of length at most lambda m.

## Attempted Derivation

- Define F on length n by exhaustive uniform search for an accepted pair (m,c) with m in [ceil(n/kappa),n], choosing the first pair in a canonical order.
- The search is in E because there are at most n values of m, at most 2^{lambda m} certificates per m, and each verification/evaluation costs 2^{tau m}.
- If F_n had a circuit C of size S, then fixing the ignored n-m input bits gives a circuit C'(z)=C(z,0^{n-m}) computing D(c,z) on m bits with size S+O(n).
- By verifier soundness, C' must have size greater than 2^{epsilon m}; hence S>2^{epsilon m}-O(n).
- Since m>=n/kappa, for every delta<epsilon/kappa and all large n, 2^{epsilon m}-O(n)>2^{delta n}.
- The accepted-image density is at most 2^{lambda m}/2^{2^m}, so the bridge is non-large and outside the largeness limb of the natural-proofs barrier.

Blocking gap: No noncircular construction is known for a 2^{O(m)}-time sound verifier that certifies MCSP no-side threshold 2^{epsilon m} for kappa-dense source lengths without already encoding an E lower bound.

## Falsifiers

- falsifier: V accepts some c whose decompressed truth table has a circuit of size at most 2^{epsilon m}.
- falsifier: accepted source lengths have gaps m_{j+1}/m_j tending to infinity, causing delta to collapse to zero.
- falsifier: |c_m| is omega(m), so exhaustive search is not guaranteed to define an E language.
- falsifier: V or D requires 2^{omega(m)} time or hidden advice, so the target language is not uniformly in E.
- falsifier: the construction only gives infinitely many target lengths, not all sufficiently large lengths.
- falsifier: the induced property is large, constructive, and useful, reactivating the natural-proofs obstruction under PRF assumptions.
- falsifier: the decompressor has circuits below 2^{epsilon m} for accepted c, contradicting soundness rather than proving hardness.

## Learning

Cycle 8 converts the certificate repair into a precise bridge theorem: O(m)-bit, 2^{O(m)}-verifiable, sound MCSP no-side certificates on kappa-dense lengths yield all-length E lower bounds with exponent delta<epsilon/kappa. The bridge is valid and non-large, but the remaining obstruction is the construction of such a verifier without circularly assuming high circuit complexity.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Test proof-complexity instantiations: can short Frege/IPS certificates soundly prove that D(c,.) avoids all circuits of size 2^{epsilon m} while V checks them in 2^{O(m)} time and remains sparse rather than natural?
