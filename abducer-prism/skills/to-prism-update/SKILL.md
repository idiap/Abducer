---
name: to-prism-update
description: Update an existing Prism conversion after its upstream project changes, with semantic invalidation and three-way conflict review. Use when a prior conversion lock exists; do not overwrite manual edits.
---
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Update a Prism conversion

Preserve valid reviewed decisions and user work while treating upstream changes
as semantic changes, not harmless cache misses.

## Establish update identity

Read the incremental-update section of [the conversion
contract](../../references/conversion-contract.md) and [the output
contract](../../references/output-contract.md). Require explicit source and
output paths, a compatible prior lock, and its content-addressed generated base
(or reproducible equivalent). Verify the current output before proposing
changes. Do not infer the base from current generated files after they diverge.

Use [`bin/to-prism`](../../bin/to-prism) to re-inventory and compute file and
semantic diffs across inventory, contracts, workflow, reasoning map, profiles,
templates, capabilities, and dependencies. Do not edit the source or run native
commands by default.

## Review invalidation

Reuse a decision only when its source evidence, profile facts, semantic inputs,
and downstream assumptions remain valid. For each changed item, examine its
dependency edges and invalidate the minimum correct set of contract,
topology, reasoning, adapter, oracle, and preservation decisions. A changed
hash is a signal to compare semantics, never automatic permission to reuse or
discard a decision.

Route new or changed domain meanings to `$to-prism-derive-types`, newly
ambiguous contracts/topology to `$to-prism-model-workflows`, new or changed
epistemic intent to `$to-prism-map-reasoning`, and affected baseline
descriptors to `$to-prism-baseline` if execution evidence must be refreshed.
Any native rerun requires fresh authorization for the exact descriptor.
Changes to skill boundaries do not automatically change reasoning granularity;
changes to typed epistemic outputs, critic/review boundaries, branch/join
structure, or provenance/assurance do. Re-run the many-to-many granularity
test and preserve generative `Generated[T]` results for every epistemic
occurrence.

## Regenerate safely

Have the CLI render into staging and perform a three-way comparison among the
prior generated base, current output, and new generated result:

- accept unchanged generated files that changed only in the new result;
- preserve user-owned files;
- preserve current edits when the generator did not change the same content;
- emit a conflict when both current output and new generation changed the same
  generated content; and
- never publish a conflicted or partially validated stage.

Unknown incompatible lock/schema/profile/template versions require an explicit
migration or a stop. Never guess a migration.

## Verify and publish

Run affected structural, contract, fixture, dependency, and preservation tests,
retaining a full-verify option. Apply `$to-prism-review-preservation` to changed
claims and any newly capped workflow. Publish atomically only after conflicts
are resolved, source fingerprints are unchanged, locks/hashes validate, and
all selected gates pass. Report reused, invalidated, newly reviewed, and
conflicted decisions plus all preserved manual files.
