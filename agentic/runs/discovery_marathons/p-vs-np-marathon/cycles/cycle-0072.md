# cycle-0072

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta=0 XOR carrier, every dense 2^{O(L)}-constructive certificate family that is functionally sound for all target label vectors yields a valid classical natural property useful against L^{O(1)}-size circuits. Thus a dense proof-mediated source lower bound escapes the natural-proofs obstruction only by being nonfunctional, nonlarge, nonconstructive, advice-leaking, or SAT-semantic and explicitly nonrelativizing.

## Definitions

- source object: H_{N,ell}(x)=\oplus_{j\le T_N} ell(G_N(x,j)), where x has length N, T_N=N^q, G_N has circuit size N^rho, and G_N outputs L=(log N)^d bit target instances.
- target object: the truth-table label vector ell_f of an L-bit Boolean function f; the intended target is ell_{SAT_L} on encoded formulas of length L.
- controlled interface: substitute a target circuit for f into each generated query, and verify/search P_N(ell,pi) in 2^{O(L)} time without label-dependent row advice.
- target-preserving condition: max{q,rho}<1+epsilon, d>1 fixed, beta=0 since L=N^{o(1)}, and P_N(ell,pi) soundly implies C(H_{N,ell})>N^{1+epsilon} for every label vector ell.

## Assumptions

- Model is nonuniform fan-in two Boolean circuits; all advice, certificate, generator, and decoder costs are charged in the stated size bounds.
- Uniformity regime: G_N and the verifier for P_N are constructible from 1^N in poly(N) or are explicitly charged as N^rho and 2^{O(L)} objects.
- Functional soundness regime: acceptance of P_N(ell,pi) is a theorem about H_{N,ell} for arbitrary label vectors, not only about the real SAT label vector.
- Largeness regime: A_N={ell: exists pi P_N(ell,pi)} has density at least 2^{-aL} among all 2^{2^L} L-bit truth tables for some fixed a.
- Same-theory condition: usefulness is against the same nonuniform circuit class used in the substitution upper bound; no oracle, algebraic extension, or hidden advice is allowed.

## Equations

- substitution_upper_bound_beta0: `C(H_{N,f}) \le C(G_N)+O(T_N\,C(f)+T_N L^{O(1)}) = N^{\max\{\rho,q\}+o(1)} \quad \text{if } C(f)\le L^c.`. Valid when: Applies when G_N has size N^rho, T_N=N^q, and the target truth-table function f has circuits of size L^c with L=(log N)^d.
- threshold_separation_window: `\max\{\rho,q\}<1+\epsilon \implies N^{\max\{\rho,q\}+o(1)}<N^{1+\epsilon}.`. Valid when: Requires fixed epsilon>0, fixed q and rho below threshold, and N large enough that the o(1) term is smaller than the threshold margin.
- natural_largeness_cutoff: `\delta_N=|A_N|/2^{2^L}\ge 2^{-aL}=(2^L)^{-a}.`. Valid when: Valid when certificates are counted over complete L-bit truth tables and constructivity is polynomial in the truth-table length 2^L.

## Attempted Derivation

- Instantiate the surviving carrier with L=(log N)^d, d>1, T_N=N^q, q<1+epsilon, and generator size N^rho with rho<1+epsilon.
- Assume a certificate predicate P_N is dense, 2^{O(L)}-constructive, and functionally sound for every label vector ell. Define R_L(f)=1 iff exists pi P_N(ell_f,pi).
- Constructivity of R_L is polynomial in the truth-table length 2^L, and density is at least 2^{-O(L)}, so R_L is large in the Razborov-Rudich sense.
- If f has circuits of size L^c, substituting f into the XOR generator gives C(H_{N,f})<=N^{max{q,rho}+o(1)}<N^{1+epsilon}; functional soundness therefore forces R_L(f)=0. This proves usefulness against L^c circuits for every fixed c.
- If P_N is not functional, extract the charged row-selection transcript it uses. A transcript with A_N+S_N+min{R_N,K_NC(SAT_L)}+E_NN below N^{1+epsilon} is a concrete falsifier of the claimed source lower-bound route.

Blocking gap: No theorem yet converts SAT-semantic, nonrelativizing certificates into functional certificates or into charged row-selection transcripts. That is the exact remaining gap, not a proof of P != NP.

## Falsifiers

- falsifier: positive target-query exponent beta gives the old transfer cap q+beta c and cannot exclude all SAT exponents.
- falsifier: a dense searchable certificate with functional soundness is a valid natural property, so it is barred under standard PRF assumptions rather than an escape route.
- falsifier: label-dependent row selection with A_N+S_N+R_N+E_NN<N^{1+epsilon} gives an unconditional small circuit for the source carrier.
- falsifier: under SAT_L in SIZE(L^c), a selected-probe transcript with A_N+S_N+K_NL^c+E_NN<N^{1+epsilon} collapses the attempted contradiction before reaching all-exponent separation.
- falsifier: density below 2^{-omega(L)} avoids classical naturalization but also breaks the promised searchable-large certificate route unless a separate nonlarge proof system is specified.
- falsifier: advice leakage in P_N invalidates both the natural-property derivation and the claimed target-preserving bridge unless the advice is explicitly charged.

## Learning

Cycle 72 upgrades the beta=0 XOR route from a vague naturalness warning to a dichotomy: dense functional searchable certificates become valid natural properties, while nonfunctional proof objects must pass an explicit row-selection leakage audit. The target bridge survives, but the source proof space is narrowed to sparse, nonconstructive, SAT-semantic nonrelativizing, or direct H_N lower bounds.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch now needs a concrete audit distinguishing valid beta=0 magnification from proof-certificate naturalization and row-selection leakage, not another restatement of hardness magnification folklore.
- Situation seed: Fix a beta=0 XOR carrier with L=(log N)^2, q=1+epsilon/2, rho=1+epsilon/3, and a proof-mediated certificate that may encode K_N formula-valued probes plus a decoder for H_N^{SAT}.
- Varied variable: row-selection advice exponent gamma where the charged selector and decoder budget is A_N+S_N=N^gamma.
- Held-fixed controls: The target bridge uses only SAT_L circuits substituted into L=(log N)^2 queries, so beta=0 is held fixed., The source lower-bound threshold remains C(H_N^{SAT})>N^{1+epsilon}., The generator size exponent rho and query count exponent q stay below 1+epsilon., All nonuniform advice, selected-image labels, and correction exceptions are charged explicitly.
- Expected observation: For gamma<1+epsilon, any small selected image R_N<N^{1+epsilon-gamma-o(1)} or small probe count K_N=N^{o(1)} becomes a subthreshold leakage falsifier; if no such transcript exists and certificates are dense-functional, the route naturalizes instead.
- Transfer certificate needed: A formal reconstruction lemma from the certificate transcript to a circuit for H_N^{SAT}, plus an advice-free enumeration or density proof before the intuition can affect proof obligations.

## Next Experiment

Instantiate the selected-probe audit for one named proof-system candidate: require q=1+epsilon/2, rho=1+epsilon/3, L=(log N)^2, then compute whether its certificates force A_N+S_N+R_N+E_NN or A_N+S_N+K_NL^c+E_NN below N^{1+epsilon}.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Bounded-width proof-view clusters do not constitute a long-proof escape. If a proof-mediated local verifier for CC(TT(SAT_m))>m^k has an explicit row cluster whose target-query union is O(log N), whose proof-view hypergraph has generalized hypertree width tau with tau*v=O(log N), and whose cluster is directly sound against every SIZE_m(m^k) truth table, then the induced existential cluster shadow is a valid Razborov-Rudich natural property useful against SIZE_m(m^k).

## Definitions

- source object: a uniform proof-mediated local verifier V_m for the lower-bound statement LB_m = CC(TT(SAT_m))>m^k, with row r reading target coordinates Q_r and proof coordinates I_r.
- target object: the total truth-table property P_m subseteq {0,1}^N defined by P_m(y)=1 iff there exists an assignment to the proof cells touched by C_m satisfying every row predicate in the explicit cluster C_m.
- controlled interface: an explicit row cluster C_m with h_m=|union_{r in C_m} Q_r| target-table queries, proof view size v_m=max_r |I_r|, and proof-view hypergraph H_m={I_r:r in C_m}.
- target-preserving condition: direct cluster soundness holds, meaning for every m-input circuit A of size at most m^k and every assignment to the touched proof cells, at least one row in C_m rejects TT(A).
- N=2^m is the truth-table length; constructivity means P_m is decidable in poly(N) time uniformly from m.
- tau_m denotes generalized hypertree width of H_m; acyclic view clusters are the special case tau_m=1.

## Assumptions

- Model: nonuniform Boolean circuits SIZE_m(m^k) over m input bits; the lower-bound statement is slice-wise and truth-table based.
- Uniformity: V_m and C_m are generated in poly(N) time, with no hidden superpolynomial advice selecting the cluster.
- Completeness: TT(SAT_m) has a proof assignment satisfying every row in C_m.
- Width regime: |C_m|<=N^a and tau_m*v_m<=b log N for constants a,b independent of m.
- Naturalness regime: h_m<=c log N, so the accepting cylinder around TT(SAT_m) has polynomial density.
- Soundness regime: usefulness is not inferred from ordinary global proof soundness; it is the direct cluster soundness stated above.

## Equations

- truth_table_length: `N=2^m`. Valid when: Valid when the source object is the m-bit SAT truth table and all complexity thresholds are measured on the same slice.
- density_from_target_union: `\mu(P_m)\ge 2^{-h_m}\ge N^{-c}`. Valid when: Valid when the SAT table has an accepting proof on C_m and h_m<=c log N target coordinates are the only target bits inspected by the cluster.
- bounded_width_constructivity: `T_{dec}(P_m)\le (N|C_m|)^{O(1)}2^{O(\tau_m v_m)}\le N^{O(1)}`. Valid when: Valid when each row relation is listable over at most v_m proof bits and H_m has a supplied or computable hypertree decomposition of width tau_m.
- direct_usefulness: `P_m\cap \{TT(A):A\in SIZE_m(m^k)\}=\varnothing`. Valid when: Valid when direct cluster soundness quantifies over all size m^k circuits and all assignments to every proof cell touched by C_m.
- prf_pressure: `Adv_D(G_m)\ge \mu(P_m)\ge N^{-c}`. Valid when: Valid when a PRF truth-table generator G_m outputs functions computable in SIZE_m(m^k) and D is the poly(N)-time decider for P_m.

## Attempted Derivation

- Encode each row r in C_m as a relation R_r(y|Q_r,z|I_r) over target bits and proof-view variables.
- Define P_m(y)=1 iff the CSP over rows C_m is satisfiable for the fixed target table y.
- Completeness gives one satisfying proof-view assignment for TT(SAT_m); therefore all truth tables agreeing with TT(SAT_m) on the h_m queried target coordinates also lie in P_m.
- A hypertree-decomposition dynamic program decides the existential proof-view CSP in time (N|C_m|)^{O(1)}2^{O(tau_m v_m)}, which is poly(N) under tau_m v_m=O(log N).
- Direct cluster soundness implies no truth table of a size m^k circuit lies in P_m, so P_m is useful against the named target class.
- Thus any such cluster yields a valid large constructive useful property; under same-class PRF security, the route faces natural-proofs pressure rather than escaping via long proofs.
- Tested replacement of direct soundness by ordinary soundness and found a blocking falsifier: inconsistent cycle-XOR systems have globally no proof but locally satisfiable bounded-width shadows.

Blocking gap: The missing theorem is direct cluster soundness or a consistency extractor for the specific lower-bound verifier; ordinary proof soundness does not imply it.

## Falsifiers

- Cycle-XOR or 3-XOR consistency systems where every acyclic row cluster is satisfiable but the full proof system is inconsistent; this falsifier blocks ordinary-soundness-to-usefulness transfer.
- A cluster with h_m=omega(log N) target queries has exponentially small accepting cylinder and may be non-large, so the natural-property conclusion is invalid.
- A proof-view hypergraph with tau_m v_m=omega(log N) can make CSP recognition superpolynomial in N, defeating constructivity without proving target hardness.
- A row cluster selected by superpolynomial nonuniform advice loses the valid uniform natural-property interface.
- A PRF family computable inside SIZE_m(m^k) and secure against poly(N)-time distinguishers at advantage N^{-O(1)} contradicts any claimed large constructive useful P_m.

## Learning

Cycle 72 adds a structural parameter to the long-proof escape analysis: proof-view hypertree width. If a local proof-mediated route has logarithmic target-query union and bounded-width proof-view CSP, then direct soundness makes it a valid natural property against the same circuit class. The precise falsifier is cyclic local consistency, showing that ordinary proof soundness is too weak.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch must decide whether long proof-mediated lower-bound certificates escape naturalization by proof length or only by high-width/nonconstructive consistency. A concrete view-CSP experiment tests the exact transfer rather than restating the barrier.
- Situation seed: Take a hypothetical local verifier for LB_m=CC(TT(SAT_m))>m^k. Choose an explicit row cluster C_m whose target queries are confined to beta log N SAT truth-table positions, and instantiate its proof-view hypergraph either as a join tree or as an inconsistent 3-XOR expander.
- Varied variable: generalized hypertree width tau_m of the proof-view hypergraph, with the product tau_m*v_m varied across the threshold c log N.
- Held-fixed controls: N=2^m and the target class SIZE_m(m^k) are fixed on the same input-length slice., The target-query union h_m=beta log N is held fixed to preserve polynomial density., Each row reads v_m=gamma log N proof bits and O(1) target bits., The cluster generator is uniform poly(N), with no hidden advice., Usefulness is tested both under direct cluster soundness and under ordinary global proof soundness.
- Expected observation: For tau_m v_m=O(log N), the existential shadow is decidable in poly(N) and becomes a natural property if direct cluster soundness holds. For cyclic 3-XOR-style clusters, ordinary soundness leaves local shadows satisfiable and supplies a falsifier to automatic usefulness.
- Transfer certificate needed: A formal certificate must give an explicit C_m, a bounded-width decomposition, and direct cluster soundness against every SIZE_m(m^k) truth table; otherwise the intuition remains a no-go diagnostic only.

## Next Experiment

Instantiate the gate for a named PCP or proof-complexity verifier for CC(TT(SAT_m))>m^k; compute h_m, v_m, tau_m, cluster explicitness, and test whether any candidate direct cluster soundness theorem survives the 3-XOR consistency falsifier.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Hierarchical semantic-cover flattening. Let T_m be an accepted truth-table row claimed to satisfy CC(T_m)>2^{theta m}. Suppose T_m has a depth d=2^{o(m)} semantic cover tree: level i has at most 2^{a_i m+o(m)} rankable nodes, each node summary has length 2^{mu_i m+o(m)}, and the shared opener at level i has unrestricted circuit size 2^{omega_i m+o(m)}. Then T_m has an unrestricted circuit of size 2^{(alpha_tree+o(1))m}, where alpha_tree=max_i{a_i+mu_i,omega_i}. Thus any proposed MCSP no-side carrier with alpha_tree<theta is invalid; this is a finite falsifier for recursive-summary proof streams.

## Definitions

- source object: an advice-free generated MCSP anti-ball carrier row T_m in {0,1}^{2^m}, optionally accompanied by a generated proof stream P_m.
- target object: an E-language L_T whose padded length blocks are obtained from the carrier rows and whose desired consequence is an unrestricted circuit lower bound.
- controlled interface: a semantic cover tree consisting of rankable block/node summaries and shared opener circuits that recover row bits from summaries.
- target-preserving condition: kappa-dense source lengths, low distinct-image entropy D, and E-uniform row generation must remain intact; a subthreshold cover exponent refutes the source before any transfer.
- CC(T_m) denotes unrestricted nonuniform Boolean circuit size for the length-m truth table.
- a_i is the exponent of the number of rankable nodes at tree level i; mu_i is the summary-length exponent; omega_i is the shared opener-size exponent.

## Assumptions

- Model is unrestricted fan-in two Boolean circuits; nonuniform hardwiring of all summaries is allowed in the MCSP lower-bound audit.
- Tree depth is d(m)<=2^{o(m)}, and path navigation, node ranking, and boundary decoding have size 2^{o(m)} or are charged to the relevant opener.
- The proposed carrier claims a constant threshold theta>0 for infinitely many or kappa-dense source lengths, not merely average-case or uniform hardness.
- The cover is semantic: summaries need only exist and be nonuniformly hardwired; they need not be generated by the original verifier.

## Equations

- tree_cover_exponent: `\alpha_{tree}=\max_{i\le d}\{a_i+\mu_i,\omega_i\}`. Valid when: Valid when a semantic cover tree has subexponential depth, rankable nodes, and all navigation costs are either subexponential or charged to the opener.
- flattened_circuit_upper_bound: `CC(T_m)\le 2^{(\alpha_{tree}+o(1))m}`. Valid when: Applies after hardwiring every level summary and composing the shared openers along a single input path in the unrestricted nonuniform circuit model.
- soundness_necessary_condition: `\theta\le \alpha_{tree}+o(1)`. Valid when: Requires the source row to be claimed as an MCSP no-instance above threshold 2^{theta m} on the same length m.

## Attempted Derivation

- Fix an accepted row T_m and a depth-d semantic cover tree with d=2^{o(m)}.
- Hardwire every node summary from every level into a nonuniform circuit; the total hardwired information at level i is at most 2^{(a_i+mu_i+o(1))m}.
- On input x in {0,1}^m, compute the rank/path of the relevant node at each level using the declared ranker or charge this cost to the opener.
- Compose the shared openers along the path and use multiplexers to retrieve the appropriate summaries; multiplexer overhead is polynomial in m times the total summary length.
- The resulting circuit size is bounded by the maximum over summary mass exponents and opener exponents, giving CC(T_m)<=2^{(alpha_tree+o(1))m}.
- If the source asserted CC(T_m)>2^{theta m} with alpha_tree<theta, the asserted MCSP no-side soundness is contradicted, so the cover is a valid route-level falsifier.

Blocking gap: The flattening proof only refutes sources that expose or imply low-exponent semantic covers. It does not construct a row with no such cover.

## Falsifiers

- A hierarchical semantic cover with alpha_tree<theta is a finite falsifier for the claimed MCSP no-side carrier.
- A compressed proof skeleton with indexed row opening exponent omega<theta gives a nonuniform circuit for each row.
- A checkpoint or block-summary implementation with max{1-lambda+mu,omega}<theta invalidates the source even if the generator is sequential.
- An algebraically skippable transition, such as affine, LFSR, or iteratable proof generation, yields a row opener and defeats MCSP soundness.
- A nonuniform hard-row selector or advice-dependent image unranking breaks the target-preserving transfer to an E language.
- A dense polytime-decidable projection that excludes all small circuits becomes a natural-property falsifier unless sparsity or proof-mediated nonconstructivity is preserved.

## Learning

Cycle 72 upgrades the semantic-cover audit from one-level summaries to hierarchical proof streams. Recursive summaries flatten to unrestricted circuits with exponent max_i{a_i+mu_i,omega_i}; hence Merkle-like, checkpoint, or digest-based repairs are invalid whenever this exponent is below theta. The useful contribution is a sharper falsifier gate, while the positive source theorem remains open and equivalent to proving genuine row hardness by nonnatural means.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe.`
- Rationale: The branch needs to know whether recursive proof streams genuinely evade one-level semantic covers or only hide a lower-exponent cover in their block summaries.
- Situation seed: For each m, imagine a generated anti-ball carrier G_m that emits a row T_m and a long proof stream; every interval of 2^{lambda m} row/proof positions has a deterministic digest of length 2^{mu(lambda)m} and a shared opener O_lambda of size 2^{omega(lambda)m}.
- Varied variable: lambda, the block-size exponent in the semantic cover tree.
- Held-fixed controls: Claimed row threshold theta for CC(T_m)>2^{theta m}., Advice-free E-time sequential generation of the row/proof stream., Distinct-image entropy D and kappa-density of source lengths., Unrestricted nonuniform circuits as the MCSP target model.
- Expected observation: If min_lambda max{1-lambda+mu(lambda),omega(lambda)}<theta, the proposed generator is invalid. If every value is at least theta, the source survives this cover audit but still has not proved row hardness.
- Transfer certificate needed: A formal extraction of rankable summaries and openers from the generator for the negative case, or a proof that no semantic tree cover below theta exists plus E-canonical low-D unranking for the positive transfer.

## Next Experiment

Instantiate the tree-cover audit on one concrete generated anti-ball proposal, compute mu(lambda) and omega(lambda) for checkpoint, digest, and opener mechanisms, and record whether min_lambda alpha(lambda) falls below the claimed theta.
