---
name: to-prism-model-workflows
description: Recover reviewed typed contracts and provider-neutral workflow topology from an inspected agent project. Use after inventory when semantic boundaries or edges need judgment; do not use to render Prism source.
---
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Model contracts and workflows

Resolve semantic questions that deterministic extraction cannot answer, while
leaving graph construction and schema validation to
[`bin/to-prism`](../../bin/to-prism).

## Prefer explicit evidence

Read the modeling gates in [the conversion
contract](../../references/conversion-contract.md). Begin with the schema-valid
inventory and extracted contract/graph proposals. Rank evidence as follows:

1. executable configuration, schemas, command interfaces, and hook payloads;
2. explicit calls, imports, capability references, and test assertions;
3. instrumented baseline traces and fixtures;
4. structured examples and documentation; then
5. prose cues, only when consistent with stronger evidence.

File order, headings, shared names, or adjacency do not establish execution
order. Every accepted edge and boundary needs source evidence.

## Recover nominal contracts

Apply `$to-prism-derive-types` before accepting public ports or epistemic
occurrence signatures. Consume its reviewed type ledger; do not replace its
domain-specific types with transport-shaped or generic envelopes.

For each entry point and callable unit, determine the smallest honest nominal
input, output, recoverable failure, effect, permission, provider, environment
binding, and confidence record. Distinguish persistent agent capabilities from
invocation-local capabilities. A skill task type must reflect its real task;
do not collapse all skills to `String`, `Task`, `Input`, `Output`, `Data`,
`Payload`, `Result`, or `Any`.

Keep an unresolved port when alternatives remain plausible. Ask for review only
when the alternatives materially change a generated type, effect boundary,
workflow boundary, portability class, or verification oracle. Record accepted
overrides and the evidence they supersede.

## Recover topology

Identify actual entry points and logical task boundaries before lifecycle
hooks. Represent data, control, condition, lifecycle, failure, and stop edges
separately. Model sequence, fan-out/parallelism, joins, exhaustive choice,
bounded repeat with changing state, delegation, aggregation, retry, and timeout
only when source evidence supports them.

Reject or leave unresolved:

- dangling references, ambiguous entry points, and unreachable required nodes;
- choice without exhaustive convergent branches;
- repeat without a positive static bound or visible state change;
- inferred execution order based only on prose/file order; and
- a whole upstream workflow disguised as one leaf adapter.

When a source feature cannot render or execute through the supported public
Prism boundary, preserve its graph/contract fact and record capability debt.
Do not hide commands, MCP/network/file effects, dynamic model tool use,
delegation, retry, or timeout behavior in a generic Python call.

Model reasoning-occurrence boundaries separately from material skill
boundaries. Consume the reviewed granularity decisions from
`$to-prism-derive-types`: several skills may materialize one occurrence, and
the same skill may contribute to several occurrences. Split on a separately
observable typed epistemic result, review/critic boundary, branch/join, or
provenance/assurance change; merge complementary skill contributions that have
one inseparable result. Never infer nodes from the count or order of skill
files, prompts, agents, or hooks. In the conversion profile, every modeled
epistemic node has a `Generated[T]` result; deterministic and effectful work
remains visible in materialization.

## Hand off

Record judgments as reviewed decisions linked to source and IR IDs, then run the
CLI model validator. The handoff is schema-valid `contracts.json` and
`workflow.json` with typed or explicitly unresolved ports, evidence on every
inferred edge, reviewed occurrence-granularity rationales, both directions of
the occurrence/skill map, complete inventory dispositions, and an explicit
list of unsupported runtime behavior. Do not render or manually edit `.prism`
in this skill.
