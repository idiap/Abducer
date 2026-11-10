# cycle-0028

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the polylog-query generated-OR carrier, any subthreshold ensemble of one-sided list selectors plus selected-image SAT solvers gives a circuit for H_N. Thus a valid N^{1+epsilon} source lower bound must beat ensemble cover complexity, not merely every single approximate list selector.

## Definitions

- source object: H_N:{0,1}^N -> {0,1}, H_N(x)=OR_{j in [N^q]} SAT(G_N(x,j)), with query length L=(log N)^d and generator access cost N^rho.
- target object: nonuniform SAT circuits on L-bit formulas, used to conclude SAT notin P/poly if a valid H_N lower bound contradicts every fixed SAT exponent.
- controlled interface: selected-query access to G_N, list selectors A_i(x), and selected-image SAT promise solvers B_i with no advice depending on x beyond the H_N input.
- target-preserving condition: d>1 and max{rho,q}<1+epsilon, so substituting any fixed polynomial SAT circuit costs only N^{o(1)} per generated query.
- ensemble compressor: R selectors A_i of size S_i output lists of length at most K_i, with solvers B_i of size T_i correct for SAT on V_i={G_N(x,j): j in A_i(x)}.
- success cover: the union over i of inputs where A_i lists at least one satisfiable generated formula covers all but E positive H_N inputs.

## Assumptions

- M=N^q and L=(log N)^d with d>1; G_N is target-clean and has reusable selected-query circuitry of size N^rho.
- Each B_i is a promise solver only on its selected image V_i, but it must be SAT-correct there on both satisfiable and unsatisfiable formulas.
- For negative H_N inputs, one-sidedness is automatic because all generated formulas are unsatisfiable and B_i is correct on V_i.
- The E uncovered positive inputs may be patched by equality gates of total size O(NE), explicitly charging nonuniform leakage.

## Equations

- generated_or_definition: `\(H_N(x)=\bigvee_{j\in[M]} SAT(G_N(x,j)),\quad M=N^q,\quad L=(\log N)^d.\)`. Valid when: Valid when the source generator is explicitly named and the H_N input length is N.
- ensemble_cover_upper_bound: `\(C(H_N)\le O\left(N^\rho+\sum_{i=1}^R(S_i+K_i(T_i+N^{o(1)}))+NE\right).\)`. Valid when: Applies when each selected-image solver is correct and residual positives are patched by equality circuits.
- exponent_form: `\(R\le N^\theta,\ S_i\le N^\alpha,\ K_i\le N^\lambda,\ T_i\le N^\tau,\ E\le N^\delta\Rightarrow C(H_N)\le N^{\max\{\rho,\theta+\alpha,\theta+\lambda+\tau,1+\delta\}+o(1)}.\)`. Valid when: Requires uniform exponent bounds for every ensemble member and polylogarithmic generator overhead.
- target_all_query_special_case: `\(SAT\in SIZE(n^c)\Rightarrow C(H_N)\le N^{\max\{\rho,q\}+o(1)}.\)`. Valid when: Valid when the selector lists all N^q queries and L^c=N^{o(1)} for fixed c.

## Attempted Derivation

- Fix H_N(x)=OR_j SAT(G_N(x,j)) with M=N^q and L=(log N)^d.
- Given an ensemble, build C_i(x)=OR_{j in A_i(x)} B_i(G_N(x,j)) for each selector-solver pair.
- If H_N(x)=0, every generated formula is unsatisfiable, so all C_i(x)=0 by selected-image correctness.
- If H_N(x)=1 and x is covered, some C_i(x)=1 because its list contains a satisfiable generated formula.
- Patch the E uncovered positive strings by an equality-DNF of size O(NE).
- Share the generator access circuitry once and sum selector, solver-copy, and patch costs to obtain the ensemble upper bound.
- Under SAT in SIZE(n^c), choose one selector listing all N^q indices and recover C(H_N)<=N^{max{rho,q}+o(1)}.

Blocking gap: No lower-bound method is known for Xi_N^{ens} against fully nonuniform selected-image promise solvers; ensemble covers can exploit semantic clusters invisible to entropy counts.

## Falsifiers

- falsifier: an ensemble of N^theta list selectors with theta+lambda+tau<1+epsilon and residual E<N^{epsilon-o(1)} collapses the source lower bound.
- falsifier: selected-image SAT is promise-easy even though unrestricted SAT on L-bit formulas is hard.
- falsifier: q>=1+epsilon or rho>=1+epsilon causes quantitative threshold collapse in the target bridge.
- falsifier: a natural dense property proving Xi_N^{ens} large would collide with standard natural-proofs concerns unless it is generator-specific and non-natural.
- falsifier: hidden advice in selectors depending on x beyond the input circuit model invalidates target preservation.

## Learning

Cycle 28 identifies an additional leakage mode: many imperfect list selectors can collectively cover the positive fiber. The valid source audit is the ensemble cover complexity Xi_N^{ens}; single-selector minimax lower bounds are insufficient for this generated-OR magnification route.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a quantitative test of the new ensemble-cover gate; another abstract hardness-magnification slogan would not distinguish real source hardness from nonuniform leakage.
- Situation seed: Generated-OR carrier H_N with M=N^q generated SAT formulas of length L=(log N)^d, d>1, where each ensemble member selects a short list of candidate formulas and uses a promise solver on its selected image.
- Varied variable: ensemble size exponent theta in R=N^theta, with list exponent lambda and selected-image solver exponent tau recorded in the transfer inequality.
- Held-fixed controls: q<1+epsilon and rho<1+epsilon so the target bridge remains valid., d>1 so fixed polynomial SAT circuits contribute only N^{o(1)} per query., Selected-image solvers must be SAT-correct on their promised ranges; false positives are not allowed., Residual positive exceptions are charged by O(NE) equality correction.
- Expected observation: If theta+lambda+tau or theta+alpha falls below 1+epsilon while the ensemble covers almost all positives, H_N has subthreshold circuits; if every such ensemble leaves more than N^{epsilon-o(1)} residual positives, the source lower-bound route survives this leakage test.
- Transfer certificate needed: A formal lower bound Xi_N^{ens}>N^{1+epsilon-o(1)} for the explicit generator, plus verification that the all-query selector under SAT in P/poly still gives the valid N^{max{rho,q}+o(1)} upper bound.

## Next Experiment

Estimate Xi_N^{ens} for a random high-entropy generator by a union-bound model over ensembles, then isolate which part of the argument can survive explicitness and avoid natural-proof leakage.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Let N=2^m and let F_N:{0,1}^N->{0,1} be a total separator with F_N(T_m)=1 for the SAT_m truth table and F_N(y)=0 for every y in TT(SIZE(m^k)). If global block sensitivity bs(F_N)<=b_N and the positive certificate at T_m is uniformly computable in poly(N) or hardwirable as allowed advice, then F_N induces a natural property of density at least 2^{-b_N^2} useful against SIZE(m^k). In particular b_N<=sqrt(a log_2 N) is a valid natural-proof threshold, so low global block sensitivity is not a barrier escape.

## Definitions

- source object: total Boolean separator family F_N on truth-table space {0,1}^N, with named source model global block sensitivity bs(F_N)<=b_N and acceptance of the SAT_m truth table T_m.
- target object: Razborov-Rudich style property P_N subset {0,1}^N, constructive in poly(N) with uniform generation or fixed advice, large at density N^{-O(1)}, and useful against m-input circuits of size m^k.
- controlled interface: extract a positive certificate for F_N at T_m using the total-function inequality C_1(F_N,T_m)<=bs(F_N)^2, then use its accepting subcube as P_N.
- target-preserving condition: F_N must reject every truth table in TT(SIZE(m^k)), and the certificate extraction/advice must not add nonuniform leakage that weakens this rejection guarantee.

## Assumptions

- N=2^m and T_m is the full truth table of SAT on m-bit encodings.
- F_N is total; the certificate-block-sensitivity inequality is not asserted for partial or promise separators.
- F_N(T_m)=1 and F_N rejects all truth tables computed by circuits of size at most m^k.
- The certificate coordinates and values are either found in poly(N) or supplied as hardwirable advice compatible with the natural-proof audit.
- The target class is the named nonuniform class SIZE(m^k), not an unspecified hardness slogan.

## Equations

- certificate_from_block_sensitivity: `C_1(F_N,T_m) \le bs(F_N)^2 \le b_N^2`. Valid when: Valid when F_N is a total Boolean function on truth tables and b_N bounds global block sensitivity.
- subcube_density: `\mu(P_N)=2^{-C_1(F_N,T_m)} \ge 2^{-b_N^2}`. Valid when: Applies after a positive certificate at T_m is fixed and all its extensions remain accepted by F_N.
- polynomial_largeness_threshold: `b_N \le \sqrt{a\log_2 N}\ \Rightarrow\ \mu(P_N)\ge N^{-a}`. Valid when: Requires the block-sensitivity threshold to be measured against the truth-table length N, not the formula length m.
- usefulness_transfer: `P_N \cap TT(SIZE(m^k))=\varnothing`. Valid when: Valid when the separator rejects every m-input circuit of size at most m^k before certificate restriction.

## Attempted Derivation

- Fix m, N=2^m, target class TT(SIZE(m^k)), and a total separator F_N accepting T_m and rejecting every target truth table.
- Invoke Nisan's total-function inequality C(F_N,x)<=bs(F_N)^2 at x=T_m to obtain a positive certificate rho of size t<=b_N^2.
- Define P_N={y in {0,1}^N : y extends rho}. Then mu(P_N)=2^{-t}.
- Since rho is a 1-certificate, P_N is contained in F_N^{-1}(1). Since F_N rejects TT(SIZE(m^k)), P_N avoids TT(SIZE(m^k)).
- If b_N<=sqrt(a log_2 N), then P_N has density at least N^{-a}; with uniform or hardwired certificate access it is constructive in poly(N).

Blocking gap: The proof is conditional on totality and certificate constructivity/advice. It does not rule out high-block-sensitivity, partial, nonconstructive, or nonuseful separators.

## Falsifiers

- Singleton equality E_T is a falsifier for average-block-sensitivity or average-sensitivity naturalization claims: tiny average boundary can coexist with density 2^{-N}.
- Partial separators are a falsifier for direct use of C<=bs^2; the inequality is valid only for total Boolean functions unless a separate promise-to-total extension is supplied.
- A separator with bs(F_N)=(log N)^{0.6} passes low-looking qualitative descriptions but fails the polynomial-density threshold because 2^{-bs^2}=N^{-omega(1)}.
- If the certificate is found only by superpolynomial search and cannot be hardwired under the route's model, the uniform natural-proof transfer is invalid.
- If F_N rejects only most small circuits rather than all TT(SIZE(m^k)), the accepting subcube may contain target circuits and usefulness is lost.

## Learning

Cycle 28 proves a route-level bridge: total SAT truth-table separators with global block sensitivity at most sqrt(O(log N)) naturalize via C<=bs^2, yielding polynomial-density properties useful against the same SIZE(m^k) target. The valid escape is high global block sensitivity, partiality, nonconstructive certificate selection, or failed usefulness. Average boundary parameters are quarantined by the singleton equality falsifier. This is barrier progress only, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for low-complexity separator routes.`
- Rationale: The branch has many naturalization gates; block sensitivity is a standard complexity measure not yet audited, and its exact sqrt(log N) threshold gives a concrete transfer certificate rather than another folklore barrier citation.
- Situation seed: A padded SAT truth-table separator family F_N over N=2^m bits, promised to accept T_m and reject every truth table of m-input circuits of size m^k, with total Boolean behavior outside the target set.
- Varied variable: The global block-sensitivity exponent gamma in b_N=(log N)^gamma.
- Held-fixed controls: Totality of F_N on all truth tables, so the certificate-block-sensitivity inequality applies., Full usefulness against TT(SIZE(m^k)), not average-case rejection., Constructivity via poly(N) certificate generation or explicitly allowed hardwired advice., Target length convention N=2^m and fixed circuit-size exponent k.
- Expected observation: For gamma<=1/2 the accepting certificate has size O(log N) and yields a polynomial-density natural property; for gamma>1/2 the density becomes N^{-omega(1)}, so natural-proof largeness no longer follows from this bridge.
- Transfer certificate needed: A formal certificate extractor or advice policy preserving poly(N) decidability, plus a proof that the accepting subcube remains disjoint from TT(SIZE(m^k)).

## Next Experiment

Audit low decision-tree-rank or low alternation-depth separators: determine whether they force small positive certificates at T_m, or whether parity/equality-style examples provide the next falsifier.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Let V_m be a uniform linear-certificate MCSP carrier: certificates y of length at most c m are checked and streamed in 2^{O(m)} time, and each accepted y names a truth table T_{m,y}:{0,1}^m -> {0,1}. On a kappa-dense uniform length set M, assume A_m={y:V_m accepts y} is nonempty and contains some y with circuit complexity greater than 2^{epsilon m}. If r_m=ceil(log_2 |A_m|) and H=limsup_{m in M} r_m/m, then canonical multiplexing gives an E language with circuit lower bound exponent every delta<epsilon/(kappa(1+H)). This is a valid route-level bridge, not a proof of P != NP.

## Definitions

- source object: a uniform MCSP certificate carrier V_m with O(m)-bit-to-cm-bit certificates, accepted set A_m, emitted table T_{m,y}, source hardness threshold CC(T_{m,y})>2^{epsilon m}, and verifier cap alpha_V.
- target object: an E-uniform padded multiplexer language L whose unpadded special lengths are n_m=m+r_m and whose desired consequence is SIZE(2^{delta n}) lower bounds on all sufficiently large lengths.
- controlled interface: lexicographic counting and unranking of accepted certificates, followed by address-bit multiplexing F_m(a,x)=T_{m,y_a}(x), with exhaustive uniform computation allowed in 2^{O(n)} time.
- target-preserving condition: M is kappa-dense and E-uniform, certificate length is O(m), H<infinity, epsilon<=alpha_V, and no nonuniform advice is used to select m, count A_m, or choose the hard accepted certificate.

## Assumptions

- V_m is deterministic and uniformly constructible from 1^m in time 2^{O(m)}.
- For every m in M, there exists at least one accepted certificate y in A_m with CC(T_{m,y})>2^{epsilon m}.
- The length set M is kappa-dense: for consecutive m_i<m_{i+1} in M, m_{i+1}<=kappa m_i for all large i.
- The accepted-set entropy profile satisfies r_m<= (H+o(1))m along M.
- The verifier implementation does not itself imply circuits of exponent below epsilon for every emitted table; formally epsilon<=alpha_V after the branch's checkpoint-cap audit.

## Equations

- accepted_entropy: `r_m=\lceil \log_2 |A_m|\rceil,\qquad H=\limsup_{m\in M}\frac{r_m}{m}.`. Valid when: Valid when accepted certificates are finite, uniformly enumerable, and certificate length is linear in m.
- multiplexer_length: `n_m=m+r_m\le (1+H+o(1))m.`. Valid when: Applies on the kappa-dense source lengths after the entropy profile is bounded asymptotically.
- slice_transfer: `CC(F_m)\ge 2^{\epsilon m}-O(n_m).`. Valid when: Requires that some accepted certificate is hard and its address can be hardwired into any circuit for the multiplexer.
- all_length_exponent: `\delta<\frac{\epsilon}{\kappa(1+H)}.`. Valid when: Applies after padding from kappa-dense source lengths and after preserving E-uniform length selection.

## Attempted Derivation

- For each m in M, enumerate A_m in lexicographic order by exhaustive scan of all O(m)-length certificates; this is E-uniform because the scan costs 2^{O(m)}.
- Define F_m(a,x)=T_{m,y_a}(x), where |a|=r_m and |x|=m; invalid addresses output 0 if |A_m| is not a power of two.
- Let y_* be an accepted hard witness. If F_m had a circuit C of size S, hardwire the address a_* of y_* and obtain a circuit of size S+O(m+r_m) for T_{m,y_*}.
- Therefore S>=2^{epsilon m}-O(n_m), and since n_m<= (1+H+eta)m for large m, special-length lower bounds have any exponent below epsilon/(1+H).
- Pad from consecutive source lengths m_i to all target lengths. Since m_{i+1}<=kappa m_i and n_{m_{i+1}}<= (1+H+eta)m_{i+1}, any padded length N in the next interval satisfies N<=kappa(1+H+eta)m_i.
- Thus any all-length circuit exponent delta<epsilon/(kappa(1+H)) would contradict the hard source slice for large i.
- Uniformity is preserved by recomputing the largest eligible source length and accepted-set count in 2^{O(N)} time; no advice chooses the witness.

Blocking gap: The bridge is now mathematically valid, but it assumes a source construction with constant epsilon, finite H, kappa-dense uniform lengths, and epsilon below the verifier cap. No such non-natural MCSP certificate source is constructed here.

## Falsifiers

- falsifier: accepted-set entropy H is unbounded or grows so that r_m/m has no finite limsup on the dense source set.
- falsifier: the source length set is only nonuniformly specified, preventing E-uniform padding and target parsing.
- falsifier: verifier checkpoint or restart leakage gives alpha_V<epsilon, contradicting the claimed MCSP no-side threshold.
- falsifier: certificate length is omega(m), making exhaustive canonical unranking incompatible with the E target interface.
- falsifier: the carrier uses a large constructive dense property of truth tables, re-entering the natural-proofs obstruction rather than the sparse non-natural route.

## Learning

Cycle 28 separates three parameters that were partly conflated: certificate length c affects only E-uniform computation, accepted-set entropy H gives the exact multiplexing rate loss, and verifier cap alpha_V bounds the admissible source threshold epsilon. The valid bridge is delta<epsilon/(kappa(1+H)); the unresolved task is constructing a uniform low-entropy, cap-compatible, non-natural MCSP source.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The bridge now has a sharp formula, so the remaining uncertainty is quantitative: whether low accepted entropy can coexist with cap-compatible constant MCSP hardness without leaking a small circuit.
- Situation seed: Consider a family V_m that accepts exactly 2^{h m} certificates, each certificate selecting one row of a sequentially generated MCSP-hard-looking table family, and suppose one accepted row-table has claimed complexity above 2^{epsilon m}. Build the canonical multiplexer over the accepted certificates and pad from a kappa-dense set of m.
- Varied variable: accepted-set entropy rate h in [0,c], holding epsilon, kappa, certificate length constant c, and verifier cap alpha_V fixed.
- Held-fixed controls: V_m is E-uniform and has O(m)-length certificates., The source length set M is kappa-dense and uniformly searchable., The claimed hard accepted witness has threshold CC(T)>2^{epsilon m}., The verifier cap audit gives epsilon<=alpha_V., No advice or external selector identifies the hard accepted certificate.
- Expected observation: As h increases, the transferred target exponent should fall as delta<epsilon/(kappa(1+h)); if the construction needs h approaching c or unbounded entropy to hide contamination, the route loses quantitative strength but remains valid only while H is finite.
- Transfer certificate needed: A formal source certificate proving both low entropy |A_m|<=2^{h m+o(m)} and existence of an accepted table with MCSP threshold 2^{epsilon m}, while also proving that the verifier's sequential implementation has no checkpoint cap below epsilon.

## Next Experiment

Audit a sequential proof-complexity-style carrier where certificates are short refutations of small-circuit hypotheses for a table prefix; compute its accepted entropy h, checkpoint cap alpha_V, and whether soundness proves an MCSP threshold without enumerating all small circuits.
