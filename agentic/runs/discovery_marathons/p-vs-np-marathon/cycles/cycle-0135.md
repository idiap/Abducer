# cycle-0135

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

CounterfactualDTSRSupport_N theorem pair: for Psys_sym^{CTSR} proofs whose bounded Tseitin self-reduction rule declares every counterfactual child row in the reachable support cone before using the rule, the least closed support fixed point K_CTSR(pi) yields a valid Gamma_CTSR parser-to-circuit falsifier. If a reachable child row can influence a later FormulaEval/SR line while absent from K_CTSR(pi), a first-hidden-child private-row construction refutes surface occurrence completion for that proof syntax.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, beta=0 polylog target-query length, generator size N^{rho+o(1)}, and source claim LB_N(1+epsilon): SIZE(H_N)>N^{1+epsilon-o(1)}.
- target object: a same-model nonuniform SIZE circuit upper bound for H_N extracted from a Psys_sym^{CTSR} lower-bound certificate, used only as a falsifier of that certificate/source claim.
- controlled interface: bit-explicit Psys_bEF plus transparent FormulaEval plus counterfactually declared bounded Tseitin self-reduction rows, with every reachable influence row enumerated before rule use and charged in Gamma_CTSR.
- target-preserving condition: the extracted circuit uses the same nonuniform SIZE model, the same generated SAT instances, beta=0 substitution, no hidden advice row selectors, and all row expansion charges stay below N^{1+epsilon-o(1)}.
- K_CTSR(pi) is the least fixed point starting from final LB_N dependencies and closing under EF parent pointers, SATeq links, FormulaEval reachable support, and every declared SR child row for every branch of each bounded TSR node.
- A CTSR line has verifier-visible fields: parent row id (x,j), formula node id a, depth t<=h, restriction prefix sigma, complete child list Child(a,sigma), row encodings for all children, and same-theory certificates for the local OR/equality relation.

## Assumptions

- Circuit model is nonuniform SIZE over Boolean circuits; the parser, carrier upper bound, and LB_N claim are interpreted in this same model with no change of target class.
- Length regime has M_N=N^{q+o(1)}, formula/query length L_N=(log N)^{O(1)}, generator overhead N^{rho+o(1)}, and beta=0 target substitution cost.
- Uniformity/advice regime: proof syntax and N determine all row sets, child lists, and enumerators; no semantic advice bit may choose an undeclared satisfying branch or hide a row selector.
- Counterfactual declaration regime: every restriction child of every used bounded-TSR node is listed even if the actual semantic branch would later be pruned; actual-branch-only listing is not sufficient.
- Threshold regime: rho<1+epsilon, Gamma_CTSR(pi)<N^{1+epsilon-o(1)}, and residual row error E_pi<N^{epsilon-o(1)} are the only conditions under which the extracted circuit contradicts LB_N(1+epsilon).
- Barrier status: the positive theorem is relativizing/parser-syntactic; any escape for hidden real SAT pruning must be nonrelativizing through RealSATInfluenceRealizer_N^{arb}, not a generic natural-proofs or algebrization claim.

## Equations

- carrier: `H_N^{\mathrm{SAT}}(x)=\bigoplus_{j\le M_N} \mathrm{SAT}(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N(x,j)|=(\log N)^{O(1)}`. Valid when: Valid when the beta-zero parity carrier and generator family are fixed uniformly for all source lengths N.
- ctsr-ledger: `\Gamma_{\mathrm{CTSR}}(\pi)=\Gamma_{\mathrm{bEF}}(\pi)+U(K_{\mathrm{CTSR}})+X(K_{\mathrm{CTSR}})+T_{\mathrm{CTSR}}(\pi)`. Valid when: Applies after K_CTSR is computed as the least influence-closed fixed point visible from the proof syntax.
- counterfactual-tsr-charge: `T_{\mathrm{CTSR}}(\pi)=N\cdot |\mathrm{ChildDecl}_{\mathrm{cf}}(\pi)|\cdot N^{o(1)}=N^{1+\kappa+\theta+o(1)}`. Valid when: Requires complete counterfactual child declaration with N^{kappa+theta+o(1)} declared row children and polylogarithmic row encodings.
- parser-upper-bound: `C_{\mathrm{SIZE}}(H_N)\le N^{\rho+o(1)}+\Gamma_{\mathrm{CTSR}}(\pi)+O(E_\pi N)`. Valid when: Valid when the line induction has converted every visible proof dependency into a same-model circuit fragment and E_pi residual rows are equality patched.
- subthreshold-falsifier: `\max\{\rho,1+\kappa+\theta,1+\log_N E_\pi\}<1+\epsilon\Rightarrow C(H_N)<N^{1+\epsilon-o(1)}`. Valid when: Applies in the nonuniform SIZE regime where all Gamma components are charged and compared against the claimed LB_N threshold.

## Attempted Derivation

- Define K_CTSR^0 from the final LB_N line and iterate a finite monotone closure: add EF parent rows, SATeq quotient links, FormulaEval support rows certified by visible enumerators or full scan, and for each CTSR node add every child row in the counterfactual child list.
- For a CTSR line with parent (x,j,a,sigma,t), the local verifier recomputes each child restriction formula, checks the child row encoding, and checks the bounded Tseitin OR/equality certificate in the same proof theory; the per-child bit overhead is polylogarithmic, hence N^{o(1)} after row expansion.
- Line induction invariant: after processing any prefix of pi, every formula-label dependency reachable from that prefix lies in K_CTSR and contributes to Gamma_bEF, U, X, or T_CTSR; no later symbolic use may introduce an uncharged row because prefix closure re-runs the fixed point.
- Circuit extraction: combine the generator circuit of size N^{rho+o(1)}, the parsed proof fragments charged by Gamma_CTSR, and equality patches for E_pi residual rows, giving C(H_N)<=N^{rho+o(1)}+Gamma_CTSR+O(E_pi N).
- Threshold comparison: if kappa+theta<epsilon, rho<1+epsilon, and E_pi<N^{epsilon-o(1)}, the extracted circuit is below N^{1+epsilon-o(1)}, so the transcript is a falsifier for a claimed same-model LB_N(1+epsilon) certificate.
- Necessity attempt: if a first reachable child row c* is used semantically but not listed, build two label worlds agreeing on every visible row and proof bit while flipping an unread enable bit for c*; the parent CTSR value and therefore one carrier parity row can differ, so surface occurrence completion is not sound.

Blocking gap: The two-world private-row argument is a no-go for extensional or relativizing hidden support, not a proof against real SAT-specific semantic pruning. Full semantic pruning remains blocked exactly at RealSATInfluenceRealizer_N^{arb}.

## Falsifiers

- first-hidden-counterfactual-child private-row falsifier for actual-branch-only DTSR declarations
- unread-enable-bit falsifier for FormulaEval lines whose later symbolic use reaches an uncharged row
- threshold falsifier when kappa+theta>=epsilon or rho>=1+epsilon because Gamma_CTSR no longer contradicts LB_N(1+epsilon)
- nonuniform leakage falsifier when a row set is selected by SAT truth advice rather than proof syntax and N
- model mismatch falsifier if the extracted upper bound changes circuit class, uses oracle labels, or leaves the same SIZE model

## Learning

Cycle 135 upgrades declared TSR to counterfactual declared TSR: complete counterfactual child support is sufficient for the Gamma_CTSR parser and necessary for extensional safety. The exact new falsifier is first-hidden-child adaptive pruning; the only full semantic escape is a charged nonrelativizing RealSATInfluenceRealizer_N^{arb}. This is a route-level theorem/countermodel boundary, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch already has a positive transparent-support theorem; the unresolved risk is whether adaptive semantic pruning can avoid counterfactual row charge while preserving the beta-zero transfer. A concrete private-row experiment tests the exact theorem boundary.
- Situation seed: Take H_N^SAT with M_N=N^{q+o(1)} and a Psys_sym proof containing one bounded TSR line for generated formula G_N(x,j). The proof lists only the actual satisfying restriction child and later FormulaEval reads a predicate depending on an unlisted sibling child c*.
- Varied variable: zeta, the exponent of declared counterfactual child coverage, ranging from actual-branch-only zeta=0 to complete coverage zeta=kappa+theta.
- Held-fixed controls: beta=0 polylog target-query length and the same nonuniform SIZE model, generator overhead N^{rho+o(1)} with rho<1+epsilon, bounded TSR depth h and same Tseitin restriction schema, no SAT truth advice in row selection and no change to the final LB_N assertion
- Expected observation: For zeta<kappa+theta there is a first unlisted child c*; two label worlds agree on the visible transcript but differ on c*, so the proof can accept while the induced carrier parity changes. At zeta=kappa+theta the spoof disappears and the ledger pays T_CTSR=N^{1+kappa+theta+o(1)}.
- Transfer certificate needed: A formal first-hidden-child theorem for extensional labels, plus a nonrelativizing RealSATInfluenceRealizer_N^{arb} certificate before any real SAT semantic pruning intuition may alter proof obligations.

## Next Experiment

Resolve RealSATInfluenceRealizer_N^{arb} for one concrete semantic rule: bounded Tseitin self-reduction with adaptive unsat-branch pruning. Either produce a syntax-and-N computable influence row list R_A with charge in Gamma_real, or formalize the first unchargeable semantic inference as a private-row no-realizer theorem.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For a BTRS-visible Psys_sym proof pi of LB_N(1+epsilon) for the beta-zero SAT-parity carrier, only the reverse-reachable transparent support cone from the final lower-bound line must be charged. After deleting unreachable FormulaEval material, the prefix-spliced bEF expansion has charge Gamma_BTRS(K*) and gives the same-model SIZE falsifier whenever N^{rho+o(1)}+Gamma_BTRS(K*)<N^{1+epsilon-o(1)}.

## Definitions

- source object: an accepted Psys_sym^BTRS proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with N=2^n and M_N=N^{q+o(1)}.
- target object: a same nonuniform Boolean SIZE upper bound for H_N^SAT below N^{1+epsilon-o(1)}, obtained by parsing pi and expanding only charged reachable FormulaEval support.
- controlled interface: BTRS visibility consists of proof-visible selector code, dependency parent pointers, row enumerators or full-scan charge, influence-closed row covers, same-theory expansion recipes, and no hidden advice or semantic row oracle.
- target-preserving condition: the parser is deterministic from (N,pi), preserves the nonuniform SIZE model and length parameters, uses prefix splicing with fresh extension variables, and never replaces a hidden semantic SAT choice by uncharged advice.
- K*(pi) is the least fixed point starting from the final LB_N line under proof-parent dependencies, bEF occurrence dependencies, visible FormulaEval row supports, and visible existential-index SR_h witness neighborhoods.
- Gamma_BTRS(K*) is the bit-size ledger for the expanded reachable cone: bEF transcript charge plus enumeration debt U_N(K*) plus row-expansion debt X_N(K*) plus explicit FormulaEval expansion debt N E_N^*(K*).

## Assumptions

- Model: nonuniform Boolean circuits over the same input length n=log N; proof-system simulation is extraction/prefix splicing, not a many-one reduction from SAT.
- Regime: M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, bounded SR_h locality h=N^{eta+o(1)}, visible existential witness multiplicity N^{alpha+o(1)}, and generator size N^{rho+o(1)}.
- Uniformity/advice: K*(pi), all row covers, and all expansion recipes are computable from (N,pi) with no SAT-truth advice and no nonuniform selector leakage beyond pi itself.
- Same-theory condition: every transparent FormulaEval line in K* has a row-expanded derivation in the same bEF/SATeq theory, introduced before the first dependent line and with fresh extension variables.
- Soundness boundary: the lemma is restricted to BTRS-visible FormulaEval; arbitrary semantic FormulaEval remains blocked at RealSATInfluenceRealizer_N.

## Equations

- reachable_fixed_point: `K_0={final}; K_{t+1}=K_t union Parents(K_t) union RowSupp_BTRS(K_t); K*=fix(K_t)`. Valid when: Valid when the proof DAG exposes parent pointers and every FormulaEval line has a proof-visible row-support certificate.
- budget_ledger: `Gamma_BTRS(K*)=Gamma_bEF(K*)+U_N(K*)+X_N(K*)+N E_N^*(K*)`. Valid when: Applies after unreachable lines are deleted and all remaining transparent FormulaEval lines are prefix-spliced in the same proof theory.
- uidx_srh_charge: `S_UidxSRh(K*) <= N^{tau+alpha+eta+o(1)},  X_UidxSRh(K*) <= N^{1+tau+alpha+eta+o(1)}`. Valid when: Requires the reachable cone to use visible existential-index bounded-SR_h covers with N^{alpha+o(1)} witnesses per relevant proof line.
- parser_falsifier_inequality: `N^{rho+o(1)}+Gamma_BTRS(K*) < N^{1+epsilon-o(1)} => not valid(LB_N(1+epsilon) by pi)`. Valid when: Valid when the parsed circuit is in the same nonuniform SIZE model and LB_N claims a lower bound against that exact target class.
- subthreshold_exponent_test: `max(rho,1+tau+alpha+eta,g_other) < 1+epsilon implies a same-model upper-bound falsifier`. Valid when: Applies when all other reachable ledger terms have exponent at most g_other and row expansion dominates enumeration only through explicit charges.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Barrier-Aware Lower-Bound Route; source object: an accepted Psys_sym^BTRS proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with N=2^n and M_N=N^{q+o(1)}.; target object: a same nonuniform Boolean SIZE upper bound for H_N^SAT below N^{1+epsilon-o(1)}, obtained by parsing pi and expanding only charged reachable FormulaEval support.; Model: nonuniform Boolean circuits over the same input length n=log N; proof-system simulation is extraction/prefix splicing, not a many-one reduction from SAT..
- Start from the final LB_N line and compute K_0={final}. Iteratively add syntactic parents, bEF occurrence dependencies, and BTRS-certified FormulaEval row supports until a fixed point K* is reached.
- Delete every proof line outside K*. Acyclic parent pointers ensure the final line and all used premises remain derivable; dead FormulaEval padding is irrelevant and must not be charged.
- For each transparent FormulaEval line in topological order inside K*, insert its row-expanded bEF derivation immediately before the first dependent line, using fresh extension variables and the certified row enumerator or full-scan transcript.
- Line induction: ordinary bEF steps contribute Gamma_bEF(K*); enumerators contribute U_N(K*); row-expanded FormulaEval contributes X_N(K*) and N E_N^*(K*). No other line can affect the final LB_N derivation because it is outside K*.
- If N^{rho+o(1)}+Gamma_BTRS(K*)<N^{1+epsilon-o(1)}, combine the generator circuit and the expanded reachable transcript to obtain a circuit below the claimed LB_N threshold. This is the route-specific falsifier, not a P != NP consequence.
- If some reachable FormulaEval influence is not in RowSupp_BTRS, choose the first omitted row r and run the private-row bisimulation: two carriers agree on K* and all surface proof bits but differ at r, so the surface parser is not target-preserving.

Blocking gap: The proof is complete only for BTRS-visible rules. Full semantic FormulaEval is still blocked at RealSATInfluenceRealizer_N: proof syntax must uniformly determine all influence rows and same-theory row expansions before the semantic rule is used.

## Falsifiers

- Dead-line padding falsifier: a proof may contain N^zeta irrelevant transparent FormulaEval lines with zeta large; any theorem charging the whole proof rather than K*(pi) is invalid, while reachable-cone charging remains valid.
- First omitted reachable row falsifier: an unread enable bit selects row r outside the visible cover; two transcripts agree on all charged rows but differ on the hidden parity contribution.
- q<epsilon falsifier: with M_N=N^{q+o(1)}, the carrier has a same-model upper-bound ceiling below N^{1+epsilon-o(1)} after reachable charge accounting, so an LB_N(1+epsilon) proof cannot be valid in the audited model.
- Nonuniform selector-advice falsifier: if RowSupp_BTRS is supplied by advice not recoverable from (N,pi), constructivity and target preservation fail even if the displayed selector syntax is small.

## Learning

Cycle 135 isolates a genuine proof-hygiene improvement: transparent FormulaEval must be charged on the least reverse-reachable support cone, not on the whole proof. This makes the Gamma theorem invariant under dead-line padding and leaves hidden semantic influence quarantined by the first-omitted-row falsifier until RealSATInfluenceRealizer_N is supplied.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The current theorem can overcharge if it counts all transparent FormulaEval lines. A concrete padding experiment tests whether the contribution is a real parser theorem or just another global-budget restatement.
- Situation seed: Take a BTRS-visible proof pi of LB_N for H_N^SAT and append a disconnected block of N^zeta transparent FormulaEval full-scan lines whose outputs are never referenced by the final LB_N line. Keep one reachable annotated UidxSR_h chain with witness exponent alpha and locality eta.
- Varied variable: zeta, the exponent of unreachable transparent FormulaEval padding mass.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, rho<1+epsilon, and the same H_N^SAT carrier are fixed., The reachable UidxSR_h chain remains BTRS-visible with no hidden advice and the same alpha, eta, tau parameters., The final LB_N line and its dependency pointers are unchanged., All FormulaEval lines, reachable or dead, satisfy the local transparent syntax checker.
- Expected observation: A global Gamma theorem changes from subthreshold to superthreshold as zeta increases, although the final derivation and target circuit implication are unchanged. The reachable-cone Gamma_BTRS(K*) is invariant in zeta, so it is the correct target-preserving charge.
- Transfer certificate needed: A deletion and prefix-splice certificate proving that lines outside the reverse dependency cone cannot affect the final LB_N derivation and that every line inside the cone has a same-theory row expansion.

## Next Experiment

Write the finite checker for K*(pi): input (N,pi), output reverse-reachable line set, row-cover list, U_N, X_N, and Gamma_BTRS(K*); test it on the dead-line padding construction and on one unread-enable-bit hidden-row countermodel.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Restricted theorem packet: In Psys_sym^{QE,eq}, quarantined FormulaEval row sharing is valid only through prefix-visible syntactic RowSetEqualityWitness_N records. With such records, the Gamma ledger charges each influential row to its first owner; without them, the proof must pay sum charge or faces a same-theory private-row falsifier. This is a parser/falsifier theorem, not a P != NP lower bound.

## Definitions

- source object: a bit-explicit Psys_sym^{QE,eq} proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with FormulaEval blocks sealed by QE exits and exits forming a prefix-visible dominator forest.
- target object: a same-model nonuniform SIZE circuit for H_N^SAT below N^{1+epsilon-o(1)}, yielding a contradiction only to the claimed finite LB_N line, not to P vs NP.
- controlled interface: RowSetEqualityWitness_N consists of owner-exit id, current-exit id, enumerator node ids, row-index equality proof, occurrence-neighborhood equality proof, and first-owner charge token, all read before the exit's first external dependency.
- target-preserving condition: all row sets, equality witnesses, and row expansions are advice-free, prefix-visible, same-theory SAT occurrence objects; no SAT-truth pruning, hidden semantic equality, or nonuniform row selector may be used.
- K_idx^{own}(pi) is the set of first-owned influential SAT-query indices after equality-witness compression.
- U_N(pi) is the total visible row-discovery/enumerator cost; W_N(pi) is the equality-witness verification cost; X_N^{own}(pi) is the same-theory row-expansion cost for first-owned rows.

## Assumptions

- Length regime: N tends to infinity, M_N=N^{q+o(1)}, formula length and row expansion overhead are N^{o(1)} unless explicitly charged as E_pi.
- Circuit model: target upper bound is unrestricted nonuniform SIZE on the same truth-table family H_N^SAT used by the LB_N proof line.
- Proof model: the base Psys_bEF^- parser theorem and Gamma_bEF(pi) line induction are already valid for non-FormulaEval rules.
- Timing model: each QE exit dominates every external dependency of its quarantined block, and every equality-sharing claim is visible before that exit is used externally.
- Uniformity/advice model: the witness verifier is generated from N and pi bits only; semantic SAT truth, advice-selected rows, and post-hoc equality explanations are not valid inputs.
- Barrier status: the restricted parser is syntactic and sparse, so it does not invoke a large natural property; full semantic FormulaEval remains quarantined at RealSATInfluenceRealizer_N.

## Equations

- owned_gamma: `\Gamma_{QEeq}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+W_N(\pi)+X_N^{own}(\pi)`. Valid when: Valid when exits form a prefix-visible QE dominator forest and every shared row has a syntactic equality witness before first external use.
- owned_row_expansion: `X_N^{own}(\pi)=E_N\cdot |K_{idx}^{own}(\pi)|\cdot N^{o(1)}`. Valid when: Applies after each first-owned influential row is expanded in the same SAT theory with formula length E_N accounted in the parser ledger.
- same_model_upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QEeq}(\pi)+O(E_\pi N)`. Valid when: Requires the parser line induction to expose every unquarantined FormulaEval influence before it affects the final LB_N line.
- subthreshold_falsifier: `\Gamma_{QEeq}(\pi)+N^{\rho+o(1)}+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Applies when the proof line LB_N claims the same nonuniform SIZE threshold and all simulation terms are measured on identical input lengths.

## Attempted Derivation

- Define verifier-visible RowSetEqualityWitness_N records at a QE exit: owner exit, current exit, enumerator-local row names, row-index equality proof, occurrence-neighborhood equality proof, and first-owner token.
- Order exits by first external dependency; maintain invariant I_t that every unquarantined line before t is determined by charged base proof bits, visible enumerator rows, and first-owned row expansions.
- Base and non-FormulaEval steps inherit Gamma_bEF(pi) from the restricted Psys_bEF^- parser theorem.
- FormulaEval steps inside sealed QE blocks do not affect I_t until their exit; delayed support is legal only while all external dependencies are dominated by that exit.
- At an exit, run the visible enumerator. For each row, either attach a valid equality witness to a prior owner or create a new owner and pay its expansion. Charge witness verification to W_N and new expansions to X_N^{own}.
- If a line uses deduplication without a valid witness, choose the first such exit. Minimality fixes all prior transcript values. Toggle an unread enable or private row occurrence to obtain two surface completions with identical read bits but different FormulaEval influence; this is the finite falsifier.
- After all exits are processed, hardwire the proof transcript, generator G_N, and charged row expansions to build the same-theory circuit for H_N^SAT, giving the stated SIZE upper bound.
- Compare the upper bound with the LB_N(1+epsilon) threshold. If it is subthreshold, the transcript cannot be a valid proof of that finite lower-bound line.

Blocking gap: RowSetEqualityWitness_N is formal at the interface level but still needs bit-field instantiation for projected-dDNNF and ROBDD examples; full semantic SAT equality remains blocked at RealSATInfluenceRealizer_N.

## Falsifiers

- Unwitnessed semantic row-set deduplication: claimed shared rows reduce Gamma without a prefix-visible syntactic equality witness.
- Post-hoc support explanation: a row set discovered after first external dependency violates prefix causality and triggers the first-hidden-influence falsifier.
- SAT-truth branch pruning: row inclusion depends on real satisfiability rather than proof-visible occurrence syntax, so it is quarantined unless RealSATInfluenceRealizer_N is supplied.
- Advice-selected hard or influential rows: a nonuniform selector may identify hard rows but is invalid for the target-preserving parser simulation.
- Membership-only selector with no output-sensitive enumerator: it pays full scan charge or becomes a semantic-oracle escape.
- Equality witness omits occurrence neighborhoods: row indices may agree while formula occurrences differ, enabling an unread-bit countermodel.
- Dense natural-property repair: making the carrier large and polynomial-time decidable while excluding small circuits would trigger the natural-property obstruction rather than validate this sparse proof transcript route.

## Learning

Cycle 135 turns the last row-sharing ambiguity into a coverage invariant: equality compression is valid exactly for rows covered by prefix-visible syntactic witnesses; uncovered rows are sum-charged, and uncharged uncovered influence gives a finite private-row falsifier. The q-trichotomy survives with K_idx counted after first-owner compression. This is route-level paper progress, not progress on P vs NP itself.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for semantic dedup and as a calibration case for the QEeq theorem packet.`
- Rationale: The current route no longer needs another abstract TransparentRowSupport_N restatement; it needs a concrete test showing when equality compression preserves the target circuit model and when it leaks hidden semantic support.
- Situation seed: Two quarantined projected-dDNNF FormulaEval blocks compute supports R_A and R_B for the same H_N^SAT XOR row family. The proof claims R_B reuses R_A, but some projected witnesses are SAT-truth-pruned and not listed before the B-exit.
- Varied variable: lambda, the fraction of the claimed overlap R_A cap R_B covered by prefix-visible RowSetEqualityWitness_N certificates.
- Held-fixed controls: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)} and generator overhead N^{rho+o(1)}., The base Psys_bEF^- parser ledger Gamma_bEF(pi) and same-theory row expansion model., QE exits dominate all external dependencies and no advice bits or nonuniform row selectors are allowed., The target LB_N(1+epsilon) is interpreted in unrestricted nonuniform SIZE on the same input length N.
- Expected observation: When lambda=1, first-owner compression gives Gamma_QEeq. When lambda<1, the unwitnessed part must be sum-charged; if the transcript still deduplicates it, an unread projected witness or enable bit yields a private-row falsifier. The support-density threshold then follows from the first-owned rows only.
- Transfer certificate needed: A prefix-visible RowSetEqualityWitness_N verifier for projected row equality, including row-index equality, occurrence-neighborhood equality, witness-fiber handling, and first-owner charge tokens, before the intuition may enter the proof ledger.

## Next Experiment

Instantiate RowSetEqualityWitness_N for one projected-dDNNF FormulaEval exit: list owner/current node ids, projection-witness fiber certificates, row-index bijection, occurrence-neighborhood equality checks, first-owner token, and verification cost W_N; then rerun the Gamma_QEeq induction and the lambda<1 private-row falsifier on that concrete example.
