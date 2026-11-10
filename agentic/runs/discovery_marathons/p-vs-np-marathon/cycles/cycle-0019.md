# cycle-0019

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: semantic range leakage gate

## Candidate Lemma

For a generated-OR carrier with bulk generator G_N, the correct source-side leakage parameter is not only positioned range entropy B_N but the aggregate complexity of SAT restricted to the positioned ranges. If this semantic cover is subthreshold, the claimed barely-superlinear lower bound for H_N is false; if H_N has the lower bound and q,rho<1+epsilon, then SAT has no polynomial-size nonuniform circuits.

## Definitions

- source object: H_N(x)=OR_{j in [M]} SAT(G_N(x)_j) on N input bits, where M=N^q, L=(log N)^d, and the bulk generator G_N outputs M formulas of length L with circuit size at most N^rho.
- target object: SAT on L-bit instances with nonuniform circuits of size L^c, and the target consequence SAT notin P/poly when the H_N lower bound is valid for all large N.
- controlled interface: substitution uses only the generated SAT instances and positioned range deciders D_{N,j} that agree with SAT on R_{N,j}={G_N(x)_j:x in {0,1}^N}.
- target-preserving condition: q<1+epsilon, rho<1+epsilon, d is fixed and greater than 1, the generator is bulk-shared, and no extra advice beyond the fixed nonuniform circuits D_{N,j} is leaked.

## Assumptions

- Circuit model is nonuniform Boolean SIZE with unbounded fan-in OR allowed at linear cost, or fan-in two OR at O(M) cost.
- G_N is a single circuit producing all positioned queries; a random-access generator would change the bound to include the cost of all invocations.
- C_R(SAT) denotes the minimum size of an L-input circuit agreeing with SAT on the finite set R and arbitrary outside R.
- The lower-bound premise is SIZE(H_N)>N^{1+epsilon} eventually, not merely infinitely often, unless the target consequence is weakened to i.o. SAT lower bounds.

## Equations

- semantic_upper_bound: `C(H_N) \le O\left(C(G_N)+\sum_{j\le M} C_{R_{N,j}}(\mathrm{SAT})+M L\right)`. Valid when: Valid when G_N is a bulk circuit outputting all positioned queries and circuit size counts shared generator gates once.
- global_sat_substitution: `\mathrm{SAT}\in \mathrm{SIZE}(n^c) \Rightarrow C(H_N) \le N^{\rho}+N^q (\log N)^{dc}+N^{q+o(1)}=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after the generated formulas have length L=(log N)^d and every fixed SAT circuit exponent contributes only N^{o(1)} overhead.
- magnification_consequence: `C(H_N)>N^{1+\epsilon}\ \wedge\ \max\{\rho,q\}<1+\epsilon \Rightarrow \mathrm{SAT}\notin \mathrm{P/poly}`. Valid when: Requires the lower bound for H_N to hold eventually and the target transfer to preserve nonuniform circuit size.
- semantic_gate: `C(H_N)>N^{1+\epsilon}\ \wedge\ q,\rho<1+\epsilon \Rightarrow \sum_{j\le M} C_{R_{N,j}}(\mathrm{SAT})\ge N^{1+\epsilon-o(1)}`. Valid when: Valid when q and rho are both strictly below the claimed source lower-bound exponent 1+epsilon.

## Attempted Derivation

- Let R_{N,j} be the j-th positioned range of the bulk generator G_N.
- For each j, choose a minimum L-input circuit D_{N,j} agreeing with SAT on R_{N,j}.
- Build a circuit for H_N by computing the full list G_N(x), feeding the j-th formula to D_{N,j}, and OR-ing all M outputs.
- This gives C(H_N)<=O(C(G_N)+sum_j C_{R_{N,j}}(SAT)+M L).
- If SAT has global circuits of size n^c, take every D_{N,j} to be the restriction of the L-bit SAT circuit; since L=(log N)^d, the substitution term is N^{q+o(1)}.
- Thus a valid N^{1+epsilon} lower bound for H_N with q,rho<1+epsilon refutes every fixed polynomial-size SAT circuit family.
- Conversely, the same upper bound proves that any subthreshold aggregate positioned range decider is a falsifier for the claimed source lower bound.

Blocking gap: The derivation does not supply an explicit G_N for which both H_N has a general-circuit lower bound N^{1+epsilon} and S_N=sum_j C_{R_{N,j}}(SAT) is provably above N^{1+epsilon-o(1)}.

## Falsifiers

- semantic leakage falsifier: SAT restricted to the positioned ranges has aggregate circuit complexity below N^{1+epsilon-o(1)}.
- threshold collapse: max{q,rho} reaches or exceeds 1+epsilon, so SAT substitution no longer contradicts the source lower bound.
- bulk-generator mismatch: G_N is only random-access with per-query cost N^rho, changing the positive upper bound to about N^{q+rho}.
- nonuniform leakage: the construction or proof accidentally supplies the positioned deciders D_{N,j} as advice for H_N.
- low-label-complexity range: high B_N is achieved using formulas from classes where satisfiability is easy, such as Horn, 2-CNF, bounded treewidth, or planted trivially satisfiable instances.
- natural-proof obstruction: a constructive dense certificate that many SAT range labels evade small circuits would be natural; the surviving route must be sparse, non-natural, or use a nonrelativizing proof object.
- oracle falsifier probe: if an oracle makes all generated range labels simple while preserving the black-box interface, then a relativizing proof of the semantic gate cannot be valid.

## Learning

Cycle 19 sharpens the generated-OR route: positioned entropy is not the decisive source gate. The valid bridge uses the semantic cover S_N=sum_j C_{R_{N,j}}(SAT). Subthreshold S_N is a concrete falsifier for H_N lower bounds, while q,rho<1+epsilon still gives the target-preserving implication from a valid H_N lower bound to SAT notin P/poly.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The target transfer is already quantified; the remaining uncertainty is whether positioned entropy can hide small SAT-on-range deciders, so another abstract magnification restatement would not move the proof queue.
- Situation seed: Fix d=2, epsilon=0.1, q=1.04, rho=1.03. Let a bulk expander-like G_N map x in {0,1}^N to M=N^q length-(log N)^2 3-CNF encodings, with each positioned range syntactically large enough that B_N>N^{1.1}.
- Varied variable: semantic leakage exponent sigma=log_N(sum_{j<=M} C_{R_{N,j}}(SAT)).
- Held-fixed controls: Target consequence remains SAT notin P/poly, not merely a padded carrier separation., The query length remains L=(log N)^2, so every fixed SAT circuit exponent contributes N^{o(1)}., The generator size exponent rho and query-count exponent q remain below 1+epsilon., No positioned range decider may be counted as part of the positive target-preserving transfer.
- Expected observation: If sigma<1.1, the carrier has a subthreshold circuit despite high entropy; if sigma>=1.1 is certifiable without natural-proof leakage, the generated-OR bridge remains a valid candidate route.
- Transfer certificate needed: A formal lower bound or barrier-evading certificate that SAT restricted to the positioned ranges has aggregate nonuniform circuit complexity at least N^{1+epsilon-o(1)}, together with a proof that G_N is bulk computable in size N^rho and does not leak D_{N,j} advice.

## Next Experiment

Instantiate G_N with a concrete expander or extractor-based 3-CNF generator, compute R_{N,j} structure, and test whether SAT on those positioned ranges collapses to a known easy subclass or requires a new semantic lower-bound certificate.

# Barrier audit for low-degree algebraic truth-table separators

## Candidate Lemma

Any explicit F_2 algebraic SAT truth-table separator whose accepted set is a conjunction of Boolean polynomial tests with total degree D=O(log N) is a Razborov-Rudich natural property useful against the named target circuit class. Thus low-degree algebraic syntax is not a valid natural-proof escape.

## Definitions

- source object: an explicit F_2 low-total-degree truth-table separator Q_m for SAT_m, or a conjunction P_{m,i}=1 whose product is Q_m.
- target object: a Razborov-Rudich natural property over N=2^m bit truth tables useful against SIZE(m^k).
- controlled interface: coefficients or an evaluation circuit for Q_m are generated and evaluated in poly(N), and soundness is universal over all target circuit truth tables.
- target-preserving condition: total degree D_m=O(log N), no per-circuit advice, and acceptance of SAT_m plus rejection of every SIZE(m^k) truth table are maintained.
- density convention: largeness means Pr_{Y in {0,1}^N}[R_m(Y)=1] >= N^{-O(1)}.
- usefulness convention: every truth table computed by an m-input circuit of size m^k is rejected by R_m.

## Assumptions

- N=2^m is the full truth-table length for m-bit inputs.
- Each P_{m,i} is a multilinear polynomial over F_2 in the N truth-table variables.
- The source separator accepts the SAT_m truth table and rejects every SIZE(m^k) truth table.
- The description/evaluation of the separator is uniform enough to give a poly(N)-time property tester.

## Equations

- product_test: `Q_m(Y)=\prod_{i=1}^{r} P_{m,i}(Y),\qquad \deg(Q_m)\le D_m:=\sum_i \deg(P_{m,i}).`. Valid when: Applies when the source separator is a conjunction of explicit Boolean polynomial tests on full truth tables.
- reed_muller_weight_floor: `Q_m\not\equiv 0\ \Longrightarrow\ \Pr_{Y\in\{0,1\}^{N}}[Q_m(Y)=1]\ge 2^{-\deg(Q_m)}.`. Valid when: Requires Q_m to be nonzero, which follows from accepting the SAT truth table.
- natural_largeness_threshold: `D_m\le c\log_2 N\ \Longrightarrow\ \Pr[Q_m(Y)=1]\ge 2^{-D_m}\ge N^{-c}.`. Valid when: Valid when total degree is at most a constant times log N and N is the truth-table length.
- prf_falsifier_advantage: `\operatorname{Adv}_{Q_m}(F)\ge \Pr[Q_m(U_N)=1]\ge N^{-c}`. Valid when: Applies after constructivity and usefulness are preserved against every target circuit truth table.

## Attempted Derivation

- Type the source model as explicit Boolean polynomials P_{m,i} over the N truth-table coordinates of SAT_m.
- Define Q_m as the product of all accepting constraints; SAT_m acceptance makes Q_m nonzero.
- Apply the Reed-Muller minimum-distance bound: a nonzero degree-D multilinear polynomial on {0,1}^N has weight at least 2^{-D}.
- If D=O(log N), obtain polynomial density, so the accepted set is large.
- Poly(N) evaluation of Q_m gives constructivity.
- Universal rejection of every SIZE(m^k) truth table gives usefulness against the target class.
- Therefore the proof object is a valid natural property; against PRF assumptions in SIZE(m^k), the property itself is a distinguisher with polynomial advantage.

Blocking gap: No gap remains for the low-degree-to-natural bridge once the separator is exactly this source object. The remaining gap is external: an actual lower-bound method may not admit a poly(N)-explicit low-total-degree product normal form.

## Falsifiers

- falsifier: D_m=omega(log N) makes the generic largeness lower bound too small for the standard natural-proof contradiction.
- falsifier: coefficients or evaluation of Q_m require superpolynomial time in N, destroying constructivity rather than escaping the barrier validly.
- falsifier: soundness rejects only a sampled or average subset of small circuits, not every SIZE(m^k) truth table.
- falsifier: nonuniform advice encodes the SAT truth table into Q_m, so the controlled interface leaks the target.
- falsifier: the proof only algebrizes over low-degree oracle extensions and never uses unrelativized syntax, leaving the algebrization audit unchanged.

## Learning

Cycle 19 adds a concrete barrier bridge: explicit F_2 algebraic SAT separators of total degree O(log N) are natural properties via the Reed-Muller weight floor. The valid escape threshold is superlogarithmic total degree or loss of constructivity, but those escapes need separate target-preserving and nonalgebrizing certificates.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a concrete threshold computation for algebraic nonlinear certificates, because prior cycles handled local cylinders, affine sketches, and correlation halfspaces but not low-degree polynomial varieties.
- Situation seed: For each m, imagine a padded SAT truth table T_m of length N=2^m and a separator Q_m over F_2 that accepts T_m and rejects every truth table of an m-input circuit of size m^k.
- Varied variable: total degree D_m=beta log_2 N of Q_m, with beta varied from constant to log N.
- Held-fixed controls: target class SIZE(m^k) and full-truth-table representation length N=2^m, poly(N)-time coefficient generation or evaluation for Q_m, universal soundness over all target circuit truth tables, no per-circuit or per-input advice hidden in the polynomial description
- Expected observation: For constant beta, the accepted set has density at least N^{-beta} and becomes a natural property; for beta=log N, the minimum-distance guarantee drops to N^{-log N}, so the natural-proof transfer no longer follows automatically.
- Transfer certificate needed: A formal certificate must prove Reed-Muller weight preservation, poly(N) constructivity, and target soundness; if beta is superconstant, it must also give an independent largeness or non-natural/nonalgebrizing reason before affecting the proof queue.

## Next Experiment

Audit degree-D polynomial threshold over integers or reals: determine whether bounded coefficient bit complexity plus D=O(log N) also yields a large semialgebraic natural property, or whether sign conditions can create exponentially tiny accepted sets without losing constructivity.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For a uniform sequential MCSP no-side certificate carrier V_m with threshold 2^{epsilon m}, kappa-dense carrier lengths, verification time 2^{C m}, and certificate length ell(m), the target-preserving E extraction is valid in the short-certificate window ell(m)=O(m). In that window the induced property is constructive but exponentially non-large. Making the certificate/salt long enough to reach Razborov-Rudich largeness, ell(m)>=2^m-O(m), destroys exhaustive E canonicalization and creates a natural-proofs falsifier if a poly(2^m)-time recognizer is also supplied.

## Definitions

- source object: a uniform sequential verifier V_m that on a certificate pi of length ell(m) emits a truth table y in {0,1}^{2^m} and is sound for MCSP no-instances at size 2^{epsilon m}.
- target object: an E language L whose length-n padded slice is defined from a canonical accepted y_m on kappa-dense source lengths and is intended to give SIZE(2^{delta n}) lower bounds.
- controlled interface: lexicographic certificate search plus padding across kappa-dense lengths, with verifier time 2^{O(m)} and declared block-simulation cap alpha_V.
- target-preserving condition: ell(m)=O(m), epsilon<=alpha_V+o(1), kappa=O(1), and no nonuniform advice or external table selector is used.
- N=2^m is the truth-table length for m-bit Boolean functions.
- P_m is the verifier image property, the set of emitted tables having some accepting certificate.
- Largeness means density at least 1/poly(N) among all N-bit truth tables.
- Constructivity means membership in P_m is decidable in poly(N) time, not merely by a nonuniform selector.

## Assumptions

- V_m is generated uniformly in time 2^{O(m)} and emits bits sequentially with no hidden advice.
- Every accepted output y satisfies circuit complexity CC(y)>2^{epsilon m}.
- For every sufficiently large target length n there is a carrier length m in [n/kappa,n].
- The canonical certificate is the lexicographically first accepting certificate; if none exists on a promised source length, the source fails.
- The cap audit from cycle 18 is enforced: a verifier with block-simulation cap alpha_V cannot soundly certify threshold epsilon>alpha_V+o(1).

## Equations

- image-density: `N=2^m,\quad \mathcal P_m=\{y:\exists \pi\in\{0,1\}^{\ell(m)}\ V_m(\pi)=y\},\quad |\mathcal P_m|/2^N\le 2^{\ell(m)-N}.`. Valid when: Valid when each certificate determines at most one emitted table and the property is the verifier image at length m.
- short-cert-constructivity: `\ell(m)=a m+O(1)\Rightarrow T_{decide}(\mathcal P_m)\le 2^{\ell(m)}2^{C m}=N^{a+C+o(1)}.`. Valid when: Valid when the verifier runs in 2^{C m} time and exhaustive search over all certificates is the recognizer.
- largeness-threshold: `|\mathcal P_m|/2^N\ge N^{-d}\Rightarrow \ell(m)\ge N-dm.`. Valid when: Valid when largeness is measured as inverse-polynomial density in truth-table length in the Razborov-Rudich sense.
- E-canonicalization-window: `m\in[n/\kappa,n],\ \ell(m)=O(m)\Rightarrow T_L(n)\le 2^{O(n)}.`. Valid when: Valid when the target language pads the canonical m-bit carrier to length n and carrier lengths are kappa-dense.
- padded-lower-bound-transfer: `CC(y_m)>2^{\epsilon m},\ m\ge n/\kappa\Rightarrow L\notin SIZE(2^{\delta n})\text{ for every }\delta<\epsilon/\kappa.`. Valid when: Valid when padding preserves lower bounds by fixing extra inputs and epsilon passes the block-simulation cap audit.

## Attempted Derivation

- Fix N=2^m and let P_m be the set of truth tables emitted by accepting certificates of length ell(m).
- Cardinality gives |P_m|<=2^{ell(m)}, independent of the semantic high-MCSP soundness claim.
- If ell(m)=O(m), exhaustive recognition of P_m costs 2^{O(m)}=poly(N), so the property is constructive; its density is at most 2^{-N+O(m)}, so it is not large.
- The same exhaustive search canonically selects a table in 2^{O(m)} time, and padding from a carrier m in [n/kappa,n] keeps the target language in E.
- No-side soundness transfers through padding: a size 2^{delta n} circuit for L_n with delta<epsilon/kappa would restrict to a circuit below 2^{epsilon m} for y_m.
- If ell(m)>=N-O(m), cardinality can reach the largeness threshold, but exhaustive canonicalization costs about 2^N=2^{2^m}, not E; a separate poly(N)-recognizer would naturalize the proof object.

Blocking gap: The derivation is conditional on existence of a sparse sound verifier with threshold epsilon and declared alpha_V. It does not construct the non-enumerative high-MCSP certificate source.

## Falsifiers

- falsifier: ell(m)=omega(m) with only exhaustive selection moves the target computation out of E, even if MCSP soundness is true.
- falsifier: ell(m)>=2^m-O(m) plus a poly(2^m)-time useful recognizer creates a natural-proofs obstruction rather than a valid unconditional route.
- falsifier: epsilon>alpha_V+o(1) contradicts the block-simulation cap and invalidates the claimed MCSP no-side threshold.
- falsifier: a nonuniform selector for the accepted table proves only an advice-based lower-bound carrier, not the target-preserving E object.
- falsifier: adding random salt to increase density without a canonical short selector destroys explicitness and cannot be used in the valid bridge.

## Learning

Cycle 19 isolates a certificate-length trichotomy. Short O(m)-bit MCSP certificates give a valid E-compatible, constructive but non-large carrier image. Superlinear certificates already break exhaustive E canonicalization, and near-N salt is the exact point where largeness can appear, creating a natural-proofs falsifier if constructivity is restored. Thus random-salt density repairs are quarantined; the remaining viable route is a sparse, canonical, non-natural, cap-aware short-certificate source.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete falsifier probe now.`
- Rationale: The route's next risk is a tempting salt-based repair: increase the carrier image until it looks plentiful. The length-window calculation decides whether that repair preserves the E transfer or merely naturalizes the object.
- Situation seed: Consider a salted sequential MCSP carrier V_{m,ell}: a core O(m)-bit certificate plus ell(m) salt bits emits one N=2^m bit truth table, and soundness asserts every accepted emitted table has circuit complexity greater than 2^{epsilon m}.
- Varied variable: Certificate/salt length ell(m), varied from O(m) through omega(m) up to N-O(m).
- Held-fixed controls: MCSP no-side threshold 2^{epsilon m} with constant epsilon., Carrier lengths are kappa-dense with fixed kappa., Verifier stream time is 2^{C m} and has declared block cap alpha_V., No external truth-table selector, advice string, or oracle is allowed., Target consequence remains an advice-free E lower bound with delta<epsilon/kappa.
- Expected observation: At ell=O(m), canonical extraction is in E and the image property is constructive but far below largeness. At ell=N-O(m), largeness becomes possible, but exhaustive selection is double-exponential in m and any separate poly(N) useful recognizer enters the natural-proofs danger zone. No intermediate ell gives both E extraction and largeness by cardinality alone.
- Transfer certificate needed: A valid transfer requires a proof of short-certificate existence, high-MCSP soundness at epsilon<=alpha_V+o(1), uniform lexicographic selection in 2^{O(m)}, and kappa-dense padding; without these certificates the salt intuition stays quarantined.

## Next Experiment

Audit a concrete candidate source based on proof transcripts of hard truth-table generation: compute its certificate length, stream time, alpha_V block profile, and whether soundness is non-enumerative rather than a disguised MCSP brute-force check.
