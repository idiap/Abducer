<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Reasoning mapping

Map epistemic intent separately from operational orchestration. A reasoning
occurrence answers a question about what licenses a conclusion, explanation,
generalization, comparison, model result, refutation, or calibrated status. It
does not represent parsing, routing, formatting, prompting, tool invocation,
deployment, or file order.

## Classification sequence

For each candidate node:

1. State its exact logical input and useful result without mentioning a model,
   prompt, provider, command, or implementation.
2. Identify the epistemic operation and the source evidence for it.
3. If the operation is only structural or operational, record
   `operational_only` and leave it in the executable workflow.
4. Otherwise compare its semantics, not its name, with every applicable
   standard method below.
5. Select typed relations and the output's provenance/assurance boundary.
6. Record alternatives, confidence, reviewer status, and dependent source
   elements. Low-confidence and custom mappings require review before
   generation.

## Granularity: occurrences are not skills

Reasoning granularity follows typed epistemic commitments, not provider
packaging. Maintain a many-to-many mapping:

```text
reasoning occurrence -> [skill contribution, ...]
skill artifact       -> [reasoning occurrence, ...]
```

Use this boundary test between adjacent candidate activities:

- **Split** when an intermediate is independently consumed, reviewed,
  criticized, validated, branched on, joined, persisted, or assigned different
  provenance/assurance, or when the source exposes a separate generative
  judgment with its own observable result.
- **Merge** when several skills merely provide complementary instructions,
  context, or specialist lenses for one inseparable input-to-output epistemic
  commitment.
- **Move out** parsing, retrieval, routing, formatting, deterministic
  validation/computation, model/tool invocation, and effects. These belong to
  materialization even when they share a skill file with reasoning guidance.

Record the accepted and rejected boundary in `granularity_rationale` with
source anchors. The count or order of skills, files, prompts, agents, hooks, or
model calls cannot decide the count of reasoning occurrences.

The repository examples illustrate the layers. In
`examples/language/refinement_loop`, the reasoning module declares abductive
and deductive occurrence topology; its materialization module separately owns
the narrator skill/agent, deterministic assembly, validation, optimization,
and material-support policy. Likewise,
`to_prism/examples/layered_release_review` separates the abstract release
reasoning from evidence capture, checks, policy, and relation builders. These
examples establish the layer boundary, not a one-method/one-skill rule.

## Generative conversion profile

General Prism can express generated, observed, computed, validated, supported,
or proved occurrences. The `to_prism` external-skill conversion profile is
deliberately narrower: every genuine epistemic occurrence is declared as
`ExactInput -> Generated[ExactOutput]`, and the composed reasoning returns
`Generated[FinalOutput]`. This includes hypothesis generation, ranking,
critique, abduction, synthesis, formalization, and epistemic judgment.

`Evidence`, `Computed`, `Validated`, `Supported`, `Proof`, and `Verified` may
appear only after a separate explicit material constructor, validator, policy,
or kernel boundary establishes them. Query/retrieval, deterministic symbolic
work, and effectful action are operational/material operations rather than
exceptions to the generative epistemic rule.

## Standard methods

| Method | Use when the operation... | Do not use merely because... |
| --- | --- | --- |
| `Deductive` | derives a conclusion from explicit premises and rules | code deterministically computes something |
| `Abductive` | proposes the best available explanation, premise, or bridge | a model generates text or a planner proposes steps |
| `Inductive` | generalizes provisionally from observed cases | a loop aggregates items |
| `Analogical` | transfers a conclusion through an explicit correspondence | two records have similar field names |
| `Contrastive` | compares a baseline and alternative to explain a difference | a conditional chooses a branch |
| `ModelBased` | obtains implications by probing an explicit domain model | implementation calls an AI model |
| `Refutational` | searches for contradiction, counterexample, or defeater | validation returns false |
| `Evidential` | calibrates status from evidence and tests | a file is called evidence or a command succeeds |

A pure constructor may reshape source data into a standard method's exact
logical input. That does not justify a new method. Operational preprocessing
that can fail or cause effects remains in materialization.

## Topology

Use `sequence` for real epistemic dependency, `parallel` for independent
occurrences whose outputs are later collected, `choice` for exactly one
exhaustive closed-sum alternative, and bounded `repeat` only when epistemic
steps re-execute over visible changing state. File or instruction order alone
is not evidence of sequence.

Every occurrence has a unique output and exact input. Relations attach to an
occurrence with exact source and target endpoints. Composition blocks do not
have the single logical input needed by a relation.

Use a relation certificate that matches what can actually be established:

- `|~` for material support of a proposition;
- `|-` only for a checked proof; or
- `-> Certificate` for an ordinary nominal witness.

The executable materialization builds certificates. The pure reasoning
declaration only states their contracts.

## Provenance and assurance

Keep ordinary data, `Generated[T]`, `Evidence[T]`, `Computed[T]`,
`Supported[P]`, `Validated[...]`, `Proof[P]`, and `Verified[...]` distinct.
No category implies another. The conversion's reasoning layer emits only
`Generated[T]`; any other category begins at a later material boundary. In
particular:

- generated text is not evidence;
- a successful tool call is not validation;
- supporting material is not proof;
- a Python or model effect returns ordinary untrusted data;
- evidence requires an attributable observation or source;
- validation requires an explicit checked predicate or validator; and
- proof requires proof construction/elaboration and the Prism kernel.

Record each transition with its actual constructor, validator, relation
builder, or checker. If none exists, retain the weaker type and report the gap.

## Custom method protocol

Propose a project-local method only when no standard method performs the same
epistemic operation. The proposal must contain:

- a concise operation statement independent of implementation;
- an inadequacy analysis covering the plausible standard alternatives;
- one exact logical input record and one result type;
- relation/certificate types, if any;
- whether the result is ordinary data, generated, evidence, computed,
  supported, validated, or proven, and why;
- the pure occurrence contract;
- the materialization boundary, including effects/failures kept outside the
  method; and
- deterministic and preservation tests.

Custom methods live in the generated project and are never added to Prism's
standard library automatically. A reviewer must approve the proposal before
generation.

Do not create a custom method for collection, record construction, parsing,
schema validation, routing, formatting, prompting, calling a tool/model,
retrying, deployment, or renaming an existing standard method. Those are pure
functions or operational workflow components.

## Review checklist

A reasoning map is ready only when every source node is either mapped to an
epistemic occurrence or explicitly operational; every occurrence has source
evidence, an exact logical input/result, and a semantic method rationale;
every epistemic result is `Generated[T]`; topology follows actual dependencies;
granularity rationales and both directions of the occurrence/skill map are
complete; relation endpoints and certificates are typed; assurance never
strengthens silently; custom methods have approved inadequacy analyses; and
the generated `.prism` declaration can remain pure of providers, prompts,
tools, permissions, effects, failures, and retry policy.
