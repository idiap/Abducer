<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Preservation policy

Preservation is evaluated per workflow and per claim. It is never a single
similarity score, and a failed critical workflow cannot be hidden by averaging
successful noncritical workflows.

## Result vocabulary

Every check has one of these states:

- `established`: the required evidence passed;
- `not_applicable`: the source workflow does not contain the feature;
- `not_tested`: the feature may be supported, but the required test was not run;
- `unsupported`: the selected Prism/runtime boundary cannot preserve it; or
- `failed`: a performed comparison or invariant check failed.

Use `not_tested` when authorization, fixtures, or a baseline are absent. Use
`unsupported` only for an identified capability gap. Neither state is success.

## Preservation levels

### Asset

Claim Asset preservation only when every in-scope source element is mapped to
a generated artifact, retained as an opaque non-secret asset, explicitly
excluded by a versioned profile, or reported as debt. Exact path/content hashes
must establish preserved bytes. Record executable-mode, symlink, metadata, and
native-resource behavior losses separately even if content bytes match.

### Structural

Claim Structural preservation only when an independently reviewed or observed
source graph corresponds to generated Prism entry points, nodes, edges,
conditions, joins, loops, lifecycle transitions, and failure/stop paths. A
second projection of the converter's own IR is not independent evidence. An
opaque adapter that owns upstream orchestration cannot establish this level.

### Contract

Claim Contract preservation only when inputs, outputs, nominal types, failures,
effects, permissions, provider identity, hooks, environment requirements, and
entry points correspond. Type-checking generated code is necessary but does
not by itself show that the source contract was recovered correctly.

### Trace

Claim Trace preservation only when normalized native and Prism executions of
the same fixtures traverse corresponding logical stages, including applicable
failure, stop, retry, hook, and loop paths. A fake Prism handler, static hook
round trip, or offline artifact-integrity verification cannot establish Trace.

### Behavioral

Claim Behavioral preservation only when observable outputs satisfy the same
independent oracle. Exact output equality is appropriate for deterministic
workflows. For nondeterministic workflows use shared schemas, invariants,
properties, deterministic replay/fakes, and, optionally, authorized
statistical evidence. Never report sample similarity as proof of equivalence.

### Epistemic

Claim Epistemic preservation only when a reviewed map shows that epistemic
roles, exact logical inputs, typed relations, provenance, and assurance
transitions are retained. An operational-only workflow may mark this level
`not_applicable`. Generated prose, tool success, or material support cannot be
promoted to evidence, validation, or proof without the corresponding checked
constructor or verifier.

## Minimum gates

The reviewed workflow policy declares which levels are required. Unless the
user defines a stricter policy:

- every published workflow requires Asset, Structural, and Contract to be
  `established`, except a deliberately partial conversion that is prominently
  labeled and whose debt is accepted;
- a workflow with genuine reasoning requires Epistemic to be `established`;
- Trace or Behavioral is required only when the stated conversion goal calls
  for runtime equivalence, but its absence must remain visible; and
- a portable claim additionally requires successful offline relocation,
  dependency-integrity, launcher, check, compile, and selected run tests.

A required `failed` or `unsupported` result blocks publication. A required
`not_tested` result blocks the corresponding preservation claim and normally
blocks publication until the user explicitly revises the threshold. Accepted
debt never changes a failed check into `established`.

## Evidence rules and caps

- Content hashes and decode comparisons support Asset only.
- Graph correspondence supports Structural only.
- Prism `check`/`compile` and schema comparisons support Contract/executability,
  not source equivalence.
- `prism run --handler fake` supports typed execution smoke only.
- `prism verify-run --mode offline` supports recorded effect/core artifact
  integrity only; it is neither replay nor behavioral evidence.
- An unavailable native baseline caps Trace and Behavioral at `not_tested`.
- Static native-hook parsing and round trip can support Asset, Structural, and
  parts of Contract, not activation or observable outcomes.
- Hook adapter materialization supports a runtime packaging fact, not native
  activation.
- A hook path may contribute to Trace only when native instrumentation observes
  it and normalized stage correspondence is checked.
- A preserved Claude hook is capped at Structural/Contract while no compatible
  Prism runtime activates it.
- A Codex hook can exceed that cap only through an authorized instrumented run
  that covers its cwd, resource, environment, failure, and timeout behavior.
- Unsupported dynamic model tool selection, MCP/process/network effects,
  retries, timeouts, or delegation cap the affected workflow at the strongest
  level that does not rely on that behavior.

## Independent oracles

Prefer, in order: an explicit source test contract; an instrumented native
trace; a reviewed graph/contract fixture maintained independently of renderer
IR; or a user-approved domain oracle. Record origin, version/hash,
normalization, limitations, and all workflow IDs it covers.

Normalizers may remove temporary roots, timestamps, random invocation IDs, or
fields explicitly declared nondeterministic. They must be versioned and tested
with negative controls showing that exit status, domain outputs, ordering,
failure identity, and meaningful branch differences remain observable.

## Review outcome

For each workflow, report:

1. criticality and required levels;
2. each level's state and direct evidence identifiers;
3. uncovered nodes, contracts, effects, hook behavior, and reasoning choices;
4. the maximum justified claim and each cap that lowered it; and
5. whether publication is allowed, blocked, or allowed only as explicitly
   accepted partial/linked output.

The aggregate result is the minimum required outcome across all critical
workflows plus a list of noncritical exceptions. Do not convert this into a
percentage that obscures failures.
