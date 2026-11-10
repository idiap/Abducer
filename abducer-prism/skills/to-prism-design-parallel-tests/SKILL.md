---
name: to-prism-design-parallel-tests
description: Design differential test manifests, independent oracles, and negative controls for source Codex workflows and generated Prism workflows. Use before execution when parity evidence needs a reviewed test contract; do not use to run native or model-backed workflows.
---
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Design Codex–Prism parallel tests

Design a frozen comparison contract that an execution skill can run without
inventing expectations after seeing results. Treat source skills, generated
Prism, and existing evidence as read-only. This skill designs tests; it does not
execute either workflow, invoke a model, or claim preservation.

## Establish correspondence

Start from the reviewed project semantic taxonomy, approved generation plan,
workflow graph, contracts, and source/conversion fingerprints. Apply [the
semantic typing protocol](../../references/semantic-typing-protocol.md) to the
comparison surface: use the exact nominal input, intermediate, and output
contracts already established by `$to-prism-derive-types`. Map each named Codex
entrypoint to its generated Prism entrypoint and map logical occurrences across
the two implementations. Mark unresolved or unsupported mappings rather than
guessing. A manifest cannot approve a generic port or infer occurrence count
from skill count.

Define observables before cases. Preserve `Generated[T]` at every generative
occurrence unless the reviewed workflow contains a later explicit constructor
for stronger assurance. Prefer typed outcomes, declared artifacts,
externally visible effects, logical stage activation and ordering, branches,
joins, bounded retries, canonicalized tool/provider calls, permission denials,
failure classes, and stopping conditions. Do not require free-form reasoning or
prose to be byte-identical.

Specify a narrow normalizer for contract-declared nondeterminism such as
timestamps, generated identifiers, temporary paths, explicitly unordered
collections, and approved wording variation. Preserve raw observations. Never
drop a field merely because it is difficult to compare or expected to differ.

## Design deterministic cases first

Prefer existing source tests, reviewed fixtures, recorded native baselines, and
minimal hand-authored success, boundary, failure, and permission cases. Give
both legs exactly the same logical input and environmental assumptions. Record
fixture hashes, dependency constraints, seed, timeout, attempt limit, expected
invariants, and allowed variation.

Include negative controls that demonstrate the comparator can fail, such as a
changed typed value, omitted stage, reordered required effect, wrong failure
class, excess retry, or unapproved tool call. Keep controls synthetic and
outside the source/conversion trees. A suite whose negative controls pass is
not a valid parity oracle.

Use generative testing only for a meaningful gap that examples cannot cover
economically, such as typed input breadth, branch boundaries, state sequences,
or metamorphic relations. Define a constrained domain, deterministic seed,
case/shrink budget, rejection policy, and stable replay format. Generation may
propose inputs and relations; it must not invent expected outcomes from the
Prism implementation or rewrite the oracle to make a mismatch pass. Model-based
generation remains only a proposed execution mode until separately authorized.

## Deliver an execution manifest

Produce a machine-readable manifest and concise rationale with:

- workflow/entrypoint and stage correspondence plus source/conversion
  fingerprints, taxonomy hash, and approved generation-plan hash;
- deterministic cases and negative controls with provenance and hashes;
- per-observable oracle rules, normalization rules, and allowed variation;
- isolated runner requirements, environment bounds, timeout/retry budgets, and
  stop conditions;
- any proposed generative strategy, provider/model needs, prompt/tool scope,
  token/cost and case budgets, seeds, and shrink procedure; and
- the exact native commands, Prism entrypoints, network/credential policy, and
  other authority that execution would require.

The manifest must be reviewable without executing either leg. Label it
`proposed` until a reviewer approves its mappings, oracle, controls, and
authority envelope. Hand approved manifests to `$to-prism-run-parallel-tests`;
do not treat approval of test design as implicit approval for native or model
execution.
