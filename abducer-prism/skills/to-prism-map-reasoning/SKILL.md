---
name: to-prism-map-reasoning
description: Map recovered workflow operations to exact Prism epistemic methods, relations, and assurance boundaries. Use only when a conversion contains genuine reasoning intent; operational-only classification is valid.
---
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Map reasoning semantics

Read [the reasoning mapping reference](../../references/reasoning-mapping.md)
and [the type taxonomy](../../references/type-taxonomy.md) in full. Work from
the reviewed workflow/contracts plus their source evidence, not from generated
Prism or node names alone.

Require the reviewed type ledger and exact occurrence signatures from
`$to-prism-derive-types`. If they are missing, vague, or based on generic
`Input`/`Output`/`Data`/`Any` envelopes, return to type derivation before method
selection. Preserve distinct statement, claim, observation, hypothesis,
ranking, critique, defeater, judgment, decision, and action roles where the
project evidences them.

## Classify conservatively

For each candidate, state the exact logical input, useful result, and epistemic
operation without implementation language. Mark parsing, routing, collection,
formatting, prompting, validation mechanics, tool/model calls, deployment, and
other structural work `operational_only`.

For a genuine epistemic step, compare semantic fit across Deductive, Abductive,
Inductive, Analogical, Contrastive, ModelBased, Refutational, and Evidential.
Record the selected method, plausible alternatives, source evidence, and
confidence. “Calls an AI model” does not imply ModelBased; “checks something”
does not imply Refutational or Evidential.

Specify exact occurrence inputs/results, topology, relation endpoints and
certificate types. Keep the abstract declaration free of prompts, providers,
agents, tools, permissions, effects, failures, retries, and materialization
choices.

For mixed workflows, encode the approved abstraction as
`workflows[].reasoning_projection`. Give each occurrence a concise
domain-specific method and relation name, one exact logical input, a result
type, explicit argument-source bindings, and one or more `material_steps`.
Cover every epistemic material step at least once. Use the projection topology
to state sequence and parallel products; never infer that topology from the
material step list. Name aliases as produced results and join fields by their
downstream semantic role, avoiding generated-looking assignments such as
`context = context` when a more specific distinction is supported.

The generator emits operation signatures to `occurrences.prism`, relations and
certificates to `relations.prism`, and only imports, comments, and the core
composition to `reasoning.prism`. It must also emit an exact typed implementation
for every projected occurrence, deduplicate and compile the skills contributed
by its reviewed `material_steps`, attach the relation builders, and construct
the named reasoning binding in `materialization.prism`. A plan-only crosswalk
or low-level hook-agent sequence does not satisfy this boundary.

## Set occurrence granularity before method names

Do not equate a reasoning type with a skill. Build two reviewed maps:

```text
reasoning occurrence -> one or more skill contributions
skill artifact       -> one or more reasoning occurrences
```

Split adjacent candidates when an intermediate result is separately consumed,
reviewed, criticized, validated, branched/joined, or differently
provenanced/assured. Merge complementary prompts, context suppliers, and
specialist lenses when they jointly make one inseparable commitment with one
typed result. Operational activities stay in materialization. Record the
decision and rejected alternative in each occurrence's
`granularity_rationale`; source file, skill, agent, and prompt boundaries are
not evidence by themselves.

For this conversion profile, render every genuine epistemic occurrence as
`ExactInput -> Generated[ExactOutput]`, including hypothesis generation,
ranking, critique, abduction, synthesis, formalization, and epistemic judgment.
Do not return `Evidence`, `Computed`, `Validated`, `Supported`, `Proof`, or
`Verified` from the generative reasoning occurrence. Those forms require a
separate material constructor, validator, policy, or kernel boundary. Pure
retrieval, query execution, parsing, deterministic symbolic computation, and
action are operational/material operations rather than epistemic occurrences.

## Protect assurance

Identify where values are ordinary, generated, evidence, computed, supported,
validated, proven, or verified. Name the real constructor, validator, relation
builder, elaborator, or kernel check for every strengthening. If it is absent,
retain the weaker type and record the gap. Consult [the preservation
policy](../../references/preservation-policy.md) before proposing an Epistemic
preservation claim.

## Extend only when necessary

When no standard method fits, prepare the complete project-local custom-method
proposal required by the reasoning mapping reference, including inadequacy
analysis for plausible standards, one exact logical input record, result and
certificate types, materialization boundary, and tests. Require human approval
before generation. Never edit Prism's standard library or create a method only
to reshape data or name an operation.

Record the reviewed decisions in `reasoning-map.json`/`decisions.json` through
the conversion command surface and run its validator. The result is ready when
every workflow node is epistemic or explicitly operational, every mapping has
evidence, every epistemic result is generative, the occurrence/skill maps and
granularity rationales are complete, all low-confidence/custom choices are
reviewed, and no assurance transition is implicit.
