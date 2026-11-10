<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Prism type taxonomy for conversions

This reference tells a conversion author which Prism type family to use and
what claim that family permits. The taxonomy is ordered from ordinary data to
strong assurance. A converter must preserve the weakest honest type: it must
never strengthen a value merely because a source skill, agent, or hook uses
words such as “verified”, “evidence”, or “proof”.

This is a taxonomy of Prism type families, not a catalogue of reusable domain
types. Every conversion derives nominal project-specific contracts first:
prefer `RankedIncidentHypotheses`, `CausalInferenceObjection`, and
`MitigationDecision` to `Output`, `CritiqueResult`, and `Data`. See
`epistemic-objects-and-operations.md` for object distinctions, operation
signatures, critic types, and the specificity gate; see
`semantic-taxonomy.json` for the machine-readable candidate catalogue.

## Taxonomy at a glance

| Family | Representative forms | Meaning in a conversion |
| --- | --- | --- |
| Primitive | `Bool`, `String`, `Int`, `Nat`, `Float`, `Decimal`, `Bytes`, `Char`, `Duration`, `Time`, `Unit`, `Never`, `Type`, `Prop` | Atomic values and propositions |
| Structural | records, variants, generic records, aliases, function types | Domain contracts and closed alternatives |
| Collection | `List[T]`, `Set[T]`, `Map[K, V]`, `Tuple[...]` | Typed groups; collection shape alone grants no assurance |
| Control and failure | `Option[T]`, `Result[T, E]`, `FailureUnion[...]` | Absence and explicit typed failure |
| Provenance | `Generated[T]`, `Evidence[T]`, `Computed[T]` | Where a value came from and how it was produced |
| Assurance | `Validated[value: T, P(value)]`, `Supported[P]`, `CoreTerm[P]`, `Proof[P]`, `Verified[T, P]` | Increasingly explicit grounds for accepting a value or proposition |
| Reasoning method | `Deductive[...]`, `Abductive[...]`, `Inductive[...]`, `Analogical[...]`, `Contrastive[...]`, `ModelBased[...]`, `Refutational[...]`, `Evidential[...]` | The epistemic operation performed by a reasoning occurrence |
| Relation | `Relation[...]`, nominal certificate records, `|~`, `|-` | The typed meaning of an edge between occurrences |
| Callable and orchestration | function types, `Workflow[T]`, `Reasoning[T]`, `Execution[T]`, refinement types | Executable composition and bounded iteration |
| Capability and artifact | `Model`, `Tool[C]`, `Tools[...]`, `Skill[T]`, `Skills[...]`, `Hooks[P]`, `Resource[T]`, `Source[T]`, `GraphSource[T]`, `Connection[T]` | Typed access to external or packaged facilities |
| Effect permission | `ModelGenerate`, `PythonCall`, `ToolCall`, `FileRead`, `DataRead`, `ClockRead`, and effect rows | Authority required for an effectful boundary |

## 1. Primitive and proposition types

Use primitives for atomic domain fields. `Nat` is a non-negative integer;
`Never` is the error type for an operation that cannot fail. `Prop` is special:
it is the type of a proposition, not a runtime boolean.

```prism
type ReviewRequest:
    text: String
    revision: Nat
    urgent: Bool

def Acceptable(request: ReviewRequest) -> Prop:
    return claim("the review request is acceptable")
```

`Acceptable(request)` names a claim. It does not test the request and it does
not produce a proof. Use `Bool` for an ordinary predicate result and an
assurance type when the result must carry justification.

## 2. Structural types

### Records

Records are immutable nominal contracts with named fields:

```prism
type Finding:
    summary: String
    accepted: Bool
```

Prefer records over unstructured strings at workflow boundaries. Field names
become part of data-flow and preservation contracts.

Names identify both domain referent and epistemic role. A
`DatabaseLatencyObservation` is not an `OperatorCauseClaim`; an
`IncidentAnalysisCritique` is not a `MitigationDecision`. Generic records such
as `Input`, `Output`, `Item`, and `ReasoningResult` are conversion defects when
source evidence or downstream use supplies a more specific meaning.

### Closed variants

Variants represent an exhaustive set of alternatives:

```prism
type ReviewError:
    | MissingInput
    | PolicyViolation(rule: String)
```

Use a closed variant for choice routers and typed failures. Do not use free
text when downstream logic must distinguish cases.

### Generic types and aliases

Generic records preserve a reusable shape:

```prism
type Envelope[Payload]:
    value: Payload
    source_name: String

type ReviewStep = (request: ReviewRequest) -> Result[Finding, ReviewError]
```

A callable alias states an exact input, result, and optionally effects. It is
particularly useful for reasoning occurrences and tool contracts.

## 3. Collections, absence, and failure

Use `List[T]` for ordered values, `Set[T]` for unique unordered values,
`Map[K, V]` for keyed values, and `Tuple[...]` for a fixed product. These are
ordinary data containers.

Use `Option[T]` when absence is expected and is not an error. Use
`Result[T, E]` when failure is observable and must be handled. `Ok(value)` and
`Err(error)` construct the two `Result` cases; `try` propagates an error through
a compatible enclosing result.

Do not collapse operational failure, policy rejection, and epistemic
uncertainty into one boolean. They are different contracts:

- `Result[T, E]` says whether an operation completed;
- an `accepted` or status field says what a policy decided; and
- `Supported[P]`, `Validated[...]`, or `Proof[P]` says why a conclusion has its
  assurance status.

## 4. Provenance types

The provenance wrappers are peers, not a ladder. None implicitly converts to
another.

| Type | Use only when | Typical constructor |
| --- | --- | --- |
| `Generated[T]` | A model or other generative producer emitted `T` | `generate[T](...)` |
| `Evidence[T]` | `T` was observed from an attributable source and method | `observe(...)`, `query[T](...)`, `resource_evidence[T](...)` |
| `Computed[T]` | A named deterministic procedure computed `T` | `compute(...)` |

Important conversion rules:

- generated content is not evidence;
- reading a prompt or skill is not observing its claims;
- a successful tool call returns data, not validation;
- deterministic computation records provenance but does not prove its result;
- `map_evidence` and `combine_evidence` must name the transformation and retain
  source provenance.

## 5. Assurance types

### `Validated[value: T, P(value)]`

A named deterministic validator accepted the exact `T` against proposition
`P(value)`. The validator is auditable application logic, not the proof kernel.
Create it with `validate` and explicit requirements.

### `Supported[P]`

Evidence supports proposition `P` under a named `MaterialPolicy`. Material
support is written with `|~`. It can be accepted or rejected by the policy; it
is never strict entailment.

### `CoreTerm[P]` and `Proof[P]`

`CoreTerm[P]` is proof syntax elaborated against the independently declared
target `P`. `Proof[P]` exists only after `kernel.check` accepts that term.
Model text, Python output, symbolic output, and prose are not proofs.

### `Verified[T, P]`

`Verified[T, P]` pairs a value `T` with a kernel-checked `Proof[P]`. Construct
it with `verify(value, proof)`. It is the strongest value-oriented assurance
form in this taxonomy.

The safe transition graph is explicit:

```text
ordinary T --generate--> Generated[T]
ordinary T --observe/query--> Evidence[T]
ordinary T --compute--> Computed[T]
T --validate against P--> Validated[value: T, P]
Evidence[T] --material policy |~ P--> Supported[P]
proof syntax --elaborate against P--> CoreTerm[P]
CoreTerm[P] --kernel.check--> Proof[P]
T + Proof[P] --verify--> Verified[T, P]
```

There are no implicit arrows between branches.

## 6. Reasoning-method types

Reasoning methods describe epistemic operations; they do not execute code and
their names do not grant assurance.

| Method | Exact intent | Common conversion mistake |
| --- | --- | --- |
| `Deductive` | Derive from explicit premises and rules | Labeling any deterministic function “deductive” |
| `Abductive` | Propose the best available explanation or bridge | Treating all model generation as abduction |
| `Inductive` | Generalize provisionally from observed cases | Treating aggregation as induction |
| `Analogical` | Transfer through an explicit correspondence | Matching similar field names |
| `Contrastive` | Explain a difference between baseline and alternative | Treating a conditional branch as contrastive reasoning |
| `ModelBased` | Draw implications by probing an explicit domain model | Treating an AI model call as model-based reasoning |
| `Refutational` | Search for contradiction, defeater, or counterexample | Treating ordinary validation as refutation |
| `Evidential` | Calibrate a conclusion from evidence and criteria | Treating any file or command output as evidence |

If no method matches, define a project-local callable type only after the
inadequacy analysis and review described in `reasoning-mapping.md`. Parsing,
routing, formatting, prompting, retrying, tool calls, and deployment remain
operational steps rather than new reasoning types.

For generated projects produced by this kit, every epistemic occurrence uses
`ExactInput -> Generated[ExactOutput]`. This is a `to_prism` conversion-profile
constraint, not a limit of the Prism language. `Evidence`, `Computed`,
`Validated`, `Supported`, `Proof`, and `Verified` require a separate explicit
material constructor or checker and never appear as the direct result of the
generative occurrence.

Use four broad inference classes only as a cross-cutting label: `formal`,
`material_defeasible`, `representational`, and `symbolic_computational`.
Retrieval and database querying can be `none`. The exact callable type and its
domain input/output still carry the real semantics; do not multiply method
types merely to mirror skill verbs.

The method family alone is insufficient. Each occurrence needs an exact domain
signature and result object. `Abductive` does not mean “returns text”: an
incident diagnosis can take `List[DatabaseLatencyObservation]` and
`List[IncidentCauseHypothesis]` and return `RankedIncidentHypotheses` with
criteria, grounds, uncertainty, ties, and residual anomalies. Hypothesis
generation, ranking, critique, adversarial review, refutation, validation,
calibration, synthesis, and decision remain distinct transformations even when
one source skill prompt mentions several of them.

Occurrence count is also independent of skill count. Several skill artifacts
may jointly materialize one typed commitment, and one skill may contribute to
several commitments. Split only when the target project exposes an
independently meaningful result, review/critic boundary, branch/join, or
provenance/assurance transition; otherwise keep complementary instructions in
one occurrence and record the decision in `granularity_rationale`.

## 7. Relations and certificates

A reasoning relation types an edge. Use:

- an ordinary nominal certificate when the edge records dependency,
  correspondence, testing, or another domain fact;
- `|~` when evidence materially supports a proposition under policy; or
- `|-` only when the edge is backed by kernel-checked proof.

The reasoning layer declares the relation contract. The materialization layer
provides the pure certificate builder or proof-producing implementation.

## 8. Callable, workflow, and refinement types

A function type gives the exact input/result/effect contract. `Workflow[T]`
and `Execution[T]` describe executable orchestration and its result/trace;
`Reasoning[T]` identifies an abstract reasoning plan. Refinement types make
bounded repetition explicit through `RefinementPolicy`, attempts, feedback,
and exhaustion failures.

Use `sequence` only for real dependency, `parallel` for independent branches
that later converge, `choice` for one exhaustive closed-sum route, and
`repeat` only with a static bound and visible changing state.

## 9. Capabilities, artifacts, and effects

`Skill[T]`, `Tool[C]`, `Hooks[P]`, and `Model` describe configured artifacts;
they do not imply that the public runtime can activate every provider feature.
`Source[T]`, `GraphSource[T]`, `Resource[T]`, and `Connection[T]` describe
external data or service boundaries.

Effect rows state observable authority:

```prism
def call_leaf(input: ReviewRequest, access: PythonCall) -> Result[Finding, PythonError]
    ! {Python.Call}:
    return python_call[Finding]("reviews.inspect", input, access)
```

The capability parameter authorizes the call; the effect row exposes it in the
contract. A converter must retain typed errors and must not hide orchestration
inside a single opaque leaf call.

## Selection checklist

For each converted boundary, ask in order:

1. What is the smallest nominal data contract?
2. Can the value be absent or can production fail?
3. Was it generated, observed, or deterministically computed?
4. Is there an actual validator, material policy, or kernel proof?
5. Is this an epistemic operation or only operational orchestration?
6. What capability and effect authority does execution require?
7. Does the installed public Prism runtime support that effect/provider?
8. Does the nominal name identify a target-project object and epistemic role
   rather than a generic container?
9. For a score, rank, critique, or decision, are criteria, grounds,
   uncertainty, and authority explicit?

When evidence is insufficient, keep the weaker type and record the gap. Type
strength is a claim and therefore part of preservation evidence.
