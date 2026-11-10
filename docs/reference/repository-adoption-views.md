<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Repository adoption historical views

This maintenance interface gives Abducer maintainers a portable, inspectable view of existing JSON records while preserving their original bytes. It renders recorded results; it does not execute the workflow, recompute scientific output, invoke a provider, or grant promotion authority.

Run from a checkout using its existing Python environment. The command also works from another working directory when invoked by its absolute script path. Supply an existing JSON source and a new destination directory whose parent exists:

```sh
.venv/bin/python proj_skills/scripts/repository_adoption_views.py render-history \
  --source tests/fixtures/reasoning_trace/generated/deep_review_and_reorientation.trace.json \
  --output-dir /tmp/abducer-historical-view
.venv/bin/python proj_skills/scripts/repository_adoption_views.py verify-view \
  --manifest /tmp/abducer-historical-view/manifest.json
```

Choose an unused output directory. Existing destinations and final symlinks are rejected, so rerunning cannot overwrite either historical records or an earlier projection. Explicit parent aliases such as macOS `/tmp` resolve to their real directory. Add `--expected-sha256 HEX` when a previously recorded source digest is available; disagreement fails before publication.

## Which existing routes run

A native assembled trace (`schema_version: "2.0"`, with identity, events and declared route) uses the existing `agentic/scripts/build_public_reasoning_monitor_packet.py` builder and `generate_public_reasoning_trace_html.py` renderer through fixed, reviewed callables. The builder receives the captured JSON value, not a fresh workflow invocation. Its complete historical identity and event timeline must remain unchanged.

An existing native monitor packet (`schema_version: "1.0"`, with identity, timeline and lens) goes directly to the same renderer. These two presentation formats are distinct from the public reasoning event schema `2.0.0` and the adoption kit's `repository-adoption.example/v2` format.

Other valid JSON, including a standalone maintenance terminal record, receives an archival HTML view. Native-looking histories missing recorded run/event identities also use this archival route. Missing identifiers stay absent. Contradictory native run identities and unsupported native versions are errors. JSONL and binary histories are not supported by this command; retain them in their original store.

A source record with no skill, reasoning mapping or public rationale displays “No skill recorded”, “Unassigned” and “Rationale not recorded”. These are display labels, not new metadata in the historical record. The renderer does not consult today's skill catalog to fill historical gaps. It does not register a maintenance validator as a named scientific workflow.

## Artifacts and interpretation

The new directory contains:

- `projection.json`: versioned sidecar with source locator/SHA-256, exact parsed source document, unchanged individual records and their JSON pointers, explicit display labels, rendering context and optional native packet.
- `view.html`: self-contained HTML produced by the native renderer or the archival fallback, with escaped historical record text.
- `manifest.json`: source digest, fixed output filenames, output byte counts/digests and rendering-context digest.

The original source file is never rewritten. For native trace rendering, the sidecar snapshots the selected lens registry and the builder/renderer hashes as **presentation context**. These current display choices do not claim to be historical skill metadata. Graph/evidence presentation identifiers created by the established builder are not newly observed invocation identities.

`verify-view` checks that the original source still exists at its recorded absolute locator, source bytes match, output bytes match, source records/pointers agree, native identity/timeline agree, the direct native packet is unchanged, and embedded HTML packet data matches the sidecar. JSON comparisons retain type distinctions such as `1` versus `true`. A changed or missing source, modified artifact, unsupported version, contradictory join or output-path escape fails verification.

These checks establish internal integrity and detect drift. They are not signatures or host attestations, and cannot establish authenticity against someone replacing all source/manifest evidence. Keep trusted source digests separately when authenticity matters. Moving the original source invalidates its recorded locator; generate a new projection from the new location instead of rewriting the old evidence.

## Protected release-promotion probe

```sh
.venv/bin/python proj_skills/scripts/repository_adoption_views.py release-probe \
  --repository-root .
```

This read-only probe compares the four `release_promotion_loop` semantic layers against the reviewed baseline, including symbols, indentation, types, order and bounded return. It also checks the manifest's disposition routes, unresolved projection blocker, absence of executable materialization/main layers, and simulated sample hash/claim. Comment-only lines, blank lines and trailing spaces do not alter the semantic baseline.

A `preserved` result means the reviewed representation and unresolved boundary remain intact. It does not execute `UnresolvedReleaseProposalProjection`, resolve that gap, certify sample behavior, or promote a release. An intentional future semantic change needs its own review and baseline update.

## Regression evidence

The dedicated suite exercises the actual CLI and native builder/renderer paths, source/identity/status preservation, explicit missing history, cross-run conflicts, malformed versions, digest failures, rehashed contradictory sidecars, HTML escaping, final symlink/path-escape rejection, portable parent aliases and release-authority mutations:

```sh
.venv/bin/python -m pytest tests/reporting/test_repository_adoption_views.py \
  tests/reporting/test_named_workflow_trace_html.py -q
```
