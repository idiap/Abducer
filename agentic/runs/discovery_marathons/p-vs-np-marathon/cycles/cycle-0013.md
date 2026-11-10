# cycle-0013

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: Polylog Nonblackbox Compact Consumer

## Candidate Lemma

Fix d>1, epsilon>0, and a compact-consumer exponent rho<1+epsilon. If a uniform carrier H_N has an i.o. general-circuit lower bound SIZE(H_N)>N^{1+epsilon} on valid lengths and every SAT circuit of size m^c at m=floor((log N)^d) yields a target-clean nonblackbox circuit for H_N of size N^rho poly(m^c,m,log N), then SAT is not in SIZE(n^c) for every fixed c. Hence SAT notin P/poly, conditional on the carrier and source lower bound.

## Definitions

- source object: A uniform carrier H={H_N} with H_N:{0,1}^N -> {0,1}, measured in nonuniform general circuit SIZE at source threshold N^{1+epsilon} on infinitely many valid N.
- target object: SAT_m under nonuniform circuits of size m^c for each fixed c; excluding all fixed c gives SAT notin P/poly and hence NP not subset P/poly.
- controlled interface: A nonblackbox compact consumer T_N that, from the description of a SAT_{L(N)} circuit D_m, constructs a circuit for H_N by universal evaluation of D_m, not by SAT-answer lookup.
- target-preserving condition: H_N is defined independently of D_m, L(N)=floor((log N)^d) is unbounded along valid N, and all extra constants in T_N are uniform or derived from D_m so no nonuniform leakage enters.
- valid length convention: If SAT has polynomial-size circuits for all large m, then it supplies D_{L(N)} for all large valid N; an i.o. source lower bound is enough for contradiction.
- source model convention: The upper circuit produced by T_N must be counted in the same general SIZE model as the lower bound.

## Assumptions

- d>1 is a fixed constant independent of N and of the target exponent c.
- For each fixed c, the universal-evaluation tax for a SAT circuit of size m^c is poly(m^c,m,log N)=N^{o(1)}.
- The compact consumer exponent rho is independent of c; otherwise the all-exponent P/poly conclusion is invalid.
- The source lower bound holds for infinitely many valid N after the target circuit family would already exist.
- SAT is the standard NP-complete language under length-respecting encodings.

## Equations

- polylog target length: `L(N)=\lfloor (\log N)^d\rfloor,\quad d>1`. Valid when: Valid when d is fixed and N ranges over the carrier's valid input lengths.
- fixed exponent amortization: `L(N)^c=(\log N)^{dc}=N^{o(1)}`. Valid when: Valid when c and d are constants, not growing with N.
- compact substitution bound: `\mathrm{SIZE}(H_N)\le N^{\rho}\operatorname{poly}(L(N)^c,L(N),\log N)=N^{\rho+o(1)}`. Valid when: Applies after the reduction preserves the source circuit model and target circuit descriptions.
- magnification threshold: `\rho<1+\varepsilon\ \wedge\ \mathrm{SIZE}(H_N)>N^{1+\varepsilon}\text{ i.o.}\ \Rightarrow\ \mathrm{SAT}\notin\mathrm{SIZE}(n^c)`. Valid when: Requires the source lower bound and compact upper bound to hold on overlapping valid lengths.

## Attempted Derivation

- Fix a target exponent c and assume, for contradiction, that SAT_m has circuits D_m of size m^c for all sufficiently large m.
- For each sufficiently large valid carrier length N, set m=L(N)=floor((log N)^d), so the assumed SAT family supplies D_m.
- Run the compact nonblackbox consumer T_N with D_m wired into its universal evaluator; no SAT truth table and no independent advice are allowed.
- Because m^c=(log N)^{dc}=N^{o(1)}, the produced H_N circuit has size N^rho poly(m^c,m,log N)=N^{rho+o(1)}.
- Choose delta>0 with rho+delta<1+epsilon. For large valid N, the upper bound is at most N^{rho+delta}, contradicting SIZE(H_N)>N^{1+epsilon} on infinitely many valid lengths.
- Since c was arbitrary and rho does not depend on c, the conditional bridge excludes every fixed polynomial exponent for SAT circuits.

Blocking gap: No explicit carrier H_N is yet supplied with both a target-clean polylog nonblackbox compact consumer and an i.o. N^{1+epsilon} general-circuit lower bound. The lower-bound proof also must be non-natural or otherwise outside the natural-proofs obstruction.

## Falsifiers

- falsifier: compact consumer exponent rho reaches or exceeds 1+epsilon, causing quantitative threshold collapse.
- falsifier: L(N)=O(log N), because hardwired SAT truth tables give an unconditional lookup simulation.
- falsifier: the carrier reduces to a black-box projection SAT(G(x)) in the same model, reviving the demagnification from earlier cycles.
- falsifier: auxiliary advice A_N is not uniformly computable from N and the hypothesized SAT circuit D_{L(N)}.
- falsifier: the produced upper circuit is not in the same SIZE model as the claimed source lower bound.
- falsifier: a dense constructive natural property is the only known path to the general-circuit lower bound, triggering the natural-proofs barrier under standard PRG assumptions.

## Learning

Cycle 13 turns the superlogarithmic polylog window into an exact bridge: L=(log N)^d with d>1 makes SAT circuits of size L^c amortize to N^{o(1)}, while truth-table lookup costs 2^L=N^{omega(1)} and no longer supplies the old falsifier. The valid threshold is rho<1+epsilon for a target-clean nonblackbox compact consumer. The new hard obstruction is not folklore but the absence of an explicit carrier with no advice leakage and a non-natural N^{1+epsilon} general-circuit lower bound.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and threshold calculator.`
- Rationale: The branch has a valid d>1 window, but another abstract magnification restatement would not test target preservation. A concrete polylog audit carrier exposes the exact rho, lookup, and advice-leakage failure modes.
- Situation seed: PolyLogAudit_{N,d,V}: imagine a fixed verifier V whose N-bit input selects one local audit location in a canonical computation that uses a length-m SAT circuit description D_m, with m=floor((log N)^d). Under the target assumption D_m is wired into a universal evaluator; the Boolean carrier H_N is fixed by V and the canonical audit rule, not by the chosen D_m.
- Varied variable: d in the query/circuit length m=(log N)^d, varied across d<=1, 1<d<2, and larger fixed constants.
- Held-fixed controls: Source model is nonuniform general SIZE and the source threshold remains N^{1+epsilon}., Target assumption supplies only SAT circuits of size m^c for fixed c, with no extra advice., Consumer overhead excluding D_m is constrained to N^rho with rho<1+epsilon., The carrier must be independent of the selected SAT circuit and valid on infinitely many N.
- Expected observation: For d<=1, lookup tables can be hardwired and should kill the source lower bound if the audit is black-box. For d>1, lookup becomes superpolynomial while D_m substitution remains N^{o(1)}, so any remaining failure should be visible as rho collapse, projection demagnification, or advice leakage.
- Transfer certificate needed: A formal construction of H_N and T_N proving SIZE(T_N[D_m])<=N^rho poly(|D_m|,m,log N), uniform derivation of all auxiliary data from D_m, and a source lower-bound method that is not a dense constructive natural proof.

## Next Experiment

Instantiate PolyLogAudit_{N,d,V} with a universal-circuit verifier, compute the exact overhead exponent rho and auxiliary advice length, and reject the instance immediately if H_N depends on a hidden SAT circuit or collapses to a black-box SAT query family.

# Barrier-Aware Lower-Bound Route: advised local naturalization gate

## Candidate Lemma

Any deterministic advised q-query black-box separator for the SAT_m truth table naturalizes unless its query bound, advice/decider size, or nonblack-box interface escapes the named quantitative thresholds.

## Definitions

- source object: a deterministic oracle verifier V_m(alpha, z) with advice alpha_m of length b(N), truth-table oracle z in {0,1}^N, N=2^m, and at most q(N) adaptive bit queries; it accepts the SAT_m truth table.
- target object: the induced property P_m={z: V_m(alpha_m,z)=1}, intended to be useful against m^k-size Boolean circuits and therefore to certify only SAT notin SIZE(m^k), not P != NP.
- controlled interface: hardwire alpha_m into the property decider, expose the accepting query transcript on SAT_m, and audit density, constructivity, and usefulness before claiming a barrier escape.
- target-preserving condition: alpha_m and V_m must yield a valid property decider within the audited adversary scale, soundness must reject every m^k-size truth table, and the verifier may not add promises, oracle gates, or advice leakage that changes the target class.

## Assumptions

- V_m is deterministic after alpha_m is fixed.
- V_m accepts the SAT_m truth table.
- For every Boolean function g:{0,1}^m->{0,1} computable by circuits of size at most m^k, V_m(alpha_m,tt(g))=0.
- The property decider obtained by hardwiring alpha_m has circuit size D(N).
- The natural-proof audit is invoked only against full-truth-table distinguishers at size at least D(N) and advantage at least 2^{-q(N)}.

## Equations

- accepting_cylinder_density: `\mu(P_m)\ge 2^{-q(N)}`. Valid when: Valid when V_m is deterministic and one accepting SAT transcript fixes at most q queried truth-table positions.
- hardwired_property_size: `D(N)\le \operatorname{poly}(|V_m|+b(N)+q(N)\log N)`. Valid when: Applies when the advice string is hardwired and oracle queries are implemented as input-wire selections.
- polynomial_largeness_threshold: `q(N)\le a\log_2 N\quad\Longrightarrow\quad \mu(P_m)\ge N^{-a}`. Valid when: Valid when the density lower bound comes from a single accepting cylinder in the full truth-table cube.
- usefulness_condition: `P_m\cap \{\operatorname{tt}(g):\operatorname{size}(g)\le m^k\}=\varnothing`. Valid when: Requires soundness against every small circuit truth table, not merely against a sampled or promised subclass.
- full_truth_table_prf_distinguishing: `\Pr_{R\leftarrow\{0,1\}^N}[P_m(R)=1]-\Pr_{K}[P_m(\operatorname{tt}(F_K))=1]\ge 2^{-q(N)}`. Valid when: Valid when every keyed function F_K has circuit size at most m^k and P_m is useful against that size.

## Attempted Derivation

- Fix m and N=2^m. Let y=tt(SAT_m) and run the deterministic verifier V_m(alpha_m,y).
- Record the adaptive accepting transcript: queried indices i_1,...,i_t with t<=q(N) and answers y_{i_j}.
- Every z agreeing with y on those queried indices follows the same deterministic path and is accepted, so P_m contains a subcube of codimension at most q(N).
- Therefore mu(P_m)>=2^{-q(N)}; when q<=a log N this is inverse-polynomial largeness.
- Soundness gives P_m no truth table computable by circuits of size m^k, so P_m is useful against SIZE(m^k).
- Hardwire alpha_m and the verifier into a full-truth-table decider. If its size is N^{O(1)}, this is a constructive or P/poly-natural property at the audited scale.
- If a PRF family has every keyed function in SIZE(m^k), the property rejects all PRF truth tables but accepts a random truth table with probability at least 2^{-q}; this is a full-truth-table distinguisher.
- Thus a low-query advised black-box lower-bound route is not a valid barrier escape unless it raises q, destroys hardwired constructivity, or uses a genuinely nonblack-box feature.

Blocking gap: The derivation excludes only deterministic black-box local separators with hardwirable advice. It does not touch nonlocal algebraic, proof-theoretic, or syntax-sensitive methods that fail to contain a large accepting cylinder.

## Falsifiers

- A proposed q=O(log N) SAT separator with polynomial-size hidden advice is a falsifier for the claim that advice alone avoids natural proofs, because the advice can be hardwired.
- A verifier whose soundness rejects only sampled circuits, average-case circuits, or a promise subset is a falsifier for target preservation: usefulness against SIZE(m^k) is then not valid.
- A superpolynomial-advice separator may evade this naturalization lemma, but it is a falsifier for uniform-route claims unless an advice-compression bridge is supplied.
- A randomized local separator without all-circuit seed preservation is a falsifier for deterministic-cylinder density claims.

## Learning

Cycle 13 isolates an advice-sensitive local naturalization lemma. Deterministic q-query SAT separators with hardwirable advice contain an accepting cylinder of density 2^{-q}; if q=O(log N) and the hardwired decider is polynomial in N, the object is a valid natural property useful against SIZE(m^k). Secret polynomial advice is therefore not a barrier escape. Superpolynomial advice may avoid the natural-proof falsifier but then loses constructive target transfer unless separately certified.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a concrete advice-leakage threshold, not another statement that natural proofs are a barrier. The experiment tests when a local SAT separator remains target-preserving after advice is hardwired.
- Situation seed: For each input length m, imagine an advised deterministic q-query verifier for the N=2^m-bit truth table of SAT_m. It accepts tt(SAT_m), rejects every truth table of an m-input circuit of size m^k, and uses an advice string alpha_m whose origin is deliberately unspecified.
- Varied variable: Advice length exponent gamma in b(N)=N^gamma, with q(N)=c log N held initially at the local-query threshold.
- Held-fixed controls: The verifier is deterministic and black-box in the candidate truth table after advice is fixed., The target lower bound remains SAT_m notin SIZE(m^k), not P != NP., Soundness is universal over all m^k-size circuits., The property is evaluated on the full N-bit truth table, so density is measured in {0,1}^N.
- Expected observation: For every fixed gamma giving polynomial hardwired decider size, the accepting transcript yields density N^{-c} and the route becomes a natural property useful against SIZE(m^k). Only when gamma or verifier size makes the decider superpolynomial, or when the interface becomes nonblack-box, does the natural-proof audit stop applying; then target preservation must be re-certified.
- Transfer certificate needed: A formal certificate showing either advice compression to a uniform/poly(N) decider with a non-natural feature, or a proof that the large-cylinder density argument is invalid because the verifier uses syntax, proof soundness, or another nonblack-box relation not reducible to queried truth-table bits.

## Next Experiment

Test a syntax-gated Cook-Levin/proof-system certificate that queries clauses or derivations rather than raw truth-table bits, and compute whether the accepting-cylinder density argument still survives under a target-preserving reduction to SAT_m notin SIZE(m^k).

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

In the circuit-by-circuit diagonal MCSP certificate source model, E-compatible verification cannot certify a constant MCSP no-side threshold. If the verifier proves C(T)>s by explicitly excluding all m-input circuits of size s and must run in 2^{O(m)}, then s log s=O(m). Hence s=O(m/log m), and the carrier transfer exponent collapses to zero.

## Definitions

- source object: an O(m)-bit certificate c and a 2^{alpha m}-time sequential verifier V_m(c) that emits a truth table T_c in {0,1}^{2^m} and proves T_c is outside SIZE(s(m)) by enumerating or individually excluding all circuits of size at most s(m).
- target object: an E language L whose length-m truth table equals some accepted T_c on kappa-dense source lengths, intended to satisfy C_L(n)>2^{delta n} for constant delta>0.
- controlled interface: exhaustive search over O(m)-bit certificates followed by V_m must stay within 2^{O(m)} time, and the MCSP no-side threshold s(m) must transfer through the existing delta<epsilon/kappa extraction with epsilon=(log s(m))/m.
- target-preserving condition: certificate length, verifier time, and source-length density are uniform constants, and no nonuniform selector, random-access generator, or advice string may identify hard tables outside the verifier.

## Assumptions

- Circuit descriptions over fan-in two Boolean gates have count at most 2^{b s log s} and at least 2^{b' s log s} for standard encodings up to constant factors.
- The source verifier is in the diagonal-enumeration model: its soundness argument inspects or excludes circuits separately, with no compressed algebraic or proof-complexity certificate for the whole low-circuit set.
- The extraction theorem from prior cycles remains valid for kappa-dense source lengths and threshold s(m)=2^{epsilon m}.

## Equations

- low_circuit_count: `|\mathrm{SIZE}_{m}(s)| \le 2^{b s\log s}`. Valid when: Valid when the source lower-bound model is explicitly Boolean fan-in two circuits with a fixed syntactic encoding and s is at least linear in m.
- enumeration_budget: `2^{\Theta(s\log s)} \le 2^{\alpha m}\quad\Rightarrow\quad s\log s=O(m)`. Valid when: Applies when the verifier certifies high MCSP by circuit-by-circuit exclusion and the E extraction budget fixes verification time to 2^{O(m)}.
- constant_threshold_failure: `s=2^{\epsilon m}\ \Rightarrow\ T_{\mathrm{enum}}=2^{\Theta(m2^{\epsilon m})}`. Valid when: Valid when epsilon is a positive constant and the soundness source performs explicit diagonal enumeration over all size-s circuits.
- collapsed_transfer: `\epsilon_m={\log s(m)\over m}=O\!\left({\log m\over m}\right),\qquad \delta<\epsilon_m/\kappa=o(1)`. Valid when: Requires the target-preserving transfer from MCSP threshold s(m) to E lower bounds while kappa remains constant and enumeration time stays E-compatible.

## Attempted Derivation

- Set N=2^m and assume a diagonal source verifier emits T and proves C(T)>s by excluding each m-input circuit of size at most s.
- Use the standard encoding bound that the number of such circuits is 2^{Theta(s log s)}.
- Since exhaustive certificate search over 2^{O(m)} certificates plus verification must remain in E, require verifier time 2^{O(m)}.
- Thus the enumerative proof can be target-preserving only when 2^{Theta(s log s)}<=2^{O(m)}, equivalently s log s=O(m).
- Solving gives s=O(m/log m), so epsilon_m=(log s)/m=O((log m)/m).
- Plugging epsilon_m into the prior valid carrier bridge gives only delta<epsilon_m/kappa=o(1), not a constant exponential E lower bound.

Blocking gap: The argument does not exclude compressed non-enumerative soundness certificates, such as a genuinely non-natural proof-complexity object that refutes all small circuits simultaneously.

## Falsifiers

- falsifier: the proposed soundness verifier performs circuit-by-circuit enumeration at threshold 2^{epsilon m}, forcing time 2^{Theta(m2^{epsilon m})}.
- falsifier: the verifier emits a bit-addressable table with circuits below the claimed MCSP threshold.
- falsifier: the accepted property becomes large, constructive, and useful against SIZE(2^{epsilon m}), triggering the natural-proofs obstruction under standard PRF assumptions.
- falsifier: certificate length grows omega(m), so exhaustive source search is no longer valid inside E.
- falsifier: kappa-density fails or kappa grows with m, collapsing the transferred exponent delta.

## Learning

Cycle 13 gives an exact quantitative falsifier for brute-force MCSP source soundness: enumeration is E-compatible only up to s=O(m/log m), making epsilon_m=O(log m/m) and delta=o(1). The valid carrier bridge survives, but any constant-threshold source must be non-enumerative, sparse, non-natural, and nonuniform-free.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for source-soundness proposals.`
- Rationale: The bridge theorem is already valid; the live uncertainty is whether a concrete MCSP no-side source can prove soundness without secretly spending super-E time or leaking nonuniform random access.
- Situation seed: A padded diagonal MCSP certificate family: for each m, a certificate names a candidate truth table stream, and the verifier tries to certify that every circuit of size s=2^{beta m} disagrees with it somewhere.
- Varied variable: The threshold exponent beta in s=2^{beta m}.
- Held-fixed controls: Certificate length is at most a m for a fixed a., Verifier plus exhaustive certificate search must run in 2^{O(m)} time., Source lengths are kappa-dense with constant kappa., The extraction target remains an E lower bound with exponent delta<beta/kappa., No nonuniform advice or subthreshold bit-access circuit is allowed.
- Expected observation: For every constant beta>0, circuit-by-circuit soundness requires 2^{Theta(m2^{beta m})} work; beta must shrink to O(log m/m) before the verifier is E-compatible, and then the target exponent vanishes.
- Transfer certificate needed: A formal classification that the proposed verifier is genuinely enumerative or black-box over low circuits; without that certificate, the experiment is only a falsifier for brute-force diagonal repairs, not for compressed non-natural sources.

## Next Experiment

Audit proof-complexity carriers for the universal circuit tautology U_{m,s,T}: no size-s circuit computes T, varying proof length p(m) while holding verifier time 2^{O(m)} and sparsity 2^{O(m)} fixed.
