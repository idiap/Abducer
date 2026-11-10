---
name: formal-claim-producer
description: Compile one exact typed formalization seed from committed reflective theory ancestry into a registered ready-or-not-ready formal-claim packet. Use only after conceptual discovery has produced a sealed formalization seed and current literature/theory ancestry; never use it to invent a theorem from prose, establish truth, choose a theory, or bypass reflective physics relevance.
---

# Formal Claim Producer

## Role

Translate one already-authored, typed formalization seed into a mechanically
checkable claim-and-execution-plan packet. This is a narrow provenance bridge
between conceptual discovery and later proof investment. It is not a creative
theory generator, proof checker, theorem authority, or physics-value judge.

Reuse `reflective-theory-synthesizer` for conceptual reconstruction and
formalization-seed generation. Reuse the Category/HoTT and formal-physics
routes only when their own committed handbacks supply the selected seed. Keep
dynamic experiments downstream and optional: experimental outputs may motivate
a later reflective cycle, but same-cycle experiment ancestry cannot authorize a
formal claim.

## Required Inputs

Require exactly one dispatcher input envelope conforming to
`agentic/spec/discovery_formal_claim_producer_input_v2.schema.json`. It must
bind:

- target, run, cycle, branch, hypothesis, concept, conjecture, and preferred
  conceptual-system identities;
- one successful registered source-producer request and receipt;
- one exact semantic formalization-seed row from the source output history;
- the current literature authority and theory ancestry;
- the source theoretical-programme identity and digest; and
- explicit authority nulls and the no-same-cycle-experiment boundary.

Reject an envelope that supplies a caller-authored `formal_claim`,
`proof_adapter`, `execution_plan`, proof result, preferred theorem, or theory
winner. Reopen every referenced artifact and descriptor before compilation.

## Total Compilation Contract

Return exactly one v2 producer output with status `ready` or `not_ready`.

### Ready

`ready` is permitted only when the selected seed begins with the versioned
`abducer-formal-claim-v2:` marker followed by canonical JSON containing exactly:

- `display_statement`;
- `formal_claim`;
- `proof_adapter`; and
- `execution_plan`.

The claim kind, adapter, and plan kind must agree with the registered contract.
All identities and digests must be derived from the sealed source bytes. Do not
repair, broaden, reinterpret, or complete the proposition during compilation.

### Not ready

Return `not_ready` without claim or plan fields when the seed is prose,
malformed, unsupported, ancestry-inconsistent, or based on non-current
literature. Preserve the source text as the display statement and emit a typed
rejection reason. `not_ready` is a successful total operator outcome; it means
the scheduler should request further formalization rather than reserve a prove
action.

## Provenance and Commit Boundary

The raw producer output never authorizes proof execution. A parent may construct
`discovery_formal_claim_authority_v2` only after reopening, from one verified
transaction commit:

- the current registered producer row and exact registry bytes;
- the producer request, input descriptor, successful receipt, and passing
  validator receipts;
- the immutable output-history bytes;
- the exact source request, source receipt, source inputs, and source output;
- the semantic-row identity and digest; and
- the current theory and literature ancestry.

Detached mappings, current-registry drift, output substitution, and stale theory
heads fail closed. The committed authority remains provenance for a later proof
handoff; it still grants no truth, checker-soundness, theorem, theory-selection,
or physics-value authority.

## Adapter Discipline

- `exact` accepts only exact equality or exact integer-predicate claims and the
  built-in worker plan.
- `finite_model` accepts only finite-model claims and the built-in worker plan.
- `lean` accepts only a Lean proposition contract and a Lean plan. Later proof
  execution must independently enforce the registered toolchain protocol and
  axiom report; zero exit alone is never a proof.
- `command` accepts only an external-checker claim and a registered external
  checker plan with explicit identity and version. Later execution must bind
  exact checker authority.

Do not weaken these pairings to make a seed executable.

## Output Contract

Produce a packet conforming to
`agentic/spec/discovery_formal_claim_producer_output_v2.schema.json` with:

1. source and namespace identities copied exactly;
2. source request, receipt, output-history, semantic-row, programme, literature,
   and theory-ancestry bindings;
3. a content-derived output ID and digest;
4. the total status and typed rejection reason;
5. claim, adapter, and plan plus their digests only when ready; and
6. explicit authority nulls.

The validator must independently reopen the input envelope, recompute the
entire output, and require exact equality.

## Validator Dependency Boundary

The registered independent validator uses a derived repository closure, not a
hand-maintained file list. From captured immutable producer, validator,
dispatcher, and registry Python roots, recursively include every
repository-local import and package initializer. From the registered
schedule-binding schema and every schema literal in that Python closure,
recursively include each local `$ref`. Bind the exact formal-claim skill and
operator-registry bytes as semantic roots and pin every admitted third-party
runtime distribution exactly.

Reject capture races, import shadowing, registry/current disagreement, any
missing, extra, or substituted closure entry, and any new or changed nested
schema reference. Repository paths remain relative so the same bytes can be
verified after relocation. This closure establishes only implementation and
contract identity; every claim-truth, proof, theorem, semantic-independence,
theory-selection, and physics-value null remains false.

## Physics Handback

When the seed comes from Category theory, HoTT, or another high-abstraction
route, require its upstream committed formal-physics handback to identify the
physics target, protected successes, changed conceptual resource, and concrete
formal obligation. This producer only compiles that obligation. It cannot infer
physics relevance from mathematical elegance, abstraction level, or formal
tractability.

## Failure and Demotion

Fail the invocation on descriptor tampering, cross-branch or cross-generation
substitution, unsuccessful or unregistered source production, source digest
drift, non-canonical identity sets, or a non-current authority join. Return
`not_ready`—rather than failure—for an honestly sealed but untyped or
unsupported seed.

Never claim that registration establishes semantic independence, novelty,
truth, conceptual depth, unification, theorem status, or physics value.

## Validation Handoff

Hand a ready producer output to the post-commit authority join. Hand a
not-ready output to reflective formalization planning. Only a committed ready
authority may be copied into a proof handoff and then bound to one frozen prove
action through the independent action-coordination ledger.
