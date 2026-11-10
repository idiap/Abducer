# cycle-0102

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization - cycle 102 SR_h normal form audit

## Candidate Lemma

For the restricted system Psys_bEF^- with bit-explicit EF variables, SATeq links, and one bounded self-reduction rule schema SR_h^bit, every accepted proof line has a parsed occurrence transcript; every SR_h^bit invocation contributes exactly its listed row-slot roots times its node/leaf overhead to B_SR(pi), hence no hidden semantic advice is available inside the bounded-SR part.

## Definitions

- source object: an accepted Psys_bEF^- proof pi of LB_N(1+epsilon) for the beta-zero parity carrier H_N^SAT(a)=xor_{j<M_N} SAT(G_N(a,j)), with a in [N], M_N=N^{q+o(1)}, L_N=(log N)^d, d>1, and generator circuit size N^{rho+o(1)}.
- target object: the charged occurrence transcript Gamma_bEF(pi)=S_dep(pi)+S_link(pi)+B_SR(pi)+E_N N used to build a nonuniform upper-bound falsifier for the claimed source lower bound, not a proof of P != NP.
- controlled interface: a parser mapping each bit-explicit proof line to row-slot roots r=(a,j), formula-node addresses u, branch or leaf words z, parent pointers, and touched occurrence-neighborhood lists O(r,u,z).
- target-preserving condition: the parser is valid only when row-slot roots are explicitly encoded or uniformly enumerable, extension dependencies expose their support, bounded-SR leaves are charged by eta/tau overheads, and no FormulaEval-SAT semantic oracle supplies hidden row information.
- row-slot encoding: a root r=(a,j) uses ceil(log N)+ceil(log M_N)=(1+q+o(1))log N bits; occurrence addresses use O(log L_N) bits per clause/literal position.
- SR_h^bit record fields: tag SR_h, line id ell, parent line ids, root list R_ell, node address u in U_ell, branch/leaf word z in V_ell, child pointers, sign bit, and occurrence list O_ell(r,u,z) of triples (formula id, clause index, literal position).
- local verifier: for fixed h it checks that each child formula is obtained from the parent by assigning at most h variables and simplifying clauses, using only listed occurrences and the bit-explicit generator G_N.
- barrier status: the lemma is syntactic and advice-free; it is relativizing as an occurrence parser and therefore does not cover real SAT-semantic FormulaEval lines without FE_Extract_N.

## Assumptions

- Psys_bEF^- contains no symbolic FormulaEval-SAT comprehension rule and no extension variable whose defining support is available only as nonuniform semantic advice.
- The bounded-SR depth h is fixed, and the simplification verifier for one SR step touches at most L_N^{O_h(1)} formula bits.
- Each SR invocation ell has |R_ell| row-slot roots, |U_ell|<=N^{eta_ell+o(1)} node addresses, and |V_ell|<=N^{tau_ell+o(1)} branch/leaf choices, with eta=max eta_ell and tau=max tau_ell over the proof family.
- The proof family is size-bounded so the sum over SR invocations is absorbed into N^{o(1)} or is explicitly included in the displayed summation.
- Uniformity/advice regime: the parser may be nonuniform in N but may not receive extra row labels or SAT truth bits not written in pi.

## Equations

- row_slot_index_bits: `b_{idx}(N)=\lceil \log N\rceil+\lceil \log M_N\rceil=(1+q+o(1))\log N`. Valid when: Valid when row-slot roots are pairs from [N] times [M_N] and M_N=N^{q+o(1)} is part of the source carrier definition.
- local_occurrence_neighborhood: `|O_\ell(r,u,z)|\le L_N^{c_h}=N^{o(1)}`. Valid when: Valid when h is fixed and the SR verifier checks only bounded-depth substitution and clause simplification in polylogarithmic-size generated formulas.
- bounded_SR_charge_exact: `B_{SR}(\pi)=\sum_{\ell\in SR(\pi)} |R_\ell|\,|U_\ell|\,|V_\ell|\,L_N^{O_h(1)}`. Valid when: Valid when every SR_h proof record explicitly lists roots, node addresses, branch words, and occurrence neighborhoods charged by the parser.
- bounded_SR_exponent_bound: `B_{SR}(\pi)\le N^{q+\eta+\tau+o(1)}`. Valid when: Applies after the proof family has N^{q+o(1)} total charged roots, N^{eta+o(1)} node overhead, N^{tau+o(1)} leaf overhead, and only polylogarithmic local verification factors.

## Attempted Derivation

- Define Psys_bEF^- syntax with bit-explicit EF extension definitions, SATeq quotient links, and SR_h^bit records; exclude FormulaEval-SAT from this restricted theorem.
- For an SR_h^bit record, parse fields tag, line id, parent ids, root list R_ell, row-slot index r=(a,j), node address u, branch word z, child pointers, sign bit, and occurrence-neighborhood list O_ell(r,u,z).
- Use b_idx=(1+q+o(1))log N to encode row-slot roots and O(log L_N) bits for local formula occurrences; verify each SR child by local substitution on at most h variables and clause simplification.
- Charge each verified SR local check to |R_ell||U_ell||V_ell|L_N^{O_h(1)}; summing gives B_SR(pi) and, under the exponent assumptions, B_SR(pi)<=N^{q+eta+tau+o(1)}.
- Run line induction: EF definitions add transitive support S_dep, SATeq links add quotient support S_link, SR_h lines add B_SR, and residual bad rows add E_N N by equality patching.
- Construct the transcript-driven circuit: compute G_N with size N^{rho+o(1)}, consult parsed SAT/SR transcript entries, xor the M_N slot values, and patch E_N rows.
- Derive C(H_N^SAT)<=N^{rho+o(1)}+O(Gamma_bEF(pi)); if this is below N^{1+epsilon-o(1)}, the lower-bound sentence LB_N(1+epsilon) is falsified in the same nonuniform model.
- Attempt to extend the proof to Psys_sym FormulaEval-SAT; classify the mechanism. Expansion is charged N^{1+q+o(1)}, while an unexpanded semantic line admits the private-row flip unless FE_Extract_N is supplied.

Blocking gap: No blocking gap remains for the restricted SR_h^bit normal form and line-induction packet. The full Psys_sym theorem is blocked at FE_Extract_N or RowSetEnumerator_N for symbolic FormulaEval-SAT.

## Falsifiers

- Hidden extension support: an EF variable whose dependency set is not revealed by the transitive bit-DAG invalidates S_dep and defeats the parser.
- Semantic FormulaEval-SAT: an unexpanded symbolic line can hide a private row-slot label; the private-row falsifier changes H_N^SAT while preserving surfaced occurrences.
- Threshold collapse: if rho or q+eta+tau reaches 1+epsilon, Gamma_bEF no longer gives a subthreshold contradiction to LB_N(1+epsilon).
- Nonuniform leakage: a row selector supplied as advice rather than by RowSetEnumerator_N can fake occurrence support without paying N^{1+q+o(1)} expansion.
- SR leaf overreach: if the bounded-SR rule imports an uncharged SAT solver for leaves, the B_SR(pi)<=N^{q+eta+tau+o(1)} accounting is not valid.
- Model mismatch: a claim about full EF+SAT or Psys_sym cannot inherit the Psys_bEF^- theorem unless every semantic rule is classified and charged.

## Learning

Cycle 102 upgrades the bounded-SR_h subgoal from an exponent slogan to a parser theorem for the explicit rule schema: SR_h contributes exactly B_SR(pi) to Gamma_bEF, and the line induction gives a valid restricted LB_N falsifier. The remaining full-system issue is sharply isolated as FE_Extract_N for symbolic FormulaEval-SAT, not generic naturalness, relativization, or P vs NP itself.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch needs a concrete target-preserving check for whether symbolic FormulaEval can be surfaced as occurrence support after SR_h normalization; another abstract barrier restatement would not decide FE_Extract_N.
- Situation seed: Consider a beta-zero parity carrier with N source rows and M_N=N^{q+o(1)} polylog-size generated SAT slots. Add one Psys_sym FormulaEval line that claims to evaluate SAT(G_N(a,j)) for all j in RowSet(a), but expose only the symbolic formula-evaluation gate rather than row-slot occurrences.
- Varied variable: q, the slot exponent M_N=N^{q+o(1)}, varied across q<epsilon, q=epsilon+o(1), and q>epsilon while keeping beta=0.
- Held-fixed controls: Generator size remains N^{rho+o(1)} with rho<1+epsilon., Formula length remains L_N=(log N)^d with d>1, so SAT-circuit substitution has N^{o(1)} exponent debt., The restricted Psys_bEF^- parser, SR_h bit fields, and equality-patching cost E_N N are held fixed., No advice-only row selector is allowed unless it is explicitly classified as semantic-oracle leakage.
- Expected observation: Expanded FormulaEval pays N^{1+q+o(1)} and is too expensive for the subthreshold falsifier, while unexpanded FormulaEval lets a private row-slot flip change the parity carrier. The q-trichotomy shows enumeration falsifies q<epsilon, near-full contact is forced at q=epsilon, and q>epsilon leaves only absolute support pressure.
- Transfer certificate needed: Before this intuition may affect proof obligations, prove FE_Extract_N or RowSetEnumerator_N for the selected Psys_sym fragment, including uniform row-slot enumeration, no hidden advice, and a nonrelativizing reason real SAT semantics blocks the private-row countermodel.

## Next Experiment

Instantiate RowSetEnumerator_N for one transparent Psys_sym^sel fragment, preferably interval-union or AC0 row selectors, and decide whether FormulaEval-SAT is an expanded axiom schema with N^{1+q+o(1)} charge or a semantic oracle exposed by the private-row falsifier.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Restricted theorem: in Psys_sym^{AC0-sel}, where every FormulaEval-SAT row selector is an explicitly encoded constant-depth Boolean circuit on row-index bits, FormulaEval is target-preserving only after RowSet enumeration and N*E_N expansion charge. Under the existing residual-patching lemma, any valid accepted proof of LB_N(1+epsilon) with subthreshold dependency/link overhead must satisfy K_idx^+(pi)>=N^{epsilon-o(1)}; otherwise the parsed transcript gives a circuit upper-bound falsifier for the claimed lower bound.

## Definitions

- source object: an accepted Psys_sym^{AC0-sel} proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, and G_N uniformly bit-encoded.
- target object: nonuniform Boolean circuits for the n-bit function H_N^SAT, measured in N-units, together with the expansion-aware semantic support K_idx^+(pi).
- controlled interface: deterministic no-advice parser P_N maps pi and each explicit selector circuit C_a to RowSet(a)={j<=M_N:C_a(j)=1}, then charges selected rows to K_idx(pi) or E_N(pi).
- target-preserving condition: every selected row must expand to the same bit-level formula G_N(x,j) inside the same proof language; selector evaluation may not call SAT, oracle truth, hidden advice, or real-formula semantics.
- Psys_sym^{AC0-sel}: Psys_bEF plus FormulaEval-SAT atoms of the form EvalSAT(C_a,G_N), where C_a is encoded as a depth-d AC0 circuit over ceil(log M_N) row bits with size L_a<=N^{lambda+o(1)}.
- K_idx(pi): union of row indices explicitly touched by row-faithful SATeq, bounded-SR_h, or expanded FormulaEval lines.
- E_N(pi): number of additional FormulaEval row instances charged by expanding explicit selector atoms, counted with union charge for support and with multiplicity only in syntactic transcript size.
- S_dep(pi) and S_link(pi): extension-DAG dependency and link-traversal costs already defined in the Psys_bEF parser packet.

## Assumptions

- Model: nonuniform Boolean SIZE for H_N^SAT, bit-explicit EF+SATeq+bounded-SR_h proof lines, and FormulaEval restricted to syntactic AC0 row selectors.
- Regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, bounded-SR_h locality h=N^{eta+o(1)}, generator overhead N^{rho+o(1)}, and rho<1+epsilon.
- Uniformity/advice: the parser receives N and pi only; all selector circuits, generator bits, row encodings, and rule parameters are displayed in pi or uniformly computable from N.
- Cutoff: the theorem is only a parser/transfer obstruction for the beta-zero H_N^SAT carrier; it is not a proof of P != NP and does not claim unrestricted Psys_sym soundness.
- Same-theory condition: selector syntax, EF extension definitions, SATeq row encodings, and FormulaEval expansion all use one row-index convention, so the parser cannot silently switch from occurrence labels to formula labels.
- Naturalness condition: if the parsed transcript is converted into a dense constructive truth-table property, then natural-proofs pressure applies; the lemma itself only proves the support and circuit-upper-bound transfer.

## Equations

- row_set: `RowSet(a)={j in [M_N] : C_a(j)=1}`. Valid when: Valid when C_a is an explicitly encoded syntactic selector circuit over row-index bits, not an oracle predicate or semantic SAT condition.
- enumeration_time: `T_enum(a) <= M_N * L_a * polylog(N) = N^{q+lambda+o(1)}`. Valid when: Valid when selector depth is constant, selector size is L_a<=N^{lambda+o(1)}, and brute-force scanning of all M_N row indices is allowed by the parser.
- expansion_support: `K_idx^+(pi)=|K_idx(pi)|+E_N(pi)`. Valid when: Valid when FormulaEval rows are either already present in row-faithful support or charged as additional expanded row instances without double-counting support.
- gamma_ac0sel: `Gamma_AC0sel(pi)=S_dep(pi)+S_link(pi)+N^{q+eta+tau+o(1)}+N*E_N(pi)`. Valid when: Valid when the Psys_bEF parser costs are inherited and each charged FormulaEval row contributes an N-bit row expansion to the transcript simulation.
- upper_bound_falsifier: `C(H_N^SAT) <= N^{rho+o(1)} + Gamma_AC0sel(pi)`. Valid when: Applies after residual patching is invoked with the same generator G_N, no advice leakage, and the parsed transcript covers every proof-used SAT row.
- forced_support: `LB_N(1+epsilon) and subthreshold Gamma imply K_idx^+(pi) >= N^{epsilon-o(1)}`. Valid when: Requires the claimed lower-bound sentence C(H_N^SAT)>N^{1+epsilon-o(1)}, rho<1+epsilon, and all non-support parser costs below N^{1+epsilon-o(1)}.
- density_trichotomy: `K_idx^+(pi)/M_N >= N^{epsilon-q-o(1)}`. Valid when: Valid when the forced-support inequality holds and M_N=N^{q+o(1)} is the total number of beta-zero SAT rows.

## Attempted Derivation

- Define Psys_sym^{AC0-sel}: start with the already audited bit-explicit Psys_bEF rules, then allow FormulaEval-SAT only when the proof line displays a constant-depth selector circuit C_a over row bits and a row-template pointer to G_N(x,j).
- For each selector line, run RowSetEnumerator_N by scanning j=1,...,M_N and evaluating C_a(j). This is deterministic, advice-free, and uses no SAT semantics. The parser appends each selected j to the semantic support list or to the FormulaEval expansion charge E_N.
- Run the existing line-induction proof for EF+SATeq+bounded-SR_h. SATeq preserves row identity, bounded-SR_h contributes the Gamma_bEF local term, and AC0 FormulaEval contributes exactly N*E_N in transcript expansion because each selected row instantiates an N-bit truth-table row predicate.
- Apply the previously isolated residual-patching lemma: if the parsed transcript plus generator has total cost below N^{1+epsilon-o(1)}, then H_N^SAT has a nonuniform circuit of size at most N^{rho+o(1)}+Gamma_AC0sel(pi), contradicting LB_N(1+epsilon).
- Infer forced support K_idx^+(pi)>=N^{epsilon-o(1)} under subthreshold non-support costs, and divide by M_N=N^{q+o(1)} to recover the support-density trichotomy: q<epsilon gives a row-enumeration falsifier, q=epsilon+o(1) forces near-full contact, q>epsilon leaves only weak density but still absolute support pressure.

Blocking gap: This is not an unrestricted Psys_sym theorem. The named gap is TransparentSelectorCode_N for FormulaEval atoms whose row predicate is extension-defined, semantic, or dependent on SAT truth values rather than proof-visible selector syntax.

## Falsifiers

- falsifier: if q<epsilon and all Gamma_AC0sel non-support costs are subthreshold, enumerating all selected rows yields C(H_N^SAT)<N^{1+epsilon-o(1)}, so the claimed LB_N source statement is false.
- falsifier: an opaque FormulaEval oracle with one unread enabled row has identical displayed syntax to the empty selector but different semantic support, invalidating surface occurrence completion.
- falsifier: an extension-defined selector whose bits depend on SAT(G_N(x,j)) is not target-preserving because enumeration would require the very semantic hardness the parser is supposed to certify.
- falsifier: nonuniform selector advice not printed in pi can hide K_idx rows and destroys the no-advice live inference-quality packet.

## Learning

Cycle 102 adds a new restricted theorem rather than a slogan: AC0 row selectors are transparent exactly when their code is proof-visible, because brute-force RowSet enumeration charges K_idx^+ and preserves the Gamma transfer. The unrestricted Psys_sym gap is now TransparentSelectorCode_N; opaque FormulaEval remains a valid semantic falsifier, not a parser theorem and not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and threshold calibration for AC0-selector FormulaEval.`
- Rationale: The branch has already closed interval-union selectors; the next concrete target-preserving case is a syntactic AC0 selector that can represent scattered rows and tests whether enumeration charge, not interval structure, is the real invariant.
- Situation seed: Let H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^q. Add one FormulaEval line whose selector is a depth-2 DNF of equality tests selecting a set A_N of t=N^alpha row indices, with every equality constant printed in the proof.
- Varied variable: alpha, the selected-row exponent in t=N^alpha, while keeping depth and generator overhead fixed.
- Held-fixed controls: The proof model is Psys_sym^{AC0-sel} with printed selector circuits and no semantic selector oracle., The generator G_N, row-index encoding, and SAT formula template are uniform and bit-identical across all rows., The lower-bound target remains C(H_N^SAT)>N^{1+epsilon-o(1)} in nonuniform Boolean SIZE., The parser is deterministic, no-advice, and only charges rows it can enumerate syntactically.
- Expected observation: For alpha<epsilon, the expanded selector line is a subthreshold support object and should trigger the circuit-upper-bound falsifier if other Gamma terms are small; for alpha>=epsilon, the line pays the forced support charge and no longer pretends to be a free semantic shortcut.
- Transfer certificate needed: TransparentSelectorCode_N plus ResidualPatch_N: the proof must certify that the printed AC0 selector enumerates exactly the rows whose SAT values affect the proof and that expanded row support yields the stated nonuniform circuit upper bound.

## Next Experiment

Dependency-check ResidualPatch_N with Gamma_AC0sel: verify that N^{rho+o(1)}+S_dep+S_link+N^{q+eta+tau+o(1)}+N*E_N<N^{1+epsilon-o(1)} is exactly the falsifier inequality, then test whether extension-defined selector circuits in Psys_sym satisfy TransparentSelectorCode_N or yield a smaller semantic countermodel.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For Psys_sym^cube, a transparent FormulaEval-SAT line whose row selector is a certified disjoint union of row-address subcubes expands to an occurrence transcript of cost T_N N^{q+o(1)}, where T_N is the selected-row count. Hence a claimed beta-zero lower bound LB_N(1+epsilon) is falsified whenever the generator, parsed proof ledger, subcube expansion, and residual correction all stay below N^{1+epsilon-o(1)}.

## Definitions

- source object: a Psys_sym^cube proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)} and row universe |X_N|=N.
- target object: a nonuniform circuit upper bound for H_N^SAT, used only as a route-level falsifier for the asserted lower-bound sentence.
- controlled interface: RowSetEnumerator_N takes each FormulaEval selector line encoded as a certified disjoint subcube list S_N over ceil(log N) row-address bits and emits all selected row indices plus the formula occurrence neighborhoods touched by G_N(x,j).
- target-preserving condition: the parser is advice-free, bit-explicit, and SAT-occurrence transparent; no FormulaEval line may use unwitnessed SAT extensionality, hidden row advice, or a semantic oracle.
- T_N(S_N) is the number of selected rows after filtering addresses outside X_N.
- Psys_sym^cube extends the already parsed Psys_bEF^- ledger by only this transparent subcube FormulaEval mechanism.

## Assumptions

- Model: Psys_bEF^- rules, SATeq, and bounded-SR_h have the cycle-0099 Gamma_bEF parser, and FormulaEval is added only through explicit subcube selector lines.
- Uniformity: G_N, selector parsing, subcube disjointness checking, and row enumeration are deterministic advice-free procedures running within the stated transcript budget.
- Regime: N tends to infinity, M_N=N^{q+o(1)}, T_N=N^{t+o(1)}, generator overhead is N^{rho+o(1)}, and all o(1) losses are uniform along the proof family.
- Subcube certificate: S_N={C_a} has disjoint row-address subcubes C_a with free dimensions d_a and list size at most T_N N^{o(1)}; overlap or hidden compression must be charged separately.
- Target class: the conclusion is an unrestricted nonuniform circuit upper bound for H_N^SAT, not a P-uniform algorithm and not a proof of P != NP.
- Barrier status: the theorem is non-natural only because it is a sparse proof-transcript falsifier; making the selector dense and polytime decidable would trigger a natural-property-style disqualifier.

## Equations

- selected_row_count: `T_N(S_N)=sum_a 2^{d_a}`. Valid when: Valid when S_N is a certified disjoint subcube list over the row-address cube and empty addresses beyond N are filtered uniformly.
- rowset_enumerator_cost: `Time(RowSetEnumerator_N(S_N))=T_N(S_N) N^{o(1)}`. Valid when: Valid when the subcube list size is at most T_N N^{o(1)} and enumeration uses lexicographic or Gray-code traversal of free coordinates.
- formulaeval_expansion_charge: `E_FE(S_N)=T_N(S_N) M_N N^{o(1)}=T_N(S_N) N^{q+o(1)}`. Valid when: Applies after every selected row is expanded into all M_N generated SAT formula occurrences and FormulaEval is not treated semantically.
- gamma_cube_ledger: `Gamma_cube(pi)=S_dep(pi)+S_link(pi)+N^{q+eta+tau+o(1)}+T_N(S_pi)N^{q+o(1)}`. Valid when: Valid when the Psys_bEF^- ledger is already parsed and the only new proof mechanism is transparent subcube FormulaEval.
- upper_bound_falsifier: `C(H_N^{SAT}) <= N^{rho+o(1)}+Gamma_cube(pi)+N^{r+1+o(1)}`. Valid when: Requires the generator circuit, parsed transcript, transparent FormulaEval expansion, and sparse residual correction to compute the same H_N^SAT family.
- exponent_threshold: `max{rho,s_dep,s_link,q+eta+tau,t+q,r+1}<1+epsilon => LB_N(1+epsilon) is false`. Valid when: Valid when S_dep=N^{s_dep+o(1)}, S_link=N^{s_link+o(1)}, T_N=N^{t+o(1)}, and LB_N asserts unrestricted circuit lower bound N^{1+epsilon-o(1)}.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside MCSP / Meta-Complexity Carrier Transfer; source object: a Psys_sym^cube proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)} and row universe |X_N|=N.; target object: a nonuniform circuit upper bound for H_N^SAT, used only as a route-level falsifier for the asserted lower-bound sentence.; Model: Psys_bEF^- rules, SATeq, and bounded-SR_h have the cycle-0099 Gamma_bEF parser, and FormulaEval is added only through explicit subcube selector lines..
- Fix N and parse pi using the cycle-0099 Psys_bEF^- line induction, obtaining S_dep(pi), S_link(pi), and the bounded-SR_h term N^{q+eta+tau+o(1)}.
- For each FormulaEval selector line in Psys_sym^cube, read the certified disjoint subcube list S_N={C_a}; verify syntactic disjointness and address bounds within the proof-line charge.
- Enumerate each C_a by traversing its free coordinates and output each row x once. The total emitted rows are T_N=sum_a 2^{d_a}, so enumeration costs T_N N^{o(1)}.
- For every emitted row x and every j<=M_N, invoke the advice-free generator G_N(x,j), expose the bit-level formula encoding, and attach the SAT occurrence neighborhood required by the already parsed SATeq/bounded-SR_h rules.
- Hardwire the parsed proof transcript and transparent expansion into a nonuniform circuit for H_N^SAT; combine it with the generator circuit N^{rho+o(1)} and any residual row correction N^{r+1+o(1)}.
- Compare the resulting upper-bound exponent max{rho,s_dep,s_link,q+eta+tau,t+q,r+1} with the claimed lower-bound exponent 1+epsilon. If it is smaller, the proof transcript is a falsifier for LB_N(1+epsilon).

Blocking gap: The derivation does not give a support-sensitive enumerator for arbitrary AC0 row selectors and does not handle semantic FormulaEval-SAT without UExtWitnessability.

## Falsifiers

- A FormulaEval line charges |RowSet|N^q for an arbitrary AC0 predicate without a valid support-sensitive RowSetEnumerator_N certificate.
- A selector uses nonuniform advice or a hard-row ranking mechanism to choose rows; this may identify nonuniform hard rows but does not transfer to a uniform language lower bound.
- A nontransparent FormulaEval-SAT rule omits an eval-critical row/formula bit and lacks UExtWitnessability, giving the private-row falsifier.
- A subcube list is compressed with overlaps or implicit difference operations but is charged as disjoint without paying duplication or disjointness verification.
- The expansion exponent t+q or the scan exponent 1+q reaches 1+epsilon, so the transcript no longer contradicts LB_N(1+epsilon).
- A dense polytime-decidable useful selector property is introduced to repair support enumeration, triggering natural-property largeness pressure rather than a sparse proof-transcript obstruction.

## Learning

Cycle 102 upgrades the FormulaEval boundary from intervals to certified disjoint subcube-union selectors: the valid expansion charge is T_N N^{q+o(1)}, so the low-cost transcript falsifier uses exponent t+q. The cycle also prevents an invalid promotion to arbitrary AC0 selectors: without a support-sensitive enumerator they pay scan charge N^{1+q+o(1)} or become semantic-oracle/private-row cases. This is paper-level obstruction progress only, not progress on P != NP itself.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and transfer calibration for FormulaEval selectors.`
- Rationale: The branch needs a concrete target-preserving test because the remaining paper gap is not generic MCSP hardness but whether FormulaEval support can be exposed at bit level with the correct exponent charge.
- Situation seed: A Psys_sym^cube proof line selects rows x in X_N by a certified disjoint union of subcubes in {0,1}^{ceil(log N)}; each selected row expands all M_N=N^{q+o(1)} SAT instances G_N(x,j) used in H_N^SAT.
- Varied variable: The free-dimension/support exponent t, defined by T_N=sum_a 2^{d_a}=N^{t+o(1)}.
- Held-fixed controls: Generator G_N remains advice-free with overhead N^{rho+o(1)} and polylogarithmic formula length., The lower-bound claim remains LB_N(1+epsilon) against unrestricted nonuniform circuits., The proof system remains Psys_bEF^- plus transparent subcube FormulaEval; no semantic FormulaEval oracle is added., The SAT occurrence encoding and bounded-SR_h parser ledger from cycle-0099 are held fixed.
- Expected observation: As t varies, the FormulaEval contribution changes exactly as N^{t+q+o(1)}; t=0 behaves like sparse row contact, t=1 recovers full-row N^{1+q+o(1)} expansion, and any uncharged semantic shortcut is exposed by a private-row falsifier.
- Transfer certificate needed: A formal RowSetEnumerator_N proof with disjointness verification, bounded duplication, advice-free generator calls, and equality to the target H_N^SAT row semantics before the exponent observation may enter the proof obligations.

## Next Experiment

Attempt RowSetEnumerator_N for a stricter AC0 fragment: read-once DNF or certified decision-DAG selectors over row-address bits. Compute whether enumeration charge is support-sensitive or necessarily scan-level, and update the FormulaEval classification table with a proof or countermodel.
