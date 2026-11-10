---
name: to-prism-baseline
description: Design, authorize, and assess an isolated native baseline for a project being converted to Prism. Use when runtime behavior or a differential oracle must be captured; do not invoke merely to inspect source.
---
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Establish a native baseline

Create a truthful behavioral reference without running the original source
tree or silently acquiring new authority.

## Design the descriptor

Read the execution-authority and failure sections of [the conversion
contract](../../references/conversion-contract.md), then inspect the inventory,
source-native tests, documented entry points, and existing fixtures. Propose the
smallest descriptor that exercises a critical workflow and states:

- exact command/arguments and isolated-copy working directory;
- fixture inputs and environment-variable **names** (never secret values);
- timeout, retry/attempt limit, network policy, and expected filesystem writes;
- stdout/stderr bounds, exit-status expectation, and expected artifacts;
- normalizers with versions/hashes and negative controls; and
- an independent result/trace oracle.

Prefer an existing deterministic project test over inventing a new runner.
Mark unavailable prerequisites rather than installing packages or reading
ambient credentials without separate authorization.

## Obtain and respect authorization

Show the descriptor before execution and obtain explicit authorization for it.
Authorization is descriptor-specific: changed arguments, package installation,
network access, live model calls, credentials, extra retries, or another
workflow require a new grant.

After authorization, use the deterministic baseline command exposed by
[`bin/to-prism`](../../bin/to-prism); do not execute discovered commands
directly. It must operate on an isolated copy or enforced equivalent, apply the
declared limits, capture bounded evidence, and compare the original source
fingerprint afterward.

## Assess the evidence

Classify the baseline as `reproducible`, `flaky`, `nondeterministic`,
`unavailable`, or `failed`. Do not normalize away exit status, domain values,
meaningful ordering, branches, or failure identity. A failed or nonzero run can
be the correct native reference if the fixture intentionally covers failure.

Consult [the preservation policy](../../references/preservation-policy.md)
before using the result as an oracle. An unavailable baseline caps Trace and
Behavioral preservation at `not_tested`; a fake Prism handler or static source
comparison does not replace it. Record descriptor identity, authorization
scope, normalizers, raw/normalized artifact identities, observed instability,
and workflow coverage.
