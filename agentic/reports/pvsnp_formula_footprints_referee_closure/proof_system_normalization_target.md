<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Proof-System Normalization Target

- Status: `integrated_in_revised_tex`
- TeX subsection: `The normalization target for proof-system applications`
- TeX label: `subsec:normalization-target`
- Table label: `tab:normalization-targets`
- Criteria affected: `C5`, `C7`, `C10`, `C11`

## Purpose

This artifact records the exact bridge needed to turn the paper's certificate-complexity results into a recognizable proof-system theorem.  It does not claim such a theorem is proved.  Instead, it makes the missing theorem precise enough to be judged, pursued, or rejected.

## Required Future Theorem

A controlled local normalization theorem for a proof system must provide:

1. a lower-bound statement family \(L_n\);
2. an extractor from accepted proofs to formula labels, private occurrence rows, or equality-quotient labels;
3. a faithfulness invariant tying extracted local data to the intended carrier labeling;
4. a completion-soundness invariant over unextracted labels;
5. an overhead bound from proof length to extracted local size.

## Extraction Routes

| Output | Paper theorem applied | Required proof-system fact |
|---|---|---|
| Displayed formula atoms | Formula-footprint barrier and displayed-atom extraction | The proof exposes faithful formula labels and stays sound under arbitrary completion of unexposed formula labels. |
| Explicit resolution assumptions | Assumption-resolution theorem | A resolution refutation of an easy-completion CNF uses faithful formula-label unit assumptions, and those assumptions are explicitly listed and counted. |
| Full-assignment resolution unit core | Resolution unit-core corollary | A resolution refutation of the easy-completion CNF plus the full hard labeling uses many distinct faithful label-unit leaves of each polarity. |
| Local resolution clauses | Resolution local-clause support theorem | A resolution refutation uses faithful clauses over formula-label variables, and the distinct label support of those clauses is explicitly exposed. |
| Support-local auxiliary resolution | Support-local auxiliary resolution theorem | A resolution refutation uses auxiliary constraints that remain satisfiable under every completion preserving a fixed formula-label support. |
| Support-local extension resolution | Support-local extension-resolution theorem | A resolution refutation uses acyclic extension definitions whose inputs are formula-label variables from a fixed support, and the final extension clauses are stable under all completions preserving that support. |
| Dependency-cone extension normalizer | Dependency-cone extension normalizer theorem | An extension proof annotates every extension variable with a formula-label dependency cone, and the final contradiction has controlled cone union. |
| Canonical syntactic-cone normalizer | Canonical syntactic-cone normalizer corollary | An acyclic extension proof needs no separate cone annotations: the final support is extracted from graph reachability in the extension-definition syntax. |
| Final backward-slice lower bound | Final backward-slice lower-bound corollary | The final backward extension slice must contain near-threshold many distinct formula-label inputs of each polarity. |
| Slice-explicit ER lower bound | Slice-explicit extension-resolution lower-bound corollary | The proof-size measure charges the distinct formula-label inputs in the final backward slice. |
| Displayed acyclic ER length lower bound | Displayed acyclic ER length lower-bound corollary | Ordinary displayed literal length of \(E_C\), \(\Theta\), and the derivation charges every formula-label input in the final backward slice. |
| Expansion-bounded compressed ER transfer | Expansion-bounded compressed ER transfer corollary | A compressed proof expands to displayed acyclic ER with expansion length bounded by \(B(|\rho|)\), forcing \(B(|\rho|)\ge 2n^{a-o(1)}\). |
| Macro-compressed ER reuse tradeoff | Macro-compressed ER reuse-tradeoff corollary | A displayed skeleton, macro library, and invocation list expanding to displayed acyclic ER must satisfy \(S+rD\ge 2n^{a-o(1)}\). |
| Support-declared macro ER normalizer | Support-declared macro ER normalizer corollary | A compressed macro proof with a sound declared support \(S_\rho\) must satisfy \(|S_\rho|\ge 2n^{a-o(1)}\) near threshold, and any budget \(B(|\rho|)\) for that support must be large. |
| Support-audited LRAT trace normalizer | Support-audited LRAT trace normalizer corollary | A checked clausal trace with a sound support audit must expose near-threshold formula-label support; unaudited LRAT/DRAT still needs a separate extraction theorem. |
| Provenance-typed LRAT support audit | Provenance-typed LRAT support audit corollary | A trusted variable-role map plus block-local clause provenance and compatible witnesses supplies the sound support audit; raw untyped LRAT/DRAT remains outside the theorem. |
| Namespace-typed LRAT antecedent closure | Namespace-typed LRAT antecedent-closure normalizer | A trusted formula-label variable namespace plus the LRAT antecedent closure of the empty clause supplies the used label support for witnessed auxiliary clauses. |
| Strict-prefix Qrep replay normalizer | Strict-prefix Qrep replay normalizer | Quotient representatives must replay from same-theory certificate forests displayed and charged before first use; delayed quotient evidence is hidden support. |
| Support-audit necessity separator | Support-audit necessity separator | A checked clausal refutation can be short while every sound support audit must expose all labels fixed by the constraint package; unsat checking alone does not certify support locality. |
| Support-erasure indistinguishability separator | Support-erasure indistinguishability separator | The same untyped LRAT skeleton can have an auxiliary lift with empty formula-label support and a label lift requiring all labels; variable-role provenance is part of the support audit. |
| Plain LRAT extraction trichotomy | Plain LRAT extraction trichotomy | A raw trace extractor must add provenance, pay role-agnostic support, or be unsound on a same-skeleton semantic lift; plain LRAT/DRAT is not a free support normalizer. |
| Semantic-relation support certificate | Semantic-relation support certificate | A nonlinear semantic relation instance, such as \(y=y_0\vee y_1\), requires the declared support to contain a standard membership certificate for the hard tuple. |
| Cone-budget extension lower bound | Cone-budget extension lower-bound corollary | A cone-annotated extension proof with final-interface size \(q\) and maximum cone size \(d\) must satisfy \(qd\ge 2n^{a-o(1)}\) near threshold. |
| Bounded-depth extension tradeoff | Bounded-depth extension tradeoff corollary | A bounded-fanin cone-annotated extension proof with final-interface size \(q\), fan-in \(r\), and final depth \(h\) must satisfy \(qr^h\ge 2n^{a-o(1)}\) near threshold. |
| Support-local normalizer | Support-local normalization transfer theorem | A proof system maps every accepted proof to support-local constraints with a support budget \(B(|\pi|)\). |
| Carrier-independent audit extractor | Carrier-independent audit upgrade criterion | The proof-system artifact itself computes support, support-locality evidence, and budget without a carrier-specific namespace manifest, hidden role advice, or semantic oracle. |
| Private occurrence rows | Row-forcing theorem | The proof exposes occurrence labels and unexposed positions are independently completable. |
| Equality quotient labels | Quotient residual-distance theorem | The proof induces a sound equality quotient with freely completable residual quotient labels. |
| Acyclic OR-tree frontier | Acyclic OR-tree residual certificate | After eliminating internal OR nodes, a root-zero frontier requires all leaves, while a root-one frontier requires one true leaf. |
| Quotiented OR-DAG frontier | OR-DAG frontier residual certificate | After eliminating internal OR nodes and soundly quotienting repeated reachable frontier formulas, a root-zero frontier requires all distinct reachable classes, while a root-one frontier requires one true reachable class. |
| Acyclic Boolean frontier | Acyclic Boolean frontier residual certificate | After exposing a finite acyclic Boolean frontier circuit, support-locality is the root coordinate plus an ordinary pointwise Boolean certificate for the induced frontier function. |
| Visible adaptive frontier | Visible adaptive frontier residual certificate | After exposing a finite adaptive decision tree over frontier coordinates, support-locality is the root coordinate plus an ordinary pointwise certificate for the induced decision-tree function; the logged transcript path is sufficient support. |
| Visible adaptive branching-program frontier | Visible adaptive branching-program frontier residual certificate | After exposing a finite acyclic branching program over frontier coordinates, support-locality is the root coordinate plus an ordinary pointwise certificate for the induced branching-program function; the logged computation path is sufficient support. |
| Hidden adaptive transcript summary | Hidden adaptive transcript insufficiency separator | A reported transcript summary is not a normalizer unless controller/path completeness or enough dependency support is certified; otherwise the same transcript can hide all-frontier OR support. |
| Controller-complete adaptive audit | Controller-complete adaptive audit normalizer | A hidden adaptive transcript becomes a normalizer when the proof object exposes a complete acyclic controller, replay path, and local equivalence certificate for the claimed completion cylinder. |
| Trace-complete DPLL decision log | Trace-complete DPLL decision-log normalizer | A DPLL-style proof object supplies the controller-complete adaptive audit when it logs the full finite decision controller, hard-tuple replay path, terminal value, and local clause or propagation witnesses for the completion cylinder. |
| Antecedent-complete CDCL learned-clause log | Antecedent-complete CDCL learned-clause normalizer | A CDCL-style proof object supplies the same audit when every learned clause used by the replay has an acyclic antecedent DAG down to original local clauses, decisions, unit propagations, or lower-rank learned clauses. |
| CDCL antecedent-erased log | CDCL antecedent-erasure trichotomy | If learned-clause antecedents and role provenance are erased, a support extractor must add equivalent provenance or a non-plain semantic invariant, pay conservative role-agnostic support, or be unsound on a same-skeleton lift. |
| RUP-complete CDCL/DRUP log | RUP-complete CDCL support normalizer | Checker-visible RUP propagation certificates over a known live clause database supply the same audit when formula-label support is parsed by a namespace, role map, or local-support parser, and deleted-clause consequences retain their support charge. |
| Canonical-namespace RUP-CDCL manifest | Canonical-namespace RUP-CDCL standardizer | A deterministic manifest with a reserved formula-label variable interval, injective coordinate map, live-database log, and retained deleted-clause supports makes the RUP-CDCL support parser checker-visible. |
| Self-auditing RUP-CDCL trace | Self-auditing RUP-CDCL instantiation | The proof syntax itself contains the checked label decoder, live-database reconstruction, RUP propagation witnesses, and retained deleted-clause support; the support audit is computed from the proof artifact rather than a side manifest. |
| Append-only self-auditing RUP-CDCL trace | Append-only self-auditing RUP-CDCL instantiation | If the trace is deletion-free, the monotone clause-addition log and RUP witnesses determine touched formula-label support; retained deleted-clause support annotations are unnecessary. |
| Prefix-typed append-only RUP-CDCL trace | Prefix-typed append-only RUP-CDCL instantiation | If formula-label variables are public syntax in an append-only RUP-CDCL system, the same scan needs no proof-internal label decoder or retained deleted-clause support annotations. |
| Prefix-typed RUP support-witness necessity | Prefix-typed RUP support-witness necessity | Public label syntax and append-only RUP checking do not certify completion-local auxiliary support without a witness or intrinsic invariant. |
| Nonlocal/compressed witness | None from this paper | A different argument is required. |

## Gate Impact

The normalization target strengthens literature closure and prevents proof-complexity overclaiming.  Restricted named-system routes are now proved for explicit-assumption resolution, the used unit core of full-assignment resolution refutations, explicit local clauses over formula-label variables, support-local auxiliary resolution, support-local extension resolution, dependency-cone extension normalization, canonical syntactic-cone normalization, final backward-slice lower bounds, slice-explicit ER lower bounds, displayed acyclic ER length lower bounds, expansion-bounded compressed ER transfer, macro-compressed ER reuse tradeoffs, support-declared macro ER support budgets, support-audited LRAT trace budgets, provenance-typed LRAT support audits, namespace-typed LRAT antecedent closure, strict-prefix Qrep replay, trace-complete DPLL decision logs, antecedent-complete CDCL learned-clause logs, CDCL antecedent-erasure trichotomy, RUP-complete CDCL support normalization, canonical-namespace RUP-CDCL standardization, the carrier-independent audit upgrade criterion, self-auditing RUP-CDCL instantiation, append-only self-auditing RUP-CDCL instantiation, prefix-typed append-only RUP-CDCL instantiation, prefix-typed RUP support-witness necessity, support-audit necessity separation, support-erasure indistinguishability, plain LRAT extraction trichotomy, semantic-relation support certificates, acyclic OR-tree frontier certificates, quotiented OR-DAG frontier certificates, acyclic Boolean frontier certificates, visible adaptive frontier certificates, visible adaptive branching-program frontier certificates, hidden adaptive transcript insufficiency, controller-complete adaptive audits, cone-budget extension lower bounds, bounded-depth extension tradeoffs, and the general support-local normalization transfer.  The remaining publication-level blocker is now sharper: supply an intrinsic support-locality invariant, handle deletion-bearing or untyped RUP-CDCL traces, or replace the proof-system payoff with an explicit SAT-family/source lower-bound theorem.
