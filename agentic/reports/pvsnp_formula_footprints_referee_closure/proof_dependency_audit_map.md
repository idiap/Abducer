<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Proof Dependency Audit Map

- Status: `integrated_in_revised_tex`
- TeX section: `Proof dependency and audit map`
- TeX label: `sec:audit`
- Table label: `tab:proof-dependencies`
- Criteria affected: `C8`, `C9`, `C11`

## Purpose

The audit map makes the theorem package referee-auditable.  It records, inside the paper, which results depend on elementary completion arguments, which depend on sorting-network lookup, which use circuit-counting or Chernoff bounds, and which claims remain outside the proved dependency graph.

## Dependency Spine

1. Equality patching gives sparse-row circuit upper bounds.
2. Batched static dictionary gives formula-label completion upper bounds.
3. Sparse formula-defect upper bound feeds the formula-footprint barrier.
4. The formula-footprint barrier feeds nondeterministic decision-tree, near-threshold, randomized accepting-union, displayed-atom, and extension-normalizer consequences.
5. Row-forcing, quotient-distance, semantic-relation support, acyclic OR-tree frontier support, quotiented OR-DAG frontier support, exposed acyclic Boolean frontier support, visible adaptive frontier support, and visible adaptive branching-program frontier support are separate interface variants of the same completion-soundness obstruction.
6. Hidden adaptive transcript insufficiency is the matching boundary: a small reported transcript without certified controller/path completeness does not determine a sound support budget.
7. Controller-complete adaptive audit is the positive bridge: a hidden adaptive transcript becomes sound only when the proof object exposes the acyclic controller, replay path, and local equivalence certificate for the completion cylinder.
8. Provenance-typed LRAT is a proof-system bridge: trusted variable roles, block-local support provenance, and compatible witnesses supply the support audit required by the LRAT trace normalizer.
9. Namespace-typed LRAT antecedent closure is a lighter proof-system bridge: a trusted formula-label namespace plus the LRAT antecedent closure of the empty clause supplies the used label support for witnessed auxiliary clauses.
10. Strict-prefix Qrep replay is a proof-system bridge: quotient compression counts only when representatives replay from already charged same-theory certificate forests.
11. Trace-complete DPLL and antecedent-complete CDCL are recognizable proof-system bridges: DPLL logs count only with a complete controller/path/witness audit, and learned clauses count only with acyclic antecedent DAGs down to audited local support.
12. CDCL antecedent-erasure is the matching boundary: once learned-clause antecedents and roles are erased, the extractor must add equivalent provenance or a semantic invariant, pay conservative support, or become unsound on a same-skeleton lift.
13. RUP-complete CDCL is the positive non-plain bridge: checker-visible RUP propagation traces over a known live database count when formula-label support is parsed and retained across deleted-clause consequences.
14. Canonical-namespace RUP-CDCL is the checkable manifest bridge: a reserved label interval and live-database log make the RUP support parser deterministic for the carrier-specific route.
15. Carrier-independent audit upgrade is the top-paper proof-system target: if a stronger proof system computes support, support-locality evidence, and budget from the proof artifact itself without a carrier-specific manifest, the support-local transfer applies.
16. Self-auditing RUP-CDCL instantiates that target for an enriched trace format: the proof object itself carries the label decoder, live-database reconstruction, RUP witnesses, and retained support annotations.
17. Append-only self-auditing RUP-CDCL removes one annotation layer in the deletion-free case: the monotone clause-addition log replaces retained deleted-clause support records.
18. Prefix-typed append-only RUP-CDCL removes another annotation layer when formula-label variables are public proof-system syntax: the checker no longer needs a proof-internal label decoder.
19. Prefix-typed RUP support-witness necessity shows the remaining auxiliary support-locality witness is not removable by public label syntax and append-only RUP checking alone.
19. Support-audit necessity and support-erasure indistinguishability show that raw clausal unsat traces and untyped LRAT skeletons do not by themselves certify formula-label support.
20. Plain LRAT extraction trichotomy turns the raw-trace route into three cases: add provenance, pay role-agnostic support, or become unsound on a same-skeleton lift.
21. SAT transfer is conditional and uses substitution plus the certificate barriers; it does not prove the source lower bound.

## Nonclaim Boundaries

- No proof of \(P\ne NP\).
- No proof of \(\SAT\notin\Ppoly\).
- No explicit hard SAT-labeled carrier.
- No lower bound for Frege, Extended Frege, IPS, implicit proofs, algebraic systems, unrestricted extended resolution, raw unaudited or untyped LRAT/DRAT, or delayed quotient compression without charging the final slice, replay dictionary, typed provenance package, system-specific invariant, or proving a stronger support-local budget.
- No expected-query randomized lower bound.
- No hidden, cyclic, arbitrary learned-clause, or proof-system-internal SAT self-reduction completion theorem; the current semantic theorems give local relation-instance costs, eliminated-frontier certificates for OR trees and quotiented OR DAGs, exposed acyclic Boolean frontier certificate costs, visible adaptive frontier certificate costs when the whole decision tree or branching program is checker-visible, a separator showing that uncertified hidden adaptive transcripts alone are unsound, a positive controller-complete audit theorem when controller completeness and local equivalence are explicitly certified, a trace-complete DPLL instantiation when the full decision controller, replay path, and local witnesses are logged, an antecedent-complete CDCL instantiation when every used learned clause has acyclic antecedent provenance down to audited local support, and a RUP-complete CDCL instantiation when checker-visible RUP traces expose parsed formula-label support over the known live database.

## Gate Impact

C8 is now satisfied for the current theorem package: every theorem-level claim has visible dependencies, assumptions, and nonclaim boundaries in the revised TeX.  The canonical syntactic-cone normalizer adds an automatic graph-reachability dependency rather than a new independent result, the final backward-slice corollary repackages that support as a visible proof-object budget, the slice-explicit ER corollary records the proof-size charging form, the displayed acyclic ER corollary shows that ordinary displayed extension clauses already pay for the same boundary, the expansion-bounded compressed ER corollary turns compression into a decompression-budget tradeoff, the macro-compressed ER corollary turns ordinary macro sharing into a reuse-product tradeoff, the support-declared macro ER corollary turns sound support summaries into near-threshold support-budget lower bounds, the support-audited LRAT corollary turns checker-visible support audits into the same budget theorem, the provenance-typed LRAT corollary proves that trusted variable roles and block-local provenance supply such an audit, the namespace-typed LRAT corollary proves that a trusted formula-label namespace plus LRAT antecedent closure supplies the used support for witnessed auxiliary clauses, the strict-prefix Qrep proposition turns quotient representative reuse into a replayable support budget, the trace-complete DPLL corollary turns a fully logged DPLL decision controller with local witnesses into a controller-complete adaptive audit, the antecedent-complete CDCL corollary turns used learned clauses with acyclic antecedent DAGs into the same audited local-support budget, the CDCL antecedent-erasure trichotomy shows that provenance-free learned-clause syntax must add a real invariant, pay conservative support, or become unsound, the RUP-complete CDCL corollary shows that checker-visible propagation certificates over the live database recover the audit when formula-label support is parsed and retained, the canonical-namespace RUP-CDCL corollary shows that a deterministic label-interval manifest makes that parser checker-visible, the carrier-independent audit upgrade criterion states the exact proof-system-intrinsic extractor needed to remove that manifest dependence, the self-auditing RUP-CDCL corollary instantiates that extractor when the proof format internalizes the decoder and support audit, the append-only self-auditing RUP-CDCL corollary removes retained deleted-clause support annotations when the trace is deletion-free, the prefix-typed append-only RUP-CDCL corollary removes the proof-internal decoder when formula-label variables are public typed syntax, the prefix-typed RUP support-witness necessity proposition shows that public label typing and append-only RUP checking do not certify auxiliary support-locality by themselves, the support-audit necessity separator shows that checked clausal unsatisfiability alone does not certify completion-local support, the support-erasure separator shows that untyped trace syntax does not determine whether a variable is auxiliary or formula-label support, the plain LRAT trichotomy shows that raw trace extraction must add provenance, pay role-agnostic support, or be unsound on a same-skeleton lift, the semantic-relation support certificate shows what each local nonlinear relation instance must expose, the acyclic OR-tree frontier theorem gives an exact eliminated-frontier certificate cost, the OR-DAG frontier theorem shows that pure sharing and repeated frontier formulas do not change that exact cost after sound quotienting, the acyclic Boolean frontier theorem reduces any exposed finite acyclic semantic frontier to ordinary pointwise certificate complexity, the visible adaptive frontier theorem shows that logged transcript-path support is sound only when the full adaptive decision tree is exposed, the visible adaptive branching-program theorem shows the same for shared acyclic adaptive control when the whole branching program is exposed, the hidden adaptive transcript separator shows that transcript-only extraction is unsound without certified controller/path completeness or worst-case support, and the controller-complete adaptive audit theorem gives the matching positive support normalizer when the controller and its local equivalence certificate are paid for.  The remaining top-paper blocker is external mathematical weight: supply an intrinsic support-locality invariant, handle deletion-bearing or untyped RUP-CDCL traces, or prove an explicit SAT-family/source lower-bound theorem.
