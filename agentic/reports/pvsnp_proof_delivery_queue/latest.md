<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# P vs NP Proof Delivery Queue

- Status: `pvsnp_proof_delivery_queue_ready`
- Target: `p-vs-np-target`
- Top item: `pvsnp.paper.bit-explicit-parser-formulaeval-boundary`
- Source draft: `/Users/afreitas/Downloads/parity_magnification_full_row_barrier (1).tex`

## Extracted Proof Assets

- **proved_in_draft_needs_formal_audit**: Separates positive target-query exponent debt from the beta-zero all-polynomial-exponent transfer needed for SAT not in P/poly.
  Source: Draft sections 2-3; Proposition 'Exponent-window lemma', Lemma 'Batched substitution', Theorem 'Beta-zero parity transfer', Corollary 'Conditional magnification'
- **proved_in_draft_needs_formal_audit**: Turns sparse exceptional rows into cheap equality patches, giving the residual robustness threshold for any source lower bound.
  Source: Draft section 4; Lemma 'Equality patching' and Corollary 'Residual threshold'
- **proved_in_draft_needs_barrier_scope_audit**: Shows dense truth-table-constructive functional certificates become natural properties in the matched-length regime.
  Source: Draft section 5; Theorem 'Naturalization of functional certificates' and Corollary 'Conditional natural-proofs obstruction'
- **proved_in_draft_needs_parser_boundary**: Classifies occurrence-relativizing certificates by forcing complete parity rows and paying Omega(M_n s_n/n) occurrence access.
  Source: Draft section 6; Theorem 'Row-forcing theorem', Corollary 'Full-row barrier for parity', Corollary 'Oracle-query lower bound'
- **proved_in_draft_or_conditional_needs_handoff**: Supplies proof-system, diagnostic upper-bound, and one-sided variants that can become paper modules once assumptions are explicit.
  Source: Draft section 8 and appendix; Proposition 'Parser-to-query consequence', Proposition 'Approximate affine-incidence sketch', Proposition 'One-sided forcing'

## Extracted Open Directions

- **Draft section 7; Open Problem 'Formula-semantic extraction'**
  For a concrete strong proof system formalizing lower bounds for H_n^SAT, prove functional extraction, occurrence-relativizing transcript extraction, or a precise nonrelativizing SAT-semantic obstruction.
- **Draft discussion; paragraph 'An explicit hard generator'**
  Construct a label-independent batched generator with q,rho < 1+epsilon and prove the SAT parity carrier lower bound above n^{1+epsilon}.
- **Draft discussion; paragraph 'A strong-system instantiation'**
  Choose a concrete proof formalism, specify accessible SAT facts, and decide whether short proofs admit the parser-to-query property.
- **Draft discussion; paragraph 'Aggregator design'**
  Find aggregators with a better tradeoff between beta-zero transfer cost, certificate complexity, proof locality, and algebraic structure.
- **Draft discussion plus appendix 'Incidence sketches as upper-bound falsifiers'**
  Turn low-rank or sparse incidence diagnostics into either explicit falsifiers or a nonrelativizing normal-form theorem strong enough to support lower bounds.

## Queue Policy

- Priority: Items extracted from the parity magnification draft's open problems and proofs outrank broad exploration until discharged, blocked at a named lemma, or demoted by countermodel.
- Promotion: A queue item completes only by emitting a proof packet and passing inference-quality/proof-quality gates.
- Anti-loop: Do not add another broad marathon cycle while the top formula-semantic extraction task has no proof attempt, countermodel, or named semantic-escape disposition.

## Highest-Priority Proof Items

### 1. Prove the TransparentRowSupport_N theorem pair and stop selector-case accumulation

- Queue ID: `pvsnp.paper.bit-explicit-parser-formulaeval-boundary`
- Priority score: `9999`
- Proof status: `cycle_0107_consolidation_next_move`
- Source anchor: Cycles 103-107 plus result-refinement packet transparent_row_support_packet.
- Next analysis: Proof-delivery task sharpened from cycles 103-107: stop adding isolated selector classes and consolidate interval-union, scan, ROBDD, guarded-dDNNF, projected-dDNNF, and influence-complete FormulaEval cases under one TransparentRowSupport_N abstraction. Prove the positive Gamma-extension theorem for transparent row support, prove the private-row/unread-enable-bit countermodel theorem for hidden semantic support, and state RealSATInfluenceRealizer_N as the exact remaining escape rather than a vague semantic gap.
- Theorem goal: TransparentRowSupport_N theorem pair: if a Psys_sym FormulaEval mechanism has visible selector code, advice-free enumeration or full-scan charge, influence closure, same-theory occurrence expansion, and no hidden support advice, then Gamma_trans(pi)=Gamma_bEF(pi)+U_N+X_N gives the parser-to-circuit falsifier N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)} for LB_N(1+epsilon). If any visibility, extensionality, or influence-closure condition fails, construct the private-row/unread-enable-bit countermodel to surface occurrence completion.
- Source object: Cycles 103-107 FormulaEval selector packets over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, polylog formula length, bit-explicit Psys_bEF parser costs, and selector cases including interval unions, full scans, ROBDD, guarded dDNNF, projected dDNNF, and influence-complete extension rules.
- Target object: A paper-core theorem/countermodel pair replacing the selector zoo: one transparent-support theorem, one hidden-support countermodel theorem, examples as corollaries, and RealSATInfluenceRealizer_N as an open problem.
- Paper handoff: Make this the next paper-critical theorem/countermodel target: if it only adds selector examples, it is looping; if it proves TransparentRowSupport_N or the hidden-support countermodel, it moves toward a claimable scoped note.

Proof outputs:
- formal definition of TransparentRowSupport_N with visible selector code, row enumeration/full scan, influence closure, row expansion, same-theory parser, and no-hidden-advice clauses
- positive theorem deriving Gamma_trans(pi)=Gamma_bEF(pi)+U_N+X_N and the subthreshold parser-to-circuit falsifier
- countermodel theorem using a private row or unread enable bit when support visibility, selector extensionality, or influence closure fails
- corollary table showing interval-union, scan, ROBDD, guarded-dDNNF, projected-dDNNF, and influence-complete extension rules as examples, not new main routes
- explicit open-problem statement for RealSATInfluenceRealizer_N and AC0 output-sensitive enumeration
- support-density q-trichotomy lemma for |K_idx(pi)|/M_N >= N^{epsilon-q-o(1)} as a corollary of the Gamma theorem
- live pvsnp_inference_quality packet
- paper-ready theorem/countermodel text with non-claims and no generic barrier restatement

Success criteria:
- TransparentRowSupport_N is formal enough that an independent reader can decide whether a FormulaEval rule satisfies it.
- Gamma_trans(pi) is derived rather than asserted, and the falsifier inequality states rho, q, epsilon, U_N, X_N, eta, tau, E_N, and all o(1) regimes.
- The private-row/unread-enable-bit countermodel is stated as a theorem with hypotheses, not as a metaphor.
- Selector cases are reorganized into examples/corollaries; no new selector family is promoted as a separate main contribution.
- The output advances a paper-level subgoal: a clean theorem pair and open-problem boundary, not another restatement of the obstruction ladder.

Demotion criteria:
- Demote if the work adds another selector class without changing the TransparentRowSupport_N definition, theorem, or countermodel.
- Demote if Gamma_trans(pi), K_idx(pi), U_N, X_N, or the transcript upper bound is named without a derivation.
- Demote if semantic FormulaEval is described as generic power rather than handled by RealSATInfluenceRealizer_N or the private-row countermodel.
- Demote if the branch broadens into MCSP/MKtP, natural-proofs folklore, or generic barriers before the theorem pair is written.

Required skills:
- `lemma-chain-proof-builder`
- `proof-delivery-workflow-orchestrator`
- `proof-gap-countermodel-splitter`
- `proof-obligation-formalizer`
- `proof-quality-gatekeeper`
- `pvsnp-barrier-specificity-reviewer`
- `pvsnp-conceptual-pressure-localizer`
- `pvsnp-forcedrows-proof-workflow`
- `pvsnp-impossibility-theorem-forger`
- `pvsnp-inference-quality-controller`
- `pvsnp-negative-tactic-selector`
- `pvsnp-pressure-bridge-forger`
- `pvsnp-proof-complexity-transfer-reviewer`
- `pvsnp-proof-derivation-builder`
- `pvsnp-qualitative-complexity-reasoner`
- `pvsnp-quantifier-uniformity-reviewer`
- `pvsnp-reduction-consistency-reviewer`
- `pvsnp-symbolic-complexity-auditor`

### 2. Write the L120.1 least-closed support proof-audit packet

- Queue ID: `pvsnp.paper.l1201-least-closed-support-proof-audit`
- Priority score: `9998`
- Proof status: `cycle_0120_next_missing_proof_audit`
- Source anchor: Cycle 120; discovery marathon latest report lines for L120.1, K_dag(pi), Gamma_dag, projected-dDNNF, and unread-enable-bit counterexample.
- Next analysis: Turn cycle 120's least prefix-closed reachable FormulaEval support cone into a referee-checkable proof packet. The task is to define the fixed-point computation of K_dag(pi), give verifier-visible dependency-closure pseudocode, prove the Gamma_dag line-induction invariant, and test the theorem on one projected-dDNNF FormulaEval example plus one unread-enable-bit counterexample.
- Theorem goal: LeastClosedTransparentSupport_N / L120.1: for a Psys_sym^dag proof pi whose FormulaEval lines expose parent pointers and support certificates, the least prefix-closed reachable cone K_dag(pi) from the final LB_N line is the minimal charged object needed for the parser-to-circuit falsifier N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N)<N^{1+epsilon-o(1)}.
- Source object: Cycle 120 theorem claims over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), Psys_sym^dag FormulaEval lines, dependency edges from later symbolic uses to earlier row supports, and the cost ledger Gamma_dag(pi)=Gamma_bEF(pi)+U(K_dag(pi))+X(K_dag(pi)).
- Target object: A self-contained proof-audit packet that an independent reader can run mentally or mechanically: input pi,N; compute K_dag(pi); either certify prefix-closed support and Gamma_dag, or return the first hidden reachable row with its private-row/unread-enable-bit countermodel.
- Paper handoff: Use as the immediate proof-audit packet for cycle 120 and as the concrete next theorem module before any new marathon exploration.

Proof outputs:
- formal definition of the dependency graph, reachable final cone, and least fixed point K_dag(pi)
- pseudocode for the verifier-visible closure computation with termination and monotonicity proof
- proof of Gamma_dag(pi)=Gamma_bEF(pi)+U(K_dag(pi))+X(K_dag(pi)) by prefix line induction
- same-model upper-bound falsifier inequality including rho, epsilon, q, E_pi, and all o(1) regimes
- worked projected-dDNNF FormulaEval example showing how K_dag, U, X, and Gamma_dag are computed
- worked unread-enable-bit counterexample returning the first hidden reachable row
- live pvsnp_inference_quality packet for L120.1

Success criteria:
- The fixed-point algorithm for K_dag(pi) is explicit enough to implement or audit line by line.
- Gamma_dag is derived from the closure invariant, not asserted by analogy with Gamma_trans.
- The projected-dDNNF example and unread-enable-bit counterexample both exercise the theorem boundary.
- The result states that it is a scoped parser/falsifier theorem and not evidence for P != NP.

Demotion criteria:
- Demote if K_dag(pi) is described informally without a computable closure algorithm.
- Demote if the proof does not distinguish reachable support from the full selector zoo.
- Demote if the examples do not compute charges or do not expose a first hidden reachable row.
- Demote if the theorem silently assumes full semantic SAT influence instead of charging it.

Required skills:
- `lemma-chain-proof-builder`
- `proof-delivery-workflow-orchestrator`
- `proof-gap-countermodel-splitter`
- `proof-obligation-formalizer`
- `proof-quality-gatekeeper`
- `pvsnp-barrier-specificity-reviewer`
- `pvsnp-conceptual-pressure-localizer`
- `pvsnp-forcedrows-proof-workflow`
- `pvsnp-impossibility-theorem-forger`
- `pvsnp-inference-quality-controller`
- `pvsnp-negative-tactic-selector`
- `pvsnp-pressure-bridge-forger`
- `pvsnp-proof-complexity-transfer-reviewer`
- `pvsnp-proof-derivation-builder`
- `pvsnp-qualitative-complexity-reasoner`
- `pvsnp-quantifier-uniformity-reviewer`
- `pvsnp-reduction-consistency-reviewer`
- `pvsnp-symbolic-complexity-auditor`

### 3. Resolve or quarantine RealSATInfluenceRealizer_N for one concrete semantic FormulaEval rule

- Queue ID: `pvsnp.paper.realsat-influence-realizer-boundary`
- Priority score: `9997`
- Proof status: `named_semantic_gap_needs_rule_level_resolution`
- Source anchor: Cycle 120 RealSATInfluenceRealizer_N boundary plus proof-delivery queue Formula-semantic extraction open problem.
- Next analysis: Attack the exact remaining full-semantic FormulaEval gap instead of naming it abstractly. Choose one concrete semantic FormulaEval rule, such as Tseitin-extension equality plus bounded self-reduction, and either produce an advice-free nonrelativizing realizer listing all influencing rows with charges, or prove a rule-specific private-row/no-realizer countermodel.
- Theorem goal: RealSATInfluenceRealizer_N boundary theorem: full semantic FormulaEval can be folded into the transparent support theorem only when proof syntax and N uniformly determine an influence-closed row set R_A, same-theory row expansions, and a charged overhead R_N before the semantic rule is used.
- Source object: Semantic FormulaEval-SAT rules over H_N^SAT generated rows where real SAT semantics, formula equality, Tseitin extensions, or self-reduction may make a proof line depend on rows not visible in a syntactic TransparentRowSupport_N certificate.
- Target object: A yes/no boundary for one named semantic rule: either a valid RealSATInfluenceRealizer_N certificate with Gamma_real=Gamma_bEF+U+X+R_N, or a finite countermodel showing why that semantic rule remains quarantined.
- Paper handoff: Use as the exact open-boundary paragraph for full semantic FormulaEval, or as a theorem if the chosen rule admits a realizer.

Proof outputs:
- selected semantic FormulaEval rule with exact bit fields, formula objects, and allowed SAT/equality facts
- definition of semantic influence Infl(A), row set R_A, realizer output format, and overhead R_N
- advice-free realizer proof, or a private-row/no-realizer theorem for the selected rule
- same-theory expansion certificates or a proof that such certificates cannot be uniformly extracted
- updated non-claims explaining that unresolved semantic FormulaEval is a model boundary, not a P vs NP barrier slogan
- live pvsnp_inference_quality packet reviewed by barrier-specificity and proof-complexity reviewers

Success criteria:
- The selected semantic rule is concrete enough that the realizer or countermodel is independently checkable.
- All influence rows are uniformly listed and charged, or the exact unchargeable semantic step is named.
- The output eliminates vague language about semantic FormulaEval and replaces it with a rule-level theorem or no-go.

Demotion criteria:
- Demote if RealSATInfluenceRealizer_N is only restated without choosing a semantic rule.
- Demote if the row set uses SAT-truth advice or hidden nonuniform row selection.
- Demote if the claimed realizer omits R_N from the Gamma ledger.
- Demote if the negative result does not identify the first semantic inference that cannot be charged.

Required skills:
- `lemma-chain-proof-builder`
- `proof-delivery-workflow-orchestrator`
- `proof-gap-countermodel-splitter`
- `proof-obligation-formalizer`
- `proof-quality-gatekeeper`
- `pvsnp-barrier-specificity-reviewer`
- `pvsnp-conceptual-pressure-localizer`
- `pvsnp-forcedrows-proof-workflow`
- `pvsnp-impossibility-theorem-forger`
- `pvsnp-inference-quality-controller`
- `pvsnp-negative-tactic-selector`
- `pvsnp-pressure-bridge-forger`
- `pvsnp-proof-complexity-transfer-reviewer`
- `pvsnp-proof-derivation-builder`
- `pvsnp-qualitative-complexity-reasoner`
- `pvsnp-quantifier-uniformity-reviewer`
- `pvsnp-reduction-consistency-reviewer`
- `pvsnp-symbolic-complexity-auditor`

### 4. Package the cycle-120 theorem/countermodel pair as a paper-ready module

- Queue ID: `pvsnp.paper.l120-theorem-countermodel-package`
- Priority score: `9996`
- Proof status: `paper_module_missing_after_cycle_0120`
- Source anchor: Cycles 116-120 and the current mathematical story in the discovery marathon report.
- Next analysis: Assemble the least-closed transparent-support theorem, hidden-support countermodel, RealSATInfluenceRealizer_N open boundary, q-trichotomy support-density corollary, and selector-example table into one coherent paper module. The package must be readable without marathon context.
- Theorem goal: Paper module: a scoped parser/falsifier contribution for FormulaEval in beta-zero parity magnification, showing exactly when transparent FormulaEval yields a same-model upper-bound falsifier and exactly where hidden semantic influence escapes the controlled interface.
- Source object: Cycles 116-120, especially L120.1 LeastClosedTransparentSupport_N, L120.2 UnreachableSupportDeletion_N, L120.3 FirstHiddenReachableUse_N, and the branch outputs that state Gamma_dag, hidden-row falsifiers, and q<epsilon/q=epsilon/q>epsilon support-density cases.
- Target object: A paper-ready theorem/countermodel section with definitions, theorem statements, proof sketches, examples, non-claims, and a handoff to the broader parity magnification/full-row barrier draft.
- Paper handoff: Use as the publishable scoped note/module if the full semantic realizer remains open.

Proof outputs:
- definition ledger for H_N^SAT, Psys_sym^dag, K_dag(pi), Gamma_bEF, U(K), X(K), E_pi, and LB_N(1+epsilon)
- theorem statement and proof sketch for the least-closed transparent support upper-bound falsifier
- countermodel theorem for first hidden reachable support using private rows or unread enable bits
- RealSATInfluenceRealizer_N open-boundary box with exact input, output, overhead, and non-claims
- q-trichotomy support-density corollary for q<epsilon, q=epsilon, and q>epsilon
- example table demoting interval-union, scan, ROBDD, guarded-dDNNF, projected-dDNNF, and influence-complete rules to corollaries/examples
- paper-ready prose with no pipeline jargon and no claim of P != NP progress

Success criteria:
- The module is understandable as a standalone paper section.
- The positive theorem, negative countermodel, and semantic open boundary are separated cleanly.
- Examples are corollaries/examples only; no new selector zoo is created.
- The paper handoff preserves the scoped claim and does not oversell P vs NP progress.

Demotion criteria:
- Demote if the package is a report summary rather than theorem/countermodel text.
- Demote if it depends on marathon-specific workflow language.
- Demote if it blurs transparent extensional FormulaEval with full semantic SAT FormulaEval.
- Demote if it omits the q-trichotomy or the non-claims.

Required skills:
- `lemma-chain-proof-builder`
- `proof-delivery-workflow-orchestrator`
- `proof-gap-countermodel-splitter`
- `proof-obligation-formalizer`
- `proof-quality-gatekeeper`
- `pvsnp-barrier-specificity-reviewer`
- `pvsnp-proof-complexity-transfer-reviewer`
- `pvsnp-quantifier-uniformity-reviewer`
- `pvsnp-reduction-consistency-reviewer`
- `pvsnp-symbolic-complexity-auditor`

### 5. Close the L120 inference-quality and marker gaps before promotion

- Queue ID: `pvsnp.paper.l120-inference-quality-gate-closure`
- Priority score: `9995`
- Proof status: `promotion_gate_missing_after_cycle_0120`
- Source anchor: P vs NP inference-quality report and discovery marathon research-quality marker warning after cycle 120.
- Next analysis: Prepare the promotion gate for the L120 theorem work. Emit a fresh pvsnp_inference_quality packet for the least-closed support theorem, run the reviewer stack, and repair any source/target/model/validity marker gaps before treating the theorem package as a paper result.
- Theorem goal: Validation theorem for promotion readiness: every L120 claim has explicit source object, target object, controlled interface, target-preserving condition, reduction direction, quantifiers, advice discipline, barrier scope, and proof-complexity transfer status.
- Source object: The live L120 claims, the 93 active inference-quality packets, and the discovery report warning that not all source/target/same-theory/validity markers are globally present.
- Target object: A repaired inference-quality packet and gate report that says exactly which L120 claims are promotable, which are conditional, and which remain blocked at RealSATInfluenceRealizer_N.
- Paper handoff: Use as the final gate before promoting the L120 module into the paper draft or queueing another proof attempt.

Proof outputs:
- new pvsnp_inference_quality packet for L120.1 and the L120 theorem/countermodel package
- reviewer findings from reduction consistency, quantifier uniformity, barrier specificity, proof-complexity transfer, and meta-complexity carrier checks
- marker-gap repair table for source object, target object, controlled interface, target-preserving condition, and validity regimes
- promotion verdict separating proved scoped theorem, conditional theorem, open boundary, and non-claims
- validator output from validate_pvsnp_inference_quality.py and validate_pvsnp_proof_delivery_queue.py

Success criteria:
- The L120 theorem package has a live IQ packet that passes validation.
- No source/target/model/validity marker is implicit.
- Reviewer objections are either discharged, converted to named obligations, or marked as demotion blockers.
- The promotion verdict is conservative and explicitly says what is not proved.

Demotion criteria:
- Demote if the IQ packet claims P vs NP progress rather than a scoped parser/falsifier result.
- Demote if source and target models are not the same nonuniform SIZE model.
- Demote if RealSATInfluenceRealizer_N is treated as solved without a rule-level proof.
- Demote if validation fails and the failure is not converted into a concrete repair item.

Required skills:
- `proof-obligation-formalizer`
- `proof-quality-gatekeeper`
- `pvsnp-barrier-specificity-reviewer`
- `pvsnp-inference-quality-controller`
- `pvsnp-meta-complexity-carrier-reviewer`
- `pvsnp-proof-complexity-transfer-reviewer`
- `pvsnp-quantifier-uniformity-reviewer`
- `pvsnp-reduction-consistency-reviewer`

### 6. Audit and package the draft's proved beta-zero/full-row barrier theorem chain

- Queue ID: `pvsnp.paper.full-row-barrier-proof-audit`
- Priority score: `9994`
- Proof status: `proved_in_draft_needs_formal_audit`
- Source anchor: Draft sections 2-8 plus appendices: all theorem/proposition/corollary proof environments.
- Next analysis: Proof-audit task extracted from the draft theorem stack: rebuild the exponent-window, batched substitution, beta-zero transfer, equality patching, naturalization, row-forcing, parity full-row, parser-to-query, incidence-sketch, and one-sided forcing proofs as a dependency-checked proof packet.
- Theorem goal: Verified theorem-chain packet: beta-zero transfers remove exponent debt; functional certificates naturalize; occurrence-relativizing parity certificates pay Omega(M_n s_n/n).
- Source object: The draft's proposition/lemma/theorem environments and their dependency graph.
- Target object: A paper-ready proof packet with explicit hypotheses, quantifiers, non-claims, and theorem dependencies.
- Paper handoff: Use as the proof backbone of the parity magnification/full-row barrier paper.

Proof outputs:
- dependency graph of all proved draft statements
- definition ledger for H_n^SAT, H_n^y, F_{n,A}^z, Phi_n, C_b(A_M), Q_pi, R_b(Q,alpha), and p_x
- formal proof-obligation list for every theorem/proposition/corollary
- gap report separating proved, conditional, and open components
- paper-ready proof summary with no pipeline jargon

Success criteria:
- Every proved draft statement has assumptions, conclusion, proof dependencies, and barrier scope recorded.
- No step silently upgrades occurrence-label statements to formula-label or full proof-system statements.
- The theorem chain is ready for paper insertion or referee-style proof checking.

Demotion criteria:
- Demote if any proof uses an unstated uniformity, density, constructivity, or formula-realizability assumption.
- Demote if theorem dependencies are circular or if the draft's non-claims are not preserved.

Required skills:
- `lemma-chain-proof-builder`
- `proof-delivery-workflow-orchestrator`
- `proof-obligation-formalizer`
- `proof-quality-gatekeeper`
- `pvsnp-barrier-specificity-reviewer`
- `pvsnp-proof-complexity-transfer-reviewer`
- `pvsnp-quantifier-uniformity-reviewer`
- `pvsnp-reduction-consistency-reviewer`
- `pvsnp-symbolic-complexity-auditor`

### 7. Attack the explicit hard-generator/source-lower-bound open problem

- Queue ID: `pvsnp.paper.explicit-hard-generator-open-problem`
- Priority score: `9993`
- Proof status: `central_open_problem_from_draft`
- Source anchor: Draft discussion paragraph 'An explicit hard generator'.
- Next analysis: Open-problem task extracted from the draft discussion: construct or rule out a label-independent batched generator with polylogarithmic SAT instances, M_n=n^{q+o(1)}, generator size n^{rho+o(1)}, q,rho<1+epsilon, and a provable general-circuit lower bound Ckt(H_n^SAT)>n^{1+epsilon-o(1)}.
- Theorem goal: Source-lower-bound theorem or impossibility diagnosis for a concrete beta-zero SAT parity carrier.
- Source object: Candidate batched generator G_n and parity carrier H_n^SAT from polylog-length SAT formulas.
- Target object: A source lower bound strong enough to activate the beta-zero magnification corollary, or a precise obstruction explaining why the candidate collapses.
- Paper handoff: Promote only if it delivers an explicit generator theorem, falsifier, or principled obstruction.

Proof outputs:
- candidate generator specification with q, rho, d, and formula universe U_n
- incidence sketch/rank/falsifier audit
- attempted lower-bound proof obligations
- blocked-lemma or impossibility packet if lower-bound proof fails
- paper paragraph stating whether this supplies or fails to supply the central source problem

Success criteria:
- A concrete generator is named with verified beta-zero transfer parameters.
- The branch produces either a real lower-bound lemma, a reproducible upper-bound falsifier, or a sharp reason it cannot be the source problem.
- Any claimed progress distinguishes scalar circuit lower bounds from incidence-linear diagnostics.

Demotion criteria:
- Demote if no explicit generator is specified.
- Demote if the evidence is only high rank, randomness intuition, or incidence complexity without a general-circuit lower-bound bridge.
- Demote if q or rho fails the stated threshold needed by the transfer theorem.

Required skills:
- `lemma-chain-proof-builder`
- `proof-delivery-workflow-orchestrator`
- `proof-gap-countermodel-splitter`
- `proof-quality-gatekeeper`
- `pvsnp-barrier-specificity-reviewer`
- `pvsnp-conceptual-pressure-localizer`
- `pvsnp-forcedrows-proof-workflow`
- `pvsnp-impossibility-theorem-forger`
- `pvsnp-qualitative-complexity-reasoner`
- `pvsnp-symbolic-complexity-auditor`

### 8. Instantiate the parser-to-query consequence for a concrete strong proof system

- Queue ID: `pvsnp.paper.strong-system-parser-instantiation`
- Priority score: `9992`
- Proof status: `open_problem_with_conditional_proposition`
- Source anchor: Draft discussion paragraph 'A strong-system instantiation' and Proposition 'Parser-to-query consequence'.
- Next analysis: Open-problem/proof task extracted from the draft's strong-system paragraph and Proposition parser-to-query: choose a concrete proof formalism for lower-bound statements, define exactly which formula equality and SAT semantic facts it can access, and prove or refute the parser property that maps accepted proofs pi to occurrence transcripts Q_pi.
- Theorem goal: Concrete parser-to-query instantiation theorem or counterexample for a named proof system.
- Source object: Named proof formalism, proof pi, verifier/parser, and allowed SAT/equality axioms.
- Target object: A proof-system-specific theorem linking proof length/access to Omega(M_n s_n/n), or an escape principle that blocks the link.
- Paper handoff: Use to turn the conditional parser-to-query proposition into a named proof-system result or a precise open boundary.

Proof outputs:
- proof-system syntax and verifier model
- allowed SAT facts and formula-equality principles
- parser pi -> (Q_pi, alpha_pi) definition or countermodel
- quantitative p(T,n) exposure bound
- paper-ready proof-system consequence or limitation

Success criteria:
- The selected proof system and its SAT access are explicit enough for independent checking.
- The parser property is proved with a quantitative p(T,n), or a precise semantic escape is isolated.
- The output is not a generic 'strong systems are hard' statement; it names the exact proof rule that matters.

Demotion criteria:
- Demote if the proof system remains unnamed or if its SAT facts are unspecified.
- Demote if the parser theorem assumes occurrence locality instead of deriving it.
- Demote if a negative answer does not identify the formula-semantic principle defeating occurrence-wise completion.

Required skills:
- `lemma-chain-proof-builder`
- `proof-delivery-workflow-orchestrator`
- `proof-gap-countermodel-splitter`
- `proof-obligation-formalizer`
- `proof-quality-gatekeeper`
- `pvsnp-forcedrows-proof-workflow`
- `pvsnp-inference-quality-controller`
- `pvsnp-negative-tactic-selector`
- `pvsnp-proof-complexity-transfer-reviewer`
- `pvsnp-quantifier-uniformity-reviewer`
- `pvsnp-reduction-consistency-reviewer`

### 9. Use incidence sketches as falsifiers and define the missing normal-form bridge

- Queue ID: `pvsnp.paper.incidence-falsifier-normal-form`
- Priority score: `9991`
- Proof status: `proved_diagnostic_plus_open_bridge`
- Source anchor: Draft appendix 'Incidence sketches as upper-bound falsifiers' and discussion paragraph 'From diagnostics to lower bounds'.
- Next analysis: Proof/diagnostic task extracted from the appendix and discussion: for candidate generators, search for low-rank or sparse affine-incidence sketches p_x=sum_i a_i(x)b_i off a small exceptional set, and state the exact nonrelativizing normal-form theorem that would be needed to turn absence of such sketches into lower-bound evidence.
- Theorem goal: Incidence-falsifier theorem plus normal-form open problem for translating diagnostics into lower bounds.
- Source object: Generated formula universe U_n, incidence vectors p_x in F^{U_n}, coefficient functions a_i, sketch vectors b_i, and exception set B_n.
- Target object: A reproducible upper-bound falsifier or a clearly scoped normal-form theorem needed before incidence diagnostics can support source lower bounds.
- Paper handoff: Add as the generator-screening and upper-bound-falsifier module in the paper.

Proof outputs:
- incidence representation and sketch-search protocol
- upper-bound theorem application Ckt(H_n^y) <= O(A_n+K+E_n n)
- candidate-generator falsifier report
- normal-form theorem statement separating scalar circuits from incidence compression
- paper-ready diagnostic subsection

Success criteria:
- Every candidate generator is checked for the appendix's explicit upper-bound mechanism before promotion.
- The output never treats absence of a sketch as a lower bound.
- The normal-form bridge is stated as a theorem obligation with assumptions strong enough to imply scalar circuit hardness.

Demotion criteria:
- Demote if the branch uses incidence rank as a lower bound without a scalar-circuit bridge.
- Demote if K, A_n, E_n, or exceptional-row patch cost are not computed or bounded.
- Demote if the diagnostic does not feed either a falsifier or a specific normal-form theorem.

Required skills:
- `lemma-chain-proof-builder`
- `proof-gap-countermodel-splitter`
- `proof-obligation-formalizer`
- `proof-quality-gatekeeper`
- `pvsnp-barrier-specificity-reviewer`
- `pvsnp-meta-complexity-carrier-reviewer`
- `pvsnp-reduction-consistency-reviewer`
- `pvsnp-symbolic-complexity-auditor`

### 10. Search aggregator designs beyond parity with explicit transfer and certificate tradeoffs

- Queue ID: `pvsnp.paper.aggregator-design-open-problem`
- Priority score: `9990`
- Proof status: `open_direction_from_draft`
- Source anchor: Draft discussion paragraph 'Aggregator design' plus appendix 'A one-sided version of row forcing'.
- Next analysis: Open-direction task extracted from the draft: compare parity with alternative aggregators by computing transfer cost, C_0(A_M), C_1(A_M), one-sided certificate behavior, algebraic structure, and whether the aggregator preserves beta-zero all-exponent SAT transfer without reopening easy selector/separator certificates.
- Theorem goal: Aggregator tradeoff theorem or no-go table identifying which aggregators preserve the desired certificate debt.
- Source object: Candidate row aggregator family A_M and batched SAT labels y(G_{n,j}(x)).
- Target object: A ranked set of aggregator candidates with proof-relevant certificate-complexity and transfer-cost guarantees.
- Paper handoff: Use to justify parity's role or to add an aggregator-comparison extension section.

Proof outputs:
- aggregator candidate list
- computed C_0(A_M), C_1(A_M), circuit size, and one-sided behavior
- beta-zero transfer audit for each aggregator
- qualitative explanation of proof locality versus algebraic exploitable structure
- paper-ready aggregator-design paragraph or appendix

Success criteria:
- Parity remains justified or a better aggregator is identified by explicit C_b(A_M) and transfer calculations.
- Any proposed aggregator has proof-locality consequences stated as theorem obligations, not analogies.
- The output explains whether it strengthens, weakens, or complements the full-row barrier.

Demotion criteria:
- Demote if aggregator comparison does not compute C_0 and C_1.
- Demote if the aggregator creates a cheap one-sided certificate that defeats the intended full-row burden.
- Demote if transfer cost reintroduces positive beta exponent debt.

Required skills:
- `proof-obligation-formalizer`
- `proof-quality-gatekeeper`
- `pvsnp-barrier-specificity-reviewer`
- `pvsnp-conceptual-pressure-localizer`
- `pvsnp-qualitative-complexity-reasoner`
- `pvsnp-symbolic-complexity-auditor`

### 11. Deliver the occurrence-local row-forcing theorem as a standalone scoped contribution

- Queue ID: `pvsnp.paper.occurrence-row-forcing-proposition-delivery`
- Priority score: `9989`
- Proof status: `proved_in_draft_needs_standalone_packaging`
- Source anchor: Draft section 'Occurrence-local certificates and the full-row barrier' plus appendix 'A one-sided version of row forcing'.
- Next analysis: Proof-delivery task extracted from the proved row-forcing section: package the occurrence-completion theorem, parity full-row corollary, adaptive verifier corollary, and one-sided variant as a standalone barrier theorem with exact scope.
- Theorem goal: Standalone occurrence-local certificate-debt theorem for beta-zero parity carriers.
- Source object: Completion-sound partial transcript (Q,alpha), forced rows R_b(Q,alpha), aggregator certificate complexity C_b(A_M), and patch circuits.
- Target object: A scoped publishable theorem: occurrence-relativizing lower-bound certificates must pay full-row cost for parity.
- Paper handoff: Promote as the scoped standalone contribution if the broader formula-semantic extraction remains open.

Proof outputs:
- formal theorem and corollaries with all constants/quantifiers explicit
- row-spoofing completion construction
- equality-patching dependency proof
- adaptive verifier interpretation
- paper-ready theorem statement and proof

Success criteria:
- The theorem is independently understandable without the rest of the P vs NP discovery machinery.
- The proof states exactly why formula-semantic SAT proofs are outside scope.
- The theorem can be cited as the paper's local-certificate barrier contribution.

Demotion criteria:
- Demote if the proof assumes formula-realizability or SAT semantics.
- Demote if the sparse patch construction does not produce a circuit below the claimed threshold.
- Demote if the theorem cannot state its non-claims cleanly.

Required skills:
- `lemma-chain-proof-builder`
- `proof-obligation-formalizer`
- `proof-quality-gatekeeper`
- `pvsnp-barrier-specificity-reviewer`
- `pvsnp-forcedrows-proof-workflow`
- `pvsnp-quantifier-uniformity-reviewer`
- `pvsnp-reduction-consistency-reviewer`
