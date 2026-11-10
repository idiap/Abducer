---
name: to-prism-run-parallel-tests
description: Execute an approved differential-test manifest for source Codex workflows and generated Prism workflows, using isolated parallel runners and preservation-safe evidence. Use after test design review; do not run native, model-backed, or generative cases without their exact authorization.
---
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Run Codex–Prism parallel tests

Execute the approved manifest without changing its cases, oracle, normalization,
or correspondence rules. Treat source skills and conversion inputs as
read-only. This skill collects differential evidence; it does not repair either
implementation or approve its own preservation claim.

## Verify authority and freeze inputs

Reject a missing, proposed, stale, or internally inconsistent manifest. Verify
the recorded source and conversion fingerprints, project semantic taxonomy
hash, and approved generation-plan hash before execution and confirm that
negative controls fail under the specified oracle. Refuse a manifest whose
comparison surface generalizes an exact nominal contract, derives occurrence
boundaries from skill files, or treats a generated value as validated,
supported, or proved without the reviewed later constructor.

Before source-native execution, obtain authorization for the exact command,
environment, network policy, credentials policy, timeout, attempt count, and
fixtures. Before any model-backed Codex execution, obtain authorization for the
provider/model, prompt and tool scope, network access, token/cost budget, case
count, and retry limit. Generative execution needs the same explicit authority
for its generator, even when its design is already approved. Authorization for
one runner, workflow, case set, or model does not authorize alternatives.

Static inspection, Prism check/compile, and fake-handler smoke execution stay
within their existing authority, but cannot substitute for a missing approved
native/model leg. When the required authority is absent, leave Trace and
Behavioral `not_tested` and report the blocked descriptor rather than
simulating a favorable baseline.

## Execute isolated parallel legs

Copy only the frozen test inputs into separate disposable workspaces. Route all
caches, logs, generated cases, model output, Prism artifacts, and temporary
credentials outside the source and conversion trees. Verify source fingerprints
again after execution and stop on mutation, credential exposure, an unreviewed
effect, scope expansion, or exhausted time/cost/retry budgets.

When parallel agents or runners are available, assign one the Codex leg and one
the Prism leg. Give both the same frozen case bundle but only the implementation
and authority needed for their own leg. Do not reveal one result to the other or
allow either runner to adapt cases. Wait for both, then run the deterministic
normalizer and independent oracle in a separate comparison pass. Sequential
execution is acceptable when it preserves the same isolation.

For approved generative cases, record generator version, prompt or strategy,
seed, rejected cases, and shrink path. Replay and minimize each mismatch into a
deterministic regression fixture. Do not retry merely to obtain agreement, and
do not change the approved oracle or normalizer during the run.

## Preserve bounded claims

Record raw observations beside normalized values. Classify each mismatch as an
implementation defect, conversion loss, allowed nondeterminism,
oracle/normalizer defect, unsupported capability, or unresolved evidence. A
passing fake Prism run establishes smoke execution only; offline `verify-run`
establishes recorded artifact/core integrity only. Neither establishes Codex
trace or behavior.

Produce machine-readable evidence and a concise summary containing:

- manifest hash, workflow mapping, source/conversion fingerprints, runner and
  dependency versions, and authorization boundaries;
- case IDs, fixture hashes, provenance, seeds, and exact runner descriptors;
- references to raw/normalized outcomes, logical traces, effects, negative
  control results, mismatches, and minimized reproducers;
- per-observable comparison status and evidence IDs; and
- unsupported debt and the maximum claim permitted by the evidence caps.

Apply [the preservation policy](../../references/preservation-policy.md). Make
the evidence consumable by `$to-prism-review-preservation`, but leave
publication eligibility to that independent review.
