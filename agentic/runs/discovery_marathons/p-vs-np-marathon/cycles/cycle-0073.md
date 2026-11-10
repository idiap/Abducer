# cycle-0073

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta=0 XOR carrier, any subthreshold residual circuit after deleting E_N<N^{epsilon-o(1)} source rows is a concrete upper-bound falsifier for the claimed N^{1+epsilon} source lower bound. Thus a valid nonfunctional proof-mediated escape from naturalization must certify row-deletion residual hardness, not merely SAT-semantic soundness.

## Definitions

- source object: H_N^{SAT}(x)=\oplus_{j\le M_N} SAT(G_N(x,j)), with |x|=N, M_N\le N^{q+o(1)}, formula length L_N=(\log N)^d, and generator/circuit overhead N^{rho+o(1)}.
- target object: SAT on L_N-bit formulas, with target consequence SAT notin SIZE(n^c) for every fixed c if C(H_N^{SAT})>N^{1+epsilon} and the beta=0 bridge is target-clean.
- controlled interface: substitute a nonuniform SAT circuit for each generated formula in the XOR carrier; separately audit proof-mediated nonfunctionality by row-deletion residual compression of the resulting source truth table.
- target-preserving condition: q<1+epsilon, rho<1+epsilon, L_N=N^{o(1)}, no advice beyond the fixed nonuniform circuits for the same input length, and the lower bound is against the same general circuit model used in the target transfer.
- row residual leakage: a pair (D_N,R_N) where D_N has size S_D and computes H_N^{SAT} on all x outside R_N, while |R_N|=E_N and R_N is patched by equality gates or an advice list.
- residual robustness obligation: for every S_D+O(E_N N)<N^{1+epsilon-o(1)}, D_N must fail on more than E_N rows; otherwise the source lower bound is invalid.

## Assumptions

- Nonuniform Boolean circuits with fan-in two over a fixed complete basis are used for both source and target statements.
- The generator G_N is explicit enough that its circuit cost is included in N^{rho+o(1)} and not hidden as advice.
- The SAT circuit substituted at length L_N is reused uniformly across all M_N generated slots for the fixed input length N.
- The proof-mediated lower-bound route is allowed to be SAT-semantic, but any sparse row exception set is charged by O(E_N N) equality patches.
- No claim is made that row-residual robustness proves P != NP; it is only a necessary audit for this carrier route.

## Equations

- xor_carrier: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j)),\quad M_N\le N^{q+o(1)},\ L_N=(\log N)^d`. Valid when: Valid when the source object is the explicitly generated beta-zero XOR carrier and every generated query has polylogarithmic target length.
- target_substitution_upper_bound: `SAT\in SIZE(n^c)\ \Rightarrow\ C(H_N^{SAT})\le N^{\rho+o(1)}+N^{q+o(1)}L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after the reduction preserves nonuniform circuit model identity and the target query length satisfies L_N=N^{o(1)}.
- row_patch_upper_bound: `D_N=H_N^{SAT}\text{ off }R_N\ \Rightarrow\ C(H_N^{SAT})\le S_D+O(E_NN)+O(1),\quad E_N=|R_N|`. Valid when: Valid when the residual circuit is fixed for length N and exceptional source rows are patched by equality tests.
- source_survival_threshold: `C(H_N^{SAT})>N^{1+\epsilon}\ \Rightarrow\ S_D\ge N^{1+\epsilon-o(1)}\text{ or }E_N\ge N^{\epsilon-o(1)}`. Valid when: Requires the row-patch upper bound and the claimed barely-superlinear source lower bound in the same circuit model.

## Attempted Derivation

- Fix H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, L_N=(log N)^d, and C(G_N)<=N^{rho+o(1)}.
- Assume SAT has circuits of size n^c at length L_N. Substituting the same SAT circuit into every generated slot gives C(H_N^{SAT})<=N^{rho+o(1)}+N^{q+o(1)}L_N^c.
- Since L_N^c=N^{o(1)}, the transfer is N^{max{rho,q}+o(1)}. Therefore C(H_N^{SAT})>N^{1+epsilon} with max{rho,q}<1+epsilon implies SAT notin SIZE(n^c) for every fixed c.
- Now suppose a residual circuit D_N of size S_D agrees with H_N^{SAT} outside R_N, with |R_N|=E_N. For each exceptional x, add an equality test to x and xor the correction bit. This costs O(E_N N) gates.
- Thus C(H_N^{SAT})<=S_D+O(E_N N). If S_D<N^{1+epsilon-delta} and E_N<N^{epsilon-delta}, the claimed source lower bound C(H_N^{SAT})>N^{1+epsilon-o(1)} is false.
- Hence a nonfunctional proof object that escapes label-functional naturalization must still prove residual hardness after deleting N^{epsilon-o(1)} rows; otherwise it supplies its own falsifier.

Blocking gap: No theorem yet converts an arbitrary SAT-semantic nonfunctional certificate into either a functional natural property or a sparse-row residual circuit. The row gate is a necessary falsifier audit, not a complete proof-system lower-bound framework.

## Falsifiers

- sparse row residual compression with E_N<N^{epsilon-o(1)} and S_D<N^{1+epsilon-o(1)}
- positive-beta black-box substitution cap q+beta c preventing all-exponent transfer
- functional dense certificate naturalization when soundness holds for arbitrary label vectors
- row-selection advice leakage hidden inside a SAT-semantic proof object
- low constructive incidence rank or label-free quotient sketch making the XOR carrier easy

## Learning

Cycle 73 adds a concrete row-deletion residual threshold to the surviving beta=0 XOR magnification route. A claimed N^{1+epsilon} source lower bound is invalid if the carrier has a subthreshold circuit wrong on fewer than N^{epsilon-o(1)} source rows, because equality patching costs O(E_N N). Thus a proof-mediated nonfunctional escape from natural proofs must be robust against sparse-row leakage; this is route-level progress, not a P vs NP proof.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The current route's live uncertainty is not the beta=0 target transfer but whether nonfunctional proof objects hide source-row leakage. A concrete row-deletion experiment tests the exact N^epsilon patching threshold before adding more abstract naturalness language.
- Situation seed: Take the beta=0 XOR carrier with L_N=(log N)^d, d>1, M_N=N^q, q in ((1+epsilon)/2,1+epsilon), and a generator whose incidence matrix has high quotient rank. Plant a residual circuit D_N that computes the carrier except on E_N selected source inputs, then patch those inputs by equality gates.
- Varied variable: row-error exponent theta where E_N=N^theta.
- Held-fixed controls: q<1+epsilon and rho<1+epsilon so the target substitution bridge stays valid, L_N=(log N)^d with d>1 so target queries remain subpolynomial and exhaustive lookup is not subthreshold, same nonuniform circuit model for source and target lower bounds, no additional advice except the fixed residual circuit and the explicit exceptional-row list
- Expected observation: For theta<epsilon, the equality patch costs N^{1+theta}<N^{1+epsilon} and kills the source lower bound; for theta>=epsilon, sparse patching no longer refutes the source claim, so any proof object must force at least N^{epsilon-o(1)} residual errors for every subthreshold D_N.
- Transfer certificate needed: A formal extraction theorem for a named proof system showing that every nonfunctional accepted certificate either is functional over labels or yields a residual circuit plus exceptional row list with charged size below the threshold.

## Next Experiment

Instantiate a named proof system Psys for beta=0 XOR certificates and test whether any accepted SAT-semantic certificate can be transformed into either a functional label property or a residual circuit wrong on fewer than N^{epsilon-o(1)} rows.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

A proof-mediated local lower-bound route with a logarithmic target projection and logarithmic proof-view treewidth naturalizes, provided the cluster has direct target soundness. Long proofs do not help once the searched projection is small and constructively decidable.

## Definitions

- source object: A proof-mediated local verifier family V_m(x,pi;r), where x in {0,1}^N is the truth table of an m-bit Boolean function, N=2^m, pi is a long auxiliary proof, and row r reads target coordinates Q_r and proof cells E_r.
- target object: SIZE_m(m^k), the nonuniform Boolean circuits on m inputs with at most m^k gates, represented by their N-bit truth tables.
- controlled interface: A finite row cluster C with target union U_X(C)=union_{r in C} Q_r, proof variables U_P(C)=union_{r in C} E_r, view-CSP constraints A_r(x|Q_r,pi|E_r)=1, and an explicit tree decomposition of the variable-constraint graph with bag size b.
- target-preserving condition: DirectClusterSound(C,k) holds: for every g in TT(SIZE_m(m^k)), no assignment to U_P(C) makes every row in C accept when x=TT(g), and C is generated from m without circuit-dependent advice.
- P_C is the projection property {x in {0,1}^N : exists pi_{U_P(C)} such that all constraints in C accept}.
- d=|U_X(C)| is the target-query union size; b is the maximum number of binary variables in a tree-decomposition bag.

## Assumptions

- Uniformity regime: row predicates and the row-cluster generator are computable in poly(N), and the tree decomposition is output or checkable in poly(N).
- Completeness regime: the intended hard truth table, e.g. TT(SAT_m), has a proof whose restriction to U_P(C) makes all rows in C accept.
- Constructivity regime: membership in P_C is decided from x|U_X(C) by dynamic programming over the displayed tree decomposition, not by hidden advice about a small circuit.
- Naturalness regime: d<=A log_2 N and b<=B log_2 N for fixed constants A,B, so density and recognition time are polynomial in N.
- Same-target regime: usefulness is quantified against exactly SIZE_m(m^k) on the same input length m; no padding, advice, or verifier-length change is allowed.

## Equations

- projection_property: `P_C=\{x\in\{0,1\}^N:\exists \pi_{U_P(C)}\ \forall r\in C\ A_r(x|Q_r,\pi|E_r)=1\}`. Valid when: Valid when the verifier rows, queried target coordinates, proof cells, and cluster C are explicitly fixed uniformly for length m.
- largeness_from_target_projection: `\mu(P_C)=|P_C|/2^N\ge 2^{-d}`. Valid when: Valid when P_C is nonempty by completeness and membership depends on only the d queried target coordinates.
- treewidth_constructivity: `T_{dec}(P_C)\le \operatorname{poly}(N,|C|)\,2^{O(b)}`. Valid when: Valid when the view-CSP has binary variables, efficiently evaluable row predicates, and a supplied tree decomposition of bag size b.
- direct_soundness_usefulness: `\mathrm{DirectClusterSound}(C,k)\Rightarrow P_C\cap TT(SIZE_m(m^k))=\emptyset`. Valid when: Valid when direct soundness is stated against the same nonuniform circuit class and the same m-bit truth-table encoding.
- natural_property_threshold: `d\le A\log_2 N\ \wedge\ b\le B\log_2 N\Rightarrow P_C\text{ is }N^{-A}\text{-large and }N^{O(B)}\text{-constructive}`. Valid when: Valid when A and B are fixed constants and all cluster descriptions are uniform polynomial-time objects.
- prf_pressure: `\operatorname{Adv}(D_{P_C})\ge \mu(P_C)\ge N^{-A}`. Valid when: Valid when the target class contains the proposed PRF family and D_{P_C} is the poly(N)-time truth-table membership test.

## Attempted Derivation

- Fix length m and a uniformly generated cluster C of verifier rows; define P_C by existentially projecting the proof variables read by C.
- Completeness gives one accepting assignment to the target coordinates U_X(C), namely TT(SAT_m)|U_X(C), so every extension outside U_X(C) lies in P_C; hence density at least 2^{-d}.
- Given a tree decomposition of the view-CSP of bag size b, decide membership in P_C by standard dynamic programming over proof variables and the d target constants read from x.
- Assume DirectClusterSound(C,k). Then no truth table of an m^k-size circuit belongs to P_C, so P_C is useful against SIZE_m(m^k).
- At d,b=O(log N), the property is simultaneously polynomial-density, poly(N)-constructive, and useful against the named target class; therefore the lower-bound route enters natural-proof/PRF pressure.
- Test the tempting replacement of DirectClusterSound by ordinary soundness using odd-charge Tseitin parity checks. Every proper local cluster is satisfiable although the full proof view is inconsistent, so ordinary soundness does not imply usefulness.

Blocking gap: No current proof supplies a uniform logarithmic-projection cluster with DirectClusterSound(C,k) for SAT lower bounds. The gap is local target soundness, not proof length or global PCP soundness.

## Falsifiers

- Odd-charge Tseitin proof-view CSP: globally unsatisfiable, but every proper local cluster is satisfiable; this falsifier refutes ordinary-soundness substitution.
- Target projection d=omega(log N): density 2^{-d} becomes too small for the natural-property contradiction and may be a valid escape.
- Tree-decomposition bag size b=omega(log N): projection membership may cease to be poly(N)-constructive.
- Circuit-dependent row selection or hidden row advice: the property is not a uniform constructive truth-table property.
- A cluster with completeness but no DirectClusterSound may contain simple functions such as constants or parity, destroying usefulness against SIZE_m(m^k).

## Learning

Cycle 73 isolates a sharper proof-mediated gate: proof length is irrelevant once the row cluster has logarithmic target projection and logarithmic projection-decision width. The exact missing object is DirectClusterSound(C,k). Odd-charge Tseitin gives a finite falsifier showing that ordinary soundness or local consistency cannot fill this gap. This is valid route-level progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs to separate genuine proof-mediated escape from local-consistency theater. A concrete proof-view CSP lets us vary one structural parameter and observe exactly when the naturalization bridge is valid or refuted.
- Situation seed: Attach an odd-charge Tseitin proof-consistency layer to a hypothetical local verifier for a SAT truth-table lower bound. Row clusters are vertex parity checks plus a fixed d=A log N target-bit projection, and the target class remains SIZE_m(m^k).
- Varied variable: cycle-rank rho of the selected proof-view cluster, ranging from a forest, to one parity cycle, to an expander-like cyclic subgraph.
- Held-fixed controls: N=2^m and the target class SIZE_m(m^k) are fixed on the same m-bit slice., The target-query union is held at d=A log N and each row has O(1) target queries., The row generator and the displayed decomposition are uniform poly(N)-time objects with no circuit-dependent advice., The global proof-consistency layer is unsatisfiable by odd total Tseitin charge.
- Expected observation: For rho=0 or any proper Tseitin subsystem, proof variables can satisfy the cluster for every target pattern, so ordinary soundness yields no usefulness. Only an additional direct target-soundness certificate can make the cluster reject all small-circuit truth tables; if it does so at d,b=O(log N), the route naturalizes.
- Transfer certificate needed: A formal certificate consisting of SAT-completeness on the cluster, DirectClusterSound(C,k) against SIZE_m(m^k), d=O(log N), b=O(log N), and advice-free uniform generation. Without all five items, the intuition cannot enter the proof queue.

## Next Experiment

Formalize the odd-charge Tseitin embedding with a dummy SAT projection and prove the proper-subsystem satisfiability lemma over F_2; then test one named proof system for an advice-free cluster satisfying DirectClusterSound(C,k) at d,b=O(log N).

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Adaptive semantic-cover falsifier. Let T_m be a generated truth-table row claimed to be on the no-side of MCSP at threshold 2^{theta m}. If T_m has an adaptive semantic cover with routing exponent tau, leaf-family count exponents a_l, per-leaf payload exponents mu_l, and shared opener exponents omega_l, and alpha_ad=max{tau,max_l(a_l+mu_l),max_l omega_l}<theta, then the claimed MCSP no-side source is invalid because T_m has unrestricted circuits of size 2^{(alpha_ad+o(1))m}.

## Definitions

- source object: generated MCSP anti-ball carrier row T_m in {0,1}^{2^m}, optionally arising from a row/proof stream G_m with low distinct-image entropy D.
- target object: E-uniform language L_T whose length-m truth table is T_m, with intended unrestricted circuit lower bound CC(T_m)>2^{theta m}.
- controlled interface: adaptive semantic block-cover consisting of a small router, ranked leaf families, hardwired leaf payload summaries, and shared openers that recover T_m(x) from the leaf payload and local coordinate.
- target-preserving condition: row lengths are advice-free and kappa-gap searchable, the image entropy overhead D is charged, and the extraction target is only delta<theta/(kappa(1+D)) after the MCSP no-side claim survives all cover falsifiers.

## Assumptions

- Circuit model is unrestricted fan-in-2 Boolean circuits with nonuniform hardwiring allowed for each m.
- The router maps each input x in {0,1}^m to a leaf identifier and local coordinate using size 2^{tau m+o(m)}.
- Leaf family l contains at most 2^{a_l m+o(m)} leaves, and each leaf carries at most 2^{mu_l m+o(m)} summary bits.
- The opener for family l has size 2^{omega_l m+o(m)} and computes the row bit from the leaf payload and local coordinate.
- The cover may be found by a nonuniform auditor; for a falsifier, existence of the cover already gives a nonuniform circuit upper bound.
- The lemma is a route-level no-go for carrier sources, not a proof or disproof of P versus NP.

## Equations

- truth-table-length: `N=2^m`. Valid when: Valid when truth tables are indexed by m-bit inputs and MCSP thresholds are measured against the full N-bit table.
- adaptive-cover-exponent: `alpha_ad=max{tau, max_l(a_l+mu_l), max_l omega_l}`. Valid when: Valid when every adaptive leaf family has ranked leaves, bounded payload length, and a shared opener counted in unrestricted circuit size.
- cover-to-circuit-upper-bound: `CC(T_m) <= 2^{(alpha_ad+o(1))m}`. Valid when: Valid when the router, all leaf payload summaries, and all shared openers can be hardwired into one nonuniform circuit for length m.
- mcsp-source-contradiction: `alpha_ad < theta implies T_m is not a valid no-side MCSP carrier at threshold 2^{theta m}`. Valid when: Valid when the source claim requires every accepted generated row to have unrestricted circuit complexity greater than 2^{theta m}.
- conditional-e-transfer: `delta < theta/(kappa(1+D))`. Valid when: Applies after a surviving hard row is kappa-gap searchable and distinct-image entropy D is the only multiplexing overhead charged.

## Attempted Derivation

- Fix m and a row T_m of length N=2^m with claimed CC(T_m)>2^{theta m}.
- Assume an adaptive semantic cover: router R sends x to a leaf family l, a ranked leaf id y, and a local coordinate z.
- Hardwire all payload strings for all leaves; their total size in family l is at most 2^{(a_l+mu_l+o(1))m}.
- Hardwire the shared opener circuits O_l and the router R. The circuit on input x computes (l,y,z), selects the hardwired payload for y, runs O_l, and outputs T_m(x).
- The resulting unrestricted circuit has size dominated by max{tau,max_l(a_l+mu_l),max_l omega_l}, proving the upper bound.
- Therefore a cover exponent strictly below theta is a concrete falsifier for the MCSP no-side source, including adaptive Merkle, checkpoint, digest, and proof-opening repairs.

Blocking gap: The positive direction still requires constructing a generated row family with semdim_ad(T_m)>=theta, which is equivalent up to o(1) to proving genuine unrestricted row hardness.

## Falsifiers

- adaptive semantic cover with alpha_ad<theta for the claimed hard row
- Merkle or digest proof stream whose leaf payloads and verifier flatten below the MCSP threshold
- checkpoint or hierarchical summary tree with max_i(a_i+mu_i,omega_i)<theta
- algebraically skippable or block-summary-rankable generator that gives a subthreshold row opener
- nonuniform hard-row selector or advice-selected length that breaks E-uniform extraction
- dense poly(N)-decidable projection repair that becomes a useful natural property
- low-D aggregate proof that certifies only index hardness rather than unrestricted row hardness

## Learning

Cycle 73 upgrades the semantic-cover falsifier from hierarchical static summaries to adaptive proof-opening streams. The exact new parameter is alpha_ad=max{tau,max_l(a_l+mu_l),max_l omega_l}. Any proposed generated MCSP carrier with alpha_ad<theta is invalid as a no-side source. Escaping the falsifier requires proving high adaptive cover dimension, which is essentially the unrestricted row lower bound in non-natural normal form.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch needs a finite falsifier probe for proof-stream repairs, not another abstract hardness-magnification statement. Adaptive covers directly test whether a proposed generated MCSP anti-ball source leaks a nonuniform circuit for its own row.
- Situation seed: Consider a generated MCSP anti-ball row T_m with a Merkle-style proof stream. The row is partitioned into ranked leaves; each leaf has a digest/payload, and a shared verifier opens any bit inside the leaf from the payload and local coordinate.
- Varied variable: leaf payload exponent mu while theta, kappa, D, router exponent tau, and opener exponent omega are held fixed.
- Held-fixed controls: Unrestricted fan-in-2 circuit size is the MCSP measure., The intended no-side threshold is CC(T_m)>2^{theta m}., Rows are advice-free and kappa-gap searchable by the E extraction procedure., Distinct-image entropy D is charged in the multiplexing loss., No dense locator set is allowed to replace the sparse generated carrier.
- Expected observation: As mu drops below theta-a for a leaf family of exponent a, the computed alpha_ad=max{tau,a+mu,omega} crosses below theta and the proof stream becomes an explicit falsifier. If alpha_ad stays above theta for every semantic opening, the remaining task is a true lower-bound certificate, not a leakage repair.
- Transfer certificate needed: A formal translation from the concrete Merkle/checkpoint opening syntax to router, payload, and opener exponents, plus a proof that any surviving carrier still satisfies delta<theta/(kappa(1+D)) under the existing E-uniform extraction theorem.

## Next Experiment

Instantiate alpha_ad for three concrete proof-stream templates: Merkle digest openings, periodic checkpoint generators, and block-summary rankers; record whether each gives a subthreshold falsifier at theta=1/2-epsilon and D=0.
