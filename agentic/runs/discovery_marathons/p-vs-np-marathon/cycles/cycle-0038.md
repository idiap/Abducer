# cycle-0038

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: realized-witness projection gate

## Candidate Lemma

For the high-q generated-OR carrier, any subthreshold family of realized position-indexed satisfying witnesses is a valid nonuniform-leakage falsifier for an N^{1+epsilon} source lower bound, while the SAT-to-carrier target bridge remains unchanged.

## Definitions

- source object: H_N(x)=OR_{j<=M} SAT(F_{N,j}(x)), where M=N^q and a batch generator G_N maps x to formulas F_{N,j}(x) of length L=(log N)^d.
- target object: SAT on L-bit formulas against nonuniform polynomial-size circuits, with the route consequence SAT notin P/poly if H_N has SIZE lower bound N^{1+epsilon}.
- controlled interface: batch generation cost C(G_N)<=N^{rho+o(1)}, evaluator cost N^{o(1)} per fixed witness, and substitution of SAT circuits into all M generated instances.
- target-preserving condition: d>1, q<1+epsilon, rho<1+epsilon, and no advice depending on x beyond the fixed nonuniform circuit for G_N and the chosen witness-cover lists.

## Assumptions

- q lies in ((1+epsilon)/2,1+epsilon) so dense tuple leakage of arity at least two is already threshold-blocked.
- For each position j, Y_j is a nonuniform list of assignments for the variables of F_{N,j}(x).
- The cover misses at most E_N positive inputs x with H_N(x)=1.
- Formula evaluation on a fixed assignment after batch generation costs poly(L)=N^{o(1)} gates.

## Equations

- target_substitution: `SAT\in SIZE(n^c)\Rightarrow C(H_N)\le N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when the batch generator outputs all queried formulas with shared cost N^{rho+o(1)} and each SAT replacement circuit is used on L=(log N)^d bit instances.
- witness_cover_upper_bound: `C(H_N)\le N^{\rho+o(1)}+\left(\sum_{j\le N^q}|Y_j|\right)N^{o(1)}+E_N\,N^{1+o(1)}`. Valid when: Applies after the witness lists hit every positive bag except E_N inputs and negative inputs remain rejected by direct formula evaluation.
- projection_entropy_threshold: `\sum_{j\le N^q}|Y_j|\ge N^{1+\epsilon-o(1)}\quad\text{or}\quad E_N\ge N^{\epsilon-o(1)}`. Valid when: Requires a claimed source lower bound C(H_N)>N^{1+epsilon-o(1)} with rho<1+epsilon and evaluator overhead only N^{o(1)}.
- average_support_gate: `\frac{1}{N^q}\sum_{j\le N^q}|Y_j|\ge N^{1+\epsilon-q-o(1)}`. Valid when: Valid when the misses are subpatchable and the total cover lower bound is converted into a per-position average witness-support obligation.

## Attempted Derivation

- Fix nonuniform lists Y_j and build one shared circuit for G_N that outputs all formulas F_{N,j}(x).
- For every pair (j,a) with a in Y_j, attach a small evaluator computing whether a satisfies F_{N,j}(x).
- OR all evaluator outputs; this never accepts a negative input because every generated formula in a negative bag is unsatisfiable.
- If a positive input is missed by all lists, add an equality patch for that x; E_N missed positives cost E_N*N^{1+o(1)} gates.
- The resulting size is N^{rho+o(1)}+(sum_j |Y_j|)N^{o(1)}+E_N N^{1+o(1)}.
- Therefore an N^{1+epsilon-o(1)} source lower bound forces either total cover size at least N^{1+epsilon-o(1)} or at least N^{epsilon-o(1)} missed positives.

Blocking gap: This proves only a necessary gate for the carrier lower bound. It does not supply the hard lower bound against all possible approximate witness covers.

## Falsifiers

- realized witness projection total W_N^* below N^{1+epsilon-o(1)}
- approximate witness lists with fewer than N^{epsilon-o(1)} missed positives and subthreshold total size
- positive fiber size below N^{epsilon-o(1)}, since equality patching alone makes H_N small
- batch generator not shareable, causing the source and target interfaces to mismatch
- rho reaching 1+epsilon, which hides witness-cover leakage behind generator cost

## Learning

Cycle 38 isolates a canonical unary leakage mechanism: all realized satisfying witnesses per generated position form a zero-error cover. Thus a valid high-q generated-OR route needs W_N^*>N^{1+epsilon-o(1)} or a stronger approximate-cover lower bound. The target substitution bridge survives, but source plausibility is now governed by witness-projection entropy rather than formula-range entropy alone.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The route now hinges on whether high-q generated OR carriers can avoid unary witness-cover leakage; an abstract barrier citation would not decide the quantitative threshold.
- Situation seed: Take H_N as an OR of M=N^q generated 3-CNF formulas of length L=(log N)^d, with q in ((1+epsilon)/2,1+epsilon), d>1, and a batch generator of size N^{rho+o(1)}. Force each position j to draw satisfiable instances from a planted-assignment pool A_j of size N^a while preserving high syntactic formula entropy by varying clauses around the planted assignment.
- Varied variable: the planted realized-witness support exponent a, where |A_j|=N^a for each generated position
- Held-fixed controls: q<1+epsilon and rho<1+epsilon so the SAT substitution bridge remains target-preserving, d>1 so exhaustive truth-table lookup on full formulas is not a subthreshold falsifier, the source lower-bound claim is general nonuniform SIZE(H_N)>N^{1+epsilon-o(1)}, negative bags are evaluated only through actual formula satisfaction, preventing false positives from witness tests
- Expected observation: A sharp boundary should appear at q+a=1+epsilon: below it, the planted pools give a subthreshold witness-cover circuit; above it, this particular falsifier disappears but residual lower-bound obligations remain.
- Transfer certificate needed: A formal certificate that the generator shares its work across all positions with cost N^{rho+o(1)}, that fixed-witness evaluation costs N^{o(1)}, and that no additional advice encodes x-specific witnesses beyond the hardwired pools.

## Next Experiment

Instantiate the planted-pool thought experiment and compute W_N^* for affine, low-degree, and pseudorandom assignment-pool generators; check whether any preserves q+a>1+epsilon without introducing natural-proof or advice-leakage collapse.

# Cycle 38: monotone lower-bound target-mismatch gate

## Candidate Lemma

A monotone circuit lower bound for a monotone NP function transfers to unrestricted circuit lower bounds only through an explicit negation-leakage simulator. Without such a simulator the route is invalid for P vs NP; perfect matching is the falsifier family.

## Definitions

- source object: a monotone lower-bound certificate proving M(f_N)>L(N) for a monotone Boolean function f_N, e.g. CLIQUE or another monotone NP search predicate encoded by edge variables.
- target object: unrestricted Boolean circuits SIZE(N^k) or uniform P algorithms for the same total language family f_N.
- controlled interface: a simulator Sim_mon that converts every unrestricted SIZE(S) circuit computing the named monotone f_N into a monotone circuit of size at most B_f(N,S), with no advice depending on the truth table beyond the original circuit.
- target-preserving condition: the source lower bound is useful for unrestricted circuits only when L(N)>B_f(N,N^k) and the simulator is uniform or at least nonuniformly valid for the exact target family.

## Assumptions

- Fan-in two monotone circuits use AND/OR gates without NOT gates on edge variables.
- Unrestricted circuits may use NOT gates and algebraic cancellations; this is the leakage channel audited here.
- The route claims a lower bound for unrestricted SIZE(N^k), not merely for monotone circuits.
- Known monotone lower bounds for a P-computable monotone function such as perfect matching are admitted as a target-mismatch falsifier.

## Equations

- monotone_complexity: `M(f_N)=\min\{|C|: C \text{ is a monotone circuit computing } f_N\}`. Valid when: Valid when the source model is exactly monotone Boolean circuits over the named input variables.
- conditional_transfer: `\big(M(f_N)>B_f(N,N^k)\ \wedge\ \mathrm{Sim}_{mon}(f_N,N^k)\le B_f(N,N^k)\big)\Rightarrow C(f_N)>N^k`. Valid when: Applies only after the simulator preserves the exact function family and size threshold.
- perfect_matching_obstruction: `C(PM_N)\le N^{O(1)}\quad\text{but}\quad M(PM_N)\ge N^{\omega(1)}`. Valid when: Valid when invoking the standard superpolynomial monotone lower bound for perfect matching and its polynomial-time algorithms.

## Attempted Derivation

- Assume a source theorem proves M(f_N)>L(N) for a monotone NP family f_N.
- To infer f_N notin SIZE(N^k), take the contrapositive: a SIZE(N^k) unrestricted circuit for f_N must imply a monotone circuit for f_N of size at most B_f(N,N^k).
- If such a simulator is available and L(N)>B_f(N,N^k), the conditional transfer is valid.
- A universal polynomial simulator is false: perfect matching has polynomial unrestricted circuits and uniform P algorithms, while its monotone circuit complexity is superpolynomial.
- Therefore a monotone lower-bound route must either remain inside monotone targets or prove a family-specific robustness theorem against NOT/cancellation leakage.

Blocking gap: No known target-preserving simulator converts arbitrary small unrestricted circuits for CLIQUE-like monotone NP functions into comparably small monotone circuits; PM_N blocks any family-independent simulator.

## Falsifiers

- Perfect matching: monotone, in P, polynomial unrestricted circuits, but superpolynomial monotone complexity; it is the decisive falsifier for universal monotone-simulation transfer.
- Any route whose only source theorem is M(f_N)>N^a and whose target conclusion is C(f_N)>N^k without a bound on B_f(N,N^k) is not valid.
- A monotone projection from a hard monotone function to an NP predicate preserves monotone hardness but is a falsifier for claims that monotone reductions alone preserve unrestricted lower bounds.

## Learning

Cycle 38 isolates a concrete target-model obstruction for monotone lower-bound routes. The valid contribution is the threshold condition L(N)>B_f(N,N^k); the route fails without a negation-leakage simulator. Perfect matching supplies the falsifier: P-computable monotone functions can have superpolynomial monotone complexity, so monotone lower bounds alone are not P-vs-NP progress.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe`
- Rationale: The branch needs to distinguish a genuine target-preserving monotone lower-bound transfer from a syntactic restriction lower bound that collapses when NOT gates or cancellations enter.
- Situation seed: Consider PM_N on N graph-edge variables and a CLIQUE_N monotone lower-bound certificate side by side. Both are monotone graph properties, but PM_N has a polynomial-time nonmonotone algorithm while retaining superpolynomial monotone circuit complexity.
- Varied variable: negation leakage t, the number of NOT gates or algebraic cancellation steps allowed in circuits computing the monotone function.
- Held-fixed controls: The source lower-bound model remains fan-in two monotone AND/OR circuits., The target class remains unrestricted SIZE(N^k) for a fixed k., The function family is total and explicit on N edge variables., No advice depending on the full truth table may be introduced by the transfer.
- Expected observation: At t=0 the monotone lower bound can be large; once enough nonmonotone leakage is allowed, PM_N drops to polynomial size. A valid route must show that the candidate NP function does not undergo the same collapse up to SIZE(N^k).
- Transfer certificate needed: A family-specific theorem bounding B_f(N,N^k), or a lower bound robust for circuits with the required amount of NOT/cancellation leakage; monotone lower bounds alone cannot enter the P-vs-NP proof queue.

## Next Experiment

Audit limited-negation lower bounds for CLIQUE-like monotone NP functions: vary t from O(1) to polylog(N), compute known lower-bound thresholds, and check whether any threshold survives to the unrestricted SIZE(N^k) regime without contradicting PM_N.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Bounded-image aggregate forcing is valid only as an unrestricted nonuniform circuit lower bound: if a canonical MCSP carrier has at most 2^{D m+o(m)} distinct rows and its ranked decoder A_m has circuit complexity above 2^{(D+epsilon)m+o(m)}, then some accepted row has MCSP threshold above 2^{epsilon m}; the multiplexed E target then has lower-bound exponent any delta<epsilon/(kappa(1+D)).

## Definitions

- source object: a length-m canonical MCSP carrier image family R_m={T_{m,i}}_{i<M_m}, where each T_{m,i} is a 2^m-bit truth table emitted or accepted by the source verifier.
- target object: an E-uniform ranked decoder language A on inputs (i,x), padded from kappa-dense source lengths to all target lengths.
- controlled interface: E-canonical distinct-image unranking computes T_{m,i}(x) without advice, while MCSP no-side means C(T_{m,i})>2^{epsilon m} against unrestricted Boolean circuits.
- target-preserving condition: the transfer preserves unrestricted circuit-size exponents, E uniformity after kappa-padding, and absence of nonuniform selector leakage.

## Assumptions

- M_m<=2^{D m+o(m)} distinct accepted images on a kappa-dense infinite set of source lengths.
- The ranked decoder A_m(i,x)=T_{m,i}(x) is E-computable by canonical unranking, not by advice.
- The aggregate lower bound is C(A_m)>2^{(D+epsilon)m+o(m)} against unrestricted nonuniform Boolean circuits.
- The target lower bound is route-level: it yields an E circuit lower bound, not P != NP itself.

## Equations

- image_entropy: `M_m \le 2^{D m+o(m)},\qquad n_m=m+\lceil\log M_m\rceil\le (1+D)m+o(m).`. Valid when: Valid when distinct images are E-canonically unranked and D is measured per source input bit m.
- row_decomposition_upper_bound: `\bigl(\forall i\; C(T_{m,i})\le 2^{\epsilon m}\bigr)\Rightarrow C(A_m)\le M_m\,2^{\epsilon m}\,\mathrm{poly}(m)=2^{(D+\epsilon)m+o(m)}.`. Valid when: Requires all rows to be truth tables on m input bits and the rank multiplexer to be an allowed unrestricted circuit construction.
- aggregate_forcing_threshold: `q_{force}=\frac{D+\epsilon}{1+D};\quad C(A_m)>2^{q n_m+o(n_m)}\text{ with }q>q_{force}\Rightarrow \exists i\; C(T_{m,i})>2^{\epsilon m}.`. Valid when: Applies only after the aggregate lower bound is nonuniform and polynomial rank decoding overhead is asymptotically negligible.
- padded_E_extraction: `\delta<\frac{\epsilon}{\kappa(1+D)}.`. Valid when: Valid when kappa-padding converts the source length set to all target lengths without advice or density-dependent selectors.

## Attempted Derivation

- Fix m and list the canonical distinct images T_{m,0},...,T_{m,M_m-1} with M_m<=2^{D m+o(m)}.
- Assume toward forcing that every accepted row has a circuit of size at most 2^{epsilon m}.
- Build an unrestricted circuit for A_m by equality-testing the rank i, selecting the corresponding row circuit, and ORing the M_m gated outputs.
- The size is at most M_m 2^{epsilon m} poly(m)=2^{(D+epsilon)m+o(m)}, hence any unrestricted aggregate lower bound above this forces at least one MCSP-hard row.
- Use the multiplexed language A itself for extraction: a circuit of size 2^{delta(1+D)m} for A would, after fixing the hard rank, give a circuit for the hard row, so delta<epsilon/(1+D); kappa-padding gives delta<epsilon/(kappa(1+D)).
- Audit the attempted shortcut: a P-uniform or restricted aggregate lower bound does not contradict the nonuniform row-decomposition circuit, so it cannot force an MCSP no-side row.

Blocking gap: No source theorem currently supplies an unrestricted, non-natural, no-advice aggregate lower bound above q_force with cap slack, nor a direct tiny-D row-hardness certificate.

## Falsifiers

- falsifier: the aggregate lower bound is only P-uniform, logspace-uniform, algebraic, or restricted to a circuit class not closed under M_m-way multiplexing.
- falsifier: the ranked decoder or canonical unranking uses advice, a nonuniform hard-row selector, or non-E-uniform length choices.
- falsifier: D violates D<(alpha_A-epsilon)/(1-alpha_A), causing quantitative threshold collapse before extraction.
- falsifier: subthreshold ranked random access yields row circuits below 2^{epsilon m}, contradicting the claimed MCSP no-side source.
- falsifier: a dense constructive property over aggregate truth tables is used; this reintroduces the natural-proofs obstruction unless the property is sparse or non-natural.
- falsifier: the source certifies index hardness or uniform decoder hardness but not unrestricted row circuit complexity.

## Learning

Cycle 38 proves the exact nonuniform aggregate-forcing gate and gives a concrete constant-row falsifier for uniform aggregate shortcuts. The bridge is valid only for unrestricted circuit lower bounds above q_force=(D+epsilon)/(1+D), with cap slack D<(alpha_A-epsilon)/(1-alpha_A); otherwise the route must switch to direct tiny-D row hardness.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch needs a concrete separation between uniform aggregate hardness and unrestricted MCSP row hardness; otherwise it will keep restating the aggregate route without a valid transfer certificate.
- Situation seed: A padded ranked MCSP-carrier family with M_m=2^{D m} rows, where the control case has constant rows T_{m,i}(x)=b_{m,i} and the intended case has E-canonical truth-table rows from a sequential certificate verifier.
- Varied variable: D, the distinct-image entropy exponent, while epsilon and the aggregate cap alpha_A are held fixed.
- Held-fixed controls: source threshold C(T)>2^{epsilon m} for MCSP no-side rows, kappa=1 length padding for the first audit, then explicit kappa loss is restored, unrestricted Boolean circuits are the target lower-bound model, E-canonical unranking is required and no advice or selector is allowed
- Expected observation: For constant rows, every row is MCSP-easy although the uniform aggregate sequence can be hard; as D increases in the intended case, q_force=(D+epsilon)/(1+D) approaches the cap and eventually blocks the route. This should identify whether the source must be direct-row tiny-D or genuinely unrestricted aggregate-hard.
- Transfer certificate needed: A valid certificate must prove either an actual hard row or an unrestricted nonuniform aggregate lower bound above q_force with D<(alpha_A-epsilon)/(1-alpha_A), plus E-uniform canonical unranking for the multiplexed target.

## Next Experiment

Instantiate the thought experiment at alpha_A=1/2 and epsilon=1/3: test D<1/3 versus D>=1/3, and audit whether any proposed sequential certificate proves direct row hardness rather than merely uniform aggregate hardness.
