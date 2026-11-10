# cycle-0025

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Generated-OR magnification: selector-range leakage gate

## Candidate Lemma

For a generated-OR carrier H_N, any small valid selector for a satisfying generated query, together with a small promise solver on the selected image, gives a direct circuit upper bound for H_N. Hence an N^{1+epsilon} source lower bound must rule out all subthreshold selector-plus-selected-range-solver pairs, not only additive hitting covers.

## Definitions

- source object: H_N(x)=OR_{1<=j<=M} SAT(G_N(x,j)) on |x|=N, with M=N^q, query length L=(log N)^d, and generator circuit size C(G_N)<=N^{rho+o(1)}.
- target object: SAT on L-bit formula encodings against nonuniform circuits of size L^c for every fixed c, yielding the route consequence SAT notin P/poly if the source lower bound is valid and target transfer is clean.
- controlled interface: target circuits enter only by replacing each SAT(G_N(x,j)) call; the source audit allows arbitrary nonuniform promise solvers on actual generated ranges as potential leakage.
- target-preserving condition: q<1+epsilon, rho<1+epsilon, L is polylogarithmic with lookup not subthreshold, and no selected-image advice or promise solver computes the carrier below N^{1+epsilon-o(1)}.

## Assumptions

- Sel_N:{0,1}^N->[M] is a total circuit of size s_N.
- For all x with H_N(x)=1, SAT(G_N(x,Sel_N(x)))=1.
- For all x with H_N(x)=0, every generated query is unsatisfiable, so the selected query is negative.
- P_N agrees with SAT on V_S={G_N(x,Sel_N(x)):x in {0,1}^N}.
- The generator and selector outputs are encoded with O(log M) overhead and no extra nonuniform advice beyond the named circuits.

## Equations

- selector_upper_bound: `C(H_N) \le C(G_N)+C(Sel_N)+C(P_N)+N^{o(1)}`. Valid when: Valid when Sel_N is a genuine positive selector and P_N is correct on the complete selected image V_S.
- source_obstruction: `C(H_N)>N^{1+\epsilon} \Rightarrow C(Sel_N)+C(P_N) \ge N^{1+\epsilon-o(1)}`. Valid when: Applies after generator overhead is below threshold and the asserted lower bound is in the same nonuniform circuit model.
- target_transfer_unchanged: `SAT\in SIZE(n^c) \Rightarrow C(H_N) \le N^{\rho+o(1)}+N^q(\log N)^{dc}=N^{\max\{\rho,q\}+o(1)}`. Valid when: Requires fixed target exponent c, polylogarithmic query length, and generator substitution preserving the nonuniform size accounting.

## Attempted Derivation

- Start with the cycle-24 condition that positive fibers and negative product fibers have no subthreshold nonuniform hitting cover.
- Try to conclude C(H_N)>N^{1+epsilon} by arguing every H_N circuit induces such a cover.
- Observe that a circuit can first compute a shared selector Sel_N(x) and query only G_N(x,Sel_N(x)).
- The induced cover over decoded selector values may have large additive cost because shared gates are replicated when charged per fiber.
- Therefore additive hitting-cover hardness does not exclude selector-plus-promise-solver circuits.

Blocking gap: Need a direct-sum or shared-computation lower bound converting any small selector/promise-solver circuit into a subthreshold cycle-24 cover. No such theorem is available, and it is plausibly false for structured selectors.

## Falsifiers

- Small valid selector plus small promise solver on V_S computes H_N below threshold.
- Selected-image equality-DNF lookup with |V_S|<N^{1+epsilon-o(1)} falsifies the claimed source lower bound.
- Shared computation collapse: additive hitting-cover lower bounds may miss one compact selector circuit.
- Nonuniform leakage through hardwired SAT labels on the selected image remains a route-level falsifier.
- If q>=1+epsilon or rho>=1+epsilon, the target transfer threshold collapses even before selector leakage is considered.

## Learning

Cycle 25 adds a shared-selector leakage gate. A generated-OR carrier can be easy via one compact selector and a promise SAT solver on only the selected image, even when additive semantic or hitting covers look expensive. Thus the valid source obligation is not merely high range entropy or label balance; it is lower bounding every selector-plus-selected-range-solver pair above N^{1+epsilon-o(1)} while preserving q,rho<1+epsilon for the target bridge.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and quantitative gate for proposed generated-OR carriers.`
- Rationale: The branch already has the target transfer; the live uncertainty is whether source lower bounds survive nonuniform leakage. Selector compression is a concrete circuit upper-bound mechanism not captured by previous range entropy or hitting-cover checks.
- Situation seed: Take H_N(x)=OR_{j<=N^q} SAT(G_N(x,j)) with L=(log N)^d, d>1, and imagine two generator designs: one where a low-depth rule points to a satisfiable query when one exists, and one where any valid selector must range over N^{1+epsilon} distinct formulas.
- Varied variable: The selected-image exponent sigma, defined by |{G_N(x,Sel_N(x)):x in {0,1}^N}|=N^{sigma+o(1)} for the smallest valid selector of subthreshold size.
- Held-fixed controls: q<1+epsilon and rho<1+epsilon so the SAT-to-H_N target bridge remains valid., Formula length L=(log N)^d with d>1 so full truth-table lookup over all formulas is superthreshold., The source lower-bound model is ordinary nonuniform Boolean circuits of size N^{1+epsilon}., The selector and promise solver receive no oracle access beyond hardwired nonuniform advice counted in their circuit size.
- Expected observation: If sigma<1+epsilon and the selector size is subthreshold, equality-DNF labels on V_S give C(H_N)<N^{1+epsilon-o(1)}. If every subthreshold selector has sigma>=1+epsilon, this particular falsifier is blocked but the main lower bound remains open.
- Transfer certificate needed: A formal selector-range lemma with exact size accounting, plus a proof that the proposed carrier has no subthreshold valid selector with a subthreshold selected-range SAT promise solver.

## Next Experiment

Instantiate Sel_N for simple generator templates, including lexicographic first-satisfying-query generators and hash-bucketed query generators, and compute whether selected-image lookup already drops below N^{1+epsilon}.

# Barrier-aware lower-bound route: positive-certificate naturalization gate

## Candidate Lemma

Let N=2^m. If a poly(N)-constructive separator P_N over truth tables accepts TT(SAT_m), rejects every m-input circuit of size m^k, and has an explicit 1-certificate alpha_N for TT(SAT_m) of size c(N), then the alpha_N-cylinder is a natural property of density 2^{-c(N)} useful against SIZE(m^k). In particular c(N)<=a log_2 N is a valid natural-proof object, not a barrier escape.

## Definitions

- source object: a total poly(N)-time decidable truth-table predicate P_N:{0,1}^N->{0,1} together with an explicit positive certificate alpha_N for TT(SAT_m).
- target object: a Razborov-Rudich style natural property R_N useful against Boolean circuits on m inputs of size m^k, with N=2^m.
- controlled interface: extract the cylinder of all truth tables agreeing with alpha_N and use the 1-certificate promise to place the cylinder inside P_N.
- target-preserving condition: alpha_N is computable or listable in poly(N), TT(SAT_m) satisfies alpha_N, alpha_N forces P_N=1 on the whole cylinder, and P_N rejects every target circuit truth table.

## Assumptions

- P_N is a total predicate on all N-bit truth tables, not merely a promise verifier on SAT and circuits.
- alpha_N is a partial assignment to c(N) coordinates and is a 1-certificate: every y extending alpha_N satisfies P_N(y)=1.
- The target class is fixed as SIZE(m^k), or another named circuit class closed under truth-table encoding.
- The certificate coordinates and required SAT bits are obtainable in poly(N); brute-force SAT on m-bit formulas is allowed because 2^m=N.
- Usefulness means R_N contains no truth table computed by the target circuit class.

## Equations

- truth_table_scale: `N=2^m,\quad c(N)=|\operatorname{dom}(\alpha_N)|`. Valid when: Valid when truth tables are indexed by all m-bit inputs and the certificate constrains coordinates of that table.
- extracted_property: `R_N=\{y\in\{0,1\}^N: \forall i\in\operatorname{dom}(\alpha_N),\ y_i=\alpha_N(i)\}`. Valid when: Applies when alpha_N is a partial assignment and membership is tested by checking its constrained coordinates.
- density_threshold: `\mu(R_N)=2^{-c(N)}\ge N^{-a}\quad\text{if }c(N)\le a\log_2 N`. Valid when: Valid when the constrained coordinates are distinct and the ambient distribution is uniform over all N-bit truth tables.
- usefulness_transfer: `R_N\cap \operatorname{TT}(\operatorname{SIZE}(m^k))=\varnothing`. Valid when: Requires the target-preserving condition that the extracted cylinder lies inside P_N and P_N rejects every target circuit truth table.

## Attempted Derivation

- Fix m and N=2^m; let H=TT(SAT_m).
- Assume P_N is total, poly(N)-constructive, P_N(H)=1, and P_N(C)=0 for every truth table C computed by an m-input circuit of size m^k.
- Let alpha_N be an explicit 1-certificate for P_N at H, so H extends alpha_N and every y extending alpha_N satisfies P_N(y)=1.
- Define R_N to be the cylinder of all y extending alpha_N.
- R_N is decidable in time poly(N) by checking the c(N) constrained coordinates; no query to P_N is required.
- The uniform measure of R_N is exactly 2^{-c(N)}; for c(N)<=a log_2 N this is at least N^{-a}.
- If a target circuit truth table y belonged to R_N, then y extends alpha_N, hence P_N(y)=1, contradicting the separator soundness P_N(y)=0.
- Therefore R_N is constructive, large at the stated threshold, and useful against SIZE(m^k).

Blocking gap: The route lemma is proved under its typed assumptions. The remaining gap for any P-vs-NP route is unjustified existence of such a low explicit positive certificate; PRF-based natural-proof barriers make that existence implausible for standard target classes.

## Falsifiers

- falsifier: a width-1 CNF fixing all N bits of TT(SAT_m) has tiny density 2^{-N}, so low clause width is not by itself a naturalness bridge.
- falsifier: a separator whose SAT acceptance requires c(N)=(log N)^2 certificate bits escapes polynomial largeness, since density becomes 2^{-(log N)^2}.
- falsifier: an implicit DNF with exponentially many terms may hide the SAT-satisfied term and lose poly(N) constructivity.
- falsifier: a promise-only proof object that is undefined off SAT and target circuits does not yield a total natural property.
- falsifier: a nonuniform alpha_N of length O(log N) chosen with unbounded advice is not a valid constructive object unless the advice is explicitly included within the poly(N) interface.

## Learning

Cycle 25 adds a valid quantitative gate: any explicit separator with O(log N) positive certificate complexity at the SAT truth table yields a natural property of polynomial density useful against the named target class. DNF witnessed-acceptance routes with O(log N) term width therefore naturalize; low-width CNF or negative-certificate routes are a concrete falsifier to the symmetric claim. This is route-level barrier progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs to distinguish witnessed accepting structure from merely low syntactic complexity; this is a concrete threshold question not settled by citing natural-proof folklore.
- Situation seed: Consider a family of explicit truth-table DNF separators P_N for SAT_m versus SIZE(m^k), with M=poly(N) terms and SAT accepted by at least one term; interpret the SAT-satisfied term as a candidate proof certificate.
- Varied variable: Positive certificate width c(N), varied from a log_2 N to (log N)^2 while keeping the same separator soundness.
- Held-fixed controls: N=2^m and target circuits are m-input SIZE(m^k)., P_N is a total poly(N)-time decidable truth-table predicate., The DNF list is poly(N)-uniform and SAT bits at queried coordinates are computable in poly(N)., Every target circuit truth table is rejected by P_N.
- Expected observation: At c(N)<=a log N the SAT-satisfied term gives density at least N^{-a} and triggers the natural-proof obstruction; at c(N)=(log N)^2 density is quasi-polynomially small and the largeness transfer collapses.
- Transfer certificate needed: A formal extraction certificate listing the SAT-satisfied term, proving its cylinder is contained in P_N^{-1}(1), and preserving rejection of all target circuit truth tables without hidden advice leakage.

## Next Experiment

Audit threshold-circuit separators by asking whether anti-concentration or monotone DNF approximations force a low positive certificate at TT(SAT_m), or whether high threshold genuinely avoids the positive-certificate naturalization gate.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Rate-costed certificate-index multiplexer bridge: existential hard accepted MCSP-carrier witnesses suffice without a selector, at exact exponent loss 1+c. If a uniform verifier/emitter V at source length m has certificates y of length at most c m and some accepted y* emits a table T_{m,y*} with circuit complexity greater than 2^{epsilon m}, then the target multiplexer L_V(y,x)=A_V(m,y)T_{m,y}(x) on n=(1+c)m input bits has circuit complexity greater than 2^{epsilon m-o(m)}. If such m are uniformly kappa-dense, padding gives every delta<epsilon/((1+c)kappa).

## Definitions

- source object: a uniform MCSP-carrier verifier/emitter V_m with certificate y of length at most c m, acceptance bit A_V(m,y), and emitted truth table T_{m,y}:{0,1}^m -> {0,1}.
- target object: an E-uniform Boolean language L_V whose length (1+c)m slice is the certificate-index multiplexer (y,x) -> A_V(m,y)T_{m,y}(x).
- controlled interface: hardwire an accepted certificate y* in any circuit for the multiplexer to obtain a circuit of essentially the same size for the hard MCSP no-side slice.
- target-preserving condition: the source lengths are uniformly locatable and kappa-dense, Eval_V runs in 2^{O(m)}, c,kappa,epsilon are constants, and no advice or nonuniform selector is used.

## Assumptions

- For each relevant m there exists an accepted y* with C(T_{m,y*})>2^{epsilon m}. Universal hardness of all accepted y is not required.
- Rejected certificates are mapped to the zero slice, so only accepted hard witnesses transfer.
- The source length set M has a uniform predecessor/locator usable in E for padding to all target lengths.
- Barrier audit: the carrier image has size at most 2^{cm+O(1)} among 2^{2^m} tables, so it is non-large; any dense constructive repair would become a natural-proofs falsifier under standard pseudorandom-function assumptions.

## Equations

- multiplexed_length: `n_m=(1+c)m+O(\log m)`. Valid when: Valid when the certificate rate c is constant and the length header or parsing overhead is logarithmic.
- slice_to_mux_lower_bound: `C(L_V\upharpoonright n_m) \ge \max_{A_V(m,y)=1} C(T_{m,y})-O(m) > 2^{\epsilon m-o(m)}`. Valid when: Valid when at least one accepted source certificate emits a hard table and hardwiring the certificate bits preserves the circuit model.
- rate_loss: `2^{\epsilon m-o(m)}=2^{(\epsilon/(1+c)-o(1))n_m}`. Valid when: Valid when source length m and certificate length c m are linearly related with fixed c.
- dense_padding_transfer: `\delta < \frac{\epsilon}{(1+c)\kappa}`. Valid when: Applies after uniformly padding from kappa-dense multiplexed lengths to all target lengths without advice or nonuniform length selection.
- cap_consistency: `\epsilon \le \alpha_V+o(1) \quad \text{and hence} \quad \delta < \frac{\alpha_V}{(1+c)\kappa}`. Valid when: Requires a valid checkpoint or block-simulation upper-bound profile alpha_V for every fixed accepted certificate slice.

## Attempted Derivation

- Define L_V on length n_m=(1+c)m by parsing the first c m bits as y and the last m bits as x; output zero if A_V(m,y)=0 and otherwise output the emitted bit T_{m,y}(x).
- Uniformity: because Eval_V(m,y,x) runs in 2^{O(m)} and n_m is linear in m, L_V is decidable in 2^{O(n_m)}, hence is an E target object.
- Lower-bound transfer: if a size-S circuit computes L_V at length n_m, fix y=y* for an accepted hard witness; the restricted circuit computes T_{m,y*} with size S+O(m).
- Therefore S>2^{epsilon m-o(m)}, giving exponent epsilon/(1+c) on the multiplexed lengths.
- If source lengths are uniformly kappa-dense, define the all-length padded language by ignoring extra pad bits and using the located predecessor source length; this loses the usual factor kappa, so every delta<epsilon/((1+c)kappa) is valid.
- Cap audit: if the verifier has fixed-slice checkpoint profile alpha_V, then any claim epsilon>alpha_V is internally inconsistent before transfer.

Blocking gap: The derivation is conditional. It does not construct a cap-compatible uniform source with constant epsilon, linear certificate rate c, and a kappa-dense locatable set of lengths containing at least one hard accepted witness.

## Falsifiers

- falsifier: certificate rate r(m)=omega(m) makes the transferred exponent o(1), so no constant E lower bound follows.
- falsifier: a claimed source with epsilon>alpha_V contradicts its own checkpoint/block-simulation upper bound and is not valid.
- falsifier: hard witnesses exist only among rejected certificates, because the multiplexer maps rejected slices to zero.
- falsifier: the source length set is not uniformly locatable, so kappa-density cannot be used for all-length padding inside E.
- falsifier: the construction uses advice to choose y*, which reintroduces nonuniform leakage and breaks the target-preserving condition.
- falsifier: replacing the sparse canonical carrier by a dense constructive property would trigger the natural-proofs obstruction rather than evade it.

## Learning

Cycle 25 converts the selector repair into a quantitative theorem: existential hard accepted MCSP witnesses transfer through certificate-index multiplexing with exact exponent loss 1+c, and kappa-padding gives delta<epsilon/((1+c)kappa). Easy contamination is no longer a falsifier for the multiplexed target, but superlinear certificates, nonuniform length selection, and epsilon above the verifier cap remain formal blockers. This is valid route-level progress, not a proof of P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The route now has a precise bridge, so the next uncertainty is quantitative: how certificate rate c erodes the target exponent and interacts with the checkpoint cap alpha_V. A concrete thought experiment tests whether multiplexing is a real repair or only hides selector advice in length growth.
- Situation seed: Hypothetical MCSP certificate family V_m where |y|=c m, Eval_V is sequential E-time, the accepted set contains many easy contaminated y and at least one y* whose table has MCSP threshold 2^{epsilon m}. Define the target function F_m(y,x)=A_V(m,y)T_{m,y}(x) and pad from a kappa-dense source set.
- Varied variable: certificate rate c in [0,1], holding epsilon, kappa, and the verifier cap profile alpha_V fixed.
- Held-fixed controls: source hard-slice threshold C(T_{m,y*})>2^{epsilon m}, uniform Eval_V time 2^{O(m)} with no advice, kappa-dense uniformly locatable source lengths, fixed-slice checkpoint cap alpha_V with epsilon<=alpha_V, target class is ordinary Boolean circuits closed under restrictions
- Expected observation: The transferred all-length exponent should follow delta(c)<epsilon/((1+c)kappa). Easy contamination should not change the lower bound, while increasing c monotonically weakens the consequence and superlinear c_m collapses it to zero.
- Transfer certificate needed: A formal proof of E-uniform parsing and padding, plus a restriction argument for the circuit class and a cap certificate showing epsilon<=alpha_V; without these, the thought experiment remains intuition and cannot enter the proof queue.

## Next Experiment

Audit concrete source templates for the tuple (c,epsilon,kappa,alpha_V): start with globally sequential proof-like emitters, compute their block-checkpoint alpha_V profile, and reject any template whose claimed MCSP threshold exceeds the cap or whose witness length is superlinear.
