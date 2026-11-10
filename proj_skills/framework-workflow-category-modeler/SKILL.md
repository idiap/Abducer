---
name: framework-workflow-category-modeler
description: Build an evidence-bound category-theory-style model of native Prism workflow descriptions for a paper appendix. Use after workflow extraction to define typed objects, occurrence arrows, composable paths, and control annotations while separating path syntax from execution semantics.
---

# Framework Workflow Category Modeler

Turn a frozen `PrismWorkflowAppendixSource` packet into a `PrismWorkflowCategoryModel` packet for the appendix writer. This describes the paper's named reasoning workflows by default; distinguish them from the Prism ME development lifecycle. This manual authoring lane does not extend the deterministic paper runner.

Read [the packet contract](references/category-model-contract.md) when constructing a model. Read [the native worked example](references/worked-example.md) for effect wrappers, retained inputs, or the abductive motif. Consume extracted evidence and approved notation; request an extractor refresh for missing facts instead of supplementing a frozen packet silently.

1. Bind the model to the source packet ID and digest. Preserve scope, original-versus-native provenance, capability profile, and omissions or unresolved mismatches.
2. Build a directed multigraph of exact typed boundary bundles and occurrence instances or documented structural adapters. Distinguish repeated occurrences of the same operation. Record named ports, provenance, posture, and the source expression establishing each adapter.
3. Define the free category of finite graph paths: identity is an empty path and composition concatenates endpoint-compatible paths. These laws concern constructed syntax. Type compatibility does not establish guard satisfaction, resource availability, reachability, termination, or scientific correctness.
4. Preserve relation certificates as annotations with their contracts; `assume`, `test`, and `calibrate` are not automatic coercions or proofs. Preserve `Generated[T]`; explicit `.value` extraction is an adapter, not identification with `T`.
5. Represent multiport inputs as named bundles with explicit packing and retained bindings. A bundle is one graph object, not automatically a categorical product or tensor. The paper's parallelism sign is motif notation unless stronger structure is established.
6. Retain guards, alternatives, stops, feedback, partial order, and parallel joins as control annotations. Do not linearize unordered branches or infer unconditional repetition from feedback.
7. Supply an arrow table, checked representative paths, notation correspondence, and equation/interpretation obligations. Explain information omitted by shorter motif notation. Hand the model to claim curation and the appendix writer with unsupported claims unapproved.

For a proposed functor, specify a target category and assignments on objects and generators. Distinguish mathematical extension on free syntax from empirical adequacy for execution. For commuting diagrams or a quotient, provide exact parallel paths, equality notion, scope, and witness. Similar labels, identical endpoints, smoke tests, or matching samples establish neither equivalence nor better reasoning.

Before delivery, check endpoints, named-port completeness, wrappers, contextual carry-through, provenance, guards, and ledger consistency. Return unresolved entries for missing evidence rather than inventing arrows. Emit the packet in the request's scratch/output directory; this skill does not install a schema or authorize manuscript publication.
