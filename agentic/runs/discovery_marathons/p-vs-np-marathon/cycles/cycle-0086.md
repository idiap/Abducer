# cycle-0086

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta-zero SAT parity carrier, pure occurrence-parser extraction is not valid for EF+SATeq_N. The repaired theorem must classify a short accepted certificate as functional-naturalizing, occurrence-full-row expensive, or EqSAT-link-covered; if the remaining uncovered rows are fewer than N^{epsilon-o(1)} and the link transcript is subthreshold, sparse-row patching gives a source-lower-bound falsifier.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with |x|=N, M_N=N^{q+o(1)}, generated formulas of length L_N=(log N)^d, and generator circuit size N^{rho+o(1)}.
- target object: a proof-mediated source certificate in Psys=EF+SATeq_N for Ckt(H_N^SAT)>N^{1+epsilon-o(1)}, used only to support the beta-zero magnification route.
- controlled interface: beta=0 substitution of a polynomial-size SAT circuit on L_N-bit formulas into the batched generator, plus a certificate parser that may expose occurrence rows or semantic EqSAT links.
- target-preserving condition: max{rho,q}<1+epsilon, no nonuniform advice beyond the generated formulas and parsed proof transcript, and no upgrade from route-level source evidence to P != NP without the source lower bound.
- EqSAT link: a proof-system edge asserting SAT(F)<->SAT(F') for formulas related by uniform padding, renaming, clause duplication, or another explicitly named equisatisfiable transformation admitted by EF+SATeq_N.
- link-covered row: a source input x whose parity vector over the M_N generated SAT labels is determined over F_2 by occurrence values, constants, and EqSAT equality classes named by the parsed transcript.

## Assumptions

- Circuit model is nonuniform Boolean circuits of fan-in two, with equality-to-a-row tests costing O(N) gates per patched source row.
- EF+SATeq_N contains ordinary EF reasoning plus a sound schema for explicitly checkable equisatisfiable formula identities; this is SAT-semantic and nonrelativizing, not an occurrence-label oracle rule.
- Functional extraction means the accepted proof defines a truth-table property over arbitrary label vectors with constructivity and density sufficient for the previously audited naturalization gate.
- Occurrence extraction means the parsed transcript is invariant under private flips of SAT labels not syntactically touched by the proof; this invariance fails for EqSAT-linked labels.
- All asymptotics are for valid lengths N in the generator family, with q,rho,epsilon fixed constants and d>1 in the polylogarithmic query window.

## Equations

- beta0_transfer: `\mathrm{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+M_N L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when SAT on L_N-bit formulas has circuits of size L_N^c and the generator is substituted without advice leakage or positive target-query exponent.
- row_residual_patching: `C(H_N^{SAT})\le S_D+O(E_N N)`. Valid when: Applies when a circuit D_N of size S_D agrees with H_N^SAT outside E_N explicitly hardwired source rows and equality tests cost O(N).
- semantic_link_residual: `C(H_N^{SAT})\le S_T+S_D+O(E_N N)`. Valid when: Valid when the parsed EF+SATeq_N transcript T_N is label-free, has circuit cost S_T, and determines all but E_N rows through occurrence values or EqSAT links.
- source_threshold_consequence: `C(H_N^{SAT})>N^{1+\epsilon-o(1)}\ \wedge\ S_T+S_D<N^{1+\epsilon-o(1)}\Rightarrow E_N\ge N^{\epsilon-o(1)}`. Valid when: Requires the row-residual patching bound and a claimed barely-superlinear source lower bound at the same valid generator lengths.
- pure_occurrence_failure_pattern: `\mathrm{ForcedRows}_{occ}(\pi_N)=0,\quad \mathrm{LinkCoveredRows}_{EqSAT}(\pi_N)=N`. Valid when: Applies to paired-padding carriers where EF+SATeq_N proves parity cancellation through semantic equality links rather than complete occurrence-row queries.

## Attempted Derivation

- Fix Psys=EF+SATeq_N: EF plus explicitly checkable equisatisfiable formula identities such as padding, renaming, and clause duplication.
- Test the previous parser theorem against the paired-padding generator G_N(x,2i)=Pad(G_N(x,2i-1)). EF+SATeq_N proves equality of paired SAT labels and hence XOR cancellation.
- Observe that a private occurrence-label spoof that flips only one member of a pair is not a model of EF+SATeq_N. Therefore the old occurrence-relativizing falsifier is not valid against this proof system.
- Repair the observable from ForcedRows_occ to a semantic-link transcript T_N containing occurrence values, constants, and EqSAT equality edges. A row is covered when its parity vector is determined modulo these links.
- Derive the residual upper bound C(H_N^SAT)<=S_T+S_D+O(E_N N). Thus any accepted certificate with subthreshold transcript and fewer than N^{epsilon-o(1)} uncovered rows is a concrete falsifier for a claimed N^{1+epsilon-o(1)} source lower bound.
- Attempt to extend the repair to all EF+SATeq_N proofs by translating each proof inference into the link transcript. The translation works for padding, renaming, duplicate clauses, and local formula isomorphisms.

Blocking gap: The normal form is not proved for arbitrary EF reasoning that invokes SAT self-reducibility, extension variables encoding witnesses, or nonlocal formula transformations not decomposed into explicit EqSAT links.

## Falsifiers

- Semantic-link falsifier: a subthreshold EqSAT-link transcript covering all but fewer than N^{epsilon-o(1)} rows gives an actual circuit upper bound by sparse-row patching.
- Paired-padding falsifier: EF+SATeq_N can prove XOR cancellations with zero occurrence-forced rows, so a pure occurrence parser is not valid for this named proof system.
- Functional-naturalization falsifier: if accepted certificates define dense constructive label properties over arbitrary truth tables, the route falls back into the naturalization audit rather than a SAT-semantic escape.
- Positive-beta falsifier remains quarantined: any repair that reintroduces L_N=N^beta target queries obeys the old q+beta c transfer cap and loses all-exponent target preservation.
- Advice-leakage falsifier: a transcript that hardwires SAT labels on the generated range is not valid source evidence, because it hides the target truth table in the certificate.

## Learning

Cycle 86 resolves one part of the formula-semantic fork: occurrence-only extraction is false for EF+SATeq_N because real EqSAT identities are nonrelativizing semantic links. The valid replacement object is a semantic-link residual transcript; subthreshold link coverage is a falsifier for source lower-bound certificates, while the open proof task is a normal form for arbitrary EF+SATeq_N reasoning.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The proof fork is blocked by a concrete semantic distinction: occurrence labels can be privately spoofed, but EqSAT-linked formula pairs cannot. Varying the amount of semantic linking tests whether the repaired audit has a real threshold rather than another restatement of hardness magnification.
- Situation seed: A beta-zero XOR carrier with M_N=N^{q+o(1)} polylog-length SAT instances, where a gamma_N fraction of slots in every row are paired with uniformly padded EqSAT twins and the remaining slots are generated independently.
- Varied variable: gamma_N, the fraction of row parity positions covered by EF+SATeq_N padding-equivalence links; equivalently vary the residual uncovered-row exponent theta where E_N=N^theta.
- Held-fixed controls: L_N=(log N)^d with d>1, q,rho<1+epsilon, and generator size N^{rho+o(1)}., Proof system fixed as EF+SATeq_N with only explicitly checkable padding, renaming, and duplicate-clause EqSAT rules., No SAT truth-table advice is allowed in the transcript; only formula descriptions and link certificates are allowed., The target bridge remains beta=0, so SAT in SIZE(n^c) still transfers as N^{max{rho,q}+o(1)} for every fixed c.
- Expected observation: As gamma_N approaches 1, occurrence ForcedRows remains small while EqSAT link coverage determines most row parities. If E_N<N^{epsilon-o(1)}, the carrier becomes subthreshold easy despite the occurrence parser reporting no full rows.
- Transfer certificate needed: A uniform label-free link-transcript construction and an F_2 row-coverage calculation showing that uncovered rows are exactly the residual rows patchable at O(E_N N) cost before the intuition can affect proof obligations.

## Next Experiment

Work the EF+SATeq_N normal-form proof rule by rule: padding, renaming, duplicate clauses, extension-variable abbreviations, and SAT self-reduction; either translate each into a bounded EqSAT-link transcript or isolate the first noncompressible SAT-semantic principle as the next theorem-shaped counterexample.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Conditional row-forcing theorem for a concrete strong system: fix Psys=EF+SAT_U^comp, Extended Frege over circuit reasoning plus explicit SAT composition axioms for formulas of length at most L_N^{O(1)}. If a polynomial-time SemanticSupportParser maps every accepted proof pi of LB_{N,s}(H_N^SAT) to a row set K_pi and satisfies proof-invariance plus semantic-completion for off-support residuals, then any valid proof of C(H_N^SAT)>s_N=N^{1+epsilon-o(1)} forces |K_pi|>=N^{epsilon-o(1)} whenever the residual circuit exponent lambda is below 1+epsilon.

## Definitions

- source object: a concrete EF+SAT_U^comp proof pi of LB_{N,s}, where LB asserts that every circuit of size less than s_N fails to compute H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)).
- target object: a fork-resolving extraction/no-go statement for beta-zero SAT parity carriers, measured by semantic row charge |K_pi| and residual circuit size.
- controlled interface: SemanticSupportParser(pi) returns rows K_pi touched by equality and SAT-composition axiom supports, and SemanticCompletion(K_pi,D_N) supplies a target-preserving spoof model for rows outside K_pi.
- target-preserving condition: the spoof completion must preserve proof acceptance, all parsed SAT_U^comp axioms, the same input length N, the same lower-bound threshold s_N, and the same circuit target SIZE_N(s_N).

## Assumptions

- Model: Psys is EF+SAT_U^comp with propositional EF rules, syntactic formula equality, and sound local composition axioms such as S(F or G)<->S(F) or S(G), all length bounded by L_N^{O(1)}.
- Uniformity: G_N is computable by circuits of size N^{rho+o(1)}, M_N<=N^{q+o(1)}, and each generated formula has length L_N=(log N)^d.
- Threshold regime: s_N=N^{1+epsilon-o(1)} and the off-support residual D_N has circuit size S(D_N)=N^{lambda+o(1)} with lambda<1+epsilon.
- Parser assumption: each nonlogical SAT axiom instance in pi has a row-support set supp_row(a), and K_pi is the union over all such supports after equality and composition closure.
- Semantic-completion assumption: for every D_N agreeing with H_N^SAT outside K_pi, the parsed proof has a model in which rows outside K_pi realize D_N while all axiom instances used by pi remain true.
- Non-claim: this is a route-level conditional theorem; it is not a proof of P != NP and not yet a full EF+SAT_U extraction theorem.

## Equations

- beta_zero_carrier: `H_N^{\mathrm{SAT}}(x)=\bigoplus_{j=1}^{M_N}\mathrm{SAT}(G_N(x,j))`. Valid when: Valid when the beta-zero carrier fixes N input rows, M_N<=N^{q+o(1)}, and G_N outputs formulas of length L_N.
- semantic_support_union: `K_\pi=\bigcup_{a\in Ax_{\mathrm{SAT}}(\pi)} supp_{row}(a)`. Valid when: Valid when every SAT-semantic axiom instance in the proof has been expanded through equality and composition supports.
- sparse_residual_patch: `C(H_N^{\mathrm{SAT}})\le S(D_N)+O(|K_\pi|N)`. Valid when: Valid when D_N agrees with H_N^{SAT} outside the parsed row set K_pi and exceptions are hardwired by row-index patches.
- forced_semantic_charge: `|K_\pi|\ge \Omega((s_N-S(D_N))/N)=N^{\epsilon-o(1)}`. Valid when: Applies after Psys soundness, semantic completion, and the sparse-patch upper bound all preserve the same N and threshold s_N=N^{1+epsilon-o(1)}.

## Attempted Derivation

- Fixed the concrete proof system Psys=EF+SAT_U^comp rather than an unnamed strong system; its SAT facts are syntactic equality plus local composition axioms for S(F).
- Formalized the lower-bound sentence LB_{N,s}: every circuit C of size <s_N differs from x -> xor_{j<=M_N} S(G_N(x,j)) on some x in {0,1}^{log N}.
- Defined row supports recursively: generated atom S(G_N(x,j)) supports row x; equality preserves support; composition axioms support the union of their subformula supports.
- Showed that propositional EF inference is syntactically invariant under changing unmentioned SAT atoms; the only possible leakage is through nonlogical SAT_U^comp axioms.
- Derived the conditional sparse-patching contradiction: if SemanticCompletion supplies an easy residual D_N off K_pi and |K_pi|<N^{epsilon-o(1)}, then C(H_N^SAT)<=N^{lambda+o(1)}+O(|K_pi|N)<s_N, contradicting sound proof acceptance in the spoof model.
- Tested the previous equality-only invariant against S(F or G)<->S(F) or S(G) and found a finite falsifier: equality fibers miss rows that subformula composition semantically touches.

Blocking gap: SemanticCompletion is not proved for full EF+SAT_U^comp. Local row assignments may violate global SAT self-reducibility or formula-composition constraints on non-generated formulas, and constructing a compatible completion appears to require a RowSyntaxRealizer or an explicit nonrelativizing SAT-semantic principle.

## Falsifiers

- Finite composition falsifier: B=F or G with F=G_N(x_1,j_1), G=G_N(x_2,j_2) defeats an equality-only parser because B is not in either generated equality fiber but its SAT axiom depends on both rows.
- Sparse semantic-support falsifier: if an accepted proof has |K_pi|<N^{epsilon-o(1)} and a valid semantic completion to an easy D_N exists, then sparse patching gives C(H_N^SAT)<N^{1+epsilon-o(1)} and refutes the claimed source lower-bound certificate.
- Natural-property falsifier: if the proof route becomes a poly(N)-constructive N^{-O(1)}-dense property useful against SIZE_N(s_N), then PRF tension applies to the exact target class unless the object is non-large or nonconstructive.
- Formula-normalization falsifier: if a proof uses semantic equivalence of formulas without exposing generated leaves, then row-support extraction is not a syntactic parser and must be charged as a SAT-semantic escape rather than a valid occurrence-relativizing transcript.

## Learning

Cycle 86 sharpens the full formula-semantic fork: equality-closed charge is valid only for P_eq, while EF+SAT_U^comp needs semantic row support plus a separate SemanticCompletion theorem. The new finite falsifier is the SAT-composition axiom, and the new positive bridge is the conditional forced-charge inequality |K_pi|>=N^{epsilon-o(1)} under completion. This is route-level proof-boundary progress, not P != NP progress.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The abstract gap is now specifically SemanticCompletion for EF+SAT_U^comp; a concrete OR-block carrier tests whether semantic support, not equality support, is the right quantitative invariant.
- Situation seed: Take the beta-zero carrier with polylogarithmic 3CNF queries G_N(x,j), add proof atoms B_Blk=OR_{x in Blk} G_N(x,1) for blocks Blk of rows, and allow EF+SAT_U^comp to use S(B_Blk)<->OR_{x in Blk} S(G_N(x,1)) when the composed formula length stays within L_N^{O(1)}.
- Varied variable: block row exponent gamma where |Blk|=N^gamma, truncated to the maximum allowed by the formula-length bound.
- Held-fixed controls: H_N^SAT, M_N<=N^{q+o(1)}, and G_N size N^{rho+o(1)} remain fixed., The lower-bound target remains SIZE_N(N^{1+epsilon-o(1)})., The parser must be uniform and must not use advice about actual SAT values., Residual patching cost remains O(|K|N) on complete rows.
- Expected observation: Equality charge stays near zero for B_Blk, while semantic-support charge grows like N^gamma per block. If total semantic charge is below N^epsilon, an easy residual completion would falsify the certificate; if it exceeds N^epsilon, the proof pays the same full-row threshold as the occurrence theorem.
- Transfer certificate needed: A formal SemanticCompletion theorem for these OR-block axioms, or a proof that OR-block SAT composition is already a nonrelativizing SAT-semantic principle outside the occurrence/full-row obstruction.

## Next Experiment

Instantiate the OR-block EF+SAT_U^comp carrier, compute the maximum block exponent gamma allowed by the formula-length cutoff, and try to prove SemanticCompletion for the parsed OR axioms; if completion fails, record the exact violated SAT-semantic constraint as the next countermodel.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Witnessed-extensionality cover lemma: for P_wExt=EF+SAT_U^{occ} plus only witnessed formula-identity/SAT-extensionality rules, every short row-parity proof pi whose quotient and extensionality witnesses have adaptive-cover exponent alpha_ext yields C(H_N^SAT)<=N^{max{rho,q+alpha_ext,max(f,r)+1}+o(1)}. Hence any claimed beta-zero source lower bound C(H_N^SAT)>N^{1+epsilon-o(1)} is falsified whenever max{rho,q+alpha_ext,max(f,r)+1}<1+epsilon.

## Definitions

- source object: a short EF+SAT_U^{wit-ext} proof pi of an alleged lower-bound or row-parity certificate for H_N^SAT, where each formula-identity or SAT-extensionality line carries an explicit quotient/transducer witness.
- target object: an unrestricted Boolean circuit upper bound for H_N^SAT, used only as a route-specific falsifier of a stronger beta-zero lower-bound claim, not as evidence for P != NP.
- controlled interface: parser pi -> (Q_pi,E_pi,W_pi,R_pi,F_pi) producing occurrence queries, equality quotient edges, witnessed extensionality openers, residual rows, and forced rows.
- target-preserving condition: the parser, quotient contraction, witness openers, residual list, and patch circuit are E-uniform and advice-free, with SAT instance length L_N=(log N)^d and generator size N^{rho+o(1)}.

## Assumptions

- Model: circuits are unrestricted nonuniform Boolean circuits on the N-bit x input; proof parsing is uniform and does not use hard-row advice.
- Proof system: P_wExt contains EF+SAT_U^{occ}, definitional equality, and Ext(F,F',w) only when w supplies a checkable E-uniform satisfiability-preserving transducer or quotient witness; no bare semantic identity axiom is allowed.
- Parameter regime: M_N=N^{q+o(1)}, generator circuit size is N^{rho+o(1)}, equality quotient cover is alpha_eq, adaptive proof-opening cover is alpha_ad, and extensionality witness cover is alpha_wit.
- Binding regime: after parsing pi, the induced approximator agrees with row parity outside residual rows R_N of size N^{r+o(1)} and forced/exception rows F_N of size N^{f+o(1)}.
- Naturalness/barrier regime: the argument is a finite falsifier and does not construct a large useful property; it is valid only for low-cover witnessed proofs and is silent about opaque semantic SAT principles.

## Equations

- beta_zero_carrier: `H_N^{\mathrm{SAT}}(x)=\bigoplus_{j\le M_N}\mathrm{SAT}(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad L_N=(\log N)^d`. Valid when: Valid when the source carrier is the beta-zero SAT parity family with polylogarithmic SAT instances and a uniform generator G_N.
- combined_cover_exponent: `\alpha_{\mathrm{ext}}=\max\{\alpha_{\mathrm{ad}},\alpha_{\mathrm{eq}},\alpha_{\mathrm{wit}}\}`. Valid when: Valid when occurrence openings, equality quotient contractions, and extensionality witnesses are all parsed into the same adaptive-cover model.
- patch_upper_bound: `C(H_N^{\mathrm{SAT}})\le N^{\max\{\rho,q+\alpha_{\mathrm{ext}},\max\{f,r\}+1\}+o(1)}`. Valid when: Applies after the reduction preserves generator uniformity, low-cover witness access, and hardwired patching of residual or forced rows.
- lower_bound_falsifier_threshold: `\max\{\rho,q+\alpha_{\mathrm{ext}},\max\{f,r\}+1\}<1+\epsilon\ \Longrightarrow\ C(H_N^{\mathrm{SAT}})\not>N^{1+\epsilon-o(1)}`. Valid when: Valid when the target claim is an unrestricted circuit lower bound for the same H_N^SAT family and no advice-selected row is substituted.

## Attempted Derivation

- Fix P_wExt and parse pi into occurrence SAT queries Q_pi, definitional equality edges, witnessed extensionality edges W_pi, residual rows R_N, and forced rows F_N.
- Contract definitional identity and extension-variable congruence edges into an equality quotient; charge the quotient opener by alpha_eq.
- For each witnessed Ext(F,F',w), replace the opaque semantic equality by the supplied satisfiability-preserving transducer or quotient witness; charge its opener by alpha_wit.
- Flatten occurrence openings, equality quotient openings, and extensionality witnesses into one adaptive cover with exponent alpha_ext=max{alpha_ad,alpha_eq,alpha_wit}.
- For every nonexception row, compute the parity over M_N=N^{q+o(1)} generated SAT instances using the cover opener; this costs N^{q+alpha_ext+o(1)} plus generator overhead N^{rho+o(1)}.
- Hardwire the truth values on residual and forced rows; the patch uses O((|R_N|+|F_N|)N) gates, giving exponent max{f,r}+1.
- Taking the maximum of generator, low-cover evaluation, and patch costs yields C(H_N^SAT)<=N^{max{rho,q+alpha_ext,max(f,r)+1}+o(1)}.
- Attempting the same derivation for full P_sem stops at a bare EqSAT(F,F') line, because no quotient, transducer, or occurrence transcript exists from which to recover row labels.

Blocking gap: Full EF+SAT_U with unparsed semantic formula identity may use actual SAT extensionality as a nonrelativizing proof principle; the current parser has no valid cover parameter for that rule.

## Falsifiers

- Low-cover witnessed extensionality with alpha_ext below the claimed theta gives an explicit same-target circuit upper bound and is a decisive falsifier for the carrier.
- A single bare semantic EqSAT(F,F') step in P_sem is a falsifier for occurrence-relativizing parser claims, because the hidden equivalence is not represented in Q_pi.
- Residual or forced rows of size below N^{epsilon-o(1)} are patchable by O(|R|N) gates and invalidate stronger row-residual lower-bound certificates.
- Any MCSP/MKtP hard-row selector using nonuniform formula-equivalence advice identifies only a hard row, not an advice-free target language lower bound.
- Dense constructive projection repairs that make the accepted certificate set large and useful re-enter the natural-proofs danger zone; sparse generated witnesses avoid that barrier but must still survive cover leakage.

## Learning

Cycle 86 separates two full-system cases: witnessed formula identity is harmless and collapses to the existing low-cover patch upper bound, while unwitnessed SAT-extensionality is the precise nonrelativizing semantic principle that blocks the occurrence parser. This is route-level progress: it certifies a finite falsifier for P_wExt and names the remaining escape, without claiming P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the formula-semantic extraction fork.`
- Rationale: The branch no longer needs another abstract hardness-magnification restatement; it needs to decide whether formula identity is harmless low-cover syntax or a genuine SAT-semantic escape from occurrence transcripts.
- Situation seed: Take H_N^SAT(x)=xor_{j<=N^q} SAT(G_N(x,j)) with L_N=(log N)^d. Build two proof packets for the same row-parity claim: one replaces each G_N(x,j) by a low-cover Tseitin/extension-equivalent formula with explicit witnesses, and the other uses a single opaque semantic EqSAT axiom for occurrence-disjoint equivalent formulas.
- Varied variable: alpha_wit, the adaptive-cover exponent of extensionality witnesses, with a sentinel value opaque for unwitnessed semantic equality.
- Held-fixed controls: Generator size remains N^{rho+o(1)} and the query exponent remains q., The target is the same unrestricted circuit lower bound for H_N^SAT, not an advice-selected row statement., Residual exponent r and forced-row exponent f are held fixed., All witness-bearing variants must be E-uniform and advice-free.
- Expected observation: For alpha_wit below the threshold, the patch upper bound appears with exponent max{rho,q+alpha_ext,max(f,r)+1}; for opaque semantic equality, the occurrence parser cannot form Q_pi, exposing a nonrelativizing escape rather than a valid carrier transfer.
- Transfer certificate needed: An E-uniform quotient/transducer extractor for every extensionality line, plus a proof that the extractor preserves SAT semantics, row parity, and the q,rho,r,f parameter ledger.

## Next Experiment

Instantiate Psys as EF+SAT_U^{occ}+Tseitin-witnessed extensionality. Define the witness grammar, prove the extractor pi -> (Q_pi,E_pi,W_pi), and compute alpha_wit for Tseitin expansions, extension-variable congruence, and formula renaming; then test whether any full-EF lower-bound proof needs a bare EqSAT rule outside this grammar.
