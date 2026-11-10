<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Repository adoption maintenance operations

These checkout tools add discoverable maintenance contracts and source-bound public views to Abducer. Existing registries, validator behavior, trace semantics and scientific workflows retain their owners. The generated [ownership catalog](../generated/repository-adoption-catalog.md) accounts for public, domain-private, project-support and Prism skills; excluded source copies remain references.

The [refactor roadmap](../plans-and-reviews/portable-repository-adoption-refactor-plan.md) explains the bounded M0–M5 migration and its preserved scope exclusions.

## Discover and validate

From the repository root, use the existing Python environment:

```sh
python3 proj_skills/scripts/repository_adoption_catalog.py --check
python3 proj_skills/scripts/repository_adoption_adapter.py validate-project-skills -- --root proj_skills
```

The adapter invokes the original validator once and returns its stdout bytes, stderr bytes and exit status. Everything after `--` belongs to the original CLI, including malformed arguments. Without `--trace-root` the adapter writes no receipts or events. The original `python3 proj_skills/scripts/validate_proj_skills.py` remains supported and unchanged.

The authored [operation sidecar](../../proj_skills/repository_adoption_operations.json) declares four fixed operations. The resolver checks the reviewed implementation paths; metadata cannot import arbitrary code. Catalog skill IDs are scoped navigation identities, not replacement public aliases. Nearby helper scripts do not make an instruction-only skill callable: `project-state-profiler` remains instruction-only.

Regenerate navigation after intentional source-contract changes:

```sh
python3 proj_skills/scripts/repository_adoption_catalog.py --write
python3 proj_skills/scripts/repository_adoption_catalog.py --check
```

Generation checks name/path agreement with canonical registries. It does not replace their full validators or certify task-taxonomy correctness.

## Record a validation and replay its result

Choose a new invocation identity for an independent execution. A retry uses a new attempt under the host's policy; replay requests the original attempt explicitly.

```sh
python3 proj_skills/scripts/repository_adoption_adapter.py validate-project-skills \
  --trace-root artifacts/adoption-demo --run-id demo-1 --invocation-id validation-1 \
  -- --root proj_skills

python3 proj_skills/scripts/repository_adoption_adapter.py validate-project-skills \
  --trace-root artifacts/adoption-demo --run-id demo-1 --invocation-id validation-1 \
  --replay -- --root proj_skills
```

Receipts live under `invocations/demo-1/validation-1/1/`; the terminal result holds the original byte streams encoded as base64, return code and request/context. Native v2 maintenance events live under `repository-adoption/runs/demo-1/`, isolated from scientific events at the selected root's `runs/`. Reusing a scientific run ID cannot append maintenance events to that scientific stream. The event references the exact result digest; execution completion does not assert scientific validation or release authority.

Older maintenance event files remain where they were written; this isolation change does not migrate or rewrite historical streams. Receipt paths remain unchanged, so explicit replay still verifies the original stored result.

Replay checks identity, arguments, working directory, implementation digest and result content before returning stored bytes. It never runs the validator. A started or corrupted receipt is not a completed result and cannot be replayed. Reusing an already reserved identity without `--replay` fails. Preserve incomplete evidence; investigate before explicitly selecting a fresh attempt.

Tracing is optional telemetry. If storage is unavailable before execution, the validator can still run without a durable receipt; this is not a global exactly-once guarantee. Optional event-writing failure cannot replace the validator's result. Existing mandatory audit or transaction requirements are unaffected; this adapter does not wrap those operations.

## Render historical evidence and check the release boundary

The view operation accepts an existing JSON document. It preserves the source file, stores its digest and original values, and creates a new output directory. Native assembled traces and monitor packets use existing Abducer presentation code; other records receive an archival view. Missing skill, rationale or reasoning mapping remains visibly missing.

```sh
python3 proj_skills/scripts/repository_adoption_views.py render-history \
  --source artifacts/adoption-demo/invocations/demo-1/validation-1/1/result.json \
  --output-dir artifacts/adoption-demo/result-view
python3 proj_skills/scripts/repository_adoption_views.py verify-view \
  --manifest artifacts/adoption-demo/result-view/manifest.json
python3 proj_skills/scripts/repository_adoption_views.py release-probe --repository-root .
```

Open `view.html` in the new directory. `projection.json` retains source records and presentation metadata; `manifest.json` binds the original source and output hashes. Hash verification detects inconsistent joins and changed content, not publisher authenticity. Keep the source available at its recorded location for verification. `--expected-sha256` optionally pins known source bytes before rendering. Existing destinations are never overwritten.

See [view formats and verification](repository-adoption-views.md) for native packet versions, archival fallbacks and source relocation behavior. The view command accepts JSON documents; assemble native JSONL events through the existing trace pipeline first.

The release probe checks the preserved unresolved projection, type/occurrence/relation ordering and documentary samples. A successful probe means the reviewed representation is preserved; it does not execute or promote a release. Validator events likewise do not acquire a named scientific workflow registration.

## Compatibility, setup and rollback

These are source-checkout tools, not new wheel entrypoints. They use the standard library and existing native scripts; the trace store retains its POSIX file-locking requirement. No provider, model, external host checkout or new package installation is needed. The tests use the repository's existing `.venv`.

To stop using the integration, return to the original validator and existing renderers. In a reviewed code rollback, remove only the additive operation sidecar, entrypoints and generated navigation belonging to this change. Keep emitted receipts and historical sources; do not reset unrelated work. Regenerated views can be replaced by publishing a new directory and changing the consumer's pointer.

The bounded milestone covers validator execution and read-only provenance. Code relocation, full executable-workflow adoption and host export remain outside its scope. Existing task-taxonomy and semantic-name baseline failures are documented in the [implementation evidence](../../.prism/implement-portable-repository-adoption/baseline-evidence.md); catalog freshness does not clear them.
