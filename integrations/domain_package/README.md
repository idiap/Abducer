<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Abducer export for Lunar

This exporter packages Abducer's existing research materials in Lunar's domain-package v1 format. Upload the resulting ZIP through Lunar's domain-package import UI; Lunar allocates ownership and an imported version. Exporting itself does not contact or change a running Lunar instance.

The package declares a source-bound viewer bundle and module catalog. Lunar's **Prism** page lists all 19 workflows with typed graphs, source-file navigation and authored examples; its **Repository** page links to the same modules. Workflow visibility is independent of executable worker registration.

## Generate an archive

From the Abducer repository root, use Python 3.11–3.13 with `jsonschema`, `packaging` and `PyYAML` installed:

```sh
python -m integrations.domain_package.export \
  --repository-root . \
  --output abducer-discovery-lunar.zip
```

The destination must not already exist. The command prints a SHA-256, byte size and collection counts. It uses the Git file inventory and current worktree bytes; commit membership does not imply that dirty files equal `HEAD`. The exporter includes its own source and explicitly named integration tests before the first commit. It snapshots and validates all selected bytes, checks source stability, then atomically publishes the ZIP. Identical selected inputs produce identical archives.

## What Lunar receives

- **Repository:** source, policies, registries, documentation, locks and the 19 reviewed Prism workflow modules, with their declared evidence and skill references.
- **Skills:** full original instructions and complete selected support trees, including project-maintenance and Prism integration skills. Path-derived identities keep same-named skills distinct.
- **Reports:** repository-authored Markdown, HTML/PDF/LaTeX companions and structured same-stem JSON. Non-Markdown documents have a short attachment index. Exact original text remains attached; no database revisions, run facts or provenance attestations are invented.
- **Data sources:** authored KBs and associated `InformalMathLib` memory, with actual local-file bytes.

All authored paths also remain under `repository/runtime/`, preserving their source layout. `repository/export-index.json` records exact selected sources and digests. Source paths mentioned in historical prose do not automatically become live workspace bindings. Existing resolvable Markdown attachment links are included; unavailable historical navigation is recorded in each report's metadata.

Historical absolute links are mapped only when they match one exact selected repository path; the exporter never reads the old host location. Original Markdown remains unchanged in its attachment. Nonconforming YAML front matter is preserved verbatim, with a labelled literal-field projection for catalog names/descriptions. Historical skills inside `agentic/external` remain source snapshots rather than being promoted to current catalog skills.

## Select a target and run in Lunar

Open **Discovery Marathon Loop → Run**, choose **Target**, then **Start a new run**. Select a configured model and enable **Allow declared public network reads for this run**. The runtime acquires current public literature, initializes canonical theory, then runs one authorized research cycle. Changing the target selects its new-run option. Historical runs remain available with their own readiness messages. The server validates the exact target/run pair.

The default export includes a new-run option for P versus NP and Yang–Mills, plus both historical local runs: `p-vs-np-marathon` (154 cycles) and `yang-mills-smoke-marathon` (352). Use `--marathon-run-id` to limit the historical selection. Historical runs without current canonical state remain blocked; new runs produce their own target/run-specific state.

Initialization makes six bounded Crossref/arXiv reads and uses the selected model for a charter, blind hypotheses, source assessment/rebase, three branch maturations, conceptual systems, reflection and two internally correlated adjudication panels. Each model stage retains its request, raw response and validation journal, with at most three attempts. The baseline is 13 calls (at most 39 for initialization), followed by at most six branch calls for one research cycle. Validation failures stop the run with retained diagnostics. Source abstracts remain unverified claims; internal panels do not establish independent scientific agreement.

The real canonical operators validate the resulting literature production record and commit generation one. A positive preference authorizes only its exact canonical branch identities. If all candidates require revision, the run generates the original report with zero research cycles and an explicit revision notice. It does not turn that outcome into a research success or grant branch investment.

## Execute the source workflow

The export now registers a **native Python execution hook** for Discovery Marathon Loop. Lunar calls `agentic/scripts/run_discovery_marathon.py` in an isolated writable copy of the exported research workspace. The source scheduler, canonical theory gate, branch prompts, JSON schema, retries, operator receipts, reducers and report rebuild commands are reused. The original Prism graph stays available in the viewer; its earlier seven-step model demo is no longer the execution entrypoint.

The selected model remains on Lunar's host. The adapter translates the source Responses request into the host's completion channel while retaining its prompt, schema, reasoning effort and token limit. Branch calls run sequentially because that channel has one RPC stream. One source research cycle runs per invocation. The host allows a two-hour worker budget, since the existing run has a 30-minute cycle budget before report rebuilding.

### Current research prerequisite

Existing historical runs still require a current committed canonical binding for their exact target/run. The available historical canonical projection belongs to `ym21-canonical-parent-20260721`, so it cannot authorize those runs. New-run initialization produces its own operator artifacts and receipts through the theory-first workflow. See [Discovery Marathon Operations](../../docs/operations/discovery-marathon-operations.md).

An export without that binding can be inspected and imported, but research execution stops before any model call. This is not a ready continuation of the historical run. The adapter never substitutes smoke output or an old HTML report after failure.

Once the matching committed projection and transaction store exist, export them explicitly:

```sh
python -m integrations.domain_package.export \
  --repository-root . \
  --output abducer-discovery-lunar.zip \
  --marathon-run-id yang-mills-smoke-marathon \
  --canonical-theory-cycle agentic/reports/YOUR_EXACT_COMMITTED_CYCLE.json \
  --canonical-theory-state-root agentic/state/YOUR_CANONICAL_TRANSACTION_STORE
```

These are repository-relative paths, not editable model context. Target/run mismatches fail export; the source runtime validates the full canonical commitment before scheduling. Do not rewrite old receipts or rename another run's projection to satisfy this requirement.

To package multiple authorized runs together, use `--marathon-bindings run-bindings.json`. The file maps run IDs to their exact paths, for example:

```json
{
  "p-vs-np-marathon": {
    "canonical_theory_cycle": "agentic/runs/reflective_discovery/p-vs-np/cycle-0001-result.json",
    "canonical_theory_state_root": "agentic/state/p-vs-np-canonical"
  }
}
```

These example paths must be replaced with actual committed state. Runs omitted from the map stay selectable for inspection with a blocked readiness message. Packaging a binding means its bytes are present; only the source gate can establish current research authority.

### Host and report behavior

This package requires the paired Lunar host update: optional `execute_hook` dispatch with mandatory verification, bounded model/worker timeouts, and native HTML report viewing. Older hosts reject the extended manifest. Rebuild the host worker image, backend and frontend, import the new package version, then prepare its runtime. Previously imported versions retain their old adapter.

A successful source run creates `latest.html`, `full_timeline.html`, `latest.json` and `latest.md`. Lunar verifies the HTML artifact's digest and displays the original document in an opaque sandbox with local scripts and embedded MathJax. Its tabs, timeline, equations and controls use the source renderer. Markdown remains available for report chat and source inspection. External network requests and application-origin access are unavailable inside the report frame.

Each invocation starts from the exported snapshot and writes a separate research workspace under its output directory. It does not update the local Abducer repository or automatically feed one Lunar invocation's state into the next. Continuing beyond that snapshot requires a newly authorized canonical cycle and a new state export. Full multi-invocation state management and current scientific research execution have not been verified by the adapter tests.

Use `--browse-only` for an export without execution registration.

## Source selection and validation

Selection is explicit in `export.py`. It excludes host dot-directories, secrets, virtual environments, caches, nested ZIPs/wheels, unselected `agentic/runs`, logs/traces and the canonical-cycle acceptance sandbox. `abducer-prism/vendor` is omitted because this adapter uses the image-owned Prism engine and packaged source modules. Tracked `artifacts/` files and the explicitly selected marathon run are included. Untracked files outside the selected integration and run/state paths are not implicitly published.

The canonical Lunar validator and schemas are pinned in `format/`; `FORMAT-PIN.json` and `UPSTREAM.json` record provenance. The snapshot builder derives from the supplied BioAgents exporter. No sibling checkout is needed for subsequent exports.

Run the focused regression suite from this root:

```sh
python -m unittest discover -s tests/infrastructure -p test_domain_package_export.py
```

Release verification should additionally run the resulting ZIP through the target Lunar checkout's `app.backend.domain_packages.archive.validate_archive`, exercising its bounded ZIP reader as well as the shared JSON contract. This check needs no server or database.

```sh
PYTHONDONTWRITEBYTECODE=1 python -m integrations.domain_package.verify \
  abducer-discovery-lunar.zip --lunar-root ../lunar-platform
```

The verifier compares the contract pin, original skill/support bytes, report sources and every workflow evidence record. Its JSON receipt states separately whether the archive passed, whether execution is enabled and whether a database import was attempted.

It also enforces the exact `metadata.bundle` and `metadata.catalog` links that Lunar's repository endpoints consume. A package with absent or unlinked viewer metadata now fails verification even if it otherwise satisfies the archive schema.

## Refresh graphs after changing workflow sources

The cached viewer is generated through the existing `prism-viewer` graph exporter and Prism's public parse/check/compile commands. Generation runs against an isolated source copy and performs no scientific/model execution. The dependency manifest binds all workflow modules and linked skill instructions; stale assets stop export with a regeneration instruction.

```sh
PYTHONDONTWRITEBYTECODE=1 python -m integrations.domain_package.build_viewer \
  --repository-root . \
  --viewer-root ../prism-viewer \
  --prism ../prism/.venv/bin/prism
node tests/infrastructure/lunar_viewer_frontend.mjs \
  ../lunar-platform integrations/domain_package/assets/bundle.json
```

Only regeneration needs those toolchain paths. Normal export uses the source-checked assets in `integrations/domain_package/assets/`. The JavaScript check calls Lunar's actual bundle validator, graph layout and source-navigation code for every workflow. Import a corrected ZIP as a new package version and select that version; an already imported version retains its original immutable bytes.

## Runtime compatibility checks

```sh
python -m pytest -q tests/infrastructure/test_lunar_marathon_parity.py \
  tests/infrastructure/test_domain_package_export.py
node tests/infrastructure/lunar_html_report_frontend.mjs ../lunar-platform \
  agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/full_timeline.html
python tests/infrastructure/check_lunar_marathon_worker.py \
  --archive abducer-discovery-lunar.zip --lunar-root ../lunar-platform \
  --image sha256:YOUR_UPDATED_WORKER_IMAGE_ID --output /tmp/marathon-worker-check.json
```

The worker check explicitly expects both currently unbound runs to fail before model access. Its separate controlled fixture proves native dispatch without compiling the old Prism demo. Branch transport tests exercise the original source prompts and validators. These checks do not claim a successful research cycle.

Verify full report rebuilding and section parity independently of model execution:

```sh
python tests/infrastructure/check_lunar_marathon_reports.py \
  --archive abducer-discovery-lunar.zip --lunar-root ../lunar-platform \
  --output /tmp/marathon-report-parity.json
```

This check unpacks a validated archive into temporary storage, deletes the four old report outputs, runs the original report pipeline for every selected run, and compares Markdown headings and HTML tabs against the packaged reports. Research state must remain byte-identical. Historical cycles that predate proof-depth packets remain reportable; every recorded packet is still validated. Yang–Mills-only controls remain scoped to that target. Successful report rebuilding is rendering evidence, not a newly executed research cycle.
