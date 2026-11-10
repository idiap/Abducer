<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Layers in a `to_prism` conversion

`to_prism` adds a Prism layer without replacing or silently rewriting the
external project. Two related layer models matter: the conversion pipeline and
the generated Prism project's semantic architecture.

## Conversion pipeline layers

```text
external project (read-only)
        |
        v
1. provider discovery and inventory
        |
        v
2. normalized contracts, workflow graph, and reasoning map
        |
        v
3. reviewed decisions and preservation obligations
        |
        v
4. canonical typed .prism generation
        |
        v
5. material adapters and portable dependency closure
        |
        v
6. checks, fixtures, differential evidence, report, and lock
```

### Layer 0: external provider project

This is the Codex, Claude Code, OpenCode, or Open Agent Skill project being
converted. Its instructions, skills, agents, hooks, tools, MCP declarations,
scripts, and configuration remain provider-native and unchanged. The converter
reads this tree and fingerprints it before and after every phase.

### Layer 1: discovery and inventory

Provider profiles classify source elements and record their paths, hashes,
ownership, contracts, and portability concerns. Discovery is descriptive. It
does not execute hooks or infer that a discovered feature is supported by
Prism.

Primary artifact: `conversion/inventory.json`.

### Layer 2: normalized semantics

The converter separates provider syntax from meaning:

- contracts describe typed inputs, outputs, errors, effects, capabilities, and
  assets;
- the workflow graph describes executable dependency and control flow; and
- the reasoning map identifies genuine epistemic occurrences, relations, and
  assurance boundaries.

Primary artifacts: `contracts.json`, `workflow.json`, and
`reasoning-map.json`. They support review and generation but are not executable
or authoritative.

Normalization derives the target project's epistemic ontology rather than
installing vague reusable placeholders. It distinguishes statement tokens from
propositions and claims; observations from evidence relations; hypotheses from
ranked assessments; critiques from objections, defeaters, and counterexamples;
and judgments, recommendations, decisions, and actions. Repository examples
can suggest candidate shapes, but target-project artifacts and consumers must
confirm every selected field.

### Layer 3: review and preservation policy

Humans approve ambiguous mappings, source copying, custom reasoning methods,
hook activation, native baseline execution, and unsupported debt. Preservation
claims are capped by available independent evidence; an offline integrity
check or fake handler cannot establish behavioral equivalence.

Primary artifact: `decisions.json` plus an approved generation plan.

### Layer 4: canonical Prism semantics

Typed `.prism` is the final workflow representation. It owns orchestration,
contracts, reasoning topology, relations, effects, failures, and application
wiring. JSON models, diagrams, Python adapters, and launchers must not redefine
that meaning.

Primary artifacts: `types.prism`, optional `reasoning.prism` and
`relations.prism`, `materialization.prism`, and `main.prism`.

### Layer 5: material and deployment boundary

Public Prism builders materialize compatible skills and hooks. Thin adapters
may implement named typed leaf effects; they cannot hide source-native
orchestration. The vendor wheelhouse, lock, SBOM, bootstrap, and launcher make
the result independently runnable on its declared Python/OS/architecture.

### Layer 6: verification and evidence

Static checking, compilation, fixture runs, adapter tests, independent graph or
output oracles, trace correspondence, and artifact-integrity checks establish
different levels of confidence. The report states exactly which level is
established, failed, unsupported, not tested, or not applicable. The lock binds
source, profiles, decisions, generated files, and dependencies.

Package-generated conformance is plan-bound. Verification reloads the embedded
official generation plan, validates its schema, checks the generated layer
shape against its semantic mode, and verifies the recorded plan and source
hashes. Successful Prism parsing or execution cannot substitute for these
checks.

## Layers inside the generated Prism project

```text
main.prism                           reasoning application/fixture boundary
    |
materialization.prism                executable implementation
    |
reasoning.prism                      high-level epistemic topology only
    |
occurrences.prism + relations.prism  occurrence and edge contracts
    |
types.prism                          nominal domain and failure contracts
    |
typed effect ports/adapters        external-world boundary
    |
Prism runtime and trace            execution evidence
```

Dependencies point downward, while results and evidence flow upward.

When a mixed workflow has a reviewed high-level projection,
`material_main.prism` additionally exposes the detailed operational/material
pipeline. It is not the public reasoning entrypoint and must not be used to
infer the reasoning topology.

### Domain layer: `types.prism`

Own nominal inputs, outputs, closed alternatives, errors, propositions, and
policy-related records. It should not contain provider configuration, prompts,
credentials, or effectful implementation.

This layer names concrete project objects: for example,
`DatabaseLatencyObservation`, `IncidentCauseHypothesis`,
`RankedIncidentHypotheses`, and `MitigationDecision`. `Input`, `Output`,
`Data`, `ReasoningResult`, and `List[String]` are not substitutes when workflow
semantics are knowable.

### Occurrence layer: `occurrences.prism`

Own abstract reasoning-operation signatures and meaningful semantic join
records. It remains pure of models, tools, effects, retry mechanisms, and
providers.

Each occurrence declares an exact operation and signature. In the `to_prism`
conversion profile that signature is `ExactInput -> Generated[ExactOutput]`.
Hypothesis generation, abduction, ranking, comparison, critique, adversarial
review, refutation, calibration, synthesis, and judgment remain separate when
they make independently observable epistemic commitments. Deterministic
validation and stronger assurance construction stay in materialization.

Occurrence boundaries and skill boundaries are independent. One occurrence
may compose several skills; one skill may contribute to several occurrences.
Split on independently consumed/reviewed/criticized results, branches/joins,
or provenance/assurance changes. Merge complementary instructions or lenses
that jointly produce one inseparable result. Every accepted boundary records a
`granularity_rationale`; file, prompt, agent, and skill count never decide it.
A critic declares target, standard, admissible grounds, and typed generated
finding output.

### Epistemic topology layer: `reasoning.prism`

Own only imports, concise documentation, and the core reasoning composition.
It answers “what kind of reasoning must happen, and in what dependency
structure?” Domain records, method signatures, relation declarations, skills,
hooks, effects, retries, and artifact transport belong to other layers. A
generated `reasoning.prism` must contain at least one `reasoning` declaration
and must not declare `type` or `relation` entries.

### Documentary sample companion: `sample_outputs.prism`

`sample_outputs.prism` is an additive, non-semantic companion rather than a fifth
ownership layer. It contains ordinary typed payload constants that illustrate the
inner `T` of each adjacent reasoning output `Generated[T]`, plus validator-owned
`# @sample` metadata for the exact binding, occurrence, stage, branch, example set,
and simulated/projection status. It must import only its workflow's `types.prism`.

This file answers “what might a reader see at this step?” while `reasoning.prism`
answers “what reasoning must happen?” and `materialization.prism` answers “how is it
executed?” A sample is not an observed trace, evidence, support, validation, proof,
or behavioral-equivalence result. Unresolved projection samples show expected shape
only. The stable alignment key is `<workflow-id>::<reasoning-name>::<binding-name>`;
the validator derives the expected set and order from reasoning and occurrence
authorities, while the manifest stores byte and alignment hashes.

### Relation layer: `relations.prism`

Own substantial relation and certificate contracts when edges carry meaning
beyond simple sequencing. Small relations may stay beside the reasoning
declaration. Builders live in materialization because a relation declaration
does not manufacture its own evidence or proof.

### Materialization layer: `materialization.prism`

Bind each abstract occurrence to a concrete function, workflow, agent, skill,
tool, source, policy, or typed leaf effect. This layer owns operational failure,
permissions, bounded retry/refinement, provider activation, deterministic
computation/validation, and any transition from generated output to evidence,
support, validation, or proof.

For a mixed `reasoning_projection`, bind every high-level occurrence by its
exact nominal signature, attach the deduplicated skills contributed by the
reviewed `material_steps`, construct its relation builders, and instantiate the
reasoning declaration. Keep the detailed material workflow alongside this
binding; do not substitute a plan cross-reference for executable wiring.

### Application layer: `main.prism`

Supply fixture or environment values, invoke or solve the workflow, and expose
the useful typed result. Until general CLI input injection exists, generated
projects use one literal typed harness per reviewed fixture.

For a reviewed mixed projection, `main.prism` solves the high-level reasoning
declaration using its explicit materialization. The detailed material pipeline
remains available through `material_main.prism`.

### Effect-adapter layer

Python or provider adapters implement only named leaf operations behind typed
ports. Inputs, outputs, errors, and authority stay visible in `.prism`. Dynamic
model-selected tools, unsupported provider hooks, and unavailable runtime
handlers remain explicit debt rather than being simulated invisibly.

### Runtime and evidence layer

The bundled public Prism runtime executes supported effects and emits traces
and effect records. A trace is evidence about the Prism execution. It becomes
equivalence evidence only when compared with an independently instrumented
native baseline and a declared oracle.

## Why the boundaries matter

The layer split prevents five common conversion errors:

1. provider filenames do not become workflow semantics by accident;
2. generated text is not promoted to evidence or proof;
3. operational steps are not mislabeled as epistemic reasoning;
4. adapters cannot become opaque replacements for canonical `.prism`; and
5. successful packaging or smoke execution is not reported as behavioral
   equivalence.

See `type-taxonomy.md` for the contracts that cross these layers and
`epistemic-objects-and-operations.md` for the epistemic ontology, operation
signatures, and critic taxonomy. See `examples/` for a concrete derivation, a
checked layered program, and an end-to-end conversion input.
