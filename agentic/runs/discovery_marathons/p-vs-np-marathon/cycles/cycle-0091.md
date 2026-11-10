# cycle-0091

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: beta-zero XOR formula-semantic parser audit

## Candidate Lemma

For the beta-zero XOR SAT carrier, a Psys_{h,Ext} certificate whose EF extension definitions, EqSAT links, and bounded self-reduction leaves admit an advice-free charged residual transcript yields a concrete upper-bound falsifier unless it forces at least N^{epsilon-o(1)} residual rows or pays a superthreshold extension-support cost. This is a route-level parser/falsifier theorem, not a proof of P != NP.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), where M_N<=N^{q+o(1)}, each G_N(x,j) has length L_N=(log N)^d, and G_N has circuit size N^{rho+o(1)}.
- target object: the source lower-bound claim Ckt(H_N^SAT)>N^{1+epsilon-o(1)} used by the beta-zero bridge to exclude SAT in P/poly if q,rho<1+epsilon.
- controlled interface: a short Psys_{h,Ext} proof pi is parsed into a charged transcript (A_pi,Q_pi,R_pi,ExtSupp_pi) consisting of bounded-depth SR leaf queries, EqSAT links, residual bad rows, and all EF extension dependencies on SAT atoms.
- target-preserving condition: L_N is polylogarithmic, beta=0, q,rho<1+epsilon, the parser is advice-free, and every nonuniform row table or extension definition is charged in S_ext or in the bad-row set.

## Assumptions

- Circuit model is nonuniform Boolean circuits for Ckt(H_N^SAT); the target class is P/poly and the reduction is batched substitution plus residual patching.
- Proof system Psys_{h,Ext} is EF augmented with EqSAT identities and self-reduction axioms to fixed depth h; extension variables are permitted only through syntactic definitions whose SAT-atom support is counted.
- The transcript has leaf-blowup exponent eta, leaf-solver exponent tau, extension-support size S_ext=N^{gamma+o(1)}, and residual bad rows E_N=|R_pi|.
- Uniformity/advice condition: the parser from pi to transcript is uniform or advice-free; any row-indexed advice is counted as extension support.
- Non-claim boundary: the lemma only refutes subthreshold proof-mediated certificates for this route; it does not prove the source lower bound or P != NP.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N\le N^{q+o(1)},\quad L_N=(\log N)^d.`. Valid when: Valid when G_N is an explicit batched generator whose outputs are SAT instances of length L_N and whose source input has length N.
- beta_zero_transfer: `SAT\in SIZE(n^c)\Rightarrow C(H_N^{SAT})\le N^{\rho+o(1)}+M_NL_N^c=N^{\max\{\rho,q\}+o(1)}.`. Valid when: Applies when SAT on L_N-bit formulas has nonuniform circuits of size L_N^c and L_N is polylogarithmic, so the target-query exponent beta is zero.
- charged_SR_residual_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+S_{ext}(\pi)+N^{q+\eta+\tau+o(1)}+O(E_NN).`. Valid when: Valid when the charged parser extracts a bounded self-reduction leaf solver of exponent tau, leaf blowup eta, extension support S_ext, and E_N bad source rows.
- subthreshold_collapse: `S_{ext}\le N^{\gamma+o(1)},\ E_N\le N^{\delta+o(1)},\ \max\{\rho,\gamma,q+\eta+\tau,1+\delta\}<1+\epsilon\Rightarrow C(H_N^{SAT})<N^{1+\epsilon-o(1)}.`. Valid when: Requires all transcript costs to be counted in the same nonuniform circuit model and equality patches to cover exactly the residual rows.

## Attempted Derivation

- Fix H_N^SAT with M_N=N^{q+o(1)}, L_N=(log N)^d, d>1, and generator size N^{rho+o(1)}; this keeps the target substitution beta at zero.
- Assume SAT has L^c-size circuits. Substitute the SAT circuit into every generated formula and obtain C(H_N^SAT)<=N^{max{rho,q}+o(1)}, so q,rho<1+epsilon is the valid target-preserving window.
- Choose Psys_{h,Ext}=EF+EqSAT+depth-h self-reduction. Parse pi by collecting visible SAT atoms, EqSAT quotient links, SR leaves, and all SAT-atom dependencies of extension definitions.
- If the parsed transcript supplies a leaf solver of exponent tau after leaf blowup eta and is wrong on E_N rows, build D_N by running G_N, evaluating the charged transcript, and xoring the row outputs.
- Patch the residual rows R_pi using equality tests for the N-bit source row; the patch cost is O(E_N N).
- Derive C(H_N^SAT)<=N^{rho+o(1)}+S_ext+N^{q+eta+tau+o(1)}+O(E_NN). If all exponents are below 1+epsilon, the claimed source lower bound is falsified.
- Test parser robustness by defining an EF extension y_r=xor_j z_{r,j}. A parser that ignores extension definitions sees one atom and no complete row, but expansion touches the full parity row; therefore extension-blind occurrence extraction is invalid.
- Conclusion: the restricted charged-extension theorem is valid, while the full EF+SAT claim is blocked exactly at the advice-free extension-support normal-form lemma.

Blocking gap: Prove or refute the advice-free extension-support normal form for arbitrary EF extension variables in EF+EqSAT+bounded-SR; the known derivation only handles proofs whose extension dependencies are syntactically charged.

## Falsifiers

- Subthreshold charged transcript falsifier: S_ext+N^{q+eta+tau}+E_NN<N^{1+epsilon-o(1)} gives an explicit circuit for H_N^SAT.
- Extension-blind parser falsifier: y_r=xor_j z_{r,j} hides a full row behind one EF atom unless definitions are expanded or charged.
- Nonuniform leakage falsifier: a row-indexed advice table inside extension definitions invalidates any claimed advice-free parser.
- Bounded-SR leaf-solver falsifier: if q+eta+tau<1+epsilon and residual errors are below N^{epsilon-o(1)}, equality patching collapses the source lower bound.
- Positive-beta falsifier remains quarantined: any return to polynomial-length SAT queries reintroduces the q+beta c transfer cap.

## Learning

Cycle 91 upgrades the bounded-SR leaf-solver audit by adding an explicit EF extension-support charge and proving a no-go for extension-blind parsers. The valid theorem is restricted but contribution-shaped: subthreshold charged transcripts are upper-bound falsifiers, while arbitrary EF+SAT remains blocked at a precise advice-free normal-form lemma.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The top proof-delivery item needs a concrete strong-proof-system obstruction, and arbitrary EF extension variables are the current named gap rather than another abstract barrier slogan.
- Situation seed: A beta-zero carrier H_N^SAT with M_N=N^q polylog SAT queries is certified in Psys_{h,Ext}; the proof uses depth-h self-reduction leaves and one EF extension variable per row block that may summarize many SAT labels.
- Varied variable: gamma, the extension-support exponent S_ext=N^{gamma+o(1)}, while h is fixed and the leaf-solver exponent tau is measured separately.
- Held-fixed controls: q,rho<1+epsilon so the beta-zero target bridge remains valid., L_N=(log N)^d with d>1, so exhaustive truth-table lookup is not a subthreshold source falsifier., The parser must be advice-free; any row table is charged as extension support., Residual row patching costs O(E_NN) in the same nonuniform circuit model.
- Expected observation: When max{rho,gamma,q+eta+tau,1+delta}<1+epsilon, the thought experiment produces a small circuit and falsifies the certificate; when gamma or forced residual rows exceed the threshold, the proof has paid the full-row barrier cost.
- Transfer certificate needed: An extension-support normal-form theorem mapping Psys_{h,Ext} proofs to charged EqSAT/SR residual transcripts without hidden advice; without it the intuition cannot be promoted beyond the restricted parser theorem.

## Next Experiment

Instantiate Psys_{h,Ext}^{schema}: EF+EqSAT+depth-h SR with extension definitions generated by row-oblivious schemas. Try to prove ExtSupp(NF(pi))<=poly(|pi|), or construct a minimal nonrelativizing SAT-semantic extension that defeats this normal form.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

In EF+SAT_U^subst, a parser theorem bounding row queries by syntactic SAT-atom occurrences is false. One indexed SAT atom A_x=SAT(Phi_x(u,w)) can have semantic row support M_N while preserving beta-zero length. Thus the full-system extraction must count semantic support K_pi or forbid index substitution; occurrence-local proof packets do not lift automatically.

## Definitions

- source object: short EF+SAT_U^subst proof pi of LB_N: Ckt(H_N^SAT)>N^{1+epsilon-o(1)}, where H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)).
- target object: parser-to-query extraction pi -> Q_pi for the formula-semantic fork, intended to classify pi as occurrence-relativizing, functional-naturalizing, or genuinely SAT-semantic.
- controlled interface: SAT atoms may contain extension substitutions and row-index variables; the audited observable is semantic row support K(A), not syntactic occurrence count.
- target-preserving condition: beta-zero regime M_N<=N^{q+o(1)}, row length L_N=(log N)^d, generator size N^{rho+o(1)}, uniform and advice-free extraction, with q,rho below the source lower-bound margin.
- semantic support K(A): the set of generator rows j whose SAT value can affect the truth of the SAT atom A under row-realizing completions.
- occurrence parser: a map that records only displayed SAT(G_N(x,j)) occurrences or bounded projections of them.

## Assumptions

- Proof model: EF+SAT_U^subst is EF plus sound universal SAT facts closed under substitution into formula variables and extension-defined circuits.
- Substitution regime: the atom A_x=SAT(Phi_x) is allowed without expansion over all row indices u in [M_N].
- Falsifier regime: the padded selector generator is row-realizing, so each j can be toggled while other visible rows are fixed; this is a finite parser countermodel, not a claim about P != NP.
- Uniformity/advice regime: the parser and any extracted property are uniform in N and cannot use nonuniform advice to hide the missing rows.

## Equations

- beta_zero_carrier: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j))`. Valid when: Valid when N indexes the beta-zero carrier and G_N is the fixed uniform SAT-query generator for the source statement.
- indexed_substitution_atom: `\Phi_x(u,w)=G_N(x,u)(w),\quad A_x=SAT(\Phi_x)`. Valid when: Valid when the proof system permits SAT atoms over formulas with row-index variables introduced by extension substitution.
- syntactic_semantic_gap: `occ_{SAT}(A_x)=1,\quad |K(A_x)|=M_N`. Valid when: Valid when the padded selector generator is row-realizing so each indexed row can change the atom semantics.
- beta_zero_length_preservation: `|\Phi_x|\le L_N+O(\log M_N)+N^{o(1)}=(\log N)^{O(1)}`. Valid when: Valid when M_N<=N^{q+o(1)} and every generated SAT instance has polylogarithmic encoded length.

## Attempted Derivation

- Fix the source statement LB_N: Ckt(H_N^SAT)>N^{1+epsilon-o(1)} for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) in the beta-zero regime M_N<=N^{q+o(1)}, L_N=(log N)^d, generator overhead N^{rho+o(1)}, q,rho<1+epsilon.
- Fix the proof/certificate model EF+SAT_U^subst: EF reasoning plus SAT facts closed under extension substitution into formula arguments. This is stronger than occurrence-local EF+SAT_U^{occ}.
- Try the occurrence parser pi -> Q_pi: record each displayed SAT(G_N(x,j)) row and use sparse patching to force |Q_pi|>=N^{epsilon-o(1)}.
- Construct the indexed atom A_x=SAT(Phi_x(u,w)) with Phi_x(u,w)=G_N(x,u)(w). It has one SAT occurrence and polylogarithmic length but semantic support M_N in a row-realizing selector family.
- Therefore syntactic occurrence width is not a valid invariant in EF+SAT_U^subst. The attempted parser proves only the occurrence-local theorem and fails for the full formula-semantic system.
- Repair attempt: replace Q_pi by semantic support K_pi and require ExtensionRowRealizer(pi), namely proof-visible SAT facts are invariant under all replacements agreeing with H_N^SAT off K_pi.
- With ExtensionRowRealizer, sparse residual patching gives Ckt(H_N^SAT)<=S_D+c|K_pi|N and hence the forced charge |K_pi|>=N^{epsilon-o(1)} when S_D<=N^{1+o(1)}.
- Live inference-quality handoff: source_statement=short EF+SAT_U^subst proof of LB_N; target_statement=classification into functional-naturalizing, semantic-support forced-row, or named SAT-semantic escape; reduction type=proof-to-property or proof-to-support extraction; advice status=none; barrier trigger=functional extraction naturalizes, syntactic extraction is refuted by indexed substitution.

Blocking gap: ExtensionRowRealizer_N for the actual H_N^SAT carrier in EF+SAT_U^subst: prove that every short accepted proof has a finite semantic support K_pi controlling all substituted SAT facts, or isolate the indispensable SAT-semantic inference that makes such support impossible.

## Falsifiers

- Indexed existential SAT atom A_x=SAT(exists u,w G_N(x,u,w)) keeps projection width one while semantically touching M_N rows; this falsifier invalidates syntactic occurrence parsers in EF+SAT_U^subst.
- Sparse-residual spoof D_N agreeing with H_N^SAT off K and having size N^{1+o(1)} falsifies any certificate claiming Ckt(H_N^SAT)>N^{1+epsilon-o(1)} when |K|=o(N^epsilon).
- Functional accepted-proof predicate with logarithmic projection, polynomial density, and poly(N) constructivity becomes a valid natural property and faces PRF pressure for the same SIZE target.
- Nonuniform row advice selecting K_pi without derivation is a leakage falsifier: it destroys the target-preserving proof-to-support bridge.

## Learning

Cycle 91 makes one new route-level move: the full EF+SAT_U^subst parser cannot be occurrence-based because indexed SAT substitution is a concrete falsifier separating one displayed atom from M_N semantic rows. The valid invariant is semantic support K_pi. The live pvsnp_inference_quality packet is: source_statement=short proof of LB_N for H_N^SAT; target_statement=functional naturalization, semantic forced-row theorem, or named SAT-semantic escape; model_context=nonuniform Boolean circuits plus EF+SAT_U^subst proofs; quantifier_context=beta-zero lengths, q,rho<1+epsilon, uniform no-advice extraction; derivation_status=blocked exactly at ExtensionRowRealizer_N; reviewer finding=syntactic occurrence lift quarantined, semantic-support dichotomy conditionally valid. This is not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the full EF+SAT_U^subst parser theorem.`
- Rationale: The branch is blocked at a concrete extraction lemma, not at a general barrier slogan. A target-preserving thought experiment tests whether syntactic projection width can certify row support after substitution.
- Situation seed: Padded selector SAT-query family with G_N(x,j) independently togglable by a padding bit, and a single allowed proof atom A_x=SAT(Phi_x(u,w)) where Phi_x(u,w)=G_N(x,u)(w).
- Varied variable: semantic row support t=|K(A_x)|, varied from log N through N^q while keeping one displayed SAT atom.
- Held-fixed controls: beta-zero row length L_N=(log N)^d, one syntactic SAT atom and logarithmic projection width, uniform generator overhead N^{rho+o(1)}, no nonuniform advice in the parser, same target circuit threshold N^{1+epsilon-o(1)}
- Expected observation: Syntactic projection stays O(log N) while semantic support grows to t. Once t<N^epsilon, residual patching can spoof the certificate; once t>=N^epsilon, the forced-row cost reappears.
- Transfer certificate needed: A formal ExtensionRowRealizer or a syntactic ban on indexed SAT substitution, plus a proof that the actual H_N^SAT generator has the row-realizing dependence needed before the intuition affects proof obligations.

## Next Experiment

Instantiate EF+SAT_U^subst with a concrete SAT-composition/substitution axiom list and test whether the indexed atom A_x=SAT(Phi_x(u,w)) is derivable as one line; if yes, formalize the no-go proposition, and if no, record the syntactic restriction that may resurrect occurrence parsing.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For the concrete system P_wExt = EF over Boolean formulas with SAT_U atoms plus only witnessed formula-extensionality rules, every short accepted proof pi for a beta-zero SAT-parity lower-bound certificate induces a quotient occurrence transcript Q_pi. If Q_pi has adaptive extensionality cover exponent alpha_ext, forced-row exponent f, residual exponent r, SAT-query exponent q, and generator exponent rho, then the certificate route gives the nonuniform upper bound C(H_N^SAT) <= N^{max{rho,q+alpha_ext,max{f,r}+1}+o(1)}. Hence any claimed proof-certificate lower bound above this cap is a finite falsifier for the low-cover P_wExt carrier, unless the proof uses unwitnessed SAT-extensionality or high-cover/high-residual behavior.

## Definitions

- source object: a P_wExt proof pi of a lower-bound or MCSP/MKtP certificate statement about H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), where G_N outputs polylogarithmic SAT instances and pi has advice-free parseable witnesses.
- target object: a nonuniform Boolean circuit upper bound for the N-bit truth table H_N^SAT, used only to refute an overstrong carrier lower-bound claim and not to prove P != NP.
- controlled interface: parse pi into a quotient occurrence transcript Q_pi, charge each witnessed formula-identity or extension-congruence step to an adaptive cover exponent alpha_ext, and then patch forced or residual rows explicitly.
- target-preserving condition: the parser, quotient witnesses, row labels, and residual set are generated without advice in the same length regime, while the final conclusion is an unrestricted nonuniform circuit-size upper bound against the same H_N^SAT family.
- P_wExt syntax: EF lines are Boolean formulas/circuits with extension variables and SAT_U(F) atoms; the only formula-identity rule is WExt(F,F',w), where w is a checkable quotient or definitional-equivalence witness implying SAT(F)=SAT(F').
- Quotient transcript Q_pi: the occurrence graph of all SAT_U formulas appearing in pi after contracting syntactic equality, extension-variable congruence, and WExt edges whose witnesses are explicitly parsed.
- Adaptive extensionality cover exponent alpha_ext: the least alpha such that the quotient graph and all label openers used by pi admit an adaptive cover of size N^{alpha+o(1)} per SAT-query block.
- ForcedRows(Q_pi): rows x for which the parity xor_j SAT(G_N(x,j)) is fixed over all SAT-label completions satisfying the local quotient constraints encoded by Q_pi.

## Assumptions

- Circuit model is unrestricted nonuniform Boolean circuits of fan-in two, size measured as gates, with constants absorbed into N^{o(1)}.
- Length regime has N truth-table rows, M_N=N^{q+o(1)} SAT queries per row, query length L_N=(log N)^d, and uniform generator circuit size N^{rho+o(1)}.
- All WExt witnesses are part of pi or generated by a uniform proof parser; no nonuniform formula-equivalence advice or hard-row selector is allowed.
- The row-parity binding claim used by the carrier is interpreted over Q_pi completions; local proof soundness alone is not assumed to imply binding.
- The number of forced rows is at most N^{f+o(1)} and the remaining disagreement residual is at most N^{r+o(1)} in the same N-row universe.
- The proof system excludes unwitnessed SAT-extensionality uExt; if uExt appears, it is treated as a semantic-oracle rule unless replaced by an advice-free quotient witness.
- The result is a route-level upper-bound falsifier for low-cover certificates; it is not a proof of P != NP or an unconditional lower bound for H_N^SAT.

## Equations

- beta_zero_sat_parity_carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N|=N^{\rho+o(1)}`. Valid when: Valid when the source object is the beta-zero SAT-parity carrier with polylogarithmic generated SAT instances and a uniform generator size ledger.
- adaptive_extensionality_cover: `\alpha_{ext}=\max\{\tau,\max_\ell(a_\ell+\mu_\ell),\max_\ell\omega_\ell\}`. Valid when: Valid when every witnessed formula-identity edge is parsed into adaptive blocks with transcript cost tau, summary costs a_l plus mu_l, and opener costs omega_l.
- low_cover_upper_bound: `C(H_N^{SAT})\le N^{\max\{\rho,q+\alpha_{ext},\max\{f,r\}+1\}+o(1)}`. Valid when: Applies after the WExt quotient transcript preserves SAT labels, forced rows have exponent f, residual rows have exponent r, and the final target is unrestricted nonuniform circuits.
- carrier_falsifier_threshold: `\theta>\max\{\rho,q+\alpha_{ext},\max\{f,r\}+1\}\;\Longrightarrow\; \text{a claimed }C(H_N^{SAT})>N^{\theta-o(1)}\text{ from this carrier is invalid}`. Valid when: Requires the claimed lower-bound certificate to target the same H_N family and to use only low-cover witnessed extensionality without hidden advice or semantic-oracle rules.

## Attempted Derivation

- Fix P_wExt: EF propositional reasoning, extension variables, SAT_U atoms for formulas of length polylog(N), and WExt(F,F',w) rules whose witnesses are checkable by the proof parser.
- Build the occurrence graph of all SAT_U formulas in pi. Add edges for syntactic identity, definitional extension congruence, and WExt witnesses. Charge the adaptive cover of these edges to alpha_ext.
- Induct on proof lines. Propositional EF steps add no SAT labels; SAT_U introduction carries an occurrence node; extension congruence adds a quotient edge; WExt adds a witness-charged quotient edge; cuts and substitutions preserve the quotient semantics.
- Canonicalize each connected component to obtain Q_pi. Because every contracted edge has a witness, SAT values are preserved within the component without invoking an unparsed semantic oracle.
- Define LocSat(Q_pi) as all Boolean labelings of quotient components satisfying the parsed local SAT facts. A row is forced when the XOR of its M_N labels is constant over LocSat(Q_pi).
- For nonforced rows, the private-row spoof gives two completions with opposite row parity, so local proof soundness alone cannot certify row hardness there. These rows must be handled by residual patching or by a stronger semantic rule.
- If |ForcedRows|<=N^{f+o(1)} and residual disagreements are |R_N|<=N^{r+o(1)}, construct a circuit for H_N^SAT: compute G_N with cost N^{rho+o(1)}, open the low-cover labels across M_N queries with cost N^{q+alpha_ext+o(1)}, and hardwire patches on forced/residual rows at cost N^{max{f,r}+1+o(1)}.
- Conclude C(H_N^SAT)<=N^{max{rho,q+alpha_ext,max{f,r}+1}+o(1)}. Therefore any same-family lower-bound certificate claiming exponent theta above this maximum is invalid for the low-cover P_wExt carrier.

Blocking gap: Full EF+SAT_U+uExt remains blocked at the named UExtWitnessability lemma: every semantic extensionality step must either expose an advice-free quotient witness or be treated as a nonrelativizing semantic-oracle rule outside the occurrence-parser model.

## Falsifiers

- A low-cover P_wExt certificate with theta>max{rho,q+alpha_ext,max{f,r}+1} is a direct falsifier of its own claimed beta-zero lower-bound exponent.
- Any uExt step lacking an advice-free quotient witness falsifies the occurrence-transcript extraction and must be quarantined as semantic-oracle access.
- If ForcedRows has exponent at least theta-1, the patch upper bound no longer contradicts the claimed lower bound and the low-cover falsifier is inconclusive.
- If the row selector or quotient canonicalizer uses nonuniform advice, the target-preserving condition fails and no valid E-uniform or advice-free carrier transfer is obtained.
- A private-row spoof for a nonforced row falsifies any argument that ordinary local proof soundness alone implies row-parity binding.
- If alpha_ext is at least theta-q, adaptive-cover leakage is too expensive to yield a contradiction, so the route must prove high-cover necessity rather than promote a lower-bound claim.

## Learning

Cycle 91 improves the paper packet by making the witnessed-extensionality branch theorem-shaped rather than a repeated fork. In P_wExt, formula identity is paid for by alpha_ext through an explicit quotient transcript, yielding the valid upper-bound falsifier C(H_N^SAT)<=N^{max{rho,q+alpha_ext,max{f,r}+1}+o(1)}. The only remaining full-system escape is not generic proof strength but the named UExtWitnessability failure: semantic SAT-extensionality without an advice-free quotient witness is outside the controlled MCSP/MKtP carrier interface.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the WExt versus uExt proof-system boundary.`
- Rationale: The current branch needs a concrete target-preserving test of whether witnessed formula identity is merely low-cover leakage or a genuine semantic escape; another abstract barrier statement would not close the proof-delivery queue item.
- Situation seed: Take H_N^SAT(x)=xor_{j<=N^q} SAT(G_N(x,j)) with L_N=(log N)^d and a P_wExt proof pi whose only nonlocal moves identify generated formulas through explicit quotient witnesses; then replace one family of witness edges by unwitnessed uExt edges and compare the induced transcript.
- Varied variable: alpha_ext, the adaptive cover exponent of formula-identity witnesses, with a secondary binary switch indicating whether extensionality is witnessed or unwitnessed.
- Held-fixed controls: M_N=N^{q+o(1)} and generator size N^{rho+o(1)} are fixed below the claimed lower-bound exponent theta., The target circuit model remains unrestricted nonuniform Boolean circuits for the same N-row H_N^SAT truth table., No advice, hard-row selector, or nonuniform quotient canonicalizer is allowed in the parser., Residual and forced-row exponents r and f are measured in the same row universe before and after quotienting.
- Expected observation: For witnessed edges, the circuit upper bound rises continuously as q+alpha_ext; once alpha_ext<theta-q and max{rho,max{f,r}+1}<theta, the certificate is invalid. For unwitnessed uExt, no cover can be charged, so the extraction fails for a named semantic reason rather than by exponent arithmetic.
- Transfer certificate needed: A formal rule-induction proof that every WExt proof line maps to Q_pi with preserved SAT labels, plus a Cook-Reckhow witnessability certificate for any attempted uExt repair before the intuition may enter proof obligations.

## Next Experiment

Write the finite P_wExt rule table: propositional axiom, cut, substitution, extension introduction, SAT_U occurrence creation, WExt quotient edge, and witness verification. For each rule, record how Q_pi, alpha_ext, ForcedRows, and residual patches change; stop at the first rule that requires unparsed SAT semantics.
