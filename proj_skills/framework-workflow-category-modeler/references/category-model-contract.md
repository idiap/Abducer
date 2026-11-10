<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Category model packet contract

This prose contract defines the JSON-compatible `PrismWorkflowCategoryModel` version `1.0.0`. It is a manual authoring interface, not an installed schema validator. Consume `PrismWorkflowAppendixSource` version `1.0.0`; references resolve within these packets or their frozen evidence index.

## Required fields

| Field | Type and meaning |
| --- | --- |
| `schema_version` | Literal `1.0.0` |
| `model_id` | Nonempty stable string |
| `source_packet_id` | Source packet's `packet_id` |
| `source_digest` | Exact source packet's `source_digest` (= its `input_digest` = `RepositoryEvidenceIndex.index_digest`), not a byte hash of the serialized index file |
| `scope` | Workflow IDs, profiles, source layers, omissions with reasons, and paper notation correspondence |
| `objects` | Boundary-object records defined below |
| `generators` | Occurrence/adapter arrow records defined below |
| `paths` | Representative finite paths and typing checks |
| `control_annotations` | Guard, branch, stop, feedback, partial-order, parallel, and join records |
| `semantic_interpretation` | Status (`not_claimed`, `proposed`, `specified`, `verified`), target category or null, object/arrow assignments, assumptions, obligations, evidence references |
| `equation_obligations` | Candidate equalities with exact paths, equality notion, scope, status, witness or unresolved reason |
| `claim_boundaries` | Allowed descriptive claims, unsupported claims, unresolved items, and evidence or missing-evidence reasons |
| `evidence_refs` | Source evidence IDs preserving paths/spans, hashes, and posture |

Each object has `id`, `label`, `ports` (ordered records of `name`, exact `type`, wrapper, binding provenance), and `evidence_refs`. Record type refinements explicitly. Object identity is exact declared bundle identity, not label similarity. A multiport bundle can represent retained context without asserting a product universal property.

Each generator has `id`, `workflow_id`, `kind` (`occurrence` or `structural_adapter`), `occurrence_id` (null for adapters), `domain`, `codomain`, `port_bindings`, `relation_annotations`, `effect`, `posture`, and `evidence_refs`. A contextual occurrence identifies its underlying operation and unchanged bindings. Each adapter records its source expression and whether source-explicit or a proposed model construction; a proposed adapter cannot establish implemented behavior.

Each path has `id`, `domain`, `codomain`, `generator_ids` in traversal order, `typing_status` (`checked`, `unresolved`), and separate `admissibility_status` (`not_assessed`, `conditional`, `evidenced`) with guard/evidence references. An empty path is an identity only when domain equals codomain. Adjacent endpoints must match exactly. Representative paths do not enumerate the free category, which contains every finite graph path.

Each control annotation has `id`, `kind`, affected object/generator/path IDs, source expression or explicit unknown, source-layer provenance, and `evidence_refs`. Preserve failure, cancellation, retry, and unavailable branches where declared. A routing-assessment value does not execute the selected route.

Each equation obligation has `id`, `left_path`, `right_path`, `equality_notion`, `status` (`syntactic`, `verified`, `conditional`, `unresolved`, `rejected`), `scope`, and `witness` (null when absent). Nonparallel paths cannot form an equality. Free-category equality means the same ordered generator sequence, including empty identities; graph diamonds do not commute by default. Observations have only their observed scope.

## Semantic boundaries

- Guards annotate syntax. Filtering paths by arbitrary guards need not yield a subcategory. Refined-state or partial-map semantics require definitions and closure checks. Alternatives alone do not establish coproducts.
- A feedback endomorphism gives finite syntactic iterates, not termination or a fixed point. Preserve stop policy without adding a trace operator.
- Preserve partial order and join dependencies in parallel blocks. A tensor interpretation needs monoidal structure and effect/resource and coherence obligations; bundles alone do not supply these.
- `Generated[T]` supplies no monad, probability distribution, Kleisli category, totality, or effect commutation law. An execution interpretation must account for relevant failure, state, nondeterminism, and provenance.
- Mapping native names to `A,D,R,E` starts as labeled correspondence. A functor requires a target category and typing-preserving assignments. Mathematical extension from free syntax is distinct from empirical adequacy.
- Equivalence needs exact categories, functors, and witnesses; similar graphs and successful runs do not suffice. Keep scientific truth and reasoning quality separate from syntactic laws.

The free-path construction follows Emily Riehl, *Category Theory in Context*, Example 4.1.13, printed p. 137: [author-hosted text](https://emilyriehl.github.io/files/context.pdf). Boundary bundles and control annotations above are this skill's proposed representation; the reference does not validate Prism execution.
