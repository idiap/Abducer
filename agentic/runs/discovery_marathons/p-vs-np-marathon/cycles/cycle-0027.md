# cycle-0027

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: approximate list-selector leakage gate

## Candidate Lemma

For the generated-OR carrier H_N, any subthreshold approximate list selector plus a promise SAT solver on its selected image is a concrete falsifier of an N^{1+epsilon} general-circuit source lower bound. Thus a valid route lower bound must prove a minimax lower bound against list selectors, not only against single witness selectors or semantic range covers.

## Definitions

- source object: H_N(x)=OR_{j<M_N} SAT(G_N(x,j)) on N-bit inputs, with M_N=N^q, SAT query length L_N=(log N)^d for fixed d>1, and batched generator circuit size at most N^rho.
- target object: SAT on L_N-bit formulas; the target consequence of a valid H_N lower bound is SAT notin P/poly when q,rho<1+epsilon and the bridge holds for every fixed SAT circuit exponent.
- controlled interface: a target SAT circuit of size L_N^c is substituted only through the generated query list, giving H_N circuits of size N^{max{rho,q}+o(1)} and no uncharged advice.
- target-preserving condition: q<1+epsilon, rho<1+epsilon, d>1, and every selector, promise solver, selected generator, and exception table used to simplify H_N is charged in the same nonuniform SIZE model.
- An approximate t-list selector A_N outputs at most t_N=N^tau indices. Its miss set E_A contains x with H_N(x)=1 but no selected index j has SAT(G_N(x,j))=1, together with points where the selected-image solver is wrong after composition.
- The selected image U_A is {G_N(x,j): x in {0,1}^N and j appears in A_N(x)}. A promise solver S_N is valid on U_A if it agrees with SAT on every formula in U_A, or outside an explicitly charged exceptional preimage set.

## Assumptions

- epsilon>0 is fixed and the claimed source lower bound is C(H_N)>N^{1+epsilon-o(1)} in unrestricted nonuniform circuits.
- The batched generator interface can expose all selected formulas with cost N^rho+N^{tau+o(1)}; if only per-query generation is available, replace rho by rho+tau in the leakage bound.
- A_N has circuit size N^a, S_N has circuit size N^b as measured after restricting to L_N-bit formulas but parameterized by N, and |E_A|<=N^delta.
- The exception correction circuit may use nonuniform equality advice for E_A and costs O(N|E_A|).

## Equations

- target_substitution_bridge: `SAT_{L_N}\in SIZE(L_N^c) \Rightarrow C(H_N)\le N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when the source carrier uses the named batched generator interface and c,d are fixed constants.
- list_selector_leakage_bound: `C(H_N)\le O(C(A_N)+C(G_N^{batch})+t_N(C(S_N)+L_N^{O(1)})+N|E_A|)`. Valid when: Applies when the selected formulas are generated inside the same nonuniform circuit and all selector errors are explicitly corrected.
- exponent_form_batched: `C(H_N)\le N^{\max\{a,\rho,\tau+b,1+\delta\}+o(1)}`. Valid when: Valid when G_N has batched cost N^rho independent of the chosen list length exponent tau.
- source_obligation_minimax: `\Lambda_N^{list}(\tau,\delta):=\min_{A,S,E}\big(C(A)+C(G_N^{batch})+t_NC(S)+N|E|\big)>N^{1+\epsilon-o(1)}`. Valid when: Requires the lower-bound proof to quantify over all nonuniform selectors, solvers, and exception sets in the source model.

## Attempted Derivation

- Start with an approximate t-list selector A_N and attempt to pick the lexicographically first selected satisfiable query.
- To choose that index the circuit must know SAT labels on all selected formulas, so the reduction imports a promise solver S_N on U_A.
- Once S_N is imported, the decision circuit ORs the t answers and no longer needs a single witness index.
- The cost is C(A_N)+t_N C(S_N)+exception correction, which can be subthreshold even if every single selector is hard.

Blocking gap: Witness canonicalization is semantic; it is not available from the selector circuit alone and can be bypassed by list-wise OR evaluation.

## Falsifiers

- Approximate list selector falsifier: max{a,rho,tau+b,1+delta}<1+epsilon yields a small circuit for H_N.
- Target threshold falsifier: q>=1+epsilon or rho>=1+epsilon destroys the magnification implication even if the source lower bound is true.
- Generator-interface falsifier: if selected generation costs N^{rho+tau} rather than N^rho, all exponent inequalities must be recomputed before calling the bridge valid.
- Promise-range falsifier: SAT may be easy on the selected image U_A although hard on the full generated range.
- Exception-leakage falsifier: |E_A|<=N^delta with delta<epsilon is removable by equality advice at cost below the claimed lower-bound threshold.

## Learning

Cycle 27 upgrades the source audit from approximate single selectors to approximate list selectors. The valid target-preserving bridge is unchanged, but a short list plus a promise solver can decide H_N without computing a canonical witness. Therefore any contribution-making lower-bound attempt must lower-bound Lambda_N^{list}; otherwise the route has a concrete nonuniform-leakage falsifier.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the generated-OR carrier.`
- Rationale: The current route has a valid target transfer, so the live risk is source-side nonuniform leakage through small lists of candidate queries rather than another hardness-magnification restatement.
- Situation seed: Fix H_N(x)=OR_{j<N^q} SAT(G_N(x,j)) with L_N=(log N)^d, d>1. Imagine G_N partitions positive inputs so that each positive x has many satisfying generated queries, but a compact selector A_N outputs a short hash-defined list hitting one satisfiable query on all but N^delta positives.
- Varied variable: The list length exponent tau in t_N=N^tau.
- Held-fixed controls: q<1+epsilon and rho<1+epsilon, so the target substitution bridge remains valid., SAT query length L_N=(log N)^d with d>1, so exhaustive truth-table lookup is not subthreshold., All selector circuits, promise solvers, batched generators, and exception tables are charged in nonuniform SIZE., The claimed source lower bound remains C(H_N)>N^{1+epsilon-o(1)}.
- Expected observation: As tau increases, the selected image U_A may become SAT-promise-easy before tau+b reaches epsilon. If max{a,rho,tau+b,1+delta}<1+epsilon, H_N collapses below the source threshold despite high full-range semantic entropy.
- Transfer certificate needed: A formal lower bound Lambda_N^{list}(tau,delta)>N^{1+epsilon-o(1)} for every subthreshold tau and delta, plus a batched-generation certificate showing no uncharged advice or per-query tax changes the exponent accounting.

## Next Experiment

Instantiate G_N with a high-entropy expander/hash-generated SAT family and compute whether any tau=O(epsilon/2) list selector has a selected image admitting a subthreshold promise solver.

# Barrier-Aware Lower-Bound Route: global-sensitivity naturalization gate

## Candidate Lemma

Let R_N:{0,1}^N->{0,1} be a poly(N)-constructive truth-table property with global sensitivity s_N. If R_N accepts TT(SAT_m), rejects every truth table computed by SIZE(m^k), N=2^m, and the sensitivity-certificate bound B(s_N) is O(log N), then R_N is a valid Razborov-Rudich natural property useful against SIZE(m^k). Thus any SAT lower-bound route whose proof object is such an R_N is blocked by the natural-proof/PRF falsifier unless it is non-large, nonconstructive, non-useful, or outside the PRF regime.

## Definitions

- source object: A total Boolean property R_N over N-bit truth tables, decidable in poly(N), with global sensitivity s_N=max_x |{i:R_N(x) != R_N(x^i)}|.
- target object: The set TT(SIZE(m^k)) of N-bit truth tables of m-input Boolean functions computed by circuits of size at most m^k, with N=2^m.
- controlled interface: R_N(TT(SAT_m))=1 and R_N(y)=0 for every y in TT(SIZE(m^k)); no promise inputs are allowed.
- target-preserving condition: The truth-table encoding, constructivity algorithm, and sensitivity bound are uniform in N, and padding/advice cannot change the rejected target class.

## Assumptions

- Use a sensitivity-to-certificate theorem giving C_1(R_N,x) <= B(s_N) for every accepted input x.
- For an elementary unconditional version, B(s)=s 2^{s-1}, enough when s_N <= log_2 log_2 N - log_2 log_2 log_2 N - O(1).
- For a sharper version, insert any established polynomial bound B(s)=s^h from sensitivity/certificate-complexity inequalities; the exact exponent h must be cited before use.
- Usefulness is full: every SIZE(m^k) truth table is rejected, not merely most circuits or a sampled subfamily.

## Equations

- positive_certificate_bound: `C_1(R_N,TT(SAT_m)) \le B(s_N)`. Valid when: Valid when R_N is total over all N-bit truth tables and s_N bounds global sensitivity.
- accepting_subcube_density: `\mu_N(R_N^{-1}(1)) \ge 2^{-C_1(R_N,TT(SAT_m))} \ge 2^{-B(s_N)}`. Valid when: Valid when the positive certificate fixes coordinates and every extension remains accepted by R_N.
- natural_largeness_threshold: `B(s_N) \le a\log_2 N \implies \mu_N(R_N^{-1}(1)) \ge N^{-a}`. Valid when: Applies when the certificate-size threshold is logarithmic in the full truth-table length N.
- elementary_sensitivity_threshold: `B(s)=s2^{s-1};\quad s_N2^{s_N-1}=O(\log N) \implies \mu_N(R_N^{-1}(1))\ge N^{-O(1)}`. Valid when: Valid when using the elementary sensitivity-to-certificate bound without invoking sharper sensitivity theorems.

## Attempted Derivation

- Fix N=2^m and x*=TT(SAT_m).
- Assume R_N is total, poly(N)-constructive, R_N(x*)=1, and R_N rejects TT(SIZE(m^k)).
- Apply a sensitivity-to-certificate theorem to obtain a set I of at most B(s_N) coordinates such that every y agreeing with x* on I satisfies R_N(y)=1.
- The accepting cylinder {y:y_I=x*_I} has uniform density 2^{-|I|} >= 2^{-B(s_N)}.
- If B(s_N)<=a log_2 N, the property has density at least N^{-a}; constructivity is already poly(N), and usefulness is exactly the rejection of TT(SIZE(m^k)).
- Therefore the route produces a valid natural property useful against SIZE(m^k), not a P != NP proof.

Blocking gap: The derivation does not rule out high-sensitivity, nonconstructive, non-large, or nonblack-box separators; it only quarantines low-global-sensitivity proof objects. The sharper polylog-sensitivity threshold needs a cited certificate bound exponent h.

## Falsifiers

- Singleton equality to TT(SAT_m) has poly(N) constructivity and tiny average sensitivity but density 2^{-N}; it is a falsifier to influence-only naturalization.
- A separator whose sensitivity bound holds only at TT(SAT_m) is not enough unless it yields an actual positive certificate; local stability can hide an exponentially small accepting component.
- Padding that changes N without preserving rejection of TT(SIZE(m^k)) is invalid target transfer, not a barrier escape.
- If pseudorandom functions exist in SIZE(m^k) with the relevant security, any polynomial-density constructive useful R_N is a natural-proof falsifier for the route.

## Learning

Cycle 27 adds a valid route-level bridge: total explicit SAT separators with sufficiently low global sensitivity contain a logarithmic positive certificate at the SAT truth table, hence a polynomial-density accepting subcube useful against the same named circuit class. Average sensitivity is not enough; singleton equality to the SAT truth table is the falsifier. This is barrier progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and threshold calculator.`
- Rationale: The branch has many local-certificate gates; global sensitivity is a different stability parameter that could be mistakenly advertised as a non-natural escape. It needs a concrete transfer threshold.
- Situation seed: PaddedSAT_{m,b} truth table of length N=2^{m+b}, indexed by a formula string and b dummy padding bits, with a putative property R_N accepting PaddedSAT_{m,b} and rejecting every SIZE((m+b)^k) truth table.
- Varied variable: Global sensitivity sigma(N) of R_N, compared with the certificate threshold B(sigma)=Theta(log N).
- Held-fixed controls: R_N is decidable in poly(N) with no advice depending on the target circuit., Usefulness is full rejection of all SIZE((m+b)^k) truth tables under the padded encoding., The padding map is uniform and does not change which truth tables count as target easy functions., The accepted source object remains the single padded SAT truth table for the chosen m,b.
- Expected observation: When B(sigma)<=O(log N), the accepted padded SAT point contains a polynomial-density accepting subcube, so the proof object naturalizes despite padding. When B(sigma)>>log N, this gate becomes inconclusive rather than positive evidence for P != NP.
- Transfer certificate needed: A formal certificate-extraction theorem for total R_N plus a proof that the extracted accepting subcube is still useful against the fixed padded target class.

## Next Experiment

Audit monotone or unate SAT-separator properties: determine whether monotonicity plus acceptance of TT(SAT_m) yields an isoperimetric density lower bound strong enough to naturalize, or whether singleton/up-set counterexamples quarantine the route.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Entropy-aware multiplexing bridge: a uniform MCSP certificate source with accepted-set entropy h, existential no-side hardness 2^{epsilon m}, and kappa-dense source lengths yields an E-uniform target family with circuit lower-bound exponent any delta < epsilon/((1+h)kappa), subject to the verifier cap epsilon <= alpha_V.

## Definitions

- source object: A uniform MCSP-certificate verifier V which, on length m, has an accepted set A_m of O(m)-bit certificates; at least one y in A_m emits a truth table T_y with circuit complexity greater than 2^{epsilon m}.
- target object: An E-uniform multiplexed language F on n_m=m+ell_m input bits, later padded to all target lengths, with circuit lower bound 2^{delta n}.
- controlled interface: Lexicographic accepted-certificate unranking maps row index a to y_a, and F_m(a,z)=T_{y_a}(z) while rows beyond |A_m| are filled with zero.
- target-preserving condition: V, the entropy bound ell_m<=h m+O(1), the source length schedule, and padding map are uniform, and the reduction preserves density, threshold, and absence of advice.

## Assumptions

- epsilon>0 and h>=0 are constants or uniformly computable limsup bounds.
- For infinitely many or kappa-dense m, A_m contains a certificate y whose emitted m-bit truth table has circuit complexity greater than 2^{epsilon m}.
- Membership in A_m and sequential bit emission of T_y are decidable in 2^{O(m)} time, with no nonuniform selector or per-length advice.
- The verifier checkpoint profile has cap alpha_V, so a claimed source threshold above alpha_V is invalid.

## Equations

- accepted_entropy: `|A_m| <= 2^{ell_m},  ell_m <= h m + O(1),  n_m=m+ell_m`. Valid when: Valid when the accepted certificates are counted by a uniform verifier and the entropy bound is publicly computable.
- multiplexed_lower_bound: `CC(F_m) > 2^{epsilon m} >= 2^{(epsilon/(1+h)-eta)n_m} for every eta>0 eventually`. Valid when: Valid when at least one accepted row is hard and circuits may be restricted by fixing the row index.
- padded_transfer: `delta < epsilon / ((1+h) kappa)`. Valid when: Applies after the kappa-dense padding map preserves E-uniformity and relates each target length to a nearby source length.
- cap_constraint: `epsilon <= alpha_V + o(1)`. Valid when: Requires the named verifier profile to give small checkpoint circuits for every accepted emitted table.

## Attempted Derivation

- Define A_m by the uniform verifier V and choose ell_m with |A_m|<=2^{ell_m}<=2^{h m+O(1)}.
- Construct F_m on inputs (a,z): enumerate certificates in lexicographic order, find the a-th accepted certificate if it exists, sequentially compute the z-th emitted bit, and output zero for missing rows.
- The decision procedure runs in 2^{O(m)} time; since n_m=m+ell_m=O(m), the target family is in E when ell_m and the length schedule are uniform.
- If a circuit C of size S computes F_m, fix a to the hard accepted certificate y*. The restricted circuit computes T_{y*}, so S>2^{epsilon m}-O(n_m).
- Convert the bound to the target input length: for every eta>0, CC(F_m)>2^{(epsilon/(1+h)-eta)n_m} for large m.
- Use kappa-dense padding to cover all target lengths, yielding any delta<epsilon/((1+h)kappa).
- Audit the source against the verifier cap alpha_V; a claim epsilon>alpha_V is invalid before extraction.

Blocking gap: No construction is known for a uniform, cap-compatible, low-entropy MCSP source with constant epsilon and a proved existential hard accepted certificate on kappa-dense lengths.

## Falsifiers

- Nonuniform entropy declaration: h is supplied by per-length advice rather than computed from the source description.
- Verifier cap violation: epsilon>alpha_V for the declared sequential/checkpoint profile.
- Entropy blowup: |A_m|=2^{omega(m)} or no constant h bound, causing the exponent transfer to collapse.
- Sparse bad lengths: hard accepted witnesses occur only on lengths not kappa-dense enough for the target consequence.
- Natural-property repair: adding random salt makes the accepted property large and constructive, triggering the natural-proofs falsifier rather than solving the source problem.
- Algebrizing/relativizing weakness: the certificate soundness proof relativizes while the claimed MCSP hardness must separate explicit truth tables from small circuits.

## Learning

Cycle 27 turns accepted-set entropy into an exact quantitative transfer parameter. The bridge is valid: existential hard MCSP witnesses suffice after multiplexing with loss 1+h and padding loss kappa. The remaining obstruction is source construction, specifically a uniform low-entropy cap-compatible non-natural certificate family with constant epsilon.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The route now has a precise rate parameter h, so a concrete thought experiment can test whether entropy savings survive easy contamination, padding, and cap constraints rather than merely restating MCSP hardness folklore.
- Situation seed: For each m, a verifier accepts exactly K_m=2^{h m} lexicographically ordered O(m)-bit certificates. One distinguished certificate emits a truth table with MCSP no-side threshold 2^{epsilon m}; the remaining accepted certificates emit constants. Build F_h(a,z) by accepted-certificate unranking and then kappa-pad to all target lengths.
- Varied variable: accepted-set entropy rate h in [0,c], with epsilon, kappa, and verifier profile alpha_V held fixed.
- Held-fixed controls: The verifier is uniform and uses no advice or nonuniform selector., The hard row has circuit complexity greater than 2^{epsilon m}., The source lengths are kappa-dense before padding., The bit-emission algorithm remains within 2^{O(m)} time.
- Expected observation: The lower-bound exponent should decay as epsilon/((1+h)kappa); easy rows do not hurt the multiplexed proof, but nonuniform h or epsilon>alpha_V invalidates the experiment.
- Transfer certificate needed: A formal certificate that ell_m is uniformly computable, lexicographic unranking is E-time, the hard row exists on kappa-dense lengths, and the verifier cap permits the claimed epsilon.

## Next Experiment

Audit candidate proof-system or meta-complexity verifiers for a computable accepted entropy bound h and checkpoint cap alpha_V; reject any candidate where the entropy certificate itself uses nonuniform length advice.
