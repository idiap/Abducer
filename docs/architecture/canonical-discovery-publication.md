<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Canonical Discovery Publication

Canonical publication separates three kinds of identity: immutable scientific
core bytes, derived validation evidence, and the one mutable pointer that says
which exact core/evidence pair is current. A changed profile version or changed
evidence therefore creates a new evidence identity without pretending that the
underlying theory cycle changed.

## Pointer-last transaction

`publication-index.json` is a small, atomically replaced pointer to an immutable
`indexes/index-<sha256>.json` snapshot. Before that pointer can move, the
publisher validates the candidate core, evidence, profile authority, every
history row, every migrated-v1 row, and every retained-source archive. History
identities are unique and disjoint from current, including an `A -> B -> A`
sequence. If a failure occurs after replacement, the exact prior pointer bytes
(or exact prior absence) are restored while the publication lock is held.

Profile authority binds more than a profile name or version. It seals the
declared dependency closure, semantic policy inputs, and each callback's stable
code projection, positional defaults, keyword defaults, closure cells, and
nested callables. Validation recomputes every nested digest and requires each
callable map key to equal the callback's internal role. Consequently a callback
relabel, a changed closed-over policy value, or a rehashed nested record cannot
reuse earlier publication authority merely because the public version string
was left unchanged.

The immutable layout is:

- `publications/<core-id>/`: portable cycle, canonical state, workspace, and a
  root `bundle-manifest.json`;
- `evidence/<evidence-id>/`: replayed validation outputs, exact profile
  authority, and a root `evidence-manifest.json`;
- `indexes/`: byte-addressed complete snapshots;
- `archive/`: byte-preserving, non-current legacy trees whose original source
  is rehashed during validation.

Manifest exclusion is root-only. A nested file named `bundle-manifest.json`,
`evidence-manifest.json`, or `archive-manifest.json` is ordinary content and is
hashed. Source traversal uses no-follow file and directory descriptors, rejects
all links and special files before installation, and checks both the source and
copy against the pre-copy descriptor snapshot. A concurrent file/link swap is
therefore a failed publication, never silently dereferenced content.

Unsafe paths use `PublicationContractError.reason_code` as a stable automation
surface. `path_symlink`, `path_missing`, `path_not_regular_file`,
`path_not_directory`, `path_absolute`, `path_noncanonical`, `path_escape`,
`path_unavailable`, and `path_changed` describe public locator/root/pointer
failures; `source_symlink` and `special_file` describe forbidden members found
inside a traversed source tree. Operators should branch on `reason_code`, not on
human-readable exception text. For example, a publication root that is itself a
link and an index locator that crosses an intermediate link both report
`path_symlink`.

## Plan and publish

Plan mode validates the source and derives exact core/evidence identities without
creating the publication root:

```bash
uv run python agentic/scripts/publish_canonical_discovery_acceptance.py \
  --cycle <candidate>/cycle-result.json \
  --cycle-request <candidate>/workspace/canonical-cycle-request.json \
  --state-root <candidate>/canonical-state \
  --workspace <candidate>/workspace \
  --receipt-root <candidate>/workspace/operator-receipts \
  --target-id <target> --run-id <run> \
  --publication-root agentic/reports/canonical_discovery_cycle/acceptance \
  --plan
```

Replace `--plan` with `--publish` to install. DWF evidence projects staging
paths into logical bundle locators such as `cycle-result.json`,
`canonical-state`, and `workspace/operator-receipts`; consequently independent
plan and publish stages produce the same evidence bytes and the entire
publication tree remains valid after relocation.

## Validation and boundaries

```bash
uv run python agentic/scripts/validate_canonical_discovery_publication.py
```

Validation replays the selected immutable snapshot, both manifests, the live
profile dependency closure, exact derived evidence, history authorities, v1
migration records, and retained archive sources. Existing bytes under a claimed
content ID that differ are a collision and fail closed.

Version-1 migration is profile-prefix agnostic, so historical non-DWF bundles
remain readable without becoming current authority. It is not identity agnostic:
the legacy bundle ID must end in the exact SHA-256 content digest recorded by its
bundle manifest, and the row must still bind both manifest bytes and the evidence
metadata. Rehashing a locally consistent row under an unrelated 64-hex suffix is
therefore rejected.

This mechanism establishes local byte identity, replay, migration, and recovery
semantics. It does not establish source truth, theorem status, independent
conceptual depth, or discovery efficacy.
