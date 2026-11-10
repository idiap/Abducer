---
name: to-prism-derive-types
description: Derive evidence-backed, project-specific domain and epistemic types from an inspected project. Use before workflow and reasoning mapping when ports, reasoning results, critics, or assurance contracts need semantic names and structure.
---
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Derive specific Prism types

Turn source evidence into nominal contracts that say what knowledge a workflow
consumes, produces, challenges, and acts on. Read [the conversion
contract](../../references/conversion-contract.md), [the type
taxonomy](../../references/type-taxonomy.md), and [semantic induction
protocol](../../references/semantic-typing-protocol.md) in full. Work from the read-only
inventory, source files, tests, fixtures, schemas, and approved baseline
evidence. Do not infer types from generated `.prism` or generic node labels.
For workflows containing claims, observations, hypotheses, ranking, critics,
defeaters, judgments, decisions, recommendations, or actions, also read
[epistemic objects and operations](../../references/epistemic-objects-and-operations.md)
and use [the machine-readable candidate taxonomy](../../references/semantic-taxonomy.json)
to seed—not decide—the project taxonomy.

## Use Prism exemplars as induction, not authority

Search the bundled `examples/` and, when this kit is used inside a Prism source
checkout, the repository's `examples/` and `catalog/` for analogous domains,
input/output objects, reasoning operations, relations, and composed workflows.
Use close examples to propose candidate structures and idiomatic `.prism`
patterns. Record which exemplar induced each candidate.

An exemplar is a hypothesis-generating template, never evidence about the new
project. Accept a candidate field, invariant, reasoning occurrence, or edge
only when the inspected project's own source supports it. Rename exemplar types
to the new domain and discard any borrowed structure that lacks project
evidence. Do not copy catalog outputs as conversion evidence.

## Build an evidence ledger first

Start from concrete source examples and use the smallest type set that
preserves their observable distinctions. Introduce a nominal type only when it
is a public workflow port, a structured collection element, a value used by
more than one occurrence, or a distinction that changes control flow,
provenance, assurance, or validation. Otherwise keep the distinction as a
field. In particular, prefer one `FormalizedEquation` with `sympy_expression`
and `latex_expression` fields over separate types for each rendering unless
the workflow independently consumes those representations.

For every proposed public type, record:

- its project-specific PascalCase name and epistemic role;
- source anchors and the exact producer/consumer occurrences they support;
- fields, alternatives, ordering, cardinality, identity, and domain invariants;
- provenance and assurance level actually constructed by the source;
- confidence, unresolved questions, and review status; and
- the generic abstraction it replaces.

Rank executable schemas, command and hook payloads, code paths, test assertions,
fixtures, and traces above examples and prose. A filename or noun alone is only
a naming clue. Evidence for a field is not automatically evidence for its
meaning, invariant, or assurance. Keep incompatible interpretations as
separate alternatives until review.

Keep four axes separate in the type design: the domain referent, its epistemic
role, its provenance, and its assurance state. A transport string is not a
statement type; a statement is not automatically its propositional claim; a
claim is not evidence merely because a source asserted it; and evidence for a
hypothesis is not proof of that hypothesis. Likewise, confidence in an
extraction, a hypothesis-ranking score, and validation assurance answer
different questions and must not share one generic score/status field. A
critique or defeater challenges a target but does not erase or invalidate it
unless an explicit adjudication step establishes that result.

## Derive the epistemic chain

Trace each workflow occurrence through the roles it really contains. Derive
specific nominal input and result types for any evidenced role:

- **statement**: what an identified source says;
- **claim**: a proposition advanced as true and open to support or challenge;
- **observation**: an encountered or measured state with provenance;
- **hypothesis**: a candidate explanation or prediction;
- **ranked hypotheses**: an ordered collection whose score/ordering criterion,
  tie policy, and supporting evidence are explicit;
- **critique**: a targeted assessment of a named claim, hypothesis, ranking, or
  judgment against explicit criteria;
- **defeater**: information that undercuts support or rebuts a conclusion, with
  its target and kind represented;
- **judgment**: an assessed conclusion under criteria and uncertainty;
- **decision**: a selected commitment with alternatives and rationale; and
- **action**: an authorized intended operation, distinct from performing its
  effect.

These are roles, not sufficient type names. Use domain nouns and occurrence
meaning: `IncidentTelemetryObservation`, `CandidateRootCauseHypothesis`,
`RankedRootCauseHypotheses`, `PrimaryCauseRankingCritique`,
`TelemetryIntegrityDefeater`, `RootCauseJudgment`, `RemediationDecision`, and
`ApprovedRemediationAction`. Do not manufacture every role when the project
skips one, and do not collapse distinct roles merely because the source stores
them all as strings or JSON.

## Type reasoning, critics, and composition exactly

For each genuine reasoning occurrence, derive an exact logical input record and
an exact result before choosing a reasoning method. Name the occurrence's
domain-bearing transformation, for example
`RootCauseInferenceInput -> Generated[RankedRootCauseHypotheses]`, rather than
`Input -> Output`. Include the evidence, constraints, background assumptions,
and uncertainty the occurrence actually uses. In the `to_prism` conversion
profile every epistemic occurrence is generative: its result is
`Generated[T]`. Retrieval, parsing, deterministic computation, validation, and
effectful action are material or operational boundaries, not exceptions that
return a stronger epistemic type. A later explicit constructor may observe,
compute, validate, support, or prove a generated value; the reasoning
occurrence itself may not claim that assurance.

When one approved workflow interleaves epistemic and deterministic work, use
`semantic_mode: mixed`. Keep each generative occurrence as
`material_kind: agent` with `Generated[T]`. Mark a deterministic occurrence
`material_kind: computed` only when its exact nominal input/output contract is
implemented by a reviewed `python_adapters` operation; name its deterministic
`procedure`, declare only `Python.Call`, and return `Computed[T]`. The adapter
and `compute` constructor are the provenance boundary. A prompt, skill, hook,
or unimplemented operation is not sufficient evidence for computed provenance.

Set occurrence granularity independently of skill files. Start with the
end-to-end typed flow, then apply the boundary test between adjacent source
activities:

1. Split when the intermediate result is separately consumed, reviewed,
   criticized, validated, branched on, joined, persisted, or assigned different
   provenance/assurance, or when the source exposes a separate generative
   judgment with its own observable result.
2. Merge when activities are complementary instructions, context providers, or
   lenses that jointly make one inseparable epistemic commitment with one
   exact input and one exact output.
3. Move parsing, retrieval, routing, formatting, deterministic validation,
   tool invocation, and effects out of the epistemic occurrence even when a
   skill contains them.
4. Record a `granularity_rationale` with source anchors for every proposed
   occurrence and test the rejected split/merge alternative.

The mapping is many-to-many. One reasoning occurrence may compose one or more
skills, and one skill may contribute to several occurrences. Recover each
skill's contribution to each occurrence, intermediate values,
branch/join/aggregation edges, and the overall occurrence signature. Never
derive the number of reasoning occurrences from the number of skill files,
prompts, agents, or provider entry points. Do not hide a critic, ranker,
adjudicator, or aggregator inside one opaque reasoning node merely because the
provider invokes them through one entry point.

Treat critics as generative typed transformations and validators as separate
material typed transformations. A critic names its target type, criteria, and
generated result such as `Generated[RootCauseRankingCritique]`; a defeater
names the proposition/support it attacks and whether it undercuts or rebuts. A
validator may strengthen assurance only when a real check constructs that
stronger value after generation. Criticism, scoring, validation, and selection
are not interchangeable operations.

Classify each occurrence only when the examples justify it as `formal`,
`material_defeasible`, `representational`, or `symbolic_computational`; use
`none` for retrieval/query operations that merely return records. Do not invent
finer inference categories from prompt verbs.

Hand the reviewed occurrence signatures to `$to-prism-map-reasoning`; method
selection must not retroactively weaken or generalize these types.

## Reject semantic erasure

Block public ports or reasoning signatures based on `Task`, `Input`, `Output`,
`Data`, `Payload`, `Result`, `Item`, `Any`, unstructured maps, or bare
`String`/`text` envelopes. Scalars may appear as justified leaf fields, never
as a substitute for a known domain contract. Also reject names that merely add
`Request` or `Response` to a generic noun.

If evidence cannot yet distinguish a type, create an explicitly unresolved,
domain-named port with its alternatives and evidence gap; do not approve a
generic fallback. A lossy compatibility boundary may retain the provider's raw
payload only alongside the specific canonical type and an explicit adapter.

## Review and hand off

Write `conversion/project-semantic-taxonomy.json` and validate it with
`to-prism validate ... --schema project-semantic-taxonomy`. This is the
source-anchored discovery artifact: it records all supported object families,
exact operation signatures, per-occurrence skill compositions, assurance,
alternatives, and unresolved questions—even candidates not selected for the
first generated workflow. Then write the approved executable subset as a
`generation-plan` version `1.0` and validate it with the same public command.
Its `type_definitions` and workflow step contracts are the only semantic input
accepted by generation; do not hand-edit generic defaults into that plan.

Present the taxonomy and occurrence signatures for human review. Require review
for low-confidence meanings, competing interpretations, inferred invariants,
assurance strengthening, ranking semantics, critic/defeater targets, and any
generic or raw compatibility boundary. Then check:

1. every public workflow port names a project-domain concept;
2. every field and invariant has evidence or is marked unresolved;
3. statements, claims, observations, hypotheses, critiques, defeaters,
   judgments, decisions, and actions remain distinct where present;
4. ranked outputs specify element type and ranking semantics;
5. every reasoning, critic, and composed-skill occurrence has exact input,
   intermediate, and `Generated[result]` types;
6. every occurrence has a reviewed granularity rationale and an explicit
   many-to-many skill contribution map; and
7. provenance and assurance transitions name their constructors or checks.

Record approved type decisions with source/IR evidence IDs through the existing
conversion decision surface. Hand the reviewed taxonomy, type ledger, and
occurrence signatures to `$to-prism-model-workflows`; do not render `.prism` in
this skill.
