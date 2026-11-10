# cycle-0090

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta-zero SAT parity carrier, any bounded self-reduction leaf solver whose induced parity carrier is wrong on fewer than N^{epsilon-o(1)} source rows gives a subthreshold circuit for H_N^{SAT}. Thus a Psys_h proof route using EqSAT plus h-round SAT self-reduction is valid only after certifying constrained residual distance against these induced easy codewords.

## Definitions

- source object: H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)), |x|=N, M_N<=N^{q+o(1)}, formula length L_N=(log N)^d with d>1, and generator circuit size N^{rho+o(1)}.
- target object: SAT notin P/poly, obtained only route-conditionally from a valid source lower bound C(H_N^{SAT})>N^{1+epsilon-o(1)} when q,rho<1+epsilon and L_N=N^{o(1)}.
- controlled interface: beta-zero batched substitution plus a parsed EF+EqSAT+SR_h transcript represented by EqSAT quotient labels and h rounds of self-reduction OR constraints over generated formulas.
- target-preserving condition: the generator and parser are uniform, q,rho<1+epsilon, every leaf solver and residual patch is charged to the source circuit budget, and no nonuniform advice is hidden in the proof transcript.
- Psys_h is EF augmented with formula-equivalence axioms EqSAT and explicit self-reduction clauses SAT(F)=OR_a SAT(F|a) for h rounds fixing b variables per round on formulas reachable from the generated range.
- eta_N=b h/log N is the SR expansion exponent, so the number of leaves per queried formula is 2^{bh}=N^{eta_N+o(1)}.
- A_N is a leaf-label circuit of size N^{tau+o(1)} on the h-round restricted formulas, and H_{A,h} is the parity carrier obtained by OR-evaluating A_N on all SR leaves for each generated query.

## Assumptions

- Circuit lower bounds are nonuniform Boolean circuit lower bounds over source length N; P/poly target circuits are nonuniform but the reduction from a SAT circuit to H_N is uniform.
- The beta-zero regime means L_N=(log N)^d, hence L_N^c=N^{o(1)} for every fixed target exponent c.
- The row-error set R_N={x:H_{A,h}(x) != H_N^{SAT}(x)} has size E_N=N^{e+o(1)} and is charged by equality patches of O(N) gates per row.
- The SR parser branch is conditional: the proof transcript must expose only EqSAT quotienting and bounded SR OR constraints; arbitrary EF semantic extension variables are not yet covered.
- The source lower-bound claim under audit is C(H_N^{SAT})>N^{1+epsilon-o(1)}; the lemma is a route falsifier, not a proof of this lower bound.

## Equations

- beta_zero_target_substitution: `C(H_N^{SAT}) \le N^{\rho+o(1)}+M_N\,L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when SAT has size L^c circuits on all generated length-L_N formulas and L_N=(log N)^d makes every fixed c contribute only N^{o(1)} overhead.
- bounded_SR_leaf_solver_upper_bound: `C(H_{A,h}) \le N^{\rho+o(1)}+N^{q+\eta_N+\tau+o(1)}`. Valid when: Applies when the parsed self-reduction tree has 2^{bh}=N^{eta_N+o(1)} leaves per generated query and A_N has size N^{tau+o(1)} with no hidden advice.
- row_residual_patch_bound: `C(H_N^{SAT}) \le C(H_{A,h})+O(E_N N) \le N^{\max\{\rho,q+\eta_N+\tau,1+e\}+o(1)}`. Valid when: Requires that H_{A,h} and H_N^{SAT} disagree on exactly E_N=N^{e+o(1)} source rows and that equality tests for source rows cost O(N) gates each.

## Attempted Derivation

- Fix Psys_h=EF+EqSAT+SR_h and the beta-zero carrier H_N^{SAT}.
- Recheck the target bridge: substituting any SIZE(L^c) SAT circuit into all generated queries gives C(H_N^{SAT})<=N^{max{rho,q}+o(1)}, so q,rho<1+epsilon is the target-preserving exponent condition.
- Expose the SR semantic escape by allowing h rounds of SAT self-reduction before labels are evaluated.
- Given a leaf solver A_N of size N^{tau+o(1)}, compute each top query by enumerating 2^{bh}=N^{eta_N+o(1)} leaves, OR their A_N labels, and XOR over M_N=N^{q+o(1)} queries.
- This yields C(H_{A,h})<=N^{rho+o(1)}+N^{q+eta_N+tau+o(1)}.
- If H_{A,h} differs from H_N^{SAT} on E_N rows, add equality patches for those rows and get C(H_N^{SAT})<=N^{max{rho,q+eta_N+tau,1+e}+o(1)}.
- Therefore any claimed N^{1+epsilon-o(1)} source lower bound must rule out all bounded-SR easy carriers with q+eta_N+tau<1+epsilon and e<epsilon.
- Attempted extension to full EF+SAT semantics: EqSAT quotienting is parsed by identifying label variables, and explicit SR rules add OR hyperedges.
- The extension fails for arbitrary EF extension variables because they may encode global SAT-semantic predicates not representable as bounded SR leaf evaluations or occurrence-row queries.

Blocking gap: ParserNormalForm(EF+EqSAT+SR_h): prove that every short proof of LB(H_N^{SAT}) either gives a dense functional label property, an occurrence/full-row transcript, or a bounded-SR residual code with advice-free size bound poly(|pi|,L_N).

## Falsifiers

- bounded-SR leaf solver falsifier: q+eta+tau<1+epsilon and row error exponent e<epsilon gives a subthreshold patched circuit for H_N^{SAT}.
- sparse-row residual falsifier: any D_N agreeing with H_N^{SAT} off fewer than N^{epsilon-o(1)} rows and having subthreshold size invalidates the source lower-bound certificate.
- functional-density falsifier: if accepted certificates are dense and truth-table constructive over quotient labels, they become natural-property evidence rather than a non-natural lower-bound proof.
- parser-advice falsifier: a proof parser depending nonuniformly on the SAT label vector can fake extraction and is not valid for the route.
- full-EF semantic-escape falsifier: extension variables for global SAT-semantic predicates may defeat the bounded-SR parser, forcing demotion to the restricted Psys_h theorem.
- positive-beta transfer falsifier remains quarantined: any interface with target query length N^beta, beta>0, has exponent q+beta c and cannot give all-exponent SAT lower bounds.

## Learning

Cycle 90 converts the SR semantic escape into a costed leaf-solver falsifier: bounded self-reduction depth is not free, but if q+eta+tau<1+epsilon and the induced row error is below N^epsilon then the source lower bound collapses by equality patching. The live inference-quality packet is now theorem-shaped for Psys_h; the only remaining full-system gap is the advice-free parser normal form for arbitrary EF extension variables.

## Gedanken Experiment Design Seed

- Need decision: `design_concrete_now`
- Rationale: The branch is blocked at the formula-semantic extraction fork; varying SR depth tests whether the named SAT-semantic escape still leaks a subthreshold source circuit before another abstract parser restatement is useful.
- Situation seed: Take a fixed beta-zero generator with M_N=N^q, L_N=(log N)^d, and an EF+EqSAT+SR_h certificate whose SR clauses expand each generated SAT formula for h rounds before a leaf predicate A_N supplies labels.
- Varied variable: eta=bh/log N, the SR leaf-expansion exponent contributed by h self-reduction rounds.
- Held-fixed controls: q,rho<1+epsilon for the beta-zero target-preserving bridge., L_N=(log N)^d with d>1 so direct SAT substitution remains N^{o(1)} per query., The parser is uniform and advice-free, and equality patches cost O(N) gates per bad source row., The target statement remains SAT notin P/poly only conditionally on a valid H_N lower bound; no main P != NP claim is inferred from the experiment.
- Expected observation: For eta below 1+epsilon-q-tau, even a weak leaf predicate A_N with row error below N^epsilon gives a concrete upper-bound falsifier. Once eta crosses that threshold, SR expansion is too expensive to be a subthreshold leakage, so the parser must prove residual robustness rather than rely on occurrence spoofing.
- Transfer certificate needed: A formal parser-normal-form certificate mapping the chosen proof pi to the bounded SR DAG and a row-error transfer lemma showing that leaf-label mistakes induce at most E_N bad source rows without hidden advice.

## Next Experiment

Build the minimal EF+EqSAT+SR_1 parser countermodel: allow one extension variable Z(F)=SAT(F_0) OR SAT(F_1) and test whether it is representable by the SR DAG without advice; if yes, increase to two nested extensions, if no, use it as the semantic escape separating full EF from Psys_h.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Conditional dichotomy: for EF+SAT_U^subst proofs of LB_N for beta-zero H_N^SAT, a valid ExtensionRowRealizer gives either |K_pi|>=N^{epsilon-o(1)} or a sparse-residual falsifier; failure of both extractions isolates a genuinely SAT-semantic nonrelativizing principle.

## Definitions

- source object: EF+SAT_U^subst proof pi of LB_N: Ckt(H_N^SAT)>N^{1+epsilon-o(1)} for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)).
- target object: fork-resolving extraction/no-go theorem: functional naturalization, occurrence/semantic row-forcing, or named SAT-semantic escape.
- controlled interface: ExtensionRowRealizer maps pi to semantic support K_pi plus advice-free D_N agreeing with H_N^SAT off K_pi.
- target-preserving condition: N=2^n, M_N<=N^{q+o(1)}, L_N=(log N)^d, G uniform size N^{rho+o(1)}, beta=0, no row advice, same truth-table length.
- semantic support K_pi is closed under EF substitution, SAT_U equality, and SAT-composition atoms that determine generator-row SAT values.

## Assumptions

- Source statement: LB_N is a nonuniform Boolean circuit lower bound; target statement is the dichotomy large K_pi, functional naturalization, or sparse-residual falsifier for the same H_N.
- Model context: Psys=EF+SAT_U^subst; extension variables may feed SAT_U atoms; the reduction type is proof-to-circuit residual patching, not Cook-Levin transfer.
- Quantifier context: for all large N=2^n, fixed epsilon>0, proof length poly(N), fixed q,rho,d, and no advice or secret row list in the extraction.
- Barrier context: functional truth-table extraction with O(log N) projection is natural; semantic-support extraction is valid only when SAT facts are preserved in the same theory.
- Cutoff: the off-support realizer must satisfy S(D_N)<=N^{1+o(1)}; otherwise patching cannot contradict the claimed N^{1+epsilon-o(1)} lower bound.

## Equations

- beta_zero_carrier: `\(H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j))\)`. Valid when: Valid when the beta-zero XOR carrier and generator length regime are fixed before proof extraction.
- semantic_residual_patch: `\(Ckt(H_N^{SAT})\le S(D_N)+O(|K_\pi|N)\)`. Valid when: Applies after an advice-free realizer D_N agrees with H_N outside the semantic support K_pi.
- forced_semantic_charge: `\(Ckt(H_N^{SAT})>N^{1+\epsilon-o(1)}\wedge S(D_N)\le N^{1+o(1)}\Rightarrow |K_\pi|\ge N^{\epsilon-o(1)}\)`. Valid when: Requires the claimed source lower bound and the residual patching bound in the same length regime.

## Attempted Derivation

- Fix pi and close its SAT_U atoms under extension substitution, equality, and composition to obtain semantic row support K_pi.
- Assume ExtensionRowRealizer_subst: from pi and K_pi compute an advice-free D_N of size N^{1+o(1)} agreeing with H_N^SAT on all rows not in K_pi.
- Patch the remaining K_pi rows by truth-table DNF over x, costing O(|K_pi|N), and compare with LB_N.
- If |K_pi|<N^{epsilon-o(1)}, pi contradicts the source lower bound; otherwise the proof pays semantic row charge or must be classified as functional/natural or SAT-semantic.

Blocking gap: ExtensionRowRealizer_subst is unproved for arbitrary EF SAT_U atoms; SAT-composition can hide global row dependence inside one extension formula.

## Falsifiers

- Substitution-compressed atom SAT(F_ext(x)) encodes xor of all M rows; occurrence support is one but semantic support is M, a falsifier to occurrence parsing.
- SAT-composition axiom equates global formula constructors without row-wise evidence; it falsifies local consistency as a source of DirectClusterSound.
- Sparse spoof table with semantic closure |K|<N^epsilon and D size N^{1+o(1)} is a residual falsifier for the alleged source lower bound.
- Functional extraction with O(log N) projection naturalizes; PRF tension is a falsifier unless the property is nonlarge, nonconstructive, or proof-specific.

## Learning

Live inference-quality packet content is now explicit: source LB_N proof in EF+SAT_U^subst, target semantic-support dichotomy, beta-zero length regime, no-advice extraction, naturalness trigger, and named blocking lemma. This is valid route-level progress only.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a concrete test of whether substitution compresses row support or merely changes its representation; another barrier restatement would not decide the parser fork.
- Situation seed: EF+SAT_U^subst proof containing one extension atom SAT(F_theta(x)) where F_theta composes the first N^theta generator rows and the remaining rows are replaced by a spoof table.
- Varied variable: semantic support exponent theta in |K_pi|=N^theta, with theta swept across epsilon.
- Held-fixed controls: beta=0 XOR carrier H_N^SAT with M_N<=N^{q+o(1)} and L_N=(log N)^d, uniform generator size N^{rho+o(1)} and no row advice, target lower-bound threshold Ckt(H_N)>N^{1+epsilon-o(1)}, same EF+SAT_U^subst syntax and SAT-composition rules
- Expected observation: If theta<epsilon and a realizer exists, residual patching gives Ckt(H_N)<=N^{1+o(1)}+N^{1+theta}, contradicting LB_N; if no realizer exists, the obstruction pinpoints the semantic escape.
- Transfer certificate needed: A formal ExtensionRowRealizer proving advice-free D_N construction from pi and K_pi, or a minimal EF+SAT_U^subst countermodel showing why SAT-composition is nonrealizable.

## Next Experiment

Instantiate F_theta using a SAT-composition axiom, compute its semantic support closure, and test whether an advice-free D_N can be built for theta<epsilon without smuggling row advice.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Witnessed-extensional beta-zero parser theorem, restricted form: For the proof system P_wExt=EF plus local SAT_U occurrence axioms plus witnessed formula-extensionality rules, any accepted low-cover row-parity certificate for H_N^SAT yields an unrestricted circuit upper bound C(H_N^SAT)<=N^{max{rho,q+alpha_ext,max(f,r)+1}+o(1)}. Hence such a carrier is a valid falsifier for any route claiming C(H_N^SAT)>N^{1+epsilon-o(1)} when max{rho,q+alpha_ext,max(f,r)+1}<1+epsilon.

## Definitions

- source object: A P_wExt proof pi or certificate transcript for the beta-zero SAT-parity family H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with explicit row-parity binding claims.
- target object: A same-length unrestricted Boolean circuit for H_N^SAT, used only to refute an overstrong carrier lower-bound claim and not as a proof of P != NP.
- controlled interface: The parser extracts an occurrence transcript Q_pi, a witnessed equality quotient E_pi, a forced-row set F_N, and a residual set R_N; E_pi is charged by adaptive-cover exponent alpha_ext.
- target-preserving condition: The extraction is uniform and advice-free, keeps the original generator G_N, query count M_N, and row length N, and charges every formula-identity step to an explicit quotient witness rather than an unwitnessed semantic oracle.
- P_wExt rule: an extensionality step may identify formula occurrences only when a polynomially checkable quotient/congruence witness is included in pi.
- ForcedRows(pi): rows whose parity is syntactically constant over all local completions compatible with Q_pi/E_pi.
- ResidualRows R_N: rows not covered by the binding argument and patched individually in the final circuit.

## Assumptions

- Source model: P_wExt is a Cook-Reckhow style proof/certificate model; every accepted proof is polynomial-time checkable from the proof string and the public generator description, with no advice and no hard-row selector.
- Length regime: M_N<=N^{q+o(1)}, each SAT instance G_N(x,j) has polylogarithmic length, and G_N is computable by circuits of size N^{rho+o(1)}.
- Cover regime: the extracted quotient/transcript has alpha_ext=max{tau,max_l(a_l+mu_l),max_l omega_l}+o(1), so all queried labels are simulated by N^{alpha_ext+o(1)}-size openings per SAT-query family.
- Binding regime: outside F_N union R_N, the row parity computed from the transcript equals H_N^SAT(x); |F_N|<=N^{f+o(1)} and |R_N|<=N^{r+o(1)}.
- Circuit model: the target upper bound is nonuniform unrestricted Boolean circuits over the N-row truth table domain; hardwiring exceptional rows costs O(N) gates per row.
- Uniformity/advice status: pi, Q_pi, E_pi, F_N, and R_N are obtained by an advice-free parser from the public proof/certificate, although the final contradiction circuit itself is nonuniform.
- Non-claim boundary: this proves a scoped upper-bound falsifier for low-cover carriers only; it does not prove P != NP or a lower bound for H_N^SAT.

## Equations

- beta_zero_sat_parity: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\qquad M_N\le N^{q+o(1)}`. Valid when: Valid when the source object is the beta-zero SAT-parity carrier with public generator G_N and polylogarithmic SAT-query length.
- adaptive_extensional_cover: `\alpha_{ext}=\max\{\tau,\max_\ell(a_\ell+\mu_\ell),\max_\ell\omega_\ell\}`. Valid when: Valid when every witnessed formula-identity step is parsed into an adaptive quotient cover with declared summary, addressing, and opener exponents.
- label_simulation_cost: `C_{labels}(N)\le N^{q+\alpha_{ext}+o(1)}`. Valid when: Applies after the reduction preserves the M_N query count and each SAT label needed by a query is opened through the same low-cover quotient interface.
- patch_upper_bound: `C(H_N^{SAT})\le N^{\max\{\rho,q+\alpha_{ext},\max(f,r)+1\}+o(1)}`. Valid when: Requires generator overhead rho, row-parity binding off F_N union R_N, and nonuniform patching of all exceptional rows at O(N) gates per row.
- carrier_falsification_threshold: `\max\{\rho,q+\alpha_{ext},\max(f,r)+1\}<1+\epsilon\ \Rightarrow\ \neg[C(H_N^{SAT})>N^{1+\epsilon-o(1)}]`. Valid when: Valid when the claimed source lower bound is an unrestricted circuit lower bound for the identical H_N^SAT family and no parameter is changed by padding or advice.

## Attempted Derivation

- Fix P_wExt syntax: EF extension rules, local SAT_U occurrence axioms, local parity rules, and witnessed extensionality rules carrying quotient/congruence witnesses.
- Define the induction invariant I(t): after t proof lines, every label used by the derived row-parity assertion is represented by an occurrence transcript plus equality quotient with cumulative adaptive-cover exponent at most alpha_t.
- Check base rules: generator lines cost N^{rho+o(1)}; local SAT occurrence labels are opened through the transcript at total cost N^{q+alpha_t+o(1)}.
- Check EF extension rules: definitional variables are added as local gates and do not create new semantic formula identity; they only increase the local opener by N^{o(1)} under the declared cover.
- Check witnessed extensionality: the supplied quotient witness contracts formula occurrences; its summaries/openers are charged to alpha_ext, so the induction invariant survives exactly when the witness is checkable and advice-free.
- Define ForcedRows as rows whose parity is invariant over all completions respecting Q_pi/E_pi; nonforced or unbound rows are placed in F_N, and semantic mismatches are placed in R_N.
- Construct D_N by computing G_N, opening all M_N labels through Q_pi/E_pi, xoring the labels, and patching rows in F_N union R_N by hardwired truth-table bits.
- Add sizes: generator overhead N^{rho+o(1)}, label simulation N^{q+alpha_ext+o(1)}, and patches O((|F_N|+|R_N|)N), yielding the stated upper bound.
- Compare the upper bound with the claimed lower-bound threshold N^{1+epsilon-o(1)}; if the maximum exponent is below 1+epsilon, the carrier claim is refuted.

Blocking gap: Named blocked lemma WExtTranscriptInduction(P_wExt): the rule-by-rule proof must be written for the exact proof-system grammar used in the draft, especially parity binding, extension-variable congruence, and quotient-witness verification.

## Falsifiers

- falsifier: a proof line uses unwitnessed SAT-extensionality, so no occurrence quotient or adaptive-cover witness is available to the parser.
- falsifier: alpha_ext is at least 1+epsilon-q, making the label-simulation bound too weak to contradict the claimed source lower bound.
- falsifier: the forced-row or residual exponent satisfies max(f,r)+1>=1+epsilon, so row patching consumes the entire lower-bound margin.
- falsifier: the certificate has only local proof soundness but not row-parity binding for H_N^SAT outside the residual set.
- falsifier: the selected hard row or quotient witness is supplied by advice or a nonuniform selector rather than by an advice-free parser.
- falsifier: the carrier changes the target family by padding, changing M_N, or replacing unrestricted circuits with a weaker circuit model.

## Learning

Cycle 90 adds a live inference-quality packet and a sharper proof-system boundary: witnessed formula identity is harmless only because it is parsed into alpha_ext and paid in the circuit upper bound, while unwitnessed SAT-extensionality is a semantic-oracle model change unless repaired by an advice-free quotient witness. The contribution remains a route-specific falsifier for low-cover MCSP/MKtP or proof-certificate carriers, not progress on P != NP itself.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the witnessed-extensionality threshold.`
- Rationale: The branch needs a concrete target-preserving stress test because the abstract fork has already been stated; the live issue is whether quotient witnesses are charged quantitatively or smuggled as semantic advice.
- Situation seed: A padded beta-zero SAT-query family where G_N emits pairs of polylogarithmic SAT instances that are syntactically different Tseitin encodings of the same small constraint system, and the proof certificate either supplies a low-cover renaming quotient or invokes unwitnessed SAT-extensionality.
- Varied variable: alpha_ext, the adaptive-cover exponent of the supplied formula-identity quotient witness, varied from o(1) up to 1+epsilon-q.
- Held-fixed controls: M_N=N^{q+o(1)} and generator size N^{rho+o(1)} are fixed., The target remains the identical H_N^SAT truth-table family and unrestricted circuit model., The checker is required to be Cook-Reckhow and advice-free unless the semantic-oracle escape is explicitly declared., Residual and forced-row exponents r and f are held below epsilon in the test instance.
- Expected observation: When alpha_ext<1+epsilon-q and rho,max(f,r)+1<1+epsilon, the quotient witness produces a valid patch circuit and falsifies the carrier lower bound; when the witness is omitted, the only surviving explanation is an unwitnessed semantic-oracle rule.
- Transfer certificate needed: A formal parser certificate mapping every formula-identity proof step to a checkable quotient cover and proving row-parity binding off F_N union R_N before the thought experiment may affect proof obligations.

## Next Experiment

Write the WExtTranscriptInduction proof for a concrete grammar EF+SAT_U^{wExt}: enumerate rule cases, define quotient-witness checker, prove ForcedRows parity constancy, and compute alpha_ext on one Tseitin-renaming certificate instance.
