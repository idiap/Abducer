<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Dependent type model packet contract

`PrismWorkflowDependentTypeModel` version `1.0.0` is a JSON-compatible prose authoring contract. It is not a registered runtime schema or executable type checker. Input is `PrismWorkflowAppendixSource` version `1.0.0`; an optional category packet supplies comparison only.

## Required fields

| Field | Meaning |
| --- | --- |
| `schema_version` | Literal `1.0.0` |
| `model_id` | Stable nonempty identifier |
| `source_packet_id` | Exact source `packet_id` |
| `source_digest` | Exact source `source_digest` (= `input_digest` = evidence index `index_digest`), not a serialized-file byte hash |
| `scope` | Workflow IDs, profiles, layers, coverage status per workflow, omissions and reasons |
| `notation` | Symbol/native-name correspondence; judgment and equality syntax; universe convention; optional category-model ID |
| `contexts` | Ordered binding telescopes defined below |
| `type_families` | Nominal types and dependent families with index contracts |
| `operation_judgments` | Native signatures and separately labeled proposed judgments |
| `derivations` | Representative let/substitution chains and their review status |
| `adapters` | Explicit unwrap, pack, erase, or transport steps |
| `equality_obligations` | Proposed conversions/identifications and their justification or gap |
| `control_annotations` | Branch, guard, stop, feedback, partial-order, and join facts with layer provenance |
| `claim_boundaries` | Allowed descriptions, unsupported claims, assumptions, unresolved obligations |
| `evidence_refs` | Source evidence IDs resolving to frozen paths/spans, digests, and evidence posture |

Every modeling record has an `id`, `evidence_refs`, and `origin` (`native`, `source_descriptive`, or `proposed_refinement`). `source_descriptive` includes mathematical abbreviations or contextual binding presentations of native facts, without suggesting the source implements that notation. Proposed records also state `rationale`, `obligations`, and `native_support` (supported aspects plus missing guarantees). Empty evidence arrays are permitted only for explicitly proposed mathematical constructions; describe their source motivation and distinguish literature from repository evidence.

A context has `id`, `parent_context_id` (null at root), and ordered `bindings`. Each binding has `name`, `type_expression`, `depends_on`, `role` (`data`, `operation_symbol`, `relation_record`, `assumed_proposition`, or `proof_term`), optional `definition`, and evidence/origin. Inherited names remain in scope; avoid shadowing. Dependency lists include all free variables from types and definitions. A proof-term role needs an exact proposition and derivation or checked artifact, not a suggestive variable name.

A family has `id`, `context_id`, `parameters` (ordered typed binders), `type_expression`, `inhabitant_contract`, and `dependence_explanation`. Parameters that only decorate a label do not establish a dependent refinement. State what makes a value admissible at this index and whether that condition is stipulated, evidenced, or enforced. Use `Type` as a schematic sort unless a universe discipline is actually specified; never assert `Type : Type`.

An operation judgment has `id`, `workflow_id`, `occurrence_id`, `context_id`, `native_signature`, `presentation_signature`, `input_bindings`, `output_binding`, `relation_annotations`, and `effect_boundary`. A proposed strengthened signature is a separate record linked by `refines_judgment_id`; it cannot replace native evidence. Opaque generation symbols represent declared occurrence contracts and no termination or operational behavior.

A derivation has `id`, `context_id`, `steps`, `conclusion`, `review_status` (`manual_checked`, `unresolved`, or `machine_checked`), `checks`, and `execution_status` (`not_assessed`, `observed`, or `verified_with_scope`). Each step gives its incoming context, expression, result type, rule (`application`, `let`, `pair`, `projection`, `substitution`, `conversion`, or `transport`), premise IDs, and instantiated substitutions. Machine checking requires tool/version, source artifact digest, command, result, and exact checked scope; otherwise use manual status. An unresolved proposed adapter makes the corresponding native-realization obligation unresolved even when the abstract typing derivation is well formed.

An adapter has `id`, `context_id`, `input_types`, `output_type`, `expression`, `source_expression` (null if absent), `preserved_bindings`, `discarded_information`, and `realization_status` (`source_explicit`, `descriptive`, `proposed`, or `unresolved`). No generic `.value` accessor is presumed for an unobserved wrapper: cite the relevant source use. A proposed forgetful map may erase an index into a native record; no inverse refinement map follows automatically.

An equality obligation has `id`, `context_id`, `left`, `right`, `ambient_type`, `kind` (`definitional`, `identity`, or `observational`), `status` (`justified`, `conditional`, `unresolved`, or `rejected`), and `justification`. For definitional conversion give the allowed expansion/computation rule. For identity give `p : Id_A(a,b)` and its source/derivation; record any `transport_B(p,u) : B(b)` explicitly. Observations retain their test scope and do not silently authorize conversion or transport. Equality of claim text is not automatically identity of claim artifacts or their provenance.

Control records name affected judgment/step IDs, exact source expressions or explicit unknowns, evidence layer, and projection differences. Preserve unknown branch order. Candidate guard-as-type encodings require a declared predicate and a producer of its evidence; Boolean flags alone do not provide that producer. Relation annotations retain their exact source/target bindings, including generated targets.

## Mathematical conventions and claim limits

In the chosen presentation, `Γ,x:A ⊢ t:B(x)` with `Γ ⊢ a:A` supports capture-avoiding substitution `Γ ⊢ t[a/x]:B(a)`. Dependent application yields `f(a):B(a)` from `f:Π(x:A).B(x)`. A dependent pair `(a,b):Σ(x:A).B(x)` requires `b:B(a)`; an ordinary claim/assessment record with unindexed assessment type does not itself enforce this relation.

Definitional equality is judgmental conversion under stated rules. An identity type is a type whose inhabitant can support transport; do not identify the two. These conventions draw on the authors' [Type theory chapter, §§1.1, 1.4, 1.6, 1.12](https://github.com/HoTT/book/blob/master/preliminaries.tex) and [transport, §2.3](https://github.com/HoTT/book/blob/master/basics.tex) in *Homotopy Type Theory* (Univalent Foundations Program, 2013). Use only this ordinary dependent-type fragment: no univalence, higher inductive types, function extensionality, or homotopical interpretation is imported into Prism.

All Prism index families, erasure maps, and workflow judgments in this packet are authoring constructions unless backed by native evidence. A term encoding an assessment is data, even if it is indexed by a claim; typing alone establishes no scientific truth, successful runtime behavior, inference soundness, or empirical quality. No normalization, subject reduction, decidable type checking, or calculus-wide substitution theorem is claimed without a specified calculus and corresponding proof.
