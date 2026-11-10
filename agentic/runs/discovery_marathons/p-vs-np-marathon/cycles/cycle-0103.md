# cycle-0103

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For Psys_sym^IU, where every FormulaEval-SAT selector is a bit-explicit union of intervals in [M_N], FE_Extract_N is valid with row expansion charge N|RowSet|. A global FormulaEval line over all M_N=N^{q+o(1)} slots costs N^{1+q+o(1)}. If the same line is treated as an unexpanded semantic oracle, surface occurrence completion is refuted by a private-row falsifier unless a nonrelativizing FE_Extract_N theorem is separately proved.

## Definitions

- source object: beta-zero SAT parity carrier H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)), with |x|=N, M_N=N^{q+o(1)}, |G_N(x,j)|=(log N)^{O(1)}, and generator size N^{rho+o(1)}.
- target object: a restricted parser and transcript-falsifier theorem for Psys_sym^IU lower-bound certificates for LB_N(1+epsilon), not a proof of P != NP.
- controlled interface: FormulaEval-SAT exposes RowSet(a) through proof-bit interval endpoints, so the parser can list every touched parity row and charge N per row plus inherited EF/SATeq/SR_h costs.
- target-preserving condition: beta=0, q,rho<1+epsilon, interval endpoints and generator bits are advice-free and uniform, and no FormulaEval line hides semantic row access outside RowSet(a).
- RowSet(a) is the subset of [M_N] selected by a proof line a; in Psys_sym^IU it is a union of R_a=N^{r_a+o(1)} explicitly encoded intervals.
- K_idx(pi) is the union of all row indices exposed by FormulaEval, SATeq links, bounded-SR_h leaves, and earlier bit-explicit dependencies in the parsed proof pi.

## Assumptions

- Length regime: N ranges over valid carrier lengths and all o(1) terms are uniform over fixed q,rho,epsilon,eta,tau.
- Proof model: Psys_sym^IU extends bit-explicit EF+SATeq+bounded-SR_h by FormulaEval-SAT lines whose row selectors are explicit interval unions; the verifier reads all interval endpoints as proof bits.
- Circuit model: nonuniform Boolean circuits measure C(H_N), while the proof parser itself receives no nonuniform advice beyond the displayed proof pi and fixed uniform generator G_N.
- Expansion convention: one exposed parity row costs O(N) gates in the transcript-to-circuit falsifier because sparse row corrections are equality tests on the N-bit source input.
- Barrier status: the positive theorem is relativizing for interval-union surface syntax; the semantic-oracle escape is outside its scope and needs a nonrelativizing FE_Extract_N certificate.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)}`. Valid when: Valid when the source carrier is the beta-zero generated parity problem with explicitly indexed SAT instances.
- IU_row_expansion: `\Gamma_{FE}^{IU}(\pi)=N\cdot |K_{idx}^{FE}(\pi)|+N^{o(1)}\sum_a R_a`. Valid when: Valid when every FormulaEval selector is an explicit interval union whose endpoints are proof bits.
- global_FE_cost: `\Gamma_{FE}^{all}=N\cdot M_N=N^{1+q+o(1)}`. Valid when: Applies when a FormulaEval line ranges over all parity slots of the generated carrier.
- total_transcript_cost: `\Gamma_{sym}^{IU}(\pi)=S_{dep}(\pi)+S_{link}(\pi)+B_{SR}(\pi)+N|K_{idx}(\pi)|+E_NN+N^{o(1)}`. Valid when: Requires the bit-explicit EF, SATeq, bounded-SR_h, and interval-union FormulaEval parsers to share one row-index convention.
- restricted_falsifier_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{sym}^{IU}(\pi)`. Valid when: Applies after the parsed transcript plus generator uniformly simulates all non-residual carrier rows.
- LB_falsifier_threshold: `N^{\rho+o(1)}+\Gamma_{sym}^{IU}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow LB_N(1+\epsilon)\text{ is false}`. Valid when: Valid when LB_N asserts circuit size at least N^{1+epsilon-o(1)} in the same nonuniform circuit model.
- support_density_pressure: `N|K_{idx}(\pi)|\ge N^{1+\epsilon-o(1)}\Rightarrow |K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Requires the transcript falsifier inequality to be the only obstruction to the claimed lower-bound certificate.

## Attempted Derivation

- Fix N, M_N=N^{q+o(1)}, b_N=ceil(log M_N), and encode each row index j by b_N bits; define Psys_sym^IU by adding interval-union FormulaEval-SAT lines to the already parsed Psys_bEF^- rules.
- For a FormulaEval line a, read all interval endpoints from pi, merge overlaps, enumerate RowSet(a), and append tuples (line a,row j,formula-bit neighborhood from G_N) to K_idx^{FE}.
- Extend the cycle-102 line invariant: after line t, every semantic SAT-label dependency used by the first t lines is either in K_idx, in a SATeq link charge, in a bounded-SR_h leaf charge B_SR, or in the residual error set E_N.
- For EF extension lines, traverse the transitive definition DAG and add S_dep; for SATeq lines, add S_link; for bounded-SR_h lines, use B_SR(pi)<=N^{q+eta+tau+o(1)} from the SR_h bit-normal form.
- For interval-union FormulaEval lines, the only new dependency is membership in RowSet(a); enumeration is advice-free, so the added circuit transcript cost is N|RowSet(a)| plus negligible row-encoding and occurrence-neighborhood overhead.
- Induct over proof lines to obtain Gamma_sym^IU(pi)=S_dep+S_link+B_SR+N|K_idx|+E_NN+N^{o(1)} and no hidden semantic row dependency inside Psys_sym^IU.
- Build the falsifier circuit: compute G_N with size N^{rho+o(1)}, use the parsed transcript for all charged rows, and patch E_N residual source rows by equality gates, giving C(H_N)<=N^{rho+o(1)}+Gamma_sym^IU(pi).
- If a FormulaEval line is instead declared semantic and unexpanded, remove it from Psys_sym^IU; if kept without RowSet charge, choose j* outside K_idx and apply the private-row spoof, showing surface occurrence completion is unsound.

Blocking gap: The derivation does not prove FE_Extract_N for arbitrary Psys_sym selectors or for real FormulaEval-SAT comprehension whose row set is defined by semantic SAT facts rather than displayed interval endpoints.

## Falsifiers

- falsifier: unexpanded symbolic FormulaEval-SAT with an uncharged private row j* makes two label worlds transcript-identical but parity-opposite, so surface occurrence completion is invalid.
- falsifier: if q<epsilon and global FormulaEval expands to all M_N rows, then the N^{1+q+o(1)} row charge is still subthreshold and can collapse the claimed LB_N lower bound when rho<1+epsilon.
- falsifier: if interval endpoints or selector descriptions are supplied as nonuniform advice rather than proof bits, RowSetEnumerator_N is not advice-free and the Psys_sym^IU theorem is not valid.
- falsifier: positive target-query exponent beta in any attempted black-box substitution reintroduces the transfer cap q+beta c and blocks all-exponent NP not subset P/poly consequences.

## Learning

Cycle 103 discharges a concrete FormulaEval subcase: transparent interval-union selectors admit a valid FE_Extract_N parser with N|RowSet| expansion charge, so global FormulaEval costs N^{1+q+o(1)} and yields the q/epsilon support trichotomy. The full Psys_sym claim remains quarantined exactly at semantic FormulaEval extraction; unexpanded symbolic FormulaEval is refuted by the private-row falsifier, not by generic barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch must decide whether FormulaEval-SAT is a chargeable transparent proof mechanism or a semantic oracle escape; an interval-union row-set experiment directly tests the transfer certificate rather than restating barriers.
- Situation seed: Consider H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^q, L_N=(log N)^d, and one Psys_sym FormulaEval line whose selector is either [1,M_N] or a union of intervals missing one planted private row j*.
- Varied variable: coverage exponent kappa=log_N |RowSet(a)|, varied from sparse N^kappa support to full coverage kappa=q.
- Held-fixed controls: beta=0 polylogarithmic SAT query length and generator size N^{rho+o(1)} with rho<1+epsilon, interval endpoints are proof bits and the parser receives no semantic row advice, the circuit model for LB_N and for the transcript falsifier is the same nonuniform Boolean circuit model, bounded-SR_h, SATeq, and EF dependency costs are held at the cycle-102 Gamma_bEF charges
- Expected observation: Expansion cost scales as N^{1+kappa+o(1)}. For kappa<epsilon it is a subthreshold falsifier; at kappa=epsilon it consumes the lower-bound margin; for kappa>epsilon it is no longer a cheap falsifier but still certifies absolute row contact. If the planted private row is omitted under semantic FormulaEval, the transcript cannot determine parity.
- Transfer certificate needed: A valid RowSetEnumerator_N/FE_Extract_N certificate proving that selected rows are uniformly enumerable from proof bits and that every FormulaEval dependency enters K_idx with N-per-row charge; otherwise the intuition remains only a private-row oracle falsifier.

## Next Experiment

Extend RowSetEnumerator_N from interval-union selectors to a named AC0 selector fragment by full scanning over [M_N]; compute whether scan overhead N^{q+o(1)} is dominated by N|RowSet| and identify the smallest AC0-private-row countermodel if enumeration depends on semantic advice.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For Psys_sym^vsel, where every FormulaEval-SAT atom carries proof-visible extensional selector code, RowSetEnumerator_N is valid with an added selector-enumeration charge. If a valid proof pi establishes LB_N(1+epsilon) for H_N^SAT, then the parsed transcript satisfies the Gamma_sel lower-pressure inequality; if Gamma_sel is subthreshold, the claimed lower bound has a circuit-upper-bound falsifier.

## Definitions

- source object: Psys_sym^vsel(N) proof pi of LB_N(1+epsilon) asserting Ckt(H_N^SAT)>N^{1+epsilon-o(1)}, where H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}, and G_N has circuit size N^{rho+o(1)}.
- target object: an expansion-aware occurrence transcript Q_pi^+ with semantic row support K_idx^+(pi) and a circuit upper-bound certificate for H_N^SAT in the same nonuniform SIZE model.
- controlled interface: FormulaEval-SAT atoms must expose a deterministic selector circuit Sel_a(j) over public row indices plus explicit formula-bit wires; the parser enumerates RowSet(a)={j<M_N: Sel_a(j)=1} and charges N per selected row.
- target-preserving condition: the selector code is proof-visible, extensional in j, independent of hidden advice and SAT oracle semantics, and its enumeration cost plus row expansion cost are included in Gamma_sel(pi).

## Assumptions

- Regime: N=2^n, epsilon>0 fixed, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, bounded-SR_h neighborhood size h=N^{eta+o(1)}, and selector evaluation time T_sel=N^{sigma+o(1)} uniformly in N.
- Model: Psys_sym^vsel contains bit-explicit EF, SATeq, bounded-SR_h, and selector-coded FormulaEval lines; its verifier reads the selector code and uses no advice.
- Same-theory condition: replacing a FormulaEval atom by all row-instantiated FormulaEval lines for RowSet(a) is sound in the proof system and preserves the lower-bound sentence's nonuniform circuit model.
- Cutoff condition: the claimed LB_N(1+epsilon) is interpreted against circuits of size N^{1+epsilon-o(1)}, while the generator overhead satisfies rho<1+epsilon.
- Non-claim: no conclusion is asserted for opaque FormulaEval or semantic selector identifiers without public extensional code.

## Equations

- visible_parameter_regime: `M_N=N^{q+o(1)},\quad |\pi|=N^{\tau+o(1)},\quad h=N^{\eta+o(1)},\quad T_{\rm sel}=N^{\sigma+o(1)}`. Valid when: Valid when the source lower-bound proof family has fixed exponent parameters and all o(1) losses are uniform over the parsed proof lines.
- selector_enumeration_charge: `\sum_{a\in FE(\pi)} M_N T_{\rm sel}(a)\le N^{q+\tau+\sigma+o(1)}`. Valid when: Applies when every FormulaEval atom has proof-visible selector code and the number of such atoms is bounded by the proof length.
- expanded_semantic_support: `K_{\rm idx}^+(\pi)=K_{\rm idx}(\pi)\cup\bigcup_{a\in FE(\pi)} RowSet(a),\qquad E_N=\left|\bigcup_{a\in FE(\pi)} RowSet(a)\right|`. Valid when: Valid when duplicate selected rows are charged once and FormulaEval expansion records all semantically touched row indices.
- gamma_visible_selector: `\Gamma_{\rm sel}(\pi)=S_{\rm dep}+S_{\rm link}+N^{q+\eta+\tau+o(1)}+N^{q+\tau+\sigma+o(1)}+N E_N`. Valid when: Requires the bit-explicit parser for EF, SATeq, bounded-SR_h, and the visible-selector RowSet enumeration just defined.
- upper_bound_falsifier: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{\rm sel}(\pi)`. Valid when: Valid after the parsed transcript simulates every proof dependency and row-expanded FormulaEval line in the same nonuniform circuit model.
- support_pressure: `N^{\rho+o(1)}+\Gamma_{\rm sel}(\pi)\ge N^{1+\epsilon-o(1)};\quad \text{if nonrow terms are subthreshold, } |K_{\rm idx}^+(\pi)|\ge N^{\epsilon-o(1)}`. Valid when: Applies only when LB_N is sound in the target circuit model and rho, q+eta+tau, and q+tau+sigma are below 1+epsilon.
- density_trichotomy: `\frac{|K_{\rm idx}^+(\pi)|}{M_N}\ge N^{\epsilon-q-o(1)}`. Valid when: Requires M_N=N^{q+o(1)} and follows from support pressure after visible-selector expansion has preserved all touched rows.

## Attempted Derivation

- Define Psys_sym^vsel by extending bit-explicit EF+SATeq+bounded-SR_h with FormulaEval-SAT atoms carrying public selector circuits Sel_a(j) and explicit formula templates.
- Run the existing Psys_bEF parser on EF, SATeq, and bounded-SR_h lines, preserving S_dep, S_link, and N^{q+eta+tau+o(1)} costs.
- For each FormulaEval atom a, enumerate all j<M_N by evaluating Sel_a(j); append exactly RowSet(a) to K_idx^+(pi) and charge N per distinct selected row for row-instantiated FormulaEval expansion.
- Build the circuit upper bound for H_N^SAT from the generator circuit and the parsed transcript; this yields C(H_N^SAT)<=N^{rho+o(1)}+Gamma_sel(pi).
- Compare the upper bound with the asserted LB_N(1+epsilon); if the right side is below N^{1+epsilon-o(1)}, the proof object supplies a falsifier to the source lower-bound claim.
- Attempt to remove proof-visible selector code; the unread-enable-bit construction gives two indistinguishable proof surfaces with different RowSet(a), blocking any advice-free parser.

Blocking gap: Unrestricted Psys_sym remains blocked at TransparentSelectorCode_N/SelectorExtensionality_N: the verifier may accept a semantic FormulaEval object without a public row-set definition or enumeration certificate.

## Falsifiers

- q<epsilon all-row expansion is a falsifier for any claimed N^{1+epsilon-o(1)} source lower bound on H_N^SAT when rho<1+epsilon.
- A hidden unread-enable-bit selector is a falsifier to surface occurrence completion for opaque FormulaEval-SAT.
- A selector circuit containing SAT-oracle gates is a falsifier to the no-advice RowSetEnumerator_N transfer because row support becomes semantic rather than syntactic.
- If q+tau+sigma>=1+epsilon, selector enumeration cost alone reaches the target threshold, so the transcript upper-bound falsifier no longer yields support pressure.
- A nonuniform advice table listing selected rows defeats target preservation unless the advice length is charged inside Gamma_sel.
- If the parsed accepting shadow is large, constructive, and useful against the same SIZE target, PRF natural-proofs tension is a barrier falsifier unless a non-large or proof-mediated escape is proved.

## Learning

Cycle 103 closes a new restricted FormulaEval fragment: proof-visible extensional selector code is target-preserving exactly with the added N^{q+tau+sigma+o(1)} enumeration term and N E_N row-expansion term. The unrestricted obstacle is now a named TransparentSelectorCode_N/SelectorExtensionality_N gap, and opaque FormulaEval has a finite hidden-selector falsifier. This is valid route-level proof-system certification, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_threshold_probe`
- Rationale: The remaining FormulaEval boundary is quantitative: visible selector code can be harmless or can consume the whole lower-bound margin. A concrete threshold experiment tests whether the route has a valid transfer certificate rather than another semantic restatement.
- Situation seed: A beta-zero SAT parity family H_N^SAT with one FormulaEval-SAT rule in Psys_sym^vsel; the rule selects rows by a public circuit Sel_sigma(j) and then expands SAT(G_N(x,j)) for the selected rows.
- Varied variable: selector evaluation exponent sigma in T_sel=N^{sigma+o(1)}
- Held-fixed controls: N=2^n and M_N=N^{q+o(1)} with fixed q., Generator size N^{rho+o(1)} with rho<1+epsilon., Proof length |pi|=N^{tau+o(1)} and bounded-SR_h parameter h=N^{eta+o(1)}., Deterministic no-advice parser and same nonuniform SIZE target model., Charge N per distinct selected row in FormulaEval expansion.
- Expected observation: When q+tau+sigma<1+epsilon and other parser terms are subthreshold, any valid LB_N proof must expose N^{epsilon-o(1)} semantic rows. When sigma crosses 1+epsilon-q-tau, enumeration overhead absorbs the margin and the route stops giving a support-pressure theorem.
- Transfer certificate needed: ProofVisibleExtensionalSelector_N: the selector code must be public, deterministic, independent of hidden advice and SAT semantics, and replaceable by row-instantiated FormulaEval lines in the same proof theory.

## Next Experiment

Attack SelectorExtensionality_N for the next stronger fragment: FormulaEval selectors may reference EF extension variables only through an acyclic row-local definition DAG. Prove inlining to public selector code with sigma+eta overhead, or build a two-row extension-dependent hidden-selector countermodel.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For Psys_sym^obdd, a FormulaEval-SAT line with an advice-free ordered-BDD row selector of size S_N=N^{s+o(1)} selecting T_N=N^{t+o(1)} rows has a valid row-expanded transcript charge S_N+T_N M_N N^{o(1)}. Combined with the already parsed Psys_bEF^- transcript, it yields the falsifier upper bound C(H_N^SAT)<=N^{rho+o(1)}+Gamma_bEF^-(pi)+S_N+N^{t+q+o(1)}; hence any claimed LB_N(1+epsilon) is false when this sum is <N^{1+epsilon-o(1)}.

## Definitions

- source object: Psys_sym^obdd proof line a=(B_N,EvalRule,wit) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)} and B_N an ordered binary decision diagram over log N row-index bits.
- target object: row-expanded occurrence transcript K_idx(pi) and a nonuniform circuit upper-bound falsifier for the asserted lower bound C(H_N^SAT)>N^{1+epsilon-o(1)}.
- controlled interface: RowSetEnumerator_N(B_N) verifies the OBDD certificate, outputs every x with B_N(x)=1 exactly once, and expands each selected row into its M_N explicit FormulaEval-SAT occurrences.
- target-preserving condition: B_N, its variable order, and any count certificate are inside the proof transcript; enumeration is deterministic and advice-free; FormulaEval reads explicit formula bits; no semantic SAT oracle or nonuniform row selector is used.

## Assumptions

- Length regime is N->infty with row universe [N], row index length log N+O(1), and M_N=N^{q+o(1)} SAT queries per row.
- Generator G_N is uniform enough to emit formula encodings in N^{rho+o(1)} size or time; its output formulas have polylogarithmic length and occurrence addresses are explicit.
- The Psys_bEF^- portion of pi is already parsed by Gap98-SRhNormalForm, giving Gamma_bEF^-(pi) without uncharged formula identity or unwitnessed SAT-extensionality.
- OBDD syntax is locally checkable: acyclic graph, one root, ordered variables, binary edges, accepting terminal, and no advice outside the written selector certificate.
- The target lower bound is nonuniform circuit size for the finite truth table H_N^SAT; uniformity is required only for the parser/enumerator, not for the circuit family falsifying LB_N.
- FormulaEval is occurrence-transparent: changing an unread formula bit is allowed in the countermodel unless the bit is represented in the expanded transcript or a valid UExt witness is supplied.

## Equations

- query_count: `M_N=N^{q+o(1)}`. Valid when: Valid when the beta-zero SAT-parity source family fixes a polynomial query exponent q and the generator encodings have only subpolynomial slack.
- selector_support: `T_N=|\{x\in[N]:B_N(x)=1\}|=N^{t+o(1)}`. Valid when: Valid when the OBDD row selector is part of the proof transcript and its accepted rows are counted by deterministic enumeration.
- obdd_formulaeval_charge: `\mathrm{Charge}_{FE}^{obdd}(N)=S_N+T_N M_N N^{o(1)}=N^{\max\{s,t+q\}+o(1)}`. Valid when: Applies after OBDD syntax verification and row enumeration preserve occurrence-level formula access without semantic row advice.
- combined_transcript: `\Gamma_{103}(\pi)=\Gamma_{bEF}^-(\pi)+\mathrm{Charge}_{FE}^{obdd}(N)`. Valid when: Requires every non-FormulaEval proof line to be covered by the Gap98-SRhNormalForm parser and every FormulaEval line to use the certified OBDD interface.
- upper_bound_falsifier: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{103}(\pi)`. Valid when: Valid when the parsed transcript and generator together determine all queried row parities in the same finite nonuniform circuit model.
- exponent_gate: `\max\{\rho,\gamma_{bEF},s,t+q\}<1+\epsilon \Rightarrow C(H_N^{SAT})<N^{1+\epsilon-o(1)}`. Valid when: Applies when \Gamma_{bEF}^-(\pi)\le N^{\gamma_{bEF}+o(1)} and all summands are measured in the same N-indexed circuit-size scale.

## Attempted Derivation

- Fix N and a Psys_sym^obdd proof pi of LB_N(1+epsilon) about H_N^SAT(x)=xor_{j<=M_N}SAT(G_N(x,j)).
- Apply the previously closed Gap98-SRhNormalForm parser to all Psys_bEF^- lines and record Gamma_bEF^-(pi).
- For each FormulaEval line, verify the OBDD certificate: graph acyclicity, ordered variable labels, legal terminals, unique root, and explicit encoding inside pi.
- Run DFS through the OBDD. Because the diagram is ordered and deterministic, every row x has a unique root-to-terminal path; accepting rows are output once, with skipped variables expanded as free bits.
- Charge O(S_N) for selector verification and O(T_N log N) enumeration overhead, absorbed into S_N+T_NN^{o(1)}.
- For every emitted row x, expand the M_N formulas G_N(x,j) at occurrence level and attach the SAT-evaluation dependency list; this contributes T_N M_N N^{o(1)} bits/gates.
- Substitute this FormulaEval charge into the existing Gamma_bEF transcript ledger and combine with the generator overhead N^{rho+o(1)} to obtain C(H_N^SAT)<=N^{rho+o(1)}+Gamma_bEF^-(pi)+S_N+N^{t+q+o(1)}.
- Conclude the route-specific falsifier: if the last bound is below N^{1+epsilon-o(1)}, then the finite lower-bound sentence LB_N(1+epsilon) cannot be a true target statement in the stated nonuniform circuit model.

Blocking gap: The proof is complete for certified OBDD selectors but still blocked for arbitrary AC0 selectors at AC0SupportSensitiveEnumerator_N and for semantic FormulaEval at UExtWitnessability.

## Falsifiers

- Nontransparent FormulaEval line with an omitted eval-critical row gives the private-row falsifier Q_pi(omega)=Q_pi(omega') but different H_N^SAT(x*).
- Arbitrary AC0 selector without a certified OBDD/disjoint-cover enumerator must pay scan charge N^{1+q+o(1)} or is a semantic-oracle escape.
- OBDD selector size S_N=N^{s+o(1)} with s>=1+epsilon destroys the low-cost falsifier threshold.
- Selector order, support count, or hard-row choice supplied as advice invalidates the target-preserving condition.
- Unwitnessed SAT-extensionality or formula identity bypasses occurrence completion and remains outside Psys_sym^obdd.
- Generator overhead rho>=1+epsilon prevents the transcript bound from contradicting LB_N(1+epsilon).

## Learning

Cycle 103 promotes a new restricted selector class: certified ordered BDD FormulaEval is transparent and pays S_N+T_NM_NN^{o(1)}, extending interval and disjoint-subcube expansion without broadening to arbitrary AC0. The exact non-claim is sharp: unsupported AC0 selectors still pay scan charge or become semantic-oracle/private-row falsifier cases.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and parameter-calibration experiment for FormulaEval selector fragments.`
- Rationale: The branch needs a concrete selector model that preserves the target lower-bound statement while deciding whether support-sensitive FormulaEval expansion is real or hidden semantic advice.
- Situation seed: A padded SAT-parity family H_N^SAT with M_N=N^{q+o(1)} queries per row and a Psys_sym proof line whose FormulaEval rows are selected by a width-W_N ordered BDD over log N row bits.
- Varied variable: BDD size exponent s, with selected-row density t and query exponent q recorded separately.
- Held-fixed controls: Generator overhead rho and polylogarithmic formula length are fixed., The Psys_bEF^- parser ledger Gamma_bEF^-(pi) is held fixed., The OBDD variable order and graph are written inside the proof, not supplied as advice., FormulaEval must be occurrence-transparent; no semantic SAT oracle is allowed.
- Expected observation: For s,t+q below 1+epsilon and rho,gamma_bEF below the same threshold, the expanded transcript gives a subthreshold circuit upper bound and falsifies LB_N(1+epsilon). If s or t+q reaches the threshold, the selector no longer yields a low-cost contradiction.
- Transfer certificate needed: A formal RowSetEnumerator_N proof for ordered BDDs plus a proof-quality check that the expanded rows bind every parity-relevant FormulaEval occurrence before the intuition may enter the theorem packet.

## Next Experiment

Instantiate Psys_sym^obdd on one beta-zero SAT-parity proof line, write the OBDD bit fields and verifier pseudocode, then run the exponent gate for q<epsilon, q=epsilon, and q>epsilon with Gamma_bEF^-(pi)=N^{gamma+o(1)}.
