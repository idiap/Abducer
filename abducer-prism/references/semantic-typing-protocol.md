<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Semantic type induction protocol

This protocol turns a provider-native project into an evidence-backed taxonomy
and then into exact contracts for canonical `.prism`. It is intentionally a
review gate: the converter must not guess through a semantic gap.

## Epistemological rule

A public type is a claim that two values may be treated alike and that certain
distinctions may be ignored. That claim needs warrant. For each proposed type,
the project must establish:

1. **identity** — what domain object or epistemic object the value denotes;
2. **structure** — which distinctions its consumers observe;
3. **provenance** — how the value became available;
4. **assurance** — what supports accepting or using it; and
5. **defeaters** — which conditions would weaken that interpretation.

`String`, `Task`, `Input`, `Output`, `Data`, and `Any` erase these distinctions.
They are not neutral conveniences at a known public boundary: they assert that
the distinctions do not matter. Generation therefore rejects them.

## Induction procedure

Use `$to-prism-derive-types` after inventory and before workflow modeling.

1. Collect producer and consumer evidence from schemas, typed functions,
   validators, tests, fixtures, prompts, hooks, tools, and approved traces.
2. Use the bundled semantic taxonomy and close Prism examples to propose
   candidate object families and operation shapes.
3. Confirm, rename, split, or discard every candidate against the target
   project's evidence. An example is never evidence about the target.
4. Separate domain referent, epistemic role, provenance, and assurance. In
   particular, keep statement, claim, observation, evidence relation,
   hypothesis, critique, judgment, decision, and action distinct.
5. Trace each epistemic workflow occurrence as an exact
   `InputType -> Generated[OutputType]` and expose only independently
   observable semantic intermediate values.
6. Apply the granularity test: split on independent consumption, review,
   criticism, validation, branch/join, persistence, or provenance/assurance;
   merge complementary instructions/lenses that make one inseparable
   commitment. Record `granularity_rationale` and the rejected alternative.
7. Associate one or more skills with each occurrence, and allow one skill to
   contribute to several occurrences. State each contribution; a skill
   artifact is a materializer, not itself a reasoning type.
8. Record unsupported alternatives and semantic uncertainty as unresolved.
   Unresolved public semantics block approval rather than falling back to a
   generic envelope.

## Required artifacts

The derivation skill creates two separate artifacts:

- `project-semantic-taxonomy.json` is the discovery ledger. It records all
  supported object types, evidence anchors, reasoning and critic operations,
  skill compositions, assurance, and unresolved alternatives.
- `generation-plan.json` is the reviewed executable subset. It contains the
  exact nominal definitions, fixture, workflow port types, step chain,
  reasoning operations, effects, and materializing skills used by generation.

Validate both through the transferred package:

```sh
./to-prism validate conversion/project-semantic-taxonomy.json \
  --schema project-semantic-taxonomy
./to-prism validate conversion/generation-plan.json \
  --schema generation-plan
```

The generator accepts only an approved `generation-plan` at schema version
`1.0`. It neither infers nor repairs missing semantics.

## Composition invariant

The central unit is a typed workflow occurrence:

```text
exact domain input
  -> exact generative epistemic transformation
  -> Generated[exact domain output]
  materialized by one or more specifically described skills
```

The relationship is many-to-many. Two skills can jointly materialize one
occurrence, and one skill can contribute different guidance to two
occurrences. Neither skill count nor file layout establishes granularity.
Operational retrieval, parsing, deterministic computation/validation, and
effects remain outside the generative epistemic occurrence.

A reviewed executable workflow may nevertheless interleave those layers. Set
`semantic_mode` to `mixed`, retain each epistemic step as
`material_kind: agent` returning `Generated[T]`, and represent a deterministic
step as `material_kind: computed` only when an exact `python_adapters`
operation implements its nominal input/output contract. The step declares
only `Python.Call`, names the deterministic procedure, and explicitly applies
`compute` to construct `Computed[T]`. The generator keeps both failure classes
and the union of effects in the material workflow. A reviewed
`reasoning_projection` separately aggregates those material steps into genuine
epistemic occurrences and explicit sequence/parallel topology. It must cover
every epistemic material step and may map several material steps or skills to
one occurrence. The generator writes signatures to `occurrences.prism`, edge
contracts to `relations.prism`, and only imports, comments, and the core
composition to `reasoning.prism`. An unimplemented instruction,
deterministic-sounding skill name, or material ordering does not justify
`Computed[T]` or a reasoning edge.

For example, an incident workflow may preserve this chain:

```text
IncidentWitnessStatements
  -> TestimonialReliabilityAssessment
  -> CorroboratedIncidentEvidence
  -> AbductiveFailureHypothesisRanking
  -> RankedFailureHypotheses
  -> AlternativeHypothesisCritique
  -> CritiquedFailureHypothesisRanking
```

Each arrow has its own contract, rationale, failures, and skill composition.
The ranked result must retain candidates, criteria, grounds, uncertainty, ties,
exclusions, and defeaters. A critic must retain its target, standard, admissible
grounds, findings, severity, scope, and disposition. Neither is a list of text.

## Approval questions

Before approving a type or operation, ask:

- Which source anchors establish its identity and every consumer-visible field?
- What would be lost if it were replaced by `String` or `List[String]`?
- Does the name encode the domain referent and epistemic role?
- Is a score tied to a criterion, scale, direction, grounds, and uncertainty?
- Does provenance describe production without overstating assurance?
- Does criticism remain distinct from refutation or adjudicated invalidation?
- Does a decision remain distinct from a recommendation and an executed action?
- Can every workflow edge be checked as an exact nominal type transition?

See `epistemic-objects-and-operations.md` for the object and critic taxonomy,
`semantic-taxonomy.json` for machine-readable induction candidates, and
`type-taxonomy.md` for the corresponding Prism type families.
