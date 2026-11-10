---
name: to-prism-review-preservation
description: Review conversion evidence, preservation caps, unsupported behavior, and publication eligibility for a generated Prism project. Use after verification; do not use to generate favorable claims from source alone.
---
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Review preservation

Independently assess the evidence already produced by inspection, native
baseline, generation, and verification. Do not repair evidence or rerender the
project during this review.

## Apply the policy exactly

Read [the preservation policy](../../references/preservation-policy.md) and the
reviewed per-workflow threshold. Evaluate Asset, Structural, Contract, Trace,
Behavioral, and Epistemic separately with only `established`,
`not_applicable`, `not_tested`, `unsupported`, or `failed`.

Check that structural comparison uses an independently reviewed/observed graph,
not another projection of renderer IR; contract comparison covers effects,
permissions, failures, providers, hooks, and entry points; trace/behavior uses
the same fixtures and an independent oracle; and reasoning/assurance decisions
have been reviewed.

Enforce evidence caps. In particular, hashes establish asset integrity,
check/compile establish typed executability, fake handlers establish smoke
execution, and offline `verify-run` establishes recorded artifact/core
integrity. None of those establishes native trace or behavior. Absence of a
baseline leaves Trace/Behavioral `not_tested`. Static or materialized hook
artifacts do not establish native activation.

## Review debt and portability

Read [the output contract](../../references/output-contract.md) when the output
claims to be portable. Verify evidence for exact dependency closure, hashes,
licenses/SBOM, platform tags, offline bootstrap, project-local launcher,
relocation, absence of ambient resolution, and successful check/compile/run for
the selected fixtures.

For every unsupported or opaque critical node, state which claims it caps and
whether the reviewed threshold permits publication. Accepted debt remains debt;
it does not become `established`. A linked output must name its external leaf
bindings and cannot be described as portable.

## Decide publication

Run deterministic verification/report validation through
[`bin/to-prism`](../../bin/to-prism), then review the machine evidence rather
than prose tone. Report each workflow's criticality, required levels, results,
evidence IDs, caps, and maximum justified claim. The aggregate outcome is the
minimum required result across critical workflows plus explicit noncritical
exceptions, never an average.

Approve publication only if every required gate is established (or a threshold
was explicitly revised), source fingerprints are unchanged, and the report
contains all debt. Otherwise block publication with actionable evidence IDs;
do not downgrade a failing gate silently.
